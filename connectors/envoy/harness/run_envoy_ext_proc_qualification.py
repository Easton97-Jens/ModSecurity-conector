#!/usr/bin/env python3
"""Bounded real-host diagnostics for direct Envoy ext_proc; no catalog award.

The versioned STREAMED profile is retained. In particular, a P2 denial that
has already dispatched headers upstream fails G3 even if its body was stopped.
The three source/binary pins identify inputs, not a reproducible-build claim.
"""
from __future__ import annotations

import argparse
import errno
import ctypes
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import hashlib
import http.client
import http.server
import json
import os
from pathlib import Path
import re
import signal
import select
import socket
import ssl
import stat
import subprocess
import threading
import time

REPO = Path(__file__).resolve().parents[3]
RUNNER = Path(__file__).absolute()
EXTERNAL = Path('/var/tmp/codex/ModSecurity-conector')
MAX_INPUT = 32 * 1024 * 1024
SOURCE_PREFIXES = ('common/', 'connectors/envoy/ext_proc/', 'connectors/envoy/config/')
QUALIFICATION_PROFILE = 'envoy-ext-proc-buffered-admission'
REDIRECT_LOCATION = '/qualification/redirect-target'
BOUNDARY_KINDS = ('exact', 'chunked-exact', 'chunked-p2', 'chunked-limit',
    'response-zero', 'response-exact', 'response-limit', 'redirect')
COMPLETION_KEYS = frozenset(('event', 'integration_mode', 'evaluation_mode',
    'rule_evaluation', 'transaction_id', 'request_header_count', 'response_header_count',
    'request_body_chunks', 'response_body_chunks', 'request_body_bytes',
    'response_body_bytes', 'late_action', 'close_reason'))
COMMON_TEXT = frozenset(('timestamp level message_id message event connector integration_mode '
    'transaction_id phase status action requested_action actual_action transport_result '
    'http_reason_phrase http_default_message rule_id reason method uri client_ip content_type').split())
COMMON_INT = frozenset(('http_status original_http_status visible_http_status body_bytes_seen '
    'body_bytes_inspected sequence previous_event_hash event_hash').split())
COMMON_BOOL = frozenset(('late_intervention response_started response_committed headers_sent '
    'body_started body_truncated connection_aborted client_disconnected upstream_disconnected '
    'cancelled eos_seen redacted truncated').split())
OPTIONAL_TEXT = frozenset(('run_id transport_case_id framework_case_id original_request_id request_id '
    'requested_protocol downstream_protocol upstream_protocol negotiated_protocol transport '
    'alpn stream_id connection_id quic_version stream_reset_code reset_by reset_code '
    'timeout_stage write_result cleanup_reason body_limit_outcome late_intervention_mode').split())
OPTIONAL_BOOL = frozenset(('connection_reused quic_connection_id_present fallback_used stream_reset').split())
RULES = '''SecRuleEngine On
SecRequestBodyAccess On
SecResponseBodyAccess On
SecResponseBodyMimeType text/plain
SecRule REQUEST_URI "@streq /qualification/p1" "id:1900001,phase:1,deny,status:403,log"
SecRule REQUEST_BODY "@contains qualification-p2" "id:1900002,phase:2,deny,status:403,log"
SecRule RESPONSE_HEADERS:X-Qualification "@streq p3" "id:1900003,phase:3,deny,status:403,log"
SecRule RESPONSE_BODY "@contains qualification-p4" "id:1900004,phase:4,deny,status:403,log"
SecRule RESPONSE_HEADERS:X-Qualification "@streq redirect" "id:1900005,phase:3,redirect:/qualification/redirect-target,status:302,log"
'''


class InvalidEvidence(ValueError):
    """Missing, unsafe or contradictory observation."""


def probe_body(kind):
    if kind in ('exact', 'chunked-exact'):
        return b'x' * 32
    if kind == 'chunked-p2':
        return b'qualification-p2'
    if kind == 'chunked-limit':
        return b'x' * 33
    return b'qualification-p2' if kind == 'p2' else b'x' * 33 if kind == 'limit' else b'' if kind == 'empty' else b'ok'


def response_body(kind):
    return b'' if kind == 'response-zero' else b'z' * 32 if kind == 'response-exact' else \
        b'z' * 33 if kind == 'response-limit' else b'qualification-p4' if kind == 'p4' else b'ok'


def client_receipt(response, kind):
    # Validate raw fields before HTTPResponse's permissive framing selection can
    # hide duplicate fields, invalid lengths or conflicting transfer codings.
    headers = response.getheaders()
    lengths = [value for name, value in headers if name.lower() == 'content-length']
    transfers = [value for name, value in headers if name.lower() == 'transfer-encoding']
    if len(lengths) > 1 or lengths and not re.fullmatch(r'0|[1-9][0-9]*', lengths[0], re.ASCII):
        raise InvalidEvidence('invalid client Content-Length')
    if len(transfers) > 1 or transfers and transfers[0].lower() != 'chunked' or lengths and transfers:
        raise InvalidEvidence('invalid or conflicting client Transfer-Encoding')
    expected_length = int(lengths[0]) if lengths else None
    if expected_length is not None and (expected_length > 65536 or response.length != expected_length or response.chunked):
        raise InvalidEvidence('client length exceeds bound or parser framing mismatch')
    if transfers and not response.chunked or not lengths and not transfers and (response.chunked or not response.will_close):
        raise InvalidEvidence('client response has no proven framing')
    safe_read = response._safe_read
    discard_trailer = response._read_and_discard_trailer
    next_chunk_size = response._read_next_chunk_size
    framing_bytes = 0
    body_bytes = 0
    chunk_count = 0

    def framing_line():
        nonlocal framing_bytes
        line = response.fp.readline(8192 - framing_bytes + 1)
        framing_bytes += len(line)
        if framing_bytes > 8192 or not line.endswith(b'\r\n'):
            raise InvalidEvidence('incomplete or oversized client chunk framing')
        return line

    def checked_chunk_size():
        nonlocal chunk_count
        chunk_count += 1
        if chunk_count > 1024:
            raise InvalidEvidence('client chunk count exceeds bound')
        line = framing_line()
        # This laboratory contract accepts no chunk extensions. In particular,
        # int(..., 16) alone also accepts signs and surrounding whitespace.
        if not re.fullmatch(rb'[0-9A-Fa-f]+\r\n', line):
            raise InvalidEvidence('invalid client chunk size')
        amount = int(line[:-2], 16)
        if amount > 65536 - body_bytes or amount and 8192 - framing_bytes < 2:
            raise InvalidEvidence('client chunk exceeds body or framing bound')
        return amount

    def checked_read(amount):
        nonlocal framing_bytes, body_bytes
        if type(amount) is not int or not 0 <= amount <= 65536:
            raise InvalidEvidence('unbounded client chunk read')
        delimiter = response.chunk_left == 0 and amount == 2
        if delimiter:
            if framing_bytes + amount > 8192:
                raise InvalidEvidence('client chunk delimiter exceeds framing bound')
            framing_bytes += amount
        elif amount > 65536 - body_bytes:
            raise InvalidEvidence('client chunk read exceeds body bound')
        data = safe_read(amount)
        # Stdlib otherwise discards two bytes without checking chunk CRLF.
        if delimiter and data != b'\r\n':
            raise InvalidEvidence('invalid client chunk delimiter')
        if not delimiter:
            body_bytes += len(data)
        return data

    def checked_trailer():
        while True:
            line = framing_line()
            if line == b'\r\n':
                return
            if not re.fullmatch(rb"[!#$%&'*+.^_`|~0-9A-Za-z-]+:[^\r\n]*\r\n", line):
                raise InvalidEvidence('invalid client chunk trailer')

    if transfers:
        response._safe_read = checked_read
        response._read_and_discard_trailer = checked_trailer
        response._read_next_chunk_size = checked_chunk_size
    try:
        body = response.read(65537)
        if len(body) > 65536 or response.read(1):
            raise InvalidEvidence('unbounded client response or missing EOS')
    except (http.client.HTTPException, ValueError, OSError) as error:
        raise InvalidEvidence('incomplete client response framing') from error
    finally:
        if transfers:
            response._safe_read = safe_read
            response._read_and_discard_trailer = discard_trailer
            response._read_next_chunk_size = next_chunk_size
    if not response.isclosed() or expected_length is not None and (response.length != 0 or len(body) != expected_length) or \
        transfers and response.chunk_left is not None:
        raise InvalidEvidence('client response lacks complete framed EOS')
    receipt = dict(bytes=len(body), sha256=hashlib.sha256(body).hexdigest(), eos=True)
    if kind not in ('p1', 'p2', 'limit', 'p3', 'chunked-p2', 'chunked-limit', 'redirect', 'unavailable'):
        expected = response_body(kind)
        if len(body) != len(expected) or receipt['sha256'] != hashlib.sha256(expected).hexdigest():
            raise InvalidEvidence('client response payload length/SHA mismatch')
    if kind == 'redirect':
        locations = [value for name, value in headers if name.lower() == 'location']
        if response.status != 302 or locations != [REDIRECT_LOCATION]:
            raise InvalidEvidence('redirect requires one exact safe Location')
        receipt['location'] = locations[0]
    return receipt


