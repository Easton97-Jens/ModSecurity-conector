#!/usr/bin/env python3
"""Normalize real host-runner observations for the canonical evidence writer.

This is a host-harness adapter, not the canonical result writer.  It reads
only explicit status, rule, transaction, and event metadata and never copies
request or response payloads into its output.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any


CORE_CASES = {"allow_without_marker": 200, "deny_header_marker_403": 403}
FORBIDDEN_EVENT_KEYS = {
    "authorization",
    "body_payload",
    "body_snippet",
    "cookie",
    "cookies",
    "password",
    "matched_value",
    "matched_value_snippet",
    "request_body",
    "response_body",
    "intervention_log",
    "rule_message",
    "secret",
}
APPROVED_RAW_EVENT_KEYS = {
    "action",
    "actual_action",
    "anomaly_score",
    "audit_log_path",
    "body_started",
    "body_bytes_seen",
    "body_bytes_inspected",
    "client_first_byte_received",
    "first_byte_before_response_end",
    "first_chunk_size",
    "upstream_paused",
    "upstream_eos_sent_at_first_byte",
    "upstream_response_finished_at_first_byte",
    "upstream_response_complete_at_first_byte",
    "no_full_response_buffering",
    "response_body_size",
    "body_truncated",
    "client_ip",
    "connection_aborted",
    "connector",
    "content_type",
    "decision",
    "disruptive",
    "event",
    "event_hash",
    "event_truncated",
    "expected_status",
    "headers_sent",
    "header_sent",
    "http_default_message",
    "http_reason_phrase",
    "http_status",
    "haproxy_log_path",
    "intervention_status",
    "intervention",
    "late_intervention",
    "level",
    "live_executed",
    "message",
    "message_id",
    "method",
    "mode",
    "modsecurity_processed",
    "modsecurity_rule_id",
    "observed_status",
    "original_http_status",
    "phase",
    "previous_event_hash",
    "reason",
    "redacted",
    "reason_code",
    "redirect_present",
    "request_id",
    "request_body_seen",
    "request_headers_seen",
    "requested_action",
    "wanted_action",
    "upstream_status",
    "client_status",
    "response_body_seen",
    "response_committed",
    "strict_abort",
    "response_headers_seen",
    "response_started",
    "result",
    "rule_id",
    "sequence",
    "status",
    "spoa_log_path",
    "timestamp",
    "transaction_id",
    "truncated",
    "tx_id",
    "uri",
    "variant",
    "visible_http_status",
    "waf_status",
    "transport_result",
    "observed_transport_result",
    "runtime_mode",
    "case",
}
BODY_SENTINELS = (
    "no-crs-request-body-marker",
    "no-crs-response-body-marker",
)
MAX_METADATA_LENGTH = {
    "connector": 64,
    "transaction_id": 256,
    "status": 64,
    "content_type": 256,
}
REQUESTED_ACTIONS = {"deny", "redirect", "drop", "log_only", "abort_connection"}
ACTUAL_ACTIONS = {"deny", "redirect", "log_only", "abort_connection"}
TRANSPORT_RESULTS = {"http_status", "log_only", "connection_aborted", "not_observable"}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON source is not an object: {path}")
    return value


def catalog_runner_case_path(catalog_root: Path, runner_case: object) -> Path:
    """Resolve one catalog-owned runner case without accepting path aliases."""
    if not isinstance(runner_case, str) or not runner_case:
        raise ValueError("catalog runner_case must be a non-empty string")
    if "\\" in runner_case:
        raise ValueError(f"catalog runner_case must use POSIX separators: {runner_case!r}")
    parts = runner_case.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ValueError(f"catalog runner_case contains an unsafe path component: {runner_case!r}")
    candidate = (catalog_root / runner_case).resolve(strict=True)
    try:
        candidate.relative_to(catalog_root)
    except ValueError as exc:
        raise ValueError(f"catalog runner_case escapes its catalog root: {runner_case!r}") from exc
    if not candidate.is_file():
        raise ValueError(f"catalog runner_case is not a regular file: {runner_case!r}")
    return candidate


def catalog_contract(
    path: Path,
) -> tuple[
    dict[str, tuple[int | None, str | None, int | None]],
    dict[Path, str],
]:
    catalog = load_json(path)
    cases = catalog.get("cases")
    if not isinstance(cases, list):
        raise ValueError(f"catalog cases are missing: {path}")
    catalog_root = path.resolve(strict=True).parent
    expectations: dict[str, tuple[int | None, str | None, int | None]] = {}
    runner_case_index: dict[Path, str] = {}
    for case in cases:
        if not isinstance(case, dict) or not case.get("case_id"):
            continue
        case_id = str(case["case_id"])
        expected_status = scalar_int(case.get("expected_status"))
        expected_rule_id = case.get("expected_rule_id")
        expectations[case_id] = (
            expected_status,
            str(expected_rule_id) if expected_rule_id not in (None, "") else None,
            scalar_int(case.get("phase")),
        )
        runner_case = case.get("runner_case")
        if runner_case in (None, ""):
            continue
        runner_path = catalog_runner_case_path(catalog_root, runner_case)
        existing = runner_case_index.get(runner_path)
        if existing is not None:
            raise ValueError(
                f"catalog runner_case is not unique: {runner_case!r} maps to "
                f"both {existing!r} and {case_id!r}"
            )
        runner_case_index[runner_path] = case_id
    return expectations, runner_case_index


def catalog_expectations(path: Path) -> dict[str, tuple[int | None, str | None, int | None]]:
    return catalog_contract(path)[0]


def catalog_case_id_from_row(
    row: dict[str, Any], runner_case_index: dict[Path, str] | None
) -> str | None:
    """Match a host result to one catalog runner_case by exact resolved path."""
    if not runner_case_index:
        return None
    raw_path = row.get("path")
    if not isinstance(raw_path, str) or not raw_path:
        return None
    try:
        candidate = Path(raw_path).resolve(strict=True)
    except OSError:
        return None
    return runner_case_index.get(candidate)


def observed_case_id(
    row: dict[str, Any],
    expectations: dict[str, tuple[Any, ...]],
    runner_case_index: dict[Path, str] | None,
) -> str:
    explicit = str(row.get("case_id") or "")
    from_runner_case = catalog_case_id_from_row(row, runner_case_index)
    if explicit and from_runner_case and explicit != from_runner_case:
        raise ValueError(
            f"source result case_id {explicit!r} conflicts with catalog runner_case "
            f"mapping {from_runner_case!r}"
        )
    if explicit in expectations:
        return explicit
    if from_runner_case is not None:
        return from_runner_case
    return str(row.get("name") or row.get("case") or "")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if not path.is_file():
        return records
    for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"JSONL record is not an object: {path}:{number}")
        records.append(value)
    return records


def scalar_int(value: Any) -> int | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def scalar_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, int) and value in {0, 1}:
        return bool(value)
    if isinstance(value, str):
        normalized = value.strip().casefold()
        if normalized in {"true", "1"}:
            return True
        if normalized in {"false", "0"}:
            return False
    return None


def parse_key_value_text(path: Path) -> dict[str, Any]:
    values: dict[str, Any] = {}
    if not path.is_file():
        return values
    text = path.read_text(encoding="utf-8", errors="replace")
    for line in text.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            if re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", key.strip()):
                values[key.strip()] = value.strip()
    match = re.search(r"\bPASS\b.*\bbaseline=(\d+)\b.*\bblocked=(\d+)\b", text)
    if match:
        values.setdefault("status", "PASS")
        values.setdefault("allowed_request_status", int(match.group(1)))
        values.setdefault("blocked_request_status", int(match.group(2)))
    return values


def nested_forbidden_key(value: Any) -> str | None:
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).strip().lower().replace("-", "_")
            if normalized in FORBIDDEN_EVENT_KEYS:
                return str(key)
            found = nested_forbidden_key(child)
            if found:
                return found
    elif isinstance(value, list):
        for child in value:
            found = nested_forbidden_key(child)
            if found:
                return found
    return None


def nested_unapproved_event_key(value: Any) -> str | None:
    """Reject raw event schemas that could hide payload under a new field.

    The canonical event is an allow-listed projection, so silently dropping an
    unknown raw field would make the payload-absence claim impossible to
    establish.  Raw producers must extend this reviewed list deliberately.
    """
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).strip().lower().replace("-", "_")
            if normalized not in APPROVED_RAW_EVENT_KEYS:
                return str(key)
            found = nested_unapproved_event_key(child)
            if found:
                return found
    elif isinstance(value, list):
        for child in value:
            found = nested_unapproved_event_key(child)
            if found:
                return found
    return None


def nested_forbidden_value(value: Any) -> str | None:
    if isinstance(value, dict):
        for child in value.values():
            found = nested_forbidden_value(child)
            if found:
                return found
    elif isinstance(value, list):
        for child in value:
            found = nested_forbidden_value(child)
            if found:
                return found
    elif isinstance(value, str):
        lowered = value.casefold()
        for sentinel in BODY_SENTINELS:
            if sentinel in lowered:
                return sentinel
    return None


def safe_metadata_value(target: str, value: Any) -> Any | None:
    if target in {
        "rule_id",
        "http_status",
        "original_http_status",
        "visible_http_status",
    }:
        return scalar_int(value)
    if target in {"first_chunk_size", "body_bytes_seen", "body_bytes_inspected"}:
        numeric = scalar_int(value)
        return numeric if numeric is not None and numeric >= 0 else None
    if target == "phase":
        numeric = scalar_int(value)
        if numeric is not None:
            return numeric
        if isinstance(value, str):
            phase_aliases = {
                "connection": 0,
                "request_headers": 1,
                "request_body": 2,
                "response_headers": 3,
                "response_body": 4,
                "phase1": 1,
                "phase2": 2,
                "phase3": 3,
                "phase4": 4,
            }
            normalized = value.strip().casefold().replace("-", "_")
            if normalized in phase_aliases:
                return phase_aliases[normalized]
        if isinstance(value, str) and re.fullmatch(r"[A-Za-z0-9_-]{1,32}", value):
            return value
        return None
    if target in {
        "truncated",
        "late_intervention",
        "headers_sent",
        "body_started",
        "connection_aborted",
        "response_committed",
        "client_first_byte_received",
        "first_byte_before_response_end",
        "upstream_paused",
        "upstream_eos_sent_at_first_byte",
        "upstream_response_finished_at_first_byte",
        "no_full_response_buffering",
    }:
        return scalar_bool(value)
    if target in {"requested_action", "actual_action"}:
        normalized = str(value).strip().casefold().replace("-", "_")
        if normalized == "connection_abort":
            normalized = "abort_connection"
        allowed = REQUESTED_ACTIONS if target == "requested_action" else ACTUAL_ACTIONS
        return normalized if normalized in allowed else None
    if target == "transport_result":
        normalized = str(value).strip().casefold().replace("-", "_")
        if normalized == "connection_abort":
            normalized = "connection_aborted"
        return normalized if normalized in TRANSPORT_RESULTS else None
    if not isinstance(value, (str, int)) or isinstance(value, bool):
        return None
    text = "".join(character for character in str(value) if character >= " " and character != "\x7f")
    return text[: MAX_METADATA_LENGTH.get(target, 256)] or None


def sanitized_event(record: dict[str, Any]) -> dict[str, Any]:
    """Keep only the metadata allow-list accepted by canonical evidence."""
    output: dict[str, Any] = {}
    aliases = {
        "connector": ("connector",),
        "event": ("event",),
        "message_id": ("message_id",),
        "transaction_id": ("transaction_id", "request_id", "tx_id"),
        "rule_id": ("rule_id", "modsecurity_rule_id"),
        "phase": ("phase",),
        "status": ("status", "decision", "result"),
        "http_status": ("http_status", "waf_status", "intervention_status"),
        "original_http_status": ("original_http_status", "upstream_status"),
        "visible_http_status": ("visible_http_status", "client_status"),
        "requested_action": ("requested_action", "wanted_action"),
        "actual_action": ("actual_action",),
        "late_intervention": ("late_intervention", "intervention"),
        "headers_sent": ("headers_sent", "header_sent"),
        "body_started": ("body_started", "response_body_seen"),
        "connection_aborted": ("connection_aborted", "strict_abort"),
        "response_committed": ("response_committed",),
        "transport_result": ("transport_result", "observed_transport_result"),
        "body_bytes_seen": ("body_bytes_seen",),
        "body_bytes_inspected": ("body_bytes_inspected",),
        "client_first_byte_received": ("client_first_byte_received",),
        "first_chunk_size": ("first_chunk_size",),
        "upstream_paused": ("upstream_paused",),
        "upstream_eos_sent_at_first_byte": ("upstream_eos_sent_at_first_byte",),
        "first_byte_before_response_end": ("first_byte_before_response_end",),
        "upstream_response_finished_at_first_byte": (
            "upstream_response_finished_at_first_byte",
            "upstream_response_complete_at_first_byte",
        ),
        "no_full_response_buffering": ("no_full_response_buffering",),
        "truncated": ("truncated", "event_truncated"),
        "content_type": ("content_type",),
    }
    for target, names in aliases.items():
        for name in names:
            value = record.get(name)
            if value not in (None, ""):
                safe_value = safe_metadata_value(target, value)
                if safe_value is not None:
                    output[target] = safe_value
                    break
    return output


def contained_source_event_path(path: Path, allowed_root: Path) -> Path:
    """Return an absolute source-event path only when it is run-local.

    Native harness summaries contain paths to audit and decision logs.  Those
    paths are evidence inputs, so accepting a path from another run would let
    stale metadata satisfy the current run.  Reject symlinks as well as lexical
    and resolved escapes before reading or removing the file.
    """

    if not path.is_absolute():
        raise ValueError(f"source event path must be absolute: {path}")
    root = Path(os.path.abspath(allowed_root))
    candidate = Path(os.path.abspath(path))
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError(
            f"source event path is outside the allowed run root: {candidate}"
        ) from exc

    current = Path(candidate.anchor)
    for component in candidate.parts[1:]:
        current /= component
        if current.is_symlink():
            raise ValueError(f"source event path contains a symlink: {current}")
        if not current.exists():
            break

    resolved_root = root.resolve(strict=True)
    resolved_candidate = candidate.resolve(strict=False)
    try:
        resolved_candidate.relative_to(resolved_root)
    except ValueError as exc:
        raise ValueError(
            f"resolved source event path is outside the allowed run root: {candidate}"
        ) from exc
    return candidate


def scrub_source_event_paths(
    paths: list[Path], allowed_root: Path, log_path: Path | None = None
) -> list[Path]:
    removed: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        candidate = contained_source_event_path(path, allowed_root)
        if candidate in seen:
            continue
        seen.add(candidate)
        if candidate.is_file():
            candidate.unlink()
            removed.append(candidate)
    if log_path is not None:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        lines = [f"removed_after_allowlist_normalization={path}" for path in removed]
        log_path.write_text("\n".join(lines or ["not_produced"]) + "\n", encoding="utf-8")
    return removed


def audit_event(path: Path, connector: str, http_status: int | None) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    rule_matches = re.findall(r'\[id "(\d+)"\]', text)
    if not rule_matches:
        return None
    transaction_matches = re.findall(r'\[unique_id "([^"\r\n]{1,256})"\]', text)
    phase_match = re.search(r"\(phase\s+(\d+)\)", text, re.IGNORECASE)
    event: dict[str, Any] = {
        "connector": connector,
        "rule_id": int(rule_matches[-1]),
        "phase": int(phase_match.group(1)) if phase_match else 1,
        "status": "blocked" if http_status and http_status >= 400 else "allowed",
    }
    if transaction_matches:
        event["transaction_id"] = transaction_matches[-1]
    if http_status is not None:
        event["http_status"] = http_status
    return event


def runtime_event_records(
    path_value: Any,
    allowed_source_root: Path | None,
    consumed_event_paths: list[Path] | None,
) -> list[dict[str, Any]]:
    """Read an explicitly referenced runtime event stream without widening scope."""
    text = str(path_value or "")
    if not text:
        return []
    path = Path(text)
    if allowed_source_root is not None:
        path = contained_source_event_path(path, allowed_source_root)
    if not path.is_file():
        return []
    if consumed_event_paths is not None:
        consumed_event_paths.append(path)
    return load_jsonl(path)


def first_byte_evidence_record(
    path_value: Any,
    allowed_source_root: Path | None,
) -> dict[str, Any] | None:
    """Read a real-host barrier record without treating it as an event stream.

    The evidence is merged only into an actual Phase-4 event emitted by the
    selected host.  This prevents a direct/synthetic helper invocation from
    manufacturing a Phase-4 rule observation.
    """
    text = str(path_value or "")
    if not text:
        return None
    path = Path(text)
    if allowed_source_root is not None:
        path = contained_source_event_path(path, allowed_source_root)
    if not path.is_file():
        return None
    try:
        value = load_json(path)
    except (OSError, ValueError, json.JSONDecodeError):
        return None
    if (
        value.get("evidence_type") != "synchronized_first_byte"
        or value.get("evidence_origin") != "real_host"
        or value.get("promotion_eligible") is not True
        or value.get("outcome") != "PASS"
        or value.get("body_payload_persisted") is not False
    ):
        return None
    required = (
        "client_first_byte_received",
        "first_byte_before_response_end",
        "first_chunk_size",
        "upstream_paused",
        "upstream_eos_sent_at_first_byte",
        "upstream_response_finished_at_first_byte",
        "response_committed",
        "body_bytes_seen",
        "body_bytes_inspected",
        "no_full_response_buffering",
        "connector_owned_full_response_buffer",
    )
    if any(name not in value for name in required):
        return None
    if (
        value.get("client_first_byte_received") is not True
        or value.get("first_byte_before_response_end") is not True
        or value.get("upstream_paused") is not True
        or value.get("upstream_eos_sent_at_first_byte") is not False
        or value.get("upstream_response_finished_at_first_byte") is not False
        or value.get("response_committed") is not True
        or value.get("no_full_response_buffering") is not True
        or value.get("connector_owned_full_response_buffer") is not False
    ):
        return None
    for name in ("first_chunk_size", "body_bytes_seen", "body_bytes_inspected"):
        number = scalar_int(value.get(name))
        if number is None or number < 0:
            return None
        value[name] = number
    if value["first_chunk_size"] < 1 or value["body_bytes_inspected"] > value["body_bytes_seen"]:
        return None
    return value


def merge_first_byte_evidence(
    records: list[dict[str, Any]], evidence: dict[str, Any] | None
) -> list[dict[str, Any]]:
    """Attach bounded causal metadata only to observed Phase-4 host events."""
    if evidence is None:
        return records
    fields = (
        "client_first_byte_received",
        "first_byte_before_response_end",
        "first_chunk_size",
        "upstream_paused",
        "upstream_eos_sent_at_first_byte",
        "upstream_response_finished_at_first_byte",
        "response_committed",
        "body_bytes_seen",
        "body_bytes_inspected",
        "no_full_response_buffering",
    )
    merged: list[dict[str, Any]] = []
    for record in records:
        candidate = dict(record)
        phase = safe_metadata_value("phase", candidate.get("phase"))
        if phase == 4:
            for field in fields:
                # The barrier observation is authoritative for its causal
                # fields.  Host counters must agree rather than be replaced.
                if field in {"body_bytes_seen", "body_bytes_inspected"} and field in candidate:
                    existing = scalar_int(candidate.get(field))
                    if existing is not None and existing != evidence[field]:
                        candidate["first_byte_evidence_counter_mismatch"] = True
                        continue
                candidate[field] = evidence[field]
        merged.append(candidate)
    return merged


def canonical_semantics(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Project only producer-observed Phase-4 metadata.

    This intentionally does not fill defaults.  A missing runtime value must
    remain missing so the framework can fail a claimed semantic case instead
    of manufacturing evidence from its catalog or capability manifest.
    """
    fields = {
        "http_status",
        "original_http_status",
        "visible_http_status",
        "requested_action",
        "actual_action",
        "late_intervention",
        "headers_sent",
        "body_started",
        "connection_aborted",
        "response_committed",
        "transport_result",
        "body_bytes_seen",
        "body_bytes_inspected",
        "client_first_byte_received",
        "first_chunk_size",
        "upstream_paused",
        "upstream_eos_sent_at_first_byte",
        "first_byte_before_response_end",
        "upstream_response_finished_at_first_byte",
        "no_full_response_buffering",
    }
    output: dict[str, Any] = {}
    for record in records:
        normalized = sanitized_event(record)
        for field in fields:
            if field in normalized:
                output[field] = normalized[field]
    return output


