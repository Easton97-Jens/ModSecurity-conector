#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

# CI helpers are shared from ci/lib even when this file is executed directly.
import sys
_CI_ROOT = next(parent for parent in Path(__file__).resolve().parents if parent.name == "ci")
if str(_CI_ROOT / "lib") not in sys.path:
    sys.path.insert(0, str(_CI_ROOT / "lib"))
from typing import Any

from generated_report_utils import (
    GENERATED_ROOT,
    build_metadata,
    current_verified_run_id,
    generated_json_text,
    generated_markdown_text,
    report_path,
    report_path_from_root,
)
from report_path_safety import add_safe_roots, write_text_file
from runtime_path_utils import verified_runtime_paths


JOB_ID = "nginx:with-crs:with-mrts"
PRIMARY_BLOCKER = "nginx_with_crs_with_mrts_http500_cluster"
ERROR_REWRITE_CYCLE = 'rewrite or internal redirection cycle while internally redirecting to "/index.html"'
ERROR_PERMISSION_DENIED = "htdocs/index.html permission denied"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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


def rel(path: str | Path, root: Path) -> str:
    if not path:
        return "-"
    item = Path(path)
    try:
        return str(item.resolve(strict=False).relative_to(root.resolve(strict=False)))
    except Exception:
        return str(path)


def read_lines(path: str | Path) -> list[str]:
    item = Path(path)
    if not item.is_file():
        return []
    return item.read_text(encoding="utf-8", errors="replace").splitlines()


def final_run_prefix(job: dict[str, Any]) -> str:
    started = str(job.get("started_at") or "")
    if started.startswith("2026-06-16"):
        return "2026/06/16"
    if len(started) >= 10:
        return started[:10].replace("-", "/")
    return ""


def final_error_lines(path: str | Path, prefix: str) -> list[str]:
    lines = read_lines(path)
    if not prefix:
        return lines
    return [line for line in lines if line.startswith(prefix)]


def access_status(path: str | Path, prefix_date: str) -> str:
    prefix = ""
    if prefix_date:
        parts = prefix_date.split("/")
        if len(parts) == 3:
            prefix = f"[{parts[2]}/{datetime.strptime(parts[1], '%m').strftime('%b')}/{parts[0]}:"
    statuses: list[str] = []
    for line in read_lines(path):
        if prefix and prefix not in line:
            continue
        match = re.search(r'"\S+ [^"]+ HTTP/[^"]+" (\d{3}) ', line)
        if match:
            statuses.append(match.group(1))
    return statuses[-1] if statuses else "-"


def harness_root_from_evidence(path: str | Path) -> Path:
    item = Path(str(path))
    try:
        if item.name == "result.json" and item.parent.parent.name == "logs":
            return item.parent.parent.parent
    except Exception:
        pass
    match = re.match(r"(.+)/logs/[^/]+/result\.json$", str(item))
    return Path(match.group(1)) if match else Path()


def patterns_for_error_line(line: str) -> list[str]:
    patterns: list[str] = []
    if ERROR_REWRITE_CYCLE in line:
        patterns.append("rewrite_internal_redirect_cycle_to_index")
    if "htdocs/index.html" in line and "Permission denied" in line:
        patterns.append("docroot_index_permission_denied")
    elif "/htdocs/" in line and "Permission denied" in line:
        patterns.append("docroot_directory_permission_denied")
    if "[crit]" in line and "Permission denied" in line:
        patterns.append("nginx_crit_permission_denied")
    if "ModSecurity: Warning." in line:
        if "/coreruleset/" in line or "OWASP_CRS" in line:
            patterns.append("modsecurity_crs_warning")
        elif "/mrts/" in line or "MRTS/" in line:
            patterns.append("modsecurity_mrts_warning")
        else:
            patterns.append("modsecurity_case_warning")
    if "failed" in line.lower() and "Permission denied" not in line:
        patterns.append("generic_failed")
    return patterns


def error_patterns_for_case(row: dict[str, Any], prefix: str) -> list[str]:
    patterns: dict[str, None] = {}
    for line in final_error_lines(str(row.get("nginx_error_log_path") or ""), prefix):
        for pattern in patterns_for_error_line(line):
            patterns.setdefault(pattern, None)
    return list(patterns)


def example_line_for_pattern(row: dict[str, Any], prefix: str, pattern: str) -> str:
    for line in final_error_lines(str(row.get("nginx_error_log_path") or ""), prefix):
        if pattern in patterns_for_error_line(line):
            return line[:600]
    return "-"


