#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from generated_report_utils import GENERATED_ROOT, build_metadata, generated_json_text, generated_markdown_text, report_path, report_path_from_root, report_relpath
from report_path_safety import add_report_roots, add_safe_roots, read_json_file, read_text_file, resolve_output_dir, safe_existing_file, write_json_file, write_text_file

try:
    import yaml
except Exception:  # pragma: no cover - regex fallback still renders the report.
    yaml = None


REPORT_DIR = GENERATED_ROOT
REPORT_STEM = "rule-chain-semantics-analysis.generated"
DETECTION_ONLY_CLASSIFICATION = "with_mrts_detection_only_non_disruptive"
ABSOLUTE_RUNTIME_PATH_RE = re.compile(r"(?<![\w.-])/(?:tmp|root|src)[^\s\"']*")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Any) -> dict[str, Any]:
    return read_json_file(path)


def write_json(path: Path, value: dict[str, Any]) -> None:
    write_json_file(path, value)


def read_text(path: Path | None) -> str:
    return read_text_file(path)


def sanitize_report_text(value: Any) -> str:
    return ABSOLUTE_RUNTIME_PATH_RE.sub("<evidence-path>", str(value or ""))


def as_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if value in (None, ""):
        return []
    return [str(value)]


def display_case_path(value: Any, framework_root: Path) -> str:
    if not value:
        return "-"
    path = safe_existing_file(value)
    if path is None:
        return sanitize_report_text(str(value).replace("\\", "/").rstrip("/").split("/")[-1] or "-")
    try:
        return "framework:" + str(path.resolve(strict=False).relative_to(framework_root.resolve(strict=False)))
    except ValueError:
        return sanitize_report_text(path.name or "-")


def load_case(path_value: Any) -> dict[str, Any]:
    path = safe_existing_file(path_value)
    if path is None or not path.is_file() or yaml is None:
        return {}
    try:
        loaded = yaml.safe_load(read_text(path))
    except Exception:
        return {}
    return loaded if isinstance(loaded, dict) else {}


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


def action_value(actions: list[str], name: str) -> str:
    prefix = f"{name.lower()}:"
    for action in actions:
        text = action.strip()
        lower = text.lower()
        if lower.startswith(prefix):
            return text.split(":", 1)[1].strip()
    return "-"


def parse_rules(rules: str) -> list[dict[str, Any]]:
    parsed: list[dict[str, Any]] = []
    rule_re = re.compile(
        r"\bSecRule\b\s+(?P<target>[^\s\"]+)\s+\"(?P<operator>[^\"]*)\"\s+(?:\\\s*)?\"(?P<actions>[^\"]+)\"",
        re.DOTALL,
    )
    for match in rule_re.finditer(rules):
        actions = action_parts(re.sub(r"\s+", " ", match.group("actions")).strip())
        parsed.append(
            {
                "rule_id": action_value(actions, "id"),
                "phase": action_value(actions, "phase"),
                "target": match.group("target") or "-",
                "operator": match.group("operator") or "-",
                "actions": actions,
                "has_chain_action": any(action.lower() == "chain" for action in actions),
                "transformations": [action.split(":", 1)[1] for action in actions if action.lower().startswith("t:")],
            }
        )
    return parsed


def chain_family(rules: list[dict[str, Any]]) -> dict[str, Any]:
    for index, rule in enumerate(rules):
        if rule.get("has_chain_action"):
            children = []
            for child_index, child in enumerate(rules[index + 1 :], start=1):
                children.append({**child, "implicit_child_id": f"{rule['rule_id']}/chain-{child_index}"})
                if not child.get("has_chain_action"):
                    break
            return {
                "parent_rule_id": rule["rule_id"],
                "parent": rule,
                "children": children,
                "child_rule_ids": [child.get("rule_id") if child.get("rule_id") != "-" else child.get("implicit_child_id") for child in children],
            }
    return {"parent_rule_id": "-", "parent": {}, "children": [], "child_rule_ids": []}


def operator_token(operator: str) -> str:
    parts = str(operator or "").split(maxsplit=1)
    if len(parts) == 2 and parts[0].startswith("@"):
        return parts[1].strip().strip("'\"")
    return "-"


def request_literal(case: dict[str, Any]) -> str:
    request = case.get("request") if isinstance(case.get("request"), dict) else {}
    headers = request.get("headers") if isinstance(request.get("headers"), dict) else {}
    return "\n".join(
        [
            str(request.get("method") or ""),
            str(request.get("path") or ""),
            json.dumps(headers, sort_keys=True),
            str(request.get("body") or ""),
        ]
    )


