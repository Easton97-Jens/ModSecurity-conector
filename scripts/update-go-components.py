#!/usr/bin/env python3
"""Resolve and validate the one bounded Go module security-update bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, TextIO


MAX_COMPONENT_FILE_BYTES = 1024 * 1024
BASELINE_FRAME_SEPARATOR = b"\0"
MAX_BASELINE_FRAME_BYTES = (MAX_COMPONENT_FILE_BYTES * 2) + len(BASELINE_FRAME_SEPARATOR)
GO_MOD_FILENAME = "go.mod"
GO_SUM_FILENAME = "go.sum"
GO_SUM_ROOT_SUFFIX = ""
GO_SUM_GO_MOD_SUFFIX = "/go.mod"
GRPC_MODULE = "google.golang.org/grpc"
SYS_MODULE = "golang.org/x/sys"
NET_MODULE = "golang.org/x/net"
TEXT_MODULE = "golang.org/x/text"
MODULE_VERSION_RE = re.compile(
    r"^v(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)$",
    re.ASCII,
)
GO_SUM_ENTRY_RE = re.compile(
    r"^(?P<module>[A-Za-z0-9._/-]+)\s+"
    r"(?P<version>v(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*))"
    r"(?P<go_mod>/go\.mod)?\s+h1:[A-Za-z0-9+/=]+$",
    re.ASCII,
)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$", re.ASCII)


class ComponentError(RuntimeError):
    """Raised when the bounded component policy cannot be proven."""


@dataclass(frozen=True, order=True)
class ModuleVersion:
    """One exact, stable Go module version."""

    major: int
    minor: int
    patch: int

    def __str__(self) -> str:
        return f"v{self.major}.{self.minor}.{self.patch}"


GRPC_TARGET_VERSION = ModuleVersion(1, 83, 2)
SYS_TARGET_VERSION = ModuleVersion(0, 47, 0)
NET_TARGET_VERSION = ModuleVersion(0, 58, 0)
TEXT_TARGET_VERSION = ModuleVersion(0, 41, 0)


@dataclass(frozen=True)
class RequirementUpdate:
    """One exact go.mod requirement transition allowed in a component bundle."""

    dependency: str
    baseline_version: ModuleVersion
    target_version: ModuleVersion
    indirect: bool


@dataclass(frozen=True)
class GoComponent:
    """The sole Go module update bundle permitted to enter the workflow."""

    directory: Path
    updates: tuple[RequirementUpdate, ...]

    @property
    def primary_update(self) -> RequirementUpdate:
        return self.updates[0]


@dataclass(frozen=True)
class RequirementLine:
    """One canonical requirement line in the repository's go.mod."""

    dependency: str
    line_index: int
    line_ending: str
    version: ModuleVersion
    indirect: bool


@dataclass(frozen=True)
class ComponentResolution:
    """The deterministic decision produced from a trusted go.mod."""

    component: GoComponent
    primary_version: ModuleVersion

    @property
    def update_available(self) -> bool:
        return self.primary_version < self.component.primary_update.target_version


