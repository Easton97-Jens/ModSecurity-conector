#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
from pathlib import Path

# CI helpers are shared from ci/lib even when this file is executed directly.
_CI_ROOT = next(parent for parent in Path(__file__).resolve().parents if parent.name == "ci")
if str(_CI_ROOT / "lib") not in sys.path:
    sys.path.insert(0, str(_CI_ROOT / "lib"))
from typing import Any
from urllib.parse import urlsplit

from generated_report_utils import (
    DATA_SOURCE_POLICY,
    FILENAME_TO_KEY,
    GENERATED_NOTICE,
    GENERATED_REPORTS,
    GENERATED_ROOT,
    portable_markdown_text,
    read_report_metadata,
    report_relpath,
    report_path,
    resolve_input_reference,
    sha256_file,
)
from runtime_path_utils import verified_runtime_paths

INSECURE_REPO_URL_PATTERNS = (
    "http://github.com",
    "git@github.com:",
    "ssh://git@github.com",
    "git://github.com",
)

negative_tests = (
    "http://github.com/coreruleset/go-ftw",
    "git@github.com:coreruleset/go-ftw.git",
    "ssh://git@github.com/coreruleset/go-ftw.git",
    "git://github.com/coreruleset/go-ftw.git",
    "https://gitlab.com/coreruleset/go-ftw",
    "https://github.com/coreruleset",
    "https://github.com/coreruleset/go-ftw/extra",
)

allowed_examples = (
    "https://github.com/coreruleset/go-ftw",
    "https://github.com/coreruleset/go-ftw.git",
)

FULL_MATRIX_CONNECTORS = ("apache", "nginx", "haproxy")
FULL_MATRIX_CRS_VARIANTS = ("no-crs", "with-crs")
FULL_MATRIX_MRTS_VARIANTS = ("no-mrts", "with-mrts")
VERIFIED_RUN_ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
VERIFIED_CRITICAL_INPUT_STATUSES = {"complete"}
VERIFIED_CRITICAL_INPUT_RECORD_STATUSES = {"present"}
SELF_GENERATED_CRITICAL_INPUT_STATUS = "self_generated_no_direct_input"
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}\Z")


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def is_plain_https_github_repo_url(url: str) -> bool:
    parsed = urlsplit(url.strip())
    if parsed.scheme != "https" or parsed.netloc != "github.com":
        return False
    if parsed.query or parsed.fragment:
        return False
    repo = parsed.path.removeprefix("/").removesuffix(".git").strip("/")
    parts = repo.split("/")
    return len(parts) == 2 and bool(parts[0]) and bool(parts[1])


def load_json(path: Path, errors: list[str], connector_root: Path, *, root: Path | None = None) -> dict[str, Any]:
    trusted_root = root or connector_root
    if not is_regular_file(path, root=trusted_root):
        errors.append(f"{rel(path, connector_root)}: expected a trusted regular JSON file")
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{rel(path, connector_root)}: invalid JSON: {exc}")
        return {}
    if not isinstance(data, dict):
        errors.append(f"{rel(path, connector_root)}: JSON root must be an object")
        return {}
    return data


def is_unverified_critical_input_status(value: object, *, report_name: str | None = None) -> bool:
    status = str(value or "unknown").strip().lower()
    if status in VERIFIED_CRITICAL_INPUT_STATUSES:
        return False
    return not (
        status == SELF_GENERATED_CRITICAL_INPUT_STATUS
        and report_name == "report_refresh_manifest"
    )


def is_unverified_critical_input_record_status(value: object) -> bool:
    return str(value or "unknown").strip().lower() not in VERIFIED_CRITICAL_INPUT_RECORD_STATUSES


def trusted_input_roots(
    connector_root: Path,
    *,
    build_root: Path | None = None,
    framework_root: Path | None = None,
) -> tuple[Path, ...]:
    selected_build_root = (build_root or Path(verified_runtime_paths()["BUILD_ROOT"])).absolute()
    selected_framework_root = (framework_root or connector_root / "modules" / "ModSecurity-test-Framework").absolute()
    return connector_root.absolute(), selected_build_root, selected_framework_root


def input_root_for_path(path: Path, roots: tuple[Path, ...]) -> Path | None:
    return next((root for root in roots if is_within(path, root)), None)


def validate_critical_input_records(
    inputs: object,
    *,
    connector_root: Path,
    errors: list[str],
    context: str,
    report_name: str,
    build_root: Path | None = None,
    framework_root: Path | None = None,
) -> None:
    if not isinstance(inputs, list):
        errors.append(f"{context}: inputs must be a list")
        return
    if report_name == "report_refresh_manifest" and not inputs:
        return
    if not inputs:
        errors.append(f"{context}: critical report has no direct input receipts")
        return
    roots = trusted_input_roots(connector_root, build_root=build_root, framework_root=framework_root)
    for item in inputs:
        if not isinstance(item, dict):
            errors.append(f"{context}: critical report input must be an object")
            continue
        value = item.get("path")
        if not isinstance(value, str) or not value:
            errors.append(f"{context}: critical report input path is invalid")
            continue
        if is_unverified_critical_input_record_status(item.get("status")):
            errors.append(f"{context}: critical report input is {item.get('status') or 'unknown'}: {value}")
            continue
        declared_hash = item.get("sha256")
        if not isinstance(declared_hash, str) or not SHA256_PATTERN.fullmatch(declared_hash):
            errors.append(f"{context}: critical report input has invalid sha256: {value}")
            continue
        path = resolve_input_reference(value, connector_root, framework_root, build_root)
        root = input_root_for_path(path, roots)
        if root is None or not is_regular_file(path, root=root):
            errors.append(f"{context}: critical report input is not a trusted regular file: {value}")
            continue
        if sha256_file(path) != declared_hash:
            errors.append(f"{context}: critical report input hash mismatch: {value}")


