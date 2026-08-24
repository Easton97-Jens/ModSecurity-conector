"""Focused source contracts for Common event output hardening.

The test is deliberately network- and runtime-independent.  It verifies that
the event writer keeps its JSONL and filesystem boundary controls in the
shared implementation without emitting request or response body payloads.
"""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVENT_SOURCE = ROOT / "common" / "src" / "event.c"
RUNTIME_SOURCE = ROOT / "common" / "runtime" / "msconnector_runtime.c"
EVENT_HEADER = ROOT / "common" / "include" / "msconnector" / "event.h"
INTEGRITY_HEADER = ROOT / "common" / "include" / "msconnector" / "integrity_event.h"


class EventRuntimeSecurityContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.event_source = EVENT_SOURCE.read_text(encoding="utf-8")
        cls.runtime_source = RUNTIME_SOURCE.read_text(encoding="utf-8")

    def test_protocol_metadata_is_json_escaped_and_null_safe(self) -> None:
        protocol_writer = self.event_source.split(
            "static int append_protocol_string(", 1
        )[1].split("static int append_protocol_bool(", 1)[0]
        metadata_probe = self.event_source.split(
            "static int protocol_metadata_present(", 1
        )[1].split("static int append_protocol_metadata(", 1)[0]

        self.assertIn("msconnector_json_escape(", protocol_writer)
        self.assertLess(
            protocol_writer.index("msconnector_json_escape("),
            protocol_writer.index("snprintf(")
        )
        self.assertIn("values[index] != NULL", metadata_probe)

    def test_event_file_open_is_no_follow_regular_and_private(self) -> None:
        secure_open = self.runtime_source.split(
            "static FILE *open_event_file_secure(", 1
        )[1].split("static int string_is_empty", 1)[0]

        for token in ("O_APPEND", "O_CREAT", "O_NOFOLLOW", "S_ISREG", "0600", "fchmod"):
            self.assertIn(token, secure_open)
        self.assertIn("open_event_file_secure(runtime->config.phase4_log_path)", self.runtime_source)
        self.assertNotIn('fopen(runtime->config.phase4_log_path, "a")', self.runtime_source)
        self.assertIn("errno = ENOTSUP", secure_open)
        self.assertIn("(void)path;", secure_open)
        self.assertNotIn("_open(", secure_open)

    def test_integrity_fields_document_non_cryptographic_correlation_only(self) -> None:
        event_header = EVENT_HEADER.read_text(encoding="utf-8")
        integrity_header = INTEGRITY_HEADER.read_text(encoding="utf-8")

        self.assertIn("not\n     * cryptographic signatures", event_header)
        self.assertIn("do not authenticate event records", integrity_header)
        self.assertIn("tamper-resistant audit", integrity_header)


if __name__ == "__main__":
    unittest.main()
