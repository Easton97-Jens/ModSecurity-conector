import hashlib,json,os,signal,subprocess,time
from pathlib import Path
TASK=Path('/task')
def run(args,label,**kwargs):
    with (TASK/(label+'.stdout')).open('wb') as out,(TASK/(label+'.stderr')).open('wb') as err:
        result=subprocess.run(['rtk','proxy',*args],stdout=out,stderr=err,timeout=60,**kwargs)
    receipts.append({'label':label,'argv':['rtk','proxy',*args],'exit':result.returncode,'signal':-result.returncode if result.returncode<0 else None})
    if result.returncode:raise RuntimeError(label+' failed')
    return result
def snapshot(process,label):
    proc=Path('/proc')/str(process.pid)
    result={'label':label,'pid':process.pid,'wall_ns':time.time_ns(),'starttime':proc.joinpath('stat').read_text().rsplit(')',1)[1].split()[19],'fds':{p.name:os.readlink(p) for p in proc.joinpath('fd').iterdir()}}
    for name in ('maps','status'): (TASK/(label+'.'+name)).write_text(proc.joinpath(name).read_text())
    for table in ('tcp','tcp6','unix'):
        (TASK/(label+'.net-'+table)).write_text(Path('/proc/net').joinpath(table).read_text())
    (TASK/(label+'.fds.json')).write_text(json.dumps(result,indent=2)+'\n')
    return result
receipts=[];children=[];snapshots=[]
rules='''SecRuleEngine On
SecRequestBodyAccess On
SecRequestBodyLimit 16
SecRequestBodyNoFilesLimit 1024
SecRequestBodyLimitAction ProcessPartial
SecResponseBodyAccess On
SecResponseBodyLimit 1024
SecResponseBodyLimitAction Reject
SecResponseBodyMimeType text/plain
SecAuditEngine On
SecAuditLog /task/native-audit.log
SecAuditLogType Serial
SecAuditLogParts ABFHZ
SecDebugLog /task/native-debug.log
SecDebugLogLevel 9
SecAction "id:1999401,phase:1,pass,log,msg:'I12_HAP_P1'"
SecAction "id:1999404,phase:4,pass,log,msg:'I12_HAP_P4'"
SecRule REQUEST_BODY "@streq haproxy-lifecycl" "id:1999461,phase:2,pass,log,msg:'I12_PARTIAL_PREFIX_EXACT16'"
SecRule REQUEST_BODY "@streq 5d226c942dcb40aec18f97f81a19695dcaaa023d" "id:1999462,phase:2,pass,log,t:sha1,t:hexEncode,msg:'I12_PARTIAL_PREFIX_NATIVE_SHA1'"
SecRule REQUEST_BODY "@streq neighbor" "id:1999463,phase:2,pass,log,msg:'I12_LIMIT_HEALTH_NEIGHBOR_BODY'"
'''
(TASK/'rules.conf').write_text(rules)
try:
    run(['openssl','req','-config','/mnt/fixtures/openssl.cnf','-extensions','v3_ca','-x509','-newkey','rsa:2048','-nodes','-sha256','-days','1','-subj','/CN=127.0.0.1','-addext','subjectAltName=IP:127.0.0.1,DNS:haproxy-i12-backend.invalid','-keyout','/task/tls.key','-out','/task/tls.crt'],'tls')
    (TASK/'tls.pem').write_bytes((TASK/'tls.key').read_bytes()+(TASK/'tls.crt').read_bytes());(TASK/'tls.pem').chmod(0o600)
    config='''global
    nbthread 1
    log stdout format raw local0
defaults
    mode http
    timeout connect 2s
    timeout client 10s
    timeout server 10s
frontend htx_in
    bind 127.0.0.1:18490 ssl crt /task/tls.pem
    filter modsecurity-htx rules-file /task/rules.conf phase4-mode safe
    default_backend htx_upstream
backend htx_upstream
    server upstream 127.0.0.1:18491
'''
    (TASK/'haproxy.cfg').write_text(config)
    run(['/mnt/artifacts/haproxy-direct','-vv'],'identity')
    run(['/mnt/artifacts/haproxy-direct','-c','-f','/task/haproxy.cfg'],'config')
    with (TASK/'backend.stdout').open('wb') as out,(TASK/'backend.stderr').open('wb') as err:
        backend=subprocess.Popen(['rtk','proxy','/usr/local/bin/python3','/mnt/fixtures/backend.py'],stdout=out,stderr=err);children.append(('backend',backend))
    deadline=time.monotonic()+10
    while not (TASK/'backend.ready').exists():
        if time.monotonic()>deadline or backend.poll() is not None:raise RuntimeError('backend readiness failed')
        time.sleep(.02)
    fd=os.open(TASK/'native-api.jsonl',os.O_WRONLY|os.O_APPEND|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
    env=dict(os.environ,MSCONNECTOR_LIFECYCLE_FD=str(fd),MSCONNECTOR_LIFECYCLE_RUN='20261014-hap-native-limit-2',MSCONNECTOR_LIFECYCLE_PROFILE='haproxy-native-htx',MSCONNECTOR_LIFECYCLE_CASE='NEED-request-process-partial')
    with (TASK/'haproxy.stdout').open('wb') as out,(TASK/'haproxy.stderr').open('wb') as err:
        host=subprocess.Popen(['/mnt/artifacts/haproxy-direct','-db','-f','/task/haproxy.cfg'],env=env,pass_fds=(fd,),stdout=out,stderr=err);children.append(('haproxy',host))
    os.close(fd);time.sleep(.5)
    if host.poll() is not None:raise RuntimeError('HAProxy startup failed')
    snapshots.append(snapshot(host,'before-main'))
    run(['/usr/local/bin/python3','/mnt/fixtures/client.py','main'],'main-client');time.sleep(.2)
    snapshots.append(snapshot(host,'after-main'))
    run(['/usr/local/bin/python3','/mnt/fixtures/client.py','neighbor'],'neighbor-client');time.sleep(.2)
    snapshots.append(snapshot(host,'after-neighbor'))
finally:
    for name,process in reversed(children):
        if process.poll() is None:process.send_signal(signal.SIGUSR1 if name=='haproxy' else signal.SIGTERM)
        result=process.wait(timeout=10);receipts.append({'label':name+'-wait','pid':process.pid,'exit':result,'signal':-result if result<0 else None,'reaped':True})
    receipt={'commands':receipts,'snapshots':snapshots,'source_instrumentation_is_test_only':True,'selected_id':'I12::haproxy-native-htx::NEED-request-process-partial','full_lifecycle_pass':None,'effective_rules_sha256':hashlib.sha256((TASK/'rules.conf').read_bytes()).hexdigest(),'effective_config_sha256':hashlib.sha256((TASK/'haproxy.cfg').read_bytes()).hexdigest() if (TASK/'haproxy.cfg').exists() else None}
    (TASK/'execution.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'commands':receipts,'full_lifecycle_pass':None}))
