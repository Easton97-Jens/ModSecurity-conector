#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover - report generation has a conservative fallback.
    yaml = None


REPORT_DIR = Path("reports/testing/generated")
TARGET_CATEGORIES = {"request_body_processor", "multipart_files", "xml_processor"}
SELECTED_CONNECTOR_GAP_CASE = "phase1_vs_phase2_request_body_gap"
URLENCODED_FORM_CONTENT_TYPE = "application/x-www-form-urlencoded"
URLENCODED_FORM_CLASSIFICATION = "with_mrts_detection_only_non_disruptive"
ABSOLUTE_RUNTIME_PATH_RE = re.compile(r"(?<![\w.-])/(?:tmp|root|src)[^\s\"']*")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def read_text(path: Path | None) -> str:
    if not path:
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sanitize_report_text(value: Any) -> str:
    return ABSOLUTE_RUNTIME_PATH_RE.sub("<evidence-path>", str(value or ""))


def normalized_content_type(value: Any) -> str:
    return str(value or "").split(";", 1)[0].strip().lower()


def as_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if value in (None, ""):
        return []
    return [str(value)]


def import_script(path: Path, module_name: str) -> Any:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def display_case_path(path_value: Any, framework_root: Path) -> str:
    path = Path(str(path_value or ""))
    try:
        return "framework:" + str(path.resolve(strict=False).relative_to(framework_root.resolve(strict=False)))
    except ValueError:
        return sanitize_report_text(path.name or "-")


def generated_config_path(entry: dict[str, Any], evidence_path: Path) -> Path | None:
    case_id = str(entry.get("case_id") or evidence_path.parent.name)
    connector = str(entry.get("connector") or "")
    if connector == "nginx":
        return evidence_path.parent.parent.parent / "runtime" / case_id / "conf/modsecurity-smoke.conf"
    if connector == "apache":
        return evidence_path.parent.parent.parent.parent / "apache-runtime" / case_id / "conf/modsecurity-smoke.conf"
    if connector == "haproxy":
        return evidence_path.parent.parent.parent.parent / "haproxy-runtime-cases" / case_id / "conf/modsecurity-smoke.conf"
    return None


def action_parts(action_text: str) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    quote: str | None = None
    for char in action_text:
        if char in {"'", '"'}:
            quote = None if quote == char else char if quote is None else quote
        if char == "," and quote is None:
            part = "".join(current).strip()
            if part:
                parts.append(part)
            current = []
            continue
        current.append(char)
    tail = "".join(current).strip()
    if tail:
        parts.append(tail)
    return parts


def parse_rules(rules: str) -> list[dict[str, Any]]:
    parsed: list[dict[str, Any]] = []
    rule_re = re.compile(
        r"\b(SecRule|SecAction)\b\s+"
        r"(?:(?P<target>[^\s\"]+)\s+\"(?P<operator>[^\"]*)\"\s+)?"
        r"(?:\\\s*)?\"(?P<actions>[^\"]+)\"",
        re.DOTALL,
    )
    for match in rule_re.finditer(rules):
        actions = action_parts(re.sub(r"\s+", " ", match.group("actions")).strip())
        action_text = ",".join(actions)
        rule_id = "-"
        id_match = re.search(r"\bid\s*:?\s*(\d+)", action_text, re.IGNORECASE)
        if id_match:
            rule_id = id_match.group(1)
        phase = "-"
        phase_match = re.search(r"\bphase\s*:?\s*(\d+)", action_text, re.IGNORECASE)
        if phase_match:
            phase = phase_match.group(1)
        parsed.append(
            {
                "rule_id": rule_id,
                "phase": phase,
                "target": match.group("target") or "-",
                "operator": match.group("operator") or "-",
                "actions": actions,
                "transformations": [action.split(":", 1)[1] for action in actions if action.lower().startswith("t:")],
            }
        )
    return parsed


def select_rule(rules: list[dict[str, Any]], expected_rule_id: Any) -> dict[str, Any]:
    expected = str(expected_rule_id or "")
    if expected:
        for rule in rules:
            if rule["rule_id"] == expected:
                return rule
    for rule in reversed(rules):
        if rule["rule_id"] != "-":
            return rule
    return {"rule_id": "-", "phase": "-", "target": "-", "operator": "-", "actions": [], "transformations": []}


