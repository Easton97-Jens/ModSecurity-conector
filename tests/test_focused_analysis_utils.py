from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import tempfile
import textwrap
import unittest
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


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
REPORT_LOG_UTILITIES = (*ACTION_UTILITIES, "action_value", "log_paths")
BODY_PROCESSOR_UTILITIES = (*REPORT_LOG_UTILITIES, "import_script")
FOCUSED_GENERATOR_UTILITIES = (
    *ACTION_UTILITIES,
    "import_script",
    "refresh_connector_queue_totals",
    "sanitize_path",
)
CASE_PATH_UTILITIES = (*FOCUSED_GENERATOR_UTILITIES, "find_framework_case_path")
SECTION_UPSERT_UTILITIES = (*FILE_UTILITIES, "upsert_marked_section")
NOLOG_UTILITIES = tuple(name for name in CASE_PATH_UTILITIES if name != "import_script")
REPORT_LIFECYCLE_UTILITIES = (
    "render_connector_work_queue_markdown",
    "regenerate_phase_work_queue",
    "write_generated_report_pair",
)
GENERATED_AT = "2026-07-29T00:00:00Z"


class FocusedAnalysisUtilsTest(unittest.TestCase):
    def setUp(self) -> None:
        self._safe_roots = set(report_path_safety.SAFE_ROOTS)
        report_path_safety.SAFE_ROOTS.clear()

    def tearDown(self) -> None:
        report_path_safety.SAFE_ROOTS.clear()
        report_path_safety.SAFE_ROOTS.update(self._safe_roots)

    def test_consumers_use_shared_safe_primitives(self) -> None:
        consumer_bindings = {
            NOLOG: (*NOLOG_UTILITIES, "action_value", "upsert_marked_section", *REPORT_LIFECYCLE_UTILITIES),
            RESPONSE_HEADER: (*CASE_PATH_UTILITIES, "upsert_marked_section", *REPORT_LIFECYCLE_UTILITIES),
            BODY_PROCESSOR: BODY_PROCESSOR_UTILITIES,
            RULE_CHAIN: (*REPORT_LOG_UTILITIES, "upsert_marked_section"),
            NO_MRTS_NOMATCH: (*LIST_UTILITIES, "upsert_marked_section"),
            INTERVENTION_BLOCKING: REPORT_LOG_UTILITIES,
            PHASE4_HARD_ABORT: SECTION_UPSERT_UTILITIES,
            REMAINING_FAILURE: ("utc_now", "read_json", "read_text", "upsert_marked_section"),
            FINAL_CONSISTENCY: ("utc_now", "read_json", "write_json"),
        }
        for consumer, names in consumer_bindings.items():
            for name in names:
                self.assertIs(getattr(consumer, name), getattr(UTILS, name))
        self.assertIs(FINAL_CONSISTENCY.listify, UTILS.as_list)

    def test_render_connector_work_queue_markdown_uses_fixed_registered_output(self) -> None:
        with tempfile.TemporaryDirectory(prefix="focused-analysis-utils-") as temporary:
            connector_root = Path(temporary) / "connector"
            framework_root = Path(temporary) / "framework"
            report_dir = connector_root / "reports/testing/generated"
            script_path = framework_root / "ci/reporting/generate-connector-work-queue.py"
            script_path.parent.mkdir(parents=True)
            connector_root.mkdir()
            report_dir.mkdir(parents=True)
            script_path.write_text(
                textwrap.dedent(
                    """
                    def render_markdown(entries, source_counts, runtime_source_counts, generated_at):
                        return f"# Queue\\n{len(entries)}:{generated_at}:{source_counts['full']}:{runtime_source_counts['runtime']}"
                    """
                ).lstrip(),
                encoding="utf-8",
            )
            report_path_safety.add_safe_roots(connector_root, framework_root, report_dir)
            report_path_safety.add_report_roots(report_dir)

            UTILS.render_connector_work_queue_markdown(
                report_dir,
                {
                    "entries": [{"case_id": "one"}],
                    "source_counts": {"full": 1},
                    "runtime_source_counts": {"runtime": 2},
                    "generated_at": GENERATED_AT,
                },
                framework_root,
            )

            output_path = generated_report_utils.report_path_from_root(report_dir, "connector_work_queue", "md")
            rendered = output_path.read_text(encoding="utf-8")

        self.assertIn(f"1:{GENERATED_AT}:1:2", rendered)
        self.assertIn("Generated at:", rendered)

    def test_regenerate_phase_work_queue_preserves_callback_and_restores_original(self) -> None:
        with tempfile.TemporaryDirectory(prefix="focused-analysis-utils-") as temporary:
            connector_root = Path(temporary) / "connector"
            framework_root = Path(temporary) / "framework"
            report_dir = connector_root / "reports/testing/generated"
            script_path = framework_root / "ci/reporting/generate-phase-work-queue.py"
            connector_root.mkdir()
            report_dir.mkdir(parents=True)
            script_path.parent.mkdir(parents=True)
            script_path.write_text(
                textwrap.dedent(
                    """
                    import json
                    from pathlib import Path

                    def phase_work_direction(entry):
                        return ["original"]

                    def read_json(path):
                        return json.loads(Path(path).read_text(encoding="utf-8"))

                    def read_json_optional(path):
                        return read_json(path)

                    def parse_phase_coverage(path):
                        return Path(path).read_text(encoding="utf-8")

                    def build_payload(connector_work_queue, phase_coverage, full_runtime_matrix, framework_root, connector_root, inputs):
                        if connector_work_queue.get("raise_error"):
                            raise RuntimeError("controlled build failure")
                        return {
                            "generated_at": "2026-07-29T00:00:00Z",
                            "directions": [phase_work_direction(entry) for entry in connector_work_queue["entries"]],
                            "inputs": inputs,
                        }

                    def render_markdown(payload):
                        return "# Phase Work\\n" + str(payload["directions"])
                    """
                ).lstrip(),
                encoding="utf-8",
            )
            report_path_safety.add_safe_roots(connector_root, framework_root, report_dir)
            report_path_safety.add_report_roots(report_dir)
            queue_path = generated_report_utils.report_path_from_root(report_dir, "connector_work_queue", "json")
            coverage_path = generated_report_utils.report_path_from_root(report_dir, "phase_coverage", "md")
            matrix_path = generated_report_utils.report_path_from_root(report_dir, "full_runtime_matrix", "json")
            for path in (queue_path, coverage_path, matrix_path):
                path.parent.mkdir(parents=True, exist_ok=True)
            coverage_path.write_text("coverage\n", encoding="utf-8")
            matrix_path.write_text("{}\n", encoding="utf-8")
            queue_path.write_text(json.dumps({"entries": [{"case_id": "selected"}, {"case_id": "other"}]}), encoding="utf-8")
            self.addCleanup(sys.modules.pop, "phase_work_queue_generator", None)

            def override(entry: dict[str, object], original, _module) -> list[str]:
                return ["override"] if entry.get("case_id") == "selected" else original(entry)

            UTILS.regenerate_phase_work_queue(report_dir, framework_root, connector_root, override)
            payload = json.loads(
                generated_report_utils.report_path_from_root(report_dir, "phase_work_queue", "json").read_text(encoding="utf-8")
            )
            module = sys.modules["phase_work_queue_generator"]

            queue_path.write_text(json.dumps({"raise_error": True, "entries": []}), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "controlled build failure"):
                UTILS.regenerate_phase_work_queue(report_dir, framework_root, connector_root, override)

        self.assertEqual(payload["directions"], [["override"], ["original"]])
        self.assertEqual(module.phase_work_direction({"case_id": "selected"}), ["original"])

    def test_nolog_phase_work_queue_uses_the_framework_list_normalizer(self) -> None:
        captured: dict[str, object] = {}

        def capture_callback(
            _report_dir: Path,
            _framework_root: Path,
            _connector_root: Path,
            callback: object,
        ) -> None:
            captured["callback"] = callback

        with patch.object(NOLOG, "regenerate_phase_work_queue", side_effect=capture_callback):
            NOLOG.render_phase_work_queue(Path("reports/generated"), Path("framework"), Path("connector"))

        callback = captured["callback"]
        work_direction = object()
        framework_module = SimpleNamespace(
            as_list=lambda value: ["classification_only"] if value is work_direction else [],
        )

        self.assertEqual(
            callback(
                {
                    "case_id": NOLOG.CASE_ID,
                    "classification": NOLOG.CLASSIFICATION,
                    "work_direction": work_direction,
                },
                lambda _entry: ["framework-default"],
                framework_module,
            ),
            NOLOG.WORK_DIRECTION,
        )

    def test_write_generated_report_pair_uses_safe_registered_paths_and_metadata(self) -> None:
        with tempfile.TemporaryDirectory(prefix="focused-analysis-utils-") as temporary:
            connector_root = Path(temporary) / "connector"
            framework_root = Path(temporary) / "framework"
            report_dir = connector_root / "reports/testing/generated"
            connector_root.mkdir()
            framework_root.mkdir()
            report_dir.mkdir(parents=True)
            analysis = {
                "generated_at": GENERATED_AT,
                "source_reports": {"source": "reports/testing/generated/source.json"},
                "summary": {"rows": 1},
            }
            with self.assertRaisesRegex(ValueError, "safe roots must be configured"):
                UTILS.write_generated_report_pair(
                    report_dir,
                    connector_root,
                    framework_root,
                    analysis,
                    report_name="nolog_audit_evidence",
                    generated_by="tests/focused-analysis-utils",
                    make_target="test-focused-analysis-utils",
                    markdown="# Nolog\n",
                )
            report_path_safety.add_safe_roots(connector_root, framework_root, report_dir)
            report_path_safety.add_report_roots(report_dir)

            markdown_path = UTILS.write_generated_report_pair(
                report_dir,
                connector_root,
                framework_root,
                analysis,
                report_name="nolog_audit_evidence",
                generated_by="tests/focused-analysis-utils",
                make_target="test-focused-analysis-utils",
                markdown="# Nolog\n",
            )
            json_path = generated_report_utils.report_path_from_root(report_dir, "nolog_audit_evidence", "json")
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            markdown = markdown_path.read_text(encoding="utf-8")

        self.assertEqual(markdown_path, generated_report_utils.report_path_from_root(report_dir, "nolog_audit_evidence", "md"))
        self.assertEqual(payload["summary"], {"rows": 1})
        self.assertEqual(payload["metadata"]["generated_by"], "tests/focused-analysis-utils")
        self.assertIn("# Nolog", markdown)

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

    def test_shared_action_value_preserves_case_and_missing_value_behavior(self) -> None:
        actions = [" id:123 ", "PHASE:2", "msg:kept"]

        self.assertEqual(UTILS.action_value(actions, "phase"), "2")
        self.assertEqual(UTILS.action_value(actions, "missing"), "-")

    def test_shared_log_paths_keep_evidence_order_and_safe_root_gate(self) -> None:
        with tempfile.TemporaryDirectory(prefix="focused-analysis-utils-") as temporary:
            temporary_root = Path(temporary)
            safe_root = temporary_root / "safe"
            safe_root.mkdir()
            audit_log = safe_root / "audit.log"
            decision_log = safe_root / "decision.log"
            outside_log = temporary_root / "outside.log"
            for path in (audit_log, decision_log, outside_log):
                path.write_text("log\n", encoding="utf-8")
            report_path_safety.add_safe_roots(safe_root)

            paths = UTILS.log_paths(
                {
                    "audit_log_path": audit_log,
                    "decision_log": decision_log,
                    "ignored": audit_log,
                    "outside_log_path": outside_log,
                }
            )

        self.assertEqual(paths, [audit_log.resolve(), decision_log.resolve()])

    def test_body_processor_literal_contracts_are_preserved(self) -> None:
        evidence_path = Path("/tmp") / "one" / "two" / "evidence.json"

        self.assertEqual(
            BODY_PROCESSOR.generated_config_path(
                {"case_id": "multipart-case", "connector": "nginx"}, evidence_path
            ),
            Path("/tmp") / "runtime" / "multipart-case" / BODY_PROCESSOR.GENERATED_SMOKE_CONFIG_RELATIVE_PATH,
        )
        self.assertEqual(
            BODY_PROCESSOR.body_kind(
                {"body": "payload"}, f"{BODY_PROCESSOR.MULTIPART_FORM_DATA_CONTENT_TYPE}; boundary=test"
            ),
            "multipart",
        )

    def test_body_processor_rejects_traversal_derived_request_body_path(self) -> None:
        with tempfile.TemporaryDirectory(prefix="focused-analysis-utils-") as temporary:
            temporary_root = Path(temporary)
            safe_root = temporary_root / "safe"
            evidence_path = safe_root / "level1/level2/level3/evidence.json"
            case_path = safe_root / "cases/probe.yaml"
            in_root_body = safe_root / "level1/runtime/legitimate-case/conf/request-body.bin"
            symlink_body = safe_root / "level1/runtime/symlink-case/conf/request-body.bin"
            outside_body = temporary_root / "outside/conf/request-body.bin"
            for path in (evidence_path, case_path, in_root_body, symlink_body, outside_body):
                path.parent.mkdir(parents=True, exist_ok=True)
            evidence_path.write_text("{}\n", encoding="utf-8")
            case_path.write_text(
                "request:\n"
                "  method: POST\n"
                "  path: /probe\n"
                "  body: fallback-body\n",
                encoding="utf-8",
            )
            in_root_body.write_bytes(b"legitimate-in-root-body")
            outside_body.write_bytes(b"outside-root-sentinel")
            symlink_body.symlink_to(outside_body)
            report_path_safety.add_safe_roots(safe_root)
            evidence = {"path": str(case_path)}
            request = {"body": "fallback-body"}
            legitimate_config = in_root_body.with_name("modsecurity-smoke.conf")
            traversal_config = safe_root / "level1/runtime/../../../outside/conf/modsecurity-smoke.conf"
            symlink_config = symlink_body.with_name("modsecurity-smoke.conf")

            legitimate = BODY_PROCESSOR.case_metadata(
                {"case_id": "legitimate-case", "connector": "nginx", "evidence": str(evidence_path)},
                evidence,
                safe_root,
            )
            traversal = BODY_PROCESSOR.case_metadata(
                {"case_id": "../../../outside", "connector": "nginx", "evidence": str(evidence_path)},
                evidence,
                safe_root,
            )
            symlink_escape = BODY_PROCESSOR.case_metadata(
                {"case_id": "symlink-case", "connector": "nginx", "evidence": str(evidence_path)},
                evidence,
                safe_root,
            )

            self.assertEqual(
                BODY_PROCESSOR.generated_body_length(legitimate_config, request), len(b"legitimate-in-root-body")
            )
            for unsafe_config in (traversal_config, symlink_config):
                with self.subTest(unsafe_config=unsafe_config):
                    self.assertEqual(BODY_PROCESSOR.generated_body_length(unsafe_config, request), len(b"fallback-body"))
                    self.assertEqual(BODY_PROCESSOR.request_body_bytes(unsafe_config, request), b"fallback-body")

        self.assertEqual(legitimate["body_preview"], "legitimate-in-root-body")
        self.assertEqual(traversal["body_preview"], "fallback-body")
        self.assertEqual(symlink_escape["body_preview"], "fallback-body")
        self.assertNotEqual(traversal["body_preview"], "outside-root-sentinel")
        outside_digest = hashlib.sha256(b"outside-root-sentinel").hexdigest()
        self.assertNotEqual(traversal["body_sha256"], outside_digest)
        self.assertNotEqual(symlink_escape["body_sha256"], outside_digest)

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
