#!/usr/bin/env python3
"""Case-driven backend for the existing isolated Apache lifecycle capture."""

import argparse
import base64
import hashlib
import http.server
import json
import os
from pathlib import Path
import threading
import time


MAX_BODY = 16 * 1024 * 1024


def content(item):
    data = base64.b64decode(item["data"], validate=True)
    if len(data) != item["bytes"] or hashlib.sha256(data).hexdigest() != item["sha256"]:
        raise ValueError("backend fixture byte identity mismatch")
    return data


def response_for(plan, path):
    """P3 response headers belong to the principal URI, never health controls."""
    principal_paths = [plan["request"]["path"]] + [item["request"]["path"]
        for item in plan.get("principal_request_variants", [])]
    if path in principal_paths:
        return plan["backend"]
    if path == "/i12-observer-control-before":
        return {"status": 200, "headers": [["Content-Type", "text/plain"]],
                "body": {"encoding": "base64", "data": "b2sK", "bytes": 3,
                    "sha256": hashlib.sha256(b"ok\n").hexdigest()},
                "chunks": [], "framing": "content_length", "barrier": None, "peer_fault": None}
    for control in plan["controls"]:
        if path == control["path"]:
            return {"status": control["expected_status"], "headers": control["backend_headers"],
                    "body": control["backend_body"], "chunks": [], "framing": "content_length",
                    "barrier": None, "peer_fault": None}
    return None


def read_body(stream, headers):
    transfer = headers.get_all("Transfer-Encoding", [])
    if transfer:
        if transfer != ["chunked"]:
            raise ValueError("unsupported backend transfer encoding")
        chunks, total = [], 0
        while True:
            line = stream.readline(128)
            if not line.endswith(b"\r\n"):
                raise ValueError("truncated backend chunk header")
            size = int(line.strip().split(b";", 1)[0], 16)
            if size < 0 or total + size > MAX_BODY:
                raise ValueError("backend body exceeds bound")
            if not size:
                if stream.readline(3) != b"\r\n":
                    raise ValueError("backend chunk trailers unsupported")
                return b"".join(chunks)
            data = stream.read(size)
            if len(data) != size or stream.read(2) != b"\r\n":
                raise ValueError("truncated backend chunk")
            chunks.append(data)
            total += size
    length = int(headers.get("Content-Length", "0"))
    if length < 0 or length > MAX_BODY:
        raise ValueError("backend body exceeds bound")
    data = stream.read(length)
    if len(data) != length:
        raise ValueError("truncated backend body")
    return data


def wait_for_client_barrier(selected, index, root, token, physical):
    barrier = selected.get("barrier")
    if barrier and barrier.get("after_chunk") == index + 1:
        physical({"kind": "barrier_wait", "request_id": token})
        release = root / "client-first-body-received.release"
        deadline = time.monotonic() + barrier["timeout_seconds"]
        while not release.exists() and time.monotonic() < deadline:
            time.sleep(0.01)
        physical({"kind": "barrier_release" if release.exists() else "barrier_timeout",
                  "request_id": token})
        if not release.exists():
            raise TimeoutError("client did not prove first body receipt before barrier timeout")


def serve(plan, root, port):
    lock = threading.Lock()

    def physical(item):
        item["monotonic_ns"] = time.monotonic_ns()
        item["pid"] = os.getpid()
        with lock, (root / "requests.jsonl").open("a", encoding="utf-8") as output:
            os.chmod(root / "requests.jsonl", 0o600)
            output.write(json.dumps(item, separators=(",", ":")) + "\n")
            output.flush()

    class Handler(http.server.BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *_args):
            pass

        def send_selected_response(self, selected, token):
            chunks = [content(x) for x in selected.get("chunks", [])]
            payload = content(selected["body"])
            if chunks and b"".join(chunks) != payload:
                raise ValueError("backend chunks do not equal declared body")
            if not chunks and payload:
                chunks = [payload]
            chunked = selected.get("framing") == "chunked"
            self.send_response(selected["status"])
            for name, value in selected["headers"]:
                if name.lower() not in ("content-length", "transfer-encoding", "connection"):
                    self.send_header(name, value)
            self.send_header("Transfer-Encoding" if chunked else "Content-Length",
                             "chunked" if chunked else str(len(payload)))
            self.end_headers()
            physical({"kind": "response_headers_write", "request_id": token})
            for index, chunk in enumerate(chunks):
                wire = ("%x\r\n" % len(chunk)).encode() + chunk + b"\r\n" if chunked else chunk
                self.wfile.write(wire)
                self.wfile.flush()
                physical({"kind": "write", "request_id": token, "chunk_index": index,
                          "bytes": len(chunk), "sha256": hashlib.sha256(chunk).hexdigest()})
                wait_for_client_barrier(selected, index, root, token, physical)
                time.sleep(selected.get("chunk_delay_seconds", 0))
            if chunked:
                self.wfile.write(b"0\r\n\r\n")
                self.wfile.flush()
            physical({"kind": "backend_eos_write", "request_id": token,
                      "body_bytes": len(payload), "body_sha256": hashlib.sha256(payload).hexdigest()})

        def do_POST(self):
            self.do_GET()

        def do_GET(self):
            token = self.headers.get("X-I12-ID", "")
            if not token or len(token) > 256 or not all(c.isascii() and (c.isalnum() or c in "-_") for c in token):
                self.send_error(400)
                return
            try:
                physical({"kind": "request_arrival", "request_id": token, "uri": self.path,
                          "method": self.command, "headers": list(self.headers.raw_items())})
                request_body = read_body(self.rfile, self.headers)
                physical({"kind": "request", "request_id": token, "uri": self.path,
                          "method": self.command, "headers": list(self.headers.raw_items()),
                          "body_bytes": len(request_body),
                          "body_sha256": hashlib.sha256(request_body).hexdigest()})
                selected = response_for(plan, self.path)
                if selected is None:
                    # Count an unexpected backend arrival before routing it.
                    # In particular an unblocked deny request must never look
                    # like backend exclusion merely because its URI is 404.
                    self.send_error(404)
                    return
                self.send_selected_response(selected, token)
            except (OSError, ValueError, TimeoutError) as error:
                physical({"kind": "backend_error", "request_id": token,
                          "type": type(error).__name__, "message": str(error)})
                self.close_connection = True

    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler)
    server.daemon_threads = True
    server.serve_forever()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    serve(json.loads(args.spec.read_text()), args.root, args.port)


if __name__ == "__main__":
    main()
