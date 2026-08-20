"""Contracts for the closed no-CRS/with-MRTS shell dispatch boundary."""
from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "ci" / "runtime" / "lifecycle" / "run-remaining-connector-target.sh"


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
        ):
            self.assertIn(variable, source)

    def test_closed_values_are_readonly_before_snapshot_source(self) -> None:
        source = RUNNER.read_text(encoding="utf-8")
        self.assertIn("readonly MRTS_CLOSED_CONNECTOR_ROOT", source)
        self.assertIn("readonly MRTS_CLOSED_RUNTIME_ENV", source)
        self.assertIn("MRTS_CLOSED_STAGE=$MSCONNECTOR_MRTS_STAGE", source)
        self.assertIn("MRTS_RUNTIME_EXECUTOR_SHA256=$MRTS_CLOSED_EXECUTOR_SHA256", source)


if __name__ == "__main__":
    unittest.main()
