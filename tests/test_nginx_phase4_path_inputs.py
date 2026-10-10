"""PathLike adapter regression at the real strict guard, before native work."""
import importlib.util
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("path_input_phase4", ROOT / "ci/runtime/lifecycle/run-nginx-phase4-cases.py")
driver = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(driver)


class Phase4PathInputsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=os.environ["TMPDIR"])
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.binary = self.root / "binary"
        self.binary.write_bytes(b"not executed")
        self.input_path = Path(__file__)
        self.upstream = ROOT / "ci/runtime/common/nginx_phase4_upstream.py"
        self.args = SimpleNamespace(framework_root=str(ROOT), projection_parent=str(self.root),
            run_id="path-input", case_id="phase4_body_at_limit")

    def test_path_inputs_reach_projection_after_real_strict_guards(self):
        guard = driver.HOST.BASE.absolute_path
        with mock.patch.object(driver.HOST.BASE, "validate_inputs", return_value=(self.binary, self.binary, self.root / "out")), \
             mock.patch.object(driver.HOST.BASE, "absolute_path", wraps=guard) as observed, \
             mock.patch.object(driver.HOST.PROJECTION, "prepare_projection", side_effect=ValueError("controlled pre-native stop")) as prepare:
            with self.assertRaisesRegex(ValueError, "controlled pre-native stop"):
                driver.run_operation(self.args, {"rules": "SecRuleEngine On\n"}, input_path=self.input_path, upstream_path=self.upstream)
        observed.assert_any_call(os.fspath(self.input_path))
        observed.assert_any_call(os.fspath(self.upstream))
        prepare.assert_called_once()

    def test_symlink_and_arbitrary_object_are_not_coerced_or_admitted(self):
        alias = self.root / "alias"
        alias.symlink_to(self.input_path)
        for path, error in ((alias, ValueError), (object(), TypeError)):
            with self.subTest(path=path):
                with mock.patch.object(driver.HOST.BASE, "validate_inputs", return_value=(self.binary, self.binary, self.root / "out")), \
                     mock.patch.object(driver.HOST.PROJECTION, "prepare_projection") as prepare:
                    with self.assertRaises(error):
                        driver.run_operation(self.args, {}, input_path=path, upstream_path=self.upstream)
                prepare.assert_not_called()
