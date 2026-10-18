"""Mutation controls for exact-original packet qualification; no host verdicts."""
import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import qualify_originals as Q


ORIGINAL = 'I12::envoy-ext-proc::NEED-request-streaming'
ORACLE = {'native_result': 'allow', 'visible_status': 200, 'rule_id': 1900032,
          'request_bytes': 95, 'response_bytes': 96, 'response_sha256': 'response',
          'request_eos_count': 1, 'response_eos_count': 1}
CLIENT_EXIT_CHECK = 'original_client_exit'
CLIENT_SIGNAL_CHECK = 'original_client_unix_signal'
CLIENT_RESPONSE_BYTES_CHECK = 'original_client_response_bytes'
CLIENT_RESPONSE_SHA_CHECK = 'original_client_response_sha256'


def summary():
    counts = {name: 1 for name in ('native_process_request_headers', 'native_process_request_body',
        'native_process_response_headers', 'native_process_response_body', 'native_cleanup',
        'native_process_logging', 'runtime_destroy', 'runtime_finish', 'common_cleanup')}
    counts.update(common_finish=2, native_intervention=9, runtime_append_request_body_chunk=3,
                  runtime_append_response_body_chunk=3, native_append_request_body=2, native_append_response_body=2)
    callbacks = []
    for direction, sizes in ((0, (64, 31, 0)), (1, (64, 32, 0))):
        callbacks.extend({'operation': 1, 'response_direction': direction, 'body_bytes': size,
                          'eos_argument': index == 2} for index, size in enumerate(sizes))
        callbacks.extend({'operation': operation, 'response_direction': direction} for operation in (3, 4))
    client = {'process_exit': 0, 'error_type': None, 'http_status': 200, 'status_agrees_with_raw': True,
              'response_body_hash_verified': True, 'request_body_hash_verified': True,
              'independent_raw_response': {'framing_complete': True, 'entity_sha256': 'response'},
              'actual_request_send_bytes': 95, 'response_body_bytes': 96}
    images = {name: {'fd_count': 4, 'matches_build_manifest': True, 'sdk_matches_native_build': True}
              for name in ('backend', 'engine', 'envoy')}
    process = {'scope_verified': True, 'classification': 'observed_local_reset', 'local_http2_close_code': 2,
               'remote_grpc_status': None, 'successful_grpc_completion': False}
    return {'route': 'envoy-ext-proc', 'artifact_integrity_issues': [], 'runner_exit_code': 0,
        'command_exit_codes': {name: 0 for name in ('selected-target-client', 'separate-neighbor-client',
            'host-version', 'go-version', 'sdk-who-compile', 'sdk-who', 'envoy-config-validate')},
        'controller': {'controller_exitcode': 0, 'exitcode': 0, 'supervisor_reaped': True,
            'error_count': 0, 'surviving_namespace_pid_count': 0, 'outside_mount_leak_count': 0,
            'namespace_pin_verified': True, 'executed_input_hashes_unchanged': True, 'timeout': False},
        'driver': {'failure_type': None, 'remaining_owned_process_count': 0,
                   'processes': {name: {'waited_exit_code': 0, 'forced_kill': False} for name in images}},
        'source_equality': {name: True for name in ('all_rows_verified',
            'independent_sealed_baseline_overlay_contract_verified', 'complete_archived_build_inventory_verified')},
        'loaded_images': {name: copy.deepcopy(images) for name in ('before-request', 'after-target', 'after-neighbor')},
        'clients': {'target': copy.deepcopy(client), 'neighbor': copy.deepcopy(client)},
        'grpc_transport': {role: {'process': copy.deepcopy(process)} for role in ('target', 'neighbor')},
        'backend': {'request_count_is_lower_bound': False, 'request_count': 2,
            'raw_request_role_counts': {'target': 1, 'neighbor': 1},
            'requests': [{'request_body_hash_verified': True, 'response_body_hash_verified': True}] * 2},
        'native': {'verified_allocation_scope_count': 2, 'scopes': [{
            'observed_return_counts': counts, 'completed_transition_count': 1,
            'return_result_counts': {'native_intervention': {'0': 9}}, 'typed_body_callbacks': callbacks,
            'explicit_runtime_eos_handoff_counts': {'request_body_finish': 1, 'response_body_finish': 1},
            'contract_state_samples': [{'state': {'response_committed': 1}}]}, {}],
            'observer_states': [{'invalid': False, 'pending_calls': 0, 'live_mappings': 0}]},
        'native_logs': {'native-audit': {'logged_numeric_rule_id_counts': {'1900032': 1, '1900034': 1}}}}


