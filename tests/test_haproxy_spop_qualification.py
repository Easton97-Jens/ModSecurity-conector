"""Negative acceptance tests for SPOP hosted qualification prerequisites."""

from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stderr
import hashlib
import copy
import http.client
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import socket
import struct
import threading
import time
import unittest
from unittest.mock import patch, Mock

SOURCE = Path(__file__).resolve().parents[1] / 'connectors/haproxy/harness/haproxy_spop_qualification.py'
SPEC = importlib.util.spec_from_file_location('spop_qualification', SOURCE)
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)
STORAGE = '/var/tmp/codex/ModSecurity-conector/runs'


def request_record(case='allow', token='haproxy-htx-1'):
    value = {key: '' for key in runner.RECORD_FIELDS}
    value.update(timestamp=100, connector='haproxy', mode='block', runtime_mode='production',
                 variant='spop-qualification', case='qualification', request_id=token,
                 transaction_id=token, phase=2, rule_id=0, disruptive=False,
                 live_executed=True, modsecurity_processed=True, request_headers_seen=True,
                 request_body_seen=True, response_headers_seen=False, response_body_seen=False,
                 expected_status=0, intervention_status=200, http_status=200,
                 anomaly_score=0, redirect_present=False, decision='pass',
                 reason_code='modsecurity_allow', reason='modsecurity_allow')
    if case in {'p1', 'p2'}:
        value.update(phase=1 if case == 'p1' else 2, rule_id=1100100 if case == 'p1' else 1100101,
                     disruptive=True, decision='deny', intervention_status=403, http_status=403,
                     reason_code='modsecurity_disruptive_intervention', reason='modsecurity_disruptive_intervention')
    return value


def expected_probe(case='allow', token='spop-0000000000000000', engine=None):
    engine = engine or 'haproxy-htx-' + str(int(token.removeprefix('spop-'), 16) + 1)
    return {'id': token, 'engine_id': engine, 'case': case, 'begin': 99, 'end': 101,
            'status': 403 if case in {'p1', 'p2', 'p3'} else 200,
            'backend_requests': 0 if case in {'p1', 'p2'} else 1,
            'decision': request_record(case, engine)}


def host_line(probe):
    blocked = probe['case'] in {'p1', 'p2'}
    engine = probe['decision']
    return (f'qualification probe={probe["id"]} id={probe["engine_id"]} '
            f'status={403 if blocked else 200} action={"deny" if blocked else "pass"} '
            f'rule={engine["rule_id"]} phase={engine["phase"]} '
            f'error={engine["reason_code"]} backend={"fe_spop" if blocked else "be_app"} '
            f'server={"<NOSRV>" if blocked else "app"}\n')


class RulesBindingTests(unittest.TestCase):
    def test_private_copy_and_source_are_bound_for_every_generation(self):
        with tempfile.TemporaryDirectory(dir=STORAGE) as directory:
            root = Path(directory)
            source = root / 'input.conf'
            source.write_text(runner.RULES)
            with runner.BoundRules(source, runner.RULES_SHA256) as bound:
                private = bound.copy(root / 'private.conf')
                self.addCleanup(private.close)
                self.assertEqual(private.path.read_text(), runner.RULES)
                self.assertEqual(private.path.stat().st_mode & 0o777, 0o400)
                bound.verify()
                private.verify()

    def test_content_replacement_and_symlink_drift_fail(self):
        for change in ('content', 'replacement', 'symlink', 'private-content', 'private-replacement'):
            with self.subTest(change=change), tempfile.TemporaryDirectory(dir=STORAGE) as directory:
                root = Path(directory)
                source = root / 'input.conf'
                source.write_text(runner.RULES)
                with runner.BoundRules(source, runner.RULES_SHA256) as bound:
                    private = bound.copy(root / 'private.conf')
                    self.addCleanup(private.close)
                    target = private.path if change.startswith('private') else source
                    if change.endswith('content'):
                        target.chmod(0o600)
                        target.write_text(runner.RULES + '# drift\n')
                    else:
                        target.unlink()
                        if change == 'symlink':
                            target.symlink_to(private.path)
                        else:
                            target.write_text(runner.RULES)
                    with self.assertRaises((ValueError, OSError)):
                        bound.verify() if target == source else private.verify()

    def test_drift_between_starts_or_before_restart_is_rejected(self):
        for transition in ('between-starts', 'before-restart'):
            with self.subTest(transition=transition), tempfile.TemporaryDirectory(dir=STORAGE) as directory:
                root = Path(directory)
                source = root / 'input.conf'
                source.write_text(runner.RULES)
                with runner.BoundRules(source, runner.RULES_SHA256) as bound:
                    private = bound.copy(root / 'first.conf')
                    self.addCleanup(private.close)
                    bound.verify()
                    private.verify()
                    source.write_text(runner.RULES.replace('SecRuleEngine On', 'SecRuleEngine Off'))
                    with self.assertRaises(ValueError):
                        if transition == 'between-starts':
                            bound.copy(root / 'second.conf')
                        else:
                            runner.verify_rules(bound, private)

    def test_campaign_reports_fail_when_rules_drift_between_starts(self):
        with tempfile.TemporaryDirectory(dir=STORAGE) as directory:
            root = Path(directory)
            source = root / 'input.conf'
            source.write_text(runner.RULES)
            original_start = runner.run_start
            def start(args, target, extended):
                if extended:
                    source.write_text(runner.RULES + '# changed after first start\n')
                    return {'passed': True, 'identities': [
                        {'pid': 1, 'start_token': 'one'}, {'pid': 2, 'start_token': 'two'}]}
                return original_start(args, target, extended)
            argv = ['--root', str(root)]
            for name in ('haproxy', 'agent', 'library'):
                argv.extend(['--' + name, '/unused', '--' + name + '-sha256', '0' * 64])
            argv.extend(['--rules', str(source), '--rules-sha256', runner.RULES_SHA256])
            with patch.object(runner, 'pinned', return_value=Path('/unused')), \
                patch.object(runner, 'validate_runtime_root'), \
                patch.object(runner, 'run_start', side_effect=start):
                self.assertEqual(runner.main(argv), 1)
            outcome = json.loads((root / 'qualification.json').read_text())
            self.assertEqual(outcome['result'], 'FAIL')
            self.assertFalse(outcome['starts'][1]['passed'])
            self.assertIn('rules', outcome['starts'][1]['error'])

    def test_restart_drift_fails_before_second_agent_is_launched(self):
        with tempfile.TemporaryDirectory(dir=STORAGE) as directory:
            root = Path(directory)
            source = root / 'input.conf'
            source.write_text(runner.RULES)
            with runner.BoundRules(source, runner.RULES_SHA256) as bound:
                args = Mock(bound_rules=bound, rules=source, agent=Path('/agent'),
                    haproxy=Path('/haproxy'), agent_sha256='0' * 64, haproxy_sha256='0' * 64)
                agent = Mock(label='spoa')
                agent.process.poll.return_value = 0
                agent.stop.side_effect = lambda: source.write_text(runner.RULES + '# restart drift\n')
                host = Mock(label='haproxy')
                checked = Mock()
                checked.process.wait.return_value = 0
                children = Mock(side_effect=[checked, agent, host])
                origin = Mock(server_port=3, parallel={})
                origin.snapshot.return_value = {}
                counter = iter(range(100))
                def observed(*_, **kwargs):
                    return {'id': str(next(counter)), 'engine_id': '-', 'case': 'allow'}
                patches = {
                    'Upstream': Mock(return_value=origin), 'free_port': Mock(side_effect=[1, 2]),
                    'Child': children, 'wait_port': Mock(), 'process_pin': Mock(return_value={'pid': 1, 'start_token': 'one'}),
                    'library_pin': Mock(return_value=[]), 'owned_sockets': Mock(return_value=[]),
                    'Monitor': Mock(return_value=Mock(finish=Mock(return_value={}))), 'probe': Mock(side_effect=observed),
                    'rejection_probe': Mock(side_effect=observed), 'verify_parallel': Mock(),
                    'await_boundary_receipts': Mock(return_value=('', {})),
                    'verify_p3_receipt': Mock(return_value={'status': 'passed_prerequisite'}),
                    'verify_p4_receipt': Mock(return_value={'status': 'passed_prerequisite'}),
                    'read_events': Mock(return_value=[]), 'verify_final_backend': Mock(),
                }
                with patch.multiple(runner, **patches), patch.object(runner.socket, 'create_connection'):
                    result = runner.run_start(args, root / 'start', True)
                self.assertEqual(result['result'], 'FAIL')
                self.assertFalse(result['passed'])
                self.assertIn('rules', result['error'])
                self.assertEqual(children.call_count, 3)


