from __future__ import annotations

import json
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[1]
FRAMEWORK_ROOT = ROOT / "modules" / "ModSecurity-test-Framework"
BACKEND = ROOT / "ci" / "runtime" / "common" / "response-header-test-backend.py"
METADATA = ROOT / "ci" / "runtime" / "common" / "harness-case-metadata.py"


def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


class ResponseHeaderBackendTest(unittest.TestCase):
    def metadata(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(METADATA), *arguments],
            cwd=ROOT,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def test_phase3_cases_materialize_their_declared_upstream_markers(self) -> None:
        fixtures = {
            "phase3_deny_before_commit.yaml": "block",
            "phase3_redirect_before_commit.yaml": "redirect",
        }
        for filename, marker in fixtures.items():
            with self.subTest(filename=filename), tempfile.TemporaryDirectory() as temporary:
                case = (
                    FRAMEWORK_ROOT
                    / "tests"
                    / "cases"
                    / "no-crs-baseline"
                    / "full-lifecycle"
                    / filename
                )
                output = Path(temporary) / "fixture.json"
                result = self.metadata(
                    "response-header-fixture",
                    "--case",
                    str(case),
                    "--framework-root",
                    str(FRAMEWORK_ROOT),
                    "--output",
                    str(output),
                )
                self.assertEqual(0, result.returncode, result.stderr)
                fixture = json.loads(output.read_text(encoding="utf-8"))
                self.assertEqual(200, fixture["status"])
                self.assertEqual([["X-Modsec-Upstream", marker]], fixture["headers"])

    def test_backend_uses_declarative_status_and_marker_header(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            body_file = root / "body.txt"
            fixture_file = root / "fixture.json"
            body_file.write_text("phase3 <marker>", encoding="utf-8")
            fixture_file.write_text(
                json.dumps(
                    {
                        "status": 201,
                        "headers": [
                            ["X-Modsec-Upstream", "block"],
                            ["Content-Type", "text/plain; charset=utf-8"],
                        ],
                    }
                ),
                encoding="utf-8",
            )
            port = free_port()
            process = subprocess.Popen(
                [
                    sys.executable,
                    str(BACKEND),
                    "--port",
                    str(port),
                    "--body-file",
                    str(body_file),
                    "--safe-root",
                    str(root),
                    "--fixture-file",
                    str(fixture_file),
                ],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            try:
                last_error: Exception | None = None
                for _ in range(40):
                    try:
                        with urlopen(f"http://127.0.0.1:{port}/", timeout=0.25) as response:
                            self.assertEqual(201, response.status)
                            self.assertEqual("block", response.headers["X-Modsec-Upstream"])
                            self.assertEqual("text/plain; charset=utf-8", response.headers["Content-Type"])
                            self.assertEqual(b"phase3 &lt;marker&gt;", response.read())
                        break
                    except OSError as exc:
                        last_error = exc
                        time.sleep(0.05)
                else:
                    self.fail(f"response-header backend did not start: {last_error}")
            finally:
                if process.poll() is None:
                    process.terminate()
                process.wait(timeout=5)
                if process.stdout is not None:
                    process.stdout.close()
                if process.stderr is not None:
                    process.stderr.close()

    def test_invalid_fixture_headers_are_rejected_before_listening(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            body_file = root / "body.txt"
            fixture_file = root / "fixture.json"
            body_file.write_text("body", encoding="utf-8")
            fixture_file.write_text(
                json.dumps({"status": 200, "headers": [["X-Test", "ok\r\nInjected: yes"]]}),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(BACKEND),
                    "--port",
                    "1",
                    "--body-file",
                    str(body_file),
                    "--safe-root",
                    str(root),
                    "--fixture-file",
                    str(fixture_file),
                ],
                cwd=ROOT,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("invalid response header value", result.stderr)

    def test_apache_phase4_mode_is_case_metadata_and_is_validated(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            case = Path(temporary) / "apache-mode.yaml"
            case.write_text(
                """\
name: apache_mode_metadata
rules: |
  SecRuleEngine On
request:
  method: GET
  path: /
response:
  body: body
apache:
  phase4_mode: strict
expect:
  status: 200
""",
                encoding="utf-8",
            )
            result = self.metadata(
                "apache-phase4-mode",
                "--case",
                str(case),
                "--framework-root",
                str(FRAMEWORK_ROOT),
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual("strict\n", result.stdout)

            case.write_text(case.read_text(encoding="utf-8").replace("strict", "unsafe"), encoding="utf-8")
            invalid = self.metadata(
                "apache-phase4-mode",
                "--case",
                str(case),
                "--framework-root",
                str(FRAMEWORK_ROOT),
            )
        self.assertNotEqual(0, invalid.returncode)
        self.assertIn("apache.phase4_mode", invalid.stderr)

    def test_both_host_harnesses_use_the_fixture_for_any_response_headers_rule(self) -> None:
        apache = (ROOT / "connectors" / "apache" / "harness" / "run_apache_smoke.sh").read_text(
            encoding="utf-8"
        )
        nginx = (ROOT / "connectors" / "nginx" / "harness" / "run_nginx_smoke.sh").read_text(
            encoding="utf-8"
        )
        for name, harness in (("apache", apache), ("nginx", nginx)):
            with self.subTest(harness=name):
                self.assertIn("RESPONSE_HEADERS([[:space:]:]|$)", harness)
                self.assertIn('--fixture-file "$RESPONSE_HEADER_FIXTURE_FILE"', harness)
                self.assertIn("response-header-fixture", harness)

        template = (ROOT / "connectors" / "apache" / "harness" / "apache_smoke.conf").read_text(
            encoding="utf-8"
        )
        self.assertIn("@@APACHE_PHASE4_MODE@@", template)
        self.assertNotIn("modsecurity_phase4_mode safe", template)
        self.assertIn("resolve_apache_phase4_mode", apache)


if __name__ == "__main__":
    unittest.main()
