"""Negative evidence tests for the distinct native middleware campaign."""
import importlib.util
from email.message import Message
from pathlib import Path
import socket
import sys
import tempfile
import unittest
from unittest import mock
import json
import signal
import threading
import time
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('native_qualification_test',
    ROOT / 'connectors/traefik/harness/traefik_native_qualification.py')
runner = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = runner
SPEC.loader.exec_module(runner)


class EventsTest(unittest.TestCase):
    def abort_events(self):
        events = self.events()[1]
        events.append(dict(connector='traefik', integration_mode='native-traefik-middleware',
            transaction_id='tnq-1-abort', sequence=1, truncated=False,
            previous_event_hash=4, event_hash=5, event='protocol_error',
            message_id='MSCONN_EVENT_PROTOCOL_ERROR', phase='request_headers',
            status='error', action='log_only', requested_action='log_only',
            actual_action='log_only', http_status=500, original_http_status=0,
            visible_http_status=0, transport_result='', rule_id='',
            response_started=False, response_committed=False, headers_sent=False,
            body_started=False, body_bytes_seen=0, body_bytes_inspected=0,
            late_intervention=False, body_truncated=False, connection_aborted=False,
            client_disconnected=False, upstream_disconnected=False, cancelled=False, eos_seen=False))
        return events

    def verify_abort(self, events):
        runner.verify_events(events, self.events()[0], runner.native.STANDALONE_RULE_IDS,
            'tnq-1-p4', 'tnq-1-abort')

    def test_exact_abort_protocol_error(self):
        self.verify_abort(self.abort_events())

    def test_abort_event_mutations_rejected(self):
        for key, value in self.abort_events()[-1].items():
            with self.subTest(key=key):
                events = self.abort_events()
                events[-1][key] = (1 << 64) if key == 'event_hash' else not value if type(value) is bool else value + 1 if type(value) is int else value + '-wrong'
                with self.assertRaises(runner.InvalidEvidence):
                    self.verify_abort(events)

    def test_missing_or_extra_abort_event_rejected(self):
        with self.assertRaises(runner.InvalidEvidence):
            self.verify_abort(self.events()[1])
        events = self.abort_events()
        events.append(dict(events[-1], sequence=2, previous_event_hash=5, event_hash=6))
        with self.assertRaises(runner.InvalidEvidence):
            self.verify_abort(events)

    def test_unknown_allow_event_rejected(self):
        events = self.events()[1]
        events.append(dict(events[0], transaction_id='unknown', actual_action='allow',
            sequence=1, previous_event_hash=4, event_hash=5))
        with self.assertRaises(runner.InvalidEvidence):
            self.verify(events)

    def events(self):
        probes = [{'transaction_id': 'tnq-1-p1', 'kind': 'p1', 'status': 403}]
        events = []
        for token, phase, rule, status, action in (
            ('tnq-1-p1', 'request_headers', '1000001', 403, 'deny'),
            ('tnq-1-p4', 'response_body', '1000004', 200, 'log_only')):
            for host in (False, True):
                p4 = phase == 'response_body'
                events.append({'connector': 'traefik', 'integration_mode': 'native-traefik-middleware',
                    'sequence': 2 if host else 1, 'truncated': False, 'transaction_id': token,
                    'previous_event_hash': len(events), 'event_hash': len(events) + 1,
                    'event': 'MSCONN_EVENT_RESPONSE_BLOCKED' if p4 else 'MSCONN_EVENT_REQUEST_BLOCKED',
                    'message_id': 'MSCONN_EVENT_RESPONSE_BLOCKED' if p4 else 'MSCONN_EVENT_REQUEST_BLOCKED',
                    'phase': phase, 'rule_id': rule, 'transport_result': action if host and action == 'log_only' else 'http_status' if host else '',
                    'requested_action': 'deny', 'http_status': 403,
                    'status': 'blocked',
                    'visible_http_status': status if host else 200 if phase == 'response_body' else 0,
                    'original_http_status': 200 if p4 else 0,
                    'action': 'deny', 'actual_action': action if host else 'deny',
                    'body_bytes_seen': 55 if p4 else 0,
                    'body_bytes_inspected': 55 if p4 else 0,
                    'response_started': p4, 'response_committed': p4,
                    'headers_sent': p4, 'body_started': p4,
                    'late_intervention': p4 and host,
                    'body_truncated': False, 'connection_aborted': False,
                    'client_disconnected': False, 'upstream_disconnected': False,
                    'cancelled': False, 'eos_seen': False,
                    **({'late_intervention_mode': 'safe'} if p4 and host else {})})
        return probes, events

    def verify(self, events):
        probes, _ = self.events()
        runner.verify_events(events, probes, runner.native.STANDALONE_RULE_IDS, 'tnq-1-p4')

    def test_complete_native_chain(self):
        self.verify(self.events()[1])

    def overlapping_events(self):
        ordered = self.events()[1]
        events = [ordered[index] for index in (0, 2, 1, 3)]
        for index, event in enumerate(events):
            event.update(previous_event_hash=index, event_hash=index + 1)
        return events

    def test_overlapping_token_sequences_are_independent(self):
        events = self.overlapping_events()
        self.assertEqual([event['sequence'] for event in events], [1, 1, 2, 2])
        self.verify(events)

    def test_token_sequence_gap_rejected(self):
        events = self.overlapping_events()
        events[2]['sequence'] = 3
        with self.assertRaises(runner.InvalidEvidence):
            self.verify(events)

    def test_token_sequence_replay_rejected(self):
        events = self.overlapping_events()
        events[2]['sequence'] = 1
        with self.assertRaises(runner.InvalidEvidence):
            self.verify(events)

    def test_token_local_hash_relink_contradicts_global_runtime_chain(self):
        events = self.overlapping_events()
        events[2]['previous_event_hash'] = events[0]['event_hash']
        with self.assertRaises(runner.InvalidEvidence):
            self.verify(events)

    def test_invalid_or_missing_hash_rejected(self):
        for value in (None, True, -1, 1 << 64):
            with self.subTest(value=value):
                events = self.events()[1]
                events[1]['event_hash'] = value
                with self.assertRaises(runner.InvalidEvidence):
                    self.verify(events)

    def test_duplicate_receipt(self):
        events = self.events()[1]
        duplicate = dict(events[-1], sequence=4)
        with self.assertRaises(runner.InvalidEvidence):
            self.verify(events + [duplicate])

    def test_missing_decision(self):
        with self.assertRaises(runner.InvalidEvidence):
            self.verify(self.events()[1][1:])

    def test_foreign_forwardauth_profile(self):
        events = self.events()[1]
        events[0]['integration_mode'] = 'forwardAuth+observer'
        with self.assertRaises(runner.InvalidEvidence):
            self.verify(events)

    def test_wrong_rule_status_and_sequence(self):
        for key, value in (('rule_id', '1000002'), ('rule_id', 1000001), ('visible_http_status', 200),
            ('sequence', 0), ('truncated', True)):
            with self.subTest(key=key):
                events = self.events()[1]
                events[1][key] = value
                with self.assertRaises(runner.InvalidEvidence):
                    self.verify(events)

    def test_unattributed_intervention(self):
        events = self.events()[1]
        events[0]['transaction_id'] = 'unrelated'
        with self.assertRaises(runner.InvalidEvidence):
            self.verify(events)

    def test_engine_decision_cannot_hide_failed_action_or_transport(self):
        for key, value in (('requested_action', 'allow'), ('actual_action', 'error'),
            ('actual_action', 'log_only'), ('http_status', 200),
            ('visible_http_status', 403), ('transport_result', 'garbage'),
            ('transport_result', 'pending'), ('transport_result', None)):
            with self.subTest(key=key, value=value):
                events = self.events()[1]
                events[0][key] = value
                with self.assertRaises(runner.InvalidEvidence):
                    self.verify(events)

    def test_host_transport_must_match_actual_phase_action(self):
        for position, transport in ((1, 'log_only'), (3, 'http_status')):
            events = self.events()[1]
            events[position]['transport_result'] = transport
            with self.assertRaises(runner.InvalidEvidence):
                self.verify(events)

    def test_error_or_missing_status_rejected_for_decision_and_host(self):
        for position in range(4):
            for status in ('error', 'allowed', None):
                with self.subTest(position=position, status=status):
                    events = self.events()[1]
                    events[position]['status'] = status
                with self.assertRaises(runner.InvalidEvidence):
                    self.verify(events)

    def test_canonical_event_semantics_are_not_mutable(self):
        fields = {
            'event', 'message_id', 'action', 'original_http_status',
            'response_started', 'response_committed', 'headers_sent',
            'body_started', 'body_bytes_seen', 'body_bytes_inspected',
            'late_intervention', 'body_truncated', 'connection_aborted',
            'client_disconnected', 'upstream_disconnected', 'cancelled',
            'eos_seen',
        }
        for position in range(4):
            for key in fields:
                with self.subTest(position=position, key=key):
                    events = self.events()[1]
                    value = events[position][key]
                    events[position][key] = not value if type(value) is bool else value + 1 if type(value) is int else value + '-wrong'
                    with self.assertRaises(runner.InvalidEvidence):
                        self.verify(events)

    def test_late_intervention_mode_is_exact_and_only_on_p4_host_receipt(self):
        events = self.events()[1]
        events[-1]['late_intervention_mode'] = 'strict'
        with self.assertRaises(runner.InvalidEvidence):
            self.verify(events)
        for position in range(3):
            with self.subTest(position=position):
                events = self.events()[1]
                events[position]['late_intervention_mode'] = 'safe'
                with self.assertRaises(runner.InvalidEvidence):
                    self.verify(events)

    def test_p2_and_p3_body_commit_contracts_are_exact(self):
        for kind, phase, rule, original, body in (
            ('p2', 'request_body', '1000002', 0, len(runner.native.P2_BODY)),
            ('p3', 'response_headers', '1000003', 200, 0),
        ):
            probes = [{'transaction_id': f'tnq-1-{kind}', 'kind': kind, 'status': 403}]
            events = self.events()[1]
            response_event = kind == 'p3'
            for host, event in enumerate(events[:2]):
                event.update(transaction_id=f'tnq-1-{kind}', phase=phase,
                    rule_id=rule,
                    event='MSCONN_EVENT_RESPONSE_BLOCKED' if response_event else 'MSCONN_EVENT_REQUEST_BLOCKED',
                    message_id='MSCONN_EVENT_RESPONSE_BLOCKED' if response_event else 'MSCONN_EVENT_REQUEST_BLOCKED',
                    original_http_status=original,
                    visible_http_status=403 if host else (200 if response_event else 0),
                    transport_result='http_status' if host else '',
                    body_bytes_seen=body, body_bytes_inspected=body,
                    response_started=False, response_committed=False,
                    headers_sent=False, body_started=False,
                    late_intervention=False)
            runner.verify_events(events, probes, runner.native.STANDALONE_RULE_IDS,
                'tnq-1-p4')
            for position in range(2):
                for key in ('body_bytes_seen', 'body_bytes_inspected',
                    'response_started', 'response_committed', 'headers_sent',
                    'body_started', 'eos_seen'):
                    with self.subTest(kind=kind, position=position, key=key):
                        mutated = [dict(event) for event in events]
                        value = mutated[position][key]
                        mutated[position][key] = not value if type(value) is bool else value + 1
                        with self.assertRaises(runner.InvalidEvidence):
                            runner.verify_events(mutated, probes,
                                runner.native.STANDALONE_RULE_IDS,
                                'tnq-1-p4')