class CorrelationTests(unittest.TestCase):
    def test_static_validated_413_precedes_403_fallback(self):
        text = runner.configuration(Path('/var/tmp/codex/ModSecurity-conector/runs/q'),
            Path('/rules'), 1, 2, 3)['haproxy.cfg']
        self.assertIn('deny status 413 if { var(txn.modsec.blocked) -m bool } { var(txn.modsec.status) -m int 413 } { var(txn.modsec.phase) -m int 2 } { var(txn.modsec.rule_id) -m int 0 }', text)
        self.assertLess(text.index('deny status 413'), text.index('deny status 403'))
        self.assertNotIn('deny status %[', text)

    def test_request_boundary_vectors_are_closed_and_hashed(self):
        for case, length, backend, status in (('request-empty', 0, 1, 200),
            ('request-exact', 32768, 1, 200), ('request-over', 32769, 0, 413),
            ('chunked-allow', 4, 1, 200), ('chunked-p2', 21, 0, 403)):
            vector = runner.case_contract(case)
            self.assertEqual((len(vector['body']), vector['backend'], vector['status']), (length, backend, status))
            self.assertEqual(vector['body_sha256'], hashlib.sha256(vector['body']).hexdigest())
        with self.assertRaises(ValueError):
            runner.case_contract('unknown')

    def test_request_413_decision_and_host_fields_are_exact(self):
        value = request_record()
        value.update(modsecurity_processed=False, disruptive=True, decision='deny',
            http_status=413, intervention_status=413, reason='modsecurity_not_processed',
            reason_code='modsecurity_not_processed')
        runner.verify_request([value], value['request_id'], 'request-over', 99, 101, 0)
        for key, replacement in (('modsecurity_processed', True), ('http_status', 403),
            ('intervention_status', 403), ('rule_id', 1), ('phase', 1),
            ('reason_code', 'modsecurity_allow'), ('request_body_seen', False), ('disruptive', False)):
            with self.subTest(key=key), self.assertRaises(ValueError):
                runner.verify_request([dict(value, **{key: replacement})], value['request_id'], 'request-over', 99, 101, 0)

    def test_no_engine_decision_for_unavailable_and_parser_reject(self):
        for case in ('agent-unavailable', 'invalid-cl', 'invalid-te'):
            probe = dict(expected_probe(case), decision=None)
            runner.verify_final_decisions([], [probe])
            with self.assertRaises(ValueError):
                runner.verify_final_decisions([request_record(token=probe['engine_id'])], [probe])

    def test_pass_500_cannot_hide_behind_valid_p3_deny_receipt(self):
        probe = expected_probe('p3', runner.token(), 'haproxy-htx-7')
        receipt = ('modsecurity-htx: response-companion phase-3 intervention; '
                   'transaction_id=haproxy-htx-7 phase=3 rule_id=1100201 requested=deny '
                   'requested_status=403 host_action=deny host_status=403\n')
        for statuses in ({'http_status': 500, 'intervention_status': 500},
                         {'http_status': 500}, {'intervention_status': 500}, {'http_status': True},
                         {'expected_status': 500}):
            decision = dict(probe['decision'], **statuses)
            bad_probe = dict(probe, decision=decision)
            with self.assertRaises(ValueError):
                runner.verify_request([decision], probe['engine_id'], 'p3', 99, 101, 1)
            with self.assertRaises(ValueError):
                runner.verify_request_mapping(host_line(bad_probe).replace('status=200', 'status=500'), bad_probe)
            with self.assertRaises(ValueError):
                runner.verify_p3_receipt(receipt, [bad_probe])

    def test_p3_response_deny_does_not_change_allowed_request_mapping(self):
        probe = expected_probe('p3', runner.token(), 'haproxy-htx-7')
        request_log = host_line(probe)
        receipt = ('modsecurity-htx: response-companion phase-3 intervention; '
                   'transaction_id=haproxy-htx-7 phase=3 rule_id=1100201 requested=deny '
                   'requested_status=403 host_action=deny host_status=403\n')
        self.assertEqual(probe['status'], 403)
        self.assertEqual(probe['decision']['http_status'], 200)
        runner.verify_request_mapping(request_log, probe)
        self.assertEqual(runner.verify_p3_receipt(receipt, [probe])['status'], 'passed_prerequisite')
        for bad in ('', receipt.replace('host_status=403', 'host_status=200')):
            with self.assertRaises(ValueError):
                runner.verify_p3_receipt(bad, [probe])
        with self.assertRaises(ValueError):
            runner.verify_request_mapping(request_log.replace('status=200', 'status=403'), probe)

    def test_native_p3_receipt_requires_exact_engine_rule_action_and_client(self):
        probe = expected_probe('p3', runner.token(), 'haproxy-htx-11')
        line = ('[WARNING]  (13) : modsecurity-htx: response-companion phase-3 intervention; '
                'transaction_id=haproxy-htx-11 phase=3 rule_id=1100201 requested=deny '
                'requested_status=403 host_action=deny host_status=403\n')
        self.assertEqual(runner.verify_p3_receipt(line, [probe])['status'], 'passed_prerequisite')
        for bad in ('', line + line, line.replace('htx-11', 'htx-12'),
                    line.replace('phase=3', 'phase=4'), line.replace('1100201', '1100301'),
                    line.replace('requested=deny', 'requested=allow'),
                    line.replace('requested_status=403', 'requested_status=500'),
                    line.replace('host_action=deny', 'host_action=error'),
                    line.replace('host_status=403', 'host_status=500'),
                    line + line.replace('1100201', '1100301')):
            with self.assertRaises(ValueError):
                runner.verify_p3_receipt(bad, [probe])
        for bad_probe in (dict(probe, status=200), dict(probe, backend_requests=0),
                          dict(probe, backend_requests=2),
                          dict(probe, decision=dict(probe['decision'], decision='deny'))):
            with self.assertRaises(ValueError):
                runner.verify_p3_receipt(line, [bad_probe])
        with self.assertRaises(ValueError):
            runner.verify_p3_receipt(line, [])

    def test_p3_renderer_fallback_500_is_explicit_failure_and_contradictions_fail(self):
        probe = expected_probe('p3', runner.token(), 'haproxy-htx-11')
        line = ('modsecurity-htx: response-companion phase-3 intervention; '
                'transaction_id=haproxy-htx-11 phase=3 rule_id=1100201 requested=deny '
                'requested_status=403 host_action=error host_status=500\n')
        failed = runner.verify_p3_receipt(line, [dict(probe, status=500)])
        self.assertEqual(failed['status'], 'failed')
        self.assertEqual(failed['receipts'][0]['reason'], 'native_renderer_fallback_500')
        with self.assertRaises(ValueError):
            runner.verify_p3_receipt(line, [probe])
        with self.assertRaises(ValueError):
            runner.verify_p3_receipt(line.replace('host_action=error', 'host_action=deny'),
                                     [dict(probe, status=500)])

    def test_probe_metadata_maps_to_host_engine_id_with_closed_final_set(self):
        probes = [expected_probe(), expected_probe('p2', runner.token(), 'haproxy-htx-2')]
        text = ''.join(host_line(probe) for probe in probes)
        records = runner.verify_mappings(text, probes)
        self.assertEqual(records[probes[0]['id']]['engine_id'], 'haproxy-htx-1')
        for bad in (text + host_line(probes[0]), text.replace('id=haproxy-htx-2', 'id=haproxy-htx-1'),
                    text + host_line(expected_probe(token=runner.token(), engine='haproxy-htx-3')),
                    text.replace('id=haproxy-htx-1', 'id=' + probes[0]['id']), text.rstrip('\n')):
            with self.assertRaises(ValueError):
                runner.verify_mappings(bad, probes)

    def test_counter_reuse_is_scoped_to_distinct_starts(self):
        first = expected_probe(token=runner.token(), engine='haproxy-htx-1')
        second = expected_probe(token=runner.token(), engine='haproxy-htx-1')
        runner.verify_mappings(host_line(first), [first])
        runner.verify_mappings(host_line(second), [second])
        with self.assertRaises(ValueError):
            runner.verify_mappings(host_line(first) + host_line(second), [first, second])

    def test_client_id_is_never_accepted_as_engine_ownership(self):
        probe = expected_probe()
        record = request_record(token=probe['id'])
        with self.assertRaises(ValueError):
            runner.verify_request([record], probe['id'], 'allow', 99, 101, 1)

    def test_native_p4_exact_rule_requires_bound_engine_id(self):
        probe = expected_probe('p4', runner.token(), 'haproxy-htx-11')
        line = ('[WARNING]  (13) : modsecurity-htx: response-companion phase-4 intervention; '
                'transaction_id=haproxy-htx-11 rule_id=1100301 requested=deny host_action=log_only\n')
        self.assertEqual(runner.verify_p4_receipt(line, [probe])['status'], 'passed_prerequisite')
        missing_rule = line.replace('rule_id=1100301', 'rule_id=')
        self.assertEqual(runner.verify_p4_receipt(missing_rule, [probe])['status'], 'blocked')
        for bad in (line.replace('htx-11', 'htx-12'), missing_rule.replace('htx-11', 'htx-12')):
            with self.assertRaises(ValueError):
                runner.verify_p4_receipt(bad, [probe])

    def test_fixture_has_host_generated_ownership_and_separate_metadata(self):
        config = runner.configuration(Path('/var/tmp/codex/ModSecurity-conector/runs/fixture'),
                                      Path('/var/tmp/codex/ModSecurity-conector/runs/rules'), 20001, 20002, 20003)
        self.assertIn('unique-id-format haproxy-htx-%rt', config['haproxy.cfg'])
        self.assertNotIn('unique-id-format %[req.hdr', config['haproxy.cfg'])
        self.assertIn('probe=%[var(txn.qualification_probe)] id=%ID', config['haproxy.cfg'])
        self.assertIn('request_id=unique-id ', config['spoe.cfg'])

    def test_real_native_p4_format_is_explicitly_blocked_for_correlation(self):
        probe = expected_probe('p4', 'spop-e8f4bf8d9fd7a4d3')
        probe.pop('engine_id')  # Historical run has no trustworthy ID mapping.
        line = ('[WARNING]  (13) : modsecurity-htx: response-companion phase-4 intervention; '
                'transaction_id=haproxy-htx-11 rule_id= requested=deny host_action=log_only\n')
        result = runner.verify_p4_receipt(line, [probe])
        self.assertEqual(result['status'], 'blocked')
        self.assertEqual(result['reason'], 'native_internal_id_and_missing_rule')
        self.assertEqual(result['expected_probe_tokens'], [probe['id']])
        self.assertEqual(result['observed_receipts'][0]['transaction_id'], 'haproxy-htx-11')
        for bad in (line + line, line + line.replace('htx-11', 'htx-12'),
                    line.replace('host_action=log_only', 'host_action=allow'),
                    line.replace('requested=deny', 'requested=allow')):
            with self.assertRaises(ValueError):
                runner.verify_p4_receipt(bad, [probe])
        with self.assertRaises(ValueError):
            runner.verify_p4_receipt(line, [])

    def test_final_decisions_reject_late_duplicate_unknown_and_changed_record(self):
        probe = expected_probe()
        record = probe['decision']
        runner.verify_final_decisions([record], [probe])
        for records in ([record, record], [dict(record, request_id=runner.token())],
                        [dict(record, audit_log_path='changed')], [dict(record, body='secret')]):
            with self.assertRaises(ValueError):
                runner.verify_final_decisions(records, [probe])

    def test_final_p4_receipt_rejects_late_duplicate_and_wrong_rule(self):
        probe = expected_probe('p4')
        line = ('modsecurity-htx: response-companion phase-4 intervention; transaction_id='
                + probe['engine_id'] + ' rule_id=1100301 requested=deny host_action=log_only\n')
        runner.verify_p4_receipt(line, [probe])
        for text in ('', line + line, line.replace('1100301', '1100201'),
                     line + line.replace('1100301', '1100201'),
                     line + line.replace('host_action=log_only', 'host_action=allow'),
                     line + line.replace('requested=deny', 'requested=allow'),
                     line + line.replace(probe['engine_id'], 'haproxy-htx-99'),
                     line.rstrip('\n') + ' ' + line,
                     line.replace(' host_action=log_only', ''),
                     line.replace(probe['engine_id'], 'haproxy-htx-99')):
            with self.assertRaises(ValueError):
                runner.verify_p4_receipt(text, [probe])
        with self.assertRaises(ValueError):
            runner.verify_p4_receipt(line, [])

    def test_allow_and_request_phase_blocks(self):
        for case in ('allow', 'p1', 'p2'):
            value = request_record(case)
            self.assertEqual(runner.verify_request([value], value['request_id'], case, 99, 101,
                             1 if case == 'allow' else 0), value)

    def test_correlated_metadata_rejects_false_claims(self):
        for field, bad in (('transaction_id', 'different'), ('phase', 3), ('rule_id', 1),
                           ('modsecurity_processed', False), ('live_executed', 1),
                           ('request_headers_seen', False), ('response_body_seen', True),
                           ('reason', 'payload'), ('timestamp', 1), ('http_status', True),
                           ('variant', 'htx'), ('decision', 'allow')):
            with self.subTest(field=field):
                value = request_record('p2')
                value[field] = bad
                with self.assertRaises(ValueError):
                    runner.verify_request([value], value['request_id'], 'p2', 99, 101, 0)

    def test_duplicate_missing_and_payload_records_rejected(self):
        value = request_record()
        for records in ([], [value, value], [dict(value, body='secret')], [None]):
            with self.assertRaises(ValueError):
                runner.verify_request(records, value['request_id'], 'allow', 99, 101, 1)

    def test_backend_leak_and_missing_allow_dispatch_rejected(self):
        for case, counts in (('p1', (1, True)), ('p2', (1, True)), ('allow', (0, True))):
            for count in counts:
                with self.assertRaises(ValueError):
                    runner.verify_request([request_record(case)], 'haproxy-htx-1', case, 99, 101, count)

    def test_host_outcome_requires_exact_rule_phase_action_and_no_server(self):
        token = 'spop-0000000000000000'
        line = f'qualification probe={token} id=haproxy-htx-1 status=403 action=deny rule=1100101 phase=2 error=modsecurity_disruptive_intervention backend=fe_spop server=<NOSRV>\n'
        runner.verify_host(line, token, 'haproxy-htx-1', 403, 'deny', 1100101, 2)
        for bad in ('', line + line, line.replace('phase=2', 'phase=1'),
                    line.replace('server=<NOSRV>', 'server=app'), line.replace('status=403', 'status=200'),
                    line.replace('error=modsecurity_disruptive_intervention', 'error=modsecurity_allow')):
            with self.assertRaises(ValueError):
                runner.verify_host(bad, token, 'haproxy-htx-1', 403, 'deny', 1100101, 2)


