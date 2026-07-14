"""Regression tests for explicit optional-prerequisite CI status handling."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shlex
import shutil
import stat
import subprocess
import sys
import tempfile
import textwrap
import unittest


ROOT = Path(__file__).resolve().parents[1]
STATUS_RUNNER = ROOT / "ci" / "tools" / "run-check-status.py"
MAKEFILE = ROOT / "Makefile"
MAKE = shutil.which("make")


def temporary_directory() -> tempfile.TemporaryDirectory[str]:
    """Keep synthetic fixtures below the configured external temporary root."""
    parent_value = os.environ.get("CODEX_TEMP_ROOT") or os.environ.get("RUNNER_TEMP")
    if parent_value:
        parent = Path(parent_value) / "test-optional-prerequisite-status"
        parent.mkdir(parents=True, exist_ok=True)
        return tempfile.TemporaryDirectory(prefix="case-", dir=parent)
    return tempfile.TemporaryDirectory(prefix="optional-prerequisite-status-")


def write_executable(path: Path, content: str) -> None:
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR)


class OptionalPrerequisiteStatusTests(unittest.TestCase):
    maxDiff = None

    def make_fixture(self, temporary: Path, apxs_present: bool) -> tuple[Path, dict[str, str]]:
        bin_dir = temporary / "bin"
        bin_dir.mkdir()
        if apxs_present:
            write_executable(
                bin_dir / "apxs",
                """
                #!/bin/sh
                exit 0
                """,
            )
        dependent = temporary / "dependent-check"
        write_executable(
            dependent,
            """
            #!/bin/sh
            if ! command -v apxs >/dev/null 2>&1; then
                echo "CHECK_STATUS_REASON apache_development_prerequisite" >&2
                echo "BLOCKED: synthetic dependent check missing apxs" >&2
                exit 77
            fi
            case "${DEPENDENT_CHECK_MODE:-pass}" in
                pass)
                    exit 0
                    ;;
                fail)
                    echo "FAIL: synthetic dependent check failed" >&2
                    exit 23
                    ;;
                unknown)
                    echo "FAIL: synthetic dependent check returned an unknown code" >&2
                    exit 41
                    ;;
                unapproved-blocked)
                    echo "CHECK_STATUS_REASON framework_unavailable" >&2
                    echo "BLOCKED: synthetic dependent check missing Framework" >&2
                    exit 77
                    ;;
            esac
            exit 99
            """,
        )
        environment = os.environ.copy()
        environment["PATH"] = str(bin_dir)
        return dependent, environment

    def run_status_runner(
        self,
        status_file: Path,
        dependent: Path | None,
        environment: dict[str, str],
        *options: str,
    ) -> tuple[subprocess.CompletedProcess[str], dict[str, object]]:
        command = [
            sys.executable,
            str(STATUS_RUNNER),
            "--check",
            "synthetic_apache_dependent_check",
            "--status-file",
            str(status_file),
            *options,
        ]
        if dependent is not None:
            command.extend(["--", str(dependent)])
        result = subprocess.run(
            command,
            cwd=ROOT,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=environment,
        )
        return result, json.loads(status_file.read_text(encoding="utf-8"))

    def test_present_apxs_and_successful_dependent_check_passes(self) -> None:
        with temporary_directory() as temporary_name:
            temporary = Path(temporary_name)
            dependent, environment = self.make_fixture(temporary, apxs_present=True)
            result, record = self.run_status_runner(
                temporary / "status.json", dependent, environment
            )

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("passed", record["status"])
        self.assertEqual(0, record["command_exit_code"])
        self.assertEqual(0, record["workflow_exit_code"])
        self.assertFalse(record["allowed_by_contract"])

    def test_present_apxs_and_real_dependent_failure_remains_failed(self) -> None:
        with temporary_directory() as temporary_name:
            temporary = Path(temporary_name)
            dependent, environment = self.make_fixture(temporary, apxs_present=True)
            environment["DEPENDENT_CHECK_MODE"] = "fail"
            result, record = self.run_status_runner(
                temporary / "status.json", dependent, environment
            )

        self.assertEqual(23, result.returncode, result.stderr)
        self.assertEqual("failed", record["status"])
        self.assertEqual(23, record["command_exit_code"])
        self.assertEqual(23, record["workflow_exit_code"])
        self.assertFalse(record["allowed_by_contract"])

    def test_missing_optional_apxs_is_blocked_but_explicitly_allowed(self) -> None:
        with temporary_directory() as temporary_name:
            temporary = Path(temporary_name)
            dependent, environment = self.make_fixture(temporary, apxs_present=False)
            result, record = self.run_status_runner(
                temporary / "status.json",
                dependent,
                environment,
                "--allow-blocked-reason",
                "apache_development_prerequisite",
            )

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("BLOCKED: synthetic dependent check missing apxs", result.stderr)
        self.assertIn("CHECK_STATUS", result.stdout)
        self.assertEqual("blocked", record["status"])
        self.assertEqual(77, record["command_exit_code"])
        self.assertEqual(0, record["workflow_exit_code"])
        self.assertTrue(record["allowed_by_contract"])

    @unittest.skipIf(MAKE is None, "GNU Make is required by the repository")
    def test_missing_mandatory_apxs_remains_red_through_make(self) -> None:
        with temporary_directory() as temporary_name:
            temporary = Path(temporary_name)
            dependent, environment = self.make_fixture(temporary, apxs_present=False)
            status_file = temporary / "mandatory.json"
            makefile = temporary / "Makefile"
            command = " ".join(
                shlex.quote(part)
                for part in (
                    sys.executable,
                    str(STATUS_RUNNER),
                    "--check",
                    "mandatory_apache_dependent_check",
                    "--status-file",
                    str(status_file),
                    "--",
                    str(dependent),
                )
            )
            makefile.write_text(f"mandatory:\n\t{command}\n", encoding="utf-8")
            result = subprocess.run(
                [MAKE, "-f", str(makefile), "mandatory"],
                cwd=temporary,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=environment,
            )
            record = json.loads(status_file.read_text(encoding="utf-8"))

        self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual("blocked", record["status"])
        self.assertEqual(77, record["command_exit_code"])
        self.assertEqual(77, record["workflow_exit_code"])
        self.assertFalse(record["allowed_by_contract"])

    def test_unapproved_blocked_reason_remains_nonzero(self) -> None:
        with temporary_directory() as temporary_name:
            temporary = Path(temporary_name)
            dependent, environment = self.make_fixture(temporary, apxs_present=True)
            environment["DEPENDENT_CHECK_MODE"] = "unapproved-blocked"
            result, record = self.run_status_runner(
                temporary / "status.json",
                dependent,
                environment,
                "--allow-blocked-reason",
                "apache_development_prerequisite",
            )

        self.assertEqual(77, result.returncode, result.stderr)
        self.assertEqual("blocked", record["status"])
        self.assertEqual("framework_unavailable", record["reason"])
        self.assertEqual(77, record["workflow_exit_code"])
        self.assertFalse(record["allowed_by_contract"])

    @unittest.skipIf(MAKE is None, "GNU Make is required by the repository")
    def test_recursive_make_keeps_the_persisted_blocked_classification(self) -> None:
        with temporary_directory() as temporary_name:
            temporary = Path(temporary_name)
            dependent, environment = self.make_fixture(temporary, apxs_present=False)
            status_file = temporary / "recursive.json"
            inner = temporary / "inner.mk"
            outer = temporary / "outer.mk"
            command = " ".join(
                shlex.quote(part)
                for part in (
                    sys.executable,
                    str(STATUS_RUNNER),
                    "--check",
                    "optional_apache_dependent_check",
                    "--status-file",
                    str(status_file),
                    "--allow-blocked-reason",
                    "apache_development_prerequisite",
                    "--",
                    str(dependent),
                )
            )
            inner.write_text(f"optional:\n\t{command}\n", encoding="utf-8")
            outer.write_text(
                f"MAKE := {shlex.quote(MAKE)}\nouter:\n\t$(MAKE) -f {shlex.quote(str(inner))} optional\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [MAKE, "-f", str(outer), "outer"],
                cwd=temporary,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=environment,
            )
            record = json.loads(status_file.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual("blocked", record["status"])
        self.assertEqual(77, record["command_exit_code"])
        self.assertEqual(0, record["workflow_exit_code"])

    @unittest.skipIf(MAKE is None, "GNU Make is required by the repository")
    def test_lint_target_rejects_an_unclassified_framework_block(self) -> None:
        with temporary_directory() as temporary_name:
            temporary = Path(temporary_name)
            status_file = temporary / "framework-block.json"
            environment = os.environ.copy()
            environment["FRAMEWORK_ROOT"] = str(temporary / "missing-framework")
            environment["APACHE_REQUEST_TRANSACTION_CLEANUP_STATUS_FILE"] = str(status_file)
            environment["BUILD_ROOT"] = str(temporary / "build")
            environment["PYTHON"] = sys.executable
            result = subprocess.run(
                [MAKE, "--no-print-directory", "check-apache-request-transaction-cleanup-lint"],
                cwd=ROOT,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=environment,
            )
            record = json.loads(status_file.read_text(encoding="utf-8"))

        self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("missing framework common.sh", result.stderr)
        self.assertEqual("blocked", record["status"])
        self.assertEqual("unclassified direct blocked exit code 77", record["reason"])
        self.assertEqual(77, record["workflow_exit_code"])
        self.assertFalse(record["allowed_by_contract"])

    def test_unknown_exit_code_remains_a_failure(self) -> None:
        with temporary_directory() as temporary_name:
            temporary = Path(temporary_name)
            dependent, environment = self.make_fixture(temporary, apxs_present=True)
            environment["DEPENDENT_CHECK_MODE"] = "unknown"
            result, record = self.run_status_runner(
                temporary / "status.json",
                dependent,
                environment,
                "--allow-blocked-reason",
                "apache_development_prerequisite",
            )

        self.assertEqual(41, result.returncode, result.stderr)
        self.assertEqual("failed", record["status"])
        self.assertEqual(41, record["command_exit_code"])
        self.assertEqual(41, record["workflow_exit_code"])
        self.assertFalse(record["allowed_by_contract"])

    @unittest.skipIf(MAKE is None, "GNU Make is required by the repository")
    def test_other_common_check_is_not_skipped_after_optional_block(self) -> None:
        with temporary_directory() as temporary_name:
            temporary = Path(temporary_name)
            dependent, environment = self.make_fixture(temporary, apxs_present=False)
            status_file = temporary / "optional.json"
            makefile = temporary / "Makefile"
            command = " ".join(
                shlex.quote(part)
                for part in (
                    sys.executable,
                    str(STATUS_RUNNER),
                    "--check",
                    "optional_apache_dependent_check",
                    "--status-file",
                    str(status_file),
                    "--allow-blocked-reason",
                    "apache_development_prerequisite",
                    "--",
                    str(dependent),
                )
            )
            makefile.write_text(
                f"all: optional common\n\noptional:\n\t{command}\n\ncommon:\n\t@exit 19\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [MAKE, "-f", str(makefile), "all"],
                cwd=temporary,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=environment,
            )
            record = json.loads(status_file.read_text(encoding="utf-8"))

        self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual("blocked", record["status"])
        self.assertTrue(record["allowed_by_contract"])
        self.assertIn("Error 19", result.stderr)

    @unittest.skipIf(MAKE is None, "GNU Make is required by the repository")
    def test_other_connector_check_is_not_skipped_after_optional_block(self) -> None:
        with temporary_directory() as temporary_name:
            temporary = Path(temporary_name)
            dependent, environment = self.make_fixture(temporary, apxs_present=False)
            status_file = temporary / "optional.json"
            makefile = temporary / "Makefile"
            command = " ".join(
                shlex.quote(part)
                for part in (
                    sys.executable,
                    str(STATUS_RUNNER),
                    "--check",
                    "optional_apache_dependent_check",
                    "--status-file",
                    str(status_file),
                    "--allow-blocked-reason",
                    "apache_development_prerequisite",
                    "--",
                    str(dependent),
                )
            )
            makefile.write_text(
                f"all: optional connector\n\noptional:\n\t{command}\n\nconnector:\n\t@exit 29\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [MAKE, "-f", str(makefile), "all"],
                cwd=temporary,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=environment,
            )
            record = json.loads(status_file.read_text(encoding="utf-8"))

        self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual("blocked", record["status"])
        self.assertTrue(record["allowed_by_contract"])
        self.assertIn("Error 29", result.stderr)

    def test_explicit_non_execution_statuses_follow_the_documented_contract(self) -> None:
        with temporary_directory() as temporary_name:
            temporary = Path(temporary_name)
            environment = os.environ.copy()
            not_applicable_result, not_applicable_record = self.run_status_runner(
                temporary / "not-applicable.json",
                None,
                environment,
                "--allow-not-applicable",
                "--not-applicable",
                "synthetic scope excludes this path",
            )
            not_executed_result, not_executed_record = self.run_status_runner(
                temporary / "not-executed.json",
                None,
                environment,
                "--not-executed",
                "synthetic command was deliberately not started",
            )

        self.assertEqual(0, not_applicable_result.returncode, not_applicable_result.stderr)
        self.assertEqual("not_applicable", not_applicable_record["status"])
        self.assertTrue(not_applicable_record["allowed_by_contract"])
        self.assertNotEqual(0, not_executed_result.returncode)
        self.assertEqual("not_executed", not_executed_record["status"])
        self.assertFalse(not_executed_record["allowed_by_contract"])

    @unittest.skipIf(MAKE is None, "GNU Make is required by the repository")
    def test_lint_target_accepts_only_the_direct_apache_preflight_marker(self) -> None:
        makefile = MAKEFILE.read_text(encoding="utf-8")
        target = makefile.split("check-apache-request-transaction-cleanup-lint:\n", 1)[1].split(
            "\n\n", 1
        )[0]
        self.assertIn("ci/tools/run-check-status.py", target)
        self.assertIn(
            "--allow-blocked-reason apache_development_prerequisite", target
        )
        self.assertIn("check-apache-request-transaction-cleanup.sh", target)
        self.assertNotIn("$(MAKE)", target)

        with temporary_directory() as temporary_name:
            temporary = Path(temporary_name)
            status_file = temporary / "actual-target.json"
            include_dir = temporary / "apache-include"
            include_dir.mkdir()
            apxs_without_headers = temporary / "apxs-without-headers"
            write_executable(
                apxs_without_headers,
                f"""
                #!/bin/sh
                if [ \"$1\" = \"-q\" ] && [ \"$2\" = \"INCLUDEDIR\" ]; then
                    printf '%s\\n' {shlex.quote(str(include_dir))}
                fi
                """,
            )
            environment = os.environ.copy()
            environment.pop("APXS_BIN", None)
            environment["APXS"] = str(apxs_without_headers)
            environment["FRAMEWORK_ROOT"] = str(ROOT / "modules" / "ModSecurity-test-Framework")
            environment["APACHE_REQUEST_TRANSACTION_CLEANUP_STATUS_FILE"] = str(status_file)
            environment["BUILD_ROOT"] = str(temporary / "build")
            environment["CONNECTOR_COMPONENT_CACHE"] = str(temporary / "component-cache")
            environment["CI_APXS_BIN_CANDIDATES"] = "synthetic-no-apxs"
            environment["CC"] = sys.executable
            environment["PYTHON"] = sys.executable
            result = subprocess.run(
                [MAKE, "--no-print-directory", "check-apache-request-transaction-cleanup-lint"],
                cwd=ROOT,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=environment,
            )
            record = json.loads(status_file.read_text(encoding="utf-8"))

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("CHECK_STATUS_REASON apache_development_prerequisite", result.stderr)
        self.assertEqual("blocked", record["status"])
        self.assertEqual("apache_development_prerequisite", record["reason"])
        self.assertEqual(77, record["command_exit_code"])
        self.assertEqual(0, record["workflow_exit_code"])


if __name__ == "__main__":
    unittest.main()
