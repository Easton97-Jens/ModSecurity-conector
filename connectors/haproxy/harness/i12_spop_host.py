#!/usr/bin/env python3
"""Request-only HAProxy I12 capture, executed inside an admitted private host.

Inputs: /mnt/artifacts/{haproxy,haproxy-spop}, this script and i12_spop_wire.py
under /mnt/fixtures. All mutable output stays under /task. The independent TCP
observer preserves every SPOP byte and decodes complete frames. An explicitly
selected companion can complete held native transactions; these independent
request-profile runs never qualify the companion profile.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import signal
import socket
import struct
import subprocess
import threading
import time

from i12_spop_wire import decode_frame, MAX_FRAME

ROOT = Path("/task")
LOCK = threading.Lock()


def record(name, value):
    with LOCK, (ROOT / name).open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(value, sort_keys=True) + "\n")


def case_identity(selected):
    # These supplemental probes do not carry a reviewed original Oracle
    # contract. In particular, an incoming legacy case_id must never invent
    # original membership or transfer a diagnostic run to a corrected ID.
    return {"diagnostic_id": "DIAG::haproxy-spop-request::" + selected["case"],
            "original_id": None, "original_obligation_eligible": False}


def snapshot(process, name):
    proc = Path("/proc") / str(process.pid)
    maps = proc.joinpath("maps").read_text()
    (ROOT / (name + ".maps")).write_text(maps)
    files = set()
    for line in maps.splitlines():
        fields = line.split(None, 5)
        if len(fields) == 6 and fields[5].startswith("/") and "libmodsecurity" in fields[5]:
            files.add(fields[5])
    identities = []
    for name_on_disk in sorted(files):
        file = Path(name_on_disk)
        identities.append({"path": name_on_disk, "sha256": hashlib.sha256(file.read_bytes()).hexdigest()})
    record("process-identity.jsonl", {"name": name, "pid": process.pid,
           "wall_ns": time.time_ns(), "native_libraries": identities,
           "exe": os.readlink(proc / "exe"),
           "fds": {file.name: os.readlink(file) for file in proc.joinpath("fd").iterdir()}})


def evaluate(selected):
    """Compare independent observations; a successful launcher is insufficient."""
    case = selected["case"]
    allowed = case in ("empty-allow", "post-allow")
    policy_deny = case in ("p1-deny", "p2-deny")
    technical_loss = case == "technical-agent-loss"
    expected = {"ack_status": None if technical_loss else 400 if case == "corrupt-notify" else 200 if allowed else 403 if policy_deny else 503,
                "ack_blocked": None if technical_loss else not allowed,
                "backend_requests": 1 if allowed else 0,
                "client_status": 200 if allowed else 503,
                "fully_inspected_http2": False}
    frames = [json.loads(line) for line in (ROOT / "frames.jsonl").read_text().splitlines()] if (ROOT / "frames.jsonl").exists() else []
    acks = [{action["name"]: action["value"] for action in frame["decoded"].get("actions", [])}
            for frame in frames if frame["decoded"].get("kind") == 103]
    clients = [json.loads(line) for line in (ROOT / "client.jsonl").read_text().splitlines()]
    observed = {"ack_status": acks[-1].get("status") if acks else None,
                "ack_blocked": acks[-1].get("blocked") if acks else None,
                "backend_requests": len((ROOT / "backend.jsonl").read_text().splitlines()) if (ROOT / "backend.jsonl").exists() else 0,
                "client_status": None if clients[-1]["http2"] else int(clients[-1]["status_line"].split()[1]),
                "fully_inspected_http2": False}
    mismatches = [key for key in ("ack_status", "ack_blocked", "backend_requests") if observed[key] != expected[key]]
    if not clients[-1]["http2"] and observed["client_status"] != expected["client_status"]:
        mismatches.append("client_status")
    record("expectations.jsonl", {"case": case, **case_identity(selected),
           "expected": expected, "observed": observed, "mismatches": mismatches,
           "observation_result": "failed" if mismatches else "passed",
           "full_lifecycle_pass": None, "companion_profile_qualified": False,
           "limitation": "HTTP2 status HPACK is retained raw; no HTTP2 inspection qualification"})


class Observer:
    def __init__(self, corrupt_notify=False):
        self.corrupt_notify = corrupt_notify
        self.stop = threading.Event()
        self.listener = socket.socket()
        self.listener.bind(("127.0.0.1", 18542))
        self.listener.listen(16)
        self.listener.settimeout(.1)
        self.peers = []
        self.workers = []
        self.thread = threading.Thread(target=self.accept, daemon=True)
        self.thread.start()

    def copy(self, source, destination, connection, direction):
        pending = bytearray()
        try:
            while not self.stop.is_set():
                try:
                    data = source.recv(65536)
                except socket.timeout:
                    continue
                if not data:
                    break
                stamp = time.time_ns()
                record("wire-chunks.jsonl", {"connection": connection,
                       "direction": direction, "wall_ns": stamp, "hex": data.hex()})
                pending.extend(data)
                while len(pending) >= 4:
                    size = struct.unpack("!I", pending[:4])[0]
                    if size > MAX_FRAME:
                        raise ValueError("observer frame budget exceeded")
                    if len(pending) < 4 + size:
                        break
                    raw = bytes(pending[:4 + size])
                    del pending[:4 + size]
                    try:
                        decoded = decode_frame(raw)
                    except (ValueError, UnicodeError) as error:
                        decoded = {"decode_error": str(error)}
                    record("frames.jsonl", {"connection": connection,
                           "direction": direction, "wall_ns": stamp,
                           "sha256": hashlib.sha256(raw).hexdigest(),
                           "hex": raw.hex(), "decoded": decoded})
                    if self.corrupt_notify and direction == "host-agent":
                        forwarded = raw
                        if decoded.get("kind") == 3:
                            # Remove a byte from the final version argument,
                            # while giving the agent a complete TCP/SPOP
                            # envelope. The production notify parser must
                            # reject the damaged typed value before native
                            # transaction allocation.
                            forwarded = struct.pack("!I", len(raw) - 5) + raw[4:-1]
                        record("forwarded-frames.jsonl", {"connection": connection,
                               "direction": direction, "wall_ns": time.time_ns(),
                               "hex": forwarded.hex(),
                               "sha256": hashlib.sha256(forwarded).hexdigest(),
                               "deliberately_corrupted": forwarded != raw})
                        destination.sendall(forwarded)
                if not (self.corrupt_notify and direction == "host-agent"):
                    destination.sendall(data)
        except (OSError, ValueError) as error:
            record("observer-errors.jsonl", {"connection": connection,
                   "direction": direction, "error": str(error)})
        finally:
            if pending:
                record("wire-partials.jsonl", {"connection": connection,
                       "direction": direction, "hex": pending.hex()})
            try:
                destination.shutdown(socket.SHUT_WR)
            except OSError:
                pass

    def accept(self):
        while not self.stop.is_set():
            try:
                source, _ = self.listener.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            try:
                destination = socket.create_connection(("127.0.0.1", 18543), timeout=2)
            except OSError as error:
                record("observer-errors.jsonl", {"direction": "connect-agent", "error": str(error)})
                source.close()
                continue
            connection = len(self.peers) // 2
            self.peers.extend((source, destination))
            for peer in (source, destination):
                peer.settimeout(.2)
            for first, second, direction in ((source, destination, "host-agent"),
                                              (destination, source, "agent-host")):
                worker = threading.Thread(target=self.copy,
                                          args=(first, second, connection, direction), daemon=True)
                self.workers.append(worker)
                worker.start()

    def close(self):
        self.stop.set()
        self.listener.close()
        for peer in self.peers:
            peer.close()
        self.thread.join(2)
        for worker in self.workers:
            worker.join(2)
        record("observer-cleanup.jsonl", {"listener_joined": not self.thread.is_alive(),
               "workers_joined": all(not worker.is_alive() for worker in self.workers)})


def backend(stop):
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 18541))
        listener.listen(16)
        listener.settimeout(.1)
        (ROOT / "backend.ready").touch()
        while not stop.is_set():
            try:
                peer, _ = listener.accept()
            except socket.timeout:
                continue
            with peer:
                peer.settimeout(3)
                request = bytearray()
                while b"\r\n\r\n" not in request:
                    chunk = peer.recv(65536)
                    if not chunk:
                        break
                    request.extend(chunk)
                if b"\r\n\r\n" not in request:
                    continue
                head, body = request.split(b"\r\n\r\n", 1)
                length = next((int(line.split(b":", 1)[1].strip())
                               for line in head.split(b"\r\n")[1:]
                               if line.lower().startswith(b"content-length:")), 0)
                while len(body) < length:
                    chunk = peer.recv(65536)
                    if not chunk:
                        break
                    body += chunk
                record("backend.jsonl", {"wall_ns": time.time_ns(),
                       "header_hex": head.hex(), "body_hex": body.hex()})
                peer.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 7\r\nConnection: close\r\n\r\nBACKEND")


def main():
    selected = json.loads(Path("/mnt/fixtures/selected.json").read_text())
    case = selected["case"]
    with_companion = selected.get("with_companion", False)
    # Mutate only the test representation emitted by the real HAProxy host.
    body_length = "body_len=req.body_size" if case != "missing-body-length" else ""
    if case == "mismatched-body-length":
        body_length = "body_len=int(99)"
    version = "http_version=req.ver" if case != "missing-version" else ""
    body = b"alpha=clean" if case in ("post-allow", "p2-deny") else b""
    if case == "p2-deny":
        body = b"alpha=I12_BLOCK_BODY"
    path = "/" + case
    headers = f"Host: localhost\r\nConnection: close\r\n"
    if case == "p1-deny":
        headers += "X-I12-Block: yes\r\n"
    if body:
        headers += f"Content-Length: {len(body)}\r\nContent-Type: application/x-www-form-urlencoded\r\n"
    if case == "chunked-unsupported":
        headers += "Transfer-Encoding: chunked\r\n"
        body = b"4\r\ntest\r\n0\r\n\r\n"
    request = f"{'POST' if body else 'GET'} {path} HTTP/1.1\r\n{headers}\r\n".encode() + body
    h2 = case in ("h2-unframed-mapping", "h2-content-length-mapping")
    if h2:
        # Minimal real HTTP/2 prior-knowledge request. HPACK static indexes:
        # method GET=2, scheme http=6, path /=4, authority=1, content-length=28.
        block = b"\x82\x86\x84\x01\x09localhost"
        if case == "h2-content-length-mapping":
            block += b"\x0f\x0d\x010"
        request = (b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n" + b"\x00\x00\x00\x04\x00\x00\x00\x00\x00" +
                   len(block).to_bytes(3, "big") + b"\x01\x05\x00\x00\x00\x01" + block)
    (ROOT / "request.raw").write_bytes(request)
    (ROOT / "rules.conf").write_text('''SecRuleEngine On
SecRequestBodyAccess On
SecRequestBodyLimit 1024
SecRequestBodyNoFilesLimit 1024
SecRequestBodyLimitAction Reject
SecAuditEngine On
SecAuditLog /task/native-audit.log
SecAuditLogType Serial
SecAuditLogParts ABFHZ
SecDebugLog /task/native-debug.log
SecDebugLogLevel 9
SecRule REQUEST_HEADERS:X-I12-Block "@streq yes" "id:1999501,phase:1,deny,status:403,log"
SecRule ARGS:alpha "@streq I12_BLOCK_BODY" "id:1999502,phase:2,deny,status:403,log"
''')
    (ROOT / "spoe.cfg").write_text(f'''[modsecurity]
spoe-agent modsecurity-agent
    groups request-check
    option var-prefix modsec
    register-var-names blocked action status redirect_url rule_id phase error response_handle
    max-frame-size 65532
    option continue-on-error
    timeout hello 1s
    timeout idle 3s
    timeout processing 2s
    use-backend be_spoa
spoe-group request-check
    messages check-request
spoe-message check-request
    args request_id=unique-id client_ip=src client_port=src_port server_ip=dst server_port=dst_port method=method path=path uri=url host=req.hdr(host) headers_bin=req.hdrs_bin headers=req.hdrs body=req.body {body_length} {version}
''')
    agent_config = '''listen=127.0.0.1:18543
log-file=/task/agent.log
decision-log=/task/decision.jsonl
rules-file=/task/rules.conf
mode=block
fail-mode=closed
runtime-mode=production
response-phases=false
spoe-timeout=2000
max-transactions=64
'''
    if with_companion:
        agent_config = agent_config.replace("response-phases=false", f'''response-phases=true
response-companion=native-htx
response-companion-socket=/task/companion.sock
response-companion-uid={os.geteuid()}
response-companion-gid={os.getegid()}
response-body-timeout=10000''')
    (ROOT / "agent.conf").write_text(agent_config)
    config = '''global
    nbthread 1
    log stdout format raw local0
    tune.bufsize 65536
defaults
    mode http
    timeout connect 2s
    timeout client 5s
    timeout server 5s
frontend request_only
    bind 127.0.0.1:18540
    unique-id-format %[uuid()]
    option http-buffer-request
    filter spoe engine modsecurity config /task/spoe.cfg
    http-request set-var(txn.modsec.blocked) bool(true)
    http-request send-spoe-group modsecurity request-check
    http-request deny deny_status 503 if { var(txn.modsec.blocked) -m bool }
    default_backend be_app
backend be_app
    server app 127.0.0.1:18541
backend be_spoa
    mode spop
    timeout connect 1s
    timeout server 3s
    server agent 127.0.0.1:18542
'''
    if h2:
        config = config.replace("bind 127.0.0.1:18540", "bind 127.0.0.1:18540 proto h2")
    if with_companion:
        anchor = "    http-request set-var(txn.modsec.blocked) bool(true)"
        config = config.replace(anchor, f"    filter modsecurity-htx response-companion-socket /task/companion.sock response-companion-timeout-ms 2000 response-companion-uid {os.geteuid()} response-companion-gid {os.getegid()} phase4-mode safe\n" + anchor)
    (ROOT / "haproxy.cfg").write_text(config)
    children = []
    stop = threading.Event()
    worker = threading.Thread(target=backend, args=(stop,), daemon=True)
    observer = None
    try:
        worker.start()
        deadline = time.monotonic() + 5
        while not (ROOT / "backend.ready").exists():
            if time.monotonic() > deadline:
                raise TimeoutError("backend startup")
            time.sleep(.01)
        observer = Observer(corrupt_notify=case == "corrupt-notify")
        for name, argv in (("identity", ["/mnt/artifacts/haproxy", "-vv"]),
                           ("config", ["/mnt/artifacts/haproxy", "-c", "-f", "/task/haproxy.cfg"])):
            with (ROOT / (name + ".stdout")).open("wb") as out, (ROOT / (name + ".stderr")).open("wb") as err:
                result = subprocess.run(["rtk", "proxy", *argv], stdout=out, stderr=err, timeout=10)
            record("commands.jsonl", {"argv": ["rtk", "proxy", *argv], "cwd": os.getcwd(), "exit": result.returncode})
            if result.returncode:
                raise RuntimeError(name + " failed")
        for name, argv in (("agent", ["/mnt/artifacts/haproxy-spop", "--config", "/task/agent.conf"]),
                           ("host", ["/mnt/artifacts/haproxy", "-db", "-f", "/task/haproxy.cfg"])):
            fd = os.open(ROOT / (name + "-native-api.jsonl"), os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_APPEND, 0o600)
            env = dict(os.environ, MSCONNECTOR_LIFECYCLE_FD=str(fd),
                       MSCONNECTOR_LIFECYCLE_RUN=selected["run"],
                       MSCONNECTOR_LIFECYCLE_PROFILE="haproxy-spop-request",
                       MSCONNECTOR_LIFECYCLE_CASE=case_identity(selected)["diagnostic_id"])
            with (ROOT / (name + ".stdout")).open("wb") as out, (ROOT / (name + ".stderr")).open("wb") as err:
                # The admitted Python launcher is itself executed through
                # RTK. Retain the actual native PID here for /proc identity,
                # terminal wait status and inherited observer-fd ownership.
                process = subprocess.Popen(argv, stdout=out, stderr=err, env=env, pass_fds=(fd,))
            os.close(fd)
            children.append((name, process, argv))
            time.sleep(.4)
            if process.poll() is not None:
                raise RuntimeError(name + " startup failed")
            snapshot(process, name + "-before")
        if case == "technical-agent-loss":
            # This is an independent transport failure, not an invented
            # native Engine result. The host's configured default stays deny.
            _, agent, _ = children[0]
            agent.send_signal(signal.SIGTERM)
            code = agent.wait(timeout=5)
            record("faults.jsonl", {"kind": "agent-stop-before-request", "exit": code})
        with socket.create_connection(("127.0.0.1", 18540), timeout=5) as client:
            client.settimeout(5)
            started = time.time_ns()
            client.sendall(request)
            response = bytearray()
            terminal = "eof"
            try:
                while True:
                    chunk = client.recv(65536)
                    if not chunk:
                        break
                    response.extend(chunk)
                    if h2:
                        # Stop only after the complete response stream's
                        # END_STREAM frame, preserving every transport byte.
                        pos = 0
                        ended = False
                        while len(response) - pos >= 9:
                            size = int.from_bytes(response[pos:pos + 3], "big")
                            if len(response) - pos < 9 + size:
                                break
                            kind, flags = response[pos + 3:pos + 5]
                            stream = int.from_bytes(response[pos + 5:pos + 9], "big") & 0x7fffffff
                            ended = ended or (stream == 1 and kind in (0, 1) and bool(flags & 1))
                            pos += 9 + size
                        if ended:
                            terminal = "h2-end-stream"
                            break
            except (OSError, TimeoutError) as error:
                terminal = type(error).__name__
            (ROOT / "response.raw").write_bytes(response)
            record("client.jsonl", {"case": case, "started_ns": started,
                   "finished_ns": time.time_ns(), "terminal": terminal,
                   "response_hex": response.hex(), "http2": h2,
                   "status_line": None if h2 else bytes(response).split(b"\r\n", 1)[0].decode("ascii", "replace")})
        time.sleep(.2)
        for name, process, _ in children:
            if process.poll() is None:
                snapshot(process, name + "-after")
    finally:
        for name, process, argv in reversed(children):
            if process.poll() is None:
                process.send_signal(signal.SIGTERM)
            try:
                code = process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                code = process.wait(timeout=5)
            record("commands.jsonl", {"argv": argv, "launcher_rtk_proxied": True, "cwd": os.getcwd(),
                   "exit": code, "reaped": True, "pid": process.pid})
        if observer is not None:
            observer.close()
        stop.set()
        worker.join(4)
        record("cleanup.jsonl", {"backend_joined": not worker.is_alive(),
               "response_companion_configured": with_companion, "full_lifecycle_pass": None})
    evaluate(selected)


if __name__ == "__main__":
    main()
