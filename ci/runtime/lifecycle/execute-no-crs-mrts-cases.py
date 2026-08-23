#!/usr/bin/env python3
"""Execute a bounded no-CRS/with-MRTS plan against a real host endpoint."""
from __future__ import annotations

import argparse
import hashlib
import http.client
import importlib.util
import json
import os
import secrets
import ssl
import struct
import sys
from pathlib import Path
from typing import Any, NoReturn

MAX_BYTES = 1_048_576
LOOPBACK_HOST = "127.0.0.1"
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


class LoopbackEndpoint:
    """A validated endpoint that can only address the fixed local host."""

    __slots__ = ("port",)

    def __init__(self, port: int) -> None:
        self.port = port


def fail(message: str) -> NoReturn:
    raise SystemExit(f"FAIL: {message}")


def safe_root(value: str, label: str) -> Path:
    root = Path(value).expanduser()
    if (
        not root.is_absolute()
        or root == Path(root.anchor)
        or ".." in root.parts
    ):
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


def confined_components(path: str, root: Path, label: str) -> tuple[str, ...]:
    """Reduce an external absolute path to safe, root-relative components."""

    prefix = f"{root}{os.sep}"
    if not isinstance(path, str) or not path.startswith(prefix):
        fail(f"{label} escapes its private root")
    components = tuple(path.removeprefix(prefix).split(os.sep))
    if not components or any(
        not component
        or component in {".", ".."}
        or not component.isascii()
        or any(not (character.isalnum() or character in "._-") for character in component)
        for component in components
    ):
        fail(f"{label} is not a canonical private-root path")
    return components


def confined_candidate(root: Path, components: tuple[str, ...]) -> Path:
    candidate = root
    for component in components:
        candidate /= component
    return candidate


def reject_confined_symlinks(root: Path, components: tuple[str, ...], label: str) -> None:
    current = root
    for component in components:
        current /= component
        if current.exists() and current.is_symlink():
            fail(f"{label} contains a symlink component")


def confined(path: str, root: Path, label: str, *, regular: bool = True) -> Path:
    components = confined_components(path, root, label)
    candidate = confined_candidate(root, components)
    reject_confined_symlinks(root, components, label)
    try:
        if not regular:
            candidate.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            reject_confined_symlinks(root, components, label)
        resolved = candidate.resolve(strict=regular)
        resolved.relative_to(root)
    except (OSError, ValueError) as exc:
        fail(f"{label} escapes its private root: {exc}")
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


def validate_rule_match_fields(
    item: dict[str, Any], connector: str, integration_mode: str,
) -> None:
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


def validate_rule_match_values(
    item: dict[str, Any], expected_phase: str | None,
) -> None:
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


def validate_rule_match_integrity(item: dict[str, Any]) -> tuple[str, int]:
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


def validate_rule_match_event(
    item: dict[str, Any],
    connector: str,
    integration_mode: str,
    expected_phase: str | None = None,
) -> tuple[str, int]:
    """Validate one exact native rule-match record and return its identity."""
    validate_rule_match_fields(item, connector, integration_mode)
    validate_rule_match_values(item, expected_phase)
    return validate_rule_match_integrity(item)


def parse_event_record(line: str) -> dict[str, Any]:
    if not line:
        fail("event log contains an empty record")
    try:
        item = json.loads(line, object_pairs_hook=reject_duplicates)
    except (UnicodeError, json.JSONDecodeError) as exc:
        fail(f"event log is not duplicate-safe JSONL: {exc}")
    if not isinstance(item, dict):
        fail("event log entries must be JSON objects")
    return item


def validate_event_chain(item: dict[str, Any], previous_event_hash: int | None) -> None:
    if previous_event_hash is None:
        if item["previous_event_hash"] != 0:
            fail("first rule-match event does not start a native integrity chain")
    elif item["previous_event_hash"] != previous_event_hash:
        fail("rule-match event does not continue the native integrity chain")