class PredicateMutations(unittest.TestCase):
    def test_complete_control(self):
        self.assertTrue(all(Q.predicates(summary(), ORACLE).values()))

    def test_missing_remote_status_never_success(self):
        value = summary()
        value['grpc_transport']['target']['process']['successful_grpc_completion'] = True
        self.assertFalse(Q.predicates(value, ORACLE)['target_scoped_local_process_closure'])

    def test_success_receipt_cannot_replace_actual_failed_client_process(self):
        value = summary()
        value['command_exit_codes']['selected-target-client'] = 1
        self.assertFalse(Q.predicates(value, ORACLE)['actual_client_process_exits'])

    def test_missing_actual_command_is_unknown(self):
        value = summary()
        value['command_exit_codes'].pop('separate-neighbor-client')
        self.assertFalse(Q.predicates(value, ORACLE)['actual_client_process_exits'])

    def test_missing_scoped_closure_fails(self):
        value = summary()
        value['grpc_transport']['target']['process']['local_http2_close_code'] = None
        self.assertFalse(Q.predicates(value, ORACLE)['target_scoped_local_process_closure'])

    def test_duplicated_eos_fails(self):
        value = summary()
        value['native']['scopes'][0]['typed_body_callbacks'][0]['eos_argument'] = True
        self.assertFalse(Q.predicates(value, ORACLE)['request_callbacks_bytes_eos'])

    def test_extra_empty_callback_fails(self):
        value = summary()
        value['native']['scopes'][0]['typed_body_callbacks'].insert(0, {
            'operation': 1, 'response_direction': 0, 'body_bytes': 0, 'eos_argument': False})
        self.assertFalse(Q.predicates(value, ORACLE)['request_exact_callback_count'])

    def test_missing_native_phase_fails(self):
        value = summary()
        value['native']['scopes'][0]['observed_return_counts']['native_process_response_body'] = 0
        self.assertFalse(Q.predicates(value, ORACLE)['native_phases_once'])

    def test_backend_lower_bound_blocks(self):
        value = summary()
        value['backend']['request_count_is_lower_bound'] = True
        self.assertFalse(Q.predicates(value, ORACLE)['exact_backend_request_count'])

    def test_sibling_does_not_substitute_neighbor(self):
        value = summary()
        value['clients']['neighbor']['http_status'] = 500
        self.assertFalse(Q.predicates(value, ORACLE)['neighbor_client'])


