#!/usr/bin/env python3
"""Bind reviewed Parent I12 host measurements to the unchanged original catalog.

This acceptance ledger does not create observations. A Root-reviewed verdict
requires physical evidence for every applicable field. Parser-only passes and
historical partial executions remain separate from full host lifecycle results.
"""
import argparse
import copy
import datetime
import hashlib
import importlib.util
import json
import re
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
    expected_exit = effective_oracle.get("visible_status")
    explicit_exit = (type(expected_exit) is int and
                     ((expected == "config_accepted" and expected_exit == 0) or
                      (expected == "config_rejected" and 1 <= expected_exit <= 255)))
    if (effective_oracle.get("phase") != 0
            or effective_oracle.get("physical_evidence_not_projection") is not True
            or effective_oracle.get("unresolved_expected_value_reason")
            or not explicit_exit):
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


PRE_NATIVE_MAPPING = {
    "invalid_content_length": ["invalid_content_length", "I12::apache-native::obligation::invalid-header"],
    "conflicting_content_length": ["conflicting_content_length"],
    "duplicate_transfer_encoding": ["duplicate_transfer_encoding"],
    "content_length_overflow": ["content_length_overflow", "I12::apache-native::obligation::size-overflow"],
}
PRE_NATIVE_ORACLE = {"native_result": "rejected_by_host_before_connector_or_connector_rejection",
                     "visible_status": 400, "rule_id": None, "phase": 1, "event_fields": [],
                     "physical_evidence_not_projection": True, "unresolved_expected_value_reason": None}
PRE_NATIVE_ROLES = frozenset((
    "client_process", "client_receipt", "request_wire", "response_wire", "native_api", "host_callback",
    "backend_process", "core_diagnostic", "event_observer", "source_manifest", "effective_configuration",
    "rules_file", "loaded_image", "native_module", "observer_image", "isolation_receipt", "cleanup_observer",
    "healthy_controls", "driver_observation",
))


def pre_native_identity(packet, row, oracle):
    selected = row["selected_requirement"]
    name = selected.get("case_id")
    if (name not in PRE_NATIVE_MAPPING or row.get("leg_id") != "apache-native"
            or row.get("run_scoped_case_id") != f"I12::apache-native::{name}"
            or selected.get("run_scoped_case_id") != row["run_scoped_case_id"]
            or selected.get("requirement_mapping") != PRE_NATIVE_MAPPING[name]
            or selected.get("expected_oracle") != PRE_NATIVE_ORACLE or oracle != PRE_NATIVE_ORACLE
            or type(oracle.get("phase")) is not int or type(oracle.get("visible_status")) is not int):
        raise ValueError("Pre-native scope requires one of four exact original Apache rejection contracts")
    if (packet.get("reviewed_by") != "root" or packet.get("execution_kind") != "host_pre_native_rejection"
            or packet.get("execution_observed") is not True or packet.get("oracle_evaluated") is not True
            or packet.get("oracle_sha256") != ORACLES.canonical_digest(oracle)
            or packet.get("full_lifecycle_qualified") is not False
            or packet.get("native_transaction_id") is not None):
        raise ValueError("Pre-native rejection cannot fabricate a native transaction or full lifecycle")
    for key in ("run_scoped_case_id", "leg_id"):
        if packet.get(key) != row[key]:
            raise ValueError("Pre-native packet belongs to another case/profile")
    for key in ("run_id", "parent_sha", "framework_sha", "mrts_sha", "effective_config_sha256", "rules_sha256",
                "request_id", "host_starttime"):
        if not packet.get(key):
            raise ValueError(f"Pre-native packet lacks actual identity: {key}")
    for key in ("host_pid", "uid"):
        if type(packet.get(key)) is not int or packet[key] <= 0:
            raise ValueError("Pre-native execution requires an actual isolated non-root host process")
    approval = packet.get("source_approval", {})
    digests = {"selected_requirement_sha256": ORACLES.canonical_digest(selected),
               "requirement_mapping_sha256": ORACLES.canonical_digest(selected["requirement_mapping"]),
               "oracle_sha256": packet["oracle_sha256"], "request_sha256": packet.get("request_sha256")}
    if (approval.get("reviewed_by") != "root" or approval.get("scope") != "host_pre_native_rejection"
            or approval.get("run_scoped_case_id") != row["run_scoped_case_id"] or not approval.get("reason")
            or any(not value or approval.get(key) != value for key, value in digests.items())):
        raise ValueError("Pre-native rejection needs separate exact-contract/request Root source approval")
    sources = [ORACLES.verify_reference(ref) for ref in approval.get("proof", [])]
    if (not {"official_host_contract", "protocol_contract"} <= {ref.get("kind") for ref in sources}
            or any(ref.get("kind") not in ORACLES.INDEPENDENT_KINDS or not ref.get("revision") for ref in sources)):
        raise ValueError("Pre-native approval lacks versioned independent Apache and protocol sources")
    if {p["sha256"] for p in sources if p.get("kind") == "official_host_contract"} & {
            p["sha256"] for p in sources if p.get("kind") == "protocol_contract"}:
        raise ValueError("Independent Apache and protocol approval must bind separate source bytes")
    return sources


