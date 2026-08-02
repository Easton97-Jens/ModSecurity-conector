#!/usr/bin/env python3
"""Produce a bounded, raw-payload-free aggregate from NGINX Memcheck logs.

The NGINX harness owns the diagnostic lifecycle.  This helper deliberately
does not interpret request/response data or print Valgrind excerpts: it only
aggregates terminal counters and whether the expected normal master/worker
evidence was retained beneath the already-validated harness evidence directory.
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
MAX_METADATA_BYTES = 64 * 1024
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


class UnsafeEvidenceError(ValueError):
    """An evidence input cannot safely contribute to a clean aggregate."""

    def __init__(self, reason: str, message: str) -> None:
        super().__init__(message)
        self.reason = reason


def parse_count(value: str) -> int:
    return int(value.replace(",", ""))


def absolute_path(path: Path) -> Path:
    """Normalize lexical paths without resolving an attacker-controlled symlink."""

    return Path(os.path.abspath(os.fspath(path)))


def same_file(first: os.stat_result, second: os.stat_result) -> bool:
    return first.st_dev == second.st_dev and first.st_ino == second.st_ino


def file_signature(file_stat: os.stat_result) -> tuple[int, int, int, int, int, int, int, int]:
    """Capture properties that must not change between validation and reading."""

    return (
        file_stat.st_dev,
        file_stat.st_ino,
        file_stat.st_mode,
        file_stat.st_uid,
        file_stat.st_nlink,
        file_stat.st_size,
        file_stat.st_mtime_ns,
        file_stat.st_ctime_ns,
    )


def validate_private_directory(path: Path, label: str) -> Path:
    """Validate a non-symlink directory before trusting evidence beneath it."""

    candidate = absolute_path(path)
    try:
        before = candidate.lstat()
    except FileNotFoundError as exc:
        raise ValueError(f"{label} is missing") from exc
    if stat.S_ISLNK(before.st_mode):
        raise ValueError(f"{label} must not be a symlink")
    if not stat.S_ISDIR(before.st_mode):
        raise ValueError(f"{label} is not a real directory")
    if before.st_uid != os.geteuid():
        raise ValueError(f"{label} is not owned by the effective uid")
    if before.st_mode & 0o022:
        raise ValueError(f"{label} is group or other writable")

    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(candidate, flags)
    except OSError as exc:
        raise ValueError(f"{label} cannot be opened safely") from exc
    try:
        opened = os.fstat(descriptor)
    finally:
        os.close(descriptor)

    if not same_file(before, opened):
        raise ValueError(f"{label} changed while being opened")
    if not stat.S_ISDIR(opened.st_mode):
        raise ValueError(f"{label} is not a real directory")
    if opened.st_uid != os.geteuid():
        raise ValueError(f"{label} is not owned by the effective uid")
    if opened.st_mode & 0o022:
        raise ValueError(f"{label} is group or other writable")
    return candidate


def validate_evidence_root(log_dir: Path) -> Path:
    """Trust only an effective-UID-owned root below a non-writable real directory."""

    root = absolute_path(log_dir)
    validate_private_directory(root.parent, "log directory parent")
    return validate_private_directory(root, "log directory")


def require_direct_child(log_dir: Path, path: Path, label: str) -> Path:
    """Reject outputs or metadata outside the harness-owned evidence root."""

    root = absolute_path(log_dir)
    candidate = absolute_path(path)
    if candidate.parent != root:
        raise ValueError(f"{label} must be a direct child of the log directory")
    return candidate


def validate_private_regular_file(
    file_stat: os.stat_result, label: str, reason_prefix: str
) -> None:
    """Apply the ownership, link, and access invariant to one evidence file."""

    if stat.S_ISLNK(file_stat.st_mode):
        raise UnsafeEvidenceError(
            f"{reason_prefix}_symlink", f"{label} must not be a symlink"
        )
    if not stat.S_ISREG(file_stat.st_mode):
        raise UnsafeEvidenceError(
            f"{reason_prefix}_invalid", f"{label} is not a regular file"
        )
    if file_stat.st_nlink != 1:
        raise UnsafeEvidenceError(
            f"{reason_prefix}_hardlink", f"{label} must have exactly one link"
        )
    if file_stat.st_uid != os.geteuid():
        raise UnsafeEvidenceError(
            f"{reason_prefix}_owner_unsafe",
            f"{label} is not owned by the effective uid",
        )
    if file_stat.st_mode & 0o077:
        raise UnsafeEvidenceError(
            f"{reason_prefix}_permissions_unsafe",
            f"{label} is group or other accessible",
        )


def open_private_input(
    log_dir: Path,
    path: Path,
    label: str,
    reason_prefix: str,
    maximum_bytes: int,
    *,
    tail: bool,
) -> tuple[bytes, bool]:
    """Open one direct child without following a late symlink substitution."""

    candidate = require_direct_child(log_dir, path, label)
    try:
        before = candidate.lstat()
    except FileNotFoundError:
        raise
    except OSError as exc:
        raise UnsafeEvidenceError(
            f"{reason_prefix}_unsafe", f"{label} cannot be inspected safely"
        ) from exc
    validate_private_regular_file(before, label, reason_prefix)

    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(candidate, flags)
    except FileNotFoundError:
        raise
    except OSError as exc:
        raise UnsafeEvidenceError(
            f"{reason_prefix}_unsafe", f"{label} cannot be opened safely"
        ) from exc

    try:
        opened = os.fstat(descriptor)
        validate_private_regular_file(opened, label, reason_prefix)
        if file_signature(before) != file_signature(opened):
            raise UnsafeEvidenceError(
                f"{reason_prefix}_changed", f"{label} changed while being opened"
            )
        truncated = opened.st_size > maximum_bytes
        with os.fdopen(descriptor, "rb", closefd=False) as handle:
            if tail and truncated:
                handle.seek(-maximum_bytes, os.SEEK_END)
            data = handle.read(maximum_bytes)
        after = os.fstat(descriptor)
    except UnsafeEvidenceError:
        raise
    except OSError as exc:
        raise UnsafeEvidenceError(
            f"{reason_prefix}_unsafe", f"{label} could not be read safely"
        ) from exc
    finally:
        os.close(descriptor)

    if file_signature(opened) != file_signature(after):
        raise UnsafeEvidenceError(
            f"{reason_prefix}_changed", f"{label} changed while being read"
        )
    return data, truncated


def read_tail(log_dir: Path, path: Path) -> tuple[str, bool]:
    """Read a bounded tail that contains Valgrind's terminal summary."""

    data, truncated = open_private_input(
        log_dir,
        path,
        "Valgrind log",
        "valgrind_log",
        MAX_LOG_BYTES,
        tail=True,
    )
    return data.decode("utf-8", errors="replace"), truncated


