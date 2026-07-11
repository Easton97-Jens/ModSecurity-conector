from __future__ import annotations

from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class MakeRuntimeDefaultsTest(unittest.TestCase):
    def test_default_tmp_root_is_below_build_root(self) -> None:
        """Standard connector targets satisfy the HAProxy host path contract."""
        with tempfile.TemporaryDirectory(prefix="make-runtime-defaults-") as temporary:
            run_root = Path(temporary) / "verified-run"
            recipe = 'print-runtime-roots: ; @printf "%s\\n%s\\n" "$(TMP_ROOT)" "$(LOG_ROOT)"'
            result = subprocess.run(
                [
                    "make",
                    "-s",
                    "--no-print-directory",
                    "--eval",
                    recipe,
                    "print-runtime-roots",
                    f"VERIFIED_RUN_ROOT={run_root}",
                ],
                cwd=ROOT,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(
                [
                    str(run_root / "build" / "tmp"),
                    str(run_root / "build" / "logs"),
                ],
                result.stdout.splitlines(),
            )


if __name__ == "__main__":
    unittest.main()
