"""Static contract for the five-connector no-CRS/with-MRTS workflow."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "test-connectors-no-crs-with-mrts.yml"
SHA_PIN = re.compile(r"uses: [^@\s]+@[a-f0-9]{40} # v[^\n]+")


class NoCrsWithMrtsWorkflowContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = WORKFLOW.read_text(encoding="utf-8")

    def test_closed_five_connector_matrix(self) -> None:
        matrix = re.search(r"matrix:\n\s+connector:\n(?P<body>(?:\s+- \w+\n)+)", self.source)
        self.assertIsNotNone(matrix)
        self.assertEqual(
            re.findall(r"^\s+- (\w+)$", matrix.group("body"), re.MULTILINE),
            ["apache", "envoy", "haproxy", "lighttpd", "traefik"],
        )
        self.assertIn("CRS_VARIANT: no-crs", self.source)
        self.assertIn("MRTS_VARIANT: with-mrts", self.source)
        self.assertNotIn("with-crs/with-mrts", self.source)
        self.assertNotIn("MODSECURITY_RULESET: crs", self.source)

    def test_target_connectors_use_dedicated_runtime_runner(self) -> None:
        self.assertIn("ci/runtime/lifecycle/run-no-crs-with-mrts-target.py", self.source)
        self.assertIn('--connector "$CONNECTOR"', self.source)
        self.assertIn("--execute-stage", self.source)
        self.assertIn('--parent-root "$GITHUB_WORKSPACE"', self.source)
        self.assertIn('--framework-root "$FRAMEWORK_ROOT"', self.source)
        self.assertIn('--runtime-root "$RUNTIME_ROOT"', self.source)
        self.assertIn("make full-matrix-single-job-runtime CONNECTOR=\"$CONNECTOR\" CRS=no-crs MRTS=with-mrts", self.source)

    def test_workflow_security_contract(self) -> None:
        self.assertIn("pull_request:", self.source)
        self.assertIn("workflow_dispatch:", self.source)
        self.assertNotIn("pull_request_target", self.source)
        self.assertIn("permissions:\n  contents: read", self.source)
        self.assertNotIn("permissions: write", self.source)
        self.assertNotIn("secrets:", self.source)
        self.assertNotIn("continue-on-error", self.source)
        self.assertNotIn("|| true", self.source)
        self.assertIn("persist-credentials: false", self.source)
        self.assertGreaterEqual(len(SHA_PIN.findall(self.source)), 3)
        self.assertIn("concurrency:", self.source)
        self.assertIn("if-no-files-found: error", self.source)

    def test_go_toolchain_is_pinned_to_repository_contract(self) -> None:
        self.assertIn(
            "uses: actions/setup-go@b7ad1dad31e06c5925ef5d2fc7ad053ef454303e # v7.0.0",
            self.source,
        )
        self.assertIn("go-version-file: .go-version", self.source)
        self.assertIn("GOTOOLCHAIN: local", self.source)
        self.assertIn('expected_go_version="$(tr -d \'[:space:]\' < .go-version)"', self.source)
        self.assertIn('actual_go_version="$(go version | sed -n', self.source)
        self.assertIn('test "$actual_go_version" = "$expected_go_version"', self.source)
        self.assertNotIn("GO: /usr/local/go/bin/go", self.source)

    def test_paths_are_run_and_attempt_and_connector_scoped(self) -> None:
        self.assertIn("${{ github.run_id }}-${{ github.run_attempt }}/${{ matrix.connector }}", self.source)
        self.assertIn("RUNTIME_ROOT:", self.source)
        self.assertIn("name: no-crs-with-mrts-${{ matrix.connector }}-${{ github.run_id }}-${{ github.run_attempt }}", self.source)


if __name__ == "__main__":
    unittest.main()
