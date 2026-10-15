#!/usr/bin/env python3
"""Bind reviewed Parent I12 host measurements to the unchanged original catalog.

This acceptance ledger does not create observations. A Root-reviewed verdict
requires physical evidence for every applicable field. Parser-only passes and
historical partial executions remain separate from full host lifecycle results.
"""
import argparse
import copy
import hashlib
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
CONFIGURATION_FIELDS = (
    "actual-config-parser-argv-cwd-exit-signal-stderr",
    "source-host-module-effective-config-identity",
    "expected-parser-acceptance-or-rejection",
)
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
    "mime_gate": {"native_debug", "physical_event_sink", "native_api"},
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


def validate_configuration_identity(packet, row, effective_oracle):
    selected = row["selected_requirement"]
    if selected.get("execution_kind") != "actual_configtest":
        raise ValueError("Only an original actual_configtest contract permits parser qualification")
    if set(selected.get("mandatory_missing_observations", [])) != set(CONFIGURATION_FIELDS):
        raise ValueError("Parser qualification must preserve the original three observations")
    if (packet.get("reviewed_by") != "root"
            or packet.get("run_scoped_case_id") != row["run_scoped_case_id"]
            or packet.get("leg_id") != row["leg_id"]):
        raise ValueError("Configuration packet requires Root review of the exact original ID")
    if packet.get("execution_kind") != "configuration_parser" or packet.get("execution_observed") is not True:
        raise ValueError("Configuration qualification requires an observed parser process")
    if packet.get("full_lifecycle_qualified") is True:
        raise ValueError("Configuration qualification cannot claim a host lifecycle")
    for name in ("run_id", "parent_sha", "effective_config_sha256"):
        if not packet.get(name):
            raise ValueError(f"Missing parser identity: {name}")
    absent_rules = packet.get("rules_absence_sha256")
    if absent_rules:
        if (row["run_scoped_case_id"].split("::")[-1] != "missing_rules_file"
                or "rules_sha256" not in packet or packet["rules_sha256"] is not None):
            raise ValueError("Rules absence is only valid for the original missing-rules contract; unloaded rules stay null")
    elif not packet.get("rules_sha256"):
        raise ValueError("Missing parser identity: rules_sha256")
    if (packet.get("oracle_evaluated") is not True or effective_oracle is None
            or packet.get("oracle_sha256") != ORACLES.canonical_digest(effective_oracle)):
        raise ValueError("Parser evaluation must bind the independently reviewed effective oracle")


def configuration_measurements(packet, ref):
    roles = {"parser_process", "source_manifest", "effective_configuration", "invoked_image",
             "cleanup_observer", "isolation_receipt", "native_module",
             "parser_stdout", "parser_stderr", "expectation_source"}
    roles.add("rules_absence" if packet.get("rules_absence_sha256") else "rules_file")
    evidence = [ORACLES.verify_reference(item) for item in packet.get("measurement_evidence", [])]
    if roles != {item.get("role") for item in evidence} or len(evidence) != len(roles):
        raise ValueError("Parser packet lacks independent process, image, source/config or cleanup producers")
    if any(item["path"] == ref["path"] for item in evidence):
        raise ValueError("Parser packet cannot be its own measurement")
    observed = packet.get("actual_observations", {})
    process = observed.get("parser_process", {})
    if (not process.get("argv") or not process.get("cwd")
            or type(process.get("waited_exit")) is not int
            or "waited_signal" not in process or "stdout" not in process or "stderr" not in process):
        raise ValueError("Parser packet needs actual argv/cwd/exit/signal/stdout/stderr")
    for name in ("invocation_identity", "source_config_binding", "cleanup"):
        if not observed.get(name):
            raise ValueError(f"Parser packet lacks actual {name}")
    producers = {item["role"]: item for item in evidence}
    configuration_process_binding(packet, process, producers)
    configuration_source_binding(packet, observed, producers)
    independent = producers["expectation_source"]
    implementation_hashes = {item["sha256"] for item in evidence if item["role"] != "expectation_source"}
    if (independent.get("kind") not in ORACLES.INDEPENDENT_KINDS or not independent.get("revision")
            or independent["sha256"] in implementation_hashes):
        raise ValueError("Parser expectation requires a separate revisioned independent source")
    return observed


