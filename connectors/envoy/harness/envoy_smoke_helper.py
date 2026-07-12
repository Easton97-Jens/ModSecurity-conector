#!/usr/bin/env python3
"""Small dependency-free upstream/probe helper for the Envoy connector smoke."""

from __future__ import annotations

import argparse
import http.server
import json
from pathlib import Path
import socket
import sys
import time
from typing import Any
import urllib.error
import urllib.request


class UpstreamHandler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    client_cancel_delay_seconds = 5.0
    phase4_barrier_dir: Path | None = None
    phase4_barrier_timeout_seconds = 10.0

    def log_message(self, fmt: str, *args: object) -> None:
        del fmt, args

    def answer(self) -> None:
        content_length = int(self.headers.get("content-length") or "0")
        if content_length > 0:
            self.rfile.read(content_length)
        if self.path == "/phase4-marker" and self.phase4_barrier_dir is not None:
            self._answer_phase4_barrier()
            return
        if self.path == "/client-cancel":
            # This fixture sends one real response byte and deliberately holds
            # the final bytes open.  The opt-in runtime probe closes the
            # downstream client socket after that first byte.  It is not used
            # to infer a reset code or to promote strict behavior.
            first_chunk = b"envoy-client-cancel-first-byte\n"
            final_chunk = b"envoy-client-cancel-final-byte\n"
            self.send_response(200)
            self.send_header("content-type", "text/plain")
            self.send_header("content-length", str(len(first_chunk) + len(final_chunk)))
            self.end_headers()
            try:
                self.wfile.write(first_chunk)
                self.wfile.flush()
                time.sleep(self.client_cancel_delay_seconds)
                self.wfile.write(final_chunk)
                self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                return
            return
        response_headers: list[tuple[str, str]] = []
        if self.path == "/phase3-block":
            response_headers.append(("X-Modsec-Upstream", "block"))
        elif self.path == "/phase3-redirect":
            response_headers.append(("X-Modsec-Upstream", "redirect"))
        if self.path == "/phase4-marker":
            body = b"no-crs-response-body-marker\n"
        else:
            body = b"envoy connector upstream ok\n"
        self.send_response(200)
        self.send_header("content-type", "text/plain")
        for name, value in response_headers:
            self.send_header(name, value)
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _answer_phase4_barrier(self) -> None:
        """Serve a controlled P4 body without persisting either body chunk.

        The first chunk is intentionally harmless.  The canonical P4 marker
        follows only after the downstream client has read a body chunk while
        the upstream has published its paused/EOS-false control record and
        created the release file.  The JSON controls contain state and sizes
        only; they never contain either fixture payload.
        """
        assert self.phase4_barrier_dir is not None
        paths = phase4_barrier_paths(self.phase4_barrier_dir)
        first_chunk = b"envoy-first-byte-prefix\n"
        later_chunk = b"no-crs-response-body-marker\n"
        self.send_response(200)
        self.send_header("content-type", "text/plain")
        self.send_header("transfer-encoding", "chunked")
        self.send_header("connection", "close")
        self.end_headers()
        try:
            self._write_chunk(first_chunk)
            write_json_atomic(paths["paused"], {
                "schema_version": 1,
                "evidence_type": "envoy_phase4_upstream_paused",
                "first_chunk_size": len(first_chunk),
                "upstream_paused": True,
                "upstream_eos_sent": False,
                "body_payload_persisted": False,
            })
            wait_for_release(paths["release"], self.phase4_barrier_timeout_seconds)
            self._write_chunk(later_chunk)
            self.wfile.write(b"0\r\n\r\n")
            self.wfile.flush()
            write_json_atomic(paths["completed"], {
                "schema_version": 1,
                "evidence_type": "envoy_phase4_upstream_completed",
                "first_chunk_size": len(first_chunk),
                "upstream_eos_sent": True,
                "body_payload_persisted": False,
            })
        except (BrokenPipeError, ConnectionResetError):
            # A failed client is not a successful barrier observation.  Leave
            # the completed record absent so the probe rejects the run.
            return

    def _write_chunk(self, payload: bytes) -> None:
        self.wfile.write(f"{len(payload):X}\r\n".encode("ascii"))
        self.wfile.write(payload)
        self.wfile.write(b"\r\n")
        self.wfile.flush()

    do_GET = answer
    do_HEAD = answer
    do_POST = answer