def send_chunked_request(client, identifier, kind, route):
    body = probe_body(kind)
    client.putrequest('POST', route)
    client.putheader('X-Request-Id', identifier)
    client.putheader('Transfer-Encoding', 'chunked')
    client.endheaders()
    split = len(body) // 2
    chunks = (body[:split], body[split:])
    for index, chunk in enumerate(chunks):
        if index:
            time.sleep(.1)
        client.send(f'{len(chunk):x}\r\n'.encode() + chunk + b'\r\n')
    client.send(b'0\r\n\r\n')
    return dict(chunks=2, bytes=len(body), sha256=hashlib.sha256(body).hexdigest(),
        delay_seconds=.1, framing='downstream_chunked', eos=True)


def verify_unavailable(identifier, status, dispatched, completions, events):
    # Versioned ext_proc template has no status_on_error override: unreachable
    # processor is HTTP500; native processing timeout is a separate HTTP504.
    if status != 500 or dispatched != 0 or any(r.get('transaction_id') == identifier for r in completions + events):
        raise InvalidEvidence('unreachable processor must fail500 before backend/engine')


def verify_cancel(identifier, completions, events, dispatched, client_bytes):
    for record in completions:
        validate_completion(record)
    for record in events:
        validate_common(record)
    selected = [r for r in completions if r.get('transaction_id') == identifier]
    if len(selected) != 1 or dispatched != 1 or client_bytes != 1:
        raise InvalidEvidence('cancel must close one actually started stream')
    record = selected[0]
    if record['close_reason'] not in ('grpc_context_canceled_unattributed', 'grpc_peer_eof') or \
        record['request_body_bytes'] != 2 or not 3 <= record['response_header_count'] <= 64 or \
        not 1 <= record['response_body_bytes'] < 32 or record['response_body_chunks'] < 1 or \
        record['late_action'] != 'none':
        raise InvalidEvidence('cancel completion lacks started partial response/cancel evidence')
    selected_events = [r for r in events if r['transaction_id'] == identifier]
    if len(selected_events) != 1:
        raise InvalidEvidence('cancel requires exactly one correlated Common event')
    event = selected_events[0]
    expected = dict(event='client_cancel', message_id='MSCONN_EVENT_CLIENT_CANCEL',
        phase='response_headers', status='blocked', action='abort_connection',
        requested_action='abort_connection', actual_action='abort_connection',
        http_status=0, original_http_status=200, visible_http_status=200,
        transport_result='', rule_id='', body_bytes_seen=record['response_body_bytes'],
        body_bytes_inspected=record['response_body_bytes'], late_intervention=False,
        response_started=True, response_committed=True, headers_sent=True,
        body_started=True, body_truncated=False, connection_aborted=False,
        client_disconnected=True, upstream_disconnected=False, cancelled=True,
        eos_seen=False, sequence=1)
    if any(event.get(key) != value for key, value in expected.items()):
        raise InvalidEvidence('Common cancel event contradicts partial response lifecycle')


def stable_identity(identity):
    return {key: identity[key] for key in ('pid', 'start', 'exe', 'ppid', 'session')}


def verify_origin_probe(origin, identifier, kind):
    """Compare the origin's actual payload/EOS to the fixed client fixture."""
    with origin.lock:
        headers = origin.observations.get(identifier, 0)
        receipts = origin.body_receipts.get(identifier, []).copy()
    expected_count = 0 if kind in ('p1', 'p2', 'limit', 'chunked-p2', 'chunked-limit', 'unavailable') else 1
    if headers != expected_count or len(receipts) != expected_count:
        raise InvalidEvidence('origin header/body receipt count contradicts probe')
    if receipts:
        receipt = receipts[0]
        expected = probe_body(kind)
        if receipt.get('eos') is not True or type(receipt.get('bytes')) is not int or \
            receipt['bytes'] != len(expected) or receipt.get('sha256') != hashlib.sha256(expected).hexdigest():
            raise InvalidEvidence('origin payload/EOS contradicts fixed probe body')


def checked_path(path: Path) -> Path:
    """Reject links at every component and config metacharacters."""
    if not path.is_absolute() or '..' in path.parts or not re.fullmatch(r'[A-Za-z0-9_./+-]+', str(path)):
        raise InvalidEvidence('unsafe absolute path')
    current = Path('/')
    for part in path.parts[1:]:
        current /= part
        info = current.lstat()
        if stat.S_ISLNK(info.st_mode):
            raise InvalidEvidence('symlink path component')
        if current != path and (not stat.S_ISDIR(info.st_mode) or info.st_uid not in (0, os.getuid()) or
            info.st_mode & 0o022 and not info.st_mode & stat.S_ISVTX):
            raise InvalidEvidence('untrusted ancestor directory')
    return path


