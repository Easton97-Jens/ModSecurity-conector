"""Shared hardened mechanics for repository release-version updater scripts."""

from __future__ import annotations

import argparse
import fcntl
import json
import os
import re
import stat
import sys
import tempfile
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, TextIO, TypeVar


MAX_METADATA_BYTES = 2 * 1024 * 1024
MAX_VERSION_FILE_BYTES = 64
NETWORK_TIMEOUT_SECONDS = 15
_UNSET = object()

VersionT = TypeVar("VersionT")


class UpdaterError(RuntimeError):
    """Base error for a fail-closed updater operation."""


class MetadataError(UpdaterError):
    """Official release metadata could not be trusted."""


class VersionError(UpdaterError):
    """A version is outside the adapter's supported stable series."""


class TargetError(UpdaterError):
    """The repository version-file target is unsafe or unavailable."""


@dataclass(frozen=True)
class ReleaseEndpoint:
    """The exact trusted metadata endpoint selected by one language adapter."""

    canonical_url: str
    hostname: str
    path: str
    query: str
    endpoint_name: str
    user_agent: str


@dataclass(frozen=True)
class ReleaseMetadataSource:
    """Bind an adapter's mutable URL seam to the shared hardened transport."""

    endpoint: ReleaseEndpoint
    url_provider: Callable[[], object]

    def validate(self, url: object) -> None:
        """Validate a candidate URL against this source's exact endpoint."""

        validate_release_endpoint(url, self.endpoint)

    def fetch(self, opener: object | None = None) -> object:
        """Fetch from the adapter's current URL through the hardened transport."""

        return fetch_release_metadata(
            self.url_provider(),
            self.endpoint,
            opener=opener,
        )


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Reject redirects without forwarding headers to another origin."""

    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None


def validate_release_endpoint(url: object, endpoint: ReleaseEndpoint) -> None:
    """Require the exact trusted endpoint before any network request is opened."""

    if type(url) is not str or url != endpoint.canonical_url:
        raise MetadataError(
            f"release metadata URL is not the canonical {endpoint.endpoint_name} API endpoint"
        )
    try:
        parsed = urllib.parse.urlsplit(url)
        invalid = (
            parsed.scheme != "https"
            or parsed.hostname != endpoint.hostname
            or parsed.port is not None
            or parsed.username is not None
            or parsed.password is not None
            or parsed.path != endpoint.path
            or parsed.query != endpoint.query
            or bool(parsed.fragment)
        )
    except ValueError as error:
        raise MetadataError("release metadata URL is invalid") from error
    if invalid:
        raise MetadataError(
            f"release metadata URL is not an exact HTTPS {endpoint.hostname} endpoint"
        )


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
    except (RecursionError, ValueError) as error:
        raise MetadataError("release metadata is not valid JSON") from error


def fetch_release_metadata(
    release_url: object,
    endpoint: ReleaseEndpoint,
    *,
    opener: object | None = None,
) -> object:
    """Fetch bounded, strict JSON from one exact release endpoint without redirects."""

    validate_release_endpoint(release_url, endpoint)
    request = urllib.request.Request(
        endpoint.canonical_url,
        headers={
            "Accept": "application/json",
            "Accept-Encoding": "identity",
            "User-Agent": endpoint.user_agent,
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
        if response_url != endpoint.canonical_url:
            raise MetadataError("release metadata response was redirected")
        return _decode_metadata(_read_metadata_body(response))
    except MetadataError:
        raise
    except OSError as error:
        raise MetadataError("release metadata request failed") from error
    finally:
        if response is not None and hasattr(response, "close"):
            response.close()


def repository_root(script_path: str | Path) -> Path:
    """Return the immutable repository root determined from an adapter's path."""

    return Path(script_path).resolve().parents[1]