def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def free_ports(count: int) -> list[int]:
    sockets: list[socket.socket] = []
    try:
        for _ in range(count):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(("127.0.0.1", 0))
            sockets.append(sock)
        return [int(sock.getsockname()[1]) for sock in sockets]
    finally:
        for sock in sockets:
            sock.close()


def phase4_barrier_paths(barrier_dir: str | Path) -> dict[str, Path]:
    directory = Path(barrier_dir)
    if not directory.is_absolute():
        raise ValueError("phase-4 barrier directory must be absolute")
    return {
        "paused": directory / "upstream-paused.json",
        "release": directory / "release",
        "completed": directory / "upstream-completed.json",
    }


def write_json_atomic(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def wait_for_release(path: Path, timeout: float) -> None:
    deadline = time.monotonic() + timeout
    while not path.exists():
        if time.monotonic() >= deadline:
            raise TimeoutError("timed out waiting for phase-4 barrier release")
        time.sleep(0.01)
    if path.is_symlink() or not path.is_file():
        raise ValueError("phase-4 barrier release must be a regular file")


def serve_upstream(
    port: int,
    client_cancel_delay: float,
    phase4_barrier_dir: str | None = None,
    phase4_barrier_timeout: float = 10.0,
) -> int:
    if client_cancel_delay <= 0 or client_cancel_delay > 30:
        raise ValueError("client cancel delay must be greater than zero and at most 30 seconds")
    if phase4_barrier_timeout <= 0 or phase4_barrier_timeout > 60:
        raise ValueError("phase-4 barrier timeout must be greater than zero and at most 60 seconds")
    barrier_directory = Path(phase4_barrier_dir) if phase4_barrier_dir else None
    if barrier_directory is not None:
        paths = phase4_barrier_paths(barrier_directory)
        if any(path.exists() for path in paths.values()):
            raise ValueError("phase-4 barrier paths must be fresh")

    class DelayedUpstreamHandler(UpstreamHandler):
        client_cancel_delay_seconds = client_cancel_delay
        phase4_barrier_dir = barrier_directory
        phase4_barrier_timeout_seconds = phase4_barrier_timeout

    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), DelayedUpstreamHandler)
    try:
        server.serve_forever()
    finally:
        server.server_close()
    return 0


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(
        self,
        req: urllib.request.Request,
        fp: object,
        code: int,
        msg: str,
        headers: object,
        newurl: str,
    ) -> None:
        del req, fp, code, msg, headers, newurl
        return None


def parse_headers(header: list[str]) -> dict[str, str]:
    headers: dict[str, str] = {}
    for item in header:
        name, separator, value = item.partition(":")
        if not separator or not name.strip() or "\r" in name or "\n" in name or "\r" in value or "\n" in value:
            raise ValueError(f"invalid header: {item!r}")
        headers[name.strip()] = value.strip()
    return headers


def probe(url: str, header: list[str], method: str, data: str | None, no_redirect: bool) -> int:
    headers = parse_headers(header)
    body = None if data is None else data.encode("utf-8")
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        opener = urllib.request.build_opener(NoRedirect) if no_redirect else urllib.request.build_opener()
        with opener.open(request, timeout=2) as response:
            response.read()
            status = int(response.status)
    except urllib.error.HTTPError as exc:
        exc.read()
        status = int(exc.code)
    print(status)
    return 0


