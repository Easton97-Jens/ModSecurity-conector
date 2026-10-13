#!/usr/bin/env python3
"""Three-generation native middleware diagnostics, never catalog promotion.

Reuses the native host fixture and generic Linux identity/cleanup utilities.
No results from the sibling forwardAuth or Envoy paths are consumed.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from dataclasses import replace
import hashlib
import http.client
import http.server
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import select
import signal
import socket
import stat
import subprocess
import sys
import threading
import time

REPO = Path(__file__).resolve().parents[3]
EXTERNAL = Path('/var/tmp/codex/ModSecurity-conector')


def load_module(name, relative):
    spec = importlib.util.spec_from_file_location(name, REPO / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


native = load_module('traefik_native_smoke_qualification', 'connectors/traefik/scripts/runtime_native_smoke.py')
linux = load_module('native_qualification_linux', 'connectors/envoy/harness/run_envoy_ext_proc_qualification.py')
InvalidEvidence = linux.InvalidEvidence
HEADER_DEADLINE_SECONDS = 4
HEADER_WIRE_LIMIT = 8192
CLIENT_BODY_LIMIT = 65536
ALLOW_PAYLOAD_SHA256 = 'e4f0bc4103f4272261f79eb3a2b6c17619e7d4ea33e46e4fbe4800f07e189e12'


class StrictHeaderStream(io.RawIOBase):
    """Reject response syntax that ``http.client`` would otherwise normalize."""

    def __init__(self, stream):
        super().__init__()
        self.stream = stream
        self.line_number = 0
        self.headers_complete = False

    def readable(self):
        return True

    def readinto(self, buffer):
        return self.stream.readinto(buffer)

    def readline(self, size=-1):
        line = self.stream.readline(size)
        if not self.headers_complete:
            if not line.endswith(b'\r\n') or b'\r' in line[:-2] or b'\n' in line[:-2]:
                raise InvalidEvidence('native client response requires exact CRLF')
            content = line[:-2]
            if self.line_number == 0:
                # This closed qualification fixture never emits informational
                # responses. Rejecting them also prevents a 1xx header block
                # from consuming the one strict-grammar validation window.
                if not re.fullmatch(rb'HTTP/1\.1 [2-5][0-9]{2}(?: [\x20-\x7e]*)?', content):
                    raise InvalidEvidence('native client response status line invalid')
            elif not content:
                self.headers_complete = True
            else:
                name, colon, value = content.partition(b':')
                if not colon or not re.fullmatch(rb"[!#$%&'*+.^_`|~0-9A-Za-z-]+", name) or \
                    any((byte < 0x20 and byte != 0x09) or byte == 0x7f for byte in value):
                    raise InvalidEvidence('native client response header grammar invalid')
            self.line_number += 1
        return line

    def fileno(self):
        return self.stream.fileno()

    def close(self):
        try:
            self.stream.close()
        finally:
            super().close()


class StrictResponseSocket:
    def __init__(self, connection):
        self.connection = connection

    def makefile(self, mode):
        return StrictHeaderStream(self.connection.makefile(mode, buffering=0))


class StrictHTTPResponse(http.client.HTTPResponse):
    def __init__(self, connection, *args, **kwargs):
        super().__init__(StrictResponseSocket(connection), *args, **kwargs)


def read_header_wire(handler):
    """Bound the complete first/subsequent request header, including CRLF."""
    wire = bytearray()
    deadline = time.monotonic() + HEADER_DEADLINE_SECONDS
    previous_timeout = handler.connection.gettimeout()
    try:
        while len(wire) < HEADER_WIRE_LIMIT:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise InvalidEvidence('upstream request header deadline')
            handler.connection.settimeout(remaining)
            byte = handler.rfile.read1(1)
            if not byte:
                if not wire:
                    return None
                raise InvalidEvidence('truncated upstream request headers')
            wire.extend(byte)
            if wire.endswith(b'\r\n\r\n'):
                raw = bytes(wire)
                residue = raw.replace(b'\r\n', b'')
                if b'\r' in residue or b'\n' in residue:
                    raise InvalidEvidence('upstream request header requires exact CRLF')
                return raw
        raise InvalidEvidence('upstream request header wire limit')
    except TimeoutError as error:
        raise InvalidEvidence('upstream_request_timeout') from error
    finally:
        handler.connection.settimeout(previous_timeout)


def immutable_process_identity(process):
    identity = linux.process_identity(process.pid)
    return {key: identity[key]
        for key in ('pid', 'start', 'exe', 'ppid', 'session')}


def verify_abort_processes(processes, before):
    if any(process.poll() is not None for process in processes):
        raise InvalidEvidence('native host/engine did not survive abort')
    if before != [immutable_process_identity(process) for process in processes]:
        raise InvalidEvidence('native host/engine identity changed after abort')


def source_manifest():
    paths = subprocess.check_output(['rtk', 'proxy', 'git', 'ls-files', '-z', '--',
        'common', 'connectors/traefik'], cwd=REPO).decode().split('\0')
    paths += ['connectors/traefik/harness/traefik_native_qualification.py',
        'connectors/envoy/harness/run_envoy_ext_proc_qualification.py']
    return {name: hashlib.sha256(linux.read_safe(REPO / name)).hexdigest()
        for name in sorted(set(paths)) if name}


def private_root(path):
    path = linux.checked_path(path)
    if not path.is_relative_to(EXTERNAL) or path == EXTERNAL:
        raise InvalidEvidence('campaign root must be a narrow external directory')
    info = path.stat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.geteuid() or \
        stat.S_IMODE(info.st_mode) != 0o700 or any(path.iterdir()):
        raise InvalidEvidence('campaign root must be empty, owned and 0700')
    return path


class Observer(http.server.ThreadingHTTPServer):
    """Track every native upstream header, completed handler and live socket."""
    daemon_threads = True

    def __init__(self, state):
        self.lock = threading.Lock()
        self.receipts = {}
        self.connections = set()
        self.connection_requests = {}
        self.accepted = self.active = self.peak = 0
        self.errors = []
        self.four = threading.Event()
        self.release = threading.Event()
        base = native.upstream_handler(state)

        class Handler(base):
            def handle_one_request(handler):
                wire = read_header_wire(handler)
                if wire is None:
                    handler.close_connection = True
                    return
                handler.raw_requestline, _, header = wire.partition(b'\r\n')
                handler.raw_requestline += b'\r\n'
                original = handler.rfile
                try:
                    handler.rfile = io.BytesIO(header)
                    handler.parse_request()
                finally:
                    handler.rfile = original
                handler.do_POST()
                handler.wfile.flush()

            def parse_request(handler):
                parsed = super().parse_request()
                if not parsed:
                    raise InvalidEvidence('invalid upstream HTTP request')
                if handler.command != 'POST' or handler.request_version != 'HTTP/1.1':
                    raise InvalidEvidence('unexpected upstream HTTP method/version')
                if handler.headers.defects or any('\r' in value or '\n' in value
                    for _, value in handler.headers.raw_items()) or \
                    len(handler.headers.get_all('Host', [])) != 1:
                    raise InvalidEvidence('invalid upstream HTTP headers')
                if parsed:
                    with self.lock:
                        self.connection_requests[handler.connection] += 1
                return parsed

            def do_POST(handler):  # noqa: N802
                identifiers = handler.headers.get_all('X-Request-Id', [])
                token = identifiers[0] if len(identifiers) == 1 else ''
                parallel = token.startswith('tnq-') and '-parallel-' in token
                with self.lock:
                    self.receipts.setdefault(token, {'headers': 0, 'completed': 0})['headers'] += 1
                    if parallel:
                        self.active += 1
                        self.peak = max(self.peak, self.active)
                        if self.active == 4:
                            self.four.set()
                try:
                    if parallel and not self.release.wait(10):
                        raise InvalidEvidence('four-client upstream barrier timed out')
                    if super().do_POST() is not True:
                        raise InvalidEvidence('upstream handler did not complete response')
                    with self.lock:
                        self.receipts[token]['completed'] += 1
                finally:
                    if parallel:
                        with self.lock:
                            self.active -= 1

            def finish(handler):
                try:
                    super().finish()
                finally:
                    with self.lock:
                        self.connections.discard(handler.connection)

        super().__init__(('127.0.0.1', 0), Handler)
        self.thread = threading.Thread(target=self.serve_forever, daemon=True)
        self.thread.start()

    def get_request(self):
        connection, address = super().get_request()
        connection.settimeout(12)
        with self.lock:
            self.accepted += 1
            self.connections.add(connection)
            self.connection_requests[connection] = 0
        return connection, address

    def handle_error(self, _request, _address):
        with self.lock:
            error = sys.exc_info()[1]
            self.errors.append(str(error) if isinstance(error, InvalidEvidence) else type(error).__name__)

    def close_observer(self):
        self.release.set()
        self.shutdown()
        queued = 0
        while select.select([self.socket], [], [], 0)[0]:
            connection, _address = self.socket.accept()
            queued += 1
            connection.close()
        with self.lock:
            connections = list(self.connections)
        for connection in connections:
            try:
                connection.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            connection.close()
        self.server_close()
        self.thread.join(2)
        deadline = time.monotonic() + 2
        while self.connections and time.monotonic() < deadline:
            time.sleep(.01)
        request_count = sum(self.connection_requests.values())
        if self.thread.is_alive() or self.connections or self.active or queued or self.errors or \
            len(self.connection_requests) != self.accepted or \
            any(count == 0 for count in self.connection_requests.values()) or \
            request_count != sum(receipt['headers'] for receipt in self.receipts.values()):
            raise InvalidEvidence('upstream queue, handler, socket or error survived reconciliation')
        return {'accepts': self.accepted, 'queued_accepts': queued,
            'requests_per_accept': list(self.connection_requests.values()),
            'active': self.active, 'peak': self.peak, 'errors': self.errors,
            'receipts': self.receipts}


def probe(connection, token, kind, expected):
    body = native.P2_BODY if kind == 'p2' else native.REQUEST_BODY
    headers = {'Content-Type': 'text/plain', 'X-Request-Id': token}
    if kind in ('p1', 'alt'):
        headers['X-Modsec-Smoke'] = 'block' if kind == 'p1' else 'alternative-status'
    if kind == 'p3':
        headers['X-Native-Response-Rule'] = 'block'
    connection.response_class = StrictHTTPResponse
    connection.request('POST', '/native', body=body, headers=headers)
    response = connection.getresponse()
    lengths = response.headers.get_all('Content-Length', [])
    if response.version != 11 or response.headers.defects or \
        any(not re.fullmatch(r"[!#$%&'*+.^_`|~0-9A-Za-z-]+", name) or
            '\r' in value or '\n' in value
            for name, value in response.headers.raw_items()) or \
        len(lengths) != 1 or not re.fullmatch(r'(?:0|[1-9][0-9]*)', lengths[0]) or \
        response.headers.get_all('Transfer-Encoding', []):
        raise InvalidEvidence('native client response framing invalid')
    declared = int(lengths[0])
    if declared > CLIENT_BODY_LIMIT:
        raise InvalidEvidence('native client response body exceeds bound')
    chunks = []
    remaining = declared
    while remaining:
        chunk = response.read(min(4096, remaining))
        if not chunk:
            break
        if len(chunk) > remaining:
            raise InvalidEvidence('native client response exceeded declared body')
        chunks.append(chunk)
        remaining -= len(chunk)
    if declared == 0 and response.read(0):
        raise InvalidEvidence('native client response exceeded declared body')
    payload = b''.join(chunks)
    digest = hashlib.sha256(payload).hexdigest()
    if response.status != expected or len(payload) != declared or not response.isclosed():
        raise InvalidEvidence('native client status/body contradicts probe')
    if kind == 'allow' and digest != ALLOW_PAYLOAD_SHA256:
        raise InvalidEvidence('native allow payload contradicts pinned upstream fixture')
    return {'transaction_id': token, 'kind': kind, 'status': response.status,
        'bytes': len(payload), 'content_length': declared, 'complete_eos': True,
        'body_sha256': digest}


def verify_receipts(observer, probes, safe_tokens, abort_token=None):
    expected = {entry['transaction_id']: int(entry['kind'] not in ('p1', 'alt', 'p2'))
        for entry in probes}
    expected.update({token: 1 for token in safe_tokens})
    if abort_token is not None:
        expected[abort_token] = 0
    actual = observer.receipts
    if set(actual) != {token for token, count in expected.items() if count}:
        raise InvalidEvidence('unexpected or missing upstream transaction')
    for token, count in expected.items():
        if actual.get(token, {'headers': 0, 'completed': 0}) != {'headers': count, 'completed': count}:
            raise InvalidEvidence('upstream header/completion count contradicts probe')
    if observer.peak != 4 or observer.active or observer.errors:
        raise InvalidEvidence('parallel overlap or upstream completion failed')


def verify_events(events, probes, rule_ids, safe_token, abort_token=None):
    """Require one decision then one correlated host receipt for each deny."""
    expected = {entry['transaction_id']: entry for entry in probes
        if entry['kind'] in ('p1', 'alt', 'p2', 'p3')}
    expected[safe_token] = {'kind': 'p4', 'status': 200}
    phases = {'p1': 'request_headers', 'alt': 'request_headers', 'p2': 'request_body',
        'p3': 'response_headers', 'p4': 'response_body'}
    rules = {**rule_ids, 'alt': rule_ids['p1_alternative']}
    states = {token: 0 for token in expected}
    sequences = {}
    previous_hash = 0
    abort_events = 0
    for event in events:
        if event.get('connector') != 'traefik' or event.get('integration_mode') != 'native-traefik-middleware':
            raise InvalidEvidence('foreign profile event')
        sequence = event.get('sequence')
        token = event.get('transaction_id')
        if type(token) is not str or not token or len(token) > 128 or \
            type(sequence) is not int or sequence != sequences.get(token, 0) + 1 or event.get('truncated') is not False:
            raise InvalidEvidence('event sequence/truncation invalid')
        # Common advances transaction->flow.sequence independently, while
        # runtime->previous_event_hash chains the complete emitted stream.
        # This checks linkage/counters, not cryptographic authenticity or a
        # recomputation of Common's ABI-dependent non-cryptographic event hash.
        for key in ('previous_event_hash', 'event_hash'):
            if type(event.get(key)) is not int or not 0 <= event[key] < 1 << 64:
                raise InvalidEvidence('invalid event hash field')
        if event['previous_event_hash'] != previous_hash:
            raise InvalidEvidence('broken Common runtime event hash linkage')
        previous_hash = event['event_hash']
        sequences[token] = sequence
        if abort_token is not None and token == abort_token:
            exact = {'sequence': 1, 'event': 'protocol_error',
                'message_id': 'MSCONN_EVENT_PROTOCOL_ERROR', 'phase': 'request_headers',
                'status': 'error', 'action': 'log_only', 'requested_action': 'log_only',
                'actual_action': 'log_only', 'http_status': 500,
                'original_http_status': 0, 'visible_http_status': 0,
                'transport_result': '', 'rule_id': '', 'response_started': False,
                'response_committed': False, 'headers_sent': False, 'body_started': False}
            exact.update({'body_bytes_seen': 0, 'body_bytes_inspected': 0,
                'late_intervention': False, 'body_truncated': False,
                'connection_aborted': False, 'client_disconnected': False,
                'upstream_disconnected': False, 'cancelled': False, 'eos_seen': False})
            if any(type(event.get(key)) is not type(value) or event[key] != value
                for key, value in exact.items()):
                raise InvalidEvidence('native abort protocol error contradiction')
            abort_events += 1
            continue
        if token not in expected:
            raise InvalidEvidence('unexpected native event transaction')
        entry = expected[token]
        kind = entry['kind']
        if states[token] not in (0, 1):
            raise InvalidEvidence('duplicate intervention decision or receipt')
        host = states[token] == 1
        if event.get('phase') != phases[kind] or \
            type(event.get('rule_id')) is not str or event['rule_id'] != rules[kind]:
            raise InvalidEvidence('intervention phase/rule mismatch')
        if event.get('sequence') != states[token] + 1:
            raise InvalidEvidence('duplicate/reversed/missing intervention decision or receipt')
        requested_status = 429 if kind == 'alt' else 403
        expected_transport = ('log_only' if kind == 'p4' else 'http_status') if host else ''
        expected_action = 'log_only' if host and kind == 'p4' else 'deny'
        expected_visible = entry['status'] if host else (200 if kind in ('p3', 'p4') else 0)
        response_started = kind == 'p4'
        body_bytes = len(native.P2_BODY) if kind == 'p2' else 55 if kind == 'p4' else 0
        response_event = kind in ('p3', 'p4')
        expected_fields = {
            'event': 'MSCONN_EVENT_RESPONSE_BLOCKED' if response_event else 'MSCONN_EVENT_REQUEST_BLOCKED',
            'message_id': 'MSCONN_EVENT_RESPONSE_BLOCKED' if response_event else 'MSCONN_EVENT_REQUEST_BLOCKED',
            'status': 'blocked', 'action': 'deny', 'requested_action': 'deny',
            'actual_action': expected_action, 'http_status': requested_status,
            'original_http_status': 200 if response_event else 0,
            'visible_http_status': expected_visible,
            'transport_result': expected_transport,
            'body_bytes_seen': body_bytes, 'body_bytes_inspected': body_bytes,
            'late_intervention': host and kind == 'p4',
            'response_started': response_started,
            'response_committed': response_started, 'headers_sent': response_started,
            'body_started': response_started, 'body_truncated': False,
            'connection_aborted': False, 'client_disconnected': False,
            'upstream_disconnected': False, 'cancelled': False, 'eos_seen': False,
        }
        if any(type(event.get(key)) is not type(value) or event[key] != value
            for key, value in expected_fields.items()):
            raise InvalidEvidence('native decision/host event semantics contradiction')
        if host and kind == 'p4':
            if event.get('late_intervention_mode') != 'safe':
                raise InvalidEvidence('native P4 host late-intervention mode contradiction')
        elif 'late_intervention_mode' in event:
            raise InvalidEvidence('unexpected native late-intervention mode')
        states[token] += 1
    if any(value != 2 for value in states.values()):
        raise InvalidEvidence('incomplete native decision/host receipt chain')
    if abort_token is not None and abort_events != 1:
        raise InvalidEvidence('missing/duplicate native abort protocol error')


def attach_process(process):
    try:
        process.qualification_identity = linux.process_identity(process.pid)
        process.qualification_tree = linux.ProcessTree(process.qualification_identity)
    except Exception:
        process.kill()
        process.wait(timeout=2)
        raise


def input_pins(args):
    return {name: linux.digest(getattr(args, name), getattr(args, name + '_sha256'))
        for name in ('traefik', 'engine', 'library', 'rules')}


def fatal_log_count(artifacts):
    return sum(sum(bool(re.search(r'\b(?:panic|fatal)\b|segmentation fault', line, re.IGNORECASE))
        for line in path.read_text(errors='replace').splitlines())
        for path in artifacts.logs_dir.glob('*.log'))


def verify_stopped_process(process, was_running):
    status = process.poll()
    if not was_running or status not in (0, -signal.SIGTERM):
        raise InvalidEvidence(f'native process exited unexpectedly: {status}')
    return status


def reconcile_adopted_and_logs(artifacts, result, cleanup_errors):
    # Descendants may inherit the runtime log descriptors. Reap them before
    # reading the final logs, including when root processes already exited.
    try:
        result['adopted_cleanup'] = linux.cleanup_adopted()
    except Exception as error:
        cleanup_errors.append(f'adopted native process reconciliation failed: {error}')
    try:
        result['final_fatal_log_lines'] = fatal_log_count(artifacts)
        if result['final_fatal_log_lines']:
            cleanup_errors.append('native fatal/panic log after final resource sample')
    except Exception as error:
        cleanup_errors.append(f'final native log reconciliation failed: {error}')


def resource_sample(processes, observer, artifacts):
    result = {name: linux.resources(process.pid) for name, process in
        (('host', processes.traefik), ('engine', processes.engine))}
    with observer.lock:
        result['fixture_errors'] = len(observer.errors)
    result['fatal_log_lines'] = fatal_log_count(artifacts)
    return result


def abort_probe(port, token):
    deadline = time.monotonic() + 4
    received = bytearray()
    with socket.create_connection(('127.0.0.1', port), timeout=2) as connection:
        connection.sendall(f'POST /native HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\nContent-Length: 2048\r\nX-Request-Id: {token}\r\n\r\nx'.encode())
        connection.shutdown(socket.SHUT_WR)
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise InvalidEvidence('native incomplete-body abort did not close before deadline')
            connection.settimeout(remaining)
            chunk = connection.recv(4096)
            if not chunk:
                verify_abort_response(bytes(received))
                return {'transaction_id': token, 'declared_bytes': 2048, 'sent_bytes': 1,
                    'write_half_closed': True, 'host_closed_connection': True,
                    'status': 500, 'response_bytes': len(received)}
            received.extend(chunk)
            if len(received) > 65536:
                raise InvalidEvidence('unbounded abort response')


def verify_abort_response(response):
    header, separator, body = response.partition(b'\r\n\r\n')
    if not separator or len(header) > 4096:
        raise InvalidEvidence('native abort response header framing invalid')
    lines = header.split(b'\r\n')
    if not re.fullmatch(rb'HTTP/1\.1 500 [^\r\n]+', lines[0]):
        raise InvalidEvidence('native abort response must be HTTP/1.1 500')
    headers = {}
    for line in lines[1:]:
        key, colon, value = line.partition(b':')
        if not colon or not re.fullmatch(rb'[A-Za-z0-9-]+', key):
            raise InvalidEvidence('native abort response header invalid')
        headers.setdefault(key.lower(), []).append(value.strip())
    lengths = headers.get(b'content-length', [])
    if len(lengths) != 1 or not re.fullmatch(rb'[0-9]+', lengths[0]) or \
        int(lengths[0]) != len(body) or b'transfer-encoding' in headers or \
        headers.get(b'connection') != [b'close']:
        raise InvalidEvidence('native abort response framing/close invalid')


def run_generation(args, root, index, pins):
    directory = root / f'start-{index}'
    socket_parent = args.socket_parent
    parent = native.EngineSocketParent(socket_parent, native.private_directory_identity(socket_parent, 'qualification UDS parent'))
    inputs = native.NativeRuntimeInputs(directory, parent, None, None, args.traefik,
        args.include, args.library.parent, args.rules, native.STANDALONE_RULE_IDS,
        'standalone-host-probe', native.read_plugin_module(native.PLUGIN_SOURCE))
    artifacts = native.stage_native_runtime(inputs)
    setup = None
    observer = None
    try:
        setup = native.start_native_runtime_setup(inputs, artifacts)
        setup.upstream.shutdown()
        setup.upstream.server_close()
        observer = Observer(setup.state)
        setup = replace(setup, upstream=observer, upstream_port=observer.server_port)
        native.write_dynamic_config(artifacts.dynamic_config, setup.upstream_port, setup.engine_socket)
    except Exception:
        if observer is not None:
            observer.close_observer()
        if setup is not None:
            native.remove_private_engine_socket_dir(setup.engine_socket_dir, parent)
        native.cleanup_staged_runtime_workspaces(inputs, artifacts)
        raise
    processes = native.NativeProcesses()
    result = {'generation': index, 'status': 'FAIL', 'catalog_acceptance': False}
    probes = []
    token_prefix = f'tnq-{index}'
    safe_tokens = [f'{token_prefix}-p4', f'{token_prefix}-safe-followup']
    abort_token = f'{token_prefix}-abort'
    try:
        result['inputs_before'] = input_pins(args)
        if result['inputs_before'] != pins:
            raise InvalidEvidence('native input pin changed before generation')
        with native.running_traefik_host(inputs, artifacts, setup, processes,
            engine_description='pinned native UDS engine', host_description='native middleware host',
            engine_binary=args.engine, process_started=attach_process):
            result['processes'] = [process.qualification_identity for process in (processes.traefik, processes.engine)]
            linux.executable_identity(processes.traefik.pid, args.traefik, args.traefik_sha256)
            linux.executable_identity(processes.engine.pid, args.engine, args.engine_sha256)
            result['loaded_library'] = linux.loaded_library(processes.engine.pid, pins['library'])
            sample = lambda: resource_sample(processes, observer, artifacts)
            result['resources'] = {'before': sample()}
            for kind, status in (('allow', 200), ('p1', 403), ('alt', 429), ('p2', 403), ('p3', 403)):
                with closing(http.client.HTTPConnection('127.0.0.1', setup.traefik_port, timeout=12)) as connection:
                    probes.append(probe(connection, f'{token_prefix}-{kind}', kind, status))
            result['safe'] = native.synchronized_safe_followup(setup.traefik_port, setup.state,
                native.REQUEST_BODY, *safe_tokens, response_class=StrictHTTPResponse)
            if result['safe'].get('connection_reused') is not True or result['safe'].get('followup_status') != 200:
                raise InvalidEvidence('P4 Safe followup failed')
            with closing(http.client.HTTPConnection('127.0.0.1', setup.traefik_port, timeout=12)) as connection:
                connection.connect()
                original = connection.sock
                for number, kind in enumerate(('allow', 'p1', 'allow', 'p2', 'allow')):
                    probes.append(probe(connection, f'{token_prefix}-keep-{number}', kind, 200 if kind == 'allow' else 403))
                    if connection.sock is not original:
                        raise InvalidEvidence('alternating keepalive connection replaced')
            # Incomplete body followed by FIN exercises client-abort handling.
            before_abort = [immutable_process_identity(process)
                for process in (processes.traefik, processes.engine)]
            abort_error = None
            try:
                result['abort'] = abort_probe(setup.traefik_port, abort_token)
            except Exception as error:
                abort_error = error
                result['abort'] = {'transaction_id': abort_token,
                    'error': f'{type(error).__name__}: {error}'}
            with closing(http.client.HTTPConnection('127.0.0.1', setup.traefik_port, timeout=12)) as connection:
                probes.append(probe(connection, f'{token_prefix}-abort-followup', 'allow', 200))
            verify_abort_processes((processes.traefik, processes.engine), before_abort)
            result['abort']['same_process_followup'] = True
            if abort_error is not None:
                raise abort_error
            def parallel(number):
                with closing(http.client.HTTPConnection('127.0.0.1', setup.traefik_port, timeout=12)) as connection:
                    return probe(connection, f'{token_prefix}-parallel-{number}', 'allow', 200)
            with ThreadPoolExecutor(max_workers=4) as pool:
                futures = [pool.submit(parallel, number) for number in range(4)]
                try:
                    if not observer.four.wait(10):
                        raise InvalidEvidence('four requests did not overlap at native upstream')
                    result['resources']['peak'] = sample()
                finally:
                    observer.release.set()
                probes += [future.result() for future in futures]
            result['resources']['after'] = sample()
            if any(observation['fixture_errors'] or observation['fatal_log_lines']
                for observation in result['resources'].values()):
                raise InvalidEvidence('native runtime error observed in resource samples')
            result['probes'] = probes
            linux.loaded_library(processes.engine.pid, pins['library'])
            result['inputs_after'] = input_pins(args)
            if result['inputs_after'] != pins:
                raise InvalidEvidence('native input pin changed during generation')
        result['status'] = 'PASS'
    except Exception as error:
        result['error'] = f'{type(error).__name__}: {error}'
    finally:
        cleanup_errors = []
        result['final_exit_statuses'] = []
        for process in (processes.traefik, processes.engine):
            if process is not None:
                try:
                    was_running = process.poll() is None
                    linux.stop_process(process)
                    result['final_exit_statuses'].append(verify_stopped_process(process, was_running))
                except Exception as error:
                    cleanup_errors.append(str(error))
        reconcile_adopted_and_logs(artifacts, result, cleanup_errors)
        try:
            result['upstream'] = observer.close_observer()
            if result['status'] == 'PASS':
                verify_receipts(observer, probes, safe_tokens, abort_token)
                verify_events(linux.jsonl(artifacts.event_path), probes, inputs.rule_ids, safe_tokens[0], abort_token)
        except Exception as error:
            cleanup_errors.append(str(error))
        if not native.remove_private_engine_socket_dir(setup.engine_socket_dir, parent) or \
            not native.cleanup_staged_runtime_workspaces(inputs, artifacts):
            cleanup_errors.append('UDS/workspace cleanup refused')
        if any(socket_parent.iterdir()):
            cleanup_errors.append('UDS parent not empty')
        for port in (setup.traefik_port, setup.upstream_port):
            with socket.socket() as connection:
                if connection.connect_ex(('127.0.0.1', port)) == 0:
                    cleanup_errors.append('listener survived cleanup')
        result['cleanup'] = {'passed': not cleanup_errors, 'errors': cleanup_errors}
        if cleanup_errors:
            result['status'] = 'FAIL'
        native.write_json(directory / 'qualification.json', result)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--socket-parent', type=Path, required=True,
        help='Existing empty 0700 narrow external parent, short enough for sockaddr_un')
    for name in ('traefik', 'engine', 'library', 'rules'):
        parser.add_argument(f'--{name}', type=Path, required=True)
        parser.add_argument(f'--{name}-sha256', required=True)
    parser.add_argument('--include', type=Path, required=True)
    args = parser.parse_args(argv)
    root = private_root(args.root)
    private_root(args.socket_parent)
    if args.root == args.socket_parent or args.socket_parent.is_relative_to(args.root) or args.root.is_relative_to(args.socket_parent):
        raise InvalidEvidence('campaign and UDS roots must be disjoint')
    native.assert_private_engine_socket_parent(args.socket_parent, 'qualification UDS parent')
    native.assert_engine_socket_path_length(args.socket_parent)
    pins = input_pins(args)
    # Only the closed standalone fixture is permitted: no unpinned Include graph.
    if linux.read_safe(args.rules) != linux.read_safe(native.STANDALONE_ENGINE_RULES):
        raise InvalidEvidence('qualification requires exact standalone native rule fixture')
    before = source_manifest()
    linux.enable_subreaper()
    starts = []
    for index in range(1, 4):
        try:
            starts.append(run_generation(args, root, index, pins))
        except Exception as error:
            starts.append({'generation': index, 'status': 'FAIL',
                'error': f'{type(error).__name__}: {error}', 'catalog_acceptance': False})
            break
    after = source_manifest()
    pin_error = None
    try:
        stable = before == after and pins == input_pins(args)
    except Exception as error:
        stable = False
        pin_error = f'{type(error).__name__}: {error}'
    identities = [tuple((process['pid'], process['start']) for process in start.get('processes', [])) for start in starts]
    success = stable and len(starts) == 3 and len(set(identities)) == 3 and all(start['status'] == 'PASS' for start in starts)
    result = {'status': 'PASS' if success else 'FAIL', 'profile': 'traefik-native-middleware',
        'catalog_acceptance': False, 'gates': ['G2', 'G5', 'G6'], 'starts': starts,
        'inputs': pins, 'source_before': before, 'source_after': after, 'inputs_stable': stable,
        'final_input_error': pin_error,
        'gaps': ['Full G1–G9 catalog acceptance', 'P4 strict post-commit enforcement', 'Production traffic validation']}
    native.write_json(root / 'result.json', result)
    return 0 if success else 1


if __name__ == '__main__':
    raise SystemExit(main())