def version_target(root: Path, version_filename: str) -> Path:
    """Validate a real repository root and derive its version-file target."""

    try:
        root_stat = os.lstat(root)
    except OSError as error:
        raise TargetError("repository root cannot be inspected safely") from error
    if stat.S_ISLNK(root_stat.st_mode) or not stat.S_ISDIR(root_stat.st_mode):
        raise TargetError("repository root must be a real directory, not a symlink")
    target = root / version_filename
    for parent in target.parents:
        if parent == root:
            break
        if parent.is_symlink() or not parent.is_dir():
            raise TargetError("version target directory must be a real directory")
    return target


def read_current_version_with_stat(
    root: Path,
    *,
    version_filename: str,
    parse_stable_version: Callable[[object], VersionT],
    max_bytes: int = MAX_VERSION_FILE_BYTES,
) -> tuple[VersionT, os.stat_result]:
    """Read a regular version file with O_NOFOLLOW and a same-file check."""

    target = version_target(root, version_filename)
    try:
        before_open = os.lstat(target)
    except OSError as error:
        raise TargetError(f"root {version_filename} cannot be inspected safely") from error
    if not stat.S_ISREG(before_open.st_mode) or before_open.st_nlink != 1:
        raise TargetError(f"root {version_filename} must be a regular non-symlink file")

    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise TargetError(
            f"platform cannot safely open {version_filename} without following symlinks"
        )
    flags = os.O_RDONLY | nofollow
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    descriptor: int | None = None
    try:
        descriptor = os.open(target, flags)
        opened_stat = os.fstat(descriptor)
        if not stat.S_ISREG(opened_stat.st_mode) or opened_stat.st_nlink != 1 or not os.path.samestat(before_open, opened_stat):
            raise TargetError(f"root {version_filename} changed while being opened")
        source = os.fdopen(descriptor, "rb")
        descriptor = None
        with source:
            body = source.read(max_bytes + 1)
    except TargetError:
        raise
    except OSError as error:
        raise TargetError(f"root {version_filename} cannot be read safely") from error
    finally:
        if descriptor is not None:
            os.close(descriptor)

    if len(body) > max_bytes:
        raise VersionError(f"root {version_filename} is unexpectedly large")
    try:
        text = body.decode("utf-8")
    except UnicodeDecodeError as error:
        raise VersionError(f"root {version_filename} is not UTF-8") from error
    if text.endswith("\n"):
        text = text[:-1]
    return parse_stable_version(text), opened_stat


def read_current_version(
    root: Path,
    *,
    version_filename: str,
    parse_stable_version: Callable[[object], VersionT],
) -> VersionT:
    """Read and strictly validate a regular root version file."""

    current, _target_stat = read_current_version_with_stat(
        root,
        version_filename=version_filename,
        parse_stable_version=parse_stable_version,
    )
    return current


def atomic_update_version(
    root: Path,
    current: VersionT,
    resolved: VersionT,
    *,
    version_filename: str,
    version_label: str,
    parse_stable_version: Callable[[object], VersionT],
) -> None:
    """Fsync and atomically replace one unchanged regular version file."""

    if resolved <= current:  # type: ignore[operator]
        raise VersionError(f"refusing a non-monotonic {version_label} version update")
    target = version_target(root, version_filename)
    observed_current, original_stat = read_current_version_with_stat(
        root,
        version_filename=version_filename,
        parse_stable_version=parse_stable_version,
    )
    if observed_current != current:
        raise TargetError(f"root {version_filename} changed before update")

    descriptor: int | None = None
    temporary_path: str | None = None
    try:
        descriptor, temporary_path = tempfile.mkstemp(
            prefix=f"{version_filename}.", suffix=".tmp", dir=root
        )
        os.fchmod(descriptor, stat.S_IMODE(original_stat.st_mode))
        destination = os.fdopen(descriptor, "wb")
        descriptor = None
        with destination:
            destination.write(f"{resolved}\n".encode("utf-8"))
            destination.flush()
            os.fsync(destination.fileno())

        replacement_stat = os.lstat(target)
        if not stat.S_ISREG(replacement_stat.st_mode) or not os.path.samestat(
            original_stat, replacement_stat
        ):
            raise TargetError(f"root {version_filename} changed before atomic replacement")
        os.replace(temporary_path, target)
        temporary_path = None
    except TargetError:
        raise
    except OSError as error:
        raise TargetError(f"root {version_filename} could not be updated atomically") from error
    finally:
        if descriptor is not None:
            os.close(descriptor)
        if temporary_path is not None:
            try:
                os.unlink(temporary_path)
            except OSError:
                pass