def client_cancel(host: str, port: int, path: str, header: list[str]) -> dict[str, int | bool]:
    """Close a real HTTP/1.1 downstream connection after its first body byte.

    The result is intentionally client-local metadata.  Envoy's ext_proc API
    does not identify the resulting gRPC cancellation as a client or upstream
    reset, so callers must pair this observation with the explicit unattributed
    completion record rather than fabricating a reset cause.
    """
    if not host or "\r" in host or "\n" in host:
        raise ValueError("invalid host")
    if port < 1 or port > 65535:
        raise ValueError("port must be in range 1..65535")
    if not path.startswith("/") or "\r" in path or "\n" in path:
        raise ValueError("path must be an absolute HTTP path")
    headers = parse_headers(header)
    request_lines = [f"GET {path} HTTP/1.1", f"Host: {host}", "Connection: keep-alive"]
    request_lines.extend(f"{name}: {value}" for name, value in headers.items())
    try:
        request = ("\r\n".join(request_lines) + "\r\n\r\n").encode("ascii")
    except UnicodeEncodeError as exc:
        raise ValueError("client-cancel headers must be ASCII") from exc
    with socket.create_connection((host, port), timeout=2) as connection:
        connection.settimeout(2)
        connection.sendall(request)
        received = bytearray()
        header_end = -1
        while True:
            chunk = connection.recv(4096)
            if not chunk:
                raise RuntimeError("server closed before sending a response body byte")
            received.extend(chunk)
            if len(received) > 64 << 10:
                raise RuntimeError("response headers exceed the client-cancel observation limit")
            header_end = received.find(b"\r\n\r\n")
            if header_end >= 0 and len(received) > header_end + 4:
                break
        status_line = bytes(received[:header_end]).split(b"\r\n", 1)[0]
        try:
            _version, status_text, _reason = status_line.split(b" ", 2)
            status = int(status_text)
        except (TypeError, ValueError) as exc:
            raise RuntimeError("server returned an invalid HTTP status line") from exc
        # Leaving the context closes the TCP connection while the delayed
        # upstream response is still open.  No response payload is persisted.
        return {"client_closed": True, "first_body_byte_received": True, "http_status": status}


def _bounded_token(value: object, *, field: str, maximum: int = 128) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string")
    token = value.strip()
    if not token or len(token) > maximum:
        raise ValueError(f"{field} must be a non-empty bounded token")
    if not all(character.isascii() and (character.isalnum() or character in ":._-") for character in token):
        raise ValueError(f"{field} must be a bounded token")
    return token


def _nonnegative_int(value: object, *, field: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{field} must be a non-negative integer")
    return value


def _http_status(value: object, *, field: str) -> int:
    status = _nonnegative_int(value, field=field)
    if status < 100 or status > 599:
        raise ValueError(f"{field} must be an HTTP status")
    return status


def _load_json_object(path: Path, *, label: str) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"{label} must be a regular JSON file")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{label} is not valid JSON") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{label} must contain a JSON object")
    return {str(key): value for key, value in payload.items()}


def _wait_for_json_object(path: Path, *, timeout: float, label: str) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    while not path.exists():
        if time.monotonic() >= deadline:
            raise TimeoutError(f"timed out waiting for {label}")
        time.sleep(0.01)
    return _load_json_object(path, label=label)


def _read_until(
    connection: socket.socket,
    buffer: bytearray,
    marker: bytes,
    *,
    timeout: float,
    label: str,
) -> None:
    deadline = time.monotonic() + timeout
    while marker not in buffer:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError(f"timed out waiting for {label}")
        connection.settimeout(remaining)
        piece = connection.recv(4096)
        if not piece:
            raise RuntimeError(f"connection closed before {label}")
        buffer.extend(piece)
        if len(buffer) > 64 << 10:
            raise RuntimeError(f"{label} exceeded the bounded observation limit")


