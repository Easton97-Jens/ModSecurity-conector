"""Executable Common runtime policy evidence using genuine libModSecurity."""
from pathlib import Path
import os
import shlex
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def engine_fixture_arguments(directory, limit, action, mode, length, chunk, marker):
    if limit is None or action is None:
        raise ValueError("response fixture requires explicit SecResponseBodyLimit and SecResponseBodyLimitAction")
    if limit <= 0 or action not in ("Reject", "ProcessPartial"):
        raise ValueError("invalid explicit engine response policy")
    return [str(directory), str(limit), action, mode, str(length), str(chunk), str(marker)]


class EngineResponseLimits(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(os.environ.get("CODEX_RUN_ROOT", "/var/tmp/codex/ModSecurity-conector/runs"))
        root.mkdir(parents=True, exist_ok=True)
        cls.temp = tempfile.TemporaryDirectory(prefix="engine-response-limits-", dir=root)
        cls.addClassCleanup(cls.temp.cleanup)
        cls.directory = Path(cls.temp.name)
        cls.binary = cls.directory / "engine-limit"
        command = shlex.split(os.environ.get("CC", "cc")) + [
            "-std=c17", "-Wall", "-Wextra", "-Werror", "-I.", "-Icommon/include",
            "tests/engine_response_limit_test.c", "common/runtime/msconnector_runtime.c",
        ] + [str(p.relative_to(ROOT)) for p in sorted((ROOT / "common/src").glob("*.c"))] + [
            "connectors/profile_registry.c", "-lmodsecurity", "-pthread", "-o", str(cls.binary)]
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=90)
        if result.returncode:
            raise AssertionError("real libModSecurity test compilation failed:\n" + result.stdout + result.stderr)

    def run_case(self, limit, action, mode, length, chunk, marker):
        with tempfile.TemporaryDirectory(dir=self.directory) as directory:
            args = engine_fixture_arguments(directory, limit, action, mode, length, chunk, marker)
            result = subprocess.run([str(self.binary)] + args, capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            print(result.stdout.strip())

    def test_boundaries_actions_chunking_and_modes(self):
        for limit in (128, 1024):
            for action in ("Reject", "ProcessPartial"):
                for mode in ("off", "safe", "strict"):
                    for delta in (-1, 0, 1):
                        for chunk in (17, 65536):
                            with self.subTest(limit=limit, action=action, mode=mode, delta=delta, chunk=chunk):
                                self.run_case(limit, action, mode, limit + delta, chunk, 0)

    def test_engine_partial_prefix_excludes_marker_after_limit(self):
        for mode in ("off", "safe", "strict"):
            self.run_case(128, "ProcessPartial", mode, 256, 17, 160)

    def test_marker_after_old_one_megabyte_connector_default(self):
        for mode in ("off", "safe", "strict"):
            self.run_case(3 * 1024 * 1024, "Reject", mode, 2 * 1024 * 1024, 65536, 1536 * 1024)
            self.run_case(1536 * 1024, "ProcessPartial", mode, 2 * 1024 * 1024, 65536, 1200 * 1024)

    def test_product_configuration_allows_omitted_engine_directives_without_inspection(self):
        result = subprocess.run([str(self.binary), "--config-only", str(self.directory)],
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("no response inspection", result.stdout)

    def test_missing_policy_parameters_fail_readably(self):
        for limit, action in ((None, "Reject"), (128, None)):
            with self.assertRaisesRegex(ValueError, "requires explicit"):
                engine_fixture_arguments(self.directory, limit, action, "safe", 128, 17, 0)
        result = subprocess.run([str(self.binary)], capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 2)
        self.assertIn("required:", result.stderr)

if __name__ == "__main__":
    unittest.main()