def expected_full_matrix_job_ids() -> set[str]:
    return {
        f"{connector}:{crs}:{mrts}"
        for connector in FULL_MATRIX_CONNECTORS
        for crs in FULL_MATRIX_CRS_VARIANTS
        for mrts in FULL_MATRIX_MRTS_VARIANTS
    }


def expected_full_matrix_jobs() -> tuple[tuple[str, str, str, str], ...]:
    return tuple(
        (job_id, *job_id.split(":"))
        for job_id in sorted(expected_full_matrix_job_ids())
    )


def is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(root.resolve(strict=False))
        return True
    except (OSError, RuntimeError, ValueError):
        return False


def has_symlink_component(path: Path, root: Path) -> bool:
    try:
        relative = path.absolute().relative_to(root.absolute())
    except ValueError:
        return True
    current = root.absolute()
    try:
        if current.is_symlink():
            return True
        for component in relative.parts:
            current = current / component
            if current.is_symlink():
                return True
    except OSError:
        return True
    return False


def is_regular_file(path: Path, *, root: Path) -> bool:
    try:
        if not is_within(path, root) or has_symlink_component(path, root):
            return False
        return path.is_file() and not path.is_symlink() and stat.S_ISREG(path.stat().st_mode)
    except OSError:
        return False


def read_jsonl_objects(path: Path, errors: list[str], connector_root: Path, *, root: Path) -> list[dict[str, Any]]:
    if not is_regular_file(path, root=root):
        errors.append(f"{rel(path, connector_root)}: expected a regular JSONL file")
        return []
    rows: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        errors.append(f"{rel(path, connector_root)}: cannot read JSONL: {exc}")
        return rows
    for line_number, raw in enumerate(lines, start=1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"{rel(path, connector_root)}:{line_number}: invalid JSONL: {exc.msg}")
            continue
        if not isinstance(row, dict):
            errors.append(f"{rel(path, connector_root)}:{line_number}: JSONL record must be an object")
            continue
        rows.append(row)
    return rows


def check_json_metadata(path: Path, errors: list[str], connector_root: Path) -> None:
    data = load_json(path, errors, connector_root)
    metadata = data.get("metadata")
    if not isinstance(metadata, dict):
        errors.append(f"{rel(path, connector_root)}: missing metadata object")
        return
    required = (
        "generated_notice",
        "generated_at",
        "generated_by",
        "make_target",
        "owner",
        "severity",
        "input_status",
        "inputs",
        "missing_inputs",
        "empty_inputs",
        "unknown_inputs",
        "verified_run_id",
        "data_source_policy",
        "schema_version",
    )
    for key in required:
        if key not in metadata:
            errors.append(f"{rel(path, connector_root)}: metadata.{key} is missing")
    if metadata.get("generated_notice") != GENERATED_NOTICE:
        errors.append(f"{rel(path, connector_root)}: metadata.generated_notice is not canonical")
    if not metadata.get("verified_run_id") or metadata.get("verified_run_id") == "unknown":
        errors.append(f"{rel(path, connector_root)}: metadata.verified_run_id is missing or unknown")
    if metadata.get("data_source_policy") != DATA_SOURCE_POLICY:
        errors.append(f"{rel(path, connector_root)}: metadata.data_source_policy is not {DATA_SOURCE_POLICY}")
    if not isinstance(metadata.get("inputs"), list):
        errors.append(f"{rel(path, connector_root)}: metadata.inputs must be a list")


def check_markdown_metadata(path: Path, errors: list[str], connector_root: Path) -> None:
    text = path.read_text(encoding="utf-8", errors="replace")
    first_lines = text.splitlines()[:20]
    if not first_lines or first_lines[0].strip() != f"> {GENERATED_NOTICE}":
        errors.append(f"{rel(path, connector_root)}: missing generated notice at top")
    if not any("Generated at:" in line for line in first_lines):
        errors.append(f"{rel(path, connector_root)}: missing visible generated timestamp")
    if not any("Verified run id:" in line for line in first_lines):
        errors.append(f"{rel(path, connector_root)}: missing visible verified run id")
    if not any("Data source policy:" in line for line in first_lines):
        errors.append(f"{rel(path, connector_root)}: missing visible data source policy")
    if "## Data Availability / Missing Information" not in text:
        errors.append(f"{rel(path, connector_root)}: missing data availability section")
    if "## Data Sources" not in text:
        errors.append(f"{rel(path, connector_root)}: missing data sources section")
    check_empty_tables_explained(path, text, errors, connector_root)


def is_table_separator(line: str) -> bool:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return bool(cells) and all(cell and set(cell) <= {"-", ":"} and cell.count("-") >= 3 for cell in cells)


def check_empty_tables_explained(path: Path, text: str, errors: list[str], connector_root: Path) -> None:
    lines = text.splitlines()
    for index in range(1, len(lines)):
        if not is_table_separator(lines[index]):
            continue
        if "|" not in lines[index - 1]:
            continue
        next_index = index + 1
        while next_index < len(lines) and not lines[next_index].strip():
            next_index += 1
        if next_index >= len(lines) or lines[next_index].startswith("## "):
            window = "\n".join(lines[index + 1 : min(index + 5, len(lines))])
            if "_No rows available. Reason:" not in window:
                errors.append(f"{rel(path, connector_root)}:{index + 1}: empty table lacks a Missing/Empty explanation")


