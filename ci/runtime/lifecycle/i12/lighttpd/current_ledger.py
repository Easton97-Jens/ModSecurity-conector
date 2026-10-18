#!/usr/bin/env python3
"""Export current lighttpd results after re-running the existing I12 validators.

The inherited exports remain immutable inputs. This exporter assigns no verdict:
it only records the shared qualifier's result and keeps historical credit apart.
"""
from __future__ import annotations

import argparse
import copy
from collections import Counter, defaultdict
import importlib.util
import json
from pathlib import Path


SPEC = importlib.util.spec_from_file_location(
    "lighttpd_qualification_adapter", Path(__file__).with_name("qualification.py"))
Q = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(Q)


def load_reference(ref):
    value, actual = Q._read_physical(ref["path"])
    if (actual["sha256"] != ref.get("sha256")
            or ("bytes" in ref and actual["bytes"] != ref["bytes"])):
        raise ValueError("Evidence content or byte length differs from its recorded SHA256")
    return value


def current_result(path):
    """Revalidate raw evidence, oracle and packet instead of trusting saved PASS."""
    result = load_reference(Q.reference(path))
    sources = result.get("qualifier_sources", [])
    if (len(sources) != len(Q.LOADED_SOURCES)
            or len({ref.get("original_source_path") for ref in sources}) != len(sources)
            or any(ref.get("role") != "qualification_source" for ref in sources)):
        raise ValueError("Current result needs the immutable executed qualification sources")
    for source in sources:
        Q.ORACLES.verify_reference(source)
    row = Q.original_row(result["run_scoped_case_id"])
    root_review = load_reference(result["root_review"])
    packet_proposal = Q.ORACLES.verify_reference(result["proposal"])
    oracle_proposal = Q.ORACLES.verify_reference(result["oracle_proposal"])
    if (root_review.get("reviewed_by") != "root"
            or root_review.get("packet_sha256") != packet_proposal["sha256"]
            or root_review.get("oracle_record_sha256") != oracle_proposal["sha256"]
            or root_review.get("run_scoped_case_id") != row["run_scoped_case_id"]):
        raise ValueError("Current result lost its exact separate Root review")
    record = load_reference(Q.reference(Path(path).parent / "root-reviewed-record.json"))
    expected_record = copy.deepcopy(load_reference(oracle_proposal))
    expected_record["reviewed_by"] = "root"
    if expected_record.get("approved_correction") is not None:
        expected_record["approved_correction"]["reviewed_by"] = "root"
    if record != expected_record:
        raise ValueError("Reviewed oracle changed after its separate exact-file approval")
    review = Q.ORACLES.review_record(record, row)
    if review != result["oracle_review"]:
        raise ValueError("Saved oracle review differs from current shared reconciliation")
    packet_ref = result["qualifier"]["receipt"]
    packet = load_reference(packet_ref)
    expected_packet = Q.reviewed_proposal(load_reference(packet_proposal), root_review)
    if packet != expected_packet:
        raise ValueError("Reviewed packet changed after its separate exact-file approval")
    parser = packet.get("execution_kind") == "configuration_parser"
    validator = Q.packet_validator(packet)
    qualification = validator(packet_ref, row, review["effective_oracle"])
    if qualification != result["qualifier"]:
        raise ValueError("Saved qualification differs from current shared qualifier")
    dedicated = parser or packet["execution_kind"] == "host_pre_native_rejection"
    clients = packet["measurement_evidence"] if dedicated else packet["observations"]["client_exit"].get("evidence", [])
    producer_role = "parser_process" if parser else "client_process"
    physical_clients = sorted({(item["path"], item["sha256"]) for item in clients
                               if item.get("role") == producer_role})
    if not physical_clients:
        raise ValueError("Cannot count an actual execution without its physical process producer")
    return result, packet, physical_clients


