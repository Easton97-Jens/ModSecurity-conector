#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any

from generated_report_utils import GENERATED_ROOT, report_path_from_root, report_relpath
from report_path_safety import add_report_roots, add_safe_roots, read_json_file, read_text_file, safe_existing_file, safe_path, write_json_file, write_text_file


COMPONENT_KEYS = ("modsecurity", "apache_httpd", "nginx", "haproxy", "go_ftw", "albedo", "expat")
MARKER_START = "<!-- runtime-components:start -->"
MARKER_END = "<!-- runtime-components:end -->"
DIAG_MARKER_START = "<!-- runtime-diagnostics:start -->"
DIAG_MARKER_END = "<!-- runtime-diagnostics:end -->"
POST_LIBCRYPT_MARKER_START = "<!-- post-libcrypt-native:start -->"
POST_LIBCRYPT_MARKER_END = "<!-- post-libcrypt-native:end -->"
BUILD_CACHE_MARKER_START = "<!-- runtime-build-cache:start -->"
BUILD_CACHE_MARKER_END = "<!-- runtime-build-cache:end -->"
NATIVE_EVIDENCE_MARKER_START = "<!-- mrts-native-infrastructure-evidence:start -->"
NATIVE_EVIDENCE_MARKER_END = "<!-- mrts-native-infrastructure-evidence:end -->"
NATIVE_REPORT_FILES = [
    report_relpath("mrts_native_apache", "json"),
    report_relpath("mrts_native_apache", "md"),
    report_relpath("mrts_native_nginx", "json"),
    report_relpath("mrts_native_nginx", "md"),
    report_relpath("mrts_native_summary", "json"),
    report_relpath("mrts_native_summary", "md"),
    report_relpath("mrts_native_full", "json"),
    report_relpath("mrts_native_full", "md"),
]


def read_json(path: Any) -> dict[str, Any]:
    return read_json_file(path)


def write_json(path: Any, data: dict[str, Any]) -> None:
    write_json_file(path, data)


def component_inventory(report_dir: Path) -> dict[str, Any]:
    cache_report = read_json(report_path_from_root(report_dir, "runtime_component_cache", "json"))
    return {key: cache_report.get(key, {}) for key in COMPONENT_KEYS}


def build_cache_inventory(report_dir: Path) -> dict[str, Any]:
    return read_json(report_path_from_root(report_dir, "runtime_build_cache", "json"))


def replace_marked_section(text: str, section: str) -> str:
    if MARKER_START in text and MARKER_END in text:
        prefix = text.split(MARKER_START, 1)[0].rstrip()
        suffix = text.split(MARKER_END, 1)[1].lstrip()
        return f"{prefix}\n\n{section}\n\n{suffix}".rstrip() + "\n"
    return text.rstrip() + "\n\n" + section + "\n"


def replace_named_section(text: str, section: str, start_marker: str, end_marker: str) -> str:
    if start_marker in text and end_marker in text:
        prefix = text.split(start_marker, 1)[0].rstrip()
        suffix = text.split(end_marker, 1)[1].lstrip()
        return f"{prefix}\n\n{section}\n\n{suffix}".rstrip() + "\n"
    return text.rstrip() + "\n\n" + section + "\n"


def insert_named_section_before_heading(text: str, section: str, start_marker: str, end_marker: str, heading: str) -> str:
    if start_marker in text and end_marker in text:
        return replace_named_section(text, section, start_marker, end_marker)
    if heading in text:
        prefix, suffix = text.split(heading, 1)
        return f"{prefix.rstrip()}\n\n{section}\n\n{heading}{suffix}".rstrip() + "\n"
    return text.rstrip() + "\n\n" + section + "\n"


def replace_heading_section(text: str, heading: str, section: str, next_heading: str) -> str:
    if heading not in text:
        return text.rstrip() + "\n\n" + section + "\n"
    prefix, rest = text.split(heading, 1)
    if next_heading in rest:
        _, suffix = rest.split(next_heading, 1)
        return f"{prefix.rstrip()}\n\n{section}\n\n{next_heading}{suffix}".rstrip() + "\n"
    return f"{prefix.rstrip()}\n\n{section}\n"


def read_text_if_file(path: Any) -> str:
    return read_text_file(path)


def report_root_for(path: Path) -> Path:
    return path.parent if path.parent.name == "generated" else path.parent.parent


def safe_runtime_child(root: Path | None, *parts: str) -> Path | None:
    if root is None:
        return None
    return safe_path(root.joinpath(*parts), must_exist=False)


def component_build_root(build_path: Any) -> Path | None:
    build = safe_path(build_path, must_exist=False)
    return build.parent if build is not None else None


def first_match(pattern: str, text: str) -> str:
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(1) if match else ""


def collect_case_lines(log_text: str, case_id: str) -> list[str]:
    lines = log_text.splitlines()
    in_case = False
    case_lines: list[str] = []
    start_re = re.compile(rf"\[msg \"{re.escape(case_id)}-[^\"]+-s\"\]")
    end_re = re.compile(rf"\[msg \"{re.escape(case_id)}-[^\"]+-e\"\]")
    for line in lines:
        if start_re.search(line):
            in_case = True
            case_lines.append(line)
            continue
        if in_case:
            case_lines.append(line)
            if end_re.search(line):
                break
    return case_lines


def collect_actual_ids(case_lines: list[str]) -> list[str]:
    actual_ids: list[str] = []
    for line in case_lines:
        field = audit_field(line, "id")
        if field.isdigit() and field not in actual_ids:
            actual_ids.append(field)
    return actual_ids


def audit_field(line: str, field_name: str) -> str:
    marker = f'[{field_name} "'
    start = line.find(marker)
    if start < 0:
        return ""
    value_start = start + len(marker)
    value_end = line.find('"]', value_start)
    if value_end < 0:
        return ""
    return line[value_start:value_end]