class ProbeReceiptTest(unittest.TestCase):
    class Response:
        def __init__(self, payload, *, status=200, length=None, version=11,
                transfer_encoding=None, closed=True):
            self.status = status
            self.version = version
            self.payload = payload
            self.headers = Message()
            if length is not None:
                self.headers['Content-Length'] = length
            if transfer_encoding is not None:
                self.headers['Transfer-Encoding'] = transfer_encoding
            self._closed = closed

        def read(self, _limit):
            return self.payload

        def isclosed(self):
            return self._closed

    class FragmentedResponse(Response):
        def __init__(self, payload, chunk_size):
            super().__init__(payload, length=str(len(payload)))
            self.chunk_size = chunk_size
            self.offset = 0

        def read(self, limit):
            size = min(limit, self.chunk_size, len(self.payload) - self.offset)
            result = self.payload[self.offset:self.offset + size]
            self.offset += size
            return result

        def isclosed(self):
            return self.offset == len(self.payload)

    @staticmethod
    def connection(response):
        return SimpleNamespace(request=mock.Mock(), getresponse=mock.Mock(return_value=response))

    @staticmethod
    def raw_probe(response_wire, *, token='tnq-1-allow', kind='allow', expected=200):
        listener = socket.socket()
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(('127.0.0.1', 0))
        listener.listen(1)
        listener.settimeout(3)
        errors = []

        def serve():
            try:
                client, _ = listener.accept()
                with client:
                    client.settimeout(3)
                    request = bytearray()
                    while b'\r\n\r\n' not in request:
                        chunk = client.recv(4096)
                        if not chunk:
                            raise AssertionError('client request ended before headers')
                        request.extend(chunk)
                    header, _, body = bytes(request).partition(b'\r\n\r\n')
                    match = __import__('re').search(rb'\r\nContent-Length: ([0-9]+)\r\n', b'\r\n' + header + b'\r\n')
                    if match is None:
                        raise AssertionError('client request omitted canonical Content-Length')
                    expected = int(match.group(1))
                    while len(body) < expected:
                        chunk = client.recv(expected - len(body))
                        if not chunk:
                            raise AssertionError('client request body truncated')
                        body += chunk
                    client.sendall(response_wire)
            except Exception as error:  # captured for the owning test thread
                errors.append(error)
            finally:
                listener.close()

        server = threading.Thread(target=serve)
        server.start()
        connection = runner.http.client.HTTPConnection('127.0.0.1',
            listener.getsockname()[1], timeout=3)
        caught = None
        result = None
        try:
            result = runner.probe(connection, token, kind, expected)
        except Exception as error:
            caught = error
        finally:
            connection.close()
            server.join(4)
        if server.is_alive():
            raise AssertionError('raw response server did not stop')
        if errors:
            raise errors[0]
        if caught is not None:
            raise caught
        return result

    def test_allow_receipt_requires_exact_payload_and_framing(self):
        payload = b'native-traefik-first-chunk\nnative-traefik-final-chunk\n'
        response = self.Response(payload, length=str(len(payload)))
        receipt = runner.probe(self.connection(response), 'tnq-1-allow', 'allow', 200)
        self.assertEqual(receipt['bytes'], len(payload))
        self.assertEqual(receipt['content_length'], len(payload))
        self.assertTrue(receipt['complete_eos'])
        self.assertEqual(receipt['body_sha256'], runner.ALLOW_PAYLOAD_SHA256)

    def test_allow_receipt_accepts_legal_fragmented_socket_reads(self):
        payload = b'native-traefik-first-chunk\nnative-traefik-final-chunk\n'
        response = self.FragmentedResponse(payload, 5)
        receipt = runner.probe(self.connection(response), 'tnq-1-allow', 'allow', 200)
        self.assertEqual(receipt['bytes'], len(payload))
        self.assertTrue(receipt['complete_eos'])

    def test_real_wire_accepts_empty_deny_body(self):
        response = (b'HTTP/1.1 403 Forbidden\r\nContent-Length: 0\r\n'
            b'Connection: close\r\n\r\n')
        receipt = self.raw_probe(response, token='tnq-1-p1', kind='p1',
            expected=403)
        self.assertEqual(receipt['bytes'], 0)
        self.assertEqual(receipt['content_length'], 0)
        self.assertTrue(receipt['complete_eos'])

    def test_truncated_or_mutated_allow_payload_is_rejected(self):
        payload = b'native-traefik-first-chunk\nnative-traefik-final-chunk\n'
        for response in (
            self.Response(b'x', length='55', closed=False),
            self.Response(b'x' * len(payload), length=str(len(payload))),
        ):
            with self.subTest(length=response.headers['Content-Length']), \
                    self.assertRaises(runner.InvalidEvidence):
                runner.probe(self.connection(response), 'tnq-1-allow', 'allow', 200)

    def test_ambiguous_or_noncanonical_response_framing_is_rejected(self):
        payload = b'native-traefik-first-chunk\nnative-traefik-final-chunk\n'
        duplicate = self.Response(payload, length=str(len(payload)))
        duplicate.headers['Content-Length'] = str(len(payload))
        cases = (
            self.Response(payload),
            duplicate,
            self.Response(payload, length='054'),
            self.Response(payload, length=str(len(payload)), transfer_encoding='identity'),
            self.Response(payload, length=str(len(payload)), version=10),
            self.Response(payload, length=str(len(payload)), closed=False),
            self.Response(payload, length='65537'),
        )
        for response in cases:
            with self.subTest(headers=list(response.headers.raw_items()), version=response.version), \
                    self.assertRaises(runner.InvalidEvidence):
                runner.probe(self.connection(response), 'tnq-1-allow', 'allow', 200)

    def test_real_wire_requires_crlf_and_control_free_canonical_headers(self):
        payload = b'native-traefik-first-chunk\nnative-traefik-final-chunk\n'
        canonical = (b'HTTP/1.1 200 OK\r\nContent-Length: 54\r\n'
            b'Connection: close\r\n\r\n' + payload)
        self.assertEqual(self.raw_probe(canonical)['body_sha256'],
            runner.ALLOW_PAYLOAD_SHA256)
        malformed = (
            b'HTTP/1.1 200 OK\nContent-Length: 54\nConnection: close\n\n' + payload,
            canonical.replace(b'Connection: close', b'X-Bad: before\x00after'),
            canonical.replace(b'Connection: close', b'X-Bad: before\x7fafter'),
            canonical.replace(b'Connection: close', b' X-Obs-Fold: bad'),
            canonical.replace(b'Content-Length: 54', b'Content-Length : 54'),
            b'HTTP/1.1 100 Continue\r\n\r\nHTTP/1.1 200 OK\n'
                b'Content-Length: 54\nConnection: close\n\n' + payload,
            b'HTTP/1.1 100 Continue\r\n\r\n' +
                canonical.replace(b'Connection: close', b'X-Bad: before\x00after'),
        )
        for response in malformed:
            with self.subTest(response=response[:80]), \
                    self.assertRaises((runner.InvalidEvidence,
                        runner.http.client.HTTPException)):
                self.raw_probe(response)


