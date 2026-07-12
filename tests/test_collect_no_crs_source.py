from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "collect_no_crs_source", ROOT / "ci/runtime/lifecycle/collect-no-crs-source.py"
)
assert SPEC is not None and SPEC.loader is not None
collector = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(collector)

FRAMEWORK_SPEC = importlib.util.spec_from_file_location(
    "framework_no_crs_baseline",
    ROOT / "modules/ModSecurity-test-Framework/ci/checks/catalog/no_crs_baseline.py",
)
assert FRAMEWORK_SPEC is not None and FRAMEWORK_SPEC.loader is not None
framework_baseline = importlib.util.module_from_spec(FRAMEWORK_SPEC)
FRAMEWORK_SPEC.loader.exec_module(framework_baseline)

TRAEFIK_SPEC = importlib.util.spec_from_file_location(
    "traefik_runtime_smoke", ROOT / "connectors/traefik/scripts/runtime_smoke.py"
)
assert TRAEFIK_SPEC is not None and TRAEFIK_SPEC.loader is not None
traefik_smoke = importlib.util.module_from_spec(TRAEFIK_SPEC)
TRAEFIK_SPEC.loader.exec_module(traefik_smoke)


class CollectNoCrsSourceTest(unittest.TestCase):
    def test_nonpromoted_native_host_is_not_reclassified_as_source_failure(self) -> None:
        self.assertTrue(
            collector.nonpromoted_host_success(
                [
                    {
                        "status": "PASS",
                        "capability_promotion": "not_permitted",
                        "integration_mode": "native-traefik-middleware",
                    }
                ]
            )
        )
        self.assertFalse(
            collector.nonpromoted_host_success([{"status": "PASS"}])
        )
        self.assertFalse(
            collector.nonpromoted_host_success(
                [{"status": "FAIL", "capability_promotion": "not_permitted"}]
            )
        )

    def test_not_executable_harness_case_is_canonical_not_executed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="no-crs-collector-") as temporary:
            source = Path(temporary) / "cases.jsonl"
            source.write_text(
                json.dumps({
                    "case_id": "allow_without_marker",
                    "status": "not_executable",
                    "live_executed": False,
                }) + "\n",
                encoding="utf-8",
            )
            cases, _ = collector.case_observations(
                [source],
                "nginx",
                "1100001",
                {"allow_without_marker": (200, None)},
            )
            self.assertEqual("NOT_EXECUTED", cases[0]["status"])
            self.assertTrue(collector.only_nonexecuted_cases(cases))

    def test_native_rule_engine_summary_keeps_explicit_case_evidence(self) -> None:
        summary = {
            "status": "PASS",
            "capability_promotion": "not_permitted",
            "common_runtime_bridge": True,
            "rule_evaluation": "libmodsecurity",
            "allowed_request_status": 200,
            "phase1_deny_status": 403,
            "p1_alternative_status": 429,
            "phase2_deny_status": 403,
            "phase3_deny_client_status": 403,
            "phase3_redirect_status": 302,
            "phase4_rule_observed_status": 200,
            "phase4_safe_status": 200,
            "phase4_end_of_stream_evaluation_status": 200,
            "phase4_first_byte_before_response_end_status": 200,
            "phase4_no_full_response_buffering_status": 200,
        }
        self.assertTrue(collector.native_rule_engine_observed([summary]))
        self.assertFalse(collector.nonpromoted_host_success([summary]))
        records = {
            record["case_id"]: record
            for record in collector.native_host_summary_cases([summary])
        }
        self.assertEqual(200, records["allow_without_marker"]["actual_status"])
        self.assertEqual([1100001], records["deny_header_marker_403"]["observed_rule_ids"])
        self.assertEqual(
            [1100002], records["deny_with_alternative_status"]["observed_rule_ids"]
        )
        self.assertEqual([1100101], records["deny_request_body_marker_403"]["observed_rule_ids"])
        self.assertEqual([1100201], records["deny_response_header_marker_403"]["observed_rule_ids"])
        self.assertEqual([1100202], records["phase3_redirect_before_commit"]["observed_rule_ids"])
        self.assertEqual([1100301], records["phase4_rule_observed"]["observed_rule_ids"])
        self.assertEqual(
            [1100301],
            records["phase4_deny_after_commit_log_only_safe"]["observed_rule_ids"],
        )
        for case_id in (
            "phase4_end_of_stream_evaluation",
            "phase4_first_byte_before_response_end",
            "phase4_no_full_response_buffering",
        ):
            with self.subTest(case_id=case_id):
                self.assertEqual([1100301], records[case_id]["observed_rule_ids"])

    def test_native_summary_without_engine_bridge_stays_nonpromoting(self) -> None:
        summary = {
            "status": "PASS",
            "capability_promotion": "not_permitted",
            "p1_allow_status": 200,
            "p1_deny_status": 403,
        }
        self.assertFalse(collector.native_rule_engine_observed([summary]))
        self.assertEqual([], collector.native_host_summary_cases([summary]))
        self.assertTrue(collector.nonpromoted_host_success([summary]))

    def test_raw_source_event_payload_field_invalidates_absence_claim(self) -> None:
        with tempfile.TemporaryDirectory(prefix="no-crs-collector-") as temporary:
            event_path = Path(temporary) / "events.jsonl"
            event_path.write_text(
                json.dumps(
                    {
                        "connector": "apache",
                        "transaction_id": "tx-1",
                        "rule_id": 1100001,
                        "phase": 1,
                        "status": "blocked",
                        "request_body": "no-crs-request-body-marker",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            evidence = collector.event_evidence([event_path], "1100001", [])
            self.assertFalse(evidence["body_payload_absent_from_events"])
            self.assertFalse(evidence["event_metadata_verified"])
            self.assertTrue(evidence["forbidden_event_keys"])
            self.assertEqual([], evidence["records"])

    def test_unknown_raw_event_field_invalidates_absence_claim(self) -> None:
        with tempfile.TemporaryDirectory(prefix="no-crs-collector-") as temporary:
            event_path = Path(temporary) / "events.jsonl"
            event_path.write_text(
                json.dumps(
                    {
                        "connector": "apache",
                        "transaction_id": "tx-unknown-field",
                        "rule_id": 1100001,
                        "phase": 1,
                        "status": "blocked",
                        "data": "arbitrary-full-request-body",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            evidence = collector.event_evidence([event_path], "1100001", [])
            self.assertFalse(evidence["body_payload_absent_from_events"])
            self.assertFalse(evidence["event_metadata_verified"])
            self.assertIn("unapproved-field:data", evidence["forbidden_event_keys"][0])
            self.assertEqual([], evidence["records"])

    def test_metadata_only_haproxy_decision_schema_is_accepted(self) -> None:
        record = {
            "timestamp": 1,
            "connector": "haproxy",
            "mode": "block",
            "runtime_mode": "test",
            "variant": "no-crs",
            "case": "deny_header_marker_403",
            "request_id": "tx-haproxy",
            "transaction_id": "tx-haproxy",
            "phase": 1,
            "live_executed": True,
            "modsecurity_processed": True,
            "request_headers_seen": True,
            "request_body_seen": False,
            "response_headers_seen": False,
            "response_body_seen": False,
            "expected_status": 403,
            "observed_status": "",
            "result": "",
            "decision": "deny",
            "disruptive": True,
            "intervention_status": 403,
            "redirect_present": False,
            "rule_id": 1100001,
            "anomaly_score": 0,
            "audit_log_path": "/tmp/audit.log",
            "haproxy_log_path": "",
            "spoa_log_path": "/tmp/spoa.log",
            "reason_code": "modsecurity_disruptive_intervention",
            "reason": "modsecurity_disruptive_intervention",
        }
        evidence = collector.event_evidence([], "1100001", [record])
        self.assertTrue(evidence["body_payload_absent_from_events"])
        self.assertTrue(evidence["event_metadata_verified"])
        self.assertEqual([], evidence["forbidden_event_keys"])

    def test_native_htx_observer_metadata_is_payload_free(self) -> None:
        record = {
            "connector": "haproxy",
            "event": "htx_observed_intervention",
            "message_id": "HAPROXY_HTX_OBSERVED_INTERVENTION",
            "integration_mode": "native_htx_filter",
            "evaluation_mode": "observer_nonpromoted",
            "rule_evaluation": "libmodsecurity_observed",
            "transaction_id": "haproxy-htx-phase4",
            "case": "phase4",
            "phase": 4,
            "rule_id": 910004,
            "status": "not_attempted",
            "requested_action": "deny",
            "host_action": "not_attempted",
            "observed_client_status": 200,
            "payload_recorded": False,
        }
        evidence = collector.event_evidence([], "910004", [record])
        self.assertTrue(evidence["body_payload_absent_from_events"])
        self.assertEqual([], evidence["forbidden_event_keys"])
        canonical_event = collector.sanitized_event(record)
        self.assertEqual(canonical_event["connector"], "haproxy")
        self.assertEqual(canonical_event["integration_mode"], "native_htx_filter")
        self.assertEqual(canonical_event["status"], "not_attempted")
        self.assertEqual(
            [],
            framework_baseline.canonical_event_errors(
                canonical_event,
                connector="haproxy",
            ),
        )

    def test_phase4_aliases_are_projected_without_status_conflation(self) -> None:
        event = collector.sanitized_event(
            {
                "connector": "nginx",
                "transaction_id": "tx-phase4",
                "rule_id": 1100301,
                "phase": "response_body",
                "waf_status": 403,
                "upstream_status": 200,
                "client_status": 200,
                "wanted_action": "deny",
                "actual_action": "connection_abort",
                "intervention": True,
                "header_sent": True,
                "response_body_seen": True,
                "strict_abort": True,
                "response_committed": True,
                "observed_transport_result": "connection_aborted",
            }
        )
        self.assertEqual(4, event["phase"])
        self.assertEqual(403, event["http_status"])
        self.assertEqual(200, event["original_http_status"])
        self.assertEqual(200, event["visible_http_status"])
        self.assertEqual("deny", event["requested_action"])
        self.assertEqual("abort_connection", event["actual_action"])
        self.assertTrue(event["late_intervention"])
        self.assertTrue(event["headers_sent"])
        self.assertTrue(event["body_started"])
        self.assertTrue(event["connection_aborted"])
        self.assertEqual("connection_aborted", event["transport_result"])

    def test_transport_lifecycle_metadata_is_allowlisted_and_bounded(self) -> None:
        event = collector.sanitized_event(
            {
                "connector": "nginx",
                "transaction_id": "tx-transport-1",
                "phase": 4,
                "transport_case_id": "transport-case-1",
                "requested_protocol": "h2",
                "downstream_protocol": "h2",
                "upstream_protocol": "http1",
                "negotiated_protocol": "h2",
                "transport": "tls_tcp",
                "stream_id": 1,
                "stream_reset": True,
                "reset_by": "strict_intervention",
                "reset_code": "CANCEL",
                "timeout_stage": "after_commit",
                "write_result": "short_write",
                "cleanup_reason": "strict_abort",
                "eos_seen": True,
                "client_disconnected": False,
                "upstream_disconnected": False,
                "cancelled": False,
            }
        )
        self.assertEqual("transport-case-1", event["transport_case_id"])
        self.assertEqual("h2", event["negotiated_protocol"])
        self.assertEqual("tls_tcp", event["transport"])
        self.assertEqual("strict_intervention", event["reset_by"])
        self.assertEqual("short_write", event["write_result"])
        self.assertTrue(event["eos_seen"])

    def test_synchronized_first_byte_metadata_is_allowlisted_without_payload(self) -> None:
        event = collector.sanitized_event(
            {
                "connector": "nginx",
                "transaction_id": "tx-first-byte",
                "rule_id": 1100301,
                "phase": "response_body",
                "status": "blocked",
                "client_first_byte_received": True,
                "first_chunk_size": 17,
                "upstream_paused": True,
                "upstream_eos_sent_at_first_byte": False,
                "first_byte_before_response_end": True,
                "upstream_response_finished_at_first_byte": False,
                "no_full_response_buffering": True,
                "body_bytes_seen": 17,
                "body_bytes_inspected": 17,
            }
        )
        self.assertTrue(event["client_first_byte_received"])
        self.assertEqual(17, event["first_chunk_size"])
        self.assertTrue(event["upstream_paused"])
        self.assertFalse(event["upstream_eos_sent_at_first_byte"])
        self.assertTrue(event["first_byte_before_response_end"])
        self.assertFalse(event["upstream_response_finished_at_first_byte"])
        self.assertTrue(event["no_full_response_buffering"])
        self.assertEqual(17, event["body_bytes_seen"])
        self.assertEqual(17, event["body_bytes_inspected"])

    def test_real_host_barrier_only_enriches_observed_phase4_event(self) -> None:
        evidence = {
            "evidence_type": "synchronized_first_byte",
            "evidence_origin": "real_host",
            "promotion_eligible": True,
            "outcome": "PASS",
            "body_payload_persisted": False,
            "client_first_byte_received": True,
            "first_byte_before_response_end": True,
            "first_chunk_size": 17,
            "upstream_paused": True,
            "upstream_eos_sent_at_first_byte": False,
            "upstream_response_finished_at_first_byte": False,
            "response_committed": True,
            "body_bytes_seen": 42,
            "body_bytes_inspected": 42,
            "no_full_response_buffering": True,
            "connector_owned_full_response_buffer": False,
        }
        records = collector.merge_first_byte_evidence(
            [
                {"phase": 1, "rule_id": 1100001},
                {"phase": "response_body", "rule_id": 1100301,
                 "body_bytes_seen": 42, "body_bytes_inspected": 42},
            ],
            evidence,
        )
        self.assertNotIn("first_byte_before_response_end", records[0])
        self.assertTrue(records[1]["first_byte_before_response_end"])
        self.assertTrue(records[1]["no_full_response_buffering"])
        self.assertEqual(42, records[1]["body_bytes_seen"])

    def test_response_status_is_not_dual_mapped_to_original_and_visible(self) -> None:
        event = collector.sanitized_event({"response_status": 200})
        self.assertNotIn("original_http_status", event)
        self.assertNotIn("visible_http_status", event)
        self.assertNotIn("http_status", event)

    def test_phase4_case_keeps_runtime_semantics_from_event(self) -> None:
        with tempfile.TemporaryDirectory(prefix="no-crs-phase4-") as temporary:
            root = Path(temporary)
            phase4_path = root / "phase4.jsonl"
            phase4_path.write_text(
                json.dumps(
                    {
                        "connector": "nginx",
                        "transaction_id": "tx-phase4",
                        "event": "phase4_intervention",
                        "message_id": "MSCONN_EVENT_PHASE4_LATE_INTERVENTION",
                        "phase": "response_body",
                        "status": "blocked",
                        "rule_id": "1100301",
                        "http_status": 403,
                        "original_http_status": 200,
                        "visible_http_status": 200,
                        "requested_action": "deny",
                        "actual_action": "log_only",
                        "late_intervention": True,
                        "late_intervention_mode": "safe",
                        "headers_sent": True,
                        "body_started": True,
                        "connection_aborted": False,
                        "response_committed": True,
                        "transport_result": "log_only",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            results_path = root / "results.jsonl"
            results_path.write_text(
                json.dumps(
                    {
                        "case_id": "phase4_deny_after_commit_log_only",
                        "status": "PASS",
                        "live_executed": True,
                        "actual_status": 200,
                        "connector_phase4_log_path": str(phase4_path),
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            cases, _ = collector.case_observations(
                [results_path],
                "nginx",
                "1100001",
                {
                    "phase4_deny_after_commit_log_only": (None, "1100301", 4),
                    "phase4_deny_after_commit_log_only_safe": (None, "1100301", 4),
                },
                allowed_source_root=root,
            )
            self.assertEqual(2, len(cases))
            by_id = {case["case_id"]: case for case in cases}
            case = by_id["phase4_deny_after_commit_log_only"]
            self.assertEqual("PASS", case["status"])
            self.assertTrue(case["event_metadata_verified"])
            self.assertEqual("deny", case["requested_action"])
            self.assertEqual("log_only", case["actual_action"])
            self.assertEqual("safe", case["late_intervention_mode"])
            self.assertEqual(403, case["http_status"])
            self.assertEqual(200, case["visible_http_status"])
            safe_alias = by_id["phase4_deny_after_commit_log_only_safe"]
            self.assertEqual("PASS", safe_alias["status"])
            self.assertEqual(["tx-phase4"], safe_alias["transaction_ids"])
            self.assertIn("reused native nginx event", safe_alias["reason"])

    def test_native_runner_safe_alias_requires_safe_event_semantics(self) -> None:
        safe_event = {
            "phase": 4,
            "rule_id": 1100301,
            "requested_action": "deny",
            "actual_action": "log_only",
            "late_intervention": True,
            "late_intervention_mode": "safe",
            "headers_sent": True,
            "body_started": True,
            "response_committed": True,
            "connection_aborted": False,
            "http_status": 403,
            "original_http_status": 200,
            "visible_http_status": 200,
            "transport_result": "log_only",
        }
        self.assertEqual(
            "phase4_deny_after_commit_log_only_safe",
            collector.native_runner_core_case_alias(
                "apache", "phase4_deny_after_commit_log_only", [safe_event]
            ),
        )
        unsafe_event = dict(safe_event, late_intervention_mode="minimal")
        self.assertIsNone(
            collector.native_runner_core_case_alias(
                "apache", "phase4_deny_after_commit_log_only", [unsafe_event]
            )
        )

    def test_native_runner_aliases_normalize_native_string_phase_and_rule_ids(self) -> None:
        apache_phase3_event = {
            "phase": "response_headers",
            "rule_id": "1100201",
            "requested_action": "deny",
            "actual_action": "deny",
            "headers_sent": False,
            "visible_http_status": 403,
            "late_intervention": False,
            "transport_result": "http_status",
        }
        nginx_phase4_event = {
            "phase": "response_body",
            "rule_id": "1100301",
            "requested_action": "deny",
            "actual_action": "log_only",
            "late_intervention": True,
            "late_intervention_mode": "safe",
            "headers_sent": True,
            "body_started": True,
            "response_committed": True,
            "connection_aborted": False,
            "http_status": 403,
            "original_http_status": 200,
            "visible_http_status": 200,
            "transport_result": "log_only",
        }
        self.assertEqual(
            "deny_response_header_marker_403",
            collector.native_runner_core_case_alias(
                "apache", "phase3_deny_before_commit", [apache_phase3_event]
            ),
        )
        self.assertEqual(
            "phase4_deny_after_commit_log_only_safe",
            collector.native_runner_core_case_alias(
                "nginx", "phase4_deny_after_commit_log_only", [nginx_phase4_event]
            ),
        )
        self.assertIsNone(
            collector.native_runner_core_case_alias(
                "nginx",
                "phase4_deny_after_commit_log_only",
                [dict(nginx_phase4_event, late_intervention_mode="minimal")],
            )
        )

    def test_phase4_rejects_an_unknown_late_intervention_mode(self) -> None:
        event = collector.sanitized_event(
            {
                "phase": "response_body",
                "late_intervention": True,
                "late_intervention_mode": "late-403",
            }
        )
        self.assertTrue(event["late_intervention"])
        self.assertNotIn("late_intervention_mode", event)
        self.assertNotIn(
            "late_intervention_mode", collector.canonical_semantics([event])
        )

    def test_phase3_precommit_case_keeps_header_status_metadata(self) -> None:
        catalog = (
            ROOT
            / "modules/ModSecurity-test-Framework/tests/cases/no-crs-baseline/catalog.json"
        )
        expectations, runner_case_index = collector.catalog_contract(catalog)
        with tempfile.TemporaryDirectory(prefix="no-crs-phase3-") as temporary:
            root = Path(temporary)
            phase3_path = root / "phase3.jsonl"
            phase3_path.write_text(
                json.dumps(
                    {
                        "connector": "apache",
                        "transaction_id": "tx-phase3",
                        "event": "phase3_intervention",
                        "message_id": "MSCONN_EVENT_RESPONSE_BLOCKED",
                        "phase": "response_headers",
                        "status": "blocked",
                        "rule_id": "1100201",
                        "http_status": 403,
                        "original_http_status": 200,
                        "visible_http_status": 403,
                        "requested_action": "deny",
                        "actual_action": "deny",
                        "late_intervention": False,
                        "headers_sent": False,
                        "connection_aborted": False,
                        "response_committed": False,
                        "transport_result": "http_status",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            results_path = root / "results.jsonl"
            results_path.write_text(
                json.dumps(
                    {
                        "name": "phase3_deny_before_commit_fixture",
                        "path": str(
                            catalog.parent
                            / "full-lifecycle/phase3_deny_before_commit.yaml"
                        ),
                        "status": "PASS",
                        "live_executed": True,
                        "actual_status": 403,
                        "connector_phase4_log_path": str(phase3_path),
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            cases, _ = collector.case_observations(
                [results_path],
                "apache",
                "1100001",
                expectations,
                allowed_source_root=root,
                runner_case_index=runner_case_index,
            )
            self.assertEqual(2, len(cases))
            by_id = {case["case_id"]: case for case in cases}
            case = by_id["phase3_deny_before_commit"]
            self.assertEqual("phase3_deny_before_commit", case["case_id"])
            self.assertEqual("PASS", case["status"])
            self.assertTrue(case["event_metadata_verified"])
            self.assertEqual("deny", case["requested_action"])
            self.assertEqual("deny", case["actual_action"])
            self.assertFalse(case["headers_sent"])
            self.assertEqual(403, case["visible_http_status"])
            core_alias = by_id["deny_response_header_marker_403"]
            self.assertEqual("PASS", core_alias["status"])
            self.assertEqual(["tx-phase3"], core_alias["transaction_ids"])
            self.assertIn("reused native apache event", core_alias["reason"])

    def test_case_event_evidence_is_bound_to_its_declared_transaction(self) -> None:
        with tempfile.TemporaryDirectory(prefix="no-crs-transaction-binding-") as temporary:
            root = Path(temporary)
            decision_path = root / "events.jsonl"
            decision_path.write_text(
                "\n".join(
                    json.dumps(event)
                    for event in (
                        {
                            "connector": "lighttpd",
                            "transaction_id": "tx-real",
                            "event": "MSCONN_EVENT_RESPONSE_BLOCKED",
                            "message_id": "MSCONN_EVENT_RESPONSE_BLOCKED",
                            "rule_id": 1100201,
                            "phase": "response_headers",
                            "status": "blocked",
                            "http_status": 403,
                            "original_http_status": 200,
                            "visible_http_status": 403,
                            "requested_action": "deny",
                            "actual_action": "deny",
                            "headers_sent": False,
                            "connection_aborted": False,
                            "transport_result": "http_status",
                        },
                        {
                            "connector": "lighttpd",
                            "transaction_id": "tx-other",
                            "event": "MSCONN_EVENT_RESPONSE_BLOCKED",
                            "message_id": "MSCONN_EVENT_RESPONSE_BLOCKED",
                            "rule_id": 1100201,
                            "phase": "response_headers",
                            "status": "blocked",
                            "http_status": 403,
                            "original_http_status": 200,
                            "visible_http_status": 200,
                            "requested_action": "deny",
                            "actual_action": "deny",
                            "headers_sent": True,
                            "connection_aborted": False,
                            "transport_result": "http_status",
                        },
                    )
                )
                + "\n",
                encoding="utf-8",
            )
            results_path = root / "results.jsonl"
            results_path.write_text(
                json.dumps(
                    {
                        "case_id": "phase3_deny_before_commit",
                        "status": "PASS",
                        "live_executed": True,
                        "actual_status": 403,
                        "transaction_ids": ["tx-real"],
                        "decision_log_path": str(decision_path),
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            cases, derived = collector.case_observations(
                [results_path],
                "lighttpd",
                "1100001",
                {"phase3_deny_before_commit": (403, "1100201", 3)},
                allowed_source_root=root,
            )
            self.assertEqual("PASS", cases[0]["status"])
            self.assertEqual(["tx-real"], cases[0]["transaction_ids"])
            self.assertFalse(cases[0]["headers_sent"])
            self.assertEqual(1, len(derived))

    def test_case_cannot_borrow_another_transaction_event(self) -> None:
        with tempfile.TemporaryDirectory(prefix="no-crs-transaction-mismatch-") as temporary:
            root = Path(temporary)
            decision_path = root / "events.jsonl"
            decision_path.write_text(
                json.dumps(
                    {
                        "connector": "lighttpd",
                        "transaction_id": "tx-other",
                        "event": "MSCONN_EVENT_RESPONSE_BLOCKED",
                        "message_id": "MSCONN_EVENT_RESPONSE_BLOCKED",
                        "rule_id": 1100201,
                        "phase": "response_headers",
                        "status": "blocked",
                        "http_status": 403,
                        "visible_http_status": 403,
                        "requested_action": "deny",
                        "actual_action": "deny",
                        "headers_sent": False,
                        "connection_aborted": False,
                        "transport_result": "http_status",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            results_path = root / "results.jsonl"
            results_path.write_text(
                json.dumps(
                    {
                        "case_id": "phase3_deny_before_commit",
                        "status": "PASS",
                        "live_executed": True,
                        "actual_status": 403,
                        "transaction_ids": ["tx-real"],
                        "decision_log_path": str(decision_path),
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            cases, _ = collector.case_observations(
                [results_path],
                "lighttpd",
                "1100001",
                {"phase3_deny_before_commit": (403, "1100201", 3)},
                allowed_source_root=root,
            )
            self.assertEqual("FAIL", cases[0]["status"])
            self.assertFalse(cases[0]["event_metadata_verified"])
            self.assertEqual([], cases[0]["transaction_ids"])

    def test_honest_not_executed_case_stays_not_executed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="no-crs-not-executed-") as temporary:
            root = Path(temporary)
            results_path = root / "results.jsonl"
            results_path.write_text(
                json.dumps(
                    {
                        "case_id": "phase3_deny_before_commit",
                        "status": "NOT_EXECUTED",
                        "live_executed": False,
                        "reason": "host API has no tested response hook",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            cases, _ = collector.case_observations(
                [results_path],
                "lighttpd",
                "1100001",
                {"phase3_deny_before_commit": (403, "1100201", 3)},
                allowed_source_root=root,
            )
            self.assertEqual("NOT_EXECUTED", cases[0]["status"])
            self.assertFalse(cases[0]["event_metadata_verified"])

    def test_catalog_runner_case_mapping_does_not_guess_from_fixture_name(self) -> None:
        catalog = (
            ROOT
            / "modules/ModSecurity-test-Framework/tests/cases/no-crs-baseline/catalog.json"
        )
        expectations, runner_case_index = collector.catalog_contract(catalog)
        with tempfile.TemporaryDirectory(prefix="no-crs-runner-name-") as temporary:
            root = Path(temporary)
            results_path = root / "results.jsonl"
            results_path.write_text(
                json.dumps(
                    {
                        "name": "phase3_deny_before_commit_fixture",
                        "status": "PASS",
                        "live_executed": True,
                        "actual_status": 403,
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            cases, _ = collector.case_observations(
                [results_path],
                "nginx",
                "1100001",
                expectations,
                allowed_source_root=root,
                runner_case_index=runner_case_index,
            )
            self.assertEqual([], cases)

    def test_catalog_runner_case_mapping_rejects_duplicate_paths(self) -> None:
        with tempfile.TemporaryDirectory(prefix="no-crs-catalog-") as temporary:
            root = Path(temporary)
            (root / "runner.yaml").write_text("name: runner\n", encoding="utf-8")
            catalog = root / "catalog.json"
            catalog.write_text(
                json.dumps(
                    {
                        "cases": [
                            {"case_id": "first", "runner_case": "runner.yaml"},
                            {"case_id": "second", "runner_case": "runner.yaml"},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "runner_case is not unique"):
                collector.catalog_contract(catalog)

    def test_phase4_case_rejects_audit_log_as_event_fallback(self) -> None:
        with tempfile.TemporaryDirectory(prefix="no-crs-phase4-audit-") as temporary:
            root = Path(temporary)
            audit_path = root / "audit.log"
            audit_path.write_text(
                '[id "1100301"] (phase 4) [unique_id "tx-audit-phase4"]\n',
                encoding="utf-8",
            )
            results_path = root / "results.jsonl"
            results_path.write_text(
                json.dumps(
                    {
                        "case_id": "phase4_rule_observed",
                        "status": "PASS",
                        "live_executed": True,
                        "actual_status": 200,
                        "audit_log_path": str(audit_path),
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            cases, events = collector.case_observations(
                [results_path],
                "apache",
                "1100001",
                {"phase4_rule_observed": (None, "1100301")},
                allowed_source_root=root,
            )

            self.assertEqual([], events)
            self.assertEqual("FAIL", cases[0]["status"])
            self.assertFalse(cases[0]["event_metadata_verified"])

    def test_structured_request_event_suppresses_weaker_audit_fallback(self) -> None:
        with tempfile.TemporaryDirectory(prefix="no-crs-structured-request-") as temporary:
            root = Path(temporary)
            event_path = root / "native-events.jsonl"
            event_path.write_text(
                json.dumps(
                    {
                        "connector": "apache",
                        "integration_mode": "native-httpd-module",
                        "event": "MSCONN_EVENT_REQUEST_BLOCKED",
                        "message_id": "MSCONN_EVENT_REQUEST_BLOCKED",
                        "transaction_id": "tx-native-p1",
                        "rule_id": 1100001,
                        "phase": 1,
                        "status": "blocked",
                        "http_status": 403,
                        "visible_http_status": 403,
                        "requested_action": "deny",
                        "actual_action": "deny",
                        "transport_result": "http_status",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            audit_path = root / "audit.log"
            audit_path.write_text(
                '[id "1100001"] (phase 1) [unique_id "tx-native-p1"]\n',
                encoding="utf-8",
            )
            results_path = root / "results.jsonl"
            results_path.write_text(
                json.dumps(
                    {
                        "case_id": "deny_header_marker_403",
                        "status": "PASS",
                        "live_executed": True,
                        "actual_status": 403,
                        "transaction_id": "tx-native-p1",
                        "decision_log_path": str(event_path),
                        "audit_log_path": str(audit_path),
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            cases, derived = collector.case_observations(
                [results_path], "apache", "1100001", allowed_source_root=root
            )
            self.assertEqual("PASS", cases[0]["status"])
            self.assertEqual(1, len(derived))
            self.assertEqual("native-httpd-module", derived[0]["integration_mode"])

    def test_traefik_runtime_output_rejects_symlink_before_cleanup(self) -> None:
        with tempfile.TemporaryDirectory(prefix="traefik-output-") as temporary:
            root = Path(temporary)
            victim = root / "victim"
            victim.mkdir()
            marker = victim / "keep.txt"
            marker.write_text("keep\n", encoding="utf-8")
            output = root / "runtime-output"
            output.symlink_to(victim, target_is_directory=True)
            with self.assertRaises(traefik_smoke.MissingDependency):
                traefik_smoke.assert_no_symlink_components(output)
            self.assertEqual("keep\n", marker.read_text(encoding="utf-8"))

    def test_decision_log_is_audited_before_metadata_sanitization(self) -> None:
        with tempfile.TemporaryDirectory(prefix="no-crs-collector-") as temporary:
            root = Path(temporary)
            decision_path = root / "decision.jsonl"
            decision_path.write_text(
                json.dumps(
                    {
                        "connector": "apache",
                        "transaction_id": "tx-2",
                        "rule_id": 1100001,
                        "phase": 1,
                        "status": "blocked",
                        "request_body": "no-crs-request-body-marker",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            results_path = root / "results.jsonl"
            results_path.write_text(
                json.dumps(
                    {
                        "case_id": "deny_header_marker_403",
                        "status": "PASS",
                        "live_executed": True,
                        "actual_status": 403,
                        "decision_log_path": str(decision_path),
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            cases, derived = collector.case_observations(
                [results_path], "apache", "1100001"
            )
            self.assertEqual("PASS", cases[0]["status"])
            evidence = collector.event_evidence([], "1100001", derived)
            self.assertFalse(evidence["body_payload_absent_from_events"])
            self.assertFalse(evidence["event_metadata_verified"])
            self.assertTrue(evidence["forbidden_event_keys"])

    def test_source_event_path_must_belong_to_current_raw_run(self) -> None:
        with tempfile.TemporaryDirectory(prefix="no-crs-run-") as temporary:
            root = Path(temporary)
            raw_run = root / "raw-run"
            raw_run.mkdir()
            outside = root / "previous-run-event.jsonl"
            outside.write_text("{}\n", encoding="utf-8")
            results_path = raw_run / "results.jsonl"
            results_path.write_text(
                json.dumps(
                    {
                        "case_id": "deny_header_marker_403",
                        "status": "PASS",
                        "live_executed": True,
                        "actual_status": 403,
                        "decision_log_path": str(outside),
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "outside the allowed run root"):
                collector.case_observations(
                    [results_path],
                    "apache",
                    "1100001",
                    allowed_source_root=raw_run,
                )

    def test_consumed_run_local_event_is_scrubbed_after_normalization(self) -> None:
        with tempfile.TemporaryDirectory(prefix="no-crs-run-") as temporary:
            raw_run = Path(temporary)
            decision_path = raw_run / "decision.jsonl"
            decision_path.write_text(
                json.dumps(
                    {
                        "connector": "haproxy",
                        "transaction_id": "tx-current-run",
                        "rule_id": 1100001,
                        "phase": 1,
                        "status": "blocked",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            results_path = raw_run / "results.jsonl"
            results_path.write_text(
                json.dumps(
                    {
                        "case_id": "deny_header_marker_403",
                        "status": "PASS",
                        "live_executed": True,
                        "actual_status": 403,
                        "decision_log_path": str(decision_path),
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            consumed: list[Path] = []
            cases, derived = collector.case_observations(
                [results_path],
                "haproxy",
                "1100001",
                allowed_source_root=raw_run,
                consumed_event_paths=consumed,
            )
            self.assertEqual("PASS", cases[0]["status"])
            self.assertEqual(1, len(derived))
            scrub_log = raw_run / "source-event-scrub.log"
            removed = collector.scrub_source_event_paths(consumed, raw_run, scrub_log)
            self.assertEqual([decision_path], removed)
            self.assertFalse(decision_path.exists())
            self.assertIn(str(decision_path), scrub_log.read_text(encoding="utf-8"))

    def test_source_event_path_rejects_symlink_components(self) -> None:
        with tempfile.TemporaryDirectory(prefix="no-crs-run-") as temporary:
            raw_run = Path(temporary)
            real = raw_run / "real"
            real.mkdir()
            event = real / "events.jsonl"
            event.write_text("{}\n", encoding="utf-8")
            alias = raw_run / "alias"
            alias.symlink_to(real, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "contains a symlink"):
                collector.contained_source_event_path(alias / event.name, raw_run)

    def test_referenced_audit_without_rule_is_still_scrubbed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="no-crs-run-") as temporary:
            raw_run = Path(temporary)
            audit_path = raw_run / "audit.log"
            audit_path.write_text("metadata without a rule match\n", encoding="utf-8")
            results_path = raw_run / "results.jsonl"
            results_path.write_text(
                json.dumps(
                    {
                        "case_id": "allow_without_marker",
                        "status": "PASS",
                        "live_executed": True,
                        "actual_status": 200,
                        "audit_log_path": str(audit_path),
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            consumed: list[Path] = []
            _, derived = collector.case_observations(
                [results_path],
                "apache",
                "1100001",
                allowed_source_root=raw_run,
                consumed_event_paths=consumed,
            )
            self.assertEqual([], derived)
            self.assertEqual([audit_path], consumed)
            collector.scrub_source_event_paths(consumed, raw_run)
            self.assertFalse(audit_path.exists())

    def test_canonical_runner_routes_native_logs_into_raw_run(self) -> None:
        source = (ROOT / "ci/runtime/lifecycle/run-no-crs-baseline.sh").read_text(encoding="utf-8")
        for assignment in (
            "CANONICAL_VERIFIED_RUN_ROOT=$VERIFIED_RUN_ROOT",
            "STAGE_BUILD_ROOT=$CONNECTOR_RUN_ROOT/haproxy-host-work",
            'VERIFIED_RUN_ROOT="$CANONICAL_VERIFIED_RUN_ROOT"',
            'BUILD_ROOT="$STAGE_BUILD_ROOT"',
            'LOG_ROOT="$STAGE_LOG_ROOT"',
            'RESULTS_DIR="$STAGE_RESULTS_DIR"',
            'RUNTIME_BASE="$STAGE_RUNTIME_ROOT"',
            'APACHE_RUNTIME_LOG_DIR="$HOST_RUNTIME_ROOT/apache-runtime"',
            'NGINX_HARNESS_WORK_ROOT="$NGINX_RUN_ROOT"',
            'HAPROXY_HTX_RUNTIME_ROOT="$STAGE_RUNTIME_ROOT"',
            'ENVOY_EXT_PROC_RUNTIME_ROOT="$HOST_RUNTIME_ROOT"',
            'TRAEFIK_NATIVE_RUNTIME_ROOT="$TRAEFIK_RUNTIME_ROOT"',
            'LIGHTTPD_PATCHED_ROOT="$HOST_RUNTIME_ROOT/lighttpd-patched"',
            'LIGHTTPD_PATCHED_SMOKE_DIR="$LIGHTTPD_RUNTIME_ROOT"',
            '--allowed-source-root "$RAW_DIR"',
            '--scrub-source-events',
        ):
            self.assertIn(assignment, source)

    def test_protocol_client_bundle_is_root_runner_scoped_and_forwarded(self) -> None:
        source = (ROOT / "ci/runtime/lifecycle/run-no-crs-baseline.sh").read_text(encoding="utf-8")
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        for fragment in (
            "NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR=${NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR:-}",
            "NO_CRS_PROTOCOL_CLIENT=${NO_CRS_PROTOCOL_CLIENT:-0}",
            "NO_CRS_PROTOCOL_CLIENT must be 0 or 1",
            "requires NO_CRS_ARTIFACT_PROFILE=full_lifecycle",
            "must remain inside this raw run",
            "protocol client artifact directory escaped the current raw run",
            'set -- "$@" --protocol-client-artifact-dir "$protocol_client_artifact_dir"',
            "skipping H1 native first-byte helper for NGINX downstream",
        ):
            self.assertIn(fragment, source)
        self.assertIn("NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR ?=", makefile)
        self.assertIn("NO_CRS_PROTOCOL_CLIENT ?= 0", makefile)
        self.assertIn("export NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR", makefile)
        self.assertIn("export NO_CRS_PROTOCOL_CLIENT", makefile)
        transport_checker = makefile.split(
            "define RUN_TRANSPORT_HARDENING_EVIDENCE_CHECK", 1
        )[1].split("endef", 1)[0]
        self.assertIn('PYTHON="$(FRAMEWORK_PYTHON)"', transport_checker)

        completed = subprocess.run(
            ["sh", str(ROOT / "ci/runtime/lifecycle/run-no-crs-baseline.sh"), "envoy", "no_crs_baseline"],
            cwd=ROOT,
            env={
                **os.environ,
            "NO_CRS_ARTIFACT_PROFILE": "generic",
            "NO_CRS_PROTOCOL_CLIENT": "1",
            "NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR": "/tmp/not-a-canonical-bundle",
            },
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(1, completed.returncode)
        self.assertIn(
            "NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR requires NO_CRS_ARTIFACT_PROFILE=full_lifecycle",
            completed.stderr,
        )

    def test_native_first_byte_log_stays_under_connector_run_root(self) -> None:
        source = (ROOT / "ci/runtime/lifecycle/run-native-first-byte.sh").read_text(encoding="utf-8")
        self.assertIn("runtime_root=$HOST_RUNTIME_ROOT/first-byte-$connector", source)
        self.assertIn("log_root=$HOST_RUNTIME_ROOT/$connector-first-byte-logs", source)
        self.assertIn(
            'TEST_CASE="$FRAMEWORK_ROOT/tests/cases/no-crs-baseline/full-lifecycle/phase4_first_byte_before_response_end.yaml"',
            source,
        )
        self.assertNotIn(
            'TEST_CASE="$FRAMEWORK_ROOT/tests/cases/no-crs-baseline/allow_without_marker.yaml"',
            source,
        )
        self.assertNotIn("log_root=$runtime_root/logs", source)
        self.assertNotIn("log_root=$HOST_LOG_ROOT/$connector-first-byte", source)


if __name__ == "__main__":
    unittest.main()
