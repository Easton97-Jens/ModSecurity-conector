#!/usr/bin/env python3
"""Drive one bounded HTTP/1.1 Traefik composite case.

The driver is an operator-side harness helper, not an evidence generator.  It
performs one real request, reads the observer's metadata-only JSONL after the
request, and writes only the verifier's bounded metadata receipts.  Request
and response bytes are held in memory for the request, never logged or saved.
"""

from __future__ import annotations

import argparse
import http.client
import json
import os
from pathlib import Path
import re
import sys
import time
from typing import Any, NoReturn

SCHEMA = "msc-composite-evidence/v1"
MAX_EVENT_LOG = 256 * 1024
MAX_EVENT_LINE = 16 * 1024
MAX_UPSTREAM_OBSERVATION = 16 * 1024
P2_LIMIT_PROBE_BYTES = 33
DECISION_ID = re.compile(r"^[A-Za-z0-9_-]{16,256}$")
CASES = {
    "p1_allow": ("P1", "P2", "P3", "P4"),
    "p1_deny": ("P1",),
    "p2_allow": ("P1", "P2", "P3", "P4"),
    "p2_deny": ("P1", "P2"),
    "p2_oversize": ("P1", "P2"),
    "p3_deny": ("P1", "P2", "P3"),
    "p3_redirect": ("P1", "P2", "P3"),
    "p4_safe": ("P1", "P2", "P3", "P4"),
    "p4_strict": ("P1", "P2", "P3", "P4"),
    # Omission is pre-admission: ForwardAuth receives no private lease and
    # returns 503 before any Common P1/P2 processing. A truthful receipt has
    # only the payload-free reservation opener and its terminal cleanup.
    "metadata_omitted": (),
    "p2_to_p3_timeout": ("P1", "P2"),
}
VECTOR_FOR_CASE = {
    "p1_allow": "allow_control",
    "p1_deny": "p1_only",
    "p2_allow": "p2_empty_body",
    "p2_deny": "p2_only",
    "p2_oversize": "p2_body_limit",
    "p3_deny": "p3_only",
    "p3_redirect": "p3_only",
    "p4_safe": "p4_safe",
    "p4_strict": "p4_strict",
    "metadata_omitted": "allow_control",
    "p2_to_p3_timeout": "allow_control",
}
ALLOWED_EVENT_KEYS = {
    "decision_id", "connector", "phase", "outcome", "reason",
    "requested_action", "actual_host_action", "visible_status",
    "cleanup_outcome", "event_time", "rule_id", "request_path",
    "response_path", "transport",
}
FORBIDDEN_OUTPUT_KEYS = ("body", "payload", "lease", "credential", "secret", "token", "password")


def fail(message: str) -> NoReturn:
    raise RuntimeError(message)


def load_catalog(path: Path) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file():
        fail("case input must be a regular non-symlink file")
    if path.stat().st_size > MAX_EVENT_LOG:
        fail("case input exceeds the bounded catalog size")
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict) or not isinstance(value.get("vectors"), list):
        fail("case input is not a catalog with vectors")
    return value


def select_case(catalog: dict[str, Any], runtime_root: Path) -> tuple[str, dict[str, Any]]:
    selected = catalog.get("selected_case")
    if selected is not None:
        if not isinstance(selected, str) or selected not in CASES:
            fail("selected_case must name one supported verifier case")
        candidates = [v for v in catalog["vectors"] if isinstance(v, dict) and v.get("id") == VECTOR_FOR_CASE[selected]]
        if len(candidates) != 1:
            fail("selected_case does not resolve to exactly one catalog vector")
        return selected, candidates[0]
    name = runtime_root.name
    matches = [case for case in CASES if re.search(rf"(?:^|[-_.]){re.escape(case)}(?:$|[-_.])", name)]
    if len(matches) != 1:
        fail("runtime-root must contain exactly one explicit verifier case name")
    case = matches[0]
    vector_id = VECTOR_FOR_CASE[case]
    candidates = [v for v in catalog["vectors"] if isinstance(v, dict) and v.get("id") == vector_id]
    if len(candidates) != 1:
        fail("runtime-root case does not resolve to exactly one catalog vector")
    return case, candidates[0]


