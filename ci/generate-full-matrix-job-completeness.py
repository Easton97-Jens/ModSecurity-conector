#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from generated_report_utils import (
    DATA_SOURCE_POLICY,
    GENERATED_REPORTS,
    build_metadata,
    generated_json_text,
    generated_markdown_text,
    git_sha,
    report_path,
)


CONNECTORS = ("apache", "nginx", "haproxy")
VARIANTS = (("no-crs", "no-mrts"), ("no-crs", "with-mrts"), ("with-crs", "no-mrts"), ("with-crs", "with-mrts"))


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_record(path: Path, label: str) -> dict[str, Any]:
    if not path.is_file():
        return {"label": label, "path": str(path), "status": "missing", "sha256": "missing"}
    return {
        "label": label,
        "path": str(path),
        "status": "present",
        "sha256": sha256_file(path),
        "bytes": path.stat().st_size,
        "mtime_utc": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
    }


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


def job_id(connector: str, crs: str, mrts: str) -> str:
    return f"{connector}:{crs}:{mrts}"


def summary_candidates(job_root: Path, connector: str) -> list[Path]:
    return [
        job_root / "results" / f"{connector}-summary.json",
        job_root / "results" / "force-all" / f"{connector}-summary.json",
    ]


def result_jsonl_path(job_root: Path, connector: str) -> Path:
    return job_root / "results" / "force-all" / f"{connector}-results.jsonl"


def summary_path(job_root: Path, connector: str) -> Path:
    summary_file = job_root / "summary.path"
    if summary_file.is_file():
        raw = summary_file.read_text(encoding="utf-8", errors="replace").strip()
        if raw:
            return Path(raw)
    for candidate in summary_candidates(job_root, connector):
        if candidate.is_file():
            return candidate
    return summary_candidates(job_root, connector)[0]


def count_summary_cases(path: Path, connector: str) -> dict[str, Any]:
    data = read_json(path)
    root = data.get(connector) if isinstance(data.get(connector), dict) else {}
    cases = root.get("cases") if isinstance(root.get("cases"), dict) else {}
    statuses = Counter(str(case.get("status", "unknown")) for case in cases.values() if isinstance(case, dict))
    attempted = root.get("attempted")
    if not isinstance(attempted, int):
        attempted = len(cases)
    return {
        "cases": len(cases),
        "attempted": attempted,
        "pass": statuses.get("pass", 0),
        "fail": statuses.get("fail", 0),
        "blocked": statuses.get("blocked", 0),
        "not_executable": statuses.get("not_executable", 0),
        "status_counts": dict(sorted(statuses.items())),
        "source": "summary_json",
    }


def count_jsonl_cases(path: Path) -> dict[str, Any]:
    rows = read_jsonl(path)
    statuses = Counter(str(row.get("status", "unknown")) for row in rows)
    actual = Counter(str(row.get("actual_status", row.get("observed_status", "unknown"))) for row in rows)
    return {
        "cases": len(rows),
        "attempted": len(rows),
        "pass": statuses.get("pass", 0),
        "fail": statuses.get("fail", 0),
        "blocked": statuses.get("blocked", 0),
        "not_executable": statuses.get("not_executable", 0),
        "status_counts": dict(sorted(statuses.items())),
        "actual_status_counts": dict(sorted(actual.items())),
        "source": "results_jsonl",
    }


def read_manifest_rows(manifest_path: Path) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for row in read_jsonl(manifest_path):
        connector = str(row.get("connector") or "")
        crs = str(row.get("test_variant") or row.get("crs") or "")
        mrts = str(row.get("mrts_variant") or row.get("mrts") or "")
        if connector and crs and mrts:
            rows[job_id(connector, crs, mrts)] = row
    return rows


def detect_job_status(job: dict[str, Any], log_path: Path, jsonl_path: Path) -> tuple[str, str]:
    if job:
        rc = job.get("return_code")
        if rc == 0:
            return "completed", "job.json exists with rc=0"
        return "completed_with_mismatches", f"job.json exists with rc={rc}"
    if log_path.is_file():
        log = log_path.read_text(encoding="utf-8", errors="replace")
        if "Terminated" in log or "timeout" in log.lower():
            return "timeout_or_incomplete", "run.log ends with termination/timeout evidence"
        if jsonl_path.is_file():
            return "incomplete", "partial results exist but job.json is missing"
        return "incomplete", "run.log exists but job.json is missing"
    return "not_started", "no job.json or run.log found"


