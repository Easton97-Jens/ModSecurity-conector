"""Regression coverage for hosted NGINX case-materialization containment."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FRAMEWORK_ROOT = ROOT / "modules" / "ModSecurity-test-Framework"
FRAMEWORK_ROOT = Path(
    os.environ.get("MSCONNECTOR_TEST_FRAMEWORK_ROOT", DEFAULT_FRAMEWORK_ROOT)
).resolve()
CASE_CLI = FRAMEWORK_ROOT / "tests" / "runners" / "case_cli.py"
CASE_FILE = (
    FRAMEWORK_ROOT
    / "tests"
    / "cases"
    / "connector-specific"
    / "nginx"
    / "nginx_phase4_deny_after_commit_log_only.yaml"
)
RULE_PREAMBLE = FRAMEWORK_ROOT / "tests" / "rules" / "no-crs-baseline.conf"
CASE_NAME = "nginx_phase4_deny_after_commit_log_only"


class NginxFunctionalMaterializationLayoutTest(unittest.TestCase):
    def setUp(self) -> None:
        for required in (CASE_CLI, CASE_FILE, RULE_PREAMBLE):
            self.assertTrue(required.is_file(), f"missing Framework test input: {required}")

    def materialize(
        self,
        *,
        output_root: Path,
        runtime_root: Path,
        log_root: Path,
        server_log_root: Path,
    ) -> subprocess.CompletedProcess[str]:
        audit_dir = server_log_root / "audit"
        audit_dir.mkdir(parents=True, mode=0o700)
        environment = os.environ.copy()
        environment.update(
            {
                "BUILD_ROOT": str(output_root),
                "PYTHONDONTWRITEBYTECODE": "1",
            }
        )
        return subprocess.run(
            [
                sys.executable,
                str(CASE_CLI),
                "materialize",
                "--case",
                str(CASE_FILE),
                "--rules-file",
                str(runtime_root / "conf" / "modsecurity-smoke.conf"),
                "--env-file",
                str(runtime_root / "conf" / "case.env"),
                "--headers-file",
                str(runtime_root / "conf" / "request-headers.txt"),
                "--body-file",
                str(runtime_root / "conf" / "request-body.bin"),
                "--docroot",
                str(runtime_root / "htdocs"),
                "--audit-log-file",
                str(server_log_root / "audit.log"),
                "--audit-log-dir",
                str(audit_dir),
                "--rules-preamble-file",
                str(RULE_PREAMBLE),
                "--nginx-location-directives-file",
                str(runtime_root / "conf" / "nginx-location-directives.conf"),
                "--nginx-runtime-config-dir",
                str(runtime_root / "conf"),
                "--nginx-phase4-log-file",
                str(log_root / "phase4.log"),
            ],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
            env=environment,
        )

    def test_common_case_root_accepts_runtime_and_log_children(self) -> None:
        with tempfile.TemporaryDirectory(prefix="nginx-functional-materialize-") as temporary:
            case_root = Path(temporary) / "on" / "phase4"
            case_root.mkdir(parents=True, mode=0o700)
            runtime_root = case_root / "runtime"
            log_root = case_root / "logs"
            server_log_root = case_root / "harness" / "server-logs" / CASE_NAME

            result = self.materialize(
                output_root=case_root,
                runtime_root=runtime_root,
                log_root=log_root,
                server_log_root=server_log_root,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            expected_outputs = (
                runtime_root / "conf" / "modsecurity-smoke.conf",
                runtime_root / "conf" / "case.env",
                runtime_root / "conf" / "request-headers.txt",
                runtime_root / "conf" / "request-body.bin",
                runtime_root / "conf" / "nginx-location-directives.conf",
                runtime_root / "htdocs" / "index.html",
            )
            for output in expected_outputs:
                self.assertTrue(output.is_file(), output)
                output.resolve().relative_to(case_root.resolve())
            directives = (
                runtime_root / "conf" / "nginx-location-directives.conf"
            ).read_text(encoding="utf-8")
            self.assertIn(str(log_root / "phase4.log"), directives)
            case_environment = (
                runtime_root / "conf" / "case.env"
            ).read_text(encoding="utf-8")
            generated_paths = (
                runtime_root / "conf" / "request-headers.txt",
                runtime_root / "conf" / "request-body.bin",
                server_log_root / "audit.log",
                server_log_root / "audit",
            )
            for generated_path in generated_paths:
                self.assertIn(str(generated_path), case_environment)
                generated_path.resolve().relative_to(case_root.resolve())
            self.assertFalse((server_log_root / "audit.log").exists())

    def test_sibling_runtime_root_is_rejected_by_framework_containment(self) -> None:
        with tempfile.TemporaryDirectory(prefix="nginx-functional-materialize-") as temporary:
            case_root = Path(temporary) / "on" / "phase4"
            output_root = case_root / "build"
            output_root.mkdir(parents=True, mode=0o700)
            runtime_root = case_root / "runtime"
            log_root = case_root / "logs"
            server_log_root = case_root / "harness" / "server-logs" / CASE_NAME

            result = self.materialize(
                output_root=output_root,
                runtime_root=runtime_root,
                log_root=log_root,
                server_log_root=server_log_root,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("write path escapes output root", result.stderr)
            self.assertFalse((runtime_root / "conf" / "modsecurity-smoke.conf").exists())


if __name__ == "__main__":
    unittest.main()
