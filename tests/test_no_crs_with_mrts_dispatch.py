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
            "GO=/usr/local/go/bin/go",
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

    def test_closed_values_are_readonly_before_snapshot_source(self) -> None:
        source = RUNNER.read_text(encoding="utf-8")
        self.assertIn("readonly MRTS_CLOSED_CONNECTOR_ROOT", source)
        self.assertIn("readonly MRTS_CLOSED_RUNTIME_ENV", source)
        self.assertIn("MRTS_CLOSED_STAGE=$MSCONNECTOR_MRTS_STAGE", source)
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
