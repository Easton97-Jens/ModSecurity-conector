"""A config receipt must survive collection without becoming request proof."""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    'configtest_collection', ROOT / 'ci/runtime/lifecycle/collect-no-crs-source.py')
assert SPEC is not None
assert SPEC.loader is not None
collector = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(collector)


class ConfigtestCollectionTest(unittest.TestCase):
    BUNDLE_FILES = ('nginx-binary', 'nginx-module.so', 'nginx.conf', 'stdout.log', 'stderr.log')

    def collect_bundle(self, row: dict[str, object], root: Path | None) -> dict[str, object]:
        cases, _ = collector.case_row_observations(
            row, 'nginx', {'invalid_boolean': (1, None, 0)}, root, None, None)
        return cases[0]

    def make_bundle(self, root: Path) -> Path:
        bundle = root / 'configtest'
        bundle.mkdir()
        for name in self.BUNDLE_FILES:
            (bundle / name).write_text('unit artifact', encoding='utf-8')
        return bundle

    def test_explicit_contained_bundle_reference_survives_collection(self) -> None:
        with tempfile.TemporaryDirectory(prefix='configtest-collector-') as temporary:
            root = Path(temporary)
            bundle = self.make_bundle(root)
            row = self.row()
            row['artifacts'] = {'configtest_dir': str(bundle)}
            observation = self.collect_bundle(row, root)
            self.assertEqual(observation.get('artifacts'), row['artifacts'])
            self.assertEqual(observation['configtest_receipt'], row['configtest_receipt'])

    def test_bundle_references_require_authority_and_closed_existing_files(self) -> None:
        with tempfile.TemporaryDirectory(prefix='configtest-collector-') as temporary:
            root = Path(temporary)
            bundle = self.make_bundle(root)
            row = self.row()
            row['artifacts'] = {'configtest_dir': str(bundle)}
            with self.assertRaises(ValueError):
                self.collect_bundle(row, None)
            for reference in ('relative/bundle', str(root / 'missing'), str(root.parent),
                              'x' * 4097, 1):
                with self.subTest(reference=reference):
                    row['artifacts'] = {'configtest_dir': reference}
                    with self.assertRaises(ValueError):
                        self.collect_bundle(row, root)
            row['artifacts'] = {'configtest_dir': str(bundle), 'unknown_ref': str(bundle)}
            with self.assertRaises(ValueError):
                self.collect_bundle(row, root)
            row['artifacts'] = {'configtest_dir': str(bundle)}
            alias = root / 'alias'
            alias.symlink_to(bundle, target_is_directory=True)
            row['artifacts'] = {'configtest_dir': str(alias)}
            with self.assertRaises(ValueError):
                self.collect_bundle(row, root)
            row['artifacts'] = {'configtest_dir': str(bundle)}
            for name in self.BUNDLE_FILES:
                with self.subTest(missing=name):
                    artifact = bundle / name
                    artifact.unlink()
                    with self.assertRaises(ValueError):
                        self.collect_bundle(row, root)
                    artifact.symlink_to(bundle / 'not-present')
                    with self.assertRaises(ValueError):
                        self.collect_bundle(row, root)
                    artifact.unlink()
                    artifact.write_text('unit artifact', encoding='utf-8')

    def row(self) -> dict[str, object]:
        return {
            'case_id': 'invalid_boolean', 'status': 'PASS', 'actual_status': 1,
            'live_executed': True, 'run_id': 'unit-configtest',
            'integration_mode': 'native-nginx-http-module',
            'observed_result': 'config_rejected',
            # Unit receipt payload only; full canonical validation is Framework-owned.
            'configtest_receipt': {'operation': 'configtest', 'case_id': 'invalid_boolean'},
        }

    def test_actual_source_receipt_and_identity_survive_without_event(self) -> None:
        row = self.row()
        cases, events = collector.case_row_observations(
            row, 'nginx', {'invalid_boolean': (1, None, 0)}, None, None, None)
        self.assertEqual(len(cases), 1)
        self.assertEqual(events, [])
        observation = cases[0]
        for field in ('configtest_receipt', 'run_id', 'integration_mode', 'observed_result'):
            self.assertEqual(observation.get(field), row[field])
        self.assertEqual(observation['transaction_ids'], [])
        self.assertEqual(observation['observed_rule_ids'], [])
        self.assertIs(observation['event_metadata_verified'], False)
        self.assertNotIn('artifacts', observation)

    def test_artifact_reference_cannot_turn_request_into_configuration_proof(self) -> None:
        row = self.row()
        row['artifacts'] = {'configtest_dir': '/not-authorized'}
        with self.assertRaises(ValueError):
            collector.configtest_source_fields(row, 1)
        del row['configtest_receipt']
        self.assertEqual(collector.configtest_source_fields(row, 0), {})

    def test_config_only_cases_cannot_claim_host_start_or_request(self) -> None:
        cases, _ = collector.case_row_observations(
            self.row(), 'nginx', {'invalid_boolean': (1, None, 0)}, None, None, None)
        self.assertFalse(collector.request_runtime_observed(None, None, cases, False))
        events = {'transaction_ids': [], 'event_metadata_verified': False,
                  'body_payload_absent_from_events': True, 'event_records': 0,
                  'event_validation_errors': [], 'forbidden_event_keys': []}
        payload = collector.collector_payload(
            argparse.Namespace(connector='nginx', stage_rc=0), 'FAIL', False,
            False, None, None, [], False, cases, events)
        self.assertIs(payload['started'], False)
        self.assertIs(payload['requests_sent'], False)
        self.assertEqual(payload['status'], 'FAIL')

    def test_actual_http_case_remains_request_runtime(self) -> None:
        self.assertTrue(collector.request_runtime_observed(
            200, None, [{'case_id': 'allow_without_marker', 'actual_status': 200}], False))


if __name__ == '__main__':
    unittest.main()
