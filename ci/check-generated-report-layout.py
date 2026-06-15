#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from generated_report_utils import (
    FILENAME_TO_KEY,
    GENERATED_NOTICE,
    GENERATED_REPORTS,
    GENERATED_ROOT,
    report_relpath,
    report_path,
)

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


def load_json(path: Path, errors: list[str], connector_root: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{rel(path, connector_root)}: invalid JSON: {exc}")
        return {}
    if not isinstance(data, dict):
        errors.append(f"{rel(path, connector_root)}: JSON root must be an object")
        return {}
    return data


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
        "schema_version",
    )
    for key in required:
        if key not in metadata:
            errors.append(f"{rel(path, connector_root)}: metadata.{key} is missing")
    if metadata.get("generated_notice") != GENERATED_NOTICE:
        errors.append(f"{rel(path, connector_root)}: metadata.generated_notice is not canonical")
    if not isinstance(metadata.get("inputs"), list):
        errors.append(f"{rel(path, connector_root)}: metadata.inputs must be a list")


def check_markdown_metadata(path: Path, errors: list[str], connector_root: Path) -> None:
    text = path.read_text(encoding="utf-8", errors="replace")
    first_lines = text.splitlines()[:12]
    if not first_lines or first_lines[0].strip() != f"> {GENERATED_NOTICE}":
        errors.append(f"{rel(path, connector_root)}: missing generated notice at top")
    if not any("Generated at:" in line for line in first_lines):
        errors.append(f"{rel(path, connector_root)}: missing visible generated timestamp")
    if "## Data Availability / Missing Information" not in text:
        errors.append(f"{rel(path, connector_root)}: missing data availability section")


def check_existing_generated_reports(connector_root: Path, errors: list[str]) -> None:
    generated_root = connector_root / GENERATED_ROOT
    for path in sorted(generated_root.rglob("*.generated.*")):
        if path.suffix == ".json":
            check_json_metadata(path, errors, connector_root)
        elif path.suffix == ".md":
            check_markdown_metadata(path, errors, connector_root)


def check_no_flat_reports(connector_root: Path, errors: list[str]) -> None:
    generated_root = connector_root / GENERATED_ROOT
    for path in sorted(generated_root.glob("*.generated.*")):
        if path.exists():
            errors.append(f"{rel(path, connector_root)}: stale flat generated report remains")


def check_manifest(connector_root: Path, errors: list[str]) -> None:
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


def check_system_environment_proof(connector_root: Path, errors: list[str]) -> None:
    md_path = report_path(connector_root, "system_environment_proof", "md")
    json_path = report_path(connector_root, "system_environment_proof", "json")
    if md_path.is_file():
        text = md_path.read_text(encoding="utf-8", errors="replace")
        if "## Framework Environment Resolution" not in text:
            errors.append(f"{rel(md_path, connector_root)}: missing Framework Environment Resolution section")
        if "## Runtime Component Readiness" not in text:
            errors.append(f"{rel(md_path, connector_root)}: missing Runtime Component Readiness section")
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
        if path.name.startswith("report-path-migration.generated.") or path.name.startswith("system-environment-proof.generated."):
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
    path = connector_root / "ci/prepare-runtime-components.py"
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
        resolved = str(path.resolve(strict=False))
        if path.name not in FILENAME_TO_KEY:
            errors.append(f"{rel(path, connector_root)}: generated file is not in registry")
        elif resolved not in expected:
            errors.append(f"{rel(path, connector_root)}: generated file is not at registry path")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector-root", default=".")
    parser.add_argument("--framework-root", default=None)
    args = parser.parse_args()

    connector_root = Path(args.connector_root).resolve()
    framework_root = Path(args.framework_root).resolve() if args.framework_root else connector_root / "modules/ModSecurity-test-Framework"
    if str(connector_root / "ci") not in sys.path:
        sys.path.insert(0, str(connector_root / "ci"))

    errors: list[str] = []
    check_registry_paths(connector_root, errors)
    check_no_flat_reports(connector_root, errors)
    check_no_orphan_generated_reports(connector_root, errors)
    check_manifest(connector_root, errors)
    check_existing_generated_reports(connector_root, errors)
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
