#!/usr/bin/env python3
"""Bounded, payload-free traffic helper owned by the Parent Apache harness.

This helper never starts, stops, or configures Apache.  The calling harness
already owns that lifecycle; it supplies one live launch PID only so this
helper can request and verify bounded graceful-restart attempts while its
fixed loopback traffic remains active.
"""

from __future__ import annotations

from collections import Counter
import argparse
import http.client
import json
import os
from pathlib import Path
import signal
import socket
import tempfile
import threading
import time
from typing import Any


RESPONSE_BOUND = 65536
REQUEST_PATH = "/__request_body_consume"
ALLOW_PAYLOAD = b"request-body-allow-marker"
DENY_PAYLOAD = b"request-body-block-marker"
LARGE_PAYLOAD = b"request-body-large-prefix-" + (b"a" * 1048577)


def bounded_text(value: object, limit: int = 512) -> str:
    return str(value or "").replace("\r", " ").replace("\n", " ").strip()[:limit]


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(payload, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, 0o600)
        os.replace(temporary, path)
    finally:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass


def normal_request(port: int, timeout: int, payload: bytes, expected: int) -> None:
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=timeout)
    try:
        connection.request(
            "POST",
            REQUEST_PATH,
            body=payload,
            headers={"Content-Type": "text/plain", "Connection": "keep-alive"},
        )
        response = connection.getresponse()
        body = response.read(RESPONSE_BOUND + 1)
        if len(body) > RESPONSE_BOUND:
            raise RuntimeError("Apache soak response exceeded the 64 KiB evidence bound")
        if response.status != expected:
            raise RuntimeError(f"expected HTTP {expected}, observed {response.status}")
    finally:
        connection.close()


def multi_bucket_request(port: int, timeout: int, expected: int) -> None:
    chunks = (b"request-body-", b"block-marker")
    request = [
        b"POST /__request_body_consume HTTP/1.1\r\n",
        b"Host: 127.0.0.1\r\n",
        b"Content-Type: text/plain\r\n",
        b"Transfer-Encoding: chunked\r\n",
        b"Connection: close\r\n\r\n",
    ]
    for chunk in chunks:
        request.extend((f"{len(chunk):X}\r\n".encode("ascii"), chunk + b"\r\n"))
    request.append(b"0\r\n\r\n")
    with socket.create_connection(("127.0.0.1", port), timeout=timeout) as client:
        client.settimeout(timeout)
        for part in request:
            client.sendall(part)
        response = bytearray()
        while b"\r\n\r\n" not in response:
            block = client.recv(4096)
            if not block:
                break
            response.extend(block)
            if len(response) > RESPONSE_BOUND:
                raise RuntimeError("Apache soak response headers exceeded the 64 KiB evidence bound")
    headers, separator, _ = bytes(response).partition(b"\r\n\r\n")
    if not separator:
        raise RuntimeError("multi-bucket request received no response headers")
    status_parts = headers.split(b"\r\n", 1)[0].split()
    if len(status_parts) < 2 or not status_parts[1].isdigit():
        raise RuntimeError("multi-bucket request received an invalid HTTP status")
    status = int(status_parts[1])
    if status != expected:
        raise RuntimeError(f"expected HTTP {expected}, observed {status}")


def request_once(port: int, timeout: int, name: str, payload: bytes | None, expected: int) -> None:
    for attempt in range(2):
        try:
            if name == "multi_bucket":
                multi_bucket_request(port, timeout, expected)
            elif payload is not None:
                normal_request(port, timeout, payload, expected)
            else:
                raise RuntimeError("missing fixed request payload")
            return
        except (OSError, http.client.HTTPException, RuntimeError):
            if attempt:
                raise
            time.sleep(0.05)


def wait_ready(port: int, timeout: int) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            connection = http.client.HTTPConnection("127.0.0.1", port, timeout=1)
            connection.request("GET", "/__modsec_smoke_ready")
            response = connection.getresponse()
            response.read(4096)
            connection.close()
            if response.status == 200:
                return
        except (OSError, http.client.HTTPException):
            pass
        time.sleep(0.05)
    raise RuntimeError("Apache did not become ready after a requested graceful restart")


def real_httpd_child(launch_pid: int) -> int:
    if launch_pid < 1:
        return 0
    children = Path(f"/proc/{launch_pid}/task/{launch_pid}/children")
    try:
        values = children.read_text(encoding="ascii").split()
    except OSError:
        return 0
    for value in values:
        if value.isdigit():
            return int(value)
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--port", type=int, required=True)
    result.add_argument("--launch-pid", type=int, required=True)
    result.add_argument("--duration-seconds", type=int, required=True)
    result.add_argument("--concurrency", type=int, required=True)
    result.add_argument("--request-timeout-seconds", type=int, required=True)
    result.add_argument("--restart-interval-seconds", type=int, required=True)
    result.add_argument("--result", type=Path, required=True)
    result.add_argument("--httpd-version", required=True)
    result.add_argument("--apxs-version", required=True)
    result.add_argument("--compiler", required=True)
    result.add_argument("--mpm", required=True)
    result.add_argument("--libmodsecurity-path", required=True)
    return result


