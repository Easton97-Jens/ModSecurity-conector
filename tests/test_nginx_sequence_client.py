"""The sequence client must prove reuse without silently reconnecting."""
import importlib.util
from pathlib import Path
import socketserver
import threading
import unittest

SPEC = importlib.util.spec_from_file_location(
    "nginx_sequence_client", Path(__file__).resolve().parents[1] / "ci/runtime/lifecycle/nginx_sequence_client.py")
CLIENT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CLIENT)


class Handler(socketserver.StreamRequestHandler):
    def handle(self):
        self.server.connections += 1
        for _ in range(3):
            first = self.rfile.readline(4096)
            if not first:
                return
            headers = []
            while True:
                line = self.rfile.readline(4096)
                if line == b"\r\n":
                    break
                headers.append(line)
            code = 403 if b"X-Modsec-Smoke: block\r\n" in headers else 200
            mode = b"close" if self.server.force_close else b"keep-alive"
            self.wfile.write(b"HTTP/1.1 " + str(code).encode() + b" Test\r\nContent-Length: 2\r\nConnection: " + mode + b"\r\n\r\nok")
            self.wfile.flush()
            if self.server.force_close or b"Connection: close\r\n" in headers:
                return


class ClientTests(unittest.TestCase):
    def server(self, close=False):
        server = socketserver.ThreadingTCPServer(("127.0.0.1", 0), Handler)
        server.daemon_threads = True
        server.force_close = close
        server.connections = 0
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        return server

    def test_actual_three_requests_use_one_connection(self):
        server = self.server()
        actual = CLIENT.run_sequence(server.server_address[1], ["/no-crs/sequence/0", "/no-crs/sequence/1", "/no-crs/sequence/2"], (200, 403, 200), keepalive=True)
        self.assertEqual([row["observed_status"] for row in actual], [200, 403, 200])
        self.assertEqual(server.connections, 1)

    def test_close_is_not_repaired_by_hidden_reconnect(self):
        server = self.server(close=True)
        with self.assertRaisesRegex(ValueError, "closed the connection"):
            CLIENT.run_sequence(server.server_address[1], ["/no-crs/sequence/0", "/no-crs/sequence/1"], (200, 200), keepalive=True)
        self.assertEqual(server.connections, 1)

    def test_sequential_independent_connections_are_distinct(self):
        server = self.server()
        CLIENT.run_sequence(server.server_address[1], ["/no-crs/sequence/0", "/no-crs/sequence/1"], (200, 200), keepalive=False)
        self.assertEqual(server.connections, 2)

    def test_path_injection_is_rejected_before_connection(self):
        with self.assertRaises(ValueError):
            CLIENT.run_sequence(19000, ["/x\r\nX: y"], (200,), keepalive=True)


if __name__ == "__main__":
    unittest.main()
