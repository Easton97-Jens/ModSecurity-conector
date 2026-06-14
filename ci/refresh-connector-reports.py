#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPORT_DIR = Path("reports/testing/generated")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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


def run_command(cmd: list[str], cwd: Path, env: dict[str, str]) -> tuple[int, str]:
    print("refresh-connector-reports: RUN " + " ".join(cmd))
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
    return proc.returncode, proc.stdout


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


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


CONNECTOR_COVERAGE_OUTPUTS = (
    "reports/testing/test-coverage-overview.md",
    "reports/testing/generated/apache-runtime-results.generated.md",
    "reports/testing/generated/case-matrix.generated.md",
    "reports/testing/generated/connector-gap-summary.generated.md",
    "reports/testing/generated/coverage-summary.generated.md",
    "reports/testing/generated/haproxy-runtime-results.generated.md",
    "reports/testing/generated/nginx-runtime-results.generated.md",
    "reports/testing/generated/phase-coverage.generated.md",
    "reports/testing/generated/runtime-matrix.generated.md",
    "reports/testing/generated/xfail-summary.generated.md",
)

FULL_RUNTIME_OUTPUTS = (
    "reports/testing/generated/full-runtime-matrix.generated.json",
    "reports/testing/generated/full-runtime-matrix.generated.md",
)

CONNECTOR_WORK_QUEUE_OUTPUTS = (
    "reports/testing/generated/connector-work-queue.generated.json",
    "reports/testing/generated/connector-work-queue.generated.md",
)

PHASE_WORK_QUEUE_OUTPUTS = (
    "reports/testing/generated/phase-work-queue.generated.json",
    "reports/testing/generated/phase-work-queue.generated.md",
)

NATIVE_OUTPUTS = (
    "reports/testing/generated/mrts-native-full.generated.json",
    "reports/testing/generated/mrts-native-full.generated.md",
    "reports/testing/generated/mrts-native-apache.generated.json",
    "reports/testing/generated/mrts-native-apache.generated.md",
    "reports/testing/generated/mrts-native-nginx.generated.json",
    "reports/testing/generated/mrts-native-nginx.generated.md",
    "reports/testing/generated/mrts-native-summary.generated.json",
    "reports/testing/generated/mrts-native-summary.generated.md",
)

FULL_RUN_EVIDENCE_OUTPUTS = (
    "reports/testing/generated/full-run-evidence.generated.json",
    "reports/testing/generated/full-run-evidence.generated.md",
)

RUNTIME_CACHE_OUTPUTS = (
    "reports/testing/generated/runtime-component-cache.generated.json",
    "reports/testing/generated/runtime-component-cache.generated.md",
    "reports/testing/generated/runtime-build-cache.generated.json",
    "reports/testing/generated/runtime-build-cache.generated.md",
)

NOLOG_OUTPUTS = (
    "reports/testing/generated/nolog-audit-evidence.generated.json",
    "reports/testing/generated/nolog-audit-evidence.generated.md",
)

RESPONSE_HEADER_OUTPUTS = (
    "reports/testing/generated/response-header-hook-analysis.generated.json",
    "reports/testing/generated/response-header-hook-analysis.generated.md",
)

PHASE4_OUTPUTS = (
    "reports/testing/generated/phase4-hard-abort-capability.generated.json",
    "reports/testing/generated/phase4-hard-abort-capability.generated.md",
)

INTERVENTION_BLOCKING_OUTPUTS = (
    "reports/testing/generated/intervention-blocking-analysis.generated.json",
    "reports/testing/generated/intervention-blocking-analysis.generated.md",
)

NO_MRTS_NOMATCH_OUTPUTS = (
    "reports/testing/generated/no-mrts-intervention-nomatch-analysis.generated.json",
    "reports/testing/generated/no-mrts-intervention-nomatch-analysis.generated.md",
)

BODY_PROCESSOR_OUTPUTS = (
    "reports/testing/generated/body-processor-analysis.generated.json",
    "reports/testing/generated/body-processor-analysis.generated.md",
)

RULE_CHAIN_OUTPUTS = (
    "reports/testing/generated/rule-chain-semantics-analysis.generated.json",
    "reports/testing/generated/rule-chain-semantics-analysis.generated.md",
)

FINAL_CONSISTENCY_OUTPUTS = (
    "reports/testing/generated/final-consistency-audit.generated.json",
    "reports/testing/generated/final-consistency-audit.generated.md",
)

