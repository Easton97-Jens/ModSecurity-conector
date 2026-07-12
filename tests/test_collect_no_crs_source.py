from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "collect_no_crs_source", ROOT / "ci/collect-no-crs-source.py"
)
assert SPEC is not None and SPEC.loader is not None
collector = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(collector)

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
            "event": "htx_observed_intervention",
            "integration_mode": "native_htx_filter",
            "evaluation_mode": "observer_nonpromoted",
            "rule_evaluation": "libmodsecurity_observed",
            "transaction_id": "haproxy-htx-phase4",
            "case": "phase4",
            "phase": 4,
            "rule_id": 910004,
            "requested_action": "deny",
            "host_action": "not_attempted",
            "observed_client_status": 200,
            "payload_recorded": False,
        }
        evidence = collector.event_evidence([], "910004", [record])
        self.assertTrue(evidence["body_payload_absent_from_events"])
        self.assertEqual([], evidence["forbidden_event_keys"])

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
                        "rule_id": 1100301,
                        "http_status": 403,
                        "original_http_status": 200,
                        "visible_http_status": 200,
                        "requested_action": "deny",
                        "actual_action": "log_only",
                        "late_intervention": True,
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
                {"phase4_deny_after_commit_log_only": (None, "1100301")},
                allowed_source_root=root,
            )
            self.assertEqual(1, len(cases))
            case = cases[0]
            self.assertEqual("PASS", case["status"])
            self.assertTrue(case["event_metadata_verified"])
            self.assertEqual("deny", case["requested_action"])
            self.assertEqual("log_only", case["actual_action"])
            self.assertEqual(403, case["http_status"])
            self.assertEqual(200, case["visible_http_status"])

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
                        "rule_id": 1100201,
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
            self.assertEqual(1, len(cases))
            case = cases[0]
            self.assertEqual("phase3_deny_before_commit", case["case_id"])
            self.assertEqual("PASS", case["status"])
            self.assertTrue(case["event_metadata_verified"])
            self.assertEqual("deny", case["requested_action"])
            self.assertEqual("deny", case["actual_action"])
            self.assertFalse(case["headers_sent"])
            self.assertEqual(403, case["visible_http_status"])

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
        source = (ROOT / "ci/run-no-crs-baseline.sh").read_text(encoding="utf-8")
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

    def test_native_first_byte_log_stays_under_connector_run_root(self) -> None:
        source = (ROOT / "ci/run-native-first-byte.sh").read_text(encoding="utf-8")
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