def read_safe(path: Path, maximum: int = MAX_INPUT, with_metadata=False):
    checked_path(path)
    directory = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
    try:
        for component in path.parts[1:-1]:
            child = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory)
            os.close(directory)
            directory = child
            info = os.fstat(directory)
            if info.st_uid not in (0, os.getuid()) or info.st_mode & 0o022 and not info.st_mode & stat.S_ISVTX:
                raise InvalidEvidence('untrusted descriptor ancestor')
        fd = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
    finally:
        os.close(directory)
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or before.st_size > maximum or \
            before.st_uid not in (0, os.getuid()) or before.st_mode & 0o022:
            raise InvalidEvidence('input must be a bounded single-link regular file')
        data = bytearray()
        while len(data) <= maximum:
            chunk = os.read(fd, min(65536, maximum + 1 - len(data)))
            if not chunk:
                break
            data.extend(chunk)
        after = os.fstat(fd)
        if len(data) > maximum or (before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (
            after.st_size, after.st_mtime_ns, after.st_ctime_ns):
            raise InvalidEvidence('input changed or exceeded bound')
        return (bytes(data), after) if with_metadata else bytes(data)
    finally:
        os.close(fd)


def digest(path: Path, expected: str, maximum: int = 512 * 1024 * 1024) -> dict:
    if not re.fullmatch(r'[0-9a-f]{64}', expected):
        raise InvalidEvidence('SHA256 must be canonical lowercase hexadecimal')
    actual = hashlib.sha256(read_safe(path, maximum)).hexdigest()
    if actual != expected:
        raise InvalidEvidence('input SHA256 mismatch')
    info = path.stat()
    return dict(path=str(path), sha256=actual, dev=info.st_dev, inode=info.st_ino)


def source_digest() -> str:
    files = subprocess.check_output(['rtk', 'proxy', 'git', '-C', str(REPO), 'ls-files', '-z',
        '--cached', '--others', '--exclude-standard', '--', *SOURCE_PREFIXES,
        'connectors/envoy/harness/run_envoy_ext_proc_qualification.py',
        'tests/test_envoy*', 'tests/test_common*'])
    result = hashlib.sha256()
    for name in sorted(set(files.decode().split('\0'))):
        if name:
            result.update(name.encode() + b'\0' + hashlib.sha256(read_safe(REPO / name)).digest())
    return result.hexdigest()


def runner_identity(expected=None, path=None):
    path = RUNNER if path is None else path
    data, info = read_safe(path, MAX_INPUT, with_metadata=True)
    sha256 = hashlib.sha256(data).hexdigest()
    if expected is not None and (not re.fullmatch(r'[0-9a-f]{64}', expected) or sha256 != expected):
        raise InvalidEvidence('runner SHA256 mismatch')
    return dict(path=str(path), sha256=sha256, dev=info.st_dev, inode=info.st_ino,
        size=info.st_size, mtime_ns=info.st_mtime_ns, ctime_ns=info.st_ctime_ns)


def verify_runner(pin):
    if runner_identity(pin['sha256'], Path(pin['path'])) != pin:
        raise InvalidEvidence('runner identity changed during campaign')


def pinned_starts(args, library_pin, runner_pin):
    starts = []
    try:
        for index in range(1, 4):
            verify_runner(runner_pin)
            starts.append(run_start(args, args.root / f'start-{index}', index, library_pin))
            verify_runner(runner_pin)
        verify_runner(runner_pin)
    except (OSError, ValueError) as error:
        write_new(args.root / 'qualification.json', json.dumps(dict(passed=False, catalog_acceptance=False,
            runner_sha256=runner_pin['sha256'], runner_pin=runner_pin, runner_pin_verified=False,
            starts=starts, errors=[str(error)]), sort_keys=True, indent=2).encode())
        raise
    return starts


def pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise InvalidEvidence('duplicate JSON key')
        result[key] = value
    return result


def jsonl(path: Path) -> list[dict]:
    raw = read_safe(path)
    if raw and not raw.endswith(b'\n'):
        raise InvalidEvidence('partial event record')
    result = []
    for line in raw.splitlines():
        if not line or len(line) > 16384:
            raise InvalidEvidence('empty or excessive event record')
        value = json.loads(line, object_pairs_hook=pairs, parse_constant=lambda _: (_ for _ in ()).throw(InvalidEvidence('nonfinite JSON')))
        if type(value) is not dict:
            raise InvalidEvidence('event is not an object')
        result.append(value)
    return result


def await_records(directory, identifier):
    deadline = time.monotonic() + 3
    while True:
        try:
            complete = jsonl(directory / 'completion.jsonl')
            events = jsonl(directory / 'common.jsonl') if (directory / 'common.jsonl').exists() else []
            if any(r.get('transaction_id') == identifier for r in complete):
                return complete, events
        except (FileNotFoundError, InvalidEvidence, json.JSONDecodeError):
            if time.monotonic() >= deadline:
                raise
        if time.monotonic() >= deadline:
            raise InvalidEvidence('completion timeout')
        time.sleep(.05)


def validate_completion(record: dict):
    attributable = 'transaction_id' in record
    if set(record) != (COMPLETION_KEYS if attributable else COMPLETION_KEYS - {'transaction_id'}) or record['event'] != 'ext_proc_stream_complete' or \
        record['integration_mode'] != 'ext_proc' or record['evaluation_mode'] != 'common_libmodsecurity_nonpromoted' or \
        record['rule_evaluation'] != 'libmodsecurity':
        raise InvalidEvidence('unexpected completion schema/engine')
    for key in COMPLETION_KEYS - {'event', 'integration_mode', 'evaluation_mode', 'rule_evaluation',
        'transaction_id', 'late_action', 'close_reason'}:
        if type(record[key]) is not int or not 0 <= record[key] <= 1 << 30:
            raise InvalidEvidence('invalid completion counter')
    if not attributable:
        if record['close_reason'] != 'grpc_context_canceled_unattributed' or record['late_action'] != 'none' or \
            any(record[key] for key in COMPLETION_KEYS - {'event', 'integration_mode', 'evaluation_mode',
                'rule_evaluation', 'transaction_id', 'late_action', 'close_reason'}):
            raise InvalidEvidence('unattributed stream contains processing evidence')
        return
    if not re.fullmatch(r'q[0-9]+-[a-z0-9-]+', record['transaction_id']) or record['late_action'] not in ('none', 'log_only'):
        raise InvalidEvidence('unexpected completion identity/action')
    if record['close_reason'] not in ('response_end_of_stream', 'request_immediate_response',
        'grpc_peer_eof', 'grpc_context_canceled_unattributed', 'processor_error',
        'grpc_stream_idle_timeout', 'grpc_stream_max_lifetime'):
        raise InvalidEvidence('unexpected completion close reason')


def validate_common(record: dict):
    required = COMMON_TEXT | COMMON_INT | COMMON_BOOL
    if not required <= set(record) or set(record) - (required | OPTIONAL_TEXT | OPTIONAL_BOOL):
        raise InvalidEvidence('unexpected Common schema or payload field')
    for key in COMMON_TEXT | (OPTIONAL_TEXT & set(record)):
        if type(record[key]) is not str or len(record[key]) > 4096:
            raise InvalidEvidence('invalid event text')
    for key in COMMON_INT:
        if type(record[key]) is not int or not 0 <= record[key] <= (1 << 64) - 1:
            raise InvalidEvidence('invalid event number')
    for key in COMMON_BOOL | (OPTIONAL_BOOL & set(record)):
        if type(record[key]) is not bool:
            raise InvalidEvidence('invalid event flag')
    if record['connector'] != 'envoy' or record['integration_mode'] != 'ext_proc' or \
        not re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z', record['timestamp']) or \
        not re.fullmatch(r'q[0-9]+-[a-z0-9-]+', record['transaction_id']) or record['truncated']:
        raise InvalidEvidence('wrong profile, identity, timestamp or truncated event')
    if record['body_bytes_inspected'] > record['body_bytes_seen']:
        raise InvalidEvidence('impossible body counters')
    try:
        datetime.fromisoformat(record['timestamp'].replace('Z', '+00:00'))
    except ValueError as error:
        raise InvalidEvidence('invalid UTC event timestamp') from error


def verify_probe(transaction_id, status, dispatched, completions, events, kind):
    selected_kind = kind
    response_limit = kind == 'response-limit'
    redirect = kind == 'redirect'
    kind = {'exact': 'allow', 'chunked-exact': 'allow', 'chunked-p2': 'p2',
        'chunked-limit': 'limit', 'response-zero': 'allow', 'response-exact': 'allow',
        'response-limit': 'allow', 'redirect': 'p3'}.get(kind, kind)
    for record in completions:
        validate_completion(record)
    for record in events:
        validate_common(record)
    matching = [r for r in completions if r.get('transaction_id') == transaction_id]
    if len(matching) != 1:
        raise InvalidEvidence('missing or duplicated completion')
    completion = matching[0]
    if not 3 <= completion['request_header_count'] <= 64:
        raise InvalidEvidence('missing or implausible request header processing')
    request_bytes = 0 if kind == 'p1' else len(probe_body(selected_kind))
    if completion['request_body_bytes'] != request_bytes or not (
        (request_bytes == 0 and completion['request_body_chunks'] <= 1) or
        (request_bytes > 0 and 1 <= completion['request_body_chunks'] <= request_bytes)):
        raise InvalidEvidence('request body counters contradict selected probe')
    if request_bytes > 0 and completion['request_body_chunks'] != 1:
        raise InvalidEvidence('buffered admission must deliver exactly one native request body')
    response = kind in ('allow', 'empty', 'p3', 'p4')
    if response:
        if not 3 <= completion['response_header_count'] <= 64:
            raise InvalidEvidence('missing response header processing')
    elif completion['response_header_count'] or completion['response_body_chunks'] or completion['response_body_bytes']:
        raise InvalidEvidence('request denial processed a response')
    response_bytes = len(response_body(selected_kind)) if kind in ('allow', 'empty', 'p4') else 0
    if completion['response_body_bytes'] != response_bytes or not (
        (response_bytes == 0 and completion['response_body_chunks'] == 0) or
        (response_bytes > 0 and 1 <= completion['response_body_chunks'] <= response_bytes)):
        raise InvalidEvidence('response body counters contradict selected probe')
    if completion['late_action'] != ('log_only' if kind == 'p4' or response_limit else 'none'):
        raise InvalidEvidence('unexpected completion late action')
    matching_events = [r for r in events if r['transaction_id'] == transaction_id]
    expected_events = 0 if kind in ('allow', 'empty') else 1 if kind == 'limit' else 2
    if len(matching_events) != expected_events:
        raise InvalidEvidence('unexpected Common intervention count')
    phase_order = dict(request_headers=1, request_body=2, response_headers=3, response_body=4)
    previous = None
    for record in matching_events:
        if record['phase'] not in phase_order:
            raise InvalidEvidence('unknown phase in selected transaction')
        current = (phase_order[record['phase']], record['sequence'], record['timestamp'])
        if previous and (current[0] < previous[0] or current[1] <= previous[1] or current[2] < previous[2]):
            raise InvalidEvidence('impossible event ordering')
        previous = current
    expected = dict(allow=(200, 1, None), empty=(200, 1, None),
        p1=(403, 0, '1900001'), p2=(403, 0, '1900002'),
        limit=(413, 0, None), p3=(403, 1, '1900003'), p4=(200, 1, '1900004'))[kind]
    if redirect:
        expected = (302, 1, '1900005')
    if (status, dispatched) != expected[:2]:
        raise InvalidEvidence(f'{kind} client/backend mismatch: status={status}, upstream_headers={dispatched}')
    if kind in ('allow', 'empty', 'p4') and completion['close_reason'] != 'response_end_of_stream':
        raise InvalidEvidence('allow did not reach response EOS')
    if kind in ('p1', 'p2', 'limit', 'p3') and completion['close_reason'] != 'request_immediate_response':
        raise InvalidEvidence('request block did not complete immediate response')
    if kind == 'empty' and completion['request_body_bytes'] != 0:
        raise InvalidEvidence('empty body observation mismatch')
    if kind == 'allow' and completion['request_body_bytes'] != len(probe_body(selected_kind)):
        raise InvalidEvidence('nonempty body observation mismatch')
    if kind in ('p1', 'p2', 'p3', 'p4', 'limit'):
        selected = [r for r in matching_events if (expected[2] is None or r['rule_id'] == expected[2]) and
            r['visible_http_status'] == status and r['transport_result'] == ('log_only' if kind == 'p4' else 'http_status')]
        if len(selected) != 1:
            raise InvalidEvidence('missing uniquely correlated host action')
        event = selected[0]
        if kind == 'limit':
            # The native runtime budget rejects before rule evaluation and
            # emits its one host-confirmed terminal BODY_LIMIT event.
            if event['sequence'] != 1:
                raise InvalidEvidence('unexpected native body-limit event sequence')
        else:
            engine_event = matching_events[0]
            if matching_events[1] is not event or engine_event['sequence'] != 1 or event['sequence'] != 2 or \
                not engine_event['event_hash'] or event['previous_event_hash'] != engine_event['event_hash'] or \
                engine_event['actual_action'] != ('redirect' if redirect else 'deny') or engine_event['transport_result'] != '' or \
                engine_event['visible_http_status'] != (200 if kind in ('p3', 'p4') else 0):
                raise InvalidEvidence('missing ordered hash-linked engine/host-action pair')
            mutable = {'timestamp', 'actual_action', 'visible_http_status', 'transport_result',
                'sequence', 'previous_event_hash', 'event_hash'}
            if kind == 'p4':
                if engine_event['late_intervention'] or 'late_intervention_mode' in engine_event or \
                    not event['late_intervention'] or event.get('late_intervention_mode') != 'safe':
                    raise InvalidEvidence('unexpected P4 Safe late-transition')
                mutable.update(('late_intervention', 'late_intervention_mode'))
            if (set(engine_event) - mutable != set(event) - mutable or
                any(engine_event[key] != event[key] for key in set(event) - mutable)):
                raise InvalidEvidence('engine/host-action pair changed intervention semantics')
        expected_name = 'MSCONN_EVENT_BODY_LIMIT' if kind == 'limit' else 'MSCONN_EVENT_REQUEST_BLOCKED' if kind in ('p1', 'p2') else 'MSCONN_EVENT_RESPONSE_BLOCKED'
        if event['event'] != expected_name or event['message_id'] != expected_name or \
            event['status'] != 'blocked' or event['action'] != ('redirect' if redirect else 'deny') or \
            event['http_status'] != (413 if kind == 'limit' else 302 if redirect else 403) or \
            any(event[key] for key in ('cancelled', 'client_disconnected', 'upstream_disconnected',
                'connection_aborted', 'body_truncated', 'truncated')):
            raise InvalidEvidence('contradictory Common intervention semantics')
        if event['event_hash'] == 0:
            raise InvalidEvidence('invalid host-action integrity hash')
        expected_phase = dict(p1='request_headers', p2='request_body', limit='request_body',
            p3='response_headers', p4='response_body')[kind]
        actual = 'log_only' if kind == 'p4' else 'redirect' if redirect else 'deny'
        if event['phase'] != expected_phase or event['requested_action'] != ('redirect' if redirect else 'deny') or \
            event['actual_action'] != actual or event['connection_aborted'] or \
            event['transport_result'] != ('log_only' if kind == 'p4' else 'http_status') or \
            (kind != 'p4' and (event['response_committed'] or event['body_started'])):
            raise InvalidEvidence('contradictory phase or host action')
        if kind == 'p4' and (not event['late_intervention'] or not event['response_committed'] or
            completion['late_action'] != 'log_only' or event['body_bytes_inspected'] < len(b'qualification-p4')):
            raise InvalidEvidence('P4 Safe commitment missing')
        if kind != 'p4' and event['late_intervention']:
            raise InvalidEvidence('unexpected late intervention')
        event_bytes = dict(p1=0, p2=16, limit=33, p3=0, p4=16)[kind]
        if event['body_bytes_seen'] != event_bytes or (kind != 'limit' and event['body_bytes_inspected'] != event_bytes):
            raise InvalidEvidence('Common body counters contradict probe')
        if event['response_started'] != (kind == 'p4') or event['headers_sent'] != (kind == 'p4') or event['body_started'] != (kind == 'p4'):
            raise InvalidEvidence('contradictory response commitment flags')
        if event['original_http_status'] != (200 if kind in ('p3', 'p4') else 0):
            raise InvalidEvidence('contradictory original response status')
        if kind == 'limit' and (event.get('body_limit_outcome') != 'reject' or event['rule_id'] or
            event['body_bytes_seen'] < 33 or event['body_bytes_inspected'] > 32):
            raise InvalidEvidence('body limit rejection missing')
    return dict(transaction_id=transaction_id, kind=selected_kind, status=status, upstream_headers=dispatched)


def write_new(path: Path, data: bytes):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'wb') as output:
        output.write(data)


