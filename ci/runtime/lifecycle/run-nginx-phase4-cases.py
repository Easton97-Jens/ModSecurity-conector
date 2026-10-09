#!/usr/bin/env python3
"""Retain real bounded Phase-4 host observations, without synthetic events."""
import json
import os
from pathlib import Path
import re
import socket
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "common"))
import importlib.util


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


HOST = load("phase4_owned_host", HERE / "run-nginx-valid-rules.py")
from nginx_phase4_upstream import BoundedPhase4Upstream
CLIENT_STDOUT = "client.stdout"


def native_observations(raw, path):
    """Select only actual native response-body records matching this request."""
    events = [json.loads(line) for line in raw.splitlines() if line.strip()]
    if any(not isinstance(event, dict) for event in events):
        raise ValueError("native JSONL records must be objects")
    return [event for event in events if event.get("connector") == "nginx"
            and event.get("integration_mode") == "native-nginx-http-module"
            and event.get("phase") == "response_body"
            and event.get("method") == "GET" and event.get("uri") == path]


def configuration(output, port, upstream_port, projection, path, mode, run_id):
    if mode not in {"off", "safe"}:
        raise ValueError("closed Phase-4 driver allows only existing off and safe contracts")
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", run_id):
        raise ValueError("native transaction prefix must be bounded and configuration-safe")
    return (f'load_module "{output}/nginx-module.so";\n'
            'user nobody nogroup;\nworker_processes 1;\ndaemon off;\n'
            f'pid "{output}/nginx.pid";\nerror_log "{output}/nginx-error.log";\n'
            'events {}\nhttp { access_log off; modsecurity on;\n'
            f'modsecurity_transaction_id "{run_id}-$connection-$connection_requests";\n'
            f'modsecurity_rules_file "{output}/rules.conf";\n'
            f'modsecurity_phase4_mode {mode};\n'
            f'modsecurity_phase4_log "{output}/phase4-events.jsonl";\n'
            f'server {{ listen 127.0.0.1:{port}; root "{projection}";\n'
            f'location = {path} {{ proxy_pass http://127.0.0.1:{upstream_port}; '
            'proxy_http_version 1.1; proxy_buffering off; } } }\n')


def request_header_arguments(spec):
    """Return bounded literal header arguments for trusted closed adapters."""
    headers = spec.get("request_headers", {})
    if not isinstance(headers, dict) or len(headers) > 8:
        raise ValueError("closed request headers must be a mapping of at most eight fields")
    arguments = []
    total = 0
    for name, value in headers.items():
        if (not isinstance(name, str) or not re.fullmatch(r"[!#$%&'*+.^_`|~0-9A-Za-z-]{1,64}", name)
                or not isinstance(value, str) or len(value) > 256
                or any(ord(character) < 32 or ord(character) > 126 for character in value)):
            raise ValueError("closed request header has an invalid name/value or control byte")
        total += len(name) + len(value) + 2
        if total > 2048:
            raise ValueError("closed request headers exceed bounded total length")
        arguments.extend(("--header", name + ": " + value))
    return arguments


def actual_request(args, spec, output, environment, server):
    header_arguments = request_header_arguments(spec)
    body = output / "response.bin"
    # Retain an empty capture even when immediate rejection forwards no bytes.
    # Curl may otherwise omit its output file; a fresh exclusive leaf preserves
    # the distinction between observed zero bytes and an absent artifact.
    body.open("xb").close()
    with (output / CLIENT_STDOUT).open("wb") as out, (output / "client.stderr").open("wb") as err:
        client = subprocess.Popen(["/usr/bin/curl", "--noproxy", "*", "--http1.1", "--no-buffer", "--silent",
                                   "--show-error", "--max-time", "6", "--output", str(body),
                                   "--dump-header", str(output / "response.headers"),
                                   "--write-out", "%{http_code}",
                                   *header_arguments,
                                   f"http://127.0.0.1:{args.port}{spec['request_path']}"],
                                  env=environment, stdout=out, stderr=err)
        first_before_eos = False
        if spec["pause_between_chunks"]:
            deadline = time.monotonic() + 3
            while time.monotonic() < deadline and client.poll() is None:
                if server.paused.is_set() and body.exists() and body.stat().st_size > 0:
                    first_before_eos = not server.eos_sent.is_set()
                    break
                time.sleep(0.02)
        server.release.set()
        try:
            exit_code = client.wait(timeout=7)
        except subprocess.TimeoutExpired:
            client.kill()
            exit_code = client.wait(timeout=2)
        server.finished.wait(6)
    raw_status = HOST.bounded_capture(output / CLIENT_STDOUT)
    return {"client_exit_code": exit_code,
            "observed_http_status": int(raw_status) if raw_status.isdigit() else None,
            "response_bytes_received": body.stat().st_size if body.exists() else 0,
            "first_body_byte_before_upstream_eos": first_before_eos,
            "upstream": server.observations()}


def run(args):
    framework = HOST.BASE.absolute_path(args.framework_root)
    input_path = framework / "tests/runners/nginx_phase4_contracts.py"
    contracts = load("phase4_closed_inputs", input_path)
    return run_operation(args, contracts.operation(args.case_id), input_path=input_path)


