"""Negative acceptance tests for the bounded direct-ext_proc host campaign."""
import importlib.util
import ast
import errno
import os
from pathlib import Path
import tempfile
from unittest.mock import Mock, patch
import hashlib
import http.client
import io
import socket
import signal
import subprocess
import sys
import threading
import time
from types import SimpleNamespace
import unittest

RUNNER = Path(__file__).resolve().parents[1] / 'connectors/envoy/harness/run_envoy_ext_proc_qualification.py'
SPEC = importlib.util.spec_from_file_location('envoy_qualification', RUNNER)
q = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(q)


def completion(identifier='q1-p1', reason='request_immediate_response'):
    result = {key: 0 for key in q.COMPLETION_KEYS}
    result.update(event='ext_proc_stream_complete', integration_mode='ext_proc',
        evaluation_mode='common_libmodsecurity_nonpromoted', rule_evaluation='libmodsecurity',
        transaction_id=identifier, late_action='none', close_reason=reason)
    result['request_header_count'] = 5
    if identifier.endswith('p2'):
        result.update(request_body_bytes=16, request_body_chunks=1)
    if identifier.endswith('p4'):
        result.update(request_body_bytes=2, request_body_chunks=1, response_header_count=5,
            response_body_bytes=16, response_body_chunks=1)
    return result


def event(identifier='q1-p1', rule='1900001', phase='request_headers', status=403):
    result = {key: '' for key in q.COMMON_TEXT}
    result.update({key: 0 for key in q.COMMON_INT})
    result.update({key: False for key in q.COMMON_BOOL})
    name = 'MSCONN_EVENT_RESPONSE_BLOCKED' if phase.startswith('response') else 'MSCONN_EVENT_REQUEST_BLOCKED'
    result.update(timestamp='2026-10-03T01:02:03Z', event=name, message_id=name, connector='envoy',
        integration_mode='ext_proc', transaction_id=identifier, phase=phase,
        requested_action='deny', actual_action='deny', visible_http_status=status,
        http_status=403, rule_id=rule, transport_result='http_status', status='blocked', action='deny',
        sequence=2, previous_event_hash=123, event_hash=456)
    if phase == 'request_body':
        result.update(body_bytes_seen=16, body_bytes_inspected=16)
    if phase.startswith('response'):
        result['original_http_status'] = 200
    return result


def decision_pair(host):
    engine = dict(host)
    engine.update(sequence=1, previous_event_hash=0, event_hash=123, actual_action='deny',
        transport_result='', visible_http_status=200 if host['phase'].startswith('response') else 0)
    if host['phase'] == 'response_body':
        engine['late_intervention'] = False
        engine.pop('late_intervention_mode', None)
    return [engine, host]


def cancel_event():
    record = event('q1-cancel', '', 'response_headers', 200)
    record.update(event='client_cancel', message_id='MSCONN_EVENT_CLIENT_CANCEL',
        action='abort_connection', requested_action='abort_connection', actual_action='abort_connection',
        http_status=0, original_http_status=200, visible_http_status=200, transport_result='',
        body_bytes_seen=1, body_bytes_inspected=1, response_started=True, response_committed=True,
        headers_sent=True, body_started=True, client_disconnected=True, cancelled=True, sequence=1)
    return record


