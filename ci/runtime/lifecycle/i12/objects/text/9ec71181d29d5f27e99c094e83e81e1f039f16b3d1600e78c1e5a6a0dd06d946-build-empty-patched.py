"""Original strict module build; reuse unchanged already pinned observer objects."""
import hashlib
import json
import os
from pathlib import Path
import subprocess

BASE=Path(__file__).resolve().parent
RUN=BASE.parent
OLD=RUN/'apache-lifecycle/lighttpd-preparation'
SOURCE=BASE/'compile-source'
BUILD=BASE/'patched-build';BUILD.mkdir(mode=0o700)
SDK=RUN.parent/'20261014T034122Z-pr410-completion/nginx-current-build/sdk'
CORE=RUN.parent/'20261013T125816Z-8c574cdf-i12-completion/build-bridges/build/lighttpd-core-patched/lighttpd-1.4.85'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
records=[]
def run(label,argv,env=None):
    result=subprocess.run(['rtk','proxy',*map(str,argv)],capture_output=True,env=env,timeout=180)
    stdout,stderr=BUILD/(label+'.stdout'),BUILD/(label+'.stderr')
    stdout.write_bytes(result.stdout);stderr.write_bytes(result.stderr)
    records.append({'argv':['rtk','proxy',*map(str,argv)],'exit_code':result.returncode,
        'stdout_sha256':sha(stdout),'stderr_sha256':sha(stderr)})
    (BUILD/'commands.json').write_text(json.dumps(records,indent=2)+'\n')
    assert result.returncode==0,result.stderr.decode()[-5000:]
logger=BUILD/'host-observer.o'
run('compile-host-logger',['cc','-std=c17','-Wall','-Wextra','-Werror','-fPIC','-fno-lto','-pthread',
    '-I',SOURCE,'-I',SOURCE/'common/include','-isystem',SDK/'include','-c',SOURCE/'lighttpd-host-observer.c','-o',logger])
original=json.loads((OLD/'build-04/build-receipt.json').read_text())
objects=[Path(path) for path in original['observer_objects'] if Path(path).name!='host-observer.o']
for path in objects:assert sha(path)==original['observer_objects'][str(path)]
objects.append(logger)
symbols=original['wrapped_symbols'];assert len(symbols)==38
wrapper=BUILD/'observer-cc.py'
wrapper.write_text('''#!/usr/local/bin/python3
import json,subprocess,sys
from pathlib import Path
args=sys.argv[1:]
extra=['-I',SOURCE,'-isystem',SDKINCLUDE]
if '-c' not in args:extra+=OBJECTS+['-Wl,--wrap='+name for name in SYMBOLS]+['-lstdc++']
argv=['rtk','proxy','cc',*args,*extra]
completed=subprocess.run(argv)
with (Path(__file__).parent/'cc-commands.jsonl').open('a') as stream:
    stream.write(json.dumps({'argv':argv,'exit_code':completed.returncode})+'\\n')
raise SystemExit(completed.returncode)
'''.replace('SOURCE',repr(str(SOURCE))).replace('SDKINCLUDE',repr(str(SDK/'include'))).replace('OBJECTS',repr(list(map(str,objects)))).replace('SYMBOLS',repr(symbols)))
wrapper.chmod(0o555)
env=dict(os.environ,CC=str(wrapper),BUILD_ROOT=str(BUILD),MODSECURITY_INCLUDE_DIR=str(SDK/'include'),
    MODSECURITY_LIB_DIR=str(SDK/'lib'),GIT_DIR=str(RUN/'host-inputs/current-source-metadata'),GIT_WORK_TREE=str(SOURCE),
    GIT_OPTIONAL_LOCKS='0',LIGHTTPD_CONNECTOR_OUT_DIR=str(BUILD/'module'),LIGHTTPD_MODULE_DIR=str(BUILD/'module/modules'),
    LIGHTTPD_SOURCE_DIR=str(CORE),LIGHTTPD_BUILD_ROOT=str(CORE.parent/'build-1.4.85'),LIGHTTPD_MSCONNECTOR_CORE_MODE='patched')
run('original-native-module-build',['/bin/sh',SOURCE/'connectors/lighttpd/build/build_module.sh'],env)
module=BUILD/'module/modules/mod_msconnector.so'
receipt={'commands':records,'observer_object_sha256':{str(path):sha(path) for path in objects},
    'original_observer_build_receipt_sha256':sha(OLD/'build-04/build-receipt.json'),
    'observer_source_sha256':sha(SOURCE/'ci/runtime/lifecycle/native-lifecycle-observer.c'),
    'module_source_sha256':sha(SOURCE/'connectors/lighttpd/module/mod_msconnector.c'),
    'module_sha256':sha(module),'compiler_wrapper_sha256':sha(wrapper),'wrapped_symbols':symbols,
    'original_product_input_equality_proof_sha256':sha(OLD/'baseline-product-equality.json'),
    'host_launched':False,'full_lifecycle_qualified':False}
(BUILD/'receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps({'module_sha256':sha(module),'receipt_sha256':sha(BUILD/'receipt.json')}))
