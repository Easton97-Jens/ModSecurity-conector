#!/usr/bin/env python3
"""Local-only helpers for real HAProxy HTX host-runtime evidence.

The helper deliberately retains only bounded metadata from the local client,
upstream, and HAProxy process.  It never persists request/response payloads.
"""

from __future__ import annotations

import argparse
import http.client
import http.server
import json
from pathlib import Path
import re
import socket
import sys
import threading
import time
import urllib.error
import urllib.request
import urllib.parse


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
LATE_DECISION_PATTERN = re.compile(
    r"transaction_id=(?P<transaction_id>[A-Za-z0-9._-]+) "
    r"phase=(?P<phase>[0-9]+) status=(?P<status>[0-9]+) "
    r"rule_id=(?P<rule_id>[0-9]+) "
    r"requested_action=(?P<requested_action>[A-Za-z_]+) "
    r"resolved_policy_action=(?P<resolved_policy_action>[A-Za-z_]+) "
    r"host_action=(?P<host_action>[A-Za-z_]+)"
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


def load_json_object(path: str, label: str) -> dict[str, object]:
    target = checked_path(path)
    try:
        value = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid {label}: {target}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} is not an object: {target}")
    return value


def safe_token(value: object, label: str, maximum: int = 128) -> str:
    text = str(value or "").strip()
    if not text or len(text) > maximum or not re.fullmatch(r"[A-Za-z0-9:._-]+", text):
        raise ValueError(f"invalid {label}")
    return text


def safe_htx_transaction_id(value: object) -> str:
    """Return the request-ID grammar accepted by the native HTX filter."""

    text = safe_token(value, "HTX transaction id", maximum=256)
    if re.fullmatch(r"[A-Za-z0-9._-]+", text) is None:
        raise ValueError("invalid HTX transaction id")
    return text


def upstream_profile(raw_path: str) -> tuple[str, str | None, bytes]:
    path = raw_path.split("?", 1)[0]
    if path == "/no-crs/request-body":
        return "phase2", None, UPSTREAM_OK_BODY
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
            record: dict[str, object] = {
                "method": self.command,
                "response_status": 200,
                "profile": profile,
            }
            # The native HTX overlay accepts this bounded request ID as its
            # transaction ID.  Retain only that already-safe correlation
            # token, never arbitrary request-header data.
            try:
                request_id = safe_htx_transaction_id(self.headers.get("x-request-id"))
            except ValueError:
                request_id = ""
            if request_id:
                record["request_id"] = request_id
            with request_log_lock:
                append_jsonl(request_log, record)
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


def streaming_probe(
    url: str,
    release_path: str,
    first_byte_path: str,
    evidence_path: str,
    timeout: float,
) -> int:
    """Read one body byte through HAProxy before releasing a paused upstream.

    The client retains only the current read buffer.  Its two JSON files contain
    status/count metadata, never body bytes.  The caller owns the release file,
    which makes the client-first-byte observation independent of the later
    Phase-4 marker and upstream EOS.
    """

    if timeout <= 0:
        raise ValueError("timeout must be positive")
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "http" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("streaming probe requires an absolute credential-free HTTP URL")
    if parsed.fragment:
        raise ValueError("streaming probe URL must not contain a fragment")
    port = parsed.port or 80
    request_path = parsed.path or "/"
    if parsed.query:
        request_path += f"?{parsed.query}"
    release = checked_path(release_path)
    first_byte_output = checked_path(first_byte_path)
    evidence_output = checked_path(evidence_path)
    connection = http.client.HTTPConnection(parsed.hostname, port, timeout=timeout)
    response: http.client.HTTPResponse | None = None
    try:
        connection.request(
            "GET",
            request_path,
            headers={
                "Host": parsed.hostname,
                "Connection": "close",
                "X-Request-Id": "haproxy-htx-phase4",
            },
        )
        response = connection.getresponse()
        first = response.read(1)
        if not first:
            raise ValueError("HAProxy response ended before its first response-body byte")
        write_json(first_byte_output, {
            "status": int(response.status),
            "client_first_byte_received": True,
            "first_chunk_size": len(first),
            "response_committed": True,
            "body_payload_persisted": False,
        })

        deadline = time.monotonic() + timeout
        while not release.is_file():
            if time.monotonic() >= deadline:
                raise ValueError("timed out waiting for the synchronized upstream release")
            time.sleep(0.01)

        response_bytes = len(first)
        while True:
            chunk = response.read(8192)
            if not chunk:
                break
            response_bytes += len(chunk)
        write_json(evidence_output, {
            "status": int(response.status),
            "response_bytes": response_bytes,
            "content_type": str(response.getheader("content-type") or "")[:256],
        })
    finally:
        if response is not None:
            response.close()
        connection.close()
    print(response.status if response is not None else 0)
    return 0


