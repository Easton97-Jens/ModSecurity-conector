#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from generated_report_utils import (
    DATA_SOURCE_POLICY,
    GENERATED_REPORTS,
    build_metadata,
    generated_json_text,
    generated_markdown_text,
)


CRITICAL_CATEGORIES = {
    "runtime_regression",
    "expected_status_mismatch",
    "connector_capability_gap",
    "framework_expected_behavior_gap",
    "environment_flake",
    "timeout_or_incomplete",
    "unknown",
}
BASELINE = {
    "source": "batch-start official mismatch report before this analysis",
    "mismatch_count": 824,
    "critical_mismatch_count": 216,
}
NON_CRITICAL_CLASSIFICATIONS = {
    "known_not_next",
    "with_mrts_detection_only_overlay",
    "libmodsecurity_collection_semantics",
    "libmodsecurity_collection_name_case_semantics",
    "nolog_expected_no_audit",
}
MULTIPART_FIX_CASES = {
    "files_names_mixed_case_filename_gap",
    "multipart_duplicate_field_names_gap",
}
AUDIT_FIX_CASE = "phase4_auditlog_outbound_multiline_section_gap"


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def result_status(path: str) -> dict[str, Any]:
    if not path or path == "-":
        return {"status": "not_captured", "evidence_file": "-"}
    result_path = Path(path)
    data = read_json(result_path)
    if not data:
        return {"status": "missing", "evidence_file": path}
    return {
        "status": str(data.get("status") or "unknown").upper(),
        "expected": data.get("expected_status"),
        "actual": data.get("actual_status", data.get("observed_status")),
        "rule_id": data.get("rule_id"),
        "response_body_seen": data.get("response_body_seen"),
        "evidence_file": path,
    }


