"""Safety and wire-input regressions for the supplemental patched capture."""
import importlib.util
import json
from pathlib import Path
import socket
import tempfile
import threading
import unittest


MODULE = Path(__file__).resolve().parents[1] / "ci/runtime/lifecycle/i12/lighttpd/patched_capture.py"
SPEC = importlib.util.spec_from_file_location("i12_patched_capture", MODULE)
capture = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(capture)
REVIEW_SPEC = importlib.util.spec_from_file_location("i12_patched_review", MODULE.with_name("patched_review.py"))
review = importlib.util.module_from_spec(REVIEW_SPEC)
REVIEW_SPEC.loader.exec_module(review)


class PatchedCaptureTests(unittest.TestCase):
    def test_artifacts_refuse_symlink_and_hardlink(self):
        with tempfile.TemporaryDirectory(dir=capture.EXTERNAL_ROOT) as temp:
            root = Path(temp)
            original = root / "image"
            original.write_bytes(b"fixture")
            self.assertEqual(capture.regular(original), original)
            alias = root / "alias"
            alias.symlink_to(original)
            with self.assertRaisesRegex(ValueError, "symlink"):
                capture.regular(alias)
            alias.unlink()
            alias.hardlink_to(original)
            with self.assertRaisesRegex(ValueError, "single-link"):
                capture.regular(original)

    def _exchange(self, body, chunked):
        received = []
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0)); listener.listen(1)
            def peer():
                with listener.accept()[0] as client:
                    data = bytearray()
                    while True:
                        data.extend(client.recv(65536))
                        if b"\r\n\r\n" not in data:
                            continue
                        entity = bytes(data).split(b"\r\n\r\n", 1)[1]
                        if (chunked and entity.endswith(b"0\r\n\r\n")) or (not chunked and len(entity) == len(body)):
                            break
                    received.append(bytes(data))
                    client.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n")
            thread = threading.Thread(target=peer, daemon=True); thread.start()
            result = capture.request(listener.getsockname()[1], "/fixture", body, chunked)
            thread.join(timeout=5)
            self.assertFalse(thread.is_alive())
        self.assertEqual(bytes.fromhex(result["request_wire_hex"]), received[0])
        self.assertEqual(result["status_line"], "HTTP/1.1 200 OK")
        self.assertIsNone(result["transport_error"])
        return received[0]

    def test_empty_is_actual_content_length_zero(self):
        wire = self._exchange(b"", False)
        self.assertIn(b"Content-Length: 0\r\n", wire)
        self.assertEqual(wire.split(b"\r\n\r\n", 1)[1], b"")

    def test_chunked_has_two_entity_chunks_and_single_terminal_chunk(self):
        wire = self._exchange(b"abcdef", True)
        self.assertIn(b"Transfer-Encoding: chunked\r\n", wire)
        self.assertEqual(wire.split(b"\r\n\r\n", 1)[1], b"3\r\nabc\r\n3\r\ndef\r\n0\r\n\r\n")

    def test_review_does_not_attribute_neighbor_append_to_empty_main(self):
        with tempfile.TemporaryDirectory(dir=capture.EXTERNAL_ROOT) as temp:
            root = Path(temp)
            capture.write_json(root / "receipt.json", {"case": "empty", "uid": 0, "gid": 0,
                "main": {"status_line": "HTTP/1.1 200 OK"}})
            rows = [
                {"function": "runtime_begin_request_stream", "edge": "enter", "call": 2},
                {"function": "native_process_request_body", "edge": "enter", "allocation_scope_call": 2},
                {"function": "runtime_begin_request_stream", "edge": "enter", "call": 80},
                {"function": "native_append_request_body", "edge": "enter", "allocation_scope_call": 80},
            ]
            (root / "native.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n")
            summary = review.summarize(root)
            self.assertEqual(summary["main_engine_function_counts"], {"native_process_request_body": 1})
            self.assertIsNone(summary["main_host_hooks"])
            self.assertFalse(summary["canonical_oracle_evaluated"])
            self.assertFalse(summary["full_lifecycle_qualified"])
            capture.write_json(root / "receipt.json", {"case": "technical", "uid": 0, "gid": 0,
                "main": {"status_line": ""}})
            technical = review.summarize(root)
            self.assertIsNone(technical["main_runtime_scope"])
            self.assertIsNone(technical["main_engine_function_counts"])


if __name__ == "__main__":
    unittest.main()
