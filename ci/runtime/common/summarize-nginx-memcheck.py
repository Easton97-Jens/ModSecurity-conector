#!/usr/bin/env python3
"""Produce a bounded, raw-payload-free aggregate from NGINX Memcheck logs.

The NGINX harness owns the diagnostic lifecycle.  This helper deliberately
does not interpret request/response data or print Valgrind excerpts: it only
aggregates terminal counters and whether the expected normal master/worker
evidence was retained beneath the already-validated harness log directory.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
import tempfile
from pathlib import Path
from typing import Iterable


MAX_LOG_BYTES = 4 * 1024 * 1024
LOG_NAME_RE = re.compile(r"valgrind\.(?P<pid>[0-9]+)\.log\Z")
ERROR_SUMMARY_RE = re.compile(r"ERROR SUMMARY:\s*(?P<count>[0-9,]+)\s+errors", re.IGNORECASE)
LEAK_RE = {
    "definitely_lost_bytes": re.compile(
        r"definitely lost:\s*(?P<count>[0-9,]+)\s+bytes", re.IGNORECASE
    ),
    "indirectly_lost_bytes": re.compile(
        r"indirectly lost:\s*(?P<count>[0-9,]+)\s+bytes", re.IGNORECASE
    ),
    "possibly_lost_bytes": re.compile(
        r"possibly lost:\s*(?P<count>[0-9,]+)\s+bytes", re.IGNORECASE
    ),
    "still_reachable_bytes": re.compile(
        r"still reachable:\s*(?P<count>[0-9,]+)\s+bytes", re.IGNORECASE
    ),
}


def parse_count(value: str) -> int:
    return int(value.replace(",", ""))


def require_direct_child(log_dir: Path, path: Path, label: str) -> None:
    """Reject outputs or metadata outside the harness-owned log directory."""

    root = log_dir.resolve(strict=True)
    parent = path.parent.resolve(strict=True)
    if parent != root:
        raise ValueError(f"{label} must be a direct child of the log directory")


def read_tail(path: Path) -> tuple[str, bool, bool]:
    """Read a bounded tail that contains Valgrind's terminal summary."""

    file_stat = path.lstat()
    if not stat.S_ISREG(file_stat.st_mode):
        raise ValueError("log is not a regular file")
    truncated = file_stat.st_size > MAX_LOG_BYTES
    with path.open("rb") as handle:
        if truncated:
            handle.seek(-MAX_LOG_BYTES, os.SEEK_END)
        data = handle.read(MAX_LOG_BYTES)
    private = not bool(file_stat.st_mode & 0o077)
    return data.decode("utf-8", errors="replace"), truncated, private


def parse_roles(path: Path | None) -> tuple[set[str], set[str], list[str]]:
    if path is None:
        return set(), set(), ["roles_file_missing"]
    if path.is_symlink() or not path.is_file():
        return set(), set(), ["roles_file_invalid"]

    masters: set[str] = set()
    workers: set[str] = set()
    reasons: list[str] = []
    raw_lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    if len(raw_lines) > 128:
        return set(), set(), ["roles_file_too_large"]
    for raw_line in raw_lines:
        if not raw_line:
            continue
        key, separator, value = raw_line.partition("=")
        if not separator or not value.isdecimal():
            reasons.append("roles_file_invalid")
            continue
        if key == "master_pid":
            masters.add(value)
        elif key == "worker_pid":
            workers.add(value)
        else:
            reasons.append("roles_file_invalid")
    if len(masters) != 1:
        reasons.append("master_snapshot_missing")
    if not workers:
        reasons.append("worker_snapshot_missing")
    return masters, workers, reasons


def parse_lifecycle(path: Path | None) -> tuple[dict[str, str], list[str]]:
    if path is None:
        return {}, ["lifecycle_file_missing"]
    if path.is_symlink() or not path.is_file():
        return {}, ["lifecycle_file_invalid"]

    values: dict[str, str] = {}
    reasons: list[str] = []
    raw_lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    if len(raw_lines) > 64:
        return {}, ["lifecycle_file_too_large"]
    for raw_line in raw_lines:
        key, separator, value = raw_line.partition("=")
        if not separator or key not in {"shutdown", "wait", "wrapper_exit_code", "containment"}:
            reasons.append("lifecycle_file_invalid")
            continue
        if key in values:
            reasons.append("lifecycle_file_invalid")
            continue
        values[key] = value
    if values.get("shutdown") not in {"graceful", "forced", "forced_term", "forced_kill"}:
        reasons.append("shutdown_status_missing")
    if values.get("wait") not in {"exited", "timed_out"}:
        reasons.append("wait_status_missing")
    if not values.get("wrapper_exit_code", "").isdecimal():
        reasons.append("wrapper_exit_status_missing")
    if values.get("containment") not in {"isolated", "unverified"}:
        reasons.append("containment_status_missing")
    return values, reasons


def unique_reasons(reasons: Iterable[str]) -> list[str]:
    return sorted(set(reasons))


def status_for(*, errors_detected: bool, incomplete: bool) -> str:
    if errors_detected and incomplete:
        return "error_incomplete"
    if errors_detected:
        return "error"
    if incomplete:
        return "incomplete"
    return "clean"


