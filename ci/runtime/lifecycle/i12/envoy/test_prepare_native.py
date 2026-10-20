"""Current-base observer adapter controls against the original capture registry."""
import copy
import io
import json
from pathlib import Path
import tarfile
import tempfile
from types import SimpleNamespace
import unittest

import prepare_native as prepare
import source_inventory as inventory


class ObserverAdapterControls(unittest.TestCase):
    def setUp(self):
        self.repository = Path(__file__).resolve().parents[5]
        self.capture = prepare.load(self.repository / 'ci/runtime/lifecycle/i12/capture_sources.py',
                                    'adapter_capture_controls')
        self.registry = self.capture.Registry(
            root=self.repository / 'ci/runtime/lifecycle/i12', repository=self.repository)
        self.temporary = tempfile.TemporaryDirectory(
            dir=self.registry.manifest['authorized_storage_root'])
        self.root = Path(self.temporary.name)
        self.source = self.root / 'source'
        self.source.mkdir()
        self.profile = self.registry.manifest['profiles']['envoy']
        self.original = {inventory.MANIFEST: (self.registry.root / 'manifest.json').read_bytes()}
        for name in self.profile['source_targets']:
            self.original[name] = (self.repository / name).read_bytes()
        for name, data in self.original.items():
            path = self.source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        marker = {'format': 'i12-disposable-source-copy-v1', 'path': str(self.source),
                  'disposable': True, 'parent_sha': self.registry.manifest['delivery_product_baseline']}
        (self.source / self.capture.MARKER).write_text(json.dumps(marker))
        self.proof = {'source_copy': str(self.source), 'actual_source_commit': 'a' * 40,
                      'manifest_sha256': prepare.sha(self.source / inventory.MANIFEST),
                      'source_before_overlay': {name: prepare.sha(self.source / name)
                                                for name in self.profile['source_targets']}}

    def tearDown(self):
        self.temporary.cleanup()

    def apply(self):
        self.proof['capture_application'] = prepare.apply_capture(
            self.capture, self.registry, self.source, self.proof)

    def bind_archive(self):
        output = io.BytesIO()
        with tarfile.open(fileobj=output, mode='w') as stream:
            for name, body in self.original.items():
                member = tarfile.TarInfo(name)
                member.size = len(body)
                stream.addfile(member, io.BytesIO(body))
        out = self.root / 'native-build'
        out.mkdir()
        (out / 'source-archive.stdout').write_bytes(output.getvalue())
        revision = self.proof['actual_source_commit']
        self.proof['source_revision_selection'] = {'requested': revision, 'resolved': revision}
        self.proof['checks'] = [
            {'label': 'source-archive', 'exit_code': 0,
             'argv': ['rtk', 'proxy', 'git', 'archive', '--format=tar', revision],
             'stdout_sha256': inventory.digest(output.getvalue())},
            {'label': 'source-head', 'exit_code': 0,
             'argv': ['rtk', 'proxy', 'git', 'rev-parse', '--verify', revision + '^{commit}'],
             'stdout_sha256': inventory.digest((revision + '\n').encode())}]
        for name in self.profile['capture_files']:
            if name.startswith('source-copy-tests/'):
                relative = name.removeprefix('source-copy-tests/')
                (self.source / relative).write_bytes((self.source / '.i12-capture/envoy' / name).read_bytes())

    def test_preserves_exact_current_observers_and_full_inventory(self):
        original_manifest = copy.deepcopy(self.registry.manifest)
        self.apply()
        self.assertEqual(self.registry.manifest, original_manifest)
        metadata = self.proof['envoy_capture_adapter']
        self.assertEqual(metadata['contract'], inventory.ADAPTER_CONTRACT)
        self.assertEqual(len(metadata['applied_targets']), 9)
        self.assertEqual(set(metadata['preserved_targets']), set(inventory.OBSERVER_HASHES))
        for name, (_old, current) in inventory.OBSERVER_HASHES.items():
            self.assertEqual(prepare.sha(self.source / name), current)
            self.assertNotIn(name, self.proof['capture_application']['exact_written_sha256'])
        self.bind_archive()
        inventory.verify(self.source, self.proof)
        for name in inventory.OBSERVER_HASHES:
            with self.subTest(name=name):
                (self.source / name).write_bytes(b'changed observer')
                with self.assertRaisesRegex(ValueError, 'inventory mismatch'):
                    inventory.verify(self.source, self.proof)
                (self.source / name).write_bytes(self.original[name])

    def test_historical_observers_use_original_application_without_adapter(self):
        for name, (old, _current) in inventory.OBSERVER_HASHES.items():
            self.original[name] = self.registry.content(old)
            (self.source / name).write_bytes(self.original[name])
            self.proof['source_before_overlay'][name] = old
        self.apply()
        self.assertNotIn('envoy_capture_adapter', self.proof)
        self.assertEqual(len(self.proof['capture_application']['actual_before_sha256']), 11)
        self.bind_archive()
        self.proof.pop('source_revision_selection')
        self.proof['checks'][1]['argv'] = ['rtk', 'proxy', 'git', 'rev-parse', 'HEAD']
        expected = inventory.verify(self.source, self.proof)
        for name, (old, _current) in inventory.OBSERVER_HASHES.items():
            self.assertEqual(expected[name], old)
            self.assertEqual(prepare.sha(self.source / name), old)
            self.assertEqual(self.proof['capture_application']['exact_written_sha256'][name], old)
        # A legacy receipt remains subject to the complete physical inventory.
        name = next(iter(inventory.OBSERVER_HASHES))
        (self.source / name).write_bytes(b'changed historical observer')
        with self.assertRaisesRegex(ValueError, 'inventory mismatch'):
            inventory.verify(self.source, self.proof)

    def test_unknown_or_mixed_observer_hashes_fail_before_overlay(self):
        for replacement in (b'unknown observer', self.registry.content(
                next(iter(inventory.OBSERVER_HASHES.values()))[0])):
            with self.subTest(replacement=inventory.digest(replacement)):
                name = next(iter(inventory.OBSERVER_HASHES))
                (self.source / name).write_bytes(replacement)
                self.proof['source_before_overlay'][name] = inventory.digest(replacement)
                with self.assertRaisesRegex(ValueError, 'unknown archived observer'):
                    self.apply()
                self.assertFalse((self.source / '.i12-capture').exists())

    def test_foreign_observer_and_changed_historical_manifest_fail_closed(self):
        targets = self.profile['source_targets']
        name = next(iter(inventory.OBSERVER_HASHES))
        targets['foreign/native-lifecycle-observer.c'] = targets[name]
        with self.assertRaisesRegex(ValueError, 'foreign observer'):
            self.apply()
        del targets['foreign/native-lifecycle-observer.c']
        targets[name] = {**targets[name], 'before_sha256': '0' * 64}
        with self.assertRaisesRegex(ValueError, 'historical observer manifest'):
            self.apply()
        self.assertFalse((self.source / '.i12-capture').exists())

    def test_corrupt_unselected_registry_object_is_not_skipped(self):
        # Poison an object outside Envoy, retaining its original identity.
        identity = next(key for key in self.registry.manifest['objects']
                        if key not in {entry['sha256'] for entry in self.profile['source_targets'].values()})
        self.registry.manifest['objects'][identity] = {'kind': 'unknown-corrupt-kind'}
        with self.assertRaisesRegex(ValueError, 'Unknown source object kind'):
            self.apply()
        self.assertFalse((self.source / '.i12-capture').exists())

    def test_metadata_omissions_substitutions_and_extra_writes_are_rejected(self):
        self.apply()
        self.bind_archive()
        baseline = copy.deepcopy(self.proof)
        mutations = [
            lambda proof: proof.pop('envoy_capture_adapter'),
            lambda proof: proof.pop('source_revision_selection'),
            lambda proof: proof['envoy_capture_adapter'].update(contract='different'),
            lambda proof: proof['envoy_capture_adapter']['preserved_targets'].pop(next(iter(inventory.OBSERVER_HASHES))),
            lambda proof: proof['envoy_capture_adapter']['preserved_targets'].update({'foreign/observer.c': {}}),
            lambda proof: proof['envoy_capture_adapter'].update(original_manifest_sha256='0' * 64),
            lambda proof: proof['envoy_capture_adapter'].update(archived_revision='b' * 40),
            lambda proof: proof['envoy_capture_adapter']['applied_targets'].pop(next(iter(
                proof['envoy_capture_adapter']['applied_targets']))),
            lambda proof: proof['capture_application']['exact_written_sha256'].update({'extra.c': '0' * 64}),
            lambda proof: proof['source_before_overlay'].update({next(iter(inventory.OBSERVER_HASHES)): '0' * 64}),
            lambda proof: proof['source_revision_selection'].update(requested='HEAD'),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(mutation=index):
                proof = copy.deepcopy(baseline)
                mutate(proof)
                with self.assertRaises(ValueError):
                    inventory.verify(self.source, proof)

    def test_applied_and_preserved_hash_substitutions_are_rejected(self):
        self.apply()
        self.bind_archive()
        baseline = copy.deepcopy(self.proof)
        applied = next(iter(baseline['envoy_capture_adapter']['applied_targets']))
        for name, field in ((applied, 'applied_targets'), *(
                (name, field) for name in inventory.OBSERVER_HASHES
                for field in ('archived_sha256', 'historical_before_sha256'))):
            with self.subTest(target=name, field=field):
                proof = copy.deepcopy(baseline)
                metadata = proof['envoy_capture_adapter']
                if field == 'applied_targets':
                    metadata[field][name] = '0' * 64
                else:
                    metadata['preserved_targets'][name][field] = '0' * 64
                with self.assertRaisesRegex(ValueError, 'adapter metadata differs from archive'):
                    inventory.verify(self.source, proof)

    def test_application_profile_manifest_and_before_hash_substitutions_are_rejected(self):
        self.apply()
        self.bind_archive()
        baseline = copy.deepcopy(self.proof)
        target = next(iter(baseline['capture_application']['actual_before_sha256']))
        mutations = {
            'profile': lambda application: application.update(profile='foreign'),
            'capture_manifest_sha256': lambda application: application.update(capture_manifest_sha256='0' * 64),
            'actual_before_sha256': lambda application: application['actual_before_sha256'].update({target: '0' * 64}),
        }
        for field, mutate in mutations.items():
            with self.subTest(field=field):
                proof = copy.deepcopy(baseline)
                mutate(proof['capture_application'])
                with self.assertRaisesRegex(ValueError, 'adapter application differs from original manifest'):
                    inventory.verify(self.source, proof)

    def test_full_sha_is_required_and_resolution_must_be_identical(self):
        for revision in ('HEAD', 'a62296f', 'A' * 40, 'a' * 40 + '^', None):
            with self.subTest(revision=revision), self.assertRaises(ValueError):
                prepare.prepare_source(self.source, {}, lambda *_args: b'', revision)
        calls = []
        def changed_resolution(label, argv):
            calls.append((label, argv))
            return ('b' * 40 + '\n').encode()
        with self.assertRaisesRegex(ValueError, 'resolved source revision differs'):
            prepare.prepare_source(self.source, {}, changed_resolution, 'a' * 40)
        self.assertEqual(calls, [('source-head', ['git', 'rev-parse', '--verify', 'a' * 40 + '^{commit}'])])


class GoProvenanceControls(unittest.TestCase):
    def setUp(self):
        manifest = Path(__file__).resolve().parents[1] / 'manifest.json'
        storage = json.loads(manifest.read_text())['authorized_storage_root']
        self.temporary = tempfile.TemporaryDirectory(dir=storage)
        self.root = Path(self.temporary.name)
        self.go = self.root / 'go'
        self.go.write_bytes(b'physical test executable identity')
        self.go.chmod(0o755)
        self.env = {'PATH': str(self.root), 'GOTOOLCHAIN': 'local'}
        self.profile = {'provenance': {'go_version': '1.27.2'}}
        self.receipt = {}
        self.calls = []
        self.output = b'go version go1.27.2 linux/amd64\n'

        class Runner:
            def __call__(_runner, label, argv, *_args):
                self.calls.append((label, argv))
                return self.output

            def save(_runner):
                pass

        self.run = Runner()

    def tearDown(self):
        self.temporary.cleanup()

    def capture(self):
        prepare.record_go_provenance(self.go, self.env, self.receipt, self.run, self.profile)

    def test_exact_identity_records_required_actual_and_physical_executable(self):
        self.capture()
        self.assertEqual(self.calls, [('go-version', [self.go, 'version'])])
        self.assertEqual(self.receipt['go_provenance'], {
            'required_version': '1.27.2', 'required_identity': 'go version go1.27.2 linux/amd64',
            'actual_identity': 'go version go1.27.2 linux/amd64',
            'configured_path': str(self.go), 'executable_path': str(self.go),
            'executable_sha256': prepare.sha(self.go), 'verified': True})

    def test_wrong_patch_release_is_recorded_and_rejected_before_any_build(self):
        self.output = b'go version go1.27.3 linux/amd64\n'
        sdk = self.root / 'libmodsecurity.so'
        sdk.write_bytes(b'test sdk identity')
        self.profile['provenance']['sdk_image_sha256'] = prepare.sha(sdk)
        args = SimpleNamespace(go=self.go, sdk_library=sdk)
        with self.assertRaisesRegex(ValueError, 'exact capture provenance'):
            prepare.compile_native(args, self.root / 'absent-source', self.root,
                                   self.env, self.receipt, self.run, self.profile)
        self.assertEqual(self.calls, [('go-version', [self.go, 'version'])])
        self.assertFalse(self.receipt['go_provenance']['verified'])
        self.assertEqual(self.receipt['go_provenance']['actual_identity'], 'go version go1.27.3 linux/amd64')
        self.assertNotIn('build_ready', self.receipt)

    def test_format_platform_development_and_extra_output_mutations_are_rejected(self):
        for output in (b'go version go1.27.2 linux/arm64\n', b'go version go1.27.2 darwin/amd64\n',
                       b'go version devel go1.27.2 linux/amd64\n', b'go version go1.27.2rc1 linux/amd64\n',
                       b'go version go1.27.2 linux/amd64', b'go version go1.27.2 linux/amd64\r\n',
                       b'go version go1.27.2 linux/amd64\nextra\n', b'go version go1.27.2 linux/amd64 \n',
                       b'go version go1.27.2 linux/amd64\xff\n', b''):
            with self.subTest(output=output):
                self.output = output
                with self.assertRaisesRegex(ValueError, 'exact capture provenance'):
                    self.capture()
                self.assertFalse(self.receipt['go_provenance']['verified'])

    def test_inexact_manifest_version_is_rejected_before_invocation(self):
        for version in ('go1.27.2', '1.27', '1.27.2rc1', '1.27.2\n', None):
            with self.subTest(version=version):
                self.profile['provenance']['go_version'] = version
                with self.assertRaisesRegex(ValueError, 'exact capture Go version required'):
                    self.capture()
        self.assertEqual(self.calls, [])

    def test_cross_platform_auto_toolchain_and_other_path_selection_are_rejected(self):
        for changes in ({'GOOS': 'windows'}, {'GOARCH': 'arm64'}, {'GOTOOLCHAIN': 'auto'}, {'PATH': ''}):
            with self.subTest(changes=changes):
                self.env = {'PATH': str(self.root), 'GOTOOLCHAIN': 'local', **changes}
                with self.assertRaisesRegex(ValueError, 'selected local Go executable'):
                    self.capture()
        self.assertEqual(self.calls, [])

    def test_changed_executable_during_version_capture_is_rejected(self):
        def changing_run(label, argv):
            self.go.write_bytes(b'substituted Go executable')
            return self.output
        changing_run.save = lambda: None
        self.run = changing_run
        with self.assertRaisesRegex(ValueError, 'changed during provenance capture'):
            self.capture()
        self.assertFalse(self.receipt['go_provenance']['verified'])


if __name__ == '__main__':
    unittest.main()
