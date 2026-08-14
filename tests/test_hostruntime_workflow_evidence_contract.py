from __future__ import annotations

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = {
    "nginx": ROOT / ".github/workflows/test-nginx.yml",
    "haproxy": ROOT / ".github/workflows/test-haproxy.yml",
    "envoy": ROOT / ".github/workflows/test-envoy.yml",
    "traefik": ROOT / ".github/workflows/test-traefik.yml",
}
LOCK_PROFILES = {
    "nginx": ("nginx-h1",),
    "haproxy": ("haproxy-htx", "haproxy-spoe-spop"),
    "envoy": ("envoy-ext-authz", "envoy-ext-proc"),
    "traefik": ("traefik-forwardauth", "traefik-native"),
}
UPLOAD_SHA = "043fb46d1a93c77aae656e7c1c64a875d1fc6a0a"
ALLOWED_STATUSES = ("PASS", "FAIL", "BLOCKED", "NOT_RUN", "NOT_APPLICABLE")


class HostRuntimeWorkflowEvidenceContractTest(unittest.TestCase):
    def test_each_connector_runs_locked_preflights_and_uploads_exact_evidence_root(self) -> None:
        for connector, path in WORKFLOWS.items():
            with self.subTest(connector=connector):
                workflow = path.read_text(encoding="utf-8")
                self.assertIn("hostruntime-preflight.py", workflow)
                self.assertIn("--runtime-lock \"$RUNTIME_LOCK\"", workflow)
                self.assertIn("--lock-profile \"$lock_profile\"", workflow)
                self.assertIn(
                    "modules/ModSecurity-test-Framework/ci/provisioning/runtime-component-lock.json",
                    workflow,
                )
                self.assertIn("preflight_dir=\"$evidence_dir/preflight\"", workflow)
                self.assertIn("--write-dir \"$RUNNER_TEMP\"", workflow)
                self.assertIn("--disk-path \"$RUNNER_TEMP\"", workflow)
                self.assertIn("--config ", workflow)
                self.assertIn("--fixture ", workflow)
                self.assertIn("--tool ", workflow)
                for lock_profile in LOCK_PROFILES[connector]:
                    self.assertIn(f"run_preflight {lock_profile}", workflow)
                self.assertIn("if: always()", workflow)
                self.assertIn(f"$RUNNER_TEMP/hostruntime-evidence/$CONNECTOR", workflow)
                self.assertIn(f"${{{{ runner.temp }}}}/hostruntime-evidence/{connector}", workflow)
                self.assertIn(
                    f"actions/upload-artifact@{UPLOAD_SHA}",
                    workflow,
                )
                self.assertIn("summary.md", workflow)
                self.assertIn("status.json", workflow)

    def test_workflows_keep_status_allowlist_and_runtime_not_run_semantics(self) -> None:
        for connector, path in WORKFLOWS.items():
            with self.subTest(connector=connector):
                workflow = path.read_text(encoding="utf-8")
                for status in ALLOWED_STATUSES:
                    self.assertIn(f'"{status}"', workflow)
                self.assertIn('status = "BLOCKED"', workflow)
                self.assertIn('status == "PASS"', workflow)
                self.assertIn("preflight_exit_without_pass_evidence", workflow)
                self.assertIn("runtime_lock_missing", workflow)
                self.assertIn("binary_", workflow)
                self.assertIn('"runtime_status": "NOT_RUN"', workflow)
                self.assertIn('"status": "NOT_RUN"', workflow)
                self.assertIn("hostruntime-record.json", workflow)
                self.assertIn("preflight_blocked", workflow)
                self.assertIn("runtime_execution_not_configured", workflow)
                self.assertNotIn('"runtime_status": "PASS"', workflow)

    def test_artifact_projection_is_allowlisted_and_bounded(self) -> None:
        allowed_fields = (
            '"schema_version": 1',
            '"evidence_kind": "preflight"',
            '"status": status',
            '"runtime_status": "NOT_RUN"',
            '"reason_code": clean(reason_code, 100)',
            '"exit_code": exit_code',
            '"expected_version": clean',
            '"actual_version": clean',
            '"runtime_lock": {',
        )
        for connector, path in WORKFLOWS.items():
            with self.subTest(connector=connector):
                workflow = path.read_text(encoding="utf-8")
                self.assertIn("def clean(value: object, limit: int = 160)", workflow)
                self.assertIn("re.sub(r\"[", workflow)
                self.assertIn("]\", \" \", str(value))[:limit]", workflow)
                for field in allowed_fields:
                    self.assertIn(field, workflow)
                self.assertNotIn('"reason":', workflow)
                self.assertNotIn('"provenance":', workflow)
                self.assertNotRegex(workflow, re.compile(r"raw\.get\(\s*['\"](?:body|payload|log|token|secret|password)"))


if __name__ == "__main__":
    unittest.main()
