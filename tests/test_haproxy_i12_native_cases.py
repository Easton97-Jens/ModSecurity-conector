"""Fixture integrity tests; runtime qualification remains an independent step."""
import hashlib
import ast
import io
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

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
CONTRACT_SPEC = importlib.util.spec_from_file_location(
    "i12_native_contracts", ROOT / "connectors/haproxy/harness/i12_native_contracts.py"
)
CONTRACTS = importlib.util.module_from_spec(CONTRACT_SPEC)
with patch.dict("sys.modules", {"i12_native_cases": CASES}):
    CONTRACT_SPEC.loader.exec_module(CONTRACTS)


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

    def test_output_rejects_traversal_symlink_ancestors_and_existing_data(self):
        target = self.base / "output"
        created = CASES.fresh_output(target)
        self.assertEqual(created.stat().st_mode & 0o777, 0o700)
        sentinel = created / "sentinel"
        sentinel.write_text("preserve")
        with self.assertRaises(FileExistsError):
            CASES.fresh_output(target)
        self.assertEqual(sentinel.read_text(), "preserve")
        link = self.base / "link"
        link.symlink_to(target, target_is_directory=True)
        through_link = link / "child"
        with self.assertRaises(ValueError):
            CASES.fresh_output(through_link)
        traversal = self.base / ".." / "escape"
        with self.assertRaises(ValueError):
            CASES.fresh_output(traversal)
        self.assertFalse((target / "child").exists())

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

    def test_canonical_source_request_keeps_duplicate_headers_and_exact_original_id(self):
        name = "duplicate_header_names"
        catalog = {name: {"request": {"method": "GET", "path": "/no-crs/headers/duplicate",
                    "headers": [{"name": "X-No-Crs-Duplicate", "value": "one"},
                                {"name": "X-No-Crs-Duplicate", "value": "two"}]}, "expected_status": 200}}
        case, document = CONTRACTS.canonical_case(name, catalog, self.base, "")
        self.assertIsNone(document)
        expected_headers = b"X-No-Crs-Duplicate: one\r\nX-No-Crs-Duplicate: two\r\n"
        self.assertIn(expected_headers, case["request_wire"])
        original = "I12::haproxy-native-htx::duplicate_header_names"
        case["original_id"] = original
        case["original_requirement_binding"] = {"selected_requirement_sha256": "a" * 64}
        record = CASES.materialize(self.capture, self.base / name, name, case)
        fixture = Path(record["source"])
        contract = json.loads((fixture / "case-contract.json").read_text())
        self.assertEqual(contract["original_id"], original)
        self.assertEqual(contract["request_method"], "GET")
        self.assertEqual(contract["request_path"], "/no-crs/headers/duplicate")
        self.assertIsNone(contract["full_lifecycle_pass"])
        self.assertIn("do_GET = do_POST", (fixture / "backend.py").read_text())

    def test_declarative_chunk_lengths_are_not_replaced_by_default_eights(self):
        case = CASES.cases()["request-streaming"]
        case["request"] = b"no-crs-request-body-marker"
        case["request_chunk_sizes"] = [15, len(case["request"]) - 15]
        record = CASES.materialize(self.capture, self.base / "source-chunks", "source-chunks", case)
        client = (Path(record["source"]) / "client.py").read_text()
        self.assertIn("body[:15],body[15:]", client)
        self.assertNotIn("body[:8],body[8:]", client)

    def test_missing_main_allocation_does_not_borrow_the_neighbor(self):
        client = {"started_wall_ns": 10, "completed_wall_ns": 20}
        contract = {"original_requirement_binding": {}}
        neighbor = {"wall_ns": 30, "allocation_scope_call": 4}
        self.assertIsNone(OBSERVER.select_main_allocation([neighbor], client, contract))
        actual_main = {"wall_ns": 15, "allocation_scope_call": 1}
        self.assertEqual(OBSERVER.select_main_allocation([actual_main, neighbor], client, contract), actual_main)
        ambiguous = [actual_main, {"wall_ns": 16, "allocation_scope_call": 2}]
        with self.assertRaisesRegex(ValueError, "ambiguous"):
            OBSERVER.select_main_allocation(ambiguous, client, contract)

    def test_replaced_inventory_and_source_reuse_cycles_fail_before_preparation(self):
        inventory = {"rows": []}
        with self.assertRaisesRegex(ValueError, "inventory identity differs"):
            CONTRACTS.native_rows(inventory)
        catalog = {"a": {"request": {"reuses": "b"}}, "b": {"request": {"reuses": "a"}}}
        with self.assertRaisesRegex(ValueError, "reuse cycle"):
            CONTRACTS.resolve_request("a", catalog)

    def test_source_barrier_waits_for_actual_client_body_and_rejects_changed_chunks(self):
        response = b"first-byte-prefix no-crs-response-body-marker"
        case = CASES.cases()["response-single-chunk"]
        case["response"] = response
        case["request_path"] = "/i12-main"
        lifecycle = {"synchronization": {"upstream_waits_for_test_barrier": True}}
        CONTRACTS.apply_source_chunks(case, lifecycle, case["request"], response)
        record = CASES.materialize(self.capture, self.base / "causal-barrier", "causal-barrier", case)
        client = (Path(record["source"]) / "client.py").read_text()
        backend = (Path(record["source"]) / "backend.py").read_text()
        self.assertIn("data.split(b'\\r\\n\\r\\n',1)[1]", client)
        self.assertIn("source':'actual_SSLSocket_recv_body_before_backend_release'", client)
        self.assertLess(backend.index("self.wfile.write(prefix)"), backend.index("while not barrier.exists()"))
        self.assertLess(backend.index("while not barrier.exists()"), backend.index("self.wfile.write(response[len(prefix):])"))
        changed = {"request_chunks": ["wrong", "source"]}
        with self.assertRaisesRegex(ValueError, "chunks differ"):
            CONTRACTS.apply_source_chunks({}, changed, case["request"], response)

    def test_common_sink_requires_exact_transaction_identity_and_keeps_other_rows(self):
        sink = self.base / "common-events.jsonl"
        rows = [{"transaction_id": "main", "event": "observed"},
                {"transaction_id": "neighbor", "event": "observed"},
                {"transaction_id": None, "event": "unassociated"}]
        sink.write_text("".join(json.dumps(row) + "\n" for row in rows))
        observed = OBSERVER.common_sink_rows(sink, "main", None)
        self.assertEqual(observed["all_physical_rows"], rows)
        self.assertEqual(observed["exact_main_transaction_rows"], [rows[0]])
        absent = OBSERVER.common_sink_rows(sink, None, None)
        self.assertEqual(absent["exact_main_transaction_rows"], [])

    def test_canonical_p3_response_marker_is_never_added_to_health_neighbor(self):
        case = CASES.cases()["response-single-chunk"]
        case["request_path"] = "/no-crs/full-lifecycle/response-header-deny"
        case["request_method"] = "GET"
        case["response_headers"] = [{"name": "X-Modsec-Upstream", "value": "block"}]
        record = CASES.materialize(self.capture, self.base / "p3-neighbor", "p3-neighbor", case)
        source = (Path(record["source"]) / "backend.py").read_text()
        handler = next(node for node in ast.parse(source).body if isinstance(node, ast.ClassDef) and node.name == "Handler")
        namespace = {"BaseHTTPRequestHandler": object, "hashlib": hashlib, "json": json,
                     "time": __import__("time"), "Path": lambda value: self.base / Path(value).name}
        exec(compile(ast.Module(body=[handler], type_ignores=[]), "p3-backend-handler", "exec"), namespace)
        for path, expected in ((case["request_path"], True), ("/i12-neighbor", False)):
            request = namespace["Handler"]()
            request.path, request.command = path, "GET"
            request.headers, request.rfile, request.wfile = {"Content-Length": "0"}, io.BytesIO(), io.BytesIO()
            emitted = []
            request.send_response = lambda status: None
            request.send_header = lambda name, value: emitted.append((name, value))
            request.end_headers = lambda: None
            request.do_GET()
            self.assertEqual(("X-Modsec-Upstream", "block") in emitted, expected)
            if not expected:
                self.assertEqual(request.wfile.getvalue(), b"healthy\n")


if __name__ == "__main__":
    unittest.main()
