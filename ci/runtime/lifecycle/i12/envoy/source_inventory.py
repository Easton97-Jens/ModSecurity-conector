"""Verify every source byte against the retained Git archive and capture receipt."""
import hashlib
import io
import json
from pathlib import Path
import re
import tarfile

ADAPTER_CONTRACT = 'i12.envoy.preserve-a622-observer.v1'
MANIFEST = 'ci/runtime/lifecycle/i12/manifest.json'
OBSERVER_HASHES = {
    'ci/runtime/lifecycle/native-lifecycle-observer.c': (
        'ad8e5e36a17e746cf202c685dbb529fc09717f5c25441b713fa369420aa55ac6',
        '0d903fc5e6432769a136931b7ebea16a6f87db941d28d23583ccccf4c75e6537'),
    'ci/runtime/lifecycle/native-lifecycle-observer.h': (
        'f9f63b62ba8efc555dc20e673cc02251d5ab6c2ab17d8f5efa760d0d97146dcd',
        '5b7d8fa7c327017cafb05b1e932f70eefe8641797751a0dc19df0337f4893b1b'),
}


def full_revision(value):
    if not isinstance(value, str) or re.fullmatch('[0-9a-f]{40}', value) is None:
        raise ValueError('explicit full lowercase source revision required')
    return value


def observer_contract(profile):
    targets = profile['source_targets']
    for name in targets:
        if Path(name).name in ('native-lifecycle-observer.c', 'native-lifecycle-observer.h') and name not in OBSERVER_HASHES:
            raise ValueError('foreign observer target')
    for name, (historical, _current) in OBSERVER_HASHES.items():
        if targets.get(name) != {'before_sha256': historical, 'sha256': historical, 'mode': 420}:
            raise ValueError('historical observer manifest contract differs: ' + name)


def adapter_metadata(manifest, before, revision, manifest_hash):
    profile = manifest['profiles']['envoy']
    observer_contract(profile)
    if any(before.get(name) != current for name, (_old, current) in OBSERVER_HASHES.items()):
        raise ValueError('unknown archived observer hashes')
    return {'contract': ADAPTER_CONTRACT, 'original_manifest_sha256': manifest_hash,
            'archived_revision': full_revision(revision), 'resolved_revision': revision,
            'applied_targets': {name: entry['sha256'] for name, entry in profile['source_targets'].items()
                                if name not in OBSERVER_HASHES},
            'preserved_targets': {name: {'historical_before_sha256': old, 'archived_sha256': current}
                                  for name, (old, current) in OBSERVER_HASHES.items()}}


def verify_adapter(proof, expected, manifest):
    """Derive every permitted omission/write from the original archived manifest."""
    revision = full_revision(proof['actual_source_commit'])
    profile = manifest['profiles']['envoy']
    before = {name: expected.get(name) for name in profile['source_targets']}
    metadata = adapter_metadata(manifest, before, revision, expected[MANIFEST])
    if proof['envoy_capture_adapter'] != metadata or proof['source_before_overlay'] != before:
        raise ValueError('Envoy observer adapter metadata differs from archive')
    if proof['manifest_sha256'] != expected[MANIFEST]:
        raise ValueError('original manifest hash differs from archive')
    application = proof['capture_application']
    writes = dict(metadata['applied_targets'])
    writes.update({'.i12-capture/envoy/' + name: entry['sha256']
                   for name, entry in profile['capture_files'].items()})
    if (application['profile'] != 'envoy' or application['source_copy'] != proof['source_copy']
            or application['capture_manifest_sha256'] != expected[MANIFEST]
            or application['actual_before_sha256'] != {name: before[name] for name in metadata['applied_targets']}
            or application['exact_written_sha256'] != writes):
        raise ValueError('Envoy observer adapter application differs from original manifest')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def tree_inventory(source):
    result = {}
    for path in sorted(source.rglob('*')):
        if path.is_symlink() or not (path.is_dir() or path.is_file()):
            raise ValueError('nonphysical source input')
        if path.is_file():
            if path.stat().st_nlink != 1:
                raise ValueError('hard-linked source input')
            result[str(path.relative_to(source))] = digest(path.read_bytes())
    return result