class ObserverTest(unittest.TestCase):
    @staticmethod
    def exchange(observer, payload):
        with socket.create_connection(('127.0.0.1', observer.server_port), timeout=2) as connection:
            connection.sendall(payload)
            connection.shutdown(socket.SHUT_WR)
            chunks = bytearray()
            while len(chunks) <= 8192:
                piece = connection.recv(4096)
                if not piece:
                    return bytes(chunks)
                chunks.extend(piece)
            raise AssertionError('fixture response exceeds test bound')

    def test_valid_post_then_malformed_second_request_fails(self):
        observer = runner.Observer(runner.native.UpstreamState())
        response = self.exchange(observer,
            b'POST /native HTTP/1.1\r\nHost: local\r\nContent-Length: 1\r\nX-Request-Id: allow\r\n\r\nx'
            b'MALFORMED SECOND REQUEST\r\n\r\n')
        self.assertIn(b'200 OK', response)
        self.assertEqual(observer.receipts['allow'], {'headers': 1, 'completed': 1})
        with self.assertRaises(runner.InvalidEvidence):
            observer.close_observer()

    def test_first_and_second_eof_terminated_headers_rejected(self):
        valid = b'POST /native HTTP/1.1\r\nHost: local\r\nContent-Length: 0\r\nX-Request-Id: allow\r\n\r\n'
        truncated = b'POST /native HTTP/1.1\r\nHost: local\r\nContent-Length: 0\r\nX-Request-Id: bad\r\n'
        for prefix in (b'', valid):
            with self.subTest(second=bool(prefix)):
                observer = runner.Observer(runner.native.UpstreamState())
                self.exchange(observer, prefix + truncated)
                self.assertNotIn('bad', observer.receipts)
                if prefix:
                    self.assertEqual(observer.receipts['allow']['completed'], 1)
                self.assertIn('truncated upstream request headers', observer.errors)
                with self.assertRaises(runner.InvalidEvidence):
                    observer.close_observer()

    def test_requestline_lf_and_excessive_header_wire_rejected(self):
        for wire in (b'POST /native HTTP/1.1\nHost: local\r\nContent-Length: 0\r\n\r\n',
            b'POST /native HTTP/1.1\r\nHost: local\r\nX-Large: ' + b'x' * 8192 + b'\r\n\r\n'):
            observer = runner.Observer(runner.native.UpstreamState())
            # A bounded rejection can reset a socket with unread excess bytes.
            try:
                self.exchange(observer, wire)
            except ConnectionResetError:
                pass
            self.assertFalse(observer.receipts)
            with self.assertRaises(runner.InvalidEvidence):
                observer.close_observer()

    def test_continuous_header_drip_cannot_extend_absolute_deadline(self):
        for second in (False, True):
            with self.subTest(second=second), mock.patch.object(runner, 'HEADER_DEADLINE_SECONDS', .2):
                observer = runner.Observer(runner.native.UpstreamState())
                connection = runner.http.client.HTTPConnection('127.0.0.1', observer.server_port, timeout=2)
                connection.connect()
                if second:
                    runner.probe(connection, 'allow', 'allow', 200)
                raw = connection.sock
                stop = threading.Event()
                def drip():
                    try:
                        raw.sendall(b'POST /native HTTP/1.1\r\nHost: ')
                        while not stop.wait(.01):
                            raw.sendall(b'x')
                    except OSError:
                        pass
                sender = threading.Thread(target=drip)
                started = time.monotonic()
                sender.start()
                try:
                    try:
                        self.assertEqual(raw.recv(1), b'')
                    except ConnectionResetError:
                        pass
                finally:
                    stop.set()
                    sender.join(1)
                    connection.close()
                self.assertLess(time.monotonic() - started, 1)
                self.assertTrue(observer.errors)
                self.assertTrue(any('timeout' in error or 'deadline' in error for error in observer.errors))
                if second:
                    self.assertEqual(observer.receipts['allow']['completed'], 1)
                with self.assertRaises(runner.InvalidEvidence):
                    observer.close_observer()

    def test_timeout_during_second_request_headers_is_not_silently_consumed(self):
        observer = runner.Observer(runner.native.UpstreamState())
        with mock.patch.object(runner, 'HEADER_DEADLINE_SECONDS', .1), \
            socket.create_connection(('127.0.0.1', observer.server_port), timeout=2) as connection:
            connection.sendall(b'POST /native HTTP/1.1\r\nHost: local\r\nContent-Length: 0\r\n'
                b'X-Request-Id: allow\r\n\r\nPOST /native HTTP/1.1\r\nHost:')
            total = 0
            while total <= 8192:
                chunk = connection.recv(4096)
                if not chunk:
                    break
                total += len(chunk)
            self.assertLessEqual(total, 8192)
        self.assertIn('upstream_request_timeout', observer.errors)
        self.assertEqual(observer.receipts['allow']['completed'], 1)
        with self.assertRaises(runner.InvalidEvidence):
            observer.close_observer()

    def test_invalid_or_incomplete_body_never_completed(self):
        for framing, body in ((b'Content-Length: 2\r\n', b'x'),
            (b'Content-Length: 1\r\nContent-Length: 1\r\n', b'x'),
            (b'Content-Length: 1, 1\r\n', b'x'),
            (b'Transfer-Encoding: chunked\r\n', b'1\r\nx\r\n0\r\n\r\n'),
            (b'Content-Length: 65537\r\n', b''),
            (b'Content-Length: 0\r\nTransfer-Encoding: identity\r\n', b'')):
            with self.subTest(framing=framing):
                observer = runner.Observer(runner.native.UpstreamState())
                self.exchange(observer, b'POST /native HTTP/1.1\r\nHost: local\r\n'
                    b'X-Request-Id: bad\r\n' + framing + b'\r\n' + body)
                self.assertEqual(observer.receipts['bad'], {'headers': 1, 'completed': 0})
                self.assertTrue(observer.errors)
                with self.assertRaises(runner.InvalidEvidence):
                    observer.close_observer()

    def test_response_write_or_flush_failure_never_completed(self):
        original = runner.native.upstream_handler
        for operation in ('write', 'flush', 'short-write'):
            with self.subTest(operation=operation):
                def handler_factory(state):
                    base = original(state)
                    class BrokenResponse(base):
                        def do_POST(handler):
                            writer = handler.wfile
                            handler.wfile = mock.Mock(wraps=writer)
                            if operation == 'short-write':
                                handler.wfile.write.return_value = 0
                            else:
                                getattr(handler.wfile, operation).side_effect = BrokenPipeError('fixture write failed')
                            return super().do_POST()
                    return BrokenResponse
                with mock.patch.object(runner.native, 'upstream_handler', side_effect=handler_factory):
                    observer = runner.Observer(runner.native.UpstreamState())
                self.exchange(observer, b'POST /native HTTP/1.1\r\nHost: local\r\n'
                    b'Content-Length: 1\r\nX-Request-Id: broken\r\n\r\nx')
                self.assertEqual(observer.receipts['broken'], {'headers': 1, 'completed': 0})
                with self.assertRaises(runner.InvalidEvidence):
                    observer.close_observer()

    def test_body_timeout_and_no_progress_rejected(self):
        from email.message import Message
        headers = Message()
        headers['Content-Length'] = '1'
        for error in (TimeoutError('no progress'), OSError('read failed')):
            handler = SimpleNamespace(headers=headers, request_version='HTTP/1.1',
                connection=mock.Mock(gettimeout=lambda: 2), rfile=mock.Mock())
            handler.rfile.read1.side_effect = error
            with self.subTest(error=type(error).__name__), self.assertRaises(runner.native.UpstreamFixtureError):
                runner.native.read_fixture_body(handler)

    def test_p2_and_abort_backend_receipts_rejected(self):
        for token, kind in (('tnq-1-p2', 'p2'), ('tnq-1-abort', 'abort')):
            observer = runner.Observer(runner.native.UpstreamState())
            observer.peak = 4
            observer.receipts[token] = {'headers': 1, 'completed': 1}
            probes = [{'transaction_id': token, 'kind': kind, 'status': 403}] if kind == 'p2' else []
            try:
                with self.assertRaises(runner.InvalidEvidence):
                    runner.verify_receipts(observer, probes, [], 'tnq-1-abort')
            finally:
                with self.assertRaises(runner.InvalidEvidence):
                    observer.close_observer()

    def test_extra_bare_tcp_accept_rejected_after_valid_http(self):
        observer = runner.Observer(runner.native.UpstreamState())
        with runner.closing(runner.http.client.HTTPConnection('127.0.0.1', observer.server_port, timeout=3)) as connection:
            runner.probe(connection, 'tnq-1-allow', 'allow', 200)
        with socket.create_connection(('127.0.0.1', observer.server_port), timeout=2) as connection:
            connection.shutdown(socket.SHUT_WR)
            self.assertEqual(connection.recv(1), b'')
        with self.assertRaises(runner.InvalidEvidence):
            observer.close_observer()

    def test_real_four_client_overlap(self):
        observer = runner.Observer(runner.native.UpstreamState())
        probes = []
        from concurrent.futures import ThreadPoolExecutor
        try:
            def client(number):
                with runner.closing(runner.http.client.HTTPConnection('127.0.0.1', observer.server_port, timeout=3)) as connection:
                    return runner.probe(connection, f'tnq-1-parallel-{number}', 'allow', 200)
            with ThreadPoolExecutor(max_workers=4) as pool:
                futures = [pool.submit(client, number) for number in range(4)]
                self.assertTrue(observer.four.wait(2))
                self.assertEqual(observer.active, 4)
                observer.release.set()
                probes = [future.result() for future in futures]
        finally:
            result = observer.close_observer()
        runner.verify_receipts(observer, probes, [])
        self.assertEqual(result['peak'], 4)
        self.assertEqual(result['queued_accepts'], 0)

    def test_unexpected_backend_is_rejected(self):
        observer = runner.Observer(runner.native.UpstreamState())
        observer.peak = 4
        observer.receipts = {'unexpected': {'headers': 1, 'completed': 1}}
        try:
            with self.assertRaises(runner.InvalidEvidence):
                runner.verify_receipts(observer, [], [])
        finally:
            with self.assertRaises(runner.InvalidEvidence):
                observer.close_observer()

    def test_open_keepalive_socket_is_closed(self):
        observer = runner.Observer(runner.native.UpstreamState())
        connection = socket.create_connection(('127.0.0.1', observer.server_port), timeout=2)
        try:
            connection.sendall(b'POST /native HTTP/1.1\r\nHost: local\r\nContent-Length: 0\r\nX-Request-Id: allow\r\n\r\n')
            self.assertIn(b'200', connection.recv(4096))
            result = observer.close_observer()
            self.assertEqual(result['active'], 0)
            self.assertFalse(observer.connections)
        finally:
            connection.close()

    def test_unexpected_method_fails_cleanup_reconciliation(self):
        observer = runner.Observer(runner.native.UpstreamState())
        with socket.create_connection(('127.0.0.1', observer.server_port), timeout=2) as connection:
            connection.sendall(b'GET /native HTTP/1.1\r\nHost: local\r\n\r\n')
            self.assertEqual(connection.recv(4096), b'')
        with self.assertRaises(runner.InvalidEvidence):
            observer.close_observer()


