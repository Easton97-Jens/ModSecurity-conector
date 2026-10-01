"""Exercise the NGINX case request command at its shell function boundary."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "connectors/nginx/harness/run_nginx_smoke.sh"


class NginxH1RequestProtocolTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.capture = self.root / "curl-args.json"
        self.curl = self.root / "capture-curl"
        self.curl.write_text(
            "#!/usr/bin/env python3\n"
            "import json, os, sys\n"
            "with open(os.environ['CURL_CAPTURE'], 'w', encoding='utf-8') as stream:\n"
            "    json.dump(sys.argv[1:], stream)\n"
            "print('200', end='')\n",
            encoding="utf-8",
        )
        self.curl.chmod(0o700)
        self.headers = self.root / "request-headers.txt"
        self.headers.write_text("X-Smoke: first\nX-Smoke: second\n", encoding="utf-8")
        self.body = self.root / "request-body.bin"
        self.body.write_bytes(b"probe body")

    def run_request(self, protocol: str) -> subprocess.CompletedProcess[str]:
        harness = HARNESS.read_text(encoding="utf-8")
        match = re.search(r"^send_case_request\(\) \{\n.*?^\}", harness, re.MULTILINE | re.DOTALL)
        self.assertIsNotNone(match)
        # These controlled collaborators only capture the function's curl
        # command; the host path validator and path encoder are separate seams.
        script = (
            "set -eu\n"
            "validate_nginx_request_output_path() { :; }\n"
            "quote_request_path() { printf '%s\\n' \"$1\"; }\n"
            "blocked() { printf '%s\\n' \"$*\" >&2; exit 77; }\n"
            f"{match.group(0)}\n"
            "send_case_request\n"
        )
        environment = os.environ.copy()
        environment.update(
            CURL_BIN=str(self.curl),
            CURL_CAPTURE=str(self.capture),
            NGINX_DOWNSTREAM_PROTOCOL=protocol,
            RESPONSE_BODY=str(self.root / "response.txt"),
            LOG_DIR=str(self.root),
            REQUEST_METHOD="POST",
            REQUEST_HEADERS_FILE=str(self.headers),
            REQUEST_BODY_FILE=str(self.body),
            REQUEST_HAS_BODY="1",
            REQUEST_PATH="/no-crs/allow",
            SEND_CASE_MAX_TIME_SECONDS="2",
            PORT="18080",
        )
        return subprocess.run(
            ["sh", "-c", script],
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_h1_request_forces_http11_without_curlrc_and_preserves_payload(self) -> None:
        completed = self.run_request("http1")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout, "200")
        args = json.loads(self.capture.read_text(encoding="utf-8"))
        self.assertEqual(args[:2], ["-q", "--http1.1"])
        self.assertEqual(args[args.index("-X") + 1], "POST")
        self.assertEqual(args[args.index("-o") + 1], str(self.root / "response.txt"))
        self.assertEqual(args[args.index("-w") + 1], "%{http_code}")
        self.assertEqual(args[args.index("--max-time") + 1], "2")
        self.assertEqual(
            [args[position + 1] for position, value in enumerate(args) if value == "-H"],
            ["X-Smoke: first", "X-Smoke: second"],
        )
        self.assertEqual(args[args.index("--data-binary") + 1], f"@{self.body}")
        self.assertEqual(args[-1], "http://127.0.0.1:18080/no-crs/allow")

    def test_non_h1_profile_never_sends_legacy_case_request(self) -> None:
        for protocol in ("h2", "h3"):
            with self.subTest(protocol=protocol):
                completed = self.run_request(protocol)
                self.assertEqual(completed.returncode, 77, completed.stderr)
                self.assertIn("requires NGINX_DOWNSTREAM_PROTOCOL=http1", completed.stderr)
                self.assertFalse(self.capture.exists())


if __name__ == "__main__":
    unittest.main()