def correlate_event(
    item: dict[str, Any], rule_id: str, correlation_id: str, connector: str,
    uri: str, expected_phase: str, expected_ids: set[str],
    allowed_rule_ids: set[str], found: set[str],
) -> None:
    if (
        item.get("transaction_id") != correlation_id
        or item.get("connector") != connector
        or item.get("uri") != uri
    ):
        return
    if item["phase"] == expected_phase:
        if rule_id not in allowed_rule_ids:
            fail("relevant rule-match event has rule ID outside the pinned corpus")
        if rule_id in found:
            fail("relevant rule-match event duplicates a rule ID")
        found.add(rule_id)
    elif not expected_ids:
        if rule_id in found:
            fail("relevant rule-match event duplicates a rule ID")
        found.add(rule_id)
    elif rule_id in expected_ids:
        fail("relevant rule-match event has invalid phase")


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
        item = parse_event_record(line)
        # Validate the complete native record and chain before correlating it.
        # Phase is intentionally checked against the closed enum here, while
        # the profile-specific expected phase is enforced only for a relevant
        # transaction/URI below. Native adapters emit legitimate records for
        # other phases and those records remain integrity-validated evidence.
        rule_id, event_hash = validate_rule_match_event(
            item, connector, integration_mode
        )
        validate_event_chain(item, previous_event_hash)
        previous_event_hash = event_hash
        correlate_event(
            item, rule_id, correlation_id, connector, uri, expected_phase,
            expected_ids, allowed_rule_ids, found,
        )
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


def request(
    path: str,
    endpoint: LoopbackEndpoint,
    method: str,
    headers: dict[str, str],
    timeout: float,
    scheme: str,
    context: ssl.SSLContext | None,
) -> int:
    """Send one request to the sealed loopback endpoint.

    The endpoint is deliberately built with ``http.client`` from the fixed
    loopback constant rather than opening a caller-provided URL.  This keeps
    the SSRF boundary explicit, and ``http.client`` never follows redirects.
    HTTPS uses a caller-supplied verified context, so hostname and certificate
    verification remain enabled for Envoy's private loopback certificate.
    """
    if type(endpoint.port) is not int or not 1 <= endpoint.port <= 65535:
        fail("sealed loopback endpoint has an invalid port")
    connection: http.client.HTTPConnection
    if scheme == "https":
        if context is None:
            fail("HTTPS request requires a verified TLS context")
        connection = http.client.HTTPSConnection(
            LOOPBACK_HOST, endpoint.port, timeout=timeout, context=context
        )
    elif scheme == "http":
        connection = http.client.HTTPConnection(
            LOOPBACK_HOST, endpoint.port, timeout=timeout
        )
    else:
        fail("unsupported request scheme")
    try:
        connection.request(method, path, headers=headers)
        with connection.getresponse() as response:
            response.read(MAX_BYTES)
            return int(response.status)
    finally:
        connection.close()


def verified_tls_context(root: Path, certificate_value: str) -> ssl.SSLContext:
    """Trust only the sealed, run-local Envoy loopback certificate."""

    certificate = confined(certificate_value, root, "TLS certificate")
    if certificate.is_symlink():
        fail("TLS certificate must not be a symlink")
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.load_verify_locations(cafile=str(certificate))
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED
    return context


def parse_args() -> argparse.Namespace:
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
    parser.add_argument("--tls-certificate")
    return parser.parse_args()


def validate_endpoint(args: argparse.Namespace) -> LoopbackEndpoint:
    if (
        type(args.port) is not int
        or not 1 <= args.port <= 65535
        or any(
            character not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-"
            for character in args.host
        )
    ):
        fail("invalid host or port")
    if args.host != LOOPBACK_HOST:
        fail("MRTS runtime endpoint must be 127.0.0.1")
    return LoopbackEndpoint(port=args.port)


def validate_result_path(value: str, root: Path) -> Path:
    result_path = confined(value, root, "result", regular=False)
    if result_path.exists():
        fail("result already exists; recycled runtime evidence is forbidden")
    return result_path


def validate_rule_id_inventory(raw_inventory: Any) -> set[str]:
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
    return set(raw_inventory)


