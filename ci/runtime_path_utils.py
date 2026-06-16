#!/usr/bin/env python3
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Mapping


DEFAULT_RUN_BASENAME = "ModSecurity-conector-verified"
WORKER_BLOCKED_REASON = "BLOCKED: nginx worker cannot access harness docroot"
SYSTEM_WRITE_PREFIXES = (
    "/usr",
    "/usr/local",
    "/opt",
    "/etc",
    "/var/lib",
    "/var/run",
    "/var/log",
    "/lib",
    "/lib64",
    "/bin",
    "/sbin",
    "/run",
)


def _env_value(env: Mapping[str, str], name: str) -> str:
    return str(env.get(name) or "").strip()


def default_verified_run_root(env: Mapping[str, str] | None = None) -> Path:
    values = env or os.environ
    parent = _env_value(values, "RUNNER_TEMP") or _env_value(values, "TMPDIR") or "/var/tmp"
    return Path(parent) / DEFAULT_RUN_BASENAME


def is_under(path: Path, root: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(root.resolve(strict=False))
        return True
    except ValueError:
        return False


def is_under_root_home(path: Path) -> bool:
    return is_under(path, Path("/root"))


def is_system_write_path(path: Path) -> bool:
    text = str(path.resolve(strict=False))
    return any(text == prefix or text.startswith(prefix + "/") for prefix in SYSTEM_WRITE_PREFIXES)


def verified_runtime_paths(
    env: Mapping[str, str] | None = None,
    *,
    build_root_override: Path | str | None = None,
) -> dict[str, str]:
    values = env or os.environ
    run_root = Path(_env_value(values, "VERIFIED_RUN_ROOT") or default_verified_run_root(values)).resolve()
    state_root = Path(_env_value(values, "VERIFIED_STATE_ROOT") or run_root / "state").resolve()
    verified_build_root = Path(_env_value(values, "VERIFIED_BUILD_ROOT") or run_root / "build").resolve()
    verified_source_root = Path(_env_value(values, "VERIFIED_SOURCE_ROOT") or run_root / "src").resolve()
    verified_tmp_root = Path(_env_value(values, "VERIFIED_TMP_ROOT") or run_root / "tmp").resolve()
    verified_log_root = Path(_env_value(values, "VERIFIED_LOG_ROOT") or run_root / "logs").resolve()
    verified_component_cache = Path(_env_value(values, "VERIFIED_COMPONENT_CACHE") or run_root / "component-cache").resolve()

    build_root = Path(
        build_root_override
        or _env_value(values, "BUILD_ROOT")
        or verified_build_root
    ).resolve()
    source_root = Path(_env_value(values, "SOURCE_ROOT") or verified_source_root).resolve()
    tmp_root = Path(_env_value(values, "TMP_ROOT") or verified_tmp_root).resolve()
    log_root = Path(_env_value(values, "LOG_ROOT") or verified_log_root).resolve()
    component_cache = Path(_env_value(values, "CONNECTOR_COMPONENT_CACHE") or verified_component_cache).resolve()
    nginx_harness_parent = Path(_env_value(values, "NGINX_HARNESS_PARENT") or run_root / "nginx-harness").resolve()
    matrix_root = Path(_env_value(values, "MATRIX_ROOT") or build_root / "full-matrix").resolve()
    mrts_build_root = Path(_env_value(values, "MRTS_BUILD_ROOT") or build_root / "mrts").resolve()
    mrts_native_root = Path(_env_value(values, "MRTS_NATIVE_ROOT") or build_root / "mrts-native").resolve()

    return {
        "VERIFIED_RUN_ROOT": str(run_root),
        "VERIFIED_STATE_ROOT": str(state_root),
        "VERIFIED_BUILD_ROOT": str(verified_build_root),
        "VERIFIED_SOURCE_ROOT": str(verified_source_root),
        "VERIFIED_TMP_ROOT": str(verified_tmp_root),
        "VERIFIED_LOG_ROOT": str(verified_log_root),
        "VERIFIED_COMPONENT_CACHE": str(verified_component_cache),
        "NGINX_HARNESS_PARENT": str(nginx_harness_parent),
        "BUILD_ROOT": str(build_root),
        "SOURCE_ROOT": str(source_root),
        "TMP_ROOT": str(tmp_root),
        "LOG_ROOT": str(log_root),
        "CONNECTOR_COMPONENT_CACHE": str(component_cache),
        "MATRIX_ROOT": str(matrix_root),
        "MRTS_BUILD_ROOT": str(mrts_build_root),
        "MRTS_NATIVE_ROOT": str(mrts_native_root),
    }


def path_status(
    path: str | Path,
    *,
    label: str,
    connector_root: Path,
    framework_root: Path,
    allowed_roots: list[Path],
    worker_compatible: bool = False,
) -> dict[str, Any]:
    resolved = Path(path).resolve(strict=False)
    status = "PASS"
    notes: list[str] = []
    if not resolved.is_absolute():
        status = "BLOCKED"
        notes.append("path is not absolute")
    if is_system_write_path(resolved):
        status = "BLOCKED"
        notes.append("system write path is forbidden")
    if is_under(resolved, connector_root):
        status = "BLOCKED"
        notes.append("path is inside connector source checkout")
    if is_under(resolved, framework_root):
        status = "BLOCKED"
        notes.append("path is inside framework source checkout")
    if worker_compatible and is_under_root_home(resolved):
        status = "BLOCKED"
        notes.append("path is under /root and is not worker-traversable")
    if not any(resolved == root.resolve(strict=False) or is_under(resolved, root) for root in allowed_roots):
        status = "BLOCKED"
        notes.append("path is outside verified runtime roots")
    return {"variable": label, "value": str(resolved), "status": status, "notes": "; ".join(notes) or "ok"}


def runtime_path_rows(
    paths: Mapping[str, str],
    *,
    connector_root: Path,
    framework_root: Path,
) -> list[dict[str, Any]]:
    allowed = [
        Path(paths["VERIFIED_RUN_ROOT"]),
        Path(paths["VERIFIED_STATE_ROOT"]),
        Path(paths["VERIFIED_BUILD_ROOT"]),
        Path(paths["VERIFIED_SOURCE_ROOT"]),
        Path(paths["VERIFIED_TMP_ROOT"]),
        Path(paths["VERIFIED_LOG_ROOT"]),
        Path(paths["VERIFIED_COMPONENT_CACHE"]),
    ]
    order = (
        "VERIFIED_RUN_ROOT",
        "VERIFIED_BUILD_ROOT",
        "VERIFIED_SOURCE_ROOT",
        "VERIFIED_TMP_ROOT",
        "VERIFIED_LOG_ROOT",
        "VERIFIED_COMPONENT_CACHE",
        "NGINX_HARNESS_PARENT",
        "BUILD_ROOT",
        "SOURCE_ROOT",
        "TMP_ROOT",
        "LOG_ROOT",
        "CONNECTOR_COMPONENT_CACHE",
    )
    return [
        path_status(
            paths[name],
            label=name,
            connector_root=connector_root,
            framework_root=framework_root,
            allowed_roots=allowed,
            worker_compatible=name == "NGINX_HARNESS_PARENT",
        )
        for name in order
        if name in paths
    ]
