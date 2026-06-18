#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
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
    "source": "Fixture hygiene batch start official mismatch report before targeted YAML fix",
    "mismatch_count": 787,
    "critical_mismatch_count": 83,
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
CURRENT_ANALYSIS_CASES = {
    "xml_namespace_edge_connector_gap",
    "xml_request_body_malformed_connector_gap",
    "unicode_whitespace_normalization_gap",
    "unicode_double_encoded_uri_runtime_difference",
    "v2_transformation_url_decode_invalid_sequence_mapped_candidate",
}
REPRESENTATIVE_REPRO_COMMANDS = {
    "xml_namespace_edge_connector_gap": "make verified-case CONNECTOR=nginx CASE=xml_namespace_edge_connector_gap CRS=no-crs MRTS=no-mrts",
    "xml_request_body_malformed_connector_gap": "make verified-case CONNECTOR=nginx CASE=xml_request_body_malformed_connector_gap CRS=no-crs MRTS=no-mrts",
    "unicode_whitespace_normalization_gap": "make verified-case CONNECTOR=nginx CASE=unicode_whitespace_normalization_gap CRS=no-crs MRTS=no-mrts",
    "unicode_double_encoded_uri_runtime_difference": "make verified-case CONNECTOR=nginx CASE=unicode_double_encoded_uri_runtime_difference CRS=no-crs MRTS=no-mrts",
    "v2_transformation_url_decode_invalid_sequence_mapped_candidate": "make verified-case CONNECTOR=haproxy CASE=v2_transformation_url_decode_invalid_sequence_mapped_candidate CRS=no-crs MRTS=no-mrts",
}
CURRENT_TARGETED_ROOT = Path(
    "/var/tmp/ModSecurity-conector-verified/build/xml-unicode-transform-targeted-20260618"
)
VERIFIED_RUN_ROOT = Path(os.environ.get("VERIFIED_RUN_ROOT", "/var/tmp/ModSecurity-conector-verified"))
YAML_FIX_FILES = {
    "modules/ModSecurity-test-Framework/tests/cases/body/json/json_empty_body_future_compatibility.yaml",
    "modules/ModSecurity-test-Framework/tests/cases/response/headers/phase3_response_headers_server_presence_pending.yaml",
    "modules/ModSecurity-test-Framework/tests/cases/response/body/phase4_response_body_empty_future_target.yaml",
    "modules/ModSecurity-test-Framework/tests/cases/transformations/unicode_whitespace_normalization_gap.yaml",
    "modules/ModSecurity-test-Framework/tests/cases/request/uri/v2_transformation_url_decode_invalid_sequence_mapped_candidate.yaml",
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
        "matched_data": data.get("matched_data") or data.get("matched_value_snippet"),
        "matched_variable": data.get("matched_variable"),
        "response_headers_seen": data.get("response_headers_seen"),
        "response_body_seen": data.get("response_body_seen"),
        "request_body_seen": data.get("request_body_seen"),
        "modsecurity_processed": data.get("modsecurity_processed"),
        "reason": data.get("reason"),
        "evidence_file": path,
    }


def runtime_reached_status(item: dict[str, Any]) -> str:
    status = str(item.get("status") or "").lower()
    actual = item.get("actual")
    if status in {"pass", "fail"} or actual is not None:
        return "runtime_reached_actual_match" if status == "pass" else "runtime_reached_actual_mismatch"
    if status == "NOT_EXECUTABLE":
        return "not_reached_not_executable"
    return "unknown"


def latest_case_run(case: str, connector: str, variant: str = "no-crs-no-mrts") -> Path | None:
    runs_root = VERIFIED_RUN_ROOT / "case-runs"
    if not runs_root.is_dir():
        return None
    pattern = f"*-{connector}-{case}-{variant}/case-run.json"
    candidates = sorted(runs_root.glob(pattern))
    return candidates[-1] if candidates else None


