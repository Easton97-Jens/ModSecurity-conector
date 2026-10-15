"""Separate genuine Parent fixture backend process; actual capture only."""
import importlib.util
from http.server import HTTPServer
import os
from pathlib import Path
import signal
import sys
sys.path.insert(0,'/mnt/src/ci/runtime/common')
spec=importlib.util.spec_from_file_location('lighttpd_independent_backend','/mnt/fixtures/observed-backend.py')
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
module.Handler.body_bytes=b'apx-eos-response-payload'
module.Handler.fixture=module.ResponseFixture(200,(('Content-Type','text/plain'),))
server=HTTPServer(('127.0.0.1',int(sys.argv[1])),module.Handler)
Path('/task/backend-ready.json').write_text('{"pid":'+str(os.getpid())+',"port":'+str(server.server_port)+'}\n')
def stop(_signum,_frame):raise SystemExit(0)
signal.signal(signal.SIGTERM,stop)
try:server.serve_forever(poll_interval=0.05)
finally:server.server_close()
