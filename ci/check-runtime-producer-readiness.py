#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from runtime_path_utils import is_system_write_path, is_under, verified_runtime_paths


def default_state_home() -> Path:
    return Path(verified_runtime_paths(os.environ)["VERIFIED_STATE_ROOT"])


def is_within(path: Path, root: Path) -> bool:
    return is_under(path, root)


def parse_export_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.strip()
        if not stripped.startswith("export ") or "=" not in stripped:
            continue
        try:
            parts = shlex.split(stripped.removeprefix("export "), posix=True)
        except ValueError:
            continue
        for part in parts:
            if "=" not in part:
                continue
            key, value = part.split("=", 1)
            if key:
                values[key] = value
    return values


def load_common_sh(connector_root: Path, framework_root: Path, env: dict[str, str]) -> dict[str, Any]:
    common_sh = framework_root / "ci/common.sh"
    if not common_sh.is_file():
        return {"status": "blocked", "return_code": 77, "path": str(common_sh), "error": "missing common.sh", "env": {}}
    proc = subprocess.run(
        ["bash", "-lc", 'set -a; . "$FRAMEWORK_ROOT/ci/common.sh"; env -0'],
        cwd=str(connector_root),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=False,
        timeout=60,
    )
    loaded: dict[str, str] = {}
    if proc.returncode == 0:
        for chunk in proc.stdout.split(b"\0"):
            if not chunk or b"=" not in chunk:
                continue
            key, value = chunk.split(b"=", 1)
            loaded[key.decode("utf-8", errors="replace")] = value.decode("utf-8", errors="replace")
    return {
        "status": "present" if proc.returncode == 0 else "blocked",
        "return_code": proc.returncode,
        "path": str(common_sh),
        "error": proc.stderr.decode("utf-8", errors="replace").strip(),
        "env": loaded,
    }


def executable(path: Path) -> bool:
    return path.is_file() and os.access(path, os.X_OK)


def executable_or_path(value: str) -> Path | None:
    if not value:
        return None
    if "/" in value:
        return Path(value)
    resolved = shutil.which(value)
    return Path(resolved) if resolved else None


def file_status(path: Path | None, *, executable_required: bool = False) -> str:
    if path is None:
        return "missing"
    if executable_required:
        return "present" if executable(path) else "missing"
    return "present" if path.is_file() else "missing"


def first_nonempty(*values: str | None) -> str:
    for value in values:
        if value:
            return value
    return ""


def status_for_required(items: list[dict[str, Any]]) -> str:
    return "PASS" if all(item["status"] == "present" for item in items) else "BLOCKED"


def status_for_optional(items: list[dict[str, Any]]) -> str:
    return "PASS" if all(item["status"] == "present" for item in items) else "WARN"


def component(
    name: str,
    status: str,
    path: Path | None,
    fix: str,
    *,
    required: bool = True,
    details: str = "",
) -> dict[str, Any]:
    return {
        "component": name,
        "required": required,
        "status": status,
        "path": str(path) if path is not None else "",
        "fix": fix,
        "details": details,
    }


def check_safe_path(path: Path, label: str, roots: dict[str, Path], connector_root: Path, framework_root: Path) -> dict[str, Any]:
    status = "PASS"
    notes: list[str] = []
    project_path_allowed = any(
        is_within(path, root) or path == root
        for root in (connector_root, framework_root)
    )
    if not path.is_absolute():
        status = "BLOCKED"
        notes.append("path is not absolute")
    if is_system_write_path(path) and not project_path_allowed:
        status = "BLOCKED"
        notes.append("system write path is forbidden")
    allowed = any(is_within(path, root) or path == root for root in roots.values())
    if project_path_allowed:
        allowed = True
    if not allowed and str(path).startswith("/tmp/"):
        allowed = True
    if not allowed:
        status = "BLOCKED"
        notes.append("path is outside allowed runtime/cache roots")
    return {"label": label, "path": str(path), "status": status, "notes": "; ".join(notes) or "ok"}


def network_cache_status(env: dict[str, str], cache_root: Path) -> list[dict[str, Any]]:
    sources = [
        ("nginx latest release", cache_root / "archives/nginx/nginx-latest-release.json"),
        ("nginx archive cache", cache_root / "archives/nginx"),
        ("go-ftw git cache", cache_root / "git/go-ftw"),
        ("albedo git cache", cache_root / "git/albedo"),
    ]
    rows = []
    for name, path in sources:
        if path.is_dir():
            status = "present" if any(path.iterdir()) else "missing"
        else:
            status = "present" if path.is_file() and path.stat().st_size > 0 else "missing"
        rows.append(
            {
                "source": name,
                "status": status,
                "path": str(path),
                "notes": "local cache available" if status == "present" else "network may be required unless this cache is prefilled",
            }
        )
    return rows


