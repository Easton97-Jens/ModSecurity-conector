#!/usr/bin/env python3
from __future__ import annotations

import argparse
import getpass
import hashlib
import json
import os
import platform
import shlex
import shutil
import socket
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from generated_report_utils import (
    FILENAME_TO_KEY,
    GENERATED_REPORTS,
    GENERATED_ROOT,
    build_metadata,
    generated_json_text,
    generated_markdown_text,
    report_path,
)

FRAMEWORK_ENVIRONMENT_VARS = (
    "GO_FTW_BIN",
    "GO_FTW_SOURCE_URL",
    "GO_FTW_PROMPT_EXPECTED_LATEST",
    "GO_FTW_GIT_REF",
    "ALBEDO_BIN",
    "ALBEDO_SOURCE_URL",
    "ALBEDO_PROMPT_EXPECTED_LATEST",
    "ALBEDO_GIT_REF",
    "APACHECTL_BIN",
    "APACHE_BIN",
    "HTTPD_BIN",
    "HTTPD_VERSION",
    "HTTPD_SOURCE_URL",
    "APXS",
    "APXS_BIN",
    "NGINX_BIN",
    "NGINX_SOURCE_REPO_URL",
    "NGINX_GITHUB_REPO",
    "NGINX_RELEASE_TAG",
    "NGINX_SOURCE_GIT_REF",
    "CI_APACHE_BIN_CANDIDATES",
    "CI_APXS_BIN_CANDIDATES",
    "CI_NGINX_BIN_CANDIDATES",
    "HAPROXY_BIN",
    "HAPROXY_VERSION",
    "HAPROXY_SOURCE_URL",
    "HAPROXY_RUNTIME_DIR",
    "HAPROXY_RUNTIME_BUILD_DIR",
    "EXPAT_SOURCE_URL",
    "EXPAT_GIT_REF",
    "EXPAT_GIT_URL",
    "EXPAT_PROMPT_EXPECTED_LATEST",
    "CC",
    "CLANG",
    "MAKE",
    "PYTHON",
)

INSECURE_REPO_URL_PATTERNS = (
    "http://github.com",
    "git@github.com:",
    "ssh://git@github.com",
    "git://github.com",
)


@dataclass(frozen=True)
class ToolSpec:
    tool: str
    version_args: tuple[str, ...]
    env_vars: tuple[str, ...] = ()
    path_fallbacks: tuple[str, ...] = ()
    sys_executable_fallback: bool = False


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run(cmd: list[str], cwd: Path, timeout: int = 300) -> dict[str, Any]:
    started_at = utc_now()
    started = time.monotonic()
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
        )
        output = proc.stdout or ""
        rc = proc.returncode
        status = "PASS" if rc == 0 else "FAIL"
    except FileNotFoundError as exc:
        output = str(exc)
        rc = 127
        status = "missing"
    except subprocess.TimeoutExpired as exc:
        output = (exc.stdout or "") + "\nTIMEOUT"
        rc = 124
        status = "timeout"
    finished_at = utc_now()
    return {
        "command": " ".join(cmd),
        "started_at": started_at,
        "finished_at": finished_at,
        "duration_seconds": round(time.monotonic() - started, 3),
        "return_code": rc,
        "status": status,
        "output_excerpt": output.strip()[:4000],
        "output_sha256": hashlib.sha256(output.encode("utf-8", errors="replace")).hexdigest(),
    }


def read_os_release() -> dict[str, str]:
    path = Path("/etc/os-release")
    data: dict[str, str] = {}
    if not path.is_file():
        return data
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key] = value.strip().strip('"')
    return data


def load_framework_environment(connector_root: Path, framework_root: Path) -> dict[str, Any]:
    common_sh = framework_root / "ci/common.sh"
    base_env = os.environ.copy()
    base_env["CONNECTOR_ROOT"] = str(connector_root)
    base_env["FRAMEWORK_ROOT"] = str(framework_root)
    if not common_sh.is_file():
        return {
            "framework_root": str(framework_root),
            "common_sh_path": str(common_sh),
            "common_sh_status": "missing",
            "load_return_code": 127,
            "load_output_excerpt": "common.sh not found",
            "env": base_env,
            "variables": {name: base_env.get(name) or None for name in FRAMEWORK_ENVIRONMENT_VARS},
        }
    try:
        proc = subprocess.run(
            ["bash", "-lc", 'set -a; . "$FRAMEWORK_ROOT/ci/common.sh"; env -0'],
            cwd=str(connector_root),
            env=base_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=False,
            timeout=60,
        )
    except FileNotFoundError as exc:
        return {
            "framework_root": str(framework_root),
            "common_sh_path": str(common_sh),
            "common_sh_status": "failed",
            "load_return_code": 127,
            "load_output_excerpt": str(exc),
            "env": base_env,
            "variables": {name: base_env.get(name) or None for name in FRAMEWORK_ENVIRONMENT_VARS},
        }
    except subprocess.TimeoutExpired as exc:
        output = (exc.stdout or b"") + b"\nTIMEOUT"
        return {
            "framework_root": str(framework_root),
            "common_sh_path": str(common_sh),
            "common_sh_status": "failed",
            "load_return_code": 124,
            "load_output_excerpt": output.decode("utf-8", errors="replace").strip()[:4000],
            "env": base_env,
            "variables": {name: base_env.get(name) or None for name in FRAMEWORK_ENVIRONMENT_VARS},
        }
    stderr = proc.stderr.decode("utf-8", errors="replace").strip()
    if proc.returncode != 0:
        return {
            "framework_root": str(framework_root),
            "common_sh_path": str(common_sh),
            "common_sh_status": "failed",
            "load_return_code": proc.returncode,
            "load_output_excerpt": stderr[:4000] or f"common.sh load failed with return code {proc.returncode}",
            "env": base_env,
            "variables": {name: base_env.get(name) or None for name in FRAMEWORK_ENVIRONMENT_VARS},
        }
    loaded_env: dict[str, str] = {}
    for chunk in proc.stdout.split(b"\0"):
        if not chunk or b"=" not in chunk:
            continue
        key, value = chunk.split(b"=", 1)
        loaded_env[key.decode("utf-8", errors="replace")] = value.decode("utf-8", errors="replace")
    return {
        "framework_root": str(framework_root),
        "common_sh_path": str(common_sh),
        "common_sh_status": "loaded",
        "load_return_code": proc.returncode,
        "load_output_excerpt": stderr[:4000],
        "env": loaded_env,
        "variables": {name: loaded_env.get(name) or None for name in FRAMEWORK_ENVIRONMENT_VARS},
    }


