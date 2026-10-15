#!/usr/bin/env python3
"""Waited, bounded loopback client for NGINX I12; EOF is transport only."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import socket
import time

LIMIT = 16 * 1024 * 1024


def sha(data):
    return hashlib.sha256(data).hexdigest()


def entity(raw):
    """Parse retained finite H1 bytes, rejecting ambiguous/incomplete framing."""
    header, body = raw.split(b"\r\n\r\n", 1)
    lines = header.split(b"\r\n")
    start = re.fullmatch(rb"HTTP/1\.[01] ([1-5][0-9]{2})(?: [^\r\n]*)?", lines[0])
    if start is None:
        raise ValueError("invalid HTTP status line")
    status = int(start[1])
    headers = []
    for line in lines[1:]:
        pair = line.split(b":", 1)
        if len(pair) != 2 or re.fullmatch(rb"[!#$%&'*+.^_`|~0-9A-Za-z-]+", pair[0]) is None:
            raise ValueError("invalid response header")
        headers.append(pair)
    raw_lengths = [v.strip(b" \t") for k, v in headers if k.lower() == b"content-length"]
    if any(re.fullmatch(rb"[0-9]+", value) is None for value in raw_lengths):
        raise ValueError("invalid Content-Length digits")
    lengths = [int(value) for value in raw_lengths]
    encodings = [v.strip().lower() for k, v in headers if k.lower() == b"transfer-encoding"]
    if encodings:
        if encodings != [b"chunked"] or lengths:
            raise ValueError("ambiguous transfer framing")
        position, decoded = 0, bytearray()
        while True:
            end = body.find(b"\r\n", position)
            if end < 0:
                raise ValueError("incomplete chunk size")
            size_text = body[position:end]
            if not size_text or any(c not in b"0123456789abcdefABCDEF" for c in size_text):
                raise ValueError("invalid chunk size")
            size = int(size_text, 16)
            position = end + 2
            if size == 0:
                if body[position:] != b"\r\n":
                    raise ValueError("incomplete terminal chunk or unsupported trailers")
                return status, header + b"\r\n\r\n", bytes(decoded), "http1.1-chunked"
            if position + size + 2 > len(body) or body[position + size:position + size + 2] != b"\r\n":
                raise ValueError("incomplete chunk data")
            decoded.extend(body[position:position + size])
            position += size + 2
    if len(lengths) != 1 or lengths[0] != len(body):
        raise ValueError("finite Content-Length mismatch")
    return status, header + b"\r\n\r\n", body, "http1.1-content-length"


def run(port, request_path, output, pieces=1):
    if not 1 <= pieces <= 64 or not 1024 < port < 65536:
        raise ValueError("closed loopback port/write-count contract")
    request = request_path.read_bytes()
    if not 0 < len(request) <= LIMIT:
        raise ValueError("request size outside bound")
    output.mkdir(mode=0o700)
    observed = {"request_sha256": sha(request), "first_response_monotonic_ns": None,
                "first_entity_monotonic_ns": None, "status": None, "writes": [],
                "framing_complete": False, "socket_eof": False, "socket_reset": False,
                "pid": os.getpid(), "uid": os.getuid()}
    wire = bytearray()
    error = None
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=5) as stream:
            observed.update(local=stream.getsockname(), peer=stream.getpeername())
            head, body = request.split(b"\r\n\r\n", 1)
            segments = [request] if pieces == 1 else [head + b"\r\n\r\n"] + [
                body[i * len(body) // pieces:(i + 1) * len(body) // pieces] for i in range(pieces)]
            for segment in segments:
                started = time.monotonic_ns()
                stream.sendall(segment)
                observed["writes"].append({"bytes": len(segment), "started_monotonic_ns": started,
                                           "returned_monotonic_ns": time.monotonic_ns()})
                if pieces > 1:
                    time.sleep(0.025)
            deadline = time.monotonic() + 10
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError("bounded client response deadline")
                stream.settimeout(remaining)
                chunk = stream.recv(65536)
                if not chunk:
                    observed.update(socket_eof=True, socket_eof_monotonic_ns=time.monotonic_ns())
                    break
                now = time.monotonic_ns()
                if observed["first_response_monotonic_ns"] is None:
                    observed["first_response_monotonic_ns"] = now
                wire.extend(chunk)
                if b"\r\n\r\n" in wire and len(wire.split(b"\r\n\r\n", 1)[1]) and observed["first_entity_monotonic_ns"] is None:
                    observed["first_entity_monotonic_ns"] = now
                if len(wire) > LIMIT:
                    raise ValueError("bounded response exceeded")
        status, headers, body, framing = entity(bytes(wire))
        (output / "headers.bin").write_bytes(headers)
        (output / "body.bin").write_bytes(body)
        observed.update(status=status, body_bytes=len(body), body_sha256=sha(body), framing=framing,
                        framing_complete=True)
    except (OSError, ValueError, TimeoutError) as exc:
        error = type(exc).__name__ + ": " + str(exc)
        observed["socket_reset"] = isinstance(exc, ConnectionResetError)
        if b"\r\n\r\n" in wire:
            head, fragment = bytes(wire).split(b"\r\n\r\n", 1)
            (output / "headers.bin").write_bytes(head + b"\r\n\r\n")
            (output / "body-fragment.bin").write_bytes(fragment)
            start = re.fullmatch(rb"HTTP/1\.[01] ([1-5][0-9]{2})(?: [^\r\n]*)?", head.split(b"\r\n", 1)[0])
            observed["status"] = int(start[1]) if start else None
            observed["fragment_bytes"] = len(fragment)
            observed["fragment_sha256"] = sha(fragment)
    finally:
        (output / "response.bin").write_bytes(wire)
        observed.update(response_sha256=sha(wire), error=error, finished_monotonic_ns=time.monotonic_ns())
        (output / "client-observation.json").write_text(json.dumps(observed, indent=2) + "\n")
    return 0 if error is None else 2


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--pieces", type=int, default=1)
    args = parser.parse_args()
    return run(args.port, args.request, args.output, args.pieces)


if __name__ == "__main__":
    raise SystemExit(main())
