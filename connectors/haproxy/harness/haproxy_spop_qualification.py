#!/usr/bin/env python3
"""Pinned real-host SPOP + native MRC1 qualification prerequisites.

This is the SPOE request/response-companion profile, not direct HTX. Successful
probes remain BLOCKED for catalog promotion until the remaining qualification
gates have evidence. Native P3/P4 receipts are checked against host-owned IDs;
fresh-build and complete regression evidence remain external.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import math
import os
from pathlib import Path
import re
import signal
import socket
import stat
import sys
import threading
import time

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / 'connectors/composite_harness'))
from qualification import (Child, Monitor, MAX_FD, MAX_RSS, bound_input, loaded_library,
                           owned_sockets, private_read, read_events,
                           read_response, trusted_path, validate_runtime_root,
                           wait_port, write_json)

LIMIT = 32768
MAX_FILE = 16 * 1024 * 1024
RULES = '''SecRuleEngine On
SecRequestBodyAccess On
SecResponseBodyAccess On
SecResponseBodyMimeType text/plain
SecRule REQUEST_HEADERS:X-Qualification-P1 "@streq deny" "id:1100100,phase:1,deny,status:403,nolog,t:none"
SecRule REQUEST_BODY "@contains qualification-p2-deny" "id:1100101,phase:2,deny,status:403,nolog,t:none"
SecRule RESPONSE_HEADERS:X-Qualification-P3 "@streq deny" "id:1100201,phase:3,deny,status:403,nolog,t:none"
SecRule RESPONSE_BODY "@contains qualification-p4-deny" "id:1100301,phase:4,deny,status:403,nolog,t:none"
'''
RULES_SHA256 = hashlib.sha256(RULES.encode()).hexdigest()
RECORD_FIELDS = frozenset(('timestamp connector mode runtime_mode variant case '
    'request_id transaction_id phase live_executed modsecurity_processed '
    'request_headers_seen request_body_seen response_headers_seen response_body_seen '
    'expected_status observed_status result decision disruptive intervention_status '
    'http_status redirect_present rule_id anomaly_score audit_log_path haproxy_log_path '
    'spoa_log_path reason_code reason').split())
MALFORMED_CASES = frozenset(('invalid-cl', 'invalid-te', 'truncated-request'))
PARSER_REJECT_CASES = MALFORMED_CASES - {'truncated-request'}
BOUNDARY_CASES = ('request-empty', 'request-exact', 'request-over',
    'chunked-allow', 'chunked-p2', 'invalid-cl', 'invalid-te', 'truncated-request',
    'response-empty', 'response-exact', 'limit', 'slow')


def case_contract(case):
    if case not in {'allow', 'p1', 'p2', 'p3', 'p4', 'parallel',
                    'agent-unavailable'} | set(BOUNDARY_CASES):
        raise ValueError('unknown closed SPOP qualification case')
    body = b'qualification-p2-deny' if case in {'p2', 'chunked-p2'} else b'ok=1'
    if case == 'request-empty':
        body = b''
    if case in {'request-exact', 'request-over'}:
        body = b'R' * (LIMIT + int(case == 'request-over'))
    route = case if case in {'p3', 'p4', 'parallel', 'limit', 'slow', 'response-empty', 'response-exact'} else 'allow'
    response = {'p4': b'qualification-p4-deny', 'response-empty': b'',
        'response-exact': b'L' * LIMIT, 'limit': b'L' * (LIMIT + 1)}.get(case, b'OK')
    status = 400 if case in MALFORMED_CASES else 503 if case == 'agent-unavailable' else 413 if case == 'request-over' else 403 if case in {'p1', 'p2', 'chunked-p2', 'p3'} else 200
    backend = int(case not in {'p1', 'p2', 'chunked-p2', 'request-over', 'agent-unavailable'} | MALFORMED_CASES)
    return {'body': body, 'body_sha256': hashlib.sha256(body).hexdigest(),
        'route': route, 'response': response, 'response_sha256': hashlib.sha256(response).hexdigest(),
        'status': status, 'backend': backend,
        'decision': case not in PARSER_REJECT_CASES and case != 'agent-unavailable'}


def safe_path(value: str) -> Path:
    if not re.fullmatch(r'/[A-Za-z0-9_./-]+', value):
        raise ValueError('configuration path outside ASCII allowlist')
    path = Path(value)
    if str(path) != os.path.normpath(value):
        raise ValueError('noncanonical path')
    return path


def pinned(value: str, expected: str, maximum=MAX_FILE) -> Path:
    path = safe_path(value)
    data = bound_input(path, maximum)
    if not re.fullmatch('[0-9a-f]{64}', expected) or hashlib.sha256(data).hexdigest() != expected:
        raise ValueError('operator SHA256 pin mismatch')
    return path


class BoundRules:
    """Keep one trusted descriptor and reject path, metadata or content drift."""
    def __init__(self, path, expected):
        self.path = safe_path(str(path))
        self.expected = expected
        self.fd = None
        trusted_path(self.path)
        self.fd = os.open(self.path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        try:
            metadata = os.fstat(self.fd)
            if not stat.S_ISREG(metadata.st_mode) or metadata.st_uid != os.getuid() or \
                metadata.st_nlink != 1 or metadata.st_mode & 0o022 or metadata.st_size > 65536:
                raise ValueError('rules must be trusted bounded single-link regular file')
            self.identity = self.fingerprint(metadata)
            self.verify()
        except BaseException:
            self.close()
            raise

    @staticmethod
    def fingerprint(metadata):
        return (metadata.st_dev, metadata.st_ino, metadata.st_mode, metadata.st_uid,
                metadata.st_nlink, metadata.st_size, metadata.st_mtime_ns, metadata.st_ctime_ns)

    def verify(self):
        trusted_path(self.path)
        if self.fingerprint(self.path.lstat()) != self.identity or \
            self.fingerprint(os.fstat(self.fd)) != self.identity:
            raise ValueError('rules path or descriptor identity changed')
        data = os.pread(self.fd, 65537, 0)
        if not re.fullmatch('[0-9a-f]{64}', self.expected) or \
            hashlib.sha256(data).hexdigest() != self.expected:
            raise ValueError('rules SHA256 changed')
        if self.fingerprint(os.fstat(self.fd)) != self.identity or \
            self.fingerprint(self.path.lstat()) != self.identity:
            raise ValueError('rules changed while reading descriptor')
        return data

    def copy(self, path):
        data = self.verify()
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        try:
            with os.fdopen(fd, 'wb', closefd=False) as output:
                output.write(data)
                output.flush()
            os.fchmod(fd, 0o400)
        finally:
            os.close(fd)
        self.verify()
        return BoundRules(path, self.expected)

    def close(self):
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()


def verify_rules(source, private):
    source.verify()
    private.verify()


def process_pin(child, path, expected):
    identity = child.identity()
    current = os.stat(f'/proc/{identity["pid"]}/exe')
    bound = path.stat()
    if (current.st_dev, current.st_ino) != (bound.st_dev, bound.st_ino):
        raise ValueError('loaded executable inode/device differs from pinned input')
    if hashlib.sha256(bound_input(path, 128 * 1024 * 1024)).hexdigest() != expected or identity['exe_sha256'] != expected:
        raise ValueError('loaded executable differs from operator pin')
    return identity


def library_pin(child, args):
    values = loaded_library(child, args.library_sha256)
    if values[0]['path'] != str(args.library):
        raise ValueError('loaded library differs from explicitly pinned path')
    return values


def private_write(path: Path, content: str):
    with path.open('x', encoding='utf-8') as output:
        os.chmod(path, 0o600)
        output.write(content)


def verify_request(records, token, case, start_time, end_time, expected_backend):
    """Reject false phase/rule/engine correlation and unexpected payload fields."""
    if not re.fullmatch(r'haproxy-htx-[1-9][0-9]*', token):
        raise ValueError('engine identity must be generated by the host')
    if any(type(record) is not dict or set(record) != RECORD_FIELDS for record in records):
        raise ValueError('unexpected SPOP event schema or payload field')
    matches = [record for record in records if record['request_id'] == token]
    if len(matches) != 1:
        raise ValueError('missing or duplicate correlated request decision')
    value = matches[0]
    phase, rule, blocked = {'p1': (1, 1100100, True), 'p2': (2, 1100101, True),
        'chunked-p2': (2, 1100101, True), 'request-over': (2, 0, True)}.get(case, (2, 0, False))
    oversized = case == 'request-over'
    deny_status = 413 if oversized else 403
    exact = {'connector': 'haproxy', 'mode': 'block', 'runtime_mode': 'production',
             'variant': 'spop-qualification', 'case': 'qualification',
             'transaction_id': token, 'phase': phase, 'rule_id': rule,
             'disruptive': blocked, 'live_executed': True,
             'modsecurity_processed': not oversized, 'request_headers_seen': True,
             'request_body_seen': True, 'response_headers_seen': False,
             'response_body_seen': False, 'redirect_present': False,
             'decision': 'deny' if blocked else 'pass',
             'http_status': deny_status if blocked else 200,
             'intervention_status': deny_status if blocked else 200,
             'expected_status': 0,
             'reason_code': 'modsecurity_not_processed' if oversized else 'modsecurity_disruptive_intervention' if blocked else 'modsecurity_allow',
             'observed_status': '', 'result': ''}
    for field, expected in exact.items():
        if type(value[field]) is not type(expected) or value[field] != expected:
            raise ValueError('incorrect correlated decision field: ' + field)
    for field in ('timestamp', 'expected_status', 'intervention_status', 'http_status', 'anomaly_score'):
        if type(value[field]) is not int:
            raise ValueError('noninteger decision field: ' + field)
    if not start_time - 1 <= value['timestamp'] <= end_time + 1 or value['reason'] != value['reason_code']:
        raise ValueError('stale decision timestamp or reason')
    if type(expected_backend) is not int or expected_backend != (0 if blocked or case == 'truncated-request' else 1):
        raise ValueError('request block reached upstream or allow did not reach upstream')
    return value


def host_records(text, final=True):
    if final and text and not text.endswith('\n'):
        raise ValueError('unfinished final HAProxy log record')
    lines = text.splitlines() if not text or text.endswith('\n') else text.splitlines()[:-1]
    pattern = (r'^qualification probe=([^\s]+) id=([^\s]+) status=([0-9]{3}) action=([a-z_-]+) '
               r'rule=([0-9]+|-) phase=([0-9]+|-) error=([a-z0-9_-]+) '
               r'backend=([a-zA-Z0-9_<>()-]+) server=([a-zA-Z0-9_<>()-]+)$')
    records, readiness, seen_ids = {}, 0, set()
    for line in lines:
        if not line.startswith('qualification '):
            continue
        match = re.fullmatch(pattern, line)
        if match is None:
            raise ValueError('malformed HAProxy mapping/outcome log')
        probe, engine, status, action, rule, phase, error, backend, server = match.groups()
        if ((probe, status, action, rule, phase, error, backend, server) == ('-', '400', '-', '-', '-', '-', 'fe_spop', '<NOSRV>')
                and (engine == '-' or re.fullmatch(r'haproxy-htx-[1-9][0-9]*', engine))):
            readiness += 1
            if engine != '-':
                if engine in seen_ids:
                    raise ValueError('readiness reused a bound engine ID')
                seen_ids.add(engine)
            if readiness > 1:
                records[f'parser-reject-{readiness - 1}'] = {'engine_id': engine,
                    'status': 400, 'action': '-', 'rule': '-', 'phase': '-',
                    'error': '-', 'backend': backend, 'server': server}
            continue
        if not re.fullmatch(r'spop-[0-9a-f]{16}', probe) or not re.fullmatch(r'haproxy-htx-[1-9][0-9]*', engine):
            raise ValueError('host must bind a metadata probe to its own engine ID')
        if probe in records or engine in seen_ids:
            raise ValueError('duplicate probe mapping or reused engine ID within process generation')
        records[probe] = {'engine_id': engine, 'status': int(status), 'action': action,
                          'rule': rule, 'phase': phase, 'error': error, 'backend': backend, 'server': server}
        seen_ids.add(engine)
    return records


def verify_mappings(text, probes):
    records = host_records(text)
    keys = [probe.get('host_key', probe['id']) for probe in probes]
    if len(set(keys)) != len(probes) or len({probe['id'] for probe in probes}) != len(probes) or set(records) != set(keys):
        raise ValueError('final host mapping token set differs from probes')
    for probe in probes:
        if records[probe.get('host_key', probe['id'])]['engine_id'] != probe['engine_id']:
            raise ValueError('final host engine mapping changed after probe')
    return records


def verify_host(text, token, engine_id, status, action, rule=0, phase=2):
    record = host_records(text).get(token)
    if record is None or record['engine_id'] != engine_id or record['status'] != status or record['action'] != action:
        raise ValueError('missing or false correlated HAProxy host action')
    if record['rule'] != str(rule) or record['phase'] != str(phase):
        raise ValueError('host rule/phase differs from engine decision')
    expected_error = 'modsecurity_not_processed' if status == 413 else 'modsecurity_disruptive_intervention' if action == 'deny' else 'modsecurity_allow'
    if record['error'] != expected_error:
        raise ValueError('host reason differs from engine decision')
    if action == 'deny' and (record['server'] != '<NOSRV>' or record['backend'] != 'fe_spop'):
        raise ValueError('request deny selected an application server')
    if action == 'pass' and (record['backend'], record['server']) != ('be_app', 'app'):
        raise ValueError('request allow did not select the exact application backend')
    return record


def verify_request_mapping(text, probe):
    case = probe['case']
    if not case_contract(case)['decision'] or case == 'truncated-request':
        key = probe.get('host_key', probe['id'])
        record = host_records(text).get(key)
        bound = case in {'agent-unavailable', 'truncated-request'}
        expected_status = 503 if bound else 400
        if record != probe.get('host_record') or record is None or \
                record['status'] != expected_status or probe['status'] != expected_status or \
                record['engine_id'] != probe['engine_id'] or \
                (bound and (key != probe['id'] or not re.fullmatch(r'haproxy-htx-[1-9][0-9]*', probe['engine_id']))) or \
                (not bound and not re.fullmatch(r'parser-reject-[1-9][0-9]*', key)) or \
                (record['backend'], record['server']) != ('fe_spop', '<NOSRV>') or \
                any(record[key] != '-' for key in ('action', 'rule', 'phase', 'error')) or \
                probe['backend_requests'] != 0:
            raise ValueError('parser/agent-unavailable host rejection contradiction')
        if case == 'truncated-request':
            # The host rejects incomplete HTTP framing after the agent inspected
            # the available one-byte body. Its allow receipt is not dispatch.
            verify_request([probe['decision']], probe['engine_id'], case,
                           probe['begin'], probe['end'], 0)
            verify_client_response(case, probe['response'])
        elif probe['decision'] is not None:
            raise ValueError('unexpected engine decision for parser/agent rejection')
        return record
    decision = probe['decision']
    verify_request([decision], probe['engine_id'], probe['case'],
                   probe['begin'], probe['end'], probe['backend_requests'])
    # logasap records the request-stage SPOP outcome. Response-companion
    # interventions have separate receipts and may change the client status.
    return verify_host(text, probe['id'], probe['engine_id'], decision['http_status'],
                       'deny' if decision['disruptive'] else 'pass',
                       decision['rule_id'], decision['phase'])


def verify_parallel(observation):
    if (set(observation) != {'seen', 'peak', 'barrier_passes', 'errors', 'inflight'}
            or any(type(value) is not int for value in observation.values())
            or observation.get('seen') != 4 or observation.get('peak') != 4
            or observation.get('barrier_passes') != 4 or observation.get('errors') != 0
            or observation.get('inflight') != 0):
        raise ValueError('four-client overlap not proven at real upstream')


def verify_final_backend(observation, probes):
    engine_ids = [probe['engine_id'] for probe in probes if probe['engine_id'] != '-']
    if (len(set(engine_ids)) != len(engine_ids)
            or any(not re.fullmatch(r'haproxy-htx-[1-9][0-9]*', value) for value in engine_ids)):
        raise ValueError('backend probes must bind distinct host engine IDs within this start')
    expected = {probe['id']: probe for probe in probes if case_contract(probe['case'])['backend']}
    headers = observation['headers']
    if (observation['invalid_requests'] or observation['server_errors'] or len(headers) != len(expected)
            or {item['token'] for item in headers} != set(expected)):
        raise ValueError('final upstream header/token set differs from probes')
    accepts = {item['connection']: item for item in observation['accepts']}
    if len(accepts) != len(observation['accepts']) or any(item['queued'] for item in accepts.values()):
        raise ValueError('extra queued or duplicate upstream accept')
    used_connections = set()
    for token_value, probe in expected.items():
        matches = [item for item in headers if item['token'] == token_value]
        if len(matches) != 1:
            raise ValueError('duplicate upstream headers for probe')
        item = matches[0]
        contract = case_contract(probe['case'])
        expected_length = len(contract['body'])
        framing_ok = item['content_length'] == str(expected_length) or \
            (probe['case'].startswith('chunked-') and item.get('transfer_encoding') == 'chunked' and item['content_length'] is None)
        if (item['method'] != 'POST' or item['route'] != contract['route']
                or not framing_ok
                or item['completed'] is not True or item['body_bytes'] != expected_length
                or item.get('body_sha256') != contract['body_sha256'] or item.get('request_eos') is not True
                or item['error'] or item['connection'] not in accepts):
            raise ValueError('upstream method/route/body completion differs from probe')
        if (item.get('response_bytes'), item.get('response_sha256')) != \
                (len(contract['response']), contract['response_sha256']) or \
            (probe['case'] not in {'p3', 'slow'} and
                (item.get('response_eos') is not True or item.get('response_completed') is not True)):
            raise ValueError('origin response length/hash/EOS contradicts vector')
        used_connections.add(item['connection'])
    if used_connections != set(accepts):
        raise ValueError('upstream accept without an expected completed request')
    expected_counts = {token_value: 1 for token_value in expected}
    if observation['counts'] != expected_counts:
        raise ValueError('final upstream completion set differs from probes')


def verify_final_decisions(records, probes):
    selected = [probe for probe in probes if case_contract(probe['case'])['decision']]
    expected = {probe['engine_id'] for probe in selected}
    if len(expected) != len(selected):
        raise ValueError('duplicate expected probe token')
    if (any(type(item) is not dict or set(item) != RECORD_FIELDS for item in records)
            or len(records) != len(expected)
            or any(type(item['request_id']) is not str for item in records)
            or {item['request_id'] for item in records} != expected):
        raise ValueError('final SPOP decision schema/token set differs from probes')
    for probe in selected:
        record = verify_request(records, probe['engine_id'], probe['case'],
                                probe['begin'], probe['end'], probe['backend_requests'])
        if record != probe['decision']:
            raise ValueError('final SPOP decision changed after probe')


def verify_p3_receipt(text, probes):
    selected = [probe for probe in probes if probe['case'] == 'p3']
    expected = {probe['engine_id']: probe for probe in selected}
    marker = 'modsecurity-htx: response-companion phase-3 intervention;'
    lines = [line for line in text.splitlines() if marker in line]
    pattern = (r'^.*' + re.escape(marker) + r' transaction_id=([^\s]+) phase=([^\s]+) '
               r'rule_id=([^\s]+) requested=([^\s]+) requested_status=([^\s]+) '
               r'host_action=([^\s]+) host_status=([^\s]+)$')
    matches = [re.fullmatch(pattern, line) for line in lines]
    if any(match is None for match in matches) or any(line.count(marker) != 1 for line in lines):
        raise ValueError('malformed native P3 host receipt')
    values = [match.groups() for match in matches]
    if (len(expected) != len(selected) or len(values) != len(selected)
            or {value[0] for value in values} != set(expected)):
        raise ValueError('P3 host receipt token set or multiplicity differs from probes')
    outcomes = []
    for engine_id, phase, rule, requested, requested_status, actual, actual_status in values:
        probe = expected[engine_id]
        if (phase, rule, requested, requested_status) != ('3', '1100201', 'deny', '403'):
            raise ValueError('P3 engine request differs from fixture contract')
        decision = probe['decision']
        verify_request([decision], engine_id, 'p3', probe['begin'], probe['end'], probe['backend_requests'])
        if (actual, actual_status, probe['status']) == ('deny', '403', 403):
            outcomes.append({'engine_id': engine_id, 'status': 'passed_prerequisite'})
        elif (actual, actual_status, probe['status']) == ('error', '500', 500):
            outcomes.append({'engine_id': engine_id, 'status': 'failed', 'reason': 'native_renderer_fallback_500'})
        else:
            raise ValueError('P3 host action/status contradicts client or enforcement contract')
    return {'status': 'failed' if any(value['status'] == 'failed' for value in outcomes) else 'passed_prerequisite',
            'receipts': outcomes}


def verify_p4_receipt(text, probes):
    selected = [probe for probe in probes if probe['case'] == 'p4']
    expected = [probe.get('engine_id', probe['id']) for probe in selected]
    marker = 'modsecurity-htx: response-companion phase-4 intervention;'
    lines = [line for line in text.splitlines() if marker in line]
    pattern = (r'^.*' + re.escape(marker)
               + r' transaction_id=([^\s]+) rule_id=([^\s]*) requested=([^\s]+) host_action=([^\s]+)$')
    matches = [re.fullmatch(pattern, line) for line in lines]
    if any(match is None for match in matches) or any(line.count(marker) != 1 for line in lines):
        raise ValueError('malformed native P4 host receipt')
    values = [match.groups() for match in matches]
    # The first pinned real host emits an internal HTX ID and an empty rule
    # field. This is parseable metadata, but cannot correlate engine/rule to
    # a client probe. Retain this exact observed gap as BLOCKED, never as a
    # correlated receipt or a phase-4 gate pass.
    if values and all(re.fullmatch(r'haproxy-htx-[1-9][0-9]*', value[0]) and value[1] == '' for value in values):
        if (len(values) != len(expected) or len({value[0] for value in values}) != len(values)
                or any(value[2:] != ('deny', 'log_only') for value in values)):
            raise ValueError('uncorrelated native P4 receipt multiplicity/action differs from probes')
        if all('engine_id' in probe for probe in selected) and {value[0] for value in values} != set(expected):
            raise ValueError('native P4 ID differs from bound host engine ID')
        return {'status': 'blocked', 'reason': 'native_internal_id_and_missing_rule',
                'observed_receipts': [{'transaction_id': value[0], 'rule_id': '',
                    'requested': value[2], 'host_action': value[3]} for value in values],
                'expected_probe_tokens': [probe['id'] for probe in selected]}
    if (len(set(expected)) != len(expected) or len(values) != len(expected)
            or {value[0] for value in values} != set(expected)):
        raise ValueError('P4 host receipt token set or multiplicity differs from probes')
    if any(value[1:] != ('1100301', 'deny', 'log_only') for value in values):
        raise ValueError('P4 client allow lacks exact Safe host/rule receipt')
    return {'status': 'passed_prerequisite', 'expected_engine_ids': expected,
            'expected_probe_tokens': [probe['id'] for probe in selected]}


def verify_boundary_receipts(text, probes, *, complete=True):
    selected_probes = [probe for probe in probes if probe['case'] in {'limit', 'slow'}]
    selected = {probe['engine_id']: probe for probe in selected_probes}
    if len(selected) != len(selected_probes):
        raise ValueError('duplicate expected response boundary engine identity')
    marker = 'modsecurity-htx: fail-closed postcommit '
    outcomes = {}
    pattern = re.compile(r'^.*' + re.escape(marker) + r'response-companion body; transaction_id=(haproxy-htx-[1-9][0-9]*)$')
    for line in text.splitlines():
        if marker not in line:
            continue
        match = pattern.fullmatch(line)
        if match is None or line.count(marker) != 1 or match[1] not in selected or match[1] in outcomes:
            raise ValueError('unexpected/duplicate/malformed postcommit response boundary receipt')
        outcomes[match[1]] = {'stage': 'response-companion body', 'host_action': 'close'}
    if complete and set(outcomes) != set(selected):
        raise ValueError('missing response limit/timeout host receipt')
    return outcomes


def await_boundary_receipts(root, probes):
    # The pinned slow-abort vector resumes origin output after the 2000ms
    # companion deadline. Freeze only its exact close receipt, not a snapshot
    # that can acquire an optional abort outcome during final reconciliation.
    expected = {probe['engine_id'] for probe in probes if probe['case'] in {'limit', 'slow'}}
    deadline = time.monotonic() + 6
    while time.monotonic() < deadline:
        text = private_read(root / 'haproxy.log', MAX_FILE)
        if text and not text.endswith('\n'):
            text = text.rsplit('\n', 1)[0] + '\n' if '\n' in text else ''
        receipts = verify_boundary_receipts(text, probes, complete=False)
        if set(receipts) == expected:
            return text, verify_boundary_receipts(text, probes)
        time.sleep(.02)
    raise ValueError('response boundary host receipt deadline exceeded')


def verify_extended_evidence(result, text):
    probes = result['probes']
    if not set(BOUNDARY_CASES) <= {probe['case'] for probe in probes} or \
        not any(probe['case'] == 'slow' and probe.get('abort') for probe in probes):
        raise ValueError('incomplete boundary/error campaign')
    for probe in probes:
        verify_client_response(probe['case'], probe['response'], probe.get('abort', False))
        if probe['backend_requests'] != case_contract(probe['case'])['backend']:
            raise ValueError('boundary backend dispatch contradiction')
    verify_parallel(result['parallel'])
    if result['p3_receipts']['status'] != 'passed_prerequisite' or \
        result['p4_receipts']['status'] != 'passed_prerequisite':
        raise ValueError('full G4 requires exact P3/P4 receipts')
    receipts = verify_boundary_receipts(text, probes)
    if result['boundary_receipts'] != receipts:
        raise ValueError('response boundary receipts changed after observation')
    required = {probe['id'] for probe in probes if probe['case'] in set(BOUNDARY_CASES) | {'p3', 'p4', 'agent-unavailable'}}
    recoveries = result['recoveries']
    if len(recoveries) != len(required) or {item['failure_id'] for item in recoveries} != required:
        raise ValueError('missing/duplicate same-host boundary recovery')
    by_id = {probe['id']: probe for probe in probes}
    allow_ids = set()
    for recovery in recoveries:
        followup = by_id.get(recovery['allow_id'])
        if followup is None or followup['case'] != 'allow' or followup['status'] != 200 or \
            followup['backend_requests'] != 1 or recovery['host_before'] != recovery['host_after'] or \
            recovery['host_after'] != result['identities'][1] or recovery['allow_id'] in allow_ids or \
            probes.index(followup) != probes.index(by_id[recovery['failure_id']]) + 1:
            raise ValueError('same-process allow recovery contradiction')
        allow_ids.add(recovery['allow_id'])
    generations = result['agent_generations']
    if len(generations) != 2 or generations[0] != result['identities'][0] or \
        (generations[0]['pid'], generations[0]['start_token']) == (generations[1]['pid'], generations[1]['start_token']) or \
        generations[0]['exe'] != generations[1]['exe'] or generations[0]['exe_sha256'] != generations[1]['exe_sha256'] or \
        not any(probe['case'] == 'agent-unavailable' for probe in probes):
        raise ValueError('controlled pinned agent replacement unproven')
    stopped = result['agent_stop']
    if set(stopped) != {'identity', 'exit_status', 'uds_removed'} or stopped['identity'] != generations[0] or \
        type(stopped['exit_status']) is not int or stopped['exit_status'] not in (0, -signal.SIGTERM) or \
        stopped['uds_removed'] is not True:
        raise ValueError('original agent controlled shutdown unproven')
    if set(result['resource_segments']) != {'before_agent_stop', 'during_agent_unavailable', 'after_agent_restart'} or \
        result.get('keepalive_alternation') is not True:
        raise ValueError('complete monitored keepalive/parallel/error segments missing')
    segment_identities = {'before_agent_stop': {'spoa': generations[0], 'haproxy': result['identities'][1]},
        'during_agent_unavailable': {'haproxy': result['identities'][1]},
        'after_agent_restart': {'spoa-generation-2': generations[1], 'haproxy': result['identities'][1]}}
    for name, segment in result['resource_segments'].items():
        if set(segment) != {'before', 'peak', 'after'}:
            raise ValueError('missing monitored resource observations')
        identities = segment_identities[name]
        for stage, samples in segment.items():
            if set(samples) != set(identities):
                raise ValueError('missing/foreign monitored process sample')
            for label, sample in samples.items():
                if set(sample) != {'pid', 'start_token', 'rss_bytes', 'fd'} or \
                    any(type(sample[key]) is not int for key in ('pid', 'rss_bytes', 'fd')) or \
                    (sample['pid'], sample['start_token']) != (identities[label]['pid'], identities[label]['start_token']) or \
                    not 0 <= sample['rss_bytes'] <= MAX_RSS or not 0 <= sample['fd'] <= MAX_FD or \
                    any(sample[key] > segment['peak'][label][key] for key in ('rss_bytes', 'fd')):
                    raise ValueError('resource sample identity/budget/peak contradiction')
    by_id = {probe['id']: probe for probe in probes}
    keepalive = result['keepalive']
    if set(keepalive) != {'ids', 'host_before', 'host_after'} or \
        keepalive['host_before'] != result['identities'][1] or keepalive['host_after'] != keepalive['host_before'] or \
        len(keepalive['ids']) != 5 or len(set(keepalive['ids'])) != 5 or \
        [by_id.get(key, {}).get('case') for key in keepalive['ids']] != ['allow', 'p1', 'allow', 'p2', 'allow'] or \
        len([probe for probe in probes if probe['case'] == 'parallel']) != 4:
        raise ValueError('complete alternating keepalive/four-client probe set missing')
    indices = [probes.index(by_id[key]) for key in keepalive['ids']]
    if indices != list(range(indices[0], indices[0] + 5)):
        raise ValueError('keepalive probes were not one contiguous alternating sequence')


class Upstream(ThreadingHTTPServer):
    daemon_threads = False
    block_on_close = True

    def __init__(self):
        self.lock = threading.Lock()
        self.counts = {}
        self.invalid_requests = 0
        self.server_errors = 0
        self.expected_resets = 0
        self.accepts = []
        self.headers_seen = []
        self.connection_ids = {}
        self.parser_progress = {}
        self.live = set()
        self.stopping = threading.Event()
        self.parallel = {'seen': 0, 'peak': 0, 'barrier_passes': 0, 'errors': 0, 'inflight': 0}
        self.barrier = threading.Barrier(4, timeout=5)
        super().__init__(('127.0.0.1', 0), Handler)
        self.thread = threading.Thread(target=self.serve_forever, daemon=False)
        self.thread.start()

    def get_request(self):
        connection, address = super().get_request()
        self.note_accept(connection)
        connection.settimeout(5)
        return connection, address

    def note_accept(self, connection, queued=False):
        with self.lock:
            number = len(self.accepts) + 1
            self.accepts.append({'connection': number, 'queued': queued})
            self.connection_ids[connection] = number
            self.parser_progress[connection] = {'request_started': False, 'active': None}
            if number > 128:
                self.invalid_requests += 1

    def snapshot(self):
        with self.lock:
            return {'counts': dict(self.counts), 'invalid_requests': self.invalid_requests,
                    'server_errors': self.server_errors, 'expected_resets': self.expected_resets,
                    'accepts': [dict(item) for item in self.accepts],
                    'headers': [dict(item) for item in self.headers_seen]}

    def process_request(self, request, address):
        with self.lock:
            self.live.add(request)
        super().process_request(request, address)

    def handle_error(self, request, client_address):
        error = sys.exc_info()[1]
        with self.lock:
            connection = self.connection_ids.get(request)
            observed = [item for item in self.headers_seen if item['connection'] == connection]
            last = observed[-1] if observed else None
            progress = self.parser_progress.get(request, {'request_started': True, 'active': None})
            expected = (isinstance(error, (ConnectionResetError, BrokenPipeError))
                        and last is not None and last['completed']
                        and (not progress['request_started'] or progress['active'] is last)
                        and (last['response_completed'] or
                             (last['route'] in {'slow', 'limit'} and last['response_headers_sent'])))
            if expected:
                self.expected_resets += 1
            else:
                self.server_errors += 1
        if not expected:
            super().handle_error(request, client_address)

    def shutdown_request(self, request):
        super().shutdown_request(request)
        with self.lock:
            self.live.discard(request)
            self.connection_ids.pop(request, None)
            self.parser_progress.pop(request, None)

    def count(self, token):
        with self.lock:
            return self.counts.get(token, 0)

    def close(self):
        self.stopping.set()
        self.barrier.abort()
        self.shutdown()
        # The only product producers have been reaped by the caller. Drain
        # the TCP accept queue to EAGAIN so an observer scheduling delay can
        # never turn a queued backend dispatch into a false zero.
        self.socket.setblocking(False)
        queued = 0
        while True:
            try:
                connection, _address = self.socket.accept()
            except BlockingIOError:
                break
            queued += 1
            self.note_accept(connection, queued=True)
            connection.close()
        with self.lock:
            pending = list(self.live)
        for connection in pending:
            try:
                connection.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            connection.close()
        self.server_close()
        self.thread.join(timeout=2)
        if self.thread.is_alive() or self.live:
            raise ValueError('upstream handler/socket cleanup failed')
        if queued:
            raise ValueError('unobserved queued upstream dispatch at cleanup')


class ProgressReader:
    """Observe first request/header bytes even when readline later resets.

    BufferedReader.readline can raise after receiving a partial line without
    returning those bytes. Reading its first byte separately closes that gap;
    the remaining bounded line uses the ordinary buffered parser.
    """

    def __init__(self, reader, mark_started):
        self.reader = reader
        self.mark_started = mark_started

    def readline(self, size=-1):
        if size == 0:
            return b''
        first = self.reader.read(1)
        if not first:
            return first
        self.mark_started()
        if first == b'\n' or size == 1:
            return first
        return first + self.reader.readline(size - 1 if size > 0 else -1)

    def __getattr__(self, name):
        return getattr(self.reader, name)


class Handler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def setup(self):
        super().setup()
        self.rfile = ProgressReader(self.rfile, self.mark_request_started)

    def mark_request_started(self):
        with self.server.lock:
            self.server.parser_progress[self.connection]['request_started'] = True

    def handle_one_request(self):
        with self.server.lock:
            self.server.parser_progress[self.connection] = {'request_started': False, 'active': None}
        try:
            super().handle_one_request()
        finally:
            with self.server.lock:
                progress = self.server.parser_progress[self.connection]
                if progress['request_started'] and (progress['active'] is None or not progress['active']['completed']):
                    self.server.invalid_requests += 1

    def parse_request(self):
        self.observation = None
        if not super().parse_request():
            with self.server.lock:
                self.server.invalid_requests += 1
            return False
        tokens = self.headers.get_all('X-Request-ID', [])
        token_value = tokens[0] if len(tokens) == 1 and re.fullmatch(r'spop-[0-9a-f]{16}', tokens[0]) else None
        route = self.path.removeprefix('/')
        if route not in {'allow', 'p3', 'p4', 'slow', 'limit', 'parallel', 'response-empty', 'response-exact'}:
            route = None
        lengths = self.headers.get_all('Content-Length', [])
        length = lengths[0] if len(lengths) == 1 and lengths[0].isdecimal() else None
        transfers = self.headers.get_all('Transfer-Encoding', [])
        transfer = 'chunked' if transfers == ['chunked'] and not lengths else None
        with self.server.lock:
            self.observation = {'connection': self.server.connection_ids[self.connection],
                'token': token_value, 'method': self.command if self.command == 'POST' else 'unsupported',
                'route': route, 'content_length': length, 'completed': False, 'body_bytes': 0, 'error': False,
                'response_headers_sent': False, 'response_completed': False,
                'transfer_encoding': transfer, 'body_sha256': '', 'request_eos': False,
                'response_bytes': 0, 'response_sha256': '', 'response_eos': False}
            self.server.headers_seen.append(self.observation)
            self.server.parser_progress[self.connection]['active'] = self.observation
            if len(self.server.headers_seen) > 128 or token_value is None or route is None or (length is None and transfer is None):
                self.server.invalid_requests += 1
        return True

    def do_POST(self):
        self.connection.settimeout(5)
        token = self.observation['token']
        case = self.observation['route']
        if token is None or case is None:
            with self.server.lock:
                self.server.invalid_requests += 1
            self.close_connection = True
            return
        length = self.observation['content_length']
        chunked = self.observation['transfer_encoding'] == 'chunked'
        if (length is None and not chunked) or (length is not None and int(length) > LIMIT) or \
                (self.headers.get_all('Transfer-Encoding') and not chunked):
            with self.server.lock:
                self.server.invalid_requests += 1
            self.close_connection = True
            return
        body = bytearray()
        deadline = time.monotonic() + 5
        def bounded_read(count):
            while count:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise ValueError('origin body deadline')
                self.connection.settimeout(remaining)
                data = self.rfile.read1(min(count, 4096))
                if not data:
                    raise ValueError('truncated origin request body')
                count -= len(data)
                body.extend(data)
        def framing_bytes(count):
            data = bytearray()
            while len(data) < count:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise ValueError('origin chunk framing deadline')
                self.connection.settimeout(remaining)
                piece = self.rfile.read1(count - len(data))
                if not piece:
                    raise ValueError('truncated origin chunk framing')
                data.extend(piece)
            return bytes(data)
        try:
            if chunked:
                while True:
                    line = bytearray()
                    while not line.endswith(b'\r\n') and len(line) < 34:
                        line.extend(framing_bytes(1))
                    if not re.fullmatch(rb'[0-9A-Fa-f]{1,8}\r\n', line):
                        raise ValueError('invalid bounded origin chunk')
                    size = int(line[:-2], 16)
                    if len(body) + size > LIMIT:
                        raise ValueError('origin chunk body limit')
                    bounded_read(size)
                    if framing_bytes(2) != b'\r\n':
                        raise ValueError('origin chunk delimiter/trailer')
                    if size == 0:
                        break
            else:
                bounded_read(int(length))
            body_bytes = len(body)
        except (OSError, ValueError):
            with self.server.lock:
                self.observation['error'] = True
                self.server.invalid_requests += 1
            return
        with self.server.lock:
            self.observation['body_bytes'] = body_bytes
            self.observation['body_sha256'] = hashlib.sha256(body).hexdigest()
            self.observation['request_eos'] = True
            self.observation['completed'] = chunked or body_bytes == int(length)
        if not self.observation['completed']:
            with self.server.lock:
                self.server.invalid_requests += 1
            return
        origin = self.server
        with origin.lock:
            origin.counts[token] = origin.counts.get(token, 0) + 1
        body = case_contract(case)['response']
        with origin.lock:
            self.observation['response_bytes'] = len(body)
            self.observation['response_sha256'] = hashlib.sha256(body).hexdigest()
        if case == 'parallel':
            with origin.lock:
                origin.parallel['seen'] += 1
                origin.parallel['inflight'] += 1
                origin.parallel['peak'] = max(origin.parallel['peak'], origin.parallel['inflight'])
            try:
                origin.barrier.wait()
                with origin.lock:
                    origin.parallel['barrier_passes'] += 1
                origin.stopping.wait(0.1)
            except threading.BrokenBarrierError:
                with origin.lock:
                    origin.parallel['errors'] += 1
            finally:
                with origin.lock:
                    origin.parallel['inflight'] -= 1
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('X-Qualification-P3', 'deny' if case == 'p3' else 'allow')
        self.end_headers()
        with origin.lock:
            self.observation['response_headers_sent'] = True
        if case == 'slow':
            origin.stopping.wait(3)
        try:
            if self.wfile.write(body) != len(body):
                raise ValueError('short origin response write')
            self.wfile.flush()
            with origin.lock:
                self.observation['response_completed'] = True
                self.observation['response_eos'] = True
        except (BrokenPipeError, ConnectionResetError):
            if case not in {'slow', 'limit'}:
                raise
            with origin.lock:
                origin.expected_resets += 1

    def log_message(self, *_args):
        pass


def free_port():
    with socket.socket() as connection:
        connection.bind(('127.0.0.1', 0))
        return connection.getsockname()[1]


def configuration(root, rules, front, spoa, upstream):
    # Every interpolated path passes an explicit configuration grammar guard.
    for path in (root, rules):
        safe_path(str(path))
    uds = root / 'mrc.sock'
    if len(str(uds).encode()) >= 100:
        raise ValueError('MRC1 socket path exceeds private profile budget')
    agent = f'''listen=127.0.0.1:{spoa}
log-file={root}/agent.log
decision-log={root}/decision.jsonl
audit-log={root}/audit.log
rules-file={rules}
mode=block
fail-mode=closed
runtime-mode=production
variant=spop-qualification
case=qualification
request-body-limit={LIMIT}
response-companion=native-htx
response-companion-socket={uds}
response-companion-uid={os.getuid()}
response-companion-gid={os.getgid()}
response-body-limit={LIMIT}
response-body-timeout=2000
spoe-timeout=2000
max-transactions=64
worker-count=8
'''
    spoe = '''[modsecurity]
spoe-agent modsecurity-agent
    groups request-check
    option var-prefix modsec
    register-var-names blocked action status rule_id phase error response_handle
    max-frame-size 65532
    timeout hello 1s
    timeout idle 3s
    timeout processing 2s
    use-backend be_spoa
spoe-group request-check
    messages check-request
spoe-message check-request
    args request_id=unique-id client_ip=src client_port=src_port server_ip=dst server_port=dst_port method=method path=path uri=url host=req.hdr(host) headers_bin=req.hdrs_bin headers=req.hdrs body=req.body body_len=req.body_len
'''
    host = f'''global
    log stdout format raw local0
    nbthread 1
    tune.bufsize 65536
defaults
    log global
    mode http
    timeout connect 1s
    timeout client 5s
    timeout server 5s
    option logasap
    log-format "qualification probe=%[var(txn.qualification_probe)] id=%ID status=%ST action=%[var(txn.modsec.action)] rule=%[var(txn.modsec.rule_id)] phase=%[var(txn.modsec.phase)] error=%[var(txn.modsec.error)] backend=%b server=%s"
frontend fe_spop
    bind 127.0.0.1:{front}
    unique-id-format haproxy-htx-%rt
    option http-buffer-request
    filter spoe engine modsecurity config {root}/spoe.cfg
    filter modsecurity-htx response-companion-socket {uds} response-companion-timeout-ms 2000 response-companion-uid {os.getuid()} response-companion-gid {os.getgid()} phase4-mode safe
    http-request set-var(txn.qualification_probe) req.hdr(X-Request-ID)
    http-request send-spoe-group modsecurity request-check
    http-request deny status 503 unless {{ var(txn.modsec.action) -m str pass deny }}
    http-request deny status 413 if {{ var(txn.modsec.blocked) -m bool }} {{ var(txn.modsec.status) -m int 413 }} {{ var(txn.modsec.phase) -m int 2 }} {{ var(txn.modsec.rule_id) -m int 0 }} {{ var(txn.modsec.action) -m str deny }} {{ var(txn.modsec.error) -m str modsecurity_not_processed }}
    http-request deny status 403 if {{ var(txn.modsec.blocked) -m bool }}
    default_backend be_app
backend be_app
    server app 127.0.0.1:{upstream}
backend be_spoa
    mode spop
    timeout connect 1s
    timeout server 3s
    server agent 127.0.0.1:{spoa}
'''
    return {'agent.conf': agent, 'spoe.cfg': spoe, 'haproxy.cfg': host}


def token():
    return 'spop-' + os.urandom(8).hex()


def wire(case, request_id, close=True):
    vector = case_contract(case)
    route, body = vector['route'], vector['body']
    header = 'X-Qualification-P1: deny\r\n' if case == 'p1' else ''
    framing = f'Content-Length: {len(body)}\r\n'
    if case.startswith('chunked-'):
        framing = 'Transfer-Encoding: chunked\r\n'
        body = b'2\r\n' + body[:2] + b'\r\n' + f'{len(body) - 2:x}\r\n'.encode() + body[2:] + b'\r\n0\r\n\r\n'
    if case == 'invalid-cl':
        framing = 'Content-Length: 1\r\nContent-Length: 2\r\n'
    if case == 'invalid-te':
        framing, body = 'Content-Length: 1\r\nTransfer-Encoding: chunked\r\n', b'Z\r\nx\r\n0\r\n\r\n'
    if case == 'truncated-request':
        framing, body = 'Content-Length: 2048\r\n', b'x'
    return (f'POST /{route} HTTP/1.1\r\nHost: localhost\r\nX-Request-ID: {request_id}\r\n'
            f'{header}Content-Type: text/plain\r\n{framing}'
            f'Connection: {"close" if close else "keep-alive"}\r\n\r\n').encode() + body


def await_decision(root, request_id):
    deadline = time.monotonic() + 6
    while time.monotonic() < deadline:
        try:
            values = read_events(root / 'decision.jsonl')
            mapping = host_records(private_read(root / 'haproxy.log', MAX_FILE), final=False).get(request_id)
            if mapping is not None and any(type(value) is dict and value.get('request_id') == mapping['engine_id'] for value in values):
                return values, mapping['engine_id']
        except FileNotFoundError:
            pass
        time.sleep(0.02)
    raise ValueError('SPOP correlated decision deadline exceeded')


def client_response(connection, *, keepalive=False, abort=False):
    return _client_response(connection, keepalive=keepalive, abort=abort)


def malformed_client_response(connection, case):
    if case not in MALFORMED_CASES:
        raise ValueError('zero-byte close is restricted to malformed request probes')
    value = _client_response(connection, allow_zero_close=True)
    verify_client_response(case, value)
    return value


def response_limit_client_response(connection):
    # stream_shutdown may run before HAProxy flushes any client response header.
    # Final host receipt, decision and origin reconciliation still prove why.
    value = _client_response(connection, allow_zero_close=True)
    verify_client_response('limit', value)
    return value


def _client_response(connection, *, keepalive=False, abort=False, allow_zero_close=False):
    deadline = time.monotonic() + 6
    begin = time.monotonic()
    def recv(size):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise ValueError('client response absolute deadline')
        connection.settimeout(remaining)
        return connection.recv(size)
    header = bytearray()
    while not header.endswith(b'\r\n\r\n'):
        piece = recv(1)
        if not piece and not header and allow_zero_close:
            # No HTTP bytes were received. Separate host/decision reconciliation
            # must bind the exact parser400, truncated503 or response-limit abort.
            return {'status': None, 'declared_bytes': 0, 'body_bytes': 0,
                'body_sha256': hashlib.sha256(b'').hexdigest(), 'eos': False,
                'termination': 'zero_close', 'elapsed_seconds': time.monotonic() - begin}
        if not piece or len(header) >= 16384:
            raise ValueError('client response header incomplete/oversized')
        header.extend(piece)
    lines = bytes(header).split(b'\r\n')
    match = re.fullmatch(rb'HTTP/1\.1 ([0-9]{3}) [^\r\n]+', lines[0])
    if not match:
        raise ValueError('client response status framing')
    fields = {}
    for line in lines[1:-2]:
        key, colon, value = line.partition(b':')
        if not colon or not re.fullmatch(rb'[A-Za-z0-9-]+', key):
            raise ValueError('client response header framing')
        fields.setdefault(key.lower(), []).append(value.strip().lower())
    lengths = fields.get(b'content-length', [])
    if len(lengths) != 1 or not re.fullmatch(rb'[0-9]+', lengths[0]) or \
        int(lengths[0]) > LIMIT + 16384 or fields.get(b'transfer-encoding') or \
        (keepalive and any(b'close' in item.split(b',') for item in fields.get(b'connection', []))):
        raise ValueError('client response bounded framing/keepalive contradiction')
    declared = int(lengths[0])
    body = bytearray()
    termination = 'framed'
    if abort:
        connection.shutdown(socket.SHUT_RDWR)
        termination = 'client_abort'
    else:
        while len(body) < declared:
            piece = recv(min(4096, declared - len(body)))
            if not piece:
                termination = 'eof'
                break
            body.extend(piece)
        if not keepalive and termination != 'eof':
            if recv(1):
                raise ValueError('bytes after declared client response')
            termination = 'eof'
    return {'status': int(match[1]), 'declared_bytes': declared, 'body_bytes': len(body),
        'body_sha256': hashlib.sha256(body).hexdigest(), 'eos': len(body) == declared and not abort,
        'termination': termination, 'elapsed_seconds': time.monotonic() - begin}


def verify_client_response(case, value, abort=False):
    if case in MALFORMED_CASES | {'limit'} and value.get('termination') == 'zero_close':
        expected = {'status': None, 'declared_bytes': 0, 'body_bytes': 0,
            'body_sha256': hashlib.sha256(b'').hexdigest(), 'eos': False,
            'termination': 'zero_close'}
        elapsed = value.get('elapsed_seconds')
        if abort or set(value) != set(expected) | {'elapsed_seconds'} or \
                any(type(value[key]) is not type(wanted) or value[key] != wanted
                    for key, wanted in expected.items()) or \
                type(elapsed) not in (float, int) or not math.isfinite(elapsed) or not 0 <= elapsed < 6:
            raise ValueError('malformed-request zero-byte close contradiction')
        return
    if set(value) != {'status', 'declared_bytes', 'body_bytes', 'body_sha256', 'eos', 'termination', 'elapsed_seconds'} or \
        any(type(value[key]) is not int for key in ('status', 'declared_bytes', 'body_bytes')) or \
        type(value['eos']) is not bool or type(value['body_sha256']) is not str or \
        not re.fullmatch(r'[0-9a-f]{64}', value['body_sha256']) or \
        type(value['elapsed_seconds']) not in (float, int) or not math.isfinite(value['elapsed_seconds']) or \
        not 0 <= value['elapsed_seconds'] < 6 or not 0 <= value['body_bytes'] <= value['declared_bytes'] <= LIMIT + 16384 or \
        value['termination'] not in ('framed', 'eof', 'client_abort') or \
        value['eos'] != (value['body_bytes'] == value['declared_bytes'] and not abort) or \
        (not abort and value['termination'] == 'client_abort'):
        raise ValueError('client response schema/framing contradiction')
    vector = case_contract(case)
    if value['status'] != vector['status']:
        raise ValueError('client status contradicts closed vector')
    if case in MALFORMED_CASES and (abort or not value['eos'] or value['termination'] != 'eof'):
        raise ValueError('malformed request requires complete HTTP400 or zero-byte EOF')
    if abort:
        if value['termination'] != 'client_abort' or value['eos'] or value['body_bytes'] != 0:
            raise ValueError('client abort observation contradicts declared action')
        return
    if case in {'limit', 'slow'}:
        if value['termination'] != 'eof' or value['eos'] or \
            not 0 <= value['body_bytes'] < len(vector['response']) or \
            value['declared_bytes'] != len(vector['response']) or \
            value['body_sha256'] != hashlib.sha256(vector['response'][:value['body_bytes']]).hexdigest():
            raise ValueError('response limit/timeout requires exact incomplete EOF, never client timeout')
        if case == 'slow' and not 1.5 <= value['elapsed_seconds'] < 6:
            raise ValueError('response timeout timing contradicts pinned 2000ms profile')
    elif not value['eos']:
        raise ValueError('ordinary client response incomplete')
    elif vector['status'] == 200 and (value['declared_bytes'], value['body_bytes'], value['body_sha256']) != \
        (len(vector['response']), len(vector['response']), vector['response_sha256']):
        raise ValueError('allow client response length/hash differs from vector')


def rejection_probe(root, front, origin, case):
    request_id = token()
    before = host_records(private_read(root / 'haproxy.log', MAX_FILE), final=False)
    begin = time.time()
    with socket.create_connection(('127.0.0.1', front), timeout=5) as connection:
        connection.sendall(wire(case, request_id))
        if case in MALFORMED_CASES:
            connection.shutdown(socket.SHUT_WR)
        response = malformed_client_response(connection, case) if case in MALFORMED_CASES else client_response(connection)
    verify_client_response(case, response)
    deadline = time.monotonic() + 6
    while time.monotonic() < deadline:
        after = host_records(private_read(root / 'haproxy.log', MAX_FILE), final=False)
        added = set(after) - set(before)
        if added:
            if len(added) != 1 or any(after[key] != value for key, value in before.items()):
                raise ValueError('unrelated/mutated host record during parser/agent rejection')
            key = added.pop()
            record = after[key]
            if case in {'agent-unavailable', 'truncated-request'} and key != request_id or case in PARSER_REJECT_CASES and not re.fullmatch(r'parser-reject-[1-9][0-9]*', key):
                raise ValueError('rejection host mapping contradicts probe identity')
            observed = {'id': request_id, 'engine_id': record['engine_id'], 'host_key': key,
                'host_record': record, 'case': case, 'status': record['status'], 'response': response,
                'backend_requests': origin.count(request_id), 'decision': None,
                'begin': begin, 'end': time.time()}
            if case == 'truncated-request':
                values, engine_id = await_decision(root, request_id)
                observed['end'] = time.time()
                if engine_id != observed['engine_id']:
                    raise ValueError('truncated-request engine identity changed')
                observed['decision'] = verify_request(values, engine_id, case,
                    begin, observed['end'], observed['backend_requests'])
            verify_request_mapping(private_read(root / 'haproxy.log', MAX_FILE), observed)
            return observed
        time.sleep(.02)
    raise ValueError('parser/agent-unavailable host receipt deadline')


def probe(root, front, origin, case, connection=None, abort=False):
    request_id = token()
    own = connection is None
    connection = connection or socket.create_connection(('127.0.0.1', front), timeout=5)
    connection.settimeout(5)
    begin = time.time()
    connection.sendall(wire(case, request_id, close=own))
    try:
        response = response_limit_client_response(connection) if case == 'limit' and own and not abort else \
            client_response(connection, keepalive=not own, abort=abort)
        verify_client_response(case, response, abort)
    finally:
        if own:
            connection.close()
    values, engine_id = await_decision(root, request_id)
    record = verify_request(values, engine_id, case, begin, time.time(), origin.count(request_id))
    return {'id': request_id, 'engine_id': engine_id, 'case': case, 'status': response['status'],
            'truncated': not response['eos'] and not abort, 'response': response,
            'abort': abort, 'backend_requests': origin.count(request_id), 'decision': record,
            'begin': begin, 'end': time.time()}


def invalidate_cleanup(result, errors):
    if errors:
        result['result'] = 'FAIL'
        result['passed'] = False
        result['cleanup_errors'] = errors
        result['gates']['G9'] = 'failed'
        for key in ('G2', 'G3', 'G4', 'G5', 'G6', 'G7'):
            result['gates'][key] = 'failed'


def run_start(args, root, extended):
    root.mkdir(mode=0o700)
    result = {'result': 'FAIL', 'passed': False, 'catalog_acceptance': False,
              'gates': {f'G{i}': 'blocked' for i in range(1, 10)}, 'probes': []}
    children = []
    origin = None
    monitor = None
    rules = None
    try:
        rules = args.bound_rules.copy(root / 'rules.conf')
        origin = Upstream()
        front, spoa = free_port(), free_port()
        if len({front, spoa, origin.server_port}) != 3:
            raise ValueError('loopback ports collide')
        configs = configuration(root, rules.path, front, spoa, origin.server_port)
        for name, content in configs.items():
            private_write(root / name, content)
        result['configuration_sha256'] = {name: hashlib.sha256(content.encode()).hexdigest() for name, content in configs.items()}
        checked = Child([str(args.haproxy), '-c', '-f', str(root / 'haproxy.cfg')], root, 'config-check')
        children.append(checked)
        if checked.process.wait(timeout=10) != 0:
            raise ValueError('HAProxy configuration rejected')
        checked.stop()
        children.clear()
        verify_rules(args.bound_rules, rules)
        agent = Child([str(args.agent), '--config', str(root / 'agent.conf')], root, 'spoa')
        children.append(agent)
        wait_port(spoa, children)
        verify_rules(args.bound_rules, rules)
        host = Child([str(args.haproxy), '-db', '-f', str(root / 'haproxy.cfg')], root, 'haproxy')
        children.append(host)
        wait_port(front, children)
        result['identities'] = [process_pin(agent, args.agent, args.agent_sha256),
                                process_pin(host, args.haproxy, args.haproxy_sha256)]
        result['agent_generations'] = [result['identities'][0]]
        result['recoveries'] = []
        result['library_before'] = {child.label: library_pin(child, args) for child in children}
        result['sockets_before'] = {child.label: owned_sockets(child) for child in children}
        monitor = Monitor(children)
        for case in ('allow', 'p1', 'p2'):
            result['probes'].append(probe(root, front, origin, case))
        if extended:
            def append_recovery(observed, before):
                result['probes'].append(observed)
                followup = probe(root, front, origin, 'allow')
                result['probes'].append(followup)
                after = process_pin(host, args.haproxy, args.haproxy_sha256)
                if before != after or after != result['identities'][1]:
                    raise ValueError('HAProxy generation changed across error/boundary recovery')
                result['recoveries'].append({'failure_id': observed['id'], 'allow_id': followup['id'],
                    'host_before': before, 'host_after': after})
            for case in ('p3', 'p4', *BOUNDARY_CASES):
                before = process_pin(host, args.haproxy, args.haproxy_sha256)
                observed = rejection_probe(root, front, origin, case) if case in MALFORMED_CASES else probe(root, front, origin, case)
                append_recovery(observed, before)
            before = process_pin(host, args.haproxy, args.haproxy_sha256)
            append_recovery(probe(root, front, origin, 'slow', abort=True), before)
            keepalive_ids = []
            keepalive_before = process_pin(host, args.haproxy, args.haproxy_sha256)
            with socket.create_connection(('127.0.0.1', front), timeout=5) as connection:
                for case in ('allow', 'p1', 'allow', 'p2', 'allow'):
                    observed = probe(root, front, origin, case, connection)
                    result['probes'].append(observed)
                    keepalive_ids.append(observed['id'])
            result['keepalive_alternation'] = True
            result['keepalive'] = {'ids': keepalive_ids, 'host_before': keepalive_before,
                'host_after': process_pin(host, args.haproxy, args.haproxy_sha256)}
            with ThreadPoolExecutor(max_workers=4) as executor:
                result['probes'].extend(executor.map(lambda _: probe(root, front, origin, 'parallel'), range(4)))
            verify_parallel(origin.parallel)
            result['parallel'] = dict(origin.parallel)
            text, result['boundary_receipts'] = await_boundary_receipts(root, result['probes'])
            result['p3_receipts'] = verify_p3_receipt(text, result['probes'])
            if result['p3_receipts']['status'] == 'failed':
                result['gates']['G4'] = 'failed'
                raise ValueError('P3 native renderer returned fallback 500; deny prerequisite failed')
            result['p4_receipts'] = verify_p4_receipt(text, result['probes'])
            result['resource_segments'] = {'before_agent_stop': monitor.finish()}
            monitor = Monitor([host])
            before = process_pin(host, args.haproxy, args.haproxy_sha256)
            agent.stop()
            children.remove(agent)
            if (root / 'mrc.sock').exists() or (root / 'mrc.sock').is_symlink():
                raise ValueError('old agent MRC1 listener survived controlled stop')
            result['agent_stop'] = {'identity': result['agent_generations'][0],
                'exit_status': agent.process.poll(), 'uds_removed': True}
            # No engine is running for this exact unavailable request. Decisions
            # remain append-only and are reconciled against the final closed set.
            unavailable = rejection_probe(root, front, origin, 'agent-unavailable')
            if any(value.get('request_id') == unavailable['engine_id']
                for value in read_events(root / 'decision.jsonl')):
                raise ValueError('unavailable agent produced a spurious engine decision')
            verify_rules(args.bound_rules, rules)
            agent = Child([str(args.agent), '--config', str(root / 'agent.conf')], root, 'spoa-generation-2')
            children.append(agent)
            wait_port(spoa, children)
            verify_rules(args.bound_rules, rules)
            identity = process_pin(agent, args.agent, args.agent_sha256)
            if (identity['pid'], identity['start_token']) == \
                (result['agent_generations'][0]['pid'], result['agent_generations'][0]['start_token']):
                raise ValueError('controlled agent restart reused original generation')
            library_pin(agent, args)
            result['agent_generations'].append(identity)
            result['resource_segments']['during_agent_unavailable'] = monitor.finish()
            monitor = Monitor(children)
            append_recovery(unavailable, before)
        final_resources = monitor.finish()
        if extended:
            result['resource_segments']['after_agent_restart'] = final_resources
            result['resources'] = result['resource_segments']['before_agent_stop']
        else:
            result['resources'] = final_resources
        monitor = None
        result['library_after'] = {child.label: library_pin(child, args) for child in children}
        result['sockets_after'] = {child.label: owned_sockets(child) for child in children}
        verify_rules(args.bound_rules, rules)
        if result['agent_generations'][-1] != process_pin(agent, args.agent, args.agent_sha256) or \
            result['identities'][1] != process_pin(host, args.haproxy, args.haproxy_sha256):
            raise ValueError('host or agent restarted during probes')
        for key in ('G2', 'G3'):
            result['gates'][key] = 'passed_prerequisite'
        result['result'] = 'BLOCKED'
        result['passed'] = True
        result['limitations'] = ['G1 requires fresh source/build identity evidence',
            'G8 complete regression suite is external']
        if not extended:
            result['limitations'].append('G4/G5/G6/G7 complete campaign belongs to first start')
        if result.get('p4_receipts', {}).get('status') == 'blocked':
            result['limitations'].append('G4 native P4 receipt lacks engine rule correlation')
    except Exception as exc:
        result['error'] = type(exc).__name__ + ': ' + str(exc)
    finally:
        errors = []
        if monitor:
            try:
                monitor.finish()
            except Exception as exc:
                errors.append('monitor: ' + str(exc))
        for child in reversed(children):
            try:
                child.stop()
            except Exception as exc:
                errors.append(child.label + ': ' + str(exc))
        if origin:
            try:
                try:
                    origin.close()
                finally:
                    result['backend_final'] = origin.snapshot()
                verify_final_backend(result['backend_final'], result['probes'])
            except Exception as exc:
                errors.append('upstream: ' + str(exc))
        if (root / 'mrc.sock').exists() or (root / 'mrc.sock').is_symlink():
            errors.append('MRC1 socket survived owner shutdown')
        if rules is not None:
            try:
                verify_rules(args.bound_rules, rules)
            except Exception as exc:
                errors.append('rules binding: ' + str(exc))
            finally:
                rules.close()
        if result['passed']:
            try:
                records = read_events(root / 'decision.jsonl')
                verify_final_decisions(records, result['probes'])
                result['final_decision_count'] = len(records)
                text = private_read(root / 'haproxy.log', MAX_FILE)
                result['host_mappings'] = verify_mappings(text, result['probes'])
                final_p3 = verify_p3_receipt(text, result['probes'])
                if 'p3_receipts' in result and final_p3 != result['p3_receipts']:
                    raise ValueError('final P3 receipts changed after probes')
                result['p3_receipts'] = final_p3
                if final_p3['status'] == 'failed':
                    result['gates']['G4'] = 'failed'
                    raise ValueError('final P3 deny prerequisite failed')
                final_p4 = verify_p4_receipt(text, result['probes'])
                if 'p4_receipts' in result and final_p4 != result['p4_receipts']:
                    raise ValueError('final P4 receipts changed after probes')
                result['p4_receipts'] = final_p4
                for observed in result['probes']:
                    verify_request_mapping(text, observed)
                if extended:
                    verify_extended_evidence(result, text)
                    for key in ('G4', 'G5', 'G6', 'G7'):
                        result['gates'][key] = 'passed_prerequisite'
            except Exception as exc:
                errors.append('host correlation: ' + str(exc))
        invalidate_cleanup(result, errors)
        if not errors:
            result['gates']['G9'] = 'passed_prerequisite'
        write_json(root / 'result.json', result)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('haproxy', 'agent', 'rules', 'library'):
        parser.add_argument('--' + name, required=True)
        parser.add_argument('--' + name + '-sha256', required=True)
    parser.add_argument('--root', required=True)
    args = parser.parse_args(argv)
    args.root = safe_path(args.root)
    validate_runtime_root(args.root)
    args.haproxy = pinned(args.haproxy, args.haproxy_sha256, 128 * 1024 * 1024)
    args.agent = pinned(args.agent, args.agent_sha256, 128 * 1024 * 1024)
    args.rules = safe_path(args.rules)
    args.library = pinned(args.library, args.library_sha256, 128 * 1024 * 1024)
    if args.rules_sha256 != RULES_SHA256:
        raise ValueError('rules must equal the reviewed self-contained SPOP vector')
    if not re.fullmatch('[0-9a-f]{64}', args.library_sha256):
        raise ValueError('library SHA256 pin required')
    previous_umask = os.umask(0o077)
    args.bound_rules = None
    try:
        args.bound_rules = BoundRules(args.rules, args.rules_sha256)
        starts = []
        for number in range(3):
            starts.append(run_start(args, args.root / f'start-{number + 1}', number == 0))
            if not starts[-1]['passed']:
                break
        identities = [(value['identities'][0]['pid'], value['identities'][0]['start_token'],
                       value['identities'][1]['pid'], value['identities'][1]['start_token'])
                      for value in starts if 'identities' in value]
        ok = len(starts) == 3 and all(value['passed'] for value in starts) and len(set(identities)) == 3
        outcome = {'profile': 'haproxy-spoe-spop-response-companion',
                   'catalog_acceptance': False, 'result': 'BLOCKED' if ok else 'FAIL',
                   'starts': starts, 'three_distinct_starts': ok,
                   'runner_sha256': hashlib.sha256(bound_input(Path(__file__), 128 * 1024)).hexdigest(),
                   'rules_sha256': args.rules_sha256, 'library_sha256': args.library_sha256}
        try:
            args.bound_rules.verify()
        except Exception as exc:
            outcome.update(result='FAIL', three_distinct_starts=False,
                           error='rules binding: ' + str(exc))
            ok = False
        write_json(args.root / 'qualification.json', outcome)
        return 77 if ok else 1
    finally:
        if args.bound_rules is not None:
            args.bound_rules.close()
        os.umask(previous_umask)


if __name__ == '__main__':
    raise SystemExit(main())