def run_operation(args, spec, *, input_path,
                  upstream_factory=BoundedPhase4Upstream,
                  upstream_kwargs=None, configuration_factory=configuration,
                  observation_factory=native_observations,
                  upstream_path=HERE.parent / "common/nginx_phase4_upstream.py"):
    """Run a prevalidated closed operation using actual source-bound adapters.

    Callers own specification validation and trusted source/helper selection.
    Factories only select the bounded actual upstream and native configuration;
    artifact, role and cleanup authority remains in this shared runtime.
    """
    binary, module, output = HOST.BASE.validate_inputs(args)
    if os.geteuid() != 0:
        raise ValueError("native host observation requires isolated root master/nobody worker")
    framework = HOST.BASE.absolute_path(args.framework_root)
    input_path = HOST.BASE.absolute_path(input_path)
    upstream_path = HOST.BASE.absolute_path(upstream_path)
    output.mkdir(mode=0o700)
    binary_sha = HOST.BASE.snapshot_artifact(binary, output / "nginx-binary", executable=True)
    module_sha = HOST.BASE.snapshot_artifact(module, output / "nginx-module.so", executable=False)
    (output / "rules.conf").write_text(spec["rules"])
    source = output / "docroot"
    source.mkdir(mode=0o700)
    for name in HOST.PROJECTION.PROJECTED_FILENAMES:
        (source / name).write_bytes(b"phase4-owned-static\n")
    parent = HOST.BASE.absolute_path(args.projection_parent)
    projection = HOST.PROJECTION.prepare_projection(source_docroot=source, private_root=output,
        projection_parent=parent, projection_root=parent / args.run_id, worker_gid=65534,
        avoid_roots=[output, HOST.BASE.PARENT_ROOT, framework])
    with socket.socket() as reservation:
        reservation.bind(("127.0.0.1", 0))
        args.port = reservation.getsockname()[1]
    environment = HOST.BASE.configtest_environment(args.library_dir)
    process = None
    handles = {}
    roles = {}
    observations = {}
    failure = None
    try:
        with upstream_factory(tuple(chunk.encode() for chunk in spec["response_chunks"]),
                              pause=spec["pause_between_chunks"], **(upstream_kwargs or {})) as server:
            config = output / "nginx.conf"
            config.write_text(configuration_factory(output, args.port, server.port, projection, spec["request_path"], spec["nginx_phase4_mode"], args.run_id))
            code, stdout, stderr, failure = HOST.BASE.invoke(
                [str(output / "nginx-binary"), "-e", "stderr", "-t", "-c", str(config), "-p", str(output) + "/"], environment)
            (output / "configtest.stdout").write_bytes(stdout)
            (output / "configtest.stderr").write_bytes(stderr)
            observations["configtest_exit_code"] = code
            if code != 0 or failure:
                raise ValueError("actual configtest failed")
            with (output / "startup.stdout").open("wb") as out, (output / "startup.stderr").open("wb") as err:
                process = subprocess.Popen([str(output / "nginx-binary"), "-e", "stderr", "-c", str(config),
                    "-p", str(output) + "/"], env=environment, stdout=out, stderr=err)
                roles = HOST.observe_roles(process, args.run_id, args.port, output, handles)
                observations.update(actual_request(args, spec, output, environment, server))
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        failure = str(exc)
    finally:
        cleanup = HOST.stop_owned_master(process, roles, args.port, args.run_id, handles)
    events_path = output / "phase4-events.jsonl"
    raw = HOST.bounded_capture(events_path) if events_path.exists() else b""
    observations["native_events"] = observation_factory(raw, spec["request_path"])
    leaves = ("rules.conf", "nginx.conf", "configtest.stdout", "configtest.stderr",
              "startup.stdout", "startup.stderr", CLIENT_STDOUT, "client.stderr",
              "response.bin", "response.headers", "phase4-events.jsonl", "nginx-error.log")
    captures = {name: HOST.BASE.digest(HOST.bounded_capture(output / name))
                for name in leaves if (output / name).exists()}
    observations.update({"case_id": args.case_id, "run_id": args.run_id,
        "operation": spec["operation"], "source_record_id": spec["source_record_id"],
        "parent_sha": args.parent_sha,
        "framework_sha": args.framework_sha, "mrts_sha": args.mrts_sha,
        "binary_sha256": binary_sha, "module_sha256": module_sha,
        "raw_sha256": captures, "request_method": "GET", "request_path": spec["request_path"],
        "effective_phase4_mode": spec["nginx_phase4_mode"],
        "driver_sha256": HOST.BASE.digest(Path(__file__).read_bytes()),
        "closed_inputs_sha256": HOST.BASE.digest(input_path.read_bytes()),
        "upstream_driver_sha256": HOST.BASE.digest(upstream_path.read_bytes()),
        "docroot_projection_parent": str(parent), "docroot_projection_root": str(projection),
        "roles": roles, "cleanup": cleanup, "driver_error": failure,
        "canonical_status": "NOT_EXECUTED", "contract_validation_pending": True})
    HOST.write_json(output / "source-result.json", observations)
    return failure is None and cleanup["verified"]


def main():
    parser = HOST.BASE.argument_parser()
    parser.description = __doc__
    for action in parser._actions:
        if action.dest == "case_id":
            action.choices = None
    parser.add_argument("--projection-parent", required=True)
    parser.add_argument("--framework-root", required=True)
    try:
        return 0 if run(parser.parse_args()) else 1
    except (OSError, ValueError) as exc:
        print("phase4 input failure: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