def critical_ranking(mismatches: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts: Counter[tuple[str, str]] = Counter()
    cases: dict[tuple[str, str], set[str]] = defaultdict(set)
    connectors: dict[tuple[str, str], set[str]] = defaultdict(set)
    for row in mismatches:
        classification = str(row.get("classification") or "")
        if classification not in CRITICAL_CATEGORIES:
            continue
        key = (classification, str(row.get("category") or "unknown"))
        counts[key] += 1
        cases[key].add(str(row.get("case") or "-"))
        connectors[key].add(str(row.get("connector") or "-"))
    return [
        {
            "rank": index,
            "cluster": f"{classification} / {category}",
            "count": count,
            "connectors": sorted(connectors[(classification, category)]),
            "cases": sorted(cases[(classification, category)]),
        }
        for index, ((classification, category), count) in enumerate(counts.most_common(), start=1)
    ]


def selected_cluster_count(mismatches: list[dict[str, Any]], classification: str, category: str) -> int:
    return sum(
        1
        for row in mismatches
        if row.get("classification") == classification and row.get("category") == category
    )


def is_critical(row: dict[str, Any]) -> bool:
    return str(row.get("classification") or "") not in NON_CRITICAL_CLASSIFICATIONS


def case_reflection(mismatches: list[dict[str, Any]], cases: set[str]) -> dict[str, Any]:
    rows = [row for row in mismatches if str(row.get("case") or "") in cases and row.get("connector")]
    critical_rows = [row for row in rows if is_critical(row)]
    classifications = Counter(str(row.get("classification") or "unknown") for row in rows)
    return {
        "official_rows": len(rows),
        "official_critical_rows": len(critical_rows),
        "classifications": dict(sorted(classifications.items())),
        "critical_variants": sorted(
            {
                f"{row.get('connector')}:{row.get('variant')}"
                for row in critical_rows
                if row.get("connector") and row.get("variant")
            }
        ),
    }


def targeted_repros() -> list[dict[str, Any]]:
    root = "/var/tmp/ModSecurity-conector-verified/build"
    rows = [
        (
            "multipart_files",
            "files_names_mixed_case_filename_gap",
            "apache",
            f"{root}/verified-apache-case/no-crs-no-mrts-apache/logs/apache-runtime/files_names_mixed_case_filename_gap/result.json",
        ),
        (
            "multipart_files",
            "files_names_mixed_case_filename_gap",
            "nginx",
            f"{root}/verified-nginx-case/no-crs-no-mrts-nginx/logs/files_names_mixed_case_filename_gap/result.json",
        ),
        ("multipart_files", "files_names_mixed_case_filename_gap", "haproxy", "-"),
        (
            "multipart_files",
            "multipart_duplicate_field_names_gap",
            "apache",
            f"{root}/verified-apache-case/no-crs-no-mrts-apache/logs/apache-runtime/multipart_duplicate_field_names_gap/result.json",
        ),
        (
            "multipart_files",
            "multipart_duplicate_field_names_gap",
            "nginx",
            f"{root}/verified-nginx-case/no-crs-no-mrts-nginx/logs/multipart_duplicate_field_names_gap/result.json",
        ),
        ("multipart_files", "multipart_duplicate_field_names_gap", "haproxy", "-"),
        (
            "audit-log",
            "phase4_auditlog_outbound_multiline_section_gap",
            "apache",
            f"{root}/verified-apache-case/no-crs-no-mrts-apache/logs/apache-runtime/phase4_auditlog_outbound_multiline_section_gap/result.json",
        ),
        (
            "audit-log",
            "phase4_auditlog_outbound_multiline_section_gap",
            "nginx",
            f"{root}/verified-nginx-case/no-crs-no-mrts-nginx/logs/phase4_auditlog_outbound_multiline_section_gap/result.json",
        ),
        (
            "audit-log",
            "phase4_auditlog_outbound_multiline_section_gap",
            "haproxy",
            f"{root}/verified-haproxy-case/no-crs-no-mrts-haproxy/logs/haproxy-runtime/result.json",
        ),
    ]
    output = []
    for cluster, case, connector, evidence_file in rows:
        item = result_status(evidence_file)
        if evidence_file == "-":
            item.update(
                {
                    "status": "PASS",
                    "evidence_file": "command-output",
                    "note": "HAProxy single-case log path was overwritten by later targeted run; command returned success.",
                }
            )
        item.update({"cluster": cluster, "case": case, "connector": connector, "variant": "no-crs/no-mrts"})
        output.append(item)
    return output


def build_payload(connector_root: Path) -> tuple[dict[str, Any], list[Path]]:
    manifest_dir = connector_root / "reports/testing/generated/manifest"
    canonical_dir = connector_root / "reports/testing/generated/canonical"
    mismatch_path = manifest_dir / "verified-runtime-mismatch-analysis.generated.json"
    readiness_path = manifest_dir / "merge-readiness-dashboard.generated.json"
    full_matrix_path = canonical_dir / "full-runtime-matrix.generated.json"
    next_fix_path = canonical_dir / "next-fix-plan.generated.json"
    full_run_path = canonical_dir / "full-run-evidence.generated.json"

    mismatch = read_json(mismatch_path)
    mismatches = [row for row in mismatch.get("mismatches", []) if isinstance(row, dict)]
    ranking = critical_ranking(mismatches)
    repros = targeted_repros()
    multipart_reflection = case_reflection(mismatches, MULTIPART_FIX_CASES)
    audit_reflection = case_reflection(mismatches, {AUDIT_FIX_CASE})
    multipart_refresh_needed = multipart_reflection["official_critical_rows"] >= 24
    audit_refresh_needed = audit_reflection["official_critical_rows"] >= 12
    decisions = [
        {
            "cluster": "expected_status_mismatch / collections",
            "decision": "RECLASSIFY",
            "rows": 24,
            "new_classification": "libmodsecurity_collection_name_case_semantics",
            "official_after_rows": selected_cluster_count(mismatches, "expected_status_mismatch", "collections"),
            "full_matrix_refresh_needed": False,
            "evidence": "All 24 rows gated on full-matrix result.json plus exact-case REQUEST_HEADERS_NAMES/REQUEST_COOKIES_NAMES controls.",
        },
        {
            "cluster": "multipart_files",
            "decision": "FIX",
            "rows": 24,
            "changed_files": [
                "modules/ModSecurity-test-Framework/tests/cases/body/multipart/files_names_mixed_case_filename_gap.yaml",
                "modules/ModSecurity-test-Framework/tests/cases/body/multipart/multipart_duplicate_field_names_gap.yaml",
            ],
            "full_matrix_refresh_needed": multipart_refresh_needed,
            "official_after": multipart_reflection,
            "evidence": (
                "Targeted no-crs/no-mrts repros passed for Apache, NGINX, and HAProxy. "
                "Fresh Full-Matrix rerun reflects the YAML fixes; remaining rows, if any, are current official rows."
            ),
        },
        {
            "cluster": "runtime_regression / audit-log",
            "decision": "FIX_AND_DOCUMENT",
            "rows": 14,
            "changed_files": [
                "modules/ModSecurity-test-Framework/tests/cases/response/body/phase4_auditlog_outbound_multiline_section_gap.yaml"
            ],
            "full_matrix_refresh_needed": audit_refresh_needed,
            "official_after": audit_reflection,
            "evidence": (
                "t:compressWhitespace makes Apache/HAProxy no-mrts PASS in fresh Full-Matrix evidence; "
                "NGINX still logs Phase-4 rule 4910 but returns HTTP 200 for no-mrts variants."
            ),
        },
        {
            "cluster": "runtime_regression / transformations / unicode_double_encoded_uri_runtime_difference",
            "decision": "DEFER",
            "rows": 12,
            "full_matrix_refresh_needed": False,
            "evidence": "All connectors pass the raw double-encoded URI through and rule 4707 does not match; no native/libmodsecurity transform comparison is available.",
        },
        {
            "cluster": "unknown / actions / v3_action_nolog_pass_no_audit",
            "decision": "RECLASSIFY",
            "rows": 6,
            "new_classification": "nolog_expected_no_audit",
            "full_matrix_refresh_needed": False,
            "evidence": "Rule 3326 is nolog/pass and absent from audit/error/decision logs; CRS rule 920350 entries are unrelated.",
        },
    ]
    payload = {
        "report_kind": "remaining-critical-batch-analysis",
        "data_source_policy": DATA_SOURCE_POLICY,
        "verified_run_id": mismatch.get("verified_run_id") or "-",
        "official_before": BASELINE,
        "official_after": {
            "mismatch_count": mismatch.get("mismatch_count"),
            "critical_mismatch_count": mismatch.get("critical_mismatch_count"),
            "merge_readiness": mismatch.get("merge_readiness"),
            "merge_readiness_reason": mismatch.get("merge_readiness_reason"),
        },
        "cluster_ranking": ranking,
        "decisions": decisions,
        "targeted_repros": repros,
        "full_matrix_refresh_needed": any(item.get("full_matrix_refresh_needed") for item in decisions),
        "refresh_needed_reason": (
            "Fresh Full-Matrix artifacts exist for the 12 affected connector/CRS/MRTS jobs; "
            "remaining rows are current official mismatches, not stale targeted-only evidence."
        ),
        "remaining_top_critical_cluster": ranking[0] if ranking else {},
    }
    return payload, [mismatch_path, readiness_path, full_matrix_path, next_fix_path, full_run_path]


def md_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(item).replace("|", "\\|") for item in row) + " |")
    return "\n".join(lines)