def request_body(vector: dict[str, Any]) -> bytes:
    request = vector.get("request")
    if not isinstance(request, dict):
        fail("vector request is not an object")
    if request.get("client_abort"):
        fail("client-abort vectors require a dedicated transport primitive and are not promoted by this driver")
    if vector.get("id") == "p2_body_limit":
        # ForwardAuth accepts at most the coordinator limit plus one byte.
        # The catalog's larger source vector remains available for host-only
        # rejection checks, while this composite case must reach the service
        # to prove its same-transaction, bounded P2-limit cleanup path.
        return b"x" * P2_LIMIT_PROBE_BYTES
    if isinstance(request.get("body"), str):
        return request["body"].encode("utf-8")
    prefix = request.get("body_prefix")
    if isinstance(prefix, str):
        target = request.get("headers", {}).get("Content-Length", len(prefix))
        if not isinstance(target, int) or target < len(prefix) or target > 64 * 1024:
            fail("body length is outside the bounded request budget")
        return prefix.encode("utf-8") + b"x" * (target - len(prefix))
    return b""


def read_events(path: Path) -> list[dict[str, Any]]:
    if path.is_symlink() or not path.is_file():
        return []
    if path.stat().st_size > MAX_EVENT_LOG:
        fail("observer event log exceeds the bounded metadata size")
    events: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for number, line in enumerate(handle, 1):
            if len(line.encode("utf-8")) > MAX_EVENT_LINE or not line.strip():
                fail(f"observer event line {number} is not bounded metadata")
            event = json.loads(line)
            if not isinstance(event, dict) or set(event) - ALLOWED_EVENT_KEYS:
                fail(f"observer event line {number} contains unsupported or payload fields")
            if any(key.lower() in FORBIDDEN_OUTPUT_KEYS for key in event):
                fail(f"observer event line {number} contains a forbidden payload field")
            events.append(event)
    return events


def wait_for_terminal(path: Path, timeout: float = 8.0) -> list[dict[str, Any]]:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        events = read_events(path)
        if events and events[-1].get("phase") == "terminal":
            return events
        time.sleep(0.05)
    fail("observer did not close this transaction within the bounded timeout")


def http_request(
    base_url: str, vector: dict[str, Any], add_client_lease: bool, timeout: float = 5.0
) -> tuple[int | None, bool]:
    match = re.fullmatch(r"http://([^:/]+):(\d+)", base_url)
    if not match or match.group(1) not in {"127.0.0.1", "localhost"}:
        fail("base-url must be a local HTTP/1.1 endpoint")
    request = vector.get("request")
    if not isinstance(request, dict) or not isinstance(request.get("path"), str):
        fail("vector request path is missing")
    method = request.get("method", "GET")
    headers = request.get("headers", {})
    if not isinstance(method, str) or not isinstance(headers, dict):
        fail("vector request metadata is malformed")
    body = request_body(vector)
    normalized_headers = {
        str(key): str(value)
        for key, value in headers.items()
        if str(key).lower() not in {"content-length", "x-msconnector-composite-lease"}
    }
    if body or any(str(key).lower() == "content-length" for key in headers):
        normalized_headers["Content-Length"] = str(len(body))
    if add_client_lease:
        # This arbitrary client value must be removed before the real upstream.
        # It is never persisted or included in an observation receipt.
        normalized_headers["X-Msconnector-Composite-Lease"] = "client-supplied-invalid"
    conn = http.client.HTTPConnection(match.group(1), int(match.group(2)), timeout=timeout)
    try:
        conn.request(method, request["path"], body=body, headers=normalized_headers)
        response = conn.getresponse()
        status = response.status
        response.read(32 * 1024)
        return status, True
    except (OSError, http.client.HTTPException):
        return None, False
    finally:
        conn.close()


def expected_status(case: str) -> set[int] | None:
    return {
        "p1_allow": set(range(200, 300)), "p1_deny": {403},
        "p2_allow": set(range(200, 300)), "p2_deny": {403},
        "p2_oversize": {413}, "p3_deny": {403}, "p3_redirect": set(range(300, 400)),
        "p4_safe": {200}, "p4_strict": None,
        "metadata_omitted": {503}, "p2_to_p3_timeout": {503},
    }[case]


def write_json(path: Path, value: dict[str, Any]) -> None:
    if path.is_symlink() or path.exists():
        fail(f"refusing to overwrite receipt path {path.name}")
    path.parent.mkdir(mode=0o700, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, sort_keys=True, separators=(",", ":"))
            handle.write("\n")
    except BaseException:
        try:
            os.close(fd)
        except OSError:
            pass
        raise


