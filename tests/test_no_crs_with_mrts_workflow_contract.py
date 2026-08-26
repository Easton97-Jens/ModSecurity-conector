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

    def test_closed_five_connector_matrix_excludes_nginx(self) -> None:
        matrix = re.search(r"matrix:\n\s+connector:\n(?P<body>(?:\s+- \w+\n)+)", self.source)
        self.assertIsNotNone(matrix)
        self.assertEqual(
            re.findall(r"^\s+- (\w+)$", matrix.group("body"), re.MULTILINE),
            ["apache", "envoy", "haproxy", "lighttpd", "traefik"],
        )
        self.assertIn("CRS_VARIANT: no-crs", self.source)
        self.assertIn("MRTS_VARIANT: with-mrts", self.source)
        self.assertIn('ALLOW_RUNTIME_DOWNLOADS: "1"', self.source)
        self.assertIn('ALLOW_RUNTIME_BUILDS: "1"', self.source)
        self.assertNotIn("nginx", self.source)
        self.assertNotIn("with-crs/with-mrts", self.source)
        self.assertNotIn("MODSECURITY_RULESET: crs", self.source)
        self.assertNotIn("NO_CRS_RUN_ID:", self.source)

    def test_preparation_is_connector_scoped_without_matrix_target_input(self) -> None:
        preparation = self.source.split("      - name: Prepare MRTS runtime dependencies\n", 1)[1].split(
            "      - name: Run connector-isolated MRTS host runtime\n", 1
        )[0]
        self.assertIn('case "$CONNECTOR" in', preparation)
        self.assertIn("apache) RUNTIME_COMPONENT_TARGET=apache make prepare-runtime-components ;;", preparation)
        self.assertIn("haproxy) RUNTIME_COMPONENT_TARGET=haproxy make prepare-runtime-components ;;", preparation)
        self.assertIn("envoy) make prepare-envoy-runtime ;;", preparation)
        self.assertIn("traefik) make prepare-traefik-runtime ;;", preparation)
        self.assertIn("lighttpd) ALLOW_RUNTIME_BUILDS=1 make prepare-lighttpd-runtime ;;", preparation)
        self.assertNotIn("apache|haproxy", preparation)
        self.assertNotIn("RUNTIME_COMPONENT_TARGET=all", preparation)
        self.assertNotIn("RUNTIME_COMPONENT_TARGET: ${{", self.source)

    def test_runtime_is_connector_scoped_and_uses_closed_literal_routes(self) -> None:
        runtime = self.source.split("      - name: Run connector-isolated MRTS host runtime\n", 1)[1].split(
            "      - name: Upload isolated runtime evidence\n", 1
        )[0]
        self.assertIn("id: runtime", runtime)
        self.assertIn('case "$CONNECTOR" in', runtime)
        for connector in ("apache", "envoy", "haproxy", "traefik", "lighttpd"):
            self.assertIn(f"--connector {connector}", runtime)
        self.assertIn("ci/runtime/lifecycle/run-no-crs-with-mrts-target.py", runtime)
        self.assertIn("--execute-stage", runtime)
        self.assertIn('--parent-root "$GITHUB_WORKSPACE"', runtime)
        self.assertIn('--framework-root "$FRAMEWORK_ROOT"', runtime)
        self.assertIn('--runtime-root "$RUNTIME_ROOT"', runtime)
        self.assertNotIn('--connector "$CONNECTOR"', runtime)
        self.assertNotIn('CONNECTOR="$CONNECTOR"', runtime)
        traefik_runtime = runtime.split("            traefik)\n", 1)[1].split(
            "            lighttpd)\n", 1
        )[0]
        self.assertIn(
            "TMPDIR=/tmp ./.venv/bin/python ci/runtime/lifecycle/run-no-crs-with-mrts-target.py",
            traefik_runtime,
        )
        self.assertEqual(runtime.count("TMPDIR=/tmp ./.venv/bin/python"), 1)
        self.assertEqual(
            runtime.count("./.venv/bin/python ci/runtime/lifecycle/run-no-crs-with-mrts-target.py"),
            5,
        )
        self.assertNotIn("full-matrix-single-job-runtime", runtime)

    def test_summary_reports_each_connector_job_without_reading_raw_evidence(self) -> None:
        summary = self.source.split(
            "      - name: Write connector-isolated MRTS runtime overview\n", 1
        )[1]
        self.assertIn("if: always()", summary)
        self.assertIn(
            'python3 ci/runtime/lifecycle/summarize-no-crs-with-mrts-workflow.py --connector "$CONNECTOR"',
            summary,
        )
        self.assertNotIn("--summary-file", summary)
        for environment_name, step_id in (
            ("CHECKOUT_OUTCOME", "checkout"),
            ("SETUP_PYTHON_OUTCOME", "setup-python"),
            ("SETUP_GO_OUTCOME", "setup-go"),
            ("VERIFY_PYTHON_OUTCOME", "verify-python"),
            ("VERIFY_GO_OUTCOME", "verify-go"),
            ("SNAPSHOT_GO_OUTCOME", "snapshot-go-provenance"),
            ("VERIFY_CELL_OUTCOME", "verify-runtime-cell"),
            ("PREPARE_RUNTIME_OUTCOME", "prepare-runtime"),
            ("RUNTIME_OUTCOME", "runtime"),
            ("UPLOAD_EVIDENCE_OUTCOME", "upload-runtime-evidence"),
        ):
            self.assertIn(f"{environment_name}: ${{{{ steps.{step_id}.outcome }}}}", summary)
        self.assertLess(
            self.source.index("      - name: Upload isolated runtime evidence\n"),
            self.source.index("      - name: Write connector-isolated MRTS runtime overview\n"),
        )

    def test_workflow_security_contract(self) -> None:
        self.assertIn("pull_request:", self.source)
        self.assertIn("workflow_dispatch:", self.source)
        self.assertNotIn("pull_request_target", self.source)
        self.assertIn("permissions:\n  contents: read", self.source)
        self.assertNotIn("permissions: write", self.source)
        self.assertNotIn("secrets:", self.source)
        self.assertNotIn("continue-on-error", self.source)
        self.assertNotIn("|| true", self.source)
        self.assertNotIn("exit 0", self.source)
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
        snapshot = self.source.split("      - name: Snapshot verified setup-Go binary provenance\n", 1)[1].split(
            "      - name: Verify closed no-CRS with-MRTS matrix row\n", 1
        )[0]
        self.assertIn("id: snapshot-go-provenance", snapshot)
        self.assertIn("matrix.connector == 'envoy'", snapshot)
        self.assertIn("matrix.connector == 'traefik'", snapshot)
        self.assertNotIn("matrix.connector == 'lighttpd'", snapshot)
        self.assertNotIn("matrix.connector == 'apache'", snapshot)
        self.assertNotIn("matrix.connector == 'haproxy'", snapshot)
        setup_go = self.source.split("      - name: Set up Go\n", 1)[1].split(
            "      - name: Verify Python interpreter contract\n", 1
        )[0]
        verify_go = self.source.split(
            "      - name: Verify Go version contract without acquisition\n", 1
        )[1].split("      - name: Snapshot verified setup-Go binary provenance\n", 1)[0]
        for block in (setup_go, verify_go, snapshot):
            self.assertIn("matrix.connector == 'envoy'", block)
            self.assertIn("matrix.connector == 'traefik'", block)
            self.assertNotIn("matrix.connector == 'lighttpd'", block)
            self.assertNotIn("matrix.connector == 'apache'", block)
            self.assertNotIn("matrix.connector == 'haproxy'", block)
        self.assertIn('go_path="$(command -v go)"', snapshot)
        self.assertIn("/opt/hostedtoolcache/go/*/bin/go", snapshot)
        self.assertIn('canonical_go_path="$(realpath -e -- "$go_path")"', snapshot)
        self.assertIn('go_sha256="$(sha256sum -- "$go_path" | awk \'{print $1}\')"', snapshot)
        self.assertIn("printf 'path=%s\\nsha256=%s\\n'", snapshot)
        runtime = self.source.split("      - name: Run connector-isolated MRTS host runtime\n", 1)[1].split(
            "      - name: Upload isolated runtime evidence\n", 1
        )[0]
        target_go = runtime.split('case "$CONNECTOR" in', 1)[1].split('case "$CONNECTOR" in', 1)[0]
        self.assertIn("envoy|traefik)", target_go)
        self.assertIn("apache|haproxy|lighttpd) ;;", target_go)
        self.assertIn("SNAPSHOT_GO_BINARY: ${{ steps.snapshot-go-provenance.outputs.path }}", runtime)
        self.assertIn(
            "SNAPSHOT_GO_BINARY_SHA256: ${{ steps.snapshot-go-provenance.outputs.sha256 }}", runtime
        )
        self.assertIn('MRTS_WORKFLOW_GO_BINARY="${SNAPSHOT_GO_BINARY}"', target_go)
        self.assertIn('MRTS_WORKFLOW_GO_BINARY_SHA256="${SNAPSHOT_GO_BINARY_SHA256}"', target_go)
        self.assertNotIn("${{ steps.snapshot-go-provenance.outputs.", target_go)
        self.assertNotIn("GO: /usr/local/go/bin/go", self.source)

    def test_paths_are_run_and_attempt_and_connector_scoped(self) -> None:
        self.assertIn("${{ github.run_id }}-${{ github.run_attempt }}/${{ matrix.connector }}", self.source)
        self.assertIn("RUNTIME_ROOT:", self.source)
        self.assertIn("name: no-crs-with-mrts-${{ matrix.connector }}-${{ github.run_id }}-${{ github.run_attempt }}", self.source)
        self.assertNotIn("${{ env.RUNTIME_ROOT }}", self.source)
        for runtime_path in (
            "BUILD_ROOT:",
            "SOURCE_ROOT:",
            "TMP_ROOT:",
            "LOG_ROOT:",
            "VERIFIED_RUN_ROOT:",
        ):
            self.assertIn(
                f"{runtime_path} ${{{{ runner.temp }}}}/ModSecurity-conector-no-crs-with-mrts/"
                "${{ github.run_id }}-${{ github.run_attempt }}/${{ matrix.connector }}",
                self.source,
            )


if __name__ == "__main__":
    unittest.main()
