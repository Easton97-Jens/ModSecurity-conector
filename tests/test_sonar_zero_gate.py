"""Offline exact-head controls using official structured response shapes."""
from __future__ import annotations

from contextlib import redirect_stdout
import copy
import importlib.util
import io
from pathlib import Path
import sys
import unittest
from unittest import mock
from urllib.parse import parse_qs, urlsplit
import yaml

ROOT = Path(__file__).resolve().parents[1]
CI_DEPENDENCY_INSTALLER = 'ci/tools/install-ci-dependencies.py'
CI_DEPENDENCY_INSTALL_COMMAND = f'python3 {CI_DEPENDENCY_INSTALLER} --ci-toolcache'
SPEC = importlib.util.spec_from_file_location("sonar_zero_gate", ROOT / "ci/checks/common/check-sonar-zero.py")
GATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)
INSTALL_SPEC = importlib.util.spec_from_file_location("sonar_gate_dependency_installer", ROOT / CI_DEPENDENCY_INSTALLER)
INSTALLER = importlib.util.module_from_spec(INSTALL_SPEC)
sys.modules[INSTALL_SPEC.name] = INSTALLER
INSTALL_SPEC.loader.exec_module(INSTALLER)
HEAD = "a" * 40
REPOSITORY = "example/connector"
PR = "413"
PR_ANALYSES = "project_pull_requests/list"
MEASURES_COMPONENT = "measures/component"
ISSUES_SEARCH = "issues/search"


def make_check(**changes):
    value = {"id": 1, "head_sha": HEAD, "name": GATE.CHECK_NAME,
             "app": {"slug": "sonarqubecloud"}, "status": "completed", "conclusion": "success",
             "output": {"summary": "Quality Gate passed", "annotations_count": 0}}
    value.update(changes)
    return value


def alter_inventory_page(mode, params, payload, first):
    if mode == 'partial':payload['issues'] = []
    if mode == 'duplicate':payload['issues'][-1] = first
    if mode == 'count-change' and params['p'] == 2:payload['paging']['total'] = 102
    if mode == 'missing-paging':payload.pop('paging')
    if mode == 'bool-page':payload['paging']['pageIndex'] = True
    return payload


def alter_check_inventory(kind, payload):
    if kind == 'missing':payload.pop('total_count')
    if kind == 'partial':payload['total_count'] = 2
    if kind == 'duplicate':
        payload['total_count'] = 2
        payload['check_runs'].append(copy.deepcopy(payload['check_runs'][0]))
    if kind == 'boolean':payload['total_count'] = True
    return payload