def body_kind(request: dict[str, Any], content_type: str) -> str:
    body = str(request.get("body") or "")
    if isinstance(request.get("multipart"), dict):
        return "multipart"
    if not body:
        return "empty"
    lowered = content_type.lower()
    if "multipart/form-data" in lowered:
        return "multipart"
    if "json" in lowered:
        return "json"
    if "xml" in lowered:
        return "xml"
    if "x-www-form-urlencoded" in lowered:
        return "form"
    return "raw"


def log_paths(evidence: dict[str, Any]) -> list[Path]:
    paths: list[Path] = []
    for key, value in evidence.items():
        if not value:
            continue
        if key.endswith("_log_path") or key in {
            "audit_log_path",
            "decision_log",
            "decision_log_path",
            "spoa_log_path",
            "haproxy_log_path",
        }:
            paths.append(Path(str(value)))
    return paths


def rule_logged(logs: str, rule_id: str) -> bool:
    if not rule_id or rule_id == "-":
        return False
    return bool(
        re.search(r'\[id "' + re.escape(rule_id) + r'"\]', logs)
        or re.search(r'"rule_id"\s*:\s*"?' + re.escape(rule_id) + r'"?', logs)
    )


def request_body_seen(logs: str) -> str:
    seen = False
    any_decision = False
    for line in logs.splitlines():
        if not line.startswith("{"):
            continue
        try:
            loaded = json.loads(line)
        except Exception:
            continue
        if isinstance(loaded, dict) and "request_body_seen" in loaded:
            any_decision = True
            seen = seen or loaded.get("request_body_seen") is True
    if seen:
        return "yes"
    return "no" if any_decision else "unknown"


def generated_body_length(config_path: Path | None, request: dict[str, Any]) -> int:
    if config_path:
        request_body = config_path.parent / "request-body.bin"
        if request_body.is_file():
            return len(read_text(request_body).encode())
    if isinstance(request.get("multipart"), dict):
        return -1
    return len(str(request.get("body") or "").encode())


def case_metadata(entry: dict[str, Any], evidence: dict[str, Any], framework_root: Path) -> dict[str, Any]:
    case_path = Path(str(evidence.get("path") or ""))
    raw = read_text(case_path) if case_path.is_file() else ""
    loaded: dict[str, Any] = {}
    if raw and yaml is not None:
        try:
            parsed = yaml.safe_load(raw)
            loaded = parsed if isinstance(parsed, dict) else {}
        except Exception:
            loaded = {}
    request = loaded.get("request") if isinstance(loaded.get("request"), dict) else {}
    headers = request.get("headers") if isinstance(request.get("headers"), dict) else {}
    content_type = str(headers.get("Content-Type") or headers.get("content-type") or "-")
    request_path = str(request.get("path") or "-")
    path = request_path
    query = "-"
    if "?" in request_path:
        path, query = request_path.split("?", 1)
        path = path or "/"
    expect = loaded.get("expect") if isinstance(loaded.get("expect"), dict) else {}
    rules = parse_rules(str(loaded.get("rules") or raw))
    rule = select_rule(rules, expect.get("rule_id"))
    config_path = generated_config_path(entry, Path(str(entry.get("evidence") or "")))
    config = read_text(config_path)
    logs = "\n".join(read_text(path_item) for path_item in log_paths(evidence))
    request_body_access = "yes" if "SecRequestBodyAccess On" in config else "no" if "SecRequestBodyAccess Off" in config else "unknown"
    xml_processor = "yes" if "ctl:requestBodyProcessor=XML" in config else "unknown"
    rule_id = str(rule["rule_id"])
    matched = rule_logged(logs, rule_id)
    return {
        "case_path": display_case_path(case_path, framework_root),
        "method": str(request.get("method") or "-"),
        "path": path,
        "query": query,
        "content_type": content_type,
        "body_kind": body_kind(request, content_type),
        "body_length": generated_body_length(config_path, request),
        "rule_id": rule_id,
        "phase": str(rule["phase"] if rule["phase"] != "-" else entry.get("phase") or "-"),
        "target": str(rule["target"] or "-"),
        "operator": str(rule["operator"] or "-"),
        "transformations": rule["transformations"],
        "actions": rule["actions"],
        "rule_in_loadfile": bool(rule_id != "-" and rule_id in config),
        "request_body_access": request_body_access,
        "xml_processor": xml_processor,
        "request_body_seen": request_body_seen(logs),
        "rule_matched": matched,
        "collection_evidence": "yes" if matched else "no",
        "parse_error": bool(re.search(r"parse|parser|multipart|xml|json", logs, re.IGNORECASE)) and "Warning. Matched" not in logs,
        "backend_reached": entry.get("actual_status") == 200,
        "known_limitations": as_list(loaded.get("known_limitations")),
    }


