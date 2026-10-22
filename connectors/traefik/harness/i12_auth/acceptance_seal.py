"""Seal selected Traefik inputs for the existing reviewed controller; never launch."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import acceptance_validate


ROOT = Path('/var/tmp/codex/ModSecurity-conector/runs/i12-traefik-acceptance-20261015/auth-current')
ISOLATION = ROOT / 'isolation'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')
    path.chmod(0o444)


def binding(source, label, target):
    if source.parent.parent != ROOT or source.resolve(strict=True) != source:
        raise ValueError('exact task-owned source/fixture root required')
    paths = [source, *source.rglob('*')]
    records = {}
    for path in paths:
        state = path.lstat()
        if state.st_uid != 0 or not (stat.S_ISREG(state.st_mode) or stat.S_ISDIR(state.st_mode)):
            raise ValueError('only root-owned regular private inputs admitted')
        if path.is_file():
            records[str(path.relative_to(source))] = sha(path)
    for path in reversed(paths):
        path.chmod(0o555 if path.is_dir() or path.stat().st_mode & 0o111 else 0o444)
    ledger = ISOLATION / (label + '-' + source.name + '-ledger.json')
    save(ledger, {'files': records})
    return {'source': str(source), 'ledger': str(ledger), 'ledger_sha256': sha(ledger), 'target': target}


def seal(prepared, artifact_binding):
    if os.geteuid() != 0 or prepared.parent != ROOT or prepared.resolve(strict=True) != prepared:
        raise ValueError('exact owned preparation required')
    if not re.fullmatch(r'(request|companion)-v[0-9]+(?:-benign|-original-causal)?', prepared.name):
        raise ValueError('explicit versioned Traefik preparation required')
    manifest = json.loads((prepared / 'fixtures/acceptance-manifest.json').read_text())
    if sha(prepared / 'fixtures/acceptance_validate.py') != sha(Path(acceptance_validate.__file__)):
        raise ValueError('runtime socket contract must match the reviewed sealed validator source')
    source = json.loads((prepared / 'source/.i12-source-export-manifest.json').read_text())
    template = json.loads((ISOLATION / 'request-v12-spec.json').read_text())
    artifacts = json.loads(artifact_binding.read_text())
    if artifacts['target'] != '/mnt/artifacts' or sha(Path(artifacts['ledger'])) != artifacts['ledger_sha256']:
        raise ValueError('explicit reviewed artifact binding identity required')
    toolchain = Path(artifacts['source']) / 'toolchains/go1.27.2'
    expected_go = '548d3c32f83fa81152f543eb1526be7884cfe0526eb5e9ce29d3eca14786e7e0'
    ledger = json.loads(Path(artifacts['ledger']).read_text())['files']
    if sha(toolchain / 'bin/go') != expected_go or ledger.get('toolchains/go1.27.2/bin/go') != expected_go:
        raise ValueError('private Go1.27.2 must be part of sealed artifact ledger')
    if (toolchain / 'VERSION').read_text().splitlines()[0] != 'go1.27.2':
        raise ValueError('private toolchain VERSION differs')
    # The unchanged private-runtime-v5 admission allowlist excludes toolchain
    # variables. The driver verifies and selects the sealed toolchain internally.
    template['environment'] = {}
    template['bindings'] = [binding(prepared / 'source', prepared.name, '/mnt/src'),
                            binding(prepared / 'fixtures', prepared.name, '/mnt/fixtures'), artifacts]
    template['logical_route'] = manifest['selected_route']
    template['source_revision'] = source['source_revision']
    template['qualification'] = None
    spec = ISOLATION / (prepared.name + '-spec.json')
    save(spec, template)
    return {'spec': str(spec), 'spec_sha256': sha(spec), 'source_revision': source['source_revision'],
            'runtime_provenance_socket_contract': acceptance_validate.PROVENANCE_SOCKET_CONTRACT,
            'runtime_contract_source_sha256': sha(prepared / 'fixtures/acceptance_validate.py'),
            'selected_original_ids': [case['id'] for case in manifest['cases']],
            'host_launched': False, 'qualification': None}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepared', type=Path, required=True)
    parser.add_argument('--artifact-binding', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(seal(args.prepared, args.artifact_binding)))
