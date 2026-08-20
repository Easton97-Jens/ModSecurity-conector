#!/usr/bin/env python3
"""Execute a bounded no-CRS/with-MRTS plan against a real host endpoint."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import secrets
import ssl
import struct
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, NoReturn

MAX_BYTES = 1_048_576
SHA256_RE = set("0123456789abcdef")
FNV64_OFFSET = 14_695_981_039_346_656_037
FNV64_PRIME = 1_099_511_628_211
FNV64_MASK = (1 << 64) - 1
RULE_MATCH_INTEGRATION_MODES = {
    "envoy": "ext_proc",
    "traefik": "native-traefik-middleware",
    "lighttpd": "patched-native-lighttpd",
}
RULE_MATCH_EVENT_KEYS = frozenset({
    "timestamp", "level", "message_id", "message", "event", "connector",
    "integration_mode", "transaction_id", "phase", "status", "action",
    "requested_action", "actual_action", "http_status", "original_http_status",
    "visible_http_status", "transport_result", "http_reason_phrase",
    "http_default_message", "rule_id", "reason", "method", "uri", "client_ip",
    "content_type", "body_bytes_seen", "body_bytes_inspected", "late_intervention",
    "response_started", "response_committed", "headers_sent", "body_started",
    "body_truncated", "connection_aborted", "client_disconnected",
    "upstream_disconnected", "cancelled", "eos_seen", "redacted", "truncated",
    "sequence", "previous_event_hash", "event_hash",
})
RULE_MATCH_FALSE_FIELDS = frozenset({
    "late_intervention", "response_started", "response_committed", "headers_sent",
    "body_started", "body_truncated", "connection_aborted", "client_disconnected",
    "upstream_disconnected", "cancelled", "eos_seen", "redacted", "truncated",
})
RULE_MATCH_ZERO_FIELDS = frozenset({
    "http_status", "original_http_status", "visible_http_status",
    "body_bytes_seen", "body_bytes_inspected",
})
RULE_MATCH_EMPTY_FIELDS = frozenset({
    "message", "transport_result", "http_reason_phrase", "http_default_message",
    "reason", "client_ip", "content_type",
})
RULE_MATCH_PHASE_VALUES = {
    "request_headers": 2,
    "request_body": 3,
    "response_headers": 4,
    "response_body": 5,
    "logging": 6,
}


def fail(message: str) -> NoReturn:
    raise SystemExit(f"FAIL: {message}")


def safe_root(value: str, label: str) -> Path:
    root = Path(value).expanduser()
    if not root.is_absolute() or ".." in root.parts:
        fail(f"{label} must be an absolute traversal-free path")
    component = Path(root.anchor)
    for part in root.parts[1:]:
        component /= part
        if component.exists() and component.is_symlink():
            fail(f"{label} contains a symlink component")
    root.mkdir(mode=0o700, parents=True, exist_ok=True)
    root = root.resolve(strict=True)
    if root.is_symlink() or os.stat(root).st_uid != os.getuid():
        fail(f"{label} is not a private owner-controlled directory")
    os.chmod(root, 0o700)
    return root


def confined(path: str, root: Path, label: str, *, regular: bool = True) -> Path:
    candidate = Path(path)
    if not candidate.is_absolute() or ".." in candidate.parts:
        fail(f"{label} is not absolute and traversal-free")
    try:
        resolved = candidate.resolve(strict=regular)
        if not regular:
            resolved.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        resolved.relative_to(root)
    except (OSError, ValueError) as exc:
        fail(f"{label} escapes its private root: {exc}")
    if candidate.is_symlink() or any(part.is_symlink() for part in candidate.parents if part.exists()):
        fail(f"{label} contains a symlink component")
    if regular and not resolved.is_file():
        fail(f"{label} is not a regular file")
    return resolved


def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            fail(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def required_sha256(value: Any, label: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in SHA256_RE for character in value)
    ):
        fail(f"{label} must be a lowercase SHA-256 digest")
    return value


def load_json(path: Path, expected_sha256: str | None = None) -> Any:
    try:
        data = path.read_bytes()
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"invalid JSON {path}: {exc}")
    if len(data) > MAX_BYTES:
        fail(f"invalid JSON {path}: exceeds bounded size")
    if expected_sha256 is not None:
        expected_sha256 = required_sha256(expected_sha256, "sealed MRTS plan digest")
        if hashlib.sha256(data).hexdigest() != expected_sha256:
            fail("sealed MRTS plan digest does not match the parent-held value")
    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=reject_duplicates)
    except (UnicodeError, json.JSONDecodeError) as exc:
        fail(f"invalid JSON {path}: {exc}")


def validate_sealed_no_crs_plan(
    plan_path: Path,
    runtime_root: Path,
    load_path: Path,
    executor_path: Path,
    plan_sha256: str,
) -> None:
    """Reuse the closed Parent validator instead of substring heuristics.

    The load file necessarily contains an absolute task runtime path.  A
    textual ``"crs"`` search therefore mistakes a legitimate ``no-crs``
    path component for a Core Rule Set reference.  The sealed plan validator
    binds the complete include set byte-for-byte to the pinned MRTS corpus and
    rejects symlinks, foreign rules, altered CRS rule content, and layout
    changes.  Load it only from the trusted sibling Parent source file.
    """
    validator_path = executor_path.with_name("run-no-crs-with-mrts-target.py")
    if validator_path.is_symlink() or not validator_path.is_file():
        fail("sealed MRTS plan validator is unavailable")
    parent_root = executor_path.parents[3]
    framework_root = parent_root / "modules" / "ModSecurity-test-Framework"
    rules_root = runtime_root / "build" / "mrts" / "upstream-config-tests" / "rules"
    try:
        spec = importlib.util.spec_from_file_location("sealed_mrts_plan_validator", validator_path)
        if spec is None or spec.loader is None:
            fail("sealed MRTS plan validator could not be loaded")
        validator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(validator)
        validate = getattr(validator, "validate_sealed_plan")
    except (ImportError, OSError, AttributeError) as exc:
        fail(f"sealed MRTS plan validator could not be loaded: {exc}")
    if not callable(validate):
        fail("sealed MRTS plan validator has no validation entry point")
    validate(plan_path, runtime_root, framework_root, rules_root, load_path, plan_sha256)


def atomic_json(path: Path, value: Any, root: Path) -> None:
    if path.parent != root and root not in path.parents:
        fail("output is outside private runtime root")
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{secrets.token_hex(8)}.tmp")
    data = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    if len(data) > MAX_BYTES:
        fail("result exceeds bounded size")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
        os.chmod(path, 0o600)
    finally:
        try:
            tmp.unlink()
        except FileNotFoundError:
            pass


def bounded_utc_timestamp(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 20
        and value[4:5] == "-"
        and value[7:8] == "-"
        and value[10:11] == "T"
        and value[13:14] == ":"
        and value[16:17] == ":"
        and value[19:20] == "Z"
        and all(character in "0123456789" for character in value[:4] + value[5:7] + value[8:10] + value[11:13] + value[14:16] + value[17:19])
    )


def unsigned_64bit_integer(value: Any) -> bool:
    return type(value) is int and 0 <= value <= FNV64_MASK


def fnv1a64_continue(value: int, payload: bytes) -> int:
    """Match the pinned Common runtime's native FNV-1a byte loop."""

    for byte in payload:
        value ^= byte
        value = (value * FNV64_PRIME) & FNV64_MASK
    return value


