from __future__ import annotations

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "all-connectors-no-crs.yml"


class AllConnectorsNoCrsWorkflowContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = WORKFLOW.read_text(encoding="utf-8")

    def test_workflow_keeps_manual_and_schedule_only_root_trust_boundary(self) -> None:
        self.assertIn("  workflow_dispatch:\n", self.source)
        self.assertIn("  schedule:\n", self.source)
        self.assertNotIn("pull_request:", self.source)
        self.assertNotIn("pull_request_target:", self.source)
        self.assertIn("permissions:\n  contents: read", self.source)
        self.assertIn("persist-credentials: false", self.source)
        self.assertIn("NGINX root handoff", self.source)

    def test_connector_workflow_uses_canonical_sibling_roots(self) -> None:
        expected = (
            'verified_root="$RUNNER_TEMP/ModSecurity-conector-verified"',
            'build_root="$verified_root/build"',
            'verified_evidence_root="$verified_root/evidence"',
            'evidence_root="$verified_evidence_root/no-crs-evidence"',
            'cache_root="$verified_root/cache-v2"',
            'echo "TMP_ROOT=$build_root/tmp"',
            'echo "LOG_ROOT=$build_root/logs"',
            'echo "VERIFIED_COMPONENT_CACHE=$cache_root/shared"',
            'echo "CONNECTOR_COMPONENT_CACHE=$cache_root/shared"',
            'echo "NGINX_HARNESS_PARENT=$build_root/nginx-harness"',
            'echo "VERIFIED_EVIDENCE_ROOT=$verified_evidence_root"',
            'echo "RUNTIME_REPORT_OUTPUT_ROOT=$build_root/runtime-component-reports"',
        )
        for fragment in expected:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.source)
        self.assertNotIn('evidence_root="$build_root/no-crs-evidence"', self.source)
        self.assertNotIn('echo "CONNECTOR_COMPONENT_CACHE=$verified_root/component-cache"', self.source)

    def test_nginx_handoff_is_scoped_to_the_nginx_matrix_row(self) -> None:
        block = re.search(
            r"- name: Configure supported NGINX Phase-4 mode\n(?P<body>.*?)(?=\n      - name: Initialize canonical evidence paths)",
            self.source,
            re.DOTALL,
        )
        self.assertIsNotNone(block)
        body = block.group("body")
        self.assertIn("if: matrix.connector == 'nginx'", body)
        self.assertIn('echo "NGINX_ROOT_HANDOFF=1" >> "$GITHUB_ENV"', body)
        self.assertIn('echo "NGINX_PHASE4_MODE=$CI_PHASE4_MODE" >> "$GITHUB_ENV"', body)
        self.assertEqual(self.source.count("NGINX_ROOT_HANDOFF=1"), 1)

    def test_workflow_uses_setup_python_path_for_privileged_handoff(self) -> None:
        self.assertIn('echo "PYTHON=${{ steps.setup-python.outputs.python-path }}"', self.source)
        self.assertIn("Verify Python interpreter contract", self.source)

    def test_aggregation_keeps_missing_artifacts_fail_closed(self) -> None:
        self.assertIn("Restore canonical evidence layout", self.source)
        self.assertIn('status=1', self.source)
        self.assertIn('exit "$status"', self.source)
        self.assertIn("Build result-only aggregate", self.source)
        self.assertIn("--output-json \"$EVIDENCE_ROOT/all-connectors-no-crs-summary.json\"", self.source)


if __name__ == "__main__":
    unittest.main()