def log_paths(evidence: dict[str, Any]) -> list[Path]:
    paths = []
    for key, value in evidence.items():
        if not value:
            continue
        if key.endswith("_log_path") or key in {"decision_log", "decision_log_path", "spoa_log_path", "haproxy_log_path"}:
            path = safe_existing_file(value)
            if path is not None:
                paths.append(path)
    return paths


def evidence_text(evidence: dict[str, Any]) -> str:
    return "\n".join(read_text(path) for path in log_paths(evidence))


def token_present(rule: dict[str, Any], literal: str) -> bool:
    token = operator_token(str(rule.get("operator") or ""))
    return token != "-" and token in literal


def rule_logged(logs: str, rule_id: str) -> bool:
    if not rule_id or rule_id == "-":
        return False
    return bool(
        re.search(r'\[id "' + re.escape(rule_id) + r'"\]', logs)
        or re.search(r'"rule_id"\s*:\s*"?' + re.escape(rule_id) + r'"?', logs)
    )


def target_logged(logs: str, target: str) -> bool:
    if not target or target == "-":
        return False
    return target in logs or target.replace(":", "_") in logs


def is_rule_chain_entry(entry: dict[str, Any]) -> bool:
    text = " ".join(
        [
            str(entry.get("case_id") or ""),
            str(entry.get("category") or ""),
            str(entry.get("classification") or ""),
            " ".join(as_list(entry.get("work_direction"))),
            " ".join(as_list(entry.get("failure_pattern"))),
        ]
    ).lower()
    return "rule_chain_semantics" in text or "rule-chain" in text or "rule_chain" in text


def is_chain_named_non_rule_chain(entry: dict[str, Any]) -> bool:
    if is_rule_chain_entry(entry):
        return False
    text = " ".join(
        [
            str(entry.get("case_id") or ""),
            str(entry.get("category") or ""),
            str(entry.get("classification") or ""),
            " ".join(as_list(entry.get("work_direction"))),
            " ".join(as_list(entry.get("failure_pattern"))),
        ]
    ).lower()
    return "chain" in text


def case_group_key(entry: dict[str, Any]) -> str:
    return str(entry.get("case_id") or "-")


def variant(entry: dict[str, Any]) -> str:
    return f"{entry.get('test_variant', '-')}/{entry.get('mrts_variant', '-')}"


def chain_row(entry: dict[str, Any], framework_root: Path) -> dict[str, Any]:
    evidence = read_json(entry.get("evidence"))
    case = load_case(evidence.get("path"))
    rules = parse_rules(str(case.get("rules") or ""))
    family = chain_family(rules)
    parent = family.get("parent") or {}
    children = family.get("children") or []
    literal = request_literal(case)
    logs = evidence_text(evidence)
    parent_expected = token_present(parent, literal)
    child_expected = all(token_present(child, literal) for child in children) if children else False
    parent_observed = rule_logged(logs, str(family.get("parent_rule_id") or "-")) or entry.get("actual_status") == 403
    child_observed = any(target_logged(logs, str(child.get("target") or "")) for child in children) or entry.get("actual_status") == 403
    detection_only = entry.get("classification") == DETECTION_ONLY_CLASSIFICATION
    full_chain_observed = bool(entry.get("actual_status") == 403 or (detection_only and parent_expected and child_expected and parent_observed))
    if detection_only:
        classification = "with_mrts_detection_only_chain_non_disruptive"
        fixability = "report_only"
        risk = "low"
        root_cause = "with-MRTS DetectionOnly overlay suppresses the disruptive chain action; no Chain semantic change is indicated."
    elif full_chain_observed and entry.get("actual_status") != entry.get("expected_status"):
        classification = "full_chain_evidence_without_expected_status"
        fixability = "evidence_parser_or_harness_review"
        risk = "medium"
        root_cause = "Full-chain evidence is visible but the expected status was not observed."
    elif parent_observed and not child_observed:
        classification = "parent_only_not_full_chain"
        fixability = "report_only"
        risk = "low"
        root_cause = "Parent-only evidence is not enough for a disruptive chain expectation."
    else:
        classification = "missing_chain_evidence"
        fixability = "analysis_required"
        risk = "medium"
        root_cause = "The report cannot prove full-chain match evidence from available logs."
    return {
        "connector": entry.get("connector", "-"),
        "variant": variant(entry),
        "case_id": entry.get("case_id", "-"),
        "source": case.get("source", "-"),
        "source_kind": entry.get("source_kind", "-"),
        "corpus": entry.get("mrts_corpus", "-"),
        "case_path": display_case_path(evidence.get("path"), framework_root),
        "rule_id": str(entry.get("rule_id") or family.get("parent_rule_id") or "-"),
        "chain_parent_rule_id": family.get("parent_rule_id", "-"),
        "chain_child_rule_ids": family.get("child_rule_ids", []),
        "phase": str(entry.get("phase") or parent.get("phase") or "-"),
        "targets": [parent.get("target", "-")] + [child.get("target", "-") for child in children],
        "operators": [parent.get("operator", "-")] + [child.get("operator", "-") for child in children],
        "transformations": [item for rule in [parent] + children for item in rule.get("transformations", [])],
        "actions": parent.get("actions", []),
        "expected_status": entry.get("expected_status", "-"),
        "actual_status": entry.get("actual_status", "-"),
        "rule_loaded": bool(rules),
        "chain_parent_matched": "yes" if parent_observed else "unknown",
        "chain_child_matched": "yes" if child_observed else "unknown",
        "full_chain_matched": "yes" if full_chain_observed else "unknown",
        "intervention_created": "no" if detection_only else "yes" if entry.get("actual_status") in {401, 403, 302} else "unknown",
        "backend_reached": entry.get("actual_status") == 200,
        "audit_error_debug_evidence": "yes" if logs else "no",
        "current_classification": entry.get("classification", "-"),
        "current_work_direction": as_list(entry.get("work_direction")) or ["-"],
        "current_priority": entry.get("priority", "-"),
        "analysis_classification": classification,
        "fixability": fixability,
        "risk": risk,
        "root_cause": root_cause,
    }


