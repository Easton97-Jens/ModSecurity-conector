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
        self.assertNotIn('RUN_ROOT="${RUNNER_TEMP:?missing runner temporary root}', workflow)
        self.assertIn(
            "FUNCTIONAL_JOB_ROOT=$(/usr/bin/mktemp -d /tmp/ModSecurity-conector-nginx-functional-root.XXXXXX)",
            workflow,
        )
        self.assertIn('if [ ! -d /tmp ] || [ -L /tmp ]; then', workflow)
        self.assertNotIn('[ -d /tmp ] && [ ! -L /tmp ] ||', workflow)
        self.assertIn(
            'if [ ! -d "$FUNCTIONAL_JOB_ROOT" ] || [ -L "$FUNCTIONAL_JOB_ROOT" ]; then',
            workflow,
        )
        self.assertNotIn(
            '[ -d "$FUNCTIONAL_JOB_ROOT" ] && [ ! -L "$FUNCTIONAL_JOB_ROOT" ] ||',
            workflow,
        )
        self.assertIn("[ \"$(/usr/bin/stat -c '%u:%a' /tmp)\" = \"0:1777\" ]", workflow)
        self.assertIn('RUN_ROOT="$FUNCTIONAL_JOB_ROOT/ModSecurity-conector-nginx-exact-head"', workflow)
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

    def test_each_hosted_case_uses_one_private_materialization_root(self):
        script = (ROOT / "connectors/nginx/harness/run_exact_head_use_error_log.sh").read_text()
        case_function = script.split("run_harness_case() {", 1)[1].split(
            "expect_config_rejection() {", 1
        )[0]

        self.assertIn('VERIFIED_RUN_ROOT="$mode_root"', case_function)
        self.assertIn('VERIFIED_BUILD_ROOT="$case_root"', case_function)
        self.assertIn('BUILD_ROOT="$case_root"', case_function)
        self.assertNotIn('BUILD_ROOT="$case_root/build"', case_function)
        for generated_path in (
            'LOG_ROOT="$case_root/logs"',
            'RESULTS_DIR="$case_root/results"',
            'NGINX_HARNESS_PARENT="$case_root/harness-parent"',
            'NGINX_HARNESS_WORK_ROOT="$case_root/harness"',
            'RUNTIME_BASE="$case_root/runtime-base"',
            'RUNTIME_ROOT="$case_root/runtime"',
            'LOG_DIR="$case_root/logs"',
        ):
            self.assertIn(generated_path, case_function)

    def test_hosted_worker_uses_a_dedicated_non_enumerable_functional_parent(self):
        workflow = (ROOT / ".github/workflows/test-nginx-exact-head.yml").read_text()
        launcher = (
            ROOT / "connectors/nginx/harness/run_github_hosted_functional_a.py"
        ).read_text()
        script = (ROOT / "connectors/nginx/harness/run_exact_head_use_error_log.sh").read_text()

        self.assertIn('/bin/chmod 700 "$RUN_ROOT"', workflow)
        self.assertIn(
            'FUNCTIONAL_PARENT_ROOT="$FUNCTIONAL_JOB_ROOT/ModSecurity-conector-nginx-functional-parent"',
            workflow,
        )
        self.assertIn(
            'if [ -e "$FUNCTIONAL_PARENT_ROOT" ] || [ -L "$FUNCTIONAL_PARENT_ROOT" ]; then',
            workflow,
        )
        self.assertNotIn(
            '[ ! -e "$FUNCTIONAL_PARENT_ROOT" ] && [ ! -L "$FUNCTIONAL_PARENT_ROOT" ] ||',
            workflow,
        )
        self.assertIn('/bin/chmod 711 "$FUNCTIONAL_PARENT_ROOT"', workflow)
        self.assertIn('/bin/chmod 711 "$FUNCTIONAL_JOB_ROOT"', workflow)
        self.assertIn('"$RUNNER_UID:700"', workflow)
        self.assertIn('"$RUNNER_UID:711"', workflow)
        self.assertIn('/usr/bin/test -x "$FUNCTIONAL_JOB_ROOT"', workflow)
        self.assertIn('/usr/bin/test -x "$FUNCTIONAL_PARENT_ROOT"', workflow)
        self.assertIn('/usr/bin/test -x "$RUN_ROOT"', workflow)
        self.assertIn("worker can traverse the private provisioning root", workflow)
        self.assertIn('NGINX_FUNCTIONAL_A_PARENT_ROOT="$NGINX_FUNCTIONAL_A_PARENT_ROOT"', workflow)
        self.assertIn('_TRUSTED_FUNCTIONAL_TMP_ROOT = Path("/tmp")', launcher)
        self.assertIn("_FUNCTIONAL_JOB_ROOT_PREFIX", launcher)
        self.assertIn("must be root-owned sticky mode 01777", launcher)
        self.assertIn("must be below the designated fresh /tmp job root", launcher)
        self.assertIn("must be the designated private child of the Functional-A job root", launcher)
        self.assertIn("_require_worker_traversable_functional_parent", launcher)
        self.assertIn("must be the designated sibling of VERIFIED_RUN_ROOT", launcher)
        self.assertIn("must be exactly non-enumerable mode 0711", launcher)
        self.assertIn("require_fresh_worker_traversable_directory()", script)
        self.assertIn('require_fresh_worker_traversable_directory "$FUNCTIONAL_ROOT"', script)
        self.assertIn('require_fresh_worker_traversable_directory "$mode_root"', script)
        self.assertIn('require_fresh_worker_traversable_directory "$case_root"', script)
        self.assertIn("0:711", script)

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