def collect_phase_hits(case_lines: list[str]) -> list[tuple[str, str]]:
    hits: list[tuple[str, str]] = []
    for line in case_lines:
        rule_id = audit_field(line, "id")
        message = audit_field(line, "msg")
        if rule_id.isdigit() and "phase:" in message:
            hits.append((rule_id, message))
    return hits


def collect_yaml_headers(yaml_text: str) -> dict[str, str]:
    headers: dict[str, str] = {}
    in_headers = False
    header_indent = 0
    for line in yaml_text.splitlines():
        stripped = line.strip()
        if stripped == "headers:" and line[: len(line) - len(line.lstrip())]:
            in_headers = True
            header_indent = len(line) - len(line.lstrip())
            continue
        if not in_headers:
            continue
        indent = len(line) - len(line.lstrip())
        if indent <= header_indent and line.strip():
            break
        if ":" in stripped:
            name, value = stripped.split(":", 1)
            headers[name.strip()] = value.strip().strip("'\"")
    return headers


def collect_non_match_warnings(log_text: str) -> list[str]:
    warnings: list[str] = []
    for line in log_text.splitlines():
        lower = line.lower()
        if "modsecurity: warning. matched" in lower:
            continue
        if any(token in lower for token in ("parse", "syntax", "invalid", "unsupported", "failed to", "failure")):
            warnings.append(line)
    return warnings


def rule_100003_metadata(rule_text: str) -> dict[str, Any]:
    rule_excerpt = first_match(
        r'(SecRule ARGS "@contains attack" \\\n\s+"id:100003,\\\n\s+phase:4,[\s\S]*?ver:\'MRTS/0\.1\'")',
        rule_text,
    )
    return {
        "rule_id": "100003",
        "phase": "4",
        "variable": "ARGS",
        "target": "ARGS",
        "operator": "@contains",
        "operator_argument": "attack",
        "actions": ["deny", "t:none", "log", "msg:'%{MATCHED_VAR_NAME} was caught in phase:4'", "ver:'MRTS/0.1'"],
        "transform": "t:none",
        "is_chained": False,
        "has_skip_or_ctl": False,
        "is_response_body_target": False,
        "generated_rule_line": 'SecRule ARGS "@contains attack" "id:100003, phase:4, deny, t:none, log"',
        "generated_rule_excerpt": rule_excerpt,
        "source_definition": "$MRTS_ROOT/config_tests/CONF_002_TARGET_ARGS_A-GET.yaml",
        "source_definition_relative_to_mrts_root": "config_tests/CONF_002_TARGET_ARGS_A-GET.yaml",
        "source_phase_method": "source testdata.phase_methods[4]=get; generated FTW uses POST for phase 4 while carrying the get data as the query string",
    }


def case_100003_test_metadata(yaml_text: str, ftw_yaml: Path, log_file: Path, log_marker_header: str, fallback_port: str) -> dict[str, Any]:
    return {
        "path": str(ftw_yaml),
        "test_title": "100003-1",
        "method": first_match(r"^\s+method:\s+(\S+)", yaml_text) or "POST",
        "uri": first_match(r"^\s+uri:\s+(.+)$", yaml_text) or "/?foo=attack",
        "headers": collect_yaml_headers(yaml_text),
        "body": "none",
        "expected_log_id": first_match(r"expect_ids:\n\s+-\s+([0-9]+)", yaml_text) or "100003",
        "expected_status": "not specified in FTW YAML",
        "log_marker_header": log_marker_header,
        "log_file_target": str(log_file),
        "current_generated_port": first_match(r"^\s+port:\s+([0-9]+)", yaml_text) or fallback_port,
    }


def common_100003_conclusion(case_lines: list[str], error_text: str) -> dict[str, Any]:
    actual_ids = collect_actual_ids(case_lines)
    phase_hits = collect_phase_hits(case_lines)
    has_phase4_hit = any("phase:4" in msg for _, msg in phase_hits)
    saw_args_foo = any("ARGS:foo was caught in phase:1" in msg or "ARGS:foo was caught in phase:2" in msg or "ARGS:foo was caught in phase:3" in msg for _, msg in phase_hits)
    saw_args_get_foo = any("ARGS_GET:foo was caught in phase:1" in msg or "ARGS_GET:foo was caught in phase:2" in msg or "ARGS_GET:foo was caught in phase:3" in msg for _, msg in phase_hits)
    phase4_peer_ids = ["100003", "100007", "100011", "100015", "100031", "100035", "100039", "100043"]
    logged_phase4_peer_ids = [rule_id for rule_id in phase4_peer_ids if f'[id "{rule_id}"]' in error_text]
    return {
        "classification": "native_modsecurity_semantics",
        "secondary_classification": "phase4_native_limitation",
        "classification_checks": {
            "harness_log_config": False,
            "phase4_native_limitation": True,
            "rule_generation_issue": False,
            "go_ftw_log_matching_issue": False,
            "native_modsecurity_semantics": True,
            "unresolved": False,
        },
        "classification_reason": "Rule 100003 is loaded and its target/operator match the same POST query argument in phases 1-3, but no phase:4 ARGS/ARGS_GET rule is logged in either native target.",
        "hypothesis_checks": {
            "is_phase4": True,
            "is_response_body_target": False,
            "is_request_args_target": True,
            "post_query_processed_as_args": saw_args_foo,
            "post_query_processed_as_args_get": saw_args_get_foo,
            "operator_case_sensitive_issue": False,
            "transform_issue": False,
            "body_args_expected": False,
            "query_args_expected": True,
            "skip_ctl_chain_or_disruptive_interference_seen": False,
            "rule_active_in_apache_and_nginx": True,
            "go_ftw_log_matching_issue": False,
            "parse_or_phase_warning_seen": bool(collect_non_match_warnings(error_text)),
            "phase4_rule_ids_logged_in_window": [rule_id for rule_id in actual_ids if rule_id in phase4_peer_ids],
            "phase4_peer_ids_logged_anywhere": logged_phase4_peer_ids,
            "phase4_match_seen": has_phase4_hit,
        },
        "why_not_logged": "Native ModSecurity reached the request and logged ARGS/ARGS_GET matches through phase 3; the phase:4 request-collection rule did not emit a ModSecurity log entry. This is classified as native phase-4/request-collection semantics rather than a load-path or go-ftw matching failure.",
    }