REMAINING_OUTPUTS = (
    "reports/testing/generated/remaining-failure-analysis.generated.json",
    "reports/testing/generated/remaining-failure-analysis.generated.md",
    "reports/testing/generated/next-fix-plan.generated.json",
    "reports/testing/generated/next-fix-plan.generated.md",
)


def make_catalog(connector_root: Path, framework_root: Path, build_root: Path, native_root: Path, python: str) -> list[ReportSpec]:
    report_dir = connector_root / REPORT_DIR
    existing_full_matrix = read_json(report_dir / "full-runtime-matrix.generated.json")
    explicit_manifest = False
    if os.environ.get("FULL_MATRIX_MANIFEST"):
        explicit_manifest = True
        full_matrix_manifest = Path(str(os.environ["FULL_MATRIX_MANIFEST"]))
    elif os.environ.get("MATRIX_ROOT"):
        full_matrix_manifest = Path(str(os.environ["MATRIX_ROOT"])) / "full-runtime-matrix-runs.jsonl"
    elif existing_full_matrix.get("manifest"):
        full_matrix_manifest = Path(str(existing_full_matrix["manifest"]))
    else:
        full_matrix_manifest = build_root.parent / "ModSecurity-conector-full-matrix" / "full-runtime-matrix-runs.jsonl"
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
            name="connector_work_queue",
            owner="connector",
            generator="framework:ci/generate-connector-work-queue.py",
            make_target="generate-work-queue",
            inputs=("reports/testing/generated/full-runtime-matrix.generated.json",),
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
                str(report_dir / "full-runtime-matrix.generated.json"),
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
                "reports/testing/generated/connector-work-queue.generated.json",
                "reports/testing/generated/phase-coverage.generated.md",
                "reports/testing/generated/full-runtime-matrix.generated.json",
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
                str(report_dir / "connector-work-queue.generated.json"),
                "--phase-coverage",
                str(report_dir / "phase-coverage.generated.md"),
                "--full-runtime-matrix",
                str(report_dir / "full-runtime-matrix.generated.json"),
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
            name="nolog_audit_evidence",
            owner="connector",
            generator="ci/generate-nolog-audit-evidence-analysis.py",
            make_target="generate-nolog-audit-evidence-analysis",
            inputs=(
                "reports/testing/generated/connector-work-queue.generated.json",
                "reports/testing/generated/full-runtime-matrix.generated.json",
                "reports/testing/generated/phase-coverage.generated.md",
            ),
            outputs=NOLOG_OUTPUTS + PHASE_WORK_QUEUE_OUTPUTS + FULL_RUN_EVIDENCE_OUTPUTS,
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
                "reports/testing/generated/connector-work-queue.generated.json",
                "reports/testing/generated/full-runtime-matrix.generated.json",
                "reports/testing/generated/phase-coverage.generated.md",
            ),
            outputs=RESPONSE_HEADER_OUTPUTS + PHASE_WORK_QUEUE_OUTPUTS + FULL_RUN_EVIDENCE_OUTPUTS,
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
                "reports/testing/generated/connector-work-queue.generated.json",
                "reports/testing/generated/full-runtime-matrix.generated.json",
                "reports/testing/generated/mrts-native-apache.generated.json",
                "reports/testing/generated/mrts-native-nginx.generated.json",
            ),
            outputs=PHASE4_OUTPUTS + PHASE_WORK_QUEUE_OUTPUTS + FULL_RUN_EVIDENCE_OUTPUTS,
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
                "reports/testing/generated/full-runtime-matrix.generated.json",
                "reports/testing/generated/connector-work-queue.generated.json",
                "reports/testing/generated/phase-work-queue.generated.json",
                "reports/testing/generated/mrts-native-summary.generated.json",
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
                "reports/testing/generated/connector-work-queue.generated.json",
                "reports/testing/generated/full-runtime-matrix.generated.json",
                "reports/testing/generated/remaining-failure-analysis.generated.json",
                "reports/testing/generated/phase-work-queue.generated.json",
                "reports/testing/generated/next-fix-plan.generated.json",
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
                "reports/testing/generated/intervention-blocking-analysis.generated.json",
                "reports/testing/generated/full-runtime-matrix.generated.json",
                "reports/testing/generated/remaining-failure-analysis.generated.json",
                "reports/testing/generated/next-fix-plan.generated.json",
            ),
            outputs=NO_MRTS_NOMATCH_OUTPUTS + FULL_RUN_EVIDENCE_OUTPUTS,
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
                "reports/testing/generated/connector-work-queue.generated.json",
                "reports/testing/generated/remaining-failure-analysis.generated.json",
                "reports/testing/generated/phase-work-queue.generated.json",
                "reports/testing/generated/next-fix-plan.generated.json",
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
                "reports/testing/generated/connector-work-queue.generated.json",
                "reports/testing/generated/remaining-failure-analysis.generated.json",
                "reports/testing/generated/next-fix-plan.generated.json",
                "reports/testing/generated/full-runtime-matrix.generated.json",
            ),
            outputs=RULE_CHAIN_OUTPUTS + FULL_RUN_EVIDENCE_OUTPUTS,
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
                "reports/testing/generated/full-runtime-matrix.generated.json",
                "reports/testing/generated/connector-work-queue.generated.json",
                "reports/testing/generated/phase-work-queue.generated.json",
                "reports/testing/generated/remaining-failure-analysis.generated.json",
                "reports/testing/generated/next-fix-plan.generated.json",
                "reports/testing/generated/full-run-evidence.generated.json",
                "reports/testing/generated/mrts-native-summary.generated.json",
                "reports/testing/generated/phase4-hard-abort-capability.generated.json",
                "reports/testing/generated/nolog-audit-evidence.generated.json",
                "reports/testing/generated/response-header-hook-analysis.generated.json",
                "reports/testing/generated/body-processor-analysis.generated.json",
                "reports/testing/generated/intervention-blocking-analysis.generated.json",
                "reports/testing/generated/no-mrts-intervention-nomatch-analysis.generated.json",
                "reports/testing/generated/rule-chain-semantics-analysis.generated.json",
            ),
            outputs=FINAL_CONSISTENCY_OUTPUTS + FULL_RUN_EVIDENCE_OUTPUTS,
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
            owner="connector",
            generator="ci/update-runtime-reports.py",
            make_target="prepare-runtime-components",
            inputs=(
                "reports/testing/generated/runtime-component-cache.generated.json",
                "reports/testing/generated/runtime-build-cache.generated.json",
            ),
            outputs=RUNTIME_CACHE_OUTPUTS + FULL_RUN_EVIDENCE_OUTPUTS,
            command=(
                python,
                "ci/update-runtime-reports.py",
                "--connector-root",
                str(connector_root),
            ),
            requires_runtime=True,
        ),
    ]


