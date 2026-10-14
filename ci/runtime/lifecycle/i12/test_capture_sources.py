"""Focused ownership/base/patch negative controls; no capture programs run."""
import difflib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("capture_sources", Path(__file__).with_name("capture_sources.py"))
CAPTURE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CAPTURE)
TEST_ROOT = Path(os.environ.get("I12_TEST_ROOT", "/var/tmp/codex/ModSecurity-conector"))


class CaptureSourceControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="unit-", dir=TEST_ROOT)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.bundle, self.repo, self.copy = (self.root / name for name in ("bundle", "repository", "copy"))
        for directory in (self.bundle, self.repo, self.copy):
            directory.mkdir()
        self.original = b"int module(void) {\n    return 0;\n}\n"
        self.observed = b"int module(void) {\n    record_actual_call();\n    return 0;\n}\n"
        (self.repo / "module.c").write_bytes(self.original)
        (self.copy / "module.c").write_bytes(self.original)
        before, after = map(CAPTURE.digest, (self.original, self.observed))
        patch = "".join(difflib.unified_diff(self.original.decode().splitlines(keepends=True), self.observed.decode().splitlines(keepends=True), fromfile="a/payload", tofile="b/payload")).encode()
        (self.bundle / "capture.patch").write_bytes(patch)
        client = b"raise RuntimeError('capture source must not execute')\n"
        (self.bundle / "client.py").write_bytes(client)
        identity = CAPTURE.digest(client)
        self.manifest = {"delivery_product_baseline": "8" * 40, "authorized_storage_root": str(self.root),
            "objects": {before: {"kind": "repository", "path": "module.c"},
                after: {"kind": "delta", "base": before, "patch": "capture.patch", "patch_sha256": CAPTURE.digest(patch)},
                identity: {"kind": "text", "file": "client.py"}},
            "profiles": {"selected": {"source_targets": {"module.c": {"before_sha256": before, "sha256": after}},
                "capture_files": {"client.py": {"sha256": identity}}}}}
        self.save_manifest()
        self.marker()

    def save_manifest(self):
        (self.bundle / "manifest.json").write_text(json.dumps(self.manifest))

    def marker(self):
        (self.copy / CAPTURE.MARKER).write_text(json.dumps({"format": "i12-disposable-source-copy-v1", "path": str(self.copy), "disposable": True, "parent_sha": "8" * 40}))

    def apply(self):
        return CAPTURE.apply(CAPTURE.Registry(self.bundle, self.repo), "selected", self.copy)

    def assert_refused_unchanged(self):
        before = (self.copy / "module.c").read_bytes()
        with self.assertRaises((ValueError, OSError)):
            self.apply()
        self.assertEqual(before, (self.copy / "module.c").read_bytes())
        self.assertFalse((self.copy / ".i12-capture").exists())

    def test_exact_application_and_no_capture_execution(self):
        result = self.apply()
        self.assertEqual(self.observed, (self.copy / "module.c").read_bytes())
        self.assertEqual((self.bundle / "client.py").read_bytes(), (self.copy / ".i12-capture/selected/client.py").read_bytes())
        self.assertFalse(result["runtime_qualified"])

    def test_existing_receipt_refused_before_source_writes(self):
        receipt = self.copy / "i12-source-application-receipt.json"
        original = b'{"retained_original_receipt": true}\n'
        receipt.write_bytes(original)
        self.assert_refused_unchanged()
        self.assertEqual(original, receipt.read_bytes())

    def test_hardlinked_receipt_refused_before_source_or_foreign_writes(self):
        foreign = self.root / "foreign-evidence.json"
        original = b'{"retained_foreign_evidence": true}\n'
        foreign.write_bytes(original)
        receipt = self.copy / "i12-source-application-receipt.json"
        os.link(foreign, receipt)
        self.assert_refused_unchanged()
        self.assertEqual(original, foreign.read_bytes())
        self.assertEqual(original, receipt.read_bytes())

    def test_receipt_directory_refused_before_source_writes(self):
        receipt = self.copy / "i12-source-application-receipt.json"
        receipt.mkdir()
        retained = receipt / "retained.txt"
        original = b"existing directory contents\n"
        retained.write_bytes(original)
        self.assert_refused_unchanged()
        self.assertTrue(receipt.is_dir())
        self.assertEqual(original, retained.read_bytes())

    def test_marker_missing_or_wrong_identity(self):
        (self.copy / CAPTURE.MARKER).unlink()
        self.assert_refused_unchanged()
        self.marker()
        value = json.loads((self.copy / CAPTURE.MARKER).read_text())
        value["path"] = str(self.repo)
        (self.copy / CAPTURE.MARKER).write_text(json.dumps(value))
        self.assert_refused_unchanged()

    def test_root_or_nested_git_refused(self):
        for relative in (".git", "nested/.git"):
            path = self.copy / relative
            path.parent.mkdir(exist_ok=True)
            path.write_text("gitdir: protected-checkout")
            self.assert_refused_unchanged()
            path.unlink()

    def test_symlink_in_copy_refused(self):
        (self.copy / "alias").symlink_to(self.repo, target_is_directory=True)
        self.assert_refused_unchanged()

    def test_hardlinked_product_file_refused(self):
        (self.copy / "module.c").unlink()
        os.link(self.repo / "module.c", self.copy / "module.c")
        self.assert_refused_unchanged()
        self.assertEqual(self.original, (self.repo / "module.c").read_bytes())

    def test_later_bad_base_refused_before_first_write(self):
        self.manifest["profiles"]["selected"]["source_targets"]["unexpected.c"] = {"before_sha256": "0" * 64, "sha256": CAPTURE.digest(self.observed)}
        (self.copy / "unexpected.c").write_text("wrong source")
        self.save_manifest()
        self.assert_refused_unchanged()

    def test_modified_delta_refused(self):
        (self.bundle / "capture.patch").write_text("not the sealed delta")
        self.assert_refused_unchanged()

    def test_context_patch_has_no_fuzz(self):
        with self.assertRaises(ValueError):
            CAPTURE.exact_patch(self.original.replace(b"return 0", b"return 1"), (self.bundle / "capture.patch").read_bytes())

    def test_zero_context_patch_matches_standard_offsets(self):
        patch = "".join(difflib.unified_diff(self.original.decode().splitlines(keepends=True), self.observed.decode().splitlines(keepends=True), fromfile="a/payload", tofile="b/payload", n=0)).encode()
        self.assertEqual(self.observed, CAPTURE.exact_patch(self.original, patch))

    def test_lossless_source_lines_preserve_original_whitespace(self):
        original = b"# retained original line \n"
        identity = CAPTURE.digest(original)
        (self.bundle / "original.lines.json").write_text(json.dumps(original.decode().splitlines(keepends=True)))
        self.manifest["objects"][identity] = {"kind": "text_lines", "file": "original.lines.json"}
        self.save_manifest()
        self.assertEqual(original, CAPTURE.Registry(self.bundle, self.repo).content(identity))

    def test_escape_path_refused(self):
        self.manifest["profiles"]["selected"]["capture_files"] = {"../escaped.py": next(iter(self.manifest["profiles"]["selected"]["capture_files"].values()))}
        self.save_manifest()
        self.assert_refused_unchanged()
        self.assertFalse((self.copy / "escaped.py").exists())

    def test_non_directory_capture_parent_refused_before_product_write(self):
        (self.copy / ".i12-capture").write_text("existing user file")
        with self.assertRaises(ValueError):
            self.apply()
        self.assertEqual(self.original, (self.copy / "module.c").read_bytes())


if __name__ == "__main__":
    unittest.main()
