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
CANONICAL_EVIDENCE_RECORD_KINDS = LIVE_EVIDENCE_KINDS | frozenset(
    ("canonical_fixture", "manifest")
)
CONTRACT_VALIDATED = "CONTRACT_VALIDATED"
VALIDATION_FAILED = "VALIDATION_FAILED"
PARTIAL = "PARTIAL"
NOT_APPLICABLE = "NOT_APPLICABLE"
RUNTIME_OBSERVATION_LABEL = "runtime observation"

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
        "isolation": dict.fromkeys(ISOLATION_FIELDS, mrts),
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
    if type(value) is not int:
        return False
    integer_value = int(value)
    return lower <= integer_value <= upper


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
    data = read_bounded_evidence_file(path, evidence_root, label=RUNTIME_OBSERVATION_LABEL)
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


def _validate_scalar_value_fields(
    label: str, mapping: Mapping[str, Any], issues: _Issues
) -> None:
    for name, item in mapping.items():
        if name not in SEMANTIC_VALUE_FIELDS:
            issues.error(f"{label}.{name} is not a supported typed semantic field")
        elif name not in {"rule_ids", "predicates"} and not (
            (item is None and name == "value")
            or _is_boolean(item)
            or _is_bounded_integer(item, lower=-MAX_COUNTER, upper=MAX_COUNTER)
            or (isinstance(item, str) and _safe_token(item))
        ):
            issues.error(f"{label}.{name} must be a bounded scalar semantic value")


def _validate_value_map_rules(label: str, mapping: Mapping[str, Any], issues: _Issues) -> None:
    http_status = mapping.get("http_status")
    if http_status is not None and not _is_bounded_integer(http_status, lower=100, upper=599):
        issues.error(f"{label}.http_status must be a bounded integer")
    for name in ("action", "intervention", "event", "transport"):
        if name in mapping and not _safe_token(mapping[name]):
            issues.error(f"{label}.{name} must be a bounded token")
    rules = mapping.get("rule_ids")
    if "rule_ids" in mapping and (
        not isinstance(rules, list)
        or not rules
        or len(rules) > 64
        or any(not _is_bounded_integer(rule, lower=1, upper=2_147_483_647) for rule in rules)
        or len(set(rules)) != len(rules)
    ):
        issues.error(f"{label}.rule_ids must be a unique bounded integer list")


def _validate_predicates(label: str, predicates: object, issues: _Issues) -> None:
    if not isinstance(predicates, Mapping) or not predicates:
        issues.error(f"{label}.predicates must be a non-empty object")
        return
    for name, predicate in predicates.items():
        safe = (
            _safe_token(name)
            and (
                _is_boolean(predicate)
                or _is_bounded_integer(predicate, lower=-MAX_COUNTER, upper=MAX_COUNTER)
                or (isinstance(predicate, str) and _safe_token(predicate))
            )
        )
        if not safe:
            issues.error(f"{label}.predicates contains an unsafe value")
            break


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
    _validate_scalar_value_fields(label, mapping, issues)
    _validate_value_map_rules(label, mapping, issues)
    if "predicates" in mapping:
        _validate_predicates(label, mapping["predicates"], issues)
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
    _validate_identity_contract(identity, issues)
    _validate_identity_profile(identity, issues)
    _validate_identity_commits(identity, issues)
    _validate_expected_identity(identity, expected_identity, issues)
    return identity


def _validate_identity_contract(identity: Mapping[str, Any], issues: _Issues) -> None:
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


def _validate_identity_profile(identity: Mapping[str, Any], issues: _Issues) -> None:
    profile = identity.get("profile")
    requirements = _profile_requirements_for_identity(profile, issues)
    for field in ("crs", "mrts"):
        if not _is_boolean(identity.get(field)):
            issues.error(f"identity.{field} must be a boolean")
    if requirements is not None:
        for field in ("crs", "mrts"):
            if identity.get(field) is not requirements[field]:
                issues.error(f"identity.{field} contradicts identity.profile")


