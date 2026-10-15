#!/usr/bin/env python3
"""Extract independently reviewable native HTX observations; never award PASS."""
import argparse
import hashlib
import json
from pathlib import Path
import re


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reference(path, role):
    return {"path": str(path), "sha256": sha(path), "bytes": path.stat().st_size, "role": role}


def load(path):
    return json.loads(path.read_text())


def match_wire_segments(writes, wire):
    """Compare every positive host write with its contiguous actual client bytes."""
    cursor = 0
    segments = []
    for row in writes:
        count = row["actual_result"]
        if count > 0:
            segment = wire[cursor:cursor + count]
            actual = hashlib.sha256(segment).hexdigest()
            segments.append({"offset": cursor, "actual_host_write": row, "client_wire_segment_sha256": actual, "digest_matches": len(segment) == count and actual == row["positive_output_sha256"]})
            cursor += count
    return segments, cursor == len(wire)


def observe(attempt, fixture, binary, source_receipt):
    data = attempt / "data"
    execution = load(data / "execution.json")
    controller = load(attempt / "controller-result.json")
    contract = load(fixture / "case-contract.json")
    client = load(data / "main-client.json")
    neighbor = load(data / "neighbor-client.json")
    raw = [json.loads(line) for line in (data / "native-api.jsonl").read_text().splitlines()]
    allocated = [row for row in raw if row["function"] == "host_allocation" and row["edge"] == "return" and row["result"] == 1]
    if len(allocated) != 2:
        raise ValueError("expected independent main and health-neighbor allocations")
    scope = allocated[0]["allocation_scope_call"]
    native = [row for row in raw if row["allocation_scope_call"] == scope]

    def calls(function, edge="return"):
        return [row for row in native if row["function"] == function and row["edge"] == edge]

    callbacks = [json.loads(line.split(" ", 1)[1]) for line in (data / "haproxy.stderr").read_text().splitlines() if line.startswith("HAPROXY_")]
    eos = [row for row in callbacks if row.get("scope_call") == scope and row.get("kind", "").startswith("htx_")]
    writes = [row for row in callbacks if row.get("function") == "SSL_write" and client["started_wall_ns"] <= row["before_wall_ns"] <= client["completed_wall_ns"]]
    wire = (data / "main-wire.bin").read_bytes()
    segments, wire_count_matches = match_wire_segments(writes, wire)
    backend = [json.loads(line) for line in (data / "backend.jsonl").read_text().splitlines()]
    main_backend = [row for row in backend if row["path"] == "/i12-main"]
    native_id = calls("native_new_with_id")[0]["transaction_id"]
    common_id = calls("common_init")[0]["canonical_transaction_id"]
    audit = (data / "native-audit.log").read_text()
    native_lines = [line for line in audit.splitlines() if f'[unique_id "{native_id}"]' in line]
    blocks = re.findall(r'^---([A-Za-z0-9]+)---A--\n([^\n]+)\n(.*?)^---\1---Z--', audit, re.M | re.S)
    main_blocks = [block for block in blocks if (" " + native_id + " ") in block[1] and "POST /i12-main HTTP/1.1" in block[2]]
    counts = {str(rule): sum(f'[id "{rule}"]' in line for line in native_lines) for rule in (1999401, 1999404, 1999471, 1999472, 1999473)}
    transitions = []
    for enter in native:
        if enter["edge"] == "enter" and enter["function"] in ("common_complete_phase", "common_finish", "common_cleanup"):
            returned = next((row for row in native if row["call"] == enter["call"] and row["edge"] == "return"), None)
            transitions.append({"function": enter["function"], "before": enter["contract_state"], "after": returned["contract_state"] if returned else None})
    command = next(row for row in execution["commands"] if row["label"] == "main-client")
    before = load(data / "before-main.fds.json")
    after = load(data / "after-main.fds.json")
    after_neighbor = load(data / "after-neighbor.fds.json")
    maps = (data / "before-main.maps").read_text()
    loaded_sdk = sorted({line.split()[-1] for line in maps.splitlines() if "libmodsecurity.so" in line})
    sdk_images = [{"path": path, "sha256": sha(Path(path))} for path in loaded_sdk]
    refs = {
        "api": reference(data / "native-api.jsonl", "native_api"),
        "host": reference(data / "haproxy.stderr", "host_callback"),
        "client": reference(data / "main-client.json", "client_process"),
        "client_commands": reference(data / "execution.json", "client_process"),
        "neighbor": reference(data / "neighbor-client.json", "client_process"),
        "backend": reference(data / "backend.jsonl", "backend_process"),
        "audit": reference(data / "native-audit.log", "physical_event_sink"),
        "debug": reference(data / "native-debug.log", "native_debug"),
        "config": reference(data / "haproxy.cfg", "effective_configuration"),
        "rules": reference(data / "rules.conf", "effective_configuration"),
        "contract": reference(fixture / "case-contract.json", "source_contract"),
        "controller": reference(attempt / "controller-result.json", "isolation_receipt"),
        "execution": reference(data / "execution.json", "cleanup_observer"),
        "source": reference(source_receipt, "source_manifest"),
        "maps": reference(data / "before-main.maps", "loaded_image"),
        "identity": reference(data / "identity.stdout", "loaded_image"),
    }

    def known(value, *proof):
        return {"applicable": True, "value": value, "evidence": [refs[key] for key in proof]}

    observations = {
        "product_host_identity": known({"host_binary_sha256": sha(binary), "actual_loaded_SDK_images": sdk_images, "loaded_maps": maps, "identity": (data / "identity.stdout").read_text()}, "maps", "identity", "controller"),
        "source_config_binding": known({"source_receipt_sha256": sha(source_receipt), "effective_rules_sha256": sha(data / "rules.conf"), "effective_config_sha256": sha(data / "haproxy.cfg")}, "source", "config", "rules"),
        "capability": known(contract, "contract"),
        "client_exit": known(command["exit"], "client_commands"),
        "client_signal": known({"actual_signal": command["signal"], "actual_normal_exit": command["exit"] >= 0}, "client_commands"),
        "client_headers": known(client["headers"], "client"),
        "client_bytes": known(client["response_bytes"], "client"),
        "client_sha256": known(client["response_sha256"], "client"),
        "backend_request_count": known({"main": len(main_backend), "neighbor": sum(row["path"] == "/i12-neighbor" for row in backend)}, "backend"),
        "backend_payload_identity": known(backend, "backend"),
        "client_backend_correlation": known({"main_backend": main_backend, "actual_client": client, "independent_backend_process": True}, "client", "backend"),
        "native_events": known({"native_id": native_id, "actual_lines": native_lines, "actual_rule_counts": counts}, "audit"),
        "native_api_returns": known(native, "api"),
        "native_transaction_id": known(native_id, "api"),
        "common_transaction_id": known(common_id, "api"),
        "observed_handle_association": known(allocated[0], "api"),
        "native_phases": known({phase: calls(phase) for phase in ("native_process_request_headers", "native_process_request_body", "native_process_response_headers", "native_process_response_body", "native_process_logging")}, "api", "debug"),
        "native_body_chunks": known({"request": calls("native_append_request_body"), "response": calls("native_append_response_body"), "native_append_has_no_EOS_argument": True}, "api"),
        "native_intervention_or_first_cause": known(calls("native_intervention"), "api"),
        "host_eos": known(eos, "host"),
        "native_eos": known({"request": calls("native_process_request_body"), "response": calls("native_process_response_body"), "not_inferred_from_client_close": True}, "api", "host"),
        "commit_order": known({"common_commit_calls": calls("common_set_response_committed"), "actual_SSL_writes": writes, "actual_client_first_receive": client["first_receive_wall_ns"], "client_wire_segments": segments, "host_positive_bytes_equal_client_wire": wire_count_matches}, "host", "client"),
        "mime_gate": known({"native_response_body_calls": calls("native_process_response_body"), "native_response_append_calls": calls("native_append_response_body"), "actual_native_mime_selection_rows": [row for row in native if row.get("native_mime_selection") is not None], "physical_P4_probe_count": counts["1999472"], "do_not_infer_MIME_from_HTTP_header_alone": True}, "debug", "audit"),
        "finish_calls": known({"native_logging": calls("native_process_logging"), "common_finish": calls("common_finish")}, "api"),
        "finish_transitions": known(transitions, "api"),
        "native_free_calls": known(calls("native_cleanup"), "api"),
        "cleanup_receipts": known({"native_final": raw[-1], "waits": execution["commands"], "survivors": controller["surviving_namespace_pids"]}, "execution", "controller"),
        "descriptor_cleanup": known({"before": before, "after_main": after, "after_neighbor": after_neighbor, "fd_targets_equal": before["fds"] == after["fds"] == after_neighbor["fds"]}, "execution"),
        "process_listener_cleanup": known({"surviving_namespace_pids": controller["surviving_namespace_pids"], "outside_mount_leaks": controller["outside_mount_leaks"], "supervisor_reaped": controller["supervisor_reaped"]}, "execution", "controller"),
        "neighbor_health": known(neighbor, "neighbor", "backend"),
        "transport_framing": known({key: client.get(key) for key in ("tls_version", "ssl_verifies_task_ca", "headers", "declared_content_length", "response_bytes", "body_complete", "termination", "ssl_reads", "actual_TLS_unwrap", "actual_raw_TCP_end")}, "client"),
        "transport_reset_scope": known({"actual_main": client.get("actual_raw_TCP_end"), "actual_neighbor": neighbor.get("actual_raw_TCP_end"), "no_synthesized_EOS": True}, "client", "host"),
        "host_action": known({"actual_client_status": client["status"], "actual_SSL_write_segments": segments, "all_segment_digests_match": bool(segments) and all(row["digest_matches"] for row in segments), "host_positive_bytes_equal_client_wire": wire_count_matches}, "client", "host"),
        "physical_event_order": known({"native_serial_A_Z_boundaries": [row[0] for row in main_blocks], "rule_counts": counts}, "audit"),
        "terminal_event_count": known({"native_main_serial_A_Z_records": len(main_blocks), "Common_Allow_physical_sink": None, "Common_Allow_reason": "No separately configured physical Common Allow sink; native audit and Common state remain separate."}, "audit"),
    }
    build_binding = source_receipt.parent.parent / "build-source-binding.json"
    if build_binding.is_file():
        observations["source_config_binding"]["evidence"].append(reference(build_binding, "source_manifest"))
        observations["source_config_binding"]["value"]["current_product_source_binding"] = load(build_binding)
    return {"run_scoped_case_id": contract.get("original_id") or contract["diagnostic_id"], "leg_id": "haproxy-native-htx", "run_id": raw[0]["run"], "execution_kind": "host_http", "execution_observed": True, "reviewed_by": "pending_root", "isolation_attempt_nonce": attempt.name.removeprefix("attempt-"), "effective_config_sha256": sha(data / "haproxy.cfg"), "rules_sha256": sha(data / "rules.conf"), "source_bound_fixture_contract": contract, "oracle_evaluated": None, "outcome": None, "full_lifecycle_qualified": None, "observations": observations, "raw_artifacts": [{"path": str(path), "sha256": sha(path), "bytes": path.stat().st_size} for path in sorted(data.iterdir()) if path.is_file() and path.name not in ("tls.key", "tls.pem")]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("attempt", "fixture", "binary", "source-receipt", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    result = observe(args.attempt, args.fixture, args.binary, args.source_receipt)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"id": result["run_scoped_case_id"], "fields": len(result["observations"]), "full_lifecycle_qualified": None}))


if __name__ == "__main__":
    main()
