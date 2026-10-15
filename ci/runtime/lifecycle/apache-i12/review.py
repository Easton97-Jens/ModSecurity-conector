#!/usr/bin/env python3
"""Extract an unsigned Apache I12 candidate from the existing physical captures.

No expected value becomes an observation, and this command never signs a Root
review or evaluates an oracle. Missing files/joins remain unknown. Root must
inspect the candidate and its physical references before independent approval.
"""

import argparse
import collections
import importlib.util
import json
from pathlib import Path
import subprocess


def load_ledger():
    spec = importlib.util.spec_from_file_location("apache_i12_candidate_ledger", Path(__file__).with_name("ledger.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


LEDGER = load_ledger()
ORACLES = LEDGER.ORACLES


def read(path):
    return json.loads(Path(path).read_text())


def json_lines(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def reference(path, role):
    return {**ORACLES.reference(Path(path).resolve(strict=True)), "role": role}


def associate(host, api, client):
    """Join one actual request to API calls by typed PID/allocation scope."""
    matches = [row for row in host if row.get("kind") == "host_context_associated"
               and row.get("request_uri") == client["path"]
               and row.get("request_method") == client["method"]
               and client["started_ns"] <= row["monotonic_ns"] <= client["completed_ns"]]
    if len(matches) != 1:
        raise ValueError("Actual client needs exactly one timed host association")
    association = matches[0]
    pid, scope = association["pid"], association["allocation_scope_call"]
    if scope is None:
        raise ValueError("Actual host allocation scope is missing")
    main_host = [row for row in host if row.get("pid") == pid and row.get("allocation_scope_call") == scope]
    main_api = [row for row in api if row.get("pid") == pid and row.get("allocation_scope_call") == scope
                and row.get("allocation_scope_kind") == "host"]
    return association, main_host, main_api


def choose_clients(data, selected_uri):
    candidates, neighbors = [], []
    for path in sorted((data / "client").glob("*.receipt.json")):
        receipt = read(path)
        process_path = path.with_name(path.name.replace(".receipt.json", ".actual-process.json"))
        process = read(process_path) if process_path.is_file() else None
        item = (path, receipt, process_path, process)
        if process and process.get("role") == "separate_original_allow_neighbor":
            neighbors.append(item)
        elif receipt.get("path") == selected_uri:
            candidates.append(item)
    if len(candidates) != 1:
        raise ValueError("Need exactly one actual main client for the selected URI")
    main = candidates[0]
    token = main[0].name.removesuffix(".receipt.json")
    neighbors = [item for item in neighbors if item[3].get("main_client_token") == token]
    return main, neighbors


def selected_identity(settings, contract, actual_case):
    """Preserve the original ID while naming the one permitted local variant."""
    original = contract.get("original_selected_requirement", {})
    original_name = original.get("case_id") or original.get("name")
    original_id = original.get("run_scoped_case_id")
    if original_id is None and original_name:
        original_id = "I12::apache-native::" + original_name
    selected = settings.get("original_selected_id", original_id)
    if not selected or not selected.startswith("I12::apache-native::"):
        raise ValueError("Original selected ID must belong to Apache")
    if selected != original_id:
        # The immutable selector explicitly names these two source filenames;
        # their internal declarative fixture names carry a _fixture suffix.
        selected_name = selected.removeprefix("I12::apache-native::")
        declarative = {
            "phase3_deny_before_commit": "7de9543c83206019ae7e77f158dd7325e7713d2c31583daeb0e012bba6d67f37",
            "phase3_redirect_before_commit": "61d0423437203ef2731e33b6c10d91abfd78abea59d375139c34a92a1ed8ee50",
        }
        if not (selected_name in declarative and original_name == selected_name + "_fixture"
                and Path(settings.get("original_source_path", "")).name == selected_name + ".yaml"
                and settings.get("original_source_sha256") == declarative[selected_name]):
            raise ValueError("Settings selected ID differs from exact original fixture contract")
    selected_name = selected.removeprefix("I12::apache-native::")
    if actual_case != selected_name and (selected_name, actual_case) != (
            "duplicate_header_names", "duplicate_header_names_apache_core_merged"):
        raise ValueError("Scenario aliases cannot transfer another selected original ID")
    return selected


def fd_difference(before, after):
    return {
        "added": {key: value for key, value in after.items() if key not in before},
        "removed": {key: value for key, value in before.items() if key not in after},
        "changed": {key: {"before": before[key], "after": value} for key, value in after.items()
                    if key in before and before[key] != value},
        "before_count": len(before), "after_count": len(after),
        "after_socket_targets": [value for value in after.values() if value.startswith("socket:[")],
    }


def mrts_gitlink(bindings):
    """Read sealed Framework Git metadata without claiming an MRTS execution."""
    binding = bindings.get("/mnt/git-framework")
    if not binding:
        return None
    result = subprocess.run(["rtk", "proxy", "git", "--git-dir=" + binding["source"],
                             "ls-tree", "HEAD", "tools/MRTS"], capture_output=True, text=True, check=False)
    if result.returncode:
        return None
    parts = result.stdout.strip().split()
    if len(parts) == 4 and parts[0:2] == ["160000", "commit"] and parts[3] == "tools/MRTS":
        return parts[2]
    return None


def extract(attempt, spec_path, case, oracle_path=None, evidence_branch_base=None):
    attempt, spec_path = Path(attempt).resolve(strict=True), Path(spec_path).resolve(strict=True)
    data = attempt / "data"
    controller_path = attempt / "controller-result.json"
    controller, spec = read(controller_path), read(spec_path)
    if controller.get("spec_sha256") != ORACLES.reference(spec_path)["sha256"]:
        raise ValueError("Attempt does not bind the supplied admission spec")
    bindings = {item["target"]: item for item in spec["bindings"]}
    for binding in bindings.values():
        if ORACLES.reference(Path(binding["ledger"]))["sha256"] != binding["ledger_sha256"]:
            raise ValueError("Sealed binding ledger hash changed")
    fixtures = Path(bindings["/mnt/fixtures"]["source"])
    contract_path = fixtures / "fixture-contract.json"
    contract = read(contract_path)
    settings_path = fixtures / "settings.json"
    settings = read(settings_path) if settings_path.is_file() else {}
    command_path = data / "apache-lifecycle-command.json"
    command = read(command_path)
    env = command["environment_overrides"]
    if env.get("MSCONNECTOR_LIFECYCLE_CASE") != case:
        raise ValueError("Requested case differs from actual launched case")
    if settings and settings.get("case_id") != case:
        raise ValueError("Prepared settings differ from selected case")
    selected_id = selected_identity(settings, contract, case)
    if settings.get("original_source_path"):
        if ORACLES.reference(Path(settings["original_source_path"]))["sha256"] != settings.get("original_source_sha256"):
            raise ValueError("Exact original source fixture hash changed")
    uri = settings.get("selected_uri") or contract.get("supplemental_contract", {}).get("request", {}).get("path")
    if not uri:
        raise ValueError("No source-bound selected request URI")
    main, neighbors = choose_clients(data, uri)
    client_path, client, process_path, process = main
    host_path, api_path, backend_path = (data / name for name in
                                       ("apache-host-eos.jsonl", "apache-native-api.jsonl", "apache-backend.jsonl"))
    host = json_lines(host_path) if host_path.is_file() else []
    api = json_lines(api_path) if api_path.is_file() else []
    backend = json_lines(backend_path) if backend_path.is_file() else None
    observations = {name: {"value": None, "reason": "No complete physical observation extracted for this field."}
                    for name in LEDGER.SHARED.ROLES}
    checks = {}

    def put(name, value, *proof):
        observations[name] = {"applicable": True, "value": value, "evidence": list(proof)}

    def unknown(name, reason):
        observations[name] = {"value": None, "reason": reason}

    cr = reference(client_path, "client_process")
    if process:
        pr = reference(process_path, "client_process")
        if "actual_waited_exit_code" in process and process["actual_waited_exit_code"] is not None:
            put("client_exit", process["actual_waited_exit_code"], pr)
        if "actual_signal" in process:
            put("client_signal", {"actual_signal": process["actual_signal"],
                                  "waited_exit_code": process.get("actual_waited_exit_code")}, pr)
    for field, key in (("client_headers", "headers"), ("transport_framing", "framing")):
        if client.get(key) is not None:
            put(field, client[key], cr)
    if all(client.get(key) is not None for key in ("request_bytes", "entity_bytes")):
        put("client_bytes", {"request": client["request_bytes"], "response_entity": client["entity_bytes"]}, cr)
    if all(client.get(key) is not None for key in ("request_sha256", "entity_sha256")):
        put("client_sha256", {"request": client["request_sha256"], "response_entity": client["entity_sha256"]}, cr)
    if all(key in client for key in ("tcp_eof_observed", "tcp_reset_observed", "timeout_observed", "error")):
        put("transport_reset_scope", {key: client[key] for key in
                                     ("tcp_eof_observed", "tcp_reset_observed", "timeout_observed", "error")}, cr)
    association = None
    main_host, main_api = [], []
    try:
        association, main_host, main_api = associate(host, api, client)
        checks["one_timed_typed_host_association"] = True
    except ValueError as error:
        checks["one_timed_typed_host_association"] = False
        unknown("observed_handle_association", str(error))
    hr = reference(host_path, "host_callback") if host_path.is_file() else None
    ar = reference(api_path, "native_api") if api_path.is_file() else None
    returns = [row for row in main_api if row.get("edge") == "return"]
    by_function = collections.defaultdict(list)
    for row in returns:
        by_function[row["function"]].append(row)
    counts = collections.Counter(row["function"] for row in returns)
    native_id = common_id = None
    for field, function in (("native_transaction_id", "native_new"), ("common_transaction_id", "common_init")):
        found = by_function[function]
        if len(found) == 1 and found[0].get("transaction_id"):
            put(field, {key: found[0].get(key) for key in
                        ("transaction_id", "canonical_transaction_id", "transaction_id_origin")}, ar)
            if field == "native_transaction_id":
                native_id = found[0]["transaction_id"]
            else:
                common_id = found[0]["transaction_id"]
    if association and main_api:
        joined = by_function["host_allocation"]
        valid_join = len(joined) == 1 and joined[0].get("allocation_join_verified") is True and joined[0].get("result") == 1
        checks["successful_actual_allocation_join"] = valid_join
        if valid_join:
            put("observed_handle_association", {"host_association": association, "actual_allocation_join": joined[0],
                "native_transaction_id": native_id, "common_transaction_id": common_id,
                "retirement": by_function["host_association_retire"],
                "retirement_is_bookkeeping_not_apr_memory_free": True}, ar)
        checks["no_invalid_main_observer_rows"] = not any(row.get("invalid") for row in main_api + main_host)
        put("native_api_returns", returns, ar)
        put("native_phases", [row for row in returns if row["function"].startswith("native_process_")], ar)
        put("native_body_chunks", [row for row in returns if row["function"].startswith("native_append_")], ar)
        put("native_intervention_or_first_cause", {"actual_native_intervention_returns": by_function["native_intervention"],
            "false_return_output_fields_preserved": True}, ar)
        eos = [row for row in main_host if row.get("actual_apr_bucket_is_eos") is True]
        put("host_eos", {"actual_apr_eos_rows": eos, "all_main_host_rows": main_host}, hr)
        put("native_eos", {"actual_apr_eos_rows": eos,
            "native_request_finalization_returns": by_function["native_process_request_body"],
            "native_response_finalization_returns": by_function["native_process_response_body"],
            "append_has_no_eos_argument": None,
            "semantics": "Actual APR EOS branches joined to native finalization; no fabricated append EOS argument."}, ar, hr)
        put("finish_calls", {"common_finish": counts["common_finish"], "native_logging": counts["native_process_logging"]}, ar)
        transitions = []
        for row in main_api:
            if row.get("edge") == "enter" and row.get("contract_state") is not None:
                matched = [item for item in returns if item["call"] == row["call"] and item.get("contract_state") is not None]
                if len(matched) == 1:
                    transitions.append({"function": row["function"], "call": row["call"],
                                        "before": row["contract_state"], "after": matched[0]["contract_state"]})
        put("finish_transitions", {"actual_state_transitions": transitions,
            "completed_status_3_transitions": sum(row["before"]["status"] != 3 and row["after"]["status"] == 3 for row in transitions)}, ar)
        put("native_free_calls", {"native_cleanup": counts["native_cleanup"], "common_cleanup": counts["common_cleanup"],
                                   "host_association_retire": counts["host_association_retire"]}, ar)
        checks["native_cleanup_exactly_once"] = counts["native_cleanup"] == 1
        checks["common_finish_exactly_once"] = counts["common_finish"] == 1
        checks["common_cleanup_exactly_once"] = counts["common_cleanup"] == 1
        output = [row for row in main_host if row["kind"].startswith("output_")]
        recv_keys = ("first_response_recv_started_ns", "first_response_recv_completed_ns", "headers_complete_recv_ns",
                     "first_encoded_entity_recv_ns", "eof_ns", "actual_socket_recv_chunks")
        if all(key in client for key in recv_keys):
            put("commit_order", {"actual_output_handoffs": output,
                "internal_committed_flag_returns": by_function["common_set_response_committed"],
                "native_p4_edges": [row for row in main_api if row["function"] == "native_process_response_body"],
                "actual_client_receives": {key: client[key] for key in recv_keys},
                "precision": "Blocking socket recv brackets and actual next-filter callbacks; no exact kernel send time is inferred."}, hr, cr)
        put("host_action", {"actual_http_status": client.get("status"), "actual_entity_bytes": client.get("entity_bytes"),
                            "host_callbacks": main_host, "native_interventions": by_function["native_intervention"]}, hr, cr)

    main_backend = None
    if backend is not None:
        br = reference(backend_path, "backend_process")
        # Complete private backend transcript is retained even for an early deny.
        main_backend = [row for row in backend if row.get("path") == client["path"]
                        and client["started_ns"] <= row.get("monotonic_ns", -1) <= client["completed_ns"]]
        put("backend_request_count", {"main": len(main_backend), "whole_transcript": len(backend),
            "main_rows": main_backend, "selection": "Exact path and actual client monotonic execution interval"}, br)
        if len(main_backend) == 1:
            actual = main_backend[0]
            put("backend_payload_identity", actual, br, cr)
            put("client_backend_correlation", {"backend": actual, "actual_client_method": client["method"],
                "actual_client_path": client["path"], "request_body_hash_equal": actual.get("body_sha256") == client.get("request_sha256"),
                "response_body_hash_equal": actual.get("response_source_body_sha256") == client.get("entity_sha256")}, br, cr)
        elif not main_backend:
            unknown("backend_payload_identity", "No backend request was observed; exact unsupported/nonapplicable disposition needs independent Root review.")
            unknown("client_backend_correlation", "No backend request was observed; client-only execution cannot prove payload correlation.")
    else:
        unknown("backend_request_count", "Physical backend capture file is missing; zero requests cannot be inferred.")

    runtime = data / "apache-lifecycle/runtime/conf"
    config_path, rules_path = runtime / "httpd.conf", runtime / "modsecurity-smoke.conf"
    source_binding = bindings.get("/mnt/src")
    config_refs = [reference(path, "effective_configuration") for path in (config_path, rules_path) if path.is_file()]
    if source_binding and len(config_refs) == 2:
        manifest_refs = [reference(source_binding["ledger"], "source_manifest")]
        artifact_binding = bindings.get("/mnt/artifacts")
        if artifact_binding:
            manifest_refs.append(reference(artifact_binding["ledger"], "source_manifest"))
        put("source_config_binding", {"sealed_source_binding": source_binding,
            "actual_effective_config_sha256": ORACLES.reference(config_path)["sha256"],
            "actual_rules_sha256": ORACLES.reference(rules_path)["sha256"],
            "spec_sha256": controller["spec_sha256"], "sealed_fixture_binding": bindings["/mnt/fixtures"],
            "sealed_artifacts_binding": artifact_binding,
            "scope": "Historical product base plus source-copy instrumentation and exact sealed overlays; not current evidence-branch binary identity."},
            *manifest_refs, *config_refs)
    if main_host:
        put("capability", {"actual_association": association, "actual_host_callback_kinds": dict(collections.Counter(row["kind"] for row in main_host)),
                           "scope": "Only this actual selected request; no sibling capability promotion."}, hr, reference(contract_path, "source_contract"))

    audit_path = data / "apache-lifecycle/logs/audit.log"
    common_path = data / "apache-lifecycle/logs/phase4.log"
    debug_path = data / "apache-lifecycle/logs/audit/native-debug.log"
    physical_refs = []
    native_lines, common_rows = None, None
    if audit_path.is_file() and native_id:
        native_lines = [line for line in audit_path.read_text().splitlines() if f'[unique_id "{native_id}"]' in line]
        physical_refs.append(reference(audit_path, "physical_event_sink"))
    if common_path.is_file() and common_id:
        common_rows = [row for row in json_lines(common_path) if row.get("transaction_id") == common_id]
        physical_refs.append(reference(common_path, "physical_event_sink"))
    if physical_refs:
        event_value = {"native_transaction_id": native_id, "native_audit_lines": native_lines,
                       "common_transaction_id": common_id, "physical_common_rows": common_rows,
                       "common_sink_mode": oct(common_path.stat().st_mode & 0o777) if common_path.is_file() else None}
        put("native_events", event_value, *physical_refs)
        put("physical_event_order", {**event_value, "actual_host_callbacks": main_host,
            "actual_backend_rows": main_backend, "timestamp_limit": "Empty Common timestamps remain empty; no cross-clock ordering inferred."}, *physical_refs)
        if common_rows is not None:
            terminal = [row for row in common_rows if row.get("message_id") != "MSCONN_EVENT_RULE_MATCHED"]
            put("terminal_event_count", {"actual_common_scoped_records": len(common_rows), "actual_common_terminal_subset": terminal,
                "actual_common_terminal_subset_count": len(terminal), "native_audit_line_count": len(native_lines) if native_lines is not None else None,
                "host_terminal_event_attempted": [row.get("terminal_event_attempted") for row in main_host],
                "host_event_sink_error": [row.get("event_sink_error") for row in main_host]}, *physical_refs)
    if debug_path.is_file() and native_id:
        debug_lines = [line for line in debug_path.read_text().splitlines() if f"[{native_id}]" in line]
        put("mime_gate", {"actual_same_native_id_debug": debug_lines,
            "actual_native_p4_calls": by_function["native_process_response_body"],
            "actual_host_mime_values": [row.get("native_mime_selection") for row in main_host],
            "scope": "Actual SDK debug and calls; nullable public state is not converted into execution."}, reference(debug_path, "native_debug"))

    if association:
        pid = association["pid"]
        finals = [row for row in api if row.get("pid") == pid and row.get("edge") == "final"]
        checks["one_clean_native_observer_final"] = len(finals) == 1 and finals[0].get("pending_calls") == 0 and finals[0].get("live_mappings") == 0
        if finals:
            put("cleanup_receipts", {"actual_native_observer_finals": finals, "actual_main_host_tail": main_host[-1:],
                "sampler_thread_stopped": command.get("sampler_thread_stopped"),
                "sampler_errors": command.get("native_process_sampler_errors")}, reference(command_path, "cleanup_observer"),
                reference(controller_path, "isolation_receipt"), reference(api_path, "cleanup_observer"))
        snapshots = [row for row in command.get("native_process_snapshots", []) if row.get("native_child_pid") == pid]
        selected = {}
        for label, event in (("main", client), *(("neighbor", item[1]) for item in neighbors)):
            before = [row for row in snapshots if row["monotonic_ns"] < event["started_ns"]]
            after = [row for row in snapshots if row["monotonic_ns"] > event["completed_ns"]]
            if before and after:
                selected["before_" + label] = max(before, key=lambda row: row["monotonic_ns"])
                selected["after_" + label] = min(after, key=lambda row: row["monotonic_ns"])
        if "before_main" in selected and "after_main" in selected:
            same_start = len({row["starttime"] for row in selected.values()}) == 1
            checks["fd_snapshots_same_pid_starttime"] = same_start
            fd_paths = {label: data / "native-process" / (row["files_label"] + ".fds.json") for label, row in selected.items()}
            if same_start and all(path.is_file() for path in fd_paths.values()):
                fds = {label: read(path) for label, path in fd_paths.items()}
                differences = {"main": fd_difference(fds["before_main"], fds["after_main"])}
                if "before_neighbor" in fds and "after_neighbor" in fds:
                    differences["neighbor"] = fd_difference(fds["before_neighbor"], fds["after_neighbor"])
                put("descriptor_cleanup", {"selected_same_pid_starttime_snapshots": selected,
                    "actual_fd_differences": differences, "raw_fd_tables": fds,
                    "observer_added_fd_classification": "Root must assess actual added targets; counts are not preset."},
                    *(reference(path, "cleanup_observer") for path in fd_paths.values()))
                first = selected["before_main"]
                maps_path = data / "native-process" / (first["files_label"] + ".maps")
                status_path = maps_path.with_suffix(".status")
                binary = data / "apache-lifecycle/native-bin/apache2"
                if maps_path.is_file() and status_path.is_file() and binary.is_file():
                    maps = maps_path.read_text()
                    images = []
                    for line in maps.splitlines():
                        parts = line.split(maxsplit=5)
                        if len(parts) == 6 and parts[5].startswith("/"):
                            loaded = parts[5]
                            if "libmodsecurity.so" in loaded or "test-observed.so" in loaded:
                                physical = Path(loaded)
                                for target, binding in bindings.items():
                                    if loaded.startswith(target + "/"):
                                        physical = Path(binding["source"]) / loaded.removeprefix(target + "/")
                                        break
                                if physical.is_file():
                                    entry = {"mapped_path": loaded, **ORACLES.reference(physical.resolve(strict=True))}
                                    if entry not in images:
                                        images.append(entry)
                    checks["maps_snapshot_hash_matches_sampler"] = ORACLES.reference(maps_path)["sha256"] == first.get("maps_sha256")
                    checks["status_snapshot_hash_matches_sampler"] = ORACLES.reference(status_path)["sha256"] == first.get("status_sha256")
                    checks["sdk_and_observed_module_loaded"] = any("libmodsecurity.so" in image["mapped_path"] for image in images) and any("test-observed.so" in image["mapped_path"] for image in images)
                    put("product_host_identity", {"actual_host_pid": pid, "actual_uid": association.get("uid"),
                        "actual_gid": association.get("gid"), "actual_starttime": first["starttime"],
                        "apache_binary": ORACLES.reference(binary), "mapped_images": images,
                        "actual_proc_status": status_path.read_text(), "instrumented_test_module_is_not_release_byteidentity": True},
                        reference(maps_path, "loaded_image"), reference(status_path, "loaded_image"),
                        reference(attempt / "admission.original.json", "isolation_receipt"))
    if all(key in controller for key in ("supervisor_reaped", "surviving_namespace_pids", "outside_mount_leaks", "errors")):
        put("process_listener_cleanup", {key: controller[key] for key in
            ("supervisor_reaped", "surviving_namespace_pids", "outside_mount_leaks", "errors", "exitcode", "controller_exitcode")},
            reference(controller_path, "isolation_receipt"), reference(command_path, "cleanup_observer"))
        checks["controller_cleanup_clean"] = (controller["supervisor_reaped"] is True and
            controller["surviving_namespace_pids"] == [] and controller["outside_mount_leaks"] == [] and controller["errors"] == [])
    if len(neighbors) == 1 and backend is not None:
        np, neighbor, npp, nproc = neighbors[0]
        nb = [row for row in backend if row.get("path") == neighbor["path"] and
              neighbor["started_ns"] <= row.get("monotonic_ns", -1) <= neighbor["completed_ns"]]
        try:
            na, _, _ = associate(host, api, neighbor)
            put("neighbor_health", {"separate_actual_client": neighbor, "actual_waited_process": nproc,
                "independent_backend": nb, "actual_host_association": na,
                "same_native_host_pid": association is not None and na["pid"] == association["pid"],
                "not_another_selected_id_execution": True}, reference(np, "client_process"), reference(npp, "client_process"),
                reference(backend_path, "backend_process"))
        except ValueError as error:
            unknown("neighbor_health", str(error))

    def metadata_head(target):
        binding = bindings.get(target)
        path = Path(binding["source"]) / "HEAD" if binding else None
        return path.read_text().strip() if path and path.is_file() else None

    packet = {"run_scoped_case_id": selected_id, "actual_scenario_variant": case,
        "original_selected_requirement": contract.get("original_selected_requirement"),
        "leg_id": "apache-native", "reviewed_by": None,
        "execution_observed": True, "execution_kind": "host_http", "run_id": env.get("MSCONNECTOR_LIFECYCLE_RUN"),
        "parent_sha": metadata_head("/mnt/git"), "framework_sha": metadata_head("/mnt/git-framework"),
        "evidence_branch_base": evidence_branch_base,
        "mrts_sha": mrts_gitlink(bindings), "mrts_scope": "sealed_Framework_gitlink_metadata_only; MRTS_not_executed",
        "effective_config_sha256": ORACLES.reference(config_path)["sha256"] if config_path.is_file() else None,
        "rules_sha256": ORACLES.reference(rules_path)["sha256"] if rules_path.is_file() else None,
        "actual_attempt": str(attempt), "oracle_evaluated": False, "oracle_sha256": None,
        "outcome": None, "full_lifecycle_qualified": False, "observations": observations,
        "review_checks": checks, "unknown_fields": [name for name, item in observations.items() if item.get("value") is None],
        "candidate_is_not_an_approval": True,
        "input_evidence": [ORACLES.reference(spec_path), ORACLES.reference(controller_path), ORACLES.reference(contract_path)]}
    if settings_path.is_file():
        packet["input_evidence"].append(ORACLES.reference(settings_path))
    if oracle_path:
        packet["candidate_oracle"] = {"reference": ORACLES.reference(Path(oracle_path).resolve(strict=True)),
                                     "effective_oracle": read(oracle_path), "evaluated": False}
    # Validate each physical role and reference through the unchanged shared
    # contract. This checks measurements, never signs or evaluates the packet.
    for name, item in observations.items():
        LEDGER.SHARED.measurement(name, item, Path("unsigned-candidate-not-yet-written"))
    return packet


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("attempt", "spec", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--case", required=True)
    parser.add_argument("--oracle", type=Path)
    parser.add_argument("--evidence-branch-base", help="Declared evidence branch base, separate from the actual sealed product source base")
    args = parser.parse_args()
    packet = extract(args.attempt, args.spec, args.case, args.oracle, args.evidence_branch_base)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(packet, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
    print(json.dumps({"output": ORACLES.reference(args.output.absolute()), "unknown_fields": packet["unknown_fields"],
                      "review_checks": packet["review_checks"], "outcome": None, "full_lifecycle_qualified": False}))


if __name__ == "__main__":
    main()
