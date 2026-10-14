"""Actual native SDK/physical logger controls, not host qualification."""
import hashlib
import json
from pathlib import Path
import subprocess

BASE=Path(__file__).resolve().parent
SOURCE=BASE/'compile-source'
OUT=BASE/'controls-03';OUT.mkdir(mode=0o700)
SDK=BASE.parent.parent/'20261014T034122Z-pr410-completion/nginx-current-build/sdk'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
commands=[]
def run(label,argv):
    result=subprocess.run(['rtk','proxy',*map(str,argv)],capture_output=True,timeout=45)
    stdout,stderr=OUT/(label+'.stdout'),OUT/(label+'.stderr')
    stdout.write_bytes(result.stdout);stderr.write_bytes(result.stderr)
    commands.append({'argv':['rtk','proxy',*map(str,argv)],'exit_code':result.returncode,
        'stdout':str(stdout),'stdout_sha256':sha(stdout),'stderr':str(stderr),'stderr_sha256':sha(stderr)})
    (OUT/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
    assert result.returncode==0,result.stderr.decode()
    return result
native=OUT/'native-empty-probe'
run('compile-native',['cc','-std=c17','-Wall','-Wextra','-Werror','-isystem',SDK/'include',
    BASE/'empty-sdk-probe-03.c','-L',SDK/'lib','-Wl,-rpath,'+str(SDK/'lib'),'-lmodsecurity','-ldl','-o',native])
native_results={}
for mode in ('empty','single','absent_length','single_zero_length'):
    observed=json.loads(run('native-'+mode,[native,mode]).stdout)
    assert observed['native_headers_result']==observed['native_body_result']==1
    assert observed['disruptive']==(1 if mode=='empty' else 0)
    assert observed['status']==(451 if mode=='empty' else 200)
    assert observed['native_append_calls']==(1 if mode in ('single','single_zero_length') else 0)
    image=Path(observed['sdk_image']).resolve()
    assert sha(image)=='32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407'
    observed['sdk_image_sha256']=sha(image)
    native_results[mode]=observed
local=OUT/'logger-output-alias.c'
prefix=str(OUT)+'/'
local.write_text((SOURCE/'lighttpd-host-observer.c').read_text().replace('"/task/",6U','"'+prefix+'",'+str(len(prefix))+'U'))
control=OUT/'empty-logger-control.c'
control.write_text('''#define _POSIX_C_SOURCE 200809L
#include "lighttpd-host-observer.h"
#include <errno.h>
#include <stdlib.h>
#include <string.h>
static int unknown;
uint64_t msconnector_lifecycle_runtime_scope_call(const msconnector_runtime_transaction *transaction) {
    (void)transaction;return unknown?0:42;
}
int main(int argc,char **argv) {
    if (argc!=3 || setenv("MSCONNECTOR_LIGHTTPD_HOST_OBSERVER",argv[1],1)!=0) return 2;
    unknown=strcmp(argv[2],"unknown_scope")==0;
    const msconnector_runtime_transaction *key=(const msconnector_runtime_transaction *)(uintptr_t)0x1234;
    errno=EDOM;
    lighttpd_observe_empty_request_boundary(key,0);
    if(errno!=EDOM)return 3;
    if(strcmp(argv[2],"duplicate")==0)lighttpd_observe_empty_request_boundary(key,0);
    lighttpd_observe_body("patched_response_body_hook",key,-1,0,24U,0);
    return errno==EDOM?0:4;
}
''')
logger=OUT/'empty-logger-control'
run('compile-logger',['cc','-std=c17','-Wall','-Wextra','-Werror','-pthread','-I',SOURCE,
    '-I',SOURCE/'common/include','-isystem',SDK/'include',control,local,'-o',logger])
logger_results={}
for mode in ('positive','duplicate','unknown_scope','invalid_sink'):
    log=OUT/(mode+'.jsonl')
    if mode=='invalid_sink':log.write_text('');log.chmod(0o666)
    completed=run('logger-'+mode,[logger,log,mode])
    records=[json.loads(line) for line in log.read_text().splitlines()]
    if mode in ('unknown_scope','invalid_sink'):
        assert not records and b'evidence invalid' in completed.stderr
    else:
        boundaries=[r for r in records if r['kind']=='patched_empty_request_boundary']
        assert len(boundaries)==(2 if mode=='duplicate' else 1)
        assert all(r['actual_eos_argument'] is None and r['empty_request_boundary'] is True and
            r['entity_length']==0 and r['input_size']==0 and r['runtime_allocation_scope_call']==42 for r in boundaries)
        assert records[-1]['actual_eos_argument']==0 and records[-1]['empty_request_boundary'] is False
        assert not completed.stderr
    logger_results[mode]={'actual_rows':records,'errno_preserved':True,'physical_sha256':sha(log)}
receipt={'commands':commands,'native_program_results':native_results,'logger_results':logger_results,
    'sdk_probe_source_sha256':sha(BASE/'empty-sdk-probe-03.c'),'logger_source_sha256':sha(SOURCE/'lighttpd-host-observer.c'),
    'scope':'Independent actual native SDK primitive P2 check uses diagnostic451 deny, not expected hostedHTTP200; logger getter explicitly stub42. Neither is a hosted lifecycle qualification.',
    'host_launched':False,'full_lifecycle_qualified':False}
(OUT/'receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps({'native_controls':4,'logger_controls':4,'receipt_sha256':sha(OUT/'receipt.json')}))
