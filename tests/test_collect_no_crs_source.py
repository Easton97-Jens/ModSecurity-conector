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
            'LOG_ROOT="$HOST_LOG_ROOT"',
            'RUNTIME_BASE="$HOST_RUNTIME_ROOT"',
            'APACHE_RUNTIME_LOG_DIR="$HOST_LOG_ROOT/apache-runtime"',
            'NGINX_HARNESS_WORK_ROOT="$NGINX_RUN_ROOT"',
            '--allowed-source-root "$RAW_DIR"',
            '--scrub-source-events',
        ):
            self.assertIn(assignment, source)


if __name__ == "__main__":
    unittest.main()
