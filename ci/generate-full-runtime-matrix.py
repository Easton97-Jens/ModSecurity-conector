#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CONNECTORS = ("apache", "nginx", "haproxy")
TEST_VARIANTS = ("no-crs", "with-crs")
MRTS_VARIANTS = ("no-mrts", "with-mrts")
DEFAULT_STATE_HOME = Path(os.environ.get("XDG_STATE_HOME", str(Path.home() / ".local/state")))
DEFAULT_BUILD_ROOT = Path(os.environ.get("BUILD_ROOT", str(DEFAULT_STATE_HOME / "ModSecurity-conector-build"))).resolve()
MRTS_BUILD_ROOT = Path(os.environ.get("MRTS_BUILD_ROOT", str(DEFAULT_BUILD_ROOT / "mrts"))).resolve()
MRTS_UPSTREAM_CASE_MARKER = "/upstream-config-tests/framework-cases/"
MRTS_FEATURE_DEMO_CASE_MARKER = "/feature-demo/framework-cases/"


@dataclass
class RunRecord:
    connector: str
    test_variant: str
    mrts_variant: str
    return_code: int | None
    results_dir: Path
    summary_path: Path
    log_path: Path
    started_at: str = ""
    ended_at: str = ""
    duration_seconds: int | None = None
    attempted: int = 0
    passed: int = 0
    failed: int = 0
    blocked: int = 0
    not_executable: int = 0
    pending: int = 0
    outcome: str = "NOT_RUN"
    missing_summary: bool = False
    missing_summary_reason: str = ""
    cases: dict[str, dict[str, Any]] = field(default_factory=dict)
    mrts_upstream: Counter[str] = field(default_factory=Counter)
    feature_demo_cases: int = 0


def read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_manifest(path: Path, build_root: Path, log_root: Path) -> list[RunRecord]:
    records: list[RunRecord] = []
    by_key: set[tuple[str, str, str]] = set()
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            item = json.loads(line)
            record = RunRecord(
                connector=item["connector"],
                test_variant=item["test_variant"],
                mrts_variant=item["mrts_variant"],
                return_code=item.get("return_code", item.get("exit_code")),
                results_dir=Path(item["results_dir"]),
                summary_path=Path(item.get("summary_path") or item.get("runtime_summary_path")),
                log_path=Path(item["log_path"]),
                started_at=item.get("started_at", ""),
                ended_at=item.get("ended_at", ""),
                duration_seconds=item.get("duration_seconds"),
            )
            records.append(record)
            by_key.add((record.test_variant, record.mrts_variant, record.connector))

    for test_variant in TEST_VARIANTS:
        for mrts_variant in MRTS_VARIANTS:
            for connector in CONNECTORS:
                key = (test_variant, mrts_variant, connector)
                if key in by_key:
                    continue
                results_dir = build_root / "results" / "full-matrix" / test_variant / mrts_variant / connector
                records.append(
                    RunRecord(
                        connector=connector,
                        test_variant=test_variant,
                        mrts_variant=mrts_variant,
                        return_code=None,
                        results_dir=results_dir,
                        summary_path=results_dir / f"{connector}-summary.json",
                        log_path=log_root / "full-matrix" / test_variant / mrts_variant / f"{connector}.log",
                    )
                )
    return records


def case_status(case: dict[str, Any]) -> str:
    return str(case.get("status") or case.get("result") or "").lower()


def case_is_pending(case: dict[str, Any]) -> bool:
    values = [
        case.get("case_status"),
        case.get("yaml_status"),
        case.get("framework_status"),
        case.get("metadata", {}).get("status") if isinstance(case.get("metadata"), dict) else None,
    ]
    return any(str(value).lower() == "pending" for value in values if value is not None)


def case_is_mrts_upstream(case: dict[str, Any]) -> bool:
    path = str(case.get("path") or case.get("test_case") or "")
    metadata = case.get("metadata") if isinstance(case.get("metadata"), dict) else {}
    return (
        MRTS_UPSTREAM_CASE_MARKER in path
        or metadata.get("mrts_corpus") == "upstream-config-tests"
    )


def case_is_feature_demo(case: dict[str, Any]) -> bool:
    path = str(case.get("path") or case.get("test_case") or "")
    metadata = case.get("metadata") if isinstance(case.get("metadata"), dict) else {}
    return (
        MRTS_FEATURE_DEMO_CASE_MARKER in path
        or metadata.get("mrts_corpus") == "feature-demo"
    )


