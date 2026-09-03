"""Compile and execute deterministic Traefik worker ownership regressions."""

from __future__ import annotations

import ctypes.util
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class TraefikEngineWorkerLifecycleTest(unittest.TestCase):
    def test_worker_cap_rollback_and_fd_reuse_shutdown_race(self) -> None:
        compiler = shutil.which("cc")
        if compiler is None:
            self.skipTest("requires a C compiler")
        if ctypes.util.find_library("modsecurity") is None:
            self.skipTest("requires libmodsecurity for the linked worker fixture")

        common_sources = sorted((ROOT / "common" / "src").glob("*.c"))
        runtime_sources = sorted((ROOT / "common" / "runtime").glob("*.c"))
        with tempfile.TemporaryDirectory(
            prefix="traefik-engine-worker-lifecycle-",
            dir=os.environ.get("TMPDIR"),
        ) as temporary_directory:
            binary = Path(temporary_directory) / "worker-lifecycle"
            compile_result = subprocess.run(
                [
                    compiler,
                    "-std=c17",
                    "-Wall",
                    "-Wextra",
                    "-Werror",
                    "-ffunction-sections",
                    "-fdata-sections",
                    "-I",
                    str(ROOT),
                    "-I",
                    str(ROOT / "common" / "include"),
                    "-I",
                    str(ROOT / "common" / "runtime"),
                    "-I",
                    str(ROOT / "connectors" / "traefik"),
                    "-I",
                    str(ROOT / "connectors" / "traefik" / "src"),
                    str(ROOT / "tests" / "traefik_engine_worker_lifecycle_test.c"),
                    *(str(source) for source in common_sources),
                    *(str(source) for source in runtime_sources),
                    str(ROOT / "connectors" / "profile_registry.c"),
                    "-Wl,--gc-sections",
                    "-lmodsecurity",
                    "-pthread",
                    "-o",
                    str(binary),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(compile_result.returncode, 0, compile_result.stderr)
            run_result = subprocess.run(
                [str(binary)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=10.0,
                check=False,
            )
            self.assertEqual(run_result.returncode, 0, run_result.stderr)


if __name__ == "__main__":
    unittest.main()
