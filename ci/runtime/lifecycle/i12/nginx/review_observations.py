#!/usr/bin/env python3
"""Propose NGINX observations from physical files; never approve an oracle/PASS.

Root must separately review every proposed value and the effective oracle.
Absent selected native transactions remain unknown, including host parser denies.
"""

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat


ROOT = Path(__file__).resolve().parents[5]
SPEC = importlib.util.spec_from_file_location(
    "i12_nginx_review_schema", ROOT / "ci/evidence/reports/generate-pr382-i12-lifecycle-ledger.py")
SCHEMA = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SCHEMA)
SDK_SHA256 = "32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407"


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def lines(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def ref(path, role):
    return {**SCHEMA.ORACLES.reference(path), "role": role}


def absolute_path(value):
    path = PurePosixPath(value)
    if path.root != "/" or ".." in path.parts or str(path) != str(value):
        raise ValueError(f"Image path must be absolute and normalized: {value}")
    return path


def physical(runtime, attempt, admission):
    path = absolute_path(runtime)
    # These are virtual mount names in the admitted namespace, never host
    # temporary directories to open. Only their protected backing files are read.
    root = PurePosixPath("/var/tmp/codex/ModSecurity-conector")
    if path.is_relative_to(root):
        return attempt / "data" / path.relative_to(root)
    worker = PurePosixPath("/var/tmp/codex/ModSecurity-nginx-i12")
    if path.is_relative_to(worker):
        return attempt / "data/nginx-worker-runtime" / path.relative_to(worker)
    for binding in sorted(admission["bindings"], key=lambda item: len(item["target"]), reverse=True):
        target = absolute_path(binding["target"])
        if path.is_relative_to(target):
            return Path(absolute_path(binding["source"])) / path.relative_to(target)
    return Path(path)


def protected_image(path):
    """Hash one pinned regular image through protected, non-symlink ancestors.

    A root-owned sticky ancestor (such as the host's temporary mount) is
    acceptable: it protects the next, trusted-owner directory from replacement.
    Descendants and the final image must otherwise deny group/other writes.
    Directory descriptors and O_NOFOLLOW prevent check/open replacement races.
    """
    path = absolute_path(path)
    trusted_owners = {0, os.geteuid()}
    directory = os.open("/", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for component in path.parts[1:-1]:
            child = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                            dir_fd=directory)
            os.close(directory)
            directory = child
            info = os.fstat(directory)
            writable = info.st_mode & (stat.S_IWGRP | stat.S_IWOTH)
            sticky_root = info.st_uid == 0 and info.st_mode & stat.S_ISVTX
            if info.st_uid not in trusted_owners or (writable and not sticky_root):
                raise ValueError(f"Unprotected image directory: {path}")
        descriptor = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                             dir_fd=directory)
        with os.fdopen(descriptor, "rb") as stream:
            info = os.fstat(stream.fileno())
            if (not stat.S_ISREG(info.st_mode) or info.st_uid not in trusted_owners or
                    info.st_mode & (stat.S_IWGRP | stat.S_IWOTH)):
                raise ValueError(f"Unprotected or non-regular image: {path}")
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
            final = os.fstat(stream.fileno())
            if (info.st_size, info.st_mtime_ns, info.st_ctime_ns) != (
                    final.st_size, final.st_mtime_ns, final.st_ctime_ns):
                raise ValueError(f"Image changed while hashing: {path}")
            return info, digest
    finally:
        os.close(directory)