class BoundaryDeltaTests(unittest.TestCase):
    def test_explicit_buffered_profile_preserves_streaming_default(self):
        self.assertEqual(q.QUALIFICATION_PROFILE, 'envoy-ext-proc-buffered-admission')
        syntax = ast.parse(RUNNER.read_text())
        for function_name, result_name in (('run_start', 'result'), ('main', 'summary')):
            function = next(node for node in syntax.body if isinstance(node, ast.FunctionDef) and node.name == function_name)
            assignment = next(node for node in ast.walk(function) if isinstance(node, ast.Assign) and
                any(isinstance(target, ast.Name) and target.id == result_name for target in node.targets))
            profile = next(keyword.value for keyword in assignment.value.keywords if keyword.arg == 'profile')
            self.assertIsInstance(profile, ast.Name)
            self.assertEqual(profile.id, 'QUALIFICATION_PROFILE')
        self.assertNotIn('envoy-ext-proc-streamed', RUNNER.read_text())
        renderer = RUNNER.parents[1] / 'config/prepare_envoy_ext_proc_config.sh'
        with tempfile.TemporaryDirectory() as directory:
            for profile in ('streaming', 'buffered-admission'):
                output = Path(directory) / (profile + '.yaml')
                env = dict(os.environ, PROFILE=profile, OUTPUT_CONFIG=str(output),
                    TLS_CERTIFICATE='/qualification/cert.pem', TLS_PRIVATE_KEY='/qualification/key.pem')
                subprocess.run(['sh', str(renderer)], env=env, check=True, capture_output=True)
                rendered = output.read_text()
                self.assertIn('request_body_mode: ' + ('STREAMED' if profile == 'streaming' else 'BUFFERED'), rendered)
                self.assertIn('response_body_mode: STREAMED', rendered)
                self.assertIn('request_trailer_mode: SEND', rendered)
                self.assertIn('response_trailer_mode: SEND', rendered)
                self.assertEqual('per_connection_buffer_limit_bytes: 65536' in rendered, profile == 'buffered-admission')
                self.assertIn('failure_mode_allow: false', rendered)

    def response(self, headers, body, status=200):
        wire = b'HTTP/1.1 ' + str(status).encode() + b' Test\r\n' + headers + b'\r\n' + body
        response = http.client.HTTPResponse(SimpleNamespace(makefile=lambda *args: io.BytesIO(wire)))
        response.begin()
        return response

    def test_real_client_response_framing_positive(self):
        for headers, body, kind in (
            (b'Content-Length: 2\r\n', b'ok', 'allow'),
            (b'Content-Length: 0\r\n', b'', 'response-zero'),
            (b'Transfer-Encoding: ChUnKeD\r\n', b'1\r\no\r\n1\r\nk\r\n0\r\n\r\n', 'allow'),
            (b'Transfer-Encoding: chunked\r\n', b'0\r\n\r\n', 'response-zero'),
            (b'Transfer-Encoding: chunked\r\n', b'2\r\nok\r\n0\r\nX-Trailer: yes\r\n\r\n', 'allow'),
            (b'Connection: close\r\n', b'ok', 'allow'),
            (b'', b'', 'response-zero')):
            with self.subTest(headers=headers, kind=kind):
                self.assertTrue(q.client_receipt(self.response(headers, body), kind)['eos'])

    def test_real_client_response_framing_negative(self):
        for headers, body in (
            (b'Content-Length: 2\r\nTransfer-Encoding: chunked\r\n', b'2\r\nok\r\n0\r\n\r\n'),
            (b'Content-Length: 2\r\nContent-Length: 2\r\n', b'ok'),
            (b'Content-Length: -1\r\n', b'ok'),
            (b'Content-Length: 02\r\n', b'ok'),
            (b'Content-Length: +2\r\n', b'ok'),
            (b'Content-Length: 2 \r\n', b'ok'),
            (b'Content-Length: \xb2\r\n', b'ok'),
            (b'Content-Length: 3\r\n', b'ok'),
            (b'Content-Length: 65537\r\n', b''),
            (b'Transfer-Encoding: gzip\r\n', b'ok'),
            (b'Transfer-Encoding: gzip, chunked\r\n', b'ok'),
            (b'Transfer-Encoding: chunked, chunked\r\n', b'ok'),
            (b'Transfer-Encoding: chunked\r\nTransfer-Encoding: chunked\r\n', b'2\r\nok\r\n0\r\n\r\n'),
            (b'Transfer-Encoding: chunked\r\n', b'3\r\nok'),
            (b'Transfer-Encoding: chunked\r\n', b'2\r\nok\r\n'),
            (b'Transfer-Encoding: chunked\r\n', b'2\r\nokXX0\r\n\r\n'),
            (b'Transfer-Encoding: chunked\r\n', b'2\nok\r\n0\r\n\r\n'),
            (b'Transfer-Encoding: chunked\r\n', b'+2\r\nok\r\n0\r\n\r\n'),
            (b'Transfer-Encoding: chunked\r\n', b' 2\r\nok\r\n0\r\n\r\n'),
            (b'Transfer-Encoding: chunked\r\n', b'2\r\nok\r\n0\n\r\n'),
            (b'Transfer-Encoding: chunked\r\n', b'2;bad extension\r\nok\r\n0\r\n\r\n'),
            (b'Transfer-Encoding: chunked\r\n', b'-1\r\nok\r\n0\r\n\r\n'),
            (b'Transfer-Encoding: chunked\r\n', b'2\r\nok\r\n0\r\n'),
            (b'Transfer-Encoding: chunked\r\n', b'2\r\nok\r\n0\r\nX-Trailer: yes\r\n'),
            (b'Transfer-Encoding: chunked\r\n', b'2\r\nok\r\n0\r\n' + b'X-Trailer: ' + b'x' * 8192 + b'\r\n\r\n'),
            (b'Connection: close\r\n', b'x' * 65537)):
            with self.subTest(headers=headers, body_length=len(body)), self.assertRaises(q.InvalidEvidence):
                q.client_receipt(self.response(headers, body), 'allow')

    def test_chunk_parser_bounds_all_body_reads_and_restores_hooks(self):
        class TrackingStream(io.BytesIO):
            def __init__(self, wire):
                super().__init__(wire)
                self.read_sizes = []
                self.line_sizes = []

            def read(self, amount=-1):
                self.read_sizes.append(amount)
                if not 0 <= amount <= 65536:
                    raise AssertionError(f'unbounded read({amount})')
                return super().read(amount)

            def readline(self, amount=-1):
                self.line_sizes.append(amount)
                if not 0 <= amount <= 8193:
                    raise AssertionError(f'unbounded readline({amount})')
                return super().readline(amount)

        valid = (b'1\r\no\r\n1\r\nk\r\n0\r\n\r\n',
            b'0\r\n\r\n', b'2\r\nok\r\n0\r\nX-Trailer: yes\r\n\r\n')
        invalid = (b'-1\r\n', b'+2\r\n', b' 2\r\n', b'2\n', b'0\n\r\n',
            b'2;bad extension\r\n', b'10001\r\n', b'ffffffffffffffff\r\n',
            b'1\r\nx\r\n' * 1024 + b'0\r\n\r\n',
            b'1\r\nx\r\n0\r\n' + (b'X: ' + b'x' * 4088 + b'\r\n') * 2 + b'\r\n')
        for wire in valid + invalid:
            with self.subTest(wire_prefix=wire[:30]):
                response = self.response(b'Transfer-Encoding: chunked\r\n', b'')
                response.fp.close()
                stream = TrackingStream(wire)
                response.fp = stream
                hooks = (response._safe_read, response._read_next_chunk_size,
                    response._read_and_discard_trailer)
                if wire in invalid:
                    with self.assertRaises(q.InvalidEvidence):
                        q.client_receipt(response, 'allow')
                else:
                    kind = 'response-zero' if wire.startswith(b'0') else 'allow'
                    self.assertTrue(q.client_receipt(response, kind)['eos'])
                self.assertEqual(hooks, (response._safe_read, response._read_next_chunk_size,
                    response._read_and_discard_trailer))
                self.assertTrue(stream.line_sizes)
                self.assertTrue(all(0 <= n <= 65536 for n in stream.read_sizes))
                self.assertTrue(all(0 <= n <= 8193 for n in stream.line_sizes))

    def test_response_payload_digest_length_and_eos_are_required(self):
        for kind in ('response-zero', 'response-exact', 'response-limit', 'exact', 'chunked-exact'):
            body = q.response_body(kind)
            response = self.response(f'Content-Length: {len(body)}\r\n'.encode(), body)
            receipt = q.client_receipt(response, kind)
            self.assertEqual(receipt['bytes'], len(body))
            self.assertEqual(receipt['sha256'], hashlib.sha256(body).hexdigest())
            self.assertTrue(receipt['eos'])
            for broken in (body + b'x', body[:-1] if body else b'x', b'Q' * len(body) if body else b'x'):
                response = self.response(f'Content-Length: {len(broken)}\r\n'.encode(), broken)
                with self.subTest(kind=kind, broken=broken), self.assertRaises(q.InvalidEvidence):
                    q.client_receipt(response, kind)

    def test_redirect_requires_one_exact_safe_location(self):
        response = self.response(f'Location: {q.REDIRECT_LOCATION}\r\nContent-Length: 0\r\n'.encode(), b'', 302)
        q.client_receipt(response, 'redirect')
        for headers in ([], [('Location', q.REDIRECT_LOCATION)] * 2,
            [('Location', q.REDIRECT_LOCATION + '\r\n Injected: yes')], [('Location', '/wrong')]):
            response = self.response(b''.join(f'{name}: {value}\r\n'.encode() for name, value in headers), b'', 302)
            with self.subTest(headers=headers), self.assertRaises(q.InvalidEvidence):
                q.client_receipt(response, 'redirect')

    def test_response33_safe_requires_no_native_event_and_log_only_eos(self):
        record = completion('q1-response-limit', 'response_end_of_stream')
        record.update(request_body_bytes=2, request_body_chunks=1, response_header_count=5,
            response_body_bytes=33, response_body_chunks=1, late_action='log_only')
        q.verify_probe('q1-response-limit', 200, 1, [record], [], 'response-limit')
        for key, value in (('response_body_bytes', 32), ('close_reason', 'grpc_peer_eof'), ('late_action', 'none')):
            broken = dict(record, **{key: value})
            with self.subTest(key=key), self.assertRaises(q.InvalidEvidence):
                q.verify_probe('q1-response-limit', 200, 1, [broken], [], 'response-limit')
        with self.assertRaises(q.InvalidEvidence):
            q.verify_probe('q1-response-limit', 200, 1, [record], [event('q1-response-limit')], 'response-limit')

    def test_unavailable_must_have_zero_engine_and_backend_evidence(self):
        q.verify_unavailable('q1-unavailable', 500, 0, [], [])
        for status, backend, complete, events in ((200, 0, [], []), (503, 0, [], []), (500, 1, [], []),
            (500, 0, [completion('q1-unavailable')], []), (500, 0, [], [event('q1-unavailable')])):
            with self.subTest(status=status, backend=backend, complete=complete, events=events), self.assertRaises(q.InvalidEvidence):
                q.verify_unavailable('q1-unavailable', status, backend, complete, events)

    def test_chunked_sender_uses_two_delayed_real_chunks_and_exact_eos(self):
        client = Mock()
        with patch.object(q.time, 'sleep') as delay:
            sent = q.send_chunked_request(client, 'q1-chunked-exact', 'chunked-exact', '/qualification/chunked-exact')
        self.assertEqual(sent['chunks'], 2)
        self.assertEqual(sent['bytes'], 32)
        self.assertEqual(sent['sha256'], hashlib.sha256(b'x' * 32).hexdigest())
        self.assertEqual(client.send.call_args_list[-1].args, (b'0\r\n\r\n',))
        delay.assert_called_once_with(.1)
        self.assertFalse(any(call.args[0].lower() == 'content-length' for call in client.putheader.call_args_list))

    def test_cancel_requires_started_stream_and_real_cancel_completion(self):
        record = completion('q1-cancel', 'grpc_context_canceled_unattributed')
        record.update(request_body_bytes=2, request_body_chunks=1, response_header_count=5,
            response_body_bytes=1, response_body_chunks=1)
        cancel = cancel_event()
        q.verify_cancel('q1-cancel', [record], [cancel], 1, 1)
        for bad_events in ([], [cancel, cancel], [dict(cancel, transaction_id='q1-foreign')]):
            with self.assertRaises(q.InvalidEvidence):
                q.verify_cancel('q1-cancel', [record], bad_events, 1, 1)
        for key, value in (('eos_seen', True), ('cancelled', False), ('body_bytes_seen', 2),
            ('body_bytes_inspected', 0), ('rule_id', '1900004'), ('actual_action', 'deny')):
            with self.subTest(event_field=key), self.assertRaises(q.InvalidEvidence):
                q.verify_cancel('q1-cancel', [record], [dict(cancel, **{key: value})], 1, 1)
        for key, value in (('response_body_bytes', 0), ('response_header_count', 0),
            ('close_reason', 'response_end_of_stream')):
            with self.subTest(key=key), self.assertRaises(q.InvalidEvidence):
                q.verify_cancel('q1-cancel', [dict(record, **{key: value})], [cancel], 1, 1)

    def test_redirect_engine_host_pair_has302_and_redirect_action(self):
        host = event('q1-redirect', '1900005', 'response_headers', 302)
        host.update(http_status=302, action='redirect', requested_action='redirect', actual_action='redirect')
        records = decision_pair(host)
        records[0]['actual_action'] = 'redirect'
        complete = completion('q1-redirect')
        complete.update(request_body_bytes=2, request_body_chunks=1, response_header_count=5)
        q.verify_probe('q1-redirect', 302, 1, [complete], records, 'redirect')
        for key, value in (('actual_action', 'deny'), ('http_status', 403), ('rule_id', '1900003')):
            changed = [dict(record) for record in records]
            changed[1][key] = value
            with self.subTest(key=key), self.assertRaises(q.InvalidEvidence):
                q.verify_probe('q1-redirect', 302, 1, [complete], changed, 'redirect')

    def test_exact_request32_and_response_boundary_counters(self):
        for kind in ('exact', 'chunked-exact', 'response-zero', 'response-exact'):
            complete = completion('q1-' + kind, 'response_end_of_stream')
            complete.update(request_body_bytes=len(q.probe_body(kind)), request_body_chunks=1,
                response_header_count=5, response_body_bytes=len(q.response_body(kind)),
                response_body_chunks=int(bool(q.response_body(kind))))
            q.verify_probe('q1-' + kind, 200, 1, [complete], [], kind)
            with self.subTest(kind=kind), self.assertRaises(q.InvalidEvidence):
                q.verify_probe('q1-' + kind, 200, 1, [dict(complete, request_body_bytes=31)], [], kind)
            if kind == 'chunked-exact':
                with self.assertRaises(q.InvalidEvidence):
                    q.verify_probe('q1-' + kind, 200, 1, [dict(complete, request_body_chunks=2)], [], kind)

    def test_client_content_length_and_response_eos_mutations(self):
        response = Mock(status=200)
        response.length = 2
        response.chunked = False
        response.isclosed.return_value = True
        for headers, reads in (([('Content-Length', '3')], [b'ok', b'']),
            ([('Content-Length', '2')] * 2, [b'ok', b'']),
            ([('Content-Length', '02')], [b'ok', b'']),
            ([('Content-Length', '2')], [b'ok', b'tail'])):
            response.getheaders.return_value = headers
            response.read.side_effect = reads
            with self.subTest(headers=headers, reads=reads), self.assertRaises(q.InvalidEvidence):
                q.client_receipt(response, 'allow')

    def test_source_manifest_requests_new_and_untracked_relevant_tests(self):
        with patch.object(q.subprocess, 'check_output', return_value=b'tests/test_envoy_new.py\0') as command, \
            patch.object(q, 'read_safe', return_value=b'new test') as read:
            q.source_digest()
        argv = command.call_args.args[0]
        for required in ('--others', '--cached', '--exclude-standard', 'tests/test_envoy*', 'tests/test_common*'):
            self.assertIn(required, argv)
        read.assert_called_once_with(q.REPO / 'tests/test_envoy_new.py')


