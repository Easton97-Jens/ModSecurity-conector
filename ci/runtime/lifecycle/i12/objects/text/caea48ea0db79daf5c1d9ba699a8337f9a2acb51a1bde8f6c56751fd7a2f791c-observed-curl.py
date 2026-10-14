#!/usr/local/bin/python3
"""Wait the actual raw client once and retain its actual process exit."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from urllib.parse import urlsplit

arguments=sys.argv[1:]
if any('/i12/apache/eos' in argument for argument in arguments):
    output=Path('/task/client');output.mkdir(mode=0o700,exist_ok=True)
    token=str(time.time_ns())
    env=dict(os.environ,I12_APACHE_CLIENT_TOKEN=token)
    if os.environ.get('I12_APACHE_CAPTURE_DELAY')=='1':time.sleep(0.2)
    argv=['rtk','proxy',sys.executable,str(Path(__file__).with_name('curl-raw-client.py')),*arguments]
    result=subprocess.run(argv,env=env,capture_output=True,timeout=25)
    (output/(token+'.actual-process.json')).write_text(json.dumps({
        'argv':argv,'actual_waited_exit_code':result.returncode,
        'actual_signal':-result.returncode if result.returncode<0 else None,
        'stdout_bytes':len(result.stdout),'stderr_bytes':len(result.stderr),
        'client_completed_before_wrapper_exit':True},indent=2)+'\n')
    if result.returncode==0 and os.environ.get('I12_APACHE_FOLLOWUP')=='1':
        url=next(argument for argument in arguments if argument.startswith('http://'))
        parsed=urlsplit(url)
        neighbor_token=str(time.time_ns())
        neighbor_args=['-sS','--http1.1','-D',str(output/'neighbor.headers'),'-X','GET',
            '-o',str(output/'neighbor.body'),'-w','%{http_code}','-H','X-Modsec-Smoke: allow',
            f'http://127.0.0.1:{parsed.port}/no-crs/allow']
        neighbor_argv=['rtk','proxy',sys.executable,str(Path(__file__).with_name('curl-raw-client.py')),*neighbor_args]
        neighbor=subprocess.run(neighbor_argv,env=dict(os.environ,I12_APACHE_CLIENT_TOKEN=neighbor_token),
                                capture_output=True,timeout=25)
        (output/(neighbor_token+'.actual-process.json')).write_text(json.dumps({
            'argv':neighbor_argv,'actual_waited_exit_code':neighbor.returncode,
            'actual_signal':-neighbor.returncode if neighbor.returncode<0 else None,
            'actual_stdout':neighbor.stdout.decode('ascii'),'stderr_bytes':len(neighbor.stderr),
            'role':'separate_original_allow_neighbor','main_client_token':token,
            'does_not_replace_main_outcome':True},indent=2)+'\n')
    if os.environ.get('I12_APACHE_CAPTURE_DELAY')=='1':time.sleep(0.2)
else:
    # Existing readiness/version probes retain genuine curl behavior.
    result=subprocess.run(['rtk','proxy','/usr/bin/curl',*arguments],capture_output=True,timeout=25)
sys.stdout.buffer.write(result.stdout);sys.stderr.buffer.write(result.stderr)
raise SystemExit(result.returncode)
