#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from runtime_path_utils import verified_runtime_paths


def read_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def run_completeness(connector_root: Path, framework_root: Path, build_root: Path, verified_run_id: str) -> int:
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
    commands_file = os.environ.get("VERIFIED_RUN_COMMANDS_FILE", "")
    if commands_file:
        cmd.extend(["--verified-commands-file", commands_file])
    return subprocess.run(cmd, cwd=str(connector_root)).returncode


def load_missing(connector_root: Path) -> list[dict]:
    path = connector_root / "reports/testing/generated/manifest/full-matrix-job-completeness.generated.json"
    data = read_json(path)
    jobs = data.get("jobs") if isinstance(data.get("jobs"), list) else []
    return [job for job in jobs if job.get("status") not in {"completed", "completed_with_mismatches"}]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector-root", default=".")
    parser.add_argument("--framework-root", default=None)
    parser.add_argument("--build-root", default=os.environ.get("BUILD_ROOT"))
    parser.add_argument("--job-timeout-seconds", type=int, default=int(os.environ.get("VERIFIED_RUN_FULL_MATRIX_JOB_TIMEOUT_SECONDS", "3600")))
    parser.add_argument("--total-timeout-seconds", type=int, default=int(os.environ.get("VERIFIED_RUN_FULL_MATRIX_TOTAL_TIMEOUT_SECONDS", "14400")))
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    connector_root = Path(args.connector_root).resolve()
    framework_root = Path(args.framework_root).resolve() if args.framework_root else connector_root / "modules/ModSecurity-test-Framework"
    default_paths = verified_runtime_paths(os.environ)
    build_root = Path(args.build_root or default_paths["BUILD_ROOT"]).resolve()
    current = build_root / "verified-runs/current-run-id"
    verified_run_id = os.environ.get("VERIFIED_RUN_ID") or (current.read_text(encoding="utf-8").strip() if current.is_file() else "")

    rc = run_completeness(connector_root, framework_root, build_root, verified_run_id)
    if rc != 0:
        return rc
    missing = load_missing(connector_root)
    if not missing:
        print("full-matrix-resume: all jobs complete")
        return 0

    started = time.monotonic()
    worst_rc = 0
    for job in missing:
        elapsed = time.monotonic() - started
        if elapsed >= args.total_timeout_seconds:
            print(f"full-matrix-resume: total timeout reached after {elapsed:.1f}s")
            return 77
        timeout = min(args.job_timeout_seconds, max(1, int(args.total_timeout_seconds - elapsed)))
        cmd = [
            sys.executable,
            str(connector_root / "ci/run-full-matrix-job.py"),
            "--connector",
            str(job["connector"]),
            "--crs",
            str(job["crs"]),
            "--mrts",
            str(job["mrts"]),
            "--connector-root",
            str(connector_root),
            "--framework-root",
            str(framework_root),
            "--build-root",
            str(build_root),
            "--timeout-seconds",
            str(timeout),
        ]
        if args.force:
            cmd.append("--force")
        print(f"full-matrix-resume: run {job['job_id']} timeout={timeout}s", flush=True)
        job_rc = subprocess.run(cmd, cwd=str(connector_root), env=dict(os.environ)).returncode
        if job_rc != 0:
            worst_rc = job_rc if worst_rc == 0 else worst_rc
    run_completeness(connector_root, framework_root, build_root, verified_run_id)
    remaining = load_missing(connector_root)
    if remaining:
        print("full-matrix-resume: incomplete jobs remain: " + ", ".join(str(job.get("job_id")) for job in remaining))
        return worst_rc or 77
    return worst_rc


if __name__ == "__main__":
    raise SystemExit(main())
