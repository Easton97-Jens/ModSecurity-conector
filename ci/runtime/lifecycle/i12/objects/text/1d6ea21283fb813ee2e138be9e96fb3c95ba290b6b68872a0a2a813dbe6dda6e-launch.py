"""Direct approved Lighttpd single-case supplemental host layer, no legacy PASS."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time

route=sys.argv[1]
assert route in ('stock-sidecar','patched-native')
assert os.geteuid()==os.getegid()==65534
for line in Path('/proc/self/status').read_text().splitlines():
    if line.startswith(('CapInh:','CapPrm:','CapEff:','CapBnd:','CapAmb:')):assert int(line.split()[1],16)==0
ROOT=Path('/task/lighttpd');ROOT.mkdir(mode=0o700)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
artifact_ledger=json.loads(Path('/mnt/fixtures/artifacts-ledger.json').read_text())['files']
sidecar_parent=None
if route=='stock-sidecar':
    manifest_values=dict(line.split('=',1) for line in Path('/mnt/artifacts/sidecar/stock-sidecar-artifact.manifest').read_text().splitlines())
    sidecar_parent=Path(manifest_values['sidecar_path']).parent
    assert sidecar_parent.is_relative_to('/var/tmp/codex/ModSecurity-conector') and '..' not in sidecar_parent.parts
    # Reproduce the genuine native build pathname inside the private /task alias.
    # The original generated manifest bytes and artifact SHAs remain unchanged.
    sidecar_parent.mkdir(parents=True,mode=0o700)
owned=ROOT/'owned';owned.mkdir(mode=0o700)
for relative,digest in artifact_ledger.items():
    source=Path('/mnt/artifacts')/relative
    assert source.is_file() and not source.is_symlink() and sha(source)==digest
    target=sidecar_parent/Path(relative).name if sidecar_parent is not None and relative.startswith('sidecar/') else owned/relative
    target.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    shutil.copyfile(source,target);target.chmod(0o500 if os.access(source,os.X_OK) else 0o400)
    assert target.stat().st_uid==65534 and sha(target)==digest
for p in owned.rglob('*'):
    if p.is_dir():p.chmod(0o500)
owned.chmod(0o500)
if sidecar_parent is not None:sidecar_parent.chmod(0o500)
rules=ROOT/'rules.conf';runtime=ROOT/'runtime.conf';hostconf=ROOT/'lighttpd.conf'
for folder in ('logs','audit','spool','htdocs','uploads','receipts'):(ROOT/folder).mkdir(mode=0o700)
rules.write_text('\n'.join([
    'SecRuleEngine On','SecRequestBodyAccess On','SecRequestBodyLimit 1048576','SecRequestBodyNoFilesLimit 1048576',
    'SecRequestBodyLimitAction Reject','SecResponseBodyAccess On','SecResponseBodyMimeType text/plain',
    'SecResponseBodyLimit 1048576','SecResponseBodyLimitAction Reject','SecAuditEngine On','SecAuditLogType Serial',
    'SecAuditLogParts ABHZ',f'SecAuditLog "{ROOT}/audit/native-audit.log"',
    f'SecAuditLogStorageDir "{ROOT}/audit"',f'SecDebugLog "{ROOT}/audit/native-debug.log"','SecDebugLogLevel 5',
    'SecRule REQUEST_METHOD "@streq POST" "id:91042002,phase:2,pass,log,t:none,chain,msg:\'test-only Lighttpd empty request P2 branch observed\'"',
    'SecRule REQUEST_HEADERS:Content-Length "@streq 0" "t:none,chain"',
    'SecRule REQUEST_BODY "@rx ^$" "t:none"',
    'SecRule RESPONSE_BODY "@contains apx-eos-response-payload" "id:91042001,phase:4,pass,log,t:none,msg:\'test-only Lighttpd native P4 branch observed\'"','']))
rules.chmod(0o600)
runtime.write_text('\n'.join(['enabled=on',f'rules_file={rules}','transaction_id_header=x-request-id',
    'request_body_mode=streaming','response_body_mode=streaming','phase4_mode=safe','default_block_status=403',
    'default_error_status=502','max_header_count=64','max_header_name_size=256','max_header_value_size=8192',
    'max_total_header_bytes=65536','max_event_json_bytes=16384',f'event_path={ROOT}/events.jsonl','']))
runtime.chmod(0o600)
env={**os.environ,'MSCONNECTOR_LIGHTTPD_NATIVE_OBSERVER':'/task/native-api.jsonl',
    'MSCONNECTOR_LIGHTTPD_HOST_OBSERVER':'/task/host-eos.jsonl','MSCONNECTOR_APACHE_BACKEND_CAPTURE':'/task/backend.jsonl',
    'MSCONNECTOR_LIFECYCLE_RUN':'20261014T182400Z-lighttpd-empty-'+route,
    'MSCONNECTOR_LIFECYCLE_PROFILE':'lighttpd-'+route,'MSCONNECTOR_LIFECYCLE_CASE':'NEED-request-empty'}
backend_port,host_port,sidecar_port=18152,18153,18154
if route=='stock-sidecar':
    binary=owned/'stock-host/bin/lighttpd';modules=owned/'stock-host/lib'
    text=['server.compat-module-load = "disable"','server.modules = ( "mod_accesslog", "mod_proxy" )',
        f'accesslog.filename = "{ROOT}/logs/stock-access.log"']
else:
    binary=owned/'patched-host/bin/lighttpd';modules=owned/'patched-host/modules'
    text=['server.compat-module-load = "disable"','server.modules = ( "mod_proxy", "mod_msconnector" )',
        'server.stream-response-body = 1','msconnector.enabled = "enable"',
        f'msconnector.config-file = "{runtime}"','msconnector.request-body-gate = "pre-upstream"']
if route=='stock-sidecar':
    stock_spec=importlib.util.spec_from_file_location('lighttpd_actual_stock_guards','/mnt/src/connectors/lighttpd/harness/run_stock_sidecar_real_backend.py')
    stock_guards=importlib.util.module_from_spec(stock_spec);sys.modules[stock_spec.name]=stock_guards;stock_spec.loader.exec_module(stock_guards)
    host_contract=stock_guards.verify_stock_host_provenance(binary,modules,sha(binary))
    stock_guards.verify_stock_launch_artifacts(binary,modules,host_contract)
    revision,tree_state=stock_guards.repository_revision()
    assert revision=='02754040bced960cfc1857416cd7101bb3116ef4' and tree_state=='dirty'
    stock_manifest=stock_guards.verify_sidecar_build_manifest(sidecar_parent/'lighttpd-stock-sidecar',
        sha(sidecar_parent/'lighttpd-stock-sidecar'),revision,tree_state)
    (ROOT/'actual-stock-native-provenance.json').write_text(json.dumps({'host_contract':host_contract,
        'native_sidecar_manifest':stock_manifest,'actual_source_commit':revision,'actual_source_tree_state':tree_state},indent=2)+'\n')
text += [f'server.document-root = "{ROOT}/htdocs"','server.bind = "127.0.0.1"',f'server.port = {host_port}',
    f'server.errorlog = "{ROOT}/logs/lighttpd-error.log"',f'server.pid-file = "{ROOT}/lighttpd.pid"',
    f'server.upload-dirs = ( "{ROOT}/uploads" )',
    f'proxy.server = ( "" => ( ( "host" => "127.0.0.1", "port" => {backend_port} ) ) )','']
hostconf.write_text('\n'.join(text));hostconf.chmod(0o600)
actors={};streams=[];cleanup=[];snapshots=[];events=[]
def launch(name,argv,extra=None):
    stdout=(ROOT/'logs'/(name+'.stdout')).open('xb');stderr=(ROOT/'logs'/(name+'.stderr')).open('xb');streams.extend((stdout,stderr))
    actual=['rtk','proxy',*map(str,argv)]
    process=subprocess.Popen(actual,env=env if extra is None else {**env,**extra},stdin=subprocess.DEVNULL,
        stdout=stdout,stderr=stderr,start_new_session=True)
    actors[name]={'process':process,'argv':actual,'starttime':None,'native_pid':None,'native_starttime':None}
    return process
def starttime(pid):return Path('/proc',str(pid),'stat').read_text().rsplit(')',1)[1].split()[19]
def native_child(name):
    row=actors[name];launcher=row['process'].pid
    expected=Path(row['argv'][2]).resolve()
    expected_digest=sha(expected)
    matches=[]
    process_rows={}
    for proc in Path('/proc').iterdir():
        if not proc.name.isdecimal():continue
        try:
            parts=(proc/'stat').read_text().rsplit(')',1)[1].split()
            process_rows[int(proc.name)]=(int(parts[1]),parts[19])
        except (FileNotFoundError,ProcessLookupError):continue
    for pid,(_parent,token) in process_rows.items():
        ancestor=pid;visited=set()
        while ancestor in process_rows and ancestor not in visited:
            if ancestor==launcher:
                try:
                    exe=Path('/proc',str(pid),'exe')
                    if exe.resolve()==expected and sha(exe)==expected_digest:matches.append((pid,token))
                except (FileNotFoundError,ProcessLookupError):pass
                break
            visited.add(ancestor);ancestor=process_rows[ancestor][0]
    assert len(matches)==1,(name,launcher,matches)
    row['native_pid'],row['native_starttime']=matches[0]
    return matches[0]
def listen(port):
    for path in (Path('/proc/net/tcp'),Path('/proc/net/tcp6')):
        if any(row.split()[3]=='0A' and row.split()[1].endswith(f':{port:04X}') for row in path.read_text().splitlines()[1:]):return True
    return False
def wait_ready(name,port):
    process=actors[name]['process'];deadline=time.monotonic()+15
    while time.monotonic()<deadline:
        if process.poll() is not None:raise RuntimeError(name+' exited before listener: '+str(process.returncode))
        if listen(port):
            actors[name]['starttime']=starttime(process.pid);native_child(name);return
        time.sleep(0.03)
    raise RuntimeError(name+' listener timeout')
def snapshot(label):
    root=ROOT/'receipts'/label;root.mkdir(mode=0o700)
    receipt={'monotonic_ns':time.monotonic_ns(),'processes':{}}
    for name,row in actors.items():
        process=row['process'];native_pid=row['native_pid'];proc=Path('/proc')/str(native_pid)
        if row['starttime'] is None:row['starttime']=starttime(process.pid)
        assert process.poll() is None and starttime(process.pid)==row['starttime']
        assert starttime(native_pid)==row['native_starttime']
        maps=(proc/'maps').read_bytes();status=(proc/'status').read_bytes()
        fds={p.name:os.readlink(p) for p in (proc/'fd').iterdir()}
        (root/(name+'.maps')).write_bytes(maps);(root/(name+'.status')).write_bytes(status)
        (root/(name+'.fds.json')).write_text(json.dumps(fds,indent=2)+'\n')
        receipt['processes'][name]={'pid':native_pid,'starttime':row['native_starttime'],
            'actual_launcher_pid':process.pid,'actual_launcher_starttime':row['starttime'],'argv':row['argv'],
            'maps_sha256':hashlib.sha256(maps).hexdigest(),'status_sha256':hashlib.sha256(status).hexdigest(),'fds':fds}
    for name in ('events.jsonl','/task/native-api.jsonl','/task/host-eos.jsonl','/task/backend.jsonl'):
        p=Path(name) if name.startswith('/') else ROOT/name
        receipt.setdefault('physical_files',{})[str(p)]=None if not p.exists() else {
            'size':p.stat().st_size,'uid':p.stat().st_uid,'mode':oct(p.stat().st_mode&0o777),'sha256':sha(p)}
    (root/'snapshot.json').write_text(json.dumps(receipt,indent=2)+'\n');snapshots.append(str(root/'snapshot.json'))
def client(label,method,path,port):
    body=ROOT/(label+'.request-body');body.write_bytes(b'');body.chmod(0o600)
    argv=['rtk','proxy','/usr/local/bin/python3','/mnt/fixtures/curl-raw-client.py','-sS','--http1.1',
        '-D',str(ROOT/(label+'.response-headers')),'-X',method,'-o',str(ROOT/(label+'.response-body')),
        '-w','%{http_code}','-H','Content-Type: text/plain','-H','X-Request-Id: lighttpd-'+route+'-'+label]
    if method=='POST':argv+=['--data-binary','@'+str(body)]
    argv += [f'http://127.0.0.1:{port}{path}']
    completed=subprocess.run(argv,env={**env,'I12_APACHE_CLIENT_TOKEN':label},capture_output=True,timeout=20)
    (ROOT/(label+'.actual-client-process.json')).write_text(json.dumps({'argv':argv,
        'actual_waited_return_code':completed.returncode,'actual_signal':-completed.returncode if completed.returncode<0 else None,
        'stdout':completed.stdout.decode(),'stderr':completed.stderr.decode()},indent=2)+'\n')
    if completed.returncode:raise RuntimeError('actual client '+label+' failed: '+completed.stderr.decode())
try:
    launch('backend',['/usr/local/bin/python3','/mnt/fixtures/backend-launch.py',str(backend_port)])
    wait_ready('backend',backend_port)
    check=['rtk','proxy',str(binary),'-tt','-m',str(modules),'-f',str(hostconf)]
    checked=subprocess.run(check,env=env,capture_output=True,timeout=20)
    (ROOT/'logs/configtest.stdout').write_bytes(checked.stdout);(ROOT/'logs/configtest.stderr').write_bytes(checked.stderr)
    (ROOT/'configtest-command.json').write_text(json.dumps({'argv':check,'exitcode':checked.returncode},indent=2)+'\n')
    if checked.returncode:raise RuntimeError('actual native config test failed: '+checked.stderr.decode())
    launch('host',[binary,'-D','-m',modules,'-f',hostconf]);wait_ready('host',host_port)
    if route=='stock-sidecar':
        launch('sidecar',[sidecar_parent/'lighttpd-stock-sidecar','--config',runtime,'--listen',f'127.0.0.1:{sidecar_port}',
            '--upstream',f'127.0.0.1:{host_port}','--timeout-ms','3000','--spool-directory',ROOT/'spool'])
        wait_ready('sidecar',sidecar_port);port=sidecar_port
    else:port=host_port
    snapshot('before-main');client('main','POST','/i12/lighttpd/empty',port);time.sleep(0.1);snapshot('after-main')
    client('neighbor','GET','/no-crs/allow',port);time.sleep(0.1);snapshot('after-neighbor')
finally:
    for name,row in reversed(list(actors.items())):
        process=row['process'];actual_before=process.poll()
        if actual_before is None:
            assert row['starttime'] is None or starttime(process.pid)==row['starttime']
            if row['native_pid'] is not None:
                assert starttime(row['native_pid'])==row['native_starttime']
                os.kill(row['native_pid'],signal.SIGTERM)
            else:os.killpg(process.pid,signal.SIGTERM)
            try:process.wait(timeout=5)
            except subprocess.TimeoutExpired:os.killpg(process.pid,signal.SIGKILL);process.wait(timeout=5)
        native_gone=row['native_pid'] is None or not Path('/proc',str(row['native_pid'])).exists()
        if not native_gone:native_gone=starttime(row['native_pid'])!=row['native_starttime']
        assert native_gone,(name,row['native_pid'])
        cleanup.append({'actor':name,'actual_launcher_pid':process.pid,'actual_launcher_starttime':row['starttime'],
            'native_pid':row['native_pid'],'native_starttime':row['native_starttime'],'actual_return_code':process.returncode,
            'actual_before_cleanup_exit':actual_before,'native_same_starttime_pid_gone':native_gone,'launcher_reaped':True})
    for stream in streams:stream.close()
    (ROOT/'execution-receipt.json').write_text(json.dumps({'route':route,'actual_selected_id':'I12::lighttpd-'+route+'::NEED-request-empty',
        'snapshots':snapshots,'cleanup':cleanup,'original_nulls_preserved':True,
        'source_layer':'Approved direct one-case native runtime supplement; no legacy whole-harness PASS or ACTIVE flag.',
        'full_lifecycle_qualified':False,'oracle_evaluated':False},indent=2)+'\n')
    print(json.dumps({'route':route,'cleanup_actor_count':len(cleanup),'snapshots':len(snapshots),'full_lifecycle_qualified':False}))