def pre_native_json(ref):
    return json.loads(Path(ref["path"]).read_text())


def pre_native_rows(ref):
    return [json.loads(line) for line in Path(ref["path"]).read_text().splitlines() if line.strip()]


def pre_native_native_window(packet, producers, client):
    """Read the existing native-lifecycle-v1 and Apache host observer captures."""
    rows = pre_native_rows(producers["native_api"])
    rows = [row for row in rows if row.get("pid") == packet["host_pid"]]
    start, end = client["started_ns"], client["completed_ns"]
    if (not rows or any(row.get("schema") != "native-lifecycle-v1" or row.get("run") != packet["run_id"]
                        or row.get("profile") != "apache-native"
                        or row.get("case") != packet["run_scoped_case_id"].split("::")[-1]
                        or row.get("uid") != packet["uid"]
                        or row.get("invalid") is not False or type(row.get("monotonic_ns")) is not int for row in rows)):
        raise ValueError("Pre-native negative allocation needs actual matching native observer records")
    if (any(type(r.get("sequence")) is not int for r in rows)
            or [r["sequence"] for r in rows] != list(range(1, len(rows) + 1))):
        raise ValueError("Pre-native observer capture must preserve the complete process sequence")
    if (not any(r.get("function") == "observer" and r.get("edge") == "admitted" and r["monotonic_ns"] < start for r in rows)
            or not any(r.get("function") == "observer" and r.get("edge") == "final" and r["monotonic_ns"] > end
                       and type(r.get("pending_calls")) is int and r["pending_calls"] == 0
                       and type(r.get("live_mappings")) is int and r["live_mappings"] == 0 for r in rows)
            or any(start <= r["monotonic_ns"] <= end and r.get("function") != "observer" for r in rows)):
        raise ValueError("Pre-native window must be complete with no main allocation/API/P2/EOS/finish/free")
    for before in (True, False):
        controls = [r for r in rows if (r["monotonic_ns"] < start if before else r["monotonic_ns"] > end)]
        constructors = [r for r in controls if r.get("function") in ("native_new", "native_new_with_id")
                        and r.get("edge") == "return" and type(r.get("result")) is int and r["result"] == 1
                        and r.get("transaction_id")]
        if not any(all(any(r.get("function") == function and r.get("edge") == "return"
                               and r.get("transaction_id") == c["transaction_id"]
                               and type(r.get("result")) is int and r["result"] == 1 for r in controls)
                       for function in ("native_process_request_headers", "native_process_request_body"))
                   for c in constructors):
            raise ValueError("Zero main calls require actual positive constructor/API controls before and after")
    host = pre_native_rows(producers["host_callback"])
    if any(r.get("pid") == packet["host_pid"] and start <= r.get("monotonic_ns", start) <= end for r in host):
        raise ValueError("A host callback during the main window contradicts pre-native rejection")
    return {"main_native_allocation": False, "main_native_api_calls": 0, "main_native_transaction_id": None,
            "window_started_ns": start, "window_completed_ns": end}


