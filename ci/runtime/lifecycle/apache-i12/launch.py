"""One genuine nonroot Apache POST/allow plus separate GET neighbor capture."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import threading
import time

settings=json.loads(Path('/mnt/fixtures/settings.json').read_text())
base=Path('/var/tmp/codex/ModSecurity-conector/apache-lifecycle')
base.mkdir(mode=0o700)
owned=base/'native-bin/apache2';owned.parent.mkdir(mode=0o700)
shutil.copyfile('/usr/sbin/apache2',owned);owned.chmod(0o500)
assert owned.stat().st_uid==os.geteuid() and hashlib.sha256(owned.read_bytes()).hexdigest()=='32226a96ed9257837341b7909edae8da368922565f4662b1f76624e7c74e4a3d'
assert hashlib.sha256(Path('/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14').read_bytes()).hexdigest()=='32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407'
env=dict(os.environ,FRAMEWORK_ROOT='/mnt/framework',BUILD_ROOT=str(base),APACHE_BUILD_ROOT=str(base/'build'),
    LOG_DIR=str(base/'logs'),RESULTS_DIR=str(base/'results'),RUNTIME_ROOT=str(base/'runtime'),
    RUNTIME_BASE=str(base/'runtime-base'),APACHE_CASE_OUTPUT_ROOT=str(base),
    HTTPD_PREFIX='/usr/lib/apache2',APACHE_HTTPD=str(owned),APACHE_MODULE='/mnt/artifacts/apache/test-observed.so',
    MODSECURITY_LIB_DIR='/usr/lib/x86_64-linux-gnu',PYTHON='/usr/local/bin/python3',CURL='/mnt/fixtures/observed-curl.py',
    RUN_ONE_CASE='1',TEST_CASE='/mnt/fixtures/'+settings['fixture_relative_path'],
    FORCE_ALL_CASES='1',PORT='18140',CASE_SCOPE='all',MODSECURITY_TEST_VARIANT='no-crs',
    MSCONNECTOR_APACHE_NATIVE_OBSERVER='/task/apache-native-api.jsonl',
    MSCONNECTOR_APACHE_HOST_OBSERVER='/task/apache-host-eos.jsonl',
    MSCONNECTOR_APACHE_BACKEND_CAPTURE='/task/apache-backend.jsonl',
    MSCONNECTOR_LIFECYCLE_RUN=settings['run_id'],
    MSCONNECTOR_LIFECYCLE_PROFILE='apache-native',MSCONNECTOR_LIFECYCLE_CASE=settings['case_id'],
    I12_APACHE_SELECTED_URI=settings['selected_uri'],I12_APACHE_FOLLOWUP='1',I12_APACHE_CAPTURE_DELAY='1')
if settings.get('canonical_no_crs_baseline'):
    env['MODSECURITY_RULE_PREAMBLE_FILE']='/mnt/framework/tests/rules/no-crs-baseline.conf'
argv=['rtk','proxy','/bin/sh','/mnt/src/connectors/apache/harness/run_apache_smoke.sh']
stop=threading.Event();snapshots=[];errors=[]
state=base/'runtime/run/httpd-supervisor-state.json'
def snapshot_child():
    while not stop.is_set():
        try:
            if state.exists():
                lease=json.loads(state.read_text())
                pid=lease['child_pid'];proc=Path('/proc')/str(pid)
                stat=proc.joinpath('stat').read_text()
                start=stat.rsplit(')',1)[1].split()[19]
                if str(start)!=str(lease['child_pid_starttime']):raise RuntimeError('native childPID starttime differs from actual supervisor lease')
                label=str(time.monotonic_ns())
                root=Path('/task/native-process');root.mkdir(mode=0o700,exist_ok=True)
                maps=proc.joinpath('maps').read_text();status=proc.joinpath('status').read_text()
                fds={path.name:os.readlink(path) for path in proc.joinpath('fd').iterdir()}
                root.joinpath(label+'.maps').write_text(maps);root.joinpath(label+'.status').write_text(status)
                root.joinpath(label+'.fds.json').write_text(json.dumps(fds,indent=2)+'\n')
                snapshots.append({'monotonic_ns':int(label),'native_child_pid':pid,'starttime':start,
                    'actual_lease':lease,'fd_count':len(fds),'maps_sha256':hashlib.sha256(maps.encode()).hexdigest(),
                    'status_sha256':hashlib.sha256(status.encode()).hexdigest(),'files_label':label})
        except (FileNotFoundError,ProcessLookupError,json.JSONDecodeError):
            pass
        except Exception as error:
            errors.append({'type':type(error).__name__,'message':str(error)})
        stop.wait(0.05)
thread=threading.Thread(target=snapshot_child,daemon=True);thread.start()
started=time.monotonic_ns()
result=None
timed_out=False
execution_error=None
try:
    with Path('/task/apache.stdout').open('xb') as stdout,Path('/task/apache.stderr').open('xb') as stderr:
        result=subprocess.run(argv,env=env,stdout=stdout,stderr=stderr,timeout=240)
except subprocess.TimeoutExpired as error:
    timed_out=True
    execution_error={'type':type(error).__name__,'message':str(error)}
except Exception as error:
    execution_error={'type':type(error).__name__,'message':str(error)}
finally:
    stop.set();thread.join(timeout=5)
receipt={'argv':argv,'actual_driver_exit':result.returncode if result is not None else None,'timed_out':timed_out,'execution_error':execution_error,'started_monotonic_ns':started,
    'completed_monotonic_ns':time.monotonic_ns(),'environment_overrides':{key:value for key,value in env.items() if os.environ.get(key)!=value},
    'owned_binary':{'path':str(owned),'uid':owned.stat().st_uid,'mode':oct(owned.stat().st_mode&0o777),'sha256':hashlib.sha256(owned.read_bytes()).hexdigest()},
    'native_process_snapshots':snapshots,'native_process_sampler_errors':errors,'sampler_thread_stopped':not thread.is_alive(),
    'source_instrumentation_is_test_only':True,'original_selected_id':settings['original_selected_id'],'settings':settings,
    'original_null_oracles_preserved_elsewhere':True,'one_main_and_one_separate_neighbor':True,
    'full_lifecycle_qualification':None}
Path('/task/apache-lifecycle-command.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps({'actual_driver_exit':result.returncode if result is not None else None,'timed_out':timed_out,'execution_error':execution_error,'native_process_snapshots':len(snapshots),'sampler_errors':len(errors),'full_lifecycle_qualification':None}))
raise SystemExit(124 if timed_out else (result.returncode if result is not None else 1))