PROJECT_VERSION_LOCK = "ci/tooling/project-versions.lock.json"
TOOLCHAIN_FIELDS = {".python-version": "python_version", ".go-version": "go_version"}


def _parse_project_lock(text: object) -> dict[str, int | str]:
    # Import only the fixed checked-in parser; lock data is never executable.
    library = Path(__file__).resolve().parents[1] / "ci" / "lib"
    sys.path.insert(0, str(library))
    try:
        from framework_revision_pins import FrameworkRevisionPinsError, parse_project_version_pins
    finally:
        sys.path.pop(0)
    try:
        return parse_project_version_pins(str(text).encode("utf-8"))
    except FrameworkRevisionPinsError as error:
        raise VersionError(str(error)) from error


def project_lock_snapshot(root: Path) -> tuple[dict[str, int | str], os.stat_result]:
    return read_current_version_with_stat(
        root, version_filename=PROJECT_VERSION_LOCK,
        parse_stable_version=_parse_project_lock, max_bytes=4096,
    )


def project_toolchain_version(root: Path, filename: str, parser: Callable) -> object:
    pins, _ = project_lock_snapshot(root)
    selected = parser(pins[TOOLCHAIN_FIELDS[filename]])
    view = read_current_version(root, version_filename=filename, parse_stable_version=parser)
    if selected != view:
        raise TargetError(f"generated {filename} disagrees with {PROJECT_VERSION_LOCK}; synchronize project versions")
    return selected


def _same_snapshot(actual: os.stat_result, expected: os.stat_result) -> bool:
    return os.path.samestat(actual, expected) and (
        actual.st_mtime_ns, actual.st_ctime_ns, actual.st_size, actual.st_mode, actual.st_nlink
    ) == (expected.st_mtime_ns, expected.st_ctime_ns, expected.st_size, expected.st_mode, expected.st_nlink)


def _unchanged(
    root: Path, filename: str, expected_stat: os.stat_result,
    expected: object, parser: Callable, limit: int,
) -> None:
    actual, metadata = read_current_version_with_stat(
        root, version_filename=filename, parse_stable_version=parser, max_bytes=limit,
    )
    if not _same_snapshot(metadata, expected_stat) or actual != expected:
        raise TargetError(f"{filename} changed before replacement")


def _write_temporary(target: Path, body: bytes, metadata: os.stat_result) -> str:
    descriptor, temporary = tempfile.mkstemp(prefix=".project-version-", dir=target.parent)
    try:
        with os.fdopen(descriptor, "wb") as destination:
            os.fchmod(destination.fileno(), stat.S_IMODE(metadata.st_mode))
            destination.write(body)
            destination.flush()
            os.fsync(destination.fileno())
    except OSError:
        os.unlink(temporary)
        raise
    return temporary



def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)

def _replacement_unchanged(
    root: Path, filename: str, expected: os.stat_result, expected_body: bytes,
) -> bool:
    try:
        text, metadata = read_current_version_with_stat(
            root, version_filename=filename,
            parse_stable_version=lambda value: value, max_bytes=4096,
        )
    except UpdaterError:
        return False
    body = text.encode("utf-8")
    if metadata.st_size == len(body) + 1:
        body += b"\n"
    return _same_snapshot(metadata, expected) and body == expected_body


def _restore_replaced_files(
    root: Path, replaced: list[tuple[str, bytes, bytes, os.stat_result]],
    prepared: list[tuple[str, str]],
) -> None:
    for filename, old_body, written_body, replacement in reversed(replaced):
        target = version_target(root, filename)
        if not _replacement_unchanged(root, filename, replacement, written_body):
            continue
        temporary = _write_temporary(target, old_body, replacement)
        prepared.append((filename, temporary))
        if _replacement_unchanged(root, filename, replacement, written_body):
            os.replace(temporary, target)
            _fsync_directory(target.parent)