class ResourceSnapshotTests(unittest.TestCase):
    def snapshot(self, links, *, listing_error=None, status_error=None, directory_error=None):
        entries = [Path('/proc/101/fd') / str(number) for number in range(len(links))]
        with patch.object(q.Path, 'read_text', side_effect=status_error or ['VmRSS: 42 kB\n', 'VmRSS: 43 kB\n']), \
            patch.object(q.Path, 'iterdir', side_effect=listing_error or [iter(entries)]), \
            patch.object(q.Path, 'stat', side_effect=directory_error) as directory_check, \
            patch.object(q.os, 'readlink', side_effect=links):
            result = q.resources(101)
        return result, directory_check

    def test_single_closed_fd_does_not_invalidate_resource_snapshot(self):
        result, directory_check = self.snapshot(['socket:[1]', FileNotFoundError(errno.ENOENT, 'closed fd'), '/file'])
        self.assertEqual(result, dict(rss_kib=42, fds=3, sockets=1))
        directory_check.assert_called_once()

    def test_all_closed_fds_retain_listed_count_without_fake_sockets(self):
        result, _ = self.snapshot([FileNotFoundError(errno.ENOENT, 'closed fd')] * 3)
        self.assertEqual(result, dict(rss_kib=42, fds=3, sockets=0))

    def test_process_loss_even_without_an_entry_race_is_fatal(self):
        for links in ([], ['socket:[1]']):
            for kwargs in (
                {'directory_error': FileNotFoundError(errno.ENOENT, 'dead process')},
                {'status_error': ['VmRSS: 42 kB\n', FileNotFoundError(errno.ENOENT, 'dead process')]}):
                with self.subTest(links=links, kwargs=kwargs), self.assertRaises(FileNotFoundError):
                    self.snapshot(links, **kwargs)

    def test_missing_fd_directory_or_status_is_fatal(self):
        for kwargs in (
            {'listing_error': FileNotFoundError(errno.ENOENT, 'dead process fd dir')},
            {'status_error': FileNotFoundError(errno.ENOENT, 'dead process status')},
            {'directory_error': FileNotFoundError(errno.ENOENT, 'dead process fd dir')},
            {'status_error': ['VmRSS: 42 kB\n', FileNotFoundError(errno.ENOENT, 'process died during snapshot')]}):
            with self.subTest(kwargs=kwargs), self.assertRaises(FileNotFoundError):
                self.snapshot([FileNotFoundError(errno.ENOENT, 'missing fd')], **kwargs)

    def test_permission_and_other_readlink_failures_are_fatal(self):
        for code in (errno.EACCES, errno.EPERM, errno.EIO, errno.ENOTDIR):
            with self.subTest(code=code), self.assertRaises(OSError) as caught:
                self.snapshot([OSError(code, 'readlink failed')])
            self.assertEqual(caught.exception.errno, code)

    def test_permission_errors_on_parent_or_status_are_fatal(self):
        for kwargs in ({'listing_error': PermissionError(errno.EACCES, 'fd dir')},
            {'directory_error': PermissionError(errno.EACCES, 'fd dir')},
            {'status_error': ['VmRSS: 42 kB\n', PermissionError(errno.EACCES, 'status')]}):
            with self.subTest(kwargs=kwargs), self.assertRaises(PermissionError):
                self.snapshot([FileNotFoundError(errno.ENOENT, 'missing fd')], **kwargs)


class SafeInputTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix='extproc-unit-', dir=q.EXTERNAL / 'runs')
        self.root = Path(self.directory.name)
        self.root.chmod(0o700)

    def tearDown(self):
        self.directory.cleanup()

    def write(self, value):
        path = self.root / 'input'
        path.write_bytes(value)
        return path

    def test_regular_input(self):
        self.assertEqual(q.read_safe(self.write(b'abc')), b'abc')

    def test_symlink_input(self):
        source = self.write(b'abc')
        link = self.root / 'link'
        link.symlink_to(source)
        with self.assertRaises(q.InvalidEvidence):
            q.read_safe(link)

    def test_ancestor_symlink(self):
        child = self.root / 'child'
        child.mkdir()
        (child / 'data').write_bytes(b'abc')
        (self.root / 'alias').symlink_to(child)
        with self.assertRaises(q.InvalidEvidence):
            q.read_safe(self.root / 'alias/data')

    def test_hardlink_input(self):
        source = self.write(b'abc')
        os.link(source, self.root / 'other')
        with self.assertRaises(q.InvalidEvidence):
            q.read_safe(source)

    def test_fifo_does_not_block(self):
        fifo = self.root / 'fifo'
        os.mkfifo(fifo)
        with self.assertRaises(q.InvalidEvidence):
            q.read_safe(fifo)

    def test_bound(self):
        with self.assertRaises(q.InvalidEvidence):
            q.read_safe(self.write(b'abc'), 2)

    def test_world_writable_input(self):
        path = self.write(b'abc')
        path.chmod(0o666)
        with self.assertRaises(q.InvalidEvidence):
            q.read_safe(path)

    def test_config_expansion_path(self):
        with self.assertRaises(q.InvalidEvidence):
            q.checked_path(Path('/var/tmp/${HOME}'))

    def test_pin_mismatch(self):
        with self.assertRaises(q.InvalidEvidence):
            q.digest(self.write(b'abc'), '0' * 64)

    def test_runner_pin_rejects_wrong_digest_before_start(self):
        path = self.write(b'untracked runner')
        with self.assertRaises(q.InvalidEvidence):
            q.runner_identity('0' * 64, path)

    def test_runner_pin_is_descriptor_bound_and_untracked_capable(self):
        path = self.write(b'untracked runner')
        expected = hashlib.sha256(b'untracked runner').hexdigest()
        with patch.object(q.subprocess, 'check_output', side_effect=AssertionError('runner pin must not use Git')):
            pin = q.runner_identity(expected, path)
            q.verify_runner(pin)
        self.assertEqual(pin['sha256'], expected)
        self.assertEqual(pin['inode'], path.stat().st_ino)

    def test_mid_campaign_runner_change_prevents_next_start(self):
        path = self.write(b'original runner')
        pin = q.runner_identity(hashlib.sha256(b'original runner').hexdigest(), path)
        def change_runner(*_args):
            path.write_bytes(b'changed runner')
            return dict(passed=True)
        with patch.object(q, 'run_start', side_effect=change_runner) as start:
            with self.assertRaises(q.InvalidEvidence):
                q.pinned_starts(SimpleNamespace(root=self.root), {}, pin)
            self.assertEqual(start.call_count, 1)
        summary = q.json.loads((self.root / 'qualification.json').read_text())
        self.assertFalse(summary['passed'])
        self.assertFalse(summary['runner_pin_verified'])
        self.assertEqual(summary['runner_sha256'], pin['sha256'])

    def test_runner_content_restoration_does_not_restore_identity(self):
        path = self.write(b'original runner')
        pin = q.runner_identity(path=path)
        path.write_bytes(b'changed runner')
        path.write_bytes(b'original runner')
        os.utime(path, ns=(pin['mtime_ns'] + 1000000000, pin['mtime_ns'] + 1000000000))
        with self.assertRaises(q.InvalidEvidence):
            q.verify_runner(pin)

    def test_uppercase_pin_rejected(self):
        with self.assertRaises(q.InvalidEvidence):
            q.digest(self.write(b'abc'), 'A' * 64)

    def test_partial_jsonl(self):
        with self.assertRaises(q.InvalidEvidence):
            q.jsonl(self.write(b'{"event":"x"}'))

    def test_malformed_jsonl(self):
        with self.assertRaises(ValueError):
            q.jsonl(self.write(b'{wrong}\n'))

    def test_duplicate_key(self):
        with self.assertRaises(q.InvalidEvidence):
            q.jsonl(self.write(b'{"event":"x","event":"y"}\n'))

    def test_nonfinite(self):
        with self.assertRaises(q.InvalidEvidence):
            q.jsonl(self.write(b'{"x":NaN}\n'))

    def test_empty_record(self):
        with self.assertRaises(q.InvalidEvidence):
            q.jsonl(self.write(b'\n'))

    def test_closed_jsonl(self):
        self.assertEqual(q.jsonl(self.write(b'{"event":"x"}\n')), [{'event': 'x'}])

    def test_library_mount_translation_is_bound(self):
        path = self.root / 'libmodsecurity.so'
        path.write_bytes(b'library')
        pin = q.digest(path, hashlib.sha256(b'library').hexdigest())
        mapped = pin['dev'] + 1
        line = f'1-2 r--p 0 {os.major(mapped):02x}:{os.minor(mapped):02x} {pin["inode"]} {path}\n'
        with patch.object(Path, 'read_text', return_value=line), patch.object(q, 'mounted_device', return_value=mapped), \
            patch.object(q, 'mount_namespace_identity', return_value=(1, 2)):
            self.assertEqual(q.loaded_library(123, pin), [line.strip()])
        with patch.object(Path, 'read_text', return_value=line), patch.object(q, 'mounted_device', return_value=mapped + 1), \
            patch.object(q, 'mount_namespace_identity', return_value=(1, 2)):
            with self.assertRaises(q.InvalidEvidence):
                q.loaded_library(123, pin)

    def test_library_translation_rejects_different_mount_namespace(self):
        path = self.root / 'libmodsecurity.so'
        path.write_bytes(b'library')
        pin = q.digest(path, hashlib.sha256(b'library').hexdigest())
        mapped = pin['dev'] + 1
        line = f'1-2 r--p 0 {os.major(mapped):02x}:{os.minor(mapped):02x} {pin["inode"]} {path}\n'
        with patch.object(Path, 'read_text', return_value=line), patch.object(q, 'mounted_device', return_value=mapped), \
            patch.object(q, 'mount_namespace_identity', side_effect=[(1, 2), (1, 3)]):
            with self.assertRaises(q.InvalidEvidence):
                q.loaded_library(123, pin)

    def test_mount_uses_deepest_component_boundary(self):
        rows = '1 0 0:1 / / rw - overlay overlay rw\n2 1 0:2 / /var/tmp rw - ext4 device rw\n3 1 0:3 / /var/tmps rw - ext4 device rw\n'
        with patch.object(Path, 'read_text', return_value=rows):
            self.assertEqual(q.mounted_device(123, '/var/tmp/libmodsecurity.so'), os.makedev(0, 2))


