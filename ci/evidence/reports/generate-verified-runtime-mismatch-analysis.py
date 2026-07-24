#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

# CI helpers are shared from ci/lib even when this file is executed directly.
_CI_ROOT = next(parent for parent in Path(__file__).resolve().parents if parent.name == "ci")
if str(_CI_ROOT / "lib") not in sys.path:
    sys.path.insert(0, str(_CI_ROOT / "lib"))
from typing import Any

from generated_report_utils import (
    DATA_SOURCE_POLICY,
    GENERATED_REPORTS,
    build_metadata,
    current_verified_run_id,
    generated_json_text,
    generated_markdown_text,
    report_path,
    sha256_file,
    utc_now,
)
from runtime_path_utils import verified_runtime_paths
from verified_run_id import VerifiedRunIdError, validate_verified_run_id


CRITICAL_CATEGORIES = {
    "runtime_regression",
    "expected_status_mismatch",
    "connector_capability_gap",
    "framework_expected_behavior_gap",
    "environment_flake",
    "timeout_or_incomplete",
    "unknown",
}
DISRUPTIVE_EXPECTED_STATUSES = {"302", "401", "403", "406", "429", "503"}
MRTS_DETECTION_ONLY_CLASSIFICATION = "with_mrts_detection_only_overlay"
MRTS_DETECTION_ONLY_NOTE = "MRTS DetectionOnly overlay; disruptive smoke rule match is report-only"
HAPROXY_MRTS_DETECTION_ONLY_NOTE = "MRTS DetectionOnly overlay; HAProxy/SPOA decision evidence is report-only"
SECACTION_DETECTION_ONLY_CLASSIFICATION = "secaction_detection_only_overlay"
SECACTION_DETECTION_ONLY_CASE = "v3_secaction_block"
SECACTION_DETECTION_ONLY_RULE_ID = "3312"
SECACTION_DETECTION_ONLY_NOTE = (
    "MRTS DetectionOnly overlay suppresses the disruptive SecAction; no-MRTS and native controls block with rule 3312"
)
COLLECTION_SEMANTICS_CLASSIFICATION = "libmodsecurity_collection_semantics"
COLLECTION_SEMANTICS_NOTE = (
    "Semicolon query splitting is not exposed as ARGS_NAMES by observed libmodsecurity runtime; "
    "control ARGS_NAMES case passes."
)
COLLECTION_NAME_CASE_SEMANTICS_CLASSIFICATION = "libmodsecurity_collection_name_case_semantics"
COLLECTION_NAME_CASE_SEMANTICS_NOTE = (
    "Observed libmodsecurity runtime preserves request header/cookie collection-name case; "
    "exact-case REQUEST_HEADERS_NAMES/REQUEST_COOKIES_NAMES controls pass."
)
NOLOG_EXPECTED_NO_AUDIT_CLASSIFICATION = "nolog_expected_no_audit"
NOLOG_EXPECTED_NO_AUDIT_NOTE = (
    "Rule 3326 has explicit nolog/pass and is absent from audit, error, and decision logs; "
    "with-CRS audit entries are unrelated CRS noise."
)
TRANSFORMATION_NATIVE_SEMANTICS_CLASSIFICATION = "libmodsecurity_transformation_semantics"
TRANSFORMATION_NATIVE_SEMANTICS_NOTE = (
    "Connector-free libmodsecurity C API oracle returns the same non-disruptive status as all "
    "Apache, NGINX, and HAProxy full-matrix variants for this transformation fixture."
)
XML_PARSER_SEMANTICS_CLASSIFICATION = "libmodsecurity_xml_parser_semantics"
XML_PARSER_SEMANTICS_CASE = "xml_request_body_malformed_connector_gap"
XML_PARSER_SEMANTICS_NOTE = (
    "Malformed XML initializes the libmodsecurity XML parser and records a parse failure, but the "
    "fixture rule targets the XML collection and no XML collection rule match or parser-error "
    "intervention is produced. Apache, NGINX, and HAProxy match connector-free libmodsecurity."
)
NGINX_PHASE4_RESPONSE_BODY_ENFORCEMENT_CLASSIFICATION = "nginx_phase4_response_body_enforcement_gap"
NGINX_PHASE4_RESPONSE_BODY_ENFORCEMENT_NOTE = (
    "NGINX/libmodsecurity records a phase-4 RESPONSE_BODY disruptive match, but the current "
    "connector path does not turn the late response-body intervention into HTTP 403 for this fixture."
)
PHASE4_RULE_MATCH_NO_DISRUPTIVE_INTERVENTION_CLASSIFICATION = "phase4_rule_match_no_disruptive_intervention"
PHASE4_RULE_MATCH_NO_DISRUPTIVE_INTERVENTION_NOTE = (
    "The NGINX with-MRTS variant observes the RESPONSE_BODY rule match in the runtime error log, but "
    "MRTS_001_INIT sets ruleEngine=DetectionOnly so no connector phase-4 intervention event is emitted."
)
TRANSFORMATION_NATIVE_SEMANTICS_CASES = {
    "unicode_whitespace_normalization_gap",
    "unicode_double_encoded_uri_runtime_difference",
}
NGINX_PHASE4_RESPONSE_BODY_ENFORCEMENT_CASES = {
    "phase4_auditlog_outbound_escaped_value_gap": "4909",
    "phase4_auditlog_outbound_message_connector_gap": "4812",
    "phase4_auditlog_outbound_multiline_section_gap": "4910",
    "phase4_auditlog_outbound_rule_id_runtime_difference": "4811",
    "phase4_response_body_chunk_assumption_connector_gap": "4808",
    "phase4_response_body_empty_future_target": "4806",
    "phase4_response_body_html_entity_decode_gap": "4907",
    "phase4_response_body_html_text_normalization_probe": "4810",
    "phase4_response_body_unicode_runtime_difference": "4807",
    "pr70_phase4_response_body_audit_xfail": "5704",
    "response_body_basic_block": "1801",
}
NGINX_PHASE4_LOG_ONLY_CASES = {
    "nginx_phase4_content_type_out_of_scope": "920002",
    "nginx_phase4_minimal_log_only": "910001",
    "nginx_phase4_safe_log_only": "910002",
}
CRS_SQLI_WITH_MRTS_DETECTION_ONLY_CASE = "crs_sqli_anomaly_block"
CRS_SQLI_WITH_MRTS_RULE_IDS = {"942100", "942190", "942270", "942360", "949110"}
CRS_SQLI_WITH_MRTS_DETECTION_ONLY_NOTE = (
    "with-CRS/with-MRTS loads MRTS_001_INIT DetectionOnly; CRS SQLi/anomaly rules match and "
    "produce an intervention status 403, but disruptive actions are report-only in that overlay."
)
SEMICOLON_COLLECTION_CASES = {
    "duplicate_args_encoded_separator_edge",
    "edge_semicolon_query_args_names",
}
SEMICOLON_COLLECTION_CONNECTORS = {"apache", "haproxy", "nginx"}
SEMICOLON_COLLECTION_VARIANTS = {
    "no-crs/no-mrts",
    "no-crs/with-mrts",
    "with-crs/no-mrts",
    "with-crs/with-mrts",
}
ARGS_NAMES_CONTROL_CASE = "v3_args_names_get_block"
COLLECTION_NAME_CASE_CASES = {
    "duplicate_header_case_normalization_gap",
    "v3_request_cookies_names_case_runtime_difference",
    "v3_request_headers_names_lowercase_runtime_difference",
}
COLLECTION_NAME_CASE_CONTROL_CASES = {
    "duplicate_header_case_normalization_gap": "v3_request_headers_names_block",
    "v3_request_cookies_names_case_runtime_difference": "v3_request_cookies_names_block",
    "v3_request_headers_names_lowercase_runtime_difference": "v3_request_headers_names_block",
}
NOLOG_EXPECTED_NO_AUDIT_CASE = "v3_action_nolog_pass_no_audit"
NOLOG_EXPECTED_NO_AUDIT_RULE_ID = "3326"
MODSECURITY_SMOKE_FILE_RE = re.compile(r'\[file "([^"]*modsecurity-smoke\.conf)"\]')
RULES_ERROR_SMOKE_FILE_RE = re.compile(r"Rules error\. File: ([^.]*modsecurity-smoke\.conf)\.")
MODSECURITY_RULE_ID_RE = re.compile(r'\[id "([^"]+)"\]')
EMPTY_MULTIPART_OPERATOR_RE = re.compile(
    r'SecRule\s+(?:FILES|MULTIPART_FILENAME)\s+"@(?:contains|streq)\s*"\s+"id:(?:4701|4706)\b'
)
INCLUDE_RE = re.compile(r'^\s*Include\s+"([^"]+)"\s*$', re.MULTILINE)


def progress(message: str) -> None:
    if os.environ.get("DEBUG_MISMATCH_GENERATOR"):
        print(f"[mismatch-analysis] {message}", file=sys.stderr, flush=True)


def is_regular_file(path: Path) -> bool:
    try:
        return stat.S_ISREG(path.stat(follow_symlinks=False).st_mode)
    except OSError:
        return False


def directory_fingerprint(path: Path) -> str:
    digest = hashlib.sha256()
    seen = False
    for item in sorted(path.rglob("*")):
        try:
            item_stat = item.stat(follow_symlinks=False)
        except OSError:
            continue
        seen = True
        digest.update(str(item.relative_to(path)).encode("utf-8", errors="replace"))
        digest.update(b"\0")
        if stat.S_ISREG(item_stat.st_mode):
            digest.update(sha256_file(item).encode("ascii"))
        else:
            digest.update(f"special:{stat.S_IFMT(item_stat.st_mode):o}".encode("ascii"))
        digest.update(b"\0")
    return digest.hexdigest() if seen else "empty"


def input_record(path: Path, label: str) -> dict[str, Any]:
    if not path.exists():
        return {"path": str(path), "label": label, "status": "missing", "sha256": "missing"}
    if is_regular_file(path):
        return {
            "path": str(path),
            "label": label,
            "status": "present",
            "sha256": sha256_file(path),
            "bytes": path.stat().st_size,
        }
    if path.is_dir():
        return {
            "path": str(path),
            "label": label,
            "status": "present",
            "sha256": directory_fingerprint(path),
            "kind": "directory",
        }
    return {"path": str(path), "label": label, "status": "unknown", "sha256": "unknown"}


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return rows
    for line in lines:
        if not line.strip():
            continue
        try:
            data = json.loads(line)
        except Exception:
            continue
        if isinstance(data, dict):
            rows.append(data)
    return rows


