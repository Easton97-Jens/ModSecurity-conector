#!/usr/bin/env python3
"""Fail closed when a Framework candidate disagrees with Parent contracts.

This tool reads an extracted Framework ``common.sh`` strictly as data.  It is
intentionally separate from the generic component synchronizer: it never
updates a Parent file and NGINX remains outside that synchronizer's registry.
The protected NGINX root-broker chain is an immutable, separately reviewed
provenance boundary and is deliberately not inspected here.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import stat


MAX_INPUT_BYTES = 512 * 1024
# Any Framework common.sh structure change needs a separate Parent review before
# the candidate updater can publish it, because this file is later sourced. The
# digest is over the structural skeleton below, not the raw source: only the
# bounded generic source-data RHSs may vary without a structural review.
APPROVED_FRAMEWORK_COMMON_STRUCTURE_SHA256 = "609315092e5f5cdd793a33636f7d620445f2e4e802a383c23bc26a70d1bc7c75"
# Keep this closed list identical to sync-framework-component-versions.py's
# SOURCE_REGISTRY. It is deliberately separate from NGINX, whose handoff stays
# manually reviewed and byte-covered by the structure digest.
MUTABLE_SOURCE_FIELDS = (
    "ENVOY_VERSION",
    "LIGHTTPD_SERIES",
    "LIGHTTPD_RELEASE_ROOT_URL",
    "LIGHTTPD_SERIES_BASE_URL",
    "LIGHTTPD_VERSION",
    "LIGHTTPD_SOURCE_URL",
    "LIGHTTPD_ARCHIVE_NAME",
    "LIGHTTPD_DOWNLOAD_URL",
    "LIGHTTPD_SHA256",
    "HAPROXY_SERIES",
    "HAPROXY_RELEASE_ROOT_URL",
    "HAPROXY_SERIES_BASE_URL",
    "HAPROXY_VERSION",
    "HAPROXY_ARCHIVE_NAME",
    "HAPROXY_SOURCE_URL",
    "HAPROXY_SHA256",
    "HAPROXY_HTX_SERIES",
    "HAPROXY_HTX_SERIES_BASE_URL",
    "HAPROXY_HTX_VERSION",
    "HAPROXY_HTX_ARCHIVE_NAME",
    "HAPROXY_HTX_SOURCE_URL",
    "HAPROXY_HTX_SHA256",
    "CRS_APPROVED_REPO_URL",
    "CRS_APPROVED_COMMIT",
    "CRS_RELEASE_TAG",
)
MUTABLE_SOURCE_FIELD_SET = frozenset(MUTABLE_SOURCE_FIELDS)
HEX40 = re.compile(r"^[0-9a-f]{40}$", re.ASCII)
HEX64 = re.compile(r"^[0-9a-f]{64}$", re.ASCII)
NGINX_TAG = re.compile(
    r"^release-(?P<version>[1-9]\d*\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*))$",
    re.ASCII,
)


class ContractError(ValueError):
    """Raised when candidate data or a fixed Parent projection is unsafe."""


@dataclass(frozen=True)
class ParentProjection:
    """One read-only unprotected Parent NGINX handoff field."""

    relative_path: str
    syntax: str
    name: str
    value_name: str


@dataclass(frozen=True)
class ParentPolicyProjection:
    """One fixed Parent policy value that a candidate must not override."""

    relative_path: str
    syntax: str
    name: str
    expected_value: str


NGINX_FIELDS = (
    "NGINX_SOURCE_MODE",
    "NGINX_SOURCE_REPO_URL",
    "NGINX_RELEASE_TAG",
    "NGINX_SOURCE_GIT_REF",
    "NGINX_RELEASE_ASSET_NAME",
    "NGINX_SHA256",
)

PARENT_OWNED_NGINX_FIELDS = ("NGINX_REQUIRE_PINNED_PROVENANCE",)

NGINX_EXACT_HEAD_WORKFLOW_PATH = ".github/workflows/test-nginx-exact-head.yml"
NGINX_FULL_SMOKE_WORKFLOW_PATH = ".github/workflows/test-full-smoke-sequential.yml"
RUNTIME_COMPONENTS_PATH = "ci/provisioning/components/prepare-runtime-components.py"
RUNTIME_PRODUCER_READINESS_PATH = "ci/checks/evidence/check-runtime-producer-readiness.py"
LITERAL_FRAMEWORK_SHA = re.compile(
    r"(?m)^[ \t]*FRAMEWORK_SHA:[ \t]*(?P<value>(?P<quote>[\"']?)[0-9a-f]{40}(?P=quote))[ \t]*(?:#.*)?$"
)
DYNAMIC_SHELL_EVALUATION = re.compile(r"\beval\b", re.ASCII)

PARENT_NGINX_PROJECTIONS = (
    ParentProjection(
        NGINX_EXACT_HEAD_WORKFLOW_PATH,
        "yaml",
        "NGINX_SOURCE_MODE",
        "source_mode",
    ),
    ParentProjection(
        NGINX_EXACT_HEAD_WORKFLOW_PATH,
        "yaml",
        "NGINX_SOURCE_REPO_URL",
        "source_repository",
    ),
    ParentProjection(
        NGINX_EXACT_HEAD_WORKFLOW_PATH,
        "yaml",
        "NGINX_RELEASE_TAG",
        "release_tag",
    ),
    ParentProjection(
        NGINX_EXACT_HEAD_WORKFLOW_PATH,
        "yaml",
        "NGINX_SOURCE_GIT_REF",
        "source_ref",
    ),
    ParentProjection(
        NGINX_EXACT_HEAD_WORKFLOW_PATH,
        "yaml",
        "NGINX_RELEASE_ASSET_NAME",
        "release_asset_name",
    ),
    ParentProjection(
        NGINX_EXACT_HEAD_WORKFLOW_PATH,
        "yaml",
        "NGINX_SHA256",
        "archive_sha256",
    ),
    ParentProjection(
        NGINX_FULL_SMOKE_WORKFLOW_PATH,
        "yaml",
        "NGINX_SOURCE_MODE",
        "source_mode",
    ),
    ParentProjection(
        NGINX_FULL_SMOKE_WORKFLOW_PATH,
        "yaml",
        "NGINX_SOURCE_REPO_URL",
        "source_repository",
    ),
    ParentProjection(
        NGINX_FULL_SMOKE_WORKFLOW_PATH,
        "yaml",
        "NGINX_RELEASE_TAG",
        "release_tag",
    ),
    ParentProjection(
        NGINX_FULL_SMOKE_WORKFLOW_PATH,
        "yaml",
        "NGINX_SOURCE_GIT_REF",
        "source_ref",
    ),
    ParentProjection(
        NGINX_FULL_SMOKE_WORKFLOW_PATH,
        "yaml",
        "NGINX_RELEASE_ASSET_NAME",
        "release_asset_name",
    ),
    ParentProjection(
        NGINX_FULL_SMOKE_WORKFLOW_PATH,
        "yaml",
        "NGINX_SHA256",
        "archive_sha256",
    ),
    ParentProjection(
        RUNTIME_COMPONENTS_PATH,
        "python",
        "NGINX_PINNED_SOURCE_MODE",
        "source_mode",
    ),
    ParentProjection(
        RUNTIME_COMPONENTS_PATH,
        "python",
        "NGINX_PINNED_SOURCE_REPOSITORY",
        "source_repository",
    ),
    ParentProjection(
        RUNTIME_COMPONENTS_PATH,
        "python",
        "NGINX_PINNED_RELEASE_TAG",
        "release_tag",
    ),
    ParentProjection(
        RUNTIME_COMPONENTS_PATH,
        "python",
        "NGINX_PINNED_SOURCE_REF",
        "source_ref",
    ),
    ParentProjection(
        RUNTIME_COMPONENTS_PATH,
        "python",
        "NGINX_PINNED_RELEASE_ASSET_NAME",
        "release_asset_name",
    ),
    ParentProjection(
        RUNTIME_COMPONENTS_PATH,
        "python",
        "NGINX_PINNED_RELEASE_ASSET_SHA256",
        "archive_sha256",
    ),
    ParentProjection(
        RUNTIME_COMPONENTS_PATH,
        "python",
        "NGINX_PINNED_VERSION_READBACK",
        "version_readback",
    ),
    ParentProjection(
        RUNTIME_PRODUCER_READINESS_PATH,
        "python",
        "CANONICAL_NGINX_SOURCE_MODE",
        "source_mode",
    ),
    ParentProjection(
        RUNTIME_PRODUCER_READINESS_PATH,
        "python",
        "CANONICAL_NGINX_SOURCE_REPOSITORY",
        "source_repository",
    ),
    ParentProjection(
        RUNTIME_PRODUCER_READINESS_PATH,
        "python",
        "CANONICAL_NGINX_RELEASE_TAG",
        "release_tag",
    ),
    ParentProjection(
        RUNTIME_PRODUCER_READINESS_PATH,
        "python",
        "CANONICAL_NGINX_SOURCE_REF",
        "source_ref",
    ),
    ParentProjection(
        RUNTIME_PRODUCER_READINESS_PATH,
        "python",
        "CANONICAL_NGINX_RELEASE_ASSET_NAME",
        "release_asset_name",
    ),
    ParentProjection(
        RUNTIME_PRODUCER_READINESS_PATH,
        "python",
        "CANONICAL_NGINX_ARCHIVE_SHA256",
        "archive_sha256",
    ),
    ParentProjection(
        RUNTIME_PRODUCER_READINESS_PATH,
        "python",
        "CANONICAL_NGINX_VERSION_READBACK",
        "version_readback",
    ),
)

PARENT_NGINX_POLICY_PROJECTIONS = (
    ParentPolicyProjection(
        NGINX_EXACT_HEAD_WORKFLOW_PATH,
        "yaml",
        "NGINX_REQUIRE_PINNED_PROVENANCE",
        "1",
    ),
    ParentPolicyProjection(
        NGINX_FULL_SMOKE_WORKFLOW_PATH,
        "yaml",
        "NGINX_REQUIRE_PINNED_PROVENANCE",
        "1",
    ),
)


def _absolute(path: Path) -> Path:
    return path if path.is_absolute() else Path.cwd() / path


def _require_directory(path: Path, label: str) -> Path:
    absolute = _absolute(path)
    try:
        metadata = os.lstat(absolute)
        resolved = absolute.resolve(strict=True)
    except OSError as error:
        raise ContractError(f"{label} cannot be inspected safely") from error
    if resolved != absolute or stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise ContractError(f"{label} must be a real directory")
    return absolute


def _root_relative_path(root: Path, relative: str) -> Path:
    parts = Path(relative).parts
    if not parts or Path(relative).is_absolute() or any(part in ("", ".", "..") for part in parts):
        raise ContractError(f"unsafe registered Parent path: {relative}")
    current = root
    for part in parts[:-1]:
        current = current / part
        try:
            metadata = os.lstat(current)
        except OSError as error:
            raise ContractError(f"registered Parent directory is unavailable: {relative}") from error
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise ContractError(f"registered Parent directory is unsafe: {relative}")
    return current / parts[-1]


def _read_regular(path: Path, label: str) -> bytes:
    absolute = _absolute(path)
    try:
        metadata = os.lstat(absolute)
        resolved = absolute.resolve(strict=True)
    except OSError as error:
        raise ContractError(f"{label} cannot be inspected safely") from error
    if resolved != absolute or stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise ContractError(f"{label} must be a regular non-symlink file")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise ContractError(f"platform cannot safely open {label} without following symlinks")
    descriptor: int | None = None
    try:
        descriptor = os.open(absolute, os.O_RDONLY | nofollow)
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode) or not os.path.samestat(metadata, opened):
            raise ContractError(f"{label} changed while being opened")
        if opened.st_size < 0 or opened.st_size > MAX_INPUT_BYTES:
            raise ContractError(f"{label} exceeds the bounded input size")
        chunks: list[bytes] = []
        remaining = MAX_INPUT_BYTES + 1
        while remaining:
            chunk = os.read(descriptor, min(65536, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        payload = b"".join(chunks)
        if len(payload) > MAX_INPUT_BYTES:
            raise ContractError(f"{label} exceeds the bounded input size")
        return payload
    except ContractError:
        raise
    except OSError as error:
        raise ContractError(f"{label} cannot be read safely") from error
    finally:
        if descriptor is not None:
            os.close(descriptor)


def _read_text(path: Path, label: str) -> str:
    try:
        return _read_regular(path, label).decode("utf-8")
    except UnicodeDecodeError as error:
        raise ContractError(f"{label} is not UTF-8 text") from error


def _mutable_source_rhs_value(name: str, rhs: str) -> str:
    if rhs != rhs.strip(" \t") or len(rhs) < 2 or rhs[0] != '"' or rhs[-1] != '"':
        raise ContractError(f"Framework common.sh has unsafe source-data syntax in {name}")
    value = rhs[1:-1]
    if not value:
        raise ContractError(f"Framework common.sh has empty source-data value in {name}")
    return value


def _mutable_source_reference(value: str, index: int, name: str) -> tuple[str, int]:
    if value.startswith("${", index):
        closing = value.find("}", index + 2)
        if closing == -1:
            raise ContractError(
                f"Framework common.sh has invalid source-data reference in {name}"
            )
        return value[index + 2 : closing], closing + 1
    match = re.match(r"\$([A-Z][A-Z0-9_]*)", value[index:])
    if match is None:
        raise ContractError(f"Framework common.sh has invalid source-data reference in {name}")
    next_index = index + len(match.group(0))
    if next_index < len(value) and re.match(r"\w", value[next_index], re.ASCII):
        raise ContractError(
            f"Framework common.sh has ambiguous source-data reference in {name}"
        )
    return match.group(1), next_index


def _validate_mutable_source_character(name: str, character: str) -> None:
    if not ("!" <= character <= "~") or character in "`;&|<>\\\"'#(){}":
        raise ContractError(f"Framework common.sh has unsafe source-data syntax in {name}")


def _validate_mutable_source_rhs(name: str, rhs: str) -> None:
    """Accept only a passive, double-quoted generic source-data expression."""

    value = _mutable_source_rhs_value(name, rhs)
    index = 0
    while index < len(value):
        if value[index] == "$":
            reference, index = _mutable_source_reference(value, index, name)
            if reference not in MUTABLE_SOURCE_FIELD_SET:
                raise ContractError(
                    f"Framework common.sh has unknown source-data reference in {name}"
                )
            continue
        _validate_mutable_source_character(name, value[index])
        index += 1


def _normalized_framework_common_structure(text: str) -> bytes:
    """Return the reviewed shell structure with generic data RHSs redacted."""

    seen: set[str] = set()
    normalized: list[str] = []
    for line in text.splitlines(keepends=True):
        content = line.rstrip("\r\n")
        line_ending = line[len(content) :]
        for name in MUTABLE_SOURCE_FIELDS:
            prefix = f"{name}="
            if not content.startswith(prefix):
                continue
            if name in seen:
                raise ContractError(f"Framework common.sh duplicates source-data field {name}")
            _validate_mutable_source_rhs(name, content[len(prefix) :])
            seen.add(name)
            normalized.append(f"{prefix}<PARENT_REVIEWED_SOURCE_DATA>{line_ending}")
            break
        else:
            normalized.append(line)
    missing = [name for name in MUTABLE_SOURCE_FIELDS if name not in seen]
    if missing:
        raise ContractError(
            "Framework common.sh misses source-data fields: " + ", ".join(missing)
        )
    return "".join(normalized).encode("utf-8")


def _framework_common_structure_sha256(payload: bytes) -> str:
    """Hash a UTF-8 candidate's reviewed executable/data structure."""

    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ContractError("Framework common.sh is not UTF-8 text") from error
    return hashlib.sha256(_normalized_framework_common_structure(text)).hexdigest()