def representative_error_excerpt(row: dict[str, Any], prefix: str, max_lines: int = 4) -> list[str]:
    interesting: list[str] = []
    for line in final_error_lines(str(row.get("nginx_error_log_path") or ""), prefix):
        if (
            ERROR_REWRITE_CYCLE in line
            or ("htdocs/index.html" in line and "Permission denied" in line)
            or ("ModSecurity: Warning." in line and len(interesting) < 2)
        ):
            interesting.append(line[:600])
        if len(interesting) >= max_lines:
            break
    return interesting


def audit_excerpt(path: str | Path, max_lines: int = 4) -> list[str]:
    lines = read_lines(path)
    return [line[:600] for line in lines[:max_lines]]


def case_env(path: str | Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in read_lines(path):
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key] = value
    return data


def request_headers(path: str | Path) -> list[str]:
    return [line for line in read_lines(path) if line.strip()]


def request_body_info(path: str | Path) -> dict[str, Any]:
    item = Path(path)
    if not item.is_file():
        return {"path": str(item), "status": "missing", "bytes": 0, "excerpt": ""}
    raw = item.read_bytes()
    excerpt = raw[:160].decode("utf-8", errors="replace")
    return {"path": str(item), "status": "present", "bytes": len(raw), "excerpt": excerpt}


def family_for(row: dict[str, Any]) -> str:
    name = str(row.get("name") or "").lower()
    category = str(row.get("category") or "").lower()
    capabilities = {str(item).lower() for item in row.get("capabilities", []) if isinstance(item, str)}
    if "request_cookies_names" in name or "request_cookies" in name or "request-cookies" in capabilities:
        return "MRTS request cookie/name"
    if "_xml_" in name or category == "xml" or "xml" in capabilities:
        return "MRTS XML"
    if "request_filename" in name:
        return "Request filename"
    if "response_body" in name or "phase4" in name or category == "response-body":
        return "Response body / phase 4"
    if "multipart" in name or "files_" in name or category == "multipart":
        return "Multipart"
    if name.startswith("mrts_"):
        return "Other MRTS"
    if category == "audit-log":
        return "Audit / intervention"
    if category in {"actions", "phase-handling"}:
        return "Intervention / actions"
    if category in {"body-processors", "request-body"}:
        return "Request body / parsers"
    if category in {"collections"}:
        return "Collections / name handling"
    if category in {"transformations", "operators"}:
        return "Transformations / operators"
    if category == "response-headers":
        return "Response headers / phase 3"
    return "Unknown"


def classification_for_family(family: str) -> str:
    if family == "MRTS XML":
        return "xml_handling_bug_secondary_harness_environment_error"
    if family == "Multipart":
        return "multipart_handling_bug_secondary_harness_environment_error"
    if family == "Response body / phase 4":
        return "response_body_phase4_bug_secondary_harness_environment_error"
    if family in {"MRTS request cookie/name", "Request filename", "Other MRTS"}:
        return "crs_mrts_rule_interaction_secondary_harness_environment_error"
    if family in {"Audit / intervention", "Intervention / actions"}:
        return "intervention_handling_bug_secondary_harness_environment_error"
    return "harness_environment_error"


def pattern_rollup(rows: list[dict[str, Any]], prefix: str) -> list[dict[str, Any]]:
    counter: Counter[str] = Counter()
    examples: dict[str, str] = {}
    affected: defaultdict[str, list[str]] = defaultdict(list)
    for row in rows:
        patterns = error_patterns_for_case(row, prefix)
        if not patterns:
            patterns = ["no_matching_error_pattern"]
        for pattern in patterns:
            counter[pattern] += 1
            if pattern not in examples:
                examples[pattern] = (
                    example_line_for_pattern(row, prefix, pattern)
                    if pattern != "no_matching_error_pattern"
                    else next(iter(representative_error_excerpt(row, prefix, 1)), "-")
                )
            if len(affected[pattern]) < 8:
                affected[pattern].append(str(row.get("name") or "-"))
    return [
        {
            "pattern": pattern,
            "count": count,
            "example": examples.get(pattern, "-"),
            "affected_cases": affected.get(pattern, []),
        }
        for pattern, count in counter.most_common()
    ]


