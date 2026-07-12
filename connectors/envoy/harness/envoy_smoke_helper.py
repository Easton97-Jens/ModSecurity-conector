#!/usr/bin/env python3
"""Small dependency-free upstream/probe helper for the Envoy connector smoke."""

from __future__ import annotations

import argparse
import http.server
import json
import socket
import sys
import time
import urllib.error
import urllib.request


class UpstreamHandler(http.server.BaseHTTPRequestHandler):
    client_cancel_delay_seconds = 5.0

    def log_message(self, fmt: str, *args: object) -> None:
        del fmt, args

    def answer(self) -> None:
        content_length = int(self.headers.get("content-length") or "0")
        if content_length > 0:
            self.rfile.read(content_length)
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


def serve_upstream(port: int, client_cancel_delay: float) -> int:
    if client_cancel_delay <= 0 or client_cancel_delay > 30:
        raise ValueError("client cancel delay must be greater than zero and at most 30 seconds")

    class DelayedUpstreamHandler(UpstreamHandler):
        client_cancel_delay_seconds = client_cancel_delay

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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("free-port")
    ports = subparsers.add_parser("free-ports")
    ports.add_argument("--count", required=True, type=int)
    serve = subparsers.add_parser("serve-upstream")
    serve.add_argument("--port", required=True, type=int)
    serve.add_argument("--client-cancel-delay", default=5.0, type=float)
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
        return serve_upstream(args.port, args.client_cancel_delay)
    if args.command == "probe":
        return probe(args.url, args.header, args.method, args.data, args.no_redirect)
    if args.command == "client-cancel":
        print(json.dumps(client_cancel(args.host, args.port, args.path, args.header), sort_keys=True))
        return 0
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as exc:
        print(f"envoy_smoke_helper: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
