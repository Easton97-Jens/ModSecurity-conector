#!/usr/bin/env python3
from __future__ import annotations

import os
import stat
from pathlib import Path
from typing import Any, Mapping


DEFAULT_RUN_BASENAME = "ModSecurity-conector-verified"
WORKER_BLOCKED_REASON = "BLOCKED: nginx worker cannot access harness docroot"
SYSTEM_WRITE_PREFIXES = (
    "/usr",
    "/usr/local",
    "/opt",
    "/etc",
    "/lib",
    "/lib64",
    "/bin",
    "/sbin",
    "/run",
    "/root",
)
SYSTEM_WRITE_VAR_ALLOWLIST = (
    "/var/tmp",
)
TRUSTED_SHARED_TEMP_DIRECTORIES = (Path("/tmp"), Path("/var/tmp"))
READ_ONLY_SOURCE_MOUNT_ROOTS = (Path("/src"),)
BROAD_RUNTIME_ROOTS = (
    Path("/"),
    Path("/tmp"),
    Path("/var/tmp"),
    Path("/home"),
)
WRITABLE_RUNTIME_PATH_KEYS = (
    "VERIFIED_RUN_ROOT",
    "VERIFIED_STATE_ROOT",
    "VERIFIED_BUILD_ROOT",
    "VERIFIED_SOURCE_ROOT",
    "VERIFIED_TMP_ROOT",
    "VERIFIED_LOG_ROOT",
    "CACHE_ROOT",
    "VERIFIED_COMPONENT_CACHE",
    "NGINX_HARNESS_PARENT",
    "BUILD_ROOT",
    "SOURCE_ROOT",
    "TMP_ROOT",
    "LOG_ROOT",
    "CONNECTOR_COMPONENT_CACHE",
    "MATRIX_ROOT",
    "MRTS_BUILD_ROOT",
    "MRTS_NATIVE_ROOT",
)


def _absolute_path_without_resolution(path: Path | str) -> Path:
    """Normalize a path lexically without following a possible symlink."""
    return Path(os.path.abspath(os.fspath(path)))


def _contains_symbolic_link(path: Path | str) -> bool:
    """Return whether an existing component would redirect this path."""
    absolute = _absolute_path_without_resolution(path)
    try:
        return absolute.resolve(strict=False) != absolute
    except OSError:
        return True


def _runtime_path(path: Path | str, label: str) -> Path:
    absolute = _absolute_path_without_resolution(path)
    if _contains_symbolic_link(absolute):
        raise ValueError(f"{label} must not use symbolic links: {absolute}")
    return absolute


def _env_value(env: Mapping[str, str], name: str) -> str:
    return str(env.get(name) or "").strip()


def _matches_path_prefix(path: Path, prefix: str) -> bool:
    text = str(path)
    return text == prefix or text.startswith(prefix + "/")


def canonical_project_roots() -> tuple[Path, Path]:
    """Return repository-owned source roots without consulting mutable environment values."""
    module_path = Path(__file__).resolve(strict=False)
    connector_root = next(
        (parent for parent in module_path.parents if (parent / "Makefile").is_file()),
        None,
    )
    if connector_root is None:
        raise RuntimeError("unable to locate the canonical connector repository root")
    framework_root = connector_root / "modules" / "ModSecurity-test-Framework"
    return (connector_root, framework_root)


def fixed_runtime_temp_parent() -> Path:
    """Return the fixed policy temp parent, never a writable run root.

    The environment cannot select this fallback. Callers must derive and
    validate a narrow child before using it for runtime artifacts.
    """
    return Path(SYSTEM_WRITE_VAR_ALLOWLIST[0])


def default_verified_run_root(env: Mapping[str, str] | None = None) -> Path:
    values = env or os.environ
    parent_value = _env_value(values, "RUNNER_TEMP") or _env_value(values, "TMPDIR")
    fallback_parent = fixed_runtime_temp_parent()
    parent = (
        _absolute_path_without_resolution(parent_value)
        if parent_value
        else fallback_parent
    )
    if not is_safe_runtime_parent(parent):
        parent = fallback_parent
    return parent / DEFAULT_RUN_BASENAME


