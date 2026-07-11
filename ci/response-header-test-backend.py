#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections.abc import Mapping
from dataclasses import dataclass
import html
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re


MAX_BODY_BYTES = 1024 * 1024
HEADER_NAME_RE = re.compile(r"^[!#$%&'*+\-.^_`|~0-9A-Za-z]+$")
FORBIDDEN_FRAMING_HEADERS = frozenset({"connection", "content-length", "transfer-encoding"})
DEFAULT_HEADERS = (
    ("Content-Type", "text/html; charset=utf-8"),
    ("Content-Security-Policy", "default-src 'none'; sandbox"),
    ("X-Content-Type-Options", "nosniff"),
    ("Last-Modified", "Wed, 21 Oct 2015 07:28:00 GMT"),
    ("Location", "/encoded%2Ftarget"),
    ("Set-Cookie", "session=token"),
    ("Set-Cookie", "a=b"),
)


@dataclass(frozen=True)
class ResponseFixture:
    status: int
    headers: tuple[tuple[str, str], ...]


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


def normalize_status(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 100 <= value <= 599:
        raise ValueError("response status must be an integer between 100 and 599")
    return value


def normalize_header(name: object, value: object) -> tuple[str, str]:
    if not isinstance(name, str) or not HEADER_NAME_RE.fullmatch(name):
        raise ValueError(f"invalid response header name: {name!r}")
    if name.lower() in FORBIDDEN_FRAMING_HEADERS:
        raise ValueError(f"response fixture must not set framing header: {name}")
    if not isinstance(value, str) or "\r" in value or "\n" in value:
        raise ValueError(f"invalid response header value for {name}")
    return name, value


def parse_header_argument(value: str) -> tuple[str, str]:
    if ":" not in value:
        raise argparse.ArgumentTypeError("--header must be NAME:VALUE")
    name, header_value = value.split(":", 1)
    try:
        return normalize_header(name.strip(), header_value.lstrip())
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def fixture_headers(value: object) -> tuple[tuple[str, str], ...]:
    headers: list[tuple[str, str]] = []
    if value is None:
        return ()
    if isinstance(value, Mapping):
        for name, raw_values in value.items():
            values = raw_values if isinstance(raw_values, list) else [raw_values]
            for header_value in values:
                headers.append(normalize_header(name, header_value))
        return tuple(headers)
    if not isinstance(value, list):
        raise ValueError("response fixture headers must be an object or a list of [name, value] pairs")
    for item in value:
        if not isinstance(item, list) or len(item) != 2:
            raise ValueError("response fixture header entries must be [name, value] pairs")
        headers.append(normalize_header(item[0], item[1]))
    return tuple(headers)


def load_fixture_file(path: Path) -> ResponseFixture:
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid response fixture JSON: {path}") from exc
    if not isinstance(loaded, Mapping):
        raise ValueError("response fixture must be a JSON object")
    return ResponseFixture(
        status=normalize_status(loaded.get("status", 200)),
        headers=fixture_headers(loaded.get("headers", [])),
    )


def response_fixture(
    *,
    status: int | None,
    headers: list[tuple[str, str]] | None,
    fixture_file: Path | None,
) -> ResponseFixture:
    configured = load_fixture_file(fixture_file) if fixture_file is not None else ResponseFixture(200, ())
    return ResponseFixture(
        status=configured.status if status is None else status,
        headers=configured.headers + tuple(headers or ()),
    )


class Handler(BaseHTTPRequestHandler):
    body_bytes: bytes
    fixture: ResponseFixture

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
        body = html.escape(self.body_bytes.decode("utf-8", errors="replace")).encode("utf-8")
        self.send_response(self.fixture.status)
        configured_names = {name.lower() for name, _ in self.fixture.headers}
        for name, value in DEFAULT_HEADERS:
            if name.lower() not in configured_names:
                self.send_header(name, value)
        for name, value in self.fixture.headers:
            self.send_header(name, value)
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
    parser.add_argument(
        "--fixture-file",
        type=Path,
        help="JSON response fixture with an upstream status and declarative response headers",
    )
    parser.add_argument("--status", type=int, help="override the fixture upstream HTTP status")
    parser.add_argument(
        "--header",
        action="append",
        type=parse_header_argument,
        default=[],
        help="append a declarative response header as NAME:VALUE",
    )
    args = parser.parse_args()

    try:
        body_file = resolve_body_file(args.body_file, args.safe_root)
        status = None if args.status is None else normalize_status(args.status)
        Handler.fixture = response_fixture(
            status=status,
            headers=args.header,
            fixture_file=args.fixture_file,
        )
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    Handler.body_bytes = body_file.read_bytes()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
