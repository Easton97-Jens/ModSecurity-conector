#!/usr/bin/env python3
"""Write the complete interim connector coverage view to GitHub's summary."""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

CONNECTORS = ("apache", "envoy", "haproxy", "lighttpd", "nginx", "traefik")
PROFILES = ("no-crs-no-mrts", "no-crs-with-mrts", "with-crs-no-mrts", "with-crs-with-mrts")
CASE_STATUSES = frozenset(("PASS", "FAIL", "BLOCKED", "UNSUPPORTED", "NOT_EXECUTED", "NOT_APPLICABLE"))
FRAMEWORK_SELECTOR = Path("ci/checks/catalog/no_crs_baseline.py")
SAFE_WRITER = Path(__file__).resolve().with_name("summarize-with-crs-no-mrts-workflow.py")
MAX_SUMMARY_VALUE_LENGTH = 280
FULL_RUNTIME_CONNECTORS = frozenset(("apache", "haproxy"))
LIMITED_ROUTE_CONNECTORS = frozenset(("envoy", "lighttpd", "traefik"))


def _escape(value: object) -> str:
    escaped = str(value).replace("|", "\\|").replace("\n", " ").replace("\r", " ").replace("`", "\\`")
    if len(escaped) <= MAX_SUMMARY_VALUE_LENGTH:
        return escaped
    return f"{escaped[:MAX_SUMMARY_VALUE_LENGTH - 3]}..."


def _json_file(path: Path, label: str) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"{label} must be a regular file")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"{label} is not valid JSON") from error
    if not isinstance(payload, dict):
        raise ValueError(f"{label} root must be an object")
    return payload


def load_framework_selector(framework_root: Path) -> Any:
    if not framework_root.is_dir() or framework_root.is_symlink():
        raise ValueError("Framework root must be a real directory")
    root = framework_root.resolve()
    selector_path = (root / FRAMEWORK_SELECTOR).resolve()
    if not selector_path.is_file() or not selector_path.is_relative_to(root):
        raise ValueError("framework selector is outside the declared Framework root")
    spec = importlib.util.spec_from_file_location("connector_framework_case_selector", selector_path)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load the canonical Framework selector")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not callable(getattr(module, "load_catalog", None)) or not callable(getattr(module, "select_cases", None)):
        raise ValueError("Framework selector does not expose its canonical selection API")
    return module


def select_framework_cases(framework_root: Path, connector: str, capabilities_path: Path) -> dict[str, Any]:
    if connector not in CONNECTORS:
        raise ValueError("connector is outside the fixed connector set")
    if not capabilities_path.is_file() or capabilities_path.is_symlink():
        raise ValueError("connector capability manifest must be a regular file")
    selector = load_framework_selector(framework_root)
    manifest = selector.load_capability_manifest(capabilities_path, connector)
    selected = selector.select_cases(connector, manifest, selector.load_catalog(), "no_crs_baseline")
    if not isinstance(selected.get("cases"), list) or not selected["cases"]:
        raise ValueError("Framework selector returned no cases")
    return selected


def _validate_evidence_header(result: Mapping[str, Any], connector: str) -> None:
    expected = {
        "connector": connector,
        "evidence_stage": "no_crs_baseline",
        "ruleset": "no-crs-baseline",
    }
    for field, value in expected.items():
        if result.get(field) != value:
            raise ValueError(f"result.json {field} does not match the canonical No-CRS profile")


