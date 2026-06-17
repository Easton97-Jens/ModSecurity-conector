#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

from generated_report_utils import utc_now
from runtime_path_utils import verified_runtime_paths


CONNECTORS = {"apache", "nginx", "haproxy"}
CRS_VARIANTS = {"no-crs", "with-crs"}
MRTS_VARIANTS = {"no-mrts", "with-mrts"}


def safe_token(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in {"-", "_"} else "-" for ch in value)


def read_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def job_root(matrix_root: Path, connector: str, crs: str, mrts: str) -> Path:
    return matrix_root / crs / mrts / connector


def count_jsonl_rows(path: Path) -> int:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return 0
    count = 0
    for line in lines:
        if line.strip():
            count += 1
    return count


def job_artifacts(root: Path, connector: str) -> dict:
    job_path = root / "job.json"
    data = read_json(job_path)
    summary_path = Path(str(data.get("summary_path") or ""))
    if not summary_path.is_absolute():
        summary_path = root / "results" / "force-all" / f"{connector}-summary.json"
    results_jsonl = root / "results" / "force-all" / f"{connector}-results.jsonl"
    summary = read_json(summary_path)
    connector_summary = summary.get(connector) if isinstance(summary.get(connector), dict) else {}
    cases = connector_summary.get("cases") if isinstance(connector_summary.get("cases"), dict) else {}
    result_rows = count_jsonl_rows(results_jsonl)
    status = str(data.get("status") or "")
    complete = (
        bool(data.get("ended_at"))
        and "return_code" in data
        and status in {"completed", "completed_with_mismatches"}
        and summary_path.is_file()
        and (result_rows > 0 or bool(cases))
    )
    return {
        "complete": complete,
        "job": data,
        "summary_path": str(summary_path),
        "results_jsonl": str(results_jsonl),
        "result_rows": result_rows,
        "summary_cases": len(cases),
    }


def job_complete(path: Path) -> bool:
    data = read_json(path)
    status = str(data.get("status") or "")
    return bool(data.get("ended_at")) and "return_code" in data and status in {"completed", "completed_with_mismatches"}


def run_completeness(
    connector_root: Path,
    framework_root: Path,
    build_root: Path,
    verified_run_id: str,
    verified_commands_file: str,
) -> int:
    cmd = [
        sys.executable,
        str(connector_root / "ci/generate-full-matrix-job-completeness.py"),
        "--connector-root",
        str(connector_root),
        "--framework-root",
        str(framework_root),
        "--build-root",
        str(build_root),
        "--verified-run-id",
        verified_run_id,
        "--rewrite-manifest",
    ]
    if verified_commands_file:
        cmd.extend(["--verified-commands-file", verified_commands_file])
    return subprocess.run(cmd, cwd=str(connector_root)).returncode


