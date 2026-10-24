"""Protect disposable source and identity boundaries of diagnostic injections."""
import hashlib
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
            self.assertEqual(receipt["input_runtime_sha256"], hashlib.sha256(original).hexdigest())
            self.assertEqual(receipt["fault_runtime_sha256"], hashlib.sha256(changed).hexdigest())
            untrusted_begin, remaining_begins = changed.decode().split(
                "int msconnector_runtime_transaction_begin_request_stream(", 1)
            self.assertIn('i12_pointer_null("headers_null"', untrusted_begin)
            self.assertIn("decision, error, 0, NULL);", untrusted_begin)
            self.assertNotIn("injected_request", remaining_begins)
            self.assertIn("decision, error, 0, provenance);", remaining_begins)
            self.assertIn("decision, error, 1, provenance);", remaining_begins)
            with self.assertRaisesRegex(ValueError, "fresh"):
                FAULTS.extend(source, HEADER)
            self.assertEqual(runtime.read_bytes(), changed)

    def test_missing_or_duplicate_current_begin_anchor_rejects_without_writes(self):
        anchor = ("    return transaction_begin_internal(runtime, request, host_request_id, out,\n"
                  "        decision, error, 0, NULL);")
        current = (ROOT / "common/runtime/msconnector_runtime.c").read_text()
        self.assertEqual(current.count(anchor), 1)
        for replacement in ("", anchor + "\n" + anchor):
            with self.subTest(anchor_count=replacement.count(anchor)):
                with tempfile.TemporaryDirectory() as temporary:
                    source = Path(temporary)
                    runtime = source / "common/runtime/msconnector_runtime.c"
                    runtime.parent.mkdir(parents=True)
                    runtime.write_text('#include "diagnostic_faults.h"\n' + current.replace(anchor, replacement))
                    original = runtime.read_bytes()
                    (source / ".i12-disposable-source-copy.json").write_text(
                        json.dumps({"disposable": True, "path": str(source)}))
                    with self.assertRaisesRegex(ValueError, "anchor missing or ambiguous"):
                        FAULTS.extend(source, HEADER)
                    self.assertEqual(runtime.read_bytes(), original)
                    self.assertFalse((source / "patched_faults.h").exists())
                    self.assertFalse((source / "diagnostic_budget_observer.h").exists())
                    self.assertFalse((source / "diagnostic_finish_observer.h").exists())

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
