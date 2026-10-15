import hashlib,json,signal,time,ssl,sys
from http.server import BaseHTTPRequestHandler,HTTPServer
from pathlib import Path
class Handler(BaseHTTPRequestHandler):
    protocol_version='HTTP/1.1'
    def do_POST(self):
        length=int(self.headers['Content-Length']); body=self.rfile.read(length)
        response=b'haproxy-lifecycle-response\n'
        row={'path':self.path,'method':self.command,'headers':list(self.headers.items()),'body_bytes':len(body),'body_sha256':hashlib.sha256(body).hexdigest(),'body_complete':len(body)==length,'response_bytes':len(response),'response_sha256':hashlib.sha256(response).hexdigest(),'wall_ns':time.time_ns()}
        with Path('/task/backend.jsonl').open('a') as out:out.write(json.dumps(row)+'\n')
        self.send_response(200);self.send_header('Content-Type','text/plain');self.send_header('Content-Length',str(len(response)));self.send_header('Connection','close');self.end_headers();self.wfile.write(response);self.wfile.flush();self.close_connection=True
    def log_message(self,*args):pass
server=HTTPServer(('127.0.0.1',18491),Handler)
if len(sys.argv)>1 and sys.argv[1]=='tls':
    context=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER);context.load_cert_chain('/task/tls.crt','/task/tls.key');server.socket=context.wrap_socket(server.socket,server_side=True)
signal.signal(signal.SIGTERM,lambda *args: (_ for _ in ()).throw(SystemExit(0)))
Path('/task/backend.ready').write_text('ready\n')
server.serve_forever()
