"""Static trust-boundary contract for the immutable broker workflow."""

from __future__ import annotations

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "nginx-root-broker.yml"


class TrustedNginxRootBrokerWorkflowTest(unittest.TestCase):
    def setUp(self) -> None:
        self.workflow = WORKFLOW.read_text(encoding="utf-8")

    def test_workflow_is_reusable_read_only_and_refuses_pr_trigger_modes(self) -> None:
        self.assertIn("  workflow_call:\n", self.workflow)
        self.assertNotIn("  pull_request:", self.workflow)
        self.assertNotIn("  pull_request_target:", self.workflow)
        self.assertIn("permissions:\n  contents: read", self.workflow)
        self.assertIn("github.event_name == 'workflow_dispatch' || github.event_name == 'schedule'", self.workflow)
        self.assertIn("github.repository == 'Easton97-Jens/ModSecurity-conector'", self.workflow)
        self.assertIn("github.event.repository.fork == false", self.workflow)
        self.assertNotIn("secrets.", self.workflow)

    def test_broker_source_is_immutable_and_must_already_be_on_protected_master(self) -> None:
        self.assertIn("ACTUAL_WORKFLOW_REF: ${{ github.workflow_ref }}", self.workflow)
        self.assertIn("EXPECTED_WORKFLOW_REF: Easton97-Jens/ModSecurity-conector/.github/workflows/nginx-root-broker.yml@${{ inputs.protected_broker_sha }}", self.workflow)
        self.assertIn('test "$ACTUAL_WORKFLOW_REF" = "$EXPECTED_WORKFLOW_REF"', self.workflow)
        self.assertIn("repository: Easton97-Jens/ModSecurity-conector", self.workflow)
        self.assertIn("ref: ${{ inputs.protected_broker_sha }}", self.workflow)
        self.assertIn("path: broker-src", self.workflow)
        self.assertIn("submodules: recursive", self.workflow)
        self.assertIn("persist-credentials: false", self.workflow)
        self.assertIn("clean: true", self.workflow)
        self.assertIn('test "$(git rev-parse HEAD)" = "$BROKER_SHA"', self.workflow)
        self.assertIn('git merge-base --is-ancestor "$BROKER_SHA" FETCH_HEAD', self.workflow)
        self.assertIn('git rev-parse "$BROKER_SHA:ci/runtime/broker/nginx_root_broker.py"', self.workflow)
        self.assertIn("git hash-object ci/runtime/broker/nginx_root_broker.py", self.workflow)
        self.assertIn("/usr/bin/python3 -I ci/runtime/broker/nginx_root_broker.py", self.workflow)
        self.assertNotIn("@master", self.workflow)
        self.assertNotIn("@fix/f-gs-003-pin-nginx-full-smoke", self.workflow)
        self.assertNotIn("uses: ./", self.workflow)

    def test_root_invocation_is_fixed_after_unprivileged_protected_build(self) -> None:
        self.assertLess(
            self.workflow.index("Build only trusted protected-source artifacts without root"),
            self.workflow.index("Build a protected immutable OWASP CRS bundle without root"),
        )
        self.assertLess(
            self.workflow.index("Build a protected immutable OWASP CRS bundle without root"),
            self.workflow.index("Admit only verified artifacts into the root-owned broker root"),
        )
        self.assertIn("make fetch-deps", self.workflow)
        self.assertIn("prepare-fresh-crs-source.sh", self.workflow)
        self.assertIn("ci/provisioning/fetch-crs.sh", self.workflow)
        self.assertIn("prepare-crs-bundle", self.workflow)
        self.assertIn("prepare-from-snapshot", self.workflow)
        self.assertIn("sudo -- /usr/bin/python3 -I ci/runtime/broker/nginx_root_broker.py action", self.workflow)
        for action in (
            "validate-manifest",
            "config-test",
            "start",
            "verify-runtime-profile",
            "verify-master-worker-identity",
            "project-evidence",
            "stop",
            "cleanup-status",
        ):
            self.assertIn(action, self.workflow)
        for forbidden in ("sudo -E", "sudo sh -c", "sudo bash -c", "systemctl", "service "):
            self.assertNotIn(forbidden, self.workflow)
        for forbidden in ("--broker-parent", "--staging-root", "--runtime-snapshot"):
            self.assertNotIn(forbidden, self.workflow)

    def test_bounded_evidence_is_staged_before_descriptor_cleanup_and_records_its_outcome(self) -> None:
        self.assertLess(
            self.workflow.index("Run fixed root-only NGINX actions"),
            self.workflow.index("Stage the fixed root-to-user evidence outside the cleanup root"),
        )
        self.assertLess(
            self.workflow.index("Stage the fixed root-to-user evidence outside the cleanup root"),
            self.workflow.index("Stop and verify root cleanup"),
        )
        self.assertLess(
            self.workflow.index("Stop and verify root cleanup"),
            self.workflow.index("Upload bounded root-to-user evidence"),
        )
        for filename in (
            "identity.json",
            "runtime.json",
            "policy.json",
            "nginx-access.log",
            "nginx-error.log",
            "nginx-audit.log",
            "cleanup.json",
        ):
            self.assertIn(filename, self.workflow)
        self.assertIn('"cleanup_status":"%s"', self.workflow)
        self.assertNotIn("cp -r", self.workflow)
        self.assertNotIn("tar ", self.workflow)

    def test_caller_data_is_limited_to_a_declarative_artifact_and_pinned_inputs(self) -> None:
        for field in (
            "caller_manifest_artifact",
            "parent_head_sha",
            "framework_sha",
            "protected_broker_sha",
            "matrix_variant",
            "run_id",
        ):
            self.assertIn(f"      {field}:\n", self.workflow)
        self.assertIn("Download declarative caller manifest", self.workflow)
        self.assertIn("caller-manifest.json", self.workflow)
        self.assertIn("--expected-parent-head \"$EXPECTED_PARENT_HEAD\"", self.workflow)
        self.assertIn("--expected-framework-sha \"$EXPECTED_FRAMEWORK_SHA\"", self.workflow)
        self.assertIn("--expected-run-id \"$BROKER_RUN_ID\"", self.workflow)
        self.assertIn("--expected-matrix-variant \"$BROKER_VARIANT\"", self.workflow)
        self.assertNotIn("github.event.pull_request.head.sha", self.workflow)
        self.assertNotIn("GITHUB_TOKEN", self.workflow)

    def test_actions_are_full_sha_pinned(self) -> None:
        for action in re.findall(r"uses:\s+([^\s]+)", self.workflow):
            self.assertRegex(action, r"^[\w.-]+/[\w.-]+@[0-9a-f]{40}$")


if __name__ == "__main__":
    unittest.main()
