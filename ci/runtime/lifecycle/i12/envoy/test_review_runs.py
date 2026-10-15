"""Controls for physical summaries; fixtures cannot qualify a hosted case."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('review_runs', HERE / 'review_runs.py')
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)


class ReviewControls(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(
            prefix='envoy-review-', dir=os.environ.get('TMPDIR', tempfile.gettempdir()))
        self.root = Path(self.temporary.name)
        storage = patch.object(review, 'STORAGE', self.root.parent)
        storage.start()
        self.addCleanup(storage.stop)

    def tearDown(self):
        self.temporary.cleanup()

    def write(self, relative, value):
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(value if isinstance(value, bytes) else json.dumps(value).encode())

    def test_partial_backend_request_is_counted_without_completed_receipt(self):
        self.write('backend/1.request-line.raw', b'POST /target HTTP/1.1\r\n')
        self.write('backend/1.parsed-headers.json', [])
        self.write('backend/1.framing-error.json', {'error': 'incomplete'})
        result = review.backend_summary(review.Artifacts(self.root), {'target': 'target', 'neighbor': 'neighbor'})
        self.assertEqual(result['request_count'], 1)
        self.assertEqual(result['completed_receipt_count'], 0)
        self.assertEqual(result['raw_request_role_counts'], {'target': 1})
        self.assertFalse(result['raw_request_lines'][0]['completed_receipt_retained'])
        self.assertTrue(result['raw_request_lines'][0]['framing_error_retained'])

    def test_backend_without_early_line_capture_counts_body_artifact_as_lower_bound(self):
        self.write('backend/1.request-body.raw', b'received')
        result = review.backend_summary(review.Artifacts(self.root), {}, False)
        self.assertEqual(result['request_count'], 1)
        self.assertEqual(result['raw_request_line_count'], 0)
        self.assertEqual(result['completed_receipt_count'], 0)
        self.assertTrue(result['request_count_is_lower_bound'])

    def test_equal_ids_never_join_independent_native_scopes(self):
        rows = []
        for scope in (1, 2):
            rows.extend([
                {'pid': 4, 'allocation_scope_call': scope, 'call': scope, 'sequence': scope,
                 'edge': 'return', 'function': 'runtime_begin_request_stream',
                 'allocation_join_verified': True, 'transaction_id': 'same-id', 'result': 1},
                {'pid': 4, 'allocation_scope_call': scope, 'call': 100 + scope, 'sequence': 10 + scope,
                 'edge': 'enter', 'function': 'native_cleanup'},
                {'pid': 4, 'allocation_scope_call': None, 'call': 100 + scope, 'sequence': 20 + scope,
                 'edge': 'return', 'function': 'native_cleanup'}])
        result = review.native_summary(rows, [])
        self.assertEqual(result['verified_allocation_scope_count'], 2)
        for scope in result['scopes']:
            self.assertEqual(scope['observed_return_counts']['native_cleanup'], 1)
            self.assertEqual(scope['explicit_runtime_eos_handoff_counts'], {})
        self.assertNotIn('same-id', json.dumps(result))

    def test_missing_remote_status_never_becomes_grpc_success(self):
        transport, _, _ = review.parser_modules(None)
        result = transport.terminal({'verified': True, 'actual_pool_request_reset': True,
            'actual_sent_reset_callback': True, 'actual_stream_close': True, 'numeric_actual_close_code': 2})
        self.assertEqual(result['process']['classification'], 'observed_local_reset')
        self.assertIsNone(result['process']['remote_grpc_status'])
        self.assertFalse(result['process']['successful_grpc_completion'])
        self.assertFalse(result['authorization']['successful_grpc_completion'])

    def test_raw_http_framing_is_independent_of_later_tls_failure(self):
        complete = review.raw_response_summary(b'HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n3\r\nabc\r\n0\r\n\r\n')
        self.assertTrue(complete['framing_complete'])
        self.assertEqual(complete['entity_bytes'], 3)
        self.assertEqual(complete['entity_sha256'], hashlib.sha256(b'abc').hexdigest())
        incomplete = review.raw_response_summary(b'HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n3\r\nab')
        self.assertFalse(incomplete['framing_complete'])
        self.assertIsNone(incomplete['entity_bytes'])

    def test_payload_and_opaque_metadata_are_not_emitted(self):
        secret = 'opaque-lease-value-do-not-emit'
        self.write('client/target.body.raw', b'body')
        self.write('client/target.request.raw', b'POST / HTTP/1.1\r\n\r\nrequest')
        self.write('client/target.response.raw', b'HTTP/1.1 403 Blocked\r\n\r\nbody')
        self.write('client/target.receipt.json', {'status': 403, 'request_bytes': 7,
            'request_sha256': hashlib.sha256(b'request').hexdigest(), 'bytes': 4,
            'sha256': '0' * 64, 'headers': [secret], 'opaque_lease': secret})
        artifacts = review.Artifacts(self.root)
        result = review.client_summary(artifacts, 'target')
        self.assertFalse(result['response_body_hash_verified'])
        self.assertEqual(result['raw_http_status'], 403)
        self.assertNotIn(secret, json.dumps(result))
        self.assertIn({'path': 'client/target.body.raw', 'kind': 'receipt_hash_mismatch'}, artifacts.issues)
        self.assertNotIn(secret, json.dumps(review.event_summary([{'outcome': secret}])))

    def test_data_is_not_opened_before_controller_handoff(self):
        self.write('controller-result.json', {'surviving_namespace_pids': [], 'outside_mount_leaks': []})
        (self.root / 'data').mkdir()
        result = review.review_run({'case': {'label': 'case', 'route': 'envoy-ext-proc'},
            'controller_result': {'attempt': str(self.root)}}, None, None)
        self.assertEqual(result['observation_state'], 'no_safe_completed_data_handoff')
        self.assertNotIn('physical_files', result)
        self.assertFalse(result['host_lifecycle_qualified'])

    def test_scoped_measurements_refuse_relabelled_or_substituted_runs(self):
        shape = {'case_id': 'I12-ENVOY-HOST::actual', 'leg': 'envoy-ext-proc', 'parent_sha': 'a' * 40}
        self.write('fixture/shape.json', shape)
        (self.root / 'source').mkdir()
        (self.root / 'binaries').mkdir()
        bindings = []
        for name, target in [('source', '/mnt/src'), ('binaries', '/mnt/artifacts'), ('fixture', '/mnt/fixtures')]:
            files = {str(path.relative_to(self.root / name)): review.digest(path)
                     for path in (self.root / name).rglob('*') if path.is_file()}
            self.write(name + '-ledger.json', {'files': files})
            ledger = self.root / (name + '-ledger.json')
            bindings.append({'source': str(self.root / name), 'target': target,
                'ledger': str(ledger), 'ledger_sha256': review.digest(ledger)})
        self.write('admission.json', {'bindings': bindings})
        self.write('controller-result.json', {'spec_sha256': review.digest(self.root / 'admission.json')})
        self.write('retained-original-ownership.json', {})
        (self.root / 'data').mkdir()
        record = {'case': {'label': 'actual', 'route': 'envoy-ext-proc', 'spec': str(self.root / 'admission.json')},
                  'controller_result': {'attempt': str(self.root)}}
        for changed, parent in [({'label': 'different'}, 'a' * 40),
                                ({'route': 'envoy-ext-authz-request'}, 'a' * 40), ({}, 'b' * 40)]:
            candidate = dict(record, case=dict(record['case'], **changed))
            result = review.review_run(candidate, None, None, parent)
            self.assertEqual(result['observation_state'], 'fixture_identity_mismatch')
            self.assertIsNone(result['route'])
            self.assertNotIn('clients', result)
        self.write('controller-result.json', {'spec_sha256': '0' * 64})
        result = review.review_run(record, None, None, 'a' * 40)
        self.assertEqual(result['observation_state'], 'admission_scope_mismatch')
        self.assertNotIn('clients', result)

    def test_sealed_binding_hash_mismatch_is_reported(self):
        self.write('source/file', b'actual')
        self.write('ledger.json', {'files': {'file': '0' * 64}})
        result = review.binding_summary({'source': str(self.root / 'source'),
            'ledger': str(self.root / 'ledger.json'), 'ledger_sha256': review.digest(self.root / 'ledger.json')})
        self.assertTrue(result['ledger_hash_verified'])
        self.assertFalse(result['all_file_hashes_verified'])
        self.assertEqual(result['mismatched_paths'], ['file'])

    def test_first_technical_cause_preserves_postcommit_original_status(self):
        first = {'event': 'protocol_error', 'phase': 'response_body', 'status': 'error', 'action': 'error',
                 'reason': 'protocol_error', 'http_status': 500, 'original_http_status': 200,
                 'visible_http_status': 200, 'response_committed': True, 'eos_seen': False,
                 'sequence': 1, 'message': 'NEVER_COPY_PAYLOAD'}
        later = dict(first, sequence=2, reason='timeout')
        result = review.event_summary([first, later])
        self.assertEqual(result['first_physical_technical_error']['reason'], 'protocol_error')
        self.assertEqual(result['first_physical_technical_error']['visible_http_status'], 200)
        self.assertTrue(result['first_physical_technical_error']['response_committed'])
        self.assertFalse(result['first_physical_technical_error']['eos_seen'])
        self.assertNotIn('NEVER_COPY_PAYLOAD', json.dumps(result))

    def test_native_limit_and_mime_markers_are_separate_closed_observations(self):
        self.write('native.log', b'Appending request body: 1024 bytes. Limit set to: 1024.000000\n'
                   b'Appending response body: 96 bytes. Limit set to: 1024.000000\n'
                   b'Request body limit is marked to process partial\n'
                   b'Target value: "text/plain; charset=utf-8" (Variable: RESPONSE_HEADERS:content-type)\n'
                   b'Not appending response body. Response Content-Type is application/octet-stream. It is not marked to be inspected.\n'
                   b'NEVER_EMIT_ARBITRARY_PAYLOAD\n')
        result = review.text_log_summary(review.Artifacts(self.root), 'native.log')
        self.assertEqual(result['sdk_request_append_sizes_and_limits'], [{'append_bytes': 1024, 'configured_limit': 1024}])
        self.assertEqual(result['sdk_response_cumulative_sizes_and_limits'], [{'cumulative_bytes': 96, 'configured_limit': 1024}])
        self.assertEqual(result['sdk_limit_action_marker_counts']['request_process_partial'], 1)
        self.assertEqual(result['sdk_limit_action_marker_counts']['request_reject'], 0)
        self.assertEqual(result['sdk_response_utf8_content_type_target_count'], 1)
        self.assertEqual(result['sdk_octet_stream_append_excluded_count'], 1)
        self.assertNotIn('NEVER_EMIT_ARBITRARY_PAYLOAD', json.dumps(result))

    def test_idempotent_finish_calls_do_not_duplicate_completed_transition(self):
        rows = []
        for call, name, before, after in [(1, 'common_complete_phase', 2, 3),
                                           (2, 'common_finish', 3, 3), (3, 'common_finish', 3, 3)]:
            for edge, status in [('enter', before), ('return', after)]:
                rows.append({'pid': 10, 'allocation_scope_call': 2, 'allocation_join_verified': True,
                    'call': call, 'function': name, 'edge': edge, 'result': 0,
                    'contract_state': {'status': status}, 'sequence': len(rows)})
        result = review.native_summary(rows, [])['scopes'][0]
        self.assertEqual(result['observed_return_counts']['common_finish'], 2)
        self.assertEqual(result['completed_transition_count'], 1)


if __name__ == '__main__':
    unittest.main()
