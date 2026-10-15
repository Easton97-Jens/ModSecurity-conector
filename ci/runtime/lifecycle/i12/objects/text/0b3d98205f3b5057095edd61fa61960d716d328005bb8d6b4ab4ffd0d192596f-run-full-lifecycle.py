"""Actual isolated NGX selected NEED single-chunk observations; Root qualifies."""
import argparse, hashlib, importlib.util, json, os, subprocess, sys, threading, time
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer

def load(source):
    path=Path(source)/"ci/runtime/lifecycle/run-nginx-raw-h1.py"
    spec=importlib.util.spec_from_file_location("current_nginx_host",path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
class Backend(BaseHTTPRequestHandler):
    protocol_version="HTTP/1.1";rows=[]
    def do_POST(self):
        n=int(self.headers.get("Content-Length","0"))
        if not 0<=n<=4096:raise ValueError("bounded backend body")
        body=self.rfile.read(n);response=b"NGXI12_RSP physical native response\n"
        row={"path":self.path,"body_size":len(body),"body_sha256":hashlib.sha256(body).hexdigest(),"response_size":len(response),"response_sha256":hashlib.sha256(response).hexdigest(),"received_monotonic_ns":time.monotonic_ns()}
        self.send_response(200);self.send_header("Content-Type","text/plain; charset=utf-8")
        self.send_header("Content-Length",str(len(response)));self.send_header("Connection","close")
        self.end_headers();self.wfile.write(response);self.wfile.flush()
        row["write_and_flush_returned_monotonic_ns"]=time.monotonic_ns();self.rows.append(row)
    def log_message(self,*args):pass

def main():
    parser=argparse.ArgumentParser(allow_abbrev=False);parser.add_argument("--source",required=True);parser.add_argument("--module-sha",required=True)
    own,rest=parser.parse_known_args();R=load(own.source);p=R.BASE.argument_parser()
    for action in p._actions:
        if action.dest=="case_id":action.choices=("need_request_single_chunk",)
    p.add_argument("--framework-root",required=True);p.add_argument("--worker-self-map-library",required=True);a=p.parse_args(rest)
    binary,module,out=R.BASE.validate_inputs(a)
    if os.geteuid()!=0 or digest(module)!=own.module_sha:raise ValueError("reviewed exact source-observed module/root master required")
    out.mkdir(mode=0o700);env=R.BASE.configtest_environment(a.library_dir)
    backend=HTTPServer(("127.0.0.1",0),Backend);thread=threading.Thread(target=backend.serve_forever,daemon=True)
    port=R.reserve_port()
    R.BASE.snapshot_artifact(binary,out/"nginx-binary",executable=True)
    R.BASE.snapshot_artifact(module,out/"nginx-module.so",executable=False)
    rules=("SecRuleEngine On\nSecRequestBodyAccess On\nSecRequestBodyLimit 4096\nSecResponseBodyAccess On\n"
        "SecResponseBodyMimeType text/plain\nSecResponseBodyLimit 4096\n"
        f'SecDebugLog "{out}/native-sdk-debug.log"\nSecDebugLogLevel 9\n'
        'SecRule REQUEST_BODY "@contains NGXI12_REQ" "id:941002,phase:2,pass,log,msg:\'NGXI12_REQUEST_BODY_PRIMARY\'"\n'
        'SecRule RESPONSE_BODY "@contains NGXI12_RSP" "id:941004,phase:4,pass,log,msg:\'NGXI12_RESPONSE_BODY_PRIMARY\'"\n')
    (out/"no-crs-baseline.conf").write_text(rules)
    config=R.config_template(out,port,backend.server_port)
    keys=("MSCONNECTOR_LIFECYCLE_FD","MSCONNECTOR_LIFECYCLE_RUN","MSCONNECTOR_LIFECYCLE_PROFILE","MSCONNECTOR_LIFECYCLE_CASE","MSCONNECTOR_NGX_HOST_FD","MSCONNECTOR_OWNED_SELF_MAP_FD","MSCONNECTOR_OWNED_SELF_MAP_UID")
    config=config.replace("events {}", "\n".join("env "+key+";" for key in keys)+"\nevents {}")
    config=config.replace("modsecurity on;", "modsecurity on; modsecurity_phase4_mode safe;")
    config=config.replace("location / { proxy_pass", "location / { proxy_http_version 1.1; proxy_buffering off; proxy_pass")
    (out/"nginx.conf").write_text(config)
    configargv=[str(out/"nginx-binary"),"-e","stderr","-t","-c",str(out/"nginx.conf"),"-p",str(out)+"/"]
    configcode,stdout,stderr,failure=R.BASE.invoke(configargv,env)
    (out/"configtest.stdout").write_bytes(stdout);(out/"configtest.stderr").write_bytes(stderr)
    descriptors=[];process=None;handles={};clients=[];errors=[]
    roles={"run_id":a.run_id,"master_pid":0,"worker_pid":0,"master_uid":-1,"worker_uid":-1}
    for leaf,key in [("physical-lifecycle.jsonl","MSCONNECTOR_LIFECYCLE_FD"),("physical-host.jsonl","MSCONNECTOR_NGX_HOST_FD")]:
        fd=os.open(out/leaf,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_APPEND,0o600);os.fchmod(fd,0o600);descriptors.append(fd);env[key]=str(fd)
    env.update(MSCONNECTOR_LIFECYCLE_RUN=a.run_id,MSCONNECTOR_LIFECYCLE_PROFILE="nginx-native",MSCONNECTOR_LIFECYCLE_CASE="I12::nginx-native::NEED-request-single-chunk")
    map_spec=importlib.util.spec_from_file_location("owned_nginx_self_maps",Path(own.source)/"ci/runtime/lifecycle/nginx-worker-self-maps.py")
    maps=importlib.util.module_from_spec(map_spec);map_spec.loader.exec_module(maps)
    map_hashes={};capture=maps.Capture(a,out,env,map_hashes,R.HOST)
    descriptors.extend(capture.descriptors())
    thread.start()
    try:
        if configcode!=0 or failure:raise ValueError("native effective config did not load")
        with (out/"startup.stdout").open("xb") as stdout,(out/"startup.stderr").open("xb") as stderr:
            argv=[str(out/"nginx-binary"),"-e","stderr","-c",str(out/"nginx.conf"),"-p",str(out)+"/"]
            process=subprocess.Popen(argv,env=env,stdin=subprocess.DEVNULL,stdout=stdout,stderr=stderr,pass_fds=tuple(descriptors))
            roles=R.HOST.observe_roles(process,a.run_id,port,out,handles)
            capture.capture(roles)
            for label in ["selected","followup"]:
                body=b"marker=NGXI12_REQ&shape=single"
                wire=(f"POST /ngxi12/{label} HTTP/1.1\r\nHost: localhost\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {len(body)}\r\nConnection: close\r\n\r\n").encode()+body
                request=out/(label+"-request.bin");request.write_bytes(wire)
                clientargv=[sys.executable,str(Path(__file__).with_name("client.py")),"--port",str(port),"--request",str(request),"--output",str(out/label)]
                started=time.monotonic_ns();client=subprocess.run(clientargv,env=env,capture_output=True,timeout=12);waited=time.monotonic_ns()
                (out/(label+"-client.stdout")).write_bytes(client.stdout);(out/(label+"-client.stderr")).write_bytes(client.stderr)
                row={"label":label,"argv":clientargv,"exit_code":client.returncode,"signal":-client.returncode if client.returncode<0 else None,"started_monotonic_ns":started,"waited_monotonic_ns":waited}
                if (out/label/"client-observation.json").exists():row["observation"]=json.loads((out/label/"client-observation.json").read_text())
                clients.append(row)
                if client.returncode!=0:errors.append(label+" actual client failed")
    except (OSError,ValueError,subprocess.SubprocessError) as exc:errors.append(str(exc))
    finally:
        cleanup=R.HOST.stop_owned_master(process,roles,port,a.run_id,handles)
        for fd in descriptors:
            if fd != capture.descriptor:os.fsync(fd);os.close(fd)
        capture.close()
        backend.shutdown();backend.server_close();thread.join(2)
    if not cleanup.get("verified") or thread.is_alive():errors.append("owned cleanup incomplete")
    (out/"backend.json").write_text(json.dumps(Backend.rows,indent=2)+"\n")
    hashes={str(x.relative_to(out)):digest(x) for x in out.rglob("*") if x.is_file() and not x.is_symlink()}
    receipt={"scope":"Root must independently qualify selected lifecycle evidence", "selected_id":"I12::nginx-native::NEED-request-single-chunk","full_lifecycle_qualified":False,"original_expected_oracle_retained_null":True,"parent_sha":a.parent_sha,"configtest_exit":configcode,"roles":roles,"cleanup":cleanup,"clients":clients,"backend":Backend.rows,"raw_artifacts_sha256":hashes,"errors":errors}
    (out/"full-observation-receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
    return 1 if errors else 0
if __name__=="__main__":raise SystemExit(main())
