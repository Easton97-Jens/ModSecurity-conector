"""Protect disposable source and identity boundaries of diagnostic injections."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("diagnostic_fault_capture",
    ROOT / "ci/runtime/lifecycle/i12/lighttpd/diagnostic_fault_capture.py")
FAULTS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FAULTS)
HEADER = ROOT / "ci/runtime/lifecycle/i12/lighttpd/patched_faults.h"


class DiagnosticFaultBoundaryTests(unittest.TestCase):
    def test_real_runtime_overlay_requires_fresh_marked_copy_and_preserves_input_identity(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary)
            runtime = source / "common/runtime/msconnector_runtime.c"
            runtime.parent.mkdir(parents=True)
            runtime.write_text('#include "diagnostic_faults.h"\n' +
                (ROOT / "common/runtime/msconnector_runtime.c").read_text())
            original = runtime.read_bytes()
            marker = source / ".i12-disposable-source-copy.json"
            marker.write_text(json.dumps({"disposable": True, "path": str(source)}))
            receipt = FAULTS.extend(source, HEADER)
            self.assertTrue(receipt["stripped_input_identity"])
            self.assertFalse(receipt["native_sdk_return_mutated"])
            self.assertNotEqual(runtime.read_bytes(), original)
            changed = runtime.read_bytes()
            with self.assertRaisesRegex(ValueError, "fresh"):
                FAULTS.extend(source, HEADER)
            self.assertEqual(runtime.read_bytes(), changed)

    def test_symlink_parent_is_rejected_before_touching_real_source(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            physical = root / "physical"
            physical.mkdir()
            alias = root / "alias"
            alias.symlink_to(physical, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "physical paths"):
                FAULTS.extend(alias, HEADER)
            self.assertEqual(list(physical.iterdir()), [])

    def test_marker_cannot_authorize_a_different_source_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary)
            marker = source / ".i12-disposable-source-copy.json"
            marker.write_text(json.dumps({"disposable": True, "path": str(source / "other")}))
            with self.assertRaisesRegex(ValueError, "exact marked"):
                FAULTS.extend(source, HEADER)
            self.assertEqual(list(source.iterdir()), [marker])


if __name__ == "__main__":
    unittest.main()