def split_command_value(value: str) -> list[str]:
    try:
        parts = shlex.split(value)
    except ValueError:
        return [value]
    return parts or [value]


def command_exists(command: str, cwd: Path, env: dict[str, str]) -> tuple[str | None, str, int]:
    expanded = os.path.expanduser(os.path.expandvars(command))
    if "/" in expanded:
        path = Path(expanded)
        if not path.is_absolute():
            path = cwd / path
        if not path.exists():
            return str(path), "file not found", 127
        if not path.is_file() or not os.access(path, os.X_OK):
            return str(path), "not executable", 126
        return str(path), "", 0
    resolved = shutil.which(expanded, path=env.get("PATH"))
    if resolved is None:
        return expanded, "command not found", 127
    return resolved, "", 0


def common_env(framework_env: dict[str, Any]) -> dict[str, str]:
    return framework_env.get("env", {})


def env_var_candidate(
    var_name: str,
    initial_env: dict[str, str],
    framework_env: dict[str, Any],
) -> tuple[str, str] | None:
    initial_value = initial_env.get(var_name)
    if initial_value:
        return initial_value, f"{var_name} from process/make environment"
    loaded_value = framework_env.get("env", {}).get(var_name)
    if loaded_value:
        return loaded_value, f"{var_name} from framework common.sh"
    return None


def env_var_value(
    var_name: str,
    initial_env: dict[str, str],
    framework_env: dict[str, Any],
) -> tuple[str, str] | None:
    return env_var_candidate(var_name, initial_env, framework_env)


def framework_candidate_values(
    var_name: str,
    initial_env: dict[str, str],
    framework_env: dict[str, Any],
) -> tuple[list[str], str]:
    initial_value = initial_env.get(var_name)
    if initial_value:
        return split_command_value(initial_value), f"{var_name} from process/make environment"
    loaded_value = common_env(framework_env).get(var_name, "")
    if loaded_value:
        return split_command_value(loaded_value), f"{var_name} from framework common.sh"
    return [], f"{var_name} from framework common.sh"


