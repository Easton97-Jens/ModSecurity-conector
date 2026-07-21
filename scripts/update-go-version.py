#!/usr/bin/env python3
"""Safely check or update the Parent's pinned Go 1.26 patch contract."""

from __future__ import annotations

import argparse
import json
import os
import re
import secrets
import stat
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import TextIO


CANONICAL_RELEASE_API_URL = "https://go.dev/dl/?mode=json&include=all"
RELEASE_API_URL = CANONICAL_RELEASE_API_URL
MODULE_PATHS = (
    Path("connectors/envoy/ext_proc/go.mod"),
    Path("connectors/traefik/native_middleware/go.mod"),
)
CODEQL_WORKFLOW_PATH = Path(".github/workflows/ci-security-codeql.yml")
TARGET_PATHS = (*MODULE_PATHS, CODEQL_WORKFLOW_PATH)
# The official ``include=all`` catalog is intentionally bounded but contains
# all maintained patch history needed to select the 1.26 series after later
# Go minors ship.  Its current legitimate payload exceeds 2 MiB.
MAX_METADATA_BYTES = 8 * 1024 * 1024
MAX_TARGET_BYTES = 2 * 1024 * 1024
NETWORK_TIMEOUT_SECONDS = 15
VERSION_RE = re.compile(r"^1\.26\.(?P<patch>0|[1-9]\d*)$", re.ASCII)
RELEASE_VERSION_RE = re.compile(
    r"^go(?P<major>[1-9]\d*)(?:\.(?P<minor>0|[1-9]\d*)(?:\.(?P<patch>0|[1-9]\d*))?)?$",
    re.ASCII,
)
GO_DIRECTIVE_RE = re.compile(
    r"^(?P<prefix>go\s+)(?P<version>[^\s#]+)(?P<suffix>[ \t]*)$",
    re.MULTILINE,
)
TOOLCHAIN_DIRECTIVE_RE = re.compile(r"^toolchain\s+", re.MULTILINE)
CODEQL_VERSION_RE = re.compile(
    r"^(?P<prefix>[ \t]*go-version:[ \t]*')(?P<version>[^']+)(?P<suffix>'[ \t]*)$",
    re.MULTILINE,
)
_UNSET = object()


class UpdaterError(RuntimeError):
    """Base error for a fail-closed updater operation."""


class MetadataError(UpdaterError):
    """Official release metadata could not be trusted."""


class NetworkError(MetadataError):
    """The official release metadata endpoint could not be reached safely."""


class NoStableReleaseError(MetadataError):
    """Official metadata contains no stable release in the approved series."""


class VersionError(UpdaterError):
    """A version is outside the supported stable Go 1.26 patch series."""


class TargetError(UpdaterError):
    """A repository target is unavailable, unsafe, or inconsistent."""


class CandidateError(UpdaterError):
    """The independently resolved Go update candidate cannot be used safely."""


@dataclass(frozen=True, order=True)
class GoVersion:
    """A validated stable Go 1.26 patch version."""

    patch: int

    def __str__(self) -> str:
        return f"1.26.{self.patch}"


@dataclass(frozen=True, order=True)
class GoReleaseVersion:
    """A complete stable upstream Go release version."""

    major: int
    minor: int
    patch: int

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


@dataclass(frozen=True)
class ReleaseSelection:
    """The approved patch candidate and any separately detected newer minor."""

    approved_version: GoVersion
    newer_minor_version: GoReleaseVersion | None


@dataclass(frozen=True)
class TargetSnapshot:
    """One safely-read contract target and its identity before an update."""

    relative_path: Path
    body: str
    stat_result: os.stat_result