def analyze_nginx_with_crs_mrts(matrix_root: Path) -> dict[str, Any]:
    job_root = matrix_root / "with-crs" / "with-mrts" / "nginx"
    log_path = job_root / "run.log"
    jsonl_path = result_jsonl_path(job_root, "nginx")
    lines = log_path.read_text(encoding="utf-8", errors="replace").splitlines() if log_path.is_file() else []
    running_cases = []
    fail_cases = []
    observed_500 = 0
    terminated = False
    for line in lines:
        if "nginx_smoke: running case=" in line:
            running_cases.append(line.split("case=", 1)[1].split()[0])
        if line.startswith("FAIL "):
            fail_cases.append(line.split(None, 1)[1] if " " in line else line)
        if "observed=500" in line or "observed 500" in line:
            observed_500 += 1
        if "Terminated" in line or "lock-release" in line and "Bad file descriptor" in line:
            terminated = True
    partial = count_jsonl_cases(jsonl_path) if jsonl_path.is_file() else {}
    return {
        "job_id": job_id("nginx", "with-crs", "with-mrts"),
        "log_path": str(log_path),
        "results_jsonl": str(jsonl_path),
        "run_log_lines": len(lines),
        "running_case_lines": len(running_cases),
        "fail_lines": len(fail_cases),
        "observed_500_lines": observed_500,
        "terminated": terminated,
        "last_running_case": running_cases[-1] if running_cases else "",
        "last_fail_case": fail_cases[-1] if fail_cases else "",
        "partial_result_counts": partial,
        "findings": [
            "The previous run was killed while NGINX with-crs/with-mrts was still executing MRTS request-cookie-name cases.",
            "The partial NGINX job produced result JSONL but no summary JSON and no job.json, so it cannot count as complete evidence.",
            "Observed failures are dominated by HTTP 500 responses in the NGINX harness for this variant.",
            "Current connector smoke runners expose TEST_CASE/SMOKE_CASES filters but no stable shard index contract for Full-Matrix merge semantics.",
        ],
        "sharding_note": (
            "Add sharding at the case-list stage in connectors/*/harness/run_*_smoke.sh, after case_cli list-cases "
            "and before the force-all loop, then write shard metadata into job.json and merge shards in this report."
        ),
    }


def collect_jobs(matrix_root: Path, manifest_path: Path) -> list[dict[str, Any]]:
    manifest = read_manifest_rows(manifest_path)
    rows: list[dict[str, Any]] = []
    for crs, mrts in VARIANTS:
        for connector in CONNECTORS:
            jid = job_id(connector, crs, mrts)
            job_root = matrix_root / crs / mrts / connector
            job_path = job_root / "job.json"
            log_path = job_root / "run.log"
            build_manifest = job_root / "build-manifest.json"
            summary = summary_path(job_root, connector)
            jsonl = result_jsonl_path(job_root, connector)
            preamble = job_root / "preambles" / f"{connector}-{crs}-{mrts}.load"
            job = read_json(job_path)
            status, reason = detect_job_status(job, log_path, jsonl)
            counts = {}
            if summary.is_file():
                counts = count_summary_cases(summary, connector)
            elif jsonl.is_file():
                counts = count_jsonl_cases(jsonl)
            manifest_row = manifest.get(jid, {})
            duration = job.get("duration_seconds", manifest_row.get("duration_seconds"))
            rows.append(
                {
                    "job_id": jid,
                    "connector": connector,
                    "crs": crs,
                    "mrts": mrts,
                    "status": status,
                    "reason": reason,
                    "manifest_recorded": bool(manifest_row),
                    "return_code": job.get("return_code", manifest_row.get("return_code")),
                    "started_at": job.get("started_at", manifest_row.get("started_at", "")),
                    "ended_at": job.get("ended_at", manifest_row.get("ended_at", "")),
                    "duration_seconds": duration if isinstance(duration, int) else None,
                    "cases": counts.get("cases", 0),
                    "attempted": counts.get("attempted", 0),
                    "pass": counts.get("pass", 0),
                    "fail": counts.get("fail", 0),
                    "blocked": counts.get("blocked", 0),
                    "not_executable": counts.get("not_executable", 0),
                    "status_counts": counts.get("status_counts", {}),
                    "actual_status_counts": counts.get("actual_status_counts", {}),
                    "job_path": str(job_path),
                    "log_path": str(log_path),
                    "summary_path": str(summary),
                    "results_jsonl": str(jsonl),
                    "result_path": str(summary if summary.is_file() else jsonl),
                    "input_hashes": [
                        file_record(job_path, "job_json"),
                        file_record(log_path, "run_log"),
                        file_record(summary, "summary_json"),
                        file_record(jsonl, "results_jsonl"),
                        file_record(build_manifest, "build_manifest"),
                        file_record(preamble, "rule_preamble"),
                    ],
                }
            )
    return rows