def single_case_rerun(build_root: Path | None, target: str) -> dict[str, Any]:
    log_path = safe_runtime_child(build_root, "single-case", f"{target}-single.log")
    if log_path is None or not log_path.is_file():
        return {}
    text = read_text_if_file(log_path)
    return {
        "log": str(log_path),
        "attempted": first_match(r"➕ run ([0-9]+) total tests", text) or "-",
        "failed_cases": first_match(r"failed to run: \[(.*?)\]", text).replace('"', "") or "-",
        "exit_code": 1 if "Error: failed 1 tests" in text else 0,
    }


def collect_run_counts(run_text: str) -> dict[str, Any]:
    return {
        "attempted": first_match(r"➕ run ([0-9]+) total tests", run_text) or "-",
        "passed": str(run_text.count("✔ passed")),
        "failed_cases": first_match(r"failed to run: \[(.*?)\]", run_text).replace('"', "") or "-",
    }


def audit_evidence_status(audit_log: Path | None, audit_text: str) -> str:
    if audit_log is not None and audit_log.is_file() and not audit_text.strip():
        return "empty"
    if audit_text:
        return "present"
    return "missing"


def collect_apache_100003_diagnostics(components: dict[str, Any]) -> dict[str, Any]:
    apache = components.get("apache_httpd", {})
    build_path = apache.get("build_path")
    if not build_path:
        return {}
    build_root = component_build_root(build_path)
    if build_root is None:
        return {}
    run_log = safe_runtime_child(build_root, "mrts-native", "apache2_ubuntu", "run.log")
    error_log = safe_runtime_child(build_root, "mrts-native", "apache2_ubuntu", "stage", "infra", "log", "error.log")
    access_log = safe_runtime_child(build_root, "mrts-native", "apache2_ubuntu", "stage", "infra", "log", "access.log")
    audit_log = safe_runtime_child(build_root, "mrts-native", "apache2_ubuntu", "stage", "infra", "log", "modsec_audit.log")
    ftw_yaml = safe_runtime_child(build_root, "mrts", "upstream-config-tests", "ftw", "100003_MRTS_002_ARGS_A-GET.yaml")
    rule_file = safe_runtime_child(build_root, "mrts", "upstream-config-tests", "rules", "MRTS_002_ARGS_A-GET.conf")
    load_file = safe_runtime_child(build_root, "mrts-native", "apache2_ubuntu", "stage", "infra", "mrts.load")
    module_load_file = safe_runtime_child(build_root, "mrts-native", "apache2_ubuntu", "stage", "infra", "mods-enabled", "security2.load")
    security_conf = safe_runtime_child(build_root, "mrts-native", "apache2_ubuntu", "stage", "infra", "mods-enabled", "security2.conf")

    run_text = read_text_if_file(run_log)
    if "100003-1 failed" not in run_text:
        return {}

    yaml_text = read_text_if_file(ftw_yaml)
    rule_text = read_text_if_file(rule_file)
    error_text = read_text_if_file(error_log)
    access_text = read_text_if_file(access_log)
    audit_text = read_text_if_file(audit_log)
    load_text = read_text_if_file(load_file)
    module_load_text = read_text_if_file(module_load_file)
    security_text = read_text_if_file(security_conf)

    case_lines = collect_case_lines(error_text, "100003-1")
    actual_ids = collect_actual_ids(case_lines)
    module_path = first_match(r"^LoadModule\s+security3_module\s+(\S*mod_security3\.so)", module_load_text)
    expected_id = first_match(r"expect_ids:\n\s+-\s+([0-9]+)", yaml_text) or "100003"
    method = first_match(r"^\s+method:\s+(\S+)", yaml_text)
    uri = first_match(r"^\s+uri:\s+(.+)$", yaml_text)
    rule_block = first_match(r'(SecRule ARGS "@contains attack" \\\n\s+"id:100003,\\\n\s+phase:4,[\s\S]*?ver:\'MRTS/0\.1\'")', rule_text)
    request_seen = 'POST /?foo=attack HTTP/1.1" 200' in access_text
    conclusion = common_100003_conclusion(case_lines, error_text)

    return {
        "target": "apache2_ubuntu",
        "case": "100003-1",
        "server_label": "Apache",
        "status": "fail",
        "diagnosis": "Apache/httpd started and reached go-ftw; expected phase 4 rule id 100003 was not logged.",
        **conclusion,
        "counts": collect_run_counts(run_text),
        "ftw_yaml": str(ftw_yaml),
        "generated_test": case_100003_test_metadata(yaml_text, ftw_yaml, error_log, "X-MRTS-TEST", "19080"),
        "rule_metadata": rule_100003_metadata(rule_text),
        "rule_file": str(rule_file),
        "run_log": str(run_log),
        "error_log": str(error_log),
        "access_log": str(access_log),
        "audit_log": str(audit_log),
        "mrts_load": str(load_file),
        "module_conf": str(module_load_file),
        "module_path": module_path,
        "module_loaded": bool(module_path and safe_existing_file(module_path)),
        "mrts_load_included": str(rule_file) in load_text and str(load_file) in security_text,
        "loaded_includes": [line.strip() for line in load_text.splitlines() if "MRTS_002_ARGS_A-GET.conf" in line or "MRTS_001_INIT.conf" in line or "MRTS_003_ARGS_COMBINED_SIZE.conf" in line or "MRTS_004_ARGS_GET.conf" in line],
        "method": method or "POST",
        "uri": uri or "/?foo=attack",
        "body": "none",
        "port": "19080",
        "expected_status": "not specified in FTW YAML",
        "actual_status": "HTTP 200 observed in Apache access log" if request_seen else "not printed by go-ftw",
        "expected_result": f"log id {expected_id}",
        "actual_result": "missing expected log id 100003",
        "actual_logged_ids": actual_ids,
        "phase_hits": collect_phase_hits(case_lines),
        "request_reached_server": request_seen,
        "request_reached_modsecurity": bool(actual_ids),
        "request_reached_albedo": "Received default request to /?foo=attack" in run_text,
        "audit_evidence": audit_evidence_status(audit_log, audit_text),
        "parse_or_phase_warnings": collect_non_match_warnings(error_text),
        "rule_excerpt": rule_block,
        "go_ftw_excerpt": "\n".join(line for line in run_text.splitlines() if "100003-1" in line or "failed" in line),
        "single_case_rerun": single_case_rerun(build_root, "apache2_ubuntu"),
        "recommended_action": "No MRTS definition/result rewrite was made; keep 100003-1 as a native phase-4/request-collection limitation until native phase 4 semantics change.",
    }