def read_metadata(log_dir: Path, path: Path, label: str, reason_prefix: str) -> tuple[str, bool]:
    data, truncated = open_private_input(
        log_dir, path, label, reason_prefix, MAX_METADATA_BYTES, tail=False
    )
    return data.decode("utf-8", errors="replace"), truncated


def parse_roles(log_dir: Path, path: Path | None) -> tuple[set[str], set[str], list[str]]:
    if path is None:
        return set(), set(), ["roles_file_missing"]
    try:
        raw_text, truncated = read_metadata(log_dir, path, "roles file", "roles_file")
    except FileNotFoundError:
        return set(), set(), ["roles_file_missing"]
    except UnsafeEvidenceError as exc:
        return set(), set(), [exc.reason]
    except (OSError, ValueError):
        return set(), set(), ["roles_file_invalid"]
    if truncated:
        return set(), set(), ["roles_file_too_large"]

    masters: set[str] = set()
    workers: set[str] = set()
    reasons: list[str] = []
    raw_lines = raw_text.splitlines()
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


def parse_lifecycle(log_dir: Path, path: Path | None) -> tuple[dict[str, str], list[str]]:
    if path is None:
        return {}, ["lifecycle_file_missing"]
    try:
        raw_text, truncated = read_metadata(
            log_dir, path, "lifecycle file", "lifecycle_file"
        )
    except FileNotFoundError:
        return {}, ["lifecycle_file_missing"]
    except UnsafeEvidenceError as exc:
        return {}, [exc.reason]
    except (OSError, ValueError):
        return {}, ["lifecycle_file_invalid"]
    if truncated:
        return {}, ["lifecycle_file_too_large"]

    values: dict[str, str] = {}
    reasons: list[str] = []
    raw_lines = raw_text.splitlines()
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


