"""Unsigned batch review controls and opt-in actual private capture regression."""
import importlib.util
import os
from pathlib import Path
import unittest

SOURCE = Path(__file__).resolve().parents[1] / 'ci/runtime/lifecycle/apache-i12/acceptance/review_batch.py'
SPEC = importlib.util.spec_from_file_location('apache_batch_review_test', SOURCE)
REVIEW = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REVIEW)


class BatchReviewTests(unittest.TestCase):
    def test_backend_arrival_and_completion_count_once_including_incomplete_body(self):
        rows = [{'kind': 'request_arrival', 'request_id': 'a', 'uri': '/main', 'monotonic_ns': 10},
                {'kind': 'request', 'request_id': 'a', 'uri': '/main', 'monotonic_ns': 20},
                {'kind': 'request_arrival', 'request_id': 'b', 'uri': '/partial', 'monotonic_ns': 30}]
        actual = REVIEW.backend_arrivals(rows)
        self.assertEqual(len(actual), 2)
        self.assertEqual(actual[0]['monotonic_ns'], 10)
        self.assertEqual(actual[1]['path'], '/partial')
        self.assertIsNone(REVIEW.backend_arrivals(None))
        with self.assertRaises(ValueError):
            REVIEW.backend_arrivals([{'kind': 'request', 'uri': '/unidentified'}])

    def test_socket_commit_requires_timed_principal_and_real_parent_call(self):
        import copy
        identity = {'pid': 100, 'tid': 101, 'socket_inode': 123, 'request_sequence': 1,
                    'request_uri': '/main', 'request_method': 'GET', 'monotonic_ns': 20,
                    'actual_successful_socket_bytes': True, 'invalid': False}
        rows = [dict(identity, kind='request_headers_received'),
                dict(identity, kind='response_headers_sent', monotonic_ns=50, parent_call=7),
                {'kind': 'transport_return', 'pid': 100, 'socket_inode': 123, 'call': 7,
                 'stream_accounted_here': True, 'reported_bytes': 80,
                 'entered_ns': 30, 'return_ns': 45}]
        client = {'path': '/main', 'method': 'GET', 'started_ns': 10, 'completed_ns': 60}
        actual = REVIEW.principal_socket_capture(rows, {'pid': 100, 'tid': 101}, client)
        self.assertEqual(actual['actual_socket_call_brackets'][0]['return_ns'], 45)
        for key, value in (('parent_call', 8), ('socket_inode', 999), ('invalid', True),
                           ('actual_successful_socket_bytes', False), ('monotonic_ns', 61)):
            changed = copy.deepcopy(rows)
            changed[1][key] = value
            with self.subTest(key=key):
                self.assertIsNone(REVIEW.principal_socket_capture(changed, {'pid': 100, 'tid': 101}, client))
        self.assertIsNone(REVIEW.principal_socket_capture(rows, {'pid': 100, 'tid': 102}, client))
        self.assertIsNone(REVIEW.principal_socket_capture(rows + [rows[0]], {'pid': 100, 'tid': 101}, client))

    def test_truncated_response_preserves_200_and_duplicate_headers(self):
        raw = b'HTTP/1.1 200 OK\r\nContent-Length: 17\r\nX-A: one\r\nX-A: two\r\n\r\n'
        parsed = REVIEW.wire_headers(raw)
        self.assertEqual(parsed['status'], 200)
        self.assertEqual(parsed['headers'][-2:], [['X-A', 'one'], ['X-A', 'two']])
        self.assertIsNone(parsed['entity_framing_complete'])

    def test_no_header_or_status_is_invented(self):
        for raw in (b'', b'garbage', b'HTTP/1.1 200 OK\r\nContent-Length: 3\r\n'):
            self.assertIsNone(REVIEW.wire_headers(raw))

    def test_audit_match_uses_native_a_section_not_request_header(self):
        text = ('---first---A--\n[time] actual-native 1 2 3 4\n---first---B--\n'
                'X-I12-ID: neighbor\n---first---H--\n[id "1100201"]\n---first---Z--\n'
                '---second---A--\n[time] neighbor 1 2 3 4\n---second---B--\n'
                'X-I12-ID: actual-native\n---second---Z--\n')
        blocks = REVIEW.audit_records(text, 'actual-native')
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0]['boundary'], 'first')
        self.assertEqual(blocks[0]['physical_rule_ids'], ['1100201'])
        self.assertTrue(blocks[0]['complete_Z_section'])

    def test_missing_case_has_all_shared_fields_and_no_execution_approval(self):
        plan = {'original_id': 'I12::apache-native::unexecuted', 'case_id': 'unexecuted',
                'original_contract': {'expected_oracle': {'visible_status': 403}}, 'execution_kind': 'host_http'}
        packet = REVIEW.empty_packet(plan, 'missing capture')
        self.assertEqual(set(packet['observations']), set(REVIEW.ROLES))
        self.assertTrue(all(row['value'] is None for row in packet['observations'].values()))
        self.assertFalse(packet['execution_observed'])
        self.assertIsNone(packet['reviewed_by'])
        self.assertIsNone(packet['outcome'])

    def test_symbolic_git_head_is_resolved_to_commit(self):
        binding = os.environ.get('APACHE_I12_SOURCE_METADATA')
        if not binding:
            self.skipTest('Opt-in sealed metadata regression')
        value = REVIEW.resolved_metadata_head({'/mnt/git': {'source': binding}}, '/mnt/git')
        self.assertRegex(value, r'^[0-9a-f]{40}$')

    def test_actual_three_capture_reference_and_constructor_regression(self):
        attempt = os.environ.get('APACHE_I12_SMOKE_ATTEMPT')
        spec = os.environ.get('APACHE_I12_SMOKE_SPEC')
        if not attempt or not spec:
            self.skipTest('Opt-in authorized private native capture regression')
        packets = REVIEW.extract_all(attempt, spec)
        self.assertEqual(len(packets), 155)
        observed = [packet for packet in packets if packet['execution_observed']]
        self.assertEqual(len(observed), 3)
        for packet in observed:
            with self.subTest(case=packet['run_scoped_case_id']):
                self.assertEqual(set(packet['observations']), set(REVIEW.ROLES))
                self.assertIsNone(packet['reviewed_by'])
                self.assertIsNone(packet['outcome'])
                self.assertFalse(packet['full_lifecycle_qualified'])
                self.assertFalse(packet['oracle_evaluated'])
                native = packet['observations']['native_transaction_id']['value']['transaction_id']
                calls = packet['observations']['native_api_returns']['value']
                constructors = [row for row in calls if row['function'] == 'native_new_with_id']
                self.assertEqual([row['transaction_id'] for row in constructors], [native])
                self.assertTrue(packet['review_checks']['successful_actual_allocation_join'])
                self.assertTrue(packet['review_checks']['sdk_and_observed_module_loaded'])
                for name, item in packet['observations'].items():
                    REVIEW.REVIEW.LEDGER.SHARED.measurement(name, item, Path('unsigned-unit-review'))
        reject = next(packet for packet in observed if packet['actual_scenario_variant'] == 'phase4_body_reject')
        fields = reject['observations']
        self.assertEqual(fields['client_exit']['value'], 1)
        self.assertEqual(fields['client_headers']['value']['status'], 200)
        self.assertIsNone(fields['transport_framing']['value'])
        self.assertIsNone(fields['client_bytes']['value']['response_entity'])
        self.assertEqual(fields['backend_request_count']['value']['main'], 1)


if __name__ == '__main__':
    unittest.main()
