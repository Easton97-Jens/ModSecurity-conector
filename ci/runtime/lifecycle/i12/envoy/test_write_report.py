"""Controls for route-specific report accounting and original-ID bindings."""
import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('write_report', HERE / 'write_report.py')
writer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(writer)


class ReportControls(unittest.TestCase):
    def test_compact_serialization_preserves_unknown_and_nested_evidence(self):
        data = {'status': 'PARTIAL', 'original_ids': [{'id': 'one', 'grpc_status': None}],
                'host_measurements': [{'backend': {'request_count': 0, 'request_count_is_lower_bound': True}}],
                'qualified_originals': [], 'counts': {'open': 119}}
        self.assertEqual(json.loads(writer.encode_report(data)), data)

    def test_existing_qualification_cannot_be_counted_as_new(self):
        baseline = {'routes': {'request': {'existing_pass_ids': ['same']}}}
        with self.assertRaisesRegex(ValueError, 'existing qualification'):
            writer.add_route_results({}, baseline, [{'route': 'request', 'run_scoped_case_id': 'same'}])

    def test_retaken_original_cannot_claim_sibling_route(self):
        item = {'route': 'response'}
        sources = {'original': {'route': 'request'}}
        with self.assertRaisesRegex(ValueError, 'sibling original ID'):
            writer.add_retaken_ids(item, ['original'], sources, {})

    def test_retaken_original_requires_physical_review_hash(self):
        item = {'route': 'request', 'oracle_review_sha256': 'wrong'}
        sources = {'original': {'route': 'request', 'review_file': '/approved/review.json'}}
        with patch.object(writer, 'reference', return_value={'sha256': 'expected'}):
            with self.assertRaisesRegex(ValueError, 'independently verified review'):
                writer.add_retaken_ids(item, ['original'], sources, {})


    def supplement_fixture(self):
        path = Path('/approved/supplement.json')
        origin = {'path': '/approved/original.json', 'sha256': 'old', 'bytes': 20}
        reviewed = {'path': str(path), 'sha256': 'supplement', 'bytes': 30}
        source_rows = {'original': {'route': 'response', 'review_file': origin['path']},
                       'different': {'route': 'response', 'review_file': origin['path']}}
        supplement = {'schema': 'supplement', 'route': 'response', 'original_id': 'original',
            'review_file': reviewed, 'origin_review': origin,
            'normalized_rows': [{'run_scoped_case_id': 'original', 'route': 'response'}],
            'canonical_resolution_changed': False, 'new_lifecycle_pass': 0}
        refs = {origin['path']: origin, str(path): reviewed}
        return path, source_rows, supplement, refs

    def test_default_empty_supplements_leave_report_structure_unchanged(self):
        data = {'physical_inputs': {}, 'source_oracle_progress': {'reviewed_count': 125}}
        self.assertEqual(writer.add_oracle_supplements(data, [], {}, {}), {})
        self.assertEqual(data, {'physical_inputs': {}, 'source_oracle_progress': {'reviewed_count': 125}})

    def test_supplement_keeps_original_counts_and_requires_fresh_validation(self):
        path, sources, supplement, refs = self.supplement_fixture()
        original_review = {'reviewed_count': 125, 'new_source_proposals': 33}
        data = {'physical_inputs': {}, 'source_oracle_progress': dict(original_review)}
        with patch.object(writer.validate_oracles, 'validate_supplement', return_value=supplement) as validate:
            with patch.object(writer, 'reference', side_effect=lambda p: refs[str(p)]):
                allowed = writer.add_oracle_supplements(data, [path], original_review, sources)
        validate.assert_called_once_with(path, original_review)
        self.assertEqual(allowed, {'original': {'supplement'}})
        self.assertEqual(data['source_oracle_progress'], original_review)
        self.assertNotIn('normalized_rows', data['oracles_supplements'][0])
        self.assertFalse(data['oracles_supplements'][0]['canonical_resolution_changed'])
        self.assertEqual(data['oracles_supplements'][0]['new_lifecycle_pass'], 0)

    def test_supplement_rejects_different_normalized_original_id(self):
        path, sources, supplement, refs = self.supplement_fixture()
        supplement['normalized_rows'][0]['run_scoped_case_id'] = 'different'
        with patch.object(writer, 'reference', side_effect=lambda p: refs[str(p)]):
            with self.assertRaisesRegex(ValueError, 'exact original ID'):
                writer.supplement_binding(supplement, path, sources)

    def test_supplement_rejects_sibling_route(self):
        path, sources, supplement, refs = self.supplement_fixture()
        supplement['route'] = 'request'
        with patch.object(writer, 'reference', side_effect=lambda p: refs[str(p)]):
            with self.assertRaisesRegex(ValueError, 'sibling original ID'):
                writer.supplement_binding(supplement, path, sources)

    def test_duplicate_supplement_cannot_count_twice(self):
        path, sources, supplement, refs = self.supplement_fixture()
        data = {'physical_inputs': {}}
        with patch.object(writer.validate_oracles, 'validate_supplement', return_value=supplement):
            with patch.object(writer, 'reference', side_effect=lambda p: refs[str(p)]):
                with self.assertRaisesRegex(ValueError, 'duplicate oracle supplement'):
                    writer.add_oracle_supplements(data, [path, path], {}, sources)

    def test_supplement_hash_accepts_only_its_exact_original_id(self):
        _, sources, _, refs = self.supplement_fixture()
        item = {'route': 'response', 'oracle_review_sha256': 'supplement', 'batch': 'retake',
                'scenario': 'new', 'runner_exit_code': 0, 'attempt': '/attempt', 'observation_state': 'observed'}
        allowed = {'original': {'supplement'}}
        with patch.object(writer, 'reference', side_effect=lambda p: refs[str(p)]):
            collected = {}
            writer.add_retaken_ids(item, ['original'], sources, collected, allowed)
            self.assertEqual(list(collected), ['original'])
            with self.assertRaisesRegex(ValueError, 'independently verified review'):
                writer.add_retaken_ids(item, ['different'], sources, {}, allowed)
            item['oracle_review_sha256'] = 'unvalidated'
            with self.assertRaisesRegex(ValueError, 'independently verified review'):
                writer.add_retaken_ids(item, ['original'], sources, {}, allowed)
            item['oracle_review_sha256'] = 'old'
            writer.add_retaken_ids(item, ['original'], sources, collected, allowed)
            self.assertEqual(len(collected['original']), 2)

    def test_old_84_runs_and_one_supplement_keep_unique_id_accounting(self):
        _, sources, _, refs = self.supplement_fixture()
        old = {'route': 'response', 'oracle_review_sha256': 'old', 'batch': 'original',
               'scenario': 'old', 'runner_exit_code': 0, 'attempt': '/attempt',
               'observation_state': 'observed', 'original_oracle_case_ids': ['original']}
        fresh = dict(old, oracle_review_sha256='supplement', batch='retake', scenario='fresh')
        data = {'host_measurements': [dict(old) for _ in range(84)] + [fresh],
                'original_ids': [{'run_scoped_case_id': 'original'}],
                'source_oracle_progress': {'reviewed_count': 125, 'new_source_proposals': 33}}
        with patch.object(writer, 'reference', side_effect=lambda p: refs[str(p)]):
            writer.add_original_retakes(data, sources, {'original': {'supplement'}})
        self.assertEqual(data['original_id_retakes']['host_runs'], 85)
        self.assertEqual(data['original_id_retakes']['unique_original_ids'], 1)
        self.assertEqual(data['source_oracle_progress'], {'reviewed_count': 125, 'new_source_proposals': 33})
        self.assertEqual(len(data['original_ids'][0]['current_task_unqualified_host_runs']), 85)
        self.assertFalse(data['original_id_retakes']['full_lifecycle_qualified'])


if __name__ == '__main__':
    unittest.main()
