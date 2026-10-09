"""Controlled native collection tests; no NGINX or Framework proof execution."""
import copy
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('native_collection_test', ROOT / 'ci/runtime/lifecycle/collect-no-crs-source.py')
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)
STORAGE = Path('/var/tmp/codex/ModSecurity-conector')


class NativeCollectionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='native-collection-unit-', dir=STORAGE)
        self.addCleanup(self.temporary.cleanup)
        self.authority = Path(self.temporary.name)
        self.bundle = self.authority / 'case'
        self.bundle.mkdir(mode=0o700)
        self.raw = b'{"unit_fixture":true}\n'
        self.receipt = self.bundle / 'source-result.json'
        self.receipt.write_bytes(self.raw)
        self.receipt.chmod(0o600)
        self.row = dict(case_id='invalid_content_length', run_id='unit-native', connector='nginx',
                        operation='native_h1_parser_rejection', integration_mode='native-nginx-http-module',
                        status='NOT_EXECUTED', canonical_status='NOT_EXECUTED', driver_exit_code=0,
                        **{key: 'a' * 40 for key in ('parent_sha', 'framework_sha', 'mrts_sha', 'parent_framework_gitlink')})
        self.row['native_operation_receipt'] = dict(schema_version=1, case_id=self.row['case_id'],
            run_id=self.row['run_id'], operation=self.row['operation'], integration_mode=self.row['integration_mode'],
            bundle_root=str(self.bundle), source_sha256={'parent:ci/runtime/lifecycle/run-nginx-raw-h1.py': 'b' * 64},
            invocations=[dict(name='main', receipt_path='source-result.json', receipt_sha256=hashlib.sha256(self.raw).hexdigest())])

    def collect(self, row=None, authority=None):
        consumed = []
        cases, events = collector.case_row_observations(row or self.row, 'nginx',
            {'invalid_content_length': (400, None, 1)}, None, consumed, None,
            allowed_native_operation_root=authority or self.authority)
        self.assertEqual(events, [])
        self.assertEqual(consumed, [])
        return cases[0]

    def test_cli_has_explicit_optional_native_authority(self):
        args = collector.collector_argument_parser().parse_args(['--connector', 'nginx', '--stage-rc', '0',
            '--framework-root', '/framework', '--catalog', '/catalog', '--output', '/output',
            '--allowed-native-operation-root', str(self.authority)])
        self.assertEqual(args.allowed_native_operation_root, self.authority)

    def test_authority_precedes_identity_and_seal_validation(self):
        # Exercise the public collection seam with simultaneous invalid inputs.
        row = copy.deepcopy(self.row)
        row['connector'] = 'foreign'
        with self.assertRaisesRegex(ValueError, '^native collection requires explicit caller authority$'):
            collector.case_row_observations(row, 'nginx', {}, None, [], None)

    def test_source_hash_unknown_fields_and_missing_seal_are_independent(self):
        for mutation in ('namespace', 'digest', 'unknown', 'missing'):
            row = copy.deepcopy(self.row)
            wrapper = row['native_operation_receipt']
            if mutation == 'namespace':
                wrapper['source_sha256'] = {'foreign:file': 'b' * 64}
            elif mutation == 'digest':
                wrapper['source_sha256'] = {'parent:file': 'invalid'}
            elif mutation == 'unknown':
                wrapper['invocations'][0]['unknown'] = True
            else:
                del wrapper['invocations'][0]['receipt_sha256']
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                self.collect(row)

    def test_original_wrapper_identity_and_raw_survive_without_promotion(self):
        original = copy.deepcopy(self.row)
        result = self.collect()
        self.assertEqual(result, original)
        self.assertEqual(self.row, original)
        self.assertEqual(self.receipt.read_bytes(), self.raw)

    def test_missing_authority_and_foreign_bundle_fail_closed(self):
        with self.assertRaises(ValueError):
            collector.case_row_observations(self.row, 'nginx', {'invalid_content_length': (400, None, 1)}, None, [], None)
        for reference in (str(self.authority), str(self.authority.parent), '/root/git/ModSecurity-conector', '../escape'):
            row = copy.deepcopy(self.row)
            row['native_operation_receipt']['bundle_root'] = reference
            with self.subTest(reference=reference), self.assertRaises(ValueError):
                self.collect(row)

    def test_unknown_wrapper_identity_and_exit_types_fail(self):
        mutations = [('extra', True), ('schema_version', True), ('case_id', 'foreign'),
                     ('operation', 'request_sequence'), ('source_sha256', {'parent:../escape': 'b' * 64})]
        for key, value in mutations:
            row = copy.deepcopy(self.row)
            row['native_operation_receipt'][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.collect(row)
        for value in (True, '0', None):
            row = copy.deepcopy(self.row)
            row['driver_exit_code'] = value
            with self.subTest(exit=value), self.assertRaises(ValueError):
                self.collect(row)

    def test_nonzero_actual_exit_is_retained_as_failure(self):
        row = copy.deepcopy(self.row)
        row['driver_exit_code'] = 7
        result = self.collect(row)
        self.assertEqual(result['driver_exit_code'], 7)
        self.assertEqual(result['status'], 'FAIL')
        self.assertEqual(result['native_operation_receipt'], row['native_operation_receipt'])

    def test_symlinks_unsafe_permissions_and_receipt_seals_fail(self):
        alias = self.authority / 'alias'
        alias.symlink_to(self.bundle, target_is_directory=True)
        row = copy.deepcopy(self.row)
        row['native_operation_receipt']['bundle_root'] = str(alias)
        with self.assertRaises((ValueError, OSError)):
            self.collect(row)
        self.bundle.chmod(0o777)
        with self.assertRaises(ValueError):
            self.collect()
        self.bundle.chmod(0o700)
        self.receipt.write_bytes(b'changed')
        with self.assertRaises(ValueError):
            self.collect()

    def test_duplicate_native_cases_and_duplicate_json_keys_fail(self):
        path = self.authority / 'rows.jsonl'
        line = json.dumps(self.row)
        path.write_text(line + '\n' + line + '\n')
        with self.assertRaises(ValueError):
            collector.case_observations([path], 'nginx', '1100001',
                {'invalid_content_length': (400, None, 1)}, allowed_native_operation_root=self.authority)
        path.write_text(line.replace('"schema_version": 1', '"schema_version": 1, "schema_version": 1') + '\n')
        with self.assertRaises(ValueError):
            collector.case_observations([path], 'nginx', '1100001',
                {'invalid_content_length': (400, None, 1)}, allowed_native_operation_root=self.authority)

    def test_legacy_event_references_never_enter_scrubber(self):
        raw_log = self.bundle / 'phase1-events.jsonl'
        raw_log.write_bytes(b'{"phase":"logging","actual_action":"allow"}\n')
        before = raw_log.read_bytes()
        row = copy.deepcopy(self.row)
        row['decision_log_path'] = str(raw_log)
        row['native_events'] = [{'phase': 'logging', 'actual_action': 'allow'}]
        self.collect(row)
        self.assertEqual(raw_log.read_bytes(), before)

    def test_event_children_are_independent_closed_original_seals(self):
        row = copy.deepcopy(self.row)
        row['case_id'] = 'event_json_limit'
        row['operation'] = 'native_event_boundary_request'
        wrapper = row['native_operation_receipt']
        wrapper.update(case_id=row['case_id'], operation=row['operation'], parent_receipt_path='source-result.json',
                       parent_receipt_sha256=hashlib.sha256(self.raw).hexdigest())
        wrapper['invocations'] = []
        for name, directory in [('at', 'at255'), ('over', 'over256')]:
            child = self.bundle / directory
            child.mkdir(mode=0o700)
            leaf = child / 'source-result.json'
            leaf.write_bytes(self.raw)
            leaf.chmod(0o600)
            wrapper['invocations'].append(dict(name=name, receipt_path=directory + '/source-result.json',
                                              receipt_sha256=hashlib.sha256(self.raw).hexdigest()))
        cases, events = collector.case_row_observations(row, 'nginx', {'event_json_limit': (200, 1100402, 1)},
            None, [], None, allowed_native_operation_root=self.authority)
        self.assertEqual(cases[0], row)
        self.assertEqual(events, [])
        wrapper['invocations'][1]['receipt_path'] = 'at255/source-result.json'
        with self.assertRaises(ValueError):
            collector.case_row_observations(row, 'nginx', {'event_json_limit': (200, 1100402, 1)},
                None, [], None, allowed_native_operation_root=self.authority)

    def test_real_jsonl_catalog_collector_wire_retains_no_events(self):
        catalog = self.authority / 'catalog.json'
        catalog.write_text(json.dumps({'cases': [dict(case_id='invalid_content_length', expected_status=400, phase=1)]}))
        rows = self.authority / 'rows.jsonl'
        rows.write_text(json.dumps(self.row) + '\n')
        args = argparse.Namespace(source_events=[], catalog=catalog, source_results_jsonl=[rows],
                                  connector='nginx', expected_rule_id='1100001', allowed_native_operation_root=self.authority)
        cases, events, source_paths, consumed = collector.collector_cases_and_events(args, self.authority, [])
        self.assertEqual(cases, [self.row])
        self.assertEqual(source_paths, [])
        self.assertEqual(consumed, [])
        self.assertEqual(events['records'], [])
        self.assertEqual(self.receipt.read_bytes(), self.raw)
        raw_log = self.bundle / 'phase1-events.jsonl'
        raw_log.write_bytes(b'{"phase":"logging","actual_action":"allow"}\n')
        before = raw_log.read_bytes()
        args.source_events = [raw_log]
        with self.assertRaises(ValueError):
            collector.collector_cases_and_events(args, self.authority, [])
        self.assertEqual(raw_log.read_bytes(), before)

    def test_original_receipt_symlink_and_hardlink_are_rejected(self):
        target = self.bundle / 'original.json'
        self.receipt.rename(target)
        self.receipt.symlink_to(target)
        with self.assertRaises(OSError):
            self.collect()
        self.receipt.unlink()
        os.link(target, self.receipt)
        with self.assertRaises(ValueError):
            self.collect()

    def test_receipt_fifo_and_oversize_are_rejected_without_reading(self):
        self.receipt.unlink()
        os.mkfifo(self.receipt, 0o600)
        with self.assertRaises(ValueError):
            self.collect()
        self.receipt.unlink()
        self.receipt.write_bytes(self.raw)
        self.receipt.chmod(0o600)
        with self.receipt.open('r+b') as output:
            output.truncate(4 * 1024 * 1024 + 1)
        with self.assertRaises(ValueError):
            self.collect()

    def test_pass_claim_unknown_case_and_mixed_duplicate_do_not_fall_back(self):
        for key, value in [('status', 'PASS'), ('canonical_status', 'PASS'), ('case_id', 'unknown'),
                           ('parent_framework_gitlink', 'short')]:
            row = copy.deepcopy(self.row)
            row[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.collect(row)
        legacy = {'case_id': 'invalid_content_length', 'status': 'NOT_EXECUTED'}
        path = self.authority / 'mixed.jsonl'
        for rows in ((legacy, self.row), (self.row, legacy)):
            path.write_text('\n'.join(json.dumps(row) for row in rows))
            with self.assertRaises(ValueError):
                collector.case_observations([path], 'nginx', '1100001',
                    {'invalid_content_length': (400, None, 1)}, allowed_native_operation_root=self.authority)