def process_identity(pid):
    raw = Path(f'/proc/{pid}/stat').read_text()
    values = raw[raw.rfind(')') + 2:].split()
    return dict(pid=pid, state=values[0], ppid=int(values[1]), session=int(values[3]),
        start=values[19], exe=os.readlink(f'/proc/{pid}/exe'))


def descendants(owner):
    entries = {}
    for path in Path('/proc').iterdir():
        if path.name.isdecimal():
            try:
                entry = process_identity(int(path.name))
                entries[entry['pid']] = entry
            except (OSError, ValueError):
                pass
    found = {owner['pid']}
    while True:
        children = {pid for pid, entry in entries.items() if entry['ppid'] in found}
        if children <= found:
            break
        found.update(children)
    return [entries[pid] for pid in found if pid in entries]


class ProcessTree:
    """Retain identity of children before their parent exits or changes session."""
    def __init__(self, owner):
        self.owner, self.entries = owner, {}
        self.lock, self.done = threading.Lock(), threading.Event()
        self.sample()
        self.thread = threading.Thread(target=self.watch, daemon=True)
        self.thread.start()

    def sample(self):
        with self.lock:
            for entry in descendants(self.owner):
                self.entries[(entry['pid'], entry['start'])] = entry
            return list(self.entries.values())

    def watch(self):
        while not self.done.wait(.01):
            self.sample()

    def close(self):
        self.done.set()
        self.thread.join(timeout=1)
        if self.thread.is_alive():
            raise InvalidEvidence('process-tree observer survived cleanup')


def enable_subreaper():
    """Confine orphan adoption to this standalone qualification process."""
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.prctl(36, 1, 0, 0, 0) != 0:  # PR_SET_CHILD_SUBREAPER
        raise InvalidEvidence('runner cannot retain orphaned task descendants')


def cleanup_adopted():
    owner = process_identity(os.getpid())
    receipts = []
    deadline = time.monotonic() + 3
    while True:
        children = [entry for entry in descendants(owner) if entry['pid'] != owner['pid']]
        for entry in children:
            current = process_identity(entry['pid'])
            if (current['start'], current['exe']) != (entry['start'], entry['exe']):
                raise InvalidEvidence('adopted child identity changed')
            os.kill(entry['pid'], signal.SIGKILL)
            receipts.append(entry)
        while True:
            try:
                pid, _status = os.waitpid(-1, os.WNOHANG)
            except ChildProcessError:
                return receipts
            if pid == 0:
                break
        if time.monotonic() >= deadline:
            raise InvalidEvidence('adopted task child survived cleanup/reap')
        time.sleep(.01)


def stop_process(process):
    errors = []
    inventory = None
    try:
        inventory = stop_owned_process(process)
    except Exception as error:
        errors.append(str(error))
    try:
        process.qualification_tree.close()
    except Exception as error:
        errors.append(f'process-tree observer cleanup: {error}')
    if errors:
        raise InvalidEvidence('; '.join(errors))
    return inventory


def stop_owned_process(process):
    identity = process.qualification_identity
    tracker = process.qualification_tree
    inventory = tracker.sample()
    errors = []
    if process.poll() is not None:
        errors.append('task process exited before controlled stop')
    else:
        try:
            current = process_identity(identity['pid'])
            if stable_identity(current) != stable_identity(identity) or current['state'] == 'Z':
                raise InvalidEvidence('task process identity/liveness changed before controlled stop')
        except (OSError, ValueError, InvalidEvidence) as error:
            errors.append(str(error))
    for sig, timeout in ((signal.SIGTERM, 6), (signal.SIGKILL, 2)):
        if sig == signal.SIGKILL:
            errors.append('task process/descendant required SIGKILL fallback')
        for entry in reversed(inventory):
            try:
                current = process_identity(entry['pid'])
                if (current['start'], current['exe']) != (entry['start'], entry['exe']):
                    raise InvalidEvidence('PID identity changed during cleanup')
                os.kill(entry['pid'], sig)
            except ProcessLookupError:
                pass
            except FileNotFoundError:
                pass
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            process.poll()
            live = []
            for entry in tracker.sample():
                try:
                    current = process_identity(entry['pid'])
                    if current['start'] == entry['start'] and current['state'] != 'Z':
                        live.append(current)
                except (OSError, ValueError):
                    pass
            if not live:
                returncode = process.wait(timeout=1)
                if returncode not in (0, -signal.SIGTERM):
                    errors.append(f'unexpected controlled-stop exit: {returncode}')
                if errors:
                    raise InvalidEvidence('; '.join(errors))
                return inventory
            time.sleep(.05)
        inventory = tracker.sample()
    raise InvalidEvidence('task process/descendant survived cleanup')


def resources(pid):
    status_path = Path(f'/proc/{pid}/status')
    status = status_path.read_text()
    rss = re.search(r'^VmRSS:\s+(\d+) kB$', status, re.M)
    directory = Path(f'/proc/{pid}/fd')
    entries = list(directory.iterdir())
    links = []
    for path in entries:
        try:
            links.append(os.readlink(path))
        except OSError as error:
            if error.errno != errno.ENOENT:
                raise
            # Linux may close this individual FD after directory enumeration.
            # Keep its listed count; do not invent a socket classification.
    # An exited process or inaccessible proc directory is not an FD-close race.
    # Recheck both after links so ENOENT cannot hide loss of the whole process.
    directory.stat()
    status_path.read_text()
    return dict(rss_kib=int(rss.group(1)) if rss else 0, fds=len(entries),
        sockets=sum(link.startswith('socket:') for link in links))


def loaded_library(pid, pin):
    before = digest(Path(pin['path']), pin['sha256'])
    if (before['dev'], before['inode']) != (pin['dev'], pin['inode']):
        raise InvalidEvidence('pinned library identity changed before maps observation')
    matches = []
    for line in Path(f'/proc/{pid}/maps').read_text().splitlines():
        fields = line.split(maxsplit=5)
        if len(fields) == 6 and 'libmodsecurity' in fields[5]:
            major, minor = (int(part, 16) for part in fields[3].split(':'))
            mapped_device = os.makedev(major, minor)
            if fields[5] != pin['path'] or int(fields[4]) != pin['inode'] or \
                mapped_device != pin['dev'] and (mount_namespace_identity('self') != mount_namespace_identity(pid) or
                    mounted_device(pid, pin['path']) != mapped_device):
                raise InvalidEvidence('loaded libmodsecurity does not match pinned inode')
            matches.append(line)
    if not matches:
        raise InvalidEvidence('service has no pinned loaded libmodsecurity')
    after = digest(Path(pin['path']), pin['sha256'])
    if after != before:
        raise InvalidEvidence('pinned library identity changed during maps observation')
    return matches


def mount_namespace_identity(pid):
    namespace = os.stat(f'/proc/{pid}/ns/mnt')
    return namespace.st_dev, namespace.st_ino