class ObserverTests(unittest.TestCase):
    def origin(self):
        return q.Origin(0, SimpleNamespace(wrap_socket=lambda connection, **_kw: connection))

    def test_queued_headers_are_drained_before_zero_backend_acceptance(self):
        origin = self.origin()
        wire = socket.create_connection(origin.server_address, 1)
        wire.sendall(b'POST /qualification/p1 HTTP/1.1\r\nHost: localhost\r\nX-Request-Id: q1-p1\r\nContent-Length: 0\r\nConnection: close\r\n\r\n')
        self.assertEqual(origin.observations.get('q1-p1', 0), 0)
        try:
            origin.drain_backlog()
            origin.server_close()
            self.assertEqual(origin.observations.get('q1-p1'), 1)
            self.assertEqual(origin.header_arrivals, 1)
            origin.verify_attribution()
        finally:
            wire.close()
            origin.server_close()

    def test_missing_invalid_duplicate_and_wrong_method_are_counted(self):
        for method, headers in [('POST', ''), ('POST', 'X-Request-Id: invalid\r\n'),
            ('POST', 'X-Request-Id: q1-p1\r\nX-Request-Id: q1-p1\r\n'),
            ('GET', 'X-Request-Id: q1-p1\r\n')]:
            with self.subTest(method=method, headers=headers):
                origin = self.origin()
                wire = socket.create_connection(origin.server_address, 1)
                wire.sendall((f'{method} /qualification/p1 HTTP/1.1\r\nHost: localhost\r\n{headers}Content-Length: 0\r\nConnection: close\r\n\r\n').encode())
                try:
                    origin.drain_backlog()
                    origin.server_close()
                    self.assertEqual(origin.header_arrivals, 1)
                    self.assertEqual(origin.unattributed, 1)
                    with self.assertRaises(q.InvalidEvidence):
                        origin.verify_attribution()
                finally:
                    wire.close()
                    origin.server_close()

    def exchange(self, framing, payload):
        origin = self.origin()
        wire = socket.create_connection(origin.server_address, 1)
        wire.sendall(b'POST /qualification/allow HTTP/1.1\r\nHost: localhost\r\nX-Request-Id: q1-allow\r\n' +
            framing + b'Connection: close\r\n\r\n' + payload)
        wire.shutdown(socket.SHUT_WR)
        try:
            origin.drain_backlog()
            origin.server_close()
            response = wire.recv(4096)
            return origin, response
        finally:
            wire.close()
            origin.server_close()

    def test_envoy_chunked_forwarding_reads_complete_body(self):
        origin, response = self.exchange(b'Transfer-Encoding: chunked\r\n', b'1\r\no\r\n1\r\nk\r\n0\r\n\r\n')
        self.assertTrue(response.startswith(b'HTTP/1.1 200'))
        origin.verify_attribution()
        q.verify_origin_probe(origin, 'q1-allow', 'allow')
        receipt = origin.body_receipts['q1-allow'][0]
        self.assertEqual((receipt['framing'], receipt['bytes'], receipt['chunks'], receipt['eos']),
            ('chunked', 2, 2, True))

    def test_empty_chunked_forwarding(self):
        origin, response = self.exchange(b'Transfer-Encoding: chunked\r\n', b'0\r\n\r\n')
        self.assertTrue(response.startswith(b'HTTP/1.1 200'))
        origin.verify_attribution()
        self.assertEqual(origin.body_receipts['q1-allow'][0]['bytes'], 0)
        q.verify_origin_probe(origin, 'q1-allow', 'empty')

    def test_origin_empty_body_cannot_pass_allow_completion(self):
        for framing in (b'Content-Length: 0\r\n', b''):
            with self.subTest(framing=framing):
                origin, response = self.exchange(framing, b'')
                self.assertTrue(response.startswith(b'HTTP/1.1 200'))
                origin.verify_attribution()
                with self.assertRaises(q.InvalidEvidence):
                    q.verify_origin_probe(origin, 'q1-allow', 'allow')

    def test_origin_equal_length_mutation_cannot_pass(self):
        for framing, payload in [(b'Content-Length: 2\r\n', b'NO'),
            (b'Transfer-Encoding: chunked\r\n', b'2\r\nNO\r\n0\r\n\r\n')]:
            with self.subTest(framing=framing):
                origin, response = self.exchange(framing, payload)
                self.assertTrue(response.startswith(b'HTTP/1.1 200'))
                origin.verify_attribution()
                self.assertEqual(origin.body_receipts['q1-allow'][0]['bytes'], 2)
                with self.assertRaises(q.InvalidEvidence):
                    q.verify_origin_probe(origin, 'q1-allow', 'allow')

    def test_receipt_requires_true_eos_and_fixed_digest_for_all_forwarded_probes(self):
        for kind in ('allow', 'p3', 'p4'):
            for eos, digest in [(False, hashlib.sha256(b'ok').hexdigest()),
                (1, hashlib.sha256(b'ok').hexdigest()), (True, hashlib.sha256(b'NO').hexdigest())]:
                with self.subTest(kind=kind, eos=eos, digest=digest):
                    origin = SimpleNamespace(lock=threading.Lock(), observations={'q1-probe': 1},
                        body_receipts={'q1-probe': [dict(bytes=2, eos=eos, sha256=digest)]})
                    with self.assertRaises(q.InvalidEvidence):
                        q.verify_origin_probe(origin, 'q1-probe', kind)

    def test_blocked_probes_require_no_body_or_header_receipts(self):
        for kind in ('p1', 'p2', 'limit'):
            origin = SimpleNamespace(lock=threading.Lock(), observations={}, body_receipts={})
            q.verify_origin_probe(origin, 'q1-block', kind)
            origin.observations['q1-block'] = 1
            with self.assertRaises(q.InvalidEvidence):
                q.verify_origin_probe(origin, 'q1-block', kind)

    def test_invalid_chunked_framing_cannot_award_evidence(self):
        cases = [(b'Transfer-Encoding: chunked\r\n', b'2\r\no'),
            (b'Transfer-Encoding: chunked\r\n', b'zz\r\n'),
            (b'Transfer-Encoding: chunked\r\n', b'2\r\nokXX0\r\n\r\n'),
            (b'Transfer-Encoding: chunked\r\n', b'22\r\n' + b'x' * 34 + b'\r\n0\r\n\r\n'),
            (b'Transfer-Encoding: chunked\r\n', b'0\r\nX-Trailer: value\r\n\r\n'),
            (b'Transfer-Encoding: chunked\r\nContent-Length: 2\r\n', b'2\r\nok\r\n0\r\n\r\n'),
            (b'Transfer-Encoding: gzip, chunked\r\n', b'0\r\n\r\n'),
            (b'Content-Length: 2\r\nContent-Length: 2\r\n', b'ok')]
        for framing, payload in cases:
            with self.subTest(framing=framing, payload=payload):
                origin, response = self.exchange(framing, payload)
                self.assertFalse(response.startswith(b'HTTP/1.1 200'))
                self.assertEqual(origin.observations['q1-allow'], 1)
                self.assertTrue(origin.framing_errors)
                with self.assertRaises(q.InvalidEvidence):
                    origin.verify_attribution()

    def test_cleanup_captures_child_that_creates_new_session(self):
        code = 'import os,time\npid=os.fork()\nif pid == 0:\n os.setsid()\n time.sleep(60)\nelse:\n time.sleep(60)\n'
        process = subprocess.Popen([sys.executable, '-c', code], start_new_session=True)
        process.qualification_identity = q.process_identity(process.pid)
        process.qualification_tree = q.ProcessTree(process.qualification_identity)
        try:
            deadline = time.monotonic() + 3
            while len(process.qualification_tree.sample()) < 2 and time.monotonic() < deadline:
                time.sleep(.01)
            children = process.qualification_tree.sample()
            self.assertEqual(len(children), 2)
            child = next(entry for entry in children if entry['pid'] != process.pid)
            self.assertNotEqual(child['session'], process.pid)
            q.stop_process(process)
            try:
                self.assertEqual(q.process_identity(child['pid'])['state'], 'Z')
            except FileNotFoundError:
                pass
        finally:
            if process.poll() is None:
                q.stop_process(process)

    def test_subreaper_reaps_orphan_from_immediate_double_fork(self):
        # Isolate prctl to a standalone runner process, as in the real campaign.
        script = '''import importlib.util, os, subprocess, sys, time
spec=importlib.util.spec_from_file_location('q',sys.argv[1])
q=importlib.util.module_from_spec(spec); spec.loader.exec_module(q)
q.enable_subreaper()
code='import os,time\\nif os.fork()==0:\\n os.setsid()\\n if os.fork()==0: time.sleep(60)\\n os._exit(0)\\nos._exit(0)'
subprocess.run([sys.executable,'-c',code],check=True)
deadline=time.monotonic()+2
while len(q.descendants(q.process_identity(os.getpid()))) < 2 and time.monotonic()<deadline: time.sleep(.01)
receipts=q.cleanup_adopted()
assert receipts, 'no adopted grandchild captured'
try: os.waitpid(-1,os.WNOHANG)
except ChildProcessError: pass
else: raise AssertionError('adopted child was not reaped')
'''
        subprocess.run([sys.executable, '-c', script, str(RUNNER)], check=True, timeout=6)


