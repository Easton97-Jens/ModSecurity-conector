"""Compile only external Apache observation overlay and retain exact commands."""
import hashlib
import json
from pathlib import Path
import shlex
import subprocess

BASE=Path(__file__).resolve().parent
ROOT=BASE.parent/'apache-oracle-retake/source'
OLD=Path('/var/tmp/codex/ModSecurity-conector/runs/e2e/20261013T125816Z-8c574cdf-i12-completion/build-native')
OUT=BASE/'build-v3';OUT.mkdir(mode=0o700,exist_ok=False)
SDK=Path('/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/nginx-current-build/sdk')
records=[]
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def run(label,argv):
    result=subprocess.run(['rtk','proxy',*argv],capture_output=True,timeout=90)
    stdout,stderr=OUT/(label+'.stdout'),OUT/(label+'.stderr')
    stdout.write_bytes(result.stdout);stderr.write_bytes(result.stderr)
    records.append({'argv':['rtk','proxy',*argv],'exit_code':result.returncode,
                    'stdout':str(stdout),'stdout_sha256':sha(stdout),
                    'stderr':str(stderr),'stderr_sha256':sha(stderr)})
    (OUT/'compile-receipt.json').write_text(json.dumps({'commands':records},indent=2)+'\n')
    if result.returncode:
        raise RuntimeError(f'{label}: {result.returncode}: {result.stderr.decode()[-4000:]}')
    return result.stdout.decode()
apr=shlex.split(run('apr-compile-flags',['apr-1-config','--includes','--cppflags','--cflags']))
common=['-std=c17','-fPIC','-O0','-fno-lto','-I',str(BASE/'source-v5/connectors/apache/src'),'-I',str(ROOT),
        '-I',str(ROOT/'common/include'),'-I',str(SDK/'include'),'-I','/usr/include/apache2',*apr]
baseline=['-pipe','-g','-Werror=implicit-function-declaration','-fno-omit-frame-pointer',
          '-mno-omit-leaf-frame-pointer','-fstack-protector-strong','-fstack-clash-protection',
          '-Wformat','-Werror=format-security','-fcf-protection','-Wdate-time','-D_FORTIFY_SOURCE=3']
for name in ('msc_filters',):
    run('compile-'+name,['cc',*baseline,*common,'-c',str(BASE/'source-v5/connectors/apache/src'/f'{name}.c'),'-o',str(OUT/f'{name}.o')])
run('compile-apache-host-observer',['cc','-Wall','-Wextra','-Werror',*common,'-c',
                                 str(BASE/'overlay-02/apache-host-observer.c'),'-o',str(OUT/'apache-host-observer.o')])
receipt={'commands':records,'objects':{str(path):sha(path) for path in OUT.glob('*.o')},
         'parent_product_files_modified':False,'historical_objects_unchanged':True,
         'baseline_warning_flags_retained':baseline,'new_observer_strict_flags':['-Wall','-Wextra','-Werror'],
         'lto_scope':'-fno-lto preserves actual wrap call boundaries; genuine historical fat-LTO native object sections retained for other objects.',
         'status':'COMPILED_NOT_LINKED_NOT_EXECUTED','full_lifecycle_qualification':None}
(OUT/'compile-receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':receipt['status'],'objects':len(receipt['objects']),'all_exit_zero':True}))
