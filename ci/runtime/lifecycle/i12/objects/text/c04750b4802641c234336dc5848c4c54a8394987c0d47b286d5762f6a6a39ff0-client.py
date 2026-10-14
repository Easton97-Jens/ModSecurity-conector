"""Actual TLS reads and subsequent actual raw TCP EOF, never inferred from close."""
import hashlib,json,socket,ssl,sys,time
from pathlib import Path
def stamp():return {'wall_ns':time.time_ns(),'monotonic_ns':time.monotonic_ns()}
name=sys.argv[1];body=b'haproxy-lifecycle-main\n' if name=='main' else b'neighbor'
request=(f'POST /i12-{name} HTTP/1.1\r\nHost: 127.0.0.1\r\nContent-Type: text/plain\r\nContent-Length: {len(body)}\r\nConnection: close\r\n\r\n').encode()+body
context=ssl.create_default_context(cafile='/task/tls.crt')
row={'name':name,'request_bytes':len(body),'request_sha256':hashlib.sha256(body).hexdigest(),'started_wall_ns':time.time_ns(),'started_monotonic_ns':time.monotonic_ns(),'ssl_verifies_task_ca':True,'suppress_ragged_eofs':False,'ssl_reads':[]}
with context.wrap_socket(socket.create_connection(('127.0.0.1',18490),timeout=10),server_hostname='127.0.0.1',suppress_ragged_eofs=False) as connection:
    connection.settimeout(10);row['tls_version']=connection.version();row['cipher']=connection.cipher()
    write_before=stamp();connection.sendall(request);write_after=stamp()
    row['actual_request_write']={'api':'SSLSocket.sendall','before':write_before,'after':write_after,'input_wire_bytes':len(request),'successful_return':None,'successful_return_reason':'sendall returns None on success, actual exception would terminate client'}
    row['sent_wall_ns']=write_after['wall_ns'];row['sent_monotonic_ns']=write_after['monotonic_ns'];data=b'';first=None;termination=None;tls_read_zero=False
    while True:
        before=stamp()
        try:chunk=connection.recv(16384)
        except ssl.SSLEOFError as error:
            after=stamp();row['ssl_reads'].append({'api':'SSLSocket.recv','before':before,'after':after,'actual_bytes':None,'error_type':type(error).__name__,'error':str(error)})
            termination={'kind':'TLS_unexpected_eof','message':str(error),'actual_tcp_recv0':None,'actual_tcp_recv0_reason':'TLS read failed before unwrap; no TCP EOF inference'};break
        after=stamp();row['ssl_reads'].append({'api':'SSLSocket.recv','before':before,'after':after,'actual_bytes':len(chunk),'sha256':hashlib.sha256(chunk).hexdigest() if chunk else None,'empty_read_sha_reason':None if chunk else 'Actual empty TLS read; no payload SHA'})
        if not chunk:
            tls_read_zero=True;termination={'kind':'strict_TLS_SSL_read_returned_zero','wall_ns':after['wall_ns'],'monotonic_ns':after['monotonic_ns']};break
        if first is None:first=after['wall_ns'];row['first_receive_monotonic_ns']=after['monotonic_ns']
        data+=chunk
    row['actual_raw_TCP_end']={'value':None,'reason':'No actual raw socket read yet'}
    if tls_read_zero:
        before=stamp()
        try:
            raw=connection.unwrap();after=stamp();row['actual_TLS_unwrap']={'before':before,'after':after,'success':True,'returned_live_socket':True}
            raw.settimeout(3);before=stamp()
            try:
                chunk=raw.recv(1);after=stamp();row['actual_raw_TCP_end']={'value':{'api':'socket.recv_after_successful_TLS_unwrap','before':before,'after':after,'actual_bytes':len(chunk),'actual_recv0':chunk==b'','actual_reset':False,'actual_timeout':False},'reason':None}
                if chunk:row['actual_raw_TCP_end']['value']['unexpected_post_TLS_bytes_sha256']=hashlib.sha256(chunk).hexdigest()
            except (TimeoutError,ConnectionResetError,OSError) as error:
                after=stamp();row['actual_raw_TCP_end']={'value':{'api':'socket.recv_after_successful_TLS_unwrap','before':before,'after':after,'actual_bytes':None,'actual_recv0':None,'actual_reset':isinstance(error,ConnectionResetError),'actual_timeout':isinstance(error,TimeoutError),'error_type':type(error).__name__,'error':str(error)},'reason':'Actual raw socket receive raised; no EOF synthesized'}
        except (ssl.SSLError,OSError) as error:
            after=stamp();row['actual_TLS_unwrap']={'before':before,'after':after,'success':False,'error_type':type(error).__name__,'error':str(error)};row['actual_raw_TCP_end']={'value':None,'reason':'TLS unwrap failed; no successful raw socket receive occurred'}
    head,entity=data.split(b'\r\n\r\n',1);lines=head.decode('iso-8859-1').split('\r\n');headers=[line.split(':',1) for line in lines[1:]];length=next(int(value.strip()) for key,value in headers if key.lower()=='content-length')
    row.update(status=int(lines[0].split()[1]),headers=headers,first_receive_wall_ns=first,response_bytes=len(entity),response_sha256=hashlib.sha256(entity).hexdigest(),declared_content_length=length,body_complete=len(entity)==length,termination=termination,wire_bytes=len(data),completed_wall_ns=time.time_ns(),completed_monotonic_ns=time.monotonic_ns(),native_EOS_not_derived_from_TLS_or_TCP_or_close=True)
    Path('/task/'+name+'-wire.bin').write_bytes(data)
Path('/task/'+name+'-client.json').write_text(json.dumps(row,indent=2)+'\n')
expected_status=403 if name=='main' else 200
row['source_bound_expected_status']=expected_status
if row['status']!=expected_status or not row['body_complete']:raise SystemExit(1)