def _read_approved_framework_common(path: Path) -> str:
    """Read only the reviewed Framework common.sh structure as candidate data."""

    payload = _read_regular(path, "Framework common.sh")
    if (
        _framework_common_structure_sha256(payload)
        != APPROVED_FRAMEWORK_COMMON_STRUCTURE_SHA256
    ):
        raise ContractError("Framework common.sh differs from approved reviewed structure")
    try:
        return payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ContractError("Framework common.sh is not UTF-8 text") from error


def _unique_match(pattern: re.Pattern[str], text: str, label: str) -> str:
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise ContractError(f"{label} must contain exactly one supported assignment")
    return matches[0].group("value")


def _safe_plain_value(value: str, label: str) -> str:
    value = value.strip()
    if not value or not value.isascii() or any(character in value for character in "\r\n\x00'\"`$;&|<>\\"):
        raise ContractError(f"{label} has an unsafe value")
    return value


def _safe_yaml_value(value: str, label: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] in "\"'" and value[-1] == value[0]:
        value = value[1:-1]
    return _safe_plain_value(value, label)


def _parent_assignment(
    root: Path, projection: ParentProjection | ParentPolicyProjection
) -> str:
    path = _root_relative_path(root, projection.relative_path)
    text = _read_text(path, f"registered Parent projection {projection.relative_path}")
    if projection.syntax == "yaml":
        pattern = re.compile(
            rf"(?m)^[ \t]*{re.escape(projection.name)}[ \t]*:[ \t]*(?P<value>[^\r\n#]+?)[ \t]*(?:#.*)?$"
        )
        return _safe_yaml_value(
            _unique_match(pattern, text, f"{projection.relative_path}:{projection.name}"),
            f"{projection.relative_path}:{projection.name}",
        )
    if projection.syntax == "python":
        pattern = re.compile(
            rf"(?m)^{re.escape(projection.name)}[ \t]*=[ \t]*\"(?P<value>[^\"\\\r\n]*)\"[ \t]*(?:#.*)?$"
        )
        return _safe_plain_value(
            _unique_match(pattern, text, f"{projection.relative_path}:{projection.name}"),
            f"{projection.relative_path}:{projection.name}",
        )
    raise ContractError(f"unsupported registered Parent syntax: {projection.syntax}")