def check_existing_generated_reports(connector_root: Path, errors: list[str]) -> None:
    generated_root = connector_root / GENERATED_ROOT
    for path in sorted(generated_root.rglob("*.generated.*")):
        if path.name.endswith(".generated.de.md"):
            continue
        if os.environ.get("ALLOW_IN_PROGRESS_SYSTEM_PROOF") == "1" and path.name.startswith("system-environment-proof.generated."):
            continue
        if path.suffix == ".json":
            check_json_metadata(path, errors, connector_root)
        elif path.suffix == ".md":
            check_markdown_metadata(path, errors, connector_root)


def check_generated_markdown_portability(connector_root: Path, errors: list[str]) -> None:
    generated_root = connector_root / GENERATED_ROOT
    for path in sorted(generated_root.rglob("*.generated*.md")):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if portable_markdown_text(text) != text:
            errors.append(f"{rel(path, connector_root)}: contains a non-portable local path display")


def check_no_flat_reports(connector_root: Path, errors: list[str]) -> None:
    generated_root = connector_root / GENERATED_ROOT
    for path in sorted(generated_root.glob("*.generated.*")):
        if path.name.endswith(".generated.de.md"):
            continue
        if path.exists():
            errors.append(f"{rel(path, connector_root)}: stale flat generated report remains")


def check_manifest(
    connector_root: Path,
    errors: list[str],
    *,
    strict_evidence: bool,
    build_root: Path | None = None,
    framework_root: Path | None = None,
) -> None:
    manifest_path = report_path(connector_root, "report_refresh_manifest", "json")
    if not manifest_path.is_file():
        errors.append(f"{rel(manifest_path, connector_root)}: refresh manifest is missing")
        return
    manifest = load_json(manifest_path, errors, connector_root)
    reports = manifest.get("reports")
    if not isinstance(reports, list):
        errors.append(f"{rel(manifest_path, connector_root)}: reports list is missing")
        return
    for record in reports:
        if not isinstance(record, dict):
            errors.append(f"{rel(manifest_path, connector_root)}: report record must be an object")
            continue
        status = record.get("status")
        outputs = record.get("output_files")
        if not isinstance(outputs, list):
            errors.append(f"{rel(manifest_path, connector_root)}: report record missing output_files")
            continue
        for output in outputs:
            path = connector_root / str(output)
            if status == "generated" and not path.is_file():
                errors.append(f"{output}: manifest says generated but file is missing")
        for key in ("category", "kind", "owner", "severity", "input_status", "inputs", "missing_inputs", "empty_inputs", "unknown_inputs"):
            if key not in record:
                errors.append(f"{rel(manifest_path, connector_root)}: report {record.get('report_name', '<unknown>')} missing {key}")
        if strict_evidence and record.get("severity") == "critical":
            report_name = record.get("report_name", "<unknown>")
            if is_unverified_critical_input_status(record.get("input_status"), report_name=str(report_name)):
                errors.append(
                    f"{rel(manifest_path, connector_root)}: critical report {report_name} has {record.get('input_status') or 'unknown'} input_status"
                )
            for key in ("missing_inputs", "empty_inputs", "unknown_inputs", "stale_inputs"):
                values = record.get(key)
                if not isinstance(values, list):
                    errors.append(
                        f"{rel(manifest_path, connector_root)}: critical report {report_name} {key} must be a list"
                    )
                elif values:
                    errors.append(
                        f"{rel(manifest_path, connector_root)}: critical report {report_name} has {key}"
                    )
            validate_critical_input_records(
                record.get("inputs"),
                connector_root=connector_root,
                errors=errors,
                context=f"{rel(manifest_path, connector_root)}: critical report {report_name}",
                report_name=str(report_name),
                build_root=build_root,
                framework_root=framework_root,
            )


