from __future__ import annotations

import http.server
import importlib.util
import json
import sys
import tempfile
import threading
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HELPER_PATH = ROOT / "connectors" / "envoy" / "harness" / "envoy_smoke_helper.py"
RUNTIME_PATH = ROOT / "connectors" / "envoy" / "harness" / "run_envoy_ext_proc_runtime.sh"


def load_helper() -> object:
    specification = importlib.util.spec_from_file_location("envoy_smoke_helper", HELPER_PATH)
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


class EnvoyTransportHardeningContractTest(unittest.TestCase):
    def test_first_body_byte_is_read_once_without_header_remainder(self) -> None:
        helper = load_helper()

        class Connection:
            def __init__(self) -> None:
                self.recv_limits: list[int] = []
                self.timeouts: list[float] = []
                self.responses = [
                    b"HTTP/1.1 200 OK\r\nContent-Length: 1\r\n\r\n",
                    b"x",
                ]

            def settimeout(self, timeout: float) -> None:
                self.timeouts.append(timeout)

            def recv(self, limit: int) -> bytes:
                self.recv_limits.append(limit)
                return self.responses.pop(0)

        connection = Connection()

        self.assertEqual((200, 1), helper._read_chunked_first_body(connection, timeout=1.0))
        self.assertEqual([4096, 1], connection.recv_limits)
        self.assertTrue(all(timeout > 0 for timeout in connection.timeouts))

    def test_client_cancel_waits_for_one_real_body_byte_then_closes(self) -> None:
        helper = load_helper()

        class FastCancelHandler(helper.UpstreamHandler):
            client_cancel_delay_seconds = 0.05

        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), FastCancelHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            observation = helper.client_cancel(
                "127.0.0.1",
                server.server_port,
                "/client-cancel",
                ["X-Request-Id: cancel-test"],
            )
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)

        self.assertEqual(200, observation["http_status"])
        self.assertTrue(observation["first_body_byte_received"])
        self.assertTrue(observation["client_closed"])

    def test_client_cancel_rejects_non_ascii_wire_headers(self) -> None:
        helper = load_helper()
        with self.assertRaises(ValueError):
            helper.client_cancel("127.0.0.1", 18080, "/client-cancel", ["X-Test: snowman-☃"])

    def test_phase4_barrier_confirms_first_byte_before_upstream_eos(self) -> None:
        helper = load_helper()
        with tempfile.TemporaryDirectory() as temporary:
            barrier_dir = Path(temporary) / "phase4-barrier"
            barrier_dir.mkdir()

            class BarrierHandler(helper.UpstreamHandler):
                phase4_barrier_dir = barrier_dir
                phase4_barrier_timeout_seconds = 2.0

            server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), BarrierHandler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                observation = helper.phase4_first_byte(
                    "127.0.0.1",
                    server.server_port,
                    "/phase4-marker",
                    ["X-Request-Id: phase4-first-byte-test"],
                    str(barrier_dir),
                    2.0,
                )
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=2)

            self.assertEqual(200, observation["http_status"])
            self.assertTrue(observation["client_first_byte_received"])
            self.assertTrue(observation["first_byte_before_response_end"])
            self.assertGreater(observation["first_chunk_size"], 0)
            self.assertTrue(observation["upstream_paused"])
            self.assertFalse(observation["upstream_eos_sent_at_first_byte"])
            self.assertFalse(observation["upstream_response_finished_at_first_byte"])
            self.assertTrue(observation["upstream_eos_sent_after_release"])
            self.assertFalse(observation["body_payload_persisted"])

            paused = json.loads((barrier_dir / "upstream-paused.json").read_text(encoding="utf-8"))
            completed = json.loads(
                (barrier_dir / "upstream-completed.json").read_text(encoding="utf-8")
            )
            self.assertTrue(paused["upstream_paused"])
            self.assertFalse(paused["upstream_eos_sent"])
            self.assertTrue(completed["upstream_eos_sent"])
            self.assertNotIn("no-crs-response-body-marker", json.dumps(observation))
            self.assertNotIn("no-crs-response-body-marker", json.dumps(paused))
            self.assertNotIn("no-crs-response-body-marker", json.dumps(completed))

    def test_phase4_first_byte_evidence_binds_to_the_common_safe_event(self) -> None:
        helper = load_helper()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            observation_path = root / "observation.json"
            event_path = root / "events.jsonl"
            evidence_path = root / "first-byte-evidence.json"
            helper.write_json_atomic(
                observation_path,
                {
                    "schema_version": 1,
                    "evidence_type": "envoy_phase4_first_byte_observation",
                    "http_status": 200,
                    "client_first_byte_received": True,
                    "first_byte_before_response_end": True,
                    "first_chunk_size": 17,
                    "upstream_paused": True,
                    "upstream_eos_sent_at_first_byte": False,
                    "upstream_response_finished_at_first_byte": False,
                    "upstream_eos_sent_after_release": True,
                    "body_payload_persisted": False,
                    "transport_protocol": "http1",
                    "outcome": "PASS",
                },
            )
            common_safe_event = {
                "connector": "envoy",
                "integration_mode": "ext_proc",
                "event": "MSCONN_EVENT_RULE",
                "message_id": "MSCONN_EVENT_RULE",
                "transaction_id": "envoy-ext-proc-phase4-safe",
                "rule_id": "1100301",
                "phase": "response_body",
                "status": "blocked",
                "http_status": 403,
                "original_http_status": 200,
                "visible_http_status": 200,
                "requested_action": "deny",
                "actual_action": "log_only",
                "late_intervention": True,
                "late_intervention_mode": "safe",
                "headers_sent": True,
                "body_started": True,
                "response_committed": True,
                "connection_aborted": False,
                "transport_result": "log_only",
                "body_bytes_seen": 42,
                "body_bytes_inspected": 42,
            }
            event_path.write_text(json.dumps(common_safe_event) + "\n", encoding="utf-8")

            result = helper.write_phase4_first_byte_evidence(
                event_log=str(event_path),
                observation_path=str(observation_path),
                transaction_id="envoy-ext-proc-phase4-safe",
                evidence_output=str(evidence_path),
                run_id="run-phase4-first-byte",
            )

            self.assertTrue(result["event_appended"])
            self.assertTrue(result["evidence_written"])
            evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
            self.assertEqual("synchronized_first_byte", evidence["evidence_type"])
            self.assertEqual("real_host", evidence["evidence_origin"])
            self.assertTrue(evidence["promotion_eligible"])
            self.assertTrue(evidence["first_byte_before_response_end"])
            self.assertTrue(evidence["no_full_response_buffering"])
            self.assertFalse(evidence["connector_owned_full_response_buffer"])
            self.assertEqual("http1", evidence["transport_protocol"])

            records = [json.loads(line) for line in event_path.read_text(encoding="utf-8").splitlines()]
            barrier_event = records[-1]
            self.assertEqual("phase4_first_byte_barrier", barrier_event["event"])
            self.assertEqual("envoy-ext-proc-phase4-safe", barrier_event["transaction_id"])
            self.assertEqual("1100301", barrier_event["rule_id"])
            self.assertEqual(4, barrier_event["phase"])
            self.assertEqual("safe", barrier_event["late_intervention_mode"])
            self.assertEqual("log_only", barrier_event["actual_action"])
            self.assertTrue(barrier_event["end_of_stream_evaluation"])
            self.assertTrue(barrier_event["eos_seen"])
            self.assertEqual("normal", barrier_event["cleanup_reason"])
            self.assertTrue(barrier_event["first_byte_before_response_end"])
            self.assertFalse(barrier_event["upstream_eos_sent_at_first_byte"])
            self.assertTrue(barrier_event["no_full_response_buffering"])
            self.assertNotIn("no-crs-response-body-marker", json.dumps(evidence))
            self.assertNotIn("no-crs-response-body-marker", json.dumps(barrier_event))

            repeated = helper.write_phase4_first_byte_evidence(
                event_log=str(event_path),
                observation_path=str(observation_path),
                transaction_id="envoy-ext-proc-phase4-safe",
                evidence_output=str(evidence_path),
                run_id="run-phase4-first-byte",
            )
            self.assertFalse(repeated["event_appended"])
            self.assertEqual(2, len(event_path.read_text(encoding="utf-8").splitlines()))

    def test_allow_event_binds_client_http200_to_one_normal_ext_proc_completion(self) -> None:
        helper = load_helper()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            events = root / "events.jsonl"
            probe = root / "allow-probe.json"
            completions = root / "completion-events.jsonl"
            events.write_text(
                json.dumps({
                    "connector": "envoy",
                    "integration_mode": "ext_proc",
                    "event": "phase4_first_byte_barrier",
                    "message_id": "MSCONN_EVENT_P4_FIRST_BYTE_BARRIER",
                    "transaction_id": "envoy-ext-proc-phase4-safe",
                    "rule_id": "1100301",
                    "phase": 4,
                    "status": "observed",
                    "http_status": 403,
                    "visible_http_status": 200,
                    "requested_action": "deny",
                    "actual_action": "log_only",
                    "late_intervention": True,
                    "late_intervention_mode": "safe",
                    "headers_sent": True,
                    "body_started": True,
                    "response_committed": True,
                    "connection_aborted": False,
                    "transport_result": "log_only",
                    "end_of_stream_evaluation": True,
                    "eos_seen": True,
                }) + "\n",
                encoding="utf-8",
            )
            helper.write_json_atomic(probe, {
                "schema_version": 1,
                "evidence_type": "envoy_http_client_probe",
                "http_status": 200,
                "response_bytes": 27,
                "body_payload_persisted": False,
            })
            completions.write_text(
                json.dumps({
                    "event": "ext_proc_stream_complete",
                    "integration_mode": "ext_proc",
                    "evaluation_mode": "common_libmodsecurity_nonpromoted",
                    "rule_evaluation": "libmodsecurity",
                    "transaction_id": "envoy-ext-proc-allow-1",
                    "response_body_bytes": 27,
                    "late_action": "none",
                    "close_reason": "response_end_of_stream",
                }) + "\n",
                encoding="utf-8",
            )

            result = helper.write_allow_event(
                event_log=str(events),
                probe_evidence_path=str(probe),
                completion_log=str(completions),
                transaction_id="envoy-ext-proc-allow-1",
            )

            self.assertTrue(result["event_appended"])
            allow_event = json.loads(events.read_text(encoding="utf-8").splitlines()[-1])
            self.assertEqual("ENVOY_EXT_PROC_NATIVE_P1_ALLOW", allow_event["message_id"])
            self.assertEqual("envoy-ext-proc-allow-1", allow_event["transaction_id"])
            self.assertEqual(1, allow_event["phase"])
            self.assertEqual(200, allow_event["visible_http_status"])
            self.assertNotIn("requested_action", allow_event)
            self.assertNotIn("actual_action", allow_event)
            self.assertNotIn("no-crs-response-body-marker", json.dumps(allow_event))

    def test_allow_event_rejects_noncausal_client_or_completion_metadata(self) -> None:
        helper = load_helper()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            events = root / "events.jsonl"
            probe = root / "allow-probe.json"
            completions = root / "completion-events.jsonl"
            events.write_text("{}\n", encoding="utf-8")
            helper.write_json_atomic(probe, {
                "schema_version": 1,
                "evidence_type": "envoy_http_client_probe",
                "http_status": 403,
                "response_bytes": 27,
                "body_payload_persisted": False,
            })
            completions.write_text(
                json.dumps({
                    "event": "ext_proc_stream_complete",
                    "integration_mode": "ext_proc",
                    "evaluation_mode": "common_libmodsecurity_nonpromoted",
                    "rule_evaluation": "libmodsecurity",
                    "transaction_id": "envoy-ext-proc-allow-1",
                    "response_body_bytes": 27,
                    "late_action": "none",
                    "close_reason": "response_end_of_stream",
                }) + "\n",
                encoding="utf-8",
            )
            event_log = str(events)
            probe_evidence_path = str(probe)
            completion_log = str(completions)
            with self.assertRaisesRegex(ValueError, "HTTP 200"):
                helper.write_allow_event(
                    event_log=event_log,
                    probe_evidence_path=probe_evidence_path,
                    completion_log=completion_log,
                    transaction_id="envoy-ext-proc-allow-1",
                )

            helper.write_json_atomic(probe, {
                "schema_version": 1,
                "evidence_type": "envoy_http_client_probe",
                "http_status": 200,
                "response_bytes": 27,
                "body_payload_persisted": False,
            })
            completions.write_text("\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "exactly one ext_proc completion"):
                helper.write_allow_event(
                    event_log=event_log,
                    probe_evidence_path=probe_evidence_path,
                    completion_log=completion_log,
                    transaction_id="envoy-ext-proc-allow-1",
                )

    def test_runtime_probe_keeps_cancellation_unattributed_and_nonpromoting(self) -> None:
        source = RUNTIME_PATH.read_text(encoding="utf-8")
        self.assertIn("ENVOY_TRANSPORT_CANCEL_PROBE", source)
        self.assertIn("grpc_context_canceled_unattributed", source)
        self.assertIn("grpc_peer_eof", source)
        self.assertIn("expected exactly one unattributed ext_proc terminal completion", source)
        self.assertIn("client_disconnect_after_first_response_chunk", source)
        self.assertIn("transport-observations.diagnostic.json", source)
        self.assertIn('"capability_promotion": "not_permitted"', source)
        self.assertIn('"state": "NOT_EXECUTED"', source)
        self.assertIn('"diagnostic_only": True', source)
        self.assertNotIn('"transport_case_id":', source)
        self.assertIn("client-cancel", source)
        self.assertIn("FULL_LIFECYCLE_EVIDENCE_OUTPUT", source)
        self.assertIn("phase4-first-byte", source)
        self.assertIn("phase4_first_byte_before_response_end_status", source)
        self.assertIn("phase4_no_full_response_buffering_status", source)
        self.assertIn("phase4_end_of_stream_evaluation_status", source)
        self.assertIn("phase4_rule_observed_status", source)
        self.assertIn("write-allow-event", source)


if __name__ == "__main__":
    unittest.main()
