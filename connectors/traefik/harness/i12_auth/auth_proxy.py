"""Transparent bounded authorization TCP relay, retaining synthetic samples."""
import hashlib
import http.client
import http.server
import json
import os
from pathlib import Path
import signal
import sys
import time

root = Path('/task/authorization');root.mkdir(mode=0o700)
class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    def do_POST(self):self.forward()
    def do_GET(self):self.forward()
    def forward(self):
        length = int(self.headers.get('Content-Length', '0'))
        if not 0 <= length <= 8192:self.send_error(400);return
        body = self.rfile.read(length)
        identity = self.headers.get('X-Request-Id', '')
        if not identity.startswith('i12-auth-') or not identity[9:].replace('-', '').isalnum():
            self.send_error(400);return
        name = identity[9:]
        (root / (name + '.sample.raw')).write_bytes(body)
        record = {'case': name, 'transaction_id': identity, 'pid': os.getpid(),
            'sample_declared_length': length, 'sample_actual_bytes': len(body),
            'sample_sha256': hashlib.sha256(body).hexdigest(), 'received_ns': time.monotonic_ns()}
        connection = http.client.HTTPConnection('127.0.0.1', int(sys.argv[2]), timeout=10)
        try:
            connection.request(self.command, self.path, body=body, headers=dict(self.headers))
            response = connection.getresponse();data = response.read(65537)
            if len(data) > 65536:raise RuntimeError('authorization response bound exceeded')
            record.update(authorization_status=response.status, authorization_body_bytes=len(data),
                response_handle_count=len(response.headers.get_all('X-Msconnector-Response-Handle', [])))
            if name in ('auth-cap-boundary','auth-cap-overlimit'):
                data=b'i' * (32768 if name=='auth-cap-boundary' else 32769)
                record['explicit_relay_fault']='synthetic authorization response capacity boundary'
            record['relay_response_bytes']=len(data)
            self.send_response(response.status)
            for key, value in response.getheaders():
                if key.lower() == 'x-msconnector-response-handle':
                    if name == 'observer-no-handle':continue
                    if name == 'observer-invalid-handle':value = 'i12-invalid-correlation-handle'
                if key.lower() not in ('connection', 'content-length', 'transfer-encoding'):self.send_header(key, value)
            self.send_header('Content-Length', str(len(data)));self.send_header('Connection', 'close');self.end_headers()
            self.wfile.write(data);self.wfile.flush()
        except OSError as error:
            record['transport_error'] = type(error).__name__;self.send_error(502)
        finally:
            connection.close();self.close_connection = True
            record['finished_ns'] = time.monotonic_ns()
            (root / (name + '.receipt.json')).write_text(json.dumps(record, indent=2) + '\n')
    def log_message(self, *_args):pass
server = http.server.HTTPServer(('127.0.0.1', int(sys.argv[1])), Handler)
signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
try:server.serve_forever(poll_interval=0.1)
finally:server.server_close()
