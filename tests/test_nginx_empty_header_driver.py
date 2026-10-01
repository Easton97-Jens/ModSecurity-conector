"""Real loopback HTTP controls for the NGINX case request driver."""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import threading
import unittest


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "connectors/nginx/harness/run_nginx_smoke.sh"


class NginxEmptyHeaderDriverTest(unittest.TestCase):
    def send_headers(self, headers: str) -> dict[str, object]:
        curl = shutil.which("curl")
        self.assertIsNotNone(curl, "real curl is required for this driver regression")
        received: dict[str, object] = {}

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:
                received.update(
                    empty=self.headers.get_all("X-No-Crs-Empty"),
                    duplicate=self.headers.get_all("X-No-Crs-Duplicate"),
                    ordinary=self.headers.get_all("X-No-Crs-Ordinary"),
                    request_version=self.request_version,
                )
                self.send_response(200)
                self.send_header("Content-Length", "2")
                self.end_headers()
                self.wfile.write(b"ok")

            def log_message(self, _format: str, *args: object) -> None:
                pass

        server = HTTPServer(("127.0.0.1", 0), Handler)
        server.timeout = 3.0
        thread = threading.Thread(target=server.handle_request, daemon=True)
        with tempfile.TemporaryDirectory(prefix="nginx-empty-header-") as temporary:
            attempt = Path(temporary)
            header_file = attempt / "headers.txt"
            header_file.write_text(headers, encoding="utf-8")
            match = re.search(
                r"^send_case_request\(\) \{\n.*?^\}",
                HARNESS.read_text(encoding="utf-8"), re.MULTILINE | re.DOTALL,
            )
            self.assertIsNotNone(match)
            # Path-authority helpers are covered separately. Only this actual
            # shell function creates the request; the server observes the wire.
            script = (
                "set -eu\n"
                "validate_nginx_request_output_path() { :; }\n"
                "quote_request_path() { printf '%s\\n' \"$1\"; }\n"
                "blocked() { exit 77; }\n"
                f"{match.group(0)}\n"
                "send_case_request\n"
            )
            environment = {
                "PATH": os.defpath,
                "CURL_BIN": str(curl),
                "NGINX_DOWNSTREAM_PROTOCOL": "http1",
                "RESPONSE_BODY": str(attempt / "body.txt"),
                "LOG_DIR": str(attempt),
                "REQUEST_METHOD": "GET",
                "REQUEST_HEADERS_FILE": str(header_file),
                "REQUEST_HAS_BODY": "0",
                "REQUEST_PATH": "/no-crs/headers/empty",
                "SEND_CASE_MAX_TIME_SECONDS": "2",
                "PORT": str(server.server_port),
            }
            thread.start()
            try:
                completed = subprocess.run(
                    ["sh", "-c", script], env=environment,
                    capture_output=True, text=True, timeout=5, check=False,
                )
                self.assertEqual(completed.returncode, 0, completed.stderr)
                self.assertEqual(completed.stdout, "200")
                self.assertEqual((attempt / "body.txt").read_bytes(), b"ok")
            finally:
                thread.join(timeout=4)
                server.server_close()
            self.assertFalse(thread.is_alive(), "attempt-owned HTTP server must stop")
        self.assertEqual(received.get("request_version"), "HTTP/1.1")
        return received

    def test_empty_value_is_a_present_header_not_curl_suppression(self) -> None:
        received = self.send_headers("X-No-Crs-Empty: \n")
        self.assertEqual(received["empty"], [""])

    def test_absent_header_remains_absent(self) -> None:
        self.assertIsNone(self.send_headers("")["empty"])

    def test_nonempty_and_duplicate_headers_are_preserved(self) -> None:
        received = self.send_headers(
            "X-No-Crs-Ordinary: one: two\n"
            "X-No-Crs-Duplicate: one\n"
            "X-No-Crs-Duplicate: two\n"
        )
        self.assertEqual(received["ordinary"], ["one: two"])
        self.assertEqual(received["duplicate"], ["one", "two"])


if __name__ == "__main__":
    unittest.main()
