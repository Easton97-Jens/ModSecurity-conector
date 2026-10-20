"""Backend fixture wire regressions; these are not Apache lifecycle evidence."""
import base64
import hashlib
import importlib.util
import io
from pathlib import Path
import unittest

SOURCE = Path(__file__).resolve().parents[1] / 'ci/runtime/lifecycle/apache-i12/acceptance/backend.py'
SPEC = importlib.util.spec_from_file_location('apache_backend_fixture_test', SOURCE)
BACKEND = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BACKEND)


def blob(data):
    return {'data': base64.b64encode(data).decode(), 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest()}


class BackendWireTests(unittest.TestCase):
    def test_chunked_wire_retains_chunk_boundaries_and_one_terminator(self):
        class Handler:
            wfile = io.BytesIO()

        selected = {'body': blob(b'onetwo'), 'chunks': [blob(b'one'), blob(b'two')]}
        chunks, payload = BACKEND.response_chunks(selected)
        events = []
        handler = Handler()
        BACKEND.write_response_body(handler, selected, chunks, True, 'principal', Path('.'), events.append)
        self.assertEqual(b'3\r\none\r\n3\r\ntwo\r\n0\r\n\r\n', handler.wfile.getvalue())
        self.assertEqual(b'onetwo', payload)
        self.assertEqual([0, 1], [row['chunk_index'] for row in events])
        self.assertEqual(['principal', 'principal'], [row['request_id'] for row in events])

    def test_mismatched_declared_body_is_rejected_before_wire_write(self):
        selected = {'body': blob(b'one'), 'chunks': [blob(b'two')]}
        with self.assertRaisesRegex(ValueError, 'chunks do not equal'):
            BACKEND.response_chunks(selected)

    def test_empty_body_keeps_no_data_chunks(self):
        self.assertEqual(([], b''), BACKEND.response_chunks({'body': blob(b'')}))
        self.assertTrue(BACKEND.valid_token('principal_1-A'))
        for token in ('', 'a' * 257, 'a b', 'ä', 'a\r\nb'):
            self.assertFalse(BACKEND.valid_token(token))

    def test_backend_rejects_nonprivate_port(self):
        self.assertEqual(BACKEND.private_loopback_port('18123'), 18123)
        self.assertEqual(BACKEND.private_loopback_port(18123), 18123)
        for value in (443, '443', True, '18123 ', '١٨١٢٣', object()):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, 'private loopback port'):
                BACKEND.private_loopback_port(value)


if __name__ == '__main__':
    unittest.main()