def check_system_environment_proof(connector_root: Path, errors: list[str]) -> None:
    md_path = report_path(connector_root, "system_environment_proof", "md")
    json_path = report_path(connector_root, "system_environment_proof", "json")
    if md_path.is_file():
        text = md_path.read_text(encoding="utf-8", errors="replace")
        if "## Framework Environment Resolution" not in text:
            errors.append(f"{rel(md_path, connector_root)}: missing Framework Environment Resolution section")
        if "## Runtime Component Readiness" not in text:
            errors.append(f"{rel(md_path, connector_root)}: missing Runtime Component Readiness section")
        if "## NGINX Runtime Module Readiness" not in text:
            errors.append(f"{rel(md_path, connector_root)}: missing NGINX Runtime Module Readiness section")
        if "## HTTPS Repository URL Policy" not in text:
            errors.append(f"{rel(md_path, connector_root)}: missing HTTPS Repository URL Policy section")
        expected_header = "| Tool | Status | Resolved Command | Source | Candidates | Version / Output | Notes |"
        if expected_header not in text:
            errors.append(f"{rel(md_path, connector_root)}: tool table missing Candidates/Notes columns")
        readiness_header = "| Component | Status | Expected Path | Source URL | Version / Ref | How to Prepare |"
        if readiness_header not in text:
            errors.append(f"{rel(md_path, connector_root)}: runtime readiness table missing Source URL/Version columns")
        for marker in (
            "CI_APACHE_BIN_CANDIDATES",
            "CI_APXS_BIN_CANDIDATES",
            "CI_NGINX_BIN_CANDIDATES",
            "GO_FTW_SOURCE_URL",
            "GO_FTW_PROMPT_EXPECTED_LATEST",
            "ALBEDO_SOURCE_URL",
            "ALBEDO_PROMPT_EXPECTED_LATEST",
            "EXPAT_SOURCE_URL",
        ):
            if marker not in text:
                errors.append(f"{rel(md_path, connector_root)}: missing {marker} in framework environment section")
    if json_path.is_file():
        data = load_json(json_path, errors, connector_root)
        if "framework_common_sh_status" not in data:
            errors.append(f"{rel(json_path, connector_root)}: missing framework_common_sh_status")
        framework_environment = data.get("framework_environment")
        if not isinstance(framework_environment, dict):
            errors.append(f"{rel(json_path, connector_root)}: missing framework_environment object")
        elif "common_sh_status" not in framework_environment:
            errors.append(f"{rel(json_path, connector_root)}: missing framework_environment.common_sh_status")
        https_policy = data.get("https_repo_url_policy")
        if not isinstance(https_policy, dict):
            errors.append(f"{rel(json_path, connector_root)}: missing https_repo_url_policy object")
        else:
            for key in ("status", "blocked_protocols", "allowed_protocol", "notes"):
                if key not in https_policy:
                    errors.append(f"{rel(json_path, connector_root)}: https_repo_url_policy missing {key}")
        readiness = data.get("runtime_component_readiness")
        if not isinstance(readiness, list) or not readiness:
            errors.append(f"{rel(json_path, connector_root)}: runtime_component_readiness list is missing")
        else:
            for item in readiness:
                if not isinstance(item, dict):
                    errors.append(f"{rel(json_path, connector_root)}: runtime readiness entry must be an object")
                    continue
                for key in ("source_url", "version_ref"):
                    if key not in item:
                        errors.append(f"{rel(json_path, connector_root)}: runtime readiness {item.get('component', '<unknown>')} missing {key}")
        tools = data.get("tools")
        if not isinstance(tools, list) or not tools:
            errors.append(f"{rel(json_path, connector_root)}: tools list is missing")
            return
        for tool in tools:
            if not isinstance(tool, dict):
                errors.append(f"{rel(json_path, connector_root)}: tool entry must be an object")
                continue
            for key in ("resolved_command", "source", "candidates", "version_output", "return_code", "notes"):
                if key not in tool:
                    errors.append(f"{rel(json_path, connector_root)}: tool {tool.get('tool', '<unknown>')} missing {key}")


def legacy_reference_regex() -> re.Pattern[str]:
    filenames = "|".join(re.escape(name) for name in sorted(FILENAME_TO_KEY, key=len, reverse=True))
    return re.compile(
        rf"(?:reports/testing/generated/|\.?/generated/)(?:{filenames})(?![A-Za-z0-9_.-])"
    )


def check_no_legacy_references(connector_root: Path, errors: list[str]) -> None:
    pattern = legacy_reference_regex()
    candidates: list[Path] = [connector_root / "README.md", connector_root / "Makefile"]
    for base in (connector_root / "docs", connector_root / "reports/testing"):
        if not base.is_dir():
            continue
        for suffix in ("*.md", "*.json"):
            for path in sorted(base.rglob(suffix)):
                if GENERATED_ROOT in path.relative_to(connector_root).parents:
                    continue
                candidates.append(path)
    candidates.extend(sorted((connector_root / "reports/testing/generated").rglob("*.generated.md")))
    candidates.extend(sorted((connector_root / "reports/testing/generated").rglob("*.generated.json")))
    for path in candidates:
        if not path.is_file():
            continue
        if path.name.startswith("system-environment-proof.generated."):
            continue
        for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
            if pattern.search(line):
                errors.append(f"{rel(path, connector_root)}:{line_number}: legacy flat generated-report reference")


def check_no_flat_generator_writes(connector_root: Path, framework_root: Path, errors: list[str]) -> None:
    filenames = "|".join(re.escape(name) for name in sorted(FILENAME_TO_KEY, key=len, reverse=True))
    direct_write = re.compile(
        rf"(?:report_dir|output_dir|generated_root|REPORT_DIR|OUT)\s*/\s*[\"'](?:{filenames})[\"']"
    )
    scan_roots = [connector_root / "ci", framework_root / "ci"]
    for scan_root in scan_roots:
        if not scan_root.is_dir():
            continue
        for path in sorted(scan_root.glob("*.py")):
            if path.name in {"generated_report_utils.py", "check-generated-report-layout.py"}:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for match in direct_write.finditer(text):
                line_number = text.count("\n", 0, match.start()) + 1
                errors.append(f"{rel(path, connector_root)}:{line_number}: flat generated-report write path")


def check_no_runtime_source_url_hardcoding(connector_root: Path, errors: list[str]) -> None:
    path = connector_root / "ci/provisioning/components/prepare-runtime-components.py"
    if not path.is_file():
        return
    forbidden = (
        "https://github.com/coreruleset/go-ftw",
        "https://github.com/coreruleset/albedo",
        "https://github.com/libexpat/libexpat",
    )
    text = path.read_text(encoding="utf-8", errors="replace")
    for url in forbidden:
        if url in text:
            errors.append(f"{rel(path, connector_root)}: hard-coded runtime source URL must live in framework common.sh: {url}")


