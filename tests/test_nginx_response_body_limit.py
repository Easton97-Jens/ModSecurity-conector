"""Compile the exact native Engine response-limit rejection predicate."""
from __future__ import annotations

import os
from pathlib import Path
import shlex
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class NginxResponseBodyLimitTests(unittest.TestCase):
    def test_exact_signature_and_negative_controls(self) -> None:
        compiler = shlex.split(os.environ.get("CC", "cc"))
        self.assertTrue(compiler and shutil.which(compiler[0]), "C compiler is required")
        with tempfile.TemporaryDirectory(prefix="nginx-response-limit-",
                                         dir=os.environ.get("RUNNER_TEMP")) as temporary:
            for sanity in (0, 1):
                with self.subTest(sanity_checks=sanity):
                    binary = Path(temporary) / f"response-limit-{sanity}"
                    command = compiler + ["-std=c17", "-Wall", "-Wextra", "-Werror",
                                          "-pedantic-errors",
                                          f"-DMODSECURITY_SANITY_CHECKS={sanity}",
                                          "-I", str(ROOT / "common/include"),
                                          "-I", str(ROOT / "connectors/nginx/src"),
                                          str(ROOT / "tests/fixtures/nginx_response_body_limit.c"),
                                          "-o", str(binary)]
                    compiled = subprocess.run(command, capture_output=True, text=True,
                                              timeout=30, check=False)
                    self.assertEqual(compiled.returncode, 0, compiled.stderr[-6000:])
                    executed = subprocess.run([str(binary)], capture_output=True, text=True,
                                              timeout=5, check=False)
                    self.assertEqual(executed.returncode, 0, executed.stderr[-2000:])


if __name__ == "__main__":
    unittest.main()
