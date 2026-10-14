"""Waitable client with independently retained socket bytes and actual EOF."""
import hashlib
import json
import os
from pathlib import Path
import socket
import sys
import time

port, nonce, transaction_id, label = int(sys.argv[1]), *sys.argv[2:]
root = Path('/task/client')
root.mkdir(mode=0o700, exist_ok=True)
body = ('i12-request-marker:' + nonce + '\n').encode('ascii')
request = (f'POST /i12-eos-{nonce} HTTP/1.1\r\nHost: example.test\r\n'
           f'X-Request-Id: {transaction_id}\r\nContent-Type: text/plain\r\n'
           f'Content-Length: {len(body)}\r\nConnection: close\r\n\r\n').encode('ascii') + body
(root / f'{label}.request.raw').write_bytes(request)
received = bytearray()
receipt = {'label': label, 'nonce': nonce, 'transaction_id': transaction_id,
           'pid': os.getpid(),
           'request_bytes': len(body), 'request_sha256': hashlib.sha256(body).hexdigest(),
           'started_ns': time.monotonic_ns(), 'tcp_eof_observed': False, 'error': None}
exit_code = 1
try:
    with socket.create_connection(('127.0.0.1', port), timeout=15) as connection:
        connection.settimeout(15)
        connection.sendall(request)
        receipt['request_sent_ns'] = time.monotonic_ns()
        while True:
            chunk = connection.recv(4096)
            stamp = {'monotonic_ns': time.monotonic_ns(), 'wall_ns': time.time_ns()}
            if not chunk:
                receipt['tcp_eof_observed'] = True
                receipt['eof_ns'] = stamp['monotonic_ns']
                receipt['eof_clock'] = stamp
                break
            receipt.setdefault("first_recv_clock", stamp)
            received.extend(chunk)
            delimiter = received.find(b"\r\n\r\n")
            if delimiter >= 0:
                receipt.setdefault("headers_complete_clock", stamp)
                if len(received) > delimiter + 4:
                    receipt.setdefault("first_entity_clock", stamp)
            if len(received) > 65536:
                raise RuntimeError('bounded client response exceeded 64 KiB')
    header, response_body = bytes(received).split(b'\r\n\r\n', 1)
    lines = header.decode('ascii').split('\r\n')
    status = int(lines[0].split()[1])
    headers = [line.split(':', 1) for line in lines[1:]]
    content_lengths = [value.strip() for name, value in headers if name.lower() == 'content-length']
    transfer = [value.strip() for name, value in headers if name.lower() == 'transfer-encoding']
    receipt.update(status=status, headers=lines, bytes=len(response_body),
                   sha256=hashlib.sha256(response_body).hexdigest(),
                   framing={'content_lengths': content_lengths, 'transfer_encoding': transfer,
                            'received_entity_bytes': len(response_body)})
    (root / f'{label}.headers.raw').write_bytes(header + b'\r\n\r\n')
    (root / f'{label}.body.raw').write_bytes(response_body)
    if status != 200 or transfer or content_lengths != [str(len(response_body))]:
        raise RuntimeError('response was not an unambiguous complete HTTP 200 Content-Length response')
    expected = ('i12-response-marker:' + nonce + '\n').encode('ascii')
    if response_body != expected:
        raise RuntimeError('client response differs from synthetic backend response')
    exit_code = 0
except Exception as error:
    receipt['error'] = {'type': type(error).__name__, 'message': str(error)}
finally:
    (root / f'{label}.response.raw').write_bytes(received)
    receipt.update(completed_ns=time.monotonic_ns(), proposed_process_exit=exit_code)
    (root / f'{label}.receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
raise SystemExit(exit_code)
