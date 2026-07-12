from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
WRITER = ROOT / "ci/write-engine-lifecycle-artifacts.py"


class EngineLifecycleArtifactsTest(unittest.TestCase):
    def run_writer(
        self,
        root: Path,
        events: list[dict[str, object]],
        *,
        output: Path | None = None,
        library_symlink: bool = False,
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
        return subprocess.run(
            [
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
                "--output-dir",
                str(result_dir),
            ],
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
            self.assertEqual(3, counts["unique_engine_events_observed"])
            self.assertEqual(2, lifecycle["transactions_started"])
            self.assertEqual(2, lifecycle["transactions_finished"])
            self.assertEqual(2, lifecycle["transactions_destroyed"])
            self.assertEqual(1, lifecycle["request_body_finishes"])
            self.assertEqual(1, lifecycle["response_body_finishes"])
            self.assertEqual(1, lifecycle["intentional_aborts"])
            self.assertNotIn("secret", json.dumps(lifecycle))

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
