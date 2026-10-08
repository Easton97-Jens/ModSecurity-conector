#!/usr/bin/env python3
"""Run closed real NGINX sequences, preserving native access/Engine evidence."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time

from nginx_sequence_client import run_sequence
from nginx_sequence_upstream import SynchronizedUpstream

import importlib.util


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


HERE = Path(__file__).resolve().parent
STARTUP = load("nginx_sequence_startup", HERE / "run-nginx-valid-rules.py")
BASE = STARTUP.BASE
from runtime_path_utils import open_private_runtime_root

SEQUENCES = {
    "single_request_cleanup": (200,), "multiple_sequential_requests": (200, 403, 200),
    "keep_alive_requests_if_supported": (200, 403, 200), "clean_shutdown": (200,),
    "keepalive_allow_allow": (200, 200), "keepalive_allow_deny_allow": (200, 403, 200),
    "early_mapping_failure_cleanup": (500,),
    "transaction_begin_failure_cleanup": (500,),
    "phase4_strict_http1_client_abort": (200,),
    "phase4_strict_host_survives": (200, 200),
    "phase4_strict_followup_request_succeeds": (200, 200),
    "keepalive_after_strict_new_connection": (200, 200),
    "keepalive_safe_followup": (200, 200),
    "response_short_write_resume": (200,),
    "response_write_would_block_resume": (200,),
    "transport_keep_alive": (200, 200),
    "transport_sequential_requests": (200, 403, 200),
    "finish_failure_propagation": (200,),
}
KEEPALIVE = {"keep_alive_requests_if_supported", "keepalive_allow_allow", "keepalive_allow_deny_allow", "keepalive_safe_followup"}
KEEPALIVE.update({"transport_keep_alive", "transport_sequential_requests"})
STRICT = {"phase4_strict_http1_client_abort", "phase4_strict_host_survives",
          "phase4_strict_followup_request_succeeds", "keepalive_after_strict_new_connection"}
WRITE = {"response_short_write_resume", "response_write_would_block_resume"}
LATE = STRICT | {"keepalive_safe_followup"} | WRITE


def sequence_config(output, port, projection, case_id, fault_transaction=None, upstream_port=None):
    text = STARTUP.config_template(output, port, str(projection))
    log = ('  log_format sequence escape=json \'{"uri":"$request_uri","status":$status,'
           '"connection":"$connection","connection_requests":$connection_requests,"remote_port":$remote_port,'
           '"transaction_id":"$request_id"}\';\n'
           f'  access_log "{output}/native-access.jsonl" sequence;\n'
           '  modsecurity_transaction_id "$request_id";')
    if case_id == "early_mapping_failure_cleanup":
        log = log.replace('modsecurity_transaction_id "$request_id";',
                          'modsecurity_transaction_id "$http_x_modsec_test_transaction";')
    if case_id == "transaction_begin_failure_cleanup":
        log = log.replace("$request_id", fault_transaction)
    if case_id == "finish_failure_propagation":
        log = log.replace("$request_id", "$sequence_transaction_id")
        log = ('  map $request_uri $sequence_transaction_id { default $request_id; '
               f'"/no-crs/sequence/{fault_transaction[:24]}/0" "{fault_transaction}"; }}\n' + log)
        text = text.replace('location / { try_files $uri /index.html; }',
                            'location / { try_files /index.html =404; }')
    if case_id in LATE:
        mode = "strict" if case_id in STRICT else "safe"
        log += f"\n  modsecurity_phase4_mode {mode};"
        text = text.replace('location / { try_files $uri /index.html; }',
                            'location / { proxy_buffering off; proxy_http_version 1.1; '
                            f'proxy_pass http://127.0.0.1:{upstream_port}; }}')
    return text.replace("  access_log off;", log).encode()


def private_json(output, leaf, value):
    if leaf not in {"sequence-observation.json", "sequence-source.json", "sequence-source.jsonl"}:
        raise ValueError("unrecognized sequence artifact")
    raw = json.dumps(value, sort_keys=True) + "\n"
    with open_private_runtime_root(output) as root:
        root.create_text(leaf, raw, "NGINX sequence observation")
    return raw.encode()


def read_access(output, count):
    path = output / "native-access.jsonl"
    deadline = time.monotonic() + 2
    while time.monotonic() < deadline:
        if path.exists():
            rows = [json.loads(line) for line in STARTUP.bounded_capture(path).splitlines() if line.strip()]
            if len(rows) >= count:
                return rows
        time.sleep(0.02)
    raise ValueError("native access records did not reach the required request count")


def run(args):
    binary, module, output = BASE.validate_inputs(args)
    if args.fault_negative_control and args.case_id not in WRITE | {"transaction_begin_failure_cleanup", "finish_failure_propagation"}:
        raise ValueError("fault negative control requires its exact native fixture case")
    if os.geteuid() != 0:
        raise ValueError("sequence operation requires isolated Root master and nobody worker")
    framework = BASE.absolute_path(args.framework_root)
    validator = load("nginx_sequence_contract", framework / "tests/runners/nginx_lifecycle_sequence.py")
    rules = framework / "tests/rules/no-crs-baseline.conf"
    parent = BASE.absolute_path(args.projection_parent)
    output.mkdir(mode=0o700)
    (output / "logs").mkdir(mode=0o700)
    hashes = {
        "binary_sha256": BASE.snapshot_artifact(binary, output / "nginx-binary", executable=True),
        "module_sha256": BASE.snapshot_artifact(module, output / "nginx-module.so", executable=False),
        "rules_sha256": BASE.snapshot_artifact(rules, output / "no-crs-baseline.conf", executable=False),
    }
    source = output / "docroot"
    source.mkdir(mode=0o700)
    for name in STARTUP.PROJECTION.PROJECTED_FILENAMES:
        (source / name).write_bytes(b"bounded-owned-sequence\n")
    identity = hashlib.sha256((args.run_id + ":" + args.case_id).encode()).hexdigest()
    token = identity[:24]
    projection = STARTUP.PROJECTION.prepare_projection(
        source_docroot=source, private_root=output, projection_parent=parent,
        projection_root=parent / ("sequence-" + token), worker_gid=65534,
        avoid_roots=[output, BASE.PARENT_ROOT, framework])
    with socket.socket() as reservation:
        reservation.bind(("127.0.0.1", 0))
        port = reservation.getsockname()[1]
    upstream = SynchronizedUpstream(backpressure=args.case_id == "response_write_would_block_resume") if args.case_id in LATE else None
    config = sequence_config(output, port, projection, args.case_id, identity[:32],
                             upstream.port if upstream is not None else None)
    (output / "nginx.conf").write_bytes(config)
    environment = BASE.configtest_environment(args.library_dir)
    write_fd = None
    if args.case_id == "transaction_begin_failure_cleanup":
        if args.fault_library is None:
            raise ValueError("native begin-failure operation requires its bounded fixture library")
        fault_library = BASE.absolute_path(args.fault_library)
        hashes["fault_library_sha256"] = BASE.snapshot_artifact(
            fault_library, output / "native-transaction-fault.so", executable=False)
        environment["LD_PRELOAD"] = str(output / "native-transaction-fault.so")
        environment["MSCONNECTOR_OWNED_BEGIN_FAULT"] = "one-native-allocation-failure"
        transaction = identity[:32]
        mismatch = transaction[:-1] + ("0" if transaction[-1] != "0" else "1")
        environment["MSCONNECTOR_OWNED_BEGIN_TXID"] = mismatch if args.fault_negative_control else transaction
    elif args.case_id in WRITE:
        if args.fault_library is None:
            raise ValueError("write-resume operation requires its bounded native fixture library")
        fault_library = BASE.absolute_path(args.fault_library)
        hashes["fault_library_sha256"] = BASE.snapshot_artifact(
            fault_library, output / "native-write-fault.so", executable=False)
        write_fd = os.open(output / "native-write-observations.jsonl", os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_WRONLY, 0o600)
        environment["LD_PRELOAD"] = str(output / "native-write-fault.so")
        environment["MSCONNECTOR_OWNED_WRITE_FAULT"] = "short_write" if args.case_id == "response_short_write_resume" else "write_would_block"
        if args.fault_negative_control:
            environment["MSCONNECTOR_OWNED_WRITE_FAULT"] = "disabled"
        environment["MSCONNECTOR_OWNED_WRITE_URI"] = f"/no-crs/sequence/{token}/0"
        environment["MSCONNECTOR_OWNED_WRITE_PORT"] = str(port)
        environment["MSCONNECTOR_OWNED_WRITE_FD"] = str(write_fd)
    elif args.case_id == "finish_failure_propagation":
        if args.fault_library is None:
            raise ValueError("post-response finish failure requires its exact owned native fixture")
        hashes["fault_library_sha256"] = BASE.snapshot_artifact(
            BASE.absolute_path(args.fault_library), output / "native-finish-fault.so", executable=False)
        write_fd = os.open(output / "native-finish-observations.jsonl", os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_WRONLY, 0o600)
        transaction = identity[:32]
        mismatch = transaction[:-1] + ("0" if transaction[-1] != "0" else "1")
        environment["LD_PRELOAD"] = str(output / "native-finish-fault.so")
        environment["MSCONNECTOR_OWNED_FINISH_TXID"] = mismatch if args.fault_negative_control else transaction
        environment["MSCONNECTOR_OWNED_FINISH_FD"] = str(write_fd)
    elif args.fault_library is not None:
        raise ValueError("fault fixture is only authorized for its exact native boundary case")
    argv = [str(output / "nginx-binary"), "-e", "stderr", "-c", str(output / "nginx.conf"), "-p", str(output) + "/"]
    exit_code, stdout, stderr, failure = BASE.invoke(argv + ["-t"], environment)
    (output / "configtest.stdout").write_bytes(stdout)
    (output / "configtest.stderr").write_bytes(stderr)
    roles = {"master_pid": 0, "worker_pid": 0, "master_uid": -1, "worker_uid": -1}
    process, handles = None, {}
    observations, access = [], []
    post_roles = None
    upstream_observation = None
    client_exit = None
    try:
        if failure or exit_code != 0:
            raise ValueError("native config acceptance is required before sequence")
        if upstream is not None:
            upstream.start()
        with (output / "startup.stdout").open("xb") as out, (output / "startup.stderr").open("xb") as err:
            process = subprocess.Popen(argv, env=environment, stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                                       pass_fds=() if write_fd is None else (write_fd,))
            roles = STARTUP.observe_roles(process, args.run_id, port, output, handles)
            with (output / "worker-maps.log").open("xb") as captured:
                captured.write(STARTUP.bounded_capture(Path("/proc") / str(roles["worker_pid"]) / "maps"))
            statuses = SEQUENCES[args.case_id]
            paths = [f"/no-crs/sequence/{token}/{index}" for index in range(len(statuses))]
            observations = run_sequence(port, paths, statuses, keepalive=args.case_id in KEEPALIVE,
                                        headers_seen=upstream.headers_seen if upstream is not None else None,
                                        expect_first_abort=args.case_id in STRICT,
                                        backpressure=args.case_id == "response_write_would_block_resume")
            client_exit = 0
            access = read_access(output, len(statuses))
            post_roles = STARTUP.observe_roles(process, args.run_id, port, output, handles)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        failure = str(exc)
        client_exit = 1
    finally:
        cleanup = STARTUP.stop_owned_master(process, roles, port, args.run_id, handles)
        if upstream is not None:
            upstream_observation = upstream.observation()
            upstream.stop()
        if write_fd is not None:
            os.fsync(write_fd)
            os.close(write_fd)
    observed = dict(schema_version=1, operation="request_sequence", protocol="http1", case_id=args.case_id,
                    run_id=args.run_id, client_exit_code=client_exit, requests=observations,
                    native_access=access, roles=roles, cleanup=cleanup)
    if args.case_id in LATE:
        observed["upstream_barrier"] = upstream_observation
        observed["post_sequence_roles"] = post_roles
        events_path = output / "phase1-events.jsonl"
        observed["native_events"] = [json.loads(line) for line in STARTUP.bounded_capture(events_path).splitlines()
                                     if line.strip()] if events_path.exists() else []
    if args.case_id in WRITE:
        observed["native_writes"] = [json.loads(line) for line in STARTUP.bounded_capture(
            output / "native-write-observations.jsonl").splitlines() if line.strip()]
    if args.case_id == "finish_failure_propagation":
        observed["native_finish"] = [json.loads(line) for line in STARTUP.bounded_capture(
            output / "native-finish-observations.jsonl").splitlines() if line.strip()]
    fault_contracts = {
        "early_mapping_failure_cleanup": ("early_mapping_failure", "ModSecurity: invalid canonical transaction identifier"),
        "transaction_begin_failure_cleanup": ("transaction_begin_failure", "ModSecurity: failed to create transaction"),
        "finish_failure_propagation": ("finish_failure", "ModSecurity: native logging phase processing failed"),
    }
    if args.case_id in fault_contracts:
        requested, diagnostic = fault_contracts[args.case_id]
        native_error = STARTUP.bounded_capture(output / "nginx-error.log")
        triggered = diagnostic.encode() in native_error
        observed["fault"] = {"requested": requested, "triggered": triggered,
                             "native_diagnostic": diagnostic if triggered else None}
    errors = validator.observation_errors(observed, args.case_id, args.run_id)
    if failure:
        errors.append(failure)
    observed_raw = private_json(output, "sequence-observation.json", observed)
    receipt = dict(hashes, schema_version=1, case_id=args.case_id, run_id=args.run_id,
                   operation="request_sequence", parent_sha=args.parent_sha,
                   framework_sha=args.framework_sha, mrts_sha=args.mrts_sha,
                   observed_exit_code=exit_code, client_exit_code=client_exit,
                   observed_sha256=BASE.digest(observed_raw), config_sha256=BASE.digest(config),
                   native_access_sha256=BASE.digest(STARTUP.bounded_capture(output / "native-access.jsonl"))
                       if (output / "native-access.jsonl").exists() else None,
                   projection_parent=str(parent), projection_root=str(projection))
    for key, leaf in {"events_sha256": "phase1-events.jsonl", "worker_maps_sha256": "worker-maps.log",
                      "native_writes_sha256": "native-write-observations.jsonl",
                      "native_finish_sha256": "native-finish-observations.jsonl"}.items():
        path = output / leaf
        if path.exists():
            receipt[key] = BASE.digest(STARTUP.bounded_capture(path))
    # Host-only evidence is not Canonical PASS for transport event contracts.
    row = {"case_id": args.case_id, "run_id": args.run_id, "live_executed": process is not None,
           "operation": "request_sequence", "sequence_observation_valid": not errors,
           "errors": errors, "sequence_receipt": receipt, "artifacts": {"sequence_dir": str(output)}}
    private_json(output, "sequence-source.json", {"cases": [row]})
    private_json(output, "sequence-source.jsonl", row)
    for error in errors:
        print(error, file=sys.stderr)
    return not errors


def main():
    parser = BASE.argument_parser()
    for action in parser._actions:
        if action.dest == "case_id":
            action.choices = tuple(SEQUENCES)
    parser.add_argument("--framework-root", required=True)
    parser.add_argument("--projection-parent", required=True)
    parser.add_argument("--fault-library")
    parser.add_argument("--fault-negative-control", action="store_true",
                        help="Deliberately mismatch the owned fault transaction; must not satisfy the fault case")
    args = parser.parse_args()
    try:
        return 0 if run(args) else 1
    except (OSError, ValueError) as exc:
        parser.exit(2, "sequence boundary rejected: " + str(exc) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
