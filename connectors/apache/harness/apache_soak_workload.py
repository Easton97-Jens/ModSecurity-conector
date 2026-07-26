#!/usr/bin/env python3
"""Bounded, payload-free traffic helper owned by the Parent Apache harness.

This helper never starts, stops, or configures Apache.  The calling harness
already owns that lifecycle; it supplies one live launch PID only so this
helper can request and verify bounded graceful-restart attempts while its
fixed loopback traffic remains active.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass, field
import http.client
import json
import os
from pathlib import Path
import signal
import socket
import stat
import tempfile
import threading
import time
from typing import Any


RESPONSE_BOUND = 65536
REQUEST_PATH = "/__request_body_consume"
ALLOW_PAYLOAD = b"request-body-allow-marker"
DENY_PAYLOAD = b"request-body-block-marker"
LARGE_PAYLOAD = b"request-body-large-prefix-" + (b"a" * 1048577)
SOURCE_CHECKOUT = Path(__file__).resolve().parents[3]
REQUEST_SHAPES = (
    ("allow", ALLOW_PAYLOAD, 200),
    ("deny", DENY_PAYLOAD, 403),
    ("body", ALLOW_PAYLOAD, 200),
    ("large_body", LARGE_PAYLOAD, 200),
    ("multi_bucket", None, 403),
)


class ResultPathError(ValueError):
    """Raised when the soak result cannot be written safely."""


@dataclass
class SoakOutcome:
    counters: Counter[str] = field(default_factory=Counter)
    restart_requests: int = 0
    restart_count: int = 0
    failure: str = ""


def bounded_text(value: object, limit: int = 512) -> str:
    return str(value or "").replace("\r", " ").replace("\n", " ").strip()[:limit]


def validate_absolute_path(path: Path, label: str) -> None:
    if not path.is_absolute():
        raise ResultPathError(f"{label} must be absolute: {path}")
    if ".." in path.parts:
        raise ResultPathError(f"{label} must not contain traversal: {path}")


def path_components(path: Path) -> list[Path]:
    current = Path(path.anchor)
    components: list[Path] = []
    for name in path.parts[1:]:
        current /= name
        components.append(current)
    return components


def reject_symlink_components(path: Path, label: str, *, require_existing: bool) -> None:
    for component in path_components(path):
        try:
            metadata = component.lstat()
        except FileNotFoundError:
            if require_existing:
                raise ResultPathError(f"{label} must exist: {component}") from None
            return
        except OSError as exc:
            raise ResultPathError(f"{label} cannot inspect path component: {component}") from exc
        if stat.S_ISLNK(metadata.st_mode):
            raise ResultPathError(f"{label} must not contain a symlink: {component}")


def canonical_real_directory(path: Path, label: str) -> Path:
    validate_absolute_path(path, label)
    reject_symlink_components(path, label, require_existing=True)
    try:
        metadata = path.lstat()
    except OSError as exc:
        raise ResultPathError(f"{label} cannot inspect directory: {path}") from exc
    if not stat.S_ISDIR(metadata.st_mode):
        raise ResultPathError(f"{label} must be an existing real directory: {path}")
    try:
        return path.resolve(strict=True)
    except OSError as exc:
        raise ResultPathError(f"{label} cannot be resolved: {path}") from exc


def require_missing_or_regular_file(path: Path, label: str) -> None:
    try:
        metadata = path.lstat()
    except FileNotFoundError:
        return
    except OSError as exc:
        raise ResultPathError(f"{label} cannot inspect final target: {path}") from exc
    if stat.S_ISLNK(metadata.st_mode):
        raise ResultPathError(f"{label} must not be a symlink: {path}")
    if not stat.S_ISREG(metadata.st_mode):
        raise ResultPathError(f"{label} must be a regular file when it exists: {path}")


def require_outside_source_checkout(run_root: Path) -> None:
    try:
        run_root.relative_to(SOURCE_CHECKOUT)
    except ValueError:
        return
    raise ResultPathError(f"--run-root must be outside the source checkout: {run_root}")


def validate_result_path(run_root: Path, result: Path) -> Path:
    """Validate a direct, pre-existing-root result destination before writes."""

    # Keep caller-controlled result checks ahead of every path inspection. No
    # parent creation or output write is permitted before this validator wins.
    validate_absolute_path(result, "--result")
    validate_absolute_path(run_root, "--run-root")
    canonical_root = canonical_real_directory(run_root, "--run-root")
    reject_symlink_components(result, "--result", require_existing=False)
    if result.parent != canonical_root:
        raise ResultPathError(
            f"--result must be a direct child of --run-root: {result}"
        )
    require_outside_source_checkout(canonical_root)
    validated_result = canonical_root / result.name
    require_missing_or_regular_file(validated_result, "--result")
    return validated_result


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    validate_absolute_path(path, "result path")
    reject_symlink_components(path, "result path", require_existing=False)
    try:
        parent_metadata = path.parent.lstat()
    except FileNotFoundError:
        raise ValueError(f"result parent does not exist: {path.parent}") from None
    except OSError as exc:
        raise ValueError(f"cannot inspect result parent: {path.parent}") from exc
    if not stat.S_ISDIR(parent_metadata.st_mode) or stat.S_ISLNK(parent_metadata.st_mode):
        raise ValueError(f"result parent must be an existing real directory: {path.parent}")
    require_missing_or_regular_file(path, "result path")
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


def require_range(value: int, minimum: int, maximum: int, label: str) -> None:
    if not minimum <= value <= maximum:
        raise SystemExit(f"{label} must be between {minimum} and {maximum}")


def validate_soak_arguments(args: argparse.Namespace) -> None:
    require_range(args.port, 1, 65535, "port")
    require_range(args.duration_seconds, 1, 3600, "duration")
    require_range(args.concurrency, 1, 16, "concurrency")
    require_range(args.request_timeout_seconds, 1, 120, "request timeout")
    require_range(args.restart_interval_seconds, 1, 3600, "restart interval")


class SoakRun:
    """Keep traffic, restart, and worker shutdown concerns independently bounded."""

    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args
        self.counters: Counter[str] = Counter()
        self.errors: list[str] = []
        self.counter_lock = threading.Lock()
        self.stop_workers = threading.Event()
        self.restart_requests = 0
        self.restart_count = 0
        self.workers: list[threading.Thread] = []

    def record(self, name: str) -> None:
        with self.counter_lock:
            self.counters[name] += 1

    def worker(self, worker_index: int, deadline: float) -> None:
        index = worker_index
        while not self.stop_workers.is_set() and time.monotonic() < deadline:
            name, payload, expected = REQUEST_SHAPES[index % len(REQUEST_SHAPES)]
            try:
                request_once(
                    self.args.port,
                    self.args.request_timeout_seconds,
                    name,
                    payload,
                    expected,
                )
                self.record(name)
            except (OSError, http.client.HTTPException, RuntimeError) as exc:
                with self.counter_lock:
                    self.errors.append(bounded_text(exc, 256))
                self.stop_workers.set()
                return
            index += 1

    def warm_up(self) -> None:
        for name, payload, expected in REQUEST_SHAPES:
            request_once(
                self.args.port,
                self.args.request_timeout_seconds,
                name,
                payload,
                expected,
            )
            self.record(name)

    def start_workers(self, deadline: float) -> None:
        self.workers = [
            threading.Thread(target=self.worker, args=(index, deadline), daemon=False)
            for index in range(self.args.concurrency)
        ]
        for worker in self.workers:
            worker.start()

    def request_restart(self) -> None:
        os.kill(self.args.launch_pid, signal.SIGUSR1)
        self.restart_requests += 1
        wait_ready(self.args.port, self.args.request_timeout_seconds)
        self.restart_count += 1

    def run_restarts(self, deadline: float) -> None:
        next_restart = time.monotonic()
        while time.monotonic() < deadline and not self.stop_workers.is_set():
            if time.monotonic() >= next_restart:
                self.request_restart()
                next_restart = time.monotonic() + self.args.restart_interval_seconds
            time.sleep(0.02)

    def raise_worker_error(self) -> None:
        with self.counter_lock:
            if self.errors:
                raise RuntimeError(f"Apache soak request failure: {self.errors[0]}")

    def require_restart(self) -> None:
        if self.restart_count == 0:
            raise RuntimeError("Apache soak did not complete a requested graceful restart")

    def stop_and_join(self) -> str:
        self.stop_workers.set()
        failure = ""
        for worker in self.workers:
            worker.join(timeout=self.args.request_timeout_seconds + 1)
            if worker.is_alive() and not failure:
                failure = "Apache soak worker did not stop within the request timeout"
        return failure

    def run(self) -> None:
        self.warm_up()
        deadline = time.monotonic() + self.args.duration_seconds
        self.start_workers(deadline)
        self.run_restarts(deadline)
        shutdown_failure = self.stop_and_join()
        if shutdown_failure:
            raise RuntimeError(shutdown_failure)
        self.raise_worker_error()
        self.require_restart()


def run_soak(args: argparse.Namespace) -> SoakOutcome:
    soak_run = SoakRun(args)
    failure = ""
    try:
        soak_run.run()
    except (OSError, RuntimeError) as exc:
        failure = bounded_text(exc)
    finally:
        shutdown_failure = soak_run.stop_and_join()
    if not failure:
        failure = shutdown_failure
    return SoakOutcome(
        counters=soak_run.counters,
        restart_requests=soak_run.restart_requests,
        restart_count=soak_run.restart_count,
        failure=failure,
    )


def result_payload(args: argparse.Namespace, outcome: SoakOutcome) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "metadata": {
            "httpd_version": bounded_text(args.httpd_version),
            "apxs_version": bounded_text(args.apxs_version),
            "libmodsecurity_version": "unavailable (shared-object version metadata is not exposed by the Parent harness)",
            "compiler": bounded_text(args.compiler),
            "mpm": bounded_text(args.mpm),
            "libmodsecurity_path": bounded_text(args.libmodsecurity_path),
        },
        "status": "PASS" if not outcome.failure else "FAIL",
        "instrumented_httpd_launch_pid": args.launch_pid,
        "real_httpd_pid": real_httpd_child(args.launch_pid),
        "requests": {
            name: int(outcome.counters.get(name, 0))
            for name, _, _ in REQUEST_SHAPES
        },
        "restart_count": outcome.restart_count,
        "restart_requests": outcome.restart_requests,
        "failure": outcome.failure,
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--port", type=int, required=True)
    result.add_argument("--launch-pid", type=int, required=True)
    result.add_argument("--duration-seconds", type=int, required=True)
    result.add_argument("--concurrency", type=int, required=True)
    result.add_argument("--request-timeout-seconds", type=int, required=True)
    result.add_argument("--restart-interval-seconds", type=int, required=True)
    result.add_argument("--run-root", type=Path, required=True)
    result.add_argument("--result", type=Path, required=True)
    result.add_argument("--httpd-version", required=True)
    result.add_argument("--apxs-version", required=True)
    result.add_argument("--compiler", required=True)
    result.add_argument("--mpm", required=True)
    result.add_argument("--libmodsecurity-path", required=True)
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        result_path = validate_result_path(args.run_root, args.result)
    except ResultPathError as exc:
        raise SystemExit(str(exc)) from exc
    validate_soak_arguments(args)
    outcome = run_soak(args)
    atomic_json(result_path, result_payload(args, outcome))
    if outcome.failure:
        raise SystemExit(outcome.failure)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
