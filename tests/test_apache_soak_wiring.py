#!/usr/bin/env python3
"""Guard the Parent-owned Apache Valgrind soak contract."""

from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "ci" / "runtime" / "lifecycle" / "run-apache-soak.sh"
WORKFLOW = ROOT / ".github" / "workflows" / "apache-soak.yml"
HARNESS = ROOT / "connectors" / "apache" / "harness" / "run_apache_smoke.sh"
WORKLOAD = ROOT / "connectors" / "apache" / "harness" / "apache_soak_workload.py"
MAKEFILE = ROOT / "Makefile"


class ApacheSoakWiringTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = RUNNER.read_text(encoding="utf-8")
        self.harness = HARNESS.read_text(encoding="utf-8")
        self.workload = WORKLOAD.read_text(encoding="utf-8")
        self.makefile = MAKEFILE.read_text(encoding="utf-8")

    def test_only_parent_harness_owns_the_apache_lifecycle(self) -> None:
        self.assertIn("run_apache_smoke.sh", self.source)
        self.assertIn("APACHE_SOAK_COMMAND", self.source)
        self.assertIn("APACHE_SOAK_TEST=1", self.source)
        self.assertIn("APACHE_SOAK_HTTPD_WRAPPER", self.source)
        self.assertIn("APACHE_SOAK_RESULT_FILE", self.source)
        self.assertIn("APACHE_SOAK_READY_FILE", self.source)
        self.assertIn("APACHE_SOAK_RUN_ROOT", self.source)
        self.assertIn("checked-in Parent Apache harness executable", self.source)
        self.assertNotIn("Dockerfile", self.source)
        self.assertNotIn("docker-compose", self.source)
        self.assertNotIn("httpd.conf", self.source)

    def test_harness_owns_wrapper_launch_readiness_traffic_and_result(self) -> None:
        for marker in (
            "validate_apache_soak_contract",
            "APACHE_SOAK_HTTPD_WRAPPER",
            "APACHE_SOAK_READY_FILE",
            "APACHE_SOAK_RESULT_FILE",
            '--run-root "$APACHE_SOAK_RUN_ROOT"',
            "write_apache_soak_ready",
            "run_apache_soak",
            "apache_soak_workload.py",
            '"$APACHE_SOAK_HTTPD_WRAPPER" "$APACHE_HTTPD_BIN" -X -f',
            '"$APACHE_HTTPD_BIN" -t -f "$CONFIG_FILE"',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.harness)
        self.assertIn("APACHE_SOAK_TEST=1", self.source)
        self.assertIn("RUN_ONE_CASE=1", self.source)
        self.assertIn("validate_harness_result", self.source)
        self.assertIn("harness_evidence_valid", self.source)
        self.assertIn("restart, readiness, and metadata evidence", self.source)

    def test_workload_is_bounded_loopback_traffic_with_verified_restart_evidence(self) -> None:
        for marker in (
            "127.0.0.1",
            "REQUEST_PATH = \"/__request_body_consume\"",
            "ALLOW_PAYLOAD",
            "DENY_PAYLOAD",
            "LARGE_PAYLOAD",
            '"multi_bucket"',
            "threading.Thread",
            "signal.SIGUSR1",
            "wait_ready",
            "restart_count",
            "atomic_json",
            "RESPONSE_BOUND",
            '"real_httpd_pid"',
            '"instrumented_httpd_launch_pid"',
            "validate_result_path",
            "--run-root",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.workload)
        self.assertNotIn("shell=True", self.workload)
        self.assertNotIn("subprocess", self.workload)

    def test_runner_generates_a_fixed_parent_neutral_request_body_fixture(self) -> None:
        for marker in (
            "apache-soak-neutral.yaml",
            "apache-soak-rules.conf",
            "SecRequestBodyAccess On",
            'SecAuditLog "@@AUDIT_LOG@@"',
            "id:2190500,phase:2,pass,log",
            "id:2190501,phase:2,deny,status:403",
            "/__request_body_consume",
            "TEST_CASE=\"$request_body_case\"",
            "CASE_SCOPE=all",
            "EXTRA_CASE_ROOTS=\"$request_body_conf_root\"",
            "NO_CRS_BASELINE=1",
            "MODSECURITY_TEST_VARIANT=no-crs",
            "MODSECURITY_RULE_PREAMBLE_FILE=\"$request_body_preamble\"",
            "APACHE_REQUEST_BODY_REGRESSION_TEST=1",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.source)

    def test_modes_use_real_valgrind_without_broad_suppressions(self) -> None:
        self.assertIn("memcheck|helgrind", self.source)
        self.assertIn("--tool=memcheck", self.source)
        self.assertIn("--tool=helgrind", self.source)
        self.assertIn("--trace-children=yes", self.source)
        self.assertIn("--error-exitcode=99", self.source)
        self.assertIn("--leak-check=full", self.source)
        self.assertIn("--show-leak-kinds=definite,indirect,possible,reachable", self.source)
        self.assertIn("--errors-for-leak-kinds=definite,indirect,possible", self.source)
        self.assertIn('exec \"$APACHE_SOAK_VALGRIND_BIN\"', self.source)
        self.assertIn("APACHE_SOAK_WRAPPER_USED_FILE", self.source)
        self.assertNotIn("--suppressions", self.source)

    def test_artifact_paths_are_external_and_bounded(self) -> None:
        for marker in (
            "APACHE_SOAK_ROOT is required",
            "prepare_external_directory",
            "reject_symlink_ancestors",
            "must be outside the source checkout",
            "APACHE_SOAK_MAX_LOG_BYTES",
            "APACHE_SOAK_MAX_ARTIFACT_BYTES",
            "limit_log_file",
            "limit_soak_log_aggregate",
            "prepare_upload_bundle",
            "APACHE_SOAK_DURATION_SECONDS",
            "APACHE_SOAK_CONCURRENCY",
            "APACHE_SOAK_REQUEST_TIMEOUT_SECONDS",
            "APACHE_SOAK_RESTART_INTERVAL_SECONDS",
            "APACHE_SOAK_HARD_TIMEOUT_SECONDS",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.source)
        self.assertIn("require_uint_range", self.source)
        self.assertIn("hard timeout expired", self.source)
        self.assertIn("/upload/", WORKFLOW.read_text(encoding="utf-8"))

    def test_nested_path_validators_do_not_mutate_the_caller_directory(self) -> None:
        prepare_start = self.source.index("prepare_external_directory() {")
        prepare_end = self.source.index("\n}\n\nrequire_regular_executable", prepare_start)
        prepare_body = self.source[prepare_start:prepare_end]
        self.assertIn("directory_candidate=$1", prepare_body)
        self.assertIn("mkdir -p \"$directory_candidate\"", prepare_body)
        self.assertIn("cd -P \"$directory_candidate\"", prepare_body)
        self.assertNotIn("\n    candidate=$1\n", prepare_body)
        self.assertIn("path_to_check=$1", self.source)
        self.assertIn("ancestor_path=$1", self.source)

    def test_timeout_and_cleanup_keep_children_contained(self) -> None:
        self.assertIn("setsid env", self.source)
        self.assertIn("watchdog_pid", self.source)
        self.assertIn('kill -TERM -- "-$harness_pid"', self.source)
        self.assertIn('kill -KILL -- "-$harness_pid"', self.source)
        self.assertIn("trap cleanup EXIT", self.source)
        self.assertIn("trap on_signal HUP INT TERM", self.source)
        self.assertIn("The Parent harness owns the only httpd start", self.source)

    def test_reports_distinguish_blocked_not_run_and_memory_categories(self) -> None:
        for marker in (
            "EXIT_PASS=0",
            "EXIT_FAIL=1",
            "EXIT_BLOCKED=77",
            "EXIT_NOT_RUN=78",
            "apache-soak-report.json",
            "apache-soak-report.md",
            '"parent_commit"',
            '"httpd_version"',
            '"apxs_version"',
            '"libmodsecurity_version"',
            '"compiler"',
            '"mpm"',
            '"requests_reported"',
            '"restarts_reported"',
            '"definitely_lost_bytes"',
            '"indirectly_lost_bytes"',
            '"possibly_lost_bytes"',
            '"still_reachable_bytes"',
            '"invalid_read_signals"',
            '"invalid_write_signals"',
            '"invalid_free_signals"',
            '"double_free_signals"',
            '"use_after_free_signals"',
            "not classified as leak-free",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.source)
        self.assertIn("Valgrind is unavailable", self.source)
        self.assertIn("without evidence of an actual Valgrind-instrumented httpd", self.source)

    def test_controlled_values_are_not_evaluated_as_shell(self) -> None:
        self.assertNotIn("eval ", self.source)
        self.assertNotIn("sh -c", self.source)
        self.assertNotIn("bash -c", self.source)

    def test_manual_workflow_is_pinned_and_does_not_promote_blocked_runs(self) -> None:
        source = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("workflow_dispatch:", source)
        self.assertNotIn("\n  push:", source)
        self.assertNotIn("\n  pull_request:", source)
        self.assertIn("permissions:\n  contents: read", source)
        self.assertIn("actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1", source)
        self.assertIn("actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97", source)
        self.assertIn("actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a", source)
        self.assertIn("apache-soak-${{ inputs.mode }}", source)
        self.assertIn("BLOCKED", source)
        self.assertIn("exit 77", source)
        self.assertIn("make build-apache", source)

    def test_makefile_exposes_static_and_manual_soak_targets(self) -> None:
        for target in (
            "check-apache-soak-wiring:",
            "apache-soak-memcheck:",
            "apache-soak-helgrind:",
            "apache-soak: apache-soak-memcheck apache-soak-helgrind",
        ):
            with self.subTest(target=target):
                self.assertIn(target, self.makefile)
        self.assertIn("tests.test_apache_soak_wiring", self.makefile)
        self.assertIn("tests.test_apache_soak_workload", self.makefile)
        self.assertIn("run-apache-soak.sh memcheck", self.makefile)
        self.assertIn("run-apache-soak.sh helgrind", self.makefile)
        self.assertNotIn("$(MAKE) apache-soak", self.makefile.split("lint:", 1)[1])


if __name__ == "__main__":
    unittest.main()