def c_string_bytes(value: str | None) -> bytes:
    """Return the byte sequence hashed by Common for a C string.

    The native helper hashes a NULL C string as one NUL byte, exactly like an
    empty string. Rule-match evidence is a fixed metadata-only schema, so the
    decoded UTF-8 JSON fields reproduce the source C strings on the pinned
    Linux x86_64 runtime ABI.
    """

    if value is None:
        return b"\0"
    return value.encode("utf-8") + b"\0"


def hash_c_string(value: int, text: str | None) -> int:
    return fnv1a64_continue(value, c_string_bytes(text))


def require_rule_match_integrity_abi() -> None:
    """Fail closed outside the ABI used by the pinned native event writer."""

    if (
        sys.byteorder != "little"
        or struct.calcsize("=i") != 4
        or struct.calcsize("=Q") != 8
    ):
        fail("rule-match integrity verification requires the pinned Linux x86_64 ABI")


def hash_native_int(value: int) -> bytes:
    try:
        return struct.pack("<i", value)
    except struct.error as exc:
        fail(f"rule-match integrity integer is outside the native range: {exc}")


def hash_native_uint64(value: int) -> bytes:
    try:
        return struct.pack("<Q", value)
    except struct.error as exc:
        fail(f"rule-match integrity uint64 is outside the native range: {exc}")


