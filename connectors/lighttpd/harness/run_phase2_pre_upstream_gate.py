#!/usr/bin/env python3
"""Exercise the patched-lighttpd HTTP/1.1 pre-upstream Phase-2 gate.

The runner starts only task-owned foreground processes.  Its loopback upstream
stores bounded framing metadata and counters, never request payloads or header
values.  It proves that a delayed chunked request cannot connect to the proxy
upstream before ModSecurity finishes Phase 2, while a complete allowed request
is still delivered after that decision.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import threading
import time
from typing import Any


MAX_HEADERS = 16 * 1024
MAX_BODY = 1024 * 1024


class GateFailure(RuntimeError):
    """A required gate assertion or task-owned cleanup check failed."""


def start_token(pid: int) -> str:
    stat_path = Path(f"/proc/{pid}/stat")
    try:
        suffix = stat_path.read_text(encoding="utf-8").rsplit(")", 1)[1].split()
        token = suffix[19]
    except (FileNotFoundError, IndexError, OSError) as exc:
        raise GateFailure(f"could not read start token for PID {pid}") from exc
    if not token.isdecimal():
        raise GateFailure(f"invalid start token for PID {pid}")
    return token


def still_owned(process: subprocess.Popen[bytes], token: str) -> bool:
    return process.poll() is None and start_token(process.pid) == token


def stop_owned(process: subprocess.Popen[bytes], token: str, label: str) -> dict[str, Any]:
    result: dict[str, Any] = {"label": label, "pid": process.pid, "start_token": token}
    if process.poll() is not None:
        result["already_exited"] = process.returncode
        return result
    if not still_owned(process, token):
        raise GateFailure(f"refusing to signal changed {label} PID")
    process.terminate()
    try:
        result["returncode"] = process.wait(timeout=5)
        result["signal"] = "TERM"
        return result
    except subprocess.TimeoutExpired:
        if not still_owned(process, token):
            raise GateFailure(f"refusing to SIGKILL changed {label} PID")
        process.kill()
        result["returncode"] = process.wait(timeout=5)
        result["signal"] = "KILL"
        return result


def listener_rows(port: int) -> list[str]:
    probe = subprocess.run(
        ["ss", "-H", "-ltnpe", f"sport = :{port}"],
        check=False,
        capture_output=True,
        text=True,
    )
    if probe.returncode != 0:
        raise GateFailure(f"ss listener probe failed for port {port}")
    return [line for line in probe.stdout.splitlines() if line.strip()]


def wait_for_listener(port: int, expected: bool, timeout: float = 5.0) -> list[str]:
    deadline = time.monotonic() + timeout
    latest: list[str] = []
    while time.monotonic() < deadline:
        latest = listener_rows(port)
        if bool(latest) == expected:
            return latest
        time.sleep(0.05)
    state = "present" if expected else "absent"
    raise GateFailure(f"listener on port {port} did not become {state}")


class ChunkAwareMetadataUpstream:
    """Task-owned HTTP/1.1 upstream retaining counters and framing only."""

    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port
        self._listener: socket.socket | None = None
        self._thread: threading.Thread | None = None
        self._stop = threading.Event()
        self._lock = threading.Lock()
        self._records: list[dict[str, Any]] = []
        self._accepted_connections = 0

    def start(self) -> None:
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((self._host, self._port))
        listener.listen(16)
        listener.settimeout(0.2)
        self._listener = listener
        self._thread = threading.Thread(target=self._serve, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._listener is not None:
            self._listener.close()
        if self._thread is not None:
            self._thread.join(timeout=3)
            if self._thread.is_alive():
                raise GateFailure("metadata upstream did not stop")

    def snapshot(self) -> list[dict[str, Any]]:
        with self._lock:
            return [dict(record) for record in self._records]

    def accepted_connections(self) -> int:
        with self._lock:
            return self._accepted_connections

    def _record(self, metadata: dict[str, Any]) -> None:
        with self._lock:
            metadata["connection_index"] = len(self._records) + 1
            self._records.append(metadata)

    def _serve(self) -> None:
        assert self._listener is not None
        while not self._stop.is_set():
            try:
                connection, _ = self._listener.accept()
            except TimeoutError:
                continue
            except OSError:
                if self._stop.is_set():
                    return
                raise
            with self._lock:
                self._accepted_connections += 1
            threading.Thread(target=self._handle, args=(connection,), daemon=True).start()

    def _handle(self, connection: socket.socket) -> None:
        metadata: dict[str, Any] = {
            "complete": False,
            "content_length_present": False,
            "error": None,
            "headers_received": False,
            "received_body_wire_bytes": 0,
            "transfer_encoding_chunked": False,
            "upstream_response_sent": False,
        }
        with connection:
            try:
                connection.settimeout(2)
                received = bytearray()
                while b"\r\n\r\n" not in received:
                    data = connection.recv(4096)
                    if not data:
                        raise GateFailure("upstream client closed before headers")
                    received.extend(data)
                    if len(received) > MAX_HEADERS:
                        raise GateFailure("upstream headers exceeded bound")
                raw_headers, body = bytes(received).split(b"\r\n\r\n", 1)
                header_lines = raw_headers.split(b"\r\n")
                request_line = header_lines[0].split()
                if len(request_line) != 3:
                    raise GateFailure("upstream received malformed request line")
                metadata["method"] = request_line[0].decode("ascii", errors="replace")
                metadata["path"] = request_line[1].decode("ascii", errors="replace")
                content_length: int | None = None
                for header in header_lines[1:]:
                    name, separator, value = header.partition(b":")
                    if not separator:
                        continue
                    normalized_name = name.strip().lower()
                    if normalized_name == b"content-length":
                        if content_length is not None:
                            raise GateFailure("upstream received duplicate content length")
                        content_length = int(value.strip())
                    elif normalized_name == b"transfer-encoding":
                        tokens = {part.strip().lower() for part in value.split(b",")}
                        metadata["transfer_encoding_chunked"] = b"chunked" in tokens
                metadata["headers_received"] = True
                metadata["received_body_wire_bytes"] = len(body)
                if content_length is not None:
                    if content_length < 0 or content_length > MAX_BODY:
                        raise GateFailure("upstream content length exceeded bound")
                    metadata["content_length_present"] = True
                    metadata["declared_content_length"] = content_length
                    while metadata["received_body_wire_bytes"] < content_length:
                        data = connection.recv(
                            min(4096, content_length - metadata["received_body_wire_bytes"])
                        )
                        if not data:
                            metadata["read_termination"] = "eof"
                            break
                        metadata["received_body_wire_bytes"] += len(data)
                    metadata["complete"] = (
                        metadata["received_body_wire_bytes"] == content_length
                    )
                elif metadata["transfer_encoding_chunked"]:
                    wire = bytearray(body)
                    metadata["received_body_payload_bytes"] = 0
                    metadata["received_chunk_count"] = 0
                    metadata["terminal_chunk_seen"] = False
                    state = "size"
                    remaining = 0
                    while not metadata["terminal_chunk_seen"]:
                        while True:
                            if state == "size":
                                line_end = wire.find(b"\r\n")
                                if line_end < 0:
                                    break
                                token = bytes(wire[:line_end]).split(b";", 1)[0].strip()
                                del wire[: line_end + 2]
                                if not token or len(token) > 16:
                                    raise GateFailure("upstream chunk-size is invalid")
                                remaining = int(token, 16)
                                if remaining == 0:
                                    state = "trailers"
                                else:
                                    if (
                                        metadata["received_body_payload_bytes"] + remaining
                                        > MAX_BODY
                                    ):
                                        raise GateFailure("upstream chunk body exceeded bound")
                                    metadata["received_chunk_count"] += 1
                                    state = "data"
                            elif state == "data":
                                available = min(len(wire), remaining)
                                if available:
                                    del wire[:available]
                                    metadata["received_body_payload_bytes"] += available
                                    remaining -= available
                                if remaining:
                                    break
                                state = "data_crlf"
                            elif state == "data_crlf":
                                if len(wire) < 2:
                                    break
                                if bytes(wire[:2]) != b"\r\n":
                                    raise GateFailure("upstream chunk data missing CRLF")
                                del wire[:2]
                                state = "size"
                            elif state == "trailers":
                                line_end = wire.find(b"\r\n")
                                if line_end < 0:
                                    break
                                del wire[: line_end + 2]
                                if line_end == 0:
                                    metadata["terminal_chunk_seen"] = True
                                    break
                            else:
                                raise GateFailure("invalid upstream chunk parser state")
                        if metadata["terminal_chunk_seen"]:
                            break
                        data = connection.recv(4096)
                        if not data:
                            metadata["read_termination"] = "eof"
                            break
                        metadata["received_body_wire_bytes"] += len(data)
                        if metadata["received_body_wire_bytes"] > MAX_BODY:
                            raise GateFailure("upstream body wire data exceeded bound")
                        wire.extend(data)
                    metadata["complete"] = bool(metadata["terminal_chunk_seen"])
                else:
                    metadata["complete"] = True
                    metadata["read_termination"] = "no_body_framing"
                if metadata["complete"]:
                    connection.sendall(
                        b"HTTP/1.1 200 OK\r\nContent-Length: 3\r\n"
                        b"Connection: close\r\n\r\nok\n"
                    )
                    metadata["upstream_response_sent"] = True
            except Exception as exc:  # retain only bounded error text
                metadata["error"] = str(exc)
            finally:
                self._record(metadata)


def read_status(connection: socket.socket) -> int:
    response = bytearray()
    while b"\r\n\r\n" not in response:
        data = connection.recv(4096)
        if not data:
            raise GateFailure("host closed request before response headers")
        response.extend(data)
        if len(response) > MAX_HEADERS:
            raise GateFailure("host response headers exceeded bound")
    status_line = bytes(response).split(b"\r\n", 1)[0].split()
    if len(status_line) < 2:
        raise GateFailure("host response status line is invalid")
    try:
        return int(status_line[1])
    except ValueError as exc:
        raise GateFailure("host response status is invalid") from exc


def send_content_length(
    port: int, label: str, body: bytes, headers: dict[str, str] | None = None
) -> int:
    request_headers = [
        f"POST /{label} HTTP/1.1",
        "Host: 127.0.0.1",
        "Content-Type: text/plain",
        f"Content-Length: {len(body)}",
        "Connection: close",
    ]
    if headers is not None:
        request_headers.extend(f"{name}: {value}" for name, value in headers.items())
    request = ("\r\n".join(request_headers) + "\r\n\r\n").encode("ascii") + body
    with socket.create_connection(("127.0.0.1", port), timeout=5) as connection:
        connection.settimeout(5)
        connection.sendall(request)
        return read_status(connection)


def send_delayed_chunked(
    port: int, label: str, body: bytes, before_terminal: callable
) -> tuple[int, dict[str, Any]]:
    split = max(1, len(body) // 2)
    chunks = (body[:split], body[split:])
    if not all(chunks):
        raise GateFailure("chunked body must produce two nonempty chunks")
    request = (
        f"POST /{label} HTTP/1.1\r\n"
        "Host: 127.0.0.1\r\n"
        "Content-Type: text/plain\r\n"
        "Transfer-Encoding: chunked\r\n"
        "Connection: close\r\n\r\n"
    ).encode("ascii")
    with socket.create_connection(("127.0.0.1", port), timeout=5) as connection:
        connection.settimeout(5)
        connection.sendall(request)
        for chunk in chunks:
            connection.sendall(f"{len(chunk):X}\r\n".encode("ascii"))
            connection.sendall(chunk)
            connection.sendall(b"\r\n")
            time.sleep(0.05)
        observation = before_terminal()
        connection.sendall(b"0\r\n\r\n")
        return read_status(connection), observation


def assert_no_upstream_before_terminal(
    upstream: ChunkAwareMetadataUpstream, baseline: int
) -> dict[str, Any]:
    deadline = time.monotonic() + 1
    while time.monotonic() < deadline:
        accepted = upstream.accepted_connections()
        if accepted != baseline or len(upstream.snapshot()) != baseline:
            raise GateFailure("request reached upstream before terminal Phase-2 decision")
        time.sleep(0.05)
    return {
        "accepted_connections": 0,
        "received_body_payload_bytes": 0,
        "upstream_response_sent": False,
    }


def await_completed_upstream(
    upstream: ChunkAwareMetadataUpstream, baseline: int, label: str
) -> dict[str, Any]:
    deadline = time.monotonic() + 3
    expected_path = f"/{label}"
    while time.monotonic() < deadline:
        records = upstream.snapshot()[baseline:]
        for record in records:
            if record.get("path") == expected_path and record.get("complete"):
                return record
        time.sleep(0.05)
    raise GateFailure("allowed request did not complete at upstream")


def write_runtime_inputs(
    root: Path,
    *,
    rules_file: Path,
    host_port: int,
    upstream_port: int,
    configured_streaming: bool,
    upgrade_request_body: bool,
    body_limit_action: str = "reject",
) -> dict[str, Path]:
    document_root = root / "document-root"
    upload_dir = root / "upload"
    document_root.mkdir(parents=True)
    upload_dir.mkdir()
    (document_root / "index.html").write_text("phase2 pre-upstream gate\n", encoding="utf-8")
    event_path = root / "events.jsonl"
    event_path.write_text("", encoding="utf-8")
    runtime_config = root / "msconnector-runtime.conf"
    runtime_config.write_text(
        "\n".join(
            (
                "enabled=on",
                f"rules_file={rules_file}",
                "transaction_id_header=x-modsec-transaction-id",
                "request_body_mode=streaming",
                "response_body_mode=none",
                "request_body_limit=1048576",
                "response_body_limit=1048576",
                f"body_limit_action={body_limit_action}",
                "default_block_status=403",
                "default_error_status=500",
                "max_header_count=256",
                "max_header_name_size=256",
                "max_header_value_size=8192",
                "max_total_header_bytes=65536",
                "max_event_json_bytes=16384",
                f"event_path={event_path}",
                "",
            )
        ),
        encoding="utf-8",
    )
    config_lines = [
        'server.compat-module-load = "disable"',
        'server.modules = ( "mod_proxy", "mod_msconnector" )',
        f'server.document-root = "{document_root}"',
        'server.bind = "127.0.0.1"',
        f"server.port = {host_port}",
        f'server.errorlog = "{root / "lighttpd-error.log"}"',
        f'server.pid-file = "{root / "lighttpd.pid"}"',
        f'server.upload-dirs = ( "{upload_dir}" )',
        'msconnector.enabled = "enable"',
        f'msconnector.config-file = "{runtime_config}"',
        "proxy.server = (",
        f'  "/" => ( ( "host" => "127.0.0.1", "port" => {upstream_port} ) )',
        ")",
        "",
    ]
    if configured_streaming:
        config_lines.insert(7, "server.stream-request-body = 1")
    if upgrade_request_body:
        config_lines.insert(
            8,
            'server.feature-flags += ( "gw.upgrade-with-request-body" => "enable" )',
        )
        config_lines.insert(-1, 'proxy.header = ( "upgrade" => "enable" )')
    config = root / "lighttpd.conf"
    config.write_text("\n".join(config_lines), encoding="utf-8")
    return {"config": config, "event_path": event_path}


def start_host(
    *,
    root: Path,
    binary: Path,
    module_dir: Path,
    config: Path,
    library_dir: Path,
) -> tuple[subprocess.Popen[bytes], str]:
    config_check = subprocess.run(
        [str(binary), "-m", str(module_dir), "-tt", "-f", str(config)],
        check=False,
        capture_output=True,
    )
    (root / "config-check.stdout").write_bytes(config_check.stdout)
    (root / "config-check.stderr").write_bytes(config_check.stderr)
    if config_check.returncode != 0:
        raise GateFailure("lighttpd config check failed")
    environment = dict(os.environ)
    environment["LD_LIBRARY_PATH"] = str(library_dir) + (
        ":" + environment["LD_LIBRARY_PATH"] if environment.get("LD_LIBRARY_PATH") else ""
    )
    stdout = (root / "lighttpd.stdout").open("wb")
    stderr = (root / "lighttpd.stderr").open("wb")
    try:
        process = subprocess.Popen(
            [str(binary), "-D", "-m", str(module_dir), "-f", str(config)],
            stdout=stdout,
            stderr=stderr,
            env=environment,
        )
    finally:
        stdout.close()
        stderr.close()
    return process, start_token(process.pid)


def ensure_regular(path: Path, label: str, *, executable: bool = False) -> Path:
    if path.is_symlink() or not path.is_file():
        raise GateFailure(f"{label} must be a regular file")
    if executable and not os.access(path, os.X_OK):
        raise GateFailure(f"{label} must be executable")
    return path.resolve()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--lighttpd-bin", type=Path, required=True)
    parser.add_argument("--module-dir", type=Path, required=True)
    parser.add_argument("--rules-file", type=Path, required=True)
    parser.add_argument("--host-port", type=int, required=True)
    parser.add_argument("--configured-host-port", type=int, required=True)
    parser.add_argument("--upstream-port", type=int, required=True)
    parser.add_argument("--modsecurity-lib-dir", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    if root.is_symlink() or not root.is_dir() or (root / "summary.json").exists():
        raise GateFailure("runtime root must be an existing fresh regular directory")
    binary = ensure_regular(args.lighttpd_bin, "lighttpd binary", executable=True)
    rules_file = ensure_regular(args.rules_file, "rules file")
    if args.module_dir.is_symlink() or not (args.module_dir / "mod_msconnector.so").is_file():
        raise GateFailure("connector module is missing")
    if not (args.module_dir / "mod_proxy.so").is_file():
        raise GateFailure("proxy module is missing")
    library_dir = args.modsecurity_lib_dir.resolve()
    if not library_dir.is_dir() or library_dir.is_symlink():
        raise GateFailure("ModSecurity library directory is invalid")
    ports = (args.host_port, args.configured_host_port, args.upstream_port)
    if len(set(ports)) != len(ports) or any(port < 1024 or port > 65535 for port in ports):
        raise GateFailure("ports must be distinct unprivileged TCP ports")

    summary: dict[str, Any] = {
        "schema_version": 1,
        "kind": "patched_lighttpd_phase2_pre_upstream_gate",
        "body_payload_persisted": False,
        "host_port": args.host_port,
        "configured_host_port": args.configured_host_port,
        "upstream_port": args.upstream_port,
        "cases": [],
        "cleanup": {},
        "result": "failed",
    }
    upstream: ChunkAwareMetadataUpstream | None = None
    active_host: tuple[subprocess.Popen[bytes], str, str] | None = None
    try:
        if any(listener_rows(port) for port in ports):
            raise GateFailure("a selected task port is already listening")
        upstream = ChunkAwareMetadataUpstream("127.0.0.1", args.upstream_port)
        upstream.start()

        normal_root = root / "normal"
        normal_inputs = write_runtime_inputs(
            normal_root,
            rules_file=rules_file,
            host_port=args.host_port,
            upstream_port=args.upstream_port,
            configured_streaming=False,
            upgrade_request_body=False,
        )
        normal_process, normal_token = start_host(
            root=normal_root,
            binary=binary,
            module_dir=args.module_dir.resolve(),
            config=normal_inputs["config"],
            library_dir=library_dir,
        )
        active_host = (normal_process, normal_token, "normal foreground lighttpd")
        wait_for_listener(args.host_port, True)
        if not still_owned(normal_process, normal_token):
            raise GateFailure("normal foreground lighttpd did not remain alive")

        marker = b"msconnector-p2-only"
        marker_baseline = upstream.accepted_connections()
        marker_status, marker_preterminal = send_delayed_chunked(
            args.host_port,
            "phase2-marker-delayed",
            marker,
            lambda: assert_no_upstream_before_terminal(upstream, marker_baseline),
        )
        if marker_status != 403 or upstream.accepted_connections() != marker_baseline:
            raise GateFailure("delayed Phase-2 marker did not fail closed")
        summary["cases"].append(
            {
                "label": "delayed_chunked_phase2_marker",
                "http_status": marker_status,
                "request_body_bytes": len(marker),
                "pre_terminal_upstream_observation": marker_preterminal,
                "upstream_connections_after": upstream.accepted_connections(),
                "upstream_connections_before": marker_baseline,
            }
        )

        allowed = b"0" * 32
        allow_baseline = upstream.accepted_connections()
        allow_status, allow_preterminal = send_delayed_chunked(
            args.host_port,
            "phase2-allow-delayed",
            allowed,
            lambda: assert_no_upstream_before_terminal(upstream, allow_baseline),
        )
        allow_record = await_completed_upstream(
            upstream, allow_baseline, "phase2-allow-delayed"
        )
        if allow_status != 200 or upstream.accepted_connections() != allow_baseline + 1:
            raise GateFailure("allowed delayed request was not delivered exactly once")
        if allow_record.get("received_body_wire_bytes") != len(allowed):
            raise GateFailure("allowed delayed request had an unexpected upstream byte count")
        summary["cases"].append(
            {
                "label": "delayed_chunked_phase2_allow",
                "http_status": allow_status,
                "request_body_bytes": len(allowed),
                "pre_terminal_upstream_observation": allow_preterminal,
                "upstream_delivery": {
                    "accepted_connections": 1,
                    "content_length_present": allow_record.get("content_length_present"),
                    "received_body_wire_bytes": allow_record.get("received_body_wire_bytes"),
                    "transfer_encoding_chunked": allow_record.get("transfer_encoding_chunked"),
                    "upstream_response_sent": allow_record.get("upstream_response_sent"),
                },
            }
        )

        immediate_baseline = upstream.accepted_connections()
        immediate_status, _ = send_delayed_chunked(
            args.host_port,
            "phase2-marker-immediate",
            marker,
            lambda: {"not_delayed": True},
        )
        if immediate_status != 403 or upstream.accepted_connections() != immediate_baseline:
            raise GateFailure("immediate Phase-2 marker did not fail closed")
        summary["cases"].append(
            {
                "label": "immediate_chunked_phase2_marker",
                "http_status": immediate_status,
                "upstream_connections_before": immediate_baseline,
                "upstream_connections_after": upstream.accepted_connections(),
            }
        )

        for label, headers in (("incremental-request-stream", {"Incremental": "?1"}),):
            baseline = upstream.accepted_connections()
            status = send_content_length(args.host_port, label, b"x", headers)
            if status != 501 or upstream.accepted_connections() != baseline:
                raise GateFailure(
                    f"{label} did not fail closed: status={status} "
                    f"upstream_connections={upstream.accepted_connections() - baseline}"
                )
            summary["cases"].append(
                {
                    "label": label,
                    "http_status": status,
                    "upstream_connections_before": baseline,
                    "upstream_connections_after": upstream.accepted_connections(),
                }
            )

        summary["cleanup"]["normal_lighttpd"] = stop_owned(
            normal_process, normal_token, "normal foreground lighttpd"
        )
        active_host = None
        wait_for_listener(args.host_port, False)

        process_partial_root = root / "process-partial"
        process_partial_inputs = write_runtime_inputs(
            process_partial_root,
            rules_file=rules_file,
            host_port=args.configured_host_port,
            upstream_port=args.upstream_port,
            configured_streaming=False,
            upgrade_request_body=False,
            body_limit_action="process_partial",
        )
        process_partial_baseline = upstream.accepted_connections()
        process_partial_check = subprocess.run(
            [
                str(binary),
                "-m",
                str(args.module_dir.resolve()),
                "-tt",
                "-f",
                str(process_partial_inputs["config"]),
            ],
            check=False,
            capture_output=True,
        )
        process_partial_output = (
            process_partial_check.stdout + process_partial_check.stderr
        )
        process_partial_log = process_partial_root / "lighttpd-error.log"
        if process_partial_log.is_file():
            process_partial_output += process_partial_log.read_bytes()
        if process_partial_check.returncode == 0:
            raise GateFailure("streaming process_partial configuration unexpectedly loaded")
        if (
            b"requires body_limit_action=reject" not in process_partial_output
            or listener_rows(args.configured_host_port)
            or upstream.accepted_connections() != process_partial_baseline
        ):
            raise GateFailure("streaming process_partial configuration did not fail closed")
        summary["cases"].append(
            {
                "label": "process_partial_body_limit_action",
                "config_check_returncode": process_partial_check.returncode,
                "upstream_connections_before": process_partial_baseline,
                "upstream_connections_after": upstream.accepted_connections(),
            }
        )

        configured_root = root / "configured-stream"
        configured_inputs = write_runtime_inputs(
            configured_root,
            rules_file=rules_file,
            host_port=args.configured_host_port,
            upstream_port=args.upstream_port,
            configured_streaming=True,
            upgrade_request_body=False,
        )
        configured_process, configured_token = start_host(
            root=configured_root,
            binary=binary,
            module_dir=args.module_dir.resolve(),
            config=configured_inputs["config"],
            library_dir=library_dir,
        )
        active_host = (configured_process, configured_token, "configured foreground lighttpd")
        wait_for_listener(args.configured_host_port, True)
        baseline = upstream.accepted_connections()
        configured_status = send_content_length(
            args.configured_host_port, "configured-request-stream", b"x"
        )
        if configured_status != 501 or upstream.accepted_connections() != baseline:
            raise GateFailure("configured request streaming did not fail closed")
        summary["cases"].append(
            {
                "label": "configured_request_stream",
                "http_status": configured_status,
                "upstream_connections_before": baseline,
                "upstream_connections_after": upstream.accepted_connections(),
            }
        )
        summary["cleanup"]["configured_lighttpd"] = stop_owned(
            configured_process, configured_token, "configured foreground lighttpd"
        )
        active_host = None
        wait_for_listener(args.configured_host_port, False)

        upgrade_root = root / "enabled-upgrade"
        upgrade_inputs = write_runtime_inputs(
            upgrade_root,
            rules_file=rules_file,
            host_port=args.configured_host_port,
            upstream_port=args.upstream_port,
            configured_streaming=False,
            upgrade_request_body=True,
        )
        upgrade_process, upgrade_token = start_host(
            root=upgrade_root,
            binary=binary,
            module_dir=args.module_dir.resolve(),
            config=upgrade_inputs["config"],
            library_dir=library_dir,
        )
        active_host = (upgrade_process, upgrade_token, "enabled-upgrade foreground lighttpd")
        wait_for_listener(args.configured_host_port, True)
        baseline = upstream.accepted_connections()
        upgrade_status = send_content_length(
            args.configured_host_port,
            "body-bearing-upgrade-enabled",
            b"x",
            {"Connection": "Upgrade", "Upgrade": "websocket"},
        )
        if upgrade_status != 501 or upstream.accepted_connections() != baseline:
            raise GateFailure("enabled body-bearing Upgrade did not fail closed")
        summary["cases"].append(
            {
                "label": "body_bearing_upgrade_enabled",
                "http_status": upgrade_status,
                "upstream_connections_before": baseline,
                "upstream_connections_after": upstream.accepted_connections(),
            }
        )
        summary["cleanup"]["enabled_upgrade_lighttpd"] = stop_owned(
            upgrade_process, upgrade_token, "enabled-upgrade foreground lighttpd"
        )
        active_host = None
        wait_for_listener(args.configured_host_port, False)
        summary["upstream"] = upstream.snapshot()
        summary["result"] = "passed"
    except Exception as exc:
        summary["error"] = str(exc)
    finally:
        if active_host is not None:
            process, token, label = active_host
            try:
                summary["cleanup"]["active_lighttpd"] = stop_owned(process, token, label)
            except Exception as exc:
                summary["cleanup"]["active_lighttpd_error"] = str(exc)
        if upstream is not None:
            try:
                upstream.stop()
                summary["cleanup"]["upstream"] = "stopped"
            except Exception as exc:
                summary["cleanup"]["upstream_error"] = str(exc)
        try:
            summary["cleanup"]["host_listener_after"] = listener_rows(args.host_port)
            summary["cleanup"]["configured_host_listener_after"] = listener_rows(
                args.configured_host_port
            )
            summary["cleanup"]["upstream_listener_after"] = listener_rows(args.upstream_port)
            if summary["result"] == "passed" and any(
                summary["cleanup"][name]
                for name in (
                    "host_listener_after",
                    "configured_host_listener_after",
                    "upstream_listener_after",
                )
            ):
                summary["result"] = "failed"
                summary["error"] = "task-owned listener cleanup did not pass"
        except Exception as exc:
            summary["cleanup"]["probe_error"] = str(exc)
            summary["result"] = "failed"
        temporary = root / "summary.json.tmp"
        temporary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        os.replace(temporary, root / "summary.json")
    return 0 if summary["result"] == "passed" else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GateFailure as exc:
        print(f"lighttpd Phase-2 pre-upstream gate: {exc}", file=sys.stderr)
        raise SystemExit(1)
