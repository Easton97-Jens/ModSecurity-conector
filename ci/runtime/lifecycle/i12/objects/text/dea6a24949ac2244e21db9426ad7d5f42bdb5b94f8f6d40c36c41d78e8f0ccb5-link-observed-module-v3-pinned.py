"""Relink genuine APX objects with separately validated test-only observers."""
import ast
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

BASE=Path(__file__).resolve().parent
WT=Path('/var/tmp/codex/ModSecurity-conector/worktrees/pr410-sonar-host-repair-20261014')
ROOT=BASE/'source-v5'
SDK=Path('/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/nginx-current-build/sdk')
OUT=BASE/'observed-module-07';OUT.mkdir(mode=0o700,exist_ok=False)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
expected={'native-lifecycle-observer.c':'a4ce3e2513bc3a9300781873119c256fe12f384427d4a4bb3b49578afd6a1df8',
          'native-lifecycle-observer.h':'5818303be9b9ed113d5b02605c223a77b45b2d587c409636bd4dd2c185ed2508'}
for name in ('native-lifecycle-observer.c','native-lifecycle-observer.h','native-lifecycle-sdk.cpp'):
    original=ROOT/'ci/runtime/lifecycle'/name
    if name in expected:assert sha(original)==expected[name],name
    shutil.copyfile(original,OUT/name)
records=[]
def run(label,argv):
    result=subprocess.run(['rtk','proxy',*argv],capture_output=True,timeout=90)
    stdout,stderr=OUT/(label+'.stdout'),OUT/(label+'.stderr')
    stdout.write_bytes(result.stdout);stderr.write_bytes(result.stderr)
    records.append({'argv':['rtk','proxy',*argv],'exit_code':result.returncode,
                    'stdout_sha256':sha(stdout),'stderr_sha256':sha(stderr),
                    'stdout':str(stdout),'stderr':str(stderr)})
    (OUT/'link-receipt.json').write_text(json.dumps({'commands':records},indent=2)+'\n')
    if result.returncode:raise RuntimeError(f'{label}: {result.stderr.decode()[-4000:]}')
    return result.stdout.decode()
includes=['-I',str(ROOT),'-I',str(ROOT/'common/include'),'-isystem',str(SDK/'include'),'-I',str(ROOT/'ci/runtime/lifecycle')]
run('compile-host-callback',['cc','-std=c17','-Wall','-Wextra','-Werror','-pthread','-fPIC','-fno-lto',
    '-D_GNU_SOURCE','-I',str(ROOT/'connectors/apache/src'),'-I','/usr/include/apache2','-I','/usr/include/apr-1.0',
    *includes,'-c',str(ROOT/'connectors/apache/src/apache-host-observer.c'),'-o',str(OUT/'apache-host-observer.o')])
run('compile-descriptor-bootstrap',['cc','-std=c17','-Wall','-Wextra','-Werror','-fPIC','-fno-lto',
    '-c',str(ROOT/'connectors/apache/src/apache-observer-fd-bootstrap.c'),'-o',str(OUT/'apache-observer-fd-bootstrap.o')])
run('compile-native-observer',['cc','-std=c17','-Wall','-Wextra','-Werror','-pthread','-fPIC','-fno-lto',
    *includes,'-c',str(ROOT/'ci/runtime/lifecycle/native-lifecycle-observer.c'),'-o',str(OUT/'native-lifecycle-observer.o')])
run('compile-sdk-accessor',['g++','-std=c++17','-Wall','-Wextra','-Werror','-fPIC','-fno-lto',
    *includes,'-c',str(ROOT/'ci/runtime/lifecycle/native-lifecycle-sdk.cpp'),'-o',str(OUT/'native-lifecycle-sdk.o')])
parsed=ast.parse((ROOT/'tests/test_native_lifecycle_observer.py').read_text())
symbols=next(ast.literal_eval(node.value) for node in parsed.body
    if isinstance(node,ast.Assign) and any(isinstance(name,ast.Name) and name.id=='SYMBOLS' for name in node.targets))
objects=[]
for path in (BASE/'baseline-objects').glob('*.o'):
    if path.name in ('src-mod_security3.o','src-msc_filters.o','src-msc_utils.o'):continue
    objects.append(path)
objects.extend(BASE/('build-v3' if name=='msc_filters.o' else 'build')/name for name in ('mod_security3.o','msc_filters.o','msc_utils.o'))
objects.extend(OUT/name for name in ('apache-host-observer.o','apache-observer-fd-bootstrap.o'))
objects.extend(OUT/name for name in ('native-lifecycle-observer.o','native-lifecycle-sdk.o'))
module=OUT/'apache-test-observed.so'
run('link',['g++','-shared','-fPIC','-fno-lto','-pthread','-Wl,--as-needed','-Wl,-Bsymbolic-functions',
    '-Wl,-z,relro','-Wl,-z,now',*[str(path) for path in objects],
    *['-Wl,--wrap='+name for name in symbols],str(SDK/'lib/libmodsecurity.so'),
    '-Wl,-rpath,/usr/lib/x86_64-linux-gnu','-o',str(module)])
nm=run('defined-symbols',['nm','-D','--defined-only',str(module)])
for name in ('security3_module','msconnector_lifecycle_host_begin','msconnector_lifecycle_host_end',
             'msconnector_lifecycle_host_scope_call','msconnector_lifecycle_host_retire',
             'apache_lifecycle_observe','apache_lifecycle_retire'):
    assert name in nm,name
receipt={'commands':records,'source_files':{name:sha(OUT/name) for name in
            ('native-lifecycle-observer.c','native-lifecycle-observer.h','native-lifecycle-sdk.cpp')},
         'objects':{str(path):sha(path) for path in objects},'wrapped_symbols':symbols,
         'test_module':str(module),'test_module_sha256':sha(module),
         'baseline_module_sha256':'908c9e7a7062ada3e36499a69e2c41e17791a36021d5872d0981bfc5864bb5d0',
         'module_scope':'External test-only actual APX sources/objects + allocation/API and physical host EOS observers. Never claim byteidentity with baseline module; no release artifact or product source modified.',
         'status':'LINKED_NOT_HOST_EXECUTED','full_lifecycle_qualification':None}
(OUT/'link-receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':receipt['status'],'objects':len(objects),'wrapped_symbols':len(symbols),
                  'module_sha256':receipt['test_module_sha256']}))
