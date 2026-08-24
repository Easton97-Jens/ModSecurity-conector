"""Focused contracts for the Framework-derived connector coverage summary."""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = ROOT / "ci/runtime/lifecycle/summarize-connector-mode-coverage.py"


def load_summary():
    spec = importlib.util.spec_from_file_location("connector_mode_coverage_summary", SUMMARY_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SUMMARY = load_summary()
PARENT_SHA = "1" * 40
FRAMEWORK_SHA = "2" * 40


def selection(case_id: str, *, category: str = "Framework group: headers", status: str = "SELECTED"):
    return {
        "case_id": case_id,
        "phase": 1,
        "group": "headers",
        "display_category": category,
        "display_name": f"Framework test {case_id}",
        "selection_status": status,
    }


def plan(*cases, connector="envoy", profile="no-crs-no-mrts"):
    return {
        "connector": connector,
        "profile": profile,
        "scenario_contract": "no_crs_baseline" if profile == "no-crs-no-mrts" else "not_applicable",
        "cases": list(cases),
    }


class ConnectorModeCoverageSummaryTest(unittest.TestCase):
    def test_exact_framework_heading_and_no_legacy_tables_or_crs_heading(self):
        rendered = SUMMARY.render_summary(plan(selection("case-1")), crs="no-crs", mrts="no-mrts")
        self.assertEqual(rendered.count("### Framework test scenario coverage"), 1)
        self.assertNotIn("Framework case counts by phase and area", rendered)
        self.assertNotIn("Framework cases by phase and area", rendered)
        self.assertNotIn("CRS security scenario coverage", rendered)

    def test_real_scenario_categories_and_total_equations(self):
        rows = [
            selection("passed", category="SQL Injection"),
            selection("failed", category="SQL Injection"),
            selection("unsupported", category="Headers", status="UNSUPPORTED"),
            selection("not-applicable", category="Headers", status="NOT_APPLICABLE"),
        ]
        evidence = {
            "passed": {"status": "PASS", "live_executed": True, "validation_status": "SUCCESS"},
            "failed": {"status": "FAIL", "live_executed": True, "validation_status": "SUCCESS"},
        }
        rendered = SUMMARY.render_summary(
            plan(*rows), evidence, evidence_validated=True,
            selection_outcome="success", execution_outcome="success",
            evidence_validation_outcome="success", crs="no-crs", mrts="no-mrts",
        )
        self.assertIn("| SQL Injection | 2 | 2 | 1 | 1 | 0 | 0 | 0 |", rendered)
        self.assertIn("| Headers | 2 | 0 | 0 | 0 | 1 | 1 | 0 |", rendered)
        self.assertIn("| **Total** | **4** | **2** | **1** | **1** | **1** | **1** | **0** |", rendered)
        self.assertIn("Selected = Executed + Unsupported + Not applicable + Not executed", rendered)
        self.assertIn("Executed = Passed + Failed + Cancelled", rendered)
        self.assertIn("`passed`", rendered)
        self.assertIn("`failed`", rendered)

    def test_run_and_pass_require_validated_live_evidence(self):
        p = plan(selection("one"))
        step_success = SUMMARY.render_summary(
            p, {"one": {"status": "PASS", "live_executed": True}},
            execution_outcome="success", evidence_validation_outcome="success",
            crs="no-crs", mrts="no-mrts",
        )
        self.assertIn("Framework test execution: `NOT RUN`", step_success)
        self.assertIn("| **Total** | **1** | **0** | **0** |", step_success)
        self.assertNotIn("| **Total** | **1** | **1** | **1** |", step_success)
        validated = SUMMARY.case_rows(
            p, {"one": {"status": "PASS", "live_executed": True, "validation_status": "SUCCESS"}},
            evidence_validated=True,
        )
        self.assertEqual(validated[0]["status"], "PASS")
        self.assertEqual(SUMMARY._row_execution(validated[0]), "RUN")
        skipped = SUMMARY.render_summary(
            p,
            {"one": {"status": "PASS", "live_executed": True, "validation_status": "SUCCESS"}},
            evidence_validated=True,
            selection_outcome="success",
            execution_outcome="skipped",
            evidence_validation_outcome="success",
            crs="no-crs",
            mrts="no-mrts",
        )
        self.assertIn("Framework test execution: `NOT RUN`", skipped)
        self.assertIn("`NOT RUN`<br>no validated live test result", skipped)
        self.assertNotIn("| `one` | `RUN`", skipped)
        not_live = SUMMARY.case_rows(
            p, {"one": {"status": "PASS", "live_executed": False}}, evidence_validated=True
        )
        self.assertEqual(not_live[0]["status"], "NOT_EXECUTED")

    def test_all_connector_profile_renderers_and_nginx_protection(self):
        for connector in SUMMARY.CONNECTORS:
            for profile in SUMMARY.PROFILES:
                with self.subTest(connector=connector, profile=profile):
                    rendered = SUMMARY.render_summary(
                        plan(selection("one"), connector=connector, profile=profile),
                        crs="with-crs" if profile.startswith("with") else "no-crs",
                        mrts="with-mrts" if profile.endswith("with-mrts") else "no-mrts",
                    )
                    self.assertIn("### Framework test scenario coverage", rendered)
                    self.assertNotIn("CRS security scenario coverage", rendered)
        routes = SUMMARY.route_inventory("nginx")
        self.assertTrue(all(row["state"] == "PROTECTED_SEPARATE" for row in routes))
        self.assertEqual(SUMMARY.route_state("envoy", "with-crs-with-mrts"), "EXPECTED_UNSUPPORTED")

    def test_display_index_is_commit_bound_and_rejects_duplicate_mappings(self):
        good = {"schema_version": 1, "framework_commit": FRAMEWORK_SHA, "tests": [
            {"framework_test_id": "fixture", "display_category": "SQL Injection", "display_name": "fixture"}
        ]}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "index.json"
            path.write_text(json.dumps(good), encoding="utf-8")
            self.assertEqual(SUMMARY._load_display_index(path, FRAMEWORK_SHA)["fixture"]["display_category"], "SQL Injection")
            with self.assertRaisesRegex(ValueError, "bound"):
                SUMMARY._load_display_index(path, PARENT_SHA)
            path.write_text(json.dumps({**good, "tests": good["tests"] + good["tests"]}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate"):
                SUMMARY._load_display_index(path, FRAMEWORK_SHA)
            with self.assertRaisesRegex(ValueError, "not valid JSON"):
                SUMMARY._json_object(b'{"schema_version":1,"schema_version":1}', "index")

    def test_case_plan_rejects_duplicate_and_evidence_rejects_unknown_or_missing_ids(self):
        with self.assertRaisesRegex(ValueError, "unique"):
            SUMMARY.case_rows(plan(selection("same"), selection("same")))
        p = plan(selection("expected"))
        with tempfile.TemporaryDirectory() as directory:
            evidence = Path(directory)
            result = {
                "connector": "envoy", "run_id": "run-1", "connector_commit": PARENT_SHA,
                "framework_commit": FRAMEWORK_SHA, "connector_commit_at_finalize": PARENT_SHA,
                "framework_commit_at_finalize": FRAMEWORK_SHA, "evidence_stage": "no_crs_baseline",
                "ruleset": "no-crs-baseline", "status": "PASS",
            }
            (evidence / "result.json").write_text(json.dumps(result), encoding="utf-8")
            record = {"connector": "envoy", "run_id": "run-1", "case_id": "unknown",
                      "phase": 1, "group": "headers", "status": "PASS", "live_executed": True}
            (evidence / "results.jsonl").write_text(json.dumps(record) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "outside"):
                SUMMARY._records_from_evidence(evidence, p, "envoy", run_id="run-1", parent_sha=PARENT_SHA, framework_sha=FRAMEWORK_SHA)
            record["case_id"] = "expected"
            (evidence / "results.jsonl").write_text(json.dumps(record) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "missing"):
                SUMMARY._records_from_evidence(evidence, plan(selection("expected"), selection("second")), "envoy", run_id="run-1", parent_sha=PARENT_SHA, framework_sha=FRAMEWORK_SHA)

    def test_no_crs_evidence_is_bound_to_exact_run_parent_and_framework(self):
        p = plan(selection("expected"))
        with tempfile.TemporaryDirectory() as directory:
            evidence = Path(directory)
            result = {"connector": "envoy", "run_id": "run-1", "connector_commit": PARENT_SHA,
                      "framework_commit": FRAMEWORK_SHA, "connector_commit_at_finalize": PARENT_SHA,
                      "framework_commit_at_finalize": FRAMEWORK_SHA, "evidence_stage": "no_crs_baseline",
                      "ruleset": "no-crs-baseline", "status": "PASS"}
            (evidence / "result.json").write_text(json.dumps(result), encoding="utf-8")
            record = {"connector": "envoy", "run_id": "run-1", "case_id": "expected", "phase": 1,
                      "group": "headers", "status": "PASS", "live_executed": True}
            (evidence / "results.jsonl").write_text(json.dumps(record) + "\n", encoding="utf-8")
            records = SUMMARY._records_from_evidence(evidence, p, "envoy", run_id="run-1", parent_sha=PARENT_SHA, framework_sha=FRAMEWORK_SHA)
            self.assertEqual(records["expected"]["validation_status"], "SUCCESS")
            for field, wrong in (("run_id", "run-2"), ("connector_commit", "3" * 40), ("framework_commit", "4" * 40)):
                broken = dict(result)
                broken[field] = wrong
                (evidence / "result.json").write_text(json.dumps(broken), encoding="utf-8")
                with self.assertRaises(ValueError):
                    SUMMARY._records_from_evidence(evidence, p, "envoy", run_id="run-1", parent_sha=PARENT_SHA, framework_sha=FRAMEWORK_SHA)

    def test_no_crs_success_requires_a_fresh_framework_validator_result(self):
        class RejectingFrameworkValidator:
            @staticmethod
            def validate_command(_args):
                return 1

        original = SUMMARY.load_framework_selector
        try:
            SUMMARY.load_framework_selector = lambda _root: RejectingFrameworkValidator()
            with self.assertRaisesRegex(ValueError, "Framework validation rejected"):
                SUMMARY._validate_no_crs_framework_contract(
                    Path("/framework"),
                    Path("/evidence"),
                    Path("/connector"),
                    Path("/capabilities.json"),
                    "envoy",
                    "run-1",
                )
        finally:
            SUMMARY.load_framework_selector = original

        class RaisingFrameworkValidator:
            @staticmethod
            def validate_command(_args):
                raise ValueError("/tmp/private")

        try:
            SUMMARY.load_framework_selector = lambda _root: RaisingFrameworkValidator()
            with self.assertRaisesRegex(ValueError, "Framework validation rejected") as raised:
                SUMMARY._validate_no_crs_framework_contract(
                    Path("/framework"),
                    Path("/evidence"),
                    Path("/connector"),
                    Path("/capabilities.json"),
                    "envoy",
                    "run-1",
                )
        finally:
            SUMMARY.load_framework_selector = original
        self.assertNotIn("/tmp/private", str(raised.exception))

        captured = {}

        class AcceptingFrameworkValidator:
            @staticmethod
            def validate_command(args):
                captured.update(vars(args))
                return 0

        try:
            SUMMARY.load_framework_selector = lambda _root: AcceptingFrameworkValidator()
            SUMMARY._validate_no_crs_framework_contract(
                Path("/framework"),
                Path("/evidence"),
                Path("/connector"),
                Path("/capabilities.json"),
                "envoy",
                "run-1",
            )
        finally:
            SUMMARY.load_framework_selector = original
        self.assertEqual(captured["connector"], "envoy")
        self.assertEqual(captured["run_id"], "run-1")
        self.assertEqual(captured["check"], "all")

    def test_summary_escapes_markdown_html_and_does_not_leak_payload_or_paths(self):
        hostile = selection("safe-id", category="<script>alert(1)</script>|payload `/tmp/private`")
        rendered = SUMMARY.render_summary(plan(hostile), crs="no-crs", mrts="no-mrts")
        self.assertNotIn("<script>", rendered)
        self.assertNotIn("/tmp/private", rendered)
        self.assertIn("&lt;script&gt;", rendered)
        self.assertNotIn("payload", rendered)


if __name__ == "__main__":
    unittest.main()
