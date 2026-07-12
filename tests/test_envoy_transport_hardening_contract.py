from __future__ import annotations

import http.server
import importlib.util
import sys
import threading
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HELPER_PATH = ROOT / "connectors" / "envoy" / "harness" / "envoy_smoke_helper.py"
RUNTIME_PATH = ROOT / "connectors" / "envoy" / "harness" / "run_envoy_ext_proc_runtime.sh"


def load_helper() -> object:
    specification = importlib.util.spec_from_file_location("envoy_smoke_helper", HELPER_PATH)
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


class EnvoyTransportHardeningContractTest(unittest.TestCase):
    def test_client_cancel_waits_for_one_real_body_byte_then_closes(self) -> None:
        helper = load_helper()

        class FastCancelHandler(helper.UpstreamHandler):
            client_cancel_delay_seconds = 0.05

        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), FastCancelHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            observation = helper.client_cancel(
                "127.0.0.1",
                server.server_port,
                "/client-cancel",
                ["X-Request-Id: cancel-test"],
            )
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)

        self.assertEqual(200, observation["http_status"])
        self.assertTrue(observation["first_body_byte_received"])
        self.assertTrue(observation["client_closed"])

    def test_client_cancel_rejects_non_ascii_wire_headers(self) -> None:
        helper = load_helper()
        with self.assertRaises(ValueError):
            helper.client_cancel("127.0.0.1", 18080, "/client-cancel", ["X-Test: snowman-☃"])

    def test_runtime_probe_keeps_cancellation_unattributed_and_nonpromoting(self) -> None:
        source = RUNTIME_PATH.read_text(encoding="utf-8")
        self.assertIn("ENVOY_TRANSPORT_CANCEL_PROBE", source)
        self.assertIn("grpc_context_canceled_unattributed", source)
        self.assertIn("grpc_peer_eof", source)
        self.assertIn("expected exactly one unattributed ext_proc terminal completion", source)
        self.assertIn("client_disconnect_after_first_response_chunk", source)
        self.assertIn("transport-observations.diagnostic.json", source)
        self.assertIn('"capability_promotion": "not_permitted"', source)
        self.assertIn('"state": "NOT_EXECUTED"', source)
        self.assertIn('"diagnostic_only": True', source)
        self.assertNotIn('"transport_case_id":', source)
        self.assertIn("client-cancel", source)


if __name__ == "__main__":
    unittest.main()
