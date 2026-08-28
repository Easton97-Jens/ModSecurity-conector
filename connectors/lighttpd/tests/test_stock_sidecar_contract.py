"""Loopback component coverage for the canonical Stock-lighttpd sidecar.

This deliberately talks raw HTTP/1.1 to the C process.  It is not a
replacement for a Stock lighttpd host run: the sidecar itself is the selected
traffic-owning implementation for the named Stock solution, while the native
Stock module remains an explicit P1/P3-only compatibility translation.
"""

from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import socket
import socketserver
import struct
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[3]
SIDECAR_SOURCE = ROOT / "connectors/lighttpd/stock_sidecar/stock_sidecar.c"
REAL_BACKEND_HARNESS = ROOT / "connectors/lighttpd/harness/run_stock_sidecar_real_backend.py"
BEGIN_SMOKE_SOURCE = ROOT / "connectors/lighttpd/stock_sidecar/runtime_begin_smoke.c"
BUILD_SCRIPT = ROOT / "connectors/lighttpd/build/build_stock_sidecar.sh"
COMMON_RUNTIME = ROOT / "common/runtime/msconnector_runtime.c"
PROFILE_REGISTRY = ROOT / "connectors/profile_registry.c"


def _load_real_backend_harness():
    module_name = "stock_sidecar_real_backend_contract_test"
    spec = importlib.util.spec_from_file_location(module_name, REAL_BACKEND_HARNESS)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load the Stock real-backend harness")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop(module_name, None)
    return module


def _strict_stock_event(harness, *, message_id: str, transaction_id: str,
                        sequence: int, previous_hash: int, phase: str,
                        actual_action: str, requested_action: str = "deny",
                        transport_result: str = "", visible_http_status: int = 0,
                        original_http_status: int = 0,
                        response_committed: bool = False,
                        rule_id: str = "", event_name: str | None = None) -> dict[str, object]:
    record: dict[str, object] = {
        "timestamp": "2026-08-27T00:00:00Z",
        "level": "warning",
        "message_id": message_id,
        "message": "bounded event",
        "event": event_name or message_id,
        "connector": "lighttpd",
        "integration_mode": "stock-lighttpd-sidecar",
        "transaction_id": transaction_id,
        "phase": phase,
        "status": "blocked",
        "action": requested_action,
        "requested_action": requested_action,
        "actual_action": actual_action,
        "http_status": visible_http_status,
        "original_http_status": original_http_status,
        "visible_http_status": visible_http_status,
        "transport_result": transport_result,
        "http_reason_phrase": "",
        "http_default_message": "",
        "rule_id": rule_id,
        "reason": "bounded reason",
        "method": "GET",
        "uri": "/verified",
        "client_ip": "127.0.0.1",
        "content_type": "",
        "body_bytes_seen": 0,
        "body_bytes_inspected": 0,
        "late_intervention": False,
        "response_started": response_committed,
        "response_committed": response_committed,
        "headers_sent": response_committed,
        "body_started": response_committed,
        "body_truncated": False,
        "connection_aborted": False,
        "client_disconnected": False,
        "upstream_disconnected": False,
        "cancelled": False,
        "eos_seen": True,
        "redacted": True,
        "truncated": False,
        "sequence": sequence,
        "previous_event_hash": previous_hash,
        "event_hash": 0,
    }
    record["event_hash"] = harness.event_integrity_hash(record, previous_hash)
    return record


COMMON_SOURCES = sorted((ROOT / "common/src").glob("*.c"))


def _temporary_root() -> str | None:
    candidate = os.environ.get("MSCONNECTOR_TEST_TMPDIR") or os.environ.get("TMPDIR")
    return candidate if candidate and Path(candidate).is_dir() else None


def _free_loopback_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


def _status(response: bytes) -> int:
    first_line = response.split(b"\r\n", 1)[0].split()
    if len(first_line) < 2:
        raise AssertionError(f"response has no HTTP status line: {response!r}")
    return int(first_line[1])


def _content_length(header_block: bytes) -> int:
    for line in header_block.split(b"\r\n")[1:]:
        name, separator, value = line.partition(b":")
        if separator and name.lower() == b"content-length":
            return int(value.strip())
    return 0


class _RecordingUpstream(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, responder):
        self.records: list[bytes] = []
        self.records_lock = threading.Lock()
        self.responder = responder
        super().__init__(("127.0.0.1", 0), _RecordingUpstreamHandler)

    def record(self, request: bytes) -> None:
        with self.records_lock:
            self.records.append(request)

    def record_count(self) -> int:
        with self.records_lock:
            return len(self.records)


class _RecordingUpstreamHandler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        self.request.settimeout(3.0)
        data = bytearray()
        try:
            while b"\r\n\r\n" not in data:
                chunk = self.request.recv(4096)
                if not chunk:
                    return
                data.extend(chunk)
                if len(data) > 128 * 1024:
                    return
            header_end = data.index(b"\r\n\r\n") + 4
            expected = _content_length(bytes(data[:header_end]))
            while len(data) - header_end < expected:
                chunk = self.request.recv(4096)
                if not chunk:
                    return
                data.extend(chunk)
            self.server.record(bytes(data))
            response = self.server.responder(bytes(data))
            if response:
                self.request.sendall(response)
        except (OSError, ValueError):
            return


@contextlib.contextmanager
def _upstream(responder):
    server = _RecordingUpstream(responder)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield server
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3.0)