def replace_project_files(
    root: Path, updates: list[tuple[str, bytes, object, os.stat_result, Callable, int]],
) -> None:
    """Prepare changes before replacing views, then commit the lock last.

    Roll back completed replacements if an operational error occurs. A process
    crash can leave detectable view drift; multi-file filesystem atomicity is
    not assumed. Concurrent external replacements are preserved during rollback.
    """
    prepared: list[tuple[str, str]] = []
    replaced: list[tuple[str, bytes, bytes, os.stat_result]] = []
    try:
        for filename, body, _, metadata, _, _ in updates:
            temporary = _write_temporary(version_target(root, filename), body, metadata)
            prepared.append((filename, temporary))
        for filename, _, original, metadata, parser, limit in updates:
            _unchanged(root, filename, metadata, original, parser, limit)
        for update, (_, temporary) in zip(updates, prepared):
            filename, written_body, original, metadata, parser, limit = update
            target = version_target(root, filename)
            old_text, old_stat = read_current_version_with_stat(
                root, version_filename=filename,
                parse_stable_version=lambda value: value, max_bytes=limit,
            )
            old_body = old_text.encode("utf-8")
            if old_stat.st_size == len(old_body) + 1:
                old_body += b"\n"
            _unchanged(root, filename, metadata, original, parser, limit)
            os.replace(temporary, target)
            replaced.append((filename, old_body, written_body, os.lstat(target)))
            _fsync_directory(target.parent)
    except (OSError, UpdaterError) as error:
        _restore_replaced_files(root, replaced, prepared)
        raise TargetError("project versions could not be updated safely") from error
    finally:
        for _, temporary in prepared:
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass


def update_project_toolchain(root: Path, current: object, resolved: object, *, filename: str, parser: Callable, label: str) -> None:
    if resolved <= current:
        raise VersionError(f"refusing a non-monotonic {label} version update")
    directory = version_target(root, PROJECT_VERSION_LOCK).parent
    descriptor = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        pins, lock_stat = project_lock_snapshot(root)
        if parser(pins[TOOLCHAIN_FIELDS[filename]]) != current:
            raise TargetError("central toolchain version changed before update")
        view, view_stat = read_current_version_with_stat(root, version_filename=filename, parse_stable_version=parser)
        if view != current:
            raise TargetError("generated toolchain version changed before update")
        candidate = dict(pins)
        candidate[TOOLCHAIN_FIELDS[filename]] = str(resolved)
        body = (json.dumps(candidate, indent=2) + "\n").encode("utf-8")
        _parse_project_lock(body.decode("utf-8"))
        replace_project_files(root, [
            (filename, f"{resolved}\n".encode(), view, view_stat, parser, 64),
            (PROJECT_VERSION_LOCK, body, pins, lock_stat, _parse_project_lock, 4096),
        ])
    finally:
        os.close(descriptor)


def execute_update(
    mode: str,
    *,
    root: Path | None,
    expected_version: str | None,
    opener: object | None,
    metadata: object,
    repository_root: Callable[[], Path],
    parse_stable_version: Callable[[object], VersionT],
    read_current_version: Callable[[Path], VersionT],
    resolve_latest_stable_version: Callable[..., VersionT],
    atomic_update_version: Callable[[Path, VersionT, VersionT], None],
    version_label: str,
) -> dict[str, object]:
    """Resolve, check, or safely update an adapter-owned version."""

    if mode not in {"check", "update"}:
        raise UpdaterError("mode must be check or update")
    expected = parse_stable_version(expected_version) if expected_version is not None else None
    selected_root = repository_root() if root is None else Path(root)
    current = read_current_version(selected_root)
    resolved = resolve_latest_stable_version(opener=opener, metadata=metadata)

    if expected is not None and resolved != expected:
        raise VersionError("resolved version does not match --expected-version")
    if resolved < current:  # type: ignore[operator]
        raise VersionError(f"refusing a resolved {version_label} version older than the current version")

    update_available = resolved > current  # type: ignore[operator]
    status = "update_available" if update_available else "current"
    changed = False
    if mode == "update" and update_available:
        atomic_update_version(selected_root, current, resolved)
        changed = True

    result: dict[str, object] = {
        "current_version": str(current),
        "latest_version": str(resolved),
        "status": status,
        "update_available": update_available,
    }
    if expected is not None:
        result["expected_version"] = str(expected)
    if mode == "update":
        result["changed"] = changed
    return result


