#!/usr/bin/env python3
"""Synchronize fixed Parent component pins from approved Framework data.

``common.sh`` is never sourced or executed. The protected update workflow
proves the Framework Git object, extracts its ``ci/lib/common.sh`` as a data
file, and this tool accepts only the bounded literal contract below. It can
write only the explicit Parent target registry.
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


MAX_COMMON_BYTES = 256 * 1024
HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")
HEX40 = re.compile(r"^[0-9a-fA-F]{40}$")
SAFE_PATCH = re.compile(r"^[A-Za-z0-9._-]+\.patch$")
LIGHTTPD_SOURCE_URL = "https://download.lighttpd.net/lighttpd/releases-1.4.x/"

REQUIRED = (
    "ENVOY_VERSION",
    "LIGHTTPD_VERSION",
    "LIGHTTPD_SOURCE_URL",
    "LIGHTTPD_DOWNLOAD_URL",
    "LIGHTTPD_SHA256",
    "HAPROXY_VERSION",
    "HAPROXY_SOURCE_URL",
    "HAPROXY_SHA256",
    "NGINX_QUIC_TLS_LIBRARY",
    "NGINX_QUIC_TLS_VERSION",
    "NGINX_QUIC_TLS_SOURCE_URL",
    "NGINX_QUIC_TLS_SOURCE_SHA256",
    "NGINX_SOURCE_MODE",
    "NGINX_SOURCE_REPO_URL",
    "NGINX_RELEASE_TAG",
    "NGINX_SOURCE_GIT_REF",
    "NGINX_RELEASE_ASSET_NAME",
    "NGINX_SHA256",
    "CRS_APPROVED_REPO_URL",
    "CRS_APPROVED_COMMIT",
    "CRS_RELEASE_TAG",
)


class SyncError(ValueError):
    """The approved Framework data or a fixed Parent target is unsafe."""


def _ascii_digits(value: str) -> bool:
    return bool(value) and all("0" <= character <= "9" for character in value)


def _semantic_version(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parts = value.split(".")
    return len(parts) == 3 and all(_ascii_digits(part) for part in parts)


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
        (
            ("DEFAULT_NGINX_QUIC_TLS_VERSION", "NGINX_QUIC_TLS_VERSION"),
            ("DEFAULT_NGINX_QUIC_TLS_SOURCE_URL", "NGINX_QUIC_TLS_SOURCE_URL"),
            ("DEFAULT_NGINX_QUIC_TLS_SOURCE_SHA256", "NGINX_QUIC_TLS_SOURCE_SHA256"),
            ("NGINX_PINNED_SOURCE_REPOSITORY", "NGINX_SOURCE_REPO_URL"),
            ("NGINX_PINNED_RELEASE_TAG", "NGINX_RELEASE_TAG"),
            ("NGINX_PINNED_SOURCE_REF", "NGINX_SOURCE_GIT_REF"),
            ("NGINX_PINNED_RELEASE_ASSET_NAME", "NGINX_RELEASE_ASSET_NAME"),
            ("NGINX_PINNED_RELEASE_ASSET_SHA256", "NGINX_SHA256"),
            ("NGINX_PINNED_VERSION_READBACK", "NGINX_VERSION_READBACK"),
            ("DEFAULT_HAPROXY_VERSION", "HAPROXY_VERSION"),
        ),
        "python",
    ),
    TargetSpec(
        "ci/checks/evidence/check-runtime-producer-readiness.py",
        (
            ("CANONICAL_NGINX_SOURCE_REPOSITORY", "NGINX_SOURCE_REPO_URL"),
            ("CANONICAL_NGINX_SOURCE_MODE", "NGINX_SOURCE_MODE"),
            ("CANONICAL_NGINX_RELEASE_TAG", "NGINX_RELEASE_TAG"),
            ("CANONICAL_NGINX_SOURCE_REF", "NGINX_SOURCE_GIT_REF"),
            ("CANONICAL_NGINX_RELEASE_ASSET_NAME", "NGINX_RELEASE_ASSET_NAME"),
            ("CANONICAL_NGINX_ARCHIVE_SHA256", "NGINX_SHA256"),
            ("CANONICAL_NGINX_VERSION_READBACK", "NGINX_VERSION_READBACK"),
        ),
        "python",
    ),
    TargetSpec(
        "ci/runtime/broker/nginx_root_broker.py",
        (
            ("CRS_APPROVED_REPOSITORY", "CRS_APPROVED_REPO_URL"),
            ("CRS_RELEASE_TAG", "CRS_RELEASE_TAG"),
            ("CRS_APPROVED_COMMIT", "CRS_APPROVED_COMMIT"),
            ("NGINX_PINNED_VERSION", "NGINX_VERSION"),
            ("NGINX_PINNED_RELEASE_TAG", "NGINX_RELEASE_TAG"),
        ),
        "python",
    ),
    TargetSpec(
        "ci/runtime/broker/protected_nginx_broker_caller.py",
        (
            ("CRS_REPOSITORY", "CRS_APPROVED_REPO_URL"),
            ("CRS_RELEASE_TAG", "CRS_RELEASE_TAG"),
            ("CRS_COMMIT", "CRS_APPROVED_COMMIT"),
            ("NGINX_PINNED_VERSION", "NGINX_VERSION"),
        ),
        "python",
    ),
    TargetSpec(
        "connectors/lighttpd/lighttpd-version.contract",
        (
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
            ("version", "LIGHTTPD_VERSION"),
            ("download_url", "LIGHTTPD_DOWNLOAD_URL"),
        ),
        "lighttpd-source-map",
    ),
    TargetSpec(
        "connectors/haproxy/htx-overlay/version-contract.json",
        (
            ("version", "HAPROXY_VERSION"),
            ("source_url", "HAPROXY_SOURCE_URL"),
            ("sha256", "HAPROXY_SHA256"),
        ),
        "haproxy-contract",
    ),
    TargetSpec(
        ".github/workflows/test-full-smoke-sequential.yml",
        (
            ("NGINX_SOURCE_MODE", "NGINX_SOURCE_MODE"),
            ("NGINX_SOURCE_REPO_URL", "NGINX_SOURCE_REPO_URL"),
            ("NGINX_RELEASE_TAG", "NGINX_RELEASE_TAG"),
            ("NGINX_SOURCE_GIT_REF", "NGINX_SOURCE_GIT_REF"),
            ("NGINX_RELEASE_ASSET_NAME", "NGINX_RELEASE_ASSET_NAME"),
            ("NGINX_SHA256", "NGINX_SHA256"),
        ),
        "yaml",
    ),
    TargetSpec(
        ".github/workflows/nginx-root-broker.yml",
        (
            ("NGINX_SOURCE_MODE", "NGINX_SOURCE_MODE"),
            ("NGINX_SOURCE_REPO_URL", "NGINX_SOURCE_REPO_URL"),
            ("NGINX_RELEASE_TAG", "NGINX_RELEASE_TAG"),
            ("NGINX_SOURCE_GIT_REF", "NGINX_SOURCE_GIT_REF"),
            ("NGINX_RELEASE_ASSET_NAME", "NGINX_RELEASE_ASSET_NAME"),
            ("NGINX_SHA256", "NGINX_SHA256"),
        ),
        "yaml",
    ),
)


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
    value = rhs.strip()
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
    value = _unquote(rhs, key)
    if any(token in value for token in ("$(`", "$(", "`", ";", "|", "\\", "\n", "\r")):
        raise SyncError(f"unsafe shell syntax in {key}")
    default = re.fullmatch(r"\$\{" + re.escape(key) + r"(?::?-)([^${}]*)\}", value)
    if default:
        value = default.group(1)
    if "$" in value or not value:
        raise SyncError(f"non-literal assignment in {key}")
    return value


def _resolve_nginx_source_ref(rhs: str, release_tag: str) -> str:
    value = _unquote(rhs, "NGINX_SOURCE_GIT_REF")
    if value == "${NGINX_SOURCE_GIT_REF-$NGINX_RELEASE_TAG}":
        return release_tag
    return _literal(rhs, "NGINX_SOURCE_GIT_REF")


def _resolve_lighttpd_download_url(rhs: str, source_url: str, version: str) -> str:
    value = _unquote(rhs, "LIGHTTPD_DOWNLOAD_URL")
    expected = f"${{LIGHTTPD_DOWNLOAD_URL:-{LIGHTTPD_SOURCE_URL}lighttpd-$LIGHTTPD_VERSION.tar.xz}}"
    if value == expected:
        return f"{source_url}lighttpd-{version}.tar.xz"
    return _literal(rhs, "LIGHTTPD_DOWNLOAD_URL")


def _resolve_haproxy_source_url(rhs: str, version: str) -> str:
    value = _unquote(rhs, "HAPROXY_SOURCE_URL")
    expected = "${HAPROXY_SOURCE_URL:-https://www.haproxy.org/download/3.2/src/haproxy-$HAPROXY_VERSION.tar.gz}"
    if value == expected:
        return f"https://www.haproxy.org/download/{'.'.join(version.split('.')[:2])}/src/haproxy-{version}.tar.gz"
    return _literal(rhs, "HAPROXY_SOURCE_URL")


def _resolve_nginx_source_repository(rhs: str) -> str:
    value = _unquote(rhs, "NGINX_SOURCE_REPO_URL")
    expected = "${NGINX_SOURCE_REPO_URL-${NGINX_GITHUB_REPO-https://github.com/nginx/nginx}}"
    if value == expected:
        return "https://github.com/nginx/nginx"
    return _literal(rhs, "NGINX_SOURCE_REPO_URL")


def _resolve_nginx_quic_tls_url(rhs: str, version: str) -> str:
    value = _unquote(rhs, "NGINX_QUIC_TLS_SOURCE_URL")
    expected = (
        "${NGINX_QUIC_TLS_SOURCE_URL:-https://github.com/openssl/openssl/releases/download/"
        "openssl-$NGINX_QUIC_TLS_VERSION/openssl-$NGINX_QUIC_TLS_VERSION.tar.gz}"
    )
    if value == expected:
        return f"https://github.com/openssl/openssl/releases/download/openssl-{version}/openssl-{version}.tar.gz"
    return _literal(rhs, "NGINX_QUIC_TLS_SOURCE_URL")


def _resolve_nginx_asset_name(rhs: str, release_tag: str) -> str:
    value = _unquote(rhs, "NGINX_RELEASE_ASSET_NAME")
    expected = "${NGINX_RELEASE_ASSET_NAME-nginx-${NGINX_RELEASE_TAG#release-}.tar.gz}"
    if value == expected:
        return f"nginx-{release_tag.removeprefix('release-')}.tar.gz"
    return _literal(rhs, "NGINX_RELEASE_ASSET_NAME")


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
    for line in text.splitlines():
        assignment = _assignment(line)
        if assignment is None:
            continue
        key, rhs = assignment
        if key not in REQUIRED:
            continue
        if key in raw:
            raise SyncError(f"duplicate required assignment: {key}")
        raw[key] = rhs
    missing = [key for key in REQUIRED if key not in raw]
    if missing:
        raise SyncError("missing required Framework assignments: " + ", ".join(missing))

    excluded = {
        "LIGHTTPD_DOWNLOAD_URL",
        "HAPROXY_SOURCE_URL",
        "NGINX_QUIC_TLS_SOURCE_URL",
        "NGINX_SOURCE_REPO_URL",
        "NGINX_SOURCE_GIT_REF",
        "NGINX_RELEASE_ASSET_NAME",
    }
    values = {key: _literal(raw[key], key) for key in REQUIRED if key not in excluded}
    values["LIGHTTPD_DOWNLOAD_URL"] = _resolve_lighttpd_download_url(
        raw["LIGHTTPD_DOWNLOAD_URL"], values["LIGHTTPD_SOURCE_URL"], values["LIGHTTPD_VERSION"]
    )
    values["HAPROXY_SOURCE_URL"] = _resolve_haproxy_source_url(
        raw["HAPROXY_SOURCE_URL"], values["HAPROXY_VERSION"]
    )
    values["NGINX_QUIC_TLS_SOURCE_URL"] = _resolve_nginx_quic_tls_url(
        raw["NGINX_QUIC_TLS_SOURCE_URL"], values["NGINX_QUIC_TLS_VERSION"]
    )
    values["NGINX_SOURCE_REPO_URL"] = _resolve_nginx_source_repository(raw["NGINX_SOURCE_REPO_URL"])
    values["NGINX_SOURCE_GIT_REF"] = _resolve_nginx_source_ref(raw["NGINX_SOURCE_GIT_REF"], values["NGINX_RELEASE_TAG"])
    values["NGINX_RELEASE_ASSET_NAME"] = _resolve_nginx_asset_name(raw["NGINX_RELEASE_ASSET_NAME"], values["NGINX_RELEASE_TAG"])
    _validate(values)
    return values


def _validate(values: dict[str, str]) -> None:
    _validate_versions(values)
    _validate_lighttpd(values)
    _validate_haproxy(values)
    _validate_nginx(values)
    _validate_crs(values)


def _validate_versions(values: dict[str, str]) -> None:
    for key in ("ENVOY_VERSION", "LIGHTTPD_VERSION", "HAPROXY_VERSION", "NGINX_QUIC_TLS_VERSION"):
        if not _semantic_version(values[key]):
            raise SyncError(f"{key} is not a semantic version")


def _validate_lighttpd(values: dict[str, str]) -> None:
    if values["LIGHTTPD_SOURCE_URL"] != LIGHTTPD_SOURCE_URL:
        raise SyncError("unsupported LIGHTTPD_SOURCE_URL")
    expected = f"{LIGHTTPD_SOURCE_URL}lighttpd-{values['LIGHTTPD_VERSION']}.tar.xz"
    if values["LIGHTTPD_DOWNLOAD_URL"] != expected:
        raise SyncError("LIGHTTPD_DOWNLOAD_URL does not match LIGHTTPD_VERSION")
    if not HEX64.fullmatch(values["LIGHTTPD_SHA256"]):
        raise SyncError("LIGHTTPD_SHA256 is not a SHA-256 digest")


def _validate_haproxy(values: dict[str, str]) -> None:
    series = ".".join(values["HAPROXY_VERSION"].split(".")[:2])
    expected = f"https://www.haproxy.org/download/{series}/src/haproxy-{values['HAPROXY_VERSION']}.tar.gz"
    if values["HAPROXY_SOURCE_URL"] != expected:
        raise SyncError("HAPROXY_SOURCE_URL does not match HAPROXY_VERSION")
    if not HEX64.fullmatch(values["HAPROXY_SHA256"]):
        raise SyncError("HAPROXY_SHA256 is not a SHA-256 digest")


def _validate_nginx(values: dict[str, str]) -> None:
    if values["NGINX_QUIC_TLS_LIBRARY"] != "openssl":
        raise SyncError("unsupported NGINX_QUIC_TLS_LIBRARY")
    tls = values["NGINX_QUIC_TLS_VERSION"]
    expected_tls = f"https://github.com/openssl/openssl/releases/download/openssl-{tls}/openssl-{tls}.tar.gz"
    if values["NGINX_QUIC_TLS_SOURCE_URL"] != expected_tls:
        raise SyncError("NGINX_QUIC_TLS_SOURCE_URL does not match its version")
    if not HEX64.fullmatch(values["NGINX_QUIC_TLS_SOURCE_SHA256"]):
        raise SyncError("NGINX_QUIC_TLS_SOURCE_SHA256 is not a SHA-256 digest")
    if values["NGINX_SOURCE_MODE"] != "github-release" or values["NGINX_SOURCE_REPO_URL"] != "https://github.com/nginx/nginx":
        raise SyncError("unsupported NGINX source contract")
    tag = values["NGINX_RELEASE_TAG"]
    if not re.fullmatch(r"release-\d+\.\d+\.\d+", tag):
        raise SyncError("NGINX_RELEASE_TAG must be a release-x.y.z tag")
    if values["NGINX_SOURCE_GIT_REF"] != tag:
        raise SyncError("NGINX_SOURCE_GIT_REF must match NGINX_RELEASE_TAG")
    if values["NGINX_RELEASE_ASSET_NAME"] != f"nginx-{tag.removeprefix('release-')}.tar.gz":
        raise SyncError("NGINX_RELEASE_ASSET_NAME does not match NGINX_RELEASE_TAG")
    if not HEX64.fullmatch(values["NGINX_SHA256"]):
        raise SyncError("NGINX_SHA256 is not a SHA-256 digest")


def _validate_crs(values: dict[str, str]) -> None:
    if values["CRS_APPROVED_REPO_URL"] != "https://github.com/coreruleset/coreruleset.git":
        raise SyncError("unsupported CRS repository")
    if not HEX40.fullmatch(values["CRS_APPROVED_COMMIT"]):
        raise SyncError("CRS_APPROVED_COMMIT is not a full commit SHA")
    if not re.fullmatch(r"v\d+\.\d+\.\d+", values["CRS_RELEASE_TAG"]):
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
    if (
        set(seen) != expected_keys
        or not _semantic_version(seen["LIGHTTPD_VERSION"])
        or seen["LIGHTTPD_SOURCE_URL"] != LIGHTTPD_SOURCE_URL
        or seen["LIGHTTPD_DOWNLOAD_URL"] != f"{seen['LIGHTTPD_SOURCE_URL']}lighttpd-{seen['LIGHTTPD_VERSION']}.tar.xz"
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
    required = ("repository", "version", "download_url")
    if any(not isinstance(upstream.get(key), str) for key in required):
        raise SyncError(f"invalid Lighttpd source map upstream fields: {path}")
    version = upstream["version"]
    if (
        not _semantic_version(version)
        or upstream["repository"] != LIGHTTPD_SOURCE_URL
        or upstream["download_url"] != f"{upstream['repository']}lighttpd-{version}.tar.xz"
    ):
        raise SyncError(f"invalid Lighttpd source map upstream tuple: {path}")
    for target_name, source_name in fields:
        upstream[target_name] = values[source_name]
    return json.dumps(payload, indent=2) + "\n"


def _render_targets(root: Path, values: dict[str, str]) -> list[RenderedTarget]:
    derived = {
        "ENVOY_IMAGE": f"envoyproxy/envoy:v{values['ENVOY_VERSION']}",
        "NGINX_VERSION": values["NGINX_RELEASE_TAG"].removeprefix("release-"),
        "NGINX_VERSION_READBACK": f"nginx/{values['NGINX_RELEASE_TAG'].removeprefix('release-')}",
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
