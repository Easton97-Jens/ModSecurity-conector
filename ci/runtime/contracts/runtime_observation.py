#!/usr/bin/env python3
"""Strict, connector-neutral runtime-observation contract.

This module deliberately separates contract validation from connector host
execution.  A connector producer must provide structured, live evidence; a
successful command or workflow step is never converted into a runtime PASS by
this validator.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Mapping


SCHEMA_VERSION = 1
MAX_OBSERVATION_BYTES = 1024 * 1024
MAX_EVIDENCE_FILES = 32
MAX_TEXT_LENGTH = 1024
MAX_COUNTER = 1_000_000

CONNECTORS = frozenset(("apache", "envoy", "haproxy", "lighttpd", "traefik", "nginx"))
PROFILES = frozenset(
    (
        "no-crs-no-mrts",
        "no-crs-with-mrts",
        "with-crs-no-mrts",
        "with-crs-with-mrts",
    )
)
EXPECTATION_KINDS = frozenset(
    (
        "http_status",
        "intervention",
        "action",
        "rule_match",
        "rule_id",
        "event",
        "request_headers",
        "response_headers",
        "request_body",
        "response_body",
        "transport",
        "lifecycle",
        "cleanup",
        "compound",
        "not_applicable",
    )
)
ASSERTION_RESULTS = frozenset(("PASS", "FAIL", "NOT_APPLICABLE", "NOT_EXECUTED"))
RUNTIME_STATUSES = frozenset(("PASS", "PARTIAL", "VALIDATION_FAILED", "FAIL"))
VALIDATION_STATUSES = frozenset(("CONTRACT_VALIDATED", "VALIDATION_FAILED", "PARTIAL"))
LIVE_EVIDENCE_KINDS = frozenset(
    (
        "structured_connector_evidence",
        "live_runtime_evidence",
        "protected_runtime_evidence",
    )
)
CANONICAL_EVIDENCE_KINDS = LIVE_EVIDENCE_KINDS | frozenset(("canonical_fixture",))
RAW_EVIDENCE_KINDS = frozenset(("raw_log", "raw_payload", "synthetic", "step_exit"))
CONTRACT_VALIDATED = "CONTRACT_VALIDATED"
VALIDATION_FAILED = "VALIDATION_FAILED"
PARTIAL = "PARTIAL"
NOT_APPLICABLE = "NOT_APPLICABLE"

CONNECTOR_INTEGRATION_MODES = {
    "apache": "native-httpd-module",
    "envoy": "ext_proc",
    "haproxy": "native-htx-filter",
    "lighttpd": "patched-native-lighttpd",
    "traefik": "native-traefik-middleware",
    "nginx": "protected-root-broker",
}
LIVE_PRODUCERS = {
    "envoy": "parent-runtime-observation-adapter-envoy",
    "lighttpd": "parent-runtime-observation-adapter-lighttpd",
    "traefik": "parent-runtime-observation-adapter-traefik",
    "nginx": "protected-nginx-root-broker",
}
PRODUCER_VERSION = "1.0.0"

TOKEN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$", re.ASCII)
SHA256 = re.compile(r"^[0-9a-f]{64}$", re.ASCII)
COMMIT = re.compile(r"^[0-9a-f]{40}$", re.ASCII)
TIMESTAMP = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,9})?Z$", re.ASCII
)
WINDOWS_ABSOLUTE_PATH = re.compile(r"^[A-Za-z]:[\\/]", re.ASCII)

RUNTIME_REQUIRED_ASSERTIONS = (
    "config_test",
    "host_start",
    "reachability",
    "allow_case",
    "block_case",
)
RUNTIME_OPTIONAL_ASSERTIONS = frozenset(("bypass_case",))
ISOLATION_FIELDS = (
    "mrts_runner_invoked",
    "mrts_inventory_loaded",
    "mrts_process_started",
    "mrts_listener_created",
    "mrts_artifact_used",
)
CLEANUP_COUNTERS = (
    "host_processes_remaining",
    "helper_processes_remaining",
    "listeners_remaining",
    "sockets_remaining",
    "pid_files_remaining",
    "temporary_paths_remaining",
)
SEMANTIC_VALUE_FIELDS = frozenset(
    (
        "kind",
        "value",
        "http_status",
        "action",
        "intervention",
        "event",
        "transport",
        "rule_ids",
        "predicates",
        "status",
        "started",
        "reachable",
    )
)


def _profile_requirement(crs: bool, mrts: bool) -> dict[str, Any]:
    return {
        "crs": crs,
        "mrts": mrts,
        "requires_mrts": mrts,
        "scenario_category": "with-crs" if crs else "no-crs",
        "framework_scenario_categories": (
            frozenset(("with-crs", "crs-sqli-anomaly"))
            if crs
            else frozenset(("no-crs",))
        ),
        "required_runtime_assertions": RUNTIME_REQUIRED_ASSERTIONS,
        "optional_runtime_assertions": RUNTIME_OPTIONAL_ASSERTIONS,
        "require_framework_live_execution": True,
        "isolation": {field: mrts for field in ISOLATION_FIELDS},
        "require_clean_cleanup": True,
    }


PROFILE_REQUIREMENTS: dict[str, dict[str, Any]] = {
    "no-crs-no-mrts": _profile_requirement(False, False),
    "no-crs-with-mrts": _profile_requirement(False, True),
    "with-crs-no-mrts": _profile_requirement(True, False),
    "with-crs-with-mrts": _profile_requirement(True, True),
}


class ObservationInputError(ValueError):
    """Raised when an observation file cannot be safely ingested."""


RuntimeObservationError = ObservationInputError


class ValidationResult(dict[str, Any]):
    """Mapping result with compatibility attributes for direct callers."""

    @property
    def status(self) -> str:
        return str(self["status"])

    @property
    def errors(self) -> list[str]:
        return list(self["errors"])

    @property
    def valid(self) -> bool:
        return self["status"] == "PASS"


@dataclass(frozen=True)
class AdapterInterface:
    """Finite connector adapter interface; it never provides a fallback producer."""

    connector: str
    live_producer_supported: bool
    protected_separate: bool = False


ADAPTER_INTERFACES = {
    connector: AdapterInterface(connector, connector in LIVE_PRODUCERS)
    for connector in CONNECTORS
}
ADAPTER_INTERFACES["nginx"] = AdapterInterface("nginx", False, protected_separate=True)


def adapter_for(connector: str) -> AdapterInterface:
    try:
        return ADAPTER_INTERFACES[connector]
    except KeyError as exc:
        raise RuntimeObservationError("connector is unsupported") from exc


def require_live_adapter(connector: str) -> AdapterInterface:
    adapter = adapter_for(connector)
    if not adapter.live_producer_supported:
        raise RuntimeObservationError(f"{connector} has no live runtime producer")
    return adapter


class _Issues:
    def __init__(self) -> None:
        self.hard: list[str] = []
        self.incomplete: list[str] = []

    @staticmethod
    def _message(message: str) -> str:
        clean = " ".join(str(message).split())
        return clean[:MAX_TEXT_LENGTH] or "validation error"

    def error(self, message: str) -> None:
        value = self._message(message)
        if value not in self.hard:
            self.hard.append(value)

    def partial(self, message: str) -> None:
        value = self._message(message)
        if value not in self.incomplete:
            self.incomplete.append(value)

    def all(self) -> list[str]:
        return [*self.hard, *self.incomplete]


def canonical_json(value: object) -> bytes:
    """Return deterministic JSON bytes without allowing non-finite values."""
    return json.dumps(
        value,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def evidence_manifest_digest(evidence: list[dict[str, Any]]) -> str:
    """Digest a canonical, path-free evidence inventory rather than raw logs."""
    normalized = [
        {
            "kind": item.get("kind"),
            "name": item.get("name"),
            "path": item.get("path"),
            "sha256": item.get("sha256"),
        }
        for item in evidence
    ]
    normalized.sort(key=lambda item: (str(item["name"]), str(item["path"])))
    return hashlib.sha256(canonical_json(normalized)).hexdigest()


def _is_boolean(value: object) -> bool:
    return type(value) is bool


def _is_bounded_integer(value: object, *, lower: int = 0, upper: int = MAX_COUNTER) -> bool:
    return type(value) is int and lower <= value <= upper


def _safe_token(value: object) -> bool:
    return isinstance(value, str) and TOKEN.fullmatch(value) is not None


def _safe_reason(value: object) -> bool:
    return (
        isinstance(value, str)
        and bool(value)
        and len(value) <= MAX_TEXT_LENGTH
        and "\x00" not in value
        and "\r" not in value
        and "\n" not in value
    )


def _is_absolute_path_text(value: str) -> bool:
    return value.startswith("/") or WINDOWS_ABSOLUTE_PATH.match(value) is not None


def _has_forbidden_metadata(value: object) -> bool:
    """Reject canonical metadata that could carry raw logs or host paths."""
    if isinstance(value, Mapping):
        for key, child in value.items():
            if not isinstance(key, str):
                return True
            lowered = key.lower()
            if lowered in {
                "payload",
                "payloads",
                "raw_log",
                "raw_logs",
                "log_content",
                "log_contents",
                "request",
                "response",
                "request_body",
                "response_body",
                "headers",
                "authorization",
                "cookie",
                "secret",
                "secrets",
                "credential",
                "credentials",
                "password",
                "private_key",
                "api_key",
                "runner_path",
                "absolute_path",
            }:
                return True
            if _has_forbidden_metadata(child):
                return True
        return False
    if isinstance(value, list):
        return any(_has_forbidden_metadata(child) for child in value)
    return isinstance(value, str) and _is_absolute_path_text(value)


def _as_mapping(value: object, label: str, issues: _Issues) -> dict[str, Any] | None:
    if not isinstance(value, Mapping):
        issues.error(f"{label} must be an object")
        return None
    return dict(value)


def _require_exact_keys(
    value: Mapping[str, Any],
    required: set[str],
    optional: set[str],
    label: str,
    issues: _Issues,
) -> None:
    missing = sorted(required - set(value))
    unexpected = sorted(set(value) - required - optional)
    if missing:
        issues.error(f"{label} is missing required fields: {', '.join(missing)}")
    if unexpected:
        issues.error(f"{label} contains unsupported fields: {', '.join(unexpected)}")


def _check_string_field(
    value: Mapping[str, Any],
    name: str,
    label: str,
    issues: _Issues,
    *,
    matcher: re.Pattern[str] | None = None,
) -> str | None:
    field = value.get(name)
    pattern = matcher or TOKEN
    if not isinstance(field, str) or pattern.fullmatch(field) is None:
        issues.error(f"{label}.{name} must be a bounded token")
        return None
    return field


def _normalise_policy(policy: str | Mapping[str, Any] | None) -> dict[str, Any]:
    if policy is None:
        policy = "strict"
    if isinstance(policy, str):
        name = policy
        supplied: Mapping[str, Any] = {}
    elif isinstance(policy, Mapping):
        name = str(policy.get("name", "strict"))
        supplied = policy
    else:
        raise TypeError("policy must be a string, mapping, or None")
    if name not in {"strict", "partial", "fixture"}:
        raise ValueError("policy name must be strict, partial, or fixture")
    return {
        "name": name,
        "allow_partial": name == "partial",
        "allow_fixture_evidence": name == "fixture",
        "evidence_root": supplied.get("evidence_root"),
    }


def _path_from_value(value: Path | str) -> Path:
    return Path(os.path.abspath(os.fspath(value)))


def _validate_directory_details(
    details: os.stat_result,
    path: Path,
    *,
    private: bool = False,
) -> None:
    if not stat.S_ISDIR(details.st_mode):
        raise ObservationInputError("evidence path contains a non-directory component")
    mode = stat.S_IMODE(details.st_mode)
    if private:
        if details.st_uid != os.geteuid() or mode != 0o700:
            raise ObservationInputError(
                "evidence root and descendants must be current-user 0700 directories"
            )
        return
    public_sticky = details.st_uid == 0 and bool(mode & stat.S_ISVTX) and bool(mode & 0o022)
    if mode & 0o022 and not public_sticky:
        raise ObservationInputError("evidence path has a group- or world-writable directory")
    if details.st_uid not in {0, os.geteuid()}:
        raise ObservationInputError("evidence path has an untrusted directory owner")
    if path == Path("/") and not public_sticky and details.st_uid != 0:
        raise ObservationInputError("filesystem root has an untrusted owner")


def _open_secure_directory(root: Path | str) -> tuple[int, Path]:
    path = _path_from_value(root)
    if path == Path("/"):
        raise ObservationInputError("evidence root must be narrower than filesystem root")
    no_follow = getattr(os, "O_NOFOLLOW", None)
    directory_flag = getattr(os, "O_DIRECTORY", None)
    if no_follow is None or directory_flag is None:
        raise ObservationInputError("safe evidence reads require O_NOFOLLOW and O_DIRECTORY")
    flags = os.O_RDONLY | directory_flag | no_follow
    descriptor = os.open("/", flags)
    current = Path("/")
    try:
        _validate_directory_details(os.fstat(descriptor), current)
        for component in path.parts[1:]:
            next_path = current / component
            try:
                before = os.stat(component, dir_fd=descriptor, follow_symlinks=False)
            except FileNotFoundError as exc:
                raise ObservationInputError("evidence root is unavailable") from exc
            _validate_directory_details(before, next_path, private=next_path == path)
            child = os.open(component, flags, dir_fd=descriptor)
            after = os.fstat(child)
            if (before.st_dev, before.st_ino, stat.S_IFMT(before.st_mode)) != (
                after.st_dev,
                after.st_ino,
                stat.S_IFMT(after.st_mode),
            ):
                os.close(child)
                raise ObservationInputError("evidence directory changed during validation")
            _validate_directory_details(after, next_path, private=next_path == path)
            os.close(descriptor)
            descriptor = child
            current = next_path
        return descriptor, current
    except BaseException:
        os.close(descriptor)
        raise


def _validate_file_details(details: os.stat_result, label: str, maximum: int) -> None:
    if not stat.S_ISREG(details.st_mode):
        raise ObservationInputError(f"{label} must be a regular file")
    if details.st_nlink != 1:
        raise ObservationInputError(f"{label} must not be hard-linked")
    if details.st_uid != os.geteuid():
        raise ObservationInputError(f"{label} must be owned by the current user")
    if stat.S_IMODE(details.st_mode) != 0o600:
        raise ObservationInputError(f"{label} must have exact mode 0600")
    if details.st_size > maximum:
        raise ObservationInputError(f"{label} exceeds the bounded evidence size")


def _file_snapshot(details: os.stat_result) -> tuple[int, int, int, int, int, int, int, int]:
    return (
        details.st_dev,
        details.st_ino,
        stat.S_IFMT(details.st_mode),
        details.st_size,
        details.st_nlink,
        details.st_uid,
        details.st_mtime_ns,
        details.st_ctime_ns,
    )


def _write_all(descriptor: int, data: bytes) -> None:
    """Write all bytes, explicitly handling short or zero-progress writes."""
    view = memoryview(data)
    while view:
        count = os.write(descriptor, view)
        if count <= 0 or count > len(view):
            raise ObservationInputError("canonical evidence write did not make progress")
        view = view[count:]


def read_bounded_evidence_file(
    path: Path | str,
    evidence_root: Path | str,
    *,
    label: str = "evidence file",
    maximum: int = MAX_OBSERVATION_BYTES,
) -> bytes:
    """Read one regular evidence file through descriptor-relative no-follow I/O."""
    root_descriptor, root = _open_secure_directory(evidence_root)
    target = _path_from_value(path)
    try:
        relative = target.relative_to(root)
    except ValueError as exc:
        os.close(root_descriptor)
        raise ObservationInputError("evidence file escapes its declared root") from exc
    if not relative.parts:
        os.close(root_descriptor)
        raise ObservationInputError("evidence root cannot itself be an evidence file")
    no_follow = getattr(os, "O_NOFOLLOW", None)
    directory_flag = getattr(os, "O_DIRECTORY", None)
    nonblock = getattr(os, "O_NONBLOCK", None)
    if no_follow is None or directory_flag is None or nonblock is None:
        os.close(root_descriptor)
        raise ObservationInputError("safe evidence reads require no-follow non-blocking support")
    directory_flags = os.O_RDONLY | directory_flag | no_follow
    descriptor = root_descriptor
    current = root
    file_descriptor = -1
    try:
        for component in relative.parts[:-1]:
            current = current / component
            before = os.stat(component, dir_fd=descriptor, follow_symlinks=False)
            _validate_directory_details(before, current, private=True)
            child = os.open(component, directory_flags, dir_fd=descriptor)
            after = os.fstat(child)
            if (before.st_dev, before.st_ino, stat.S_IFMT(before.st_mode)) != (
                after.st_dev,
                after.st_ino,
                stat.S_IFMT(after.st_mode),
            ):
                os.close(child)
                raise ObservationInputError("evidence directory changed during validation")
            _validate_directory_details(after, current, private=True)
            os.close(descriptor)
            descriptor = child
        filename = relative.parts[-1]
        before = os.stat(filename, dir_fd=descriptor, follow_symlinks=False)
        _validate_file_details(before, label, maximum)
        file_descriptor = os.open(
            filename,
            os.O_RDONLY | no_follow | nonblock,
            dir_fd=descriptor,
        )
        opened = os.fstat(file_descriptor)
        _validate_file_details(opened, label, maximum)
        if _file_snapshot(before) != _file_snapshot(opened):
            raise ObservationInputError("evidence file changed between validation and open")
        pieces: list[bytes] = []
        remaining = maximum + 1
        while remaining:
            chunk = os.read(file_descriptor, min(65536, remaining))
            if not chunk:
                break
            pieces.append(chunk)
            remaining -= len(chunk)
        data = b"".join(pieces)
        final = os.fstat(file_descriptor)
        _validate_file_details(final, label, maximum)
        if _file_snapshot(opened) != _file_snapshot(final):
            raise ObservationInputError("evidence file changed while reading")
        if len(data) > maximum:
            raise ObservationInputError("evidence file grew beyond the bounded size")
        return data
    finally:
        if file_descriptor >= 0:
            os.close(file_descriptor)
        os.close(descriptor)


def _reject_duplicate_json_key(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ObservationInputError("JSON object contains a duplicate key")
        result[key] = value
    return result


def _reject_nonfinite_json(value: str) -> None:
    raise ObservationInputError("JSON contains a non-finite value")


def load_runtime_observation_file(
    path: Path | str,
    evidence_root: Path | str,
) -> dict[str, Any]:
    """Safely load a canonical observation without following arbitrary paths."""
    data = read_bounded_evidence_file(path, evidence_root, label="runtime observation")
    try:
        value = json.loads(
            data.decode("utf-8", "strict"),
            object_pairs_hook=_reject_duplicate_json_key,
            parse_constant=_reject_nonfinite_json,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ObservationInputError) as exc:
        if isinstance(exc, ObservationInputError):
            raise
        raise ObservationInputError("runtime observation is not valid UTF-8 JSON") from exc
    if not isinstance(value, dict):
        raise ObservationInputError("runtime observation JSON root must be an object")
    return value


def write_canonical_evidence_file(
    relative_path: str,
    data: bytes,
    evidence_root: Path | str,
) -> Path:
    """Create one fresh canonical evidence file through no-follow descriptors.

    The writer intentionally never overwrites an existing path.  The caller
    must reserve its private run directory first; this function pins that
    directory before creating the leaf, so an intermediate path replacement
    cannot redirect the write outside the declared evidence root.
    """
    if len(data) > MAX_OBSERVATION_BYTES:
        raise ObservationInputError("canonical evidence exceeds the bounded size")
    if not _safe_relative_evidence_path(relative_path):
        raise ObservationInputError("canonical evidence path must be a safe relative path")
    root_descriptor, root = _open_secure_directory(evidence_root)
    no_follow = getattr(os, "O_NOFOLLOW", None)
    directory_flag = getattr(os, "O_DIRECTORY", None)
    if no_follow is None or directory_flag is None:
        os.close(root_descriptor)
        raise ObservationInputError("safe evidence writes require O_NOFOLLOW and O_DIRECTORY")
    descriptor = root_descriptor
    current = root
    temporary_name: str | None = None
    file_descriptor = -1
    try:
        parts = PurePosixPath(relative_path).parts
        for component in parts[:-1]:
            current = current / component
            before = os.stat(component, dir_fd=descriptor, follow_symlinks=False)
            _validate_directory_details(before, current, private=True)
            child = os.open(component, os.O_RDONLY | directory_flag | no_follow, dir_fd=descriptor)
            after = os.fstat(child)
            if (before.st_dev, before.st_ino, stat.S_IFMT(before.st_mode)) != (
                after.st_dev,
                after.st_ino,
                stat.S_IFMT(after.st_mode),
            ):
                os.close(child)
                raise ObservationInputError("canonical evidence directory changed during validation")
            _validate_directory_details(after, current, private=True)
            os.close(descriptor)
            descriptor = child
        leaf = parts[-1]
        try:
            os.stat(leaf, dir_fd=descriptor, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            raise ObservationInputError("refusing to overwrite canonical evidence")
        temporary_name = f".{leaf}.{os.urandom(16).hex()}.tmp"
        file_descriptor = os.open(
            temporary_name,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | no_follow,
            0o600,
            dir_fd=descriptor,
        )
        _write_all(file_descriptor, data)
        os.fsync(file_descriptor)
        opened = os.fstat(file_descriptor)
        _validate_file_details(opened, "canonical evidence", MAX_OBSERVATION_BYTES)
        os.close(file_descriptor)
        file_descriptor = -1
        try:
            os.stat(leaf, dir_fd=descriptor, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            raise ObservationInputError("canonical evidence appeared during write")
        os.link(temporary_name, leaf, src_dir_fd=descriptor, dst_dir_fd=descriptor, follow_symlinks=False)
        os.unlink(temporary_name, dir_fd=descriptor)
        temporary_name = None
        os.fsync(descriptor)
        return root / PurePosixPath(relative_path)
    finally:
        if file_descriptor >= 0:
            os.close(file_descriptor)
        if temporary_name is not None:
            try:
                os.unlink(temporary_name, dir_fd=descriptor)
            except FileNotFoundError:
                pass
        os.close(descriptor)


load_runtime_observation = load_runtime_observation_file


def _validate_value_map(label: str, value: object, issues: _Issues) -> dict[str, Any] | None:
    mapping = _as_mapping(value, label, issues)
    if mapping is None:
        return None
    if not mapping:
        issues.error(f"{label} must not be empty")
        return mapping
    if _has_forbidden_metadata(mapping):
        issues.error(f"{label} contains raw-log, payload, or absolute-path metadata")
        return mapping
    for name, item in mapping.items():
        if name not in SEMANTIC_VALUE_FIELDS:
            issues.error(f"{label}.{name} is not a supported typed semantic field")
            continue
        if name in {"rule_ids", "predicates"}:
            continue
        if item is None and name == "value":
            continue
        if _is_boolean(item) or _is_bounded_integer(item, lower=-MAX_COUNTER, upper=MAX_COUNTER):
            continue
        if isinstance(item, str) and _safe_token(item):
            continue
        issues.error(f"{label}.{name} must be a bounded scalar semantic value")
    http_status = mapping.get("http_status")
    if http_status is not None and not _is_bounded_integer(http_status, lower=100, upper=599):
        issues.error(f"{label}.http_status must be a bounded integer")
    for name in ("action", "intervention", "event", "transport"):
        if name in mapping and not _safe_token(mapping[name]):
            issues.error(f"{label}.{name} must be a bounded token")
    if "rule_ids" in mapping:
        rules = mapping["rule_ids"]
        if (
            not isinstance(rules, list)
            or not rules
            or len(rules) > 64
            or any(not _is_bounded_integer(rule, lower=1, upper=2_147_483_647) for rule in rules)
            or len(set(rules)) != len(rules)
        ):
            issues.error(f"{label}.rule_ids must be a unique bounded integer list")
    if "predicates" in mapping:
        predicates = mapping["predicates"]
        if not isinstance(predicates, Mapping) or not predicates:
            issues.error(f"{label}.predicates must be a non-empty object")
        else:
            for name, predicate in predicates.items():
                if (
                    not _safe_token(name)
                    or not (
                        _is_boolean(predicate)
                        or _is_bounded_integer(predicate, lower=-MAX_COUNTER, upper=MAX_COUNTER)
                        or (isinstance(predicate, str) and _safe_token(predicate))
                    )
                ):
                    issues.error(f"{label}.predicates contains an unsafe value")
                    break
    return mapping


def _expected_matches_observed(
    expected: Mapping[str, Any], observed: Mapping[str, Any], label: str, issues: _Issues
) -> None:
    for name, expected_value in expected.items():
        if name not in observed:
            issues.error(f"{label}.observed is missing expected field {name}")
        elif observed[name] != expected_value:
            issues.error(f"{label}.expected and observed disagree for {name}")


def _validate_identity(
    identity_value: object,
    expected_identity: Mapping[str, Any] | None,
    issues: _Issues,
) -> dict[str, Any] | None:
    identity = _as_mapping(identity_value, "identity", issues)
    if identity is None:
        return None
    required = {
        "connector",
        "integration_mode",
        "profile",
        "crs",
        "mrts",
        "run_id",
        "parent_commit",
        "framework_commit",
        "mrts_commit",
        "producer",
        "producer_version",
    }
    _require_exact_keys(identity, required, set(), "identity", issues)
    connector = identity.get("connector")
    if connector not in CONNECTORS:
        issues.error("identity.connector is not a supported connector")
    for field in ("integration_mode", "run_id", "producer", "producer_version"):
        _check_string_field(identity, field, "identity", issues)
    if connector in CONNECTOR_INTEGRATION_MODES and identity.get("integration_mode") != CONNECTOR_INTEGRATION_MODES[connector]:
        issues.error("identity.integration_mode does not match the connector contract")
    profile = identity.get("profile")
    if profile not in PROFILES:
        issues.error("identity.profile is not a supported profile")
        requirements = None
    else:
        requirements = PROFILE_REQUIREMENTS[str(profile)]
    for field in ("crs", "mrts"):
        if not _is_boolean(identity.get(field)):
            issues.error(f"identity.{field} must be a boolean")
    if requirements is not None:
        for field in ("crs", "mrts"):
            if identity.get(field) is not requirements[field]:
                issues.error(f"identity.{field} contradicts identity.profile")
    for field in ("parent_commit", "framework_commit", "mrts_commit"):
        value = identity.get(field)
        if not isinstance(value, str) or COMMIT.fullmatch(value) is None:
            issues.error(f"identity.{field} must be a lowercase full commit")
    if expected_identity is not None:
        aliases = {
            "parent_sha": "parent_commit",
            "framework_sha": "framework_commit",
            "mrts_sha": "mrts_commit",
        }
        for supplied_name, supplied_value in expected_identity.items():
            name = aliases.get(supplied_name, supplied_name)
            if name not in identity:
                issues.error(f"expected identity contains unsupported field {supplied_name}")
            elif supplied_value is not None and identity.get(name) != supplied_value:
                issues.error(f"identity.{name} does not match expected identity")
    return identity


def _validate_assertion(
    value: object,
    label: str,
    issues: _Issues,
    *,
    matrix_required: bool,
    matrix_optional: bool,
    provenance_evidence_kind: object,
    allow_fixture_evidence: bool,
) -> None:
    assertion = _as_mapping(value, label, issues)
    if assertion is None:
        return
    required = {
        "required",
        "applicable",
        "executed",
        "live_executed",
        "expected",
        "observed",
        "result",
        "reason",
        "evidence_kind",
    }
    _require_exact_keys(assertion, required, {"case_id"}, label, issues)
    if "case_id" in assertion and not _safe_token(assertion.get("case_id")):
        issues.error(f"{label}.case_id must be a bounded token")
    for field in ("required", "applicable", "executed", "live_executed"):
        if not _is_boolean(assertion.get(field)):
            issues.error(f"{label}.{field} must be a boolean")
    result = assertion.get("result")
    if result not in ASSERTION_RESULTS:
        issues.error(f"{label}.result uses an unsupported status")
    if not _safe_reason(assertion.get("reason")):
        issues.error(f"{label}.reason must be bounded sanitized text")
    evidence_kind = assertion.get("evidence_kind")
    if evidence_kind not in CANONICAL_EVIDENCE_KINDS:
        issues.error(f"{label}.evidence_kind is not canonical")
    if evidence_kind in RAW_EVIDENCE_KINDS:
        issues.error(f"{label}.evidence_kind cannot use raw or synthetic evidence")
    if provenance_evidence_kind in CANONICAL_EVIDENCE_KINDS and evidence_kind != provenance_evidence_kind:
        issues.error(f"{label}.evidence_kind does not match provenance.evidence_kind")
    expected = _validate_value_map(f"{label}.expected", assertion.get("expected"), issues)
    observed = _validate_value_map(f"{label}.observed", assertion.get("observed"), issues)
    applicable = assertion.get("applicable")
    required_flag = assertion.get("required")
    if applicable is False:
        if not matrix_optional:
            issues.error(f"{label} is not centrally optional")
        if required_flag is not False:
            issues.error(f"{label} marked not applicable must not be required")
        if result != "NOT_APPLICABLE":
            issues.error(f"{label} marked not applicable must report NOT_APPLICABLE")
        if assertion.get("executed") is not False or assertion.get("live_executed") is not False:
            issues.error(f"{label} marked not applicable cannot claim execution")
        return
    if matrix_required and required_flag is not True:
        issues.error(f"{label} is mandatory in the central profile matrix")
    if applicable is True and (assertion.get("executed") is not True or assertion.get("live_executed") is not True):
        issues.partial(f"{label} lacks required live execution")
    if applicable is True and result != "PASS":
        issues.partial(f"{label} is not a PASS assertion")
    if applicable is True and evidence_kind not in LIVE_EVIDENCE_KINDS and not (
        allow_fixture_evidence and evidence_kind == "canonical_fixture"
    ):
        issues.error(f"{label} must bind live execution to live evidence")
    if expected is not None and observed is not None:
        _expected_matches_observed(expected, observed, label, issues)


def _validate_runtime(
    value: object,
    requirements: Mapping[str, Any] | None,
    issues: _Issues,
    *,
    allow_partial: bool,
    provenance_evidence_kind: object,
    allow_fixture_evidence: bool,
) -> dict[str, Any] | None:
    runtime = _as_mapping(value, "runtime", issues)
    if runtime is None:
        return None
    required = set(RUNTIME_REQUIRED_ASSERTIONS) | {"runtime_status"}
    missing = sorted(required - set(runtime))
    unexpected = sorted(set(runtime) - required - set(RUNTIME_OPTIONAL_ASSERTIONS))
    if missing:
        if allow_partial:
            issues.partial(f"runtime is missing required fields: {', '.join(missing)}")
        else:
            issues.error(f"runtime is missing required fields: {', '.join(missing)}")
    if unexpected:
        issues.error(f"runtime contains unsupported fields: {', '.join(unexpected)}")
    runtime_status = runtime.get("runtime_status")
    if runtime_status not in RUNTIME_STATUSES:
        issues.error("runtime.runtime_status uses an unsupported status")
    case_ids: set[str] = set()
    for name in RUNTIME_REQUIRED_ASSERTIONS:
        if name not in runtime:
            continue
        _validate_assertion(
            runtime.get(name),
            f"runtime.{name}",
            issues,
            matrix_required=True,
            matrix_optional=False,
            provenance_evidence_kind=provenance_evidence_kind,
            allow_fixture_evidence=allow_fixture_evidence,
        )
        candidate = runtime.get(name)
        if isinstance(candidate, Mapping) and isinstance(candidate.get("case_id"), str):
            case_id = candidate["case_id"]
            if case_id in case_ids:
                issues.error("runtime assertion case IDs are contradictory")
            case_ids.add(case_id)
    if "bypass_case" in runtime:
        _validate_assertion(
            runtime["bypass_case"],
            "runtime.bypass_case",
            issues,
            matrix_required=False,
            matrix_optional=True,
            provenance_evidence_kind=provenance_evidence_kind,
            allow_fixture_evidence=allow_fixture_evidence,
        )
        candidate = runtime.get("bypass_case")
        if isinstance(candidate, Mapping) and isinstance(candidate.get("case_id"), str):
            case_id = candidate["case_id"]
            if case_id in case_ids:
                issues.error("runtime assertion case IDs are contradictory")
    if runtime_status == "PASS":
        return runtime
    if runtime_status in {"PARTIAL", "VALIDATION_FAILED"}:
        issues.partial("runtime aggregate is not PASS")
    elif runtime_status == "FAIL":
        issues.error("runtime aggregate reports FAIL")
    return runtime


def _validate_framework_expectation(
    expectation_value: object,
    observation_value: object,
    issues: _Issues,
) -> None:
    expectation = _as_mapping(expectation_value, "framework.expectation", issues)
    observation = _validate_value_map("framework.observation", observation_value, issues)
    if expectation is None:
        return
    kind = expectation.get("kind")
    if kind not in EXPECTATION_KINDS:
        issues.error("framework.expectation.kind is unsupported")
        return
    expected = dict(expectation)
    expected.pop("kind", None)
    if kind in {"http_status", "intervention"}:
        if not _is_bounded_integer(expected.get("http_status"), lower=100, upper=599):
            issues.error("framework HTTP expectation requires a bounded http_status")
    if kind == "intervention":
        if not _safe_token(expected.get("action")):
            issues.error("framework intervention expectation requires action")
        rules = expected.get("rule_ids")
        if not isinstance(rules, list) or not rules:
            issues.error("framework intervention expectation requires rule_ids")
    if kind == "action" and not _safe_token(expected.get("action")):
        issues.error("framework action expectation requires action")
    if kind == "rule_match":
        rules = expected.get("rule_ids")
        if not isinstance(rules, list) or not rules:
            issues.error("framework rule_match expectation requires rule_ids")
    if kind == "rule_id" and not _is_bounded_integer(
        expected.get("value"), lower=1, upper=2_147_483_647
    ):
        issues.error("framework rule_id expectation requires a bounded value")
    if kind in {"event", "lifecycle", "cleanup", "compound"} and not expected:
        issues.error(f"framework {kind} expectation must declare a typed predicate")
    if kind == "not_applicable" and expected:
        issues.error("not_applicable expectation must not carry an expected value")
    if kind == "not_applicable":
        issues.error("framework expectation cannot be not_applicable in the central profile matrix")
    _validate_value_map("framework.expectation", expected or {"kind": kind}, issues)
    if observation is not None and kind != "not_applicable":
        _expected_matches_observed(expected, observation, "framework", issues)


def _validate_framework(
    value: object,
    requirements: Mapping[str, Any] | None,
    issues: _Issues,
) -> dict[str, Any] | None:
    framework = _as_mapping(value, "framework", issues)
    if framework is None:
        return None
    required = {
        "framework_test_id",
        "scenario_category",
        "selected",
        "executed",
        "live_executed",
        "expectation",
        "observation",
        "result",
        "validation_status",
        "failure_count",
        "mismatch_count",
    }
    _require_exact_keys(framework, required, {"framework_test_ids"}, "framework", issues)
    for field in ("framework_test_id", "scenario_category"):
        _check_string_field(framework, field, "framework", issues)
    allowed_categories = (
        requirements.get("framework_scenario_categories", frozenset())
        if requirements is not None
        else frozenset()
    )
    if allowed_categories and framework.get("scenario_category") not in allowed_categories:
        issues.error("framework.scenario_category contradicts the central profile matrix")
    declared_ids = framework.get("framework_test_ids")
    if declared_ids is not None:
        if (
            not isinstance(declared_ids, list)
            or len(declared_ids) != 1
            or declared_ids[0] != framework.get("framework_test_id")
        ):
            issues.error("framework test IDs are contradictory")
    for field in ("selected", "executed", "live_executed"):
        if not _is_boolean(framework.get(field)):
            issues.error(f"framework.{field} must be a boolean")
    if framework.get("result") not in ASSERTION_RESULTS:
        issues.error("framework.result uses an unsupported status")
    validation_status = framework.get("validation_status")
    if validation_status not in VALIDATION_STATUSES:
        issues.error("framework.validation_status uses an unsupported status")
    for field in ("failure_count", "mismatch_count"):
        if not _is_bounded_integer(framework.get(field)):
            issues.error(f"framework.{field} must be a bounded integer")
    _validate_framework_expectation(framework.get("expectation"), framework.get("observation"), issues)
    for field in ("selected", "executed", "live_executed"):
        if framework.get(field) is not True:
            issues.partial(f"framework.{field} is required for a runtime PASS")
    if framework.get("result") != "PASS":
        issues.partial("framework result is not PASS")
    if validation_status != "CONTRACT_VALIDATED":
        issues.partial("framework validation_status is not CONTRACT_VALIDATED")
    if framework.get("failure_count") != 0 or framework.get("mismatch_count") != 0:
        issues.partial("framework failure_count or mismatch_count is non-zero")
    return framework


def _validate_isolation(value: object, requirements: Mapping[str, Any] | None, issues: _Issues) -> None:
    isolation = _as_mapping(value, "isolation", issues)
    if isolation is None:
        return
    _require_exact_keys(isolation, set(ISOLATION_FIELDS), set(), "isolation", issues)
    expected_values = requirements.get("isolation", {}) if requirements is not None else {}
    for field in ISOLATION_FIELDS:
        actual = isolation.get(field)
        if not _is_boolean(actual):
            issues.error(f"isolation.{field} must be a boolean")
        elif field in expected_values and actual is not expected_values[field]:
            issues.error(f"isolation.{field} contradicts the central profile matrix")


def _validate_cleanup(value: object, issues: _Issues) -> dict[str, Any] | None:
    cleanup = _as_mapping(value, "cleanup", issues)
    if cleanup is None:
        return None
    required = set(CLEANUP_COUNTERS) | {"cleanup_status"}
    _require_exact_keys(cleanup, required, set(), "cleanup", issues)
    for field in CLEANUP_COUNTERS:
        if not _is_bounded_integer(cleanup.get(field)):
            issues.error(f"cleanup.{field} must be a bounded integer")
    if cleanup.get("cleanup_status") not in {"PASS", "PARTIAL", "FAIL"}:
        issues.error("cleanup.cleanup_status uses an unsupported status")
    residual = any(cleanup.get(field) not in {0, None} for field in CLEANUP_COUNTERS)
    if residual:
        issues.partial("cleanup residue prevents a runtime PASS")
    if cleanup.get("cleanup_status") != "PASS":
        issues.partial("cleanup status is not PASS")
    return cleanup


def _safe_relative_evidence_path(value: object) -> bool:
    if not isinstance(value, str) or not value or len(value) > 512:
        return False
    if _is_absolute_path_text(value) or "\\" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and all(part not in {"", ".", ".."} for part in path.parts)


def _validate_producer_binding(
    identity: Mapping[str, Any] | None,
    provenance: Mapping[str, Any],
    policy: Mapping[str, Any],
    issues: _Issues,
) -> None:
    """Bind a producer, connector, and evidence class before any PASS is possible."""
    if identity is None:
        return
    connector = identity.get("connector")
    producer = identity.get("producer")
    producer_version = identity.get("producer_version")
    evidence_kind = provenance.get("evidence_kind")
    if producer_version != PRODUCER_VERSION:
        issues.error("identity.producer_version is not an approved contract producer version")
    if connector == "nginx":
        if producer != LIVE_PRODUCERS["nginx"]:
            issues.error("identity.producer is not approved for the protected NGINX boundary")
        if evidence_kind != "protected_runtime_evidence":
            issues.error("provenance.evidence_kind is not approved for the protected NGINX boundary")
        return
    if evidence_kind == "canonical_fixture":
        expected = f"canonical-runtime-fixture-{connector}"
        if producer != expected:
            issues.error("fixture evidence is not bound to its connector fixture producer")
        if not policy["allow_fixture_evidence"]:
            issues.error("fixture evidence is forbidden by the strict runtime policy")
        return
    if connector in {"apache", "haproxy"}:
        issues.error(f"{connector} has no approved live runtime producer")
        return
    expected_producer = LIVE_PRODUCERS.get(str(connector))
    if producer != expected_producer:
        issues.error("identity.producer is not approved for the connector")
    expected_kind = "protected_runtime_evidence" if connector == "nginx" else "structured_connector_evidence"
    if evidence_kind != expected_kind:
        issues.error("provenance.evidence_kind is not approved for the connector producer")


def _validate_provenance(
    value: object,
    identity: Mapping[str, Any] | None,
    policy: Mapping[str, Any],
    issues: _Issues,
) -> dict[str, Any] | None:
    provenance = _as_mapping(value, "provenance", issues)
    if provenance is None:
        return None
    required = {
        "evidence_kind",
        "fixture_id",
        "source_contract",
        "manifest_digest",
        "evidence_digest",
        "contract_schema_version",
        "producer_version",
        "evidence",
    }
    _require_exact_keys(
        provenance,
        required,
        {"validation_timestamp", "validation_basis"},
        "provenance",
        issues,
    )
    if "validation_timestamp" not in provenance and "validation_basis" not in provenance:
        issues.error("provenance needs a timestamp or deterministic validation basis")
    if "validation_timestamp" in provenance and (
        not isinstance(provenance["validation_timestamp"], str)
        or TIMESTAMP.fullmatch(provenance["validation_timestamp"]) is None
    ):
        issues.error("provenance.validation_timestamp is not an ISO-8601 UTC timestamp")
    if "validation_basis" in provenance and provenance["validation_basis"] != "evidence-digest-v1":
        issues.error("provenance.validation_basis is unsupported")
    evidence_kind = provenance.get("evidence_kind")
    if evidence_kind not in CANONICAL_EVIDENCE_KINDS:
        issues.error("provenance.evidence_kind is not canonical")
    if evidence_kind in RAW_EVIDENCE_KINDS:
        issues.error("provenance.evidence_kind cannot name raw or synthetic evidence")
    for field in ("fixture_id", "source_contract", "producer_version"):
        _check_string_field(provenance, field, "provenance", issues)
    for field in ("manifest_digest", "evidence_digest"):
        digest = provenance.get(field)
        if not isinstance(digest, str) or SHA256.fullmatch(digest) is None:
            issues.error(f"provenance.{field} must be a SHA-256 digest")
    if provenance.get("contract_schema_version") != SCHEMA_VERSION:
        issues.error("provenance.contract_schema_version does not match schema_version")
    if identity is not None and provenance.get("producer_version") != identity.get("producer_version"):
        issues.error("provenance.producer_version does not match identity.producer_version")
    _validate_producer_binding(identity, provenance, policy, issues)
    evidence = provenance.get("evidence")
    valid_records: list[dict[str, Any]] = []
    if not isinstance(evidence, list) or not evidence or len(evidence) > MAX_EVIDENCE_FILES:
        issues.error("provenance.evidence must be a bounded non-empty list")
    else:
        names: set[str] = set()
        paths: set[str] = set()
        has_bound_evidence = False
        for index, item in enumerate(evidence):
            record = _as_mapping(item, f"provenance.evidence[{index}]", issues)
            if record is None:
                continue
            _require_exact_keys(record, {"name", "path", "sha256", "kind"}, set(), f"provenance.evidence[{index}]", issues)
            if not _safe_token(record.get("name")):
                issues.error(f"provenance.evidence[{index}].name must be a bounded token")
            if not _safe_relative_evidence_path(record.get("path")):
                issues.error(f"provenance.evidence[{index}].path must be a safe relative path")
            digest = record.get("sha256")
            if not isinstance(digest, str) or SHA256.fullmatch(digest) is None:
                issues.error(f"provenance.evidence[{index}].sha256 must be a SHA-256 digest")
            if record.get("kind") not in LIVE_EVIDENCE_KINDS | frozenset(("canonical_fixture", "manifest")):
                issues.error(f"provenance.evidence[{index}].kind is not a canonical evidence kind")
            if record.get("kind") == "canonical_fixture" and evidence_kind != "canonical_fixture":
                issues.error("fixture evidence record cannot support a live runtime claim")
            if record.get("kind") in LIVE_EVIDENCE_KINDS and evidence_kind == "canonical_fixture":
                issues.error("live evidence record cannot be relabelled as a fixture")
            if record.get("kind") != "manifest" and record.get("kind") != evidence_kind:
                issues.error("provenance evidence record kind does not match the producer evidence kind")
            if record.get("kind") == evidence_kind:
                has_bound_evidence = True
            name = record.get("name")
            path = record.get("path")
            if isinstance(name, str) and name in names:
                issues.error("provenance.evidence contains duplicate names")
            if isinstance(path, str) and path in paths:
                issues.error("provenance.evidence contains duplicate paths")
            if isinstance(name, str):
                names.add(name)
            if isinstance(path, str):
                paths.add(path)
            valid_records.append(record)
        if not has_bound_evidence:
            issues.error("provenance.evidence needs connector-bound evidence, not only a manifest")
    if valid_records and provenance.get("evidence_digest") != evidence_manifest_digest(valid_records):
        issues.error("provenance.evidence_digest does not bind the evidence inventory")
    if _has_forbidden_metadata(provenance):
        issues.error("provenance contains raw-log, payload, or absolute-path metadata")
    evidence_root = policy.get("evidence_root")
    if evidence_root is None and evidence_kind != "canonical_fixture":
        if policy["allow_partial"]:
            issues.partial("live runtime evidence requires a private evidence root")
        else:
            issues.error("live runtime evidence requires a private evidence root")
    elif evidence_root is not None and valid_records:
        try:
            root = _path_from_value(evidence_root)
            for record in valid_records:
                path = root / str(record["path"])
                data = read_bounded_evidence_file(path, root, label="referenced evidence")
                if hashlib.sha256(data).hexdigest() != record["sha256"]:
                    issues.error("referenced evidence digest does not match")
        except (ObservationInputError, OSError):
            # Do not leak a host path from an OS exception into the canonical
            # validation result. Missing or unreadable bound evidence is a
            # validation failure, never an in-process exception or a PASS.
            issues.error("referenced evidence is unavailable or unsafe")
    return provenance


def _observation_digest(value: object) -> str | None:
    try:
        return hashlib.sha256(canonical_json(value)).hexdigest()
    except (TypeError, ValueError):
        return None


def validate_runtime_observation(
    observation: object,
    expected_identity: Mapping[str, Any] | None,
    policy: str | Mapping[str, Any] | None = "strict",
) -> ValidationResult:
    """Validate one canonical observation and return a bounded canonical result.

    The API deliberately reports validation failures as data so a workflow can
    retain a bounded, non-payload diagnostic record.  Callers must use
    ``status == 'PASS'`` as the only success condition.
    """
    normalized_policy = _normalise_policy(policy)
    issues = _Issues()
    document = _as_mapping(observation, "runtime observation", issues)
    identity: dict[str, Any] | None = None
    runtime: dict[str, Any] | None = None
    provenance: dict[str, Any] | None = None
    if document is not None:
        _require_exact_keys(
            document,
            {"schema_version", "identity", "runtime", "framework", "isolation", "cleanup", "provenance"},
            set(),
            "runtime observation",
            issues,
        )
        if document.get("schema_version") != SCHEMA_VERSION:
            issues.error("schema_version is unsupported")
        identity = _validate_identity(document.get("identity"), expected_identity, issues)
        profile = identity.get("profile") if identity is not None else None
        requirements = PROFILE_REQUIREMENTS.get(profile) if isinstance(profile, str) else None
        provenance_hint = document.get("provenance")
        provenance_evidence_kind = (
            provenance_hint.get("evidence_kind")
            if isinstance(provenance_hint, Mapping)
            else None
        )
        runtime = _validate_runtime(
            document.get("runtime"),
            requirements,
            issues,
            allow_partial=bool(normalized_policy["allow_partial"]),
            provenance_evidence_kind=provenance_evidence_kind,
            allow_fixture_evidence=bool(normalized_policy["allow_fixture_evidence"]),
        )
        _validate_framework(document.get("framework"), requirements, issues)
        _validate_isolation(document.get("isolation"), requirements, issues)
        _validate_cleanup(document.get("cleanup"), issues)
        provenance = _validate_provenance(document.get("provenance"), identity, normalized_policy, issues)
    if issues.hard:
        status = "VALIDATION_FAILED"
        validation_status = "VALIDATION_FAILED"
    elif issues.incomplete:
        status = "PARTIAL" if normalized_policy["allow_partial"] else "VALIDATION_FAILED"
        validation_status = "PARTIAL" if status == "PARTIAL" else "VALIDATION_FAILED"
    else:
        status = "PASS"
        validation_status = "CONTRACT_VALIDATED"
    result: ValidationResult = ValidationResult({
        "schema_version": SCHEMA_VERSION,
        "result_type": "runtime_observation_validation",
        "status": status,
        "validation_status": validation_status,
        "policy": normalized_policy["name"],
        "failure_count": len(issues.hard),
        "incomplete_count": len(issues.incomplete),
        "errors": issues.all(),
        "observation_digest": _observation_digest(observation),
        "identity": {
            name: identity.get(name)
            for name in ("connector", "profile", "run_id", "parent_commit", "framework_commit", "mrts_commit")
        }
        if identity is not None
        else {},
    })
    if provenance is not None and provenance.get("evidence_kind") == "canonical_fixture":
        result["evidence_disposition"] = "fixture_only"
    else:
        result["evidence_disposition"] = "runtime_evidence" if status == "PASS" else "not_validated"
    if runtime is not None:
        result["declared_runtime_status"] = runtime.get("runtime_status")
    return result
