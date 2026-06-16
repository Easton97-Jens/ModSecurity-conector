#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
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


CRITICAL_CATEGORIES = {
    "runtime_regression",
    "expected_status_mismatch",
    "connector_capability_gap",
    "framework_expected_behavior_gap",
    "environment_flake",
    "timeout_or_incomplete",
    "unknown",
}


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
    row = {
        "connector": connector,
        "variant": variant,
        "case": str(case.get("name") or case.get("case") or Path(str(case.get("path") or "unknown")).stem),
        "expected": expected,
        "actual": actual,
        "status": status,
        "classification": classification,
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
        "full_matrix_refresh_timeout": str(full.get("refresh_status") or "") == "refresh_timeout"
        or (str(full.get("classification") or "") == "blocked_timeout" and full_complete),
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
    verified_run_id = args.verified_run_id or current_verified_run_id(connector_root)
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
            command_state["full_matrix_runtime_status"] = (
                "runtime_completed_with_mismatches"
                if any(job.get("return_code") not in {0, None} for job in completed_completeness_jobs)
                else "runtime_completed"
            )
            command_state["full_matrix_timeout"] = False
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
        ),
        "artifact_roots": {
            "runtime_matrix_results": str(results_root),
            "full_matrix_results": str(full_matrix_root),
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
        inputs=[commands_file, manifest_path],
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
