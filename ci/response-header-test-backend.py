#!/usr/bin/env python3
from __future__ import annotations

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


MAX_BODY_BYTES = 1024 * 1024


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def resolve_body_file(path: Path, safe_roots: list[Path]) -> Path:
    resolved = path.resolve(strict=True)
    roots = [root.resolve(strict=True) for root in safe_roots] if safe_roots else [Path.cwd().resolve(strict=True)]
    if not resolved.is_file():
        raise ValueError(f"body file is not a regular file: {path}")
    if not any(_is_relative_to(resolved, root) for root in roots):
        raise ValueError(f"body file is outside the allowed fixture roots: {path}")
    if resolved.stat().st_size > MAX_BODY_BYTES:
        raise ValueError(f"body file is too large: {path}")
    return resolved


class Handler(BaseHTTPRequestHandler):
    body_bytes: bytes

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
        body = self.body_bytes
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Security-Policy", "default-src 'none'; sandbox")
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
    parser.add_argument("--safe-root", type=Path, action="append", default=[])
    args = parser.parse_args()

    body_file = resolve_body_file(args.body_file, args.safe_root)
    Handler.body_bytes = body_file.read_bytes()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
