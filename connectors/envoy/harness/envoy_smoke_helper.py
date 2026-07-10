#!/usr/bin/env python3
"""Small dependency-free upstream/probe helper for the Envoy connector smoke."""

from __future__ import annotations

import argparse
import http.server
import socket
import sys
import urllib.error
import urllib.request


class UpstreamHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: object) -> None:
        del fmt, args

    def answer(self) -> None:
        content_length = int(self.headers.get("content-length") or "0")
        if content_length > 0:
            self.rfile.read(content_length)
        body = b"envoy connector upstream ok\n"
        self.send_response(200)
        self.send_header("content-type", "text/plain")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

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


def serve_upstream(port: int) -> int:
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), UpstreamHandler)
    try:
        server.serve_forever()
    finally:
        server.server_close()
    return 0


def probe(url: str, header: list[str]) -> int:
    headers: dict[str, str] = {}
    for item in header:
        name, separator, value = item.partition(":")
        if not separator or not name.strip():
            raise ValueError(f"invalid header: {item!r}")
        headers[name.strip()] = value.strip()
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=2) as response:
            response.read()
            status = int(response.status)
    except urllib.error.HTTPError as exc:
        exc.read()
        status = int(exc.code)
    print(status)
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("free-port")
    ports = subparsers.add_parser("free-ports")
    ports.add_argument("--count", required=True, type=int)
    serve = subparsers.add_parser("serve-upstream")
    serve.add_argument("--port", required=True, type=int)
    request = subparsers.add_parser("probe")
    request.add_argument("--url", required=True)
    request.add_argument("--header", action="append", default=[])
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
        return serve_upstream(args.port)
    if args.command == "probe":
        return probe(args.url, args.header)
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as exc:
        print(f"envoy_smoke_helper: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