GRPC_COMPONENT = GoComponent(
    directory=Path("connectors/envoy/ext_proc"),
    updates=(
        RequirementUpdate(
            dependency=GRPC_MODULE,
            baseline_version=ModuleVersion(1, 83, 1),
            target_version=GRPC_TARGET_VERSION,
            indirect=False,
        ),
        RequirementUpdate(
            dependency=SYS_MODULE,
            baseline_version=ModuleVersion(0, 46, 0),
            target_version=SYS_TARGET_VERSION,
            indirect=False,
        ),
        RequirementUpdate(
            dependency=NET_MODULE,
            baseline_version=ModuleVersion(0, 56, 0),
            target_version=NET_TARGET_VERSION,
            indirect=True,
        ),
        RequirementUpdate(
            dependency=TEXT_MODULE,
            baseline_version=ModuleVersion(0, 39, 0),
            target_version=TEXT_TARGET_VERSION,
            indirect=True,
        ),
    ),
)
COMPONENTS = (GRPC_COMPONENT,)
TRUSTED_TARGET_GO_SUM_ENTRIES = {
    (NET_MODULE, str(NET_TARGET_VERSION), GO_SUM_ROOT_SUFFIX): "h1:ynWG7rqYi4ccpTEuPZ2QGWHktVEM9DMCj9yzDE0Q7To=",
    (NET_MODULE, str(NET_TARGET_VERSION), GO_SUM_GO_MOD_SUFFIX): "h1:YwCddHnFlT7eLQqVprV19OnhLGtc5xOKgE0RyqgfWAU=",
    (SYS_MODULE, str(SYS_TARGET_VERSION), GO_SUM_ROOT_SUFFIX): "h1:o7XGOvZQCADBQQ4Y7VNq2dRWQR7JmOUW8Kxx4ZsNgWs=",
    (SYS_MODULE, str(SYS_TARGET_VERSION), GO_SUM_GO_MOD_SUFFIX): "h1:4GL1E5IUh+htKOUEOaiffhrAeqysfVGipDYzABqnCmw=",
    (TEXT_MODULE, str(TEXT_TARGET_VERSION), GO_SUM_ROOT_SUFFIX): "h1:vz/seA0lnX87Othu2f/0L24RcgrXD9/YFTSuGjj3rH8=",
    (TEXT_MODULE, str(TEXT_TARGET_VERSION), GO_SUM_GO_MOD_SUFFIX): "h1:jvf1O8ajNzZqhSrQBPbutR/EB83Cc0CFrezNQIwbb5M=",
    (GRPC_MODULE, str(GRPC_TARGET_VERSION), GO_SUM_ROOT_SUFFIX): "h1:EManeRomTObA0BU7I8vXgg/78uE5MJ9M8B39EX2WscU=",
    (GRPC_MODULE, str(GRPC_TARGET_VERSION), GO_SUM_GO_MOD_SUFFIX): "h1:YPI1hK3kDked6iHvgX3tR0y+nX/qpMFKhPgFsokw1S8=",
}


def parse_module_version(value: object) -> ModuleVersion:
    """Parse only a stable `vMAJOR.MINOR.PATCH` Go module version."""

    if type(value) is not str:
        raise ComponentError("component version must be an exact stable string")
    match = MODULE_VERSION_RE.fullmatch(value)
    if match is None:
        raise ComponentError("component version must be vMAJOR.MINOR.PATCH without a suffix")
    return ModuleVersion(
        major=int(match.group("major")),
        minor=int(match.group("minor")),
        patch=int(match.group("patch")),
    )


def repository_root() -> Path:
    """Return the repository root determined from this checked-in script."""

    return Path(__file__).resolve().parents[1]


def _require_real_directory(path: Path, label: str) -> None:
    try:
        path_stat = os.lstat(path)
    except OSError as error:
        raise ComponentError(f"{label} cannot be inspected safely") from error
    if stat.S_ISLNK(path_stat.st_mode) or not stat.S_ISDIR(path_stat.st_mode):
        raise ComponentError(f"{label} must be a real directory")


def read_regular_file(path: Path, label: str) -> bytes:
    """Read a small regular file without following a replacement symlink."""

    try:
        before_open = os.lstat(path)
    except OSError as error:
        raise ComponentError(f"{label} cannot be inspected safely") from error
    if not stat.S_ISREG(before_open.st_mode):
        raise ComponentError(f"{label} must be a regular non-symlink file")

    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise ComponentError(f"platform cannot safely open {label} without following symlinks")
    flags = os.O_RDONLY | nofollow
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    descriptor: int | None = None
    try:
        descriptor = os.open(path, flags)
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode) or not os.path.samestat(before_open, opened):
            raise ComponentError(f"{label} changed while being opened")
        source = os.fdopen(descriptor, "rb")
        descriptor = None
        with source:
            body = source.read(MAX_COMPONENT_FILE_BYTES + 1)
    except ComponentError:
        raise
    except OSError as error:
        raise ComponentError(f"{label} cannot be read safely") from error
    finally:
        if descriptor is not None:
            os.close(descriptor)

    if len(body) > MAX_COMPONENT_FILE_BYTES:
        raise ComponentError(f"{label} exceeds the size limit")
    return body