def build_arg_parser(description: str | None, version_metavar: str) -> argparse.ArgumentParser:
    """Build the shared fail-closed CLI shape with an adapter-specific version form."""

    parser = argparse.ArgumentParser(description=description)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="report whether the root version is current")
    mode.add_argument("--update", action="store_true", help="atomically update the root version when newer")
    parser.add_argument(
        "--expected-version",
        metavar=version_metavar,
        help="require independently resolved metadata to equal this stable version",
    )
    parser.add_argument("--json", action="store_true", help="emit the stable JSON decision record")
    return parser


def emit(payload: dict[str, object], output: TextIO) -> None:
    """Emit the stable, payload-safe JSON record used by both updater CLIs."""

    print(json.dumps(payload, sort_keys=True, separators=(",", ":")), file=output)


def run_cli(
    argv: list[str] | None,
    *,
    root: Path | None,
    opener: object | None,
    metadata: object,
    output: TextIO | None,
    build_arg_parser: Callable[[], argparse.ArgumentParser],
    execute: Callable[..., dict[str, object]],
) -> int:
    """Run an adapter CLI and fail closed for expected and unexpected errors."""

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
        emit({"error": str(error), "status": "error"}, selected_output)
        return 1
    except Exception:
        emit({"error": "updater failed closed", "status": "error"}, selected_output)
        return 1
    emit(result, selected_output)
    return 0


@dataclass(frozen=True)
class UpdaterRuntime:
    """Bind one language adapter's version policy to the shared updater mechanics."""

    script_path: str
    version_filename: str
    version_label: str
    version_metavar: str
    description: str | None
    parse_stable_version: Callable[[object], object]
    resolve_latest_stable_version: Callable[..., object]

    def repository_root(self) -> Path:
        return repository_root(self.script_path)

    def version_target(self, root: Path) -> Path:
        return version_target(root, self.version_filename)

    def read_current_version_with_stat(self, root: Path) -> tuple[object, os.stat_result]:
        return read_current_version_with_stat(
            root,
            version_filename=self.version_filename,
            parse_stable_version=self.parse_stable_version,
        )

    def read_current_version(self, root: Path) -> object:
        return project_toolchain_version(root, self.version_filename, self.parse_stable_version)

    def atomic_update_version(self, root: Path, current: object, resolved: object) -> None:
        update_project_toolchain(root, current, resolved, filename=self.version_filename,
                                 parser=self.parse_stable_version, label=self.version_label)

    def execute(
        self,
        mode: str,
        *,
        root: Path | None = None,
        expected_version: str | None = None,
        opener: object | None = None,
        metadata: object = _UNSET,
    ) -> dict[str, object]:
        return execute_update(
            mode,
            root=root,
            expected_version=expected_version,
            opener=opener,
            metadata=metadata,
            repository_root=self.repository_root,
            parse_stable_version=self.parse_stable_version,
            read_current_version=self.read_current_version,
            resolve_latest_stable_version=self.resolve_latest_stable_version,
            atomic_update_version=self.atomic_update_version,
            version_label=self.version_label,
        )

    def build_arg_parser(self) -> argparse.ArgumentParser:
        return build_arg_parser(self.description, self.version_metavar)

    def main(
        self,
        argv: list[str] | None = None,
        *,
        root: Path | None = None,
        opener: object | None = None,
        metadata: object = _UNSET,
        output: TextIO | None = None,
    ) -> int:
        return run_cli(
            argv,
            root=root,
            opener=opener,
            metadata=metadata,
            output=output,
            build_arg_parser=self.build_arg_parser,
            execute=self.execute,
        )