def execution_inventory(path):
    """Retain reviewed capture coverage without assigning qualification credit."""
    if path is None:
        return {}, None
    ref = Q.reference(path)
    document = load_reference(ref)
    if (document.get("schema") != "lighttpd-i12-execution-index-v1"
            or document.get("reviewed_by") != "root" or not document.get("independent_review")):
        raise ValueError("Execution coverage requires a separate Root-reviewed index")
    indexed = {}
    permitted = {"PARTIAL_HOST_MEASUREMENTS", "PARTIAL_CONFIGURATION_MEASUREMENTS",
                 "HOST_START_ONLY", "NOT_EXECUTED_UNQUALIFIED", "UNSUPPORTED_CAPABILITY",
                 "ENVIRONMENT_BLOCKED"}
    for item in document["rows"]:
        identity = item["run_scoped_case_id"]
        row = Q.original_row(identity)
        if identity in indexed or item.get("original_row_sha256") != row["original_row_sha256"]:
            raise ValueError("Capture coverage changed or duplicated an original ID")
        if item.get("status") not in permitted or not item.get("remaining_reason"):
            raise ValueError("Capture coverage cannot assign a qualified verdict")
        evidence = [Q.ORACLES.verify_reference(r) for r in item.get("capture_refs", [])]
        processes = [Q.ORACLES.verify_reference(r) for r in item.get("process_producers", [])]
        observed = item.get("execution_observed")
        kind = item.get("execution_kind")
        if observed is not None and type(observed) is not bool:
            raise ValueError("Capture execution observation must remain explicit")
        if observed is True:
            role = {"host_http": "client_process", "configuration_parser": "parser_process"}.get(kind)
            if not evidence or not processes or role is None or any(p.get("role") != role for p in processes):
                raise ValueError("An executed original needs its physical independent process producers")
        elif processes:
            raise ValueError("Unexecuted coverage cannot count an HTTP/parser process")
        if item["status"] in ("UNSUPPORTED_CAPABILITY", "ENVIRONMENT_BLOCKED") and not evidence:
            raise ValueError("Capability or environment disposition requires concrete evidence")
        if item["status"] in ("HOST_START_ONLY", "NOT_EXECUTED_UNQUALIFIED") and observed is True:
            raise ValueError("A host start cannot count as an original HTTP execution")
        if item["status"] == "UNSUPPORTED_CAPABILITY" and item.get("oracle_record") is None:
            raise ValueError("Unsupported coverage requires the per-ID existing oracle reconciliation")
        indexed[identity] = {**copy.deepcopy(item), "capture_refs": evidence,
                             "process_producers": processes}
        if item.get("oracle_record") is not None:
            record = load_reference(item["oracle_record"])
            if record.get("reviewed_by") != "root" or record.get("run_scoped_case_id") != identity:
                raise ValueError("Capture oracle disposition needs Root review of this exact original ID")
            reviewed = Q.ORACLES.review_record(record, row)
            if item["status"] == "UNSUPPORTED_CAPABILITY" and reviewed["category"] != "UNSUPPORTED_CAPABILITY":
                raise ValueError("Unsupported coverage needs the existing per-ID capability reconciliation")
            indexed[identity]["oracle_review"] = reviewed
    return indexed, ref


def capture_only_result(capture, inventory_ref):
    """A physical execution can remain unqualified, even if its worker says PASS."""
    return {
        "qualification": None, "status": capture["status"],
        "execution_observed": capture["execution_observed"],
        "full_lifecycle_qualified": False, "full_case_qualified": False,
        "scope": "capture_only", "execution_kind": capture.get("execution_kind"),
        "oracle_resolved": capture.get("oracle_review", {}).get("resolved"),
        "oracle_review": capture.get("oracle_review"),
        "unknown_fields": capture.get("missing_observations", []),
        "actual_client_producers": capture.get("process_producers", []),
        "root_reviewed_execution_inventory": inventory_ref,
    }


def producer_identity(producers):
    """A copied receipt is the same execution witness, regardless of its path."""
    return tuple(sorted({item["sha256"] for item in producers}))