def resolve_input(raw: str, connector_root: Path, framework_root: Path, build_root: Path) -> Path:
    path = Path(raw)
    if path.is_absolute():
        return path
    if raw.startswith("framework:"):
        return framework_root / raw.removeprefix("framework:")
    if raw.startswith("BUILD_ROOT:"):
        return build_root / raw.removeprefix("BUILD_ROOT:")
    return connector_root / raw


def resolve_output(raw: str, connector_root: Path) -> Path:
    path = Path(raw)
    return path if path.is_absolute() else connector_root / path


def run_spec(
    spec: ReportSpec,
    connector_root: Path,
    framework_root: Path,
    build_root: Path,
    env: dict[str, str],
) -> dict[str, Any]:
    input_paths = [resolve_input(raw, connector_root, framework_root, build_root) for raw in spec.inputs]
    output_paths = [resolve_output(raw, connector_root) for raw in spec.outputs]
    missing_inputs = [path for path in input_paths if not path.is_file()]
    if missing_inputs and (spec.optional or spec.name in {"runtime_cache_reports"}):
        print(
            "refresh-connector-reports: SKIPPED_MISSING_INPUT "
            f"{spec.name}: " + ", ".join(display_path(path, connector_root, framework_root, build_root) for path in missing_inputs)
        )
        return report_record(spec, "skipped_missing_input", input_paths, output_paths, connector_root, framework_root, build_root, missing_inputs)

    rc, _ = run_command(list(spec.command), connector_root, env)
    missing_outputs = [path for path in output_paths if not path.is_file()]
    if rc != 0 or missing_outputs:
        status = "failed"
    else:
        status = "generated"
    record = report_record(spec, status, input_paths, output_paths, connector_root, framework_root, build_root, missing_inputs)
    record["return_code"] = rc
    if missing_outputs:
        record["missing_outputs"] = [
            display_path(path, connector_root, framework_root, build_root) for path in missing_outputs
        ]
    return record


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
    return {
        "report_name": spec.name,
        "path": ", ".join(display_path(path, connector_root, framework_root, build_root) for path in output_paths),
        "owner": spec.owner,
        "generator": spec.generator,
        "make_target": spec.make_target,
        "status": status,
        "input_files": [display_path(path, connector_root, framework_root, build_root) for path in input_paths],
        "output_files": [display_path(path, connector_root, framework_root, build_root) for path in output_paths],
        "missing_inputs": [display_path(path, connector_root, framework_root, build_root) for path in missing_inputs],
        "input_fingerprint": combined_fingerprint(input_paths),
        "output_fingerprint": combined_fingerprint(output_paths),
        "requires_runtime": spec.requires_runtime,
        "requires_native_mrts": spec.requires_native_mrts,
        "requires_full_matrix": spec.requires_full_matrix,
        "optional": spec.optional,
    }


