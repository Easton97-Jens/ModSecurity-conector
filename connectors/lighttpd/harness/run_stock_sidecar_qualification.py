#!/usr/bin/env python3
"""Bounded Stock-sidecar lifecycle qualification; never a catalog-B award.

The existing real-backend campaign remains the independent boundary evidence
layer. This entry point retains its operator attestation and artifact checks.
Four accepted partial-body client sockets overlap; this does not establish
concurrent Common engine execution. Completion is released serially because
the production receipt publisher deliberately cannot overwrite one receipt.
"""
from __future__ import annotations

from contextlib import ExitStack
from dataclasses import dataclass, replace
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import socket
import stat
import subprocess
import sys
import time
import resource

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from connectors.lighttpd.harness import run_stock_sidecar_real_backend as base

MAX_LOG_BYTES = 8 * 1024 * 1024
MAX_REQUESTS = 32
MAX_START_SECONDS = 60
MAX_PROCESS_FILE_BYTES = 1024 * 1024
CASES = {case.name: case for case in base.REAL_BACKEND_CASES}
RECEIPT_COMMON_KEYS = frozenset(("schema_version", "connector", "connector_profile", "integration_mode",
    "transport_version", "phase_observation", "observed_phase_sequence", "transaction_id_sha256",
    "receipt_binding_sha256", "request_body_bytes", "response_body_bytes", "engine_decision",
    "original_http_status", "response_committed", "cleanup_status", "cleanup_complete",
    "payloads_persisted", "opaque_handles_persisted"))