def _validate_identity_commits(identity: Mapping[str, Any], issues: _Issues) -> None:
    for field in ("parent_commit", "framework_commit", "mrts_commit"):
        value = identity.get(field)
        if not isinstance(value, str) or COMMIT.fullmatch(value) is None:
            issues.error(f"identity.{field} must be a lowercase full commit")


def _validate_expected_identity(
    identity: Mapping[str, Any],
    expected_identity: Mapping[str, Any] | None,
    issues: _Issues,
) -> None:
    if expected_identity is None:
        return
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


def _profile_requirements_for_identity(
    profile: object, issues: _Issues
) -> Mapping[str, Any] | None:
    if profile not in PROFILES:
        issues.error("identity.profile is not a supported profile")
        return None
    return PROFILE_REQUIREMENTS[str(profile)]


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
    if _validate_not_applicable_assertion(assertion, label, result, issues, matrix_optional):
        return
    _validate_applicable_assertion(
        assertion,
        label,
        result,
        evidence_kind,
        issues,
        matrix_required=matrix_required,
        allow_fixture_evidence=allow_fixture_evidence,
    )
    if expected is not None and observed is not None:
        _expected_matches_observed(expected, observed, label, issues)


def _validate_not_applicable_assertion(
    assertion: Mapping[str, Any],
    label: str,
    result: object,
    issues: _Issues,
    matrix_optional: bool,
) -> bool:
    if assertion.get("applicable") is not False:
        return False
    if not matrix_optional:
        issues.error(f"{label} is not centrally optional")
    if assertion.get("required") is not False:
        issues.error(f"{label} marked not applicable must not be required")
    if result != "NOT_APPLICABLE":
        issues.error(f"{label} marked not applicable must report NOT_APPLICABLE")
    if assertion.get("executed") is not False or assertion.get("live_executed") is not False:
        issues.error(f"{label} marked not applicable cannot claim execution")
    return True


def _validate_applicable_assertion(
    assertion: Mapping[str, Any],
    label: str,
    result: object,
    evidence_kind: object,
    issues: _Issues,
    *,
    matrix_required: bool,
    allow_fixture_evidence: bool,
) -> None:
    if matrix_required and assertion.get("required") is not True:
        issues.error(f"{label} is mandatory in the central profile matrix")
    if assertion.get("applicable") is not True:
        return
    if assertion.get("executed") is not True or assertion.get("live_executed") is not True:
        issues.partial(f"{label} lacks required live execution")
    if result != "PASS":
        issues.partial(f"{label} is not a PASS assertion")
    fixture_allowed = allow_fixture_evidence and evidence_kind == "canonical_fixture"
    if evidence_kind not in LIVE_EVIDENCE_KINDS and not fixture_allowed:
        issues.error(f"{label} must bind live execution to live evidence")


