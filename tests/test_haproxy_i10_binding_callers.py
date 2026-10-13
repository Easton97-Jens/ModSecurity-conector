"""Full HAProxy binding compilation, real Common FSM, controlled native API."""
from pathlib import Path
import os
import re
import subprocess
import tempfile
import unittest
from tests import test_haproxy_libmodsecurity_compat as compat

ROOT = Path(__file__).resolve().parents[1]
BINDING = ROOT / "connectors/haproxy/src/haproxy_modsecurity_binding.c"

class HAProxyI10BindingCallers(unittest.TestCase):
    def run_caller(self, source, *, spop=False, runtime_source=None):
        temp_root = Path(os.environ.get("TMPDIR", "/var/tmp/codex/ModSecurity-conector/tmp"))
        temp_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="haproxy-i10-native-", dir=temp_root) as directory:
            temp = Path(directory)
            fixture = compat.HAProxyLibModSecurityCompatibilityTests()
            fixture.setUp()
            include, _ = fixture.write_fake_installation(temp / "native",
                optional_declaration=False, optional_symbol=False)
            native_path = temp / "native/fake_modsecurity.c"
            native = native_path.read_text()
            control = """
const char *native_failure;
int native_failure_result;
unsigned int native_calls, native_cleanups;
static int test_native(const char *name) {
    native_calls++;
    return native_failure != 0 && strcmp(name, native_failure) == 0 ? native_failure_result : 1;
}
"""
            native = native.replace("struct ModSecurity {", control + "\nstruct ModSecurity {")
            native = re.sub(r"(int msc_(?:process|append|add)[^\n]+)return 1;", r"\1return test_native(__func__);", native)
            native = native.replace("void msc_transaction_cleanup(Transaction *value) { (void)value; }",
                "void msc_transaction_cleanup(Transaction *value) { (void)value; native_cleanups++; }")
            if spop:
                header = include / "modsecurity/modsecurity.h"
                header.write_text(header.read_text() + "\nint msc_set_request_hostname(Transaction *, const unsigned char *);\nint msc_add_n_request_header(Transaction *, const unsigned char *, size_t, const unsigned char *, size_t);\nint msc_add_n_response_header(Transaction *, const unsigned char *, size_t, const unsigned char *, size_t);\n")
                native += "\nint msc_set_request_hostname(Transaction *t, const unsigned char *h) { (void)t; (void)h; return 1; }\nint msc_add_n_request_header(Transaction *t, const unsigned char *n, size_t nl, const unsigned char *v, size_t vl) { (void)nl; (void)vl; return msc_add_request_header(t,n,v); }\nint msc_add_n_response_header(Transaction *t, const unsigned char *n, size_t nl, const unsigned char *v, size_t vl) { (void)nl; (void)vl; return msc_add_response_header(t,n,v); }\n"
            native_path.write_text(native)
            # Copy only the owned binding TU for mutation, preserving its native includes.
            binding = temp / "binding.c"
            binding.write_text(source)
            harness = temp / "caller.c"
            fixture_name = "haproxy_i10_spop_caller_test.c" if spop else "haproxy_i10_binding_caller_test.c"
            fixture_source = (ROOT / "tests" / fixture_name).read_text()
            fixture_source = fixture_source.replace('"PRODUCT_BINDING"', '"' + str(binding) + '"')
            runtime_path = temp / "runtime.c"
            if spop:
                runtime_path.write_text(runtime_source if runtime_source is not None else
                    (ROOT / "connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c").read_text())
            fixture_source = fixture_source.replace('"PRODUCT_RUNTIME"', '"' + str(runtime_path) + '"')
            fixture_source = fixture_source.replace("PRODUCT_RULES", str(ROOT / "connectors/haproxy/harness/fixtures/modsecurity-binding-lifecycle.conf"))
            harness.write_text(fixture_source)
            makefile = (ROOT / "connectors/haproxy/Makefile").read_text()
            sdk = next(line.split(":=", 1)[1].split() for line in makefile.splitlines()
                       if line.startswith("COMMON_SDK_SRCS :="))
            sources = [ROOT / "common/src" / item.rsplit("/",1)[1] for item in sdk]
            if spop:
                sources.extend([binding, ROOT / "common/runtime/msconnector_runtime.c",
                    ROOT / "common/runtime/response_companion_transport.c",
                    ROOT / "common/runtime/response_companion_client.c",
                    ROOT / "connectors/haproxy/src/haproxy_spop_response_companion_backend.c"])
            command = ["cc", "-std=c17", "-D_POSIX_C_SOURCE=200809L", "-Wall", "-Wextra", "-Werror",
                       "-I", str(include), "-I", str(ROOT), "-I", str(ROOT / "common/include"),
                       "-I", str(ROOT / "connectors/haproxy/src"), "-I", str(ROOT / "common/runtime"),
                       "-pthread", "-ffunction-sections", "-Wl,--gc-sections", str(harness), str(native_path),
                       str(ROOT / "connectors/haproxy/src/haproxy_modsecurity_mapper.c"),
                       str(ROOT / "connectors/profile_registry.c"), *(str(s) for s in sources),
                       "-o", str(temp / "caller")]
            compiled = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(compiled.returncode, 0, compiled.stdout + compiled.stderr)
            return subprocess.run([str(temp / "caller")], capture_output=True, text=True, cwd=temp, timeout=30)

    def test_full_spop_request_caller_and_ack_fail_closed(self):
        result = self.run_caller(BINDING.read_text(), spop=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_spop_failure_reason_negative_control(self):
        source = (ROOT / "connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c").read_text()
        old = 'runtime_init_decision(decision, retained_phase, "deny", 503, retained_reason);'
        self.assertIn(old, source)
        result = self.run_caller(BINDING.read_text(), spop=True,
            runtime_source=source.replace(old,
                'runtime_init_decision(decision, retained_phase, "deny", 503, reason);'))
        self.assertNotEqual(result.returncode, 0, "borrowed failure reason regression survived")

    def test_spop_request_negative_controls(self):
        source = (ROOT / "connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c").read_text()
        mutations = {
            "native-failure-cause-lost": ("return MSCONNECTOR_ERROR_MODSECURITY_FAILURE;", "return MSCONNECTOR_ERROR_PHASE_SEQUENCE;"),
            "header-failure-cause-lost": ("case MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE: return MSCONNECTOR_ERROR_MODSECURITY_FAILURE;", "case MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE: return MSCONNECTOR_ERROR_PHASE_SEQUENCE;"),
            "technical-fail-open": ('runtime_init_decision(decision, retained_phase, "deny", 503, retained_reason);',
                'runtime_init_decision(decision, retained_phase, "pass", 200, retained_reason);'),
            "ignored-request-terminal-error": ('if (haproxy_modsecurity_transaction_finish_with_decision(transaction, decision) != 0)',
                'if (haproxy_modsecurity_transaction_finish_with_decision(transaction, decision) == 123)'),
            "detect-only-drops-failure-ack": ('return origin != SPOP_ACK_ENGINE_DECISION || mode_enforces(config);',
                'return origin == SPOP_ACK_ENGINE_DECISION || mode_enforces(config);'),
        }
        for name,(old,new) in mutations.items():
            with self.subTest(mutation=name):
                self.assertIn(old,source)
                result = self.run_caller(BINDING.read_text(), spop=True, runtime_source=source.replace(old,new))
                self.assertNotEqual(result.returncode,0,name + " survived")

    def test_real_binding_phase_commit_first_failure_and_reentry(self):
        result = self.run_caller(BINDING.read_text())
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_terminal_reentry_and_commit_negative_controls(self):
        source = BINDING.read_text()
        mutations = {
            "direct-commit-rejected": ("(transaction->response_companion.response_phases_require_companion &&\n                !transaction->response_companion.response_companion_claimed)",
                "!transaction->response_companion.response_companion_claimed"),
            "header-failure-not-terminal": ("MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE, \"msc_add_response_header failed\");",
                "MSCONNECTOR_TRANSACTION_ERROR_NONE, \"msc_add_response_header failed\");"),
        }
        for name, (old, new) in mutations.items():
            with self.subTest(mutation=name):
                self.assertIn(old,source)
                result = self.run_caller(source.replace(old,new))
                self.assertNotEqual(result.returncode,0,name + " survived")

if __name__ == "__main__":
    unittest.main()