def wait_for_file(path: str, timeout: float) -> int:
    if timeout <= 0:
        raise ValueError("timeout must be positive")
    target = checked_path(path)
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if target.is_file() and target.stat().st_size > 0:
            return 0
        time.sleep(0.01)
    raise ValueError(f"timed out waiting for payload-free control file: {target}")


def synchronized_upstream_port(path: str) -> int:
    value = load_json_object(path, "synchronized upstream ready record")
    if value.get("schema_version") != 1 or value.get("evidence_type") != "synchronized_upstream_ready":
        raise ValueError("invalid synchronized upstream ready record")
    if value.get("body_payload_persisted") is not False:
        raise ValueError("synchronized upstream ready record must be payload-free")
    host = value.get("upstream_host")
    port = value.get("upstream_port")
    if host != "127.0.0.1" or isinstance(port, bool) or not isinstance(port, int) or not 1 <= port <= 65535:
        raise ValueError("invalid synchronized upstream address")
    return port


def validate_synchronized_upstream_complete(path: str) -> int:
    value = load_json_object(path, "synchronized upstream completion record")
    if value.get("schema_version") != 1 or value.get("evidence_type") != "synchronized_upstream_server":
        raise ValueError("invalid synchronized upstream completion record")
    if value.get("body_payload_persisted") is not False:
        raise ValueError("synchronized upstream completion record must be payload-free")
    if value.get("upstream_paused") is not True or value.get("upstream_eos_sent") is not True:
        raise ValueError("synchronized upstream did not record the required pause and EOS")
    size = value.get("first_chunk_size")
    if isinstance(size, bool) or not isinstance(size, int) or size < 1:
        raise ValueError("synchronized upstream completion record has invalid first_chunk_size")
    return 0


def first_byte_evidence(
    paused_path: str, client_first_byte_path: str,
) -> dict[str, object]:
    """Bind a real HTTP client first byte to the still-paused upstream state."""

    paused = load_json_object(paused_path, "synchronized upstream pause record")
    client = load_json_object(client_first_byte_path, "client first-byte record")
    if paused.get("schema_version") != 1 or paused.get("evidence_type") != "synchronized_upstream_paused":
        raise ValueError("invalid synchronized upstream pause record")
    if paused.get("upstream_paused") is not True or paused.get("upstream_eos_sent") is not False:
        raise ValueError("synchronized upstream was not paused before EOS")
    if paused.get("body_payload_persisted") is not False:
        raise ValueError("synchronized upstream pause record must be payload-free")
    upstream_first_chunk = paused.get("first_chunk_size")
    if isinstance(upstream_first_chunk, bool) or not isinstance(upstream_first_chunk, int) or upstream_first_chunk < 1:
        raise ValueError("synchronized upstream pause record has invalid first_chunk_size")
    if client.get("client_first_byte_received") is not True or client.get("response_committed") is not True:
        raise ValueError("HAProxy client did not observe a committed first response-body byte")
    if client.get("body_payload_persisted") is not False:
        raise ValueError("client first-byte record must be payload-free")
    client_first_chunk = client.get("first_chunk_size")
    if isinstance(client_first_chunk, bool) or not isinstance(client_first_chunk, int) or client_first_chunk < 1:
        raise ValueError("client first-byte record has invalid first_chunk_size")
    status = client.get("status")
    if isinstance(status, bool) or not isinstance(status, int) or status != 200:
        raise ValueError("first-byte client did not observe HTTP 200")
    # The filter consumes the current borrowed HTX DATA slice before returning
    # its length.  At the observed first byte, the only connector-side body
    # accounting that can honestly be published is the current upstream chunk.
    return {
        "schema_version": 1,
        "evidence_type": "synchronized_first_byte",
        "evidence_origin": "real_host",
        "promotion_eligible": True,
        "client_first_byte_received": True,
        "first_byte_before_response_end": True,
        "first_chunk_size": upstream_first_chunk,
        "upstream_paused": True,
        "upstream_eos_sent_at_first_byte": False,
        "upstream_response_finished_at_first_byte": False,
        "response_committed": True,
        "body_bytes_seen": upstream_first_chunk,
        "body_bytes_inspected": upstream_first_chunk,
        "no_full_response_buffering": True,
        "connector_owned_full_response_buffer": False,
        "transport_protocol": "http1",
        "body_payload_persisted": False,
        "outcome": "PASS",
    }


