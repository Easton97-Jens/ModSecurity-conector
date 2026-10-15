"""Prepare source-only central capture inputs for a fresh isolated Traefik run.

The reviewed controller is supplied separately. This script never launches it.
Historical source snapshots supply build scaffolding, never runtime evidence.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil


def validate_output(path, *, fresh):
    """Reject unsafe destinations before copying, creating or chmodding anything.

    The configured storage root is a control-plane boundary, not a candidate
    checkout. Its own Git metadata is outside the disposable destination tree.
    """
    path = Path(path)
    storage = Path(os.environ.get('CODEX_TEMP_ROOT', '/var/tmp/codex/ModSecurity-conector'))
    if not path.is_absolute() or not storage.is_absolute() or '..' in path.parts:
        raise ValueError('absolute normalized external output required')
    for item in (path, *path.parents, storage, *storage.parents):
        if item.is_symlink():
            raise ValueError('symlink output components are forbidden')
    if path.resolve() != path or storage.resolve() != storage:
        raise ValueError('physical output path required')
    if not storage.is_dir() or storage not in path.parents:
        raise ValueError('output outside configured external storage')
    for ancestor in (path, *path.parents):
        if ancestor == storage:
            break
        metadata = ancestor / '.git'
        if metadata.exists() or metadata.is_symlink():
            raise ValueError('Git checkout/metadata destination is forbidden')
    if fresh and path.exists():
        raise ValueError('fresh output required')
    if not fresh and not path.is_dir():
        raise ValueError('existing physical output directory required')
    return path


def validate_prepared_root(root):
    root = validate_output(root, fresh=False)
    for name in ('source', 'fixtures', 'artifacts'):
        validate_output(root / name, fresh=False)
    return root


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def replace_once(text, before, after):
    if text.count(before) != 1:
        raise ValueError('central driver template changed: ' + before[:80])
    return text.replace(before, after)


def seal(root):
    inventory = {'files': {}, 'symlinks': {}}
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            raise ValueError('symlink prohibited: ' + str(path))
        if path.is_file():
            inventory['files'][str(path.relative_to(root))] = sha(path)
            path.chmod(0o555 if path.stat().st_mode & 0o111 else 0o444)
    for path in sorted(root.rglob('*'), reverse=True):
        if path.is_dir():
            path.chmod(0o555)
    root.chmod(0o555)
    return inventory


def prepare(repo, historical, output):
    output = validate_output(output, fresh=True)
    output.mkdir(parents=True, mode=0o700)
    source, fixtures = output / 'source', output / 'fixtures'
    previous = historical / 'traefik-lifecycle/execution-review/inputs-v4'
    shutil.copytree(previous / 'source', source)
    for path in (source, *source.rglob('*')):
        path.chmod(0o700 if path.is_dir() or path.stat().st_mode & 0o111 else 0o600)
    capture_root = repo / 'ci/runtime/lifecycle/i12'
    spec = importlib.util.spec_from_file_location('capture_sources', capture_root / 'capture_sources.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    registry = module.Registry(capture_root, repo)
    profile = registry.manifest['profiles']['traefik-native']
    overlays = {}
    # Refresh every actual build input from this checkout before instrumentation.
    product_paths = [*sorted((repo / 'common').rglob('*.c')), *sorted((repo / 'common').rglob('*.h')),
                     *sorted((repo / 'connectors/traefik').rglob('*.c')),
                     *sorted((repo / 'connectors/traefik').rglob('*.h')),
                     *sorted((repo / 'connectors/traefik/native_middleware').glob('*.go')),
                     repo / 'connectors/profile_registry.c']
    bindings = {}
    for path in product_paths:
        relative = str(path.relative_to(repo))
        destination = source / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, destination)
        bindings[relative] = sha(path)
    for relative, entry in profile['source_targets'].items():
        path = source / relative
        # Verify the declared current base before applying any capture delta.
        if entry['before_sha256'] is not None:
            base = repo / relative
            if sha(base) != entry['before_sha256']:
                raise ValueError('current capture base differs: ' + relative)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(registry.content(entry['sha256']))
        if relative in bindings and bindings[relative] != sha(path):
            overlays[relative] = {'baseline_a9_sha256': bindings[relative], 'instrumented_sha256': sha(path),
                                  'scope': 'central traefik-native capture-only observation'}
    fixtures.mkdir()
    for relative, entry in profile['capture_files'].items():
        if relative.startswith('drivers/'):
            path = fixtures / Path(relative).name
            path.write_bytes(registry.content(entry['sha256']))
            if path.suffix == '.sh':
                path.chmod(0o700)
    for name in ('client.py', 'backend.py'):
        shutil.copyfile(Path(__file__).parent / name, fixtures / name)
    driver = (fixtures / 'driver.py').read_text()
    driver = replace_once(driver, "RUN = 'tf-i12-eos-20261014'", "RUN = 'tf-i12-native-20261015'")
    driver = replace_once(driver, "'delivery_base': '02754040bced960cfc1857416cd7101bb3116ef4'", "'delivery_base': 'f27eb59b53beff6f65384fc2e5037881a3052c01'")
    driver = replace_once(driver, "'product_base': 'a9d48bb58aa948aea7d79e20cdf09d3f239b7808'", "'product_base': 'f27eb59b53beff6f65384fc2e5037881a3052c01'")
    start = driver.index('    product = json.loads(')
    end = driver.index("    write('build-manifest.json'", start)
    driver = driver[:start] + "    write('current-product-binding.json', json.loads((FIXTURES / 'current-product-binding.json').read_text()))\n" + driver[end:]
    driver = replace_once(driver, "    os.environ.update(env)", "    os.environ.update(env)")
    marker = "    (TASK / 'rules.conf').write_text('\\n'.join(rules) + '\\n')"
    additions = '''    rules.extend([
        'SecRule REQUEST_URI "@streq /i12-eos-p1-deny" "id:1999201,phase:1,deny,status:403,log"',
        'SecRule REQUEST_BODY "@contains i12-p2-deny" "id:1999202,phase:2,deny,status:403,log"',
        'SecRule RESPONSE_HEADERS:X-I12-P3 "@streq deny" "id:1999203,phase:3,deny,status:403,log"',
        'SecRule RESPONSE_BODY "@contains p4-safe-late" "id:1999204,phase:4,deny,status:403,log"',
        'SecRule RESPONSE_BODY "@contains i12-response-marker" "id:1999205,phase:4,pass,log,msg:\\'i12-mime-body-proof\\'"'])
'''
    driver = replace_once(driver, marker, additions + marker)
    old = "        for label, nonce in (('target', TARGET), ('neighbor', NEIGHBOR)):\n            transaction_id = 'tf-' + nonce\n            execute(f'client-{label}', ['/usr/local/bin/python3', '-P', FIXTURES / 'client.py', str(host_port),\n                                      nonce, transaction_id, label], env)\n            time.sleep(0.15)\n            snapshot(f'after-{label}', processes)"
    new = "        for label, expected in (('allow-chunks',200),('p1-deny',403),('p2-deny',403),('p3-deny',403),('p4-safe-late',200),('mime-out',200),('neighbor',200)):\n            execute(f'client-{label}', ['/usr/local/bin/python3', '-P', FIXTURES / 'client.py', str(host_port), label, str(expected)], env)\n            time.sleep(0.15)\n            snapshot(f'after-{label}', processes)"
    driver = replace_once(driver, old, new)
    driver = driver.replace("'selected_case_count': 1", "'selected_case_count': 6")
    (fixtures / 'driver.py').write_text(driver)
    save(fixtures / 'current-product-binding.json', {'checkout': str(repo), 'checkout_base': 'f27eb59b53beff6f65384fc2e5037881a3052c01',
         'product_inputs': bindings, 'capture_overlays': overlays, 'central_manifest_sha256': sha(capture_root / 'manifest.json'),
         'historical_build_scaffolding': str(previous / 'source'), 'runtime_replay': False})
    shutil.copytree(historical / 'sealed-common-inputs/artifacts/traefik', output / 'artifacts/traefik')
    ledgers = {}
    for name in ('source', 'fixtures', 'artifacts'):
        ledger = output / (name + '-ledger.json')
        save(ledger, seal(output / name))
        ledger.chmod(0o444)
        ledgers[name] = ledger
    admission = {'mode': 'nonroot', 'timeout_seconds': 1000, 'setup_timeout_seconds': 120,
                 'resource_limits': {'memory_bytes': 3221225472, 'processes': 384, 'output_bytes': 2147483648},
                 'argv': ['/usr/local/bin/python3', '-P', '/mnt/fixtures/driver.py'],
                 'bindings': [{'source': str(output / name), 'target': target, 'ledger': str(ledgers[name]),
                               'ledger_sha256': sha(ledgers[name])} for name, target in
                              [('source', '/mnt/src'), ('fixtures', '/mnt/fixtures'), ('artifacts', '/mnt/artifacts')]],
                 'environment': {'CONNECTOR_ROOT': '/mnt/src'}}
    save(output / 'admission.json', admission)
    (output / 'admission.json').chmod(0o444)
    print(json.dumps({'prepared': str(output), 'admission_sha256': sha(output / 'admission.json'), 'runtime_qualified': False}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--historical', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    prepare(args.repo.resolve(), args.historical.resolve(), args.output)