def write_text(path: Path, summary: dict[str, object]) -> None:
    lines = [
        f"status={summary['status']}",
        f"complete={int(bool(summary['complete']))}",
        f"errors_detected={int(bool(summary['errors_detected']))}",
        f"logs_seen={summary['logs_seen']}",
        f"logs_with_final_summary={summary['logs_with_final_summary']}",
        f"error_count={summary['error_count']}",
        f"definitely_lost_bytes={summary['definitely_lost_bytes']}",
        f"indirectly_lost_bytes={summary['indirectly_lost_bytes']}",
        f"possibly_lost_bytes={summary['possibly_lost_bytes']}",
        f"still_reachable_bytes={summary['still_reachable_bytes']}",
        f"truncated_log_inputs={summary['truncated_log_inputs']}",
        f"private_log_inputs={summary['private_log_inputs']}",
        f"incomplete_reasons={','.join(summary['incomplete_reasons'])}",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_json(path: Path, summary: dict[str, object]) -> None:
    path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def atomic_write(path: Path, writer, summary: dict[str, object]) -> None:
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
    ) as handle:
        temporary = Path(handle.name)
    try:
        writer(temporary, summary)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def summarize(log_dir: Path, roles_file: Path | None, lifecycle_file: Path | None) -> dict[str, object]:
    log_files: dict[str, Path] = {}
    reasons: list[str] = []
    for candidate in log_dir.iterdir():
        match = LOG_NAME_RE.fullmatch(candidate.name)
        if match is None:
            continue
        if candidate.is_symlink() or not candidate.is_file():
            reasons.append("valgrind_log_invalid")
            continue
        log_files[match.group("pid")] = candidate

    masters, workers, role_reasons = parse_roles(roles_file)
    lifecycle, lifecycle_reasons = parse_lifecycle(lifecycle_file)
    reasons.extend(role_reasons)
    reasons.extend(lifecycle_reasons)

    if not log_files:
        reasons.append("valgrind_logs_missing")
    for master_pid in masters:
        if master_pid not in log_files:
            reasons.append("master_log_missing")
    for worker_pid in workers:
        if worker_pid not in log_files:
            reasons.append("worker_log_missing")

    error_count = 0
    leak_counts = {name: 0 for name in LEAK_RE}
    final_summary_count = 0
    truncated_log_inputs = 0
    private_log_inputs = 0
    for log_path in log_files.values():
        try:
            text, truncated, private = read_tail(log_path)
        except ValueError:
            reasons.append("valgrind_log_invalid")
            continue
        if truncated:
            truncated_log_inputs += 1
        if private:
            private_log_inputs += 1
        else:
            reasons.append("valgrind_log_permissions_unsafe")
        matches = ERROR_SUMMARY_RE.findall(text)
        if not matches:
            reasons.append("valgrind_final_summary_missing")
        else:
            final_summary_count += 1
            error_count += parse_count(matches[-1])
        for name, pattern in LEAK_RE.items():
            matches = pattern.findall(text)
            if matches:
                leak_counts[name] += parse_count(matches[-1])

    if lifecycle.get("shutdown") != "graceful" or lifecycle.get("wait") == "timed_out":
        reasons.append("graceful_shutdown_incomplete")
    if lifecycle.get("containment") != "isolated":
        reasons.append("process_group_unverified")
    wrapper_exit_code = lifecycle.get("wrapper_exit_code")
    if wrapper_exit_code and wrapper_exit_code != "0":
        if wrapper_exit_code == "99":
            error_count += 1
        else:
            reasons.append("wrapper_exit_nonzero")

    errors_detected = bool(
        error_count
        or leak_counts["definitely_lost_bytes"]
        or leak_counts["indirectly_lost_bytes"]
    )
    incomplete_reasons = unique_reasons(reasons)
    incomplete = bool(incomplete_reasons)
    return {
        "status": status_for(errors_detected=errors_detected, incomplete=incomplete),
        "complete": not incomplete,
        "errors_detected": errors_detected,
        "logs_seen": len(log_files),
        "logs_with_final_summary": final_summary_count,
        "error_count": error_count,
        "definitely_lost_bytes": leak_counts["definitely_lost_bytes"],
        "indirectly_lost_bytes": leak_counts["indirectly_lost_bytes"],
        "possibly_lost_bytes": leak_counts["possibly_lost_bytes"],
        "still_reachable_bytes": leak_counts["still_reachable_bytes"],
        "truncated_log_inputs": truncated_log_inputs,
        "private_log_inputs": private_log_inputs,
        "incomplete_reasons": incomplete_reasons,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log-dir", required=True, type=Path)
    parser.add_argument("--roles-file", required=True, type=Path)
    parser.add_argument("--lifecycle-file", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--text-output", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.log_dir.is_symlink() or not args.log_dir.is_dir():
            raise ValueError("log directory is not a real directory")
        require_direct_child(args.log_dir, args.roles_file, "roles file")
        require_direct_child(args.log_dir, args.lifecycle_file, "lifecycle file")
        require_direct_child(args.log_dir, args.output, "JSON output")
        require_direct_child(args.log_dir, args.text_output, "text output")
        summary = summarize(args.log_dir, args.roles_file, args.lifecycle_file)
        atomic_write(args.output, write_json, summary)
        atomic_write(args.text_output, write_text, summary)
    except (OSError, ValueError) as exc:
        print(f"nginx memcheck summary rejected input: {exc}", file=sys.stderr)
        return 2

    return 0 if summary["status"] == "clean" else 99


if __name__ == "__main__":
    raise SystemExit(main())
