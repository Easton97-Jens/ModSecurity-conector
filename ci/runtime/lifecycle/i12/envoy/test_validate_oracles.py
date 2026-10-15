"""Mutation controls for exact original membership and source-only proposals."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('validate_oracles', HERE / 'validate_oracles.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class OracleValidationControls(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(
            prefix='envoy-oracle-controls-',
            dir=os.environ.get('TMPDIR', str(validator.STORAGE_ROOTS[0])))
        self.root = Path(self.temporary.name)
        self.source = self.root / 'source.txt'
        self.source.write_text('symbol boundary\nsecond line\n')
        self.reference = {'path': str(self.source),
            'sha256': hashlib.sha256(self.source.read_bytes()).hexdigest(),
            'line': 1, 'symbol': 'boundary', 'claim': 'Independent fixture source boundary.'}
        self.baseline = {'rows': []}
        self.documents = []
        oracle = {'visible_status': None, 'physical_evidence_not_projection': True}
        for index, (route, (total, selected)) in enumerate(validator.ROUTES.items()):
            records = []
            for number in range(total):
                identity = f'I12::{route}::case-{number}'
                existing = number == 0
                original = {'run_scoped_case_id': identity, 'leg_id': route,
                    'original_oracle_member': number < selected,
                    'original_oracle': copy.deepcopy(oracle),
                    'qualified_host_lifecycle_pass': existing,
                    'oracle_review': {'resolved': existing}}
                self.baseline['rows'].append(original)
                if number < selected:
                    records.append({'run_scoped_case_id': identity, 'route': route,
                        'category': 'FIXTURE_PENDING', 'original_oracle': copy.deepcopy(oracle),
                        'source_refs': [copy.deepcopy(self.reference)], 'effective_oracle': None,
                        'fixture_binding': None, 'lifecycle_qualified': False,
                        'remaining_requirements': ['Exact host lifecycle packet remains required.']})
            row = records[1]
            row.update(category='SOURCE_SEMANTICS_CONFIRMED', effective_oracle={'visible_status': 200},
                fixture_binding={'origin': 'new_task_fixture_binding',
                    'original_id': row['run_scoped_case_id'], 'files': [copy.deepcopy(self.reference)]})
            key = 'records' if index == 0 else 'rows'
            self.documents.append({'route': route, key: records})
        self.paths = [self.root / f'review-{number}.json' for number in range(3)]
        self.write_reviews()

    def tearDown(self):
        self.temporary.cleanup()

    def rows(self, index=0):
        document = self.documents[index]
        return document.get('records', document.get('rows'))

    def write_reviews(self):
        for path, document in zip(self.paths, self.documents):
            path.write_text(json.dumps(document))

    def reject(self, pattern):
        self.write_reviews()
        with self.assertRaisesRegex(ValueError, pattern):
            validator.validate(self.baseline, self.paths)

    def test_normalization_preserves_canonical_inventory_and_separates_proposals(self):
        result = validator.validate(self.baseline, self.paths)
        self.assertEqual((result['original_count'], result['reviewed_count']), (125, 125))
        self.assertEqual((result['canonical_resolved'], result['canonical_open']), (3, 122))
        self.assertEqual(result['proposed_new_source_oracles'], 3)
        self.assertEqual(result['new_lifecycle_pass'], 0)
        self.assertEqual(len(result['normalized_rows']), 125)
        self.assertNotIn('symbol boundary', json.dumps(result))
        self.assertTrue(all(row['lifecycle_qualified'] is False for row in result['normalized_rows']))

    def test_changed_original_id_is_rejected(self):
        self.rows()[0]['run_scoped_case_id'] += '-invented'
        self.reject('membership differs')

    def test_changed_original_oracle_is_rejected(self):
        self.rows()[0]['original_oracle']['visible_status'] = 403
        self.reject('original oracle changed')

    def test_boolean_to_integer_oracle_change_is_not_equal(self):
        self.rows()[0]['original_oracle']['physical_evidence_not_projection'] = 1
        self.reject('original oracle changed')

    def test_row_route_change_is_rejected(self):
        self.rows()[0]['route'] = 'envoy-ext-authz-request'
        self.reject('route membership differs')

    def test_duplicate_original_id_is_rejected(self):
        self.rows().append(copy.deepcopy(self.rows()[0]))
        self.reject('duplicate reviewed original ID')

    def test_missing_route_review_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'all three complete route reviews'):
            validator.validate(self.baseline, self.paths[:2])

    def test_changed_physical_reference_is_rejected_on_fresh_validation(self):
        validator.validate(self.baseline, self.paths)
        self.source.write_text('changed physical bytes\n')
        with self.assertRaisesRegex(ValueError, 'reference SHA256 mismatch'):
            validator.validate(self.baseline, self.paths)

    def test_nested_independent_source_hash_is_verified(self):
        bad = copy.deepcopy(self.reference)
        bad['sha256'] = '0' * 64
        self.rows()[0]['fixture_binding'] = {'origin': 'existing_original_fixture_binding',
            'independent_sources': [bad]}
        self.reject('reference SHA256 mismatch')

    def test_false_lifecycle_claim_and_missing_flag_are_rejected(self):
        for value in (True, None, 0):
            with self.subTest(value=value):
                self.rows()[0]['lifecycle_qualified'] = value
                self.reject('lifecycle_qualified must be explicitly false')

    def test_explicit_host_pass_cannot_hide_behind_false_lifecycle_flag(self):
        self.rows()[0]['outcome'] = 'PASS'
        self.reject('cannot assign host PASS')

    def test_source_line_bounds_and_private_reference_paths_are_enforced(self):
        self.rows()[0]['source_refs'][0]['line'] = 99999
        self.reject('source reference line outside file')
        self.rows()[0]['source_refs'][0]['line'] = 1
        self.rows()[0]['source_refs'][0]['path'] = '/etc/hosts'
        self.reject('outside approved storage')

    def test_source_boundary_category_is_not_counted_as_ready_oracle(self):
        row = self.rows()[2]
        row.update(category='SOURCE_SEMANTICS_CONFIRMED', source_oracle_resolved=False)
        self.write_reviews()
        result = validator.validate(self.baseline, self.paths)
        route = result['routes'][self.documents[0]['route']]
        self.assertEqual(route['proposed_new_source_oracles'], 1)
        self.assertEqual(route['source_boundary_only_ids'], [row['run_scoped_case_id']])

    def test_new_binding_must_name_the_same_original_id(self):
        self.rows()[1]['fixture_binding']['original_id'] += '-other'
        self.reject('fixture binding names a different original ID')

    def test_proposed_oracle_requires_new_explicit_fixture_binding(self):
        self.rows()[1]['fixture_binding'] = None
        self.reject('lacks an explicit new fixture binding')


if __name__ == '__main__':
    unittest.main()
