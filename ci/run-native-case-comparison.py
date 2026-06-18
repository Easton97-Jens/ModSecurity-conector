#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from generated_report_utils import (
    DATA_SOURCE_POLICY,
    GENERATED_REPORTS,
    build_metadata,
    generated_json_text,
    generated_markdown_text,
    report_path,
)

try:
    import yaml
except Exception:  # pragma: no cover - runner reports missing PyYAML.
    yaml = None


DEFAULT_CASES = (
    "unicode_whitespace_normalization_gap",
    "unicode_double_encoded_uri_runtime_difference",
    "xml_namespace_edge_connector_gap",
    "xml_request_body_malformed_connector_gap",
    "v2_transformation_url_decode_invalid_sequence_mapped_candidate",
)
CONNECTORS = ("apache", "nginx", "haproxy")
VARIANTS = ("no-crs/no-mrts", "no-crs/with-mrts", "with-crs/no-mrts", "with-crs/with-mrts")


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_utc(value: datetime) -> str:
    return value.isoformat(timespec="seconds").replace("+00:00", "Z")


def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", value.strip()).strip("-") or "unknown"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_runtime_env(verified_run_root: Path) -> dict[str, str]:
    env = dict(os.environ)
    runtime_env = Path(
        env.get("CONNECTOR_COMPONENT_CACHE")
        or env.get("VERIFIED_COMPONENT_CACHE")
        or verified_run_root / "component-cache"
    ) / "runtime-env.sh"
    if not runtime_env.is_file():
        return env
    command = f". {sh_quote(str(runtime_env))}; env"
    proc = subprocess.run(
        ["sh", "-c", command],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return env
    for line in proc.stdout.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key] = value
    return env


def sh_quote(value: str) -> str:
    return "'" + value.replace("'", "'\"'\"'") + "'"


def find_case_path(framework_root: Path, case: str) -> Path | None:
    cases_root = framework_root / "tests/cases"
    if not cases_root.is_dir():
        return None
    matches = sorted(cases_root.rglob(f"{case}.yaml"))
    return matches[0] if matches else None


