"""Exercise exact marker barriers and failure observations without NGINX."""
import importlib.util
import io
from pathlib import Path
import threading
from types import SimpleNamespace
import unittest
from unittest.mock import Mock


SPEC = importlib.util.spec_from_file_location(
    "sequence_barrier_quality", Path(__file__).resolve().parents[1] / "ci/runtime/lifecycle/nginx_sequence_upstream.py")
UPSTREAM = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(UPSTREAM)


class BarrierQualityTests(unittest.TestCase):
    def handler(self, released):
        handler = UPSTREAM._Handler.__new__(UPSTREAM._Handler)
        handler.rfile = io.BytesIO(b"GET /no-crs/sequence/0 HTTP/1.1\r\nHost: localhost\r\n\r\n")
        handler.wfile = Mock()
        handler.server = SimpleNamespace(backpressure=False, prefix_sent=threading.Event(),
            marker_sent=threading.Event(), client_headers_seen=Mock(),
            barrier_timeout=False, upstream_write_failed=False)
        handler.server.client_headers_seen.wait.return_value = released
        return handler

    @staticmethod
    def upstream(handler):
        upstream = UPSTREAM.SynchronizedUpstream.__new__(UPSTREAM.SynchronizedUpstream)
        upstream.server = handler.server
        return upstream

    def test_headers_callback_during_prefix_write_observes_armed_publication(self):
        handler = self.handler(True)
        handler.server.client_headers_seen = threading.Event()
        upstream = self.upstream(handler)

        def write(_payload):
            if handler.wfile.write.call_count == 1:
                upstream.headers_seen(0)

        handler.wfile.write.side_effect = write
        handler.handle()
        self.assertTrue(handler.server.prefix_sent.is_set())
        self.assertTrue(handler.server.client_headers_seen.is_set())
        self.assertTrue(handler.server.marker_sent.is_set())
        self.assertFalse(handler.server.upstream_write_failed)

    def test_headers_callback_during_prefix_flush_observes_armed_publication(self):
        handler = self.handler(True)
        handler.server.client_headers_seen = threading.Event()
        upstream = self.upstream(handler)

        def flush():
            if handler.wfile.flush.call_count == 1:
                upstream.headers_seen(0)

        handler.wfile.flush.side_effect = flush
        handler.handle()
        self.assertTrue(handler.server.prefix_sent.is_set())
        self.assertTrue(handler.server.client_headers_seen.is_set())
        self.assertTrue(handler.server.marker_sent.is_set())
        self.assertFalse(handler.server.upstream_write_failed)

    def test_headers_callback_before_prefix_publication_is_rejected(self):
        handler = self.handler(True)
        handler.server.client_headers_seen = threading.Event()
        upstream = self.upstream(handler)
        with self.assertRaisesRegex(ValueError, "client headers preceded the upstream prefix"):
            upstream.headers_seen(0)
        self.assertFalse(handler.server.client_headers_seen.is_set())

    def test_timeout_keeps_suffix_unsent_and_marker_false(self):
        handler = self.handler(False)
        handler.handle()
        self.assertTrue(handler.server.prefix_sent.is_set())
        self.assertTrue(handler.server.barrier_timeout)
        self.assertFalse(handler.server.marker_sent.is_set())
        self.assertFalse(handler.server.upstream_write_failed)
        handler.server.client_headers_seen.wait.assert_called_once_with(timeout=5)
        self.assertEqual(handler.wfile.write.call_count, 1)

    def test_released_barrier_writes_actual_suffix_before_marking(self):
        handler = self.handler(True)
        handler.handle()
        self.assertTrue(handler.server.prefix_sent.is_set())
        self.assertTrue(handler.server.marker_sent.is_set())
        self.assertFalse(handler.server.barrier_timeout)
        self.assertFalse(handler.server.upstream_write_failed)
        self.assertEqual(handler.wfile.write.call_count, 2)
        self.assertEqual(handler.wfile.write.call_args.args[0],
            format(len(UPSTREAM.SUFFIX), "x").encode() + b"\r\n" + UPSTREAM.SUFFIX + b"\r\n0\r\n\r\n")

    def test_suffix_write_error_is_observed_without_marking(self):
        handler = self.handler(True)
        handler.wfile.write.side_effect = [None, OSError("controlled suffix write failure")]
        handler.handle()
        self.assertTrue(handler.server.prefix_sent.is_set())
        self.assertTrue(handler.server.upstream_write_failed)
        self.assertFalse(handler.server.marker_sent.is_set())
        self.assertFalse(handler.server.barrier_timeout)

    def test_prefix_write_error_clears_publication_and_skips_barrier(self):
        handler = self.handler(True)
        handler.wfile.write.side_effect = OSError("controlled prefix write failure")
        handler.handle()
        self.assertFalse(handler.server.prefix_sent.is_set())
        self.assertTrue(handler.server.upstream_write_failed)
        self.assertFalse(handler.server.marker_sent.is_set())
        handler.server.client_headers_seen.wait.assert_not_called()

    def test_prefix_flush_error_clears_publication_and_skips_barrier(self):
        handler = self.handler(True)
        handler.wfile.flush.side_effect = OSError("controlled prefix flush failure")
        handler.handle()
        self.assertFalse(handler.server.prefix_sent.is_set())
        self.assertTrue(handler.server.upstream_write_failed)
        self.assertFalse(handler.server.marker_sent.is_set())
        handler.server.client_headers_seen.wait.assert_not_called()

    def test_suffix_flush_error_is_observed_without_marking(self):
        handler = self.handler(True)
        handler.wfile.flush.side_effect = [None, OSError("controlled suffix flush failure")]
        handler.handle()
        self.assertTrue(handler.server.prefix_sent.is_set())
        self.assertTrue(handler.server.upstream_write_failed)
        self.assertFalse(handler.server.marker_sent.is_set())
        self.assertFalse(handler.server.barrier_timeout)

    def test_followup_does_not_enter_marker_barrier(self):
        handler = self.handler(True)
        handler.rfile = io.BytesIO(b"GET /no-crs/sequence/1 HTTP/1.1\r\nHost: localhost\r\n\r\n")
        handler.handle()
        handler.server.client_headers_seen.wait.assert_not_called()
        self.assertFalse(handler.server.prefix_sent.is_set())
        self.assertFalse(handler.server.marker_sent.is_set())
        handler.wfile.write.assert_called_once()
