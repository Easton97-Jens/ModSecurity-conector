"""Actual HTTP/2 stream close evidence with bounded unique method construction."""
import json
import re
from host_log_observations import extract, STAMP, TAGS, interval

def observe(raw, path):
 host=extract(raw,path)
 if not host['scope_verified']:return {'verified':False,'reason':'unknown downstream nonce stream','actual_stream_close':None}
 lines=raw.splitlines();start=host['decoded_nonce_original_line']-1
 end=next((i for i in range(start+1,len(lines)) if 'request headers complete (end_stream=' in lines[i] and 'conn_manager_impl.cc:' in lines[i]),len(lines))
 records=[]
 for i in range(start,end):
  stamp=STAMP.match(lines[i]);tag=TAGS.search(lines[i])
  if not stamp:continue
  try:tags=json.loads('{'+tag.group(1)+'}') if tag else {}
  except json.JSONDecodeError:tags={}
  records.append({'original_line':i+1,'text':lines[i],'tags':tags,'clock_interval':interval(stamp.group(1))})
 def unknown(reason):return {'verified':False,'reason':reason,'actual_stream_close':None}
 target=host['actual_host_stream_tags']
 opening=[r for r in records if r['tags']==target and 'ext_proc.cc:' in r['text'] and 'Opening gRPC stream to external processor' in r['text']]
 methods=[r for r in records if 'router.cc:' in r['text'] and "match for URL '/envoy.service.ext_proc.v3.ExternalProcessor/Process'" in r['text']]
 if len(opening)!=1 or len(methods)!=1 or methods[0]['original_line']<=opening[0]['original_line']:return unknown('missing or ambiguous actual gRPC Process construction')
 method=methods[0];payload=[]
 for r in records:
  match=re.search(r'Http2Visitor: remaining data payload: \d+, stream_id: (\d+), end_stream: (true|false)',r['text'])
  if match and r['original_line']>method['original_line'] and 'http2/codec_impl.cc:' in r['text']:
   payload.append((r['tags'].get('ConnectionId'),match.group(1),r))
 keys={(c,s) for c,s,_ in payload}
 if len(keys)!=1 or not payload:return unknown('missing or ambiguous actual HTTP2 connection/stream')
 connection,stream=next(iter(keys))
 resets=[r for r in records if r['tags']==method['tags'] and 'upstream_request.cc:' in r['text'] and 'resetting pool request' in r['text'] and r['original_line']>payload[-1][2]['original_line']]
 closes=[r for r in records if r['tags'].get('ConnectionId')==connection and 'http2/codec_impl.cc:' in r['text'] and re.search(r' stream '+re.escape(stream)+r' closed: \d+$',r['text']) and r['original_line']>payload[-1][2]['original_line']]
 if len(resets)!=1 or len(closes)!=1 or resets[0]['original_line']>=closes[0]['original_line']:return unknown('missing or ambiguous actual request reset/HTTP2 onStreamClose')
 close=closes[0];sent=[r for r in records if r['tags'].get('ConnectionId')==connection and 'http2/codec_impl.cc:' in r['text'] and 'sent reset code=' in r['text'] and resets[0]['original_line']<r['original_line']<close['original_line']]
 if len(sent)!=1:return unknown('missing or ambiguous actual sent-reset callback')
 unary_methods=[r for r in records if 'router.cc:' in r['text'] and "match for URL '/envoy.service.auth.v3.Authorization/Check'" in r['text'] and r['original_line']<opening[0]['original_line']]
 unary=None
 if len(unary_methods)==1:
  u=unary_methods[0];urows=[r for r in records if u['original_line']<r['original_line']<opening[0]['original_line']];up=[]
  for r in urows:
   match=re.search(r'Http2Visitor: remaining data payload: \d+, stream_id: (\d+),',r['text'])
   if match:up.append((r['tags'].get('ConnectionId'),match.group(1),r))
  ukeys={(c,s) for c,s,_ in up}
  if len(ukeys)==1:
   uc,us=next(iter(ukeys));allclose=[r for r in records if r['original_line']>u['original_line'] and r['original_line']<method['original_line'] and r['tags'].get('ConnectionId')==uc and re.search(r' stream '+re.escape(us)+r' closed: 0$',r['text'])]
   trailers=[{'original_line':i+1,'text':lines[i]} for i in range(u['original_line'],opening[0]['original_line']-1) if lines[i]=="'grpc-status', '0'"]
   if len(allclose)==len(trailers)==1:unary={'method':u,'http2_connection':uc,'http2_stream':us,'actual_success_trailer':trailers[0],'actual_stream_close':allclose[0]}
 return {'verified':True,'downstream_actual_tags':target,'opening':opening[0],'actual_method_construction':method,'actual_http2_connection':connection,'actual_http2_stream':stream,'actual_received_payload_callbacks':[r for _,_,r in payload],'actual_pool_request_reset':resets[0],'actual_sent_reset_callback':sent[0],'actual_stream_close':close,'numeric_actual_close_code':int(close['text'].rsplit(': ',1)[1]),'unary_authorization_grpc_end':unary,'scope_contract':'one selected request then separately waited neighbor; unique actual method construction and HTTP2 payload stream in that request interval, own async request reset and codec onStreamClose. No ID equality runtime join. Actual local reset closure; no remote grpc-status/EOF inferred.'}