ALLOW_RECEIPT_KEYS = RECEIPT_COMMON_KEYS | {"actual_host_action", "visible_http_status"}
NON_ALLOW_RECEIPT_KEYS = RECEIPT_COMMON_KEYS | {"receipt_kind", "last_completed_phase",
    "request_body_truncated", "response_body_truncated", "contract_action", "error_class", "mode",
    "response_headers_processed", "response_headers_sent", "response_body_finished",
    "created_at_ms", "completed_at_ms", "cleanup_at_ms"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def bound_child_files() -> None:
    """The single-threaded launcher caps each child's file before exec."""
    resource.setrlimit(resource.RLIMIT_FSIZE, (MAX_PROCESS_FILE_BYTES, MAX_PROCESS_FILE_BYTES))


def bounded_read(path: Path, maximum: int, *, absent: bool = False) -> tuple[bytes, tuple[int, int]]:
    """Pin a private, single-link file and reject mutation during the read."""
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    except FileNotFoundError:
        if absent:
            return b"", (0, 0)
        raise RuntimeError("qualification evidence is missing") from None
    try:
        info = os.fstat(fd)
        require(stat.S_ISREG(info.st_mode) and info.st_uid == os.getuid() and
                not info.st_mode & 0o077 and info.st_nlink == 1 and info.st_size <= maximum,
                "qualification evidence is not bounded and owner-private")
        data = bytearray()
        while len(data) <= maximum:
            chunk = os.read(fd, min(65536, maximum + 1 - len(data)))
            if not chunk:
                break
            data.extend(chunk)
        after = os.fstat(fd)
        require(len(data) <= maximum and len(data) == info.st_size and
                (info.st_size, info.st_mtime_ns, info.st_ctime_ns) ==
                (after.st_size, after.st_mtime_ns, after.st_ctime_ns),
                "qualification evidence changed during its bounded read")
        require(path.lstat().st_ino == info.st_ino and path.lstat().st_dev == info.st_dev,
                "qualification evidence path was replaced")
        return bytes(data), (info.st_dev, info.st_ino)
    finally:
        os.close(fd)


def decode(data: bytes) -> dict[str, object]:
    value = json.loads(data, object_pairs_hook=base._reject_duplicate_json_keys,
                       parse_constant=base._reject_json_constant)
    require(isinstance(value, dict), "qualification JSON is not an object")
    return value


@dataclass(frozen=True)
class Identity:
    pid: int
    start_ticks: int
    executable_sha256: str


def identity(pid: int, binary_digest: str) -> Identity:
    fields = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()
    require(fields[0] not in ("Z", "X"), "sidecar is not alive")
    actual = base.file_sha256(Path(f"/proc/{pid}/exe").resolve(strict=True), "sidecar process executable")
    require(actual == binary_digest, "sidecar executable pin drifted")
    return Identity(pid, int(fields[19]), actual)


def resources(pin: Identity, port: int) -> dict[str, object]:
    require(identity(pin.pid, pin.executable_sha256) == pin, "sidecar process identity drifted")
    root = Path(f"/proc/{pin.pid}")
    status = root.joinpath("status").read_text()
    rss = next(int(line.split()[1]) for line in status.splitlines() if line.startswith("VmRSS:"))
    descriptors = list(root.joinpath("fd").iterdir())
    owned = set()
    for item in descriptors:
        try:
            target = os.readlink(item)
        except FileNotFoundError:
            continue
        if target.startswith("socket:["):
            owned.add(target[8:-1])
    accepted = []
    listeners = 0
    for line in root.joinpath("net/tcp").read_text().splitlines()[1:]:
        columns = line.split()
        if columns[9] not in owned:
            continue
        address, local_port = columns[1].split(":")
        if int(local_port, 16) != port:
            continue
        require(address == "0100007F", "sidecar socket escaped loopback")
        if columns[3] == "0A":
            listeners += 1
        if columns[3] == "01":
            accepted.append(int(columns[2].split(":")[1], 16))
    require(rss > 0 and 0 < len(descriptors) < 4096 and listeners == 1,
            "invalid sidecar resource or listener observation")
    return {"rss_kib": rss, "fd_count": len(descriptors), "listeners": listeners,
            "accepted_peer_ports": sorted(accepted)}


def verify_overlap(sample: dict[str, object], clients: list[socket.socket]) -> None:
    peers = [client.getsockname()[1] for client in clients]
    require(len(peers) == 4 and len(set(peers)) == 4 and
            set(peers) <= set(sample["accepted_peer_ports"]),
            "four partial-body clients did not actually overlap in the sidecar")


class Evidence:
    """Validate every completion against one append-only Common chain."""
    def __init__(self, receipt: Path, events: Path, backend: Path, binding: str):
        self.receipt, self.events, self.backend, self.binding = receipt, events, backend, binding
        self.event_prefix = b""
        self.event_inode = None
        self.backend_prefix = b""
        self.backend_inode = None
        self.transaction_ids: set[str] = set()
        self.requests = 0

    def ready(self) -> None:
        require(not self.receipt.exists() and not self.receipt.is_symlink(), "stale sidecar receipt")
        require(self.requests < MAX_REQUESTS, "qualification request bound exceeded")
        for path, prefix, inode in ((self.events, self.event_prefix, self.event_inode),
                                    (self.backend, self.backend_prefix, self.backend_inode)):
            data, _ = self._append(path, prefix, inode)
            require(data == prefix, "unattributed event or backend receipt before probe")

    def _append(self, path: Path, prefix: bytes, inode: tuple[int, int] | None) -> tuple[bytes, tuple[int, int]]:
        data, current = bounded_read(path, MAX_LOG_BYTES, absent=True)
        require(data.startswith(prefix) and (inode is None or current == inode),
                "qualification log was truncated or replaced")
        require(not data or data.endswith(b"\n"), "qualification log contains a partial record")
        return data, current

    def finish(self, case: base.RealBackendCase, token: str, *, abort: bool = False) -> dict[str, object]:
        deadline = time.monotonic() + 3
        while not self.receipt.exists() and time.monotonic() < deadline:
            time.sleep(.01)
        data, inode = bounded_read(self.receipt, base._MAX_RECEIPT_BYTES)
        receipt = decode(data)
        expected_keys = ALLOW_RECEIPT_KEYS if receipt.get("schema_version") == 1 else NON_ALLOW_RECEIPT_KEYS
        require(receipt.keys() == expected_keys, "receipt contains missing or unexpected fields")
        for key in ("request_body_truncated", "response_body_truncated"):
            if key in receipt:
                require(type(receipt[key]) is bool, "receipt truncation state is not boolean")
        base._validate_receipt_identity(receipt, self.binding, case)
        base._validate_receipt_body_and_decision(receipt, case)
        base._validate_receipt_schema(receipt, case)
        transaction = receipt["transaction_id_sha256"]
        require(transaction == hashlib.sha256(token.encode("ascii")).hexdigest(),
                "receipt is not correlated to the submitted request")
        require(transaction not in self.transaction_ids, "duplicate or stale transaction receipt")
        event_data, event_inode = self._append(self.events, self.event_prefix, self.event_inode)
        records = []
        for line in event_data.splitlines():
            require(line and len(line) <= base._MAX_RECEIPT_BYTES, "invalid Common event line")
            record = decode(line)
            base._validate_event_schema(record)
            records.append(record)
        base.verify_event_chain(records)
        delta = records[len(self.event_prefix.splitlines()):]
        base._event_payload_free(event_data.decode(), case)
        if abort:
            require(len(delta) == 2, "client abort requires exactly two Common events")
            engine, host = delta
            require(engine["message_id"] == "MSCONN_EVENT_CLIENT_CANCEL" and
                    engine["connector"] == "lighttpd" and
                    engine["integration_mode"] == "stock-lighttpd-sidecar" and
                    engine["phase"] == "request_body" and host["phase"] == "request_body" and
                    engine["body_bytes_seen"] == len(base.request_body(case.request)) and
                    engine["eos_seen"] is False and engine["response_committed"] is False and
                    engine["cancelled"] is True and engine["client_disconnected"] is True and
                    engine["actual_action"] == "abort_connection" and
                    engine["transport_result"] == "" and engine["visible_http_status"] == 0 and
                    host["message_id"] == "MSCONN_EVENT_CONNECTOR_ERROR" and
                    host["connector"] == "lighttpd" and
                    host["integration_mode"] == "stock-lighttpd-sidecar" and
                    host["response_committed"] is False and
                    host["actual_action"] == "deny" and host["visible_http_status"] == 502 and
                    host["transport_result"] == "http_status",
                    "client abort engine/host outcome is not exact")
            base._validate_event_pair_correlation(delta, engine, host, receipt)
        elif case.expected_host_action_event is None:
            require(not delta, "Allow emitted unexpected Common events")
        else:
            event = base._host_action_event_from_records(delta, case, receipt)
            require(event is not None, "missing or stale engine/host event pair")
        deadline = time.monotonic() + 3
        while True:
            backend_data, backend_inode = self._append(self.backend, self.backend_prefix, self.backend_inode)
            if backend_data != self.backend_prefix or not case.expected_backend_requests:
                break
            require(time.monotonic() < deadline, "backend receipt missing")
            time.sleep(.01)
        new_backend = backend_data[len(self.backend_prefix):].splitlines()
        require(len(new_backend) == case.expected_backend_requests and
                all(line == token.encode() for line in new_backend),
                "backend receipt missing, extra, or uncorrelated")
        consumed_data, consumed_inode = bounded_read(self.receipt, base._MAX_RECEIPT_BYTES)
        require(consumed_inode == inode and consumed_data == data,
                "receipt changed before strict consumption")
        self.receipt.unlink()
        self.event_prefix, self.event_inode = event_data, event_inode if event_data else None
        self.backend_prefix, self.backend_inode = backend_data, backend_inode if backend_data else None
        self.transaction_ids.add(transaction)
        self.requests += 1
        return {"case": case.name, "transaction_id_sha256": transaction,
                "receipt_sha256": hashlib.sha256(data).hexdigest(), "events_added": len(delta),
                "backend_requests": len(new_backend), "cleanup_complete": True}


def request(case: base.RealBackendCase, token: str, keepalive: bool = False) -> bytes:
    head, body = case.request.split(b"\r\n\r\n", 1)
    head = head.replace(b"Connection: close", b"Connection: keep-alive" if keepalive else b"Connection: close")
    return head + b"\r\nX-Request-ID: " + token.encode() + b"\r\n\r\n" + body


def response(client: socket.socket, case: base.RealBackendCase, keepalive: bool = False) -> None:
    deadline = time.monotonic() + 3

    def receive(size: int) -> bytes:
        remaining = deadline - time.monotonic()
        require(remaining > 0, "absolute client response deadline exceeded")
        client.settimeout(remaining)
        return client.recv(size)

    head = bytearray()
    while not head.endswith(b"\r\n\r\n") and len(head) <= 65536:
        piece = receive(1)
        require(bool(piece), "incomplete client response headers")
        head.extend(piece)
    require(len(head) <= 65536, "oversized client response headers")
    lines = bytes(head).split(b"\r\n")
    status = re.fullmatch(rb"HTTP/1\.1 ([0-9]{3}) ([\x20-\x7e]+)", lines[0])
    require(status is not None and status[1] == str(case.expected_status).encode(), "unexpected client status")
    fields: dict[bytes, list[bytes]] = {}
    require(len(lines[1:-2]) <= 64, "too many client response headers")
    for line in lines[1:-2]:
        name, colon, raw_value = line.partition(b":")
        require(len(line) <= 8192 and colon == b":" and
                re.fullmatch(rb"[!#$%&'*+.^_`|~0-9A-Za-z-]+", name) is not None and
                raw_value.startswith(b" ") and
                (not raw_value[1:] or raw_value[1:] == raw_value[1:].strip(b" ")) and
                all(32 <= byte <= 126 for byte in raw_value),
                "invalid client response header grammar")
        fields.setdefault(name.lower(), []).append(raw_value[1:])
    require(fields.get(b"content-length") == [str(len(case.expected_body)).encode()] and
            b"transfer-encoding" not in fields,
            "ambiguous client framing")
    require(fields.get(b"connection") == [b"keep-alive" if keepalive else b"close"],
            "unexpected reuse contract")
    body = bytearray()
    while len(body) < len(case.expected_body):
        piece = receive(len(case.expected_body) - len(body))
        require(bool(piece), "incomplete client response body")
        body.extend(piece)
    require(bytes(body) == case.expected_body, "unexpected client response body")
    if not keepalive:
        require(receive(1) == b"", "client connection did not end cleanly")


def controlled_stop(process: subprocess.Popen[bytes], port: int) -> None:
    require(process.poll() is None, "process exited before controlled stop")
    process.terminate()
    try:
        result = process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)
        raise RuntimeError("controlled stop required a hard kill") from None
    require(result in (0, -15), "unexpected controlled stop status")
    require(not Path(f"/proc/{process.pid}").exists(), "process was not reaped")
    with socket.socket() as probe:
        probe.settimeout(.2)
        require(probe.connect_ex(("127.0.0.1", port)) != 0, "listener survived cleanup")


