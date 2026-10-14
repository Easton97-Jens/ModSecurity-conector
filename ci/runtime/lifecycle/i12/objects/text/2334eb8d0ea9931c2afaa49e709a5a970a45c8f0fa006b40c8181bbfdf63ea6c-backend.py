"""Independent synthetic backend: raw bytes first, hash receipts from those bytes."""
import hashlib
import http.server
import json
import signal
from pathlib import Path
import sys
import time

root = Path('/task/backend')
root.mkdir(mode=0o700)
sequence = 0

class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def do_POST(self):
        global sequence
        length = int(self.headers.get('Content-Length', '0'))
        if length < 0 or length > 1024:
            self.send_error(400)
            return
        body = self.rfile.read(length)
        sequence += 1
        nonce = self.path.removeprefix('/i12-eos-')
        response = ('i12-response-marker:' + nonce + '\n').encode('ascii')
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
                   'request_declared_length': length, 'request_bytes': len(body),
                   'request_sha256': hashlib.sha256(body).hexdigest(),
                   'response_status': 200, 'response_bytes': len(response),
                   'response_sha256': hashlib.sha256(response).hexdigest(),
                   'received_ns': received_ns, 'response_written_ns': time.monotonic_ns()}
        with (root / 'receipts.jsonl').open('a', encoding='utf-8') as output:
            output.write(json.dumps(receipt) + '\n')

    def log_message(self, *_args):
        return

server = http.server.HTTPServer(('127.0.0.1', int(sys.argv[1])), Handler)
def stop(_signal, _frame):
    raise SystemExit(0)
signal.signal(signal.SIGTERM, stop)
try:
    server.serve_forever(poll_interval=0.1)
finally:
    server.server_close()
