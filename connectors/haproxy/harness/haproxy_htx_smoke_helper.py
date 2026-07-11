#!/usr/bin/env python3
"""Small local-only helper for the non-promoted HAProxy HTX runtime smoke."""

from __future__ import annotations

import argparse
import http.server
import json
from pathlib import Path
import socket
import sys
import urllib.error
import urllib.request


RESPONSE_HEADER_VALUE = "htx-response-header-marker"
RESPONSE_BODY = b"haproxy-htx-response-body-marker\n"


class UpstreamHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: object) -> None:
        del fmt, args

    def answer(self) -> None:
        content_length = int(self.headers.get("content-length") or "0")
        if content_length > 0:
            self.rfile.read(content_length)
        self.send_response(200)
        self.send_header("content-type", "text/plain")
        self.send_header("x-htx-response", RESPONSE_HEADER_VALUE)
        self.send_header("content-length", str(len(RESPONSE_BODY)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(RESPONSE_BODY)

    do_GET = answer
    do_HEAD = answer
    do_POST = answer


def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def wait_port(port: int) -> int:
    with socket.create_connection(("127.0.0.1", port), timeout=0.5):
        pass
    return 0


def serve_upstream(port: int) -> int:
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), UpstreamHandler)
    try:
        server.serve_forever()
    finally:
        server.server_close()
    return 0


def probe(url: str, header: list[str], method: str, data: str | None) -> int:
    headers: dict[str, str] = {}
    for item in header:
        name, separator, value = item.partition(":")
        if not separator or not name.strip():
            raise ValueError(f"invalid header: {item!r}")
        headers[name.strip()] = value.strip()
    request_body = None if data is None else data.encode("utf-8")
    request = urllib.request.Request(url, data=request_body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=2) as response:
            response.read()
            status = int(response.status)
    except urllib.error.HTTPError as exc:
        exc.read()
        status = int(exc.code)
    print(status)
    return 0


def checked_path(raw_path: str) -> Path:
    path = Path(raw_path)
    if not path.is_absolute():
        raise ValueError(f"path must be absolute: {path}")
    return path


