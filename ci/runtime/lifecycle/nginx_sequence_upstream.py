"""Own bounded upstream: release the marker only after client sees headers."""
from __future__ import annotations

import socketserver
import threading

PREFIX = b"owned-prefix\n" * 400
SUFFIX = b"no-crs-response-body-marker\n" + b"owned-suffix\n" * 400


class _Handler(socketserver.StreamRequestHandler):
    def handle(self):
        first = self.rfile.readline(4096)
        if not first or len(first) == 4096:
            return
        while True:
            line = self.rfile.readline(4096)
            if not line or len(line) == 4096:
                return
            if line == b"\r\n":
                break
        path = first.split(b" ", 2)[1]
        late = path.endswith(b"/0")
        prefix = PREFIX * 40 if self.server.backpressure else PREFIX
        body = prefix + SUFFIX if late else b"owned-followup\n"
        framing = b"Transfer-Encoding: chunked" if late else b"Content-Length: " + str(len(body)).encode()
        header = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n" + framing + b"\r\nConnection: close\r\n\r\n"
        try:
            prefix_wire = format(len(prefix), "x").encode() + b"\r\n" + prefix + b"\r\n"
            self.wfile.write(header + (prefix_wire if late else body))
            self.wfile.flush()
            if late:
                self.server.prefix_sent.set()
                if not self.server.client_headers_seen.wait(timeout=5):
                    self.server.barrier_timeout = True
                    return
                self.wfile.write(format(len(SUFFIX), "x").encode() + b"\r\n" + SUFFIX + b"\r\n0\r\n\r\n")
                self.wfile.flush()
                self.server.marker_sent.set()
        except OSError:
            self.server.upstream_write_failed = True


class SynchronizedUpstream:
    def __init__(self, *, backpressure=False):
        self.server = socketserver.ThreadingTCPServer(("127.0.0.1", 0), _Handler)
        self.server.daemon_threads = True
        self.server.prefix_sent = threading.Event()
        self.server.client_headers_seen = threading.Event()
        self.server.marker_sent = threading.Event()
        self.server.barrier_timeout = False
        self.server.upstream_write_failed = False
        self.server.backpressure = backpressure
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    @property
    def port(self):
        return self.server.server_address[1]

    def start(self):
        self.thread.start()

    def headers_seen(self, index):
        if index == 0:
            if not self.server.prefix_sent.is_set():
                raise ValueError("client headers preceded the upstream prefix")
            self.server.client_headers_seen.set()

    def observation(self):
        return {"prefix_sent": self.server.prefix_sent.is_set(),
                "client_headers_seen": self.server.client_headers_seen.is_set(),
                "marker_sent": self.server.marker_sent.is_set(),
                "barrier_timeout": self.server.barrier_timeout,
                "upstream_write_failed": self.server.upstream_write_failed}

    def stop(self):
        self.server.client_headers_seen.set()
        if self.thread.is_alive():
            self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
