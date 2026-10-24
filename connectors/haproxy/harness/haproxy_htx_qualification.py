#!/usr/bin/env python3
"""Fail-closed native HTX delayed-P2 prerequisite, not a full B qualification.

Use an existing pinned overlay binary, its expected digest, and the canonical
No-CRS rules with their expected digest. The deliberately incomplete request
body gives the forward-first host time to dispatch before P2/EOS. Even an
accepted backend connection fails this prerequisite. No alternate filter or
buffering directive is introduced in the default streaming diagnostic. The
explicit host-buffered candidate requires header-stage native EOM inspection.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import signal
import socket
import socketserver
import stat as stat_module
import subprocess
import sys
import threading
import time

from runtime_artifacts import artifact_path, read_text, verified_runtime_root, write_text_atomic
from runtime_path_utils import open_runtime_artifact_parent
from haproxy_htx_smoke_helper import canonical_rules_content

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from connectors.composite_harness.qualification import (
    Child, Monitor, mounted_device_for_path, owned_sockets, read_response, surviving_descendants,
)

REQUEST_ID = 'htx-qualification-p2'
HOST_TRANSACTION_ID = r'haproxy-htx-[0-9]+'
P2_BODY = b'no-crs-request-body-marker'
LIMIT = 65536
TIMEOUT = 5.0


def assess(status: int | None, backend: dict, decision: bool) -> list[str]:
    issues = []
    if status != 403:
        issues.append('client_status_not_403')
    if not decision:
        issues.append('missing_unique_correlated_native_p2_rule')
    for key in ('accepts', 'complete_headers', 'body_bytes', 'request_completed', 'parse_errors'):
        if type(backend.get(key)) is not int or backend[key] != 0:
            issues.append('backend_' + key)
    return issues


def native_decision_id(text: str) -> str | None:
    pattern = (r'modsecurity-htx: request-body intervention observed; '
               rf'transaction_id=({HOST_TRANSACTION_ID}) phase=2 status=403 rule_id=1100101 action=deny')
    matches = re.findall(pattern + r'(?=\r?$)', text, re.MULTILINE)
    return matches[0] if len(matches) == 1 and text.count(
        'request-body intervention observed;'
    ) == 1 else None


def valid_decision(text: str) -> bool:
    return native_decision_id(text) is not None


def config(front: int, back: int, rules: Path, request_mode: str = 'streaming') -> str:
    if request_mode not in ('streaming', 'host-buffered'):
        raise ValueError('unknown request mode')
    if not re.fullmatch(r'/[A-Za-z0-9_./-]+', str(rules)):
        raise ValueError('rules path must use the absolute ASCII path allowlist')
    tuning = '    tune.bufsize 131072\n' if request_mode == 'host-buffered' else ''
    buffering = ('    option http-buffer-request\n    timeout http-request 5s\n'
                 if request_mode == 'host-buffered' else '')
    mode_option = ' request-body-mode host-buffered' if request_mode == 'host-buffered' else ''
    return f'''global
    log stdout format raw local0
    nbthread 1
{tuning}defaults
    mode http
    timeout connect 2s
    timeout client 5s
    timeout server 5s
{buffering}frontend htx_in
    bind 127.0.0.1:{front}
    filter modsecurity-htx rules-file {rules} phase4-mode safe{mode_option}
    default_backend htx_upstream
backend htx_upstream
    server upstream 127.0.0.1:{back}
'''


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(LIMIT), b''):
            h.update(chunk)
    return h.hexdigest()


def verified_input(path: str, expected: str, maximum: int) -> Path:
    target = Path(path)
    if not target.is_absolute() or target.is_symlink() or not target.is_file():
        raise ValueError('input must be an absolute regular non-symlink file')
    if not re.fullmatch('[0-9a-f]{64}', expected) or target.stat().st_size > maximum:
        raise ValueError('invalid input digest or size')
    if digest(target) != expected:
        raise ValueError('input digest mismatch')
    return target


def pinned_rules(path, expected, pin=None, root=None):
    """Read bounded rules through no-follow descriptors and bind file identity."""
    path = Path(path)
    if not path.is_absolute() or '..' in path.parts or not re.fullmatch('[0-9a-f]{64}', expected):
        raise ValueError('invalid pinned rules path or digest')
    parent = os.open('/', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for component in path.parts[1:-1]:
            next_parent = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent)
            os.close(parent)
            parent = next_parent
        fd = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
        try:
            before = os.fstat(fd)
            def identity(details):
                return (details.st_dev, details.st_ino, details.st_mode, details.st_uid,
                        details.st_gid, details.st_nlink, details.st_size,
                        details.st_mtime_ns, details.st_ctime_ns)
            current = identity(before)
            if (not stat_module.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                    before.st_size > LIMIT or (pin is not None and current != pin)):
                raise ValueError('pinned rules identity or size changed')
            with os.fdopen(os.dup(fd), 'rb') as stream:
                content = stream.read(LIMIT + 1)
            if (len(content) > LIMIT or hashlib.sha256(content).hexdigest() != expected or
                    identity(os.fstat(fd)) != current or
                    identity(os.stat(path.name, dir_fd=parent, follow_symlinks=False)) != current):
                raise ValueError('pinned rules changed during read or digest mismatch')
        finally:
            os.close(fd)
    finally:
        os.close(parent)
    text = content.decode('utf-8')
    if root is not None and read_text(root, path, 'pinned rules') != text:
        raise ValueError('private rules changed during validation')
    if root is not None:
        pinned_rules(path, expected, current)
    return text, current


def copy_campaign_rules(root, source, expected, source_pin=None):
    text, source_pin = pinned_rules(source, expected, source_pin)
    destination = root / 'rules.conf'
    if destination.exists() or destination.is_symlink():
        raise ValueError('campaign rules copy must be fresh')
    write_text_atomic(root, destination, text, 'campaign pinned rules')
    _, destination_pin = pinned_rules(destination, expected, root=root)
    canonical_rules_content(root, str(destination))
    pinned_rules(destination, expected, destination_pin, root)
    pinned_rules(source, expected, source_pin)
    return destination, source_pin, destination_pin


def check_campaign_rules(args):
    pinned_rules(args.rules, args.rules_sha256, args.rules_source_pin)
    pinned_rules(args.rules_path, args.rules_sha256, args.rules_pin, args.campaign_root)
    for root, path, pin in args.start_rules_pins:
        pinned_rules(path, args.rules_sha256, pin, root)


def campaign_parallel_probe(args, front, token):
    check_campaign_rules(args)
    return campaign_probe(front, 'parallel', token)


class Backend:
    """Independent backend observer; never retains headers or request bodies."""

    def __init__(self):
        self.listener = socket.socket()
        self.listener.bind(('127.0.0.1', 0))
        self.listener.listen(4)
        self.listener.settimeout(0.1)
        self.port = self.listener.getsockname()[1]
        self.drained = threading.Event()
        self.drain_error = None
        self.barrier_address = None
        self.barrier_accepted = False
        self.lock = threading.Lock()
        self.observed = dict.fromkeys(('accepts', 'complete_headers', 'body_bytes',
                                       'request_completed', 'parse_errors'), 0)
        self.observed['request_id_matches'] = False
        self.thread = threading.Thread(target=self.serve, daemon=False)

    def snapshot(self):
        with self.lock:
            return dict(self.observed)

    def add(self, key: str, value: int = 1):
        with self.lock:
            self.observed[key] += value

    def serve(self):
        try:
            self.observe()
        except Exception as exc:
            self.drain_error = type(exc).__name__
        finally:
            self.listener.close()
            self.drained.set()

    def observe(self):
        while True:
            try:
                connection, address = self.listener.accept()
            except BlockingIOError:
                # Only reached after the queue barrier was accepted. The host
                # has been reaped before the barrier is submitted, so it can
                # no longer enqueue another backend connection.
                return
            except socket.timeout:
                continue
            except OSError:
                self.drain_error = 'listener_accept_error'
                return
            with self.lock:
                is_barrier = address == self.barrier_address
            if is_barrier:
                connection.close()
                self.barrier_accepted = True
                self.listener.setblocking(False)
                continue
            self.add('accepts')
            with connection:
                connection.settimeout(0.1)
                header = b''
                length = None
                body_count = 0
                deadline = time.monotonic() + TIMEOUT
                while time.monotonic() < deadline:
                    try:
                        chunk = connection.recv(4096)
                    except socket.timeout:
                        continue
                    except OSError:
                        break
                    if not chunk:
                        break
                    if length is None:
                        header += chunk
                        if len(header) > LIMIT:
                            self.add('parse_errors')
                            break
                        if b'\r\n\r\n' not in header:
                            continue
                        raw_header, chunk = header.split(b'\r\n\r\n', 1)
                        header = b''
                        self.add('complete_headers')
                        try:
                            lines = raw_header.decode('ascii').split('\r\n')
                            fields = [line.split(':', 1) for line in lines[1:]]
                            lengths = [v.strip() for k, v in fields if k.lower() == 'content-length']
                            if lengths != [str(len(P2_BODY))]:
                                raise ValueError('unexpected length')
                            length = int(lengths[0])
                            ids = [v.strip() for k, v in fields if k.lower() == 'x-request-id']
                            with self.lock:
                                self.observed['request_id_matches'] = ids == [REQUEST_ID]
                        except (ValueError, UnicodeError):
                            self.add('parse_errors')
                            break
                    body_count += len(chunk)
                    self.add('body_bytes', len(chunk))
                    if body_count > length:
                        self.add('parse_errors')
                        break
                    if body_count == length:
                        self.add('request_completed')
                        # Respond only after request completion, so early P3
                        # cannot turn the intended P2 probe into a phase error.
                        try:
                            connection.sendall(b'HTTP/1.1 200 OK\r\nContent-Length: 2\r\nConnection: close\r\n\r\nOK')
                        except OSError:
                            pass
                        break
                else:
                    self.drain_error = 'backend_read_deadline'

    def close(self):
        """Drain after the sole producer has been reaped, then close listener.

        A real queue barrier makes delayed observer scheduling harmless. The
        observer accepts all preceding connections, acknowledges the barrier,
        drains remaining accepts to EAGAIN and closes its own listener.
        """
        with socket.socket() as barrier:
            barrier.bind(('127.0.0.1', 0))
            with self.lock:
                self.barrier_address = barrier.getsockname()
            barrier.settimeout(TIMEOUT)
            try:
                barrier.connect(('127.0.0.1', self.port))
            except OSError:
                self.drain_error = 'queue_barrier_connect_failed'
        if not self.drained.wait(TIMEOUT * 2):
            self.drain_error = 'queue_drain_timeout'
            self.listener.close()
        self.thread.join(TIMEOUT + 1)
        if self.thread.is_alive() or not self.barrier_accepted or self.drain_error:
            raise RuntimeError('backend drain not proven: ' + str(self.drain_error))


def qualification_outcome(issues: list[str], native_proven: bool, request_mode: str = 'streaming') -> str:
    if request_mode not in ('streaming', 'host-buffered'):
        raise ValueError('unknown request mode')
    if issues:
        return 'FAIL'
    return 'PASS' if native_proven else 'BLOCKED'


def buffered_inspection_id(text: str) -> str | None:
    pattern = (r'modsecurity-htx: buffered request inspected before header release; '
               rf'transaction_id=({HOST_TRANSACTION_ID}) body_mode=buffered '
               rf'body_bytes_seen={len(P2_BODY)} eos_seen=true')
    matches = re.findall(pattern + r'(?=\r?$)', text, re.MULTILINE)
    return matches[0] if len(matches) == 1 and text.count(
        'buffered request inspected before header release;'
    ) == 1 else None


def valid_buffered_inspection(text: str) -> bool:
    return buffered_inspection_id(text) is not None


def mapped_libraries(maps: str, expected: str | None,
                     process_root: Path | None = None) -> list[dict]:
    if expected is not None and not re.fullmatch('[0-9a-f]{64}', expected):
        raise ValueError('invalid expected library digest')
    libraries = {}
    for line in maps.splitlines():
        fields = line.split(None, 5)
        if len(fields) != 6 or 'libmodsecurity' not in fields[5]:
            continue
        path = fields[5]
        if path in libraries:
            if (libraries[path]['map_device'] != fields[3] or
                    libraries[path]['inode'] != int(fields[4])):
                raise ValueError('mapped library identity changed between segments')
            continue
        if (not re.fullmatch(r'/[A-Za-z0-9_./+-]+', path) or
                os.path.normpath(path) != path or
                path.endswith(' (deleted)')):
            raise ValueError('mapped library path is not a stable absolute path')
        flags = os.O_RDONLY | os.O_NOFOLLOW | getattr(os, 'O_NONBLOCK', 0)
        with os.fdopen(os.open(path, flags), 'rb') as stream:
            stat = os.fstat(stream.fileno())
            major, minor = (int(part, 16) for part in fields[3].split(':'))
            map_device = (major, minor)
            opened_device = (os.major(stat.st_dev), os.minor(stat.st_dev))
            translation = map_device != opened_device
            if translation and (process_root is None or
                    mounted_device_for_path(process_root, path) != map_device):
                raise ValueError('mapped library device has no process-mount binding')
            if (not stat_module.S_ISREG(stat.st_mode) or stat.st_nlink != 1 or
                    stat.st_uid != os.getuid() or stat.st_mode & 0o022 or
                    stat.st_ino != int(fields[4])):
                raise ValueError(
                    'mapped library inode/metadata differs from opened file: '
                    f'map={fields[3]}/{fields[4]} '
                    f'file={os.major(stat.st_dev):02x}:{os.minor(stat.st_dev):02x}/{stat.st_ino}'
                )
            h = hashlib.sha256()
            for chunk in iter(lambda: stream.read(LIMIT), b''):
                h.update(chunk)
            actual = h.hexdigest()
            if expected is not None and actual != expected:
                raise ValueError('mapped library digest differs from expected build')
            libraries[path] = {'path': path, 'inode': stat.st_ino,
                               'map_device': fields[3],
                               'opened_device': f'{opened_device[0]:02x}:{opened_device[1]:02x}',
                               'device_translation_verified': translation,
                               'sha256': actual, 'expected_digest_verified': expected is not None}
    return list(libraries.values())


def limits():
    resource.setrlimit(resource.RLIMIT_FSIZE, (LIMIT, LIMIT))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


def run_child(command: list[str], output, *, timeout=None):
    return subprocess.run(command, stdout=output, stderr=subprocess.STDOUT,
                          timeout=timeout, check=True, preexec_fn=limits)


def write_json(root: Path, name: str, record: dict):
    text = json.dumps(record, sort_keys=True, separators=(',', ':')) + '\n'
    if len(text) > LIMIT:
        raise ValueError('receipt too large')
    write_text_atomic(root, root / name, text, 'qualification receipt')


def run(args) -> int:
    os.umask(0o077)
    if Path(args.runtime_root).exists():
        raise ValueError('runtime root must be fresh')
    root = verified_runtime_root(args.runtime_root)
    binary = verified_input(args.haproxy, args.binary_sha256, 256 * 1024 * 1024)
    rules = verified_input(args.rules, args.rules_sha256, LIMIT)
    copied_rules = root / 'rules.conf'
    write_text_atomic(root, copied_rules, rules.read_text(), 'canonical rules copy')
    if digest(copied_rules) != args.rules_sha256:
        raise ValueError('rules changed while copied')
    canonical_rules_content(root, str(copied_rules))
    config(1, 2, copied_rules, args.request_body_mode)  # Validate interpolation before opening sockets.
    version_contract = Path(__file__).resolve().parents[1] / 'htx-overlay/version-contract.json'
    pinned_version = json.loads(version_contract.read_text())['version']
    backend = Backend()
    front_socket = socket.socket()
    front_socket.bind(('127.0.0.1', 0))
    front = front_socket.getsockname()[1]
    front_socket.close()
    cfg = root / 'haproxy.cfg'
    write_text_atomic(root, cfg, config(front, backend.port, copied_rules, args.request_body_mode), 'native HTX config')
    process = None
    log_fd = None
    backend_started = False
    status = None
    prefix_observed = None
    identity = None
    issues = []
    try:
        log_fd = os.open(root / 'host.log', os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW, 0o600)
        run_child([str(binary), '-vv'], log_fd, timeout=TIMEOUT)
        if f'HAProxy version {pinned_version}' not in read_text(root, root / 'host.log', 'version'):
            raise ValueError('binary version differs from pinned contract')
        run_child([str(binary), '-c', '-f', str(cfg)], log_fd, timeout=TIMEOUT)
        # Start HAProxy before creating threads; preexec resource setup then
        # never runs in a multithreaded parent.
        process = subprocess.Popen([str(binary), '-db', '-f', str(cfg)], stdout=log_fd,
                                   stderr=subprocess.STDOUT, preexec_fn=limits)
        backend.thread.start()
        backend_started = True
        deadline = time.monotonic() + TIMEOUT
        while True:
            if process.poll() is not None:
                raise RuntimeError('HAProxy exited before readiness')
            try:
                client = socket.create_connection(('127.0.0.1', front), timeout=0.1)
                break
            except OSError:
                if time.monotonic() >= deadline:
                    raise RuntimeError('HAProxy readiness timeout')
                time.sleep(0.02)
        proc_root = Path('/proc') / str(process.pid)
        identity = {'pid': process.pid, 'start_ticks': proc_root.joinpath('stat').read_text().rsplit(')', 1)[1].split()[19],
                    'exe_sha256': digest(proc_root / 'exe'),
                    'fd_count': len(list(proc_root.joinpath('fd').iterdir())),
                    'status': [line for line in proc_root.joinpath('status').read_text().splitlines() if line.startswith(('VmRSS:', 'Threads:'))],
                    'libmodsecurity': mapped_libraries(
                        proc_root.joinpath('maps').read_text(), args.library_sha256, proc_root
                    )}
        if identity['exe_sha256'] != args.binary_sha256 or not identity['libmodsecurity']:
            raise RuntimeError('running host executable/library identity missing')
        with client:
            client.settimeout(TIMEOUT)
            headers = (f'POST /no-crs/request-body HTTP/1.1\r\nHost: localhost\r\nX-Request-Id: {REQUEST_ID}\r\n'
                       f'Content-Type: text/plain\r\nContent-Length: {len(P2_BODY)}\r\nConnection: close\r\n\r\n').encode('ascii')
            client.sendall(headers + P2_BODY[:-1])
            # Diagnostic observation window only. A timer cannot prove native
            # DATA delivery; the final outcome remains BLOCKED without the
            # correlated pre-EOS trace described in the receipt.
            time.sleep(0.5)
            prefix_observed = backend.snapshot()
            client.sendall(P2_BODY[-1:])
            response = b''
            while b'\r\n' not in response and len(response) < LIMIT:
                chunk = client.recv(4096)
                if not chunk:
                    break
                response += chunk
            first = response.split(b'\r\n', 1)[0]
            if re.fullmatch(rb'HTTP/1\.[01] [1-5][0-9]{2}(?: [^\r\n]*)?', first):
                status = int(first.split(b' ')[1])
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        issues.append(type(exc).__name__ + ': ' + str(exc)[:200])
    finally:
        if process is not None and process.poll() is None:
            process.terminate()
            try:
                process.wait(TIMEOUT)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(TIMEOUT)
        if backend_started:
            if not backend.thread.is_alive():
                issues.append('backend_observer_terminated_early')
            try:
                backend.close()
            except RuntimeError as exc:
                issues.append(str(exc))
        else:
            backend.listener.close()
        if log_fd is not None:
            os.close(log_fd)
    observed = backend.snapshot()
    host_log = read_text(root, root / 'host.log', 'bounded host log') if (root / 'host.log').exists() else ''
    decision_id = native_decision_id(host_log)
    inspection_id = buffered_inspection_id(host_log)
    decision = decision_id is not None
    if decision_id is not None and inspection_id is not None and decision_id != inspection_id:
        issues.append('native_inspection_decision_id_mismatch')
    buffered_proven = (args.request_body_mode == 'host-buffered'
                       and bool(args.library_sha256) and decision_id is not None
                       and decision_id == inspection_id)
    issues.extend(assess(status, observed, decision))
    for port in (front, backend.port):
        with socket.socket() as probe:
            probe.settimeout(0.1)
            if probe.connect_ex(('127.0.0.1', port)) == 0:
                issues.append('listener_survived_cleanup')
    receipt = {'schema_version': 1, 'profile': 'haproxy-native-htx', 'stage': 'delayed_p2_zero_dispatch_prerequisite',
               'outcome': qualification_outcome(issues, buffered_proven, args.request_body_mode), 'full_b_acceptance': False,
               'request_body_mode': 'buffered' if args.request_body_mode == 'host-buffered' else 'streaming',
               'request_profile': args.request_body_mode,
               'request_body_limit': 65536 if args.request_body_mode == 'host-buffered' else None,
               'native_buffered_eom_inspection_proven': buffered_proven,
               'native_prefix_observation': 'NOT_APPLICABLE' if args.request_body_mode == 'host-buffered' else 'NOT_PROVEN',
               'blockers': ([] if buffered_proven else ['Missing native correlated inspection proof; streaming diagnostic additionally requires pre-EOS DATA acknowledgement.'])
                           + ([] if args.library_sha256 else ['Expected libmodsecurity build digest omitted.']),
               'client_supplied_request_id': REQUEST_ID, 'client_supplied_request_id_trusted': False,
               'host_transaction_id': decision_id if decision_id == inspection_id else None,
               'rule_id': 1100101, 'client_status': status,
               'unique_native_rule_observed': decision, 'backend_before_request_eos': prefix_observed,
               'backend_final': observed, 'host_identity': identity, 'issues': issues,
               'backend_queue_barrier_accepted': backend.barrier_accepted,
               'backend_observer_joined': backend_started and not backend.thread.is_alive(),
               'backend_queue_drained': backend.barrier_accepted and backend.drained.is_set() and not backend.drain_error,
               'binary_sha256': args.binary_sha256, 'rules_sha256': args.rules_sha256,
               'config_sha256': digest(cfg), 'host_log_sha256': digest(root / 'host.log'),
               'body_payload_persisted': False, 'owned_process_reaped': process is None or process.poll() is not None,
               'remaining_gates': 'Full G1-G9 remains unexecuted beyond this prerequisite'}
    write_json(root, 'qualification.json', receipt)
    write_json(root, 'qualification-integrity.json', {'qualification_sha256': digest(root / 'qualification.json')})
    print(json.dumps({'outcome': receipt['outcome'], 'issues': issues, 'receipt': str(root / 'qualification.json')}))
    return 1 if issues else (0 if buffered_proven else 77)


CAMPAIGN_CASES = {'allow': (200, 1), 'p1': (403, 0), 'p2': (403, 0),
                  'alternative': (429, 0), 'p3': (403, 1), 'p4': (200, 1),
                  'nonempty': (200, 1), 'boundary': (200, 1),
                  'limit': (503, 0), 'chunked': (200, 1),
                  'upstream_abort': (502, 1), 'parallel': (200, 1)}
CAMPAIGN_RESPONSE = b'htxq-upstream-ok\n'
CAMPAIGN_P4 = b'no-crs-response-body-marker\n'


def campaign_config(front, back, rules):
    value = config(front, back, rules, 'host-buffered')
    return value.replace('    mode http\n',
                         '    mode http\n    log global\n    option dontlognull\n'
                         '    log-format "HTXQ request_id=%HU host_id=haproxy-htx-%rt status=%ST termination=%ts"\n')


def campaign_body(case):
    if case == 'p2':
        return P2_BODY
    if case in ('nonempty', 'chunked'):
        return b'legitimate-body'
    if case == 'boundary':
        return b'x' * LIMIT
    if case == 'limit':
        return b'x' * (LIMIT + 1)
    return b''


def campaign_wire(case, token, keepalive=False):
    if case not in CAMPAIGN_CASES or not re.fullmatch(r'q[1-3]-[a-z0-9-]{1,48}', token):
        raise ValueError('invalid campaign case/token')
    body = campaign_body(case)
    fields = [f'POST /htxq/{token} HTTP/1.1', 'Host: localhost',
              f'X-Request-Id: {token}', f'X-Htxq-Case: {case}',
              'Content-Type: text/plain',
              'Connection: ' + ('keep-alive' if keepalive else 'close')]
    if case in ('p1', 'alternative'):
        fields.append('X-Modsec-Smoke: ' + ('block' if case == 'p1' else 'alternative-status'))
    if case == 'chunked':
        fields.append('Transfer-Encoding: chunked')
        body = f'{len(body):x}\r\n'.encode() + body + b'\r\n0\r\n\r\n'
    else:
        fields.append(f'Content-Length: {len(body)}')
    return ('\r\n'.join(fields) + '\r\n\r\n').encode('ascii') + body


def campaign_correlate(text, probes):
    """Bind HAProxy's native stream counter to the synthetic wire URI.

    `%rt` and the native overlay both use `s->uniq_id`; request headers never
    supply the host identity. No missing or duplicate receipt is accepted.
    """
    if re.search(r'\b(?:panic|fatal|segfault|segmentation fault)\b|\[(?:ALERT|EMERG)\]', text, re.I):
        raise ValueError('fatal host diagnostic, including shutdown')
    pattern = (r'HTXQ request_id=/htxq/(q[1-3]-[a-z0-9-]{1,48}) '
               r'host_id=(haproxy-htx-[0-9]+) status=([0-9]{3}) termination=([^\s]+)')
    rows = re.findall(pattern + r'(?=\r?$)', text, re.M)
    if len(rows) != len(probes) or text.count('HTXQ ') != len(rows):
        raise ValueError('missing/duplicate/malformed host request receipt')
    by_token = {}
    for token, host_id, status, termination in rows:
        if token in by_token or host_id in {r['host_id'] for r in by_token.values()}:
            raise ValueError('duplicate host request/transaction identity')
        by_token[token] = {'token': token, 'host_id': host_id,
                          'status': int(status), 'termination': termination}
    if set(by_token) != {p['token'] for p in probes}:
        raise ValueError('unknown host request receipt')
    expected_lines = []
    expected_inspections = []
    for probe in probes:
        case = probe['case']
        if (case not in CAMPAIGN_CASES or type(probe['status']) is not int or
                probe['status'] != CAMPAIGN_CASES[case][0] or
                type(probe['body_bytes']) is not int or
                probe['body_bytes'] != len(campaign_body(case)) or
                type(probe['backend']) is not int or probe['backend'] != CAMPAIGN_CASES[case][1]):
            raise ValueError('invalid expected campaign probe')
        row = by_token[probe['token']]
        if row['status'] != probe['status']:
            raise ValueError('host/client status mismatch')
        host_id, case = row['host_id'], probe['case']
        intervention = None
        if case in ('p1', 'alternative', 'p2', 'p3'):
            stage, phase, rule, status = {
                'p1': ('request', 1, 1100001, 403),
                'alternative': ('request', 1, 1100002, 429),
                'p2': ('request-body', 2, 1100101, 403),
                'p3': ('response-header', 3, 1100201, 403),
            }[case]
            intervention = (f'modsecurity-htx: {stage} intervention observed; transaction_id={host_id} '
                            f'phase={phase} status={status} rule_id={rule} action=deny')
        elif case == 'p4':
            intervention = (f'modsecurity-htx: response-body late intervention observed; transaction_id={host_id} '
                            'phase=4 status=403 rule_id=1100301 requested_action=deny '
                            'resolved_policy_action=log_only host_action=log_only')
        elif case == 'limit':
            intervention = (f'modsecurity-htx: fail-closed host-buffered request exceeds limit or append failed; '
                            f'transaction_id={host_id} status=503')
        if intervention:
            expected_lines.append(intervention)
            if len(re.findall(re.escape(intervention) + r'(?=\r?$)', text, re.M)) != 1:
                raise ValueError('missing/duplicate/divergent native decision')
        if case not in ('p1', 'alternative', 'limit'):
            inspection = (f'modsecurity-htx: buffered request inspected before header release; '
                          f'transaction_id={host_id} body_mode=buffered '
                          f'body_bytes_seen={probe["body_bytes"]} eos_seen=true')
            expected_inspections.append(inspection)
            if len(re.findall(re.escape(inspection) + r'(?=\r?$)', text, re.M)) != 1:
                raise ValueError('buffered EOS inspection absent or ambiguous')
        row['native_decision'] = intervention
    actual = [line[line.index('modsecurity-htx: '):].rstrip('\r')
              for line in text.splitlines()
              if 'modsecurity-htx: ' in line and ('intervention observed;' in line or 'fail-closed ' in line)]
    if sorted(actual) != sorted(expected_lines):
        raise ValueError('unexpected native intervention/fail-closed receipt')
    inspected = [line[line.index('modsecurity-htx: '):].rstrip('\r') for line in text.splitlines()
                 if 'modsecurity-htx: buffered request inspected before header release;' in line]
    if sorted(inspected) != sorted(expected_inspections):
        raise ValueError('unexpected buffered inspection receipt')
    native_lines = [line[line.index('modsecurity-htx: '):].rstrip('\r')
                    for line in text.splitlines() if 'modsecurity-htx: ' in line]
    if sorted(native_lines) != sorted(expected_lines + expected_inspections):
        raise ValueError('unexpected native diagnostic, including shutdown')
    return [by_token[p['token']] for p in probes]


def campaign_backend_check(observation, probes):
    if observation.get('errors') != [] or observation.get('active') != 0:
        raise ValueError('backend parse/unfinished request evidence')
    expected = {p['token']: p for p in probes if p['backend'] == 1}
    records = observation.get('requests')
    if not isinstance(records, list) or len(records) != len(expected):
        raise ValueError('unexpected/missing backend dispatch')
    seen = set()
    for record in records:
        token = record.get('token')
        if (token not in expected or token in seen or type(record.get('body_bytes')) is not int or
                record.get('body_bytes') != expected[token]['body_bytes'] or
                record.get('case') != expected[token]['case'] or
                record.get('body_sha256') != hashlib.sha256(campaign_body(expected[token]['case'])).hexdigest()):
            raise ValueError('backend dispatch/body correlation mismatch')
        seen.add(token)
    terminated = set()
    boundaries = observation.get('boundary_terminations', [])
    if not isinstance(boundaries, list):
        raise ValueError('invalid backend boundary terminations')
    for boundary in boundaries:
        if not isinstance(boundary, dict):
            raise ValueError('invalid backend boundary termination')
        tokens = boundary.get('request_tokens')
        if (boundary.get('kind') != 'connection_reset' or not isinstance(tokens, list) or
                not 1 <= len(tokens) <= 32 or any(not isinstance(token, str) for token in tokens) or
                len(set(tokens)) != len(tokens) or not set(tokens) <= seen or
                set(tokens) & terminated):
            raise ValueError('unbound backend boundary termination')
        terminated.update(tokens)


class CampaignUpstream(socketserver.ThreadingTCPServer):
    allow_reuse_address = False
    daemon_threads = False
    block_on_close = True

    def __init__(self):
        self.lock = threading.Lock()
        self.requests, self.errors, self.handlers = [], [], set()
        self.boundary_terminations = []
        self.accepts = self.active = self.peak = 0
        self.parallel = set()
        self.overlap_callback = None
        self.overlap_sample = None
        self.release = threading.Event()
        super().__init__(('127.0.0.1', 0), CampaignHandler)
        self.thread = threading.Thread(target=self.serve_forever, kwargs={'poll_interval': 0.02})

    def start(self):
        self.thread.start()

    def get_request(self):
        connection, address = super().get_request()
        with self.lock:
            self.accepts += 1
            self.handlers.add(connection)
        return connection, address

    def snapshot(self):
        with self.lock:
            return {'requests': list(self.requests), 'errors': list(self.errors),
                    'boundary_terminations': list(self.boundary_terminations),
                    'active': self.active, 'peak_active': self.peak,
                    'parallel_tokens': sorted(self.parallel), 'accepts': self.accepts,
                    'overlap_sample': self.overlap_sample}

    def close(self):
        self.release.set()
        if self.thread.ident is not None:
            self.shutdown()
            self.thread.join(TIMEOUT)
        self.socket.setblocking(False)
        while True:
            try:
                pending, _ = self.socket.accept()
            except BlockingIOError:
                break
            with pending:
                with self.lock:
                    self.errors.append('backend queued connection at cleanup')
        with self.lock:
            sockets = list(self.handlers)
        # HAProxy has already been reaped. EOF is allowed only between requests;
        # every accepted partial header/body remains a recorded parse error.
        for connection in sockets:
            try:
                connection.shutdown(socket.SHUT_RD)
            except OSError:
                pass
        self.server_close()
        if self.thread.is_alive():
            raise ValueError('upstream observer survived cleanup')


class CampaignHandler(socketserver.BaseRequestHandler):
    def read_exact(self, count):
        value = bytearray()
        while len(value) < count:
            remaining = self.deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError('backend absolute deadline')
            self.request.settimeout(remaining)
            data = self.request.recv(min(4096, count - len(value)))
            if not data:
                raise ValueError('backend truncated body/header')
            value.extend(data)
        return bytes(value)

    def line(self, maximum=16384, clean_eof=False, completed_tokens=()):
        value = bytearray()
        while not value.endswith(b'\r\n'):
            try:
                value.extend(self.read_exact(1))
            except ConnectionResetError:
                if clean_eof and not value and completed_tokens:
                    with self.server.lock:
                        self.server.boundary_terminations.append(
                            {'kind': 'connection_reset', 'request_tokens': list(completed_tokens)})
                    return None
                raise
            except ValueError:
                if clean_eof and not value:
                    return None
                raise
            if len(value) > maximum:
                raise ValueError('backend framing limit')
            if clean_eof and len(value) == 1:
                self.deadline = time.monotonic() + TIMEOUT
        if b'\n' in value[:-2] or b'\r' in value[:-2]:
            raise ValueError('backend malformed CRLF')
        return bytes(value)

    def handle(self):
        server = self.server
        handled = 0
        completed_tokens = []
        try:
            for _ in range(32):
                self.deadline = time.monotonic() + 60
                first = self.line(clean_eof=True, completed_tokens=completed_tokens)
                if first is None:
                    return
                self.deadline = time.monotonic() + TIMEOUT
                match = re.fullmatch(rb'POST /htxq/(q[1-3]-[a-z0-9-]{1,48}) HTTP/1\.1\r\n', first)
                if not match:
                    raise ValueError('unexpected backend request line')
                fields, size = {}, len(first)
                while True:
                    line = self.line()
                    size += len(line)
                    if size > 16384:
                        raise ValueError('backend headers too large')
                    if line == b'\r\n':
                        break
                    key, separator, value = line[:-2].partition(b':')
                    if not separator or not re.fullmatch(rb'[A-Za-z0-9-]+', key):
                        raise ValueError('backend invalid header')
                    fields.setdefault(key.lower(), []).append(value.strip())
                token = match[1].decode('ascii')
                if fields.get(b'x-request-id') != [token.encode()]:
                    raise ValueError('backend request-ID mismatch')
                cases = fields.get(b'x-htxq-case', [])
                if len(cases) != 1 or cases[0].decode('ascii') not in CAMPAIGN_CASES:
                    raise ValueError('backend unknown case')
                case = cases[0].decode('ascii')
                lengths, transfer = fields.get(b'content-length', []), fields.get(b'transfer-encoding', [])
                count = 0
                entity = bytearray()
                if transfer:
                    if transfer != [b'chunked'] or lengths:
                        raise ValueError('backend ambiguous transfer framing')
                    while True:
                        chunk = self.line(32)
                        if not re.fullmatch(rb'[0-9a-fA-F]+\r\n', chunk):
                            raise ValueError('backend invalid chunk size')
                        amount = int(chunk[:-2], 16)
                        count += amount
                        if count > LIMIT:
                            raise ValueError('backend request too large')
                        entity.extend(self.read_exact(amount))
                        if self.read_exact(2) != b'\r\n':
                            raise ValueError('backend invalid chunk delimiter')
                        if amount == 0:
                            break
                else:
                    if len(lengths) != 1 or not re.fullmatch(rb'[0-9]+', lengths[0]) or int(lengths[0]) > LIMIT:
                        raise ValueError('backend invalid Content-Length')
                    count = int(lengths[0])
                    entity.extend(self.read_exact(count))
                if bytes(entity) != campaign_body(case):
                    raise ValueError('backend entity differs from exact synthetic request')
                with server.lock:
                    server.requests.append({'token': token, 'case': case, 'body_bytes': count,
                                            'body_sha256': hashlib.sha256(entity).hexdigest()})
                    handled += 1
                    completed_tokens.append(token)
                    server.active += 1
                    server.peak = max(server.peak, server.active)
                try:
                    if case == 'parallel':
                        with server.lock:
                            server.parallel.add(token)
                            if len(server.parallel) == 4:
                                if server.overlap_callback:
                                    server.overlap_sample = server.overlap_callback()
                                server.release.set()
                        if not server.release.wait(TIMEOUT):
                            raise TimeoutError('four-client overlap was not reached')
                    if case == 'upstream_abort':
                        return
                    body = CAMPAIGN_P4 if case == 'p4' else CAMPAIGN_RESPONSE
                    extra = b'X-Modsec-Upstream: block\r\n' if case == 'p3' else b''
                    self.request.sendall(b'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n' + extra +
                                         f'Content-Length: {len(body)}\r\n\r\n'.encode() + body)
                finally:
                    with server.lock:
                        server.active -= 1
            raise ValueError('backend per-connection request budget')
        except (OSError, ValueError, UnicodeError) as exc:
            with server.lock:
                server.errors.append(type(exc).__name__ + ': ' + str(exc)[:100])
        finally:
            with server.lock:
                server.handlers.discard(self.request)
                if handled == 0:
                    server.errors.append('backend accepted without any complete request')


def campaign_probe(front, case, token, connection=None):
    own = connection is None
    connection = connection or socket.create_connection(('127.0.0.1', front), timeout=TIMEOUT)
    try:
        connection.settimeout(TIMEOUT)
        connection.sendall(campaign_wire(case, token, not own))
        # Reuse the shared strict response-framing/deadline reader, retaining
        # only an in-memory bounded synthetic wire copy for a body hash check.
        class Capture:
            def __init__(self):
                self.data = bytearray()
            def settimeout(self, value):
                connection.settimeout(value)
            def recv(self, count):
                data = connection.recv(count)
                self.data.extend(data)
                if len(self.data) > 131072:
                    raise ValueError('campaign response size budget')
                return data
        capture = Capture()
        status = read_response(capture, require_keepalive=not own, deadline=time.monotonic() + TIMEOUT)
        if status != CAMPAIGN_CASES[case][0]:
            raise ValueError(f'{case} client status {status}, expected {CAMPAIGN_CASES[case][0]}')
        body = bytes(capture.data).split(b'\r\n\r\n', 1)[1]
        if case in ('allow', 'nonempty', 'boundary', 'chunked', 'parallel', 'p4'):
            expected = CAMPAIGN_P4 if case == 'p4' else CAMPAIGN_RESPONSE
            if body != expected:
                raise ValueError('allow/P4 client response entity mismatch')
        return {'token': token, 'case': case, 'status': status,
                'body_bytes': len(campaign_body(case)), 'backend': CAMPAIGN_CASES[case][1],
                'response_bytes': len(body), 'response_sha256': hashlib.sha256(body).hexdigest()}
    finally:
        if own:
            connection.close()


def campaign_identity(child, expected):
    identity = child.identity()
    if identity != expected:
        raise ValueError('host identity or executable digest changed during campaign')
    return identity


def campaign_host_log(root, pin=None):
    target = artifact_path(root, root / 'host.log', 'campaign host log', must_exist=True)
    parent = open_runtime_artifact_parent(target)
    try:
        fd = os.open(target.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
        try:
            before = os.fstat(fd)
            identity = [before.st_dev, before.st_ino, before.st_mode, before.st_uid, before.st_gid, before.st_nlink]
            if (not stat_module.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                    before.st_uid != os.getuid() or before.st_mode & 0o077 or before.st_size > 8 << 20):
                raise ValueError('unsafe or oversized campaign host log')
            with os.fdopen(os.dup(fd), 'rb') as stream:
                content = stream.read((8 << 20) + 1)
            after = os.fstat(fd)
            current = os.stat(target.name, dir_fd=parent, follow_symlinks=False)
            def state(details):
                return (details.st_dev, details.st_ino, details.st_mode, details.st_uid,
                        details.st_gid, details.st_nlink, details.st_size, details.st_mtime_ns, details.st_ctime_ns)
            if (len(content) > 8 << 20 or state(before) != state(after) or state(after) != state(current) or
                    len(content) != after.st_size or (content and not content.endswith(b'\n'))):
                raise ValueError('campaign host log changed or contains partial append')
        finally:
            os.close(fd)
    finally:
        os.close(parent)
    if pin is None:
        text = content.decode('utf-8')
        if re.search(r'Proxy .*stop|hard[- ]stop', text, re.I):
            raise ValueError('stale stop acknowledgement before signal delivery')
        return {'identity': identity, 'offset': len(content), 'prefix_sha256': hashlib.sha256(content).hexdigest()}
    if (identity != pin['identity'] or len(content) < pin['offset'] or
            hashlib.sha256(content[:pin['offset']]).hexdigest() != pin['prefix_sha256']):
        raise ValueError('campaign host log prefix or identity changed')
    return content.decode('utf-8'), content[pin['offset']:].decode('utf-8')


def campaign_stop(child, expected, root=None):
    """Qualifying standalone shutdown reaps the pinned live host by soft-stop.

    Child.stop remains the bounded safety cleanup on failure; its fallback may
    never turn a failed shutdown into successful qualification evidence.
    """
    try:
        if not callable(getattr(os, 'pidfd_open', None)) or not callable(getattr(signal, 'pidfd_send_signal', None)):
            raise ValueError('confirmed soft-stop requires pidfd APIs')
        campaign_identity(child, expected)
        child.inventory()
        if surviving_descendants(list(child.descendants.values())):
            raise ValueError('unexpected live host descendants before shutdown')
        campaign_identity(child, expected)
        if child.process.poll() is not None:
            raise ValueError('host exited before controlled soft-stop')
        pidfd = os.pidfd_open(expected['pid'], 0)
        try:
            campaign_identity(child, expected)
            if child.process.poll() is not None:
                raise ValueError('host exited while binding controlled soft-stop')
            log_pin = campaign_host_log(root) if root is not None else None
            # Unlike Popen.send_signal, this API never silently suppresses ESRCH.
            signal.pidfd_send_signal(pidfd, signal.SIGUSR1, None, 0)
        finally:
            os.close(pidfd)
        try:
            exit_status = child.process.wait(timeout=3)
        except subprocess.TimeoutExpired as exc:
            raise ValueError('controlled shutdown required SIGKILL fallback') from exc
        if exit_status != 0:
            raise ValueError(f'unexpected controlled host exit status: {exit_status}')
        return {'signal': 'SIGUSR1', 'delivery': 'pidfd_send_signal',
                'returncode': exit_status, 'no_kill_fallback': True, 'host_log_pin': log_pin}
    finally:
        child.stop()


def campaign_soft_stop_ack(text, identity, probes):
    """Bind native proxy_cond_disable warnings to this standalone host run."""
    keepalive = sum('-keep-' in probe['token'] for probe in probes)
    frontend_connections = 1 + len(probes) - max(0, keepalive - 1)
    # stream_set_backend increments cum_sess when selecting this default
    # backend, before the native HTX header analyser may block dispatch.
    # This counts proxy streams; CampaignUpstream independently counts origin I/O.
    expected = {'htx_in': (frontend_connections, 0),
                'htx_upstream': (0, len(probes))}
    native, raw = {}, set()
    for line in text.splitlines():
        if re.search(r'hard[- ]stop', line, re.I):
            raise ValueError('hard-stop diagnostic cannot qualify soft-stop')
        if 'Proxy ' not in line or 'stop' not in line.lower():
            continue
        match = re.fullmatch(r'(?:\[WARNING\]  \(([1-9][0-9]*)\) : )?Proxy ([A-Za-z0-9_]+) stopped '
                             r'\(cumulated conns: FE: (0|[1-9][0-9]*), BE: (0|[1-9][0-9]*)\)\.', line)
        if not match:
            raise ValueError('malformed proxy soft-stop acknowledgement')
        pid, name, front, back = match.groups()
        if name not in expected or (int(front), int(back)) != expected[name]:
            raise ValueError('proxy soft-stop name or count mismatch')
        if pid is None:
            if name in raw:
                raise ValueError('duplicate raw proxy soft-stop diagnostic')
            raw.add(name)
        else:
            if int(pid) != identity['pid'] or name in native:
                raise ValueError('proxy soft-stop PID mismatch or duplicate')
            native[name] = {'pid': int(pid), 'frontend_connections': int(front), 'backend_streams': int(back)}
    if set(native) != set(expected):
        raise ValueError('missing native proxy soft-stop acknowledgement')
    return native


def campaign_start(args, root, number):
    root = verified_runtime_root(str(root))
    check_campaign_rules(args)
    copied_rules, _, local_rules_pin = copy_campaign_rules(
        root, args.rules_path, args.rules_sha256, args.rules_pin)
    args.start_rules_pins.append((root, copied_rules, local_rules_pin))
    campaign_config(1, 2, copied_rules)  # Validate paths before opening any sockets.
    upstream = CampaignUpstream()
    front_socket = socket.socket()
    front_socket.bind(('127.0.0.1', 0))
    front = front_socket.getsockname()[1]
    front_socket.close()
    cfg = root / 'haproxy.cfg'
    write_text_atomic(root, cfg, campaign_config(front, upstream.server_address[1], copied_rules), 'campaign native config')
    child = monitor = identity = None
    start_deadline = time.monotonic() + 60
    probes, issues = [], []
    result = {'start': number, 'full_b_acceptance': False, 'catalog_acceptance': False,
              'profile': 'haproxy-native-htx', 'request_profile': 'host-buffered'}
    try:
        with (root / 'config-check.log').open('xb') as output:
            run_child([str(args.binary), '-c', '-f', str(cfg)], output.fileno(), timeout=TIMEOUT)
        check_campaign_rules(args)
        child = Child([str(args.binary), '-db', '-f', str(cfg)], root, 'host')
        upstream.start()
        deadline = time.monotonic() + TIMEOUT
        while True:
            if child.process.poll() is not None:
                raise ValueError('host exited before readiness')
            try:
                ready = socket.create_connection(('127.0.0.1', front), timeout=0.1)
                ready.close()
                break
            except OSError:
                if time.monotonic() >= deadline:
                    raise TimeoutError('host readiness deadline')
                time.sleep(0.02)
        identity = child.identity()
        if identity['exe_sha256'] != args.binary_sha256:
            raise ValueError('host executable changed')
        process_root = Path('/proc') / str(child.process.pid)
        libraries = mapped_libraries((process_root / 'maps').read_text(), args.library_sha256, process_root)
        if not libraries:
            raise ValueError('host has no pinned mapped libmodsecurity')
        result.update(host_identity=identity, loaded_libraries=libraries)
        monitor = Monitor([child])
        result['sockets_before'] = owned_sockets(child)
        def sample_overlap():
            status = (process_root / 'status').read_text()
            return {'identity': campaign_identity(child, identity),
                    'rss_bytes': int(re.search(r'^VmRSS:\s+(\d+) kB', status, re.M)[1]) * 1024,
                    'fd': len(list((process_root / 'fd').iterdir())),
                    'sockets': owned_sockets(child), 'active_backend_handlers': 4}
        upstream.overlap_callback = sample_overlap
        def probe(case, suffix, connection=None):
            if time.monotonic() >= start_deadline:
                raise TimeoutError('campaign start budget exceeded')
            check_campaign_rules(args)
            pinned_rules(copied_rules, args.rules_sha256, local_rules_pin, root)
            value = campaign_probe(front, case, f'q{number}-{suffix}', connection)
            probes.append(value)
            return value
        for case in ('allow', 'p1', 'p2'):
            probe(case, case)
        if number == 1:
            for case in ('alternative', 'nonempty', 'boundary', 'limit', 'chunked', 'p3', 'p4'):
                probe(case, case)
            before = child.identity()
            probe('upstream_abort', 'upstream-abort')
            probe('allow', 'recovery')
            if before != child.identity():
                raise ValueError('error recovery replaced the surviving host')
            result['same_process_recovery'] = True
            with socket.create_connection(('127.0.0.1', front), timeout=TIMEOUT) as keep:
                for index, case in enumerate(('allow', 'p1', 'allow', 'p2', 'allow')):
                    probe(case, f'keep-{index}', keep)
            result['keepalive_same_socket'] = True
            with ThreadPoolExecutor(max_workers=4) as pool:
                futures = [pool.submit(campaign_parallel_probe, args, front, f'q{number}-parallel-{n}') for n in range(4)]
                probes.extend(f.result(timeout=TIMEOUT * 2) for f in futures)
            if upstream.snapshot()['peak_active'] != 4 or len(upstream.snapshot()['parallel_tokens']) != 4:
                raise ValueError('real four-client handler overlap missing')
            result['parallel_overlap'] = True
        result['sockets_after'] = owned_sockets(child)
        result['host_identity_final'] = campaign_identity(child, identity)
        if time.monotonic() >= start_deadline:
            raise TimeoutError('campaign start budget exceeded')
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        issues.append(type(exc).__name__ + ': ' + str(exc)[:200])
    finally:
        if monitor:
            try:
                result['resources'] = monitor.finish()
            except (OSError, ValueError) as exc:
                issues.append('resource monitor: ' + str(exc)[:160])
        if child:
            try:
                if identity is None:
                    child.stop()
                    raise ValueError('no qualified initial host identity')
                result['controlled_shutdown'] = campaign_stop(child, identity, root)
            except (OSError, ValueError, subprocess.SubprocessError) as exc:
                issues.append('host cleanup: ' + str(exc)[:160])
        try:
            upstream.close()
        except (OSError, ValueError) as exc:
            issues.append('observer cleanup: ' + str(exc)[:160])
    observation = upstream.snapshot()
    try:
        check_campaign_rules(args)
        pinned_rules(copied_rules, args.rules_sha256, local_rules_pin, root)
        campaign_backend_check(observation, probes)
        if child is None or child.process.poll() is None or identity is None:
            raise ValueError('soft-stop acknowledgement requires reaped original host')
        log_pin = result.get('controlled_shutdown', {}).get('host_log_pin')
        if log_pin is None:
            raise ValueError('soft-stop acknowledgement requires pre-delivery log pin')
        host_log, stop_suffix = campaign_host_log(root, log_pin)
        result['soft_stop_acknowledgement'] = campaign_soft_stop_ack(stop_suffix, identity, probes)
        result['correlation'] = campaign_correlate(host_log, probes)
        result['post_reap_log_reconciled'] = child is not None and child.process.poll() is not None
    except (OSError, ValueError) as exc:
        issues.append('correlation: ' + str(exc)[:160])
    for port in (front, upstream.server_address[1]):
        with socket.socket() as listener:
            listener.settimeout(0.1)
            if listener.connect_ex(('127.0.0.1', port)) == 0:
                issues.append('listener survived cleanup')
    result.update(probes=probes, backend=observation, issues=issues,
                  errors_or_timeouts=len(issues),
                  expected_upstream_abort_statuses=[p['status'] for p in probes if p['case'] == 'upstream_abort'],
                  passed=not issues, owned_process_reaped=child is None or child.process.poll() is not None,
                  observer_joined=not upstream.thread.is_alive(),
                  config_sha256=digest(cfg), rules_sha256=digest(copied_rules))
    write_json(root, 'campaign-start.json', result)
    write_json(root, 'campaign-start-integrity.json', {'sha256': digest(root / 'campaign-start.json')})
    return result


def run_campaign(args):
    if args.request_body_mode != 'host-buffered' or not args.library_sha256:
        raise ValueError('campaign requires explicit host-buffered mode and expected library digest')
    os.umask(0o077)
    if Path(args.runtime_root).exists():
        raise ValueError('campaign runtime root must be fresh')
    root = verified_runtime_root(args.runtime_root)
    args.binary = verified_input(args.haproxy, args.binary_sha256, 256 * 1024 * 1024)
    args.campaign_root = root
    args.start_rules_pins = []
    args.rules_path, args.rules_source_pin, args.rules_pin = copy_campaign_rules(
        root, args.rules, args.rules_sha256)
    runner_hash = digest(Path(__file__))
    with (root / 'host-version.log').open('xb') as output:
        run_child([str(args.binary), '-vv'], output.fileno(), timeout=TIMEOUT)
    pinned_version = json.loads(Path(__file__).resolve().parents[1].joinpath('htx-overlay/version-contract.json').read_text())['version']
    if f'HAProxy version {pinned_version}' not in read_text(root, root / 'host-version.log', 'version'):
        raise ValueError('campaign host version differs from pin')
    starts = []
    for number in (1, 2, 3):
        starts.append(campaign_start(args, root / f'start{number}', number))
    identities = [r.get('host_identity', {}) for r in starts]
    distinct = len({(i.get('pid'), i.get('start_token')) for i in identities}) == 3 and all(identities)
    check_campaign_rules(args)
    unchanged = digest(Path(__file__)) == runner_hash and digest(args.binary) == args.binary_sha256
    result = {'profile': 'haproxy-native-htx', 'request_profile': 'host-buffered',
              'passed': all(s['passed'] for s in starts) and distinct and unchanged,
              'full_b_acceptance': False, 'catalog_acceptance': False,
              'three_distinct_starts': distinct, 'inputs_unchanged': unchanged,
              'runner_sha256': runner_hash, 'binary_sha256': args.binary_sha256,
              'rules_sha256': args.rules_sha256, 'library_sha256': args.library_sha256,
              'starts': [str(root / f'start{n}/campaign-start.json') for n in (1, 2, 3)],
              'budget': {'starts': 3, 'clients': 4, 'maximum_requests': 32,
                         'request_timeout_seconds': TIMEOUT, 'maximum_start_seconds': 60,
                         'maximum_log_bytes': 8 << 20, 'maximum_rss_bytes': 8 << 30, 'maximum_fd': 4096},
              'remaining_gates': ['G1 final source/build provenance', 'G4 response-transfer/response-limit and broader phase boundaries',
                                  'G7 profile-wide review', 'G8 final regression suite'],
              'limitations': ['body limit fail-closed503 is the current host-buffered error policy, not413',
                              'request admission buffers at most65536 bytes; response remains Safe/log-only',
                              'no streaming-profile or SPOP/response-companion evidence transfer']}
    write_json(root, 'campaign.json', result)
    write_json(root, 'campaign-integrity.json', {'sha256': digest(root / 'campaign.json')})
    print(json.dumps({'passed': result['passed'], 'receipt': str(root / 'campaign.json'), 'full_b_acceptance': False}))
    return 0 if result['passed'] else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('runtime-root', 'haproxy', 'binary-sha256', 'rules', 'rules-sha256'):
        parser.add_argument('--' + name, required=True)
    parser.add_argument('--library-sha256')
    parser.add_argument('--request-body-mode', choices=('streaming', 'host-buffered'), default='streaming')
    parser.add_argument('--campaign', action='store_true', help='explicit three-start host-buffered diagnostic; never awards B')
    args = parser.parse_args()
    return run_campaign(args) if args.campaign else run(args)


if __name__ == '__main__':
    raise SystemExit(main())