def pre_native_producer_binding(packet, producers, client):
    source = pre_native_json(producers["source_manifest"])
    if (source.get("parent_sha") != packet["parent_sha"]
            or packet["effective_config_sha256"] != producers["effective_configuration"]["sha256"]
            or packet["rules_sha256"] != producers["rules_file"]["sha256"]
            or packet["request_sha256"] != producers["request_wire"]["sha256"]):
        raise ValueError("Pre-native source/config/rules/request bytes differ from actual sealed inputs")
    isolation = pre_native_json(producers["isolation_receipt"])
    for key in ("run_id", "parent_sha", "effective_config_sha256", "rules_sha256", "host_pid", "host_starttime", "uid"):
        if isolation.get(key) != packet[key]:
            raise ValueError("Pre-native image/isolation belongs to a different actual host")
    for key, role in (("host_binary_sha256", "loaded_image"), ("module_sha256", "native_module"),
                      ("observer_sha256", "observer_image")):
        if isolation.get(key) != producers[role]["sha256"] or source.get(key) != producers[role]["sha256"]:
            raise ValueError("Pre-native actual loaded host/module/observer image differs from source manifest")
    maps = Path(ORACLES.verify_reference(isolation["maps"])["path"]).read_text()
    status = Path(ORACLES.verify_reference(isolation["status"])["path"]).read_text()
    if (not re.search(r"^Pid:\s+" + str(packet["host_pid"]) + r"$", status, re.MULTILINE)
            or not re.search(r"^Uid:\s+" + r"\s+".join([str(packet["uid"])] * 4) + r"$", status, re.MULTILINE)):
        raise ValueError("Pre-native actual process status must bind all four isolated UIDs and PID")
    for role in ("loaded_image", "native_module", "observer_image"):
        mapped = isolation.get("mapped_paths", {}).get(role)
        if not isinstance(mapped, str) or not Path(mapped).is_absolute() or mapped not in maps:
            raise ValueError("Pre-native image must be observed in the actual host process maps")
    if isolation.get("loaded_images_observed") is not True or isolation.get("exclusive_request_window") is not True:
        raise ValueError("Pre-native negative observation needs actual loaded images and an exclusive request window")
    for role in ("event_observer", "cleanup_observer", "healthy_controls"):
        actual = pre_native_json(producers[role])
        for key in ("run_scoped_case_id", "leg_id", "run_id", "parent_sha", "effective_config_sha256", "rules_sha256",
                    "host_pid", "host_starttime", "uid", "request_id", "request_sha256"):
            if actual.get(key) != packet[key]:
                raise ValueError(f"Pre-native {role} correlation differs: {key}")
    event = pre_native_json(producers["event_observer"])
    sink = ORACLES.verify_reference(event["sink"])
    content = Path(sink["path"]).read_bytes()
    offsets = event.get("before_offset"), event.get("after_offset")
    if (event.get("execution_observed") is not True or event.get("window_complete") is not True
            or type(event.get("observed_from_ns")) is not int or type(event.get("observed_through_ns")) is not int
            or event.get("observed_from_ns", client["started_ns"] + 1) > client["started_ns"]
            or event.get("observed_through_ns", 0) < client["completed_ns"]
            or any(type(v) is not int or v < 0 or v > len(content) for v in offsets)
            or offsets[0] != offsets[1]):
        raise ValueError("Zero physical events need an actual complete independent sink window")
    for label in ("before_control", "after_control"):
        control = event.get(label, {})
        begin, finish = control.get("start_offset"), control.get("end_offset")
        if (type(begin) is not int or type(finish) is not int or not 0 <= begin < finish <= len(content)
                or not content[begin:finish].strip()
                or (finish > offsets[0] if label == "before_control" else begin < offsets[1])):
            raise ValueError("Independent event observer needs actual positive sink bytes before and after")
        positive = [json.loads(line) for line in content[begin:finish].splitlines() if line.strip()]
        native = pre_native_rows(producers["native_api"])
        identities = {r.get(key) for r in native for key in ("transaction_id", "canonical_transaction_id")
                      if r.get("pid") == packet["host_pid"] and r.get("function") in ("native_new", "native_new_with_id")
                      and r.get("edge") == "return" and type(r.get("result")) is int and r["result"] == 1
                      and (r["monotonic_ns"] < client["started_ns"] if label == "before_control"
                           else r["monotonic_ns"] > client["completed_ns"])}
        if (not positive or any(not isinstance(r, dict) or not r.get("transaction_id")
                or r["transaction_id"] not in identities or r.get("connector") != "apache"
                or not isinstance(r.get("message_id"), str) or not r["message_id"].startswith("MSCONN_EVENT_") for r in positive)):
            raise ValueError("Positive sink controls must be actual Apache events joined to observed native allocations")
    cleanup = pre_native_json(producers["cleanup_observer"])
    if (cleanup.get("execution_observed") is not True
            or any(cleanup.get(key) is not True for key in ("descriptor_cleanup_observed", "process_cleanup_observed", "listener_cleanup_observed"))
            or cleanup.get("remaining_processes") != [] or cleanup.get("remaining_listeners") != []
            or cleanup.get("unexpected_fd_targets") != []):
        raise ValueError("Pre-native rejection requires actual FD/process/listener cleanup")
    controls = pre_native_json(producers["healthy_controls"])
    for label in ("before", "after"):
        control = controls.get(label, {})
        receipt = pre_native_json(ORACLES.verify_reference(control["client_receipt"]))
        process = pre_native_json(ORACLES.verify_reference(control["client_process"]))
        if (receipt.get("status") != 200 or type(process.get("waited_exit")) is not int or process["waited_exit"] != 0
                or not process.get("argv") or not process.get("cwd") or not control.get("request_id")
                or control["request_id"] == packet["request_id"]
                or (receipt.get("completed_ns", client["started_ns"]) >= client["started_ns"] if label == "before"
                    else receipt.get("started_ns", 0) <= client["completed_ns"])):
            raise ValueError("Pre-native rejection needs actual healthy client controls before and after")
        native = pre_native_rows(producers["native_api"])
        host = pre_native_rows(producers["host_callback"])
        begin, finish = receipt.get("started_ns"), receipt.get("completed_ns")
        if (type(begin) is not int or type(finish) is not int or begin >= finish
                or not any(r.get("pid") == packet["host_pid"] and begin <= r.get("monotonic_ns", 0) <= finish
                           and r.get("function") in ("native_new", "native_new_with_id") and r.get("edge") == "return"
                           and r.get("transaction_id") for r in native)
                or not receipt.get("path") or not any(r.get("pid") == packet["host_pid"]
                    and r.get("kind") == "host_context_associated" and r.get("native_transaction_present") is True
                    and r.get("owner_request_matches") is True and r.get("request_uri") == receipt["path"]
                    and begin <= r.get("monotonic_ns", 0) <= finish for r in host)):
            raise ValueError("Healthy controls must join actual native constructor and host association in their windows")
        backend = pre_native_rows(producers["backend_process"])
        if not any(r.get("kind") in ("request", "request_arrival") and r.get("request_id") == control["request_id"] for r in backend):
            raise ValueError("Healthy controls need an independent actual backend request")