class FinalIntegrityTests(unittest.TestCase):
    def process(self, returncode=None):
        identity = dict(pid=99999999, start='1', exe='/owned/test', state='S', ppid=1, session=99999999)
        process = Mock(qualification_identity=identity)
        process.poll.return_value = returncode
        process.wait.return_value = -signal.SIGTERM
        process.qualification_tree.sample.return_value = [identity]
        return process

    def test_stop_rejects_process_that_already_crashed(self):
        process = self.process(-signal.SIGSEGV)
        with patch.object(q, 'process_identity', side_effect=FileNotFoundError):
            with self.assertRaises(q.InvalidEvidence):
                q.stop_process(process)

    def test_stop_rejects_unexpected_exit_after_term(self):
        process = self.process()
        process.wait.return_value = -signal.SIGKILL
        with patch.object(q, 'process_identity', side_effect=[process.qualification_identity,
                FileNotFoundError(), FileNotFoundError()]):
            with self.assertRaisesRegex(q.InvalidEvidence, 'unexpected controlled-stop exit'):
                q.stop_process(process)

    def test_stop_rejects_kill_fallback_even_with_zero_returncode(self):
        process = self.process()
        process.wait.return_value = 0
        identity = process.qualification_identity
        with patch.object(q, 'process_identity', side_effect=[identity, identity,
                FileNotFoundError(), FileNotFoundError()]), patch.object(q.os, 'kill'), \
                patch.object(q.time, 'monotonic', side_effect=[0, 7, 7, 8]):
            with self.assertRaisesRegex(q.InvalidEvidence, 'SIGKILL fallback'):
                q.stop_process(process)

    def test_stop_accepts_live_identity_and_expected_exit(self):
        for returncode in (0, -signal.SIGTERM):
            process = self.process()
            process.wait.return_value = returncode
            with patch.object(q, 'process_identity', side_effect=[process.qualification_identity,
                    FileNotFoundError(), FileNotFoundError()]):
                q.stop_process(process)
            process.qualification_tree.close.assert_called_once()

    def test_stop_preserves_primary_and_observer_failure(self):
        process = self.process(-signal.SIGSEGV)
        process.qualification_tree.close.side_effect = q.InvalidEvidence('observer survived')
        with patch.object(q, 'process_identity', side_effect=FileNotFoundError):
            with self.assertRaises(q.InvalidEvidence) as raised:
                q.stop_process(process)
        self.assertIn('exited before controlled stop', str(raised.exception))
        self.assertIn('observer survived', str(raised.exception))

    def test_final_logs_reject_crash_written_during_reap(self):
        with tempfile.TemporaryDirectory() as name:
            path = Path(name) / 'service.log'
            for marker in (b'panic', b'FATAL', b'segfault', b'Segmentation fault'):
                path.write_bytes(b'started\n' + marker + b': final writer failure\n')
                with self.subTest(marker=marker), self.assertRaises(q.InvalidEvidence):
                    q.verify_final_logs([path])
            path.write_bytes(b'normal shutdown\n')
            q.verify_final_logs([path])

    def test_final_inventory_rejects_unknown_duplicate_or_mutated_records(self):
        original = completion()
        events = decision_pair(event())
        probe = dict(transaction_id='q1-p1', kind='p1', status=403, upstream_headers=0,
            evidence=q.probe_evidence('q1-p1', [original], events))
        result = dict(probes=[probe])
        origin = SimpleNamespace(observations={})
        q.reconcile_records(result, origin, {'q1-p1': 'p1'}, [original], events)
        for records in ([original, original], [original, completion('q1-unknown')],
                [dict(original, request_header_count=6)]):
            with self.subTest(records=records), self.assertRaises(q.InvalidEvidence):
                q.reconcile_records(result, origin, {'q1-p1': 'p1'}, records, events)
        with self.assertRaises(q.InvalidEvidence):
            q.reconcile_records(result, origin, {'q1-p1': 'p1'}, [original],
                [dict(events[0], timestamp='2026-10-03T01:02:04Z'), events[1]])
        for changed in (events + [events[1]], events + [event('q1-foreign')]):
            with self.assertRaises(q.InvalidEvidence):
                q.reconcile_records(result, origin, {'q1-p1': 'p1'}, [original], changed)

    def test_each_ordinary_and_boundary_probe_reuses_final_oracle(self):
        kinds = ('allow', 'p1', 'p2', 'p3', 'p4', 'empty', 'limit', *q.BOUNDARY_KINDS)
        attempted = {f'q1-case-{index}': kind for index, kind in enumerate(kinds)}
        records = [completion(identifier) for identifier in attempted]
        probes = [dict(transaction_id=identifier, kind=kind, status=200, upstream_headers=0,
            evidence=q.probe_evidence(identifier, records, [])) for identifier, kind in attempted.items()]
        with patch.object(q, 'verify_probe') as verify:
            q.reconcile_records(dict(probes=probes), SimpleNamespace(observations={}), attempted, records, [])
        self.assertEqual(verify.call_count, len(kinds))
        self.assertEqual([call.args[-1] for call in verify.call_args_list], list(kinds))

    def test_selected_snapshot_cannot_be_mutated_by_live_records(self):
        original = completion()
        selected = q.probe_evidence('q1-p1', [original], [])
        original['request_header_count'] = 9
        self.assertEqual(selected['completions'][0]['request_header_count'], 5)

    def test_cleanup_keeps_primary_and_multiple_cleanup_failures(self):
        result = dict(passed=True, errors=['primary request failure'], gates={'G9': 'passed'})
        q.fail_cleanup(result, 'unexpected process exit')
        q.fail_cleanup(result, 'fatal final log')
        self.assertEqual(result['errors'], ['primary request failure', 'unexpected process exit', 'fatal final log'])
        self.assertFalse(result['passed'])
        self.assertFalse(result['cleanup_passed'])

    def test_final_inventory_requires_every_attempted_probe(self):
        with self.assertRaises(q.InvalidEvidence):
            q.reconcile_records(dict(probes=[]), SimpleNamespace(observations={}),
                {'q1-p1': 'p1'}, [completion()], decision_pair(event()))

    def test_final_inventory_checks_late_cancel_unavailable_and_malformed(self):
        origin = SimpleNamespace(observations={}, lock=threading.Lock(), body_receipts={}, unattributed=0)
        probe = dict(transaction_id='q1-unavailable', kind='unavailable', status=500,
            upstream_headers=0, evidence=q.probe_evidence('q1-unavailable', [], []))
        q.reconcile_records(dict(probes=[probe]), origin, {'q1-unavailable': 'unavailable'}, [], [])
        with self.assertRaises(q.InvalidEvidence):
            q.reconcile_records(dict(probes=[probe]), origin, {'q1-unavailable': 'unavailable'},
                [completion('q1-unavailable')], [])
        receipt = dict(closed=True, status=None, valid_headers=False, headers={},
            response_bytes=0, header_bytes=0, body_bytes=0)
        result = dict(probes=[], malformed_rejection=receipt)
        q.reconcile_records(result, origin, {'q1-invalid': 'malformed'}, [], [])
        with self.assertRaises(q.InvalidEvidence):
            q.reconcile_records(result, origin, {'q1-invalid': 'malformed'}, [completion('q1-invalid')], [])
        cancel = completion('q1-cancel', 'grpc_context_canceled_unattributed')
        cancel.update(request_body_bytes=2, request_body_chunks=1, response_header_count=5,
            response_body_bytes=1, response_body_chunks=1)
        origin.observations['q1-cancel'] = 1
        probe = dict(transaction_id='q1-cancel', kind='cancel', client_partial_bytes=1,
            evidence=q.probe_evidence('q1-cancel', [cancel], [cancel_event()]))
        q.reconcile_records(dict(probes=[probe]), origin, {'q1-cancel': 'cancel'}, [cancel], [cancel_event()])
        with self.assertRaises(q.InvalidEvidence):
            q.reconcile_records(dict(probes=[probe]), origin, {'q1-cancel': 'cancel'}, [cancel, cancel], [])


