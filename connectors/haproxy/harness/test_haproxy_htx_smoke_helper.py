#!/usr/bin/env python3
"""Focused tests for the payload-free HAProxy HTX host-runtime helper."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import stat
import sys
import tempfile
import unittest


HELPER_PATH = Path(__file__).with_name("haproxy_htx_smoke_helper.py")
RUNTIME_PATH = Path(__file__).with_name("run_haproxy_htx_runtime.sh")
SPEC = importlib.util.spec_from_file_location("haproxy_htx_smoke_helper", HELPER_PATH)
assert SPEC is not None and SPEC.loader is not None
HELPER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HELPER)
COLLECTOR_PATH = HELPER.REPO_ROOT / "ci/runtime/lifecycle/collect-no-crs-source.py"
COLLECTOR_SPEC = importlib.util.spec_from_file_location("collect_no_crs_source", COLLECTOR_PATH)
assert COLLECTOR_SPEC is not None and COLLECTOR_SPEC.loader is not None
COLLECTOR = importlib.util.module_from_spec(COLLECTOR_SPEC)
COLLECTOR_SPEC.loader.exec_module(COLLECTOR)
SYNCHRONIZED_UPSTREAM_PATH = (
    HELPER.REPO_ROOT
    / "modules/ModSecurity-test-Framework/tests/runners/synchronized_upstream.py"
)
SYNCHRONIZED_UPSTREAM_SPEC = importlib.util.spec_from_file_location(
    "synchronized_upstream", SYNCHRONIZED_UPSTREAM_PATH,
)
assert SYNCHRONIZED_UPSTREAM_SPEC is not None and SYNCHRONIZED_UPSTREAM_SPEC.loader is not None
SYNCHRONIZED_UPSTREAM = importlib.util.module_from_spec(SYNCHRONIZED_UPSTREAM_SPEC)
sys.modules[SYNCHRONIZED_UPSTREAM_SPEC.name] = SYNCHRONIZED_UPSTREAM
SYNCHRONIZED_UPSTREAM_SPEC.loader.exec_module(SYNCHRONIZED_UPSTREAM)


class HAProxyHTXSmokeHelperTest(unittest.TestCase):
    def test_phase2_upstream_profile_is_isolated_from_ordinary_requests(self) -> None:
        self.assertEqual(
            ("phase2", None, HELPER.UPSTREAM_OK_BODY),
            HELPER.upstream_profile("/no-crs/request-body?trace=ignored"),
        )

    def test_runtime_summary_uses_collector_recognized_phase_keys(self) -> None:
        runtime = RUNTIME_PATH.read_text(encoding="utf-8")
        self.assertIn("FULL_LIFECYCLE_EVIDENCE_OUTPUT", runtime)
        self.assertIn("streaming-probe", runtime)
        self.assertIn("phase2_deny_status=403", runtime)
        for key in (
            "phase4_safe_status=%s",
            "phase4_end_of_stream_evaluation_status=%s",
            "phase4_first_byte_before_response_end_status=%s",
            "phase4_no_full_response_buffering_status=%s",
        ):
            with self.subTest(key=key):
                self.assertIn(key, runtime)

    def test_generated_config_selects_only_native_htx_filter(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            rules = root / "rules.conf"
            config = root / "haproxy.cfg"
            self.assertEqual(HELPER.write_rules(str(rules)), 0)
            self.assertEqual(HELPER.write_config(str(config), 18080, 18081, str(rules)), 0)
            content = config.read_text(encoding="utf-8")
            self.assertIn("filter modsecurity-htx rules-file", content)
            for forbidden in ("filter spoe", "send-spoe", "http-buffer-request", "wait-for-body", "res.body"):
                self.assertNotIn(forbidden, content)
            generated_rules = rules.read_text(encoding="utf-8")
            self.assertEqual(generated_rules, HELPER.canonical_rules_content())
            for rule_id in (1100001, 1100002, 1100101, 1100201, 1100301):
                self.assertIn(f"id:{rule_id}", generated_rules)
            self.assertNotIn("91000", generated_rules)

    def test_event_contains_only_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            events = Path(temporary) / "events.jsonl"
            decision_log = Path(temporary) / "haproxy.stderr.log"
            decision_log.write_text(
                "modsecurity-htx: request intervention observed; "
                "transaction_id=haproxy-htx-phase1 phase=1 status=403 "
                "rule_id=1100001 action=deny\n",
                encoding="utf-8",
            )
            self.assertEqual(
                HELPER.write_event(
                    str(events),
                    "phase1_403",
                    str(decision_log),
                    1,
                    1100001,
                    403,
                    "enforced_reply",
                ),
                0,
            )
            record = json.loads(events.read_text(encoding="utf-8"))
            self.assertEqual(record["connector"], "haproxy")
            self.assertEqual(record["message_id"], "HAPROXY_HTX_NATIVE_PRECOMMIT_DENY")
            self.assertEqual(record["status"], "blocked")
            self.assertEqual(record["integration_mode"], "native-htx-filter")
            self.assertEqual(record["evaluation_mode"], "native_host_runtime_nonpromoted")
            self.assertEqual(record["actual_action"], "deny")
            self.assertEqual(record["visible_http_status"], 403)
            self.assertFalse(record["headers_sent"])
            self.assertNotIn("body", record)
            self.assertNotIn("headers", record)
            self.assertEqual(stat.S_IMODE(events.stat().st_mode), 0o600)

            probe = Path(temporary) / "client-probe.json"
            host_evidence = Path(temporary) / "host-runtime-evidence.jsonl"
            probe.write_text(
                json.dumps({"status": 403, "response_bytes": 93, "content_type": "text/html"}),
                encoding="utf-8",
            )
            self.assertEqual(
                HELPER.write_host_evidence(
                    str(host_evidence),
                    "phase1_403",
                    1,
                    1100001,
                    str(probe),
                    0,
                    "enforced_reply",
                    str(decision_log),
                ),
                0,
            )
            raw_record = json.loads(host_evidence.read_text(encoding="utf-8"))
            self.assertEqual(raw_record["upstream_requests"], 0)
            self.assertEqual(raw_record["client_response_bytes"], 93)
            self.assertNotIn("no-crs-request-body-marker", host_evidence.read_text(encoding="utf-8"))

    def test_allow_event_binds_completed_client_and_upstream_transaction(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            events = root / "events.jsonl"
            probe = root / "client-probe.json"
            upstream = root / "upstream-requests.jsonl"
            probe.write_text(
                json.dumps({"status": 200, "response_bytes": 24, "content_type": "text/plain"}),
                encoding="utf-8",
            )
            upstream.write_text(
                json.dumps({
                    "method": "GET",
                    "response_status": 200,
                    "profile": "ordinary",
                    "request_id": "haproxy-htx-allow",
                }) + "\n",
                encoding="utf-8",
            )
            self.assertEqual(
                HELPER.write_allow_event(
                    str(events), str(probe), str(upstream), "haproxy-htx-allow",
                ),
                0,
            )
            record = json.loads(events.read_text(encoding="utf-8"))
            self.assertEqual(record["message_id"], "HAPROXY_HTX_NATIVE_P1_ALLOW")
            self.assertEqual(record["transaction_id"], "haproxy-htx-allow")
            self.assertEqual(record["phase"], 1)
            self.assertEqual(record["status"], "allowed")
            self.assertEqual(record["visible_http_status"], 200)
            self.assertNotIn("requested_action", record)
            self.assertNotIn("actual_action", record)
            schema = json.loads((
                HELPER.REPO_ROOT
                / "modules/ModSecurity-test-Framework/tests/schemas/no-crs-baseline/event.schema.json"
            ).read_text(encoding="utf-8"))
            self.assertTrue(set(record).issubset(set(schema["properties"])))
            self.assertTrue(set(record).issubset(COLLECTOR.APPROVED_RAW_EVENT_KEYS))
            self.assertNotIn("no-crs-request-body-marker", events.read_text(encoding="utf-8"))

    def test_allow_event_rejects_noncausal_or_nonallow_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            events = root / "events.jsonl"
            probe = root / "client-probe.json"
            upstream = root / "upstream-requests.jsonl"
            probe.write_text(
                json.dumps({"status": 403, "response_bytes": 24, "content_type": "text/plain"}),
                encoding="utf-8",
            )
            upstream.write_text(
                json.dumps({
                    "profile": "ordinary", "request_id": "haproxy-htx-allow",
                }) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "preserve HTTP 200"):
                HELPER.write_allow_event(
                    str(events), str(probe), str(upstream), "haproxy-htx-allow",
                )

            probe.write_text(
                json.dumps({"status": 200, "response_bytes": 24, "content_type": "text/plain"}),
                encoding="utf-8",
            )
            upstream.write_text(
                json.dumps({"profile": "ordinary", "request_id": "wrong-id"}) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "not observed exactly once upstream"):
                HELPER.write_allow_event(
                    str(events), str(probe), str(upstream), "haproxy-htx-allow",
                )
            with self.assertRaisesRegex(ValueError, "invalid HTX transaction id"):
                HELPER.write_allow_event(
                    str(events), str(probe), str(upstream), "haproxy:htx-allow",
                )

    def test_first_byte_evidence_binds_client_byte_to_paused_upstream(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            paused = root / "upstream-paused.json"
            client = root / "client-first-byte.json"
            evidence = root / "first-byte-evidence.json"
            paused.write_text(
                json.dumps({
                    "schema_version": 1,
                    "evidence_type": "synchronized_upstream_paused",
                    "first_chunk_size": 37,
                    "upstream_paused": True,
                    "upstream_eos_sent": False,
                    "body_payload_persisted": False,
                }),
                encoding="utf-8",
            )
            client.write_text(
                json.dumps({
                    "status": 200,
                    "client_first_byte_received": True,
                    "first_chunk_size": 1,
                    "response_committed": True,
                    "body_payload_persisted": False,
                }),
                encoding="utf-8",
            )
            self.assertEqual(
                HELPER.write_first_byte_evidence(str(evidence), str(paused), str(client)),
                0,
            )
            record = json.loads(evidence.read_text(encoding="utf-8"))
            self.assertEqual(record["evidence_origin"], "real_host")
            self.assertTrue(record["promotion_eligible"])
            self.assertTrue(record["client_first_byte_received"])
            self.assertTrue(record["upstream_paused"])
            self.assertFalse(record["upstream_eos_sent_at_first_byte"])
            self.assertFalse(record["upstream_response_finished_at_first_byte"])
            self.assertTrue(record["no_full_response_buffering"])
            self.assertFalse(record["connector_owned_full_response_buffer"])
            self.assertEqual(record["body_bytes_seen"], 37)
            self.assertEqual(record["body_bytes_inspected"], 37)
            self.assertEqual(
                [],
                SYNCHRONIZED_UPSTREAM.first_byte_evidence_errors(
                    record, require_real_host=True, require_complete_proof=True,
                ),
            )
            self.assertNotIn("no-crs-response-body-marker", evidence.read_text(encoding="utf-8"))

    def test_phase4_safe_event_requires_real_barrier_and_native_late_decision(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            events = root / "events.jsonl"
            decision_log = root / "haproxy.stderr.log"
            probe = root / "client-probe.json"
            first_byte = root / "first-byte-evidence.json"
            decision_log.write_text(
                "modsecurity-htx: response-body late intervention observed; "
                "transaction_id=haproxy-htx-phase4 phase=4 status=403 "
                "rule_id=1100301 requested_action=deny "
                "resolved_policy_action=log_only host_action=log_only\n",
                encoding="utf-8",
            )
            probe.write_text(
                json.dumps({"status": 200, "response_bytes": 81, "content_type": "text/plain"}),
                encoding="utf-8",
            )
            first_byte.write_text(
                json.dumps({
                    "schema_version": 1,
                    "evidence_type": "synchronized_first_byte",
                    "evidence_origin": "real_host",
                    "promotion_eligible": True,
                    "client_first_byte_received": True,
                    "first_byte_before_response_end": True,
                    "first_chunk_size": 19,
                    "upstream_paused": True,
                    "upstream_eos_sent_at_first_byte": False,
                    "upstream_response_finished_at_first_byte": False,
                    "response_committed": True,
                    "body_bytes_seen": 19,
                    "body_bytes_inspected": 19,
                    "no_full_response_buffering": True,
                    "connector_owned_full_response_buffer": False,
                    "body_payload_persisted": False,
                    "outcome": "PASS",
                }),
                encoding="utf-8",
            )
            self.assertEqual(
                HELPER.phase4_safe_event(
                    str(events),
                    str(decision_log),
                    str(probe),
                    str(first_byte),
                    "run-42",
                    "phase4_first_byte_before_response_end",
                ),
                0,
            )
            record = json.loads(events.read_text(encoding="utf-8"))
            self.assertEqual(record["integration_mode"], "native-htx-filter")
            self.assertEqual(record["transaction_id"], "haproxy-htx-phase4")
            self.assertEqual(record["phase"], 4)
            self.assertEqual(record["rule_id"], 1100301)
            self.assertEqual(record["requested_action"], "deny")
            self.assertEqual(record["actual_action"], "log_only")
            self.assertEqual(record["visible_http_status"], 200)
            self.assertTrue(record["late_intervention"])
            self.assertTrue(record["eos_seen"])
            self.assertTrue(record["end_of_stream_evaluation"])
            self.assertTrue(record["first_byte_before_response_end"])
            self.assertTrue(record["no_full_response_buffering"])
            self.assertNotIn("connector_owned_full_response_buffer", record)
            schema = json.loads((
                HELPER.REPO_ROOT
                / "modules/ModSecurity-test-Framework/tests/schemas/no-crs-baseline/event.schema.json"
            ).read_text(encoding="utf-8"))
            self.assertTrue(set(record).issubset(set(schema["properties"])))
            self.assertTrue(set(record).issubset(COLLECTOR.APPROVED_RAW_EVENT_KEYS))
            self.assertNotIn("no-crs-response-body-marker", events.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