def reviewed_pre_native_packet(supplied, row, effective_oracle):
    """Qualify a host parser rejection, preserving the original native alternative.

    Logical phase1 does not assert a native phase call. No absent native
    transaction, P2/EOS, finish or free is replaced with a fabricated identity.
    """
    ref = ORACLES.verify_reference(supplied)
    packet = pre_native_json(ref)
    sources = pre_native_identity(packet, row, effective_oracle)
    evidence = [ORACLES.verify_reference(item) for item in packet.get("measurement_evidence", [])]
    if (len(evidence) != len(PRE_NATIVE_ROLES) or {p.get("role") for p in evidence} != PRE_NATIVE_ROLES
            or any(p["path"] == ref["path"] for p in evidence)
            or {p["sha256"] for p in evidence} & {p["sha256"] for p in sources}):
        raise ValueError("Pre-native rejection needs distinct physical producers for every dedicated role")
    for item in evidence:
        aliases = {p["role"] for p in evidence if p["path"] == item["path"]}
        if len(aliases) > 1 and aliases != {"native_module", "observer_image"}:
            raise ValueError("Pre-native producers cannot alias independent physical measurements")
    producers = {p["role"]: p for p in evidence}
    actual = pre_native_json(producers["driver_observation"])
    if (actual.get("original_id") != row["run_scoped_case_id"] or actual.get("case_id") != row["selected_requirement"]["case_id"]
            or actual.get("actual_principal_execution") is not True or actual.get("executed_case_contract") is not True
            or actual.get("missing_operations") != []):
        raise ValueError("A driver stub or sibling execution cannot qualify pre-native rejection")
    client = pre_native_json(producers["client_receipt"])
    process = pre_native_json(producers["client_process"])
    if (type(client.get("pid")) is not int or client["pid"] <= 0
            or type(client.get("started_ns")) is not int or type(client.get("completed_ns")) is not int
            or not client["started_ns"] < client["completed_ns"] or client.get("error") is not None
            or not process.get("argv") or not process.get("cwd") or type(process.get("wrapper_pid")) is not int
            or type(process.get("waited_exit")) is not int or process["waited_exit"] != 0
            or type(process.get("started_unix_ns")) is not int or type(process.get("ended_unix_ns")) is not int
            or process["started_unix_ns"] >= process["ended_unix_ns"]):
        raise ValueError("Pre-native rejection needs the actual completed client process and wire receipt")
    main = [item for item in actual.get("clients", []) if item.get("role") == "main"]
    if (len(main) != 1 or main[0].get("request_id") != packet["request_id"]
            or main[0].get("actual_waited_exit") != process["waited_exit"] or main[0].get("command") != process):
        raise ValueError("The actual waited client command must bind the exact original main request")
    raw = Path(producers["response_wire"]["path"]).read_bytes()
    if type(client.get("status")) is not int or client["status"] != 400 or not re.match(rb"HTTP/1\.[01] 400 [^\r\n]*\r\n", raw) or b"\r\n\r\n" not in raw:
        raise ValueError("Pre-native client status must bind an actual complete HTTP400 header block")
    request = Path(producers["request_wire"]["path"]).read_bytes()
    if (not isinstance(client.get("path"), str) or not client["path"]
            or packet["request_id"].encode() not in request or client["path"].encode() not in request):
        raise ValueError("Pre-native main request cannot transfer from another physical client")
    native = pre_native_native_window(packet, producers, client)
    backend = pre_native_rows(producers["backend_process"])
    if any(r.get("request_id") == packet["request_id"] or client["started_ns"] <= r.get("monotonic_ns", client["started_ns"]) <= client["completed_ns"] for r in backend):
        raise ValueError("Pre-native host rejection must have zero actual main backend activity")
    diagnostic = Path(producers["core_diagnostic"]["path"]).read_text()
    approval = packet["source_approval"]
    code = approval.get("core_diagnostic_code")
    if (not isinstance(code, str) or not re.fullmatch(r"AH[0-9]{5}", code) or code not in diagnostic
            or not re.search(r"\[pid " + str(packet["host_pid"]) + r"(?::|\])", diagnostic)
            or not packet.get("connection_id") or "[client " + packet["connection_id"] + "]" not in diagnostic):
        raise ValueError("A raw Apache Core diagnostic must independently bind the actual process and connection")
    matching_lines = [line for line in diagnostic.splitlines() if code in line
                      and re.search(r"\[pid " + str(packet["host_pid"]) + r"(?::|\])", line)
                      and "[client " + packet["connection_id"] + "]" in line]
    in_window = False
    for line in matching_lines:
        try:
            stamp = datetime.datetime.strptime(line.split("]", 1)[0][1:], "%a %b %d %H:%M:%S.%f %Y")
            delta = stamp - datetime.datetime(1970, 1, 1)
            timestamp = ((delta.days * 86400 + delta.seconds) * 1_000_000 + delta.microseconds) * 1000
            in_window |= process["started_unix_ns"] <= timestamp <= process["ended_unix_ns"]
        except (ValueError, IndexError):
            continue
    if not in_window:
        raise ValueError("Actual Apache Core diagnostic must fall inside the waited client UTC window")
    pre_native_producer_binding(packet, producers, client)
    if packet.get("outcome") != "PASS":
        raise ValueError("Only a physically established host-before-native rejection is qualified in this scope")
    return {"receipt": ref, "observations": {"client_process": process, "client": client, **native},
            "measurement_evidence": evidence, "source_approval": copy.deepcopy(packet["source_approval"]),
            "execution_observed": True, "qualification_scope": "host_pre_native_rejection",
            "full_case_qualified": True, "full_lifecycle_qualified": False, "outcome": "PASS", "unknown_fields": []}


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
        if packet.get("execution_kind") == "host_pre_native_rejection":
            reviewer = reviewed_pre_native_packet
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
        pre_native = observation is not None and observation.get("qualification_scope") == "host_pre_native_rejection"
        row["current_lifecycle_packet"] = None if configuration or pre_native else observation
        row["current_pre_native_packet"] = observation if pre_native else None
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
            elif pre_native:
                row["status"] = observation["outcome"]
                row["qualified_full_case_pass"] = observation["outcome"] == "PASS"
                row["qualification_scope"] = "host_pre_native_rejection"
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
                "pre_native_rejection_pass": sum(row["qualification_scope"] == "host_pre_native_rejection" and row["status"] == "PASS" for row in rows),
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
