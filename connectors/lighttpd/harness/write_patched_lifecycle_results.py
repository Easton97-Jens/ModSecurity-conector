#!/usr/bin/env python3
"""Write metadata-only selected-case observations for a patched lighttpd run.

The input is the event stream emitted by the real patched lighttpd host.  A
disruptive case is PASS only when the client status and a *host-confirmed*
Common event agree on its rule, transaction, and visible status.  This helper
never invents an event, transaction ID, or rule observation.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


CASE_RULES = {
    "deny_header_marker_403": (1100001, 403),
    "deny_with_alternative_status": (1100002, 429),
    "deny_request_body_marker_403": (1100101, 403),
    "deny_response_header_marker_403": (1100201, 403),
    "phase3_deny_before_commit": (1100201, 403),
    "phase3_original_and_visible_status": (1100201, 403),
}


def load_events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"events.jsonl:{number} is not an object")
        events.append(value)
    return events


def host_confirmed_event(
    events: list[dict[str, Any]], rule_id: int, visible_status: int
) -> dict[str, Any] | None:
    matches = [
        event
        for event in events
        if event.get("connector") == "lighttpd"
        and event.get("integration_mode") == "patched-native-lighttpd"
        and str(event.get("rule_id") or "") == str(rule_id)
        and event.get("visible_http_status") == visible_status
        and event.get("transport_result") == "http_status"
        and isinstance(event.get("transaction_id"), str)
        and event["transaction_id"]
    ]
    return matches[-1] if matches else None


def result_row(
    case_id: str,
    actual_status: int,
    event: dict[str, Any] | None,
    event_path: Path,
) -> dict[str, Any]:
    rule_id, expected_status = CASE_RULES[case_id]
    matched = event is not None and actual_status == expected_status
    row: dict[str, Any] = {
        "case_id": case_id,
        "status": "PASS" if matched else "FAIL",
        "actual_status": actual_status,
        "live_executed": True,
        "observed_rule_ids": [rule_id] if event is not None else [],
        "transaction_ids": [event["transaction_id"]] if event is not None else [],
        "decision_log_path": str(event_path),
        "observed_transport_result": "http_status",
        "reason": (
            "real patched-lighttpd host status and host-confirmed Common event agree"
            if matched
            else "real patched-lighttpd status lacks a matching host-confirmed Common event"
        ),
    }
    if case_id.startswith("phase3_") and event is not None:
        row.update(
            {
                "http_status": event.get("http_status"),
                "original_http_status": event.get("original_http_status"),
                "visible_http_status": event.get("visible_http_status"),
                "requested_action": event.get("requested_action"),
                "actual_action": event.get("actual_action"),
                "headers_sent": event.get("headers_sent"),
                "connection_aborted": event.get("connection_aborted"),
                "transport_result": event.get("transport_result"),
            }
        )
    return row


def requested_cases(value: str) -> set[str]:
    return {item for item in value.split() if item}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--selected-case-ids", default="")
    parser.add_argument("--allow-status", required=True, type=int)
    parser.add_argument("--deny-status", required=True, type=int)
    parser.add_argument("--alternative-status", required=True, type=int)
    parser.add_argument("--request-body-status", required=True, type=int)
    parser.add_argument("--response-header-status", required=True, type=int)
    args = parser.parse_args()

    events = load_events(args.events)
    selected = requested_cases(args.selected_case_ids)
    rows: list[dict[str, Any]] = []
    if "allow_without_marker" in selected:
        rows.append(
            {
                "case_id": "allow_without_marker",
                "status": "PASS" if args.allow_status == 200 else "FAIL",
                "actual_status": args.allow_status,
                "live_executed": True,
                "observed_transport_result": "http_status",
                "reason": "real patched-lighttpd allow request",
            }
        )

    statuses = {
        "deny_header_marker_403": args.deny_status,
        "deny_with_alternative_status": args.alternative_status,
        "deny_request_body_marker_403": args.request_body_status,
        "deny_response_header_marker_403": args.response_header_status,
        "phase3_deny_before_commit": args.response_header_status,
        "phase3_original_and_visible_status": args.response_header_status,
    }
    for case_id, actual_status in statuses.items():
        if case_id not in selected:
            continue
        rule_id, expected_status = CASE_RULES[case_id]
        rows.append(
            result_row(
                case_id,
                actual_status,
                host_confirmed_event(events, rule_id, expected_status),
                args.events,
            )
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as stream:
        for row in rows:
            stream.write(json.dumps(row, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