def check_no_insecure_repo_url_literals(connector_root: Path, framework_root: Path, errors: list[str]) -> None:
    for pattern in INSECURE_REPO_URL_PATTERNS:
        if not any(pattern in sample for sample in negative_tests):
            errors.append(f"internal https-url-policy negative tests do not cover: {pattern}")
    for sample in negative_tests:
        if is_plain_https_github_repo_url(sample):
            errors.append(f"internal https-url-policy negative test was accepted: {sample}")
    for sample in allowed_examples:
        if not is_plain_https_github_repo_url(sample):
            errors.append(f"internal https-url-policy allowed example was rejected: {sample}")
    text_suffixes = {"", ".md", ".py", ".sh", ".json", ".yml", ".yaml", ".mk"}
    scan_paths: list[Path] = [
        connector_root / "Makefile",
        connector_root / "README.md",
    ]
    scan_paths.extend(sorted(connector_root.glob("COMPILE_*.md")))
    for base in (
        connector_root / "ci",
        framework_root / "ci",
        connector_root / "docs",
        connector_root / "reports/testing",
    ):
        if base.is_dir():
            scan_paths.extend(path for path in sorted(base.rglob("*")) if path.is_file())
    for path in scan_paths:
        if not path.is_file():
            continue
        if "__pycache__" in path.parts or path.suffix not in text_suffixes:
            continue
        try:
            if (connector_root / GENERATED_ROOT).resolve(strict=False) in path.resolve(strict=False).parents:
                continue
        except OSError:
            continue
        if path.resolve(strict=False) == Path(__file__).resolve(strict=False):
            continue
        if path.name == "generate-system-environment-proof.py":
            continue
        if path.name.startswith("system-environment-proof.generated."):
            continue
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(lines, start=1):
            for pattern in INSECURE_REPO_URL_PATTERNS:
                if pattern in line:
                    errors.append(f"{rel(path, connector_root)}:{line_number}: insecure repo URL protocol literal: {pattern}")


def check_registry_paths(connector_root: Path, errors: list[str]) -> None:
    for key, report in GENERATED_REPORTS.items():
        if os.environ.get("ALLOW_IN_PROGRESS_SYSTEM_PROOF") == "1" and key == "verified_run_manifest":
            continue
        if not report.category:
            errors.append(f"registry:{key}: missing category")
        if not report.owner:
            errors.append(f"registry:{key}: missing owner")
        if not report.severity:
            errors.append(f"registry:{key}: missing severity")
        for ext in report.formats:
            path = report_path(connector_root, key, ext)
            if path.parent.name != report.category:
                errors.append(f"{rel(path, connector_root)}: registry category mismatch")
            if not path.is_file() and report.commit_policy not in {"local-only", "do-not-commit"} and report.data_kind != "system-proof":
                errors.append(f"{rel(path, connector_root)}: registry output missing")


def check_no_orphan_generated_reports(connector_root: Path, errors: list[str]) -> None:
    generated_root = connector_root / GENERATED_ROOT
    expected = {
        str((connector_root / report_relpath(key, ext)).resolve(strict=False))
        for key, report in GENERATED_REPORTS.items()
        for ext in report.formats
    }
    for path in sorted(generated_root.rglob("*.generated.*")):
        if path.name.endswith(".generated.de.md"):
            continue
        resolved = str(path.resolve(strict=False))
        if path.name not in FILENAME_TO_KEY:
            errors.append(f"{rel(path, connector_root)}: generated file is not in registry")
        elif resolved not in expected:
            errors.append(f"{rel(path, connector_root)}: generated file is not at registry path")


def critical_run_keys() -> set[str]:
    return {
        key
        for key, report in GENERATED_REPORTS.items()
        if report.severity == "critical" and report.commit_policy not in {"local-only", "do-not-commit"}
    } | {"system_environment_proof"}


def check_critical_report_run_consistency(
    connector_root: Path,
    errors: list[str],
    *,
    strict_evidence: bool,
    build_root: Path | None = None,
    framework_root: Path | None = None,
) -> None:
    run_ids: dict[str, set[str]] = {}
    keys = critical_run_keys()
    if os.environ.get("ALLOW_IN_PROGRESS_SYSTEM_PROOF") == "1":
        keys = keys - {"system_environment_proof", "verified_run_manifest"}
    for key in sorted(keys):
        report = GENERATED_REPORTS[key]
        for ext in report.formats:
            path = report_path(connector_root, key, ext)
            if not path.is_file():
                continue
            metadata = read_report_metadata(path)
            run_id = str(metadata.get("verified_run_id") or "")
            if not run_id or run_id == "unknown":
                errors.append(f"{rel(path, connector_root)}: critical report has unknown verified_run_id")
            else:
                run_ids.setdefault(run_id, set()).add(f"{key}.{ext}")
            for sha_key in ("connector_sha", "framework_sha"):
                if str(metadata.get(sha_key) or "unknown") == "unknown":
                    errors.append(f"{rel(path, connector_root)}: critical report has unknown {sha_key}")
            if path.suffix == ".json":
                data = load_json(path, errors, connector_root)
                metadata_obj = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
                if strict_evidence and is_unverified_critical_input_status(metadata_obj.get("input_status"), report_name=key):
                    errors.append(
                        f"{rel(path, connector_root)}: critical report metadata.input_status is {metadata_obj.get('input_status') or 'unknown'}"
                    )
                if strict_evidence:
                    validate_critical_input_records(
                        metadata_obj.get("inputs"),
                        connector_root=connector_root,
                        errors=errors,
                        context=f"{rel(path, connector_root)}: critical report metadata",
                        report_name=key,
                        build_root=build_root,
                        framework_root=framework_root,
                    )
    if len(run_ids) > 1:
        summary = "; ".join(f"{run_id}: {', '.join(sorted(items))}" for run_id, items in sorted(run_ids.items()))
        errors.append(f"critical generated reports use multiple verified_run_id values: {summary}")


def exact_canonical_path(value: object, expected: Path) -> bool:
    if not isinstance(value, str) or not value:
        return False
    candidate = Path(value)
    return candidate.is_absolute() and candidate.absolute() == expected.absolute()


