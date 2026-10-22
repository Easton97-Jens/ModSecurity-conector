"""Shared source, fixture, spec and build binding for Traefik auth evidence."""
import hashlib
import importlib.util
import json
from pathlib import Path


def read(path):
    return json.loads(path.read_text()) if path.is_file() else None


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def validate_attempt_binding(attempt, prepared):
    """Reject mixed preparations before emitting any source-bearing packet."""
    def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
    def required(path):
        value=read(path)
        if not isinstance(value,dict):raise ValueError('missing binding receipt: '+str(path))
        return value
    controller=required(attempt/'controller-result.json')
    originals=list((attempt/'executed-input-originals').iterdir())
    def retained(digest):
        matches=[path for path in originals if path.is_file() and sha(path)==digest]
        if len(matches)!=1:raise ValueError('unique retained executed-input identity required')
        return matches[0]
    before=controller.get('executed_input_hashes_before')
    if not before or before!=controller.get('executed_input_hashes_after'):
        raise ValueError('controller executed inputs changed or missing')
    for digest in before.values():retained(digest)
    if controller.get('controller_sha256') not in before.values():
        raise ValueError('controller identity is not an executed input')
    spec_hash=controller.get('spec_sha256')
    if spec_hash not in before.values():raise ValueError('spec identity is not an executed input')
    spec=required(retained(spec_hash))
    bindings={row['target']:row for row in spec['bindings']}
    if set(bindings)!={'/mnt/src','/mnt/fixtures','/mnt/artifacts'}:
        raise ValueError('exact source/fixture/artifact bindings required')
    ledgers={}
    for target,binding in bindings.items():
        ledger=required(retained(binding['ledger_sha256']))['files'];ledgers[target]=ledger
        if target!='/mnt/artifacts':
            directory=prepared/('source' if target=='/mnt/src' else 'fixtures')
            if Path(binding['source']).resolve()!=directory.resolve():
                raise ValueError('Prepared path differs from actual executed binding')
            actual={str(p.relative_to(directory)):sha(p) for p in directory.rglob('*') if p.is_file()}
            if actual!=ledger:raise ValueError('Prepared bytes differ from executed ledger: '+target)
    source=required(prepared/'source/.i12-source-export-manifest.json')
    if source['source_revision']!=spec.get('source_revision'):
        raise ValueError('Prepared source revision differs from executed spec')
    manifest=required(prepared/'fixtures/acceptance-manifest.json')
    build=required(attempt/'data/acceptance-build.json')
    summary=required(attempt/'data/acceptance-execution-summary.json')
    if (build.get('source_inputs')!=ledgers['/mnt/src'] or
        build.get('fixture_inputs')!=ledgers['/mnt/fixtures'] or
        build.get('manifest_sha256')!=ledgers['/mnt/fixtures'].get('acceptance-manifest.json') or
        summary.get('runtime_source_manifest_sha256')!=sha(attempt/'data/acceptance-build.json') or
        summary.get('route')!=manifest.get('selected_route') or
        summary.get('original_ids')!=len(manifest['cases']) or
        spec.get('logical_route')!=manifest.get('selected_route')):
        raise ValueError('runtime build/manifest/source/fixture identity differs')
    artifacts=ledgers['/mnt/artifacts']
    if (not artifacts.get('toolchains/go1.27.2/bin/go') or
        not build.get('observer_source_sha256') or not build.get('fault_source_sha256') or
        build.get('host_sha256')!=artifacts.get('traefik/host') or
        build.get('host_sha256')!=sha(attempt/'data/cache/traefik') or
        build.get('engine_sha256')!=sha(attempt/'data/build/service/traefik-forwardauth') or
        build.get('observer_source_sha256')!=ledgers['/mnt/src'].get('ci/runtime/lifecycle/native-lifecycle-observer.c') or
        build.get('fault_source_sha256')!=ledgers['/mnt/fixtures'].get('acceptance_faults.c') or
        build.get('toolchain',{}).get('binary_sha256')!=artifacts.get('toolchains/go1.27.2/bin/go')):
        raise ValueError('runtime artifact/build image identity differs')
    controls=load(Path(__file__).with_name('acceptance_controls.py'),'auth_binding_controls')
    admitted={case['probe_id']:case for case in manifest['cases']}
    for case in manifest['cases']:
        for control in controls.controls(case):
            if control['probe_id'] in admitted:raise ValueError('duplicate admitted probe')
            admitted[control['probe_id']]=control
    for case_root in (attempt/'data/cases').iterdir():
        if case_root.is_dir() and required(case_root/'case.json')!=admitted.get(case_root.name):
            raise ValueError('runtime case fixture differs from admitted manifest/control')
    return {'spec_sha256':spec_hash,'source_revision':source['source_revision'],
        'build_sha256':sha(attempt/'data/acceptance-build.json'),
        'manifest_sha256':build['manifest_sha256'],'prepared_attempt_bound':True}
