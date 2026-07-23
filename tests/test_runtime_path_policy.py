from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "ci" / "checks" / "security" / "check-runtime-path-policy.py"
CI_LIB = ROOT / "ci" / "lib"
if str(CI_LIB) not in sys.path:
    sys.path.insert(0, str(CI_LIB))

from runtime_path_utils import (
    default_verified_run_root,
    is_allowed_runtime_path,
    is_system_write_path,
    fixed_runtime_temp_parent,
    verified_runtime_paths,
)


class RuntimePathPolicyTest(unittest.TestCase):
    def test_mutable_project_roots_cannot_authorize_system_runtime_paths(self) -> None:
        """Project-location inputs must never turn system paths into runtime roots."""
        with tempfile.TemporaryDirectory(prefix="runtime-path-policy-control-") as temporary:
            safe_run_root = Path(temporary) / "verified-run"
            poisoned_env = {
                "VERIFIED_RUN_ROOT": str(safe_run_root),
                "REPO_ROOT": "/",
                "CONNECTOR_ROOT": "/",
                "FRAMEWORK_ROOT": "/",
            }

            for attempted_path in (Path("/etc/evidence-escape"), Path("/root/evidence-escape")):
                with self.subTest(attempted_path=attempted_path):
                    self.assertTrue(is_system_write_path(attempted_path, poisoned_env))
                    self.assertFalse(is_allowed_runtime_path(attempted_path, poisoned_env))

            safe_control = safe_run_root / "build" / "apache" / "control-run"
            self.assertFalse(is_system_write_path(safe_control, poisoned_env))
            self.assertTrue(is_allowed_runtime_path(safe_control, poisoned_env))

    def test_broad_runner_parent_cannot_expand_runtime_allowlist(self) -> None:
        """A broad RUNNER_TEMP or TMPDIR value must not authorize arbitrary descendants."""
        with tempfile.TemporaryDirectory(prefix="runtime-path-policy-control-") as temporary:
            env = {
                "VERIFIED_RUN_ROOT": str(Path(temporary) / "verified-run"),
                "RUNNER_TEMP": "/",
                "TMPDIR": "/",
            }

            self.assertFalse(is_allowed_runtime_path(Path("/etc/evidence-escape"), env))
            self.assertFalse(is_allowed_runtime_path(Path("/root/evidence-escape"), env))
            self.assertEqual(
                fixed_runtime_temp_parent() / "ModSecurity-conector-verified",
                default_verified_run_root(env),
            )

    def test_verified_runtime_paths_reject_broad_or_system_writable_roots(self) -> None:
        """Runtime paths must remain narrow external locations, never broad/system roots."""
        with tempfile.TemporaryDirectory(prefix="runtime-path-policy-control-") as temporary:
            safe_run_root = Path(temporary) / "verified-run"
            broad_root_env = {"VERIFIED_RUN_ROOT": "/"}
            direct_root_env = {"VERIFIED_RUN_ROOT": "/runtime-escape"}
            system_build_env = {
                "VERIFIED_RUN_ROOT": str(safe_run_root),
                "BUILD_ROOT": "/etc/evidence-escape",
            }
            system_source_env = {
                "VERIFIED_RUN_ROOT": str(safe_run_root),
                "SOURCE_ROOT": "/etc/evidence-escape",
            }
            with self.assertRaises(ValueError):
                verified_runtime_paths(broad_root_env)
            with self.assertRaises(ValueError):
                verified_runtime_paths(direct_root_env)
            with self.assertRaises(ValueError):
                verified_runtime_paths(system_build_env)
            with self.assertRaises(ValueError):
                verified_runtime_paths(system_source_env)

            external_build_root = safe_run_root.parent / "separate-safe-build-root"
            external_matrix_root = fixed_runtime_temp_parent() / "codex/ModSecurity-conector/matrix"
            safe_external_env = {
                "VERIFIED_RUN_ROOT": str(safe_run_root),
                "BUILD_ROOT": str(external_build_root),
                "MATRIX_ROOT": str(external_matrix_root),
            }
            paths = verified_runtime_paths(safe_external_env)
            self.assertEqual(str(external_build_root), paths["BUILD_ROOT"])
            self.assertEqual(str(external_matrix_root), paths["MATRIX_ROOT"])

    def test_python_path_policy_selftest_accepts_only_writable_run_paths(self) -> None:
        """The reusable Python policy distinguishes runtime writes from source reads."""
        spec = importlib.util.spec_from_file_location("runtime_path_policy_checker", CHECKER)
        assert spec is not None and spec.loader is not None
        checker = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = checker
        spec.loader.exec_module(checker)

        checker.check_python_policy()

    def test_shell_policy_allows_framework_to_reject_source_roots_as_runtime_paths(self) -> None:
        """A source root is non-system/read-only, not a required write-safe path."""
        spec = importlib.util.spec_from_file_location("runtime_path_policy_checker", CHECKER)
        assert spec is not None and spec.loader is not None
        checker = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = checker
        spec.loader.exec_module(checker)

        source_paths = (
            "/src",
            "/src/ModSecurity-conector-build",
            str(ROOT),
            str(ROOT / "build"),
        )
        system_paths = (
            "/var",
            "/var/lib/foo",
            "/var/log/foo",
            "/var/cache/foo",
            "/etc/foo",
            "/usr/local/foo",
        )
        calls: list[str] = []
        original_shell_status = checker.shell_status

        def candidate_shell_status(script: str) -> int:
            calls.append(script)
            if "ci_path_is_system_path" in script:
                return 0 if any(checker.sh_quote(path) in script for path in system_paths) else 1
            if "assert_safe_runtime_path" in script:
                if any(
                    f"assert_safe_runtime_path {checker.sh_quote(path)} test_path" in script
                    for path in source_paths
                ):
                    return 77
                if "assert_safe_runtime_path /root/.local/state/foo test_path" in script:
                    return 77
                return 0
            if "HAPROXY_SMOKE_POLICY_SELFTEST=1" in script:
                return 77 if any(f"SOURCE_ROOT={checker.sh_quote(path)}" in script for path in system_paths) else 0
            return 0

        try:
            checker.shell_status = candidate_shell_status
            checker.check_shell_policy()
        finally:
            checker.shell_status = original_shell_status

        for source_path in source_paths:
            self.assertNotIn(
                f"assert_safe_runtime_path {checker.sh_quote(source_path)} test_path",
                calls,
            )

    def test_default_policy_selftest_ignores_caller_cache_overrides(self) -> None:
        """A custom verified root must not poison the checker’s default probe."""
        with tempfile.TemporaryDirectory(prefix="runtime-path-policy-") as temporary:
            caller_root = Path(temporary) / "custom-run"
            env = {
                **os.environ,
                "VERIFIED_RUN_ROOT": str(caller_root),
                "CACHE_ROOT": str(caller_root / "cache-v2"),
                "VERIFIED_COMPONENT_CACHE": str(caller_root / "cache-v2" / "shared"),
                "BUILD_ROOT": str(caller_root / "build"),
                "TMP_ROOT": str(caller_root / "build" / "tmp"),
                "LOG_ROOT": str(caller_root / "build" / "logs"),
            }
            result = subprocess.run(
                [sys.executable, str(CHECKER)],
                cwd=ROOT,
                env=env,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