class AbortClientTest(unittest.TestCase):
    @staticmethod
    def response():
        return b'HTTP/1.1 500 Internal Server Error\r\nContent-Length: 5\r\nConnection: close\r\n\r\nerror'

    def test_exact_500_framed_response(self):
        runner.verify_abort_response(self.response())

    def test_malformed_wrong_status_or_incomplete_abort_response_rejected(self):
        response = self.response()
        for data in (b'', response.replace(b'500', b'200'), response[:-1],
            response.replace(b'Content-Length: 5', b'Content-Length: 5\r\nContent-Length: 5'),
            response.replace(b'Content-Length: 5', b'Content-Length: 5, 5'),
            response.replace(b'Content-Length: 5', b'Transfer-Encoding: chunked'),
            response.replace(b'Connection: close', b'Connection: keep-alive'),
            response + b'extra', response.replace(b'HTTP/1.1', b'HTTP/1.0')):
            with self.subTest(data=data), self.assertRaises(runner.InvalidEvidence):
                runner.verify_abort_response(data)

    def test_abort_probe_requires_closed_socket_and_records_status(self):
        connection = mock.MagicMock()
        connection.__enter__.return_value = connection
        connection.recv.side_effect = [self.response(), b'']
        with mock.patch.object(runner.socket, 'create_connection', return_value=connection):
            receipt = runner.abort_probe(1234, 'tnq-1-abort')
        self.assertEqual(receipt['status'], 500)
        self.assertTrue(receipt['host_closed_connection'])
        self.assertEqual(receipt['response_bytes'], len(self.response()))
        connection.shutdown.assert_called_once_with(socket.SHUT_WR)

    def test_abort_probe_timeout_and_oversize_rejected(self):
        for chunks in ([TimeoutError('not closed')], [b'x' * 65537]):
            connection = mock.MagicMock()
            connection.__enter__.return_value = connection
            connection.recv.side_effect = chunks
            with mock.patch.object(runner.socket, 'create_connection', return_value=connection), \
                self.assertRaises((runner.InvalidEvidence, TimeoutError)):
                runner.abort_probe(1234, 'tnq-1-abort')


