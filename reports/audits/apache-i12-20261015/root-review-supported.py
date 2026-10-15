"""Root review for seven explicitly specified supported request obligations.

Expectations derive from the retained native SDK contract and exact fixtures.
This whitelist deliberately excludes limits, framing faults and historical IDs.
"""
import collections
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

WT=Path('/var/tmp/codex/ModSecurity-conector/worktrees/i12-apache-410-20261015')
BASE=Path('/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle')
OUT=Path(__file__).resolve().parent
APPROVED=OUT/'approved'; APPROVED.mkdir(mode=0o700,exist_ok=True)
spec=importlib.util.spec_from_file_location('review',WT/'ci/runtime/lifecycle/apache-i12/review.py')
R=importlib.util.module_from_spec(spec);spec.loader.exec_module(R)
L=R.LEDGER
baseline=json.loads((BASE/'ledger/twentyone-qualified-08.json').read_text())
rows={r['selected_requirement']['case_id']:r for r in L.apache_rows(baseline)}
expected={
 'NEED-request-empty':(b'', 'text/plain'),
 'NEED-request-single-chunk':(b'apx-eos-request-payload','text/plain'),
 'NEED-request-content-type-present':(b'apx-eos-request-payload','text/plain'),
 'NEED-request-content-type-missing':(b'apx-eos-request-payload',None),
 'NEED-request-charset-present':(b'apx-eos-request-payload','text/plain; charset=utf-8'),
 'NEED-request-charset-missing':(b'apx-eos-request-payload','text/plain'),
 'NEED-request-csv':(b'column_a,column_b\nvalue_a,value_b\n','text/csv'),
}
def ref(path,**extra):return {**L.ORACLES.reference(Path(path).resolve(strict=True)),**extra}
def sha(data):return hashlib.sha256(data).hexdigest()

sources=[ref(BASE/'source-proof/sdk-3.0.14-transaction.cc',kind='native_engine_contract',revision='ModSecurity v3.0.14'),
         ref(BASE/'source-proof/rfc9110.txt',kind='protocol_contract',revision='RFC9110')]
