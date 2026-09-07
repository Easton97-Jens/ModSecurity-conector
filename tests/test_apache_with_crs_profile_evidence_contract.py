"""Static contract checks for the Parent Apache With-CRS evidence handoff."""

from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "connectors/apache/harness/run_apache_smoke.sh"
PROFILE = ROOT / "ci/runtime/lifecycle/with-crs-no-mrts-profile.py"
WORKFLOW = ROOT / ".github/workflows/test-connectors-with-crs-no-mrts.yml"


class ApacheWithCrsProfileEvidenceContractTest(unittest.TestCase):
    @staticmethod
    def block(source: str, start: str, end: str) -> str:
        return source.split(start, 1)[1].split(end, 1)[0]

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
