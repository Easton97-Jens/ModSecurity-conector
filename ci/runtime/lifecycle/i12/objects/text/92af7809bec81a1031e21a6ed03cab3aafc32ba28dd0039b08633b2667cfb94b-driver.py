"""One selected EOS obligation, separate neighbor, original physical artifacts."""
import contextlib
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import signal
import socket
import subprocess
import sys
import time

SOURCE = Path('/mnt/src')
TASK = Path('/task')
FIXTURES = Path('/mnt/fixtures')
ARTIFACTS = Path('/mnt/artifacts')
SDK_SHA = '32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407'
SHAPE = json.loads((FIXTURES / 'shape.json').read_text())
CASE = SHAPE['case_id']
RUN = 'envoy-i12-' + SHAPE['target']
TARGET = SHAPE['target']
NEIGHBOR = SHAPE['neighbor']
SYMBOLS = ('msconnector_transaction_contract_init', 'msconnector_transaction_contract_finish', 'msconnector_transaction_contract_cleanup', 'msconnector_transaction_contract_complete_phase', 'msconnector_transaction_contract_set_response_committed', 'msconnector_transaction_contract_record_response_metadata', 'msc_new_transaction', 'msc_new_transaction_with_id', 'msc_transaction_cleanup', 'msc_process_request_body', 'msc_process_response_body', 'msc_process_logging', 'msc_append_request_body', 'msc_append_response_body', 'msc_process_request_headers', 'msc_process_response_headers', 'msc_intervention', 'msconnector_runtime_transaction_begin', 'msconnector_runtime_transaction_begin_request_stream', 'msconnector_runtime_transaction_append_request_body_chunk', 'msconnector_runtime_transaction_finish_request_body', 'msconnector_runtime_transaction_process_response_headers', 'msconnector_runtime_transaction_append_response_body_chunk', 'msconnector_runtime_transaction_finish_response_body', 'msconnector_runtime_transaction_finish', 'msconnector_runtime_transaction_destroy', 'msconnector_runtime_transaction_finalize_and_snapshot', 'msconnector_runtime_response_companion_handoff_with_handle', 'msconnector_runtime_response_companion_claim_handle', 'msconnector_runtime_response_companion_revoke_handle', 'msconnector_runtime_response_companion_session_process_response_headers', 'msconnector_runtime_response_companion_session_append_response_body_chunk', 'msconnector_runtime_response_companion_session_finish_response_body', 'msconnector_runtime_response_companion_session_set_response_commit_state', 'msconnector_runtime_response_companion_session_record_host_action', 'msconnector_runtime_response_companion_session_fail', 'msconnector_runtime_response_companion_session_cancel', 'msconnector_runtime_response_companion_session_release')

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def write(name, value):
    (TASK / name).write_text(json.dumps(value, indent=2) + '\n')

def execute(label, argv, environment):
    command = ['rtk', 'proxy', *map(str, argv)]
    with (TASK / f'{label}.stdout').open('wb') as stdout, (TASK / f'{label}.stderr').open('wb') as stderr:
        result = subprocess.run(command, env=environment, cwd=SOURCE, stdout=stdout, stderr=stderr, timeout=240)
    receipt = {'argv': command, 'cwd': str(SOURCE), 'exit_code': result.returncode,
               'stdout_sha256': digest(TASK / f'{label}.stdout'), 'stderr_sha256': digest(TASK / f'{label}.stderr')}
    write(f'{label}.command.json', receipt)
    if result.returncode:
        raise RuntimeError(f'{label} exited {result.returncode}')

def descendants(process):
    queue, result = [process.pid], []
    while queue:
        pid = queue.pop()
        result.append(pid)
        try:
            child_text = Path(f'/proc/{pid}/task/{pid}/children').read_text()
        except FileNotFoundError:
            continue
        queue.extend(int(value) for value in child_text.split())
        if len(result) > 128:
            raise RuntimeError('bounded task process inventory exceeded')
    return result