def load_case(case_path: Path) -> dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML is required for native case comparison")
    data = yaml.safe_load(case_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError(f"case YAML is not an object: {case_path}")
    return data


def normalize_request(case_data: dict[str, Any]) -> dict[str, Any]:
    request = case_data.get("request")
    if not isinstance(request, dict):
        request = {}
    headers = request.get("headers")
    if not isinstance(headers, dict):
        headers = {}
    normalized_headers = {str(key): str(value) for key, value in headers.items()}
    if "Host" not in normalized_headers and "host" not in {key.lower() for key in normalized_headers}:
        normalized_headers["Host"] = "127.0.0.1"
    body = request.get("body", "")
    if body is None:
        body = ""
    return {
        "method": str(request.get("method") or "GET"),
        "path": str(request.get("path") or request.get("uri") or request.get("url") or "/"),
        "headers": normalized_headers,
        "body": str(body),
    }


def expected_status(case_data: dict[str, Any]) -> int:
    expect = case_data.get("expect")
    if isinstance(expect, dict):
        try:
            return int(expect.get("status") or 200)
        except (TypeError, ValueError):
            return 200
    return 200


def materialize_rules(raw_rules: str, run_dir: Path) -> str:
    logs_dir = run_dir / "logs"
    audit_log = logs_dir / "audit.log"
    debug_log = logs_dir / "debug.log"
    audit_dir = logs_dir / "audit"
    audit_dir.mkdir(parents=True, exist_ok=True)
    rules = raw_rules.replace("@@AUDIT_LOG@@", str(audit_log)).replace("@@AUDIT_LOG_DIR@@", str(audit_dir))
    preamble = "\n".join(
        [
            "SecRequestBodyAccess On",
            f"SecDebugLog {debug_log}",
            "SecDebugLogLevel 9",
            "SecAuditEngine RelevantOnly",
            "SecAuditLogType Serial",
            f"SecAuditLog {audit_log}",
            "SecAuditLogParts ABHZ",
            "",
        ]
    )
    return preamble + rules.strip() + "\n"


def write_request_artifacts(request: dict[str, Any], run_dir: Path) -> dict[str, str]:
    body_bytes = str(request.get("body", "")).encode("utf-8")
    body_path = run_dir / "body.bin"
    headers_path = run_dir / "headers.tsv"
    request_path = run_dir / "request.json"
    body_path.write_bytes(body_bytes)
    with headers_path.open("w", encoding="utf-8") as handle:
        for key, value in request.get("headers", {}).items():
            handle.write(f"{key}\t{value}\n")
    request_payload = {
        "method": request.get("method", "GET"),
        "path": request.get("path", "/"),
        "headers": request.get("headers", {}),
        "body_sha256": hashlib.sha256(body_bytes).hexdigest(),
        "body_bytes": len(body_bytes),
        "body_preview": body_bytes[:200].decode("utf-8", errors="replace"),
    }
    write_json(request_path, request_payload)
    return {"body": str(body_path), "headers": str(headers_path), "request": str(request_path)}


def compile_oracle(connector_root: Path, run_root: Path, env: dict[str, str]) -> tuple[Path | None, dict[str, Any]]:
    source = connector_root / "ci/native_modsecurity_oracle.c"
    include_dir = env.get("MODSECURITY_INCLUDE_DIR")
    lib_dir = env.get("MODSECURITY_LIB_DIR")
    cc = env.get("CC", "cc")
    bin_dir = run_root / "native-oracle-bin"
    binary = bin_dir / "native_modsecurity_oracle"
    log_path = bin_dir / "compile.log"
    bin_dir.mkdir(parents=True, exist_ok=True)
    if not source.is_file():
        return None, {"status": "blocked", "reason": f"missing source {source}", "compile_log": str(log_path)}
    if not include_dir or not Path(include_dir).is_dir():
        return None, {"status": "blocked", "reason": "MODSECURITY_INCLUDE_DIR missing", "compile_log": str(log_path)}
    if not lib_dir or not (Path(lib_dir) / "libmodsecurity.so").exists():
        return None, {"status": "blocked", "reason": "MODSECURITY_LIB_DIR missing libmodsecurity.so", "compile_log": str(log_path)}
    needs_build = not binary.is_file() or binary.stat().st_mtime < source.stat().st_mtime
    if not needs_build:
        return binary, {"status": "reused", "binary": str(binary), "compile_log": str(log_path)}
    cmd = [
        cc,
        "-Wall",
        "-Wextra",
        "-I",
        include_dir,
        str(source),
        "-L",
        lib_dir,
        f"-Wl,-rpath,{lib_dir}",
        "-lmodsecurity",
        "-o",
        str(binary),
    ]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False, env=env)
    log_path.write_text("$ " + " ".join(cmd) + "\n" + proc.stdout, encoding="utf-8")
    if proc.returncode != 0:
        return None, {"status": "blocked", "reason": "oracle compile failed", "compile_log": str(log_path), "return_code": proc.returncode}
    return binary, {"status": "compiled", "binary": str(binary), "compile_log": str(log_path), "return_code": 0}


def extract_log_evidence(text: str) -> dict[str, Any]:
    rule_ids = sorted(set(re.findall(r'\[id "([0-9]+)"\]', text) + re.findall(r"\bid:([0-9]+)", text)))
    matched = re.findall(r"Matched Data:\s*(.*?)\s+found within", text)
    messages = re.findall(r'\[msg "([^"]+)"\]', text)
    return {
        "rule_ids": rule_ids,
        "matched_data": matched[:5],
        "messages": messages[:5],
    }


