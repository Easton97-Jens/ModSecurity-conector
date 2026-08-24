#!/usr/bin/env python3
"""Render bounded, Framework-derived connector scenario coverage.

The renderer deliberately separates Framework selection, host execution and
evidence validation. It reads only canonical Framework plans and validated,
cell-bound evidence; a GitHub step outcome alone cannot create a ``RUN`` or
``PASS`` claim.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import importlib.util
import json
import os
import re
from collections import Counter
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any


CONNECTORS = ("apache", "envoy", "haproxy", "lighttpd", "nginx", "traefik")
PROFILES = (
    "no-crs-no-mrts",
    "no-crs-with-mrts",
    "with-crs-no-mrts",
    "with-crs-with-mrts",
)
FRAMEWORK_SELECTOR = Path("ci/checks/catalog/no_crs_baseline.py")
FRAMEWORK_CRS_CONTRACT = Path(
    "ci/checks/catalog/five_connectors_with_crs_no_mrts.py"
)
DISPLAY_INDEX = (
    Path(__file__).resolve().parents[1]
    / "scenarios"
    / "framework-display-index.json"
)
SAFE_RUNTIME_READER = Path(__file__).resolve().with_name(
    "summarize-with-crs-no-mrts-workflow.py"
)

RAW_CASE_STATUSES = frozenset(
    ("PASS", "FAIL", "BLOCKED", "UNSUPPORTED", "NOT_EXECUTED", "NOT_APPLICABLE")
)
CASE_STATUSES = frozenset(
    ("PASS", "FAIL", "UNSUPPORTED", "NOT_EXECUTED", "NOT_APPLICABLE", "CANCELLED")
)
WORKFLOW_OUTCOMES = frozenset(
    ("success", "failure", "skipped", "cancelled", "not_applicable", "not_run")
)
FULL_RUNTIME_CONNECTORS = frozenset(("apache", "haproxy"))
LIMITED_ROUTE_CONNECTORS = frozenset(("envoy", "lighttpd", "traefik"))
NO_CRS_PROFILE = "no-crs-no-mrts"
CRS_PROFILE = "with-crs-no-mrts"
CRS_FRAMEWORK_PROFILE = "five-connectors-with-crs-no-mrts"
CONTRACT_VALIDATED = "CONTRACT_VALIDATED"
MAX_SUMMARY_VALUE_LENGTH = 280
MAX_INDEX_BYTES = 64 * 1024
RESULT_FILE_NAME = "result.json"
RUN_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,47}$", re.ASCII)
COMMIT = re.compile(r"^[0-9a-f]{40}$", re.ASCII)
FRAMEWORK_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,127}$", re.ASCII)
ABSOLUTE_PATH_FRAGMENT = re.compile(
    r"(?<![A-Za-z0-9_.-])/[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)+"
)
SENSITIVE_SUMMARY_FRAGMENT = re.compile(
    r"\b(?:authorization|bearer|cookie|password|payload|secret|token)\b",
    re.IGNORECASE,
)
LABEL_FRAMEWORK_CRS_RESULT = "Framework CRS result"
LABEL_FRAMEWORK_CRS_MANIFEST = "Framework CRS manifest"
LABEL_FRAMEWORK_CRS_RECEIPT = "Framework CRS receipt"
LABEL_NORMALIZED_RUNTIME_EVENT = "normalized runtime event"
LABEL_RUNTIME_ATTESTATION = "runtime attestation"
LABEL_NORMALIZED_HOST_CONFIGURATION = "normalized host configuration"
LABEL_NORMALIZED_CLEANUP = "normalized cleanup"
LABEL_VALIDATED_FRAMEWORK_RESULT = "validated Framework result"
NOT_REPORTED = "not reported"
NOT_RUN = "NOT RUN"
NOT_APPLICABLE = "NOT APPLICABLE"


def _escape(value: object) -> str:
    """Escape one bounded dynamic value for a Markdown table cell."""
    raw = str(value)
    raw = "".join(
        character if character >= " " and character != "\x7f" else " "
        for character in raw
    )
    # The renderer only needs short labels and fixed technical tokens.  Redact
    # path-like and sensitive free-text fragments at the final output sink as
    # defense in depth should an otherwise validated metadata field be hostile.
    raw = ABSOLUTE_PATH_FRAGMENT.sub("[redacted path]", raw)
    raw = SENSITIVE_SUMMARY_FRAGMENT.sub("[redacted]", raw)
    escaped = html.escape(raw, quote=True)
    escaped = escaped.replace("|", "\\|").replace("`", "\\`")
    escaped = escaped.replace("\n", " ").replace("\r", " ")
    if len(escaped) <= MAX_SUMMARY_VALUE_LENGTH:
        return escaped
    return f"{escaped[:MAX_SUMMARY_VALUE_LENGTH - 3]}..."


def _metadata_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value or len(value) > 160:
        raise ValueError(f"{label} must be a bounded non-empty string")
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise ValueError(f"{label} contains a control character")
    return value


def _framework_identifier(value: object, label: str) -> str:
    if not isinstance(value, str) or not FRAMEWORK_IDENTIFIER.fullmatch(value):
        raise ValueError(f"{label} is not a safe Framework identifier")
    return value


def _commit(value: object, label: str) -> str:
    if not isinstance(value, str) or not COMMIT.fullmatch(value):
        raise ValueError(f"{label} is not a full lowercase commit")
    return value


def _run_id(value: object, label: str) -> str:
    if not isinstance(value, str) or not RUN_ID.fullmatch(value):
        raise ValueError(f"{label} is not a safe run ID")
    return value


def _integer(
    value: object, label: str, *, minimum: int = 0, maximum: int = 2**31 - 1
) -> int:
    if (
        not isinstance(value, int)
        or isinstance(value, bool)
        or value < minimum
        or value > maximum
    ):
        raise ValueError(f"{label} is not a bounded integer")
    return value


def _http_status(value: object, label: str) -> int:
    return _integer(value, label, minimum=100, maximum=599)


def _require_mapping(value: object, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be an object")
    return value


def _reject_duplicate_json_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def _json_object(data: bytes, label: str) -> dict[str, Any]:
    try:
        parsed = json.loads(
            data.decode("utf-8", "strict"), object_pairs_hook=_reject_duplicate_json_keys
        )
    except (json.JSONDecodeError, ValueError) as error:
        raise ValueError(f"{label} is not valid JSON") from error
    if not isinstance(parsed, dict):
        raise ValueError(f"{label} root must be an object")
    return parsed


def _load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot load {name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _framework_file(framework_root: Path, relative: Path, label: str) -> Path:
    if not framework_root.is_dir() or framework_root.is_symlink():
        raise ValueError("Framework root must be a real directory")
    root = framework_root.resolve()
    candidate = (root / relative).resolve()
    if not candidate.is_file() or candidate.is_symlink() or not candidate.is_relative_to(root):
        raise ValueError(f"{label} is outside the declared Framework root")
    return candidate


def load_framework_selector(framework_root: Path) -> Any:
    selector_path = _framework_file(framework_root, FRAMEWORK_SELECTOR, "framework selector")
    module = _load_module(selector_path, "connector_framework_case_selector")
    if not callable(getattr(module, "load_catalog", None)) or not callable(
        getattr(module, "select_cases", None)
    ) or not callable(getattr(module, "validate_command", None)):
        raise ValueError("Framework selector does not expose its canonical selection API")
    return module


def _profile(crs: str, mrts: str) -> str:
    profile = f"{crs}-{mrts}"
    if profile not in PROFILES:
        raise ValueError("CRS/MRTS profile is outside the fixed inventory")
    return profile


def _load_display_index(index_path: Path, framework_sha: str) -> dict[str, dict[str, str]]:
    if (
        not index_path.is_file()
        or index_path.is_symlink()
        or index_path.stat().st_size > MAX_INDEX_BYTES
    ):
        raise ValueError("Framework display index is not a bounded regular file")
    index = _json_object(index_path.read_bytes(), "Framework display index")
    if index.get("schema_version") != 1:
        raise ValueError("Framework display index schema version is unsupported")
    if index.get("framework_commit") != framework_sha:
        raise ValueError("Framework display index is not bound to the pinned Framework commit")
    entries = index.get("tests")
    if not isinstance(entries, list) or not entries:
        raise ValueError("Framework display index has no test entries")
    mappings: dict[str, dict[str, str]] = {}
    for position, entry in enumerate(entries, start=1):
        record = _require_mapping(entry, f"Framework display index entry {position}")
        identifier = _framework_identifier(
            record.get("framework_test_id"), f"Framework display index entry {position} ID"
        )
        if identifier in mappings:
            raise ValueError("Framework display index contains duplicate test IDs")
        mappings[identifier] = {
            "display_category": _metadata_text(
                record.get("display_category"),
                f"Framework display index entry {position} category",
            ),
            "display_name": _metadata_text(
                record.get("display_name"),
                f"Framework display index entry {position} name",
            ),
        }
    return mappings


def _select_no_crs_cases(
    framework_root: Path, connector: str, capabilities_path: Path
) -> dict[str, Any]:
    if not capabilities_path.is_file() or capabilities_path.is_symlink():
        raise ValueError("connector capability manifest must be a regular file")
    selector = load_framework_selector(framework_root)
    manifest = selector.load_capability_manifest(capabilities_path, connector)
    selected = selector.select_cases(
        connector, manifest, selector.load_catalog(), "no_crs_baseline"
    )
    if not isinstance(selected, Mapping) or not isinstance(selected.get("cases"), list):
        raise ValueError("Framework selector did not return a canonical case plan")
    if not selected["cases"]:
        raise ValueError("Framework selector returned no cases")
    return {
        **selected,
        "connector": connector,
        "profile": NO_CRS_PROFILE,
        "scenario_contract": "no_crs_baseline",
    }


def _select_crs_cases(
    framework_root: Path,
    connector: str,
    framework_sha: str,
    display_index_path: Path,
) -> dict[str, Any]:
    contract_path = _framework_file(
        framework_root, FRAMEWORK_CRS_CONTRACT, "five-connector CRS contract"
    )
    contract = _load_module(contract_path, "connector_framework_crs_contract")
    required = ("PROFILE", "CONNECTORS", "FIXTURE_ID", "load_fixture")
    if any(not hasattr(contract, field) for field in required):
        raise ValueError("Framework CRS contract is incomplete")
    if contract.PROFILE != CRS_FRAMEWORK_PROFILE or connector not in tuple(contract.CONNECTORS):
        raise ValueError("connector is outside the pinned Framework CRS profile")
    fixture = _require_mapping(contract.load_fixture(), "pinned Framework CRS fixture")
    fixture_id = _framework_identifier(
        fixture.get("fixture_id"), "pinned Framework CRS fixture ID"
    )
    if fixture_id != _framework_identifier(contract.FIXTURE_ID, "Framework CRS contract fixture ID"):
        raise ValueError("Framework CRS fixture does not match the declared contract")
    display_mappings = _load_display_index(display_index_path, framework_sha)
    # The current Framework profile declares exactly one fixture. Requiring an
    # exact index prevents an unverified Parent label from adding scenarios.
    if set(display_mappings) != {fixture_id}:
        raise ValueError("Framework display index does not match the declared scenario profile")
    profile_data = _require_mapping(
        fixture.get("with_crs_no_mrts"), "pinned Framework CRS fixture profile"
    )
    block = _require_mapping(profile_data.get("canonical_block"), "Framework canonical block")
    mapping = display_mappings[fixture_id]
    return {
        "connector": connector,
        "profile": CRS_PROFILE,
        "scenario_contract": CRS_FRAMEWORK_PROFILE,
        "cases": [{
            "case_id": fixture_id,
            "group": mapping["display_category"],
            "display_category": mapping["display_category"],
            "display_name": mapping["display_name"],
            "phase": 2,
            "selection_status": "SELECTED",
            "selection_reason": "Declared by the pinned five-connector Framework profile.",
            "fixture_id": fixture_id,
            "expected_status": _http_status(
                block.get("expected_status"), "Framework canonical block expected status"
            ),
            "expected_rule_id": _integer(
                block.get("expected_rule_id"), "Framework canonical block expected rule ID"
            ),
        }],
    }


def select_framework_cases(
    framework_root: Path,
    connector: str,
    capabilities_path: Path,
    *,
    crs: str = "no-crs",
    mrts: str = "no-mrts",
    framework_sha: str | None = None,
    display_index_path: Path = DISPLAY_INDEX,
) -> dict[str, Any]:
    """Return the actual declared Framework scenario plan for one cell."""
    if connector not in CONNECTORS:
        raise ValueError("connector is outside the fixed connector set")
    profile = _profile(crs, mrts)
    if profile == NO_CRS_PROFILE:
        return _select_no_crs_cases(framework_root, connector, capabilities_path)
    if profile == CRS_PROFILE:
        return _select_crs_cases(
            framework_root,
            connector,
            _commit(framework_sha, "Framework commit"),
            display_index_path,
        )
    # No current Framework fixture/plan declares either MRTS profile. Never
    # reuse a no-MRTS plan for a different cell.
    return {
        "connector": connector,
        "profile": profile,
        "scenario_contract": "not_applicable",
        "cases": [],
    }


def _selection_by_case_id(plan: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    cases = plan.get("cases")
    if not isinstance(cases, list):
        raise ValueError("plan cases must be a list")
    selections: dict[str, Mapping[str, Any]] = {}
    for selection in cases:
        if not isinstance(selection, Mapping):
            raise ValueError("plan case must be an object")
        case_id = _framework_identifier(selection.get("case_id"), "plan case ID")
        if case_id in selections:
            raise ValueError("plan case identifiers must be unique")
        selection_status = str(selection.get("selection_status") or "")
        if selection_status not in {
            "SELECTED", "UNSUPPORTED", "NOT_APPLICABLE", "NOT_EXECUTED"
        }:
            raise ValueError("Framework selector returned an invalid selection status")
        selections[case_id] = selection
    return selections


def _load_safe_runtime_reader() -> Any:
    if not SAFE_RUNTIME_READER.is_file() or SAFE_RUNTIME_READER.is_symlink():
        raise ValueError("existing safe runtime evidence reader is unavailable")
    reader = _load_module(SAFE_RUNTIME_READER, "connector_safe_runtime_evidence_reader")
    required = (
        "_open_directory_without_symlinks",
        "_require_private_evidence_directory",
        "_safe_child_directory",
        "_open_evidence_file",
        "_read_evidence_bytes",
    )
    if any(not callable(getattr(reader, name, None)) for name in required):
        raise ValueError("existing safe runtime evidence reader is incomplete")
    return reader


def _read_private_evidence_bytes(
    evidence_root: Path, components: Sequence[str], label: str
) -> bytes:
    """Use existing descriptor-safe code for a fixed evidence path."""
    if not components:
        raise ValueError("evidence file is unspecified")
    reader = _load_safe_runtime_reader()
    root_descriptor = -1
    directory_descriptor = -1
    file_descriptor = -1
    try:
        root_descriptor = reader._open_directory_without_symlinks(evidence_root)
        reader._require_private_evidence_directory(root_descriptor)
        directory_descriptor = root_descriptor
        for component in components[:-1]:
            next_descriptor = reader._safe_child_directory(directory_descriptor, component)
            if directory_descriptor != root_descriptor:
                os.close(directory_descriptor)
            directory_descriptor = next_descriptor
        file_descriptor = reader._open_evidence_file(
            directory_descriptor, components[-1], label
        )
        return reader._read_evidence_bytes(
            file_descriptor, os.fstat(file_descriptor), label
        )
    finally:
        if file_descriptor >= 0:
            os.close(file_descriptor)
        if directory_descriptor >= 0 and directory_descriptor != root_descriptor:
            os.close(directory_descriptor)
        if root_descriptor >= 0:
            os.close(root_descriptor)


def _read_private_json(
    evidence_root: Path, components: Sequence[str], label: str
) -> tuple[dict[str, Any], str]:
    data = _read_private_evidence_bytes(evidence_root, components, label)
    return _json_object(data, label), hashlib.sha256(data).hexdigest()


def _read_private_jsonl(
    evidence_root: Path, components: Sequence[str], label: str
) -> list[Mapping[str, Any]]:
    data = _read_private_evidence_bytes(evidence_root, components, label)
    try:
        lines = data.decode("utf-8", "strict").splitlines()
    except UnicodeDecodeError as error:
        raise ValueError(f"{label} is not UTF-8") from error
    records: list[Mapping[str, Any]] = []
    for index, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        records.append(_json_object(line.encode("utf-8"), f"{label} record {index}"))
    return records


def _exact(record: Mapping[str, Any], field: str, expected: object, label: str) -> None:
    if record.get(field) != expected:
        raise ValueError(f"{label} {field} does not match the workflow cell")


def _validate_no_crs_header(
    result: Mapping[str, Any], connector: str, run_id: str, parent_sha: str, framework_sha: str
) -> None:
    expected = {
        "connector": connector,
        "run_id": run_id,
        "connector_commit": parent_sha,
        "framework_commit": framework_sha,
        "connector_commit_at_finalize": parent_sha,
        "framework_commit_at_finalize": framework_sha,
        "evidence_stage": "no_crs_baseline",
        "ruleset": "no-crs-baseline",
    }
    for field, value in expected.items():
        _exact(result, field, value, RESULT_FILE_NAME)
    status = str(result.get("status") or "").upper()
    if status not in RAW_CASE_STATUSES:
        raise ValueError("result.json contains an invalid canonical status")


def _validate_no_crs_record(
    record: Mapping[str, Any],
    index: int,
    selections: Mapping[str, Mapping[str, Any]],
    connector: str,
    run_id: str,
    records: Mapping[str, Mapping[str, Any]],
) -> str:
    case_id = _framework_identifier(record.get("case_id"), f"results.jsonl record {index} ID")
    selection = selections.get(case_id)
    if selection is None:
        raise ValueError(f"results.jsonl record {index} is outside the canonical case plan")
    if case_id in records:
        raise ValueError(f"results.jsonl contains duplicate case_id {case_id}")
    _exact(record, "connector", connector, f"results.jsonl record {index}")
    _exact(record, "run_id", run_id, f"results.jsonl record {index}")
    if str(record.get("phase")) != str(selection.get("phase")):
        raise ValueError(f"results.jsonl record {index} phase does not match the canonical plan")
    if str(record.get("group") or "") != str(selection.get("group") or ""):
        raise ValueError(f"results.jsonl record {index} group does not match the canonical plan")
    status = str(record.get("status") or "").upper()
    if status not in RAW_CASE_STATUSES:
        raise ValueError(f"results.jsonl record {index} contains an invalid case status")
    if "live_executed" not in record or not isinstance(record.get("live_executed"), bool):
        raise ValueError(f"results.jsonl record {index} lacks a live-execution flag")
    return case_id


def _no_crs_records_from_evidence(
    evidence_dir: Path,
    plan: Mapping[str, Any],
    connector: str,
    run_id: str,
    parent_sha: str,
    framework_sha: str,
) -> dict[str, Mapping[str, Any]]:
    selections = _selection_by_case_id(plan)
    result, _digest = _read_private_json(evidence_dir, (RESULT_FILE_NAME,), RESULT_FILE_NAME)
    _validate_no_crs_header(result, connector, run_id, parent_sha, framework_sha)
    records: dict[str, Mapping[str, Any]] = {}
    for index, record in enumerate(
        _read_private_jsonl(evidence_dir, ("results.jsonl",), "results.jsonl"), start=1
    ):
        case_id = _validate_no_crs_record(
            record, index, selections, connector, run_id, records
        )
        records[case_id] = record
    selected_ids = {
        case_id
        for case_id, selection in selections.items()
        if selection.get("selection_status") == "SELECTED"
    }
    if selected_ids.difference(records):
        raise ValueError("validated evidence is missing selected Framework case results")
    return {
        case_id: {
            **record,
            "validation_status": "SUCCESS",
            "evidence_kind": "validated canonical Framework result",
        }
        for case_id, record in records.items()
    }


def _validate_no_crs_framework_contract(
    framework_root: Path,
    evidence_dir: Path,
    connector_root: Path,
    capabilities_path: Path,
    connector: str,
    run_id: str,
) -> None:
    """Require a fresh Framework validation, not only a workflow outcome."""
    selector = load_framework_selector(framework_root)
    validation_args = argparse.Namespace(
        evidence_root=str(evidence_dir),
        connector=connector,
        run_id=run_id,
        capabilities=str(capabilities_path),
        connector_root=str(connector_root),
        check="all",
    )
    try:
        validation_exit = selector.validate_command(validation_args)
    except (OSError, ValueError) as error:
        raise ValueError("canonical Framework validation rejected no-CRS evidence") from error
    if validation_exit != 0:
        raise ValueError("canonical Framework validation rejected no-CRS evidence")


def _false(record: Mapping[str, Any], field: str, label: str) -> None:
    if record.get(field) is not False:
        raise ValueError(f"{label} {field} is not false")


def _zero(record: Mapping[str, Any], field: str, label: str) -> None:
    if _integer(record.get(field), f"{label} {field}") != 0:
        raise ValueError(f"{label} {field} is not zero")


def _with_crs_records_from_evidence(
    evidence_root: Path,
    plan: Mapping[str, Any],
    connector: str,
    run_id: str,
    parent_sha: str,
    framework_sha: str,
) -> dict[str, Mapping[str, Any]]:
    selections = _selection_by_case_id(plan)
    if len(selections) != 1:
        raise ValueError("Framework CRS profile does not contain exactly one declared fixture")
    fixture_id, selection = next(iter(selections.items()))
    result, _result_digest = _read_private_json(
        evidence_root, ("results", connector, run_id, "result.json"), LABEL_FRAMEWORK_CRS_RESULT
    )
    manifest, manifest_digest = _read_private_json(
        evidence_root, ("results", connector, run_id, "manifest.json"), LABEL_FRAMEWORK_CRS_MANIFEST
    )
    receipt, receipt_digest = _read_private_json(
        evidence_root, ("results", connector, run_id, "receipt.json"), LABEL_FRAMEWORK_CRS_RECEIPT
    )
    event, _event_digest = _read_private_json(
        evidence_root, ("normalized", connector, run_id, "event.json"), LABEL_NORMALIZED_RUNTIME_EVENT
    )
    runtime, _runtime_digest = _read_private_json(
        evidence_root, ("runtime", connector, run_id, "runtime.json"), LABEL_RUNTIME_ATTESTATION
    )

    for record, label in (
        (result, LABEL_FRAMEWORK_CRS_RESULT),
        (manifest, LABEL_FRAMEWORK_CRS_MANIFEST),
        (receipt, LABEL_FRAMEWORK_CRS_RECEIPT),
    ):
        _exact(record, "connector", connector, label)
        _exact(record, "run_id", run_id, label)
        _exact(record, "profile", CRS_FRAMEWORK_PROFILE, label)
        _exact(record, "validation_status", CONTRACT_VALIDATED, label)
    _exact(result, "status", CONTRACT_VALIDATED, LABEL_FRAMEWORK_CRS_RESULT)
    _exact(manifest, "connector_commit", parent_sha, LABEL_FRAMEWORK_CRS_MANIFEST)
    _exact(manifest, "framework_commit", framework_sha, LABEL_FRAMEWORK_CRS_MANIFEST)
    _exact(receipt, "connector_commit", parent_sha, LABEL_FRAMEWORK_CRS_RECEIPT)
    _exact(receipt, "framework_commit", framework_sha, LABEL_FRAMEWORK_CRS_RECEIPT)
    _exact(manifest, "fixture_id", fixture_id, LABEL_FRAMEWORK_CRS_MANIFEST)
    _exact(receipt, "fixture_id", fixture_id, LABEL_FRAMEWORK_CRS_RECEIPT)
    _exact(result, "manifest_sha256", manifest_digest, LABEL_FRAMEWORK_CRS_RESULT)
    _exact(result, "receipt_sha256", receipt_digest, LABEL_FRAMEWORK_CRS_RESULT)
    _exact(receipt, "manifest_sha256", manifest_digest, LABEL_FRAMEWORK_CRS_RECEIPT)
    for field in ("failure_count", "mismatch_count"):
        _zero(result, field, LABEL_FRAMEWORK_CRS_RESULT)

    for record, label in ((event, LABEL_NORMALIZED_RUNTIME_EVENT), (runtime, LABEL_RUNTIME_ATTESTATION)):
        _exact(record, "connector", connector, label)
        _exact(record, "run_id", run_id, label)
    _exact(event, "profile", CRS_FRAMEWORK_PROFILE, LABEL_NORMALIZED_RUNTIME_EVENT)
    _exact(event, "connector_commit", parent_sha, LABEL_NORMALIZED_RUNTIME_EVENT)
    _exact(event, "framework_commit", framework_sha, LABEL_NORMALIZED_RUNTIME_EVENT)
    _exact(event, "fixture_id", fixture_id, LABEL_NORMALIZED_RUNTIME_EVENT)
    _exact(event, "status", "PASS", LABEL_NORMALIZED_RUNTIME_EVENT)
    _exact(runtime, "record_type", "parent_runtime_attestation", LABEL_RUNTIME_ATTESTATION)
    _exact(runtime, "runtime_status", "PASS", LABEL_RUNTIME_ATTESTATION)
    configuration = _require_mapping(event.get("host_configuration"), LABEL_NORMALIZED_HOST_CONFIGURATION)
    allow = _require_mapping(event.get("allow_case"), "normalized allow case")
    no_mrts = _require_mapping(event.get("no_mrts"), "normalized no-MRTS attestation")
    runtime_no_mrts = _require_mapping(runtime.get("no_mrts"), "runtime no-MRTS attestation")
    cleanup = _require_mapping(event.get("cleanup"), LABEL_NORMALIZED_CLEANUP)
    cleanup_scan = _require_mapping(runtime.get("cleanup_scan"), "runtime cleanup scan")
    _exact(configuration, "config_test_status", "passed", LABEL_NORMALIZED_HOST_CONFIGURATION)
    _exact(configuration, "host_start_status", "passed", LABEL_NORMALIZED_HOST_CONFIGURATION)
    if (
        _http_status(allow.get("expected_status"), "normalized allow expected status") != 200
        or _http_status(allow.get("observed_status"), "normalized allow observed status") != 200
    ):
        raise ValueError("normalized allow case does not prove the canonical live allow request")
    for field, expected in (
        ("expected_status", 403),
        ("observed_status", 403),
        ("expected_rule_id", selection.get("expected_rule_id")),
        ("observed_rule_id", selection.get("expected_rule_id")),
    ):
        if event.get(field) != expected:
            raise ValueError(f"{LABEL_NORMALIZED_RUNTIME_EVENT} {field} does not match the Framework fixture")
    for field in (
        "runner_invoked",
        "case_inventory_loaded",
        "process_started",
        "socket_or_listener_created",
        "artifact_used",
    ):
        _false(no_mrts, field, "normalized no-MRTS attestation")
        _false(runtime_no_mrts, field, "runtime no-MRTS attestation")
    _exact(cleanup, "status", "passed", LABEL_NORMALIZED_CLEANUP)
    for field in (
        "host_processes_remaining",
        "helper_processes_remaining",
        "listeners_remaining",
        "sockets_remaining",
        "pid_files_remaining",
        "runtime_fixtures_remaining",
        "temporary_paths_remaining",
    ):
        _zero(cleanup, field, LABEL_NORMALIZED_CLEANUP)
        _zero(cleanup_scan, field, "runtime cleanup scan")
    request_id = _framework_identifier(event.get("request_id"), "normalized runtime request ID")
    transaction_id = _framework_identifier(
        event.get("transaction_id"), "normalized runtime transaction ID"
    )
    if not request_id or not transaction_id:
        raise ValueError(f"{LABEL_NORMALIZED_RUNTIME_EVENT} lacks request/transaction correlation")
    return {
        fixture_id: {
            "connector": connector,
            "case_id": fixture_id,
            "status": "PASS",
            "live_executed": True,
            "expected_status": 403,
            "observed_status": 403,
            "expected_rule_id": selection.get("expected_rule_id"),
            "observed_rule_id": selection.get("expected_rule_id"),
            "failure_count": 0,
            "mismatch_count": 0,
            "validation_status": CONTRACT_VALIDATED,
            "evidence_kind": f"{LABEL_VALIDATED_FRAMEWORK_RESULT} and {LABEL_NORMALIZED_RUNTIME_EVENT}",
            "fixture_id": fixture_id,
        }
    }


def _records_from_evidence(
    evidence_dir: Path,
    plan: Mapping[str, Any],
    connector: str,
    *,
    run_id: str,
    parent_sha: str,
    framework_sha: str,
) -> dict[str, Mapping[str, Any]]:
    contract = str(plan.get("scenario_contract") or "")
    if contract == "no_crs_baseline":
        return _no_crs_records_from_evidence(
            evidence_dir, plan, connector, run_id, parent_sha, framework_sha
        )
    if contract == CRS_FRAMEWORK_PROFILE:
        return _with_crs_records_from_evidence(
            evidence_dir, plan, connector, run_id, parent_sha, framework_sha
        )
    raise ValueError("the selected Framework profile has no evidence contract")


def _unvalidated_terminal_signal(
    evidence_dir: Path, connector: str
) -> dict[str, str] | None:
    """Return one bounded non-promoting diagnostic from no-CRS evidence."""
    try:
        result, _digest = _read_private_json(
            evidence_dir, (RESULT_FILE_NAME,), RESULT_FILE_NAME
        )
        _exact(result, "connector", connector, RESULT_FILE_NAME)
        status = str(result.get("status") or "").upper()
        if status not in RAW_CASE_STATUSES:
            return None
        return {"status": status}
    except (OSError, ValueError):
        return None


def _scenario_category(selection: Mapping[str, Any]) -> str:
    display_category = selection.get("display_category")
    if display_category is not None:
        return _metadata_text(display_category, "Framework display category")
    group = _framework_identifier(selection.get("group"), "Framework catalog group")
    return f"Framework group: {group}"


def _case_status_and_details(
    selection: Mapping[str, Any],
    evidence: Mapping[str, Any] | None,
    *,
    evidence_validated: bool,
) -> tuple[str, str, str]:
    selection_status = str(selection.get("selection_status") or "")
    if selection_status in ("UNSUPPORTED", "NOT_APPLICABLE", "NOT_EXECUTED"):
        return selection_status, "canonical Framework selection", NOT_REPORTED
    if selection_status != "SELECTED":
        raise ValueError("Framework selector returned an invalid selection status")
    if not evidence_validated or not isinstance(evidence, Mapping):
        return "NOT_EXECUTED", "no validated Framework result", NOT_REPORTED
    status = str(evidence.get("status") or "").upper()
    if status not in RAW_CASE_STATUSES:
        raise ValueError("result contains an invalid case status")
    if status == "PASS":
        if evidence.get("live_executed") is not True:
            return "NOT_EXECUTED", LABEL_VALIDATED_FRAMEWORK_RESULT, NOT_REPORTED
        return "PASS", LABEL_VALIDATED_FRAMEWORK_RESULT, NOT_REPORTED
    if status == "FAIL" and evidence.get("live_executed") is True:
        return "FAIL", LABEL_VALIDATED_FRAMEWORK_RESULT, NOT_REPORTED
    if status in ("UNSUPPORTED", "NOT_APPLICABLE"):
        return status, LABEL_VALIDATED_FRAMEWORK_RESULT, NOT_REPORTED
    return "NOT_EXECUTED", LABEL_VALIDATED_FRAMEWORK_RESULT, NOT_REPORTED


def _optional_http(record: Mapping[str, Any], field: str) -> int | None:
    value = record.get(field)
    if value is None:
        return None
    return _http_status(value, field)


def _optional_rule(record: Mapping[str, Any], field: str) -> int | None:
    value = record.get(field)
    if value is None:
        return None
    return _integer(value, field, minimum=1, maximum=9_999_999)


def case_rows(
    plan: Mapping[str, Any],
    evidence: Mapping[str, Mapping[str, Any]] | None = None,
    *,
    evidence_validated: bool = False,
) -> list[dict[str, Any]]:
    selections = _selection_by_case_id(plan)
    records = evidence or {}
    rows: list[dict[str, Any]] = []
    for case_id, selection in selections.items():
        record = records.get(case_id)
        status, evidence_source, reason = _case_status_and_details(
            selection, record, evidence_validated=evidence_validated
        )
        details: Mapping[str, Any] = record if isinstance(record, Mapping) else selection
        observed_status = _optional_http(details, "observed_status")
        if observed_status is None:
            observed_status = _optional_http(details, "actual_status")
        rows.append({
            "case_id": case_id,
            "category": _scenario_category(selection),
            "display_name": _metadata_text(
                selection.get("display_name", case_id), "Framework display name"
            ),
            "phase": str(selection.get("phase") if selection.get("phase") is not None else "unknown"),
            "area": str(selection.get("group") or "ungrouped"),
            "selection_status": str(selection.get("selection_status")),
            "status": status,
            "live_executed": bool(record.get("live_executed")) if isinstance(record, Mapping) else False,
            "expected_status": _optional_http(details, "expected_status"),
            "observed_status": observed_status,
            "expected_rule_id": _optional_rule(details, "expected_rule_id"),
            "observed_rule_id": _optional_rule(details, "observed_rule_id"),
            "failure_count": _integer(details.get("failure_count", 0), "failure_count"),
            "mismatch_count": _integer(details.get("mismatch_count", 0), "mismatch_count"),
            "validation_status": _metadata_text(
                details.get("validation_status", "not validated"), "validation status"
            ),
            "evidence_kind": _metadata_text(
                details.get("evidence_kind", evidence_source), "evidence kind"
            ),
            "fixture_id": _framework_identifier(details.get("fixture_id", case_id), "fixture ID"),
            "reason": reason,
        })
    return rows


def route_state(connector: str, profile: str) -> str:
    if connector not in CONNECTORS or profile not in PROFILES:
        raise ValueError("connector/profile is outside the fixed route inventory")
    if connector == "nginx":
        return "PROTECTED_SEPARATE"
    if connector in FULL_RUNTIME_CONNECTORS:
        return "RUNTIME_ROUTE"
    if connector not in LIMITED_ROUTE_CONNECTORS:
        raise ValueError("connector/profile is outside the fixed route inventory")
    if profile in ("no-crs-no-mrts", "with-crs-no-mrts"):
        return "RUNTIME_ROUTE"
    return "EXPECTED_UNSUPPORTED"


def route_inventory(connector: str) -> list[dict[str, str]]:
    if connector not in CONNECTORS:
        raise ValueError("connector is outside the fixed route inventory")
    return [{"profile": profile, "state": route_state(connector, profile)} for profile in PROFILES]


def aggregate_cases_by_phase_and_area(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, str | int]]:
    """Compatibility-only aggregation; it is intentionally not rendered."""
    counts: Counter[tuple[str, str]] = Counter()
    for row in rows:
        phase = row.get("phase")
        area = row.get("area")
        if not isinstance(phase, str) or not isinstance(area, str):
            raise ValueError("case row phase and area must be strings")
        counts[(phase, area)] += 1
    return [
        {"phase": phase, "area": area, "cases": count}
        for (phase, area), count in sorted(counts.items())
    ]


def _aggregate_scenarios(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[Mapping[str, Any]]] = {}
    for row in rows:
        category = row.get("category")
        if not isinstance(category, str):
            raise ValueError("scenario row category must be a string")
        grouped.setdefault(category, []).append(row)
    aggregates: list[dict[str, Any]] = []
    for category in sorted(grouped, key=str.casefold):
        records = grouped[category]
        counts = Counter(str(record.get("status")) for record in records)
        selected = len(records)
        executed = counts["PASS"] + counts["FAIL"] + counts["CANCELLED"]
        passed = counts["PASS"]
        failed = counts["FAIL"]
        cancelled = counts["CANCELLED"]
        unsupported = counts["UNSUPPORTED"]
        not_applicable = counts["NOT_APPLICABLE"]
        not_executed = counts["NOT_EXECUTED"]
        if selected != executed + unsupported + not_applicable + not_executed:
            raise ValueError("Framework scenario count equation is violated")
        if executed != passed + failed + cancelled:
            raise ValueError("Framework execution count equation is violated")
        aggregates.append({
            "category": category,
            "records": records,
            "selected": selected,
            "executed": executed,
            "passed": passed,
            "failed": failed,
            "cancelled": cancelled,
            "unsupported": unsupported,
            "not_applicable": not_applicable,
            "not_executed": not_executed,
        })
    return aggregates


def _aggregate_result(
    aggregate: Mapping[str, Any], *, evidence_validated: bool, execution_outcome: str
) -> str:
    selected = _integer(aggregate.get("selected"), "selected")
    executed = _integer(aggregate.get("executed"), "executed")
    passed = _integer(aggregate.get("passed"), "passed")
    failed = _integer(aggregate.get("failed"), "failed")
    cancelled = _integer(aggregate.get("cancelled"), "cancelled")
    unsupported = _integer(aggregate.get("unsupported"), "unsupported")
    not_applicable = _integer(aggregate.get("not_applicable"), "not applicable")
    not_executed = _integer(aggregate.get("not_executed"), "not executed")
    if selected == 0:
        return NOT_APPLICABLE
    if execution_outcome == "cancelled" or cancelled:
        return "CANCELLED"
    if execution_outcome == "failure":
        return "FAIL"
    if execution_outcome in {"skipped", "not_run"}:
        return NOT_RUN
    if execution_outcome == "not_applicable":
        return NOT_APPLICABLE
    if failed:
        return "FAIL"
    if unsupported == selected:
        return "UNSUPPORTED"
    if not_applicable == selected:
        return NOT_APPLICABLE
    if (
        evidence_validated
        and selected > 0
        and executed == selected
        and passed == selected
        and not_executed == 0
        and failed == 0
        and cancelled == 0
    ):
        return "PASS"
    return "PARTIAL"


def _aggregate_result_detail(aggregate: Mapping[str, Any], result: str) -> str:
    selected = _integer(aggregate.get("selected"), "selected")
    passed = _integer(aggregate.get("passed"), "passed")
    failed = _integer(aggregate.get("failed"), "failed")
    not_executed = _integer(aggregate.get("not_executed"), "not executed")
    if result == NOT_RUN:
        return f"`{NOT_RUN}`<br>no validated live test result"
    if result == NOT_APPLICABLE:
        return f"`{NOT_APPLICABLE}`<br>no Framework scenario is declared for this cell"
    if result == "FAIL" and failed == 0:
        return "`FAIL`<br>workflow execution failed before a validated case result"
    return (
        f"`{result}`<br>{passed}/{selected} live tests passed"
        f"<br>failed: {failed}; not executed: {not_executed}"
    )


def _aggregate_evidence(aggregate: Mapping[str, Any], *, evidence_validated: bool) -> str:
    records = aggregate.get("records")
    if not isinstance(records, list) or not records:
        return "no Framework scenario contract"
    if not evidence_validated:
        return "validated evidence not available"
    validations = sorted({str(record.get("validation_status")) for record in records})
    if len(validations) != 1:
        return "inconsistent Framework validation state"
    return f"framework results validated: `{_escape(validations[0])}`"


def _expectation(record: Mapping[str, Any], *, observed: bool) -> str:
    status_key = "observed_status" if observed else "expected_status"
    rule_key = "observed_rule_id" if observed else "expected_rule_id"
    parts: list[str] = []
    status = record.get(status_key)
    if isinstance(status, int) and not isinstance(status, bool):
        parts.append(f"HTTP `{status}`")
    rule = record.get(rule_key)
    if isinstance(rule, int) and not isinstance(rule, bool):
        parts.append(f"rule `{rule}`")
    if observed and record.get("live_executed") is True:
        parts.append("live request completed")
    return "; ".join(parts) if parts else NOT_REPORTED


def _row_execution(record: Mapping[str, Any]) -> str:
    status = str(record.get("status") or "")
    if status in {"PASS", "FAIL"} and record.get("live_executed") is True:
        return "RUN"
    if status == "CANCELLED":
        return "CANCELLED"
    if status == "UNSUPPORTED":
        return "UNSUPPORTED"
    if status == "NOT_APPLICABLE":
        return NOT_APPLICABLE
    return NOT_RUN


def _row_result(record: Mapping[str, Any]) -> str:
    status = str(record.get("status") or "NOT_EXECUTED")
    return (
        f"`{_escape(status)}`<br>live executed: {str(record.get('live_executed') is True).lower()}"
        f"<br>mismatches: {_integer(record.get('mismatch_count'), 'mismatch count')}"
        f"; failures: {_integer(record.get('failure_count'), 'failure count')}"
    )


def _row_evidence(record: Mapping[str, Any]) -> str:
    return (
        f"{_escape(record.get('evidence_kind', NOT_REPORTED))}<br>"
        f"validation: `{_escape(record.get('validation_status', 'not validated'))}`<br>"
        f"fixture: `{_escape(record.get('fixture_id', record.get('case_id', 'unknown')))}`"
    )


def _selection_state(
    rows: Sequence[Mapping[str, Any]], *, selection_outcome: str
) -> str:
    if selection_outcome == "failure":
        return "FAILED"
    if selection_outcome == "cancelled":
        return "CANCELLED"
    if selection_outcome in {"skipped", "not_run"}:
        return NOT_RUN
    if selection_outcome == "not_applicable":
        return NOT_APPLICABLE
    if not rows:
        return NOT_APPLICABLE
    selections = {str(row.get("selection_status")) for row in rows}
    if "SELECTED" in selections:
        return "SELECTED"
    if selections == {"UNSUPPORTED"}:
        return "UNSUPPORTED"
    if selections == {"NOT_APPLICABLE"}:
        return NOT_APPLICABLE
    return "PARTIAL"


def _apply_execution_outcome(
    rows: Sequence[Mapping[str, Any]], execution_outcome: str
) -> list[dict[str, Any]]:
    """Fail closed when the recorded workflow execution does not complete."""
    if execution_outcome == "success":
        return [dict(row) for row in rows]
    replacement = {
        "cancelled": "CANCELLED",
        "not_applicable": "NOT_APPLICABLE",
    }.get(execution_outcome, "NOT_EXECUTED")
    reconciled: list[dict[str, Any]] = []
    for row in rows:
        updated = dict(row)
        if updated.get("selection_status") == "SELECTED":
            updated["status"] = replacement
            updated["live_executed"] = False
            updated["validation_status"] = "not validated"
            updated["evidence_kind"] = "workflow execution did not complete"
        reconciled.append(updated)
    return reconciled


def _execution_state(
    rows: Sequence[Mapping[str, Any]], *, evidence_validated: bool, execution_outcome: str
) -> str:
    if not rows:
        return NOT_APPLICABLE
    if execution_outcome == "cancelled":
        return "CANCELLED"
    if execution_outcome == "failure":
        return "FAILED"
    if execution_outcome in {"skipped", "not_run"}:
        return NOT_RUN
    if execution_outcome == "not_applicable":
        return NOT_APPLICABLE
    if evidence_validated and any(_row_execution(row) == "RUN" for row in rows):
        return "RUN"
    if all(_row_execution(row) == "UNSUPPORTED" for row in rows):
        return "UNSUPPORTED"
    if all(_row_execution(row) == NOT_APPLICABLE for row in rows):
        return NOT_APPLICABLE
    return NOT_RUN


def _validation_state(
    rows: Sequence[Mapping[str, Any]], *, evidence_validated: bool, outcome: str
) -> str:
    if not rows:
        return NOT_APPLICABLE
    if not evidence_validated:
        return outcome.upper().replace("_", " ")
    states = {str(row.get("validation_status")) for row in rows}
    if len(states) != 1:
        return "INCONSISTENT"
    return next(iter(states))


def _append_aggregate_rows(
    output: list[str],
    aggregates: Sequence[Mapping[str, Any]],
    *,
    evidence_validated: bool,
    execution_outcome: str,
) -> None:
    for aggregate in aggregates:
        result = _aggregate_result(
            aggregate,
            evidence_validated=evidence_validated,
            execution_outcome=execution_outcome,
        )
        output.append(
            "| {category} | {selected} | {executed} | {passed} | {failed} | {unsupported} | {not_applicable} | {not_executed} | {result} | {evidence} |".format(
                category=_escape(aggregate["category"]),
                selected=aggregate["selected"],
                executed=aggregate["executed"],
                passed=aggregate["passed"],
                failed=aggregate["failed"],
                unsupported=aggregate["unsupported"],
                not_applicable=aggregate["not_applicable"],
                not_executed=aggregate["not_executed"],
                result=_aggregate_result_detail(aggregate, result),
                evidence=_aggregate_evidence(aggregate, evidence_validated=evidence_validated),
            )
        )
    total = {
        key: sum(int(aggregate[key]) for aggregate in aggregates)
        for key in (
            "selected", "executed", "passed", "failed", "unsupported",
            "not_applicable", "not_executed", "cancelled",
        )
    }
    if total["selected"] != total["executed"] + total["unsupported"] + total["not_applicable"] + total["not_executed"]:
        raise ValueError("Framework total count equation is violated")
    if total["executed"] != total["passed"] + total["failed"] + total["cancelled"]:
        raise ValueError("Framework total execution equation is violated")
    total_result = _aggregate_result(
        {**total, "records": [record for aggregate in aggregates for record in aggregate["records"]]},
        evidence_validated=evidence_validated,
        execution_outcome=execution_outcome,
    )
    output.append(
        "| **Total** | **{selected}** | **{executed}** | **{passed}** | **{failed}** | **{unsupported}** | **{not_applicable}** | **{not_executed}** | {result} | {evidence} |".format(
            **total,
            result=_aggregate_result_detail(total, total_result),
            evidence=("framework results validated" if evidence_validated else "validated evidence not available"),
        )
    )


def _append_framework_details(
    output: list[str], aggregates: Sequence[Mapping[str, Any]]
) -> None:
    for aggregate in aggregates:
        records = aggregate["records"]
        output.extend((
            "",
            "<details>",
            f"<summary>{_escape(aggregate['category'])} — {len(records)} framework tests</summary>",
            "",
            "| Framework test | Execution | Expected | Observed | Result | Evidence |",
            "| --- | --- | --- | --- | --- | --- |",
        ))
        for record in records:
            output.append(
                "| `{case_id}` | `{execution}` | {expected} | {observed} | {result} | {evidence} |".format(
                    case_id=_escape(record["case_id"]),
                    execution=_escape(_row_execution(record)),
                    expected=_expectation(record, observed=False),
                    observed=_expectation(record, observed=True),
                    result=_row_result(record),
                    evidence=_row_evidence(record),
                )
            )
        output.extend(("", "</details>"))


def render_summary(
    plan: Mapping[str, Any],
    evidence: Mapping[str, Mapping[str, Any]] | None = None,
    *,
    coverage_kind: str = "runtime",
    crs: str = "",
    mrts: str = "",
    selection_outcome: str = "not_run",
    execution_outcome: str = "not_run",
    evidence_validation_outcome: str = "not_run",
    evidence_validated: bool = False,
    terminal_signal: Mapping[str, str] | None = None,
) -> str:
    if selection_outcome not in WORKFLOW_OUTCOMES:
        raise ValueError("selection outcome is outside the fixed workflow state set")
    if execution_outcome not in WORKFLOW_OUTCOMES:
        raise ValueError("execution outcome is outside the fixed workflow state set")
    if evidence_validation_outcome not in WORKFLOW_OUTCOMES:
        raise ValueError("evidence validation outcome is outside the fixed workflow state set")
    connector = str(plan.get("connector") or "")
    profile = str(
        plan.get("profile")
        or (_profile(crs, mrts) if crs and mrts else NO_CRS_PROFILE)
    )
    if connector not in CONNECTORS or profile not in PROFILES:
        raise ValueError("plan connector/profile is outside the fixed inventory")
    rows = _apply_execution_outcome(
        case_rows(plan, evidence, evidence_validated=evidence_validated),
        execution_outcome,
    )
    aggregates = _aggregate_scenarios(rows)
    status_counts = Counter(str(row["status"]) for row in rows)
    selection_state = _selection_state(rows, selection_outcome=selection_outcome)
    execution_state = _execution_state(
        rows, evidence_validated=evidence_validated, execution_outcome=execution_outcome
    )
    validation_state = _validation_state(
        rows, evidence_validated=evidence_validated, outcome=evidence_validation_outcome
    )
    output = [
        "## Connector mode coverage (interim)",
        "",
        f"Connector: `{_escape(connector)}`; coverage: `{_escape(coverage_kind)}`; CRS: `{_escape(crs)}`; MRTS: `{_escape(mrts)}`.",
        f"Framework test selection: `{_escape(selection_state)}` (workflow: `{_escape(selection_outcome)}`).",
        f"Framework test execution: `{_escape(execution_state)}` (workflow: `{_escape(execution_outcome)}`).",
        f"Framework evidence validation: `{_escape(validation_state)}` (workflow: `{_escape(evidence_validation_outcome)}`).",
        "",
        "| Terminal framework status | Count |",
        "| --- | ---: |",
    ]
    output.extend(
        f"| {_escape(status)} | `{status_counts.get(status, 0)}` |"
        for status in sorted(CASE_STATUSES)
    )
    if terminal_signal is not None:
        output.extend((
            "",
            "### Unvalidated terminal signal",
            "",
            "A bounded terminal result exists, but it was not used to promote execution or case status.",
            f"Observed terminal status (not promoted): `{_escape(terminal_signal.get('status', 'unknown'))}`.",
        ))
    output.extend((
        "",
        f"### Connector/profile routes for `{_escape(connector)}`",
        "",
        "This inventory lists current workflow routes, not individual test results.",
        "",
        "| Profile | Route state |",
        "| --- | --- |",
    ))
    output.extend(
        f"| {_escape(route['profile'])} | {_escape(route['state'])} |"
        for route in route_inventory(connector)
    )
    output.extend((
        "",
        "### Framework test scenario coverage",
        "",
        "`Selected` is the number of canonical Framework plan entries, including explicit terminal selection outcomes. "
        "The checked invariants are `Selected = Executed + Unsupported + Not applicable + Not executed` and "
        "`Executed = Passed + Failed + Cancelled`.",
        "",
        "| Framework scenario | Selected | Executed | Passed | Failed | Unsupported | Not applicable | Not executed | Result | Evidence |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ))
    _append_aggregate_rows(
        output,
        aggregates,
        evidence_validated=evidence_validated,
        execution_outcome=execution_outcome,
    )
    _append_framework_details(output, aggregates)
    output.append(
        f"\nA `RUN` requires a bound, live Framework result; a successful workflow step without that evidence remains `{NOT_RUN}` or `PARTIAL`."
    )
    return "\n".join(output) + "\n"


def append_github_step_summary(environment: Mapping[str, str], content: str) -> None:
    if not SAFE_RUNTIME_READER.is_file() or SAFE_RUNTIME_READER.is_symlink():
        raise ValueError("existing safe GitHub Step Summary writer is unavailable")
    writer = _load_module(SAFE_RUNTIME_READER, "connector_safe_step_summary_writer")
    if not callable(getattr(writer, "append_github_step_summary", None)):
        raise ValueError("existing safe GitHub Step Summary writer is incomplete")
    writer.append_github_step_summary(environment, content)


def main(arguments: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector", required=True, choices=CONNECTORS)
    parser.add_argument("--crs", required=True, choices=("no-crs", "with-crs"))
    parser.add_argument("--mrts", required=True, choices=("no-mrts", "with-mrts"))
    parser.add_argument(
        "--coverage-kind",
        required=True,
        choices=("runtime", "contract", "inventory", "expected_unsupported"),
    )
    parser.add_argument("--connector-root", required=True, type=Path)
    parser.add_argument("--framework-root", required=True, type=Path)
    parser.add_argument("--framework-sha", required=True)
    parser.add_argument("--parent-sha", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--evidence-dir", type=Path)
    parser.add_argument(
        "--selection-outcome", required=True, choices=sorted(WORKFLOW_OUTCOMES)
    )
    parser.add_argument(
        "--execution-outcome", required=True, choices=sorted(WORKFLOW_OUTCOMES)
    )
    parser.add_argument(
        "--evidence-validation-outcome",
        required=True,
        choices=sorted(WORKFLOW_OUTCOMES),
    )
    args = parser.parse_args(arguments)
    try:
        framework_sha = _commit(args.framework_sha, "Framework commit")
        parent_sha = _commit(args.parent_sha, "Parent commit")
        run_id = _run_id(args.run_id, "runtime run ID")
        if not args.connector_root.is_dir() or args.connector_root.is_symlink():
            raise ValueError("connector root must be a real directory")
        connector_root = args.connector_root.resolve()
        capabilities = connector_root / "connectors" / args.connector / "capabilities.json"
        if capabilities.is_symlink() or not capabilities.resolve().is_relative_to(connector_root):
            raise ValueError("connector capability manifest is outside connector root")
        plan = select_framework_cases(
            args.framework_root,
            args.connector,
            capabilities,
            crs=args.crs,
            mrts=args.mrts,
            framework_sha=framework_sha,
        )
        evidence: dict[str, Mapping[str, Any]] | None = None
        evidence_validated = False
        terminal_signal = None
        if args.evidence_validation_outcome == "success":
            if args.evidence_dir is None:
                raise ValueError("successful validation requires a canonical evidence directory")
            if plan.get("scenario_contract") == "no_crs_baseline":
                _validate_no_crs_framework_contract(
                    args.framework_root,
                    args.evidence_dir,
                    connector_root,
                    capabilities,
                    args.connector,
                    run_id,
                )
            evidence = _records_from_evidence(
                args.evidence_dir,
                plan,
                args.connector,
                run_id=run_id,
                parent_sha=parent_sha,
                framework_sha=framework_sha,
            )
            evidence_validated = True
        elif args.evidence_dir and plan.get("scenario_contract") == "no_crs_baseline":
            terminal_signal = _unvalidated_terminal_signal(args.evidence_dir, args.connector)
        append_github_step_summary(
            os.environ,
            render_summary(
                plan,
                evidence,
                coverage_kind=args.coverage_kind,
                crs=args.crs,
                mrts=args.mrts,
                selection_outcome=args.selection_outcome,
                execution_outcome=args.execution_outcome,
                evidence_validation_outcome=args.evidence_validation_outcome,
                evidence_validated=evidence_validated,
                terminal_signal=terminal_signal,
            ),
        )
    except (ImportError, OSError, ValueError) as error:
        print(f"FAIL: {error}", file=os.sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