@dataclass
class StagedTarget:
    """A prepared replacement file held in its verified parent directory."""

    snapshot: TargetSnapshot
    parent_fd: int
    temporary_name: str | None


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Reject redirects instead of allowing urllib to follow them."""

    def redirect_request(self, request, fp, code, msg, headers, newurl):
        raise MetadataError("redirects are not allowed for Go release metadata")


def parse_stable_version(value: object) -> GoVersion:
    """Return a stable supported version or reject every other representation."""

    if type(value) is not str:
        raise VersionError("version must be a string in the exact form 1.26.N")
    match = VERSION_RE.fullmatch(value)
    if match is None:
        raise VersionError("version must be an exact stable Go 1.26.N patch value")
    return GoVersion(patch=int(match.group("patch")))


def _validate_release_endpoint(url: object) -> None:
    """Defend the fixed Go release API URL against accidental substitution."""

    if type(url) is not str or url != CANONICAL_RELEASE_API_URL:
        raise MetadataError("release metadata URL is not the canonical go.dev endpoint")
    try:
        parsed = urllib.parse.urlsplit(url)
        invalid = (
            parsed.scheme != "https"
            or parsed.hostname != "go.dev"
            or parsed.port is not None
            or parsed.username is not None
            or parsed.password is not None
            or parsed.path != "/dl/"
            or parsed.query != "mode=json&include=all"
            or bool(parsed.fragment)
        )
    except ValueError as error:
        raise MetadataError("release metadata URL is invalid") from error
    if invalid:
        raise MetadataError("release metadata URL is not an exact HTTPS go.dev endpoint")


def _response_header(response: object, name: str) -> str | None:
    headers = getattr(response, "headers", None)
    if headers is None:
        return None
    value = headers.get(name) if hasattr(headers, "get") else None
    if value is not None:
        return str(value)
    if hasattr(headers, "items"):
        for key, candidate in headers.items():
            if str(key).lower() == name.lower():
                return str(candidate)
    return None


def _response_status(response: object) -> int | None:
    status = getattr(response, "status", None)
    if status is None and hasattr(response, "getcode"):
        status = response.getcode()
    if status is None:
        return None
    if type(status) is not int:
        raise MetadataError("release metadata response has an invalid status")
    return status


def _parse_content_length(value: str | None) -> int | None:
    if value is None:
        return None
    if not re.fullmatch(r"\d+", value.strip(), re.ASCII):
        raise MetadataError("release metadata response has an invalid Content-Length")
    length = int(value)
    if length > MAX_METADATA_BYTES:
        raise MetadataError("release metadata response exceeds the size limit")
    return length


def _read_metadata_body(response: object) -> bytes:
    content_type = _response_header(response, "Content-Type")
    if content_type is None or content_type.split(";", 1)[0].strip().lower() != "application/json":
        raise MetadataError("release metadata response is not application/json")

    content_length = _parse_content_length(_response_header(response, "Content-Length"))
    if not hasattr(response, "read"):
        raise MetadataError("release metadata response cannot be read")
    body = response.read(MAX_METADATA_BYTES + 1)
    if type(body) is not bytes:
        raise MetadataError("release metadata response body is not bytes")
    if len(body) > MAX_METADATA_BYTES:
        raise MetadataError("release metadata response exceeds the size limit")
    if content_length is not None and len(body) != content_length:
        raise MetadataError("release metadata response was truncated")
    return body


def _reject_json_constant(value: str) -> object:
    raise ValueError(f"non-standard JSON constant {value!r}")


def _reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise MetadataError("release metadata JSON contains duplicate object keys")
        result[key] = value
    return result


def _decode_metadata(body: bytes) -> object:
    try:
        return json.loads(
            body.decode("utf-8"),
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_json_constant,
        )
    except MetadataError:
        raise
    except (RecursionError, UnicodeDecodeError, ValueError) as error:
        raise MetadataError("release metadata is not valid JSON") from error


def fetch_release_metadata(opener: object | None = None) -> object:
    """Fetch the fixed release API with no redirects and bounded JSON input."""

    _validate_release_endpoint(RELEASE_API_URL)
    request = urllib.request.Request(
        RELEASE_API_URL,
        headers={
            "Accept": "application/json",
            "Accept-Encoding": "identity",
            "User-Agent": "modsecurity-go-version-updater",
        },
        method="GET",
    )
    if opener is None:
        opener = urllib.request.build_opener(NoRedirectHandler())
    if not hasattr(opener, "open"):
        raise MetadataError("release metadata opener is invalid")

    response = None
    try:
        response = opener.open(request, timeout=NETWORK_TIMEOUT_SECONDS)
        status = _response_status(response)
        if status is not None and status != 200:
            raise MetadataError("release metadata response did not succeed")
        response_url = response.geturl() if hasattr(response, "geturl") else None
        if response_url != CANONICAL_RELEASE_API_URL:
            raise MetadataError("release metadata response was redirected")
        return _decode_metadata(_read_metadata_body(response))
    except MetadataError:
        raise
    except urllib.error.HTTPError as error:
        raise MetadataError("release metadata endpoint returned an unexpected HTTP response") from error
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        raise NetworkError("release metadata request failed") from error
    finally:
        if response is not None and hasattr(response, "close"):
            response.close()


def select_release_selection(metadata: object) -> ReleaseSelection:
    """Select the approved patch and report, but never select, a newer minor."""

    if type(metadata) is not list:
        raise MetadataError("release metadata must be a JSON array")

    approved_candidates: list[GoVersion] = []
    newer_minor_candidates: list[GoReleaseVersion] = []
    for index, record in enumerate(metadata):
        if type(record) is not dict:
            raise MetadataError(f"release metadata record {index} is not an object")
        version = record.get("version", _UNSET)
        stable = record.get("stable", _UNSET)
        if type(version) is not str or type(stable) is not bool:
            raise MetadataError(f"release metadata record {index} has an invalid version or stable field")
        if not stable:
            continue
        match = RELEASE_VERSION_RE.fullmatch(version)
        if match is None:
            raise MetadataError(f"release metadata record {index} has an invalid stable Go version")
        release = GoReleaseVersion(
            major=int(match.group("major")),
            minor=int(match.group("minor") or 0),
            patch=int(match.group("patch") or 0),
        )
        if (release.major, release.minor) == (1, 26):
            approved_candidates.append(GoVersion(patch=release.patch))
        elif (release.major, release.minor) > (1, 26):
            newer_minor_candidates.append(release)

    if not approved_candidates:
        raise NoStableReleaseError("release metadata contains no stable Go 1.26 patch")
    return ReleaseSelection(
        approved_version=max(approved_candidates),
        newer_minor_version=max(newer_minor_candidates, default=None),
    )


def select_latest_stable_version(metadata: object) -> GoVersion:
    """Select the highest official stable Go 1.26 patch, never another minor."""

    return select_release_selection(metadata).approved_version


def resolve_latest_stable_version(
    *,
    opener: object | None = None,
    metadata: object = _UNSET,
) -> GoVersion:
    """Resolve metadata through an injectable offline seam for focused tests."""

    if metadata is _UNSET:
        metadata = fetch_release_metadata(opener=opener)
    return select_latest_stable_version(metadata)


def resolve_release_selection(
    *,
    opener: object | None = None,
    metadata: object = _UNSET,
) -> ReleaseSelection:
    """Resolve approved and newer-minor release state through an offline seam."""

    if metadata is _UNSET:
        metadata = fetch_release_metadata(opener=opener)
    return select_release_selection(metadata)


def repository_root() -> Path:
    """Return the immutable repository root determined from this script's path."""

    return Path(__file__).resolve().parents[1]


