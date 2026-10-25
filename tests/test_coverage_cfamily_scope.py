"""Offline CFamily codecs/classification using explicitly SYNTHETIC observations.

No compiler or measured Parent coverage is produced. Synthetic line counts only
exercise parsers against ordinary private fixtures or existing source bytes.
"""
from __future__ import annotations

import hashlib
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from ci.lib.active_coverage import _gcov_source_lines
from ci.lib.sonar_source_roles import is_test_source

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "coverage_cfamily_scope_collector", ROOT / "ci/tools/collect-active-coverage.py")
assert SPEC is not None and SPEC.loader is not None
COLLECTOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(COLLECTOR)
# Deliberately independent of the implementation's shared suffix constant.
SUFFIXES = (".c", ".cc", ".cpp", ".cxx", ".h", ".hpp", ".hh", ".hxx")


class CoverageCFamilyScopeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(
            prefix="synthetic-cfamily-codec-fixtures-", dir=os.environ["RUNNER_TEMP"])
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "synthetic").mkdir(mode=0o700)
        for suffix in SUFFIXES:
            (self.root / ("synthetic/observed" + suffix)).write_text(
                "/* SYNTHETIC offline codec fixture; never compiled or published. */\n",
                encoding="utf-8")

    @staticmethod
    def synthetic_gcov(path):
        return {"synthetic_codec_fixture": True, "files": [
            {"file": str(path), "lines": [{"line_number": 1, "count": 1}]}]}

    def test_gcov_codec_retains_all_cfamily_suffixes(self):
        for suffix in SUFFIXES:
            with self.subTest(suffix=suffix):
                relative = "synthetic/observed" + suffix
                observed = {}
                _gcov_source_lines(self.synthetic_gcov(self.root / relative), self.root, observed)
                self.assertEqual(observed, {relative: {1: 1}})

    def test_snapshot_binds_all_cfamily_suffixes(self):
        for suffix in SUFFIXES:
            with self.subTest(suffix=suffix):
                relative = "synthetic/observed" + suffix
                listing = (relative + "\0").encode("utf-8")
                with patch.object(COLLECTOR, "ROOT", self.root), patch.object(
                        COLLECTOR.subprocess, "check_output", return_value=listing) as git_listing:
                    snapshot = COLLECTOR.source_snapshot()
                git_listing.assert_called_once_with(
                    ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
                    cwd=self.root)
                expected = hashlib.sha256((self.root / relative).read_bytes()).hexdigest()
                self.assertEqual(snapshot, {relative: expected})

    def test_actual_native_fixture_paths_remain_main(self):
        # Counts remain SYNTHETIC codec inputs even though paths bind real source.
        paths = (
            "tests/active_header_case.c",
            "ci/checks/common/http_authorization_service_timeout_smoke.c",
            "fuzz/common_http_headers_fuzz.c",
        )
        for relative in paths:
            with self.subTest(path=relative):
                self.assertFalse(is_test_source(relative))
                observed = {}
                _gcov_source_lines(self.synthetic_gcov(ROOT / relative), ROOT, observed)
                self.assertEqual(observed, {relative: {1: 1}})


if os.environ.get("ON_DEMAND_TESTS") != "1":
    def load_tests(loader, standard_tests, pattern):
        from ci.lib.active_test_inventory import module_load_tests
        return module_load_tests(loader, standard_tests, pattern)


if __name__ == "__main__":
    unittest.main()
