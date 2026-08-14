#!/usr/bin/env python3
"""Run a bounded, read-only host-runtime preflight.

The command deliberately never installs packages, changes the environment, or
starts a service.  It emits one machine-readable result and one short summary
for workflow artifact collection.  A result is PASS only when the required
identity checks and every requested prerequisite have concrete evidence.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


STATUSES = {"PASS", "FAIL", "BLOCKED", "NOT_RUN", "NOT_APPLICABLE"}
MAX_TEXT = 240
MAX_CHECKS = 64
DEFAULT_TIMEOUT = 5.0
LOCK_SHA256 = re.compile(r"^[0-9a-fA-F]{64}$")


def _bounded(value: object, limit: int = MAX_TEXT) -> str:
    text = str(value).replace("\x00", "")
    return text if len(text) <= limit else text[: limit - 3] + "..."


def _safe_name(value: str) -> str:
    return Path(value).name or "unknown"


def _check(name: str, status: str, reason: str, remediation: str) -> dict[str, str]:
    if status not in STATUSES:
        raise ValueError(f"invalid status: {status}")
    return {
        "name": _bounded(name, 80),
        "status": status,
        "reason_code": _bounded(reason, 100),
        "remediation": _bounded(remediation),
    }


def _run(argv: list[str], timeout: float = DEFAULT_TIMEOUT) -> tuple[int, str, str]:
    try:
        result = subprocess.run(
            argv,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=os.environ.copy(),
        )
    except FileNotFoundError:
        return 127, "", "not found"
    except subprocess.TimeoutExpired:
        return 124, "", "timed out"
    return result.returncode, _bounded(result.stdout), _bounded(result.stderr)


def _parse_pair(value: str) -> tuple[str, str]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("expected NAME=VALUE")
    name, expected = value.split("=", 1)
    if not name or not expected:
        raise argparse.ArgumentTypeError("expected non-empty NAME=VALUE")
    return name, expected


def _normal_os(value: str) -> str:
    return value.lower().replace("linux", "linux").replace("darwin", "macos")


def _normal_arch(value: str) -> str:
    aliases = {"x86_64": "amd64", "amd64": "amd64", "aarch64": "arm64", "arm64": "arm64"}
    return aliases.get(value.lower(), value.lower())


def _load_runtime_lock(path: Path, profile: str, expected_os: str, expected_arch: str) -> tuple[dict[str, str], str, str, dict[str, list[Any]]]:
    """Return safe lock metadata, expected version, and a stable error code."""
    if not path.is_file():
        return {}, "", "runtime_lock_missing", {}
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return {}, "", "runtime_lock_invalid", {}
    if not isinstance(document, dict) or document.get("schema_version") != 1:
        return {}, "", "runtime_lock_invalid", {}
    profiles = document.get("profiles")
    if not isinstance(profiles, list) or len(profiles) > MAX_CHECKS:
        return {}, "", "runtime_lock_invalid", {}
    lock_profile = profile
    entry = next((item for item in profiles if isinstance(item, dict) and item.get("id") == lock_profile), None)
    if not isinstance(entry, dict):
        return {"lock_profile": _bounded(lock_profile, 120)}, "", "runtime_lock_invalid", {}
    required = ("os", "arch", "version", "sha256", "asset_name", "download_url", "source_provenance")
    if any(not isinstance(entry.get(key), str) or not entry[key] for key in required):
        return {"lock_profile": _bounded(lock_profile, 120)}, "", "runtime_lock_invalid", {}
    asset = entry["asset_name"]
    download_url = entry["download_url"]
    if Path(asset).name != asset or asset in {".", ".."} or not LOCK_SHA256.fullmatch(entry["sha256"]):
        return {"lock_profile": _bounded(lock_profile, 120)}, "", "runtime_lock_invalid", {}
    parsed_url = urlparse(download_url)
    if parsed_url.scheme != "https" or not parsed_url.hostname or "\n" in download_url or "\r" in download_url:
        return {"lock_profile": _bounded(lock_profile, 120)}, "", "runtime_lock_invalid", {}
    if _normal_os(entry["os"]) != _normal_os(expected_os) or _normal_arch(entry["arch"]) != _normal_arch(expected_arch):
        return {"lock_profile": _bounded(lock_profile, 120)}, "", "runtime_lock_platform_mismatch", {}
    metadata = {
        "name": _safe_name(str(path)),
        "lock_profile": _bounded(lock_profile, 120),
        "expected_version": _bounded(entry["version"], 80),
        "provenance": _bounded(entry["source_provenance"]),
        "asset_id": _bounded(asset, 120),
    }
    requirements = entry.get("requirements", {})
    if not isinstance(requirements, dict):
        return metadata, "", "runtime_lock_invalid", {}
    normalized: dict[str, list[Any]] = {}
    for key in ("headers", "sources", "tools", "configs", "fixtures", "ports"):
        values = requirements.get(key, [])
        if not isinstance(values, list) or len(values) > MAX_CHECKS:
            return metadata, "", "runtime_lock_invalid", {}
        if key == "ports" and any(not isinstance(value, int) for value in values):
            return metadata, "", "runtime_lock_invalid", {}
        if key != "ports" and any(not isinstance(value, str) or not value or "\n" in value for value in values):
            return metadata, "", "runtime_lock_invalid", {}
        normalized[key] = values
    return metadata, entry["version"], "", normalized


def _write_result(output_dir: Path, result: dict[str, Any], output_file: Path | None = None) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    temporary = output_dir / ".status.json.tmp"
    target = output_file or output_dir / "status.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(target)
    summary = output_dir / "summary.md"
    lines = [
        "# Host-runtime preflight",
        "",
        f"- Connector: `{result['connector']}`",
        f"- Profile: `{result['profile']}`",
        f"- Status: **{result['status']}**",
        f"- Reason: `{result['reason_code']}`",
        f"- Remediation: {result['remediation']}",
        "",
        "| Check | Status | Reason |",
        "| --- | --- | --- |",
    ]
    for item in result["checks"]:
        lines.append(f"| `{item['name']}` | `{item['status']}` | `{item['reason_code']}` |")
    summary.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--connector")
    parser.add_argument("--profile", required=True)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--output", type=Path, help="status JSON path (workflow-compatible alias)")
    parser.add_argument("--expected-version", default="")
    parser.add_argument("--runtime-lock", type=Path)
    parser.add_argument("--lock-profile")
    parser.add_argument("--binary", type=Path)
    parser.add_argument("--expected-os", default="linux")
    parser.add_argument("--expected-arch", default="amd64")
    parser.add_argument("--header", action="append", default=[])
    parser.add_argument("--source", action="append", default=[])
    parser.add_argument("--tool", action="append", default=[])
    parser.add_argument("--port", action="append", type=int, default=[])
    parser.add_argument("--write-dir", action="append", default=[])
    parser.add_argument("--disk-path", action="append", default=[])
    parser.add_argument("--min-free-bytes", type=int, default=0)
    parser.add_argument("--config", action="append", default=[])
    parser.add_argument("--fixture", action="append", default=[])
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    args = parser.parse_args(argv)
    if args.output_dir is None and args.output is None:
        parser.error("one of --output-dir or --output is required")
    if args.output_dir is not None and args.output is not None:
        parser.error("--output-dir and --output are mutually exclusive")
    output_dir = args.output.parent if args.output is not None else args.output_dir
    connector = args.connector or args.profile

    checks: list[dict[str, str]] = []
    runtime_lock_meta: dict[str, str] = {}
    lock_reason = ""
    lock_requirements: dict[str, list[Any]] = {}
    if args.runtime_lock is not None:
        lock_profile = args.lock_profile or args.profile
        runtime_lock_meta, locked_version, lock_reason, lock_requirements = _load_runtime_lock(
            args.runtime_lock, lock_profile, args.expected_os, args.expected_arch
        )
        if not lock_reason:
            args.expected_version = locked_version
            checks.append(_check("runtime-lock", "PASS", "runtime_lock_valid", "No action required."))
        else:
            runtime_lock_meta.setdefault("name", _safe_name(str(args.runtime_lock)))
            runtime_lock_meta.setdefault("lock_profile", _bounded(lock_profile, 120))
            checks.append(_check("runtime-lock", "BLOCKED", lock_reason, "Provide a valid reviewed runtime lock and rerun the preflight."))
    elif not args.expected_version:
        lock_reason = "runtime_lock_missing" if args.lock_profile else ""
        if lock_reason:
            checks.append(_check("runtime-lock", "BLOCKED", lock_reason, "Provide the reviewed runtime lock and rerun the preflight."))

    args.header = lock_requirements.get("headers", []) + args.header
    args.source = lock_requirements.get("sources", []) + args.source
    args.tool = lock_requirements.get("tools", []) + args.tool
    args.config = lock_requirements.get("configs", []) + args.config
    args.fixture = lock_requirements.get("fixtures", []) + args.fixture
    args.port = lock_requirements.get("ports", []) + args.port
    checks.append(
        _check(
            "identity.os",
            "PASS" if _normal_os(platform.system()) == _normal_os(args.expected_os) else "BLOCKED",
            "os_match" if _normal_os(platform.system()) == _normal_os(args.expected_os) else "os_mismatch",
            "Run on the reviewed operating system.",
        )
    )
    actual_arch = _normal_arch(platform.machine())
    expected_arch = _normal_arch(args.expected_arch)
    checks.append(
        _check(
            "identity.arch",
            "PASS" if actual_arch == expected_arch else "BLOCKED",
            "arch_match" if actual_arch == expected_arch else "arch_mismatch",
            "Run on the reviewed CPU architecture.",
        )
    )

    binary = args.binary
    actual_version = ""
    if binary is None:
        checks.append(_check("binary", "BLOCKED", "binary_missing", "Provide the expected executable."))
        version_output = ""
    elif not binary.is_file():
        checks.append(_check("binary", "BLOCKED", "binary_missing", "Build or provision the expected executable."))
        version_output = ""
    elif not os.access(binary, os.X_OK):
        checks.append(_check("binary", "BLOCKED", "binary_not_executable", "Make the expected binary executable."))
        version_output = ""
    else:
        checks.append(_check("binary", "PASS", "binary_present", "No action required."))
        code, stdout, stderr = _run([str(binary), "--version"], args.timeout)
        version_output = stdout + " " + stderr
        version_match = re.search(r"\b\d+(?:\.\d+){1,3}\b", version_output)
        actual_version = version_match.group(0) if version_match else "unknown"
        if not args.expected_version:
            checks.append(_check("version", "BLOCKED", "expected_version_missing", "Provide the reviewed runtime version."))
        elif code == 124:
            checks.append(_check("version", "BLOCKED", "version_timeout", "Make the binary version probe responsive."))
        elif code == 127:
            checks.append(_check("version", "BLOCKED", "version_probe_missing", "Provide a runnable binary."))
        elif args.expected_version not in version_output:
            checks.append(_check("version", "BLOCKED", "version_mismatch", "Provision the reviewed runtime version."))
        else:
            checks.append(_check("version", "PASS", "version_match", "No action required."))

    if binary is None and not args.expected_version:
        checks.append(_check("version", "BLOCKED", "expected_version_missing", "Provide the reviewed runtime version."))

    if binary is not None and binary.is_file() and os.access(binary, os.X_OK):
        code, stdout, stderr = _run(["ldd", str(binary)], args.timeout)
        ldd_output = stdout + " " + stderr
        if code == 127:
            checks.append(_check("dynamic-libraries", "BLOCKED", "ldd_missing", "Install or expose ldd for read-only verification."))
        elif code == 124:
            checks.append(_check("dynamic-libraries", "BLOCKED", "ldd_timeout", "Make dependency inspection responsive."))
        elif "not found" in ldd_output:
            checks.append(_check("dynamic-libraries", "BLOCKED", "dynamic_library_missing", "Provision all binary runtime libraries."))
        elif code != 0:
            checks.append(_check("dynamic-libraries", "BLOCKED", "ldd_failed", "Inspect the binary's dynamic dependencies."))
        else:
            checks.append(_check("dynamic-libraries", "PASS", "dynamic_libraries_resolved", "No action required."))
    else:
        checks.append(_check("dynamic-libraries", "BLOCKED", "binary_unavailable", "Provide the expected executable first."))

    def path_check(kind: str, values: list[str], predicate: str = "file") -> None:
        for value in values[:MAX_CHECKS]:
            path = Path(value)
            exists = path.is_file() if predicate == "file" else path.exists()
            checks.append(_check(f"{kind}:{_safe_name(value)}", "PASS" if exists else "BLOCKED", f"{kind}_present" if exists else f"{kind}_missing", "No action required." if exists else f"Provide the required {kind}."))

    path_check("header", args.header)
    path_check("source", args.source, "any")
    path_check("config", args.config)
    path_check("fixture", args.fixture, "any")

    for tool in args.tool[:MAX_CHECKS]:
        found = shutil.which(tool)
        checks.append(_check(f"tool:{_safe_name(tool)}", "PASS" if found else "BLOCKED", "tool_present" if found else "tool_missing", "No action required." if found else "Expose the required host tool."))

    for port in args.port[:MAX_CHECKS]:
        if not 1 <= port <= 65535:
            checks.append(_check(f"port:{port}", "BLOCKED", "port_invalid", "Use a TCP port between 1 and 65535."))
            continue
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(args.timeout)
        try:
            sock.bind(("127.0.0.1", port))
            result = 0
        except OSError:
            result = 1
        finally:
            sock.close()
        checks.append(_check(f"port:{port}", "PASS" if result == 0 else "BLOCKED", "port_free" if result == 0 else "port_in_use", "No action required." if result == 0 else "Stop the conflicting listener or select a free port."))

    for value in args.write_dir[:MAX_CHECKS]:
        path = Path(value)
        writable = path.is_dir() and os.access(path, os.W_OK)
        checks.append(_check(f"write:{_safe_name(value)}", "PASS" if writable else "BLOCKED", "write_available" if writable else "write_unavailable", "No action required." if writable else "Provide a writable evidence/build directory."))

    for value in args.disk_path[:MAX_CHECKS]:
        try:
            free = shutil.disk_usage(value).free
            enough = free >= args.min_free_bytes
        except OSError:
            free = 0
            enough = False
        checks.append(_check(f"disk:{_safe_name(value)}", "PASS" if enough else "BLOCKED", "disk_sufficient" if enough else "disk_insufficient", "No action required." if enough else "Provide sufficient free disk space."))

    if len(checks) > MAX_CHECKS:
        checks = checks[:MAX_CHECKS]
        checks.append(_check("checks", "BLOCKED", "check_limit_reached", "Reduce the preflight input set."))

    statuses = {item["status"] for item in checks}
    if "BLOCKED" in statuses:
        status, reason, remediation = "BLOCKED", lock_reason or "prerequisite_missing", "Resolve blocked prerequisites and rerun the preflight."
    elif "FAIL" in statuses:
        status, reason, remediation = "BLOCKED", "preflight_unclassified_mismatch", "Resolve the preflight mismatch and rerun before host integration."
    elif not checks or "PASS" not in statuses:
        status, reason, remediation = "NOT_RUN", "insufficient_evidence", "Provide the required host-runtime evidence and rerun."
    else:
        status, reason, remediation = "PASS", "preflight_pass", "No action required."

    result: dict[str, Any] = {
        "schema_version": 1,
        "evidence_kind": "preflight",
        "runtime_status": "NOT_RUN",
        "connector": _bounded(connector, 80),
        "profile": _bounded(args.profile, 120),
        "status": status,
        "reason_code": reason,
        "remediation": remediation,
        "observed_at": int(time.time()),
        "host": {"os": _normal_os(platform.system()), "arch": actual_arch},
        "checks": checks,
    }
    if args.runtime_lock is not None:
        runtime_lock_meta.setdefault("expected_version", _bounded(args.expected_version, 80))
        runtime_lock_meta["actual_version"] = _bounded(actual_version, 80)
        result["runtime_lock"] = runtime_lock_meta
        result["lock_profile"] = runtime_lock_meta.get("lock_profile", "")
        result["expected_version"] = runtime_lock_meta.get("expected_version", "")
        result["actual_version"] = runtime_lock_meta.get("actual_version", "")
        result["provenance"] = runtime_lock_meta.get("provenance", "")
        result["asset_id"] = runtime_lock_meta.get("asset_id", "")
    _write_result(output_dir, result, args.output)
    print(json.dumps(result, sort_keys=True))
    return 0 if status == "PASS" else 77 if status == "BLOCKED" else 1


if __name__ == "__main__":
    sys.exit(main())
