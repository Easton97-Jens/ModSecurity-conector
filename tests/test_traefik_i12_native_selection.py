"""Exact execution selection must not silently expand supplementary stimuli."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock


REPO = Path(__file__).resolve().parents[1]
MODULE = REPO / 'connectors/traefik/harness/i12/native/acceptance_plan.py'
EXTERNAL = Path(os.environ.get('CODEX_TEMP_ROOT', '/var/tmp/codex/ModSecurity-conector'))


class NativeSelectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('native_selection_plan', MODULE)
        cls.plan = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.plan)

    def setUp(self):
        EXTERNAL.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix='native-selection-', dir=EXTERNAL)
        self.addCleanup(self.temporary.cleanup)
        self.source = Path(self.temporary.name) / 'selection.json'
        self.manifest = {
            'cases': [{'id': f'id-{index}', 'key': f'key-{index}'} for index in range(118)],
            'supplementary_executions': [
                {'id': 'id-1', 'key': 'key-1-first'},
                {'id': 'id-1', 'key': 'key-1-second'},
                {'id': 'id-2', 'key': 'key-2-file'}]}

    def select(self, values, kind='keys'):
        self.source.write_text(json.dumps(values) + '\n')
        self.plan.apply_selection(self.manifest, self.source, kind)

    def test_exact_keys_do_not_expand_sibling_supplements(self):
        original = copy.deepcopy(self.manifest)
        self.select(['key-2-file', 'key-1-first', 'key-1'])
        self.assertEqual(self.manifest['selected_keys'], ['key-1', 'key-1-first', 'key-2-file'])
        self.assertEqual(self.manifest['cases'], original['cases'])
        self.assertEqual(len(self.manifest['cases']), 118)
        self.assertEqual(self.manifest['supplementary_executions'], original['supplementary_executions'])
        self.assertEqual(self.manifest['selection_source'], {
            'path': str(self.source), 'sha256': hashlib.sha256(self.source.read_bytes()).hexdigest(),
            'kind': 'keys'})

    def test_original_ids_keep_existing_supplement_expansion(self):
        self.select(['id-2', 'id-1'], kind='ids')
        self.assertEqual(self.manifest['selected_keys'],
                         ['key-1', 'key-2', 'key-1-first', 'key-1-second', 'key-2-file'])
        self.assertEqual(self.manifest['selection_source']['kind'], 'ids')

    def test_original_only_and_supplement_only_are_valid(self):
        for keys in (['key-0'], ['key-1-second']):
            with self.subTest(keys=keys):
                self.select(keys)
                self.assertEqual(self.manifest['selected_keys'], keys)

    def test_invalid_selections_fail_before_modifying_manifest(self):
        for values in ([], {}, None, 'key-0', [0], [True], [[]], [{}], [''],
                       ['key-0', 'key-0'], ['missing'], ['id-1'], ['key-0', 'missing']):
            with self.subTest(values=values):
                before = copy.deepcopy(self.manifest)
                with self.assertRaises(ValueError):
                    self.select(values)
                self.assertEqual(self.manifest, before)

    def test_keys_are_not_accepted_as_original_ids(self):
        with self.assertRaises(ValueError):
            self.select(['key-1-first'], kind='ids')

    def test_duplicate_manifest_keys_fail_closed(self):
        self.manifest['supplementary_executions'][0]['key'] = 'key-1'
        with self.assertRaisesRegex(ValueError, 'keys must be unique'):
            self.select(['key-1'])
        self.assertNotIn('selected_keys', self.manifest)

    def test_malformed_json_and_missing_source_fail_closed(self):
        self.source.write_text('["key-1"')
        with self.assertRaises(ValueError):
            self.plan.apply_selection(self.manifest, self.source, 'keys')
        with self.assertRaises(FileNotFoundError):
            self.plan.apply_selection(self.manifest, self.source.with_name('missing.json'), 'keys')
        self.assertNotIn('selected_keys', self.manifest)

    def test_unknown_selection_kind_fails_closed(self):
        with self.assertRaisesRegex(ValueError, 'unknown selection kind'):
            self.select(['key-1'], kind='other')

    def test_cli_selection_flags_are_mutually_exclusive(self):
        argv = ['acceptance_plan.py', '--inventory', 'inventory.json', '--proposals', 'proposals.json',
                '--framework', 'framework', '--output', 'output.json',
                '--selected-ids', 'ids.json', '--selected-keys', 'keys.json']
        with mock.patch('sys.argv', argv), mock.patch('sys.stderr'):
            with self.assertRaises(SystemExit) as error:
                self.plan.main()
        self.assertEqual(error.exception.code, 2)


if __name__ == '__main__':
    unittest.main()
