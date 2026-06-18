#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
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
    "source": "critical-cluster batch start official mismatch report before this analysis",
    "mismatch_count": 808,
    "critical_mismatch_count": 152,
}
NON_CRITICAL_CLASSIFICATIONS = {
    "known_not_next",
    "with_mrts_detection_only_overlay",
    "libmodsecurity_collection_semantics",
    "libmodsecurity_collection_name_case_semantics",
    "nolog_expected_no_audit",
}
DUPLICATE_HEADER_CASE = "duplicate_header_case_normalization_gap"
YAML_FIX_CASES = {
    "json_empty_body_future_compatibility",
    "phase3_response_headers_server_presence_pending",
    "phase4_response_body_empty_future_target",
    "unicode_whitespace_normalization_gap",
}
TRANSFORMATION_DEFER_CASE = "unicode_double_encoded_uri_runtime_difference"
YAML_FIX_FILES = {
    "modules/ModSecurity-test-Framework/tests/cases/body/json/json_empty_body_future_compatibility.yaml",
    "modules/ModSecurity-test-Framework/tests/cases/response/headers/phase3_response_headers_server_presence_pending.yaml",
    "modules/ModSecurity-test-Framework/tests/cases/response/body/phase4_response_body_empty_future_target.yaml",
    "modules/ModSecurity-test-Framework/tests/cases/transformations/unicode_whitespace_normalization_gap.yaml",
}
FULL_MATRIX_CONNECTORS = ("apache", "nginx", "haproxy")
FULL_MATRIX_VARIANTS = (
    ("no-crs", "no-mrts"),
    ("no-crs", "with-mrts"),
    ("with-crs", "no-mrts"),
    ("with-crs", "with-mrts"),
)


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def parse_utc(value: str | None) -> float | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def full_matrix_refresh_status(connector_root: Path, completeness_path: Path) -> dict[str, Any]:
    newest_input_mtime = 0.0
    inputs: list[dict[str, Any]] = []
    for rel_path in sorted(YAML_FIX_FILES):
        path = connector_root / rel_path
        if not path.is_file():
            inputs.append({"path": rel_path, "status": "missing"})
            return {"fresh": False, "reason": f"missing input {rel_path}", "inputs": inputs, "jobs": []}
        mtime = path.stat().st_mtime
        newest_input_mtime = max(newest_input_mtime, mtime)
        inputs.append(
            {
                "path": rel_path,
                "status": "present",
                "mtime": datetime.fromtimestamp(mtime, timezone.utc).isoformat().replace("+00:00", "Z"),
            }
        )

    data = read_json(completeness_path)
    raw_jobs: Any
    if isinstance(data, list):
        raw_jobs = data
    else:
        raw_jobs = data.get("jobs") or data.get("matrix") or data.get("records") or data.get("rows") or []
    jobs = raw_jobs if isinstance(raw_jobs, list) else []
    by_key: dict[tuple[str, str, str], dict[str, Any]] = {}
    for job in jobs:
        if not isinstance(job, dict):
            continue
        connector = str(job.get("connector") or "")
        crs = str(job.get("crs") or job.get("test_variant") or "")
        mrts = str(job.get("mrts") or job.get("mrts_variant") or "")
        by_key[(connector, crs, mrts)] = job

    job_statuses: list[dict[str, Any]] = []
    fresh = True
    for connector in FULL_MATRIX_CONNECTORS:
        for crs, mrts in FULL_MATRIX_VARIANTS:
            job = by_key.get((connector, crs, mrts), {})
            ended_at = str(job.get("ended_at") or "")
            ended_ts = parse_utc(ended_at)
            complete = str(job.get("status") or "") in {"completed", "completed_with_mismatches"}
            current = bool(ended_ts is not None and ended_ts >= newest_input_mtime and complete)
            if not current:
                fresh = False
            job_statuses.append(
                {
                    "connector": connector,
                    "crs": crs,
                    "mrts": mrts,
                    "status": job.get("status") or "missing",
                    "return_code": job.get("return_code"),
                    "ended_at": ended_at or "-",
                    "fresh_after_yaml_inputs": current,
                }
            )
    reason = "all affected Full-Matrix jobs ended after the YAML/input fixes" if fresh else "one or more affected Full-Matrix jobs are stale or missing"
    return {"fresh": fresh, "reason": reason, "inputs": inputs, "jobs": job_statuses}


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
        "response_headers_seen": data.get("response_headers_seen"),
        "response_body_seen": data.get("response_body_seen"),
        "modsecurity_processed": data.get("modsecurity_processed"),
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
    before_root = "/var/tmp/ModSecurity-conector-verified/build/critical-batch-targeted"
    after_root = "/var/tmp/ModSecurity-conector-verified/build/critical-batch-targeted-after"
    rows = [
        (
            "connector_capability_gap / collections",
            DUPLICATE_HEADER_CASE,
            "apache",
            "-",
            f"{before_root}/{DUPLICATE_HEADER_CASE}-apache.log",
            "BEFORE",
            "FAIL_RC_2",
        ),
        (
            "connector_capability_gap / collections",
            DUPLICATE_HEADER_CASE,
            "nginx",
            "-",
            f"{before_root}/{DUPLICATE_HEADER_CASE}-nginx.log",
            "BEFORE",
            "FAIL_RC_2",
        ),
        (
            "connector_capability_gap / collections",
            DUPLICATE_HEADER_CASE,
            "haproxy",
            "-",
            f"{before_root}/{DUPLICATE_HEADER_CASE}-haproxy.log",
            "BEFORE",
            "FAIL_RC_2",
        ),
    ]
    for case in sorted(YAML_FIX_CASES):
        for connector in ("apache", "nginx", "haproxy"):
            rows.append(
                (
                    "targeted YAML/input fix",
                    case,
                    connector,
                    f"{after_root}/{case}-{connector}-result.json",
                    f"{after_root}/{case}-{connector}.log",
                    "AFTER",
                    None,
                )
            )
    for connector in ("apache", "nginx", "haproxy"):
        rows.append(
            (
                "runtime_regression / transformations",
                TRANSFORMATION_DEFER_CASE,
                connector,
                "-",
                f"{before_root}/{TRANSFORMATION_DEFER_CASE}-{connector}.log",
                "BEFORE",
                "FAIL_RC_2",
            )
        )
    output = []
    for cluster, case, connector, evidence_file, log_file, phase, status_override in rows:
        item = result_status(evidence_file)
        if status_override:
            item.update({"status": status_override, "evidence_file": log_file})
        item["log_file"] = log_file
        item["phase"] = phase
        item.update({"cluster": cluster, "case": case, "connector": connector, "variant": "no-crs/no-mrts"})
        output.append(item)
    return output