def write_timeout_record(root: Path, connector: str, crs: str, mrts: str, started_at: str, duration: float) -> None:
    root.mkdir(parents=True, exist_ok=True)
    payload = {
        "connector": connector,
        "job_id": f"{connector}:{crs}:{mrts}",
        "test_variant": crs,
        "mrts_variant": mrts,
        "status": "timeout",
        "return_code": -15,
        "started_at": started_at,
        "ended_at": utc_now(),
        "duration_seconds": round(duration, 3),
        "log_path": str(root / "run.log"),
        "results_dir": str(root / "results"),
    }
    (root / "job-timeout.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector", required=True, choices=sorted(CONNECTORS))
    parser.add_argument("--crs", required=True, choices=sorted(CRS_VARIANTS))
    parser.add_argument("--mrts", required=True, choices=sorted(MRTS_VARIANTS))
    parser.add_argument("--connector-root", default=".")
    parser.add_argument("--framework-root", default=None)
    parser.add_argument("--build-root", default=os.environ.get("BUILD_ROOT"))
    parser.add_argument("--timeout-seconds", type=int, default=int(os.environ.get("VERIFIED_RUN_FULL_MATRIX_JOB_TIMEOUT_SECONDS", "3600")))
    parser.add_argument("--finalize-grace-seconds", type=int, default=int(os.environ.get("VERIFIED_RUN_JOB_FINALIZE_GRACE_SECONDS", "60")))
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    connector_root = Path(args.connector_root).resolve()
    framework_root = Path(args.framework_root).resolve() if args.framework_root else connector_root / "modules/ModSecurity-test-Framework"
    default_paths = verified_runtime_paths(os.environ)
    build_root = Path(args.build_root or default_paths["BUILD_ROOT"]).resolve()
    matrix_root = Path(os.environ.get("MATRIX_ROOT", str(build_root / "full-matrix"))).resolve()
    verified_run_id = os.environ.get("VERIFIED_RUN_ID", "")
    if not verified_run_id:
        current = build_root / "verified-runs/current-run-id"
        verified_run_id = current.read_text(encoding="utf-8").strip() if current.is_file() else utc_now().replace(":", "-")
    verified_commands_file = os.environ.get("VERIFIED_RUN_COMMANDS_FILE", "")

    root = job_root(matrix_root, args.connector, args.crs, args.mrts)
    if not args.force and job_artifacts(root, args.connector)["complete"]:
        print(f"full-matrix-job: skip complete job {args.connector}:{args.crs}:{args.mrts}")
        return run_completeness(connector_root, framework_root, build_root, verified_run_id, verified_commands_file)

    stamp = utc_now().replace(":", "-")
    jid = safe_token(f"{args.connector}-{args.crs}-{args.mrts}")
    temp_manifest = matrix_root / "_job-manifests" / verified_run_id / f"{jid}-{stamp}.jsonl"
    temp_report_dir = matrix_root / "_job-reports" / verified_run_id / jid
    temp_manifest.parent.mkdir(parents=True, exist_ok=True)
    temp_report_dir.mkdir(parents=True, exist_ok=True)

    env = dict(os.environ)
    env.update(
        {
            "CONNECTOR_ROOT": str(connector_root),
            "FRAMEWORK_ROOT": str(framework_root),
            "BUILD_ROOT": str(build_root),
            "MATRIX_ROOT": str(matrix_root),
            "FULL_MATRIX_VARIANTS": f"{args.crs}/{args.mrts}",
            "FULL_MATRIX_CONNECTORS": args.connector,
            "FULL_MATRIX_MANIFEST": str(temp_manifest),
            "FULL_MATRIX_REPORT_DIR": str(temp_report_dir),
            "FULL_MATRIX_TRUNCATE_MANIFEST": "1",
            "FULL_MATRIX_SKIP_REPORTS": "1",
            "VERIFIED_RUN_ID": verified_run_id,
        }
    )
    cmd = ["sh", str(connector_root / "ci/run-full-matrix-parallel.sh")]
    started_at = utc_now()
    started = time.monotonic()
    process = subprocess.Popen(cmd, cwd=str(connector_root), env=env, start_new_session=True)
    try:
        rc = process.wait(timeout=args.timeout_seconds)
    except subprocess.TimeoutExpired:
        print(
            f"full-matrix-job: timeout after {args.timeout_seconds}s for {args.connector}:{args.crs}:{args.mrts}",
            flush=True,
        )
        if args.finalize_grace_seconds > 0:
            print(
                f"full-matrix-job: waiting {args.finalize_grace_seconds}s finalize grace for job artifacts",
                flush=True,
            )
            try:
                rc = process.wait(timeout=args.finalize_grace_seconds)
            except subprocess.TimeoutExpired:
                rc = None
            if rc is not None:
                artifacts = job_artifacts(root, args.connector)
                if artifacts["complete"]:
                    print(
                        "full-matrix-job: completed during finalize grace; using job artifacts as source of truth",
                        flush=True,
                    )
                    run_completeness(connector_root, framework_root, build_root, verified_run_id, verified_commands_file)
                    return int(artifacts["job"].get("return_code", rc))
        artifacts = job_artifacts(root, args.connector)
        if artifacts["complete"]:
            print(
                "full-matrix-job: timeout after completed job artifacts were written; using job artifacts as source of truth",
                flush=True,
            )
            run_completeness(connector_root, framework_root, build_root, verified_run_id, verified_commands_file)
            return int(artifacts["job"].get("return_code", 2))
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            rc = process.wait(timeout=30)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            rc = process.wait()
        artifacts = job_artifacts(root, args.connector)
        if artifacts["complete"]:
            print(
                "full-matrix-job: timeout wrapper ended after complete artifacts; using job artifacts as source of truth",
                flush=True,
            )
            run_completeness(connector_root, framework_root, build_root, verified_run_id, verified_commands_file)
            return int(artifacts["job"].get("return_code", 2))
        write_timeout_record(root, args.connector, args.crs, args.mrts, started_at, time.monotonic() - started)
        run_completeness(connector_root, framework_root, build_root, verified_run_id, verified_commands_file)
        return 77

    completeness_rc = run_completeness(connector_root, framework_root, build_root, verified_run_id, verified_commands_file)
    if completeness_rc != 0:
        return completeness_rc
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