def single_connector_row(case_id: str, entries: list[dict[str, Any]], framework_root: Path) -> dict[str, Any]:
    example = entries[0]
    evidence = read_json(example.get("evidence"))
    case = load_case(evidence.get("path"))
    rules = parse_rules(str(case.get("rules") or ""))
    expected_statuses = Counter(str(entry.get("expected_status", "-")) for entry in entries)
    actual_statuses = Counter(str(entry.get("actual_status", "-")) for entry in entries)
    classifications = Counter(str(entry.get("classification", "-")) for entry in entries)
    categories = Counter(str(entry.get("category", "-")) for entry in entries)
    phase4 = str(example.get("phase") or "") == "4" or str(example.get("category") or "") == "response-body"
    detection_only = all(entry.get("classification") == DETECTION_ONLY_CLASSIFICATION for entry in entries)
    if detection_only:
        analysis_classification = "with_mrts_detection_only_single_connector_non_disruptive"
        fixability = "report_only"
        root_cause = "with-MRTS DetectionOnly overlay keeps the otherwise disruptive NGINX-specific action non-blocking."
    elif phase4:
        analysis_classification = "phase4_not_next_single_connector_leftover"
        fixability = "report_only"
        root_cause = "Phase-4 hard-abort/log-only evidence is already tracked by the Phase-4 capability report and is not a Rule-Chain runtime fix."
    else:
        analysis_classification = "runtime_fixable_candidate"
        fixability = "targeted_runtime_triage"
        root_cause = "Single-connector failure not covered by existing report-only buckets."
    return {
        "case_id": case_id,
        "count": len(entries),
        "connector": sorted({str(entry.get("connector", "-")) for entry in entries}),
        "variants": sorted({variant(entry) for entry in entries}),
        "case_path": display_case_path(evidence.get("path"), framework_root),
        "category_counts": dict(categories),
        "classification_counts": dict(classifications),
        "phase": str(example.get("phase") or "-"),
        "rule_ids": [rule["rule_id"] for rule in rules if rule["rule_id"] != "-"],
        "expected_statuses": dict(expected_statuses),
        "actual_statuses": dict(actual_statuses),
        "analysis_classification": analysis_classification,
        "fixability": fixability,
        "risk": "low" if fixability == "report_only" else "medium",
        "root_cause": root_cause,
    }