def write_first_byte_evidence(
    path: str, paused_path: str, client_first_byte_path: str,
) -> int:
    write_json(checked_path(path), first_byte_evidence(paused_path, client_first_byte_path))
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


def probe_status(path: str) -> int:
    """Return the validated status from a payload-free completed probe."""

    return int(read_probe(path)["status"])


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


def upstream_transaction_observed(path: str, profile: str, transaction_id: str) -> bool:
    """Return whether exactly one upstream request preserved the HTX ID."""

    expected_transaction_id = safe_htx_transaction_id(transaction_id)
    target = checked_path(path)
    if not target.is_file():
        return False
    matches = 0
    for line in target.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid upstream evidence: {target}") from exc
        if not isinstance(record, dict):
            continue
        if (
            record.get("profile") == profile
            and record.get("request_id") == expected_transaction_id
        ):
            matches += 1
    return matches == 1


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


def late_decision_from_log(path: str, phase: int, rule_id: int) -> dict[str, object]:
    target = checked_path(path)
    if not target.is_file():
        raise ValueError(f"HAProxy host log is missing: {target}")
    matches: list[dict[str, object]] = []
    for line in target.read_text(encoding="utf-8", errors="replace").splitlines():
        match = LATE_DECISION_PATTERN.search(line)
        if not match:
            continue
        result: dict[str, object] = {
            "transaction_id": match.group("transaction_id"),
            "phase": int(match.group("phase")),
            "status": int(match.group("status")),
            "rule_id": int(match.group("rule_id")),
            "requested_action": match.group("requested_action").lower(),
            "resolved_policy_action": match.group("resolved_policy_action").lower(),
            "host_action": match.group("host_action").lower(),
        }
        if result["phase"] == phase and result["rule_id"] == rule_id:
            matches.append(result)
    if not matches:
        raise ValueError(f"HAProxy host log lacks late phase {phase} rule {rule_id}: {target}")
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


def write_allow_event(
    path: str, probe_path: str, upstream_log: str, transaction_id: str,
) -> int:
    """Publish a real, payload-free P1 allow outcome after the full run.

    The event is deliberately appended after the P4 barrier event.  The
    Framework's generic no-rule case selector chooses the final matching 200
    response, so this preserves its causal binding to this actual Phase-1
    request rather than accidentally borrowing the P4 safe response.
    """

    transaction = safe_htx_transaction_id(transaction_id)
    probe = read_probe(probe_path)
    if probe["status"] != 200 or int(probe["response_bytes"]) < 1:
        raise ValueError("HAProxy allow client outcome must preserve HTTP 200 with a body")
    if not upstream_transaction_observed(upstream_log, "ordinary", transaction):
        raise ValueError("HAProxy allow transaction was not observed exactly once upstream")
    record: dict[str, object] = {
        # This is a projection of the completed client request and the
        # matching upstream request-ID, not a policy decision or capability
        # promotion.  Allow is intentionally absent from the closed action
        # vocabularies, so no requested/actual action is inferred here.
        "connector": "haproxy",
        "event": "native_htx_host_forward",
        "message_id": "HAPROXY_HTX_NATIVE_P1_ALLOW",
        "integration_mode": "native-htx-filter",
        "transaction_id": transaction,
        "phase": 1,
        "status": "allowed",
        "http_status": 200,
        "visible_http_status": 200,
        "headers_sent": True,
        "response_committed": True,
        "connection_aborted": False,
        "transport_result": "http_status",
    }
    append_jsonl(checked_path(path), record)
    return 0