def loaded_images(out, attempt, admission, receipt, build):
    header, content = (out / "worker-self-maps.raw").read_bytes().split(b"\n", 1)
    identity = json.loads(header)
    roles = receipt["roles"]
    if not (identity["bytes"] == len(content) and identity["pid"] == roles["worker_pid"] and
            identity["uid"] == identity["gid"] == roles["worker_uid"] == 65534 and
            roles["master_uid"] == 0):
        raise ValueError("Loaded worker mappings do not bind Root-master/Nobody-worker")
    images, devices = [], []
    paths = {}
    for line in content.decode().splitlines():
        columns = line.split(None, 5)
        if len(columns) != 6 or not columns[5].startswith("/"):
            continue
        if columns[5].startswith("/dev/"):
            devices.append(line)
            continue
        paths[columns[5]] = int(columns[4])
    for runtime, inode in sorted(paths.items()):
        source = physical(runtime, attempt, admission)
        info, digest = protected_image(source)
        if info.st_ino != inode:
            raise ValueError(f"Mapped inode differs from physical image: {runtime}")
        images.append({"runtime_path": runtime, "physical_source": str(source), "inode": inode,
                       "sha256": digest, "mode": oct(stat.S_IMODE(info.st_mode)),
                       "uid": info.st_uid, "gid": info.st_gid})
    sdk = [item for item in images if "libmodsecurity.so" in item["runtime_path"]]
    modules = [item for item in images if item["sha256"] == build["module_sha256"]]
    if (not sdk or any(item["sha256"] != SDK_SHA256 for item in sdk) or not modules or
            sha(out / "nginx-module.so") != build["module_sha256"] or
            sha(out / "nginx-binary") != build["nginx_binary_sha256"]):
        raise ValueError("Actual mapped SDK/module or host binary differs from build receipt")
    return {"worker": identity, "roles": roles, "file_backed_images": images,
            "special_device_maps": devices, "sdk_version": build["sdk_version"],
            "sdk_sha256": SDK_SHA256, "module_sha256": build["module_sha256"],
            "host_binary_sha256": build["nginx_binary_sha256"]}


