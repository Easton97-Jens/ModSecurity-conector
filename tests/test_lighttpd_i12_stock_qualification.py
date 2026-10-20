"""Boundaries of exact-original Stock fixture and actual typed allocation joins."""
import importlib.util
import json
import os
from pathlib import Path
import socket
import struct
import subprocess
import sys
import tempfile
import threading
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    path = ROOT / 'ci/runtime/lifecycle/i12/lighttpd' / (name + '.py')
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


FIXTURES = load('stock_qualification')
PACKET = load('stock_packet')


class StockOriginalQualificationTests(unittest.TestCase):
    def test_unreviewed_case_cannot_receive_generic_allow_fixture(self):
        with self.assertRaisesRegex(ValueError, 'separately reviewed'):
            FIXTURES.fixture('NEED-invalid-native-return')

    def test_measurement_hash_rejects_outside_source_and_capture_roots(self):
        path = Path('/etc/passwd')
        with self.assertRaisesRegex(ValueError, 'outside declared'):
            PACKET.sha(path)

    def test_report_output_rejects_source_checkout(self):
        path = ROOT / 'not-runtime-evidence.json'
        with self.assertRaisesRegex(ValueError, 'external task root'):
            PACKET.external_path(path)

    def test_native_jsonl_rule_metadata_remains_bound_to_actual_sdk_id(self):
        with tempfile.TemporaryDirectory(prefix='stock-native-json-', dir=FIXTURES.EXTERNAL) as name:
            path = Path(name) / 'audit.jsonl'
            main = json.dumps({'transaction': {'unique_id': 'actual-main',
                'messages': [{'details': {'ruleId': '1100501'}}]}})
            neighbor = json.dumps({'transaction': {'unique_id': 'actual-neighbor',
                'messages': [{'details': {'ruleId': '1100504'}}]}})
            path.write_text(main + '\n' + neighbor + '\n')
            scoped = PACKET.native_audit_for_id(path, 'actual-main')
            self.assertEqual(scoped, [main])
            self.assertTrue(PACKET.native_rule_observed(scoped, 1100501))
            self.assertFalse(PACKET.native_rule_observed(scoped, 1100504))
            self.assertEqual(PACKET.native_audit_for_id(path, None), [])

    def test_spool_exhaustion_is_separate_from_native_limit(self):
        value = FIXTURES.fixture('NEED-resource-exhaustion-technical')
        self.assertTrue(value['spool_probe'])
        self.assertEqual(len(bytes.fromhex(value['request_hex'])), 4096)
        self.assertGreater(4097 + 4096, value['spool_capacity_bytes'])
        self.assertEqual(value['expected_visible_status'], 503)
        self.assertEqual(value['expected_backend_main_count'], 0)

    def test_default_floor_enforcement_uses_actual_product_at_existing_syscall_seam(self):
        if not Path('/usr/include/modsecurity/modsecurity.h').is_file():
            self.skipTest('requires installed native SDK headers')
        with tempfile.TemporaryDirectory(prefix='stock-floor-test-', dir=FIXTURES.EXTERNAL) as name:
            output = Path(name) / 'capture'
            completed = subprocess.run(['rtk', 'proxy', sys.executable, '-B',
                str(ROOT / 'ci/runtime/lifecycle/i12/lighttpd/stock_floor.py'), '--output', str(output)],
                capture_output=True, text=True, timeout=75)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            receipt = json.loads((output / 'receipt.json').read_text())
            self.assertEqual(receipt['compile_exit'], 0, (output / 'compile.stderr').read_text())
            self.assertEqual(receipt['run_exit'], 0, (output / 'run.stderr').read_text())
            observed = receipt['actual_assertion_receipt']
            self.assertEqual(observed['default_reserve'], 67108864)
            self.assertTrue(observed['exact_floor_accept'])
            self.assertTrue(observed['before_floor_reject'])
            self.assertTrue(observed['after_floor_reject_cleanup'])
            self.assertTrue(observed['readmit'])
            self.assertFalse(receipt['host_disk_exhausted'])

    def test_copy_rejects_directory_symlink_without_following(self):
        with tempfile.TemporaryDirectory(prefix='stock-copy-test-', dir=FIXTURES.EXTERNAL) as name:
            root = Path(name)
            (root / 'source').mkdir()
            (root / 'source/alias').symlink_to(ROOT, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, 'source tree alias'):
                FIXTURES.copy_input_tree(root / 'source', root / 'target')

    def test_response_status_survives_actual_tcp_reset_without_hiding_exit(self):
        """An actual TCP reset after complete503 preserves both independent facts."""
        with tempfile.TemporaryDirectory(prefix='stock-client-test-', dir=FIXTURES.EXTERNAL) as name:
            directory = Path(name)
            source = ROOT / 'ci/runtime/lifecycle/i12/lighttpd/stock_raw_client.py'
            client = directory / 'client.py'
            client.write_text(source.read_text().replace("Path('/task/client')", 'Path(' + repr(str(directory / 'receipts')) + ')'))
            (directory / 'lighttpd_capture_response.py').write_text(FIXTURES.response_helper_text())
            listener = socket.socket()
            listener.bind(('127.0.0.1', 0))
            listener.listen(1)
            listener.settimeout(5)
            failures = []

            def reset_after_response():
                try:
                    connection, _address = listener.accept()
                    with connection:
                        request = b''
                        while b'\r\n\r\n' not in request:
                            request += connection.recv(4096)
                        connection.sendall(b'HTTP/1.1 503 Service Unavailable\r\nContent-Length: 0\r\nConnection: close\r\n\r\n')
                        connection.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))
                except Exception as error:
                    failures.append(error)

            worker = threading.Thread(target=reset_after_response)
            worker.start()
            try:
                completed = subprocess.run(['rtk', 'proxy', sys.executable, '-B', str(client),
                    '-sS', '--http1.1', '-D', str(directory / 'headers'), '-X', 'GET',
                    '-o', str(directory / 'body'), '-w', '%{http_code}',
                    f'http://127.0.0.1:{listener.getsockname()[1]}/actual-reset'],
                    env={**os.environ, 'I12_APACHE_CLIENT_TOKEN': 'reset'}, capture_output=True, timeout=10)
            finally:
                listener.close()
                worker.join(timeout=6)
            self.assertFalse(worker.is_alive())
            self.assertEqual(failures, [])
            receipt = json.loads((directory / 'receipts/reset.receipt.json').read_text())
            self.assertEqual(completed.returncode, 1)
            self.assertEqual(completed.stdout, b'503')
            self.assertEqual(receipt['status'], 503)
            self.assertTrue(receipt['tcp_reset_observed'])
            self.assertFalse(receipt['tcp_eof_observed'])
            self.assertEqual(receipt['entity_bytes'], 0)
            self.assertEqual(receipt['error']['type'], 'ConnectionResetError')

    def test_original_streaming_has_large_delayed_body_and_default_resource_contract(self):
        fixture = FIXTURES.fixture('NEED-request-streaming')
        self.assertTrue(fixture['delayed_request'])
        self.assertGreater(len(bytes.fromhex(fixture['request_hex'])), 8192)
        self.assertEqual(fixture['spool_capacity_bytes'], 256 * 1024 * 1024)
        self.assertEqual(fixture['spool_free_reserve_bytes'], 64 * 1024 * 1024)
        self.assertIsNone(fixture['native_request_append_count'])

    def test_missing_and_present_content_type_are_distinct_fixture_inputs(self):
        missing = FIXTURES.fixture('NEED-request-content-type-missing')
        present = FIXTURES.fixture('NEED-request-content-type-present')
        self.assertIsNone(missing['request_content_type'])
        self.assertEqual(present['request_content_type'], 'text/plain')
        self.assertNotEqual(missing['path'], present['path'])

    def test_stale_retained_source_fails_closed(self):
        with self.assertRaisesRegex(ValueError, 'retained source boundary'):
            FIXTURES.replace_once('two two', 'two', 'three')

    def test_main_allocation_joins_actual_constructor_in_main_window(self):
        rows = [self.constructor(9, 101), self.constructor(50, 201)]
        self.assertEqual(PACKET.selected_scope(rows, 100, 150), 9)

    def test_equal_ids_cannot_replace_typed_native_join(self):
        row = self.constructor(9, 101)
        row.update(allocation_join_verified=False, canonical_transaction_id='same-id')
        with self.assertRaisesRegex(ValueError, 'typed main allocation'):
            PACKET.selected_scope([row], 100, 150)

    def test_multiple_main_allocations_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'one typed main allocation'):
            PACKET.selected_scope([self.constructor(9, 101), self.constructor(50, 102)], 100, 150)

    def test_failed_constructor_absence_requires_actual_output_scalar(self):
        row = self.constructor(9, 101)
        row.update(result=0, allocation_join_verified=False)
        self.assertIsNone(PACKET.failed_constructor_absence([row], 9))
        row.update(output_argument_present=True, actual_output_handle_present=False)
        actual = PACKET.failed_constructor_absence([row], 9)
        self.assertIsNone(actual['actual_returned_handle'])
        self.assertFalse(actual['allocation_join_verified'])
        self.assertEqual(actual['nested_actual_native_ids'], [])
        row['actual_output_handle_present'] = True
        self.assertIsNone(PACKET.failed_constructor_absence([row], 9))

    def test_abort_fixture_exceeds_actual_stock_read_chunk(self):
        fixture = FIXTURES.fixture('NEED-rst-disconnect')
        self.assertGreater(len(bytes.fromhex(fixture['response_hex'])), 8192)
        self.assertEqual(fixture['backend_split_bytes'], 8192)
        self.assertEqual(fixture['client_abort_mode'], 'reset')
        self.assertEqual(fixture['expected_response_finalizations'], 0)

    def test_incomplete_fixture_does_not_expect_native_eos(self):
        fixture = FIXTURES.fixture('NEED-missing-eos')
        self.assertTrue(fixture['backend_incomplete'])
        self.assertEqual(fixture['expected_client_exit'], 1)
        self.assertEqual(fixture['expected_response_finalizations'], 0)

    def test_existing_boundary_faults_preserve_distinct_commit_expectations(self):
        before = FIXTURES.fixture('transaction_begin_failure_cleanup')
        finish = FIXTURES.fixture('finish_failure_propagation')
        self.assertEqual(before['diagnostic_boundary_fault'], 'request_headers_error')
        self.assertEqual(before['expected_visible_status'], 500)
        self.assertEqual(before['expected_backend_main_count'], 0)
        self.assertEqual(finish['diagnostic_boundary_fault'], 'logging_error')
        self.assertEqual(finish['expected_visible_status'], 200)
        self.assertEqual(finish['expected_backend_main_count'], 1)
        self.assertTrue(before['preserve_original_oracle'])
        self.assertTrue(finish['preserve_original_oracle'])

    def test_event_limit_relocation_remains_valid_launcher_python(self):
        source = FIXTURES._launch_caller_and_transport(
            "config = 'default_error_status=502'", 'event_json_limit',
            {'configured_event_json_limit': 512})
        namespace = {}
        exec(compile(source, '<bounded-event-config>', 'exec'), namespace)
        self.assertEqual(namespace['config'].splitlines(),
                         ['default_error_status=502', 'max_event_json_bytes=512'])

    @staticmethod
    def constructor(scope, time):
        return {'function': 'runtime_begin_request_stream', 'edge': 'return',
                'allocation_scope_call': scope, 'allocation_join_verified': True, 'monotonic_ns': time}


if __name__ == '__main__':
    unittest.main()