def check_job_artifact(
    *,
    job_id: str,
    label: str,
    expected_path: Path,
    declared_path: object,
    declared_hash: object,
    job_root: Path,
    errors: list[str],
    connector_root: Path,
) -> None:
    if not exact_canonical_path(declared_path, expected_path):
        errors.append(f"{job_id}: {label} path is not canonical")
    if not is_within(expected_path, job_root) or has_symlink_component(expected_path, job_root):
        errors.append(f"{job_id}: {label} path escapes the job root")
    if not is_regular_file(expected_path, root=job_root):
        errors.append(f"{job_id}: {label} is not a regular file")
        return
    actual_hash = sha256_file(expected_path)
    if not isinstance(declared_hash, str) or declared_hash != actual_hash:
        errors.append(f"{job_id}: {label} hash mismatch")


def check_verified_command_receipt(
    verified_manifest: dict[str, Any],
    *,
    manifest_path: Path,
    connector_root: Path,
    build_root: Path,
    run_id: str,
    errors: list[str],
) -> None:
    command_path = build_root / "verified-runs" / run_id / "verified-commands.json"
    command_record = verified_manifest.get("command_file")
    if not isinstance(command_record, dict):
        errors.append(f"{rel(manifest_path, connector_root)}: command_file receipt is missing")
        return
    if not exact_canonical_path(command_record.get("path"), command_path):
        errors.append(f"{rel(manifest_path, connector_root)}: command_file path is not canonical")
    if command_record.get("status") != "present" or not is_regular_file(command_path, root=build_root):
        errors.append(f"{rel(command_path, connector_root)}: verified command receipt is missing or not regular")
        return
    if command_record.get("sha256") != sha256_file(command_path):
        errors.append(f"{rel(command_path, connector_root)}: verified command receipt hash mismatch")
    if command_record.get("bytes") != command_path.stat().st_size:
        errors.append(f"{rel(command_path, connector_root)}: verified command receipt byte count mismatch")
    commands = load_json(command_path, errors, connector_root, root=build_root)
    if commands.get("verified_run_id") != run_id:
        errors.append(f"{rel(command_path, connector_root)}: verified_run_id mismatch")
    command_rows = commands.get("commands")
    if not isinstance(command_rows, list):
        errors.append(f"{rel(command_path, connector_root)}: commands list is missing")
        return
    expected = [
        row
        for row in command_rows
        if isinstance(row, dict)
        and row.get("logical_target") == "full-matrix-parallel"
        and row.get("phase") == "runtime-producers"
        and row.get("required") is True
    ]
    if len(expected) != 1:
        errors.append(f"{rel(command_path, connector_root)}: expected one required full-matrix producer command")
    elif not expected[0].get("runtime_complete") or expected[0].get("runtime_status") not in {"runtime_completed", "runtime_completed_with_mismatches"}:
        errors.append(f"{rel(command_path, connector_root)}: full-matrix producer command is not runtime complete")


def read_raw_matrix_rows(
    matrix_manifest: Path,
    *,
    connector_root: Path,
    run_id: str,
    errors: list[str],
) -> dict[str, dict[str, Any]]:
    expected_ids = expected_full_matrix_job_ids()
    raw_rows: dict[str, dict[str, Any]] = {}
    for row in read_jsonl_objects(matrix_manifest, errors, connector_root, root=matrix_manifest.parent):
        connector = str(row.get("connector") or "")
        crs = str(row.get("test_variant") or "")
        mrts = str(row.get("mrts_variant") or "")
        job_id = str(row.get("job_id") or "")
        if job_id != f"{connector}:{crs}:{mrts}" or job_id not in expected_ids:
            errors.append(f"{rel(matrix_manifest, connector_root)}: raw matrix record has invalid job identity {job_id or '<missing>'}")
            continue
        if row.get("verified_run_id") != run_id:
            errors.append(f"{rel(matrix_manifest, connector_root)}: {job_id} verified_run_id mismatch")
        if job_id in raw_rows:
            errors.append(f"{rel(matrix_manifest, connector_root)}: duplicate raw matrix job {job_id}")
            continue
        raw_rows[job_id] = row
    return raw_rows


def check_raw_matrix_completeness(
    raw_rows: dict[str, dict[str, Any]],
    *,
    matrix_manifest: Path,
    connector_root: Path,
    verified_manifest: dict[str, Any],
    manifest_path: Path,
    errors: list[str],
) -> None:
    expected_ids = expected_full_matrix_job_ids()
    if set(raw_rows) != expected_ids:
        missing = sorted(expected_ids - set(raw_rows))
        detail = ", ".join(missing) if missing else "invalid or duplicate records"
        errors.append(f"{rel(matrix_manifest, connector_root)}: full runtime matrix is incomplete: {detail}")
    completeness = verified_manifest.get("full_matrix_job_completeness")
    if not isinstance(completeness, dict) or completeness.get("complete_jobs") != len(expected_ids) or completeness.get("missing_jobs") not in ([], None):
        errors.append(f"{rel(manifest_path, connector_root)}: derived full-matrix completeness does not match the required raw job set")


def check_job_identity_and_state(job: dict[str, Any], *, job_id: str, connector: str, crs: str, mrts: str, run_id: str, errors: list[str]) -> None:
    for key, expected in (("connector", connector), ("job_id", job_id), ("verified_run_id", run_id), ("test_variant", crs), ("mrts_variant", mrts)):
        if job.get(key) != expected:
            errors.append(f"{job_id}: {key} mismatch")
    if job.get("status") not in {"completed", "completed_with_mismatches"}:
        errors.append(f"{job_id}: status is not a completed runtime state")
    if not isinstance(job.get("return_code"), int) or isinstance(job.get("return_code"), bool):
        errors.append(f"{job_id}: return_code is missing or invalid")
    for key in ("started_at", "ended_at"):
        if not isinstance(job.get(key), str) or not job.get(key):
            errors.append(f"{job_id}: missing {key}")
    duration = job.get("duration_seconds")
    if not isinstance(duration, (int, float)) or isinstance(duration, bool) or duration < 0:
        errors.append(f"{job_id}: duration_seconds is missing or invalid")