class Evidence:
    """Independent fake API boundaries; every response has explicit counts."""
    def __init__(self):
        self.checks = [make_check()]
        self.heads = [HEAD, HEAD]
        self.annotations = []
        self.analysis = {"key": PR, "commit": {"sha": HEAD}, "analysisDate": "2026-10-15T14:48:42+0000",
                         "status": {"qualityGateStatus": "OK"}}
        self.gate = {"status": "OK", "ignoredConditions": False,
                     "conditions": [{"status": "OK", "metricKey": "new_security_rating"}]}
        self.measures = [{"metric": key, "periods": [{"index": 1, "value": "1" if key in GATE.RATING_METRICS else "0"}]} for key in GATE.METRICS]
        self.active, self.accepted, self.hotspots = [], [], []
        self.github_calls, self.sonar_calls = [], []
        self.hook = lambda endpoint, params, payload: payload

    def set_measure(self, key, value):
        next(row for row in self.measures if row['metric'] == key)['periods'][0]['value'] = value

    def records(self, count, prefix="issue"):
        return [{"key": prefix+str(index), "project": GATE.PROJECT, "pullRequest": PR} for index in range(count)]

    def fetch(self, path):
        self.github_calls.append(path)
        if "/pulls/" in path:
            head = self.heads.pop(0) if len(self.heads) > 1 else self.heads[0]
            return {"number": int(PR), "head": {"sha": head}}
        page = int(parse_qs(urlsplit(path).query).get('page', ['1'])[0])
        if "/annotations?" in path:
            return copy.deepcopy(self.annotations[(page-1)*GATE.PAGE_SIZE:page*GATE.PAGE_SIZE])
        if "/commits/" in path:
            return {"total_count": len(self.checks), "check_runs": copy.deepcopy(self.checks[(page-1)*GATE.PAGE_SIZE:page*GATE.PAGE_SIZE])}
        raise AssertionError('unexpected GitHub endpoint: '+path)

    def sonar(self, endpoint, params):
        self.sonar_calls.append((endpoint, dict(params)))
        if endpoint == PR_ANALYSES:
            result = {"pullRequests": [copy.deepcopy(self.analysis)]}
        elif endpoint == "qualitygates/project_status":
            result = {"projectStatus": copy.deepcopy(self.gate)}
        elif endpoint == MEASURES_COMPONENT:
            result = {"component": {"key": GATE.PROJECT, "pullRequest": PR, "measures": copy.deepcopy(self.measures)}}
        elif endpoint == ISSUES_SEARCH:
            rows = self.accepted if params['issueStatuses'] == 'ACCEPTED' else self.active
            page, size = params['p'], params['ps']
            result = {"paging": {"pageIndex": page, "pageSize": size, "total": len(rows)},
                      "issues": copy.deepcopy(rows[(page-1)*size:page*size])}
        elif endpoint == "measures/component_tree":
            result = {"paging": {"pageIndex": params['p'], "pageSize": params['ps'], "total": 0}, "components": []}
        else:
            raise AssertionError('unexpected Sonar endpoint: '+endpoint)
        return self.hook(endpoint, params, result)

    def verify(self, **options):
        with redirect_stdout(io.StringIO()):
            return GATE.verify(REPOSITORY, HEAD, self.fetch, pr=PR, read_sonar=self.sonar,
                               sleep=lambda _: None, attempts=options.pop('attempts', 1), **options)


