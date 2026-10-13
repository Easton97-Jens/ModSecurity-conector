"""Fixed controlled TLS upstream; persist counters only, never payloads."""
import argparse
import http.server
import json
import os
from pathlib import Path
import ssl
import threading
import time


class Server(http.server.ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = False


class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def log_message(self, *_args):
        pass

    def do_GET(self):
        self.serve()

    def do_POST(self):
        self.serve()

    def serve(self):
        self.connection.settimeout(5)
        size = self.headers.get('Content-Length', '0')
        if not size.isdigit() or int(size) > 33 or self.headers.get('Transfer-Encoding'):
            self.send_error(400)
            return
        # Drain the bounded body without retaining it in evidence.
        self.rfile.read(int(size))
        with self.server.lock:
            self.server.count += 1
            self.server.lease = self.server.lease or any(name.lower().startswith('x-msconnector-composite-') for name in self.headers)
            persist(self.server)
        if self.path == '/qualification/timeout':
            # One fixed route delays headers beyond the real companion's
            # five-second idle/read deadline. Other routes stay immediate.
            time.sleep(6.0)
        parallel = self.path == '/qualification/parallel'
        try:
            admitted = parallel_enter(self.server) if parallel else True
            self.send_response(200 if admitted else 503)
            self.send_header('Content-Length', '2')
            self.end_headers()
            self.wfile.write(b'ok')
        finally:
            if parallel:
                parallel_leave(self.server)


def parallel_enter(server):
    with server.lock:
        server.parallel['parallel_requests_seen'] += 1
        server.parallel['parallel_inflight'] += 1
        server.parallel['parallel_max_inflight'] = max(server.parallel['parallel_max_inflight'], server.parallel['parallel_inflight'])
        persist(server)
    try:
        # Actual upstream handlers must overlap. A client-side thread barrier
        # alone cannot prove that the host forwards requests concurrently.
        server.parallel_barrier.wait(timeout=2.0)
        passed = True
    except threading.BrokenBarrierError:
        passed = False
    with server.lock:
        key = 'parallel_barrier_passes' if passed else 'parallel_barrier_errors'
        server.parallel[key] += 1
        persist(server)
    return passed


def parallel_leave(server):
    with server.lock:
        server.parallel['parallel_inflight'] -= 1
        persist(server)


def persist(server):
    path = server.root / 'upstream-observation.json'
    temporary = server.root / 'upstream-observation.next'
    fd = os.open(temporary, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'w') as output:
        json.dump({'requests_seen': server.count, 'lease_header_observed': server.lease, **server.parallel}, output)
    os.replace(temporary, path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, required=True)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--cert', required=True)
    parser.add_argument('--key', required=True)
    args = parser.parse_args()
    server = Server(('127.0.0.1', args.port), Handler)
    server.root, server.count, server.lease = args.root, 0, False
    server.lock = threading.Lock()
    server.parallel = dict.fromkeys(('parallel_requests_seen', 'parallel_inflight', 'parallel_max_inflight', 'parallel_barrier_passes', 'parallel_barrier_errors'), 0)
    server.parallel_barrier = threading.Barrier(4)
    persist(server)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.load_cert_chain(args.cert, args.key)
    server.socket = context.wrap_socket(server.socket, server_side=True)
    try:
        server.serve_forever(poll_interval=0.1)
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