def validate_inventory_root(plan: dict[str, Any], build_root: Path) -> Path:
    inventory_root = build_root / "mrts" / "upstream-config-tests" / "framework-cases"
    if plan.get("inventory_root") != str(inventory_root):
        fail("MRTS inventory root does not match the closed private layout")
    if inventory_root.is_symlink() or not inventory_root.is_dir():
        fail("MRTS inventory root is not a regular contained directory")
    return inventory_root


def direct_case_sources(inventory_root: Path) -> dict[str, Path]:
    sources: dict[str, Path] = {}
    for source in inventory_root.glob("*.yaml"):
        if source.is_symlink() or not source.is_file() or source.parent != inventory_root:
            fail("MRTS inventory contains a non-regular case source")
        if source.name in sources:
            fail("MRTS inventory contains duplicate case source names")
        sources[source.name] = source
    return sources


def validate_case_hashes(case_hashes: Any, inventory_root: Path) -> dict[str, Any]:
    if not isinstance(case_hashes, dict):
        fail("MRTS case hash map is missing")
    sources = direct_case_sources(inventory_root)
    for relative, expected_hash in case_hashes.items():
        case_path = sources.get(relative) if isinstance(relative, str) else None
        if case_path is None:
            fail("MRTS case hash map contains a source outside the pinned inventory")
        if (
            not isinstance(expected_hash, str)
            or len(expected_hash) != 64
            or any(char not in SHA256_RE for char in expected_hash)
            or hashlib.sha256(case_path.read_bytes()).hexdigest() != expected_hash
        ):
            fail(f"MRTS case digest mismatch: {relative}")
    return case_hashes


def validate_case_sources(cases: list[Any], case_hashes: dict[str, Any]) -> None:
    for case in cases:
        if (
            isinstance(case, dict)
            and case.get("source") not in (None, "")
            and str(case["source"]) not in case_hashes
        ):
            fail("plan case references an unverified MRTS source")


def validate_inventory(plan: dict[str, Any], build_root: Path) -> set[str]:
    validation = plan.get("no_crs_validation")
    if not isinstance(validation, dict):
        fail("plan has no sealed no-CRS validation")
    allowed_rule_ids = validate_rule_id_inventory(validation.get("rule_id_inventory"))
    inventory_root = validate_inventory_root(plan, build_root)
    case_hashes = validate_case_hashes(plan.get("case_hashes"), inventory_root)
    validate_case_sources(plan["cases"], case_hashes)
    return allowed_rule_ids


def load_runtime_plan(
    args: argparse.Namespace, root: Path, plan_path: Path,
) -> tuple[dict[str, Any], str, set[str]]:
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
    load_path = build_root / "mrts" / "upstream-config-tests" / "mrts.load"
    if plan.get("load_file") != str(load_path) or args.load_file != str(load_path):
        fail("supplied MRTS load file does not match the closed private layout")
    if load_path.is_symlink() or not load_path.is_file():
        fail("MRTS load file is not a regular closed-layout artifact")
    load_sha = plan.get("load_file_sha256")
    if not isinstance(load_sha, str) or hashlib.sha256(load_path.read_bytes()).hexdigest() != load_sha:
        fail("MRTS load file digest mismatch")
    validate_sealed_no_crs_plan(plan_path, root, load_path, executor_path, plan_sha256)
    return plan, plan_sha256, validate_inventory(plan, build_root)


def prepare_tls(
    args: argparse.Namespace, root: Path,
) -> ssl.SSLContext | None:
    if args.scheme == "https":
        if args.tls_certificate is None:
            fail("HTTPS MRTS runtime requires a sealed TLS certificate")
        return verified_tls_context(root, args.tls_certificate)
    if args.tls_certificate is not None:
        fail("HTTP MRTS runtime must not receive a TLS certificate")
    return None


def prepare_runtime(
    args: argparse.Namespace,
) -> tuple[
    Path, dict[str, Any], Path, Path, str, set[str], ssl.SSLContext | None,
    LoopbackEndpoint,
]:
    endpoint = validate_endpoint(args)
    root = safe_root(args.runtime_root, "runtime root")
    plan_path = confined(args.plan, root, "plan")
    result_path = validate_result_path(args.result, root)
    event_path = confined(args.event_log, root, "event log", regular=False)
    plan, plan_sha256, allowed_rule_ids = load_runtime_plan(args, root, plan_path)
    tls_context = prepare_tls(args, root)
    return (
        root, plan, event_path, result_path, plan_sha256, allowed_rule_ids,
        tls_context, endpoint,
    )


