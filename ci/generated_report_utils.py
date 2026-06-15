#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


GENERATED_ROOT = Path("reports/testing/generated")
GENERATED_NOTICE = "Generated file - do not edit manually."


@dataclass(frozen=True)
class GeneratedReport:
    key: str
    category: str
    stem: str
    formats: tuple[str, ...]
    purpose: str
    kind: str
    generator: str
    make_target: str
    owner: str = "connector"
    severity: str = "informational"
    data_origin: str = "connector"
    data_kind: str = "report"
    commit_policy: str = "versioned-generated"
    inputs: tuple[str, ...] = ()
    requires_runtime: bool = False
    requires_full_matrix: bool = False
    requires_native_mrts: bool = False
    optional: bool = False

    def filename(self, ext: str) -> str:
        clean_ext = ext.removeprefix(".")
        if clean_ext not in self.formats:
            raise ValueError(f"{self.key} does not produce .{clean_ext}")
        return f"{self.stem}.{clean_ext}"


GENERATED_REPORTS: dict[str, GeneratedReport] = {
    "report_refresh_manifest": GeneratedReport(
        "report_refresh_manifest",
        "manifest",
        "report-refresh-manifest.generated",
        ("json", "md"),
        "Catalog of report generators, outputs, inputs, and refresh status.",
        "canonical",
        "ci/refresh-connector-reports.py",
        "refresh-connector-reports",
        owner="manifest",
        severity="critical",
        data_origin="manifest",
        data_kind="manifest",
    ),
    "report_dependency_graph": GeneratedReport(
        "report_dependency_graph",
        "manifest",
        "report-dependency-graph.generated",
        ("json", "md"),
        "Dependency graph for generated reports and their data flow.",
        "canonical",
        "ci/refresh-connector-reports.py",
        "refresh-connector-reports",
        owner="manifest",
        severity="important",
        data_origin="manifest",
        data_kind="manifest",
    ),
    "report_data_lineage": GeneratedReport(
        "report_data_lineage",
        "manifest",
        "report-data-lineage.generated",
        ("json", "md"),
        "Data-lineage index for generated reports.",
        "canonical",
        "ci/refresh-connector-reports.py",
        "refresh-connector-reports",
        owner="manifest",
        severity="important",
        data_origin="manifest",
        data_kind="manifest",
    ),
    "report_freshness": GeneratedReport(
        "report_freshness",
        "manifest",
        "report-freshness.generated",
        ("json", "md"),
        "Freshness and stale-status report for generated reports.",
        "canonical",
        "ci/refresh-connector-reports.py",
        "refresh-connector-reports",
        owner="manifest",
        severity="important",
        data_origin="manifest",
        data_kind="manifest",
    ),
    "report_path_migration": GeneratedReport(
        "report_path_migration",
        "manifest",
        "report-path-migration.generated",
        ("json", "md"),
        "Old-path to new-path migration table for generated reports.",
        "canonical",
        "ci/refresh-connector-reports.py",
        "refresh-connector-reports",
        owner="manifest",
        severity="important",
        data_origin="manifest",
        data_kind="manifest",
    ),
    "generator_runtime_summary": GeneratedReport(
        "generator_runtime_summary",
        "manifest",
        "generator-runtime-summary.generated",
        ("md",),
        "Generator runtime, return-code, and missing-input summary.",
        "canonical",
        "ci/refresh-connector-reports.py",
        "refresh-connector-reports",
        owner="manifest",
        severity="informational",
        data_origin="manifest",
        data_kind="manifest",
    ),
    "merge_readiness_dashboard": GeneratedReport(
        "merge_readiness_dashboard",
        "manifest",
        "merge-readiness-dashboard.generated",
        ("json", "md"),
        "Top-level merge-readiness dashboard.",
        "canonical",
        "ci/refresh-connector-reports.py",
        "refresh-connector-reports",
        owner="manifest",
        severity="critical",
        data_origin="manifest",
        data_kind="dashboard",
    ),
    "system_environment_proof": GeneratedReport(
        "system_environment_proof",
        "manifest",
        "system-environment-proof.generated",
        ("json", "md"),
        "System, tool-version, git, and check-execution proof.",
        "canonical",
        "ci/generate-system-environment-proof.py",
        "generate-system-environment-proof",
        owner="system",
        severity="important",
        data_origin="external-local",
        data_kind="system-proof",
    ),
    "full_runtime_matrix": GeneratedReport(
        "full_runtime_matrix",
        "canonical",
        "full-runtime-matrix.generated",
        ("json", "md"),
        "Complete connector full-runtime matrix summary.",
        "canonical",
        "ci/generate-full-runtime-matrix.py",
        "generate-full-runtime-matrix",
        severity="critical",
        data_origin="runtime",
        data_kind="matrix",
        requires_runtime=True,
        requires_full_matrix=True,
    ),
    "full_run_evidence": GeneratedReport(
        "full_run_evidence",
        "canonical",
        "full-run-evidence.generated",
        ("json", "md"),
        "Evidence rollup shared by focused analysis and consistency checks.",
        "canonical",
        "ci/generate-remaining-failure-analysis.py",
        "refresh-connector-reports",
        severity="critical",
        data_origin="runtime",
        data_kind="evidence",
        requires_runtime=True,
        requires_full_matrix=True,
    ),
    "final_consistency_audit": GeneratedReport(
        "final_consistency_audit",
        "canonical",
        "final-consistency-audit.generated",
        ("json", "md"),
        "Merge-readiness consistency gate across generated evidence.",
        "canonical",
        "ci/generate-final-consistency-audit.py",
        "generate-final-consistency-audit",
        severity="critical",
        data_origin="connector",
        data_kind="evidence",
        requires_runtime=True,
        requires_full_matrix=True,
    ),
    "remaining_failure_analysis": GeneratedReport(
        "remaining_failure_analysis",
        "canonical",
        "remaining-failure-analysis.generated",
        ("json", "md"),
        "Remaining failure clustering and classification.",
        "canonical",
        "ci/generate-remaining-failure-analysis.py",
        "generate-remaining-failure-analysis",
        severity="important",
        data_origin="runtime",
        data_kind="focused-analysis",
        requires_runtime=True,
        requires_full_matrix=True,
    ),
    "next_fix_plan": GeneratedReport(
        "next_fix_plan",
        "canonical",
        "next-fix-plan.generated",
        ("json", "md"),
        "Current recommended next fix cluster.",
        "canonical",
        "ci/generate-remaining-failure-analysis.py",
        "generate-remaining-failure-analysis",
        severity="important",
        data_origin="runtime",
        data_kind="focused-analysis",
        requires_runtime=True,
        requires_full_matrix=True,
    ),
    "connector_work_queue": GeneratedReport(
        "connector_work_queue",
        "work-queues",
        "connector-work-queue.generated",
        ("json", "md"),
        "Connector-scoped queue and classification state.",
        "focused",
        "framework:ci/generate-connector-work-queue.py",
        "generate-work-queue",
        owner="framework",
        severity="important",
        data_origin="framework",
        data_kind="work-queue",
        requires_runtime=True,
        requires_full_matrix=True,
    ),
    "phase_work_queue": GeneratedReport(
        "phase_work_queue",
        "work-queues",
        "phase-work-queue.generated",
        ("json", "md"),
        "Phase-scoped queue and classification state.",
        "focused",
        "framework:ci/generate-phase-work-queue.py",
        "generate-phase-work-queue",
        owner="framework",
        severity="important",
        data_origin="framework",
        data_kind="work-queue",
        requires_runtime=True,
        requires_full_matrix=True,
    ),
    "case_matrix": GeneratedReport(
        "case_matrix",
        "coverage",
        "case-matrix.generated",
        ("md",),
        "Framework/connector case matrix.",
        "focused",
        "framework:ci/generate-case-matrix.py",
        "generate-test-matrix",
        owner="framework",
        data_origin="framework",
        data_kind="report",
        requires_runtime=True,
    ),
    "connector_gap_summary": GeneratedReport(
        "connector_gap_summary",
        "coverage",
        "connector-gap-summary.generated",
        ("md",),
        "Connector gap summary.",
        "focused",
        "framework:ci/generate-case-matrix.py",
        "generate-test-matrix",
        owner="framework",
        data_origin="framework",
        data_kind="report",
        requires_runtime=True,
    ),
    "coverage_summary": GeneratedReport(
        "coverage_summary",
        "coverage",
        "coverage-summary.generated",
        ("md",),
        "Coverage summary by scope, status, runtime, phase, and variable.",
        "focused",
        "framework:ci/generate-case-matrix.py",
        "generate-test-matrix",
        owner="framework",
        data_origin="framework",
        data_kind="report",
        requires_runtime=True,
    ),
    "phase_coverage": GeneratedReport(
        "phase_coverage",
        "coverage",
        "phase-coverage.generated",
        ("md",),
        "Phase coverage summary.",
        "focused",
        "framework:ci/generate-case-matrix.py",
        "generate-test-matrix",
        owner="framework",
        data_origin="framework",
        data_kind="report",
        requires_runtime=True,
    ),
    "xfail_summary": GeneratedReport(
        "xfail_summary",
        "coverage",
        "xfail-summary.generated",
        ("md",),
        "Expected-failure and import-status summary.",
        "focused",
        "framework:ci/generate-case-matrix.py",
        "generate-test-matrix",
        owner="framework",
        data_origin="framework",
        data_kind="report",
        requires_runtime=True,
    ),
    "body_processor_analysis": GeneratedReport(
        "body_processor_analysis",
        "focused-analysis",
        "body-processor-analysis.generated",
        ("json", "md"),
        "Request-body, multipart, and XML processor classification.",
        "focused",
        "ci/generate-body-processor-analysis.py",
        "generate-body-processor-analysis",
        data_kind="focused-analysis",
        requires_runtime=True,
        requires_full_matrix=True,
    ),
    "intervention_blocking_analysis": GeneratedReport(
        "intervention_blocking_analysis",
        "focused-analysis",
        "intervention-blocking-analysis.generated",
        ("json", "md"),
        "Intervention blocking classification and no-match separation.",
        "focused",
        "ci/generate-intervention-blocking-analysis.py",
        "generate-intervention-blocking-analysis",
        data_kind="focused-analysis",
        requires_runtime=True,
        requires_full_matrix=True,
    ),
    "no_mrts_intervention_nomatch_analysis": GeneratedReport(
        "no_mrts_intervention_nomatch_analysis",
        "focused-analysis",
        "no-mrts-intervention-nomatch-analysis.generated",
        ("json", "md"),
        "Framework-owned no-MRTS no-match semantics.",
        "focused",
        "ci/generate-no-mrts-intervention-nomatch-analysis.py",
        "generate-no-mrts-intervention-nomatch-analysis",
        data_kind="focused-analysis",
        requires_runtime=True,
        requires_full_matrix=True,
    ),
    "nolog_audit_evidence": GeneratedReport(
        "nolog_audit_evidence",
        "focused-analysis",
        "nolog-audit-evidence.generated",
        ("json", "md"),
        "Explicit nolog audit-evidence classification.",
        "focused",
        "ci/generate-nolog-audit-evidence-analysis.py",
        "generate-nolog-audit-evidence-analysis",
        data_kind="focused-analysis",
        requires_runtime=True,
        requires_full_matrix=True,
    ),
    "phase4_hard_abort_capability": GeneratedReport(
        "phase4_hard_abort_capability",
        "focused-analysis",
        "phase4-hard-abort-capability.generated",
        ("json", "md"),
        "Phase 4 hard-abort capability evidence.",
        "focused",
        "ci/generate-phase4-hard-abort-capability.py",
        "generate-phase4-hard-abort-capability",
        data_kind="focused-analysis",
        requires_runtime=True,
        requires_full_matrix=True,
    ),
    "response_header_hook_analysis": GeneratedReport(
        "response_header_hook_analysis",
        "focused-analysis",
        "response-header-hook-analysis.generated",
        ("json", "md"),
        "Response-header hook and backend setup analysis.",
        "focused",
        "ci/generate-response-header-hook-analysis.py",
        "generate-response-header-hook-analysis",
        data_kind="focused-analysis",
        requires_runtime=True,
        requires_full_matrix=True,
    ),
    "rule_chain_semantics_analysis": GeneratedReport(
        "rule_chain_semantics_analysis",
        "focused-analysis",
        "rule-chain-semantics-analysis.generated",
        ("json", "md"),
        "Rule-chain semantics and runtime-fixability analysis.",
        "focused",
        "ci/generate-rule-chain-semantics-analysis.py",
        "generate-rule-chain-semantics-analysis",
        data_kind="focused-analysis",
        requires_runtime=True,
        requires_full_matrix=True,
    ),
    "apache_runtime_results": GeneratedReport(
        "apache_runtime_results",
        "runtime",
        "apache-runtime-results.generated",
        ("md",),
        "Apache runtime result details.",
        "runtime",
        "framework:ci/generate-case-matrix.py",
        "generate-test-matrix",
        owner="runtime",
        data_origin="runtime",
        data_kind="report",
        requires_runtime=True,
    ),
    "nginx_runtime_results": GeneratedReport(
        "nginx_runtime_results",
        "runtime",
        "nginx-runtime-results.generated",
        ("md",),
        "NGINX runtime result details.",
        "runtime",
        "framework:ci/generate-case-matrix.py",
        "generate-test-matrix",
        owner="runtime",
        data_origin="runtime",
        data_kind="report",
        requires_runtime=True,
    ),
    "haproxy_runtime_results": GeneratedReport(
        "haproxy_runtime_results",
        "runtime",
        "haproxy-runtime-results.generated",
        ("md",),
        "HAProxy runtime result details.",
        "runtime",
        "framework:ci/generate-case-matrix.py",
        "generate-test-matrix",
        owner="runtime",
        data_origin="runtime",
        data_kind="report",
        requires_runtime=True,
    ),
    "runtime_matrix": GeneratedReport(
        "runtime_matrix",
        "runtime",
        "runtime-matrix.generated",
        ("md",),
        "Default runtime matrix summary.",
        "runtime",
        "framework:ci/generate-case-matrix.py",
        "generate-test-matrix",
        owner="runtime",
        data_origin="runtime",
        data_kind="matrix",
        requires_runtime=True,
    ),
    "mrts_native_full": GeneratedReport(
        "mrts_native_full",
        "mrts-native",
        "mrts-native-full.generated",
        ("json", "md"),
        "Combined native MRTS infrastructure evidence.",
        "optional",
        "framework:ci/generate-mrts-native-report.py",
        "mrts-native-full-run",
        owner="mrts",
        severity="optional",
        data_origin="mrts",
        data_kind="evidence",
        commit_policy="optional-generated",
        requires_native_mrts=True,
        optional=True,
    ),
    "mrts_native_apache": GeneratedReport(
        "mrts_native_apache",
        "mrts-native",
        "mrts-native-apache.generated",
        ("json", "md"),
        "Apache native MRTS infrastructure evidence.",
        "optional",
        "framework:ci/generate-mrts-native-report.py",
        "mrts-native-full-run",
        owner="mrts",
        severity="optional",
        data_origin="mrts",
        data_kind="evidence",
        commit_policy="optional-generated",
        requires_native_mrts=True,
        optional=True,
    ),
    "mrts_native_nginx": GeneratedReport(
        "mrts_native_nginx",
        "mrts-native",
        "mrts-native-nginx.generated",
        ("json", "md"),
        "NGINX native MRTS infrastructure evidence.",
        "optional",
        "framework:ci/generate-mrts-native-report.py",
        "mrts-native-full-run",
        owner="mrts",
        severity="optional",
        data_origin="mrts",
        data_kind="evidence",
        commit_policy="optional-generated",
        requires_native_mrts=True,
        optional=True,
    ),
    "mrts_native_summary": GeneratedReport(
        "mrts_native_summary",
        "mrts-native",
        "mrts-native-summary.generated",
        ("json", "md"),
        "Native MRTS summary.",
        "optional",
        "framework:ci/generate-mrts-native-report.py",
        "mrts-native-full-run",
        owner="mrts",
        severity="optional",
        data_origin="mrts",
        data_kind="evidence",
        commit_policy="optional-generated",
        requires_native_mrts=True,
        optional=True,
    ),
    "runtime_build_cache": GeneratedReport(
        "runtime_build_cache",
        "cache",
        "runtime-build-cache.generated",
        ("json", "md"),
        "Runtime build-cache report.",
        "cache",
        "ci/prepare-runtime-components.py",
        "prepare-runtime-components",
        owner="cache",
        severity="cache",
        data_origin="cache",
        data_kind="cache",
        commit_policy="local-only",
        requires_runtime=True,
    ),
    "runtime_component_cache": GeneratedReport(
        "runtime_component_cache",
        "cache",
        "runtime-component-cache.generated",
        ("json", "md"),
        "Runtime component-cache report.",
        "cache",
        "ci/prepare-runtime-components.py",
        "prepare-runtime-components",
        owner="cache",
        severity="cache",
        data_origin="cache",
        data_kind="cache",
        commit_policy="local-only",
        requires_runtime=True,
    ),
}