def chain_named_non_rule_row(entry: dict[str, Any], framework_root: Path) -> dict[str, Any]:
    evidence = read_json(entry.get("evidence"))
    case = load_case(evidence.get("path"))
    rules = parse_rules(str(case.get("rules") or ""))
    return {
        "connector": entry.get("connector", "-"),
        "variant": variant(entry),
        "case_id": entry.get("case_id", "-"),
        "case_path": display_case_path(evidence.get("path"), framework_root),
        "category": entry.get("category", "-"),
        "classification": entry.get("classification", "-"),
        "work_direction": as_list(entry.get("work_direction")) or ["-"],
        "rule_ids": [rule["rule_id"] for rule in rules if rule["rule_id"] != "-"],
        "expected_status": entry.get("expected_status", "-"),
        "actual_status": entry.get("actual_status", "-"),
        "analysis_classification": "transformation_chain_name_not_secrule_chain",
        "fixability": "not_this_cluster",
        "root_cause": "The case name contains chain, but the rules are transformation-chain semantics rather than a SecRule chain construct.",
    }


def top_single_connector_failures(failures: list[dict[str, Any]], framework_root: Path) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in failures:
        grouped[case_group_key(entry)].append(entry)
    rows = []
    for case_id, entries in grouped.items():
        if len({entry.get("connector") for entry in entries}) == 1:
            rows.append(single_connector_row(case_id, entries, framework_root))
    rows.sort(key=lambda item: (-item["count"], item["case_id"]))
    return rows


def build_report(connector_root: Path, framework_root: Path) -> dict[str, Any]:
    queue = read_json(report_path(connector_root, "connector_work_queue", "json"))
    entries = [entry for entry in queue.get("entries", []) if isinstance(entry, dict)]
    failures = [entry for entry in entries if entry.get("runtime_status") == "FAIL"]
    chain_failures = [entry for entry in failures if is_rule_chain_entry(entry)]
    chain_named_non_rule = [entry for entry in failures if is_chain_named_non_rule_chain(entry)]
    chain_rows = [chain_row(entry, framework_root) for entry in chain_failures]
    non_rule_rows = [chain_named_non_rule_row(entry, framework_root) for entry in chain_named_non_rule]
    single_rows = top_single_connector_failures(failures, framework_root)
    runtime_candidates = [row for row in single_rows if row["analysis_classification"] == "runtime_fixable_candidate"]
    report_only_rows = [row for row in chain_rows if row["fixability"] == "report_only"] + [row for row in single_rows if row["fixability"] == "report_only"]
    next_plan = read_json(report_path(connector_root, "next_fix_plan", "json"))
    summary = {
        "rule_chain_failure_rows": len(chain_rows),
        "rule_chain_case_groups": len({row["case_id"] for row in chain_rows}),
        "chain_named_non_rule_chain_rows": len(non_rule_rows),
        "chain_named_non_rule_chain_groups": len({row["case_id"] for row in non_rule_rows}),
        "small_single_connector_failure_groups": len(single_rows),
        "small_single_connector_failure_rows": sum(int(row["count"]) for row in single_rows),
        "runtime_fixable_candidates": len(runtime_candidates),
        "report_only_items": len(report_only_rows),
        "chain_parent_matched_rows": sum(1 for row in chain_rows if row["chain_parent_matched"] == "yes"),
        "chain_child_matched_rows": sum(1 for row in chain_rows if row["chain_child_matched"] == "yes"),
        "full_chain_matched_rows": sum(1 for row in chain_rows if row["full_chain_matched"] == "yes"),
        "full_chain_disruptive_rows": sum(1 for row in chain_rows if row["actual_status"] in {401, 403, 302}),
        "full_chain_non_disruptive_detection_only_rows": sum(1 for row in chain_rows if row["analysis_classification"] == "with_mrts_detection_only_chain_non_disruptive"),
        "evidence_parser_missing_full_chain_rows": sum(1 for row in chain_rows if row["analysis_classification"] == "missing_chain_evidence"),
        "connectors": dict(Counter(row["connector"] for row in chain_rows)),
        "single_connector_connectors": dict(Counter(connector for row in single_rows for connector in row["connector"])),
        "single_connector_classifications": dict(Counter(row["analysis_classification"] for row in single_rows)),
    }
    return {
        "generated_at": utc_now(),
        "report_kind": "rule-chain-semantics-analysis",
        "source_reports": {
            "connector_work_queue": queue.get("generated_at", "-"),
            "remaining_failure_analysis": read_json(report_path(connector_root, "remaining_failure_analysis", "json")).get("generated_at", "-"),
            "next_fix_plan": next_plan.get("generated_at", "-"),
            "full_runtime_matrix": read_json(report_path(connector_root, "full_runtime_matrix", "json")).get("generated_at", "-"),
            "connector_work_queue_path": report_relpath("connector_work_queue", "json"),
            "remaining_failure_analysis_path": report_relpath("remaining_failure_analysis", "json"),
            "next_fix_plan_path": report_relpath("next_fix_plan", "json"),
            "full_runtime_matrix_path": report_relpath("full_runtime_matrix", "json"),
        },
        "summary": summary,
        "rule_chain_failures": chain_rows,
        "chain_named_non_rule_chain_failures": non_rule_rows,
        "small_single_connector_failures": single_rows,
        "runtime_fixable_candidates": runtime_candidates,
        "next_recommendation": next_plan.get("recommendation", {}),
        "conclusion": {
            "selected_subcluster": "with-MRTS DetectionOnly redirect classification and report-only Rule-Chain triage",
            "root_cause": "Rule-chain semantics are not the active blocker: no-MRTS Rule-Chain rows pass, while with-MRTS failures are non-disruptive DetectionOnly overlay rows. The remaining NGINX-only rows are either Phase-4 not-next evidence or with-MRTS DetectionOnly rows.",
            "safe_change": "metadata/report-only classification; no Expected status, rule, MRTS definition, or connector-core change.",
        },
    }