def configuration_process_binding(packet, process, producers):
    """Match a physical parser receipt; the driver's exit cannot substitute."""
    actual = json.loads(Path(producers["parser_process"]["path"]).read_text())
    for name in ("run_scoped_case_id", "leg_id", "run_id", "parent_sha", "effective_config_sha256", "rules_sha256",
                 "execution_kind", "execution_observed"):
        if actual.get(name) != packet[name]:
            raise ValueError(f"Parser process identity differs: {name}")
    if packet.get("rules_absence_sha256"):
        configuration_rules_absence(packet, actual, producers["rules_absence"])
    for name in ("argv", "cwd", "waited_exit", "waited_signal", "stdout", "stderr", "executable_sha256"):
        if name not in process or actual.get(name) != process[name]:
            raise ValueError(f"Parser observation differs from physical process: {name}")
    if (not isinstance(process["argv"], list) or not process["argv"]
            or any(not isinstance(arg, str) or not arg for arg in process["argv"])
            or not isinstance(process["cwd"], str) or not Path(process["cwd"]).is_absolute()
            or process["executable_sha256"] != producers["invoked_image"]["sha256"]):
        raise ValueError("Actual parser argv/cwd/executable identity is required")
    for stream in ("stdout", "stderr"):
        content = process[stream]
        if not isinstance(content, str) or hashlib.sha256(content.encode()).hexdigest() != producers["parser_" + stream]["sha256"]:
            raise ValueError(f"Parser {stream} differs from physical stream bytes")


def configuration_rules_absence(packet, actual, ref):
    """The attempted missing path has an absence receipt, never a file hash."""
    absence = json.loads(Path(ref["path"]).read_text())
    if (absence.get("type") != "physical_path_absence" or absence.get("exists") is not False
            or absence.get("measurement") != "lstat" or absence.get("errno") != 2
            or absence.get("symlink_components") != [] or actual.get("rules_lstat_errno") != 2
            or not isinstance(absence.get("rules_path"), str) or not Path(absence["rules_path"]).is_absolute()
            or actual.get("rules_path") != absence["rules_path"] or actual.get("rules_exists") is not False
            or actual.get("rules_absence_sha256") != packet["rules_absence_sha256"]
            or ref["sha256"] != packet["rules_absence_sha256"]):
        raise ValueError("Missing rules need the actual attempted absolute path and physical absence measurement")
    for name in ("run_scoped_case_id", "leg_id", "run_id", "parent_sha"):
        if absence.get(name) != packet[name]:
            raise ValueError(f"Rules absence belongs to a different execution: {name}")


def configuration_source_binding(packet, observed, producers):
    """Bind every invoked image and effective parser input to physical bytes."""
    identity = observed["invocation_identity"]
    binding = observed["source_config_binding"]
    for field, role in (("host_binary_sha256", "invoked_image"), ("module_sha256", "native_module")):
        if identity.get(field) != producers[role]["sha256"]:
            raise ValueError(f"Parser image identity differs: {field}")
    rules_binding = (("rules_absence_sha256", "rules_absence") if packet.get("rules_absence_sha256")
                     else ("rules_sha256", "rules_file"))
    for field, role in (("effective_config_sha256", "effective_configuration"), rules_binding):
        if packet[field] != producers[role]["sha256"] or binding.get(field) != packet[field]:
            raise ValueError(f"Parser effective input identity differs: {field}")
    if packet.get("rules_absence_sha256") and binding.get("rules_sha256", "missing") is not None:
        raise ValueError("An unloaded missing rules file has no rules SHA256")
    source = json.loads(Path(producers["source_manifest"]["path"]).read_text())
    if binding.get("parent_sha") != packet["parent_sha"] or source.get("parent_sha") != packet["parent_sha"]:
        raise ValueError("Parser source revision differs from actual source manifest")
    cleanup = json.loads(Path(producers["cleanup_observer"]["path"]).read_text())
    if observed["cleanup"] != cleanup:
        raise ValueError("Parser cleanup differs from physical observer")