class RootTest(unittest.TestCase):
    def test_source_checkout_rejected(self):
        with self.assertRaises(runner.InvalidEvidence):
            runner.private_root(ROOT)

    def test_nonempty_or_public_external_root_rejected(self):
        with tempfile.TemporaryDirectory(dir=runner.EXTERNAL) as directory:
            path = Path(directory)
            path.chmod(0o755)
            with self.assertRaises(runner.InvalidEvidence):
                runner.private_root(path)
            path.chmod(0o700)
            (path / 'foreign').touch()
            with self.assertRaises(runner.InvalidEvidence):
                runner.private_root(path)


class FinalProcessTest(unittest.TestCase):
    def test_abort_identity_ignores_transient_running_sleeping_state(self):
        process = mock.Mock(pid=10, poll=lambda: None)
        running = dict(pid=10, start='123', exe='/bin/host', ppid=1, session=10, state='R')
        with mock.patch.object(runner.linux, 'process_identity', side_effect=[running, dict(running, state='S')]):
            before = [runner.immutable_process_identity(process)]
            runner.verify_abort_processes([process], before)

    def test_abort_changed_start_exe_parent_session_or_dead_process_rejected(self):
        process = mock.Mock(pid=10, poll=lambda: None)
        original = dict(pid=10, start='123', exe='/bin/host', ppid=1, session=10, state='S')
        before = [{key: value for key, value in original.items() if key != 'state'}]
        for key, value in (('pid', 11), ('start', '124'), ('exe', '/bin/other'), ('ppid', 2), ('session', 11)):
            with self.subTest(key=key), mock.patch.object(runner.linux, 'process_identity', return_value=dict(original, **{key: value})), \
                self.assertRaises(runner.InvalidEvidence):
                runner.verify_abort_processes([process], before)
        with self.assertRaises(runner.InvalidEvidence):
            runner.verify_abort_processes([mock.Mock(pid=10, poll=lambda: 0)], before)

    def test_descendant_shutdown_panic_is_scanned_after_adopted_cleanup(self):
        with tempfile.TemporaryDirectory(dir=runner.EXTERNAL) as directory:
            logs = Path(directory)
            log = logs / 'engine.log'
            log.write_text('normal runtime\n')
            artifacts = SimpleNamespace(logs_dir=logs)
            result, errors = {}, []
            def cleanup():
                log.write_text('normal runtime\npanic: adopted child shutdown\n')
                return {'reaped': 1}
            with mock.patch.object(runner.linux, 'cleanup_adopted', side_effect=cleanup):
                runner.reconcile_adopted_and_logs(artifacts, result, errors)
            self.assertEqual(result['adopted_cleanup'], {'reaped': 1})
            self.assertEqual(result['final_fatal_log_lines'], 1)
            self.assertTrue(errors)

    def test_adopted_cleanup_failure_remains_error_and_still_scans_logs(self):
        result, errors = {}, []
        with mock.patch.object(runner.linux, 'cleanup_adopted', side_effect=RuntimeError('survivor')), \
            mock.patch.object(runner, 'fatal_log_count', return_value=1) as scan:
            runner.reconcile_adopted_and_logs(None, result, errors)
        scan.assert_called_once_with(None)
        self.assertEqual(len(errors), 2)
        self.assertIn('survivor', errors[0])

    def test_controlled_success_and_sigterm_are_accepted(self):
        for status in (0, -signal.SIGTERM):
            self.assertEqual(runner.verify_stopped_process(mock.Mock(poll=lambda: status), True), status)

    def test_late_crash_or_forced_kill_is_rejected(self):
        for status in (1, 2, -signal.SIGSEGV, -signal.SIGKILL, None):
            with self.subTest(status=status), self.assertRaises(runner.InvalidEvidence):
                runner.verify_stopped_process(mock.Mock(poll=lambda: status), True)

    def test_exit_before_controlled_stop_is_rejected(self):
        with self.assertRaises(runner.InvalidEvidence):
            runner.verify_stopped_process(mock.Mock(poll=lambda: 0), False)

    def test_final_log_rescan_sees_shutdown_panic(self):
        with tempfile.TemporaryDirectory(dir=runner.EXTERNAL) as directory:
            logs = Path(directory)
            log = logs / 'engine.log'
            log.write_text('normal runtime\n')
            artifacts = SimpleNamespace(logs_dir=logs)
            self.assertEqual(runner.fatal_log_count(artifacts), 0)
            log.write_text('normal runtime\npanic: crash during shutdown\n')
            self.assertEqual(runner.fatal_log_count(artifacts), 1)
            for fatal_line in ('level=fatal msg=shutdown', '{"level":"fatal","msg":"shutdown"}',
                'FATAL shutdown failure', 'fatal error: runtime crash'):
                log.write_text(fatal_line + '\n')
                self.assertEqual(runner.fatal_log_count(artifacts), 1)