def expected_summary_path(job: dict[str, Any], *, job_id: str, results_dir: Path, errors: list[str]) -> Path:
    candidates = (results_dir / f"{job_id.split(':', 1)[0]}-summary.json", results_dir / "force-all" / f"{job_id.split(':', 1)[0]}-summary.json")
    candidate = Path(str(job.get("summary_path") or ""))
    if candidate.is_absolute() and any(candidate.absolute() == path.absolute() for path in candidates):
        return candidate
    errors.append(f"{job_id}: summary path is not canonical")
    return candidates[-1]


def check_job_artifacts(
    job: dict[str, Any],
    *,
    job_id: str,
    connector: str,
    job_root: Path,
    connector_root: Path,
    errors: list[str],
) -> tuple[Path, Path]:
    results_dir = job_root / "results"
    if not exact_canonical_path(job.get("results_dir"), results_dir) or not is_within(results_dir, job_root) or has_symlink_component(results_dir, job_root) or not results_dir.is_dir() or results_dir.is_symlink():
        errors.append(f"{job_id}: results_dir is not canonical")
    hashes = job.get("hashes") if isinstance(job.get("hashes"), dict) else {}
    outputs = job.get("outputs") if isinstance(job.get("outputs"), dict) else {}
    inputs = job.get("inputs") if isinstance(job.get("inputs"), dict) else {}
    paths = (
        ("log", job_root / "run.log", job.get("log_path"), hashes.get("log")),
        ("build_manifest", job_root / "build-manifest.json", inputs.get("build_manifest"), hashes.get("build_manifest")),
        ("summary", expected_summary_path(job, job_id=job_id, results_dir=results_dir, errors=errors), outputs.get("summary"), hashes.get("summary")),
        ("results_jsonl", results_dir / "force-all" / f"{connector}-results.jsonl", outputs.get("results_jsonl"), hashes.get("results_jsonl")),
    )
    for label, path, declared_path, declared_hash in paths:
        check_job_artifact(job_id=job_id, label=label, expected_path=path, declared_path=declared_path, declared_hash=declared_hash, job_root=job_root, errors=errors, connector_root=connector_root)
    expected_outputs = (("job_json", job_root / "job.json"), ("log", job_root / "run.log"), ("results_dir", results_dir))
    for label, path in expected_outputs:
        if not exact_canonical_path(outputs.get(label), path):
            errors.append(f"{job_id}: {label} output path is not canonical")
    return paths[2][1], paths[3][1]


def check_job_result_content(summary_path: Path, results_jsonl_path: Path, *, job_id: str, connector: str, job_root: Path, connector_root: Path, errors: list[str]) -> None:
    summary = load_json(summary_path, errors, connector_root, root=job_root) if is_regular_file(summary_path, root=job_root) else {}
    connector_summary = summary.get(connector) if isinstance(summary.get(connector), dict) else {}
    if not isinstance(connector_summary.get("cases"), dict) or not connector_summary.get("cases"):
        errors.append(f"{job_id}: summary lacks structured connector cases")
    rows = read_jsonl_objects(results_jsonl_path, errors, connector_root, root=job_root) if is_regular_file(results_jsonl_path, root=job_root) else []
    if not rows:
        errors.append(f"{job_id}: results_jsonl lacks structured result records")


def check_raw_job_consistency(raw: dict[str, Any] | None, job: dict[str, Any], *, job_id: str, errors: list[str]) -> None:
    if raw is None:
        return
    for key in ("connector", "job_id", "verified_run_id", "test_variant", "mrts_variant", "return_code", "status", "hashes", "inputs", "outputs"):
        if raw.get(key) != job.get(key):
            errors.append(f"{job_id}: raw matrix {key} does not match job receipt")


def check_matrix_job(
    *,
    job_id: str,
    connector: str,
    crs: str,
    mrts: str,
    matrix_root: Path,
    connector_root: Path,
    build_root: Path,
    run_id: str,
    raw: dict[str, Any] | None,
    errors: list[str],
) -> None:
    job_root = matrix_root / crs / mrts / connector
    job_path = job_root / "job.json"
    if not is_regular_file(job_path, root=build_root):
        errors.append(f"{job_id}: job receipt is missing or not regular")
        return
    job = load_json(job_path, errors, connector_root, root=build_root)
    check_job_identity_and_state(job, job_id=job_id, connector=connector, crs=crs, mrts=mrts, run_id=run_id, errors=errors)
    summary_path, results_jsonl_path = check_job_artifacts(job, job_id=job_id, connector=connector, job_root=job_root, connector_root=connector_root, errors=errors)
    check_job_result_content(summary_path, results_jsonl_path, job_id=job_id, connector=connector, job_root=job_root, connector_root=connector_root, errors=errors)
    check_raw_job_consistency(raw, job, job_id=job_id, errors=errors)