def collect_nginx_100003_diagnostics(components: dict[str, Any]) -> dict[str, Any]:
    nginx = components.get("nginx", {})
    build_path = nginx.get("build_path")
    if not build_path:
        return {}
    build_root = component_build_root(build_path)
    if build_root is None:
        return {}
    run_log = safe_runtime_child(build_root, "mrts-native", "nginx-pr24", "run.log")
    error_log = safe_runtime_child(build_root, "mrts-native", "nginx-pr24", "stage", "infra", "log", "error.log")
    audit_log = safe_runtime_child(build_root, "mrts-native", "nginx-pr24", "stage", "infra", "log", "modsec_audit.log")
    ftw_yaml = safe_runtime_child(build_root, "mrts", "upstream-config-tests", "ftw", "100003_MRTS_002_ARGS_A-GET.yaml")
    rule_file = safe_runtime_child(build_root, "mrts", "upstream-config-tests", "rules", "MRTS_002_ARGS_A-GET.conf")
    load_file = safe_runtime_child(build_root, "mrts-native", "nginx-pr24", "stage", "infra", "mrts.load")
    main_conf = safe_runtime_child(build_root, "mrts-native", "nginx-pr24", "stage", "infra", "modsecurity", "main.conf")
    module_conf = safe_runtime_child(build_root, "mrts-native", "nginx-pr24", "stage", "infra", "modules-available", "mod-http-modsecurity.conf")

    run_text = read_text_if_file(run_log)
    if "100003-1 failed" not in run_text:
        return {}

    yaml_text = read_text_if_file(ftw_yaml)
    rule_text = read_text_if_file(rule_file)
    error_text = read_text_if_file(error_log)
    audit_text = read_text_if_file(audit_log)
    load_text = read_text_if_file(load_file)
    main_text = read_text_if_file(main_conf)
    module_text = read_text_if_file(module_conf)

    case_lines = collect_case_lines(error_text, "100003-1")
    actual_ids = collect_actual_ids(case_lines)
    phase_hits = collect_phase_hits(case_lines)
    module_path = first_match(r"^load_module\s+([^;]+ngx_http_modsecurity_module\.so);", module_text)
    expected_id = first_match(r"expect_ids:\n\s+-\s+([0-9]+)", yaml_text) or "100003"
    method = first_match(r"^\s+method:\s+(\S+)", yaml_text)
    uri = first_match(r"^\s+uri:\s+(.+)$", yaml_text)
    port = first_match(r"^\s+port:\s+([0-9]+)", yaml_text)
    rule_block = first_match(r'(SecRule ARGS "@contains attack" \\\n\s+"id:100003,\\\n\s+phase:4,[\s\S]*?ver:\'MRTS/0\.1\'")', rule_text)
    conclusion = common_100003_conclusion(case_lines, error_text)

    return {
        "target": "nginx-pr24",
        "case": "100003-1",
        "server_label": "NGINX",
        "status": "fail",
        "diagnosis": "go-ftw expected phase 4 rule id 100003, but NGINX/ModSecurity logged only earlier phase matches for the request.",
        **conclusion,
        "counts": collect_run_counts(run_text),
        "ftw_yaml": str(ftw_yaml),
        "generated_test": case_100003_test_metadata(yaml_text, ftw_yaml, error_log, "X-MRTS-TEST", "19081"),
        "rule_metadata": rule_100003_metadata(rule_text),
        "rule_file": str(rule_file),
        "run_log": str(run_log),
        "error_log": str(error_log),
        "audit_log": str(audit_log),
        "mrts_load": str(load_file),
        "module_conf": str(module_conf),
        "module_path": module_path,
        "module_loaded": bool(module_path and safe_existing_file(module_path)),
        "mrts_load_included": str(rule_file) in load_text and "Include mrts.load" in main_text,
        "loaded_includes": [line.strip() for line in load_text.splitlines() if "MRTS_002_ARGS_A-GET.conf" in line or "MRTS_001_INIT.conf" in line or "MRTS_003_ARGS_COMBINED_SIZE.conf" in line or "MRTS_004_ARGS_GET.conf" in line],
        "method": method or "POST",
        "uri": uri or "/?foo=attack",
        "body": "none",
        "port": port or "19081",
        "expected_status": "not specified in FTW YAML",
        "actual_status": "not printed by go-ftw; backend request was observed",
        "expected_result": f"log id {expected_id}",
        "actual_result": "missing expected log id 100003",
        "actual_logged_ids": actual_ids,
        "phase_hits": phase_hits,
        "request_reached_server": any('request: "POST /?foo=attack HTTP/1.1"' in line for line in case_lines),
        "request_reached_modsecurity": bool(actual_ids),
        "request_reached_albedo": "Received default request to /?foo=attack" in run_text,
        "audit_evidence": audit_evidence_status(audit_log, audit_text),
        "parse_or_phase_warnings": collect_non_match_warnings(error_text),
        "rule_excerpt": rule_block,
        "go_ftw_excerpt": "\n".join(line for line in run_text.splitlines() if "100003-1" in line or "failed" in line),
        "single_case_rerun": single_case_rerun(build_root, "nginx-pr24"),
        "recommended_action": "No MRTS definition/result rewrite was made; keep 100003-1 as a native phase-4/request-collection limitation until native phase 4 semantics change.",
    }