def _checked_root(root: Path) -> Path:
    try:
        root_stat = os.lstat(root)
    except OSError as error:
        raise TargetError("repository root cannot be inspected safely") from error
    if stat.S_ISLNK(root_stat.st_mode) or not stat.S_ISDIR(root_stat.st_mode):
        raise TargetError("repository root must be a real directory, not a symlink")
    return root


def _open_parent_directory(root: Path, relative_path: Path) -> int:
    """Open a fixed target's parent with no symlink traversal."""

    if relative_path.is_absolute() or not relative_path.parts or any(
        part in {"", ".", ".."} for part in relative_path.parts
    ):
        raise TargetError("target path is not a fixed safe repository-relative path")
    _checked_root(root)
    nofollow = getattr(os, "O_NOFOLLOW", None)
    directory = getattr(os, "O_DIRECTORY", None)
    if nofollow is None or directory is None:
        raise TargetError("platform cannot safely open target directories without following symlinks")
    flags = os.O_RDONLY | nofollow | directory
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC

    descriptor: int | None = None
    try:
        descriptor = os.open(root, flags)
        for component in relative_path.parts[:-1]:
            next_descriptor = os.open(component, flags, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = next_descriptor
        return descriptor
    except OSError as error:
        if descriptor is not None:
            os.close(descriptor)
        raise TargetError(f"target parent cannot be opened safely: {relative_path}") from error


def _read_descriptor(descriptor: int) -> bytes:
    chunks: list[bytes] = []
    remaining = MAX_TARGET_BYTES + 1
    try:
        while remaining:
            chunk = os.read(descriptor, min(65536, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
    except OSError as error:
        raise TargetError("target cannot be read safely") from error
    body = b"".join(chunks)
    if len(body) > MAX_TARGET_BYTES:
        raise TargetError("target exceeds the size limit")
    return body


def _read_target(root: Path, relative_path: Path) -> TargetSnapshot:
    """Read one fixed regular target without following a symlink."""

    parent_fd = _open_parent_directory(root, relative_path)
    descriptor: int | None = None
    try:
        before_open = os.stat(relative_path.name, dir_fd=parent_fd, follow_symlinks=False)
        if not stat.S_ISREG(before_open.st_mode):
            raise TargetError(f"target must be a regular non-symlink file: {relative_path}")
        nofollow = getattr(os, "O_NOFOLLOW", None)
        if nofollow is None:
            raise TargetError("platform cannot safely open targets without following symlinks")
        flags = os.O_RDONLY | nofollow
        if hasattr(os, "O_CLOEXEC"):
            flags |= os.O_CLOEXEC
        descriptor = os.open(relative_path.name, flags, dir_fd=parent_fd)
        opened_stat = os.fstat(descriptor)
        if not stat.S_ISREG(opened_stat.st_mode) or not os.path.samestat(before_open, opened_stat):
            raise TargetError(f"target changed while being opened: {relative_path}")
        body = _read_descriptor(descriptor)
        try:
            text = body.decode("utf-8")
        except UnicodeDecodeError as error:
            raise TargetError(f"target is not UTF-8: {relative_path}") from error
        return TargetSnapshot(relative_path=relative_path, body=text, stat_result=opened_stat)
    except TargetError:
        raise
    except OSError as error:
        raise TargetError(f"target cannot be inspected safely: {relative_path}") from error
    finally:
        if descriptor is not None:
            os.close(descriptor)
        os.close(parent_fd)


def _module_version(snapshot: TargetSnapshot) -> GoVersion:
    if TOOLCHAIN_DIRECTIVE_RE.search(snapshot.body):
        raise TargetError(f"explicit toolchain directives are not allowed: {snapshot.relative_path}")
    directives = list(GO_DIRECTIVE_RE.finditer(snapshot.body))
    if len(directives) != 1:
        raise TargetError(f"target must contain exactly one Go directive: {snapshot.relative_path}")
    try:
        return parse_stable_version(directives[0].group("version"))
    except VersionError as error:
        raise TargetError(f"target has an invalid approved Go directive: {snapshot.relative_path}") from error


def _codeql_versions(snapshot: TargetSnapshot) -> list[GoVersion]:
    matches = list(CODEQL_VERSION_RE.finditer(snapshot.body))
    if len(matches) != 2:
        raise TargetError("CodeQL workflow must contain exactly two quoted go-version fields")
    try:
        return [parse_stable_version(match.group("version")) for match in matches]
    except VersionError as error:
        raise TargetError("CodeQL workflow has an invalid approved Go version") from error


def read_current_contract(root: Path) -> tuple[GoVersion, dict[Path, TargetSnapshot]]:
    """Read all fixed contract targets and require one exact consensus version."""

    selected_root = _checked_root(Path(root))
    snapshots = {relative_path: _read_target(selected_root, relative_path) for relative_path in TARGET_PATHS}
    versions = [_module_version(snapshots[path]) for path in MODULE_PATHS]
    versions.extend(_codeql_versions(snapshots[CODEQL_WORKFLOW_PATH]))
    if len(set(versions)) != 1:
        rendered = ", ".join(str(version) for version in versions)
        raise TargetError(f"Go contract targets disagree: {rendered}")
    return versions[0], snapshots


def _replace_module_version(body: str, current: GoVersion, resolved: GoVersion) -> str:
    matches = list(GO_DIRECTIVE_RE.finditer(body))
    if len(matches) != 1 or matches[0].group("version") != str(current):
        raise TargetError("module changed after contract validation")
    return GO_DIRECTIVE_RE.sub(
        lambda match: f"{match.group('prefix')}{resolved}{match.group('suffix')}", body, count=1
    )


def _replace_codeql_versions(body: str, current: GoVersion, resolved: GoVersion) -> str:
    matches = list(CODEQL_VERSION_RE.finditer(body))
    if len(matches) != 2 or any(match.group("version") != str(current) for match in matches):
        raise TargetError("CodeQL workflow changed after contract validation")
    return CODEQL_VERSION_RE.sub(
        lambda match: f"{match.group('prefix')}{resolved}{match.group('suffix')}", body
    )


def _replacement_body(snapshot: TargetSnapshot, current: GoVersion, resolved: GoVersion) -> str:
    if snapshot.relative_path in MODULE_PATHS:
        return _replace_module_version(snapshot.body, current, resolved)
    if snapshot.relative_path == CODEQL_WORKFLOW_PATH:
        return _replace_codeql_versions(snapshot.body, current, resolved)
    raise TargetError(f"unexpected update target: {snapshot.relative_path}")


def _write_all(descriptor: int, content: bytes) -> None:
    offset = 0
    while offset < len(content):
        try:
            written = os.write(descriptor, content[offset:])
        except OSError as error:
            raise TargetError("temporary replacement cannot be written") from error
        if written <= 0:
            raise TargetError("temporary replacement write made no progress")
        offset += written


def _stage_replacement(parent_fd: int, mode: int, content: str) -> str:
    """Write a private candidate under a verified parent directory descriptor."""

    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    descriptor: int | None = None
    temporary_name: str | None = None
    completed = False
    try:
        for _attempt in range(32):
            candidate = f".go-version-update-{secrets.token_hex(16)}.tmp"
            try:
                descriptor = os.open(candidate, flags, stat.S_IMODE(mode), dir_fd=parent_fd)
            except FileExistsError:
                continue
            temporary_name = candidate
            break
        if descriptor is None or temporary_name is None:
            raise TargetError("could not allocate a private replacement file")
        os.fchmod(descriptor, stat.S_IMODE(mode))
        _write_all(descriptor, content.encode("utf-8"))
        os.fsync(descriptor)
        completed = True
        return temporary_name
    except TargetError:
        raise
    except OSError as error:
        raise TargetError("temporary replacement cannot be prepared") from error
    finally:
        if descriptor is not None:
            os.close(descriptor)
        if temporary_name is not None and not completed:
            try:
                os.unlink(temporary_name, dir_fd=parent_fd)
            except OSError:
                pass


def atomic_update_contract(
    root: Path,
    snapshots: dict[Path, TargetSnapshot],
    current: GoVersion,
    resolved: GoVersion,
) -> None:
    """Stage all contract fields, then replace each fixed target with an atomic rename."""

    staged: list[StagedTarget] = []
    try:
        for relative_path in TARGET_PATHS:
            snapshot = snapshots[relative_path]
            replacement = _replacement_body(snapshot, current, resolved)
            parent_fd = _open_parent_directory(root, relative_path)
            try:
                observed = os.stat(relative_path.name, dir_fd=parent_fd, follow_symlinks=False)
                if not stat.S_ISREG(observed.st_mode) or not os.path.samestat(snapshot.stat_result, observed):
                    raise TargetError(f"target changed before update: {relative_path}")
                temporary_name = _stage_replacement(parent_fd, snapshot.stat_result.st_mode, replacement)
            except Exception:
                os.close(parent_fd)
                raise
            staged.append(StagedTarget(snapshot, parent_fd, temporary_name))

        for item in staged:
            observed = os.stat(item.snapshot.relative_path.name, dir_fd=item.parent_fd, follow_symlinks=False)
            if not stat.S_ISREG(observed.st_mode) or not os.path.samestat(item.snapshot.stat_result, observed):
                raise TargetError(f"target changed before atomic replacement: {item.snapshot.relative_path}")
        for item in staged:
            if item.temporary_name is None:
                raise TargetError("replacement state is invalid")
            os.replace(
                item.temporary_name,
                item.snapshot.relative_path.name,
                src_dir_fd=item.parent_fd,
                dst_dir_fd=item.parent_fd,
            )
            item.temporary_name = None
    except TargetError:
        raise
    except OSError as error:
        raise TargetError("Go contract targets could not be updated after staging") from error
    finally:
        for item in staged:
            if item.temporary_name is not None:
                try:
                    os.unlink(item.temporary_name, dir_fd=item.parent_fd)
                except OSError:
                    pass
            os.close(item.parent_fd)


def execute(
    mode: str,
    *,
    root: Path | None = None,
    expected_version: str | None = None,
    opener: object | None = None,
    metadata: object = _UNSET,
) -> dict[str, object]:
    """Resolve, check, or safely update the fixed Go 1.26 patch contract."""

    if mode not in {"check", "update"}:
        raise UpdaterError("mode must be check or update")
    try:
        expected = parse_stable_version(expected_version) if expected_version is not None else None
    except VersionError as error:
        raise CandidateError("expected version is not an exact stable Go 1.26 patch") from error
    selected_root = repository_root() if root is None else Path(root)
    current, snapshots = read_current_contract(selected_root)
    selection = resolve_release_selection(opener=opener, metadata=metadata)
    resolved = selection.approved_version
    if expected is not None and resolved != expected:
        raise CandidateError("resolved version does not match --expected-version")
    if resolved < current:
        raise TargetError("current Go contract is newer than the approved stable Go 1.26 patch")

    update_available = resolved > current
    if update_available:
        status = "patch_update_available"
    elif selection.newer_minor_version is not None:
        status = "newer_minor_available"
    else:
        status = "current"
    changed = False
    if mode == "update" and update_available:
        try:
            atomic_update_contract(selected_root, snapshots, current, resolved)
        except TargetError as error:
            raise CandidateError("resolved Go patch could not be applied safely") from error
        changed = True

    result: dict[str, object] = {
        "current_version": str(current),
        "latest_version": str(resolved),
        "newer_minor_available": selection.newer_minor_version is not None,
        "newer_minor_version": (
            str(selection.newer_minor_version) if selection.newer_minor_version is not None else None
        ),
        "status": status,
        "update_available": update_available,
    }
    if expected is not None:
        result["expected_version"] = str(expected)
    if mode == "update":
        result["changed"] = changed
    return result


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="report whether the pinned Go patch is current")
    mode.add_argument("--update", action="store_true", help="stage and update only the pinned Go contract fields")
    parser.add_argument(
        "--expected-version",
        metavar="1.26.N",
        help="require independently resolved metadata to equal this stable Go 1.26 patch",
    )
    parser.add_argument("--json", action="store_true", help="emit the stable JSON decision record")
    return parser


def _emit(payload: dict[str, object], output: TextIO) -> None:
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")), file=output)


def _error_status(error: UpdaterError) -> str:
    """Map a fail-closed exception to the documented machine-readable status."""

    if isinstance(error, NetworkError):
        return "blocked_network"
    if isinstance(error, NoStableReleaseError):
        return "no_stable_release"
    if isinstance(error, MetadataError):
        return "blocked_metadata"
    if isinstance(error, CandidateError):
        return "candidate_failed"
    if isinstance(error, (TargetError, VersionError)):
        return "invalid_current_version"
    return "candidate_failed"


def main(
    argv: list[str] | None = None,
    *,
    root: Path | None = None,
    opener: object | None = None,
    metadata: object = _UNSET,
    output: TextIO | None = None,
) -> int:
    """Run the CLI and return a nonzero status for every untrusted condition."""

    args = build_arg_parser().parse_args(argv)
    selected_output = sys.stdout if output is None else output
    mode = "check" if args.check else "update"
    try:
        result = execute(
            mode,
            root=root,
            expected_version=args.expected_version,
            opener=opener,
            metadata=metadata,
        )
    except UpdaterError as error:
        _emit({"error": str(error), "status": _error_status(error)}, selected_output)
        return 1
    except Exception:
        _emit({"error": "updater failed closed", "status": "candidate_failed"}, selected_output)
        return 1
    _emit(result, selected_output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
