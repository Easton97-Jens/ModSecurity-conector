#!/usr/bin/env python3
"""Validate the evidence properties that gate full-lifecycle promotion.

This checker is deliberately conservative: an absent capability is not a
failure, but a connector that marks a capability ``verified`` must provide a
fresh strict-profile run that proves the corresponding property.  It therefore
cannot turn a compilation, a source audit, or a synthetic upstream probe into
a capability promotion.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


CONNECTORS = ("apache", "nginx", "haproxy", "envoy", "traefik", "lighttpd")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: JSON object required")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if not path.is_file():
        return records
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{number}: JSON object required")
        records.append(value)
    return records


def capability_state(manifest: dict[str, Any], name: str) -> str:
    entry = manifest.get("capabilities", {}).get(name, {})
    return str(entry.get("state") or "") if isinstance(entry, dict) else ""


def matching_events(events: list[dict[str, Any]], rule_id: object) -> list[dict[str, Any]]:
    return [event for event in events if event.get("rule_id") == rule_id and event.get("phase") == 4]


def first_byte_errors(run_dir: Path, manifest: dict[str, Any], result: dict[str, Any]) -> list[str]:
    claimed = capability_state(manifest, "first_byte_before_response_end") == "verified"
    verified = set(result.get("capabilities_verified") or [])
    claimed = claimed or "first_byte_before_response_end" in verified
    if not claimed:
        return []
    if result.get("artifact_profile") != "full_lifecycle":
        return ["first-byte promotion requires a full_lifecycle artifact profile"]
    events = load_jsonl(run_dir / "events.jsonl")
    records = load_jsonl(run_dir / "results.jsonl")
    expected = {"phase4_first_byte_before_response_end", "phase4_no_full_response_buffering"}
    passed = {str(record.get("case_id")) for record in records if record.get("status") == "PASS"}
    missing = expected - passed
    if missing:
        return ["first-byte promotion lacks PASS cases: " + ", ".join(sorted(missing))]
    errors: list[str] = []
    for record in records:
        if record.get("case_id") not in expected or record.get("status") != "PASS":
            continue
        candidates = matching_events(events, record.get("expected_rule_id"))
        if not any(
            event.get("first_byte_before_response_end") is True
            and event.get("upstream_response_finished_at_first_byte") is False
            and event.get("upstream_paused") is True
            and isinstance(event.get("first_chunk_size"), int)
            and event.get("first_chunk_size", 0) > 0
            for event in candidates
        ):
            errors.append(f"{record.get('case_id')}: missing synchronized first-byte event metadata")
    return errors


def no_buffer_errors(run_dir: Path, manifest: dict[str, Any], result: dict[str, Any]) -> list[str]:
    claimed = capability_state(manifest, "no_full_response_buffering") == "verified"
    claimed = claimed or "no_full_response_buffering" in set(result.get("capabilities_verified") or [])
    if not claimed:
        return []
    events = load_jsonl(run_dir / "events.jsonl")
    records = load_jsonl(run_dir / "results.jsonl")
    records = [record for record in records if record.get("case_id") == "phase4_no_full_response_buffering" and record.get("status") == "PASS"]
    if not records:
        return ["no-full-response-buffering promotion lacks a PASS case"]
    for record in records:
        candidates = matching_events(events, record.get("expected_rule_id"))
        if not any(
            event.get("no_full_response_buffering") is True
            and event.get("first_byte_before_response_end") is True
            and event.get("upstream_response_finished_at_first_byte") is False
            for event in candidates
        ):
            return ["no-full-response-buffering PASS lacks the causal first-byte metadata"]
    return []


def promotion_errors(run_dir: Path, manifest: dict[str, Any], result: dict[str, Any]) -> list[str]:
    declared = manifest.get("capabilities", {})
    if not isinstance(declared, dict):
        return ["capability manifest has no capabilities object"]
    verified = {name for name, entry in declared.items() if isinstance(entry, dict) and entry.get("state") == "verified"}
    if not verified:
        return []
    if result.get("artifact_profile") != "full_lifecycle":
        return ["verified capability declarations require a full_lifecycle run"]
    runtime_verified = set(result.get("capabilities_verified") or [])
    missing = verified - runtime_verified
    if missing:
        return ["verified capabilities lack current host evidence: " + ", ".join(sorted(missing))]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--connector-root", required=True, type=Path)
    parser.add_argument("--evidence-root", required=True, type=Path)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--check", required=True, choices=("first-byte", "no-full-buffer", "promotion"))
    args = parser.parse_args()

    errors: list[str] = []
    for connector in CONNECTORS:
        run_dir = args.evidence_root / connector / args.run_id
        if not run_dir.is_dir():
            errors.append(f"{connector}: missing canonical run: {run_dir}")
            continue
        try:
            manifest = load_json(args.connector_root / "connectors" / connector / "capabilities.json")
            result = load_json(run_dir / "result.json")
            if args.check == "first-byte":
                connector_errors = first_byte_errors(run_dir, manifest, result)
            elif args.check == "no-full-buffer":
                connector_errors = no_buffer_errors(run_dir, manifest, result)
            else:
                connector_errors = promotion_errors(run_dir, manifest, result)
                connector_errors += first_byte_errors(run_dir, manifest, result)
                connector_errors += no_buffer_errors(run_dir, manifest, result)
            errors.extend(f"{connector}: {error}" for error in connector_errors)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"{connector}: cannot read canonical evidence: {exc}")
    if errors:
        for error in errors:
            print(f"full-lifecycle-evidence: FAIL: {error}")
        return 1
    print(f"full-lifecycle-evidence: PASS ({args.check}; no unsupported promotion claims)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