def rule_match_event_hash(item: dict[str, Any]) -> int:
    """Reconstruct the Common hash for the fixed metadata-only rule event.

    This intentionally verifies only the exact event shape emitted by
    emit_rule_match_events. It does not generalize the non-cryptographic
    native format into a parser for arbitrary Common event records.
    """

    require_rule_match_integrity_abi()
    value = fnv1a64_continue(FNV64_OFFSET, hash_native_uint64(item["previous_event_hash"]))
    for key in (
        "timestamp",
        "level",
        "message_id",
        "event",
        "connector",
        "integration_mode",
    ):
        value = hash_c_string(value, item[key])
    # run_id and transport_case_id are unset by msconnector_event_init() for
    # this target-only record and therefore hash as a single NUL each.
    value = hash_c_string(value, None)
    value = hash_c_string(value, None)
    value = hash_c_string(value, item["transaction_id"])
    value = fnv1a64_continue(value, hash_native_int(RULE_MATCH_PHASE_VALUES[item["phase"]]))
    value = fnv1a64_continue(value, hash_native_int(0))  # MSCONNECTOR_STATUS_OK
    value = hash_c_string(value, item["action"])
    value = hash_c_string(value, item["rule_id"])
    value = hash_c_string(value, item["reason"])
    for key in ("http_status", "original_http_status", "visible_http_status"):
        value = fnv1a64_continue(value, hash_native_int(item[key]))
    value = hash_c_string(value, item["transport_result"])
    # All protocol metadata is unset for a metadata-only rule-match record.
    for _ in range(12):
        value = hash_c_string(value, None)
    for _ in range(4):
        value = fnv1a64_continue(value, hash_native_int(0))
    for key in ("method", "uri", "client_ip"):
        value = hash_c_string(value, item[key])
    value = hash_c_string(value, item["content_type"])
    value = hash_c_string(value, None)  # body.limit_outcome
    for key in ("body_bytes_seen", "body_bytes_inspected"):
        value = fnv1a64_continue(value, hash_native_uint64(item[key]))
    value = fnv1a64_continue(value, hash_native_int(0))  # late_intervention
    value = hash_c_string(value, None)  # late_intervention_mode
    for _ in range(10):
        value = fnv1a64_continue(value, hash_native_int(0))
    for _ in range(3):
        value = hash_c_string(value, None)
    return value


def validate_rule_match_event(
    item: dict[str, Any],
    connector: str,
    integration_mode: str,
    expected_phase: str | None = None,
) -> tuple[str, int]:
    """Validate one exact native rule-match record and return its identity."""

    if set(item) != RULE_MATCH_EVENT_KEYS:
        fail("rule-match event has an unexpected schema")
    required = {
        "level": "info",
        "message_id": "MSCONN_EVENT_RULE_MATCHED",
        "event": "request_rule_match",
        "connector": connector,
        "integration_mode": integration_mode,
        "status": "ok",
        "action": "allow",
        "requested_action": "allow",
        "actual_action": "allow",
        "method": "GET",
    }
    for key, expected in required.items():
        if item.get(key) != expected:
            fail(f"rule-match event has invalid {key}")
    if item.get("phase") not in RULE_MATCH_PHASE_VALUES:
        fail("rule-match event has invalid phase")
    if expected_phase is not None and item.get("phase") != expected_phase:
        fail("rule-match event has invalid phase")
    if not bounded_utc_timestamp(item.get("timestamp")):
        fail("rule-match event has invalid timestamp")
    for key in RULE_MATCH_EMPTY_FIELDS:
        if item.get(key) != "":
            fail(f"rule-match event has nonempty {key}")
    for key in RULE_MATCH_FALSE_FIELDS:
        if item.get(key) is not False:
            fail(f"rule-match event has invalid {key}")
    for key in RULE_MATCH_ZERO_FIELDS:
        if item.get(key) != 0 or type(item.get(key)) is not int:
            fail(f"rule-match event has invalid {key}")
    if (
        type(item.get("sequence")) is not int
        or item["sequence"] <= 0
        or not unsigned_64bit_integer(item.get("previous_event_hash"))
        or not unsigned_64bit_integer(item.get("event_hash"))
        or item["event_hash"] == 0
    ):
        fail("rule-match event has invalid integrity metadata")
    rule_id = item.get("rule_id")
    if (
        not isinstance(rule_id, str)
        or not rule_id
        or len(rule_id) > 12
        or rule_id[0] == "0"
        or any(char not in "0123456789" for char in rule_id)
    ):
        fail("rule-match event has invalid rule_id")
    computed_hash = rule_match_event_hash(item)
    if item["event_hash"] != computed_hash:
        fail("rule-match event hash does not match native integrity data")
    return rule_id, item["event_hash"]