def _candidate_field_writes(text: str, name: str) -> list[re.Match[str]]:
    """Find shell forms that can mutate one named candidate field.

    The verifier is deliberately data-only.  It accepts one plain assignment
    below and treats every other write spelling as unsupported rather than
    trying to emulate a sourced shell program.
    """

    pattern = re.compile(
        rf"(?<![A-Za-z0-9_]){re.escape(name)}(?:\[[^\]\r\n]*\])?[ \t]*(?:\+?=|\+\+|--)",
        re.ASCII,
    )
    return list(pattern.finditer(text))


def _reject_unsupported_candidate_field_mutation(text: str, name: str) -> None:
    parameter_assignment = re.compile(rf"\$\{{{re.escape(name)}:?=", re.ASCII)
    mutating_builtin = re.compile(
        rf"(?m)^[ \t]*(?:declare|getopts|local|mapfile|printf|read|readonly|typeset|unset)\b"
        rf"[^\r\n]*\b{re.escape(name)}\b",
        re.ASCII,
    )
    loop_assignment = re.compile(
        rf"(?m)^[ \t]*(?:for|select)[ \t]+{re.escape(name)}\b", re.ASCII
    )
    if (
        parameter_assignment.search(text)
        or mutating_builtin.search(text)
        or loop_assignment.search(text)
    ):
        raise ContractError(f"Framework common.sh:{name} uses unsupported shell mutation syntax")


