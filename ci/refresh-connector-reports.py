#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from generated_report_utils import (
    DATA_SOURCE_POLICY,
    FILENAME_TO_KEY,
    GENERATED_REPORTS,
    GENERATED_ROOT,
    build_metadata,
    current_verified_run_id,
    generated_json_text,
    generated_at_from_report,
    generated_markdown_text,
    generated_report_outputs,
    input_record,
    input_status_summary,
    legacy_report_path,
    legacy_report_relpath,
    registry_record,
    report_outputs,
    report_path,
    report_path_from_root,
    report_relpath,
    rewrite_generated_relpath,
    resolve_input_reference,
)

REPORT_DIR = GENERATED_ROOT


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def iso_from_timestamp(value: float | None) -> str:
    if value is None:
        return "-"
    return datetime.fromtimestamp(value, timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def path_mtime(path: Path) -> float | None:
    try:
        return path.stat().st_mtime if path.exists() else None
    except OSError:
        return None


def git_output(args: list[str], cwd: Path) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=str(cwd),
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
    except Exception as exc:
        return f"unknown: {exc}"
    return result.stdout.strip()


def git_dirty_status(root: Path) -> str:
    status = git_output(["status", "--short"], root)
    if status.startswith("unknown:"):
        return "unknown"
    return "dirty" if status else "clean"


def git_branch(root: Path) -> str:
    return git_output(["rev-parse", "--abbrev-ref", "HEAD"], root) or "unknown"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def combined_fingerprint(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    seen = False
    for path in sorted(paths, key=lambda item: str(item)):
        if not path.is_file():
            continue
        seen = True
        digest.update(str(path).encode("utf-8"))
        digest.update(b"\0")
        digest.update(sha256_file(path).encode("ascii"))
        digest.update(b"\0")
    return digest.hexdigest() if seen else "missing"


def git_sha(root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except Exception:
        return "unknown"
    return result.stdout.strip() or "unknown"


def display_path(path: Path, connector_root: Path, framework_root: Path, build_root: Path) -> str:
    path = path.resolve(strict=False)
    roots = (
        (connector_root.resolve(strict=False), ""),
        (framework_root.resolve(strict=False), "framework:"),
        (build_root.resolve(strict=False), "BUILD_ROOT:"),
    )
    for root, prefix in roots:
        try:
            rel = path.relative_to(root)
        except ValueError:
            continue
        return prefix + str(rel)
    return f"<local>/{path.name}"


def run_command(cmd: list[str], cwd: Path, env: dict[str, str]) -> tuple[int, str, dict[str, Any]]:
    print("refresh-connector-reports: RUN " + " ".join(cmd))
    started = time.monotonic()
    proc = subprocess.run(
        cmd,
        cwd=str(cwd),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    if proc.stdout:
        print(proc.stdout.rstrip())
    output = proc.stdout or ""
    log_info: dict[str, Any] = {
        "output_sha256": hashlib.sha256(output.encode("utf-8", errors="replace")).hexdigest(),
        "log_path": None,
        "log_hash": None,
        "duration_seconds": round(time.monotonic() - started, 3),
    }
    log_root = env.get("VERIFIED_RUN_LOG_ROOT")
    if log_root:
        logs_dir = Path(log_root) / "generator-logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        slug_source = cmd[-1] if cmd else "command"
        slug = "".join(ch if ch.isalnum() else "-" for ch in slug_source).strip("-") or "command"
        log_path = logs_dir / f"{int(time.time() * 1000)}-{slug[:80]}.log"
        log_path.write_text(output, encoding="utf-8")
        log_info["log_path"] = str(log_path)
        log_info["log_hash"] = sha256_file(log_path)
    return proc.returncode, output, log_info


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def read_verified_commands(env: dict[str, str]) -> list[dict[str, Any]]:
    path_value = env.get("VERIFIED_RUN_COMMANDS_FILE")
    if not path_value:
        return []
    path = Path(path_value)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []
    commands = data.get("commands") if isinstance(data, dict) else data
    return commands if isinstance(commands, list) else []


def verified_command_for_target(env: dict[str, str], target: str) -> dict[str, Any]:
    for command in read_verified_commands(env):
        raw = command.get("command")
        if command.get("logical_target") == target:
            return command
        if isinstance(raw, list) and raw == ["make", target]:
            return command
    return {}


def full_matrix_job_evidence_complete(env: dict[str, str]) -> bool:
    connector_root_value = env.get("CONNECTOR_ROOT") or "."
    connector_root = Path(connector_root_value).resolve()
    data = read_json(report_path(connector_root, "full_matrix_job_completeness", "json"))
    try:
        complete = int(data.get("complete_jobs") or 0)
        total = int(data.get("total_jobs") or 0)
    except (TypeError, ValueError):
        return False
    return total > 0 and complete >= total and str(data.get("evidence_scope") or "") == "full"


def full_matrix_producer_block(spec: ReportSpec, env: dict[str, str]) -> tuple[str, str]:
    if spec.name != "full_runtime_matrix":
        return "", ""
    if env.get("VERIFIED_RUN_PROFILE") == "smoke":
        return "blocked_smoke_only", "smoke verified run does not produce merge-ready full matrix evidence"
    if full_matrix_job_evidence_complete(env):
        return "", ""
    command = verified_command_for_target(env, "full-matrix-parallel")
    if not command:
        return "", ""
    if command.get("runtime_complete") is True or str(command.get("runtime_status") or "").startswith("runtime_completed"):
        return "", ""
    try:
        return_code = int(command.get("return_code", 1))
    except (TypeError, ValueError):
        return_code = 1
    if command.get("status") == "PASS" and return_code == 0:
        return "", ""
    classification = str(command.get("classification") or "command_failed")
    if classification == "blocked_timeout":
        return "blocked_timeout", "full-matrix-parallel timed out before producing complete verified evidence"
    if classification == "interrupted":
        return "interrupted", "full-matrix-parallel was interrupted before producing complete verified evidence"
    return "blocked", f"full-matrix-parallel did not complete successfully: {classification}"


@dataclass(frozen=True)
class ReportSpec:
    name: str
    owner: str
    generator: str
    make_target: str
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    command: tuple[str, ...]
    requires_runtime: bool = False
    requires_native_mrts: bool = False
    requires_full_matrix: bool = False
    optional: bool = False


CONNECTOR_COVERAGE_OUTPUTS = ("reports/testing/test-coverage-overview.md",) + generated_report_outputs(
    [
        "apache_runtime_results",
        "case_matrix",
        "connector_gap_summary",
        "coverage_summary",
        "haproxy_runtime_results",
        "nginx_runtime_results",
        "phase_coverage",
        "runtime_matrix",
        "xfail_summary",
    ]
)
FULL_RUNTIME_OUTPUTS = generated_report_outputs(["full_runtime_matrix"])
CONNECTOR_WORK_QUEUE_OUTPUTS = generated_report_outputs(["connector_work_queue"])
PHASE_WORK_QUEUE_OUTPUTS = generated_report_outputs(["phase_work_queue"])
NATIVE_OUTPUTS = generated_report_outputs(
    ["mrts_native_full", "mrts_native_apache", "mrts_native_nginx", "mrts_native_summary"]
)
FULL_RUN_EVIDENCE_OUTPUTS = generated_report_outputs(["full_run_evidence"])
RUNTIME_CACHE_OUTPUTS = generated_report_outputs(["runtime_component_cache", "runtime_build_cache", "runtime_cache_index"])
FULL_MATRIX_JOB_COMPLETENESS_OUTPUTS = generated_report_outputs(["full_matrix_job_completeness"])
VERIFIED_RUNTIME_MISMATCH_OUTPUTS = generated_report_outputs(["verified_runtime_mismatch_analysis"])
NGINX_MRTS_HTTP500_OUTPUTS = generated_report_outputs(["nginx_mrts_http500_cluster_analysis"])
NATIVE_SEMANTICS_OUTPUTS = generated_report_outputs(["native_semantics_comparison"])
NOLOG_OUTPUTS = generated_report_outputs(["nolog_audit_evidence"])
RESPONSE_HEADER_OUTPUTS = generated_report_outputs(["response_header_hook_analysis"])
PHASE4_OUTPUTS = generated_report_outputs(["phase4_hard_abort_capability"])
INTERVENTION_BLOCKING_OUTPUTS = generated_report_outputs(["intervention_blocking_analysis"])
NO_MRTS_NOMATCH_OUTPUTS = generated_report_outputs(["no_mrts_intervention_nomatch_analysis"])
BODY_PROCESSOR_OUTPUTS = generated_report_outputs(["body_processor_analysis"])
RULE_CHAIN_OUTPUTS = generated_report_outputs(["rule_chain_semantics_analysis"])
FINAL_CONSISTENCY_OUTPUTS = generated_report_outputs(["final_consistency_audit"])
REMAINING_OUTPUTS = generated_report_outputs(["remaining_failure_analysis", "next_fix_plan"])


def make_catalog(connector_root: Path, framework_root: Path, build_root: Path, native_root: Path, python: str) -> list[ReportSpec]:
    report_dir = connector_root / REPORT_DIR
    verified_run_root = Path(os.environ.get("VERIFIED_RUN_ROOT", "/var/tmp/ModSecurity-conector-verified"))
    component_cache_root = Path(
        os.environ.get("CONNECTOR_COMPONENT_CACHE")
        or os.environ.get("VERIFIED_COMPONENT_CACHE")
        or verified_run_root / "component-cache"
    ).resolve()
    existing_full_matrix = read_json(report_path(connector_root, "full_runtime_matrix", "json"))
    if not existing_full_matrix:
        existing_full_matrix = read_json(legacy_report_path(connector_root, "full_runtime_matrix", "json"))
    explicit_manifest = False
    if os.environ.get("FULL_MATRIX_MANIFEST"):
        explicit_manifest = True
        full_matrix_manifest = Path(str(os.environ["FULL_MATRIX_MANIFEST"]))
    elif os.environ.get("MATRIX_ROOT"):
        full_matrix_manifest = Path(str(os.environ["MATRIX_ROOT"])) / "full-runtime-matrix-runs.jsonl"
    elif existing_full_matrix.get("manifest"):
        full_matrix_manifest = Path(str(existing_full_matrix["manifest"]))
    else:
        full_matrix_manifest = build_root / "full-matrix" / "full-runtime-matrix-runs.jsonl"
    full_matrix_build_root = Path(str(existing_full_matrix.get("build_root") or build_root))
    if explicit_manifest:
        full_matrix_build_root = full_matrix_manifest.parent
    if os.environ.get("MATRIX_ROOT"):
        full_matrix_build_root = Path(str(os.environ["MATRIX_ROOT"]))
    full_matrix_log_root = Path(str(existing_full_matrix.get("log_root") or os.environ.get("LOG_ROOT", str(build_root / "logs"))))
    if explicit_manifest:
        full_matrix_log_root = full_matrix_manifest.parent
    if os.environ.get("MATRIX_ROOT"):
        full_matrix_log_root = Path(str(os.environ["MATRIX_ROOT"]))
    return [
        ReportSpec(
            name="connector_coverage_reports",
            owner="connector",
            generator="framework:ci/generate-case-matrix.py",
            make_target="generate-test-matrix",
            inputs=(
                "config/testing/import-status.json",
                "reports/testing/runtime-validation-snapshot.json",
            ),
            outputs=CONNECTOR_COVERAGE_OUTPUTS,
            command=(
                "make",
                "-C",
                str(framework_root),
                "generate-test-matrix",
                f"PYTHON={python}",
                f"FRAMEWORK_ROOT={framework_root}",
                f"CONNECTOR_ROOT={connector_root}",
                f"OUTPUT_ROOT={connector_root}",
                "SKIP_ROOT_SUMMARY=1",
            ),
            requires_runtime=True,
        ),
        ReportSpec(
            name="full_runtime_matrix",
            owner="connector",
            generator="ci/generate-full-runtime-matrix.py",
            make_target="generate-full-runtime-matrix",
            inputs=(str(full_matrix_manifest),),
            outputs=FULL_RUNTIME_OUTPUTS,
            command=(
                python,
                "ci/generate-full-runtime-matrix.py",
                "--connector-root",
                str(connector_root),
                "--framework-root",
                str(framework_root),
                "--build-root",
                str(full_matrix_build_root),
                "--log-root",
                str(full_matrix_log_root),
                "--manifest",
                str(full_matrix_manifest),
                "--output-dir",
                str(report_dir),
            ),
            requires_runtime=True,
            requires_full_matrix=True,
        ),
        ReportSpec(
            name="full_matrix_job_completeness",
            owner="connector",
            generator="ci/generate-full-matrix-job-completeness.py",
            make_target="generate-full-matrix-job-completeness",
            inputs=(
                str(Path(os.environ.get("VERIFIED_RUN_COMMANDS_FILE", str(build_root / "verified-runs" / current_verified_run_id(connector_root) / "verified-commands.json")))),
                str(full_matrix_manifest),
            ),
            outputs=FULL_MATRIX_JOB_COMPLETENESS_OUTPUTS,
            command=(
                python,
                "ci/generate-full-matrix-job-completeness.py",
                "--connector-root",
                str(connector_root),
                "--framework-root",
                str(framework_root),
                "--build-root",
                str(build_root),
                "--output-dir",
                str(report_dir / "manifest"),
                "--verified-run-id",
                current_verified_run_id(connector_root),
                "--verified-commands-file",
                str(Path(os.environ.get("VERIFIED_RUN_COMMANDS_FILE", str(build_root / "verified-runs" / current_verified_run_id(connector_root) / "verified-commands.json")))),
                "--rewrite-manifest",
            ),
            requires_runtime=True,
            requires_full_matrix=True,
        ),
        ReportSpec(
            name="verified_runtime_mismatch_analysis",
            owner="connector",
            generator="ci/generate-verified-runtime-mismatch-analysis.py",
            make_target="generate-verified-runtime-mismatch-analysis",
            inputs=(
                str(Path(os.environ.get("VERIFIED_RUN_COMMANDS_FILE", str(build_root / "verified-runs" / current_verified_run_id(connector_root) / "verified-commands.json")))),
                str(full_matrix_manifest),
            ),
            outputs=VERIFIED_RUNTIME_MISMATCH_OUTPUTS,
            command=(
                python,
                "ci/generate-verified-runtime-mismatch-analysis.py",
                "--connector-root",
                str(connector_root),
                "--framework-root",
                str(framework_root),
                "--build-root",
                str(build_root),
                "--output-dir",
                str(report_dir / "manifest"),
                "--verified-run-id",
                current_verified_run_id(connector_root),
                "--verified-commands-file",
                str(Path(os.environ.get("VERIFIED_RUN_COMMANDS_FILE", str(build_root / "verified-runs" / current_verified_run_id(connector_root) / "verified-commands.json")))),
            ),
            requires_runtime=True,
        ),
        ReportSpec(
            name="nginx_mrts_http500_cluster_analysis",
            owner="connector",
            generator="ci/generate-nginx-mrts-http500-cluster-analysis.py",
            make_target="generate-nginx-mrts-http500-cluster-analysis",
            inputs=(
                str(Path(os.environ.get("VERIFIED_RUN_COMMANDS_FILE", str(build_root / "verified-runs" / current_verified_run_id(connector_root) / "verified-commands.json")))),
                str(full_matrix_manifest),
                report_relpath("full_matrix_job_completeness", "json"),
                report_relpath("verified_runtime_mismatch_analysis", "json"),
            ),
            outputs=NGINX_MRTS_HTTP500_OUTPUTS,
            command=(
                python,
                "ci/generate-nginx-mrts-http500-cluster-analysis.py",
                "--connector-root",
                str(connector_root),
                "--framework-root",
                str(framework_root),
                "--build-root",
                str(build_root),
                "--output-dir",
                str(report_dir / "manifest"),
                "--verified-run-id",
                current_verified_run_id(connector_root),
            ),
            requires_runtime=True,
            requires_full_matrix=True,
        ),
        ReportSpec(
            name="connector_work_queue",
            owner="connector",
            generator="framework:ci/generate-connector-work-queue.py",
            make_target="generate-work-queue",
            inputs=(report_relpath("full_runtime_matrix", "json"),),
            outputs=CONNECTOR_WORK_QUEUE_OUTPUTS,
            command=(
                python,
                str(framework_root / "ci/generate-connector-work-queue.py"),
                "--connector-root",
                str(connector_root),
                "--framework-root",
                str(framework_root),
                "--output-root",
                str(connector_root),
                "--full-runtime-matrix",
                str(report_path(connector_root, "full_runtime_matrix", "json")),
            ),
            requires_runtime=True,
            requires_full_matrix=True,
        ),
        ReportSpec(
            name="phase_work_queue",
            owner="connector",
            generator="framework:ci/generate-phase-work-queue.py",
            make_target="generate-phase-work-queue",
            inputs=(
                report_relpath("connector_work_queue", "json"),
                report_relpath("phase_coverage", "md"),
                report_relpath("full_runtime_matrix", "json"),
            ),
            outputs=PHASE_WORK_QUEUE_OUTPUTS,
            command=(
                python,
                str(framework_root / "ci/generate-phase-work-queue.py"),
                "--connector-root",
                str(connector_root),
                "--framework-root",
                str(framework_root),
                "--output-root",
                str(connector_root),
                "--connector-work-queue",
                str(report_path(connector_root, "connector_work_queue", "json")),
                "--phase-coverage",
                str(report_path(connector_root, "phase_coverage", "md")),
                "--full-runtime-matrix",
                str(report_path(connector_root, "full_runtime_matrix", "json")),
            ),
            requires_runtime=True,
            requires_full_matrix=True,
        ),
        ReportSpec(
            name="native_mrts_reports",
            owner="connector",
            generator="framework:ci/generate-mrts-native-report.py",
            make_target="mrts-native-full-run",
            inputs=(
                str(native_root / "apache2_ubuntu/job.json"),
                str(native_root / "nginx-pr24/job.json"),
            ),
            outputs=NATIVE_OUTPUTS,
            command=(
                python,
                str(framework_root / "ci/generate-mrts-native-report.py"),
                "--connector-root",
                str(connector_root),
                "--framework-root",
                str(framework_root),
                "--native-root",
                str(native_root),
                "--output-root",
                str(connector_root),
            ),
            requires_native_mrts=True,
            optional=True,
        ),
        ReportSpec(
            name="native_semantics_comparison",
            owner="connector",
            generator="ci/run-native-case-comparison.py",
            make_target="generate-native-semantics-comparison",
            inputs=(
                "ci/run-native-case-comparison.py",
                "ci/native_modsecurity_oracle.c",
                report_relpath("verified_runtime_mismatch_analysis", "json"),
            ),
            outputs=NATIVE_SEMANTICS_OUTPUTS,
            command=(
                python,
                "ci/run-native-case-comparison.py",
                "--connector-root",
                str(connector_root),
                "--framework-root",
                str(framework_root),
                "--build-root",
                str(build_root),
                "--verified-run-root",
                str(verified_run_root),
                "--output-dir",
                str(report_dir / "manifest"),
                "--report-only",
            ),
            requires_runtime=True,
            requires_full_matrix=True,
            optional=True,
        ),
        ReportSpec(
            name="nolog_audit_evidence",
            owner="connector",
            generator="ci/generate-nolog-audit-evidence-analysis.py",
            make_target="generate-nolog-audit-evidence-analysis",
            inputs=(
                report_relpath("connector_work_queue", "json"),
                report_relpath("full_runtime_matrix", "json"),
                report_relpath("phase_coverage", "md"),
            ),
            outputs=NOLOG_OUTPUTS + PHASE_WORK_QUEUE_OUTPUTS,
            command=(
                python,
                "ci/generate-nolog-audit-evidence-analysis.py",
                "--connector-root",
                str(connector_root),
                "--framework-root",
                str(framework_root),
                "--output-dir",
                str(report_dir),
            ),
            requires_runtime=True,
            requires_full_matrix=True,
        ),
        ReportSpec(
            name="response_header_hook_analysis",
            owner="connector",
            generator="ci/generate-response-header-hook-analysis.py",
            make_target="generate-response-header-hook-analysis",
            inputs=(
                report_relpath("connector_work_queue", "json"),
                report_relpath("full_runtime_matrix", "json"),
                report_relpath("phase_coverage", "md"),
            ),
            outputs=RESPONSE_HEADER_OUTPUTS + PHASE_WORK_QUEUE_OUTPUTS,
            command=(
                python,
                "ci/generate-response-header-hook-analysis.py",
                "--connector-root",
                str(connector_root),
                "--framework-root",
                str(framework_root),
                "--output-dir",
                str(report_dir),
            ),
            requires_runtime=True,
            requires_full_matrix=True,
        ),
        ReportSpec(
            name="phase4_hard_abort_capability",
            owner="connector",
            generator="ci/generate-phase4-hard-abort-capability.py",
            make_target="generate-phase4-hard-abort-capability",
            inputs=(
                report_relpath("connector_work_queue", "json"),
                report_relpath("full_runtime_matrix", "json"),
                report_relpath("mrts_native_apache", "json"),
                report_relpath("mrts_native_nginx", "json"),
            ),
            outputs=PHASE4_OUTPUTS + PHASE_WORK_QUEUE_OUTPUTS,
            command=(
                python,
                "ci/generate-phase4-hard-abort-capability.py",
                "--connector-root",
                str(connector_root),
                "--output-dir",
                str(report_dir),
            ),
            requires_runtime=True,
            requires_full_matrix=True,
        ),
        ReportSpec(
            name="remaining_failure_analysis",
            owner="connector",
            generator="ci/generate-remaining-failure-analysis.py",
            make_target="generate-remaining-failure-analysis",
            inputs=(
                report_relpath("full_runtime_matrix", "json"),
                report_relpath("connector_work_queue", "json"),
                report_relpath("phase_work_queue", "json"),
                report_relpath("mrts_native_summary", "json"),
            ),
            outputs=REMAINING_OUTPUTS + FULL_RUN_EVIDENCE_OUTPUTS,
            command=(
                python,
                "ci/generate-remaining-failure-analysis.py",
                "--connector-root",
                str(connector_root),
                "--output-dir",
                str(report_dir),
            ),
            requires_runtime=True,
            requires_full_matrix=True,
        ),
        ReportSpec(
            name="intervention_blocking_analysis",
            owner="connector",
            generator="ci/generate-intervention-blocking-analysis.py",
            make_target="generate-intervention-blocking-analysis",
            inputs=(
                report_relpath("connector_work_queue", "json"),
                report_relpath("full_runtime_matrix", "json"),
                report_relpath("remaining_failure_analysis", "json"),
                report_relpath("phase_work_queue", "json"),
                report_relpath("next_fix_plan", "json"),
            ),
            outputs=INTERVENTION_BLOCKING_OUTPUTS,
            command=(
                python,
                "ci/generate-intervention-blocking-analysis.py",
                "--connector-root",
                str(connector_root),
                "--framework-root",
                str(framework_root),
                "--output-dir",
                str(report_dir),
            ),
            requires_runtime=True,
            requires_full_matrix=True,
        ),
        ReportSpec(
            name="no_mrts_intervention_nomatch_analysis",
            owner="connector",
            generator="ci/generate-no-mrts-intervention-nomatch-analysis.py",
            make_target="generate-no-mrts-intervention-nomatch-analysis",
            inputs=(
                report_relpath("intervention_blocking_analysis", "json"),
                report_relpath("full_runtime_matrix", "json"),
                report_relpath("remaining_failure_analysis", "json"),
                report_relpath("next_fix_plan", "json"),
            ),
            outputs=NO_MRTS_NOMATCH_OUTPUTS,
            command=(
                python,
                "ci/generate-no-mrts-intervention-nomatch-analysis.py",
                "--connector-root",
                str(connector_root),
                "--framework-root",
                str(framework_root),
                "--output-dir",
                str(report_dir),
            ),
            requires_runtime=True,
            requires_full_matrix=True,
        ),
        ReportSpec(
            name="body_processor_analysis",
            owner="connector",
            generator="ci/generate-body-processor-analysis.py",
            make_target="generate-body-processor-analysis",
            inputs=(
                report_relpath("connector_work_queue", "json"),
                report_relpath("remaining_failure_analysis", "json"),
                report_relpath("phase_work_queue", "json"),
                report_relpath("next_fix_plan", "json"),
            ),
            outputs=BODY_PROCESSOR_OUTPUTS,
            command=(
                python,
                "ci/generate-body-processor-analysis.py",
                "--connector-root",
                str(connector_root),
                "--framework-root",
                str(framework_root),
                "--output-dir",
                str(report_dir),
            ),
            requires_runtime=True,
            requires_full_matrix=True,
        ),
        ReportSpec(
            name="rule_chain_semantics_analysis",
            owner="connector",
            generator="ci/generate-rule-chain-semantics-analysis.py",
            make_target="generate-rule-chain-semantics-analysis",
            inputs=(
                report_relpath("connector_work_queue", "json"),
                report_relpath("remaining_failure_analysis", "json"),
                report_relpath("next_fix_plan", "json"),
                report_relpath("full_runtime_matrix", "json"),
            ),
            outputs=RULE_CHAIN_OUTPUTS,
            command=(
                python,
                "ci/generate-rule-chain-semantics-analysis.py",
                "--connector-root",
                str(connector_root),
                "--framework-root",
                str(framework_root),
                "--output-dir",
                str(report_dir),
            ),
            requires_runtime=True,
            requires_full_matrix=True,
        ),
        ReportSpec(
            name="final_consistency_audit",
            owner="connector",
            generator="ci/generate-final-consistency-audit.py",
            make_target="generate-final-consistency-audit",
            inputs=(
                report_relpath("full_runtime_matrix", "json"),
                report_relpath("connector_work_queue", "json"),
                report_relpath("phase_work_queue", "json"),
                report_relpath("remaining_failure_analysis", "json"),
                report_relpath("next_fix_plan", "json"),
                report_relpath("full_run_evidence", "json"),
                report_relpath("mrts_native_summary", "json"),
                report_relpath("phase4_hard_abort_capability", "json"),
                report_relpath("nolog_audit_evidence", "json"),
                report_relpath("response_header_hook_analysis", "json"),
                report_relpath("body_processor_analysis", "json"),
                report_relpath("intervention_blocking_analysis", "json"),
                report_relpath("no_mrts_intervention_nomatch_analysis", "json"),
                report_relpath("rule_chain_semantics_analysis", "json"),
            ),
            outputs=FINAL_CONSISTENCY_OUTPUTS,
            command=(
                python,
                "ci/generate-final-consistency-audit.py",
                "--connector-root",
                str(connector_root),
                "--framework-root",
                str(framework_root),
                "--output-dir",
                str(report_dir),
            ),
            requires_runtime=True,
            requires_full_matrix=True,
        ),
        ReportSpec(
            name="runtime_cache_reports",
            owner="cache",
            generator="ci/update-runtime-reports.py",
            make_target="prepare-runtime-components",
            inputs=(
                str(component_cache_root / "manifest.json"),
                str(component_cache_root / "runtime-build-cache.json"),
            ),
            outputs=RUNTIME_CACHE_OUTPUTS,
            command=(
                python,
                "ci/update-runtime-reports.py",
                "--connector-root",
                str(connector_root),
                "--cache-root",
                str(component_cache_root),
            ),
            requires_runtime=True,
            optional=True,
        ),
    ]


def resolve_input(raw: str, connector_root: Path, framework_root: Path, build_root: Path) -> Path:
    return resolve_input_reference(raw, connector_root, framework_root, build_root)


def resolve_output(raw: str, connector_root: Path) -> Path:
    path = Path(raw)
    return path if path.is_absolute() else connector_root / path


SPEC_PRIMARY_OUTPUT_KEYS: dict[str, set[str]] = {
    "connector_coverage_reports": {
        "apache_runtime_results",
        "case_matrix",
        "connector_gap_summary",
        "coverage_summary",
        "haproxy_runtime_results",
        "nginx_runtime_results",
        "phase_coverage",
        "runtime_matrix",
        "xfail_summary",
    },
    "native_mrts_reports": {"mrts_native_full", "mrts_native_apache", "mrts_native_nginx", "mrts_native_summary"},
    "remaining_failure_analysis": {"remaining_failure_analysis", "next_fix_plan", "full_run_evidence"},
    "final_consistency_audit": {"final_consistency_audit"},
    "runtime_cache_reports": {"runtime_component_cache", "runtime_build_cache"},
}


def primary_output_paths(spec: ReportSpec, output_paths: list[Path]) -> list[Path]:
    allowed = SPEC_PRIMARY_OUTPUT_KEYS.get(spec.name)
    if allowed is None and spec.name in GENERATED_REPORTS:
        allowed = {spec.name}
    if allowed is None:
        return output_paths
    return [path for path in output_paths if FILENAME_TO_KEY.get(path.name) in allowed]


def placeholder_markdown(key: str, status: str, reason: str, spec: ReportSpec) -> str:
    title = GENERATED_REPORTS[key].purpose
    command = " ".join(spec.command)
    return "\n".join(
        [
            f"# {title}",
            "",
            f"Status: `{status}`",
            "",
            f"Reason: {reason}",
            "",
            "## Verified Command",
            "",
            "| Command | Status | Return Code | Notes |",
            "|---|---|---:|---|",
            f"| `{md(command)}` | {status} | - | {md(reason)} |",
            "",
            "## Rows",
            "",
            "_No rows available. Reason: producer command was not run or verified input is unavailable._",
        ]
    ) + "\n"


def write_placeholder_outputs(
    spec: ReportSpec,
    status: str,
    reason: str,
    output_paths: list[Path],
    connector_root: Path,
    framework_root: Path,
    generated_at: str,
) -> None:
    for path in primary_output_paths(spec, output_paths):
        key = FILENAME_TO_KEY.get(path.name)
        if not key:
            continue
        report = GENERATED_REPORTS[key]
        metadata = build_metadata(
            generated_by=report.generator,
            make_target=report.make_target,
            connector_root=connector_root,
            framework_root=framework_root,
            inputs=spec.inputs,
            generated_at=generated_at,
            report_key=key,
            extra={"run_status": status, "blocked_reason": reason},
        )
        payload = {
            "status": status,
            "reason": reason,
            "report_key": key,
            "report_name": key,
            "generator": spec.generator,
            "make_target": spec.make_target,
            "command": list(spec.command),
            "data_source_policy": DATA_SOURCE_POLICY,
            "verified_run_id": metadata["verified_run_id"],
            "rows": [],
            "empty_reason": "producer command was not run or verified input is unavailable",
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix == ".json":
            path.write_text(generated_json_text(payload, metadata), encoding="utf-8")
        elif path.suffix == ".md":
            path.write_text(generated_markdown_text(placeholder_markdown(key, status, reason, spec), metadata), encoding="utf-8")


def run_spec(
    spec: ReportSpec,
    connector_root: Path,
    framework_root: Path,
    build_root: Path,
    env: dict[str, str],
) -> dict[str, Any]:
    started_at = utc_now()
    started = time.monotonic()
    input_paths = [resolve_input(raw, connector_root, framework_root, build_root) for raw in spec.inputs]
    output_paths = [resolve_output(raw, connector_root) for raw in spec.outputs]
    records = [input_record(raw, connector_root, framework_root, build_root) for raw in spec.inputs]
    missing_inputs = [path for path in input_paths if not path.exists()]
    stale_inputs = [record["path"] for record in records if record.get("status") == "stale"]
    blocked_inputs = [
        record["path"]
        for record in records
        if str(record.get("status", "")) in {"blocked", "failed", "interrupted"}
        or str(record.get("status", "")).startswith("blocked")
        or str(record.get("status", "")).startswith("skipped")
    ]
    empty_inputs = [record["path"] for record in records if record.get("status") == "empty"]
    unknown_inputs = [record["path"] for record in records if record.get("status") == "unknown"]
    raw_stale_inputs = stale_runtime_raw_inputs(spec, input_paths, env)
    stale_inputs.extend(raw_stale_inputs)
    producer_block_status, producer_block_reason = full_matrix_producer_block(spec, env)
    skip_status = ""
    blocked_reason = ""
    if producer_block_status:
        skip_status = producer_block_status
        blocked_reason = producer_block_reason
    elif blocked_inputs:
        skip_status = "blocked"
        blocked_reason = "required generated input is blocked"
    elif missing_inputs or empty_inputs:
        skip_status = "skipped_missing_input"
        blocked_reason = "required input missing or empty"
    elif stale_inputs:
        skip_status = "skipped_stale_input"
        blocked_reason = "required generated input is stale"
    elif unknown_inputs:
        skip_status = "blocked"
        blocked_reason = "required input status is unknown"
    if skip_status:
        finished_at = utc_now()
        print(
            f"refresh-connector-reports: {skip_status.upper()} {spec.name}: {blocked_reason}"
        )
        write_placeholder_outputs(spec, skip_status, blocked_reason, output_paths, connector_root, framework_root, finished_at)
        record = report_record(spec, skip_status, input_paths, output_paths, connector_root, framework_root, build_root, missing_inputs)
        record.update(
            {
                "started_at": started_at,
                "finished_at": finished_at,
                "duration_seconds": round(time.monotonic() - started, 3),
                "return_code": 0,
                "command": list(spec.command),
                "blocked_reason": blocked_reason,
                "blocked_inputs": blocked_inputs,
            }
        )
        return record

    command_env = dict(env)
    if spec.name != "remaining_failure_analysis":
        command_env["SUPPRESS_FULL_RUN_EVIDENCE_SIDE_EFFECTS"] = "1"
    rc, _output, log_info = run_command(list(spec.command), connector_root, command_env)
    finished_at = utc_now()
    missing_outputs = [path for path in output_paths if not path.is_file()]
    if rc == 77:
        status = "blocked"
    elif rc != 0 or missing_outputs:
        status = "failed"
    else:
        status = "generated"
    if status in {"failed", "blocked"}:
        reason = f"generator returned {rc}" if rc != 0 else "generator did not produce all expected outputs"
        write_placeholder_outputs(spec, status, reason, output_paths, connector_root, framework_root, finished_at)
        missing_outputs = [path for path in output_paths if not path.is_file()]
    record = report_record(spec, status, input_paths, output_paths, connector_root, framework_root, build_root, missing_inputs)
    record.update(
        {
            "started_at": started_at,
            "finished_at": finished_at,
            "duration_seconds": round(time.monotonic() - started, 3),
            "return_code": rc,
            "command": list(spec.command),
            "log_path": log_info.get("log_path"),
            "log_hash": log_info.get("log_hash") or log_info.get("output_sha256"),
            "output_sha256": log_info.get("output_sha256"),
        }
    )
    if missing_outputs:
        record["missing_outputs"] = [
            display_path(path, connector_root, framework_root, build_root) for path in missing_outputs
        ]
    return record


def stale_runtime_raw_inputs(spec: ReportSpec, input_paths: list[Path], env: dict[str, str]) -> list[str]:
    if spec.name not in {"full_runtime_matrix", "native_mrts_reports"}:
        return []
    started_at = env.get("VERIFIED_RUN_STARTED_AT", "")
    if not started_at:
        return []
    try:
        start_ts = datetime.fromisoformat(started_at.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return []
    stale: list[str] = []
    for path in input_paths:
        if not path.exists():
            continue
        try:
            if path.stat().st_mtime < start_ts:
                stale.append(str(path))
        except OSError:
            stale.append(str(path))
    return stale


def report_record(
    spec: ReportSpec,
    status: str,
    input_paths: list[Path],
    output_paths: list[Path],
    connector_root: Path,
    framework_root: Path,
    build_root: Path,
    missing_inputs: list[Path],
) -> dict[str, Any]:
    records = [input_record(raw, connector_root, framework_root, build_root) for raw in spec.inputs]
    missing = [record["path"] for record in records if record["status"] == "missing"]
    empty = [record["path"] for record in records if record["status"] == "empty"]
    unknown = [record["path"] for record in records if record["status"] == "unknown"]
    stale = [record["path"] for record in records if record["status"] == "stale"]
    blocked = [
        record["path"]
        for record in records
        if str(record.get("status", "")) in {"blocked", "failed", "interrupted"}
        or str(record.get("status", "")).startswith("blocked")
        or str(record.get("status", "")).startswith("skipped")
    ]
    primary_key = spec.name if spec.name in GENERATED_REPORTS else ""
    category = GENERATED_REPORTS[primary_key].category if primary_key else "mixed"
    kind = GENERATED_REPORTS[primary_key].kind if primary_key else "mixed"
    registry = registry_record(primary_key) if primary_key else {}
    freshness = freshness_status(status, input_paths, output_paths)
    if stale:
        freshness["freshness_status"] = "stale"
    return {
        "report_name": spec.name,
        "verified_run_id": current_verified_run_id(connector_root),
        "data_source_policy": DATA_SOURCE_POLICY,
        "category": category,
        "kind": kind,
        "path": ", ".join(display_path(path, connector_root, framework_root, build_root) for path in output_paths),
        "owner": spec.owner,
        "severity": registry.get("severity", "informational"),
        "data_origin": registry.get("data_origin", "connector"),
        "data_kind": registry.get("data_kind", kind),
        "commit_policy": registry.get("commit_policy", "versioned-generated"),
        "generator": spec.generator,
        "make_target": spec.make_target,
        "status": status,
        "input_status": input_status_summary(records),
        "inputs": records,
        "input_files": [record["path"] for record in records],
        "output_files": [display_path(path, connector_root, framework_root, build_root) for path in output_paths],
        "generated_at": next((generated_at_from_report(path) for path in output_paths if path.is_file()), "-"),
        "missing_inputs": missing,
        "empty_inputs": empty,
        "unknown_inputs": unknown,
        "stale_inputs": stale,
        "blocked_inputs": blocked,
        "missing_outputs": [],
        "input_fingerprint": combined_fingerprint(input_paths),
        "output_fingerprint": combined_fingerprint(output_paths),
        **freshness,
        "requires_runtime": spec.requires_runtime,
        "requires_native_mrts": spec.requires_native_mrts,
        "requires_full_matrix": spec.requires_full_matrix,
        "optional": spec.optional,
    }


def freshness_status(status: str, input_paths: list[Path], output_paths: list[Path]) -> dict[str, Any]:
    input_mtimes = [mtime for mtime in (path_mtime(path) for path in input_paths) if mtime is not None]
    output_mtimes = [mtime for mtime in (path_mtime(path) for path in output_paths) if mtime is not None]
    missing_inputs = [str(path) for path in input_paths if not path.exists()]
    missing_outputs = [str(path) for path in output_paths if not path.exists()]
    newest_input = max(input_mtimes) if input_mtimes else None
    newest_output = max(output_mtimes) if output_mtimes else None
    input_newer = bool(newest_input and newest_output and newest_input > newest_output)
    if status == "failed":
        freshness = "failed"
    elif status.startswith("skipped"):
        freshness = "skipped"
    elif missing_outputs:
        freshness = "missing-output"
    elif missing_inputs:
        freshness = "missing-input"
    elif input_newer:
        freshness = "input-newer-than-output"
    elif output_mtimes:
        freshness = "fresh"
    else:
        freshness = "unknown"
    return {
        "freshness_status": freshness,
        "oldest_input_mtime": iso_from_timestamp(min(input_mtimes) if input_mtimes else None),
        "newest_input_mtime": iso_from_timestamp(newest_input),
        "oldest_output_mtime": iso_from_timestamp(min(output_mtimes) if output_mtimes else None),
        "newest_output_mtime": iso_from_timestamp(newest_output),
        "input_newer_than_output": input_newer,
    }


def render_manifest_md(manifest: dict[str, Any]) -> str:
    lines = [
        "# Report Refresh Manifest",
        "",
        f"> Verified run id: `{manifest.get('verified_run_id', 'unknown')}`",
        f"> Data source policy: `{manifest.get('data_source_policy', DATA_SOURCE_POLICY)}`",
        "",
        "## Summary",
        f"- Connector SHA: `{manifest['connector_sha']}`",
        f"- Framework SHA: `{manifest['framework_sha']}`",
        f"- Framework submodule SHA: `{manifest['framework_submodule_sha']}`",
        f"- MRTS SHA: `{manifest['mrts_sha']}`",
        "",
        "## Inputs",
    ]
    for name, value in manifest["inputs"].items():
        lines.append(f"- `{name}`: `{value}`")
    lines.extend(
        [
            "",
            "## Verified Commands",
            "",
            "| Command | Status | Return Code | Duration | Log Hash | Notes |",
            "|---|---|---:|---:|---|---|",
        ]
    )
    commands = manifest.get("verified_commands", [])
    if commands:
        for command in commands:
            raw_command = command.get("command", "-")
            command_text = " ".join(raw_command) if isinstance(raw_command, list) else str(raw_command)
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"`{md(command_text)}`",
                        str(command.get("status", "unknown")),
                        str(command.get("return_code", "-")),
                        str(command.get("duration_seconds", "-")),
                        f"`{command.get('log_hash', 'unknown')}`",
                        md(command.get("notes") or command.get("summary") or "-"),
                    ]
                )
                + " |"
            )
    else:
        lines.append("| `-` | not_run | - | - | `unknown` | No verified command file was supplied. |")
    lines.extend(
        [
            "",
            "## Submodules",
            "| Name | Path | SHA | Branch | Dirty | Status |",
            "|---|---|---|---|---|---|",
        ]
    )
    for item in manifest.get("submodules", []):
        lines.append(
            "| "
            + " | ".join(
                [
                    str(item.get("name", "-")),
                    f"`{item.get('path', '-')}`",
                    f"`{item.get('sha', '-')}`",
                    f"`{item.get('branch', '-')}`",
                    str(item.get("dirty", "-")),
                    str(item.get("status", "-")),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Reports",
            "| Category | Owner | Severity | Report | Generator | Target | Status | Return code | Duration | Freshness | Outputs | Input status | Missing inputs | Missing outputs | Generated at |",
            "|---|---|---|---|---|---|---|---:|---:|---|---|---|---|---|---|",
        ]
    )
    for report in manifest["reports"]:
        missing = ", ".join(report.get("missing_inputs", [])) or "-"
        missing_outputs = ", ".join(report.get("missing_outputs", [])) or "-"
        outputs = "<br>".join(f"`{item}`" for item in report.get("output_files", [])) or "-"
        lines.append(
            "| "
            + " | ".join(
                [
                    report.get("category", "mixed"),
                    report.get("owner", "unknown"),
                    report.get("severity", "unknown"),
                    report["report_name"],
                    report["generator"],
                    report["make_target"],
                    report["status"],
                    str(report.get("return_code", "-")),
                    str(report.get("duration_seconds", "-")),
                    report.get("freshness_status", "unknown"),
                    outputs,
                    report.get("input_status", "unknown"),
                    missing,
                    missing_outputs,
                    report.get("generated_at", "-"),
                ]
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def manifest_inputs(report_dir: Path) -> dict[str, str]:
    native_json = [
        report_path_from_root(report_dir, "mrts_native_full", "json"),
        report_path_from_root(report_dir, "mrts_native_apache", "json"),
        report_path_from_root(report_dir, "mrts_native_nginx", "json"),
        report_path_from_root(report_dir, "mrts_native_summary", "json"),
    ]
    return {
        "full_runtime_matrix": combined_fingerprint([report_path_from_root(report_dir, "full_runtime_matrix", "json")]),
        "native_mrts": combined_fingerprint(native_json),
        "build_cache": combined_fingerprint([report_path_from_root(report_dir, "runtime_build_cache", "json")]),
        "component_cache": combined_fingerprint([report_path_from_root(report_dir, "runtime_component_cache", "json")]),
    }


def md(value: Any) -> str:
    return str(value if value is not None else "-").replace("|", "\\|")


def submodule_report(connector_root: Path, framework_root: Path) -> list[dict[str, str]]:
    sibling = Path("/root/git/ModSecurity-test-Framework")
    mrts_root = framework_root / "tools/MRTS"
    rows = [
        {
            "name": "parent",
            "path": ".",
            "sha": git_sha(connector_root),
            "branch": git_branch(connector_root),
            "dirty": git_dirty_status(connector_root),
            "status": "present",
        },
        {
            "name": "framework_submodule",
            "path": "modules/ModSecurity-test-Framework",
            "sha": git_sha(framework_root),
            "branch": git_branch(framework_root),
            "dirty": git_dirty_status(framework_root),
            "status": "present" if framework_root.exists() else "not_found",
        },
        {
            "name": "mrts_submodule",
            "path": "modules/ModSecurity-test-Framework/tools/MRTS",
            "sha": git_sha(mrts_root),
            "branch": git_branch(mrts_root) if mrts_root.exists() else "not_found",
            "dirty": git_dirty_status(mrts_root) if mrts_root.exists() else "not_found",
            "status": "present" if mrts_root.exists() else "not_found",
        },
        {
            "name": "framework_sibling_checkout",
            "path": str(sibling),
            "sha": git_sha(sibling) if sibling.exists() else "not_found",
            "branch": git_branch(sibling) if sibling.exists() else "not_found",
            "dirty": git_dirty_status(sibling) if sibling.exists() else "not_found",
            "status": "present" if sibling.exists() else "not_found",
        },
    ]
    expected = git_output(["submodule", "status", "--recursive"], connector_root)
    for row in rows:
        row["expected"] = "-"
    for line in expected.splitlines():
        clean = line.strip()
        parts = clean.split()
        if len(parts) >= 2 and parts[1] == "modules/ModSecurity-test-Framework":
            rows[1]["expected"] = parts[0].lstrip("+-")
        if len(parts) >= 2 and parts[1] == "modules/ModSecurity-test-Framework/tools/MRTS":
            rows[2]["expected"] = parts[0].lstrip("+-")
    if sibling.exists() and rows[1]["sha"] != rows[3]["sha"]:
        rows[3]["status"] = "differs"
    return rows


def spec_for_key(key: str, catalog: list[ReportSpec]) -> ReportSpec | None:
    wanted = set(report_outputs(key))
    for spec in catalog:
        if spec.name == key or wanted.intersection(spec.outputs):
            return spec
    return None


def actual_inputs_for_key(key: str, catalog: list[ReportSpec]) -> tuple[str, ...]:
    spec = spec_for_key(key, catalog)
    if spec:
        return spec.inputs
    return GENERATED_REPORTS[key].inputs


def dependency_payload(catalog: list[ReportSpec]) -> dict[str, Any]:
    output_to_key: dict[str, str] = {}
    for key in GENERATED_REPORTS:
        for output in report_outputs(key):
            output_to_key[output] = key
    nodes: list[dict[str, Any]] = []
    edges: set[tuple[str, str]] = set()
    root_inputs: set[str] = set()
    for key in GENERATED_REPORTS:
        inputs = list(actual_inputs_for_key(key, catalog))
        outputs = list(report_outputs(key))
        deps: list[str] = []
        for raw in inputs:
            rewritten = rewrite_generated_relpath(raw)
            dependency = output_to_key.get(rewritten)
            if dependency and dependency != key:
                deps.append(dependency)
                edges.add((dependency, key))
            else:
                root_inputs.add(raw)
        record = registry_record(key)
        record.update({"inputs": inputs, "outputs": outputs, "dependencies": sorted(set(deps))})
        nodes.append(record)
    return {
        "nodes": nodes,
        "edges": [{"from": source, "to": target} for source, target in sorted(edges)],
        "root_inputs": sorted(root_inputs),
        "final_reports": ["final_consistency_audit", "full_run_evidence", "merge_readiness_dashboard"],
    }


def render_dependency_graph_md(payload: dict[str, Any]) -> str:
    lines = [
        "# Report Dependency Graph",
        "",
        "## Mermaid",
        "",
        "```mermaid",
        "flowchart TD",
    ]
    for node in payload["nodes"]:
        lines.append(f'  {node["key"]}["{node["stem"]}"]')
    for edge in payload["edges"]:
        lines.append(f'  {edge["from"]} --> {edge["to"]}')
    lines.extend(["```", "", "## Reports", "", "| Report | Inputs | Outputs | Dependencies |", "|---|---|---|---|"])
    for node in payload["nodes"]:
        lines.append(
            f"| `{node['key']}` | "
            f"{'<br>'.join(f'`{item}`' for item in node.get('inputs', [])) or '-'} | "
            f"{'<br>'.join(f'`{item}`' for item in node.get('outputs', [])) or '-'} | "
            f"{', '.join(f'`{item}`' for item in node.get('dependencies', [])) or '-'} |"
        )
    lines.extend(["", "## Root Inputs", ""])
    lines.extend(f"- `{item}`" for item in payload["root_inputs"])
    lines.extend(["", "## Final Reports", ""])
    lines.extend(f"- `{item}`" for item in payload["final_reports"])
    return "\n".join(lines) + "\n"


def data_lineage_payload(catalog: list[ReportSpec]) -> dict[str, Any]:
    reports: list[dict[str, Any]] = []
    for key in GENERATED_REPORTS:
        record = registry_record(key)
        record["inputs"] = list(actual_inputs_for_key(key, catalog))
        record["outputs"] = list(report_outputs(key))
        record["notes"] = GENERATED_REPORTS[key].purpose
        reports.append(record)
    return {"reports": reports}


def render_data_lineage_md(payload: dict[str, Any]) -> str:
    lines = [
        "# Report Data Lineage",
        "",
        "| Report | Owner | Origin | Kind | Inputs | Outputs | Commit Policy | Notes |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for report in payload["reports"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{report['key']}`",
                    report["owner"],
                    report["data_origin"],
                    report["data_kind"],
                    "<br>".join(f"`{item}`" for item in report.get("inputs", [])) or "-",
                    "<br>".join(f"`{item}`" for item in report.get("outputs", [])) or "-",
                    report["commit_policy"],
                    md(report.get("notes", "-")),
                ]
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def render_freshness_md(payload: dict[str, Any]) -> str:
    lines = [
        "# Report Freshness",
        "",
        "| Report | Status | Generated At | Newest Input | Newest Output | Missing Inputs | Notes |",
        "|---|---|---|---|---|---|---|",
    ]
    for report in payload["reports"]:
        missing = ", ".join(report.get("missing_inputs", [])) or "-"
        notes = report.get("notes") or report.get("status", "-")
        lines.append(
            f"| `{report['report_name']}` | {report.get('freshness_status', 'unknown')} | "
            f"{report.get('generated_at', '-')} | {report.get('newest_input_mtime', '-')} | "
            f"{report.get('newest_output_mtime', '-')} | {md(missing)} | {md(notes)} |"
        )
    return "\n".join(lines) + "\n"


def path_migration_payload(connector_root: Path) -> dict[str, Any]:
    rows = []
    for filename, key in sorted(FILENAME_TO_KEY.items()):
        ext = Path(filename).suffix.removeprefix(".")
        old_path = legacy_report_relpath(key, ext)
        new_path = report_relpath(key, ext)
        flat = connector_root / old_path
        rows.append(
            {
                "old_path": old_path,
                "new_path": new_path,
                "category": GENERATED_REPORTS[key].category,
                "status": "flat-file-present-error" if flat.exists() else "migrated",
            }
        )
    return {"paths": rows}


def render_path_migration_md(payload: dict[str, Any]) -> str:
    lines = [
        "# Report Path Migration",
        "",
        "| Old Path | New Path | Category | Status |",
        "|---|---|---|---|",
    ]
    for row in payload["paths"]:
        lines.append(f"| `{row['old_path']}` | `{row['new_path']}` | {row['category']} | {row['status']} |")
    return "\n".join(lines) + "\n"


def render_generator_runtime_summary_md(reports: list[dict[str, Any]]) -> str:
    lines = [
        "# Generator Runtime Summary",
        "",
        "| Report | Generator | Target | Status | Return Code | Duration | Missing Inputs | Missing Outputs |",
        "|---|---|---|---|---:|---:|---|---|",
    ]
    for report in reports:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{report['report_name']}`",
                    f"`{report['generator']}`",
                    f"`{report['make_target']}`",
                    report.get("status", "unknown"),
                    str(report.get("return_code", "-")),
                    str(report.get("duration_seconds", "-")),
                    md(", ".join(report.get("missing_inputs", [])) or "-"),
                    md(", ".join(report.get("missing_outputs", [])) or "-"),
                ]
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def build_governance_record(
    key: str,
    connector_root: Path,
    framework_root: Path,
    build_root: Path,
    generated_at: str,
    inputs: tuple[str, ...] = (),
) -> dict[str, Any]:
    report = GENERATED_REPORTS[key]
    outputs = [report_path(connector_root, key, ext) for ext in report.formats]
    input_paths = [resolve_input(raw, connector_root, framework_root, build_root) for raw in inputs]
    input_records = [input_record(raw, connector_root, framework_root, build_root) for raw in inputs]
    input_status = input_status_summary(input_records)
    input_fingerprint = combined_fingerprint(input_paths)
    if key == "report_refresh_manifest" and not inputs:
        input_status = "self_generated_no_direct_input"
        input_fingerprint = "self_generated_no_direct_input"
    record = {
        "report_name": key,
        "verified_run_id": current_verified_run_id(connector_root),
        "data_source_policy": DATA_SOURCE_POLICY,
        "category": report.category,
        "kind": report.kind,
        "path": ", ".join(display_path(path, connector_root, framework_root, build_root) for path in outputs),
        "owner": report.owner,
        "severity": report.severity,
        "data_origin": report.data_origin,
        "data_kind": report.data_kind,
        "commit_policy": report.commit_policy,
        "generator": report.generator,
        "make_target": report.make_target,
        "status": "generated" if all(path.is_file() for path in outputs) else "missing-output",
        "input_status": input_status,
        "inputs": input_records,
        "input_files": list(inputs),
        "output_files": [display_path(path, connector_root, framework_root, build_root) for path in outputs],
        "generated_at": generated_at,
        "missing_inputs": [display_path(path, connector_root, framework_root, build_root) for path in input_paths if not path.exists()],
        "empty_inputs": [],
        "unknown_inputs": [],
        "missing_outputs": [display_path(path, connector_root, framework_root, build_root) for path in outputs if not path.exists()],
        "input_fingerprint": input_fingerprint,
        "output_fingerprint": combined_fingerprint(outputs),
        "started_at": generated_at,
        "finished_at": generated_at,
        "duration_seconds": 0.0,
        "return_code": 0,
        "command": ["internal", report.generator],
        "requires_runtime": report.requires_runtime,
        "requires_native_mrts": report.requires_native_mrts,
        "requires_full_matrix": report.requires_full_matrix,
        "optional": report.optional,
    }
    record.update(freshness_status(record["status"], input_paths, outputs))
    return record


def merge_dashboard_payload(manifest: dict[str, Any], freshness: dict[str, Any], submodules: list[dict[str, str]], connector_root: Path) -> dict[str, Any]:
    full_matrix = read_json(report_path(connector_root, "full_runtime_matrix", "json"))
    final_audit = read_json(report_path(connector_root, "final_consistency_audit", "json"))
    next_plan = read_json(report_path(connector_root, "next_fix_plan", "json"))
    system_proof = read_json(report_path(connector_root, "system_environment_proof", "json"))
    mismatch_analysis = read_json(report_path(connector_root, "verified_runtime_mismatch_analysis", "json"))
    job_completeness = read_json(report_path(connector_root, "full_matrix_job_completeness", "json"))
    nginx_http500 = read_json(report_path(connector_root, "nginx_mrts_http500_cluster_analysis", "json"))
    reports = manifest.get("reports", [])
    failed = [report for report in reports if report.get("status") == "failed" and not report.get("optional")]
    optional_failed = [report for report in reports if report.get("status") == "failed" and report.get("optional")]
    skipped = [
        report
        for report in reports
        if str(report.get("status", "")).startswith("skipped") and not report.get("optional")
    ]
    optional_skipped = [
        report
        for report in reports
        if str(report.get("status", "")).startswith("skipped") and report.get("optional")
    ]
    optional_blocked = [report for report in reports if report.get("status") == "blocked" and report.get("optional")]
    stale = [
        report
        for report in freshness.get("reports", [])
        if report.get("freshness_status") in {"stale", "input-newer-than-output", "missing-output", "missing-input"}
    ]
    dirty = [item for item in submodules if item.get("dirty") == "dirty" or item.get("status") == "differs"]
    verified_run_id = str(manifest.get("verified_run_id") or current_verified_run_id(connector_root))
    critical_reports = [report for report in reports if report.get("severity") == "critical" and not report.get("optional")]
    critical_missing = [report for report in critical_reports if report.get("status") != "generated"]
    critical_stale = [
        report
        for report in critical_reports
        if report.get("freshness_status") in {"stale", "input-newer-than-output", "missing-output", "missing-input"}
        or report.get("input_status") in {"stale", "blocked", "missing", "partial", "unknown"}
        or report.get("stale_inputs")
    ]
    critical_run_mismatches = [
        report.get("report_name", "unknown")
        for report in critical_reports
        if str(report.get("verified_run_id") or "") not in {"", verified_run_id}
    ]
    metadata_verified_run_ids = {
        "full_runtime_matrix": (full_matrix.get("metadata") if isinstance(full_matrix.get("metadata"), dict) else {}).get("verified_run_id"),
        "final_consistency_audit": (final_audit.get("metadata") if isinstance(final_audit.get("metadata"), dict) else {}).get("verified_run_id"),
        "system_environment_proof": (system_proof.get("metadata") if isinstance(system_proof.get("metadata"), dict) else {}).get("verified_run_id"),
        "verified_runtime_mismatch_analysis": (mismatch_analysis.get("metadata") if isinstance(mismatch_analysis.get("metadata"), dict) else {}).get("verified_run_id"),
    }
    metadata_run_mismatches = [
        name for name, run_id in metadata_verified_run_ids.items() if run_id != verified_run_id
    ]
    critical_producer_not_run = [
        report for report in critical_reports if report.get("requires_full_matrix") and report.get("status") != "generated"
    ]
    verified_commands = manifest.get("verified_commands") if isinstance(manifest.get("verified_commands"), list) else []
    refresh_timeout = any(
        command.get("refresh_status") == "refresh_timeout"
        or command.get("overall_status") == "blocked_refresh_timeout"
        or (
            command.get("logical_target") in {"refresh-all-reports", "generate-system-environment-proof"}
            and command.get("classification") == "blocked_timeout"
        )
        for command in verified_commands
        if isinstance(command, dict)
    )
    mismatch_full_matrix = mismatch_analysis.get("full_matrix") if isinstance(mismatch_analysis.get("full_matrix"), dict) else {}
    full_matrix_complete = bool(mismatch_full_matrix.get("complete"))
    full_matrix_timeout = bool(mismatch_full_matrix.get("timeout"))
    full_matrix_completed_jobs = int(mismatch_full_matrix.get("completed_jobs") or job_completeness.get("complete_jobs") or 0)
    full_matrix_expected_jobs = int(mismatch_full_matrix.get("expected_jobs") or job_completeness.get("total_jobs") or 0)
    full_matrix_missing_jobs = (
        mismatch_full_matrix.get("missing_jobs")
        if isinstance(mismatch_full_matrix.get("missing_jobs"), list)
        else job_completeness.get("missing_job_ids")
        if isinstance(job_completeness.get("missing_job_ids"), list)
        else []
    )
    full_matrix_refresh_timeout = bool(mismatch_full_matrix.get("refresh_timeout")) or refresh_timeout
    evidence_scope = str(mismatch_analysis.get("evidence_scope") or "")
    critical_mismatch_count = int(mismatch_analysis.get("critical_mismatch_count") or 0)
    mismatch_count = int(mismatch_analysis.get("mismatch_count") or 0)
    smoke_only = evidence_scope == "smoke-only"
    full_matrix_incomplete = bool(mismatch_analysis) and (smoke_only or not full_matrix_complete)
    primary_blocker = str(nginx_http500.get("primary_blocker") or "")
    if primary_blocker == "none":
        primary_blocker = ""
    if not primary_blocker and full_matrix_complete and critical_mismatch_count > 0:
        primary_blocker = str(
            next_plan.get("recommendation", {}).get("recommended_next_fix_cluster")
            or final_audit.get("recommended_next_fix_cluster", {}).get("value", "unknown")
        )
    core_ok = (
        not failed
        and not skipped
        and not stale
        and not dirty
        and not critical_missing
        and not critical_stale
        and not critical_run_mismatches
        and not metadata_run_mismatches
        and critical_mismatch_count == 0
        and final_audit.get("release_readiness") in {"ready", "ready_with_known_reported_gaps"}
    )
    if full_matrix_incomplete:
        readiness = "UNKNOWN"
    elif failed:
        readiness = "FAIL"
    elif full_matrix_complete and critical_mismatch_count > 0:
        readiness = "FAIL"
    elif critical_producer_not_run:
        readiness = "UNKNOWN"
    elif (
        skipped
        or optional_failed
        or optional_skipped
        or optional_blocked
        or stale
        or dirty
        or critical_missing
        or critical_stale
        or critical_run_mismatches
        or metadata_run_mismatches
    ):
        readiness = "WARN"
    elif core_ok:
        readiness = "PASS"
    else:
        readiness = "UNKNOWN"
    return {
        "status": readiness,
        "verified_run_id": verified_run_id,
        "data_source_policy": DATA_SOURCE_POLICY,
        "generated_at": manifest.get("generated_at"),
        "connector_sha": manifest.get("connector_sha"),
        "framework_sha": manifest.get("framework_sha"),
        "full_matrix_totals": full_matrix.get("totals", {}),
        "full_matrix_complete": full_matrix_complete,
        "full_matrix_completed_jobs": full_matrix_completed_jobs,
        "full_matrix_expected_jobs": full_matrix_expected_jobs,
        "full_matrix_missing_jobs": full_matrix_missing_jobs,
        "full_matrix_timeout": full_matrix_timeout,
        "full_matrix_refresh_timeout": full_matrix_refresh_timeout,
        "evidence_scope": evidence_scope or "unknown",
        "runtime_mismatch_count": mismatch_count,
        "critical_runtime_mismatch_count": critical_mismatch_count,
        "runtime_mismatch_categories": mismatch_analysis.get("by_classification", {}) if isinstance(mismatch_analysis.get("by_classification"), dict) else {},
        "final_consistency_status": final_audit.get("release_readiness", "unknown"),
        "primary_blocker": primary_blocker or "unknown",
        "recommended_next_fix_cluster": next_plan.get("recommendation", {}).get("recommended_next_fix_cluster")
        or final_audit.get("recommended_next_fix_cluster", {}).get("value", "unknown"),
        "failed_reports": [report.get("report_name") for report in failed],
        "skipped_reports": [report.get("report_name") for report in skipped],
        "optional_failed_reports": [report.get("report_name") for report in optional_failed],
        "optional_skipped_reports": [report.get("report_name") for report in optional_skipped],
        "optional_blocked_reports": [report.get("report_name") for report in optional_blocked],
        "stale_reports": [report.get("report_name") for report in stale],
        "critical_missing_reports": [report.get("report_name") for report in critical_missing],
        "critical_stale_reports": [report.get("report_name") for report in critical_stale],
        "critical_run_mismatches": critical_run_mismatches,
        "metadata_run_mismatches": metadata_run_mismatches,
        "metadata_verified_run_ids": metadata_verified_run_ids,
        "critical_producer_not_run": [report.get("report_name") for report in critical_producer_not_run],
        "dirty_submodules": dirty,
        "submodules": submodules,
        "reason": (
            "Smoke-only evidence is not a full verified matrix run; merge readiness remains UNKNOWN."
            if smoke_only
            else (
                "Full-Matrix evidence is incomplete; "
                f"{full_matrix_completed_jobs}/{full_matrix_expected_jobs} jobs complete; "
                f"missing jobs: {', '.join(str(item) for item in full_matrix_missing_jobs) or 'unknown'}."
            )
            if full_matrix_incomplete
            else "Failed generator records block merge readiness."
            if failed
            else "Full-Matrix runtime completed with critical mismatches; downstream report refresh timed out."
            if full_matrix_complete and critical_mismatch_count > 0 and full_matrix_refresh_timeout
            else "Full-Matrix runtime completed with critical mismatches; downstream reports remain blocked, stale, or unknown."
            if full_matrix_complete and critical_mismatch_count > 0 and (full_matrix_refresh_timeout or stale or critical_stale)
            else "Full-Matrix completed and critical runtime mismatches are present."
            if full_matrix_complete and critical_mismatch_count > 0
            else "Critical producer evidence was not generated in this verified run."
            if readiness == "UNKNOWN"
            else "Optional producer evidence is unavailable; required critical inputs are tracked separately."
            if optional_failed or optional_skipped or optional_blocked
            else "Core canonical reports are generated; warning conditions are documented."
            if readiness == "WARN"
            else "Core canonical reports are generated and no warning conditions were found."
            if readiness == "PASS"
            else "Merge readiness could not be determined from available reports."
        ),
    }


def render_merge_dashboard_md(payload: dict[str, Any]) -> str:
    totals = payload.get("full_matrix_totals", {})
    checks = [
        (
            "Full Runtime Matrix",
            "PASS" if payload.get("full_matrix_complete") else "UNKNOWN",
            f"complete={payload.get('full_matrix_complete', False)} jobs={payload.get('full_matrix_completed_jobs', 0)}/{payload.get('full_matrix_expected_jobs', 0)} missing={payload.get('full_matrix_missing_jobs', [])} runtime_timeout={payload.get('full_matrix_timeout', False)} refresh_timeout={payload.get('full_matrix_refresh_timeout', False)} PASS={totals.get('pass', '-')} FAIL={totals.get('fail', '-')} BLOCKED={totals.get('blocked', '-')}",
        ),
        (
            "Runtime Mismatch Analysis",
            "UNKNOWN"
            if not payload.get("full_matrix_complete")
            else "FAIL"
            if payload.get("critical_runtime_mismatch_count")
            else "PASS",
            f"mismatches={payload.get('runtime_mismatch_count', 0)} critical={payload.get('critical_runtime_mismatch_count', 0)} categories={payload.get('runtime_mismatch_categories', {})}",
        ),
        ("Final Consistency Audit", "PASS" if payload.get("final_consistency_status") else "UNKNOWN", payload.get("final_consistency_status", "unknown")),
        ("Missing Inputs / Skipped Reports", "WARN" if payload.get("skipped_reports") else "PASS", ", ".join(payload.get("skipped_reports", [])) or "none"),
        ("Optional Producer Evidence", "WARN" if payload.get("optional_failed_reports") or payload.get("optional_skipped_reports") or payload.get("optional_blocked_reports") else "PASS", ", ".join(payload.get("optional_failed_reports", []) + payload.get("optional_skipped_reports", []) + payload.get("optional_blocked_reports", [])) or "available/not required"),
        ("Stale Reports", "WARN" if payload.get("stale_reports") else "PASS", ", ".join(payload.get("stale_reports", [])) or "none"),
        ("Report Refresh", "WARN" if payload.get("full_matrix_refresh_timeout") else "PASS", "refresh timeout after runtime completed" if payload.get("full_matrix_refresh_timeout") else "completed/no timeout recorded"),
        ("Critical Input Freshness", "WARN" if payload.get("critical_stale_reports") else "PASS", ", ".join(payload.get("critical_stale_reports", [])) or "fresh"),
        (
            "Verified Run Consistency",
            "WARN" if payload.get("critical_run_mismatches") or payload.get("metadata_run_mismatches") else "PASS",
            ", ".join(payload.get("critical_run_mismatches", []) + payload.get("metadata_run_mismatches", [])) or "consistent",
        ),
        ("Failed Generators", "FAIL" if payload.get("failed_reports") else "PASS", ", ".join(payload.get("failed_reports", [])) or "none"),
        ("Submodule Status", "WARN" if payload.get("dirty_submodules") else "PASS", ", ".join(item.get("name", "-") for item in payload.get("dirty_submodules", [])) or "clean/no mismatch"),
    ]
    lines = [
        "# Merge Readiness Dashboard",
        "",
        f"Merge Readiness: `{payload.get('status', 'UNKNOWN')}`",
        "",
        "## Summary",
        "",
        "| Check | Status | Notes |",
        "|---|---|---|",
    ]
    for name, status, notes in checks:
        lines.append(f"| {name} | {status} | {md(notes)} |")
    lines.extend(
        [
            "",
            "## Decision",
            "",
            f"Merge readiness: `{payload.get('status', 'UNKNOWN')}`",
            "",
            f"Reason: {payload.get('reason', 'unknown')}",
            "",
            "## Evidence",
            "",
            f"- Verified run id: `{payload.get('verified_run_id', 'unknown')}`",
            f"- Connector SHA: `{payload.get('connector_sha', 'unknown')}`",
            f"- Framework SHA: `{payload.get('framework_sha', 'unknown')}`",
            f"- Primary blocker: `{payload.get('primary_blocker', 'unknown')}`",
            f"- Recommended next fix cluster: `{payload.get('recommended_next_fix_cluster', 'unknown')}`",
            f"- Evidence scope: `{payload.get('evidence_scope', 'unknown')}`",
            f"- Full-Matrix complete: `{payload.get('full_matrix_complete', False)}`",
            f"- Full-Matrix completeness: `{payload.get('full_matrix_completed_jobs', 0)}` / `{payload.get('full_matrix_expected_jobs', 0)}`",
            f"- Missing Full-Matrix jobs: `{', '.join(str(item) for item in payload.get('full_matrix_missing_jobs', [])) or '-'}`",
            f"- Full-Matrix refresh timeout: `{payload.get('full_matrix_refresh_timeout', False)}`",
            f"- Runtime mismatches / critical: `{payload.get('runtime_mismatch_count', 0)}` / `{payload.get('critical_runtime_mismatch_count', 0)}`",
            f"- Full-Matrix PASS/FAIL/BLOCKED/NOT_EXECUTABLE: `{totals.get('pass', '-')}` / `{totals.get('fail', '-')}` / `{totals.get('blocked', '-')}` / `{totals.get('not_executable', '-')}`",
            "",
            "## Submodules",
            "",
            "| Name | Path | SHA | Branch | Dirty | Status |",
            "|---|---|---|---|---|---|",
        ]
    )
    for item in payload.get("submodules", []):
        lines.append(
            f"| {item.get('name', '-')} | `{item.get('path', '-')}` | `{item.get('sha', '-')}` | `{item.get('branch', '-')}` | {item.get('dirty', '-')} | {item.get('status', '-')} |"
        )
    return "\n".join(lines) + "\n"


def report_record_for_output(manifest: dict[str, Any], output_path: str) -> dict[str, Any]:
    for report in manifest.get("reports", []):
        if output_path in report.get("output_files", []):
            return report
    return {}


def render_report_index_md(manifest: dict[str, Any]) -> str:
    lines = [
        "# Testing Reports",
        "",
        "This index is refreshed by `make refresh-connector-reports`. Generated reports live under",
        "`reports/testing/generated/<category>/`; do not edit generated report files manually.",
        "",
        "## Verified Run Phases",
        "",
        "Runtime-producing commands and report refresh are intentionally separated. Runtime evidence remains valid",
        "when a later report refresh times out or downstream focused reports are stale.",
        "",
        "```sh",
        "make verified-runtime-producers",
        "make verified-report-refresh",
        "make verified-report-checks",
        "```",
        "",
        "For long full-matrix runs:",
        "",
        "```sh",
        "export VERIFIED_RUN_FULL_MATRIX_RUNTIME_TIMEOUT_SECONDS=7200",
        "export VERIFIED_RUN_REPORT_REFRESH_TIMEOUT_SECONDS=1800",
        "make verified-report-run",
        "```",
        "",
        "Compatibility: `VERIFIED_RUN_FULL_MATRIX_TIMEOUT_SECONDS` is still accepted as an alias for",
        "`VERIFIED_RUN_FULL_MATRIX_RUNTIME_TIMEOUT_SECONDS`.",
        "",
        "## Generated Report Index",
        "",
        "| Category | Owner | Severity | Report file | Purpose | Generator | Make target | Inputs | Output path | Last generated | Kind |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for key, report in sorted(GENERATED_REPORTS.items(), key=lambda item: (item[1].category, item[1].stem)):
        for ext in report.formats:
            output_path = report_relpath(key, ext)
            record = report_record_for_output(manifest, output_path)
            inputs = "<br>".join(f"`{item}`" for item in record.get("input_files", report.inputs)) or "`-`"
            generated_at = record.get("generated_at", "-") if record else "-"
            link = output_path.removeprefix("reports/testing/")
            lines.append(
                "| "
                + " | ".join(
                    [
                        report.category,
                        report.owner,
                        report.severity,
                        f"[{Path(output_path).name}](./{link})",
                        report.purpose.replace("|", "\\|"),
                        report.generator,
                        report.make_target,
                        inputs,
                        f"`{output_path}`",
                        generated_at,
                        report.kind,
                    ]
                )
                + " |"
            )
    lines.extend(
        [
            "",
            "## Migration Notes",
            "",
            "- The previous flat `reports/testing/generated/*.generated.*` layout is deprecated.",
            "- Generator code writes category paths directly; refresh removes stale flat generated report files.",
            "- Runtime caches and native MRTS evidence are regenerated by their generator targets when local inputs are available.",
        ]
    )
    return "\n".join(lines) + "\n"


def cleanup_legacy_flat_reports(connector_root: Path) -> list[str]:
    removed: list[str] = []
    report_dir = connector_root / REPORT_DIR
    for filename in sorted(FILENAME_TO_KEY):
        path = report_dir / filename
        if not path.is_file():
            continue
        path.unlink()
        removed.append(str(path.relative_to(connector_root)))
    return removed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector-root", default=".")
    parser.add_argument("--framework-root", default=None)
    parser.add_argument("--build-root", default=os.environ.get("BUILD_ROOT"))
    parser.add_argument("--native-root", default=os.environ.get("MRTS_NATIVE_ROOT"))
    parser.add_argument("--strict-inputs", action="store_true")
    args = parser.parse_args()

    connector_root = Path(args.connector_root).resolve()
    framework_root = Path(args.framework_root).resolve() if args.framework_root else connector_root / "modules/ModSecurity-test-Framework"
    from runtime_path_utils import verified_runtime_paths

    default_paths = verified_runtime_paths(os.environ)
    build_root = Path(args.build_root or default_paths["BUILD_ROOT"]).resolve()
    native_root = Path(args.native_root or build_root / "mrts-native").resolve()
    report_dir = connector_root / REPORT_DIR
    report_dir.mkdir(parents=True, exist_ok=True)
    verified_run_id = current_verified_run_id(connector_root)
    os.environ.setdefault("VERIFIED_RUN_ID", verified_run_id)
    python = sys.executable
    env = dict(os.environ)
    env.update(
        {
            "PYTHONDONTWRITEBYTECODE": env.get("PYTHONDONTWRITEBYTECODE", "1"),
            "FRAMEWORK_ROOT": str(framework_root),
            "CONNECTOR_ROOT": str(connector_root),
            "BUILD_ROOT": str(build_root),
            "MRTS_NATIVE_ROOT": str(native_root),
            "VERIFIED_RUN_ID": verified_run_id,
        }
    )

    catalog = make_catalog(connector_root, framework_root, build_root, native_root, python)
    reports: list[dict[str, Any]] = []
    for spec in catalog:
        reports.append(run_spec(spec, connector_root, framework_root, build_root, env))

    submodule_root = connector_root / "modules/ModSecurity-test-Framework"
    mrts_root = framework_root / "tools/MRTS"
    submodules = submodule_report(connector_root, framework_root)
    generated_at = utc_now()
    cyclic_governance_reports = {
        "merge_readiness_dashboard",
        "report_freshness",
        "report_refresh_manifest",
    }

    def record_outputs(records: list[dict[str, Any]], exclude: set[str] | None = None) -> tuple[str, ...]:
        excluded = exclude or set()
        return tuple(
            output
            for record in records
            if str(record.get("report_name") or "") not in excluded
            for output in record.get("output_files", [])
        )

    def write_governance_json_md(key: str, payload: dict[str, Any], markdown: str, inputs: tuple[str, ...] = ()) -> dict[str, Any]:
        metadata = build_metadata(
            generated_by=GENERATED_REPORTS[key].generator,
            make_target=GENERATED_REPORTS[key].make_target,
            connector_root=connector_root,
            framework_root=framework_root,
            inputs=inputs,
            generated_at=generated_at,
            report_key=key,
        )
        json_path = report_path(connector_root, key, "json") if "json" in GENERATED_REPORTS[key].formats else None
        md_path = report_path(connector_root, key, "md") if "md" in GENERATED_REPORTS[key].formats else None
        if json_path is not None:
            json_path.parent.mkdir(parents=True, exist_ok=True)
            json_path.write_text(generated_json_text(payload, metadata), encoding="utf-8")
        if md_path is not None:
            md_path.parent.mkdir(parents=True, exist_ok=True)
            md_path.write_text(generated_markdown_text(markdown, metadata), encoding="utf-8")
        return build_governance_record(key, connector_root, framework_root, build_root, generated_at, inputs)

    dependency = dependency_payload(catalog)
    data_lineage = data_lineage_payload(catalog)
    path_migration = path_migration_payload(connector_root)
    governance_records = [
        write_governance_json_md(
            "report_dependency_graph",
            dependency,
            render_dependency_graph_md(dependency),
            tuple(sorted({item for node in dependency["nodes"] for item in node.get("inputs", [])})),
        ),
        write_governance_json_md(
            "report_data_lineage",
            data_lineage,
            render_data_lineage_md(data_lineage),
            tuple(sorted({item for report in data_lineage["reports"] for item in report.get("inputs", [])})),
        ),
        write_governance_json_md(
            "report_path_migration",
            path_migration,
            render_path_migration_md(path_migration),
        ),
    ]
    runtime_md = render_generator_runtime_summary_md(reports)
    runtime_metadata = build_metadata(
        generated_by=GENERATED_REPORTS["generator_runtime_summary"].generator,
        make_target=GENERATED_REPORTS["generator_runtime_summary"].make_target,
        connector_root=connector_root,
        framework_root=framework_root,
        inputs=record_outputs(reports),
        generated_at=generated_at,
        report_key="generator_runtime_summary",
    )
    runtime_path = report_path(connector_root, "generator_runtime_summary", "md")
    runtime_path.parent.mkdir(parents=True, exist_ok=True)
    runtime_path.write_text(generated_markdown_text(runtime_md, runtime_metadata), encoding="utf-8")
    governance_records.append(build_governance_record("generator_runtime_summary", connector_root, framework_root, build_root, generated_at))

    manifest_record = build_governance_record("report_refresh_manifest", connector_root, framework_root, build_root, generated_at)
    freshness_record_placeholder = build_governance_record("report_freshness", connector_root, framework_root, build_root, generated_at)
    dashboard_record_placeholder = build_governance_record("merge_readiness_dashboard", connector_root, framework_root, build_root, generated_at)
    all_records = reports + governance_records + [freshness_record_placeholder, dashboard_record_placeholder, manifest_record]
    freshness = {"generated_at": generated_at, "reports": all_records}
    freshness_record = write_governance_json_md(
        "report_freshness",
        freshness,
        render_freshness_md(freshness),
        record_outputs(all_records, cyclic_governance_reports),
    )
    all_records = reports + governance_records + [freshness_record, dashboard_record_placeholder, manifest_record]
    manifest = {
        "verified_run_id": verified_run_id,
        "data_source_policy": DATA_SOURCE_POLICY,
        "generated_at": generated_at,
        "connector_sha": git_sha(connector_root),
        "framework_sha": git_sha(framework_root),
        "framework_submodule_sha": git_sha(submodule_root),
        "mrts_sha": git_sha(mrts_root),
        "parent_branch": git_branch(connector_root),
        "parent_dirty": git_dirty_status(connector_root),
        "framework_branch": git_branch(framework_root),
        "framework_dirty": git_dirty_status(framework_root),
        "submodules": submodules,
        "verified_commands": read_verified_commands(env),
        "inputs": manifest_inputs(report_dir),
        "reports": all_records,
    }
    dashboard = merge_dashboard_payload(manifest, freshness, submodules, connector_root)
    dashboard_record = write_governance_json_md(
        "merge_readiness_dashboard",
        dashboard,
        render_merge_dashboard_md(dashboard),
        (
            report_relpath("full_runtime_matrix", "json"),
            report_relpath("verified_runtime_mismatch_analysis", "json"),
            report_relpath("final_consistency_audit", "json"),
            report_relpath("next_fix_plan", "json"),
            report_relpath("full_run_evidence", "json"),
            report_relpath("report_freshness", "json"),
        ),
    )
    manifest["reports"] = reports + governance_records + [freshness_record, dashboard_record, manifest_record]
    freshness = {"generated_at": generated_at, "reports": manifest["reports"]}
    freshness_record = write_governance_json_md(
        "report_freshness",
        freshness,
        render_freshness_md(freshness),
        record_outputs(manifest["reports"], cyclic_governance_reports),
    )
    manifest["reports"] = reports + governance_records + [freshness_record, dashboard_record, manifest_record]
    dashboard = merge_dashboard_payload(manifest, freshness, submodules, connector_root)
    dashboard_record = write_governance_json_md(
        "merge_readiness_dashboard",
        dashboard,
        render_merge_dashboard_md(dashboard),
        (
            report_relpath("full_runtime_matrix", "json"),
            report_relpath("verified_runtime_mismatch_analysis", "json"),
            report_relpath("final_consistency_audit", "json"),
            report_relpath("next_fix_plan", "json"),
            report_relpath("full_run_evidence", "json"),
            report_relpath("report_freshness", "json"),
        ),
    )
    manifest["reports"] = reports + governance_records + [freshness_record, dashboard_record, manifest_record]
    metadata = build_metadata(
        generated_by="ci/refresh-connector-reports.py",
        make_target="refresh-connector-reports",
        connector_root=connector_root,
        framework_root=framework_root,
        inputs=record_outputs(manifest["reports"], {"report_refresh_manifest"}),
        generated_at=manifest["generated_at"],
        report_key="report_refresh_manifest",
        extra={
            "framework_submodule_sha": manifest["framework_submodule_sha"],
            "mrts_sha": manifest["mrts_sha"],
            "submodules": submodules,
        },
    )
    json_path = report_path_from_root(report_dir, "report_refresh_manifest", "json")
    md_path = report_path_from_root(report_dir, "report_refresh_manifest", "md")
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(generated_json_text(manifest, metadata), encoding="utf-8")
    md_path.write_text(generated_markdown_text(render_manifest_md(manifest), metadata), encoding="utf-8")
    (connector_root / "reports/testing/README.md").write_text(render_report_index_md(manifest), encoding="utf-8")
    removed_legacy = cleanup_legacy_flat_reports(connector_root)
    if removed_legacy:
        print("refresh-connector-reports: removed legacy flat reports: " + ", ".join(removed_legacy))
    print(f"refresh-connector-reports: manifest={md_path}")

    failed = [item for item in reports if item["status"] == "failed" and not item.get("optional")]
    skipped_required = [
        item
        for item in reports
        if (str(item["status"]).startswith("skipped") or str(item["status"]).startswith("blocked") or item["status"] == "interrupted") and not item.get("optional")
    ]
    if failed or (args.strict_inputs and skipped_required):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
