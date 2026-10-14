import hashlib,json,os,signal,subprocess,time
from pathlib import Path
TASK=Path('/task')
selected=json.loads(Path('/mnt/fixtures/selected.json').read_text())
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
rules=r'''SecRuleEngine On
SecRequestBodyAccess On
SecRequestBodyLimit 1024
SecRequestBodyNoFilesLimit 1024
SecRequestBodyLimitAction Reject
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
SecRule REQUEST_BODY "@rx \Ahaproxy-lifecycle-main\x0a\z" "id:1999422,phase:2,pass,log,msg:'I12_REQUEST_BODY_EXACT_MAIN'"
SecRule REQUEST_BODY "@rx \Ahaproxy-lifecycle-neighbor\x0a\z" "id:1999423,phase:2,pass,log,msg:'I12_REQUEST_BODY_EXACT_NEIGHBOR'"
'''
(TASK/'rules.conf').write_text(rules)
try:
    run(['openssl','req','-config','/mnt/fixtures/openssl.cnf','-extensions','v3_ca','-x509','-newkey','rsa:2048','-nodes','-sha256','-days','1','-subj','/CN=127.0.0.1','-addext','subjectAltName=IP:127.0.0.1,DNS:haproxy-i12-backend.invalid','-keyout','/task/tls.key','-out','/task/tls.crt'],'tls')
    (TASK/'tls.pem').write_bytes((TASK/'tls.key').read_bytes()+(TASK/'tls.crt').read_bytes());(TASK/'tls.pem').chmod(0o600)
    (TASK/'spoe.cfg').write_text("""[modsecurity]
spoe-agent modsecurity-agent
    groups request-check
    option var-prefix modsec
    register-var-names blocked action status redirect_url rule_id phase error response_handle
    max-frame-size 65532
    option continue-on-error
    timeout hello 1s
    timeout idle 3s
    timeout processing 2s
    use-backend be_spoa
spoe-group request-check
    messages check-request
spoe-message check-request
    args request_id=unique-id client_ip=src client_port=src_port server_ip=dst server_port=dst_port method=method path=path uri=url host=req.hdr(host) headers_bin=req.hdrs_bin headers=req.hdrs body=req.body body_len=req.body_size http_version=req.ver
""")
    (TASK/'agent.conf').write_text(f"""listen=127.0.0.1:18492
log-file=/task/spoa.log
decision-log=/task/decision.jsonl
audit-log=/task/audit.jsonl
rules-file=/task/rules.conf
mode=block
fail-mode=closed
runtime-mode=production
response-companion=native-htx
response-phases=true
response-companion-socket=/task/companion.sock
response-companion-uid={os.geteuid()}
response-companion-gid={os.getegid()}
response-body-timeout=10000
spoe-timeout=2000
max-transactions=64
""")
    config=f"""global
    nbthread 1
    log stdout format raw local0
    tune.bufsize 65536
defaults
    mode http
    timeout connect 2s
    timeout client 10s
    timeout server 10s
frontend combined
    bind 127.0.0.1:18490 ssl crt /task/tls.pem
    unique-id-format %[uuid()]
    option http-buffer-request
    filter spoe engine modsecurity config /task/spoe.cfg
    filter modsecurity-htx response-companion-socket /task/companion.sock response-companion-timeout-ms 2000 response-companion-uid {os.geteuid()} response-companion-gid {os.getegid()} phase4-mode safe
    http-request send-spoe-group modsecurity request-check
    http-request deny status 403 if {{ var(txn.modsec.blocked) -m bool }}
    default_backend be_app
backend be_app
    server app 127.0.0.1:18491 ssl verify required ca-file /task/tls.crt verifyhost haproxy-i12-backend.invalid sni str(haproxy-i12-backend.invalid)
backend be_spoa
    mode spop
    timeout connect 1s
    timeout server 3s
    server agent 127.0.0.1:18492
"""
    (TASK/'haproxy.cfg').write_text(config)
    run(['/mnt/artifacts/haproxy-companion','-vv'],'identity')
    run(['/mnt/artifacts/haproxy-companion','-c','-f','/task/haproxy.cfg'],'config')
    with (TASK/'backend.stdout').open('wb') as out,(TASK/'backend.stderr').open('wb') as err:
        backend=subprocess.Popen(['rtk','proxy','/usr/local/bin/python3','/mnt/fixtures/backend.py','tls'],stdout=out,stderr=err);children.append(('backend',backend))
    deadline=time.monotonic()+10
    while not (TASK/'backend.ready').exists():
        if time.monotonic()>deadline or backend.poll() is not None:raise RuntimeError('backend readiness failed')
        time.sleep(.02)
    agent_fd=os.open(TASK/'agent-native-api.jsonl',os.O_WRONLY|os.O_APPEND|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
    agent_env=dict(os.environ,MSCONNECTOR_LIFECYCLE_FD=str(agent_fd),MSCONNECTOR_LIFECYCLE_RUN=selected['run'],MSCONNECTOR_LIFECYCLE_PROFILE=selected['leg_id'],MSCONNECTOR_LIFECYCLE_CASE=selected['case_id'])
    with (TASK/'agent.stdout').open('wb') as out,(TASK/'agent.stderr').open('wb') as err:
        agent=subprocess.Popen(['/mnt/artifacts/haproxy-spop','--config','/task/agent.conf'],env=agent_env,pass_fds=(agent_fd,),stdout=out,stderr=err);children.append(('agent',agent))
    os.close(agent_fd);time.sleep(.5)
    if agent.poll() is not None:raise RuntimeError('SPOP agent startup failed')
    snapshots.append(snapshot(agent,'agent-before-main'))
    fd=os.open(TASK/'native-api.jsonl',os.O_WRONLY|os.O_APPEND|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
    env=dict(os.environ,MSCONNECTOR_LIFECYCLE_FD=str(fd),MSCONNECTOR_LIFECYCLE_RUN=selected['run'],MSCONNECTOR_LIFECYCLE_PROFILE=selected['leg_id'],MSCONNECTOR_LIFECYCLE_CASE=selected['case_id'])
    with (TASK/'haproxy.stdout').open('wb') as out,(TASK/'haproxy.stderr').open('wb') as err:
        host=subprocess.Popen(['/mnt/artifacts/haproxy-companion','-db','-f','/task/haproxy.cfg'],env=env,pass_fds=(fd,),stdout=out,stderr=err);children.append(('haproxy',host))
    os.close(fd);time.sleep(.5)
    if host.poll() is not None:raise RuntimeError('HAProxy startup failed')
    snapshots.append(snapshot(host,'before-main'))
    run(['/usr/local/bin/python3','/mnt/fixtures/client.py','main'],'main-client');time.sleep(.2)
    snapshots.append(snapshot(host,'after-main'));snapshots.append(snapshot(agent,'agent-after-main'))
    run(['/usr/local/bin/python3','/mnt/fixtures/client.py','neighbor'],'neighbor-client');time.sleep(.2)
    snapshots.append(snapshot(host,'after-neighbor'));snapshots.append(snapshot(agent,'agent-after-neighbor'))
finally:
    for name,process in reversed(children):
        if process.poll() is None:process.send_signal(signal.SIGUSR1 if name=='haproxy' else signal.SIGTERM)
        result=process.wait(timeout=10);receipts.append({'label':name+'-wait','pid':process.pid,'exit':result,'signal':-result if result<0 else None,'reaped':True})
    receipt={'commands':receipts,'snapshots':snapshots,'source_instrumentation_is_test_only':True,'selected_id':selected['run_scoped_case_id'],'full_lifecycle_pass':None,'effective_rules_sha256':hashlib.sha256((TASK/'rules.conf').read_bytes()).hexdigest(),'effective_config_sha256':hashlib.sha256((TASK/'haproxy.cfg').read_bytes()).hexdigest() if (TASK/'haproxy.cfg').exists() else None}
    (TASK/'execution.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'commands':receipts,'full_lifecycle_pass':None}))
