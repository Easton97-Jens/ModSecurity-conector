#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

# CI helpers are shared from ci/lib even when this file is executed directly.
_CI_ROOT = next(parent for parent in Path(__file__).resolve().parents if parent.name == "ci")
if str(_CI_ROOT / "lib") not in sys.path:
    sys.path.insert(0, str(_CI_ROOT / "lib"))

from runtime_path_utils import is_allowed_runtime_path, is_system_write_path, verified_runtime_paths


CONNECTOR_ROOT = next(parent for parent in Path(__file__).resolve().parents if (parent / "Makefile").is_file())
FRAMEWORK_ROOT = CONNECTOR_ROOT / "modules/ModSecurity-test-Framework"
VERIFIED_ROOT = Path("/var/tmp/ModSecurity-conector-verified")
RUNTIME_PATH_OVERRIDES = (
    "VERIFIED_RUN_ROOT",
    "VERIFIED_STATE_ROOT",
    "VERIFIED_BUILD_ROOT",
    "VERIFIED_SOURCE_ROOT",
    "VERIFIED_TMP_ROOT",
    "VERIFIED_LOG_ROOT",
    "CACHE_ROOT",
    "VERIFIED_COMPONENT_CACHE",
    "CONNECTOR_COMPONENT_CACHE",
    "SOURCE_ROOT",
    "BUILD_ROOT",
    "TMP_ROOT",
    "LOG_ROOT",
    "NGINX_HARNESS_PARENT",
    "RUNTIME_RUN_ROOT",
    "RUNTIME_LOG_ROOT",
    "MATRIX_ROOT",
    "MRTS_BUILD_ROOT",
    "MRTS_NATIVE_ROOT",
)


def fail(message: str) -> None:
    print(f"check-runtime-path-policy: FAIL: {message}")
    raise SystemExit(1)


def policy_environment() -> dict[str, str]:
    """Return a deterministic environment for default-path policy self-tests.

    This checker deliberately verifies *defaults*.  A caller may legitimately
    invoke it beneath a custom Cache-v2 run root, so inherited path overrides
    must not leak into the self-test and make its fixed expected defaults look
    incorrect.
    """
    env = dict(os.environ)
    for name in RUNTIME_PATH_OVERRIDES:
        env.pop(name, None)
    env.update(
        {
            "CONNECTOR_ROOT": str(CONNECTOR_ROOT),
            "FRAMEWORK_ROOT": str(FRAMEWORK_ROOT),
            "REPO_ROOT": str(CONNECTOR_ROOT),
            "VERIFIED_RUN_ROOT": str(VERIFIED_ROOT),
            "RUNNER_TEMP": "/tmp/runner-temp",
            "TMPDIR": "/tmp",
        }
    )
    return env


