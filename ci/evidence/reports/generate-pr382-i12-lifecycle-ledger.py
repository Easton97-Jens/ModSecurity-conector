#!/usr/bin/env python3
"""Bind reviewed Parent I12 host measurements to the unchanged original catalog.

This acceptance ledger does not create observations. A Root-reviewed verdict
requires physical evidence for every applicable field. Parser-only passes and
historical partial executions remain separate from full host lifecycle results.
"""
import argparse
import copy
import importlib.util
import json
from pathlib import Path


def oracle_module():
    path = Path(__file__).with_name("generate-pr382-i12-oracle-reconciliation.py")
    spec = importlib.util.spec_from_file_location("i12_original_oracles", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ORACLES = oracle_module()
ROLES = {
    "product_host_identity": {"loaded_image", "isolation_receipt"},
    "source_config_binding": {"source_manifest", "effective_configuration"},
    "capability": {"host_callback", "source_contract"},
    "client_exit": {"client_process"},
    "client_signal": {"client_process"},
    "client_headers": {"client_process"},
    "client_bytes": {"client_process"},
    "client_sha256": {"client_process"},
    "backend_request_count": {"backend_process"},
    "backend_payload_identity": {"backend_process", "client_process"},
    "client_backend_correlation": {"backend_process", "client_process"},
    "native_events": {"physical_event_sink"},
    "native_api_returns": {"native_api"},
    "native_transaction_id": {"native_api"},
    "common_transaction_id": {"native_api"},
    "observed_handle_association": {"native_api"},
    "native_phases": {"native_api", "native_debug"},
    "native_body_chunks": {"native_api"},
    "native_intervention_or_first_cause": {"native_api"},
    "host_eos": {"host_callback"},
    "native_eos": {"native_api", "host_callback"},
    "commit_order": {"host_callback", "client_process"},
    "mime_gate": {"native_debug", "physical_event_sink"},
    "finish_calls": {"native_api"},
    "finish_transitions": {"native_api"},
    "native_free_calls": {"native_api"},
    "cleanup_receipts": {"cleanup_observer", "isolation_receipt"},
    "descriptor_cleanup": {"cleanup_observer"},
    "process_listener_cleanup": {"cleanup_observer", "isolation_receipt"},
    "neighbor_health": {"client_process", "backend_process"},
    "transport_framing": {"client_process"},
    "transport_reset_scope": {"client_process", "host_callback"},
    "host_action": {"host_callback", "client_process"},
    "physical_event_order": {"physical_event_sink"},
    "terminal_event_count": {"physical_event_sink"},
}
# These observations are required even for a request-only route or an early deny.
ALWAYS_APPLICABLE = frozenset((
    "product_host_identity", "source_config_binding", "capability", "client_exit",
    "client_signal", "client_headers", "client_bytes", "client_sha256",
    "backend_request_count", "native_api_returns", "native_transaction_id",
    "observed_handle_association", "native_phases", "native_intervention_or_first_cause",
    "finish_calls", "native_free_calls", "cleanup_receipts", "descriptor_cleanup",
    "process_listener_cleanup", "neighbor_health", "transport_framing", "host_action",
))
REQUIRED_ROLES = {
    "product_host_identity": {"loaded_image", "isolation_receipt"},
    "source_config_binding": {"source_manifest", "effective_configuration"},
    "capability": {"host_callback", "source_contract"},
    "backend_payload_identity": {"backend_process", "client_process"},
    "client_backend_correlation": {"backend_process", "client_process"},
    "native_eos": {"native_api", "host_callback"},
    "commit_order": {"host_callback", "client_process"},
    "cleanup_receipts": {"cleanup_observer", "isolation_receipt"},
    "process_listener_cleanup": {"cleanup_observer", "isolation_receipt"},
    "neighbor_health": {"client_process", "backend_process"},
}


def measurement(field, supplied, packet_path):
    """Missing data stays unknown; source contracts cannot substitute for calls."""
    item = copy.deepcopy(supplied)
    applicable = item.get("applicable", True)
    value = item.get("value")
    if applicable is False:
        if field in ALWAYS_APPLICABLE or value is not None or not item.get("reason"):
            raise ValueError(f"Invalid nonapplicability for {field}")
        proofs = [ORACLES.verify_reference(ref) for ref in item.get("capability_proof", [])]
        if not proofs or any(ref.get("role") != "source_contract" for ref in proofs):
            raise ValueError(f"Nonapplicability needs a source-bound capability proof: {field}")
        item["capability_proof"] = proofs
        return item, True
    if applicable is not True:
        raise ValueError("Applicability must be a literal boolean")
    if value is None:
        if not item.get("reason"):
            raise ValueError(f"Unknown observation needs an exact missing reason: {field}")
        return item, False
    proofs = [ORACLES.verify_reference(ref) for ref in item.get("evidence", [])]
    if not proofs or any(ref.get("role") not in ROLES[field] for ref in proofs):
        raise ValueError(f"Observation has no suitable physical producer: {field}")
    if not REQUIRED_ROLES.get(field, set()) <= {ref.get("role") for ref in proofs}:
        raise ValueError(f"Independent producers are missing for {field}")
    if any(ref["path"] == str(packet_path) for ref in proofs):
        raise ValueError("A reviewed packet cannot be its own measurement")
    if field != "capability" and all(ref.get("role") == "source_contract" for ref in proofs):
        raise ValueError("A source contract does not prove actual execution")
    item["evidence"] = proofs
    return item, True


def reviewed_packet(supplied, row, effective_oracle):
    ref = ORACLES.verify_reference(supplied)
    path = Path(ref["path"])
    packet = json.loads(path.read_text())
    if packet.get("reviewed_by") != "root":
        raise ValueError("Host packet requires explicit Root review")
    if (packet.get("run_scoped_case_id") != row["run_scoped_case_id"] or
            packet.get("leg_id") != row["leg_id"]):
        raise ValueError("Packet cannot transfer to a sibling route or case")
    if packet.get("execution_observed") is not True or packet.get("execution_kind") != "host_http":
        raise ValueError("A full lifecycle packet requires an actual host HTTP transaction")
    for name in ("run_id", "parent_sha", "framework_sha", "mrts_sha", "effective_config_sha256"):
        if not packet.get(name):
            raise ValueError(f"Missing actual packet identity: {name}")
    if set(packet.get("observations", {})) != set(ROLES):
        raise ValueError("Packet must preserve every prescribed observation field")
    values, known = {}, []
    for name, observation in packet["observations"].items():
        values[name], complete = measurement(name, observation, path)
        known.append(complete)
    evaluated = packet.get("oracle_evaluated") is True
    if evaluated and (effective_oracle is None or
                      packet.get("oracle_sha256") != ORACLES.canonical_digest(effective_oracle)):
        raise ValueError("Evaluation does not bind the independently reviewed effective oracle")
    verdict = packet.get("outcome")
    if verdict not in (None, "PASS", "FAIL"):
        raise ValueError("A driver exit or transport result is not a lifecycle verdict")
    full = all(known) and evaluated and verdict is not None
    if packet.get("full_lifecycle_qualified") is True and not full:
        raise ValueError("A missing observation or unresolved oracle prevents full qualification")
    return {"receipt": ref, "observations": values, "execution_observed": True,
            "full_lifecycle_qualified": full, "outcome": verdict if full else None,
            "unknown_fields": [name for name, item in values.items()
                               if item.get("applicable", True) and item.get("value") is None]}


def build_ledger(requirements, selection, reconciliation, packets):
    original = ORACLES.original_contracts(requirements, selection)
    if reconciliation["original_selected_contracts"] != [row["selected_requirement"] for row in original]:
        raise ValueError("Reconciliation does not preserve the original selected catalog")
    reviews = {row["run_scoped_case_id"]: row for row in
               reconciliation["oracle_matrix"] + reconciliation["supplemental_dispositions"]}
    by_id = {row["run_scoped_case_id"]: row for row in original}
    observations = {}
    for ref in packets:
        packet = json.loads(Path(ORACLES.verify_reference(ref)["path"]).read_text())
        identity = packet["run_scoped_case_id"]
        if identity not in by_id or identity in observations:
            raise ValueError("Unknown or duplicate original packet ID")
        review = reviews.get(identity)
        oracle = review["effective_oracle"] if review else by_id[identity]["selected_requirement"]["expected_oracle"]
        if oracle and oracle.get("unresolved_expected_value_reason"):
            oracle = None
        observations[identity] = reviewed_packet(ref, by_id[identity], oracle)
    rows = []
    for original_row in original:
        row = copy.deepcopy(original_row)
        identity = row["run_scoped_case_id"]
        row["historical_status"] = row["status"]
        row["historical_execution_observed"] = row["execution_observed"]
        row["oracle_reconciliation"] = copy.deepcopy(reviews.get(identity))
        row["current_lifecycle_packet"] = observations.get(identity)
        row["qualified_host_lifecycle_pass"] = False
        row["qualification_scope"] = "historical_configuration_only" if row["status"] == "PASS" else None
        if identity in observations:
            observation = observations[identity]
            row["execution_observed"] = True
            if observation["full_lifecycle_qualified"]:
                row["status"] = observation["outcome"]
                row["qualified_full_case_pass"] = observation["outcome"] == "PASS"
                row["qualified_host_lifecycle_pass"] = observation["outcome"] == "PASS"
                row["qualification_scope"] = "full_host_lifecycle"
            else:
                row["status"] = "PARTIAL_HOST_MEASUREMENTS"
                row["qualified_full_case_pass"] = False
        rows.append(row)
    full = [row for row in rows if row["qualification_scope"] == "full_host_lifecycle"]
    required_full_pass = [row for row in full if row["required_leg"] and row["status"] == "PASS"]
    return {"schema_version": 1, "original_ordered_id_sha256": ORACLES.ID_SHA256,
            "original_selected_contract_sha256": ORACLES.CONTRACT_SHA256,
            "summary": {
                "original_ids": len(rows), "actually_executed_ids": sum(row["execution_observed"] is True for row in rows),
                "configuration_only_pass": sum(row["qualification_scope"] == "historical_configuration_only" for row in rows),
                "full_lifecycle_pass": sum(row["status"] == "PASS" for row in full),
                "full_lifecycle_fail": sum(row["status"] == "FAIL" for row in full),
                "required_full_lifecycle_pass": len(required_full_pass),
                "required_full_lifecycle_fail": sum(row["required_leg"] and row["status"] == "FAIL" for row in full),
                "required_qualified_pass": sum(row["required_leg"] and row["status"] == "PASS" for row in rows),
                "required_qualified_fail": sum(row["required_leg"] and row["status"] == "FAIL" for row in rows),
                "required_routes_with_full_case": len({row["leg_id"] for row in required_full_pass}),
                "unqualified_ids": sum(row["qualification_scope"] is None for row in rows),
                "oracle_counts": copy.deepcopy(reconciliation["summary"]),
            }, "rows": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("requirements", "original-selection", "reconciliation", "reviewed-packets", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    result = build_ledger(json.loads(args.requirements.read_text()), json.loads(args.original_selection.read_text()),
                          json.loads(args.reconciliation.read_text()),
                          json.loads(args.reviewed_packets.read_text())["packets"])
    with args.output.open("x", encoding="utf-8") as output:
        json.dump(result, output, indent=2, ensure_ascii=False)
        output.write("\n")


if __name__ == "__main__":
    main()
