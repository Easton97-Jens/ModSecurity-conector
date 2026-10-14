"""Waitable client with independently retained socket bytes and actual EOF."""
import hashlib
import json
import os
from pathlib import Path
import socket
import ssl
import sys
import time

port, label = int(sys.argv[1]), sys.argv[2]
shape = json.loads(Path('/mnt/fixtures/shape.json').read_text())
nonce = shape['target'] if label == 'target' else shape['neighbor']
transaction_id = nonce
root = Path('/task/client')
root.mkdir(mode=0o700, exist_ok=True)
body = bytes.fromhex(shape['request_hex'] if label == 'target' else shape['neighbor_request_hex'])
request = (f'POST /{nonce} HTTP/1.1\r\nHost: example.test\r\n'
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
    context = ssl.create_default_context(cafile='/mnt/fixtures/loopback.crt')
    with socket.create_connection(('127.0.0.1', port), timeout=15) as raw_connection:
        with context.wrap_socket(raw_connection,server_hostname='127.0.0.1',suppress_ragged_eofs=False) as connection:
            connection.settimeout(15)
            connection.sendall(request)
            receipt['request_sent_ns'] = time.monotonic_ns()
            while True:
                chunk = connection.recv(4096)
                stamp = {'monotonic_ns': time.monotonic_ns(), 'wall_ns': time.time_ns()}
                if not chunk:
                    receipt['tls_stream_eof_observed'] = True
                    receipt['eof_ns'] = stamp['monotonic_ns']
                    receipt['eof_clock'] = stamp
                    break
                receipt.setdefault("first_recv_clock", stamp)
                received.extend(chunk)
                delimiter = received.find(b"\r\n\r\n")
                if delimiter >= 0:
                    receipt.setdefault("headers_complete_clock", stamp)
                    if len(received) > delimiter + 4:
                        receipt.setdefault("first_body_framing_byte_clock", stamp)
                    block = bytes(received[:delimiter]).lower()
                    wire = bytes(received[delimiter+4:])
                    chunked = any(line.split(b":",1)[0].strip() == b"transfer-encoding" and line.split(b":",1)[1].strip() == b"chunked" for line in block.split(b"\r\n")[1:] if b":" in line)
                    if wire and not chunked:
                        receipt.setdefault("first_entity_clock", stamp)
                    elif b"\r\n" in wire:
                        prefix, rest = wire.split(b"\r\n",1)
                        if int(prefix.split(b";",1)[0],16) > 0 and rest:
                            receipt.setdefault("first_entity_clock", stamp)
                if len(received) > 65536:
                    raise RuntimeError('bounded client response exceeded 64 KiB')
            transport = connection.unwrap()
            transport.settimeout(15)
            transport_tail = transport.recv(1)
            receipt['tcp_eof_clock'] = {'monotonic_ns':time.monotonic_ns(),'wall_ns':time.time_ns()}
            receipt['tcp_eof_observed'] = transport_tail == b''
            if transport_tail != b'': raise RuntimeError('unexpected trailing raw TCP bytes after TLS shutdown')
    header, response_body = bytes(received).split(b'\r\n\r\n', 1)
    lines = header.decode('ascii').split('\r\n')
    status = int(lines[0].split()[1])
    headers = [line.split(':', 1) for line in lines[1:]]
    content_lengths = [value.strip() for name, value in headers if name.lower() == 'content-length']
    transfer = [value.strip() for name, value in headers if name.lower() == 'transfer-encoding']
    wire_body = response_body
    if transfer:
        if transfer != ['chunked'] or content_lengths:
            raise RuntimeError('ambiguous transfer framing')
        decoded = bytearray()
        remainder = wire_body
        chunk_sizes = []
        while True:
            prefix, remainder = remainder.split(b"\r\n",1)
            size = int(prefix.split(b";",1)[0],16)
            if size < 0 or size > 65536: raise RuntimeError('invalid bounded chunk size')
            chunk_sizes.append(size)
            if size == 0:
                if remainder != b"\r\n": raise RuntimeError('unexpected trailers/trailing bytes in synthetic response')
                break
            if len(remainder) < size+2 or remainder[size:size+2] != b"\r\n":
                raise RuntimeError('incomplete chunk framing')
            decoded.extend(remainder[:size]); remainder = remainder[size+2:]
        response_body = bytes(decoded)
        receipt['chunk_sizes'] = chunk_sizes
    elif content_lengths != [str(len(response_body))]:
        raise RuntimeError('incomplete or ambiguous Content-Length framing')
    receipt['wire_body_sha256'] = hashlib.sha256(wire_body).hexdigest()
    receipt['wire_body_bytes'] = len(wire_body)
    receipt.update(status=status, headers=lines, bytes=len(response_body),
                   sha256=hashlib.sha256(response_body).hexdigest(),
                   framing={'content_lengths': content_lengths, 'transfer_encoding': transfer,
                            'received_entity_bytes': len(response_body)})
    (root / f'{label}.headers.raw').write_bytes(header + b'\r\n\r\n')
    (root / f'{label}.body.raw').write_bytes(response_body)
    if status != 200:
        raise RuntimeError('response was not HTTP 200')
    expected = bytes.fromhex(shape['response_hex'] if label == 'target' else shape['neighbor_response_hex'])
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