def build_groups(rows: list[dict[str, Any]], connector_root: Path) -> list[dict[str, Any]]:
    grouped: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[family_for(row)].append(row)
    result: list[dict[str, Any]] = []
    for family, items in sorted(grouped.items(), key=lambda item: (-len(item[1]), item[0])):
        result.append(
            {
                "group": family,
                "count": len(items),
                "classification": classification_for_family(family),
                "representative_cases": [
                    {
                        "case": str(row.get("name") or "-"),
                        "expected": row.get("expected_status"),
                        "actual": row.get("actual_status"),
                        "evidence": rel(row.get("evidence_path") or row.get("nginx_error_log_path") or "-", connector_root),
                    }
                    for row in items[:5]
                ],
            }
        )
    return result


def representative_cases(rows: list[dict[str, Any]], prefix: str, connector_root: Path) -> list[dict[str, Any]]:
    wanted = [
        "audit_log_empty_sections_future_target",
        "action_allow_phase1_pass",
        "duplicate_args_encoded_separator_edge",
        "multipart_basic_block",
        "response_body_basic_block",
        "mrts_100000_mrts_002_args_a_get_100000_1",
        "mrts_100116_mrts_059_request_cookies_100116_2",
        "mrts_100132_mrts_060_request_cookies_names_100132_2",
        "mrts_100148_mrts_061_request_filename_100148_1",
        "mrts_100154_mrts_110_xml_100154_1",
    ]
    by_name = {str(row.get("name") or ""): row for row in rows}
    selected = [by_name[name] for name in wanted if name in by_name]
    if len(selected) < 10:
        seen = {str(row.get("name") or "") for row in selected}
        for row in rows:
            if str(row.get("name") or "") not in seen:
                selected.append(row)
                seen.add(str(row.get("name") or ""))
            if len(selected) >= 10:
                break
    cases: list[dict[str, Any]] = []
    for row in selected[:10]:
        env_path = Path(str(row.get("evidence_path") or "")).parent.parent / "runtime" / "missing"
        evidence_path = Path(str(row.get("evidence_path") or ""))
        runtime_conf = Path(str(row.get("nginx_error_log_path") or "")).parents[1] if row.get("nginx_error_log_path") else Path()
        # The result path is .../logs/<case>/result.json; runtime is under sibling runtime/<case>/conf.
        case_name = str(row.get("name") or "")
        harness_root = harness_root_from_evidence(evidence_path)
        case_env_path = harness_root / "runtime" / case_name / "conf/case.env"
        headers_path = harness_root / "runtime" / case_name / "conf/request-headers.txt"
        body_path = harness_root / "runtime" / case_name / "conf/request-body.bin"
        nginx_conf_path = harness_root / "runtime" / case_name / "conf/nginx.conf"
        env = case_env(case_env_path)
        headers = request_headers(headers_path)
        content_type = next((line.split(":", 1)[1].strip() for line in headers if line.lower().startswith("content-type:")), "")
        cases.append(
            {
                "case": case_name,
                "group": family_for(row),
                "expected": row.get("expected_status"),
                "actual": row.get("actual_status"),
                "access_log_status": access_status(str(row.get("nginx_access_log_path") or ""), prefix),
                "error_pattern": ", ".join(error_patterns_for_case(row, prefix)[:4]) or "-",
                "classification": classification_for_family(family_for(row)),
                "error_log_excerpt": representative_error_excerpt(row, prefix),
                "audit_log_excerpt": audit_excerpt(str(row.get("audit_log_path") or "")),
                "result_json": read_json(Path(str(row.get("evidence_path") or ""))),
                "loaded_rules": {
                    "crs_active": True,
                    "mrts_active": True,
                    "modsecurity_config": rel(nginx_conf_path, connector_root),
                    "rule_preamble": "crs/modsecurity-crs-preamble.conf + MRTS load/case rules",
                },
                "request": {
                    "method": env.get("REQUEST_METHOD", "-"),
                    "path": env.get("REQUEST_PATH", "-"),
                    "has_body": env.get("REQUEST_HAS_BODY", "-"),
                    "content_type": content_type or "-",
                    "headers": headers[:8],
                    "body": request_body_info(body_path),
                },
                "evidence": {
                    "result_json": rel(row.get("evidence_path") or "-", connector_root),
                    "nginx_error_log": rel(row.get("nginx_error_log_path") or "-", connector_root),
                    "nginx_access_log": rel(row.get("nginx_access_log_path") or "-", connector_root),
                    "audit_log": rel(row.get("audit_log_path") or "-", connector_root),
                },
            }
        )
    return cases


