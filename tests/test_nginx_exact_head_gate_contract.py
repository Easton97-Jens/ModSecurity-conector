import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class NginxExactHeadGateContractTest(unittest.TestCase):
    def test_workflow_pins_nginx_and_runs_gate(self):
        workflow = (ROOT / ".github/workflows/test-nginx-exact-head.yml").read_text()
        self.assertIn("runs-on: ubuntu-24.04", workflow)
        self.assertIn("permissions:\n  contents: read", workflow)
        self.assertNotIn("pull_request_target", workflow)
        self.assertIn("ref: ${{ github.event.pull_request.head.sha || github.sha }}", workflow)
        self.assertIn("actual=\"$(git rev-parse --verify 'HEAD^{commit}')\"", workflow)
        self.assertNotIn("${{ runner.temp }}", workflow)
        self.assertIn('RUN_ROOT="${RUNNER_TEMP:?missing runner temporary root}/ModSecurity-conector-nginx-exact-head"', workflow)
        self.assertIn("^[0-9a-f]{40}$", workflow)
        self.assertIn('test "$actual" = "$EXPECTED_PARENT_SHA"', workflow)
        self.assertIn("Preflight root and isolated NGINX worker", workflow)
        self.assertIn("/usr/bin/sudo -n /usr/bin/id -u", workflow)
        self.assertIn("/usr/bin/sudo -n /usr/sbin/runuser -u", workflow)
        self.assertIn("--shell /usr/sbin/nologin", workflow)
        self.assertIn('test "$worker_uid" -ne 0', workflow)
        self.assertIn('test "$worker_gid" -ne 0', workflow)
        self.assertIn('test "$worker_gid" = "$worker_group_gid"', workflow)
        self.assertIn("NGINX_FUNCTIONAL_WORKER_USER: msconnector-nginx-functional", workflow)
        self.assertIn("NGINX_FUNCTIONAL_WORKER_GROUP: msconnector-nginx-functional", workflow)
        self.assertIn("/usr/bin/env -i", workflow)
        self.assertNotIn("sudo -E", workflow)
        self.assertNotIn("sudo sh", workflow)
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
            self.assertEqual(workflow.count(f"-u {override}"), 1)
        self.assertIn("run_github_hosted_functional_a.py", workflow)
        self.assertIn("NGINX_HOSTED_FUNCTIONAL_A=1", workflow)
        self.assertIn("with-runtime-components.sh", workflow)
        runtime_step = workflow.split(
            "      - name: Run isolated modsecurity_use_error_log on/off cells", 1
        )[1]
        self.assertIn(
            'NGINX_FUNCTIONAL_WORKER_USER="$NGINX_FUNCTIONAL_WORKER_USER"',
            runtime_step,
        )
        self.assertIn(
            'NGINX_FUNCTIONAL_WORKER_GROUP="$NGINX_FUNCTIONAL_WORKER_GROUP"',
            runtime_step,
        )
        provision_step = workflow.split(
            "      - name: Provision pinned NGINX and connector runtime", 1
        )[1].split("      - name: Print bounded NGINX provisioning failure diagnostics", 1)[0]
        self.assertIn("make setup-dev", provision_step)
        self.assertIn("make fetch-deps", provision_step)
        self.assertNotIn("sudo", provision_step)
        self.assertIn("persist-credentials: false", workflow)
        self.assertIn("Print bounded NGINX provisioning failure diagnostics", workflow)
        self.assertIn("if: failure()", workflow)
        diagnostic_step = workflow.split(
            "      - name: Print bounded NGINX provisioning failure diagnostics", 1
        )[1].split("      - name: Run isolated modsecurity_use_error_log on/off cells", 1)[0]
        self.assertIn('"$RUN_ROOT"', diagnostic_step)
        self.assertIn("/usr/bin/env -i PATH=/usr/bin:/bin HOME=/nonexistent LC_ALL=C", diagnostic_step)
        self.assertIn("ci/provisioning/components/nginx_exact_head_diagnostics.py", diagnostic_step)
        self.assertNotIn("VERIFIED_RUN_ROOT", diagnostic_step)
        self.assertNotIn("RUNTIME_REPORT_OUTPUT_ROOT", diagnostic_step)

    def test_gate_has_two_real_runtime_cells_and_fail_closed_markers(self):
        script = (ROOT / "connectors/nginx/harness/run_exact_head_use_error_log.sh").read_text()
        self.assertIn("for CURRENT_MODE in on off", script)
        self.assertIn("NGINX_USE_ERROR_LOG=\"$CURRENT_MODE\"", script)
        self.assertIn("MODSECURITY_RULE_PREAMBLE_FILE=\"$RULE_PREAMBLE\"", script)
        self.assertIn('"rule_id":"1100301"', script)
        self.assertNotIn("Access denied|ModSecurity", script)
        self.assertIn("native callback marker leaked with error-log off", script)
        self.assertIn("NGINX_HOSTED_FUNCTIONAL_A", script)
        self.assertIn("NGINX_FUNCTIONAL_A_PARENT_ROOT", script)
        self.assertIn("NGINX_FUNCTIONAL_A_RUNTIME_LIBRARY", script)
        self.assertIn("libmodsecurity.so.3", script)
        self.assertIn("require_existing_non_symlink_regular_file", script)
        self.assertIn('"$FUNCTIONAL_RUNTIME_LIBRARY"', script)
        self.assertNotIn('"$MODSECURITY_LIB_DIR/libmodsecurity.so"', script)
        self.assertIn("require_existing_non_symlink_directory", script)
        self.assertIn("functional-A root must be the designated fresh child", script)
        self.assertIn("artifact-identity.start.sha256", script)
        self.assertIn("unsafe_symlink", script)
        self.assertIn("phase4_reload_unsafe", script)
        self.assertNotIn("find ", script)

    def test_existing_template_renders_directive(self):
        template = (ROOT / "connectors/nginx/harness/nginx_smoke.conf").read_text()
        harness = (ROOT / "connectors/nginx/harness/run_nginx_smoke.sh").read_text()
        self.assertIn("@@NGINX_USE_ERROR_LOG_DIRECTIVE@@", template)
        self.assertIn("modsecurity_use_error_log off;", harness)
        self.assertIn('MODSECURITY_RUNTIME_LIBRARY="$MODSECURITY_LIB_DIR/libmodsecurity.so"', harness)
        self.assertIn('MODSECURITY_RUNTIME_LIBRARY="$NGINX_FUNCTIONAL_A_RUNTIME_LIBRARY"', harness)
        self.assertIn("hosted functional-A runtime library must not be a symlink", harness)


if __name__ == "__main__":
    unittest.main()
