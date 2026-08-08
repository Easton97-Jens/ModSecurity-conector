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

    def test_connector_workflow_pins_the_reviewed_nginx_provenance_tuple(self) -> None:
        job_environment = re.search(
            r"^    env:\n(?P<body>.*?)(?=^    steps:)",
            self.source,
            re.MULTILINE | re.DOTALL,
        )
        self.assertIsNotNone(job_environment)
        environment = job_environment.group("body")
        expected = {
            "NGINX_SOURCE_MODE": "github-release",
            "NGINX_SOURCE_REPO_URL": "https://github.com/nginx/nginx",
            "NGINX_GITHUB_REPO": "https://github.com/nginx/nginx",
            "NGINX_RELEASE_TAG": "release-1.31.3",
            "NGINX_SOURCE_GIT_REF": "release-1.31.3",
            "NGINX_RELEASE_ASSET_NAME": "nginx-1.31.3.tar.gz",
            "NGINX_SHA256": "a7657c50811c2d92d9895395e8b873ef60398142c4db21eb647811c38f6dd525",
        }
        for name, value in expected.items():
            with self.subTest(name=name):
                self.assertIn(f"      {name}: {value}\n", environment)
        self.assertNotIn("NGINX_RELEASE_TAG: latest", environment)

    def test_connector_workflow_defers_apr_util_provenance_to_the_pinned_framework(self) -> None:
        job_environment = re.search(
            r"^    env:\n(?P<body>.*?)(?=^    steps:)",
            self.source,
            re.MULTILINE | re.DOTALL,
        )
        self.assertIsNotNone(job_environment)
        environment = job_environment.group("body")
        for name in (
            "APR_UTIL_VERSION",
            "APR_UTIL_SOURCE_URL",
            "APR_UTIL_SHA256",
            "APR_UTIL_SHA256_URL",
        ):
            with self.subTest(name=name):
                self.assertNotIn(f"      {name}:", environment)

    def test_makefile_keeps_absent_apr_util_variables_absent(self) -> None:
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        for name in (
            "APR_UTIL_VERSION",
            "APR_UTIL_SOURCE_URL",
            "APR_UTIL_SHA256",
            "APR_UTIL_SHA256_URL",
        ):
            with self.subTest(name=name):
                self.assertIn(
                    f"ifneq ($(origin {name}),undefined)\nexport {name}\nendif",
                    makefile,
                )
                self.assertEqual(makefile.count(f"export {name}\n"), 1)

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
        self.assertIn(
            "SETUP_PYTHON_PATH: ${{ steps.setup-python.outputs.python-path }}",
            self.source,
        )
        self.assertIn("printf 'PYTHON=%s\\n' \"$SETUP_PYTHON_PATH\"", self.source)
        self.assertNotIn('echo "PYTHON=${{ steps.setup-python.outputs.python-path }}"', self.source)
        self.assertIn("Verify Python interpreter contract", self.source)

    def test_aggregation_keeps_missing_artifacts_fail_closed(self) -> None:
        self.assertIn("Restore canonical evidence layout", self.source)
        self.assertIn('status=1', self.source)
        self.assertIn('exit "$status"', self.source)
        self.assertIn("Build result-only aggregate", self.source)
        self.assertIn("--output-json \"$EVIDENCE_ROOT/all-connectors-no-crs-summary.json\"", self.source)


if __name__ == "__main__":
    unittest.main()
