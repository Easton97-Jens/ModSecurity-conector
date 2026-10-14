"""Prepare only fresh stock inputs after independently validated observer controls."""
import hashlib
import importlib.util
import json
import shutil
import subprocess
from pathlib import Path

BASE = Path(__file__).resolve().parent
RUN = BASE.parents[1]
WT = Path('/var/tmp/codex/ModSecurity-conector/worktrees/pr410-sonar-host-repair-20261014')
control_path = RUN/'native-observer-worker/control-15/receipt.json'
control = json.loads(control_path.read_text())
assert control['exit']==0
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def seal(tree, name):
    ledger=BASE/name
    ledger.write_text(json.dumps({'files':{str(p.relative_to(tree)):sha(p) for p in tree.rglob('*') if p.is_file()}},indent=2,sort_keys=True)+'\n')
    ledger.chmod(0o444)
    for p in tree.rglob('*'): p.chmod(0o555 if p.is_dir() or p.stat().st_mode&0o111 else 0o444)
    tree.chmod(0o555)
    return ledger

source=BASE/'source-04'
shutil.copytree(BASE/'source-02',source)
for relative, expected in control['source_sha256'].items():
    target=source/relative
    assert sha(WT/relative)==expected
    target.chmod(0o600)
    shutil.copyfile(WT/relative,target)
    assert sha(target)==expected
preparation=json.loads((BASE/'source-preparation.json').read_text())
symbols=preparation['wrapped_symbols']+['msconnector_runtime_transaction_finalize_and_snapshot']
assert len(symbols)==len(set(symbols))==38
(BASE/'stock-finalize-source-preparation.json').write_text(json.dumps({'wrapped_symbols':symbols,'control_receipt_sha256':sha(control_path)},indent=2)+'\n')
script=(BASE/'build-observed-03.py').read_text().replace("SOURCE=BASE/'source-02'","SOURCE=BASE/'source-04'").replace("BUILD=BASE/'build-03'","BUILD=BASE/'build-04'")
script=script.replace("BASE/'source-preparation.json'","BASE/'stock-finalize-source-preparation.json'")
script=script.replace("run('patched-native-module-build',['/bin/sh',SOURCE/'connectors/lighttpd/build/build_module.sh'],env)","")
script=script.replace(",\n        BUILD/'patched-module/modules/mod_msconnector.so'","")
script=script.replace('control-14/receipt.json','control-15/receipt.json')
buildscript=BASE/'build-observed-04.py';buildscript.write_text(script)
result=subprocess.run(['rtk','proxy','python3',str(buildscript)],capture_output=True,timeout=240)
(BASE/'build-04-driver.stdout').write_bytes(result.stdout)
(BASE/'build-04-driver.stderr').write_bytes(result.stderr)
assert result.returncode==0, result.stderr.decode()[-4000:]
seal(source,'source-04-ledger.json')
runtime=BASE/'source-05'
shutil.copytree(source,runtime,ignore=shutil.ignore_patterns('.git','__pycache__','*.pyc'))
for target in (runtime/'.git',runtime/'modules/ModSecurity-test-Framework/.git'):
    target.parent.chmod(0o755);target.mkdir(mode=0o555)
binding={'compiled_source':str(source),'runtime_source':str(runtime),'files':{}}
for p in runtime.rglob('*'):
    if p.is_file():
        relative=p.relative_to(runtime);assert sha(p)==sha(source/relative)
        binding['files'][str(relative)]=sha(p)
(BASE/'source-05-compilation-binding.json').write_text(json.dumps(binding,indent=2,sort_keys=True)+'\n')
source_ledger=seal(runtime,'source-05-ledger.json')
stage=BASE/'stock-sidecar'
artifacts=stage/'observed-artifacts-v4';artifacts.mkdir(mode=0o700)
for relative in json.loads((stage/'baseline-artifacts-ledger.json').read_text())['files']:
    original=stage/'baseline-artifacts'/relative
    if relative.startswith('sidecar/'):original=BASE/'build-04/stock-sidecar'/Path(relative).name
    target=artifacts/relative;target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(original,target)
    if original.stat().st_mode&0o111:target.chmod(0o555)
artifact_ledger=seal(artifacts,'stock-sidecar-observed-artifacts-v4-ledger.json')
fixtures=stage/'single-fixtures-v4'
shutil.copytree(stage/'single-fixtures-v3',fixtures)
(fixtures/'artifacts-ledger.json').chmod(0o600)
shutil.copyfile(artifact_ledger,fixtures/'artifacts-ledger.json')
fixture_ledger=seal(fixtures,'stock-sidecar-single-fixtures-v4-ledger.json')
spec=json.loads((stage/'single-admission-spec-v3.json').read_text())
for item in spec['bindings']:
    updates={'/mnt/src':(runtime,source_ledger),'/mnt/artifacts':(artifacts,artifact_ledger),'/mnt/fixtures':(fixtures,fixture_ledger)}
    if item['target'] in updates:
        path,ledger=updates[item['target']]
        item.update(source=str(path),ledger=str(ledger),ledger_sha256=sha(ledger))
path=stage/'single-admission-spec-v4.json'
path.write_text(json.dumps(spec,indent=2,sort_keys=True)+'\n');path.chmod(0o444)
loader=importlib.util.spec_from_file_location('stock_finalize_spec',RUN/'isolation/private-runtime-v5.py')
module=importlib.util.module_from_spec(loader);loader.loader.exec_module(module);module.read_spec(path)
receipt={'spec':str(path),'spec_sha256':sha(path),'read_spec':'passed','wrapped_symbols':symbols,'shared_control_receipt_sha256':sha(control_path),'source_ledger_sha256':sha(source_ledger),'source_compilation_binding_sha256':sha(BASE/'source-05-compilation-binding.json'),'artifact_ledger_sha256':sha(artifact_ledger),'fixture_ledger_sha256':sha(fixture_ledger),'build_receipt_sha256':sha(BASE/'build-04/build-receipt.json'),'observed_binary_sha256':sha(BASE/'build-04/stock-sidecar/lighttpd-stock-sidecar'),'host_launched':False,'oracle_evaluated':False,'full_lifecycle_qualified':False}
(BASE/'stock-finalize-retake-readiness.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps(receipt,indent=2))
