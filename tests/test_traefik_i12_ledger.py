"""Keep the Traefik original inventory and qualification boundaries explicit."""

import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    'traefik_i12_ledger', ROOT / 'connectors/traefik/harness/i12_ledger.py')
LEDGER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LEDGER)


class TraefikI12LedgerTest(unittest.TestCase):
    def setUp(self):
        self.inventory = json.loads(LEDGER.INVENTORY.read_text())

    def test_exact_original_ids_contracts_and_124_members_are_preserved(self):
        rows = self.inventory['rows']
        ids = '\n'.join(r['run_scoped_case_id'] for r in rows) + '\n'
        self.assertEqual(hashlib.sha256(ids.encode()).hexdigest(),
                         'd42fe8f76bac2b1162ffa91e8aa4f270a6e84c2009029e1e365f3cb4552d08ee')
        self.assertEqual(LEDGER.contracts().ORACLES.canonical_digest(
            [r['selected_requirement'] for r in rows]),
            '94fe75e6ee0154c9a55bca42f1e9d41882655bedbf7425d8fb0731a8016de7f2')
        before = copy.deepcopy(self.inventory)
        result = LEDGER.reconcile(self.inventory)
        self.assertEqual(self.inventory, before)
        for leg, unresolved, config_only in [('traefik-native-uds', 54, 1),
                                             ('traefik-forwardauth-request', 38, 8),
                                             ('traefik-forwardauth-response-companion', 29, 0)]:
            summary = result['summary'][leg]
            self.assertEqual(summary['baseline_lifecycle_pass'], 1)
            self.assertEqual(summary['fresh_lifecycle_pass'], 0)
            self.assertEqual(summary['baseline_config_only_pass'], config_only)
            self.assertEqual(len(summary['unresolved_original_oracle_ids']), unresolved)
            self.assertEqual(len(summary['lifecycle_unqualified_ids']), summary['required_ids']-1)

    def test_duplicate_or_sibling_membership_cannot_qualify(self):
        for mutate in (lambda d:d['rows'].append(copy.deepcopy(d['rows'][0])),
                       lambda d:d['rows'][0].update(leg_id='traefik-forwardauth-request'),
                       lambda d:d['rows'][0].update(required_leg=False)):
            with self.subTest(mutation=mutate):
                bad = copy.deepcopy(self.inventory)
                mutate(bad)
                with self.assertRaises(ValueError):
                    LEDGER.reconcile(bad)

    def test_baseline_pass_and_resolved_dispositions_cannot_be_injected(self):
        bad_pass = copy.deepcopy(self.inventory)
        bad_pass['rows'][0]['qualified_host_lifecycle_pass'] = True
        bad_oracle = copy.deepcopy(self.inventory)
        unresolved = next(r['original_oracle_disposition'] for r in bad_oracle['rows'] if
                          (r.get('original_oracle_disposition') or {}).get('resolved') is False)
        unresolved['resolved'] = True
        for bad in (bad_pass,bad_oracle):
            with self.assertRaisesRegex(ValueError,'baseline inventory changed'):
                LEDGER.reconcile(bad)

    def test_tcp_eof_and_driver_pass_cannot_replace_native_measurements(self):
        contract = LEDGER.contracts()
        row = self.inventory['rows'][0]
        packet = dict(reviewed_by='root',run_scoped_case_id=row['run_scoped_case_id'],
                      leg_id=row['leg_id'],execution_observed=True,execution_kind='host_http',
                      run_id='negative-control',parent_sha=self.inventory['parent_sha'],
                      framework_sha='99a7985c1be92a2297b1b59208f64df6768f2cbf',
                      mrts_sha='8a6bb546c4c81d8ffc7be801dceac60c6925685f',
                      effective_config_sha256='0'*64,oracle_evaluated=False,
                      outcome=None, observations={k:dict(value=None,reason='Not measured in negative control')
                                                 for k in contract.ROLES})
        with tempfile.TemporaryDirectory(dir=os.environ.get('TMPDIR')) as temporary:
            path = Path(temporary)/'packet.json'
            client = Path(temporary)/'client.json'
            client.write_text('{"tcp_eof":true,"driver_exit":0}')
            packet['observations']['native_eos'] = dict(value=True,evidence=[
                {**contract.ORACLES.reference(client),'role':'client_process'}])
            path.write_text(json.dumps(packet))
            with self.assertRaisesRegex(ValueError,'physical producer'):
                LEDGER.reconcile(self.inventory, packets=[contract.ORACLES.reference(path)])

    def test_partial_host_attempt_preserves_unknowns_and_does_not_resolve_oracle(self):
        contract = LEDGER.contracts()
        row = next(r for r in self.inventory['rows'] if
                   (r.get('original_oracle_disposition') or {}).get('resolved') is False)
        packet = dict(reviewed_by='root',run_scoped_case_id=row['run_scoped_case_id'],
                      leg_id=row['leg_id'],execution_observed=True,execution_kind='host_http',
                      run_id='partial-control',parent_sha=self.inventory['parent_sha'],
                      framework_sha='99a7985c1be92a2297b1b59208f64df6768f2cbf',
                      mrts_sha='8a6bb546c4c81d8ffc7be801dceac60c6925685f',
                      effective_config_sha256='0'*64,oracle_evaluated=False,
                      outcome=None, observations={k:dict(value=None,reason='No physical producer for this field')
                                                 for k in contract.ROLES})
        with tempfile.TemporaryDirectory(dir=os.environ.get('TMPDIR')) as temporary:
            path = Path(temporary)/'packet.json'
            path.write_text(json.dumps(packet))
            result = LEDGER.reconcile(self.inventory,packets=[contract.ORACLES.reference(path)])
        summary = result['summary'][row['leg_id']]
        self.assertEqual(summary['fresh_partial'],1)
        self.assertEqual(summary['fresh_lifecycle_pass'],0)
        self.assertIn(row['run_scoped_case_id'],summary['unresolved_original_oracle_ids'])
        current = next(r for r in result['rows'] if r.get('fresh_lifecycle'))
        self.assertEqual(current['status'],'PARTIAL_HOST_MEASUREMENTS')
        self.assertEqual(current['baseline_status'],row['status'])
        observation = next(r['fresh_lifecycle'] for r in result['rows'] if r.get('fresh_lifecycle'))
        self.assertEqual(set(observation['unknown_fields']),set(contract.ROLES))

    def test_empty_host_capture_cannot_claim_observed_absence(self):
        contract = LEDGER.contracts()
        row = self.inventory['rows'][0]
        packet = dict(reviewed_by='root',run_scoped_case_id=row['run_scoped_case_id'],
                      leg_id=row['leg_id'],execution_observed=True,execution_kind='host_http',
                      run_id='empty-capture',parent_sha=self.inventory['parent_sha'],
                      framework_sha='99a7985c1be92a2297b1b59208f64df6768f2cbf',
                      mrts_sha='8a6bb546c4c81d8ffc7be801dceac60c6925685f',
                      effective_config_sha256='0'*64,oracle_evaluated=False,outcome=None,
                      observations={k:dict(value=None,reason='Not independently measured') for k in contract.ROLES})
        with tempfile.TemporaryDirectory(dir=os.environ.get('TMPDIR')) as temporary:
            path = Path(temporary)/'packet.json'
            host = Path(temporary)/'host.jsonl'
            host.write_text('')
            packet['observations']['host_eos'] = dict(value=[],evidence=[
                {**contract.ORACLES.reference(host),'role':'host_callback'}])
            path.write_text(json.dumps(packet))
            with self.assertRaisesRegex(ValueError,'empty host callback'):
                LEDGER.reconcile(self.inventory,packets=[contract.ORACLES.reference(path)])


if __name__ == '__main__':
    unittest.main()
