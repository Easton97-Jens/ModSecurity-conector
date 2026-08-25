"""Source-level fail-closed contracts for Apache native request processing."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FILTERS = ROOT / "connectors/apache/src/msc_filters.c"
EVENT_JSONL = ROOT / "common/src/event_jsonl.c"


class ApacheNativeSecurityContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = FILTERS.read_text(encoding="utf-8")
        cls.event_jsonl = EVENT_JSONL.read_text(encoding="utf-8")

    def test_request_body_append_requires_exact_libmodsecurity_success(self) -> None:
        self.assertRegex(
            self.source,
            re.compile(
                r"msc_append_request_body\(msr->t,\s*"
                r"\(const unsigned char \*\)data, plan\.append_size\) != 1",
                re.DOTALL,
            ),
        )

    def test_final_request_body_processing_requires_exact_success(self) -> None:
        self.assertIn("if (msc_process_request_body(msr->t) != 1)", self.source)

    def test_response_header_append_failure_enters_precommit_terminal_path(self) -> None:
        self.assertRegex(
            self.source,
            re.compile(
                r"static int apache_add_response_headers.*?"
                r"if \(msc_add_response_header\(msr->t,.*?\) != 1\).*?"
                r"return 0;.*?"
                r"if \(!apache_add_response_headers\(msr, r->err_headers_out\) \|\|"
                r"\s*!apache_add_response_headers\(msr, r->headers_out\)\).*?"
                r"return apache_send_precommit_terminal_error\(msr, filter, brigade,\s*"
                r"HTTP_INTERNAL_SERVER_ERROR\);",
                re.DOTALL,
            ),
        )

    def test_response_content_type_append_failure_enters_precommit_terminal_path(self) -> None:
        self.assertRegex(
            self.source,
            re.compile(
                r"if \(msc_add_response_header\(msr->t,\s*"
                r"\(const unsigned char \*\)\"Content-Type\",\s*"
                r"\(const unsigned char \*\)content_type\) != 1\).*?"
                r"return apache_send_precommit_terminal_error\(msr, filter, brigade,\s*"
                r"HTTP_INTERNAL_SERVER_ERROR\);",
                re.DOTALL,
            ),
        )

    def test_event_path_walk_is_fail_closed_and_descriptor_backed(self) -> None:
        self.assertIn("msconnector_open_private_event_file(path, &fd)", self.source)
        self.assertIn("apr_os_file_put", self.source)
        self.assertIn("openat(directory_fd, component", self.event_jsonl)
        self.assertIn("O_DIRECTORY | O_NOFOLLOW", self.event_jsonl)
        self.assertIn("strcmp(component, \"..\") == 0", self.event_jsonl)
        self.assertIn("strcmp(component, \".\") == 0", self.event_jsonl)
        self.assertIn("!S_ISREG(file_status.st_mode)", self.event_jsonl)
        self.assertIn("file_status.st_uid != geteuid()", self.event_jsonl)
        self.assertIn("fchmod(fd, (mode_t)0600)", self.event_jsonl)

    def test_event_path_rejects_empty_double_and_trailing_components(self) -> None:
        self.assertIn("path[path_length - 1U] == '/'", self.event_jsonl)
        self.assertIn("component[0] == '\\0'", self.event_jsonl)
        self.assertIn("path[0] == '/' ? \"/\" : \".\"", self.event_jsonl)


if __name__ == "__main__":
    unittest.main()
