"""Actual MSE1 relay with independently named, selected-operation faults."""
import hashlib
import importlib.util
import json
from pathlib import Path
import signal
import socket
import sys
import threading
import time

_spec = importlib.util.spec_from_file_location('native_acceptance_transport', Path(__file__).with_name('fault_proxy.py'))
transport = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(transport)


def relay(client, engine_path, case):
    chunks = 0
    injected = False
    fault = case['fixture'].get('fault') or {}
    kind = fault.get('kind')
    key = case['key']
    connection_id = time.monotonic_ns()
    positive_control = False
    try:
        with client, socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as engine:
            engine.settimeout(15)
            client.settimeout(15)
            engine.connect(engine_path)
            while True:
                head, payload = transport.frame(client)
                opcode = head[5]
                if opcode == 1:
                    positive_control = case['positive_control_id'].encode() in payload
                chunks += int(opcode == 5)
                row = {'key': key, 'connection': connection_id, 'opcode': opcode,
                       'request_bytes': len(payload), 'request_sha256': hashlib.sha256(head + payload).hexdigest(),
                       'started_ns': time.monotonic_ns(), 'fault': None}
                if kind == 'invalid-metadata' and opcode == 1 and not injected:
                    uri = case['fixture']['request']['uri'].encode()
                    if payload.count(uri) != 1:
                        raise ValueError('exact metadata URI not present once')
                    payload = payload.replace(uri, b'\x00' + uri[1:], 1)
                    injected = True
                    row['fault'] = 'outgoing-BEGIN-URI-embedded-NUL'
                engine.sendall(head + payload)
                reply_head, reply = transport.frame(engine)
                target = ((kind == 'commit-ack-applied' and opcode == 10) or
                          (kind in ('incomplete-framing', 'no-second-response') and opcode == 5 and chunks == 2))
                if target and not injected and not positive_control:
                    if opcode == 5:
                        marker = Path('/task/barriers') / key
                        deadline = time.monotonic() + 5
                        while not marker.exists() and time.monotonic() < deadline:
                            time.sleep(0.01)
                        row['actual_client_prefix_marker'] = marker.exists()
                        if not marker.exists():
                            raise TimeoutError('no client prefix before postcommit fault')
                    reply = reply[:1] + b'\x05' + reply[2:]
                    injected = True
                    row['fault'] = 'MSE1-result-TECHNICAL-5'
                if kind == 'mse1-error' and opcode == 1 and not injected:
                    reply_head = b'BAD!' + reply_head[4:]
                    injected = True
                    row['fault'] = 'MSE1-reply-magic-BAD!'
                timeout_opcode = 5 if kind == 'engine_timeout_after_commit' else 1
                if kind in ('timeout', 'engine_timeout_before_commit', 'engine_timeout_after_commit') and opcode == timeout_opcode and not injected:
                    if opcode != 5 or chunks >= 2:
                        time.sleep(5.5)
                        injected = True
                        row['fault'] = 'physical-reply-delay-5500ms-exceeds-real5000ms-client-deadline'
                row.update(reply_bytes=len(reply), reply_sha256=hashlib.sha256(reply_head + reply).hexdigest(),
                           completed_ns=time.monotonic_ns())
                transport.record(row)
                client.sendall(reply_head + reply)
    except (EOFError, OSError, ValueError) as error:
        transport.record({'key': key, 'connection': connection_id, 'end': type(error).__name__,
                          'injected': injected, 'monotonic_ns': time.monotonic_ns()})


def main():
    listener_path = transport.validate_socket(sys.argv[1], listener=True)
    engine_path = transport.validate_socket(sys.argv[2], listener=False)
    manifest = json.loads(Path(sys.argv[3]).read_text())
    case = next(c for c in manifest['cases'] if c['key'] == sys.argv[4])
    listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    listener.bind(listener_path)
    owned = Path(listener_path).lstat()
    listener.listen(16)
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    try:
        while True:
            client, _ = listener.accept()
            threading.Thread(target=relay, args=(client, engine_path, case), daemon=True).start()
    finally:
        listener.close()
        transport.remove_owned_socket(owned)


if __name__ == '__main__':
    main()