class BoundaryEvidenceTests(unittest.TestCase):
    @staticmethod
    def malformed_socket(payload, *, normal=False, case='invalid-cl'):
        client, peer = socket.socketpair()
        try:
            peer.sendall(payload)
            peer.shutdown(socket.SHUT_WR)
            return runner.client_response(client) if normal else runner.malformed_client_response(client, case)
        finally:
            client.close()
            peer.close()

    def test_real_malformed_zero_close_and_complete_400_only(self):
        zero = self.malformed_socket(b'')
        self.assertIsNone(zero['status'])
        self.assertEqual((zero['termination'], zero['eos'], zero['body_bytes']), ('zero_close', False, 0))
        full = self.malformed_socket(b'HTTP/1.1 400 Bad Request\r\nContent-Length: 3\r\nConnection: close\r\n\r\nbad')
        self.assertEqual((full['status'], full['termination'], full['eos']), (400, 'eof', True))
        for case in runner.MALFORMED_CASES:
            runner.verify_client_response(case, full)
            runner.verify_client_response(case, zero)
        with self.assertRaises(ValueError):
            self.malformed_socket(b'', normal=True)
        for case in ('allow', 'agent-unavailable', 'p1'):
            with self.assertRaises(ValueError):
                runner.verify_client_response(case, zero)
        for key, bad in (('status', 400), ('declared_bytes', 1), ('body_bytes', True),
                        ('body_sha256', '0' * 64), ('eos', True), ('elapsed_seconds', 6),
                        ('elapsed_seconds', float('nan'))):
            with self.subTest(key=key), self.assertRaises(ValueError):
                runner.verify_client_response('invalid-cl', dict(zero, **{key: bad}))

    def test_real_malformed_partial_wrong_status_and_ambiguous_framing_rejected(self):
        header = b'HTTP/1.1 400 Bad Request\r\nContent-Length: 3\r\n\r\n'
        payloads = (b'x', b'HTTP/1.1 ', header[:-1], header, header + b'ba', header + b'badextra',
            header.replace(b'400', b'200') + b'bad',
            header.replace(b'Content-Length: 3', b'Content-Length: -1'),
            header.replace(b'Content-Length: 3', b'Content-Length: 3\r\nContent-Length: 3') + b'bad',
            header.replace(b'Content-Length: 3', b'Transfer-Encoding: chunked') + b'0\r\n\r\n',
            header.replace(b'Content-Length: 3', b'Content-Length: 3\r\nTransfer-Encoding: chunked') + b'bad')
        for payload in payloads:
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                self.malformed_socket(payload)

    def test_real_malformed_socket_timeout_and_tcp_reset_rejected(self):
        client, peer = socket.socketpair()
        clock = time.monotonic
        calls = 0
        def almost_expired():
            nonlocal calls
            calls += 1
            return clock() + (5.98 if calls > 2 else 0)
        try:
            with patch.object(runner.time, 'monotonic', side_effect=almost_expired), self.assertRaises(TimeoutError):
                runner.malformed_client_response(client, 'invalid-cl')
        finally:
            client.close()
            peer.close()
        with socket.socket() as listener:
            listener.bind(('127.0.0.1', 0))
            listener.listen(1)
            with socket.create_connection(listener.getsockname(), timeout=1) as client:
                peer, _ = listener.accept()
                peer.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))
                peer.close()
                with self.assertRaises(ConnectionResetError):
                    runner.malformed_client_response(client, 'invalid-cl')

    @staticmethod
    def response(case, *, truncated=False, abort=False):
        vector = runner.case_contract(case)
        body = vector['response']
        received = body[:0] if truncated or abort else body
        return {'status': vector['status'], 'declared_bytes': len(body) if vector['status'] == 200 else 0,
            'body_bytes': len(received) if vector['status'] == 200 else 0,
            'body_sha256': hashlib.sha256(received if vector['status'] == 200 else b'').hexdigest(),
            'eos': not truncated and not abort, 'termination': 'client_abort' if abort else 'eof',
            'elapsed_seconds': 2.5 if case == 'slow' and not abort else .1}

    def test_client_empty_and_exact_response_lengths_hashes(self):
        for case in ('allow', 'p4', 'response-empty', 'response-exact'):
            value = self.response(case)
            runner.verify_client_response(case, value)
            for key, bad in (('body_sha256', '0' * 64), ('body_bytes', True),
                ('declared_bytes', value['declared_bytes'] + 1), ('eos', False),
                ('termination', 'timeout'), ('elapsed_seconds', float('nan'))):
                with self.subTest(case=case, key=key), self.assertRaises(ValueError):
                    runner.verify_client_response(case, dict(value, **{key: bad}))

    def test_incomplete_response_requires_eof_not_timeout_or_success(self):
        for case in ('limit', 'slow'):
            value = self.response(case, truncated=True)
            runner.verify_client_response(case, value)
            for key, bad in (('termination', 'timeout'), ('termination', 'reset'),
                ('eos', True), ('status', 503), ('declared_bytes', 0),
                ('body_sha256', '0' * 64), ('elapsed_seconds', 6)):
                with self.subTest(case=case, key=key), self.assertRaises(ValueError):
                    runner.verify_client_response(case, dict(value, **{key: bad}))
            if case == 'slow':
                with self.assertRaises(ValueError):
                    runner.verify_client_response(case, dict(value, elapsed_seconds=.1))

    def test_response_limit_zero_eof_requires_exact_boundary_receipt_and_recovery(self):
        client, peer = socket.socketpair()
        try:
            peer.shutdown(socket.SHUT_WR)
            value = runner.response_limit_client_response(client)
        finally:
            client.close()
            peer.close()
        self.assertEqual((value['status'], value['termination'], value['body_bytes']),
                         (None, 'zero_close', 0))
        result, text = self.campaign()
        limit = next(probe for probe in result['probes'] if probe['case'] == 'limit')
        limit.update(response=value, status=None)
        runner.verify_extended_evidence(result, text)
        marker = f'modsecurity-htx: fail-closed postcommit response-companion body; transaction_id={limit["engine_id"]}\n'
        for bad_text in (text.replace(marker, ''), text + marker,
                         text.replace(marker, marker.replace('response-companion body', 'response body')),
                         text.replace(marker, marker.replace(limit['engine_id'], 'haproxy-htx-999'))):
            with self.subTest(text=bad_text), self.assertRaises(ValueError):
                runner.verify_extended_evidence(result, bad_text)
        for case in ('allow', 'response-empty', 'response-exact', 'slow'):
            with self.subTest(case=case), self.assertRaises(ValueError):
                runner.verify_client_response(case, value)
        for changes in ({'body_bytes': 1}, {'status': 413}, {'status': 500}, {'eos': True},
                        {'termination': 'timeout'}, {'termination': 'reset'}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                runner.verify_client_response('limit', dict(value, **changes))
        with self.assertRaises(ValueError):
            runner.verify_client_response('limit', self.response('limit'))
        recovery = next(item for item in result['recoveries'] if item['failure_id'] == limit['id'])
        recovery['host_after'] = dict(recovery['host_after'], start_token='restarted')
        with self.assertRaises(ValueError):
            runner.verify_extended_evidence(result, text)

    def test_response_limit_partial_headers_and_transport_failures_are_not_zero_eof(self):
        for payload in (b'x', b'HTTP/1.1 ', b'HTTP/1.1 200 OK\r\n', b'H' * 16385,
            b'HTTP/1.1 413 Payload Too Large\r\nContent-Length: 0\r\n\r\n',
            b'HTTP/1.1 500 Internal Server Error\r\nContent-Length: 0\r\n\r\n'):
            client, peer = socket.socketpair()
            try:
                peer.sendall(payload)
                peer.shutdown(socket.SHUT_WR)
                with self.subTest(payload=payload[:60]), self.assertRaises(ValueError):
                    runner.response_limit_client_response(client)
            finally:
                client.close()
                peer.close()
        for failure in (TimeoutError('timeout'), ConnectionResetError('reset')):
            connection = Mock()
            connection.recv.side_effect = failure
            with self.subTest(failure=failure), self.assertRaises(type(failure)):
                runner.response_limit_client_response(connection)

    def test_response_limit_requires_origin_eos_and_completed_write(self):
        probe = expected_probe('limit', runner.token(), 'haproxy-htx-53')
        vector = runner.case_contract('limit')
        receipt = {'token': probe['id'], 'connection': 21, 'method': 'POST',
            'route': 'limit', 'content_length': str(len(vector['body'])),
            'completed': True, 'body_bytes': len(vector['body']),
            'body_sha256': vector['body_sha256'], 'request_eos': True, 'error': False,
            'response_bytes': len(vector['response']), 'response_sha256': vector['response_sha256'],
            'response_eos': True, 'response_completed': True}
        snapshot = {'headers': [receipt], 'accepts': [{'connection': 21, 'queued': False}],
            'invalid_requests': 0, 'server_errors': 0, 'counts': {probe['id']: 1}}
        runner.verify_final_backend(snapshot, [probe])
        for field in ('response_eos', 'response_completed'):
            for value in (False, 1, None):
                bad = copy.deepcopy(snapshot)
                bad['headers'][0][field] = value
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    runner.verify_final_backend(bad, [probe])

    def test_actual_client_parser_rejects_socket_timeout_and_reset(self):
        class Socket:
            def __init__(self, payload, terminal=None):
                self.data = io.BytesIO(payload)
                self.terminal = terminal
            def settimeout(self, _value):
                pass
            def recv(self, size):
                result = self.data.read(size)
                if not result and self.terminal:
                    raise self.terminal
                return result
        header = b'HTTP/1.1 200 OK\r\nContent-Length: 2\r\nConnection: close\r\n\r\n'
        value = runner.client_response(Socket(header))
        self.assertEqual((value['termination'], value['eos'], value['body_bytes']), ('eof', False, 0))
        for error in (TimeoutError('timeout'), ConnectionResetError('reset')):
            with self.subTest(error=type(error).__name__), self.assertRaises(OSError):
                runner.client_response(Socket(header, error))
        for payload in (header.replace(b'Content-Length: 2', b'Content-Length: 2\r\nContent-Length: 2'),
            header.replace(b'Content-Length: 2', b'Content-Length: 2, 2'),
            header.replace(b'Content-Length: 2', b'Transfer-Encoding: chunked'), header + b'OKextra'):
            with self.assertRaises(ValueError):
                runner.client_response(Socket(payload))

    def test_exact_limit_and_slow_receipt_multiplicity(self):
        probes = [dict(expected_probe(case, runner.token(), f'haproxy-htx-{index}'), abort=False)
            for index, case in enumerate(('limit', 'slow'), 1)]
        text = ''.join(f'modsecurity-htx: fail-closed postcommit response-companion body; transaction_id={probe["engine_id"]}\n' for probe in probes)
        self.assertEqual(len(runner.verify_boundary_receipts(text, probes)), 2)
        for bad in (text + text.splitlines(True)[0], text.splitlines(True)[0],
            text.replace('haproxy-htx-2', 'haproxy-htx-9'), text.replace('response-companion body;', 'response body;')):
            with self.assertRaises(ValueError):
                runner.verify_boundary_receipts(bad, probes)

    def test_parser_and_agent_host_rejections_are_exact_and_finally_bound(self):
        ready = 'qualification probe=- id=- status=400 action=- rule=- phase=- error=- backend=fe_spop server=<NOSRV>\n'
        for case in ('invalid-cl', 'invalid-te', 'agent-unavailable'):
            identifier = runner.token()
            parser = case != 'agent-unavailable'
            line = ready if parser else f'qualification probe={identifier} id=haproxy-htx-3 status=503 action=- rule=- phase=- error=- backend=fe_spop server=<NOSRV>\n'
            text = ready + line
            key = 'parser-reject-1' if parser else identifier
            record = runner.host_records(text)[key]
            observed = dict(expected_probe(case, identifier, record['engine_id']),
                decision=None, backend_requests=0, status=400 if parser else 503,
                host_key=key, host_record=record)
            runner.verify_request_mapping(text, observed)
            runner.verify_mappings(text, [observed])
            for bad in (dict(observed, backend_requests=1), dict(observed, decision=request_record()),
                dict(observed, host_record=dict(record, server='app'))):
                with self.assertRaises(ValueError):
                    runner.verify_request_mapping(text, bad)
            with self.assertRaises(ValueError):
                runner.verify_mappings(text + ready, [observed])

    def test_truncated_request_requires_exact_client400_host503_and_allow_receipt(self):
        identifier = runner.token()
        line = f'qualification probe={identifier} id=haproxy-htx-41 status=503 action=- rule=- phase=- error=- backend=fe_spop server=<NOSRV>\n'
        record = runner.host_records(line)[identifier]
        observed = dict(expected_probe('truncated-request', identifier, 'haproxy-htx-41'),
            status=503, backend_requests=0, host_key=identifier, host_record=record,
            response=self.response('truncated-request'))
        runner.verify_request_mapping(line, observed)
        runner.verify_request_mapping(line, dict(observed,
            response=self.malformed_socket(b'', case='truncated-request')))
        runner.verify_final_decisions([observed['decision']], [observed])
        runner.verify_mappings(line, [observed])
        for changes in ({'status': 400}, {'status': 200}, {'backend_requests': 1},
            {'host_key': 'parser-reject-1'}, {'engine_id': 'haproxy-htx-42'},
            {'host_record': dict(record, status=400)}, {'host_record': dict(record, action='pass')},
            {'host_record': dict(record, server='app')},
            {'decision': None}, {'decision': dict(observed['decision'], phase=1)},
            {'decision': dict(observed['decision'], http_status=503)},
            {'decision': dict(observed['decision'], request_id='haproxy-htx-42')},
            {'response': dict(observed['response'], status=503)},
            {'response': dict(self.malformed_socket(b''), body_bytes=1)}):
            with self.subTest(changes=changes), self.assertRaises((ValueError, TypeError)):
                runner.verify_request_mapping(line, dict(observed, **changes))
        for records in ([], [observed['decision']] * 2,
                        [dict(observed['decision'], transaction_id='haproxy-htx-42')]):
            with self.assertRaises(ValueError):
                runner.verify_final_decisions(records, [observed])
        with self.assertRaises(ValueError):
            runner.verify_mappings(line + line, [observed])

    def test_truncated_zero_close_is_explicit_and_partial_timeout_reset_remain_fatal(self):
        value = self.malformed_socket(b'', case='truncated-request')
        self.assertEqual((value['status'], value['termination'], value['body_bytes']),
                         (None, 'zero_close', 0))
        for payload in (b'x', b'HTTP/1.1 ', b'HTTP/1.1 400 Bad Request\r\n',
            b'HTTP/1.1 400 Bad Request\r\nContent-Length: 1\r\n\r\n',
            b'HTTP/1.1 503 Service Unavailable\r\nContent-Length: 0\r\n\r\n'):
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                self.malformed_socket(payload, case='truncated-request')
        for failure in (TimeoutError('timeout'), ConnectionResetError('reset')):
            connection = Mock()
            connection.recv.side_effect = failure
            with self.subTest(failure=failure), self.assertRaises(type(failure)):
                runner.malformed_client_response(connection, 'truncated-request')

    def test_real_origin_empty_exact_and_chunked_request_hash_eos(self):
        for case in ('request-empty', 'request-exact', 'chunked-allow', 'response-empty', 'response-exact'):
            with self.subTest(case=case):
                origin = runner.Upstream()
                observed = expected_probe(case, runner.token())
                try:
                    with socket.create_connection(('127.0.0.1', origin.server_port), timeout=2) as connection:
                        connection.sendall(runner.wire(case, observed['id']))
                        response = runner.client_response(connection)
                    runner.verify_client_response(case, response)
                finally:
                    origin.close()
                snapshot = origin.snapshot()
                runner.verify_final_backend(snapshot, [observed])
                for key, bad in (('body_sha256', '0' * 64), ('request_eos', False),
                    ('body_bytes', 1 if case == 'request-empty' else 0),
                    ('response_eos', False), ('response_bytes', 999), ('response_sha256', '0' * 64)):
                    mutated = copy.deepcopy(snapshot)
                    mutated['headers'][0][key] = bad
                    with self.subTest(key=key), self.assertRaises(ValueError):
                        runner.verify_final_backend(mutated, [observed])

    def campaign(self):
        probes, recoveries, text = [], [], ''
        host = {'pid': 50, 'start_token': 'a', 'exe': '/host', 'exe_sha256': '1' * 64}
        for case, abort in [(case, False) for case in ('p3', 'p4', *runner.BOUNDARY_CASES)] + [('slow', True), ('agent-unavailable', False)]:
            index = len(probes) + 1
            observed = dict(expected_probe(case, runner.token(), f'haproxy-htx-{index}'),
                status=runner.case_contract(case)['status'], backend_requests=runner.case_contract(case)['backend'],
                abort=abort, response=self.response(case, truncated=case in {'limit', 'slow'} and not abort, abort=abort))
            if case in {'limit', 'slow'}:
                text += f'modsecurity-htx: fail-closed postcommit response-companion body; transaction_id={observed["engine_id"]}\n'
            followup = dict(expected_probe('allow', runner.token(), f'haproxy-htx-{index + 1}'),
                abort=False, response=self.response('allow'))
            probes.extend([observed, followup])
            recoveries.append({'failure_id': observed['id'], 'allow_id': followup['id'],
                'host_before': host, 'host_after': host})
        first = {'pid': 60, 'start_token': 'b', 'exe': '/agent', 'exe_sha256': '2' * 64}
        keep_ids = []
        for case in ('allow', 'p1', 'allow', 'p2', 'allow', 'parallel', 'parallel', 'parallel', 'parallel'):
            observed = dict(expected_probe(case, runner.token(), f'haproxy-htx-{len(probes) + 1}'),
                abort=False, response=self.response(case))
            probes.append(observed)
            if case != 'parallel':
                keep_ids.append(observed['id'])
        result = {'probes': probes, 'identities': [first, host], 'recoveries': recoveries,
            'parallel': {'seen': 4, 'peak': 4, 'barrier_passes': 4, 'errors': 0, 'inflight': 0},
            'p3_receipts': {'status': 'passed_prerequisite'}, 'p4_receipts': {'status': 'passed_prerequisite'},
            'boundary_receipts': runner.verify_boundary_receipts(text, probes),
            'agent_generations': [first, dict(first, pid=70, start_token='c')],
            'agent_stop': {'identity': first, 'exit_status': 0, 'uds_removed': True},
            'resource_segments': {'before_agent_stop': {}, 'during_agent_unavailable': {}, 'after_agent_restart': {}},
            'keepalive_alternation': True,
            'keepalive': {'ids': keep_ids, 'host_before': host, 'host_after': host}}
        for segment, identities in (
            ('before_agent_stop', {'spoa': first, 'haproxy': host}),
            ('during_agent_unavailable', {'haproxy': host}),
            ('after_agent_restart', {'spoa-generation-2': result['agent_generations'][1], 'haproxy': host})):
            samples = {label: {'pid': identity['pid'], 'start_token': identity['start_token'],
                'rss_bytes': 4096, 'fd': 10} for label, identity in identities.items()}
            result['resource_segments'][segment] = {stage: copy.deepcopy(samples) for stage in ('before', 'peak', 'after')}
        return result, text

    def test_late_abort_receipt_is_required_before_boundary_snapshot_freezes(self):
        result, text = self.campaign()
        aborted = next(probe for probe in result['probes'] if probe['case'] == 'slow' and probe['abort'])
        late = f'modsecurity-htx: fail-closed postcommit response-companion body; transaction_id={aborted["engine_id"]}\n'
        early = text.replace(late, '')
        with self.assertRaises(ValueError):
            runner.verify_boundary_receipts(early, result['probes'])
        with patch.object(runner, 'private_read', side_effect=[early, early + late[:-4], text]), \
             patch.object(runner.time, 'sleep') as sleep:
            frozen_text, receipts = runner.await_boundary_receipts(Path('/campaign'), result['probes'])
        self.assertEqual(frozen_text, text)
        self.assertIn(aborted['engine_id'], receipts)
        self.assertEqual(receipts, runner.verify_boundary_receipts(text, result['probes']))
        self.assertEqual(sleep.call_count, 2)
        with patch.object(runner, 'private_read', return_value=early), \
             patch.object(runner.time, 'monotonic', side_effect=[0, 0, 7]), \
             patch.object(runner.time, 'sleep'), self.assertRaisesRegex(ValueError, 'deadline'):
            runner.await_boundary_receipts(Path('/campaign'), result['probes'])
        for bad in (text + late, early + late.replace(aborted['engine_id'], 'haproxy-htx-999'),
                    early + late.replace('response-companion body', 'response body')):
            with self.subTest(text=bad), patch.object(runner, 'private_read', return_value=bad), \
                 self.assertRaises(ValueError):
                runner.await_boundary_receipts(Path('/campaign'), result['probes'])

    def test_only_complete_extended_evidence_qualifies(self):
        result, text = self.campaign()
        runner.verify_extended_evidence(result, text)
        mutations = (
            lambda item: item['probes'].pop(4),
            lambda item: item['recoveries'].pop(),
            lambda item: item['recoveries'].append(item['recoveries'][0]),
            lambda item: item['recoveries'][0].update(host_after=dict(item['identities'][1], pid=99)),
            lambda item: item['recoveries'][0].update(allow_id=item['recoveries'][1]['allow_id']),
            lambda item: item['agent_generations'].__setitem__(1, item['agent_generations'][0]),
            lambda item: item['agent_generations'][1].update(exe_sha256='3' * 64),
            lambda item: item['agent_stop'].update(exit_status=-9),
            lambda item: item['agent_stop'].update(uds_removed=False),
            lambda item: item.update(keepalive_alternation=False),
            lambda item: item['resource_segments'].pop('after_agent_restart'),
            lambda item: item['resource_segments']['during_agent_unavailable'].clear(),
            lambda item: item['resource_segments']['before_agent_stop']['peak']['haproxy'].update(fd=9),
            lambda item: item['resource_segments']['after_agent_restart']['after']['haproxy'].update(pid=99),
            lambda item: next(probe for probe in item['probes'] if probe['case'] == 'agent-unavailable').update(backend_requests=1),
            lambda item: item['p4_receipts'].update(status='blocked'),
            lambda item: item['parallel'].update(peak=1),
            lambda item: item['boundary_receipts'].clear(),
            lambda item: item['keepalive']['ids'].pop(),
            lambda item: item['keepalive']['ids'].reverse(),
            lambda item: item['keepalive'].update(host_after=dict(item['identities'][1], pid=99)),
            lambda item: item['probes'].pop())
        for index, mutate in enumerate(mutations):
            bad = copy.deepcopy(result)
            mutate(bad)
            with self.subTest(index=index), self.assertRaises((ValueError, KeyError)):
                runner.verify_extended_evidence(bad, text)

    def test_zero_close_preserves_parser_receipt_and_same_host_recovery_requirements(self):
        result, text = self.campaign()
        ready = 'qualification probe=- id=- status=400 action=- rule=- phase=- error=- backend=fe_spop server=<NOSRV>\n'
        host_text = ready
        for index, probe in enumerate(item for item in result['probes'] if item['case'] in runner.PARSER_REJECT_CASES):
            host_text += ready
            key = f'parser-reject-{index + 1}'
            record = runner.host_records(host_text)[key]
            probe.update(response=self.malformed_socket(b''), status=400, decision=None,
                         backend_requests=0, engine_id='-', host_key=key, host_record=record)
            runner.verify_request_mapping(host_text, probe)
            for changes in ({'backend_requests': 1}, {'decision': request_record()},
                            {'host_record': dict(record, status=200)}, {'host_record': dict(record, server='app')}):
                with self.subTest(changes=changes), self.assertRaises(ValueError):
                    runner.verify_request_mapping(host_text, dict(probe, **changes))
        runner.verify_extended_evidence(result, text)
        malformed = next(probe for probe in result['probes'] if probe['case'] in runner.MALFORMED_CASES)
        recovery = next(item for item in result['recoveries'] if item['failure_id'] == malformed['id'])
        recovery['host_after'] = dict(recovery['host_after'], pid=99)
        with self.assertRaises(ValueError):
            runner.verify_extended_evidence(result, text)

    def test_truncated_request_requires_immediate_same_process_recovery(self):
        for mutation in ('missing', 'duplicate', 'restart', 'wrong-allow'):
            result, text = self.campaign()
            truncated = next(probe for probe in result['probes'] if probe['case'] == 'truncated-request')
            recovery = next(item for item in result['recoveries'] if item['failure_id'] == truncated['id'])
            if mutation == 'missing':
                result['recoveries'].remove(recovery)
            elif mutation == 'duplicate':
                result['recoveries'].append(copy.deepcopy(recovery))
            elif mutation == 'restart':
                recovery['host_after'] = dict(recovery['host_after'], start_token='new')
            else:
                recovery['allow_id'] = result['recoveries'][0]['allow_id']
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                runner.verify_extended_evidence(result, text)


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='p370spoptest.', dir=STORAGE)
        self.root = Path(self.temp.name)
        os.chmod(self.root, 0o700)

    def tearDown(self):
        self.temp.cleanup()

    def private_file(self, name, text):
        target = self.root / name
        runner.private_write(target, text)
        return target

    def test_pins_and_config_metacharacters(self):
        path = self.private_file('input', 'data')
        digest = hashlib.sha256(b'data').hexdigest()
        self.assertEqual(runner.pinned(str(path), digest), path)
        for bad in ('0' * 64, digest.upper(), 'bad'):
            with self.assertRaises(ValueError):
                runner.pinned(str(path), bad)
        for text in ('relative', '/a/$VAR', '/a/${VAR}', '/a\nfoo', '/a/../b', '/a/"b', '/a\\b'):
            with self.assertRaises(ValueError):
                runner.safe_path(text)

    def test_symlink_hardlink_fifo_oversize_and_writable_input_rejected(self):
        original = self.private_file('original', 'data')
        link = self.root / 'link'
        link.symlink_to(original)
        with self.assertRaises(ValueError):
            runner.pinned(str(link), hashlib.sha256(b'data').hexdigest())
        hardlink = self.root / 'hardlink'
        os.link(original, hardlink)
        with self.assertRaises(ValueError):
            runner.pinned(str(hardlink), hashlib.sha256(b'data').hexdigest())
        fifo = self.root / 'fifo'
        os.mkfifo(fifo, 0o600)
        with self.assertRaises(ValueError):
            runner.pinned(str(fifo), '0' * 64)
        plain = self.private_file('plain', 'data')
        with self.assertRaises(ValueError):
            runner.pinned(str(plain), hashlib.sha256(b'data').hexdigest(), 1)
        os.chmod(plain, 0o666)
        with self.assertRaises(ValueError):
            runner.pinned(str(plain), hashlib.sha256(b'data').hexdigest())

    def test_duplicate_and_completed_malformed_json_rejected(self):
        for number, text in enumerate(('{}garbage\n', '{"phase":1,"phase":2}\n', '\n')):
            with self.assertRaises((ValueError, json.JSONDecodeError)):
                runner.read_events(self.private_file(str(number), text))

    def test_partial_json_retry_is_bounded_and_completion_supported(self):
        path = self.private_file('partial', '{"phase":')
        with self.assertRaises(ValueError):
            runner.read_events(path)
        def complete():
            time.sleep(0.05)
            with path.open('a') as output:
                output.write('2}\n')
        thread = threading.Thread(target=complete)
        thread.start()
        try:
            self.assertEqual(runner.read_events(path), [{'phase': 2}])
        finally:
            thread.join()

    def test_final_file_read_rejects_late_duplicate_and_incomplete_tail(self):
        probe = expected_probe()
        path = self.private_file('final-decisions', json.dumps(probe['decision']) + '\n')
        runner.verify_final_decisions(runner.read_events(path), [probe])
        with path.open('a') as output:
            output.write(json.dumps(probe['decision']) + '\n')
        with self.assertRaises(ValueError):
            runner.verify_final_decisions(runner.read_events(path), [probe])
        partial = self.private_file('final-partial', json.dumps(probe['decision']) + '\n{"request_id":')
        with self.assertRaises(ValueError):
            runner.read_events(partial)

    def test_live_await_waits_for_complete_host_mapping_then_binds_decision(self):
        probe = expected_probe()
        self.private_file('decision.jsonl', json.dumps(probe['decision']) + '\n')
        log = self.private_file('haproxy.log', '')
        line = host_line(probe)
        def flush_mapping():
            with log.open('a') as output:
                output.write(line[:30])
                output.flush()
                time.sleep(0.05)
                output.write(line[30:])
        writer = threading.Thread(target=flush_mapping)
        writer.start()
        try:
            records, engine = runner.await_decision(self.root, probe['id'])
            self.assertEqual(engine, probe['engine_id'])
            runner.verify_final_decisions(records, [probe])
        finally:
            writer.join()

    def test_output_root_and_cleanup_failure_never_pass(self):
        runner.validate_runtime_root(self.root)
        self.private_file('occupied', 'data')
        with self.assertRaises(ValueError):
            runner.validate_runtime_root(self.root)
        value = {'result': 'BLOCKED', 'passed': True, 'catalog_acceptance': False,
                 'gates': {f'G{i}': 'passed_prerequisite' for i in range(1, 10)}}
        runner.invalidate_cleanup(value, ['descendant survived'])
        self.assertFalse(value['passed'])
        self.assertEqual(value['result'], 'FAIL')
        self.assertEqual(value['gates']['G9'], 'failed')
        self.assertEqual(value['gates']['G3'], 'failed')