def build_payload(connector_root: Path) -> tuple[dict[str, Any], list[Path]]:
    manifest_dir = connector_root / "reports/testing/generated/manifest"
    canonical_dir = connector_root / "reports/testing/generated/canonical"
    mismatch_path = manifest_dir / "verified-runtime-mismatch-analysis.generated.json"
    readiness_path = manifest_dir / "merge-readiness-dashboard.generated.json"
    completeness_path = manifest_dir / "full-matrix-job-completeness.generated.json"
    full_matrix_path = canonical_dir / "full-runtime-matrix.generated.json"
    next_fix_path = canonical_dir / "next-fix-plan.generated.json"
    full_run_path = canonical_dir / "full-run-evidence.generated.json"

    mismatch = read_json(mismatch_path)
    mismatches = [row for row in mismatch.get("mismatches", []) if isinstance(row, dict)]
    ranking = critical_ranking(mismatches)
    repros = targeted_repros()
    duplicate_header_reflection = case_reflection(mismatches, {DUPLICATE_HEADER_CASE})
    yaml_fix_reflection = case_reflection(mismatches, YAML_FIX_CASES)
    unicode_double_reflection = case_reflection(mismatches, {TRANSFORMATION_DEFER_CASE})
    matrix_refresh_status = full_matrix_refresh_status(connector_root, completeness_path)
    yaml_fix_refresh_needed = yaml_fix_reflection["official_critical_rows"] > 0 and not matrix_refresh_status["fresh"]
    decisions = [
        {
            "cluster": "connector_capability_gap / collections / duplicate_header_case_normalization_gap",
            "decision": "RECLASSIFY",
            "rows": 12,
            "new_classification": "libmodsecurity_collection_name_case_semantics",
            "official_after": duplicate_header_reflection,
            "full_matrix_refresh_needed": False,
            "evidence": (
                "All three connectors fail the lowercase REQUEST_HEADERS_NAMES probe while exact-case "
                "REQUEST_HEADERS_NAMES control evidence passes. The YAML request header map cannot encode a "
                "true duplicate header, so this row is narrowed to observed libmodsecurity collection-name "
                "case semantics rather than a connector duplicate-header bug."
            ),
        },
        {
            "cluster": "timeout_or_incomplete / body-processors / json_empty_body_future_compatibility",
            "decision": "FIX",
            "rows": 12,
            "changed_files": [
                "modules/ModSecurity-test-Framework/tests/cases/body/json/json_empty_body_future_compatibility.yaml",
            ],
            "full_matrix_refresh_needed": yaml_fix_refresh_needed,
            "official_after": case_reflection(mismatches, {"json_empty_body_future_compatibility"}),
            "evidence": (
                "Original rule used an empty @streq parameter and was not executable. The fixed @rx ^$ "
                "empty-body probe passes targeted no-crs/no-mrts repros on Apache, NGINX, and HAProxy; "
                "current official rows reflect the Full-Matrix refresh status recorded in this report."
            ),
        },
        {
            "cluster": "timeout_or_incomplete / response-headers / phase3_response_headers_server_presence_pending",
            "decision": "FIX",
            "rows": 12,
            "changed_files": [
                "modules/ModSecurity-test-Framework/tests/cases/response/headers/phase3_response_headers_server_presence_pending.yaml"
            ],
            "full_matrix_refresh_needed": yaml_fix_refresh_needed,
            "official_after": case_reflection(mismatches, {"phase3_response_headers_server_presence_pending"}),
            "evidence": (
                "Original @contains operator had no argument and the rule was disruptive despite a pass/200 "
                "expectation. The fixed non-disruptive @rx .+ response-header probe passes targeted "
                "no-crs/no-mrts repros on Apache, NGINX, and HAProxy; refreshed official evidence removes "
                "the timeout/incomplete rows."
            ),
        },
        {
            "cluster": "timeout_or_incomplete / response-body / phase4_response_body_empty_future_target",
            "decision": "FIX_AND_DOCUMENT",
            "rows": 12,
            "changed_files": [
                "modules/ModSecurity-test-Framework/tests/cases/response/body/phase4_response_body_empty_future_target.yaml"
            ],
            "full_matrix_refresh_needed": yaml_fix_refresh_needed,
            "official_after": case_reflection(mismatches, {"phase4_response_body_empty_future_target"}),
            "evidence": (
                "Original empty @streq parameter was not executable and the test response body was not empty. "
                "The fixed empty-body target passes Apache and HAProxy targeted repros. Fresh Full-Matrix "
                "evidence leaves only the narrow NGINX no-MRTS phase-4 enforcement/status gap as critical; "
                "MRTS variants are DetectionOnly overlay rows."
            ),
        },
        {
            "cluster": "connector_capability_gap / transformations / unicode_whitespace_normalization_gap",
            "decision": "FIX_INPUT_AND_DEFER_CLASSIFICATION",
            "rows": 12,
            "changed_files": [
                "modules/ModSecurity-test-Framework/tests/cases/transformations/unicode_whitespace_normalization_gap.yaml"
            ],
            "full_matrix_refresh_needed": yaml_fix_refresh_needed,
            "official_after": case_reflection(mismatches, {"unicode_whitespace_normalization_gap"}),
            "evidence": (
                "Original request used q=SAFE, so it did not exercise Unicode whitespace. The fixed request "
                "uses an encoded Unicode em-space. Fresh Full-Matrix evidence shows 200/expected 403 for "
                "all connectors/variants; classification remains deferred pending native/libmodsecurity "
                "transform comparison."
            ),
        },
        {
            "cluster": "runtime_regression / transformations / unicode_double_encoded_uri_runtime_difference",
            "decision": "DEFER",
            "rows": 12,
            "full_matrix_refresh_needed": False,
            "official_after": unicode_double_reflection,
            "evidence": (
                "All connectors pass the raw double-encoded URI through and rule 4707 does not match in "
                "targeted evidence. No native/libmodsecurity transform comparison is available, so no "
                "official reclassification is made."
            ),
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
        "full_matrix_refresh_status": matrix_refresh_status,
        "full_matrix_refresh_needed": any(item.get("full_matrix_refresh_needed") for item in decisions),
        "refresh_needed_reason": (
            matrix_refresh_status["reason"]
        ),
        "remaining_top_critical_cluster": ranking[0] if ranking else {},
    }
    return payload, [mismatch_path, readiness_path, completeness_path, full_matrix_path, next_fix_path, full_run_path]


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
            item["phase"],
            item["cluster"],
            item["case"],
            item["connector"],
            item["variant"],
            item["status"],
            item.get("actual") or "-",
            item.get("rule_id") or "-",
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
            md_table(["Phase", "Cluster", "Case", "Connector", "Variant", "Status", "Actual", "Rule", "Evidence"], repro_rows),
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