def latest_case_run_status(case: str, connector: str) -> dict[str, Any] | None:
    case_run_path = latest_case_run(case, connector)
    if case_run_path is None:
        return None
    case_run = read_json(case_run_path)
    run_dir = case_run_path.parent
    result_path = run_dir / "result.json"
    item = result_status(str(result_path))
    item["case_run"] = str(case_run_path)
    item["full_matrix_refresh_needed"] = bool(case_run.get("full_matrix_refresh_needed", False))
    rule_evidence = case_run.get("rule_evidence")
    if isinstance(rule_evidence, dict):
        item["rule_id"] = item.get("rule_id") or rule_evidence.get("rule_id")
        item["matched_data"] = item.get("matched_data") or rule_evidence.get("matched_data")
        item["matched_variable"] = item.get("matched_variable") or rule_evidence.get("matched_variable")
    item["runtime_classification"] = runtime_reached_status(item)
    return item


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
    clusters = {
        "xml_namespace_edge_connector_gap": "connector_capability_gap / body-processors",
        "xml_request_body_malformed_connector_gap": "expected_status_mismatch / body-processors",
        "unicode_whitespace_normalization_gap": "expected_status_mismatch / transformations",
        "unicode_double_encoded_uri_runtime_difference": "runtime_regression / transformations",
        "v2_transformation_url_decode_invalid_sequence_mapped_candidate": "timeout_or_incomplete / transformations",
    }
    output = []
    for case in sorted(CURRENT_ANALYSIS_CASES):
        for connector in ("apache", "nginx", "haproxy"):
            item = None
            if case == "v2_transformation_url_decode_invalid_sequence_mapped_candidate":
                item = latest_case_run_status(case, connector)
            if item is None:
                result_file = CURRENT_TARGETED_ROOT / "results" / f"{case}-{connector}-result.json"
                item = result_status(str(result_file))
                item["runtime_classification"] = runtime_reached_status(item)
            item.update(
                {
                    "cluster": clusters[case],
                    "case": case,
                    "connector": connector,
                    "variant": "no-crs/no-mrts",
                    "phase": "TARGETED",
                    "log_file": str(CURRENT_TARGETED_ROOT / f"{case}-{connector}.log"),
                }
            )
            if case == "v2_transformation_url_decode_invalid_sequence_mapped_candidate" and item.get("case_run"):
                item["log_file"] = str(Path(str(item["case_run"])).parent / "logs")
            if connector == "haproxy":
                item["decision_log"] = str(CURRENT_TARGETED_ROOT / "results" / f"{case}-haproxy-decision.jsonl")
                if case == "v2_transformation_url_decode_invalid_sequence_mapped_candidate" and item.get("case_run"):
                    item["decision_log"] = str(Path(str(item["case_run"])).parent / "logs")
            output.append(item)
    return output