def validate_starts(starts: list[dict[str, object]]) -> None:
    require(len(starts) == 3, "qualification requires exactly three starts")
    identities = {(item["identity"]["pid"], item["identity"]["start_ticks"]) for item in starts}
    require(len(identities) == 3, "three sidecar starts were not distinct")
    backend_identities = {(item["backend_identity"]["pid"], item["backend_identity"]["start_ticks"]) for item in starts}
    require(len(backend_identities) == 3, "three complete backend generations were not distinct")
    require(len({item["backend_port"] for item in starts}) == 3 and
            len({item["sidecar_port"] for item in starts}) == 3,
            "three generations did not use distinct listener ports")
    require(sum(len(item["probes"]) for item in starts) <= MAX_REQUESTS,
            "qualification request bound exceeded")
    for item in starts:
        require(item["controlled_stop_reaped"] is True and item["backend_controlled_stop_reaped"] is True and
                item["backend_final_log_verified"] is True and 0 < item["elapsed_seconds"] <= MAX_START_SECONDS,
                "start cleanup or duration failed")
        require({probe["case"] for probe in item["probes"]} >= {"allow_full", "p1_deny", "p2_deny"},
                "start lacks Allow/P1/P2")
        before, after = item["resources_before"], item["resources_after"]
        require(not after["accepted_peer_ports"] and after["fd_count"] <= before["fd_count"] and
                after["rss_kib"] <= before["rss_kib"] + 8192,
                "resource stabilization failed")
    require(starts[0].get("overlap_verified") is True and starts[0].get("keepalive_verified") is True and
            starts[0].get("abort_recovery_verified") is True, "start1 lifecycle evidence missing")


