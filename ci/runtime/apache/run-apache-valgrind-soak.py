#!/usr/bin/env python3
"""Run the Parent-built Apache module under a bounded Valgrind soak."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import threading
import time


EXIT_BLOCKED = 77


def version(command: list[str]) -> str:
    try:
        return subprocess.run(command, text=True, capture_output=True, timeout=10).stdout.splitlines()[0]
    except (OSError, subprocess.SubprocessError, IndexError):
        return "unavailable"


def summary(log: str) -> dict[str, int]:
    patterns = {
        "definitely_lost": r"definitely lost: ([0-9,]+)",
        "indirectly_lost": r"indirectly lost: ([0-9,]+)",
        "possibly_lost": r"possibly lost: ([0-9,]+)",
        "still_reachable": r"still reachable: ([0-9,]+)",
        "error_count": r"ERROR SUMMARY: ([0-9,]+)",
    }
    values: dict[str, int] = {}
    for key, pattern in patterns.items():
        matches = re.findall(pattern, log)
        values[key] = max((int(value.replace(",", "")) for value in matches), default=0)
    lowered = log.lower()
    values["invalid_access"] = len(re.findall(r"invalid (?:read|write)", lowered))
    values["use_after_free"] = lowered.count("use-after-free")
    values["double_free"] = len(re.findall(r"invalid free|double.free", lowered))
    return values


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("memcheck", "helgrind"), required=True)
    parser.add_argument("--duration", type=int, default=20)
    parser.add_argument("--parallelism", type=int, default=2)
    parser.add_argument("--restart-interval", type=int, default=5)
    parser.add_argument("--httpd", default=os.environ.get("APACHE_HTTPD"))
    parser.add_argument("--config", default=os.environ.get("APACHE_CONFIG"))
    parser.add_argument("--base-url", default=os.environ.get("APACHE_TEST_BASE_URL"))
    parser.add_argument("--evidence-root", default=os.environ.get("APACHE_SOAK_EVIDENCE_ROOT"))
    args = parser.parse_args()
    if not args.httpd or not args.config or not args.base_url:
        print("BLOCKED: APACHE_HTTPD, APACHE_CONFIG and APACHE_TEST_BASE_URL are required", file=sys.stderr)
        return EXIT_BLOCKED
    if not 1 <= args.duration <= 3600 or not 1 <= args.parallelism <= 16:
        parser.error("duration must be 1..3600 and parallelism 1..16")
    if not shutil_which("valgrind") or not Path(args.httpd).is_file() or not Path(args.config).is_file():
        print("BLOCKED: Valgrind, httpd, or rendered Parent config is unavailable", file=sys.stderr)
        return EXIT_BLOCKED

    root = Path(args.evidence_root or Path.home() / ".local/state/ModSecurity-conector-build/evidence/apache-soak")
    root.mkdir(parents=True, exist_ok=True)
    if root.resolve().is_relative_to(Path.cwd().resolve()):
        print("FAIL: evidence root must be outside the Git worktree", file=sys.stderr)
        return 1
    log_path, json_path, md_path = root / f"{args.mode}.log", root / f"{args.mode}.json", root / f"{args.mode}.md"
    tool = ["valgrind", f"--tool={args.mode}", "--error-exitcode=99", f"--log-file={log_path}"]
    if args.mode == "memcheck":
        tool += ["--leak-check=full", "--show-leak-kinds=all", "--errors-for-leak-kinds=definite,indirect"]
    process = subprocess.Popen(tool + [args.httpd, "-DFOREGROUND", "-f", args.config], start_new_session=True)
    stop = threading.Event()
    counts = {"requests": 0, "request_failures": 0, "restarts": 0}
    lock = threading.Lock()

    def traffic() -> None:
        command = [sys.executable, str(Path(__file__).parents[3] / "connectors/apache/harness/request_body_regressions.py"),
                   "--base-url", args.base_url, "--repetitions", "1"]
        while not stop.is_set():
            rc = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=20).returncode
            with lock:
                counts["requests"] += 6
                counts["request_failures"] += rc != 0

    workers = [threading.Thread(target=traffic, daemon=True) for _ in range(args.parallelism)]
    try:
        time.sleep(1)
        for worker in workers:
            worker.start()
        deadline, next_restart = time.monotonic() + args.duration, time.monotonic() + args.restart_interval
        while time.monotonic() < deadline and process.poll() is None:
            if time.monotonic() >= next_restart:
                process.send_signal(signal.SIGUSR1)
                counts["restarts"] += 1
                next_restart += args.restart_interval
            time.sleep(0.2)
    finally:
        stop.set()
        for worker in workers:
            worker.join(timeout=25)
        if process.poll() is None:
            process.terminate()
        try:
            process.wait(timeout=20)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=5)

    log = log_path.read_text(encoding="utf-8", errors="replace") if log_path.exists() else ""
    leaks = summary(log)
    fatal = process.returncode not in (0, -signal.SIGTERM) or counts["request_failures"] > 0
    if args.mode == "memcheck":
        fatal |= any(leaks[key] for key in ("definitely_lost", "indirectly_lost", "invalid_access", "use_after_free", "double_free"))
    else:
        fatal |= leaks["error_count"] > 0
    report = {"status": "FAIL" if fatal else "PASS", "mode": args.mode, "duration_seconds": args.duration,
              **counts, "exit_code": process.returncode, "parent_commit": version(["git", "rev-parse", "HEAD"]),
              "apache_version": version([args.httpd, "-v"]), "libmodsecurity_version": os.environ.get("LIBMODSECURITY_VERSION", "unavailable"),
              "compiler": version([os.environ.get("CC", "cc"), "--version"]), "valgrind_version": version(["valgrind", "--version"]),
              "mpm": version([args.httpd, "-V"]), "leaks": leaks,
              "still_reachable_is_not_leak_free": True}
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text("# Apache Valgrind soak\n\n" + "\n".join(f"- **{key}:** `{value}`" for key, value in report.items()) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if fatal else 0


def shutil_which(program: str) -> str | None:
    for directory in os.environ.get("PATH", "").split(os.pathsep):
        candidate = Path(directory) / program
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate)
    return None


if __name__ == "__main__":
    raise SystemExit(main())
