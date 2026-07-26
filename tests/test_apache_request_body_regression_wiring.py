#!/usr/bin/env python3
"""Guard the Parent-owned Apache request-body regression seam."""

from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "connectors" / "apache" / "harness" / "run_apache_smoke.sh"
HARNESS_MODULE = ROOT / "connectors" / "apache" / "harness" / "mod_phase4_terminal_rogue.c"
PRODUCT_FILTERS = ROOT / "connectors" / "apache" / "src" / "msc_filters.c"
RUNNER = ROOT / "ci" / "runtime" / "lifecycle" / "run-apache-request-body-regression.sh"
MAKEFILE = ROOT / "Makefile"

REQUEST_BODY_FLAGS = (
    "APACHE_REQUEST_BODY_REGRESSION_TEST",
    "APACHE_REQUEST_BODY_MODE",
    "APACHE_REQUEST_BODY_EXPECT_STATUS",
    "APACHE_REQUEST_BODY_LARGE_BYTES",
    "APACHE_REQUEST_BODY_REPEAT_COUNT",
    "APACHE_REQUEST_BODY_CHUNKED",
)


class ApacheRequestBodyRegressionWiringTest(unittest.TestCase):
    def setUp(self) -> None:
        self.runner = RUNNER.read_text(encoding="utf-8")
        self.harness = HARNESS.read_text(encoding="utf-8")
        self.harness_module = HARNESS_MODULE.read_text(encoding="utf-8")
        self.product_filters = PRODUCT_FILTERS.read_text(encoding="utf-8")
        self.makefile = MAKEFILE.read_text(encoding="utf-8")

    def test_runner_exposes_only_the_parent_native_request_body_modes(self) -> None:
        self.assertIn('case "$mode" in', self.runner)
        for mode in (
            "small-allow",
            "body-deny",
            "large-multibucket",
            "split-trigger-chunked",
            "non-consuming-handler",
            "empty-body",
            "keep-alive-repeat",
            "fail-closed-read-error",
        ):
            with self.subTest(mode=mode):
                self.assertIn(f"    {mode})", self.runner)
        self.assertNotIn("docker", self.runner.lower())
        self.assertNotIn("eval ", self.runner)

    def test_runner_uses_literal_status_and_body_shape_contracts(self) -> None:
        expected = {
            "small-allow": (200, 0, 1, 0),
            "body-deny": (403, 0, 1, 0),
            "large-multibucket": (200, 1048577, 1, 0),
            "split-trigger-chunked": (403, 64, 1, 1),
            "non-consuming-handler": (403, 64, 1, 0),
            "empty-body": (200, 0, 1, 0),
            "keep-alive-repeat": (200, 64, 8, 0),
            "fail-closed-read-error": (400, 64, 1, 0),
        }
        for mode, (status, large_bytes, repeat_count, chunked) in expected.items():
            with self.subTest(mode=mode):
                start = self.runner.index(f"    {mode})")
                end = self.runner.index("        ;;", start)
                body = self.runner[start:end]
                self.assertIn(f"expect_status={status}", body)
                self.assertIn(f"large_bytes={large_bytes}", body)
                self.assertIn(f"repeat_count={repeat_count}", body)
                self.assertIn(f"chunked={chunked}", body)

    def test_runner_requires_external_task_owned_runtime_inputs(self) -> None:
        for variable in (
            "BUILD_ROOT",
            "RUNTIME_ROOT",
            "LOG_DIR",
            "PORT",
            "APACHE_REQUEST_BODY_ROOT",
        ):
            self.assertIn(f': "${{{variable}:?{variable} is required}}"', self.runner)
        self.assertIn("prepare_external_root", self.runner)
        self.assertIn("prepare_run_child", self.runner)
        self.assertIn("reject_symlink_ancestors", self.runner)
        self.assertIn("must be absolute", self.runner)
        self.assertIn("must name a task-owned child directory", self.runner)
        self.assertIn("must be outside a source checkout", self.runner)
        self.assertIn("must be a child of APACHE_REQUEST_BODY_ROOT", self.runner)
        self.assertIn("escapes APACHE_REQUEST_BODY_ROOT after canonicalization", self.runner)
        self.assertIn("PORT must be a numeric TCP port", self.runner)
        self.assertIn("PORT must be between 1 and 65535", self.runner)

    def test_runner_generates_a_task_local_case_and_preamble(self) -> None:
        self.assertIn("REQUEST_BODY_CONF_ROOT=$RUNTIME_ROOT/conf", self.runner)
        self.assertIn("mkdir -p \"$REQUEST_BODY_CONF_ROOT\"", self.runner)
        self.assertIn("printf '%s\\n'", self.runner)
        self.assertIn('TEST_CASE="$REQUEST_BODY_CASE_FILE"', self.runner)
        self.assertIn(
            'MODSECURITY_RULE_PREAMBLE_FILE="$REQUEST_BODY_RULE_PREAMBLE_FILE"',
            self.runner,
        )
        self.assertIn('EXTRA_CASE_ROOTS="$REQUEST_BODY_CONF_ROOT"', self.runner)
        self.assertIn("NO_CRS_BASELINE=1", self.runner)
        self.assertIn("supported EXTRA_CASE_ROOTS boundary", self.runner)
        for marker in (
            "SecRequestBodyAccess On",
            "SecAuditLog \"@@AUDIT_LOG@@\"",
            "request-body-allow-marker",
            "request-body-block-marker",
            "SecAction",
            "id:2190500,phase:2,pass,log",
            "phase:2,deny,status:403",
            "id:2190501",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.runner)
        self.assertIn("request_path=/__request_body_consume", self.runner)
        self.assertIn("request_path=/__request_body_nonconsume", self.runner)
        self.assertIn('if [ "$mode" = non-consuming-handler ]; then', self.runner)
        self.assertIn("'  status: 200'", self.runner)
        self.assertIn("'  intervention: none'", self.runner)

    def test_runner_and_harness_share_the_exact_request_body_environment(self) -> None:
        self.assertIn("exec env", self.runner)
        self.assertIn('sh "$HARNESS"', self.runner)
        for flag in REQUEST_BODY_FLAGS:
            with self.subTest(flag=flag):
                self.assertIn(flag, self.runner)
                self.assertIn(flag, self.harness)
        self.assertIn("APACHE_REQUEST_BODY_REGRESSION_TEST=1", self.runner)
        self.assertIn('APACHE_REQUEST_BODY_MODE="$mode"', self.runner)
        self.assertIn('APACHE_REQUEST_BODY_EXPECT_STATUS="$expect_status"', self.runner)
        self.assertIn('APACHE_REQUEST_BODY_LARGE_BYTES="$large_bytes"', self.runner)
        self.assertIn('APACHE_REQUEST_BODY_REPEAT_COUNT="$repeat_count"', self.runner)
        self.assertIn('APACHE_REQUEST_BODY_CHUNKED="$chunked"', self.runner)

    def test_read_error_control_uses_a_dedicated_test_only_lower_filter(self) -> None:
        for marker in (
            "request-body-regression-read-error",
            "REQUEST_BODY_REGRESSION_READ_ERROR",
            "request_body_regression_read_error_filter",
            "request_body_regression_insert_filter",
            "AP_FTYPE_CONTENT_SET",
            "APR_HOOK_LAST",
            "APR_EGENERAL",
            "injected lower input read error",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.harness_module)
        self.assertIn('/__request_body_read_error', self.harness)
        self.assertIn("request_body_regression_path=/__request_body_read_error", self.harness)
        self.assertIn("Apache discard returned status=", self.harness)
        self.assertIn("unexpectedly completed Apache body discard", self.harness)
        self.assertNotIn(
            "assert_request_body_regression_audit_count 1\n            grep -F 'injected lower input read error'",
            self.harness,
        )

    def test_parent_eos_drain_architecture_remains_the_production_path(self) -> None:
        self.assertIn("request_body_processed", self.product_filters)
        self.assertIn("ap_get_brigade(f->next", self.product_filters)
        self.assertIn("apache_finish_unread_request_body", self.product_filters)
        self.assertNotIn("ap_get_client_block", self.product_filters)
        self.assertNotIn("ap_get_client_block", self.harness_module)
        self.assertIn("test-only lower input-chain failure", self.harness_module)

    def test_makefile_exposes_every_literal_runtime_mode_without_adding_it_to_lint(self) -> None:
        self.assertIn("check-apache-request-body-regression-wiring:", self.makefile)
        self.assertIn("tests.test_apache_request_body_regression_wiring", self.makefile)
        self.assertIn("apache-request-body-regression:", self.makefile)
        for mode in (
            "small-allow",
            "body-deny",
            "large-multibucket",
            "split-trigger-chunked",
            "non-consuming-handler",
            "empty-body",
            "keep-alive-repeat",
            "fail-closed-read-error",
        ):
            with self.subTest(mode=mode):
                self.assertIn(f"apache-request-body-{mode}:", self.makefile)
                self.assertIn(
                    f"run-apache-request-body-regression.sh {mode}", self.makefile
                )
        lint_body = self.makefile.split("lint:", 1)[1]
        self.assertIn("$(MAKE) check-apache-request-body-regression-wiring", lint_body)
        self.assertNotIn("$(MAKE) apache-request-body-regression", lint_body)


if __name__ == "__main__":
    unittest.main()
