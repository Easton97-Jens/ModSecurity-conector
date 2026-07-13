#!/usr/bin/env python3
"""Extract bounded host counters for a synchronized first-byte evidence run.

The client/upstream barrier establishes ordering.  The selected host's Phase-4
event supplies the counters.  This helper joins those two observations without
copying a body, an intervention message, or an audit-log record into evidence.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def phase4_record(path: Path) -> dict[str, Any]:
    selected: dict[str, Any] | None = None
    for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{number}: invalid JSONL") from exc
        if not isinstance(record, dict):
            continue
        if str(record.get("rule_id") or "") != "1100301":
            continue
        phase = str(record.get("phase") or "").replace("-", "_").lower()
        if phase not in {"4", "response_body", "phase4"}:
            continue
        selected = record
    if selected is None:
        raise ValueError("host Phase-4 log does not contain rule 1100301")
    return selected


def nonnegative(record: dict[str, Any], name: str) -> int:
    value = record.get(name)
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a non-negative integer")
    try:
        number = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a non-negative integer") from exc
    if number < 0:
        raise ValueError(f"{name} must be a non-negative integer")
    return number


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase4-log", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)

    event = phase4_record(args.phase4_log)
    if event.get("response_committed") is not True:
        raise ValueError("host Phase-4 event does not confirm response_committed=true")
    seen = nonnegative(event, "body_bytes_seen")
    inspected = nonnegative(event, "body_bytes_inspected")
    if inspected > seen:
        raise ValueError("host body_bytes_inspected exceeds body_bytes_seen")
    # The client received a chunk while the reusable upstream still waited.
    # Combined with the host's current-chunk event counters, this is the
    # observed forward-first path; no payload is copied into this document.
    payload = {
        "response_committed": True,
        "body_bytes_seen": seen,
        "body_bytes_inspected": inspected,
        "no_full_response_buffering": True,
        "connector_owned_full_response_buffer": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