def main() -> int:
    args = parser().parse_args()
    if not 1 <= args.port <= 65535:
        raise SystemExit("port must be between 1 and 65535")
    if not 1 <= args.duration_seconds <= 3600:
        raise SystemExit("duration must be between 1 and 3600 seconds")
    if not 1 <= args.concurrency <= 16:
        raise SystemExit("concurrency must be between 1 and 16")
    if not 1 <= args.request_timeout_seconds <= 120:
        raise SystemExit("request timeout must be between 1 and 120 seconds")
    if not 1 <= args.restart_interval_seconds <= 3600:
        raise SystemExit("restart interval must be between 1 and 3600 seconds")

    shapes = (
        ("allow", ALLOW_PAYLOAD, 200),
        ("deny", DENY_PAYLOAD, 403),
        ("body", ALLOW_PAYLOAD, 200),
        ("large_body", LARGE_PAYLOAD, 200),
        ("multi_bucket", None, 403),
    )
    counters: Counter[str] = Counter()
    errors: list[str] = []
    counter_lock = threading.Lock()
    stop_workers = threading.Event()
    restart_requests = 0
    restart_count = 0
    failure = ""

    def record(name: str) -> None:
        with counter_lock:
            counters[name] += 1

    def worker(worker_index: int, deadline: float) -> None:
        index = worker_index
        while not stop_workers.is_set() and time.monotonic() < deadline:
            name, payload, expected = shapes[index % len(shapes)]
            try:
                request_once(args.port, args.request_timeout_seconds, name, payload, expected)
                record(name)
            except (OSError, http.client.HTTPException, RuntimeError) as exc:
                with counter_lock:
                    errors.append(bounded_text(exc, 256))
                stop_workers.set()
                return
            index += 1

    try:
        for name, payload, expected in shapes:
            request_once(args.port, args.request_timeout_seconds, name, payload, expected)
            record(name)

        deadline = time.monotonic() + args.duration_seconds
        # Start the first request only after every worker exists, then request
        # a graceful restart immediately.  This guarantees that every valid
        # bounded run stresses the new config-pool cleanup while traffic is
        # active; subsequent requests follow the configured cadence.
        next_restart = time.monotonic()
        workers = [
            threading.Thread(target=worker, args=(index, deadline), daemon=False)
            for index in range(args.concurrency)
        ]
        for thread in workers:
            thread.start()
        while time.monotonic() < deadline and not stop_workers.is_set():
            if time.monotonic() >= next_restart:
                os.kill(args.launch_pid, signal.SIGUSR1)
                restart_requests += 1
                wait_ready(args.port, args.request_timeout_seconds)
                restart_count += 1
                next_restart = time.monotonic() + args.restart_interval_seconds
            time.sleep(0.02)
        stop_workers.set()
        for thread in workers:
            thread.join(timeout=args.request_timeout_seconds + 1)
            if thread.is_alive():
                raise RuntimeError("Apache soak worker did not stop within the request timeout")
        if errors:
            raise RuntimeError(f"Apache soak request failure: {errors[0]}")
        if restart_count == 0:
            raise RuntimeError("Apache soak did not complete a requested graceful restart")
    except (OSError, RuntimeError) as exc:
        failure = bounded_text(exc)
    finally:
        atomic_json(
            args.result,
            {
                "schema_version": 1,
                "metadata": {
                    "httpd_version": bounded_text(args.httpd_version),
                    "apxs_version": bounded_text(args.apxs_version),
                    "libmodsecurity_version": "unavailable (shared-object version metadata is not exposed by the Parent harness)",
                    "compiler": bounded_text(args.compiler),
                    "mpm": bounded_text(args.mpm),
                    "libmodsecurity_path": bounded_text(args.libmodsecurity_path),
                },
                "status": "PASS" if not failure else "FAIL",
                "instrumented_httpd_launch_pid": args.launch_pid,
                "real_httpd_pid": real_httpd_child(args.launch_pid),
                "requests": {name: int(counters.get(name, 0)) for name, _, _ in shapes},
                "restart_count": restart_count,
                "restart_requests": restart_requests,
                "failure": failure,
            },
        )
    if failure:
        raise SystemExit(failure)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