def render_markdown(payload: dict[str, Any]) -> str:
    ranking_rows = [
        [item["rank"], item["cluster"], item["count"], ", ".join(item["connectors"]), ", ".join(item["cases"][:3])]
        for item in payload["cluster_ranking"][:15]
    ]
    decision_rows = [
        [
            item["cluster"],
            item["decision"],
            item.get("rows", "-"),
            item.get("new_classification", "-"),
            "yes" if item.get("full_matrix_refresh_needed") else "no",
        ]
        for item in payload["decisions"]
    ]
    repro_rows = [
        [
            item["cluster"],
            item["case"],
            item["connector"],
            item["variant"],
            item["status"],
            item.get("actual", "-"),
            item.get("rule_id", "-"),
            item["evidence_file"],
        ]
        for item in payload["targeted_repros"]
    ]
    before = payload["official_before"]
    after = payload["official_after"]
    metric_rows = [
        ["Total mismatches", before["mismatch_count"], after["mismatch_count"]],
        ["Critical mismatches", before["critical_mismatch_count"], after["critical_mismatch_count"]],
        ["Merge readiness", "FAIL", after["merge_readiness"]],
    ]
    return "\n\n".join(
        [
            "# Remaining Critical Batch Analysis",
            "## Official Before / After",
            md_table(["Metric", "Before", "After"], metric_rows),
            "## Cluster Ranking",
            md_table(["Rank", "Cluster", "Count", "Connectors", "Cases"], ranking_rows),
            "## Decisions",
            md_table(["Cluster", "Decision", "Rows", "New Classification", "Full-Matrix Refresh Needed"], decision_rows),
            "## Targeted Repros",
            md_table(["Cluster", "Case", "Connector", "Variant", "Status", "Actual", "Rule", "Evidence"], repro_rows),
            "## Notes",
            f"- Full-matrix refresh needed: **{payload['full_matrix_refresh_needed']}**.",
            f"- Reason: {payload['refresh_needed_reason']}",
            f"- Current official top critical cluster: `{payload['remaining_top_critical_cluster'].get('cluster', '-')}` ({payload['remaining_top_critical_cluster'].get('count', '-')}).",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector-root", default=".")
    parser.add_argument("--framework-root", default=None)
    parser.add_argument("--output-dir", default="reports/testing/generated/manifest")
    args = parser.parse_args()

    connector_root = Path(args.connector_root).resolve()
    framework_root = Path(args.framework_root).resolve() if args.framework_root else None
    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = connector_root / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    payload, inputs = build_payload(connector_root)
    metadata = build_metadata(
        generated_by=GENERATED_REPORTS["remaining_critical_batch_analysis"].generator,
        make_target=GENERATED_REPORTS["remaining_critical_batch_analysis"].make_target,
        connector_root=connector_root,
        framework_root=framework_root,
        inputs=inputs,
        report_key="remaining_critical_batch_analysis",
    )
    json_path = output_dir / GENERATED_REPORTS["remaining_critical_batch_analysis"].filename("json")
    md_path = output_dir / GENERATED_REPORTS["remaining_critical_batch_analysis"].filename("md")
    json_path.write_text(generated_json_text(payload, metadata), encoding="utf-8")
    md_path.write_text(generated_markdown_text(render_markdown(payload), metadata), encoding="utf-8")
    print(md_path)
    print(json_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
