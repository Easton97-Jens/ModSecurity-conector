"""Independent HTTP backend: connection/header arrivals precede body reads."""
import hashlib
import argparse
import http.server
import json
import os
from pathlib import Path
import signal
import socketserver
import sys
import threading
import time

MAX_BODY = 8 * 1024 * 1024
LOCK = threading.Lock()
LOOPBACK = '127.0.0.1'
MANIFEST = '/mnt/fixtures/acceptance-manifest.json'


def manifest_cases(value):
    if value != MANIFEST or Path(value).resolve(strict=True) != Path(MANIFEST):
        raise ValueError('sealed physical acceptance manifest required')
    return json.loads(Path(MANIFEST).read_text())


def bounded_port(value):
    port = int(value)
    if not 1 <= port <= 65535:
        raise ValueError('bounded loopback port required')
    return port


def record(root, value):
    value = value | {'pid': os.getpid(), 'monotonic_ns': time.monotonic_ns()}
    with LOCK, (root / 'receipts.jsonl').open('a') as stream:
        stream.write(json.dumps(value) + '\n')


class Backend(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    block_on_close = True

    def get_request(self):
        connection, address = super().get_request()
        if address[0] != LOOPBACK:
            connection.close()
            raise OSError('only isolated loopback clients are admitted')
        record(self.root, {'operation': 'accept', 'peer': list(address), 'socket_fd': connection.fileno()})
        connection.settimeout(12)
        return connection, address


def response_fixture(case, key, neighbor):
    if neighbor:
        return {'status': 200, 'headers': [['Content-Type', 'text/plain']],
                'body_hex': b'independent-healthy-neighbor\n'.hex(), 'chunk_lengths': [7, 12, 10]}, 'independent_neighbor'
    if key.startswith(('main-before-', 'main-after-')) and 'main_control_backend' in case['fixture']:
        return case['fixture']['main_control_backend'], 'explicit_main_control_override'
    return case['fixture']['backend'], 'original_target_fixture'


class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def read_chunked_body(self, body):
        while True:
            line = self.rfile.readline(128)
            if not line:
                raise EOFError('EOF before chunk size')
            size = int(line.split(b';', 1)[0].strip(), 16)
            if size == 0:
                if self.rfile.readline(4096) != b'\r\n':
                    raise ValueError('unsupported trailers')
                return
            if size < 0 or size > MAX_BODY or len(body) + size > MAX_BODY:
                raise ValueError('bounded backend body exceeded')
            part = self.rfile.read(size)
            body.extend(part)
            if len(part) != size or self.rfile.read(2) != b'\r\n':
                raise EOFError('incomplete body chunk')

    def read_sized_body(self, body):
        size = int(self.headers.get('Content-Length', '0'))
        if not 0 <= size <= MAX_BODY:
            raise ValueError('bounded backend body exceeded')
        while len(body) < size:
            part = self.rfile.read(min(8192, size - len(body)))
            if not part:
                raise EOFError('incomplete content length')
            body.extend(part)

    def read_body(self, key):
        body = bytearray()
        try:
            if self.headers.get('Transfer-Encoding', '').lower() == 'chunked':
                self.read_chunked_body(body)
            else:
                self.read_sized_body(body)
            record(self.server.root, {'operation': 'body-complete', 'key': key,
                'body_bytes': len(body), 'body_sha256': hashlib.sha256(body).hexdigest()})
            return bytes(body)
        except (OSError, EOFError, ValueError) as error:
            record(self.server.root, {'operation': 'body-incomplete', 'key': key,
                'body_bytes': len(body), 'body_sha256': hashlib.sha256(body).hexdigest(),
                'error': type(error).__name__, 'detail': str(error)[:256]})
            raise
        finally:
            (self.server.root / (key + '.request-body.raw')).write_bytes(body)

    def wait_barrier(self, key):
        marker = self.server.barriers / key
        record(self.server.root, {'operation': 'upstream-barrier-enter', 'key': key})
        deadline = time.monotonic() + 10
        while not marker.exists() and time.monotonic() < deadline:
            time.sleep(0.01)
        if not marker.exists():
            raise TimeoutError('client did not observe prefix before upstream release')
        record(self.server.root, {'operation': 'upstream-barrier-release', 'key': key,
            'client_marker_sha256': hashlib.sha256(marker.read_bytes()).hexdigest()})

    def write_body(self, key, fixture, body):
        position = 0
        for index, size in enumerate(fixture['chunk_lengths']):
            piece = body[position:position + size]
            if len(piece) != size:
                raise ValueError('response fixture chunk mismatch')
            self.wfile.write(piece)
            self.wfile.flush()
            position += size
            record(self.server.root, {'operation': 'response-chunk-flushed', 'key': key,
                'index': index, 'bytes': size, 'sha256': hashlib.sha256(piece).hexdigest()})
            if index == 0 and fixture.get('barrier'):
                self.wait_barrier(key)
            time.sleep(0.15 if len(body) < 65536 else 0.01)
        if position != len(body):
            raise ValueError('response fixture not exhausted')
        record(self.server.root, {'operation': 'response-complete', 'key': key,
            'body_bytes': position, 'body_sha256': hashlib.sha256(body).hexdigest()})

    def handle_request(self):
        key = self.headers.get('X-I12-Acceptance-Key', '')
        neighbor = key.startswith('neighbor-')
        lookup = key.removeprefix('neighbor-').removeprefix('main-before-').removeprefix('main-after-')
        for index in range(10):
            lookup = lookup.removeprefix('readiness-' + str(index) + '-')
        for index in range(3):
            lookup = lookup.removeprefix('sequence-' + str(index) + '-')
        if lookup not in self.server.cases:
            self.send_error(400)
            return
        case = self.server.cases[lookup]
        record(self.server.root, {'operation': 'headers-arrived', 'key': key, 'method': self.command,
            'path': self.path[:8192], 'request_id': self.headers.get('X-Request-Id'),
            'headers': list(self.headers.items()), 'peer': list(self.client_address)})
        try:
            self.read_body(key)
            fixture, selection = response_fixture(case, key, neighbor)
            body = bytes.fromhex(fixture['body_hex'])
            record(self.server.root, {'operation': 'response-fixture-selected', 'key': key,
                'selection': selection, 'body_bytes': len(body), 'body_sha256': hashlib.sha256(body).hexdigest(),
                'override_reason': case['fixture'].get('main_control_override_reason') if selection == 'explicit_main_control_override' else None})
            (self.server.root / (key + '.response-body.raw')).write_bytes(body)
            self.send_response(fixture['status'])
            for name, value in fixture['headers']:
                self.send_header(name, value)
            # Missing Content-Type fixture must not silently gain one.
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Connection', 'close')
            self.end_headers()
            record(self.server.root, {'operation': 'response-headers-flushed', 'key': key,
                                      'status': fixture['status'], 'declared_bytes': len(body)})
            self.write_body(key, fixture, body)
        except (OSError, EOFError, ValueError) as error:
            record(self.server.root, {'operation': 'handler-error', 'key': key,
                                      'error': type(error).__name__, 'detail': str(error)[:256]})
        finally:
            self.close_connection = True
            record(self.server.root, {'operation': 'handler-end', 'key': key})

    do_GET = handle_request
    do_POST = handle_request
    do_PUT = handle_request

    def log_message(self, *_):
        # Structured append-only records above replace unbound stderr logging.
        return


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('port', type=bounded_port)
    parser.add_argument('manifest', choices=(MANIFEST,))
    args = parser.parse_args()
    specification = manifest_cases(args.manifest)
    root = Path('/task/backend')
    root.mkdir(mode=0o700)
    server = Backend((LOOPBACK, args.port), Handler)
    server.root = root
    server.barriers = Path('/task/barriers')
    server.barriers.mkdir(mode=0o700)
    server.cases = {c['key']: c for c in specification['cases'] + specification.get('supplementary_executions', [])}
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    try:
        server.serve_forever(poll_interval=0.1)
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
