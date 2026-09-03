#!/usr/bin/env python3
"""Source contract tests for the HAProxy libmodsecurity phase binding."""

from pathlib import Path
import re
import unittest


SOURCE = (
    Path(__file__).resolve().parents[1]
    / "connectors/haproxy/src/haproxy_modsecurity_binding.c"
).read_text(encoding="utf-8")


class HaproxyBindingPhaseContractTests(unittest.TestCase):
    def test_direct_request_phase_calls_require_exact_success(self):
        calls = (
            "msc_process_connection",
            "msc_process_uri",
            "msc_add_request_header",
            "msc_process_request_headers",
            "msc_append_request_body",
            "msc_process_request_body",
        )
        for call in calls:
            with self.subTest(call=call):
                self.assertRegex(
                    SOURCE,
                    re.compile(rf"{call}\(.*?\)\s*!=\s*1", re.DOTALL),
                )

    def test_direct_response_phase_calls_require_exact_success(self):
        calls = (
            "msc_add_response_header",
            "msc_process_response_headers",
        )
        for call in calls:
            with self.subTest(call=call):
                self.assertRegex(
                    SOURCE,
                    re.compile(rf"{call}\(.*?\)\s*!=\s*1", re.DOTALL),
                )

    def test_shared_body_helpers_require_exact_success(self):
        append_helper = re.search(
            r"static int append_body_chunk\(.*?^}\n\nstatic int finish_body",
            SOURCE,
            re.DOTALL | re.MULTILINE,
        )
        finish_helper = re.search(
            r"static int finish_body\(.*?^}\n\nstatic int load_rules_file",
            SOURCE,
            re.DOTALL | re.MULTILINE,
        )
        self.assertIsNotNone(append_helper)
        self.assertIsNotNone(finish_helper)
        self.assertRegex(
            append_helper.group(0),
            re.compile(r"append_body\(.*?\)\s*!=\s*1", re.DOTALL),
        )
        self.assertRegex(
            finish_helper.group(0),
            re.compile(r"finish_body\(.*?\)\s*!=\s*1", re.DOTALL),
        )

    def test_rule_loading_keeps_its_distinct_negative_error_contract(self):
        rules = re.search(
            r"static int load_rules_file\(.*?^}\n\nstatic int load_rules_text",
            SOURCE,
            re.DOTALL | re.MULTILINE,
        )
        self.assertIsNotNone(rules)
        self.assertRegex(rules.group(0), r"msc_rules_add_file\(")
        self.assertRegex(rules.group(0), r"if \(rc\s*<\s*0\)")

    def test_no_legacy_negative_phase_checks_remain(self):
        phase_calls = (
            "msc_process_connection",
            "msc_process_uri",
            "msc_add_request_header",
            "msc_process_request_headers",
            "msc_append_request_body",
            "msc_process_request_body",
            "msc_add_response_header",
            "msc_process_response_headers",
        )
        for call in phase_calls:
            with self.subTest(call=call):
                self.assertNotRegex(
                    SOURCE,
                    re.compile(rf"{call}\(.*?\)\s*<\s*0", re.DOTALL),
                )

    def test_body_chunks_are_bounded_before_the_libmodsecurity_sink(self):
        helper = re.search(
            r"static int append_body_chunk\(.*?^}\n\nstatic int finish_body",
            SOURCE,
            re.DOTALL | re.MULTILINE,
        )
        self.assertIsNotNone(helper)
        body = helper.group(0)
        self.assertIn("body_limit == 0U", body)
        self.assertIn("(size_t)body_len > body_limit - *phase->body_bytes_seen", body)
        self.assertLess(
            body.index("(size_t)body_len > body_limit - *phase->body_bytes_seen"),
            body.index("phase->append_body("),
        )

    def test_request_and_response_copy_effective_common_body_limits(self):
        self.assertIn(
            "transaction->engine->common_config.request_body_limit", SOURCE
        )
        self.assertIn(
            "transaction->engine->common_config.response_body_limit", SOURCE
        )


if __name__ == "__main__":
    unittest.main()
