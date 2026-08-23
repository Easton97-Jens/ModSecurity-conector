#!/usr/bin/env python3
"""Write a bounded GitHub summary of one real CRS/no-MRTS workflow cell.

The report renders fixed GitHub step outcomes and, when available, only
strictly validated structured evidence at a path derived from the current
workflow cell.  It never parses raw runtime paths and never turns missing or
unvalidated evidence into a successful connector capability claim.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any


CONNECTORS = frozenset(("apache", "envoy", "haproxy", "lighttpd", "traefik"))
VALID_OUTCOMES = frozenset(("success", "failure", "skipped", "cancelled"))
ASSERTION_STATUSES = frozenset(("PASS", "FAIL", "NOT_RUN", "NOT_AVAILABLE", "NOT_APPLICABLE"))
BUNDLE_STATUSES = frozenset(("PASS", "PARTIAL", "FAIL", "NOT_RUN", "CANCELLED"))
NORMALIZED_EVIDENCE_CONNECTORS = frozenset(("envoy", "lighttpd", "traefik"))
PROFILE = "five-connectors-with-crs-no-mrts"
RULE_ID = 942270
MAX_EVIDENCE_FILE_BYTES = 2 * 1024 * 1024
RUN_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,47}$", re.ASCII)
COMMIT = re.compile(r"^[0-9a-f]{40}$", re.ASCII)
INTEGRATION_MODES = {
    "envoy": "ext_proc",
    "lighttpd": "patched-native-lighttpd",
    "traefik": "native-traefik-middleware",
}
NO_MRTS_ASSERTIONS = (
    ("MRTS runner invoked", "runner_invoked"),
    ("MRTS case inventory loaded", "case_inventory_loaded"),
    ("MRTS process started", "process_started"),
    ("MRTS socket/listener created", "socket_or_listener_created"),
    ("MRTS artifact used", "artifact_used"),
)
CLEANUP_ASSERTIONS = (
    ("Remaining host processes", "host_processes_remaining"),
    ("Remaining helper processes", "helper_processes_remaining"),
    ("Remaining listeners", "listeners_remaining"),
    ("Remaining sockets", "sockets_remaining"),
    ("Remaining PID files", "pid_files_remaining"),
    ("Remaining runtime fixtures", "runtime_fixtures_remaining"),
    ("Remaining temporary paths", "temporary_paths_remaining"),
    ("Remaining processes", "processes_remaining"),
)
STAGES = (
    ("checkout", "Checkout exact Parent head", "CHECKOUT_OUTCOME"),
    ("setup_python", "Locked Python toolchain", "SETUP_PYTHON_OUTCOME"),
    ("verify_python", "Python interpreter contract", "VERIFY_PYTHON_OUTCOME"),
    ("verify_revisions", "Parent/Framework/MRTS revisions", "VERIFY_REVISIONS_OUTCOME"),
    ("install_dependencies", "Hash-locked Framework dependency", "INSTALL_DEPENDENCIES_OUTCOME"),
    ("verify_cell", "Fixed runtime-cell policy", "VERIFY_CELL_OUTCOME"),
    ("initialize_roots", "Private runtime roots", "INITIALIZE_ROOTS_OUTCOME"),
    ("prepare_crs", "Workflow CRS source preparation", "PREPARE_CRS_OUTCOME"),
    ("runtime", "Real connector runtime target", "RUNTIME_OUTCOME"),
    ("upload_evidence", "Evidence publication", "UPLOAD_EVIDENCE_OUTCOME"),
)
SECURITY_SKIPPED_STAGE = ("haproxy", "upload_evidence")
SUMMARY_DIRECTORY_NAME = "_runner_file_commands"
SUMMARY_FILE_NAME = re.compile(r"^step_summary_[A-Za-z0-9_-]+$", re.ASCII)
UNSAFE_SUMMARY_PATH = "GitHub step summary path is unsafe"


def require_connector(value: str) -> str:
    if value not in CONNECTORS:
        raise ValueError("connector is outside the fixed CRS/no-MRTS runtime set")
    return value


def outcomes_from_environment(environment: Mapping[str, str]) -> dict[str, str]:
    outcomes: dict[str, str] = {}
    for key, _label, environment_name in STAGES:
        value = environment.get(environment_name, "")
        if value not in VALID_OUTCOMES:
            raise ValueError(f"{environment_name} is not a GitHub step outcome")
        outcomes[key] = value
    return outcomes


def rendered_outcome(connector: str, stage: str, outcome: str) -> str:
    if (connector, stage) == SECURITY_SKIPPED_STAGE and outcome == "skipped":
        return "skipped_by_security_policy"
    return outcome


def outcome_counts(connector: str, outcomes: Mapping[str, str]) -> dict[str, int]:
    counts = {
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "cancelled": 0,
        "security_skipped": 0,
    }
    for stage, _label, _environment_name in STAGES:
        outcome = outcomes[stage]
        if rendered_outcome(connector, stage, outcome) == "skipped_by_security_policy":
            counts["security_skipped"] += 1
        elif outcome == "success":
            counts["passed"] += 1
        elif outcome == "failure":
            counts["failed"] += 1
        elif outcome == "skipped":
            counts["skipped"] += 1
        else:
            counts["cancelled"] += 1
    return counts


def first_nonpassing_stage(connector: str, outcomes: Mapping[str, str]) -> str:
    for stage, label, _environment_name in STAGES:
        outcome = rendered_outcome(connector, stage, outcomes[stage])
        if outcome != "success" and outcome != "skipped_by_security_policy":
            return label
    return "none"


def _render_assertion_section(title: str, assertions: Sequence[Mapping[str, str]]) -> list[str]:
    rows = ["", f"#### {title}", "", "| Assertion | Expected | Observed | Result | Evidence |", "| --- | --- | --- | --- | --- |"]
    rows.extend(
        f"| {row['assertion']} | {row['expected']} | {row['observed']} | `{row['result']}` | {row['evidence']} |"
        for row in assertions
    )
    return rows


def render_summary(
    connector: str,
    outcomes: Mapping[str, str],
    *,
    evidence_context: Mapping[str, str] | None = None,
) -> str:
    connector = require_connector(connector)
    if set(outcomes) != {stage for stage, _label, _environment_name in STAGES}:
        raise ValueError("summary outcomes do not match the fixed workflow stage set")
    if any(outcome not in VALID_OUTCOMES for outcome in outcomes.values()):
        raise ValueError("summary outcomes contain an invalid state")
    counts = outcome_counts(connector, outcomes)
    bundle = runtime_assertion_bundle(
        connector,
        outcomes["runtime"],
        evidence_context=evidence_context or {},
    )
    rows = [
        f"### {connector} — CRS/no-MRTS runtime overview",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Stages passed | `{counts['passed']}` |",
        f"| Stages failed | `{counts['failed']}` |",
        f"| Stages skipped | `{counts['skipped']}` |",
        f"| Stages cancelled | `{counts['cancelled']}` |",
        f"| Security-policy skips | `{counts['security_skipped']}` |",
        f"| First non-passing stage | `{first_nonpassing_stage(connector, outcomes)}` |",
        "",
        "| Stage | Actual outcome |",
        "| --- | --- |",
    ]
    rows.extend(
        f"| {label} | `{rendered_outcome(connector, stage, outcomes[stage])}` |"
        for stage, label, _environment_name in STAGES
    )
    rows.extend(
        (
            "",
            "### Real runtime assertions",
            "",
            f"Overall runtime assertion status: `{bundle['overall']}`",
        )
    )
    rows.extend(_render_assertion_section("Configuration and startup", bundle["configuration"]))
    rows.extend(_render_assertion_section("Request and CRS behavior", bundle["requests"]))
    rows.extend(_render_assertion_section("no-MRTS isolation and cleanup", bundle["isolation_cleanup"]))
    rows.extend(
        (
            "",
            connector_narrative(connector, bundle["evidence_state"]),
            "",
        )
    )
    return "\n".join(rows)


def _write_summary(descriptor: int, content: str) -> None:
    data = content.encode("utf-8")
    while data:
        written = os.write(descriptor, data)
        if written <= 0:
            raise OSError("cannot append GitHub step summary")
        data = data[written:]


def _safe_open_flags() -> tuple[int, int, int, int]:
    nofollow = getattr(os, "O_NOFOLLOW", None)
    directory = getattr(os, "O_DIRECTORY", None)
    nonblock = getattr(os, "O_NONBLOCK", None)
    if (
        not isinstance(nofollow, int)
        or not isinstance(directory, int)
        or not isinstance(nonblock, int)
    ):
        raise ValueError("GitHub step summary safe-open capability is unavailable")
    return nofollow, directory, nonblock, getattr(os, "O_CLOEXEC", 0)


def _open_directory_without_symlinks(path: Path) -> int:
    if (
        not path.is_absolute()
        or path == Path("/")
        or os.path.normpath(os.fspath(path)) != os.fspath(path)
    ):
        raise ValueError(UNSAFE_SUMMARY_PATH)
    nofollow, directory, _nonblock, close_on_exec = _safe_open_flags()
    descriptor = -1
    try:
        descriptor = os.open(path.anchor, os.O_RDONLY | directory | close_on_exec)
        for component in path.parts[1:]:
            next_descriptor = os.open(
                component,
                os.O_RDONLY | directory | nofollow | close_on_exec,
                dir_fd=descriptor,
            )
            os.close(descriptor)
            descriptor = next_descriptor
    except OSError as error:
        if descriptor >= 0:
            os.close(descriptor)
        raise ValueError(UNSAFE_SUMMARY_PATH) from error
    return descriptor


def _require_private_evidence_directory(descriptor: int) -> None:
    details = os.fstat(descriptor)
    if (
        not stat.S_ISDIR(details.st_mode)
        or details.st_uid != os.geteuid()
        or details.st_mode & 0o022
    ):
        raise ValueError("runtime evidence directory is unsafe")


def _safe_child_directory(parent: int, component: str) -> int:
    if not re.fullmatch(r"[A-Za-z0-9._-]+", component) or component in {".", ".."}:
        raise ValueError("runtime evidence path component is unsafe")
    nofollow, directory, _nonblock, close_on_exec = _safe_open_flags()
    try:
        descriptor = os.open(
            component,
            os.O_RDONLY | directory | nofollow | close_on_exec,
            dir_fd=parent,
        )
    except OSError as error:
        raise ValueError("runtime evidence directory is unavailable") from error
    try:
        _require_private_evidence_directory(descriptor)
    except Exception:
        os.close(descriptor)
        raise
    return descriptor


def _read_bounded_json(root: Path, components: Sequence[str], label: str) -> dict[str, Any]:
    """Read one fixed JSON artifact through no-follow descriptor traversal."""
    if not components:
        raise ValueError("runtime evidence file is unspecified")
    root_descriptor = -1
    directory_descriptor = -1
    file_descriptor = -1
    try:
        root_descriptor = _open_directory_without_symlinks(root)
        _require_private_evidence_directory(root_descriptor)
        directory_descriptor = root_descriptor
        for component in components[:-1]:
            next_descriptor = _safe_child_directory(directory_descriptor, component)
            if directory_descriptor != root_descriptor:
                os.close(directory_descriptor)
            directory_descriptor = next_descriptor
        filename = components[-1]
        if not re.fullmatch(r"[A-Za-z0-9._-]+", filename) or filename in {".", ".."}:
            raise ValueError("runtime evidence filename is unsafe")
        nofollow, _directory, nonblock, close_on_exec = _safe_open_flags()
        try:
            file_descriptor = os.open(
                filename,
                os.O_RDONLY | nofollow | nonblock | close_on_exec,
                dir_fd=directory_descriptor,
            )
        except OSError as error:
            raise ValueError(f"{label} is unavailable") from error
        before = os.fstat(file_descriptor)
        if (
            not stat.S_ISREG(before.st_mode)
            or before.st_uid != os.geteuid()
            or before.st_mode & 0o022
            or before.st_nlink != 1
            or before.st_size > MAX_EVIDENCE_FILE_BYTES
        ):
            raise ValueError(f"{label} is unsafe")
        data = bytearray()
        while len(data) < before.st_size:
            chunk = os.read(file_descriptor, min(65536, before.st_size - len(data)))
            if not chunk:
                break
            data.extend(chunk)
        after = os.fstat(file_descriptor)
        if (
            len(data) != before.st_size
            or (
                before.st_dev,
                before.st_ino,
                stat.S_IFMT(before.st_mode),
                before.st_uid,
                stat.S_IMODE(before.st_mode),
                before.st_nlink,
                before.st_size,
            )
            != (
                after.st_dev,
                after.st_ino,
                stat.S_IFMT(after.st_mode),
                after.st_uid,
                stat.S_IMODE(after.st_mode),
                after.st_nlink,
                after.st_size,
            )
        ):
            raise ValueError(f"{label} changed while it was read")
        try:
            parsed = json.loads(bytes(data).decode("utf-8", "strict"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError(f"{label} is not valid JSON") from error
        if not isinstance(parsed, dict):
            raise ValueError(f"{label} root must be an object")
        return parsed
    finally:
        if file_descriptor >= 0:
            os.close(file_descriptor)
        if directory_descriptor >= 0 and directory_descriptor != root_descriptor:
            os.close(directory_descriptor)
        if root_descriptor >= 0:
            os.close(root_descriptor)


def _context_value(context: Mapping[str, str], name: str) -> str:
    value = context.get(name, "")
    if not isinstance(value, str) or not value:
        raise ValueError("runtime evidence context is incomplete")
    return value


def _verified_runtime_root(context: Mapping[str, str]) -> tuple[Path, str, str, str]:
    runner_temp = Path(_context_value(context, "runner_temp"))
    parent_sha = _context_value(context, "parent_sha")
    framework_sha = _context_value(context, "framework_sha")
    run_id = _context_value(context, "run_id")
    if (
        not runner_temp.is_absolute()
        or runner_temp == Path("/")
        or os.path.normpath(os.fspath(runner_temp)) != os.fspath(runner_temp)
        or not COMMIT.fullmatch(parent_sha)
        or not COMMIT.fullmatch(framework_sha)
        or not RUN_ID.fullmatch(run_id)
    ):
        raise ValueError("runtime evidence context is unsafe")
    return (
        runner_temp / "ModSecurity-conector-with-crs-no-mrts" / parent_sha / run_id / "verified",
        run_id,
        parent_sha,
        framework_sha,
    )


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} is not an object")
    return value


def _exact(record: Mapping[str, Any], field: str, expected: Any, label: str) -> None:
    if record.get(field) != expected:
        raise ValueError(f"{label} {field} does not match the workflow cell")


def _http_status(record: Mapping[str, Any], field: str, expected: int, label: str) -> int:
    value = record.get(field)
    if not isinstance(value, int) or isinstance(value, bool) or value != expected:
        raise ValueError(f"{label} {field} is not the expected HTTP status")
    return value


def _zero_counter(record: Mapping[str, Any], field: str, label: str) -> int:
    value = record.get(field)
    if not isinstance(value, int) or isinstance(value, bool) or value != 0:
        raise ValueError(f"{label} {field} is not zero")
    return value


def _false_flag(record: Mapping[str, Any], field: str, label: str) -> bool:
    if record.get(field) is not False:
        raise ValueError(f"{label} {field} is not false")
    return False


def _assertion(
    name: str, expected: str, observed: str, result: str, evidence: str,
) -> dict[str, str]:
    if result not in ASSERTION_STATUSES:
        raise ValueError("assertion result is outside the fixed status set")
    return {
        "assertion": name,
        "expected": expected,
        "observed": observed,
        "result": result,
        "evidence": evidence,
    }


def _empty_assertion_sections(result: str, observed: str, evidence: str) -> dict[str, list[dict[str, str]]]:
    configuration = [
        _assertion("Configuration/load", "passed", observed, result, evidence),
        _assertion("Connector host start", "passed", observed, result, evidence),
    ]
    requests = [
        _assertion("Allow request", "HTTP 200", observed, result, evidence),
        _assertion("CRS block request", "HTTP 403", observed, result, evidence),
        _assertion("CRS trigger rule", f"rule {RULE_ID}", observed, result, evidence),
        _assertion("Case-variant/bypass probe", "HTTP 403", observed, result, evidence),
    ]
    isolation_cleanup = [
        _assertion(name, "false", observed, result, evidence)
        for name, _field in NO_MRTS_ASSERTIONS
    ]
    isolation_cleanup.extend(
        _assertion(name, "0", observed, result, evidence)
        for name, _field in CLEANUP_ASSERTIONS
    )
    return {
        "configuration": configuration,
        "requests": requests,
        "isolation_cleanup": isolation_cleanup,
    }


def _normalized_assertion_sections(
    connector: str, root: Path, run_id: str, parent_sha: str, framework_sha: str,
) -> dict[str, list[dict[str, str]]]:
    event = _read_bounded_json(
        root,
        ("evidence", "normalized", connector, run_id, "event.json"),
        "normalized event",
    )
    runtime = _read_bounded_json(
        root,
        ("evidence", "runtime", connector, run_id, "runtime.json"),
        "runtime attestation",
    )
    mode = INTEGRATION_MODES[connector]
    for record, label in ((event, "normalized event"), (runtime, "runtime attestation")):
        _exact(record, "connector", connector, label)
        _exact(record, "run_id", run_id, label)
    _exact(event, "schema_version", 1, "normalized event")
    _exact(event, "profile", PROFILE, "normalized event")
    _exact(event, "integration_mode", mode, "normalized event")
    _exact(event, "connector_commit", parent_sha, "normalized event")
    _exact(event, "framework_commit", framework_sha, "normalized event")
    _exact(event, "status", "PASS", "normalized event")
    _exact(runtime, "schema_version", 1, "runtime attestation")
    _exact(runtime, "record_type", "parent_runtime_attestation", "runtime attestation")
    _exact(runtime, "runtime_status", "PASS", "runtime attestation")

    configuration = _mapping(event.get("host_configuration"), "normalized host configuration")
    allow = _mapping(event.get("allow_case"), "normalized allow case")
    event_no_mrts = _mapping(event.get("no_mrts"), "normalized no-MRTS attestation")
    runtime_no_mrts = _mapping(runtime.get("no_mrts"), "runtime no-MRTS attestation")
    event_cleanup = _mapping(event.get("cleanup"), "normalized cleanup")
    cleanup_scan = _mapping(runtime.get("cleanup_scan"), "runtime cleanup scan")
    observed_statuses = _mapping(runtime.get("observed_statuses"), "runtime observed statuses")

    _exact(configuration, "config_test_status", "passed", "normalized host configuration")
    _exact(configuration, "host_start_status", "passed", "normalized host configuration")
    _http_status(allow, "expected_status", 200, "normalized allow case")
    _http_status(allow, "observed_status", 200, "normalized allow case")
    _http_status(event, "expected_status", 403, "normalized event")
    _http_status(event, "observed_status", 403, "normalized event")
    _http_status(event, "expected_rule_id", RULE_ID, "normalized event")
    _http_status(event, "observed_rule_id", RULE_ID, "normalized event")
    _http_status(observed_statuses, "allow", 200, "runtime observed statuses")
    _http_status(observed_statuses, "block", 403, "runtime observed statuses")
    _http_status(observed_statuses, "bypass", 403, "runtime observed statuses")
    _exact(event_cleanup, "status", "passed", "normalized cleanup")

    for _name, field in NO_MRTS_ASSERTIONS:
        _false_flag(event_no_mrts, field, "normalized no-MRTS attestation")
        _false_flag(runtime_no_mrts, field, "runtime no-MRTS attestation")
    for _name, field in CLEANUP_ASSERTIONS:
        _zero_counter(cleanup_scan, field, "runtime cleanup scan")
        if field != "processes_remaining":
            _zero_counter(event_cleanup, field, "normalized cleanup")
    if cleanup_scan.get("paths") != [] or cleanup_scan.get("listener_records") != []:
        raise ValueError("runtime cleanup diagnostics are not empty")

    configuration_rows = [
        _assertion("Configuration/load", "passed", "passed", "PASS", "normalized event"),
        _assertion("Connector host start", "passed", "passed", "PASS", "normalized event"),
    ]
    request_rows = [
        _assertion("Allow request", "HTTP 200", "HTTP 200", "PASS", "normalized event"),
        _assertion("CRS block request", "HTTP 403", "HTTP 403", "PASS", "normalized event"),
        _assertion("CRS trigger rule", f"rule {RULE_ID}", f"rule {RULE_ID}", "PASS", "normalized event"),
        _assertion("Case-variant/bypass probe", "HTTP 403", "HTTP 403", "PASS", "runtime attestation"),
    ]
    isolation_cleanup_rows = [
        _assertion(name, "false", "false", "PASS", "runtime attestation")
        for name, _field in NO_MRTS_ASSERTIONS
    ]
    isolation_cleanup_rows.extend(
        _assertion(name, "0", "0", "PASS", "runtime attestation")
        for name, _field in CLEANUP_ASSERTIONS
    )
    return {
        "configuration": configuration_rows,
        "requests": request_rows,
        "isolation_cleanup": isolation_cleanup_rows,
    }


def _summary_case_assertion_sections(
    connector: str, root: Path,
) -> dict[str, list[dict[str, str]]]:
    summary = _read_bounded_json(
        root,
        (
            "build",
            f"verified-{connector}-case",
            "with-crs",
            "no-mrts",
            "results",
            f"{connector}-summary.json",
        ),
        f"{connector} summary",
    )
    connector_summary = _mapping(summary.get(connector), f"{connector} summary")
    cases = _mapping(connector_summary.get("cases"), f"{connector} summary cases")
    case = _mapping(cases.get("crs_sqli_anomaly_block"), f"{connector} CRS case")
    _exact(case, "name", "crs_sqli_anomaly_block", f"{connector} CRS case")
    expected = case.get("expected_status")
    observed = case.get("actual_status")
    transport = case.get("observed_transport_result")
    case_status = case.get("status")
    live_executed = case.get("live_executed")
    if (
        not isinstance(expected, int)
        or isinstance(expected, bool)
        or not isinstance(observed, int)
        or isinstance(observed, bool)
        or transport != "http_status"
        or case_status not in {"pass", "fail", "blocked", "not_executable", "skipped"}
        or not isinstance(live_executed, bool)
    ):
        raise ValueError(f"{connector} CRS case is malformed")
    # A case status and HTTP value alone are insufficient: the fixed harness
    # summary must explicitly attest that this was a live connector request.
    if case_status == "pass" and live_executed and expected == 403 and observed == 403:
        result = "PASS"
    elif case_status == "fail" and live_executed:
        result = "FAIL"
    elif case_status == "skipped":
        result = "NOT_RUN"
    else:
        result = "NOT_AVAILABLE"
    sections = _empty_assertion_sections("NOT_AVAILABLE", "not reported", "not reported")
    sections["requests"][1] = _assertion(
        "CRS block request", f"HTTP {expected}", f"HTTP {observed}", result, f"{connector} summary"
    )
    return sections


def _all_assertions_pass(sections: Mapping[str, Sequence[Mapping[str, str]]]) -> bool:
    return all(
        row.get("result") == "PASS"
        for rows in sections.values()
        for row in rows
    )


def runtime_assertion_bundle(
    connector: str,
    runtime_outcome: str,
    *,
    evidence_context: Mapping[str, str],
) -> dict[str, Any]:
    """Build a fail-closed assertion bundle from fixed, validated evidence only."""
    connector = require_connector(connector)
    if runtime_outcome not in VALID_OUTCOMES:
        raise ValueError("runtime outcome is outside the fixed workflow state set")
    if runtime_outcome == "skipped":
        sections = _empty_assertion_sections("NOT_RUN", "not run", "GitHub step outcome")
        return {**sections, "overall": "NOT_RUN", "evidence_state": "not_run"}
    try:
        root, run_id, parent_sha, framework_sha = _verified_runtime_root(evidence_context)
        if connector in NORMALIZED_EVIDENCE_CONNECTORS:
            sections = _normalized_assertion_sections(
                connector, root, run_id, parent_sha, framework_sha,
            )
            evidence_state = "normalized"
        else:
            sections = _summary_case_assertion_sections(connector, root)
            evidence_state = "case_summary"
    except (OSError, ValueError):
        if runtime_outcome == "cancelled":
            sections = _empty_assertion_sections("NOT_RUN", "not run", "GitHub step outcome")
            overall = "CANCELLED"
        elif runtime_outcome == "failure":
            sections = _empty_assertion_sections("NOT_AVAILABLE", "not reported", "not reported")
            overall = "FAIL"
        else:
            sections = _empty_assertion_sections("NOT_AVAILABLE", "not reported", "not reported")
            overall = "PARTIAL"
        return {**sections, "overall": overall, "evidence_state": "unavailable"}
    if runtime_outcome == "cancelled":
        overall = "CANCELLED"
    elif runtime_outcome == "failure":
        overall = "FAIL"
    elif _all_assertions_pass(sections):
        overall = "PASS"
    else:
        overall = "PARTIAL"
    if overall not in BUNDLE_STATUSES:
        raise ValueError("runtime assertion overall status is invalid")
    return {**sections, "overall": overall, "evidence_state": evidence_state}


def connector_narrative(connector: str, evidence_state: str) -> str:
    require_connector(connector)
    narratives = {
        "apache": (
            "Apache uses the real httpd path with the ModSecurity module and the live CRS case. "
            "Only the fixed apache summary can support the displayed case assertion; fields not in "
            "that structured contract are reported as not available."
        ),
        "haproxy": (
            "HAProxy uses the real HAProxy-plus-SPOA path and evaluates only its fixed local summary. "
            "Artifact publication remains skipped by the existing same-UID/symlink security policy; "
            "that publication skip is separate from local runtime evidence."
        ),
        "envoy": (
            "Envoy uses the real ext_proc path with correlated live requests. Its displayed proof is "
            "carried by the normalized event and runtime attestation."
        ),
        "lighttpd": (
            "Lighttpd uses the patched native module path with host-transaction correlation and "
            "validated audit/wire evidence, projected into the normalized event and runtime attestation."
        ),
        "traefik": (
            "Traefik uses the native middleware path with correlated live requests; the normalized "
            "event and runtime attestation carry the displayed evidence."
        ),
    }
    text = narratives[connector]
    if evidence_state == "unavailable":
        return text + " Structured runtime evidence was missing or did not validate, so unavailable assertions were not promoted."
    if evidence_state == "not_run":
        return text + " The runtime step did not run, so no assertion is reported as PASS."
    return text


def _require_trusted_directory(descriptor: int) -> None:
    details = os.fstat(descriptor)
    if (
        not stat.S_ISDIR(details.st_mode)
        or details.st_uid != os.geteuid()
        or details.st_mode & 0o022
    ):
        raise ValueError("GitHub step summary directory is unsafe")


def _open_github_step_summary(environment: Mapping[str, str]) -> int:
    runner_temp_value = environment.get("RUNNER_TEMP", "")
    summary_value = environment.get("GITHUB_STEP_SUMMARY", "")
    runner_temp = Path(runner_temp_value)
    runner_descriptor = -1
    summary_parent_descriptor = -1
    summary_descriptor = -1
    try:
        if not summary_value:
            raise ValueError("GitHub step summary path is unavailable")
        nofollow, directory, nonblock, close_on_exec = _safe_open_flags()
        runner_descriptor = _open_directory_without_symlinks(runner_temp)
        _require_trusted_directory(runner_descriptor)
        summary_path = Path(summary_value)
        if (
            not summary_path.is_absolute()
            or os.path.normpath(summary_value) != summary_value
        ):
            raise ValueError(UNSAFE_SUMMARY_PATH)
        try:
            relative = summary_path.relative_to(runner_temp)
        except ValueError as error:
            raise ValueError(UNSAFE_SUMMARY_PATH) from error
        if (
            len(relative.parts) != 2
            or relative.parts[0] != SUMMARY_DIRECTORY_NAME
            or not SUMMARY_FILE_NAME.fullmatch(relative.parts[1])
        ):
            raise ValueError(UNSAFE_SUMMARY_PATH)
        summary_parent_descriptor = os.open(
            SUMMARY_DIRECTORY_NAME,
            os.O_RDONLY | directory | nofollow | close_on_exec,
            dir_fd=runner_descriptor,
        )
        _require_trusted_directory(summary_parent_descriptor)
        summary_descriptor = os.open(
            relative.parts[1],
            os.O_WRONLY | os.O_APPEND | nofollow | nonblock | close_on_exec,
            dir_fd=summary_parent_descriptor,
        )
        details = os.fstat(summary_descriptor)
        if (
            not stat.S_ISREG(details.st_mode)
            or details.st_uid != os.geteuid()
            or details.st_mode & 0o022
            or details.st_nlink != 1
        ):
            raise ValueError("GitHub step summary file is unsafe")
        result = summary_descriptor
        summary_descriptor = -1
        return result
    except OSError as error:
        raise ValueError(UNSAFE_SUMMARY_PATH) from error
    finally:
        if runner_descriptor >= 0:
            os.close(runner_descriptor)
        if summary_parent_descriptor >= 0:
            os.close(summary_parent_descriptor)
        if summary_descriptor >= 0:
            os.close(summary_descriptor)


def append_github_step_summary(environment: Mapping[str, str], content: str) -> None:
    descriptor = _open_github_step_summary(environment)
    try:
        _write_summary(descriptor, content)
    finally:
        os.close(descriptor)


def main(arguments: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector", required=True)
    parser.add_argument("--runner-temp", default="")
    parser.add_argument("--parent-sha", default="")
    parser.add_argument("--framework-sha", default="")
    parser.add_argument("--run-id", default="")
    args = parser.parse_args(arguments)
    try:
        append_github_step_summary(
            os.environ,
            render_summary(
                args.connector,
                outcomes_from_environment(os.environ),
                evidence_context={
                    "runner_temp": args.runner_temp,
                    "parent_sha": args.parent_sha,
                    "framework_sha": args.framework_sha,
                    "run_id": args.run_id,
                },
            ),
        )
    except (OSError, ValueError) as error:
        print(f"FAIL: {error}", file=os.sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
