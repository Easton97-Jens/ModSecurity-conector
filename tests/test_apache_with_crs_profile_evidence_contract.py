"""Static contract checks for the Parent Apache With-CRS evidence handoff."""

from __future__ import annotations

from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "connectors/apache/harness/run_apache_smoke.sh"
PROFILE = ROOT / "ci/runtime/lifecycle/with-crs-no-mrts-profile.py"
WORKFLOW = ROOT / ".github/workflows/test-connectors-with-crs-no-mrts.yml"


class ApacheWithCrsProfileEvidenceContractTest(unittest.TestCase):
    @staticmethod
    def block(source: str, start: str, end: str) -> str:
        return source.split(start, 1)[1].split(end, 1)[0]

    def run_profile_audit_path_guard(self, path: str) -> subprocess.CompletedProcess[str]:
        source = HARNESS.read_text(encoding="utf-8")
        guard = "require_safe_apache_config_path() {\n" + self.block(
            source,
            "require_safe_apache_config_path() {\n",
            "configure_apache_profile_audit() {\n",
        )
        script = "\n".join(
            (
                "blocked() { exit 77; }",
                guard,
                'require_safe_apache_config_path "$1" "Apache profile audit path"',
            )
        )
        return subprocess.run(
            ["sh", "-c", script, "sh", path],
            cwd=ROOT,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def test_harness_requires_a_transaction_bound_audit_and_proven_cleanup_before_pass(self) -> None:
        source = HARNESS.read_text(encoding="utf-8")
        self.assertIn("apache_profile_stop_tracked_process()", source)
        self.assertIn("apache_profile_publish_cleanup_receipt()", source)
        self.assertIn('port_is_free "$PORT"', source)
        self.assertIn('[ ! -e "$RUNTIME_PID_FILE" ]', source)
        success = self.block(
            source,
            'if "$PYTHON_BIN" "$CASE_CLI" assert-status',
            'reason=$(cat "$LOG_DIR/case-assert.log"',
        )
        self.assertIn("verify-apache-audit", success)
        self.assertIn("APACHE_PROFILE_FINAL_CLEANUP=1", success)
        self.assertIn("if ! cleanup; then", success)
        self.assertIn("APACHE_PROFILE_FINAL_CLEANUP=0", success)
        self.assertLess(success.index("verify-apache-audit"), success.index("APACHE_PROFILE_FINAL_CLEANUP=1"))
        self.assertLess(success.index("APACHE_PROFILE_FINAL_CLEANUP=1"), success.index("if ! cleanup; then"))
        self.assertLess(success.index("if ! cleanup; then"), success.index('write_case_result "$TEST_CASE" pass'))

    def test_profile_scoped_audit_configuration_follows_materialization_and_excludes_no_crs(self) -> None:
        source = HARNESS.read_text(encoding="utf-8")
        audit = self.block(
            source,
            "configure_apache_profile_audit() {\n",
            "apache_profile_stop_tracked_process() {\n",
        )
        self.assertIn("1) return 0 ;;", audit)
        self.assertIn('[ "$MODSECURITY_TEST_VARIANT" = "with-crs" ] ||', audit)
        self.assertIn("SecAuditEngine On", audit)
        self.assertIn("SecAuditLogType Serial", audit)
        self.assertIn("SecAuditLogFormat Native", audit)
        self.assertIn("SecAuditLogParts ABFHZ", audit)
        self.assertIn(
            'require_safe_apache_config_path "$AUDIT_LOG_FILE" "Apache profile audit path"',
            audit,
        )
        self.assertIn('printf \'SecAuditLog "%s"\\n\' "$AUDIT_LOG_FILE"', audit)
        self.assertLess(
            audit.index('require_safe_apache_config_path "$AUDIT_LOG_FILE"'),
            audit.index('printf \'SecAuditLog "%s"\\n\' "$AUDIT_LOG_FILE"'),
        )
        materialization = self.block(
            source,
            'if ! "$PYTHON_BIN" "$CASE_CLI" materialize',
            '. "$CASE_ENV_FILE"',
        )
        self.assertIn("configure_apache_profile_audit", materialization)

    def test_profile_audit_config_path_rejects_unsafe_apache_quoted_value(self) -> None:
        cases = (
            ("/tmp/profile audit-()[]!;,.log", 0),
            ('/tmp/profile-"\nSecAuditLog "/tmp/attacker"\n#', 77),
            ("/tmp/profile\\audit.log", 77),
            ("/tmp/" + "$" + "{AUDIT_TARGET}/audit.log", 77),
        )
        for path, expected_returncode in cases:
            with self.subTest(path=repr(path)):
                result = self.run_profile_audit_path_guard(path)
                self.assertEqual(result.returncode, expected_returncode, result.stderr)

    def test_single_case_creates_results_directory_before_runtime_output(self) -> None:
        source = HARNESS.read_text(encoding="utf-8")
        single_case = source.split(
            'if [ "$RUN_ONE_CASE" != "1" ]; then\n', 1
        )[1]
        single_case_setup = single_case.split("RUNTIME_PID_FILE=", 1)[0]
        self.assertIn(
            'if [ "$RUN_ONE_CASE" = "1" ]; then\n'
            '    require_absolute_generated_path "$RESULTS_DIR" "RESULTS_DIR"\n'
            '    mkdir -p "$RESULTS_DIR"\n'
            "fi",
            single_case_setup,
        )
        self.assertLess(
            single_case_setup.index('require_absolute_generated_path "$RESULTS_DIR" "RESULTS_DIR"'),
            single_case_setup.index('mkdir -p "$RESULTS_DIR"'),
        )
        all_cases = self.block(source, "run_all_cases() {\n", "write_case_result() {")
        self.assertIn('mkdir -p "$LOG_DIR" "$RESULTS_DIR"', all_cases)

    def test_profile_consumes_raw_audit_and_exact_cleanup_receipt_fields(self) -> None:
        source = PROFILE.read_text(encoding="utf-8")
        self.assertIn("APACHE_AUDIT_RELATIVE_PATH", source)
        self.assertIn("APACHE_CLEANUP_RECEIPT_NAME", source)
        self.assertIn("_apache_audit_block_observation(audit_raw)", source)
        self.assertIn("_apache_cleanup_receipt(", source)
        self.assertIn('"tracked_host_processes_remaining"', source)
        self.assertIn('"tracked_helper_processes_remaining"', source)
        self.assertIn('"selected_listeners_remaining"', source)
        self.assertIn('"github_run_id"', source)
        self.assertIn('"github_run_attempt"', source)
        self.assertIn("os.O_EXCL", source)
        self.assertIn("os.O_NOFOLLOW", source)

    def test_workflow_hands_runtime_identity_into_harness_then_requires_source_receipts(self) -> None:
        source = WORKFLOW.read_text(encoding="utf-8")
        checkout = self.block(
            source,
            "      - name: Checkout exact Parent head with pinned submodules\n",
            "      - name: Set up locked Python toolchain\n",
        )
        self.assertIn("fetch-depth: 0", checkout)
        revisions = self.block(
            source,
            "      - name: Verify pinned Parent, Framework, and MRTS revisions\n",
            "      - name: Install hash-locked Framework CI dependency\n",
        )
        self.assertIn('base_commit=$(git rev-parse "${EXPECTED_BASE_SHA}^{commit}")', revisions)
        self.assertIn('test "$base_commit" = "$EXPECTED_BASE_SHA"', revisions)
        runtime = self.block(
            source,
            "      - name: Run selected real with-CRS no-MRTS runtime\n",
            "      - name: Project HAProxy runtime evidence\n",
        )
        for assignment in (
            "RUN_ONE_CASE=1",
            'APACHE_PROFILE_CLEANUP_RECEIPT="$VERIFIED_RUN_ROOT/apache-profile-cleanup-receipt.json"',
            'APACHE_PROFILE_CELL_RUN_ID="$CRS_RUNTIME_RUN_ID"',
            'APACHE_PROFILE_GITHUB_RUN_ID="$GITHUB_RUN_ID"',
            'APACHE_PROFILE_GITHUB_RUN_ATTEMPT="$GITHUB_RUN_ATTEMPT"',
        ):
            self.assertIn(assignment, runtime)
        validation = self.block(
            source,
            "      - name: Validate Apache runtime evidence\n",
            "      - name: Produce canonical with-CRS no-MRTS profile cell\n",
        )
        self.assertIn("AUDIT_LOG:", validation)
        self.assertIn("CLEANUP_RECEIPT:", validation)
        self.assertIn("verify-apache-audit", validation)
        # The Framework wrapper passes APACHE_RUNTIME_LOG_DIR as the harness's
        # LOG_DIR, and the harness writes its native serial audit directly at
        # "$LOG_DIR/audit.log".  A case-name suffix here would validate a
        # nonexistent path after an otherwise successful real Apache run.
        self.assertIn(
            "AUDIT_LOG: ${{ env.BUILD_ROOT }}/verified-apache-case/"
            "with-crs-no-mrts-apache/logs/apache-runtime/audit.log",
            validation,
        )
        self.assertNotIn(
            "logs/apache-runtime/crs_sqli_anomaly_block/audit.log",
            validation,
        )
        producer = self.block(
            source,
            "      - name: Produce canonical with-CRS no-MRTS profile cell\n",
            "      - name: Upload Apache runtime evidence\n",
        )
        self.assertIn("apache)\n              source_root=\"$VERIFIED_ROOT\"", producer)
        self.assertIn("--crs-source-root \"$crs_source_root\"", producer)
        self.assertIn("HAPROXY_EVIDENCE_UID:", producer)
        self.assertIn("HAPROXY_EVIDENCE_GID:", producer)
        self.assertIn("--haproxy-evidence-uid \"$HAPROXY_EVIDENCE_UID\"", producer)
        self.assertIn("--haproxy-evidence-gid \"$HAPROXY_EVIDENCE_GID\"", producer)
        self.assertIn("steps.validate-apache-runtime-evidence.outcome == 'success'", source)


if __name__ == "__main__":
    unittest.main()