assert sources[0]['sha256']=='328ffa3b4517f0242450293a916aba4f512b4defc3bd1fcc7465e0778adc725c'
assert sources[1]['sha256']=='21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a'
index=json.loads((OUT/'host-runs/index.json').read_text()) if (OUT/'host-runs/index.json').exists() else []
index=[{'case':'NEED-request-empty','attempt':str(BASE/'isolation/attempt-1792071942428624144')},*index]
packets=[];records=[];results=[]
for run in index:
    name=run['case']
    if name not in expected:continue
    packet_path=APPROVED/(name+'.json'); oracle_path=APPROVED/(name+'.oracle.json')
    if packet_path.exists():
        packets.append(ref(packet_path));records.append(json.loads(oracle_path.read_text()));continue
    prepared=BASE/'apache-i12-20261015'/name
    p=R.extract(Path(run['attempt']),prepared/'admission-spec.json',name,
                evidence_branch_base='f27eb59b53beff6f65384fc2e5037881a3052c01')
    o=p['observations'];v={k:item.get('value') for k,item in o.items()}
    body,content_type=expected[name]
    assert not p['unknown_fields'],p['unknown_fields']
    assert all(p['review_checks'].values()),p['review_checks']
    assert p['parent_sha']=='02754040bced960cfc1857416cd7101bb3116ef4'
    assert p['framework_sha']=='99a7985c1be92a2297b1b59208f64df6768f2cbf'
    assert p['mrts_sha']=='8a6bb546c4c81d8ffc7be801dceac60c6925685f'
    assert v['client_exit']==0 and v['client_signal']['actual_signal'] is None
    assert v['client_bytes']=={'request':len(body),'response_entity':24}
    assert v['client_sha256']=={'request':sha(body),'response_entity':sha(b'apx-eos-response-payload')}
    assert v['client_headers'][0]=='HTTP/1.1 200 OK'
    c=next(x for x in Path(run['attempt']).joinpath('data/client').glob('*.receipt.json')
           if json.loads(x.read_text()).get('method')=='POST')
    wire=c.with_name(c.name.replace('.receipt.json','.request.raw')).read_bytes()
    wire_headers,wire_body=wire.split(b'\r\n\r\n',1)
    assert wire_body==body
    actual_types=[line.split(b':',1)[1].strip().decode() for line in wire_headers.split(b'\r\n')
                  if line.lower().startswith(b'content-type:')]
    assert actual_types==([] if content_type is None else [content_type]),actual_types
    assert v['backend_request_count']['main']==1
    assert v['client_backend_correlation']['request_body_hash_equal'] is True
    assert v['client_backend_correlation']['response_body_hash_equal'] is True
    phases=[(x['phase'],x['result']) for x in v['native_phases'] if x['phase'] in (1,2,3,4)]
    assert phases==[(1,1),(2,1),(3,1),(4,1)],phases
    chunks=v['native_body_chunks']
    assert sum(x['input_size'] for x in chunks if x['function']=='native_append_request_body')==len(body)
    assert sum(x['input_size'] for x in chunks if x['function']=='native_append_response_body')==24
    if name=='NEED-request-single-chunk':
        assert sum(x['function']=='native_append_request_body' for x in chunks)==1
    eos=collections.Counter(x['kind'] for x in v['host_eos']['actual_apr_eos_rows'])
    assert eos=={'actual_request_apr_eos':1,'actual_response_apr_eos':1},eos
    assert v['finish_calls']=={'common_finish':1,'native_logging':1}
    assert v['native_free_calls']=={'native_cleanup':1,'common_cleanup':1,'host_association_retire':1}
    assert v['finish_transitions']['completed_status_3_transitions']==1
    native=v['native_intervention_or_first_cause']['actual_native_intervention_returns']
    assert native and all(x['result']==0 for x in native)
    events=v['native_events']; common=events['physical_common_rows']
    assert len(common)==1 and common[0]['rule_id']=='91041002'
    assert common[0]['event']=='rule_match' and common[0]['actual_action']=='allow'
    assert sum('[id "91041001"]' in x for x in events['native_audit_lines'])==1
    assert v['terminal_event_count']['actual_common_terminal_subset_count']==0
    assert events['common_sink_mode']=='0o600'
    fd=v['descriptor_cleanup']['actual_fd_differences']
    assert not fd['main']['removed'] and not fd['main']['changed']
    assert set(fd['main']['added'].values()) <= {'/task/apache-host-eos.jsonl'}
    assert not any(fd['neighbor'][k] for k in ('added','removed','changed'))
    n=v['neighbor_health'];assert n['same_native_host_pid'] is True
    assert n['actual_waited_process']['actual_waited_exit_code']==0
    assert n['separate_actual_client']['status']==200 and len(n['independent_backend'])==1
    assert v['transport_framing']['kind']=='content_length'
    assert v['transport_reset_scope']=={'tcp_eof_observed':True,'tcp_reset_observed':False,
                                      'timeout_observed':False,'error':None}
    status=v['product_host_identity']['actual_proc_status']
    assert v['product_host_identity']['actual_uid']==v['product_host_identity']['actual_gid']==65534
    assert all(f'{k}:\t0000000000000000' in status for k in ('CapInh','CapPrm','CapEff','CapBnd','CapAmb'))
    images=v['product_host_identity']['mapped_images']
    assert any(x['sha256']=='32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407' for x in images)
    assert any(x['sha256']=='d4244dde8ebfae13fe513ee8464522acbbf1bab4a239f00d2315de40688a1a01' for x in images)
    oracle={'native_result':'allow','visible_status':200,'phase':2,'rule_id':None,
      'event_fields':[],'physical_evidence_not_projection':True,'unresolved_expected_value_reason':None,
      'request_body_bytes':len(body),'request_content_type':content_type,
      'request_apr_eos':1,'response_apr_eos':1,'native_request_body_finalizations':1,
      'native_response_body_finalizations':1,'common_finish_calls':1,'native_free_calls':1,
      'scope':'Bounded supported native request; CSV is raw bytes, no CSV-specific processor claim.'}
    record={'run_scoped_case_id':p['run_scoped_case_id'],'leg_id':'apache-native','reviewed_by':'root',
      'category':'SOURCE_CONFIRMED_EXPECTATION','resolved_expectation':oracle,
      'interpretation':'Exact supplemental input resolved using native SDK body processing and protocol entity semantics; original null oracle is preserved.',
      'scope':'Only this independently executed Apache2.4.66/APR1.7.6/SDK3.0.14 request. No truncation, native file, streaming, size-limit, or sibling-case promotion.',
      'independent_sources':sources,'implementation_sources':[ref(prepared/'fixtures/fixture-contract.json',revision='Apache task-owned fixture 20261015')]}
    review=L.ORACLES.review_record(record,rows[name])
    p.update(reviewed_by='root',oracle_evaluated=True,oracle_sha256=L.ORACLES.canonical_digest(oracle),
             outcome='PASS',full_lifecycle_qualified=True,candidate_is_not_an_approval=False,
             root_review='Explicit whitelist source/fixture and actual35-field review; assertions in approve_supported.py retained.')
    packet_path.write_text(json.dumps(p,indent=2)+'\n');oracle_path.write_text(json.dumps(record,indent=2)+'\n')
    L.SHARED.reviewed_packet(ref(packet_path),rows[name],review['effective_oracle'])
    packets.append(ref(packet_path));records.append(record);results.append({'case':name,'outcome':'PASS','packet':ref(packet_path)})
(OUT/'reviewed-packets.json').write_text(json.dumps({'packets':packets},indent=2)+'\n')
(OUT/'reviewed-oracles.json').write_text(json.dumps({'records':records},indent=2)+'\n')
print(json.dumps({'qualified':len(packets),'newly_reviewed':results}))