class OverlapTests(unittest.TestCase):
    def test_keepalive_second_incomplete_request_then_rst_cannot_use_previous_allow(self):
        allow = expected_probe(token=runner.token())
        blocked = expected_probe('p2', runner.token())
        prefixes = (f'POST /allow HTTP/1.1\r\nX-Request-ID: {blocked["id"]}\r\n'.encode(),
                    b'POST /allow HTTP/1.1')
        for prefix in prefixes:
            origin = runner.Upstream()
            captured = io.StringIO()
            client = socket.create_connection(('127.0.0.1', origin.server_port), timeout=2)
            try:
                client.sendall(runner.wire('allow', allow['id'], close=False))
                self.assertEqual(runner.read_response(client), 200)
                with redirect_stderr(captured):
                    client.sendall(prefix)
                    deadline = time.monotonic() + 1
                    started = False
                    while time.monotonic() < deadline:
                        with origin.lock:
                            started = any(progress['request_started'] and progress['active'] is None
                                          for progress in origin.parser_progress.values())
                        if started:
                            break
                        time.sleep(0.01)
                    self.assertTrue(started, 'observer must consume new request bytes before RST')
                    client.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))
                    client.close()
                    origin.close()
            finally:
                client.close()
                if origin.thread.is_alive():
                    origin.close()
            observation = origin.snapshot()
            self.assertGreater(observation['invalid_requests'], 0)
            self.assertGreater(observation['server_errors'], 0)
            self.assertEqual(observation['expected_resets'], 0)
            with self.assertRaises(ValueError):
                runner.verify_final_backend(observation, [allow, blocked])

    def test_idle_keepalive_reset_after_complete_response_remains_expected(self):
        origin = runner.Upstream()
        probe = expected_probe(token=runner.token())
        client = socket.create_connection(('127.0.0.1', origin.server_port), timeout=2)
        captured = io.StringIO()
        try:
            client.sendall(runner.wire('allow', probe['id'], close=False))
            self.assertEqual(runner.read_response(client), 200)
            with redirect_stderr(captured):
                client.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))
                client.close()
                origin.close()
        finally:
            client.close()
            if origin.thread.is_alive():
                origin.close()
        observation = origin.snapshot()
        self.assertEqual(observation['server_errors'], 0)
        self.assertEqual(observation['invalid_requests'], 0)
        self.assertEqual(observation['expected_resets'], 1)
        self.assertEqual(captured.getvalue(), '')
        runner.verify_final_backend(observation, [probe])

    def test_only_completed_or_declared_abort_resets_suppress_traceback(self):
        for response_completed, route, error, expected_reset in (
                (True, 'allow', ConnectionResetError(), True),
                (False, 'slow', BrokenPipeError(), True),
                (False, 'allow', ConnectionResetError(), False),
                (True, 'allow', RuntimeError('unexpected server error'), False)):
            origin = runner.Upstream()
            connection = socket.socket()
            origin.note_accept(connection)
            record = {'connection': 1, 'completed': True, 'route': route,
                      'response_headers_sent': True, 'response_completed': response_completed}
            origin.headers_seen.append(record)
            captured = io.StringIO()
            try:
                with redirect_stderr(captured):
                    try:
                        raise error
                    except Exception:
                        origin.handle_error(connection, ('127.0.0.1', 1))
                observation = origin.snapshot()
                self.assertEqual(observation['expected_resets'], int(expected_reset))
                self.assertEqual(observation['server_errors'], int(not expected_reset))
                self.assertEqual(bool(captured.getvalue()), not expected_reset)
            finally:
                connection.close()
                origin.close()

    def test_unexpected_handler_error_is_counted_and_fails_final_validation(self):
        origin = runner.Upstream()
        probe = expected_probe()
        captured = io.StringIO()
        try:
            with patch.object(runner.Handler, 'do_POST', side_effect=RuntimeError('fixture server failure')):
                with redirect_stderr(captured):
                    with self.assertRaises(http.client.RemoteDisconnected):
                        self.exchange(origin, 'POST', probe['id'])
        finally:
            origin.close()
        self.assertEqual(origin.snapshot()['server_errors'], 1)
        self.assertIn('fixture server failure', captured.getvalue())
        with self.assertRaises(ValueError):
            runner.verify_final_backend(origin.snapshot(), [probe])

    def exchange(self, origin, method, token, client=None):
        own = client is None
        client = client or http.client.HTTPConnection('127.0.0.1', origin.server_port, timeout=2)
        try:
            client.request(method, '/allow', body=b'ok=1', headers={'X-Request-ID': token})
            response = client.getresponse()
            response.read()
            return response.status
        finally:
            if own:
                client.close()

    def test_get_with_blocked_p2_id_is_observed_and_fails_final_validation(self):
        origin = runner.Upstream()
        probe = expected_probe('p2')
        try:
            self.assertEqual(self.exchange(origin, 'GET', probe['id']), 501)
        finally:
            origin.close()
        observation = origin.snapshot()
        self.assertEqual(len(observation['accepts']), 1)
        self.assertEqual(observation['headers'][0]['token'], probe['id'])
        self.assertEqual(observation['headers'][0]['method'], 'unsupported')
        with self.assertRaises(ValueError):
            runner.verify_final_backend(observation, [probe])

    def test_unknown_valid_token_cannot_hide_in_completed_backend_requests(self):
        origin = runner.Upstream()
        expected = expected_probe()
        try:
            self.assertEqual(self.exchange(origin, 'POST', runner.token()), 200)
        finally:
            origin.close()
        with self.assertRaises(ValueError):
            runner.verify_final_backend(origin.snapshot(), [expected])

    def test_missing_invalid_and_duplicate_ids_are_observed(self):
        for ids in ([], ['invalid'], [runner.token(), runner.token()]):
            origin = runner.Upstream()
            with socket.create_connection(('127.0.0.1', origin.server_port), timeout=1) as client:
                headers = ''.join('X-Request-ID: ' + value + '\r\n' for value in ids)
                client.sendall(('POST /allow HTTP/1.1\r\nHost: localhost\r\n' + headers
                                + 'Content-Length: 4\r\n\r\nok=1').encode())
                deadline = time.monotonic() + 1
                while not origin.snapshot()['headers'] and time.monotonic() < deadline:
                    time.sleep(0.01)
            origin.close()
            observation = origin.snapshot()
            self.assertEqual(len(observation['accepts']), 1)
            self.assertEqual(len(observation['headers']), 1)
            self.assertIsNone(observation['headers'][0]['token'])
            with self.assertRaises(ValueError):
                runner.verify_final_backend(observation, [])

    def test_backend_keepalive_multiple_expected_requests_share_one_accept(self):
        origin = runner.Upstream()
        probes = [expected_probe(token=runner.token()) for _ in range(2)]
        client = http.client.HTTPConnection('127.0.0.1', origin.server_port, timeout=2)
        try:
            for probe in probes:
                self.assertEqual(self.exchange(origin, 'POST', probe['id'], client), 200)
        finally:
            client.close()
            origin.close()
        observation = origin.snapshot()
        self.assertEqual(len(observation['accepts']), 1)
        self.assertEqual(len(observation['headers']), 2)
        runner.verify_final_backend(observation, probes)

    def test_header_only_and_empty_accept_fail_final_validation(self):
        for header_only in (False, True):
            origin = runner.Upstream()
            probe = expected_probe()
            client = socket.create_connection(('127.0.0.1', origin.server_port), timeout=1)
            try:
                if header_only:
                    client.sendall(runner.wire('allow', probe['id']).split(b'\r\n\r\n')[0] + b'\r\n\r\n')
                deadline = time.monotonic() + 1
                while time.monotonic() < deadline:
                    observation = origin.snapshot()
                    if observation['accepts'] and (not header_only or observation['headers']):
                        break
                    time.sleep(0.01)
                self.assertEqual(len(observation['accepts']), 1)
                if header_only:
                    self.assertFalse(observation['headers'][0]['completed'])
            finally:
                client.close()
                origin.close()
            with self.assertRaises(ValueError):
                runner.verify_final_backend(origin.snapshot(), [probe])

    def test_queued_dispatch_cannot_be_reported_as_zero(self):
        origin = runner.Upstream()
        # Pause the observer, then enqueue an already-connected request. The
        # producer is closed before cleanup, mirroring a reaped HAProxy.
        origin.shutdown()
        with socket.create_connection(('127.0.0.1', origin.server_port), timeout=1) as client:
            client.sendall(runner.wire('allow', runner.token()))
        with self.assertRaisesRegex(ValueError, 'queued upstream dispatch'):
            origin.close()
        self.assertFalse(origin.thread.is_alive())

    def test_serial_and_errored_parallel_observation_rejected(self):
        good = {'seen': 4, 'peak': 4, 'barrier_passes': 4, 'errors': 0, 'inflight': 0}
        runner.verify_parallel(good)
        for key, bad in (('peak', 1), ('barrier_passes', 3), ('errors', 1), ('errors', False), ('inflight', 1), ('seen', 5)):
            with self.assertRaises(ValueError):
                runner.verify_parallel(dict(good, **{key: bad}))

    def test_actual_upstream_four_client_overlap_and_cleanup(self):
        origin = runner.Upstream()
        def request(_):
            client = http.client.HTTPConnection('127.0.0.1', origin.server_port, timeout=7)
            try:
                client.request('POST', '/parallel', body=b'ok=1', headers={'X-Request-ID': runner.token()})
                response = client.getresponse()
                self.assertEqual(response.status, 200)
                self.assertEqual(response.read(), b'OK')
            finally:
                client.close()
        try:
            with ThreadPoolExecutor(max_workers=4) as executor:
                list(executor.map(request, range(4)))
            runner.verify_parallel(origin.parallel)
        finally:
            origin.close()
        self.assertFalse(origin.thread.is_alive())
        self.assertFalse(origin.live)


if __name__ == '__main__':
    unittest.main()
