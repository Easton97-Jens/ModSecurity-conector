"""Focused contracts for the workflow-style connector coverage summary."""
from __future__ import annotations

import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = ROOT / "ci/runtime/lifecycle/summarize-connector-mode-coverage.py"


def load_summary():
    spec = importlib.util.spec_from_file_location("connector_mode_coverage_summary", SUMMARY_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load coverage summary")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SUMMARY = load_summary()


def selected(case_id: str, phase: int, area: str = "headers", state: str = "SELECTED") -> dict[str, object]:
    return {
        "case_id": case_id,
        "phase": phase,
        "group": area,
        "selection_status": state,
        "selection_reason": "fixture selection reason",
    }


def canonical_result(connector: str) -> dict[str, object]:
    return {
        "connector": connector,
        "evidence_stage": "no_crs_baseline",
        "ruleset": "no-crs-baseline",
    }


class ConnectorModeCoverageSummaryTest(unittest.TestCase):
    def test_166_like_plan_is_grouped_by_phase_and_area(self) -> None:
        plan = {"connector": "apache", "cases": [selected(f"case-{i:03d}", i % 6, f"area-{i % 4}") for i in range(166)]}
        rendered = SUMMARY.render_summary(plan)
        self.assertIn("Framework cases by phase and area", rendered)
        self.assertIn("complete No-CRS catalogue is an inventory", rendered)
        self.assertIn("| 5 | area-1 | case-005 | NOT_EXECUTED | no validated result |", rendered)
        self.assertEqual(rendered.count("| NOT_EXECUTED |"), 167)

    def test_phase_zero_is_rendered_as_phase_zero(self) -> None:
        plan = {"connector": "apache", "cases": [selected("phase-zero", 0)]}
        rows = SUMMARY.case_rows(plan)
        self.assertEqual(rows[0]["phase"], "0")
        self.assertIn("| 0 | headers | phase-zero | NOT_EXECUTED |", SUMMARY.render_summary(plan))

    def test_current_framework_catalog_has_a_terminal_row_for_every_case_and_connector(self) -> None:
        framework_root = Path(os.environ.get(
            "FRAMEWORK_ROOT", ROOT / "modules" / "ModSecurity-test-Framework"
        ))
        if not (framework_root / SUMMARY.FRAMEWORK_SELECTOR).is_file():
            self.skipTest("the current Framework checkout is unavailable")
        selector = SUMMARY.load_framework_selector(framework_root)
        catalog = selector.load_catalog()
        catalog_cases = catalog.get("cases")
        self.assertIsInstance(catalog_cases, list)
        expected_case_ids = {str(case["case_id"]) for case in catalog_cases}
        self.assertEqual(len(expected_case_ids), len(catalog_cases))
        self.assertTrue(expected_case_ids)
        for connector in SUMMARY.CONNECTORS:
            with self.subTest(connector=connector):
                plan = SUMMARY.select_framework_cases(
                    framework_root, connector,
                    ROOT / "connectors" / connector / "capabilities.json",
                )
                rows = SUMMARY.case_rows(plan)
                self.assertEqual({row["case_id"] for row in rows}, expected_case_ids)
                self.assertEqual(len(rows), len(expected_case_ids))
                self.assertTrue(all(row["phase"] != "unknown" for row in rows))
                self.assertTrue(all(row["area"] != "ungrouped" for row in rows))
                self.assertTrue(all(row["status"] in SUMMARY.CASE_STATUSES for row in rows))

    def test_unvalidated_fabricated_pass_is_demoted(self) -> None:
        plan = {"connector": "envoy", "cases": [selected("one", 1)]}
        evidence = {"one": {"status": "PASS", "live_executed": False}}
        self.assertEqual(SUMMARY.case_rows(plan, evidence)[0]["status"], "NOT_EXECUTED")

    def test_validated_live_pass_is_retained_without_invented_validated_field(self) -> None:
        plan = {"connector": "apache", "cases": [selected("one", 2)]}
        evidence = {"one": {"status": "PASS", "live_executed": True}}
        self.assertEqual(SUMMARY.case_rows(plan, evidence)[0]["status"], "PASS")

    def test_unsupported_selection_is_retained(self) -> None:
        plan = {"connector": "traefik", "cases": [selected("one", 3, state="UNSUPPORTED")]}
        self.assertEqual(SUMMARY.case_rows(plan)[0]["status"], "UNSUPPORTED")

    def test_route_inventory_keeps_runtime_and_protected_paths_distinct(self) -> None:
        states = {(row["connector"], row["profile"]): row["state"] for row in SUMMARY.route_inventory()}
        self.assertEqual(states[("envoy", "with-crs-no-mrts")], "RUNTIME_ROUTE")
        self.assertEqual(states[("nginx", "no-crs-no-mrts")], "PROTECTED_SEPARATE")

    def test_evidence_requires_unique_bound_case_records(self) -> None:
        plan = {"connector": "apache", "cases": [selected("fixture", 1, "area")]}
        with tempfile.TemporaryDirectory(prefix="connector-summary-evidence-") as temporary:
            evidence = Path(temporary)
            (evidence / "result.json").write_text(json.dumps(canonical_result("apache")), encoding="utf-8")
            record = {"connector": "apache", "case_id": "fixture", "phase": 1, "group": "area", "status": "PASS", "live_executed": True}
            (evidence / "results.jsonl").write_text(json.dumps(record) + "\n" + json.dumps(record) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate case_id"):
                SUMMARY._records_from_evidence(evidence, plan, "apache")

    def test_summary_records_the_validation_outcome(self) -> None:
        plan = {"connector": "apache", "cases": [selected("one", 1)]}
        rendered = SUMMARY.render_summary(plan, evidence_validation_outcome="failure")
        self.assertIn("Canonical evidence validation: `failure`.", rendered)

    def test_unvalidated_terminal_signal_is_bounded_and_non_promoting(self) -> None:
        plan = {"connector": "apache", "cases": [selected("fixture", 1, "area")]}
        with tempfile.TemporaryDirectory(prefix="connector-summary-unvalidated-") as temporary:
            evidence = Path(temporary)
            (evidence / "result.json").write_text(
                json.dumps({**canonical_result("apache"), "status": "FAIL"}),
                encoding="utf-8",
            )
            (evidence / "results.jsonl").write_text(
                json.dumps({
                    "connector": "apache",
                    "case_id": "fixture",
                    "phase": 1,
                    "group": "area",
                    "status": "FAIL",
                    "live_executed": True,
                    "reason": "untrusted raw reason must not enter the summary",
                }) + "\n",
                encoding="utf-8",
            )
            signal = SUMMARY._unvalidated_terminal_signal(evidence, plan, "apache")

        self.assertEqual(signal, {
            "status": "FAIL",
            "case_id": "fixture",
            "case_status": "FAIL",
            "phase": "1",
            "area": "area",
        })
        rendered = SUMMARY.render_summary(
            plan,
            evidence_validation_outcome="skipped",
            terminal_signal=signal,
        )
        self.assertIn("Unvalidated terminal signal", rendered)
        self.assertIn("Observed terminal status (not promoted): `FAIL`.", rendered)
        self.assertIn("`fixture` — `FAIL`; phase `1`; area `area`.", rendered)
        self.assertIn("| 1 | area | fixture | NOT_EXECUTED |", rendered)
        self.assertNotIn("untrusted raw reason", rendered)

    def test_unvalidated_terminal_signal_tolerates_non_utf8_jsonl(self) -> None:
        plan = {"connector": "apache", "cases": [selected("fixture", 1, "area")]}
        with tempfile.TemporaryDirectory(prefix="connector-summary-non-utf8-") as temporary:
            evidence = Path(temporary)
            (evidence / "result.json").write_text(
                json.dumps({**canonical_result("apache"), "status": "BLOCKED"}),
                encoding="utf-8",
            )
            (evidence / "results.jsonl").write_bytes(b"\xff\xfe\n")
            signal = SUMMARY._unvalidated_terminal_signal(evidence, plan, "apache")

        self.assertEqual(signal, {"status": "BLOCKED"})

    def test_unvalidated_terminal_signal_rejects_a_symlinked_evidence_directory(self) -> None:
        plan = {"connector": "apache", "cases": [selected("fixture", 1, "area")]}
        with tempfile.TemporaryDirectory(prefix="connector-summary-symlink-") as temporary:
            root = Path(temporary)
            evidence = root / "evidence"
            evidence.mkdir()
            (evidence / "result.json").write_text(
                json.dumps({**canonical_result("apache"), "status": "FAIL"}),
                encoding="utf-8",
            )
            evidence_link = root / "evidence-link"
            evidence_link.symlink_to(evidence, target_is_directory=True)
            signal = SUMMARY._unvalidated_terminal_signal(evidence_link, plan, "apache")

        self.assertIsNone(signal)

    def test_fake_selector_and_capability_fixture_are_consumed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="connector-summary-framework-") as temporary:
            root = Path(temporary)
            (root / "selector.py").write_text(
                "def load_capability_manifest(path, connector):\n    return {'connector': connector}\n"
                "def load_catalog():\n    return {'cases': []}\n"
                "def select_cases(connector, manifest, catalog, evidence_stage):\n"
                "    return {'connector': connector, 'cases': [{'case_id': 'fixture', 'phase': 1, 'group': 'fixture-area', 'selection_status': 'SELECTED'}]}\n",
                encoding="utf-8",
            )
            capabilities = root / "capabilities.json"
            capabilities.write_text(json.dumps({"connector": "apache"}), encoding="utf-8")
            with mock.patch.object(SUMMARY, "FRAMEWORK_SELECTOR", Path("selector.py")):
                plan = SUMMARY.select_framework_cases(root, "apache", capabilities)
            self.assertEqual(plan["cases"][0]["case_id"], "fixture")

    def test_workflow_main_reads_jsonl_only_after_success_and_writes_secure_summary(self) -> None:
        with tempfile.TemporaryDirectory(prefix="connector-summary-workflow-") as temporary:
            root = Path(temporary)
            framework = root / "framework"
            connector_root = root / "connector"
            (framework / "ci/checks/catalog").mkdir(parents=True)
            (connector_root / "connectors/apache").mkdir(parents=True)
            (framework / "ci/checks/catalog/selector.py").write_text(
                "def load_capability_manifest(path, connector):\n    return {'connector': connector}\n"
                "def load_catalog():\n    return {'cases': []}\n"
                "def select_cases(connector, manifest, catalog, evidence_stage):\n"
                "    return {'connector': connector, 'cases': [{'case_id': 'fixture', 'phase': 1, 'group': 'area', 'selection_status': 'SELECTED'}]}\n",
                encoding="utf-8",
            )
            (connector_root / "connectors/apache/capabilities.json").write_text("{}", encoding="utf-8")
            evidence = root / "evidence"
            evidence.mkdir()
            (evidence / "result.json").write_text(json.dumps(canonical_result("apache")), encoding="utf-8")
            (evidence / "results.jsonl").write_text(json.dumps({"connector": "apache", "case_id": "fixture", "phase": 1, "group": "area", "status": "PASS", "live_executed": True}) + "\n", encoding="utf-8")
            runner_temp = root / "runner-temp"
            summary_dir = runner_temp / "_runner_file_commands"
            summary_dir.mkdir(parents=True)
            summary = summary_dir / "step_summary_fixture"
            summary.touch()
            environment = {"RUNNER_TEMP": str(runner_temp), "GITHUB_STEP_SUMMARY": str(summary)}
            with mock.patch.object(SUMMARY, "FRAMEWORK_SELECTOR", Path("ci/checks/catalog/selector.py")), mock.patch.dict(SUMMARY.os.environ, environment, clear=True):
                result = SUMMARY.main(["--connector", "apache", "--crs", "no-crs", "--mrts", "no-mrts", "--coverage-kind", "runtime", "--connector-root", str(connector_root), "--framework-root", str(framework), "--evidence-dir", str(evidence), "--evidence-validation-outcome", "success"])
            self.assertEqual(result, 0)
            self.assertIn("| area | fixture | PASS | validated results.jsonl |", summary.read_text(encoding="utf-8"))

    def test_mismatched_and_unsafe_inputs_are_rejected(self) -> None:
        unsafe_framework_root = Path(tempfile.gettempdir())
        with self.assertRaisesRegex(ValueError, "outside"):
            SUMMARY.load_framework_selector(unsafe_framework_root)
        plan = {"connector": "apache", "cases": [selected("one", 1)]}
        with self.assertRaisesRegex(ValueError, "invalid case status"):
            SUMMARY.case_rows(plan, {"one": {"status": "MAYBE"}})


if __name__ == "__main__":
    unittest.main()