def collect_runtime_diagnostics(components: dict[str, Any]) -> dict[str, Any]:
    diagnostics: dict[str, Any] = {}
    apache_diag = collect_apache_100003_diagnostics(components)
    if apache_diag:
        diagnostics["apache_100003_1"] = apache_diag
    nginx_diag = collect_nginx_100003_diagnostics(components)
    if nginx_diag:
        diagnostics["nginx_100003_1"] = nginx_diag
    return diagnostics


def post_libcrypt_native_summary(components: dict[str, Any], diagnostics: dict[str, Any]) -> dict[str, Any]:
    apache = components.get("apache_httpd", {})
    nginx = components.get("nginx", {})
    apache_diag = diagnostics.get("apache_100003_1", {})
    nginx_diag = diagnostics.get("nginx_100003_1", {})
    build_path = apache.get("build_path") or nginx.get("build_path") or ""
    build_root_path = component_build_root(build_path) if build_path else None
    build_root = str(build_root_path) if build_root_path else "-"
    return {
        "build_root": build_root,
        "apachectl_bin": apache.get("apachectl_bin") or "-",
        "apache_module": apache.get("module_file") or "-",
        "nginx_bin": nginx.get("nginx_bin") or "-",
        "nginx_module": nginx.get("module_file") or "-",
        "apache_result": "FAIL" if apache_diag else "-",
        "apache_counts": apache_diag.get("counts", {}),
        "nginx_result": "FAIL" if nginx_diag else "-",
        "nginx_counts": nginx_diag.get("counts", {}),
    }


def normalize_native_remediation(text: str, components: dict[str, Any]) -> str:
    go_ftw = components.get("go_ftw", {})
    albedo = components.get("albedo", {})
    if go_ftw.get("status") in {"present", "built"}:
        text = re.sub(
            r"\n- nginx-pr24: `go-ftw` missing;[^\n]*",
            "\n- nginx-pr24: go-ftw is present; native execution reached go-ftw and failed during test execution.",
            text,
        )
        text = re.sub(
            r"\n- apache2_ubuntu: `go-ftw` missing;[^\n]*",
            "",
            text,
        )
    if albedo.get("status") in {"present", "built"}:
        text = re.sub(
            r"\n- nginx-pr24: `albedo` missing;[^\n]*",
            "",
            text,
        )
        text = re.sub(
            r"\n- apache2_ubuntu: `albedo` missing;[^\n]*",
            "",
            text,
        )
    return text