class SonarZeroGateTests(unittest.TestCase):
    def assert_locked_install_before_gate_tests(self, steps):
        installs = [(index, step) for index, step in enumerate(steps)
                    if CI_DEPENDENCY_INSTALLER in step.get('run', '')]
        self.assertEqual(len(installs), 1)
        index, step = installs[0]
        self.assertEqual(step['run'].strip(), CI_DEPENDENCY_INSTALL_COMMAND)
        self.assertNotIn('if', step)
        verifiers = [position for position, candidate in enumerate(steps)
                     if candidate.get('name') == 'Verify Python interpreter contract']
        self.assertEqual(len(verifiers), 1)
        self.assertLess(verifiers[0], index)
        consumers = [position for position, candidate in enumerate(steps)
                     if 'tests.test_sonar_zero_gate' in candidate.get('run', '')]
        self.assertEqual(len(consumers), 1)
        self.assertLess(index, consumers[0])

    def test_hash_locked_yaml_dependency_is_installed_before_gate_unit_tests(self):
        workflow = yaml.safe_load((ROOT/'.github/workflows/lint.yml').read_text())
        self.assert_locked_install_before_gate_tests(workflow['jobs']['scaffold-lint']['steps'])
        # The reviewed source exception verifies both locks before execution;
        # pip still accepts only hash-checked local wheels without resolution.
        source, tools, version = INSTALLER.reviewed_pins(None)
        self.assertEqual(source.name, 'PyYAML')
        self.assertEqual(source.filename, f'pyyaml-{version}.tar.gz')
        self.assertEqual({tool.name for tool in tools}, {'pip', 'setuptools', 'Cython'})
        for flag in ('--only-binary=:all:', '--require-hashes', '--no-index', '--no-deps'):
            self.assertIn(flag, INSTALLER.PIP_INSTALL)

    def test_missing_late_or_unprotected_yaml_install_is_rejected(self):
        workflow = yaml.safe_load((ROOT/'.github/workflows/lint.yml').read_text())
        original = workflow['jobs']['scaffold-lint']['steps']
        index = next(position for position, step in enumerate(original)
                     if CI_DEPENDENCY_INSTALLER in step.get('run', ''))
        for mutation in ('missing', 'late', 'unguarded', 'conditional', 'duplicate'):
            with self.subTest(mutation=mutation):
                steps = copy.deepcopy(original)
                if mutation == 'missing':
                    steps.pop(index)
                elif mutation == 'late':
                    steps.append(steps.pop(index))
                elif mutation == 'unguarded':
                    steps[index]['run'] = f'python3 {CI_DEPENDENCY_INSTALLER}'
                elif mutation == 'conditional':
                    steps[index]['if'] = 'false'
                else:
                    steps.insert(index, copy.deepcopy(steps[index]))
                with self.assertRaises(AssertionError):
                    self.assert_locked_install_before_gate_tests(steps)

    def test_both_workflow_gates_bind_explicit_PR_and_head(self):
        workflow = yaml.safe_load((ROOT/'.github/workflows/lint.yml').read_text())
        commands = {'python ci/checks/common/check-sonar-zero.py',
                    'python ci/checks/common/check-sonar-duplication.py'}
        steps = [s for job in workflow['jobs'].values() for s in job.get('steps', []) if s.get('run') in commands]
        self.assertEqual(len(steps), 2)
        for step in steps:
            self.assertEqual(step['env']['PR_NUMBER'], '${{ github.event.pull_request.number }}')
            self.assertEqual(step['env']['PR_HEAD_SHA'], '${{ github.event.pull_request.head.sha }}')

    def test_missing_presentation_counts_pass_only_with_complete_structured_zero(self):
        evidence = Evidence()
        result = evidence.verify()
        self.assertEqual(result['head_sha'], HEAD)
        self.assertEqual(result['new_violations'], '0')
        self.assertEqual(result['security_rating'], '1')
        self.assertEqual(sum(name == PR_ANALYSES for name, _ in evidence.sonar_calls), 2)

    def test_all_missing_metrics_fail_instead_of_defaulting_to_zero(self):
        for missing in GATE.METRICS:
            with self.subTest(metric=missing):
                evidence = Evidence()
                evidence.measures = [r for r in evidence.measures if r['metric'] != missing]
                with self.assertRaisesRegex(GATE.GateError, 'incomplete'):
                    evidence.verify()

    def test_duplicate_and_null_metric_values_fail(self):
        evidence = Evidence()
        evidence.measures.append(copy.deepcopy(evidence.measures[0]))
        with self.assertRaisesRegex(GATE.GateError, 'duplicate'):
            evidence.verify()
        evidence = Evidence()
        evidence.set_measure('new_violations', None)
        with self.assertRaisesRegex(GATE.GateError, 'numeric'):
            evidence.verify()

    def test_every_nonzero_finding_class_fails(self):
        for key, inventory in [('new_violations', 'active'), ('new_accepted_issues', 'accepted'), ('new_security_hotspots', 'hotspots')]:
            with self.subTest(metric=key):
                evidence = Evidence()
                evidence.set_measure(key, '1')
                setattr(evidence, inventory, evidence.records(1))
                with self.assertRaisesRegex(GATE.GateError, 'zero new issues'):
                    evidence.verify()

    def test_measures_cannot_hide_finding_inventory(self):
        evidence = Evidence()
        evidence.active = evidence.records(1)
        with self.assertRaisesRegex(GATE.GateError, 'disagree'):
            evidence.verify()

    def test_security_rating_must_be_explicit_A(self):
        for key in GATE.RATING_METRICS:
            with self.subTest(metric=key):
                evidence = Evidence()
                evidence.set_measure(key, '2')
                with self.assertRaisesRegex(GATE.GateError, 'Security Rating'):
                    evidence.verify()

    def test_provider_must_be_terminal_success_for_current_head(self):
        for change in ({'head_sha': 'b'*40}, {'status': 'in_progress'}, {'conclusion': 'failure'}, {'app': {'slug': 'foreign'}}):
            with self.subTest(change=change):
                evidence = Evidence()
                evidence.checks = [make_check(**change)]
                with self.assertRaises(GATE.GateError):
                    evidence.verify()

    def test_latest_pending_run_supersedes_old_success(self):
        evidence = Evidence()
        evidence.checks.append(make_check(id=2, status='in_progress'))
        with self.assertRaisesRegex(GATE.GateError, 'completed'):
            evidence.verify()

    def test_current_PR_head_checked_before_and_after(self):
        for heads in (['b'*40, HEAD], [HEAD, 'b'*40]):
            with self.subTest(heads=heads):
                evidence = Evidence()
                evidence.heads = heads
                with self.assertRaisesRegex(GATE.GateError, 'PR head changed'):
                    evidence.verify()

    def test_stale_missing_ambiguous_or_changed_analysis_is_rejected(self):
        cases = (
            lambda e, p: {'pullRequests': []},
            lambda e, p: {'pullRequests': [p['pullRequests'][0], p['pullRequests'][0]]},
            lambda e, p: {'pullRequests': [{**p['pullRequests'][0], 'commit': {'sha': 'b'*40}}]},
            lambda e, p: {'pullRequests': [{**p['pullRequests'][0], 'commit': {}}]},
            lambda e, p: {'pullRequests': [{**p['pullRequests'][0], 'analysisDate': None}]},
        )
        for mutate in cases:
            with self.subTest(mutate=mutate):
                evidence = Evidence()
                evidence.hook = lambda endpoint, params, payload: mutate(evidence, payload) if endpoint == PR_ANALYSES else payload
                with self.assertRaises(GATE.GateError):
                    evidence.verify()

    def test_analysis_replacement_during_readback_fails(self):
        evidence = Evidence()
        def hook(endpoint, params, payload):
            if endpoint == PR_ANALYSES and len(evidence.sonar_calls) > 1:
                payload['pullRequests'][0]['analysisDate'] = '2026-10-15T15:00:00+0000'
            return payload
        evidence.hook = hook
        with self.assertRaisesRegex(GATE.GateError, 'analysis changed'):
            evidence.verify()

    def test_quality_gate_failure_ignored_or_missing_conditions_fail(self):
        for changes in ({'status': 'ERROR'}, {'ignoredConditions': True}, {'ignoredConditions': None},
                        {'conditions': None}, {'conditions': [{'status': 'ERROR'}]}):
            with self.subTest(changes=changes):
                evidence = Evidence()
                evidence.gate.update(changes)
                with self.assertRaises(GATE.GateError):
                    evidence.verify()

    def test_foreign_or_missing_component_identity_fails(self):
        for identity in ({'key': 'foreign'}, {'pullRequest': '410'}, {'pullRequest': None}):
            with self.subTest(identity=identity):
                evidence = Evidence()
                def hook(endpoint, params, payload):
                    if endpoint == MEASURES_COMPONENT:
                        payload['component'].update(identity)
                    return payload
                evidence.hook = hook
                with self.assertRaisesRegex(GATE.GateError, 'identity'):
                    evidence.verify()

    def test_github_inventory_is_fully_paginated(self):
        evidence = Evidence()
        evidence.checks = [make_check(id=i) for i in range(1, 102)]
        result = evidence.verify()
        self.assertEqual(result['check_id'], 101)
        self.assertEqual(sum('/commits/' in p for p in evidence.github_calls), 4)

    def test_sonar_inventory_is_fully_paginated_before_nonzero_rejection(self):
        evidence = Evidence()
        evidence.active = evidence.records(101)
        evidence.set_measure('new_violations', '101')
        with self.assertRaisesRegex(GATE.GateError, 'zero new issues'):
            evidence.verify()
        active_pages = [p['p'] for name, p in evidence.sonar_calls if name == ISSUES_SEARCH and p['issueStatuses'] == 'OPEN,CONFIRMED']
        self.assertEqual(active_pages, [1, 2])

    def test_partial_duplicate_or_ambiguous_pages_fail(self):
        for mode in ('partial', 'duplicate', 'count-change', 'missing-paging', 'bool-page'):
            with self.subTest(mode=mode):
                evidence = Evidence()
                evidence.active = evidence.records(101)
                evidence.set_measure('new_violations', '101')
                def hook(endpoint, params, payload):
                    if endpoint != ISSUES_SEARCH or params['issueStatuses'] != 'OPEN,CONFIRMED':
                        return payload
                    return alter_inventory_page(mode, params, payload, evidence.active[0])
                evidence.hook = hook
                with self.assertRaises(GATE.GateError):
                    evidence.verify()

    def test_annotations_cannot_be_hidden_or_left_partial(self):
        for declared, records in ((0, [{}]), (1, []), (1, [{}])):
            with self.subTest(declared=declared, records=records):
                evidence = Evidence()
                evidence.annotations = records
                evidence.checks[0]['output']['annotations_count'] = declared
                with self.assertRaises(GATE.GateError):
                    evidence.verify()

    def test_annotation_inventory_is_fully_paginated_before_rejection(self):
        evidence = Evidence()
        evidence.annotations = [{} for _ in range(101)]
        evidence.checks[0]['output']['annotations_count'] = 101
        with self.assertRaises(GATE.GateError):
            evidence.verify()
        self.assertEqual(sum('/annotations?' in p for p in evidence.github_calls), 2)

    def test_missing_partial_duplicate_or_boolean_github_counts_fail(self):
        for kind in ('missing', 'partial', 'duplicate', 'boolean'):
            with self.subTest(kind=kind):
                evidence = Evidence()
                fetch = evidence.fetch
                def altered(path):
                    payload = fetch(path)
                    if '/commits/' in path:
                        return alter_check_inventory(kind, payload)
                    return payload
                with self.assertRaises(GATE.GateError):
                    GATE.verify(REPOSITORY, HEAD, altered, pr=PR, read_sonar=evidence.sonar, attempts=1)

    def test_analysis_timestamp_must_be_explicit_and_timezone_aware(self):
        for date in ('', ' ', 'yesterday', '2026-10-15T14:00:00', None):
            with self.subTest(date=date):
                evidence = Evidence()
                evidence.analysis['analysisDate'] = date
                with self.assertRaisesRegex(GATE.GateError, 'date'):
                    evidence.verify()

    def test_missing_checks_and_counts_fail(self):
        evidence = Evidence()
        evidence.checks = []
        with self.assertRaises(GATE.GateError):
            evidence.verify()
        evidence = Evidence()
        evidence.checks[0]['output'].pop('annotations_count')
        with self.assertRaises(GATE.GateError):
            evidence.verify()

    def test_provider_replacement_during_readback_fails(self):
        evidence = Evidence()
        def hook(endpoint, params, payload):
            if endpoint == MEASURES_COMPONENT:
                evidence.checks.append(make_check(id=2))
            return payload
        evidence.hook = hook
        with self.assertRaisesRegex(GATE.GateError, 'provider changed'):
            evidence.verify()

    def test_provider_conclusion_change_during_readback_fails(self):
        evidence = Evidence()
        def hook(endpoint, params, payload):
            if endpoint == MEASURES_COMPONENT:
                evidence.checks[0]["conclusion"] = "failure"
            return payload
        evidence.hook = hook
        with self.assertRaisesRegex(GATE.GateError, "provider changed"):
            evidence.verify()

    def test_invalid_identity_stops_before_network(self):
        for repository, head, pr in (('../foreign', HEAD, PR), ('example/..', HEAD, PR),
                                     (REPOSITORY, 'branch', PR), (REPOSITORY, HEAD, '0')):
            with self.subTest(repository=repository, head=head, pr=pr):
                with self.assertRaises(GATE.GateError):
                    GATE.verify(repository, head, lambda _: self.fail('network reached'), pr=pr)

    def test_diagnostic_text_is_bounded_and_command_inert(self):
        output = io.StringIO()
        annotation = {'path': 'file.c', 'start_line': 9, 'title': 'issue',
                      'message': '\n::error::'+'x'*2000, 'raw_details': 'never print source'}
        with redirect_stdout(output):
            GATE.report_findings(REPOSITORY, 1, lambda _: [annotation])
        self.assertEqual(len(output.getvalue().splitlines()), 1)
        self.assertNotIn('never print source', output.getvalue())
        self.assertLess(len(output.getvalue()), 700)

    def test_duplicate_JSON_fields_and_redirects_fail(self):
        with self.assertRaisesRegex(GATE.GateError, 'duplicate JSON'):
            GATE.unique_object([('total', 0), ('total', 1)])
        redirect_guard = GATE.RejectRedirects()
        with self.assertRaisesRegex(GATE.GateError, 'redirected'):
            redirect_guard.redirect_request(None, None, None, None, None, None)

    def test_official_client_enforces_timeout_byte_bound_and_object_shape(self):
        opener = mock.MagicMock()
        response = opener.open.return_value.__enter__.return_value
        response.read.return_value = b'x' * (GATE.MAX_RESPONSE_BYTES+1)
        with mock.patch.object(GATE.urllib.request, 'build_opener', return_value=opener):
            with self.assertRaisesRegex(GATE.GateError, 'bounded'):
                GATE.read_json(object())
        self.assertEqual(opener.open.call_args.kwargs['timeout'], 15)
        response.read.assert_called_once_with(GATE.MAX_RESPONSE_BYTES+1)
        with mock.patch.object(GATE, 'read_json', return_value=[]):
            with self.assertRaisesRegex(GATE.GateError, 'object'):
                GATE.sonar_get(MEASURES_COMPONENT, {})

    def test_only_supported_new_code_filter_is_sent_and_hotspots_remain_PR_measure(self):
        evidence = Evidence()
        evidence.verify()
        for endpoint, params in evidence.sonar_calls:
            self.assertNotEqual(endpoint, 'hotspots/search')
            if endpoint == ISSUES_SEARCH:
                self.assertEqual(params['sinceLeakPeriod'], 'true')
                self.assertNotIn('inNewCodePeriod', params)

    def test_duplicate_file_and_blocks_remain_bounded_diagnostics_before_failure(self):
        evidence = Evidence()
        evidence.set_measure('new_duplicated_lines', '2')
        def hook(endpoint, params, payload):
            if endpoint == 'measures/component_tree':
                payload['paging']['total'] = 1
                payload['components'] = [{'key': GATE.PROJECT+':file.c', 'path': 'file.c',
                    'measures': [{'metric': 'new_duplicated_lines', 'period': {'value': '2'}}]}]
            return payload
        evidence.hook = hook
        read = evidence.sonar
        def sonar(endpoint, params):
            if endpoint == 'duplications/show':
                return {'duplications': [{'blocks': [{'from': 1, 'size': 2, '_ref': '1'}]}], 'files': {}}
            return read(endpoint, params)
        output = io.StringIO()
        with redirect_stdout(output), self.assertRaisesRegex(GATE.GateError, 'zero new issues'):
            GATE.verify(REPOSITORY, HEAD, evidence.fetch, pr=PR, read_sonar=sonar, attempts=1)
        self.assertIn('sonar duplicate file:', output.getvalue())
        self.assertIn('sonar duplicate blocks:', output.getvalue())



# Parent default discovery uses the one admitted active-case inventory.
if __import__("os").environ.get("ON_DEMAND_TESTS") != "1":
    def load_tests(loader, standard_tests, pattern):
        from ci.lib.active_test_inventory import module_load_tests
        return module_load_tests(loader, standard_tests, pattern)

if __name__ == '__main__':
    unittest.main()