class CampaignTest(unittest.TestCase):
    def campaign(self, directory, starts, sources=None):
        args = ['--root', str(directory), '--socket-parent', str(directory.parent / 'uds'),
            '--include', '/not-used']
        for name in ('traefik', 'engine', 'library', 'rules'):
            args += [f'--{name}', '/not-used', f'--{name}-sha256', '0' * 64]
        with mock.patch.object(runner, 'private_root', side_effect=lambda path: path), \
            mock.patch.object(runner.native, 'assert_private_engine_socket_parent'), \
            mock.patch.object(runner.native, 'assert_engine_socket_path_length'), \
            mock.patch.object(runner, 'input_pins', return_value={}), \
            mock.patch.object(runner.linux, 'read_safe', return_value=b'closed rules'), \
            mock.patch.object(runner.linux, 'enable_subreaper'), \
            mock.patch.object(runner, 'source_manifest', side_effect=sources or [{}, {}]), \
            mock.patch.object(runner, 'run_generation', side_effect=starts):
            code = runner.main(args)
        return code, json.loads((directory / 'result.json').read_text())

    @staticmethod
    def start(index, status='PASS'):
        return {'status': status, 'processes': [{'pid': index, 'start': str(index)}]}

    def test_failed_generation_never_promoted(self):
        with tempfile.TemporaryDirectory(dir=runner.EXTERNAL) as directory:
            code, result = self.campaign(Path(directory), [self.start(1), self.start(2, 'FAIL'), self.start(3)])
        self.assertEqual(code, 1)
        self.assertFalse(result['catalog_acceptance'])

    def test_reused_process_generation_rejected(self):
        with tempfile.TemporaryDirectory(dir=runner.EXTERNAL) as directory:
            code, result = self.campaign(Path(directory), [self.start(1)] * 3)
        self.assertEqual(code, 1)
        self.assertEqual(result['status'], 'FAIL')

    def test_changed_source_invalidates_complete_starts(self):
        with tempfile.TemporaryDirectory(dir=runner.EXTERNAL) as directory:
            code, result = self.campaign(Path(directory), [self.start(i) for i in (1, 2, 3)], [{}, {'changed': 'hash'}])
        self.assertEqual(code, 1)
        self.assertFalse(result['inputs_stable'])

    def test_all_starts_pass_diagnostic_only(self):
        with tempfile.TemporaryDirectory(dir=runner.EXTERNAL) as directory:
            code, result = self.campaign(Path(directory), [self.start(i) for i in (1, 2, 3)])
        self.assertEqual(code, 0)
        self.assertFalse(result['catalog_acceptance'])


if __name__ == '__main__':
    unittest.main()
