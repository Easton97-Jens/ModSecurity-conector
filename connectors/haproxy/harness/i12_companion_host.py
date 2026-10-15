#!/usr/bin/env python3
"""Independent, loopback-only I12 companion host capture; never assigns PASS IDs.

Supply freshly source-bound observed binaries. The output records physical bytes,
backend observations, each native FD, process maps, argv/exits, and file hashes.
HTTP success alone intentionally cannot qualify a lifecycle.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import signal
import socket
import ssl
import subprocess
import sys
import threading
import time

ROOT = Path("/var/tmp/codex/ModSecurity-conector")
BODY = b"companion-physical-response-body\n"
BACKEND_LISTEN_BACKLOG = 32


class CaptureBackendServer(ThreadingHTTPServer):
    request_queue_size = BACKEND_LISTEN_BACKLOG

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def fresh_root(path: Path, allowed_root: Path = ROOT) -> Path:
    if not path.is_absolute() or path.is_symlink():
        raise ValueError("absolute, physical external run root required")
    resolved = path.resolve()
    resolved.relative_to(allowed_root.resolve())
    resolved.mkdir(mode=0o700, parents=False, exist_ok=False)
    return resolved

def start_capture_thread(target, args, registry):
    """Publish only started threads so concurrent cleanup never joins a new one."""
    thread = threading.Thread(target=target, args=args, daemon=True)
    thread.start()
    registry.append(thread)
    return thread


def stop_capture_threads(workers, sockets, relays):
    """Freeze relay ownership only after every bounded accept worker has stopped."""
    for worker in workers:
        if worker.ident is not None:
            worker.join(timeout=4)
    if any(worker.is_alive() for worker in workers):
        raise RuntimeError("capture accept worker did not stop; relay ownership is not frozen")
    for sock in sockets:
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        sock.close()
    stopped_relays = tuple(relays)
    for thread in stopped_relays:
        thread.join(timeout=1)
    if any(thread.is_alive() for thread in stopped_relays):
        raise RuntimeError("capture relay did not stop")
    return {"accept_workers_stopped": len(workers), "relays_stopped": len(stopped_relays)}


def capture_client(root: Path, front: int, index: int, cancel: bool, neighbor: bool = False) -> None:
    path = "/neighbor" if neighbor else f"/i12/{index}"
    body = b"neighbor" if neighbor else b"abcdefgh"
    request = (f"POST {path} HTTP/1.1\r\nHost: companion.invalid\r\nContent-Type: text/plain\r\nContent-Length: {len(body)}\r\nConnection: close\r\n\r\n").encode() + body
    response = bytearray()
    error = None
    kernel_eof = None
    unwrap_error = None
    with ssl.create_default_context(cafile=str(root / "tls.crt")).wrap_socket(socket.create_connection(("127.0.0.1", front), timeout=5), server_hostname="localhost", suppress_ragged_eofs=False) as sock:
        sock.sendall(request)
        if cancel:
            response.extend(sock.recv(4096))
        else:
            try:
                while chunk := sock.recv(4096):
                    response.extend(chunk)
            except OSError as exc:
                error = type(exc).__name__ + ": " + str(exc)
        if not error and not cancel:
            try:
                raw_socket = sock.unwrap()
                raw_socket.settimeout(5)
                kernel_eof = raw_socket.recv(1) == b""
                raw_socket.close()
            except OSError as exc:
                unwrap_error = type(exc).__name__ + ": " + str(exc)
    (root / f"client-{index}.request").write_bytes(request)
    (root / f"client-{index}.response").write_bytes(response)
    (root / f"client-{index}.json").write_text(json.dumps({"kind": "client", "index": index, "length": len(response), "error": error, "tls_eof": "exception" if error else ("client_cancel" if cancel else "close_notify"), "kernel_tcp_eof": kernel_eof, "unwrap_error": unwrap_error, "time_ns": time.time_ns()}) + "\n")

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--neighbor", action="store_true")
    parser.add_argument("--case-id", default=None)
    parser.add_argument("--host", required=True, type=Path)
    parser.add_argument("--agent", required=True, type=Path)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--openssl-config", type=Path, required=True)
    parser.add_argument("--allowed-root", type=Path, default=ROOT)
    parser.add_argument("--case", choices=("p3-deny", "safe", "strict", "missing", "expired", "parallel", "cancel"), required=True)
    args = parser.parse_args()
    root = fresh_root(args.root, args.allowed_root)
    if len(str(root / "mrc.sock")) >= 100:
        raise ValueError("MRC1 socket path must be shorter than 100 bytes")
    commands = []
    children = []
    observations = []
    lock = threading.Lock()
    def record(value):
        with lock:
            observations.append(value)
    def port():
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            return sock.getsockname()[1]
    front, spop = port(), port()
    proxy = socket.socket()
    proxy.bind(("127.0.0.1", 0))
    proxy.listen(16)
    proxy.settimeout(.1)
    proxy_stop = threading.Event()
    proxy_threads = []
    proxy_sockets = []
    def proxy_loop():
        connection = 0
        while not proxy_stop.is_set():
            try:
                downstream, _ = proxy.accept()
            except socket.timeout:
                continue
            except OSError:
                return
            upstream = socket.create_connection(("127.0.0.1", spop), timeout=3)
            proxy_sockets.extend((downstream, upstream))
            connection += 1
            def relay(source, target, path):
                with path.open("wb") as raw:
                    try:
                        while not proxy_stop.is_set():
                            chunk = source.recv(65536)
                            if not chunk:
                                break
                            raw.write(chunk)
                            raw.flush()
                            target.sendall(chunk)
                    except OSError:
                        pass
                    try:
                        target.shutdown(socket.SHUT_WR)
                    except OSError:
                        pass
            for source, target, direction in ((downstream, upstream, "notify"), (upstream, downstream, "ack")):
                start_capture_thread(relay, (source, target, root / f"spop-{connection}-{direction}.bin"), proxy_threads)
    proxy_worker = threading.Thread(target=proxy_loop, daemon=True)
    # Independent private MRC1 byte tap; peer UID/GID checks remain effective.
    mrc_proxy = socket.socket(socket.AF_UNIX)
    mrc_proxy.bind(str(root / "mrc-tap.sock"))
    mrc_proxy.listen(32)
    mrc_proxy.settimeout(.1)
    def mrc_loop():
        connection = 0
        while not proxy_stop.is_set():
            try:
                downstream, _ = mrc_proxy.accept()
            except socket.timeout:
                continue
            except OSError:
                return
            upstream = socket.socket(socket.AF_UNIX)
            upstream.connect(str(root / "mrc.sock"))
            proxy_sockets.extend((downstream, upstream))
            connection += 1
            def relay(source, target, path):
                with path.open("wb") as raw:
                    try:
                        while not proxy_stop.is_set():
                            chunk = source.recv(65536)
                            if not chunk:
                                break
                            raw.write(chunk)
                            raw.flush()
                            target.sendall(chunk)
                    except OSError:
                        pass
                    try:
                        target.shutdown(socket.SHUT_WR)
                    except OSError:
                        pass
            for source, target, direction in ((downstream, upstream, "host"), (upstream, downstream, "owner")):
                start_capture_thread(relay, (source, target, root / f"mrc1-{connection}-{direction}.bin"), proxy_threads)
    mrc_worker = threading.Thread(target=mrc_loop, daemon=True)

    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"
        def do_POST(self):
            request = self.rfile.read(int(self.headers.get("Content-Length", "0")))
            record({"kind": "backend_request", "path": self.path, "body_hex": request.hex(), "headers": list(self.headers.items()), "time_ns": time.time_ns()})
            if args.case == "expired":
                time.sleep(.4)
            response_body = b"healthy-neighbor-response\n" if self.path == "/neighbor" else BODY
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("X-Companion", "deny" if args.case == "p3-deny" else "allow")
            self.send_header("Content-Length", str(len(response_body)))
            self.end_headers()
            if args.case == "cancel":
                time.sleep(.4)
            try:
                self.wfile.write(response_body)
            except (BrokenPipeError, ConnectionResetError):
                record({"kind": "backend_disconnect", "time_ns": time.time_ns()})
        def log_message(self, *_args):
            return
    backend = CaptureBackendServer(("127.0.0.1", 0), Handler)
    worker = threading.Thread(target=backend.serve_forever, daemon=True)
    def run(argv, label):
        actual = ["rtk", "proxy", *map(str, argv)]
        result = subprocess.run(actual, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        (root / (label + ".stdout")).write_bytes(result.stdout)
        (root / (label + ".stderr")).write_bytes(result.stderr)
        commands.append({"label": label, "argv": actual, "exit": result.returncode})
        if result.returncode:
            raise RuntimeError(label + " failed")
    def start(argv, label):
        fd = os.open(root / (label + "-native.jsonl"), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_APPEND | os.O_NOFOLLOW, 0o600)
        env = dict(os.environ, MSCONNECTOR_LIFECYCLE_FD=str(fd), MSCONNECTOR_LIFECYCLE_RUN=root.name, MSCONNECTOR_LIFECYCLE_PROFILE="haproxy-spop-htx-response-companion", MSCONNECTOR_LIFECYCLE_CASE=args.case_id or args.case)
        argv = list(map(str, argv))
        # Direct subprocess ownership matches the preserved private launcher: no shell.
        with (root / (label + ".stdout")).open("wb") as out, (root / (label + ".stderr")).open("wb") as err:
            process = subprocess.Popen(argv, env=env, pass_fds=(fd,), stdout=out, stderr=err)
        os.close(fd)
        children.append((label, process))
        commands.append({"label": label, "argv": argv, "pid": process.pid})
        return process
    def wait_for(value, proc):
        deadline = time.monotonic() + 8
        while not value():
            if proc.poll() is not None or time.monotonic() > deadline:
                raise RuntimeError("service readiness failed")
            time.sleep(.02)
    def snapshot(stage):
        for label, process in children:
            proc = Path("/proc") / str(process.pid)
            (root / f"{label}-{stage}.maps").write_text((proc / "maps").read_text())
            (root / f"{label}-{stage}.status").write_text((proc / "status").read_text())
            fds = {}
            for path in (proc / "fd").iterdir():
                try:
                    fds[path.name] = os.readlink(path)
                except FileNotFoundError:
                    fds[path.name] = "closed_during_snapshot"
            (root / f"{label}-{stage}.fds.json").write_text(json.dumps({"pid": process.pid, "stage": stage, "wall_ns": time.time_ns(), "monotonic_ns": time.monotonic_ns(), "fds": fds}, indent=2) + "\n")
    def client(index, neighbor=False):
        argv = [sys.executable, str(Path(__file__).resolve()), "--client-capture", str(root), str(front), str(index), "neighbor" if neighbor else args.case]
        result = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=12)
        (root / f"client-{index}.stdout").write_bytes(result.stdout)
        (root / f"client-{index}.stderr").write_bytes(result.stderr)
        with lock:
            commands.append({"label": f"client-{index}", "argv": argv, "exit": result.returncode, "reaped": True})
        if result.returncode:
            raise RuntimeError(f"client-{index} failed: {result.returncode}")
        record(json.loads((root / f"client-{index}.json").read_text()))
    status = 0
    try:
        run([args.host, "-vv"], "host-identity")
        run(["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-sha256", "-days", "1", "-config", args.openssl_config, "-extensions", "v3_ca", "-subj", "/CN=localhost", "-addext", "subjectAltName=DNS:localhost", "-keyout", root / "tls.key", "-out", root / "tls.crt"], "tls")
        (root / "tls.key").chmod(0o600)
        (root / "tls.pem").write_bytes((root / "tls.key").read_bytes() + (root / "tls.crt").read_bytes())
        (root / "tls.pem").chmod(0o600)
        rules = "SecRuleEngine On\nSecRequestBodyAccess On\nSecResponseBodyAccess On\nSecResponseBodyMimeType text/plain\nSecAuditEngine On\nSecAuditLogType Serial\nSecAuditLogParts ABFHZ\n" + f"SecAuditLog {root}/native-audit.log\nSecDebugLog {root}/native-debug.log\nSecDebugLogLevel 9\n"
        if args.case == "p3-deny":
            rules += 'SecRule RESPONSE_HEADERS:X-Companion "@streq deny" "id:1999503,phase:3,deny,status:403,log,msg:companion-P3"\n'
        else:
            rules += 'SecRule RESPONSE_BODY "@contains companion-physical" "id:1999504,phase:4,deny,status:403,log,msg:companion-P4"\n'
        (root / "rules.conf").write_text(rules)
        ttl = 100 if args.case == "expired" else 5000
        (root / "agent.conf").write_text(f"listen=127.0.0.1:{spop}\nlog-file={root}/spoa.log\ndecision-log={root}/decision.jsonl\naudit-log={root}/audit.jsonl\nrules-file={root}/rules.conf\nmode=block\nfail-mode=closed\nruntime-mode=production\nresponse-companion=native-htx\nresponse-phases=true\nresponse-companion-socket={root}/mrc.sock\nresponse-companion-uid={os.geteuid()}\nresponse-companion-gid={os.getegid()}\nresponse-body-timeout={ttl}\nspoe-timeout=2000\nmax-transactions=64\n")
        (root / "spoe.cfg").write_text(f"[modsecurity]\nspoe-agent modsecurity-agent\n    groups request-check\n    option var-prefix modsec\n    register-var-names blocked action status redirect_url rule_id phase error response_handle\n    max-frame-size 65532\n    option continue-on-error\n    timeout hello 1s\n    timeout idle 3s\n    timeout processing 2s\n    use-backend be_spoa\nspoe-group request-check\n    messages check-request\nspoe-message check-request\n    args request_id=unique-id client_ip=src client_port=src_port server_ip=dst server_port=dst_port method=method path=path uri=url host=req.hdr(host) headers_bin=req.hdrs_bin headers=req.hdrs body=req.body body_len=req.body_size http_version=req.ver\n")
        send = "" if args.case == "missing" else "    http-request send-spoe-group modsecurity request-check\n"
        mode = "strict" if args.case == "strict" else "safe"
        (root / "haproxy.cfg").write_text(f"global\n    nbthread 1\n    log stdout format raw local0\n    tune.bufsize 65536\ndefaults\n    mode http\n    timeout connect 2s\n    timeout client 5s\n    timeout server 5s\nfrontend combined\n    bind 127.0.0.1:{front} ssl crt {root}/tls.pem\n    unique-id-format %[uuid()]\n    option http-buffer-request\n    filter spoe engine modsecurity config {root}/spoe.cfg\n    filter modsecurity-htx response-companion-socket {root}/mrc-tap.sock response-companion-timeout-ms 2000 response-companion-uid {os.geteuid()} response-companion-gid {os.getegid()} phase4-mode {mode}\n{send}    http-request deny status 403 if {{ var(txn.modsec.blocked) -m bool }}\n    default_backend be_app\nbackend be_app\n    server app 127.0.0.1:{backend.server_port}\nbackend be_spoa\n    mode spop\n    timeout connect 1s\n    timeout server 3s\n    server agent 127.0.0.1:{proxy.getsockname()[1]}\n")
        run([args.host, "-c", "-f", root / "haproxy.cfg"], "config")
        worker.start()
        proxy_worker.start()
        agent = start([args.agent, "--config", root / "agent.conf"], "agent")
        wait_for(lambda: (root / "mrc.sock").is_socket(), agent)
        mrc_worker.start()
        host = start([args.host, "-db", "-f", root / "haproxy.cfg"], "host")
        time.sleep(.3)
        if host.poll() is not None:
            raise RuntimeError("host exited at startup")
        # Capture the actual mapped engine and host independently of caller claims.
        for name, proc in children:
            (root / (name + ".maps")).write_text(Path(f"/proc/{proc.pid}/maps").read_text())
        snapshot("before-main")
        with ThreadPoolExecutor(max_workers=8) as executor:
            list(executor.map(client, range(16 if args.case == "parallel" else 1)))
        time.sleep(.2)
        snapshot("after-main")
        if args.neighbor:
            client(100, neighbor=True)
            time.sleep(.2)
            snapshot("after-neighbor")
        time.sleep(.3)
    except Exception as exc:
        status = 1
        record({"kind": "runner_error", "error": repr(exc)})
    finally:
        for name, proc in reversed(children):
            if proc.poll() is None:
                proc.send_signal(signal.SIGUSR1 if name == "host" else signal.SIGTERM)
            try:
                code = proc.wait(timeout=8)
            except subprocess.TimeoutExpired:
                proc.kill()
                code = proc.wait(timeout=3)
            commands.append({"label": name + "-wait", "exit": code, "reaped": True})
        if worker.is_alive():
            backend.shutdown()
            worker.join(timeout=3)
        backend.server_close()
        proxy_stop.set()
        proxy.close()
        mrc_proxy.close()
        (root / "mrc-tap.sock").unlink(missing_ok=True)
        try:
            record({"kind": "capture_cleanup", **stop_capture_threads((mrc_worker, proxy_worker), proxy_sockets, proxy_threads)})
        except Exception as exc:
            status = 1
            record({"kind": "capture_cleanup_error", "error": repr(exc)})
        (root / "observations.json").write_text(json.dumps(observations, indent=2) + "\n")
        receipt = {"format": "i12-companion-private-host-v1", "case": args.case, "case_id": args.case_id, "commands": commands, "runner_exit": status, "host_sha256": sha(args.host), "agent_sha256": sha(args.agent), "runner_sha256": sha(Path(__file__)), "full_lifecycle_pass": None, "limitation": "Physical capture only; independent oracle/lifecycle review required. Private TLS keys omitted from hash inventory.", "files": {str(p.relative_to(root)): sha(p) for p in sorted(root.rglob("*")) if p.is_file() and p.suffix not in (".key", ".pem")}}
        (root / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    return status

if __name__ == "__main__":
    if len(sys.argv) == 6 and sys.argv[1] == "--client-capture":
        capture_client(Path(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5] == "cancel", sys.argv[5] == "neighbor")
    else:
        raise SystemExit(main())