def archive_inventory(data):
    expected = {}
    seen = set()
    manifest = None
    with tarfile.open(fileobj=io.BytesIO(data)) as stream:
        for member in stream:
            path = Path(member.name)
            if path.is_absolute() or '..' in path.parts or not (member.isfile() or member.isdir()):
                raise ValueError('unsupported source archive entry')
            if member.name in seen:
                raise ValueError('duplicate source archive entry')
            seen.add(member.name)
            if member.isfile():
                body = stream.extractfile(member).read()
                expected[member.name] = digest(body)
                if member.name == 'ci/runtime/lifecycle/i12/manifest.json':
                    manifest = json.loads(body)
    if manifest is None:
        raise ValueError('source archive manifest unavailable')
    return expected, manifest


def expected_inventory(proof):
    """Reconstruct old receipts too; never bless the current source by hashing it."""
    archive = Path(proof['source_copy']).parent / 'native-build/source-archive.stdout'
    data = archive.read_bytes()
    checks = [check for check in proof['checks'] if check['label'] == 'source-archive'
              and check['exit_code'] == 0
              and check['argv'][-3:] == ['archive', '--format=tar', proof['actual_source_commit']]]
    if len(checks) != 1 or checks[0]['stdout_sha256'] != digest(data):
        raise ValueError('hash-bound original Git archive unavailable')
    expected, manifest = archive_inventory(data)
    if ('envoy' in manifest.get('profiles', {})
            and any(expected.get(name) != old for name, (old, _current) in OBSERVER_HASHES.items())
            and 'envoy_capture_adapter' not in proof):
        raise ValueError('changed archived observer requires explicit adapter metadata')
    if 'source_revision_selection' in proof:
        revision = full_revision(proof['actual_source_commit'])
        if proof['source_revision_selection'] != {'requested': revision, 'resolved': revision}:
            raise ValueError('source revision selection differs')
        resolutions = [check for check in proof['checks'] if check['label'] == 'source-head'
                       and check['exit_code'] == 0
                       and check['argv'] == ['rtk', 'proxy', 'git', 'rev-parse', '--verify', revision + '^{commit}']
                       and check['stdout_sha256'] == digest((revision + '\n').encode())]
        if len(resolutions) != 1:
            raise ValueError('source revision resolution unavailable')
    if 'envoy_capture_adapter' in proof:
        if 'source_revision_selection' not in proof:
            raise ValueError('adapter requires explicit source revision selection')
        verify_adapter(proof, expected, manifest)
    expected.update(proof['capture_application']['exact_written_sha256'])
    prefix = '.i12-capture/envoy/source-copy-tests/'
    copies = {path.removeprefix(prefix): value for path, value in expected.items()
              if path.startswith(prefix)}
    for relative, value in copies.items():
        if relative in expected:
            raise ValueError('capture test overwrites original source')
        expected[relative] = value
    marker = {'format': 'i12-disposable-source-copy-v1', 'path': proof['source_copy'],
              'disposable': True, 'parent_sha': manifest['delivery_product_baseline']}
    expected['.i12-disposable-source-copy.json'] = digest(json.dumps(marker).encode())
    expected['i12-source-application-receipt.json'] = digest(
        (json.dumps(proof['capture_application'], indent=2) + '\n').encode())
    return expected


def verify(source, proof):
    expected = expected_inventory(proof)
    actual = tree_inventory(source)
    changed = sorted(name for name in set(expected) | set(actual) if expected.get(name) != actual.get(name))
    if changed:
        raise ValueError('complete build-source inventory mismatch: ' + ', '.join(changed[:8]))
    return expected
