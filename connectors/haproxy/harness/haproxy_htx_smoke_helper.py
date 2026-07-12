#!/usr/bin/env python3
"""Local-only helpers for real HAProxy HTX host-runtime evidence.

The helper deliberately retains only bounded metadata from the local client,
upstream, and HAProxy process.  It never persists request/response payloads.
"""

from __future__ import annotations

import argparse
import http.server
import json
from pathlib import Path
import re
import socket
import sys
import threading
import urllib.error
import urllib.request


REPO_ROOT = Path(__file__).resolve().parents[3]
CANONICAL_RULES_PATH = (
    REPO_ROOT / "modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf"
)
CANONICAL_RULE_SNIPPETS = (
    "id:1100001,phase:1,deny,status:403",
    "id:1100002,phase:1,deny,status:429",
    "id:1100101,phase:2,deny,status:403",
    "id:1100201,phase:3,deny,status:403",
    "id:1100301,phase:4,deny,status:403",
)
UPSTREAM_OK_BODY = b"haproxy-htx-upstream-ok\n"
UPSTREAM_PHASE4_BODY = b"no-crs-response-body-marker\n"
DECISION_PATTERN = re.compile(
    r"transaction_id=(?P<transaction_id>[A-Za-z0-9._-]+) "
    r"phase=(?P<phase>[0-9]+) status=(?P<status>[0-9]+) "
    r"rule_id=(?P<rule_id>[0-9]+) "
    r"(?:action|requested_action)=(?P<action>[A-Za-z_]+)"
)


def checked_path(raw_path: str) -> Path:
    path = Path(raw_path)
    if not path.is_absolute():
        raise ValueError(f"path must be absolute: {path}")
    return path


def append_jsonl(path: Path, record: dict[str, object]) -> None:
    path.parent.mkdir(mode=0o750, parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as output:
        output.write(json.dumps(record, separators=(",", ":"), sort_keys=True) + "\n")
    path.chmod(0o600)


def write_json(path: Path, record: dict[str, object]) -> None:
    path.parent.mkdir(mode=0o750, parents=True, exist_ok=True)
    path.write_text(json.dumps(record, separators=(",", ":"), sort_keys=True) + "\n", encoding="utf-8")
    path.chmod(0o600)


def upstream_profile(raw_path: str) -> tuple[str, str | None, bytes]:
    path = raw_path.split("?", 1)[0]
    if path == "/no-crs/response-header":
        return "phase3", "block", UPSTREAM_OK_BODY
    if path == "/no-crs/response-body":
        return "phase4", None, UPSTREAM_PHASE4_BODY
    return "ordinary", None, UPSTREAM_OK_BODY


class UpstreamHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: object) -> None:
        del fmt, args

    def answer(self) -> None:
        try:
            content_length = int(self.headers.get("content-length") or "0")
        except ValueError:
            content_length = 0
        if content_length > 0:
            self.rfile.read(content_length)
        profile, response_header, response_body = upstream_profile(self.path)
        request_log = getattr(self.server, "request_log", None)
        request_log_lock = getattr(self.server, "request_log_lock", None)
        if isinstance(request_log, Path) and request_log_lock is not None:
            with request_log_lock:
                append_jsonl(request_log, {
                    "method": self.command,
                    "response_status": 200,
                    "profile": profile,
                })
        self.send_response(200)
        self.send_header("content-type", "text/plain")
        if response_header is not None:
            self.send_header("x-modsec-upstream", response_header)
        self.send_header("content-length", str(len(response_body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(response_body)

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


def serve_upstream(port: int, request_log: str | None = None) -> int:
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), UpstreamHandler)
    server.request_log = checked_path(request_log) if request_log else None
    server.request_log_lock = threading.Lock()
    try:
        server.serve_forever()
    finally:
        server.server_close()
    return 0


def probe(
    url: str, header: list[str], method: str, data: str | None,
    evidence_path: str | None = None,
) -> int:
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
            response_body = response.read()
            status = int(response.status)
            content_type = str(response.headers.get("content-type") or "")[:256]
    except urllib.error.HTTPError as exc:
        response_body = exc.read()
        status = int(exc.code)
        content_type = str(exc.headers.get("content-type") or "")[:256]
    if evidence_path:
        write_json(checked_path(evidence_path), {
            "status": status,
            "response_bytes": len(response_body),
            "content_type": content_type,
        })
    print(status)
    return 0


def canonical_rules_content(canonical_rules: str | None = None) -> str:
    source = checked_path(canonical_rules) if canonical_rules else CANONICAL_RULES_PATH
    if not source.is_file():
        raise ValueError(f"canonical No-CRS rules are missing: {source}")
    content = source.read_text(encoding="utf-8")
    missing = [snippet for snippet in CANONICAL_RULE_SNIPPETS if snippet not in content]
    if missing:
        raise ValueError(f"canonical No-CRS rules are incomplete: {', '.join(missing)}")
    if "id:91000" in content:
        raise ValueError("canonical No-CRS rules must not use temporary 91000x IDs")
    return content


def write_rules(path: str, canonical_rules: str | None = None) -> int:
    target = checked_path(path)
    target.parent.mkdir(mode=0o750, parents=True, exist_ok=True)
    target.write_text(canonical_rules_content(canonical_rules), encoding="utf-8")
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


def read_probe(path: str) -> dict[str, object]:
    target = checked_path(path)
    try:
        value = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid probe evidence: {target}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"probe evidence is not an object: {target}")
    status = value.get("status")
    response_bytes = value.get("response_bytes")
    content_type = value.get("content_type")
    if isinstance(status, bool) or not isinstance(status, int) or not 100 <= status <= 599:
        raise ValueError(f"invalid probe status: {target}")
    if isinstance(response_bytes, bool) or not isinstance(response_bytes, int) or response_bytes < 0:
        raise ValueError(f"invalid probe response size: {target}")
    if not isinstance(content_type, str) or len(content_type) > 256:
        raise ValueError(f"invalid probe content type: {target}")
    return value


