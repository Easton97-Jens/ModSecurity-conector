#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from runtime_path_utils import is_allowed_runtime_path, is_system_write_path


CONNECTOR_ROOT = Path(__file__).resolve().parents[1]
FRAMEWORK_ROOT = CONNECTOR_ROOT / "modules/ModSecurity-test-Framework"
VERIFIED_ROOT = Path("/var/tmp/ModSecurity-conector-verified")


def fail(message: str) -> None:
    print(f"check-runtime-path-policy: FAIL: {message}")
    raise SystemExit(1)


def check_python_policy() -> None:
    env = {
        **os.environ,
        "VERIFIED_RUN_ROOT": str(VERIFIED_ROOT),
        "RUNNER_TEMP": "/tmp/runner-temp",
        "TMPDIR": "/tmp",
    }
    allowed = (
        VERIFIED_ROOT,
        VERIFIED_ROOT / "component-cache",
        Path("/tmp/ModSecurity-conector-verified"),
        Path("/tmp/runner-temp/ModSecurity-conector-verified"),
    )
    blocked = (
        Path("/var"),
        Path("/var/lib/foo"),
        Path("/var/log/foo"),
        Path("/var/cache/foo"),
        Path("/etc/foo"),
        Path("/usr/local/foo"),
        Path("/root/.local/state/foo"),
    )
    for path in allowed:
        if is_system_write_path(path):
            fail(f"python marked allowed runtime path as system write path: {path}")
        if not is_allowed_runtime_path(path, env):
            fail(f"python rejected allowed runtime path: {path}")
    for path in blocked:
        if not is_system_write_path(path):
            fail(f"python did not block system/runtime path: {path}")


def shell_status(script: str) -> int:
    env = {
        **os.environ,
        "CONNECTOR_ROOT": str(CONNECTOR_ROOT),
        "FRAMEWORK_ROOT": str(FRAMEWORK_ROOT),
        "REPO_ROOT": str(CONNECTOR_ROOT),
        "VERIFIED_RUN_ROOT": str(VERIFIED_ROOT),
    }
    result = subprocess.run(
        ["bash", "-lc", script],
        cwd=str(CONNECTOR_ROOT),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode


def check_shell_policy() -> None:
    common = "set -eu; . \"$FRAMEWORK_ROOT/ci/common.sh\"; "
    expected_system = (
        "/var",
        "/var/lib/foo",
        "/var/log/foo",
        "/var/cache/foo",
        "/etc/foo",
        "/usr/local/foo",
    )
    expected_not_system = (
        str(VERIFIED_ROOT),
        str(VERIFIED_ROOT / "component-cache"),
        "/tmp/ModSecurity-conector-verified",
    )
    for path in expected_system:
        rc = shell_status(common + f"ci_path_is_system_path {sh_quote(path)}")
        if rc != 0:
            fail(f"shell did not classify system path as blocked: {path}")
    for path in expected_not_system:
        rc = shell_status(common + f"ci_path_is_system_path {sh_quote(path)}")
        if rc == 0:
            fail(f"shell classified allowed runtime path as system path: {path}")

    rc = shell_status(common + f"assert_safe_runtime_path {sh_quote(str(VERIFIED_ROOT / 'component-cache'))} test_path")
    if rc != 0:
        fail(f"shell rejected allowed safe runtime path: {VERIFIED_ROOT / 'component-cache'}")
    rc = shell_status(common + "assert_safe_runtime_path /root/.local/state/foo test_path")
    if rc == 0:
        fail("shell accepted old /root runtime path")


def sh_quote(value: str) -> str:
    return "'" + value.replace("'", "'\"'\"'") + "'"


def main() -> int:
    check_python_policy()
    check_shell_policy()
    print("check-runtime-path-policy: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
