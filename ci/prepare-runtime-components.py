#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from generated_report_utils import GENERATED_ROOT, build_metadata, generated_json_text, generated_markdown_text, report_path_from_root
from runtime_path_utils import is_system_write_path


COMMON_SH_CONFIG_VARS = (
    "GO_FTW_SOURCE_URL",
    "GO_FTW_PROMPT_EXPECTED_LATEST",
    "GO_FTW_GIT_REF",
    "GO_FTW_BIN",
    "ALBEDO_SOURCE_URL",
    "ALBEDO_PROMPT_EXPECTED_LATEST",
    "ALBEDO_GIT_REF",
    "ALBEDO_BIN",
    "EXPAT_SOURCE_URL",
    "EXPAT_GIT_REF",
    "EXPAT_GIT_URL",
    "EXPAT_PROMPT_EXPECTED_LATEST",
)

GITHUB_REPO_URL_KEYS = (
    "CRS_REPO_URL",
    "MODSECURITY_REPO_URL",
    "MODSECURITY_V3_GIT_URL",
    "MODSECURITY_APACHE_REPO_URL",
    "MODSECURITY_APACHE_GIT_URL",
    "MODSECURITY_NGINX_REPO_URL",
    "MODSECURITY_NGINX_GIT_URL",
    "NGINX_SOURCE_REPO_URL",
    "NGINX_GITHUB_REPO",
    "GO_FTW_SOURCE_URL",
    "ALBEDO_SOURCE_URL",
    "EXPAT_SOURCE_URL",
    "EXPAT_GIT_URL",
)

HTTPS_URL_KEYS = (
    "HAPROXY_SOURCE_URL",
    "HAPROXY_SHA256_URL",
    "HTTPD_SOURCE_URL",
    "HTTPD_SHA256_URL",
    "APR_SOURCE_URL",
    "APR_SHA256_URL",
    "APR_UTIL_SOURCE_URL",
    "APR_UTIL_SHA256_URL",
    "PCRE2_SOURCE_URL",
    "PCRE2_SHA256_URL",
)

PATH_POLICY_ENV = dict(os.environ)


# Bump this whenever the on-disk cache contract or the identity inputs change.
# A cache entry is only reusable when its manifest was produced by this schema.
CACHE_SCHEMA_VERSION = 2
CACHE_ROOT_MARKER = ".msconnector-runtime-cache-root.json"
CACHE_ENTRY_MARKER_DIRECTORY = ".msconnector-runtime-cache-entries"
CACHE_MANIFEST_STATUS_COMPLETE = "complete"
RUNTIME_ENV_SNAPSHOT_SCHEMA_VERSION = 1

# Apache httpd generates several installed helper/configuration files with the
# configured absolute prefix.  Connector cache entries are built below an
# atomic staging directory and then renamed, so those text files must be
# rebased before publication.  Keep this an explicit allowlist: native
# executables are deliberately never rewritten after they are linked.
APACHE_INSTALL_TEXT_PATHS = (
    "bin/apachectl",
    "bin/apachectl-mrts",
    "bin/apr-1-config",
    "bin/apu-1-config",
    "bin/apxs",
    "bin/envvars",
    "bin/envvars-std",
    "build/apr_rules.mk",
    "build/config.nice",
    "build/config_vars.mk",
    "build/config_vars.sh",
    "build/instdso.sh",
    "build/libtool",
    "include/ap_config_auto.h",
    "include/ap_config_layout.h",
    "lib/libapr-1.la",
    "lib/libaprutil-1.la",
    "lib/pkgconfig/apr-1.pc",
    "lib/pkgconfig/apr-util-1.pc",
)


def cache_root_marker_path(cache_root: Path) -> Path:
    return cache_root / CACHE_ROOT_MARKER


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def is_system_path(path: Path) -> bool:
    return is_system_write_path(path, PATH_POLICY_ENV)


def sh_quote(value: str) -> str:
    return "'" + value.replace("'", "'\"'\"'") + "'"


def run(cmd: list[str], cwd: Path | None = None, check: bool = False) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and proc.returncode != 0:
        raise RuntimeError((proc.stdout + proc.stderr).strip() or f"command failed: {' '.join(cmd)}")
    return proc


