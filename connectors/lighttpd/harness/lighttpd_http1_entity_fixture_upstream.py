#!/usr/bin/env python3
"""Serve bounded HTTP/1.1 entity-body fixtures for patched lighttpd.

The daemon sends one Content-Length response and one chunked response.  Each
body contains the canonical Phase-4 marker across separate upstream writes,
but it writes only counts and transport metadata to its control artifacts.
It is deliberately HTTP/1.1-only and does not persist either response body.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import socket
import sys
import time
from typing import Final


CONTENT_LENGTH_PATH: Final = "/p4/fixture/content-length"
CHUNKED_PATH: Final = "/p4/fixture/chunked"

# Keep the marker split across distinct upstream entity writes.  The harness
# checks the patched host's final entity-byte counters, while the core patch
# contract guarantees a borrowed callback before later socket write retries.
CONTENT_LENGTH_PARTS: Final = (
    b"lighttpd-content-length-prefix:",
    b"no-crs-response-",
    b"body-marker",
)
CHUNKED_PARTS: Final = (
    b"lighttpd-chunked-prefix:",
    b"no-crs-response-",
    b"body-marker",
)


class FixtureError(RuntimeError):
    """A bounded fixture exchange could not be completed."""


def write_json(path: Path, value: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def receive_request_path(connection: socket.socket, timeout: float) -> str:
    deadline = time.monotonic() + timeout
    data = bytearray()
    while b"\r\n\r\n" not in data:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise FixtureError("timed out while reading bounded HTTP request headers")
        connection.settimeout(remaining)
        chunk = connection.recv(4096)
        if not chunk:
            raise FixtureError("client closed before HTTP request headers")
        data.extend(chunk)
        if len(data) > 65536:
            raise FixtureError("HTTP request headers exceed the bounded fixture limit")
    request_line = bytes(data).split(b"\r\n", 1)[0].split()
    if len(request_line) != 3:
        raise FixtureError("fixture received an invalid HTTP request line")
    try:
        method = request_line[0].decode("ascii")
        path = request_line[1].decode("ascii")
        version = request_line[2].decode("ascii")
    except UnicodeDecodeError as exc:
        raise FixtureError("fixture request line is not ASCII") from exc
    if method != "GET" or version != "HTTP/1.1" or not path.startswith("/"):
        raise FixtureError("fixture requires an HTTP/1.1 GET request")
    return path.split("?", 1)[0]


def send_parts(
    connection: socket.socket,
    parts: tuple[bytes, ...],
    *,
    chunked: bool,
    delay: float,
) -> None:
    if chunked:
        connection.sendall(
            b"HTTP/1.1 200 OK\r\n"
            b"Content-Type: text/plain\r\n"
            b"Transfer-Encoding: chunked\r\n"
            b"Connection: close\r\n\r\n"
        )
        for index, part in enumerate(parts):
            connection.sendall(f"{len(part):X}\r\n".encode("ascii") + part + b"\r\n")
            if index + 1 < len(parts):
                time.sleep(delay)
        connection.sendall(b"0\r\n\r\n")
        return

    body_size = sum(len(part) for part in parts)
    connection.sendall(
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: text/plain\r\n"
        + f"Content-Length: {body_size}\r\n".encode("ascii")
        + b"Connection: close\r\n\r\n"
    )
    for index, part in enumerate(parts):
        connection.sendall(part)
        if index + 1 < len(parts):
            time.sleep(delay)


def serve(
    *,
    ready_file: Path,
    result_file: Path,
    host: str,
    port: int,
    timeout: float,
    inter_part_delay: float,
) -> None:
    if timeout <= 0 or inter_part_delay <= 0:
        raise FixtureError("timeouts and inter-part delay must be positive")
    if ready_file.exists() or result_file.exists():
        raise FixtureError("fixture control files must be fresh")
    fixtures = {
        CONTENT_LENGTH_PATH: (CONTENT_LENGTH_PARTS, False, "content_length"),
        CHUNKED_PATH: (CHUNKED_PARTS, True, "chunked"),
    }
    served: set[str] = set()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((host, port))
        listener.listen(len(fixtures))
        listener.settimeout(timeout)
        address_host, address_port = listener.getsockname()[:2]
        write_json(
            ready_file,
            {
                "schema_version": 1,
                "evidence_type": "lighttpd_http1_entity_fixture_ready",
                "upstream_host": str(address_host),
                "upstream_port": int(address_port),
                "body_payload_persisted": False,
            },
        )
        while len(served) < len(fixtures):
            try:
                connection, _peer = listener.accept()
            except TimeoutError as exc:
                raise FixtureError("timed out waiting for HTTP/1.1 entity fixture requests") from exc
            with connection:
                path = receive_request_path(connection, timeout)
                fixture = fixtures.get(path)
                if fixture is None or path in served:
                    raise FixtureError("fixture received an unexpected or duplicate request path")
                parts, chunked, label = fixture
                send_parts(
                    connection,
                    parts,
                    chunked=chunked,
                    delay=inter_part_delay,
                )
                served.add(path)
                if label not in {"content_length", "chunked"}:
                    raise FixtureError("fixture label invariant failed")
    write_json(
        result_file,
        {
            "schema_version": 1,
            "evidence_type": "lighttpd_http1_entity_fixture_result",
            "content_length_requests": int(CONTENT_LENGTH_PATH in served),
            "chunked_requests": int(CHUNKED_PATH in served),
            "content_length_entity_bytes": sum(len(part) for part in CONTENT_LENGTH_PARTS),
            "chunked_entity_bytes": sum(len(part) for part in CHUNKED_PARTS),
            "entity_parts_per_response": len(CONTENT_LENGTH_PARTS),
            "body_payload_persisted": False,
        },
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ready-file", required=True, type=Path)
    parser.add_argument("--result-file", required=True, type=Path)
    parser.add_argument("--listen-host", default="127.0.0.1")
    parser.add_argument("--listen-port", type=int, default=0)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--inter-part-delay", type=float, default=0.35)
    args = parser.parse_args(argv)
    try:
        serve(
            ready_file=args.ready_file,
            result_file=args.result_file,
            host=args.listen_host,
            port=args.listen_port,
            timeout=args.timeout,
            inter_part_delay=args.inter_part_delay,
        )
    except (FixtureError, OSError) as exc:
        print(f"lighttpd_http1_entity_fixture: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
