import ast
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent
RUN = BASE.parent
OUT = ROOT / 'inputs-v3'
SOURCE, FIXTURES = OUT / 'source', OUT / 'fixtures'
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')
    path.chmod(0o444)
def seal(tree, baseline=None):
    ledger = {'files': {}, 'symlinks': {}}
    for path in sorted(tree.rglob('*')):
        if path.is_symlink():
            raise RuntimeError('private source/fixture must contain no symlink')
        if path.is_file():
            relative = str(path.relative_to(tree))
            previous = baseline / relative if baseline else None
            executable = path.suffix == '.sh' if baseline is None else previous.is_file() and bool(previous.stat().st_mode & 0o111)
            path.chmod(0o555 if executable else 0o444)
            ledger['files'][relative] = sha(path)
    for path in sorted(tree.rglob('*'), reverse=True):
        if path.is_dir():
            path.chmod(0o555)
    tree.chmod(0o555)
    return ledger
syntax = []
for path in FIXTURES.glob('*.py'):
    ast.parse(path.read_text())
    syntax.append({'path': str(path), 'sha256': sha(path), 'syntax': 'passed'})
source_ledger = seal(SOURCE, BASE / 'source-v2')
fixture_ledger = seal(FIXTURES)
write(OUT / 'source-ledger.json', source_ledger)
write(OUT / 'fixture-ledger.json', fixture_ledger)
old_source = json.loads((BASE / 'source-ledger.json').read_text())['files']
source_delta = {relative: {'before': old_source.get(relative), 'after': digest}
                for relative, digest in source_ledger['files'].items() if old_source.get(relative) != digest}
allowed = {'ci/runtime/lifecycle/native-lifecycle-observer.c', 'ci/runtime/lifecycle/native-lifecycle-observer.h',
           'connectors/traefik/native_middleware/middleware.go', 'connectors/traefik/native_middleware/engine_uds.go',
           'connectors/traefik/native_middleware/i12_observer.go', 'connectors/traefik/native_middleware/i12_observer_test.go'}
if set(source_delta) - allowed:
    raise RuntimeError('unapproved source-copy delta')
spec = json.loads((BASE / 'admission-single-eos-v2.json').read_text())
for binding in spec['bindings']:
    if binding['target'] == '/mnt/src':
        binding.update(source=str(SOURCE), ledger=str(OUT / 'source-ledger.json'), ledger_sha256=sha(OUT / 'source-ledger.json'))
    if binding['target'] == '/mnt/fixtures':
        binding.update(source=str(FIXTURES), ledger=str(OUT / 'fixture-ledger.json'), ledger_sha256=sha(OUT / 'fixture-ledger.json'))
write(OUT / 'admission-single-eos-v3.json', spec)
controller_path = RUN / 'isolation/private-runtime-v5.py'
loader = importlib.util.spec_from_file_location('reviewed_v5', controller_path)
controller = importlib.util.module_from_spec(loader)
loader.loader.exec_module(controller)
controller.read_spec(OUT / 'admission-single-eos-v3.json')
review = {'spec': str(OUT / 'admission-single-eos-v3.json'), 'spec_sha256': sha(OUT / 'admission-single-eos-v3.json'),
    'source_ledger_sha256': sha(OUT / 'source-ledger.json'), 'fixture_ledger_sha256': sha(OUT / 'fixture-ledger.json'),
    'controller_read_spec': 'passed', 'controller_sha256': sha(controller_path), 'source_copy_delta': source_delta,
    'fixture_syntax': syntax, 'go_validation': str(ROOT / 'go-verify-02/receipt.json'),
    'go_validation_sha256': sha(ROOT / 'go-verify-02/receipt.json'),
    'native_validation': str(RUN / 'native-observer-worker/control-09/receipt.json'),
    'native_validation_sha256': sha(RUN / 'native-observer-worker/control-09/receipt.json'),
    'retained_previous_successful_attempt': '1792005342243666083', 'launch_performed': False,
    'scope': 'same single selected request-EOS obligation + separate neighbor; approved transparent private writer/EOF/UDS collectors',
    'clock_caveat': 'Actual wall clocks and measured monotonic observations retained separately; no guessed epoch conversion.',
    'original_selected_row_sha256': sha(BASE / 'original-selected-row.json'),
    'known_event_semantics': 'Allow has no disruptive Common event; actual native audit/debug/API records retained; Common finish calls2 pertransaction remain visible.'}
write(OUT / 'sealed-v3-review.json', review)
print(json.dumps({key: review[key] for key in ('spec', 'spec_sha256', 'source_ledger_sha256', 'fixture_ledger_sha256', 'controller_read_spec', 'launch_performed')}))