def _validate_runtime(
    value: object,
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
    _validate_runtime_assertions(
        runtime,
        issues,
        provenance_evidence_kind,
        allow_fixture_evidence,
    )
    if runtime_status != "PASS":
        _validate_runtime_aggregate(runtime_status, issues)
    return runtime


def _validate_runtime_assertions(
    runtime: Mapping[str, Any],
    issues: _Issues,
    provenance_evidence_kind: object,
    allow_fixture_evidence: bool,
) -> None:
    case_ids: set[str] = set()
    for name in RUNTIME_REQUIRED_ASSERTIONS:
        if name in runtime:
            _validate_assertion(
                runtime.get(name),
                f"runtime.{name}",
                issues,
                matrix_required=True,
                matrix_optional=False,
                provenance_evidence_kind=provenance_evidence_kind,
                allow_fixture_evidence=allow_fixture_evidence,
            )
            _record_case_id(runtime.get(name), case_ids, issues)
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
        _record_case_id(runtime["bypass_case"], case_ids, issues)


def _record_case_id(candidate: object, case_ids: set[str], issues: _Issues) -> None:
    if not isinstance(candidate, Mapping) or not isinstance(candidate.get("case_id"), str):
        return
    case_id = candidate["case_id"]
    if case_id in case_ids:
        issues.error("runtime assertion case IDs are contradictory")
    case_ids.add(case_id)


def _validate_runtime_aggregate(runtime_status: object, issues: _Issues) -> None:
    if runtime_status in {"PARTIAL", "VALIDATION_FAILED"}:
        issues.partial("runtime aggregate is not PASS")
    elif runtime_status == "FAIL":
        issues.error("runtime aggregate reports FAIL")


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
    _validate_framework_expectation_kind(kind, expected, issues)
    _validate_value_map("framework.expectation", expected or {"kind": kind}, issues)
    if observation is not None and kind != "not_applicable":
        _expected_matches_observed(expected, observation, "framework", issues)


def _validate_framework_expectation_kind(
    kind: object, expected: Mapping[str, Any], issues: _Issues
) -> None:
    if kind in {"http_status", "intervention"} and not _is_bounded_integer(
        expected.get("http_status"), lower=100, upper=599
    ):
        issues.error("framework HTTP expectation requires a bounded http_status")
    if kind == "intervention":
        if not _safe_token(expected.get("action")):
            issues.error("framework intervention expectation requires action")
        _require_nonempty_rule_ids("framework intervention expectation requires rule_ids", expected, issues)
    if kind == "action" and not _safe_token(expected.get("action")):
        issues.error("framework action expectation requires action")
    if kind == "rule_match":
        _require_nonempty_rule_ids("framework rule_match expectation requires rule_ids", expected, issues)
    if kind == "rule_id" and not _is_bounded_integer(
        expected.get("value"), lower=1, upper=2_147_483_647
    ):
        issues.error("framework rule_id expectation requires a bounded value")
    if kind in {"event", "lifecycle", "cleanup", "compound"} and not expected:
        issues.error(f"framework {kind} expectation must declare a typed predicate")
    if kind == "not_applicable":
        if expected:
            issues.error("not_applicable expectation must not carry an expected value")
        issues.error("framework expectation cannot be not_applicable in the central profile matrix")


def _require_nonempty_rule_ids(message: str, expected: Mapping[str, Any], issues: _Issues) -> None:
    rules = expected.get("rule_ids")
    if not isinstance(rules, list) or not rules:
        issues.error(message)


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
    _validate_framework_identity(framework, requirements, issues)
    validation_status = _validate_framework_status(framework, issues)
    _validate_framework_expectation(framework.get("expectation"), framework.get("observation"), issues)
    _validate_framework_disposition(framework, validation_status, issues)
    return framework


def _validate_framework_identity(
    framework: Mapping[str, Any],
    requirements: Mapping[str, Any] | None,
    issues: _Issues,
) -> None:
    for field in ("framework_test_id", "scenario_category"):
        _check_string_field(framework, field, "framework", issues)
    allowed_categories = _framework_allowed_categories(requirements)
    if allowed_categories and framework.get("scenario_category") not in allowed_categories:
        issues.error("framework.scenario_category contradicts the central profile matrix")
    declared_ids = framework.get("framework_test_ids")
    if declared_ids is not None and (
        not isinstance(declared_ids, list)
        or len(declared_ids) != 1
        or declared_ids[0] != framework.get("framework_test_id")
    ):
        issues.error("framework test IDs are contradictory")
    _validate_framework_boolean_fields(framework, issues)


def _validate_framework_status(
    framework: Mapping[str, Any], issues: _Issues
) -> object:
    if framework.get("result") not in ASSERTION_RESULTS:
        issues.error("framework.result uses an unsupported status")
    validation_status = framework.get("validation_status")
    if validation_status not in VALIDATION_STATUSES:
        issues.error("framework.validation_status uses an unsupported status")
    for field in ("failure_count", "mismatch_count"):
        if not _is_bounded_integer(framework.get(field)):
            issues.error(f"framework.{field} must be a bounded integer")
    return validation_status


def _validate_framework_disposition(
    framework: Mapping[str, Any], validation_status: object, issues: _Issues
) -> None:
    for field in ("selected", "executed", "live_executed"):
        if framework.get(field) is not True:
            issues.partial(f"framework.{field} is required for a runtime PASS")
    if framework.get("result") != "PASS":
        issues.partial("framework result is not PASS")
    if validation_status != "CONTRACT_VALIDATED":
        issues.partial("framework validation_status is not CONTRACT_VALIDATED")
    if framework.get("failure_count") != 0 or framework.get("mismatch_count") != 0:
        issues.partial("framework failure_count or mismatch_count is non-zero")


def _framework_allowed_categories(requirements: Mapping[str, Any] | None) -> frozenset[str]:
    if requirements is None:
        return frozenset()
    return requirements.get("framework_scenario_categories", frozenset())


def _validate_framework_boolean_fields(
    framework: Mapping[str, Any], issues: _Issues
) -> None:
    for field in ("selected", "executed", "live_executed"):
        if not _is_boolean(framework.get(field)):
            issues.error(f"framework.{field} must be a boolean")


def _validate_isolation(value: object, requirements: Mapping[str, Any] | None, issues: _Issues) -> None:
    isolation = _as_mapping(value, "isolation", issues)
    if isolation is None:
        return
    _require_exact_keys(isolation, set(ISOLATION_FIELDS), set(), "isolation", issues)
    expected_values = requirements.get("isolation", {}) if requirements is not None else {}
    for field in ISOLATION_FIELDS:
        _validate_isolation_field(field, isolation.get(field), expected_values, issues)


def _validate_isolation_field(
    field: str,
    actual: object,
    expected_values: Mapping[str, Any],
    issues: _Issues,
) -> None:
    if not _is_boolean(actual):
        issues.error(f"isolation.{field} must be a boolean")
        return
    if field in expected_values and actual is not expected_values[field]:
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
        _validate_nginx_producer(producer, evidence_kind, issues)
        return
    if evidence_kind == "canonical_fixture":
        _validate_fixture_producer(connector, producer, policy, issues)
        return
    if connector in {"apache", "haproxy"}:
        _validate_unsupported_live_producer(connector, issues)
        return
    _validate_live_producer(connector, producer, evidence_kind, issues)


def _validate_nginx_producer(
    producer: object, evidence_kind: object, issues: _Issues
) -> None:
    if producer != LIVE_PRODUCERS["nginx"]:
        issues.error("identity.producer is not approved for the protected NGINX boundary")
    if evidence_kind != "protected_runtime_evidence":
        issues.error("provenance.evidence_kind is not approved for the protected NGINX boundary")


def _validate_fixture_producer(
    connector: object,
    producer: object,
    policy: Mapping[str, Any],
    issues: _Issues,
) -> None:
    expected = f"canonical-runtime-fixture-{connector}"
    if producer != expected:
        issues.error("fixture evidence is not bound to its connector fixture producer")
    if not policy["allow_fixture_evidence"]:
        issues.error("fixture evidence is forbidden by the strict runtime policy")


def _validate_unsupported_live_producer(connector: object, issues: _Issues) -> None:
    issues.error(f"{connector} has no approved live runtime producer")


def _validate_live_producer(
    connector: object,
    producer: object,
    evidence_kind: object,
    issues: _Issues,
) -> None:
    expected_producer = LIVE_PRODUCERS.get(str(connector))
    if producer != expected_producer:
        issues.error("identity.producer is not approved for the connector")
    expected_kind = "structured_connector_evidence"
    if evidence_kind != expected_kind:
        issues.error("provenance.evidence_kind is not approved for the connector producer")


def _validate_evidence_records(
    evidence: object,
    evidence_kind: object,
    issues: _Issues,
) -> list[dict[str, Any]]:
    valid_records: list[dict[str, Any]] = []
    if not isinstance(evidence, list) or not evidence or len(evidence) > MAX_EVIDENCE_FILES:
        issues.error("provenance.evidence must be a bounded non-empty list")
        return valid_records
    names: set[str] = set()
    paths: set[str] = set()
    has_bound_evidence = False
    for index, item in enumerate(evidence):
        record, is_bound = _validate_evidence_record(
            index, item, evidence_kind, names, paths, issues
        )
        if record is None:
            continue
        has_bound_evidence = has_bound_evidence or is_bound
        valid_records.append(record)
    if not has_bound_evidence:
        issues.error("provenance.evidence needs connector-bound evidence, not only a manifest")
    return valid_records


def _validate_evidence_record(
    index: int,
    item: object,
    evidence_kind: object,
    names: set[str],
    paths: set[str],
    issues: _Issues,
) -> tuple[dict[str, Any] | None, bool]:
    label = f"provenance.evidence[{index}]"
    record = _as_mapping(item, label, issues)
    if record is None:
        return None, False
    _require_exact_keys(record, {"name", "path", "sha256", "kind"}, set(), label, issues)
    if not _safe_token(record.get("name")):
        issues.error(f"{label}.name must be a bounded token")
    if not _safe_relative_evidence_path(record.get("path")):
        issues.error(f"{label}.path must be a safe relative path")
    digest = record.get("sha256")
    if not isinstance(digest, str) or SHA256.fullmatch(digest) is None:
        issues.error(f"{label}.sha256 must be a SHA-256 digest")
    _validate_evidence_record_kind(record.get("kind"), evidence_kind, label, issues)
    _validate_evidence_record_uniqueness(record, names, paths, issues)
    return record, record.get("kind") == evidence_kind


def _validate_evidence_record_uniqueness(
    record: Mapping[str, Any],
    names: set[str],
    paths: set[str],
    issues: _Issues,
) -> None:
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


def _validate_evidence_record_kind(
    record_kind: object, evidence_kind: object, label: str, issues: _Issues
) -> None:
    if record_kind not in CANONICAL_EVIDENCE_RECORD_KINDS:
        issues.error(f"{label}.kind is not a canonical evidence kind")
    if record_kind == "canonical_fixture" and evidence_kind != "canonical_fixture":
        issues.error("fixture evidence record cannot support a live runtime claim")
    if record_kind in LIVE_EVIDENCE_KINDS and evidence_kind == "canonical_fixture":
        issues.error("live evidence record cannot be relabelled as a fixture")
    if record_kind != "manifest" and record_kind != evidence_kind:
        issues.error("provenance evidence record kind does not match the producer evidence kind")


def _validate_referenced_evidence(
    evidence_root: object,
    records: list[dict[str, Any]],
    issues: _Issues,
) -> None:
    if evidence_root is None or not records:
        return
    try:
        root = _path_from_value(evidence_root)
        for record in records:
            path = root / str(record["path"])
            data = read_bounded_evidence_file(path, root, label="referenced evidence")
            if hashlib.sha256(data).hexdigest() != record["sha256"]:
                issues.error("referenced evidence digest does not match")
    except (ObservationInputError, OSError):
        # Do not leak a host path from an OS exception into the canonical
        # validation result. Missing or unreadable bound evidence is a
        # validation failure, never an in-process exception or a PASS.
        issues.error("referenced evidence is unavailable or unsafe")


def _validate_provenance(
    value: object,
    identity: Mapping[str, Any] | None,
    policy: Mapping[str, Any],
    issues: _Issues,
) -> dict[str, Any] | None:
    provenance = _as_mapping(value, "provenance", issues)
    if provenance is None:
        return None
    _validate_provenance_header(provenance, issues)
    _validate_provenance_kind(provenance, issues)
    _validate_provenance_fields(provenance, identity, issues)
    evidence_kind = provenance.get("evidence_kind")
    _validate_producer_binding(identity, provenance, policy, issues)
    valid_records = _validate_evidence_records(provenance.get("evidence"), evidence_kind, issues)
    if valid_records and provenance.get("evidence_digest") != evidence_manifest_digest(valid_records):
        issues.error("provenance.evidence_digest does not bind the evidence inventory")
    if _has_forbidden_metadata(provenance):
        issues.error("provenance contains raw-log, payload, or absolute-path metadata")
    _validate_provenance_evidence_root(provenance, evidence_kind, valid_records, policy, issues)
    return provenance


def _validate_provenance_header(
    provenance: Mapping[str, Any], issues: _Issues
) -> None:
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


def _validate_provenance_kind(provenance: Mapping[str, Any], issues: _Issues) -> None:
    evidence_kind = provenance.get("evidence_kind")
    if evidence_kind not in CANONICAL_EVIDENCE_KINDS:
        issues.error("provenance.evidence_kind is not canonical")
    if evidence_kind in RAW_EVIDENCE_KINDS:
        issues.error("provenance.evidence_kind cannot name raw or synthetic evidence")


def _validate_provenance_fields(
    provenance: Mapping[str, Any],
    identity: Mapping[str, Any] | None,
    issues: _Issues,
) -> None:
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


def _validate_provenance_evidence_root(
    provenance: Mapping[str, Any],
    evidence_kind: object,
    valid_records: list[dict[str, Any]],
    policy: Mapping[str, Any],
    issues: _Issues,
) -> None:
    evidence_root = policy.get("evidence_root")
    if evidence_root is None and evidence_kind != "canonical_fixture":
        if policy["allow_partial"]:
            issues.partial("live runtime evidence requires a private evidence root")
        else:
            issues.error("live runtime evidence requires a private evidence root")
    elif evidence_root is not None and valid_records:
        _validate_referenced_evidence(evidence_root, valid_records, issues)


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
    issues = _Issues()
    normalized_policy = _normalise_policy(policy)
    identity, runtime, provenance = _validate_document(
        observation, expected_identity, normalized_policy, issues
    )
    status, validation_status = _validation_status(issues, normalized_policy)
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
    _add_result_disposition(result, provenance, runtime, status)
    return result


def _validate_document(
    observation: object,
    expected_identity: Mapping[str, Any] | None,
    policy: Mapping[str, Any],
    issues: _Issues,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None, dict[str, Any] | None]:
    document = _as_mapping(observation, RUNTIME_OBSERVATION_LABEL, issues)
    if document is None:
        return None, None, None
    _require_exact_keys(
        document,
        {"schema_version", "identity", "runtime", "framework", "isolation", "cleanup", "provenance"},
        set(),
        RUNTIME_OBSERVATION_LABEL,
        issues,
    )
    if document.get("schema_version") != SCHEMA_VERSION:
        issues.error("schema_version is unsupported")
    identity = _validate_identity(document.get("identity"), expected_identity, issues)
    profile = identity.get("profile") if identity is not None else None
    requirements = PROFILE_REQUIREMENTS.get(profile) if isinstance(profile, str) else None
    provenance_hint = document.get("provenance")
    provenance_evidence_kind = (
        provenance_hint.get("evidence_kind") if isinstance(provenance_hint, Mapping) else None
    )
    runtime = _validate_runtime(
        document.get("runtime"),
        issues,
        allow_partial=bool(policy["allow_partial"]),
        provenance_evidence_kind=provenance_evidence_kind,
        allow_fixture_evidence=bool(policy["allow_fixture_evidence"]),
    )
    _validate_framework(document.get("framework"), requirements, issues)
    _validate_isolation(document.get("isolation"), requirements, issues)
    _validate_cleanup(document.get("cleanup"), issues)
    provenance = _validate_provenance(document.get("provenance"), identity, policy, issues)
    return identity, runtime, provenance


def _validation_status(issues: _Issues, policy: Mapping[str, Any]) -> tuple[str, str]:
    if issues.hard:
        return "VALIDATION_FAILED", "VALIDATION_FAILED"
    if issues.incomplete:
        status = "PARTIAL" if policy["allow_partial"] else "VALIDATION_FAILED"
        return status, "PARTIAL" if status == "PARTIAL" else "VALIDATION_FAILED"
    return "PASS", "CONTRACT_VALIDATED"


def _add_result_disposition(
    result: ValidationResult,
    provenance: Mapping[str, Any] | None,
    runtime: Mapping[str, Any] | None,
    status: str,
) -> None:
    if provenance is not None and provenance.get("evidence_kind") == "canonical_fixture":
        result["evidence_disposition"] = "fixture_only"
    else:
        result["evidence_disposition"] = "runtime_evidence" if status == "PASS" else "not_validated"
    if runtime is not None:
        result["declared_runtime_status"] = runtime.get("runtime_status")
