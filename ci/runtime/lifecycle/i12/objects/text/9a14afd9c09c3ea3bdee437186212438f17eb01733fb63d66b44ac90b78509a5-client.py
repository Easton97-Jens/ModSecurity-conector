"""Actual bounded single-write HTTP client; no oracle/native event synthesis."""
import argparse, hashlib, json, socket, time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--port",type=int,required=True);p.add_argument("--request",required=True);p.add_argument("--output",required=True)
a=p.parse_args();request=Path(a.request).read_bytes();out=Path(a.output);out.mkdir(mode=0o700)
if not 0<len(request)<=4096: raise ValueError("bounded owned wire required")
observed={"request_sha256":hashlib.sha256(request).hexdigest(),"first_response_monotonic_ns":None,"first_response_realtime_ns":None}
wire=bytearray()
try:
    with socket.create_connection(("127.0.0.1",a.port),timeout=5) as s:
        observed["local"]=s.getsockname();observed["peer"]=s.getpeername()
        observed["send_started_monotonic_ns"]=time.monotonic_ns()
        s.sendall(request)
        observed["send_returned_monotonic_ns"]=time.monotonic_ns()
        deadline=time.monotonic()+8
        while True:
            left=deadline-time.monotonic()
            if left<=0:raise TimeoutError("bounded response deadline")
            s.settimeout(left);chunk=s.recv(8192)
            if not chunk:break
            if observed["first_response_monotonic_ns"] is None:
                observed["first_response_monotonic_ns"]=time.monotonic_ns()
                observed["first_response_realtime_ns"]=time.time_ns()
            wire.extend(chunk)
            if len(wire)>65536:raise ValueError("bounded response size")
        observed["actual_socket_eof_monotonic_ns"]=time.monotonic_ns()
    header,body=bytes(wire).split(b"\r\n\r\n",1)
    lines=header.split(b"\r\n");observed["status"]=int(lines[0].split()[1])
    headers=[line.split(b":",1) for line in lines[1:]]
    lengths=[int(value.strip()) for key,value in headers if key.lower()==b"content-length"]
    if len(lengths)!=1 or lengths[0]!=len(body):raise ValueError("actual finite Content-Length framing mismatch")
    if any(key.lower()==b"transfer-encoding" for key,_ in headers):raise ValueError("ambiguous framing")
    (out/"headers.bin").write_bytes(header+b"\r\n\r\n");(out/"body.bin").write_bytes(body)
    observed.update({"body_bytes":len(body),"body_sha256":hashlib.sha256(body).hexdigest(),"framing":"http1.1-content-length","content_length":lengths[0],"client_function_completed":True})
finally:
    (out/"response.bin").write_bytes(wire)
    observed["response_sha256"]=hashlib.sha256(wire).hexdigest()
    (out/"client-observation.json").write_text(json.dumps(observed,indent=2)+"\n")