class MalformedRejectionTests(unittest.TestCase):
    def test_oracle_read_reset_or_ssl_error_still_attempts_same_service_recovery(self):
        identity = dict(pid=123, start='1', exe='/owned/service', state='S')
        for error in (ConnectionResetError('reset while reading'), q.ssl.SSLError('TLS alert')):
            with self.subTest(error=error):
                result = dict(passed=True, errors=[], probes=[], gates={'G5': 'not_run'})
                recovery = Mock(return_value=dict(kind='allow', status=200))
                current = dict(identity, state='R')
                with patch.object(q, 'read_malformed_response', side_effect=error):
                    q.run_malformed_recovery(result, lambda: q.read_malformed_response(None), recovery,
                        identity, lambda: current)
                recovery.assert_called_once_with()
                self.assertFalse(result['passed'])
                self.assertEqual(result['gates']['G5'], 'failed')
                self.assertTrue(result['recovery_passed'])
                self.assertEqual(result['probes'][0]['status'], 200)

    def test_recovery_failure_or_process_replacement_cannot_pass_g5(self):
        identity = dict(pid=123, start='1', exe='/owned/service')
        for recovery, current in [(Mock(side_effect=OSError('followup failed')), identity),
            (Mock(return_value=dict(kind='allow', status=200)), dict(identity, start='2'))]:
            with self.subTest(current=current):
                result = dict(passed=True, errors=[], probes=[], gates={'G5': 'not_run'})
                identity_reader = Mock(return_value=current)
                q.run_malformed_recovery(result, lambda: None, recovery, identity, identity_reader)
                recovery.assert_called_once_with()
                identity_reader.assert_called_once_with()
                self.assertFalse(result['passed'])
                self.assertFalse(result['recovery_passed'])
                self.assertEqual(result['gates']['G5'], 'failed')

    def observe(self, chunks):
        chunks = list(chunks)
        def receive(_size):
            value = chunks.pop(0) if chunks else b''
            if isinstance(value, Exception):
                raise value
            return value
        return q.read_malformed_response(SimpleNamespace(settimeout=lambda _timeout: None, recv=receive))

    def verify(self, receipt, completions=None, events=None, origin=None):
        origin = origin or SimpleNamespace(lock=threading.Lock(), observations={}, body_receipts={}, unattributed=0)
        q.verify_malformed_rejection(receipt, 'q1-invalid', completions or [], events or [], origin)

    def test_fragmented_http400_is_fully_observed(self):
        receipt = self.observe([b'HT', b'TP/1.1 400 Bad Request\r\nContent-L',
            b'ength: 0\r\nConnection: close\r\n\r\n', b''])
        self.verify(receipt)
        self.assertEqual(receipt['status'], 400)
        self.assertTrue(receipt['closed'])
        self.assertEqual(receipt['body_bytes'], 0)

    def test_exact_zero_byte_close_is_valid_pre_evaluation_rejection(self):
        receipt = self.observe([b''])
        self.verify(receipt)
        self.assertIsNone(receipt['status'])
        self.assertEqual((receipt['response_bytes'], receipt['header_bytes'], receipt['body_bytes']), (0, 0, 0))
        for origin in [SimpleNamespace(lock=threading.Lock(), observations={'q1-invalid': 1}, body_receipts={}, unattributed=0),
            SimpleNamespace(lock=threading.Lock(), observations={}, body_receipts={}, unattributed=1)]:
            with self.assertRaises(q.InvalidEvidence):
                self.verify(receipt, origin=origin)
        with self.assertRaises(q.InvalidEvidence):
            self.verify(receipt, completions=[completion('q1-invalid')])
        with self.assertRaises(q.InvalidEvidence):
            self.verify(receipt, events=[event('q1-invalid')])

    def test_zero_close_cannot_accept_timeout_partial_reply_or_inconsistent_receipt(self):
        for chunks in ([TimeoutError()], [b'H'], [b'HTTP/1.1 400'], [b'malformed reply']):
            with self.subTest(chunks=chunks):
                with self.assertRaises(q.InvalidEvidence):
                    self.verify(self.observe(chunks))
        clean = self.observe([b''])
        for key, value in [('response_bytes', False), ('header_bytes', 1), ('body_bytes', 1),
            ('status', 200), ('headers', {'connection': 'close'}), ('valid_headers', True), ('closed', False)]:
            with self.subTest(key=key):
                corrupt = dict(clean)
                corrupt[key] = value
                with self.assertRaises(q.InvalidEvidence):
                    self.verify(corrupt)

    def test_failclosed_oracle_rejects_wrong_status_incomplete_or_open_connection(self):
        for chunks in ([b'HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n'],
            [b'HTTP/1.1 403 Forbidden\r\nContent-Length: 0\r\n\r\n'],
            [b'HTTP/1.1 400 Bad Request\r\n'],
            [b'HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\n\r\n', TimeoutError()],
            [b'HTTP/1.1 400 Bad Request\r\nContent-Length: 2\r\n\r\nx'],
            [b'HTTP/1.1 400 Bad Request\r\nTransfer-Encoding: chunked\r\n\r\n0\r\n\r\n']):
            with self.subTest(chunks=chunks):
                with self.assertRaises(q.InvalidEvidence):
                    self.verify(self.observe(chunks))

    def test_rejection_must_precede_common_extproc_and_origin_evaluation(self):
        receipt = self.observe([b'HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\n\r\n'])
        with self.assertRaises(q.InvalidEvidence):
            self.verify(receipt, completions=[completion('q1-invalid')])
        with self.assertRaises(q.InvalidEvidence):
            self.verify(receipt, events=[event('q1-invalid')])
        origin = SimpleNamespace(lock=threading.Lock(), observations={'q1-invalid': 1}, body_receipts={}, unattributed=0)
        with self.assertRaises(q.InvalidEvidence):
            self.verify(receipt, origin=origin)

    def test_only_zero_processing_unattributed_cancellation_is_permitted(self):
        record = completion()
        record.pop('transaction_id')
        record.update(request_header_count=0, close_reason='grpc_context_canceled_unattributed')
        q.validate_completion(record)
        for key, value in [('request_header_count', 1), ('request_body_bytes', 1),
            ('late_action', 'log_only'), ('close_reason', 'processor_error')]:
            with self.subTest(key=key):
                corrupt = dict(record)
                corrupt[key] = value
                with self.assertRaises(q.InvalidEvidence):
                    q.validate_completion(corrupt)


