"""Test-only UDS relay: real engine execution, explicit physical reply faults."""
import json
from pathlib import Path
import re
import signal
import socket
import struct
import sys
import threading
import time

LOG = Path('/task/proxy.jsonl')
LOCK = threading.Lock()


def record(value):
    with LOCK, LOG.open('a') as output:
        output.write(json.dumps(value) + '\n')


def exact(connection, count):
    result = bytearray()
    while len(result) < count:
        part = connection.recv(count - len(result))
        if not part:
            raise EOFError()
        result.extend(part)
    return bytes(result)


def frame(connection):
    head = exact(connection, 12)
    count = struct.unpack('!I', head[8:12])[0]
    if count > 131072:
        raise ValueError('bounded proxy frame exceeded')
    return head, exact(connection, count)


def relay(client, engine_path):
    label = 'unknown'
    connection_id = time.monotonic_ns()
    body_chunks = 0
    try:
        with client, socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as engine:
            engine.settimeout(15)
            client.settimeout(15)
            engine.connect(engine_path)
            while True:
                head, payload = frame(client)
                opcode = head[5]
                if opcode == 5:
                    body_chunks += 1
                if opcode == 1:
                    match = re.search(rb'/i12-eos-([a-z0-9-]+)', payload)
                    if match:
                        label = match[1].decode()
                engine.sendall(head + payload)
                reply_head, reply_payload = frame(engine)
                fault = None
                if label == 'fault-mse1' and opcode == 1:
                    reply_head = b'BAD1' + reply_head[4:]
                    fault = 'corrupt-MSE1-magic-after-real-engine-begin'
                elif label == 'fault-result' and opcode == 3:
                    reply_payload = reply_payload[:1] + b'\x05' + reply_payload[2:]
                    fault = 'technical-result-after-real-request-EOS'
                elif label == 'fault-postcommit' and opcode == 5 and body_chunks >= 2:
                    reply_payload = reply_payload[:1] + b'\x05' + reply_payload[2:]
                    fault = 'technical-result-on-response-chunk-after-host-headers'
                elif label == 'fault-ack' and opcode == 10:
                    reply_payload = reply_payload[:1] + b'\x05' + reply_payload[2:]
                    fault = 'technical-result-on-acknowledge-applied'
                record({'connection': connection_id, 'label': label, 'opcode': opcode,
                        'request_payload_bytes': len(payload), 'reply_payload_bytes': len(reply_payload),
                        'fault': fault, 'monotonic_ns': time.monotonic_ns()})
                client.sendall(reply_head + reply_payload)
    except (EOFError, OSError, ValueError) as error:
        record({'connection': connection_id, 'label': label, 'end': type(error).__name__,
                'monotonic_ns': time.monotonic_ns()})


if __name__ == '__main__':
    path, engine_path = sys.argv[1:]
    listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    listener.bind(path)
    listener.listen(16)
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    try:
        while True:
            client, _ = listener.accept()
            threading.Thread(target=relay, args=(client, engine_path), daemon=True).start()
    finally:
        listener.close()
        Path(path).unlink(missing_ok=True)
