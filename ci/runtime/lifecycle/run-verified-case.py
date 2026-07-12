#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CONNECTORS = {"apache", "nginx", "haproxy"}
LOG_EXTENSIONS = {".err", ".json", ".jsonl", ".log", ".txt"}
LOG_NAME_FRAGMENTS = (
    "access",
    "audit",
    "case-assert",
    "configtest",
    "curl",
    "decision",
    "error",
    "haproxy",
    "nginx",
    "observed",
    "phase4",
    "result",
    "spoa",
    "stderr",
    "stdout",
    "status",
)
EXCERPT_PATTERNS = re.compile(
    r"(ModSecurity|Access denied|Matched Data|\[id \"|\[msg \"|"
    r"intervention|decision|rule|rule_id|audit|error|fail|denied|status)",
    re.IGNORECASE,
)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_utc(value: datetime) -> str:
    return value.isoformat(timespec="seconds").replace("+00:00", "Z")


def safe_name(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9_.-]+", "-", value.strip())
    return value.strip("-") or "unknown"


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def try_load_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml  # type: ignore
    except Exception:
        return {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def find_case_path(framework_root: Path, case: str) -> Path | None:
    cases_root = framework_root / "tests/cases"
    if not cases_root.is_dir():
        return None
    matches = sorted(cases_root.rglob(f"{case}.yaml"))
    return matches[0] if matches else None


def find_first_key(value: Any, names: set[str]) -> Any:
    if isinstance(value, dict):
        for key, item in value.items():
            if str(key) in names:
                return item
        for item in value.values():
            found = find_first_key(item, names)
            if found is not None:
                return found
    elif isinstance(value, list):
        for item in value:
            found = find_first_key(item, names)
            if found is not None:
                return found
    return None


def summarize_case_definition(case_path: Path | None) -> dict[str, Any]:
    if not case_path or not case_path.is_file():
        return {
            "path": str(case_path) if case_path else "-",
            "status": "missing",
            "request": {},
            "rule_ids": [],
            "transforms": [],
        }

    data = try_load_yaml(case_path)
    rules_text = str(data.get("rules") or "")
    request = data.get("request") if isinstance(data.get("request"), dict) else {}
    if not request:
        request = find_first_key(data, {"request"}) if isinstance(find_first_key(data, {"request"}), dict) else {}
    headers = request.get("headers") if isinstance(request, dict) else None
    request_summary = {
        "method": request.get("method", "-") if isinstance(request, dict) else "-",
        "path": request.get("path") or request.get("uri") or request.get("url") or "-",
        "headers": headers if isinstance(headers, dict) else {},
        "body": request.get("body", "") if isinstance(request, dict) else "",
    }
    transforms = sorted(set(re.findall(r"\bt:([A-Za-z0-9_]+)", rules_text)))
    rule_ids = sorted(set(re.findall(r"\bid:(\d+)", rules_text)), key=lambda item: int(item))
    return {
        "path": str(case_path),
        "status": "present",
        "request": request_summary,
        "rule_ids": rule_ids,
        "transforms": transforms,
        "expect": data.get("expect") if isinstance(data.get("expect"), dict) else {},
        "category": data.get("category"),
        "capabilities": data.get("capabilities"),
    }


def harness_paths(connector: str, build_root: Path, crs: str, mrts: str) -> dict[str, Path]:
    base = build_root / f"verified-{connector}-case"
    variant_work = base / f"{crs}-{mrts}-{connector}"
    if connector == "apache":
        return {
            "results": base / crs / mrts / "results",
            "work": variant_work,
            "logs": variant_work / "logs/apache-runtime",
            "runtime": variant_work / "apache-runtime",
        }
    if connector == "nginx":
        return {
            "results": base / crs / mrts / "results",
            "work": variant_work,
            "logs": variant_work / "logs",
            "runtime": variant_work / "runtime",
        }
    return {
        "results": base / crs / mrts / "results",
        "work": variant_work,
        "logs": variant_work / "logs/haproxy-runtime",
        "runtime": variant_work / "haproxy-runtime-cases",
        "tmp": variant_work / "tmp",
    }


def build_harness_command(
    connector: str,
    connector_root: Path,
    framework_root: Path,
    build_root: Path,
    source_root: Path,
    tmp_root: Path,
    py: str,
    case: str,
    crs: str,
    mrts: str,
) -> tuple[list[str], dict[str, str], dict[str, Path]]:
    paths = harness_paths(connector, build_root, crs, mrts)
    env = os.environ.copy()
    env.update(
        {
            "PYTHON": py,
            "FRAMEWORK_ROOT": str(framework_root),
            "CONNECTOR_ROOT": str(connector_root),
            "FORCE_ALL_CASES": "1",
            "MODSECURITY_TEST_VARIANT": crs,
            "MODSECURITY_MRTS_VARIANT": mrts,
            "TEST_CASE": case,
            "CASE_SCOPE": "all",
            "RESULTS_DIR": str(paths["results"]),
            "BUILD_ROOT": str(build_root),
            "SOURCE_ROOT": str(source_root),
            "TMP_ROOT": str(tmp_root),
        }
    )
    if connector == "apache":
        env["APACHE_RUNTIME_LOG_DIR"] = str(paths["logs"])
        env["RUNTIME_BASE"] = str(paths["runtime"])
        harness = framework_root / "ci/runtime/run-apache-smoke.sh"
    elif connector == "nginx":
        env["NGINX_HARNESS_WORK_ROOT"] = str(paths["work"])
        harness = framework_root / "ci/runtime/run-nginx-smoke.sh"
    else:
        env["TMP_ROOT"] = str(paths["tmp"])
        env["LOG_ROOT"] = str(paths["work"] / "logs")
        env["RUNTIME_BASE"] = str(paths["runtime"])
        env["RUN_ONE_CASE"] = "1"
        harness = framework_root / "ci/runtime/run-haproxy-smoke.sh"

    cmd = ["sh", "ci/provisioning/cache/with-runtime-components.sh", "env"]
    for key in sorted(env):
        if key in {
            "APACHE_RUNTIME_LOG_DIR",
            "BUILD_ROOT",
            "CASE_SCOPE",
            "CONNECTOR_ROOT",
            "FORCE_ALL_CASES",
            "FRAMEWORK_ROOT",
            "LOG_ROOT",
            "MODSECURITY_MRTS_VARIANT",
            "MODSECURITY_TEST_VARIANT",
            "NGINX_HARNESS_WORK_ROOT",
            "PYTHON",
            "RESULTS_DIR",
            "RUNTIME_BASE",
            "RUN_ONE_CASE",
            "SOURCE_ROOT",
            "TEST_CASE",
            "TMP_ROOT",
        }:
            cmd.append(f"{key}={env[key]}")
    cmd.extend(["sh", str(harness)])
    return cmd, env, paths


def find_result_json(paths: dict[str, Path], case: str, started_at_ts: float) -> Path | None:
    candidates: list[Path] = []
    for root in {paths.get("logs"), paths.get("results"), paths.get("work")}:
        if root and root.exists():
            candidates.extend(root.rglob("result.json"))
    filtered = [path for path in candidates if case in str(path)]
    if not filtered and candidates:
        filtered = candidates
    recent = [path for path in filtered if path.stat().st_mtime >= started_at_ts - 5]
    chosen = recent or filtered
    if not chosen:
        return None
    return max(chosen, key=lambda path: path.stat().st_mtime)


def relevant_log_files(paths: dict[str, Path], case: str, result: dict[str, Any]) -> list[Path]:
    found: set[Path] = set()
    for key, value in result.items():
        if key.endswith("_path") or key in {"decision_log", "decision_log_path", "evidence_path"}:
            path = Path(str(value))
            if path.is_file():
                found.add(path)
    for root in {paths.get("logs"), paths.get("runtime"), paths.get("work")}:
        if not root or not root.exists():
            continue
        case_roots = [path for path in root.rglob(case) if path.is_dir()]
        if root.name == "haproxy-runtime":
            case_roots.append(root)
        for case_root in case_roots:
            for path in case_root.rglob("*"):
                if not path.is_file():
                    continue
                lower = path.name.lower()
                if path.suffix.lower() in LOG_EXTENSIONS or any(fragment in lower for fragment in LOG_NAME_FRAGMENTS):
                    found.add(path)
    return sorted(found)


def copy_or_excerpt_logs(logs: list[Path], output_dir: Path, limit_bytes: int = 2_000_000) -> list[dict[str, Any]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    artifacts: list[dict[str, Any]] = []
    used_names: set[str] = set()
    for source in logs:
        name = safe_name("-".join(source.parts[-4:]))
        if name in used_names:
            name = f"{source.stat().st_mtime_ns}-{name}"
        used_names.add(name)
        dest = output_dir / name
        size = source.stat().st_size
        copied = False
        if size <= limit_bytes:
            shutil.copy2(source, dest)
            copied = True
        else:
            text = source.read_text(encoding="utf-8", errors="replace")
            excerpt = text[: limit_bytes // 2] + "\n\n[... log truncated ...]\n\n" + text[-limit_bytes // 2 :]
            dest = dest.with_suffix(dest.suffix + ".excerpt")
            dest.write_text(excerpt, encoding="utf-8")
        artifacts.append({"source": str(source), "path": str(dest), "bytes": size, "copied": copied})
    return artifacts


def collect_log_excerpt(artifacts: list[dict[str, Any]], max_lines: int = 160) -> list[str]:
    lines: list[str] = []
    for artifact in artifacts:
        path = Path(str(artifact["path"]))
        if not path.is_file():
            continue
        try:
            text_lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception:
            continue
        for line in text_lines:
            if EXCERPT_PATTERNS.search(line):
                lines.append(f"{path.name}: {line[:500]}")
                if len(lines) >= max_lines:
                    return lines
    return lines


def result_rule_evidence(result: dict[str, Any], artifacts: list[dict[str, Any]]) -> dict[str, Any]:
    evidence = {
        "rule_id": result.get("rule_id") or result.get("matched_rule_id") or "-",
        "matched_data": result.get("matched_data") or result.get("matched_value_snippet") or "-",
        "matched_variable": result.get("matched_variable") or "-",
        "reason": result.get("reason") or "-",
        "decision": {},
    }
    for artifact in artifacts:
        path = Path(str(artifact["path"]))
        if "decision" not in path.name or not path.is_file():
            continue
        last_json: dict[str, Any] = {}
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                candidate = json.loads(line)
            except Exception:
                continue
            if isinstance(candidate, dict):
                last_json = candidate
        if last_json:
            evidence["decision"] = last_json
            if "rule_id" in last_json:
                evidence["rule_id"] = last_json.get("rule_id")
            evidence["matched_data"] = (
                last_json.get("matched_data")
                or last_json.get("matched_value_snippet")
                or last_json.get("matched_var_value")
                or evidence["matched_data"]
            )
            break
    return evidence


def load_mismatch_rows(connector_root: Path, case: str, connector: str, crs: str, mrts: str) -> dict[str, Any]:
    path = connector_root / "reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json"
    data = read_json(path)
    rows = [row for row in data.get("mismatches", []) if isinstance(row, dict) and str(row.get("case")) == case]
    exact = []
    for row in rows:
        variant = str(row.get("variant") or "")
        if row.get("connector") == connector and variant in {f"{crs}/{mrts}", crs, f"{crs}-{mrts}"}:
            exact.append(row)
    affected_jobs: set[tuple[str, str, str]] = {(connector, crs, mrts)}
    for row in rows:
        row_connector = str(row.get("connector") or "")
        variant = str(row.get("variant") or "")
        if not row_connector:
            continue
        if "/" in variant:
            row_crs, row_mrts = variant.split("/", 1)
        elif "-" in variant:
            parts = variant.split("-")
            row_crs = "-".join(parts[:2]) if len(parts) >= 4 else variant
            row_mrts = "-".join(parts[2:]) if len(parts) >= 4 else ""
        else:
            row_crs, row_mrts = variant, ""
        if row_crs and row_mrts:
            affected_jobs.add((row_connector, row_crs, row_mrts))

    evidence_files = []
    for row in exact or rows:
        for key in ("evidence_file", "evidence_path"):
            value = row.get(key)
            if value:
                evidence_files.append(str(value))
        evidence = row.get("evidence")
        if isinstance(evidence, dict):
            for value in evidence.values():
                if isinstance(value, str) and (value.endswith(".json") or value.endswith(".log") or value.endswith(".jsonl")):
                    evidence_files.append(value)
    return {
        "report": str(path),
        "case_rows": rows,
        "exact_rows": exact,
        "affected_jobs": [
            {
                "connector": item[0],
                "crs": item[1],
                "mrts": item[2],
                "command": f"make verified-full-matrix-job CONNECTOR={item[0]} CRS={item[1]} MRTS={item[2]}",
            }
            for item in sorted(affected_jobs)
        ],
        "evidence_files": sorted(set(evidence_files)),
    }


def resolve_evidence_path(path_value: str, connector_root: Path, build_root: Path, verified_run_root: Path) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    for root in (connector_root, build_root, verified_run_root):
        candidate = root / path
        if candidate.exists():
            return candidate
    return connector_root / path


def full_matrix_refresh_needed(
    mismatch: dict[str, Any],
    connector_root: Path,
    build_root: Path,
    verified_run_root: Path,
    case_run_mtime: float,
) -> bool:
    evidence_files = mismatch.get("evidence_files") or []
    existing: list[Path] = []
    for item in evidence_files:
        path = resolve_evidence_path(str(item), connector_root, build_root, verified_run_root)
        if path.exists():
            existing.append(path)
    if not existing:
        return bool(mismatch.get("case_rows"))
    return all(case_run_mtime > path.stat().st_mtime for path in existing)


def markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(item).replace("|", "\\|").replace("\n", " ") for item in row) + " |")
    return "\n".join(lines)


def render_markdown(report: dict[str, Any]) -> str:
    result = report["result"]
    request = report["case_definition"].get("request", {})
    official = report["official_mismatch_report"]
    exact_rows = official.get("exact_rows") or []
    case_rows = official.get("case_rows") or []
    official_rows = exact_rows or case_rows
    row_table = markdown_table(
        ["Classification", "Category", "Connector", "Variant", "Expected", "Actual", "Critical", "Evidence"],
        [
            [
                row.get("classification", "-"),
                row.get("category", "-"),
                row.get("connector", "-"),
                row.get("variant", "-"),
                row.get("expected", "-"),
                row.get("actual", "-"),
                row.get("critical", row.get("is_critical", "-")),
                row.get("evidence_file") or row.get("evidence_path") or "-",
            ]
            for row in official_rows
        ]
        or [["-", "-", "-", "-", "-", "-", "-", "-"]],
    )
    affected_jobs = markdown_table(
        ["Connector", "CRS", "MRTS", "Command"],
        [[job["connector"], job["crs"], job["mrts"], f"`{job['command']}`"] for job in official.get("affected_jobs", [])],
    )
    artifacts = markdown_table(
        ["Artifact", "Path"],
        [[Path(item["path"]).name, item["path"]] for item in report["evidence_artifacts"][:40]]
        or [["-", "-"]],
    )
    rule = report.get("rule_evidence", {})
    excerpt = "\n".join(f"- `{line}`" for line in report.get("log_excerpt", [])[:40]) or "- No focused log excerpt found."
    return "\n\n".join(
        [
            "# Verified Case Run",
            "## Summary",
            markdown_table(
                ["Field", "Value"],
                [
                    ["Connector", report["connector"]],
                    ["Case", report["case"]],
                    ["Variant", f"{report['crs']}/{report['mrts']}"],
                    ["Status", result.get("status", "-")],
                    ["Expected", result.get("expected_status", "-")],
                    ["Actual", result.get("actual_status", result.get("observed_status", "-"))],
                    ["Return Code", report["return_code"]],
                    ["Full-Matrix Refresh Needed", report["full_matrix_refresh_needed"]],
                ],
            ),
            "## Request",
            markdown_table(
                ["Field", "Value"],
                [
                    ["Case Definition", report["case_definition"].get("path", "-")],
                    ["Method", request.get("method", "-")],
                    ["URI", request.get("path", "-")],
                    ["Headers", json.dumps(request.get("headers", {}), sort_keys=True)],
                    ["Body", repr(request.get("body", ""))[:500]],
                    ["Transforms", ", ".join(report["case_definition"].get("transforms", [])) or "-"],
                    ["Rule IDs", ", ".join(report["case_definition"].get("rule_ids", [])) or "-"],
                ],
            ),
            "## Evidence",
            artifacts,
            "## Official Mismatch Context",
            row_table,
            "## Affected Full-Matrix Jobs",
            affected_jobs,
            "## Rule Evidence",
            markdown_table(
                ["Field", "Value"],
                [
                    ["Rule ID", rule.get("rule_id", "-")],
                    ["Matched Data", rule.get("matched_data", "-")],
                    ["Matched Variable", rule.get("matched_variable", "-")],
                    ["Reason", rule.get("reason", "-")],
                ],
            ),
            "## Log Excerpt",
            excerpt,
            "## Next Step",
            "\n".join(
                [
                    f"- Re-run this case: `make verified-case CONNECTOR={report['connector']} CASE={report['case']} CRS={report['crs']} MRTS={report['mrts']}`",
                    f"- Re-run the matching Full-Matrix job: `make verified-full-matrix-job CONNECTOR={report['connector']} CRS={report['crs']} MRTS={report['mrts']}`",
                ]
            ),
        ]
    )


def explain(args: argparse.Namespace, case_def: dict[str, Any], mismatch: dict[str, Any]) -> int:
    rows = mismatch.get("exact_rows") or mismatch.get("case_rows") or []
    print("Verified case explain")
    print(f"case: {args.case}")
    print(f"connector: {args.connector}")
    print(f"variant: {args.crs}/{args.mrts}")
    print(f"case_definition: {case_def.get('path', '-')}")
    print(f"would_run: make verified-case CONNECTOR={args.connector} CASE={args.case} CRS={args.crs} MRTS={args.mrts}")
    print(f"matching_report: {mismatch.get('report')}")
    print(f"listed_in_report: {'yes' if rows else 'no'}")
    if rows:
        print("official_rows:")
        for row in rows:
            print(
                "  "
                + json.dumps(
                    {
                        "classification": row.get("classification"),
                        "category": row.get("category"),
                        "connector": row.get("connector"),
                        "variant": row.get("variant"),
                        "expected": row.get("expected"),
                        "actual": row.get("actual"),
                        "critical": row.get("critical", row.get("is_critical")),
                        "evidence_file": row.get("evidence_file") or row.get("evidence_path"),
                    },
                    sort_keys=True,
                )
            )
    print("affected_full_matrix_jobs:")
    for job in mismatch.get("affected_jobs", []):
        print(f"  {job['command']}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run one verified runtime case and write focused local evidence.")
    parser.add_argument("--connector", required=True, choices=sorted(CONNECTORS))
    parser.add_argument("--case", required=True)
    parser.add_argument("--crs", required=True)
    parser.add_argument("--mrts", required=True)
    parser.add_argument("--connector-root", default=".")
    parser.add_argument("--framework-root", required=True)
    parser.add_argument("--build-root", required=True)
    parser.add_argument("--source-root", default=None)
    parser.add_argument("--tmp-root", default=None)
    parser.add_argument("--verified-run-root", default=None)
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument("--explain", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    connector_root = Path(args.connector_root).resolve()
    framework_root = Path(args.framework_root).resolve()
    build_root = Path(args.build_root).resolve()
    source_root = Path(args.source_root).resolve() if args.source_root else connector_root
    tmp_root = Path(args.tmp_root).resolve() if args.tmp_root else build_root / "tmp"
    verified_run_root = (
        Path(args.verified_run_root).resolve()
        if args.verified_run_root
        else Path(os.environ.get("VERIFIED_RUN_ROOT", "/var/tmp/ModSecurity-conector-verified")).resolve()
    )

    case_path = find_case_path(framework_root, args.case)
    case_def = summarize_case_definition(case_path)
    mismatch = load_mismatch_rows(connector_root, args.case, args.connector, args.crs, args.mrts)
    if args.explain:
        return explain(args, case_def, mismatch)

    started_at = utc_now()
    run_id = f"{started_at.strftime('%Y%m%dT%H%M%SZ')}-{safe_name(args.connector)}-{safe_name(args.case)}-{safe_name(args.crs)}-{safe_name(args.mrts)}"
    run_dir = verified_run_root / "case-runs" / run_id
    logs_dir = run_dir / "logs"
    run_dir.mkdir(parents=True, exist_ok=True)

    cmd, env, paths = build_harness_command(
        args.connector,
        connector_root,
        framework_root,
        build_root,
        source_root,
        tmp_root,
        args.python,
        args.case,
        args.crs,
        args.mrts,
    )
    command_log = run_dir / "command.log"
    return_code = 1
    with command_log.open("w", encoding="utf-8") as handle:
        handle.write("$ " + " ".join(cmd) + "\n")
        handle.flush()
        proc = subprocess.run(
            cmd,
            cwd=connector_root,
            env=env,
            stdout=handle,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        return_code = proc.returncode

    result_path = find_result_json(paths, args.case, started_at.timestamp())
    if result_path and result_path.is_file():
        result = read_json(result_path)
        shutil.copy2(result_path, run_dir / "result.json")
    else:
        result = {
            "status": "missing_result",
            "expected_status": case_def.get("expect", {}).get("status") if isinstance(case_def.get("expect"), dict) else None,
            "actual_status": None,
            "reason": "Harness completed without a discoverable result.json.",
        }
        write_json(run_dir / "result.json", result)
    result.setdefault("status", "unknown")

    logs = relevant_log_files(paths, args.case, result)
    logs.append(command_log)
    artifacts = copy_or_excerpt_logs(sorted(set(logs)), logs_dir)
    rule_evidence = result_rule_evidence(result, artifacts)
    log_excerpt = collect_log_excerpt(artifacts)
    case_run_mtime = (run_dir / "result.json").stat().st_mtime
    refresh_needed = full_matrix_refresh_needed(mismatch, connector_root, build_root, verified_run_root, case_run_mtime)
    ended_at = utc_now()

    report = {
        "schema_version": 1,
        "report_kind": "verified-case-run",
        "started_at": iso_utc(started_at),
        "ended_at": iso_utc(ended_at),
        "duration_seconds": round((ended_at - started_at).total_seconds(), 3),
        "connector": args.connector,
        "case": args.case,
        "crs": args.crs,
        "mrts": args.mrts,
        "return_code": return_code,
        "command": cmd,
        "case_definition": case_def,
        "result": result,
        "result_source": str(result_path) if result_path else "-",
        "evidence_artifacts": artifacts,
        "log_excerpt": log_excerpt,
        "rule_evidence": rule_evidence,
        "official_mismatch_report": mismatch,
        "full_matrix_refresh_needed": refresh_needed,
        "next_steps": {
            "case_rerun": f"make verified-case CONNECTOR={args.connector} CASE={args.case} CRS={args.crs} MRTS={args.mrts}",
            "full_matrix_job": f"make verified-full-matrix-job CONNECTOR={args.connector} CRS={args.crs} MRTS={args.mrts}",
        },
    }
    write_json(run_dir / "case-run.json", report)
    (run_dir / "case-run.md").write_text(render_markdown(report) + "\n", encoding="utf-8")

    print(f"case-run: {run_dir}")
    print(f"case-run.json: {run_dir / 'case-run.json'}")
    print(f"case-run.md: {run_dir / 'case-run.md'}")
    print(f"result.json: {run_dir / 'result.json'}")
    print(f"status: {result.get('status')} return_code={return_code}")
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