def _candidate_rhs(text: str, name: str) -> str:
    _reject_unsupported_candidate_field_mutation(text, name)
    plain_assignment = re.compile(
        rf"(?m)^{re.escape(name)}=(?P<value>[^\r\n]*)$", re.ASCII
    )
    plain_matches = list(plain_assignment.finditer(text))
    writes = _candidate_field_writes(text, name)
    if (
        len(plain_matches) != 1
        or len(writes) != 1
        or writes[0].start() != plain_matches[0].start()
    ):
        raise ContractError(
            f"Framework common.sh:{name} must contain exactly one plain top-level assignment"
        )
    return plain_matches[0].group("value")


def _reject_parent_owned_candidate_assignments(text: str) -> None:
    for name in PARENT_OWNED_NGINX_FIELDS:
        _reject_unsupported_candidate_field_mutation(text, name)
        if _candidate_field_writes(text, name):
            raise ContractError(f"Framework common.sh must not assign Parent-owned {name}")


def _reject_dynamic_candidate_evaluation(text: str) -> None:
    """Reject evaluation that can conceal an effective target-field write."""

    if DYNAMIC_SHELL_EVALUATION.search(text):
        raise ContractError("Framework common.sh uses unsupported dynamic shell evaluation")


def _quoted_rhs(rhs: str, label: str) -> str:
    value = rhs.strip(" \t")
    if len(value) < 2 or value[0] not in "\"'" or value[-1] != value[0]:
        raise ContractError(f"{label} must be one balanced quoted value")
    content = value[1:-1]
    if not content or not content.isascii() or any(character in content for character in "\r\n\x00'\"`;&|<>\\"):
        raise ContractError(f"{label} has unsafe shell syntax")
    return content


