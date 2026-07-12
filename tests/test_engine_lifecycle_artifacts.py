from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
WRITER = ROOT / "ci/runtime/lifecycle/write-engine-lifecycle-artifacts.py"


class EngineLifecycleArtifactsTest(unittest.TestCase):
    def run_writer(
        self,
        root: Path,
        events: list[dict[str, object]],
        *,
        output: Path | None = None,
        library_symlink: bool = False,
        transport_lifecycle_records: list[dict[str, object]] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        source = root / "source-result.json"
        source.write_text(json.dumps({"transaction_ids": ["tx-one", "tx-two"]}), encoding="utf-8")
        event_file = root / "events.jsonl"
        event_file.write_text(
            "".join(json.dumps(event) + "\n" for event in events), encoding="utf-8"
        )
        rules = root / "rules.conf"
        rules.write_text("SecRuleEngine On\n", encoding="utf-8")
        library = root / "libmodsecurity.so"
        library_payload = b"current-engine-library"
        if library_symlink:
            target = root / "libmodsecurity.so.3"
            target.write_bytes(library_payload)
            library.symlink_to(target.name)
        else:
            library.write_bytes(library_payload)
        result_dir = output or root / "engine-artifacts"
        command = [
            sys.executable,
            str(WRITER),
            "--connector",
            "envoy",
            "--source-result",
            str(source),
            "--source-events",
            str(event_file),
            "--rules-file",
            str(rules),
            "--libmodsecurity-version",
            "git:abc;build:def",
            "--libmodsecurity-library",
            str(library),
            "--stage-exit-code",
            "0",
        ]
        if transport_lifecycle_records is not None:
            transport_lifecycle = root / "connection-lifecycle.json"
            transport_lifecycle.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "connector": "envoy",
                        "integration_mode": "ext_proc",
                        "run_id": "run-one",
                        "records": transport_lifecycle_records,
                    }
                ),
                encoding="utf-8",
            )
            command.extend(["--transport-lifecycle", str(transport_lifecycle)])
        command.extend(["--output-dir", str(result_dir)])
        return subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
        )

    def test_writes_payload_free_current_host_inventory(self) -> None:
        with tempfile.TemporaryDirectory(prefix="engine-lifecycle-artifacts-") as temporary:
            root = Path(temporary)
            completed = self.run_writer(
                root,
                [
                    {"transaction_id": "tx-one", "phase": 2, "status": "blocked"},
                    {"transaction_id": "tx-one", "phase": 4, "status": "blocked", "actual_action": "abort_connection"},
                    {
                        "transaction_id": "tx-one",
                        "phase": 4,
                        "transport_result": "stream_reset",
                        "stream_reset": True,
                        "client_disconnected": True,
                        "cancelled": True,
                        "timeout_stage": "response_body",
                        "write_result": "short_write",
                        "cleanup_reason": "strict_abort",
                    },
                    {
                        "transaction_id": "tx-two",
                        "phase": 3,
                        "transport_result": "upstream_reset",
                        "upstream_disconnected": True,
                        "write_result": "write_would_block",
                        "cleanup_reason": "cancelled",
                    },
                    {"transaction_id": "tx-two", "phase": 3, "status": "blocked"},
                    {"transaction_id": "tx-two", "phase": 3, "status": "blocked"},
                ],
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            output = root / "engine-artifacts"
            self.assertEqual("git:abc;build:def\n", (output / "engine-version.txt").read_text(encoding="utf-8"))
            self.assertEqual(
                hashlib.sha256(b"current-engine-library").hexdigest(),
                (output / "engine-library-sha256.txt").read_text(encoding="utf-8").strip(),
            )
            self.assertEqual(
                hashlib.sha256(b"SecRuleEngine On\n").hexdigest(),
                (output / "ruleset-sha256.txt").read_text(encoding="utf-8").strip(),
            )
            counts = json.loads((output / "transaction-counts.json").read_text(encoding="utf-8"))
            lifecycle = json.loads((output / "lifecycle-counters.json").read_text(encoding="utf-8"))
            self.assertEqual(["tx-one", "tx-two"], counts["transaction_ids"])
            self.assertEqual(2, counts["transactions_observed"])
            self.assertEqual(5, counts["unique_engine_events_observed"])
            self.assertEqual(2, lifecycle["transactions_started"])
            self.assertEqual(2, lifecycle["transactions_finished"])
            self.assertEqual(2, lifecycle["transactions_destroyed"])
            self.assertEqual(1, lifecycle["request_body_finishes"])
            self.assertEqual(1, lifecycle["response_body_finishes"])
            self.assertEqual(1, lifecycle["intentional_aborts"])
            self.assertEqual(1, lifecycle["client_disconnects"])
            self.assertEqual(1, lifecycle["upstream_disconnects"])
            self.assertEqual(1, lifecycle["stream_resets"])
            self.assertEqual(1, lifecycle["timeouts"])
            self.assertEqual(1, lifecycle["short_writes"])
            self.assertEqual(1, lifecycle["write_would_block"])
            self.assertEqual(1, lifecycle["cleanup_cancel"])
            self.assertEqual(1, lifecycle["cleanup_abort"])
            self.assertEqual(0, lifecycle["cleanup_normal"])
            self.assertFalse(lifecycle["transport_counters_bound"])
            self.assertNotIn("secret", json.dumps(lifecycle))

    def test_uses_causal_lifecycle_records_for_bound_transport_counters(self) -> None:
        with tempfile.TemporaryDirectory(prefix="engine-lifecycle-artifacts-") as temporary:
            root = Path(temporary)
            record = {
                "transaction_id": "tx-one",
                "transport_case_id": "phase4_strict_http1_client_abort",
                "transaction_started": 1,
                "transaction_finished": 1,
                "transaction_destroyed": 1,
                "request_body_finished": 1,
                "response_body_finished": 1,
                "eos_seen": 0,
                "intentional_abort": 1,
                "client_disconnect": 1,
                "upstream_disconnect": 0,
                "stream_reset": 0,
                "timeout": 0,
                "short_writes": 1,
                "write_would_block": 0,
                "cleanup_reason": "strict_abort",
            }
            completed = self.run_writer(
                root,
                [
                    {
                        "transaction_id": "tx-one",
                        "phase": 4,
                        "actual_action": "abort_connection",
                        "intentional_abort": True,
                    },
                    {
                        "transaction_id": "tx-two",
                        "phase": 3,
                        "actual_action": "abort_connection",
                        "intentional_abort": True,
                    },
                ],
                transport_lifecycle_records=[record],
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            lifecycle = json.loads(
                (root / "engine-artifacts/lifecycle-counters.json").read_text(encoding="utf-8")
            )
            self.assertTrue(lifecycle["transport_counters_bound"])
            self.assertEqual(1, lifecycle["request_body_finishes"])
            self.assertEqual(1, lifecycle["response_body_finishes"])
            self.assertEqual(1, lifecycle["intentional_aborts"])
            self.assertEqual(1, lifecycle["client_disconnects"])
            self.assertEqual(1, lifecycle["short_writes"])
            self.assertEqual(1, lifecycle["cleanup_abort"])

    def test_bound_upstream_disconnect_counts_as_cancel_cleanup(self) -> None:
        with tempfile.TemporaryDirectory(prefix="engine-lifecycle-artifacts-") as temporary:
            root = Path(temporary)
            record = {
                "transaction_id": "tx-one",
                "transport_case_id": "upstream-disconnect",
                "transaction_started": 1,
                "transaction_finished": 1,
                "transaction_destroyed": 1,
                "request_body_finished": 0,
                "response_body_finished": 0,
                "eos_seen": 0,
                "intentional_abort": 0,
                "client_disconnect": 0,
                "upstream_disconnect": 1,
                "stream_reset": 0,
                "timeout": 0,
                "short_writes": 0,
                "write_would_block": 0,
                "cleanup_reason": "upstream_disconnected",
            }
            completed = self.run_writer(
                root,
                [{"transaction_id": "tx-one", "upstream_disconnected": True}],
                transport_lifecycle_records=[record],
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            lifecycle = json.loads(
                (root / "engine-artifacts/lifecycle-counters.json").read_text(encoding="utf-8")
            )
            self.assertEqual(1, lifecycle["upstream_disconnects"])
            self.assertEqual(1, lifecycle["cleanup_cancel"])
            self.assertEqual(0, lifecycle["intentional_aborts"])

    def test_rejects_payload_bearing_event_input(self) -> None:
        with tempfile.TemporaryDirectory(prefix="engine-lifecycle-artifacts-") as temporary:
            root = Path(temporary)
            completed = self.run_writer(
                root,
                [{"transaction_id": "tx-one", "phase": 2, "request_body": "secret"}],
            )
            self.assertNotEqual(0, completed.returncode)
            self.assertIn("forbidden payload metadata", completed.stderr)
            self.assertFalse((root / "engine-artifacts/lifecycle-counters.json").exists())

    def test_hashes_managed_soname_library_target(self) -> None:
        with tempfile.TemporaryDirectory(prefix="engine-lifecycle-artifacts-") as temporary:
            root = Path(temporary)
            completed = self.run_writer(
                root,
                [{"transaction_id": "tx-one", "phase": 1, "status": "blocked"}],
                library_symlink=True,
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertEqual(
                hashlib.sha256(b"current-engine-library").hexdigest(),
                (root / "engine-artifacts/engine-library-sha256.txt").read_text(encoding="utf-8").strip(),
            )


if __name__ == "__main__":
    unittest.main()
