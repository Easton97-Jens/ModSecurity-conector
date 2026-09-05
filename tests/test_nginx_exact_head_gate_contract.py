import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class NginxExactHeadGateContractTest(unittest.TestCase):
    def test_workflow_pins_nginx_and_runs_gate(self):
        workflow = (ROOT / ".github/workflows/test-nginx-exact-head.yml").read_text()
        self.assertIn("ref: ${{ github.event.pull_request.head.sha || github.sha }}", workflow)
        self.assertIn("actual=\"$(git rev-parse HEAD)\"", workflow)
        self.assertIn('test "$actual" = "$EXPECTED_PARENT_SHA"', workflow)
        self.assertIn("NGINX_SOURCE_MODE: github-release", workflow)
        self.assertIn('ALLOW_RUNTIME_BUILDS: "1"', workflow)
        self.assertIn('ALLOW_RUNTIME_DOWNLOADS: "1"', workflow)
        self.assertIn("RUNTIME_COMPONENT_TARGET: nginx", workflow)
        self.assertIn("NGINX_SOURCE_GIT_REF: release-1.31.4", workflow)
        self.assertIn("NGINX_SHA256: e6f20b644a17a643f059ae6467a1971fe2811587d025e071068753a1f1e3b3c3", workflow)
        for override in (
            "MRTS_NATIVE_NGINX_BIN",
            "MRTS_NATIVE_NGINX_MODULE_DIR",
            "MRTS_NATIVE_NGINX_MODULE_FILE",
            "MRTS_NATIVE_NGINX_MODSECURITY_LIB_DIR",
            "NGINX_MRTS_MODSECURITY_LIB_DIR",
            "NGINX_BINARY",
            "NGINX_MODULE",
            "NGINX_PREFIX",
            "NGINX_BUILD_DIR",
        ):
            self.assertIn(f"-u {override}", workflow)
            self.assertEqual(workflow.count(f"-u {override}"), 2)
        self.assertIn("run_exact_head_use_error_log.sh", workflow)
        self.assertIn("Print bounded NGINX provisioning failure diagnostics", workflow)
        self.assertIn("if: failure()", workflow)
        diagnostic_step = workflow.split(
            "      - name: Print bounded NGINX provisioning failure diagnostics", 1
        )[1].split("      - name: Run isolated modsecurity_use_error_log on/off cells", 1)[0]
        self.assertIn("run_root='${{ runner.temp }}/ModSecurity-conector-nginx-exact-head'", diagnostic_step)
        self.assertIn("/usr/bin/env -i /usr/bin/python3 -I", diagnostic_step)
        self.assertIn("ci/provisioning/components/nginx_exact_head_diagnostics.py", diagnostic_step)
        self.assertNotIn("VERIFIED_RUN_ROOT", diagnostic_step)
        self.assertNotIn("RUNTIME_REPORT_OUTPUT_ROOT", diagnostic_step)

    def test_gate_has_two_real_runtime_cells_and_fail_closed_markers(self):
        script = (ROOT / "connectors/nginx/harness/run_exact_head_use_error_log.sh").read_text()
        self.assertIn("for mode in on off", script)
        self.assertIn("NGINX_USE_ERROR_LOG=\"$mode\"", script)
        self.assertIn("MODSECURITY_RULE_PREAMBLE_FILE=\"$RULE_PREAMBLE\"", script)
        self.assertIn("grep -Eq '949110'", script)
        self.assertNotIn("Access denied|ModSecurity", script)
        self.assertIn("intervention marker leaked with error-log off", script)

    def test_existing_template_renders_directive(self):
        template = (ROOT / "connectors/nginx/harness/nginx_smoke.conf").read_text()
        harness = (ROOT / "connectors/nginx/harness/run_nginx_smoke.sh").read_text()
        self.assertIn("@@NGINX_USE_ERROR_LOG_DIRECTIVE@@", template)
        self.assertIn("modsecurity_use_error_log off;", harness)


if __name__ == "__main__":
    unittest.main()