def reviewed_configuration_packet(supplied, row, effective_oracle):
    """Qualify an original parser contract without fabricating an HTTP lifecycle.

    This separate scope can only cover an original actual_configtest selection.
    It never contributes a full_host_lifecycle result or substitutes for body,
    transport, native transaction, finish or free measurements.
    """
    ref = ORACLES.verify_reference(supplied)
    packet = json.loads(Path(ref["path"]).read_text())
    validate_configuration_identity(packet, row, effective_oracle)
    observed = configuration_measurements(packet, ref)
    verdict = packet.get("outcome")
    if verdict not in ("PASS", "FAIL"):
        raise ValueError("Parser exit alone is not an evaluated configuration verdict")
    expected = effective_oracle.get("native_result")
    if (effective_oracle.get("phase") != 0
            or effective_oracle.get("physical_evidence_not_projection") is not True
            or effective_oracle.get("unresolved_expected_value_reason")
            or (expected, effective_oracle.get("visible_status")) not in (("config_accepted", 0), ("config_rejected", 1))):
        raise ValueError("Parser scope requires an explicit acceptance or rejection oracle")
    process = observed["parser_process"]
    matched = (process["waited_signal"] is None and process["waited_exit"] >= 0
               and process["waited_exit"] == effective_oracle["visible_status"])
    if verdict != ("PASS" if matched else "FAIL"):
        raise ValueError("Parser verdict contradicts actual exit/signal and independent oracle")
    return {"receipt": ref, "observations": observed, "execution_observed": True,
            "mandatory_observations": dict(zip(CONFIGURATION_FIELDS, (
                observed["parser_process"],
                {"invocation_identity": observed["invocation_identity"], "source_config_binding": observed["source_config_binding"]},
                {"expected_oracle": copy.deepcopy(effective_oracle), "oracle_sha256": packet["oracle_sha256"]}), strict=True)),
            "qualification_scope": "configuration_control", "full_case_qualified": True,
            "full_lifecycle_qualified": False, "outcome": verdict, "unknown_fields": []}


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
        reviewer = (reviewed_configuration_packet
                    if by_id[identity]["selected_requirement"].get("execution_kind") == "actual_configtest"
                    else reviewed_packet)
        observations[identity] = reviewer(ref, by_id[identity], oracle)
    rows = []
    for original_row in original:
        row = copy.deepcopy(original_row)
        identity = row["run_scoped_case_id"]
        row["historical_status"] = row["status"]
        row["historical_execution_observed"] = row["execution_observed"]
        row["oracle_reconciliation"] = copy.deepcopy(reviews.get(identity))
        observation = observations.get(identity)
        configuration = observation is not None and observation.get("qualification_scope") == "configuration_control"
        row["current_lifecycle_packet"] = None if configuration else observation
        row["current_configuration_packet"] = observation if configuration else None
        row["qualified_host_lifecycle_pass"] = False
        row["qualified_configuration_pass"] = False
        row["qualification_scope"] = "historical_configuration_only" if row["status"] == "PASS" else None
        if identity in observations:
            observation = observations[identity]
            row["execution_observed"] = True
            if configuration:
                row["status"] = observation["outcome"]
                row["qualified_full_case_pass"] = observation["outcome"] == "PASS"
                row["qualified_configuration_pass"] = observation["outcome"] == "PASS"
                row["qualification_scope"] = "configuration_control"
            elif observation["full_lifecycle_qualified"]:
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
                "current_configuration_pass": sum(row["qualification_scope"] == "configuration_control" and row["status"] == "PASS" for row in rows),
                "current_configuration_fail": sum(row["qualification_scope"] == "configuration_control" and row["status"] == "FAIL" for row in rows),
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
