#!/usr/bin/env python3
"""Safely check or update the repository's Python 3.13 patch version."""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import TextIO


CANONICAL_RELEASE_API_URL = "https://www.python.org/api/v2/downloads/release/?is_published=true"
RELEASE_API_URL = CANONICAL_RELEASE_API_URL
VERSION_FILENAME = ".python-version"
MAX_METADATA_BYTES = 2 * 1024 * 1024
MAX_VERSION_FILE_BYTES = 64
NETWORK_TIMEOUT_SECONDS = 15
VERSION_RE = re.compile(r"^3\.13\.(?P<patch>0|[1-9][0-9]*)$")
RELEASE_NAME_RE = re.compile(r"^Python 3\.13\.(?P<patch>0|[1-9][0-9]*)$")
_UNSET = object()


class UpdaterError(RuntimeError):
    """Base error for a fail-closed updater operation."""


class MetadataError(UpdaterError):
    """Official release metadata could not be trusted."""


class VersionError(UpdaterError):
    """A version is outside the supported stable Python 3.13 series."""


class TargetError(UpdaterError):
    """The root .python-version target is unsafe or unavailable."""


@dataclass(frozen=True, order=True)
class PythonVersion:
    """A validated stable Python 3.13 patch version."""

    patch: int

    def __str__(self) -> str:
        return f"3.13.{self.patch}"


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Reject redirects instead of allowing urllib to follow them."""

    def redirect_request(self, request, fp, code, msg, headers, newurl):
        raise MetadataError("redirects are not allowed for release metadata")


def parse_stable_version(value: object) -> PythonVersion:
    """Return a stable supported version or reject every other representation."""

    if type(value) is not str:
        raise VersionError("version must be a string in the exact form 3.13.N")
    match = VERSION_RE.fullmatch(value)
    if match is None:
        raise VersionError("version must be an exact stable 3.13.N value with nonnegative N")
    return PythonVersion(patch=int(match.group("patch")))


def _validate_release_endpoint(url: object) -> None:
    """Defend the fixed API URL against accidental or test-time substitution."""

    if type(url) is not str or url != CANONICAL_RELEASE_API_URL:
        raise MetadataError("release metadata URL is not the canonical Python.org API endpoint")
    try:
        parsed = urllib.parse.urlsplit(url)
        invalid = (
            parsed.scheme != "https"
            or parsed.hostname != "www.python.org"
            or parsed.port is not None
            or parsed.username is not None
            or parsed.password is not None
            or parsed.path != "/api/v2/downloads/release/"
            or parsed.query != "is_published=true"
            or bool(parsed.fragment)
        )
    except ValueError as error:
        raise MetadataError("release metadata URL is invalid") from error
    if invalid:
        raise MetadataError("release metadata URL is not an exact HTTPS www.python.org endpoint")


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
    if not re.fullmatch(r"[0-9]+", value.strip()):
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
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError, ValueError) as error:
        raise MetadataError("release metadata is not valid JSON") from error


def fetch_release_metadata(opener: object | None = None) -> object:
    """Fetch the fixed release API with no redirects and bounded JSON input."""

    _validate_release_endpoint(RELEASE_API_URL)
    request = urllib.request.Request(
        RELEASE_API_URL,
        headers={
            "Accept": "application/json",
            "Accept-Encoding": "identity",
            "User-Agent": "modsecurity-python-version-updater",
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
    except (OSError, TimeoutError, urllib.error.URLError, urllib.error.HTTPError) as error:
        raise MetadataError("release metadata request failed") from error
    finally:
        if response is not None and hasattr(response, "close"):
            response.close()


def _required_boolean(record: dict[str, object], field: str, index: int) -> bool:
    value = record.get(field, _UNSET)
    if type(value) is not bool:
        raise MetadataError(f"release metadata record {index} has an invalid {field}")
    return value


def select_latest_stable_version(metadata: object) -> PythonVersion:
    """Select the highest published, non-prerelease stable 3.13 patch."""

    if type(metadata) is not list:
        raise MetadataError("release metadata must be a JSON array")

    candidates: list[PythonVersion] = []
    for index, record in enumerate(metadata):
        if type(record) is not dict:
            raise MetadataError(f"release metadata record {index} is not an object")
        name = record.get("name", _UNSET)
        if type(name) is not str:
            raise MetadataError(f"release metadata record {index} has an invalid name")
        if not _required_boolean(record, "is_published", index):
            raise MetadataError("release metadata contained an unpublished release")
        pre_release = _required_boolean(record, "pre_release", index)
        if not name.startswith("Python 3.13.") or pre_release:
            continue

        match = RELEASE_NAME_RE.fullmatch(name)
        if match is None:
            raise MetadataError(f"release metadata record {index} has an invalid stable 3.13 name")
        patch = int(match.group("patch"))
        candidates.append(PythonVersion(patch=patch))

    if not candidates:
        raise MetadataError("release metadata contains no published stable Python 3.13 patch")
    return max(candidates)


def resolve_latest_stable_version(
    *,
    opener: object | None = None,
    metadata: object = _UNSET,
) -> PythonVersion:
    """Resolve metadata through an injectable offline seam for focused tests."""

    if metadata is _UNSET:
        metadata = fetch_release_metadata(opener=opener)
    return select_latest_stable_version(metadata)


def repository_root() -> Path:
    """Return the immutable repository root determined from this script's path."""

    return Path(__file__).resolve().parents[1]


