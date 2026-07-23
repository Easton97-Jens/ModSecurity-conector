#!/usr/bin/env python3
"""Safely check or update the repository's Python 3.14 patch version."""

from __future__ import annotations

import re
from dataclasses import dataclass

from version_updater_common import (
    MetadataError,
    ReleaseEndpoint,
    UpdaterRuntime,
    VersionError,
    _UNSET,
    _decode_metadata,
    _parse_content_length,
    fetch_release_metadata as _fetch_release_metadata,
    validate_release_endpoint,
)


CANONICAL_RELEASE_API_URL = "https://www.python.org/api/v2/downloads/release/?is_published=true"
RELEASE_API_URL = CANONICAL_RELEASE_API_URL
VERSION_FILENAME = ".python-version"
VERSION_RE = re.compile(r"^3\.14\.(?P<patch>0|[1-9]\d*)$", re.ASCII)
RELEASE_NAME_RE = re.compile(r"^Python 3\.14\.(?P<patch>0|[1-9]\d*)$", re.ASCII)
RELEASE_ENDPOINT = ReleaseEndpoint(
    canonical_url=CANONICAL_RELEASE_API_URL,
    hostname="www.python.org",
    path="/api/v2/downloads/release/",
    query="is_published=true",
    endpoint_name="Python.org",
    user_agent="modsecurity-python-version-updater",
)


@dataclass(frozen=True, order=True)
class PythonVersion:
    """A validated stable Python 3.14 patch version."""

    patch: int

    def __str__(self) -> str:
        return f"3.14.{self.patch}"


def parse_stable_version(value: object) -> PythonVersion:
    """Return a stable supported version or reject every other representation."""

    if type(value) is not str:
        raise VersionError("version must be a string in the exact form 3.14.N")
    match = VERSION_RE.fullmatch(value)
    if match is None:
        raise VersionError("version must be an exact stable 3.14.N value with nonnegative N")
    return PythonVersion(patch=int(match.group("patch")))


def _validate_release_endpoint(url: object) -> None:
    """Defend the fixed API URL against accidental or test-time substitution."""

    validate_release_endpoint(url, RELEASE_ENDPOINT)


def fetch_release_metadata(opener: object | None = None) -> object:
    """Fetch the fixed release API with no redirects and bounded JSON input."""

    return _fetch_release_metadata(RELEASE_API_URL, RELEASE_ENDPOINT, opener=opener)


def _required_boolean(record: dict[str, object], field: str, index: int) -> bool:
    value = record.get(field, _UNSET)
    if type(value) is not bool:
        raise MetadataError(f"release metadata record {index} has an invalid {field}")
    return value


def select_latest_stable_version(metadata: object) -> PythonVersion:
    """Select the highest published, non-prerelease stable 3.14 patch."""

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
        if not name.startswith("Python 3.14.") or pre_release:
            continue

        match = RELEASE_NAME_RE.fullmatch(name)
        if match is None:
            raise MetadataError(f"release metadata record {index} has an invalid stable 3.14 name")
        candidates.append(PythonVersion(patch=int(match.group("patch"))))

    if not candidates:
        raise MetadataError("release metadata contains no published stable Python 3.14 patch")
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


_RUNTIME = UpdaterRuntime(
    script_path=__file__,
    version_filename=VERSION_FILENAME,
    version_label="Python",
    version_metavar="3.14.N",
    description=__doc__,
    parse_stable_version=parse_stable_version,
    resolve_latest_stable_version=resolve_latest_stable_version,
)
repository_root = _RUNTIME.repository_root
_version_target = _RUNTIME.version_target
_read_current_version_with_stat = _RUNTIME.read_current_version_with_stat
read_current_version = _RUNTIME.read_current_version
atomic_update_version = _RUNTIME.atomic_update_version
execute = _RUNTIME.execute
build_arg_parser = _RUNTIME.build_arg_parser
main = _RUNTIME.main


if __name__ == "__main__":
    raise SystemExit(main())