def build_payload(connector_root: Path, framework_root: Path, build_root: Path) -> dict[str, Any]:
    defaults = verified_runtime_paths(os.environ, build_root_override=build_root)
    state_home = Path(defaults["VERIFIED_STATE_ROOT"])
    cache_root = Path(os.environ.get("CONNECTOR_COMPONENT_CACHE", defaults["CONNECTOR_COMPONENT_CACHE"])).resolve()
    base_env = dict(os.environ)
    base_env.update(
        {
            "CONNECTOR_ROOT": str(connector_root),
            "FRAMEWORK_ROOT": str(framework_root),
            "BUILD_ROOT": str(build_root),
            "VERIFIED_RUN_ROOT": defaults["VERIFIED_RUN_ROOT"],
            "VERIFIED_STATE_ROOT": defaults["VERIFIED_STATE_ROOT"],
            "VERIFIED_BUILD_ROOT": defaults["VERIFIED_BUILD_ROOT"],
            "VERIFIED_SOURCE_ROOT": defaults["VERIFIED_SOURCE_ROOT"],
            "VERIFIED_TMP_ROOT": defaults["VERIFIED_TMP_ROOT"],
            "VERIFIED_LOG_ROOT": defaults["VERIFIED_LOG_ROOT"],
            "VERIFIED_COMPONENT_CACHE": defaults["VERIFIED_COMPONENT_CACHE"],
            "SOURCE_ROOT": base_env.get("SOURCE_ROOT", defaults["SOURCE_ROOT"]),
            "TMP_ROOT": base_env.get("TMP_ROOT", defaults["TMP_ROOT"]),
            "LOG_ROOT": base_env.get("LOG_ROOT", defaults["LOG_ROOT"]),
            "CONNECTOR_COMPONENT_CACHE": str(cache_root),
            "NGINX_HARNESS_PARENT": base_env.get("NGINX_HARNESS_PARENT", defaults["NGINX_HARNESS_PARENT"]),
            "MRTS_NATIVE_ROOT": base_env.get("MRTS_NATIVE_ROOT", defaults["MRTS_NATIVE_ROOT"]),
        }
    )
    common = load_common_sh(connector_root, framework_root, base_env)
    effective_env = dict(base_env)
    effective_env.update(common.get("env", {}))
    runtime_env_path = cache_root / "runtime-env.sh"
    runtime_env = parse_export_file(runtime_env_path)
    effective_env.update(runtime_env)

    nginx_prefix = Path(effective_env.get("NGINX_PREFIX", str(build_root / "nginx-runtime/nginx"))).resolve()
    nginx_bin = Path(effective_env.get("NGINX_BINARY", str(nginx_prefix / "sbin/nginx"))).resolve()
    nginx_module_dir_value = first_nonempty(effective_env.get("MRTS_NATIVE_NGINX_MODULE_DIR"), str(nginx_prefix / "modules"))
    nginx_module_file = Path(
        first_nonempty(
            effective_env.get("NGINX_MODULE"),
            effective_env.get("MRTS_NATIVE_NGINX_MODULE_FILE"),
            str(Path(nginx_module_dir_value) / "ngx_http_modsecurity_module.so"),
        )
    ).resolve()
    nginx_module_dir = nginx_module_file.parent
    modsecurity_lib_dir = Path(
        first_nonempty(
            effective_env.get("NGINX_MRTS_MODSECURITY_LIB_DIR"),
            effective_env.get("MRTS_NATIVE_NGINX_MODSECURITY_LIB_DIR"),
            effective_env.get("MODSECURITY_LIB_DIR"),
        )
    )
    modsecurity_lib = (modsecurity_lib_dir / "libmodsecurity.so").resolve() if str(modsecurity_lib_dir) else None

    apache_httpd = executable_or_path(effective_env.get("APACHE_HTTPD", ""))
    apache_module = Path(effective_env.get("APACHE_MODULE", "")).resolve() if effective_env.get("APACHE_MODULE") else None
    apxs = executable_or_path(effective_env.get("APXS_BIN") or effective_env.get("APXS", ""))
    haproxy = executable_or_path(effective_env.get("HAPROXY_BIN", ""))
    spoa = executable_or_path(effective_env.get("SPOA_RUNTIME_BIN", ""))
    haproxy_binding = Path(effective_env.get("MODSECURITY_BINDING_DIR", "")) / "paths.env" if effective_env.get("MODSECURITY_BINDING_DIR") else None
    go_ftw = executable_or_path(effective_env.get("GO_FTW_BIN", "go-ftw"))
    albedo = executable_or_path(effective_env.get("ALBEDO_BIN", "albedo"))

    required_items = [
        component("common.sh", "present" if common["status"] == "present" else "missing", Path(common["path"]), "ensure FRAMEWORK_ROOT points at modules/ModSecurity-test-Framework"),
        component("NGINX binary", file_status(nginx_bin, executable_required=True), nginx_bin, "run make prepare-runtime-components"),
        component("NGINX ModSecurity module", file_status(nginx_module_file), nginx_module_file, "run make prepare-runtime-components"),
        component("NGINX libmodsecurity", file_status(modsecurity_lib), modsecurity_lib, "run make prepare-runtime-components"),
        component("Apache/httpd", file_status(apache_httpd, executable_required=True), apache_httpd, "run make prepare-runtime-components"),
        component("Apache/APXS", file_status(apxs, executable_required=True), apxs, "run make prepare-runtime-components"),
        component("Apache ModSecurity module", file_status(apache_module), apache_module, "run make prepare-runtime-components"),
        component("HAProxy binary", file_status(haproxy, executable_required=True), haproxy, "run make prepare-runtime-components"),
        component("HAProxy SPOA runtime", file_status(spoa, executable_required=True), spoa, "run make prepare-runtime-components"),
        component("HAProxy binding metadata", file_status(haproxy_binding), haproxy_binding, "run make prepare-runtime-components"),
    ]
    optional_items = [
        component("go-ftw", file_status(go_ftw, executable_required=True), go_ftw, "optional native MRTS: install or cache go-ftw", required=False),
        component("albedo", file_status(albedo, executable_required=True), albedo, "optional native MRTS: install or cache albedo", required=False),
    ]
    roots = {
        "verified_run_root": Path(effective_env["VERIFIED_RUN_ROOT"]).resolve(),
        "state_home": state_home,
        "build_root": build_root,
        "cache_root": cache_root,
        "tmp_root": Path(effective_env["TMP_ROOT"]).resolve(),
        "log_root": Path(effective_env["LOG_ROOT"]).resolve(),
        "mrts_native_root": Path(effective_env["MRTS_NATIVE_ROOT"]).resolve(),
    }
    path_checks = [
        check_safe_path(Path(effective_env[key]).resolve(), key, roots, connector_root, framework_root)
        for key in ("BUILD_ROOT", "SOURCE_ROOT", "TMP_ROOT", "LOG_ROOT", "CONNECTOR_COMPONENT_CACHE", "NGINX_HARNESS_PARENT", "MRTS_NATIVE_ROOT")
        if effective_env.get(key)
    ]
    required_status = status_for_required(required_items)
    path_status = "PASS" if all(item["status"] == "PASS" for item in path_checks) else "BLOCKED"
    status = "PASS" if required_status == "PASS" and path_status == "PASS" else "BLOCKED"
    if status == "PASS" and status_for_optional(optional_items) == "WARN":
        status = "WARN"
    return {
        "status": status,
        "runtime_env_path": str(runtime_env_path),
        "runtime_env_loaded": runtime_env_path.is_file(),
        "common_sh": {key: value for key, value in common.items() if key != "env"},
        "paths": path_checks,
        "components": required_items + optional_items,
        "nginx_runtime_module_readiness": {
            "NGINX_BIN": str(nginx_bin),
            "NGINX_MODULE_DIR": str(nginx_module_dir),
            "ModSecurity module path": str(nginx_module_file),
            "Module exists": nginx_module_file.is_file(),
            "How to prepare": "make prepare-runtime-components",
        },
        "network_cache": network_cache_status(effective_env, cache_root),
    }