def write_text(handle, summary: dict[str, object]) -> None:
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
    handle.write("\n".join(lines) + "\n")


def write_json(handle, summary: dict[str, object]) -> None:
    json.dump(summary, handle, indent=2, sort_keys=True)
    handle.write("\n")


def validate_output_target(log_dir: Path, path: Path, label: str) -> Path:
    """Existing output targets are evidence files too; absent targets are created safely."""

    candidate = require_direct_child(log_dir, path, label)
    try:
        file_stat = candidate.lstat()
    except FileNotFoundError:
        return candidate
    except OSError as exc:
        raise ValueError(f"{label} cannot be inspected safely") from exc
    try:
        validate_private_regular_file(file_stat, label, "output")
    except UnsafeEvidenceError as exc:
        raise ValueError(f"{label} is unsafe: {exc}") from exc
    return candidate


def atomic_write(log_dir: Path, path: Path, label: str, writer, summary: dict[str, object]) -> None:
    """Create a private direct-child output without following an existing symlink."""

    output = validate_output_target(log_dir, path, label)
    descriptor, temporary_name = tempfile.mkstemp(dir=log_dir, prefix=f".{output.name}.")
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            descriptor = -1
            writer(handle, summary)
        os.replace(temporary, output)
        validate_output_target(log_dir, output, label)
    finally:
        if descriptor != -1:
            os.close(descriptor)
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def require_distinct_paths(paths: Iterable[tuple[str, Path]]) -> None:
    """Prevent an output path from replacing metadata or another requested output."""

    seen: dict[Path, str] = {}
    for label, path in paths:
        if path in seen:
            raise ValueError(f"{label} must not alias {seen[path]}")
        seen[path] = label


def summarize(log_dir: Path, roles_file: Path | None, lifecycle_file: Path | None) -> dict[str, object]:
    log_dir = validate_evidence_root(log_dir)
    log_files: dict[str, Path] = {}
    reasons: list[str] = []
    try:
        candidates = tuple(log_dir.iterdir())
    except OSError as exc:
        raise ValueError("log directory cannot be listed safely") from exc
    for candidate in candidates:
        match = LOG_NAME_RE.fullmatch(candidate.name)
        if match is None:
            continue
        log_files[match.group("pid")] = candidate

    masters, workers, role_reasons = parse_roles(log_dir, roles_file)
    lifecycle, lifecycle_reasons = parse_lifecycle(log_dir, lifecycle_file)
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
            text, truncated = read_tail(log_dir, log_path)
        except FileNotFoundError:
            reasons.append("valgrind_log_missing")
            continue
        except UnsafeEvidenceError as exc:
            reasons.append(exc.reason)
            continue
        except (OSError, ValueError):
            reasons.append("valgrind_log_invalid")
            continue
        if truncated:
            truncated_log_inputs += 1
        private_log_inputs += 1
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
        log_dir = validate_evidence_root(args.log_dir)
        roles_file = require_direct_child(log_dir, args.roles_file, "roles file")
        lifecycle_file = require_direct_child(log_dir, args.lifecycle_file, "lifecycle file")
        output = require_direct_child(log_dir, args.output, "JSON output")
        text_output = require_direct_child(log_dir, args.text_output, "text output")
        require_distinct_paths(
            (
                ("roles file", roles_file),
                ("lifecycle file", lifecycle_file),
                ("JSON output", output),
                ("text output", text_output),
            )
        )
        validate_output_target(log_dir, output, "JSON output")
        validate_output_target(log_dir, text_output, "text output")
        summary = summarize(log_dir, roles_file, lifecycle_file)
        atomic_write(log_dir, output, "JSON output", write_json, summary)
        atomic_write(log_dir, text_output, "text output", write_text, summary)
    except (OSError, ValueError) as exc:
        print(f"nginx memcheck summary rejected input: {exc}", file=sys.stderr)
        return 2

    return 0 if summary["status"] == "clean" else 99


if __name__ == "__main__":
    raise SystemExit(main())
