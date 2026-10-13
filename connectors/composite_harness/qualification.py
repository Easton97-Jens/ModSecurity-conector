"""Bounded G2/G5/G6 laboratory qualification; never catalog acceptance.

Invoke a profile entrypoint with explicit host/composite/config/certificate inputs.
The runtime root must already exist, be empty, external, canonical and 0700.
No payload or client-to-decision correlation is persisted.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
import hashlib
from datetime import datetime
import json
import os
from pathlib import Path
import re
import shutil
import signal
import socket
import ssl
import stat
import subprocess
import sys
import threading
import time

REPO = Path(__file__).resolve().parents[2]
STORAGE_ROOT = Path('/var/tmp/codex/ModSecurity-conector')
FRESH_STARTS = 3
CLIENTS = 4
PARALLEL_REQUESTS_PER_CLIENT = 4
REQUEST_TIMEOUT = 5.0
ERROR_TIMEOUT = 10.0
CAMPAIGN_TIMEOUT = 180.0
MAX_LOG = 8 << 20
MAX_RSS = 8 << 30
MAX_FD = 4096
MAX_RESPONSE = 64 << 10
EXPECTED = {"allow": 200, "p1": 403, "p2": 403, "oversize": 413, "timeout": 503}
# This narrow runner has a closed rule dependency set, not a general CRS
# loader. Changes to the reviewed vector fixture require explicit re-review.
VETTED_VECTOR_SHA256 = 'e726ba9049942bbec54cf9efd2de1a21608e76c349b3eb87152f23a441be5b2b'


def trusted_path(path: Path, private=False):
    if not path.is_absolute() or str(path) != os.path.normpath(str(path)):
        raise ValueError("input path must be canonical and absolute")
    for item in [path, *path.parents]:
        metadata = item.lstat()
        if stat.S_ISLNK(metadata.st_mode) or metadata.st_uid not in {0, os.getuid()}:
            raise ValueError("unsafe path ownership or symlink")
        if metadata.st_mode & 0o022:
            if item not in {Path('/tmp'), Path('/var/tmp')} or metadata.st_uid != 0 or not metadata.st_mode & stat.S_ISVTX:
                raise ValueError("writable path ancestor")
    if path.stat().st_uid != os.getuid():
        raise ValueError("input must be owned by operator")
    if private and stat.S_IMODE(path.stat().st_mode) != 0o700:
        raise ValueError("runtime directory must be 0700")
    return path


def digest(path):
    with path.open('rb') as source:
        return hashlib.file_digest(source, 'sha256').hexdigest()


def write_json(path, value):
    with path.open('x', encoding='utf-8') as output:
        os.chmod(path, 0o600)
        json.dump(value, output, sort_keys=True)
        output.write('\n')


def request_wire(case, port, parallel=False):
    body = b'msconnector-p2-only' if case == 'p2' else b'x' * 33 if case == 'oversize' else b''
    target = '/qualification/timeout' if case == 'timeout' else '/vector/p1' if case == 'p1' else '/vector/p2' if body else '/allow'
    if parallel and case == 'allow':
        target = '/qualification/parallel'
    headers = [f"{'POST' if body else 'GET'} {target} HTTP/1.1", f'Host: 127.0.0.1:{port}', f'Content-Length: {len(body)}']
    if case == 'p1':
        headers.append('X-Msconnector-Vector: msconnector-p1-only')
    if body:
        headers.append('Content-Type: text/plain')
    return ('\r\n'.join(headers) + '\r\n\r\n').encode('ascii') + body


class DeadlineSocket:
    """Absolute request deadline, including a peer that dribbles bytes."""
    def __init__(self, connection, deadline):
        self.connection = connection
        self.deadline = deadline

    def recv(self, count):
        remaining = self.deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError('absolute request deadline exceeded')
        self.connection.settimeout(remaining)
        return self.connection.recv(count)


def read_response(connection, require_keepalive=False, deadline=None):
    connection = DeadlineSocket(connection, deadline or time.monotonic() + REQUEST_TIMEOUT)
    # A byte-at-a-time bounded header reader never loses bytes belonging to a
    # later response on the same socket. Bodies are drained, never retained.
    header = bytearray()
    while not header.endswith(b'\r\n\r\n'):
        part = connection.recv(1)
        if not part or len(header) >= 16384:
            raise ValueError('truncated/oversized response header')
        header.extend(part)
    lines = bytes(header).split(b'\r\n')
    match = re.fullmatch(rb'HTTP/1\.1 ([0-9]{3}) .+', lines[0])
    if not match:
        raise ValueError('response must be HTTP/1.1')
    headers = defaultdict(list)
    for line in lines[1:-2]:
        key, separator, value = line.partition(b':')
        if not separator:
            raise ValueError('malformed response header')
        headers[key.lower()].append(value.strip().lower())
    if require_keepalive and any(b'close' in value.split(b',') for value in headers[b'connection']):
        raise ValueError('host closed keepalive connection')
    if headers[b'transfer-encoding']:
        if headers[b'transfer-encoding'] != [b'chunked'] or headers[b'content-length']:
            raise ValueError('unsupported/ambiguous framing')
        consumed = 0
        while True:
            line = bytearray()
            while not line.endswith(b'\r\n'):
                part = connection.recv(1)
                if not part or len(line) > 32:
                    raise ValueError('bad chunk framing')
                line.extend(part)
            if not re.fullmatch(rb'[0-9a-fA-F]+\r\n', line):
                raise ValueError('bad chunk size')
            count = int(line[:-2], 16)
            consumed += count
            if consumed > MAX_RESPONSE:
                raise ValueError('response size limit')
            drain(connection, count)
            if connection.recv(1) + connection.recv(1) != b'\r\n':
                raise ValueError('bad chunk delimiter/trailer')
            if count == 0:
                break
    else:
        sizes = headers[b'content-length']
        if len(sizes) != 1 or not sizes[0].isdigit() or int(sizes[0]) > MAX_RESPONSE:
            raise ValueError('response requires bounded length')
        drain(connection, int(sizes[0]))
    return int(match.group(1))


def drain(connection, count):
    while count:
        data = connection.recv(min(count, 4096))
        if not data:
            raise ValueError('truncated response body')
        count -= len(data)


EVENT_BASE = {'decision_id', 'connector', 'phase', 'outcome', 'event_time', 'request_path', 'response_path', 'transport'}
EVENT_OPTIONAL = {
    'reservation': set(), 'lease': set(), 'claim': set(),
    'P1': {'rule_id', 'requested_action', 'visible_status', 'reason'},
    'P2': {'rule_id', 'requested_action', 'visible_status', 'reason'},
    'P3': {'rule_id', 'requested_action', 'visible_status', 'reason'},
    'P4': {'rule_id', 'requested_action', 'visible_status', 'reason'},
    'request_host_action': {'requested_action', 'actual_host_action', 'visible_status', 'reason'},
    'neutral_outcome': {'actual_host_action', 'visible_status'},
    'terminal': {'cleanup_outcome', 'reason'},
}
EVENT_OUTCOME = {'reservation': 'reserved', 'lease': 'issued', 'claim': 'accepted',
                 'P1': 'observed', 'P2': 'observed', 'P3': 'observed', 'P4': 'observed',
                 'request_host_action': 'recorded', 'neutral_outcome': 'allow', 'terminal': 'closed'}


def event_metadata(event, profile):
    if not isinstance(event, dict) or not EVENT_BASE <= event.keys():
        raise ValueError('missing required event metadata')
    phase = event['phase']
    if type(phase) is not str or phase not in EVENT_OPTIONAL or event.keys() - EVENT_BASE - EVENT_OPTIONAL[phase]:
        raise ValueError('unknown phase or forbidden/payload event field')
    for key, value in event.items():
        if key == 'visible_status':
            if type(value) is not int or not 100 <= value <= 599:
                raise ValueError('invalid event visible status type/range')
        elif type(value) is not str or not value or len(value.encode('utf-8')) > (128 if key == 'rule_id' else 256) or any(ord(c) < 32 or ord(c) > 126 for c in value):
            raise ValueError('invalid bounded event string metadata')
    if not re.fullmatch(r'[A-Za-z0-9_-]{43}', event['decision_id']):
        raise ValueError('invalid server decision ID')
    if event['outcome'] != EVENT_OUTCOME[phase]:
        raise ValueError('invalid phase outcome')
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,9})?Z', event['event_time']):
        raise ValueError('invalid event UTC timestamp')
    timestamp = datetime.fromisoformat(event['event_time'].replace('Z', '+00:00'))
    if profile not in {'envoy', 'traefik'}:
        raise ValueError('invalid profile identity')
    pipeline = ('envoy.ext_authz', 'envoy.ext_proc', 'envoy_ext_authz_ext_proc_grpc') if profile == 'envoy' else ('traefik.forwardAuth', 'traefik.native_uds', 'traefik_forwardauth_private_uds')
    if event['connector'] != profile or tuple(event[k] for k in ('request_path', 'response_path', 'transport')) != pipeline:
        raise ValueError('wrong profile event identity')
    fraction = event['event_time'].split('.', 1)[1][:-1] if '.' in event['event_time'] else ''
    return timestamp.replace(microsecond=0), int(fraction.ljust(9, '0') or '0')


def verify_events(events, expected, profile=None):
    if not isinstance(events, list) or len(events) > 1024 or not isinstance(expected, dict) or any(k not in EXPECTED or type(v) is not int or not 0 < v <= 100 for k, v in expected.items()):
        raise ValueError('invalid bounded lifecycle multiplicity input')
    groups = defaultdict(list)
    times = {}
    selected_profile = profile or (events[0].get('connector') if events and isinstance(events[0], dict) else None)
    for event in events:
        timestamp = event_metadata(event, selected_profile)
        identifier = event['decision_id']
        if identifier in times and timestamp < times[identifier]:
            raise ValueError('event timestamp moved backwards')
        times[identifier] = timestamp
        groups[identifier].append(event)
    counts = Counter()
    for records in groups.values():
        phases = [e['phase'] for e in records]
        prefix = ['reservation'] if records[0]['connector'] == 'traefik' else []
        terminals = [e for e in records if e['phase'] == 'terminal']
        if len(terminals) != 1 or terminals[0].get('cleanup_outcome') != 'closed' or terminals[0].get('outcome') != 'closed':
            raise ValueError('missing/duplicate/failed cleanup')
        for record in records:
            if record['phase'] in {'P1', 'P2', 'P3', 'P4'} and record.get('requested_action') == 'allow' and record.keys() != EVENT_BASE | {'requested_action'}:
                raise ValueError('allow phase contains unexpected rule/status/reason fields')
        denies = [e for e in records if e['phase'] in {'P1', 'P2'} and e.get('requested_action') == 'deny']
        if terminals[0].get('reason') == 'timeout':
            case = 'timeout'
            if denies or phases != prefix + ['P1', 'P2', 'lease', 'terminal'] or any(e.get('requested_action') != 'allow' for e in records if e['phase'] in {'P1', 'P2'}):
                raise ValueError('wrong timeout admission lifecycle')
        elif denies:
            if len(denies) != 1:
                raise ValueError('duplicate denial')
            decision = denies[0]
            case = 'p1' if decision['phase'] == 'P1' else 'oversize' if decision.get('reason') == 'request_body_limit' else 'p2'
            if case != 'oversize' and decision.get('rule_id') != {'p1': '1101001', 'p2': '1102001'}[case]:
                raise ValueError('wrong denial rule')
            if phases != prefix + (['P1'] if case == 'p1' else ['P1', 'P2']) + ['request_host_action', 'terminal']:
                raise ValueError('wrong denial phases')
            actions = [e for e in records if e['phase'] == 'request_host_action']
            if len(actions) != 1 or actions[0].get('requested_action') != 'block' or actions[0].get('actual_host_action') != 'deny' or actions[0].get('visible_status') != EXPECTED[case] or decision.get('visible_status') != EXPECTED[case]:
                raise ValueError('wrong actual host action')
            reason = 'request_body_limit' if case == 'oversize' and not prefix else 'request_block'
            if terminals[0].get('reason') != reason or (case != 'p1' and next(e for e in records if e['phase'] == 'P1').get('requested_action') != 'allow'):
                raise ValueError('wrong denial terminal/admission action')
            denial_fields = {'requested_action', 'visible_status', 'reason'} if case == 'oversize' else {'requested_action', 'visible_status', 'rule_id'}
            action_fields = {'requested_action', 'actual_host_action', 'visible_status'} | ({'reason'} if case == 'oversize' else set())
            if decision.keys() != EVENT_BASE | denial_fields or actions[0].keys() != EVENT_BASE | action_fields:
                raise ValueError('unexpected denial phase/host-action metadata')
            if case == 'oversize' and actions[0].get('reason') != 'request_body_limit':
                raise ValueError('wrong body-limit host-action reason')
        else:
            case = 'allow'
            if phases != prefix + ['P1', 'P2', 'lease', 'claim', 'P3', 'P4', 'neutral_outcome', 'terminal'] or any(e.get('requested_action') != 'allow' for e in records if e['phase'] in {'P1', 'P2', 'P3', 'P4'}):
                raise ValueError('wrong allow lifecycle')
            for phase, field, value in [('lease', 'outcome', 'issued'), ('claim', 'outcome', 'accepted'), ('neutral_outcome', 'actual_host_action', 'allow')]:
                found = [e for e in records if e['phase'] == phase]
                if len(found) != 1 or found[0].get(field) != value:
                    raise ValueError('wrong lease/claim/actual allow multiplicity')
            if next(e for e in records if e['phase'] == 'neutral_outcome').get('visible_status') != 200:
                raise ValueError('wrong actual allow status')
            if terminals[0].get('reason') != ('finish' if prefix else 'response_end_of_stream'):
                raise ValueError('wrong allow terminal reason')
        counts[case] += 1
    if counts != Counter(expected):
        raise ValueError('server lifecycle multiplicities do not match bounded requests')
    return dict(counts)


def start_token(pid):
    return Path(f'/proc/{pid}/stat').read_text().rsplit(')', 1)[1].split()[19]


def process_record(pid):
    root = Path(f'/proc/{pid}')
    if root.stat().st_uid != os.getuid():
        raise ValueError('process owner changed')
    fields = (root / 'stat').read_text().rsplit(')', 1)[1].split()
    return {'pid': pid, 'start_token': fields[19], 'ppid': int(fields[1]),
            'pgrp': int(fields[2]), 'session': int(fields[3]), 'exe': os.readlink(root / 'exe')}


def surviving_descendants(records):
    survivors = []
    for record in records:
        try:
            current = process_record(record['pid'])
        except FileNotFoundError:
            # A zombie/unavailable executable is not proof that the process
            # disappeared. Retain the bound token as an unresolved survivor.
            try:
                token = start_token(record['pid'])
            except FileNotFoundError:
                continue
            if token == record['start_token']:
                survivors.append({'pid': record['pid'], 'start_token': token, 'exe_unavailable': True})
            continue
        if current['start_token'] == record['start_token']:
            survivors.append(current)
    return survivors


class Child:
    def __init__(self, argv, cwd, label):
        self.label = label
        self.log = cwd / f'{label}.log'
        self.output = self.log.open('xb')
        os.chmod(self.log, 0o600)
        self.process = subprocess.Popen([sys.executable, str(Path(__file__).with_name('limits.py')), *argv], cwd=cwd, stdout=self.output, stderr=subprocess.STDOUT, start_new_session=True,
                                        env={**os.environ, 'PYTHONNOUSERSITE': '1'})
        self.token = start_token(self.process.pid)
        self.descendants = {}

    def inventory(self):
        # start_new_session binds an exact session/process-group to the child.
        # PPID ancestry also captures descendants that create a new session.
        candidates = {}
        for path in Path('/proc').iterdir():
            if path.name.isdecimal():
                try:
                    record = process_record(int(path.name))
                except (FileNotFoundError, PermissionError, ValueError):
                    continue
                candidates[record['pid']] = record
        leader_live = self.process.poll() is None and start_token(self.process.pid) == self.token
        owned = {self.process.pid} if leader_live else set()
        changed = True
        while changed:
            changed = False
            for pid, record in candidates.items():
                previously_bound = self.descendants.get(pid, {}).get('start_token') == record['start_token']
                if pid not in owned and (previously_bound or record['ppid'] in owned or (leader_live and record['session'] == self.process.pid)):
                    owned.add(pid)
                    self.descendants[pid] = record
                    changed = True
                    if len(self.descendants) > 128:
                        raise ValueError('task descendant inventory bound exceeded')
        return list(self.descendants.values())

    def identity(self):
        if self.process.poll() is not None or start_token(self.process.pid) != self.token:
            raise ValueError('owned process exited or identity changed')
        executable = Path(os.readlink(f'/proc/{self.process.pid}/exe'))
        return {'pid': self.process.pid, 'start_token': self.token, 'exe': str(executable), 'exe_sha256': digest(executable)}

    def sample(self):
        if self.process.poll() is not None or start_token(self.process.pid) != self.token:
            raise ValueError('owned process exited or identity changed')
        self.inventory()
        identity = {'pid': self.process.pid, 'start_token': self.token}
        status = Path(f'/proc/{identity["pid"]}/status').read_text()
        rss = int(re.search(r'^VmRSS:\s+(\d+) kB', status, re.M)[1]) * 1024
        fd = len(list(Path(f'/proc/{identity["pid"]}/fd').iterdir()))
        if rss > MAX_RSS or fd > MAX_FD or self.log.stat().st_size > MAX_LOG:
            raise ValueError('fixed resource/log budget exceeded')
        return {**identity, 'rss_bytes': rss, 'fd': fd}

    def stop(self):
        self.inventory()
        # Signals target only inventoried PID/start-token/exe identities. A
        # changed or surviving descendant is an explicit cleanup failure.
        records = list(self.descendants.values())
        for requested_signal in (signal.SIGTERM, signal.SIGKILL):
            for record in reversed(records):
                current = surviving_descendants([record])
                if not current:
                    continue
                if current[0].get('exe_unavailable'):
                    continue
                if current[0]['exe'] != record['exe']:
                    raise ValueError('descendant executable changed before cleanup')
                os.kill(record['pid'], requested_signal)
            end = time.monotonic() + 1.0
            while time.monotonic() < end and surviving_descendants(records):
                time.sleep(0.02)
        if self.process.poll() is None:
            if start_token(self.process.pid) != self.token:
                raise ValueError('refusing to signal changed process identity')
            # Exact child PID, never an unresolved PID or broad process group.
            self.process.send_signal(signal.SIGTERM)
            try:
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                if start_token(self.process.pid) != self.token:
                    raise ValueError('refusing to kill changed process identity')
                self.process.kill()
                self.process.wait(timeout=3)
        self.output.close()
        if surviving_descendants(list(self.descendants.values())):
            raise ValueError('owned descendants survived cleanup')


class Monitor:
    def __init__(self, children):
        self.children = children
        self.before = {c.label: c.sample() for c in children}
        self.peak = {k: dict(v) for k, v in self.before.items()}
        self.error = None
        self.done = threading.Event()
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def run(self):
        while not self.done.wait(0.02):
            try:
                for child in self.children:
                    value = child.sample()
                    for key in ('rss_bytes', 'fd'):
                        self.peak[child.label][key] = max(self.peak[child.label][key], value[key])
            except (OSError, ValueError) as exc:
                self.error = str(exc)
                return

    def finish(self):
        self.done.set()
        self.thread.join(timeout=1)
        if self.error:
            raise ValueError(self.error)
        return {'before': self.before, 'peak': self.peak, 'after': {c.label: c.sample() for c in self.children}}


def free_ports():
    sockets = []
    try:
        for _ in range(4):
            connection = socket.socket()
            connection.bind(('127.0.0.1', 0))
            sockets.append(connection)
        return [s.getsockname()[1] for s in sockets]
    finally:
        for connection in sockets:
            connection.close()


def wait_port(port, children):
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        for child in children:
            child.sample()
        try:
            if not owns_listener(children[-1], port):
                time.sleep(0.05)
                continue
            with socket.create_connection(('127.0.0.1', port), timeout=0.1):
                return
        except OSError:
            time.sleep(0.05)
    raise ValueError('listener readiness timeout')


def _mount_field(value):
    for encoded, decoded in ((r'\040', ' '), (r'\011', '\t'),
                             (r'\012', '\n'), (r'\134', '\\')):
        value = value.replace(encoded, decoded)
    return value


def mounted_device_for_path(process_root, path):
    selected = None
    for line in (process_root / 'mountinfo').read_text().splitlines():
        fields = line.split()
        if len(fields) < 7 or '-' not in fields:
            raise ValueError('invalid process mountinfo record')
        mountpoint = _mount_field(fields[4])
        if path == mountpoint or path.startswith(mountpoint.rstrip('/') + '/'):
            device = tuple(int(part, 10) for part in fields[2].split(':'))
            if len(device) != 2:
                raise ValueError('invalid process mount device')
            if selected is None or len(mountpoint) > selected[0]:
                selected = (len(mountpoint), device)
    if selected is None:
        raise ValueError('mapped library has no process mount')
    return selected[1]


def loaded_library(child, expected_sha256):
    mappings = Path(f'/proc/{child.process.pid}/maps').read_text().splitlines()
    libraries = sorted({line.split(maxsplit=5)[5] for line in mappings if len(line.split(maxsplit=5)) == 6 and '/libmodsecurity.so' in line})
    if len(libraries) != 1:
        raise ValueError('composite must load exactly one bound libmodsecurity')
    result = []
    for path in libraries:
        library = trusted_path(Path(path))
        metadata = library.stat()
        segments = set()
        for line in mappings:
            fields = line.split(maxsplit=5)
            if len(fields) == 6 and fields[5] == path:
                segments.add((fields[3], int(fields[4])))
        if len(segments) != 1:
            raise ValueError('loaded library mapping identity differs between segments')
        map_device_text, map_inode = next(iter(segments))
        mapped_device = tuple(int(part, 16) for part in map_device_text.split(':'))
        opened_device = (os.major(metadata.st_dev), os.minor(metadata.st_dev))
        translation = mapped_device != opened_device
        if translation:
            own_namespace = os.stat('/proc/self/ns/mnt')
            child_namespace = os.stat(f'/proc/{child.process.pid}/ns/mnt')
            if ((own_namespace.st_dev, own_namespace.st_ino) !=
                    (child_namespace.st_dev, child_namespace.st_ino)):
                raise ValueError('loaded library path is in a different mount namespace')
            if mounted_device_for_path(Path(f'/proc/{child.process.pid}'), path) != mapped_device:
                raise ValueError('loaded library device has no process-mount binding')
        if map_inode != metadata.st_ino:
            raise ValueError('loaded library mapping inode/device differs from hashed file')
        result.append({'path': str(library), 'sha256': digest(library),
                       'map_device': map_device_text,
                       'opened_device': f'{os.major(metadata.st_dev):02x}:{os.minor(metadata.st_dev):02x}',
                       'device_translation_verified': translation,
                       'inode': metadata.st_ino})
    if result[0]['sha256'] != expected_sha256:
        raise ValueError('loaded libmodsecurity hash does not match operator pin')
    return result


def owned_sockets(child):
    child.identity()
    sockets = []
    for descriptor in Path(f'/proc/{child.process.pid}/fd').iterdir():
        try:
            target = os.readlink(descriptor)
        except FileNotFoundError:
            continue
        if target.startswith('socket:['):
            sockets.append({'fd': int(descriptor.name), 'inode': int(target[8:-1])})
    return sorted(sockets, key=lambda item: item['fd'])


def owns_listener(child, port):
    inodes = {str(value['inode']) for value in owned_sockets(child)}
    for table in ('tcp', 'tcp6'):
        for line in Path(f'/proc/{child.process.pid}/net/{table}').read_text().splitlines()[1:]:
            fields = line.split()
            if fields[3] == '0A' and int(fields[1].split(':')[1], 16) == port and fields[9] in inodes:
                return True
    return False


def render(profile, args, root, ports):
    listener, upstream, auth, admin = ports
    events = root / 'events.jsonl'
    service = [str(args.composite_bin), '--mode', profile, '--runtime-config', str(args.runtime_config), '--event-log', str(events)]
    if profile == 'envoy':
        text = (REPO / 'connectors/envoy/config/envoy-ext-authz-composite.yaml.in').read_text()
        values = {'@LISTEN_PORT@': listener, '@UPSTREAM_PORT@': upstream, '@AUTHZ_PORT@': auth, '@ADMIN_PORT@': admin,
                  '@TLS_CERTIFICATE@': args.cert, '@TLS_PRIVATE_KEY@': args.key, '@EXT_PROC_METADATA_NAMESPACE@': 'envoy.filters.http.ext_authz'}
        config = root / 'envoy.yaml'
        service += ['--listen', f'127.0.0.1:{auth}']
        host = [str(args.host_bin), '-c', str(config), '--base-id', str(listener + admin), '--disable-hot-restart', '--concurrency', '2', '--log-level', 'error']
        configs = [(config, text, values)]
        uds = None
    else:
        uds = root / 'c.sock'
        if len(str(uds).encode()) > 100:
            raise ValueError('runtime root too long for private UDS')
        plugin = root / 'plugins-local/src/github.com/Easton97-Jens/ModSecurity-conector/connectors/traefik/composite_middleware'
        source = REPO / 'connectors/traefik/composite_middleware'
        for item in source.rglob('*'):
            trusted_path(item)
        shutil.copytree(source, plugin)
        config = root / 'static.yaml'
        dynamic = root / 'dynamic.yaml'
        values = {'__TRAEFIK_ADDRESS__': f'127.0.0.1:{listener}', '__TRAEFIK_DYNAMIC_CONFIG__': dynamic,
                  '__AUTH_ADDRESS__': f'127.0.0.1:{auth}', '__COMPOSITE_SOCKET__': uds,
                  '__UPSTREAM_ADDRESS__': f'127.0.0.1:{upstream}', '__UPSTREAM_CERTIFICATE__': args.cert}
        configs = [(config, (REPO / 'connectors/traefik/config/traefik-forwardauth-composite-static.yaml').read_text(), values),
                   (dynamic, (REPO / 'connectors/traefik/config/traefik-forwardauth-composite-dynamic.yaml').read_text(), values)]
        service += ['--forwardauth-listen', f'127.0.0.1:{auth}', '--uds', str(uds)]
        host = [str(args.host_bin), '--configFile', str(config)]
    for path, text, values in configs:
        if profile == 'traefik':
            text = render_traefik_yaml(text, values)
        else:
            for key, value in values.items():
                if any(c in str(value) for c in '\n\r"\\'):
                    raise ValueError('unsafe rendered value')
                text = text.replace(key, str(value))
        if re.search(r'@[A-Z_]+@|__[A-Z_]+__', text):
            raise ValueError('unrendered template placeholder')
        with path.open('x') as output:
            os.chmod(path, 0o600)
            output.write(text)
    return service, host, events, uds


def render_traefik_yaml(template, values):
    values = {key: str(value) for key, value in values.items()}
    if any(any(ord(c) < 32 or ord(c) == 127 for c in value) for value in values.values()):
        raise ValueError('control bytes in YAML interpolation')
    if any(re.search(r'__[A-Z_]+__', value) for value in values.values()):
        raise ValueError('template token in YAML interpolation value')
    def substitute(scalar):
        for key, value in values.items():
            scalar = scalar.replace(key, value)
        return scalar
    rendered = []
    for line in template.splitlines(keepends=True):
        if not any(key in line for key in values):
            rendered.append(line)
            continue
        newline = '\n' if line.endswith('\n') else ''
        if line.lstrip().startswith('#'):
            # Comments are not values; control bytes remain prohibited.
            rendered.append(substitute(line))
            continue
        match = re.fullmatch(r'(\s*(?:-\s+)?[A-Za-z][A-Za-z0-9_-]*:\s*|\s*-\s+)(.+?)\s*', line.rstrip('\n'))
        if not match:
            raise ValueError('unsupported YAML placeholder context')
        prefix, scalar = match.groups()
        if scalar.startswith('"'):
            scalar = json.loads(scalar)
            if not isinstance(scalar, str):
                raise ValueError('YAML interpolation requires string scalar')
        elif scalar.startswith(("'", '|', '>')):
            raise ValueError('unsupported YAML scalar quoting')
        # Quote the whole URL/path, including literal prefix and suffix.
        # JSON double-quoted strings are valid YAML scalar strings.
        rendered.append(prefix + json.dumps(substitute(scalar), ensure_ascii=True) + newline)
    return ''.join(rendered)


def connect(profile, port, cert, timeout=REQUEST_TIMEOUT):
    connection = socket.create_connection(('127.0.0.1', port), timeout=REQUEST_TIMEOUT)
    connection.settimeout(timeout)
    if profile == 'envoy':
        context = ssl.create_default_context(cafile=str(cert))
        connection = context.wrap_socket(connection, server_hostname='127.0.0.1')
    return connection


def private_read(path, maximum):
    trusted_path(path.parent, private=True)
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        metadata = os.fstat(fd)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_uid != os.getuid() or stat.S_IMODE(metadata.st_mode) != 0o600 or metadata.st_nlink != 1 or metadata.st_size > maximum:
            raise ValueError('receipt must be bounded private single-link regular file')
        data = bytearray()
        while len(data) <= maximum:
            chunk = os.read(fd, min(4096, maximum + 1 - len(data)))
            if not chunk:
                break
            data.extend(chunk)
        if len(data) > maximum:
            raise ValueError('receipt size budget exceeded')
        return data.decode('utf-8')
    finally:
        os.close(fd)


def read_events(path):
    deadline = time.monotonic() + 0.5
    while True:
        text = private_read(path, MAX_LOG)
        lines = text.splitlines()
        if len(lines) > 1024 or any(len(line.encode('utf-8')) > 2048 for line in lines):
            raise ValueError('event record/count bound exceeded')
        # Observer writes a record then its newline. Only an unfinished tail
        # warrants retry. Completed malformed JSON is a permanent failure.
        if text and not text.endswith('\n'):
            if time.monotonic() >= deadline:
                raise ValueError('unfinished event JSON exceeded retry budget')
            time.sleep(0.02)
            continue
        return [json.loads(line, object_pairs_hook=unique_json_object) for line in lines]


def unique_json_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON metadata field')
        result[key] = value
    return result


def backend_count(path):
    return backend_observation(path)['requests_seen']


def backend_observation(path):
    value = json.loads(private_read(path, 16384))
    integer_fields = {'requests_seen', 'parallel_requests_seen', 'parallel_max_inflight', 'parallel_inflight', 'parallel_barrier_passes', 'parallel_barrier_errors'}
    if not isinstance(value, dict) or set(value) != integer_fields | {'lease_header_observed'} or any(type(value[key]) is not int or not 0 <= value[key] <= 100 for key in integer_fields) or type(value['lease_header_observed']) is not bool:
        raise ValueError('invalid bounded backend receipt schema')
    if value['lease_header_observed']:
        raise ValueError('private lease leaked upstream')
    return value


def run_start(profile, args, root, deadline):
    ports = free_ports()
    service_argv, host_argv, events, uds = render(profile, args, root, ports)
    children = []
    monitor = None
    result = {'start': root.name, 'requests': [], 'catalog_acceptance': False,
              'gates': dict.fromkeys(('G2', 'G5', 'G6'), 'not_run')}
    uds_identity = None
    try:
        upstream = Child([sys.executable, str(Path(__file__).with_name('upstream.py')), '--port', str(ports[1]), '--root', str(root), '--cert', str(args.cert), '--key', str(args.key)], root, 'upstream')
        children.append(upstream)
        wait_port(ports[1], children)
        service = Child(service_argv, root, 'service')
        children.append(service)
        wait_port(ports[2], children)
        host = Child(host_argv, root, 'host')
        children.append(host)
        wait_port(ports[0], children)
        # Traefik binds before installing the provider. Wait without generating
        # unaccounted HTTP requests or corresponding server lifecycle events.
        time.sleep(1)
        result['processes'] = {c.label: c.identity() for c in children}
        result['libmodsecurity_before'] = loaded_library(service, args.library_sha256)
        result['sockets'] = {'ports': ports, 'uds': str(uds) if uds else None}
        result['effective_config'] = {path.name: digest(path) for path in root.glob('*.yaml')}
        if uds:
            metadata = uds.lstat()
            if not stat.S_ISSOCK(metadata.st_mode) or metadata.st_uid != os.getuid():
                raise ValueError('private socket was not created by operator')
            uds_identity = (metadata.st_dev, metadata.st_ino)
        result['sockets']['before'] = {c.label: owned_sockets(c) for c in children}
        monitor = Monitor(children)
        expected = Counter()
        observation = root / 'upstream-observation.json'

        def request(case, connection=None, persistent=False, parallel=False):
            if time.monotonic() >= deadline:
                raise ValueError('campaign time budget exceeded')
            own = connection is None
            request_deadline = min(deadline, time.monotonic() + (ERROR_TIMEOUT if case == 'timeout' else REQUEST_TIMEOUT))
            connection = connect(profile, ports[0], args.cert, max(0.001, request_deadline - time.monotonic())) if own else connection
            try:
                connection.settimeout(max(0.001, request_deadline - time.monotonic()))
                connection.sendall(request_wire(case, ports[0], parallel))
                status = read_response(connection, persistent, request_deadline)
                if status != EXPECTED[case]:
                    raise ValueError('unexpected client status')
                return status
            finally:
                if own:
                    connection.close()

        def isolated(case, connection=None, persistent=False):
            prior_ids = {e['decision_id'] for e in read_events(events)}
            before = backend_count(observation)
            status = request(case, connection, persistent)
            after = backend_count(observation)
            delta = after - before
            if delta != (1 if case in {'allow', 'timeout'} else 0):
                raise ValueError('wrong actual backend delta')
            end = time.monotonic() + 3
            while True:
                fresh = [e for e in read_events(events) if e['decision_id'] not in prior_ids]
                try:
                    verify_events(fresh, {case: 1}, profile)
                    break
                except ValueError:
                    if time.monotonic() >= end:
                        raise
                    time.sleep(0.02)
            expected[case] += 1
            result['requests'].append({'case': case, 'status': status, 'backend_delta': delta,
                                       'isolated_server_ids': sorted({e['decision_id'] for e in fresh})})

        for case in ('allow', 'p1', 'p2'):
            isolated(case)
        result['gates']['G2'] = 'passed'
        identity = {c.label: c.identity() for c in children}
        isolated('oversize')
        isolated('allow')
        isolated('timeout')
        isolated('allow')
        if identity != {c.label: c.identity() for c in children}:
            raise ValueError('error recovery changed process identity')
        result['same_process_error_recovery'] = identity
        result['gates']['G5'] = 'passed'
        with connect(profile, ports[0], args.cert) as connection:
            socket_identity = {'fd': connection.fileno(), 'local': connection.getsockname(), 'peer': connection.getpeername()}
            for case in ('allow', 'p1', 'allow', 'p2'):
                isolated(case, connection, True)
                if socket_identity != {'fd': connection.fileno(), 'local': connection.getsockname(), 'peer': connection.getpeername()}:
                    raise ValueError('keepalive socket identity changed')
            result['keepalive_socket'] = socket_identity
        before = backend_count(observation)
        barrier = threading.Barrier(CLIENTS)

        def client(_index):
            barrier.wait(timeout=2)
            statuses, errors, timeouts = [], 0, 0
            for case in ('allow', 'p1', 'allow', 'p2'):
                try:
                    statuses.append(request(case, parallel=True))
                except TimeoutError:
                    timeouts += 1
                except (OSError, ValueError):
                    errors += 1
            return {'statuses': statuses, 'errors': errors, 'timeouts': timeouts}

        with ThreadPoolExecutor(max_workers=CLIENTS) as pool:
            parallel = list(pool.map(client, range(CLIENTS)))
        if any(v != {'statuses': [200, 403, 200, 403], 'errors': 0, 'timeouts': 0} for v in parallel):
            raise ValueError('parallel requests failed')
        if backend_count(observation) - before != 2 * CLIENTS:
            raise ValueError('parallel backend multiplicity mismatch')
        overlap_deadline = time.monotonic() + 1.0
        while True:
            overlap = backend_observation(observation)
            try:
                verify_parallel_overlap(overlap)
                break
            except ValueError:
                if time.monotonic() >= overlap_deadline:
                    raise
                time.sleep(0.02)
        expected.update({'allow': CLIENTS * 2, 'p1': CLIENTS, 'p2': CLIENTS})
        result['parallel'] = {'clients': CLIENTS, 'requests_per_client': PARALLEL_REQUESTS_PER_CLIENT,
                              'results': parallel, 'upstream_overlap': overlap, 'correlation': 'aggregate_server_ids_only'}
        end = time.monotonic() + 5
        while True:
            try:
                result['events'] = verify_events(read_events(events), dict(expected), profile)
                break
            except ValueError:
                if time.monotonic() > end:
                    raise
                time.sleep(0.05)
        result['resources'] = monitor.finish()
        result['libmodsecurity_after'] = loaded_library(service, args.library_sha256)
        if result['libmodsecurity_before'] != result['libmodsecurity_after']:
            raise ValueError('loaded library identity changed during start')
        result['sockets']['after'] = {c.label: owned_sockets(c) for c in children}
        monitor = None
        result['passed'] = True
        result['gates']['G6'] = 'passed'
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        result['error'] = str(exc)
        for gate, value in result['gates'].items():
            if value == 'not_run':
                result['gates'][gate] = 'failed'
        raise
    finally:
        if monitor:
            monitor.done.set()
            monitor.thread.join(timeout=1)
        finalize_cleanup(root, result, children, ports, uds, uds_identity)
    return result


def finalize_cleanup(root, result, children, ports, uds, uds_identity):
    cleanup_errors = []
    for child in reversed(children):
        try:
            child.stop()
        except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
            cleanup_errors.append(str(exc))
    process_absent, descendant_survivors = {}, {}
    for child in children:
        try:
            process_absent[child.label] = start_token(child.process.pid) != child.token
        except FileNotFoundError:
            process_absent[child.label] = True
        except OSError:
            process_absent[child.label] = False
            cleanup_errors.append('owned process absence could not be verified')
        if not process_absent[child.label]:
            cleanup_errors.append('owned process survived cleanup')
        try:
            descendant_survivors[child.label] = surviving_descendants(list(child.descendants.values()))
        except (OSError, ValueError):
            descendant_survivors[child.label] = [{'verification_failed': True}]
        if descendant_survivors[child.label]:
            cleanup_errors.append('owned descendants survived cleanup')
    ports_closed = {}
    for port in ports:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=0.1):
                ports_closed[str(port)] = False
                cleanup_errors.append('allocated listener survived cleanup')
        except ConnectionRefusedError:
            ports_closed[str(port)] = True
        except OSError:
            ports_closed[str(port)] = False
            cleanup_errors.append('could not prove allocated port closure')
    # Remove only the exact task-created socket, after all owners stopped.
    if uds and (uds.exists() or uds.is_symlink()):
        try:
            metadata = uds.lstat()
            if stat.S_ISSOCK(metadata.st_mode) and metadata.st_uid == os.getuid() and (metadata.st_dev, metadata.st_ino) == uds_identity:
                uds.unlink()
            else:
                cleanup_errors.append('unsafe leftover UDS')
        except OSError:
            cleanup_errors.append('private socket cleanup could not be verified')
    result['cleanup'] = {'passed': not cleanup_errors, 'errors': cleanup_errors,
                         'processes': {c.label: {'pid': c.process.pid, 'start_token': c.token, 'returncode': c.process.poll()} for c in children},
                         'process_absent': process_absent, 'ports_closed': ports_closed,
                         'descendants': {c.label: list(c.descendants.values()) for c in children},
                         'descendant_survivors': descendant_survivors,
                         'socket_absent': not uds or not (uds.exists() or uds.is_symlink())}
    if cleanup_errors:
        result['passed'] = False
        result['gates'] = dict.fromkeys(result['gates'], 'failed')
        result['error'] = 'owned cleanup failed: ' + '; '.join(cleanup_errors)
    write_json(root / 'start-result.json', result)
    if cleanup_errors:
        raise ValueError('owned cleanup failed')


def main(profile, argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('root', 'host-bin', 'composite-bin', 'runtime-config', 'rules-file', 'cert', 'key'):
        parser.add_argument('--' + name, required=True, type=Path)
    parser.add_argument('--rules-sha256', required=True)
    parser.add_argument('--library-sha256', required=True)
    args = parser.parse_args(argv)
    summary = {'profile': profile, 'catalog_acceptance': False, 'p4_strict': 'out_of_scope',
               'gates': {gate: 'not_run' for gate in ('G2', 'G5', 'G6')}, 'starts': [],
               'budgets': {'fresh_starts': FRESH_STARTS, 'clients': CLIENTS, 'requests_per_client': 4,
                           'request_seconds': REQUEST_TIMEOUT, 'error_request_seconds': ERROR_TIMEOUT, 'campaign_seconds': CAMPAIGN_TIMEOUT,
                           'log_bytes_per_process': MAX_LOG, 'rss_bytes_per_process': MAX_RSS, 'fd_per_process': MAX_FD,
                           'descendants_per_child': 128, 'descendant_stop_seconds_per_child': 2}}
    root_valid = False
    previous_umask = None
    try:
        for path in (args.host_bin, args.composite_bin, args.runtime_config, args.rules_file, args.cert, args.key):
            trusted_path(path)
            if not path.is_file():
                raise ValueError('input must be regular file')
        for binary in (args.host_bin, args.composite_bin):
            if not os.access(binary, os.X_OK):
                raise ValueError('binary must be executable')
        for path in (args.runtime_config, args.key):
            if path.stat().st_mode & 0o077:
                raise ValueError('runtime config and key must be private 0600 files')
        validate_runtime_root(args.root)
        root_valid = True
        previous_umask = os.umask(0o077)
        validate_rule_binding(args.runtime_config, args.rules_file, args.rules_sha256)
        if not re.fullmatch('[0-9a-f]{64}', args.library_sha256):
            raise ValueError('library hash must be exact lowercase SHA256')
        summary['library_sha256'] = args.library_sha256
        summary['inputs'] = {name: {'path': str(path), 'sha256': digest(path)} for name, path in vars(args).items() if isinstance(path, Path) and name != 'root'}
        summary['source_before'] = source_manifest()
        write_json(args.root / 'budgets.json', summary['budgets'])
        def alarm(_signal, _frame):
            raise TimeoutError('hard campaign time budget exceeded')
        previous_handler = signal.signal(signal.SIGALRM, alarm)
        signal.setitimer(signal.ITIMER_REAL, CAMPAIGN_TIMEOUT)
        deadline = time.monotonic() + CAMPAIGN_TIMEOUT
        try:
            for index in range(FRESH_STARTS):
                root = args.root / f'start-{index + 1}'
                root.mkdir(mode=0o700)
                start = run_start(profile, args, root, deadline)
                summary['starts'].append(start)
                if start.get('passed') is not True or start.get('cleanup', {}).get('passed') is not True or start.get('gates') != dict.fromkeys(('G2', 'G5', 'G6'), 'passed'):
                    raise ValueError('start generation did not qualify all gates and cleanup')
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, previous_handler)
        identities = [s['processes'] for s in summary['starts']]
        for label in ('host', 'service', 'upstream'):
            if len({(v[label]['pid'], v[label]['start_token']) for v in identities}) != FRESH_STARTS:
                raise ValueError('fresh starts reused process identity')
        for name, receipt in summary['inputs'].items():
            if digest(Path(receipt['path'])) != receipt['sha256']:
                raise ValueError('input changed during campaign')
        summary['source_after'] = source_manifest()
        if summary['source_before'] != summary['source_after']:
            raise ValueError('source changed during campaign')
        summary['gates'] = dict.fromkeys(summary['gates'], 'passed')
        summary['controlled_stop_start'] = True
        return 0
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        summary['error'] = str(exc)
        summary['gates'] = dict.fromkeys(summary['gates'], 'failed')
        return 1
    finally:
        if root_valid:
            if 'source_before' in summary and 'source_after' not in summary:
                try:
                    summary['source_after'] = source_manifest()
                    summary['source_unchanged'] = summary['source_after'] == summary['source_before']
                except (OSError, ValueError) as exc:
                    summary['source_after_error'] = str(exc)
            write_json(args.root / 'qualification-result.json', summary)
        if previous_umask is not None:
            os.umask(previous_umask)
        print(json.dumps({'profile': profile, 'gates': summary['gates'], 'catalog_acceptance': False}))


def source_manifest():
    result = {}
    for directory in ('common', 'include', 'src', 'connectors/envoy', 'connectors/traefik', 'connectors/composite_harness'):
        for path in (REPO / directory).rglob('*'):
            if path.suffix in {'.c', '.h', '.go', '.py', '.yaml', '.yml', '.json', '.sh', '.in', '.conf', '.proto', '.mod', '.sum'} and path.is_file():
                trusted_path(path)
                result[str(path.relative_to(REPO))] = digest(path)
    return result


def validate_runtime_root(root):
    if STORAGE_ROOT not in root.parents:
        raise ValueError('runtime root must be below approved external storage root')
    trusted_path(root, private=True)
    if not root.is_dir() or list(root.iterdir()) or root == REPO or REPO in root.parents:
        raise ValueError('root must be empty private external directory')


def validate_rule_binding(config, rules, expected_sha256):
    config_bytes = bound_input(config, 65536)
    rule_bytes = bound_input(rules, 256 * 1024)
    if not re.fullmatch('[0-9a-f]{64}', expected_sha256) or hashlib.sha256(rule_bytes).hexdigest() != expected_sha256:
        raise ValueError('rules hash must match exact operator SHA256 pin')
    if expected_sha256 != VETTED_VECTOR_SHA256:
        raise ValueError('rules must match the exact reviewed self-contained vector fixture')
    settings = {}
    for line in config_bytes.decode('utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        key, separator, value = line.partition('=')
        if not separator or key.strip() in settings:
            raise ValueError('malformed/duplicate runtime config key')
        settings[key.strip()] = value.strip()
    if settings.keys() & {'rules_remote_url', 'rules_remote_key', 'rules_inline'}:
        raise ValueError('runtime config selects an additional unpinned rule source')
    if settings.get('rules_file') != str(rules):
        raise ValueError('runtime config must select exactly the explicitly pinned rules file')
    # This narrow profile runner supports the self-contained vector fixture.
    # Includes/macros/globs cannot be silently treated as bound dependencies.
    if any(re.match(r'(?i)^\s*(?:include|includeoptional|secremoterules)\b', line) for line in rule_bytes.decode('utf-8').splitlines() if not line.lstrip().startswith('#')):
        raise ValueError('rules Include directives require a separate dependency resolver')


def verify_parallel_overlap(observation):
    if observation['parallel_requests_seen'] != CLIENTS * 2 or observation['parallel_max_inflight'] < CLIENTS or observation['parallel_barrier_passes'] != CLIENTS * 2 or observation['parallel_barrier_errors'] != 0 or observation['parallel_inflight'] != 0:
        raise ValueError('four-client overlap was not proven at actual upstream')


def bound_input(path, maximum):
    trusted_path(path)
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        metadata = os.fstat(fd)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_uid != os.getuid() or metadata.st_nlink != 1 or metadata.st_mode & 0o022 or metadata.st_size > maximum:
            raise ValueError('bound input must be trusted single-link bounded regular file')
        data = bytearray()
        while len(data) <= maximum:
            chunk = os.read(fd, min(4096, maximum + 1 - len(data)))
            if not chunk:
                break
            data.extend(chunk)
        if len(data) > maximum:
            raise ValueError('bound input grew beyond fixed size budget')
        return bytes(data)
    finally:
        os.close(fd)