def write_rules(path: str, case: str) -> int:
    rules_by_case = {
        "phase1": (
            "SecRuleEngine On\n"
            "SecAuditEngine Off\n"
            "SecRule REQUEST_HEADERS:X-Modsec-Htx \"@streq htx-phase1-marker\" "
            "\"id:910001,phase:1,deny,status:403,log\"\n"
        ),
        "phase2": (
            "SecRuleEngine On\n"
            "SecAuditEngine Off\n"
            "SecRequestBodyAccess On\n"
            "SecRule REQUEST_BODY \"@contains htx-request-body-marker\" "
            "\"id:910002,phase:2,deny,status:403,log\"\n"
        ),
        "phase3": (
            "SecRuleEngine On\n"
            "SecAuditEngine Off\n"
            "SecResponseBodyAccess On\n"
            "SecRule RESPONSE_HEADERS:X-Htx-Response \"@streq htx-response-header-marker\" "
            "\"id:910003,phase:3,deny,status:403,log\"\n"
        ),
        "phase4": (
            "SecRuleEngine On\n"
            "SecAuditEngine Off\n"
            "SecResponseBodyAccess On\n"
            "SecResponseBodyMimeType text/plain\n"
            "SecRule RESPONSE_BODY \"@contains htx-response-body-marker\" "
            "\"id:910004,phase:4,deny,status:403,log\"\n"
        ),
    }
    try:
        content = rules_by_case[case]
    except KeyError as exc:
        raise ValueError(f"unknown rule case: {case}") from exc
    target = checked_path(path)
    target.parent.mkdir(mode=0o750, parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    target.chmod(0o600)
    return 0


def config_value(value: str, name: str) -> str:
    if not value or "\n" in value or "\r" in value:
        raise ValueError(f"invalid {name}")
    return value


def write_config(path: str, listen_port: int, upstream_port: int, rules_file: str) -> int:
    target = checked_path(path)
    rules = config_value(str(checked_path(rules_file)), "rules file")
    if not 1 <= listen_port <= 65535 or not 1 <= upstream_port <= 65535:
        raise ValueError("port out of range")
    content = f"""global
    log stdout format raw local0

defaults
    mode http
    timeout connect 2s
    timeout client 5s
    timeout server 5s

frontend htx_in
    bind 127.0.0.1:{listen_port}
    filter modsecurity-htx rules-file {rules} phase4-mode safe
    default_backend htx_upstream

backend htx_upstream
    server upstream 127.0.0.1:{upstream_port}
"""
    target.parent.mkdir(mode=0o750, parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    target.chmod(0o600)
    return 0


def write_event(
    path: str,
    case: str,
    transaction_id: str,
    phase: int,
    rule_id: int,
    observed_status: int,
    host_action: str,
) -> int:
    target = checked_path(path)
    if (
        not transaction_id
        or len(transaction_id) > 127
        or any(not (character.isascii() and (character.isalnum() or character in "._-")) for character in transaction_id)
    ):
        raise ValueError("invalid transaction id")
    if host_action not in {"not_enforced", "not_attempted"}:
        raise ValueError("invalid host action")
    record = {
        "event": "htx_observed_intervention",
        "integration_mode": "native_htx_filter",
        "evaluation_mode": "observer_nonpromoted",
        "rule_evaluation": "libmodsecurity_observed",
        "transaction_id": transaction_id,
        "case": case,
        "phase": phase,
        "rule_id": rule_id,
        "requested_action": "deny",
        "host_action": host_action,
        "observed_client_status": observed_status,
        "payload_recorded": False,
    }
    target.parent.mkdir(mode=0o750, parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as output:
        output.write(json.dumps(record, separators=(",", ":")) + "\n")
    target.chmod(0o600)
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("free-port")
    wait = subparsers.add_parser("wait-port")
    wait.add_argument("--port", required=True, type=int)
    serve = subparsers.add_parser("serve-upstream")
    serve.add_argument("--port", required=True, type=int)
    request = subparsers.add_parser("probe")
    request.add_argument("--url", required=True)
    request.add_argument("--header", action="append", default=[])
    request.add_argument("--method", default="GET")
    request.add_argument("--data")
    rules = subparsers.add_parser("write-rules")
    rules.add_argument("--path", required=True)
    rules.add_argument("--case", required=True, choices=("phase1", "phase2", "phase3", "phase4"))
    config = subparsers.add_parser("write-config")
    config.add_argument("--path", required=True)
    config.add_argument("--listen-port", required=True, type=int)
    config.add_argument("--upstream-port", required=True, type=int)
    config.add_argument("--rules-file", required=True)
    event = subparsers.add_parser("write-event")
    event.add_argument("--path", required=True)
    event.add_argument("--case", required=True)
    event.add_argument("--transaction-id", required=True)
    event.add_argument("--phase", required=True, type=int)
    event.add_argument("--rule-id", required=True, type=int)
    event.add_argument("--observed-status", required=True, type=int)
    event.add_argument("--host-action", required=True, choices=("not_enforced", "not_attempted"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.command == "free-port":
        print(free_port())
        return 0
    if args.command == "wait-port":
        return wait_port(args.port)
    if args.command == "serve-upstream":
        return serve_upstream(args.port)
    if args.command == "probe":
        return probe(args.url, args.header, args.method, args.data)
    if args.command == "write-rules":
        return write_rules(args.path, args.case)
    if args.command == "write-config":
        return write_config(args.path, args.listen_port, args.upstream_port, args.rules_file)
    if args.command == "write-event":
        return write_event(
            args.path,
            args.case,
            args.transaction_id,
            args.phase,
            args.rule_id,
            args.observed_status,
            args.host_action,
        )
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as exc:
        print(f"haproxy_htx_smoke_helper: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
