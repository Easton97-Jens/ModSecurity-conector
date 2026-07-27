from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]


def load_report_module(relative_path: str, module_name: str):
    specification = importlib.util.spec_from_file_location(module_name, ROOT / relative_path)
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    sys.modules[module_name] = module
    specification.loader.exec_module(module)
    return module


CONNECTOR_ROADMAP = load_report_module(
    "ci/evidence/reports/generate-connector-roadmap.py",
    "report_conditional_connector_roadmap",
)
REFRESH = load_report_module(
    "ci/evidence/reports/refresh-connector-reports.py",
    "report_conditional_refresh",
)
NGINX_HTTP500 = load_report_module(
    "ci/evidence/reports/generate-nginx-mrts-http500-cluster-analysis.py",
    "report_conditional_nginx_http500",
)
RUNTIME_MISMATCH = load_report_module(
    "ci/evidence/reports/generate-verified-runtime-mismatch-analysis.py",
    "report_conditional_runtime_mismatch",
)
BODY_PROCESSOR = load_report_module(
    "ci/evidence/reports/generate-body-processor-analysis.py",
    "report_conditional_body_processor",
)
INTERVENTION = load_report_module(
    "ci/evidence/reports/generate-intervention-blocking-analysis.py",
    "report_conditional_intervention",
)
NOLOG = load_report_module(
    "ci/evidence/reports/generate-nolog-audit-evidence-analysis.py",
    "report_conditional_nolog",
)
RESPONSE_HEADERS = load_report_module(
    "ci/evidence/reports/generate-response-header-hook-analysis.py",
    "report_conditional_response_headers",
)
RULE_CHAIN = load_report_module(
    "ci/evidence/reports/generate-rule-chain-semantics-analysis.py",
    "report_conditional_rule_chain",
)