def decode_utf8(body: bytes, label: str) -> str:
    """Decode a bounded text input without normalizing its contents."""

    try:
        return body.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ComponentError(f"{label} is not UTF-8") from error


def component_path(root: Path, component: GoComponent, filename: str) -> Path:
    """Derive a static, repository-contained component file path."""

    _require_real_directory(root, "repository root")
    if component.directory.is_absolute():
        raise ComponentError("component directory must be relative")
    directory = root
    for part in component.directory.parts:
        if part in {"", ".", ".."}:
            raise ComponentError("component directory contains an unsafe path segment")
        directory = directory / part
        _require_real_directory(directory, f"component directory {directory}")
    candidate = directory / filename
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise ComponentError("component path escapes the repository root") from error
    return candidate


def validate_component_files(root: Path, component: GoComponent = GRPC_COMPONENT) -> dict[str, object]:
    """Prove that the writable component inputs are regular in-repository files."""

    go_mod_path = component_path(root, component, GO_MOD_FILENAME)
    go_sum_path = component_path(root, component, GO_SUM_FILENAME)
    read_regular_file(go_mod_path, str(go_mod_path))
    read_regular_file(go_sum_path, str(go_sum_path))
    return {
        "status": "valid",
        "directory": str(component.directory),
        "files": [GO_MOD_FILENAME, GO_SUM_FILENAME],
    }


def _parse_component_requirement_line(
    raw_line: str,
    index: int,
    updates: dict[str, RequirementUpdate],
) -> RequirementLine | None:
    """Parse one approved requirement line without interpreting other dependencies."""

    line = raw_line.rstrip("\r\n")
    dependency = line.lstrip().split(" ", 1)[0]
    update = updates.get(dependency)
    if update is None:
        return None
    match = re.fullmatch(
        rf"\t{re.escape(dependency)} (?P<version>\S+)(?P<suffix> // indirect)?",
        line,
        re.ASCII,
    )
    if match is None:
        raise ComponentError(f"{dependency} must use one canonical go.mod requirement line")
    indirect = match.group("suffix") is not None
    if indirect != update.indirect:
        raise ComponentError(f"{dependency} has an unexpected indirect marker")
    return RequirementLine(
        dependency=dependency,
        line_index=index,
        line_ending=raw_line[len(line) :],
        version=parse_module_version(match.group("version")),
        indirect=indirect,
    )


def component_requirements(go_mod: str, component: GoComponent) -> dict[str, RequirementLine]:
    """Read the exact canonical lines for every explicit bundle requirement."""

    updates = {update.dependency: update for update in component.updates}
    in_require_block = False
    result: dict[str, RequirementLine] = {}
    for index, raw_line in enumerate(go_mod.splitlines(keepends=True)):
        line = raw_line.rstrip("\r\n")
        if line == "require (":
            if in_require_block:
                raise ComponentError("go.mod contains nested require blocks")
            in_require_block = True
            continue
        if line == ")":
            in_require_block = False
            continue
        if not in_require_block:
            continue
        requirement = _parse_component_requirement_line(raw_line, index, updates)
        if requirement is None:
            continue
        if requirement.dependency in result:
            raise ComponentError(f"go.mod contains duplicate {requirement.dependency} requirements")
        result[requirement.dependency] = requirement
    if in_require_block:
        raise ComponentError("go.mod has an unterminated require block")
    missing = sorted(set(updates) - set(result))
    if missing:
        raise ComponentError(f"go.mod lacks required component entries: {', '.join(missing)}")
    return result


def resolve_component(root: Path, component: GoComponent = GRPC_COMPONENT) -> ComponentResolution:
    """Resolve one explicit component bundle from a trusted repository checkout."""

    go_mod_path = component_path(root, component, GO_MOD_FILENAME)
    go_mod = decode_utf8(read_regular_file(go_mod_path, str(go_mod_path)), str(go_mod_path))
    requirements = component_requirements(go_mod, component)
    primary = requirements[component.primary_update.dependency]
    if primary.version < component.primary_update.target_version:
        for update in component.updates:
            if requirements[update.dependency].version != update.baseline_version:
                raise ComponentError(
                    f"component baseline is inconsistent for {update.dependency}; refusing an open-ended update"
                )
    else:
        for update in component.updates:
            if requirements[update.dependency].version < update.target_version:
                raise ComponentError(
                    f"component floor is inconsistent for {update.dependency}; refusing a partial update"
                )
    return ComponentResolution(component=component, primary_version=primary.version)


