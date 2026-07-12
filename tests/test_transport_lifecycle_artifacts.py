from __future__ import annotations

import importlib.util
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "transport_lifecycle_artifacts", ROOT / "ci" / "runtime" / "lifecycle" / "write-transport-lifecycle-artifacts.py"
)
assert SPEC is not None and SPEC.loader is not None
artifacts = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(artifacts)


class TransportLifecycleArtifactsTest(unittest.TestCase):
    def test_emits_only_payload_free_inventory_without_client_inference(self) -> None:
        events = [
            {
                # Canonical events retain only the transport case relation;
                # the sidecar uses it as the asserted catalog case identity.
                "transport_case_id": "phase4_first_byte_before_response_end",
                "transaction_id": "tx-one",
                "negotiated_protocol": "h2",
                "stream_id": 3,
                "phase": 4,
                "rule_id": 1100301,
                "event": "phase4_intervention",
                "message_id": "MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200",
                "requested_action": "deny",
                "actual_action": "stream_reset",
                "transport_result": "stream_reset",
                "response_committed": True,
                "client_disconnected": True,
                "stream_reset": True,
                "cancelled": True,
                "eos_seen": True,
                "transaction_started": True,
                "transaction_finished": True,
                "transaction_destroyed": True,
                "request_body_finished": True,
                "response_body_finished": True,
                "intentional_abort": True,
                "host_survived": True,
                "followup_request_result": "completed",
                "cleanup_reason": "strict_abort",
                "first_byte_before_response_end": True,
                "client_first_byte_received": True,
                "upstream_paused": True,
                "upstream_eos_sent_at_first_byte": False,
                "first_chunk_size": 11,
            }
        ]
        observations, lifecycle, barriers, counters = artifacts.build_artifacts("nginx", "run-1", events)
        self.assertEqual("run-1", observations["run_id"])
        self.assertEqual("not_observable", observations["observations"][0]["client_result"])
        self.assertTrue(observations["observations"][0]["host_survived"])
        self.assertEqual(
            "phase4_first_byte_before_response_end",
            observations["observations"][0]["case_id"],
        )
        self.assertEqual(1, counters["stream_resets"])
        self.assertEqual(1, counters["client_disconnects"])
        self.assertEqual(1, len(barriers))
        self.assertEqual("nginx", barriers[0]["connector"])
        self.assertEqual("run-1", barriers[0]["run_id"])
        self.assertNotIn("case_id", barriers[0])
        self.assertNotIn("protocol", barriers[0])
        self.assertFalse(barriers[0]["upstream_eos_sent_at_first_byte"])
        self.assertEqual(1, len(lifecycle["records"]))
        self.assertEqual(1, lifecycle["records"][0]["intentional_abort"])
        self.assertNotIn("body", json.dumps(observations))

    def test_barrier_record_is_accepted_as_a_framework_canonical_event(self) -> None:
        event = {
            "transport_case_id": "phase4_first_byte_before_response_end",
            "transaction_id": "tx-barrier",
            "negotiated_protocol": "h2",
            "stream_id": 3,
            "phase": 4,
            "rule_id": 1100301,
            "event": "phase4_intervention",
            "message_id": "MSCONN_EVENT_PHASE4",
            "requested_action": "deny",
            "actual_action": "stream_reset",
            "transport_result": "stream_reset",
            "response_committed": True,
            "client_first_byte_received": True,
            "first_byte_before_response_end": True,
            "upstream_paused": True,
            "upstream_eos_sent_at_first_byte": False,
        }
        barrier = artifacts.barrier_record(
            event, "nginx", "native-nginx-http-module", "run-barrier"
        )
        self.assertIsNotNone(barrier)
        framework_ci = ROOT / "modules" / "ModSecurity-test-Framework" / "ci" / "checks" / "catalog"
        framework_runners = ROOT / "modules" / "ModSecurity-test-Framework" / "tests" / "runners"
        probe = (
            "import json, sys; "
            "sys.path[:0] = [sys.argv[1], sys.argv[2]]; "
            "import no_crs_baseline as no_crs; "
            "errors = no_crs.canonical_event_errors(json.loads(sys.argv[3]), 'barrier', "
            "'nginx', 'native-nginx-http-module'); "
            "print('\\n'.join(errors)); raise SystemExit(bool(errors))"
        )
        completed = subprocess.run(
            [
                sys.executable,
                "-c",
                probe,
                str(framework_ci),
                str(framework_runners),
                json.dumps(barrier),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, completed.returncode, completed.stderr + completed.stdout)

    def test_h3_connection_id_is_retained_only_as_a_hash(self) -> None:
        base = {
            "transport_case_id": "h3-case",
            "transaction_id": "tx-h3",
            "negotiated_protocol": "h3",
            "stream_id": 1,
            "phase": 4,
            "event": "phase4",
            "message_id": "MSCONN_EVENT",
            "rule_id": 1100301,
            "requested_action": "deny",
            "actual_action": "stream_reset",
            "transport_result": "stream_reset",
            "host_survived": True,
            "followup_request_result": "completed",
        }
        raw_observations, _lifecycle, _barriers, _counters = artifacts.build_artifacts(
            "nginx", "run-h3", [{**base, "connection_id": "raw-quic-cid"}]
        )
        hashed_observations, _lifecycle, _barriers, _counters = artifacts.build_artifacts(
            "nginx", "run-h3", [{**base, "connection_id": "sha256:0123456789abcdef"}]
        )
        self.assertIsNone(raw_observations["observations"][0]["connection_id"])
        self.assertEqual(
            "sha256:0123456789abcdef",
            hashed_observations["observations"][0]["connection_id"],
        )

    def test_rejects_payload_bearing_source_event(self) -> None:
        with tempfile.TemporaryDirectory(prefix="transport-lifecycle-") as temporary:
            root = Path(temporary)
            source = root / "events.jsonl"
            source.write_text('{"transaction_id":"tx","response_body":"secret"}\n', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "forbidden payload metadata"):
                artifacts.load_events(source)

    def test_effective_config_keeps_only_hashes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="transport-config-") as temporary:
            root = Path(temporary)
            source = root / "runtime.conf"
            source.write_text("secret-looking but never copied\n", encoding="utf-8")
            output = root / "effective-config"
            artifacts.write_effective_config(
                output,
                "apache",
                "run-one",
                [f"runtime.conf={source}"],
            )
            manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual("run-one", manifest["run_id"])
            self.assertEqual(
                hashlib.sha256(source.read_bytes()).hexdigest(),
                manifest["files"][0]["sha256"],
            )
            self.assertNotIn("secret-looking", (output / "manifest.json").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
