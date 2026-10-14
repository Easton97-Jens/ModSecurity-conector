import unittest
from grpc_stream_observations import observe

def fixture():
 def row(file,tags,text):return '[2026-10-14T12:00:00.123+0000] [1] [debug] [http] ['+file+':1] [Tags: '+tags+'] '+text+'\n'
 host='"ConnectionId":"1","StreamId":"2"';rpc='"ConnectionId":"0","StreamId":"9"';codec='"ConnectionId":"3"'
 return row('conn_manager_impl.cc',host,"request headers complete (end_stream=false):\n':path', '/own'")+row('ext_proc.cc',host,'Opening gRPC stream to external processor')+row('router.cc',rpc,"cluster 'native' match for URL '/envoy.service.ext_proc.v3.ExternalProcessor/Process'")+row('http2/codec_impl.cc',codec,'Http2Visitor: remaining data payload: 9, stream_id: 1, end_stream: false')+row('upstream_request.cc',rpc,'resetting pool request')+row('http2/codec_impl.cc',codec,'sent reset code=2')+row('http2/codec_impl.cc',codec,'stream 1 closed: 2')
class GrpcStreamControls(unittest.TestCase):
 def test_exact_stream_closed_positive(self):
  result=observe(fixture(),'/own');self.assertTrue(result['verified']);self.assertEqual(result['numeric_actual_close_code'],2);self.assertIsNone(result['unary_authorization_grpc_end'])
 def test_missing_ambiguous_and_wrong_scope_remain_unknown(self):
  raw=fixture();lines=raw.splitlines(True)
  variants=[raw.replace('stream 1 closed: 2','stream 2 closed: 2'),raw.replace('stream 1 closed: 2','close attempted'),raw.replace('sent reset code=2','not actually sent'),raw.replace('resetting pool request','attempting reset'),raw.replace('ExternalProcessor/Process','Other/Process'),raw.replace('Opening gRPC stream to external processor','no opening'),raw+next(x for x in lines if 'Opening gRPC' in x),raw+next(x for x in lines if 'stream_id: 1,' in x).replace('stream_id: 1,','stream_id: 5,')]
  for value in variants:
   with self.subTest(raw=value):self.assertFalse(observe(value,'/own')['verified']);self.assertIsNone(observe(value,'/own')['actual_stream_close'])
  self.assertFalse(observe(raw,'/other')['verified'])
if __name__=='__main__':unittest.main()
