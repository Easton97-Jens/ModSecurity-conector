#!/usr/bin/env python3
from __future__ import annotations

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class Handler(BaseHTTPRequestHandler):
    body_file: Path

    def do_GET(self) -> None:
        self._send_fixture(include_body=True)

    def do_HEAD(self) -> None:
        self._send_fixture(include_body=False)

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length:
            self.rfile.read(length)
        self._send_fixture(include_body=True)

    def _send_fixture(self, *, include_body: bool) -> None:
        body = self.body_file.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Last-Modified", "Wed, 21 Oct 2015 07:28:00 GMT")
        self.send_header("Location", "/encoded%2Ftarget")
        self.send_header("Set-Cookie", "session=token")
        self.send_header("Set-Cookie", "a=b")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if include_body:
            self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--body-file", type=Path, required=True)
    args = parser.parse_args()

    Handler.body_file = args.body_file
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
