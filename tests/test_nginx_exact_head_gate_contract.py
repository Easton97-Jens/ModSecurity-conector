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
            "FUNCTIONAL_JOB_ROOT=$(/usr/bin/sudo -n /usr/bin/mktemp -d /tmp/ModSecurity-conector-nginx-functional-root.XXXXXX)",
            workflow,
        )
        self.assertNotIn(
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
        self.assertIn("RUNNER_GID=$(/usr/bin/id -g)", workflow)
        self.assertIn(
            "NATIVE_FIXTURE_ROOT=$(/usr/bin/mktemp -d /tmp/ModSecurity-conector-nginx-native-fixture.XXXXXX)",
            workflow,
        )
        self.assertNotIn(
            "NATIVE_FIXTURE_ROOT=$(/usr/bin/sudo -n /usr/bin/mktemp",
            workflow,
        )
        self.assertIn('case "$NATIVE_FIXTURE_ROOT" in', workflow)
        self.assertIn(
            "/tmp/ModSecurity-conector-nginx-native-fixture.*) ;;",
            workflow,
        )
        self.assertIn(
            'if [ ! -d "$NATIVE_FIXTURE_ROOT" ] || [ -L "$NATIVE_FIXTURE_ROOT" ]; then',
            workflow,
        )
        self.assertIn(
            '"$RUNNER_UID:$RUNNER_GID:700"',
            workflow,
        )
        self.assertIn('echo "NATIVE_FIXTURE_ROOT=$NATIVE_FIXTURE_ROOT"', workflow)
        self.assertIn('"0:700"', workflow)
        self.assertIn('"0:711"', workflow)
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
        self.assertIn("NGINX_SOURCE_MODE: github-release", workflow)
        self.assertIn("NGINX_SOURCE_REPO_URL: https://github.com/nginx/nginx", workflow)
        self.assertIn("NGINX_RELEASE_TAG: release-1.31.5", workflow)
        self.assertIn("NGINX_SOURCE_GIT_REF: release-1.31.5", workflow)
        self.assertIn("NGINX_RELEASE_ASSET_NAME: nginx-1.31.5.tar.gz", workflow)
        self.assertIn("NGINX_SHA256: e951607d534836624bd36b6b45a71dbfb055237deae3738da6bbf3270dada279", workflow)
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
        self.assertIn('RUN_ROOT="$RUN_ROOT"', runtime_step)
        self.assertIn('NATIVE_FIXTURE_ROOT="$NATIVE_FIXTURE_ROOT"', runtime_step)
        for fixture_argument in (
            "tests/run_nginx_body_buffer_fixture.py",
            '--connector-root "$CONNECTOR_ROOT"',
            '--expected-head "$EXPECTED_PARENT_SHA"',
            '--nginx-archive "$NGINX_DOWNLOAD_DIR/nginx-1.31.5.tar.gz"',
            '--nginx-sha256 "$NGINX_SHA256"',
            '--modsecurity-include "$MODSECURITY_INCLUDE_DIR"',
            '--modsecurity-lib "$MODSECURITY_LIB_DIR"',
            '--output-root "$NATIVE_FIXTURE_ROOT"',
        ):
            self.assertIn(fixture_argument, runtime_step)
        self.assertNotIn('$RUN_ROOT/native-nginx-body-buffer-fixture', workflow)
        fixture_upload = workflow.split(
            "      - name: Upload native NGINX body-buffer fixture evidence", 1
        )[1]
        self.assertIn("if: success()", fixture_upload)
        self.assertIn(
            "actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a # v7.0.1",
            fixture_upload,
        )
        self.assertIn(
            "${{ env.NATIVE_FIXTURE_ROOT }}/**/evidence/result.json",
            fixture_upload,
        )
        self.assertIn("if-no-files-found: error", fixture_upload)
        functional_upload = workflow.split(
            "      - name: Upload bounded NGINX Functional-A evidence", 1
        )[1].split("      - name: Upload native NGINX body-buffer fixture evidence", 1)[0]
        self.assertIn("if: success()", functional_upload)
        self.assertIn(
            "actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a # v7.0.1",
            functional_upload,
        )
        self.assertIn(
            "${{ env.RUN_ROOT }}/nginx-functional-a-evidence/result.json",
            functional_upload,
        )
        self.assertNotIn("nginx-hosted-functional-a/**", functional_upload)
        self.assertIn("if-no-files-found: error", functional_upload)
        self.assertIn("overwrite: false", functional_upload)
        self.assertIn('FUNCTIONAL_EVIDENCE_ROOT="$RUN_ROOT/nginx-functional-a-evidence"', runtime_step)
        self.assertIn('NGINX_FUNCTIONAL_A_EVIDENCE_ROOT="$FUNCTIONAL_EVIDENCE_ROOT"', runtime_step)
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
        self.assertIn("publish_functional_evidence", script)
        self.assertIn("write-nginx-functional-a-evidence.py", script)
        self.assertIn("NGINX_FUNCTIONAL_A_EVIDENCE_ROOT", script)
        self.assertIn("EXPECTED_PARENT_SHA", script)
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
        self.assertIn('/usr/bin/sudo -n /bin/mkdir "$RUN_ROOT"', workflow)
        self.assertIn('/usr/bin/sudo -n /bin/chown "$RUNNER_UID:$RUNNER_GID" "$RUN_ROOT"', workflow)
        self.assertIn('/usr/bin/sudo -n /bin/chmod 700 "$RUN_ROOT"', workflow)
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
        self.assertIn('/usr/bin/sudo -n /bin/mkdir "$FUNCTIONAL_PARENT_ROOT"', workflow)
        self.assertIn('/usr/bin/sudo -n /bin/chmod 711 "$FUNCTIONAL_PARENT_ROOT"', workflow)
        self.assertIn('/usr/bin/sudo -n /bin/chmod 711 "$FUNCTIONAL_JOB_ROOT"', workflow)
        self.assertIn('"$RUNNER_UID:700"', workflow)
        self.assertIn('"0:711"', workflow)
        self.assertNotIn('"$RUNNER_UID:711"', workflow)
        self.assertIn('/usr/bin/test -x "$FUNCTIONAL_JOB_ROOT"', workflow)
        self.assertIn('/usr/bin/test -x "$FUNCTIONAL_PARENT_ROOT"', workflow)
        self.assertIn('/usr/bin/test -x "$RUN_ROOT"', workflow)
        self.assertIn("worker can traverse the private provisioning root", workflow)
        self.assertIn('NGINX_FUNCTIONAL_A_PARENT_ROOT="$NGINX_FUNCTIONAL_A_PARENT_ROOT"', workflow)
        self.assertIn("import tempfile", launcher)
        self.assertIn('_EXPECTED_FUNCTIONAL_TMP_ROOT = Path(os.sep) / "tmp"', launcher)
        self.assertIn('path = _absolute_path(tempfile.gettempdir(), "Functional-A temporary root")', launcher)
        self.assertIn("if path != _EXPECTED_FUNCTIONAL_TMP_ROOT:", launcher)
        self.assertNotIn('_TRUSTED_FUNCTIONAL_TMP_ROOT = Path("/tmp")', launcher)
        self.assertIn("Functional-A job root must be owned by root", launcher)
        self.assertIn("NGINX_FUNCTIONAL_A_PARENT_ROOT must be owned by root", launcher)
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