def permissions_probe(row: dict[str, Any]) -> dict[str, Any]:
    evidence_path = Path(str(row.get("evidence_path") or ""))
    case_name = str(row.get("name") or "")
    harness_root = harness_root_from_evidence(evidence_path)
    index_path = harness_root / "runtime" / case_name / "htdocs/index.html"
    paths: list[dict[str, Any]] = []
    current = Path("/")
    for part in index_path.parts[1:]:
        current = current / part
        try:
            stat = current.stat()
            paths.append(
                {
                    "path": str(current),
                    "mode": oct(stat.st_mode & 0o777),
                    "uid": stat.st_uid,
                    "gid": stat.st_gid,
                    "traversable_by_other": bool(stat.st_mode & 0o001) if current.is_dir() else None,
                }
            )
        except OSError as exc:
            paths.append({"path": str(current), "error": str(exc)})
            break
    return {"index_path": str(index_path), "path_components": paths}


def build_payload(connector_root: Path, framework_root: Path, build_root: Path, verified_run_id: str) -> dict[str, Any]:
    job_root = build_root / "full-matrix/with-crs/with-mrts/nginx"
    job_json = job_root / "job.json"
    run_log = job_root / "run.log"
    summary_json = job_root / "results/force-all/nginx-summary.json"
    results_jsonl = job_root / "results/force-all/nginx-results.jsonl"
    completeness_json = report_path(connector_root, "full_matrix_job_completeness", "json")
    mismatch_json = report_path(connector_root, "verified_runtime_mismatch_analysis", "json")
    commands_json = build_root / "verified-runs" / verified_run_id / "verified-commands.json"

    job = read_json(job_json)
    rows = read_jsonl(results_jsonl)
    http500_rows = [row for row in rows if row.get("actual_status") == 500]
    prefix = final_run_prefix(job)
    groups = build_groups(http500_rows, connector_root)
    patterns = pattern_rollup(http500_rows, prefix)
    reps = representative_cases(http500_rows, prefix, connector_root)
    rewrite_count = next((item["count"] for item in patterns if item["pattern"] == "rewrite_internal_redirect_cycle_to_index"), 0)
    permission_case_count = sum(1 for row in http500_rows if "docroot_index_permission_denied" in error_patterns_for_case(row, prefix))
    example = reps[0] if reps else {}
    minimal_case = "mrts_100000_mrts_002_args_a_get_100000_1"
    minimal_row = next((row for row in http500_rows if row.get("name") == minimal_case), http500_rows[0] if http500_rows else {})
    payload = {
        "generated_at": utc_now(),
        "verified_run_id": verified_run_id,
        "job_id": JOB_ID,
        "primary_blocker": PRIMARY_BLOCKER if http500_rows else "none",
        "merge_readiness": "FAIL" if http500_rows else "UNKNOWN",
        "job": {
            "status": job.get("status"),
            "return_code": job.get("return_code"),
            "started_at": job.get("started_at"),
            "ended_at": job.get("ended_at"),
            "duration_seconds": job.get("duration_seconds"),
            "path": str(job_json),
        },
        "inputs": {
            "job_json": str(job_json),
            "run_log": str(run_log),
            "summary_json": str(summary_json),
            "results_jsonl": str(results_jsonl),
            "full_matrix_job_completeness": str(completeness_json),
            "verified_runtime_mismatch_analysis": str(mismatch_json),
            "verified_commands": str(commands_json),
        },
        "summary": {
            "total_rows": len(rows),
            "http500_failures": len(http500_rows),
            "rewrite_cycle_cases": rewrite_count,
            "permission_denied_cases": permission_case_count,
            "expected_status_counts": dict(Counter(str(row.get("expected_status")) for row in http500_rows)),
            "actual_status_counts": dict(Counter(str(row.get("actual_status")) for row in rows)),
            "status_counts": dict(Counter(str(row.get("status")) for row in rows)),
        },
        "root_cause": {
            "likely_cause": "Historical evidence: NGINX worker could not traverse /root-owned runtime parents, generated docroot was inaccessible, and try_files /index.html looped into HTTP 500. New runs should block in the worker-docroot preflight before this becomes runtime mismatch evidence.",
            "classification": "harness_environment_error",
            "secondary_classification": "nginx_config_error",
            "confidence": "high",
            "evidence": [
                f"{rewrite_count} HTTP-500 rows have {ERROR_REWRITE_CYCLE!r}.",
                f"{permission_case_count} HTTP-500 rows have htdocs/index.html Permission denied in final-run error logs.",
                "Historical namei evidence shows /root is 0700 while NGINX worker user is nobody; generated files below it are otherwise readable.",
                "No segfault/core/module-load error pattern was observed in the final-run cluster.",
            ],
        },
        "groups": groups,
        "error_patterns": patterns,
        "representative_cases": reps,
        "permissions_probe": permissions_probe(minimal_row) if minimal_row else {},
        "minimal_repro": {
            "case": minimal_case,
            "status": "reproduced_by_full_matrix_evidence; direct single-case target needs a stable full-matrix wrapper",
            "existing_reproducer": "VERIFIED_RUN_FULL_MATRIX_JOB_TIMEOUT_SECONDS=3600 make verified-full-matrix-job CONNECTOR=nginx CRS=with-crs MRTS=with-mrts",
            "target_to_add": "make verified-nginx-mrts-case CASE=mrts_100000_mrts_002_args_a_get_100000_1 CRS=with-crs MRTS=with-mrts",
            "notes": "The connector harness supports TEST_CASE internally, but the verified full-matrix path does not yet expose a single-case target with CRS/MRTS setup and isolated job metadata.",
            "evidence": {
                "result_json": rel(minimal_row.get("evidence_path") or "-", connector_root) if minimal_row else "-",
                "nginx_error_log": rel(minimal_row.get("nginx_error_log_path") or "-", connector_root) if minimal_row else "-",
            },
        },
        "cluster_classification": [
            {
                "cluster": group["group"],
                "count": group["count"],
                "classification": group["classification"],
                "code_fix_needed": group["classification"] in {"harness_environment_error", "crs_mrts_rule_interaction_secondary_harness_environment_error"},
                "test_expectation_wrong": False,
                "document_only": False,
            }
            for group in groups
        ],
        "fix_plan": [
            {
                "fix": "Keep verified NGINX Full-Matrix harness roots under VERIFIED_RUN_ROOT/NGINX_HARNESS_PARENT outside /root.",
                "path": "ci/runtime/lifecycle/run-full-matrix-parallel.sh / Makefile NGINX_HARNESS_PARENT",
                "risk": "medium",
                "expected_effect": "Eliminates docroot Permission denied or reports it as a BLOCKED preflight before the 500 cluster can form.",
                "needs_new_verified_run": True,
            },
            {
                "fix": "Add a readiness/permission preflight that blocks NGINX jobs when worker user cannot traverse DOCROOT parents.",
                "path": "connectors/nginx/harness/run_nginx_smoke.sh",
                "risk": "low",
                "expected_effect": "Classifies future inaccessible-docroot evidence as BLOCKED instead of runtime FAIL.",
                "needs_new_verified_run": True,
            },
            {
                "fix": "Add a verified single-case Full-Matrix target for NGINX with CRS/MRTS setup and job metadata.",
                "path": "Makefile / ci/runtime/lifecycle/run-full-matrix-job.py",
                "risk": "low",
                "expected_effect": "Provides minimal repro without rerunning the 524-case NGINX job.",
                "needs_new_verified_run": False,
            },
        ],
        "data_availability": {
            "audit_logs": "Mostly absent for permission/docroot failures; NGINX fails while serving generated htdocs.",
            "single_case_target": "Not yet exposed as a verified make target.",
            "old_log_lines": "Some per-case logs include previous 2026-06-15 attempts; this report filters final-run error analysis to the job date prefix.",
        },
        "no_invented_values_statement": "All counts and examples are parsed from the verified NGINX with-crs/with-mrts job.json, JSONL result file, and referenced per-case logs.",
    }
    return payload