def upstream_count(path: str, profile: str) -> int:
    target = checked_path(path)
    if not target.exists():
        return 0
    count = 0
    for line in target.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid upstream evidence: {target}") from exc
        if isinstance(record, dict) and record.get("profile") == profile:
            count += 1
    return count


def decision_from_log(path: str, phase: int, rule_id: int) -> dict[str, object]:
    target = checked_path(path)
    if not target.is_file():
        raise ValueError(f"HAProxy host log is missing: {target}")
    matches: list[dict[str, object]] = []
    for line in target.read_text(encoding="utf-8", errors="replace").splitlines():
        match = DECISION_PATTERN.search(line)
        if not match:
            continue
        result = {
            "transaction_id": match.group("transaction_id"),
            "phase": int(match.group("phase")),
            "status": int(match.group("status")),
            "rule_id": int(match.group("rule_id")),
            "action": match.group("action").lower(),
        }
        if result["phase"] == phase and result["rule_id"] == rule_id:
            matches.append(result)
    if not matches:
        raise ValueError(f"HAProxy host log lacks phase {phase} rule {rule_id}: {target}")
    return matches[-1]


def write_event(
    path: str, case: str, decision_log: str, phase: int, rule_id: int,
    observed_status: int, host_action: str, original_http_status: int | None = None,
) -> int:
    if host_action != "enforced_reply":
        raise ValueError("canonical event output is reserved for an enforced host reply")
    decision = decision_from_log(decision_log, phase, rule_id)
    if decision["action"] != "deny" or decision["status"] != observed_status:
        raise ValueError("host decision does not match the client-visible enforced reply")
    if original_http_status is not None and not 100 <= original_http_status <= 599:
        raise ValueError("invalid original upstream status")
    record: dict[str, object] = {
        # This is a harness projection of the HAProxy host log and client
        # response, not a Common-runtime event or a capability promotion.
        "connector": "haproxy",
        "event": "native_htx_host_intervention",
        "message_id": "HAPROXY_HTX_NATIVE_PRECOMMIT_DENY",
        "integration_mode": "native-htx-filter",
        "evaluation_mode": "native_host_runtime_nonpromoted",
        "rule_evaluation": "libmodsecurity_host_runtime",
        "transaction_id": decision["transaction_id"],
        "case": case,
        "phase": phase,
        "rule_id": rule_id,
        "status": "blocked",
        "requested_action": "deny",
        "actual_action": "deny",
        "host_action": host_action,
        "http_status": observed_status,
        "observed_status": observed_status,
        "client_status": observed_status,
        "visible_http_status": observed_status,
        "headers_sent": False,
        "response_committed": False,
        "connection_aborted": False,
        "transport_result": "http_status",
    }
    if original_http_status is not None:
        record["original_http_status"] = original_http_status
    append_jsonl(checked_path(path), record)
    return 0


