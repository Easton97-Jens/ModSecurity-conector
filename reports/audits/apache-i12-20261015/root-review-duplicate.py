"""Root qualification of the pinned Apache-core duplicate-header oracle only."""
import copy,hashlib,importlib.util,json
from pathlib import Path
W=Path('/var/tmp/codex/ModSecurity-conector/worktrees/i12-apache-410-20261015')
O=Path(__file__).resolve().parent
B=Path('/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle')
s=importlib.util.spec_from_file_location('review',W/'ci/runtime/lifecycle/apache-i12/review.py');R=importlib.util.module_from_spec(s);s.loader.exec_module(R)
L=R.LEDGER
r=next(x for x in json.loads((O/'apache-ledger-interim.json').read_text())['rows'] if x['run_scoped_case_id']=='I12::apache-native::duplicate_header_names')
p=json.loads((O/'candidates/attempt-1792074105980006823.json').read_text());v={k:x['value'] for k,x in p['observations'].items()}
assert not p['unknown_fields'] and all(p['review_checks'].values())
assert p['parent_sha']=='02754040bced960cfc1857416cd7101bb3116ef4'
for source in r['oracle_reconciliation']['independent_sources']: L.ORACLES.verify_reference(source)
effective=r['oracle_reconciliation']['effective_oracle']
assert effective['apache_core_header_count']==1 and effective['apache_core_ordered_header_value']=='one, two'
assert v['client_exit']==0 and v['client_headers'][0]=='HTTP/1.1 200 OK' and v['client_bytes']['response_entity']==24
assert v['backend_request_count']['main']==1 and v['client_backend_correlation']['request_body_hash_equal'] and v['client_backend_correlation']['response_body_hash_equal']
assert [(x['phase'],x['result']) for x in v['native_phases'] if x['phase'] in (1,2,3,4)]==[(1,1),(2,1),(3,1),(4,1)]
assert v['finish_calls']=={'common_finish':1,'native_logging':1}
assert v['native_free_calls']=={'native_cleanup':1,'common_cleanup':1,'host_association_retire':1}
assert v['finish_transitions']['completed_status_3_transitions']==1
assert all(x['result']==0 for x in v['native_intervention_or_first_cause']['actual_native_intervention_returns'])
e=v['native_events']; assert len(e['physical_common_rows'])==1
row=e['physical_common_rows'][0];assert row['rule_id']=='1100504' and row['phase']=='request_headers' and row['actual_action']=='allow'
assert len(e['native_audit_lines'])==1 and '[id "1100504"]' in e['native_audit_lines'][0] and 'one, two' in e['native_audit_lines'][0]
a=B/'isolation/attempt-1792074105980006823/data'
wire=[x for x in (a/'client').glob('*.request.raw') if b'/no-crs/headers/duplicate ' in x.read_bytes()]
assert len(wire)==1
headers=[x.split(b':',1)[1].strip() for x in wire[0].read_bytes().split(b'\r\n\r\n',1)[0].split(b'\r\n') if x.lower().startswith(b'x-no-crs-duplicate:')]
assert headers==[b'one',b'two']
h=v['host_eos']['all_main_host_rows'];k={x['kind']:x['monotonic_ns'] for x in h}
assert sum(x['kind']=='actual_request_apr_eos' for x in h)==sum(x['kind']=='actual_response_apr_eos' for x in h)==1
edges=v['commit_order']['native_p4_edges'];assert len(edges)==2
assert k['output_prefix_release_return_ok']<edges[0]['monotonic_ns']<edges[1]['monotonic_ns']<k['output_terminal_release_enter']
assert v['terminal_event_count']['actual_common_terminal_subset_count']==0
fd=v['descriptor_cleanup']['actual_fd_differences'];assert not fd['main']['removed'] and not fd['main']['changed']
assert set(fd['main']['added'].values()) <= {'/task/apache-host-eos.jsonl'}
assert not any(fd['neighbor'][x] for x in ('added','removed','changed'))
n=v['neighbor_health'];assert n['same_native_host_pid'] and n['separate_actual_client']['status']==200 and n['actual_waited_process']['actual_waited_exit_code']==0 and len(n['independent_backend'])==1
images=v['product_host_identity']['mapped_images'];assert any(x['sha256']=='32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407' for x in images)
assert any(x['sha256']=='d4244dde8ebfae13fe513ee8464522acbbf1bab4a239f00d2315de40688a1a01' for x in images)
p.update(reviewed_by='root',oracle_evaluated=True,oracle_sha256=L.ORACLES.canonical_digest(effective),outcome='PASS',full_lifecycle_qualified=True,candidate_is_not_an_approval=False,
 root_review='Existing independently source-confirmed version-bound correction; original failure retained; raw two-line input plus Root assertions and independent audit. Literal comma singleton remains indistinguishable downstream.')
dest=O/'approved/duplicate_header_names.json';dest.write_text(json.dumps(p,indent=2)+'\n')
ref=L.ORACLES.reference(dest);review=L.SHARED.reviewed_packet(ref,r['historical_result'],effective);assert review['full_lifecycle_qualified']
mp=O/'reviewed-packets.json';m=json.loads(mp.read_text());m['packets']=[x for x in m['packets'] if not x['path'].endswith('/duplicate_header_names.json')]+[ref];mp.write_text(json.dumps(m,indent=2)+'\n');print(json.dumps({'qualified':True,'packet':ref}))