def unused_port(used: set[int]) -> int:
    for _ in range(20):
        port = base.free_port()
        if port not in used:
            used.add(port)
            return port
    raise RuntimeError("could not allocate a distinct generation listener port")


def verify_final_backend_log(path: Path, evidence: dict[str, object]) -> None:
    data, inode = bounded_read(path, MAX_PROCESS_FILE_BYTES)
    require(inode == (evidence["device"], evidence["inode"]) and len(data) == evidence["bytes"] and
            hashlib.sha256(data).hexdigest() == evidence["sha256"],
            "final backend log differs from the consumed ledger prefix")


def run_start(root: Path, binary: Path, digest: str, backend_port: int, backend_log: Path,
              backend_pin: Identity, used_ports: set[int]) -> dict[str, object]:
    started = time.monotonic()
    root.mkdir(mode=0o700)
    combined = replace(CASES["allow_full"], rules=CASES["p1_deny"].rules + CASES["p2_deny"].rules)
    _, events, config = base.write_case_runtime_inputs(root, combined)
    receipt = root / "receipt.json"
    binding = secrets.token_hex(32)
    port = unused_port(used_ports)
    base.verify_artifact_digest(binary, "Stock sidecar", digest)
    log = root / "sidecar.log"
    with log.open("xb") as output:
        log.chmod(0o600)
        process = subprocess.Popen([str(binary), "--config", str(config), "--listen", f"127.0.0.1:{port}",
                                    "--upstream", f"127.0.0.1:{backend_port}", "--timeout-ms", "3000"],
                                   stdout=output, stderr=output,
                                   preexec_fn=bound_child_files,
                                   env={**os.environ, "STOCK_SIDECAR_RECEIPT_PATH": str(receipt),
                                        "STOCK_SIDECAR_RECEIPT_BINDING": binding})
        probes = []
        result: dict[str, object] = {}
        failure = None
        try:
            base.wait_ready(port, process, "Stock qualification sidecar")
            pin = identity(process.pid, digest)
            baseline_deadline = time.monotonic() + 1
            before = resources(pin, port)
            while before["accepted_peer_ports"]:
                require(time.monotonic() < baseline_deadline, "readiness connection did not close")
                time.sleep(.01)
                before = resources(pin, port)
            ledger = Evidence(receipt, events, backend_log, binding)
            ledger.backend_prefix, ledger.backend_inode = bounded_read(backend_log, MAX_LOG_BYTES, absent=True)
            if not ledger.backend_prefix:
                ledger.backend_inode = None

            def finish(case: base.RealBackendCase, client: socket.socket, token: str, *, reuse: bool = False, abort: bool = False):
                response(client, case, reuse)
                probes.append(ledger.finish(case, token, abort=abort))
                require(identity(process.pid, digest) == pin, "process changed during probe")
                require(identity(backend_pin.pid, backend_pin.executable_sha256) == backend_pin,
                        "backend process changed during probe")
                require(time.monotonic() - started < MAX_START_SECONDS, "start deadline exceeded")

            for name in ("allow_full", "p1_deny", "p2_deny"):
                ledger.ready()
                case = CASES[name]
                token = secrets.token_hex(16)
                with socket.create_connection(("127.0.0.1", port), timeout=3) as client:
                    client.sendall(request(case, token))
                    finish(case, client, token)
            peak = before
            if root.name == "start-1":
                with socket.create_connection(("127.0.0.1", port), timeout=3) as client:
                    socket_pin = client.getsockname(), client.getpeername(), client.fileno()
                    for name in ("allow_full", "p1_deny", "allow_full"):
                        ledger.ready()
                        case = CASES[name]
                        token = secrets.token_hex(16)
                        client.sendall(request(case, token, True))
                        finish(case, client, token, reuse=True)
                        require(socket_pin == (client.getsockname(), client.getpeername(), client.fileno()),
                                "keepalive socket identity changed")
                result["keepalive_verified"] = True
                marker = b"stock-abort-marker"
                abort_case = replace(CASES["p1_deny"], name="client_abort", request=base.http_request("POST", "/health.txt", marker),
                                     expected_status=502, expected_phase_sequence=("P1",), expected_engine_decision="client_cancel",
                                     expected_contract_action="abort_connection", expected_error_class="client_cancel")
                ledger.ready()
                token = secrets.token_hex(16)
                with socket.create_connection(("127.0.0.1", port), timeout=3) as client:
                    # A complete header/P1 followed by clean EOF during P2.
                    client.sendall(request(abort_case, token).replace(
                        f"Content-Length: {len(marker)}\r\n".encode(),
                        f"Content-Length: {len(marker) + 1}\r\n".encode()))
                    client.shutdown(socket.SHUT_WR)
                    finish(abort_case, client, token, abort=True)
                ledger.ready()
                token = secrets.token_hex(16)
                with socket.create_connection(("127.0.0.1", port), timeout=3) as client:
                    client.sendall(request(CASES["allow_full"], token))
                    finish(CASES["allow_full"], client, token)
                result["abort_recovery_verified"] = True
                held = replace(CASES["allow_full"], request=base.http_request("GET", "/health.txt", b"xy"))
                with ExitStack() as stack:
                    clients = [stack.enter_context(socket.create_connection(("127.0.0.1", port), timeout=3)) for _ in range(4)]
                    tokens = [secrets.token_hex(16) for _ in clients]
                    ledger.ready()
                    for client, token in zip(clients, tokens):
                        client.sendall(request(held, token)[:-1])
                    deadline = time.monotonic() + 1
                    while True:
                        peak = resources(pin, port)
                        if set(client.getsockname()[1] for client in clients) <= set(peak["accepted_peer_ports"]):
                            break
                        require(time.monotonic() < deadline, "sidecar never accepted four overlapping clients")
                        time.sleep(.01)
                    verify_overlap(peak, clients)
                    require(peak["fd_count"] >= before["fd_count"] + 4,
                            "overlap lacks four additional process descriptors")
                    require(not receipt.exists(), "partial-body barrier completed prematurely")
                    for client, token in zip(clients, tokens):
                        ledger.ready()
                        client.sendall(b"y")
                        finish(held, client, token)
                result["overlap_verified"] = True
                result["overlap_scope"] = "four simultaneously accepted partial client sockets"
            deadline = time.monotonic() + 2
            while True:
                after = resources(pin, port)
                if not after["accepted_peer_ports"] and after["fd_count"] <= before["fd_count"]:
                    break
                require(time.monotonic() < deadline, "sidecar resources failed to stabilize")
                time.sleep(.01)
            bounded_read(log, MAX_LOG_BYTES)
            ledger.ready()
            result.update(identity=pin.__dict__, probes=probes, resources_before=before,
                          resources_peak=peak, resources_after=after)
        except BaseException as error:
            failure = error
            raise
        finally:
            try:
                controlled_stop(process, port)
            except BaseException as cleanup_error:
                if failure is not None:
                    raise BaseExceptionGroup("qualification and cleanup failed", [failure, cleanup_error]) from None
                raise
        ledger.ready()
        require(ledger.backend_inode is not None, "backend ledger has no pinned receipt log")
        result.update(controlled_stop_reaped=True, elapsed_seconds=time.monotonic() - started,
                      sidecar_port=port, backend_log_evidence={"bytes": len(ledger.backend_prefix),
                      "sha256": hashlib.sha256(ledger.backend_prefix).hexdigest(),
                      "device": ledger.backend_inode[0], "inode": ledger.backend_inode[1]})
        return result


