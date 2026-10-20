"""Negative controls for separate current-base evidence and its accounting."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import current_base_evidence as current


def observed():
    return {'runner_exit_code': 0, 'observation_state': 'driver_result_observed',
        'artifact_integrity_issues': [], 'controller': {'exitcode': 0, 'controller_exitcode': 0,
            'timeout': False, 'supervisor_reaped': True, 'resource_violation': None,
            'namespace_pin_verified': True, 'error_count': 0, 'surviving_namespace_pid_count': 0,
            'outside_mount_leak_count': 0, 'executed_input_hashes_unchanged': True},
        'driver': {'remaining_owned_process_count': 0}, 'route': 'envoy-ext-authz-request',
        'build': {'source_git_baseline': current.PARENT, 'engine_sha256': 'engine'},
        'source_equality': {'source_contract_parent_sha': current.PARENT,
            'complete_archived_build_inventory_verified': True},
        'loaded_images': {name: {'engine': {'matches_build_manifest': True,
            'sdk_matches_native_build': True}, 'envoy': {'matches_build_manifest': True}}
            for name in ('before-request', 'after-target', 'after-neighbor')},
        'clients': {role: {'request_body_bytes': request, 'response_body_bytes': response,
            'raw_http_status': 200, 'process_exit': 0,
            'independent_raw_response': {'framing_complete': True},
            'request_body_hash_verified': True, 'response_body_hash_verified': True}
            for role, request, response in (('target', 95, 96), ('neighbor', 6, 7))},
        'grpc_transport': {role: {'process': {'remote_grpc_status': None,
            'successful_grpc_completion': False}, 'authorization': {'remote_grpc_status': 0,
            'successful_grpc_completion': True, 'classification': 'explicit_remote_status_and_close'}}
            for role in ('target', 'neighbor')},
        'backend': {'request_count': 2, 'request_count_is_lower_bound': False,
            'completed_receipt_count': 2, 'requests': [
                {'role': 'target', 'request_body_bytes': 95, 'response_body_bytes': 96},
                {'role': 'neighbor', 'request_body_bytes': 6, 'response_body_bytes': 7}]},
        'versions': {'go-version': {'identity': 'go version go1.27.3 linux/amd64', 'command_exit_code': 0},
            'sdk-who': {'identity': 'ModSecurity v3.0.14 (Linux)', 'command_exit_code': 0},
            'host-version': {'identity': 'envoy/1.39.1/Clean/RELEASE/BoringSSL', 'command_exit_code': 0}}}


class CurrentBaseControls(unittest.TestCase):
    def setUp(self):
        self.proof = {'binaries': {'engine': 'engine'}}

    def test_streaming_contract_preserves_missing_process_status(self):
        current.observed_contract(observed(), self.proof)

    def test_host_environment_identity_is_separate_from_engine_build_go(self):
        row = observed()
        row['versions']['go-version']['identity'] = 'go version go1.27.2 linux/amd64'
        with self.assertRaisesRegex(ValueError, 'runtime identities differ'):
            current.observed_contract(row, self.proof)

    def test_incomplete_loaded_image_snapshots_are_rejected(self):
        mutations = [lambda images: images.clear(),
            lambda images: images['before-request'].clear(),
            lambda images: images['after-target'].pop('engine'),
            lambda images: images['after-neighbor'].pop('envoy')]
        for mutate in mutations:
            row = observed()
            mutate(row['loaded_images'])
            with self.assertRaisesRegex(ValueError, 'loaded host/native image identity'):
                current.observed_contract(row, self.proof)

    def test_false_process_success_is_rejected(self):
        row = observed()
        row['grpc_transport']['target']['process']['successful_grpc_completion'] = True
        with self.assertRaisesRegex(ValueError, 'missing Process status'):
            current.observed_contract(row, self.proof)

    def test_unknown_authorization_cannot_count_as_success(self):
        row = observed()
        row['grpc_transport']['target']['authorization']['remote_grpc_status'] = None
        with self.assertRaisesRegex(ValueError, 'Authorization completion'):
            current.observed_contract(row, self.proof)

    def test_unscoped_authorization_remains_unknown(self):
        row = observed()
        for transport in row['grpc_transport'].values():
            transport['authorization'] = {'remote_grpc_status': None,
                'successful_grpc_completion': False, 'classification': 'unknown'}
        current.observed_contract(row, self.proof)

    def test_go_provenance_requires_physical_compiler_and_local_identity(self):
        with tempfile.TemporaryDirectory(dir=current.evidence_io.STORAGE) as directory:
            path = Path(directory) / 'bin/go'
            path.parent.mkdir()
            path.write_bytes(b'physical compiler')
            identity = 'go version go1.27.2 linux/amd64'
            proof = {'environment': {'GOTOOLCHAIN': 'local'}, 'checks': [
                {'label': 'go-version', 'argv': ['rtk', 'proxy', str(path), 'version']}],
                'go_provenance': {'required_version': '1.27.2', 'required_identity': identity,
                    'actual_identity': identity, 'verified': True, 'configured_path': str(path),
                    'executable_path': str(path), 'executable_sha256': current.evidence_io.reference(path)['sha256']}}
            root = path.parent.parent
            required = {'GOROOT': str(root), 'GOOS': 'linux', 'GOARCH': 'amd64',
                'GOVERSION': 'go1.27.2', 'GOTOOLDIR': str(root / 'pkg/tool/linux_amd64')}
            proof['environment'].update({key: required[key] for key in ('GOROOT', 'GOOS', 'GOARCH')})
            proof['go_provenance'].update(required_environment=dict(required), actual_environment=dict(required),
                environment_output=''.join(value + '\n' for value in required.values()), tools={})
            proof['checks'].append({'label': 'go-environment',
                'argv': ['rtk', 'proxy', str(path), 'env', *required]})
            proof['go_provenance']['configured_path'] = str(path)
            for name in ('compile', 'link'):
                tool_path = root / 'pkg/tool/linux_amd64' / name
                tool_path.parent.mkdir(parents=True, exist_ok=True)
                tool_path.write_bytes(name.encode())
                tool = {'path': str(tool_path), 'sha256': current.evidence_io.reference(tool_path)['sha256'],
                    'required_identity': name + ' version go1.27.2',
                    'actual_identity': name + ' version go1.27.2'}
                proof['go_provenance']['tools'][name] = tool
                proof['checks'].append({'label': 'go-' + name + '-version',
                    'argv': ['rtk', 'proxy', str(tool_path), '-V']})
            refs = {}
            current.go_provenance(proof, refs)
            self.assertIn(str(path), refs)
            mutations = [lambda p: p.pop('go_provenance'),
                lambda p: p['go_provenance'].update(actual_identity='go version go1.27.3 linux/amd64'),
                lambda p: p['go_provenance'].update(verified=False),
                lambda p: p['environment'].update(GOTOOLCHAIN='auto'),
                lambda p: p['go_provenance'].update(executable_sha256='0' * 64),
                lambda p: p['environment'].update(GOROOT='/different'),
                lambda p: p['go_provenance']['actual_environment'].update(GOVERSION='go1.27.3'),
                lambda p: p['go_provenance']['tools']['compile'].update(actual_identity='compile version go1.27.3'),
                lambda p: p['go_provenance']['tools']['link'].update(path='/different/link'),
                lambda p: p['go_provenance']['tools']['link'].update(sha256='0' * 64),
                lambda p: p['checks'][0]['argv'].__setitem__(2, '/other/go')]
            for mutate in mutations:
                changed = copy.deepcopy(proof)
                mutate(changed)
                with self.assertRaises(ValueError):
                    current.go_provenance(changed, {})
            path.write_bytes(b'changed compiler')
            with self.assertRaisesRegex(ValueError, 'physical reference changed'):
                current.go_provenance(proof, {})

    def test_legacy_go_provenance_allowance_is_explicit(self):
        current.go_provenance({}, {}, allow_legacy=True)
        with self.assertRaisesRegex(ValueError, 'provenance required'):
            current.go_provenance({}, {})

    def test_rejected_native_preserves_only_pre_host_compiler_failure(self):
        with tempfile.TemporaryDirectory(dir=current.evidence_io.STORAGE) as directory:
            root = Path(directory)
            labels = current.CHECKS - {'go-native', 'go-race', 'go-vet', 'native-observer-controls'}
            proof = {'actual_source_commit': current.PARENT, 'host_launched': False,
                'status': 'failed', 'source_copy': str(root / 'source'),
                'complete_source_inventory': {'source': 'hash'}, 'checks': []}
            diagnostic = b'compile: version "go1.27.3" does not match go tool version "go1.27.2"\n'
            for label in sorted(labels - {'composite-build'}) + ['composite-build']:
                check = {'label': label, 'exit_code': int(label == 'composite-build')}
                for channel in ('stdout', 'stderr'):
                    data = (diagnostic if label == 'composite-build' and channel == 'stderr' else
                            b'go version go1.27.2 linux/amd64\n' if label == 'go-version' and channel == 'stdout' else b'')
                    log = root / (label + '.' + channel)
                    log.write_bytes(data)
                    check[channel + '_sha256'] = current.evidence_io.reference(log)['sha256']
                proof['checks'].append(check)
            path = root / 'receipt.json'
            path.write_text(json.dumps(proof))
            with patch.object(current, 'go_provenance'), \
                    patch.object(current.source_inventory, 'verify', return_value=proof['complete_source_inventory']):
                result = current.rejected_native_evidence(path, {})
                self.assertEqual(result['classification'], 'rejected_toolchain_isolation')
                self.assertEqual(result['new_lifecycle_pass'], 0)
                mutations = [lambda p: p.update(host_launched=True),
                    lambda p: p.update(status='pass'), lambda p: p.update(binaries={}),
                    lambda p: p.update(build_ready=True),
                    lambda p: p.update(actual_source_commit='b' * 40),
                    lambda p: p['checks'][0].update(exit_code=1)]
                for mutate in mutations:
                    changed = copy.deepcopy(proof)
                    mutate(changed)
                    path.write_text(json.dumps(changed))
                    with self.assertRaises(ValueError):
                        current.rejected_native_evidence(path, {})
                path.write_text(json.dumps(proof))
                (root / 'composite-build.stderr').write_bytes(b'other failure')
                with self.assertRaisesRegex(ValueError, 'physical reference changed'):
                    current.rejected_native_evidence(path, {})
                proof['checks'][-1]['stderr_sha256'] = current.evidence_io.reference(
                    root / 'composite-build.stderr')['sha256']
                path.write_text(json.dumps(proof))
                with self.assertRaisesRegex(ValueError, 'physical compiler/tool mismatch'):
                    current.rejected_native_evidence(path, {})

    def test_rejected_native_input_is_required(self):
        with self.assertRaises(TypeError):
            current.produce(*(Path('/input') for _ in range(5)))

    def test_cleanup_mutations_are_rejected(self):
        mutations = [lambda row: row['controller'].update(surviving_namespace_pid_count=1),
            lambda row: row['driver'].update(remaining_owned_process_count=1),
            lambda row: row['controller'].update(namespace_pin_verified=False),
            lambda row: row['artifact_integrity_issues'].append({'kind': 'changed'})]
        for mutate in mutations:
            row = observed()
            mutate(row)
            with self.assertRaisesRegex(ValueError, 'cleanup or physical integrity'):
                current.observed_contract(row, self.proof)

    def test_revision_and_original_id_injection_are_rejected(self):
        review = {'parent_sha': current.PARENT, 'host_lifecycle_qualified': False,
            'oracle_progress_assigned': False, 'scenarios': [
                {'scenario': scenario, 'route': route, 'original_oracle_case_ids': [],
                 'host_lifecycle_qualified': False} for scenario, route in current.SCENARIOS.items()]}
        current.nonqualification(review)
        review['parent_sha'] = 'b' * 40
        with self.assertRaisesRegex(ValueError, 'revision differs'):
            current.nonqualification(review)
        review['parent_sha'] = current.PARENT
        review['scenarios'][0]['original_oracle_case_ids'] = ['original']
        with self.assertRaisesRegex(ValueError, 'original ID injection'):
            current.nonqualification(review)

    def test_changed_file_hash_is_rejected(self):
        with tempfile.TemporaryDirectory(dir=current.evidence_io.STORAGE) as directory:
            path = Path(directory) / 'receipt.json'
            path.write_text('{}')
            original = current.evidence_io.reference(path)
            path.write_text('{"changed":true}')
            with self.assertRaisesRegex(ValueError, 'physical reference changed'):
                current.bind(path, original['sha256'], {})

    def test_supplement_requires_admission_input(self):
        with self.assertRaises(TypeError):
            current.produce(Path('/native'), review=Path('/review'))

    def test_validation_replays_and_rejects_supplement_mutation(self):
        ref = {'path': '/native', 'sha256': 'native', 'bytes': 1}
        supplement = {'inputs': {name: dict(ref) for name in (
            'native', 'admission_review', 'review', 'superseded_native', 'superseded_review', 'rejected_native')},
                      'new_lifecycle_pass': 0}
        with patch.object(current.evidence_io, 'read_json', return_value=supplement), \
                patch.object(current.evidence_io, 'reference', return_value=ref), \
                patch.object(current, 'produce', return_value=copy.deepcopy(supplement)) as replay:
            self.assertEqual(current.validate(Path('/supplement')), supplement)
            replay.assert_called_once()
            supplement['new_lifecycle_pass'] = 1
            with self.assertRaisesRegex(ValueError, 'fresh validation'):
                current.validate(Path('/supplement'))


if __name__ == '__main__':
    unittest.main()