def event_evidence(
    paths: list[Path], expected_rule_id: str, derived_records: list[dict[str, Any]]
) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    invalid: list[str] = []
    forbidden: list[str] = []
    for index, record in enumerate(derived_records):
        forbidden_key = nested_forbidden_key(record)
        unapproved_key = nested_unapproved_event_key(record)
        forbidden_value = nested_forbidden_value(record)
        if forbidden_key:
            forbidden.append(f"derived-event:{index + 1}:{forbidden_key}")
            continue
        if unapproved_key:
            forbidden.append(f"derived-event:{index + 1}:unapproved-field:{unapproved_key}")
            continue
        if forbidden_value:
            forbidden.append(f"derived-event:{index + 1}:payload-sentinel")
            continue
        records.append(sanitized_event(record))
    for path in paths:
        try:
            for index, record in enumerate(load_jsonl(path)):
                forbidden_key = nested_forbidden_key(record)
                unapproved_key = nested_unapproved_event_key(record)
                forbidden_value = nested_forbidden_value(record)
                if forbidden_key:
                    forbidden.append(f"{path}:{index + 1}:{forbidden_key}")
                    continue
                if unapproved_key:
                    forbidden.append(f"{path}:{index + 1}:unapproved-field:{unapproved_key}")
                    continue
                if forbidden_value:
                    forbidden.append(f"{path}:{index + 1}:payload-sentinel")
                    continue
                records.append(sanitized_event(record))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            invalid.append(f"{path}: {exc}")

    observed_rule_ids: set[str] = set()
    transaction_ids: set[str] = set()
    connector_seen = False
    phase_seen = False
    status_seen = False
    for record in records:
        connector_seen = connector_seen or bool(record.get("connector"))
        phase_seen = phase_seen or record.get("phase") not in (None, "")
        status_seen = status_seen or record.get("status") not in (None, "")
        rule_id = record.get("rule_id")
        if rule_id not in (None, ""):
            observed_rule_ids.add(str(rule_id))
        transaction_id = record.get("transaction_id")
        if transaction_id not in (None, ""):
            transaction_ids.add(str(transaction_id))
        found = nested_forbidden_key(record)
        if found:
            forbidden.append(found)

    records = [record for record in records if record]
    metadata_verified = bool(
        records
        and connector_seen
        and transaction_ids
        and expected_rule_id in observed_rule_ids
        and phase_seen
        and status_seen
        and not invalid
        and not forbidden
    )
    return {
        "body_payload_absent_from_events": bool(records) and not forbidden and not invalid,
        "event_metadata_verified": metadata_verified,
        "event_records": len(records),
        "event_validation_errors": invalid,
        "forbidden_event_keys": sorted(set(forbidden)),
        "observed_rule_ids": sorted(observed_rule_ids),
        "transaction_ids": sorted(transaction_ids),
        "records": records,
    }


