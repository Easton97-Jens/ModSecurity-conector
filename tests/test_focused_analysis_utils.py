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
import generated_report_utils
import report_path_safety


def load_report_module(relative_path: str, module_name: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


REPORTS_DIR = "ci/evidence/reports"
REPORT_MODULE_PATHS = {
    "nolog": f"{REPORTS_DIR}/generate-nolog-audit-evidence-analysis.py",
    "response_header": f"{REPORTS_DIR}/generate-response-header-hook-analysis.py",
    "body_processor": f"{REPORTS_DIR}/generate-body-processor-analysis.py",
    "rule_chain": f"{REPORTS_DIR}/generate-rule-chain-semantics-analysis.py",
    "no_mrts_nomatch": f"{REPORTS_DIR}/generate-no-mrts-intervention-nomatch-analysis.py",
    "intervention_blocking": f"{REPORTS_DIR}/generate-intervention-blocking-analysis.py",
    "phase4_hard_abort": f"{REPORTS_DIR}/generate-phase4-hard-abort-capability.py",
    "remaining_failure": f"{REPORTS_DIR}/generate-remaining-failure-analysis.py",
    "final_consistency": f"{REPORTS_DIR}/generate-final-consistency-audit.py",
}
REPORT_MODULES = {
    name: load_report_module(path, f"{name}_focused_utils_test")
    for name, path in REPORT_MODULE_PATHS.items()
}
NOLOG = REPORT_MODULES["nolog"]
RESPONSE_HEADER = REPORT_MODULES["response_header"]
BODY_PROCESSOR = REPORT_MODULES["body_processor"]
RULE_CHAIN = REPORT_MODULES["rule_chain"]
NO_MRTS_NOMATCH = REPORT_MODULES["no_mrts_nomatch"]
INTERVENTION_BLOCKING = REPORT_MODULES["intervention_blocking"]
PHASE4_HARD_ABORT = REPORT_MODULES["phase4_hard_abort"]
REMAINING_FAILURE = REPORT_MODULES["remaining_failure"]
FINAL_CONSISTENCY = REPORT_MODULES["final_consistency"]

FILE_UTILITIES = ("utc_now", "read_json", "write_json", "read_text")
LIST_UTILITIES = (*FILE_UTILITIES, "as_list")
ACTION_UTILITIES = (*LIST_UTILITIES, "action_parts")
BODY_PROCESSOR_UTILITIES = (*ACTION_UTILITIES, "import_script")
FOCUSED_GENERATOR_UTILITIES = (
    *BODY_PROCESSOR_UTILITIES,
    "refresh_connector_queue_totals",
    "sanitize_path",
)
CASE_PATH_UTILITIES = (*FOCUSED_GENERATOR_UTILITIES, "find_framework_case_path")
SECTION_UPSERT_UTILITIES = (*FILE_UTILITIES, "upsert_marked_section")


class FocusedAnalysisUtilsTest(unittest.TestCase):
    def setUp(self) -> None:
        self._safe_roots = set(report_path_safety.SAFE_ROOTS)
        report_path_safety.SAFE_ROOTS.clear()

    def tearDown(self) -> None:
        report_path_safety.SAFE_ROOTS.clear()
        report_path_safety.SAFE_ROOTS.update(self._safe_roots)

    def test_consumers_use_shared_safe_primitives(self) -> None:
        consumer_bindings = {
            NOLOG: (*CASE_PATH_UTILITIES, "upsert_marked_section"),
            RESPONSE_HEADER: (*CASE_PATH_UTILITIES, "upsert_marked_section"),
            BODY_PROCESSOR: BODY_PROCESSOR_UTILITIES,
            RULE_CHAIN: (*ACTION_UTILITIES, "upsert_marked_section"),
            NO_MRTS_NOMATCH: (*LIST_UTILITIES, "upsert_marked_section"),
            INTERVENTION_BLOCKING: ACTION_UTILITIES,
            PHASE4_HARD_ABORT: SECTION_UPSERT_UTILITIES,
            REMAINING_FAILURE: ("utc_now", "read_json", "read_text", "upsert_marked_section"),
            FINAL_CONSISTENCY: ("utc_now", "read_json", "write_json"),
        }
        for consumer, names in consumer_bindings.items():
            for name in names:
                self.assertIs(getattr(consumer, name), getattr(UTILS, name))
        self.assertIs(FINAL_CONSISTENCY.listify, UTILS.as_list)

    def test_utc_formatting_and_scalar_list_coercion_are_preserved(self) -> None:
        generated_at = UTILS.utc_now()
        parsed = datetime.fromisoformat(generated_at.replace("Z", "+00:00"))
        self.assertEqual(parsed.tzinfo, timezone.utc)
        self.assertEqual(parsed.microsecond, 0)
        self.assertIs(UTILS.utc_now, generated_report_utils.utc_now)
        self.assertIs(UTILS.read_json, report_path_safety.read_json_file)
        self.assertIs(UTILS.read_text, report_path_safety.read_text_file)
        self.assertIs(UTILS.write_json, report_path_safety.write_json_file)
        self.assertEqual(UTILS.as_list(None), [])
        self.assertEqual(UTILS.as_list(""), [])
        self.assertEqual(UTILS.as_list(7), ["7"])
        self.assertEqual(UTILS.as_list("  "), ["  "])
        self.assertEqual(UTILS.as_list(["kept", "", "  ", 3, None]), ["kept", "3", "None"])

    def test_find_framework_case_path_rejects_unsafe_names_and_keeps_safe_cases(self) -> None:
        with tempfile.TemporaryDirectory(prefix="focused-analysis-utils-") as temporary:
            framework_root = Path(temporary) / "framework"
            case_path = framework_root / "tests" / "cases" / "safe-case.yaml"
            upstream_path = framework_root / "tests" / "upstream" / "upstream-case.yaml"
            case_path.parent.mkdir(parents=True)
            upstream_path.parent.mkdir(parents=True)
            case_path.write_text("name: safe-case\n", encoding="utf-8")
            upstream_path.write_text("name: upstream-case\n", encoding="utf-8")
            report_path_safety.add_safe_roots(framework_root)

            self.assertEqual(UTILS.find_framework_case_path(framework_root, "safe-case"), case_path.resolve())
            self.assertEqual(UTILS.find_framework_case_path(framework_root, "upstream-case"), upstream_path.resolve())
            for unsafe_name in (None, "", "../safe-case", "nested/safe-case", r"nested\\safe-case"):
                with self.subTest(case_id=unsafe_name):
                    self.assertIsNone(UTILS.find_framework_case_path(framework_root, unsafe_name))

    def test_upsert_marked_section_preserves_replace_anchor_and_append_layout(self) -> None:
        start = "<!-- report:start -->"
        end = "<!-- report:end -->"
        section = "## Report\n- refreshed"

        self.assertEqual(
            UTILS.upsert_marked_section(
                "before\n\n<!-- report:start -->\nold\n<!-- report:end -->\n\nafter\n",
                start=start,
                end=end,
                section=section,
                insert_before="## Reports And Logs",
            ),
            "before\n\n<!-- report:start -->\n## Report\n- refreshed\n<!-- report:end -->\n\nafter\n",
        )
        self.assertEqual(
            UTILS.upsert_marked_section(
                "before\n\n## Reports And Logs\nafter\n",
                start=start,
                end=end,
                section=section,
                insert_before="## Reports And Logs",
            ),
            "before\n\n<!-- report:start -->\n## Report\n- refreshed\n<!-- report:end -->\n\n## Reports And Logs\nafter\n",
        )
        self.assertEqual(
            UTILS.upsert_marked_section(
                "before\n\n<!-- next:start -->\nafter\n",
                start=start,
                end=end,
                section=section,
                insert_before="<!-- next:start -->",
            ),
            "before\n\n<!-- report:start -->\n## Report\n- refreshed\n<!-- report:end -->\n\n<!-- next:start -->\nafter\n",
        )
        self.assertEqual(
            UTILS.upsert_marked_section("before\n", start=start, end=end, section=section),
            "before\n\n<!-- report:start -->\n## Report\n- refreshed\n<!-- report:end -->\n",
        )

    def test_quoted_commas_and_nolog_value_selection_are_preserved(self) -> None:
        actions = UTILS.action_parts('id:123,msg:"comma, preserved",phase:2,logdata:\'also, preserved\'')

        self.assertEqual(
            actions,
            ["id:123", 'msg:"comma, preserved"', "phase:2", "logdata:'also, preserved'"],
        )
        self.assertEqual(NOLOG.action_value(actions, "PHASE"), "2")

    def test_action_parts_preserves_empty_and_unterminated_quote_behavior(self) -> None:
        cases = {
            "": [],
            "id:1,,phase:2": ["id:1", "phase:2"],
            "id:1,msg:'unterminated, quote": ["id:1", "msg:'unterminated, quote"],
            "id:1,msg:'mixed \" quote, kept',phase:2": ["id:1", "msg:'mixed \" quote, kept'", "phase:2"],
            'id:1,msg:"mixed \' quote, kept",phase:2': ["id:1", 'msg:"mixed \' quote, kept"', "phase:2"],
            "id:1, msg:plain , phase:2 ,": ["id:1", "msg:plain", "phase:2"],
        }
        for action_text, expected in cases.items():
            self.assertEqual(UTILS.action_parts(action_text), expected)

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
