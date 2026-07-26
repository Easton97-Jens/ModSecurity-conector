#!/usr/bin/env python3
"""Bounded request-body regressions against a running Parent Apache harness."""

from __future__ import annotations

import argparse
import http.client
import json
import socket
from dataclasses import asdict, dataclass
from urllib.parse import urlsplit


ALLOW = b"apache-body-allow-token"
BLOCK = b"apache-body-block-token"


@dataclass(frozen=True)
class Result:
    name: str
    expected: int
    observed: int

    @property
    def passed(self) -> bool:
        return self.expected == self.observed


def chunked_request(host: str, port: int, path: str, chunks: list[bytes]) -> int:
    """Send chunks as distinct writes so the input filter sees fragmentation."""
    with socket.create_connection((host, port), timeout=10) as stream:
        stream.sendall(
            f"POST {path} HTTP/1.1\r\nHost: {host}\r\n"
            "Transfer-Encoding: chunked\r\nConnection: close\r\n\r\n".encode("ascii")
        )
        for chunk in chunks:
            stream.sendall(f"{len(chunk):x}\r\n".encode("ascii"))
            stream.sendall(chunk)
            stream.sendall(b"\r\n")
        stream.sendall(b"0\r\n\r\n")
        response = http.client.HTTPResponse(stream)
        response.begin()
        response.read()
        return response.status


def post(host: str, port: int, path: str, body: bytes) -> int:
    connection = http.client.HTTPConnection(host, port, timeout=10)
    try:
        connection.request("POST", path, body=body, headers={"Content-Type": "text/plain"})
        response = connection.getresponse()
        response.read()
        return response.status
    finally:
        connection.close()


def run(base_url: str, repetitions: int) -> list[Result]:
    parsed = urlsplit(base_url)
    if parsed.scheme != "http" or not parsed.hostname:
        raise ValueError("--base-url must be an http URL")
    host, port = parsed.hostname, parsed.port or 80
    path = parsed.path or "/"
    cases = [
        Result("small_allow", 200, post(host, port, path, ALLOW)),
        Result("body_block", 403, post(host, port, path, BLOCK)),
        Result("large_allow", 200, post(host, port, path, b"a" * 262144 + ALLOW)),
        Result("empty", 200, post(host, port, path, b"")),
        Result(
            "multi_bucket_block",
            403,
            chunked_request(host, port, path, [b"prefix-", BLOCK[:11], BLOCK[11:]]),
        ),
    ]
    for index in range(repetitions):
        token = ALLOW if index % 2 == 0 else BLOCK
        expected = 200 if index % 2 == 0 else 403
        cases.append(Result(f"repeat_{index}", expected, post(host, port, path, token)))
    return cases


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--repetitions", type=int, default=4)
    parser.add_argument("--output")
    args = parser.parse_args()
    if not 0 <= args.repetitions <= 100:
        parser.error("--repetitions must be between 0 and 100")
    results = run(args.base_url, args.repetitions)
    payload = {"status": "PASS" if all(r.passed for r in results) else "FAIL",
               "results": [{**asdict(r), "passed": r.passed} for r in results]}
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as output:
            output.write(rendered)
    print(rendered, end="")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
