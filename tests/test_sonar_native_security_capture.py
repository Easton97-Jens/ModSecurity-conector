"""Pure negative control for the compiler invocation environment boundary."""

import importlib.util
import os
from pathlib import Path
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "sonar_native_security_capture",
    ROOT / "ci/checks/analysis/sonar-native-security/capture.py")
CAPTURE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CAPTURE)


class NativeCompilerEnvironmentTest(unittest.TestCase):
    def assert_environment_rejected(self, name, value):
        with patch.dict(os.environ, {name: value}, clear=True):
            with patch.object(CAPTURE.subprocess, "run", side_effect=AssertionError("compiler must not start")):
                with self.assertRaisesRegex(ValueError, "undeclared implicit compiler environment"):
                    CAPTURE.capture("unused-compiler", [], Path("unused-capture-root"))

    def test_implicit_environment_rejected_before_compiler(self):
        self.assert_environment_rejected("CPATH", "/unit-only-unadmitted-include")

    def test_clang_override_environment_rejected_before_compiler(self):
        self.assert_environment_rejected("CCC_OVERRIDE_OPTIONS", "+-DUNIT_UNDECLARED_FLAG")


if os.environ.get("ON_DEMAND_TESTS") != "1":
    def load_tests(loader, standard_tests, pattern):
        from ci.lib.active_test_inventory import module_load_tests
        return module_load_tests(loader, standard_tests, pattern)


if __name__ == "__main__":
    unittest.main()
