"""Compile unchanged productive HTX caller bodies with controlled host/native seams.

This checks host API calls, never client transport effects. Common policy code
is linked unchanged. Mutation copies live outside the source checkout.
"""
from pathlib import Path
import os
import subprocess
import tempfile
import unittest
from tests.c_source_contract import function_definition

ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "connectors/haproxy/htx-overlay/haproxy_modsecurity_htx_filter.c"
FUNCTIONS = (
    "companion_cancel_cause_from_error", "companion_cancel_and_close", "abort_context", "finish_context", "apply_precommit_deny",
    "fail_closed_precommit", "fail_closed_postcommit", "fail_closed_request_phase",
    "companion_result_is_forwardable", "companion_record_precommit_outcome", "companion_record_terminal_outcome",
    "companion_open_and_claim", "companion_commit", "process_companion_response_headers", "send_companion_response_chunk", "finish_companion_response",
    "handle_response_headers", "filter_request_payload", "filter_response_payload",
    "filter_http_payload", "finish_request", "finish_response", "filter_http_end",
    "filter_http_headers",
)

class HAProxyI10HostCallers(unittest.TestCase):
    def compile_and_run(self, source):
        # Extract declarations and complete productive functions without changing
        # their bodies. Unrelated HTX parser/registration APIs are outside this seam.
        structs = source[source.index("struct haproxy_modsecurity_htx_filter_config {"):
                         source.index("typedef int (*haproxy_modsecurity_htx_append_body_chunk)")]
        bodies = []
        for suffix in FUNCTIONS:
            name = "haproxy_modsecurity_htx_" + suffix
            body = function_definition(source, name)
            # Parser returns name line; recover return type on preceding line.
            start = source.index(body)
            previous = source[source.rfind("\n", 0, start - 1) + 1:start].strip()
            bodies.append(previous + "\n" + body if not body.startswith("static ") else body)
        fixture = (ROOT / "tests/haproxy_i10_host_caller_test.c").read_text()
        c_source = fixture.replace("/* PRODUCT_STRUCTS */", structs).replace(
            "/* PRODUCT_FUNCTIONS */", "\n\n".join(bodies))
        temp_root = Path(os.environ.get("TMPDIR", "/var/tmp/codex/ModSecurity-conector/tmp"))
        temp_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="haproxy-i10-", dir=temp_root) as directory:
            temp = Path(directory)
            harness = temp / "caller.c"
            harness.write_text(c_source)
            binary = temp / "caller"
            sources = ["late_intervention.c", "decision_action.c", "block_statuses.c",
                       "http_status.c", "error.c", "decision.c", "intervention.c", "event.c", "json_escape.c", "status.c"]
            command = ["cc", "-std=c17", "-Wall", "-Wextra", "-Werror", "-ffunction-sections", "-Wl,--gc-sections",
                       "-I", str(ROOT / "common/include"),
                       "-I", str(ROOT / "common/runtime"),
                       "-I", str(ROOT / "connectors/haproxy/src"),
                       str(harness), *(str(ROOT / "common/src" / s) for s in sources),
                       "-o", str(binary)]
            compiled = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(compiled.returncode, 0, compiled.stdout + compiled.stderr)
            return subprocess.run([str(binary)], capture_output=True, text=True, cwd=temp, timeout=30)

    def test_productive_host_callers_mode_commit_reentry_matrix(self):
        result = self.compile_and_run(OVERLAY.read_text())
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_negative_controls_detect_actual_boundary_regressions(self):
        source = OVERLAY.read_text()
        mutations = {
            "invalid-nested-success-ignored": ("|| result.success != 1", "|| result.success == 123"),
            "invalid-result-success-accepted": ("result->success == 1 &&", "result->success != 0 &&"),
            "invalid-release-accepted": ("if (ok != 1) {\n        haproxy_modsecurity_htx_companion_cancel_and_close(ctx, &error);\n        return 0;", "if (ok == 0) {\n        haproxy_modsecurity_htx_companion_cancel_and_close(ctx, &error);\n        return 0;"),
            "invalid-open-accepted": ("if (ok == 1) {\n        ok = msconnector_response_companion_client_claim(", "if (ok != 0) {\n        ok = msconnector_response_companion_client_claim("),
            "invalid-claim-accepted": ("return ok == 1;\n}\n\nstatic int haproxy_modsecurity_htx_companion_commit", "return ok != 0;\n}\n\nstatic int haproxy_modsecurity_htx_companion_commit"),
            "ignored-cleanup-ack": ("return ok == 1 && cleanup_ok == 1;", "return ok == 1 || cleanup_ok == 1;"),
            "duplicate-host-action": ("if (ctx->lifecycle.host_failure_applied)", "if (0)"),
            "terminal-request-success": ("if (ctx->lifecycle.fail_closed) {\n        return -1;", "if (0) {\n        return -1;"),
            "ignored-commit": ("ctx->transaction, 1, 0) != 0", "ctx->transaction, 1, 0) == 123"),
            "invalid-common-eos-success": ("&ctx->companion.client, &result, &error) != 1", "&ctx->companion.client, &result, &error) == 0"),
            "duplicate-response-reply": ("if (ctx->response.headers_committed) {", "if (0) {"),
            "ignored-outcome-ack": ("if (!haproxy_modsecurity_htx_companion_record_precommit_outcome(ctx,", "if (0 && !haproxy_modsecurity_htx_companion_record_precommit_outcome(ctx,"),
            "ignored-terminal-finish": ("if (haproxy_modsecurity_htx_finish_context(ctx) != 0)", "if (haproxy_modsecurity_htx_finish_context(ctx) == 123)"),
            "false-abort-observation": ("if (connection_aborted) {", "if (connection_aborted && 0) {"),
        }
        for name, (old, new) in mutations.items():
            with self.subTest(mutation=name):
                self.assertIn(old, source)
                result = self.compile_and_run(source.replace(old, new))
                self.assertNotEqual(result.returncode, 0, name + " unexpectedly survived")

if __name__ == "__main__":
    unittest.main()