def actual_pid(process, marker):
    found = []
    for pid in descendants(process):
        try:
            arguments = Path(f'/proc/{pid}/cmdline').read_bytes().split(b'\0')
        except FileNotFoundError:
            continue
        direct_binary = arguments[0] == marker.encode()
        direct_python = arguments[:3] == [b'/usr/local/bin/python3', b'-P', marker.encode()]
        if direct_binary or direct_python:
            found.append(pid)
    if len(found) != 1:
        raise RuntimeError(f'exact process identity unavailable for {marker}: {found}')
    return found[0]

def snapshot(label, processes):
    value = {'monotonic_ns': time.monotonic_ns(), 'wall_ns': time.time_ns(), 'processes': {}}
    value['clock_calibration'] = {'wall_before_ns': time.time_ns(), 'monotonic_ns': time.monotonic_ns(), 'wall_after_ns': time.time_ns()}
    for name, (process, marker) in processes.items():
        pid = actual_pid(process, marker)
        base = Path(f'/proc/{pid}')
        status = base.joinpath('status').read_text()
        maps = base.joinpath('maps').read_text()
        (TASK / f'{label}.{name}.maps.raw').write_text(maps)
        (TASK / f'{label}.{name}.status.raw').write_text(status)
        descriptors = {}
        vanished = []
        for descriptor in sorted(base.joinpath('fd').iterdir(), key=lambda item: int(item.name)):
            try:
                descriptors[descriptor.name] = os.readlink(descriptor)
            except FileNotFoundError:
                vanished.append(descriptor.name)
        executable = os.readlink(base / 'exe')
        libraries = sorted({line.split()[-1] for line in maps.splitlines()
                            if 'libmodsecurity.so' in line and line.split()[-1].startswith('/')})
        record = {'pid': pid, 'proxy_pid': process.pid, 'executable': executable,
                  'executable_sha256': digest(base / 'exe'), 'fd_count': len(descriptors),
                  'fds': descriptors, 'vanished_during_snapshot': vanished,
                  'native_libraries': [{'path': item, 'sha256': digest(item)} for item in libraries],
                  'identity': {key: next((line.split(':', 1)[1].strip() for line in status.splitlines()
                      if line.startswith(key + ':')), None) for key in ('Uid', 'Gid', 'CapEff', 'CapBnd', 'NoNewPrivs')}}
        if name == 'engine' and (len(libraries) != 1 or record['native_libraries'][0]['sha256'] != SDK_SHA):
            raise RuntimeError('actual engine mapping does not bind the selected SDK')
        value['processes'][name] = record
    for name in ('tcp', 'tcp6', 'unix'):
        (TASK / f'{label}.net-{name}.raw').write_text(Path(f'/proc/net/{name}').read_text())
    write(f'{label}.json', value)

def start(label, argv, environment, handles, pass_fds=()):
    stdout = (TASK / f'{label}.stdout').open('wb')
    stderr = (TASK / f'{label}.stderr').open('wb')
    handles.extend((stdout, stderr))
    command = ['rtk', 'proxy', *map(str, argv)]
    process = subprocess.Popen(command, cwd=TASK / 'runtime', env=environment,
                               stdout=stdout, stderr=stderr, pass_fds=pass_fds)
    write(f'{label}.launch.json', {'argv': command, 'proxy_pid': process.pid, 'monotonic_ns': time.monotonic_ns()})
    return process


def wait_port(port, process, label):
    deadline=time.monotonic()+20
    while time.monotonic()<deadline:
        if process.poll() is not None: raise RuntimeError(label+' exited before ready')
        try:
            with socket.create_connection(('127.0.0.1',port),timeout=0.1): return
        except OSError: time.sleep(0.05)
    raise RuntimeError(label+' listener deadline expired')

