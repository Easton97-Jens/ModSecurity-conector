"""Boundary and verdict controls for stock-native supplementary diagnostics."""
import importlib.util
from pathlib import Path
import tempfile
import socket
import threading
import unittest


SPEC = importlib.util.spec_from_file_location("lighttpd_i12_diagnostic",
    Path(__file__).resolve().parents[1] / "ci/runtime/lifecycle/i12/lighttpd/diagnostic_capture.py")
DIAGNOSTIC = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DIAGNOSTIC)


class DiagnosticTests(unittest.TestCase):
    def test_real_peer_response_over_bound_is_rejected_and_socket_closes(self):
        with socket.socket() as server:
            server.bind(("127.0.0.1", 0))
            server.listen(1)
            server.settimeout(3)
            def peer():
                with server.accept()[0] as client:
                    client.recv(65536)
                    try:
                        client.sendall(b"HTTP/1.1 200 OK\r\n\r\n" + b"x" * 140000)
                    except (BrokenPipeError, ConnectionResetError):
                        pass
            thread = threading.Thread(target=peer)
            thread.start()
            try:
                with self.assertRaisesRegex(ValueError, "128 KiB"):
                    DIAGNOSTIC.request(server.getsockname()[1])
            finally:
                thread.join(timeout=5)
            self.assertFalse(thread.is_alive())

    def test_negative_parser_acceptance_and_signals_cannot_succeed(self):
        receipt = {"configuration_probes": [{"exitcode": code} for code in [0] + [255] * 7],
                   "clients": [{"status": code} for code in [200, 403, 200]]}
        self.assertTrue(DIAGNOSTIC.controls_match(receipt))
        for code in (0, -9):
            receipt["configuration_probes"][3]["exitcode"] = code
            self.assertFalse(DIAGNOSTIC.controls_match(receipt))
        receipt["configuration_probes"][3]["exitcode"] = 255
        receipt["clients"][2]["status"] = 500
        self.assertFalse(DIAGNOSTIC.controls_match(receipt))

    def test_output_parent_alias_existing_and_private_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "alias").symlink_to(root, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "physical"):
                DIAGNOSTIC.fresh_output(root / "alias/child")
            actual = DIAGNOSTIC.fresh_output(root / "physical")
            self.assertEqual(actual.stat().st_mode & 0o777, 0o700)
            with self.assertRaisesRegex(ValueError, "Fresh"):
                DIAGNOSTIC.fresh_output(actual)


if __name__ == "__main__":
    unittest.main()