def run_common_helper(
    function_name: str,
    args: list[str],
    cwd: Path,
    framework_env: dict[str, Any],
    timeout: int = 60,
) -> dict[str, Any]:
    if framework_env.get("common_sh_status") != "loaded":
        return {
            "return_code": 127,
            "status": "missing",
            "output_excerpt": f"common.sh not loaded; cannot run {function_name}",
            "output_sha256": hashlib.sha256(b"").hexdigest(),
        }
    env = dict(common_env(framework_env))
    script = f'. "$FRAMEWORK_ROOT/ci/common.sh"; {function_name} "$@"'
    try:
        proc = subprocess.run(
            ["bash", "-lc", script, "bash", *args],
            cwd=str(cwd),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError as exc:
        output = str(exc)
        return {
            "return_code": 127,
            "status": "missing",
            "output_excerpt": output,
            "output_sha256": hashlib.sha256(output.encode("utf-8")).hexdigest(),
        }
    except subprocess.TimeoutExpired as exc:
        output = (exc.stdout or "") + "\nTIMEOUT"
        return {
            "return_code": 124,
            "status": "timeout",
            "output_excerpt": output.strip()[:4000],
            "output_sha256": hashlib.sha256(output.encode("utf-8")).hexdigest(),
        }
    output = proc.stdout or ""
    return {
        "return_code": proc.returncode,
        "status": "PASS" if proc.returncode == 0 else "FAIL",
        "output_excerpt": output.strip()[:4000],
        "output_sha256": hashlib.sha256(output.encode("utf-8", errors="replace")).hexdigest(),
    }


def unique_candidates(candidates: list[str]) -> list[str]:
    unique: list[str] = []
    for candidate in candidates:
        if candidate not in unique:
            unique.append(candidate)
    return unique


def make_tool_record(
    *,
    tool: str,
    status: str,
    resolved_command: str | None,
    attempted_command: str | None,
    source: str,
    candidates: list[str] | None = None,
    version_output: str,
    return_code: int,
    notes: str = "",
    output_sha256: str | None = None,
) -> dict[str, Any]:
    version = version_output.splitlines()[0] if version_output else f"return code {return_code}"
    clean_candidates = unique_candidates(candidates or [])
    return {
        "tool": tool,
        "status": status,
        "resolved_command": resolved_command,
        "attempted_command": attempted_command,
        "source": source,
        "candidates": clean_candidates,
        "version_output": version_output,
        "version": version,
        "return_code": return_code,
        "notes": notes,
        "output_sha256": output_sha256 or hashlib.sha256(version_output.encode("utf-8")).hexdigest(),
    }


def run_resolved_tool(
    *,
    tool: str,
    resolved_command: str,
    attempted_command: str,
    source: str,
    version_args: tuple[str, ...],
    candidates: list[str],
    cwd: Path,
    notes: str = "",
) -> dict[str, Any]:
    result = run([resolved_command, *version_args], cwd, timeout=60)
    version_output = result["output_excerpt"] or f"return code {result['return_code']}"
    return make_tool_record(
        tool=tool,
        status="present" if result["return_code"] == 0 else "error",
        resolved_command=resolved_command,
        attempted_command=attempted_command,
        source=source,
        candidates=candidates,
        version_output=version_output,
        return_code=result["return_code"],
        notes=notes,
        output_sha256=result["output_sha256"],
    )


def resolve_candidate_list(
    *,
    tool: str,
    candidates: list[str],
    source: str,
    version_args: tuple[str, ...],
    cwd: Path,
    env: dict[str, str],
    notes: str,
) -> dict[str, Any]:
    attempted = candidates[-1] if candidates else None
    for candidate in candidates:
        resolved, error, rc = command_exists(candidate, cwd, env)
        attempted = candidate
        if rc == 0 and resolved is not None:
            return run_resolved_tool(
                tool=tool,
                resolved_command=resolved,
                attempted_command=candidate,
                source=source,
                version_args=version_args,
                candidates=candidates,
                cwd=cwd,
                notes=notes,
            )
    joined = " ".join(candidates)
    output = f"no candidate found: {joined}" if joined else "no candidate configured"
    return make_tool_record(
        tool=tool,
        status="missing",
        resolved_command=None,
        attempted_command=attempted,
        source=source,
        candidates=candidates,
        version_output=output,
        return_code=127,
        notes=notes,
    )


def resolve_tool(spec: ToolSpec, cwd: Path, framework_env: dict[str, Any], initial_env: dict[str, str]) -> dict[str, Any]:
    effective_env = dict(framework_env.get("env") or initial_env)
    candidates: list[tuple[str, str]] = []
    for var_name in spec.env_vars:
        candidate = env_var_candidate(var_name, initial_env, framework_env)
        if candidate is not None:
            candidates.append(candidate)
    if spec.sys_executable_fallback:
        candidates.append((sys.executable, "current sys.executable"))
    candidates.extend((name, "PATH fallback") for name in spec.path_fallbacks)

    attempted_command = spec.path_fallbacks[0] if spec.path_fallbacks else spec.tool
    source = "PATH fallback"
    resolved_command: str | None = None
    prefix_args: list[str] = []
    resolution_error = "command not found"
    resolution_rc = 127
    for value, candidate_source in candidates:
        parts = split_command_value(value)
        attempted_command = parts[0]
        source = candidate_source
        resolved, error, rc = command_exists(parts[0], cwd, effective_env)
        prefix_args = parts[1:]
        if rc == 0:
            resolved_command = resolved
            resolution_error = ""
            resolution_rc = 0
            break
        if candidate_source != "PATH fallback":
            resolved_command = resolved
            resolution_error = error
            resolution_rc = rc
            break
        resolved_command = None
        resolution_error = error
        resolution_rc = rc

    if resolution_rc != 0:
        return {
            "tool": spec.tool,
            "status": "missing",
            "resolved_command": resolved_command if source != "PATH fallback" else None,
            "attempted_command": attempted_command,
            "source": source,
            "candidates": unique_candidates([item for item, _source in candidates]),
            "version_output": resolution_error,
            "version": resolution_error,
            "return_code": resolution_rc,
            "notes": "",
            "output_sha256": hashlib.sha256(resolution_error.encode("utf-8")).hexdigest(),
        }

    command = [resolved_command or attempted_command, *prefix_args, *spec.version_args]
    result = run(command, cwd, timeout=60)
    version_output = result["output_excerpt"] or f"return code {result['return_code']}"
    return {
        "tool": spec.tool,
        "status": "present" if result["return_code"] == 0 else "error",
        "resolved_command": resolved_command,
        "attempted_command": attempted_command,
        "source": source,
        "candidates": unique_candidates([item for item, _source in candidates]),
        "version_output": version_output,
        "version": version_output.splitlines()[0] if version_output else f"return code {result['return_code']}",
        "return_code": result["return_code"],
        "notes": "",
        "output_sha256": result["output_sha256"],
    }


def resolve_python_tool(cwd: Path, framework_env: dict[str, Any], initial_env: dict[str, str]) -> dict[str, Any]:
    candidates: list[tuple[str, str]] = []
    python_env = initial_env.get("PYTHON")
    if python_env:
        candidates.append((python_env, "PYTHON from process/make environment"))
    else:
        helper = run_common_helper("ci_python", [], cwd, framework_env)
        helper_output = helper.get("output_excerpt", "").splitlines()[0] if helper.get("output_excerpt") else ""
        if helper.get("return_code") == 0 and helper_output:
            candidates.append((helper_output, "ci_python from framework common.sh"))
    candidates.extend((item, "PATH fallback") for item in ("python3", "python"))

    effective_env = dict(common_env(framework_env) or initial_env)
    for value, source in candidates:
        parts = split_command_value(value)
        resolved, error, rc = command_exists(parts[0], cwd, effective_env)
        if rc == 0 and resolved is not None:
            return run_resolved_tool(
                tool="python",
                resolved_command=resolved,
                attempted_command=parts[0],
                source=source,
                version_args=("--version",),
                candidates=[candidate for candidate, _source in candidates],
                cwd=cwd,
                notes="resolved by Make PYTHON, ci_python, then python3/python fallback",
            )
        if source != "PATH fallback":
            return make_tool_record(
                tool="python",
                status="missing",
                resolved_command=resolved,
                attempted_command=parts[0],
                source=source,
                candidates=[candidate for candidate, _source in candidates],
                version_output=error,
                return_code=rc,
                notes="configured Python command could not be executed",
            )
    return make_tool_record(
        tool="python",
        status="missing",
        resolved_command=None,
        attempted_command="python",
        source="PATH fallback",
        candidates=[candidate for candidate, _source in candidates],
        version_output="no candidate found: python3 python",
        return_code=127,
        notes="python3/python fallback commands are unavailable",
    )


def resolve_sh_tool(cwd: Path) -> dict[str, Any]:
    sh_path = Path("/bin/sh")
    if not sh_path.exists():
        return make_tool_record(
            tool="sh",
            status="missing",
            resolved_command=None,
            attempted_command="/bin/sh",
            source="/bin/sh executable check",
            candidates=["/bin/sh"],
            version_output="file not found",
            return_code=127,
            notes="checked /bin/sh without using unsupported --version",
        )
    if not os.access(sh_path, os.X_OK):
        return make_tool_record(
            tool="sh",
            status="missing",
            resolved_command=str(sh_path),
            attempted_command="/bin/sh",
            source="/bin/sh executable check",
            candidates=["/bin/sh"],
            version_output="not executable",
            return_code=126,
            notes="checked /bin/sh without using unsupported --version",
        )
    result = run([str(sh_path), "-c", "printf '%s' 'POSIX shell available'"], cwd, timeout=60)
    resolved = str(sh_path.resolve(strict=False))
    version_output = f"{result['output_excerpt']} ({resolved})" if result["output_excerpt"] else resolved
    return make_tool_record(
        tool="sh",
        status="present" if result["return_code"] == 0 else "error",
        resolved_command=resolved,
        attempted_command="/bin/sh",
        source="/bin/sh executable check",
        candidates=["/bin/sh"],
        version_output=version_output,
        return_code=result["return_code"],
        notes="checked shell availability with /bin/sh -c instead of sh --version",
        output_sha256=result["output_sha256"],
    )


def resolve_haproxy_tool(cwd: Path, framework_env: dict[str, Any], initial_env: dict[str, str]) -> dict[str, Any]:
    effective_env = dict(common_env(framework_env) or initial_env)
    candidate = env_var_value("HAPROXY_BIN", initial_env, framework_env)
    if candidate is not None:
        value, source = candidate
        resolved, error, rc = command_exists(value, cwd, effective_env)
        metadata = common_env(framework_env)
        notes = (
            "runtime path configured by common.sh but binary has not been built/prepared locally; "
            f"HAPROXY_VERSION={metadata.get('HAPROXY_VERSION', 'unset')}; "
            f"HAPROXY_SOURCE_URL={metadata.get('HAPROXY_SOURCE_URL', 'unset')}; "
            f"HAPROXY_RUNTIME_DIR={metadata.get('HAPROXY_RUNTIME_DIR', 'unset')}; "
            f"HAPROXY_RUNTIME_BUILD_DIR={metadata.get('HAPROXY_RUNTIME_BUILD_DIR', 'unset')}"
        )
        if rc != 0:
            return make_tool_record(
                tool="haproxy",
                status="configured_missing",
                resolved_command=resolved,
                attempted_command=value,
                source=source,
                candidates=[],
                version_output=error,
                return_code=rc,
                notes=notes,
            )
        return run_resolved_tool(
            tool="haproxy",
            resolved_command=resolved or value,
            attempted_command=value,
            source=source,
            version_args=("-vv",),
            candidates=[],
            cwd=cwd,
            notes="runtime path configured and executable",
        )
    return resolve_candidate_list(
        tool="haproxy",
        candidates=["haproxy"],
        source="PATH fallback",
        version_args=("-vv",),
        cwd=cwd,
        env=effective_env,
        notes="HAPROXY_BIN is unset; checked PATH fallback",
    )


def resolve_nginx_tool(cwd: Path, framework_env: dict[str, Any], initial_env: dict[str, str]) -> dict[str, Any]:
    effective_env = dict(common_env(framework_env) or initial_env)
    candidate = env_var_value("NGINX_BIN", initial_env, framework_env)
    if candidate is not None:
        value, source = candidate
        resolved, error, rc = command_exists(value, cwd, effective_env)
        if rc == 0 and resolved is not None:
            return run_resolved_tool(
                tool="nginx",
                resolved_command=resolved,
                attempted_command=value,
                source=source,
                version_args=("-v",),
                candidates=[],
                cwd=cwd,
                notes="NGINX_BIN is set and executable",
            )
        return make_tool_record(
            tool="nginx",
            status="missing",
            resolved_command=resolved,
            attempted_command=value,
            source=source,
            candidates=[],
            version_output=error,
            return_code=rc,
            notes="NGINX_BIN is set but does not resolve to an executable",
        )
    candidates, source = framework_candidate_values("CI_NGINX_BIN_CANDIDATES", initial_env, framework_env)
    return resolve_candidate_list(
        tool="nginx",
        candidates=candidates,
        source=source,
        version_args=("-v",),
        cwd=cwd,
        env=effective_env,
        notes="NGINX_BIN is unset; checked framework candidates",
    )


def resolve_apxs_tool(cwd: Path, framework_env: dict[str, Any], initial_env: dict[str, str]) -> dict[str, Any]:
    effective_env = dict(common_env(framework_env) or initial_env)
    for var_name in ("APXS_BIN", "APXS"):
        candidate = env_var_value(var_name, initial_env, framework_env)
        if candidate is None:
            continue
        value, source = candidate
        if var_name == "APXS" and source.endswith("framework common.sh"):
            source = "APXS from environment"
        resolved, error, rc = command_exists(value, cwd, effective_env)
        if rc == 0 and resolved is not None:
            return run_resolved_tool(
                tool="apxs",
                resolved_command=resolved,
                attempted_command=value,
                source=source,
                version_args=("-v",),
                candidates=[],
                cwd=cwd,
                notes=f"{var_name} is set and executable",
            )
        return make_tool_record(
            tool="apxs",
            status="missing",
            resolved_command=resolved,
            attempted_command=value,
            source=source,
            candidates=[],
            version_output=error,
            return_code=rc,
            notes=f"{var_name} is set but does not resolve to an executable",
        )
    candidates, source = framework_candidate_values("CI_APXS_BIN_CANDIDATES", initial_env, framework_env)
    return resolve_candidate_list(
        tool="apxs",
        candidates=candidates,
        source=source,
        version_args=("-v",),
        cwd=cwd,
        env=effective_env,
        notes="APXS_BIN is unset; checked framework candidates",
    )


def resolve_apache_tool(
    cwd: Path,
    framework_env: dict[str, Any],
    initial_env: dict[str, str],
    apxs_record: dict[str, Any],
) -> dict[str, Any]:
    effective_env = dict(common_env(framework_env) or initial_env)
    for var_name in ("APACHECTL_BIN", "APACHE_BIN", "HTTPD_BIN"):
        candidate = env_var_value(var_name, initial_env, framework_env)
        if candidate is None:
            continue
        value, source = candidate
        resolved, error, rc = command_exists(value, cwd, effective_env)
        if rc == 0 and resolved is not None:
            return run_resolved_tool(
                tool="apache/httpd",
                resolved_command=resolved,
                attempted_command=value,
                source=source,
                version_args=("-v",),
                candidates=[],
                cwd=cwd,
                notes=f"{var_name} is set and executable",
            )
        return make_tool_record(
            tool="apache/httpd",
            status="missing",
            resolved_command=resolved,
            attempted_command=value,
            source=source,
            candidates=[],
            version_output=error,
            return_code=rc,
            notes=f"{var_name} is set but does not resolve to an executable",
        )

    apxs_path = apxs_record.get("resolved_command")
    if apxs_record.get("status") == "present" and apxs_path:
        helper = run_common_helper("ci_resolve_apache_from_apxs", [apxs_path], cwd, framework_env)
        helper_output = helper.get("output_excerpt", "").splitlines()[0] if helper.get("output_excerpt") else ""
        if helper.get("return_code") == 0 and helper_output:
            resolved, error, rc = command_exists(helper_output, cwd, effective_env)
            if rc == 0 and resolved is not None:
                return run_resolved_tool(
                    tool="apache/httpd",
                    resolved_command=resolved,
                    attempted_command=helper_output,
                    source="ci_resolve_apache_from_apxs from framework common.sh",
                    version_args=("-v",),
                    candidates=[apxs_path],
                    cwd=cwd,
                    notes="resolved Apache binary through APXS helper",
                )
            return make_tool_record(
                tool="apache/httpd",
                status="missing",
                resolved_command=resolved,
                attempted_command=helper_output,
                source="ci_resolve_apache_from_apxs from framework common.sh",
                candidates=[apxs_path],
                version_output=error,
                return_code=rc,
                notes="APXS helper returned a path that is not executable",
            )

    candidates, source = framework_candidate_values("CI_APACHE_BIN_CANDIDATES", initial_env, framework_env)
    return resolve_candidate_list(
        tool="apache/httpd",
        candidates=candidates,
        source=source,
        version_args=("-v",),
        cwd=cwd,
        env=effective_env,
        notes="APACHECTL_BIN/APACHE_BIN are unset; checked APXS helper and framework candidates",
    )


def resolve_apachectl_tool(cwd: Path, framework_env: dict[str, Any], initial_env: dict[str, str]) -> dict[str, Any]:
    effective_env = dict(common_env(framework_env) or initial_env)
    candidate = env_var_value("APACHECTL_BIN", initial_env, framework_env)
    if candidate is not None:
        value, source = candidate
        resolved, error, rc = command_exists(value, cwd, effective_env)
        if rc == 0 and resolved is not None:
            return run_resolved_tool(
                tool="apachectl",
                resolved_command=resolved,
                attempted_command=value,
                source=source,
                version_args=("-v",),
                candidates=[],
                cwd=cwd,
                notes="APACHECTL_BIN is set and executable",
            )
        return make_tool_record(
            tool="apachectl",
            status="missing",
            resolved_command=resolved,
            attempted_command=value,
            source=source,
            candidates=[],
            version_output=error,
            return_code=rc,
            notes="APACHECTL_BIN is set but does not resolve to an executable",
        )
    candidates, source = framework_candidate_values("CI_APACHE_BIN_CANDIDATES", initial_env, framework_env)
    apachectl_candidates = [candidate for candidate in candidates if "apachectl" in Path(candidate).name]
    return resolve_candidate_list(
        tool="apachectl",
        candidates=apachectl_candidates or ["apachectl"],
        source=source if apachectl_candidates else "PATH fallback",
        version_args=("-v",),
        cwd=cwd,
        env=effective_env,
        notes="APACHECTL_BIN is unset; checked apachectl candidate",
    )


def add_optional_tool_note(record: dict[str, Any], note: str) -> dict[str, Any]:
    if record.get("status") == "missing":
        record = dict(record)
        record["notes"] = note
    return record


def resolve_tools(cwd: Path, framework_env: dict[str, Any], initial_env: dict[str, str]) -> list[dict[str, Any]]:
    generic_specs = [
        ToolSpec("git", ("--version",), path_fallbacks=("git",)),
        ToolSpec("python3", ("--version",), path_fallbacks=("python3",)),
        ToolSpec("make", ("--version",), env_vars=("MAKE",), path_fallbacks=("make",)),
        ToolSpec("bash", ("--version",), path_fallbacks=("bash",)),
        ToolSpec("gcc", ("--version",), env_vars=("CC",), path_fallbacks=("gcc",)),
        ToolSpec("clang", ("--version",), env_vars=("CLANG",), path_fallbacks=("clang",)),
        ToolSpec("go", ("version",), path_fallbacks=("go",)),
        ToolSpec("go-ftw", ("version",), env_vars=("GO_FTW_BIN",), path_fallbacks=("go-ftw",)),
        ToolSpec("albedo", ("--version",), env_vars=("ALBEDO_BIN",), path_fallbacks=("albedo",)),
        ToolSpec("actionlint", ("--version",), path_fallbacks=("actionlint",)),
        ToolSpec("jq", ("--version",), path_fallbacks=("jq",)),
        ToolSpec("curl", ("--version",), path_fallbacks=("curl",)),
        ToolSpec("docker", ("--version",), path_fallbacks=("docker",)),
    ]
    generic_records = {spec.tool: resolve_tool(spec, cwd, framework_env, initial_env) for spec in generic_specs}
    generic_records["go-ftw"] = add_optional_tool_note(
        generic_records["go-ftw"],
        "optional MRTS/FTW tool not installed or not in PATH",
    )
    generic_records["albedo"] = add_optional_tool_note(
        generic_records["albedo"],
        "optional native MRTS tool not installed or not in PATH",
    )
    apxs_record = resolve_apxs_tool(cwd, framework_env, initial_env)
    return [
        generic_records["git"],
        generic_records["python3"],
        resolve_python_tool(cwd, framework_env, initial_env),
        generic_records["make"],
        generic_records["bash"],
        resolve_sh_tool(cwd),
        generic_records["gcc"],
        generic_records["clang"],
        generic_records["go"],
        generic_records["go-ftw"],
        generic_records["albedo"],
        generic_records["actionlint"],
        generic_records["jq"],
        generic_records["curl"],
        generic_records["docker"],
        resolve_apachectl_tool(cwd, framework_env, initial_env),
        resolve_apache_tool(cwd, framework_env, initial_env, apxs_record),
        resolve_nginx_tool(cwd, framework_env, initial_env),
        resolve_haproxy_tool(cwd, framework_env, initial_env),
        apxs_record,
    ]


def git_evidence(connector_root: Path, framework_root: Path) -> dict[str, Any]:
    commands = {
        "git_status_short": ["git", "status", "--short"],
        "git_head": ["git", "rev-parse", "HEAD"],
        "git_branch": ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        "git_submodule_status": ["git", "submodule", "status", "--recursive"],
        "git_diff_stat": ["git", "diff", "--stat"],
    }
    evidence = {name: run(command, connector_root, timeout=120) for name, command in commands.items()}
    framework_commands = {
        "framework_status_short": ["git", "-C", str(framework_root), "status", "--short"],
        "framework_head": ["git", "-C", str(framework_root), "rev-parse", "HEAD"],
        "framework_diff_stat": ["git", "-C", str(framework_root), "diff", "--stat"],
    }
    evidence.update({name: run(command, connector_root, timeout=120) for name, command in framework_commands.items()})
    return evidence


def layout_evidence(connector_root: Path) -> dict[str, Any]:
    generated_root = connector_root / GENERATED_ROOT
    generated_files = sorted(generated_root.rglob("*.generated.*"))
    flat_files = sorted(generated_root.glob("*.generated.*"))
    categories = sorted({path.parent.name for path in generated_files if path.parent != generated_root})
    expected = {
        str((connector_root / GENERATED_ROOT / report.category / report.filename(ext)).resolve(strict=False))
        for report in GENERATED_REPORTS.values()
        for ext in report.formats
        if report.commit_policy not in {"local-only", "do-not-commit"} and report.data_kind != "system-proof"
    }
    existing = {str(path.resolve(strict=False)) for path in generated_files}
    orphan = [
        str(path.relative_to(connector_root))
        for path in generated_files
        if path.name not in FILENAME_TO_KEY or str(path.resolve(strict=False)) not in {
            str((connector_root / GENERATED_ROOT / GENERATED_REPORTS[FILENAME_TO_KEY[path.name]].category / path.name).resolve(strict=False))
        }
    ]
    manifest = {}
    manifest_path = report_path(connector_root, "report_refresh_manifest", "json")
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:
            manifest = {}
    reports = manifest.get("reports", []) if isinstance(manifest.get("reports"), list) else []
    return {
        "generated_report_files": len(generated_files),
        "flat_files_in_generated_root": len(flat_files),
        "categories": categories,
        "category_count": len(categories),
        "reports_per_category": {category: sum(1 for path in generated_files if path.parent.name == category) for category in categories},
        "missing_registry_outputs": sorted(expected - existing),
        "orphan_generated_reports": orphan,
        "skipped_reports": [report for report in reports if str(report.get("status", "")).startswith("skipped")],
        "failed_reports": [report for report in reports if report.get("status") == "failed"],
    }


def https_repo_url_policy(connector_root: Path, framework_root: Path) -> dict[str, Any]:
    text_suffixes = {"", ".md", ".py", ".sh", ".json", ".yml", ".yaml", ".mk"}
    scan_paths: list[Path] = [
        connector_root / "Makefile",
        connector_root / "README.md",
    ]
    scan_paths.extend(sorted(connector_root.glob("COMPILE_*.md")))
    for base in (
        connector_root / "ci",
        framework_root / "ci",
        connector_root / "docs",
        connector_root / "reports/testing",
    ):
        if base.is_dir():
            scan_paths.extend(path for path in sorted(base.rglob("*")) if path.is_file())
    skip_names = {"check-generated-report-layout.py", "generate-system-environment-proof.py"}
    findings = []
    for path in scan_paths:
        if "__pycache__" in path.parts or path.suffix not in text_suffixes:
            continue
        try:
            if (connector_root / GENERATED_ROOT).resolve(strict=False) in path.resolve(strict=False).parents:
                continue
        except OSError:
            continue
        if path.name in skip_names:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            for pattern in INSECURE_REPO_URL_PATTERNS:
                if pattern in line:
                    findings.append(
                        {
                            "path": str(path.relative_to(connector_root)) if path.is_relative_to(connector_root) else str(path),
                            "line": line_number,
                            "pattern": pattern,
                        }
                    )
    status = "PASS" if not findings else "FAIL"
    notes = (
        "no active http, ssh, git protocol repo URLs found"
        if status == "PASS"
        else f"{len(findings)} insecure repo URL pattern(s) found"
    )
    return {
        "status": status,
        "blocked_protocols": ["http", "ssh", "git"],
        "allowed_protocol": "https",
        "notes": "Only HTTPS repository URLs are accepted.",
        "active_scan_notes": notes,
        "github_policy": "only https://github.com/owner/repo accepted",
        "findings": findings,
    }


def pip_freeze_summary(cwd: Path) -> dict[str, Any]:
    result = run([sys.executable, "-m", "pip", "freeze"], cwd, timeout=120)
    lines = [line for line in result["output_excerpt"].splitlines() if line.strip()]
    full_output_hash = result["output_sha256"]
    return {
        "status": result["status"],
        "return_code": result["return_code"],
        "package_count_from_excerpt": len(lines),
        "output_sha256": full_output_hash,
    }


def md_cell(value: Any) -> str:
    text = "unset" if value is None else str(value)
    return text.replace("|", "/").replace("\n", " ")


def md_code(value: Any) -> str:
    return "`" + md_cell(value).replace("`", "\\`") + "`"


def md_optional_code(value: Any) -> str:
    if value is None:
        return "``"
    return md_code(value)


def tool_by_name(tools: list[dict[str, Any]], name: str) -> dict[str, Any]:
    return next((tool for tool in tools if tool.get("tool") == name), {})


def runtime_component_readiness(tools: list[dict[str, Any]], framework_env: dict[str, Any]) -> list[dict[str, str]]:
    variables = framework_env.get("variables", {})
    haproxy = tool_by_name(tools, "haproxy")
    nginx = tool_by_name(tools, "nginx")
    apxs = tool_by_name(tools, "apxs")
    apache = tool_by_name(tools, "apache/httpd")
    go_ftw = tool_by_name(tools, "go-ftw")
    albedo = tool_by_name(tools, "albedo")
    apache_status = "present" if apxs.get("status") == "present" or apache.get("status") == "present" else "missing"
    return [
        {
            "component": "HAProxy",
            "status": str(haproxy.get("status", "missing")),
            "expected_path": str(variables.get("HAPROXY_BIN") or "$HAPROXY_BIN"),
            "source_url": str(variables.get("HAPROXY_SOURCE_URL") or "$HAPROXY_SOURCE_URL"),
            "version_ref": str(variables.get("HAPROXY_VERSION") or "$HAPROXY_VERSION"),
            "how_to_prepare": "make prepare-runtime-components or make runtime-matrix-haproxy",
        },
        {
            "component": "NGINX",
            "status": "present" if nginx.get("status") == "present" else "missing",
            "expected_path": str(variables.get("NGINX_BIN") or variables.get("CI_NGINX_BIN_CANDIDATES") or "$NGINX_BIN or CI_NGINX_BIN_CANDIDATES"),
            "source_url": str(variables.get("NGINX_SOURCE_REPO_URL") or variables.get("NGINX_GITHUB_REPO") or "$NGINX_SOURCE_REPO_URL"),
            "version_ref": str(variables.get("NGINX_RELEASE_TAG") or variables.get("NGINX_SOURCE_GIT_REF") or "$NGINX_RELEASE_TAG"),
            "how_to_prepare": "install nginx or prepare runtime components",
        },
        {
            "component": "Apache/APXS",
            "status": apache_status,
            "expected_path": str(variables.get("APXS_BIN") or variables.get("CI_APXS_BIN_CANDIDATES") or "$APXS_BIN or CI_APXS_BIN_CANDIDATES"),
            "source_url": str(variables.get("HTTPD_SOURCE_URL") or "$HTTPD_SOURCE_URL"),
            "version_ref": str(variables.get("HTTPD_VERSION") or "$HTTPD_VERSION"),
            "how_to_prepare": "install apache2-dev/httpd-devel or prepare Apache runtime",
        },
        {
            "component": "go-ftw",
            "status": "present" if go_ftw.get("status") == "present" else "missing_optional",
            "expected_path": str(variables.get("GO_FTW_BIN") or "$GO_FTW_BIN"),
            "source_url": str(variables.get("GO_FTW_SOURCE_URL") or "$GO_FTW_SOURCE_URL"),
            "version_ref": str(variables.get("GO_FTW_PROMPT_EXPECTED_LATEST") or variables.get("GO_FTW_GIT_REF") or "$GO_FTW_PROMPT_EXPECTED_LATEST"),
            "how_to_prepare": "install go-ftw only if MRTS/FTW checks are required",
        },
        {
            "component": "albedo",
            "status": "present" if albedo.get("status") == "present" else "missing_optional",
            "expected_path": str(variables.get("ALBEDO_BIN") or "$ALBEDO_BIN"),
            "source_url": str(variables.get("ALBEDO_SOURCE_URL") or "$ALBEDO_SOURCE_URL"),
            "version_ref": str(variables.get("ALBEDO_PROMPT_EXPECTED_LATEST") or variables.get("ALBEDO_GIT_REF") or "$ALBEDO_PROMPT_EXPECTED_LATEST"),
            "how_to_prepare": "install albedo only if native MRTS checks require it",
        },
        {
            "component": "expat",
            "status": "informational",
            "expected_path": "n/a",
            "source_url": str(variables.get("EXPAT_SOURCE_URL") or "$EXPAT_SOURCE_URL"),
            "version_ref": str(variables.get("EXPAT_GIT_REF") or "$EXPAT_GIT_REF"),
            "how_to_prepare": "used only if the related runtime build path requires it",
        },
    ]


def render_markdown(payload: dict[str, Any]) -> str:
    os_info = payload["os"]
    python_info = payload["python"]
    layout = payload["layout"]
    framework_env = payload["framework_environment"]
    lines = [
        "# System Environment Proof",
        "",
        "## OS / System",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| OS Name | {os_info.get('name', '-')} |",
        f"| OS Version | {os_info.get('version', '-')} |",
        f"| Kernel | {os_info.get('kernel', '-')} |",
        f"| Architecture | {os_info.get('architecture', '-')} |",
        f"| Hostname | {os_info.get('hostname', '-')} |",
        f"| User | {os_info.get('user', '-')} |",
        f"| Working Directory | `{os_info.get('working_directory', '-')}` |",
        "",
        "## Framework Environment Resolution",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Framework root | {md_code(framework_env.get('framework_root'))} |",
        f"| common.sh path | {md_code(framework_env.get('common_sh_path'))} |",
        f"| common.sh status | {md_code(framework_env.get('common_sh_status'))} |",
        f"| common.sh return code | {md_code(framework_env.get('load_return_code'))} |",
    ]
    for name in FRAMEWORK_ENVIRONMENT_VARS:
        lines.append(f"| {name} | {md_code(framework_env.get('variables', {}).get(name))} |")
    if framework_env.get("load_output_excerpt"):
        lines.append(f"| common.sh output | {md_code(framework_env.get('load_output_excerpt'))} |")
    lines.extend(
        [
            "",
            "## Tool Versions",
            "",
            "| Tool | Status | Resolved Command | Source | Candidates | Version / Output | Notes |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for tool in payload["tools"]:
        displayed_command = tool.get("resolved_command")
        candidates = " ".join(str(item) for item in tool.get("candidates", []))
        version_line = str(tool.get("version_output") or tool.get("version") or "-").splitlines()[0]
        lines.append(
            f"| {tool['tool']} | {tool['status']} | {md_optional_code(displayed_command)} | "
            f"{md_code(tool.get('source', '-'))} | {md_optional_code(candidates or None)} | "
            f"{md_code(version_line)} | {md_optional_code(tool.get('notes') or None)} |"
        )
    lines.extend(
        [
            "",
            "## Runtime Component Readiness",
            "",
            "| Component | Status | Expected Path | Source URL | Version / Ref | How to Prepare |",
            "|---|---|---|---|---|---|",
        ]
    )
    for item in payload["runtime_component_readiness"]:
        lines.append(
            f"| {item['component']} | {item['status']} | {md_code(item['expected_path'])} | "
            f"{md_code(item['source_url'])} | {md_code(item['version_ref'])} | {md_code(item['how_to_prepare'])} |"
        )
    policy = payload["https_repo_url_policy"]
    lines.extend(
        [
            "",
            "## HTTPS Repository URL Policy",
            "",
            "| Check | Status | Notes |",
            "|---|---|---|",
            f"| HTTPS-only repo URLs | {policy.get('status', '-')} | {md_cell(policy.get('active_scan_notes', '-'))} |",
            f"| GitHub repo URL policy | {policy.get('status', '-')} | {md_cell(policy.get('github_policy', '-'))} |",
        ]
    )
    lines.extend(
        [
            "",
            "## Python Environment",
            "",
            "| Field | Value |",
            "|---|---|",
            f"| sys.version | `{python_info.get('sys_version', '-')}` |",
            f"| sys.executable | `{python_info.get('sys_executable', '-')}` |",
            f"| sys.platform | `{python_info.get('sys_platform', '-')}` |",
            f"| platform.platform() | `{python_info.get('platform', '-')}` |",
            f"| PYTHONPATH | `{python_info.get('pythonpath', '-')}` |",
            f"| PYTHONDONTWRITEBYTECODE | `{python_info.get('pythondontwritebytecode', '-')}` |",
            f"| .venv exists | `{python_info.get('venv_exists', '-')}` |",
            f"| pip --version | `{python_info.get('pip_version', '-')}` |",
            f"| pip freeze packages in excerpt | `{python_info.get('pip_freeze', {}).get('package_count_from_excerpt', '-')}` |",
            f"| pip freeze output hash | `{python_info.get('pip_freeze', {}).get('output_sha256', '-')}` |",
            "",
            "## Executed Checks",
            "",
            "| Command | Status | Return Code | Duration | Notes |",
            "|---|---|---:|---:|---|",
        ]
    )
    for check in payload["checks"]:
        note = check["output_excerpt"].splitlines()[-1] if check["output_excerpt"] else "-"
        lines.append(f"| `{check['command']}` | {check['status']} | {check['return_code']} | {check['duration_seconds']} | {note.replace('|', '/')} |")
    lines.extend(
        [
            "",
            "## Report Layout Evidence",
            "",
            "| Metric | Value |",
            "|---|---|",
            f"| Generated report files | {layout['generated_report_files']} |",
            f"| Flat files in generated root | {layout['flat_files_in_generated_root']} |",
            f"| Categories | {layout['category_count']} ({', '.join(layout['categories'])}) |",
            f"| Missing registry outputs | {len(layout['missing_registry_outputs'])} |",
            f"| Orphan generated reports | {len(layout['orphan_generated_reports'])} |",
            f"| Skipped reports | {len(layout['skipped_reports'])} |",
            f"| Failed reports | {len(layout['failed_reports'])} |",
            "",
            "## Known Skipped Inputs",
            "",
            "| Report | Status | Missing Inputs | Reason |",
            "|---|---|---|---|",
        ]
    )
    skipped = layout.get("skipped_reports", [])
    if skipped:
        for report in skipped:
            lines.append(
                f"| `{report.get('report_name', '-')}` | {report.get('status', '-')} | "
                f"{', '.join(f'`{item}`' for item in report.get('missing_inputs', [])) or '-'} | "
                "local optional inputs are missing or unavailable |"
            )
    else:
        lines.append("| `-` | none | - | no skipped reports |")
    lines.extend(
        [
            "",
            "## Git Evidence",
            "",
            "| Command | Status | Return Code | Output Hash |",
            "|---|---|---:|---|",
        ]
    )
    for name, record in payload["git"].items():
        lines.append(f"| `{name}` | {record['status']} | {record['return_code']} | `{record['output_sha256']}` |")
    lines.extend(
        [
            "",
            "## Proof Summary",
            "",
            "The generated report layout was validated on the system above.",
        ]
    )
    for check in payload["checks"]:
        lines.append(f"- `{check['command']}`: {check['status']}")
    lines.extend(
        [
            f"- Flat generated root files: {layout['flat_files_in_generated_root']}",
            f"- Categorized generated report files: {layout['generated_report_files']}",
        ]
    )
    if skipped:
        lines.append("- Known skipped report: runtime/cache reports due to missing optional local inputs")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector-root", default=".")
    parser.add_argument("--framework-root", default=None)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--skip-check-runs", action="store_true")
    args = parser.parse_args()

    connector_root = Path(args.connector_root).resolve()
    framework_root = Path(args.framework_root).resolve() if args.framework_root else connector_root / "modules/ModSecurity-test-Framework"
    output_dir = Path(args.output_dir).resolve() if args.output_dir else connector_root / GENERATED_ROOT / "manifest"
    generated_at = utc_now()
    initial_env = os.environ.copy()
    framework_environment = load_framework_environment(connector_root, framework_root)

    os_release = read_os_release()
    checks = []
    if args.skip_check_runs:
        for command in (
            "make refresh-connector-reports",
            "make check-generated-report-layout",
            "make lint",
            "make quick-check",
            "git status --short",
        ):
            checks.append(
                {
                    "command": command,
                    "started_at": generated_at,
                    "finished_at": generated_at,
                    "duration_seconds": 0.0,
                    "return_code": 0,
                    "status": "not-run-by-generator",
                    "output_excerpt": "Skipped by --skip-check-runs.",
                    "output_sha256": hashlib.sha256(b"").hexdigest(),
                }
            )
    else:
        checks = [
            run(["make", "refresh-connector-reports"], connector_root, timeout=900),
            run(["make", "check-generated-report-layout"], connector_root, timeout=300),
            run(["make", "lint"], connector_root, timeout=900),
            run(["make", "quick-check"], connector_root, timeout=900),
            run(["git", "status", "--short"], connector_root, timeout=120),
        ]

    pip_version = run([sys.executable, "-m", "pip", "--version"], connector_root, timeout=60)
    tools = resolve_tools(connector_root, framework_environment, initial_env)
    readiness = runtime_component_readiness(tools, framework_environment)
    https_policy = https_repo_url_policy(connector_root, framework_root)
    payload = {
        "generated_at": generated_at,
        "framework_common_sh_status": framework_environment["common_sh_status"],
        "framework_environment": {
            key: value for key, value in framework_environment.items() if key != "env"
        },
        "os": {
            "name": os_release.get("NAME", platform.system()),
            "version": os_release.get("VERSION", platform.version()),
            "kernel": platform.release(),
            "architecture": platform.machine(),
            "hostname": socket.gethostname(),
            "user": getpass.getuser(),
            "working_directory": str(connector_root),
            "uname": " ".join(platform.uname()),
        },
        "tools": tools,
        "runtime_component_readiness": readiness,
        "https_repo_url_policy": https_policy,
        "python": {
            "sys_version": sys.version,
            "sys_executable": sys.executable,
            "sys_platform": sys.platform,
            "platform": platform.platform(),
            "pythonpath": os.environ.get("PYTHONPATH", ""),
            "pythondontwritebytecode": os.environ.get("PYTHONDONTWRITEBYTECODE", ""),
            "venv_exists": (connector_root / ".venv").is_dir(),
            "pip_version": pip_version["output_excerpt"].splitlines()[0] if pip_version["output_excerpt"] else "missing",
            "pip_freeze": pip_freeze_summary(connector_root),
        },
        "git": git_evidence(connector_root, framework_root),
        "checks": checks,
        "layout": layout_evidence(connector_root),
    }
    metadata = build_metadata(
        generated_by="ci/generate-system-environment-proof.py",
        make_target="generate-system-environment-proof",
        connector_root=connector_root,
        framework_root=framework_root,
        inputs=[
            report_path(connector_root, "report_refresh_manifest", "json"),
            report_path(connector_root, "report_freshness", "json"),
            report_path(connector_root, "merge_readiness_dashboard", "json"),
        ],
        generated_at=generated_at,
        report_key="system_environment_proof",
        extra={"check_statuses": [{key: item[key] for key in ("command", "status", "return_code")} for item in checks]},
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / GENERATED_REPORTS["system_environment_proof"].filename("json")
    md_path = output_dir / GENERATED_REPORTS["system_environment_proof"].filename("md")
    json_path.write_text(generated_json_text(payload, metadata), encoding="utf-8")
    md_path.write_text(generated_markdown_text(render_markdown(payload), metadata), encoding="utf-8")
    print(md_path)
    return 0 if all(item["return_code"] == 0 for item in checks if item["status"] != "not-run-by-generator") else 2


if __name__ == "__main__":
    raise SystemExit(main())