def write_host_evidence(
    path: str, case: str, phase: int, rule_id: int, probe_path: str,
    upstream_requests: int, host_action: str, decision_log: str | None = None,
) -> int:
    if upstream_requests < 0:
        raise ValueError("upstream request count must not be negative")
    probe = read_probe(probe_path)
    if host_action == "enforced_reply" and int(probe["response_bytes"]) == 0:
        raise ValueError("enforced host reply has no response bytes")
    record: dict[str, object] = {
        "evidence_type": "haproxy_native_htx_host_runtime",
        "evidence_origin": "real_host_socket_traffic",
        "case": case,
        "phase": phase,
        "rule_id": rule_id,
        "client_status": probe["status"],
        "client_response_bytes": probe["response_bytes"],
        "upstream_requests": upstream_requests,
        "host_action": host_action,
    }
    if decision_log:
        decision = decision_from_log(decision_log, phase, rule_id)
        record.update({
            "transaction_id": decision["transaction_id"],
            "decision_status": decision["status"],
            "requested_action": decision["action"],
        })
    append_jsonl(checked_path(path), record)
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("free-port")
    wait = subparsers.add_parser("wait-port")
    wait.add_argument("--port", required=True, type=int)
    serve = subparsers.add_parser("serve-upstream")
    serve.add_argument("--port", required=True, type=int)
    serve.add_argument("--request-log")
    request = subparsers.add_parser("probe")
    request.add_argument("--url", required=True)
    request.add_argument("--header", action="append", default=[])
    request.add_argument("--method", default="GET")
    request.add_argument("--data")
    request.add_argument("--evidence-path")
    rules = subparsers.add_parser("write-rules")
    rules.add_argument("--path", required=True)
    rules.add_argument("--canonical-rules")
    config = subparsers.add_parser("write-config")
    config.add_argument("--path", required=True)
    config.add_argument("--listen-port", required=True, type=int)
    config.add_argument("--upstream-port", required=True, type=int)
    config.add_argument("--rules-file", required=True)
    count = subparsers.add_parser("upstream-count")
    count.add_argument("--path", required=True)
    count.add_argument("--profile", required=True, choices=("ordinary", "phase3", "phase4"))
    event = subparsers.add_parser("write-event")
    event.add_argument("--path", required=True)
    event.add_argument("--case", required=True)
    event.add_argument("--decision-log", required=True)
    event.add_argument("--phase", required=True, type=int)
    event.add_argument("--rule-id", required=True, type=int)
    event.add_argument("--observed-status", required=True, type=int)
    event.add_argument("--host-action", required=True, choices=("enforced_reply",))
    event.add_argument("--original-http-status", type=int)
    evidence = subparsers.add_parser("write-host-evidence")
    evidence.add_argument("--path", required=True)
    evidence.add_argument("--case", required=True)
    evidence.add_argument("--phase", required=True, type=int)
    evidence.add_argument("--rule-id", required=True, type=int)
    evidence.add_argument("--probe-path", required=True)
    evidence.add_argument("--upstream-requests", required=True, type=int)
    evidence.add_argument("--host-action", required=True,
                          choices=("forwarded", "enforced_reply", "observed_only", "not_attempted"))
    evidence.add_argument("--decision-log")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.command == "free-port":
        print(free_port())
        return 0
    if args.command == "wait-port":
        return wait_port(args.port)
    if args.command == "serve-upstream":
        return serve_upstream(args.port, args.request_log)
    if args.command == "probe":
        return probe(args.url, args.header, args.method, args.data, args.evidence_path)
    if args.command == "write-rules":
        return write_rules(args.path, args.canonical_rules)
    if args.command == "write-config":
        return write_config(args.path, args.listen_port, args.upstream_port, args.rules_file)
    if args.command == "upstream-count":
        print(upstream_count(args.path, args.profile))
        return 0
    if args.command == "write-event":
        return write_event(
            args.path, args.case, args.decision_log, args.phase, args.rule_id,
            args.observed_status, args.host_action, args.original_http_status,
        )
    if args.command == "write-host-evidence":
        return write_host_evidence(
            args.path, args.case, args.phase, args.rule_id, args.probe_path,
            args.upstream_requests, args.host_action, args.decision_log,
        )
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as exc:
        print(f"haproxy_htx_smoke_helper: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
