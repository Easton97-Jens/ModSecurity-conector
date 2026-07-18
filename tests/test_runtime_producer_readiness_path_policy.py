from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "ci" / "checks" / "evidence" / "check-runtime-producer-readiness.py"
SPEC = importlib.util.spec_from_file_location("runtime_producer_readiness", CHECKER_PATH)
assert SPEC is not None and SPEC.loader is not None
readiness = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = readiness
SPEC.loader.exec_module(readiness)


class RuntimeProducerReadinessPathPolicyTest(unittest.TestCase):
    def test_project_root_argument_cannot_authorize_system_write_path(self) -> None:
        """Readiness reporting must not trust a caller-supplied project root for writes."""
        with tempfile.TemporaryDirectory(prefix="runtime-producer-path-policy-") as temporary:
            run_root = Path(temporary) / "verified-run"
            roots = {
                "verified_run_root": run_root,
                "state_home": run_root / "state",
                "build_root": run_root / "build",
                "cache_root": run_root / "cache-v2",
                "tmp_root": run_root / "tmp",
                "log_root": run_root / "logs",
                "mrts_native_root": run_root / "build" / "mrts-native",
            }

            escaped = readiness.check_safe_path(
                Path("/etc/evidence-escape"),
                "BUILD_ROOT",
                roots,
                Path("/"),
                Path("/"),
            )
            self.assertEqual("BLOCKED", escaped["status"])
            self.assertIn("system write path", escaped["notes"])

            control = readiness.check_safe_path(
                run_root / "build" / "apache",
                "BUILD_ROOT",
                roots,
                Path("/"),
                Path("/"),
            )
            self.assertEqual("PASS", control["status"])


if __name__ == "__main__":
    unittest.main()