def read_upstream_observation(path: Path, runtime_root: Path, case: str) -> dict[str, Any]:
    if path.parent != runtime_root or runtime_root.is_symlink() or not runtime_root.is_dir():
        fail("upstream observation root is not a directory")
    root_stat = runtime_root.stat()
    if root_stat.st_uid != os.getuid() or root_stat.st_mode & 0o077:
        fail("upstream observation root is not owner-only")
    if path.is_symlink() or not path.is_file():
        fail("upstream observation must be a direct-child regular file")
    stat_result = path.stat()
    if stat_result.st_uid != os.getuid() or stat_result.st_mode & 0o077:
        fail("upstream observation is not owner-only")
    if stat_result.st_size > MAX_UPSTREAM_OBSERVATION:
        fail("upstream observation exceeds the bounded metadata size")
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict) or set(value) != {"schema", "requests_seen", "lease_header_observed"}:
        fail("upstream observation schema is invalid")
    if value.get("schema") != "traefik-composite-upstream-observation/v1":
        fail("upstream observation schema version is invalid")
    if not isinstance(value.get("requests_seen"), int) or value["requests_seen"] < 0:
        fail("upstream observation request count is invalid")
    if not isinstance(value.get("lease_header_observed"), bool):
        fail("upstream observation lease flag is invalid")
    expected_upstream = case not in {"p1_deny", "p2_deny", "p2_oversize", "metadata_omitted"}
    if expected_upstream and value["requests_seen"] < 1:
        fail("expected case did not reach the real upstream")
    if value["lease_header_observed"]:
        fail("internal lease header reached the real upstream")
    return value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--event-log", required=True, type=Path)
    parser.add_argument("--runtime-root", required=True, type=Path)
    parser.add_argument("--upstream-observation", required=True, type=Path)
    parser.add_argument("--connector", required=True, choices=("traefik",))
    args = parser.parse_args(argv)
    try:
        catalog = load_catalog(args.input)
        case, vector = select_case(catalog, args.runtime_root)
        request_timeout = 10.0 if case == "p2_to_p3_timeout" else 5.0
        status, response_completed = http_request(
            args.base_url, vector, case == "p1_allow", request_timeout
        )
        allowed = expected_status(case)
        if allowed is not None and status not in allowed:
            fail(f"{case} returned an unexpected client status")
        events = wait_for_terminal(args.event_log)
        upstream_observation = read_upstream_observation(args.upstream_observation, args.runtime_root, case)
        ids = {event.get("decision_id") for event in events}
        if len(ids) != 1 or not isinstance(next(iter(ids)), str) or not DECISION_ID.fullmatch(next(iter(ids))):
            fail("observer did not provide exactly one server-generated decision_id")
        decision_id = next(iter(ids))
        phases = [event.get("phase") for event in events if event.get("phase") in {"P1", "P2", "P3", "P4"}]
        if tuple(phases) != CASES[case]:
            fail("observer phases do not match the selected isolated case")
        client = {
            "lease_observed": False, "visible_status": status,
            "p4_outcome": "none", "p4_visible_status": None,
            "p4_response_committed": bool(response_completed and case in {"p1_allow", "p2_allow", "p4_safe"}),
        }
        upstream = {
            "lease_observed": upstream_observation["lease_header_observed"],
            "request_terminal": case in {"p1_deny", "p2_deny", "p2_oversize"},
            "response_observed": upstream_observation["requests_seen"] > 0,
        }
        stem = args.manifest.stem
        write_json(args.runtime_root / f"{stem}.client.json", client)
        write_json(args.runtime_root / f"{stem}.upstream.json", upstream)
        manifest = {
            "schema": SCHEMA, "connector": args.connector, "case": case,
            "case_artifact": {"id": f"traefik-{case}", "event_log": args.event_log.name},
            "expected_phases": list(CASES[case]),
            "client_observation": f"{stem}.client.json",
            "upstream_observation": f"{stem}.upstream.json",
            "cleanup": {"count": 1, "status": "completed"},
        }
        write_json(args.manifest, manifest)
        print(json.dumps({"case": case, "decision_id": decision_id, "status": status}, sort_keys=True))
        return 0
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"traefik_composite_case_driver: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