def is_under(path: Path, root: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(root.resolve(strict=False))
        return True
    except ValueError:
        return False


def is_under_root_home(path: Path) -> bool:
    return is_under(path, Path("/root"))


def is_read_only_source_path(path: Path) -> bool:
    resolved = path.resolve(strict=False)
    return any(
        resolved == root.resolve(strict=False) or is_under(resolved, root)
        for root in (*READ_ONLY_SOURCE_MOUNT_ROOTS, *canonical_project_roots())
    )


def is_configured_project_path(path: Path, env: Mapping[str, str] | None = None) -> bool:
    """Compatibility helper that deliberately ignores mutable project-root inputs.

    ``REPO_ROOT``, ``CONNECTOR_ROOT``, and ``FRAMEWORK_ROOT`` are location
    hints.  They are not write authorization.  Known source locations remain
    recognizable only for callers that need to preserve read-only source use.
    """
    del env
    return is_read_only_source_path(path)


def is_safe_runtime_parent(path: Path) -> bool:
    """Return whether an invocation parent is safe to derive a child run root."""
    if _contains_symbolic_link(path):
        return False
    resolved = _absolute_path_without_resolution(path)
    if (
        resolved == Path("/")
        or resolved.parent == Path("/")
        or is_read_only_source_path(resolved)
    ):
        return False
    text = str(resolved)
    if text == "/var" or text.startswith("/var/"):
        fixed_parent = fixed_runtime_temp_parent()
        return resolved == fixed_parent or is_under(resolved, fixed_parent)
    return not any(_matches_path_prefix(resolved, prefix) for prefix in SYSTEM_WRITE_PREFIXES)


def is_safe_runtime_root(path: Path) -> bool:
    """Return whether an exact invocation root is narrow enough for writes."""
    if _contains_symbolic_link(path):
        return False
    resolved = _absolute_path_without_resolution(path)
    return resolved not in BROAD_RUNTIME_ROOTS and is_safe_runtime_parent(resolved)


def is_system_write_path(path: Path, env: Mapping[str, str] | None = None) -> bool:
    del env
    resolved = path.resolve(strict=False)
    if is_read_only_source_path(resolved):
        return True
    text = str(resolved)
    if text == "/var":
        return True
    if text.startswith("/var/"):
        for prefix in SYSTEM_WRITE_VAR_ALLOWLIST:
            if text == prefix or text.startswith(prefix + "/"):
                return False
        return True
    return any(text == prefix or text.startswith(prefix + "/") for prefix in SYSTEM_WRITE_PREFIXES)


def allowed_runtime_roots(env: Mapping[str, str] | None = None) -> list[Path]:
    values = env or os.environ
    try:
        paths = verified_runtime_paths(values)
    except ValueError:
        paths = {}
    roots = [Path(paths["VERIFIED_RUN_ROOT"])] if paths else []
    roots.extend((*READ_ONLY_SOURCE_MOUNT_ROOTS, *canonical_project_roots()))
    normalized: list[Path] = []
    for root in roots:
        resolved = root.resolve(strict=False)
        if not (is_safe_runtime_root(resolved) or is_read_only_source_path(resolved)):
            continue
        if resolved not in normalized:
            normalized.append(resolved)
    return normalized


def is_allowed_runtime_path(path: Path, env: Mapping[str, str] | None = None) -> bool:
    resolved = path.resolve(strict=False)
    return any(resolved == root or is_under(resolved, root) for root in allowed_runtime_roots(env))


def verified_runtime_paths(
    env: Mapping[str, str] | None = None,
    *,
    build_root_override: Path | str | None = None,
) -> dict[str, str]:
    values = env or os.environ
    run_root = _runtime_path(
        _env_value(values, "VERIFIED_RUN_ROOT") or default_verified_run_root(values),
        "VERIFIED_RUN_ROOT",
    )
    if not is_safe_runtime_root(run_root):
        raise ValueError(f"VERIFIED_RUN_ROOT is unsafe for runtime writes: {run_root}")
    state_root = _runtime_path(
        _env_value(values, "VERIFIED_STATE_ROOT") or run_root / "state",
        "VERIFIED_STATE_ROOT",
    )
    verified_build_root = _runtime_path(
        _env_value(values, "VERIFIED_BUILD_ROOT") or run_root / "build",
        "VERIFIED_BUILD_ROOT",
    )
    verified_source_root = _runtime_path(
        _env_value(values, "VERIFIED_SOURCE_ROOT") or run_root / "src",
        "VERIFIED_SOURCE_ROOT",
    )
    verified_tmp_root = _runtime_path(
        _env_value(values, "VERIFIED_TMP_ROOT") or run_root / "tmp",
        "VERIFIED_TMP_ROOT",
    )
    verified_log_root = _runtime_path(
        _env_value(values, "VERIFIED_LOG_ROOT") or run_root / "logs",
        "VERIFIED_LOG_ROOT",
    )
    cache_root = _runtime_path(
        _env_value(values, "CACHE_ROOT") or run_root / "cache-v2",
        "CACHE_ROOT",
    )
    verified_component_cache = _runtime_path(
        _env_value(values, "VERIFIED_COMPONENT_CACHE") or cache_root / "shared",
        "VERIFIED_COMPONENT_CACHE",
    )

    build_root = _runtime_path(
        build_root_override
        or _env_value(values, "BUILD_ROOT")
        or verified_build_root,
        "BUILD_ROOT",
    )
    source_root = _runtime_path(
        _env_value(values, "SOURCE_ROOT") or verified_source_root,
        "SOURCE_ROOT",
    )
    tmp_root = _runtime_path(
        _env_value(values, "TMP_ROOT") or verified_tmp_root,
        "TMP_ROOT",
    )
    log_root = _runtime_path(
        _env_value(values, "LOG_ROOT") or verified_log_root,
        "LOG_ROOT",
    )
    component_cache = _runtime_path(
        _env_value(values, "CONNECTOR_COMPONENT_CACHE") or verified_component_cache,
        "CONNECTOR_COMPONENT_CACHE",
    )
    nginx_harness_parent = _runtime_path(
        _env_value(values, "NGINX_HARNESS_PARENT") or run_root / "nginx-harness",
        "NGINX_HARNESS_PARENT",
    )
    matrix_root = _runtime_path(
        _env_value(values, "MATRIX_ROOT") or build_root / "full-matrix",
        "MATRIX_ROOT",
    )
    mrts_build_root = _runtime_path(
        _env_value(values, "MRTS_BUILD_ROOT") or build_root / "mrts",
        "MRTS_BUILD_ROOT",
    )
    mrts_native_root = _runtime_path(
        _env_value(values, "MRTS_NATIVE_ROOT") or build_root / "mrts-native",
        "MRTS_NATIVE_ROOT",
    )

    for label, path in (
        ("VERIFIED_STATE_ROOT", state_root),
        ("VERIFIED_BUILD_ROOT", verified_build_root),
        ("VERIFIED_SOURCE_ROOT", verified_source_root),
        ("VERIFIED_TMP_ROOT", verified_tmp_root),
        ("VERIFIED_LOG_ROOT", verified_log_root),
        ("CACHE_ROOT", cache_root),
        ("VERIFIED_COMPONENT_CACHE", verified_component_cache),
        ("NGINX_HARNESS_PARENT", nginx_harness_parent),
        ("BUILD_ROOT", build_root),
        ("SOURCE_ROOT", source_root),
        ("TMP_ROOT", tmp_root),
        ("LOG_ROOT", log_root),
        ("CONNECTOR_COMPONENT_CACHE", component_cache),
        ("MATRIX_ROOT", matrix_root),
        ("MRTS_BUILD_ROOT", mrts_build_root),
        ("MRTS_NATIVE_ROOT", mrts_native_root),
    ):
        if label == "SOURCE_ROOT" and is_read_only_source_path(path):
            continue
        if not is_safe_runtime_root(path):
            raise ValueError(f"{label} is unsafe for runtime writes: {path}")

    return {
        "VERIFIED_RUN_ROOT": str(run_root),
        "VERIFIED_STATE_ROOT": str(state_root),
        "VERIFIED_BUILD_ROOT": str(verified_build_root),
        "VERIFIED_SOURCE_ROOT": str(verified_source_root),
        "VERIFIED_TMP_ROOT": str(verified_tmp_root),
        "VERIFIED_LOG_ROOT": str(verified_log_root),
        "CACHE_ROOT": str(cache_root),
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


def ensure_safe_runtime_directory(path: Path | str) -> Path:
    """Create or open one runtime directory without following path symlinks.

    The returned leaf must be owned by the current user and not writable by
    group or other users.  Existing safe directories retain their mode so
    worker-readable directories stay compatible with the runtime harness.
    """

    directory_path = _runtime_path(path, "runtime directory")
    if not is_safe_runtime_root(directory_path):
        raise ValueError(f"runtime directory is unsafe for writes: {directory_path}")
    no_follow = getattr(os, "O_NOFOLLOW", None)
    directory_flag = getattr(os, "O_DIRECTORY", None)
    if no_follow is None or directory_flag is None:
        raise ValueError(
            "safe runtime directories require O_NOFOLLOW and O_DIRECTORY support"
        )

    descriptor = os.open("/", os.O_RDONLY | directory_flag | no_follow)
    current_path = Path("/")
    shared_temp_root: Path | None = None
    try:
        for component in directory_path.parts[1:]:
            try:
                os.mkdir(component, 0o755, dir_fd=descriptor)
            except FileExistsError:
                pass
            try:
                child_descriptor = os.open(
                    component,
                    os.O_RDONLY | directory_flag | no_follow,
                    dir_fd=descriptor,
                )
            except OSError as exc:
                raise ValueError(
                    f"runtime directory is unavailable or unsafe: {directory_path}: {exc}"
                ) from exc
            os.close(descriptor)
            descriptor = child_descriptor
            current_path /= component
            details = os.fstat(descriptor)
            if not stat.S_ISDIR(details.st_mode):
                raise ValueError(f"runtime directory is not a directory: {current_path}")
            if (
                current_path not in TRUSTED_SHARED_TEMP_DIRECTORIES
                and stat.S_IMODE(details.st_mode) & 0o022
            ):
                raise ValueError(
                    "runtime directory has a group- or world-writable ancestor: "
                    f"{current_path}"
                )
            if current_path in TRUSTED_SHARED_TEMP_DIRECTORIES:
                shared_temp_root = current_path
            elif (
                shared_temp_root is not None
                and details.st_uid not in {os.geteuid(), 0}
            ):
                raise ValueError(
                    "runtime directory has an untrusted owner below shared temporary root "
                    f"{shared_temp_root}: {current_path}"
                )

        details = os.fstat(descriptor)
        if not stat.S_ISDIR(details.st_mode):
            raise ValueError(f"runtime directory is not a directory: {directory_path}")
        if details.st_uid != os.geteuid():
            raise ValueError(
                f"runtime directory is not owned by the current user: {directory_path}"
            )
        if stat.S_IMODE(details.st_mode) & 0o022:
            raise ValueError(f"runtime directory is group- or world-writable: {directory_path}")
    finally:
        os.close(descriptor)
    return directory_path


def ensure_safe_writable_runtime_paths(paths: Mapping[str, str]) -> None:
    """Materialize every write-capable verified runtime path without following links.

    ``verified_runtime_paths()`` keeps canonical source locations available for
    read-only inputs.  All other returned locations can become write sinks in
    a lifecycle child, so create and inspect them before exporting the values.
    """

    for key in WRITABLE_RUNTIME_PATH_KEYS:
        try:
            path = Path(paths[key])
        except KeyError as exc:
            raise ValueError(f"missing verified runtime path: {key}") from exc
        if key == "SOURCE_ROOT" and is_read_only_source_path(_runtime_path(path, key)):
            continue
        ensure_safe_runtime_directory(path)


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
    del connector_root, framework_root
    read_only_source = label == "SOURCE_ROOT" and is_read_only_source_path(resolved)
    if not resolved.is_absolute():
        status = "BLOCKED"
        notes.append("path is not absolute")
    if is_system_write_path(resolved) and not read_only_source:
        status = "BLOCKED"
        notes.append("system write path is forbidden")
    if worker_compatible and is_under_root_home(resolved) and not read_only_source:
        status = "BLOCKED"
        notes.append("path is under /root and is not worker-traversable")
    safe_allowed_roots = [
        root.resolve(strict=False)
        for root in allowed_roots
        if is_safe_runtime_root(root.resolve(strict=False))
    ]
    if not read_only_source and not any(resolved == root or is_under(resolved, root) for root in safe_allowed_roots):
        status = "BLOCKED"
        notes.append("path is outside verified runtime roots")
    if read_only_source:
        notes.append("read-only source path")
    return {"variable": label, "value": str(resolved), "status": status, "notes": "; ".join(notes) or "ok"}


def runtime_path_rows(
    paths: Mapping[str, str],
    *,
    connector_root: Path,
    framework_root: Path,
) -> list[dict[str, Any]]:
    allowed = [Path(value) for value in paths.values()]
    order = (
        "VERIFIED_RUN_ROOT",
        "VERIFIED_BUILD_ROOT",
        "VERIFIED_SOURCE_ROOT",
        "VERIFIED_TMP_ROOT",
        "VERIFIED_LOG_ROOT",
        "CACHE_ROOT",
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