def mounted_device(pid, path):
    selected = None
    for line in Path(f'/proc/{pid}/mountinfo').read_text().splitlines():
        fields = line.split()
        if len(fields) < 7 or '-' not in fields or not re.fullmatch(r'\d+:\d+', fields[2]):
            raise InvalidEvidence('invalid process mountinfo')
        mount = fields[4]
        for escaped, plain in ((r'\040', ' '), (r'\011', '\t'), (r'\012', '\n'), (r'\134', '\\')):
            mount = mount.replace(escaped, plain)
        if path == mount or path.startswith(mount.rstrip('/') + '/'):
            if selected is None or len(mount) > selected[0]:
                selected = (len(mount), os.makedev(*map(int, fields[2].split(':'))))
    if selected is None:
        raise InvalidEvidence('mapped library has no process mount binding')
    return selected[1]


def executable_identity(pid, path, sha256):
    pin = digest(path, sha256)
    observed = os.stat(f'/proc/{pid}/exe')
    if os.readlink(f'/proc/{pid}/exe') != pin['path'] or (observed.st_dev, observed.st_ino) != (pin['dev'], pin['inode']):
        raise InvalidEvidence('executing host/service is not pinned binary')
    return pin


def free_port():
    with socket.socket() as listener:
        listener.bind(('127.0.0.1', 0))
        return listener.getsockname()[1]


class Origin(http.server.ThreadingHTTPServer):
    daemon_threads = False
    block_on_close = True
    allow_reuse_address = False

    def __init__(self, port, context):
        super().__init__(('127.0.0.1', port), Handler)
        self.lock = threading.Lock()
        self.observations = {}
        self.header_arrivals = self.unattributed = 0
        self.framing_errors = []
        self.body_receipts = {}
        self.cancel_started = {}
        self.cancel_release = {}
        self.connections = set()
        self.barrier = threading.Barrier(4)
        self.parallel_seen = self.inflight = self.peak = self.barrier_passes = self.barrier_errors = 0
        self.tls_context = context

    def get_request(self):
        connection, address = super().get_request()
        connection.settimeout(3)
        try:
            return self.tls_context.wrap_socket(connection, server_side=True), address
        except Exception:
            connection.close()
            raise

    def close_owned(self):
        for release in self.cancel_release.values():
            release.set()
        self.shutdown()
        self.drain_backlog()
        # Join accepted handlers before closing sockets: early socket closure
        # could discard complete queued headers and manufacture zero dispatch.
        self.server_close()
        with self.lock:
            for connection in self.connections.copy():
                try:
                    connection.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass
                connection.close()

    def drain_backlog(self):
        deadline = time.monotonic() + 5
        while select.select([self.socket], [], [], 0)[0]:
            if time.monotonic() >= deadline:
                raise InvalidEvidence('origin accept backlog did not drain')
            self._handle_request_noblock()

    def verify_attribution(self):
        if self.unattributed or self.header_arrivals != sum(self.observations.values()):
            raise InvalidEvidence('unattributed backend header arrival')
        if self.framing_errors:
            raise InvalidEvidence('invalid or incomplete backend body framing')
        if any(len(self.body_receipts.get(identifier, [])) != count for identifier, count in self.observations.items()):
            raise InvalidEvidence('backend headers have no complete body/EOS receipt')


class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def log_message(self, *_args):
        pass

    def setup(self):
        self.request.settimeout(3)
        super().setup()
        with self.server.lock:
            self.server.connections.add(self.connection)

    def finish(self):
        try:
            super().finish()
        finally:
            with self.server.lock:
                self.server.connections.discard(self.connection)

    def do_POST(self):
        identifier = self.headers.get('X-Request-Id', '')
        if not re.fullmatch(r'q[0-9]+-[a-z0-9-]+', identifier):
            self.send_error(400)
            return
        parallel = self.path == '/qualification/parallel'
        if parallel:
            with self.server.lock:
                self.server.parallel_seen += 1
                self.server.inflight += 1
                self.server.peak = max(self.server.peak, self.server.inflight)
            try:
                self.server.barrier.wait(timeout=3)
                with self.server.lock:
                    self.server.barrier_passes += 1
            except threading.BrokenBarrierError:
                with self.server.lock:
                    self.server.barrier_errors += 1
                self.close_connection = True
                return
        try:
            receipt = self.read_body()
            with self.server.lock:
                self.server.body_receipts.setdefault(identifier, []).append(receipt)
            kind = self.path.rsplit('/', 1)[-1]
            body = b'z' * 32 if kind == 'cancel' else response_body(kind)
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Content-Length', str(len(body)))
            self.send_header('X-Qualification', kind if kind in ('p3', 'redirect') else 'allow')
            self.end_headers()
            if kind == 'cancel':
                with self.server.lock:
                    started = self.server.cancel_started.setdefault(identifier, threading.Event())
                    release = self.server.cancel_release.setdefault(identifier, threading.Event())
                self.wfile.write(body[:1])
                self.wfile.flush()
                started.set()
                if not release.wait(5):
                    raise InvalidEvidence('cancel client failed to close started response')
                self.close_connection = True
                return
            self.wfile.write(body)
        except (OSError, TimeoutError, InvalidEvidence) as error:
            with self.server.lock:
                self.server.framing_errors.append(dict(transaction_id=identifier, error=str(error)))
            self.close_connection = True
        finally:
            if parallel:
                with self.server.lock:
                    self.server.inflight -= 1

    def read_body(self):
        """Decode Envoy's HTTP/1 framing, bounded in payload, wire and time."""
        lengths = self.headers.get_all('Content-Length', [])
        encodings = self.headers.get_all('Transfer-Encoding', [])
        deadline = time.monotonic() + 3
        wire_bytes = chunks = body_bytes = 0
        payload_digest = hashlib.sha256()

        def read(size, line=False):
            nonlocal wire_bytes
            data = bytearray()
            while len(data) < size:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise InvalidEvidence('backend body deadline exceeded')
                self.connection.settimeout(remaining)
                # read1 performs at most one raw read. A slow sender cannot
                # restart an internal buffered-read timeout for each byte.
                chunk = self.rfile.read1(1 if line else size - len(data))
                if not chunk:
                    raise InvalidEvidence('truncated backend framing')
                data.extend(chunk)
                wire_bytes += len(chunk)
                if wire_bytes > 4096:
                    raise InvalidEvidence('excessive backend framing')
                if line and chunk == b'\n':
                    break
            return bytes(data)

        if encodings:
            if lengths or len(encodings) != 1 or encodings[0].lower() != 'chunked':
                raise InvalidEvidence('ambiguous or unsupported backend transfer encoding')
            while True:
                line = read(128, line=True)
                if not re.fullmatch(rb'[0-9a-fA-F]{1,8}\r\n', line):
                    raise InvalidEvidence('invalid bounded chunk size line')
                size = int(line[:-2], 16)
                if size == 0:
                    if read(2) != b'\r\n':
                        raise InvalidEvidence('backend trailers are not declared by profile')
                    break
                chunks += 1
                if chunks > 64 or body_bytes + size > 33:
                    raise InvalidEvidence('backend chunked body exceeds bound')
                payload_digest.update(read(size))
                body_bytes += size
                if read(2) != b'\r\n':
                    raise InvalidEvidence('invalid chunk data terminator')
            framing = 'chunked'
        else:
            if len(lengths) > 1 or lengths and not re.fullmatch(r'0|[1-9][0-9]*', lengths[0]):
                raise InvalidEvidence('invalid backend content length')
            body_bytes = int(lengths[0]) if lengths else 0
            if body_bytes > 33:
                raise InvalidEvidence('backend content length exceeds bound')
            payload_digest.update(read(body_bytes))
            chunks = int(body_bytes > 0)
            framing = 'content_length' if lengths else 'empty'
        return dict(framing=framing, bytes=body_bytes, chunks=chunks, wire_bytes=wire_bytes,
            eos=True, sha256=payload_digest.hexdigest())

    def parse_request(self):
        with self.server.lock:
            self.server.header_arrivals += 1
        valid = super().parse_request()
        if valid:
            identifiers = self.headers.get_all('X-Request-Id', [])
            with self.server.lock:
                if len(identifiers) != 1 or not re.fullmatch(r'q[0-9]+-[a-z0-9-]+', identifiers[0]) or self.command != 'POST':
                    self.server.unattributed += 1
                else:
                    identifier = identifiers[0]
                    self.server.observations[identifier] = self.server.observations.get(identifier, 0) + 1
        else:
            with self.server.lock:
                self.server.unattributed += 1
        return valid


def verify_parallel(origin):
    if (origin.parallel_seen, origin.peak, origin.barrier_passes, origin.barrier_errors,
        origin.inflight) != (4, 4, 4, 0, 0):
        raise InvalidEvidence('four actual simultaneous upstream handlers were not observed')
    return dict(requests=4, peak=4, barrier_passes=4, barrier_errors=0)