def parse_candidate_nginx_handoff(common_path: Path) -> dict[str, str]:
    """Read the candidate NGINX tuple without sourcing its shell file."""

    text = _read_approved_framework_common(common_path)
    _reject_dynamic_candidate_evaluation(text)
    _reject_parent_owned_candidate_assignments(text)
    raw = {name: _quoted_rhs(_candidate_rhs(text, name), name) for name in NGINX_FIELDS}
    tag = raw["NGINX_RELEASE_TAG"]
    match = NGINX_TAG.fullmatch(tag)
    if match is None:
        raise ContractError("NGINX_RELEASE_TAG is not a stable release tag")
    version = match.group("version")
    source_ref = raw["NGINX_SOURCE_GIT_REF"]
    if source_ref == "$NGINX_RELEASE_TAG":
        source_ref = tag
    asset_name = raw["NGINX_RELEASE_ASSET_NAME"]
    if asset_name == "nginx-${NGINX_RELEASE_TAG#release-}.tar.gz":
        asset_name = f"nginx-{version}.tar.gz"
    actual = {
        "source_mode": raw["NGINX_SOURCE_MODE"],
        "source_repository": raw["NGINX_SOURCE_REPO_URL"],
        "release_tag": tag,
        "source_ref": source_ref,
        "release_asset_name": asset_name,
        "archive_sha256": raw["NGINX_SHA256"],
        "version_readback": f"nginx/{version}",
    }
    if HEX64.fullmatch(actual["archive_sha256"]) is None:
        raise ContractError("candidate NGINX handoff is not one canonical release tuple")
    expected = {
        "source_mode": "github-release",
        "source_repository": "https://github.com/nginx/nginx",
        "release_tag": tag,
        "source_ref": tag,
        "release_asset_name": f"nginx-{version}.tar.gz",
        "version_readback": f"nginx/{version}",
    }
    if any(actual[name] != expected_value for name, expected_value in expected.items()):
        raise ContractError("candidate NGINX handoff is not one canonical release tuple")
    return actual


