"""Unit wiring observations only, never runtime proof."""
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]


def helper(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'ci/runtime/lifecycle' / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ValidRulesWiringTest(unittest.TestCase):
    def setUp(self):
        self.dispatch = helper('valid_rules_dispatch', 'run-selected-nginx-configtests.py')
        self.base = helper('valid_rules_base', 'run-nginx-configtest.py')
        self.positive = helper('valid_rules_positive', 'run-nginx-valid-rules.py')
        self.contract = dict(self.positive.VALID_RULES_CONTRACT)
        self.record = {'case_id': 'valid_rules_file', 'config_invocations': {'nginx': self.contract}}

    def test_explicit_selected_startup_contract_has_a_real_driver(self):
        self.assertEqual(self.dispatch.supported_invocations(self.base, [self.record], ['valid_rules_file']),
                         ['valid_rules_file'])
        self.assertEqual(self.dispatch.supported_invocations(self.base, [self.record], []), [])
        self.assertNotIn('valid_rules_file', self.base.CONFIGTEST_CONTRACTS,
                         'startup cannot fall through to a configuration-only driver')

    def test_wrong_operation_or_unknown_record_remains_rejected(self):
        for record in (
            {'case_id': 'valid_rules_file', 'config_invocations': {'nginx': {**self.contract, 'operation': 'configtest'}}},
            {'case_id': 'invalid_status', 'config_invocations': {'nginx': self.contract}},
        ):
            with self.subTest(record=record), self.assertRaises(ValueError):
                self.dispatch.supported_invocations(self.base, [record], [record['case_id']])

    def test_startup_command_binds_the_actual_rules_projection_and_three_revisions(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            (output/'source-result.jsonl').write_text(json.dumps({'case_id': 'valid_rules_file', 'status': 'FAIL'})+'\n')
            environment = {'FRAMEWORK_ROOT': '/var/tmp/codex/unit-framework',
                           'NGINX_DOCROOT_PROJECTION_PARENT': '/var/tmp/codex/unit-projection'}
            with mock.patch.dict(os.environ, environment), \
                    mock.patch.object(self.dispatch.sys, 'stderr', new_callable=io.StringIO) as diagnostic, \
                    mock.patch.object(self.dispatch.subprocess, 'run', return_value=mock.Mock(returncode=1)) as invoke:
                row, failed = self.dispatch.invoke_configtest(self.base, 'valid_rules_file', Path('/var/tmp/codex/prefix'),
                                                             output, 'unit-run', ('1'*40, '2'*40, '3'*40))
                self.assertEqual(diagnostic.getvalue(), 'nginx host invocation case=valid_rules_file driver_exit_code=1\n')
            argv = invoke.call_args.args[0]
            self.assertEqual(argv[1], str(ROOT/'ci/runtime/lifecycle/run-nginx-valid-rules.py'))
            for flag, value in (('--rules-file', '/var/tmp/codex/unit-framework/tests/rules/no-crs-baseline.conf'),
                                ('--projection-parent', environment['NGINX_DOCROOT_PROJECTION_PARENT']),
                                ('--framework-root', environment['FRAMEWORK_ROOT']),
                                ('--parent-sha', '1'*40), ('--framework-sha', '2'*40), ('--mrts-sha', '3'*40)):
                self.assertEqual(argv[argv.index(flag)+1], value)
            self.assertTrue(failed)
            self.assertEqual(row['status'], 'FAIL')


if __name__ == '__main__':
    unittest.main()
