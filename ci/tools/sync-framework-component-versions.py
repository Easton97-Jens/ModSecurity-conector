#!/usr/bin/env python3
"""Synchronize fixed Parent component pins from approved Framework data.

``common.sh`` is never sourced or executed. The protected update workflow
proves the Framework Git object, extracts its ``ci/lib/common.sh`` as a data
file, and this tool accepts only a bounded registry-defined data grammar. It
can write only the explicit Parent target registry.

NGINX is intentionally outside this generic synchronizer. Its privileged
release tuple remains owned by the dedicated root-broker workflow and must be
updated through an independently reviewed NGINX change.
"""
from __future__ import annotations

import argparse
from collections.abc import Callable
from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
import stat
import tempfile
from urllib.parse import urlsplit


MAX_COMMON_BYTES = 256 * 1024
MAX_RESOLUTION_DEPTH = 32
MAX_RESOLVED_VALUE_BYTES = 64 * 1024
MAX_RESOLVED_TOTAL_BYTES = 256 * 1024
HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")
HEX40 = re.compile(r"^[0-9a-fA-F]{40}$")
SAFE_PATCH = re.compile(r"^[A-Za-z0-9._-]+\.patch$")
SERIES = re.compile(r"^(?a:\d+)\.(?a:\d+)$")
OFFICIAL_LIGHTTPD_RELEASE_ROOT_URL = "https://download.lighttpd.net/lighttpd"
OFFICIAL_HAPROXY_RELEASE_ROOT_URL = "https://www.haproxy.org/download"
OFFICIAL_CRS_REPOSITORY = "https://github.com/coreruleset/coreruleset.git"
ENVOY_PROJECTION = "Envoy projection"
LIGHTTPD_PROJECTION = "Lighttpd projection"
LIGHTTPD_RESOLUTION_DEPENDENCY = "Lighttpd resolution dependency"
HAPROXY_RUNTIME_TUPLE = "HAProxy runtime tuple"
HAPROXY_RESOLUTION_DEPENDENCY = "HAProxy resolution dependency"
HAPROXY_RUNTIME_PROJECTION = "HAProxy runtime projection"
HAPROXY_HTX_TUPLE = "HAProxy HTX tuple"
HAPROXY_HTX_PROJECTION = "HAProxy HTX projection"
HAPROXY_HTX_RESOLUTION_DEPENDENCY = "HAProxy HTX resolution dependency"
CRS_PROJECTION = "CRS Parent projections"


class SyncError(ValueError):
    """The approved Framework data or a fixed Parent target is unsafe."""


def _ascii_digits(value: str) -> bool:
    return bool(value) and all("0" <= character <= "9" for character in value)