def case_observations(
    paths: list[Path],
    connector: str,
    expected_rule_id: str,
    expectations: dict[str, tuple[Any, ...]] | None = None,
    allowed_source_root: Path | None = None,
    consumed_event_paths: list[Path] | None = None,
    runner_case_index: dict[Path, str] | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    expectations = expectations or {
        case_id: (status, expected_rule_id if case_id == "deny_header_marker_403" else None)
        for case_id, status in CORE_CASES.items()
    }
    rows: list[dict[str, Any]] = []
    for path in paths:
        rows.extend(load_jsonl(path))
    observations: list[dict[str, Any]] = []
    derived_events: list[dict[str, Any]] = []
    for row in rows:
        decision_text = str(row.get("decision_log_path") or row.get("decision_log") or "")
        decision_path = Path(decision_text)
        if decision_text and allowed_source_root is not None:
            decision_path = contained_source_event_path(decision_path, allowed_source_root)
        if decision_path.is_file() and consumed_event_paths is not None:
            consumed_event_paths.append(decision_path)
        audit_text = str(row.get("audit_log_path") or "")
        audit_path = Path(audit_text)
        if audit_text and allowed_source_root is not None:
            audit_path = contained_source_event_path(audit_path, allowed_source_root)
        if audit_path.is_file() and consumed_event_paths is not None:
            consumed_event_paths.append(audit_path)

        case_id = observed_case_id(row, expectations, runner_case_index)
        if case_id not in expectations:
            continue
        expectation = expectations[case_id]
        expected_status = scalar_int(expectation[0]) if expectation else None
        case_expected_rule_id = (
            str(expectation[1]) if len(expectation) > 1 and expectation[1] not in (None, "") else None
        )
        expected_phase = scalar_int(expectation[2]) if len(expectation) > 2 else None
        actual = scalar_int(row.get("actual_status", row.get("observed_status")))
        status = str(row.get("status") or row.get("result") or "").upper()
        live = row.get("live_executed", True) is not False
        observed_rule_ids: set[str] = set()
        raw_rule_ids = row.get("observed_rule_ids")
        if isinstance(raw_rule_ids, list):
            observed_rule_ids.update(str(value) for value in raw_rule_ids)
        for key in ("rule_id", "modsecurity_rule_id"):
            if row.get(key) not in (None, ""):
                observed_rule_ids.add(str(row[key]))
        runtime_records: list[dict[str, Any]] = []
        if decision_path.is_file():
            runtime_records.extend(load_jsonl(decision_path))
        for key in ("connector_phase4_log_path", "phase4_log_path"):
            runtime_records.extend(runtime_event_records(
                row.get(key), allowed_source_root, consumed_event_paths))
        runtime_records = merge_first_byte_evidence(
            runtime_records,
            first_byte_evidence_record(
                row.get("first_byte_evidence_path"), allowed_source_root
            ),
        )
        for record in runtime_records:
            event = sanitized_event(record)
            derived_events.append(record)
            if event.get("rule_id") not in (None, ""):
                observed_rule_ids.add(str(event["rule_id"]))
        phase4_case = expected_phase == 4 or case_id.startswith("phase4_")
        structured_runtime_case = expected_phase in {3, 4}
        # An audit log can corroborate the older request-path cases, but it
        # is not a Phase-4 producer event.  In particular it lacks the
        # canonical event/message identity that the Framework requires for a
        # response-body observation.  Phase-4 cases therefore require the
        # connector's structured Phase-4 log above; absent that log, leave
        # the case unverified instead of manufacturing a malformed event.
        if not phase4_case:
            event = audit_event(audit_path, connector, actual)
            if event:
                derived_events.append(event)
                observed_rule_ids.add(str(event["rule_id"]))
        passed = status == "PASS" and live
        if not phase4_case and expected_status is not None:
            passed = passed and actual == expected_status
        if case_expected_rule_id is not None:
            passed = passed and case_expected_rule_id in observed_rule_ids
        canonical_records = [sanitized_event(record) for record in runtime_records]
        if structured_runtime_case:
            passed = passed and any(
                record.get("phase") == expected_phase for record in canonical_records
            )
        semantic = canonical_semantics([row, *runtime_records])
        transaction_ids = {
            str(record["transaction_id"])
            for record in canonical_records
            if record.get("transaction_id") not in (None, "")
        }
        observed_event_fields = sorted({
            field for record in canonical_records for field in record
        })
        event_metadata_verified = bool(
            canonical_records
            and transaction_ids
            and case_expected_rule_id is not None
            and case_expected_rule_id in observed_rule_ids
            and (
                not structured_runtime_case
                or any(record.get("phase") == expected_phase for record in canonical_records)
            )
        )
        observations.append(
            {
                "case_id": case_id,
                "actual_status": actual,
                "expected_status": expected_status,
                "live_executed": live,
                "observed_rule_ids": sorted(observed_rule_ids),
                "transaction_ids": sorted(transaction_ids),
                "observed_event_fields": observed_event_fields,
                "event_metadata_verified": event_metadata_verified,
                "source_status": status,
                "status": "PASS" if passed else "FAIL",
                **semantic,
            }
        )
    return observations, derived_events


def source_objects(paths: list[Path]) -> list[dict[str, Any]]:
    objects: list[dict[str, Any]] = []
    for path in paths:
        if not path.is_file():
            continue
        if path.suffix == ".json":
            objects.append(load_json(path))
        else:
            objects.append(parse_key_value_text(path))
    return objects


def first_status(objects: list[dict[str, Any]], key: str) -> int | None:
    for value in objects:
        observed = scalar_int(value.get(key))
        if observed is not None:
            return observed
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--connector", required=True)
    parser.add_argument("--stage-rc", required=True, type=int)
    parser.add_argument("--expected-rule-id", default="1100001")
    parser.add_argument(
        "--catalog",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "modules/ModSecurity-test-Framework/tests/cases/no-crs-baseline/catalog.json",
    )
    parser.add_argument("--source-result", action="append", type=Path, default=[])
    parser.add_argument("--source-results-jsonl", action="append", type=Path, default=[])
    parser.add_argument("--source-events", action="append", type=Path, default=[])
    parser.add_argument("--allowed-source-root", type=Path)
    parser.add_argument("--scrub-source-events", action="store_true")
    parser.add_argument("--source-event-scrub-log", type=Path)
    parser.add_argument("--events-output", type=Path)
    parser.add_argument("--stdout", type=Path)
    parser.add_argument("--stderr", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    objects = source_objects(args.source_result)
    if args.stdout:
        objects.append(parse_key_value_text(args.stdout))
    consumed_event_paths: list[Path] = []
    source_events = list(args.source_events)
    if args.allowed_source_root is not None:
        source_events = [
            contained_source_event_path(path, args.allowed_source_root)
            for path in source_events
        ]
    expectations, runner_case_index = catalog_contract(args.catalog)
    cases, derived_events = case_observations(
        args.source_results_jsonl,
        args.connector,
        args.expected_rule_id,
        expectations,
        args.allowed_source_root,
        consumed_event_paths,
        runner_case_index,
    )
    events = event_evidence(source_events, args.expected_rule_id, derived_events)

    allowed = first_status(objects, "allowed_request_status")
    blocked = first_status(objects, "blocked_request_status")
    if allowed is None:
        allowed = first_status(objects, "baseline_status")
    if blocked is None:
        blocked = first_status(objects, "block_status")
    for case in cases:
        if case["case_id"] == "allow_without_marker":
            allowed = scalar_int(case["actual_status"])
        elif case["case_id"] == "deny_header_marker_403":
            blocked = scalar_int(case["actual_status"])

    object_rule_ids = {
        str(value)
        for obj in objects
        for value in (
            obj.get("modsecurity_rule_id"),
            obj.get("rule_id"),
        )
        if value not in (None, "")
    }
    observed_rule_ids = sorted(object_rule_ids | set(events["observed_rule_ids"]))
    explicit_runtime = allowed is not None or blocked is not None or bool(cases)
    core_status_ok = allowed == 200 and blocked == 403

    if args.stage_rc == 77:
        status = "FAIL" if explicit_runtime else "BLOCKED"
    elif args.stage_rc != 0:
        status = "FAIL"
    elif (
        core_status_ok
        and args.expected_rule_id in observed_rule_ids
        and events["event_metadata_verified"]
        and events["body_payload_absent_from_events"]
    ):
        status = "PASS"
    else:
        status = "FAIL"

    payload = {
        "schema_version": 1,
        "connector": args.connector,
        "status": status,
        "stage_exit_code": args.stage_rc,
        "started": explicit_runtime,
        "requests_sent": explicit_runtime,
        "allowed_request_status": allowed,
        "blocked_request_status": blocked,
        "observed_rule_ids": observed_rule_ids,
        "transaction_ids": events["transaction_ids"],
        "request_headers_verified": core_status_ok,
        "request_body_verified": False,
        "response_headers_verified": False,
        "response_body_verified": False,
        "late_intervention_verified": False,
        "event_metadata_verified": events["event_metadata_verified"],
        "body_payload_absent_from_events": events["body_payload_absent_from_events"],
        "cases": cases,
        "event_records": events["event_records"],
        "event_validation_errors": events["event_validation_errors"],
        "forbidden_event_keys": events["forbidden_event_keys"],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.events_output:
        args.events_output.parent.mkdir(parents=True, exist_ok=True)
        with args.events_output.open("w", encoding="utf-8") as handle:
            for record in events["records"]:
                handle.write(json.dumps(record, sort_keys=True) + "\n")
    if args.scrub_source_events:
        if args.allowed_source_root is None:
            raise ValueError("--scrub-source-events requires --allowed-source-root")
        scrub_source_event_paths(
            [*source_events, *consumed_event_paths],
            args.allowed_source_root,
            args.source_event_scrub_log,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
