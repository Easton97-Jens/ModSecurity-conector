#!/usr/bin/env python3
"""Safely check or update the repository's Go 1.26 patch version."""

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


CANONICAL_RELEASE_API_URL = "https://go.dev/dl/?mode=json"
RELEASE_API_URL = CANONICAL_RELEASE_API_URL
VERSION_FILENAME = ".go-version"
VERSION_RE = re.compile(r"^1\.26\.(?P<patch>0|[1-9]\d*)$", re.ASCII)
RELEASE_VERSION_RE = re.compile(r"^go1\.26\.(?P<patch>0|[1-9]\d*)$", re.ASCII)
RELEASE_ENDPOINT = ReleaseEndpoint(
    canonical_url=CANONICAL_RELEASE_API_URL,
    hostname="go.dev",
    path="/dl/",
    query="mode=json",
    endpoint_name="go.dev",
    user_agent="modsecurity-go-version-updater",
)


@dataclass(frozen=True, order=True)
class GoVersion:
    """A validated stable Go 1.26 patch version."""

    patch: int

    def __str__(self) -> str:
        return f"1.26.{self.patch}"


def parse_stable_version(value: object) -> GoVersion:
    """Return a stable supported version or reject every other representation."""

    if type(value) is not str:
        raise VersionError("version must be a string in the exact form 1.26.N")
    match = VERSION_RE.fullmatch(value)
    if match is None:
        raise VersionError("version must be an exact stable 1.26.N value with nonnegative N")
    return GoVersion(patch=int(match.group("patch")))


def _validate_release_endpoint(url: object) -> None:
    """Defend the fixed API URL against accidental or test-time substitution."""

    validate_release_endpoint(url, RELEASE_ENDPOINT)


def fetch_release_metadata(opener: object | None = None) -> object:
    """Fetch the fixed release API with no redirects and bounded JSON input."""

    return _fetch_release_metadata(RELEASE_API_URL, RELEASE_ENDPOINT, opener=opener)


def select_latest_stable_version(metadata: object) -> GoVersion:
    """Select the highest stable Go 1.26 patch from official release metadata."""

    if type(metadata) is not list:
        raise MetadataError("release metadata must be a JSON array")

    candidates: list[GoVersion] = []
    for index, record in enumerate(metadata):
        if type(record) is not dict:
            raise MetadataError(f"release metadata record {index} is not an object")
        raw_version = record.get("version", _UNSET)
        stable = record.get("stable", _UNSET)
        if type(raw_version) is not str:
            raise MetadataError(f"release metadata record {index} has an invalid version")
        if type(stable) is not bool:
            raise MetadataError(f"release metadata record {index} has an invalid stable flag")
        if not stable or not raw_version.startswith("go1.26."):
            continue
        match = RELEASE_VERSION_RE.fullmatch(raw_version)
        if match is None:
            raise MetadataError(f"release metadata record {index} has an invalid stable Go 1.26 version")
        candidates.append(GoVersion(patch=int(match.group("patch"))))

    if not candidates:
        raise MetadataError("release metadata contains no stable Go 1.26 patch")
    return max(candidates)


def resolve_latest_stable_version(
    *,
    opener: object | None = None,
    metadata: object = _UNSET,
) -> GoVersion:
    """Resolve metadata through an injectable offline seam for focused tests."""

    if metadata is _UNSET:
        metadata = fetch_release_metadata(opener=opener)
    return select_latest_stable_version(metadata)


_RUNTIME = UpdaterRuntime(
    script_path=__file__,
    version_filename=VERSION_FILENAME,
    version_label="Go",
    version_metavar="1.26.N",
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