def read_malformed_response(wire):
    """Retain a bounded complete rejection, including actual socket closure."""
    data = bytearray()
    deadline = time.monotonic() + 3
    closed = False
    while len(data) <= 8192:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break
        wire.settimeout(remaining)
        try:
            chunk = wire.recv(min(4096, 8193 - len(data)))
        except (TimeoutError, socket.timeout):
            break
        except ssl.SSLEOFError:
            closed = True
            break
        if not chunk:
            closed = True
            break
        data.extend(chunk)
    receipt = dict(status=None, closed=closed, response_bytes=len(data), header_bytes=0,
        headers={}, body_bytes=0, valid_headers=False)
    boundary = data.find(b'\r\n\r\n')
    if boundary < 0 or boundary > 4096 or len(data) > 8192:
        return receipt
    header = bytes(data[:boundary])
    lines = header.split(b'\r\n')
    status = re.fullmatch(rb'HTTP/1\.[01] ([0-9]{3}) [\x20-\x7e]*', lines[0])
    if status is None:
        return receipt
    receipt.update(status=int(status[1]), header_bytes=boundary + 4, body_bytes=len(data) - boundary - 4)
    for line in lines[1:]:
        match = re.fullmatch(rb'([A-Za-z0-9-]+):[ \t]*([\x20-\x7e]*)', line)
        if match is None:
            return receipt
        name, value = match[1].decode().lower(), match[2].decode().strip()
        if name in receipt['headers']:
            return receipt
        receipt['headers'][name] = value
    receipt['valid_headers'] = True
    return receipt


def verify_malformed_rejection(receipt, identifier, completions, events, origin):
    zero_close = receipt['closed'] is True and receipt['status'] is None and receipt['valid_headers'] is False and \
        receipt['headers'] == {} and all(type(receipt[key]) is int and receipt[key] == 0 for key in
            ('response_bytes', 'header_bytes', 'body_bytes'))
    # An HTTP/1 codec may reject divergent Content-Length values by closing
    # before a local reply. Accept only exact zero-byte EOF; a partial reply,
    # timeout, reset exception or any engine/upstream activity still fails.
    http_close = all(type(receipt[key]) is int for key in ('response_bytes', 'header_bytes', 'body_bytes')) and \
        0 < receipt['header_bytes'] <= 4096 and 0 <= receipt['body_bytes'] and \
        receipt['response_bytes'] == receipt['header_bytes'] + receipt['body_bytes'] <= 8192
    if not zero_close and (not http_close or receipt['status'] != 400 or receipt['closed'] is not True or receipt['valid_headers'] is not True or \
        'transfer-encoding' in receipt['headers'] or receipt['headers'].get('connection', 'close').lower() != 'close'):
        raise InvalidEvidence('malformed framing lacks bounded HTTP400/close or exact zero-byte close rejection')
    length = receipt['headers'].get('content-length')
    if length is not None and (not re.fullmatch(r'0|[1-9][0-9]*', length) or int(length) != receipt['body_bytes']):
        raise InvalidEvidence('malformed rejection response framing mismatch')
    for record in completions:
        validate_completion(record)
        if record.get('transaction_id') == identifier:
            raise InvalidEvidence('malformed framing reached ext_proc evaluation')
    if any(record.get('transaction_id') == identifier for record in events):
        raise InvalidEvidence('malformed framing reached Common evaluation')
    with origin.lock:
        if origin.observations.get(identifier) or origin.body_receipts.get(identifier) or origin.unattributed:
            raise InvalidEvidence('malformed framing reached upstream')


def run_malformed_recovery(result, malformed, recovery, identity, identity_reader):
    oracle_passed = recovery_passed = False
    try:
        malformed()
        oracle_passed = True
    except Exception as error:
        result['errors'].append(f'malformed framing: {error}')
        result['passed'] = False
    try:
        result['probes'].append(recovery())
        recovery_passed = True
    except Exception as error:
        result['errors'].append(f'framing recovery: {error}')
        result['passed'] = False
    try:
        current = identity_reader()
        if any(current[key] != identity[key] for key in ('pid', 'start', 'exe')):
            raise InvalidEvidence('recovery replaced service process')
    except Exception as error:
        recovery_passed = False
        result['errors'].append(f'framing recovery identity: {error}')
        result['passed'] = False
    result['recovery_passed'] = recovery_passed
    result['gates']['G5'] = 'framing_recovery_passed_other_failures_not_proven' if oracle_passed and recovery_passed else 'failed'


def fail_cleanup(result, error):
    result['passed'] = False
    result['cleanup_passed'] = False
    result.setdefault('errors', []).append(str(error))
    # The final observer inventory is a prerequisite of every claimed runtime
    # gate. Retain not-run entries, but never retain a prior positive verdict
    # after late reconciliation or process/observer cleanup invalidates it.
    for gate, verdict in result['gates'].items():
        if verdict != 'not_run':
            result['gates'][gate] = 'failed'
    result['gates']['G3'] = result['gates']['G9'] = 'failed'


def reconcile_origin(result, origin, attempted):
    """Invalidate runtime evidence independently of observer teardown."""
    result['upstream_headers'] = origin.observations
    result['upstream_header_arrivals'] = origin.header_arrivals
    result['upstream_unattributed'] = origin.unattributed
    result['upstream_body_receipts'] = origin.body_receipts
    result['upstream_framing_errors'] = origin.framing_errors
    try:
        origin.verify_attribution()
        if set(origin.observations) - set(attempted):
            raise InvalidEvidence('unknown attributed backend transaction')
        for identifier, kind in attempted.items():
            verify_origin_probe(origin, identifier, kind)
        for probe in result['probes']:
            final_count = origin.observations.get(probe['transaction_id'], 0)
            if final_count != probe['upstream_headers']:
                raise InvalidEvidence('backend observation changed after probe completion')
    except Exception as error:
        fail_evidence(result, error)


def fail_evidence(result, error):
    result['passed'] = False
    result.setdefault('errors', []).append(str(error))
    for gate in ('G2', 'G3', 'G4', 'G5', 'G6'):
        if gate == 'G3' or result['gates'][gate] != 'not_run':
            result['gates'][gate] = 'failed'


def probe_evidence(identifier, completions, events):
    """Retain immutable attributed records, including order and all fields."""
    return json.loads(json.dumps(dict(
        completions=[record for record in completions if record.get('transaction_id') == identifier],
        events=[record for record in events if record.get('transaction_id') == identifier]), sort_keys=True))


def reconcile_records(result, origin, attempted, completions, events):
    """Verify every attempted transaction against the final reaped inventory."""
    for record in completions:
        validate_completion(record)
    for record in events:
        validate_common(record)
    if {record['transaction_id'] for record in completions + events if 'transaction_id' in record} - set(attempted):
        raise InvalidEvidence('unknown attributed final transaction')
    probes = {probe['transaction_id']: probe for probe in result['probes']}
    if len(probes) != len(result['probes']) or set(probes) - set(attempted):
        raise InvalidEvidence('duplicate or unknown probe receipt')
    for identifier, kind in attempted.items():
        if kind == 'malformed':
            verify_malformed_rejection(result['malformed_rejection'], identifier, completions, events, origin)
            continue
        if identifier not in probes:
            raise InvalidEvidence('attempted probe has no successful receipt')
        probe = probes[identifier]
        dispatch = origin.observations.get(identifier, 0)
        if kind == 'unavailable':
            verify_unavailable(identifier, probe['status'], dispatch, completions, events)
        elif kind == 'cancel':
            verify_cancel(identifier, completions, events, dispatch, probe['client_partial_bytes'])
        else:
            verify_probe(identifier, probe['status'], dispatch, completions, events, kind)
        if probe.get('evidence') != probe_evidence(identifier, completions, events):
            raise InvalidEvidence('attributed records changed after probe completion')


def verify_final_logs(paths):
    for path in paths:
        data = read_safe(path)
        if re.search(rb'\b(?:panic|fatal|segfault|segmentation fault)\b', data, re.IGNORECASE):
            raise InvalidEvidence(f'host/service crash marker in final log: {path.name}')