def phase4_safe_event(
    path: str,
    decision_log: str,
    probe_path: str,
    first_byte_evidence_path: str,
    run_id: str,
    transport_case_id: str,
) -> int:
    """Publish one payload-free host-confirmed P4 safe outcome.

    The decision comes from the native HTX filter's post-EOS log record, the
    visible status comes from the real HTTP/1.1 client, and the barrier fields
    come from the already-written real-host first-byte artifact.  No field is
    inferred from a policy default or fixture payload.
    """

    decision = late_decision_from_log(decision_log, 4, 1100301)
    if (
        decision["requested_action"] != "deny"
        or decision["resolved_policy_action"] != "log_only"
        or decision["host_action"] != "log_only"
        or decision["status"] != 403
    ):
        raise ValueError("HAProxy late decision is not the required safe log-only outcome")
    probe = read_probe(probe_path)
    if probe["status"] != 200 or int(probe["response_bytes"]) < 1:
        raise ValueError("HAProxy safe P4 client outcome must preserve HTTP 200 with a body")
    evidence = load_json_object(first_byte_evidence_path, "first-byte evidence")
    required_true = (
        "promotion_eligible",
        "client_first_byte_received",
        "first_byte_before_response_end",
        "upstream_paused",
        "response_committed",
        "no_full_response_buffering",
    )
    if (
        evidence.get("schema_version") != 1
        or evidence.get("evidence_type") != "synchronized_first_byte"
        or evidence.get("evidence_origin") != "real_host"
        or evidence.get("outcome") != "PASS"
        or evidence.get("body_payload_persisted") is not False
        or any(evidence.get(name) is not True for name in required_true)
        or evidence.get("upstream_eos_sent_at_first_byte") is not False
        or evidence.get("upstream_response_finished_at_first_byte") is not False
        or evidence.get("connector_owned_full_response_buffer") is not False
    ):
        raise ValueError("first-byte evidence is not a complete real-host no-buffer proof")
    first_chunk_size = evidence.get("first_chunk_size")
    body_seen = evidence.get("body_bytes_seen")
    body_inspected = evidence.get("body_bytes_inspected")
    if any(
        isinstance(value, bool) or not isinstance(value, int) or value < 0
        for value in (first_chunk_size, body_seen, body_inspected)
    ) or int(first_chunk_size) < 1 or int(body_inspected) > int(body_seen):
        raise ValueError("first-byte evidence has invalid body accounting")
    safe_run_id = safe_token(run_id, "run id", maximum=128)
    safe_transport_case = safe_token(transport_case_id, "transport case id")
    transaction_id = safe_token(decision["transaction_id"], "transaction id", maximum=256)
    record: dict[str, object] = {
        "connector": "haproxy",
        "event": "native_htx_phase4_late_intervention",
        "message_id": "HAPROXY_HTX_NATIVE_LATE_LOG_ONLY",
        "integration_mode": "native-htx-filter",
        "run_id": safe_run_id,
        "transaction_id": transaction_id,
        "phase": 4,
        "rule_id": 1100301,
        "status": "blocked",
        "requested_action": "deny",
        "actual_action": "log_only",
        "http_status": 403,
        "original_http_status": 200,
        "visible_http_status": 200,
        "late_intervention": True,
        "late_intervention_mode": "safe",
        "headers_sent": True,
        "response_started": True,
        "body_started": True,
        "response_committed": True,
        "connection_aborted": False,
        "transport_result": "log_only",
        "negotiated_protocol": "http1",
        "transport": "tcp",
        "transport_case_id": safe_transport_case,
        "barrier_id": f"{transaction_id}.first-byte",
        "client_first_byte_received": True,
        "first_byte_before_response_end": True,
        "first_chunk_size": first_chunk_size,
        "upstream_paused": True,
        "upstream_eos_sent_at_first_byte": False,
        "upstream_response_finished_at_first_byte": False,
        "no_full_response_buffering": True,
        "body_bytes_seen": body_seen,
        "body_bytes_inspected": body_inspected,
        "eos_seen": True,
        "end_of_stream_evaluation": True,
        "cleanup_reason": "normal",
    }
    append_jsonl(checked_path(path), record)
    return 0