def _version_target(root: Path) -> Path:
    try:
        root_stat = os.lstat(root)
    except OSError as error:
        raise TargetError("repository root cannot be inspected safely") from error
    if stat.S_ISLNK(root_stat.st_mode) or not stat.S_ISDIR(root_stat.st_mode):
        raise TargetError("repository root must be a real directory, not a symlink")
    return root / VERSION_FILENAME


def _read_current_version_with_stat(root: Path) -> tuple[PythonVersion, os.stat_result]:
    target = _version_target(root)
    try:
        before_open = os.lstat(target)
    except OSError as error:
        raise TargetError("root .python-version cannot be inspected safely") from error
    if not stat.S_ISREG(before_open.st_mode):
        raise TargetError("root .python-version must be a regular non-symlink file")

    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise TargetError("platform cannot safely open .python-version without following symlinks")
    flags = os.O_RDONLY | nofollow
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    descriptor: int | None = None
    try:
        descriptor = os.open(target, flags)
        opened_stat = os.fstat(descriptor)
        if not stat.S_ISREG(opened_stat.st_mode) or not os.path.samestat(before_open, opened_stat):
            raise TargetError("root .python-version changed while being opened")
        source = os.fdopen(descriptor, "rb")
        descriptor = None
        with source:
            body = source.read(MAX_VERSION_FILE_BYTES + 1)
    except TargetError:
        raise
    except OSError as error:
        raise TargetError("root .python-version cannot be read safely") from error
    finally:
        if descriptor is not None:
            os.close(descriptor)

    if len(body) > MAX_VERSION_FILE_BYTES:
        raise VersionError("root .python-version is unexpectedly large")
    try:
        text = body.decode("utf-8")
    except UnicodeDecodeError as error:
        raise VersionError("root .python-version is not UTF-8") from error
    if text.endswith("\n"):
        text = text[:-1]
    return parse_stable_version(text), opened_stat


def read_current_version(root: Path) -> PythonVersion:
    """Read and strictly validate the regular root .python-version file."""

    current, _target_stat = _read_current_version_with_stat(root)
    return current


def atomic_update_version(root: Path, current: PythonVersion, resolved: PythonVersion) -> None:
    """Atomically replace the regular root file only with a strictly newer patch."""

    if resolved <= current:
        raise VersionError("refusing a non-monotonic Python version update")
    target = _version_target(root)
    observed_current, original_stat = _read_current_version_with_stat(root)
    if observed_current != current:
        raise TargetError("root .python-version changed before update")

    descriptor: int | None = None
    temporary_path: str | None = None
    try:
        descriptor, temporary_path = tempfile.mkstemp(prefix=".python-version.", suffix=".tmp", dir=root)
        os.fchmod(descriptor, stat.S_IMODE(original_stat.st_mode))
        destination = os.fdopen(descriptor, "wb")
        descriptor = None
        with destination:
            destination.write(f"{resolved}\n".encode("utf-8"))
            destination.flush()
            os.fsync(destination.fileno())

        replacement_stat = os.lstat(target)
        if not stat.S_ISREG(replacement_stat.st_mode) or not os.path.samestat(original_stat, replacement_stat):
            raise TargetError("root .python-version changed before atomic replacement")
        os.replace(temporary_path, target)
        temporary_path = None
    except TargetError:
        raise
    except OSError as error:
        raise TargetError("root .python-version could not be updated atomically") from error
    finally:
        if descriptor is not None:
            os.close(descriptor)
        if temporary_path is not None:
            try:
                os.unlink(temporary_path)
            except OSError:
                pass


def execute(
    mode: str,
    *,
    root: Path | None = None,
    expected_version: str | None = None,
    opener: object | None = None,
    metadata: object = _UNSET,
) -> dict[str, object]:
    """Resolve, check, or safely update the root Python patch version."""

    if mode not in {"check", "update"}:
        raise UpdaterError("mode must be check or update")
    expected = parse_stable_version(expected_version) if expected_version is not None else None
    selected_root = repository_root() if root is None else Path(root)
    current = read_current_version(selected_root)
    resolved = resolve_latest_stable_version(opener=opener, metadata=metadata)

    if expected is not None and resolved != expected:
        raise VersionError("resolved version does not match --expected-version")
    if resolved < current:
        raise VersionError("refusing a resolved Python version older than the current version")

    update_available = resolved > current
    status = "update_available" if update_available else "current"
    changed = False
    if mode == "update" and update_available:
        atomic_update_version(selected_root, current, resolved)
        changed = True

    result = {
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


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="report whether the root version is current")
    mode.add_argument("--update", action="store_true", help="atomically update the root version when newer")
    parser.add_argument(
        "--expected-version",
        metavar="3.13.N",
        help="require independently resolved metadata to equal this stable patch version",
    )
    parser.add_argument("--json", action="store_true", help="emit the stable JSON decision record")
    return parser


def _emit(payload: dict[str, object], output: TextIO) -> None:
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")), file=output)


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
        _emit({"error": str(error), "status": "error"}, selected_output)
        return 1
    except Exception:
        _emit({"error": "updater failed closed", "status": "error"}, selected_output)
        return 1
    _emit(result, selected_output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
