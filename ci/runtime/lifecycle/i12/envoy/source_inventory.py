"""Verify every source byte against the retained Git archive and capture receipt."""
import hashlib
import io
import json
from pathlib import Path
import tarfile


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


def expected_inventory(proof):
    """Reconstruct old receipts too; never bless the current source by hashing it."""
    archive = Path(proof['source_copy']).parent / 'native-build/source-archive.stdout'
    data = archive.read_bytes()
    checks = [check for check in proof['checks'] if check['label'] == 'source-archive'
              and check['exit_code'] == 0
              and check['argv'][-3:] == ['archive', '--format=tar', proof['actual_source_commit']]]
    if len(checks) != 1 or checks[0]['stdout_sha256'] != digest(data):
        raise ValueError('hash-bound original Git archive unavailable')
    expected = {}
    with tarfile.open(fileobj=io.BytesIO(data)) as stream:
        for member in stream:
            path = Path(member.name)
            if path.is_absolute() or '..' in path.parts or not (member.isfile() or member.isdir()):
                raise ValueError('unsupported source archive entry')
            if member.isfile():
                body = stream.extractfile(member).read()
                expected[member.name] = digest(body)
                if member.name == 'ci/runtime/lifecycle/i12/manifest.json':
                    manifest = json.loads(body)
    expected.update(proof['capture_application']['exact_written_sha256'])
    prefix = '.i12-capture/envoy/source-copy-tests/'
    for path, value in list(expected.items()):
        if path.startswith(prefix):
            relative = path.removeprefix(prefix)
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
