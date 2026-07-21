"""Regression coverage for bounded local runtime-smoke request bodies."""

from __future__ import annotations

import http.client
import importlib.util
import io
from email.message import Message
from pathlib import Path
import socket
import tempfile
import unittest


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "common/scripts/run_local_runtime_smoke.py"
SPEC = importlib.util.spec_from_file_location("local_runtime_smoke", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
SMOKE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SMOKE)


class RecordingBackend:
    decision_backend = "test"

    def __init__(self) -> None:
        self.last_error: str | None = None
        self.bodies: list[bytes] = []

    def decide(
        self,
        headers: http.client.HTTPMessage,
        path: str,
        method: str = "GET",
        body: bytes = b"",
    ) -> dict[str, object]:
        del headers, path, method
        self.bodies.append(body)
        return {"status": 200, "body": b"ok\n"}


class RequestBodyReader:
    def __init__(self, headers: Message, body: bytes) -> None:
        self.headers = headers
        self.rfile = io.BytesIO(body)


class LocalRuntimeSmokeRequestBodyTest(unittest.TestCase):
    def start_server(self, handler: type[SMOKE.QuietHandler]) -> SMOKE.LocalSmokeHTTPServer:
        server = SMOKE.start_http_server(handler, 0)
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        return server

    def post(self, port: int, body: bytes) -> int:
        connection = http.client.HTTPConnection("127.0.0.1", port, timeout=3)
        try:
            connection.request("POST", "/", body=body, headers={"Content-Length": str(len(body))})
            response = connection.getresponse()
            response.read()
            return int(response.status)
        finally:
            connection.close()

    def raw_status(self, port: int, request: bytes) -> int:
        with socket.create_connection(("127.0.0.1", port), timeout=3) as connection:
            connection.sendall(request)
            connection.shutdown(socket.SHUT_WR)
            response = bytearray()
            while b"\r\n" not in response:
                received = connection.recv(4096)
                if not received:
                    break
                response.extend(received)
        status_line = bytes(response).split(b"\r\n", 1)[0].split()
        self.assertGreaterEqual(len(status_line), 2, response)
        return int(status_line[1])

    def assert_handlers_reject_without_processing(self, request: bytes) -> None:
        decision_backend = RecordingBackend()
        decision_server = self.start_server(SMOKE.make_decision_handler(decision_backend))
        self.assertEqual(self.raw_status(decision_server.server_port, request), 400)
        self.assertEqual(decision_backend.bodies, [])

        forwarded_methods: list[str] = []

        class RecordingUpstream(SMOKE.QuietHandler):
            def do_POST(self) -> None:
                forwarded_methods.append(self.command)
                self.send_response(200)
                self.send_header("Content-Length", "0")
                self.end_headers()

        with tempfile.TemporaryDirectory() as temporary:
            sidecar_backend = RecordingBackend()
            upstream_server = self.start_server(RecordingUpstream)
            sidecar_server = self.start_server(
                SMOKE.make_sidecar_proxy_handler(
                    sidecar_backend,
                    upstream_server.server_port,
                    Path(temporary) / "sidecar.jsonl",
                ),
            )
            self.assertEqual(self.raw_status(sidecar_server.server_port, request), 400)
            self.assertEqual(sidecar_backend.bodies, [])
            self.assertEqual(forwarded_methods, [])

    def test_decision_and_sidecar_handlers_accept_exact_content_length_limit(self) -> None:
        body = b"a" * SMOKE.MAX_REQUEST_BODY_BYTES
        decision_backend = RecordingBackend()
        decision_server = self.start_server(SMOKE.make_decision_handler(decision_backend))
        self.assertEqual(self.post(decision_server.server_port, body), 200)
        self.assertEqual(decision_backend.bodies, [body])

        with tempfile.TemporaryDirectory() as temporary:
            sidecar_backend = RecordingBackend()
            upstream_server = self.start_server(SMOKE.UpstreamHandler)
            transcript = Path(temporary) / "sidecar.jsonl"
            sidecar_server = self.start_server(
                SMOKE.make_sidecar_proxy_handler(sidecar_backend, upstream_server.server_port, transcript),
            )
            self.assertEqual(self.post(sidecar_server.server_port, body), 200)
            self.assertEqual(sidecar_backend.bodies, [body])

    def test_decision_and_sidecar_handlers_reject_oversized_content_length(self) -> None:
        request = (
            b"POST / HTTP/1.1\r\nHost: local\r\nContent-Length: "
            + str(SMOKE.MAX_REQUEST_BODY_BYTES + 1).encode("ascii")
            + b"\r\n\r\n"
        )
        decision_backend = RecordingBackend()
        decision_server = self.start_server(SMOKE.make_decision_handler(decision_backend))
        self.assertEqual(self.raw_status(decision_server.server_port, request), 413)
        self.assertEqual(decision_backend.bodies, [])

        with tempfile.TemporaryDirectory() as temporary:
            sidecar_backend = RecordingBackend()
            sidecar_server = self.start_server(
                SMOKE.make_sidecar_proxy_handler(sidecar_backend, 1, Path(temporary) / "sidecar.jsonl"),
            )
            self.assertEqual(self.raw_status(sidecar_server.server_port, request), 413)
            self.assertEqual(sidecar_backend.bodies, [])

    def test_decision_and_sidecar_handlers_reject_conflicting_body_framing(self) -> None:
        request = (
            b"POST / HTTP/1.1\r\n"
            b"Host: local\r\n"
            b"Transfer-Encoding: chunked\r\n"
            b"Content-Length: 5\r\n"
            b"\r\n"
            b"0\r\n\r\n"
        )
        self.assert_handlers_reject_without_processing(request)

    def test_decision_and_sidecar_handlers_reject_duplicate_content_length(self) -> None:
        for first, second in ((b"0", b"0"), (b"0", b"5")):
            with self.subTest(first=first, second=second):
                request = (
                    b"POST / HTTP/1.1\r\n"
                    b"Host: local\r\n"
                    b"Content-Length: "
                    + first
                    + b"\r\nContent-Length: "
                    + second
                    + b"\r\n\r\n"
                )
                self.assert_handlers_reject_without_processing(request)

    def test_decision_and_sidecar_handlers_reject_duplicate_transfer_encoding(self) -> None:
        request = (
            b"POST / HTTP/1.1\r\n"
            b"Host: local\r\n"
            b"Transfer-Encoding: chunked\r\n"
            b"Transfer-Encoding: chunked\r\n"
            b"\r\n"
            b"0\r\n\r\n"
        )
        self.assert_handlers_reject_without_processing(request)

    def test_reader_rejects_zero_content_length_with_transfer_encoding(self) -> None:
        headers = Message()
        headers["transfer-encoding"] = "chunked"
        headers["content-length"] = "0"
        with self.assertRaises(SMOKE.RequestBodyError):
            SMOKE.read_request_body(RequestBodyReader(headers, b"0\r\n\r\n"))

    def test_chunked_reader_accepts_exact_limit_and_rejects_cumulative_overflow(self) -> None:
        headers = Message()
        headers["Transfer-Encoding"] = "chunked"
        exact_body = b"a" * SMOKE.MAX_REQUEST_BODY_BYTES
        exact_request = (
            f"{len(exact_body):X}\r\n".encode("ascii")
            + exact_body
            + b"\r\n0\r\n\r\n"
        )
        self.assertEqual(
            SMOKE.read_request_body(RequestBodyReader(headers, exact_request)),
            exact_body,
        )
        overflow_request = exact_request[:-5] + b"1\r\nb\r\n0\r\n\r\n"
        with self.assertRaises(SMOKE.RequestBodyTooLarge):
            SMOKE.read_request_body(RequestBodyReader(headers, overflow_request))

    def test_reader_rejects_malformed_and_incomplete_request_bodies(self) -> None:
        chunked_headers = Message()
        chunked_headers["Transfer-Encoding"] = "chunked"
        with self.assertRaises(SMOKE.RequestBodyError):
            SMOKE.read_request_body(RequestBodyReader(chunked_headers, b"not-hex\r\n"))
        length_headers = Message()
        length_headers["Content-Length"] = "2"
        with self.assertRaises(SMOKE.RequestBodyError):
            SMOKE.read_request_body(RequestBodyReader(length_headers, b"x"))

    def test_accepted_connections_receive_a_finite_socket_deadline(self) -> None:
        observed: list[float | None] = []

        class DeadlineHandler(SMOKE.QuietHandler):
            def do_GET(self) -> None:
                observed.append(self.connection.gettimeout())
                self.send_response(200)
                self.send_header("Content-Length", "0")
                self.end_headers()

        server = self.start_server(DeadlineHandler)
        connection = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=3)
        try:
            connection.request("GET", "/")
            response = connection.getresponse()
            response.read()
            self.assertEqual(response.status, 200)
        finally:
            connection.close()
        self.assertEqual(observed, [SMOKE.SERVER_SOCKET_TIMEOUT_SECONDS])


if __name__ == "__main__":
    unittest.main()