def resolution_payload(resolution: ComponentResolution) -> dict[str, object]:
    """Return the fixed JSON shape consumed by the trusted workflow resolver."""

    available = resolution.update_available
    component = resolution.component
    primary = component.primary_update
    return {
        "status": "update_available" if available else "current",
        "update_available": available,
        "components": [
            {
                "directory": str(component.directory),
                "dependency": primary.dependency,
                "current_version": str(resolution.primary_version),
                "target_version": str(primary.target_version),
                "update_available": available,
            }
        ],
    }


def expected_go_mod_after_update(baseline_go_mod: str, component: GoComponent) -> str:
    """Allow only the exact requirement bundle mandated by grpc v1.83.2."""

    requirements = component_requirements(baseline_go_mod, component)
    lines = baseline_go_mod.splitlines(keepends=True)
    for update in component.updates:
        requirement = requirements[update.dependency]
        if requirement.version != update.baseline_version:
            raise ComponentError(f"component baseline is inconsistent for {update.dependency}")
        suffix = " // indirect" if update.indirect else ""
        lines[requirement.line_index] = (
            f"\t{update.dependency} {update.target_version}{suffix}{requirement.line_ending}"
        )
    return "".join(lines)


def _read_unique_go_sum_entries(go_sum: str, label: str) -> list[str]:
    """Split one go.sum file while refusing duplicate checksum entries."""

    entries = go_sum.splitlines()
    if len(entries) != len(set(entries)):
        raise ComponentError(f"{label} go.sum contains duplicate entries")
    return entries


def _calculate_go_sum_changes(
    baseline_entries: list[str],
    candidate_entries: list[str],
) -> tuple[set[str], set[str]]:
    """Calculate the only checksum rows a component candidate may change."""

    removed = set(baseline_entries) - set(candidate_entries)
    added = set(candidate_entries) - set(baseline_entries)
    if not added:
        raise ComponentError("component candidate did not add checksum entries")
    return removed, added


def _allowed_go_sum_versions(component: GoComponent) -> set[tuple[str, str]]:
    """List the baseline and target versions trusted for the bounded bundle."""

    return {
        (update.dependency, str(version))
        for update in component.updates
        for version in (update.baseline_version, update.target_version)
    }


def _validate_changed_go_sum_entries(
    changed_entries: set[str],
    allowed_versions: set[tuple[str, str]],
) -> None:
    """Reject malformed or unapproved checksum changes before publication."""

    for entry in sorted(changed_entries):
        match = GO_SUM_ENTRY_RE.fullmatch(entry)
        if match is None:
            raise ComponentError("component candidate changed a malformed go.sum entry")
        if (match.group("module"), match.group("version")) not in allowed_versions:
            raise ComponentError("component candidate changed an unapproved go.sum entry")


def _require_trusted_target_checksum(
    candidate_entries: list[str],
    update: RequirementUpdate,
    suffix: str,
) -> None:
    """Require the exact trusted checksum for one target module/version row."""

    key = (update.dependency, str(update.target_version), suffix)
    expected_checksum = TRUSTED_TARGET_GO_SUM_ENTRIES.get(key)
    if expected_checksum is None:
        raise ComponentError(f"component policy lacks a trusted checksum for {update.dependency}")
    expected_entry = f"{update.dependency} {update.target_version}{suffix} {expected_checksum}"
    matching_entries = [
        entry
        for entry in candidate_entries
        if entry.startswith(f"{update.dependency} {update.target_version}{suffix} ")
    ]
    if matching_entries != [expected_entry]:
        raise ComponentError(f"component candidate lacks a trusted target checksum for {update.dependency}")


