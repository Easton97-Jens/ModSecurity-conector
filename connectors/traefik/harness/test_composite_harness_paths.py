"""Focused path and loopback-client tests for the Traefik composite harness."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import socket
import ssl
import subprocess
import tempfile
import threading
import unittest



HARNESS = Path(__file__).with_name("traefik_composite_case_driver.py")
SPEC = importlib.util.spec_from_file_location("traefik_case_driver", HARNESS)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("failed to load Traefik case driver")
DRIVER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DRIVER)
UPSTREAM_HARNESS = Path(__file__).with_name("traefik_composite_upstream.py")
UPSTREAM_SPEC = importlib.util.spec_from_file_location("traefik_upstream", UPSTREAM_HARNESS)
if UPSTREAM_SPEC is None or UPSTREAM_SPEC.loader is None:
    raise RuntimeError("failed to load Traefik upstream harness")
UPSTREAM = importlib.util.module_from_spec(UPSTREAM_SPEC)
UPSTREAM_SPEC.loader.exec_module(UPSTREAM)


class CompositeHarnessPathTests(unittest.TestCase):
  def test_artifact_leaf_requires_absolute_direct_child(self) -> None:
    root = Path("/private/runtime")
    assert DRIVER.artifact_leaf(root / "input.json", root, "input") == "input.json"
    for candidate in (Path("input.json"), root / "nested" / "input.json", root / ".." / "outside.json"):
        with self.assertRaises(RuntimeError):
            DRIVER.artifact_leaf(candidate, root, "input")


  def test_private_runtime_root_rejects_symlink_and_hardlink(self) -> None:
    from runtime_path_utils import open_private_runtime_root

    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary) / "runtime"
        root.mkdir(mode=0o700)
        with open_private_runtime_root(root) as runtime:
            runtime.create_text("valid.json", "{}\n")
            assert runtime.read_text("valid.json") == "{}\n"
            (root / "link.json").symlink_to(root / "valid.json")
            (root / "hard.json").hardlink_to(root / "valid.json")
            with self.assertRaises((OSError, ValueError)):
                runtime.read_text("link.json")
            with self.assertRaises((OSError, ValueError)):
                runtime.read_text("hard.json")


  def test_read_events_counts_crlf_terminators_in_line_limit(self) -> None:
    from runtime_path_utils import open_private_runtime_root

    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary) / "runtime"
        root.mkdir(mode=0o700)
        event = {
            "decision_id": "A" * 16,
            "phase": "terminal",
            "reason": "x" * (DRIVER.MAX_EVENT_LINE - 50),
        }
        import json
        encoded = json.dumps(event, separators=(",", ":")) + "\r\n"
        self.assertGreater(len(encoded.encode("utf-8")), DRIVER.MAX_EVENT_LINE)
        with open_private_runtime_root(root) as runtime:
            runtime.create_text("events.jsonl", encoded)
            with self.assertRaises(RuntimeError):
                DRIVER.read_events(runtime, "events.jsonl")


  def test_origin_form_rejects_absolute_and_control_targets(self) -> None:
    assert DRIVER._origin_target("/safe?x=1") == "/safe?x=1"
    for target in ("https://127.0.0.1/", "//other/", "/bad\r\nX: y", ""):
        with self.assertRaises(RuntimeError):
            DRIVER._origin_target(target)


  def test_main_rejects_absolute_outside_root_input_before_opening_runtime(self) -> None:
    with tempfile.TemporaryDirectory() as temporary:
        base = Path(temporary)
        root = base / "runtime"
        root.mkdir(mode=0o700)
        sentinel = root / "sentinel"
        sentinel.write_text("unchanged\n", encoding="utf-8")
        outside = base / "outside.json"
        outside.write_text("{}\n", encoding="utf-8")
        before = sorted(path.name for path in root.iterdir())
        driver_result = DRIVER.main([
            "--input", str(outside), "--port", "19180",
            "--manifest", str(root / "case.manifest.json"),
            "--event-log", str(root / "events.jsonl"), "--runtime-root", str(root),
            "--upstream-observation", str(root / "upstream.json"), "--connector", "traefik",
        ])
        upstream_result = UPSTREAM.main([
            "--listen", "127.0.0.1:19181", "--root", str(root),
            "--case-input", str(outside), "--observation", str(root / "upstream.json"),
            "--observation-root", str(root),
            "--cert", str(outside), "--key", str(outside),
        ])
        self.assertEqual(driver_result, 1)
        self.assertEqual(upstream_result, 1)
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "unchanged\n")
        self.assertEqual(sorted(path.name for path in root.iterdir()), before)


  @staticmethod
  def _generate_certificate(
      base: Path, name: str, hostname: str = "composite-upstream.local"
  ) -> tuple[Path, Path]:
    cert = base / f"{name}-cert.pem"
    key = base / f"{name}-key.pem"
    subprocess.run([
        "openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes",
        "-sha256", "-days", "1", "-keyout", str(key), "-out", str(cert),
        "-subj", f"/CN={hostname}",
        "-addext", f"subjectAltName=DNS:{hostname}",
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return cert, key

  @staticmethod
  def _controlled_tls_server(cert: Path, key: Path):
    class Observation:
      def record(self, _headers: object) -> None:
        return

    server = UPSTREAM.ControlledServer(
        ("127.0.0.1", 0),
        {"/safe": {"upstream": {"status": 200, "headers": {}, "body": "OK"}}},
        Observation(),
        Path("/private/runtime"),
        str(cert),
        str(key),
    )
    thread = threading.Thread(target=server.handle_request)
    thread.start()
    return server, thread

  @staticmethod
  def _open_tls_connection(context: ssl.SSLContext, port: int):
    connection = socket.create_connection(("127.0.0.1", port), timeout=2)
    try:
      return context.wrap_socket(connection, server_hostname="composite-upstream.local")
    finally:
      connection.close()

  def test_controlled_upstream_uses_native_tls_server_loop(self) -> None:
    text = UPSTREAM_HARNESS.read_text(encoding="utf-8")
    self.assertIn("class ControlledServer(http.server.ThreadingHTTPSServer)", text)
    self.assertIn("server.handle_request()", text)
    self.assertNotIn("server.serve_forever", text)

  def test_loopback_client_accepts_bounded_http_response(self) -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 0))
    server.listen(1)
    port = server.getsockname()[1]

    def serve() -> None:
      connection, _ = server.accept()
      try:
        request = connection.recv(4096)
        assert request.startswith(b"GET /safe HTTP/1.1\r\n")
        assert b"Host: 127.0.0.1:" in request
        connection.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK")
      finally:
        connection.close()
        server.close()

    thread = threading.Thread(target=serve)
    thread.start()
    try:
      status, completed = DRIVER.http_request(
          port,
          {"request": {"method": "GET", "path": "/safe", "headers": {}}},
          False,
      )
    finally:
      thread.join(timeout=2)
    self.assertEqual((status, completed), (200, True))

  def test_controlled_upstream_accepts_verified_tls(self) -> None:
    with tempfile.TemporaryDirectory() as temporary:
      base = Path(temporary)
      cert, key = self._generate_certificate(base, "trusted")
      server, thread = self._controlled_tls_server(cert, key)
      try:
        context = ssl.create_default_context(cafile=str(cert))
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        with socket.create_connection(("127.0.0.1", server.server_address[1]), timeout=2) as connection:
          with context.wrap_socket(connection, server_hostname="composite-upstream.local") as tls_connection:
            tls_connection.sendall(b"GET /safe HTTP/1.1\r\nHost: composite-upstream.local\r\n\r\n")
            self.assertTrue(tls_connection.recv(4096).startswith(b"HTTP/1.1 200 OK\r\n"))
      finally:
        server.server_close()
        thread.join(timeout=2)

  def test_controlled_upstream_rejects_untrusted_certificate(self) -> None:
    with tempfile.TemporaryDirectory() as temporary:
      base = Path(temporary)
      trusted_cert, _ = self._generate_certificate(base, "trusted")
      server_cert, server_key = self._generate_certificate(base, "untrusted")
      server, thread = self._controlled_tls_server(server_cert, server_key)
      try:
        context = ssl.create_default_context(cafile=str(trusted_cert))
        with self.assertRaises(ssl.SSLCertVerificationError):
          self._open_tls_connection(context, server.server_address[1])
      finally:
        server.server_close()
        thread.join(timeout=2)

  def test_controlled_upstream_rejects_trusted_wrong_hostname(self) -> None:
    with tempfile.TemporaryDirectory() as temporary:
      base = Path(temporary)
      cert, key = self._generate_certificate(base, "wrong-host", "other-upstream.local")
      server, thread = self._controlled_tls_server(cert, key)
      try:
        context = ssl.create_default_context(cafile=str(cert))
        with self.assertRaises(ssl.SSLCertVerificationError):
          self._open_tls_connection(context, server.server_address[1])
      finally:
        server.server_close()
        thread.join(timeout=2)


if __name__ == "__main__":
    unittest.main()