def build_records(
    connector_root: Path, framework_root: Path
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    remaining = import_script(connector_root / "ci/generate-remaining-failure-analysis.py", "remaining_failure_analysis")
    queue = read_json(connector_root / REPORT_DIR / "connector-work-queue.generated.json")
    entries = [entry for entry in queue.get("entries", []) if isinstance(entry, dict) and entry.get("runtime_status") == "FAIL"]
    target_records: list[dict[str, Any]] = []
    selected_gap_records: list[dict[str, Any]] = []
    urlencoded_form_records: list[dict[str, Any]] = []
    for entry in entries:
        category = remaining.failure_category(entry)
        is_selected_gap = entry.get("case_id") == SELECTED_CONNECTOR_GAP_CASE
        is_candidate_urlencoded = entry.get("classification") == URLENCODED_FORM_CLASSIFICATION
        if category not in TARGET_CATEGORIES and not is_selected_gap and not is_candidate_urlencoded:
            continue
        evidence = read_json(Path(str(entry.get("evidence") or "")))
        meta = case_metadata(entry, evidence, framework_root)
        record = {
            "case_id": entry.get("case_id"),
            "connector": entry.get("connector"),
            "variant": f"{entry.get('test_variant')}/{entry.get('mrts_variant')}",
            "test_variant": entry.get("test_variant"),
            "mrts_variant": entry.get("mrts_variant"),
            "failure_category": category,
            "queue_category": entry.get("category"),
            "classification": entry.get("classification"),
            "priority": entry.get("priority"),
            "functional_area": as_list(entry.get("functional_area")),
            "source_kind": entry.get("source_kind"),
            "source_corpus": entry.get("mrts_corpus"),
            "expected_status": entry.get("expected_status"),
            "actual_status": entry.get("actual_status"),
            "failure_pattern": as_list(entry.get("failure_pattern")),
            "work_direction": as_list(entry.get("work_direction")),
            **meta,
        }
        if is_urlencoded_form_detection_only(record):
            urlencoded_form_records.append(record)
        if is_selected_gap:
            selected_gap_records.append(record)
        elif category in TARGET_CATEGORIES:
            target_records.append(record)
    return target_records, selected_gap_records, urlencoded_form_records


def is_urlencoded_form_detection_only(record: dict[str, Any]) -> bool:
    return (
        record.get("classification") == URLENCODED_FORM_CLASSIFICATION
        and record.get("mrts_variant") == "with-mrts"
        and record.get("body_kind") == "form"
        and normalized_content_type(record.get("content_type")) == URLENCODED_FORM_CONTENT_TYPE
    )


def count_records(records: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    counter = Counter(str(record.get(key) or "-") for record in records)
    return [{"value": value, "count": count} for value, count in counter.most_common()]


def grouped_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        grouped[
            (
                str(record["connector"]),
                str(record["body_kind"]),
                str(record["content_type"]),
                str(record["phase"]),
                str(record["target"]),
                f"{record['expected_status']}->{record['actual_status']}",
                str(record["failure_category"]),
                str(record["source_kind"]),
            )
        ].append(record)
    rows: list[dict[str, Any]] = []
    for key, items in grouped.items():
        example = items[0]
        rows.append(
            {
                "count": len(items),
                "connector": key[0],
                "body_kind": key[1],
                "content_type": key[2],
                "phase": key[3],
                "target": key[4],
                "status_pair": key[5],
                "failure_category": key[6],
                "source_kind": key[7],
                "variants": sorted({str(item["variant"]) for item in items}),
                "example_cases": sorted({str(item["case_id"]) for item in items})[:6],
                "request_body_access": sorted({str(item["request_body_access"]) for item in items}),
                "rule_matched_count": sum(1 for item in items if item["rule_matched"]),
                "collection_evidence_count": sum(1 for item in items if item["collection_evidence"] == "yes"),
                "body_seen": sorted({str(item["request_body_seen"]) for item in items}),
                "suspected_cause": suspected_cause(example, items),
                "risk": risk_for(example),
                "fixability": fixability_for(example),
            }
        )
    return sorted(rows, key=lambda item: (-item["count"], item["failure_category"], item["connector"], item["target"]))


def counter_dict(records: list[dict[str, Any]], key: str) -> dict[str, int]:
    return dict(Counter(str(record.get(key) or "-") for record in records).most_common())


def summarize_urlencoded_form(records: list[dict[str, Any]]) -> dict[str, Any]:
    body_sent = sum(1 for record in records if int(record.get("body_length") or 0) > 0)
    content_type_correct = sum(
        1 for record in records if normalized_content_type(record.get("content_type")) == URLENCODED_FORM_CONTENT_TYPE
    )
    return {
        "count": len(records),
        "active_request_body_processor_before_report_sync": len(records),
        "active_request_body_processor_after_report_sync": 0,
        "classification": URLENCODED_FORM_CLASSIFICATION,
        "work_direction": "classification_only",
        "priority": "report_only",
        "connectors": counter_dict(records, "connector"),
        "variants": counter_dict(records, "variant"),
        "case_ids": counter_dict(records, "case_id"),
        "rule_ids": counter_dict(records, "rule_id"),
        "targets": counter_dict(records, "target"),
        "operators": counter_dict(records, "operator"),
        "methods": counter_dict(records, "method"),
        "content_types": counter_dict(records, "content_type"),
        "body_kinds": counter_dict(records, "body_kind"),
        "body_lengths": counter_dict(records, "body_length"),
        "request_body_seen": counter_dict(records, "request_body_seen"),
        "body_sent_count": body_sent,
        "content_type_correct_count": content_type_correct,
        "request_body_access_on_count": sum(1 for record in records if record["request_body_access"] == "yes"),
        "rule_loaded_count": sum(1 for record in records if record["rule_in_loadfile"]),
        "rule_matched_count": sum(1 for record in records if record["rule_matched"]),
        "collection_evidence_count": sum(1 for record in records if record["collection_evidence"] == "yes"),
        "backend_reached_count": sum(1 for record in records if record["backend_reached"]),
        "root_cause": "The URL-encoded bodies and Content-Type are present; these rows are with-MRTS DetectionOnly overlay cases, so disruptive actions remain non-blocking and belong to report-only classification.",
        "fix": "metadata/report-only; no request body, Content-Type, rule, Expected status, or PASS/FAIL value changed",
        "risk": "low when kept out of active request_body_processor work; high if promoted to PASS without disruptive runtime evidence",
        "examples": records[:9],
    }


def suspected_cause(example: dict[str, Any], items: list[dict[str, Any]]) -> str:
    if example["failure_category"] == "request_body_processor" and example["body_kind"] == "json":
        return "JSON/raw REQUEST_BODY rows need processor-specific semantics review; with-MRTS rows may be non-blocking due DetectionOnly overlay."
    if example["failure_category"] == "request_body_processor" and example["body_kind"] == "form":
        return "URL-encoded body variables are present in selected rows, but with-MRTS overlay suppresses disruption."
    if example["failure_category"] == "xml_processor":
        return "XML target population is absent for future/gap rows or non-disruptive under with-MRTS DetectionOnly; XML processor parity needs targeted review."
    if example["failure_category"] == "multipart_files":
        return "Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence."
    if example["case_id"] == SELECTED_CONNECTOR_GAP_CASE:
        return "The YAML request body is empty while a phase:1 REQUEST_BODY rule expects bodyhit; existing metadata marks it as connector-gap."
    return "manual review"


def risk_for(example: dict[str, Any]) -> str:
    if example["case_id"] == SELECTED_CONNECTOR_GAP_CASE:
        return "low for classification-only"
    if example["failure_category"] == "xml_processor":
        return "medium to high"
    return "medium"


def fixability_for(example: dict[str, Any]) -> str:
    if example["case_id"] == SELECTED_CONNECTOR_GAP_CASE:
        return "metadata-only; do not change request body, rule, or expected status"
    if example["mrts_variant"] == "with-mrts" and example["rule_matched"]:
        return "classification/report-only unless MRTS DetectionOnly policy changes"
    return "requires targeted native/connector comparison before code changes"


def build_report(connector_root: Path, framework_root: Path) -> dict[str, Any]:
    records, selected_gap_records, urlencoded_form_records = build_records(connector_root, framework_root)
    category_counts = Counter(record["failure_category"] for record in records)
    selected_count = len(selected_gap_records)
    urlencoded_form_summary = summarize_urlencoded_form(urlencoded_form_records)
    summary = {
        "before_metadata_fix": {
            "request_body_processor": category_counts.get("request_body_processor", 0) + selected_count,
            "multipart_files": category_counts.get("multipart_files", 0),
            "xml_processor": category_counts.get("xml_processor", 0),
            "combined": len(records) + selected_count,
        },
        "after_metadata_fix": {
            "request_body_processor": category_counts.get("request_body_processor", 0),
            "multipart_files": category_counts.get("multipart_files", 0),
            "xml_processor": category_counts.get("xml_processor", 0),
            "combined": len(records),
        },
        "selected_subcluster_count": selected_count,
        "urlencoded_form_subcluster_count": urlencoded_form_summary["count"],
        "urlencoded_form_active_after_report_sync": urlencoded_form_summary["active_request_body_processor_after_report_sync"],
        "rule_loaded": sum(1 for record in records + selected_gap_records if record["rule_in_loadfile"]),
        "rule_matched": sum(1 for record in records + selected_gap_records if record["rule_matched"]),
        "backend_reached": sum(1 for record in records + selected_gap_records if record["backend_reached"]),
        "request_body_access_on": sum(1 for record in records + selected_gap_records if record["request_body_access"] == "yes"),
        "collection_evidence": sum(1 for record in records + selected_gap_records if record["collection_evidence"] == "yes"),
    }
    plan = read_json(connector_root / REPORT_DIR / "next-fix-plan.generated.json")
    recommendation = plan.get("recommendation") if isinstance(plan.get("recommendation"), dict) else {}
    return {
        "report_kind": "body-processor-analysis",
        "generated_at": utc_now(),
        "source_reports": {
            "connector_work_queue": "reports/testing/generated/connector-work-queue.generated.json",
            "remaining_failure_analysis": "reports/testing/generated/remaining-failure-analysis.generated.json",
            "phase_work_queue": "reports/testing/generated/phase-work-queue.generated.json",
            "next_fix_plan": "reports/testing/generated/next-fix-plan.generated.json",
        },
        "summary": summary,
        "distribution": {
            "connectors": count_records(records, "connector"),
            "variants": count_records(records, "variant"),
            "body_kinds": count_records(records, "body_kind"),
            "content_types": count_records(records, "content_type"),
            "targets": count_records(records, "target"),
            "failure_categories": count_records(records, "failure_category"),
        },
        "selected_subcluster": {
            "case_id": SELECTED_CONNECTOR_GAP_CASE,
            "count": selected_count,
            "action": "metadata-only classification: request_body_processor -> connector_gap",
            "why_safe": "the case has an empty request body and existing source metadata says connector-gap; no request, rule, expected status, or PASS/FAIL value changed",
            "root_cause": "phase:1 REQUEST_BODY cannot match the expected bodyhit because the YAML request body is empty",
            "body_arrived": "empty by fixture",
            "processor_active": "not relevant for the selected metadata-only classification",
            "collections_created": "no target rule match evidence",
            "examples": selected_gap_records[:9],
        },
        "urlencoded_form_subcluster": urlencoded_form_summary,
        "groups": grouped_records(records),
        "records": records,
        "next_fix_plan": {
            "recommended_next_fix_cluster": recommendation.get("recommended_next_fix_cluster", "-"),
            "reason": recommendation.get("reason", "-"),
        },
    }


def md_bool(value: Any) -> str:
    return "yes" if bool(value) else "no"


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    before = summary["before_metadata_fix"]
    after = summary["after_metadata_fix"]
    urlencoded = report["urlencoded_form_subcluster"]
    lines = [
        "# Body Processor Failure Analysis",
        "",
        f"- Generated at: `{report['generated_at']}`",
        f"- Before selected metadata fix: request_body_processor **{before['request_body_processor']}**, multipart_files **{before['multipart_files']}**, xml_processor **{before['xml_processor']}**, combined **{before['combined']}**.",
        f"- After selected metadata fix: request_body_processor **{after['request_body_processor']}**, multipart_files **{after['multipart_files']}**, xml_processor **{after['xml_processor']}**, combined **{after['combined']}**.",
        f"- Selected subcluster rows: **{summary['selected_subcluster_count']}**",
        f"- URL-encoded form rows moved out of active body-processor work: **{summary['urlencoded_form_subcluster_count']}** -> **{summary['urlencoded_form_active_after_report_sync']}**.",
        f"- Rule loaded evidence rows: **{summary['rule_loaded']}**",
        f"- Target rule matched rows: **{summary['rule_matched']}**",
        f"- Backend reached rows: **{summary['backend_reached']}**",
        f"- Request body access explicitly on: **{summary['request_body_access_on']}**",
        f"- Collection/target evidence rows: **{summary['collection_evidence']}**",
        "",
        "## Selected Subcluster",
        "",
        f"- Case: `{report['selected_subcluster']['case_id']}`",
        f"- Count: **{report['selected_subcluster']['count']}**",
        f"- Action: {report['selected_subcluster']['action']}",
        f"- Why safe: {report['selected_subcluster']['why_safe']}",
        f"- Root cause: {report['selected_subcluster']['root_cause']}",
        f"- Body arrived: {report['selected_subcluster']['body_arrived']}",
        f"- Processor active: {report['selected_subcluster']['processor_active']}",
        f"- Collections created: {report['selected_subcluster']['collections_created']}",
        "",
        "## URL-encoded Form Subcluster",
        "",
        f"- Count: **{urlencoded['count']}**",
        f"- Active request_body_processor rows before report sync: **{urlencoded['active_request_body_processor_before_report_sync']}**",
        f"- Active request_body_processor rows after report sync: **{urlencoded['active_request_body_processor_after_report_sync']}**",
        f"- Classification: `{urlencoded['classification']}`",
        f"- Work direction: `{urlencoded['work_direction']}`",
        f"- Priority: `{urlencoded['priority']}`",
        f"- Body sent rows: **{urlencoded['body_sent_count']}**",
        f"- Correct Content-Type rows: **{urlencoded['content_type_correct_count']}**",
        f"- SecRequestBodyAccess On rows: **{urlencoded['request_body_access_on_count']}**",
        f"- Rule loaded rows: **{urlencoded['rule_loaded_count']}**",
        f"- Rule matched rows: **{urlencoded['rule_matched_count']}**",
        f"- Collection/target evidence rows: **{urlencoded['collection_evidence_count']}**",
        f"- Backend reached rows: **{urlencoded['backend_reached_count']}**",
        f"- Root cause: {urlencoded['root_cause']}",
        f"- Fix: {urlencoded['fix']}",
        f"- Risk: {urlencoded['risk']}",
        "",
        "| field | distribution |",
        "| --- | --- |",
    ]
    for key in ("connectors", "variants", "case_ids", "rule_ids", "targets", "operators", "body_lengths", "request_body_seen"):
        values = ", ".join(f"`{sanitize_report_text(name)}`: {count}" for name, count in urlencoded[key].items()) or "-"
        lines.append(f"| {key} | {values} |")
    lines.extend(
        [
            "",
            "## Distributions",
            "",
        ]
    )
    for title, key in (
        ("Connectors", "connectors"),
        ("Variants", "variants"),
        ("Body Kinds", "body_kinds"),
        ("Content Types", "content_types"),
        ("Targets", "targets"),
        ("Failure Categories", "failure_categories"),
    ):
        lines.append(f"### {title}")
        lines.append("")
        lines.append("| value | count |")
        lines.append("| --- | ---: |")
        for item in report["distribution"][key]:
            lines.append(f"| `{sanitize_report_text(item['value'])}` | {item['count']} |")
        lines.append("")
    lines.extend(
        [
            "## Grouped Rows",
            "",
            "| count | connector | body kind | content-type | phase | target | status | category | variants | matched | cause | fixability |",
            "| ---: | --- | --- | --- | --- | --- | --- | --- | --- | ---: | --- | --- |",
        ]
    )
    for group in report["groups"]:
        lines.append(
            "| {count} | {connector} | {body_kind} | `{content_type}` | {phase} | `{target}` | {status_pair} | {category} | {variants} | {matched} | {cause} | {fixability} |".format(
                count=group["count"],
                connector=group["connector"],
                body_kind=group["body_kind"],
                content_type=sanitize_report_text(group["content_type"]),
                phase=group["phase"],
                target=sanitize_report_text(group["target"]),
                status_pair=group["status_pair"],
                category=group["failure_category"],
                variants=", ".join(group["variants"]),
                matched=group["rule_matched_count"],
                cause=sanitize_report_text(group["suspected_cause"]),
                fixability=sanitize_report_text(group["fixability"]),
            )
        )
    lines.extend(
        [
            "",
            "## Current Next Fix Plan",
            "",
            f"- Recommended next cluster: `{report['next_fix_plan']['recommended_next_fix_cluster']}`",
            f"- Reason: {sanitize_report_text(report['next_fix_plan']['reason'])}",
            "",
            "## Guardrail Notes",
            "",
            "- No Expected statuses, testcase rules, request bodies, MRTS definitions, or PASS/FAIL values are changed by this analysis.",
            "- The selected subcluster is metadata-only and remains a runtime FAIL; it is no longer counted as body-processor work.",
            "- URL-encoded/form rows are report-only with-MRTS DetectionOnly overlay evidence; no harness or connector-core change is made for them.",
            "- Remaining Body/XML/Multipart rows need narrower connector/native comparisons before connector-core changes.",
            "",
        ]
    )
    return "\n".join(lines)


def replace_marked_section(text: str, start: str, end: str, section: str) -> str:
    block = f"{start}\n{section}\n{end}"
    if start in text and end in text:
        pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
        return pattern.sub(block, text)
    return text.rstrip() + "\n\n" + block + "\n"


def update_full_run_evidence(report_dir: Path, report: dict[str, Any]) -> None:
    json_path = report_dir / "full-run-evidence.generated.json"
    data = read_json(json_path)
    if data:
        data["body_processor_analysis_report"] = {
            "analysis": "reports/testing/generated/body-processor-analysis.generated.md",
            "json": "reports/testing/generated/body-processor-analysis.generated.json",
            "urlencoded_form_subcluster_count": report["summary"]["urlencoded_form_subcluster_count"],
            "active_after_report_sync": report["summary"]["urlencoded_form_active_after_report_sync"],
        }
        reports = data.get("reports")
        if isinstance(reports, list):
            for item in (
                "reports/testing/generated/body-processor-analysis.generated.json",
                "reports/testing/generated/body-processor-analysis.generated.md",
            ):
                if item not in reports:
                    reports.append(item)
            data["reports"] = reports
        write_json(json_path, data)

    md_path = report_dir / "full-run-evidence.generated.md"
    text = read_text(md_path)
    if text:
        section = "\n".join(
            [
                "## Body Processor Analysis",
                "- Body processor analysis: `reports/testing/generated/body-processor-analysis.generated.md`",
                f"- URL-encoded/form rows: **{report['summary']['urlencoded_form_subcluster_count']}** -> **{report['summary']['urlencoded_form_active_after_report_sync']}** active request_body_processor rows after report sync.",
                "- The URL-encoded rows have body and Content-Type evidence and are kept as report-only with-MRTS DetectionOnly overlay cases.",
            ]
        )
        updated = replace_marked_section(
            text,
            "<!-- body-processor-analysis:start -->",
            "<!-- body-processor-analysis:end -->",
            section,
        )
        md_path.write_text(updated, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector-root", type=Path, default=Path.cwd())
    parser.add_argument("--framework-root", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    connector_root = args.connector_root.resolve()
    framework_root = (args.framework_root or connector_root / "modules/ModSecurity-test-Framework").resolve()
    output_dir = (args.output_dir or connector_root / REPORT_DIR).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    report = build_report(connector_root, framework_root)
    write_json(output_dir / "body-processor-analysis.generated.json", report)
    (output_dir / "body-processor-analysis.generated.md").write_text(render_markdown(report), encoding="utf-8")
    update_full_run_evidence(output_dir, report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