def _validate_trusted_target_checksums(candidate_entries: list[str], component: GoComponent) -> None:
    """Bind every target dependency to both trusted Go checksum rows."""

    for update in component.updates:
        for suffix in (GO_SUM_ROOT_SUFFIX, GO_SUM_GO_MOD_SUFFIX):
            _require_trusted_target_checksum(candidate_entries, update, suffix)


def validate_go_sum_update(
    baseline_go_sum: str,
    candidate_go_sum: str,
    *,
    component: GoComponent,
) -> None:
    """Allow checksum changes only for the exact declared component bundle."""

    baseline_entries = _read_unique_go_sum_entries(baseline_go_sum, "baseline")
    candidate_entries = _read_unique_go_sum_entries(candidate_go_sum, "candidate")
    removed, added = _calculate_go_sum_changes(baseline_entries, candidate_entries)
    _validate_changed_go_sum_entries(removed | added, _allowed_go_sum_versions(component))
    _validate_trusted_target_checksums(candidate_entries, component)


def validate_component_candidate(
    baseline_go_mod: bytes,
    candidate_go_mod: bytes,
    baseline_go_sum: bytes,
    candidate_go_sum: bytes,
    component: GoComponent = GRPC_COMPONENT,
) -> dict[str, object]:
    """Validate a generated bundle candidate and bind its exact file hashes."""

    baseline_go_mod_text = decode_utf8(baseline_go_mod, "baseline go.mod")
    candidate_go_mod_text = decode_utf8(candidate_go_mod, "candidate go.mod")
    baseline_go_sum_text = decode_utf8(baseline_go_sum, "baseline go.sum")
    candidate_go_sum_text = decode_utf8(candidate_go_sum, "candidate go.sum")
    expected_go_mod = expected_go_mod_after_update(baseline_go_mod_text, component)
    if candidate_go_mod_text != expected_go_mod:
        raise ComponentError("component candidate changed go.mod outside the approved bundle")
    candidate_requirements = component_requirements(candidate_go_mod_text, component)
    for update in component.updates:
        if candidate_requirements[update.dependency].version != update.target_version:
            raise ComponentError(f"component candidate lacks the target requirement for {update.dependency}")
    validate_go_sum_update(baseline_go_sum_text, candidate_go_sum_text, component=component)
    primary = component.primary_update
    return {
        "status": "valid",
        "directory": str(component.directory),
        "dependency": primary.dependency,
        "baseline_version": str(primary.baseline_version),
        "target_version": str(primary.target_version),
        "go_mod_sha256": hashlib.sha256(candidate_go_mod).hexdigest(),
        "go_sum_sha256": hashlib.sha256(candidate_go_sum).hexdigest(),
    }


def require_expected_candidate_hashes(
    payload: dict[str, object],
    *,
    expected_go_mod_sha256: str | None,
    expected_go_sum_sha256: str | None,
) -> None:
    """Bind a regenerated candidate to the independently validated hashes."""

    expected = {
        "go_mod_sha256": expected_go_mod_sha256,
        "go_sum_sha256": expected_go_sum_sha256,
    }
    for field, value in expected.items():
        if value is None:
            continue
        if SHA256_RE.fullmatch(value) is None:
            raise ComponentError(f"expected {field} must be a lowercase SHA-256 digest")
        if payload.get(field) != value:
            raise ComponentError("component candidate differs from independently validated content")


def emit(payload: dict[str, object], output: TextIO) -> None:
    """Emit a stable, payload-safe JSON result."""

    print(json.dumps(payload, sort_keys=True, separators=(",", ":")), file=output)


def build_arg_parser() -> argparse.ArgumentParser:
    """Build the fail-closed, non-mutating command modes."""

    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="resolve the approved component bundle")
    mode.add_argument(
        "--validate-candidate",
        action="store_true",
        help="validate a generated go.mod/go.sum candidate without modifying it",
    )
    mode.add_argument(
        "--validate-component-files",
        action="store_true",
        help="prove component go.mod/go.sum are safe regular files before a writer runs",
    )
    parser.add_argument(
        "--repository-root",
        type=Path,
        help="repository root for --check, --validate-candidate, or --validate-component-files",
    )
    parser.add_argument("--expected-go-mod-sha256")
    parser.add_argument("--expected-go-sum-sha256")
    parser.add_argument("--json", action="store_true", help="emit the stable JSON result")
    return parser