def _read_chunked_first_body(
    connection: socket.socket, *, timeout: float
) -> tuple[int, int]:
    """Return status and first downstream body size, retaining no payload.

    The controlled upstream always uses HTTP/1.1 chunking.  A real proxy may
    legally normalize that framing for the downstream, so the proof accepts a
    first body byte without chunk framing too.  In either case the upstream's
    independently published pause record establishes that its EOS was still
    absent when the client observed that byte.
    """
    received = bytearray()
    _read_until(
        connection,
        received,
        b"\r\n\r\n",
        timeout=timeout,
        label="HTTP response headers",
    )
    headers, remainder = bytes(received).split(b"\r\n\r\n", 1)
    status_line = headers.split(b"\r\n", 1)[0]
    parts = status_line.split(b" ", 2)
    try:
        status = int(parts[1])
    except (IndexError, ValueError) as exc:
        raise RuntimeError("server returned an invalid HTTP status line") from exc
    normalized_headers = b"\r\n" + headers.lower() + b"\r\n"
    if b"\r\ntransfer-encoding: chunked\r\n" not in normalized_headers:
        if remainder:
            return status, 1
        deadline = time.monotonic() + timeout
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("timed out waiting for first response body byte")
            connection.settimeout(remaining)
            if connection.recv(1):
                return status, 1
            raise RuntimeError("connection closed before the first response body byte")
    chunk_data = bytearray(remainder)
    _read_until(
        connection,
        chunk_data,
        b"\r\n",
        timeout=timeout,
        label="first response chunk length",
    )
    line_end = chunk_data.find(b"\r\n")
    try:
        size = int(bytes(chunk_data[:line_end]).split(b";", 1)[0], 16)
    except ValueError as exc:
        raise RuntimeError("first response chunk length is invalid") from exc
    if size < 1:
        raise RuntimeError("first response chunk must contain a body byte")
    body_start = line_end + 2
    deadline = time.monotonic() + timeout
    while len(chunk_data) - body_start < size:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("timed out waiting for first response body chunk")
        connection.settimeout(remaining)
        piece = connection.recv(min(4096, size - (len(chunk_data) - body_start)))
        if not piece:
            raise RuntimeError("connection closed during the first response body chunk")
        chunk_data.extend(piece)
    # ``chunk_data`` deliberately goes out of scope without being copied to a
    # file, JSON record, or log.  The observation retains only its byte count.
    return status, size


def _drain_response(connection: socket.socket, *, timeout: float) -> None:
    deadline = time.monotonic() + timeout
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("timed out draining released phase-4 response")
        connection.settimeout(remaining)
        piece = connection.recv(4096)
        if not piece:
            return


def phase4_first_byte(
    host: str,
    port: int,
    path: str,
    header: list[str],
    barrier_dir: str,
    timeout: float,
) -> dict[str, int | bool | str]:
    """Observe one downstream byte while the controlled upstream has no EOS."""
    if not host or "\r" in host or "\n" in host:
        raise ValueError("invalid host")
    if port < 1 or port > 65535:
        raise ValueError("port must be in range 1..65535")
    if not path.startswith("/") or "\r" in path or "\n" in path:
        raise ValueError("path must be an absolute HTTP path")
    if timeout <= 0 or timeout > 60:
        raise ValueError("timeout must be greater than zero and at most 60 seconds")
    paths = phase4_barrier_paths(barrier_dir)
    if any(path_value.exists() for path_value in paths.values()):
        raise ValueError("phase-4 barrier paths must be fresh before probing")
    headers = parse_headers(header)
    request_lines = [f"GET {path} HTTP/1.1", f"Host: {host}", "Connection: close"]
    request_lines.extend(f"{name}: {value}" for name, value in headers.items())
    try:
        request = ("\r\n".join(request_lines) + "\r\n\r\n").encode("ascii")
    except UnicodeEncodeError as exc:
        raise ValueError("phase-4 barrier headers must be ASCII") from exc

    with socket.create_connection((host, port), timeout=timeout) as connection:
        connection.sendall(request)
        status, first_chunk_size = _read_chunked_first_body(connection, timeout=timeout)
        paused = _wait_for_json_object(
            paths["paused"], timeout=timeout, label="upstream phase-4 pause record"
        )
        if (
            paused.get("schema_version") != 1
            or paused.get("evidence_type") != "envoy_phase4_upstream_paused"
            or paused.get("upstream_paused") is not True
            or paused.get("upstream_eos_sent") is not False
            or paused.get("body_payload_persisted") is not False
        ):
            raise RuntimeError("upstream phase-4 pause record is invalid")
        _nonnegative_int(paused.get("first_chunk_size"), field="paused first_chunk_size")
        if paused["first_chunk_size"] < 1:
            raise RuntimeError("upstream phase-4 pause record has no first chunk")
        paths["release"].parent.mkdir(parents=True, exist_ok=True)
        try:
            paths["release"].touch(exist_ok=False)
        except FileExistsError as exc:
            raise RuntimeError("phase-4 barrier release was already present") from exc
        _drain_response(connection, timeout=timeout)

    completed = _wait_for_json_object(
        paths["completed"], timeout=timeout, label="upstream phase-4 completion record"
    )
    if (
        completed.get("schema_version") != 1
        or completed.get("evidence_type") != "envoy_phase4_upstream_completed"
        or completed.get("upstream_eos_sent") is not True
        or completed.get("body_payload_persisted") is not False
    ):
        raise RuntimeError("upstream phase-4 completion record is invalid")
    _nonnegative_int(completed.get("first_chunk_size"), field="completed first_chunk_size")
    return {
        "schema_version": 1,
        "evidence_type": "envoy_phase4_first_byte_observation",
        "http_status": status,
        "client_first_byte_received": True,
        "first_byte_before_response_end": True,
        "first_chunk_size": first_chunk_size,
        "upstream_paused": True,
        "upstream_eos_sent_at_first_byte": False,
        "upstream_response_finished_at_first_byte": False,
        "upstream_eos_sent_after_release": True,
        "body_payload_persisted": False,
        "transport_protocol": "http1",
        "outcome": "PASS",
    }


