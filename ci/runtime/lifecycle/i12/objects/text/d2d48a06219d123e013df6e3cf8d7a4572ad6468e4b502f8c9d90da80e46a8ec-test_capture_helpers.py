import ast
import os
from pathlib import Path
import tempfile
import unittest
import host_log_observations as logs
ROOT=Path(__file__).resolve().parent
class CaptureControls(unittest.TestCase):
 def test_exact_log_order_and_exclusive_refusal(self):
  tree=ast.parse((ROOT/'driver.py').read_text()); main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
  loop=next(n for n in main.body if isinstance(n,ast.For) and isinstance(n.iter,ast.List) and any(isinstance(x,ast.Constant) and x.value=='envoy-access.jsonl' for x in n.iter.elts))
  validate=next(n for n in main.body if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and n.value.args and isinstance(n.value.args[0],ast.Constant) and n.value.args[0].value=='envoy-config-validate')
  self.assertLess(loop.lineno,validate.lineno)
  module=ast.Module(body=[loop],type_ignores=[]);ast.fix_missing_locations(module);code=compile(module,'driver-log-block','exec')
  with tempfile.TemporaryDirectory(dir=ROOT) as directory:
   task=Path(directory);(task/'runtime').mkdir();scope={'TASK':task,'os':os};exec(code,scope)
   with (task/'runtime/envoy-access.jsonl').open('ab') as stream: stream.write(b'')
   with self.assertRaises(FileExistsError):exec(code,scope)
   (task/'runtime/native-lifecycle.jsonl').unlink();target=task/'untouched';target.write_bytes(b'unchanged');(task/'runtime/native-lifecycle.jsonl').symlink_to(target)
   with self.assertRaises(FileExistsError):exec(code,scope)
   self.assertEqual(target.read_bytes(),b'unchanged')
 def test_host_scope_positive_and_negative(self):
  prefix='[2026-10-14T12:00:00.123+0000] [1] [debug] [http] [conn_manager_impl.cc:1356] [Tags: "ConnectionId":"1","StreamId":"2"] '
  header=prefix+"request headers complete (end_stream=false):\n':path', '/case-a'\n"
  codec=prefix.replace('1356','1871')+'encoding headers via codec (end_stream=false)\n'
  value=logs.extract(header+codec,'/case-a');self.assertTrue(value['scope_verified']);self.assertEqual(len(value['codec_headers']),1)
  self.assertEqual(value['codec_headers'][0]['clock_interval']['quantization_ns'],1000000)
  self.assertFalse(logs.extract(header+codec,'/wrong')['scope_verified'])
  self.assertFalse(logs.extract(header+header+codec,'/case-a')['scope_verified'])
  self.assertFalse(logs.extract(codec,'/case-a')['scope_verified'])
  self.assertEqual(logs.extract(header,'/case-a')['codec_headers'],[])
 def test_extproc_backend_exact_parser_controls(self):
  import email.message
  import io
  tree=ast.parse((ROOT/'backend-extproc.py').read_text());fun=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='read_framed_body');module=ast.Module(body=[fun],type_ignores=[]);ast.fix_missing_locations(module);scope={};exec(compile(module,'actual-backend-parser','exec'),scope);parse=scope['read_framed_body']
  def headers(cl=(),te=()):
   h=email.message.Message()
   for value in cl:h['Content-Length']=value
   for value in te:h['Transfer-Encoding']=value
   return h
  for wire,h in [(b'abc',headers(['3'])),(b'3\r\nabc\r\n0\r\n\r\n',headers(te=['chunked'])),(b'1\r\na\r\n2\r\nbc\r\n0\r\n\r\n',headers(te=['chunked']))]:
   with self.subTest(wire=wire):self.assertEqual(parse(io.BytesIO(wire),h)[0],b'abc')
  for wire,h in [(b'',headers(['3'],['chunked'])),(b'',headers(['3','3'])),(b'zz\r\n',headers(te=['chunked'])),(b'3\r\nab',headers(te=['chunked'])),(b'401\r\n',headers(te=['chunked'])),(b'0\r\nx:',headers(te=['chunked'])),(b'ab',headers(['3'])),(b'',headers())]:
   with self.subTest(wire=wire):
    with self.assertRaises(ValueError):parse(io.BytesIO(wire),h)
if __name__=='__main__':unittest.main()
