#!/usr/bin/env python3
"""Write payload-free engine provenance and lifecycle inventory sidecars.

The sidecars describe only transaction identifiers and aggregate counters from
the current raw host run.  They deliberately do not participate in capability
selection or PASS promotion; canonical event validation remains the sole
promotion gate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
from typing import Any, Iterable


FORBIDDEN_EVENT_KEYS = {
    "authorization",
    "cookie",
    "matched_value",
    "matched_value_snippet",
    "request_body",
    "response_body",
    "rule_message",
    "snippet",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ensure_safe_directory(path: Path) -> None:
    if not path.is_absolute():
        raise ValueError("output directory must be absolute")
    for candidate in (path, *path.parents):
        if candidate.exists() and candidate.is_symlink():
            raise ValueError(f"output directory contains a symlink: {candidate}")
        if candidate == candidate.parent:
            break
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    if path.is_symlink() or not path.is_dir():
        raise ValueError(f"output directory is not a real directory: {path}")


def atomic_write(path: Path, payload: bytes) -> None:
    if path.exists() and path.is_symlink():
        raise ValueError(f"refusing to replace symlink artifact: {path}")
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, 0o600)
        os.replace(temporary, path)
    finally:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load source result {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"source result must be an object: {path}")
    return value


def load_events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise ValueError(f"cannot load source events {path}: {exc}") from exc
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"source events line {number} is not JSON: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"source events line {number} must be an object")
        forbidden = sorted(FORBIDDEN_EVENT_KEYS.intersection(value))
        if forbidden:
            raise ValueError(
                f"source events line {number} contains forbidden payload metadata: "
                + ", ".join(forbidden)
            )
        events.append(value)
    return events


def transaction_ids(source: dict[str, Any], events: Iterable[dict[str, Any]]) -> list[str]:
    identifiers: set[str] = set()
    raw_ids = source.get("transaction_ids", [])
    if not isinstance(raw_ids, list):
        raise ValueError("source result transaction_ids must be a list")
    for value in raw_ids:
        identifier = str(value).strip()
        if identifier:
            identifiers.add(identifier)
    for event in events:
        identifier = str(event.get("transaction_id") or "").strip()
        if identifier:
            identifiers.add(identifier)
    return sorted(identifiers)


def phase_number(value: object) -> int | None:
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    text = str(value or "").strip().lower()
    aliases = {
        "request_headers": 1,
        "request_body": 2,
        "response_headers": 3,
        "response_body": 4,
    }
    if text in aliases:
        return aliases[text]
    try:
        return int(text)
    except ValueError:
        return None


def unique_event_signature(event: dict[str, Any]) -> tuple[str, str, str, str, str, str]:
    return tuple(
        str(event.get(name) or "")
        for name in (
            "transaction_id",
            "phase",
            "rule_id",
            "requested_action",
            "actual_action",
            "status",
        )
    )


def engine_error_event(event: dict[str, Any]) -> bool:
    values = " ".join(
        str(event.get(name) or "").lower()
        for name in ("event", "message_id", "status", "actual_action", "transport_result")
    )
    return "engine_error" in values or "adapter_error" in values or "host_filter_error" in values


def build_artifacts(
    *,
    connector: str,
    source: dict[str, Any],
    events: list[dict[str, Any]],
    libmodsecurity_version: str,
    library_sha256: str,
    ruleset_sha256: str,
    stage_exit_code: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    identifiers = transaction_ids(source, events)
    unique_events = {unique_event_signature(event) for event in events}
    phase2_transactions = {
        str(event.get("transaction_id"))
        for event in events
        if event.get("transaction_id") and phase_number(event.get("phase")) == 2
    }
    phase4_transactions = {
        str(event.get("transaction_id"))
        for event in events
        if event.get("transaction_id") and phase_number(event.get("phase")) == 4
    }
    abort_transactions = {
        str(event.get("transaction_id"))
        for event in events
        if event.get("transaction_id") and str(event.get("actual_action") or "") == "abort_connection"
    }
    error_signatures = {
        unique_event_signature(event) for event in events if engine_error_event(event)
    }
    accounting_scope = "unique transaction IDs in the current raw host result and normalized engine events"
    counts = {
        "schema_version": 1,
        "connector": connector,
        "accounting_scope": accounting_scope,
        "transaction_ids": identifiers,
        "transactions_observed": len(identifiers),
        "unique_engine_events_observed": len(unique_events),
        "stage_exit_code": stage_exit_code,
    }
    lifecycle = {
        "schema_version": 1,
        "connector": connector,
        "accounting_scope": accounting_scope,
        "counter_basis": (
            "A successful host stage and each unique transaction ID in the current "
            "raw result/event stream; sidecar counters are non-promoting inventory."
        ),
        "transactions_started": len(identifiers),
        "transactions_finished": len(identifiers),
        "transactions_destroyed": len(identifiers),
        "request_body_finishes": len(phase2_transactions),
        "response_body_finishes": len(phase4_transactions),
        "interventions_seen": len(unique_events),
        "intentional_aborts": len(abort_transactions),
        "unexpected_engine_errors": len(error_signatures),
        "stage_exit_code": stage_exit_code,
        "engine_version": libmodsecurity_version,
        "engine_library_sha256": library_sha256,
        "ruleset_sha256": ruleset_sha256,
    }
    return counts, lifecycle


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--connector", required=True)
    parser.add_argument("--source-result", required=True)
    parser.add_argument("--source-events", required=True)
    parser.add_argument("--rules-file", required=True)
    parser.add_argument("--libmodsecurity-version", required=True)
    parser.add_argument("--libmodsecurity-library", required=True)
    parser.add_argument("--stage-exit-code", required=True, type=int)
    parser.add_argument("--output-dir", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.stage_exit_code != 0:
        raise ValueError("engine lifecycle sidecars require a successful host stage")
    source_path = Path(args.source_result)
    events_path = Path(args.source_events)
    rules_path = Path(args.rules_file)
    library_path = Path(args.libmodsecurity_library)
    for label, path in (("source result", source_path), ("source events", events_path), ("rules", rules_path)):
        if not path.is_file() or path.is_symlink():
            raise ValueError(f"{label} must be a regular file: {path}")
    # The managed libmodsecurity prefix intentionally exposes the conventional
    # SONAME symlink (libmodsecurity.so). Hash its regular resolved target;
    # this input never becomes a canonical artifact path.
    if not library_path.is_file():
        raise ValueError(f"library must be a regular file: {library_path}")
    version = str(args.libmodsecurity_version).strip()
    if not version or version == "not_provisioned":
        raise ValueError("libmodsecurity version must be concrete")
    output_dir = Path(args.output_dir)
    ensure_safe_directory(output_dir)
    source = load_json(source_path)
    events = load_events(events_path)
    library_sha256 = sha256_file(library_path)
    ruleset_sha256 = sha256_file(rules_path)
    counts, lifecycle = build_artifacts(
        connector=args.connector,
        source=source,
        events=events,
        libmodsecurity_version=version,
        library_sha256=library_sha256,
        ruleset_sha256=ruleset_sha256,
        stage_exit_code=args.stage_exit_code,
    )
    atomic_write(output_dir / "engine-version.txt", f"{version}\n".encode("utf-8"))
    atomic_write(output_dir / "engine-library-sha256.txt", f"{library_sha256}\n".encode("ascii"))
    atomic_write(output_dir / "ruleset-sha256.txt", f"{ruleset_sha256}\n".encode("ascii"))
    atomic_write(
        output_dir / "transaction-counts.json",
        (json.dumps(counts, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    )
    atomic_write(
        output_dir / "lifecycle-counters.json",
        (json.dumps(lifecycle, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        print(f"engine-lifecycle-artifacts: {exc}", file=sys.stderr)
        raise SystemExit(1)
