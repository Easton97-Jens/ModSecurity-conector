"""The I12 wire observer must reject incomplete evidence instead of guessing."""
import importlib.util
from pathlib import Path
import struct
import unittest
from unittest import mock


PATH = Path(__file__).resolve().parents[1] / "connectors/haproxy/harness/i12_spop_wire.py"
SPEC = importlib.util.spec_from_file_location("i12_spop_wire", PATH)
WIRE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(WIRE)


def envelope(payload, kind=3):
    body = bytes([kind]) + b"\x00\x00\x00\x01\x01\x01" + payload
    return struct.pack("!I", len(body)) + body


class HaproxyI12SpopWireTests(unittest.TestCase):
    def test_supplemental_identity_cannot_transfer_a_legacy_or_mistyped_original_id(self):
        spec = importlib.util.spec_from_file_location("i12_spop_host", PATH.with_name("i12_spop_host.py"))
        host = importlib.util.module_from_spec(spec)
        with mock.patch.dict("sys.modules", {"i12_spop_wire": WIRE}):
            spec.loader.exec_module(host)
        for value in ("NEED-marker-at-payload-end", "NEED-request-marker-at-payload-end"):
            identity = host.case_identity({"case": "p2-deny", "case_id": value})
            self.assertEqual(identity["diagnostic_id"], "DIAG::haproxy-spop-request::p2-deny")
            self.assertIsNone(identity["original_id"])
            self.assertFalse(identity["original_obligation_eligible"])

    def test_real_signed_haproxy_body_length_and_version_are_preserved(self):
        # HAProxy's integer sample uses INT64, not string or unsigned coercion.
        payload = (b"\x0dcheck-request\x03\x04body\x09\x04test"
                   b"\x08body_len\x04\x04\x0chttp_version\x08\x031.1")
        decoded = WIRE.decode_frame(envelope(payload))
        arguments = decoded["messages"][0]["arguments"]
        self.assertEqual(arguments, [{"name": "body", "tag": 9, "value": "74657374"},
                                    {"name": "body_len", "tag": 4, "value": 4},
                                    {"name": "http_version", "tag": 8, "value": "1.1"}])

    def test_null_sample_is_not_reported_as_empty_binary_sample(self):
        decoded = WIRE.decode_frame(envelope(b"\x0dcheck-request\x01\x04body\x00"))
        self.assertEqual(decoded["messages"][0]["arguments"][0],
                         {"name": "body", "tag": 0, "value": None})

    def test_ack_boolean_status_and_error_remain_independent_fields(self):
        payload = (b"\x01\x03\x02\x07blocked\x11"
                   b"\x01\x03\x02\x06status\x03\xf7\x10"
                   b"\x01\x03\x02\x05error\x08\x07invalid")
        actions = WIRE.decode_frame(envelope(payload, 103))["actions"]
        self.assertEqual([value["value"] for value in actions], [True, 503, "invalid"])

    def test_duplicate_argument_bytes_are_preserved_without_last_value_wins(self):
        decoded = WIRE.decode_frame(envelope(b"\x0dcheck-request\x02\x08body_len\x03\x00\x08body_len\x03\x01"))
        self.assertEqual(len(decoded["messages"][0]["arguments"]), 2)

    def test_every_truncated_prefix_of_complete_frame_is_rejected(self):
        raw = envelope(b"\x0dcheck-request\x01\x08body_len\x04\x00")
        for size in range(len(raw)):
            with self.subTest(size=size), self.assertRaises(WIRE.InvalidFrame):
                WIRE.decode_frame(raw[:size])

    def test_supported_envelope_cannot_hide_truncated_or_unknown_typed_value(self):
        for payload in (b"\x0dcheck-request\x01\x04body\x09\x04te",
                        b"\x0dcheck-request\x01\x04body\x0f"):
            with self.subTest(payload=payload), self.assertRaises(WIRE.InvalidFrame):
                WIRE.decode_frame(envelope(payload))

    def test_frame_size_and_integer_budgets_fail_before_unbounded_decode(self):
        with self.assertRaises(WIRE.InvalidFrame):
            WIRE.decode_frame(struct.pack("!I", WIRE.MAX_FRAME + 1))
        with self.assertRaises(WIRE.InvalidFrame):
            WIRE.Reader(b"\xff" * 12).uint()


if __name__ == "__main__":
    unittest.main()