def preflight() -> dict[str, object]:
    root = base.required("STOCK_SIDECAR_RUNTIME_ROOT")
    base.private_directory(root, "Stock qualification root")
    require(not any(character in str(root) for character in ('"', '\\', '\r', '\n')),
            "runtime root cannot be encoded in the host configuration")
    binary = base.required("MSCONNECTOR_STOCK_SIDECAR_BINARY")
    host = base.required("STOCK_LIGHTTPD_BIN")
    modules = base.required("STOCK_LIGHTTPD_MODULE_DIR")
    host_digest = base.file_sha256(host, "Stock lighttpd")
    contract = base.verify_stock_host_provenance(host, modules, host_digest)
    revision, tree = base.repository_revision()
    digest = base.file_sha256(binary, "Stock sidecar")
    manifest = base.verify_sidecar_build_manifest(binary, digest, revision, tree)
    attestation = base.required("STOCK_SIDECAR_ARTIFACT_ATTESTATION")
    attestation_digest = base.verify_stock_artifact_attestation(attestation, contract, manifest, revision, tree,
                                                             host, binary, root)
    base.verify_stock_staticfile_linkage(host)
    require(base.host_version(host) == contract["LIGHTTPD_VERSION"], "host version pin mismatch")
    campaign = root / "qualification"
    require(not campaign.exists() and not campaign.is_symlink(), "qualification campaign path already exists")
    return {"root": root, "host": host, "modules": modules, "binary": binary,
            "host_digest": host_digest, "digest": digest, "contract": contract,
            "attestation": attestation, "attestation_digest": attestation_digest}