def _verify_framework_sha_contract(root: Path, candidate_sha: str) -> None:
    workflow = _read_text(
        _root_relative_path(root, ".github/workflows/test-connectors-with-crs-no-mrts.yml"),
        "CRS/no-MRTS workflow",
    )
    workflow_sha = _unique_match(
        re.compile(r"(?m)^ {6}EXPECTED_FRAMEWORK_SHA:[ \t]*(?P<value>[0-9a-f]{40})[ \t]*$"),
        workflow,
        "CRS/no-MRTS workflow expected Framework SHA",
    )
    literal_framework_shas = [
        _safe_yaml_value(
            match.group("value"), "CRS/no-MRTS workflow literal Framework SHA"
        )
        for match in LITERAL_FRAMEWORK_SHA.finditer(workflow)
    ]
    if not literal_framework_shas:
        raise ContractError("CRS/no-MRTS workflow has no literal Framework SHA consumers")
    fixture = _read_text(
        _root_relative_path(root, "tests/test_ci_security_workflows.py"),
        "CRS/no-MRTS workflow fixture",
    )
    fixture_sha = _unique_match(
        re.compile(
            r'(?m)^WITH_CRS_NO_MRTS_FRAMEWORK_SHA[ \t]*=[ \t]*"(?P<value>[0-9a-f]{40})"[ \t]*$'
        ),
        fixture,
        "CRS/no-MRTS workflow fixture Framework SHA",
    )
    for label, observed in (("workflow", workflow_sha), ("fixture", fixture_sha)):
        if observed != candidate_sha:
            raise ContractError(
                f"CRS/no-MRTS {label} Framework SHA does not match candidate SHA"
            )
    for index, observed in enumerate(literal_framework_shas, start=1):
        if observed != candidate_sha:
            raise ContractError(
                f"CRS/no-MRTS workflow literal Framework SHA consumer {index} "
                "does not match candidate SHA"
            )