def _phase4_safe_event(
    records: list[dict[str, Any]], *, transaction_id: str
) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    for record in records:
        if record.get("event") == "phase4_first_byte_barrier":
            continue
        rule_id = record.get("rule_id")
        if isinstance(rule_id, bool) or str(rule_id) != "1100301":
            continue
        if record.get("connector") != "envoy" or record.get("integration_mode") != "ext_proc":
            continue
        phase = record.get("phase")
        if record.get("transaction_id") != transaction_id or phase not in {
            4,
            "4",
            "phase4",
            "response_body",
        }:
            continue
        if (
            record.get("requested_action") == "deny"
            and record.get("actual_action") == "log_only"
            and record.get("late_intervention") is True
            and record.get("late_intervention_mode") == "safe"
            and record.get("headers_sent") is True
            and record.get("body_started") is True
            and record.get("response_committed") is True
            and record.get("connection_aborted") is False
            and record.get("transport_result") == "log_only"
        ):
            candidates.append(record)
    if len(candidates) != 1:
        raise ValueError(
            "expected exactly one Common P4 safe log-only event for the barrier transaction"
        )
    return candidates[0]


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    if path.is_symlink() or not path.is_file():
        raise ValueError("Common event log must be a regular JSONL file")
    records: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Common event log line {number} is not JSON") from exc
        if not isinstance(value, dict):
            raise ValueError(f"Common event log line {number} is not an object")
        records.append({str(key): item for key, item in value.items()})
    return records


def _phase4_observation(path: Path) -> dict[str, Any]:
    observation = _load_json_object(path, label="phase-4 first-byte observation")
    expected = {
        "schema_version": 1,
        "evidence_type": "envoy_phase4_first_byte_observation",
        "http_status": 200,
        "client_first_byte_received": True,
        "first_byte_before_response_end": True,
        "upstream_paused": True,
        "upstream_eos_sent_at_first_byte": False,
        "upstream_response_finished_at_first_byte": False,
        "upstream_eos_sent_after_release": True,
        "body_payload_persisted": False,
        "transport_protocol": "http1",
        "outcome": "PASS",
    }
    for field, expected_value in expected.items():
        if observation.get(field) != expected_value:
            raise ValueError(f"phase-4 first-byte observation has invalid {field}")
    if _nonnegative_int(observation.get("first_chunk_size"), field="first_chunk_size") < 1:
        raise ValueError("phase-4 first-byte observation has no first chunk")
    return observation