class ReportConditionalRemediationTest(unittest.TestCase):
    def test_action_part_helpers_preserve_quote_transitions(self) -> None:
        cases = (
            (
                "id:1,msg:'one,two',ctl:\"three,four\",tag:five",
                ["id:1", "msg:'one,two'", 'ctl:"three,four"', "tag:five"],
            ),
            (
                "id:2,msg:'outer,\"inside,comma\"',ctl:\"outer,'inside,comma'\",tag:four",
                [
                    "id:2",
                    "msg:'outer,\"inside,comma\"'",
                    'ctl:"outer,\'inside,comma\'"',
                    "tag:four",
                ],
            ),
            (
                "id:3,msg:'unterminated,tag:five",
                ["id:3", "msg:'unterminated,tag:five"],
            ),
        )
        for actions, expected in cases:
            for module in (BODY_PROCESSOR, INTERVENTION, NOLOG, RESPONSE_HEADERS, RULE_CHAIN):
                with self.subTest(module=module.__name__, actions=actions):
                    self.assertEqual(module.action_parts(actions), expected)

    def test_connector_roadmap_keeps_production_and_partial_statuses(self) -> None:
        production = CONNECTOR_ROADMAP.connector_row(ROOT, "apache")
        partial = CONNECTOR_ROADMAP.connector_row(ROOT, "envoy")

        self.assertEqual(production["runtime_evidence"], "yes")
        self.assertEqual(production["modsecurity_integration"], "yes")
        self.assertEqual(partial["runtime_evidence"], "targeted proof required")
        self.assertEqual(partial["modsecurity_integration"], "starter_only")

    def test_access_log_status_is_linear_parser_with_valid_log_control(self) -> None:
        valid = '127.0.0.1 - - [16/Jun/2026:12:00:00 +0000] "GET /ok HTTP/1.1" 503 12 "-" "test"'
        malformed = '"GET ' + ("path HTTP/1.1 " * 800)

        self.assertEqual(NGINX_HTTP500.access_log_status(valid), "503")
        with mock.patch.object(NGINX_HTTP500.re, "search", side_effect=AssertionError("unbounded request regex")):
            self.assertIsNone(NGINX_HTTP500.access_log_status(malformed))

        with tempfile.TemporaryDirectory() as temporary:
            access_log = Path(temporary) / "access.log"
            access_log.write_text(
                "\n".join(
                    (
                        valid,
                        malformed,
                        '127.0.0.1 - - [16/Jun/2026:12:00:01 +0000] "POST /final HTTP/2.0" 502 7 "-" "test"',
                    )
                )
                + "\n",
                encoding="utf-8",
            )
            self.assertEqual(NGINX_HTTP500.access_status(access_log, "2026/06/16"), "502")

    def test_runtime_summary_preserves_mismatch_and_timeout_priorities(self) -> None:
        mismatch_summary = RUNTIME_MISMATCH.command_summary(
            [
                {
                    "logical_target": "full-matrix-parallel",
                    "runtime_complete": True,
                    "runtime_status": "",
                }
            ],
            [{"return_code": 1}],
            "full",
        )
        timeout_summary = RUNTIME_MISMATCH.command_summary(
            [{"logical_target": "full-matrix-parallel", "classification": "blocked_timeout"}],
            [],
            "full",
        )

        self.assertEqual(mismatch_summary["full_matrix_runtime_status"], "runtime_completed_with_mismatches")
        self.assertEqual(timeout_summary["full_matrix_runtime_status"], "runtime_timeout")

    def test_full_runtime_status_preserves_priority_and_laziness(self) -> None:
        class RowsMustNotBeRead(list):
            def __iter__(self):
                raise AssertionError("explicit runtime status must not inspect manifest rows")

        self.assertEqual(
            RUNTIME_MISMATCH.full_runtime_status({"runtime_status": "reported"}, RowsMustNotBeRead(), True),
            "reported",
        )
        self.assertEqual(RUNTIME_MISMATCH.full_runtime_status({}, RowsMustNotBeRead(), False), "not_run")
        self.assertEqual(RUNTIME_MISMATCH.full_runtime_status({}, [], True), "runtime_completed")
        self.assertEqual(RUNTIME_MISMATCH.full_runtime_status({}, [{"return_code": None}], True), "runtime_completed")
        self.assertEqual(
            RUNTIME_MISMATCH.full_runtime_status({}, [{"return_code": 1}], True),
            "runtime_completed_with_mismatches",
        )
        self.assertEqual(
            RUNTIME_MISMATCH.full_runtime_status({"classification": "blocked_timeout"}, [], False),
            "runtime_timeout",
        )
        self.assertEqual(RUNTIME_MISMATCH.full_runtime_status({}, [], False), "not_run")

    def test_report_status_branches_keep_existing_values(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            case_path = root / "case.yaml"
            evidence_path = root / "evidence.json"
            config_path = root / "modsecurity-smoke.conf"
            case_path.write_text("", encoding="utf-8")
            evidence_path.write_text("{}\n", encoding="utf-8")
            for config, expected in (
                ("SecRequestBodyAccess On\nSecRequestBodyAccess Off\n", "yes"),
                ("SecRequestBodyAccess Off\n", "no"),
                ("", "unknown"),
            ):
                with self.subTest(config=config):
                    config_path.write_text(config, encoding="utf-8")
                    with mock.patch.object(BODY_PROCESSOR, "generated_config_path", return_value=config_path):
                        metadata = BODY_PROCESSOR.case_metadata(
                            {"evidence": str(evidence_path), "connector": "nginx"},
                            {"path": str(case_path)},
                            root,
                        )
                    self.assertEqual(metadata["request_body_access"], expected)

            for classification, actual_status, expected in (
                (RULE_CHAIN.DETECTION_ONLY_CLASSIFICATION, 403, "no"),
                ("other", 403, "yes"),
                ("other", 500, "unknown"),
            ):
                with self.subTest(classification=classification, actual_status=actual_status):
                    row = RULE_CHAIN.chain_row(
                        {
                            "evidence": "",
                            "classification": classification,
                            "actual_status": actual_status,
                            "expected_status": actual_status,
                        },
                        root,
                    )
                    self.assertEqual(row["intervention_created"], expected)

            responses = [
                {"metadata": {}, "totals": {}},
                {"metadata": {}, "release_readiness": "ready"},
                {"recommendation": {}},
                {"metadata": {}},
                {
                    "metadata": {},
                    "full_matrix": {"complete": False, "missing_jobs": "invalid"},
                    "evidence_scope": "full",
                    "critical_mismatch_count": 0,
                    "mismatch_count": 0,
                },
                {"missing_job_ids": ["apache", "nginx"]},
                {},
            ]
            with mock.patch.object(REFRESH, "read_json", side_effect=responses):
                dashboard = REFRESH.merge_dashboard_payload(
                    {"verified_run_id": "run", "reports": []},
                    {"reports": []},
                    [],
                    root,
                )

        self.assertEqual(dashboard["full_matrix_missing_jobs"], ["apache", "nginx"])
        self.assertEqual(
            dashboard["reason"],
            "Full-Matrix evidence is incomplete; 0/0 jobs complete; missing jobs: apache, nginx.",
        )
        self.assertIn("| Runtime Mismatch Analysis | UNKNOWN |", REFRESH.render_merge_dashboard_md(dashboard))


if __name__ == "__main__":
    unittest.main()
