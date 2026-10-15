"""Source-bound Envoy logger extraction. Original rows are never rewritten."""
import datetime
import json
import re
STAMP = re.compile(r'^\[(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}(?:[+-]\d{2}:?\d{2}|Z))\]')
TAGS = re.compile(r'\[Tags:\s*([^\]]+)\]')
def interval(stamp):
    value=datetime.datetime.fromisoformat(stamp)
    if value.tzinfo is None: return None
    delta=value-datetime.datetime(1970,1,1,tzinfo=datetime.timezone.utc)
    ns=(delta.days*86400+delta.seconds)*1000000000+delta.microseconds*1000
    return {'lower_wall_ns':ns,'upper_exclusive_wall_ns':ns+1000000,'quantization_ns':1000000}
def extract(raw,path):
    blocks=[]
    for number,line in enumerate(raw.splitlines(),1):
        match=STAMP.match(line)
        if match:
            tag=TAGS.search(line)
            try: scope=json.loads('{'+tag.group(1)+'}') if tag else {}
            except json.JSONDecodeError:scope={}
            blocks.append({'line':number,'text':line,'scope':(scope.get('ConnectionId'),scope.get('StreamId')),'clock':interval(match.group(1))})
        elif blocks:blocks[-1]['text']+='\n'+line
    matches=[b for b in blocks if 'conn_manager_impl.cc:' in b['text'] and 'request headers complete (end_stream=' in b['text'] and ':path' in b['text'] and (repr(path) in b['text'] or json.dumps(path) in b['text']) and all(b['scope'])]
    scopes={b['scope'] for b in matches}
    if len(scopes)!=1 or len(matches)!=1:return {'scope_verified':False,'reason':'missing_or_ambiguous_actual_decoded_nonce','codec_headers':[],'codec_body':[],'grpc_remote_close':[],'filter_destroy':[]}
    scope=next(iter(scopes));same=[b for b in blocks if b['scope']==scope]
    def rows(marker,file):return [{'original_line':b['line'],'clock_interval':b['clock'],'original_first_line':b['text'].splitlines()[0]} for b in same if marker in b['text'] and file in b['text']]
    return {'scope_verified':True,'actual_host_stream_tags':{'ConnectionId':scope[0],'StreamId':scope[1]},'decoded_nonce_original_line':matches[0]['line'],'codec_headers':rows('encoding headers via codec (end_stream=','conn_manager_impl.cc:'),'codec_body':rows('encoding data via codec (size=','conn_manager_impl.cc:'),'grpc_remote_close':rows('Received gRPC stream close','ext_proc.cc:'),'grpc_close_attempt':rows('Calling close on stream','ext_proc.cc:'),'filter_destroy':rows('onDestroy','ext_proc.cc:'),'claim':'actual existing host callbacks only; no kernel send/allocator free/status/commit inferred from protocol send'}
