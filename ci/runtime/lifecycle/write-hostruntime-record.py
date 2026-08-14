#!/usr/bin/env python3
"""Project a finalized lifecycle result into a bounded hostruntime record.

This writer is deliberately a projection, not a lifecycle runner.  It never
starts a process and it never treats the presence of a log as proof of a
successful host run.  PASS requires an explicit, boolean proof for every
required lifecycle dimension in the final result.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import tempfile
from typing import Any


STATUS_VALUES = {"PASS", "FAIL", "BLOCKED", "NOT_RUN", "NOT_APPLICABLE"}
SAFE_TOKEN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
REQUIRED = ("process", "config", "readiness", "interaction", "result", "cleanup")


def safe_token(value: object, name: str) -> str:
    if not isinstance(value, str) or not SAFE_TOKEN.fullmatch(value.strip()):
        raise ValueError(f"{name} must be a bounded ASCII token")
    return value.strip()


def optional_token(value: object) -> str | None:
    """Keep optional provenance fields bounded without failing finalization."""

    if not isinstance(value, str):
        return None
    normalized = value.strip()
    return normalized if SAFE_TOKEN.fullmatch(normalized) else None


def load_result(path: Path) -> dict[str, Any]:
    if not path.is_absolute() or path.is_symlink() or not path.is_file():
        raise ValueError("result must be an existing regular file")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("result must be a JSON object")
    return value


def explicit_status(value: object) -> str | None:
    if value is True:
        return "PASS"
    if value is False:
        return "FAIL"
    if not isinstance(value, str):
        return None
    normalized = value.strip().upper().replace("-", "_")
    if normalized in {"PASS", "PASSED", "VERIFIED", "COMPLETE", "TRUE"}:
        return "PASS"
    if normalized in {"FAIL", "FAILED", "FALSE"}:
        return "FAIL"
    if normalized in {"BLOCKED", "NOT_RUN", "NOT_APPLICABLE"}:
        return normalized
    return None


ALIASES = {
    "process": ("host_process_verified", "process_verified", "process_status"),
    "config": ("config_loaded", "configuration_loaded", "config_status"),
    "readiness": ("readiness_verified", "readiness_status"),
    "interaction": ("interaction_verified", "real_interaction", "interaction_status"),
    "result": ("result_verified", "result_status", "evaluation_status"),
    "cleanup": ("cleanup_verified", "cleanup_status"),
}


def evidence_status(result: dict[str, Any]) -> tuple[dict[str, str], str | None]:
    evidence = result.get("hostruntime_evidence")
    if not isinstance(evidence, dict):
        evidence = result.get("evidence")
    if not isinstance(evidence, dict):
        return {}, "missing_evidence_object"
    statuses: dict[str, str] = {}
    for dimension in REQUIRED:
        value = next((evidence[name] for name in ALIASES[dimension] if name in evidence), None)
        status = explicit_status(value)
        if status is None:
            return statuses, f"missing_evidence:{dimension}"
        statuses[dimension] = status
        if status != "PASS":
            return statuses, f"{dimension}:{status}"
    return statuses, None


def project(args: argparse.Namespace) -> dict[str, Any]:
    result = load_result(Path(args.result))
    # The finalizer's result may contain established, payload-free metadata
    # such as ``request_body_verified`` or ``body_payload_absent_from_events``.
    # Project only the allowlisted fields below; never reject the whole source
    # object and never copy arbitrary source keys into this record.
    connector = safe_token(args.connector, "connector")
    profile = safe_token(args.profile, "profile")
    source_status = explicit_status(result.get("status"))
    statuses, reason = evidence_status(result)
    if source_status == "FAIL" and reason is not None and (
        reason.startswith("missing_") or reason.endswith(":BLOCKED") or reason.endswith(":NOT_RUN")
    ):
        # A source failure without a complete host proof is an evidence gap,
        # not a connector/product failure attributable to this projection.
        final_status = "BLOCKED"
        reason = f"incomplete_hostruntime_evidence:{reason}"
    elif source_status in {"FAIL", "NOT_RUN", "NOT_APPLICABLE"}:
        final_status = source_status
        reason = f"source_result:{source_status}"
    elif source_status != "PASS":
        final_status = "BLOCKED"
        reason = "source_result_status_missing_or_not_pass"
    elif reason is None:
        final_status = "PASS"
        reason = "all_required_hostruntime_evidence_verified"
    elif reason.split(":", 1)[-1] in STATUS_VALUES:
        final_status = "BLOCKED" if "BLOCKED" in reason or "NOT_" in reason else "FAIL"
    else:
        final_status = "BLOCKED"
    record: dict[str, Any] = {
        "schema_version": "hostruntime-record-v1",
        "connector": connector,
        "profile": profile,
        "status": final_status,
        "reason": reason,
        "evidence": {name: statuses.get(name, "NOT_RUN") for name in REQUIRED},
        "runtime_lock_id": optional_token(args.runtime_lock_id),
        "expected_version": optional_token(args.expected_version),
        "actual_version": optional_token(args.actual_version),
        "timestamp": args.timestamp or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }
    return record


def atomic_write(path: Path, text: str) -> None:
    if not path.is_absolute() or path.is_symlink():
        raise ValueError("output must be an absolute non-symlink path")
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with open(descriptor, "w", encoding="utf-8", closefd=True) as handle:
            handle.write(text)
        Path(temporary).chmod(0o600)
        Path(temporary).replace(path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--summary")
    parser.add_argument("--connector", required=True)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--runtime-lock-id")
    parser.add_argument("--expected-version")
    parser.add_argument("--actual-version")
    parser.add_argument("--timestamp")
    args = parser.parse_args(argv)
    try:
        record = project(args)
        serialized = json.dumps(record, indent=2, sort_keys=True) + "\n"
        atomic_write(Path(args.output), serialized)
        if args.summary:
            summary = (f"status={record['status']}\nconnector={record['connector']}\n"
                       f"profile={record['profile']}\nreason={record['reason']}\n")
            atomic_write(Path(args.summary), summary)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