def base_case(row, cases_ref, index, original_oracle):
    return {
        "run_scoped_case_id": row["run_scoped_case_id"], "leg_id": row["leg_id"],
        "required_leg": row["required_leg"],
        "original_contract": {**cases_ref, "json_pointer": f"/rows/{index}/selected_requirement",
                              "canonical_sha256": Q.ORACLES.canonical_digest(row["selected_requirement"])},
        "baseline_original_row_sha256": row["original_row_sha256"],
        "historical": {key: row.get(key) for key in
                       ("status", "execution_observed", "qualification_scope",
                        "qualified_host_lifecycle_pass", "qualified_full_case_pass")},
        "original_oracle": original_oracle,
        "current": None, "capture_history": None, "new_evidence_refs": [],
        "remaining_reason": "No current Root-reviewed qualified execution for this exact original ID.",
    }


def qualified_result(result, packet, clients, row, result_ref):
    qualifier = result["qualifier"]
    full_case = qualifier.get("full_case_qualified", qualifier["full_lifecycle_qualified"])
    http = packet["execution_kind"] in ("host_http", "host_pre_native_rejection")
    return {
        "qualification": result_ref, "status": result["status"],
        "execution_observed": qualifier["execution_observed"],
        "full_lifecycle_qualified": row["required_leg"] and qualifier["full_lifecycle_qualified"],
        "full_case_qualified": full_case,
        "diagnostic_host_qualified": not row["required_leg"] and http and full_case,
        "scope": qualifier.get("qualification_scope", "mandatory_host" if row["required_leg"] else "diagnostic_host"),
        "execution_kind": packet["execution_kind"],
        "run_id": packet["run_id"], "parent_sha": packet["parent_sha"],
        "effective_config_sha256": packet["effective_config_sha256"],
        "oracle_resolved": result["oracle_review"]["resolved"],
        "effective_oracle": result["oracle_review"]["effective_oracle"],
        "unknown_fields": qualifier["unknown_fields"],
        "actual_client_producers": [{"path": p, "sha256": h} for p, h in clients],
    }


def route_export(route, revisions, results, captures=None, inventory_ref=None):
    cases_path = Q.BASELINE / (route + "-cases.json")
    oracle_path = Q.BASELINE / (route + "-oracles.json")
    cases_ref, oracle_ref = Q.reference(cases_path), Q.reference(oracle_path)
    inherited = load_reference(cases_ref)
    oracles = {r["run_scoped_case_id"]: r for r in load_reference(oracle_ref)["rows"]}
    rows, executions, execution_producers = [], defaultdict(list), {}
    captures = captures or {}
    for index, row in enumerate(inherited["rows"]):
        case_id = row["run_scoped_case_id"]
        old_oracle = oracles.get(case_id)
        entry = base_case(row, cases_ref, index, old_oracle)
        if case_id in captures:
            capture = captures[case_id]
            entry["capture_history"] = capture
            entry["current"] = capture_only_result(capture, inventory_ref)
            entry["remaining_reason"] = capture["remaining_reason"]
            entry["new_evidence_refs"] = [inventory_ref, *capture["capture_refs"],
                                           *capture["process_producers"]]
            if capture["execution_observed"] is True:
                key = producer_identity(capture["process_producers"])
                execution_producers.setdefault(key, capture["process_producers"])
                executions[key].append(case_id)
        if case_id in results:
            result, packet, clients, result_ref = results[case_id]
            qualifier = result["qualifier"]
            entry["current"] = qualified_result(result, packet, clients, row, result_ref)
            entry["new_evidence_refs"] += result["new_evidence_refs"] + [result_ref]
            entry["remaining_reason"] = None if entry["current"]["full_case_qualified"] else "Missing: " + ", ".join(qualifier["unknown_fields"])
            producers = [{"path": p, "sha256": h} for p, h in clients]
            key = producer_identity(producers)
            execution_producers.setdefault(key, producers)
            if case_id not in executions[key]:
                executions[key].append(case_id)
        rows.append(entry)
    summary = summarize(rows, inherited["summary"], oracles)
    return {"schema": "lighttpd-i12-current-ledger-v1", "route": route,
            "revision_binding": revisions, "baseline": [cases_ref, oracle_ref],
            "summary": summary,
            "actual_executions": [{"client_producers": execution_producers[key],
                                   "original_ids": ids, "unique_execution_count": 1}
                                  for key, ids in executions.items()], "rows": rows}