class _RunningSidecar:
    def __init__(self, binary: Path, config: Path, upstream_port: int, library_dir: Path,
                 timeout_ms: int, environment: dict[str, str] | None = None) -> None:
        self.port = _free_loopback_port()
        self.config = config
        self.process: subprocess.Popen[bytes] | None = None
        self._command = [
            str(binary),
            "--config", str(config),
            "--listen", f"127.0.0.1:{self.port}",
            "--upstream", f"127.0.0.1:{upstream_port}",
            "--timeout-ms", str(timeout_ms),
        ]
        self._environment = os.environ.copy()
        original_path = self._environment.get("LD_LIBRARY_PATH", "")
        self._environment["LD_LIBRARY_PATH"] = (
            f"{library_dir}:{original_path}" if original_path else str(library_dir)
        )
        if environment is not None:
            self._environment.update(environment)

    def __enter__(self) -> "_RunningSidecar":
        self.process = subprocess.Popen(
            self._command,
            cwd=ROOT,
            env=self._environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        if self.process is None:
            return
        if self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.communicate(timeout=3.0)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.communicate(timeout=3.0)
        self.process = None

    def connect(self) -> socket.socket:
        deadline = time.monotonic() + 3.0
        last_error: OSError | None = None
        while time.monotonic() < deadline:
            if self.process is not None and self.process.poll() is not None:
                stdout, stderr = self.process.communicate()
                raise AssertionError(
                    f"sidecar exited early ({self.process.returncode}): "
                    f"stdout={stdout!r} stderr={stderr!r}"
                )
            try:
                client = socket.create_connection(("127.0.0.1", self.port), timeout=0.2)
                client.settimeout(3.0)
                return client
            except OSError as error:
                last_error = error
                time.sleep(0.02)
        raise AssertionError(f"sidecar did not accept loopback clients: {last_error}")

    def exchange(self, request: bytes) -> bytes:
        with self.connect() as client:
            client.sendall(request)
            response = bytearray()
            while True:
                chunk = client.recv(4096)
                if not chunk:
                    return bytes(response)
                response.extend(chunk)


class StockSidecarSourceContractTest(unittest.TestCase):
    def test_real_backend_event_selection_separates_engine_and_host_action(self) -> None:
        harness = _load_real_backend_harness()
        case = next(candidate for candidate in harness.REAL_BACKEND_CASES
                    if candidate.name == "p1_deny")
        transaction_id = "sidecar-host-action-test"
        engine_event = _strict_stock_event(
            harness, message_id=case.expected_engine_event or "", transaction_id=transaction_id,
            sequence=1, previous_hash=0, phase="request_headers", actual_action="deny",
            rule_id=case.expected_rule_id or "",
        )
        host_action_event = _strict_stock_event(
            harness, message_id=case.expected_host_action_event or "", transaction_id=transaction_id,
            sequence=2, previous_hash=int(engine_event["event_hash"]), phase="request_headers",
            actual_action=case.expected_actual_action or "deny",
            transport_result=case.expected_transport_result or "",
            visible_http_status=case.expected_status,
            response_committed=case.expected_response_committed,
            rule_id=case.expected_rule_id or "",
        )
        receipt = {
            "transaction_id_sha256": hashlib.sha256(
                transaction_id.encode("utf-8")
            ).hexdigest(),
        }
        with tempfile.TemporaryDirectory(prefix="stock-host-action-selection-",
                                         dir=_temporary_root()) as temporary:
            events = Path(temporary) / "events.jsonl"
            events.write_text(
                "\n".join(json.dumps(value) for value in (engine_event, host_action_event)) + "\n",
                encoding="utf-8",
            )
            events.chmod(0o600)
            selected = harness.select_host_action_event(events, case, receipt)
            duplicate = _strict_stock_event(
                harness, message_id=case.expected_host_action_event or "",
                transaction_id=transaction_id, sequence=3,
                previous_hash=int(host_action_event["event_hash"]), phase="request_headers",
                actual_action=case.expected_actual_action or "deny",
                transport_result=case.expected_transport_result or "",
                visible_http_status=case.expected_status,
                response_committed=case.expected_response_committed,
                rule_id=case.expected_rule_id or "",
            )
            events.write_text(
                "\n".join(json.dumps(value) for value in (
                    engine_event, host_action_event, duplicate,
                )) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(RuntimeError, "duplicate host-action events"):
                harness.select_host_action_event(events, case, receipt)
        self.assertEqual(selected["actual_host_action"], case.expected_actual_action)
        self.assertEqual(selected["transport_result"], case.expected_transport_result)
        self.assertEqual(selected["rule_id"], case.expected_rule_id)

    def test_real_backend_event_selection_requires_causal_engine_event(self) -> None:
        harness = _load_real_backend_harness()
        case = next(candidate for candidate in harness.REAL_BACKEND_CASES
                    if candidate.name == "p1_deny")
        transaction_id = "sidecar-reverse-causal-test"
        host_action_event = _strict_stock_event(
            harness, message_id=case.expected_host_action_event or "", transaction_id=transaction_id,
            sequence=1, previous_hash=0, phase="request_headers",
            actual_action=case.expected_actual_action or "deny",
            transport_result=case.expected_transport_result or "",
            visible_http_status=case.expected_status,
            response_committed=case.expected_response_committed,
            rule_id=case.expected_rule_id or "",
        )
        engine_event = _strict_stock_event(
            harness, message_id=case.expected_engine_event or "", transaction_id=transaction_id,
            sequence=2, previous_hash=int(host_action_event["event_hash"]), phase="request_headers",
            actual_action="deny", rule_id=case.expected_rule_id or "",
        )
        receipt = {
            "transaction_id_sha256": hashlib.sha256(
                transaction_id.encode("utf-8")
            ).hexdigest(),
        }
        with tempfile.TemporaryDirectory(prefix="stock-reverse-causal-",
                                         dir=_temporary_root()) as temporary:
            events = Path(temporary) / "events.jsonl"
            events.write_text(
                "\n".join(json.dumps(value) for value in (host_action_event, engine_event)) + "\n",
                encoding="utf-8",
            )
            events.chmod(0o600)
            with self.assertRaisesRegex(RuntimeError, "engine event must precede"):
                harness.select_host_action_event(events, case, receipt)

    def test_real_backend_event_selection_preserves_precommit_response_status(self) -> None:
        harness = _load_real_backend_harness()
        p3_case = next(candidate for candidate in harness.REAL_BACKEND_CASES
                       if candidate.name == "p3_deny")
        p4_case = next(candidate for candidate in harness.REAL_BACKEND_CASES
                       if candidate.name == "p4_safe_rate_limit")

        def verify_response_case(case, host_action: str, transport_result: str) -> None:
            transaction_id = f"{case.name}-engine-event"
            engine_event = _strict_stock_event(
                harness, message_id=case.expected_engine_event or "", transaction_id=transaction_id,
                sequence=1, previous_hash=0,
                phase=harness._EVENT_CONTRACT_PHASE_NAMES[case.expected_phase_sequence[-1]],
                actual_action="deny", visible_http_status=200, original_http_status=200,
                response_committed=case.expected_response_committed,
                rule_id=case.expected_rule_id or "",
            )
            host_event = _strict_stock_event(
                harness, message_id=case.expected_host_action_event or "", transaction_id=transaction_id,
                sequence=2, previous_hash=int(engine_event["event_hash"]),
                phase=harness._EVENT_CONTRACT_PHASE_NAMES[case.expected_phase_sequence[-1]],
                actual_action=host_action, transport_result=transport_result,
                visible_http_status=case.expected_status, original_http_status=200,
                response_committed=case.expected_response_committed,
                rule_id=case.expected_rule_id or "",
            )
            if case.expected_phase_sequence[-1] == "P4":
                host_event["late_intervention"] = True
                host_event["late_intervention_mode"] = case.phase4_mode
                host_event["event_hash"] = harness.event_integrity_hash(
                    host_event, int(engine_event["event_hash"])
                )
            self.assertTrue(harness._is_engine_event_candidate(engine_event, case))
            for invalid in (
                {**engine_event, "visible_http_status": 200, "original_http_status": 0},
                {**engine_event, "visible_http_status": 200, "original_http_status": 201},
                {**engine_event, "transport_result": "http_status"},
                {**engine_event, "status": "error"},
                {**engine_event, "action": "error"},
                {**engine_event, "requested_action": "error"},
                {**engine_event, "actual_action": "log_only"},
                {**engine_event, "response_committed": not case.expected_response_committed},
                {**engine_event, "late_intervention": True},
            ):
                self.assertFalse(harness._is_engine_event_candidate(invalid, case))
            receipt = {
                "transaction_id_sha256": hashlib.sha256(
                    transaction_id.encode("utf-8")
                ).hexdigest(),
            }
            with tempfile.TemporaryDirectory(prefix="stock-response-event-selection-",
                                             dir=_temporary_root()) as temporary:
                events = Path(temporary) / "events.jsonl"
                events.write_text(
                    "\n".join(json.dumps(record) for record in (engine_event, host_event)) + "\n",
                    encoding="utf-8",
                )
                events.chmod(0o600)
                selected = harness.select_host_action_event(events, case, receipt)
            self.assertEqual(selected["actual_host_action"], host_action)
            self.assertEqual(selected["transport_result"], transport_result)

        verify_response_case(p3_case, "deny", "http_status")
        verify_response_case(p4_case, "log_only", "log_only")

    def test_real_backend_event_hash_matches_common_p4_vectors(self) -> None:
        harness = _load_real_backend_harness()
        engine_event = {
            "timestamp": "2026-08-27T23:28:19Z",
            "level": "warn",
            "message_id": "MSCONN_EVENT_RESPONSE_BLOCKED",
            "message": "Response blocked by ModSecurity rule.",
            "event": "MSCONN_EVENT_RESPONSE_BLOCKED",
            "connector": "lighttpd",
            "integration_mode": "stock-lighttpd-sidecar",
            "transaction_id": "lighttpd-1",
            "phase": "response_body",
            "status": "blocked",
            "action": "deny",
            "requested_action": "deny",
            "actual_action": "deny",
            "http_status": 429,
            "original_http_status": 200,
            "visible_http_status": 200,
            "transport_result": "",
            "http_reason_phrase": "Too Many Requests",
            "http_default_message": "Too many requests",
            "rule_id": "9821004",
            "reason": "ModSecurity rule requested an intervention",
            "method": "GET",
            "uri": "/p4.txt",
            "client_ip": "",
            "content_type": "text/plain;charset=utf-8",
            "body_bytes_seen": 15,
            "body_bytes_inspected": 15,
            "late_intervention": False,
            "response_started": True,
            "response_committed": True,
            "headers_sent": True,
            "body_started": True,
            "body_truncated": False,
            "connection_aborted": False,
            "client_disconnected": False,
            "upstream_disconnected": False,
            "cancelled": False,
            "eos_seen": False,
            "redacted": False,
            "truncated": False,
            "sequence": 1,
            "previous_event_hash": 0,
            "event_hash": 6976292163263236490,
        }
        self.assertEqual(harness.event_integrity_hash(engine_event, 0), engine_event["event_hash"])
        host_event = {
            **engine_event,
            "actual_action": "log_only",
            "transport_result": "log_only",
            "late_intervention": True,
            "late_intervention_mode": "safe",
            "sequence": 2,
            "previous_event_hash": engine_event["event_hash"],
            "event_hash": 1053947771207529214,
        }
        self.assertEqual(
            harness.event_integrity_hash(host_event, host_event["previous_event_hash"]),
            host_event["event_hash"],
        )

    def test_real_backend_event_schema_allows_body_progress_but_not_payload(self) -> None:
        harness = _load_real_backend_harness()
        progress_event = _strict_stock_event(
            harness, message_id="MSCONN_EVENT_REQUEST_BLOCKED", transaction_id="schema-test",
            sequence=1, previous_hash=0, phase="request_headers", actual_action="deny",
        )
        progress_event["body_limit_outcome"] = "none"
        progress_event["event_hash"] = harness.event_integrity_hash(progress_event, 0)
        with tempfile.TemporaryDirectory(prefix="stock-event-schema-",
                                         dir=_temporary_root()) as temporary:
            events = Path(temporary) / "events.jsonl"
            events.write_text(json.dumps(progress_event) + "\n", encoding="utf-8")
            events.chmod(0o600)
            _raw, records = harness.event_records(events)
            self.assertEqual(records, [progress_event])
            events.write_text(json.dumps({**progress_event, "body_payload": "blocked"}) + "\n",
                              encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "unexpected body field"):
                harness.event_records(events)
            events.write_text(
                json.dumps({**progress_event, "message": "bounded\0event"}) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(RuntimeError, "invalid message"):
                harness.event_records(events)
            events.write_text(
                json.dumps({**progress_event, "run_id": "run\0identifier"}) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(RuntimeError, "invalid run_id"):
                harness.event_records(events)

    def test_real_backend_event_schema_rejects_tampering_and_noncanonical_json(self) -> None:
        harness = _load_real_backend_harness()
        first = _strict_stock_event(
            harness, message_id="MSCONN_EVENT_REQUEST_BLOCKED", transaction_id="event-chain-test",
            sequence=1, previous_hash=0, phase="request_headers", actual_action="deny",
        )
        second = _strict_stock_event(
            harness, message_id="MSCONN_EVENT_REQUEST_BLOCKED", transaction_id="event-chain-test",
            sequence=2, previous_hash=int(first["event_hash"]), phase="request_headers",
            actual_action="deny", transport_result="http_status", visible_http_status=451,
        )
        with tempfile.TemporaryDirectory(prefix="stock-event-integrity-",
                                         dir=_temporary_root()) as temporary:
            events = Path(temporary) / "events.jsonl"

            def write_records(*records: dict[str, object]) -> None:
                events.write_text("\n".join(json.dumps(record) for record in records) + "\n",
                                  encoding="utf-8")
                events.chmod(0o600)

            write_records(first, second)
            self.assertEqual(harness.event_records(events)[1], [first, second])
            altered = {**second, "actual_action": "log_only"}
            write_records(first, altered)
            with self.assertRaisesRegex(RuntimeError, "event hash is invalid"):
                harness.event_records(events)
            wrong_type = {**first, "visible_http_status": "451"}
            write_records(wrong_type)
            with self.assertRaisesRegex(RuntimeError, "invalid visible_http_status"):
                harness.event_records(events)
            unknown = {**first, "opaque_handle": "forbidden"}
            write_records(unknown)
            with self.assertRaisesRegex(RuntimeError, "unknown field"):
                harness.event_records(events)
            events.write_text(
                '{"timestamp":"a","timestamp":"b"}\n', encoding="utf-8"
            )
            events.chmod(0o600)
            with self.assertRaisesRegex(RuntimeError, "event log is malformed"):
                harness.event_records(events)
            write_records(second, first)
            with self.assertRaisesRegex(RuntimeError, "sequence is not contiguous"):
                harness.event_records(events)
            write_records(second)
            with self.assertRaisesRegex(RuntimeError, "sequence is not contiguous"):
                harness.event_records(events)

    def test_real_backend_allow_and_body_limit_evidence_are_fail_closed(self) -> None:
        harness = _load_real_backend_harness()
        allow_case = next(candidate for candidate in harness.REAL_BACKEND_CASES
                          if candidate.name == "allow_full")
        body_limit_case = next(candidate for candidate in harness.REAL_BACKEND_CASES
                               if candidate.name == "p2_body_limit")
        transaction_id = "body-limit-event-test"
        engine_event = _strict_stock_event(
            harness, message_id=body_limit_case.expected_engine_event or "",
            transaction_id=transaction_id, sequence=1, previous_hash=0,
            phase="request_headers", actual_action="deny", requested_action="deny",
            event_name="rule_block",
        )
        host_event = _strict_stock_event(
            harness, message_id=body_limit_case.expected_host_action_event or "",
            transaction_id=transaction_id, sequence=2, previous_hash=int(engine_event["event_hash"]),
            phase="request_headers", actual_action="deny", requested_action="error",
            transport_result="http_status", visible_http_status=413,
        )
        receipt = {
            "transaction_id_sha256": hashlib.sha256(transaction_id.encode("utf-8")).hexdigest(),
        }
        with tempfile.TemporaryDirectory(prefix="stock-event-role-", dir=_temporary_root()) as temporary:
            events = Path(temporary) / "events.jsonl"
            events.write_text(
                "\n".join(json.dumps(record) for record in (engine_event, host_event)) + "\n",
                encoding="utf-8",
            )
            events.chmod(0o600)
            selected = harness.select_host_action_event(events, body_limit_case, receipt)
            self.assertEqual(selected["actual_host_action"], "deny")
            with self.assertRaisesRegex(RuntimeError, "allow case emitted an unexpected event"):
                harness.select_host_action_event(events, allow_case, receipt)

    def test_real_backend_harness_requires_an_unchanged_stock_host(self) -> None:
        source = REAL_BACKEND_HARNESS.read_text(encoding="utf-8")

        self.assertIn('required("STOCK_LIGHTTPD_BIN")', source)
        self.assertIn('required("STOCK_LIGHTTPD_MODULE_DIR")', source)
        self.assertIn('required("MSCONNECTOR_STOCK_SIDECAR_BINARY")', source)
        self.assertIn('required("STOCK_SIDECAR_ARTIFACT_ATTESTATION")', source)
        self.assertIn('required_new_path("STOCK_SIDECAR_RECEIPT_PATH")', source)
        self.assertIn("backend=unchanged-stock-lighttpd", source)
        self.assertIn("traffic_owner=sidecar", source)
        self.assertIn('"evidence_scope": ["real_host", "real_client"]', source)
        self.assertIn("REAL_BACKEND_CASES", source)
        self.assertIn("p1_deny", source)
        self.assertIn("p2_body_limit", source)
        self.assertIn("p3_deny", source)
        self.assertIn("p4_safe_rate_limit", source)
        self.assertIn("_BACKEND_ACCESS_LOG_WAIT_SECONDS = 6.0", source)
        self.assertIn("time.monotonic() + _BACKEND_ACCESS_LOG_WAIT_SECONDS", source)
        self.assertIn('"body_started",', source)
        self.assertIn("Stock lighttpd event contains an unexpected body field", source)
        self.assertIn("read_sidecar_receipt(path, binding, case)", source)
        self.assertIn("publish_verified_receipt", source)
        self.assertIn('"actual_host_action": actual_action', source)
        self.assertIn('"payloads_persisted": False', source)
        self.assertIn('"STOCK_SIDECAR_RECEIPT_BINDING": receipt_binding', source)
        self.assertIn("verify_stock_host_provenance", source)
        self.assertIn("verify_stock_staticfile_linkage", source)
        self.assertIn("verify_sidecar_build_manifest", source)
        self.assertIn("verify_stock_artifact_attestation", source)
        self.assertIn("verify_artifact_path_chain", source)
        self.assertIn("verify_stock_launch_artifacts", source)
        self.assertIn('_EVENT_INTEGRATION_MODE = "stock-lighttpd-sidecar"', source)
        self.assertIn("expected_engine_event", source)
        self.assertIn("expected_host_action_event", source)
        self.assertLess(
            source.index("verify_stock_host_provenance"),
            source.index("host_version(stock_binary)"),
        )
        self.assertLess(
            source.index("verify_stock_staticfile_linkage(stock_binary)"),
            source.index("host_version(stock_binary)"),
        )
        self.assertLess(
            source.rindex("verify_stock_launch_artifacts("),
            source.index("backend = subprocess.Popen"),
        )
        self.assertIn('"stock_lighttpd_staticfile_linkage": _STOCK_STATICFILE_LINKAGE', source)
        self.assertNotIn("write_receipt(receipt, outcome)", source)
        self.assertIn('"127.0.0.1"', source)
        self.assertIn('"-D", "-m", str(module_dir)', source)
        self.assertIn('"--upstream", f"127.0.0.1:{backend_port}"', source)
        self.assertNotIn("stock_version=1.4.85", source)
        self.assertNotIn("patched", source.lower())

    def test_real_backend_harness_rejects_self_consistent_artifacts_without_external_attestation(self) -> None:
        harness = _load_real_backend_harness()
        with tempfile.TemporaryDirectory(prefix="stock-host-provenance-", dir=_temporary_root()) as temporary:
            root = Path(temporary)
            build_root = root / "build"
            binary = build_root / "bin" / "lighttpd"
            module_dir = build_root / "lib"
            runtime_root = root / "runtime"
            sidecar_root = root / "sidecar"
            sidecar = sidecar_root / "lighttpd-stock-sidecar"
            smoke = sidecar_root / "runtime-begin-smoke"
            binary.parent.mkdir(parents=True)
            module_dir.mkdir()
            runtime_root.mkdir(mode=0o700)
            sidecar_root.mkdir()
            binary.write_text("#!/bin/sh\nprintf 'lighttpd/1.4.85\\n'\n", encoding="utf-8")
            binary.chmod(0o700)
            (module_dir / "mod_accesslog.so").write_bytes(b"not-a-module")
            sidecar.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            sidecar.chmod(0o700)
            smoke.write_bytes(b"smoke")
            smoke.chmod(0o700)
            binary_digest = hashlib.sha256(binary.read_bytes()).hexdigest()
            contract = harness.expected_stock_lighttpd_contract()
            (build_root / ".lighttpd-binary.provenance").write_text(
                "\n".join((
                    f"lighttpd_version={contract['LIGHTTPD_VERSION']}",
                    f"lighttpd_source_sha256={contract['LIGHTTPD_SHA256']}",
                    f"lighttpd_binary_sha256={binary_digest}",
                    "",
                )), encoding="utf-8",
            )
            source_root = build_root / "src" / f"lighttpd-{contract['LIGHTTPD_VERSION']}"
            source_root.mkdir(parents=True)
            (source_root / ".lighttpd-source-provenance").write_text(
                "\n".join((
                    f"lighttpd_version={contract['LIGHTTPD_VERSION']}",
                    f"lighttpd_source_url={contract['LIGHTTPD_SOURCE_URL']}",
                    f"lighttpd_download_url={contract['LIGHTTPD_DOWNLOAD_URL']}",
                    f"lighttpd_sha256={contract['LIGHTTPD_SHA256']}",
                    "",
                )), encoding="utf-8",
            )
            parent_commit, source_tree_state = harness.repository_revision()
            sidecar_digest = hashlib.sha256(sidecar.read_bytes()).hexdigest()
            smoke_digest = hashlib.sha256(smoke.read_bytes()).hexdigest()
            sidecar_manifest = sidecar_root / "stock-sidecar-artifact.manifest"
            sidecar_manifest.write_text(
                "\n".join((
                    "schema_version=1",
                    "artifact_kind=lighttpd_stock_sidecar",
                    "connector_id=lighttpd",
                    "integration_mode=stock-lighttpd-sidecar",
                    f"parent_commit_sha={parent_commit}",
                    f"parent_source_tree_state={source_tree_state}",
                    "c_standard=c17",
                    f"sidecar_path={sidecar}",
                    f"sidecar_binary_sha256={sidecar_digest}",
                    f"runtime_begin_smoke_path={smoke}",
                    f"runtime_begin_smoke_sha256={smoke_digest}",
                    f"sidecar_source_inputs_sha256={'0' * 64}",
                    f"modsecurity_library_sha256={'0' * 64}",
                    "",
                )), encoding="utf-8",
            )
            sidecar_manifest.chmod(0o444)
            host = harness.verify_stock_host_provenance(binary, module_dir, binary_digest)
            source_root.chmod(0o775)
            self.assertEqual(
                harness.verify_stock_host_provenance(binary, module_dir, binary_digest), host
            )
            source_root.chmod(0o755)
            accesslog = module_dir / "mod_accesslog.so"
            accesslog.chmod(0o666)
            with self.assertRaisesRegex(RuntimeError, "loaded module"):
                harness.verify_stock_host_provenance(binary, module_dir, binary_digest)
            accesslog.chmod(0o644)
            accesslog.unlink()
            with self.assertRaisesRegex(RuntimeError, "loaded module"):
                harness.verify_stock_host_provenance(binary, module_dir, binary_digest)
            accesslog.write_bytes(b"not-a-module")
            accesslog.chmod(0o644)
            accesslog.unlink()
            accesslog.symlink_to(binary)
            with self.assertRaisesRegex(RuntimeError, "loaded module"):
                harness.verify_stock_host_provenance(binary, module_dir, binary_digest)
            accesslog.unlink()
            accesslog.write_bytes(b"not-a-module")
            accesslog.chmod(0o644)
            host = harness.verify_stock_host_provenance(binary, module_dir, binary_digest)
            sidecar_values = harness.verify_sidecar_build_manifest(
                sidecar, sidecar_digest, parent_commit, source_tree_state
            )
            environment = {
                **os.environ,
                "PYTHONDONTWRITEBYTECODE": "1",
                "STOCK_LIGHTTPD_BIN": str(binary),
                "STOCK_LIGHTTPD_MODULE_DIR": str(module_dir),
                "MSCONNECTOR_STOCK_SIDECAR_BINARY": str(sidecar),
                "STOCK_SIDECAR_RUNTIME_ROOT": str(runtime_root),
                "STOCK_SIDECAR_RECEIPT_PATH": str(runtime_root / "receipt.json"),
            }
            completed = subprocess.run(
                [sys.executable, str(REAL_BACKEND_HARNESS)],
                cwd=ROOT,
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 77, completed.stderr)
            self.assertIn("STOCK_SIDECAR_ARTIFACT_ATTESTATION is required", completed.stderr)
            attestation = root / "operator-attestation"
            attestation.write_text(
                "\n".join((
                    "schema_version=1",
                    "attestation_kind=operator_expected_artifact_tuple",
                    "connector_id=lighttpd",
                    "integration_mode=stock-lighttpd-sidecar",
                    f"parent_commit_sha={parent_commit}",
                    f"parent_source_tree_state={source_tree_state}",
                    f"lighttpd_version={host['LIGHTTPD_VERSION']}",
                    f"lighttpd_source_sha256={host['LIGHTTPD_SHA256']}",
                    f"stock_lighttpd_binary_sha256={host['stock_lighttpd_binary_sha256']}",
                    f"stock_lighttpd_mod_accesslog_sha256={host['stock_lighttpd_mod_accesslog_sha256']}",
                    "stock_lighttpd_staticfile_linkage=dynamic",
                    f"sidecar_binary_sha256={sidecar_values['sidecar_binary_sha256']}",
                    f"sidecar_source_inputs_sha256={sidecar_values['sidecar_source_inputs_sha256']}",
                    f"sidecar_modsecurity_library_sha256={sidecar_values['modsecurity_library_sha256']}",
                    "sidecar_c_standard=c17",
                    "",
                )), encoding="utf-8",
            )
            attestation.chmod(0o444)
            completed = subprocess.run(
                [sys.executable, str(REAL_BACKEND_HARNESS)],
                cwd=ROOT,
                env={**environment, "STOCK_SIDECAR_ARTIFACT_ATTESTATION": str(attestation)},
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertEqual(completed.returncode, 77, completed.stderr)
        self.assertIn("artifact attestation does not match", completed.stderr)

    def test_real_backend_harness_requires_builtin_staticfile_symbol(self) -> None:
        harness = _load_real_backend_harness()
        with tempfile.TemporaryDirectory(prefix="stock-staticfile-linkage-", dir=_temporary_root()) as temporary:
            binary = Path(temporary) / "lighttpd"
            binary.write_bytes(b"placeholder")
            with mock.patch.object(
                harness.subprocess,
                "run",
                return_value=subprocess.CompletedProcess(
                    args=["nm"], returncode=0,
                    stdout="00000000 T mod_staticfile_plugin_init\n", stderr="",
                ),
            ):
                harness.verify_stock_staticfile_linkage(binary)
            with mock.patch.object(
                harness.subprocess,
                "run",
                return_value=subprocess.CompletedProcess(
                    args=["nm"], returncode=0,
                    stdout="00000000 T unrelated_plugin_init\n", stderr="",
                ),
            ):
                with self.assertRaisesRegex(RuntimeError, "staticfile linkage"):
                    harness.verify_stock_staticfile_linkage(binary)

    def test_real_backend_artifact_path_chain_rejects_writable_and_symlinked_ancestors(self) -> None:
        harness = _load_real_backend_harness()
        with tempfile.TemporaryDirectory(prefix="stock-artifact-path-chain-",
                                         dir=_temporary_root()) as temporary:
            root = Path(temporary)
            artifact_root = root / "artifacts"
            artifact_root.mkdir(mode=0o755)
            artifact = artifact_root / "sidecar"
            artifact.write_bytes(b"artifact")
            artifact.chmod(0o700)
            harness.verify_artifact_path_chain(artifact, "test artifact")
            artifact_root.chmod(0o775)
            with self.assertRaisesRegex(RuntimeError, "path chain is not trusted"):
                harness.verify_artifact_path_chain(artifact, "test artifact")
            artifact_root.chmod(0o755)
            alias = root / "artifact-alias"
            alias.symlink_to(artifact_root, target_is_directory=True)
            with self.assertRaisesRegex(RuntimeError, "path chain is not trusted"):
                harness.verify_artifact_path_chain(alias / "sidecar", "test artifact")

    def test_c_source_uses_the_canonical_route_and_bounded_http1_translation(self) -> None:
        source = SIDECAR_SOURCE.read_text(encoding="utf-8")

        self.assertIn('SIDECAR_RUNTIME_CONNECTOR "lighttpd"', source)
        self.assertIn('"stock-lighttpd-sidecar"', source)
        self.assertIn("msconnector_runtime_transaction_begin", source)
        self.assertIn("msconnector_runtime_set_transaction_profile", source)
        self.assertIn("msconnector_runtime_transaction_finish_request_body", source)
        self.assertIn("msconnector_runtime_transaction_process_response_headers", source)
        self.assertIn("msconnector_runtime_transaction_finish_response_body", source)
        self.assertIn("msconnector_runtime_transaction_finalize_and_snapshot", source)
        self.assertIn("sidecar_write_allow_receipt", source)
        self.assertIn("sidecar_receipt_sha256", source)
        self.assertNotIn("sidecar_receipt_hash", source)
        self.assertIn("msconnector_runtime_transaction_fail", source)
        self.assertIn("sidecar_record_decision_delivery_failure", source)
        self.assertGreaterEqual(source.count("sidecar_record_decision_delivery_failure(transaction, &decision, &error)"), 4)
        self.assertIn("SIDECAR_MAX_PARALLEL 16U", source)
        self.assertIn('"127.0.0.1:"', source)
        self.assertIn("MSCONNECTOR_ERROR_BODY_TOO_LARGE", source)
        self.assertIn("sidecar_connection_value_allowed", source)
        self.assertIn("sidecar_headers_has_name", source)
        self.assertIn('sidecar_write_error(state->client, 417, &state->deadline)', source)
        self.assertIn('strcmp(state->payload.request_headers.method, "HEAD") == 0', source)
        self.assertIn("sidecar_parse_header_field", source)
        self.assertIn("sidecar_read_request_body", source)
        self.assertIn("sidecar_read_response_body", source)
        self.assertIn("unsigned char chunk[SIDECAR_IO_CHUNK]", source)
        self.assertIn("#define SIDECAR_IO_CHUNK (2U * 1024U)", source)
        runtime_source = COMMON_RUNTIME.read_text(encoding="utf-8")
        self.assertIn("begin_or_resume_streaming_body_phase", runtime_source)
        self.assertIn("MSCONNECTOR_PHASE_RESPONSE_BODY, companion, error", runtime_source)
        self.assertNotIn("response_body = malloc(state->payload.response_headers.content_length)", source)
        self.assertIn("Connection: close", source)
        self.assertNotIn("sidecar_proxy", source)

    def test_response_metadata_and_request_target_use_common_contract_bounds(self) -> None:
        source = SIDECAR_SOURCE.read_text(encoding="utf-8")
        request_start = source.index("static int sidecar_parse_request_headers_start")
        response_start = source.index("static int sidecar_parse_response_headers_start")
        request_parser = source[request_start:response_start]
        field_start = source.index("static int sidecar_parse_header_field")
        field_parser = source[field_start:request_start]
        exchange_start = source.index("static int sidecar_exchange_response")
        exchange_end = source.index("static void sidecar_exchange_error", exchange_start)
        response_exchange = source[exchange_start:exchange_end]

        self.assertIn('#include "msconnector/transaction_contract.h"', source)
        self.assertIn(
            "char uri[MSCONNECTOR_TRANSACTION_CONTRACT_URI_SIZE];", source
        )
        self.assertIn("sidecar_parse_request_start(cursor", request_parser)
        self.assertNotIn("char uri[512];", request_parser)
        self.assertNotIn("char start_line[1024];", request_parser)
        self.assertIn("out->status_code == 204", field_parser)
        self.assertNotIn("out->status_code == 304", field_parser)
        self.assertIn(
            "if (!state->payload.response_headers.no_body &&\n"
            "        state->payload.response_headers.content_length > state->response_limit)",
            response_exchange,
        )
        self.assertIn(
            "char request_line[MSCONNECTOR_TRANSACTION_CONTRACT_METHOD_SIZE +",
            response_exchange,
        )
        self.assertIn(
            "(size_t)request_line_size >= sizeof(request_line)", response_exchange
        )
        self.assertNotIn("char request_line[600];", response_exchange)

    def test_build_requires_an_explicit_external_output_root(self) -> None:
        script = BUILD_SCRIPT.read_text(encoding="utf-8")
        self.assertIn('BUILD_ROOT is required', script)
        self.assertIn('BUILD_ROOT must not be inside the checkout', script)
        self.assertIn('mktemp "$OUT_DIR/.stock-sidecar-artifact.manifest.XXXXXX"', script)
        self.assertIn('mv -f "$artifact_manifest_tmp" "$artifact_manifest"', script)
        self.assertIn('"$CONNECTOR_DIR/stock_sidecar/stock_sidecar.h"', script)
        self.assertIn('"$REPO_ROOT/common/runtime/msconnector_runtime.h"', script)
        self.assertIn('"$REPO_ROOT/connectors/profile_registry.h"', script)
        self.assertIn('"$REPO_ROOT/common/src/header_validation_internal.h"', script)
        self.assertIn("printf '%s\\000' \"$source_relative\"", script)
        self.assertNotIn('${HOME', script)

    def test_partial_response_header_write_claims_client_response_ownership(self) -> None:
        """A partial proxied header must suppress a second fallback response."""
        compiler = shutil.which("cc")
        include_directory = Path(os.environ.get("MODSECURITY_INCLUDE_DIR", "/usr/include"))
        if compiler is None:
            self.skipTest("requires a C compiler")
        if not (include_directory / "modsecurity" / "modsecurity.h").is_file():
            self.skipTest("requires libmodsecurity headers")

        source = SIDECAR_SOURCE.read_text(encoding="utf-8")
        forward_start = source.index("static int sidecar_forward_response")
        forward_end = source.index("\n}\n\nstatic int sidecar_exchange_request", forward_start)
        forward = source[forward_start:forward_end]
        exchange_error_start = source.index("static void sidecar_exchange_error")
        exchange_error_end = source.index("\n}\n\nstatic int sidecar_exchange", exchange_error_start)
        exchange_error = source[exchange_error_start:exchange_error_end]
        self.assertIn("sidecar_write_upstream_response_headers_observed", forward)
        self.assertIn("size_t header_bytes_sent = 0U;", forward)
        self.assertIn("if (header_bytes_sent > 0U) {", forward)
        self.assertIn("state->client_response_started = 1;", forward)
        self.assertIn("msconnector_runtime_transaction_set_response_commit_state_checked(", forward)
        self.assertIn("if (!state->client_response_started)", exchange_error)

        harness_source = r'''
#define MSCONNECTOR_STOCK_SIDECAR_MAIN
#define main stock_sidecar_program_main
#include "__SIDECAR_SOURCE__"
#undef main

#include <assert.h>

int main(void) {
    int sockets[2];
    int flags;
    int send_buffer = 1024;
    static char value[65536U];
    msconnector_header header;
    sidecar_headers headers;
    sidecar_deadline deadline;
    size_t bytes_sent = 0U;

    memset(value, 'x', sizeof(value));
    memset(&header, 0, sizeof(header));
    header.name = "X-Test";
    header.name_size = strlen(header.name);
    header.value = value;
    header.value_size = sizeof(value);
    memset(&headers, 0, sizeof(headers));
    headers.items = &header;
    headers.count = 1U;
    assert(socketpair(AF_UNIX, SOCK_STREAM, 0, sockets) == 0);
    assert(setsockopt(sockets[0], SOL_SOCKET, SO_SNDBUF, &send_buffer,
                      sizeof(send_buffer)) == 0);
    flags = fcntl(sockets[0], F_GETFL, 0);
    assert(flags >= 0);
    assert(fcntl(sockets[0], F_SETFL, flags | O_NONBLOCK) == 0);
    deadline.at_ms = sidecar_now_ms() + 100U;
    assert(sidecar_write_upstream_response_headers_observed(
        sockets[0], "HTTP/1.1 200 Proxied\r\n", &headers, &deadline,
        &bytes_sent) == 0);
    assert(bytes_sent > 0U);
    assert(close(sockets[0]) == 0);
    assert(close(sockets[1]) == 0);
    return 0;
}
'''.replace("__SIDECAR_SOURCE__", SIDECAR_SOURCE.as_posix())
        with tempfile.TemporaryDirectory(prefix="stock-sidecar-header-ownership-",
                                         dir=_temporary_root()) as temporary:
            directory = Path(temporary)
            harness = directory / "header_ownership.c"
            binary = directory / "header_ownership"
            harness.write_text(harness_source, encoding="utf-8")
            compiled = subprocess.run(
                [
                    compiler,
                    "-std=c17", "-Wall", "-Wextra", "-Werror",
                    "-ffunction-sections", "-fdata-sections", "-pthread",
                    "-I.", "-Icommon/include", "-Icommon/runtime",
                    "-Iconnectors/lighttpd/stock_sidecar", f"-I{include_directory}",
                    str(harness), "-Wl,--gc-sections", "-o", str(binary),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(compiled.returncode, 0, compiled.stderr)
            executed = subprocess.run(
                [str(binary)], cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertEqual(executed.returncode, 0, executed.stderr)


class StockSidecarLoopbackContractTest(unittest.TestCase):
    binary: Path
    begin_smoke: Path
    library_dir: Path
    build_directory: tempfile.TemporaryDirectory[str]

    @classmethod
    def setUpClass(cls) -> None:
        include_directory = os.environ.get("MODSECURITY_INCLUDE_DIR")
        library_directory = os.environ.get("MODSECURITY_LIB_DIR")
        compiler = os.environ.get("CC", "cc")
        if not include_directory or not library_directory:
            raise unittest.SkipTest(
                "set MODSECURITY_INCLUDE_DIR and MODSECURITY_LIB_DIR for Stock-sidecar loopback tests"
            )
        if not Path(include_directory, "modsecurity/modsecurity.h").is_file():
            raise unittest.SkipTest("MODSECURITY_INCLUDE_DIR does not contain modsecurity/modsecurity.h")
        if not Path(library_directory, "libmodsecurity.so").is_file():
            raise unittest.SkipTest("MODSECURITY_LIB_DIR does not contain libmodsecurity.so")
        if shutil.which(compiler) is None:
            raise unittest.SkipTest(f"C compiler is unavailable: {compiler}")

        cls.library_dir = Path(library_directory)
        cls.build_directory = tempfile.TemporaryDirectory(
            prefix="stock-lighttpd-sidecar-build-", dir=_temporary_root()
        )
        output_directory = Path(cls.build_directory.name)
        requested_binary = os.environ.get("MSCONNECTOR_STOCK_SIDECAR_BINARY")
        if requested_binary:
            cls.binary = Path(requested_binary)
            if not cls.binary.is_file():
                raise AssertionError(f"MSCONNECTOR_STOCK_SIDECAR_BINARY is missing: {cls.binary}")
        else:
            cls.binary = output_directory / "stock-lighttpd-sidecar"
            cls._compile(cls.binary, SIDECAR_SOURCE, define_main=True, include_directory=Path(include_directory))
        cls.begin_smoke = output_directory / "runtime-begin-smoke"
        cls._compile(cls.begin_smoke, BEGIN_SMOKE_SOURCE, define_main=False,
                     include_directory=Path(include_directory))

    @classmethod
    def tearDownClass(cls) -> None:
        cls.build_directory.cleanup()

    @classmethod
    def _compile(cls, output: Path, source: Path, *, define_main: bool,
                 include_directory: Path) -> None:
        compiler = os.environ.get("CC", "cc")
        command = [
            compiler,
            "-std=c17", "-Wall", "-Wextra", "-Werror", "-pthread",
            "-I.", "-Icommon/include", "-Icommon/runtime",
            "-Iconnectors/lighttpd/stock_sidecar", f"-I{include_directory}",
        ]
        if define_main:
            command.append("-DMSCONNECTOR_STOCK_SIDECAR_MAIN")
        command.extend([str(source), str(COMMON_RUNTIME), str(PROFILE_REGISTRY)])
        command.extend(str(path) for path in COMMON_SOURCES)
        command.extend([
            f"-L{cls.library_dir}", f"-Wl,-rpath,{cls.library_dir}",
            "-lmodsecurity", "-lcrypto", "-lyajl", "-o", str(output),
        ])
        completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            raise AssertionError(
                "Stock sidecar compile/link failed:\n"
                f"command={' '.join(command)}\nstdout={completed.stdout}\nstderr={completed.stderr}"
            )

    @contextlib.contextmanager
    def _fixture(self, rules: str, responder, *, request_limit: int = 64,
                 response_limit: int = 64, timeout_ms: int = 1000,
                 phase4_mode: str = "strict",
                 environment: dict[str, str] | None = None):
        with tempfile.TemporaryDirectory(prefix="stock-lighttpd-sidecar-case-",
                                         dir=_temporary_root()) as temporary:
            directory = Path(temporary)
            rules_path = directory / "rules.conf"
            event_path = directory / "events.jsonl"
            config_path = directory / "runtime.conf"
            rules_path.write_text(
                "\n".join((
                    "SecRuleEngine On",
                    "SecRequestBodyAccess On",
                    "SecResponseBodyAccess On",
                    "SecResponseBodyMimeType text/plain",
                    rules.strip(),
                    "",
                )),
                encoding="utf-8",
            )
            config_path.write_text(
                "\n".join((
                    "enabled=on",
                    f"rules_file={rules_path}",
                    "transaction_id_header=x-request-id",
                    "request_body_mode=streaming",
                    "response_body_mode=streaming",
                    f"request_body_limit={request_limit}",
                    f"response_body_limit={response_limit}",
                    "body_limit_action=reject",
                    f"phase4_mode={phase4_mode}",
                    "default_block_status=403",
                    "default_error_status=502",
                    "max_header_count=32",
                    "max_header_name_size=128",
                    "max_header_value_size=512",
                    "max_total_header_bytes=65536",
                    "max_event_json_bytes=16384",
                    f"event_path={event_path}",
                    "",
                )),
                encoding="utf-8",
            )
            with _upstream(responder) as upstream:
                with _RunningSidecar(self.binary, config_path, upstream.server_address[1],
                                     self.library_dir, timeout_ms, environment) as sidecar:
                    yield sidecar, upstream, event_path, config_path

    def test_startup_rejects_limits_that_exceed_sidecar_allocation_bounds(self) -> None:
        limit_overrides = (
            "max_header_count=257",
            "max_total_header_bytes=65537",
            "max_event_json_bytes=16385",
            "request_body_limit=1048577",
            "response_body_limit=1048577",
        )
        for override in limit_overrides:
            with self.subTest(override=override), tempfile.TemporaryDirectory(
                prefix="stock-sidecar-limit-reject-", dir=_temporary_root(),
            ) as temporary:
                directory = Path(temporary)
                config = directory / "runtime.conf"
                config.write_text(
                    "\n".join((
                        "enabled=on",
                        "rules_inline=SecRuleEngine On",
                        "transaction_id_header=x-request-id",
                        "request_body_mode=streaming",
                        "response_body_mode=streaming",
                        "request_body_limit=64",
                        "response_body_limit=64",
                        "body_limit_action=reject",
                        "phase4_mode=strict",
                        "default_block_status=403",
                        "default_error_status=502",
                        "max_header_count=32",
                        "max_header_name_size=128",
                        "max_header_value_size=512",
                        "max_total_header_bytes=4096",
                        "max_event_json_bytes=16384",
                        override,
                        f"event_path={directory / 'events.jsonl'}",
                        "",
                    )),
                    encoding="utf-8",
                )
                completed = subprocess.run(
                    [str(self.binary), "--config", str(config), "--listen",
                     f"127.0.0.1:{_free_loopback_port()}", "--upstream", "127.0.0.1:9"],
                    cwd=ROOT,
                    env={**os.environ, "LD_LIBRARY_PATH": str(self.library_dir)},
                    text=True,
                    capture_output=True,
                    check=False,
                    timeout=3.0,
                )
                self.assertEqual(completed.returncode, 78, completed.stderr)

    def test_allow_receipt_is_published_from_a_cleaned_snapshot(self) -> None:
        normal = b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\nConnection: close\r\n\r\n"
        binding = "a" * 64
        with tempfile.TemporaryDirectory(prefix="stock-sidecar-receipt-",
                                         dir=_temporary_root()) as temporary:
            receipt = Path(temporary) / "allow-receipt.json"
            environment = {
                "STOCK_SIDECAR_RECEIPT_PATH": str(receipt),
                "STOCK_SIDECAR_RECEIPT_BINDING": binding,
            }
            with self._fixture("", lambda _request: normal, environment=environment) as (
                sidecar, upstream, _events, _config,
            ):
                self.assertEqual(_status(sidecar.exchange(self._request())), 200)
                self.assertEqual(upstream.record_count(), 1)
            value = json.loads(receipt.read_text(encoding="utf-8"))
        self.assertEqual(value["phase_observation"], "runtime_snapshot_after_cleanup")
        self.assertEqual(value["cleanup_status"], "complete")
        self.assertIs(value["cleanup_complete"], True)
        self.assertIs(value["response_committed"], True)
        self.assertEqual(
            value["receipt_binding_sha256"],
            hashlib.sha256(binding.encode("ascii")).hexdigest(),
        )
        self.assertRegex(value["transaction_id_sha256"], r"^[0-9a-f]{64}$")
        self.assertNotIn("transaction_id", value)
        self.assertIs(value["opaque_handles_persisted"], False)

    def test_non_allow_receipt_is_bounded_and_separate_from_host_action(self) -> None:
        normal = b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\nConnection: close\r\n\r\n"
        binding = "b" * 64
        with tempfile.TemporaryDirectory(prefix="stock-sidecar-terminal-receipt-",
                                         dir=_temporary_root()) as temporary:
            receipt = Path(temporary) / "terminal-receipt.json"
            environment = {
                "STOCK_SIDECAR_RECEIPT_PATH": str(receipt),
                "STOCK_SIDECAR_RECEIPT_BINDING": binding,
            }
            with self._fixture(
                'SecRule REQUEST_URI "@streq /p1-terminal" '
                '"id:9801006,phase:1,deny,status:451,log"',
                lambda _request: normal,
                environment=environment,
            ) as (sidecar, upstream, _events, _config):
                self.assertEqual(_status(sidecar.exchange(self._request("/p1-terminal"))), 451)
                self.assertEqual(upstream.record_count(), 0)
            value = json.loads(receipt.read_text(encoding="utf-8"))
        self.assertEqual(value["schema_version"], 2)
        self.assertEqual(value["receipt_kind"], "non_allow")
        self.assertEqual(value["phase_observation"], "runtime_snapshot_after_cleanup")
        self.assertEqual(value["observed_phase_sequence"], ["P1"])
        self.assertEqual(value["engine_decision"], "block")
        self.assertEqual(value["contract_action"], "deny")
        self.assertEqual(value["error_class"], "none")
        self.assertEqual(value["mode"], "strict")
        self.assertIs(value["response_committed"], False)
        self.assertEqual(value["cleanup_status"], "complete")
        self.assertIs(value["cleanup_complete"], True)
        self.assertEqual(
            value["receipt_binding_sha256"],
            hashlib.sha256(binding.encode("ascii")).hexdigest(),
        )
        self.assertRegex(value["transaction_id_sha256"], r"^[0-9a-f]{64}$")
        self.assertNotIn("transaction_id", value)
        self.assertNotIn("actual_host_action", value)
        self.assertNotIn("rule_id", value)
        self.assertIs(value["payloads_persisted"], False)
        self.assertIs(value["opaque_handles_persisted"], False)

    def test_safe_p4_receipt_keeps_engine_and_host_outcomes_separate(self) -> None:
        response_body = b"stock-p4-safe-marker"
        response = (
            b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n"
            + f"Content-Length: {len(response_body)}\r\n".encode("ascii")
            + b"Connection: close\r\n\r\n"
            + response_body
        )
        binding = "c" * 64
        with tempfile.TemporaryDirectory(prefix="stock-sidecar-p4-receipt-",
                                         dir=_temporary_root()) as temporary:
            receipt = Path(temporary) / "p4-safe-receipt.json"
            environment = {
                "STOCK_SIDECAR_RECEIPT_PATH": str(receipt),
                "STOCK_SIDECAR_RECEIPT_BINDING": binding,
            }
            with self._fixture(
                'SecRule RESPONSE_BODY "@contains stock-p4-safe-marker" '
                '"id:9801007,phase:4,deny,status:429,log"',
                lambda _request: response,
                response_limit=len(response_body),
                phase4_mode="safe",
                environment=environment,
            ) as (sidecar, upstream, events, _config):
                client_response = sidecar.exchange(self._request())
                self.assertEqual(_status(client_response), 200)
                self.assertTrue(client_response.endswith(response_body))
                self.assertEqual(upstream.record_count(), 1)
                event_text = self._wait_for_event(events, "MSCONN_EVENT_RESPONSE_BLOCKED")
            value = json.loads(receipt.read_text(encoding="utf-8"))
        self.assertEqual(value["schema_version"], 2)
        self.assertEqual(value["receipt_kind"], "non_allow")
        self.assertEqual(value["observed_phase_sequence"], ["P1", "P2", "P3", "P4"])
        self.assertEqual(value["engine_decision"], "rate_limit")
        self.assertEqual(value["contract_action"], "rate_limit")
        self.assertEqual(value["mode"], "safe")
        self.assertIs(value["response_committed"], True)
        self.assertNotIn("actual_host_action", value)
        self.assertIn('"requested_action":"deny"', event_text)
        self.assertIn('"actual_action":"log_only"', event_text)
        self.assertIn('"late_intervention":true', event_text)
        self.assertIn('"late_intervention_mode":"safe"', event_text)
        self.assertIn('"transport_result":"log_only"', event_text)
        self.assertNotIn(response_body.decode("ascii"), event_text)

    def _wait_for_event(self, event_path: Path, marker: str) -> str:
        deadline = time.monotonic() + 3.0
        value = ""
        while time.monotonic() < deadline:
            if event_path.exists():
                value = event_path.read_text(encoding="utf-8")
                if marker in value:
                    return value
            time.sleep(0.02)
        self.fail(f"event marker {marker!r} was not observed: {value!r}")

    @staticmethod
    def _request(path: str = "/", body: bytes = b"", extra_headers: bytes = b"") -> bytes:
        return (
            f"POST {path} HTTP/1.1\r\nHost: example.test\r\n"
            f"Content-Length: {len(body)}\r\n".encode("ascii")
            + extra_headers
            + b"Connection: close\r\n\r\n"
            + body
        )

    def test_runtime_identity_smoke_accepts_the_canonical_profile(self) -> None:
        def responder(_request: bytes) -> bytes:
            return b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n"

        with self._fixture("", responder) as (_sidecar, _upstream_server, _events, config):
            completed = subprocess.run(
                [str(self.begin_smoke), str(config)], cwd=ROOT, text=True,
                capture_output=True, check=False,
                env={**os.environ, "LD_LIBRARY_PATH": str(self.library_dir)},
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_allow_exercises_p1_to_p4_before_client_commit(self) -> None:
        # Exceed the sidecar's bounded request I/O chunk so the real Common
        # runtime must keep P2 active across more than one append before EOS.
        body = b"request-body-" + (b"x" * ((2 * 1024) + 17))
        response_body = b"response-body"

        def responder(request: bytes) -> bytes:
            self.assertIn(body, request)
            return (
                b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n"
                + f"Content-Length: {len(response_body)}\r\n".encode("ascii")
                + b"Connection: close\r\n\r\n"
                + response_body
            )

        with self._fixture("", responder, request_limit=len(body)) as (sidecar, upstream, _events, _config):
            response = sidecar.exchange(self._request(body=body))
            self.assertEqual(_status(response), 200)
            self.assertTrue(response.endswith(response_body))
            self.assertEqual(upstream.record_count(), 1)

    def test_p1_p2_p3_blocks_are_precommit_and_p4_uses_late_policy(self) -> None:
        normal = b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\nConnection: close\r\n\r\n"

        with self._fixture(
            'SecRule REQUEST_URI "@streq /p1-block" "id:9801001,phase:1,deny,status:451,log"',
            lambda _request: normal,
        ) as (sidecar, upstream, _events, _config):
            self.assertEqual(_status(sidecar.exchange(self._request("/p1-block"))), 451)
            self.assertEqual(upstream.record_count(), 0)

        with self._fixture(
            'SecRule REQUEST_BODY "@contains p2-marker" "id:9801002,phase:2,deny,status:418,log"',
            lambda _request: normal,
        ) as (sidecar, upstream, events, _config):
            request_body = b"p2-marker"
            self.assertEqual(_status(sidecar.exchange(self._request(body=request_body))), 418)
            self.assertEqual(upstream.record_count(), 0)
            event_text = self._wait_for_event(events, "MSCONN_EVENT_REQUEST_BLOCKED")
            self.assertNotIn(request_body.decode("ascii"), event_text)
            self.assertNotIn("body_payload", event_text)

        p3_response = (
            b"HTTP/1.1 200 OK\r\nX-Block-P3: yes\r\nContent-Length: 0\r\n"
            b"Connection: close\r\n\r\n"
        )
        with self._fixture(
            'SecRule RESPONSE_HEADERS:X-Block-P3 "@streq yes" "id:9801003,phase:3,deny,status:422,log"',
            lambda _request: p3_response,
        ) as (sidecar, upstream, _events, _config):
            self.assertEqual(_status(sidecar.exchange(self._request())), 422)
            self.assertEqual(upstream.record_count(), 1)

        # Two bounded sidecar reads exercise a multi-chunk P4 stream while
        # remaining below libmodsecurity's independent default body ceiling.
        p4_body = b"p4-marker-" + b"x" * 3000
        p4_response = (
            b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n"
            + f"Content-Length: {len(p4_body)}\r\n".encode("ascii")
            + b"Connection: close\r\n\r\n"
            + p4_body
        )
        with self._fixture(
            'SecRule RESPONSE_BODY "@contains p4-marker" "id:9801004,phase:4,deny,status:429,log"',
            lambda _request: p4_response, response_limit=len(p4_body),
            phase4_mode="safe",
        ) as (sidecar, upstream, events, _config):
            response = sidecar.exchange(self._request())
            self.assertEqual(_status(response), 200)
            self.assertTrue(response.endswith(p4_body))
            self.assertEqual(upstream.record_count(), 1)
            event_text = self._wait_for_event(events, "MSCONN_EVENT_RESPONSE_BLOCKED")
            self.assertIn('"requested_action":"deny"', event_text)
            self.assertIn('"actual_action":"log_only"', event_text)
            self.assertIn('"transport_result":"log_only"', event_text)
            self.assertNotIn(p4_body.decode("ascii"), event_text)
            self.assertNotIn("body_payload", event_text)

        with self._fixture(
            'SecRule RESPONSE_BODY "@contains p4-marker" "id:9801005,phase:4,deny,status:429,log"',
            lambda _request: p4_response, response_limit=len(p4_body),
            phase4_mode="strict",
        ) as (sidecar, upstream, events, _config):
            response = sidecar.exchange(self._request())
            self.assertEqual(_status(response), 200)
            # A committed HTTP/1.1 response cannot be replaced retroactively.
            # Strict therefore aborts the stream instead of emitting the rule's
            # pre-commit 429 decision after the original 200 status line.
            self.assertNotIn(b"HTTP/1.1 429", response)
            self.assertEqual(upstream.record_count(), 1)
            event_text = self._wait_for_event(events, "MSCONN_EVENT_RESPONSE_BLOCKED")
            self.assertIn('"actual_action":"abort_connection"', event_text)
            self.assertIn('"connection_aborted":true', event_text)
            self.assertNotIn(p4_body.decode("ascii"), event_text)
            self.assertNotIn("body_payload", event_text)

    def test_limits_and_unsafe_framing_fail_closed_without_upstream_release(self) -> None:
        normal = b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\nConnection: close\r\n\r\n"

        with self._fixture("", lambda _request: normal, request_limit=4) as (sidecar, upstream, events, _config):
            request_body = b"12345"
            self.assertEqual(_status(sidecar.exchange(self._request(body=request_body))), 413)
            self.assertEqual(upstream.record_count(), 0)
            event_text = self._wait_for_event(events, "MSCONN_EVENT_BODY_LIMIT")
            self.assertNotIn(request_body.decode("ascii"), event_text)

        oversized_response = b"HTTP/1.1 200 OK\r\nContent-Length: 5\r\n\r\n12345"
        with self._fixture("", lambda _request: oversized_response, response_limit=4) as (sidecar, upstream, events, _config):
            self.assertEqual(_status(sidecar.exchange(self._request())), 413)
            self.assertEqual(upstream.record_count(), 1)
            self._wait_for_event(events, "MSCONN_EVENT_BODY_LIMIT")

        with self._fixture("", lambda _request: normal) as (sidecar, upstream, _events, _config):
            unsafe = (
                b"POST / HTTP/1.1\r\nHost: example.test\r\nTransfer-Encoding: chunked\r\n"
                b"Connection: close\r\n\r\n0\r\n\r\n"
            )
            self.assertEqual(_status(sidecar.exchange(unsafe)), 400)
            self.assertEqual(upstream.record_count(), 0)
            unknown_connection = self._request(extra_headers=b"Connection: invented-token\r\n")
            self.assertEqual(_status(sidecar.exchange(unknown_connection)), 400)
            self.assertEqual(upstream.record_count(), 0)
            duplicate_length = (
                b"POST / HTTP/1.1\r\nHost: example.test\r\nContent-Length: 0\r\n"
                b"Content-Length: 0\r\nConnection: close\r\n\r\n"
            )
            self.assertEqual(_status(sidecar.exchange(duplicate_length)), 400)
            self.assertEqual(upstream.record_count(), 0)

    def test_head_and_status_without_body_do_not_read_or_forward_a_body(self) -> None:
        head_response = b"HTTP/1.1 200 OK\r\nContent-Length: 5\r\n\r\n"
        no_content = b"HTTP/1.1 204 No Content\r\nContent-Length: 0\r\n\r\n"

        with self._fixture("", lambda _request: head_response, response_limit=4) as (
            sidecar, upstream, _events, _config,
        ):
            request = b"HEAD /head HTTP/1.1\r\nHost: example.test\r\nConnection: close\r\n\r\n"
            response = sidecar.exchange(request)
            self.assertEqual(_status(response), 200)
            self.assertIn(b"Content-Length: 5", response)
            self.assertEqual(upstream.record_count(), 1)

        with self._fixture("", lambda _request: no_content) as (sidecar, upstream, _events, _config):
            response = sidecar.exchange(self._request())
            self.assertEqual(_status(response), 204)
            self.assertEqual(upstream.record_count(), 1)

        invalid_no_content = b"HTTP/1.1 204 No Content\r\nContent-Length: 1\r\n\r\nx"
        with self._fixture("", lambda _request: invalid_no_content) as (sidecar, upstream, _events, _config):
            self.assertEqual(_status(sidecar.exchange(self._request())), 502)
            self.assertEqual(upstream.record_count(), 1)

    def test_not_modified_representation_length_is_metadata_only(self) -> None:
        not_modified = b"HTTP/1.1 304 Not Modified\r\nContent-Length: 5\r\n\r\n"

        with self._fixture("", lambda _request: not_modified, response_limit=4) as (
            sidecar, upstream, _events, _config,
        ):
            response = sidecar.exchange(self._request("/cached"))
            self.assertEqual(_status(response), 304)
            self.assertIn(b"Content-Length: 5", response)
            self.assertEqual(upstream.record_count(), 1)

    def test_request_target_reaches_the_canonical_uri_boundary(self) -> None:
        target = b"/" + b"a" * (16384 - 2)
        request = (
            b"POST " + target + b" HTTP/1.1\r\nHost: example.test\r\n"
            b"Content-Length: 0\r\nConnection: close\r\n\r\n"
        )
        normal = b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n"

        with self._fixture("", lambda _request: normal) as (sidecar, upstream, _events, _config):
            self.assertEqual(_status(sidecar.exchange(request)), 200)
            self.assertEqual(upstream.record_count(), 1)
            with upstream.records_lock:
                self.assertIn(target, upstream.records[0])

    def test_expect_is_rejected_before_body_read_or_upstream_release(self) -> None:
        normal = b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n"
        expectations = (
            (b"Expect: 100-continue\r\n", b""),
            (b"eXpEcT: 100-CONTINUE\r\n", b"body"),
            (b"EXPECT: unsupported\r\n", b""),
        )

        with self._fixture("", lambda _request: normal, timeout_ms=250) as (
            sidecar, upstream, _events, _config,
        ):
            for expectation, body in expectations:
                with self.subTest(expectation=expectation, body=body):
                    request = (
                        b"POST /expect HTTP/1.1\r\nHost: example.test\r\n"
                        b"Content-Length: 4\r\n" + expectation +
                        b"Connection: close\r\n\r\n" + body
                    )
                    self.assertEqual(_status(sidecar.exchange(request)), 417)
                    self.assertEqual(upstream.record_count(), 0)

    def test_timeout_and_client_cancel_emit_distinct_terminal_events(self) -> None:
        normal = b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n"

        with self._fixture("", lambda _request: normal, timeout_ms=120) as (sidecar, _upstream, events, _config):
            with sidecar.connect() as client:
                client.sendall(
                    b"POST /slow HTTP/1.1\r\nHost: example.test\r\nContent-Length: 4\r\n\r\na"
                )
                response = bytearray()
                while True:
                    chunk = client.recv(4096)
                    if not chunk:
                        break
                    response.extend(chunk)
            self.assertEqual(_status(bytes(response)), 504)
            self._wait_for_event(events, "engine_timeout")

        with self._fixture("", lambda _request: normal) as (sidecar, _upstream, events, _config):
            client = sidecar.connect()
            try:
                client.sendall(
                    b"POST /cancel HTTP/1.1\r\nHost: example.test\r\nContent-Length: 4\r\n\r\na"
                )
            finally:
                client.close()
            self._wait_for_event(events, "client_cancel")

    def test_client_reset_during_a_rule_block_records_an_abort_host_action(self) -> None:
        normal = b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n"
        rule = 'SecRule REQUEST_BODY "@contains block-reset" "id:9801102,phase:2,deny,status:418,log"'

        with self._fixture(rule, lambda _request: normal) as (sidecar, upstream, events, _config):
            client = sidecar.connect()
            try:
                client.sendall(self._request(body=b"block-reset"))
                # The complete P2 input has been queued before the RST.  A
                # reset forces the pending small decision response through
                # the adapter's failed-delivery path instead of allowing a
                # normal visible status to be inferred.
                client.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0))
            finally:
                client.close()
            event_text = self._wait_for_event(events, '"actual_action":"abort_connection"')
            self.assertIn('"connection_aborted":true', event_text)
            self.assertIn('"rule_id":"9801102"', event_text)
            self.assertEqual(upstream.record_count(), 0)

    def test_parallel_capacity_and_connection_reuse_are_bounded(self) -> None:
        normal = b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\nConnection: close\r\n\r\n"

        with self._fixture("", lambda _request: normal, timeout_ms=2000) as (sidecar, upstream, _events, _config):
            held_clients: list[socket.socket] = []
            try:
                for _ in range(16):
                    client = sidecar.connect()
                    client.sendall(
                        b"POST /hold HTTP/1.1\r\nHost: example.test\r\nContent-Length: 1\r\n\r\n"
                    )
                    held_clients.append(client)
                time.sleep(0.15)
                self.assertEqual(_status(sidecar.exchange(self._request())), 503)
                self.assertEqual(upstream.record_count(), 0)
            finally:
                for client in held_clients:
                    client.close()

        with self._fixture("", lambda _request: normal) as (sidecar, upstream, _events, _config):
            with sidecar.connect() as client:
                request = self._request()
                client.sendall(request + request)
                response = bytearray()
                while True:
                    chunk = client.recv(4096)
                    if not chunk:
                        break
                    response.extend(chunk)
            self.assertEqual(_status(bytes(response)), 200)
            self.assertEqual(bytes(response).count(b"HTTP/1.1"), 1)
            deadline = time.monotonic() + 1.0
            while upstream.record_count() == 0 and time.monotonic() < deadline:
                time.sleep(0.02)
            self.assertEqual(upstream.record_count(), 1)

    def test_nonreading_clients_cannot_hold_all_workers_past_the_exchange_deadline(self) -> None:
        large_body = b"x" * (1024 * 1024)
        large_response = (
            b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n"
            + f"Content-Length: {len(large_body)}\r\n\r\n".encode("ascii")
            + large_body
        )
        released_response = b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n"

        def responder(request: bytes) -> bytes:
            if request.startswith(b"POST /released HTTP/1.1\r\n"):
                return released_response
            return large_response

        with self._fixture("", responder, response_limit=len(large_body), timeout_ms=2500) as (
            sidecar, upstream, _events, _config,
        ):
            held_clients: list[socket.socket] = []
            try:
                for _ in range(16):
                    client = sidecar.connect()
                    client.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024)
                    client.sendall(
                        b"POST /slow-send HTTP/1.1\r\nHost: example.test\r\n"
                        b"Content-Length: 0\r\nConnection: close\r\n\r\n"
                    )
                    held_clients.append(client)
                deadline = time.monotonic() + 3.0
                while upstream.record_count() < 16 and time.monotonic() < deadline:
                    time.sleep(0.02)
                # The listener may reject the final client while the first
                # 16 workers are live; either way at least 15 clients have
                # reached the expensive response-write boundary before the
                # follow-up request proves deadline-driven release.
                self.assertGreaterEqual(upstream.record_count(), 15)
                time.sleep(3.0)
                self.assertEqual(_status(sidecar.exchange(self._request("/released"))), 200)
            finally:
                for client in held_clients:
                    client.close()


if __name__ == "__main__":
    unittest.main()