def run_start(args, directory, index, library_pin):
    directory.mkdir(mode=0o700)
    result = dict(start=index, profile=QUALIFICATION_PROFILE, passed=False, catalog_acceptance=False, cleanup_passed=False,
        gates={f'G{i}': 'not_run' for i in range(1, 10)}, probes=[], errors=[])
    result['runner_sha256'] = args.runner_sha256
    processes, outputs, log_paths = [], [], []
    attempted = {}
    origin = thread = None
    try:
        cert, key = directory / 'tls.crt', directory / 'tls.key'
        subprocess.run(['openssl', 'req', '-x509', '-newkey', 'rsa:2048', '-nodes', '-days', '1',
            '-subj', '/CN=localhost', '-addext', 'subjectAltName=IP:127.0.0.1',
            '-keyout', str(key), '-out', str(cert)], check=True, stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL, timeout=15)
        key.chmod(0o600)
        cert.chmod(0o600)
        downstream, upstream, service_port, admin = [free_port() for _ in range(4)]
        if len({downstream, upstream, service_port, admin}) != 4:
            raise InvalidEvidence('port collision')
        tls = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        tls.minimum_version = ssl.TLSVersion.TLSv1_2
        tls.load_cert_chain(cert, key)
        origin = Origin(upstream, tls)
        thread = threading.Thread(target=origin.serve_forever, kwargs={'poll_interval': .05})
        thread.start()
        config = json.loads(read_safe(REPO / 'connectors/envoy/config/envoy-ext-proc-service.json'), object_pairs_hook=pairs)
        config.update(listen_address=f'127.0.0.1:{service_port}', max_request_body_bytes=32,
            max_response_body_bytes=32, stream_idle_timeout_ms=2000)
        write_new(directory / 'service.json', json.dumps(config).encode())
        write_new(directory / 'rules.conf', read_safe(args.rules_file))
        runtime = '\n'.join(('enabled=on', f'rules_file={directory / "rules.conf"}',
            'transaction_id_header=x-request-id', 'request_body_mode=streaming',
            'response_body_mode=streaming', 'request_body_limit=32', 'response_body_limit=32',
            'body_limit_action=reject', 'phase4_mode=safe', 'default_block_status=403',
            'default_error_status=500', 'use_error_log=off', f'event_path={directory / "common.jsonl"}', ''))
        write_new(directory / 'runtime.conf', runtime.encode())
        template = read_safe(REPO / 'connectors/envoy/config/envoy-ext-proc-streaming.yaml.in').decode()
        if template.count('request_body_mode: STREAMED') != 1 or template.count('  - name: msconnector_ext_proc_listener\n') != 1:
            raise InvalidEvidence('buffered admission template contract changed')
        template = template.replace('request_body_mode: STREAMED', 'request_body_mode: BUFFERED').replace(
            '  - name: msconnector_ext_proc_listener\n',
            '  - name: msconnector_ext_proc_listener\n    per_connection_buffer_limit_bytes: 65536\n')
        for name, value in dict(ENVOY_RELEASE='qualification', LISTEN_PORT=downstream, UPSTREAM_PORT=upstream,
            EXT_PROC_PORT=service_port, ADMIN_PORT=admin, TLS_CERTIFICATE=cert, TLS_PRIVATE_KEY=key).items():
            template = template.replace(f'@{name}@', str(value))
        if re.search(r'@[A-Z_]+@', template):
            raise InvalidEvidence('unexpanded Envoy template token')
        write_new(directory / 'envoy.yaml', template.encode())
        service_command = [str(args.service_bin), '--config', str(directory / 'service.json'),
            '--runtime-config', str(directory / 'runtime.conf'), '--event-log', str(directory / 'completion.jsonl')]
        subprocess.run([*service_command, '--check-config'], check=True, timeout=10, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run([str(args.envoy_bin), '--mode', 'validate', '-c', str(directory / 'envoy.yaml')],
            check=True, timeout=10, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for label, command in [('service', service_command), ('envoy', [str(args.envoy_bin), '-c',
            str(directory / 'envoy.yaml'), '--concurrency', '2', '--log-level', 'error'])]:
            log_path = directory / f'{label}.log'
            log = os.fdopen(os.open(log_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600), 'wb')
            log_paths.append(log_path)
            outputs.append(log)
            processes.append(subprocess.Popen(command, stdout=log, stderr=log, start_new_session=True))
            processes[-1].qualification_identity = process_identity(processes[-1].pid)
            processes[-1].qualification_tree = ProcessTree(processes[-1].qualification_identity)
        deadline = time.monotonic() + 10
        while True:
            if any(p.poll() is not None for p in processes):
                raise InvalidEvidence('host/service exited before readiness')
            try:
                with socket.create_connection(('127.0.0.1', downstream), .1):
                    break
            except OSError:
                if time.monotonic() >= deadline:
                    raise InvalidEvidence('readiness timeout')
                time.sleep(.05)
        service = processes[0]
        result['executables'] = [executable_identity(processes[0].pid, args.service_bin, args.service_sha256),
            executable_identity(processes[1].pid, args.envoy_bin, args.envoy_sha256)]
        result['loaded_library_before'] = loaded_library(service.pid, library_pin)
        result['processes'] = [process_identity(p.pid) for p in processes]
        result['resources_before'] = [resources(p.pid) for p in processes]
        client_tls = ssl.create_default_context(cafile=str(cert))
        client_tls.minimum_version = ssl.TLSVersion.TLSv1_2
        result['gates']['G1'] = 'pins_verified_build_provenance_not_proven'

        def connection():
            return http.client.HTTPSConnection('127.0.0.1', downstream, context=client_tls, timeout=6)

        def request(identifier, kind, client=None, route=None, retain=False):
            attempted[identifier] = kind
            client = client or connection()
            client.connect() if client.sock is None else None
            socket_identity = (client.sock.fileno(), client.sock.getsockname())
            body = probe_body(kind)
            target = route or f'/qualification/{kind}'
            wire_receipt = None
            if kind.startswith('chunked-'):
                wire_receipt = send_chunked_request(client, identifier, kind, target)
            else:
                client.request('POST', target, body, {'X-Request-Id': identifier})
            response = client.getresponse()
            status = response.status
            receipt = client_receipt(response, kind)
            completion, events = await_records(directory, identifier)
            with origin.lock:
                dispatch = origin.observations.get(identifier, 0)
            observed = verify_probe(identifier, status, dispatch, completion, events, kind)
            observed['evidence'] = probe_evidence(identifier, completion, events)
            observed['client_body'] = receipt
            if wire_receipt:
                observed['downstream_request'] = wire_receipt
            verify_origin_probe(origin, identifier, kind)
            if retain and (client.sock is None or (client.sock.fileno(), client.sock.getsockname()) != socket_identity):
                raise InvalidEvidence('host closed/replaced keepalive socket')
            return observed

        # Continue after individual failures to retain strongest available gate evidence.
        initial_identities = [stable_identity(process_identity(p.pid)) for p in processes]
        for kind in ('allow', 'p1', 'p2', 'empty', 'limit', 'p3', 'p4', *BOUNDARY_KINDS):
            client = connection()
            try:
                result['probes'].append(request(f'q{index}-{kind}', kind, client))
                if kind in ('chunked-limit', 'redirect'):
                    followup = connection()
                    try:
                        result['probes'].append(request(f'q{index}-{kind}-recovery', 'allow', followup))
                        if [stable_identity(process_identity(p.pid)) for p in processes] != initial_identities:
                            raise InvalidEvidence('boundary recovery replaced Envoy/service')
                    finally:
                        followup.close()
            except Exception as error:
                result['errors'].append(f'{kind}: {error}')
            finally:
                client.close()
        kinds = {probe['kind'] for probe in result['probes']}
        result['gates']['G2'] = 'passed' if {'allow', 'p1', 'p2'} <= kinds else 'failed'
        result['gates']['G3'] = 'passed' if {'p1', 'p2'} <= kinds else 'failed'
        result['gates']['G4'] = 'bounded_body_delta_passed_other_boundaries_incomplete' if \
            {'empty', 'limit', 'p3', 'p4', *BOUNDARY_KINDS} <= kinds else 'failed'

        # Abort a real downstream connection after the first streamed byte;
        # hold the origin open until cancellation is recorded, then recover.
        cancel_id = f'q{index}-cancel'
        attempted[cancel_id] = 'cancel'
        cancel_client = connection()
        try:
            cancel_client.request('POST', '/qualification/cancel', b'ok', {'X-Request-Id': cancel_id})
            cancel_response = cancel_client.getresponse()
            if cancel_response.status != 200 or cancel_response.read(1) != b'z':
                raise InvalidEvidence('cancel response never actually started')
            with origin.lock:
                started = origin.cancel_started.get(cancel_id)
            if started is None or not started.is_set() or cancel_client.sock is None:
                raise InvalidEvidence('missing origin/client streaming start')
            cancel_client.sock.shutdown(socket.SHUT_RDWR)
            cancel_client.close()
            complete, events = await_records(directory, cancel_id)
            with origin.lock:
                dispatch = origin.observations.get(cancel_id, 0)
            verify_cancel(cancel_id, complete, events, dispatch, 1)
            result['probes'].append(dict(transaction_id=cancel_id, kind='cancel', status=200,
                upstream_headers=dispatch, client_partial_bytes=1, client_connection_closed=True,
                evidence=probe_evidence(cancel_id, complete, events)))
            followup = connection()
            try:
                result['probes'].append(request(f'q{index}-cancel-recovery', 'allow', followup))
                if [stable_identity(process_identity(p.pid)) for p in processes] != initial_identities:
                    raise InvalidEvidence('cancel recovery replaced Envoy/service')
                result['cancel_same_process_recovery'] = True
            finally:
                followup.close()
        finally:
            cancel_client.close()
            with origin.lock:
                release = origin.cancel_release.get(cancel_id)
            if release:
                release.set()
        # Relevant malformed request: same surviving service must allow next request.
        malformed_id = f'q{index}-invalid'
        result['malformed_transaction_id'] = malformed_id
        def malformed():
            attempted[malformed_id] = 'malformed'
            with socket.create_connection(('127.0.0.1', downstream), 3) as raw:
                with client_tls.wrap_socket(raw, server_hostname='127.0.0.1') as wire:
                    # Divergent duplicate lengths are unambiguously invalid
                    # framing; no body or engine transaction may start.
                    wire.sendall((f'POST /qualification/invalid HTTP/1.1\r\nHost: localhost\r\nX-Request-Id: {malformed_id}\r\n'
                        'Content-Length: 1\r\nContent-Length: 2\r\n\r\n').encode())
                    result['malformed_rejection'] = read_malformed_response(wire)
            verify_malformed_rejection(result['malformed_rejection'], malformed_id,
                jsonl(directory / 'completion.jsonl'), jsonl(directory / 'common.jsonl'), origin)

        def recovery():
            followup = connection()
            try:
                return request(f'q{index}-recovery', 'allow', followup)
            finally:
                followup.close()

        run_malformed_recovery(result, malformed, recovery, result['processes'][0], lambda: process_identity(service.pid))
        keepalive = connection()
        try:
            for count, kind in enumerate(('allow', 'p1', 'allow', 'p2', 'allow')):
                result['probes'].append(request(f'q{index}-keep-{count}', kind, keepalive, retain=True))
        finally:
            keepalive.close()
        def parallel(count):
            client = connection()
            try:
                return request(f'q{index}-parallel-{count}', 'allow', client, '/qualification/parallel')
            finally:
                client.close()
        with ThreadPoolExecutor(max_workers=4) as executor:
            result['probes'].extend(executor.map(parallel, range(4)))
        result['parallel'] = verify_parallel(origin)
        result['resources_after'] = [resources(p.pid) for p in processes]
        result['gates']['G6'] = 'passed'
        result['gates']['G7'] = 'versioned_fail_closed_configuration_only'
        result['gates']['G8'] = 'not_run_external_regression_required'
        result['loaded_library_after'] = loaded_library(service.pid, library_pin)
        executable_identity(processes[0].pid, args.service_bin, args.service_sha256)
        executable_identity(processes[1].pid, args.envoy_bin, args.envoy_sha256)

        # Controlled processor-unreachable case uses the current template's
        # exact HTTP500. Restart only the pinned processor, retaining Envoy.
        envoy_identity = stable_identity(process_identity(processes[1].pid))
        old_service = stable_identity(process_identity(service.pid))
        stop_process(service)
        with socket.socket() as stopped_listener:
            stopped_listener.settimeout(.2)
            if stopped_listener.connect_ex(('127.0.0.1', service_port)) == 0:
                raise InvalidEvidence('stopped processor listener remained reachable')
        unavailable_id = f'q{index}-unavailable'
        attempted[unavailable_id] = 'unavailable'
        unavailable_client = connection()
        try:
            unavailable_client.request('POST', '/qualification/unavailable', b'ok', {'X-Request-Id': unavailable_id})
            response = unavailable_client.getresponse()
            receipt = client_receipt(response, 'unavailable')
            complete = jsonl(directory / 'completion.jsonl')
            events = jsonl(directory / 'common.jsonl') if (directory / 'common.jsonl').exists() else []
            with origin.lock:
                dispatch = origin.observations.get(unavailable_id, 0)
            verify_unavailable(unavailable_id, response.status, dispatch, complete, events)
            result['probes'].append(dict(transaction_id=unavailable_id, kind='unavailable', status=response.status,
                upstream_headers=dispatch, engine_event_count=0, client_body=receipt,
                evidence=probe_evidence(unavailable_id, complete, events),
                failure_semantics='versioned_ext_proc_unreachable_processor_http500'))
        finally:
            unavailable_client.close()
        digest(args.service_bin, args.service_sha256)
        service = subprocess.Popen(service_command, stdout=outputs[0], stderr=outputs[0], start_new_session=True)
        processes[0] = service
        service.qualification_identity = process_identity(service.pid)
        service.qualification_tree = ProcessTree(service.qualification_identity)
        deadline = time.monotonic() + 10
        while True:
            if service.poll() is not None:
                raise InvalidEvidence('restarted pinned service exited')
            try:
                with socket.create_connection(('127.0.0.1', service_port), .1):
                    break
            except OSError:
                if time.monotonic() >= deadline:
                    raise InvalidEvidence('restarted service readiness timeout')
                time.sleep(.05)
        executable_identity(service.pid, args.service_bin, args.service_sha256)
        result['loaded_library_restarted'] = loaded_library(service.pid, library_pin)
        followup = connection()
        try:
            result['probes'].append(request(f'q{index}-restart-recovery', 'allow', followup))
        finally:
            followup.close()
        restarted = stable_identity(process_identity(service.pid))
        if restarted == old_service or stable_identity(process_identity(processes[1].pid)) != envoy_identity:
            raise InvalidEvidence('restart did not replace service or changed Envoy')
        result['service_restart'] = dict(before=old_service, after=restarted, envoy=envoy_identity,
            pinned_executable=True, unavailable_status=500, same_envoy_allow=True)
        result['gates']['G5'] = 'bounded_cancel_restart_recovery_passed_other_failures_not_proven' if \
            result['gates']['G5'] != 'failed' else 'failed'
        result['passed'] = not result['errors']
    except Exception as error:
        result['errors'].append(str(error))
    finally:
        cleanup_errors = []
        for process in reversed(processes):
            try:
                stop_process(process)
            except Exception as error:
                cleanup_errors.append(error)
        if getattr(args, 'subreaper', False):
            try:
                result['adopted_cleanup'] = cleanup_adopted()
                if result['adopted_cleanup']:
                    raise InvalidEvidence('adopted task descendants required SIGKILL cleanup')
            except Exception as error:
                cleanup_errors.append(error)
        if origin:
            try:
                origin.close_owned()
                thread.join(timeout=3)
                if thread.is_alive() or origin.connections:
                    raise InvalidEvidence('origin handlers/serve thread survived cleanup')
                # Reconcile after both real host processes have stopped and all
                # accepted handlers joined. Missing EOS or late dispatch fails
                # attribution, while fully completed teardown still passes G9.
                reconcile_origin(result, origin, attempted)
                try:
                    complete = jsonl(directory / 'completion.jsonl') if attempted else []
                    events = jsonl(directory / 'common.jsonl') if attempted and (directory / 'common.jsonl').exists() else []
                    reconcile_records(result, origin, attempted, complete, events)
                except Exception as error:
                    fail_evidence(result, error)
            except Exception as error:
                cleanup_errors.append(error)
        for output in outputs:
            try:
                output.close()
            except Exception as error:
                cleanup_errors.append(error)
        try:
            verify_final_logs(log_paths)
        except Exception as error:
            cleanup_errors.append(error)
        for secret in (directory / 'tls.key', directory / 'tls.crt'):
            try:
                secret.unlink(missing_ok=True)
            except OSError as error:
                cleanup_errors.append(error)
        if cleanup_errors:
            for error in cleanup_errors:
                fail_cleanup(result, error)
        else:
            result['cleanup_passed'] = True
            result['gates']['G9'] = 'cleanup_passed_catalog_gaps_recorded'
        write_new(directory / 'qualification.json', json.dumps(result, sort_keys=True, indent=2).encode())
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-digest', action='store_true', help='print current scoped source SHA256 and exit')
    parser.add_argument('--runner-digest', action='store_true', help='print actual runner SHA256 independently of the Git index')
    for name in ('envoy-bin', 'service-bin', 'library', 'rules-file', 'root'):
        parser.add_argument('--' + name, type=Path)
    for name in ('source-sha256', 'runner-sha256', 'envoy-sha256', 'service-sha256', 'library-sha256', 'rules-sha256'):
        parser.add_argument('--' + name)
    args = parser.parse_args(argv)
    if args.source_digest:
        print(source_digest())
        return 0
    if args.runner_digest:
        print(runner_identity()['sha256'])
        return 0
    try:
        if any(getattr(args, name) is None for name in ('envoy_bin', 'service_bin', 'library',
            'rules_file', 'root', 'source_sha256', 'envoy_sha256', 'service_sha256',
            'library_sha256', 'rules_sha256', 'runner_sha256')):
            raise InvalidEvidence('all paths and SHA256 pins required')
        checked_path(args.root)
        if not args.root.is_relative_to(EXTERNAL) or args.root == EXTERNAL:
            raise InvalidEvidence('run root must be below external task storage')
        info = args.root.stat()
        if info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) != 0o700 or any(args.root.iterdir()):
            raise InvalidEvidence('run root must be owned, private and empty')
        if source_digest() != args.source_sha256:
            raise InvalidEvidence('source SHA256 mismatch')
        runner_pin = runner_identity(args.runner_sha256)
        pins = dict(envoy=digest(args.envoy_bin, args.envoy_sha256),
            service=digest(args.service_bin, args.service_sha256),
            library=digest(args.library, args.library_sha256), rules=digest(args.rules_file, args.rules_sha256))
        if read_safe(args.rules_file).decode() != RULES:
            raise InvalidEvidence('qualification requires exact declared no-Include fixed rules fixture')
        if not os.access(args.envoy_bin, os.X_OK) or not os.access(args.service_bin, os.X_OK):
            raise InvalidEvidence('host/service binaries not executable')
        write_new(args.root / 'run-contract.json', json.dumps(dict(source_sha256=args.source_sha256,
            runner_sha256=runner_pin['sha256'], runner_pin=runner_pin), sort_keys=True, indent=2).encode())
        enable_subreaper()
        args.subreaper = True
        starts = pinned_starts(args, pins['library'], runner_pin)
        for label, path in [('envoy', args.envoy_bin), ('service', args.service_bin),
            ('library', args.library), ('rules', args.rules_file)]:
            digest(path, pins[label]['sha256'])
        if source_digest() != args.source_sha256:
            raise InvalidEvidence('source changed during campaign')
        verify_runner(runner_pin)
        identities = [record.get('processes', []) for record in starts]
        distinct = len({(record[0]['pid'], record[0]['start']) for record in identities if record}) == 3
        passed = all(record['passed'] and record['cleanup_passed'] for record in starts) and distinct
        summary = dict(passed=passed, catalog_acceptance=False, profile=QUALIFICATION_PROFILE,
            source_sha256=args.source_sha256, runner_sha256=runner_pin['sha256'], runner_pin=runner_pin,
            runner_pin_verified=True, pins=pins, starts=starts, distinct_service_starts=distinct,
            gaps=['fresh reproducible build provenance', 'complete boundary matrix', 'timeout/abort/failmode matrix',
                'external regression', 'canonical G1-G9 acceptance'], controlled_stop_start=distinct and all(
                    record['cleanup_passed'] for record in starts))
        write_new(args.root / 'qualification.json', json.dumps(summary, sort_keys=True, indent=2).encode())
        print(json.dumps(dict(passed=passed, catalog_acceptance=False, runner_sha256=runner_pin['sha256'], root=str(args.root))))
        return 0 if passed else 1
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(json.dumps(dict(passed=False, catalog_acceptance=False, error=str(error))))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