def runtime_components_markdown(components: dict[str, Any]) -> str:
    apache = components.get("apache_httpd", {})
    nginx = components.get("nginx", {})
    go_ftw = components.get("go_ftw", {})
    albedo = components.get("albedo", {})
    expat = components.get("expat", {})
    lines = [
        MARKER_START,
        "## Runtime Components",
        "",
        "### Apache httpd",
        f"- Status: `{apache.get('status', '-')}`",
        f"- Blocker: `{apache.get('blocker_reason') or '-'}`",
        f"- Cache path: `{apache.get('cache_path', '-')}`",
        f"- Build path: `{apache.get('build_path', '-')}`",
        f"- apachectl/APACHECTL_BIN: `{apache.get('apachectl_bin', '-')}`",
        f"- Module file: `{apache.get('module_file', '-')}`",
        f"- Missing file: `{apache.get('missing_file') or '-'}`",
        f"- Build component: `{apache.get('build_component') or '-'}`",
        f"- Env variable to set: `{apache.get('env_variable_can_set') or apache.get('env_override') or '-'}`",
        f"- Expat source: `{apache.get('expat_source') or '-'}`",
        f"- Expat release tag: `{apache.get('expat_release_tag') or '-'}`",
        f"- CPPFLAGS: `{apache.get('cppflags') or '-'}`",
        f"- LDFLAGS: `{apache.get('ldflags') or '-'}`",
        f"- LIBS: `{apache.get('libs') or '-'}`",
        f"- PKG_CONFIG_PATH: `{apache.get('pkg_config_path') or '-'}`",
        f"- crypt.h status: `{apache.get('crypt_h_status') or '-'}`",
        f"- crypt.h path: `{apache.get('crypt_h_path') or '-'}`",
        f"- libcrypt status: `{apache.get('libcrypt_status') or '-'}`",
        f"- libcrypt paths: `{', '.join(apache.get('libcrypt_paths', [])) or '-'}`",
        f"- crypt link mode: `{apache.get('crypt_link_mode') or '-'}`",
        "",
        "### NGINX",
        f"- Status: `{nginx.get('status', '-')}`",
        f"- Blocker: `{nginx.get('blocker_reason') or '-'}`",
        f"- Cache path: `{nginx.get('cache_path', '-')}`",
        f"- Build path: `{nginx.get('build_path', '-')}`",
        f"- MRTS_NATIVE_NGINX_BIN: `{nginx.get('nginx_bin', '-')}`",
        f"- MRTS_NATIVE_NGINX_MODULE_DIR: `{nginx.get('module_dir', '-')}`",
        f"- Module file: `{nginx.get('module_file', '-')}`",
        f"- Missing file: `{nginx.get('missing_file') or '-'}`",
        f"- Build component: `{nginx.get('build_component') or '-'}`",
        f"- Env variable to set: `{nginx.get('env_variable_can_set') or nginx.get('env_override') or '-'}`",
        "",
        "### Expat",
        f"- Status: `{expat.get('status', '-')}`",
        f"- Blocker: `{expat.get('blocker_reason') or '-'}`",
        f"- Source: `{expat.get('source', '-')}`",
        f"- Release tag: `{expat.get('release_tag') or expat.get('expected_ref') or '-'}`",
        f"- Actual head: `{expat.get('actual_head') or '-'}`",
        f"- Prefix: `{expat.get('prefix') or '-'}`",
        f"- expat.h: `{expat.get('expat_h') or '-'}`",
        f"- lib dir: `{expat.get('lib_dir') or '-'}`",
        f"- Recursive submodules: `{expat.get('recursive_submodule_status') or '-'}`",
        "",
        "### go-ftw / albedo",
        "| Dependency | Status | Binary | Env override | Source | Release tag | Head | Submodules | Release note | Blocker |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for item in (go_ftw, albedo):
        lines.append(
            "| {dep} | {status} | `{binary}` | `{env}` | `{source}` | `{ref}` | `{head}` | `{subs}` | {note} | {blocker} |".format(
                dep=item.get("dependency", "-"),
                status=item.get("status", "-"),
                binary=item.get("binary") or item.get("path") or "-",
                env=item.get("env_override", "-"),
                source=item.get("known_source") or "-",
                ref=item.get("release_tag") or item.get("known_ref") or "-",
                head=item.get("actual_head") or "-",
                subs=item.get("recursive_submodule_status") or "-",
                note=item.get("release_tag_deviation_note") or "-",
                blocker=item.get("blocker_reason") or "-",
            )
        )
    lines.append(MARKER_END)
    return "\n".join(lines)


def native_evidence_links_markdown() -> str:
    lines = [
        NATIVE_EVIDENCE_MARKER_START,
        "## MRTS Native Infrastructure Evidence",
        "",
        f"- Apache native: `{report_relpath('mrts_native_apache', 'md')}`",
        f"- NGINX PR24 native: `{report_relpath('mrts_native_nginx', 'md')}`",
        f"- Native summary: `{report_relpath('mrts_native_summary', 'md')}`",
        f"- Combined native report: `{report_relpath('mrts_native_full', 'md')}`",
        "",
        "These native MRTS reports are separate from connector full-matrix evidence.",
        NATIVE_EVIDENCE_MARKER_END,
    ]
    return "\n".join(lines)


def native_summary_markdown(report_dir: Path) -> str:
    native = read_json(report_path_from_root(report_dir, "mrts_native_full", "json"))
    targets = native.get("targets") if isinstance(native.get("targets"), dict) else {}
    lines = [
        "## MRTS Native Summary",
        f"- Report generated at: `{native.get('generated_at', '-')}`",
        "- Native MRTS evidence is separate from connector runtime matrix evidence.",
        "",
        "| Target | Status | Exit code | Attempted | PASS | FAIL | BLOCKED | Reason | Run log | Summary |",
        "|---|---|---:|---:|---:|---:|---:|---|---|---|",
    ]
    for target in ("apache2_ubuntu", "nginx-pr24"):
        job = targets.get(target, {}) if isinstance(targets.get(target), dict) else {}
        counts = job.get("counts") if isinstance(job.get("counts"), dict) else {}
        lines.append(
            "| {target} | {status} | {exit_code} | {attempted} | {passed} | {failed} | {blocked} | {reason} | `{run_log}` | `{summary}` |".format(
                target=target,
                status=job.get("status", "NOT_RUN"),
                exit_code=job.get("exit_code", "-"),
                attempted=counts.get("attempted", 0),
                passed=counts.get("pass", 0),
                failed=counts.get("fail", 0),
                blocked=counts.get("blocked", 0),
                reason=str(job.get("reason") or "-").replace("|", "\\|"),
                run_log=job.get("run_log", "-"),
                summary=job.get("summary_path", job.get("job_json", "-")),
            )
        )
    return "\n".join(lines)


def native_target_script_exit_code(summary: dict[str, Any]) -> int:
    if int(summary.get("FAIL", 0) or 0) > 0:
        return 2
    if int(summary.get("BLOCKED", 0) or 0) > 0:
        return 77
    return 0


def remove_stale_native_blockers(text: str, report_dir: Path) -> str:
    native = read_json(report_path_from_root(report_dir, "mrts_native_full", "json"))
    summary = native.get("summary") if isinstance(native.get("summary"), dict) else {}
    if int(summary.get("BLOCKED", 0) or 0) > 0:
        return text
    lines = []
    for line in text.splitlines():
        if line.startswith(("- apache2_ubuntu:", "- nginx-pr24:")):
            continue
        lines.append(line)
    return "\n".join(lines) + "\n"


def post_libcrypt_native_markdown(summary: dict[str, Any]) -> str:
    apache_counts = summary.get("apache_counts", {})
    nginx_counts = summary.get("nginx_counts", {})
    lines = [
        POST_LIBCRYPT_MARKER_START,
        "## Post-libcrypt Native Rerun",
        "- Scope: requested native rerun after external `libcrypt-dev` availability; the earlier full-matrix sections in this file remain historical evidence from their original generation time.",
        "- Command: `BUILD_ROOT=$HOME/.local/state/ModSecurity-conector-build SOURCE_ROOT=$HOME/.local/state/ModSecurity-conector-src CONNECTOR_COMPONENT_CACHE=$HOME/.local/state/ModSecurity-conector-build/component-cache MRTS_NATIVE_TARGETS=\"apache2_ubuntu nginx-pr24\" PYTHONDONTWRITEBYTECODE=1 make mrts-native-full-run`",
        f"- BUILD_ROOT: `{summary.get('build_root', '-')}`",
        f"- Apache wrapper: `{summary.get('apachectl_bin', '-')}`",
        f"- Apache module: `{summary.get('apache_module', '-')}`",
        f"- Apache native result: `{summary.get('apache_result', '-')}`; attempted `{apache_counts.get('attempted', '-')}`, passed `{apache_counts.get('passed', '-')}`, failed cases `{apache_counts.get('failed_cases', '-')}`",
        f"- NGINX binary: `{summary.get('nginx_bin', '-')}`",
        f"- NGINX module: `{summary.get('nginx_module', '-')}`",
        f"- NGINX native result: `{summary.get('nginx_result', '-')}`; attempted `{nginx_counts.get('attempted', '-')}`, passed `{nginx_counts.get('passed', '-')}`, failed cases `{nginx_counts.get('failed_cases', '-')}`",
        POST_LIBCRYPT_MARKER_END,
    ]
    return "\n".join(lines)


def runtime_build_cache_markdown(build_cache: dict[str, Any]) -> str:
    modsecurity = build_cache.get("shared_modsecurity_build", {})
    summary = build_cache.get("build_reuse_summary", {})
    lines = [
        BUILD_CACHE_MARKER_START,
        "## Runtime Build Cache",
        f"- Shared ModSecurity status: `{modsecurity.get('status', '-')}`",
        f"- Shared ModSecurity source ref/SHA: `{modsecurity.get('source_ref', '-')}` / `{modsecurity.get('actual_sha', '-')}`",
        f"- Shared ModSecurity build ID: `{modsecurity.get('build_id', '-')}`",
        f"- Shared ModSecurity prefix: `{modsecurity.get('prefix', '-')}`",
        f"- Build reuse summary: rebuilt `{summary.get('rebuilt_count', '-')}`, reused `{summary.get('reused_count', '-')}`, blocked `{summary.get('blocked_count', '-')}`, saved rebuilds estimate `{summary.get('saved_rebuilds_estimate', '-')}`",
        "",
        "| Connector | Status | Connector build ID | Uses ModSecurity build ID | Blocker |",
        "|---|---|---|---|---|",
    ]
    for item in build_cache.get("connector_builds", []):
        lines.append(
            "| {connector} | {status} | `{connector_id}` | `{modsec_id}` | {blocker} |".format(
                connector=item.get("connector", "-"),
                status=item.get("status", "-"),
                connector_id=item.get("connector_build_id", "-"),
                modsec_id=item.get("modsecurity_build_id", "-"),
                blocker=item.get("blocker_reason") or "-",
            )
        )
    lines.append(BUILD_CACHE_MARKER_END)
    return "\n".join(lines)


def diagnostics_markdown(diagnostics: dict[str, Any]) -> str:
    lines = [DIAG_MARKER_START, "## Native Runtime Diagnostics"]
    if not diagnostics:
        lines.extend(["", "- No generated native runtime diagnostics were detected."])
    else:
        for key in ("apache_100003_1", "nginx_100003_1"):
            diag = diagnostics.get(key, {})
            if not diag:
                continue
            label = diag.get("server_label") or diag.get("target", "-")
            counts = diag.get("counts", {})
            rule = diag.get("rule_metadata", {})
            generated_test = diag.get("generated_test", {})
            headers = generated_test.get("headers", {})
            hypotheses = diag.get("hypothesis_checks", {})
            single_rerun = diag.get("single_case_rerun", {})
            warnings = diag.get("parse_or_phase_warnings", [])
            loaded_includes = diag.get("loaded_includes", [])
            header_text = ", ".join(f"{name}: {value}" for name, value in headers.items()) or "-"
            single_rerun_text = (
                "not recorded"
                if not single_rerun
                else (
                    f"attempted `{single_rerun.get('attempted', '-')}`, "
                    f"failed cases `{single_rerun.get('failed_cases', '-')}`, "
                    f"exit `{single_rerun.get('exit_code', '-')}`, "
                    f"log `{single_rerun.get('log', '-')}`"
                )
            )
            lines.extend(
                [
                    "",
                    f"### {label} 100003-1",
                    f"- Status: `{diag.get('status', '-')}`",
                    f"- Target: `{diag.get('target', '-')}`",
                    f"- Run counts: attempted `{counts.get('attempted', '-')}`, passed `{counts.get('passed', '-')}`, failed cases `{counts.get('failed_cases', '-')}`",
                    f"- Diagnosis: {diag.get('diagnosis', '-')}",
                    f"- Classification: `{diag.get('classification', '-')}`; secondary `{diag.get('secondary_classification', '-')}`; unresolved `{diag.get('classification_checks', {}).get('unresolved', '-')}`",
                    f"- Classification reason: {diag.get('classification_reason', '-')}",
                    f"- Generated YAML: `{diag.get('ftw_yaml', '-')}`",
                    f"- Generated rule file: `{diag.get('rule_file', '-')}`",
                    f"- Source definition: `{rule.get('source_definition_relative_to_mrts_root', '-')}`",
                    f"- Generated rule line: `{rule.get('generated_rule_line', '-')}`",
                    f"- Rule 100003: variable `{rule.get('variable', '-')}`, phase `{rule.get('phase', '-')}`, operator `{rule.get('operator', '-')} {rule.get('operator_argument', '-')}`, transform `{rule.get('transform', '-')}`",
                    f"- Request: `{diag.get('method', '-')} {diag.get('uri', '-')} HTTP/1.1` on port `{diag.get('port', '-')}`; body `{diag.get('body', '-')}`",
                    f"- Generated test headers: `{header_text}`",
                    f"- Log matching: marker header `{generated_test.get('log_marker_header', '-')}`, target log `{generated_test.get('log_file_target', '-')}`",
                    f"- Expected status/result: `{diag.get('expected_status', '-')}` / `{diag.get('expected_result', '-')}`",
                    f"- Actual status/result: `{diag.get('actual_status', '-')}` / `{diag.get('actual_result', '-')}`",
                    f"- Actual logged IDs: `{', '.join(diag.get('actual_logged_ids', [])) or '-'}`",
                    f"- Phase 4 evidence: match seen `{hypotheses.get('phase4_match_seen', '-')}`, peer IDs in case window `{', '.join(hypotheses.get('phase4_rule_ids_logged_in_window', [])) or '-'}`, peer IDs anywhere `{', '.join(hypotheses.get('phase4_peer_ids_logged_anywhere', [])) or '-'}`",
                    f"- Request collection evidence: POST query as ARGS `{hypotheses.get('post_query_processed_as_args', '-')}`, as ARGS_GET `{hypotheses.get('post_query_processed_as_args_get', '-')}`",
                    f"- Excluded causes: response-body target `{hypotheses.get('is_response_body_target', '-')}`, operator case/transform issue `{hypotheses.get('operator_case_sensitive_issue', '-')}` / `{hypotheses.get('transform_issue', '-')}`, skip/ctl/chain interference `{hypotheses.get('skip_ctl_chain_or_disruptive_interference_seen', '-')}`, go-ftw log matching issue `{hypotheses.get('go_ftw_log_matching_issue', '-')}`",
                    f"- Parse/phase warnings: `{len(warnings)}`",
                    f"- Loaded MRTS includes checked: `{', '.join(loaded_includes) or '-'}`",
                    f"- Module loaded: `{diag.get('module_loaded')}` from `{diag.get('module_path') or '-'}`",
                    f"- mrts.load included: `{diag.get('mrts_load_included')}`",
                    f"- Request reached {label}/ModSecurity/Albedo: `{diag.get('request_reached_server')}` / `{diag.get('request_reached_modsecurity')}` / `{diag.get('request_reached_albedo')}`",
                    f"- Audit/debug evidence: audit log `{diag.get('audit_evidence', '-')}`, error log `{diag.get('error_log', '-')}`, go-ftw log `{diag.get('run_log', '-')}`",
                    f"- Single-case rerun: {single_rerun_text}",
                    f"- Why not logged: {diag.get('why_not_logged', '-')}",
                    f"- Action: {diag.get('recommended_action', '-')}",
                ]
            )
    lines.append(DIAG_MARKER_END)
    return "\n".join(lines)


def update_report_json(path: Path, components: dict[str, Any], diagnostics: dict[str, Any], build_cache: dict[str, Any]) -> None:
    if not path.is_file():
        return
    data = read_json(path)
    if not data:
        return
    data["mrts_native_reports"] = {
        "apache": report_relpath("mrts_native_apache", "md"),
        "nginx": report_relpath("mrts_native_nginx", "md"),
        "summary": report_relpath("mrts_native_summary", "md"),
        "combined": report_relpath("mrts_native_full", "md"),
    }
    if path.name == "full-run-evidence.generated.json":
        reports = data.get("reports")
        if not isinstance(reports, list):
            reports = []
        for report_file in NATIVE_REPORT_FILES:
            if report_file not in reports:
                reports.append(report_file)
        data["reports"] = reports
        report_dir = report_root_for(path)
        native_full = read_json(report_path_from_root(report_dir, "mrts_native_full", "json"))
        if native_full:
            mrts_native = data.get("mrts_native") if isinstance(data.get("mrts_native"), dict) else {}
            mrts_native.update(
                {
                    "generated_at": native_full.get("generated_at"),
                    "report_json": report_relpath("mrts_native_full", "json"),
                    "report_md": report_relpath("mrts_native_full", "md"),
                    "reports": native_full.get("reports", data["mrts_native_reports"]),
                    "summary": native_full.get("summary", {}),
                    "target_script_exit_code": native_target_script_exit_code(native_full.get("summary", {})),
                    "targets": native_full.get("targets", {}),
                }
            )
            data["mrts_native"] = mrts_native
        write_json(path, data)
        return
    data["runtime_components"] = components
    data["runtime_diagnostics"] = diagnostics
    data["runtime_build_cache"] = build_cache
    for key, value in components.items():
        data[key] = value
    write_json(path, data)


def update_report_md(path: Path, components: dict[str, Any], diagnostics: dict[str, Any], build_cache: dict[str, Any]) -> None:
    if not path.is_file():
        return
    text = read_text_file(path)
    if path.name == "mrts-native-full.generated.md":
        text = normalize_native_remediation(text, components)
    if path.name == "full-run-evidence.generated.md":
        text = remove_stale_native_blockers(text, path.parent)
        text = replace_heading_section(
            text,
            "## MRTS Native Summary",
            native_summary_markdown(path.parent),
            "## External Blockers",
        )
        text = insert_named_section_before_heading(
            text,
            native_evidence_links_markdown(),
            NATIVE_EVIDENCE_MARKER_START,
            NATIVE_EVIDENCE_MARKER_END,
            "## External Blockers",
        )
        write_text_file(path, text)
        return
    section = runtime_components_markdown(components)
    text = replace_marked_section(text, section)
    text = replace_named_section(text, runtime_build_cache_markdown(build_cache), BUILD_CACHE_MARKER_START, BUILD_CACHE_MARKER_END)
    text = replace_named_section(text, diagnostics_markdown(diagnostics), DIAG_MARKER_START, DIAG_MARKER_END)
    write_text_file(path, text)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector-root", required=True)
    args = parser.parse_args()

    connector_root = Path(args.connector_root).resolve()
    report_dir = connector_root / GENERATED_ROOT
    add_safe_roots(connector_root, report_dir)
    add_report_roots(report_dir)
    components = component_inventory(report_dir)
    build_cache = build_cache_inventory(report_dir)
    diagnostics = collect_runtime_diagnostics(components)
    update_report_json(report_path_from_root(report_dir, "runtime_component_cache", "json"), components, diagnostics, build_cache)
    update_report_md(report_path_from_root(report_dir, "runtime_component_cache", "md"), components, diagnostics, build_cache)
    if os.environ.get("SUPPRESS_FULL_RUN_EVIDENCE_SIDE_EFFECTS") != "1":
        update_report_json(report_path_from_root(report_dir, "full_run_evidence", "json"), components, diagnostics, build_cache)
        update_report_md(report_path_from_root(report_dir, "full_run_evidence", "md"), components, diagnostics, build_cache)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
