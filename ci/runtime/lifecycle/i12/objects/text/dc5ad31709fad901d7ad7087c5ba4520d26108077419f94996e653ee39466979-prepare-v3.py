"""Retain all old inputs; add actual output handoff and socket-read boundaries."""
import hashlib
import json
from pathlib import Path
import shutil

BASE = Path(__file__).resolve().parent
SOURCE = BASE / 'source-v5'
FIXTURES = BASE / 'fixtures-v3'
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def replace(path, old, new):
    text = path.read_text()
    assert text.count(old) == 1, (path, old, text.count(old))
    path.write_text(text.replace(old, new))
for original, target in ((BASE/'source-v4',SOURCE),(BASE/'fixtures-v1',FIXTURES)):
    shutil.copytree(original,target)
    for path in target.rglob('*'):
        path.chmod(0o700 if path.is_dir() else 0o600 | (path.stat().st_mode & 0o111))
    target.chmod(0o700)
filters = SOURCE/'connectors/apache/src/msc_filters.c'
replace(filters, '    rc = ap_pass_brigade(f->next, brigade);',
'''    apache_lifecycle_observe(terminal ? "output_terminal_release_enter" : "output_prefix_release_enter", msr, r, NULL);
    rc = ap_pass_brigade(f->next, brigade);
    apache_lifecycle_observe(terminal ?
        (rc == APR_SUCCESS ? "output_terminal_release_return_ok" : "output_terminal_release_return_error") :
        (rc == APR_SUCCESS ? "output_prefix_release_return_ok" : "output_prefix_release_return_error"), msr, r, NULL);''')
observer = SOURCE/'connectors/apache/src/apache-host-observer.c'
replace(observer, '"\\\"request_eos_released\\\":%d,\\\"response_eos_seen\\\":%d,"',
    '"\\\"response_committed\\\":%d,\\\"response_eos_released\\\":%d,\\\"terminal_event_attempted\\\":%d,\\\"event_sink_error\\\":%d,"\n        "\\\"request_eos_released\\\":%d,\\\"response_eos_seen\\\":%d,"')
replace(observer, '        msr != NULL ? msr->request_body_eos_released : -1,',
'''        msr != NULL ? msr->response.committed : -1,
        msr != NULL ? msr->response_phase4_eos_released : -1,
        msr != NULL ? msr->intervention.terminal_event_attempted : -1,
        msr != NULL ? (int)msr->intervention.event_sink_error : -1,
        msr != NULL ? msr->request_body_eos_released : -1,''')
client = FIXTURES/'curl-raw-client.py'
replace(client, "received=bytearray()", "received=bytearray()\nrecv_chunks=[]")
replace(client, '            chunk=connection.recv(4096)',
'''            recv_started_ns=time.monotonic_ns()
            chunk=connection.recv(4096)
            recv_completed_ns=time.monotonic_ns()''')
replace(client, '            received.extend(chunk)',
'''            if 'first_response_recv_completed_ns' not in receipt:
                receipt['first_response_recv_started_ns']=recv_started_ns
                receipt['first_response_recv_completed_ns']=recv_completed_ns
            recv_chunks.append({'started_ns':recv_started_ns,'completed_ns':recv_completed_ns,
                                'bytes':len(chunk),'prior_received_bytes':len(received)})
            received.extend(chunk)
            delimiter=received.find(b'\\r\\n\\r\\n')
            if delimiter >= 0 and 'headers_complete_recv_ns' not in receipt:
                receipt['headers_complete_recv_ns']=recv_completed_ns
                receipt['observed_header_bytes']=delimiter+4
            if delimiter >= 0 and len(received)>delimiter+4 and 'first_encoded_entity_recv_ns' not in receipt:
                receipt['first_encoded_entity_recv_ns']=recv_completed_ns''')
replace(client, '    receipt.update(completed_ns=time.monotonic_ns(),proposed_process_exit=exit_code)',
    '    receipt.update(completed_ns=time.monotonic_ns(),proposed_process_exit=exit_code,actual_socket_recv_chunks=recv_chunks)')
case = FIXTURES/'tests/cases/connector-specific/apache/NEED-request-eos-once.yaml'
replace(case, '  SecRule RESPONSE_HEADERS:Content-Type',
'''  SecRule REQUEST_METHOD "@streq POST" "id:91041002,phase:1,pass,log,t:none,chain,msg:'test-only Apache genuine Common sink admission'"
      SecRule REQUEST_URI "@streq /i12/apache/eos" "t:none"
  SecRule RESPONSE_HEADERS:Content-Type''')
contract = json.loads((FIXTURES/'fixture-contract.json').read_text())
contract['supplemental_contract']['common_nonterminal_rule_id']=91041002
contract['supplemental_contract']['common_physical_nonterminal_request_rule_match_count']=1
contract['supplemental_contract']['common_physical_terminal_event_count']=0
contract['supplemental_contract']['wire_observation']='Actual one-request client socket recv timestamps and source-copy actual next-filter ap_pass_brigade enter/return callbacks. No kernel-send inference.'
contract['supplemental_contract']['effective_rules'] += ' One benign scoped POST/path P1 pass/log marker exercises the genuine existing Common physical event sink; native P4 marker remains non-disruptive.'
(FIXTURES/'fixture-contract.json').write_text(json.dumps(contract,indent=2,sort_keys=True)+'\n')
old=json.loads((BASE/'source-v4-ledger.json').read_text())['files']
new={str(p.relative_to(SOURCE)):sha(p) for p in SOURCE.rglob('*') if p.is_file()}
changes={name:{'before':old.get(name),'after':value} for name,value in new.items() if old.get(name)!=value}
assert set(changes)=={'connectors/apache/src/msc_filters.c','connectors/apache/src/apache-host-observer.c'}
(BASE/'v3-overlay-manifest.json').write_text(json.dumps({'source_changes':changes,
    'fixture_changes':{str(p.relative_to(FIXTURES)):sha(p) for p in FIXTURES.rglob('*') if p.is_file()},
    'host_launched':False,'source_shared_observer_revision_unchanged':'a4ce3e2513bc3a9300781873119c256fe12f384427d4a4bb3b49578afd6a1df8',
    'wire_semantics':'Actual client first received wire bytes, bounded socket recv bracket, no exact kernel send claim.',
    'sink_semantics':'Genuine Common event writer emits one actual nonterminal P1 match for POST. Allow has no intervention/terminal event; zero terminal subset is measured on configured physically exercised sink.'},indent=2,sort_keys=True)+'\n')
print(json.dumps({'source_changes':list(changes),'fixture':str(case),'host_launched':False}))
