#!/usr/bin/env python3
"""Serve bounded, catalog-backed upstream responses for one Traefik case.

Only the selected vector's response metadata is used.  The response body is
written to the socket, but is never printed, persisted, or included in an
observation record.  This helper intentionally has no shutdown endpoint and
is expected to be owned by the shell runner's process-group cleanup.
"""

from __future__ import annotations

import argparse
import http.client
import http.server
import json
import os
from pathlib import Path
import sys
import threading
import time
from typing import Any, NoReturn

MAX_CATALOG = 256 * 1024
MAX_RESPONSE = 64 * 1024
MAX_OBSERVATION = 16 * 1024
LEASE_HEADER = "x-msconnector-composite-lease"
P2_TO_P3_TIMEOUT_SECONDS = 6.0
P2_TO_P3_TIMEOUT_CASE = "p2_to_p3_timeout"


def fail(message: str) -> NoReturn:
    raise RuntimeError(message)


def response_header_delay_seconds(observation_root: Path) -> float:
    """Select a bounded delay only from the operator-owned runtime-root."""
    root_name = observation_root.name
    if root_name == P2_TO_P3_TIMEOUT_CASE or root_name.endswith(
        f"-{P2_TO_P3_TIMEOUT_CASE}"
    ):
        return P2_TO_P3_TIMEOUT_SECONDS
    return 0.0


def load_catalog(path: Path) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file():
        fail("case input must be a regular non-symlink file")
    if path.stat().st_size > MAX_CATALOG:
        fail("case input exceeds the bounded catalog size")
    with path.open("r", encoding="utf-8") as handle:
        catalog = json.load(handle)
    if not isinstance(catalog, dict) or not isinstance(catalog.get("vectors"), list):
        fail("case input is not a catalog with vectors")
    return catalog


def vectors_by_path(catalog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for vector in catalog["vectors"]:
        if not isinstance(vector, dict):
            continue
        request = vector.get("request")
        if not isinstance(request, dict) or not isinstance(request.get("path"), str):
            continue
        path = request["path"]
        if path in result:
            fail("catalog contains duplicate request paths")
        result[path] = vector
    return result


class ControlledHandler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, _format: str, *_args: object) -> None:
        # The default server logger would retain request paths and headers.
        return

    def do_GET(self) -> None:  # noqa: N802 - stdlib callback name
        self._serve()

    def do_POST(self) -> None:  # noqa: N802 - stdlib callback name
        self._serve()

    def _serve(self) -> None:
        self.server.observation.record(self.headers)  # type: ignore[attr-defined]
        vector = self.server.vectors.get(self.path)  # type: ignore[attr-defined]
        if vector is None:
            self.send_response(404)
            self.send_header("Content-Length", "0")
            self.send_header("Connection", "close")
            self.end_headers()
            return
        upstream = vector.get("upstream")
        if not isinstance(upstream, dict):
            self.send_response(404)
            self.send_header("Content-Length", "0")
            self.send_header("Connection", "close")
            self.end_headers()
            return
        status = upstream.get("status", 200)
        headers = upstream.get("headers", {})
        body_text = upstream.get("body", "")
        if not isinstance(status, int) or not 100 <= status <= 599:
            fail("catalog upstream status is invalid")
        if not isinstance(headers, dict) or not isinstance(body_text, str):
            fail("catalog upstream metadata is invalid")
        body = body_text.encode("utf-8")
        if len(body) > MAX_RESPONSE:
            fail("catalog upstream response exceeds the bounded response size")
        delay = response_header_delay_seconds(self.server.observation.root)  # type: ignore[attr-defined]
        if delay:
            # The request is already recorded; only response headers are delayed.
            time.sleep(delay)
        self.send_response(status)
        for name, value in headers.items():
            if not isinstance(name, str) or not isinstance(value, str):
                fail("catalog upstream header is invalid")
            if name.lower() in {"content-length", "connection", "transfer-encoding"}:
                continue
            self.send_header(name, value)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)


class ControlledServer(http.server.ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = False

    def __init__(
        self,
        address: tuple[str, int],
        vectors: dict[str, dict[str, Any]],
        observation_path: Path,
        observation_root: Path,
    ) -> None:
        super().__init__(address, ControlledHandler)
        self.vectors = vectors
        self.observation = ObservationWriter(observation_path, observation_root)


class ObservationWriter:
    """Write only bounded metadata about requests received by this child."""

    def __init__(self, path: Path, root: Path) -> None:
        if path.parent != root or root.is_symlink() or not root.is_dir():
            fail("observation must be a direct child of the owner-only root")
        if path.is_symlink() or not path.is_file():
            fail("observation must be a pre-created regular file")
        stat_result = path.stat()
        if stat_result.st_uid != os.getuid() or stat_result.st_mode & 0o077:
            fail("observation must be owner-only")
        self.path = path
        self.root = root
        self.lock = threading.Lock()
        self.requests_seen = 0
        self.lease_header_observed = False
        self._persist()

    def record(self, headers: http.client.HTTPMessage) -> None:
        with self.lock:
            self.requests_seen += 1
            self.lease_header_observed = self.lease_header_observed or any(
                name.lower() == LEASE_HEADER for name in headers.keys()
            )

            self._persist()

    def _persist(self) -> None:
        value = {
            "schema": "traefik-composite-upstream-observation/v1",
            "requests_seen": self.requests_seen,
            "lease_header_observed": self.lease_header_observed,
        }
        encoded = (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
        if len(encoded) > MAX_OBSERVATION:
            fail("observation exceeds the bounded metadata size")
        try:
            fd = os.open(self.path, os.O_WRONLY | os.O_TRUNC | os.O_NOFOLLOW)
            with os.fdopen(fd, "wb") as handle:
                handle.write(encoded)
                handle.flush()
                os.fsync(handle.fileno())
        except OSError as exc:
            fail(f"observation write failed: {exc}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--listen", required=True)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--case-input", required=True, type=Path)
    parser.add_argument("--observation", required=True, type=Path)
    parser.add_argument("--observation-root", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        if not args.root.is_dir() or args.root.is_symlink():
            fail("upstream root must be an existing non-symlink directory")
        host, separator, port_text = args.listen.rpartition(":")
        if not separator or host not in {"127.0.0.1", "localhost"}:
            fail("listen must be a local host:port endpoint")
        port = int(port_text)
        if not 1 <= port <= 65535:
            fail("listen port is outside the valid range")
        server = ControlledServer(
            (host, port),
            vectors_by_path(load_catalog(args.case_input)),
            args.observation,
            args.observation_root,
        )
        try:
            server.serve_forever(poll_interval=0.2)
        finally:
            server.server_close()
        return 0
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"traefik_composite_upstream: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
