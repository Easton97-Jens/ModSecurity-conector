from __future__ import annotations

import importlib
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "modules" / "ModSecurity-test-Framework" / "tests" / "runners"
_MISSING_MODULE = object()


def load_framework_runner_core():
    """Load the Framework runner without retaining its generic CI helper.

    Parent and Framework both provide ``generated_report_utils``.  Discovery
    must bind the Framework implementation for this test, then restore the
    surrounding interpreter state so later Parent tests resolve their own
    helper.
    """

    previous_path = list(sys.path)
    previous_runner_core = sys.modules.pop("runner_core", _MISSING_MODULE)
    previous_generated_report_utils = sys.modules.pop(
        "generated_report_utils", _MISSING_MODULE
    )
    try:
        sys.path.insert(0, str(RUNNERS))
        module = importlib.import_module("runner_core")
    finally:
        sys.path[:] = previous_path
        sys.modules.pop("runner_core", None)
        if previous_runner_core is not _MISSING_MODULE:
            sys.modules["runner_core"] = previous_runner_core
        sys.modules.pop("generated_report_utils", None)
        if previous_generated_report_utils is not _MISSING_MODULE:
            sys.modules["generated_report_utils"] = previous_generated_report_utils
    return module


runner_core = load_framework_runner_core()
load_case = runner_core.load_case
write_shell_env = runner_core.write_shell_env


FIXTURES = ROOT / "modules" / "ModSecurity-test-Framework" / "tests" / "cases" / "connector-specific" / "nginx"


class NginxPhase4RunnerWiringTest(unittest.TestCase):
    def load_fixture(self, filename: str):
        return load_case(FIXTURES / filename)

    def test_safe_fixture_records_a_real_late_log_only_outcome(self) -> None:
        case = self.load_fixture("nginx_phase4_deny_after_commit_log_only.yaml")
        expect = case["expect"]
        phase4_log = expect["phase4_log"]

        self.assertEqual(case["name"], "phase4_deny_after_commit_log_only")
        self.assertTrue(case["no_crs_baseline"])
        self.assertEqual(case["nginx"]["phase4_mode"], "safe")
        self.assertEqual(expect["status"], 200)
        self.assertEqual(expect["transport"], "http_status")
        self.assertIn("event", case["expected_event_fields"])
        self.assertIn("message_id", case["expected_event_fields"])
        self.assertIn('"message_id":"MSCONN_EVENT_PHASE4_LATE_INTERVENTION"', phase4_log["contains"])
        self.assertIn('"actual_action":"log_only"', phase4_log["contains"])
        self.assertIn('"visible_http_status":200', phase4_log["contains"])
        self.assertIn('"connection_aborted":false', phase4_log["contains"])
        self.assertIn("no-crs-response-body-marker", phase4_log["not_contains"])
        self.assertIn('"intervention_log":', phase4_log["not_contains"])

    def test_strict_fixture_asserts_abort_transport_not_a_rewritten_403(self) -> None:
        case = self.load_fixture("nginx_phase4_deny_after_commit_abort.yaml")
        expect = case["expect"]
        phase4_log = expect["phase4_log"]

        self.assertEqual(case["name"], "phase4_deny_after_commit_abort")
        self.assertTrue(case["no_crs_baseline"])
        self.assertEqual(case["nginx"]["phase4_mode"], "strict")
        self.assertEqual(expect["status"], 200)
        self.assertEqual(expect["transport"], "connection_aborted")
        self.assertIn("event", case["expected_event_fields"])
        self.assertIn("message_id", case["expected_event_fields"])
        self.assertIn('"message_id":"MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200"', phase4_log["contains"])
        self.assertIn('"actual_action":"abort_connection"', phase4_log["contains"])
        self.assertIn('"visible_http_status":200', phase4_log["contains"])
        self.assertIn('"connection_aborted":true', phase4_log["contains"])
        self.assertIn('"transport_result":"connection_aborted"', phase4_log["contains"])
        self.assertIn("no-crs-response-body-marker", phase4_log["not_contains"])

    def test_generic_case_environment_carries_only_the_reviewed_mode(self) -> None:
        case = self.load_fixture("nginx_phase4_deny_after_commit_log_only.yaml")
        with tempfile.TemporaryDirectory() as temporary:
            env_file = Path(temporary) / "case.env"
            write_shell_env(case, env_file, output_root=temporary)
            content = env_file.read_text(encoding="utf-8")
        self.assertIn("NGINX_PHASE4_MODE=safe", content)
        self.assertNotIn("actual_action", content)
        self.assertNotIn("visible_http_status", content)

    def test_runner_maps_only_selected_canonical_late_paths(self) -> None:
        harness = (ROOT / "connectors" / "nginx" / "harness" / "run_nginx_smoke.sh").read_text(encoding="utf-8")
        template = (ROOT / "connectors" / "nginx" / "harness" / "nginx_smoke.conf").read_text(encoding="utf-8")
        stage = (ROOT / "ci" / "runtime" / "lifecycle" / "run-connector-stage.sh").read_text(encoding="utf-8")
        baseline = (ROOT / "ci" / "runtime" / "lifecycle" / "run-no-crs-baseline.sh").read_text(encoding="utf-8")

        self.assertIn("NO_CRS_SELECTED_CASE_IDS", baseline)
        self.assertIn("NO_CRS_SELECTED_CASE_IDS", stage)
        self.assertIn("phase4_deny_after_commit_log_only", harness)
        self.assertIn("phase4_deny_after_commit_abort", harness)
        self.assertNotIn("phase4_deny_before_commit)\n                append_smoke_case", harness)
        self.assertIn("@@NGINX_PHASE4_MODE_DIRECTIVE@@", template)
        self.assertIn("@@NGINX_TRANSACTION_ID_DIRECTIVE@@", template)
        self.assertIn(
            "modsecurity_transaction_id nginx-${case_name}-\\$connection-\\$connection_requests;",
            harness,
        )

    def test_precommit_phase4_deny_is_not_declared_for_the_body_filter(self) -> None:
        import json

        manifest = json.loads(
            (ROOT / "connectors" / "nginx" / "capabilities.json").read_text(encoding="utf-8")
        )
        declaration = manifest["capabilities"]["phase4_pre_commit_deny"]
        self.assertEqual(declaration["state"], "not_implemented")
        self.assertIn("body filter", declaration["reason"])

    def test_apache_declares_a_gate_backed_precommit_phase4_deny(self) -> None:
        import json

        manifest = json.loads(
            (ROOT / "connectors" / "apache" / "capabilities.json").read_text(encoding="utf-8")
        )
        declaration = manifest["capabilities"]["phase4_pre_commit_deny"]
        self.assertEqual(declaration["state"], "implemented_not_asserted")
        self.assertIn("retains original response bytes", declaration["reason"])
        self.assertIn("terminal error", declaration["reason"])


if __name__ == "__main__":
    unittest.main()