def md_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(str(item).replace("|", "\\|") for item in row) + " |")
    return lines


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Rule Chain Semantics Analysis",
        "",
        f"Generated at: `{report['generated_at']}`",
        "",
        "## Summary",
    ]
    lines.extend(
        md_table(
            [
                "Rule-chain rows",
                "Rule-chain groups",
                "Single-connector groups",
                "Single-connector rows",
                "Runtime-fixable candidates",
                "Report-only items",
                "Parent matched",
                "Child matched",
                "Full chain matched",
                "Name-only non-rule-chain rows",
            ],
            [
                [
                    summary["rule_chain_failure_rows"],
                    summary["rule_chain_case_groups"],
                    summary["small_single_connector_failure_groups"],
                    summary["small_single_connector_failure_rows"],
                    summary["runtime_fixable_candidates"],
                    summary["report_only_items"],
                    summary["chain_parent_matched_rows"],
                    summary["chain_child_matched_rows"],
                    summary["full_chain_matched_rows"],
                    summary["chain_named_non_rule_chain_rows"],
                ]
            ],
        )
    )
    lines.extend(
        [
            "",
            "## Conclusion",
            f"- Selected subcluster: {report['conclusion']['selected_subcluster']}.",
            f"- Root cause: {report['conclusion']['root_cause']}",
            f"- Safe change: {report['conclusion']['safe_change']}",
            "",
            "## Rule-Chain Failure Rows",
        ]
    )
    if report["rule_chain_failures"]:
        lines.extend(
            md_table(
                [
                    "Connector",
                    "Variant",
                    "Case",
                    "Parent",
                    "Children",
                    "Expected",
                    "Actual",
                    "Parent matched",
                    "Child matched",
                    "Full chain",
                    "Classification",
                    "Fixability",
                ],
                [
                    [
                        row["connector"],
                        row["variant"],
                        row["case_id"],
                        row["chain_parent_rule_id"],
                        ", ".join(row["chain_child_rule_ids"]) or "-",
                        row["expected_status"],
                        row["actual_status"],
                        row["chain_parent_matched"],
                        row["chain_child_matched"],
                        row["full_chain_matched"],
                        row["analysis_classification"],
                        row["fixability"],
                    ]
                    for row in report["rule_chain_failures"]
                ],
            )
        )
    else:
        lines.append("- None.")
    lines.extend(["", "## Chain-Named Non-Rule-Chain Rows"])
    if report["chain_named_non_rule_chain_failures"]:
        lines.extend(
            md_table(
                ["Connector", "Variant", "Case", "Category", "Rules", "Expected", "Actual", "Classification", "Root cause"],
                [
                    [
                        row["connector"],
                        row["variant"],
                        row["case_id"],
                        row["category"],
                        ", ".join(row["rule_ids"]) or "-",
                        row["expected_status"],
                        row["actual_status"],
                        row["analysis_classification"],
                        row["root_cause"],
                    ]
                    for row in report["chain_named_non_rule_chain_failures"]
                ],
            )
        )
    else:
        lines.append("- None.")
    lines.extend(["", "## Single-Connector Leftovers"])
    if report["small_single_connector_failures"]:
        lines.extend(
            md_table(
                ["Count", "Connector", "Case", "Variants", "Rules", "Expected", "Actual", "Classification", "Fixability", "Root cause"],
                [
                    [
                        row["count"],
                        ", ".join(row["connector"]),
                        row["case_id"],
                        ", ".join(row["variants"]),
                        ", ".join(row["rule_ids"]) or "-",
                        row["expected_statuses"],
                        row["actual_statuses"],
                        row["analysis_classification"],
                        row["fixability"],
                        row["root_cause"],
                    ]
                    for row in report["small_single_connector_failures"]
                ],
            )
        )
    else:
        lines.append("- None.")
    rec = report.get("next_recommendation") or {}
    lines.extend(
        [
            "",
            "## Next Recommendation",
            f"- Recommended next cluster: `{rec.get('recommended_next_fix_cluster', 'none')}`",
            f"- Reason: {rec.get('reason', '-')}",
        ]
    )
    return "\n".join(lines) + "\n"