class CorrelationTests(unittest.TestCase):
    def test_real_allow_completion_oracle_rejects_origin_503_artifact(self):
        record = completion('q1-allow', 'response_end_of_stream')
        record.update(request_header_count=8, request_body_chunks=1, request_body_bytes=2,
            response_header_count=3, response_body_chunks=1, response_body_bytes=2)
        q.verify_probe('q1-allow', 200, 1, [record], [], 'allow')
        record.update(response_body_bytes=95, late_action='log_only', close_reason='processor_error')
        with self.assertRaises(q.InvalidEvidence):
            q.verify_probe('q1-allow', 200, 1, [record], [], 'allow')

    def test_missing_request_headers(self):
        record = completion()
        record['request_header_count'] = 0
        with self.assertRaises(q.InvalidEvidence):
            q.verify_probe('q1-p1', 403, 0, [record], decision_pair(event()), 'p1')

    def test_contradictory_semantics(self):
        for key, value in [('event', 'cleanup'), ('status', 'error'), ('action', 'allow'),
            ('http_status', 500), ('cancelled', True), ('upstream_disconnected', True),
            ('body_bytes_seen', 2), ('sequence', 0), ('event_hash', 0)]:
            with self.subTest(key=key):
                record = event()
                record[key] = value
                with self.assertRaises(q.InvalidEvidence):
                    q.verify_probe('q1-p1', 403, 0, [completion()], decision_pair(record), 'p1')

    def test_allow_requires_complete_body_and_response(self):
        record = completion('q1-allow', 'response_end_of_stream')
        with self.assertRaises(q.InvalidEvidence):
            q.verify_probe('q1-allow', 200, 1, [record], [], 'allow')
        record.update(request_body_bytes=2, request_body_chunks=1, response_header_count=5,
            response_body_bytes=2, response_body_chunks=1)
        q.verify_probe('q1-allow', 200, 1, [record], [], 'allow')
        with self.assertRaises(q.InvalidEvidence):
            q.verify_probe('q1-allow', 200, 1, [record], [event('q1-allow')], 'allow')

    def test_p1_exact(self):
        observed = q.verify_probe('q1-p1', 403, 0, [completion()], decision_pair(event()), 'p1')
        self.assertEqual(observed['upstream_headers'], 0)

    def test_p2_exact_engine_host_pair(self):
        records = decision_pair(event('q1-p2', '1900002', 'request_body'))
        q.verify_probe('q1-p2', 403, 0, [completion('q1-p2')], records, 'p2')

    def test_engine_host_pair_rejects_broken_link_and_changed_semantics(self):
        for change in ('hash', 'rule', 'body', 'action', 'engine_visible', 'extra'):
            with self.subTest(change=change):
                records = decision_pair(event())
                if change == 'hash':
                    records[1]['previous_event_hash'] = 999
                elif change == 'rule':
                    records[0]['rule_id'] = '1900002'
                elif change == 'body':
                    records[0]['body_bytes_seen'] = 1
                elif change == 'action':
                    records[0]['actual_action'] = 'allow'
                elif change == 'engine_visible':
                    records[0]['visible_http_status'] = 403
                else:
                    records.append(dict(records[1]))
                with self.assertRaises(q.InvalidEvidence):
                    q.verify_probe('q1-p1', 403, 0, [completion()], records, 'p1')

    def test_native_limit_terminal_with_completion_and_no_rule_id(self):
        record = event('q1-limit', '', 'request_body', 413)
        record.update(event='MSCONN_EVENT_BODY_LIMIT', message_id='MSCONN_EVENT_BODY_LIMIT',
            http_status=413, body_bytes_seen=33, body_bytes_inspected=0, body_limit_outcome='reject',
            sequence=1, previous_event_hash=0)
        complete = completion('q1-limit')
        complete.update(request_body_bytes=33, request_body_chunks=1)
        q.verify_probe('q1-limit', 413, 0, [complete], [record], 'limit')

    def test_p2_header_dispatch_is_failure(self):
        with self.assertRaises(q.InvalidEvidence):
            q.verify_probe('q1-p2', 403, 1, [completion('q1-p2')],
                decision_pair(event('q1-p2', '1900002', 'request_body')), 'p2')

    def test_cross_request_rule_correlation(self):
        with self.assertRaises(q.InvalidEvidence):
            q.verify_probe('q1-p1', 403, 0, [completion()], decision_pair(event('q1-other')), 'p1')

    def test_rule_mismatch(self):
        with self.assertRaises(q.InvalidEvidence):
            q.verify_probe('q1-p1', 403, 0, [completion()], decision_pair(event(rule='1900002')), 'p1')

    def test_duplicate_completion(self):
        with self.assertRaises(q.InvalidEvidence):
            q.verify_probe('q1-p1', 403, 0, [completion(), completion()], decision_pair(event()), 'p1')

    def test_duplicate_host_action(self):
        with self.assertRaises(q.InvalidEvidence):
            q.verify_probe('q1-p1', 403, 0, [completion()], [event(), event()], 'p1')

    def test_post_commit_deny_rejected(self):
        record = event()
        record['response_committed'] = True
        with self.assertRaises(q.InvalidEvidence):
            q.verify_probe('q1-p1', 403, 0, [completion()], decision_pair(record), 'p1')

    def test_payload_field_rejected(self):
        record = event()
        record['request_body'] = 'payload'
        with self.assertRaises(q.InvalidEvidence):
            q.validate_common(record)

    def test_boolean_counter_rejected(self):
        record = completion()
        record['request_body_bytes'] = True
        with self.assertRaises(q.InvalidEvidence):
            q.validate_completion(record)

    def test_wrong_engine_rejected(self):
        record = completion()
        record['evaluation_mode'] = 'passthrough_nonpromoted'
        with self.assertRaises(q.InvalidEvidence):
            q.validate_completion(record)

    def test_bad_timestamp_rejected(self):
        record = event()
        record['timestamp'] = 'yesterday'
        with self.assertRaises(q.InvalidEvidence):
            q.validate_common(record)

    def test_impossible_calendar_timestamp_rejected(self):
        record = event()
        record['timestamp'] = '2026-99-03T01:02:03Z'
        with self.assertRaises(q.InvalidEvidence):
            q.validate_common(record)

    def test_later_phase_before_p1_rejected(self):
        earlier = event(phase='response_headers')
        earlier['sequence'] = 1
        later = event()
        later['sequence'] = 2
        with self.assertRaises(q.InvalidEvidence):
            q.verify_probe('q1-p1', 403, 0, [completion()], [earlier, later], 'p1')

    def test_p4_safe(self):
        record = event('q1-p4', '1900004', 'response_body', 200)
        record.update(actual_action='log_only', response_committed=True, late_intervention=True,
            transport_result='log_only', body_bytes_seen=16, body_bytes_inspected=16,
            response_started=True, headers_sent=True, body_started=True, late_intervention_mode='safe')
        complete = completion('q1-p4', 'response_end_of_stream')
        complete['late_action'] = 'log_only'
        q.verify_probe('q1-p4', 200, 1, [complete], decision_pair(record), 'p4')

    def test_p4_allows_only_exact_safe_late_transition(self):
        host = event('q1-p4', '1900004', 'response_body', 200)
        host.update(actual_action='log_only', response_committed=True, response_started=True,
            headers_sent=True, body_started=True, late_intervention=True, late_intervention_mode='safe',
            transport_result='log_only', body_bytes_seen=16, body_bytes_inspected=16)
        complete = completion('q1-p4', 'response_end_of_stream')
        complete['late_action'] = 'log_only'
        for target, key, value in [(0, 'late_intervention', True), (0, 'late_intervention_mode', 'safe'),
            (1, 'late_intervention_mode', 'strict'), (1, 'late_intervention_mode', 'off'),
            (1, 'content_type', 'modified'), (1, 'body_started', False)]:
            with self.subTest(target=target, key=key):
                records = decision_pair(dict(host))
                records[target][key] = value
                with self.assertRaises(q.InvalidEvidence):
                    q.verify_probe('q1-p4', 200, 1, [complete], records, 'p4')

    def test_p4_without_commit_rejected(self):
        record = event('q1-p4', '1900004', 'response_body', 200)
        record.update(actual_action='log_only', late_intervention=True, transport_result='log_only',
            body_bytes_seen=16, body_bytes_inspected=16)
        complete = completion('q1-p4', 'response_end_of_stream')
        complete['late_action'] = 'log_only'
        with self.assertRaises(q.InvalidEvidence):
            q.verify_probe('q1-p4', 200, 1, [complete], decision_pair(record), 'p4')

    def test_serial_parallel_counter_rejected(self):
        origin = SimpleNamespace(parallel_seen=4, peak=1, barrier_passes=4, barrier_errors=0, inflight=0)
        with self.assertRaises(q.InvalidEvidence):
            q.verify_parallel(origin)

    def test_parallel_barrier_errors_rejected(self):
        origin = SimpleNamespace(parallel_seen=4, peak=4, barrier_passes=3, barrier_errors=1, inflight=0)
        with self.assertRaises(q.InvalidEvidence):
            q.verify_parallel(origin)

    def test_actual_four_way_overlap(self):
        origin = SimpleNamespace(parallel_seen=4, peak=4, barrier_passes=4, barrier_errors=0, inflight=0)
        self.assertEqual(q.verify_parallel(origin)['peak'], 4)

    def test_cleanup_failure_invalidates_pass(self):
        result = dict(passed=True, cleanup_passed=True, gates={'G9': 'passed'}, errors=[])
        q.fail_cleanup(result, 'handler survived')
        self.assertFalse(result['passed'])
        self.assertFalse(result['cleanup_passed'])
        self.assertEqual(result['gates']['G9'], 'failed')

    def test_actual_cleanup_failure_invalidates_claimed_gates(self):
        result = dict(passed=True, cleanup_passed=True, errors=[], gates={
            'G1': 'pins_verified_build_provenance_not_proven', 'G2': 'passed',
            'G3': 'passed', 'G4': 'selected_cases_passed_boundaries_incomplete',
            'G5': 'framing_recovery_passed_other_failures_not_proven',
            'G6': 'passed', 'G8': 'not_run', 'G9': 'passed'})
        q.fail_cleanup(result, 'backend observation changed after probe completion')
        self.assertFalse(result['passed'])
        for gate in ('G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G9'):
            self.assertEqual(result['gates'][gate], 'failed')
        self.assertEqual(result['gates']['G8'], 'not_run')

    def test_streamed_p2_missing_eos_fails_attribution_but_preserves_cleanup(self):
        result = dict(passed=True, cleanup_passed=True, errors=[], probes=[], gates={
            'G1': 'pins_verified_build_provenance_not_proven', 'G2': 'passed', 'G3': 'passed',
            'G4': 'selected_cases_passed_boundaries_incomplete', 'G5': 'not_run',
            'G6': 'not_run', 'G9': 'cleanup_passed_catalog_gaps_recorded'})
        origin = SimpleNamespace(lock=threading.Lock(), observations={'q1-p2': 1},
            header_arrivals=1, unattributed=0, body_receipts={}, framing_errors=[])
        origin.verify_attribution = lambda: q.Origin.verify_attribution(origin)
        q.reconcile_origin(result, origin, {'q1-p2': 'p2'})
        self.assertFalse(result['passed'])
        self.assertTrue(result['cleanup_passed'])
        self.assertEqual(result['gates']['G3'], 'failed')
        self.assertEqual(result['gates']['G2'], 'failed')
        self.assertEqual(result['gates']['G4'], 'failed')
        self.assertEqual(result['gates']['G1'], 'pins_verified_build_provenance_not_proven')
        self.assertEqual(result['gates']['G9'], 'cleanup_passed_catalog_gaps_recorded')
        self.assertIn('backend headers have no complete body/EOS receipt', result['errors'])

    def test_late_header_dispatch_invalidates_g3_without_cleanup_failure(self):
        result = dict(passed=True, cleanup_passed=True, errors=[], probes=[{
            'transaction_id': 'q1-p2', 'upstream_headers': 0}], gates={
            'G2': 'passed', 'G3': 'passed', 'G4': 'not_run', 'G5': 'not_run',
            'G6': 'not_run', 'G9': 'cleanup_passed_catalog_gaps_recorded'})
        origin = SimpleNamespace(lock=threading.Lock(), observations={'q1-p2': 1},
            header_arrivals=1, unattributed=0, body_receipts={'q1-p2': [dict(
                bytes=16, sha256=hashlib.sha256(b'qualification-p2').hexdigest(), eos=True)]},
            framing_errors=[])
        origin.verify_attribution = lambda: q.Origin.verify_attribution(origin)
        q.reconcile_origin(result, origin, {'q1-p2': 'p2'})
        self.assertFalse(result['passed'])
        self.assertTrue(result['cleanup_passed'])
        self.assertEqual(result['gates']['G3'], 'failed')
        self.assertEqual(result['gates']['G9'], 'cleanup_passed_catalog_gaps_recorded')


if __name__ == '__main__':
    unittest.main()
