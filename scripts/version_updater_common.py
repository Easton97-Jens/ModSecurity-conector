"""Shared hardened mechanics for repository release-version updater scripts."""

from __future__ import annotations

import argparse
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


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Reject redirects instead of allowing urllib to follow them."""

    def redirect_request(self, request, fp, code, msg, headers, newurl):
        raise MetadataError("redirects are not allowed for release metadata")


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
    return root / version_filename


def read_current_version_with_stat(
    root: Path,
    *,
    version_filename: str,
    parse_stable_version: Callable[[object], VersionT],
) -> tuple[VersionT, os.stat_result]:
    """Read a regular version file with O_NOFOLLOW and a same-file check."""

    target = version_target(root, version_filename)
    try:
        before_open = os.lstat(target)
    except OSError as error:
        raise TargetError(f"root {version_filename} cannot be inspected safely") from error
    if not stat.S_ISREG(before_open.st_mode):
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
        if not stat.S_ISREG(opened_stat.st_mode) or not os.path.samestat(before_open, opened_stat):
            raise TargetError(f"root {version_filename} changed while being opened")
        source = os.fdopen(descriptor, "rb")
        descriptor = None
        with source:
            body = source.read(MAX_VERSION_FILE_BYTES + 1)
    except TargetError:
        raise
    except OSError as error:
        raise TargetError(f"root {version_filename} cannot be read safely") from error
    finally:
        if descriptor is not None:
            os.close(descriptor)

    if len(body) > MAX_VERSION_FILE_BYTES:
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
    """Resolve, check, or safely update an adapter-owned patch version."""

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
        help="require independently resolved metadata to equal this stable patch version",
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
        return read_current_version(
            root,
            version_filename=self.version_filename,
            parse_stable_version=self.parse_stable_version,
        )

    def atomic_update_version(self, root: Path, current: object, resolved: object) -> None:
        atomic_update_version(
            root,
            current,
            resolved,
            version_filename=self.version_filename,
            version_label=self.version_label,
            parse_stable_version=self.parse_stable_version,
        )

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
