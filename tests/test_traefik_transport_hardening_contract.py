from __future__ import annotations

import http.server
import importlib.util
import sys
import threading
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_SCRIPT = ROOT / "connectors" / "traefik" / "scripts" / "runtime_native_smoke.py"


def load_runtime_module() -> object:
    specification = importlib.util.spec_from_file_location("traefik_runtime_native_smoke", RUNTIME_SCRIPT)
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


class _KeepAliveHandler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_POST(self) -> None:  # noqa: N802 - http.server callback shape
        size = int(self.headers.get("Content-Length", "0"))
        if size:
            self.rfile.read(size)
        body = b"payload-free-test-body\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, _format: str, *_args: object) -> None:
        return


class TraefikTransportHardeningContractTest(unittest.TestCase):
    def test_safe_followup_requires_the_same_http11_connection(self) -> None:
        runtime = load_runtime_module()
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _KeepAliveHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            observation = runtime.keepalive_safe_followup(
                server.server_port,
                b"request-body",
                "safe-transaction",
                "followup-transaction",
            )
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)

        self.assertTrue(observation["connection_reused"])
        self.assertEqual(200, observation["safe_status"])
        self.assertEqual(200, observation["followup_status"])
        self.assertTrue(observation["safe_first_byte_received"])
        self.assertTrue(observation["followup_first_byte_received"])

    def test_nonpromoting_sidecar_and_strict_boundary_are_explicit(self) -> None:
        source = RUNTIME_SCRIPT.read_text(encoding="utf-8")
        self.assertIn('"artifact_profile": "native-transport-diagnostic-nonpromoting"', source)
        self.assertIn('"diagnostic_case": "keepalive_safe_followup"', source)
        self.assertIn('"canonical_evidence": False', source)
        self.assertIn('"diagnostic_only": True', source)
        self.assertNotIn('"transport_case_id":', source)
        self.assertIn('"connection_reused": bool(keepalive_observation["connection_reused"])', source)
        self.assertIn('"state": "NOT_EXECUTED"', source)
        self.assertIn('"client_visible_abort": False', source)


if __name__ == "__main__":
    unittest.main()
