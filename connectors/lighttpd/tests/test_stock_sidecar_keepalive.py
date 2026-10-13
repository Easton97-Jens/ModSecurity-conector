"""Raw socket component tests for bounded Stock-sidecar sequential reuse."""
import socket
import json
import time
import tempfile
import threading
import socketserver
from pathlib import Path
import unittest
from unittest import mock

from connectors.lighttpd.tests import test_stock_sidecar_contract as contracts


class StockSidecarKeepaliveTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        contracts.StockSidecarLoopbackContractTest.setUpClass()
        # A test-only observer calls the real Common finalizer and records its
        # returned cleanup snapshots. Production source/control flow stays real.
        directory = Path(contracts.StockSidecarLoopbackContractTest.build_directory.name)
        source = directory / "stock-keepalive-finalize-observer.c"
        source.write_text(r'''
#define _POSIX_C_SOURCE 200809L
#include "msconnector_runtime.h"
static int test_finalize(msconnector_runtime_transaction **,
                         msconnector_runtime_transaction_snapshot *, msconnector_error *);
#define msconnector_runtime_transaction_finalize_and_snapshot test_finalize
#include "__SIDECAR_SOURCE__"
#undef msconnector_runtime_transaction_finalize_and_snapshot
static int test_finalize(msconnector_runtime_transaction **transaction,
                         msconnector_runtime_transaction_snapshot *snapshot,
                         msconnector_error *error) {
    int result = msconnector_runtime_transaction_finalize_and_snapshot(transaction, snapshot, error);
    const char *path = getenv("STOCK_TEST_FINALIZE_LOG");
    if (result && path != NULL) {
        char digest[SIDECAR_RECEIPT_HEX_SIZE + 1U];
        char record[256];
        int fd = open(path, O_WRONLY | O_APPEND | O_CREAT | O_CLOEXEC | O_NOFOLLOW, 0600);
        if (fd < 0 || !sidecar_receipt_sha256(snapshot->contract.transaction_id, digest)) abort();
        int length = snprintf(record, sizeof(record),
            "{\"id\":\"%s\",\"cleaned\":%s,\"finished\":%s}\n", digest,
            snapshot->contract.cleanup_complete && snapshot->contract.status ==
                MSCONNECTOR_TRANSACTION_STATUS_CLEANED ? "true" : "false",
            snapshot->finished ? "true" : "false");
        if (length <= 0 || (size_t)length >= sizeof(record) ||
            write(fd, record, (size_t)length) != length || close(fd) != 0) abort();
    }
    return result;
}
'''.replace("__SIDECAR_SOURCE__", contracts.SIDECAR_SOURCE.as_posix()))
        cls.observed_binary = directory / "stock-keepalive-finalize-observer"
        contracts.StockSidecarLoopbackContractTest._compile(
            cls.observed_binary, source, define_main=True,
            include_directory=Path(contracts.os.environ["MODSECURITY_INCLUDE_DIR"]))

    @classmethod
    def tearDownClass(cls):
        contracts.StockSidecarLoopbackContractTest.tearDownClass()

    def fixture(self, rules="", responder=None, **kwargs):
        helper = contracts.StockSidecarLoopbackContractTest()
        return helper._fixture(rules, responder or (
            lambda _: b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nok"), **kwargs)

    @staticmethod
    def request(path="/allow", body=b"", connection=b"keep-alive", method="POST"):
        return (f"{method} {path} HTTP/1.1\r\nHost: example.test\r\nContent-Length: {len(body)}\r\n".encode()
                + b"Connection: " + connection + b"\r\n\r\n" + body)

    @staticmethod
    def response_headers(client):
        data = bytearray()
        while not data.endswith(b"\r\n\r\n"):
            chunk = client.recv(1)
            if not chunk:
                raise AssertionError("connection closed before complete response")
            data.extend(chunk)
        return bytes(data)

    @staticmethod
    def response(client):
        data = bytearray(StockSidecarKeepaliveTest.response_headers(client))
        length = next((int(line.split(b":", 1)[1]) for line in data.split(b"\r\n")
                       if line.lower().startswith(b"content-length:")), 0)
        for _ in range(length):
            chunk = client.recv(1)
            if not chunk:
                raise AssertionError("incomplete response body")
            data.extend(chunk)
        return int(data.split(b" ", 2)[1]), bytes(data)

    def test_allow_block_allow_same_socket(self):
        rules = 'SecRule REQUEST_URI "@streq /block" "id:985001,phase:1,deny,status:403,log"'
        with self.fixture(rules) as (sidecar, upstream, events, _config):
            with sidecar.connect() as client:
                identity = client.getsockname(), client.getpeername(), client.fileno()
                for path, expected in (("/allow", 200), ("/block", 403), ("/after", 200)):
                    client.sendall(self.request(path, method="GET"))
                    status, response = self.response(client)
                    self.assertEqual(status, expected)
                    self.assertIn(b"Connection: keep-alive", response)
                    self.assertEqual(identity, (client.getsockname(), client.getpeername(), client.fileno()))
                self.assertEqual(upstream.record_count(), 2)
                client.sendall(self.request("/close", connection=b"close"))
                self.assertEqual(self.response(client)[0], 200)
                self.assertEqual(client.recv(1), b"")
            records = [json.loads(line) for line in events.read_text().splitlines()]
            ids = {record["transaction_id"] for record in records if record.get("transaction_id")}
            self.assertEqual(len(ids), 1)  # Only the rule block emits event records.
            self.assertTrue(any(record.get("rule_id") == "985001" for record in records))

    def test_each_exchange_finalizes_a_distinct_common_transaction(self):
        rules = 'SecRule REQUEST_URI "@streq /block" "id:985004,phase:1,deny,status:403,log"'
        with tempfile.TemporaryDirectory(dir=contracts._temporary_root()) as temporary:
            receipt = Path(temporary) / "receipt.json"
            environment = {"STOCK_SIDECAR_RECEIPT_PATH": str(receipt),
                           "STOCK_SIDECAR_RECEIPT_BINDING": "a" * 64}
            with self.fixture(rules, environment=environment) as (sidecar, upstream, _events, _config):
                snapshots = []
                with sidecar.connect() as client:
                    for path, expected in (("/allow", 200), ("/block", 403), ("/after", 200)):
                        client.sendall(self.request(path))
                        self.assertEqual(self.response(client)[0], expected)
                        deadline = time.monotonic() + 1.0
                        while not receipt.exists() and time.monotonic() < deadline:
                            time.sleep(0.005)
                        snapshots.append(json.loads(receipt.read_text()))
                        receipt.unlink()
                self.assertEqual(upstream.record_count(), 2)
            self.assertEqual(len({value["transaction_id_sha256"] for value in snapshots}), 3)
            for value in snapshots:
                self.assertIs(value["cleanup_complete"], True)
                self.assertEqual(value["cleanup_status"], "complete")
            self.assertEqual(snapshots[1]["observed_phase_sequence"], ["P1"])

    def test_p2_complete_body_block_then_allow(self):
        rules = 'SecRule REQUEST_BODY "@contains attack" "id:985002,phase:2,deny,status:403,log"'
        with self.fixture(rules) as (sidecar, upstream, _events, _config):
            with sidecar.connect() as client:
                identity = client.getsockname(), client.getpeername(), client.fileno()
                for body, expected in ((b"safe", 200), (b"attack", 403), (b"safe-after", 200)):
                    client.sendall(self.request(body=body))
                    status, response = self.response(client)
                    self.assertEqual(status, expected)
                    self.assertIn(b"Connection: keep-alive", response)
                    self.assertEqual(identity, (client.getsockname(), client.getpeername(), client.fileno()))
                self.assertEqual(upstream.record_count(), 2)

    def test_p1_unread_body_closes(self):
        rules = 'SecRule REQUEST_URI "@streq /block" "id:985003,phase:1,deny,status:403,log"'
        with self.fixture(rules) as (sidecar, upstream, _events, _config):
            with sidecar.connect() as client:
                client.sendall(self.request("/block", body=b"unread")[:-6])
                status, response = self.response(client)
                self.assertEqual(status, 403)
                self.assertIn(b"Connection: close", response)
                self.assertEqual(client.recv(1), b"")
            self.assertEqual(upstream.record_count(), 0)

    def test_request_limit_closes_at_32_without_exchange_33(self):
        with self.fixture() as (sidecar, upstream, _events, _config):
            with sidecar.connect() as client:
                for number in range(1, 33):
                    client.sendall(self.request(f"/request-{number}"))
                    status, response = self.response(client)
                    self.assertEqual(status, 200)
                    self.assertIn(b"Connection: close" if number == 32 else
                                  b"Connection: keep-alive", response)
                self.assertEqual(client.recv(1), b"")
                try:
                    client.sendall(self.request("/request-33"))
                except OSError:
                    pass
            self.assertEqual(upstream.record_count(), 32)

    def test_idle_deadline_releases_connection(self):
        with self.fixture(timeout_ms=120) as (sidecar, upstream, _events, _config):
            with sidecar.connect() as client:
                client.sendall(self.request())
                self.assertEqual(self.response(client)[0], 200)
                started = time.monotonic()
                self.assertEqual(client.recv(1), b"")
                self.assertLess(time.monotonic() - started, 1.0)
            self.assertEqual(upstream.record_count(), 1)

    def test_pipelined_bytes_close_after_first_validated_request(self):
        with self.fixture() as (sidecar, upstream, _events, _config):
            with sidecar.connect() as client:
                client.sendall(self.request() + self.request("/pipelined"))
                status, response = self.response(client)
                self.assertEqual(status, 200)
                self.assertIn(b"Connection: close", response)
                self.assertEqual(client.recv(1), b"")
            self.assertEqual(upstream.record_count(), 1)

    def test_pipelining_during_backend_wait_closes_before_response(self):
        reached = threading.Event()
        release = threading.Event()

        def responder(_request):
            reached.set()
            release.wait(timeout=1.0)
            return b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n"

        with self.fixture(responder=responder) as (sidecar, upstream, _events, _config):
            with sidecar.connect() as client:
                client.sendall(self.request())
                self.assertTrue(reached.wait(timeout=1.0))
                client.sendall(self.request("/pipelined"))
                release.set()
                status, response = self.response(client)
                self.assertEqual(status, 200)
                self.assertIn(b"Connection: close", response)
                self.assertEqual(client.recv(1), b"")
            self.assertEqual(upstream.record_count(), 1)

    def test_explicit_close_token_wins_case_and_list(self):
        for connection in (b"close", b"ClOsE", b"keep-alive, CLOSE"):
            with self.subTest(connection=connection), self.fixture() as (sidecar, upstream, _events, _config):
                with sidecar.connect() as client:
                    client.sendall(self.request(connection=connection))
                    status, response = self.response(client)
                    self.assertEqual(status, 200)
                    self.assertIn(b"Connection: close", response)
                    self.assertEqual(client.recv(1), b"")
                self.assertEqual(upstream.record_count(), 1)

    def _late_followup(self, *, rules, body, status, upstream_count, rule_id=None):
        reached = threading.Event()
        release = threading.Event()

        class HeldBodyHandler(socketserver.BaseRequestHandler):
            def handle(handler):
                handler.request.settimeout(2.0)
                data = bytearray()
                while b"\r\n\r\n" not in data:
                    chunk = handler.request.recv(4096)
                    if not chunk:
                        return
                    data.extend(chunk)
                end = data.index(b"\r\n\r\n") + 4
                expected = contracts._content_length(bytes(data[:end]))
                while len(data) - end < expected:
                    chunk = handler.request.recv(expected - (len(data) - end))
                    if not chunk:
                        return
                    data.extend(chunk)
                handler.server.record(bytes(data))
                handler.request.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\n")
                if data.startswith(b"POST /first "):
                    reached.set()
                    if not release.wait(timeout=2.0):
                        return
                handler.request.sendall(b"ok")

        with tempfile.TemporaryDirectory(dir=contracts._temporary_root()) as temporary:
            snapshots_path = Path(temporary) / "finalized.jsonl"
            with mock.patch.object(contracts, "_RecordingUpstreamHandler", HeldBodyHandler), \
                    mock.patch.object(contracts.StockSidecarLoopbackContractTest,
                                      "binary", self.observed_binary):
                with self.fixture(rules, timeout_ms=2000,
                                  environment={"STOCK_TEST_FINALIZE_LOG": str(snapshots_path)}) as (
                                      sidecar, upstream, events, _config):
                    with sidecar.connect() as client:
                        identity = client.getsockname(), client.getpeername(), client.fileno()
                        client.sendall(self.request("/first"))
                        first_headers = self.response_headers(client)
                        self.assertTrue(reached.wait(timeout=1.0))
                        self.assertIn(b"Connection: keep-alive", first_headers)
                        # First response headers are already committed, but its
                        # body is held: these bytes deliberately arrive late.
                        client.sendall(self.request("/late", body=body))
                        self.assertEqual(upstream.record_count(), 1)
                        self.assertFalse(snapshots_path.exists())
                        release.set()
                        self.assertEqual(client.recv(1) + client.recv(1), b"ok")
                        self.assertEqual(int(first_headers.split(b" ", 2)[1]), 200)
                        second_status, second_response = self.response(client)
                        self.assertEqual(second_status, status)
                        self.assertIn(b"Connection: keep-alive", second_response)
                        self.assertEqual(identity, (client.getsockname(), client.getpeername(), client.fileno()))
                        deadline = time.monotonic() + 1.0
                        while time.monotonic() < deadline:
                            if snapshots_path.exists() and len(snapshots_path.read_text().splitlines()) == 2:
                                break
                            time.sleep(0.005)
                        snapshots = [json.loads(line) for line in snapshots_path.read_text().splitlines()]
                        self.assertEqual(len(snapshots), 2)
                        self.assertEqual(len({value["id"] for value in snapshots}), 2)
                        for value in snapshots:
                            self.assertIs(value["cleaned"], True)
                            self.assertIs(value["finished"], True)
                        self.assertEqual(upstream.record_count(), upstream_count)
                    if rule_id is not None:
                        records = [json.loads(line) for line in events.read_text().splitlines()]
                        matched = [record for record in records if record.get("rule_id") == rule_id]
                        self.assertTrue(matched)
                        self.assertEqual(len({record["transaction_id"] for record in matched}), 1)
                        self.assertNotIn(b"ok", second_response)

    def test_late_allow_is_a_second_validated_exchange(self):
        self._late_followup(rules="", body=b"safe", status=200, upstream_count=2)

    def test_late_p1_block_never_reaches_backend(self):
        self._late_followup(
            rules='SecRule REQUEST_URI "@streq /late" "id:985005,phase:1,deny,status:403,log"',
            body=b"", status=403, upstream_count=1, rule_id="985005")

    def test_late_p2_block_never_reaches_backend(self):
        self._late_followup(
            rules='SecRule REQUEST_BODY "@contains attack" "id:985006,phase:2,deny,status:403,log"',
            body=b"attack", status=403, upstream_count=1, rule_id="985006")

    def test_ambiguous_framing_after_allow_closes_without_backend_release(self):
        malformed = (
            b"POST /bad HTTP/1.1\r\nHost: example.test\r\nContent-Length: 0\r\nContent-Length: 1\r\n\r\n",
            b"POST /bad HTTP/1.1\r\nHost: example.test\r\nContent-Length: 0\r\nTransfer-Encoding: chunked\r\n\r\n",
            b"GET /old HTTP/1.0\r\nHost: example.test\r\n\r\n",
        )
        for request in malformed:
            with self.subTest(request=request), self.fixture() as (sidecar, upstream, _events, _config):
                with sidecar.connect() as client:
                    client.sendall(self.request())
                    self.assertEqual(self.response(client)[0], 200)
                    client.sendall(request)
                    status, response = self.response(client)
                    self.assertEqual(status, 400)
                    self.assertIn(b"Connection: close", response)
                    self.assertEqual(client.recv(1), b"")
                self.assertEqual(upstream.record_count(), 1)

    def test_backend_failure_closes_and_followup_connection_is_clean(self):
        def responder(request):
            if b"/backend-close " in request:
                return b""
            return b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\nConnection: close\r\n\r\nok"
        with self.fixture(responder=responder) as (sidecar, upstream, _events, _config):
            with sidecar.connect() as client:
                client.sendall(self.request())
                self.assertEqual(self.response(client)[0], 200)
                client.sendall(self.request("/backend-close"))
                status, response = self.response(client)
                self.assertEqual(status, 502)
                self.assertIn(b"Connection: close", response)
                self.assertEqual(client.recv(1), b"")
            self.assertEqual(contracts._status(sidecar.exchange(
                self.request("/after", connection=b"close"))), 200)
            self.assertEqual(upstream.record_count(), 3)

    def test_reuse_requires_successful_cleanup_contract(self):
        source = contracts.SIDECAR_SOURCE.read_text()
        self.assertIn("#define SIDECAR_MAX_REQUESTS_PER_CONNECTION 32U", source)
        exchange = source[source.index("static int sidecar_exchange(int"):source.index("#if 0")]
        self.assertLess(exchange.index("finalize_and_snapshot"), exchange.index("return receipt_ready"))
        self.assertIn("receipt_snapshot.contract.error_class == MSCONNECTOR_TRANSACTION_ERROR_NONE", exchange)


if __name__ == "__main__":
    unittest.main()
