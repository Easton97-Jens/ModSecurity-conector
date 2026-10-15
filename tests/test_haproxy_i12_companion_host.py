"""Safety and evidence boundaries for the HAProxy-only companion runner."""
import importlib.util
from pathlib import Path
import tempfile
import json
import ssl
from unittest.mock import MagicMock, patch
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "connectors/haproxy/harness/i12_companion_host.py"
spec = importlib.util.spec_from_file_location("i12_companion_host", SOURCE)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)

class CompanionCaptureTests(unittest.TestCase):
    def setUp(self):
        runner.ROOT.mkdir(parents=True, exist_ok=True)

    def test_tls_truncation_preserves_physical_bytes(self):
        with tempfile.TemporaryDirectory(dir=runner.ROOT) as directory:
            root = Path(directory)
            context = MagicMock()
            stream = context.wrap_socket.return_value.__enter__.return_value
            stream.recv.side_effect = [b"HTTP/1.1 200 OK\r\nContent-Length: 8\r\n\r\nabc", ssl.SSLEOFError("no close_notify")]
            with patch.object(runner.ssl, "create_default_context", return_value=context), patch.object(runner.socket, "create_connection"):
                runner.capture_client(root, 19000, 0, False)
            report = json.loads((root / "client-0.json").read_text())
            self.assertEqual(report["tls_eof"], "exception")
            self.assertIn("SSLEOFError", report["error"])
            self.assertIsNone(report["kernel_tcp_eof"])
            stream.unwrap.assert_not_called()
            self.assertTrue((root / "client-0.response").read_bytes().endswith(b"abc"))
            context.wrap_socket.assert_called_once()
            self.assertFalse(context.wrap_socket.call_args.kwargs["suppress_ragged_eofs"])

    def test_tls_close_notify_is_distinct_from_client_cancel(self):
        for cancel, expected in ((False, "close_notify"), (True, "client_cancel")):
            with self.subTest(cancel=cancel), tempfile.TemporaryDirectory(dir=runner.ROOT) as directory:
                root = Path(directory)
                context = MagicMock()
                stream = context.wrap_socket.return_value.__enter__.return_value
                stream.recv.side_effect = [b"HTTP/1.1 200 OK\r\n\r\nbody", b""]
                stream.unwrap.return_value.recv.return_value = b""
                with patch.object(runner.ssl, "create_default_context", return_value=context), patch.object(runner.socket, "create_connection"):
                    runner.capture_client(root, 19000, 0, cancel)
                report = json.loads((root / "client-0.json").read_text())
                self.assertEqual(report["tls_eof"], expected)
                self.assertIsNone(report["error"])
                self.assertEqual(report["kernel_tcp_eof"], None if cancel else True)

    def test_close_notify_without_tcp_eof_remains_distinct(self):
        with tempfile.TemporaryDirectory(dir=runner.ROOT) as directory:
            root = Path(directory)
            context = MagicMock()
            stream = context.wrap_socket.return_value.__enter__.return_value
            stream.recv.side_effect = [b"HTTP/1.1 200 OK\r\n\r\n", b""]
            stream.unwrap.return_value.recv.return_value = b"unexpected"
            with patch.object(runner.ssl, "create_default_context", return_value=context), patch.object(runner.socket, "create_connection"):
                runner.capture_client(root, 19000, 100, False, neighbor=True)
            report = json.loads((root / "client-100.json").read_text())
            self.assertEqual(report["tls_eof"], "close_notify")
            self.assertFalse(report["kernel_tcp_eof"])
            self.assertIn(b"POST /neighbor HTTP/1.1", (root / "client-100.request").read_bytes())

    def test_unstarted_relay_is_never_published_to_concurrent_cleanup(self):
        registry = []
        thread = MagicMock()
        thread.start.side_effect = lambda: self.assertEqual(registry, [])
        with patch.object(runner.threading, "Thread", return_value=thread):
            runner.start_capture_thread(lambda: None, (), registry)
        self.assertEqual(registry, [thread])
        thread.start.side_effect = RuntimeError("start failed")
        registry.clear()
        with patch.object(runner.threading, "Thread", return_value=thread), self.assertRaisesRegex(RuntimeError, "start failed"):
            runner.start_capture_thread(lambda: None, (), registry)
        self.assertEqual(registry, [])

    def test_live_accept_worker_prevents_relay_snapshot(self):
        class UnstableRegistry:
            def __iter__(self):
                raise AssertionError("relay ownership read before accept worker stopped")
        worker = MagicMock()
        worker.ident = 123
        worker.is_alive.return_value = True
        with self.assertRaisesRegex(RuntimeError, "accept worker did not stop"):
            runner.stop_capture_threads((worker,), [], UnstableRegistry())
        worker.join.assert_called_once_with(timeout=4)

    def test_live_relay_is_a_reported_cleanup_failure(self):
        worker = MagicMock()
        worker.ident = 123
        worker.is_alive.return_value = False
        relay = MagicMock()
        relay.is_alive.return_value = True
        with self.assertRaisesRegex(RuntimeError, "relay did not stop"):
            runner.stop_capture_threads((worker,), [], [relay])
        relay.join.assert_called_once_with(timeout=1)

    def test_backend_accept_backlog_covers_the_parallel_fixture(self):
        self.assertEqual(runner.BACKEND_LISTEN_BACKLOG, 32)
        self.assertGreaterEqual(runner.CaptureBackendServer.request_queue_size, 16)

    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory(dir=runner.ROOT) as directory:
            root = Path(directory)
            sentinel = root / "sentinel"
            sentinel.write_text("retain")
            with self.assertRaises(FileExistsError):
                runner.fresh_root(root)
            self.assertEqual(sentinel.read_text(), "retain")

    def test_escape_and_symlink_are_rejected(self):
        with tempfile.TemporaryDirectory(dir=runner.ROOT) as directory:
            root = Path(directory)
            with self.assertRaises(ValueError):
                runner.fresh_root(root.parent / "escape", root)
            link = root / "link"
            link.symlink_to(root / "new")
            with self.assertRaises(ValueError):
                runner.fresh_root(link, root)

    def test_controller_child_is_explicit_and_fresh(self):
        with tempfile.TemporaryDirectory(dir=runner.ROOT) as directory:
            root = Path(directory)
            child = runner.fresh_root(root / "child", root)
            self.assertEqual(child.stat().st_mode & 0o777, 0o700)

if __name__ == "__main__":
    unittest.main()
