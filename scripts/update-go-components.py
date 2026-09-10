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
from typing import TextIO


MAX_COMPONENT_FILE_BYTES = 1024 * 1024
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
TRUSTED_TARGET_GO_SUM_ENTRIES = {
    ("golang.org/x/net", "v0.58.0", ""): "h1:ynWG7rqYi4ccpTEuPZ2QGWHktVEM9DMCj9yzDE0Q7To=",
    ("golang.org/x/net", "v0.58.0", "/go.mod"): "h1:YwCddHnFlT7eLQqVprV19OnhLGtc5xOKgE0RyqgfWAU=",
    ("golang.org/x/sys", "v0.47.0", ""): "h1:o7XGOvZQCADBQQ4Y7VNq2dRWQR7JmOUW8Kxx4ZsNgWs=",
    ("golang.org/x/sys", "v0.47.0", "/go.mod"): "h1:4GL1E5IUh+htKOUEOaiffhrAeqysfVGipDYzABqnCmw=",
    ("golang.org/x/text", "v0.41.0", ""): "h1:vz/seA0lnX87Othu2f/0L24RcgrXD9/YFTSuGjj3rH8=",
    ("golang.org/x/text", "v0.41.0", "/go.mod"): "h1:jvf1O8ajNzZqhSrQBPbutR/EB83Cc0CFrezNQIwbb5M=",
    ("google.golang.org/grpc", "v1.83.2", ""): "h1:EManeRomTObA0BU7I8vXgg/78uE5MJ9M8B39EX2WscU=",
    ("google.golang.org/grpc", "v1.83.2", "/go.mod"): "h1:YPI1hK3kDked6iHvgX3tR0y+nX/qpMFKhPgFsokw1S8=",
}


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
            dependency="google.golang.org/grpc",
            baseline_version=ModuleVersion(1, 83, 1),
            target_version=ModuleVersion(1, 83, 2),
            indirect=False,
        ),
        RequirementUpdate(
            dependency="golang.org/x/sys",
            baseline_version=ModuleVersion(0, 46, 0),
            target_version=ModuleVersion(0, 47, 0),
            indirect=False,
        ),
        RequirementUpdate(
            dependency="golang.org/x/net",
            baseline_version=ModuleVersion(0, 56, 0),
            target_version=ModuleVersion(0, 58, 0),
            indirect=True,
        ),
        RequirementUpdate(
            dependency="golang.org/x/text",
            baseline_version=ModuleVersion(0, 39, 0),
            target_version=ModuleVersion(0, 41, 0),
            indirect=True,
        ),
    ),
)
COMPONENTS = (GRPC_COMPONENT,)


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

    go_mod_path = component_path(root, component, "go.mod")
    go_sum_path = component_path(root, component, "go.sum")
    read_regular_file(go_mod_path, str(go_mod_path))
    read_regular_file(go_sum_path, str(go_sum_path))
    return {
        "status": "valid",
        "directory": str(component.directory),
        "files": ["go.mod", "go.sum"],
    }


def component_requirements(go_mod: str, component: GoComponent) -> dict[str, RequirementLine]:
    """Read the exact canonical lines for every explicit bundle requirement."""

    updates = {update.dependency: update for update in component.updates}
    in_require_block = False
    result: dict[str, RequirementLine] = {}
    for index, raw_line in enumerate(go_mod.splitlines(keepends=True)):
        line = raw_line.rstrip("\r\n")
        line_ending = raw_line[len(line) :]
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
        stripped = line.lstrip()
        dependency = stripped.split(" ", 1)[0]
        update = updates.get(dependency)
        if update is None:
            continue
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
        if dependency in result:
            raise ComponentError(f"go.mod contains duplicate {dependency} requirements")
        result[dependency] = RequirementLine(
            dependency=dependency,
            line_index=index,
            line_ending=line_ending,
            version=parse_module_version(match.group("version")),
            indirect=indirect,
        )
    if in_require_block:
        raise ComponentError("go.mod has an unterminated require block")
    missing = sorted(set(updates) - set(result))
    if missing:
        raise ComponentError(f"go.mod lacks required component entries: {', '.join(missing)}")
    return result


