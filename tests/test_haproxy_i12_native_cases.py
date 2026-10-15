"""Fixture integrity tests; runtime qualification remains an independent step."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "haproxy_i12_native_cases", ROOT / "connectors/haproxy/harness/i12_native_cases.py"
)
CASES = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CASES)
CAPTURE_SPEC = importlib.util.spec_from_file_location(
    "i12_native_capture_registry", ROOT / "ci/runtime/lifecycle/i12/capture_sources.py"
)
CAPTURE = importlib.util.module_from_spec(CAPTURE_SPEC)
CAPTURE_SPEC.loader.exec_module(CAPTURE)
OBSERVER_SPEC = importlib.util.spec_from_file_location(
    "i12_native_observe", ROOT / "connectors/haproxy/harness/i12_native_observe.py"
)
OBSERVER = importlib.util.module_from_spec(OBSERVER_SPEC)
OBSERVER_SPEC.loader.exec_module(OBSERVER)


class NativeFixtureIntegrity(unittest.TestCase):
    def setUp(self):
        Path("/var/tmp/codex/ModSecurity-conector").mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(
            prefix="i12-native-fixture-test-", dir="/var/tmp/codex/ModSecurity-conector"
        )
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.capture = self.base / "capture"
        self.capture.mkdir()
        registry = CAPTURE.Registry()
        for name, digest in CASES.CAPTURE_HASHES.items():
            (self.capture / name).write_bytes(registry.content(digest))

    def make(self, name):
        return CASES.materialize(self.capture, self.base / name, name, CASES.cases()[name])

    def tearDown(self):
        # Fixture sealing is intentional; make only this test's private files
        # writable again so TemporaryDirectory can remove its own artifacts.
        for path in self.base.rglob("*"):
            path.chmod(0o755 if path.is_dir() else 0o644)

    def test_capture_mutation_rejected_before_fixture_creation(self):
        source = self.capture / "launch.py"
        source.write_text(source.read_text() + "\n# changed input\n")
        with self.assertRaisesRegex(ValueError, "immutable capture hash differs"):
            self.make("response-single-chunk")
        self.assertFalse((self.base / "response-single-chunk").exists())

    def test_native_partial_limit_has_independent_prefix_oracle(self):
        record = self.make("response-process-partial")
        launch = (Path(record["source"]) / "launch.py").read_text()
        self.assertIn("SecResponseBodyLimit 16\n", launch)
        self.assertIn("SecResponseBodyLimitAction ProcessPartial", launch)
        prefix_digest = hashlib.sha1(CASES.BASE_RESPONSE[:16]).hexdigest()
        whole_digest = hashlib.sha1(CASES.BASE_RESPONSE).hexdigest()
        self.assertIn("RESPONSE_BODY \"@streq " + prefix_digest, launch)
        self.assertNotIn("RESPONSE_BODY \"@streq " + whole_digest, launch)

    def test_response_deny_excludes_the_health_neighbor(self):
        record = self.make("p3-deny")
        fixture = Path(record["source"])
        self.assertIn("RESPONSE_HEADERS:X-I12-Main", (fixture / "launch.py").read_text())
        self.assertIn("self.path=='/i12-main' else 'neighbor'", (fixture / "backend.py").read_text())

    def test_each_fixture_is_sealed_bound_and_unqualified(self):
        for name in CASES.cases():
            record = self.make(name)
            fixture = Path(record["source"])
            contract = json.loads((fixture / "case-contract.json").read_text())
            self.assertIsNone(contract["full_lifecycle_pass"])
            self.assertTrue(contract["private_host_execution_required"])
            if name in CASES.DIAGNOSTIC_CASES:
                self.assertIsNone(contract["original_id"])
                self.assertFalse(contract["original_obligation_eligible"])
                self.assertTrue(contract["diagnostic_id"].startswith("DIAG::"))
            else:
                self.assertIsNone(contract["diagnostic_id"])
                self.assertTrue(contract["original_obligation_eligible"])
            self.assertEqual(fixture.stat().st_mode & 0o222, 0)
            ledger = json.loads(Path(record["ledger"]).read_text())
            for filename, expected in ledger["files"].items():
                self.assertEqual(hashlib.sha256((fixture / filename).read_bytes()).hexdigest(), expected)
            for filename in ("launch.py", "client.py", "backend.py"):
                compile((fixture / filename).read_text(), filename, "exec")

    def test_fragmented_host_writes_match_independent_client_wire(self):
        wire = b"HTTP/1.1 200 OK\r\nContent-Length: 5\r\n\r\nhello"
        chunks = [wire[:17], wire[17:-3], wire[-3:]]
        writes = [{"actual_result": len(chunk), "positive_output_sha256": hashlib.sha256(chunk).hexdigest()} for chunk in chunks]
        segments, complete = OBSERVER.match_wire_segments(writes, wire)
        self.assertTrue(complete)
        self.assertTrue(all(segment["digest_matches"] for segment in segments))
        # Equal total byte counts do not qualify reordered/damaged output.
        writes[0]["positive_output_sha256"] = "0" * 64
        segments, complete = OBSERVER.match_wire_segments(writes, wire)
        self.assertTrue(complete)
        self.assertFalse(segments[0]["digest_matches"])

    def test_truncated_client_wire_cannot_match_complete_host_write(self):
        writes = [{"actual_result": 5, "positive_output_sha256": hashlib.sha256(b"hello").hexdigest()}]
        segments, complete = OBSERVER.match_wire_segments(writes, b"hell")
        self.assertFalse(complete)
        self.assertFalse(segments[0]["digest_matches"])


if __name__ == "__main__":
    unittest.main()