def run_native_case(
    case: str,
    connector_root: Path,
    framework_root: Path,
    verified_run_root: Path,
    env: dict[str, str],
) -> dict[str, Any]:
    started = utc_now()
    run_root = verified_run_root / "native-case-runs"
    run_dir = run_root / f"{started.strftime('%Y%m%dT%H%M%SZ')}-{safe_name(case)}"
    logs_dir = run_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    case_path = find_case_path(framework_root, case)
    if case_path is None:
        result = {
            "case": case,
            "status": "blocked",
            "native_actual": None,
            "reason": "case YAML not found",
            "run_dir": str(run_dir),
        }
        write_json(run_dir / "native-case-run.json", result)
        return result
    try:
        case_data = load_case(case_path)
    except Exception as exc:
        result = {
            "case": case,
            "status": "blocked",
            "native_actual": None,
            "reason": str(exc),
            "case_path": str(case_path),
            "run_dir": str(run_dir),
        }
        write_json(run_dir / "native-case-run.json", result)
        return result

    request = normalize_request(case_data)
    rules = materialize_rules(str(case_data.get("rules") or ""), run_dir)
    rules_path = run_dir / "rules.conf"
    rules_path.write_text(rules, encoding="utf-8")
    request_paths = write_request_artifacts(request, run_dir)
    expected = expected_status(case_data)
    binary, compile_info = compile_oracle(connector_root, run_root, env)
    native_result_path = run_dir / "native-result.json"
    server_log_path = logs_dir / "server-log.log"

    return_code = 77
    if binary is None:
        native_result = {
            "status": "blocked",
            "reason": compile_info.get("reason", "oracle binary unavailable"),
            "expected_status": expected,
            "actual_status": None,
            "native_match": False,
        }
        write_json(native_result_path, native_result)
    else:
        run_env = dict(env)
        lib_dir = env.get("MODSECURITY_LIB_DIR", "")
        existing_ld = run_env.get("LD_LIBRARY_PATH", "")
        if lib_dir:
            run_env["LD_LIBRARY_PATH"] = lib_dir + (":" + existing_ld if existing_ld else "")
        cmd = [
            str(binary),
            str(rules_path),
            request_paths["headers"],
            request_paths["body"],
            request["method"],
            request["path"],
            str(expected),
            str(native_result_path),
            str(server_log_path),
        ]
        command_log = logs_dir / "command.log"
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False, env=run_env)
        command_log.write_text("$ " + " ".join(cmd) + "\n" + proc.stdout, encoding="utf-8")
        return_code = proc.returncode
        native_result = read_json(native_result_path)
        if not native_result:
            native_result = {
                "status": "blocked",
                "reason": "oracle did not produce native-result.json",
                "expected_status": expected,
                "actual_status": None,
                "native_match": False,
            }
            write_json(native_result_path, native_result)
    if str(native_result.get("status") or "") in {"blocked", "setup_error", "not_executable"}:
        native_result["actual_status"] = None
        native_result["native_match"] = False
        write_json(native_result_path, native_result)

    log_text_parts = []
    for path in sorted(logs_dir.rglob("*")):
        if path.is_file() and path.suffix in {".log", ".txt"}:
            log_text_parts.append(path.read_text(encoding="utf-8", errors="replace"))
    log_evidence = extract_log_evidence("\n".join(log_text_parts))
    official = official_context(connector_root, case)
    comparison = compare_native_to_connectors(native_result, official)
    ended = utc_now()
    report = {
        "schema_version": 1,
        "report_kind": "native-case-run",
        "case": case,
        "case_path": str(case_path),
        "run_dir": str(run_dir),
        "started_at": iso_utc(started),
        "ended_at": iso_utc(ended),
        "duration_seconds": round((ended - started).total_seconds(), 3),
        "expected_status": expected,
        "native_actual": native_result.get("actual_status"),
        "native_match": bool(native_result.get("native_match")),
        "status": native_result.get("status", "unknown"),
        "return_code": return_code,
        "reason": native_result.get("reason", ""),
        "request": read_json(Path(request_paths["request"])),
        "rules_sha256": sha256_file(rules_path),
        "request_sha256": sha256_file(Path(request_paths["request"])),
        "input_hash": combined_hash([case_path, rules_path, Path(request_paths["request"])]),
        "rules_path": str(rules_path),
        "request_path": request_paths["request"],
        "native_result_path": str(native_result_path),
        "logs_dir": str(logs_dir),
        "compile": compile_info,
        "libmodsecurity": native_result.get("libmodsecurity") or env.get("MODSECURITY_SOURCE_SHA") or "unknown",
        "log_evidence": log_evidence,
        "official_mismatch_context": official,
        "connector_comparison": comparison["rows"],
        "classification_hint": comparison["classification_hint"],
        "decision": comparison["decision"],
        "full_matrix_refresh_needed": False,
    }
    write_json(run_dir / "native-case-run.json", report)
    (run_dir / "native-case-run.md").write_text(render_case_markdown(report), encoding="utf-8")
    return report