def main():
    if (os.geteuid(),os.getegid()) != (65534,65534): raise RuntimeError('v5 isolated nonroot identity required')
    for name in ['runtime','build','tmp','cache']: (TASK/name).mkdir(mode=0o700)
    for filename in ['envoy.yaml','native.conf','loopback.crt','loopback.key']:
        shutil.copyfile(FIXTURES/filename,TASK/'runtime'/filename)
        (TASK/'runtime'/filename).chmod(0o600)
    host=TASK/'cache/envoy'
    engine=TASK/'cache'/('msconnector_envoy_ext_proc' if SHAPE['leg']=='envoy-ext-proc' else 'msconnector_composite')
    for binary in [host,engine]:shutil.copyfile(ARTIFACTS/binary.name,binary);binary.chmod(0o700)
    product=json.loads((FIXTURES/'scoped-product-source-a9.json').read_text())
    equality=[]
    for relative,expected in product['source_inputs'].items():
        actual=digest(SOURCE/relative);overlay=product['approved_test_overlays'].get(relative)
        allowed=actual==expected or overlay is not None and overlay['baseline_a9_sha256']==expected and overlay['instrumented_sha256']==actual
        equality.append({'path':relative,'baseline_a9_sha256':expected,'actual_source_sha256':actual,'approved_private_overlay':overlay,'verified':allowed})
    write('scoped-product-source-equality.json',equality)
    if not all(row['verified'] for row in equality):raise RuntimeError('source contract differs from sealed build input')
    env=os.environ.copy()
    env.update(TZ='UTC',TMPDIR='/task/tmp',CC='/mnt/fixtures/cc-wrapper.sh',CXX='/mnt/fixtures/cxx-wrapper.sh',GOTOOLCHAIN='local',GOPROXY='off',GOSUMDB='off')
    execute('host-version',[host,'--version'],env)
    execute('go-version',['/usr/local/go/bin/go','version'],env)
    execute('sdk-who-compile',['/usr/bin/gcc','-std=c17','-Wall','-Wextra','-Werror',FIXTURES/'sdk-who.c','-lmodsecurity','-o',TASK/'build/sdk-who'],env)
    execute('sdk-who',[TASK/'build/sdk-who'],env)
    for name in ['native-lifecycle.jsonl','host-lifecycle.jsonl','native-audit.log','native-debug.log','envoy-access.jsonl']:
        fd=os.open(TASK/'runtime'/name,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);os.close(fd)
    execute('envoy-config-validate',[host,'--mode','validate','-c',TASK/'runtime/envoy.yaml','--disable-hot-restart','--base-id','17','--concurrency','1'],env)
    write('build-manifest.json',{'case':CASE,'run':RUN,'source_git_baseline':'3a1bafecd0c38ccf20427d580c767ed42addf4aa plus v5 harness and declared private overlays','product_contract':'a9d48bb58aa948aea7d79e20cdf09d3f239b7808','delivery_source_baseline':'02754040bced960cfc1857416cd7101bb3116ef4','delivery_scoped_verified':'8cc32dceb06121f589150a9794f28878c5e4ba2a','source_scope_count':len(equality),'host_sha256':digest(host),'engine_sha256':digest(engine),'wrap_symbols':SYMBOLS,'actual_external_build_provenance':json.loads((FIXTURES/'actual-build-provenance-v1.json').read_text()),'runtime_backend_profile_actual_source':'envoy-ext-proc Common runtime backend reused by actual composite adapters','fixture_configuration':{str(p):digest(p) for p in [FIXTURES/'shape.json',FIXTURES/'native.rules',TASK/'runtime/native.conf',TASK/'runtime/envoy.yaml',TASK/'runtime/loopback.crt',TASK/'runtime/loopback.key']},'rules_original_sha256':digest(FIXTURES/'native.rules')})
    handles,processes=[],{}
    lifecycle_fd=os.open(TASK/'runtime/native-lifecycle.jsonl',os.O_WRONLY|os.O_APPEND)
    failure=None
    final={'case':CASE,'qualification':'unreviewed_actual_measurements','selected_case_count':1,'neighbor_health_probe_count':1,'processes':{}}
    try:
        backend=start('backend',['/usr/local/bin/python3','-P',FIXTURES/'backend.py','18444'],env,handles)
        processes['backend']=(backend,str(FIXTURES/'backend.py'));wait_port(18444,backend,'TLS backend')
        native_env=env|{'MSCONNECTOR_LIFECYCLE_FD':str(lifecycle_fd),'MSCONNECTOR_LIFECYCLE_RUN':RUN,'MSCONNECTOR_LIFECYCLE_PROFILE':SHAPE['leg'],'MSCONNECTOR_LIFECYCLE_CASE':CASE,'I12_ENVOY_HOST_TRACE_PATH':'/task/runtime/host-lifecycle.jsonl'}
        if SHAPE['leg']=='envoy-ext-proc':
            command=[engine,'--config',FIXTURES/'extproc-service.json','--runtime-config',TASK/'runtime/native.conf','--listen','127.0.0.1:18083','--event-log',TASK/'runtime/adapter-events.jsonl']
        else:
            command=[engine,'--mode','envoy','--listen','127.0.0.1:18083','--runtime-config',TASK/'runtime/native.conf','--event-log',TASK/'runtime/adapter-events.jsonl']
        native=start('engine',command,native_env,handles,(lifecycle_fd,));processes['engine']=(native,str(engine));wait_port(18083,native,'actual native gRPC engine')
        envoy=start('envoy',[host,'-c',TASK/'runtime/envoy.yaml','--disable-hot-restart','--base-id','17','--concurrency','1','--drain-time-s','0','--log-level','debug','--component-log-level','http:trace,http2:debug,ext_proc:trace,grpc:debug','--log-format','[%Y-%m-%dT%T.%e%z] [%t] [%l] [%n] [%g:%#] %v'],env,handles)
        processes['envoy']=(envoy,str(host));wait_port(18443,envoy,'actual TLS Envoy')
        time.sleep(0.15);snapshot('before-request',processes)
        execute('selected-target-client',['/usr/local/bin/python3','-P',FIXTURES/'client.py','18443','target'],env)
        time.sleep(0.15);snapshot('after-target',processes)
        execute('separate-neighbor-client',['/usr/local/bin/python3','-P',FIXTURES/'client.py','18443','neighbor'],env)
        time.sleep(0.15);snapshot('after-neighbor',processes)
        receipts=[json.loads(line) for line in (TASK/'backend/receipts.jsonl').read_text().splitlines()]
        if len(receipts)!=2 or [row['path'] for row in receipts]!=['/'+TARGET,'/'+NEIGHBOR]:raise RuntimeError('independent backend count/nonces differ')
        final['independent_backend_request_count']=len(receipts)
    except Exception as error:
        failure={'type':type(error).__name__,'message':str(error)}
    finally:
        for name in ['envoy','engine','backend']:
            if name not in processes:continue
            process,marker=processes[name]
            record={'proxy_pid':process.pid,'signal_sent':None,'forced_kill':False}
            if process.poll() is None:
                try:
                    pid=actual_pid(process,marker);record['pid']=pid
                    os.kill(pid,signal.SIGTERM);record['signal_sent']=int(signal.SIGTERM)
                    record['waited_exit_code']=process.wait(timeout=15)
                except Exception as error:
                    record['stop_error']={'type':type(error).__name__,'message':str(error)}
                    if process.poll() is None:
                        for pid in reversed(descendants(process)):
                            try:os.kill(pid,signal.SIGKILL)
                            except ProcessLookupError:pass
                        record['forced_kill']=True
                        record['waited_exit_code']=process.wait(timeout=5)
            else:record['waited_exit_code']=process.returncode
            final['processes'][name]=record
        os.close(lifecycle_fd)
        for handle in handles:handle.close()
        final['failure']=failure
        final['remaining_owned_processes']=[name for name,(process,_) in processes.items() if process.poll() is None]
        for name in ['tcp','tcp6','unix']:(TASK/f'final.net-{name}.raw').write_text(Path(f'/proc/net/{name}').read_text())
        final['actual_runtime_copies_hashes']={str(p.relative_to(TASK)):digest(p) for p in (TASK/'runtime').iterdir() if p.is_file()}
        write('result.json',final)
    if failure or any(item.get('waited_exit_code')!=0 or item.get('forced_kill') for item in final['processes'].values()):return 1
    return 0

if __name__=='__main__':raise SystemExit(main())
