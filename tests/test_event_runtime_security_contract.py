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
EVENT_JSONL_SOURCE = ROOT / "common" / "src" / "event_jsonl.c"
RUNTIME_SOURCE = ROOT / "common" / "runtime" / "msconnector_runtime.c"
APACHE_SOURCE = ROOT / "connectors" / "apache" / "src" / "msc_filters.c"
EVENT_HEADER = ROOT / "common" / "include" / "msconnector" / "event.h"
INTEGRITY_HEADER = ROOT / "common" / "include" / "msconnector" / "integrity_event.h"


class EventRuntimeSecurityContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.event_source = EVENT_SOURCE.read_text(encoding="utf-8")
        cls.event_jsonl_source = EVENT_JSONL_SOURCE.read_text(encoding="utf-8")
        cls.runtime_source = RUNTIME_SOURCE.read_text(encoding="utf-8")
        cls.apache_source = APACHE_SOURCE.read_text(encoding="utf-8")

    def test_protocol_metadata_is_json_escaped_and_null_safe(self) -> None:
        escaping_writer = self.event_source.split(
            "static void escape_field(", 1
        )[1].split("/* Callers supply bounded JSON-escaped text", 1)[0]
        protocol_writer = self.event_source.split(
            "static int append_escaped_protocol_string(", 1
        )[1].split("static int append_protocol_bool(", 1)[0]
        metadata_probe = self.event_source.split(
            "static int protocol_metadata_present(", 1
        )[1].split("static int append_protocol_metadata(", 1)[0]

        self.assertIn("msconnector_json_escape_n(", escaping_writer)
        self.assertLess(
            self.event_source.index("escape_field(event->protocol.requested_protocol"),
            self.event_source.rindex("append_event_provenance(")
        )
        self.assertIn("value == NULL", protocol_writer)
        self.assertIn("values[index] != NULL", metadata_probe)

    def test_event_file_open_is_no_follow_regular_and_private(self) -> None:
        secure_open = self.event_jsonl_source.split(
            "int msconnector_open_private_event_file(", 1
        )[1]

        for token in (
            "O_APPEND",
            "O_CREAT",
            "O_NOFOLLOW",
            "O_DIRECTORY",
            "S_ISREG",
            "0600",
            "fchmod",
            "O_CLOEXEC",
            "FD_CLOEXEC",
        ):
            self.assertIn(token, secure_open)
        self.assertIn("msconnector_open_private_event_file(path, &fd)", self.runtime_source)
        self.assertNotIn('fopen(runtime->config.phase4_log_path, "a")', self.runtime_source)
        self.assertIn("errno = ENOTSUP", secure_open)
        self.assertIn("(void)path;", secure_open)
        self.assertNotIn("_open(", secure_open)

    def test_event_path_walk_rejects_ancestor_and_normalization_escapes(self) -> None:
        secure_open = self.event_jsonl_source.split(
            "int msconnector_open_private_event_file(", 1
        )[1]
        path_validation = self.runtime_source.split(
            "static int validate_runtime_event_path(", 1
        )[1].split("static int validate_runtime_config", 1)[0]

        for token in ("openat", "O_DIRECTORY", "O_NOFOLLOW", "directory_fd",
                      "next_directory_fd", "strcmp(component, \"..\")",
                      "strcmp(component, \".\")", "directory_status.st_uid",
                      "directory_status.st_mode", "S_IWGRP", "S_IWOTH",
                      "geteuid()", "file_status.st_uid"):
            self.assertIn(token, secure_open)
        for token in ("path[path_length - 1U] == '/'", "path[index] == '\\\\'",
                      "strstr(path, \"/./\")", "strncmp(path, \"./\", 2U)"):
            self.assertIn(token, path_validation)

    def test_apache_uses_the_common_private_descriptor_before_apr_ownership(self) -> None:
        opener = self.apache_source.split(
            "static apr_status_t apache_open_event_file(", 1
        )[1].split("/* Kept private", 1)[0]

        self.assertIn("msconnector_open_private_event_file(path, &fd)", opener)
        self.assertIn("apr_os_file_put", opener)
        self.assertIn("close(fd)", opener)

    def test_integrity_fields_document_non_cryptographic_correlation_only(self) -> None:
        event_header = EVENT_HEADER.read_text(encoding="utf-8")
        integrity_header = INTEGRITY_HEADER.read_text(encoding="utf-8")

        self.assertIn("not\n     * cryptographic signatures", event_header)
        self.assertIn("do not authenticate event records", integrity_header)
        self.assertIn("tamper-resistant audit", integrity_header)


if __name__ == "__main__":
    unittest.main()
