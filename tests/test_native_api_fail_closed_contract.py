"""Guard operation-specific native results and every actual caller."""

from pathlib import Path
import re
import os
import shutil
import subprocess
import tempfile
import unittest
from tests.c_source_contract import function_definition


ROOT = Path(__file__).resolve().parents[1]
COMMON_RUNTIME = (ROOT / "common" / "runtime" / "msconnector_runtime.c").read_text(encoding="utf-8")
HAPROXY = (ROOT / "connectors" / "haproxy" / "src" / "haproxy_modsecurity_binding.c").read_text(encoding="utf-8")
APACHE_FILTERS = (ROOT / "connectors" / "apache" / "src" / "msc_filters.c").read_text(encoding="utf-8")


def requires_success(source: str, operation: str) -> bool:
    source = re.sub(r"/\*.*?\*/|//[^\n]*", "", source, flags=re.DOTALL)
    if "append" in operation:
        return re.search(rf"!msconnector_native_body_append_can_continue\(\s*{re.escape(operation)}\(", source) is not None
    return (re.search(rf"{re.escape(operation)}\([^;]*?\)\s*!=\s*1", source, re.DOTALL) is not None or
            re.search(rf"!msconnector_native_phase_succeeded\(\s*{re.escape(operation)}\(", source) is not None)


class NativeAPIFailClosedContractTests(unittest.TestCase):
    def test_common_runtime_checks_each_operation_specific_result(self) -> None:
        for operation in ("msc_process_connection", "msc_process_uri", "msc_set_request_hostname", "msc_add_n_request_header", "msc_process_request_headers", "msc_append_request_body", "msc_process_request_body", "msc_add_n_response_header", "msc_process_response_headers", "msc_append_response_body", "msc_process_response_body"):
            with self.subTest(operation=operation):
                self.assertTrue(requires_success(COMMON_RUNTIME, operation))

    def test_haproxy_checks_legacy_and_streaming_operation_results(self) -> None:
        for operation in ("msc_process_connection", "msc_add_request_header", "msc_process_request_headers", "msc_append_request_body", "msc_process_request_body", "msc_process_uri", "msc_add_response_header", "msc_process_response_headers"):
            with self.subTest(operation=operation):
                self.assertTrue(requires_success(HAPROXY, operation))
        self.assertTrue(requires_success(function_definition(HAPROXY, "append_body_chunk"), "phase->append_body"))
        self.assertTrue(requires_success(function_definition(HAPROXY, "finish_body"), "phase->finish_body"))
        for function, append, finish in (("request_body_phase", "msc_append_request_body", "msc_process_request_body"),
                                         ("response_body_phase", "msc_append_response_body", "msc_process_response_body")):
            route = function_definition(HAPROXY, function)
            self.assertIn(append + ", " + finish, route)

    def test_apache_response_mapping_and_body_paths_check_exact_results(self) -> None:
        for operation in ("msc_process_request_body", "msc_append_request_body", "msc_add_response_header", "msc_process_response_headers", "msc_append_response_body", "msc_process_response_body"):
            with self.subTest(operation=operation):
                self.assertTrue(requires_success(APACHE_FILTERS, operation))

    def test_guard_requires_negative_operation_specific_predicate(self) -> None:
        for operation in ("msc_append_request_body", "msc_process_request_body"):
            helper = "msconnector_native_body_append_can_continue" if "append" in operation else "msconnector_native_phase_succeeded"
            original = f"if (!{helper}({operation}(tx))) return 0;"
            self.assertTrue(requires_success(original, operation))
            self.assertFalse(requires_success(original.replace("!" + helper, helper), operation))
            self.assertFalse(requires_success(original.replace(helper, "unchecked_result"), operation))
            self.assertFalse(requires_success("/* " + original + " */", operation))
        self.assertFalse(requires_success("if (msc_append_request_body(tx) != 1) return 0;", "msc_append_request_body"))
        self.assertFalse(requires_success("if (!msconnector_native_body_append_can_continue(msc_process_request_body(tx))) return 0;", "msc_process_request_body"))

    def test_real_native_predicates_reject_unknown_results_and_preserve_partial(self) -> None:
        compiler = shutil.which("cc")
        self.assertIsNotNone(compiler)
        with tempfile.TemporaryDirectory(prefix="native-results-", dir=os.environ.get("TMPDIR", "/var/tmp/codex/ModSecurity-conector")) as directory:
            fixture = Path(directory) / "results.c"
            binary = Path(directory) / "results"
            fixture.write_text('#include "msconnector/native_result.h"\nint main(void) { int values[]={-2,-1,0,1,2,17}; for(unsigned i=0;i<6;i++){int r=values[i]; if(msconnector_native_phase_succeeded(r)!=(r==1))return 1; if(msconnector_native_body_append_can_continue(r)!=(r==0||r==1))return 2;} return 0;}\n')
            compiled = subprocess.run([compiler, "-std=c17", "-Wall", "-Wextra", "-Werror", "-I" + str(ROOT / "common/include"), str(fixture), "-o", str(binary)], capture_output=True, text=True)
            self.assertEqual(compiled.returncode, 0, compiled.stderr)
            executed = subprocess.run([str(binary)], capture_output=True, text=True)
            self.assertEqual(executed.returncode, 0, executed.stderr)


if __name__ == "__main__":
    unittest.main()
