"""Real-frame parser and original sequence-contract regressions; no Apache host."""

import importlib.util
from pathlib import Path
import socket
import unittest


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "ci/runtime/lifecycle/apache-i12/acceptance/keepalive.py"
SPEC = importlib.util.spec_from_file_location("apache_i12_keepalive", PATH)
KEEPALIVE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(KEEPALIVE)


class CapturedSocket:
    """Feed exact captured-like TCP fragments without opening a listener."""
    def __init__(self, chunks):
        self.chunks = list(chunks)

    def recv(self, _size):
        return self.chunks.pop(0) if self.chunks else b""


class KeepaliveTest(unittest.TestCase):
    def plan(self, case_id):
        return {"case_id": case_id, "request": {"method": "GET", "path": "/principal",
            "headers": [["X-I12-ID", "unique-main"]], "body": {"bytes": 0}, "chunks": []},
            "backend": {"body": None}, "driver_seams": ["raw_connection_sequence_transaction_join"]}

    def test_exact_original_allow_deny_allow_families_have_three_unique_transactions(self):
        for case_id in KEEPALIVE.DENY_SEQUENCES:
            steps = KEEPALIVE.sequence_requests(self.plan(case_id))
            self.assertEqual([x["label"] for x in steps], ["main", "sequence-deny", "sequence-followup"])
            self.assertIn(["X-Modsec-Smoke", "block"], steps[1]["request"]["headers"])
            ids = [next(v for k, v in x["request"]["headers"] if k == "X-I12-ID") for x in steps]
            self.assertEqual(len(ids), len(set(ids)))

    def test_content_length_response_is_drained_without_waiting_for_eof(self):
        reader = KEEPALIVE.ResponseReader(CapturedSocket([
            b"HTTP/1.1 200 OK\r\nContent-Length: 3\r\n\r\na", b"bc"]))
        response, raw, body = reader.read_response()
        self.assertEqual(body, b"abc")
        self.assertTrue(response["framing_complete"])
        self.assertFalse(response["tcp_eof_observed"])
        self.assertTrue(response["connection_reusable_by_headers"])
        self.assertTrue(raw.endswith(b"abc"))

    def test_real_kernel_stream_reads_two_frames_while_peer_remains_open(self):
        # A socketpair exercises actual kernel reads without starting a host
        # or a network listener; this is parser evidence, not Apache evidence.
        first = b"HTTP/1.1 200 OK\r\nContent-Length: 3\r\n\r\none"
        second = b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n3\r\ntwo\r\n0\r\n\r\n"
        left, right = socket.socketpair()
        self.addCleanup(left.close)
        self.addCleanup(right.close)
        left.settimeout(1)
        right.sendall(first + second)
        reader = KEEPALIVE.ResponseReader(left)
        response, raw, body = reader.read_response()
        self.assertEqual((raw, body), (first, b"one"))
        self.assertFalse(response["tcp_eof_observed"])
        response, raw, body = reader.read_response()
        self.assertEqual((raw, body), (second, b"two"))
        self.assertFalse(response["tcp_eof_observed"])

    def test_two_distinct_responses_buffered_correctly_not_concatenated_bodies(self):
        first = b"HTTP/1.1 200 OK\r\nContent-Length: 3\r\n\r\none"
        second = b"HTTP/1.1 403 Denied\r\nContent-Length: 3\r\n\r\ntwo"
        reader = KEEPALIVE.ResponseReader(CapturedSocket([first + second]))
        response, raw, body = reader.read_response()
        self.assertEqual((response["status"], raw, body), (200, first, b"one"))
        response, raw, body = reader.read_response()
        self.assertEqual((response["status"], raw, body), (403, second, b"two"))

    def test_chunked_response_trailers_are_consumed_before_next_status_line(self):
        first = b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n3\r\nabc\r\n0\r\nX-End: yes\r\n\r\n"
        second = b"HTTP/1.1 204 No Content\r\n\r\n"
        reader = KEEPALIVE.ResponseReader(CapturedSocket([first + second]))
        response, raw, body = reader.read_response()
        self.assertEqual((response["framing"], raw, body), ("chunked", first, b"abc"))
        response, raw, body = reader.read_response()
        self.assertEqual((response["status"], raw, body), (204, second, b""))

    def test_interim100_is_not_the_final_request_response(self):
        wire = b"HTTP/1.1 100 Continue\r\n\r\nHTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n"
        result, _, body = KEEPALIVE.ResponseReader(CapturedSocket([wire])).read_response()
        self.assertEqual(result["status"], 200)
        self.assertEqual(len(result["interim_responses"]), 1)
        self.assertEqual(body, b"")

    def test_eof_mid_content_length_keeps_error_and_real_eof(self):
        reader = KEEPALIVE.ResponseReader(CapturedSocket([b"HTTP/1.1 200 OK\r\nContent-Length: 4\r\n\r\nabc"]))
        with self.assertRaisesRegex(KEEPALIVE.IncompleteResponse, "EOF"):
            reader.read_response()
        self.assertTrue(reader.exchange["tcp_eof_observed"])
        self.assertFalse(reader.exchange["framing_complete"])

    def test_chunk_size_without_body_cannot_release_streaming_barrier(self):
        state = []
        class ObservedSocket(CapturedSocket):
            def recv(self, size):
                state.append("recv")
                return super().recv(size)
        reader = KEEPALIVE.ResponseReader(ObservedSocket([
            b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n3\r\n", b"abc\r\n0\r\n\r\n"]),
            lambda: state.append("body-prefix"))
        reader.read_response()
        self.assertEqual(state, ["recv", "recv", "body-prefix"])

    def test_ambiguous_unframed_and_invalid_chunk_responses_fail(self):
        wires = [b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\nTransfer-Encoding: chunked\r\n\r\n",
                 b"HTTP/1.1 200 OK\r\n\r\nunframed",
                 b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\nxyz\r\n"]
        for wire in wires:
            with self.subTest(wire=wire), self.assertRaises(ValueError):
                KEEPALIVE.ResponseReader(CapturedSocket([wire])).read_response()

    def test_strict_new_socket_contract_needs_actual_server_close(self):
        plan = self.plan("keepalive_after_strict_new_connection")
        summary = {"steps": [{"request_send_completed_ns": 1, "error": {"type": "IncompleteResponse"}, "response": {}},
                             {"request_send_completed_ns": 2, "error": None, "response": {"framing_complete": True}}],
                   "server_close_before_fresh_socket": False}
        self.assertFalse(KEEPALIVE.sequence_complete(plan, summary))
        summary["server_close_before_fresh_socket"] = True
        self.assertTrue(KEEPALIVE.sequence_complete(plan, summary))

    def test_neighbor_case_has_real_backend_pause_and_keeps_original_input(self):
        original = self.plan("NEED-neighbor-connection-stream")
        result = KEEPALIVE.prepare_plan(original)
        self.assertIsNone(original["backend"]["body"])
        self.assertEqual(result["backend"]["barrier"]["release_condition"],
                         "independent_neighbor_process_completed_after_main_prefix")
        self.assertEqual(len(KEEPALIVE.sequence_requests(result)), 1)


if __name__ == "__main__":
    unittest.main()