def run_generation(inputs: dict[str, object], campaign: Path, number: int, used_ports: set[int]) -> dict[str, object]:
    started = time.monotonic()
    host, modules, binary = inputs["host"], inputs["modules"], inputs["binary"]
    host_digest, digest, contract = inputs["host_digest"], inputs["digest"], inputs["contract"]
    campaign.mkdir(mode=0o700)
    docs = campaign / "htdocs"
    docs.mkdir(mode=0o700)
    docs.joinpath("health.txt").write_bytes(b"stock-backend-health")
    uploads = campaign / "uploads"
    uploads.mkdir(mode=0o700)
    config, access = campaign / "lighttpd.conf", campaign / "backend.log"
    port = unused_port(used_ports)
    config.write_text('\n'.join(('server.modules = ( "mod_accesslog", "mod_staticfile" )',
                                f'server.document-root = "{docs}"', 'server.bind = "127.0.0.1"',
                                f'server.port = {port}', f'accesslog.filename = "{access}"',
                                'accesslog.format = "%{X-Request-ID}i"',
                                f'server.upload-dirs = ( "{uploads}" )', '')))
    config.chmod(0o600)
    # lighttpd creates its access log under the process umask.
    fd = os.open(access, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    os.close(fd)
    base.verify_stock_launch_artifacts(host, modules, contract)
    base.verify_artifact_digest(inputs["attestation"], "Stock attestation", inputs["attestation_digest"])
    with (campaign / "backend-stderr.log").open("xb") as output:
        os.chmod(output.name, 0o600)
        backend = subprocess.Popen([str(host), "-D", "-m", str(modules), "-f", str(config)],
                                   stdout=output, stderr=output, preexec_fn=bound_child_files)
        failure = None
        try:
            base.wait_ready(port, backend, "unchanged Stock backend")
            backend_pin = identity(backend.pid, host_digest)
            backend_before = resources(backend_pin, port)
            result = run_start(campaign / f"start-{number}", binary, digest, port, access, backend_pin, used_ports)
            backend_after = resources(backend_pin, port)
        except BaseException as error:
            failure = error
            raise
        finally:
            try:
                controlled_stop(backend, port)
            except BaseException as cleanup_error:
                if failure is not None:
                    raise BaseExceptionGroup("generation and backend cleanup failed", [failure, cleanup_error]) from None
                raise
    verify_final_backend_log(access, result["backend_log_evidence"])
    result.update(backend_identity=backend_pin.__dict__, backend_port=port,
                  backend_resources_before=backend_before, backend_resources_after=backend_after,
                  backend_controlled_stop_reaped=True, backend_final_log_verified=True,
                  elapsed_seconds=time.monotonic() - started)
    return result


def run_campaign(inputs: dict[str, object]) -> None:
    campaign = inputs["root"] / "qualification"
    campaign.mkdir(mode=0o700)
    used_ports: set[int] = set()
    starts = [run_generation(inputs, campaign / f"generation-{number}", number, used_ports)
              for number in range(1, 4)]
    validate_starts(starts)
    total_log_bytes = 0
    for number in range(1, 4):
        generation = campaign / f"generation-{number}"
        for path in (generation / "backend.log", generation / "backend-stderr.log",
                     generation / f"start-{number}" / "events.jsonl", generation / f"start-{number}" / "sidecar.log"):
            data, _ = bounded_read(path, MAX_PROCESS_FILE_BYTES, absent=path.name == "events.jsonl")
            total_log_bytes += len(data)
    require(total_log_bytes <= MAX_LOG_BYTES, "campaign aggregate log bound exceeded")
    summary = {"schema_version": 1, "profile": "lighttpd-stock-sidecar", "catalog_b": False,
               "operator_attestation_sha256": inputs["attestation_digest"], "sidecar_binary_sha256": inputs["digest"],
               "stock_binary_sha256": inputs["host_digest"], "starts": starts,
               "prerequisites": {"G2": "passed", "G5": "passed", "G6": "passed"},
               "remaining": {"G1": "blocked: full provenance gate", "G4": "blocked: separate imported boundary campaign",
                             "G8": "blocked: external regression campaign"}, "cleanup": "passed"}
    base.publish_verified_receipt(campaign / "qualification.json", summary)
    print("lighttpd_stock_qualification: bounded G2/G5/G6 prerequisites PASS; catalog B remains blocked")


def main(argv: list[str] | None = None) -> int:
    if (sys.argv[1:] if argv is None else argv):
        print("lighttpd_stock_qualification: usage error: configure prerequisites through environment variables", file=sys.stderr)
        return 2
    try:
        inputs = preflight()
    except (OSError, RuntimeError, ValueError, subprocess.TimeoutExpired) as error:
        print(f"lighttpd_stock_qualification: BLOCKED: {error}", file=sys.stderr)
        return 77
    except Exception as error:
        print(f"lighttpd_stock_qualification: FAIL: unexpected preflight error: {error}", file=sys.stderr)
        return 1
    try:
        run_campaign(inputs)
    except Exception as error:
        print(f"lighttpd_stock_qualification: FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