def native_comparison_status() -> list[dict[str, Any]]:
    rows = []
    for case in sorted(CURRENT_ANALYSIS_CASES):
        if case == "v2_transformation_url_decode_invalid_sequence_mapped_candidate":
            latest = [latest_case_run_status(case, connector) for connector in ("apache", "nginx", "haproxy")]
            if all(item and item.get("runtime_classification") == "runtime_reached_actual_match" for item in latest):
                rows.append(
                    {
                        "case": case,
                        "status": "runtime_reached_actual_match",
                        "evidence": "Targeted connector repros now execute to HTTP 403; native comparison is no longer blocked by fixture syntax.",
                    }
                )
                continue
        rows.append(
            {
                "case": case,
                "status": "native_comparison_missing",
                "evidence": (
                    "Existing reports/testing/generated/mrts-native artifacts cover the MRTS native suite; "
                    "no direct native/libmodsecurity control artifact exists for this framework case."
                ),
            }
        )
    return rows


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
    matrix_refresh_status = full_matrix_refresh_status(connector_root, completeness_path)
    invalid_repros = [
        item
        for item in repros
        if item.get("case") == "v2_transformation_url_decode_invalid_sequence_mapped_candidate"
    ]
    invalid_runtime_reached = (
        len(invalid_repros) == 3
        and all(item.get("runtime_classification") == "runtime_reached_actual_match" for item in invalid_repros)
    )
    decisions = [
        {
            "cluster": "connector_capability_gap / body-processors / xml_namespace_edge_connector_gap",
            "decision": "DOCUMENT",
            "rows": 12,
            "new_classification": "-",
            "native_comparison": "native_comparison_missing",
            "official_after": case_reflection(mismatches, {"xml_namespace_edge_connector_gap"}),
            "full_matrix_refresh_needed": False,
            "evidence": (
                "Targeted Apache, NGINX, and HAProxy no-crs/no-mrts repros all return 200 instead of 403 "
                "with no rule match. HAProxy records modsecurity_processed=true and request_body_seen=true. "
                "The generated rule file contains only SecRule XML and no XML request-body processor "
                "activation, so the best current finding is a test/input fixture gap, not a connector-only bug."
            ),
        },
        {
            "cluster": "expected_status_mismatch / body-processors / xml_request_body_malformed_connector_gap",
            "decision": "DEFER",
            "rows": 12,
            "new_classification": "-",
            "native_comparison": "native_comparison_missing",
            "full_matrix_refresh_needed": False,
            "official_after": case_reflection(mismatches, {"xml_request_body_malformed_connector_gap"}),
            "evidence": (
                "Targeted repros all return 200 instead of 403 with no rule match. The generated rule file "
                "also lacks explicit XML processor activation. Because the body is malformed XML, native "
                "libmodsecurity parser semantics are needed before tightening the fixture or reclassifying."
            ),
        },
        {
            "cluster": "expected_status_mismatch / transformations / unicode_whitespace_normalization_gap",
            "decision": "DEFER",
            "rows": 12,
            "new_classification": "-",
            "native_comparison": "native_comparison_missing",
            "full_matrix_refresh_needed": False,
            "official_after": case_reflection(mismatches, {"unicode_whitespace_normalization_gap"}),
            "evidence": (
                "Targeted repros exercise q=a%E2%80%83b and all connectors return 200 with no rule match. "
                "This suggests either libmodsecurity transformation semantics for t:compressWhitespace and "
                "Unicode spaces or an over-strict framework expectation, but native comparison is missing."
            ),
        },
        {
            "cluster": "runtime_regression / transformations / unicode_double_encoded_uri_runtime_difference",
            "decision": "DEFER",
            "rows": 12,
            "new_classification": "-",
            "native_comparison": "native_comparison_missing",
            "full_matrix_refresh_needed": False,
            "official_after": case_reflection(mismatches, {"unicode_double_encoded_uri_runtime_difference"}),
            "evidence": (
                "Targeted repros send /?q=%25u0063%25u0061%25u0066%25u00E9. Apache, NGINX, and HAProxy "
                "all return 200 with no rule match; HAProxy logs the raw double-encoded URI. No connector "
                "divergence was observed, so native transform comparison is required before reclassification."
            ),
        },
        {
            "cluster": "timeout_or_incomplete / transformations / v2_transformation_url_decode_invalid_sequence_mapped_candidate",
            "decision": "FIX_INPUT_REFRESH_REQUIRED" if invalid_runtime_reached else "DOCUMENT",
            "rows": 12,
            "new_classification": "-",
            "native_comparison": "runtime_reached_actual_match" if invalid_runtime_reached else "not_reached_not_executable",
            "full_matrix_refresh_needed": invalid_runtime_reached and not matrix_refresh_status["fresh"],
            "official_after": case_reflection(mismatches, {"v2_transformation_url_decode_invalid_sequence_mapped_candidate"}),
            "evidence": (
                "The fixture syntax blocker was corrected by removing the former-XFAIL msg action text and "
                "using a parser-safe regex literal for percent (%). Targeted Apache, NGINX, and HAProxy "
                "no-crs/no-mrts repros now reach runtime and return HTTP 403 with rule 4406. Official "
                "Full-Matrix rows remain stale until the affected jobs are rerun."
                if invalid_runtime_reached
                else (
                    "The targeted case is not executable on Apache, NGINX, or HAProxy. Generated config uses "
                    "msg:'former XFAIL invalid urlDecode sequence mapped candidate' and configtest/SPOA parsing "
                    "fails before the request runs. This is a narrow test fixture syntax gap, not runtime evidence "
                    "for t:urlDecode invalid-sequence behavior yet."
                )
            ),
        },
    ]
    for item in decisions:
        case = str(item.get("cluster", "")).split("/")[-1].strip()
        item["repro_command"] = REPRESENTATIVE_REPRO_COMMANDS.get(
            case,
            f"make verified-case CONNECTOR=nginx CASE={case} CRS=no-crs MRTS=no-mrts",
        )
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
        "native_comparison": native_comparison_status(),
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
            item.get("native_comparison", "-"),
            "yes" if item.get("full_matrix_refresh_needed") else "no",
            f"`{item.get('repro_command', '-')}`",
        ]
        for item in payload["decisions"]
    ]
    native_rows = [
        [item["case"], item["status"], item["evidence"]]
        for item in payload["native_comparison"]
    ]
    repro_rows = [
        [
            item["phase"],
            item["cluster"],
            item["case"],
            item["connector"],
            item["variant"],
            item["status"],
            item.get("runtime_classification") or "-",
            item.get("actual") or "-",
            item.get("rule_id") or "-",
            item.get("matched_data") or "-",
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
            md_table(
                [
                    "Cluster",
                    "Decision",
                    "Rows",
                    "New Classification",
                    "Native Comparison",
                    "Full-Matrix Refresh Needed",
                    "Repro",
                ],
                decision_rows,
            ),
            "## Native Comparison",
            md_table(["Case", "Status", "Evidence"], native_rows),
            "## Targeted Repros",
            md_table(
                [
                    "Phase",
                    "Cluster",
                    "Case",
                    "Connector",
                    "Variant",
                    "Status",
                    "Runtime Classification",
                    "Actual",
                    "Rule",
                    "Matched Data",
                    "Evidence",
                ],
                repro_rows,
            ),
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