def walk_dicts(value: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if isinstance(value, dict):
        rows.append(value)
        for child in value.values():
            rows.extend(walk_dicts(child))
    elif isinstance(value, list):
        for child in value:
            rows.extend(walk_dicts(child))
    return rows


def rel(path: str | Path, root: Path) -> str:
    item = Path(path)
    try:
        return str(item.resolve(strict=False).relative_to(root.resolve(strict=False)))
    except Exception:
        return str(path)


def resolve_recorded_path(value: str, *, connector_root: Path, build_root: Path) -> Path | None:
    if not value or value == "-":
        return None
    path = Path(value)
    if path.is_absolute():
        return path
    build_candidate = build_root / path
    if build_candidate.exists():
        return build_candidate
    connector_candidate = connector_root / path
    if connector_candidate.exists():
        return connector_candidate
    return build_candidate


def input_records_for_sources(
    *,
    commands_file: Path,
    manifest_path: Path,
    mismatches: list[dict[str, Any]],
    connector_root: Path,
    build_root: Path,
    native_semantics_inputs: list[Path] | None = None,
) -> list[dict[str, Any]]:
    records: list[tuple[Path, str]] = [
        (commands_file, "verified commands"),
        (manifest_path, "full matrix manifest"),
    ]
    seen = {str(commands_file), str(manifest_path)}
    for row in mismatches:
        source = resolve_recorded_path(str(row.get("source_file") or ""), connector_root=connector_root, build_root=build_root)
        if source is None:
            continue
        key = str(source)
        if key in seen:
            continue
        seen.add(key)
        records.append((source, f"{row.get('source_scope', 'runtime')} source"))
    for native_input in native_semantics_inputs or []:
        key = str(native_input)
        if key in seen:
            continue
        seen.add(key)
        records.append((native_input, "native libmodsecurity case oracle"))
    return [input_record(path, label) for path, label in sorted(records, key=lambda item: str(item[0]))]


def command_for(commands: list[dict[str, Any]], target: str) -> dict[str, Any]:
    for command in commands:
        raw = command.get("command")
        if command.get("logical_target") == target:
            return command
        if isinstance(raw, list) and raw == ["make", target]:
            return command
    return {}


def load_commands(path: Path | None) -> list[dict[str, Any]]:
    if path is None or not path.is_file():
        return []
    data = read_json(path)
    commands = data.get("commands")
    return commands if isinstance(commands, list) else []


def load_commands_payload(path: Path | None) -> dict[str, Any]:
    if path is None or not path.is_file():
        return {}
    return read_json(path)


def parse_time(value: str | None) -> float | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def new_enough(path: Path, min_mtime: float | None) -> bool:
    if min_mtime is None:
        return True
    try:
        return path.stat().st_mtime >= min_mtime
    except OSError:
        return False


def classify_case(case: dict[str, Any], *, incomplete: bool = False) -> tuple[str, str, bool, bool, bool]:
    if incomplete:
        return (
            "timeout_or_incomplete",
            "Producer job did not produce complete result evidence.",
            False,
            False,
            False,
        )
    status = str(case.get("status") or case.get("case_status") or "").lower()
    reason = str(case.get("reason") or "").lower()
    known = " ".join(str(item) for item in case.get("known_limitations", [])).lower()
    expected = case.get("expected_status")
    actual = case.get("actual_status", case.get("observed_status"))
    if status in {"blocked", "not_executable", "not-executable", "skipped"}:
        return ("timeout_or_incomplete", "Case did not execute to a comparable live result.", False, False, False)
    if "connector-gap" in known:
        return ("connector_capability_gap", "Case is already marked as a connector capability gap.", True, False, False)
    if "runtime-difference" in known:
        return ("runtime_regression", "Case is marked as a runtime difference and still mismatches live evidence.", True, False, False)
    if "future-compatibility" in known or "experimental" in known:
        return ("known_not_next", "Case is marked as future/experimental coverage, not a next critical fix.", False, False, True)
    if "pending-runtime-verification" in known:
        return ("framework_expected_behavior_gap", "Expected behavior is still pending runtime verification.", False, True, False)
    try:
        actual_int = int(actual)
    except (TypeError, ValueError):
        actual_int = None
    if actual_int in {500, 502, 503, 504}:
        return ("runtime_regression", "Connector returned a server error for a live runtime case.", True, False, False)
    if expected is not None and actual is not None and str(expected) != str(actual):
        return ("expected_status_mismatch", "Observed HTTP status differs from expected status.", True, False, False)
    if "timeout" in reason:
        return ("environment_flake", "Failure text indicates a timeout-like runtime condition.", False, False, False)
    return ("unknown", "Mismatch requires manual triage.", False, False, False)


def source_text(case: dict[str, Any]) -> str:
    origin = case.get("origin")
    if isinstance(origin, list) and origin:
        parts = []
        for item in origin:
            if not isinstance(item, dict):
                continue
            repo = str(item.get("repo") or "-")
            path = str(item.get("path") or "-")
            parts.append(f"{repo}:{path}")
        if parts:
            return "; ".join(parts)
    return str(case.get("path") or "-")


def expected_actual(case: dict[str, Any]) -> tuple[str, str]:
    expected = case.get("expected_status")
    actual = case.get("actual_status", case.get("observed_status"))
    if expected is None:
        expected = case.get("expected_intervention", "-")
    if actual is None:
        actual = case.get("observed_transport_result", "-")
    return str(expected), str(actual)


def runtime_evidence_state(case: dict[str, Any], expected: str, actual: str) -> str:
    status = str(case.get("status") or case.get("case_status") or "").lower()
    if status in {"blocked", "not_executable", "not-executable", "skipped"}:
        return "not_reached_not_executable"
    if expected != "-" and actual != "-" and expected != actual:
        return "runtime_reached_actual_mismatch"
    if expected != "-" and actual != "-" and expected == actual:
        return "runtime_reached_actual_match"
    return "unknown"


def configtest_log_from_reason(reason: str) -> Path | None:
    match = re.search(r"see\s+(\S*configtest\.log)", reason)
    return Path(match.group(1)) if match else None


def runtime_failure_mode(case: dict[str, Any], case_name: str) -> str:
    state = runtime_evidence_state(case, *expected_actual(case))
    if state == "runtime_reached_actual_mismatch":
        return "runtime_reached_actual_mismatch"
    if state != "not_reached_not_executable":
        return state
    if case_name == "v2_transformation_url_decode_invalid_sequence_mapped_candidate":
        return "fixture_syntax_error"
    reason = str(case.get("reason") or "")
    log_path = configtest_log_from_reason(reason)
    log_text = ""
    if log_path is not None:
        try:
            log_text = log_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            log_text = ""
    combined = f"{reason}\n{log_text}"
    if "Rules error" in combined or "Rules must have an ID" in combined or "configuration file" in combined:
        if case_name == "v2_transformation_url_decode_invalid_sequence_mapped_candidate":
            return "fixture_syntax_error"
        return "parser_config_error"
    return "not_reached_not_executable"


def full_matrix_refresh_needed_for_case(case: dict[str, Any], evidence: str) -> bool:
    case_path = Path(str(case.get("path") or ""))
    evidence_path = Path(evidence)
    if not case_path.is_file() or not evidence_path.is_file():
        return False
    try:
        return case_path.stat().st_mtime > evidence_path.stat().st_mtime
    except OSError:
        return False


def resolve_evidence_file(value: str, *, connector_root: Path, build_root: Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    build_candidate = build_root / path
    if build_candidate.exists():
        return build_candidate
    return connector_root / path


def result_error_log_path(result_path: Path, result: dict[str, Any]) -> Path:
    for key in ("nginx_error_log_path", "apache_error_log_path", "haproxy_error_log_path", "error_log_path"):
        value = result.get(key)
        if value:
            return Path(str(value))
    return result_path.parent / "error.log"


def result_decision_log_path(result_path: Path, result: dict[str, Any]) -> Path:
    for key in ("decision_log_path", "decision_log"):
        value = result.get(key)
        if value:
            return Path(str(value))
    return result_path.parent / "decision.jsonl"


def rule_ids_from_text_log(path: Path) -> set[str]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return set()
    return set(MODSECURITY_RULE_ID_RE.findall(text))


def rule_ids_from_decision_log(path: Path) -> set[str]:
    ids: set[str] = set()
    for item in read_jsonl(path):
        rule_id = item.get("rule_id")
        if rule_id in (None, "", 0, "0"):
            continue
        ids.add(str(rule_id))
    return ids


def detection_only_rule_paths_from_smoke_file(smoke_rules_file: Path) -> list[Path]:
    try:
        smoke_text = smoke_rules_file.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    candidate_paths: list[Path] = []
    if "ctl:ruleEngine=DetectionOnly" in smoke_text:
        candidate_paths.append(smoke_rules_file)
    for include in INCLUDE_RE.findall(smoke_text):
        include_path = Path(include)
        if not include_path.is_absolute():
            include_path = smoke_rules_file.parent / include_path
        if include_path.name == "mrts.load" or "mrts" in str(include_path):
            try:
                load_text = include_path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            if "ctl:ruleEngine=DetectionOnly" in load_text:
                candidate_paths.append(include_path)
            for nested in INCLUDE_RE.findall(load_text):
                nested_path = Path(nested)
                if not nested_path.is_absolute():
                    nested_path = include_path.parent / nested_path
                try:
                    nested_text = nested_path.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    continue
                if "ctl:ruleEngine=DetectionOnly" in nested_text:
                    candidate_paths.append(nested_path)
    return candidate_paths


def secaction_smoke_rules_file(
    result_path: Path,
    *,
    connector: str,
) -> Path | None:
    result_text = str(result_path)
    replacements = {
        "apache": ("/logs/apache-runtime/", "/apache-runtime/"),
        "haproxy": ("/logs/haproxy-runtime/", "/haproxy-runtime-cases/"),
        "nginx": ("/logs/", "/runtime/"),
    }
    old, new = replacements.get(connector, ("", ""))
    if not old or old not in result_text:
        return None
    candidate = Path(result_text.replace(old, new)).parent / "conf" / "modsecurity-smoke.conf"
    return candidate if candidate.is_file() else None


def secaction_rule_loaded(smoke_rules_file: Path) -> bool:
    try:
        smoke_text = smoke_rules_file.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    compact = smoke_text.replace(" ", "")
    return (
        "SecAction" in smoke_text
        and f"id:{SECACTION_DETECTION_ONLY_RULE_ID}" in compact
        and "phase:2" in compact
        and "deny" in compact
        and "status:403" in compact
    )


def no_mrts_control_evidence(
    row: dict[str, Any],
    *,
    build_root: Path,
) -> dict[str, str] | None:
    connector = str(row.get("connector") or "")
    variant = str(row.get("variant") or "")
    if "/" not in variant:
        return None
    crs, _mrts = variant.split("/", 1)
    patterns = {
        "apache": build_root
        / "full-matrix"
        / crs
        / "no-mrts"
        / "apache"
        / "logs"
        / "apache-runtime"
        / SECACTION_DETECTION_ONLY_CASE
        / "result.json",
        "haproxy": build_root
        / "full-matrix"
        / crs
        / "no-mrts"
        / "haproxy"
        / "logs"
        / "haproxy-runtime"
        / SECACTION_DETECTION_ONLY_CASE
        / "result.json",
    }
    result_path = patterns.get(connector)
    if connector == "nginx":
        summary_path = build_root / "full-matrix" / crs / "no-mrts" / "nginx" / "results" / "force-all" / "nginx-summary.json"
        summary = read_json(summary_path)
        for item in walk_dicts(summary):
            if str(item.get("name") or item.get("case") or "") != SECACTION_DETECTION_ONLY_CASE:
                continue
            result_path = Path(str(item.get("evidence_path") or ""))
            break
    if not result_path or not result_path.is_file():
        return None
    result = read_json(result_path)
    actual = str(result.get("actual_status", result.get("observed_status")) or "")
    status = str(result.get("status") or "")
    if status != "pass" or actual != "403":
        return None
    error_log = result_error_log_path(result_path, result)
    rule_ids = rule_ids_from_text_log(error_log)
    decision_log = result_decision_log_path(result_path, result)
    rule_ids |= rule_ids_from_decision_log(decision_log)
    if SECACTION_DETECTION_ONLY_RULE_ID not in rule_ids and connector not in {"apache", "haproxy"}:
        return None
    return {
        "variant": f"{crs}/no-mrts",
        "result": rel(result_path, build_root),
        "status": "pass",
        "actual": actual,
        "rule_ids": ",".join(sorted(rule_ids)) or SECACTION_DETECTION_ONLY_RULE_ID,
    }


def no_mrts_case_control_evidence(
    row: dict[str, Any],
    *,
    build_root: Path,
    case_name: str,
) -> dict[str, str] | None:
    connector = str(row.get("connector") or "")
    variant = str(row.get("variant") or "")
    if "/" not in variant:
        return None
    crs, _mrts = variant.split("/", 1)
    result_path: Path | None = None
    if connector == "apache":
        result_path = (
            build_root
            / "full-matrix"
            / crs
            / "no-mrts"
            / "apache"
            / "logs"
            / "apache-runtime"
            / case_name
            / "result.json"
        )
    elif connector == "haproxy":
        result_path = (
            build_root
            / "full-matrix"
            / crs
            / "no-mrts"
            / "haproxy"
            / "logs"
            / "haproxy-runtime"
            / case_name
            / "result.json"
        )
    elif connector == "nginx":
        summary_path = build_root / "full-matrix" / crs / "no-mrts" / "nginx" / "results" / "force-all" / "nginx-summary.json"
        summary = read_json(summary_path)
        for item in walk_dicts(summary):
            if str(item.get("name") or item.get("case") or "") != case_name:
                continue
            result_path = Path(str(item.get("evidence_path") or ""))
            break
    if not result_path or not result_path.is_file():
        return None
    result = read_json(result_path)
    actual = str(result.get("actual_status", result.get("observed_status")) or "")
    status = str(result.get("status") or "")
    if status != "pass" or actual != "403":
        return None
    return {
        "variant": f"{crs}/no-mrts",
        "result": rel(result_path, build_root),
        "status": status,
        "actual": actual,
    }


def nginx_phase4_response_body_enforcement_gap(
    row: dict[str, Any],
    *,
    evidence: str,
    connector_root: Path,
    build_root: Path,
) -> dict[str, str] | None:
    case_name = str(row.get("case") or "")
    expected_rule_id = NGINX_PHASE4_RESPONSE_BODY_ENFORCEMENT_CASES.get(case_name)
    if expected_rule_id is None:
        return None
    if row.get("full_matrix_refresh_needed") is True:
        return None
    if row.get("connector") != "nginx" or not str(row.get("variant") or "").endswith("/no-mrts"):
        return None
    if row.get("category") not in {"response-body", "audit-log"} or row.get("status") != "fail":
        return None
    if row.get("expected") != "403" or row.get("actual") != "200":
        return None
    result_path = resolve_evidence_file(evidence, connector_root=connector_root, build_root=build_root)
    result = read_json(result_path)
    if result.get("live_executed") is not True or str(result.get("phase") or "") != "4":
        return None
    error_log_path = result_error_log_path(result_path, result)
    audit_log_path = Path(str(result.get("audit_log_path") or result_path.parent / "audit.log"))
    try:
        error_text = error_log_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        error_text = ""
    try:
        audit_text = audit_log_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        audit_text = ""
    combined = f"{error_text}\n{audit_text}"
    if expected_rule_id not in rule_ids_from_text_log(error_log_path) | rule_ids_from_text_log(audit_log_path):
        return None
    if "RESPONSE_BODY" not in combined or "Access denied with code 403 (phase 4)" not in combined:
        return None
    intervention = result.get("intervention")
    if not isinstance(intervention, dict) or intervention.get("disruptive") is not True:
        return None
    return {
        "result": rel(result_path, build_root),
        "error_log": rel(error_log_path, build_root),
        "audit_log": rel(audit_log_path, build_root),
        "rule_id": expected_rule_id,
        "phase": "4",
        "matched_variable": "RESPONSE_BODY",
        "expected_status": "403",
        "actual_status": "200",
        "intervention_status": str(intervention.get("status") or ""),
        "response_body_match_seen": "true",
        "http_status_enforced": "false",
        "native_response_body_not_applicable": "true",
        "targeted_only": "false",
        "full_matrix_refresh_needed": str(row.get("full_matrix_refresh_needed")).lower(),
        "note": NGINX_PHASE4_RESPONSE_BODY_ENFORCEMENT_NOTE,
    }


def nginx_no_mrts_phase4_log_control(
    row: dict[str, Any],
    *,
    build_root: Path,
) -> dict[str, str] | None:
    variant = str(row.get("variant") or "")
    if "/" not in variant:
        return None
    crs, _mrts = variant.split("/", 1)
    summary_path = build_root / "full-matrix" / crs / "no-mrts" / "nginx" / "results" / "force-all" / "nginx-summary.json"
    summary = read_json(summary_path)
    cases = summary.get("nginx", {}).get("cases")
    if isinstance(cases, dict):
        case_items = list(cases.values())
    elif isinstance(cases, list):
        case_items = cases
    else:
        return None
    case_name = str(row.get("case") or "")
    for item in case_items:
        if not isinstance(item, dict):
            continue
        if str(item.get("name") or item.get("case") or "") != case_name:
            continue
        if str(item.get("status") or "").lower() != "pass":
            return None
        evidence_path = Path(str(item.get("evidence_path") or ""))
        if not evidence_path.is_file():
            return None
        result = read_json(evidence_path)
        phase4_log_path = Path(str(result.get("connector_phase4_log_path") or evidence_path.parent / "phase4.log"))
        try:
            phase4_log = phase4_log_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return None
        if "phase4_intervention" not in phase4_log:
            return None
        return {
            "variant": f"{crs}/no-mrts",
            "result": rel(evidence_path, build_root),
            "phase4_log": rel(phase4_log_path, build_root),
            "status": "pass",
        }
    return None


def nginx_phase4_rule_match_no_disruptive_intervention(
    row: dict[str, Any],
    *,
    evidence: str,
    connector_root: Path,
    build_root: Path,
) -> dict[str, str] | None:
    case_name = str(row.get("case") or "")
    expected_rule_id = NGINX_PHASE4_LOG_ONLY_CASES.get(case_name)
    if expected_rule_id is None:
        return None
    if row.get("connector") != "nginx" or not str(row.get("variant") or "").endswith("/with-mrts"):
        return None
    if row.get("category") != "response-body" or row.get("status") != "fail":
        return None
    if row.get("expected") != "200" or row.get("actual") != "200":
        return None
    result_path = resolve_evidence_file(evidence, connector_root=connector_root, build_root=build_root)
    result = read_json(result_path)
    reason = str(result.get("reason") or row.get("reason") or "").lower()
    if "phase4 log file missing or empty" not in reason:
        return None
    if result.get("live_executed") is not True or str(result.get("phase") or "") != "4":
        return None
    error_log_path = result_error_log_path(result_path, result)
    try:
        error_text = error_log_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if "RESPONSE_BODY" not in error_text or expected_rule_id not in rule_ids_from_text_log(error_log_path):
        return None
    smoke_match = MODSECURITY_SMOKE_FILE_RE.search(error_text)
    if not smoke_match:
        return None
    smoke_rules_file = Path(smoke_match.group(1))
    detection_only_paths = detection_only_rule_paths_from_smoke_file(smoke_rules_file)
    if not detection_only_paths:
        return None
    control = nginx_no_mrts_phase4_log_control(row, build_root=build_root)
    if control is None:
        return None
    phase4_log_path = Path(str(result.get("connector_phase4_log_path") or result_path.parent / "phase4.log"))
    response_body_path = Path(str(result.get("response_body_path") or result_path.parent / "response-body.txt"))
    return {
        "result": rel(result_path, build_root),
        "error_log": rel(error_log_path, build_root),
        "phase4_log": rel(phase4_log_path, build_root),
        "response_body": rel(response_body_path, build_root),
        "rules_file": rel(smoke_rules_file, build_root),
        "detection_only_rule": rel(detection_only_paths[0], build_root),
        "no_mrts_control_result": control["result"],
        "no_mrts_control_phase4_log": control["phase4_log"],
        "rule_id": expected_rule_id,
        "phase": "4",
        "matched_variable": "RESPONSE_BODY",
        "expected_status": "200",
        "actual_status": "200",
        "phase4_rule_match_seen": "true",
        "connector_phase4_log_empty": "true",
        "disruptive_intervention_expected": "false",
        "native_response_body_not_applicable": "true",
        "targeted_only": "false",
        "full_matrix_refresh_needed": str(row.get("full_matrix_refresh_needed")).lower(),
        "note": PHASE4_RULE_MATCH_NO_DISRUPTIVE_INTERVENTION_NOTE,
    }


def haproxy_report_only_decisions(decision_log_path: Path) -> tuple[bool, dict[str, str]]:
    entries = read_jsonl(decision_log_path)
    if not entries:
        return False, {}
    phases: list[str] = []
    for entry in entries:
        if entry.get("live_executed") is not True or entry.get("modsecurity_processed") is not True:
            return False, {}
        if entry.get("decision") != "pass" or entry.get("disruptive") is not False:
            return False, {}
        if str(entry.get("intervention_status")) != "200":
            return False, {}
        phase = entry.get("phase")
        if phase is not None:
            phases.append(str(phase))
    return True, {
        "decision_entries": str(len(entries)),
        "decision": "pass",
        "disruptive": "false",
        "intervention_status": "200",
        "phases": ",".join(phases),
    }


def haproxy_with_mrts_detection_only_overlay(
    result_path: Path,
    result: dict[str, Any],
    *,
    build_root: Path,
) -> dict[str, str] | None:
    decision_log_path = result_decision_log_path(result_path, result)
    decisions_ok, decision_evidence = haproxy_report_only_decisions(decision_log_path)
    if not decisions_ok:
        return None
    spoa_runtime_log_path = result_path.parent / "spoa-runtime.stderr.log"
    try:
        spoa_runtime_text = spoa_runtime_log_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if "ModSecurity:" not in spoa_runtime_text:
        return None
    smoke_match = MODSECURITY_SMOKE_FILE_RE.search(spoa_runtime_text)
    if not smoke_match:
        return None
    smoke_rules_file = Path(smoke_match.group(1))
    detection_only_paths = detection_only_rule_paths_from_smoke_file(smoke_rules_file)
    if not detection_only_paths:
        return None
    spoa_log_path = Path(str(result.get("spoa_log_path") or result_path.parent / "spoa-agent.log"))
    try:
        spoa_log_text = spoa_log_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if f"rules_file={smoke_rules_file}" not in spoa_log_text:
        return None
    return {
        "decision_log": rel(decision_log_path, build_root),
        "spoa_runtime_log": rel(spoa_runtime_log_path, build_root),
        "spoa_log": rel(spoa_log_path, build_root),
        "rules_file": rel(smoke_rules_file, build_root),
        "detection_only_rule": rel(detection_only_paths[0], build_root),
        "decision": decision_evidence["decision"],
        "disruptive": decision_evidence["disruptive"],
        "intervention_status": decision_evidence["intervention_status"],
        "decision_entries": decision_evidence["decision_entries"],
        "phases": decision_evidence["phases"],
        "note": HAPROXY_MRTS_DETECTION_ONLY_NOTE,
    }


def with_mrts_detection_only_overlay(
    row: dict[str, Any],
    *,
    evidence: str,
    connector_root: Path,
    build_root: Path,
) -> dict[str, str] | None:
    if row["connector"] not in {"apache", "haproxy", "nginx"} or not row["variant"].endswith("/with-mrts"):
        return None
    if row["status"] != "fail" or row["actual"] != "200" or row["expected"] not in DISRUPTIVE_EXPECTED_STATUSES:
        return None
    result_path = resolve_evidence_file(evidence, connector_root=connector_root, build_root=build_root)
    result = read_json(result_path)
    if row["connector"] == "haproxy":
        return haproxy_with_mrts_detection_only_overlay(result_path, result, build_root=build_root)
    error_log_path = result_error_log_path(result_path, result)
    try:
        error_text = error_log_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if "ModSecurity:" not in error_text:
        return None
    smoke_match = MODSECURITY_SMOKE_FILE_RE.search(error_text)
    if not smoke_match:
        return None
    smoke_rules_file = Path(smoke_match.group(1))
    detection_only_paths = detection_only_rule_paths_from_smoke_file(smoke_rules_file)
    if not detection_only_paths:
        return None
    return {
        "error_log": rel(error_log_path, build_root),
        "rules_file": rel(smoke_rules_file, build_root),
        "detection_only_rule": rel(detection_only_paths[0], build_root),
        "note": MRTS_DETECTION_ONLY_NOTE,
    }


def crs_sqli_with_mrts_detection_only_overlay(
    row: dict[str, Any],
    *,
    evidence: str,
    connector_root: Path,
    build_root: Path,
) -> dict[str, str] | None:
    if row.get("case") != CRS_SQLI_WITH_MRTS_DETECTION_ONLY_CASE:
        return None
    if row.get("connector") not in {"apache", "haproxy", "nginx"} or row.get("variant") != "with-crs/with-mrts":
        return None
    if row.get("status") != "fail" or row.get("expected") != "403" or row.get("actual") != "200":
        return None
    if row.get("full_matrix_refresh_needed") is True:
        return None
    result_path = resolve_evidence_file(evidence, connector_root=connector_root, build_root=build_root)
    result = read_json(result_path)
    if result.get("live_executed") is not True:
        return None
    intervention = result.get("intervention")
    if not isinstance(intervention, dict) or intervention.get("disruptive") is not True:
        return None
    if str(intervention.get("status") or "") != "403":
        return None
    smoke_rules_file = secaction_smoke_rules_file(result_path, connector=str(row["connector"]))
    if smoke_rules_file is None:
        return None
    detection_only_paths = detection_only_rule_paths_from_smoke_file(smoke_rules_file)
    if not detection_only_paths:
        return None
    log_paths = [result_error_log_path(result_path, result)]
    if row["connector"] == "haproxy":
        log_paths.extend([result_path.parent / "spoa-runtime.stderr.log", result_path.parent / "spoa-agent.log"])
    combined_rule_ids: set[str] = set()
    matched_data_seen = False
    anomaly_seen = False
    for log_path in log_paths:
        try:
            log_text = log_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        combined_rule_ids |= rule_ids_from_text_log(log_path)
        matched_data_seen = matched_data_seen or "UNION SELECT" in log_text or "SQL Injection Attack Detected" in log_text
        anomaly_seen = anomaly_seen or "Inbound Anomaly Score Exceeded" in log_text
    decision_log_path = result_decision_log_path(result_path, result)
    combined_rule_ids |= rule_ids_from_decision_log(decision_log_path)
    if not (combined_rule_ids & CRS_SQLI_WITH_MRTS_RULE_IDS):
        return None
    if "949110" not in combined_rule_ids or not matched_data_seen or not anomaly_seen:
        return None
    control = no_mrts_case_control_evidence(
        row,
        build_root=build_root,
        case_name=CRS_SQLI_WITH_MRTS_DETECTION_ONLY_CASE,
    )
    if control is None:
        return None
    evidence_out: dict[str, str] = {
        "result": rel(result_path, build_root),
        "rules_file": rel(smoke_rules_file, build_root),
        "detection_only_rule": rel(detection_only_paths[0], build_root),
        "no_mrts_control_result": control["result"],
        "no_mrts_control_variant": control["variant"],
        "no_mrts_control_actual": control["actual"],
        "rule_ids": ",".join(sorted(combined_rule_ids & CRS_SQLI_WITH_MRTS_RULE_IDS)),
        "anomaly_rule_id": "949110",
        "matched_data": "UNION SELECT",
        "expected_status": "403",
        "actual_status": "200",
        "intervention_status": str(intervention.get("status") or ""),
        "targeted_only": "false",
        "full_matrix_refresh_needed": "false",
        "note": CRS_SQLI_WITH_MRTS_DETECTION_ONLY_NOTE,
    }
    if row["connector"] == "haproxy" and decision_log_path.is_file():
        evidence_out["decision_log"] = rel(decision_log_path, build_root)
    else:
        evidence_out["error_log"] = rel(log_paths[0], build_root)
    return evidence_out


def secaction_with_mrts_detection_only_overlay(
    row: dict[str, Any],
    *,
    evidence: str,
    connector_root: Path,
    build_root: Path,
) -> dict[str, str] | None:
    if row["case"] != SECACTION_DETECTION_ONLY_CASE:
        return None
    if row["connector"] not in {"apache", "haproxy", "nginx"} or not row["variant"].endswith("/with-mrts"):
        return None
    if row["status"] != "fail" or row["actual"] != "200" or row["expected"] != "403":
        return None
    result_path = resolve_evidence_file(evidence, connector_root=connector_root, build_root=build_root)
    result = read_json(result_path)
    if result.get("live_executed") is not True:
        return None
    smoke_rules_file = secaction_smoke_rules_file(result_path, connector=row["connector"])
    if smoke_rules_file is None or not secaction_rule_loaded(smoke_rules_file):
        return None
    detection_only_paths = detection_only_rule_paths_from_smoke_file(smoke_rules_file)
    if not detection_only_paths:
        return None
    control = no_mrts_control_evidence(row, build_root=build_root)
    if control is None:
        return None
    evidence_out: dict[str, str] = {
        "result": rel(result_path, build_root),
        "rules_file": rel(smoke_rules_file, build_root),
        "detection_only_rule": rel(detection_only_paths[0], build_root),
        "no_mrts_control_result": control["result"],
        "no_mrts_control_variant": control["variant"],
        "no_mrts_control_actual": control["actual"],
        "secaction_rule_id": SECACTION_DETECTION_ONLY_RULE_ID,
        "secaction_runtime_reached": "true",
        "secaction_intervention_seen": "false",
        "secaction_no_intervention": "true",
        "native_secaction_same_as_connectors": "false_for_with_mrts_overlay; true_for_no_mrts_control",
        "targeted_only": "false",
        "full_matrix_refresh_needed": "false",
        "note": SECACTION_DETECTION_ONLY_NOTE,
    }
    if row["connector"] == "haproxy":
        decision_log_path = result_decision_log_path(result_path, result)
        decisions_ok, decision_evidence = haproxy_report_only_decisions(decision_log_path)
        if not decisions_ok:
            return None
        evidence_out.update(
            {
                "decision_log": rel(decision_log_path, build_root),
                "decision": decision_evidence["decision"],
                "disruptive": decision_evidence["disruptive"],
                "intervention_status": decision_evidence["intervention_status"],
                "decision_entries": decision_evidence["decision_entries"],
                "phases": decision_evidence["phases"],
            }
        )
    else:
        error_log_path = result_error_log_path(result_path, result)
        evidence_out["error_log"] = rel(error_log_path, build_root)
    return evidence_out


def multipart_fixture_gap(
    row: dict[str, Any],
    *,
    evidence: str,
    connector_root: Path,
    build_root: Path,
) -> dict[str, str] | None:
    if row["category"] != "multipart" or row["status"] not in {"not_executable", "not-executable"}:
        return None
    result_path = resolve_evidence_file(evidence, connector_root=connector_root, build_root=build_root)
    result = read_json(result_path)
    candidates = [
        result_path.parent / "configtest.log",
        result_path.parent / "spoa-runtime.stderr.log",
        result_path.parent / "haproxy-configtest.log",
        result_path.parent / "error.log",
    ]
    for value in result.values():
        if isinstance(value, str) and value.endswith((".log", ".txt")):
            candidates.append(Path(value))

    for log_path in candidates:
        try:
            log_text = log_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if "Rules error" not in log_text or "syntax error" not in log_text:
            continue
        if "unexpected Id" not in log_text and "unexpected id" not in log_text:
            continue
        smoke_match = RULES_ERROR_SMOKE_FILE_RE.search(log_text)
        if not smoke_match:
            continue
        smoke_rules_file = Path(smoke_match.group(1))
        try:
            smoke_text = smoke_rules_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if not EMPTY_MULTIPART_OPERATOR_RE.search(smoke_text):
            continue
        return {
            "result": rel(result_path, build_root),
            "parse_error_log": rel(log_path, build_root),
            "rules_file": rel(smoke_rules_file, build_root),
            "note": "Multipart fixture generated an invalid empty-argument ModSecurity rule; no comparable runtime decision was produced.",
        }
    return None


def full_matrix_summary_case(build_root: Path, connector: str, variant: str, case_name: str) -> dict[str, Any]:
    try:
        crs, mrts = variant.split("/", 1)
    except ValueError:
        return {}
    base = build_root / "full-matrix" / crs / mrts / connector / "results"
    summary_paths = [
        base / "force-all" / f"{connector}-summary.json",
        base / f"{connector}-summary.json",
    ]
    for summary_path in summary_paths:
        data = read_json(summary_path)
        summary = data.get(connector)
        if not isinstance(summary, dict):
            continue
        cases = summary.get("cases")
        if isinstance(cases, dict) and isinstance(cases.get(case_name), dict):
            return cases[case_name]
    return {}


def full_matrix_control_evidence(build_root: Path) -> dict[str, dict[str, str]]:
    evidence: dict[str, dict[str, str]] = {}
    for connector in sorted(SEMICOLON_COLLECTION_CONNECTORS):
        for variant in ("no-crs/no-mrts", "with-crs/no-mrts"):
            case = full_matrix_summary_case(build_root, connector, variant, ARGS_NAMES_CONTROL_CASE)
            key = f"{connector}:{variant}:{ARGS_NAMES_CONTROL_CASE}"
            if (
                str(case.get("status") or "").lower() == "pass"
                and str(case.get("expected_status") or "") == "403"
                and str(case.get("actual_status", case.get("observed_status")) or "") == "403"
                and case.get("live_executed") is True
            ):
                evidence[key] = {
                    "status": "pass",
                    "expected": "403",
                    "actual": "403",
                    "evidence_file": str(case.get("evidence_path") or "-"),
                }
            else:
                evidence[key] = {
                    "status": str(case.get("status") or "missing"),
                    "expected": str(case.get("expected_status") or "-"),
                    "actual": str(case.get("actual_status", case.get("observed_status")) or "-"),
                    "evidence_file": str(case.get("evidence_path") or "-"),
                }
    return evidence


def full_matrix_case_control_evidence(build_root: Path, control_case_name: str) -> dict[str, dict[str, str]]:
    evidence: dict[str, dict[str, str]] = {}
    for connector in sorted(SEMICOLON_COLLECTION_CONNECTORS):
        for variant in ("no-crs/no-mrts", "with-crs/no-mrts"):
            case = full_matrix_summary_case(build_root, connector, variant, control_case_name)
            key = f"{connector}:{variant}:{control_case_name}"
            if (
                str(case.get("status") or "").lower() == "pass"
                and str(case.get("expected_status") or "") == "403"
                and str(case.get("actual_status", case.get("observed_status")) or "") == "403"
                and case.get("live_executed") is True
            ):
                evidence[key] = {
                    "status": "pass",
                    "expected": "403",
                    "actual": "403",
                    "evidence_file": str(case.get("evidence_path") or "-"),
                }
            else:
                evidence[key] = {
                    "status": str(case.get("status") or "missing"),
                    "expected": str(case.get("expected_status") or "-"),
                    "actual": str(case.get("actual_status", case.get("observed_status")) or "-"),
                    "evidence_file": str(case.get("evidence_path") or "-"),
                }
    return evidence


def semicolon_collection_result_evidence(
    row: dict[str, Any],
    *,
    connector_root: Path,
    build_root: Path,
) -> dict[str, str] | None:
    if row["connector"] not in SEMICOLON_COLLECTION_CONNECTORS:
        return None
    if row["variant"] not in SEMICOLON_COLLECTION_VARIANTS:
        return None
    if row["case"] not in SEMICOLON_COLLECTION_CASES:
        return None
    if row["category"] != "collections":
        return None
    if row["status"] != "fail" or row["expected"] != "403" or row["actual"] != "200":
        return None
    result_path = resolve_evidence_file(str(row.get("evidence_file") or ""), connector_root=connector_root, build_root=build_root)
    result = read_json(result_path)
    if result.get("live_executed") is not True:
        return None
    if str(result.get("expected_status") or "") != "403":
        return None
    if str(result.get("actual_status", result.get("observed_status")) or "") != "200":
        return None
    if str(result.get("observed_transport_result") or "") not in {"", "http_status"}:
        return None
    if row["connector"] == "haproxy" and result.get("modsecurity_processed") is not True:
        return None
    return {
        "result": rel(result_path, build_root),
        "expected": "403",
        "actual": "200",
        "live_executed": "true",
        "observed_transport_result": str(result.get("observed_transport_result") or "http_status"),
        "modsecurity_processed": str(result.get("modsecurity_processed", "n/a")).lower(),
    }


def apply_semicolon_collection_semantics_classification(
    mismatches: list[dict[str, Any]],
    *,
    connector_root: Path,
    build_root: Path,
) -> list[dict[str, Any]]:
    expected_matrix = {
        (case, connector, variant)
        for case in SEMICOLON_COLLECTION_CASES
        for connector in SEMICOLON_COLLECTION_CONNECTORS
        for variant in SEMICOLON_COLLECTION_VARIANTS
    }
    candidates = {
        (row["case"], row["connector"], row["variant"]): row
        for row in mismatches
        if row.get("case") in SEMICOLON_COLLECTION_CASES
        and row.get("connector") in SEMICOLON_COLLECTION_CONNECTORS
        and row.get("variant") in SEMICOLON_COLLECTION_VARIANTS
    }
    if set(candidates) != expected_matrix:
        return mismatches

    row_evidence: dict[tuple[str, str, str], dict[str, str]] = {}
    for key, row in candidates.items():
        evidence = semicolon_collection_result_evidence(row, connector_root=connector_root, build_root=build_root)
        if evidence is None:
            return mismatches
        row_evidence[key] = evidence

    control_evidence = full_matrix_control_evidence(build_root)
    if not control_evidence or any(item.get("status") != "pass" for item in control_evidence.values()):
        return mismatches

    for key, row in candidates.items():
        row["classification"] = COLLECTION_SEMANTICS_CLASSIFICATION
        row["technical_cause"] = COLLECTION_SEMANTICS_NOTE
        row["code_fix_needed"] = False
        row["test_expectation_wrong"] = False
        row["document_only"] = True
        row["classification_note"] = COLLECTION_SEMANTICS_NOTE
        row["classification_evidence"] = {
            "note": COLLECTION_SEMANTICS_NOTE,
            "row_evidence": row_evidence[key],
            "control_case": ARGS_NAMES_CONTROL_CASE,
            "control_evidence": control_evidence,
        }
    return mismatches


def collection_name_case_result_evidence(
    row: dict[str, Any],
    *,
    connector_root: Path,
    build_root: Path,
) -> dict[str, str] | None:
    if row["connector"] not in SEMICOLON_COLLECTION_CONNECTORS:
        return None
    if row["variant"] not in SEMICOLON_COLLECTION_VARIANTS:
        return None
    if row["case"] not in COLLECTION_NAME_CASE_CASES:
        return None
    if row["category"] != "collections":
        return None
    if row["status"] != "fail" or row["expected"] != "403" or row["actual"] != "200":
        return None
    result_path = resolve_evidence_file(str(row.get("evidence_file") or ""), connector_root=connector_root, build_root=build_root)
    result = read_json(result_path)
    if result.get("live_executed") is not True:
        return None
    if str(result.get("expected_status") or "") != "403":
        return None
    if str(result.get("actual_status", result.get("observed_status")) or "") != "200":
        return None
    if str(result.get("observed_transport_result") or "") not in {"", "http_status"}:
        return None
    if row["connector"] == "haproxy" and result.get("modsecurity_processed") is not True:
        return None
    return {
        "result": rel(result_path, build_root),
        "expected": "403",
        "actual": "200",
        "live_executed": "true",
        "observed_transport_result": str(result.get("observed_transport_result") or "http_status"),
        "modsecurity_processed": str(result.get("modsecurity_processed", "n/a")).lower(),
    }


def apply_collection_name_case_semantics_classification(
    mismatches: list[dict[str, Any]],
    *,
    connector_root: Path,
    build_root: Path,
) -> list[dict[str, Any]]:
    expected_matrix = {
        (case, connector, variant)
        for case in COLLECTION_NAME_CASE_CASES
        for connector in SEMICOLON_COLLECTION_CONNECTORS
        for variant in SEMICOLON_COLLECTION_VARIANTS
    }
    candidates = {
        (row["case"], row["connector"], row["variant"]): row
        for row in mismatches
        if row.get("case") in COLLECTION_NAME_CASE_CASES
        and row.get("connector") in SEMICOLON_COLLECTION_CONNECTORS
        and row.get("variant") in SEMICOLON_COLLECTION_VARIANTS
    }
    if set(candidates) != expected_matrix:
        return mismatches

    row_evidence: dict[tuple[str, str, str], dict[str, str]] = {}
    for key, row in candidates.items():
        evidence = collection_name_case_result_evidence(row, connector_root=connector_root, build_root=build_root)
        if evidence is None:
            return mismatches
        row_evidence[key] = evidence

    control_evidence_by_case: dict[str, dict[str, dict[str, str]]] = {}
    for control_case in sorted(set(COLLECTION_NAME_CASE_CONTROL_CASES.values())):
        control_evidence = full_matrix_case_control_evidence(build_root, control_case)
        if not control_evidence or any(item.get("status") != "pass" for item in control_evidence.values()):
            return mismatches
        control_evidence_by_case[control_case] = control_evidence

    for key, row in candidates.items():
        control_case = COLLECTION_NAME_CASE_CONTROL_CASES[str(row["case"])]
        row["classification"] = COLLECTION_NAME_CASE_SEMANTICS_CLASSIFICATION
        row["technical_cause"] = COLLECTION_NAME_CASE_SEMANTICS_NOTE
        row["code_fix_needed"] = False
        row["test_expectation_wrong"] = False
        row["document_only"] = True
        row["classification_note"] = COLLECTION_NAME_CASE_SEMANTICS_NOTE
        row["classification_evidence"] = {
            "note": COLLECTION_NAME_CASE_SEMANTICS_NOTE,
            "row_evidence": row_evidence[key],
            "control_case": control_case,
            "control_evidence": control_evidence_by_case[control_case],
        }
    return mismatches


def nolog_expected_no_audit_evidence(
    row: dict[str, Any],
    *,
    connector_root: Path,
    build_root: Path,
) -> dict[str, Any] | None:
    if row["case"] != NOLOG_EXPECTED_NO_AUDIT_CASE:
        return None
    if row["category"] != "actions":
        return None
    if row["status"] != "fail" or row["expected"] != "200" or row["actual"] != "200":
        return None
    result_path = resolve_evidence_file(str(row.get("evidence_file") or ""), connector_root=connector_root, build_root=build_root)
    result = read_json(result_path)
    if result.get("live_executed") is not True:
        return None
    if str(result.get("expected_status") or "") != "200":
        return None
    if str(result.get("actual_status", result.get("observed_status")) or "") != "200":
        return None

    audit_log_path = Path(str(result.get("audit_log_path") or result_path.parent / "audit.log"))
    error_log_path = result_error_log_path(result_path, result)
    decision_log_path = result_decision_log_path(result_path, result)
    audit_rule_ids = rule_ids_from_text_log(audit_log_path)
    error_rule_ids = rule_ids_from_text_log(error_log_path)
    decision_rule_ids = rule_ids_from_decision_log(decision_log_path)
    all_rule_ids = audit_rule_ids | error_rule_ids | decision_rule_ids
    if NOLOG_EXPECTED_NO_AUDIT_RULE_ID in all_rule_ids:
        return None
    return {
        "result": rel(result_path, build_root),
        "expected": "200",
        "actual": "200",
        "target_rule": NOLOG_EXPECTED_NO_AUDIT_RULE_ID,
        "audit_rule_ids": sorted(audit_rule_ids),
        "error_rule_ids": sorted(error_rule_ids),
        "decision_rule_ids": sorted(decision_rule_ids),
        "audit_log": rel(audit_log_path, build_root),
        "error_log": rel(error_log_path, build_root),
        "decision_log": rel(decision_log_path, build_root) if decision_log_path.exists() else "-",
    }


def apply_nolog_expected_no_audit_classification(
    mismatches: list[dict[str, Any]],
    *,
    connector_root: Path,
    build_root: Path,
) -> list[dict[str, Any]]:
    expected_matrix = {
        (NOLOG_EXPECTED_NO_AUDIT_CASE, connector, variant)
        for connector in SEMICOLON_COLLECTION_CONNECTORS
        for variant in ("with-crs/no-mrts", "with-crs/with-mrts")
    }
    candidates = {
        (row["case"], row["connector"], row["variant"]): row
        for row in mismatches
        if row.get("case") == NOLOG_EXPECTED_NO_AUDIT_CASE
        and row.get("connector") in SEMICOLON_COLLECTION_CONNECTORS
        and row.get("variant") in {"with-crs/no-mrts", "with-crs/with-mrts"}
    }
    if set(candidates) != expected_matrix:
        return mismatches

    row_evidence: dict[tuple[str, str, str], dict[str, Any]] = {}
    for key, row in candidates.items():
        evidence = nolog_expected_no_audit_evidence(row, connector_root=connector_root, build_root=build_root)
        if evidence is None:
            return mismatches
        row_evidence[key] = evidence

    for key, row in candidates.items():
        row["classification"] = NOLOG_EXPECTED_NO_AUDIT_CLASSIFICATION
        row["technical_cause"] = NOLOG_EXPECTED_NO_AUDIT_NOTE
        row["code_fix_needed"] = False
        row["test_expectation_wrong"] = False
        row["document_only"] = True
        row["classification_note"] = NOLOG_EXPECTED_NO_AUDIT_NOTE
        row["classification_evidence"] = {
            "note": NOLOG_EXPECTED_NO_AUDIT_NOTE,
            "row_evidence": row_evidence[key],
        }
    return mismatches


def status_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def latest_native_case_run(verified_run_root: Path, case_name: str) -> tuple[dict[str, Any], Path] | None:
    native_root = verified_run_root / "native-case-runs"
    paths = sorted(native_root.glob(f"*-{case_name}/native-case-run.json"))
    for path in reversed(paths):
        data = read_json(path)
        if data.get("case") == case_name:
            return data, path
    return None


def native_semantics_result_evidence(
    row: dict[str, Any],
    *,
    connector_root: Path,
    build_root: Path,
    expected_status: str,
    native_actual: str,
) -> dict[str, str] | None:
    if row.get("connector") not in SEMICOLON_COLLECTION_CONNECTORS:
        return None
    if row.get("variant") not in SEMICOLON_COLLECTION_VARIANTS:
        return None
    if row.get("case") not in TRANSFORMATION_NATIVE_SEMANTICS_CASES:
        return None
    if row.get("category") != "transformations":
        return None
    if row.get("status") != "fail" or row.get("expected") != expected_status or row.get("actual") != native_actual:
        return None
    result_path = resolve_evidence_file(str(row.get("evidence_file") or ""), connector_root=connector_root, build_root=build_root)
    result = read_json(result_path)
    if result.get("live_executed") is not True:
        return None
    if status_string(result.get("expected_status")) != expected_status:
        return None
    if status_string(result.get("actual_status", result.get("observed_status"))) != native_actual:
        return None
    if str(result.get("observed_transport_result") or "") not in {"", "http_status"}:
        return None
    if row["connector"] == "haproxy" and result.get("modsecurity_processed") is not True:
        return None
    return {
        "result": rel(result_path, build_root),
        "expected": expected_status,
        "actual": native_actual,
        "live_executed": "true",
        "observed_transport_result": str(result.get("observed_transport_result") or "http_status"),
        "modsecurity_processed": str(result.get("modsecurity_processed", "n/a")).lower(),
    }


def valid_native_transformation_semantics_evidence(
    native_case_run: dict[str, Any],
    candidates: dict[tuple[str, str], dict[str, Any]],
    *,
    connector_root: Path,
    build_root: Path,
) -> dict[str, Any] | None:
    if str(native_case_run.get("status") or "") != "fail":
        return None
    if str(native_case_run.get("decision") or "") != "DOCUMENT":
        return None
    if str(native_case_run.get("classification_hint") or "") != "likely_framework_expected_behavior_gap_or_libmodsecurity_semantics":
        return None
    if native_case_run.get("native_match") is not False:
        return None
    input_hash = str(native_case_run.get("input_hash") or "")
    if not input_hash:
        return None

    expected_status = status_string(native_case_run.get("expected_status"))
    native_actual = status_string(native_case_run.get("native_actual"))
    if expected_status != "403" or native_actual != "200":
        return None
    if expected_status == native_actual:
        return None

    expected_matrix = {
        (connector, variant)
        for connector in SEMICOLON_COLLECTION_CONNECTORS
        for variant in SEMICOLON_COLLECTION_VARIANTS
    }
    comparisons = native_case_run.get("connector_comparison")
    if not isinstance(comparisons, list):
        return None
    comparison_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    for item in comparisons:
        if not isinstance(item, dict):
            return None
        key = (str(item.get("connector") or ""), str(item.get("variant") or ""))
        comparison_by_key[key] = item
    if set(comparison_by_key) != expected_matrix:
        return None
    if set(candidates) != expected_matrix:
        return None

    row_evidence: dict[str, dict[str, str]] = {}
    comparison_evidence: dict[str, dict[str, Any]] = {}
    for key, item in comparison_by_key.items():
        if item.get("same") is not True:
            return None
        if status_string(item.get("native_actual")) != native_actual:
            return None
        if status_string(item.get("connector_actual")) != native_actual:
            return None
        if str(item.get("meaning") or "") != "same_as_native":
            return None
        row = candidates[key]
        evidence = native_semantics_result_evidence(
            row,
            connector_root=connector_root,
            build_root=build_root,
            expected_status=expected_status,
            native_actual=native_actual,
        )
        if evidence is None:
            return None
        evidence_key = f"{key[0]}:{key[1]}"
        row_evidence[evidence_key] = evidence
        comparison_evidence[evidence_key] = {
            "connector_actual": status_string(item.get("connector_actual")),
            "native_actual": status_string(item.get("native_actual")),
            "same": True,
            "meaning": str(item.get("meaning") or ""),
        }

    return {
        "expected": expected_status,
        "native_actual": native_actual,
        "input_hash": input_hash,
        "request_sha256": str(native_case_run.get("request_sha256") or ""),
        "rules_sha256": str(native_case_run.get("rules_sha256") or ""),
        "libmodsecurity": str(native_case_run.get("libmodsecurity") or ""),
        "native_result_path": str(native_case_run.get("native_result_path") or ""),
        "run_dir": str(native_case_run.get("run_dir") or ""),
        "row_evidence": row_evidence,
        "connector_comparison": comparison_evidence,
    }


def apply_native_transformation_semantics_classification(
    mismatches: list[dict[str, Any]],
    *,
    connector_root: Path,
    build_root: Path,
    verified_run_root: Path,
) -> tuple[list[dict[str, Any]], list[Path]]:
    native_inputs: list[Path] = []
    for case_name in sorted(TRANSFORMATION_NATIVE_SEMANTICS_CASES):
        candidates = {
            (str(row["connector"]), str(row["variant"])): row
            for row in mismatches
            if row.get("case") == case_name
            and row.get("connector") in SEMICOLON_COLLECTION_CONNECTORS
            and row.get("variant") in SEMICOLON_COLLECTION_VARIANTS
        }
        latest = latest_native_case_run(verified_run_root, case_name)
        if latest is None:
            continue
        native_case_run, native_path = latest
        evidence = valid_native_transformation_semantics_evidence(
            native_case_run,
            candidates,
            connector_root=connector_root,
            build_root=build_root,
        )
        if evidence is None:
            continue
        native_inputs.append(native_path)
        for key, row in candidates.items():
            evidence_key = f"{key[0]}:{key[1]}"
            row["classification"] = TRANSFORMATION_NATIVE_SEMANTICS_CLASSIFICATION
            row["technical_cause"] = TRANSFORMATION_NATIVE_SEMANTICS_NOTE
            row["code_fix_needed"] = False
            row["test_expectation_wrong"] = False
            row["document_only"] = True
            row["classification_note"] = TRANSFORMATION_NATIVE_SEMANTICS_NOTE
            row["classification_evidence"] = {
                "note": TRANSFORMATION_NATIVE_SEMANTICS_NOTE,
                "native_case_run": str(native_path),
                "native_run_dir": evidence["run_dir"],
                "native_result_path": evidence["native_result_path"],
                "expected": evidence["expected"],
                "native_actual": evidence["native_actual"],
                "input_hash": evidence["input_hash"],
                "request_sha256": evidence["request_sha256"],
                "rules_sha256": evidence["rules_sha256"],
                "libmodsecurity": evidence["libmodsecurity"],
                "row_evidence": evidence["row_evidence"][evidence_key],
                "connector_comparison": evidence["connector_comparison"][evidence_key],
            }
    return mismatches, native_inputs


def xml_parser_semantics_result_evidence(
    row: dict[str, Any],
    *,
    connector_root: Path,
    build_root: Path,
    expected_status: str,
    native_actual: str,
) -> dict[str, Any] | None:
    if row.get("case") != XML_PARSER_SEMANTICS_CASE:
        return None
    if row.get("connector") not in SEMICOLON_COLLECTION_CONNECTORS:
        return None
    if row.get("variant") not in SEMICOLON_COLLECTION_VARIANTS:
        return None
    if row.get("category") != "body-processors":
        return None
    if row.get("status") != "fail" or row.get("expected") != expected_status or row.get("actual") != native_actual:
        return None
    if row.get("full_matrix_refresh_needed") is not False:
        return None
    result_path = resolve_evidence_file(str(row.get("evidence_file") or ""), connector_root=connector_root, build_root=build_root)
    result = read_json(result_path)
    if result.get("live_executed") is not True:
        return None
    if status_string(result.get("expected_status")) != expected_status:
        return None
    if status_string(result.get("actual_status", result.get("observed_status"))) != native_actual:
        return None
    if str(result.get("observed_transport_result") or "") not in {"", "http_status"}:
        return None

    evidence: dict[str, Any] = {
        "result": rel(result_path, build_root),
        "expected": expected_status,
        "actual": native_actual,
        "live_executed": "true",
        "full_matrix_refresh_needed": "false",
        "observed_transport_result": str(result.get("observed_transport_result") or "http_status"),
        "modsecurity_processed": str(result.get("modsecurity_processed", "n/a")).lower(),
        "request_body_seen": str(result.get("request_body_seen", "n/a")).lower(),
    }
    if row["connector"] == "haproxy":
        if result.get("modsecurity_processed") is not True or result.get("request_body_seen") is not True:
            return None
        decision_log_path = result_decision_log_path(result_path, result)
        entries = read_jsonl(decision_log_path)
        if len(entries) != 1:
            return None
        decision = entries[0]
        if decision.get("live_executed") is not True or decision.get("modsecurity_processed") is not True:
            return None
        if decision.get("request_body_seen") is not True:
            return None
        if decision.get("decision") != "pass" or decision.get("disruptive") is not False:
            return None
        if str(decision.get("matched_variable") or "") or str(decision.get("matched_value_snippet") or ""):
            return None
        evidence["decision_log"] = rel(decision_log_path, build_root)
        evidence["decision"] = "pass"
        evidence["rule_id"] = str(decision.get("rule_id") or "0")
        evidence["matched_variable"] = str(decision.get("matched_variable") or "")
        evidence["matched_value_snippet"] = str(decision.get("matched_value_snippet") or "")
    return evidence


def valid_xml_parser_semantics_evidence(
    native_case_run: dict[str, Any],
    candidates: dict[tuple[str, str], dict[str, Any]],
    *,
    connector_root: Path,
    build_root: Path,
) -> dict[str, Any] | None:
    if str(native_case_run.get("case") or "") != XML_PARSER_SEMANTICS_CASE:
        return None
    if str(native_case_run.get("status") or "") != "fail":
        return None
    if str(native_case_run.get("decision") or "") != "DOCUMENT":
        return None
    if str(native_case_run.get("classification_hint") or "") != "likely_framework_expected_behavior_gap_or_libmodsecurity_semantics":
        return None
    if native_case_run.get("native_match") is not False:
        return None
    if native_case_run.get("full_matrix_refresh_needed") is not False:
        return None
    input_hash = str(native_case_run.get("input_hash") or "")
    if not input_hash:
        return None

    expected_status = status_string(native_case_run.get("expected_status"))
    native_actual = status_string(native_case_run.get("native_actual"))
    if expected_status != "403" or native_actual != "200":
        return None

    case_path = Path(str(native_case_run.get("case_path") or ""))
    try:
        case_text = case_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if "ctl:requestBodyProcessor=XML" not in case_text or "SecRule XML" not in case_text:
        return None

    log_evidence = native_case_run.get("log_evidence")
    if not isinstance(log_evidence, dict):
        return None
    if log_evidence.get("rule_ids") not in ([], None):
        return None
    if log_evidence.get("matched_data") not in ([], None):
        return None

    logs_dir = Path(str(native_case_run.get("logs_dir") or ""))
    debug_log = logs_dir / "debug.log"
    try:
        debug_text = debug_log.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    required_debug_markers = [
        "XML: Initialising parser.",
        "XML: Parsing complete (well_formed 0).",
        "XML: Failed to parse document.",
        "(Rule: 4408) Executing operator",
        "Rule returned 0.",
    ]
    if any(marker not in debug_text for marker in required_debug_markers):
        return None

    expected_matrix = {
        (connector, variant)
        for connector in SEMICOLON_COLLECTION_CONNECTORS
        for variant in SEMICOLON_COLLECTION_VARIANTS
    }
    comparisons = native_case_run.get("connector_comparison")
    if not isinstance(comparisons, list):
        return None
    comparison_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    for item in comparisons:
        if not isinstance(item, dict):
            return None
        key = (str(item.get("connector") or ""), str(item.get("variant") or ""))
        comparison_by_key[key] = item
    if set(comparison_by_key) != expected_matrix or set(candidates) != expected_matrix:
        return None

    row_evidence: dict[str, dict[str, Any]] = {}
    comparison_evidence: dict[str, dict[str, Any]] = {}
    for key, item in comparison_by_key.items():
        if item.get("same") is not True:
            return None
        if status_string(item.get("native_actual")) != native_actual:
            return None
        if status_string(item.get("connector_actual")) != native_actual:
            return None
        if str(item.get("meaning") or "") != "same_as_native":
            return None
        if item.get("full_matrix_refresh_needed") is not False:
            return None
        row = candidates[key]
        evidence = xml_parser_semantics_result_evidence(
            row,
            connector_root=connector_root,
            build_root=build_root,
            expected_status=expected_status,
            native_actual=native_actual,
        )
        if evidence is None:
            return None
        evidence_key = f"{key[0]}:{key[1]}"
        row_evidence[evidence_key] = evidence
        comparison_evidence[evidence_key] = {
            "connector_actual": status_string(item.get("connector_actual")),
            "native_actual": status_string(item.get("native_actual")),
            "same": True,
            "meaning": str(item.get("meaning") or ""),
        }

    return {
        "expected": expected_status,
        "native_actual": native_actual,
        "input_hash": input_hash,
        "request_sha256": str(native_case_run.get("request_sha256") or ""),
        "rules_sha256": str(native_case_run.get("rules_sha256") or ""),
        "libmodsecurity": str(native_case_run.get("libmodsecurity") or ""),
        "native_result_path": str(native_case_run.get("native_result_path") or ""),
        "native_case_path": str(case_path),
        "run_dir": str(native_case_run.get("run_dir") or ""),
        "debug_log": str(debug_log),
        "xml_processor_control_present": True,
        "parser_debug_markers": required_debug_markers,
        "row_evidence": row_evidence,
        "connector_comparison": comparison_evidence,
    }


def apply_xml_parser_semantics_classification(
    mismatches: list[dict[str, Any]],
    *,
    connector_root: Path,
    build_root: Path,
    verified_run_root: Path,
) -> tuple[list[dict[str, Any]], list[Path]]:
    candidates = {
        (str(row["connector"]), str(row["variant"])): row
        for row in mismatches
        if row.get("case") == XML_PARSER_SEMANTICS_CASE
        and row.get("connector") in SEMICOLON_COLLECTION_CONNECTORS
        and row.get("variant") in SEMICOLON_COLLECTION_VARIANTS
    }
    latest = latest_native_case_run(verified_run_root, XML_PARSER_SEMANTICS_CASE)
    if latest is None:
        return mismatches, []
    native_case_run, native_path = latest
    evidence = valid_xml_parser_semantics_evidence(
        native_case_run,
        candidates,
        connector_root=connector_root,
        build_root=build_root,
    )
    if evidence is None:
        return mismatches, []

    for key, row in candidates.items():
        evidence_key = f"{key[0]}:{key[1]}"
        row["classification"] = XML_PARSER_SEMANTICS_CLASSIFICATION
        row["technical_cause"] = XML_PARSER_SEMANTICS_NOTE
        row["code_fix_needed"] = False
        row["test_expectation_wrong"] = False
        row["document_only"] = True
        row["classification_note"] = XML_PARSER_SEMANTICS_NOTE
        row["classification_evidence"] = {
            "note": XML_PARSER_SEMANTICS_NOTE,
            "native_case_run": str(native_path),
            "native_case_path": evidence["native_case_path"],
            "native_run_dir": evidence["run_dir"],
            "native_result_path": evidence["native_result_path"],
            "debug_log": evidence["debug_log"],
            "expected": evidence["expected"],
            "native_actual": evidence["native_actual"],
            "input_hash": evidence["input_hash"],
            "request_sha256": evidence["request_sha256"],
            "rules_sha256": evidence["rules_sha256"],
            "libmodsecurity": evidence["libmodsecurity"],
            "xml_processor_control_present": evidence["xml_processor_control_present"],
            "parser_debug_markers": evidence["parser_debug_markers"],
            "row_evidence": evidence["row_evidence"][evidence_key],
            "connector_comparison": evidence["connector_comparison"][evidence_key],
        }
    return mismatches, [native_path]


def row_from_case(
    *,
    case: dict[str, Any],
    connector: str,
    variant: str,
    evidence_file: Path,
    source_file: Path,
    source_scope: str,
    connector_root: Path,
    build_root: Path,
) -> dict[str, Any] | None:
    status = str(case.get("status") or "").lower()
    if status in {"", "pass"}:
        return None
    expected, actual = expected_actual(case)
    classification, cause, code_fix, expectation_wrong, document_only = classify_case(case)
    evidence = str(case.get("evidence_path") or evidence_file)
    case_name = str(case.get("name") or case.get("case") or Path(str(case.get("path") or "unknown")).stem)
    runtime_state = runtime_evidence_state(case, expected, actual)
    row = {
        "connector": connector,
        "variant": variant,
        "case": case_name,
        "expected": expected,
        "actual": actual,
        "status": status,
        "classification": classification,
        "runtime_evidence_state": runtime_state,
        "failure_mode": runtime_failure_mode(case, case_name),
        "runtime_reached": runtime_state.startswith("runtime_reached"),
        "full_matrix_refresh_needed": full_matrix_refresh_needed_for_case(case, evidence),
        "technical_cause": cause,
        "code_fix_needed": code_fix,
        "test_expectation_wrong": expectation_wrong,
        "document_only": document_only,
        "source": source_text(case),
        "reason": str(case.get("reason") or ""),
        "evidence_file": rel(evidence, connector_root),
        "source_file": rel(source_file, connector_root),
        "source_scope": source_scope,
        "requires_crs": case.get("requires_crs"),
        "category": case.get("category") or "-",
        "capabilities": case.get("capabilities") or [],
        "known_limitations": case.get("known_limitations") or [],
    }
    if row["evidence_file"].startswith("/"):
        row["evidence_file"] = rel(evidence, build_root)
    if row["source_file"].startswith("/"):
        row["source_file"] = rel(source_file, build_root)
    fixture_evidence = multipart_fixture_gap(
        row,
        evidence=evidence,
        connector_root=connector_root,
        build_root=build_root,
    )
    if fixture_evidence is not None and row["classification"] in CRITICAL_CATEGORIES:
        row["classification"] = "multipart_fixture_gap"
        row["technical_cause"] = (
            "Multipart smoke fixture emitted an empty-argument ModSecurity operator, so the connector rejected "
            "the generated rules before a live runtime result could be compared."
        )
        row["code_fix_needed"] = True
        row["test_expectation_wrong"] = False
        row["document_only"] = True
        row["classification_note"] = fixture_evidence["note"]
        row["classification_evidence"] = fixture_evidence
    detection_only_evidence = with_mrts_detection_only_overlay(
        row,
        evidence=evidence,
        connector_root=connector_root,
        build_root=build_root,
    )
    if detection_only_evidence is not None and row["classification"] in CRITICAL_CATEGORIES:
        connector_label = {"apache": "Apache", "haproxy": "HAProxy", "nginx": "NGINX"}[row["connector"]]
        classification_note = str(detection_only_evidence.get("note") or MRTS_DETECTION_ONLY_NOTE)
        row["classification"] = MRTS_DETECTION_ONLY_CLASSIFICATION
        row["technical_cause"] = (
            f"{connector_label} with-MRTS loaded an MRTS rule that sets ctl:ruleEngine=DetectionOnly; "
            "the runtime log shows the smoke rule matched, but disruptive actions are non-blocking in this overlay."
        )
        row["code_fix_needed"] = False
        row["test_expectation_wrong"] = False
        row["document_only"] = True
        row["classification_note"] = classification_note
        row["classification_evidence"] = detection_only_evidence
    crs_detection_only_evidence = crs_sqli_with_mrts_detection_only_overlay(
        row,
        evidence=evidence,
        connector_root=connector_root,
        build_root=build_root,
    )
    if crs_detection_only_evidence is not None and row["classification"] in CRITICAL_CATEGORIES:
        row["classification"] = MRTS_DETECTION_ONLY_CLASSIFICATION
        row["technical_cause"] = (
            "The CRS SQLi fixture matches CRS request rules and reaches the inbound anomaly blocking rule, "
            "but the with-MRTS variant loads MRTS_001_INIT DetectionOnly. The no-MRTS control blocks with "
            "HTTP 403, while the with-MRTS overlay records a report-only intervention and returns HTTP 200."
        )
        row["code_fix_needed"] = False
        row["test_expectation_wrong"] = False
        row["document_only"] = True
        row["classification_note"] = CRS_SQLI_WITH_MRTS_DETECTION_ONLY_NOTE
        row["classification_evidence"] = crs_detection_only_evidence
    nginx_phase4_enforcement_evidence = nginx_phase4_response_body_enforcement_gap(
        row,
        evidence=evidence,
        connector_root=connector_root,
        build_root=build_root,
    )
    if nginx_phase4_enforcement_evidence is not None and row["classification"] in CRITICAL_CATEGORIES:
        row["classification"] = NGINX_PHASE4_RESPONSE_BODY_ENFORCEMENT_CLASSIFICATION
        row["technical_cause"] = (
            "NGINX records a libmodsecurity phase-4 RESPONSE_BODY disruptive match in error/audit evidence, "
            "but the response has already been sent through the current connector path and the observed HTTP "
            "status remains 200. Apache and HAProxy controls can satisfy the same generic deny fixture; this "
            "row documents the NGINX Phase-4 response-body enforcement boundary."
        )
        row["code_fix_needed"] = False
        row["test_expectation_wrong"] = False
        row["document_only"] = True
        row["classification_note"] = NGINX_PHASE4_RESPONSE_BODY_ENFORCEMENT_NOTE
        row["classification_evidence"] = nginx_phase4_enforcement_evidence
    phase4_no_disruptive_evidence = nginx_phase4_rule_match_no_disruptive_intervention(
        row,
        evidence=evidence,
        connector_root=connector_root,
        build_root=build_root,
    )
    if phase4_no_disruptive_evidence is not None and row["classification"] in CRITICAL_CATEGORIES:
        row["classification"] = PHASE4_RULE_MATCH_NO_DISRUPTIVE_INTERVENTION_CLASSIFICATION
        row["technical_cause"] = (
            "The NGINX with-MRTS log-only fixture reaches HTTP 200 as expected and the error log shows the "
            "phase-4 RESPONSE_BODY rule match. The only failed assertion is connector phase4.log content; "
            "with MRTS_001_INIT DetectionOnly active there is no disruptive connector intervention event to emit."
        )
        row["code_fix_needed"] = False
        row["test_expectation_wrong"] = False
        row["document_only"] = True
        row["classification_note"] = PHASE4_RULE_MATCH_NO_DISRUPTIVE_INTERVENTION_NOTE
        row["classification_evidence"] = phase4_no_disruptive_evidence
    secaction_detection_only_evidence = secaction_with_mrts_detection_only_overlay(
        row,
        evidence=evidence,
        connector_root=connector_root,
        build_root=build_root,
    )
    if secaction_detection_only_evidence is not None and row["classification"] in CRITICAL_CATEGORIES:
        row["classification"] = SECACTION_DETECTION_ONLY_CLASSIFICATION
        row["technical_cause"] = (
            "The v3 SecAction block fixture is loaded as id 3312, and no-MRTS/native controls block with HTTP 403. "
            "The with-MRTS variant loads MRTS_001_INIT, which sets ctl:ruleEngine=DetectionOnly for the transaction, "
            "so the disruptive SecAction is report-only and the observed HTTP status remains 200."
        )
        row["code_fix_needed"] = False
        row["test_expectation_wrong"] = False
        row["document_only"] = True
        row["classification_note"] = SECACTION_DETECTION_ONLY_NOTE
        row["classification_evidence"] = secaction_detection_only_evidence
    return row


def variant_from_result_path(path: Path, root: Path, connector: str, source_scope: str) -> str:
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        return source_scope
    if source_scope == "full_matrix" and len(parts) >= 3:
        return "/".join(parts[:2])
    if source_scope == "runtime_matrix":
        if len(parts) >= 4 and parts[0] in {"no-crs", "with-crs"}:
            return "/".join(parts[:2])
        if len(parts) >= 2 and parts[0] in {"force-all", "with-crs"}:
            return parts[0]
    return "default"


def collect_summary_rows(
    root: Path,
    connector_root: Path,
    build_root: Path,
    source_scope: str,
    min_mtime: float | None,
    search_roots: list[Path] | None = None,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    summary_paths: list[Path] = []
    for search_root in search_roots or [root]:
        if search_root.exists():
            summary_paths.extend(sorted(search_root.rglob("*-summary.json")))
    for summary_path in summary_paths:
        if not new_enough(summary_path, min_mtime):
            continue
        data = read_json(summary_path)
        for connector, summary in data.items():
            if not isinstance(summary, dict):
                continue
            cases = summary.get("cases")
            if not isinstance(cases, dict):
                continue
            variant = variant_from_result_path(summary_path, root, connector, source_scope)
            result_file = Path(str(summary.get("jsonl_path") or summary_path))
            for case in cases.values():
                if not isinstance(case, dict):
                    continue
                row = row_from_case(
                    case=case,
                    connector=str(case.get("executed_connector") or connector),
                    variant=variant,
                    evidence_file=result_file,
                    source_file=summary_path,
                    source_scope=source_scope,
                    connector_root=connector_root,
                    build_root=build_root,
                )
                if row is not None:
                    rows.append(row)
    return rows


def collect_jsonl_rows(
    root: Path,
    connector_root: Path,
    build_root: Path,
    source_scope: str,
    min_mtime: float | None,
    search_roots: list[Path] | None = None,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    jsonl_paths: list[Path] = []
    for search_root in search_roots or [root]:
        if search_root.exists():
            jsonl_paths.extend(sorted(search_root.rglob("*-results.jsonl")))
    for jsonl_path in jsonl_paths:
        if not new_enough(jsonl_path, min_mtime):
            continue
        connector = jsonl_path.name.removesuffix("-results.jsonl")
        variant = variant_from_result_path(jsonl_path, root, connector, source_scope)
        for case in read_jsonl(jsonl_path):
            row = row_from_case(
                case=case,
                connector=str(case.get("executed_connector") or connector),
                variant=variant,
                evidence_file=jsonl_path,
                source_file=jsonl_path,
                source_scope=source_scope,
                connector_root=connector_root,
                build_root=build_root,
            )
            if row is not None:
                rows.append(row)
    return rows


def collect_incomplete_jobs(root: Path, connector_root: Path, build_root: Path, min_mtime: float | None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for job_path in sorted(root.glob("*/*/*/job.json")):
        if not new_enough(job_path, min_mtime):
            continue
        job = read_json(job_path)
        connector = str(job.get("connector") or job_path.parent.name)
        test_variant = str(job.get("test_variant") or "unknown")
        mrts_variant = str(job.get("mrts_variant") or "unknown")
        variant = f"{test_variant}/{mrts_variant}"
        summary_path = Path(str(job.get("summary_path") or ""))
        return_code = job.get("return_code")
        job_status = str(job.get("status") or "")
        if summary_path.is_file() and (return_code == 0 or job_status == "completed_with_mismatches"):
            continue
        case = {
            "name": "__job__",
            "status": "blocked",
            "expected_status": "complete",
            "actual_status": f"return_code={return_code}",
            "reason": f"job did not complete cleanly; summary_path={summary_path}",
        }
        classification, cause, code_fix, expectation_wrong, document_only = classify_case(case, incomplete=True)
        rows.append(
            {
                "connector": connector,
                "variant": variant,
                "case": "__job__",
                "expected": "complete",
                "actual": f"return_code={return_code}",
                "status": "blocked",
                "classification": classification,
                "technical_cause": cause,
                "code_fix_needed": code_fix,
                "test_expectation_wrong": expectation_wrong,
                "document_only": document_only,
                "source": "-",
                "reason": str(case["reason"]),
                "evidence_file": rel(job_path, build_root),
                "source_file": rel(job_path, build_root),
                "source_scope": "full_matrix",
                "requires_crs": None,
                "category": "producer-job",
                "capabilities": [],
                "known_limitations": [],
            }
        )
    return rows


def dedupe_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    deduped: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    priority = {"full_matrix": 0, "runtime_matrix": 1}
    for row in rows:
        key = (row["source_scope"], row["connector"], row["variant"], row["case"])
        existing = deduped.get(key)
        if existing is None:
            deduped[key] = row
            continue
        if priority.get(row["source_scope"], 9) < priority.get(existing["source_scope"], 9):
            deduped[key] = row
    return sorted(deduped.values(), key=lambda item: (item["connector"], item["variant"], item["case"], item["source_scope"]))


def command_summary(commands: list[dict[str, Any]], manifest_rows: list[dict[str, Any]], profile: str) -> dict[str, Any]:
    full = command_for(commands, "full-matrix-parallel")
    runtime = command_for(commands, "runtime-matrix-all")
    full_status = str(full.get("status") or "not_run")
    full_rc = full.get("return_code")
    expected_jobs = 0 if profile == "smoke" else 12
    full_runtime_complete = bool(full.get("runtime_complete"))
    if expected_jobs and len(manifest_rows) >= expected_jobs:
        full_runtime_complete = True
    full_complete = full_runtime_complete
    full_runtime_status = str(
        full.get("runtime_status")
        or ("runtime_completed_with_mismatches" if full_complete and any(row.get("return_code") not in {0, None} for row in manifest_rows) else "")
        or ("runtime_completed" if full_complete else "runtime_timeout" if full.get("classification") == "blocked_timeout" else "not_run")
    )
    return {
        "runtime_matrix_all": runtime,
        "full_matrix_parallel": full,
        "full_matrix_complete": full_complete,
        "full_matrix_runtime_status": full_runtime_status,
        "full_matrix_expected_jobs": expected_jobs,
        "full_matrix_completed_jobs": len(manifest_rows),
        "full_matrix_job_statuses": [
            {
                "connector": row.get("connector"),
                "variant": f"{row.get('test_variant')}/{row.get('mrts_variant')}",
                "return_code": row.get("return_code"),
                "duration_seconds": row.get("duration_seconds"),
                "log_path": row.get("log_path"),
                "summary_path": row.get("summary_path"),
            }
            for row in manifest_rows
        ],
        "full_matrix_status": full_status,
        "full_matrix_return_code": full_rc,
        "full_matrix_classification": full.get("classification") or "not_run",
        "full_matrix_timeout": str(full.get("classification") or "") == "blocked_timeout" and not full_complete,
        "full_matrix_refresh_timeout": str(full.get("refresh_status") or "") == "refresh_timeout",
        "report_refresh_status": str(full.get("refresh_status") or "not_recorded"),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Verified Runtime Mismatch Analysis",
        "",
        f"Verified run id: `{payload['verified_run_id']}`",
        "",
        "This report is generated only from verified runtime producer files. It does not invent missing PASS/FAIL values.",
        "",
        "## Summary",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Mismatches | `{payload['mismatch_count']}` |",
        f"| Critical mismatches | `{payload['critical_mismatch_count']}` |",
        f"| Full matrix complete | `{str(payload['full_matrix']['complete']).lower()}` |",
        f"| Full matrix runtime status | `{payload['full_matrix'].get('runtime_status', 'unknown')}` |",
        f"| Full matrix jobs | `{payload['full_matrix'].get('completed_jobs', 0)}/{payload['full_matrix'].get('expected_jobs', 0)}` |",
        f"| Full matrix status | `{payload['full_matrix']['status']}` |",
        f"| Full matrix timeout | `{str(payload['full_matrix']['timeout']).lower()}` |",
        f"| Full matrix refresh timeout | `{str(payload['full_matrix'].get('refresh_timeout', False)).lower()}` |",
        f"| Evidence scope | `{payload['evidence_scope']}` |",
        "",
        "## Inputs",
        "",
        "| Input | Status | SHA256 |",
        "|---|---|---|",
    ]
    for item in payload["inputs"]:
        lines.append(f"| `{item['path']}` | {item['status']} | `{item.get('sha256', '-')}` |")
    lines.extend(["", "## By Connector", "", "| Connector | Count |", "|---|---:|"])
    for connector, count in sorted(payload["by_connector"].items()):
        lines.append(f"| {connector} | {count} |")
    lines.extend(["", "## By Category", "", "| Category | Count |", "|---|---:|"])
    for category, count in sorted(payload["by_classification"].items()):
        lines.append(f"| {category} | {count} |")
    lines.extend(["", "## Top Cases", "", "| Case | Count |", "|---|---:|"])
    for item in payload["top_cases"][:20]:
        lines.append(f"| `{item['case']}` | {item['count']} |")
    lines.extend(
        [
            "",
            "## Mismatch Table",
            "",
            "| Connector | Variant | Case | Expected | Actual | Status | Classification | Evidence File |",
            "|---|---|---|---|---|---|---|---|",
        ]
    )
    for row in payload["mismatches"][:200]:
        lines.append(
            f"| {row['connector']} | {row['variant']} | `{row['case']}` | `{row['expected']}` | "
            f"`{row['actual']}` | {row['status']} | {row['classification']} | `{row['evidence_file']}` |"
        )
    if payload["mismatch_count"] > 200:
        lines.append(f"| ... | ... | `{payload['mismatch_count'] - 200} more rows in JSON` | ... | ... | ... | ... | ... |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector-root", default=".")
    parser.add_argument("--framework-root", default=None)
    parser.add_argument("--build-root", default=os.environ.get("BUILD_ROOT"))
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--verified-run-id", default=os.environ.get("VERIFIED_RUN_ID"))
    parser.add_argument("--verified-commands-file", default=os.environ.get("VERIFIED_RUN_COMMANDS_FILE"))
    args = parser.parse_args()

    connector_root = Path(args.connector_root).resolve()
    framework_root = Path(args.framework_root).resolve() if args.framework_root else connector_root / "modules/ModSecurity-test-Framework"
    default_paths = verified_runtime_paths(os.environ)
    build_root = Path(args.build_root or default_paths["BUILD_ROOT"]).resolve()
    verified_run_root = Path(default_paths["VERIFIED_RUN_ROOT"]).resolve()
    try:
        verified_run_id = validate_verified_run_id(
            args.verified_run_id or current_verified_run_id(connector_root)
        )
    except VerifiedRunIdError as exc:
        parser.error(str(exc))
    os.environ["VERIFIED_RUN_ID"] = verified_run_id
    output_dir = Path(args.output_dir).resolve() if args.output_dir else connector_root / "reports/testing/generated/manifest"
    commands_file = Path(args.verified_commands_file).resolve() if args.verified_commands_file else build_root / "verified-runs" / verified_run_id / "verified-commands.json"
    results_root = build_root / "results"
    full_matrix_root = build_root / "full-matrix"
    manifest_path = full_matrix_root / "full-runtime-matrix-runs.jsonl"
    completeness_path = report_path(connector_root, "full_matrix_job_completeness", "json")
    completeness = read_json(completeness_path)
    manifest_rows = read_jsonl(manifest_path)
    commands_payload = load_commands_payload(commands_file)
    commands = commands_payload.get("commands") if isinstance(commands_payload.get("commands"), list) else []
    profile = str(commands_payload.get("profile") or os.environ.get("VERIFIED_RUN_PROFILE") or "full")
    command_state = command_summary(commands, manifest_rows, profile)
    runtime_command = command_state.get("runtime_matrix_all") if isinstance(command_state.get("runtime_matrix_all"), dict) else {}
    full_command = command_state.get("full_matrix_parallel") if isinstance(command_state.get("full_matrix_parallel"), dict) else {}
    completeness_jobs = completeness.get("jobs") if isinstance(completeness.get("jobs"), list) else []
    completed_completeness_jobs = [
        job for job in completeness_jobs if job.get("status") in {"completed", "completed_with_mismatches"}
    ]
    completeness_total_jobs = int(completeness.get("total_jobs") or command_state["full_matrix_expected_jobs"] or 0)
    completeness_completed_jobs = int(completeness.get("complete_jobs") or len(completed_completeness_jobs))
    completeness_missing_jobs = [
        str(job.get("job_id"))
        for job in completeness_jobs
        if job.get("status") not in {"completed", "completed_with_mismatches"}
    ]
    if completeness_jobs:
        command_state["full_matrix_expected_jobs"] = completeness_total_jobs
        command_state["full_matrix_completed_jobs"] = completeness_completed_jobs
        command_state["full_matrix_complete"] = completeness_total_jobs > 0 and completeness_completed_jobs >= completeness_total_jobs
        command_state["full_matrix_job_statuses"] = [
            {
                "connector": job.get("connector"),
                "variant": f"{job.get('crs')}/{job.get('mrts')}",
                "status": job.get("status"),
                "return_code": job.get("return_code"),
                "duration_seconds": job.get("duration_seconds"),
                "summary_path": job.get("summary_path"),
                "log_path": job.get("log_path"),
                "manifest_recorded": job.get("manifest_recorded"),
            }
            for job in completeness_jobs
        ]
        if command_state["full_matrix_complete"]:
            mismatched_jobs = any(job.get("return_code") not in {0, None} for job in completed_completeness_jobs)
            command_state["full_matrix_runtime_status"] = (
                "completed_with_mismatches"
                if mismatched_jobs
                else "runtime_completed"
            )
            command_state["full_matrix_timeout"] = False
            command_state["full_matrix_refresh_timeout"] = False
            command_state["full_matrix_status"] = "complete"
            command_state["full_matrix_classification"] = "completed_with_mismatches" if mismatched_jobs else "complete"
        else:
            command_state["full_matrix_runtime_status"] = "runtime_timeout"
            command_state["full_matrix_timeout"] = True
    run_cutoff = parse_time(str(commands_payload.get("started_at_utc") or ""))
    runtime_cutoff = parse_time(runtime_command.get("started_at") if isinstance(runtime_command, dict) else None) or run_cutoff
    full_cutoff = parse_time(full_command.get("started_at") if isinstance(full_command, dict) else None)

    rows = []
    rows.extend(collect_summary_rows(results_root, connector_root, build_root, "runtime_matrix", runtime_cutoff))
    rows.extend(collect_jsonl_rows(results_root, connector_root, build_root, "runtime_matrix", runtime_cutoff))
    if full_command or completeness_jobs:
        full_search_roots = [
            Path(str(job.get("result_path") or job.get("summary_path") or "")).resolve().parent
            for job in completed_completeness_jobs
            if job.get("result_path") or job.get("summary_path")
        ] or [
            Path(str(item.get("results_dir"))).resolve()
            for item in manifest_rows
            if isinstance(item, dict) and item.get("results_dir")
        ]
        rows.extend(
            collect_summary_rows(
                full_matrix_root,
                connector_root,
                build_root,
                "full_matrix",
                full_cutoff,
                full_search_roots,
            )
        )
        rows.extend(
            collect_jsonl_rows(
                full_matrix_root,
                connector_root,
                build_root,
                "full_matrix",
                full_cutoff,
                full_search_roots,
            )
        )
        rows.extend(collect_incomplete_jobs(full_matrix_root, connector_root, build_root, full_cutoff))
    mismatches = dedupe_rows(rows)
    mismatches = apply_semicolon_collection_semantics_classification(
        mismatches,
        connector_root=connector_root,
        build_root=build_root,
    )
    mismatches = apply_collection_name_case_semantics_classification(
        mismatches,
        connector_root=connector_root,
        build_root=build_root,
    )
    mismatches = apply_nolog_expected_no_audit_classification(
        mismatches,
        connector_root=connector_root,
        build_root=build_root,
    )
    mismatches, native_semantics_inputs = apply_native_transformation_semantics_classification(
        mismatches,
        connector_root=connector_root,
        build_root=build_root,
        verified_run_root=verified_run_root,
    )
    mismatches, xml_semantics_inputs = apply_xml_parser_semantics_classification(
        mismatches,
        connector_root=connector_root,
        build_root=build_root,
        verified_run_root=verified_run_root,
    )
    native_semantics_inputs.extend(xml_semantics_inputs)

    by_connector = Counter(row["connector"] for row in mismatches)
    by_classification = Counter(row["classification"] for row in mismatches)
    top_cases = Counter(row["case"] for row in mismatches).most_common(50)
    critical_count = sum(1 for row in mismatches if row["classification"] in CRITICAL_CATEGORIES)
    payload = {
        "verified_run_id": verified_run_id,
        "data_source_policy": DATA_SOURCE_POLICY,
        "generated_at": utc_now(),
        "evidence_scope": "smoke-only" if profile == "smoke" else "full" if command_state["full_matrix_complete"] else "partial",
        "merge_readiness": "UNKNOWN" if profile == "smoke" else "UNKNOWN" if not command_state["full_matrix_complete"] else "FAIL" if critical_count else "PASS",
        "merge_readiness_reason": "not a full verified matrix run" if profile == "smoke" else "full matrix runtime incomplete" if not command_state["full_matrix_complete"] else "critical mismatches present" if critical_count else "no critical runtime mismatches",
        "inputs": input_records_for_sources(
            commands_file=commands_file,
            manifest_path=manifest_path,
            mismatches=mismatches,
            connector_root=connector_root,
            build_root=build_root,
            native_semantics_inputs=native_semantics_inputs,
        ),
        "artifact_roots": {
            "runtime_matrix_results": str(results_root),
            "full_matrix_results": str(full_matrix_root),
            "native_case_runs": str(verified_run_root / "native-case-runs"),
        },
        "commands": command_state,
        "artifact_filters": {
            "runtime_matrix_started_at": runtime_command.get("started_at") if isinstance(runtime_command, dict) else "",
            "full_matrix_started_at": full_command.get("started_at") if isinstance(full_command, dict) else "",
            "runtime_matrix_min_mtime": runtime_cutoff,
            "full_matrix_min_mtime": full_cutoff,
        },
        "full_matrix": {
            "complete": command_state["full_matrix_complete"],
            "runtime_status": command_state["full_matrix_runtime_status"],
            "expected_jobs": command_state["full_matrix_expected_jobs"],
            "completed_jobs": command_state["full_matrix_completed_jobs"],
            "job_statuses": command_state["full_matrix_job_statuses"],
            "status": command_state["full_matrix_status"],
            "return_code": command_state["full_matrix_return_code"],
            "classification": command_state["full_matrix_classification"],
            "timeout": command_state["full_matrix_timeout"],
            "refresh_timeout": command_state["full_matrix_refresh_timeout"],
            "report_refresh_status": command_state.get("report_refresh_status", "not_recorded"),
            "completeness": f"{command_state['full_matrix_completed_jobs']}/{command_state['full_matrix_expected_jobs']}",
            "manifest_path": str(manifest_path),
            "manifest_present": manifest_path.is_file(),
            "manifest_recorded_jobs": completeness.get("manifest_recorded_jobs", len(manifest_rows)),
            "missing_jobs": completeness_missing_jobs,
            "job_completeness_report": str(completeness_path),
        },
        "mismatch_count": len(mismatches),
        "critical_mismatch_count": critical_count,
        "by_connector": dict(sorted(by_connector.items())),
        "by_classification": dict(sorted(by_classification.items())),
        "top_cases": [{"case": case, "count": count} for case, count in top_cases],
        "mismatches": mismatches,
        "no_invented_values_statement": "All rows are parsed from runtime result files, job files, or verified command records; missing producer evidence is reported as timeout_or_incomplete.",
    }
    metadata = build_metadata(
        generated_by=GENERATED_REPORTS["verified_runtime_mismatch_analysis"].generator,
        make_target=GENERATED_REPORTS["verified_runtime_mismatch_analysis"].make_target,
        connector_root=connector_root,
        framework_root=framework_root,
        inputs=[commands_file, manifest_path, *native_semantics_inputs],
        generated_at=payload["generated_at"],
        report_key="verified_runtime_mismatch_analysis",
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / GENERATED_REPORTS["verified_runtime_mismatch_analysis"].filename("json")
    md_path = output_dir / GENERATED_REPORTS["verified_runtime_mismatch_analysis"].filename("md")
    json_path.write_text(generated_json_text(payload, metadata), encoding="utf-8")
    md_path.write_text(generated_markdown_text(render_markdown(payload), metadata), encoding="utf-8")
    print(md_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
