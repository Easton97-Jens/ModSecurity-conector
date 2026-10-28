"""Compile the productive Traefik dispatcher with controlled Common error seams."""

from __future__ import annotations

import ctypes.util
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class TraefikI10DispatcherTest(unittest.TestCase):
    def test_technical_failure_and_terminal_reentry(self) -> None:
        compiler = shutil.which("cc")
        if compiler is None:
            self.skipTest("requires a C compiler")
        if ctypes.util.find_library("modsecurity") is None:
            self.skipTest("requires installed libmodsecurity to link retained Common runtime")

        common_sources = sorted((ROOT / "common" / "src").glob("*.c"))
        runtime_sources = sorted((ROOT / "common" / "runtime").glob("*.c"))
        with tempfile.TemporaryDirectory(
            prefix="traefik-i10-dispatcher-",
            dir=os.environ.get("TMPDIR"),
        ) as temporary_directory:
            binary = Path(temporary_directory) / "dispatcher"
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
                    str(ROOT / "tests" / "traefik_i10_dispatcher_test.c"),
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
            config_paths = []
            example = (ROOT / "connectors/traefik/config/traefik-engine-service.conf").read_text()
            example = example.replace("rules_file=common/rules/modsecurity_targeted_smoke.conf", "rules_file=" + str(ROOT / "common/rules/modsecurity_targeted_smoke.conf"))
            for mode in ("off", "safe", "strict"):
                config_path = Path(temporary_directory) / (mode + ".conf")
                config_path.write_text(example.replace("phase4_mode=off", "phase4_mode=" + mode))
                config_paths.append(str(config_path))
            run_result = subprocess.run(
                [str(binary), *config_paths],
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=10.0,
                check=False,
            )
            self.assertEqual(run_result.returncode, 0, run_result.stderr)



# Parent default discovery uses the one admitted active-case inventory.
if __import__("os").environ.get("ON_DEMAND_TESTS") != "1":
    def load_tests(loader, standard_tests, pattern):
        from ci.lib.active_test_inventory import module_load_tests
        return module_load_tests(loader, standard_tests, pattern)

if __name__ == "__main__":
    unittest.main()
