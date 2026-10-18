#!/usr/bin/env python3
"""Real NGINX I12 observations in the sealed controller; no PASS synthesis."""
from __future__ import annotations

import argparse
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer
import importlib.util
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile
import threading
import time

from scenarios import cases, serializable


def storage_root():
    """Require the configured private project anchor, with no temp fallback."""
    value = os.environ.get("CODEX_TEMP_ROOT", "")
    match = re.fullmatch(r"/[A-Za-z0-9_./-]+", value)
    if match is None:
        raise ValueError("canonical CODEX_TEMP_ROOT required")
    root = Path(match.group(0))
    if (str(root) != value or root != root.resolve() or root == Path("/") or
            ".." in root.parts):
        raise ValueError("canonical CODEX_TEMP_ROOT required")
    info = root.lstat()
    if (not stat.S_ISDIR(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o022):
        raise ValueError("private root-owned CODEX_TEMP_ROOT required")
    return root


def client_environment(parser_environment):
    """Pass only the validated storage anchor alongside the filtered host env."""
    return {**parser_environment, "CODEX_TEMP_ROOT": str(storage_root())}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Backend(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        if not 0 <= length <= 4 * 1024 * 1024:
            raise ValueError("bounded backend entity required")
        body = self.rfile.read(length)
        selected = self.path.endswith("/selected")
        row = self.server.fixture
        response = row["response"] if selected else b"NGXI12_RSP neighbor healthy\n"
        item = {"path": self.path, "body_bytes": len(body), "body_sha256": hashlib.sha256(body).hexdigest(),
                "response_bytes": len(response), "response_sha256": hashlib.sha256(response).hexdigest(),
                "request_transaction": self.headers.get("X-I12-Transaction"),
                "received_monotonic_ns": time.monotonic_ns(), "writes": []}
        self.send_response(200)
        content_type = row["response_type"] if selected else "text/plain"
        if content_type:
            self.send_header("Content-Type", content_type)
        if selected and row.get("response_header"):
            self.send_header("X-Modsec-Upstream", row["response_header"])
        chunked = selected and row["chunked"]
        self.send_header("Transfer-Encoding" if chunked else "Content-Length", "chunked" if chunked else str(len(response)))
        self.send_header("Connection", "close")
        self.end_headers()
        parts = row["response_parts"] if selected else 1
        try:
            for index in range(parts):
                data = response[index * len(response) // parts:(index + 1) * len(response) // parts]
                if chunked and data:
                    self.wfile.write(f"{len(data):x}\r\n".encode() + data + b"\r\n")
                elif not chunked:
                    self.wfile.write(data)
                self.wfile.flush()
                item["writes"].append({"bytes": len(data), "returned_monotonic_ns": time.monotonic_ns()})
                if parts > 1:
                    time.sleep(0.08)
            if chunked:
                self.wfile.write(b"0\r\n\r\n")
                self.wfile.flush()
            item["write_completed"] = True
        except OSError as exc:
            item["write_completed"] = False
            item["write_error"] = type(exc).__name__
        finally:
            item["finished_monotonic_ns"] = time.monotonic_ns()
            self.server.observations.append(item)

    do_GET = do_POST

    def log_message(self, *args):
        pass


def configuration(raw, output, port, backend_port, row, worker, environment):
    text = raw.config_template(output, port, backend_port)
    text = text.replace("events {}", "\n".join("env " + key + ";" for key in environment if key.startswith("MSCONNECTOR_")) + "\nevents {}")
    text = text.replace("modsecurity on;", "modsecurity on; modsecurity_phase4_mode " + row["mode"] + ";")
    text = text.replace("location / { proxy_pass", "location / { proxy_http_version 1.1; proxy_buffering off; proxy_pass")
    # Keep NGINX's own client-body ceiling above the bounded 2 MiB native
    # cases.  Otherwise its default 1 MiB parser limit would mask the former
    # connector-limit regression before the request reached ModSecurity.
    directives = (f'client_body_temp_path "{worker}/client"; proxy_temp_path "{worker}/proxy";\n'
                  + "client_max_body_size 4m;\n"
                  + ("client_body_in_file_only clean; client_body_buffer_size 1k;\n" if row["request_file"] else "")
                  + row["nginx_directives"])
    if row["fault"] or row.get("budget_phase") or row.get("invalid_return"):
        directives += "modsecurity_transaction_id $http_x_i12_transaction;\n"
    if row.get("budget_phase"):
        directives += "modsecurity_engine_call_budget_ms 10;\n"
    text = text.replace("http {", "http {\n" + directives)
    if row["response_file"]:
        text = text.replace("location / {", f'location = /ngxi12/selected {{ alias "{worker}/payload.txt"; default_type text/plain; sendfile on; }}\n    location / {{')
    return text


def rules(output, row, framework):
    baseline = (framework / "tests/rules/no-crs-baseline.conf").read_text()
    return (baseline + f'\nSecRequestBodyLimit {row["request_limit"]}\nSecRequestBodyNoFilesLimit {row["request_limit"]}\n'
            + f'SecRequestBodyLimitAction {row["request_action"]}\nSecResponseBodyLimit {row["response_limit"]}\n'
            + f'SecResponseBodyLimitAction {row["response_action"]}\nSecDebugLog "{output}/native-sdk-debug.log"\nSecDebugLogLevel 9\n'
            + 'SecRule REQUEST_BODY "@contains NGXI12_REQ" "id:941002,phase:2,pass,log,msg:\'NGXI12_REQUEST_BODY_PRIMARY\'"\n'
            + 'SecRule RESPONSE_BODY "@contains NGXI12_RSP" "id:941004,phase:4,pass,log,msg:\'NGXI12_RESPONSE_BODY_PRIMARY\'"\n'
            + row["extra_rules"])


def run_one(args, row, raw, maps):
    output = args.output_root / row["case_id"]
    args.output_root.mkdir(exist_ok=True, mode=0o700)
    local_args = argparse.Namespace(**vars(args))
    local_args.output_root = str(output)
    # The preserved observer accepts run labels up to64 bytes. The complete
    # original ID remains independently present in its128-byte case field.
    local_args.run_id = args.run_prefix + "-" + hashlib.sha256(row["case_id"].encode()).hexdigest()[:16]
    local_args.nginx_binary, local_args.module = str(args.nginx_binary), str(args.module)
    binary, module, output = raw.BASE.validate_inputs(local_args)
    if os.geteuid() != 0:
        raise ValueError("actual root master required")
    output.mkdir(mode=0o700)
    environment = raw.BASE.configtest_environment(str(args.library_dir))
    raw.BASE.snapshot_artifact(binary, output / "nginx-binary", executable=True)
    raw.BASE.snapshot_artifact(module, output / "nginx-module.so", executable=False)
    backend = HTTPServer(("127.0.0.1", 0), Backend)
    backend.fixture, backend.observations = row, []
    thread = threading.Thread(target=backend.serve_forever, daemon=True)
    port = raw.reserve_port()
    # Atomically reserve an unpredictable root-owned directory. The Nobody
    # worker may traverse it, but cannot replace files or plant child symlinks.
    # The sealed controller admits this tree as writable and maps it back to
    # nginx-worker-runtime; its parent remains read-only inside the namespace.
    scratch_parent = storage_root().with_name("ModSecurity-nginx-i12")
    metadata = scratch_parent.lstat()
    if (scratch_parent.resolve() != scratch_parent or not stat.S_ISDIR(metadata.st_mode)
            or metadata.st_uid != 0 or metadata.st_mode & 0o022):
        raise ValueError("root-owned non-writable worker scratch parent required")
    for ancestor in scratch_parent.parents:
        info = ancestor.lstat()
        sticky_root = (stat.S_ISDIR(info.st_mode) and info.st_uid == 0
                       and info.st_mode & stat.S_ISVTX)
        if (not stat.S_ISDIR(info.st_mode) or info.st_uid != 0 or
                info.st_mode & 0o022 and not sticky_root):
            raise ValueError("protected root-owned worker scratch ancestry required")
    worker = Path(tempfile.mkdtemp(prefix="nginx-i12-", dir=scratch_parent))
    worker.chmod(0o711)
    for leaf in ("client", "proxy"):
        path = worker / leaf
        path.mkdir(mode=0o700)
        os.chown(path, 65534, 65534)
    if row["response_file"]:
        (worker / "payload.txt").write_bytes(row["response"])
        (worker / "payload.txt").chmod(0o444)
    descriptors, handles, clients, errors = [], {}, [], []
    process, capture = None, None
    roles = {"run_id": local_args.run_id, "master_pid": 0, "worker_pid": 0, "master_uid": -1, "worker_uid": -1}
    cleanup, configcode = {}, None
    for leaf, key in (("physical-lifecycle.jsonl", "MSCONNECTOR_LIFECYCLE_FD"), ("physical-host.jsonl", "MSCONNECTOR_NGX_HOST_FD")):
        descriptor = os.open(output / leaf, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_APPEND, 0o600)
        os.fchmod(descriptor, 0o600)
        descriptors.append(descriptor)
        environment[key] = str(descriptor)
    environment.update(MSCONNECTOR_LIFECYCLE_RUN=local_args.run_id, MSCONNECTOR_LIFECYCLE_PROFILE="nginx-native",
                       MSCONNECTOR_LIFECYCLE_CASE="I12::nginx-native::" + row["case_id"])
    if row["fault"]:
        descriptor = os.open(output / "input-fault.jsonl", os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_APPEND, 0o600)
        descriptors.append(descriptor)
        environment.update(LD_PRELOAD=str(args.input_fault_library), MSCONNECTOR_OWNED_INPUT_FD=str(descriptor),
                           MSCONNECTOR_OWNED_INPUT_FAULT=row["fault"], MSCONNECTOR_OWNED_INPUT_TXID="a" * 32)
    if row.get("budget_phase"):
        descriptor = os.open(output / "budget-fault.jsonl", os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_APPEND, 0o600)
        descriptors.append(descriptor)
        environment.update(LD_PRELOAD=str(args.budget_fault_library), MSCONNECTOR_OWNED_BUDGET_FD=str(descriptor),
                           MSCONNECTOR_OWNED_BUDGET_PHASE=str(row["budget_phase"]), MSCONNECTOR_OWNED_BUDGET_TXID="a" * 32)
    if row.get("invalid_return"):
        descriptor = os.open(output / "invalid-return.jsonl", os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_APPEND, 0o600)
        descriptors.append(descriptor)
        environment.update(LD_PRELOAD=str(args.invalid_return_library), MSCONNECTOR_I12_INVALID_FD=str(descriptor),
                           MSCONNECTOR_I12_INVALID_TXID="a" * 32)
    capture = maps.Capture(local_args, output, environment, {}, raw.HOST)
    descriptors.extend(capture.descriptors())
    thread.start()
    try:
        (output / "no-crs-baseline.conf").write_text(rules(output, row, args.framework_root))
        (output / "fixture.json").write_text(json.dumps(serializable(row), indent=2) + "\n")
        (output / "nginx.conf").write_text(configuration(raw, output, port, backend.server_port, row, worker, environment))
        argv = [str(output / "nginx-binary"), "-e", "stderr", "-t", "-c", str(output / "nginx.conf"), "-p", str(output) + "/"]
        # Preload constructors require an empty evidence inode at actual master
        # startup. The parser runs without test faults/self-map preloads.
        parser_env = {key: value for key, value in environment.items() if key != "LD_PRELOAD" and not key.startswith("MSCONNECTOR_")}
        configcode, stdout, stderr, failure = raw.BASE.invoke(argv, parser_env)
        (output / "configtest.stdout").write_bytes(stdout)
        (output / "configtest.stderr").write_bytes(stderr)
        if configcode != 0 or failure:
            raise ValueError("actual native configuration did not load")
        with (output / "startup.stdout").open("xb") as stdout, (output / "startup.stderr").open("xb") as stderr:
            argv.remove("-t")
            process = subprocess.Popen(argv, env=environment, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr,
                                       pass_fds=tuple(descriptors))
            roles = raw.HOST.observe_roles(process, local_args.run_id, port, output, handles)
            capture.capture(roles)
            labels = ["selected", "followup"] + (["wrong-transaction"] if row["fault"] or row.get("invalid_return") else [])
            for label in labels:
                selected = label == "selected"
                body = row["request"] if selected else b"marker=NGXI12_REQ&neighbor=1"
                path = "/no-crs/input-fault/" + row["fault"] if row["fault"] and label != "followup" else "/ngxi12/" + label
                method = "GET" if selected and row["response_file"] else "POST"
                if method == "GET" and not row.get("get_entity"):
                    body = b""
                headers = [("Host", "localhost"), ("Content-Length", str(len(body))), ("Connection", "close")]
                content_type = row["request_type"] if selected else "application/x-www-form-urlencoded"
                if content_type:
                    headers.append(("Content-Type", content_type))
                if selected:
                    headers.extend(row["extra_headers"])
                if row["fault"] or row.get("budget_phase") or row.get("invalid_return"):
                    headers.append(("X-I12-Transaction", ("a" if selected else "b") * 32))
                malformed = row.get("malformed") if selected else None
                if malformed == "invalid_content_length":
                    headers = [(key, "abc" if key == "Content-Length" else value) for key, value in headers]
                elif malformed == "conflicting_content_length":
                    headers.append(("Content-Length", "1"))
                elif malformed == "duplicate_transfer_encoding":
                    headers.extend([("Transfer-Encoding", "chunked"), ("Transfer-Encoding", "chunked")])
                elif malformed == "content_length_overflow":
                    headers = [(key, "9223372036854775808" if key == "Content-Length" else value) for key, value in headers]
                wire = (method + " " + path + " HTTP/1.1\r\n" + "".join(key + ": " + value + "\r\n" for key, value in headers) + "\r\n").encode() + body
                request = output / (label + "-request.bin")
                request.write_bytes(wire)
                # The outer driver is RTK-proxied. Wait the actual Python
                # client directly, as the original NGINX capture does: an RTK
                # child wrapper would translate a signal into exit128+signal.
                clientargv = [sys.executable, str(Path(__file__).with_name("wire_client.py")), "--port", str(port),
                              "--request", str(request), "--output", str(output / label), "--pieces", str(row["writes"] if selected else 1)]
                started = time.monotonic_ns()
                with subprocess.Popen(clientargv, env=client_environment(parser_env),
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE) as client:
                    try:
                        client_stdout, client_stderr = client.communicate(timeout=20)
                    except subprocess.TimeoutExpired:
                        client.kill()
                        client_stdout, client_stderr = client.communicate()
                        errors.append(label + " actual client timed out and was reaped")
                waited = time.monotonic_ns()
                (output / (label + "-client.stdout")).write_bytes(client_stdout)
                (output / (label + "-client.stderr")).write_bytes(client_stderr)
                item = {"label": label, "argv": clientargv, "exit_code": client.returncode,
                        "pid": client.pid, "direct_child_wait": True,
                        "signal": -client.returncode if client.returncode < 0 else None,
                        "started_monotonic_ns": started, "waited_monotonic_ns": waited}
                observation = output / label / "client-observation.json"
                if observation.exists():
                    item["observation"] = json.loads(observation.read_text())
                clients.append(item)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        errors.append(type(exc).__name__ + ": " + str(exc))
    finally:
        cleanup = raw.HOST.stop_owned_master(process, roles, port, local_args.run_id, handles)
        master_result = process.returncode if process is not None else None
        for descriptor in descriptors:
            if descriptor != capture.descriptor:
                os.fsync(descriptor)
                os.close(descriptor)
        capture.close()
        backend.shutdown()
        backend.server_close()
        thread.join(2)
    if not cleanup.get("verified") or thread.is_alive():
        errors.append("owned cleanup incomplete")
    (output / "backend.json").write_text(json.dumps(backend.observations, indent=2) + "\n")
    receipt = {"selected_id": "I12::nginx-native::" + row["case_id"], "run_id": local_args.run_id,
               "parent_sha": args.parent_sha, "framework_sha": args.framework_sha, "mrts_sha": args.mrts_sha,
               "roles": roles, "configtest_exit": configcode, "cleanup": cleanup,
               "master_wait_result": master_result, "master_signal": -master_result if master_result is not None and master_result < 0 else None,
               "clients": clients, "backend": backend.observations, "errors": errors,
               "full_lifecycle_qualified": False, "scope": "Physical observations only; independent Root reconciliation required",
               "raw_artifacts_sha256": {str(p.relative_to(output)): digest(p) for p in output.rglob("*") if p.is_file() and not p.is_symlink()}}
    (output / "full-observation-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    return {"case_id": row["case_id"], "output": str(output), "errors": errors, "clients": [
        {key: x.get(key) for key in ("label", "exit_code", "signal")} for x in clients]}


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for name in ("source", "nginx-binary", "module", "output-root", "library-dir", "framework-root", "worker-self-map-library", "input-fault-library", "budget-fault-library", "invalid-return-library"):
        parser.add_argument("--" + name, type=Path, required=True)
    for name in ("parent-sha", "framework-sha", "mrts-sha"):
        parser.add_argument("--" + name, required=True)
    parser.add_argument("--run-prefix", required=True)
    parser.add_argument("--case", action="append", default=[])
    args = parser.parse_args()
    args.worker_self_map_library = str(args.worker_self_map_library)
    args.nginx_binary, args.module = args.nginx_binary.resolve(), args.module.resolve()
    raw = load("i12_real_nginx_raw", args.source / "ci/runtime/lifecycle/run-nginx-raw-h1.py")
    maps = load("i12_actual_worker_maps", args.source / "ci/runtime/lifecycle/nginx-worker-self-maps.py")
    selected = [row for row in cases() if not args.case or row["case_id"] in args.case]
    if args.case and len(selected) != len(set(args.case)):
        raise ValueError("unknown selected fixture")
    results = []
    for row in selected:
        result = run_one(args, row, raw, maps)
        results.append(result)
        print(json.dumps(result), flush=True)
    (args.output_root / "suite-observations.json").write_text(json.dumps(results, indent=2) + "\n")
    return 1 if any(row["errors"] for row in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