class PacketMutations(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(
            dir=os.environ.get('TMPDIR', tempfile.gettempdir()), prefix='packet-controls-')
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        storage = patch.object(Q, 'RUNROOT', self.root)
        storage.start()
        self.addCleanup(storage.stop)
        read_storage = patch.object(Q, 'READ_ROOTS', (self.root,))
        read_storage.start()
        self.addCleanup(read_storage.stop)
        self.proof = self.root / 'proof.json'
        self.proof.write_text('{}\n')

    def test_physical_file_mutation(self):
        ref = Q.reference(self.proof)
        self.proof.write_text('changed\n')
        with self.assertRaisesRegex(ValueError, 'physical reference changed'):
            Q.verify_ref(ref)

    def test_original_mapping_mutation(self):
        with self.assertRaisesRegex(ValueError, 'original ID or sibling'):
            Q.identity({'case': {'original_case_ids': [ORIGINAL], 'route': 'envoy-ext-authz-request', 'label': 'fixture'}},
                       {'original_case_ids': [ORIGINAL], 'leg': 'envoy-ext-proc', 'case_id': 'I12-ENVOY-HOST::fixture'})

    def test_unknown_original_fails(self):
        with self.assertRaisesRegex(ValueError, 'explicitly selected singleton original IDs'):
            Q.identity({'case': {'original_case_ids': ['I12::envoy-ext-proc::NEED-allow']}}, {})

    def test_source_expected_body_disagreement(self):
        with self.assertRaisesRegex(ValueError, 'source oracle disagrees'):
            Q.expected_contract({'request_bytes': 2}, {'request_hex': '61', 'response_hex': '62'})

    def test_unreviewed_packet_rejected(self):
        packet = self.root / 'staged.json'
        packet.write_text(json.dumps({'reviewed_by': 'pending_root_review'}))
        with self.assertRaisesRegex(ValueError, 'individual explicit Root approval'):
            Q.validate_approved(packet)

    def test_approval_not_ready_rejected(self):
        packet = self.root / 'staged.json'
        packet.write_text(json.dumps({'reviewed_by': 'pending_root_review', 'run_scoped_case_id': ORIGINAL,
                                     'approval_ready': False}))
        expected_sha = Q.reference(packet)['sha256']
        with self.assertRaisesRegex(ValueError, 'not individually eligible'):
            Q.approve(packet, self.root / 'approved.json', ORIGINAL, expected_sha)

    def test_all_35_shared_roles_are_checked(self):
        shared = Q.shared_validator()
        self.assertEqual(len(shared.ROLES), 35)
        for field, roles in shared.ROLES.items():
            supplied = {'value': 1, 'evidence': [Q.reference(self.proof, role) for role in roles]}
            self.assertTrue(shared.measurement(field, supplied, self.root / 'packet.json')[1])
        incomplete = {'value': 1, 'evidence': [Q.reference(self.proof, 'native_api')]}
        with self.assertRaisesRegex(ValueError, 'Independent producers'):
            shared.measurement('native_eos', incomplete,
                               self.root / 'packet.json')

    def test_each_measurement_value_must_match_fresh_capture(self):
        shared = Q.shared_validator()
        fresh = {'observations': {name: {'value': 1} for name in shared.ROLES}}
        for field in shared.ROLES:
            with self.subTest(field=field):
                forged = copy.deepcopy(fresh)
                forged['observations'][field]['value'] = 2
                with self.assertRaisesRegex(ValueError, 'freshly reproduced physical facts: observations'):
                    Q.compare_regenerated(forged, fresh, fresh)

    def test_original_mapping_and_approval_metadata_cannot_be_forged(self):
        names = ('observations', 'predicate_results', 'original_mapping', 'effective_oracle',
                 'additional_sealed_expected_contract', 'physical_refs', 'parent_sha', 'framework_sha', 'mrts_sha',
                 'effective_config_sha256', 'run_id', 'closure_contract', 'approval_ready', 'remaining_requirements',
                 'run_scoped_case_id', 'leg_id', 'reproduction')
        fresh = {name: {'unchanged': True} for name in names}
        Q.compare_regenerated(fresh, fresh, fresh)
        for name in names:
            with self.subTest(name=name):
                forged = copy.deepcopy(fresh)
                forged[name] = {'forged': True}
                with self.assertRaisesRegex(ValueError, 'freshly reproduced physical facts: ' + name):
                    Q.compare_regenerated(forged, fresh, fresh)

    def test_fixture_probe_rule_requires_exact_source_semantics(self):
        (self.root / 'native.rules').write_text(
            'SecRule REQUEST_BODY "@contains request-marker" "id:101,phase:2,pass,log,t:none,msg:\'I12 Envoy P2\'"\n'
            'SecRule RESPONSE_BODY "@contains response-marker" "id:102,phase:4,pass,log,t:none,msg:\'I12 Envoy P4\'"\n')
        self.assertEqual(Q.fixture_probe_rules(self.root), {'fixture_p2_probe_rule': 101, 'fixture_p4_probe_rule': 102})
        (self.root / 'native.rules').write_text((self.root / 'native.rules').read_text().replace('phase:4,pass', 'phase:4,deny'))
        with self.assertRaisesRegex(ValueError, 'exact positive native body probe source missing'):
            Q.fixture_probe_rules(self.root)

    def fixture_pair(self):
        old, new = self.root / 'bound', self.root / 'executed'
        old.mkdir()
        new.mkdir()
        shape = {'case_id': 'old', 'request_hex': '6162', 'request_mime': 'text/plain', 'concurrent': False,
                 'expected_status': 500, 'host_request_buffer_max_bytes': 999}
        current = dict(shape, case_id='new', expected_status=200, original_case_ids=[ORIGINAL])
        current.pop('host_request_buffer_max_bytes')
        (old / 'shape.json').write_text(json.dumps(shape))
        (new / 'shape.json').write_text(json.dumps(current))
        (old / 'native.rules').write_text('SecRuleEngine On\n')
        (new / 'native.rules').write_text('SecRuleEngine On\n')
        row = {'fixture_binding': {'physical_inputs': [Q.reference(path) for path in old.iterdir()]}}
        return row, new, current

    def test_declared_binder_identity_mutations_preserve_stimulus(self):
        row, new, shape = self.fixture_pair()
        self.assertTrue(Q.verify_fixture_binding(row, new, shape, {'visible_status': 200}))

    def test_resealed_weaker_rules_do_not_change_reviewed_source_oracle(self):
        row, new, shape = self.fixture_pair()
        (new / 'native.rules').write_text('SecRuleEngine Off\n')
        # Even a new ledger accepting these bytes cannot replace the independent old binding.
        (new / 'new-ledger.json').write_text(json.dumps(Q.reference(new / 'native.rules')))
        (new / 'new-ledger.json').unlink()
        with self.assertRaisesRegex(ValueError, 'executed bound fixture bytes differ: native.rules'):
            Q.verify_fixture_binding(row, new, shape, {'visible_status': 200})

    def test_resealed_body_metadata_cannot_replace_reviewed_stimulus(self):
        row, new, shape = self.fixture_pair()
        shape['request_hex'] = '6364'
        (new / 'shape.json').write_text(json.dumps(shape))
        with self.assertRaisesRegex(ValueError, 'fixture stimulus differs'):
            Q.verify_fixture_binding(row, new, shape, {'visible_status': 200})

    def test_git_revision_cannot_supply_options_or_expressions(self):
        with patch.object(Q.subprocess, 'run') as command:
            for revision in ('--help', 'HEAD', 'a' * 40 + ':path', 'a' * 39, 'A' * 40, None, ['a' * 40]):
                with self.subTest(revision=revision), self.assertRaisesRegex(ValueError, 'exact lowercase Git commit'):
                    Q.gitlinks(revision)
            command.assert_not_called()

    def test_gitlink_output_cannot_inject_second_revision(self):
        with patch.object(Q.subprocess, 'run') as command:
            command.return_value.stdout = '160000 commit --help\tmodules/ModSecurity-test-Framework\n'
            with self.assertRaisesRegex(ValueError, 'missing recorded gitlink identity'):
                Q.gitlinks('a' * 40)
            self.assertEqual(command.call_count, 1)
            self.assertEqual(command.call_args.args[0][-3:], ['a' * 40, '--', 'modules/ModSecurity-test-Framework'])

    def test_output_nested_creation_is_private_and_exclusive(self):
        destination = self.root / 'new' / 'packet.json'
        Q.write(destination, {'safe': True})
        self.assertEqual(json.loads(destination.read_text()), {'safe': True})
        self.assertEqual(destination.stat().st_mode & 0o777, 0o600)
        self.assertEqual(destination.parent.stat().st_mode & 0o777, 0o700)
        with self.assertRaisesRegex(ValueError, 'output authority rejected'):
            Q.write(destination, {'replace': True})
        self.assertEqual(json.loads(destination.read_text()), {'safe': True})

    def test_output_rejects_traversal_before_open(self):
        with patch.object(Q.os, 'open') as opened:
            with self.assertRaisesRegex(ValueError, 'new task-owned external file'):
                Q.write(Q.RUNROOT / '..' / 'escape.json', {})
            opened.assert_not_called()

    def test_output_rejects_symlink_parent_and_leaf(self):
        (self.root / 'link').symlink_to(self.root, target_is_directory=True)
        (self.root / 'leaf.json').symlink_to(self.proof)
        for destination in (self.root / 'link' / 'new.json', self.root / 'leaf.json'):
            with self.subTest(destination=destination), self.assertRaisesRegex(ValueError, 'output authority rejected'):
                Q.write(destination, {})
        self.assertEqual(self.proof.read_text(), '{}\n')

    def test_output_rejects_public_writable_directory(self):
        public = self.root / 'public'
        public.mkdir(mode=0o777)
        public.chmod(0o777)
        with self.assertRaisesRegex(ValueError, 'directory authority rejected'):
            Q.write(public / 'packet.json', {})

    def test_read_rejects_outside_domain_before_any_open(self):
        with patch.object(Q.EVIDENCE.os, 'open') as opened:
            for value in ('/etc/passwd', '/proc/self/environ', 'https://example.test/input.json',
                          str(Q.RUNROOT / '..' / 'other-run' / 'input.json')):
                for reader in (Q.load, Q.read_bytes, Q.reference):
                    with self.subTest(value=value, reader=reader.__name__), self.assertRaises(ValueError):
                        reader(value)
            opened.assert_not_called()

    def test_read_rejects_parent_and_leaf_symlinks(self):
        (self.root / 'directory-link').symlink_to(self.root, target_is_directory=True)
        (self.root / 'file-link.json').symlink_to(self.proof)
        for path in (self.root / 'directory-link' / 'proof.json', self.root / 'file-link.json'):
            for reader in (Q.load, Q.read_bytes, Q.reference):
                with self.subTest(path=path, reader=reader.__name__), self.assertRaises(ValueError):
                    reader(path)

    def test_read_rejects_group_writable_evidence(self):
        self.proof.chmod(0o660)
        for reader in (Q.load, Q.read_bytes, Q.reference):
            with self.subTest(reader=reader.__name__), self.assertRaises(ValueError):
                reader(self.proof)

    def test_read_does_not_reveal_missing_or_inaccessible_leaf(self):
        missing = self.root / 'absent.json'
        self.proof.chmod(0o666)
        for reader in (Q.load, Q.read_bytes, Q.reference):
            messages = []
            for path in (missing, self.proof):
                with self.assertRaises(ValueError) as caught:
                    reader(path)
                messages.append(str(caught.exception))
            self.assertEqual(messages[0], messages[1])

    def test_read_retains_valid_physical_identity(self):
        self.assertEqual(Q.load(self.proof), {})
        self.assertEqual(Q.read_bytes(self.proof), b'{}\n')
        self.assertEqual(Q.reference(self.proof)['bytes'], 3)

    def test_missing_storage_configuration_fails_before_write_or_stage(self):
        with patch.object(Q, 'RUNROOT', None), patch.object(Q.os, 'open') as opened:
            for operation in (lambda: Q.write(self.root / 'packet.json', {}),
                              lambda: Q.prepare(self.root / 'runs.json', self.root / 'packets'),
                              lambda: Q.stage_one({}, 'a' * 40, self.root / 'runs.json', self.root, None)):
                with self.assertRaisesRegex(ValueError, 'CODEX_PROJECT_STATE configuration required'):
                    operation()
            opened.assert_not_called()

    def test_import_without_storage_configuration_stays_read_only(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location('qualifier_without_storage', Q.__file__)
        module = importlib.util.module_from_spec(spec)
        with patch.object(Q.EVIDENCE, 'configured_storage', return_value=None):
            spec.loader.exec_module(module)
        self.assertIsNone(module.RUNROOT)
        self.assertEqual(module.READ_ROOTS, (module.REPO,))
        with self.assertRaisesRegex(ValueError, 'CODEX_PROJECT_STATE configuration required'):
            module.write(self.root / 'packet.json', {})

    def test_configured_storage_keeps_exact_run_domains(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location('qualifier_configured_storage', Q.__file__)
        module = importlib.util.module_from_spec(spec)
        with patch.object(Q.EVIDENCE, 'configured_storage', return_value=self.root):
            spec.loader.exec_module(module)
        self.assertEqual(module.RUNROOT, self.root / 'runs/i12-envoy-410-20261015')
        self.assertEqual(module.READ_ROOTS, (module.REPO, module.RUNROOT,
            self.root / 'runs/e2e/20261014T182400Z-pr410-oracle-lifecycle'))
        self.assertNotIn(self.root, module.READ_ROOTS)

    def client_original_fixture(self):
        body = b'response'
        digest = hashlib.sha256(body).hexdigest()
        client = self.root / 'client'
        client.mkdir()
        (client / 'target.response.raw').write_bytes(b'HTTP/1.1 200 OK\r\nContent-Length: 8\r\n\r\n' + body)
        (client / 'target.body.raw').write_bytes(body)
        (client / 'target.receipt.json').write_text(json.dumps({
            'bytes': len(body), 'sha256': digest, 'proposed_process_exit': 0}))
        self.command = self.root / 'selected-target-client.command.json'
        self.command.write_text(json.dumps({'exit_code': 0}))
        value = summary()
        value['clients']['target']['response_body_bytes'] = len(body)
        value['clients']['target']['independent_raw_response']['entity_sha256'] = digest
        expected = dict(ORACLE, response_bytes=len(body), response_sha256=digest, client_exit=0, client_signal=None)
        return value, expected

    def client_original_results(self, original, value, expected):
        checks = {}
        Q.client_original_checks(original, value, expected, self.root, checks)
        return checks

    def test_selected_client_response_bytes_uses_both_raw_http_and_entity_file(self):
        value, expected = self.client_original_fixture()
        self.assertTrue(all(self.client_original_results(Q.CLIENT_RESPONSE_BYTES_ID, value, expected).values()))
        (self.root / 'client/target.body.raw').write_bytes(b'short')
        checks = self.client_original_results(Q.CLIENT_RESPONSE_BYTES_ID, value, expected)
        self.assertFalse(checks[CLIENT_RESPONSE_BYTES_CHECK])
        self.assertFalse(checks[CLIENT_RESPONSE_SHA_CHECK])

    def test_selected_client_response_cannot_substitute_receipt_for_raw_http(self):
        value, expected = self.client_original_fixture()
        (self.root / 'client/target.response.raw').write_bytes(b'HTTP/1.1 200 OK\r\nContent-Length: 9\r\n\r\nresponse')
        checks = self.client_original_results(Q.CLIENT_RESPONSE_BYTES_ID, value, expected)
        self.assertFalse(checks[CLIENT_RESPONSE_BYTES_CHECK])
        self.assertFalse(checks[CLIENT_RESPONSE_SHA_CHECK])

    def test_selected_client_response_source_hash_cannot_be_replaced(self):
        value, expected = self.client_original_fixture()
        expected['response_sha256'] = '0' * 64
        checks = self.client_original_results(Q.CLIENT_RESPONSE_BYTES_ID, value, expected)
        self.assertFalse(checks[CLIENT_RESPONSE_SHA_CHECK])

    def test_selected_client_exit_signal_requires_actual_command_and_receipt(self):
        value, expected = self.client_original_fixture()
        self.assertTrue(all(self.client_original_results(Q.CLIENT_EXIT_SIGNAL_ID, value, expected).values()))
        self.command.write_text(json.dumps({'exit_code': -9}))
        checks = self.client_original_results(Q.CLIENT_EXIT_SIGNAL_ID, value, expected)
        self.assertFalse(checks[CLIENT_EXIT_CHECK])
        self.assertFalse(checks[CLIENT_SIGNAL_CHECK])
        self.assertEqual(Q.client_termination_evidence(self.root)['unix_signal'], 9)

    def test_selected_client_receipt_cannot_hide_failed_or_unknown_command(self):
        value, expected = self.client_original_fixture()
        for code in (1, 137, '0', False, None):
            with self.subTest(code=code):
                self.command.write_text(json.dumps({'exit_code': code}))
                checks = self.client_original_results(Q.CLIENT_EXIT_SIGNAL_ID, value, expected)
                self.assertFalse(checks[CLIENT_EXIT_CHECK])
                self.assertFalse(checks[CLIENT_SIGNAL_CHECK])

    def test_selected_client_command_cannot_hide_failed_receipt(self):
        value, expected = self.client_original_fixture()
        receipt = self.root / 'client/target.receipt.json'
        document = json.loads(receipt.read_text())
        document['proposed_process_exit'] = -15
        receipt.write_text(json.dumps(document))
        checks = self.client_original_results(Q.CLIENT_EXIT_SIGNAL_ID, value, expected)
        self.assertFalse(checks[CLIENT_EXIT_CHECK])
        self.assertFalse(checks[CLIENT_SIGNAL_CHECK])

    def test_selected_client_oracle_exit_and_signal_are_not_generic_allow(self):
        value, expected = self.client_original_fixture()
        expected['client_exit'] = 1
        self.assertFalse(self.client_original_results(Q.CLIENT_EXIT_SIGNAL_ID, value, expected)[CLIENT_EXIT_CHECK])
        expected['client_exit'] = 0
        expected['client_signal'] = 9
        self.assertFalse(self.client_original_results(Q.CLIENT_EXIT_SIGNAL_ID, value, expected)[CLIENT_SIGNAL_CHECK])
        expected.pop('client_signal')
        self.assertFalse(self.client_original_results(Q.CLIENT_EXIT_SIGNAL_ID, value, expected)[CLIENT_SIGNAL_CHECK])

    def test_selected_client_checks_do_not_expand_other_original_contracts(self):
        for original in Q.ALLOWED - {Q.CLIENT_EXIT_SIGNAL_ID, Q.CLIENT_RESPONSE_BYTES_ID}:
            with self.subTest(original=original):
                checks = self.client_original_results(original, {}, {})
                self.assertEqual(checks, {})


if __name__ == '__main__':
    unittest.main()
