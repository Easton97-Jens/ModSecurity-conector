from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "write_hostruntime_record", ROOT / "ci/runtime/lifecycle/write-hostruntime-record.py"
)
assert SPEC is not None and SPEC.loader is not None
writer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(writer)


class HostRuntimeRecordTest(unittest.TestCase):
    def write_result(self, directory: Path, payload: dict[str, object]) -> Path:
        path = directory / "result.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def invoke(self, result: Path, output: Path, summary: Path) -> dict[str, object]:
        self.assertEqual(writer.main([
            "--result", str(result), "--output", str(output), "--summary", str(summary),
            "--connector", "haproxy", "--profile", "native-htx",
            "--runtime-lock-id", "haproxy-htx-3.2.21",
            "--expected-version", "3.2.21", "--actual-version", "3.2.21",
            "--timestamp", "2026-08-14T00:00:00Z",
        ]), 0)
        return json.loads(output.read_text(encoding="utf-8"))

    def complete(self) -> dict[str, object]:
        return {
            "status": "PASS",
            "hostruntime_evidence": {
                "host_process_verified": True,
                "config_loaded": True,
                "readiness_verified": True,
                "real_interaction": True,
                "result_verified": True,
                "cleanup_verified": True,
            },
        }

    def test_complete_record_is_pass(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            record = self.invoke(self.write_result(root, self.complete()), root / "record.json", root / "summary.md")
            self.assertEqual(record["status"], "PASS")
            self.assertEqual(record["evidence"]["interaction"], "PASS")

    def test_incomplete_record_cannot_pass(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            result = self.complete()
            del result["hostruntime_evidence"]["cleanup_verified"]
            record = self.invoke(self.write_result(root, result), root / "record.json", root / "summary.md")
            self.assertEqual(record["status"], "BLOCKED")
            self.assertIn("cleanup", record["reason"])

    def test_blocked_source_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            result = self.complete()
            result["hostruntime_evidence"]["readiness_verified"] = "BLOCKED"
            record = self.invoke(self.write_result(root, result), root / "record.json", root / "summary.md")
            self.assertEqual(record["status"], "BLOCKED")

    def test_body_safe_existing_result_fields_are_not_copied(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            result = self.complete()
            result["request_body_verified"] = True
            result["body_payload_absent_from_events"] = True
            result["response_body"] = "sensitive-payload"
            record = self.invoke(self.write_result(root, result), root / "record.json", root / "summary.md")
            self.assertEqual(record["status"], "PASS")
            serialized = json.dumps(record)
            self.assertNotIn("sensitive-payload", serialized)
            self.assertNotIn("request_body_verified", serialized)

    def test_existing_result_and_unsafe_versions_do_not_break_projection(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            result = self.complete()
            del result["hostruntime_evidence"]["readiness_verified"]
            source = self.write_result(root, result)
            output = root / "record.json"
            self.assertEqual(writer.main([
                "--result", str(source), "--output", str(output),
                "--connector", "haproxy", "--profile", "native-htx",
                "--expected-version", "HAProxy /usr/local/bin/haproxy",
                "--actual-version", "HAProxy /tmp/host runtime",
            ]), 0)
            record = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(record["status"], "BLOCKED")
            self.assertIsNone(record["expected_version"])
            self.assertIsNone(record["actual_version"])

    def test_source_fail_with_incomplete_host_evidence_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            result = self.complete()
            result["status"] = "FAIL"
            del result["hostruntime_evidence"]["cleanup_verified"]
            record = self.invoke(self.write_result(root, result), root / "record.json", root / "summary.md")
            self.assertEqual(record["status"], "BLOCKED")
            self.assertIn("incomplete_hostruntime_evidence", record["reason"])

    def test_source_fail_with_complete_evidence_remains_fail(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            result = self.complete()
            result["status"] = "FAIL"
            record = self.invoke(self.write_result(root, result), root / "record.json", root / "summary.md")
            self.assertEqual(record["status"], "FAIL")

    def test_status_schema_is_bounded(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            record = self.invoke(self.write_result(root, self.complete()), root / "record.json", root / "summary.md")
            self.assertIn(record["status"], writer.STATUS_VALUES)
            self.assertNotIn("response_body", json.dumps(record))
            self.assertNotIn("/tmp", json.dumps(record))

    def test_runner_writes_projection_after_finalization(self) -> None:
        runner = (ROOT / "ci/runtime/lifecycle/run-no-crs-baseline.sh").read_text(encoding="utf-8")
        self.assertIn("write-hostruntime-record.py", runner)
        self.assertIn("FINAL_RESULT=", runner)
        self.assertIn('if [ "$finalize_rc" -ne 0 ]; then', runner)
        self.assertLess(runner.index("FINAL_RESULT="), runner.index("latest_file="))


if __name__ == "__main__":
    unittest.main()
