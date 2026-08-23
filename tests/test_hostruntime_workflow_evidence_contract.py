from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
COLLECTOR = ROOT / "ci/runtime/common/collect_hostruntime_preflight_evidence.py"
WORKFLOWS = {
    "nginx": ROOT / ".github/workflows/test-nginx.yml",
    "haproxy": ROOT / ".github/workflows/test-haproxy.yml",
    "envoy": ROOT / ".github/workflows/test-envoy.yml",
    "traefik": ROOT / ".github/workflows/test-traefik.yml",
}
WORKFLOW_SPECS = {
    "nginx": {
        "binary": "nginx",
        "profiles": (
            (
                "nginx-h1",
                "connectors/nginx/harness/nginx_smoke.conf",
                "modules/ModSecurity-test-Framework/tests/cases/connector-specific/nginx/nginx_tx_scoring_absolute_block.yaml",
            ),
        ),
        "markdown_code": True,
    },
    "haproxy": {
        "binary": "haproxy",
        "profiles": (
            (
                "haproxy-htx",
                "connectors/haproxy/poc/spoe/haproxy.cfg.example",
                "connectors/haproxy/harness/fixtures/modsecurity-binding-lifecycle.conf",
            ),
            (
                "haproxy-spoe-spop",
                "connectors/haproxy/poc/spoe/haproxy.cfg.example",
                "connectors/haproxy/harness/fixtures/modsecurity-binding-lifecycle.conf",
            ),
        ),
        "markdown_code": False,
    },
    "envoy": {
        "binary": "envoy",
        "profiles": (
            (
                "envoy-ext-authz",
                "connectors/envoy/config/envoy-ext-authz.conf",
                "connectors/envoy/config/envoy-ext-proc-service.json",
            ),
            (
                "envoy-ext-proc",
                "connectors/envoy/config/envoy-ext-authz.conf",
                "connectors/envoy/config/envoy-ext-proc-service.json",
            ),
        ),
        "markdown_code": False,
    },
    "traefik": {
        "binary": "traefik",
        "profiles": (
            (
                "traefik-forwardauth",
                "connectors/traefik/config/traefik-forwardauth.conf",
                "connectors/traefik/config/traefik-native-middleware-dynamic.yaml",
            ),
            (
                "traefik-native",
                "connectors/traefik/config/traefik-forwardauth.conf",
                "connectors/traefik/config/traefik-native-middleware-dynamic.yaml",
            ),
        ),
        "markdown_code": False,
    },
}
UPLOAD_SHA = "043fb46d1a93c77aae656e7c1c64a875d1fc6a0a"


class HostRuntimeWorkflowEvidenceContractTest(unittest.TestCase):
    def test_each_connector_calls_the_shared_collector_with_its_locked_inputs(self) -> None:
        for connector, path in WORKFLOWS.items():
            with self.subTest(connector=connector):
                workflow = path.read_text(encoding="utf-8")
                spec = WORKFLOW_SPECS[connector]
                self.assertIn("collect_hostruntime_preflight_evidence.py", workflow)
                self.assertNotIn("hostruntime-preflight.py", workflow)
                self.assertNotIn("<<'PY'", workflow)
                self.assertIn('--connector "$CONNECTOR"', workflow)
                self.assertIn('--runtime-lock "$RUNTIME_LOCK"', workflow)
                self.assertIn('--runner-temp "$RUNNER_TEMP"', workflow)
                self.assertIn(f"--binary-name {spec['binary']}", workflow)
                self.assertIn(
                    "modules/ModSecurity-test-Framework/ci/provisioning/runtime-component-lock.json",
                    workflow,
                )
                for profile, config, fixture in spec["profiles"]:
                    self.assertIn(f"--profile {profile}", workflow)
                    self.assertIn(f"--config {config}", workflow)
                    self.assertIn(f"--fixture {fixture}", workflow)
                self.assertEqual("--markdown-code" in workflow, spec["markdown_code"])

    def test_workflows_preserve_always_run_upload_and_exact_artifact_projection(self) -> None:
        for connector, path in WORKFLOWS.items():
            with self.subTest(connector=connector):
                workflow = path.read_text(encoding="utf-8")
                self.assertGreaterEqual(workflow.count("if: always()"), 2)
                self.assertIn(f"${{{{ runner.temp }}}}/hostruntime-evidence/{connector}", workflow)
                self.assertIn(f"actions/upload-artifact@{UPLOAD_SHA}", workflow)
                self.assertIn(f"name: {connector}-hostruntime-evidence", workflow)
                self.assertIn("if-no-files-found: error", workflow)

    def test_shared_collector_retains_the_payload_safe_fail_closed_contract(self) -> None:
        collector = COLLECTOR.read_text(encoding="utf-8")
        for status in ("PASS", "FAIL", "BLOCKED", "NOT_RUN", "NOT_APPLICABLE"):
            with self.subTest(status=status):
                self.assertIn(f'"{status}"', collector)
        for marker in (
            "preflight_exit_without_pass_evidence",
            "runtime_lock_missing",
            "invalid_or_missing_preflight_status",
            "binary_",
            '"runtime_status": "NOT_RUN"',
            '"status": "NOT_RUN"',
            "runtime_execution_not_configured",
            "preflight_blocked",
            "def safe_component",
            "def safe_relative_path",
            "subprocess.run(command, check=False)",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, collector)
        self.assertNotIn("shell=True", collector)
        self.assertNotIn('"reason":', collector)
        self.assertNotIn('"provenance":', collector)


if __name__ == "__main__":
    unittest.main()