def parse_time(value: str) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def duration_seconds(started_at: str, ended_at: str) -> int | None:
    start = parse_time(started_at)
    end = parse_time(ended_at)
    if start is None or end is None:
        return None
    seconds = int((end - start).total_seconds())
    return seconds if seconds >= 0 else None


def summarize_cases(cases: dict[str, dict[str, Any]]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for case in cases.values():
        status = case_status(case)
        if status == "pass":
            counts["pass"] += 1
        elif status == "fail":
            counts["fail"] += 1
        elif status == "blocked":
            counts["blocked"] += 1
        elif status in {"not_executable", "not-executable"}:
            counts["not_executable"] += 1
        if case_is_pending(case):
            counts["pending"] += 1
    return counts


def populate_record(record: RunRecord) -> None:
    if record.duration_seconds is None:
        record.duration_seconds = duration_seconds(record.started_at, record.ended_at)
    if not record.summary_path.is_file():
        if record.return_code is not None or record.started_at:
            record.outcome = "BLOCKED"
            record.blocked = 1
            record.missing_summary = True
            record.missing_summary_reason = f"summary JSON missing: {record.summary_path}"
        return

    raw = read_json(record.summary_path)
    data = raw.get(record.connector, raw) if isinstance(raw, dict) else {}
    if not isinstance(data, dict):
        data = {}
    summary = data.get("summary") if isinstance(data.get("summary"), dict) else {}
    cases = data.get("cases") if isinstance(data.get("cases"), dict) else {}
    record.cases = {str(name): case for name, case in cases.items() if isinstance(case, dict)}
    derived = summarize_cases(record.cases)

    record.attempted = int(data.get("attempted") or data.get("total_cases") or len(record.cases) or 0)
    record.passed = int(summary.get("pass", derived["pass"]) or 0)
    record.failed = int(summary.get("fail", derived["fail"]) or 0)
    record.blocked = int(summary.get("blocked", derived["blocked"]) or 0)
    record.not_executable = int(summary.get("not_executable", derived["not_executable"]) or 0)
    record.pending = int(derived["pending"] or 0)

    for case in record.cases.values():
        if case_is_feature_demo(case):
            record.feature_demo_cases += 1
        if not case_is_mrts_upstream(case):
            continue
        status = case_status(case)
        if status == "pass":
            record.mrts_upstream["pass"] += 1
        elif status == "fail":
            record.mrts_upstream["fail"] += 1
        elif status == "blocked":
            record.mrts_upstream["blocked"] += 1
        elif status in {"not_executable", "not-executable"}:
            record.mrts_upstream["not_executable"] += 1
        if case_is_pending(case):
            record.mrts_upstream["pending"] += 1
        record.mrts_upstream["attempted"] += 1

    if record.blocked and record.attempted == 0:
        record.outcome = "BLOCKED"
    elif record.failed or (record.return_code not in (None, 0) and record.return_code != 77):
        record.outcome = "FAIL"
    elif record.return_code == 77:
        record.outcome = "BLOCKED"
    else:
        record.outcome = "PASS"


def record_to_json(record: RunRecord) -> dict[str, Any]:
    return {
        "connector": record.connector,
        "test_variant": record.test_variant,
        "mrts_variant": record.mrts_variant,
        "return_code": record.return_code,
        "outcome": record.outcome,
        "attempted": record.attempted,
        "pass": record.passed,
        "fail": record.failed,
        "blocked": record.blocked,
        "not_executable": record.not_executable,
        "pending": record.pending,
        "runtime_summary_path": str(record.summary_path),
        "log_path": str(record.log_path),
        "started_at": record.started_at,
        "ended_at": record.ended_at,
        "duration_seconds": record.duration_seconds,
        "missing_summary": record.missing_summary,
        "missing_summary_reason": record.missing_summary_reason,
        "mrts_upstream_config_tests": dict(record.mrts_upstream),
        "feature_demo_runtime_cases": record.feature_demo_cases,
    }


def markdown(records: list[RunRecord], totals: Counter[str], generated_at: str) -> str:
    lines: list[str] = []
    lines.append("# Full MRTS Runtime Matrix")
    lines.append("")
    lines.append("Generated file - do not edit manually.")
    lines.append("")
    lines.append(f"- Generated at: `{generated_at}`")
    lines.append(f"- Variant runs: **{len(records)}**")
    lines.append(f"- Total attempted: **{totals['attempted']}**")
    lines.append(f"- Total PASS/FAIL/BLOCKED/NOT_EXECUTABLE: **{totals['pass']}** / **{totals['fail']}** / **{totals['blocked']}** / **{totals['not_executable']}**")
    lines.append(f"- Pending metadata rows observed in runtime summaries: **{totals['pending']}**")
    lines.append("")
    lines.append("## Variant Results")
    lines.append("| Connector | Test variant | MRTS variant | Outcome | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Pending | Duration seconds | Summary | Log |")
    lines.append("|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|")
    for record in records:
        lines.append(
            "| {connector} | {test_variant} | {mrts_variant} | {outcome} | {attempted} | {passed} | {failed} | {blocked} | {not_executable} | {pending} | {duration} | {summary} | {log} |".format(
                connector=record.connector,
                test_variant=record.test_variant,
                mrts_variant=record.mrts_variant,
                outcome=record.outcome,
                attempted=record.attempted,
                passed=record.passed,
                failed=record.failed,
                blocked=record.blocked,
                not_executable=record.not_executable,
                pending=record.pending,
                duration=record.duration_seconds if record.duration_seconds is not None else "-",
                summary=record.summary_path,
                log=record.log_path,
            )
        )
    lines.append("")
    lines.append("## MRTS Upstream Config Tests")
    lines.append("| Connector | Variant | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Pending |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|")
    for record in records:
        if record.mrts_variant != "with-mrts":
            continue
        counts = record.mrts_upstream
        lines.append(
            f"| {record.connector} | {record.test_variant}/{record.mrts_variant} | {counts['attempted']} | {counts['pass']} | {counts['fail']} | {counts['blocked']} | {counts['not_executable']} | {counts['pending']} |"
        )
    lines.append("")
    lines.append("## Guardrails")
    lines.append("- `feature-demo` is visible in reports but not runtime-executed unless `MODSECURITY_MRTS_INCLUDE_FEATURE_DEMO=1` is set.")
    lines.append("- MRTS golden outputs under the submodule are golden/reference/drift input only and are not runtime case roots.")
    lines.append("- `no-mrts` variants should have zero MRTS runtime cases.")
    lines.append("- Runtime PASS/FAIL/BLOCKED values come from connector summary JSON, not classification overlays.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector-root", default=".")
    parser.add_argument("--framework-root", default=None)
    parser.add_argument("--build-root", default=os.environ.get("BUILD_ROOT", str(DEFAULT_BUILD_ROOT)))
    parser.add_argument("--log-root", default=os.environ.get("LOG_ROOT"))
    parser.add_argument("--manifest", default=None)
    parser.add_argument("--output-dir", default=None)
    args = parser.parse_args()

    connector_root = Path(args.connector_root).resolve()
    build_root = Path(args.build_root).resolve()
    log_root = Path(args.log_root).resolve() if args.log_root else build_root / "logs"
    output_dir = Path(args.output_dir).resolve() if args.output_dir else connector_root / "reports/testing/generated"
    manifest = Path(args.manifest).resolve() if args.manifest else build_root / "results/full-matrix/full-runtime-matrix-runs.jsonl"

    records = load_manifest(manifest, build_root, log_root)
    records.sort(key=lambda item: (TEST_VARIANTS.index(item.test_variant), MRTS_VARIANTS.index(item.mrts_variant), CONNECTORS.index(item.connector)))
    for record in records:
        populate_record(record)

    totals: Counter[str] = Counter()
    for record in records:
        totals["attempted"] += record.attempted
        totals["pass"] += record.passed
        totals["fail"] += record.failed
        totals["blocked"] += record.blocked
        totals["not_executable"] += record.not_executable
        totals["pending"] += record.pending

    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    payload = {
        "generated_at": generated_at,
        "manifest": str(manifest),
        "build_root": str(build_root),
        "log_root": str(log_root),
        "totals": dict(totals),
        "runs": [record_to_json(record) for record in records],
        "guardrails": {
            "feature_demo_runtime_cases": sum(record.feature_demo_cases for record in records),
            "no_mrts_mrts_runtime_cases": sum(record.mrts_upstream["attempted"] for record in records if record.mrts_variant == "no-mrts"),
        },
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "full-runtime-matrix.generated.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (output_dir / "full-runtime-matrix.generated.md").write_text(markdown(records, totals, generated_at), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
