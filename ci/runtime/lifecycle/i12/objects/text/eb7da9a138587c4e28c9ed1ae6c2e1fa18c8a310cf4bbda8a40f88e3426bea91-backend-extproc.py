"""Independent synthetic backend: raw bytes first, hash receipts from those bytes."""
import hashlib
import http.server
import json
import signal
import ssl
from pathlib import Path
import sys
import time

root = Path('/task/backend')
root.mkdir(mode=0o700)
sequence = 0
shape = json.loads(Path("/mnt/fixtures/shape.json").read_text())
shapes = {"/"+shape["target"]:(shape["request_hex"],shape["response_hex"]), "/"+shape["neighbor"]:(shape["neighbor_request_hex"],shape["neighbor_response_hex"])}

def read_framed_body(stream, headers, limit=1024):
    lengths = headers.get_all('Content-Length', [])
    transfer = headers.get_all('Transfer-Encoding', [])
    wire = bytearray()
    if transfer:
        if lengths or [v.strip().lower() for v in transfer] != ['chunked']:
            raise ValueError('ambiguous transfer framing')
        body = bytearray()
        while True:
            line = stream.readline(130)
            wire.extend(line)
            if len(line) > 128 or not line.endswith(b'\r\n'):
                raise ValueError('invalid chunk line')
            token = line[:-2]
            if not token or any(c not in b'0123456789abcdefABCDEF' for c in token):
                raise ValueError('invalid chunk size')
            size = int(token, 16)
            if size > limit-len(body): raise ValueError('body limit exceeded')
            if size == 0:
                tail = stream.read(2);wire.extend(tail)
                if tail != b'\r\n':raise ValueError('trailers unsupported in synthetic fixture')
                return bytes(body), bytes(wire), {'kind':'chunked','declared_length':None,'end_of_framing':True}
            chunk=stream.read(size+2);wire.extend(chunk)
            if len(chunk)!=size+2 or chunk[-2:]!=b'\r\n':raise ValueError('truncated chunk')
            body.extend(chunk[:-2])
    if len(lengths)!=1 or not lengths[0].isdigit():raise ValueError('missing or ambiguous length')
    length=int(lengths[0])
    if length>limit:raise ValueError('body limit exceeded')
    body=stream.read(length)
    if len(body)!=length:raise ValueError('truncated content length')
    return body,body,{'kind':'content-length','declared_length':length,'end_of_framing':True}

class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def do_POST(self):
        global sequence
        sequence += 1
        (root / f'{sequence}.request-line.raw').write_bytes(self.raw_requestline)
        (root / f'{sequence}.parsed-headers.json').write_text(json.dumps(list(self.headers.items())))
        try:
            body, wire, framing = read_framed_body(self.rfile, self.headers)
        except ValueError as error:
            (root / f'{sequence}.framing-error.json').write_text(json.dumps({'error':str(error)}))
            self.send_error(400);return
        length = framing['declared_length']
        (root / f'{sequence}.request-framing.raw').write_bytes(wire)
        if self.path not in shapes or body != bytes.fromhex(shapes[self.path][0]):
            self.send_error(400); return
        nonce = self.path[1:]
        response = bytes.fromhex(shapes[self.path][1])
        (root / f'{sequence}.request-body.raw').write_bytes(body)
        (root / f'{sequence}.response-body.raw').write_bytes(response)
        received_ns = time.monotonic_ns()
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Content-Length', str(len(response)))
        self.send_header('Connection', 'close')
        self.end_headers()
        self.wfile.write(response)
        self.wfile.flush()
        self.close_connection = True
        receipt = {'pid': __import__('os').getpid(), 'sequence': sequence, 'path': self.path,
                   'request_id': self.headers.get('X-Request-Id'), 'nonce': nonce,
                   'request_declared_length': length, 'request_framing':framing, 'request_wire_bytes':len(wire), 'request_wire_sha256':hashlib.sha256(wire).hexdigest(), 'request_bytes': len(body),
                   'request_sha256': hashlib.sha256(body).hexdigest(),
                   'response_status': 200, 'response_bytes': len(response),
                   'response_sha256': hashlib.sha256(response).hexdigest(),
                   'received_ns': received_ns, 'response_written_ns': time.monotonic_ns(), 'wall_ns': time.time_ns()}
        with (root / 'receipts.jsonl').open('a', encoding='utf-8') as output:
            output.write(json.dumps(receipt) + '\n')

    def log_message(self, *_args):
        return

server = http.server.HTTPServer(('127.0.0.1', int(sys.argv[1])), Handler)
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('/task/runtime/loopback.crt','/task/runtime/loopback.key')
server.socket = context.wrap_socket(server.socket, server_side=True)
def stop(_signal, _frame):
    raise SystemExit(0)
signal.signal(signal.SIGTERM, stop)
try:
    server.serve_forever(poll_interval=0.1)
finally:
    server.server_close()