def write_host_evidence(
    path: str, case: str, phase: int, rule_id: int, probe_path: str,
    upstream_requests: int, host_action: str, decision_log: str | None = None,
) -> int:
    if upstream_requests < 0:
        raise ValueError("upstream request count must not be negative")
    probe = read_probe(probe_path)
    if host_action in {"enforced_reply", "safe_log_only"} and int(probe["response_bytes"]) == 0:
        raise ValueError(f"{host_action} host outcome has no client response bytes")
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
    streaming = subparsers.add_parser("streaming-probe")
    streaming.add_argument("--url", required=True)
    streaming.add_argument("--release-path", required=True)
    streaming.add_argument("--first-byte-path", required=True)
    streaming.add_argument("--evidence-path", required=True)
    streaming.add_argument("--timeout", type=float, default=10.0)
    wait = subparsers.add_parser("wait-file")
    wait.add_argument("--path", required=True)
    wait.add_argument("--timeout", type=float, default=10.0)
    ready = subparsers.add_parser("synchronized-upstream-port")
    ready.add_argument("--path", required=True)
    upstream_complete = subparsers.add_parser("validate-synchronized-upstream")
    upstream_complete.add_argument("--path", required=True)
    first_byte = subparsers.add_parser("write-first-byte-evidence")
    first_byte.add_argument("--path", required=True)
    first_byte.add_argument("--paused-path", required=True)
    first_byte.add_argument("--client-first-byte-path", required=True)
    probe_status_parser = subparsers.add_parser("probe-status")
    probe_status_parser.add_argument("--path", required=True)
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
    count.add_argument("--profile", required=True, choices=("ordinary", "phase2", "phase3", "phase4"))
    event = subparsers.add_parser("write-event")
    event.add_argument("--path", required=True)
    event.add_argument("--case", required=True)
    event.add_argument("--decision-log", required=True)
    event.add_argument("--phase", required=True, type=int)
    event.add_argument("--rule-id", required=True, type=int)
    event.add_argument("--observed-status", required=True, type=int)
    event.add_argument("--host-action", required=True, choices=("enforced_reply",))
    event.add_argument("--original-http-status", type=int)
    allow_event = subparsers.add_parser("write-allow-event")
    allow_event.add_argument("--path", required=True)
    allow_event.add_argument("--probe-path", required=True)
    allow_event.add_argument("--upstream-log", required=True)
    allow_event.add_argument("--transaction-id", required=True)
    evidence = subparsers.add_parser("write-host-evidence")
    evidence.add_argument("--path", required=True)
    evidence.add_argument("--case", required=True)
    evidence.add_argument("--phase", required=True, type=int)
    evidence.add_argument("--rule-id", required=True, type=int)
    evidence.add_argument("--probe-path", required=True)
    evidence.add_argument("--upstream-requests", required=True, type=int)
    evidence.add_argument("--host-action", required=True,
                          choices=("forwarded", "enforced_reply", "observed_only", "safe_log_only", "not_attempted"))
    evidence.add_argument("--decision-log")
    safe_event = subparsers.add_parser("write-phase4-safe-event")
    safe_event.add_argument("--path", required=True)
    safe_event.add_argument("--decision-log", required=True)
    safe_event.add_argument("--probe-path", required=True)
    safe_event.add_argument("--first-byte-evidence", required=True)
    safe_event.add_argument("--run-id", required=True)
    safe_event.add_argument("--transport-case-id", required=True)
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
    if args.command == "streaming-probe":
        return streaming_probe(
            args.url, args.release_path, args.first_byte_path,
            args.evidence_path, args.timeout,
        )
    if args.command == "wait-file":
        return wait_for_file(args.path, args.timeout)
    if args.command == "synchronized-upstream-port":
        print(synchronized_upstream_port(args.path))
        return 0
    if args.command == "validate-synchronized-upstream":
        return validate_synchronized_upstream_complete(args.path)
    if args.command == "write-first-byte-evidence":
        return write_first_byte_evidence(
            args.path, args.paused_path, args.client_first_byte_path,
        )
    if args.command == "probe-status":
        print(probe_status(args.path))
        return 0
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
    if args.command == "write-allow-event":
        return write_allow_event(
            args.path, args.probe_path, args.upstream_log, args.transaction_id,
        )
    if args.command == "write-host-evidence":
        return write_host_evidence(
            args.path, args.case, args.phase, args.rule_id, args.probe_path,
            args.upstream_requests, args.host_action, args.decision_log,
        )
    if args.command == "write-phase4-safe-event":
        return phase4_safe_event(
            args.path, args.decision_log, args.probe_path,
            args.first_byte_evidence, args.run_id, args.transport_case_id,
        )
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as exc:
        print(f"haproxy_htx_smoke_helper: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