def rewrite_manifest(path: Path, jobs: list[dict[str, Any]]) -> None:
    completed = [job for job in jobs if job["status"] in {"completed", "completed_with_mismatches"}]
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for job in completed:
        row = {
            "connector": job["connector"],
            "test_variant": job["crs"],
            "mrts_variant": job["mrts"],
            "return_code": job["return_code"],
            "started_at": job["started_at"],
            "ended_at": job["ended_at"],
            "duration_seconds": job["duration_seconds"],
            "results_dir": str(Path(job["job_path"]).parent / "results"),
            "summary_path": job["summary_path"],
            "log_path": job["log_path"],
        }
        lines.append(json.dumps(row, sort_keys=True))
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def markdown_table(rows: list[list[Any]]) -> list[str]:
    return ["| " + " | ".join(str(cell) for cell in row) + " |" for row in rows]


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Full-Matrix Job Completeness",
        "",
        f"Verified run id: `{payload['verified_run_id']}`",
        "",
        "## Summary",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Complete jobs | `{payload['complete_jobs']}/{payload['total_jobs']}` |",
        f"| Manifest-recorded jobs | `{payload['manifest_recorded_jobs']}/{payload['total_jobs']}` |",
        f"| Overall status | `{payload['overall_status']}` |",
        f"| Evidence scope | `{payload['evidence_scope']}` |",
        f"| Missing jobs | `{', '.join(payload['missing_job_ids']) or '-'}` |",
        "",
        "## Jobs",
        "",
    ]
    lines.extend(
        markdown_table(
            [
                ["Job", "Connector", "CRS", "MRTS", "Status", "Duration", "Cases", "Failures", "Log"],
                ["---", "---", "---", "---", "---", "---:", "---:", "---:", "---"],
                *[
                    [
                        f"`{job['job_id']}`",
                        job["connector"],
                        job["crs"],
                        job["mrts"],
                        f"`{job['status']}`",
                        job["duration_seconds"] if job["duration_seconds"] is not None else "-",
                        job["cases"],
                        job["fail"],
                        f"`{job['log_path']}`",
                    ]
                    for job in payload["jobs"]
                ],
            ]
        )
    )
    lines.extend(["", "## Completed Jobs", ""])
    lines.extend(
        markdown_table(
            [
                ["Job", "Duration", "RC", "Failures"],
                ["---", "---:", "-:", "---:"],
                *[
                    [f"`{job['job_id']}`", job["duration_seconds"], job["return_code"], job["fail"]]
                    for job in payload["jobs"]
                    if job["status"] in {"completed", "completed_with_mismatches"}
                ],
            ]
        )
    )
    lines.extend(["", "## Missing / Timeout Jobs", ""])
    missing_rows = [
        [
            f"`{job['job_id']}`",
            job["reason"],
            f"`make verified-full-matrix-job CONNECTOR={job['connector']} CRS={job['crs']} MRTS={job['mrts']}`",
        ]
        for job in payload["jobs"]
        if job["status"] not in {"completed", "completed_with_mismatches"}
    ]
    if missing_rows:
        lines.extend(markdown_table([["Job", "Reason", "Next Command"], ["---", "---", "---"], *missing_rows]))
    else:
        lines.append("Missing/Empty: no missing or timed-out Full-Matrix jobs.")
    lines.extend(["", "## Slowest Jobs", ""])
    lines.extend(
        markdown_table(
            [
                ["Job", "Duration", "Notes"],
                ["---", "---:", "---"],
                *[
                    [f"`{job['job_id']}`", job["duration_seconds"], job["reason"]]
                    for job in payload["slowest_jobs"]
                ],
            ]
        )
    )
    lines.extend(["", "## NGINX with-crs/with-mrts Runtime Analysis", ""])
    nginx = payload["nginx_with_crs_with_mrts_analysis"]
    lines.extend(
        [
            f"- Last running case: `{nginx.get('last_running_case') or '-'}`",
            f"- Last failed case: `{nginx.get('last_fail_case') or '-'}`",
            f"- Run log lines: `{nginx.get('run_log_lines', 0)}`",
            f"- Running-case lines: `{nginx.get('running_case_lines', 0)}`",
            f"- FAIL lines: `{nginx.get('fail_lines', 0)}`",
            f"- Observed 500 lines: `{nginx.get('observed_500_lines', 0)}`",
            f"- Terminated evidence: `{str(nginx.get('terminated', False)).lower()}`",
            f"- Partial result rows: `{nginx.get('partial_result_counts', {}).get('cases', 0)}`",
            "",
        ]
    )
    for finding in nginx.get("findings", []):
        lines.append(f"- {finding}")
    lines.extend(["", "## Sharding Note", "", nginx.get("sharding_note", "")])
    lines.extend(["", "## Inputs", ""])
    lines.extend(
        markdown_table(
            [
                ["Input", "Status", "SHA256"],
                ["---", "---", "---"],
                *[[f"`{item['path']}`", item["status"], f"`{item['sha256']}`"] for item in payload["inputs"]],
            ]
        )
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector-root", default=".")
    parser.add_argument("--framework-root", default=None)
    parser.add_argument("--build-root", default=None)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--verified-run-id", default="")
    parser.add_argument("--verified-commands-file", default="")
    parser.add_argument("--rewrite-manifest", action="store_true")
    args = parser.parse_args()

    connector_root = Path(args.connector_root).resolve()
    framework_root = Path(args.framework_root).resolve() if args.framework_root else connector_root / "modules/ModSecurity-test-Framework"
    build_root = Path(args.build_root or Path.home() / ".local/state/ModSecurity-conector-build").resolve()
    output_dir = Path(args.output_dir).resolve() if args.output_dir else connector_root / "reports/testing/generated/manifest"
    matrix_root = build_root / "full-matrix"
    manifest_path = matrix_root / "full-runtime-matrix-runs.jsonl"
    commands_path = Path(args.verified_commands_file) if args.verified_commands_file else build_root / "verified-runs/current-run-id"
    verified_run_id = args.verified_run_id
    if not verified_run_id:
        current = build_root / "verified-runs" / "current-run-id"
        verified_run_id = current.read_text(encoding="utf-8").strip() if current.is_file() else ""
    if not verified_run_id:
        verified_run_id = "unknown"
    verified_commands = build_root / "verified-runs" / verified_run_id / "verified-commands.json"
    if args.verified_commands_file:
        verified_commands = Path(args.verified_commands_file)

    jobs = collect_jobs(matrix_root, manifest_path)
    if args.rewrite_manifest:
        rewrite_manifest(manifest_path, jobs)
        jobs = collect_jobs(matrix_root, manifest_path)
    complete = sum(1 for job in jobs if job["status"] in {"completed", "completed_with_mismatches"})
    manifest_recorded = sum(1 for job in jobs if job["manifest_recorded"])
    missing = [job for job in jobs if job["status"] not in {"completed", "completed_with_mismatches"}]
    slowest = sorted(
        [job for job in jobs if isinstance(job.get("duration_seconds"), int)],
        key=lambda item: int(item["duration_seconds"]),
        reverse=True,
    )[:5]
    inputs = [
        file_record(manifest_path, "full_matrix_manifest"),
        file_record(verified_commands, "verified_commands"),
    ]
    for job in jobs:
        inputs.extend(item for item in job["input_hashes"] if item["status"] == "present")
    dedup_inputs = {item["path"]: item for item in inputs}
    payload = {
        "verified_run_id": verified_run_id,
        "generated_at_utc": utc_now(),
        "data_source_policy": DATA_SOURCE_POLICY,
        "connector_sha": git_sha(connector_root),
        "framework_sha": git_sha(framework_root),
        "matrix_root": str(matrix_root),
        "manifest_path": str(manifest_path),
        "total_jobs": len(jobs),
        "complete_jobs": complete,
        "manifest_recorded_jobs": manifest_recorded,
        "missing_jobs": missing,
        "missing_job_ids": [job["job_id"] for job in missing],
        "overall_status": "complete" if complete == len(jobs) else "incomplete",
        "evidence_scope": "full" if complete == len(jobs) else "partial",
        "jobs": jobs,
        "slowest_jobs": slowest,
        "nginx_with_crs_with_mrts_analysis": analyze_nginx_with_crs_mrts(matrix_root),
        "inputs": list(dedup_inputs.values()),
    }
    metadata = build_metadata(
        generated_by=GENERATED_REPORTS["full_matrix_job_completeness"].generator,
        make_target=GENERATED_REPORTS["full_matrix_job_completeness"].make_target,
        connector_root=connector_root,
        framework_root=framework_root,
        report_key="full_matrix_job_completeness",
        inputs=[item["path"] for item in dedup_inputs.values()],
        extra={"verified_run_id": verified_run_id},
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / GENERATED_REPORTS["full_matrix_job_completeness"].filename("json")
    md_path = output_dir / GENERATED_REPORTS["full_matrix_job_completeness"].filename("md")
    json_path.write_text(generated_json_text(payload, metadata), encoding="utf-8")
    md_path.write_text(generated_markdown_text(render_markdown(payload), metadata), encoding="utf-8")
    print(md_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
