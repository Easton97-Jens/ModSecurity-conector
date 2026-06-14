#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from report_path_safety import add_report_roots, add_safe_roots, read_json_file, read_text_file, resolve_output_dir, write_json_file, write_text_file


REPORT_DIR = Path("reports/testing/generated")
REPORT_JSON = "reports/testing/generated/final-consistency-audit.generated.json"
REPORT_MD = "reports/testing/generated/final-consistency-audit.generated.md"

INPUT_REPORTS = (
    "full-runtime-matrix.generated.json",
    "connector-work-queue.generated.json",
    "phase-work-queue.generated.json",
    "remaining-failure-analysis.generated.json",
    "next-fix-plan.generated.json",
    "full-run-evidence.generated.json",
    "mrts-native-summary.generated.json",
    "phase4-hard-abort-capability.generated.json",
    "nolog-audit-evidence.generated.json",
    "response-header-hook-analysis.generated.json",
    "body-processor-analysis.generated.json",
    "intervention-blocking-analysis.generated.json",
    "no-mrts-intervention-nomatch-analysis.generated.json",
    "rule-chain-semantics-analysis.generated.json",
)

REPORT_ONLY_CATEGORIES = {
    "with_mrts_detection_only_non_disruptive",
    "response_header_mrts_detection_only",
    "xml_processor_activation_missing",
    "multipart_processor_activation_missing",
    "nolog_expected_no_audit",
    "phase4_log_only_no_abort",
}
SEMANTIC_PENDING_CATEGORIES = {
    "transformation_semantics",
    "collection_name_normalization_semantics",
}
CAPABILITY_PENDING_CATEGORIES = {
    "phase4_missing_abort_evidence",
}
CONNECTOR_GAP_CATEGORIES = {
    "phase4_connector_gap",
    "connector_gap",
}
NOT_NEXT_CLUSTERS = {
    "phase4_hard_abort_capability",
    "transformation_semantics",
    "nolog_expected_no_audit",
    "response_header_mrts_detection_only",
    "with_mrts_detection_only_non_disruptive",
    "xml_processor_activation_missing",
    "multipart_processor_activation_missing",
    "collection_name_normalization_semantics",
}
STALE_CLUSTER_NAMES = (
    "audit_log_evidence",
    "intervention_blocking",
    "request_body_processor",
    "multipart_files",
    "xml_processor",
    "phase4_hard_abort_supported",
    "rule_chain_semantics",
    "response_header_backend_setup",
    "response_header_hook",
    "response_header_multi_value_gap",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    return read_json_file(path)


def write_json(path: Path, data: dict[str, Any]) -> None:
    write_json_file(path, data)


def git_stdout(root: Path, args: list[str]) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except Exception:
        return "unknown"
    return result.stdout.strip()


def git_status(root: Path) -> list[str]:
    output = git_stdout(root, ["status", "--short"])
    if not output or output == "unknown":
        return []
    return output.splitlines()


def listify(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if value in (None, ""):
        return []
    return [str(value)]


def counter_dict(counter: Counter[str]) -> dict[str, int]:
    return {key: counter[key] for key in sorted(counter)}


def count_by(entries: list[dict[str, Any]], field: str) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for entry in entries:
        values = listify(entry.get(field))
        if not values:
            values = ["-"]
        counts.update(values)
    return counter_dict(counts)


def compact_category(row: dict[str, Any]) -> dict[str, Any]:
    category = str(row.get("category") or "-")
    if category in REPORT_ONLY_CATEGORIES:
        disposition = "report_only"
    elif category in SEMANTIC_PENDING_CATEGORIES:
        disposition = "semantic_pending_native_or_libmodsecurity_comparison"
    elif category in CAPABILITY_PENDING_CATEGORIES:
        disposition = "capability_evidence_pending"
    elif category in CONNECTOR_GAP_CATEGORIES:
        disposition = "connector_gap"
    elif int(row.get("count") or 0) == 0:
        disposition = "clear"
    else:
        disposition = "review_required"
    return {
        "category": category,
        "count": int(row.get("count") or 0),
        "connectors": row.get("connectors", []),
        "disposition": disposition,
        "fixable": row.get("fixable", "-"),
        "recommended_next_step": row.get("recommended_next_step", "-"),
        "risk": row.get("risk", "-"),
    }


def category_count(categories: dict[str, dict[str, Any]], category: str) -> int:
    row = categories.get(category) or {}
    return int(row.get("count") or 0)


def recommendation_cluster_count(categories: dict[str, dict[str, Any]], cluster: str) -> int:
    if cluster == "phase4_hard_abort_capability":
        return (
            category_count(categories, "phase4_missing_abort_evidence")
            + category_count(categories, "phase4_connector_gap")
            + category_count(categories, "phase4_log_only_no_abort")
        )
    return category_count(categories, cluster)


def build_stale_cluster_audit(
    categories: dict[str, dict[str, Any]],
    failed_entries: list[dict[str, Any]],
    rule_chain: dict[str, Any],
) -> list[dict[str, Any]]:
    work_direction_counts = count_by(failed_entries, "work_direction")
    classification_counts = count_by(failed_entries, "classification")
    rows: list[dict[str, Any]] = []
    for cluster in STALE_CLUSTER_NAMES:
        remaining_count = category_count(categories, cluster)
        work_direction_count = int(work_direction_counts.get(cluster, 0))
        classification_count = int(classification_counts.get(cluster, 0))
        if cluster == "phase4_hard_abort_supported":
            classification_count += int(classification_counts.get("phase4-hard-abort-supported", 0))
        if cluster == "rule_chain_semantics":
            runtime_fixable = int(rule_chain.get("summary", {}).get("runtime_fixable_candidates") or 0)
            status = "clear" if remaining_count == 0 and runtime_fixable == 0 else "review"
            detail = f"runtime_fixable_candidates={runtime_fixable}"
        elif cluster == "request_body_processor" and work_direction_count:
            status = "known_connector_gap_not_active_processor_cluster"
            detail = "remaining work-direction rows are classified as phase1 request-body unavailable connector gap"
        elif remaining_count == 0 and work_direction_count == 0 and classification_count == 0:
            status = "clear"
            detail = "no active rows"
        else:
            status = "review"
            detail = "nonzero remaining, work-direction, or classification count"
        rows.append(
            {
                "cluster": cluster,
                "remaining_category_count": remaining_count,
                "failed_work_direction_count": work_direction_count,
                "failed_classification_count": classification_count,
                "status": status,
                "detail": detail,
            }
        )
    return rows


def native_status(native_summary: dict[str, Any]) -> dict[str, Any]:
    targets = native_summary.get("targets", {})
    result: dict[str, Any] = {}
    for target, payload in sorted(targets.items()):
        counts = payload.get("counts", {}) if isinstance(payload, dict) else {}
        result[target] = {
            "status": payload.get("status", "-") if isinstance(payload, dict) else "-",
            "attempted": counts.get("attempted", 0),
            "pass": counts.get("pass", 0),
            "fail": counts.get("fail", 0),
            "blocked": counts.get("blocked", 0),
            "failed_cases": counts.get("failed_cases", []),
            "classification": "native_modsecurity_semantics / phase4_native_limitation"
            if "100003-1" in listify(counts.get("failed_cases"))
            else "-",
        }
    return result


def input_freshness(report_dir: Path) -> list[dict[str, Any]]:
    freshness: list[dict[str, Any]] = []
    for name in INPUT_REPORTS:
        path = report_dir / name
        data = read_json(path)
        freshness.append(
            {
                "path": f"reports/testing/generated/{name}",
                "present": path.is_file(),
                "generated_at": data.get("generated_at", "-"),
                "report_kind": data.get("report_kind", "-"),
            }
        )
    return freshness


def build_audit(connector_root: Path, framework_root: Path) -> dict[str, Any]:
    report_dir = connector_root / REPORT_DIR
    full_matrix = read_json(report_dir / "full-runtime-matrix.generated.json")
    queue = read_json(report_dir / "connector-work-queue.generated.json")
    remaining = read_json(report_dir / "remaining-failure-analysis.generated.json")
    next_plan = read_json(report_dir / "next-fix-plan.generated.json")
    native_summary = read_json(report_dir / "mrts-native-summary.generated.json")
    phase4 = read_json(report_dir / "phase4-hard-abort-capability.generated.json")
    body = read_json(report_dir / "body-processor-analysis.generated.json")
    intervention = read_json(report_dir / "intervention-blocking-analysis.generated.json")
    response_headers = read_json(report_dir / "response-header-hook-analysis.generated.json")
    nolog = read_json(report_dir / "nolog-audit-evidence.generated.json")
    rule_chain = read_json(report_dir / "rule-chain-semantics-analysis.generated.json")

    entries = [entry for entry in queue.get("entries", []) if isinstance(entry, dict)]
    failed_entries = [entry for entry in entries if entry.get("runtime_status") == "FAIL"]
    non_pass_entries = [entry for entry in entries if entry.get("runtime_status") != "PASS"]
    category_rows = [compact_category(row) for row in remaining.get("category_rollup", []) if isinstance(row, dict)]
    categories = {row["category"]: row for row in category_rows}
    nonzero_categories = [row for row in category_rows if row["count"]]

    queue_totals_priority = queue.get("totals", {}).get("priority", {})
    recomputed_non_pass_priority = count_by(non_pass_entries, "priority")
    queue_totals_consistent = dict(queue_totals_priority) == dict(recomputed_non_pass_priority)
    recommendation = next_plan.get("recommendation", {})
    recommended_cluster = str(recommendation.get("recommended_next_fix_cluster") or "-")
    stale_audit = build_stale_cluster_audit(categories, failed_entries, rule_chain)
    stale_runtime_fixable = [
        item for item in stale_audit
        if item["status"] not in {"clear", "known_connector_gap_not_active_processor_cluster"}
    ]
    p0_p1_failure_count = sum(1 for entry in failed_entries if entry.get("priority") in {"P0", "P1"})
    p2_failures = [entry for entry in failed_entries if entry.get("priority") == "P2"]
    p2_detection_only = all(
        entry.get("classification") == "response-header-mrts-detection-only"
        and "response_header_mrts_detection_only" in listify(entry.get("work_direction"))
        for entry in p2_failures
    )
    active_runtime_fixable_clusters: list[str] = []
    for row in nonzero_categories:
        if row["disposition"] == "review_required":
            active_runtime_fixable_clusters.append(row["category"])

    not_next = [
        {
            "cluster": str(item.get("cluster") or "-"),
            "reason": str(item.get("reason") or "-"),
            "count": recommendation_cluster_count(categories, str(item.get("cluster") or "")),
        }
        for item in recommendation.get("not_next", [])
        if isinstance(item, dict)
    ]
    not_next_known = sorted({item["cluster"] for item in not_next if item["cluster"] in NOT_NEXT_CLUSTERS})

    body_summary = body.get("summary", {})
    intervention_summary = intervention.get("summary", {})
    response_header_summary = response_headers.get("summary", {})
    nolog_summary = nolog.get("summary", {})
    rule_chain_summary = rule_chain.get("summary", {})
    phase4_summary = phase4.get("summary", {})
    phase4_connector_summary = phase4.get("connector_summary", {})

    release_checks = {
        "recommended_next_fix_cluster_none": recommended_cluster == "none",
        "blocked_zero": int(full_matrix.get("totals", {}).get("blocked") or 0) == 0,
        "queue_totals_consistent": queue_totals_consistent,
        "p0_p1_failure_rows_zero": p0_p1_failure_count == 0,
        "p2_rows_are_response_header_mrts_detection_only": p2_detection_only,
        "active_runtime_fixable_clusters_zero": not active_runtime_fixable_clusters,
        "intervention_blocking_true_candidates_zero": int(intervention_summary.get("intervention_blocking_true_candidates") or 0) == 0,
        "audit_log_evidence_after_zero": int(nolog_summary.get("audit_log_evidence_after") or 0) == 0,
        "body_processor_active_after_zero": int(body_summary.get("after_metadata_fix", {}).get("combined") or 0) == 0,
        "response_header_backend_setup_zero": int(response_header_summary.get("response_header_hook_after") or 0) == 0,
        "rule_chain_runtime_fixable_zero": int(rule_chain_summary.get("runtime_fixable_candidates") or 0) == 0,
        "phase4_supported_label_absent": "phase4_hard_abort_supported" not in phase4_summary.get("category_counts", {}),
    }
    release_ready = all(release_checks.values())

    return {
        "report_kind": "final-consistency-audit",
        "generated_at": utc_now(),
        "source_reports": {
            "full_runtime_matrix": "reports/testing/generated/full-runtime-matrix.generated.json",
            "connector_work_queue": "reports/testing/generated/connector-work-queue.generated.json",
            "phase_work_queue": "reports/testing/generated/phase-work-queue.generated.json",
            "remaining_failure_analysis": "reports/testing/generated/remaining-failure-analysis.generated.json",
            "next_fix_plan": "reports/testing/generated/next-fix-plan.generated.json",
            "full_run_evidence": "reports/testing/generated/full-run-evidence.generated.json",
        },
        "git_snapshot": {
            "connector_head": git_stdout(connector_root, ["rev-parse", "HEAD"]),
            "framework_head": git_stdout(framework_root, ["rev-parse", "HEAD"]),
            "submodules": git_stdout(connector_root, ["submodule", "status", "--recursive"]).splitlines(),
        },
        "full_matrix_summary": full_matrix.get("totals", {}),
        "remaining_summary": remaining.get("summary", {}),
        "priority_distribution": {
            "queue_totals_non_pass": queue_totals_priority,
            "recomputed_non_pass": recomputed_non_pass_priority,
            "recomputed_failures": count_by(failed_entries, "priority"),
            "p0_p1_failure_rows": p0_p1_failure_count,
        },
        "active_vs_report_only": {
            "active_runtime_fixable_clusters": active_runtime_fixable_clusters,
            "report_only_rows": sum(row["count"] for row in nonzero_categories if row["disposition"] == "report_only"),
            "semantic_pending_rows": sum(row["count"] for row in nonzero_categories if row["disposition"].startswith("semantic_pending")),
            "capability_evidence_pending_rows": sum(row["count"] for row in nonzero_categories if row["disposition"] == "capability_evidence_pending"),
            "connector_gap_rows": sum(row["count"] for row in nonzero_categories if row["disposition"] == "connector_gap"),
            "categories": nonzero_categories,
        },
        "stale_cluster_audit": stale_audit,
        "clusters_no_longer_next": {
            "not_next_clusters_present": not_next_known,
            "not_next": not_next,
            "p3_plan": next_plan.get("priority_plan", {}).get("P3", []),
        },
        "recommended_next_fix_cluster": {
            "value": recommended_cluster,
            "reason": recommendation.get("reason", "-"),
            "justified": recommended_cluster == "none" and not active_runtime_fixable_clusters and not stale_runtime_fixable,
        },
        "remaining_known_gaps": {
            "phase4_missing_abort_evidence": category_count(categories, "phase4_missing_abort_evidence"),
            "phase4_connector_gap": category_count(categories, "phase4_connector_gap"),
            "transformation_semantics": category_count(categories, "transformation_semantics"),
            "collection_name_normalization_semantics": category_count(categories, "collection_name_normalization_semantics"),
            "connector_gap": category_count(categories, "connector_gap"),
        },
        "user_decision_required": [
            {
                "area": "phase4_hard_abort",
                "reason": "Apache has implementation-path evidence but no runtime hard-abort proof; HAProxy remains a connector gap.",
                "safe_next": "collect real transport-abort evidence or keep these rows as capability/gap classifications",
            },
            {
                "area": "transformation_and_collection_semantics",
                "reason": "remaining no-match rows need native/libmodsecurity comparison before runtime changes.",
                "safe_next": "decide whether to build comparator evidence; do not change Expected statuses or rules.",
            },
            {
                "area": "phase1_request_body_connector_gap",
                "reason": "three rows remain classified as phase1 request-body unavailable connector gap.",
                "safe_next": "treat as connector capability discussion before core behavior changes.",
            },
        ],
        "native_mrts_status": {
            "note": "Native MRTS evidence remains separate from connector Full-Matrix PASS/FAIL.",
            "targets": native_status(native_summary),
        },
        "phase4_status": {
            "rows": phase4_summary.get("rows", 0),
            "hard_abort_evidence_rows": phase4_summary.get("hard_abort_evidence_rows", 0),
            "sensitive_log_leak_rows": phase4_summary.get("sensitive_log_leak_rows", 0),
            "connector_summary": {
                connector: {
                    "capability_status": data.get("capability_status", "-"),
                    "hard_abort_evidence_rows": data.get("hard_abort_evidence_rows", 0),
                }
                for connector, data in sorted(phase4_connector_summary.items())
                if isinstance(data, dict)
            },
        },
        "freshness": input_freshness(report_dir),
        "guardrails": {
            "expected_status_changed": False,
            "runtime_pass_fail_manually_changed": False,
            "mrt_definitions_changed": False,
            "tools_mrts_changed": False,
            "rules_changed": False,
            "connector_core_changed": False,
            "full_matrix_rerun_required": False,
            "matrix_counts_source": "existing full-runtime-matrix evidence",
        },
        "release_checks": release_checks,
        "release_readiness": "ready_with_known_reported_gaps" if release_ready else "needs_attention",
    }


def table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    if not rows:
        lines.append("| " + " | ".join("-" for _ in headers) + " |")
        return lines
    for row in rows:
        lines.append("| " + " | ".join(str(item).replace("|", "\\|").replace("\n", " ") for item in row) + " |")
    return lines


def yes_no(value: Any) -> str:
    return "yes" if bool(value) else "no"


def render_markdown(audit: dict[str, Any]) -> str:
    totals = audit["full_matrix_summary"]
    recommendation = audit["recommended_next_fix_cluster"]
    priority = audit["priority_distribution"]
    phase4_status = audit["phase4_status"]
    non_pass_priority = priority["recomputed_non_pass"]
    priority_line = (
        f"{non_pass_priority.get('P0', 0)} / {non_pass_priority.get('P1', 0)} / "
        f"{non_pass_priority.get('P2', 0)} / {non_pass_priority.get('P3', 0)} / "
        f"{non_pass_priority.get('report_only', 0)}"
    )
    lines = [
        "# Final Consistency Audit",
        "",
        "Generated file - do not edit manually.",
        "",
        f"- Generated at: `{audit['generated_at']}`",
        f"- Release readiness: `{audit['release_readiness']}`",
        f"- Recommended next fix cluster: `{recommendation['value']}`",
        f"- Recommendation justified: `{yes_no(recommendation['justified'])}`",
        f"- Reason: {recommendation['reason']}",
        "",
        "## Git And Submodules",
        f"- Connector HEAD: `{audit['git_snapshot']['connector_head']}`",
        f"- Framework HEAD: `{audit['git_snapshot']['framework_head']}`",
        "",
        *table(
            ["Submodule status"],
            [[line] for line in audit["git_snapshot"]["submodules"]],
        ),
        "",
        "## Full-Matrix Summary",
        f"- Attempted: **{totals.get('attempted', 0)}**",
        f"- PASS: **{totals.get('pass', 0)}**",
        f"- FAIL: **{totals.get('fail', 0)}**",
        f"- BLOCKED: **{totals.get('blocked', 0)}**",
        f"- NOT_EXECUTABLE: **{totals.get('not_executable', 0)}**",
        f"- Pending: **{totals.get('pending', 0)}**",
        "- Full-Matrix was not rerun for this audit; counts come from existing evidence.",
        "",
        "## Priority Distribution",
        f"- P0/P1/P2/P3/report_only non-PASS: **{priority_line}**",
        f"- Queue totals and recomputed non-PASS priorities match: `{yes_no(audit['release_checks']['queue_totals_consistent'])}`",
        f"- Queue totals non-PASS: `{priority['queue_totals_non_pass']}`",
        f"- Recomputed non-PASS: `{priority['recomputed_non_pass']}`",
        f"- Recomputed FAIL only: `{priority['recomputed_failures']}`",
        f"- P0/P1 failing rows: **{priority['p0_p1_failure_rows']}**",
        f"- P2 rows are response-header DetectionOnly/report-only leftovers: `{yes_no(audit['release_checks']['p2_rows_are_response_header_mrts_detection_only'])}`",
        "",
        "## Remaining Categories",
        f"- Active runtime-fixable clusters: **{len(audit['active_vs_report_only']['active_runtime_fixable_clusters'])}**",
        f"- Report-only rows: **{audit['active_vs_report_only']['report_only_rows']}**",
        f"- Semantic pending rows: **{audit['active_vs_report_only']['semantic_pending_rows']}**",
        f"- Capability-evidence pending rows: **{audit['active_vs_report_only']['capability_evidence_pending_rows']}**",
        f"- Connector-gap rows: **{audit['active_vs_report_only']['connector_gap_rows']}**",
    ]
    category_rows = [
        [
            row["category"],
            row["count"],
            ", ".join(row.get("connectors", [])) or "-",
            row["disposition"],
            row["recommended_next_step"],
        ]
        for row in audit["active_vs_report_only"]["categories"]
    ]
    lines.extend(table(["Category", "Count", "Connectors", "Disposition", "Recommended next step"], category_rows))
    lines.extend(
        [
            "",
            "## Stale Cluster Check",
        ]
    )
    lines.extend(table(
        ["Cluster", "Remaining category", "FAIL work direction", "FAIL classification", "Status", "Detail"],
        [
            [
                item["cluster"],
                item["remaining_category_count"],
                item["failed_work_direction_count"],
                item["failed_classification_count"],
                item["status"],
                item["detail"],
            ]
            for item in audit["stale_cluster_audit"]
        ],
    ))
    lines.extend(
        [
            "",
            "## Clusters No Longer Next",
        ]
    )
    lines.extend(table(
        ["Cluster", "Count", "Reason"],
        [[item["cluster"], item["count"], item["reason"]] for item in audit["clusters_no_longer_next"]["not_next"]],
    ))
    lines.extend(
        [
            "",
            "## Known Gaps",
        ]
    )
    lines.extend(table(
        ["Gap", "Rows"],
        [[name, count] for name, count in audit["remaining_known_gaps"].items()],
    ))
    lines.extend(
        [
            "",
            "## User Decisions",
        ]
    )
    lines.extend(table(
        ["Area", "Reason", "Safe next"],
        [[item["area"], item["reason"], item["safe_next"]] for item in audit["user_decision_required"]],
    ))
    lines.extend(
        [
            "",
            "## Native MRTS",
            "- Native MRTS evidence remains separate from connector Full-Matrix PASS/FAIL.",
        ]
    )
    lines.extend(table(
        ["Target", "Status", "Attempted", "PASS", "FAIL", "BLOCKED", "Failed cases", "Classification"],
        [
            [
                target,
                data["status"],
                data["attempted"],
                data["pass"],
                data["fail"],
                data["blocked"],
                ", ".join(data.get("failed_cases", [])) or "-",
                data["classification"],
            ]
            for target, data in audit["native_mrts_status"]["targets"].items()
        ],
    ))
    lines.extend(
        [
            "",
            "## Phase 4 Hard-Abort",
            f"- Rows: **{phase4_status['rows']}**",
            f"- Hard-abort evidence rows: **{phase4_status['hard_abort_evidence_rows']}**",
            f"- Sensitive log leak rows: **{phase4_status['sensitive_log_leak_rows']}**",
        ]
    )
    lines.extend(table(
        ["Connector", "Capability status", "Hard-abort evidence rows"],
        [
            [connector, data["capability_status"], data["hard_abort_evidence_rows"]]
            for connector, data in phase4_status["connector_summary"].items()
        ],
    ))
    lines.extend(
        [
            "",
            "## Freshness",
        ]
    )
    lines.extend(table(
        ["Input", "Present", "Generated at"],
        [[item["path"], yes_no(item["present"]), item["generated_at"]] for item in audit["freshness"]],
    ))
    lines.extend(
        [
            "",
            "## Guardrails",
        ]
    )
    lines.extend(table(
        ["Guardrail", "Value"],
        [[name, value] for name, value in audit["guardrails"].items()],
    ))
    lines.extend(
        [
            "",
            "## Release Checks",
        ]
    )
    lines.extend(table(
        ["Check", "Pass"],
        [[name, yes_no(value)] for name, value in audit["release_checks"].items()],
    ))
    return "\n".join(lines) + "\n"


def replace_marked_section(text: str, start: str, end: str, section: str) -> str:
    if start in text and end in text:
        before = text.split(start, 1)[0]
        after = text.split(end, 1)[1]
        return before + start + "\n" + section.strip() + "\n" + end + after
    insert_before = "## Reports And Logs"
    block = start + "\n" + section.strip() + "\n" + end + "\n\n"
    if insert_before in text:
        return text.replace(insert_before, block + insert_before, 1)
    return text.rstrip() + "\n\n" + block


def update_full_run_evidence(report_dir: Path, audit: dict[str, Any]) -> None:
    json_path = report_dir / "full-run-evidence.generated.json"
    data = read_json(json_path)
    if data:
        data["final_consistency_audit_report"] = {
            "analysis": REPORT_MD,
            "json": REPORT_JSON,
            "recommended_next_fix_cluster": audit["recommended_next_fix_cluster"]["value"],
            "release_readiness": audit["release_readiness"],
            "full_matrix_summary": audit["full_matrix_summary"],
        }
        reports = data.setdefault("reports", [])
        for path in (REPORT_JSON, REPORT_MD):
            if path not in reports:
                reports.append(path)
        write_json(json_path, data)

    md_path = report_dir / "full-run-evidence.generated.md"
    if md_path.is_file():
        text = read_text_file(md_path)
        section = "\n".join(
            [
                "## Final Consistency Audit",
                f"- Report: `{REPORT_MD}`",
                f"- Recommended next fix cluster: `{audit['recommended_next_fix_cluster']['value']}`",
                f"- Release readiness: `{audit['release_readiness']}`",
                "- This is an audit-only report; Expected statuses and runtime PASS/FAIL values remain unchanged.",
            ]
        )
        updated = replace_marked_section(
            text,
            "<!-- final-consistency-audit:start -->",
            "<!-- final-consistency-audit:end -->",
            section,
        )
        write_text_file(md_path, updated)


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

    audit = build_audit(connector_root, framework_root)
    write_json(output_dir / "final-consistency-audit.generated.json", audit)
    write_text_file(output_dir / "final-consistency-audit.generated.md", render_markdown(audit))
    update_full_run_evidence(output_dir, audit)
    print(output_dir / "final-consistency-audit.generated.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
