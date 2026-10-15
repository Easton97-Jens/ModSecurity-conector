"""Original strict native builds with declared external observer link objects."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
BASE=Path(__file__).resolve().parent
SOURCE=BASE/'source-04'
BUILD=BASE/'build-04';BUILD.mkdir(mode=0o700)
SDK=Path('/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/nginx-current-build/sdk')
CORE=Path('/var/tmp/codex/ModSecurity-conector/runs/e2e/20261013T125816Z-8c574cdf-i12-completion/build-bridges/build/lighttpd-core-patched/lighttpd-1.4.85')
RUN=BASE.parents[1]
records=[]
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def run(label,argv,env=None):
    result=subprocess.run(['rtk','proxy',*map(str,argv)],capture_output=True,env=env,timeout=180)
    stdout,stderr=BUILD/(label+'.stdout'),BUILD/(label+'.stderr')
    stdout.write_bytes(result.stdout);stderr.write_bytes(result.stderr)
    records.append({'argv':['rtk','proxy',*map(str,argv)],'exit_code':result.returncode,
        'stdout':str(stdout),'stdout_sha256':sha(stdout),'stderr':str(stderr),'stderr_sha256':sha(stderr)})
    (BUILD/'commands.json').write_text(json.dumps(records,indent=2)+'\n')
    assert result.returncode==0,(label,result.stderr.decode()[-6000:])
    return result
observer=BUILD/'observer';observer.mkdir(mode=0o700)
includes=['-I',SOURCE,'-I',SOURCE/'common/include','-I',SOURCE/'ci/runtime/lifecycle','-isystem',SDK/'include']
strict=['-Wall','-Wextra','-Werror','-fPIC','-fno-lto','-pthread']
for name,relative in [('native-observer','ci/runtime/lifecycle/native-lifecycle-observer.c'),
    ('host-observer','lighttpd-host-observer.c'),('fd-bootstrap','lighttpd-observer-fd-bootstrap.c')]:
    run('compile-'+name,['cc','-std=c17',*strict,*includes,'-c',SOURCE/relative,'-o',observer/(name+'.o')])
run('compile-sdk-accessor',['g++','-std=c++17',*strict,*includes,'-c',SOURCE/'ci/runtime/lifecycle/native-lifecycle-sdk.cpp','-o',observer/'sdk-accessor.o'])
symbols=json.loads((BASE/'stock-finalize-source-preparation.json').read_text())['wrapped_symbols']
wrapper=BUILD/'test-observer-cc.py'
wrapper.write_text('''#!/usr/local/bin/python3
import hashlib,json,subprocess,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent
arguments=sys.argv[1:]
extra=['-I',SOURCE,'-isystem',SDKINCLUDE]
if '-c' not in arguments:
    extra += OBJECTS + ['-Wl,--wrap='+name for name in SYMBOLS] + ['-lstdc++']
argv=['rtk','proxy','cc',*arguments,*extra]
result=subprocess.run(argv)
with (BASE/'cc-commands.jsonl').open('a') as stream:
    stream.write(json.dumps({'argv':argv,'exit_code':result.returncode})+'\\n')
raise SystemExit(result.returncode)
'''.replace('SOURCE',repr(str(SOURCE))).replace('OBJECTS',repr([str(p) for p in observer.glob('*.o')])).replace('SYMBOLS',repr(symbols)).replace('SDKINCLUDE',repr(str(SDK/'include'))))
wrapper.chmod(0o555)
env=dict(os.environ,CC=str(wrapper),BUILD_ROOT=str(BUILD),MODSECURITY_INCLUDE_DIR=str(SDK/'include'),
    MODSECURITY_LIB_DIR=str(SDK/'lib'),GIT_DIR=str(RUN/'host-inputs/current-source-metadata'),GIT_WORK_TREE=str(SOURCE),
    GIT_OPTIONAL_LOCKS='0',LIGHTTPD_STOCK_SIDECAR_OUT_DIR=str(BUILD/'stock-sidecar'),
    LIGHTTPD_CONNECTOR_OUT_DIR=str(BUILD/'patched-module'),LIGHTTPD_MODULE_DIR=str(BUILD/'patched-module/modules'),
    LIGHTTPD_SOURCE_DIR=str(CORE),LIGHTTPD_BUILD_ROOT=str(CORE.parent/'build-1.4.85'),LIGHTTPD_MSCONNECTOR_CORE_MODE='patched')
run('stock-native-build',['/bin/sh',SOURCE/'connectors/lighttpd/build/build_stock_sidecar.sh'],env)

native_inputs={str(p.relative_to(CORE)):sha(p) for p in CORE.glob('src/*.h')}
native_inputs.update({str(p.relative_to(CORE)):sha(p) for p in CORE.glob('*.h')})
manifest={'commands':records,'compiler_wrapper':{'path':str(wrapper),'sha256':sha(wrapper)},
    'compiler_commands':str(BUILD/'cc-commands.jsonl'),'compiler_commands_sha256':sha(BUILD/'cc-commands.jsonl'),
    'actual_patched_core_header_inputs':native_inputs,
    'observed_artifacts':{str(p):sha(p) for p in (BUILD/'stock-sidecar/lighttpd-stock-sidecar',
        BUILD/'stock-sidecar/runtime-begin-smoke',BUILD/'stock-sidecar/stock-sidecar-artifact.manifest')},
    'observer_objects':{str(p):sha(p) for p in observer.glob('*.o')},'wrapped_symbols':symbols,
    'shared_control_receipt':str(RUN/'native-observer-worker/control-15/receipt.json'),
    'shared_control_receipt_sha256':sha(RUN/'native-observer-worker/control-15/receipt.json'),
    'source_commit':'02754040bced960cfc1857416cd7101bb3116ef4','source_tree_overlay_explicit':True,
    'product_equality_proof_sha256':sha(BASE/'baseline-product-equality.json'),
    'host_launched':False,'full_lifecycle_qualified':False}
(BUILD/'build-receipt.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
print(json.dumps({'artifacts':manifest['observed_artifacts'],'receipt_sha256':sha(BUILD/'build-receipt.json')}))