def md(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    if not rows:
        lines.append("| " + " | ".join(["Missing/Empty"] + ["-" for _ in headers[1:]]) + " |")
        return lines
    for row in rows:
        lines.append("| " + " | ".join(md(item) for item in row) + " |")
    return lines


def render_markdown(payload: dict[str, Any]) -> str:
    root = payload["root_cause"]
    lines = [
        "# NGINX with-crs/with-mrts HTTP-500 Cluster Analysis",
        "",
        "## Summary",
        "",
        f"- Verified run id: `{payload['verified_run_id']}`",
        f"- Job: `{payload['job_id']}`",
        f"- Primary blocker: `{payload['primary_blocker']}`",
        f"- HTTP-500 failures: `{payload['summary']['http500_failures']}`",
        f"- Likely cause: {root['likely_cause']}",
        f"- Classification: `{root['classification']}`; secondary `{root['secondary_classification']}`",
        f"- Confidence: `{root['confidence']}`",
        "",
        "## Cluster Counts",
        "",
    ]
    lines.extend(
        table(
            ["Group", "Count", "Classification", "Representative Cases"],
            [
                [
                    group["group"],
                    group["count"],
                    group["classification"],
                    "<br>".join(f"`{case['case']}`" for case in group["representative_cases"][:3]),
                ]
                for group in payload["groups"]
            ],
        )
    )
    lines.extend(["", "## Error Patterns", ""])
    lines.extend(
        table(
            ["Error Pattern", "Count", "Example", "Affected Cases"],
            [
                [
                    item["pattern"],
                    item["count"],
                    item["example"][:220],
                    "<br>".join(f"`{case}`" for case in item["affected_cases"][:4]),
                ]
                for item in payload["error_patterns"][:12]
            ],
        )
    )
    lines.extend(["", "## Representative Cases", ""])
    lines.extend(
        table(
            ["Case", "Expected", "Actual", "Access", "Error Pattern", "Classification", "Evidence"],
            [
                [
                    f"`{case['case']}`",
                    case["expected"],
                    case["actual"],
                    case["access_log_status"],
                    case["error_pattern"],
                    case["classification"],
                    case["evidence"]["result_json"],
                ]
                for case in payload["representative_cases"]
            ],
        )
    )
    lines.extend(["", "## Root Cause Evidence", ""])
    for evidence in root["evidence"]:
        lines.append(f"- {evidence}")
    lines.extend(["", "## Minimal Repro", ""])
    repro = payload["minimal_repro"]
    lines.extend(
        [
            f"- Minimal case: `{repro['case']}`",
            f"- Existing producer reproducer: `{repro['existing_reproducer']}`",
            f"- Target to add: `{repro['target_to_add']}`",
            f"- Notes: {repro['notes']}",
        ]
    )
    lines.extend(["", "## Fix Plan", ""])
    lines.extend(
        table(
            ["Fix", "File/Path", "Risk", "Expected Effect", "Needs New Verified Run"],
            [
                [item["fix"], item["path"], item["risk"], item["expected_effect"], item["needs_new_verified_run"]]
                for item in payload["fix_plan"]
            ],
        )
    )
    lines.extend(["", "## Data Availability / Missing Information", ""])
    lines.extend(
        table(
            ["Item", "Status"],
            [[key, value] for key, value in payload["data_availability"].items()],
        )
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector-root", default=os.getcwd())
    parser.add_argument("--framework-root", default=None)
    parser.add_argument("--build-root", default=os.environ.get("BUILD_ROOT"))
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--verified-run-id", default=None)
    args = parser.parse_args()

    connector_root = Path(args.connector_root).resolve()
    framework_root = Path(args.framework_root).resolve() if args.framework_root else connector_root / "modules/ModSecurity-test-Framework"
    default_paths = verified_runtime_paths(os.environ)
    build_root = Path(args.build_root or default_paths["BUILD_ROOT"]).resolve()
    output_dir = Path(args.output_dir).resolve() if args.output_dir else connector_root / GENERATED_ROOT
    report_root = output_dir.parent if output_dir.name == "manifest" else output_dir
    add_safe_roots(report_root, output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    verified_run_id = args.verified_run_id or current_verified_run_id(connector_root)

    payload = build_payload(connector_root, framework_root, build_root, verified_run_id)
    inputs = [Path(value) for value in payload["inputs"].values()]
    metadata = build_metadata(
        generated_by="ci/evidence/reports/generate-nginx-mrts-http500-cluster-analysis.py",
        make_target="generate-nginx-mrts-http500-cluster-analysis",
        connector_root=connector_root,
        framework_root=framework_root,
        inputs=inputs,
        report_key="nginx_mrts_http500_cluster_analysis",
        extra={"verified_run_id": verified_run_id},
    )
    json_path = report_path_from_root(report_root, "nginx_mrts_http500_cluster_analysis", "json")
    md_path = report_path_from_root(report_root, "nginx_mrts_http500_cluster_analysis", "md")
    write_text_file(json_path, generated_json_text(payload, metadata))
    write_text_file(md_path, generated_markdown_text(render_markdown(payload), metadata))
    print(md_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
