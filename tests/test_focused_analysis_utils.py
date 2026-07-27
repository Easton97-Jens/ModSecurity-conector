from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CI_LIB = ROOT / "ci" / "lib"
if str(CI_LIB) not in sys.path:
    sys.path.insert(0, str(CI_LIB))

import focused_analysis_utils as UTILS
import report_path_safety


def load_report_module(relative_path: str, module_name: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


NOLOG = load_report_module(
    "ci/evidence/reports/generate-nolog-audit-evidence-analysis.py",
    "nolog_analysis_focused_utils_test",
)
RESPONSE_HEADER = load_report_module(
    "ci/evidence/reports/generate-response-header-hook-analysis.py",
    "response_header_analysis_focused_utils_test",
)


class FocusedAnalysisUtilsTest(unittest.TestCase):
    def setUp(self) -> None:
        self._safe_roots = set(report_path_safety.SAFE_ROOTS)
        report_path_safety.SAFE_ROOTS.clear()

    def tearDown(self) -> None:
        report_path_safety.SAFE_ROOTS.clear()
        report_path_safety.SAFE_ROOTS.update(self._safe_roots)

    def test_consumers_use_the_shared_identical_utility_block(self) -> None:
        for name in (
            "utc_now",
            "read_json",
            "write_json",
            "read_text",
            "as_list",
            "refresh_connector_queue_totals",
            "import_script",
            "sanitize_path",
            "action_parts",
        ):
            self.assertIs(getattr(NOLOG, name), getattr(UTILS, name))
            self.assertIs(getattr(RESPONSE_HEADER, name), getattr(UTILS, name))

    def test_utc_formatting_and_scalar_list_coercion_are_preserved(self) -> None:
        generated_at = UTILS.utc_now()
        parsed = datetime.fromisoformat(generated_at.replace("Z", "+00:00"))
        self.assertEqual(parsed.tzinfo, timezone.utc)
        self.assertEqual(parsed.microsecond, 0)
        self.assertEqual(UTILS.as_list(None), [])
        self.assertEqual(UTILS.as_list(""), [])
        self.assertEqual(UTILS.as_list(7), ["7"])
        self.assertEqual(UTILS.as_list(["kept", "", "  ", 3]), ["kept", "3"])

    def test_quoted_commas_and_nolog_value_selection_are_preserved(self) -> None:
        actions = UTILS.action_parts('id:123,msg:"comma, preserved",phase:2,logdata:\'also, preserved\'')

        self.assertEqual(
            actions,
            ["id:123", 'msg:"comma, preserved"', "phase:2", "logdata:'also, preserved'"],
        )
        self.assertEqual(NOLOG.action_value(actions, "PHASE"), "2")

    def test_queue_totals_keep_entry_failure_and_priority_values(self) -> None:
        data: dict[str, object] = {
            "entries": [
                {"runtime_status": "PASS", "priority": "P3"},
                {"runtime_status": "FAIL", "priority": "P0"},
                {"runtime_status": "WARN", "priority": None},
                "ignored",
            ]
        }

        UTILS.refresh_connector_queue_totals(data)

        self.assertEqual(data["totals"], {"entries": 3, "failures": 1, "priority": {"-": 1, "P0": 1}})

    def test_safe_in_root_json_and_text_wrappers_round_trip(self) -> None:
        with tempfile.TemporaryDirectory(prefix="focused-analysis-utils-") as temporary:
            safe_root = Path(temporary) / "safe"
            safe_root.mkdir()
            report_path_safety.add_safe_roots(safe_root)
            configured_roots = set(report_path_safety.SAFE_ROOTS)
            json_path = safe_root / "nested" / "evidence.json"
            text_path = safe_root / "nested" / "evidence.txt"

            UTILS.write_json(json_path, {"status": "PASS"})
            text_path.write_text("evidence\n", encoding="utf-8")

            self.assertEqual(UTILS.read_json(json_path), {"status": "PASS"})
            self.assertEqual(UTILS.read_text(text_path), "evidence\n")
            self.assertEqual(UTILS.sanitize_path(json_path, safe_root, safe_root / "framework"), "connector:nested/evidence.json")
            self.assertEqual(report_path_safety.SAFE_ROOTS, configured_roots)

    def test_outside_paths_are_rejected_and_redacted(self) -> None:
        with tempfile.TemporaryDirectory(prefix="focused-analysis-utils-") as temporary:
            temporary_root = Path(temporary)
            safe_root = temporary_root / "safe"
            safe_root.mkdir()
            outside_path = temporary_root / "outside" / "sensitive.json"
            outside_path.parent.mkdir()
            outside_path.write_text('{"private": true}\n', encoding="utf-8")
            report_path_safety.add_safe_roots(safe_root)

            self.assertIsNone(report_path_safety.safe_existing_file(outside_path))
            self.assertEqual(
                UTILS.sanitize_path(outside_path, safe_root, safe_root / "framework"),
                "<runtime-artifact>/sensitive.json",
            )
            with self.assertRaisesRegex(ValueError, "unsafe output path"):
                UTILS.write_json(outside_path, {"must": "not write"})

    def test_dynamic_module_loading_keeps_the_module_registration_contract(self) -> None:
        module_name = "focused_analysis_utils_dynamic_module"
        self.addCleanup(sys.modules.pop, module_name, None)
        with tempfile.TemporaryDirectory(prefix="focused-analysis-utils-") as temporary:
            script_path = Path(temporary) / "dynamic_module.py"
            script_path.write_text("VALUE = 41\n", encoding="utf-8")

            module = UTILS.import_script(script_path, module_name)

        self.assertEqual(module.VALUE, 41)
        self.assertIs(sys.modules[module_name], module)