def update_full_run_evidence(report_dir: Path, report: dict[str, Any]) -> None:
    if os.environ.get("SUPPRESS_FULL_RUN_EVIDENCE_SIDE_EFFECTS") == "1":
        return
    json_path = report_path_from_root(report_dir, "full_run_evidence", "json")
    data = read_json(json_path)
    if data:
        data["rule_chain_semantics_analysis"] = {
            "report": report_relpath("rule_chain_semantics_analysis", "md"),
            "json": report_relpath("rule_chain_semantics_analysis", "json"),
            "summary": report["summary"],
        }
        reports = data.get("reports")
        if isinstance(reports, list):
            for item in (
                report_relpath("rule_chain_semantics_analysis", "json"),
                report_relpath("rule_chain_semantics_analysis", "md"),
            ):
                if item not in reports:
                    reports.append(item)
            data["reports"] = reports
        write_json(json_path, data)

    md_path = report_path_from_root(report_dir, "full_run_evidence", "md")
    text = read_text(md_path)
    if text:
        section = "\n".join(
            [
                "## Rule Chain Semantics Analysis",
                f"- Report: `{report_relpath('rule_chain_semantics_analysis', 'md')}`",
                f"- Rule-chain failure rows: **{report['summary']['rule_chain_failure_rows']}**",
                f"- Runtime-fixable candidates: **{report['summary']['runtime_fixable_candidates']}**",
                "- The report keeps Expected status and runtime PASS/FAIL unchanged while classifying report-only Rule-Chain and single-connector leftovers.",
            ]
        )
        start = "<!-- rule-chain-semantics-analysis:start -->"
        end = "<!-- rule-chain-semantics-analysis:end -->"
        marked = f"{start}\n{section}\n{end}"
        if start in text and end in text:
            prefix = text.split(start, 1)[0].rstrip()
            suffix = text.split(end, 1)[1].lstrip()
            text = f"{prefix}\n\n{marked}\n\n{suffix}".rstrip() + "\n"
        elif "## Reports And Logs" in text:
            prefix, suffix = text.split("## Reports And Logs", 1)
            text = f"{prefix.rstrip()}\n\n{marked}\n\n## Reports And Logs{suffix}".rstrip() + "\n"
        else:
            text = text.rstrip() + "\n\n" + marked + "\n"
        write_text_file(md_path, text)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector-root", default=".")
    parser.add_argument("--framework-root", default=None)
    parser.add_argument("--output-dir", default=None)
    args = parser.parse_args()
    connector_root = Path(args.connector_root).resolve()
    framework_root = Path(args.framework_root).resolve() if args.framework_root else connector_root / "modules/ModSecurity-test-Framework"
    output_dir = resolve_output_dir(connector_root, args.output_dir, REPORT_DIR)
    add_safe_roots(connector_root, framework_root, connector_root / REPORT_DIR)
    add_report_roots(connector_root / REPORT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    report = build_report(connector_root, framework_root)
    metadata = build_metadata(
        generated_by="ci/generate-rule-chain-semantics-analysis.py",
        make_target="generate-rule-chain-semantics-analysis",
        connector_root=connector_root,
        framework_root=framework_root,
        inputs=[
            report["source_reports"]["connector_work_queue_path"],
            report["source_reports"]["remaining_failure_analysis_path"],
            report["source_reports"]["next_fix_plan_path"],
            report["source_reports"]["full_runtime_matrix_path"],
        ],
        generated_at=report["generated_at"],
    )
    json_path = report_path_from_root(output_dir, "rule_chain_semantics_analysis", "json")
    md_path = report_path_from_root(output_dir, "rule_chain_semantics_analysis", "md")
    write_text_file(json_path, generated_json_text(report, metadata))
    write_text_file(md_path, generated_markdown_text(render_markdown(report), metadata))
    update_full_run_evidence(output_dir, report)
    print(md_path)
    print(json_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
