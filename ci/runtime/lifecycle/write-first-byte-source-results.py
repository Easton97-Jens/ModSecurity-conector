#!/usr/bin/env python3
"""Write narrow host-result rows for the two causal Phase-4 capabilities."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: JSON object required")
    return value


def has_phase4_rule(path: Path) -> bool:
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(record, dict):
            continue
        if str(record.get("rule_id") or "") == "1100301" and str(record.get("phase") or "").replace("-", "_") in {"4", "response_body", "phase4"}:
            return True
    return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--connector", required=True, choices=("apache", "nginx"))
    parser.add_argument("--phase4-log", required=True, type=Path)
    parser.add_argument("--first-byte-evidence", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)

    evidence = load_object(args.first_byte_evidence)
    required = {
        "evidence_type": "synchronized_first_byte",
        "evidence_origin": "real_host",
        "promotion_eligible": True,
        "outcome": "PASS",
        "body_payload_persisted": False,
        "first_byte_before_response_end": True,
        "upstream_paused": True,
        "upstream_eos_sent_at_first_byte": False,
        "upstream_response_finished_at_first_byte": False,
        "no_full_response_buffering": True,
        "connector_owned_full_response_buffer": False,
    }
    if any(evidence.get(key) != expected for key, expected in required.items()):
        raise ValueError("first-byte evidence is not a successful real-host no-buffer observation")
    if not has_phase4_rule(args.phase4_log):
        raise ValueError("Phase-4 rule 1100301 was not observed in the host log")
    rows = [
        {
            "case_id": case_id,
            "status": "PASS",
            "live_executed": True,
            "actual_status": 200,
            "observed_rule_ids": [1100301],
            "connector_phase4_log_path": str(args.phase4_log),
            "first_byte_evidence_path": str(args.first_byte_evidence),
            "reason": "real host synchronized upstream barrier; payload-free metadata only",
        }
        for case_id in (
            "phase4_rule_observed",
            "phase4_first_byte_before_response_end",
            "phase4_no_full_response_buffering",
        )
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
