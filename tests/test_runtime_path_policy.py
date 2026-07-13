from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "ci" / "checks" / "security" / "check-runtime-path-policy.py"


class RuntimePathPolicyTest(unittest.TestCase):
    def test_default_policy_selftest_ignores_caller_cache_overrides(self) -> None:
        """A custom verified root must not poison the checker’s default probe."""
        with tempfile.TemporaryDirectory(prefix="runtime-path-policy-") as temporary:
            caller_root = Path(temporary) / "custom-run"
            env = {
                **os.environ,
                "VERIFIED_RUN_ROOT": str(caller_root),
                "CACHE_ROOT": str(caller_root / "cache-v2"),
                "VERIFIED_COMPONENT_CACHE": str(caller_root / "cache-v2" / "shared"),
                "BUILD_ROOT": str(caller_root / "build"),
                "TMP_ROOT": str(caller_root / "build" / "tmp"),
                "LOG_ROOT": str(caller_root / "build" / "logs"),
            }
            result = subprocess.run(
                [sys.executable, str(CHECKER)],
                cwd=ROOT,
                env=env,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