def read_baseline_frame(source: BinaryIO) -> tuple[bytes, bytes]:
    """Read the two baseline files from one bounded, NUL-delimited byte frame."""

    try:
        frame = source.read(MAX_BASELINE_FRAME_BYTES + 1)
    except (OSError, ValueError) as error:
        raise ComponentError("baseline candidate frame cannot be read") from error
    if type(frame) is not bytes:
        raise ComponentError("baseline candidate frame must be binary")
    if len(frame) > MAX_BASELINE_FRAME_BYTES:
        raise ComponentError("baseline candidate frame exceeds the size limit")
    if frame.count(BASELINE_FRAME_SEPARATOR) != 1:
        raise ComponentError("baseline candidate frame must contain exactly one separator")
    baseline_go_mod, baseline_go_sum = frame.split(BASELINE_FRAME_SEPARATOR)
    if len(baseline_go_mod) > MAX_COMPONENT_FILE_BYTES or len(baseline_go_sum) > MAX_COMPONENT_FILE_BYTES:
        raise ComponentError("baseline component file exceeds the size limit")
    return baseline_go_mod, baseline_go_sum


def candidate_inputs(root: Path, source: BinaryIO) -> tuple[bytes, bytes, bytes, bytes]:
    """Read the baseline frame and static, repository-contained candidate files."""

    baseline_go_mod, baseline_go_sum = read_baseline_frame(source)
    candidate_go_mod_path = component_path(root, GRPC_COMPONENT, GO_MOD_FILENAME)
    candidate_go_sum_path = component_path(root, GRPC_COMPONENT, GO_SUM_FILENAME)
    candidate_go_mod = read_regular_file(candidate_go_mod_path, str(candidate_go_mod_path))
    candidate_go_sum = read_regular_file(candidate_go_sum_path, str(candidate_go_sum_path))
    return baseline_go_mod, candidate_go_mod, baseline_go_sum, candidate_go_sum


def _select_repository_root(args: argparse.Namespace, root: Path | None) -> Path:
    """Select an injected root before the CLI value and script-derived default."""

    selected_root = root if root is not None else args.repository_root
    if selected_root is None:
        selected_root = repository_root()
    return Path(selected_root)


def _validate_candidate_mode(
    args: argparse.Namespace,
    selected_root: Path,
    input_stream: BinaryIO | None,
) -> dict[str, object]:
    """Validate one fixed component candidate and bind any expected hashes."""

    selected_input = sys.stdin.buffer if input_stream is None else input_stream
    payload = validate_component_candidate(*candidate_inputs(selected_root, selected_input))
    require_expected_candidate_hashes(
        payload,
        expected_go_mod_sha256=args.expected_go_mod_sha256,
        expected_go_sum_sha256=args.expected_go_sum_sha256,
    )
    return payload


def _run_mode(
    args: argparse.Namespace,
    root: Path | None,
    input_stream: BinaryIO | None,
) -> dict[str, object]:
    """Run the one selected fail-closed CLI mode."""

    selected_root = _select_repository_root(args, root)
    if args.check:
        return resolution_payload(resolve_component(selected_root))
    if args.validate_candidate:
        return _validate_candidate_mode(args, selected_root, input_stream)
    return validate_component_files(selected_root)


def main(
    argv: list[str] | None = None,
    *,
    root: Path | None = None,
    output: TextIO | None = None,
    input_stream: BinaryIO | None = None,
) -> int:
    """Run the resolver or candidate validator and fail closed on malformed input."""

    args = build_arg_parser().parse_args(argv)
    stream = sys.stdout if output is None else output
    try:
        payload = _run_mode(args, root, input_stream)
    except ComponentError as error:
        payload = {"error": str(error), "status": "error"}
        status = 1
    except Exception:
        payload = {"error": "component updater failed closed", "status": "error"}
        status = 1
    else:
        status = 0
    if args.json:
        emit(payload, stream)
    else:
        print(payload["status"], file=stream)
    return status


if __name__ == "__main__":
    raise SystemExit(main())