def _verify_unprotected_nginx_handoff(root: Path, values: dict[str, str]) -> None:
    for projection in PARENT_NGINX_PROJECTIONS:
        observed = _parent_assignment(root, projection)
        expected = values[projection.value_name]
        if observed != expected:
            raise ContractError(
                f"unprotected NGINX handoff mismatch at "
                f"{projection.relative_path}:{projection.name}"
            )
    exact_head = _read_text(
        _root_relative_path(root, NGINX_EXACT_HEAD_WORKFLOW_PATH),
        "NGINX exact-head workflow",
    )
    archive = _unique_match(
        re.compile(r'(?m)^\s*--nginx-archive "\$NGINX_DOWNLOAD_DIR/(?P<value>nginx-[0-9.]+\.tar\.gz)" \\$'),
        exact_head,
        "NGINX exact-head archive argument",
    )
    if archive != values["release_asset_name"]:
        raise ContractError("NGINX exact-head archive argument does not match handoff")


def _verify_parent_nginx_policy(root: Path) -> None:
    for projection in PARENT_NGINX_POLICY_PROJECTIONS:
        observed = _parent_assignment(root, projection)
        if observed != projection.expected_value:
            raise ContractError(
                f"Parent NGINX policy mismatch at {projection.relative_path}:{projection.name}"
            )


def verify_contract(root: Path, candidate_sha: str, framework_common: Path) -> dict[str, str]:
    repository_root = _require_directory(root, "repository root")
    if not HEX40.fullmatch(candidate_sha):
        raise ContractError("candidate SHA must be exactly 40 lowercase hexadecimal characters")
    _verify_framework_sha_contract(repository_root, candidate_sha)
    nginx = parse_candidate_nginx_handoff(framework_common)
    _verify_parent_nginx_policy(repository_root)
    _verify_unprotected_nginx_handoff(repository_root, nginx)
    return nginx


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).parents[2])
    parser.add_argument("--candidate-sha", required=True)
    parser.add_argument("--framework-common", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        nginx = verify_contract(args.repo_root, args.candidate_sha, args.framework_common)
    except (ContractError, OSError) as error:
        print(f"verify-framework-candidate-contract: error: {error}")
        return 2
    print(
        json.dumps(
            {
                "candidate_sha": args.candidate_sha,
                "nginx_release_tag": nginx["release_tag"],
                "status": "verified",
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