def resolve_component(root: Path, component: GoComponent = GRPC_COMPONENT) -> ComponentResolution:
    """Resolve one explicit component bundle from a trusted repository checkout."""

    go_mod_path = component_path(root, component, "go.mod")
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


def validate_go_sum_update(
    baseline_go_sum: str,
    candidate_go_sum: str,
    *,
    component: GoComponent,
) -> None:
    """Allow checksum changes only for the exact declared component bundle."""

    baseline_entries = baseline_go_sum.splitlines()
    candidate_entries = candidate_go_sum.splitlines()
    if len(baseline_entries) != len(set(baseline_entries)):
        raise ComponentError("baseline go.sum contains duplicate entries")
    if len(candidate_entries) != len(set(candidate_entries)):
        raise ComponentError("candidate go.sum contains duplicate entries")
    removed = set(baseline_entries) - set(candidate_entries)
    added = set(candidate_entries) - set(baseline_entries)
    if not added:
        raise ComponentError("component candidate did not add checksum entries")

    allowed_versions = {
        (update.dependency, str(version))
        for update in component.updates
        for version in (update.baseline_version, update.target_version)
    }
    for entry in [*sorted(removed), *sorted(added)]:
        match = GO_SUM_ENTRY_RE.fullmatch(entry)
        if match is None:
            raise ComponentError("component candidate changed a malformed go.sum entry")
        if (match.group("module"), match.group("version")) not in allowed_versions:
            raise ComponentError("component candidate changed an unapproved go.sum entry")

    for update in component.updates:
        for suffix in ("", "/go.mod"):
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
        help="repository root for --check or --validate-component-files",
    )
    parser.add_argument("--baseline-go-mod", type=Path)
    parser.add_argument("--candidate-go-mod", type=Path)
    parser.add_argument("--baseline-go-sum", type=Path)
    parser.add_argument("--candidate-go-sum", type=Path)
    parser.add_argument("--expected-go-mod-sha256")
    parser.add_argument("--expected-go-sum-sha256")
    parser.add_argument("--json", action="store_true", help="emit the stable JSON result")
    return parser


def candidate_inputs(args: argparse.Namespace) -> tuple[bytes, bytes, bytes, bytes]:
    """Read exactly the four regular files required for candidate validation."""

    values = (
        (args.baseline_go_mod, "baseline go.mod"),
        (args.candidate_go_mod, "candidate go.mod"),
        (args.baseline_go_sum, "baseline go.sum"),
        (args.candidate_go_sum, "candidate go.sum"),
    )
    if any(path is None for path, _label in values):
        raise ComponentError("candidate validation requires all baseline and candidate module files")
    baseline_go_mod = read_regular_file(args.baseline_go_mod, "baseline go.mod")
    candidate_go_mod = read_regular_file(args.candidate_go_mod, "candidate go.mod")
    baseline_go_sum = read_regular_file(args.baseline_go_sum, "baseline go.sum")
    candidate_go_sum = read_regular_file(args.candidate_go_sum, "candidate go.sum")
    return baseline_go_mod, candidate_go_mod, baseline_go_sum, candidate_go_sum


def main(
    argv: list[str] | None = None,
    *,
    root: Path | None = None,
    output: TextIO | None = None,
) -> int:
    """Run the resolver or candidate validator and fail closed on malformed input."""

    args = build_arg_parser().parse_args(argv)
    stream = sys.stdout if output is None else output
    try:
        if args.check or args.validate_component_files:
            selected_root = root if root is not None else args.repository_root
            if selected_root is None:
                selected_root = repository_root()
            selected_root = Path(selected_root)
            if args.check:
                payload = resolution_payload(resolve_component(selected_root))
            else:
                payload = validate_component_files(selected_root)
        else:
            payload = validate_component_candidate(*candidate_inputs(args))
            require_expected_candidate_hashes(
                payload,
                expected_go_mod_sha256=args.expected_go_mod_sha256,
                expected_go_sum_sha256=args.expected_go_sum_sha256,
            )
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