def combined_hash(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in paths:
        digest.update(str(path).encode("utf-8"))
        digest.update(b"\0")
        digest.update(sha256_file(path).encode("ascii"))
        digest.update(b"\0")
    return digest.hexdigest()


def official_context(connector_root: Path, case: str) -> dict[str, Any]:
    path = report_path(connector_root, "verified_runtime_mismatch_analysis", "json")
    data = read_json(path)
    rows = [row for row in data.get("mismatches", []) if isinstance(row, dict) and row.get("case") == case]
    compact_rows = []
    for row in rows:
        compact_rows.append(
            {
                "case": row.get("case"),
                "connector": row.get("connector"),
                "variant": row.get("variant"),
                "expected": row.get("expected"),
                "actual": row.get("actual"),
                "classification": row.get("classification"),
                "category": row.get("category"),
                "full_matrix_refresh_needed": bool(row.get("full_matrix_refresh_needed", False)),
                "evidence_file": row.get("evidence_file") or row.get("evidence_path"),
            }
        )
    return {
        "report": str(path),
        "rows": compact_rows,
        "row_count": len(compact_rows),
        "classifications": dict(Counter(str(row.get("classification") or "unknown") for row in compact_rows)),
    }


def normalize_status(value: Any) -> str:
    if value is None:
        return "-"
    text = str(value)
    if text.endswith(".0"):
        text = text[:-2]
    return text


def compare_native_to_connectors(native_result: dict[str, Any], official: dict[str, Any]) -> dict[str, Any]:
    native_actual = normalize_status(native_result.get("actual_status"))
    expected = normalize_status(native_result.get("expected_status"))
    rows = []
    connector_actuals: dict[str, set[str]] = defaultdict(set)
    for row in official.get("rows", []):
        actual = normalize_status(row.get("actual"))
        connector_actuals[str(row.get("connector") or "-")].add(actual)
        same = actual == native_actual and native_actual != "-"
        if native_actual == "-":
            meaning = "native_comparison_missing"
        elif same:
            meaning = "same_as_native"
        elif native_actual == expected:
            meaning = "connector_differs_from_native_expected"
        else:
            meaning = "connector_differs_from_native"
        rows.append(
            {
                "connector": row.get("connector"),
                "variant": row.get("variant"),
                "connector_actual": actual,
                "native_actual": native_actual,
                "same": same,
                "meaning": meaning,
                "classification": row.get("classification"),
                "full_matrix_refresh_needed": bool(row.get("full_matrix_refresh_needed", False)),
                "evidence_file": row.get("evidence_file"),
            }
        )
    all_actuals = {actual for values in connector_actuals.values() for actual in values}
    all_three = all(connector in connector_actuals for connector in CONNECTORS)
    all_same_as_native = bool(rows) and all(row["same"] for row in rows)
    any_same_as_native = any(row["same"] for row in rows)
    all_connectors_same = len(all_actuals) == 1 and all_three
    all_refresh_needed = bool(rows) and all(bool(row.get("full_matrix_refresh_needed")) for row in official.get("rows", []))
    status = str(native_result.get("status") or "")
    if status in {"blocked", "setup_error", "not_executable"} or native_actual == "-":
        hint = "native_comparison_missing"
        decision = "DEFER"
    elif all_refresh_needed and native_actual == expected:
        hint = "full_matrix_refresh_needed"
        decision = "REFRESH"
    elif all_same_as_native and native_actual != expected:
        hint = "likely_framework_expected_behavior_gap_or_libmodsecurity_semantics"
        decision = "DOCUMENT"
    elif native_actual == expected and not any_same_as_native and all_connectors_same:
        hint = "common_harness_or_input_issue_possible"
        decision = "DEFER"
    elif native_actual == expected and not all_same_as_native:
        hint = "connector_bug_or_harness_gap_possible"
        decision = "DEFER"
    else:
        hint = "unknown"
        decision = "DEFER"
    return {"rows": rows, "classification_hint": hint, "decision": decision}


def latest_case_runs(verified_run_root: Path, cases: tuple[str, ...]) -> list[dict[str, Any]]:
    runs_root = verified_run_root / "native-case-runs"
    output = []
    for case in cases:
        candidates = sorted(runs_root.glob(f"*-{safe_name(case)}/native-case-run.json"))
        if not candidates:
            output.append({"case": case, "status": "missing", "reason": "no native case run found"})
            continue
        output.append(read_json(candidates[-1]))
    return output


def refresh_official_context(connector_root: Path, reports: list[dict[str, Any]]) -> list[dict[str, Any]]:
    refreshed = []
    for report in reports:
        item = dict(report)
        case = str(item.get("case") or "")
        if not case or item.get("status") == "missing":
            refreshed.append(item)
            continue
        official = official_context(connector_root, case)
        native_result = {
            "actual_status": item.get("native_actual"),
            "expected_status": item.get("expected_status"),
            "status": item.get("status"),
        }
        comparison = compare_native_to_connectors(native_result, official)
        item["official_mismatch_context"] = official
        item["connector_comparison"] = comparison["rows"]
        item["classification_hint"] = comparison["classification_hint"]
        item["decision"] = comparison["decision"]
        refreshed.append(item)
    return refreshed


def reclassified_rows(reports: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for report in reports:
        rows = [
            row
            for row in report.get("connector_comparison", [])
            if row.get("classification") == "libmodsecurity_transformation_semantics"
        ]
        if not rows:
            continue
        output.append(
            {
                "case": report.get("case"),
                "rows": len(rows),
                "classification": "libmodsecurity_transformation_semantics",
                "native_actual": normalize_status(report.get("native_actual")),
                "decision": report.get("decision"),
            }
        )
    return output


def inventory(connector_root: Path, framework_root: Path) -> list[dict[str, str]]:
    return [
        {
            "tool_target": "tools/MRTS/mrts/generate-rules.py",
            "purpose": "Generate MRTS rules and go-ftw tests from upstream MRTS YAML definitions.",
            "inputs": "MRTS config_tests YAML",
            "outputs": "$BUILD_ROOT/mrts/*/rules and ftw",
            "single_case": "no; corpus generator",
        },
        {
            "tool_target": "framework Makefile mrts-generate/mrts-import/mrts-ftw",
            "purpose": "Prepare/import MRTS corpora and optionally run go-ftw.",
            "inputs": "MRTS corpus definitions and infra config",
            "outputs": "generated framework cases, rules, go-ftw results",
            "single_case": "not for framework YAML cases",
        },
        {
            "tool_target": "ci/run-mrts-native-full.sh",
            "purpose": "Stage native Apache/NGINX MRTS infra and run the MRTS suite through go-ftw.",
            "inputs": "MRTS generated corpus, native Apache/NGINX binaries, libmodsecurity",
            "outputs": "$BUILD_ROOT/mrts-native/*/job.json and logs",
            "single_case": "no; suite-oriented MRTS evidence",
        },
        {
            "tool_target": "framework:ci/generate-mrts-native-report.py",
            "purpose": "Summarize native MRTS jobs into generated reports.",
            "inputs": "$MRTS_NATIVE_ROOT/apache2_ubuntu/job.json and nginx-pr24/job.json",
            "outputs": "reports/testing/generated/mrts-native/*.generated.*",
            "single_case": "no; summarizes completed native MRTS jobs",
        },
        {
            "tool_target": "ci/run-native-case-comparison.py",
            "purpose": "Run one framework YAML case through connector-free libmodsecurity C API.",
            "inputs": "framework case YAML, native_modsecurity_oracle.c, libmodsecurity runtime-env",
            "outputs": "$VERIFIED_RUN_ROOT/native-case-runs/<timestamp>-<case>/ and native-semantics-comparison.generated.*",
            "single_case": "yes",
        },
    ]


def render_case_markdown(report: dict[str, Any]) -> str:
    return "\n\n".join(
        [
            "# Native Case Run",
            md_table(
                ["Field", "Value"],
                [
                    ["Case", report.get("case", "-")],
                    ["Expected Status", report.get("expected_status", "-")],
                    ["Native Actual", report.get("native_actual", "-")],
                    ["Native Match", "yes" if report.get("native_match") else "no"],
                    ["Status", report.get("status", "-")],
                    ["Rule ID", ", ".join(report.get("log_evidence", {}).get("rule_ids", [])) or "-"],
                    ["Matched Data", ", ".join(report.get("log_evidence", {}).get("matched_data", [])) or "-"],
                    ["Classification Hint", report.get("classification_hint", "-")],
                ],
            ),
            "## Connector Comparison",
            md_table(
                ["Connector", "Variant", "Connector Actual", "Native Actual", "Same", "Meaning"],
                [
                    [row["connector"], row["variant"], row["connector_actual"], row["native_actual"], row["same"], row["meaning"]]
                    for row in report.get("connector_comparison", [])
                ]
                or [["-", "-", "-", "-", "-", "no official Full-Matrix row found"]],
            ),
            "## Artifacts",
            md_table(
                ["Artifact", "Path"],
                [
                    ["request.json", report.get("request_path", "-")],
                    ["rules.conf", report.get("rules_path", "-")],
                    ["native-result.json", report.get("native_result_path", "-")],
                    ["logs", report.get("logs_dir", "-")],
                ],
            ),
        ]
    ) + "\n"


def md_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    if not rows:
        lines.append("| " + " | ".join("_No rows available. Reason: no data._" for _ in headers) + " |")
    for row in rows:
        lines.append("| " + " | ".join(str(item).replace("|", "\\|").replace("\n", " ") for item in row) + " |")
    return "\n".join(lines)


def render_summary_markdown(payload: dict[str, Any]) -> str:
    comparison_rows = []
    for item in payload.get("cases", []):
        connector_actuals = Counter(
            f"{row.get('connector')}:{row.get('variant')}={row.get('connector_actual')}"
            for row in item.get("connector_comparison", [])
        )
        comparison_rows.append(
            [
                item.get("case", "-"),
                item.get("native_actual", "-"),
                ", ".join(sorted(connector_actuals)) or "-",
                "yes" if item.get("native_match") else "no",
                item.get("decision", "-"),
                item.get("classification_hint", "-"),
            ]
        )
    reclassified = payload.get("reclassified", [])
    reclassified_table = (
        md_table(
            ["Case", "Rows", "Classification", "Native Actual", "Decision"],
            [
                [
                    item.get("case", "-"),
                    item.get("rows", "-"),
                    item.get("classification", "-"),
                    item.get("native_actual", "-"),
                    item.get("decision", "-"),
                ]
                for item in reclassified
            ],
        )
        if reclassified
        else "_No rows available. Reason: no current official rows are classified from native semantics evidence._"
    )
    return "\n\n".join(
        [
            "# Native Semantics Comparison",
            "## Tool Inventory",
            md_table(
                ["Tool/Target", "Purpose", "Inputs", "Outputs", "Usable for Single Case?"],
                [
                    [row["tool_target"], row["purpose"], row["inputs"], row["outputs"], row["single_case"]]
                    for row in payload.get("tool_inventory", [])
                ],
            ),
            "## Native Comparisons",
            md_table(
                ["Case", "Native Actual", "Connector Actuals", "Native Match", "Decision", "Classification Hint"],
                comparison_rows,
            ),
            "## Reclassified",
            reclassified_table,
            "## Fixed",
            "_No rows available. Reason: this pass added native comparison tooling only._",
            "## Deferred",
            md_table(
                ["Case", "Reason"],
                [
                    [item.get("case", "-"), item.get("classification_hint", item.get("reason", "-"))]
                    for item in payload.get("cases", [])
                    if item.get("decision") == "DEFER"
                ],
            ),
            "## Notes",
            f"- Data source policy: `{DATA_SOURCE_POLICY}`.",
            "- Native comparison rows are refreshed from the current verified runtime mismatch analysis; no PASS/FAIL values are invented.",
        ]
    )


def write_summary_report(
    connector_root: Path,
    framework_root: Path,
    build_root: Path,
    verified_run_root: Path,
    cases: tuple[str, ...],
    run_reports: list[dict[str, Any]] | None,
    output_dir: Path,
) -> dict[str, Any]:
    reports = run_reports if run_reports is not None else latest_case_runs(verified_run_root, cases)
    reports = refresh_official_context(connector_root, reports)
    inv = inventory(connector_root, framework_root)
    inputs: list[Path | str] = [
        connector_root / "ci/run-native-case-comparison.py",
        connector_root / "ci/native_modsecurity_oracle.c",
        report_path(connector_root, "verified_runtime_mismatch_analysis", "json"),
    ]
    for item in reports:
        if item.get("case_path"):
            inputs.append(str(item["case_path"]))
        if item.get("run_dir"):
            run_json = Path(str(item["run_dir"])) / "native-case-run.json"
            if run_json.is_file():
                inputs.append(run_json)
    payload = {
        "report_kind": "native-semantics-comparison",
        "data_source_policy": DATA_SOURCE_POLICY,
        "verified_run_id": os.environ.get("VERIFIED_RUN_ID") or "",
        "tool_inventory": inv,
        "native_tool": {
            "source": "ci/native_modsecurity_oracle.c",
            "runner": "ci/run-native-case-comparison.py",
        },
        "cases": reports,
        "reclassified": reclassified_rows(reports),
        "fixed": [],
        "full_matrix_refresh_needed": False,
    }
    metadata = build_metadata(
        generated_by=GENERATED_REPORTS["native_semantics_comparison"].generator,
        make_target=GENERATED_REPORTS["native_semantics_comparison"].make_target,
        connector_root=connector_root,
        framework_root=framework_root,
        inputs=inputs,
        report_key="native_semantics_comparison",
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / GENERATED_REPORTS["native_semantics_comparison"].filename("json")
    md_path = output_dir / GENERATED_REPORTS["native_semantics_comparison"].filename("md")
    json_path.write_text(generated_json_text(payload, metadata), encoding="utf-8")
    md_path.write_text(generated_markdown_text(render_summary_markdown(payload), metadata), encoding="utf-8")
    return {"json": str(json_path), "md": str(md_path), "payload": payload}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run connector-free native libmodsecurity comparison for framework cases.")
    parser.add_argument("--case", action="append", dest="cases")
    parser.add_argument("--connector-root", default=".")
    parser.add_argument("--framework-root", default=None)
    parser.add_argument("--build-root", default=None)
    parser.add_argument("--verified-run-root", default=None)
    parser.add_argument("--output-dir", default="reports/testing/generated/manifest")
    parser.add_argument("--report-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    connector_root = Path(args.connector_root).resolve()
    framework_root = Path(args.framework_root).resolve() if args.framework_root else connector_root / "modules/ModSecurity-test-Framework"
    verified_run_root = (
        Path(args.verified_run_root).resolve()
        if args.verified_run_root
        else Path(os.environ.get("VERIFIED_RUN_ROOT", "/var/tmp/ModSecurity-conector-verified")).resolve()
    )
    build_root = Path(args.build_root).resolve() if args.build_root else verified_run_root / "build"
    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = connector_root / output_dir
    cases = tuple(args.cases or DEFAULT_CASES)
    run_reports: list[dict[str, Any]] | None = None
    rc = 0
    if not args.report_only:
        env = load_runtime_env(verified_run_root)
        run_reports = []
        for case in cases:
            report = run_native_case(case, connector_root, framework_root, verified_run_root, env)
            run_reports.append(report)
            print(f"native-case-run: {report.get('run_dir')}")
            print(f"case={case} status={report.get('status')} native_actual={report.get('native_actual')} decision={report.get('decision')}")
            status = str(report.get("status") or "")
            if status in {"blocked", "setup_error"}:
                rc = 77 if rc == 0 else rc
            elif status == "not_executable" and rc == 0:
                rc = 2
    summary = write_summary_report(connector_root, framework_root, build_root, verified_run_root, cases, run_reports, output_dir)
    print(summary["md"])
    print(summary["json"])
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
