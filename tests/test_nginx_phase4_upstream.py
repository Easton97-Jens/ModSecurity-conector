"""Actual loopback wire checks for the bounded split response fixture."""
import importlib.util
from pathlib import Path
import socket
import unittest

PATH = Path(__file__).resolve().parents[1] / "ci/runtime/common/nginx_phase4_upstream.py"
SPEC = importlib.util.spec_from_file_location("phase4_upstream", PATH)
upstream = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(upstream)


class Phase4UpstreamTest(unittest.TestCase):
    def test_actual_two_chunk_frames_and_explicit_eos(self):
        with upstream.BoundedPhase4Upstream((b"no-crs-response-", b"body-marker"), pause=True) as server:
            with socket.create_connection(("127.0.0.1", server.port), timeout=2) as client:
                client.sendall(b"GET /probe HTTP/1.1\r\nHost: localhost\r\n\r\n")
                first = b""
                while b"10\r\nno-crs-response-\r\n" not in first:
                    first += client.recv(4096)
                self.assertNotIn(b"body-marker", first)
                self.assertTrue(server.paused.wait(2))
                self.assertFalse(server.eos_sent.is_set())
                server.release.set()
                rest = b""
                while data := client.recv(4096):
                    rest += data
                self.assertIn(b"b\r\nbody-marker\r\n0\r\n\r\n", rest)
            self.assertTrue(server.finished.wait(2))
            observations = server.observations()
            self.assertEqual(observations["chunk_sizes_sent"], [16, 11])
            self.assertTrue(observations["eos_sent"])
            self.assertNotIn("body", observations)

    def test_unknown_network_address_or_unbounded_input_rejected(self):
        for chunks in ((), (b"",), (b"x" * 4097,), (b"x",) * 9, ("text",)):
            with self.subTest(chunks=tuple(len(c) for c in chunks)), self.assertRaises(ValueError):
                upstream.BoundedPhase4Upstream(chunks)

    def test_unreleased_barrier_is_bounded_and_not_successful_eos(self):
        with upstream.BoundedPhase4Upstream((b"first", b"last"), pause=True, barrier_timeout=0.1) as server:
            with socket.create_connection(("127.0.0.1", server.port), timeout=2) as client:
                client.sendall(b"GET /probe HTTP/1.1\r\nHost: localhost\r\n\r\n")
                while client.recv(4096):
                    pass
            self.assertTrue(server.finished.wait(2))
            self.assertFalse(server.observations()["eos_sent"])
            self.assertEqual(server.observations()["error_class"], "barrier_timeout")


if __name__ == "__main__":
    unittest.main()