def check_verified_runtime_artifact_chain(
    connector_root: Path,
    errors: list[str],
    *,
    build_root: Path | None = None,
) -> None:
    """Validate detached full-matrix receipts rather than derived report claims."""
    manifest_path = report_path(connector_root, "verified_run_manifest", "json")
    if not is_regular_file(manifest_path, root=connector_root):
        errors.append(f"{rel(manifest_path, connector_root)}: verified run manifest is missing or not regular")
        return
    verified_manifest = load_json(manifest_path, errors, connector_root)
    run_id = str(verified_manifest.get("verified_run_id") or "")
    if not VERIFIED_RUN_ID_PATTERN.fullmatch(run_id):
        errors.append(f"{rel(manifest_path, connector_root)}: verified_run_id is invalid")
        return
    if verified_manifest.get("profile") != "full":
        errors.append(f"{rel(manifest_path, connector_root)}: verified run profile is not full")
        return
    selected_build_root = (build_root or Path(verified_runtime_paths()["BUILD_ROOT"])).absolute()
    check_verified_command_receipt(verified_manifest, manifest_path=manifest_path, connector_root=connector_root, build_root=selected_build_root, run_id=run_id, errors=errors)
    matrix_root = selected_build_root / "full-matrix"
    matrix_manifest = matrix_root / "full-runtime-matrix-runs.jsonl"
    if not is_regular_file(matrix_manifest, root=selected_build_root):
        errors.append(f"{rel(matrix_manifest, connector_root)}: full runtime matrix manifest is missing or not regular")
        return
    raw_rows = read_raw_matrix_rows(matrix_manifest, connector_root=connector_root, run_id=run_id, errors=errors)
    check_raw_matrix_completeness(raw_rows, matrix_manifest=matrix_manifest, connector_root=connector_root, verified_manifest=verified_manifest, manifest_path=manifest_path, errors=errors)
    for job_id, connector, crs, mrts in expected_full_matrix_jobs():
        check_matrix_job(job_id=job_id, connector=connector, crs=crs, mrts=mrts, matrix_root=matrix_root, connector_root=connector_root, build_root=selected_build_root, run_id=run_id, raw=raw_rows.get(job_id), errors=errors)


def check_verified_runtime_diagnostics(connector_root: Path, errors: list[str], *, strict_evidence: bool) -> None:
    if not strict_evidence:
        return
    dashboard_path = report_path(connector_root, "merge_readiness_dashboard", "json")
    mismatch_path = report_path(connector_root, "verified_runtime_mismatch_analysis", "json")
    if not dashboard_path.is_file() or not mismatch_path.is_file():
        return
    dashboard = load_json(dashboard_path, errors, connector_root)
    mismatch = load_json(mismatch_path, errors, connector_root)
    full_matrix = mismatch.get("full_matrix") if isinstance(mismatch.get("full_matrix"), dict) else {}
    runtime_complete = bool(full_matrix.get("complete"))
    refresh_timeout = bool(dashboard.get("full_matrix_refresh_timeout") or full_matrix.get("refresh_timeout"))
    critical_mismatches = int(mismatch.get("critical_mismatch_count") or dashboard.get("critical_runtime_mismatch_count") or 0)
    stale_reports = dashboard.get("stale_reports") if isinstance(dashboard.get("stale_reports"), list) else []
    if runtime_complete and stale_reports:
        errors.append(
            "critical runtime evidence exists but downstream reports are stale: "
            + ", ".join(str(item) for item in stale_reports)
        )
    if runtime_complete and refresh_timeout:
        errors.append("refresh timeout after runtime completed; merge dashboard cannot PASS until downstream reports are fresh")
    if runtime_complete and critical_mismatches:
        errors.append(f"full-matrix critical mismatches detected: {critical_mismatches}; merge dashboard cannot PASS")
    if not runtime_complete and mismatch:
        completed = full_matrix.get("completed_jobs", "unknown")
        expected = full_matrix.get("expected_jobs", "unknown")
        missing = full_matrix.get("missing_jobs") if isinstance(full_matrix.get("missing_jobs"), list) else []
        errors.append(
            f"full-matrix incomplete: {completed}/{expected} jobs complete; missing jobs: "
            + (", ".join(str(item) for item in missing) if missing else "unknown")
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector-root", default=".")
    parser.add_argument("--framework-root", default=None)
    parser.add_argument(
        "--governance-only",
        action="store_true",
        help="Validate generated-report layout, metadata, registry paths, URL policy, and runtime path governance without enforcing full verified runtime evidence freshness or mismatch gates.",
    )
    args = parser.parse_args()

    connector_root = Path(args.connector_root).resolve()
    framework_root = Path(args.framework_root).resolve() if args.framework_root else connector_root / "modules/ModSecurity-test-Framework"
    if str(connector_root / "ci") not in sys.path:
        sys.path.insert(0, str(connector_root / "ci"))

    errors: list[str] = []
    check_registry_paths(connector_root, errors)
    check_no_flat_reports(connector_root, errors)
    check_no_orphan_generated_reports(connector_root, errors)
    strict_evidence = not args.governance_only

    check_manifest(
        connector_root,
        errors,
        strict_evidence=strict_evidence,
        framework_root=framework_root,
    )
    check_existing_generated_reports(connector_root, errors)
    check_generated_markdown_portability(connector_root, errors)
    check_critical_report_run_consistency(
        connector_root,
        errors,
        strict_evidence=strict_evidence,
        framework_root=framework_root,
    )
    if strict_evidence:
        check_verified_runtime_artifact_chain(connector_root, errors)
    check_verified_runtime_diagnostics(connector_root, errors, strict_evidence=strict_evidence)
    check_system_environment_proof(connector_root, errors)
    check_no_legacy_references(connector_root, errors)
    check_no_flat_generator_writes(connector_root, framework_root, errors)
    check_no_runtime_source_url_hardcoding(connector_root, errors)
    check_no_insecure_repo_url_literals(connector_root, framework_root, errors)

    if errors:
        print("check-generated-report-layout: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("check-generated-report-layout: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