def propose(out, attempt, admission, controller, source_manifest, build_receipt, output):
    receipt_path = out / "full-observation-receipt.json"
    receipt, build = read(receipt_path), read(build_receipt)
    for relative, expected in receipt["raw_artifacts_sha256"].items():
        path = out / relative
        if not path.is_relative_to(out) or ".." in Path(relative).parts or path.is_symlink() or sha(path) != expected:
            raise ValueError(f"Raw artifact digest/path changed: {relative}")
    selected_clients = [client for client in receipt["clients"] if client["label"] == "selected"]
    if len(selected_clients) != 1:
        raise ValueError("Need exactly one selected actual client process")
    selected = selected_clients[0]
    client_observation = selected.get("observation", {})
    if (selected.get("direct_child_wait") is not True or
            not isinstance(selected.get("pid"), int) or selected["pid"] <= 0 or
            client_observation.get("pid") != selected["pid"]):
        raise ValueError("Selected client exit/signal is not bound to the directly waited client process")
    wire = (out / "selected-request.bin").read_bytes()
    uri = wire.split(b" ", 2)[1].decode("ascii")
    request_body = wire.split(b"\r\n\r\n", 1)[1]
    if client_observation.get("request_sha256") != sha(out / "selected-request.bin"):
        raise ValueError("Selected client does not bind actual request bytes")
    native = lines(out / "physical-lifecycle.jsonl")
    host = lines(out / "physical-host.jsonl")
    events = lines(out / "native-events.jsonl")
    selected_events = [event for event in events if event.get("uri") == uri]
    selection_binding = {"method": "unique native transaction at selected physical URI"}
    transaction_directives = re.findall(r"\bmodsecurity_transaction_id\s+([^;]+);", (out / "nginx.conf").read_text())
    if len(transaction_directives) == 1 and transaction_directives[0].strip() == "$http_x_i12_transaction":
        header_lines = wire.split(b"\r\n\r\n", 1)[0].split(b"\r\n")[1:]
        declared = [line.split(b":", 1)[1].strip().decode("ascii") for line in header_lines
                    if b":" in line and line.split(b":", 1)[0].lower() == b"x-i12-transaction"]
        if len(declared) != 1 or not declared[0]:
            raise ValueError("Configured custom native transaction ID lacks a unique selected wire header")
        selected_events = [event for event in selected_events if event.get("transaction_id") == declared[0]]
        selection_binding = {"method": "effective NGINX $http_x_i12_transaction directive and exact selected wire header",
                             "declared_native_transaction_id": declared[0],
                             "request": SCHEMA.ORACLES.reference(out / "selected-request.bin"),
                             "effective_configuration": SCHEMA.ORACLES.reference(out / "nginx.conf")}
    transactions = {event.get("transaction_id") for event in selected_events if event.get("transaction_id")}
    tx = next(iter(transactions)) if len(transactions) == 1 else None
    selected_native = [row for row in native if tx and row.get("transaction_id") == tx]
    scopes = {row["allocation_scope_call"] for row in selected_native if row.get("allocation_join_verified")}
    scope = next(iter(scopes)) if len(scopes) == 1 else None
    if scope is None:
        selected_native = []
    native_scope = [row for row in native if scope is not None and row.get("allocation_scope_call") == scope]
    callbacks = [row for row in host if scope is not None and row.get("allocation_scope_call") == scope]
    returns = [row for row in selected_native if row.get("edge") == "return"]
    calls = lambda name: [row for row in returns if row.get("function") == name]
    enters = lambda name: [row for row in selected_native if row.get("function") == name and row.get("edge") == "enter"]
    observations = {field: {"applicable": True, "value": None,
                           "reason": "No independently joined selected native transaction, or physical proof unavailable."}
                    for field in SCHEMA.ROLES}
    assertions, gaps = {}, []

    def put(field, value, *proofs):
        observations[field] = {"applicable": True, "value": value,
                               "evidence": [ref(path, role) for path, role in proofs]}

    api = (out / "physical-lifecycle.jsonl", "native_api")
    cb = (out / "physical-host.jsonl", "host_callback")
    sink = (out / "native-events.jsonl", "physical_event_sink")
    cli = (out / "selected/client-observation.json", "client_process")
    back = (out / "backend.json", "backend_process")
    isolation = (attempt / "controller-result.json", "isolation_receipt")
    cleanup = (receipt_path, "cleanup_observer")
    fixture = read(out / "fixture.json")
    # The admitted runner snapshot may intentionally contain only ci/ helpers.
    # Connector contracts belong to the independently recorded build snapshot.
    source = Path(build["source_snapshot"])
    for relative in ("connectors/nginx/src/ngx_http_modsecurity_access.c",
                     "connectors/nginx/src/ngx_http_modsecurity_body_filter.c"):
        units = [unit for unit in build["compiled_parent_units"]
                 if unit["compiled_source"] == str(source / relative)]
        if len(units) != 1 or sha(source / relative) != units[0]["compiled_source_sha256"]:
            raise ValueError("Build snapshot source contract bytes changed: " + relative)
    assertions["raw_artifact_digests_match"] = True
    assertions["config_loaded"] = receipt.get("configtest_exit") == 0
    assertions["receipt_errors_empty"] = not receipt.get("errors")
    assertions["selected_transaction_unique"] = len(transactions) == 1
    assertions["selected_allocation_unique"] = len(scopes) == 1
    assertions["native_invalid_rows_absent"] = not any(row.get("invalid") for row in native)
    assertions["selected_native_nobody"] = bool(selected_native) and all(
        row.get("uid") == row.get("gid") == 65534 for row in selected_native)
    assertions["callbacks_owned_by_worker"] = bool(callbacks) and all(
        row.get("pid") == receipt["roles"]["worker_pid"] for row in callbacks)
    try:
        identity = loaded_images(out, attempt, admission, receipt, build)
        put("product_host_identity", identity, (out / "worker-self-maps.raw", "loaded_image"), isolation)
        assertions["actual_loaded_image_binding"] = True
    except (OSError, ValueError, KeyError) as exc:
        gaps.append("Loaded-image binding: " + str(exc))
        assertions["actual_loaded_image_binding"] = False
    put("source_config_binding", {"parent_sha": receipt["parent_sha"],
        "framework_sha": receipt["framework_sha"], "mrts_sha": receipt["mrts_sha"],
        "config_sha256": sha(out / "nginx.conf"), "rules_sha256": sha(out / "no-crs-baseline.conf"),
        "build_receipt": SCHEMA.ORACLES.reference(build_receipt)},
        (source_manifest, "source_manifest"), (build_receipt, "source_manifest"),
        (out / "nginx.conf", "effective_configuration"), (out / "no-crs-baseline.conf", "effective_configuration"))
    if callbacks:
        put("capability", {"route": "nginx-native", "actual_callbacks": callbacks,
            "configured_mode": fixture["mode"], "native_body_limits_owner": "libModSecurity"},
            cb, (source / "connectors/nginx/src/ngx_http_modsecurity_access.c", "source_contract"),
            (source / "connectors/nginx/src/ngx_http_modsecurity_body_filter.c", "source_contract"))
    put("client_exit", {"exit": selected["exit_code"], "pid": selected["pid"],
                        "observation_pid": client_observation["pid"],
                        "direct_child_wait": selected["direct_child_wait"],
                        "waited_monotonic_ns": selected["waited_monotonic_ns"],
                        "argv": selected["argv"]}, (receipt_path, "client_process"))
    put("client_signal", {"signal": selected["signal"], "process_waited": True,
                           "direct_child_wait": selected["direct_child_wait"],
                           "pid": selected["pid"]}, (receipt_path, "client_process"))
    headers = out / "selected/headers.bin"
    response_path = out / "selected/response.bin"
    put("client_headers", {"raw_latin1": headers.read_bytes().decode("latin1") if headers.exists() else None,
                           "headers_received": headers.exists(),
                           "http_status": selected["observation"].get("status")},
        (headers if headers.exists() else response_path, "client_process"))
    body_path = out / "selected/body.bin"
    complete_body = body_path.exists()
    if not complete_body:
        body_path = out / "selected/body-fragment.bin"
    body = body_path.read_bytes() if body_path.exists() else b""
    body_kind = "decoded_entity" if complete_body else "unparsed_wire_body_fragment"
    assertions["client_body_digest_size_match"] = (
        len(body) == selected["observation"].get("body_bytes" if complete_body else "fragment_bytes", 0) and
        (hashlib.sha256(body).hexdigest() == selected["observation"].get(
            "body_sha256" if complete_body else "fragment_sha256") if body_path.exists() else not response_path.read_bytes()))
    put("client_bytes", {"size": len(body), "body_hex": body.hex(), "kind": body_kind,
                         "framing_complete": selected["observation"].get("framing_complete")},
        (body_path if body_path.exists() else response_path, "client_process"))
    put("client_sha256", {"body_or_fragment": hashlib.sha256(body).hexdigest(), "kind": body_kind,
                           "response": sha(response_path)}, cli)
    backend_window = {"uri": uri, "client_started_monotonic_ns": selected["started_monotonic_ns"],
                      "client_waited_monotonic_ns": selected["waited_monotonic_ns"],
                      "scope": "Physical backend receipt time within selected client lifetime; later same-URI controls excluded"}
    backend = [row for row in receipt["backend"] if row["path"] == uri and
               selected["started_monotonic_ns"] <= row["received_monotonic_ns"] <= selected["waited_monotonic_ns"]]
    followup_backend = [row for row in receipt["backend"] if row["path"] == "/ngxi12/followup"]
    put("backend_request_count", {"selected": len(backend), "followup": len(followup_backend),
                                 "selected_binding": backend_window,
                                 "all_actual_backend_rows": receipt["backend"]}, back)
    if len(backend) == 1:
        request_match = hashlib.sha256(request_body).hexdigest() == backend[0]["body_sha256"]
        response_match = hashlib.sha256(body).hexdigest() == backend[0]["response_sha256"] if complete_body else None
        put("backend_payload_identity", {"actual_backend": backend[0], "request_body_matches": request_match,
            "client_response_matches_full_backend_payload": response_match,
            "request_body_sha256": hashlib.sha256(request_body).hexdigest()}, back, cli)
        put("client_backend_correlation", {"selected_uri": uri, "native_transaction_id": tx,
            "request_body_matches": request_match, "actual_backend": backend[0],
            "selected_client": selected["observation"]}, back, cli)
    else:
        if not backend:
            status = selected["observation"].get("status")
            if fixture.get("response_file") and isinstance(status, int) and 200 <= status < 300:
                reason = ("Zero selected backend requests physically observed because the selected location uses "
                          "NGINX's static alias/sendfile content handler")
                contract = source / "connectors/nginx/src/ngx_http_modsecurity_body_filter.c"
                disposition = "static_content_path"
            else:
                reason = "Zero selected backend requests physically observed; native/host handling prevented forwarding"
                contract = source / "connectors/nginx/src/ngx_http_modsecurity_access.c"
                disposition = "prevented_forwarding"
            prevented = {"reason": reason, "disposition": disposition,
                         "source_contract": SCHEMA.ORACLES.reference(contract)}
            put("backend_payload_identity", {"selected_backend_requests": 0,
                "request_body_equality": None, "response_body_equality": None,
                "prevented_forwarding": prevented}, back, cli)
            put("client_backend_correlation", {"selected_uri": uri, "selected_backend_requests": 0,
                "native_transaction_id": tx, "request_sha256": sha(out / "selected-request.bin"),
                "prevented_forwarding": prevented}, back, cli)
        else:
            gaps.append("Multiple selected backend requests; no unique client/backend payload equality asserted")
    if selected_native:
        scoped_fixture_events = {}
        native_proofs = [api]
        for filename, label in (("input-fault.jsonl", "mapper_fault"),
                                ("budget-fault.jsonl", "engine_budget"),
                                ("invalid-return.jsonl", "invalid_native_return")):
            trace = out / filename
            if not trace.exists():
                continue
            actual = lines(trace)
            matched = [item for item in actual if item.get("transaction_id") == tx]
            if not actual or len(matched) != len(actual):
                raise ValueError(f"Scoped fixture trace does not bind only the selected native transaction: {filename}")
            scoped_fixture_events[label] = matched
            native_proofs.append((trace, "native_api"))
        assertions["scoped_fixture_traces_bind_selected_transaction"] = bool(
            not scoped_fixture_events or all(scoped_fixture_events.values()))
        put("native_events", selected_events, sink)
        put("native_api_returns", {"measured_calls": returns,
            "unintercepted_calls": ["connection", "URI", "header-add"],
            "scoped_fixture_events": scoped_fixture_events}, *native_proofs)
        put("native_transaction_id", {"value": tx, "source": "sdk_public_m_id", "allocation_scope_call": scope,
                                       "selection_binding": selection_binding}, api)
        common = {row.get("canonical_transaction_id") for row in selected_native if row.get("canonical_transaction_id")}
        if len(common) == 1:
            put("common_transaction_id", {"canonical": next(iter(common)), "mapped_native_id": tx}, api)
        put("observed_handle_association", {"allocation_scope_call": scope, "actual_rows": native_scope,
                                           "verified_join_rows": [row for row in selected_native if row.get("allocation_join_verified")]}, api)
        phase_calls = [row for row in returns if row.get("function", "").startswith("native_process_")]
        put("native_phases", {"actual_reached_calls": phase_calls,
                              "absent_phase_calls_are_not_fabricated": True}, api)
        put("native_body_chunks", {"request": calls("native_append_request_body"),
            "response": calls("native_append_response_body"), "host_buffer_state": callbacks}, api)
        put("native_intervention_or_first_cause", {"actual_interventions": calls("native_intervention"),
            "actual_contract_states": [row.get("contract_state") for row in returns if row.get("contract_state")],
            "actual_error_events": [row for row in selected_events if row.get("status") == "error"],
            "scoped_fixture_events": scoped_fixture_events,
            "requested_fixture_rule_is_not_an_observation": True}, *native_proofs)
        terminals = [row for row in callbacks if row.get("operation") in (
            "request_eos", "request_before_native_finalize", "response_eos")]
        p2, p4 = enters("native_process_request_body"), enters("native_process_response_body")
        request_notes = [row for row in terminals if row.get("operation") == "request_before_native_finalize"]
        legacy_request = [row for row in terminals if row.get("operation") == "request_eos"]
        response_notes = [row for row in terminals if row.get("operation") == "response_eos"]
        request_terminal = request_notes or legacy_request
        request_valid = bool(request_terminal) and all(row.get("remaining") == 0 for row in request_terminal)
        if request_notes:
            request_valid = request_valid and all(
                (row.get("temp_file_present") == 1 and row.get("temp_file_offset") == len(request_body) and
                 row.get("request_body_bytes_seen") == len(request_body)) or
                (row.get("temp_file_present") == 0 and row.get("request_body_bytes_seen") == len(request_body))
                for row in request_notes)
        response_valid = bool(response_notes) and all(row.get("last_buf") or row.get("last_in_chain") for row in response_notes)
        request_once = (len(request_terminal) == len(p2) == 1 and request_valid and
                        request_terminal[0]["monotonic_ns"] < p2[0]["monotonic_ns"])
        response_once = (len(response_notes) == len(p4) == 1 and response_valid and
                         response_notes[0]["monotonic_ns"] < p4[0]["monotonic_ns"])
        assertions.update(request_terminal_to_p2_once=request_once,
                          response_terminal_to_p4_once=response_once)
        put("host_eos", {"actual_terminal_callbacks": terminals,
            "request_terminal_valid": request_valid, "response_terminal_valid": response_valid,
            "absent_terminal": "No callback measured for unreached/failed body paths"}, cb)
        put("native_eos", {"actual_terminal_callbacks": terminals, "p2_actual_enter": p2, "p4_actual_enter": p4,
            "request_terminal_precedes_single_p2": request_once, "response_terminal_precedes_single_p4": response_once,
            "append_api_eos_argument": None, "scope": "Native process-body finalization paired with actual host terminal; no EOF or zero-byte append inference"}, api, cb)
        put("commit_order", {"actual_host_callbacks": callbacks,
            "actual_common_commit": calls("common_set_response_committed"),
            "client_first_response_monotonic_ns": selected["observation"].get("first_response_monotonic_ns"),
            "p4_actual_enters": p4}, cb, cli)
        debug_path = out / "native-sdk-debug.log"
        debug = [line for line in debug_path.read_text(errors="replace").splitlines() if "[" + uri + "]" in line]
        log_path = out / "nginx-error.log"
        log = [line for line in log_path.read_text(errors="replace").splitlines()
               if '[uri "' + uri + '"]' in line and '[unique_id "' + tx + '"]' in line]
        put("mime_gate", {"selected_debug": debug, "actual_sdk_host_log": log,
            "actual_common_events": selected_events, "sdk_fixture_semantics": "3.0.14 MIME list retained; no Clear reset inferred"},
            (debug_path, "native_debug"), (log_path, "physical_event_sink"), sink)
        put("finish_calls", {"common_finish": calls("common_finish"), "native_logging": calls("native_process_logging")}, api)
        put("finish_transitions", {"complete_phase": calls("common_complete_phase"), "common_finish": calls("common_finish")}, api)
        put("native_free_calls", {"count": len(calls("native_cleanup")), "actual_calls": calls("native_cleanup"),
                                  "void_return_not_synthetic_zero": True}, api)
        retire = [row for row in native_scope if row.get("function") == "host_association_retire"]
        assertions["native_cleanup_once"] = len(calls("native_cleanup")) == 1
        assertions["native_logging_once"] = len(calls("native_process_logging")) == 1
        assertions["common_finish_once"] = len(calls("common_finish")) == 1
        put("descriptor_cleanup", {"actual_cleanup_callbacks": [row for row in callbacks if row.get("operation", "").startswith("cleanup")],
            "actual_fd_counts": [row.get("fd_count") for row in callbacks if "fd_count" in row],
            "actual_mapping_retire": retire}, (out / "physical-host.jsonl", "cleanup_observer"))
        put("physical_event_order", {"ordered_selected_events": selected_events,
            "source": "Original physical append-only JSONL order"}, sink)
        put("terminal_event_count", {"transaction_cleanup": sum(row.get("event") == "transaction_cleanup" for row in selected_events),
            "phase4_completion": sum(row.get("event") == "phase4_completion" for row in selected_events),
            "actual_errors": sum(row.get("status") == "error" for row in selected_events)}, sink)
        put("host_action", {"actual_http_status": selected["observation"].get("status"),
            "actual_body_bytes": len(body), "actual_host_callbacks": callbacks, "actual_events": selected_events}, cb, cli)
    else:
        gaps.append("No unique URI/native transaction/allocation join; native observations remain unknown")
    put("cleanup_receipts", {"actual_host": receipt["cleanup"], "actual_master_wait_result": receipt.get("master_wait_result"),
        "actual_master_signal": receipt.get("master_signal"), "observer_finals": [row for row in native if row.get("function") == "observer" and row.get("edge") == "final"]}, cleanup, isolation)
    put("process_listener_cleanup", {"host": receipt["cleanup"], "namespace_survivors": controller["surviving_namespace_pids"],
        "outside_mount_leaks": controller["outside_mount_leaks"], "supervisor_reaped": controller["supervisor_reaped"]}, cleanup, isolation)
    followup = [client for client in receipt["clients"] if client["label"] == "followup"]
    put("neighbor_health", {"actual_followup_clients": followup, "actual_followup_backend": followup_backend},
        (receipt_path, "client_process"), back)
    put("transport_framing", selected["observation"], cli)
    put("transport_reset_scope", {"actual_client_observation": selected["observation"],
        "scope": "Only selected HTTP/1 connection; no HTTP/2 stream/reset claim"}, cli)
    assertions["host_cleanup_verified"] = receipt["cleanup"].get("verified") is True
    packet = {"schema_version": 1, "run_scoped_case_id": receipt["selected_id"], "leg_id": "nginx-native",
        "run_id": receipt["run_id"], "parent_sha": receipt["parent_sha"], "framework_sha": receipt["framework_sha"],
        "mrts_sha": receipt["mrts_sha"], "effective_config_sha256": sha(out / "nginx.conf"),
        "execution_observed": True, "execution_kind": "host_http", "reviewed_by": None,
        "oracle_evaluated": False, "outcome": None, "full_lifecycle_qualified": False,
        "observations": observations, "scope": "Unapproved physical observations; independent Root/oracle review required"}
    destination = output / (out.name + "-proposed.json")
    for field, observation in observations.items():
        SCHEMA.measurement(field, observation, destination)
    with destination.open("x") as stream:
        json.dump(packet, stream, indent=2)
        stream.write("\n")
    return {"run_scoped_case_id": receipt["selected_id"], "packet": SCHEMA.ORACLES.reference(destination),
        "request_identity": {"physical_request_path": str(out / "selected-request.bin"), "transaction_id": tx},
        "measured_assertions": assertions, "unknown_fields": [name for name, item in observations.items() if item["value"] is None],
        "gaps": gaps, "full_lifecycle_qualified": False, "oracle_review_performed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("attempt", "source-manifest", "build-receipt", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    controller = read(args.attempt / "controller-result.json")
    admission_path = args.attempt / "admission.original.json"
    live_admission = read(admission_path)
    sealed_specs = [path for path in (args.attempt / "executed-input-originals").iterdir()
                    if path.is_file() and sha(path) == controller["spec_sha256"]]
    if len(sealed_specs) != 1:
        raise ValueError("Exactly one retained sealed execution spec must match controller SHA256")
    admission = read(sealed_specs[0])
    if (sha(admission_path) != controller["admission_sha256"] or
            controller["executed_input_hashes_before"] != controller["executed_input_hashes_after"] or
            controller["surviving_namespace_pids"] or controller["outside_mount_leaks"] or
            controller.get("timeout") or controller.get("errors") or controller.get("resource_violation")):
        raise ValueError("Sealed attempt source/isolation integrity is not established")
    if not live_admission.get("namespaces") or not live_admission.get("argv"):
        raise ValueError("Live runtime admission lacks observed namespaces/argv")
    source_bindings = [binding for binding in admission["bindings"] if binding.get("ledger") == str(args.source_manifest)]
    if len(source_bindings) != 1 or sha(args.source_manifest) != source_bindings[0]["ledger_sha256"]:
        raise ValueError("Source manifest does not bind this admitted host attempt")
    args.output.mkdir(parents=True, exist_ok=True)
    summaries = []
    for path in sorted((args.attempt / "data").rglob("full-observation-receipt.json")):
        try:
            summaries.append(propose(path.parent, args.attempt, admission, controller,
                                     args.source_manifest, args.build_receipt, args.output))
        except (OSError, ValueError, KeyError, TypeError) as exc:
            summaries.append({"raw_receipt": str(path), "gaps": [str(exc)], "packet": None,
                              "full_lifecycle_qualified": False})
    result = {"scope": "PROPOSED only; no oracle evaluation or PASS", "attempt": str(args.attempt),
              "controller_exit": controller["controller_exitcode"], "driver_exit": controller["exitcode"],
              "proposed_packets": sum(row.get("packet") is not None for row in summaries),
              "full_lifecycle_qualified": False, "cases": summaries}
    with (args.output / "candidate-summary.json").open("x") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")
    print(json.dumps({"cases": len(summaries), "proposed_packets": result["proposed_packets"],
                      "full_lifecycle_qualified": False}))


if __name__ == "__main__":
    main()
