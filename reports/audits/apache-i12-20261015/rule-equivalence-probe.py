import ctypes as c
import hashlib,json,re
from pathlib import Path
import yaml
ROOT=Path('/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T182400Z-pr410-oracle-lifecycle/sealed-common-inputs/framework')
LIB=Path('/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14')
lib=c.CDLL(str(LIB)); P=c.c_void_p; S=c.c_char_p; I=c.c_int
class Intervention(c.Structure):
 _fields_=[('status',I),('pause',I),('url',S),('log',S),('disruptive',I)]
def bind(name,ret,args):
 f=getattr(lib,name);f.restype=ret;f.argtypes=args;return f
init=bind('msc_init',P,[]);newrules=bind('msc_create_rules_set',P,[])
add=bind('msc_rules_add',I,[P,S,c.POINTER(S)])
newtx=bind('msc_new_transaction',P,[P,P,P])
conn=bind('msc_process_connection',I,[P,S,I,S,I]);uri=bind('msc_process_uri',I,[P,S,S,S])
rh=bind('msc_process_request_headers',I,[P]);rb=bind('msc_process_request_body',I,[P])
addh=bind('msc_add_response_header',I,[P,S,S]);resh=bind('msc_process_response_headers',I,[P,I,S])
append=bind('msc_append_response_body',I,[P,S,c.c_size_t]);p4=bind('msc_process_response_body',I,[P])
intervene=bind('msc_intervention',I,[P,c.POINTER(Intervention)])
log=bind('msc_process_logging',I,[P]);cleantx=bind('msc_transaction_cleanup',None,[P])
cleanrules=bind('msc_rules_cleanup',I,[P]);clean=bind('msc_cleanup',None,[P])
callbacktype=c.CFUNCTYPE(None,P,P);setcb=bind('msc_set_log_cb',None,[P,callbacktype])
pattern=re.compile(r'SecRule RESPONSE_BODY[^\n]*\n[^\n]*1100301[^\n]*\n')
preamble=ROOT/'tests/rules/no-crs-baseline.conf';canonical=pattern.search(preamble.read_text()).group()
assert 'SecDefaultAction' not in preamble.read_text()
records=[]
for name in ('phase4_body_at_limit','phase4_body_over_limit','phase4_body_reject'):
 source=next(ROOT.rglob(name+'.yaml'));fixture=yaml.safe_load(source.read_text());local=pattern.search(fixture['rules']).group()
 assert 'SecDefaultAction' not in fixture['rules']
 assert re.sub(r'\s+', ' ',canonical.replace(',t:none','')).strip()==re.sub(r'\s+',' ',local).strip()
 result={}
 for form,rule in [('local',local),('canonical',canonical)]:
  engine=init();rules=newrules();messages=[]
  cb=callbacktype(lambda data,message:messages.append(c.string_at(message).decode(errors='replace')));setcb(engine,cb)
  text=pattern.sub('',preamble.read_text())+'\n'+pattern.sub('',fixture['rules'])+'\n'+rule
  err=S();loaded=add(rules,text.encode(),c.byref(err));assert loaded>=0,err.value
  tx=newtx(engine,rules,None);assert tx
  calls=[conn(tx,b'127.0.0.1',1234,b'127.0.0.1',8080),uri(tx,b'/native-equivalence',b'GET',b'1.1'),rh(tx),rb(tx),addh(tx,b'Content-Type',b'text/plain'),resh(tx,200,b'HTTP/1.1')]
  body=fixture['response']['body'].encode();appended=append(tx,body,len(body));processed=p4(tx)
  intervention=Intervention(200,0,None,None,0);present=intervene(tx,c.byref(intervention));log(tx)
  result[form]={'rules_loaded':loaded,'calls':calls,'payload_bytes':len(body),'payload_sha256':hashlib.sha256(body).hexdigest(),'native_append_result':appended,'native_p4_result':processed,'intervention_present':present,'status':intervention.status,'disruptive':intervention.disruptive,'native_log_rule_ids':sorted(set(re.findall(r'\[id "(\d+)"\]', '\n'.join(messages)+(intervention.log.decode() if intervention.log else ''))))}
  cleantx(tx);cleanrules(rules);clean(engine)
 assert result['local']==result['canonical'],result
 records.append({'case':name,'source_path':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'local_rule':local,'canonical_rule':canonical,'comparison':result,'equivalent_for_exact_fixture':True})
value={'sdk_path':str(LIB),'sdk_sha256':hashlib.sha256(LIB.read_bytes()).hexdigest(),'canonical_path':str(preamble),'canonical_sha256':hashlib.sha256(preamble.read_bytes()).hexdigest(),'scope':'exact ASCII fixture payloads and same no-SecDefaultAction directives; no universal byte identity claim','cases':records,'all_equivalent':True}
Path(__file__).with_name('proof.json').write_text(json.dumps(value,indent=2)+'\n')
print(json.dumps(value,indent=2))