def check_python_policy() -> None:
    env = policy_environment()
    writable_allowed = (
        VERIFIED_ROOT,
        VERIFIED_ROOT / "cache-v2",
        VERIFIED_ROOT / "cache-v2" / "shared",
    )
    read_only_sources = (
        Path("/src"),
        Path("/src/ModSecurity-conector-build"),
        CONNECTOR_ROOT,
        CONNECTOR_ROOT / "build",
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
    for path in writable_allowed:
        if is_system_write_path(path, env):
            fail(f"python marked allowed runtime path as system write path: {path}")
        if not is_allowed_runtime_path(path, env):
            fail(f"python rejected allowed runtime path: {path}")
    for path in read_only_sources:
        if not is_system_write_path(path, env):
            fail(f"python accepted read-only source path as writable: {path}")
        if not is_allowed_runtime_path(path, env):
            fail(f"python rejected read-only source path: {path}")
    for path in blocked:
        if not is_system_write_path(path):
            fail(f"python did not block system/runtime path: {path}")
    paths = verified_runtime_paths(env)
    if paths["CACHE_ROOT"] != str(VERIFIED_ROOT / "cache-v2"):
        fail(f"unexpected default cache root: {paths['CACHE_ROOT']}")
    if paths["VERIFIED_COMPONENT_CACHE"] != str(VERIFIED_ROOT / "cache-v2" / "shared"):
        fail(f"unexpected default shared cache: {paths['VERIFIED_COMPONENT_CACHE']}")


def shell_status(script: str) -> int:
    env = policy_environment()
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
    common = "set -eu; . \"$FRAMEWORK_ROOT/ci/lib/common.sh\"; "
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
        str(VERIFIED_ROOT / "cache-v2"),
        str(VERIFIED_ROOT / "cache-v2" / "shared"),
        "/tmp/ModSecurity-conector-verified",
        "/src",
        "/src/ModSecurity-conector-build",
        str(CONNECTOR_ROOT),
        str(CONNECTOR_ROOT / "build"),
    )
    for path in expected_system:
        rc = shell_status(common + f"ci_path_is_system_path {sh_quote(path)}")
        if rc != 0:
            fail(f"shell did not classify system path as blocked: {path}")
    for path in expected_not_system:
        rc = shell_status(common + f"ci_path_is_system_path {sh_quote(path)}")
        if rc == 0:
            fail(f"shell classified allowed runtime path as system path: {path}")

    rc = shell_status(common + f"assert_safe_runtime_path {sh_quote(str(VERIFIED_ROOT / 'cache-v2' / 'shared'))} test_path")
    if rc != 0:
        fail(f"shell rejected allowed safe runtime path: {VERIFIED_ROOT / 'cache-v2' / 'shared'}")
    # Source roots are legitimate non-system/read-only inputs, not mutable
    # runtime destinations.  A Framework candidate may therefore reject them
    # through assert_safe_runtime_path while still accepting the verified cache
    # root above.
    rc = shell_status(common + "assert_safe_runtime_path /root/.local/state/foo test_path")
    if rc == 0:
        fail("shell accepted old /root runtime path")

    haproxy_allowed = haproxy_policy_selftest(str(VERIFIED_ROOT / "cache-v2" / "shared" / "sources"))
    rc = shell_status(haproxy_allowed)
    if rc != 0:
        fail(f"HAProxy smoke policy rejected verified component-cache SOURCE_ROOT: {VERIFIED_ROOT / 'cache-v2' / 'shared' / 'sources'}")

    for blocked_path in ("/var/lib/foo", "/var/log/foo", "/usr/local/foo", "/etc/foo"):
        rc = shell_status(haproxy_policy_selftest(blocked_path))
        if rc == 0:
            fail(f"HAProxy smoke policy accepted blocked SOURCE_ROOT: {blocked_path}")


def sh_quote(value: str) -> str:
    return "'" + value.replace("'", "'\"'\"'") + "'"


def haproxy_policy_selftest(source_root: str) -> str:
    build_root = VERIFIED_ROOT / "build" / "haproxy-policy-selftest"
    log_root = build_root / "logs"
    return " ".join(
        [
            "set -eu;",
            f"VERIFIED_RUN_ROOT={sh_quote(str(VERIFIED_ROOT))}",
            f"CONNECTOR_COMPONENT_CACHE={sh_quote(str(VERIFIED_ROOT / 'cache-v2' / 'shared'))}",
            f"SOURCE_ROOT={sh_quote(source_root)}",
            f"BUILD_ROOT={sh_quote(str(build_root))}",
            f"RESULTS_DIR={sh_quote(str(build_root / 'results'))}",
            f"TMP_ROOT={sh_quote(str(build_root / 'tmp'))}",
            f"LOG_ROOT={sh_quote(str(log_root))}",
            f"LOG_DIR={sh_quote(str(log_root / 'haproxy-runtime'))}",
            f"RUNTIME_BASE={sh_quote(str(build_root / 'haproxy-runtime-cases'))}",
            "HAPROXY_SMOKE_POLICY_SELFTEST=1",
            "connectors/haproxy/harness/run_haproxy_smoke.sh",
        ]
    )


def main() -> int:
    check_python_policy()
    check_shell_policy()
    print("check-runtime-path-policy: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
