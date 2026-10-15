"""Finite-wire client regressions; these do not claim a native NGINX EOS."""
import importlib.util
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import threading
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "ci/runtime/lifecycle/i12/nginx/wire_client.py"
SPEC = importlib.util.spec_from_file_location("i12_nginx_wire_client", SCRIPT)
CLIENT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CLIENT)


def response(headers, body=b"", status=b"HTTP/1.1 200 OK"):
    return status + b"\r\n" + headers + b"\r\n\r\n" + body


class FiniteFramingTests(unittest.TestCase):
    def test_content_length_preserves_binary_entity(self):
        body = b"\x00\xffa\r\nb"
        wire = response(b"cOnTeNt-LeNgTh: 6", body)
        status, headers, actual, framing = CLIENT.entity(wire)
        self.assertEqual((status, actual, framing), (200, body, "http1.1-content-length"))
        self.assertEqual(headers + actual, wire)

    def test_empty_finite_entity(self):
        self.assertEqual(CLIENT.entity(response(b"Content-Length: 0"))[2], b"")

    def test_content_length_rejects_incomplete_and_ambiguous(self):
        for headers, body in [
            (b"Content-Length: 4", b"abc"),
            (b"Content-Length: 2", b"abc"),
            (b"Content-Length: 3\r\nContent-Length: 3", b"abc"),
            (b"Content-Length: 3, 3", b"abc"),
            (b"Content-Length: -0", b""),
            (b"Content-Length: +3", b"abc"),
            (b"Content-Length: 0_3", b"abc"),
            (b"Connection: close", b"abc"),
        ]:
            with self.subTest(headers=headers, body=body), self.assertRaises(ValueError):
                CLIENT.entity(response(headers, body))

    def test_chunked_decodes_only_complete_terminal_framing(self):
        parsed = CLIENT.entity(response(b"Transfer-Encoding: chunked", b"2\r\nab\r\n1\r\nc\r\n0\r\n\r\n"))
        self.assertEqual((parsed[0], parsed[2], parsed[3]), (200, b"abc", "http1.1-chunked"))
        self.assertEqual(CLIENT.entity(response(b"Transfer-Encoding: chunked", b"0\r\n\r\n"))[2], b"")

    def test_chunked_rejects_truncation_and_unsupported_forms(self):
        for body in (b"", b"3", b"3\r\nab", b"3\r\nabc", b"3\r\nabc\r\n", b"0\r\n",
                     b"0\r\n\r\nextra", b"0\r\nTrailer: value\r\n\r\n", b"1;x=1\r\na\r\n0\r\n\r\n",
                     b"+1\r\na\r\n0\r\n\r\n", b"-1\r\n0\r\n\r\n"):
            with self.subTest(body=body), self.assertRaises(ValueError):
                CLIENT.entity(response(b"Transfer-Encoding: chunked", body))

    def test_transfer_encoding_conflicts_are_rejected(self):
        for headers in (b"Transfer-Encoding: chunked\r\nContent-Length: 0",
                        b"Transfer-Encoding: chunked\r\nTransfer-Encoding: chunked",
                        b"Transfer-Encoding: gzip, chunked", b"Transfer-Encoding: identity"):
            with self.subTest(headers=headers), self.assertRaises(ValueError):
                CLIENT.entity(response(headers, b"0\r\n\r\n"))


class WaitedClientTests(unittest.TestCase):
    def execute(self, wire):
        """Use one owned ephemeral listener, and wait for both child and server."""
        failures = []
        with socket.socket() as listener, tempfile.TemporaryDirectory(prefix="i12-wire-") as directory:
            listener.bind(("127.0.0.1", 0))
            listener.listen(1)
            listener.settimeout(5)
            port = listener.getsockname()[1]

            def serve():
                try:
                    stream, _ = listener.accept()
                    with stream:
                        stream.settimeout(5)
                        request = b""
                        while b"\r\n\r\n" not in request:
                            chunk = stream.recv(4096)
                            if not chunk:
                                raise ValueError("client closed before request headers")
                            request += chunk
                        stream.sendall(wire)
                except Exception as exc:
                    failures.append(exc)

            server = threading.Thread(target=serve)
            server.start()
            root = Path(directory)
            request = root / "request.bin"
            request.write_bytes(b"GET / HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n")
            try:
                process = subprocess.run(
                    ["rtk", "proxy", sys.executable, str(SCRIPT), "--port", str(port),
                     "--request", str(request), "--output", str(root / "observation")],
                    capture_output=True, timeout=15, check=False,
                    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"},
                )
            finally:
                server.join(6)
            self.assertFalse(server.is_alive(), "owned loopback server must terminate")
            self.assertEqual(failures, [])
            output = root / "observation"
            observed = json.loads((output / "client-observation.json").read_text())
            self.assertEqual((output / "response.bin").read_bytes(), wire)
            self.assertNotIn("native_eos", observed)
            return process, observed

    def test_complete_response_is_waited_and_eof_is_transport_only(self):
        process, observed = self.execute(response(b"Content-Length: 3", b"abc"))
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertTrue(observed["framing_complete"])
        self.assertTrue(observed["socket_eof"])
        self.assertIsNone(observed["error"])
        self.assertEqual(observed["body_bytes"], 3)
        self.assertLessEqual(observed["first_response_monotonic_ns"], observed["finished_monotonic_ns"])

    def test_eof_does_not_qualify_incomplete_content_length(self):
        process, observed = self.execute(response(b"Content-Length: 4", b"abc"))
        self.assertEqual(process.returncode, 2, process.stderr)
        self.assertTrue(observed["socket_eof"])
        self.assertFalse(observed["framing_complete"])
        self.assertEqual(observed["fragment_bytes"], 3)

    def test_eof_does_not_supply_chunked_terminator(self):
        process, observed = self.execute(response(b"Transfer-Encoding: chunked", b"3\r\nabc\r\n"))
        self.assertEqual(process.returncode, 2, process.stderr)
        self.assertTrue(observed["socket_eof"])
        self.assertFalse(observed["framing_complete"])

    def test_complete_chunked_response(self):
        process, observed = self.execute(response(b"Transfer-Encoding: chunked", b"3\r\nabc\r\n0\r\n\r\n"))
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(observed["body_bytes"], 3)
        self.assertTrue(observed["framing_complete"])

    def test_malformed_status_still_retains_observation(self):
        process, observed = self.execute(response(b"Content-Length: 0", status=b"HTTP/1.1 broken"))
        self.assertEqual(process.returncode, 2, process.stderr)
        self.assertFalse(observed["framing_complete"])
        self.assertIsNotNone(observed["error"])


if __name__ == "__main__":
    unittest.main()