def write_phase4_first_byte_evidence(
    *,
    event_log: str,
    observation_path: str,
    transaction_id: str,
    evidence_output: str | None = None,
    run_id: str | None = None,
) -> dict[str, object]:
    """Bind the controlled first-byte observation to the real Common P4 event."""
    transaction = _bounded_token(transaction_id, field="transaction_id", maximum=256)
    event_path = Path(event_log)
    observation = _phase4_observation(Path(observation_path))
    source = _phase4_safe_event(_load_jsonl(event_path), transaction_id=transaction)
    body_seen = _nonnegative_int(source.get("body_bytes_seen"), field="body_bytes_seen")
    body_inspected = _nonnegative_int(
        source.get("body_bytes_inspected"), field="body_bytes_inspected"
    )
    first_chunk_size = _nonnegative_int(observation.get("first_chunk_size"), field="first_chunk_size")
    if body_inspected > body_seen:
        raise ValueError("Common P4 body_bytes_inspected exceeds body_bytes_seen")
    if body_seen < first_chunk_size or body_inspected < first_chunk_size:
        raise ValueError("Common P4 body counters do not cover the observed first chunk")
    source_http_status = _http_status(source.get("http_status"), field="http_status")
    original_http_status = _http_status(
        source.get("original_http_status"), field="original_http_status"
    )
    visible_http_status = _http_status(
        source.get("visible_http_status"), field="visible_http_status"
    )
    if source_http_status != 403 or original_http_status != 200 or visible_http_status != 200:
        raise ValueError("Common P4 safe event has unexpected status metadata")
    normalized_run_id = (
        _bounded_token(run_id, field="run_id", maximum=256) if run_id else None
    )
    evidence: dict[str, object] = {
        "schema_version": 1,
        "evidence_type": "synchronized_first_byte",
        "evidence_origin": "real_host",
        "promotion_eligible": True,
        "client_first_byte_received": True,
        "first_byte_before_response_end": True,
        "first_chunk_size": first_chunk_size,
        "upstream_paused": True,
        "upstream_eos_sent_at_first_byte": False,
        "upstream_response_finished_at_first_byte": False,
        "response_committed": True,
        "body_bytes_seen": body_seen,
        "body_bytes_inspected": body_inspected,
        "no_full_response_buffering": True,
        "connector_owned_full_response_buffer": False,
        "transport_protocol": "http1",
        "body_payload_persisted": False,
        "outcome": "PASS",
    }
    barrier_event: dict[str, object] = {
        "connector": "envoy",
        "integration_mode": "ext_proc",
        "event": "phase4_first_byte_barrier",
        "message_id": "MSCONN_EVENT_P4_FIRST_BYTE_BARRIER",
        "transaction_id": transaction,
        "rule_id": "1100301",
        "phase": 4,
        "status": "observed",
        "http_status": source_http_status,
        "original_http_status": original_http_status,
        "visible_http_status": visible_http_status,
        "requested_action": "deny",
        "actual_action": "log_only",
        "late_intervention": True,
        "late_intervention_mode": "safe",
        "headers_sent": True,
        "body_started": True,
        "response_committed": True,
        "connection_aborted": False,
        "transport_result": "log_only",
        "end_of_stream_evaluation": True,
        "eos_seen": True,
        "cleanup_reason": "normal",
        "client_first_byte_received": True,
        "first_byte_before_response_end": True,
        "first_chunk_size": first_chunk_size,
        "upstream_paused": True,
        "upstream_eos_sent_at_first_byte": False,
        "upstream_response_finished_at_first_byte": False,
        "body_bytes_seen": body_seen,
        "body_bytes_inspected": body_inspected,
        "no_full_response_buffering": True,
        "negotiated_protocol": "http1",
        "transport": "tcp",
        "transport_case_id": "phase4_first_byte_before_response_end",
        "barrier_id": "envoy-ext-proc-p4-first-byte",
    }
    if normalized_run_id is not None:
        barrier_event["run_id"] = normalized_run_id
    if evidence_output:
        destination = Path(evidence_output)
        if not destination.is_absolute() or destination.is_symlink():
            raise ValueError("first-byte evidence output must be an absolute regular path")
        write_json_atomic(destination, evidence)
    existing_barriers = [
        record
        for record in _load_jsonl(event_path)
        if record.get("event") == barrier_event["event"]
        and record.get("transaction_id") == transaction
        and record.get("transport_case_id") == barrier_event["transport_case_id"]
    ]
    if existing_barriers:
        if len(existing_barriers) != 1:
            raise ValueError("phase-4 first-byte barrier event was emitted more than once")
        existing = existing_barriers[0]
        for field in (
            "rule_id",
            "phase",
            "requested_action",
            "actual_action",
            "late_intervention_mode",
            "first_byte_before_response_end",
            "upstream_eos_sent_at_first_byte",
            "no_full_response_buffering",
        ):
            if existing.get(field) != barrier_event[field]:
                raise ValueError("existing phase-4 first-byte barrier event is not causally bound")
        appended = False
    else:
        with event_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(barrier_event, sort_keys=True) + "\n")
        appended = True
    return {
        "schema_version": 1,
        "evidence_written": bool(evidence_output),
        "event_appended": appended,
        "transaction_id": transaction,
        "body_payload_persisted": False,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("free-port")
    ports = subparsers.add_parser("free-ports")
    ports.add_argument("--count", required=True, type=int)
    serve = subparsers.add_parser("serve-upstream")
    serve.add_argument("--port", required=True, type=int)
    serve.add_argument("--client-cancel-delay", default=5.0, type=float)
    serve.add_argument("--phase4-barrier-dir")
    serve.add_argument("--phase4-barrier-timeout", default=10.0, type=float)
    request = subparsers.add_parser("probe")
    request.add_argument("--url", required=True)
    request.add_argument("--header", action="append", default=[])
    request.add_argument("--method", default="GET")
    request.add_argument("--data")
    request.add_argument("--no-redirect", action="store_true")
    cancel = subparsers.add_parser("client-cancel")
    cancel.add_argument("--host", required=True)
    cancel.add_argument("--port", required=True, type=int)
    cancel.add_argument("--path", default="/client-cancel")
    cancel.add_argument("--header", action="append", default=[])
    phase4 = subparsers.add_parser("phase4-first-byte")
    phase4.add_argument("--host", required=True)
    phase4.add_argument("--port", required=True, type=int)
    phase4.add_argument("--path", default="/phase4-marker")
    phase4.add_argument("--header", action="append", default=[])
    phase4.add_argument("--barrier-dir", required=True)
    phase4.add_argument("--timeout", default=10.0, type=float)
    phase4.add_argument("--output")
    finalize = subparsers.add_parser("write-phase4-first-byte-evidence")
    finalize.add_argument("--event-log", required=True)
    finalize.add_argument("--observation", required=True)
    finalize.add_argument("--transaction-id", required=True)
    finalize.add_argument("--evidence-output")
    finalize.add_argument("--run-id")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.command == "free-port":
        print(free_port())
        return 0
    if args.command == "free-ports":
        if args.count < 1 or args.count > 16:
            raise ValueError("free port count must be between 1 and 16")
        print(" ".join(str(port) for port in free_ports(args.count)))
        return 0
    if args.command == "serve-upstream":
        return serve_upstream(
            args.port,
            args.client_cancel_delay,
            args.phase4_barrier_dir,
            args.phase4_barrier_timeout,
        )
    if args.command == "probe":
        return probe(args.url, args.header, args.method, args.data, args.no_redirect)
    if args.command == "client-cancel":
        print(json.dumps(client_cancel(args.host, args.port, args.path, args.header), sort_keys=True))
        return 0
    if args.command == "phase4-first-byte":
        observation = phase4_first_byte(
            args.host,
            args.port,
            args.path,
            args.header,
            args.barrier_dir,
            args.timeout,
        )
        if args.output:
            output = Path(args.output)
            if not output.is_absolute() or output.is_symlink():
                raise ValueError("phase-4 observation output must be an absolute regular path")
            write_json_atomic(output, observation)
        print(json.dumps(observation, sort_keys=True))
        return 0
    if args.command == "write-phase4-first-byte-evidence":
        result = write_phase4_first_byte_evidence(
            event_log=args.event_log,
            observation_path=args.observation,
            transaction_id=args.transaction_id,
            evidence_output=args.evidence_output,
            run_id=args.run_id,
        )
        print(json.dumps(result, sort_keys=True))
        return 0
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"envoy_smoke_helper: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