def event_ids(
    event_log: Path,
    correlation_id: str,
    connector: str,
    uri: str,
    expected_phase: str,
    expected_ids: set[str],
    allowed_rule_ids: set[str],
) -> set[str]:
    """Return IDs from the dedicated, metadata-only rule-match record.

    The event log is evidence, not an input language.  Every record is fully
    validated, including its closed phase enum and native integrity chain,
    before case correlation.  Detection cases select only expected-phase
    IDs; an expected ID observed in another phase fails closed, while a
    non-selected ID in another phase is out of profile and may be ignored
    after validation.  Control and bypass cases retain every correlated ID so
    their empty-set oracle can reject any match.  Records for another
    transaction or request remain irrelevant and are ignored.
    """
    integration_mode = RULE_MATCH_INTEGRATION_MODES.get(connector)
    if integration_mode is None:
        fail("rule-match connector is outside the closed profile")
    if expected_phase != "request_body":
        fail("rule-match phase is outside the closed MRTS profile")
    found: set[str] = set()
    previous_event_hash: int | None = None
    if not event_log.exists():
        return found
    if event_log.stat().st_size > MAX_BYTES:
        fail("event log exceeds bounded size")
    for line in event_log.read_text(encoding="utf-8").splitlines():
        if not line:
            fail("event log contains an empty record")
        try:
            item = json.loads(line, object_pairs_hook=reject_duplicates)
        except (UnicodeError, json.JSONDecodeError) as exc:
            fail(f"event log is not duplicate-safe JSONL: {exc}")
        if not isinstance(item, dict):
            fail("event log entries must be JSON objects")
        # Validate the complete native record and chain before correlating it.
        # Phase is intentionally checked against the closed enum here, while
        # the profile-specific expected phase is enforced only for a relevant
        # transaction/URI below. Native adapters emit legitimate records for
        # other phases and those records remain integrity-validated evidence.
        rule_id, event_hash = validate_rule_match_event(
            item, connector, integration_mode
        )
        if previous_event_hash is None:
            if item["previous_event_hash"] != 0:
                fail("first rule-match event does not start a native integrity chain")
        elif item["previous_event_hash"] != previous_event_hash:
            fail("rule-match event does not continue the native integrity chain")
        previous_event_hash = event_hash
        if (
            item.get("transaction_id") != correlation_id
            or item.get("connector") != connector
            or item.get("uri") != uri
        ):
            continue
        if item["phase"] == expected_phase:
            if rule_id not in allowed_rule_ids:
                fail("relevant rule-match event has rule ID outside the pinned corpus")
            if rule_id in found:
                fail("relevant rule-match event duplicates a rule ID")
            found.add(rule_id)
        elif not expected_ids:
            # Control and bypass cases must expose every correlated match to
            # the existing empty-set oracle, regardless of native phase.
            if rule_id in found:
                fail("relevant rule-match event duplicates a rule ID")
            found.add(rule_id)
        elif rule_id in expected_ids:
            # An expected rule observed in another phase is a fail-closed
            # correlation error.  Other fully validated rule IDs in that
            # phase are unrelated to this case and may be ignored.
            fail("relevant rule-match event has invalid phase")
    return found


def require_case_rule_matches(
    case_kind: str,
    case_id: str,
    expected_ids: set[str],
    matched_ids: set[str],
) -> None:
    """Apply the canonical MRTS DetectionOnly oracle.

    Each selected canonical case declares the rule IDs that must be observed,
    while the sealed load file deliberately contains the complete pinned MRTS
    corpus.  A single real request may consequently trigger additional,
    fully-correlated native rules.  Keep every such event in the receipt, but
    require every selected expectation; an extra match cannot replace one.
    """

    if case_kind == "detection" and not expected_ids.issubset(matched_ids):
        fail(
            f"{case_id} rule-match missing expected IDs: "
            f"expected {sorted(expected_ids)}, observed {sorted(matched_ids)}"
        )
    if case_kind in {"control", "bypass"} and matched_ids:
        fail(f"{case_id} unexpectedly matched rules: {sorted(matched_ids)}")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request: urllib.request.Request, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> None:
        raise urllib.error.HTTPError(request.full_url, code, "redirect refused", headers, fp)


