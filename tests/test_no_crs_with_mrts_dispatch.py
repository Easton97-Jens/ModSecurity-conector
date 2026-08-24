"""Contracts for the closed no-CRS/with-MRTS shell dispatch boundary."""
from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "ci" / "runtime" / "lifecycle" / "run-remaining-connector-target.sh"
STAGE = ROOT / "ci" / "runtime" / "lifecycle" / "run-connector-stage.sh"
ENVOY = ROOT / "connectors" / "envoy" / "harness" / "run_envoy_ext_proc_runtime.sh"


class NoCrsWithMrtsDispatchContractTests(unittest.TestCase):
    def test_snapshot_load_reasserts_closed_toolchain_environment(self) -> None:
        source = RUNNER.read_text(encoding="utf-8")
        load_index = source.index('. "$runtime_env"')
        reassert_index = source.index("reassert_mrts_closed_environment", load_index)
        self.assertGreater(reassert_index, load_index)
        for variable in (
            "GO=$MRTS_GO_BINARY",
            "MRTS_GO_BINARY=$MRTS_CLOSED_GO_BINARY",
            "GOTOOLCHAIN=local",
            "GOENV=off",
            "PYTHON=$MRTS_CLOSED_PYTHON",
            "PYTHON_BIN=$MRTS_CLOSED_PYTHON",
            "HOME=$MRTS_CLOSED_HOME",
            "GOPATH=$MRTS_CLOSED_GOPATH",
            "GOMODCACHE=$MRTS_CLOSED_GOMODCACHE",
            "GOCACHE=$MRTS_CLOSED_GOCACHE",
            "GOTMPDIR=$MRTS_CLOSED_GOTMPDIR",
            "TMPDIR=$MRTS_CLOSED_TMPDIR",
            "ALLOW_RUNTIME_DOWNLOADS=$MRTS_CLOSED_ALLOW_RUNTIME_DOWNLOADS",
            "ALLOW_RUNTIME_BUILDS=$MRTS_CLOSED_ALLOW_RUNTIME_BUILDS",
        ):
            self.assertIn(variable, source)

    def test_direct_target_builds_resolve_literal_go_to_the_sealed_binary(self) -> None:
        source = RUNNER.read_text(encoding="utf-8")
        self.assertIn("set_mrts_go_path()", source)
        self.assertIn("MRTS_GO_BIN_DIR=${candidate%/go}", source)
        self.assertIn("MRTS Go binary path contains a PATH separator", source)
        self.assertIn(
            "PATH=$MRTS_GO_BIN_DIR:/usr/local/go/bin:/usr/bin:/bin",
            source,
        )
        self.assertIn('set_mrts_go_path "$MRTS_GO_BINARY" || exit $?', source)
        self.assertIn('set_mrts_go_path "$MRTS_GO_BINARY" || return $?', source)
        self.assertIn('[ "$PATH" = "$MRTS_CLOSED_PATH" ]', source)

    def test_closed_values_are_readonly_before_snapshot_source(self) -> None:
        source = RUNNER.read_text(encoding="utf-8")
        self.assertIn("readonly MRTS_CLOSED_CONNECTOR_ROOT", source)
        self.assertIn("readonly MRTS_CLOSED_RUNTIME_ENV", source)
        self.assertIn("MRTS_CLOSED_STAGE=$MSCONNECTOR_MRTS_STAGE", source)
        self.assertIn("MRTS_CLOSED_GO_BINARY=$MRTS_GO_BINARY", source)
        self.assertIn("MRTS_CLOSED_GO_SHA256=$MRTS_GO_BINARY_SHA256", source)
        self.assertIn("MRTS_CLOSED_GO_VERSION=$MRTS_GO_VERSION", source)
        self.assertIn("sha256sum \"$MRTS_GO_BINARY\"", source)
        self.assertIn("sha256sum \"$GO\"", source)
        stage = STAGE.read_text(encoding="utf-8")
        self.assertIn('MRTS_GO_BINARY_SHA256="${MRTS_GO_BINARY_SHA256:?MRTS_GO_BINARY_SHA256 is required}"', stage)
        self.assertIn('MRTS_GO_VERSION="${MRTS_GO_VERSION:?MRTS_GO_VERSION is required}"', stage)
        self.assertIn("MRTS_CLOSED_PLAN_SHA256=$MRTS_RUNTIME_PLAN_SHA256", source)
        self.assertIn("MRTS_RUNTIME_EXECUTOR_SHA256=$MRTS_CLOSED_EXECUTOR_SHA256", source)
        self.assertIn("MRTS_CLOSED_ALLOW_RUNTIME_DOWNLOADS=1", source)
        self.assertIn("MRTS_CLOSED_ALLOW_RUNTIME_BUILDS=1", source)

    def test_runtime_provisioning_opt_ins_are_gated_and_reasserted_as_literals(self) -> None:
        stage_source = STAGE.read_text(encoding="utf-8")
        runner_source = RUNNER.read_text(encoding="utf-8")
        for source in (stage_source, runner_source):
            self.assertIn('"${ALLOW_RUNTIME_DOWNLOADS:-}" = 1', source)
            self.assertIn('"${ALLOW_RUNTIME_BUILDS:-}" = 1', source)
        self.assertIn("env -i", stage_source)
        self.assertIn("ALLOW_RUNTIME_DOWNLOADS=1", stage_source)
        self.assertIn("ALLOW_RUNTIME_BUILDS=1", stage_source)

    def test_all_mrts_dispatch_boundaries_revalidate_the_sealed_no_crs_plan(self) -> None:
        for path in (STAGE, RUNNER, ENVOY):
            source = path.read_text(encoding="utf-8")
            self.assertIn("--validate-sealed-plan", source)
            self.assertIn("--plan-sha256", source)
            self.assertNotIn("grep -Eiq 'crs", source)

    def test_envoy_standalone_mrts_runner_defaults_connector_root_to_its_repository(self) -> None:
        source = ENVOY.read_text(encoding="utf-8")
        self.assertIn("CONNECTOR_ROOT=${CONNECTOR_ROOT:-$REPO_ROOT}", source)
        self.assertLess(
            source.index("CONNECTOR_ROOT=${CONNECTOR_ROOT:-$REPO_ROOT}"),
            source.index("sealed_plan_validator=$CONNECTOR_ROOT/"),
        )

    def test_parent_held_plan_digest_is_required_and_survives_each_shell_boundary(self) -> None:
        stage_source = STAGE.read_text(encoding="utf-8")
        runner_source = RUNNER.read_text(encoding="utf-8")
        for source in (stage_source, runner_source):
            self.assertIn("MRTS_RUNTIME_PLAN_SHA256 is required", source)
            self.assertIn("MRTS_RUNTIME_PLAN_SHA256 must be a lowercase SHA-256 digest", source)
            self.assertIn('"$MRTS_RUNTIME_PLAN_SHA256"', source)
        self.assertIn('MRTS_RUNTIME_PLAN_SHA256="$MRTS_RUNTIME_PLAN_SHA256"', stage_source)
        self.assertIn("MRTS_CLOSED_PLAN_SHA256=$MRTS_RUNTIME_PLAN_SHA256", runner_source)
        self.assertIn("MRTS_RUNTIME_PLAN_SHA256=$MRTS_CLOSED_PLAN_SHA256", runner_source)

    def test_no_crs_mrts_keeps_canonical_preamble_separate_from_mrts_load_file(self) -> None:
        source = RUNNER.read_text(encoding="utf-8")
        self.assertIn(
            "NO_CRS_RULES_FILE=$FRAMEWORK_ROOT/tests/rules/no-crs-baseline.conf",
            source,
        )
        self.assertIn("MODSECURITY_RULE_PREAMBLE_FILE=$NO_CRS_RULES_FILE", source)
        self.assertIn("MSCONNECTOR_RULES_FILE=$MRTS_LOAD_FILE", source)
        self.assertIn("RULES_FILE=$MRTS_LOAD_FILE", source)
        self.assertNotIn("MODSECURITY_RULE_PREAMBLE_FILE=$MRTS_LOAD_FILE", source)

    def test_lighttpd_mrts_route_seals_its_canonical_evidence_output(self) -> None:
        source = RUNNER.read_text(encoding="utf-8")
        lighttpd = source.split("    lighttpd)\n", 1)[1].split("    *)\n", 1)[0]
        mrts = lighttpd.split(
            'if [ "${MSCONNECTOR_MRTS_STAGE:-}" = no_crs_with_mrts ]; then\n', 1
        )[1].split("        else\n", 1)[0]
        self.assertIn("lighttpd_patched_smoke_dir=$RUNTIME_ROOT", mrts)
        self.assertIn("NO_CRS_ARTIFACT_PROFILE=full_lifecycle", mrts)
        self.assertIn(
            "FULL_LIFECYCLE_EVIDENCE_OUTPUT=$lighttpd_patched_smoke_dir/first-byte-evidence.json",
            mrts,
        )
        self.assertIn(
            "export NO_CRS_ARTIFACT_PROFILE FULL_LIFECYCLE_EVIDENCE_OUTPUT",
            mrts,
        )

    def test_python_invocation_contract_allows_only_a_final_venv_symlink(self) -> None:
        for source in (STAGE.read_text(encoding="utf-8"), RUNNER.read_text(encoding="utf-8")):
            self.assertIn("require_mrts_python_invocation()", source)
            self.assertIn('require_mrts_python_invocation "$MRTS_PYTHON_BIN" || exit 77', source)
            self.assertIn('*/../*|../*|*/..|..)', source)
            self.assertIn('symlinked parent: $candidate', source)
            self.assertNotIn('MRTS Python interpreter must not be a symlink', source)
        runner_source = RUNNER.read_text(encoding="utf-8")
        self.assertIn('require_mrts_python_invocation "$PYTHON_BIN" || {', runner_source)


if __name__ == "__main__":
    unittest.main()