FILENAME_TO_KEY = {
    report.filename(ext): key
    for key, report in GENERATED_REPORTS.items()
    for ext in report.formats
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def git_sha(root: Path | None) -> str:
    if root is None:
        return "unknown"
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


def git_dirty(root: Path | None) -> str:
    if root is None:
        return "unknown"
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "status", "--short"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except Exception:
        return "unknown"
    return "dirty" if result.stdout.strip() else "clean"


def report_key_for_filename(filename: str | Path) -> str:
    name = Path(filename).name
    key = FILENAME_TO_KEY.get(name)
    if not key:
        raise KeyError(f"unknown generated report filename: {name}")
    return key


def generated_root(connector_root: Path) -> Path:
    return connector_root / GENERATED_ROOT


def report_filename(key: str, ext: str) -> str:
    return GENERATED_REPORTS[key].filename(ext)


def report_relpath(key: str, ext: str) -> str:
    report = GENERATED_REPORTS[key]
    return str(GENERATED_ROOT / report.category / report.filename(ext))


def report_path(connector_root: Path, key: str, ext: str) -> Path:
    return connector_root / report_relpath(key, ext)


def report_path_from_root(report_root: Path, key: str, ext: str) -> Path:
    report = GENERATED_REPORTS[key]
    return report_root / report.category / report.filename(ext)


def report_relpath_for_filename(filename: str | Path) -> str:
    key = report_key_for_filename(filename)
    ext = Path(filename).suffix.removeprefix(".")
    return report_relpath(key, ext)


def report_path_for_filename(report_root: Path, filename: str | Path) -> Path:
    key = report_key_for_filename(filename)
    ext = Path(filename).suffix.removeprefix(".")
    return report_path_from_root(report_root, key, ext)


def legacy_report_relpath(key: str, ext: str) -> str:
    return str(GENERATED_ROOT / GENERATED_REPORTS[key].filename(ext))


def legacy_report_path(connector_root: Path, key: str, ext: str) -> Path:
    return connector_root / legacy_report_relpath(key, ext)


def rewrite_generated_relpath(value: str | Path) -> str:
    text = str(value)
    prefix = GENERATED_ROOT.as_posix() + "/"
    if not text.startswith(prefix):
        return text
    rest = text[len(prefix) :]
    if "/" in rest:
        return text
    try:
        return report_relpath_for_filename(rest)
    except KeyError:
        return text


def generated_report_outputs(keys: Iterable[str]) -> tuple[str, ...]:
    outputs: list[str] = []
    for key in keys:
        report = GENERATED_REPORTS[key]
        outputs.extend(report_relpath(key, ext) for ext in report.formats)
    return tuple(outputs)


def report_outputs(key: str) -> tuple[str, ...]:
    report = GENERATED_REPORTS[key]
    return tuple(report_relpath(key, ext) for ext in report.formats)


def registry_record(key: str) -> dict[str, Any]:
    report = GENERATED_REPORTS[key]
    return {
        "key": report.key,
        "category": report.category,
        "owner": report.owner,
        "severity": report.severity,
        "stem": report.stem,
        "formats": list(report.formats),
        "purpose": report.purpose,
        "kind": report.kind,
        "generator": report.generator,
        "make_target": report.make_target,
        "inputs": list(report.inputs),
        "outputs": list(report_outputs(key)),
        "data_origin": report.data_origin,
        "data_kind": report.data_kind,
        "commit_policy": report.commit_policy,
        "runtime_required": report.requires_runtime,
        "full_matrix_required": report.requires_full_matrix,
        "native_mrts_required": report.requires_native_mrts,
        "optional": report.optional,
    }


def infer_report_key(generated_by: str, make_target: str) -> str | None:
    matches = [
        key
        for key, report in GENERATED_REPORTS.items()
        if report.generator == generated_by and report.make_target == make_target
    ]
    if not matches and not generated_by.startswith("framework:"):
        framework_generated_by = f"framework:{generated_by}"
        matches = [
            key
            for key, report in GENERATED_REPORTS.items()
            if report.generator == framework_generated_by and report.make_target == make_target
        ]
    if not matches:
        return None
    severity_order = {"critical": 0, "important": 1, "informational": 2, "optional": 3, "cache": 4, "debug": 5}
    matches.sort(key=lambda key: (severity_order.get(GENERATED_REPORTS[key].severity, 99), key))
    return matches[0]


def display_path(path: Path, connector_root: Path, framework_root: Path | None = None, build_root: Path | None = None) -> str:
    resolved = path.resolve(strict=False)
    roots: list[tuple[Path, str]] = [(connector_root.resolve(strict=False), "")]
    if framework_root is not None:
        roots.append((framework_root.resolve(strict=False), "framework:"))
    if build_root is not None:
        roots.append((build_root.resolve(strict=False), "BUILD_ROOT:"))
    for root, prefix in roots:
        try:
            return prefix + str(resolved.relative_to(root))
        except ValueError:
            continue
    return str(path)


def resolve_input_reference(
    raw: str | Path,
    connector_root: Path,
    framework_root: Path | None = None,
    build_root: Path | None = None,
) -> Path:
    text = str(raw)
    if text.startswith("framework:") and framework_root is not None:
        return framework_root / text.removeprefix("framework:")
    if text.startswith("BUILD_ROOT:") and build_root is not None:
        return build_root / text.removeprefix("BUILD_ROOT:")
    path = Path(text)
    if path.is_absolute():
        return path
    rewritten = rewrite_generated_relpath(text)
    return connector_root / rewritten


def input_record(
    raw: str | Path,
    connector_root: Path,
    framework_root: Path | None = None,
    build_root: Path | None = None,
) -> dict[str, str]:
    try:
        path = resolve_input_reference(raw, connector_root, framework_root, build_root)
    except Exception as exc:
        return {"path": str(raw), "status": "unknown", "notes": f"could not resolve input: {exc}"}
    shown = display_path(path, connector_root, framework_root, build_root)
    if not path.exists():
        return {"path": shown, "status": "missing", "notes": "input file missing"}
    if path.is_file():
        try:
            if path.stat().st_size == 0:
                return {"path": shown, "status": "empty", "notes": "input file exists but is empty"}
        except OSError as exc:
            return {"path": shown, "status": "unknown", "notes": f"could not stat input: {exc}"}
        return {"path": shown, "status": "present", "notes": "input file available"}
    if path.is_dir():
        try:
            if not any(path.iterdir()):
                return {"path": shown, "status": "empty", "notes": "input directory exists but is empty"}
        except OSError as exc:
            return {"path": shown, "status": "unknown", "notes": f"could not inspect input directory: {exc}"}
        return {"path": shown, "status": "present", "notes": "input directory available"}
    return {"path": shown, "status": "unknown", "notes": "input exists but is not a regular file or directory"}


def input_records(
    raw_inputs: Iterable[str | Path],
    connector_root: Path,
    framework_root: Path | None = None,
    build_root: Path | None = None,
) -> list[dict[str, str]]:
    return [input_record(raw, connector_root, framework_root, build_root) for raw in raw_inputs]


def input_status_summary(records: list[dict[str, str]]) -> str:
    if not records:
        return "unknown"
    statuses = [record.get("status", "unknown") for record in records]
    if all(status in {"missing", "empty"} for status in statuses):
        return "missing"
    if any(status in {"missing", "empty", "unknown", "stale"} for status in statuses):
        return "partial"
    return "complete"


def build_metadata(
    *,
    generated_by: str,
    make_target: str,
    connector_root: Path,
    framework_root: Path | None = None,
    inputs: Iterable[str | Path] = (),
    generated_at: str | None = None,
    report_key: str | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    records = input_records(inputs, connector_root, framework_root)
    registry_key = report_key or infer_report_key(generated_by, make_target)
    registry = registry_record(registry_key) if registry_key else {}
    metadata: dict[str, Any] = {
        "generated_notice": GENERATED_NOTICE,
        "generated_at": generated_at or utc_now(),
        "generated_by": generated_by,
        "make_target": make_target,
        "report_key": registry_key or "unknown",
        "category": registry.get("category", "unknown"),
        "owner": registry.get("owner", "unknown"),
        "severity": registry.get("severity", "unknown"),
        "data_origin": registry.get("data_origin", "unknown"),
        "data_kind": registry.get("data_kind", "unknown"),
        "commit_policy": registry.get("commit_policy", "unknown"),
        "connector_sha": git_sha(connector_root),
        "framework_sha": git_sha(framework_root),
        "working_tree_dirty": git_dirty(connector_root),
        "framework_working_tree_dirty": git_dirty(framework_root),
        "input_status": input_status_summary(records),
        "inputs": records,
        "missing_inputs": [record["path"] for record in records if record["status"] == "missing"],
        "empty_inputs": [record["path"] for record in records if record["status"] == "empty"],
        "unknown_inputs": [record["path"] for record in records if record["status"] == "unknown"],
        "schema_version": 1,
    }
    if extra:
        metadata.update(extra)
    return metadata


def attach_metadata(payload: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
    result = dict(payload)
    result["metadata"] = metadata
    result.setdefault("generated_at", metadata["generated_at"])
    return result


def generated_json_text(payload: dict[str, Any], metadata: dict[str, Any]) -> str:
    return json.dumps(attach_metadata(payload, metadata), indent=2, sort_keys=True) + "\n"


def metadata_block(metadata: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"> {GENERATED_NOTICE}",
            ">",
            f"> Generated at: `{metadata.get('generated_at', 'unknown')}`",
            f"> Generator: `{metadata.get('generated_by', 'unknown')}`",
            f"> Make target: `{metadata.get('make_target', 'unknown')}`",
            f"> Owner: `{metadata.get('owner', 'unknown')}`",
            f"> Severity: `{metadata.get('severity', 'unknown')}`",
            f"> Connector SHA: `{metadata.get('connector_sha', 'unknown')}`",
            f"> Framework SHA: `{metadata.get('framework_sha', 'unknown')}`",
            f"> Input status: `{metadata.get('input_status', 'unknown')}`",
        ]
    )


def render_empty_table_note(reason: str) -> str:
    return f"_No rows available. Reason: {reason}_"


def missing_information_section(metadata: dict[str, Any]) -> str:
    lines = [
        "## Data Availability / Missing Information",
        "",
        "| Input | Status | Notes |",
        "|---|---|---|",
    ]
    records = metadata.get("inputs")
    if not isinstance(records, list) or not records:
        lines.append("| `-` | unknown | no input files were declared for this generated report |")
    else:
        for record in records:
            path = str(record.get("path", "-")).replace("|", "\\|")
            status = str(record.get("status", "unknown"))
            notes = str(record.get("notes", "")).replace("|", "\\|") or "-"
            lines.append(f"| `{path}` | {status} | {notes} |")
    return "\n".join(lines)


def generated_markdown_text(markdown: str, metadata: dict[str, Any]) -> str:
    body = markdown.strip()
    if body.startswith(f"> {GENERATED_NOTICE}"):
        lines = body.splitlines()
        index = 0
        while index < len(lines):
            if index > 0 and not lines[index].strip():
                index += 1
                break
            index += 1
        body = "\n".join(lines[index:]).strip()
    marker = "\n## Data Availability / Missing Information"
    if marker in body:
        body = body.split(marker, 1)[0].rstrip()
    if body.startswith("## Data Availability / Missing Information"):
        body = ""
    return metadata_block(metadata) + "\n\n" + body + "\n\n" + missing_information_section(metadata) + "\n"


def generated_at_from_json(data: dict[str, Any]) -> str:
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    return str(metadata.get("generated_at") or data.get("generated_at") or "-")


def generated_at_from_report(path: Path) -> str:
    if path.suffix == ".json" and path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return "-"
        return generated_at_from_json(data if isinstance(data, dict) else {})
    if path.is_file():
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines()[:20]:
            if "Generated at:" in line:
                return line.split("Generated at:", 1)[1].strip().strip("` ")
    return "-"