def summarize(rows, inherited, oracles):
    current = [row for row in rows if row["current"] is not None]
    verdicts = Counter(row["current"]["status"] for row in current)
    new_full = [row for row in current if row["current"]["full_case_qualified"]]
    historical_ids = {row["run_scoped_case_id"] for row in rows
                      if row["historical"]["qualification_scope"] is not None}
    current_ids = {row["run_scoped_case_id"] for row in new_full}
    newly_resolved = [row for row in current if row["run_scoped_case_id"] in oracles
                      and not oracles[row["run_scoped_case_id"]]["resolved"]
                      and row["current"]["oracle_resolved"]]
    return {
        "original_ids": len(rows), "historical": inherited,
        "current_executed_original_ids": sum(r["current"]["execution_observed"] is True for r in current),
        "current_unique_http_executions": len({producer_identity(row["current"]["actual_client_producers"]) for row in current
             if row["current"]["execution_kind"] in ("host_http", "host_pre_native_rejection") and row["current"]["execution_observed"] is True}),
        "current_unique_parser_executions": len({producer_identity(row["current"]["actual_client_producers"]) for row in current
             if row["current"]["execution_kind"] == "configuration_parser" and row["current"]["execution_observed"] is True}),
        "current_verdicts": dict(verdicts),
        "current_qualified_verdicts": dict(Counter(r["current"]["status"] for r in new_full)),
        "current_required_host_lifecycle_pass": sum(r["required_leg"] and r["current"]["full_lifecycle_qualified"]
            and r["current"]["status"] == "PASS" for r in current),
        "current_diagnostic_host_pass": sum(r["current"].get("diagnostic_host_qualified", False)
            and r["current"]["status"] == "PASS" for r in current),
        "current_configuration_pass": sum(r["current"].get("scope") == "configuration_control"
            and r["current"]["full_case_qualified"] and r["current"]["status"] == "PASS" for r in current),
        "newly_qualified_original_ids": len(current_ids - historical_ids),
        "currently_unqualified_original_ids": len(rows) - len(historical_ids | current_ids),
        "newly_resolved_original_oracles": len(newly_resolved),
        "remaining_open_original_oracles": inherited["unresolved_original_oracles"] - len(newly_resolved),
    }


def export(paths, revisions, output, execution_index=None):
    captures, inventory_ref = execution_inventory(execution_index)
    indexed = {}
    for path in paths:
        result, packet, clients = current_result(path)
        identity = result["run_scoped_case_id"]
        if identity in indexed:
            raise ValueError("Multiple selected current results for the same original ID")
        indexed[identity] = result, packet, clients, Q.reference(path)
    output = Path(output)
    if output.exists() or output.is_symlink():
        raise ValueError("Use a fresh output directory; inherited exports are immutable")
    if output.absolute().resolve() != output.absolute():
        raise ValueError("Current ledger output must have physical parents")
    output.mkdir(parents=True, mode=0o700)
    summaries = {}
    for route in Q.ROUTES:
        result = route_export(route, revisions, indexed, captures, inventory_ref)
        Q._exclusive_json(output / (route + ".json"), result)
        summaries[route] = result["summary"]
    Q._exclusive_json(output / "summary.json", {"revision_binding": revisions, "routes": summaries})
    return summaries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qualifications", required=True, type=Path)
    parser.add_argument("--revisions", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--execution-index", type=Path)
    args = parser.parse_args()
    manifest = load_reference(Q.reference(args.qualifications))
    paths = [Q.ORACLES.verify_reference(ref)["path"] for ref in manifest["qualifications"]]
    revisions = load_reference(Q.reference(args.revisions))
    print(json.dumps(export(paths, revisions, args.output, args.execution_index), indent=2))


if __name__ == "__main__":
    main()