def request(url: str, method: str, headers: dict[str, str], timeout: float, context: ssl.SSLContext | None) -> int:
    req = urllib.request.Request(url, method=method, headers=headers)
    handlers: list[Any] = [NoRedirect]
    if context is not None:
        handlers.append(urllib.request.HTTPSHandler(context=context))
    opener = urllib.request.build_opener(*handlers)
    try:
        with opener.open(req, timeout=timeout) as response:
            response.read(MAX_BYTES)
            return int(response.status)
    except urllib.error.HTTPError as exc:
        exc.read(MAX_BYTES)
        return int(exc.code)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector", required=True, choices=("envoy", "traefik", "lighttpd"))
    parser.add_argument("--runtime-root", required=True)
    parser.add_argument("--plan", required=True)
    parser.add_argument("--plan-sha256", required=True)
    parser.add_argument("--load-file", required=True)
    parser.add_argument("--result", required=True)
    parser.add_argument("--event-log", required=True)
    parser.add_argument("--scheme", choices=("http", "https"), default="http")
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", required=True, type=int)
    parser.add_argument("--tls-insecure", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.port <= 65535 or any(ch not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-" for ch in args.host):
        fail("invalid host or port")
    if args.host != "127.0.0.1":
        fail("MRTS runtime endpoint must be 127.0.0.1")
    root = safe_root(args.runtime_root, "runtime root")
    plan_path = confined(args.plan, root, "plan")
    result_path = Path(args.result)
    if not result_path.is_absolute() or ".." in result_path.parts:
        fail("result is not traversal-free")
    result_path = result_path.resolve(strict=False)
    if root not in result_path.parents:
        fail("result escapes runtime root")
    if result_path.exists():
        fail("result already exists; recycled runtime evidence is forbidden")
    event_path = confined(args.event_log, root, "event log", regular=False)
    plan_sha256 = required_sha256(args.plan_sha256, "MRTS plan digest")
    plan = load_json(plan_path, plan_sha256)
    if not isinstance(plan, dict) or plan.get("profile") != "no-crs/with-mrts" or plan.get("connector") != args.connector:
        fail("plan profile or connector is not closed")
    cases = plan.get("cases")
    if not isinstance(cases, list) or not cases:
        fail("plan has no cases")
    executor_record = plan.get("executor")
    executor_path = Path(__file__).resolve()
    if not isinstance(executor_record, dict) or executor_record.get("path") != str(executor_path):
        fail("plan executor path does not match the trusted executor")
    executor_sha = executor_record.get("sha256")
    if not isinstance(executor_sha, str) or len(executor_sha) != 64 or any(char not in SHA256_RE for char in executor_sha):
        fail("plan executor digest is invalid")
    if hashlib.sha256(executor_path.read_bytes()).hexdigest() != executor_sha:
        fail("executor digest mismatch")
    build_root = root / "build"
    load_path = Path(str(plan.get("load_file", "")))
    load_path = confined(str(load_path), build_root, "MRTS load file")
    supplied_load_path = confined(args.load_file, build_root, "supplied MRTS load file")
    if supplied_load_path != load_path:
        fail("supplied MRTS load file does not match the plan")
    load_sha = plan.get("load_file_sha256")
    if not isinstance(load_sha, str) or hashlib.sha256(load_path.read_bytes()).hexdigest() != load_sha:
        fail("MRTS load file digest mismatch")
    validate_sealed_no_crs_plan(plan_path, root, load_path, executor_path, plan_sha256)
    validation = plan.get("no_crs_validation")
    if not isinstance(validation, dict):
        fail("plan has no sealed no-CRS validation")
    raw_inventory = validation.get("rule_id_inventory")
    if (
        not isinstance(raw_inventory, list)
        or not raw_inventory
        or raw_inventory != sorted(raw_inventory, key=lambda value: int(value) if isinstance(value, str) and value.isdigit() else -1)
        or len(raw_inventory) > 100_000
        or any(
            not isinstance(value, str)
            or not value
            or len(value) > 12
            or value[0] == "0"
            or any(character not in "0123456789" for character in value)
            for value in raw_inventory
        )
        or len(set(raw_inventory)) != len(raw_inventory)
    ):
        fail("plan rule ID inventory is not canonical")
    allowed_rule_ids = set(raw_inventory)
    inventory_root = confined(str(plan.get("inventory_root", "")), build_root, "MRTS inventory root", regular=False)
    if inventory_root.is_symlink() or not inventory_root.is_dir():
        fail("MRTS inventory root is not a regular contained directory")
    case_hashes = plan.get("case_hashes")
    if not isinstance(case_hashes, dict):
        fail("MRTS case hash map is missing")
    for relative, expected_hash in case_hashes.items():
        case_path = confined(str(inventory_root / str(relative)), inventory_root, "MRTS case")
        if not isinstance(expected_hash, str) or len(expected_hash) != 64 or any(char not in SHA256_RE for char in expected_hash) or hashlib.sha256(case_path.read_bytes()).hexdigest() != expected_hash:
            fail(f"MRTS case digest mismatch: {relative}")
    for case in cases:
        if isinstance(case, dict) and case.get("source") not in (None, "") and str(case["source"]) not in case_hashes:
            fail("plan case references an unverified MRTS source")
    run_id = secrets.token_hex(12)
    tls_context = ssl._create_unverified_context() if args.tls_insecure else None
    observed: list[dict[str, Any]] = []
    for index, case in enumerate(cases):
        if not isinstance(case, dict) or case.get("kind") not in {"control", "detection", "bypass"}:
            fail("invalid case kind")
        correlation_id = f"{run_id}-{index:04d}"
        # The executor supplies X-MRTS-Transaction-ID.  Each target-only
        # adapter binds its native runtime to that explicit header, while
        # X-Request-ID remains an independent host/proxy identifier.
        request_id = correlation_id
        transaction_id = correlation_id
        host_request_id = f"host-{correlation_id}"
        uri = case.get("uri")
        if not isinstance(uri, str) or len(uri) > 2048 or not uri.startswith("/") or any(ord(char) < 0x20 or ord(char) == 0x7F for char in uri):
            fail("invalid case URI")
        status = request(f"{args.scheme}://{args.host}:{args.port}{uri}", "GET", {
            "Host": args.host,
            "X-MRTS-Request-ID": request_id,
            "X-MRTS-Transaction-ID": transaction_id,
            "X-Request-ID": host_request_id,
            "User-Agent": "MRTS-runtime/1",
        }, 15.0, tls_context)
        raw_expected_ids = case.get("expect_ids", [])
        if not isinstance(raw_expected_ids, list) or any(not str(value).isdigit() or len(str(value)) > 12 for value in raw_expected_ids):
            fail("invalid expected rule ID")
        expected_ids = {str(value) for value in raw_expected_ids}
        expected_phase = case.get("expect_event_phase")
        if expected_phase != "request_body":
            fail("invalid expected MRTS rule-match phase")
        matched = event_ids(
            event_path, correlation_id, args.connector, uri, expected_phase,
            expected_ids, allowed_rule_ids)
        if status != 200:
            fail(f"{case.get('id', index)} returned HTTP {status}, expected DetectionOnly 200")
        require_case_rule_matches(
            case["kind"], str(case.get("id", index)), expected_ids, matched
        )
        observed.append({"case_id": case.get("id", str(index)), "kind": case["kind"], "uri": uri, "connector": args.connector, "correlation_id": correlation_id, "request_id": request_id, "transaction_id": transaction_id, "host_request_id": host_request_id, "expected_event_phase": expected_phase, "status": status, "expected_rule_ids": sorted(expected_ids), "observed_rule_ids": sorted(matched)})
    if not {item["kind"] for item in observed} >= {"control", "detection", "bypass"}:
        fail("plan must contain control, detection, and bypass cases")
    receipt = {"connector": args.connector, "profile": "no-crs/with-mrts", "run_id": run_id, "plan_sha256": plan_sha256, "cases": observed, "status": "passed"}
    atomic_json(result_path, receipt, root)
    return 0


if __name__ == "__main__":
    main()