def _semantic_version(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parts = value.split(".")
    return len(parts) == 3 and all(_ascii_digits(part) for part in parts)


def _series(value: object) -> bool:
    return isinstance(value, str) and bool(SERIES.fullmatch(value))


def _safe_ascii_value(value: str) -> bool:
    """Accept only printable, non-shell-significant resolved data."""

    if not value or not value.isascii():
        return False
    return all(
        "!" <= character <= "~"
        and character not in "$`;&|<>\\\"'#"
        for character in value
    )


def _fixed_value(expected: str) -> Callable[[str], bool]:
    return lambda value: value == expected


def _assignment_key(value: str) -> bool:
    if not value or not ("A" <= value[0] <= "Z"):
        return False
    return all(
        "A" <= character <= "Z" or "0" <= character <= "9" or character == "_"
        for character in value[1:]
    )


def _assignment(line: str) -> tuple[str, str] | None:
    """Parse one bounded shell-like assignment without ambiguous regex matching."""

    lhs, separator, rhs = line.partition("=")
    if not separator:
        return None
    key = lhs.strip(" \t")
    if not _assignment_key(key):
        return None
    return key, rhs.lstrip(" \t")


@dataclass(frozen=True)
class SourceField:
    """One fixed Framework datum that the Parent may consume or resolve."""

    name: str
    required: bool
    allowed_expression_types: tuple[str, ...]
    validator: Callable[[str], bool]
    parent_consumer: str


LITERAL = ("literal",)
REFERENCES = ("literal", "references")

# This is a source/data allowlist, deliberately separate from TARGET_REGISTRY.
# It records direct Parent consumers and the intermediate fields required to
# resolve their tuples. Framework-only pins are intentionally not listed and
# cannot influence Parent output.
SOURCE_REGISTRY = (
    SourceField("ENVOY_VERSION", True, LITERAL, _semantic_version, ENVOY_PROJECTION),
    SourceField("LIGHTTPD_SERIES", True, LITERAL, _series, "Lighttpd provenance"),
    SourceField(
        "LIGHTTPD_RELEASE_ROOT_URL",
        True,
        LITERAL,
        _safe_ascii_value,
        LIGHTTPD_RESOLUTION_DEPENDENCY,
    ),
    SourceField(
        "LIGHTTPD_SERIES_BASE_URL",
        True,
        REFERENCES,
        _safe_ascii_value,
        LIGHTTPD_RESOLUTION_DEPENDENCY,
    ),
    SourceField("LIGHTTPD_VERSION", True, LITERAL, _semantic_version, LIGHTTPD_PROJECTION),
    SourceField(
        "LIGHTTPD_SOURCE_URL",
        True,
        REFERENCES,
        _safe_ascii_value,
        LIGHTTPD_PROJECTION,
    ),
    SourceField(
        "LIGHTTPD_ARCHIVE_NAME",
        True,
        REFERENCES,
        _safe_ascii_value,
        LIGHTTPD_RESOLUTION_DEPENDENCY,
    ),
    SourceField(
        "LIGHTTPD_DOWNLOAD_URL",
        True,
        REFERENCES,
        _safe_ascii_value,
        LIGHTTPD_PROJECTION,
    ),
    SourceField(
        "LIGHTTPD_SHA256",
        True,
        LITERAL,
        lambda value: bool(HEX64.fullmatch(value)),
        LIGHTTPD_PROJECTION,
    ),
    SourceField("HAPROXY_SERIES", True, LITERAL, _series, HAPROXY_RUNTIME_TUPLE),
    SourceField(
        "HAPROXY_RELEASE_ROOT_URL",
        True,
        LITERAL,
        _safe_ascii_value,
        HAPROXY_RESOLUTION_DEPENDENCY,
    ),
    SourceField(
        "HAPROXY_SERIES_BASE_URL",
        True,
        REFERENCES,
        _safe_ascii_value,
        HAPROXY_RESOLUTION_DEPENDENCY,
    ),
    SourceField("HAPROXY_VERSION", True, LITERAL, _semantic_version, HAPROXY_RUNTIME_PROJECTION),
    SourceField(
        "HAPROXY_ARCHIVE_NAME",
        True,
        REFERENCES,
        _safe_ascii_value,
        HAPROXY_RESOLUTION_DEPENDENCY,
    ),
    SourceField(
        "HAPROXY_SOURCE_URL",
        True,
        REFERENCES,
        _safe_ascii_value,
        HAPROXY_RUNTIME_TUPLE,
    ),
    SourceField(
        "HAPROXY_SHA256",
        True,
        LITERAL,
        lambda value: bool(HEX64.fullmatch(value)),
        HAPROXY_RUNTIME_TUPLE,
    ),
    SourceField("HAPROXY_HTX_SERIES", True, LITERAL, _series, HAPROXY_HTX_TUPLE),
    SourceField(
        "HAPROXY_HTX_SERIES_BASE_URL",
        True,
        REFERENCES,
        _safe_ascii_value,
        HAPROXY_HTX_RESOLUTION_DEPENDENCY,
    ),
    SourceField(
        "HAPROXY_HTX_VERSION",
        True,
        LITERAL,
        _semantic_version,
        HAPROXY_HTX_PROJECTION,
    ),
    SourceField(
        "HAPROXY_HTX_ARCHIVE_NAME",
        True,
        REFERENCES,
        _safe_ascii_value,
        HAPROXY_HTX_RESOLUTION_DEPENDENCY,
    ),
    SourceField(
        "HAPROXY_HTX_SOURCE_URL",
        True,
        REFERENCES,
        _safe_ascii_value,
        HAPROXY_HTX_PROJECTION,
    ),
    SourceField(
        "HAPROXY_HTX_SHA256",
        True,
        LITERAL,
        lambda value: bool(HEX64.fullmatch(value)),
        HAPROXY_HTX_PROJECTION,
    ),
    SourceField(
        "CRS_APPROVED_REPO_URL",
        True,
        LITERAL,
        _fixed_value(OFFICIAL_CRS_REPOSITORY),
        CRS_PROJECTION,
    ),
    SourceField(
        "CRS_APPROVED_COMMIT",
        True,
        LITERAL,
        lambda value: bool(HEX40.fullmatch(value)),
        CRS_PROJECTION,
    ),
    SourceField(
        "CRS_RELEASE_TAG",
        True,
        LITERAL,
        lambda value: bool(re.fullmatch(r"v(?a:\d+)\.(?a:\d+)\.(?a:\d+)", value)),
        CRS_PROJECTION,
    ),
)
SOURCE_FIELDS = {field.name: field for field in SOURCE_REGISTRY}
if len(SOURCE_FIELDS) != len(SOURCE_REGISTRY):
    raise RuntimeError("duplicate source field registry entry")


@dataclass(frozen=True)
class TargetSpec:
    relative_path: str
    fields: tuple[tuple[str, str], ...]
    syntax: str


@dataclass(frozen=True)
class RenderedTarget:
    path: Path
    original: bytes
    replacement: bytes
    mode: int


# This is the sole Parent write allowlist. Discovery never broadens it: a new
# Framework value needs an explicit target and a dedicated target renderer.
TARGET_REGISTRY = (
    TargetSpec(
        "connectors/envoy/config/envoy-ext-proc-versions.env",
        (("ENVOY_RELEASE", "ENVOY_VERSION"), ("ENVOY_IMAGE", "ENVOY_IMAGE")),
        "shell",
    ),
    TargetSpec(
        "ci/provisioning/components/prepare-runtime-components.py",
        (("DEFAULT_HAPROXY_VERSION", "HAPROXY_VERSION"),),
        "python",
    ),
    TargetSpec(
        "ci/runtime/broker/nginx_root_broker.py",
        (
            ("CRS_APPROVED_REPOSITORY", "CRS_APPROVED_REPO_URL"),
            ("CRS_RELEASE_TAG", "CRS_RELEASE_TAG"),
            ("CRS_APPROVED_COMMIT", "CRS_APPROVED_COMMIT"),
        ),
        "python",
    ),
    TargetSpec(
        "ci/runtime/broker/protected_nginx_broker_caller.py",
        (
            ("CRS_REPOSITORY", "CRS_APPROVED_REPO_URL"),
            ("CRS_RELEASE_TAG", "CRS_RELEASE_TAG"),
            ("CRS_COMMIT", "CRS_APPROVED_COMMIT"),
        ),
        "python",
    ),
    TargetSpec(
        "connectors/lighttpd/lighttpd-version.contract",
        (
            ("LIGHTTPD_SERIES", "LIGHTTPD_SERIES"),
            ("LIGHTTPD_VERSION", "LIGHTTPD_VERSION"),
            ("LIGHTTPD_SOURCE_URL", "LIGHTTPD_SOURCE_URL"),
            ("LIGHTTPD_DOWNLOAD_URL", "LIGHTTPD_DOWNLOAD_URL"),
            ("LIGHTTPD_SHA256", "LIGHTTPD_SHA256"),
        ),
        "lighttpd-contract",
    ),
    TargetSpec(
        "connectors/lighttpd/SOURCE_MAP.json",
        (
            ("repository", "LIGHTTPD_SOURCE_URL"),
            ("series", "LIGHTTPD_SERIES"),
            ("version", "LIGHTTPD_VERSION"),
            ("download_url", "LIGHTTPD_DOWNLOAD_URL"),
        ),
        "lighttpd-source-map",
    ),
    TargetSpec(
        "connectors/haproxy/htx-overlay/version-contract.json",
        (
            ("version", "HAPROXY_HTX_VERSION"),
            ("source_url", "HAPROXY_HTX_SOURCE_URL"),
            ("sha256", "HAPROXY_HTX_SHA256"),
        ),
        "haproxy-contract",
    ),
)

# Security boundary: the general Framework updater must never regain ownership
# of NGINX. NGINX source data and Parent projections belong to its dedicated
# root-broker workflow and independently reviewed release process.
if any(field.name.startswith("NGINX_") for field in SOURCE_REGISTRY):
    raise RuntimeError("NGINX must not be registered as Framework source data")
if any(
    source_name.startswith("NGINX_")
    for spec in TARGET_REGISTRY
    for _target_name, source_name in spec.fields
):
    raise RuntimeError("NGINX must not be registered as a Framework Parent target")


def _absolute(path: Path) -> Path:
    """Make a lexical absolute path without resolving caller-controlled links."""

    return Path(os.path.abspath(os.fspath(path)))


def _walk_no_symlinks(path: Path, label: str) -> os.stat_result:
    """Return metadata only when every existing component is non-symlink."""

    if not path.is_absolute():
        raise SyncError(f"{label} path must be absolute")
    current = Path(path.anchor)
    try:
        metadata = current.lstat()
    except OSError as exc:
        raise SyncError(f"cannot inspect {label}: {current}") from exc
    if not stat.S_ISDIR(metadata.st_mode):
        raise SyncError(f"{label} path has an invalid filesystem root")
    for part in path.parts[1:]:
        current /= part
        try:
            metadata = current.lstat()
        except OSError as exc:
            raise SyncError(f"cannot inspect {label}: {current}") from exc
        if stat.S_ISLNK(metadata.st_mode):
            raise SyncError(f"{label} must not contain symlinks: {current}")
        if current != path and not stat.S_ISDIR(metadata.st_mode):
            raise SyncError(f"{label} has a non-directory path component: {current}")
    return metadata


def _require_directory(path: Path, label: str) -> Path:
    absolute = _absolute(path)
    metadata = _walk_no_symlinks(absolute, label)
    if not stat.S_ISDIR(metadata.st_mode):
        raise SyncError(f"{label} must be a directory")
    return absolute


def _allowed_path(path: Path, allowed_root: Path, label: str) -> Path:
    """Return a path proven to stay below an explicit, non-symlink root."""

    absolute = _absolute(path)
    root = _require_directory(allowed_root, f"{label} allowed root")
    try:
        resolved = absolute.resolve(strict=True)
        resolved_root = root.resolve(strict=True)
    except OSError as exc:
        raise SyncError(f"cannot resolve {label}: {absolute}") from exc
    if resolved != absolute:
        raise SyncError(f"{label} must not contain symlinks: {absolute}")
    if not resolved.is_relative_to(resolved_root):
        raise SyncError(f"{label} is outside its allowed root: {absolute}")
    return resolved


def _framework_common_root() -> Path:
    """Select the runner-controlled temporary root for extracted Framework data."""

    configured = os.environ.get("RUNNER_TEMP")
    root = Path(configured) if configured else Path(tempfile.gettempdir())
    if not root.is_absolute():
        raise SyncError("Framework common temporary root must be absolute")
    return root


def _read_regular(
    path: Path,
    label: str,
    *,
    allowed_root: Path,
    maximum: int | None = None,
) -> tuple[bytes, int]:
    """Read a checked regular file without following its final path element."""

    absolute = _allowed_path(path, allowed_root, label)
    metadata = _walk_no_symlinks(absolute, label)
    if not stat.S_ISREG(metadata.st_mode):
        raise SyncError(f"{label} must be a regular file")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(absolute, flags)
    except OSError as exc:
        raise SyncError(f"cannot open {label}: {absolute}") from exc
    try:
        opened_metadata = os.fstat(descriptor)
        if not stat.S_ISREG(opened_metadata.st_mode):
            raise SyncError(f"{label} must be a regular file")
        if maximum is not None and opened_metadata.st_size > maximum:
            raise SyncError(f"{label} exceeds the bounded input size")
        with os.fdopen(descriptor, "rb", closefd=True) as handle:
            descriptor = -1
            contents = handle.read((maximum + 1) if maximum is not None else -1)
        if maximum is not None and len(contents) > maximum:
            raise SyncError(f"{label} exceeds the bounded input size")
        return contents, stat.S_IMODE(opened_metadata.st_mode)
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def _target_path(root: Path, relative_path: str) -> Path:
    relative = Path(relative_path)
    if relative.is_absolute() or any(part in ("", ".", "..") for part in relative.parts):
        raise SyncError(f"unsafe registered target path: {relative_path}")
    target = root.joinpath(*relative.parts)
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise SyncError(f"registered target escapes the repository: {relative_path}") from exc
    _walk_no_symlinks(target, f"registered target {relative_path}")
    return target


def _unquote(rhs: str, key: str) -> str:
    # Preserve CR/LF so the source-expression gate can reject them explicitly.
    value = rhs.strip(" \t")
    if not value:
        raise SyncError(f"empty assignment in {key}")
    if value[0] in "\"'":
        if len(value) < 2 or value[-1] != value[0]:
            raise SyncError(f"unbalanced quotation in {key}")
        return value[1:-1]
    if value[-1] in "\"'":
        raise SyncError(f"unbalanced quotation in {key}")
    return value


def _literal(rhs: str, key: str) -> str:
    """Read a literal from a generated Parent contract, never Framework data."""

    value = _unquote(rhs, key)
    if not _safe_ascii_value(value):
        raise SyncError(f"unsafe shell syntax in {key}")
    return value


def _require_expression_type(field: SourceField, expression_type: str) -> None:
    if expression_type not in field.allowed_expression_types:
        raise SyncError(
            f"unsupported {expression_type} expression in {field.name}"
        )


def _braced_source_variable_part(value: str, index: int, field: SourceField) -> tuple[tuple[str, str, str], int]:
    closing = value.find("}", index + 2)
    if closing == -1:
        raise SyncError(f"unbalanced parameter expansion in {field.name}")
    body = value[index + 2 : closing]
    if _assignment_key(body):
        _require_expression_type(field, "references")
        if body not in SOURCE_FIELDS:
            raise SyncError(f"unknown source variable reference in {field.name}: {body}")
        return ("reference", body, ""), closing + 1
    raise SyncError(f"unsupported parameter expansion in {field.name}")


def _source_variable_part(value: str, index: int, field: SourceField) -> tuple[tuple[str, str, str], int]:
    if index + 1 >= len(value):
        raise SyncError(f"invalid variable reference in {field.name}")
    if value[index + 1] == "{":
        return _braced_source_variable_part(value, index, field)
    match = re.match(r"\$([A-Z][A-Z0-9_]*)", value[index:])
    if match is None:
        raise SyncError(f"invalid variable reference in {field.name}")
    reference = match.group(1)
    _require_expression_type(field, "references")
    if reference not in SOURCE_FIELDS:
        raise SyncError(f"unknown source variable reference in {field.name}: {reference}")
    return ("reference", reference, ""), index + len(match.group(0))


def _source_expression_parts(rhs: str, field: SourceField) -> list[tuple[str, str, str]]:
    """Tokenize one allowlisted non-executing assignment expression."""

    stripped = rhs.strip(" \t")
    if stripped.startswith("'"):
        raise SyncError(f"single-quoted assignment is unsupported in {field.name}")
    value = _unquote(rhs, field.name)
    if any(character in value for character in ("`", ";", "|", "&", "<", ">", "\\", "\r", "\n", "\x00", "'", "\"", "(", ")")):
        raise SyncError(f"unsafe shell syntax in {field.name}")
    if re.search(r"(?:^|(?a:\W|_))eval(?:$|(?a:\W|_))", value):
        raise SyncError(f"unsafe shell syntax in {field.name}")

    parts: list[tuple[str, str, str]] = []
    literal: list[str] = []
    index = 0
    while index < len(value):
        character = value[index]
        if character == "$":
            if literal:
                parts.append(("literal", "".join(literal), ""))
                literal = []
            part, index = _source_variable_part(value, index, field)
            parts.append(part)
            continue
        if character in "{}":
            raise SyncError(f"unsupported shell syntax in {field.name}")
        literal.append(character)
        index += 1
    if literal:
        parts.append(("literal", "".join(literal), ""))
    if not parts:
        raise SyncError(f"empty assignment in {field.name}")
    if all(kind == "literal" for kind, _value, _detail in parts):
        _require_expression_type(field, "literal")
    return parts


def _resolve_source_fragments(
    name: str,
    raw: dict[str, str],
    states: dict[str, str],
    resolved: dict[str, str],
    depth: int,
    resolved_total_bytes: list[int],
) -> tuple[str, int]:
    fragments: list[str] = []
    resolved_size_bytes = 0
    for kind, value, detail in _source_expression_parts(raw[name], SOURCE_FIELDS[name]):
        if kind == "literal":
            fragment = value
        else:
            fragment = _resolve_source_name(
                value, raw, states, resolved, depth + 1, resolved_total_bytes
            )
            if kind == "prefix_remove":
                if not fragment.startswith(detail):
                    raise SyncError(f"{name} prefix removal does not match referenced value")
                fragment = fragment.removeprefix(detail)
        resolved_size_bytes += len(fragment.encode("utf-8"))
        if resolved_size_bytes > MAX_RESOLVED_VALUE_BYTES:
            raise SyncError(f"resolved assignment exceeds byte budget in {name}")
        fragments.append(fragment)
    resolved_value = "".join(fragments)
    if not resolved_value:
        raise SyncError(f"empty resolved assignment in {name}")
    return resolved_value, resolved_size_bytes


def _resolve_source_name(
    name: str,
    raw: dict[str, str],
    states: dict[str, str],
    resolved: dict[str, str],
    depth: int,
    resolved_total_bytes: list[int],
) -> str:
    if depth > MAX_RESOLUTION_DEPTH:
        raise SyncError(f"source assignment resolution exceeds depth limit at {name}")
    state = states.get(name)
    if state == "active":
        raise SyncError(f"cyclic source assignment reference at {name}")
    if state == "complete":
        return resolved[name]
    states[name] = "active"
    resolved_value, resolved_size_bytes = _resolve_source_fragments(
        name, raw, states, resolved, depth, resolved_total_bytes
    )
    if resolved_total_bytes[0] + resolved_size_bytes > MAX_RESOLVED_TOTAL_BYTES:
        raise SyncError("resolved source assignments exceed aggregate byte budget")
    if not SOURCE_FIELDS[name].validator(resolved_value):
        raise SyncError(f"resolved value is invalid for {name}")
    resolved[name] = resolved_value
    resolved_total_bytes[0] += resolved_size_bytes
    states[name] = "complete"
    return resolved_value


def _resolve_source_values(raw: dict[str, str]) -> dict[str, str]:
    """Resolve only fixed-registry references without a shell or environment."""

    states: dict[str, str] = {}
    resolved: dict[str, str] = {}
    resolved_total_bytes = [0]
    for field in SOURCE_REGISTRY:
        _resolve_source_name(
            field.name, raw, states, resolved, 0, resolved_total_bytes
        )
    return resolved


def parse_common(path: Path) -> dict[str, str]:
    contents, _mode = _read_regular(
        path,
        "Framework common.sh",
        allowed_root=_framework_common_root(),
        maximum=MAX_COMMON_BYTES,
    )
    try:
        text = contents.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SyncError("Framework common.sh is not UTF-8 text") from exc
    raw: dict[str, str] = {}
    for line_number, line in enumerate(text.split("\n"), start=1):
        assignment = _assignment(line)
        if assignment is None:
            continue
        key, rhs = assignment
        if key not in SOURCE_FIELDS:
            continue
        if line.startswith((" ", "\t")):
            raise SyncError(f"known assignment must be top-level at line {line_number}: {key}")
        if key in raw:
            raise SyncError(f"duplicate required assignment: {key}")
        raw[key] = rhs
    missing = [field.name for field in SOURCE_REGISTRY if field.required and field.name not in raw]
    if missing:
        raise SyncError("missing required Framework assignments: " + ", ".join(missing))
    values = _resolve_source_values(raw)
    _validate(values)
    return values


def _major_minor(version: str) -> str:
    return ".".join(version.split(".")[:2])


def _validate_exact_https_url(value: str, expected: str, label: str) -> None:
    """Require one canonical HTTPS URL with no authority/path ambiguity."""

    try:
        parsed = urlsplit(value)
        expected_parsed = urlsplit(expected)
        port = parsed.port
    except ValueError as exc:
        raise SyncError(f"invalid {label} URL") from exc
    if (
        value != expected
        or parsed.scheme != "https"
        or parsed.netloc != expected_parsed.netloc
        or parsed.hostname != expected_parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or port is not None
        or parsed.query
        or parsed.fragment
        or "//" in parsed.path
    ):
        raise SyncError(f"unsupported {label} URL")


def _validate(values: dict[str, str]) -> None:
    _validate_versions(values)
    _validate_lighttpd(values)
    _validate_haproxy(values)
    _validate_crs(values)


def _validate_versions(values: dict[str, str]) -> None:
    for key in (
        "ENVOY_VERSION",
        "LIGHTTPD_VERSION",
        "HAPROXY_VERSION",
        "HAPROXY_HTX_VERSION",
    ):
        if not _semantic_version(values[key]):
            raise SyncError(f"{key} is not a semantic version")


def _validate_lighttpd(values: dict[str, str]) -> None:
    series = values["LIGHTTPD_SERIES"]
    version = values["LIGHTTPD_VERSION"]
    root = values["LIGHTTPD_RELEASE_ROOT_URL"]
    if not _series(series) or _major_minor(version) != series:
        raise SyncError("LIGHTTPD_SERIES does not match LIGHTTPD_VERSION")
    _validate_exact_https_url(
        root,
        OFFICIAL_LIGHTTPD_RELEASE_ROOT_URL,
        "LIGHTTPD_RELEASE_ROOT_URL",
    )
    expected_base = f"{root}/releases-{series}.x"
    if values["LIGHTTPD_SERIES_BASE_URL"] != expected_base:
        raise SyncError("LIGHTTPD_SERIES_BASE_URL does not match its series")
    expected_source = f"{expected_base}/"
    _validate_exact_https_url(
        values["LIGHTTPD_SOURCE_URL"], expected_source, "LIGHTTPD_SOURCE_URL"
    )
    expected_archive = f"lighttpd-{version}.tar.xz"
    if values["LIGHTTPD_ARCHIVE_NAME"] != expected_archive:
        raise SyncError("LIGHTTPD_ARCHIVE_NAME does not match LIGHTTPD_VERSION")
    expected_download = f"{expected_source}{expected_archive}"
    _validate_exact_https_url(
        values["LIGHTTPD_DOWNLOAD_URL"],
        expected_download,
        "LIGHTTPD_DOWNLOAD_URL",
    )
    if not HEX64.fullmatch(values["LIGHTTPD_SHA256"]):
        raise SyncError("LIGHTTPD_SHA256 is not a SHA-256 digest")


def _validate_haproxy_tuple(values: dict[str, str], prefix: str) -> None:
    series = values[f"{prefix}_SERIES"]
    version = values[f"{prefix}_VERSION"]
    base = values[f"{prefix}_SERIES_BASE_URL"]
    archive = values[f"{prefix}_ARCHIVE_NAME"]
    source = values[f"{prefix}_SOURCE_URL"]
    digest = values[f"{prefix}_SHA256"]
    if not _series(series) or _major_minor(version) != series:
        raise SyncError(f"{prefix}_SERIES does not match {prefix}_VERSION")
    expected_base = f"{OFFICIAL_HAPROXY_RELEASE_ROOT_URL}/{series}/src"
    if base != expected_base:
        raise SyncError(f"{prefix}_SERIES_BASE_URL does not match its series")
    expected_archive = f"haproxy-{version}.tar.gz"
    if archive != expected_archive:
        raise SyncError(f"{prefix}_ARCHIVE_NAME does not match {prefix}_VERSION")
    expected_source = f"{expected_base}/{expected_archive}"
    _validate_exact_https_url(source, expected_source, f"{prefix}_SOURCE_URL")
    if not HEX64.fullmatch(digest):
        raise SyncError(f"{prefix}_SHA256 is not a SHA-256 digest")


def _validate_haproxy(values: dict[str, str]) -> None:
    _validate_exact_https_url(
        values["HAPROXY_RELEASE_ROOT_URL"],
        OFFICIAL_HAPROXY_RELEASE_ROOT_URL,
        "HAPROXY_RELEASE_ROOT_URL",
    )
    _validate_haproxy_tuple(values, "HAPROXY")
    _validate_haproxy_tuple(values, "HAPROXY_HTX")


def _validate_crs(values: dict[str, str]) -> None:
    if values["CRS_APPROVED_REPO_URL"] != OFFICIAL_CRS_REPOSITORY:
        raise SyncError("unsupported CRS repository")
    if not HEX40.fullmatch(values["CRS_APPROVED_COMMIT"]):
        raise SyncError("CRS_APPROVED_COMMIT is not a full commit SHA")
    if not re.fullmatch(r"v(?a:\d+)\.(?a:\d+)\.(?a:\d+)", values["CRS_RELEASE_TAG"]):
        raise SyncError("CRS_RELEASE_TAG must be a release tag")


def _require_one(matches: list[re.Match[str]], name: str, path: Path) -> re.Match[str]:
    if len(matches) != 1:
        raise SyncError(f"registered target {path} must contain exactly one {name} assignment")
    return matches[0]


def _python_assignment(text: str, name: str, value: str, path: Path) -> str:
    pattern = re.compile(
        rf"(?ms)^(?P<prefix>\s*{re.escape(name)}\s*=\s*)(?P<value>\(\s*\"(?:[^\"\\]|\\.)*\"\s*\)|\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*'|[A-Za-z_][A-Za-z0-9_]*)\s*(?:#.*)?$"
    )
    match = _require_one(list(pattern.finditer(text)), name, path)
    return text[: match.start()] + f'{match.group("prefix")}{json.dumps(value)}' + text[match.end() :]


def _shell_assignment(text: str, name: str, value: str, path: Path) -> str:
    pattern = re.compile(rf"(?m)^(?P<prefix>\s*{re.escape(name)}\s*=).*$")
    match = _require_one(list(pattern.finditer(text)), name, path)
    return text[: match.start()] + f'{match.group("prefix")}{value}' + text[match.end() :]


def _yaml_assignment(text: str, name: str, value: str, path: Path) -> str:
    pattern = re.compile(
        rf"(?m)^(?P<prefix>[ \t]*{re.escape(name)}\s*:\s*)(?P<current>[^\r\n#]*)(?P<suffix>\s*(?:#.*)?)$"
    )
    match = _require_one(list(pattern.finditer(text)), name, path)
    if not match.group("current").strip():
        raise SyncError(f"registered target {path} has an empty YAML value for {name}")
    return text[: match.start()] + f'{match.group("prefix")}{value}{match.group("suffix")}' + text[match.end() :]


def _lighttpd_contract(text: str, fields: tuple[tuple[str, str], ...], values: dict[str, str], path: Path) -> str:
    expected_keys = {
        "LIGHTTPD_SERIES",
        "LIGHTTPD_VERSION",
        "LIGHTTPD_SOURCE_URL",
        "LIGHTTPD_DOWNLOAD_URL",
        "LIGHTTPD_SHA256",
        "LIGHTTPD_PATCH_FILENAME",
    }
    seen: dict[str, str] = {}
    for line in text.splitlines():
        assignment = _assignment(line)
        if assignment is None:
            continue
        key, rhs = assignment
        if key not in expected_keys:
            continue
        if key in seen:
            raise SyncError(f"duplicate Lighttpd contract assignment: {key}")
        seen[key] = _literal(rhs, key)
    series = seen.get("LIGHTTPD_SERIES", "")
    version = seen.get("LIGHTTPD_VERSION", "")
    expected_source = f"{OFFICIAL_LIGHTTPD_RELEASE_ROOT_URL}/releases-{series}.x/"
    if (
        set(seen) != expected_keys
        or not _series(series)
        or not _semantic_version(version)
        or _major_minor(version) != series
        or seen["LIGHTTPD_SOURCE_URL"] != expected_source
        or seen["LIGHTTPD_DOWNLOAD_URL"] != f"{expected_source}lighttpd-{version}.tar.xz"
        or not HEX64.fullmatch(seen["LIGHTTPD_SHA256"])
        or not SAFE_PATCH.fullmatch(seen["LIGHTTPD_PATCH_FILENAME"])
    ):
        raise SyncError(f"invalid Lighttpd contract: {path}")
    rendered = text
    for target_name, source_name in fields:
        rendered = _shell_assignment(rendered, target_name, values[source_name], path)
    return rendered


def _haproxy_contract(text: str, fields: tuple[tuple[str, str], ...], values: dict[str, str], path: Path) -> str:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise SyncError(f"invalid HAProxy contract JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise SyncError(f"invalid HAProxy contract JSON object: {path}")
    if (
        payload.get("schema_version") != 1
        or payload.get("component") != "haproxy-htx-overlay"
        or payload.get("source_version_file") != "VERSION"
        or not isinstance(payload.get("version"), str)
        or not _semantic_version(payload["version"])
        or not isinstance(payload.get("source_url"), str)
        or not isinstance(payload.get("sha256"), str)
        or not isinstance(payload.get("makefile_patch"), str)
        or not SAFE_PATCH.fullmatch(payload["makefile_patch"])
    ):
        raise SyncError(f"invalid HAProxy contract fields: {path}")
    series = ".".join(payload["version"].split(".")[:2])
    if payload["source_url"] != f"https://www.haproxy.org/download/{series}/src/haproxy-{payload['version']}.tar.gz":
        raise SyncError(f"invalid HAProxy contract source URL: {path}")
    if not HEX64.fullmatch(payload["sha256"]):
        raise SyncError(f"invalid HAProxy contract SHA-256: {path}")
    for target_name, source_name in fields:
        payload[target_name] = values[source_name]
    return json.dumps(payload, indent=2) + "\n"


def _lighttpd_source_map(text: str, fields: tuple[tuple[str, str], ...], values: dict[str, str], path: Path) -> str:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise SyncError(f"invalid Lighttpd source map JSON: {path}") from exc
    if not isinstance(payload, dict) or payload.get("connector") != "lighttpd":
        raise SyncError(f"invalid Lighttpd source map: {path}")
    upstream = payload.get("upstream")
    if not isinstance(upstream, dict) or upstream.get("selected") is not True:
        raise SyncError(f"invalid Lighttpd source map upstream data: {path}")
    required = ("repository", "series", "version", "download_url")
    if any(not isinstance(upstream.get(key), str) for key in required):
        raise SyncError(f"invalid Lighttpd source map upstream fields: {path}")
    series = upstream["series"]
    version = upstream["version"]
    expected_source = f"{OFFICIAL_LIGHTTPD_RELEASE_ROOT_URL}/releases-{series}.x/"
    if (
        not _series(series)
        or not _semantic_version(version)
        or _major_minor(version) != series
        or upstream["repository"] != expected_source
        or upstream["download_url"] != f"{expected_source}lighttpd-{version}.tar.xz"
    ):
        raise SyncError(f"invalid Lighttpd source map upstream tuple: {path}")
    for target_name, source_name in fields:
        upstream[target_name] = values[source_name]
    return json.dumps(payload, indent=2) + "\n"


def _render_targets(root: Path, values: dict[str, str]) -> list[RenderedTarget]:
    derived = {
        "ENVOY_IMAGE": f"envoyproxy/envoy:v{values['ENVOY_VERSION']}",
    }
    rendered: list[RenderedTarget] = []

    def source_value(name: str) -> str:
        if name in derived:
            return derived[name]
        return values[name]

    for spec in TARGET_REGISTRY:
        path = _target_path(root, spec.relative_path)
        original, mode = _read_regular(
            path,
            f"registered target {spec.relative_path}",
            allowed_root=root,
        )
        try:
            text = original.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise SyncError(f"registered target is not UTF-8 text: {path}") from exc
        replacement = _render_target(spec, text, values, path, source_value)
        rendered.append(RenderedTarget(path, original, replacement.encode("utf-8"), mode))
    return rendered


def _render_target(
    spec: TargetSpec,
    text: str,
    values: dict[str, str],
    path: Path,
    source_value: Callable[[str], str],
) -> str:
    if spec.syntax in {"shell", "yaml", "python"}:
        return _render_assignments(spec, text, path, source_value)
    renderers = {
        "lighttpd-contract": _lighttpd_contract,
        "lighttpd-source-map": _lighttpd_source_map,
        "haproxy-contract": _haproxy_contract,
    }
    renderer = renderers.get(spec.syntax)
    if renderer is None:
        raise SyncError(f"unsupported registered target syntax: {spec.syntax}")
    return renderer(text, spec.fields, values, path)


def _render_assignments(spec: TargetSpec, text: str, path: Path, source_value: Callable[[str], str]) -> str:
    replacement = text
    assignment_renderers = {
        "shell": _shell_assignment,
        "yaml": _yaml_assignment,
        "python": _python_assignment,
    }
    renderer = assignment_renderers[spec.syntax]
    for target_name, source_name in spec.fields:
        replacement = renderer(replacement, target_name, source_value(source_name), path)
    return replacement


def _fsync_directory(path: Path) -> None:
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _replace_file(path: Path, contents: bytes, mode: int) -> None:
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb", closefd=True) as handle:
            descriptor = -1
            os.fchmod(handle.fileno(), mode)
            handle.write(contents)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        _fsync_directory(path.parent)
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        if os.path.exists(temporary):
            os.unlink(temporary)


def synchronize(root: Path, framework_common: Path, sync: bool) -> list[str]:
    repository_root = _require_directory(root, "repository root")
    values = parse_common(framework_common)
    rendered = _render_targets(repository_root, values)
    changed = [str(item.path.relative_to(repository_root)) for item in rendered if item.replacement != item.original]
    if sync and changed:
        _commit_rendered(rendered)
    return changed


def _commit_rendered(rendered: list[RenderedTarget]) -> None:
    committed: list[RenderedTarget] = []
    try:
        for item in rendered:
            if item.replacement == item.original:
                continue
            _replace_file(item.path, item.replacement, item.mode)
            committed.append(item)
    except OSError as exc:
        rollback_errors: list[str] = []
        for item in reversed(committed):
            try:
                _replace_file(item.path, item.original, item.mode)
            except OSError as rollback_exc:
                rollback_errors.append(str(rollback_exc))
        detail = "; rollback failed: " + "; ".join(rollback_errors) if rollback_errors else ""
        raise SyncError(f"synchronization failed; completed changes were rolled back: {exc}{detail}") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--validate", action="store_true", help="parse inputs and targets without requiring an already-synced tree")
    mode.add_argument("--check", action="store_true", help="fail when a fixed target would change")
    mode.add_argument("--sync", action="store_true", help="write the fixed target registry atomically")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).parents[2])
    parser.add_argument("--framework-common", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        changed = synchronize(_absolute(args.repo_root), _absolute(args.framework_common), args.sync)
    except (OSError, SyncError) as exc:
        print(f"sync-framework-component-versions: error: {exc}")
        return 2
    if args.sync:
        selected_mode = "sync"
    elif args.check:
        selected_mode = "check"
    else:
        selected_mode = "validate"
    print(json.dumps({"changed": changed, "mode": selected_mode}, sort_keys=True))
    return 1 if args.check and changed else 0


if __name__ == "__main__":
    raise SystemExit(main())