def render_text(payload: dict[str, Any]) -> str:
    lines = [f"check-runtime-producer-readiness: {payload['status']}"]
    lines.extend(
        [
            "",
            "| Component | Required | Status | Path | Fix |",
            "|---|---|---|---|---|",
        ]
    )
    for item in payload["components"]:
        lines.append(
            f"| {item['component']} | {item['required']} | {item['status']} | `{item['path'] or '-'}` | `{item['fix']}` |"
        )
    lines.extend(["", "| Path | Status | Notes |", "|---|---|---|"])
    for item in payload["paths"]:
        lines.append(f"| `{item['label']}={item['path']}` | {item['status']} | {item['notes']} |")
    lines.extend(["", "| Source | Status | Notes |", "|---|---|---|"])
    for item in payload["network_cache"]:
        lines.append(f"| {item['source']} | {item['status']} | `{item['path']}`: {item['notes']} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector-root", default=".")
    parser.add_argument("--framework-root", default=None)
    parser.add_argument("--build-root", default=os.environ.get("BUILD_ROOT"))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    connector_root = Path(args.connector_root).resolve()
    framework_root = Path(args.framework_root).resolve() if args.framework_root else connector_root / "modules/ModSecurity-test-Framework"
    default_paths = verified_runtime_paths(os.environ)
    build_root = Path(args.build_root or default_paths["BUILD_ROOT"]).resolve()
    payload = build_payload(connector_root, framework_root, build_root)
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        sys.stdout.write(render_text(payload))
    if payload["status"] == "BLOCKED":
        return 77
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
