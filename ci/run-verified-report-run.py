#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import time
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
    git_sha,
    report_path,
    report_relpath,
    sha256_file,
    utc_now,
)
from runtime_path_utils import (
    WORKER_BLOCKED_REASON,
    is_under_root_home,
    runtime_path_rows,
    verified_runtime_paths,
)


def git_output(args: list[str], cwd: Path) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=str(cwd),
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=10,
        )
    except Exception as exc:
        return f"unknown: {exc}"
    return result.stdout.strip() or "unknown"


def git_dirty_status(root: Path) -> str:
    status = git_output(["status", "--short"], root)
    if status.startswith("unknown:"):
        return "unknown"
    return "dirty" if status else "clean"


def git_branch(root: Path) -> str:
    return git_output(["rev-parse", "--abbrev-ref", "HEAD"], root)


def command_status(return_code: int, *, optional: bool = False, classification: str = "") -> str:
    if return_code == 0:
        return "PASS"
    if classification == "blocked_timeout":
        return "BLOCKED_TIMEOUT"
    if classification in {"blocked_network", "blocked_network_optional", "producer_readiness_blocked", "nginx_worker_docroot_blocked"}:
        return "BLOCKED_OPTIONAL" if optional else "BLOCKED"
    if classification == "interrupted":
        return "INTERRUPTED"
    if optional:
        return "BLOCKED_OPTIONAL" if return_code == 77 else "FAILED_OPTIONAL"
    if return_code == 77:
        return "BLOCKED"
    return "FAIL"