def validate_case(case: Any) -> tuple[str, str, list[Any]]:
    if not isinstance(case, dict) or case.get("kind") not in {"control", "detection", "bypass"}:
        fail("invalid case kind")
    uri = case.get("uri")
    if not isinstance(uri, str) or len(uri) > 2048 or not uri.startswith("/") or any(
        ord(char) < 0x20 or ord(char) == 0x7F for char in uri
    ):
        fail("invalid case URI")
    raw_expected_ids = case.get("expect_ids", [])
    if not isinstance(raw_expected_ids, list) or any(
        not str(value).isdigit() or len(str(value)) > 12 for value in raw_expected_ids
    ):
        fail("invalid expected rule ID")
    expected_phase = case.get("expect_event_phase")
    if expected_phase != "request_body":
        fail("invalid expected MRTS rule-match phase")
    return str(case["kind"]), uri, raw_expected_ids


def execute_case(
    args: argparse.Namespace, case: Any, index: int, run_id: str,
    event_path: Path, allowed_rule_ids: set[str],
    tls_context: ssl.SSLContext | None, endpoint: LoopbackEndpoint,
) -> dict[str, Any]:
    case_kind, uri, raw_expected_ids = validate_case(case)
    correlation_id = f"{run_id}-{index:04d}"
    request_id = correlation_id
    transaction_id = correlation_id
    host_request_id = f"host-{correlation_id}"
    status = request(uri, endpoint, "GET", {
        "Host": args.host,
        "X-MRTS-Request-ID": request_id,
        "X-MRTS-Transaction-ID": transaction_id,
        "X-Request-ID": host_request_id,
        "User-Agent": "MRTS-runtime/1",
    }, 15.0, args.scheme, tls_context)
    expected_ids = {str(value) for value in raw_expected_ids}
    matched = event_ids(
        event_path, correlation_id, args.connector, uri, "request_body",
        expected_ids, allowed_rule_ids,
    )
    if status != 200:
        fail(f"{case.get('id', index)} returned HTTP {status}, expected DetectionOnly 200")
    case_id = str(case.get("id", index))
    require_case_rule_matches(case_kind, case_id, expected_ids, matched)
    return {
        "case_id": case.get("id", str(index)), "kind": case_kind, "uri": uri,
        "connector": args.connector, "correlation_id": correlation_id,
        "request_id": request_id, "transaction_id": transaction_id,
        "host_request_id": host_request_id, "expected_event_phase": "request_body",
        "status": status, "expected_rule_ids": sorted(expected_ids),
        "observed_rule_ids": sorted(matched),
    }


def run_cases(
    args: argparse.Namespace,
    root: Path,
    plan: dict[str, Any],
    event_path: Path,
    result_path: Path,
    plan_sha256: str,
    allowed_rule_ids: set[str],
    tls_context: ssl.SSLContext | None,
    endpoint: LoopbackEndpoint,
) -> None:
    cases = plan["cases"]
    run_id = secrets.token_hex(12)
    observed: list[dict[str, Any]] = []
    for index, case in enumerate(cases):
        observed.append(execute_case(
            args, case, index, run_id, event_path, allowed_rule_ids, tls_context,
            endpoint,
        ))
    if not {item["kind"] for item in observed} >= {"control", "detection", "bypass"}:
        fail("plan must contain control, detection, and bypass cases")
    receipt = {"connector": args.connector, "profile": "no-crs/with-mrts", "run_id": run_id, "plan_sha256": plan_sha256, "cases": observed, "status": "passed"}
    atomic_json(result_path, receipt, root)


def main() -> int:
    args = parse_args()
    (
        root, plan, event_path, result_path, plan_sha256, allowed_rule_ids,
        tls_context, endpoint,
    ) = prepare_runtime(args)
    run_cases(
        args, root, plan, event_path, result_path, plan_sha256,
        allowed_rule_ids, tls_context, endpoint,
    )
    return 0


if __name__ == "__main__":
    main()
