"""Bounded raw HTTP/1 client for the exact test-fixture curl argv contract.

Retain received bytes and actual TCP FIN/RST/timeout separately from HTTP status.
No expected backend bytes or status are used to construct observations.
"""
import hashlib
import json
import os
from pathlib import Path
import socket
import sys
import time
from urllib.parse import urlsplit

arguments=sys.argv[1:]
method='GET';headers=[];body=b'';header_file=None;body_file=None;writeout=None;url=None
index=0
while index<len(arguments):
    argument=arguments[index]
    if argument in ('-sS','--http1.1'):
        index+=1;continue
    if argument in ('-D','-X','-o','-w','-H','--data-binary'):
        if index+1>=len(arguments):raise SystemExit('incomplete fixture curl argument')
        value=arguments[index+1];index+=2
        if argument=='-D':header_file=Path(value)
        elif argument=='-X':method=value
        elif argument=='-o':body_file=Path(value)
        elif argument=='-w':writeout=value
        elif argument=='-H':
            name,separator,content=value.partition(':')
            if separator:headers.append((name,content.lstrip(' ')))
            elif value.endswith(';'):headers.append((value[:-1],''))
            else:raise SystemExit('unsupported fixture header form')
        else:
            if not value.startswith('@'):raise SystemExit('fixture requires materialized body file')
            body=Path(value[1:]).read_bytes()
        continue
    if argument.startswith('http://') and url is None:
        url=argument;index+=1;continue
    raise SystemExit('unsupported fixture curl argument: '+argument)
if url is None or header_file is None or body_file is None or writeout!='%{http_code}':
    raise SystemExit('incomplete exact fixture curl contract')
parsed=urlsplit(url)
if parsed.hostname!='127.0.0.1' or parsed.username is not None or parsed.port is None:
    raise SystemExit('fixture client only supports its private loopback target')
if len(body)>65536 or method not in ('GET','POST'):
    raise SystemExit('unsupported bounded fixture request')
path=parsed.path+('?' +parsed.query if parsed.query else '')
request=(f'{method} {path} HTTP/1.1\r\nHost: 127.0.0.1:{parsed.port}\r\n').encode('ascii')
for name,value in headers:
    if '\r' in name+value or '\n' in name+value or name.lower() in ('host','connection','content-length','transfer-encoding'):
        raise SystemExit('fixture client framing/header contract mismatch')
    request+=(name+': '+value+'\r\n').encode('ascii')
if body or method=='POST':request+=f'Content-Length: {len(body)}\r\n'.encode('ascii')
request+=b'Connection: close\r\n\r\n'+body
root=Path('/task/client');root.mkdir(mode=0o700,exist_ok=True)
token=os.environ['I12_APACHE_CLIENT_TOKEN']
received=bytearray()
recv_chunks=[]
receipt={'pid':os.getpid(),'argv':arguments,'method':method,'path':path,
         'request_bytes':len(body),'request_sha256':hashlib.sha256(body).hexdigest(),
         'started_ns':time.monotonic_ns(),'tcp_eof_observed':False,'tcp_reset_observed':False,
         'timeout_observed':False,'error':None}
status='000';exit_code=1
try:
    with socket.create_connection(('127.0.0.1',parsed.port),timeout=15) as connection:
        connection.settimeout(15)
        connection.sendall(request)
        receipt['request_sent_ns']=time.monotonic_ns()
        while True:
            recv_started_ns=time.monotonic_ns()
            chunk=connection.recv(4096)
            recv_completed_ns=time.monotonic_ns()
            if not chunk:
                receipt['tcp_eof_observed']=True;receipt['eof_ns']=time.monotonic_ns();break
            if 'first_response_recv_completed_ns' not in receipt:
                receipt['first_response_recv_started_ns']=recv_started_ns
                receipt['first_response_recv_completed_ns']=recv_completed_ns
            recv_chunks.append({'started_ns':recv_started_ns,'completed_ns':recv_completed_ns,
                                'bytes':len(chunk),'prior_received_bytes':len(received)})
            received.extend(chunk)
            delimiter=received.find(b'\r\n\r\n')
            if delimiter >= 0 and 'headers_complete_recv_ns' not in receipt:
                receipt['headers_complete_recv_ns']=recv_completed_ns
                receipt['observed_header_bytes']=delimiter+4
            if delimiter >= 0 and len(received)>delimiter+4 and 'first_encoded_entity_recv_ns' not in receipt:
                receipt['first_encoded_entity_recv_ns']=recv_completed_ns
            if len(received)>131072:raise RuntimeError('bounded response exceeded128KiB')
    header,encoded_body=bytes(received).split(b'\r\n\r\n',1)
    lines=header.decode('ascii').split('\r\n')
    parts=lines[0].split()
    if len(parts)<2 or parts[0] not in ('HTTP/1.0','HTTP/1.1'):raise RuntimeError('invalid status line')
    status=parts[1]
    fields=[line.split(':',1) for line in lines[1:]]
    lengths=[value.strip() for name,value in fields if name.lower()=='content-length']
    transfer=[value.strip().lower() for name,value in fields if name.lower()=='transfer-encoding']
    decoded=encoded_body
    framing='close_delimited'
    if lengths and transfer:raise RuntimeError('ambiguous Content-Length and Transfer-Encoding')
    if lengths:
        framing='content_length'
        if len(lengths)!=1 or not lengths[0].isascii() or not lengths[0].isdecimal() or int(lengths[0])!=len(decoded):
            raise RuntimeError('ambiguous or truncated Content-Length response')
    elif transfer:
        if transfer!=['chunked']:raise RuntimeError('unsupported Transfer-Encoding')
        framing='chunked';remaining=encoded_body;chunks=[]
        while True:
            length_line,remaining=remaining.split(b'\r\n',1)
            length_text=length_line.split(b';',1)[0]
            if not length_text or any(byte not in b'0123456789abcdefABCDEF' for byte in length_text):
                raise RuntimeError('invalid chunk size')
            length=int(length_text,16)
            if length==0:
                if remaining!=b'\r\n':raise RuntimeError('unexpected trailers or bytes after terminal chunk')
                break
            if len(remaining)<length+2 or remaining[length:length+2]!=b'\r\n':raise RuntimeError('truncated chunk')
            chunks.append(remaining[:length]);remaining=remaining[length+2:]
        decoded=b''.join(chunks)
    header_file.write_bytes(header+b'\r\n\r\n');body_file.write_bytes(decoded)
    receipt.update(status=int(status),headers=lines,entity_bytes=len(decoded),
                   entity_sha256=hashlib.sha256(decoded).hexdigest(),
                   framing={'kind':framing,'content_lengths':lengths,'transfer_encoding':transfer,
                            'encoded_entity_bytes':len(encoded_body),'decoded_entity_bytes':len(decoded)})
    exit_code=0
except ConnectionResetError as error:
    receipt['tcp_reset_observed']=True;receipt['error']={'type':type(error).__name__,'message':str(error)}
except TimeoutError as error:
    receipt['timeout_observed']=True;receipt['error']={'type':type(error).__name__,'message':str(error)}
except Exception as error:
    receipt['error']={'type':type(error).__name__,'message':str(error)}
finally:
    (root/(token+'.request.raw')).write_bytes(request)
    (root/(token+'.response.raw')).write_bytes(received)
    receipt.update(completed_ns=time.monotonic_ns(),proposed_process_exit=exit_code,actual_socket_recv_chunks=recv_chunks)
    (root/(token+'.receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n')
sys.stdout.write(status)
raise SystemExit(exit_code)