def write_commands_file(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_command(
    command: list[str],
    *,
    cwd: Path,
    env: dict[str, str],
    logs_dir: Path,
    index: int,
    phase: str,
    required: bool,
    optional: bool,
    timeout_seconds: int | None,
    affected_reports: list[str],
    logical_target: str,
) -> dict[str, Any]:
    started_at = utc_now()
    started = time.monotonic()
    slug = "".join(ch if ch.isalnum() else "-" for ch in "-".join(command)).strip("-")[:96] or "command"
    log_path = logs_dir / f"{index:02d}-{slug}.log"
    print("verified-report-run: RUN " + " ".join(command), flush=True)
    return_code = 0
    classification = ""
    signal_name = ""
    with log_path.open("w", encoding="utf-8") as log_handle:
        process = subprocess.Popen(
            command,
            cwd=str(cwd),
            env=env,
            stdout=log_handle,
            stderr=subprocess.STDOUT,
            text=True,
            start_new_session=True,
        )
        try:
            return_code = process.wait(timeout=timeout_seconds)
        except subprocess.TimeoutExpired:
            classification = "blocked_timeout"
            log_handle.write(
                f"\nverified-report-run: timeout after {timeout_seconds} seconds; terminating process group\n"
            )
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                return_code = process.wait(timeout=30)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                return_code = process.wait()
        except KeyboardInterrupt:
            classification = "interrupted"
            log_handle.write("\nverified-report-run: interrupted; terminating process group\n")
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            return_code = process.wait()
    finished_at = utc_now()
    if return_code < 0:
        try:
            signal_name = signal.Signals(-return_code).name
        except ValueError:
            signal_name = f"SIG{-return_code}"
        classification = classification or "interrupted"
    log_text = log_path.read_text(encoding="utf-8", errors="replace") if log_path.is_file() else ""
    if return_code != 0 and not classification and ("HTTP Error 504" in log_text or "Gateway Timeout" in log_text):
        classification = "blocked_network_optional" if optional else "blocked_network"
    if return_code != 0 and not classification and WORKER_BLOCKED_REASON in log_text:
        classification = "nginx_worker_docroot_blocked"
    log_hash = sha256_file(log_path)
    status = command_status(return_code, optional=optional, classification=classification)
    print(f"verified-report-run: {status} rc={return_code} log={log_path}", flush=True)
    return {
        "phase": phase,
        "command": command,
        "logical_target": logical_target,
        "required": required,
        "optional": optional,
        "affected_reports": affected_reports,
        "status": status,
        "return_code": return_code,
        "classification": classification or ("success" if return_code == 0 else "command_failed"),
        "signal": signal_name,
        "timeout_seconds": timeout_seconds,
        "started_at": started_at,
        "finished_at": finished_at,
        "duration_seconds": round(time.monotonic() - started, 3),
        "log_path": str(log_path),
        "log_hash": log_hash,
        "notes": "executed in verified-report-run",
    }


def skipped_command_record(
    command: list[str],
    *,
    logs_dir: Path,
    index: int,
    phase: str,
    required: bool,
    optional: bool,
    affected_reports: list[str],
    reason: str,
    logical_target: str,
) -> dict[str, Any]:
    started_at = utc_now()
    slug = "".join(ch if ch.isalnum() else "-" for ch in "-".join(command)).strip("-")[:96] or "command"
    log_path = logs_dir / f"{index:02d}-{slug}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(f"verified-report-run: skipped because {reason}\n", encoding="utf-8")
    return {
        "phase": phase,
        "command": command,
        "logical_target": logical_target,
        "required": required,
        "optional": optional,
        "affected_reports": affected_reports,
        "status": command_status(77, optional=optional, classification="producer_readiness_blocked"),
        "return_code": 77,
        "classification": "producer_readiness_blocked",
        "signal": "",
        "timeout_seconds": 0,
        "started_at": started_at,
        "finished_at": started_at,
        "duration_seconds": 0.0,
        "log_path": str(log_path),
        "log_hash": sha256_file(log_path),
        "notes": f"not executed: {reason}",
    }


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def file_record(path: Path, root: Path) -> dict[str, Any]:
    shown = str(path.relative_to(root)) if path.is_relative_to(root) else str(path)
    if not path.is_file():
        return {"path": shown, "status": "missing", "sha256": "missing"}
    return {"path": shown, "status": "present", "sha256": sha256_file(path), "bytes": path.stat().st_size}


def generated_output_records(connector_root: Path) -> list[dict[str, Any]]:
    generated_root = connector_root / "reports/testing/generated"
    if not generated_root.is_dir():
        return []
    return [file_record(path, connector_root) for path in sorted(generated_root.rglob("*.generated.*")) if path.is_file()]


def manifest_report_records(connector_root: Path) -> list[dict[str, Any]]:
    manifest = read_json(report_path(connector_root, "report_refresh_manifest", "json"))
    reports = manifest.get("reports")
    return reports if isinstance(reports, list) else []


def collect_declared_inputs(connector_root: Path) -> list[dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for report in manifest_report_records(connector_root):
        for item in report.get("inputs", []):
            if not isinstance(item, dict):
                continue
            path = str(item.get("path", "unknown"))
            rows[path] = {
                "path": path,
                "status": item.get("status", "unknown"),
                "sha256": item.get("sha256") or item.get("source_hash") or "unknown",
                "verified_run_id": item.get("verified_run_id", "unknown"),
                "notes": item.get("notes", ""),
            }
    return [rows[key] for key in sorted(rows)]


def collect_report_statuses(connector_root: Path, status_prefix: str | None = None, status_values: set[str] | None = None) -> list[dict[str, Any]]:
    rows = []
    for report in manifest_report_records(connector_root):
        status = str(report.get("status", "unknown"))
        if status_prefix is not None and not status.startswith(status_prefix):
            continue
        if status_values is not None and status not in status_values:
            continue
        rows.append(
            {
                "report_name": report.get("report_name", "unknown"),
                "status": status,
                "reason": report.get("blocked_reason") or report.get("freshness_status") or report.get("input_status") or "unknown",
                "outputs": report.get("output_files", []),
                "inputs": report.get("input_files", []),
            }
        )
    return rows


def runtime_paths(env: dict[str, str], build_root: Path, verified_run_id: str) -> dict[str, str]:
    paths = verified_runtime_paths(env, build_root_override=build_root)
    paths["VERIFIED_RUN_INSTANCE_ROOT"] = str(build_root / "verified-runs" / verified_run_id)
    return paths


def prepare_runtime_roots(paths: dict[str, str]) -> None:
    for key in (
        "VERIFIED_RUN_ROOT",
        "VERIFIED_STATE_ROOT",
        "VERIFIED_BUILD_ROOT",
        "VERIFIED_SOURCE_ROOT",
        "VERIFIED_TMP_ROOT",
        "VERIFIED_LOG_ROOT",
        "VERIFIED_COMPONENT_CACHE",
        "NGINX_HARNESS_PARENT",
    ):
        path = Path(paths[key])
        path.mkdir(parents=True, exist_ok=True)
        try:
            path.chmod(0o755)
        except OSError:
            pass


def runtime_path_report_rows(paths: dict[str, str], connector_root: Path, framework_root: Path) -> list[dict[str, Any]]:
    return runtime_path_rows(paths, connector_root=connector_root, framework_root=framework_root)


def worker_preflight_rows(paths: dict[str, str], build_root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    harness_parent = Path(paths["NGINX_HARNESS_PARENT"])
    root_status = "FAIL" if is_under_root_home(harness_parent) else "PASS"
    rows.append(
        {
            "check": "Path under /root",
            "status": root_status,
            "path": str(harness_parent),
            "notes": "NGINX_HARNESS_PARENT must be outside /root" if root_status == "FAIL" else "outside /root",
        }
    )
    if harness_parent.exists():
        traverse_status = "PASS" if os.access(harness_parent, os.X_OK) else "FAIL"
        rows.append(
            {
                "check": "Harness parent traversable",
                "status": traverse_status,
                "path": str(harness_parent),
                "notes": "current process can traverse; per-case worker checks are recorded in nginx-worker-preflight.jsonl",
            }
        )
    else:
        rows.append(
            {
                "check": "Harness parent traversable",
                "status": "UNKNOWN",
                "path": str(harness_parent),
                "notes": "harness parent has not been created yet",
            }
        )

    candidates: list[Path] = []
    for root in (harness_parent, build_root):
        if root.exists():
            candidates.extend(root.rglob("nginx-worker-preflight.jsonl"))
    seen: set[str] = set()
    for path in sorted(candidates, key=lambda item: item.stat().st_mtime if item.exists() else 0, reverse=True):
        key = str(path)
        if key in seen:
            continue
        seen.add(key)
        for record in read_jsonl(path):
            if not isinstance(record, dict):
                continue
            row = {
                "check": record.get("check", "unknown"),
                "status": record.get("status", "UNKNOWN"),
                "path": record.get("path", str(path)),
                "notes": record.get("notes", "-"),
                "source_file": str(path),
                "source_hash": sha256_file(path),
            }
            rows.append(row)
            if len(rows) >= 60:
                return rows
    return rows


def full_matrix_completeness_summary(connector_root: Path) -> dict[str, Any]:
    data = read_json(report_path(connector_root, "full_matrix_job_completeness", "json"))
    jobs = data.get("jobs") if isinstance(data.get("jobs"), list) else []
    slowest = data.get("slowest_jobs") if isinstance(data.get("slowest_jobs"), list) else []
    return {
        "status": data.get("overall_status", "unknown"),
        "complete_jobs": data.get("complete_jobs", 0),
        "total_jobs": data.get("total_jobs", 0),
        "missing_jobs": data.get("missing_job_ids", []),
        "timeout_jobs": [
            job.get("job_id", "unknown")
            for job in jobs
            if str(job.get("status", "")).startswith("timeout") or "timeout" in str(job.get("reason", "")).lower()
        ],
        "slowest_jobs": [
            {
                "job_id": job.get("job_id", "unknown"),
                "duration_seconds": job.get("duration_seconds", "unknown"),
                "status": job.get("status", "unknown"),
            }
            for job in slowest[:5]
            if isinstance(job, dict)
        ],
        "source": str(report_path(connector_root, "full_matrix_job_completeness", "json")),
    }


def runtime_mismatch_summary(connector_root: Path) -> dict[str, Any]:
    data = read_json(report_path(connector_root, "verified_runtime_mismatch_analysis", "json"))
    by_connector = data.get("by_connector") if isinstance(data.get("by_connector"), dict) else {}
    top_connector = "unknown"
    top_count = -1
    for name, value in by_connector.items():
        count = value.get("total", value.get("count", 0)) if isinstance(value, dict) else value
        try:
            numeric = int(count)
        except Exception:
            numeric = 0
        if numeric > top_count:
            top_connector = str(name)
            top_count = numeric
    full_matrix = data.get("full_matrix") if isinstance(data.get("full_matrix"), dict) else {}
    blocker = full_matrix.get("classification") or full_matrix.get("status") or data.get("merge_readiness_reason") or "unknown"
    return {
        "total_mismatches": data.get("mismatch_count", "unknown"),
        "critical_mismatches": data.get("critical_mismatch_count", "unknown"),
        "top_connector": top_connector,
        "primary_blocker": blocker,
        "merge_readiness": data.get("merge_readiness", "unknown"),
        "source": str(report_path(connector_root, "verified_runtime_mismatch_analysis", "json")),
    }


def manifest_input_status(payload: dict[str, Any], metadata_status: str) -> str:
    if payload.get("missing_inputs") or payload.get("blocked_reports") or payload.get("failed_reports"):
        return "blocked"
    for item in payload.get("skipped_reports", []):
        status = str(item.get("status", ""))
        if status == "skipped_stale_input":
            return "stale"
        if status.startswith("skipped"):
            return "blocked"
    if payload.get("stale_inputs"):
        return "stale"
    if metadata_status != "complete":
        return metadata_status
    completeness = payload.get("full_matrix_job_completeness", {})
    if completeness.get("status") == "unknown":
        return "unknown"
    mismatch = payload.get("runtime_mismatch_summary", {})
    if mismatch.get("total_mismatches", "unknown") == "unknown":
        return "unknown"
    return "complete"


def parse_timeout(value: str | None) -> int | None:
    if value is None or value.strip() == "":
        return None
    try:
        parsed = int(value)
    except ValueError:
        return None
    return parsed if parsed > 0 else None


def timeout_from_env(env: dict[str, str], name: str, default: int, *, aliases: tuple[str, ...] = ()) -> int:
    for key in (name, *aliases):
        parsed = parse_timeout(env.get(key))
        if parsed is not None:
            return parsed
    return default


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


def parse_time(value: str | None) -> float | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def full_matrix_runtime_state(record: dict[str, Any], env: dict[str, str], profile: str) -> dict[str, Any]:
    manifest = Path(env.get("FULL_MATRIX_MANIFEST", ""))
    rows = read_jsonl(manifest)
    started_ts = parse_time(str(record.get("started_at") or ""))
    fresh_rows = []
    for row in rows:
        row_started = parse_time(str(row.get("started_at") or ""))
        if started_ts is not None and row_started is not None and row_started + 1 < started_ts:
            continue
        fresh_rows.append(row)
    expected = 0 if profile == "smoke" else 12
    complete = expected > 0 and len(fresh_rows) >= expected
    return_codes = [row.get("return_code") for row in fresh_rows]
    mismatched = any(code not in {0, None} for code in return_codes)
    if complete and mismatched:
        runtime_status = "runtime_completed_with_mismatches"
    elif complete:
        runtime_status = "runtime_completed"
    elif record.get("classification") == "blocked_timeout":
        runtime_status = "runtime_timeout"
    elif record.get("return_code") == 0:
        runtime_status = "runtime_completed"
    else:
        runtime_status = "runtime_failed"
    return {
        "runtime_status": runtime_status,
        "runtime_complete": complete,
        "runtime_expected_jobs": expected,
        "runtime_completed_jobs": len(fresh_rows),
        "runtime_manifest_path": str(manifest),
        "runtime_job_return_codes": return_codes,
    }


def native_runtime_state(record: dict[str, Any], env: dict[str, str]) -> dict[str, Any]:
    native_root = Path(env.get("MRTS_NATIVE_ROOT", ""))
    targets = ("apache2_ubuntu", "nginx-pr24")
    jobs = []
    for target in targets:
        job_path = native_root / target / "job.json"
        if job_path.is_file():
            data = read_json(job_path)
            jobs.append({"target": target, "return_code": data.get("return_code"), "job_path": str(job_path)})
    complete = len(jobs) == len(targets)
    mismatched = any(job.get("return_code") not in {0, None} for job in jobs)
    if complete and mismatched:
        runtime_status = "runtime_completed_with_mismatches"
    elif complete:
        runtime_status = "runtime_completed"
    elif record.get("classification") == "blocked_timeout":
        runtime_status = "runtime_timeout"
    elif record.get("return_code") == 0:
        runtime_status = "runtime_completed"
    else:
        runtime_status = "runtime_failed"
    return {
        "runtime_status": runtime_status,
        "runtime_complete": complete,
        "runtime_expected_jobs": len(targets),
        "runtime_completed_jobs": len(jobs),
        "runtime_jobs": jobs,
    }


def simple_runtime_state(record: dict[str, Any]) -> dict[str, Any]:
    if record.get("classification") == "blocked_timeout":
        runtime_status = "runtime_timeout"
    elif record.get("return_code") == 0:
        runtime_status = "runtime_completed"
    elif record.get("return_code") in {1, 2}:
        runtime_status = "runtime_completed_with_mismatches"
    else:
        runtime_status = "runtime_failed"
    return {"runtime_status": runtime_status, "runtime_complete": runtime_status != "runtime_timeout"}


def full_matrix_job_state(record: dict[str, Any]) -> dict[str, Any]:
    if record.get("classification") == "blocked_timeout" or record.get("return_code") == 77:
        runtime_status = "runtime_timeout"
    elif record.get("return_code") == 0:
        runtime_status = "runtime_completed"
    elif record.get("return_code") in {1, 2}:
        runtime_status = "runtime_completed_with_mismatches"
    else:
        runtime_status = "runtime_failed"
    return {"runtime_status": runtime_status, "runtime_complete": runtime_status != "runtime_timeout"}


def refresh_state(record: dict[str, Any]) -> dict[str, Any]:
    if record.get("classification") == "blocked_timeout":
        status = "refresh_timeout"
    elif record.get("return_code") == 0:
        status = "refresh_completed"
    else:
        log_path = Path(str(record.get("log_path") or ""))
        log_text = log_path.read_text(encoding="utf-8", errors="replace") if log_path.is_file() else ""
        if (
            "SKIPPED_STALE_INPUT" in log_text
            or "required generated input is stale" in log_text
            or "required generated input is blocked" in log_text
        ):
            status = "consumer_stale"
        else:
            status = "refresh_failed"
    overall = "blocked_refresh_timeout" if status == "refresh_timeout" else status
    return {"refresh_status": status, "overall_status": overall}


def apply_command_semantics(record: dict[str, Any], env: dict[str, str], profile: str) -> dict[str, Any]:
    target = str(record.get("logical_target") or "")
    if target == "full-matrix-parallel":
        record.update(full_matrix_runtime_state(record, env, profile))
        record["overall_status"] = record["runtime_status"]
    elif target == "runtime-matrix-all":
        record.update(simple_runtime_state(record))
        record["overall_status"] = record["runtime_status"]
    elif target == "mrts-native-full-run":
        record.update(native_runtime_state(record, env))
        record["overall_status"] = record["runtime_status"]
    elif target.startswith("full-matrix-job:") or target == "full-matrix-resume":
        record.update(full_matrix_job_state(record))
        record["overall_status"] = record["runtime_status"]
    elif target in {"refresh-all-reports", "generate-system-environment-proof"}:
        record.update(refresh_state(record))
    elif target == "check-generated-report-layout":
        if record.get("return_code") == 0:
            record["overall_status"] = "checks_completed"
        else:
            record["overall_status"] = "layout_failed"
    return record


def command_plan(
    *,
    runtime_matrix_timeout: int,
    full_matrix_runtime_timeout: int,
    report_refresh_timeout: int,
    native_mrts_timeout: int,
    profile: str,
) -> list[dict[str, Any]]:
    producers: list[dict[str, Any]] = [
        {
            "phase": "runtime-producers",
            "command": ["git", "submodule", "update", "--init", "--recursive"],
            "logical_target": "git-submodule-update",
            "required": True,
            "optional": False,
            "affected_reports": ["framework_submodule", "mrts_submodule"],
            "timeout_seconds": 300,
        },
        {
            "phase": "runtime-producers",
            "command": ["make", "prepare-runtime-components"],
            "logical_target": "prepare-runtime-components",
            "required": True,
            "optional": False,
            "affected_reports": ["runtime_component_cache", "runtime_build_cache"],
            "timeout_seconds": 1800,
        },
        {
            "phase": "runtime-producers",
            "command": ["make", "check-runtime-producer-readiness"],
            "logical_target": "check-runtime-producer-readiness",
            "required": True,
            "optional": False,
            "affected_reports": ["runtime_component_cache", "runtime_build_cache", "system_environment_proof"],
            "timeout_seconds": 300,
        },
        {
            "phase": "runtime-producers",
            "command": ["make", "runtime-matrix-all-runtime"],
            "logical_target": "runtime-matrix-all",
            "required": True,
            "optional": False,
            "affected_reports": [
                "apache_runtime_results",
                "nginx_runtime_results",
                "haproxy_runtime_results",
                "runtime_matrix",
                "phase_coverage",
            ],
            "timeout_seconds": runtime_matrix_timeout,
        },
    ]
    if profile == "full":
        producers.extend(
            [
                {
                    "phase": "runtime-producers",
                    "command": ["make", "full-matrix-parallel-runtime"],
                    "logical_target": "full-matrix-parallel",
                    "required": True,
                    "optional": False,
                    "affected_reports": [
                        "full_runtime_matrix",
                        "connector_work_queue",
                        "phase_work_queue",
                        "remaining_failure_analysis",
                        "next_fix_plan",
                        "final_consistency_audit",
                        "full_run_evidence",
                    ],
                    "timeout_seconds": full_matrix_runtime_timeout,
                },
                {
                    "phase": "runtime-producers",
                    "command": ["make", "mrts-native-full-run-runtime"],
                    "logical_target": "mrts-native-full-run",
                    "required": False,
                    "optional": True,
                    "affected_reports": [
                        "mrts_native_full",
                        "mrts_native_apache",
                        "mrts_native_nginx",
                        "mrts_native_summary",
                    ],
                    "timeout_seconds": native_mrts_timeout,
                },
            ]
        )
    producers.append(
        {
            "phase": "runtime-producers",
            "command": ["make", "generate-verified-runtime-mismatch-analysis"],
            "logical_target": "generate-verified-runtime-mismatch-analysis",
            "required": False,
            "optional": True,
            "affected_reports": ["verified_runtime_mismatch_analysis"],
            "timeout_seconds": report_refresh_timeout,
        }
    )
    consumers = [
        {
            "phase": "report-refresh",
            "command": ["make", "refresh-all-reports"],
            "logical_target": "refresh-all-reports",
            "required": True,
            "optional": False,
            "affected_reports": ["report_refresh_manifest", "merge_readiness_dashboard", "report_freshness"],
            "timeout_seconds": report_refresh_timeout,
        },
        {
            "phase": "report-refresh",
            "command": ["make", "generate-system-environment-proof"],
            "logical_target": "generate-system-environment-proof",
            "required": True,
            "optional": False,
            "affected_reports": ["system_environment_proof"],
            "timeout_seconds": report_refresh_timeout,
        },
        {
            "phase": "report-refresh",
            "command": ["make", "refresh-all-reports"],
            "logical_target": "refresh-all-reports",
            "required": True,
            "optional": False,
            "affected_reports": ["report_refresh_manifest", "merge_readiness_dashboard", "report_freshness"],
            "timeout_seconds": report_refresh_timeout,
        },
    ]
    checks = [
        {
            "phase": "checks",
            "command": ["make", "check-generated-report-layout"],
            "logical_target": "check-generated-report-layout",
            "required": True,
            "optional": False,
            "affected_reports": ["all_generated_reports"],
            "timeout_seconds": 300,
        },
        {
            "phase": "checks",
            "command": ["make", "lint"],
            "logical_target": "lint",
            "required": True,
            "optional": False,
            "affected_reports": ["python_sources", "generated_report_layout"],
            "timeout_seconds": 900,
        },
        {
            "phase": "checks",
            "command": ["make", "quick-check"],
            "logical_target": "quick-check",
            "required": True,
            "optional": False,
            "affected_reports": ["python_sources", "generated_report_layout"],
            "timeout_seconds": 900,
        },
    ]
    return producers + consumers + checks


def select_commands(plan: list[dict[str, Any]], phase: str) -> list[dict[str, Any]]:
    aliases = {
        "producers": "runtime-producers",
        "consumers": "report-refresh",
    }
    phase = aliases.get(phase, phase)
    if phase == "all":
        return plan
    return [item for item in plan if item["phase"] == phase]


def system_proof_summary(connector_root: Path) -> dict[str, Any]:
    proof = read_json(report_path(connector_root, "system_environment_proof", "json"))
    return {
        "tools": proof.get("tools", []) if isinstance(proof.get("tools"), list) else [],
        "system": proof.get("os", {}) if isinstance(proof.get("os"), dict) else {},
        "runtime_component_readiness": proof.get("runtime_component_readiness", [])
        if isinstance(proof.get("runtime_component_readiness"), list)
        else [],
        "runtime_producer_readiness_check": proof.get("runtime_producer_readiness_check", {})
        if isinstance(proof.get("runtime_producer_readiness_check"), dict)
        else {},
        "https_repo_url_policy": proof.get("https_repo_url_policy", {})
        if isinstance(proof.get("https_repo_url_policy"), dict)
        else {},
    }


def duration_seconds(start: str, end: str) -> float | str:
    try:
        start_dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
        end_dt = datetime.fromisoformat(end.replace("Z", "+00:00"))
    except ValueError:
        return "unknown"
    return round((end_dt - start_dt).total_seconds(), 3)


def render_markdown(payload: dict[str, Any]) -> str:
    def cell(value: Any) -> str:
        return str(value if value is not None else "-").replace("|", "/").replace("\n", " ")

    producer_targets = {
        "git-submodule-update",
        "prepare-runtime-components",
        "check-runtime-producer-readiness",
        "runtime-matrix-all",
        "full-matrix-parallel",
        "mrts-native-full-run",
        "generate-verified-runtime-mismatch-analysis",
    }
    consumer_targets = {"refresh-all-reports", "generate-system-environment-proof"}
    check_targets = {"check-generated-report-layout", "lint", "quick-check"}

    lines = [
        "# Verified Run Manifest",
        "",
        "## Summary",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Verified run id | `{cell(payload.get('verified_run_id', 'unknown'))}` |",
        f"| Data source policy | `{cell(payload.get('data_source_policy', DATA_SOURCE_POLICY))}` |",
        f"| Profile | `{cell(payload.get('profile', 'full'))}` |",
        f"| Start time UTC | `{cell(payload.get('started_at_utc', 'unknown'))}` |",
        f"| End time UTC | `{cell(payload.get('finished_at_utc', 'unknown'))}` |",
        f"| Duration seconds | `{cell(payload.get('duration_seconds', 'unknown'))}` |",
        f"| Input status | `{cell(payload.get('input_status', 'unknown'))}` |",
        "",
        "## Runtime Environment",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Connector SHA | `{cell(payload.get('connector_sha', 'unknown'))}` |",
        f"| Framework SHA | `{cell(payload.get('framework_sha', 'unknown'))}` |",
        f"| MRTS SHA | `{cell(payload.get('mrts_sha', 'unknown'))}` |",
        f"| Connector branch | `{cell(payload.get('branches', {}).get('connector', 'unknown'))}` |",
        f"| Framework branch | `{cell(payload.get('branches', {}).get('framework', 'unknown'))}` |",
        f"| Dirty status | `{cell(payload.get('dirty_status', {}).get('connector', 'unknown'))}` / `{cell(payload.get('dirty_status', {}).get('framework', 'unknown'))}` |",
        f"| Runtime matrix timeout seconds | `{cell(payload.get('timeout_budgets', {}).get('runtime_matrix', 'none'))}` |",
        f"| Full matrix runtime timeout seconds | `{cell(payload.get('timeout_budgets', {}).get('full_matrix_runtime', 'none'))}` |",
        f"| Report refresh timeout seconds | `{cell(payload.get('timeout_budgets', {}).get('report_refresh', 'none'))}` |",
        f"| Native MRTS timeout seconds | `{cell(payload.get('timeout_budgets', {}).get('native_mrts', 'none'))}` |",
        "",
        "## Runtime Paths",
        "",
        "| Variable | Value | Status | Notes |",
        "|---|---|---|---|",
    ]
    for item in payload.get("runtime_path_rows", []):
        lines.append(
            f"| `{cell(item.get('variable'))}` | `{cell(item.get('value'))}` | {cell(item.get('status'))} | {cell(item.get('notes'))} |"
        )
    if not payload.get("runtime_path_rows"):
        lines.append("| `-` | `-` | UNKNOWN | no runtime path rows recorded |")

    lines.extend(["", "## Worker Accessibility / Preflight", "", "| Check | Status | Path | Notes |", "|---|---|---|---|"])
    for item in payload.get("worker_preflight", []):
        lines.append(f"| {cell(item.get('check'))} | {cell(item.get('status'))} | `{cell(item.get('path'))}` | {cell(item.get('notes'))} |")
    if not payload.get("worker_preflight"):
        lines.append("| NGINX worker preflight | UNKNOWN | `-` | no preflight evidence recorded |")

    producer_check = payload.get("runtime_producer_readiness_check", {})
    nginx_readiness = producer_check.get("nginx_runtime_module_readiness", {}) if isinstance(producer_check, dict) else {}
    lines.extend(
        [
            "",
            "## Runtime Producer Readiness",
            "",
            f"- Status: `{producer_check.get('status', 'unknown') if isinstance(producer_check, dict) else 'unknown'}`",
            f"- Runtime env loaded: `{producer_check.get('runtime_env_loaded', False) if isinstance(producer_check, dict) else False}`",
            f"- Runtime env path: `{producer_check.get('runtime_env_path', '-') if isinstance(producer_check, dict) else '-'}`",
            "",
            "| Component | Required | Status | Path | Fix |",
            "|---|---|---|---|---|",
        ]
    )
    components = producer_check.get("components", []) if isinstance(producer_check, dict) else []
    for item in components:
        if isinstance(item, dict):
            lines.append(
                f"| {cell(item.get('component', '-'))} | {cell(item.get('required', '-'))} | {cell(item.get('status', 'unknown'))} | "
                f"`{cell(item.get('path', '-'))}` | `{cell(item.get('fix', '-'))}` |"
            )
    if not components:
        lines.append("| - | - | unknown | `-` | `make check-runtime-producer-readiness` |")
    lines.extend(
        [
            "",
            "## NGINX Runtime Module Readiness",
            "",
            "| Field | Value |",
            "|---|---|",
            f"| NGINX_BIN | `{cell(nginx_readiness.get('NGINX_BIN', ''))}` |",
            f"| NGINX_MODULE_DIR | `{cell(nginx_readiness.get('NGINX_MODULE_DIR', ''))}` |",
            f"| ModSecurity module path | `{cell(nginx_readiness.get('ModSecurity module path', ''))}` |",
            f"| Module exists | `{cell(str(nginx_readiness.get('Module exists', False)).lower())}` |",
            f"| How to prepare | `{cell(nginx_readiness.get('How to prepare', 'make prepare-runtime-components'))}` |",
            "",
            "## Runtime Network / Cache Readiness",
            "",
            "| Source | Status | Path | Notes |",
            "|---|---|---|---|",
        ]
    )
    network_cache = producer_check.get("network_cache", []) if isinstance(producer_check, dict) else []
    for item in network_cache:
        if isinstance(item, dict):
            lines.append(f"| {cell(item.get('source', '-'))} | {cell(item.get('status', 'unknown'))} | `{cell(item.get('path', '-'))}` | {cell(item.get('notes', '-'))} |")
    if not network_cache:
        lines.append("| - | unknown | `-` | No runtime producer cache rows recorded. |")

    def command_table(title: str, targets: set[str]) -> None:
        lines.extend(["", title, "", "| Command | Status | RC | Duration | Runtime Status | Refresh Status | Log |", "|---|---:|---:|---:|---|---|---|"])
        rows = [
            command for command in payload.get("commands", [])
            if str(command.get("logical_target", "")) in targets
            or (title == "## Producer Commands" and str(command.get("logical_target", "")).startswith("full-matrix-job:"))
        ]
        for command in rows:
            command_text = " ".join(command.get("command", []))
            lines.append(
                f"| `{cell(command_text)}` | {cell(command.get('status', 'unknown'))} | {cell(command.get('return_code', '-'))} | "
                f"{cell(command.get('duration_seconds', '-'))} | {cell(command.get('runtime_status', '-'))} | "
                f"{cell(command.get('refresh_status', '-'))} | `{cell(command.get('log_path', '-'))}` |"
            )
        if not rows:
            lines.append("| `-` | not_run | - | - | - | - | `-` |")

    command_table("## Producer Commands", producer_targets)
    command_table("## Consumer / Refresh Commands", consumer_targets)
    command_table("## Checks", check_targets)

    completeness = payload.get("full_matrix_job_completeness", {})
    lines.extend(["", "## Full-Matrix Job Completeness", "", "| Field | Value |", "|---|---|"])
    lines.append(f"| Completeness | `{cell(completeness.get('complete_jobs', 0))}/{cell(completeness.get('total_jobs', 0))}` |")
    lines.append(f"| Overall status | `{cell(completeness.get('status', 'unknown'))}` |")
    lines.append(f"| Missing jobs | `{cell(', '.join(completeness.get('missing_jobs', [])) or '-')}` |")
    lines.append(f"| Timeout jobs | `{cell(', '.join(completeness.get('timeout_jobs', [])) or '-')}` |")
    lines.extend(["", "| Slowest Job | Duration Seconds | Status |", "|---|---:|---|"])
    for job in completeness.get("slowest_jobs", []):
        lines.append(f"| `{cell(job.get('job_id'))}` | {cell(job.get('duration_seconds'))} | {cell(job.get('status'))} |")
    if not completeness.get("slowest_jobs"):
        lines.append("| `-` | - | unknown |")

    mismatch = payload.get("runtime_mismatch_summary", {})
    lines.extend(["", "## Runtime Mismatch Summary", "", "| Field | Value |", "|---|---|"])
    lines.append(f"| Total mismatches | `{cell(mismatch.get('total_mismatches', 'unknown'))}` |")
    lines.append(f"| Critical mismatches | `{cell(mismatch.get('critical_mismatches', 'unknown'))}` |")
    lines.append(f"| Top connector | `{cell(mismatch.get('top_connector', 'unknown'))}` |")
    lines.append(f"| Primary blocker | `{cell(mismatch.get('primary_blocker', 'unknown'))}` |")
    lines.append(f"| Merge readiness | `{cell(mismatch.get('merge_readiness', 'unknown'))}` |")

    lines.extend(["", "## Blocked / Stale Inputs", "", "| Item | Status | Reason | Affected Reports |", "|---|---|---|---|"])
    rows = []
    for key in ("missing_inputs", "skipped_reports", "blocked_reports", "failed_reports", "stale_inputs"):
        for item in payload.get(key, []):
            rows.append(item)
    for item in rows:
        affected = ", ".join(str(value) for value in item.get("outputs", [])) or "-"
        lines.append(
            f"| `{cell(item.get('report_name', item.get('path', 'unknown')))}` | {cell(item.get('status', 'unknown'))} | "
            f"{cell(item.get('reason', item.get('notes', 'unknown')))} | {cell(affected)} |"
        )
    if not rows:
        lines.append("| `-` | zero_result_verified | No missing, skipped, blocked, stale, or failed reports were recorded. | - |")

    lines.extend(["", "## Tool Versions", "", "| Tool | Status | Version / Output |", "|---|---|---|"])
    for tool in payload.get("tool_versions", []):
        version = str(tool.get("version") or tool.get("version_output") or "-").splitlines()[0]
        lines.append(f"| {cell(tool.get('tool', '-'))} | {cell(tool.get('status', 'unknown'))} | `{cell(version)}` |")
    if not payload.get("tool_versions"):
        lines.append("| `-` | unknown | `system-environment-proof unavailable` |")

    lines.extend(
        [
            "",
            "## Git Evidence",
            "",
            "| Repository | SHA | Branch | Dirty Status |",
            "|---|---|---|---|",
            f"| connector | `{cell(payload.get('connector_sha', 'unknown'))}` | `{cell(payload.get('branches', {}).get('connector', 'unknown'))}` | `{cell(payload.get('dirty_status', {}).get('connector', 'unknown'))}` |",
            f"| framework | `{cell(payload.get('framework_sha', 'unknown'))}` | `{cell(payload.get('branches', {}).get('framework', 'unknown'))}` | `{cell(payload.get('dirty_status', {}).get('framework', 'unknown'))}` |",
            f"| MRTS | `{cell(payload.get('mrts_sha', 'unknown'))}` | `{cell(payload.get('branches', {}).get('mrts', 'unknown'))}` | `{cell(payload.get('dirty_status', {}).get('mrts', 'unknown'))}` |",
            "",
            "## Proof Summary",
            "",
            "| Claim | Status | Evidence |",
            "|---|---|---|",
            f"| Runtime paths outside /root by default | `{cell('PASS' if not is_under_root_home(Path(payload.get('runtime_paths', {}).get('VERIFIED_RUN_ROOT', '/root'))) else 'FAIL')}` | `VERIFIED_RUN_ROOT={cell(payload.get('runtime_paths', {}).get('VERIFIED_RUN_ROOT', 'unknown'))}` |",
            f"| NGINX docroot preflight evidence | `{cell('PASS' if payload.get('worker_preflight') else 'UNKNOWN')}` | `nginx-worker-preflight.jsonl` rows are included when NGINX smoke ran |",
            f"| Verified inputs only | `PASS` | `{DATA_SOURCE_POLICY}` |",
        ]
    )
    return "\n".join(lines) + "\n"


def write_verified_manifest(
    *,
    connector_root: Path,
    framework_root: Path,
    build_root: Path,
    verified_run_id: str,
    started_at: str,
    finished_at: str,
    commands: list[dict[str, Any]],
    commands_file: Path,
    env: dict[str, str],
    profile: str,
    full_matrix_timeout: int | None,
    timeout_budgets: dict[str, int],
) -> None:
    mrts_root = framework_root / "tools/MRTS"
    proof = system_proof_summary(connector_root)
    reports = manifest_report_records(connector_root)
    runtime_path_records = runtime_path_report_rows(runtime_paths(env, build_root, verified_run_id), connector_root, framework_root)
    input_files = collect_declared_inputs(connector_root)
    payload = {
        "verified_run_id": verified_run_id,
        "data_source_policy": DATA_SOURCE_POLICY,
        "profile": profile,
        "full_matrix_timeout_seconds": full_matrix_timeout,
        "timeout_budgets": timeout_budgets,
        "runtime_paths": runtime_paths(env, build_root, verified_run_id),
        "runtime_path_rows": runtime_path_records,
        "worker_preflight": worker_preflight_rows(runtime_paths(env, build_root, verified_run_id), build_root),
        "started_at_utc": started_at,
        "finished_at_utc": finished_at,
        "duration_seconds": duration_seconds(started_at, finished_at),
        "connector_sha": git_sha(connector_root),
        "framework_sha": git_sha(framework_root),
        "mrts_sha": git_sha(mrts_root),
        "branches": {
            "connector": git_branch(connector_root),
            "framework": git_branch(framework_root),
            "mrts": git_branch(mrts_root) if mrts_root.exists() else "missing",
        },
        "dirty_status": {
            "connector": git_dirty_status(connector_root),
            "framework": git_dirty_status(framework_root),
            "mrts": git_dirty_status(mrts_root) if mrts_root.exists() else "missing",
        },
        "commands": commands,
        "command_file": file_record(commands_file, connector_root),
        "input_files": input_files,
        "output_files": generated_output_records(connector_root),
        "missing_inputs": [
            {"path": item.get("path"), "status": item.get("status"), "reason": item.get("notes", "input missing")}
            for item in input_files
            if item.get("status") in {"missing", "empty", "unknown", "stale"}
        ],
        "stale_inputs": [
            {"path": item.get("path"), "status": item.get("status"), "reason": item.get("notes", "input stale")}
            for item in input_files
            if item.get("status") == "stale"
        ],
        "skipped_reports": collect_report_statuses(connector_root, status_prefix="skipped"),
        "blocked_reports": collect_report_statuses(connector_root, status_prefix="blocked"),
        "failed_reports": collect_report_statuses(connector_root, status_values={"failed"}),
        "full_matrix_job_completeness": full_matrix_completeness_summary(connector_root),
        "runtime_mismatch_summary": runtime_mismatch_summary(connector_root),
        "tool_versions": proof["tools"],
        "system": proof["system"],
        "runtime_component_readiness": proof["runtime_component_readiness"],
        "runtime_producer_readiness_check": proof["runtime_producer_readiness_check"],
        "https_repo_url_policy": proof["https_repo_url_policy"],
        "report_refresh_manifest_reports": reports,
    }
    metadata = build_metadata(
        generated_by=GENERATED_REPORTS["verified_run_manifest"].generator,
        make_target=GENERATED_REPORTS["verified_run_manifest"].make_target,
        connector_root=connector_root,
        framework_root=framework_root,
        inputs=[
            commands_file,
            report_path(connector_root, "report_refresh_manifest", "json"),
            report_path(connector_root, "system_environment_proof", "json"),
            report_path(connector_root, "merge_readiness_dashboard", "json"),
        ],
        generated_at=finished_at,
        report_key="verified_run_manifest",
        extra={"mrts_sha": git_sha(mrts_root)},
    )
    metadata["input_status"] = manifest_input_status(payload, metadata.get("input_status", "unknown"))
    payload["input_status"] = metadata.get("input_status", "unknown")
    json_path = report_path(connector_root, "verified_run_manifest", "json")
    md_path = report_path(connector_root, "verified_run_manifest", "md")
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(generated_json_text(payload, metadata), encoding="utf-8")
    md_path.write_text(generated_markdown_text(render_markdown(payload), metadata), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector-root", default=".")
    parser.add_argument("--framework-root", default=None)
    parser.add_argument("--build-root", default=os.environ.get("BUILD_ROOT"))
    parser.add_argument(
        "--phase",
        choices=(
            "all",
            "runtime-producers",
            "report-refresh",
            "checks",
            "full-matrix-job",
            "full-matrix-resume",
            "producers",
            "consumers",
        ),
        default="all",
    )
    parser.add_argument("--connector", choices=("apache", "nginx", "haproxy"), default=None)
    parser.add_argument("--crs", choices=("no-crs", "with-crs"), default=None)
    parser.add_argument("--mrts", choices=("no-mrts", "with-mrts"), default=None)
    parser.add_argument("--mode", choices=("strict", "soft"), default="strict")
    parser.add_argument("--profile", choices=("full", "smoke"), default="full")
    parser.add_argument("--soft", action="store_true")
    args = parser.parse_args()

    connector_root = Path(args.connector_root).resolve()
    framework_root = Path(args.framework_root).resolve() if args.framework_root else connector_root / "modules/ModSecurity-test-Framework"
    initial_paths = verified_runtime_paths(os.environ)
    build_root = Path(args.build_root or initial_paths["BUILD_ROOT"]).resolve()
    paths = runtime_paths(dict(os.environ), build_root, os.environ.get("VERIFIED_RUN_ID", "pending"))
    prepare_runtime_roots(paths)
    current_run_file = build_root / "verified-runs" / "current-run-id"
    if not os.environ.get("VERIFIED_RUN_ID") and args.phase in {
        "report-refresh",
        "consumers",
        "checks",
        "full-matrix-job",
        "full-matrix-resume",
    }:
        try:
            previous_run_id = current_run_file.read_text(encoding="utf-8").strip()
        except OSError:
            previous_run_id = ""
        if previous_run_id:
            os.environ["VERIFIED_RUN_ID"] = previous_run_id
    os.environ.setdefault("VERIFIED_RUN_ID", current_verified_run_id(connector_root))
    verified_run_id = os.environ["VERIFIED_RUN_ID"]
    started_at = utc_now()
    paths = runtime_paths(dict(os.environ), build_root, verified_run_id)
    prepare_runtime_roots(paths)
    run_root = build_root / "verified-runs" / verified_run_id
    logs_dir = run_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    current_run_file.parent.mkdir(parents=True, exist_ok=True)
    current_run_file.write_text(verified_run_id + "\n", encoding="utf-8")
    commands_file = run_root / "verified-commands.json"

    env = dict(os.environ)
    runtime_matrix_timeout = timeout_from_env(env, "VERIFIED_RUN_RUNTIME_MATRIX_TIMEOUT_SECONDS", 1800)
    full_matrix_runtime_timeout = timeout_from_env(
        env,
        "VERIFIED_RUN_FULL_MATRIX_RUNTIME_TIMEOUT_SECONDS",
        7200,
        aliases=("VERIFIED_RUN_FULL_MATRIX_TIMEOUT_SECONDS",),
    )
    report_refresh_timeout = timeout_from_env(env, "VERIFIED_RUN_REPORT_REFRESH_TIMEOUT_SECONDS", 1800)
    native_mrts_timeout = timeout_from_env(env, "VERIFIED_RUN_NATIVE_MRTS_TIMEOUT_SECONDS", 1800)
    full_matrix_job_timeout = timeout_from_env(env, "VERIFIED_RUN_FULL_MATRIX_JOB_TIMEOUT_SECONDS", 3600)
    full_matrix_total_timeout = timeout_from_env(env, "VERIFIED_RUN_FULL_MATRIX_TOTAL_TIMEOUT_SECONDS", 14400)
    env.update(
        {
            "CONNECTOR_ROOT": str(connector_root),
            "FRAMEWORK_ROOT": str(framework_root),
            "VERIFIED_RUN_ROOT": paths["VERIFIED_RUN_ROOT"],
            "VERIFIED_STATE_ROOT": paths["VERIFIED_STATE_ROOT"],
            "VERIFIED_BUILD_ROOT": paths["VERIFIED_BUILD_ROOT"],
            "VERIFIED_SOURCE_ROOT": paths["VERIFIED_SOURCE_ROOT"],
            "VERIFIED_TMP_ROOT": paths["VERIFIED_TMP_ROOT"],
            "VERIFIED_LOG_ROOT": paths["VERIFIED_LOG_ROOT"],
            "VERIFIED_COMPONENT_CACHE": paths["VERIFIED_COMPONENT_CACHE"],
            "BUILD_ROOT": str(build_root),
            "SOURCE_ROOT": paths["SOURCE_ROOT"],
            "TMP_ROOT": paths["TMP_ROOT"],
            "LOG_ROOT": paths["LOG_ROOT"],
            "CONNECTOR_COMPONENT_CACHE": paths["CONNECTOR_COMPONENT_CACHE"],
            "NGINX_HARNESS_PARENT": paths["NGINX_HARNESS_PARENT"],
            "MATRIX_ROOT": paths["MATRIX_ROOT"],
            "FULL_MATRIX_MANIFEST": str(Path(paths["MATRIX_ROOT"]) / "full-runtime-matrix-runs.jsonl"),
            "MRTS_BUILD_ROOT": paths["MRTS_BUILD_ROOT"],
            "MRTS_NATIVE_ROOT": paths["MRTS_NATIVE_ROOT"],
            "VERIFIED_RUN_ID": verified_run_id,
            "VERIFIED_RUN_STARTED_AT": started_at,
            "VERIFIED_RUN_LOG_ROOT": str(logs_dir),
            "VERIFIED_RUN_COMMANDS_FILE": str(commands_file),
            "VERIFIED_RUN_PROFILE": args.profile,
            "VERIFIED_RUN_RUNTIME_MATRIX_TIMEOUT_SECONDS": str(runtime_matrix_timeout),
            "VERIFIED_RUN_FULL_MATRIX_RUNTIME_TIMEOUT_SECONDS": str(full_matrix_runtime_timeout),
            "VERIFIED_RUN_FULL_MATRIX_TIMEOUT_SECONDS": str(full_matrix_runtime_timeout),
            "VERIFIED_RUN_REPORT_REFRESH_TIMEOUT_SECONDS": str(report_refresh_timeout),
            "VERIFIED_RUN_NATIVE_MRTS_TIMEOUT_SECONDS": str(native_mrts_timeout),
            "VERIFIED_RUN_FULL_MATRIX_JOB_TIMEOUT_SECONDS": str(full_matrix_job_timeout),
            "VERIFIED_RUN_FULL_MATRIX_TOTAL_TIMEOUT_SECONDS": str(full_matrix_total_timeout),
            "PYTHONDONTWRITEBYTECODE": env.get("PYTHONDONTWRITEBYTECODE", "1"),
        }
    )

    if args.phase == "full-matrix-job":
        if not args.connector or not args.crs or not args.mrts:
            parser.error("--phase full-matrix-job requires --connector, --crs, and --mrts")
        plan = [
            {
                "phase": "full-matrix-job",
                "command": [
                    "make",
                    "full-matrix-single-job-runtime",
                    f"CONNECTOR={args.connector}",
                    f"CRS={args.crs}",
                    f"MRTS={args.mrts}",
                ],
                "logical_target": f"full-matrix-job:{args.connector}:{args.crs}:{args.mrts}",
                "required": True,
                "optional": False,
                "affected_reports": ["full_matrix_job_completeness", "verified_runtime_mismatch_analysis"],
                "timeout_seconds": full_matrix_job_timeout,
            },
            {
                "phase": "full-matrix-job",
                "command": ["make", "generate-full-matrix-job-completeness"],
                "logical_target": "generate-full-matrix-job-completeness",
                "required": False,
                "optional": True,
                "affected_reports": ["full_matrix_job_completeness"],
                "timeout_seconds": report_refresh_timeout,
            },
        ]
    elif args.phase == "full-matrix-resume":
        plan = [
            {
                "phase": "full-matrix-resume",
                "command": ["make", "full-matrix-resume-runtime"],
                "logical_target": "full-matrix-resume",
                "required": True,
                "optional": False,
                "affected_reports": ["full_matrix_job_completeness", "verified_runtime_mismatch_analysis"],
                "timeout_seconds": full_matrix_total_timeout,
            },
            {
                "phase": "full-matrix-resume",
                "command": ["make", "generate-full-matrix-job-completeness"],
                "logical_target": "generate-full-matrix-job-completeness",
                "required": False,
                "optional": True,
                "affected_reports": ["full_matrix_job_completeness"],
                "timeout_seconds": report_refresh_timeout,
            },
            {
                "phase": "full-matrix-resume",
                "command": ["make", "generate-verified-runtime-mismatch-analysis"],
                "logical_target": "generate-verified-runtime-mismatch-analysis",
                "required": False,
                "optional": True,
                "affected_reports": ["verified_runtime_mismatch_analysis"],
                "timeout_seconds": report_refresh_timeout,
            },
        ]
    else:
        plan = select_commands(
            command_plan(
                runtime_matrix_timeout=runtime_matrix_timeout,
                full_matrix_runtime_timeout=full_matrix_runtime_timeout,
                report_refresh_timeout=report_refresh_timeout,
                native_mrts_timeout=native_mrts_timeout,
                profile=args.profile,
            ),
            args.phase,
        )
    timeout_budgets = {
        "runtime_matrix": runtime_matrix_timeout,
        "full_matrix_runtime": full_matrix_runtime_timeout,
        "full_matrix_job": full_matrix_job_timeout,
        "full_matrix_total": full_matrix_total_timeout,
        "report_refresh": report_refresh_timeout,
        "native_mrts": native_mrts_timeout,
    }
    existing_payload = read_json(commands_file)
    existing_commands = existing_payload.get("commands") if isinstance(existing_payload.get("commands"), list) else []
    append_phases = {"report-refresh", "consumers", "checks", "full-matrix-job", "full-matrix-resume"}
    command_records: list[dict[str, Any]] = list(existing_commands) if args.phase in append_phases else []
    run_started_at = str(existing_payload.get("started_at_utc") or started_at) if command_records else started_at
    write_commands_file(
        commands_file,
        {
            "verified_run_id": verified_run_id,
            "data_source_policy": DATA_SOURCE_POLICY,
            "profile": args.profile,
            "phase": args.phase,
            "started_at_utc": run_started_at,
            "commands": command_records,
        },
    )
    write_verified_manifest(
        connector_root=connector_root,
        framework_root=framework_root,
        build_root=build_root,
        verified_run_id=verified_run_id,
        started_at=run_started_at,
        finished_at=started_at,
        commands=command_records,
        commands_file=commands_file,
        env=env,
        profile=args.profile,
        full_matrix_timeout=full_matrix_runtime_timeout,
        timeout_budgets=timeout_budgets,
    )
    next_log_index = len(command_records) + 1
    for index, item in enumerate(plan, start=next_log_index):
        command = list(item["command"])
        target = str(item.get("logical_target") or (command[1] if len(command) == 2 and command[0] == "make" else ""))
        readiness_blocked = any(
            record.get("logical_target") == "check-runtime-producer-readiness"
            and record.get("return_code") != 0
            for record in command_records
        )
        if readiness_blocked and target in {"runtime-matrix-all", "full-matrix-parallel", "mrts-native-full-run"}:
            record = skipped_command_record(
                command,
                logs_dir=logs_dir,
                index=index,
                phase=str(item["phase"]),
                required=bool(item["required"]),
                optional=bool(item["optional"]),
                affected_reports=list(item.get("affected_reports", [])),
                reason="check-runtime-producer-readiness did not pass",
                logical_target=target,
            )
            print(f"verified-report-run: {record['status']} {target}: {record['notes']} log={record['log_path']}", flush=True)
        else:
            record = run_command(
                command,
                cwd=connector_root,
                env=env,
                logs_dir=logs_dir,
                index=index,
                phase=str(item["phase"]),
                required=bool(item["required"]),
                optional=bool(item["optional"]),
                timeout_seconds=item.get("timeout_seconds"),
                affected_reports=list(item.get("affected_reports", [])),
                logical_target=target,
            )
        record = apply_command_semantics(record, env, args.profile)
        command_records.append(record)
        last_updated = utc_now()
        write_commands_file(
            commands_file,
            {
                "verified_run_id": verified_run_id,
                "data_source_policy": DATA_SOURCE_POLICY,
                "profile": args.profile,
                "phase": args.phase,
                "started_at_utc": run_started_at,
                "last_updated_at_utc": last_updated,
                "commands": command_records,
            },
        )
        write_verified_manifest(
            connector_root=connector_root,
            framework_root=framework_root,
            build_root=build_root,
            verified_run_id=verified_run_id,
            started_at=run_started_at,
            finished_at=last_updated,
            commands=command_records,
            commands_file=commands_file,
            env=env,
            profile=args.profile,
            full_matrix_timeout=full_matrix_runtime_timeout,
            timeout_budgets=timeout_budgets,
        )

    finished_at = utc_now()
    write_commands_file(
        commands_file,
        {
            "verified_run_id": verified_run_id,
            "data_source_policy": DATA_SOURCE_POLICY,
            "profile": args.profile,
            "phase": args.phase,
            "started_at_utc": run_started_at,
            "finished_at_utc": finished_at,
            "commands": command_records,
        },
    )
    write_verified_manifest(
        connector_root=connector_root,
        framework_root=framework_root,
        build_root=build_root,
        verified_run_id=verified_run_id,
        started_at=run_started_at,
        finished_at=finished_at,
        commands=command_records,
        commands_file=commands_file,
        env=env,
        profile=args.profile,
        full_matrix_timeout=full_matrix_runtime_timeout,
        timeout_budgets=timeout_budgets,
    )

    failed = [
        record
        for record in command_records
        if record["return_code"] != 0 and record.get("required") and not record.get("optional")
    ]
    soft_mode = args.soft or args.mode == "soft"
    if failed and not soft_mode:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