def render_manifest_md(manifest: dict[str, Any]) -> str:
    lines = [
        "# Report Refresh Manifest",
        "",
        "Generated file - do not edit manually.",
        "",
        f"- Generated at: `{manifest['generated_at']}`",
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
            "## Reports",
            "| Report | Owner | Generator | Target | Status | Requires runtime | Requires native MRTS | Requires full matrix | Missing input |",
            "|---|---|---|---|---|---|---|---|---|",
        ]
    )
    for report in manifest["reports"]:
        missing = ", ".join(report.get("missing_inputs", [])) or "-"
        lines.append(
            "| "
            + " | ".join(
                [
                    report["report_name"],
                    report["owner"],
                    report["generator"],
                    report["make_target"],
                    report["status"],
                    str(report["requires_runtime"]).lower(),
                    str(report["requires_native_mrts"]).lower(),
                    str(report["requires_full_matrix"]).lower(),
                    missing,
                ]
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def manifest_inputs(report_dir: Path) -> dict[str, str]:
    native_json = [
        report_dir / "mrts-native-full.generated.json",
        report_dir / "mrts-native-apache.generated.json",
        report_dir / "mrts-native-nginx.generated.json",
        report_dir / "mrts-native-summary.generated.json",
    ]
    return {
        "full_runtime_matrix": combined_fingerprint([report_dir / "full-runtime-matrix.generated.json"]),
        "native_mrts": combined_fingerprint(native_json),
        "build_cache": combined_fingerprint([report_dir / "runtime-build-cache.generated.json"]),
        "component_cache": combined_fingerprint([report_dir / "runtime-component-cache.generated.json"]),
    }


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
    default_state_home = Path(os.environ.get("XDG_STATE_HOME", str(Path.home() / ".local/state")))
    build_root = Path(args.build_root or default_state_home / "ModSecurity-conector-build").resolve()
    native_root = Path(args.native_root or build_root / "mrts-native").resolve()
    report_dir = connector_root / REPORT_DIR
    report_dir.mkdir(parents=True, exist_ok=True)
    python = sys.executable
    env = dict(os.environ)
    env.update(
        {
            "PYTHONDONTWRITEBYTECODE": env.get("PYTHONDONTWRITEBYTECODE", "1"),
            "FRAMEWORK_ROOT": str(framework_root),
            "CONNECTOR_ROOT": str(connector_root),
            "BUILD_ROOT": str(build_root),
            "MRTS_NATIVE_ROOT": str(native_root),
        }
    )

    catalog = make_catalog(connector_root, framework_root, build_root, native_root, python)
    reports: list[dict[str, Any]] = []
    for spec in catalog:
        reports.append(run_spec(spec, connector_root, framework_root, build_root, env))

    submodule_root = connector_root / "modules/ModSecurity-test-Framework"
    mrts_root = framework_root / "tools/MRTS"
    manifest = {
        "generated_at": utc_now(),
        "connector_sha": git_sha(connector_root),
        "framework_sha": git_sha(framework_root),
        "framework_submodule_sha": git_sha(submodule_root),
        "mrts_sha": git_sha(mrts_root),
        "inputs": manifest_inputs(report_dir),
        "reports": reports,
    }
    json_path = report_dir / "report-refresh-manifest.generated.json"
    md_path = report_dir / "report-refresh-manifest.generated.md"
    json_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(render_manifest_md(manifest), encoding="utf-8")
    print(f"refresh-connector-reports: manifest={md_path}")

    failed = [item for item in reports if item["status"] == "failed"]
    skipped_required = [
        item
        for item in reports
        if item["status"] == "skipped_missing_input" and not item.get("optional")
    ]
    if failed or (args.strict_inputs and skipped_required):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