def run_env(
    cmd: list[str],
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    check: bool = False,
) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(cmd, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and proc.returncode != 0:
        raise RuntimeError((proc.stdout + proc.stderr).strip() or f"command failed: {' '.join(cmd)}")
    return proc


def load_framework_environment(connector_root: Path, framework_root: Path, base_env: dict[str, str]) -> tuple[dict[str, str], str]:
    common_sh = framework_root / "ci/common.sh"
    if not common_sh.is_file():
        return dict(base_env), f"missing:{common_sh}"
    env = dict(base_env)
    env["CONNECTOR_ROOT"] = str(connector_root)
    env["FRAMEWORK_ROOT"] = str(framework_root)
    try:
        proc = subprocess.run(
            ["bash", "-lc", 'set -a; . "$FRAMEWORK_ROOT/ci/common.sh"; env -0'],
            cwd=str(connector_root),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=False,
            timeout=60,
        )
    except FileNotFoundError as exc:
        return dict(base_env), f"failed:{exc}"
    except subprocess.TimeoutExpired as exc:
        output = (exc.stdout or b"").decode("utf-8", errors="replace").strip()
        return dict(base_env), f"failed:timeout loading common.sh {output}"
    if proc.returncode != 0:
        stderr = proc.stderr.decode("utf-8", errors="replace").strip()
        return dict(base_env), f"failed:{stderr or proc.returncode}"
    loaded: dict[str, str] = {}
    for chunk in proc.stdout.split(b"\0"):
        if not chunk or b"=" not in chunk:
            continue
        key, value = chunk.split(b"=", 1)
        loaded[key.decode("utf-8", errors="replace")] = value.decode("utf-8", errors="replace")
    return loaded, "loaded"


def require_env_value(env: dict[str, str], key: str) -> str:
    value = env.get(key, "").strip()
    if not value:
        raise RuntimeError(f"missing required runtime component config: {key} from framework common.sh")
    return value


def require_https_url(url: str, label: str) -> str:
    raw = url.strip()
    if not raw.startswith("https://"):
        raise RuntimeError(f"{label} must use https:// only: {url}")
    return raw


def require_https_github_repo_url(url: str, label: str) -> str:
    repo = github_repo_path(url)
    return f"https://github.com/{repo}"


def validate_https_url_config(env: dict[str, str]) -> None:
    for key in GITHUB_REPO_URL_KEYS:
        value = env.get(key, "").strip()
        if value:
            require_https_github_repo_url(value, key)
    for key in HTTPS_URL_KEYS:
        value = env.get(key, "").strip()
        if value:
            require_https_url(value, key)


def network_blocker_reason(exc: Exception, *, optional: bool = False) -> str:
    prefix = "blocked_network_optional" if optional else "blocked_network"
    return f"{prefix}:{exc}"


def retry_count() -> int:
    try:
        return max(1, int(os.environ.get("RUNTIME_COMPONENT_NETWORK_RETRIES", "3")))
    except ValueError:
        return 3


def retry_delay_seconds() -> float:
    try:
        return max(0.0, float(os.environ.get("RUNTIME_COMPONENT_NETWORK_RETRY_DELAY_SECONDS", "2")))
    except ValueError:
        return 2.0


def urlopen_bytes(url: str, *, timeout: int = 60) -> bytes:
    last_exc: Exception | None = None
    for attempt in range(1, retry_count() + 1):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as response:
                return response.read()
        except Exception as exc:
            last_exc = exc
            if attempt < retry_count():
                time.sleep(retry_delay_seconds())
    raise RuntimeError(last_exc or f"network request failed: {url}")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def tree_manifest(path: Path) -> dict[str, Any]:
    file_count = 0
    total_size = 0
    digest = hashlib.sha256()
    if not path.exists():
        return {"exists": False, "file_count": 0, "total_size": 0, "sha256_manifest": ""}
    for item in sorted(path.rglob("*")):
        if not item.is_file():
            continue
        try:
            rel = item.relative_to(path).as_posix()
            size = item.stat().st_size
        except OSError:
            continue
        file_count += 1
        total_size += size
        digest.update(rel.encode("utf-8", "surrogateescape"))
        digest.update(b"\0")
        digest.update(str(size).encode("ascii"))
        digest.update(b"\0")
    return {
        "exists": True,
        "file_count": file_count,
        "total_size": total_size,
        "sha256_manifest": digest.hexdigest(),
    }


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def atomic_write_text(path: Path, text: str) -> None:
    """Publish a small cache-control file without exposing partial JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.tmp-", dir=str(path.parent))
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except Exception:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
        raise


def runtime_env_shell_text(values: dict[str, str]) -> str:
    """Render the deliberately small, sourceable runtime environment format."""
    return "\n".join(
        f"export {key}={sh_quote(value)}" for key, value in sorted(values.items())
    ) + "\n"


def snapshot_path_within_output_root(snapshot_path: Path, output_root: Path) -> Path:
    """Resolve and validate a caller-selected invocation-local snapshot path.

    A shared Cache-v2 runtime-env file remains a compatibility artifact, but
    it cannot be used as a later runner input: concurrent target preparation
    may legitimately republish it.  Snapshot files therefore belong to the
    invocation's report root, never to the shared cache.
    """
    if not snapshot_path.is_absolute():
        raise RuntimeError(f"runtime_env_snapshot_must_be_absolute:{snapshot_path}")
    resolved_root = output_root.resolve()
    resolved_snapshot = snapshot_path.resolve()
    try:
        resolved_snapshot.relative_to(resolved_root)
    except ValueError as exc:
        raise RuntimeError(
            "runtime_env_snapshot_outside_output_root:"
            f"snapshot={resolved_snapshot} output_root={resolved_root}"
        ) from exc
    if resolved_snapshot == resolved_root:
        raise RuntimeError("runtime_env_snapshot_must_be_a_file")
    return resolved_snapshot


def allocate_runtime_env_snapshot(output_root: Path) -> Path:
    """Reserve one unique local destination for a direct Python invocation."""
    output_root.mkdir(parents=True, exist_ok=True)
    descriptor, name = tempfile.mkstemp(
        prefix="runtime-env-snapshot.", suffix=".sh", dir=str(output_root)
    )
    os.close(descriptor)
    return Path(name)


def write_runtime_env_snapshot(
    runtime_env: dict[str, str],
    *,
    snapshot_path: Path,
    output_root: Path,
    target_connector: str,
    cache_root: Path,
) -> Path:
    """Atomically publish an invocation-local environment snapshot.

    The additional metadata intentionally lives only in this snapshot.  The
    shared ``runtime-env.sh`` keeps its long-standing export contract for
    reports and legacy consumers, while central runners can verify that the
    local file belongs to their selected target and Cache-v2 root.
    """
    destination = snapshot_path_within_output_root(snapshot_path, output_root)
    values = dict(runtime_env)
    values.update(
        {
            "RUNTIME_COMPONENT_ENV_SNAPSHOT": str(destination),
            "RUNTIME_COMPONENT_ENV_SNAPSHOT_CACHE": str(cache_root),
            "RUNTIME_COMPONENT_ENV_SNAPSHOT_SCHEMA": str(
                RUNTIME_ENV_SNAPSHOT_SCHEMA_VERSION
            ),
            "RUNTIME_COMPONENT_ENV_SNAPSHOT_TARGET": target_connector,
        }
    )
    atomic_write_text(destination, runtime_env_shell_text(values))
    return destination


def atomic_write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.tmp-", dir=str(path.parent))
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except Exception:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
        raise


def write_json(path: Path, data: Any) -> None:
    atomic_write_text(path, json.dumps(data, indent=2, sort_keys=True) + "\n")


def stable_hash(data: Any) -> str:
    encoded = json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def target_architecture(env: dict[str, str]) -> str:
    return (
        env.get("TARGET_ARCHITECTURE", "").strip()
        or env.get("TARGETARCH", "").strip()
        or env.get("ARCH", "").strip()
        or platform.machine().strip()
        or "unknown"
    )


def patchset_identity(roots: list[Path]) -> dict[str, Any]:
    """Hash patch names, deterministic application order, and full contents."""
    digest = hashlib.sha256()
    files: list[str] = []
    for root_index, root in enumerate(roots):
        digest.update(f"root:{root_index}:{root.name}".encode("utf-8", "surrogateescape"))
        digest.update(b"\0")
        if not root.is_dir():
            digest.update(b"missing\0")
            continue
        ordered = [item for item in sorted(root.rglob("*")) if item.is_file() and ".git" not in item.parts]
        for order, item in enumerate(ordered):
            relative = item.relative_to(root).as_posix()
            files.append(relative)
            digest.update(f"{order}:{relative}".encode("utf-8", "surrogateescape"))
            digest.update(b"\0")
            digest.update(hashlib.sha256(item.read_bytes()).digest())
            digest.update(b"\0")
    return {"sha256": digest.hexdigest(), "files": files}


def component_patchset_roots(connector_root: Path | None, component: str) -> list[Path]:
    if connector_root is None:
        return []
    roots = [
        connector_root / "connectors" / component / "patches",
        connector_root / "patches" / component,
        connector_root / "common" / "patches" / component,
    ]
    # The HAProxy 3.2.21 HTX overlay is copied into a disposable upstream
    # worktree during its optional source-linked build. Treat its source,
    # build script, and pinned Makefile overlay exactly like a patchset so a
    # change cannot reuse a binary built from older overlay inputs.
    if component == "haproxy":
        roots.append(connector_root / "connectors" / "haproxy" / "htx-overlay")
    return roots


def canonical_cache_identity(
    component: str,
    *,
    env: dict[str, str],
    upstream_url: str = "",
    upstream_version: str = "",
    upstream_commit: str = "",
    source_sha256: str = "",
    patchset_sha256: str = "",
    build_profile: str = "",
    configuration_flags: Any = None,
    toolchain: dict[str, Any] | None = None,
    extra_inputs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """The complete, stable cache contract used for every reusable build entry."""
    toolchain_payload = toolchain if toolchain is not None else toolchain_identity(env)
    identity: dict[str, Any] = {
        "cache_schema_version": CACHE_SCHEMA_VERSION,
        "component": component,
        "upstream_url": upstream_url,
        "upstream_version": upstream_version,
        "upstream_commit": upstream_commit,
        "source_sha256": source_sha256,
        "patchset_sha256": patchset_sha256,
        "target_architecture": target_architecture(env),
        "compiler_id": str(toolchain_payload.get("cc", "")),
        "compiler_version": str(toolchain_payload.get("cc_version", "")),
        "toolchain": toolchain_payload,
        "build_profile": build_profile or env.get("RUNTIME_BUILD_PROFILE", "") or env.get("BUILD_PROFILE", ""),
        "configuration_flags": configuration_flags if configuration_flags is not None else {},
    }
    if extra_inputs:
        identity["extra_inputs"] = extra_inputs
    identity["cache_key"] = stable_hash(identity)
    return identity


def cache_manifest_complete(path: Path, identity: dict[str, Any]) -> bool:
    manifest = read_json(path)
    return (
        manifest.get("status") == CACHE_MANIFEST_STATUS_COMPLETE
        and manifest.get("cache_schema_version") == CACHE_SCHEMA_VERSION
        and manifest.get("cache_key") == identity.get("cache_key")
        and manifest.get("cache_identity") == identity
    )


def write_cache_manifest(path: Path, record: dict[str, Any]) -> None:
    """Persist an entry manifest; only successful artifacts receive complete status."""
    manifest = dict(record)
    record_status = str(record.get("status", "unknown"))
    if record_status in {"built", "reused", "present"}:
        manifest["build_status"] = record_status
        manifest["status"] = CACHE_MANIFEST_STATUS_COMPLETE
    else:
        manifest["status"] = record_status
    manifest.setdefault("cache_schema_version", CACHE_SCHEMA_VERSION)
    identity = manifest.get("cache_identity")
    if isinstance(identity, dict):
        manifest.setdefault("cache_key", identity.get("cache_key", ""))
    write_json(path, manifest)


def is_within(path: Path, owner: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(owner.resolve(strict=False))
        return True
    except ValueError:
        return False


def _resolved_absolute(path: Path, label: str) -> Path:
    raw = Path(path)
    if not raw.is_absolute():
        raise RuntimeError(f"unsafe_{label}_path_not_absolute: {path}")
    return raw.resolve(strict=False)


def paths_overlap(first: Path, second: Path) -> bool:
    first_resolved = first.resolve(strict=False)
    second_resolved = second.resolve(strict=False)
    return first_resolved == second_resolved or is_within(first_resolved, second_resolved) or is_within(second_resolved, first_resolved)


def default_protected_cache_paths() -> tuple[Path, ...]:
    connector_root = Path(__file__).resolve().parents[1]
    return (connector_root, connector_root / "modules" / "ModSecurity-test-Framework")


def cache_root_marker_valid(cache_root: Path) -> bool:
    resolved_root = cache_root.resolve(strict=False)
    marker = read_json(cache_root_marker_path(resolved_root))
    return (
        marker.get("kind") == "msconnector-runtime-cache-root"
        and marker.get("schema_version") == CACHE_SCHEMA_VERSION
        and marker.get("cache_root") == str(resolved_root)
    )


def ensure_managed_cache_root(cache_root: Path, *, protected_paths: tuple[Path, ...] = ()) -> Path:
    """Declare an explicitly configured runtime cache root as repository-managed."""
    resolved_root = _resolved_absolute(cache_root, "cache_root")
    home = Path.home().resolve(strict=False)
    protected = (*default_protected_cache_paths(), *protected_paths)
    if (
        resolved_root == Path("/")
        or resolved_root == home
        or is_system_path(resolved_root)
        or any(paths_overlap(resolved_root, item) for item in protected)
    ):
        raise RuntimeError(f"unsafe_cache_root_forbidden: {resolved_root}")
    resolved_root.mkdir(parents=True, exist_ok=True)
    marker_path = cache_root_marker_path(resolved_root)
    existing_marker = read_json(marker_path) if marker_path.exists() else {}
    if marker_path.exists() and (
        existing_marker.get("kind") != "msconnector-runtime-cache-root"
        or existing_marker.get("cache_root") != str(resolved_root)
    ):
        raise RuntimeError(f"invalid_managed_cache_root_marker: {marker_path}")
    if not cache_root_marker_valid(resolved_root):
        write_json(
            marker_path,
            {
                "kind": "msconnector-runtime-cache-root",
                "schema_version": CACHE_SCHEMA_VERSION,
                "cache_root": str(resolved_root),
                "created_at": utc_now(),
                "previous_schema_version": existing_marker.get("schema_version", ""),
            },
        )
    return resolved_root


def validate_managed_cache_child(
    path: Path,
    cache_root: Path,
    *,
    protected_paths: tuple[Path, ...] = (),
) -> tuple[Path, Path]:
    resolved_path = _resolved_absolute(path, "remove")
    resolved_root = _resolved_absolute(cache_root, "cache_root")
    protected = (*default_protected_cache_paths(), *protected_paths)
    if (
        resolved_path == Path("/")
        or resolved_path == Path.home().resolve(strict=False)
        or resolved_path == resolved_root
        or is_system_path(resolved_path)
        or not is_within(resolved_path, resolved_root)
        or any(paths_overlap(resolved_path, item) for item in protected)
    ):
        raise RuntimeError(f"unsafe_remove_path_forbidden: {resolved_path}")
    if not cache_root_marker_valid(resolved_root):
        raise RuntimeError(f"unmanaged_cache_root_marker_missing: {resolved_root}")
    entry_registry = resolved_root / CACHE_ENTRY_MARKER_DIRECTORY
    if resolved_path == entry_registry or is_within(resolved_path, entry_registry):
        raise RuntimeError(f"unsafe_remove_cache_control_path: {resolved_path}")
    return resolved_path, resolved_root


def cache_entry_marker_path(entry: Path, cache_root: Path) -> Path:
    key = stable_hash({"entry_path": str(entry.resolve(strict=False))})
    return cache_root / CACHE_ENTRY_MARKER_DIRECTORY / f"{key}.json"


def cache_entry_marker_valid(entry: Path, cache_root: Path) -> bool:
    resolved_entry = entry.resolve(strict=False)
    resolved_root = cache_root.resolve(strict=False)
    marker = read_json(cache_entry_marker_path(resolved_entry, resolved_root))
    return (
        marker.get("kind") == "msconnector-runtime-cache-entry"
        and marker.get("schema_version") == CACHE_SCHEMA_VERSION
        and marker.get("cache_root") == str(resolved_root)
        and marker.get("entry_path") == str(resolved_entry)
        and isinstance(marker.get("component"), str)
        and bool(marker.get("component"))
        and isinstance(marker.get("cache_key"), str)
        and bool(marker.get("cache_key"))
    )


def cache_entry_complete(
    entry: Path,
    cache_root: Path,
    *,
    component: str,
    cache_key: str,
    cache_identity: dict[str, Any] | None = None,
) -> bool:
    """Check the registry-side completion manifest for a cache entry."""
    resolved_entry = entry.resolve(strict=False)
    resolved_root = cache_root.resolve(strict=False)
    marker = read_json(cache_entry_marker_path(resolved_entry, resolved_root))
    return (
        cache_entry_marker_valid(resolved_entry, resolved_root)
        and marker.get("component") == component
        and marker.get("cache_key") == cache_key
        and marker.get("status") == CACHE_MANIFEST_STATUS_COMPLETE
        and (cache_identity is None or marker.get("cache_identity") == cache_identity)
    )


def write_cache_entry_completion(
    entry: Path,
    cache_root: Path,
    *,
    component: str,
    cache_key: str,
    cache_identity: dict[str, Any],
) -> None:
    """Write a complete registry-side manifest without touching a Git tree."""
    resolved_entry, resolved_root = validate_managed_cache_child(entry, cache_root)
    marker_path = cache_entry_marker_path(resolved_entry, resolved_root)
    marker = read_json(marker_path)
    if (
        not cache_entry_marker_valid(resolved_entry, resolved_root)
        or marker.get("component") != component
        or marker.get("cache_key") != cache_key
    ):
        raise RuntimeError(f"managed_cache_entry_identity_mismatch: {resolved_entry}")
    identity_key = cache_identity.get("cache_key")
    identity_payload = dict(cache_identity)
    identity_payload.pop("cache_key", None)
    if identity_key != cache_key or stable_hash(identity_payload) != cache_key:
        raise RuntimeError(f"invalid_cache_entry_identity: {resolved_entry}")
    marker.update(
        status=CACHE_MANIFEST_STATUS_COMPLETE,
        cache_identity=cache_identity,
        completed_at=utc_now(),
    )
    write_json(marker_path, marker)


def migrate_legacy_cache_entry_for_removal(
    entry: Path,
    cache_root: Path,
    *,
    component: str,
) -> bool:
    """Upgrade one exact legacy entry marker solely so the entry can be removed.

    Schema upgrades must rebuild old entries, not silently reuse them.  A
    legacy marker therefore grants deletion only when it still binds the exact
    canonical cache root and target path and names the expected component.  It
    is deliberately not a generic path claim and its old cache key is never
    treated as a cache hit.
    """
    resolved_entry, resolved_root = validate_managed_cache_child(entry, cache_root)
    marker_path = cache_entry_marker_path(resolved_entry, resolved_root)
    marker = read_json(marker_path)
    schema_version = marker.get("schema_version")
    if (
        marker.get("kind") != "msconnector-runtime-cache-entry"
        or not isinstance(schema_version, int)
        or schema_version < 1
        or schema_version >= CACHE_SCHEMA_VERSION
        or marker.get("cache_root") != str(resolved_root)
        or marker.get("entry_path") != str(resolved_entry)
        or marker.get("component") != component
        or not isinstance(marker.get("cache_key"), str)
        or not marker.get("cache_key")
    ):
        return False
    write_json(
        marker_path,
        {
            "kind": "msconnector-runtime-cache-entry",
            "schema_version": CACHE_SCHEMA_VERSION,
            "cache_root": str(resolved_root),
            "entry_path": str(resolved_entry),
            "component": component,
            "cache_key": marker["cache_key"],
            "created_at": utc_now(),
            "migrated_from_schema_version": schema_version,
        },
    )
    return True


def validated_cache_manifest_for_entry(entry: Path) -> dict[str, Any] | None:
    """Return a complete, self-consistent local manifest for exactly ``entry``.

    A filename and a plausible path string are not enough to authorize removal:
    the manifest must carry a current schema cache identity whose deterministic
    key agrees with the manifest, and it must explicitly bind that identity to
    this directory.
    """
    resolved_entry = entry.resolve(strict=False)
    for manifest_path in (resolved_entry / "manifest.json", resolved_entry / "component-manifest.json"):
        manifest = read_json(manifest_path)
        if not manifest:
            continue
        identity = manifest.get("cache_identity")
        cache_key = manifest.get("cache_key")
        if (
            manifest.get("status") != CACHE_MANIFEST_STATUS_COMPLETE
            or manifest.get("cache_schema_version") != CACHE_SCHEMA_VERSION
            or not isinstance(identity, dict)
            or identity.get("cache_schema_version") != CACHE_SCHEMA_VERSION
            or not isinstance(cache_key, str)
            or not cache_key
            or identity.get("cache_key") != cache_key
        ):
            continue
        identity_payload = dict(identity)
        identity_payload.pop("cache_key", None)
        if stable_hash(identity_payload) != cache_key:
            continue
        for key in ("prefix", "build_root", "root", "build_path", "path", "source_path"):
            raw_path = manifest.get(key)
            if not isinstance(raw_path, str) or not raw_path:
                continue
            try:
                if Path(raw_path).resolve(strict=False) == resolved_entry:
                    return manifest
            except OSError:
                continue
        if manifest_path.parent == resolved_entry and resolved_entry.name == cache_key:
            return manifest
    return None


def cache_manifest_owns_entry(entry: Path) -> bool:
    """Whether a validated local manifest uniquely assigns this cache entry."""
    return validated_cache_manifest_for_entry(entry) is not None


def managed_cache_entry_valid(entry: Path, cache_root: Path) -> bool:
    return cache_entry_marker_valid(entry, cache_root) or cache_manifest_owns_entry(entry)


def mark_managed_cache_entry(
    entry: Path,
    cache_root: Path,
    *,
    component: str,
    cache_key: str,
) -> None:
    resolved_entry, resolved_root = validate_managed_cache_child(entry, cache_root)
    marker_path = cache_entry_marker_path(resolved_entry, resolved_root)
    existing_marker = read_json(marker_path) if marker_path.exists() else {}
    entry_exists = resolved_entry.exists() or resolved_entry.is_symlink()
    manifest = validated_cache_manifest_for_entry(resolved_entry) if entry_exists else None
    if entry_exists and not cache_entry_marker_valid(resolved_entry, resolved_root):
        # A self-consistent local manifest can authorize *removal* of an old
        # cache entry, but it must never become a substitute for the registry
        # marker.  In particular, do not bless an interrupted or externally
        # copied tree merely because it contains a plausible manifest: callers
        # must remove that entry and build a newly marked staging entry.
        if manifest is not None:
            raise RuntimeError(f"managed_cache_entry_requires_rebuild: {resolved_entry}")
        raise RuntimeError(f"unmanaged_cache_entry_marker_missing: {resolved_entry}")
    if marker_path.exists() and not cache_entry_marker_valid(resolved_entry, resolved_root):
        raise RuntimeError(f"invalid_managed_cache_entry_marker: {marker_path}")
    if existing_marker and cache_entry_marker_valid(resolved_entry, resolved_root):
        if existing_marker.get("component") != component or existing_marker.get("cache_key") != cache_key:
            raise RuntimeError(f"managed_cache_entry_identity_mismatch: {resolved_entry}")
        return
    write_json(
        marker_path,
        {
            "kind": "msconnector-runtime-cache-entry",
            "schema_version": CACHE_SCHEMA_VERSION,
            "cache_root": str(resolved_root),
            "entry_path": str(resolved_entry),
            "component": component,
            "cache_key": cache_key,
            "created_at": utc_now(),
        },
    )


def remove_managed_cache_entry_marker(entry: Path, cache_root: Path) -> None:
    marker_path = cache_entry_marker_path(entry.resolve(strict=False), cache_root.resolve(strict=False))
    try:
        marker_path.unlink()
    except FileNotFoundError:
        pass


def temporary_cache_dir(
    final_path: Path,
    cache_root: Path,
    *,
    component: str = "staging",
    cache_key: str = "",
) -> Path:
    """Create a same-filesystem staging directory for atomic cache publication."""
    resolved_final, resolved_root = validate_managed_cache_child(final_path, cache_root)
    resolved_final.parent.mkdir(parents=True, exist_ok=True)
    for _ in range(32):
        staging = resolved_final.parent / f".{resolved_final.name}.tmp-{os.getpid()}-{uuid.uuid4().hex}"
        # Register the randomly named, still-nonexistent path before creating
        # it.  This preserves per-entry ownership even for an interrupted
        # staging setup without retroactively claiming an existing directory.
        mark_managed_cache_entry(staging, resolved_root, component=component, cache_key=cache_key or resolved_final.name)
        try:
            staging.mkdir()
            return staging
        except FileExistsError:
            remove_managed_cache_entry_marker(staging, resolved_root)
    raise RuntimeError(f"cache_staging_directory_collision: {resolved_final.parent}")


def atomic_publish_dir(
    staging_path: Path,
    final_path: Path,
    cache_root: Path,
    *,
    require_complete: bool = False,
) -> None:
    """Publish a fully prepared cache entry without replacing a valid peer entry."""
    staging, resolved_root = validate_managed_cache_child(staging_path, cache_root)
    final, _ = validate_managed_cache_child(final_path, resolved_root)
    if not staging.is_dir():
        raise RuntimeError(f"cache_staging_directory_missing: {staging}")
    if not managed_cache_entry_valid(staging, resolved_root):
        raise RuntimeError(f"unmanaged_cache_entry_marker_missing: {staging}")
    if final.exists():
        raise RuntimeError(f"cache_publish_destination_exists: {final}")
    staging_marker = read_json(cache_entry_marker_path(staging, resolved_root))
    if require_complete and (
        staging_marker.get("status") != CACHE_MANIFEST_STATUS_COMPLETE
        and read_json(staging / "manifest.json").get("status") != CACHE_MANIFEST_STATUS_COMPLETE
    ):
        raise RuntimeError(f"cache_staging_manifest_incomplete: {staging}")
    publish_lock = final.parent / f".{final.name}.publish.lock"
    try:
        publish_lock.mkdir()
    except FileExistsError as exc:
        if final.exists():
            raise RuntimeError(f"cache_publish_destination_exists: {final}") from exc
        raise RuntimeError(f"cache_publish_lock_busy: {publish_lock}") from exc
    try:
        # Do not let a non-cooperating writer overwrite a valid peer entry.
        if final.exists():
            raise RuntimeError(f"cache_publish_destination_exists: {final}")
        final_marker = dict(staging_marker)
        final_marker.update(
            schema_version=CACHE_SCHEMA_VERSION,
            cache_root=str(resolved_root),
            entry_path=str(final),
            published_at=utc_now(),
        )
        write_json(cache_entry_marker_path(final, resolved_root), final_marker)
        os.replace(staging, final)
        remove_managed_cache_entry_marker(staging, resolved_root)
    except Exception:
        remove_managed_cache_entry_marker(final, resolved_root)
        raise
    finally:
        try:
            publish_lock.rmdir()
        except OSError:
            pass


def safe_remove_dir(
    path: Path,
    owner: Path,
    *,
    protected_paths: tuple[Path, ...] = (),
) -> None:
    """Remove only a per-entry marked or manifest-owned cache entry."""
    managed_owner = ensure_managed_cache_root(owner)
    resolved_path, resolved_root = validate_managed_cache_child(path, managed_owner, protected_paths=protected_paths)
    if not resolved_path.exists():
        return
    if not managed_cache_entry_valid(resolved_path, resolved_root):
        raise RuntimeError(f"unmanaged_cache_entry_marker_missing: {resolved_path}")
    shutil.rmtree(resolved_path)
    remove_managed_cache_entry_marker(resolved_path, resolved_root)


def safe_remove_file(
    path: Path,
    owner: Path,
    *,
    protected_paths: tuple[Path, ...] = (),
) -> None:
    managed_owner = ensure_managed_cache_root(owner)
    resolved_path, resolved_root = validate_managed_cache_child(path, managed_owner, protected_paths=protected_paths)
    if not resolved_path.exists() and not resolved_path.is_symlink():
        return
    if not resolved_path.is_file() and not resolved_path.is_symlink():
        raise RuntimeError(f"unsafe_remove_file_not_regular: {resolved_path}")
    if not managed_cache_entry_valid(resolved_path, resolved_root):
        raise RuntimeError(f"unmanaged_cache_entry_marker_missing: {resolved_path}")
    resolved_path.unlink()
    remove_managed_cache_entry_marker(resolved_path, resolved_root)


def git_output(path: Path, *args: str) -> str:
    proc = run(["git", "-C", str(path), *args])
    return proc.stdout.strip()


def git_revision(path: Path) -> str:
    proc = run(["git", "-C", str(path), "rev-parse", "HEAD"])
    return proc.stdout.strip() if proc.returncode == 0 else ""


def resolved_remote_git_ref(url: str, expected_ref: str) -> str:
    """Resolve a requested Git ref without mutating a published checkout.

    Cache reuse for a moving branch must still notice that origin advanced.
    ``git ls-remote`` supplies that freshness check without cloning or
    fetching the immutable published source tree.
    """
    if re.fullmatch(r"[0-9a-fA-F]{40,64}", expected_ref):
        return expected_ref
    requested = expected_ref.removeprefix("origin/")
    if requested.startswith("refs/heads/"):
        candidates = (requested,)
    elif requested.startswith("refs/tags/"):
        candidates = (f"{requested}^{{}}", requested)
    elif requested.startswith("refs/"):
        candidates = (requested,)
    else:
        candidates = (
            f"refs/heads/{requested}",
            f"refs/tags/{requested}^{{}}",
            f"refs/tags/{requested}",
            requested,
        )
    proc = run(["git", "ls-remote", url, *candidates])
    if proc.returncode != 0:
        return ""
    resolved: dict[str, str] = {}
    for line in proc.stdout.splitlines():
        fields = line.split()
        if len(fields) >= 2 and re.fullmatch(r"[0-9a-fA-F]{40,64}", fields[0]):
            resolved.setdefault(fields[1], fields[0])
    for candidate in candidates:
        if candidate in resolved:
            return resolved[candidate]
    return ""


def submodule_status_clean(status_text: str) -> tuple[bool, str]:
    for line in status_text.splitlines():
        if not line:
            continue
        if line.startswith("-"):
            return False, "submodule_missing"
        if line.startswith("+"):
            return False, "submodule_ref_mismatch"
    return True, ""


def should_skip_fsck(previous: dict[str, Any], record: dict[str, Any], strict: bool) -> bool:
    if strict:
        return False
    return (
        previous.get("url") == record.get("url")
        and previous.get("expected_ref") == record.get("expected_ref")
        and previous.get("actual_head") == record.get("actual_head")
        and previous.get("submodule_status") == record.get("submodule_status")
        and previous.get("git_fsck") == "PASS"
    )


def source_cache_identity(
    name: str,
    url: str,
    expected_ref: str,
    resolved_commit: str | None = None,
) -> dict[str, Any]:
    """Identity for a Git source, including the immutable resolved commit."""
    if resolved_commit is None:
        # Preserve deterministic identities for callers already pinning a
        # full commit, while leaving moving refs unresolved until Git has
        # fetched and checked out their current origin commit.
        resolved_commit = expected_ref if re.fullmatch(r"[0-9a-fA-F]{40,64}", expected_ref) else ""
    identity: dict[str, Any] = {
        "cache_schema_version": CACHE_SCHEMA_VERSION,
        "component": name,
        "source_kind": "git",
        "url": url,
        "expected_ref": expected_ref,
        "resolved_commit": resolved_commit,
    }
    identity["cache_key"] = stable_hash(identity)
    return identity


def archive_cache_identity(name: str, url: str, expected_sha: str, sha_url: str) -> dict[str, Any]:
    identity: dict[str, Any] = {
        "cache_schema_version": CACHE_SCHEMA_VERSION,
        "component": name,
        "source_kind": "archive",
        "url": url,
        "expected_sha256": expected_sha,
        "sha256_url": sha_url,
    }
    identity["cache_key"] = stable_hash(identity)
    return identity


def retag_staging_cache_entry(
    entry: Path,
    cache_root: Path,
    *,
    component: str,
    cache_key: str,
) -> None:
    """Bind a newly-created, incomplete staging entry to its final identity."""
    resolved_entry, resolved_root = validate_managed_cache_child(entry, cache_root)
    marker_path = cache_entry_marker_path(resolved_entry, resolved_root)
    marker = read_json(marker_path)
    if (
        not cache_entry_marker_valid(resolved_entry, resolved_root)
        or marker.get("component") != component
        or marker.get("status") == CACHE_MANIFEST_STATUS_COMPLETE
        or not resolved_entry.name.startswith(".")
        or ".tmp-" not in resolved_entry.name
    ):
        raise RuntimeError(f"invalid_staging_cache_entry: {resolved_entry}")
    marker["cache_key"] = cache_key
    write_json(marker_path, marker)


def git_checkout_is_reusable(
    checkout_path: Path,
    cache_root: Path,
    *,
    component: str,
    cache_identity: dict[str, Any],
    expected_url: str,
    actual_head: str,
) -> bool:
    """Read-only validation for a published source checkout cache hit."""
    cache_key = str(cache_identity["cache_key"])
    if not (
        checkout_path.is_dir()
        and (checkout_path / ".git").exists()
        and cache_entry_complete(
            checkout_path,
            cache_root,
            component=component,
            cache_key=cache_key,
            cache_identity=cache_identity,
        )
    ):
        return False
    remote = git_output(checkout_path, "config", "--get", "remote.origin.url")
    if remote != expected_url or git_revision(checkout_path) != actual_head:
        return False
    status = run(
        [
            "git",
            "-C",
            str(checkout_path),
            "status",
            "--porcelain",
            "--untracked-files=all",
            "--ignored=matching",
        ]
    )
    return status.returncode == 0 and not status.stdout.strip()


def reusable_git_source_record(
    checkout_path: Path,
    cache_root: Path,
    *,
    name: str,
    expected_url: str,
    expected_ref: str,
    previous: dict[str, Any],
) -> dict[str, Any] | None:
    """Return current provenance for a clean, complete published checkout.

    Target-specific preparation calls share one Cache-v2 source root.  The
    first call has already resolved a moving ref in a fresh clone and stored
    its immutable commit in the root manifest.  A later target can safely
    reuse that exact completed checkout after local provenance/cleanliness
    checks; it must not create another clone merely to rediscover the same
    commit.  Missing, dirty, stale, or incomplete records deliberately fall
    through to the normal fresh-clone recovery path.
    """
    actual_head = previous.get("actual_head")
    if not (
        previous.get("status") in {"present", "built", "reused"}
        and previous.get("url") == expected_url
        and previous.get("expected_ref") == expected_ref
        and isinstance(actual_head, str)
        and actual_head
        and previous.get("git_fsck") == "PASS"
    ):
        return None
    remote_head = resolved_remote_git_ref(expected_url, expected_ref)
    if not remote_head or remote_head.lower() != actual_head.lower():
        return None
    identity = source_cache_identity(name, expected_url, expected_ref, actual_head)
    component = f"source:{name}"
    if not git_checkout_is_reusable(
        checkout_path,
        cache_root,
        component=component,
        cache_identity=identity,
        expected_url=expected_url,
        actual_head=actual_head,
    ):
        return None
    submodules = git_output(checkout_path, "submodule", "status", "--recursive")
    clean, _ = submodule_status_clean(submodules)
    if not clean:
        return None
    return {
        "actual_head": actual_head,
        "status_short": "",
        "submodule_status": submodules,
        "submodule_count": len([line for line in submodules.splitlines() if line.strip()]),
        "submodule_status_clean": True,
        "git_fsck": "PASS",
        "tree": tree_manifest(checkout_path),
        "cache_schema_version": CACHE_SCHEMA_VERSION,
        "cache_identity": identity,
        "cache_key": identity["cache_key"],
    }


def prepare_git_component(
    name: str,
    url: str,
    expected_ref: str,
    path: Path,
    previous_records: dict[str, dict[str, Any]],
    strict: bool,
    cache_root: Path | None = None,
    _recovery_attempt: bool = False,
    _lock_held: bool = False,
) -> dict[str, Any]:
    managed_root: Path | None = None
    checkout_path = Path(path)
    record: dict[str, Any] = {
        "name": name,
        "url": url,
        "expected_ref": expected_ref,
        "path": str(checkout_path),
        "recursive_submodules": True,
        "submodule_count": 0,
        "submodule_status_clean": False,
        "git_fsck": "SKIPPED",
        "status": "unknown",
        "blocker_reason": "",
    }
    if not url or not expected_ref:
        record.update(status="blocked", blocker_reason="missing_url_or_ref")
        return record
    try:
        github_repo_path(url)
    except RuntimeError as exc:
        record.update(status="blocked", blocker_reason=f"https_github_url_policy:{exc}")
        return record
    if cache_root is not None:
        try:
            managed_root = ensure_managed_cache_root(cache_root)
            checkout_path, _ = validate_managed_cache_child(checkout_path, managed_root)
            record["path"] = str(checkout_path)
        except RuntimeError as exc:
            record.update(status="blocked", blocker_reason=str(exc))
            return record
    if is_system_path(checkout_path):
        record.update(status="blocked", blocker_reason="system_path_write_forbidden")
        return record
    # The lock is deliberately keyed by the requested ref, not the eventual
    # commit: a moving ref must serialize its resolve/build/publish sequence.
    ref_lock_identity = source_cache_identity(name, url, expected_ref)
    ref_lock_key = str(ref_lock_identity["cache_key"])
    if managed_root is not None and not _lock_held:
        try:
            with BuildLock(cache_entry_lock_path(managed_root, f"source-{name}", ref_lock_key)):
                return prepare_git_component(
                    name,
                    url,
                    expected_ref,
                    checkout_path,
                    previous_records,
                    strict,
                    cache_root=managed_root,
                    _recovery_attempt=_recovery_attempt,
                    _lock_held=True,
                )
        except TimeoutError as exc:
            record.update(status="blocked", blocker_reason="cache_lock_timeout", details=str(exc))
            return record
    staging_path: Path | None = None

    try:
        if managed_root is None and checkout_path.exists():
            record.update(status="blocked", blocker_reason="unmanaged_source_checkout_requires_cache_root")
            return record
        if managed_root is not None:
            previous = previous_records.get(name, {})
            if isinstance(previous, dict):
                reusable = reusable_git_source_record(
                    checkout_path,
                    managed_root,
                    name=name,
                    expected_url=url,
                    expected_ref=expected_ref,
                    previous=previous,
                )
                if reusable is not None:
                    record.update(
                        reusable,
                        path=str(checkout_path),
                        manifest=str(cache_entry_marker_path(checkout_path, managed_root)),
                        status="present",
                    )
                    return record
            # Always resolve and verify in a new entry.  A completed final
            # checkout that did not pass the prior-record reuse check is never
            # fetched, checked out, reset, or otherwise mutated in place.
            staging_path = temporary_cache_dir(
                checkout_path,
                managed_root,
                component=f"source:{name}",
                cache_key=ref_lock_key,
            )
            working_path = staging_path
        else:
            checkout_path.parent.mkdir(parents=True, exist_ok=True)
            working_path = checkout_path
        run(["git", "clone", "--recursive", url, str(working_path)], check=True)
        remote_url = git_output(working_path, "config", "--get", "remote.origin.url")
        if remote_url and remote_url != url:
            record.update(status="blocked", blocker_reason=f"unexpected_origin:{remote_url}")
            return record
        fetch = run(["git", "-C", str(working_path), "fetch", "--tags", "--prune", "origin"])
        if fetch.returncode != 0:
            record.update(status="blocked", blocker_reason="git_fetch_failed", details=(fetch.stdout + fetch.stderr).strip())
            return record
        checkout_candidates = [expected_ref]
        if (
            not expected_ref.startswith(("origin/", "refs/"))
            and not re.fullmatch(r"[0-9a-fA-F]{40,64}", expected_ref)
        ):
            # Prefer the freshly fetched remote tracking ref for branches;
            # tags and other refs still fall back to the requested spelling.
            checkout_candidates.insert(0, f"origin/{expected_ref}")
        checkout_ref = checkout_candidates[0]
        checkout = subprocess.CompletedProcess([], 1, "", "")
        for candidate in checkout_candidates:
            checkout_ref = candidate
            checkout = run(["git", "-C", str(working_path), "checkout", "--detach", candidate])
            if checkout.returncode == 0:
                break
        if checkout.returncode != 0:
            record.update(status="blocked", blocker_reason="git_checkout_failed", details=(checkout.stdout + checkout.stderr).strip())
            return record
        record["checkout_ref"] = checkout_ref
        for cmd in (
            ["git", "-C", str(working_path), "submodule", "sync", "--recursive"],
            ["git", "-C", str(working_path), "submodule", "update", "--init", "--recursive"],
        ):
            proc = run(cmd)
            if proc.returncode != 0:
                record.update(status="blocked", blocker_reason="submodule_update_failed", details=(proc.stdout + proc.stderr).strip())
                return record
        actual_head = git_output(working_path, "rev-parse", "HEAD")
        if not actual_head:
            record.update(status="blocked", blocker_reason="git_resolved_commit_missing")
            return record
        source_identity = source_cache_identity(name, url, expected_ref, actual_head)
        source_cache_key = str(source_identity["cache_key"])
        status_short = git_output(
            working_path,
            "status",
            "--porcelain",
            "--untracked-files=all",
            "--ignored=matching",
        )
        submodules = git_output(working_path, "submodule", "status", "--recursive")
        clean, reason = submodule_status_clean(submodules)
        record.update(
            actual_head=actual_head,
            status_short=status_short,
            submodule_status=submodules,
            submodule_count=len([line for line in submodules.splitlines() if line.strip()]),
            submodule_status_clean=clean,
            tree=tree_manifest(working_path),
            cache_schema_version=CACHE_SCHEMA_VERSION,
            cache_identity=source_identity,
            cache_key=source_cache_key,
        )
        if status_short:
            record.update(
                status="blocked",
                blocker_reason="dirty_source_checkout",
                details=status_short,
            )
            return record
        if not clean:
            record.update(status="blocked", blocker_reason=reason)
            return record
        # Resolution happens in a fresh clone, so always verify that clone
        # before it is eligible to replace the published checkout.
        fsck = run(["git", "-C", str(working_path), "fsck", "--full"])
        record["git_fsck"] = "PASS" if fsck.returncode == 0 else "FAIL"
        if fsck.returncode != 0:
            record.update(status="corrupt", blocker_reason="git_fsck_failed", details=(fsck.stdout + fsck.stderr).strip())
            return record
        if managed_root is not None:
            component = f"source:{name}"
            if git_checkout_is_reusable(
                checkout_path,
                managed_root,
                component=component,
                cache_identity=source_identity,
                expected_url=url,
                actual_head=actual_head,
            ):
                record.update(
                    path=str(checkout_path),
                    manifest=str(cache_entry_marker_path(checkout_path, managed_root)),
                    status="present",
                    tree=tree_manifest(checkout_path),
                )
                return record

            if checkout_path.exists():
                marker = read_json(cache_entry_marker_path(checkout_path, managed_root))
                if cache_entry_marker_valid(checkout_path, managed_root):
                    if marker.get("component") != component:
                        record.update(status="blocked", blocker_reason=f"managed_cache_entry_identity_mismatch: {checkout_path}")
                        return record
                elif cache_manifest_owns_entry(checkout_path):
                    # Markerless local manifests are deletion-only proofs.
                    pass
                elif not migrate_legacy_cache_entry_for_removal(checkout_path, managed_root, component=component):
                    record.update(status="blocked", blocker_reason=f"unmanaged_cache_entry_marker_missing: {checkout_path}")
                    return record
                safe_remove_dir(checkout_path, managed_root)
                record.update(
                    rebuild_required=True,
                    invalidation_reason="resolved_source_commit_changed_or_incomplete",
                    old_entry_removed=True,
                    previous_path=str(checkout_path),
                )

            assert staging_path is not None
            retag_staging_cache_entry(
                staging_path,
                managed_root,
                component=component,
                cache_key=source_cache_key,
            )
            write_cache_entry_completion(
                staging_path,
                managed_root,
                component=component,
                cache_key=source_cache_key,
                cache_identity=source_identity,
            )
            atomic_publish_dir(staging_path, checkout_path, managed_root, require_complete=True)
            staging_path = None
            record.update(
                path=str(checkout_path),
                manifest=str(cache_entry_marker_path(checkout_path, managed_root)),
                status="present",
                tree=tree_manifest(checkout_path),
            )
            return record
        record.update(path=str(checkout_path), status="present")
        return record
    except Exception as exc:
        record.update(status="blocked", blocker_reason=str(exc))
        return record
    finally:
        if staging_path is not None and staging_path.exists() and managed_root is not None:
            try:
                safe_remove_dir(staging_path, managed_root)
            except RuntimeError:
                pass


def resolve_latest_github_release_tag(source_url: str, cache_path: Path | None = None) -> tuple[str, str, str]:
    repo = github_repo_path(source_url)
    api_url = f"https://api.github.com/repos/{repo}/releases/latest"
    source = "network"
    try:
        raw = urlopen_bytes(api_url, timeout=60)
        data = json.loads(raw.decode("utf-8"))
        if cache_path is not None:
            atomic_write_bytes(cache_path, raw)
    except Exception as exc:
        if cache_path is None or not cache_path.is_file():
            raise
        data = json.loads(cache_path.read_text(encoding="utf-8"))
        source = f"cached_after_network_error:{exc}"
    tag = data.get("tag_name")
    html_url = data.get("html_url") or f"https://github.com/{repo}/releases/tag/{tag or ''}"
    if not isinstance(tag, str) or not tag:
        raise RuntimeError(f"latest release for {source_url} did not include tag_name")
    return tag, str(html_url), source


def prepare_release_git_component(
    name: str,
    source_url: str,
    expected_prompt_latest: str,
    path: Path,
    previous_records: dict[str, dict[str, Any]],
    strict: bool,
    optional: bool = False,
    cache_root: Path | None = None,
) -> dict[str, Any]:
    try:
        release_tag, release_url, release_lookup_status = resolve_latest_github_release_tag(
            source_url,
            path.parent / f"{name}-latest-release.json",
        )
    except Exception as exc:
        return {
            "name": name,
            "url": source_url,
            "source": source_url,
            "path": str(path),
            "expected_ref": "",
            "release_tag": "",
            "status": "blocked_optional" if optional else "blocked",
            "optional": optional,
            "blocker_reason": network_blocker_reason(exc, optional=optional),
        }
    record = prepare_git_component(
        name,
        source_url,
        release_tag,
        path,
        previous_records,
        strict,
        cache_root=cache_root,
    )
    if optional and record.get("status") in {"blocked", "corrupt"}:
        record["status"] = "blocked_optional"
        record["optional"] = True
        record["blocker_reason"] = f"optional_source_unavailable:{record.get('blocker_reason', 'unknown')}"
    record.update(
        source=source_url,
        release_tag=release_tag,
        release_url=release_url,
        release_lookup_status=release_lookup_status,
        optional=optional,
        expected_prompt_latest=expected_prompt_latest,
        release_tag_deviation=bool(expected_prompt_latest and release_tag != expected_prompt_latest),
        release_tag_deviation_note=(
            f"prompt_expected_latest={expected_prompt_latest}; current_latest={release_tag}"
            if expected_prompt_latest and release_tag != expected_prompt_latest
            else ""
        ),
    )
    return record


def archive_can_list(path: Path) -> bool:
    try:
        with tarfile.open(path) as archive:
            archive.getmembers()
        return True
    except Exception:
        return False


def download(url: str, dest: Path) -> None:
    require_https_url(url, "download URL")
    atomic_write_bytes(dest, urlopen_bytes(url, timeout=60))


def expected_sha_from_url(url: str, archive_name: str, dest: Path) -> str:
    if not url:
        return ""
    download(url, dest)
    text = dest.read_text(encoding="utf-8", errors="replace")
    for line in text.splitlines():
        fields = line.split()
        if not fields:
            continue
        if len(fields) == 1 or archive_name in fields[-1]:
            return fields[0]
    return ""


def prepare_archive(
    name: str,
    url: str,
    expected_sha: str,
    sha_url: str,
    dest_dir: Path,
    cache_root: Path | None = None,
    _lock_held: bool = False,
) -> dict[str, Any]:
    archive_name = url.rstrip("/").split("/")[-1] if url else ""
    path = dest_dir / archive_name if archive_name else dest_dir / name
    record: dict[str, Any] = {
        "name": name,
        "url": url,
        "path": str(path),
        "status": "unknown",
        "blocker_reason": "",
        "checksum_status": "checksum_unavailable",
    }
    if not url:
        record.update(status="blocked", blocker_reason="missing_url")
        return record
    if is_system_path(dest_dir):
        record.update(status="blocked", blocker_reason="system_path_write_forbidden")
        return record
    try:
        managed_root: Path | None = None
        archive_identity = archive_cache_identity(name, url, expected_sha, sha_url)
        archive_cache_key = str(archive_identity["cache_key"])
        if cache_root is not None:
            managed_root = ensure_managed_cache_root(cache_root)
            _, _ = validate_managed_cache_child(dest_dir, managed_root)
        if managed_root is not None and not _lock_held:
            try:
                with BuildLock(cache_entry_lock_path(managed_root, f"archive-{name}", archive_cache_key)):
                    return prepare_archive(
                        name,
                        url,
                        expected_sha,
                        sha_url,
                        dest_dir,
                        managed_root,
                        _lock_held=True,
                    )
            except TimeoutError as exc:
                record.update(status="blocked", blocker_reason="cache_lock_timeout", details=str(exc))
                return record
        dest_dir.mkdir(parents=True, exist_ok=True)
        if managed_root is not None:
            if path.exists():
                marker = read_json(cache_entry_marker_path(path, managed_root))
                if not cache_entry_marker_valid(path, managed_root):
                    if not migrate_legacy_cache_entry_for_removal(
                        path,
                        managed_root,
                        component=f"archive:{name}",
                    ):
                        record.update(status="blocked", blocker_reason=f"unmanaged_cache_entry_marker_missing: {path}")
                        return record
                    safe_remove_file(path, managed_root)
                    mark_managed_cache_entry(
                        path,
                        managed_root,
                        component=f"archive:{name}",
                        cache_key=archive_cache_key,
                    )
                    record.update(
                        rebuild_required=True,
                        invalidation_reason="cache_schema_changed",
                        old_entry_removed=True,
                    )
                elif marker.get("component") != f"archive:{name}":
                    record.update(status="blocked", blocker_reason=f"managed_cache_entry_identity_mismatch: {path}")
                    return record
                elif marker.get("cache_key") != archive_cache_key:
                    # The basename is intentionally stable for many upstream
                    # URLs.  A matching archive owner but different canonical
                    # identity is stale, so discard it before downloading.
                    safe_remove_file(path, managed_root)
                    mark_managed_cache_entry(
                        path,
                        managed_root,
                        component=f"archive:{name}",
                        cache_key=archive_cache_key,
                    )
                    record.update(
                        rebuild_required=True,
                        invalidation_reason="archive_cache_identity_changed",
                        old_entry_removed=True,
                    )
                elif not cache_entry_complete(
                    path,
                    managed_root,
                    component=f"archive:{name}",
                    cache_key=archive_cache_key,
                    cache_identity=archive_identity,
                ):
                    safe_remove_file(path, managed_root)
                    mark_managed_cache_entry(
                        path,
                        managed_root,
                        component=f"archive:{name}",
                        cache_key=archive_cache_key,
                    )
                    record.update(
                        rebuild_required=True,
                        invalidation_reason="incomplete_archive_cache_entry",
                        old_entry_removed=True,
                    )
            else:
                mark_managed_cache_entry(
                    path,
                    managed_root,
                    component=f"archive:{name}",
                    cache_key=archive_cache_key,
                )
        if not path.is_file() or path.stat().st_size <= 0 or not archive_can_list(path):
            if path.exists():
                if managed_root is not None:
                    safe_remove_file(path, managed_root)
                else:
                    path.unlink()
            if managed_root is not None:
                mark_managed_cache_entry(
                    path,
                    managed_root,
                    component=f"archive:{name}",
                    cache_key=archive_cache_key,
                )
            download(url, path)
        size = path.stat().st_size
        if size <= 0:
            if managed_root is not None:
                safe_remove_file(path, managed_root)
            else:
                path.unlink()
            record.update(status="corrupt", blocker_reason="empty_archive")
            return record
        if not archive_can_list(path):
            if managed_root is not None:
                safe_remove_file(path, managed_root)
            else:
                path.unlink()
            record.update(status="corrupt", blocker_reason="archive_list_failed")
            return record
        local_sha = sha256_file(path)
        record.update(size=size, sha256=local_sha, archive_list="PASS")
        expected = expected_sha
        if not expected and sha_url:
            expected = expected_sha_from_url(sha_url, archive_name, dest_dir / f"{name}.sha256")
        if expected:
            record["expected_sha256"] = expected
            record["checksum_status"] = "PASS" if expected == local_sha else "FAIL"
            if expected != local_sha:
                if managed_root is not None:
                    safe_remove_file(path, managed_root)
                else:
                    path.unlink()
                record.update(status="corrupt", blocker_reason="sha256_mismatch")
                return record
        if managed_root is not None:
            write_cache_entry_completion(
                path,
                managed_root,
                component=f"archive:{name}",
                cache_key=archive_cache_key,
                cache_identity=archive_identity,
            )
        record["status"] = "present"
        return record
    except Exception as exc:
        record.update(status="blocked", blocker_reason=str(exc))
        return record


def github_repo_path(url: str) -> str:
    raw = url.strip()
    parsed = urlsplit(raw)
    if parsed.scheme != "https":
        raise RuntimeError(f"only HTTPS GitHub URLs are supported: {url}")
    if parsed.netloc != "github.com":
        raise RuntimeError(f"only github.com URLs are supported: {url}")
    if parsed.query or parsed.fragment:
        raise RuntimeError(f"not a plain GitHub owner/repo URL: {url}")
    repo = parsed.path.removeprefix("/").removesuffix(".git").strip("/")
    parts = repo.split("/")
    if len(parts) != 2 or not parts[0] or not parts[1]:
        raise RuntimeError(f"not a plain GitHub owner/repo URL: {url}")
    return f"{parts[0]}/{parts[1]}"


def resolve_nginx_archive(env: dict[str, str], latest_cache_path: Path | None = None) -> tuple[str, str, str]:
    mode = env.get("NGINX_SOURCE_MODE", "github-release")
    if mode != "github-release":
        raise RuntimeError(f"unsupported NGINX_SOURCE_MODE={mode}")
    repo_url = env.get("NGINX_SOURCE_REPO_URL") or env.get("NGINX_GITHUB_REPO")
    tag = env.get("NGINX_RELEASE_TAG") or env.get("NGINX_SOURCE_GIT_REF") or "latest"
    if not repo_url:
        raise RuntimeError("missing NGINX_SOURCE_REPO_URL")
    repo = github_repo_path(repo_url)
    lookup_status = "configured"
    if tag == "latest":
        api_url = f"https://api.github.com/repos/{repo}/releases/latest"
        lookup_status = "network"
        try:
            raw = urlopen_bytes(api_url, timeout=60)
            data = json.loads(raw.decode("utf-8"))
            if latest_cache_path is not None:
                atomic_write_bytes(latest_cache_path, raw)
        except Exception as exc:
            if latest_cache_path is None or not latest_cache_path.is_file():
                raise
            data = json.loads(latest_cache_path.read_text(encoding="utf-8"))
            lookup_status = f"cached_after_network_error:{exc}"
        tag = data.get("tag_name")
        if not isinstance(tag, str) or not tag:
            raise RuntimeError("GitHub latest release response missing tag_name")
    return tag, f"https://github.com/{repo}/archive/refs/tags/{tag}.tar.gz", lookup_status


def default_state_home() -> Path:
    from runtime_path_utils import verified_runtime_paths

    return Path(verified_runtime_paths(os.environ)["VERIFIED_STATE_ROOT"])


def executable(path: Path) -> bool:
    return path.is_file() and os.access(path, os.X_OK)


def resolve_executable(configured: str) -> str | None:
    if not configured:
        return None
    if "/" in configured:
        path = Path(configured)
        return str(path) if executable(path) else None
    return shutil.which(configured)


def read_key_values(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if "=" not in line or line.lstrip().startswith("#"):
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def artifact_status(paths: dict[str, Path], executable_keys: set[str] | None = None) -> tuple[bool, list[str]]:
    executable_keys = executable_keys or set()
    missing = []
    for key, path in paths.items():
        if key in executable_keys:
            if not executable(path):
                missing.append(f"{key}:{path}")
        elif not path.is_file():
            missing.append(f"{key}:{path}")
    return not missing, missing


def build_env(base: dict[str, str], **overrides: str) -> dict[str, str]:
    result = dict(base)
    for key, value in overrides.items():
        if value is not None:
            result[key] = value
    return result


def command_text(cmd: list[str], cwd: Path | None = None, env: dict[str, str] | None = None) -> str:
    proc = run_env(cmd, cwd=cwd, env=env)
    text = (proc.stdout + proc.stderr).strip()
    return text if proc.returncode == 0 else f"unavailable rc={proc.returncode}: {text}"


def compiler_identity(env: dict[str, str]) -> dict[str, str]:
    cc = resolve_compiler(env)
    cxx_configured = env.get("CXX", "").strip()
    cxx = cxx_configured.split()[0] if cxx_configured and shutil.which(cxx_configured.split()[0]) else (shutil.which("c++") or shutil.which("g++") or "")
    return {
        "cc": cc,
        "cc_version": command_text([cc, "--version"], env=env).splitlines()[0] if cc else "",
        "cxx": cxx,
        "cxx_version": command_text([cxx, "--version"], env=env).splitlines()[0] if cxx else "",
    }


def toolchain_identity(env: dict[str, str]) -> dict[str, Any]:
    """Capture compiler, linker, and build-tool versions that affect artifacts."""
    identity: dict[str, Any] = dict(compiler_identity(env))
    linker_configured = env.get("LD", "").strip().split()
    linker = linker_configured[0] if linker_configured and shutil.which(linker_configured[0]) else (shutil.which("ld") or "")
    identity["linker"] = linker
    identity["linker_version"] = command_text([linker, "--version"], env=env).splitlines()[0] if linker else ""
    build_tools: dict[str, str] = {}
    for tool in ("make", "cmake", "autoconf", "meson", "ninja"):
        resolved = shutil.which(tool)
        build_tools[tool] = command_text([resolved, "--version"], env=env).splitlines()[0] if resolved else ""
    identity["build_tools"] = build_tools
    return identity


def hash_file_contents(path: Path, digest: Any) -> None:
    try:
        rel = path.as_posix()
        data = path.read_bytes()
    except OSError:
        return
    digest.update(rel.encode("utf-8", "surrogateescape"))
    digest.update(b"\0")
    digest.update(hashlib.sha256(data).hexdigest().encode("ascii"))
    digest.update(b"\0")


def hash_input_paths(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for root in paths:
        if not root.exists():
            digest.update(f"missing:{root}".encode("utf-8", "surrogateescape"))
            digest.update(b"\0")
            continue
        if root.is_file():
            hash_file_contents(root, digest)
            continue
        for item in sorted(root.rglob("*")):
            if ".git" in item.parts or "__pycache__" in item.parts:
                continue
            if not item.is_file():
                continue
            if item.suffix in {".o", ".so", ".a", ".la", ".lo", ".log"}:
                continue
            try:
                rel = item.relative_to(root)
            except ValueError:
                rel = item
            digest.update(f"{root.as_posix()}:{rel.as_posix()}".encode("utf-8", "surrogateescape"))
            digest.update(hashlib.sha256(item.read_bytes()).hexdigest().encode("ascii"))
            digest.update(b"\0")
    return digest.hexdigest()


def read_text_if_file(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def run_build(script: Path, env: dict[str, str], cwd: Path, log_path: Path) -> subprocess.CompletedProcess[str]:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        ["sh", str(script)],
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    log_path.write_text(proc.stdout, encoding="utf-8", errors="replace")
    return proc


def append_command_log(log_parts: list[str], label: str, proc: subprocess.CompletedProcess[str]) -> None:
    log_parts.extend(
        [
            f"[{label}]",
            f"returncode={proc.returncode}",
            "$ " + " ".join(sh_quote(str(part)) for part in proc.args) if isinstance(proc.args, list) else f"$ {proc.args}",
            "",
            proc.stdout,
            proc.stderr,
            "",
        ]
    )


def write_component_log(log_path: Path, log_parts: list[str]) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("\n".join(log_parts), encoding="utf-8", errors="replace")


def local_build_env(base: dict[str, str], cache_root: Path) -> dict[str, str]:
    result = dict(base)
    result["GOPATH"] = str(cache_root / "go")
    result["GOMODCACHE"] = str(cache_root / "go/pkg/mod")
    result["GOCACHE"] = str(cache_root / "go/cache")
    result["XDG_CACHE_HOME"] = str(cache_root / "go/xdg-cache")
    return result


def resolve_compiler(env: dict[str, str]) -> str:
    configured = env.get("CC", "").strip()
    if configured:
        return configured.split()[0] if shutil.which(configured.split()[0]) else ""
    return shutil.which("cc") or shutil.which("gcc") or ""


def first_missing_tool(tools: list[tuple[str, str]]) -> str:
    for tool, reason in tools:
        if not shutil.which(tool):
            return reason
    return ""


def expat_libs(lib_dir: Path) -> list[Path]:
    if not lib_dir.is_dir():
        return []
    return sorted(path for path in lib_dir.glob("libexpat.*") if path.is_file() or path.is_symlink())


def expat_artifacts_ready(prefix: Path) -> bool:
    return (prefix / "include/expat.h").is_file() and bool(expat_libs(prefix / "lib"))


def expat_source_dir(repo_path: Path) -> Path:
    for candidate in (repo_path / "expat", repo_path):
        if (
            (candidate / "buildconf.sh").is_file()
            or (candidate / "configure").is_file()
            or (candidate / "configure.ac").is_file()
            or (candidate / "CMakeLists.txt").is_file()
        ):
            return candidate
    return repo_path


def map_expat_build_failure(text: str) -> str:
    lowered = text.lower()
    if "cmake" in lowered and "not found" in lowered:
        return "missing_cmake"
    if "autoconf" in lowered and ("not found" in lowered or "no such file" in lowered):
        return "missing_autoconf"
    if "automake" in lowered or "aclocal" in lowered:
        return "missing_automake"
    if "libtoolize" in lowered or "glibtoolize" in lowered or "libtool" in lowered:
        return "missing_libtool"
    if re.search(r"\bmake\b.*(not found|no such file)", lowered):
        return "missing_make"
    if "c compiler" in lowered or "compiler" in lowered and "not found" in lowered:
        return "missing_compiler"
    return "expat_build_failed"


def expat_override_entries_complete(
    prefix: Path,
    build_dir: Path,
    source_copy: Path,
    cache_root: Path,
    cache_identity: dict[str, Any],
) -> bool:
    """A managed override is reusable only when every published entry completed."""
    cache_key = str(cache_identity["cache_key"])
    return (
        expat_artifacts_ready(prefix)
        and cache_manifest_complete(prefix / "component-manifest.json", cache_identity)
        and build_dir.is_dir()
        and source_copy.is_dir()
        and cache_entry_complete(
            prefix,
            cache_root,
            component="expat-prefix",
            cache_key=cache_key,
            cache_identity=cache_identity,
        )
        and cache_entry_complete(
            build_dir,
            cache_root,
            component="expat-build",
            cache_key=cache_key,
            cache_identity=cache_identity,
        )
        and cache_entry_complete(
            source_copy,
            cache_root,
            component="expat-source",
            cache_key=cache_key,
            cache_identity=cache_identity,
        )
    )


def prepare_expat_managed_overrides(
    env: dict[str, str],
    cache_root: Path,
    build_root: Path,
    git_record: dict[str, Any],
    record: dict[str, Any],
    *,
    prefix: Path,
    build_dir: Path,
    source_copy: Path,
    cache_identity: dict[str, Any],
) -> dict[str, Any]:
    """Publish explicit, managed Expat paths from isolated staging entries.

    Historical EXPAT_PREFIX/EXPAT_BUILD_DIR support wrote directly into the
    supplied directories.  Keep the override feature only for cache-managed
    paths, and publish each independently owned path from a completed staging
    entry.  This makes an interrupted override build non-reusable and keeps
    external/unowned directories out of the cache mutation path.
    """
    final_entries = (
        ("expat-prefix", prefix),
        ("expat-build", build_dir),
        ("expat-source", source_copy),
    )
    try:
        resolved_entries = tuple(
            (component, validate_managed_cache_child(path, cache_root)[0])
            for component, path in final_entries
        )
    except RuntimeError as exc:
        record.update(status="blocked", blocker_reason=str(exc))
        return record
    for index, (_, first) in enumerate(resolved_entries):
        if any(paths_overlap(first, second) for _, second in resolved_entries[index + 1 :]):
            record.update(status="blocked", blocker_reason="expat_override_paths_overlap")
            return record

    cache_key = str(cache_identity["cache_key"])
    staging_entries: dict[str, Path | None] = {}
    try:
        with BuildLock(cache_entry_lock_path(cache_root, "expat", cache_key)):
            if expat_override_entries_complete(prefix, build_dir, source_copy, cache_root, cache_identity):
                previous = read_json(prefix / "component-manifest.json")
                record.update(
                    status="present",
                    manifest=str(prefix / "component-manifest.json"),
                    libraries=[str(path) for path in expat_libs(prefix / "lib")],
                    build_system=previous.get("build_system", ""),
                    tree=tree_manifest(prefix),
                )
                return record

            for component, final_path in resolved_entries:
                if not final_path.exists():
                    continue
                if not managed_cache_entry_valid(final_path, cache_root):
                    if not migrate_legacy_cache_entry_for_removal(final_path, cache_root, component=component):
                        record.update(status="blocked", blocker_reason=f"unmanaged_cache_entry_marker_missing: {final_path}")
                        return record
                record.update(
                    rebuild_required=True,
                    invalidation_reason="missing_or_incomplete_expat_override_cache",
                    old_entry_removed=True,
                )

            for component, final_path in resolved_entries:
                staging_entries[component] = temporary_cache_dir(
                    final_path,
                    cache_root,
                    component=component,
                    cache_key=cache_key,
                )
            staged_env = dict(env)
            staged_env.update(
                EXPAT_PREFIX=str(staging_entries["expat-prefix"]),
                EXPAT_BUILD_DIR=str(staging_entries["expat-build"]),
                EXPAT_SOURCE_COPY=str(staging_entries["expat-source"]),
            )
            staged_record = prepare_expat(staged_env, cache_root, build_root, git_record, _transactional=True)
            if staged_record.get("status") != "built":
                failed_record = dict(staged_record)
                failed_record.update(
                    prefix=str(prefix),
                    expat_h=str(prefix / "include/expat.h"),
                    include=str(prefix / "include/expat.h"),
                    lib_dir=str(prefix / "lib"),
                    library=str(prefix / "lib"),
                    build_path=str(build_dir),
                    build_source_copy=str(source_copy),
                    manifest=str(prefix / "component-manifest.json"),
                )
                return failed_record

            for component, staging_path in staging_entries.items():
                assert staging_path is not None
                write_cache_entry_completion(
                    staging_path,
                    cache_root,
                    component=component,
                    cache_key=cache_key,
                    cache_identity=cache_identity,
                )
            # Validate/build before removing an old final entry; a failed
            # staging build therefore leaves a known-good prior cache intact.
            for _, final_path in resolved_entries:
                if final_path.exists():
                    safe_remove_dir(final_path, cache_root)
            for component, final_path in resolved_entries:
                staging_path = staging_entries[component]
                assert staging_path is not None
                atomic_publish_dir(staging_path, final_path, cache_root, require_complete=True)
                staging_entries[component] = None

            published_record = dict(staged_record)
            published_record.update(
                status="built",
                prefix=str(prefix),
                expat_h=str(prefix / "include/expat.h"),
                include=str(prefix / "include/expat.h"),
                lib_dir=str(prefix / "lib"),
                library=str(prefix / "lib"),
                build_path=str(build_dir),
                build_source_copy=str(source_copy),
                manifest=str(prefix / "component-manifest.json"),
                tree=tree_manifest(prefix),
            )
            write_cache_manifest(prefix / "component-manifest.json", published_record)
            return published_record
    except TimeoutError as exc:
        record.update(status="blocked", blocker_reason="cache_lock_timeout", details=str(exc))
        return record
    except RuntimeError as exc:
        record.update(status="blocked", blocker_reason=str(exc))
        return record
    finally:
        for staging_path in staging_entries.values():
            if staging_path is not None and staging_path.exists():
                try:
                    safe_remove_dir(staging_path, cache_root)
                except RuntimeError:
                    pass


def prepare_expat(
    env: dict[str, str],
    cache_root: Path,
    build_root: Path,
    git_record: dict[str, Any],
    _transactional: bool = False,
) -> dict[str, Any]:
    try:
        cache_root = ensure_managed_cache_root(cache_root)
    except RuntimeError as exc:
        return {"name": "expat", "status": "blocked", "blocker_reason": str(exc)}
    prefix = Path(env.get("EXPAT_PREFIX", str(cache_root / "prefix/expat"))).resolve()
    build_dir = Path(env.get("EXPAT_BUILD_DIR", str(cache_root / "build/expat"))).resolve()
    build_source_copy = Path(env.get("EXPAT_SOURCE_COPY", str(cache_root / "build/expat-source"))).resolve()
    expat_h = prefix / "include/expat.h"
    lib_dir = prefix / "lib"
    log_path = build_root / "logs/runtime-components/expat-build.log"
    marker_path = prefix / "component-manifest.json"
    source_path = Path(git_record.get("path", "")).resolve() if git_record.get("path") else Path()
    expat_source = git_record.get("source") or git_record.get("url") or env.get("EXPAT_SOURCE_URL", "")
    record: dict[str, Any] = {
        "name": "expat",
        "source": expat_source,
        "url": git_record.get("url") or git_record.get("source") or expat_source,
        "expected_ref": git_record.get("expected_ref", ""),
        "release_tag": git_record.get("release_tag", git_record.get("expected_ref", "")),
        "actual_head": git_record.get("actual_head", ""),
        "recursive_submodules": True,
        "recursive_submodule_status": git_record.get("submodule_status", ""),
        "submodule_status_clean": git_record.get("submodule_status_clean", False),
        "git_fsck": git_record.get("git_fsck", ""),
        "path": str(source_path) if str(source_path) != "." else "",
        "prefix": str(prefix),
        "expat_h": str(expat_h),
        "include": str(expat_h),
        "lib_dir": str(lib_dir),
        "library": str(lib_dir),
        "build_path": str(build_dir),
        "build_source_copy": str(build_source_copy),
        "build_log": str(log_path),
        "status": "unknown",
        "blocker_reason": "",
    }
    build_flags = {
        key: env.get(key, "")
        for key in ("CC", "CXX", "CPPFLAGS", "CFLAGS", "CXXFLAGS", "LDFLAGS", "LIBS")
    }
    toolchain = toolchain_identity(env)
    cache_identity = canonical_cache_identity(
        "expat",
        env=env,
        upstream_url=str(record["url"]),
        upstream_version=str(record["release_tag"]),
        upstream_commit=str(record["actual_head"]),
        source_sha256=str(record["actual_head"]),
        patchset_sha256=patchset_identity([])["sha256"],
        configuration_flags=build_flags,
        toolchain=toolchain,
    )
    build_inputs = {
        "actual_head": record["actual_head"],
        "compiler": toolchain,
        "build_flags": build_flags,
        "cache_identity": cache_identity,
    }
    record["cache_schema_version"] = CACHE_SCHEMA_VERSION
    record["cache_identity"] = cache_identity
    record["cache_key"] = cache_identity["cache_key"]
    record["build_id"] = cache_identity["cache_key"]
    record["build_inputs"] = build_inputs
    if git_record.get("status") != "present":
        record.update(status="blocked", blocker_reason=git_record.get("blocker_reason") or "expat_source_unavailable")
        return record
    if is_system_path(prefix) or is_system_path(build_dir) or is_system_path(build_source_copy):
        record.update(status="blocked", blocker_reason="system_path_write_forbidden")
        return record
    if not is_within(prefix, cache_root) or not is_within(build_dir, cache_root) or not is_within(build_source_copy, cache_root):
        record.update(status="blocked", blocker_reason="expat_paths_must_be_under_connector_component_cache")
        return record
    explicit_override = any(env.get(key) for key in ("EXPAT_PREFIX", "EXPAT_BUILD_DIR", "EXPAT_SOURCE_COPY"))
    if not _transactional and explicit_override:
        return prepare_expat_managed_overrides(
            env,
            cache_root,
            build_root,
            git_record,
            record,
            prefix=prefix,
            build_dir=build_dir,
            source_copy=build_source_copy,
            cache_identity=cache_identity,
        )
    if not _transactional:
        entry_root = (cache_root / "builds/expat" / str(cache_identity["cache_key"])).resolve()
        final_prefix = entry_root / "prefix"
        final_build_dir = entry_root / "build"
        final_source_copy = entry_root / "source"
        final_manifest = entry_root / "manifest.json"
        record.update(
            prefix=str(final_prefix),
            expat_h=str(final_prefix / "include/expat.h"),
            include=str(final_prefix / "include/expat.h"),
            lib_dir=str(final_prefix / "lib"),
            library=str(final_prefix / "lib"),
            build_path=str(final_build_dir),
            build_source_copy=str(final_source_copy),
            manifest=str(final_manifest),
        )
        staging_root: Path | None = None
        try:
            with BuildLock(cache_entry_lock_path(cache_root, "expat", str(cache_identity["cache_key"]))):
                if (
                    expat_artifacts_ready(final_prefix)
                    and cache_manifest_complete(final_manifest, cache_identity)
                    and cache_entry_complete(
                        entry_root,
                        cache_root,
                        component="expat",
                        cache_key=str(cache_identity["cache_key"]),
                        cache_identity=cache_identity,
                    )
                ):
                    previous = read_json(final_manifest)
                    record.update(
                        status="present",
                        libraries=[str(path) for path in expat_libs(final_prefix / "lib")],
                        build_system=previous.get("build_system", ""),
                        tree=tree_manifest(final_prefix),
                    )
                    return record
                if entry_root.exists():
                    if not managed_cache_entry_valid(entry_root, cache_root):
                        if not migrate_legacy_cache_entry_for_removal(entry_root, cache_root, component="expat"):
                            record.update(status="blocked", blocker_reason=f"unmanaged_cache_entry_marker_missing: {entry_root}")
                            return record
                    safe_remove_dir(entry_root, cache_root)
                    record.update(rebuild_required=True, invalidation_reason="missing_or_incomplete_expat_cache", old_entry_removed=True)
                staging_root = temporary_cache_dir(
                    entry_root,
                    cache_root,
                    component="expat",
                    cache_key=str(cache_identity["cache_key"]),
                )
                staged_env = dict(env)
                staged_env.update(
                    EXPAT_PREFIX=str(staging_root / "prefix"),
                    EXPAT_BUILD_DIR=str(staging_root / "build"),
                    EXPAT_SOURCE_COPY=str(staging_root / "source"),
                )
                staged_record = prepare_expat(staged_env, cache_root, build_root, git_record, _transactional=True)
                if staged_record.get("status") != "built":
                    return rebase_cache_record(staged_record, staging_root, entry_root)
                published_record = rebase_cache_record(staged_record, staging_root, entry_root)
                published_record.update(
                    prefix=str(final_prefix),
                    expat_h=str(final_prefix / "include/expat.h"),
                    include=str(final_prefix / "include/expat.h"),
                    lib_dir=str(final_prefix / "lib"),
                    library=str(final_prefix / "lib"),
                    build_path=str(final_build_dir),
                    build_source_copy=str(final_source_copy),
                    manifest=str(final_manifest),
                    tree=tree_manifest(staging_root / "prefix"),
                )
                write_cache_manifest(staging_root / "manifest.json", published_record)
                write_cache_entry_completion(
                    staging_root,
                    cache_root,
                    component="expat",
                    cache_key=str(cache_identity["cache_key"]),
                    cache_identity=cache_identity,
                )
                for child in (staging_root / "build", staging_root / "source", staging_root / "prefix"):
                    remove_managed_cache_entry_marker(child, cache_root)
                atomic_publish_dir(staging_root, entry_root, cache_root, require_complete=True)
                staging_root = None
                published_record["tree"] = tree_manifest(final_prefix)
                write_cache_manifest(final_manifest, published_record)
                return published_record
        except TimeoutError as exc:
            record.update(status="blocked", blocker_reason="cache_lock_timeout", details=str(exc))
            return record
        finally:
            if staging_root is not None and staging_root.exists():
                try:
                    safe_remove_dir(staging_root, cache_root)
                except RuntimeError:
                    pass
    previous = read_json(marker_path)
    if (
        expat_artifacts_ready(prefix)
        and cache_manifest_complete(marker_path, cache_identity)
        and cache_entry_complete(
            prefix,
            cache_root,
            component="expat-prefix",
            cache_key=str(cache_identity["cache_key"]),
            cache_identity=cache_identity,
        )
    ):
        record.update(
            status="present",
            libraries=[str(path) for path in expat_libs(lib_dir)],
            build_system=previous.get("build_system", ""),
            tree=tree_manifest(prefix),
        )
        return record

    missing = first_missing_tool([("make", "missing_make")])
    compiler = resolve_compiler(env)
    if not compiler:
        missing = "missing_compiler"
    if missing:
        record.update(status="blocked", blocker_reason=missing)
        return record

    git_source_dir = expat_source_dir(source_path)
    record["git_source_dir"] = str(git_source_dir)
    has_autotools = (
        (git_source_dir / "buildconf.sh").is_file()
        or (git_source_dir / "configure").is_file()
        or (git_source_dir / "configure.ac").is_file()
    )
    has_cmake = (git_source_dir / "CMakeLists.txt").is_file()
    if has_autotools:
        if not (git_source_dir / "configure").is_file():
            missing = first_missing_tool(
                [
                    ("autoconf", "missing_autoconf"),
                    ("automake", "missing_automake"),
                    ("aclocal", "missing_automake"),
                    ("libtoolize", "missing_libtool"),
                ]
            )
            if missing:
                record.update(status="blocked", blocker_reason=missing)
                return record
        build_system = "autotools"
    elif has_cmake:
        if not shutil.which("cmake"):
            record.update(status="blocked", blocker_reason="missing_cmake")
            return record
        build_system = "cmake"
    else:
        record.update(status="blocked", blocker_reason="missing_expat_build_system")
        return record

    log_parts: list[str] = []
    build_env_vars = dict(os.environ)
    build_env_vars.update(env)
    build_env_vars["CC"] = env.get("CC", compiler)
    build_env_vars["PKG_CONFIG_PATH"] = f"{prefix / 'lib/pkgconfig'}{os.pathsep}{env.get('PKG_CONFIG_PATH', '')}".rstrip(os.pathsep)
    try:
        for label, cache_path in (
            ("expat-build", build_dir),
            ("expat-source", build_source_copy),
            ("expat-prefix", prefix),
        ):
            if cache_path.exists() and not managed_cache_entry_valid(cache_path, cache_root):
                if not migrate_legacy_cache_entry_for_removal(
                    cache_path,
                    cache_root,
                    component=label,
                ):
                    record.update(status="blocked", blocker_reason=f"unmanaged_cache_entry_marker_missing: {cache_path}")
                    return record
        safe_remove_dir(build_dir, cache_root)
        safe_remove_dir(build_source_copy, cache_root)
        safe_remove_dir(prefix, cache_root)
        for label, cache_path in (
            ("expat-build", build_dir),
            ("expat-source", build_source_copy),
            ("expat-prefix", prefix),
        ):
            mark_managed_cache_entry(
                cache_path,
                cache_root,
                component=label,
                cache_key=record["cache_key"],
            )
        shutil.copytree(
            git_source_dir,
            build_source_copy,
            ignore=shutil.ignore_patterns(".git", ".github", "autom4te.cache", "__pycache__"),
        )
        source_dir = build_source_copy
        mark_managed_cache_entry(
            build_source_copy,
            cache_root,
            component="expat-source",
            cache_key=record["cache_key"],
        )
        record["build_source_dir"] = str(source_dir)
        build_dir.mkdir(parents=True, exist_ok=True)
        mark_managed_cache_entry(
            build_dir,
            cache_root,
            component="expat-build",
            cache_key=record["cache_key"],
        )
        prefix.mkdir(parents=True, exist_ok=True)
        mark_managed_cache_entry(
            prefix,
            cache_root,
            component="expat-prefix",
            cache_key=record["cache_key"],
        )
        if build_system == "autotools":
            if (source_dir / "buildconf.sh").is_file():
                proc = run_env(["sh", str(source_dir / "buildconf.sh")], cwd=source_dir, env=build_env_vars)
                append_command_log(log_parts, "expat-buildconf", proc)
                if proc.returncode != 0:
                    write_component_log(log_path, log_parts)
                    record.update(status="failed", blocker_reason=map_expat_build_failure(proc.stdout + proc.stderr), build_exit_code=proc.returncode)
                    return record
            elif not (source_dir / "configure").is_file():
                proc = run_env(["autoreconf", "-fi"], cwd=source_dir, env=build_env_vars)
                append_command_log(log_parts, "expat-autoreconf", proc)
                if proc.returncode != 0:
                    write_component_log(log_path, log_parts)
                    record.update(status="failed", blocker_reason=map_expat_build_failure(proc.stdout + proc.stderr), build_exit_code=proc.returncode)
                    return record
            configure = source_dir / "configure"
            proc = run_env([str(configure), f"--prefix={prefix}"], cwd=build_dir, env=build_env_vars)
            append_command_log(log_parts, "expat-configure", proc)
            if proc.returncode != 0:
                write_component_log(log_path, log_parts)
                record.update(status="failed", blocker_reason=map_expat_build_failure(proc.stdout + proc.stderr), build_exit_code=proc.returncode)
                return record
            jobs = env.get("MAKE_JOBS") or str(os.cpu_count() or 2)
            for label, cmd in (
                ("expat-make", ["make", f"-j{jobs}"]),
                ("expat-make-install", ["make", "install"]),
            ):
                proc = run_env(cmd, cwd=build_dir, env=build_env_vars)
                append_command_log(log_parts, label, proc)
                if proc.returncode != 0:
                    write_component_log(log_path, log_parts)
                    record.update(status="failed", blocker_reason=map_expat_build_failure(proc.stdout + proc.stderr), build_exit_code=proc.returncode)
                    return record
        else:
            proc = run_env(
                [
                    "cmake",
                    "-S",
                    str(source_dir),
                    "-B",
                    str(build_dir),
                    f"-DCMAKE_INSTALL_PREFIX={prefix}",
                    "-DEXPAT_BUILD_TESTS=OFF",
                    "-DEXPAT_BUILD_EXAMPLES=OFF",
                    "-DEXPAT_BUILD_TOOLS=OFF",
                ],
                env=build_env_vars,
            )
            append_command_log(log_parts, "expat-cmake-configure", proc)
            if proc.returncode != 0:
                write_component_log(log_path, log_parts)
                record.update(status="failed", blocker_reason=map_expat_build_failure(proc.stdout + proc.stderr), build_exit_code=proc.returncode)
                return record
            for label, cmd in (
                ("expat-cmake-build", ["cmake", "--build", str(build_dir), "--parallel", env.get("MAKE_JOBS") or str(os.cpu_count() or 2)]),
                ("expat-cmake-install", ["cmake", "--install", str(build_dir)]),
            ):
                proc = run_env(cmd, env=build_env_vars)
                append_command_log(log_parts, label, proc)
                if proc.returncode != 0:
                    write_component_log(log_path, log_parts)
                    record.update(status="failed", blocker_reason=map_expat_build_failure(proc.stdout + proc.stderr), build_exit_code=proc.returncode)
                    return record
        write_component_log(log_path, log_parts)
    except Exception as exc:
        write_component_log(log_path, log_parts + [str(exc)])
        record.update(status="failed", blocker_reason=str(exc), build_exit_code=1)
        return record

    if not expat_artifacts_ready(prefix):
        record.update(status="failed", blocker_reason="expat_artifacts_missing", build_exit_code=0)
        return record
    record.update(
        status="built",
        build_system=build_system,
        libraries=[str(path) for path in expat_libs(lib_dir)],
        tree=tree_manifest(prefix),
        generated_at=utc_now(),
    )
    write_cache_manifest(marker_path, record)
    write_cache_entry_completion(
        prefix,
        cache_root,
        component="expat-prefix",
        cache_key=str(cache_identity["cache_key"]),
        cache_identity=cache_identity,
    )
    return record


def shared_modsecurity_paths(cache_root: Path, build_id: str) -> dict[str, Path]:
    return {
        "build_root": cache_root / "builds/modsecurity" / build_id,
        "prefix": cache_root / "prefix/modsecurity" / build_id,
        "manifest": cache_root / "builds/modsecurity" / build_id / "manifest.json",
        "lock": cache_root / "locks" / f"modsecurity-{build_id}.lock",
    }


def modsecurity_lib_file(prefix: Path) -> Path:
    return prefix / "lib/libmodsecurity.so"


def modsecurity_ready(prefix: Path) -> bool:
    return (prefix / "include/modsecurity/modsecurity.h").is_file() and modsecurity_lib_file(prefix).is_file()


def modsecurity_build_manifest_binds_prefix(
    build_root: Path,
    prefix: Path,
    cache_identity: dict[str, Any],
) -> bool:
    """Whether a complete build manifest explicitly owns this stale prefix.

    This is deliberately a deletion-only proof.  It lets recovery discard a
    prefix whose registry marker was lost, while never turning the build
    manifest into a cache-hit or post-hoc ownership marker for that prefix.
    """
    manifest_path = build_root / "manifest.json"
    if not cache_manifest_complete(manifest_path, cache_identity):
        return False
    manifest = read_json(manifest_path)
    try:
        return (
            Path(str(manifest.get("build_root", ""))).resolve(strict=False) == build_root.resolve(strict=False)
            and Path(str(manifest.get("prefix", ""))).resolve(strict=False) == prefix.resolve(strict=False)
        )
    except OSError:
        return False


def safe_remove_modsecurity_prefix_bound_by_build_manifest(
    prefix: Path,
    cache_root: Path,
    *,
    build_root: Path,
    cache_identity: dict[str, Any],
) -> None:
    """Remove only a prefix bound by a complete, current build manifest."""
    resolved_prefix, resolved_root = validate_managed_cache_child(prefix, cache_root)
    if not resolved_prefix.exists():
        return
    if cache_entry_marker_valid(resolved_prefix, resolved_root):
        safe_remove_dir(resolved_prefix, resolved_root)
        return
    if not modsecurity_build_manifest_binds_prefix(build_root, resolved_prefix, cache_identity):
        raise RuntimeError(f"unmanaged_cache_entry_marker_missing: {resolved_prefix}")
    shutil.rmtree(resolved_prefix)
    remove_managed_cache_entry_marker(resolved_prefix, resolved_root)


def modsecurity_build_inputs(
    env: dict[str, str],
    git_record: dict[str, Any],
    expat: dict[str, Any],
    connector_root: Path | None = None,
) -> dict[str, Any]:
    expat_prefix = str(expat.get("prefix", ""))
    expat_lib_dir = str(expat.get("lib_dir", ""))
    # Expat publishes a component-manifest below its prefix.  Its contents
    # contain timestamps and its own tree summary, so using a freshly walked
    # prefix tree here would make the ModSecurity cache key depend on cache
    # publication order.  Bind the dependency to Expat's immutable cache
    # identity instead.  This keeps standard and full-lifecycle invocations
    # on the same shared key while still invalidating ModSecurity whenever the
    # Expat source, patchset, toolchain, or build flags change.
    expat_cache_identity = expat.get("cache_identity")
    if isinstance(expat_cache_identity, dict) and expat_cache_identity:
        expat_dependency: dict[str, Any] = {
            "cache_identity": expat_cache_identity,
            "cache_key": str(
                expat.get("cache_key", expat_cache_identity.get("cache_key", ""))
            ),
            "prefix": expat_prefix,
        }
    else:
        # Keep the legacy fallback for callers which provide an external
        # dependency record without a Cache-v2 identity.  Such a record is not
        # used as a managed-cache hit, but its declared tree remains the best
        # available invalidation input.
        expat_dependency = {
            "actual_head": expat.get("actual_head", ""),
            "prefix": expat_prefix,
            "tree": expat.get("tree", {}),
        }
    dependency_payload = {
        "expat": expat_dependency,
        "pkg_config_path": env.get("PKG_CONFIG_PATH", ""),
        "ld_library_path": env.get("LD_LIBRARY_PATH", ""),
    }
    build_flags = {
        "configure_args": env.get("MODSECURITY_CONFIGURE_ARGS", ""),
        "CPPFLAGS": " ".join(part for part in (f"-I{Path(expat_prefix) / 'include'}" if expat_prefix else "", env.get("CPPFLAGS", "")) if part).strip(),
        "CFLAGS": env.get("CFLAGS", ""),
        "CXXFLAGS": env.get("CXXFLAGS", ""),
        "LDFLAGS": " ".join(part for part in (f"-L{expat_lib_dir}" if expat_lib_dir else "", env.get("LDFLAGS", "")) if part).strip(),
        "LIBS": env.get("LIBS", ""),
        "PKG_CONFIG_PATH": (
            f"{expat_prefix}/lib/pkgconfig{os.pathsep}{env.get('PKG_CONFIG_PATH', '')}".rstrip(os.pathsep)
            if expat_prefix
            else env.get("PKG_CONFIG_PATH", "")
        ),
    }
    dependency_hash = stable_hash(dependency_payload)
    toolchain = toolchain_identity(env)
    patchset = patchset_identity(component_patchset_roots(connector_root, "modsecurity"))
    cache_identity = canonical_cache_identity(
        "modsecurity",
        env=env,
        upstream_url=str(git_record.get("url", git_record.get("source", ""))),
        upstream_version=str(git_record.get("expected_ref", "")),
        upstream_commit=str(git_record.get("actual_head", "")),
        source_sha256=str(git_record.get("actual_head", "")),
        patchset_sha256=str(patchset["sha256"]),
        configuration_flags=build_flags,
        toolchain=toolchain,
        extra_inputs={
            "dependency_hash": dependency_hash,
            "recursive_submodule_status": git_record.get("submodule_status", ""),
        },
    )
    inputs = {
        "source_url": git_record.get("url", git_record.get("source", "")),
        "source_ref": git_record.get("expected_ref", ""),
        "actual_source_sha": git_record.get("actual_head", ""),
        "recursive_submodule_status": git_record.get("submodule_status", ""),
        "build_flags": build_flags,
        "compiler": toolchain,
        "dependency_hash": dependency_hash,
        "dependency_prefixes": dependency_payload,
        "patchset": patchset,
        "cache_schema_version": CACHE_SCHEMA_VERSION,
        "cache_identity": cache_identity,
        "cache_key": cache_identity["cache_key"],
    }
    inputs["build_id"] = cache_identity["cache_key"]
    inputs["build_flags_text"] = json.dumps(build_flags, sort_keys=True)
    inputs["dependency_hash"] = dependency_hash
    return inputs


class BuildLock:
    def __init__(self, lock_path: Path, timeout: int = 900) -> None:
        self.lock_path = lock_path
        self.timeout = timeout
        self.handle: Any = None
        self.mkdir_lock = lock_path.with_suffix(lock_path.suffix + ".dir")

    def __enter__(self) -> "BuildLock":
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            import fcntl  # type: ignore

            self.handle = self.lock_path.open("w", encoding="utf-8")
            deadline = time.time() + self.timeout
            while True:
                try:
                    fcntl.flock(self.handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    self.handle.write(f"pid={os.getpid()} acquired_at={utc_now()}\n")
                    self.handle.flush()
                    return self
                except BlockingIOError:
                    if time.time() > deadline:
                        raise TimeoutError(f"lock_timeout: {self.lock_path}")
                    time.sleep(1)
        except ImportError:
            deadline = time.time() + self.timeout
            while True:
                try:
                    self.mkdir_lock.mkdir()
                    (self.mkdir_lock / "owner").write_text(f"pid={os.getpid()} acquired_at={utc_now()}\n", encoding="utf-8")
                    return self
                except FileExistsError:
                    if time.time() > deadline:
                        raise TimeoutError(f"lock_timeout: {self.mkdir_lock}")
                    time.sleep(1)

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        if self.handle is not None:
            try:
                import fcntl  # type: ignore

                fcntl.flock(self.handle.fileno(), fcntl.LOCK_UN)
            finally:
                self.handle.close()
        if self.mkdir_lock.is_dir():
            # The fallback lock directory contains only the owner marker we
            # created; avoid a recursive removal primitive for lock cleanup.
            try:
                (self.mkdir_lock / "owner").unlink()
            except FileNotFoundError:
                pass
            try:
                self.mkdir_lock.rmdir()
            except OSError:
                pass


def cache_entry_lock_path(cache_root: Path, component: str, cache_key: str) -> Path:
    """Return a deterministic lock path for exactly one canonical entry."""
    safe_component = re.sub(r"[^A-Za-z0-9_.-]+", "-", component).strip("-") or "component"
    safe_key = stable_hash({"component": component, "cache_key": cache_key})[:24]
    return cache_root / "locks" / f"{safe_component}-{safe_key}.lock"


def copy_modsecurity_outputs(source_dir: Path, prefix: Path) -> None:
    headers = source_dir / "headers"
    libs = source_dir / "src/.libs"
    if not (headers / "modsecurity/modsecurity.h").is_file():
        raise RuntimeError("modsecurity_headers_missing_after_build")
    if not (libs / "libmodsecurity.so").is_file():
        raise RuntimeError("modsecurity_library_missing_after_build")
    include_dir = prefix / "include"
    lib_dir = prefix / "lib"
    include_dir.mkdir(parents=True, exist_ok=True)
    lib_dir.mkdir(parents=True, exist_ok=True)
    shutil.copytree(headers, include_dir, dirs_exist_ok=True, symlinks=True)
    for item in libs.glob("libmodsecurity.so*"):
        dest = lib_dir / item.name
        if dest.exists() or dest.is_symlink():
            dest.unlink()
        if item.is_symlink():
            os.symlink(os.readlink(item), dest)
        else:
            shutil.copy2(item, dest)


def prepare_shared_modsecurity(
    env: dict[str, str],
    cache_root: Path,
    build_root: Path,
    git_record: dict[str, Any],
    expat: dict[str, Any],
    connector_root: Path | None = None,
) -> dict[str, Any]:
    try:
        cache_root = ensure_managed_cache_root(cache_root)
    except RuntimeError as exc:
        return {"component": "modsecurity", "status": "blocked", "blocker_reason": str(exc)}
    inputs = modsecurity_build_inputs(env, git_record, expat, connector_root)
    build_id = inputs["build_id"]
    paths = shared_modsecurity_paths(cache_root, build_id)
    prefix = paths["prefix"]
    manifest_path = paths["manifest"]
    log_path = build_root / "logs/runtime-components" / f"modsecurity-{build_id[:16]}-build.log"
    source_path = Path(str(git_record.get("path", ""))).resolve() if git_record.get("path") else Path()
    record: dict[str, Any] = {
        "component": "modsecurity",
        "name": "modsecurity",
        "source_url": inputs["source_url"],
        "source_ref": inputs["source_ref"],
        "actual_sha": inputs["actual_source_sha"],
        "build_id": build_id,
        "prefix": str(prefix),
        "include_dir": str(prefix / "include"),
        "lib_dir": str(prefix / "lib"),
        "lib_file": str(modsecurity_lib_file(prefix)),
        "pkg_config_path": str(prefix / "lib/pkgconfig"),
        "submodules_recursive": True,
        "submodule_status": inputs["recursive_submodule_status"],
        "build_flags": inputs["build_flags_text"],
        "dependency_hash": inputs["dependency_hash"],
        "compiler": inputs["compiler"],
        "cache_schema_version": CACHE_SCHEMA_VERSION,
        "cache_identity": inputs["cache_identity"],
        "cache_key": inputs["cache_key"],
        "patchset_sha256": inputs["patchset"]["sha256"],
        "target_architecture": inputs["cache_identity"]["target_architecture"],
        "build_root": str(paths["build_root"]),
        "manifest": str(manifest_path),
        "lock": str(paths["lock"]),
        "status": "unknown",
        "blocker_reason": "",
    }
    for label, path in (("build_root", paths["build_root"]), ("prefix", prefix), ("lock", paths["lock"])):
        if is_system_path(path) or not is_within(path, cache_root):
            record.update(status="blocked", blocker_reason="system_path_write_forbidden", blocked_path=f"{label}:{path}")
            return record
    if paths["build_root"].exists() and not cache_entry_marker_valid(paths["build_root"], cache_root):
        # A complete local manifest is sufficient to safely discard a stale
        # entry, never to claim it or treat it as reusable cache state.
        if cache_manifest_owns_entry(paths["build_root"]):
            safe_remove_dir(paths["build_root"], cache_root)
            record.update(
                rebuild_required=True,
                invalidation_reason="missing_modsecurity_cache_registry_marker",
                old_entry_removed=True,
            )
        elif migrate_legacy_cache_entry_for_removal(
            paths["build_root"],
            cache_root,
            component="modsecurity-build",
        ):
            safe_remove_dir(paths["build_root"], cache_root)
            record.update(rebuild_required=True, invalidation_reason="cache_schema_changed", old_entry_removed=True)
        else:
            record.update(status="blocked", blocker_reason=f"unmanaged_cache_entry_marker_missing: {paths['build_root']}")
            return record
    try:
        # `manifest_path` lives below this entry.  Claim a fresh entry before
        # any early-return status can create that directory.  An existing
        # markerless local manifest was discarded above rather than claimed.
        mark_managed_cache_entry(
            paths["build_root"],
            cache_root,
            component="modsecurity-build",
            cache_key=inputs["cache_key"],
        )
    except RuntimeError as exc:
        record.update(status="blocked", blocker_reason=str(exc))
        return record
    if git_record.get("status") != "present":
        record.update(status="blocked", blocker_reason=git_record.get("blocker_reason") or "modsecurity_source_unavailable")
        write_cache_manifest(manifest_path, record)
        return record
    if not git_record.get("submodule_status_clean", False):
        record.update(status="blocked", blocker_reason="modsecurity_submodule_missing")
        write_cache_manifest(manifest_path, record)
        return record

    def reuse_if_ready(status: str) -> bool:
        if (
            modsecurity_ready(prefix)
            and cache_manifest_complete(manifest_path, inputs["cache_identity"])
            and cache_entry_complete(
                paths["build_root"],
                cache_root,
                component="modsecurity-build",
                cache_key=inputs["cache_key"],
                cache_identity=inputs["cache_identity"],
            )
            and cache_entry_complete(
                prefix,
                cache_root,
                component="modsecurity-prefix",
                cache_key=inputs["cache_key"],
                cache_identity=inputs["cache_identity"],
            )
        ):
            record.update(status=status, tree=tree_manifest(prefix), generated_at=utc_now())
            write_cache_manifest(manifest_path, record)
            return True
        return False

    try:
        with BuildLock(paths["lock"]):
            if reuse_if_ready("reused"):
                return record
            missing = first_missing_tool([("make", "missing_make"), ("git", "missing_git")])
            compiler = resolve_compiler(env)
            if not compiler:
                missing = "missing_compiler"
            if missing:
                record.update(status="blocked", blocker_reason="missing_modsecurity_dependency", missing_dependency=missing)
                write_cache_manifest(manifest_path, record)
                return record
            for label, cache_path, component in (
                ("modsecurity-build", paths["build_root"], "modsecurity-build"),
                ("modsecurity-prefix", prefix, "modsecurity-prefix"),
            ):
                if cache_path.exists() and not managed_cache_entry_valid(cache_path, cache_root):
                    if label == "modsecurity-prefix" and modsecurity_build_manifest_binds_prefix(
                        paths["build_root"],
                        prefix,
                        inputs["cache_identity"],
                    ):
                        # The bound build manifest grants deletion only.  Do
                        # not re-claim this markerless prefix; discard it and
                        # create a fresh staged entry below.
                        safe_remove_modsecurity_prefix_bound_by_build_manifest(
                            prefix,
                            cache_root,
                            build_root=paths["build_root"],
                            cache_identity=inputs["cache_identity"],
                        )
                        record.update(
                            rebuild_required=True,
                            invalidation_reason="missing_modsecurity_prefix_registry_marker",
                            old_entry_removed=True,
                        )
                        continue
                    if not migrate_legacy_cache_entry_for_removal(
                        cache_path,
                        cache_root,
                        component=component,
                    ):
                        record.update(status="blocked", blocker_reason=f"unmanaged_cache_entry_marker_missing: {cache_path}")
                        return record
            safe_remove_dir(paths["build_root"], cache_root)
            safe_remove_dir(prefix, cache_root)
            staging_build = temporary_cache_dir(
                paths["build_root"],
                cache_root,
                component="modsecurity-build",
                cache_key=inputs["cache_key"],
            )
            staging_prefix = temporary_cache_dir(
                prefix,
                cache_root,
                component="modsecurity-prefix",
                cache_key=inputs["cache_key"],
            )
            try:
                build_source = staging_build / "source"
                shutil.copytree(
                    source_path,
                    build_source,
                    ignore=shutil.ignore_patterns(".git", ".github", "__pycache__", "autom4te.cache", "*.o", "*.lo", "*.la", "*.log"),
                )
                build_env_vars = dict(os.environ)
                build_env_vars.update(env)
                flag_payload = json.loads(inputs["build_flags_text"])
                for key in ("CPPFLAGS", "CFLAGS", "CXXFLAGS", "LDFLAGS", "LIBS", "PKG_CONFIG_PATH"):
                    if flag_payload.get(key):
                        build_env_vars[key] = str(flag_payload[key])
                if expat.get("lib_dir"):
                    build_env_vars["LD_LIBRARY_PATH"] = f"{expat.get('lib_dir')}{os.pathsep}{env.get('LD_LIBRARY_PATH', '')}".rstrip(os.pathsep)
                log_parts: list[str] = []
                configure_cmd = ["./configure", f"--prefix={staging_prefix}"]
                configure_cmd.extend(env.get("MODSECURITY_CONFIGURE_ARGS", "").split())
                commands: list[tuple[str, list[str]]] = [
                    ("modsecurity-build-sh", ["sh", "./build.sh"]),
                    ("modsecurity-configure", configure_cmd),
                    ("modsecurity-make", ["make", f"-j{env.get('MAKE_JOBS') or str(os.cpu_count() or 2)}"]),
                ]
                for label, cmd in commands:
                    proc = run_env(cmd, cwd=build_source, env=build_env_vars)
                    append_command_log(log_parts, label, proc)
                    if proc.returncode != 0:
                        write_component_log(log_path, log_parts)
                        record.update(status="failed", blocker_reason="modsecurity_build_failed", build_exit_code=proc.returncode, build_log=str(log_path))
                        write_cache_manifest(staging_build / "manifest.json", record)
                        return record
                copy_modsecurity_outputs(build_source, staging_prefix)
                write_component_log(log_path, log_parts)
                if not modsecurity_ready(staging_prefix):
                    record.update(status="failed", blocker_reason="modsecurity_build_failed", build_exit_code=0, build_log=str(log_path))
                    write_cache_manifest(staging_build / "manifest.json", record)
                    return record
                record.update(status="built", build_log=str(log_path), tree=tree_manifest(staging_prefix), generated_at=utc_now())
                write_cache_manifest(staging_build / "manifest.json", record)
                write_cache_entry_completion(
                    staging_build,
                    cache_root,
                    component="modsecurity-build",
                    cache_key=inputs["cache_key"],
                    cache_identity=inputs["cache_identity"],
                )
                write_cache_entry_completion(
                    staging_prefix,
                    cache_root,
                    component="modsecurity-prefix",
                    cache_key=inputs["cache_key"],
                    cache_identity=inputs["cache_identity"],
                )
                atomic_publish_dir(staging_prefix, prefix, cache_root, require_complete=True)
                staging_prefix = None
                atomic_publish_dir(staging_build, paths["build_root"], cache_root, require_complete=True)
                staging_build = None
                record.update(tree=tree_manifest(prefix), generated_at=utc_now())
                write_cache_manifest(manifest_path, record)
                return record
            finally:
                if staging_build is not None and staging_build.exists():
                    try:
                        safe_remove_dir(staging_build, cache_root)
                    except RuntimeError:
                        pass
                if staging_prefix is not None and staging_prefix.exists():
                    try:
                        safe_remove_dir(staging_prefix, cache_root)
                    except RuntimeError:
                        pass
    except TimeoutError as exc:
        record.update(status="blocked", blocker_reason="cache_lock_timeout", details=str(exc), build_log=str(log_path))
        write_cache_manifest(manifest_path, record)
        return record
    except Exception as exc:
        write_component_log(log_path, [str(exc)])
        record.update(status="failed", blocker_reason="modsecurity_build_failed", details=str(exc), build_exit_code=1, build_log=str(log_path))
        write_cache_manifest(manifest_path, record)
        return record


def connector_input_paths(connector_root: Path, framework_root: Path, connector: str) -> list[Path]:
    common_paths = [connector_root / "common/include", connector_root / "common/src"]
    framework_script = {
        "apache": framework_root / "ci/prepare-apache-build.sh",
        "nginx": framework_root / "ci/prepare-nginx-build.sh",
        "haproxy": framework_root / "ci/prepare-haproxy-runtime.sh",
    }.get(connector)
    paths = [connector_root / "connectors" / connector, *common_paths]
    if framework_script:
        paths.append(framework_script)
    return paths


def connector_plan(
    connector_root: Path,
    framework_root: Path,
    cache_root: Path,
    env: dict[str, str],
    connector: str,
    modsecurity: dict[str, Any],
    expat: dict[str, Any],
    archives: list[dict[str, Any]],
) -> dict[str, Any]:
    source_paths = connector_input_paths(connector_root, framework_root, connector)
    source_hash = hash_input_paths(source_paths)
    patchset = patchset_identity(component_patchset_roots(connector_root, connector))
    build_flags = {
        key: env.get(key, "")
        for key in (
            "CPPFLAGS",
            "CFLAGS",
            "CXXFLAGS",
            "LDFLAGS",
            "LIBS",
            "HTTPD_VERSION",
            "HTTPD_SOURCE_URL",
            "HTTPD_SHA256",
            "APR_VERSION",
            "APR_SOURCE_URL",
            "APR_SHA256",
            "APR_UTIL_VERSION",
            "APR_UTIL_SOURCE_URL",
            "APR_UTIL_SHA256",
            "PCRE2_VERSION",
            "PCRE2_SOURCE_URL",
            "PCRE2_SHA256",
            "NGINX_RELEASE_TAG",
            "NGINX_SOURCE_GIT_REF",
            "NGINX_SOURCE_REPO_URL",
            "NGINX_SHA256",
            "HAPROXY_VERSION",
            "HAPROXY_SOURCE_URL",
            "HAPROXY_SHA256",
        )
    }
    archive_names = {
        "apache": {"httpd", "apr", "apr-util", "pcre2"},
        "nginx": {"nginx"},
        "haproxy": {"haproxy"},
    }[connector]
    archive_inputs = {
        str(item.get("name")): {
            key: item.get(key, "")
            for key in ("url", "sha256", "expected_sha256", "resolved_tag", "checksum_status")
        }
        for item in archives
        if isinstance(item, dict) and item.get("name") in archive_names
    }
    toolchain = toolchain_identity(env)
    archive_source_hash = stable_hash(archive_inputs)
    upstream_version = (
        env.get("HTTPD_VERSION", "")
        if connector == "apache"
        else env.get("NGINX_RELEASE_TAG", "") or env.get("NGINX_SOURCE_GIT_REF", "")
        if connector == "nginx"
        else env.get("HAPROXY_VERSION", "")
    )
    upstream_url = (
        env.get("HTTPD_SOURCE_URL", "")
        if connector == "apache"
        else env.get("NGINX_SOURCE_REPO_URL", "")
        if connector == "nginx"
        else env.get("HAPROXY_SOURCE_URL", "")
    )
    upstream_commit = env.get("NGINX_SOURCE_GIT_REF", "") if connector == "nginx" else ""
    cache_identity = canonical_cache_identity(
        connector,
        env=env,
        upstream_url=upstream_url,
        upstream_version=upstream_version,
        upstream_commit=upstream_commit,
        source_sha256=archive_source_hash,
        patchset_sha256=str(patchset["sha256"]),
        configuration_flags=build_flags,
        toolchain=toolchain,
        extra_inputs={
            "archives": archive_inputs,
            "archive_source_hash": archive_source_hash,
            "connector_source_hash": source_hash,
            "modsecurity_build_id": modsecurity.get("build_id", ""),
            "expat_build_id": expat.get("build_id", ""),
            "connector_commit": git_revision(connector_root),
            "framework_commit": git_revision(framework_root),
        },
    )
    payload = {
        "connector": connector,
        "source_hash": source_hash,
        "build_flags": build_flags,
        "compiler": toolchain,
        "archives": archive_inputs,
        "modsecurity_build_id": modsecurity.get("build_id", ""),
        "dependency_prefixes": {
            "modsecurity_prefix": modsecurity.get("prefix", ""),
            "expat_prefix": expat.get("prefix", ""),
            "expat_build_id": expat.get("build_id", ""),
        },
        "patchset": patchset,
        "cache_schema_version": CACHE_SCHEMA_VERSION,
        "cache_identity": cache_identity,
    }
    build_id = cache_identity["cache_key"]
    root = cache_root / "builds/connectors" / connector / build_id
    plan = {
        "connector": connector,
        "connector_build_id": build_id,
        "modsecurity_build_id": modsecurity.get("build_id", ""),
        "source_hash": source_hash,
        "source_inputs": [str(path) for path in source_paths],
        "build_flags": json.dumps(build_flags, sort_keys=True),
        "compiler": payload["compiler"],
        "archive_inputs": archive_inputs,
        "cache_schema_version": CACHE_SCHEMA_VERSION,
        "cache_identity": cache_identity,
        "cache_key": cache_identity["cache_key"],
        "patchset_sha256": patchset["sha256"],
        "patchset_files": patchset["files"],
        "target_architecture": cache_identity["target_architecture"],
        "cache_root": str(cache_root),
        "root": str(root),
        "manifest": str(root / "manifest.json"),
        "status": "unknown",
        "blocker_reason": "",
    }
    if connector == "apache":
        plan["build_root"] = str(root / "build")
        plan["httpd_prefix"] = str(root / "httpd")
        plan["output_paths"] = {
            "binary": str(root / "httpd/bin/httpd"),
            "module": str(root / "build/output/apache/mod_security3.so"),
            "config": str(root / "httpd/conf/httpd.conf"),
        }
    elif connector == "nginx":
        plan["build_root"] = str(root / "build")
        plan["nginx_prefix"] = str(root / "nginx")
        plan["output_paths"] = {
            "binary": str(root / "nginx/sbin/nginx"),
            "module": str(root / "nginx/modules/ngx_http_modsecurity_module.so"),
            "config": str(root / "nginx/conf/nginx.conf"),
        }
    elif connector == "haproxy":
        plan["build_root"] = str(root)
        plan["output_paths"] = {
            "binary": str(root / "haproxy-runtime/haproxy/sbin/haproxy"),
            "module": str(root / "haproxy-spoa-runtime/haproxy-modsecurity-spoa"),
            "config": str(root / "haproxy-modsecurity-binding/paths.env"),
        }
    return reuse_connector_cache_entry_if_only_commit_changed(plan)


def connector_manifest_contract_ready(plan: dict[str, Any]) -> bool:
    """Validate the local connector manifest, without treating it as a hit."""
    manifest_path = Path(str(plan.get("manifest", "")))
    identity = plan.get("cache_identity")
    if not isinstance(identity, dict) or not cache_manifest_complete(manifest_path, identity):
        return False
    manifest = read_json(manifest_path)
    return (
        manifest.get("connector_build_id") == plan.get("connector_build_id")
        and manifest.get("modsecurity_build_id") == plan.get("modsecurity_build_id")
        and manifest.get("source_hash") == plan.get("source_hash")
    )


def connector_manifest_ready(plan: dict[str, Any]) -> bool:
    """A connector cache hit additionally requires registry completion."""
    if not connector_manifest_contract_ready(plan):
        return False
    cache_root_value = plan.get("cache_root")
    root_value = plan.get("root")
    cache_key = plan.get("cache_key", plan.get("connector_build_id", ""))
    identity = plan.get("cache_identity")
    if (
        not isinstance(cache_root_value, str)
        or not cache_root_value
        or not isinstance(root_value, str)
        or not root_value
        or not isinstance(cache_key, str)
        or not cache_key
        or not isinstance(identity, dict)
    ):
        return False
    try:
        return cache_entry_complete(
            Path(root_value),
            Path(cache_root_value),
            component=f"connector:{plan.get('connector', 'unknown')}",
            cache_key=cache_key,
            cache_identity=identity,
        )
    except OSError:
        return False


def write_connector_manifest(plan: dict[str, Any], record: dict[str, Any]) -> None:
    cache_root_value = plan.get("cache_root")
    root_value = plan.get("root")
    if isinstance(cache_root_value, str) and cache_root_value and isinstance(root_value, str) and root_value:
        cache_root = Path(cache_root_value)
        root = Path(root_value)
        try:
            # Claim a planned, absent root before `write_json` creates it.  If
            # it already exists, it must already be marker- or
            # complete-manifest-owned; never bless an arbitrary cache child.
            mark_managed_cache_entry(
                root,
                cache_root,
                component=f"connector:{plan.get('connector', 'unknown')}",
                cache_key=str(plan.get("cache_key", "")),
            )
        except RuntimeError:
            return
    manifest = dict(plan)
    manifest.pop("root", None)
    manifest.update(
        status=record.get("status", "blocked"),
        blocker_reason=record.get("blocker_reason", ""),
        invalidation_reason=record.get("invalidation_reason", ""),
        output_paths=record.get("output_paths", plan.get("output_paths", {})),
        generated_at=utc_now(),
    )
    write_cache_manifest(Path(str(plan["manifest"])), manifest)


def go_main_packages(source_path: Path, env: dict[str, str], log_parts: list[str]) -> tuple[list[str], subprocess.CompletedProcess[str]]:
    proc = run_env(
        ["go", "list", "-mod=readonly", "-f", "{{if eq .Name \"main\"}}{{.ImportPath}}{{end}}", "./..."],
        cwd=source_path,
        env=env,
    )
    append_command_log(log_parts, "go-list-main-packages", proc)
    packages = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    return packages, proc


def prepare_go_tool(
    dependency: str,
    env_var: str,
    cache_root: Path,
    build_root: Path,
    git_record: dict[str, Any],
    optional: bool = False,
) -> dict[str, Any]:
    env = dict(os.environ)
    try:
        cache_root = ensure_managed_cache_root(cache_root)
    except RuntimeError as exc:
        return {
            "dependency": dependency,
            "name": dependency,
            "status": "blocked_optional" if optional else "blocked",
            "blocker_reason": str(exc),
            "optional": optional,
        }
    log_path = build_root / f"logs/runtime-components/{dependency}-build.log"
    source_path = Path(git_record.get("path", "")).resolve() if git_record.get("path") else Path()
    record: dict[str, Any] = {
        "dependency": dependency,
        "name": dependency,
        "source": git_record.get("source", git_record.get("url", "")),
        "known_source": git_record.get("source", git_record.get("url", "")),
        "known_source_url": git_record.get("source", git_record.get("url", "")),
        "expected_ref": git_record.get("expected_ref", ""),
        "known_ref": git_record.get("expected_ref", ""),
        "release_tag": git_record.get("release_tag", git_record.get("expected_ref", "")),
        "release_url": git_record.get("release_url", ""),
        "expected_prompt_latest": git_record.get("expected_prompt_latest", ""),
        "release_tag_deviation": git_record.get("release_tag_deviation", False),
        "release_tag_deviation_note": git_record.get("release_tag_deviation_note", ""),
        "actual_head": git_record.get("actual_head", ""),
        "recursive_submodules": True,
        "recursive_submodule_status": git_record.get("submodule_status", ""),
        "submodule_status_clean": git_record.get("submodule_status_clean", False),
        "git_fsck": git_record.get("git_fsck", ""),
        "path": "",
        "binary": "",
        "source_path": str(source_path) if str(source_path) != "." else "",
        "searched_paths": [],
        "env_override": env_var,
        "can_build_locally": True,
        "build_log": str(log_path),
        "status": "unknown",
        "blocker_reason": "",
        "optional": optional,
    }
    def block(reason: str, **extra: Any) -> dict[str, Any]:
        record.update(status="blocked_optional" if optional else "blocked", blocker_reason=reason, **extra)
        return record

    if git_record.get("status") != "present":
        return block(git_record.get("blocker_reason") or f"{dependency}_source_unavailable")
    go_bin = shutil.which("go")
    if not go_bin:
        return block("missing_go")
    go_toolchain = toolchain_identity(env)
    go_toolchain["go"] = command_text([go_bin, "version"], env=env)
    cache_identity = canonical_cache_identity(
        dependency,
        env=env,
        upstream_url=str(record["source"]),
        upstream_version=str(record["release_tag"]),
        upstream_commit=str(record["actual_head"]),
        source_sha256=str(record["actual_head"]),
        patchset_sha256=patchset_identity([])["sha256"],
        configuration_flags={"go_build_flags": "-trimpath -mod=readonly"},
        toolchain=go_toolchain,
    )
    record.update(
        cache_schema_version=CACHE_SCHEMA_VERSION,
        cache_identity=cache_identity,
        cache_key=cache_identity["cache_key"],
    )
    entry_root = (cache_root / "builds/go" / dependency / str(cache_identity["cache_key"])).resolve()
    binary_path = entry_root / "bin" / dependency
    manifest_path = entry_root / "manifest.json"
    if is_system_path(entry_root) or not is_within(entry_root, cache_root):
        return block("system_path_write_forbidden")
    record.update(
        path=str(binary_path),
        binary=str(binary_path),
        searched_paths=[str(binary_path)],
        build_path=str(entry_root),
        manifest=str(manifest_path),
    )
    staging_path: Path | None = None
    try:
        with BuildLock(cache_entry_lock_path(cache_root, f"go-{dependency}", str(cache_identity["cache_key"]))):
            previous = read_json(manifest_path)
            if (
                executable(binary_path)
                and cache_manifest_complete(manifest_path, cache_identity)
                and cache_entry_complete(
                    entry_root,
                    cache_root,
                    component=f"go:{dependency}",
                    cache_key=str(cache_identity["cache_key"]),
                    cache_identity=cache_identity,
                )
            ):
                record.update(
                    status="present",
                    build_package=previous.get("build_package", ""),
                    go_version=previous.get("go_version", ""),
                )
                return record
            if entry_root.exists():
                if not managed_cache_entry_valid(entry_root, cache_root):
                    if not migrate_legacy_cache_entry_for_removal(
                        entry_root,
                        cache_root,
                        component=f"go:{dependency}",
                    ):
                        return block(f"unmanaged_cache_entry_marker_missing: {entry_root}")
                    record.update(
                        rebuild_required=True,
                        invalidation_reason="cache_schema_changed",
                        old_entry_removed=True,
                    )
                safe_remove_dir(entry_root, cache_root)
                record.setdefault("rebuild_required", True)
                record.setdefault("invalidation_reason", "missing_or_incomplete_go_cache")
                record.setdefault("old_entry_removed", True)
            staging_path = temporary_cache_dir(
                entry_root,
                cache_root,
                component=f"go:{dependency}",
                cache_key=str(cache_identity["cache_key"]),
            )
            staging_binary = staging_path / "bin" / dependency
            staging_manifest = staging_path / "manifest.json"
            build_env_vars = local_build_env(os.environ, cache_root)
            build_env_vars["PATH"] = os.environ.get("PATH", "")
            log_parts: list[str] = []
            version_proc = run_env(["go", "version"], env=build_env_vars)
            append_command_log(log_parts, "go-version", version_proc)
            packages, list_proc = go_main_packages(source_path, build_env_vars, log_parts)
            if list_proc.returncode != 0:
                write_component_log(log_path, log_parts)
                return block("go_list_failed", build_exit_code=list_proc.returncode)
            if not packages:
                write_component_log(log_path, log_parts)
                return block("go_main_package_not_found")
            if len(packages) > 1:
                write_component_log(log_path, log_parts)
                return block("go_multiple_main_packages", main_packages=packages)
            build_package = packages[0]
            staging_binary.parent.mkdir(parents=True, exist_ok=True)
            proc = run_env(
                ["go", "build", "-trimpath", "-mod=readonly", "-o", str(staging_binary), build_package],
                cwd=source_path,
                env=build_env_vars,
            )
            append_command_log(log_parts, "go-build", proc)
            write_component_log(log_path, log_parts)
            if proc.returncode != 0:
                return block("go_build_failed", build_exit_code=proc.returncode)
            if not executable(staging_binary):
                return block("go_binary_missing_after_build")
            staged_record = dict(record)
            staged_record.update(
                status="built",
                build_package=build_package,
                go_version=version_proc.stdout.strip(),
                tree=tree_manifest(staging_path),
                generated_at=utc_now(),
            )
            write_cache_manifest(staging_manifest, staged_record)
            write_cache_entry_completion(
                staging_path,
                cache_root,
                component=f"go:{dependency}",
                cache_key=str(cache_identity["cache_key"]),
                cache_identity=cache_identity,
            )
            atomic_publish_dir(staging_path, entry_root, cache_root, require_complete=True)
            staging_path = None
            record.update(
                status="built",
                build_package=build_package,
                go_version=version_proc.stdout.strip(),
                tree=tree_manifest(entry_root),
                generated_at=utc_now(),
            )
            return record
    except TimeoutError as exc:
        return block("cache_lock_timeout", details=str(exc))
    finally:
        if staging_path is not None and staging_path.exists():
            try:
                safe_remove_dir(staging_path, cache_root)
            except RuntimeError:
                pass


def map_apache_blocker(text: str, missing: list[str]) -> str:
    lowered = text.lower()
    if "undefined reference to `crypt" in lowered or "undefined reference to 'crypt" in lowered:
        return "missing_crypt_library"
    if "expat.h" in lowered or "expat" in lowered and "header" in lowered:
        return "missing_expat_headers"
    if "missing required command" in lowered or "not found" in lowered:
        return "missing_apache_build_dependency"
    if any(item.startswith("modsecurity_lib:") for item in missing) or "libmodsecurity" in lowered:
        return "missing_libmodsecurity_build"
    return "missing_local_httpd_build"


def map_nginx_blocker(text: str, missing: list[str]) -> str:
    lowered = text.lower()
    if any(item.startswith("module_file:") for item in missing):
        return "missing_nginx_modsecurity_module"
    if any(item.startswith("modsecurity_lib:") for item in missing) or "libmodsecurity" in lowered:
        return "missing_libmodsecurity_build"
    if "missing required command" in lowered or "not found" in lowered:
        return "missing_nginx_build_dependency"
    return "missing_local_nginx_build"


def apache_apxs_includedir_usable(httpd_prefix: Path) -> bool:
    """Return whether an installed Apache ``apxs`` resolves its include dir.

    Merely checking that the generated Perl script is executable is not
    enough: it can still point at the vanished atomic staging directory.  The
    query is deliberately narrow, side-effect free, and also verifies that
    the reported directory belongs to the published prefix.
    """
    prefix = httpd_prefix.resolve(strict=False)
    apxs_bin = prefix / "bin/apxs"
    expected_include = prefix / "include"
    if not executable(apxs_bin) or not expected_include.is_dir():
        return False
    try:
        proc = subprocess.run(
            [str(apxs_bin), "-q", "INCLUDEDIR"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return proc.returncode == 0 and proc.stdout.strip() == str(expected_include)


def apache_install_text_paths(httpd_prefix: Path) -> list[Path]:
    """Return the installed Apache text files allowed to carry its prefix."""
    paths = [httpd_prefix / relative for relative in APACHE_INSTALL_TEXT_PATHS]
    config_root = httpd_prefix / "conf"
    if config_root.is_dir() and not config_root.is_symlink():
        paths.extend(sorted(config_root.rglob("*.conf")))
    return paths


def rebase_apache_install_text_paths_for_publish(
    staged_plan: dict[str, Any],
    final_root: Path,
) -> None:
    """Rebase known Apache install text files before atomically publishing.

    httpd's installed ``apxs`` and its configuration helpers contain absolute
    paths to the configured prefix.  Cache-v2 builds that prefix below a
    temporary sibling directory, then renames the complete tree.  Rewrite
    only the allowlisted text artifacts here; linked executables and modules
    are intentionally left byte-for-byte untouched.
    """
    root_value = staged_plan.get("root")
    prefix_value = staged_plan.get("httpd_prefix")
    if (
        not isinstance(root_value, str)
        or not root_value
        or not isinstance(prefix_value, str)
        or not prefix_value
    ):
        raise RuntimeError("apache_publication_paths_missing")
    staging_root = Path(root_value).resolve()
    staging_prefix = Path(prefix_value).resolve()
    published_root = final_root.resolve(strict=False)
    if not is_within(staging_prefix, staging_root):
        raise RuntimeError(f"apache_publication_prefix_outside_staging_root: {staging_prefix}")
    if not staging_prefix.is_dir() or staging_prefix.is_symlink():
        raise RuntimeError(f"apache_publication_prefix_missing: {staging_prefix}")

    staging_bytes = os.fsencode(str(staging_root))
    published_bytes = os.fsencode(str(published_root))
    for path in apache_install_text_paths(staging_prefix):
        if not path.exists():
            continue
        if path.is_symlink() or not path.is_file():
            raise RuntimeError(f"apache_publication_text_path_invalid: {path}")
        content = path.read_bytes()
        if staging_bytes not in content:
            continue
        if b"\0" in content:
            raise RuntimeError(f"apache_publication_text_path_contains_nul: {path}")
        mode = path.stat().st_mode & 0o777
        atomic_write_bytes(path, content.replace(staging_bytes, published_bytes))
        path.chmod(mode)

    # These are the two files required for `apxs -q INCLUDEDIR`; ensure a
    # staging reference can never reach the final cache entry unnoticed.
    for relative in ("bin/apxs", "build/config_vars.mk"):
        path = staging_prefix / relative
        if path.is_symlink() or not path.is_file():
            raise RuntimeError(f"apache_publication_required_text_path_missing: {path}")
        if staging_bytes in path.read_bytes():
            raise RuntimeError(f"apache_publication_staging_reference_remaining: {path}")


def connector_cache_entry_complete(plan: dict[str, Any]) -> bool:
    """A connector entry is a hit only with its manifest and declared outputs."""
    if not connector_manifest_ready(plan):
        return False
    output_paths = plan.get("output_paths")
    if not isinstance(output_paths, dict):
        return False
    for name, raw_path in output_paths.items():
        if not isinstance(raw_path, str) or not raw_path:
            return False
        path = Path(raw_path)
        if name == "binary":
            if not executable(path):
                return False
        elif not path.is_file():
            return False
    if plan.get("connector") == "apache":
        httpd_prefix = plan.get("httpd_prefix")
        if (
            not isinstance(httpd_prefix, str)
            or not httpd_prefix
            or not apache_apxs_includedir_usable(Path(httpd_prefix))
        ):
            return False
    return True


def cache_identity_is_self_consistent(identity: Any) -> bool:
    """Return whether a cache identity still hashes to its declared key."""
    if not isinstance(identity, dict):
        return False
    cache_key = identity.get("cache_key")
    if not isinstance(cache_key, str) or not cache_key:
        return False
    if identity.get("cache_schema_version") != CACHE_SCHEMA_VERSION:
        return False
    payload = dict(identity)
    payload.pop("cache_key", None)
    return stable_hash(payload) == cache_key


def connector_cache_identity_equivalent_ignoring_connector_commit(
    candidate: Any,
    requested: Any,
) -> bool:
    """Compare all connector build inputs except a differing root revision.

    ``connector_commit`` is deliberately a broad provenance input.  A
    top-level runner-only change should not force a source download and host
    rebuild when every connector build input below remains byte-for-byte the
    same.  This compatibility comparison is intentionally narrow: both
    identities must validate their own keys, both commits must be present and
    different, and every other field stays part of the equality check.
    """
    if not cache_identity_is_self_consistent(candidate) or not cache_identity_is_self_consistent(requested):
        return False
    try:
        candidate_payload = json.loads(json.dumps(candidate, sort_keys=True))
        requested_payload = json.loads(json.dumps(requested, sort_keys=True))
    except (TypeError, ValueError):
        return False
    candidate_payload.pop("cache_key", None)
    requested_payload.pop("cache_key", None)
    candidate_inputs = candidate_payload.get("extra_inputs")
    requested_inputs = requested_payload.get("extra_inputs")
    if not isinstance(candidate_inputs, dict) or not isinstance(requested_inputs, dict):
        return False
    candidate_commit = candidate_inputs.pop("connector_commit", "")
    requested_commit = requested_inputs.pop("connector_commit", "")
    return (
        isinstance(candidate_commit, str)
        and bool(candidate_commit)
        and isinstance(requested_commit, str)
        and bool(requested_commit)
        and candidate_commit != requested_commit
        and candidate_payload == requested_payload
    )


def reuse_connector_cache_entry_if_only_commit_changed(plan: dict[str, Any]) -> dict[str, Any]:
    """Adopt one complete managed connector entry with matching scoped inputs.

    This is read-only cache discovery.  It never marks, repairs, removes, or
    trusts an entry solely because its directory exists.  The adopted plan
    uses the current canonical layout rebased to the candidate root instead
    of accepting output paths embedded in a cache manifest.
    """
    connector = plan.get("connector")
    cache_root_value = plan.get("cache_root")
    requested_identity = plan.get("cache_identity")
    requested_key = plan.get("cache_key")
    if (
        not isinstance(connector, str)
        or not connector
        or not isinstance(cache_root_value, str)
        or not cache_root_value
        or not isinstance(requested_key, str)
        or not requested_key
        or not cache_identity_is_self_consistent(requested_identity)
    ):
        return plan
    cache_root = Path(cache_root_value)
    if not cache_root_marker_valid(cache_root):
        return plan
    candidate_parent = cache_root / "builds" / "connectors" / connector
    try:
        candidates = sorted(candidate_parent.iterdir(), key=lambda path: path.name)
    except OSError:
        return plan
    requested_inputs = requested_identity.get("extra_inputs")
    requested_commit = (
        str(requested_inputs.get("connector_commit", "")) if isinstance(requested_inputs, dict) else ""
    )
    for candidate_root in candidates:
        if candidate_root.is_symlink() or not candidate_root.is_dir():
            continue
        try:
            resolved_candidate, _ = validate_managed_cache_child(candidate_root, cache_root)
        except RuntimeError:
            continue
        if resolved_candidate.parent != candidate_parent.resolve(strict=False):
            continue
        manifest = read_json(resolved_candidate / "manifest.json")
        candidate_identity = manifest.get("cache_identity")
        candidate_key = manifest.get("cache_key")
        if (
            manifest.get("connector") != connector
            or not isinstance(candidate_key, str)
            or candidate_key != resolved_candidate.name
            or not connector_cache_identity_equivalent_ignoring_connector_commit(
                candidate_identity, requested_identity
            )
        ):
            continue
        candidate_plan = staged_connector_plan(plan, resolved_candidate)
        candidate_plan.update(
            connector_build_id=candidate_key,
            cache_identity=candidate_identity,
            cache_key=candidate_key,
            requested_cache_identity=requested_identity,
            requested_cache_key=requested_key,
            requested_connector_commit=requested_commit,
            reused_from_connector_commit=str(candidate_identity["extra_inputs"]["connector_commit"]),
            cache_reuse_reason="connector_commit_only",
        )
        if connector_cache_entry_complete(candidate_plan):
            return candidate_plan
    return plan


def rebase_cache_path(path: Path, source_root: Path, destination_root: Path) -> Path:
    resolved = path.resolve(strict=False)
    try:
        return destination_root / resolved.relative_to(source_root)
    except ValueError:
        return resolved


def staged_connector_plan(plan: dict[str, Any], staging_root: Path) -> dict[str, Any]:
    """Clone a connector plan with every entry-local path rebased to staging."""
    final_root = Path(str(plan["root"])).resolve()
    staged = dict(plan)
    staged["root"] = str(staging_root)
    for key in ("manifest", "build_root", "httpd_prefix", "nginx_prefix"):
        raw_path = plan.get(key)
        if isinstance(raw_path, str) and raw_path:
            staged[key] = str(rebase_cache_path(Path(raw_path), final_root, staging_root))
    output_paths = plan.get("output_paths")
    if isinstance(output_paths, dict):
        staged["output_paths"] = {
            name: str(rebase_cache_path(Path(raw_path), final_root, staging_root))
            if isinstance(raw_path, str) and raw_path
            else raw_path
            for name, raw_path in output_paths.items()
        }
    return staged


def rebase_cache_record(value: Any, source_root: Path, destination_root: Path) -> Any:
    if isinstance(value, dict):
        return {key: rebase_cache_record(item, source_root, destination_root) for key, item in value.items()}
    if isinstance(value, list):
        return [rebase_cache_record(item, source_root, destination_root) for item in value]
    if isinstance(value, str):
        try:
            path = Path(value)
            if path.is_absolute():
                # Records contain both entry-local artifact paths and stable
                # identity inputs such as /usr/bin/cc.  Only a path already
                # lexically under the staging tree is eligible for resolving
                # and rebasing.  External strings must remain byte-for-byte
                # unchanged: normalizing a compiler symlink after cache_key
                # calculation makes the published manifest disagree with its
                # registry marker and turns every later invocation into a
                # cache miss.
                source = source_root.resolve(strict=False)
                try:
                    path.relative_to(source)
                except ValueError:
                    # Do not even canonicalize a foreign spelling such as
                    # /usr/bin/cc; it is an identity value, not an artifact.
                    return value
                resolved = path.resolve(strict=False)
                relative = resolved.relative_to(source)
                return str(destination_root / relative)
        except (OSError, RuntimeError, ValueError):
            pass
    return value


def prepare_connector_transactionally(
    connector: str,
    cache_root: Path,
    plan: dict[str, Any],
    prepare: Any,
) -> dict[str, Any]:
    """Build a keyed connector tree in staging, then atomically publish it."""
    final_root = Path(str(plan["root"])).resolve()
    cache_key = str(plan.get("cache_key", plan.get("connector_build_id", "")))
    if not cache_key:
        return prepare(plan, True)
    try:
        _, managed_root = validate_managed_cache_child(final_root, cache_root)
    except RuntimeError:
        return prepare(plan, True)
    try:
        with BuildLock(cache_entry_lock_path(managed_root, f"connector-{connector}", cache_key)):
            if connector_cache_entry_complete(plan):
                return prepare(plan, True)
            if final_root.exists():
                if not managed_cache_entry_valid(final_root, managed_root):
                    if not migrate_legacy_cache_entry_for_removal(
                        final_root,
                        managed_root,
                        component=f"connector:{connector}",
                    ):
                        return prepare(plan, True)
                safe_remove_dir(final_root, managed_root)
            staging_root = temporary_cache_dir(
                final_root,
                managed_root,
                component=f"connector:{connector}",
                cache_key=cache_key,
            )
            try:
                staged_plan = staged_connector_plan(plan, staging_root)
                record = prepare(staged_plan, True)
                if record.get("status") != "built" or not connector_manifest_contract_ready(staged_plan):
                    return rebase_cache_record(record, staging_root, final_root)
                if connector == "apache":
                    try:
                        rebase_apache_install_text_paths_for_publish(staged_plan, final_root)
                    except RuntimeError as exc:
                        failed_record = rebase_cache_record(record, staging_root, final_root)
                        failed_record.update(
                            status="failed",
                            blocker_reason="apache_publication_relocation_failed",
                            details=str(exc),
                        )
                        return failed_record
                write_cache_entry_completion(
                    staging_root,
                    managed_root,
                    component=f"connector:{connector}",
                    cache_key=cache_key,
                    cache_identity=staged_plan["cache_identity"],
                )
                atomic_publish_dir(staging_root, final_root, managed_root, require_complete=True)
                published_record = rebase_cache_record(record, staging_root, final_root)
                if connector == "apache" and not apache_apxs_includedir_usable(
                    Path(str(plan.get("httpd_prefix", "")))
                ):
                    try:
                        safe_remove_dir(final_root, managed_root)
                    except RuntimeError as exc:
                        published_record.update(
                            status="failed",
                            blocker_reason="apache_apxs_publish_validation_failed",
                            details=str(exc),
                        )
                    else:
                        published_record.update(
                            status="failed",
                            blocker_reason="apache_apxs_publish_validation_failed",
                        )
                    return published_record
                write_connector_manifest(plan, published_record)
                return published_record
            finally:
                if staging_root.exists():
                    try:
                        safe_remove_dir(staging_root, managed_root)
                    except RuntimeError:
                        pass
    except TimeoutError as exc:
        return {
            "connector": connector,
            "connector_build_id": plan.get("connector_build_id", ""),
            "status": "blocked",
            "blocker_reason": "cache_lock_timeout",
            "details": str(exc),
        }


def can_link_crypt(link_arg: str, env: dict[str, str] | None = None) -> bool:
    check_env = env or os.environ
    compiler = resolve_compiler(check_env)
    if not compiler:
        return False
    source = "extern char *crypt(const char *, const char *); int main(void) { return crypt(\"x\", \"xx\") == 0; }\n"
    proc = subprocess.run(
        [compiler, "-x", "c", "-", link_arg, "-o", os.devnull],
        input=source,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=check_env,
    )
    return proc.returncode == 0


def crypt_diagnostics(env: dict[str, str]) -> dict[str, Any]:
    header_path = Path("/usr/include/crypt.h")
    candidates = [
        Path("/usr/lib/x86_64-linux-gnu/libcrypt.so"),
        Path("/lib/x86_64-linux-gnu/libcrypt.so"),
        Path("/usr/lib64/libcrypt.so"),
        Path("/lib64/libcrypt.so"),
        Path("/usr/lib/x86_64-linux-gnu/libcrypt.so.1"),
        Path("/lib/x86_64-linux-gnu/libcrypt.so.1"),
        Path("/usr/lib64/libcrypt.so.1"),
        Path("/lib64/libcrypt.so.1"),
    ]
    found = [str(path) for path in candidates if path.exists()]
    configured = env.get("CRYPT_LIB", "").strip()
    link_arg = ""
    link_mode = ""
    if configured:
        link_arg = configured
        link_mode = "env:CRYPT_LIB"
    elif can_link_crypt("-lcrypt", env):
        link_arg = "-lcrypt"
        link_mode = "compiler:-lcrypt"
    elif found:
        link_arg = found[0]
        link_mode = "direct-path"
    return {
        "crypt_h_path": str(header_path),
        "crypt_h_status": "present" if header_path.is_file() else "missing",
        "libcrypt_paths": found,
        "libcrypt_status": "present" if found else "missing",
        "crypt_link_arg": link_arg,
        "crypt_link_mode": link_mode,
    }


def resolve_crypt_link_arg(env: dict[str, str]) -> str:
    configured = env.get("CRYPT_LIB", "").strip()
    if configured:
        return configured
    if can_link_crypt("-lcrypt", env):
        return "-lcrypt"
    for candidate in (
        Path("/usr/lib/x86_64-linux-gnu/libcrypt.so"),
        Path("/lib/x86_64-linux-gnu/libcrypt.so"),
        Path("/usr/lib64/libcrypt.so"),
        Path("/lib64/libcrypt.so"),
        Path("/usr/lib/x86_64-linux-gnu/libcrypt.so.1"),
        Path("/lib/x86_64-linux-gnu/libcrypt.so.1"),
        Path("/usr/lib64/libcrypt.so.1"),
        Path("/lib64/libcrypt.so.1"),
    ):
        if candidate.is_file():
            return str(candidate)
    return ""


def write_apachectl_wrapper(
    wrapper_path: Path,
    httpd_bin: Path,
    httpd_prefix: Path,
    modsecurity_lib_dir: Path,
    pcre2_lib_dir: Path,
    expat_lib_dir: Path | None = None,
) -> None:
    if is_system_path(wrapper_path):
        raise RuntimeError(f"system_path_write_forbidden: {wrapper_path}")
    wrapper_path.parent.mkdir(parents=True, exist_ok=True)
    content = f"""#!/bin/sh
set -eu

HTTPD_BIN={sh_quote(str(httpd_bin))}
HTTPD_PREFIX={sh_quote(str(httpd_prefix))}
MODSECURITY_LIB_DIR={sh_quote(str(modsecurity_lib_dir))}
PCRE2_LIB_DIR={sh_quote(str(pcre2_lib_dir))}
EXPAT_LIB_DIR={sh_quote(str(expat_lib_dir or ""))}

server_root=""
previous=""
for arg in "$@"; do
    if [ "$previous" = "-d" ]; then
        server_root=$arg
        previous=""
        continue
    fi
    if [ "$arg" = "-d" ]; then
        previous="-d"
    fi
done

if [ -n "$server_root" ]; then
    export APACHE_RUN_DIR="${{APACHE_RUN_DIR:-$server_root/run}}"
    export APACHE_LOCK_DIR="${{APACHE_LOCK_DIR:-$server_root/run}}"
    export APACHE_LOG_DIR="${{APACHE_LOG_DIR:-$server_root/log}}"
fi

if [ -z "${{APACHE_RUN_USER:-}}" ]; then
    if [ "$(id -u)" = "0" ]; then
        APACHE_RUN_USER=nobody
    else
        APACHE_RUN_USER=$(id -un)
    fi
    export APACHE_RUN_USER
fi
if [ -z "${{APACHE_RUN_GROUP:-}}" ]; then
    if [ "$(id -u)" = "0" ]; then
        APACHE_RUN_GROUP=$(getent group nogroup >/dev/null 2>&1 && printf '%s' nogroup || printf '%s' nobody)
    else
        APACHE_RUN_GROUP=$(id -gn)
    fi
    export APACHE_RUN_GROUP
fi

LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR:$HTTPD_PREFIX/lib:$PCRE2_LIB_DIR${{EXPAT_LIB_DIR:+:$EXPAT_LIB_DIR}}${{LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}}"
export LD_LIBRARY_PATH
exec "$HTTPD_BIN" "$@"
"""
    wrapper_path.write_text(content, encoding="utf-8")
    wrapper_path.chmod(0o755)


def prepare_apache_httpd(
    env: dict[str, str],
    connector_root: Path,
    framework_root: Path,
    cache_root: Path,
    build_root: Path,
    sources_root: Path,
    archives_root: Path,
    expat: dict[str, Any] | None = None,
    modsecurity: dict[str, Any] | None = None,
    plan: dict[str, Any] | None = None,
    _transactional: bool = False,
) -> dict[str, Any]:
    if plan and plan.get("root") and not _transactional:
        return prepare_connector_transactionally(
            "apache",
            cache_root,
            plan,
            lambda staged_plan, _inner: prepare_apache_httpd(
                env,
                connector_root,
                framework_root,
                cache_root,
                build_root,
                sources_root,
                archives_root,
                expat,
                modsecurity,
                staged_plan,
                _transactional=True,
            ),
        )
    modsecurity = modsecurity or {}
    plan = plan or {}
    apache_build_root = Path(env.get("APACHE_BUILD_ROOT", str(plan.get("build_root") or build_root / "apache-build"))).resolve()
    httpd_prefix = Path(env.get("HTTPD_PREFIX", str(plan.get("httpd_prefix") or build_root / "apache-runtime/httpd"))).resolve()
    httpd_bin = Path(env.get("APACHE_HTTPD") or env.get("APACHE") or str(httpd_prefix / "bin/httpd")).resolve()
    apxs_bin = Path(env.get("APXS") or env.get("APXS_BIN") or str(httpd_prefix / "bin/apxs")).resolve()
    apache_module = Path(env.get("APACHE_MODULE", str(apache_build_root / "output/apache/mod_security3.so"))).resolve()
    modsecurity_lib_dir = Path(
        env.get("APACHE_MRTS_MODSECURITY_LIB_DIR", str(modsecurity.get("lib_dir") or apache_build_root / "output/modsecurity/lib"))
    ).resolve()
    pcre2_prefix = Path(env.get("PCRE2_PREFIX", str(apache_build_root / "output/pcre2"))).resolve()
    pcre2_lib_dir = pcre2_prefix / "lib"
    expat = expat or {}
    expat_prefix = Path(str(expat.get("prefix", ""))).resolve() if expat.get("prefix") else None
    expat_lib_dir = Path(str(expat.get("lib_dir", ""))).resolve() if expat.get("lib_dir") else None
    expat_cppflags = f"-I{expat_prefix / 'include'}" if expat_prefix else ""
    expat_ldflags = f"-L{expat_lib_dir}" if expat_lib_dir else ""
    expat_pkg_config_path = str(expat_prefix / "lib/pkgconfig") if expat_prefix else ""
    crypt = crypt_diagnostics(env)
    crypt_link_arg = str(crypt.get("crypt_link_arg", ""))
    apache_libs = " ".join(part for part in (env.get("LIBS", ""), crypt_link_arg) if part).strip()
    wrapper_path = httpd_prefix / "bin/apachectl-mrts"
    override_apachectl = env.get("APACHECTL_BIN", "")
    effective_apachectl = Path(override_apachectl).resolve() if override_apachectl else wrapper_path
    artifacts = {
        "httpd_bin": httpd_bin,
        "apxs_bin": apxs_bin,
        "module_file": apache_module,
        "modsecurity_lib": modsecurity_lib_dir / "libmodsecurity.so",
    }
    ready, missing = artifact_status(artifacts, {"httpd_bin", "apxs_bin"})
    record: dict[str, Any] = {
        "source": "connector-local-build",
        "connector": "apache",
        "connector_build_id": plan.get("connector_build_id", ""),
        "modsecurity_build_id": modsecurity.get("build_id", ""),
        "cache_schema_version": plan.get("cache_schema_version", ""),
        "cache_key": plan.get("cache_key", ""),
        "patchset_sha256": plan.get("patchset_sha256", ""),
        "target_architecture": plan.get("target_architecture", ""),
        "expected_ref": env.get("HTTPD_VERSION", ""),
        "cache_path": str(archives_root / "apache"),
        "build_path": str(apache_build_root),
        "httpd_prefix": str(httpd_prefix),
        "pcre2_prefix": str(pcre2_prefix),
        "httpd_bin": str(httpd_bin),
        "apxs_bin": str(apxs_bin),
        "module_file": str(apache_module),
        "modsecurity_lib_dir": str(modsecurity_lib_dir),
        "apachectl_bin": str(effective_apachectl),
        "expat_source": expat.get("source", ""),
        "expat_release_tag": expat.get("release_tag", expat.get("expected_ref", "")),
        "expat_actual_head": expat.get("actual_head", ""),
        "expat_prefix": str(expat_prefix) if expat_prefix else "",
        "expat_h": str(expat.get("expat_h", "")),
        "expat_lib_dir": str(expat_lib_dir) if expat_lib_dir else "",
        "cppflags": " ".join(part for part in (expat_cppflags, env.get("CPPFLAGS", "")) if part).strip(),
        "ldflags": " ".join(part for part in (expat_ldflags, env.get("LDFLAGS", "")) if part).strip(),
        "libs": apache_libs,
        "crypt_lib": crypt_link_arg,
        "crypt_h_status": crypt.get("crypt_h_status", ""),
        "crypt_h_path": crypt.get("crypt_h_path", ""),
        "libcrypt_status": crypt.get("libcrypt_status", ""),
        "libcrypt_paths": crypt.get("libcrypt_paths", []),
        "crypt_link_mode": crypt.get("crypt_link_mode", ""),
        "crypt_config_cache": crypt_link_arg,
        "aprutil_libs": crypt_link_arg,
        "pkg_config_path": f"{expat_pkg_config_path}{os.pathsep}{env.get('PKG_CONFIG_PATH', '')}".rstrip(os.pathsep)
        if expat_pkg_config_path
        else env.get("PKG_CONFIG_PATH", ""),
        "status": "unknown",
        "blocker_reason": "",
        "searched_paths": [str(path) for path in artifacts.values()],
        "env_override": "APACHECTL_BIN",
        "output_paths": {
            "binary": str(httpd_bin),
            "module": str(apache_module),
            "config": str(httpd_prefix / "conf/httpd.conf"),
        },
    }
    if modsecurity.get("status") == "blocked":
        record.update(status="blocked", blocker_reason=modsecurity.get("blocker_reason") or "modsecurity_build_failed")
        write_connector_manifest(plan, record) if plan else None
        return record
    if override_apachectl and not executable(Path(override_apachectl)):
        record.update(status="blocked", blocker_reason="missing_local_httpd_build", missing_file=override_apachectl)
        write_connector_manifest(plan, record) if plan else None
        return record
    manifest_ready = connector_manifest_ready(plan) if plan else False
    if plan.get("root") and Path(str(plan["root"])).exists() and not (ready and manifest_ready):
        try:
            stale_root = Path(str(plan["root"]))
            safe_remove_dir(stale_root, cache_root)
        except RuntimeError as exc:
            record.update(status="blocked", blocker_reason=str(exc))
            write_connector_manifest(plan, record)
            return record
        record["invalidation_reason"] = (
            "missing_or_incomplete_connector_manifest" if not manifest_ready else "connector_artifact_missing"
        )
        ready, missing = artifact_status(artifacts, {"httpd_bin", "apxs_bin"})
        if ready:
            record.update(status="blocked", blocker_reason="connector_manifest_missing_for_external_artifacts")
            write_connector_manifest(plan, record)
            return record
    if (
        ready
        and plan
        and connector_manifest_ready(plan)
        and apache_apxs_includedir_usable(httpd_prefix)
    ):
        record.update(status="reused", tree=tree_manifest(apache_build_root), apachectl_bin=str(effective_apachectl))
        write_connector_manifest(plan, record)
        return record
    if plan.get("root"):
        try:
            mark_managed_cache_entry(
                Path(str(plan["root"])),
                cache_root,
                component="connector:apache",
                cache_key=str(plan.get("cache_key", plan.get("connector_build_id", ""))),
            )
        except RuntimeError as exc:
            record.update(status="blocked", blocker_reason=str(exc))
            write_connector_manifest(plan, record)
            return record
    if not ready:
        log_path = build_root / "logs/runtime-components/apache-build.log"
        proc = run_build(
            framework_root / "ci/prepare-apache-build.sh",
            build_env(
                env,
                FRAMEWORK_ROOT=str(framework_root),
                CONNECTOR_ROOT=str(connector_root),
                CONNECTOR_COMPONENT_CACHE=str(cache_root),
                SOURCE_ROOT=str(sources_root),
                MODSECURITY_SOURCE_DIR=str(sources_root / "ModSecurity_V3"),
                MODSECURITY_V3_SOURCE_DIR=str(sources_root / "ModSecurity_V3"),
                MODSECURITY_V3_ROOT=str(sources_root / "ModSecurity_V3"),
                BUILD_ROOT=str(build_root),
                TMP_ROOT=str(build_root / "tmp"),
                LOG_ROOT=str(build_root / "logs"),
                APACHE_BUILD_ROOT=str(apache_build_root),
                APACHE_BUILD_OWNER_ROOT=str(cache_root),
                HTTPD_PREFIX=str(httpd_prefix),
                APACHE_DOWNLOAD_DIR=str(archives_root / "apache"),
                MODSECURITY_SHARED_PREFIX=str(modsecurity.get("prefix", "")),
                MODSECURITY_BUILD_ID=str(modsecurity.get("build_id", "")),
                CPPFLAGS=" ".join(part for part in (expat_cppflags, env.get("CPPFLAGS", "")) if part).strip(),
                LDFLAGS=" ".join(part for part in (expat_ldflags, env.get("LDFLAGS", "")) if part).strip(),
                LIBS=apache_libs,
                CRYPT_LIBS=crypt_link_arg if crypt_link_arg else None,
                APRUTIL_LIBS=crypt_link_arg if crypt_link_arg else None,
                ac_cv_search_crypt=crypt_link_arg if crypt_link_arg else None,
                PKG_CONFIG_PATH=(
                    f"{expat_pkg_config_path}{os.pathsep}{env.get('PKG_CONFIG_PATH', '')}".rstrip(os.pathsep)
                    if expat_pkg_config_path
                    else env.get("PKG_CONFIG_PATH", "")
                ),
                LD_LIBRARY_PATH=(
                    f"{expat_lib_dir}{os.pathsep}{env.get('LD_LIBRARY_PATH', '')}".rstrip(os.pathsep)
                    if expat_lib_dir
                    else env.get("LD_LIBRARY_PATH", "")
                ),
                BUILD_HTTPD_FROM_SOURCE="1",
                BUILD_PCRE2_FROM_SOURCE="1",
                AUTO_FETCH_SMOKE_SOURCES="0",
                REFRESH="1",
                SKIP_RUNTIME_COMPONENT_PREPARE="1",
            ),
            connector_root,
            log_path,
        )
        record["build_log"] = str(log_path)
        record["build_exit_code"] = proc.returncode
        artifacts_file = apache_build_root / "logs/apache/artifacts.txt"
        if artifacts_file.is_file():
            record["artifacts"] = read_key_values(artifacts_file)
        ready, missing = artifact_status(artifacts, {"httpd_bin", "apxs_bin"})
        if proc.returncode != 0 or not ready:
            apache_log_dir = build_root / "logs/apache"
            diagnostic_text = "\n".join(
                [
                    proc.stdout,
                    read_text_if_file(log_path),
                    read_text_if_file(apache_log_dir / "check-expat.h.log"),
                    read_text_if_file(apache_log_dir / "httpd-configure.log"),
                    read_text_if_file(apache_log_dir / "httpd-make.log"),
                    read_text_if_file(apache_log_dir / "apache-configure.log"),
                    read_text_if_file(apache_log_dir / "apache-make.log"),
                ]
            )
            blocker = map_apache_blocker(diagnostic_text, missing)
            blocker_details: dict[str, Any] = {}
            if blocker == "missing_expat_headers":
                blocker_details = {
                    "missing_file": "expat.h",
                    "build_component": "apache_httpd_source_build",
                    "env_variable_can_set": "CPPFLAGS/LDFLAGS",
                    "dependency_searched_paths": [env.get("CPPFLAGS") or "<compiler default include paths>"],
                }
            elif blocker == "missing_crypt_library":
                blocker_details = {
                    "missing_file": "libcrypt.so development link target or explicit -lcrypt linkage",
                    "build_component": "apache_httpd_source_build",
                    "env_variable_can_set": "LIBS/LDFLAGS",
                    "dependency_searched_paths": [env.get("LIBS") or "<configure default libraries>"],
                }
            record.update(
                status="failed",
                blocker_reason=blocker,
                missing_files=missing,
                **blocker_details,
            )
            write_connector_manifest(plan, record) if plan else None
            return record
    try:
        if not override_apachectl:
            write_apachectl_wrapper(wrapper_path, httpd_bin, httpd_prefix, modsecurity_lib_dir, pcre2_lib_dir, expat_lib_dir)
        elif not executable(Path(override_apachectl)):
            raise RuntimeError(f"APACHECTL_BIN is not executable: {override_apachectl}")
    except Exception as exc:
        record.update(status="blocked", blocker_reason="missing_local_httpd_build", details=str(exc))
        write_connector_manifest(plan, record) if plan else None
        return record
    record.update(
        status="built" if plan else "present",
        invalidation_reason=record.get("invalidation_reason") or ("missing_or_stale_connector_build" if plan else ""),
        tree=tree_manifest(apache_build_root),
        apachectl_bin=str(effective_apachectl),
    )
    write_connector_manifest(plan, record) if plan else None
    return record


def prepare_nginx_runtime(
    env: dict[str, str],
    connector_root: Path,
    framework_root: Path,
    cache_root: Path,
    build_root: Path,
    sources_root: Path,
    archives_root: Path,
    modsecurity: dict[str, Any] | None = None,
    plan: dict[str, Any] | None = None,
    _transactional: bool = False,
) -> dict[str, Any]:
    if plan and plan.get("root") and not _transactional:
        return prepare_connector_transactionally(
            "nginx",
            cache_root,
            plan,
            lambda staged_plan, _inner: prepare_nginx_runtime(
                env,
                connector_root,
                framework_root,
                cache_root,
                build_root,
                sources_root,
                archives_root,
                modsecurity,
                staged_plan,
                _transactional=True,
            ),
        )
    modsecurity = modsecurity or {}
    plan = plan or {}
    nginx_build_root = Path(env.get("NGINX_BUILD_DIR", str(plan.get("build_root") or build_root / "nginx-build"))).resolve()
    nginx_prefix = Path(env.get("NGINX_PREFIX", str(plan.get("nginx_prefix") or build_root / "nginx-runtime/nginx"))).resolve()
    local_nginx_bin = Path(env.get("NGINX_BINARY", str(nginx_prefix / "sbin/nginx"))).resolve()
    local_module = Path(
        env.get("NGINX_MODULE", str(nginx_prefix / "modules/ngx_http_modsecurity_module.so"))
    ).resolve()
    modsecurity_lib_dir = Path(
        env.get("NGINX_MRTS_MODSECURITY_LIB_DIR", str(modsecurity.get("lib_dir") or nginx_build_root / "output/modsecurity/lib"))
    ).resolve()
    override_bin = env.get("MRTS_NATIVE_NGINX_BIN", "")
    override_module_dir = env.get("MRTS_NATIVE_NGINX_MODULE_DIR", "")
    effective_bin = Path(override_bin).resolve() if override_bin else local_nginx_bin
    effective_module = (
        Path(override_module_dir).resolve() / "ngx_http_modsecurity_module.so"
        if override_module_dir
        else local_module
    )
    local_artifacts = {
        "nginx_bin": local_nginx_bin,
        "module_file": local_module,
        "modsecurity_lib": modsecurity_lib_dir / "libmodsecurity.so",
    }
    effective_artifacts = {
        "nginx_bin": effective_bin,
        "module_file": effective_module,
    }
    local_ready, local_missing = artifact_status(local_artifacts, {"nginx_bin"})
    effective_ready, effective_missing = artifact_status(effective_artifacts, {"nginx_bin"})
    record: dict[str, Any] = {
        "source": "connector-local-build",
        "connector": "nginx",
        "connector_build_id": plan.get("connector_build_id", ""),
        "modsecurity_build_id": modsecurity.get("build_id", ""),
        "cache_schema_version": plan.get("cache_schema_version", ""),
        "cache_key": plan.get("cache_key", ""),
        "patchset_sha256": plan.get("patchset_sha256", ""),
        "target_architecture": plan.get("target_architecture", ""),
        "expected_ref": env.get("NGINX_RELEASE_TAG") or env.get("NGINX_SOURCE_GIT_REF", ""),
        "cache_path": str(archives_root / "nginx"),
        "build_path": str(nginx_build_root),
        "nginx_prefix": str(nginx_prefix),
        "nginx_bin": str(effective_bin),
        "module_dir": str(effective_module.parent),
        "module_file": str(effective_module),
        "local_nginx_bin": str(local_nginx_bin),
        "local_module_file": str(local_module),
        "modsecurity_lib_dir": str(modsecurity_lib_dir),
        "status": "unknown",
        "blocker_reason": "",
        "searched_paths": [str(path) for path in local_artifacts.values()],
        "env_override": "MRTS_NATIVE_NGINX_BIN/MRTS_NATIVE_NGINX_MODULE_DIR",
        "output_paths": {
            "binary": str(effective_bin),
            "module": str(effective_module),
            "config": str(nginx_prefix / "conf/nginx.conf"),
        },
    }
    if modsecurity.get("status") == "blocked":
        record.update(status="blocked", blocker_reason=modsecurity.get("blocker_reason") or "modsecurity_build_failed")
        write_connector_manifest(plan, record) if plan else None
        return record
    if override_bin and not executable(Path(override_bin)):
        record.update(status="blocked", blocker_reason="missing_local_nginx_build", missing_file=override_bin)
        write_connector_manifest(plan, record) if plan else None
        return record
    if override_module_dir and not (Path(override_module_dir) / "ngx_http_modsecurity_module.so").is_file():
        record.update(
            status="blocked",
            blocker_reason="missing_nginx_modsecurity_module",
            missing_file=str(Path(override_module_dir) / "ngx_http_modsecurity_module.so"),
        )
        write_connector_manifest(plan, record) if plan else None
        return record
    manifest_ready = connector_manifest_ready(plan) if plan else False
    if plan.get("root") and Path(str(plan["root"])).exists() and not (local_ready and effective_ready and manifest_ready):
        try:
            stale_root = Path(str(plan["root"]))
            safe_remove_dir(stale_root, cache_root)
        except RuntimeError as exc:
            record.update(status="blocked", blocker_reason=str(exc))
            write_connector_manifest(plan, record)
            return record
        record["invalidation_reason"] = (
            "missing_or_incomplete_connector_manifest" if not manifest_ready else "connector_artifact_missing"
        )
        local_ready, local_missing = artifact_status(local_artifacts, {"nginx_bin"})
        effective_ready, effective_missing = artifact_status(effective_artifacts, {"nginx_bin"})
        if local_ready and effective_ready:
            record.update(status="blocked", blocker_reason="connector_manifest_missing_for_external_artifacts")
            write_connector_manifest(plan, record)
            return record
    if effective_ready and local_ready and plan and connector_manifest_ready(plan):
        record.update(
            status="reused",
            nginx_bin=str(effective_bin),
            module_dir=str(effective_module.parent),
            module_file=str(effective_module),
            tree=tree_manifest(nginx_build_root),
        )
        write_connector_manifest(plan, record)
        return record
    if plan.get("root"):
        try:
            mark_managed_cache_entry(
                Path(str(plan["root"])),
                cache_root,
                component="connector:nginx",
                cache_key=str(plan.get("cache_key", plan.get("connector_build_id", ""))),
            )
        except RuntimeError as exc:
            record.update(status="blocked", blocker_reason=str(exc))
            write_connector_manifest(plan, record)
            return record
    if not effective_ready and not local_ready:
        common_source_root = connector_root / "common/src"
        common_build_source_root = Path(str(plan["root"])) / "common-src"
        common_build_source_root.mkdir(parents=True, exist_ok=True)
        for common_source in sorted(common_source_root.glob("*.c")):
            shutil.copy2(common_source, common_build_source_root / common_source.name)
        log_path = build_root / "logs/runtime-components/nginx-build.log"
        proc = run_build(
            framework_root / "ci/prepare-nginx-build.sh",
            build_env(
                env,
                FRAMEWORK_ROOT=str(framework_root),
                CONNECTOR_ROOT=str(connector_root),
                CONNECTOR_COMPONENT_CACHE=str(cache_root),
                SOURCE_ROOT=str(sources_root),
                MODSECURITY_SOURCE_DIR=str(sources_root / "ModSecurity_V3"),
                MODSECURITY_V3_SOURCE_DIR=str(sources_root / "ModSecurity_V3"),
                MODSECURITY_V3_ROOT=str(sources_root / "ModSecurity_V3"),
                BUILD_ROOT=str(cache_root),
                TMP_ROOT=str(build_root / "tmp"),
                LOG_ROOT=str(build_root / "logs"),
                NGINX_BUILD_DIR=str(nginx_build_root),
                NGINX_PREFIX=str(nginx_prefix),
                NGINX_BINARY=str(local_nginx_bin),
                NGINX_MODULE=str(local_module),
                NGINX_DOWNLOAD_DIR=str(archives_root / "nginx"),
                MSCONNECTOR_COMMON_SRC=str(common_build_source_root),
                MODSECURITY_SHARED_PREFIX=str(modsecurity.get("prefix", "")),
                MODSECURITY_BUILD_ID=str(modsecurity.get("build_id", "")),
                BUILD_NGINX_FROM_SOURCE="1",
                AUTO_FETCH_SMOKE_SOURCES="0",
                REFRESH="1",
                SKIP_RUNTIME_COMPONENT_PREPARE="1",
            ),
            connector_root,
            log_path,
        )
        record["build_log"] = str(log_path)
        record["build_exit_code"] = proc.returncode
        artifacts_file = nginx_build_root / "logs/nginx/artifacts.txt"
        if artifacts_file.is_file():
            record["artifacts"] = read_key_values(artifacts_file)
        local_ready, local_missing = artifact_status(local_artifacts, {"nginx_bin"})
        effective_ready, effective_missing = artifact_status(effective_artifacts, {"nginx_bin"})
        if proc.returncode != 0 or not local_ready:
            blocker = map_nginx_blocker(proc.stdout, local_missing)
            blocker_details = {
                "build_component": "nginx_modsecurity_module_build",
                "env_variable_can_set": "MRTS_NATIVE_NGINX_BIN/MRTS_NATIVE_NGINX_MODULE_DIR",
            }
            if blocker == "missing_libmodsecurity_build":
                blocker_details["build_component"] = "libmodsecurity_build"
            elif blocker == "missing_local_nginx_build":
                blocker_details["build_component"] = "nginx_source_build"
            record.update(
                status="failed",
                blocker_reason=blocker,
                missing_files=local_missing,
                **blocker_details,
            )
            write_connector_manifest(plan, record) if plan else None
            return record
    if not override_bin:
        effective_bin = local_nginx_bin
    if not override_module_dir:
        effective_module = local_module
    effective_ready, effective_missing = artifact_status(
        {"nginx_bin": effective_bin, "module_file": effective_module},
        {"nginx_bin"},
    )
    if not effective_ready:
        blocker = map_nginx_blocker("", effective_missing)
        record.update(
            status="blocked",
            blocker_reason=blocker,
            missing_files=effective_missing,
            build_component="nginx_native_runtime_inventory",
            env_variable_can_set="MRTS_NATIVE_NGINX_BIN/MRTS_NATIVE_NGINX_MODULE_DIR",
        )
        write_connector_manifest(plan, record) if plan else None
        return record
    record.update(
        status="built" if plan else "present",
        invalidation_reason=record.get("invalidation_reason") or ("missing_or_stale_connector_build" if plan else ""),
        nginx_bin=str(effective_bin),
        module_dir=str(effective_module.parent),
        module_file=str(effective_module),
        tree=tree_manifest(nginx_build_root),
    )
    write_connector_manifest(plan, record) if plan else None
    return record


def prepare_haproxy_runtime(
    env: dict[str, str],
    connector_root: Path,
    framework_root: Path,
    cache_root: Path,
    build_root: Path,
    sources_root: Path,
    archives_root: Path,
    modsecurity: dict[str, Any],
    plan: dict[str, Any],
    _transactional: bool = False,
) -> dict[str, Any]:
    if plan.get("root") and not _transactional:
        return prepare_connector_transactionally(
            "haproxy",
            cache_root,
            plan,
            lambda staged_plan, _inner: prepare_haproxy_runtime(
                env,
                connector_root,
                framework_root,
                cache_root,
                build_root,
                sources_root,
                archives_root,
                modsecurity,
                staged_plan,
                _transactional=True,
            ),
        )
    root = Path(str(plan.get("build_root"))).resolve()
    haproxy_runtime_build_dir = root / "haproxy-runtime-build"
    haproxy_runtime_dir = root / "haproxy-runtime/haproxy"
    haproxy_bin = haproxy_runtime_dir / "sbin/haproxy"
    binding_dir = root / "haproxy-modsecurity-binding"
    spoa_dir = root / "haproxy-spoa-runtime"
    spoa_bin = spoa_dir / "haproxy-modsecurity-spoa"
    paths_env = binding_dir / "paths.env"
    log_path = build_root / "logs/runtime-components/haproxy-build.log"
    output_paths = {
        "binary": str(haproxy_bin),
        "module": str(spoa_bin),
        "config": str(paths_env),
    }
    record: dict[str, Any] = {
        "connector": "haproxy",
        "connector_build_id": plan.get("connector_build_id", ""),
        "modsecurity_build_id": modsecurity.get("build_id", ""),
        "cache_schema_version": plan.get("cache_schema_version", ""),
        "cache_key": plan.get("cache_key", ""),
        "patchset_sha256": plan.get("patchset_sha256", ""),
        "target_architecture": plan.get("target_architecture", ""),
        "source_hash": plan.get("source_hash", ""),
        "build_flags": plan.get("build_flags", ""),
        "build_path": str(root),
        "haproxy_runtime_build_dir": str(haproxy_runtime_build_dir),
        "haproxy_runtime_dir": str(haproxy_runtime_dir),
        "haproxy_bin": str(haproxy_bin),
        "spoa_runtime_bin": str(spoa_bin),
        "modsecurity_binding_dir": str(binding_dir),
        "paths_env": str(paths_env),
        "output_paths": output_paths,
        "status": "unknown",
        "blocker_reason": "",
    }
    if modsecurity.get("status") == "blocked":
        record.update(status="blocked", blocker_reason=modsecurity.get("blocker_reason") or "modsecurity_build_failed")
        write_connector_manifest(plan, record)
        return record
    for path in (root, haproxy_runtime_build_dir, haproxy_runtime_dir, binding_dir, spoa_dir):
        if is_system_path(path) or not is_within(path, cache_root):
            record.update(status="blocked", blocker_reason="system_path_write_forbidden", blocked_path=str(path))
            write_connector_manifest(plan, record)
            return record
    if root.exists() and not connector_manifest_ready(plan):
        try:
            safe_remove_dir(root, cache_root)
        except RuntimeError as exc:
            record.update(status="blocked", blocker_reason=str(exc))
            write_connector_manifest(plan, record)
            return record
        record["invalidation_reason"] = "missing_or_incomplete_connector_manifest"
    if executable(haproxy_bin) and executable(spoa_bin) and paths_env.is_file() and connector_manifest_ready(plan):
        record.update(status="reused", tree=tree_manifest(root))
        write_connector_manifest(plan, record)
        return record

    try:
        mark_managed_cache_entry(
            root,
            cache_root,
            component="connector:haproxy",
            cache_key=str(plan.get("cache_key", plan.get("connector_build_id", ""))),
        )
    except RuntimeError as exc:
        record.update(status="blocked", blocker_reason=str(exc))
        write_connector_manifest(plan, record)
        return record
    root.mkdir(parents=True, exist_ok=True)
    prep_env = build_env(
        env,
        FRAMEWORK_ROOT=str(framework_root),
        CONNECTOR_ROOT=str(connector_root),
        CONNECTOR_COMPONENT_CACHE=str(cache_root),
        SOURCE_ROOT=str(sources_root),
        BUILD_ROOT=str(root),
        TMP_ROOT=str(root / "tmp"),
        LOG_ROOT=str(build_root / "logs"),
        HAPROXY_SOURCE_ROOT=str(sources_root / "haproxy"),
        HAPROXY_DOWNLOAD_DIR=str(archives_root / "haproxy"),
        HAPROXY_SOURCE_DIR=str(sources_root / "haproxy" / f"haproxy-{env.get('HAPROXY_VERSION', '3.2.19')}"),
        HAPROXY_RUNTIME_BUILD_DIR=str(haproxy_runtime_build_dir),
        HAPROXY_RUNTIME_BUILD_WORKTREE=str(haproxy_runtime_build_dir / "worktree"),
        HAPROXY_RUNTIME_DIR=str(haproxy_runtime_dir),
        HAPROXY_BIN=str(haproxy_bin),
        REFRESH="0",
        SKIP_RUNTIME_COMPONENT_PREPARE="1",
    )
    prep = run_build(framework_root / "ci/prepare-haproxy-runtime.sh", prep_env, connector_root, log_path)
    record["build_log"] = str(log_path)
    record["haproxy_prepare_exit_code"] = prep.returncode
    if prep.returncode != 0 or not executable(haproxy_bin):
        prepare_reached_execution = any(
            marker in prep.stdout
            for marker in (
                "haproxy_prepare: running haproxy-source-extract",
                "haproxy_prepare: running haproxy-source-copy",
                "haproxy_prepare: running haproxy-build",
                "haproxy_prepare: running haproxy-binary-stage",
            )
        )
        if prep.returncode == 0 or prep.returncode != 77 or prepare_reached_execution:
            record.update(
                status="failed",
                blocker_reason="haproxy_runtime_prepare_failed",
                build_exit_code=prep.returncode,
            )
        else:
            record.update(status="blocked", blocker_reason="missing_haproxy_runtime_build")
        write_connector_manifest(plan, record)
        return record

    make_env = build_env(
        prep_env,
        REPO_ROOT=str(connector_root),
        HAPROXY_SPOA_RUNTIME_DIR=str(spoa_dir),
        HAPROXY_MODSECURITY_BINDING_DIR=str(binding_dir),
        MODSECURITY_INCLUDE_DIR=str(modsecurity.get("include_dir", "")),
        MODSECURITY_LIB_DIR=str(modsecurity.get("lib_dir", "")),
        MODSECURITY_INCLUDE_CANDIDATES=str(modsecurity.get("include_dir", "")),
        MODSECURITY_LIB_CANDIDATES=str(modsecurity.get("lib_dir", "")),
    )
    proc = run_env(
        ["make", "-C", str(connector_root / "connectors/haproxy"), "build-modsecurity-binding", "build-spoa-runtime"],
        env=make_env,
    )
    with log_path.open("a", encoding="utf-8", errors="replace") as handle:
        handle.write("\n[haproxy-modsecurity-binding]\n")
        handle.write(proc.stdout)
        handle.write(proc.stderr)
    if proc.returncode != 0 or not (executable(spoa_bin) and paths_env.is_file()):
        record.update(status="failed", blocker_reason="haproxy_connector_build_failed", build_exit_code=proc.returncode)
        write_connector_manifest(plan, record)
        return record
    record.update(
        status="built",
        invalidation_reason=record.get("invalidation_reason") or "missing_or_stale_connector_build",
        tree=tree_manifest(root),
    )
    write_connector_manifest(plan, record)
    return record


def known_tool_source(tool: str, roots: list[Path]) -> tuple[str, str, bool]:
    token = f"github.com/coreruleset/{tool}"
    source_url = ""
    known_ref = ""
    can_build = False
    build_markers = (f"go install {token}", f"git clone https://{token}", f"git clone https://{token}.git")
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if ".git" in path.parts or not path.is_file():
                continue
            if path.suffix not in {"", ".md", ".sh", ".py", ".txt", ".yaml", ".yml", ".mk", ".json"}:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if token in text and not source_url:
                source_url = f"https://{token}"
            if any(marker in text for marker in build_markers):
                can_build = True
            if token in text and "ref=" in text and not known_ref:
                known_ref = "see " + str(path)
    return source_url, known_ref, can_build


def inventory_tool(
    dependency: str,
    env_var: str,
    default: str,
    env: dict[str, str],
    cache_root: Path,
    build_root: Path,
    native_root: Path,
    source_roots: list[Path],
) -> dict[str, Any]:
    configured = env.get(env_var, "")
    candidates = []
    if configured:
        candidates.append(configured)
    candidates.extend(
        [
            default,
            str(cache_root / f"bin/{dependency}"),
            str(cache_root / f"tools/{dependency}"),
            str(build_root / f"bin/{dependency}"),
            str(build_root / f"tools/{dependency}"),
            str(native_root / f"bin/{dependency}"),
        ]
    )
    searched = []
    resolved = ""
    for candidate in candidates:
        if not candidate or candidate in searched:
            continue
        searched.append(candidate)
        path = resolve_executable(candidate)
        if path and not resolved:
            resolved = path
    source_url, known_ref, can_build = known_tool_source(dependency, source_roots)
    status = "present" if resolved else "blocked"
    blocker = "" if resolved else f"missing_{dependency.replace('-', '_')}_source_ref"
    return {
        "dependency": dependency,
        "status": status,
        "path": resolved,
        "searched_paths": searched,
        "env_override": env_var,
        "known_source": source_url,
        "known_source_url": source_url,
        "known_ref": known_ref,
        "can_build_locally": can_build and bool(known_ref),
        "blocker_reason": blocker,
    }


def dependency_inventory(
    apache_httpd: dict[str, Any],
    nginx: dict[str, Any],
    haproxy: dict[str, Any],
    go_ftw: dict[str, Any],
    albedo: dict[str, Any],
    expat: dict[str, Any],
    modsecurity: dict[str, Any],
) -> list[dict[str, Any]]:
    def available(component: dict[str, Any]) -> bool:
        return component.get("status") in {"present", "built", "reused"}

    return [
        {
            "name": "go-ftw",
            "env_var": "GO_FTW_BIN",
            "path": go_ftw.get("path"),
            "status": "present" if available(go_ftw) else "missing",
            "access": "read-only/executable",
        },
        {
            "name": "albedo",
            "env_var": "ALBEDO_BIN",
            "path": albedo.get("path"),
            "status": "present" if available(albedo) else "missing",
            "access": "read-only/executable",
        },
        {
            "name": "expat",
            "env_var": "EXPAT_PREFIX",
            "path": expat.get("prefix"),
            "status": "present" if available(expat) else "missing",
            "access": "local-prefix/read-only",
        },
        {
            "name": "libmodsecurity",
            "env_var": "MODSECURITY_LIB_DIR",
            "path": modsecurity.get("lib_file"),
            "status": "present" if available(modsecurity) else "missing",
            "access": "shared-local-prefix/read-only",
        },
        {
            "name": "apachectl",
            "env_var": "APACHECTL_BIN",
            "path": apache_httpd.get("apachectl_bin"),
            "status": "present" if available(apache_httpd) else "missing",
            "access": "local-wrapper/read-only-executable",
        },
        {
            "name": "nginx",
            "env_var": "MRTS_NATIVE_NGINX_BIN",
            "path": nginx.get("nginx_bin"),
            "status": "present" if available(nginx) else "missing",
            "access": "local-build/read-only-executable",
        },
        {
            "name": "ngx_http_modsecurity_module.so",
            "env_var": "MRTS_NATIVE_NGINX_MODULE_DIR",
            "path": nginx.get("module_file"),
            "status": "present" if available(nginx) else "missing",
            "access": "local-build/module-reference",
        },
        {
            "name": "haproxy",
            "env_var": "HAPROXY_BIN",
            "path": haproxy.get("haproxy_bin"),
            "status": "present" if available(haproxy) else "missing",
            "access": "local-build/read-only-executable",
        },
        {
            "name": "haproxy-modsecurity-spoa",
            "env_var": "SPOA_RUNTIME_BIN",
            "path": haproxy.get("spoa_runtime_bin"),
            "status": "present" if available(haproxy) else "missing",
            "access": "local-build/read-only-executable",
        },
    ]


def runtime_build_cache_payload(modsecurity: dict[str, Any], connectors: list[dict[str, Any]]) -> dict[str, Any]:
    rebuilt = sum(1 for item in connectors if item.get("status") == "built")
    reused = sum(1 for item in connectors if item.get("status") == "reused")
    blocked = sum(1 for item in connectors if item.get("status") == "blocked")
    failed = sum(1 for item in connectors if item.get("status") == "failed")
    shared_id = modsecurity.get("build_id", "")
    mismatches = [
        item.get("connector", "")
        for item in connectors
        if item.get("status") in {"built", "reused", "present"}
        and item.get("modsecurity_build_id") != shared_id
    ]
    return {
        "generated_at": utc_now(),
        "shared_modsecurity_build": modsecurity,
        "connector_builds": connectors,
        "build_reuse_summary": {
            "rebuilt_count": rebuilt,
            "reused_count": reused,
            "blocked_count": blocked,
            "failed_count": failed,
            "saved_rebuilds_estimate": reused,
            "modsecurity_build_status": modsecurity.get("status", ""),
            "modsecurity_build_id_mismatches": mismatches,
            "status": "blocked" if mismatches else "ok",
            "blocker_reason": "modsecurity_build_id_mismatch" if mismatches else "",
        },
    }


def runtime_build_cache_markdown(payload: dict[str, Any]) -> str:
    modsecurity = payload.get("shared_modsecurity_build", {})
    summary = payload.get("build_reuse_summary", {})
    lines = [
        "# Runtime Build Cache",
        "",
        f"Generated at: `{payload.get('generated_at', '-')}`",
        "",
        "## Shared ModSecurity Build",
        f"- Status: `{modsecurity.get('status', '-')}`",
        f"- Blocker: `{modsecurity.get('blocker_reason') or '-'}`",
        f"- Source URL: `{modsecurity.get('source_url', '-')}`",
        f"- Source ref: `{modsecurity.get('source_ref', '-')}`",
        f"- Actual SHA: `{modsecurity.get('actual_sha', '-')}`",
        f"- Build ID: `{modsecurity.get('build_id', '-')}`",
        f"- Prefix: `{modsecurity.get('prefix', '-')}`",
        f"- Include dir: `{modsecurity.get('include_dir', '-')}`",
        f"- Lib dir: `{modsecurity.get('lib_dir', '-')}`",
        f"- libmodsecurity: `{modsecurity.get('lib_file', '-')}`",
        f"- pkg-config path: `{modsecurity.get('pkg_config_path', '-')}`",
        f"- Dependency hash: `{modsecurity.get('dependency_hash', '-')}`",
        f"- Submodules recursive: `{modsecurity.get('submodules_recursive', '-')}`",
        f"- Submodule status: `{modsecurity.get('submodule_status') or '-'}`",
        "",
        "## Connector Builds",
        "| Connector | Status | Connector build ID | ModSecurity build ID | Invalidation reason | Binary | Module | Config | Blocker |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for item in payload.get("connector_builds", []):
        outputs = item.get("output_paths", {})
        lines.append(
            "| {connector} | {status} | `{connector_id}` | `{modsec_id}` | {reason} | `{binary}` | `{module}` | `{config}` | {blocker} |".format(
                connector=item.get("connector", "-"),
                status=item.get("status", "-"),
                connector_id=item.get("connector_build_id", "-"),
                modsec_id=item.get("modsecurity_build_id", "-"),
                reason=item.get("invalidation_reason") or "-",
                binary=outputs.get("binary", "-"),
                module=outputs.get("module", "-"),
                config=outputs.get("config", "-"),
                blocker=item.get("blocker_reason") or "-",
            )
        )
    lines.extend(
        [
            "",
            "## Build Reuse Summary",
            f"- Rebuilt count: `{summary.get('rebuilt_count', '-')}`",
            f"- Reused count: `{summary.get('reused_count', '-')}`",
            f"- Blocked count: `{summary.get('blocked_count', '-')}`",
            f"- Saved rebuilds estimate: `{summary.get('saved_rebuilds_estimate', '-')}`",
            f"- Mismatch status: `{summary.get('status', '-')}`",
            f"- Mismatch blocker: `{summary.get('blocker_reason') or '-'}`",
        ]
    )
    return "\n".join(lines) + "\n"


def markdown_report(payload: dict[str, Any]) -> str:
    apache = payload.get("apache_httpd", {})
    nginx = payload.get("nginx", {})
    haproxy = payload.get("haproxy", {})
    modsecurity = payload.get("modsecurity", {})
    go_ftw = payload.get("go_ftw", {})
    albedo = payload.get("albedo", {})
    expat = payload.get("expat", {})
    lines = [
        "# Runtime Component Cache",
        "",
        f"Generated at: `{payload['generated_at']}`",
        f"Cache root: `{payload['cache_root']}`",
        f"Cache schema: `{payload.get('cache_schema_version', '-')}`",
        f"Cache manifest status: `{payload.get('status', '-')}`",
        "",
        "## Prepare Phases",
    ]
    for phase in payload.get("prepare_phases", []):
        lines.append(f"- {phase}")
    lines.extend(
        [
            "",
            "## Shared ModSecurity",
            f"- Status: `{modsecurity.get('status', '-')}`",
            f"- Blocker: `{modsecurity.get('blocker_reason') or '-'}`",
            f"- Source ref: `{modsecurity.get('source_ref') or '-'}`",
            f"- Actual SHA: `{modsecurity.get('actual_sha') or '-'}`",
            f"- Build ID: `{modsecurity.get('build_id') or '-'}`",
            f"- Prefix: `{modsecurity.get('prefix') or '-'}`",
            f"- Include dir: `{modsecurity.get('include_dir') or '-'}`",
            f"- Lib dir: `{modsecurity.get('lib_dir') or '-'}`",
            "",
            "## Apache httpd",
            f"- Status: `{apache.get('status', '-')}`",
            f"- Blocker: `{apache.get('blocker_reason') or '-'}`",
            f"- Connector build ID: `{apache.get('connector_build_id') or '-'}`",
            f"- Uses ModSecurity build ID: `{apache.get('modsecurity_build_id') or '-'}`",
            f"- Source: `{apache.get('source', '-')}`",
            f"- Expected ref/version: `{apache.get('expected_ref', '-')}`",
            f"- Cache path: `{apache.get('cache_path', '-')}`",
            f"- Build path: `{apache.get('build_path', '-')}`",
            f"- apachectl/APACHECTL_BIN: `{apache.get('apachectl_bin', '-')}`",
            f"- Missing file: `{apache.get('missing_file') or '-'}`",
            f"- Build component: `{apache.get('build_component') or '-'}`",
            f"- Env variable to set: `{apache.get('env_variable_can_set') or apache.get('env_override') or '-'}`",
            f"- Expat source: `{apache.get('expat_source') or '-'}`",
            f"- Expat release tag: `{apache.get('expat_release_tag') or '-'}`",
            f"- CPPFLAGS: `{apache.get('cppflags') or '-'}`",
            f"- LDFLAGS: `{apache.get('ldflags') or '-'}`",
            f"- LIBS: `{apache.get('libs') or '-'}`",
            f"- PKG_CONFIG_PATH: `{apache.get('pkg_config_path') or '-'}`",
            f"- crypt.h status: `{apache.get('crypt_h_status') or '-'}`",
            f"- crypt.h path: `{apache.get('crypt_h_path') or '-'}`",
            f"- libcrypt status: `{apache.get('libcrypt_status') or '-'}`",
            f"- libcrypt paths: `{', '.join(apache.get('libcrypt_paths', [])) or '-'}`",
            f"- crypt link mode: `{apache.get('crypt_link_mode') or '-'}`",
            "",
            "## NGINX",
            f"- Status: `{nginx.get('status', '-')}`",
            f"- Blocker: `{nginx.get('blocker_reason') or '-'}`",
            f"- Connector build ID: `{nginx.get('connector_build_id') or '-'}`",
            f"- Uses ModSecurity build ID: `{nginx.get('modsecurity_build_id') or '-'}`",
            f"- Source: `{nginx.get('source', '-')}`",
            f"- Expected ref/version: `{nginx.get('expected_ref', '-')}`",
            f"- Cache path: `{nginx.get('cache_path', '-')}`",
            f"- Build path: `{nginx.get('build_path', '-')}`",
            f"- MRTS_NATIVE_NGINX_BIN: `{nginx.get('nginx_bin', '-')}`",
            f"- MRTS_NATIVE_NGINX_MODULE_DIR: `{nginx.get('module_dir', '-')}`",
            f"- Module file: `{nginx.get('module_file', '-')}`",
            f"- Missing file: `{nginx.get('missing_file') or '-'}`",
            f"- Build component: `{nginx.get('build_component') or '-'}`",
            f"- Env variable to set: `{nginx.get('env_variable_can_set') or nginx.get('env_override') or '-'}`",
            "",
            "## HAProxy",
            f"- Status: `{haproxy.get('status', '-')}`",
            f"- Blocker: `{haproxy.get('blocker_reason') or '-'}`",
            f"- Connector build ID: `{haproxy.get('connector_build_id') or '-'}`",
            f"- Uses ModSecurity build ID: `{haproxy.get('modsecurity_build_id') or '-'}`",
            f"- HAPROXY_BIN: `{haproxy.get('haproxy_bin') or '-'}`",
            f"- SPOA_RUNTIME_BIN: `{haproxy.get('spoa_runtime_bin') or '-'}`",
            f"- MODSECURITY_BINDING_DIR: `{haproxy.get('modsecurity_binding_dir') or '-'}`",
            "",
            "## Expat",
            f"- Status: `{expat.get('status', '-')}`",
            f"- Blocker: `{expat.get('blocker_reason') or '-'}`",
            f"- Source: `{expat.get('source', '-')}`",
            f"- Release tag: `{expat.get('release_tag') or expat.get('expected_ref') or '-'}`",
            f"- Actual head: `{expat.get('actual_head') or '-'}`",
            f"- Prefix: `{expat.get('prefix') or '-'}`",
            f"- expat.h: `{expat.get('expat_h') or '-'}`",
            f"- lib dir: `{expat.get('lib_dir') or '-'}`",
            f"- Recursive submodules: `{expat.get('recursive_submodule_status') or '-'}`",
            "",
            "## go-ftw / albedo",
            "| Dependency | Status | Env override | Source | Release tag | Head | Binary | Submodules | Release note | Blocker |",
            "|---|---|---|---|---|---|---|---|---|---|",
        ]
    )
    for item in (go_ftw, albedo):
        lines.append(
            "| {dep} | {status} | `{env}` | `{source}` | `{ref}` | `{head}` | `{binary}` | `{subs}` | {note} | {blocker} |".format(
                dep=item.get("dependency", "-"),
                status=item.get("status", "-"),
                env=item.get("env_override", "-"),
                source=item.get("known_source") or "-",
                ref=item.get("release_tag") or item.get("known_ref") or "-",
                head=item.get("actual_head") or "-",
                binary=item.get("binary") or item.get("path") or "-",
                subs=item.get("recursive_submodule_status") or "-",
                note=item.get("release_tag_deviation_note") or "-",
                blocker=item.get("blocker_reason") or "-",
            )
        )
    lines.extend(
        [
        "",
        "## Git Components",
        "| Name | Status | Ref | Head | Submodules | fsck | Blocker |",
        "|---|---|---|---|---:|---|---|",
        ]
    )
    for item in payload["git_components"]:
        lines.append(
            "| {name} | {status} | `{ref}` | `{head}` | {subs} | {fsck} | {blocker} |".format(
                name=item.get("name", "-"),
                status=item.get("status", "-"),
                ref=item.get("expected_ref", "-"),
                head=item.get("actual_head", "-"),
                subs=item.get("submodule_count", 0),
                fsck=item.get("git_fsck", "-"),
                blocker=item.get("blocker_reason", "-") or "-",
            )
        )
    lines.extend(["", "## Archives", "| Name | Status | Checksum | Path | Blocker |", "|---|---|---|---|---|"])
    for item in payload["archives"]:
        lines.append(
            "| {name} | {status} | {checksum} | `{path}` | {blocker} |".format(
                name=item.get("name", "-"),
                status=item.get("status", "-"),
                checksum=item.get("checksum_status", "-"),
                path=item.get("path", "-"),
                blocker=item.get("blocker_reason", "-") or "-",
            )
        )
    lines.extend(["", "## Local Dependencies", "| Name | Status | Env | Path | Access |", "|---|---|---|---|---|"])
    for item in payload["dependencies"]:
        lines.append(
            "| {name} | {status} | `{env}` | `{path}` | {access} |".format(
                name=item.get("name", "-"),
                status=item.get("status", "-"),
                env=item.get("env_var", "-"),
                path=item.get("path") or item.get("configured") or "-",
                access=item.get("access", "-"),
            )
        )
    lines.extend(
        [
            "",
            "## Guardrails",
            "- System paths are not used for runtime component writes.",
            "- Runtime writes are constrained to cache/build/runtime roots.",
            "- Native Apache and NGINX use local prepared components when env overrides are absent.",
            "- go-ftw, albedo, and expat are prepared from explicit release-tag sources.",
            "- `RUNTIME_COMPONENT_STRICT_VERIFY=1` forces full git fsck.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    global PATH_POLICY_ENV

    parser = argparse.ArgumentParser()
    parser.add_argument("--connector-root", required=True)
    parser.add_argument("--framework-root", required=True)
    parser.add_argument("--cache-root", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument(
        "--runtime-env-snapshot",
        default=os.environ.get("RUNTIME_COMPONENT_ENV_SNAPSHOT", ""),
        help=(
            "Invocation-local runtime environment export file.  When omitted, "
            "a unique file is allocated below --output-root."
        ),
    )
    parser.add_argument("--build-root", default=None)
    parser.add_argument("--native-root", default=None)
    parser.add_argument(
        "--target-connector",
        choices=("all", "shared", "apache", "nginx", "haproxy"),
        default=os.environ.get("RUNTIME_COMPONENT_TARGET", "all"),
        help="Prepare shared dependencies, one native connector, or all native connectors.",
    )
    args = parser.parse_args()
    target_connector = args.target_connector

    initial_env = dict(os.environ)
    connector_root = Path(args.connector_root).resolve()
    framework_root = Path(args.framework_root).resolve()
    env, common_status = load_framework_environment(connector_root, framework_root, initial_env)
    if common_status != "loaded":
        print(f"prepare-runtime-components: BLOCKED: framework common.sh could not be loaded ({common_status})")
        return 77
    cache_root = Path(args.cache_root).resolve()
    output_root = Path(args.output_root).resolve()
    requested_runtime_env_snapshot: Path | None = None
    if args.runtime_env_snapshot:
        try:
            requested_runtime_env_snapshot = snapshot_path_within_output_root(
                Path(args.runtime_env_snapshot), output_root
            )
        except RuntimeError as exc:
            print(f"prepare-runtime-components: BLOCKED runtime env snapshot: {exc}")
            return 77
    build_root = Path(args.build_root or env.get("BUILD_ROOT", str(default_state_home() / "ModSecurity-conector-build"))).resolve()
    native_root = Path(args.native_root or env.get("MRTS_NATIVE_ROOT", str(build_root / "mrts-native"))).resolve()
    env.update(
        {
            "REPO_ROOT": str(connector_root),
            "CONNECTOR_ROOT": str(connector_root),
            "FRAMEWORK_ROOT": str(framework_root),
            "CONNECTOR_COMPONENT_CACHE": str(cache_root),
            "BUILD_ROOT": str(build_root),
            "MRTS_NATIVE_ROOT": str(native_root),
        }
    )
    PATH_POLICY_ENV = dict(env)
    try:
        validate_https_url_config(env)
        go_ftw_source_url = require_env_value(env, "GO_FTW_SOURCE_URL")
        go_ftw_expected_latest = require_env_value(env, "GO_FTW_PROMPT_EXPECTED_LATEST")
        albedo_source_url = require_env_value(env, "ALBEDO_SOURCE_URL")
        albedo_expected_latest = require_env_value(env, "ALBEDO_PROMPT_EXPECTED_LATEST")
        expat_source_url = require_env_value(env, "EXPAT_SOURCE_URL")
        expat_git_ref = require_env_value(env, "EXPAT_GIT_REF")
    except RuntimeError as exc:
        print(f"prepare-runtime-components: BLOCKED: {exc}")
        return 77
    report_dir = output_root / GENERATED_ROOT
    strict = env.get("RUNTIME_COMPONENT_STRICT_VERIFY") == "1"
    try:
        cache_root = ensure_managed_cache_root(
            cache_root,
            protected_paths=(connector_root, framework_root),
        )
    except RuntimeError as exc:
        print(f"prepare-runtime-components: BLOCKED cache: {exc}")
        return 77
    for label, path in (("BUILD_ROOT", build_root), ("MRTS_NATIVE_ROOT", native_root)):
        if is_system_path(path):
            print(f"prepare-runtime-components: BLOCKED {label}: system_path_write_forbidden path={path}")
            return 77
    build_root.mkdir(parents=True, exist_ok=True)
    native_root.mkdir(parents=True, exist_ok=True)

    previous_manifest = read_json(cache_root / "manifest.json")
    previous_git = {
        str(item.get("name")): item
        for item in previous_manifest.get("git_components", [])
        if isinstance(item, dict) and item.get("name")
    }

    sources_root = cache_root / "sources"
    archives_root = cache_root / "archives"
    git_root = cache_root / "git"
    modsec_path = sources_root / "ModSecurity_V3"
    crs_path = sources_root / "coreruleset"
    haproxy_source_root = sources_root / "haproxy"
    prepare_phases = [
        "1. validate safe paths",
        "2. prepare git/source/archive cache recursively",
        "3. prepare/build expat local prefix",
        "4. prepare/build shared ModSecurity v3 once per source/ref/build config",
        "5. prepare/reuse connector builds keyed by connector inputs and ModSecurity build ID",
        "6. prepare/build go-ftw from latest release tag",
        "7. prepare/build albedo from latest release tag",
        "8. write manifests/reports",
    ]

    git_components = [
        prepare_git_component(
            "modsecurity-v3",
            env.get("MODSECURITY_V3_GIT_URL") or env.get("MODSECURITY_REPO_URL", ""),
            env.get("MODSECURITY_V3_GIT_REF") or env.get("MODSECURITY_GIT_REF", ""),
            modsec_path,
            previous_git,
            strict,
            cache_root=cache_root,
        ),
        prepare_release_git_component(
            "expat",
            env.get("EXPAT_GIT_URL") or expat_source_url,
            env.get("EXPAT_PROMPT_EXPECTED_LATEST") or expat_git_ref,
            git_root / "libexpat",
            previous_git,
            strict,
            cache_root=cache_root,
        ),
    ]
    if target_connector == "all":
        git_components.extend(
            [
                prepare_git_component(
                    "coreruleset",
                    env.get("CRS_REPO_URL", ""),
                    env.get("CRS_GIT_REF", ""),
                    crs_path,
                    previous_git,
                    strict,
                    cache_root=cache_root,
                ),
                prepare_release_git_component(
                    "go-ftw",
                    go_ftw_source_url,
                    go_ftw_expected_latest,
                    git_root / "go-ftw",
                    previous_git,
                    strict,
                    optional=True,
                    cache_root=cache_root,
                ),
                prepare_release_git_component(
                    "albedo",
                    albedo_source_url,
                    albedo_expected_latest,
                    git_root / "albedo",
                    previous_git,
                    strict,
                    optional=True,
                    cache_root=cache_root,
                ),
            ]
        )
    if env.get("ALLOW_EXTERNAL_CONNECTOR_REPOS") == "1":
        for name, url_key, ref_key in (
            ("modsecurity-apache", "MODSECURITY_APACHE_GIT_URL", "MODSECURITY_APACHE_GIT_REF"),
            ("modsecurity-nginx", "MODSECURITY_NGINX_GIT_URL", "MODSECURITY_NGINX_GIT_REF"),
        ):
            url = env.get(url_key, "")
            ref = env.get(ref_key, "")
            if not url or not ref:
                git_components.append(
                    {
                        "name": name,
                        "url": url,
                        "expected_ref": ref,
                        "path": str(sources_root / name),
                        "status": "blocked",
                        "blocker_reason": "missing_url_or_ref",
                    }
                )
            else:
                git_components.append(
                    prepare_git_component(
                        name,
                        url,
                        ref,
                        sources_root / name,
                        previous_git,
                        strict,
                        cache_root=cache_root,
                    )
                )

    archives: list[dict[str, Any]] = []
    if target_connector in {"all", "apache"}:
        archives.extend(
            [
                prepare_archive("httpd", env.get("HTTPD_SOURCE_URL", ""), env.get("HTTPD_SHA256", ""), env.get("HTTPD_SHA256_URL", ""), archives_root / "apache", cache_root),
                prepare_archive("apr", env.get("APR_SOURCE_URL", ""), env.get("APR_SHA256", ""), env.get("APR_SHA256_URL", ""), archives_root / "apache", cache_root),
                prepare_archive("apr-util", env.get("APR_UTIL_SOURCE_URL", ""), env.get("APR_UTIL_SHA256", ""), env.get("APR_UTIL_SHA256_URL", ""), archives_root / "apache", cache_root),
                prepare_archive("pcre2", env.get("PCRE2_SOURCE_URL", ""), env.get("PCRE2_SHA256", ""), env.get("PCRE2_SHA256_URL", ""), archives_root / "apache", cache_root),
            ]
        )
    if target_connector in {"all", "haproxy"}:
        archives.append(
            prepare_archive("haproxy", env.get("HAPROXY_SOURCE_URL", ""), env.get("HAPROXY_SHA256", ""), env.get("HAPROXY_SHA256_URL", ""), archives_root / "haproxy", cache_root)
        )
    if target_connector in {"all", "nginx"}:
        try:
            nginx_tag, nginx_url, nginx_lookup_status = resolve_nginx_archive(env, archives_root / "nginx/nginx-latest-release.json")
            nginx_record = prepare_archive("nginx", nginx_url, env.get("NGINX_SHA256", ""), "", archives_root / "nginx", cache_root)
            nginx_record["resolved_tag"] = nginx_tag
            nginx_record["release_lookup_status"] = nginx_lookup_status
            archives.append(nginx_record)
        except Exception as exc:
            archives.append({"name": "nginx", "status": "blocked", "blocker_reason": network_blocker_reason(exc), "checksum_status": "unknown"})

    git_by_name = {str(item.get("name")): item for item in git_components if isinstance(item, dict)}
    expat = prepare_expat(env, cache_root, build_root, git_by_name.get("expat", {}))
    modsecurity = prepare_shared_modsecurity(
        env,
        cache_root,
        build_root,
        git_by_name.get("modsecurity-v3", {}),
        expat,
        connector_root,
    )
    connector_plans = {
        name: connector_plan(connector_root, framework_root, cache_root, env, name, modsecurity, expat, archives)
        for name in ("apache", "nginx", "haproxy")
    }
    def not_selected(name: str) -> dict[str, Any]:
        return {
            "connector": name,
            "name": name,
            "status": "not_selected",
            "blocker_reason": "",
            "modsecurity_build_id": modsecurity.get("build_id", ""),
        }

    apache_httpd = (
        prepare_apache_httpd(
            env,
            connector_root,
            framework_root,
            cache_root,
            build_root,
            sources_root,
            archives_root,
            expat,
            modsecurity,
            connector_plans["apache"],
        )
        if target_connector in {"all", "apache"}
        else not_selected("apache")
    )
    nginx = (
        prepare_nginx_runtime(
            env,
            connector_root,
            framework_root,
            cache_root,
            build_root,
            sources_root,
            archives_root,
            modsecurity,
            connector_plans["nginx"],
        )
        if target_connector in {"all", "nginx"}
        else not_selected("nginx")
    )
    haproxy = (
        prepare_haproxy_runtime(
            env,
            connector_root,
            framework_root,
            cache_root,
            build_root,
            sources_root,
            archives_root,
            modsecurity,
            connector_plans["haproxy"],
        )
        if target_connector in {"all", "haproxy"}
        else not_selected("haproxy")
    )
    if target_connector == "all":
        go_ftw = prepare_go_tool("go-ftw", "GO_FTW_BIN", cache_root, build_root, git_by_name.get("go-ftw", {}), optional=True)
        albedo = prepare_go_tool("albedo", "ALBEDO_BIN", cache_root, build_root, git_by_name.get("albedo", {}), optional=True)
    else:
        go_ftw = {"dependency": "go-ftw", "name": "go-ftw", "status": "not_selected", "blocker_reason": ""}
        albedo = {"dependency": "albedo", "name": "albedo", "status": "not_selected", "blocker_reason": ""}

    runtime_env = {
        "CONNECTOR_COMPONENT_CACHE": str(cache_root),
        "SOURCE_ROOT": str(sources_root),
        "MODSECURITY_SOURCE_DIR": str(modsec_path),
        "MODSECURITY_V3_SOURCE_DIR": str(modsec_path),
        "MODSECURITY_V3_ROOT": str(modsec_path),
        "CRS_SOURCE_DIR": str(crs_path),
        "APACHE_DOWNLOAD_DIR": str(archives_root / "apache"),
        "NGINX_DOWNLOAD_DIR": str(archives_root / "nginx"),
        "HAPROXY_SOURCE_ROOT": str(haproxy_source_root),
        "HAPROXY_DOWNLOAD_DIR": str(archives_root / "haproxy"),
        "HAPROXY_SOURCE_DIR": str(haproxy_source_root / f"haproxy-{env.get('HAPROXY_VERSION', '3.2.19')}"),
    }
    if modsecurity.get("status") in {"built", "reused", "present"}:
        runtime_env.update(
            {
                "MODSECURITY_SOURCE_URL": str(modsecurity.get("source_url", "")),
                "MODSECURITY_SOURCE_REF": str(modsecurity.get("source_ref", "")),
                "MODSECURITY_SOURCE_SHA": str(modsecurity.get("actual_sha", "")),
                "MODSECURITY_BUILD_FLAGS": str(modsecurity.get("build_flags", "")),
                "MODSECURITY_DEPENDENCY_HASH": str(modsecurity.get("dependency_hash", "")),
                "MODSECURITY_BUILD_ID": str(modsecurity.get("build_id", "")),
                "MODSECURITY_PREFIX": str(modsecurity.get("prefix", "")),
                "MODSECURITY_SHARED_PREFIX": str(modsecurity.get("prefix", "")),
                "MODSECURITY_INCLUDE_DIR": str(modsecurity.get("include_dir", "")),
                "MODSECURITY_LIB_DIR": str(modsecurity.get("lib_dir", "")),
                "MODSECURITY_PKG_CONFIG_PATH": str(modsecurity.get("pkg_config_path", "")),
            }
        )
    if expat.get("status") in {"present", "built"}:
        runtime_env.update(
            {
                "EXPAT_PREFIX": str(expat.get("prefix", "")),
                "CPPFLAGS": " ".join(part for part in (f"-I{Path(str(expat.get('prefix'))) / 'include'}", env.get("CPPFLAGS", "")) if part).strip(),
                "LDFLAGS": " ".join(part for part in (f"-L{expat.get('lib_dir')}", env.get("LDFLAGS", "")) if part).strip(),
                "LIBS": " ".join(part for part in (env.get("LIBS", ""), resolve_crypt_link_arg(env)) if part).strip(),
                "PKG_CONFIG_PATH": f"{expat.get('prefix')}/lib/pkgconfig{os.pathsep}{env.get('PKG_CONFIG_PATH', '')}".rstrip(os.pathsep),
                "LD_LIBRARY_PATH": f"{expat.get('lib_dir')}{os.pathsep}{env.get('LD_LIBRARY_PATH', '')}".rstrip(os.pathsep),
            }
        )
    if apache_httpd.get("status") in {"present", "built", "reused"}:
        runtime_env.update(
            {
                "APACHECTL_BIN": str(apache_httpd.get("apachectl_bin", "")),
                "APACHE_BUILD_ROOT": str(apache_httpd.get("build_path", "")),
                "APACHE_HTTPD": str(apache_httpd.get("httpd_bin", "")),
                "APXS": str(apache_httpd.get("apxs_bin", "")),
                "APXS_BIN": str(apache_httpd.get("apxs_bin", "")),
                "HTTPD_PREFIX": str(apache_httpd.get("httpd_prefix", "")),
                "PCRE2_PREFIX": str(apache_httpd.get("pcre2_prefix", "")),
                "APACHE_MODULE": str(apache_httpd.get("module_file", "")),
                "APACHE_MRTS_MODULE": str(apache_httpd.get("module_file", "")),
                "APACHE_MRTS_MODSECURITY_LIB_DIR": str(apache_httpd.get("modsecurity_lib_dir", "")),
                "APACHE_CONNECTOR_BUILD_ID": str(apache_httpd.get("connector_build_id", "")),
            }
        )
    if nginx.get("status") in {"present", "built", "reused"}:
        runtime_env.update(
            {
                "MRTS_NATIVE_NGINX_BIN": str(nginx.get("nginx_bin", "")),
                "MRTS_NATIVE_NGINX_MODULE_DIR": str(nginx.get("module_dir", "")),
                "MRTS_NATIVE_NGINX_MODULE_FILE": str(nginx.get("module_file", "")),
                "MRTS_NATIVE_NGINX_MODSECURITY_LIB_DIR": str(nginx.get("modsecurity_lib_dir", "")),
                "NGINX_BUILD_DIR": str(nginx.get("build_path", "")),
                "NGINX_PREFIX": str(nginx.get("nginx_prefix", "")),
                "NGINX_CONNECTOR_BUILD_ID": str(nginx.get("connector_build_id", "")),
            }
        )
    if haproxy.get("status") in {"built", "reused", "present"}:
        runtime_env.update(
            {
                "HAPROXY_BIN": str(haproxy.get("haproxy_bin", "")),
                "HAPROXY_RUNTIME_BUILD_DIR": str(haproxy.get("haproxy_runtime_build_dir", "")),
                "HAPROXY_RUNTIME_DIR": str(haproxy.get("haproxy_runtime_dir", "")),
                "SPOA_RUNTIME_BIN": str(haproxy.get("spoa_runtime_bin", "")),
                "MODSECURITY_BINDING_DIR": str(haproxy.get("modsecurity_binding_dir", "")),
                "HAPROXY_CONNECTOR_BUILD_ID": str(haproxy.get("connector_build_id", "")),
            }
        )
    runtime_env["RUNTIME_BUILD_CACHE_MANIFEST"] = str(report_path_from_root(report_dir, "runtime_build_cache", "json"))
    if go_ftw.get("path"):
        runtime_env["GO_FTW_BIN"] = str(go_ftw["path"])
    if albedo.get("path"):
        runtime_env["ALBEDO_BIN"] = str(albedo["path"])
    # Preserve the shared file as a backwards-compatible cache/report input.
    # It is atomically published but deliberately not a runner input: a
    # concurrent target-specific invocation may replace it after this one
    # returns.  Every invocation gets a separate local snapshot below its
    # RUNTIME_REPORT_OUTPUT_ROOT instead.
    env_path = cache_root / "runtime-env.sh"
    atomic_write_text(env_path, runtime_env_shell_text(runtime_env))
    snapshot_reserved_here = False
    if requested_runtime_env_snapshot is not None:
        runtime_env_snapshot = requested_runtime_env_snapshot
    else:
        runtime_env_snapshot = allocate_runtime_env_snapshot(output_root)
        snapshot_reserved_here = True
    try:
        runtime_env_snapshot = write_runtime_env_snapshot(
            runtime_env,
            snapshot_path=runtime_env_snapshot,
            output_root=output_root,
            target_connector=target_connector,
            cache_root=cache_root,
        )
    except Exception:
        if snapshot_reserved_here:
            try:
                runtime_env_snapshot.unlink()
            except FileNotFoundError:
                pass
        raise
    connector_builds = [apache_httpd, nginx, haproxy]
    build_cache = runtime_build_cache_payload(modsecurity, connector_builds)
    cache_records = [*git_components, *archives, modsecurity, apache_httpd, nginx, haproxy, go_ftw, albedo, expat]
    cache_manifest_status = (
        CACHE_MANIFEST_STATUS_COMPLETE
        if all(item.get("status") not in {"unknown", "blocked", "corrupt", "failed"} for item in cache_records)
        else "incomplete"
    )

    payload = {
        "cache_schema_version": CACHE_SCHEMA_VERSION,
        "status": cache_manifest_status,
        "generated_at": utc_now(),
        "cache_root": str(cache_root),
        "connector_root": str(connector_root),
        "framework_root": str(framework_root),
        "build_root": str(build_root),
        "native_root": str(native_root),
        "strict_verify": strict,
        "target_connector": target_connector,
        "prepare_phases": prepare_phases,
        "framework_runtime_config": {key: env.get(key, "") for key in COMMON_SH_CONFIG_VARS},
        "runtime_env": runtime_env,
        "git_components": git_components,
        "archives": archives,
        "modsecurity": modsecurity,
        "apache_httpd": apache_httpd,
        "nginx": nginx,
        "haproxy": haproxy,
        "go_ftw": go_ftw,
        "albedo": albedo,
        "expat": expat,
        "runtime_build_cache": build_cache,
        "dependencies": dependency_inventory(apache_httpd, nginx, haproxy, go_ftw, albedo, expat, modsecurity),
        "guardrails": {
            "system_paths_read_only": True,
            "no_new_external_sources": True,
            "fsck_cache_enabled": True,
            "native_system_apachectl_dependency": False,
            "native_system_nginx_dependency": False,
        },
    }
    write_json(cache_root / "manifest.json", payload)
    write_json(cache_root / "git-components.json", {"generated_at": payload["generated_at"], "components": git_components})
    write_json(cache_root / "runtime-build-cache.json", build_cache)
    component_metadata = build_metadata(
        generated_by="ci/prepare-runtime-components.py",
        make_target="prepare-runtime-components",
        connector_root=connector_root,
        framework_root=framework_root,
        inputs=[cache_root / "manifest.json"],
        generated_at=payload["generated_at"],
        report_key="runtime_component_cache",
    )
    build_metadata_payload = build_metadata(
        generated_by="ci/prepare-runtime-components.py",
        make_target="prepare-runtime-components",
        connector_root=connector_root,
        framework_root=framework_root,
        inputs=[cache_root / "runtime-build-cache.json"],
        generated_at=str(build_cache.get("generated_at") or payload["generated_at"]),
        report_key="runtime_build_cache",
    )
    component_json = report_path_from_root(report_dir, "runtime_component_cache", "json")
    component_md = report_path_from_root(report_dir, "runtime_component_cache", "md")
    build_json = report_path_from_root(report_dir, "runtime_build_cache", "json")
    build_md = report_path_from_root(report_dir, "runtime_build_cache", "md")
    component_json.parent.mkdir(parents=True, exist_ok=True)
    write_json(component_json, json.loads(generated_json_text(payload, component_metadata)))
    write_json(build_json, json.loads(generated_json_text(build_cache, build_metadata_payload)))
    component_md.write_text(generated_markdown_text(markdown_report(payload), component_metadata), encoding="utf-8")
    build_md.write_text(generated_markdown_text(runtime_build_cache_markdown(build_cache), build_metadata_payload), encoding="utf-8")
    postprocess = connector_root / "ci/update-runtime-reports.py"
    if postprocess.is_file():
        run([sys.executable, str(postprocess), "--connector-root", str(connector_root), "--output-root", str(output_root)])

    blocked = [
        item
        for item in git_components + archives
        if item.get("status") in {"blocked", "corrupt"} and item.get("name") not in {"nginx"}
    ]
    nginx_blocked = [item for item in archives if item.get("name") == "nginx" and item.get("status") in {"blocked", "corrupt"}]
    if nginx.get("status") not in {"present", "built", "reused"}:
        blocked.extend(nginx_blocked)
    native_components = (("apache_httpd", apache_httpd), ("nginx", nginx), ("haproxy", haproxy))
    selected_components = (
        native_components
        if target_connector == "all"
        else tuple(item for item in native_components if item[1].get("connector") == target_connector)
    )
    for component_name, component in (("modsecurity", modsecurity), *selected_components):
        if component.get("status") in {"blocked", "corrupt", "failed"}:
            blocked.append({"name": component_name, **component})
    if build_cache.get("build_reuse_summary", {}).get("status") == "blocked":
        blocked.append(
            {
                "name": "runtime_build_cache",
                "blocker_reason": build_cache.get("build_reuse_summary", {}).get("blocker_reason", "modsecurity_build_id_mismatch"),
            }
        )
    for component_name, component in (("expat", expat), ("go-ftw", go_ftw), ("albedo", albedo)):
        if component.get("status") in {"blocked", "corrupt", "failed"}:
            blocked.append({"name": component_name, **component})
    if blocked:
        for item in blocked:
            label = "FAILED" if item.get("status") == "failed" else "BLOCKED"
            print(f"prepare-runtime-components: {label} {item.get('name')}: {item.get('blocker_reason')}")
        # Once a build command ran, a non-zero exit or a missing expected
        # artifact is an execution failure.  Exit 77 remains reserved for a
        # prerequisite that prevented the build from starting.
        if any("build_exit_code" in item for item in blocked):
            return 1
        return 77
    print(f"prepare-runtime-components: cache={cache_root}")
    print(f"prepare-runtime-components: report={component_md}")
    print(f"prepare-runtime-components: runtime-env-snapshot={runtime_env_snapshot}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
