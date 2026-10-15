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


class CurrentSourceCopyControls(CaptureSourceControls):
    def setUp(self):
        super().setUp()
        # Binary and executable files outside the capture target must also bind.
        self.extra = self.copy / "fixture.bin"
        self.extra.write_bytes(b"\0exact export bytes\xff")
        self.extra.chmod(493)
        self.revision = "a" * 40
        self.snapshot = {"format": "i12-source-export-manifest-v1",
            "source_revision": self.revision, "git_tree": "b" * 40,
            "files": {"module.c": {"mode": 420, "sha256": CAPTURE.digest(self.original)},
                      "fixture.bin": {"mode": 493, "sha256": CAPTURE.digest(self.extra.read_bytes())}},
            "gitlinks": {"modules/example": "c" * 40}}
        (self.copy / "modules/example").mkdir(parents=True)
        self.freeze()

    def freeze(self):
        data = json.dumps(self.snapshot).encode()
        (self.copy / CAPTURE.SNAPSHOT).write_bytes(data)
        marker = {"format": "i12-disposable-source-copy-v2", "path": str(self.copy),
            "disposable": True, "source_revision": self.revision,
            "snapshot_manifest": CAPTURE.SNAPSHOT,
            "snapshot_manifest_sha256": CAPTURE.digest(data)}
        (self.copy / CAPTURE.MARKER).write_text(json.dumps(marker))

    def test_exact_application_and_no_capture_execution(self):
        result = self.apply()
        self.assertEqual(self.observed, (self.copy / "module.c").read_bytes())
        self.assertEqual(result["source_revision"], self.revision)
        self.assertEqual(result["delivery_product_baseline"], "8" * 40)
        self.assertEqual(result["source_git_tree"], "b" * 40)
        self.assertEqual(result["snapshot_file_count"], 2)
        self.assertEqual(result["snapshot_gitlinks"], self.snapshot["gitlinks"])
        self.assertEqual(result["snapshot_manifest_sha256"], CAPTURE.digest((self.copy / CAPTURE.SNAPSHOT).read_bytes()))
        self.assertFalse(result["runtime_qualified"])

    def test_bad_revision_format_refused(self):
        for revision in ("a" * 39, "A" * 40, "g" * 40, 40, None):
            with self.subTest(revision=revision):
                self.revision = revision
                self.snapshot["source_revision"] = revision
                self.freeze()
                self.assert_refused_unchanged()

    def test_snapshot_revision_mismatch_refused(self):
        self.snapshot["source_revision"] = "d" * 40
        self.freeze()
        self.assert_refused_unchanged()

    def test_snapshot_hash_tampering_refused(self):
        with (self.copy / CAPTURE.SNAPSHOT).open("a") as output:
            output.write(" ")
        self.assert_refused_unchanged()

    def test_marker_schema_and_manifest_pointer_refused(self):
        self.freeze()
        original = json.loads((self.copy / CAPTURE.MARKER).read_text())
        variants = ({**original, "extra": True}, {**original, "disposable": 1},
                    {**original, "snapshot_manifest": "../manifest.json"},
                    {**original, "snapshot_manifest_sha256": "F" * 64})
        for marker in variants:
            with self.subTest(marker=marker):
                (self.copy / CAPTURE.MARKER).write_text(json.dumps(marker))
                self.assert_refused_unchanged()

    def test_snapshot_schema_and_duplicate_fields_refused(self):
        self.snapshot["extra"] = True
        self.freeze()
        self.assert_refused_unchanged()
        del self.snapshot["extra"]
        self.freeze()
        marker = json.loads((self.copy / CAPTURE.MARKER).read_text())
        data = json.dumps(self.snapshot).replace('"git_tree":', '"git_tree": "e' + 'e' * 39 + '", "git_tree":').encode()
        (self.copy / CAPTURE.SNAPSHOT).write_bytes(data)
        marker["snapshot_manifest_sha256"] = CAPTURE.digest(data)
        (self.copy / CAPTURE.MARKER).write_text(json.dumps(marker))
        self.assert_refused_unchanged()

    def test_marker_duplicate_fields_refused(self):
        data = (self.copy / CAPTURE.MARKER).read_text()
        (self.copy / CAPTURE.MARKER).write_text(data.replace('"disposable":', '"disposable": false, "disposable":'))
        self.assert_refused_unchanged()

    def test_unselected_export_hash_and_mode_tampering_refused(self):
        original = self.extra.read_bytes()
        self.extra.write_bytes(b"different")
        self.assert_refused_unchanged()
        self.extra.write_bytes(original)
        self.extra.chmod(420)
        self.assert_refused_unchanged()

    def test_missing_unselected_export_file_refused(self):
        self.extra.unlink()
        self.assert_refused_unchanged()

    def test_extra_export_file_and_directory_refused(self):
        extra = self.copy / "unlisted.txt"
        extra.write_bytes(b"unlisted")
        self.assert_refused_unchanged()
        extra.unlink()
        extra.mkdir()
        self.assert_refused_unchanged()

    def test_unselected_hardlink_refused(self):
        self.extra.unlink()
        os.link(self.repo / "module.c", self.extra)
        self.assert_refused_unchanged()
        self.assertEqual(self.original, (self.repo / "module.c").read_bytes())

    def test_unselected_symlink_refused(self):
        self.extra.unlink()
        self.extra.symlink_to(self.repo / "module.c")
        self.assert_refused_unchanged()

    def test_fifo_object_refused_without_reading(self):
        os.mkfifo(self.copy / "unexpected.pipe")
        self.assert_refused_unchanged()

    def test_gitlink_content_and_nested_inventory_refused(self):
        (self.copy / "modules/example/foreign").write_text("not Parent export")
        self.assert_refused_unchanged()
        (self.copy / "modules/example/foreign").unlink()
        self.snapshot["gitlinks"]["modules/example/nested"] = "d" * 40
        self.freeze()
        self.assert_refused_unchanged()

    def test_inventory_invalid_entries_refused(self):
        original = dict(self.snapshot["files"]["fixture.bin"])
        for entry in ({**original, "mode": 511}, {**original, "mode": True},
                      {**original, "sha256": "A" * 64}, {**original, "extra": True}):
            with self.subTest(entry=entry):
                self.snapshot["files"]["fixture.bin"] = entry
                self.freeze()
                self.assert_refused_unchanged()

    def test_missing_gitlink_directory_is_allowed_but_contents_are_not(self):
        (self.copy / "modules/example").rmdir()
        (self.copy / "modules").rmdir()
        result = self.apply()
        self.assertEqual(result["snapshot_gitlinks"], self.snapshot["gitlinks"])

    def test_inventory_path_escape_and_git_metadata_refused(self):
        original = self.snapshot["files"].pop("fixture.bin")
        for name in ("../fixture.bin", "nested/.git/config", "/absolute.c"):
            with self.subTest(name=name):
                self.snapshot["files"][name] = original
                self.freeze()
                self.assert_refused_unchanged()
                del self.snapshot["files"][name]

    def test_wrong_tree_identity_and_reserved_inventory_object_refused(self):
        self.snapshot["git_tree"] = "b" * 39
        self.freeze()
        self.assert_refused_unchanged()
        self.snapshot["git_tree"] = "b" * 40
        self.snapshot["files"][CAPTURE.MARKER] = {"mode": 420, "sha256": "0" * 64}
        self.freeze()
        self.assert_refused_unchanged()

    def test_selected_base_checked_even_with_valid_complete_export(self):
        changed = b"different but frozen source\n"
        (self.copy / "module.c").write_bytes(changed)
        self.snapshot["files"]["module.c"]["sha256"] = CAPTURE.digest(changed)
        self.freeze()
        self.assert_refused_unchanged()


if __name__ == "__main__":
    unittest.main()
