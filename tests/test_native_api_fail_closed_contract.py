"""Regression contracts for libmodsecurity's boolean C API result handling."""

from pathlib import Path
import re
import unittest

from tests.c_source_contract import function_definition, matching_delimiter


ROOT = Path(__file__).resolve().parents[1]
COMMON_RUNTIME = (ROOT / "common" / "runtime" / "msconnector_runtime.c").read_text(encoding="utf-8")
HAPROXY = (ROOT / "connectors" / "haproxy" / "src" / "haproxy_modsecurity_binding.c").read_text(encoding="utf-8")
APACHE_FILTERS = (ROOT / "connectors" / "apache" / "src" / "msc_filters.c").read_text(encoding="utf-8")


NATIVE_RESULT = (ROOT / "common" / "include" / "msconnector" / "native_result.h").read_text(encoding="utf-8")


def requires_success(source: str, operation: str) -> bool:
    """Check every call, with append partial distinct from phase success."""
    calls = list(re.finditer(rf"{re.escape(operation)}\s*\(", source))
    if not calls:
        return False
    helper = ("msconnector_native_body_append_can_continue" if
        "append" in operation else "msconnector_native_phase_succeeded")
    for call in calls:
        opening = source.index("(", call.start())
        closing = matching_delimiter(source, opening, "(", ")")
        prefix = source[max(0, call.start() - 100):call.start()]
        suffix = source[closing + 1:]
        delegated = re.search(rf"!{helper}\s*\(\s*$", prefix) is not None
        direct = re.match(r"\s*!=\s*1\b", suffix) is not None
        if "append" in operation:
            if not delegated:
                return False
        elif not (delegated or direct):
            return False
    return True


class NativeAPIFailClosedContractTests(unittest.TestCase):
    def test_native_helpers_keep_phase_success_and_append_partial_distinct(self) -> None:
        phase = function_definition(NATIVE_RESULT, "msconnector_native_phase_succeeded")
        self.assertRegex(phase, r"return\s+result\s*==\s*1\s*;")
        classifier = function_definition(NATIVE_RESULT, "msconnector_native_body_result_classify")
        self.assertRegex(classifier, r"if\s*\(result == 0\)\s*\{\s*return MSCONNECTOR_NATIVE_BODY_PARTIAL;")
        self.assertRegex(classifier, r"if\s*\(result == 1\)\s*\{\s*return MSCONNECTOR_NATIVE_BODY_SUCCESS;")
        self.assertTrue(classifier.rstrip().endswith("return MSCONNECTOR_NATIVE_BODY_FAILURE;\n}"))
        append = function_definition(NATIVE_RESULT, "msconnector_native_body_append_can_continue")
        self.assertRegex(append, r"return msconnector_native_body_result_classify\(result\) !=\s*MSCONNECTOR_NATIVE_BODY_FAILURE;")

    def test_call_contract_rejects_unchecked_or_wrong_classifier_calls(self) -> None:
        operation = "msc_process_request_body"
        checked = f"if (!msconnector_native_phase_succeeded({operation}(tx))) return 0;"
        self.assertTrue(requires_success(checked, operation))
        self.assertFalse(requires_success(checked + f" {operation}(tx);", operation))
        self.assertFalse(requires_success(checked.replace("phase_succeeded", "body_append_can_continue"), operation))
        append = "msc_append_request_body"
        self.assertFalse(requires_success(f"if ({append}(tx, data, size) != 1) return 0;", append))
        self.assertFalse(requires_success(f"if (!msconnector_native_phase_succeeded({append}(tx, data, size))) return 0;", append))

    def test_common_runtime_rejects_every_boolean_native_failure(self) -> None:
        for operation in ("msc_process_connection", "msc_process_uri", "msc_set_request_hostname", "msc_add_n_request_header", "msc_process_request_headers", "msc_append_request_body", "msc_process_request_body", "msc_add_n_response_header", "msc_process_response_headers", "msc_append_response_body", "msc_process_response_body"):
            with self.subTest(operation=operation):
                self.assertTrue(requires_success(COMMON_RUNTIME, operation))

    def test_haproxy_rejects_failures_with_append_partial_and_exact_eos(self) -> None:
        for operation in ("msc_process_connection", "msc_add_request_header", "msc_process_request_headers", "msc_append_request_body", "msc_process_request_body", "msc_process_uri", "msc_add_response_header", "msc_process_response_headers"):
            with self.subTest(operation=operation):
                self.assertTrue(requires_success(HAPROXY, operation))
        self.assertTrue(requires_success(HAPROXY, "phase->append_body"))
        self.assertTrue(requires_success(HAPROXY, "phase->finish_body"))

    def test_apache_response_mapping_and_body_paths_classify_failures(self) -> None:
        for operation in ("msc_process_request_body", "msc_append_request_body", "msc_add_response_header", "msc_process_response_headers", "msc_append_response_body", "msc_process_response_body"):
            with self.subTest(operation=operation):
                self.assertTrue(requires_success(APACHE_FILTERS, operation))


if __name__ == "__main__":
    unittest.main()