def _selection_by_case_id(plan: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    cases = plan.get("cases")
    if not isinstance(cases, list):
        raise ValueError("plan cases must be a list")
    selections: dict[str, Mapping[str, Any]] = {}
    for selection in cases:
        if not isinstance(selection, Mapping):
            raise ValueError("plan case must be an object")
        case_id = str(selection.get("case_id") or "")
        if not case_id or case_id in selections:
            raise ValueError("plan case identifiers must be unique")
        selections[case_id] = selection
    return selections


def _parse_evidence_line(line: str, index: int) -> Mapping[str, Any]:
    try:
        record = json.loads(line)
    except json.JSONDecodeError as error:
        raise ValueError("results.jsonl contains invalid JSON") from error
    if not isinstance(record, Mapping):
        raise ValueError(f"results.jsonl record {index} must be an object")
    return record


def _validate_evidence_record(
    record: Mapping[str, Any], index: int, selections: Mapping[str, Mapping[str, Any]],
    connector: str, records: Mapping[str, Mapping[str, Any]],
) -> str:
    case_id = str(record.get("case_id") or "")
    selection = selections.get(case_id)
    if not case_id or selection is None:
        raise ValueError(f"results.jsonl record {index} is outside the canonical case plan")
    if case_id in records:
        raise ValueError(f"results.jsonl contains duplicate case_id {case_id}")
    if record.get("connector") != connector:
        raise ValueError(f"results.jsonl record {index} connector does not match the workflow cell")
    if str(record.get("phase")) != str(selection.get("phase")):
        raise ValueError(f"results.jsonl record {index} phase does not match the canonical plan")
    if str(record.get("group") or "") != str(selection.get("group") or ""):
        raise ValueError(f"results.jsonl record {index} area does not match the canonical plan")
    status = str(record.get("status") or "").upper()
    if status not in CASE_STATUSES:
        raise ValueError(f"results.jsonl record {index} contains an invalid case status")
    return case_id


def _records_from_evidence(
    evidence_dir: Path, plan: Mapping[str, Any], connector: str,
) -> dict[str, Mapping[str, Any]]:
    if not evidence_dir.is_dir() or evidence_dir.is_symlink():
        raise ValueError("evidence directory must be a real directory")
    selections = _selection_by_case_id(plan)
    records: dict[str, Mapping[str, Any]] = {}
    result_path = evidence_dir / "result.json"
    result = _json_file(result_path, "result.json")
    _validate_evidence_header(result, connector)
    jsonl_path = evidence_dir / "results.jsonl"
    if not jsonl_path.is_file() or jsonl_path.is_symlink():
        raise ValueError("results.jsonl must be a regular file")
    for index, line in enumerate(jsonl_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        record = _parse_evidence_line(line, index)
        case_id = _validate_evidence_record(record, index, selections, connector, records)
        records[case_id] = record
    return records


def _case_status_and_details(
    selection: Mapping[str, Any], evidence: Mapping[str, Any] | None,
) -> tuple[str, str, str]:
    selected = str(selection.get("selection_status") or "")
    selection_reason = str(selection.get("selection_reason") or "")
    if selected in ("UNSUPPORTED", "NOT_APPLICABLE", "NOT_EXECUTED"):
        return selected, "catalog selection", selection_reason or "The canonical capability selection excludes this case."
    if selected != "SELECTED":
        raise ValueError("Framework selector returned an invalid selection status")
    if not isinstance(evidence, Mapping):
        return "NOT_EXECUTED", "no validated result", "No validated canonical case result was available."
    status = str(evidence.get("status") or "").upper()
    if status not in CASE_STATUSES:
        raise ValueError("result contains an invalid case status")
    if status == "PASS" and evidence.get("live_executed") is not True:
        return "NOT_EXECUTED", "validated results.jsonl", "PASS was not backed by live_executed=true."
    return status, "validated results.jsonl", str(evidence.get("reason") or "Canonical validated case result.")


def case_rows(plan: Mapping[str, Any], evidence: Mapping[str, Mapping[str, Any]] | None = None) -> list[dict[str, str]]:
    cases = _selection_by_case_id(plan)
    evidence = evidence or {}
    rows = []
    for case_id, selection in cases.items():
        status, evidence_source, reason = _case_status_and_details(selection, evidence.get(case_id))
        rows.append({
            "case_id": case_id,
            "phase": str(selection.get("phase") or "unknown"),
            "area": str(selection.get("group") or "ungrouped"),
            "status": status,
            "evidence": evidence_source,
            "reason": reason,
        })
    return rows


def route_inventory() -> list[dict[str, str]]:
    rows = []
    for connector in CONNECTORS:
        for profile in PROFILES:
            rows.append({"connector": connector, "profile": profile, "state": route_state(connector, profile)})
    return rows


def route_state(connector: str, profile: str) -> str:
    if connector == "nginx":
        return "PROTECTED_SEPARATE"
    if connector in FULL_RUNTIME_CONNECTORS:
        return "RUNTIME_ROUTE"
    if connector not in LIMITED_ROUTE_CONNECTORS or profile not in PROFILES:
        raise ValueError("connector/profile is outside the fixed route inventory")
    if profile in ("no-crs-no-mrts", "with-crs-no-mrts"):
        return "RUNTIME_ROUTE"
    return "EXPECTED_UNSUPPORTED"


def render_summary(
    plan: Mapping[str, Any], evidence: Mapping[str, Mapping[str, Any]] | None = None,
    *, coverage_kind: str = "runtime", crs: str = "", mrts: str = "",
    evidence_validation_outcome: str = "not_run",
) -> str:
    rows = case_rows(plan, evidence)
    counts = Counter(row["status"] for row in rows)
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(row["phase"], row["area"])].append(row)
    output = ["## Connector mode coverage (interim)", "", f"Connector: `{_escape(plan.get('connector', 'unknown'))}`; coverage: `{_escape(coverage_kind)}`; CRS: `{_escape(crs)}`; MRTS: `{_escape(mrts)}`", f"Canonical evidence validation: `{_escape(evidence_validation_outcome)}`.", "", "| Status | Count |", "| --- | ---: |"]
    output.extend(f"| {_escape(status)} | `{counts.get(status, 0)}` |" for status in sorted(CASE_STATUSES))
    output.extend(("", "### Connector/profile routes", "", "This inventory lists the current workflow route, not a per-case execution result.", "", "| Connector | Profile | Route state |", "| --- | --- | --- |"))
    output.extend(f"| {_escape(row['connector'])} | {_escape(row['profile'])} | {_escape(row['state'])} |" for row in route_inventory())
    output.extend(("", "### Framework cases by phase and area", "", "| Phase | Area | Case | Status | Evidence | Reason |", "| --- | --- | --- | --- | --- | --- |"))
    for key in sorted(grouped, key=lambda item: (int(item[0]) if item[0].isdigit() else 999, item[1])):
        for row in sorted(grouped[key], key=lambda item: item["case_id"]):
            output.append(f"| {_escape(row['phase'])} | {_escape(row['area'])} | {_escape(row['case_id'])} | {_escape(row['status'])} | {_escape(row['evidence'])} | {_escape(row['reason'])} |")
    output.append("\nSelection is not execution. PASS requires live_executed=true; missing or unvalidated evidence remains NOT_EXECUTED. The complete No-CRS catalogue is an inventory for CRS/MRTS profiles until their dedicated runtime evidence exists.")
    return "\n".join(output) + "\n"


def append_github_step_summary(environment: Mapping[str, str], content: str) -> None:
    if not SAFE_WRITER.is_file() or SAFE_WRITER.is_symlink():
        raise ValueError("existing safe GitHub Step Summary writer is unavailable")
    spec = importlib.util.spec_from_file_location("connector_safe_step_summary_writer", SAFE_WRITER)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load the existing safe GitHub Step Summary writer")
    writer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(writer)
    writer.append_github_step_summary(environment, content)


def main(arguments: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector", required=True, choices=CONNECTORS)
    parser.add_argument("--crs", required=True, choices=("no-crs", "with-crs"))
    parser.add_argument("--mrts", required=True, choices=("no-mrts", "with-mrts"))
    parser.add_argument("--coverage-kind", required=True, choices=("runtime", "contract", "inventory", "expected_unsupported"))
    parser.add_argument("--connector-root", required=True, type=Path)
    parser.add_argument("--framework-root", required=True, type=Path)
    parser.add_argument("--evidence-dir", type=Path)
    parser.add_argument("--evidence-validation-outcome", required=True, choices=("success", "failure", "skipped", "cancelled", "not_run"))
    args = parser.parse_args(arguments)
    try:
        if not args.connector_root.is_dir() or args.connector_root.is_symlink():
            raise ValueError("connector root must be a real directory")
        connector_root = args.connector_root.resolve()
        capabilities = connector_root / "connectors" / args.connector / "capabilities.json"
        if capabilities.is_symlink() or not capabilities.resolve().is_relative_to(connector_root):
            raise ValueError("connector capability manifest is outside connector root")
        plan = select_framework_cases(args.framework_root, args.connector, capabilities)
        evidence = None
        if args.evidence_dir and args.evidence_validation_outcome == "success":
            if (args.crs, args.mrts, args.coverage_kind) != ("no-crs", "no-mrts", "runtime"):
                raise ValueError("canonical No-CRS evidence is only valid for the no-crs/no-mrts runtime cell")
            evidence = _records_from_evidence(args.evidence_dir, plan, args.connector)
        append_github_step_summary(
            os.environ,
            render_summary(
                plan,
                evidence,
                coverage_kind=args.coverage_kind,
                crs=args.crs,
                mrts=args.mrts,
                evidence_validation_outcome=args.evidence_validation_outcome,
            ),
        )
    except (OSError, ValueError) as error:
        print(f"FAIL: {error}", file=os.sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
