"""Bounded identity/overlay tests; no second native build or host claim."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


MODULE = Path(__file__).resolve().parents[1] / "ci/runtime/lifecycle/apache-i12/acceptance/build_observed_module.py"
LOADER = importlib.util.spec_from_file_location("apache_observed_module_builder", MODULE)
builder = importlib.util.module_from_spec(LOADER)
LOADER.loader.exec_module(builder)


class OverlayTests(unittest.TestCase):
    def setUp(self):
        self.texts = {
            builder.SOURCE_FILES[0]: "P1\nADD\nFINISH\n    return msconnector_transaction_contract_record_request_metadata(&msr->contract,",
            builder.SOURCE_FILES[1]: "APPEND\n    ret = apr_bucket_read(bucket, &data, &len, block);\n"
                "    if (ret != APR_SUCCESS)\n        return ret;\n"
                "    rc = apr_bucket_read(bucket, &data, &len, APR_BLOCK_READ);\n"}
        self.anchors = [{"file": name, "original": old, "replacement": new, "occurrences_required": 1}
                        for name, old, new in [(builder.SOURCE_FILES[0], "P1", "FAULT_P1"),
                        (builder.SOURCE_FILES[0], "ADD", "FAULT_ADD"),
                        (builder.SOURCE_FILES[0], "FINISH", "FAULT_FINISH"),
                        (builder.SOURCE_FILES[1], "APPEND", "FAULT_APPEND")]]

    def test_bucket_observation_precedes_actual_read_and_null_seam_follows_success(self):
        changed = builder.instrument(self.texts, self.anchors)
        text = changed[builder.SOURCE_FILES[1]]
        for direction, expression in (("request", "ret = apr_bucket_read"), ("response", "rc = apr_bucket_read")):
            hook = 'apache_lifecycle_observe("actual_' + direction + '_apr_bucket_before_read"'
            self.assertEqual(text.count(hook), 1)
            self.assertLess(text.index(hook), text.index(expression))
        self.assertGreater(text.index("i12_apache_fault_after_bucket_read"), text.index("return ret;"))
        self.assertNotIn("FAULT", self.texts[builder.SOURCE_FILES[0]])

    def test_duplicate_read_anchor_rejected(self):
        self.texts[builder.SOURCE_FILES[1]] += "    ret = apr_bucket_read(bucket, &data, &len, block);"
        with self.assertRaisesRegex(ValueError, "exactly once"):
            builder.instrument(self.texts, self.anchors)

    def test_missing_fault_anchor_rejected(self):
        self.anchors[0]["original"] = "ABSENT"
        with self.assertRaisesRegex(ValueError, "exactly once"):
            builder.instrument(self.texts, self.anchors)

    def test_incomplete_fault_set_rejected(self):
        with self.assertRaisesRegex(ValueError, "four"):
            builder.instrument(self.texts, self.anchors[:3])

    def test_out_of_scope_anchor_rejected(self):
        self.anchors[0]["file"] = "common/runtime.c"
        with self.assertRaisesRegex(ValueError, "scope"):
            builder.instrument(self.texts, self.anchors)


class CanonicalCommandTests(unittest.TestCase):
    def command(self):
        return "libtool: compile: cc " + " ".join(sorted(builder.STRICT)) + " -c src/mod_security3.c -o src/.libs/mod_security3.o"

    def test_actual_transcript_preserves_hardening(self):
        argv = builder.compiler_argv(self.command(), "src/mod_security3.c")
        self.assertTrue(builder.STRICT.issubset(argv))

    def test_missing_hardening_rejected(self):
        with self.assertRaisesRegex(ValueError, "strict"):
            builder.compiler_argv(self.command().replace("-fstack-protector-strong", ""), "src/mod_security3.c")

    def test_duplicate_command_rejected(self):
        with self.assertRaisesRegex(ValueError, "ambiguous"):
            builder.compiler_argv(self.command() + "\n" + self.command(), "src/mod_security3.c")

    def test_response_file_rejected(self):
        with self.assertRaisesRegex(ValueError, "injection"):
            builder.compiler_argv(self.command() + " @options", "src/mod_security3.c")

    def test_dependency_output_flags_rejected(self):
        for flags in ("-MMD -MF src/.deps/module.d", "-MFsrc/immutable.d", "-Wp,-MD,src/deps.d",
                      "-MJ src/compile.json", "--dependency-file=src/immutable.d", "-Xpreprocessor -MD"):
            with self.subTest(flags=flags), self.assertRaisesRegex(ValueError, "dependency output"):
                builder.compiler_argv(self.command() + " " + flags, "src/mod_security3.c")

    def test_auxiliary_outputs_rejected(self):
        for flag in ("-save-temps", "-dumpdir=src/", "-fprofile-arcs", "-ftest-coverage"):
            with self.subTest(flag=flag), self.assertRaisesRegex(ValueError, "output"):
                builder.compiler_argv(self.command() + " " + flag, "src/mod_security3.c")


class ElfValidationTests(unittest.TestCase):
    def test_defined_wrapper_and_legitimate_host_import(self):
        builder.validate_wrapper_definitions(
            "1: 0000 16 FUNC GLOBAL DEFAULT 12 __wrap_msc_example\n"
            "2: 0000 0 NOTYPE GLOBAL DEFAULT UND ap_log_rerror_", ["msc_example"])

    def test_undefined_wrapper_rejected(self):
        with self.assertRaisesRegex(ValueError, "defined wrapper"):
            builder.validate_wrapper_definitions(
                "1: 0000 0 NOTYPE GLOBAL DEFAULT UND __wrap_msc_example", ["msc_example"])

    def test_missing_wrapper_rejected(self):
        with self.assertRaisesRegex(ValueError, "defined wrapper"):
            builder.validate_wrapper_definitions(
                "1: 0000 16 FUNC GLOBAL DEFAULT 12 unrelated", ["msc_example"])

    def test_selected_sdk_resolution_accepts_host_import_diagnostic(self):
        sdk = Path("/selected/libmodsecurity.so.3.0.14")
        result = builder.validate_sdk_resolution(
            "libmodsecurity.so.3 => /selected/libmodsecurity.so.3.0.14 (0x1)\n"
            "undefined symbol: ap_log_rerror_ (mod_security3.so)", sdk)
        self.assertEqual(result, str(sdk))

    def test_wrong_sdk_resolution_rejected(self):
        with self.assertRaisesRegex(ValueError, "different SDK"):
            builder.validate_sdk_resolution("libmodsecurity.so.3 => /other/libmodsecurity.so.3.0.14 (0x1)",
                                            Path("/selected/libmodsecurity.so.3.0.14"))

    def test_missing_or_unresolved_sdk_rejected(self):
        for output in ("libmodsecurity.so.3 => not found", "libc.so.6 => /lib/libc.so.6 (0x1)"):
            with self.subTest(output=output), self.assertRaises(ValueError):
                builder.validate_sdk_resolution(output, Path("/selected/libmodsecurity.so.3.0.14"))


class IdentityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "export"
        self.root.mkdir()

    def file(self, relative, content):
        path = self.base / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content if isinstance(content, str) else json.dumps(content))
        return {"path": str(path), "sha256": builder.sha(path)}

    def fixture(self):
        revision = "a" * 40
        symbols = ["msc_example", "msconnector_open_private_event_file", "apache_lifecycle_observe"]
        paths = list(builder.SOURCE_FILES) + ["tests/test_native_lifecycle_observer.py", "ci/runtime/lifecycle/i12/manifest.json"]
        for name in paths:
            self.file("export/" + name, "SYMBOLS = ('msc_example',)\n" if name.startswith("tests/") else "fixture\n")
        files = {name: {"sha256": builder.sha(self.root / name)} for name in paths}
        inventory = self.file("export/inventory.json", {"files": files})
        self.file("export/.i12-disposable-source-copy.json", {"format": "i12-disposable-source-copy-v2",
            "disposable": True, "path": str(self.root), "source_revision": revision,
            "snapshot_manifest": "inventory.json", "snapshot_manifest_sha256": inventory["sha256"]})
        capture = self.file("capture.json", {"profile": "apache-current", "source_copy": str(self.root),
            "source_revision": revision, "snapshot_manifest_sha256": inventory["sha256"],
            "source_git_tree": "b" * 40,
            "capture_manifest_sha256": files["ci/runtime/lifecycle/i12/manifest.json"]["sha256"],
            "exact_written_sha256": {name: files[name]["sha256"] for name in builder.SOURCE_FILES},
            "actual_before_sha256": {name: files[name]["sha256"] for name in builder.SOURCE_FILES}})
        make = self.file("make.stdout", "fixture transcript")
        sdk = self.file("sdk.so", "SDK fixture")
        header = self.file("include/modsecurity/transaction.h", "SDK fixture header")
        objects = {}
        for index in range(33):
            item = self.file("objects/" + str(index) + ".o", "object " + str(index))
            objects[item["path"]] = item["sha256"]
        identity = self.file("identity.json", {"source_revision": revision, "git_tree": "b" * 40, "source_inventory_sha256": inventory["sha256"],
            "objects": objects, "fresh_product_translation_units": 33, "historical_objects_reused": False,
            "commands": [{"label": "make", "exit": 0, "stdout_sha256": make["sha256"]}],
            "sdk": sdk, "sdk_headers": {header["path"]: header["sha256"]}})
        helpers = {name: self.file(name + ".o", name) for name in ("common", "fault", "bucket")}
        fault = self.file("fault.json", {"exit": 0, "helper_revision": 2,
            "object_sha256": helpers["fault"]["sha256"], "external_source_anchors": [
                {"file": name, "source_sha256": files[name]["sha256"]} for name in builder.SOURCE_FILES]})
        return {"source_root": str(self.root), "output": str(self.base / "output"),
                "capture_receipt": capture, "build_identity": identity, "make_stdout": make,
                "sdk_library": sdk, "sdk_include": str(self.base / "include"), "helper_objects": helpers,
                "fault_receipt": fault, "fault_header": self.file("fault.h", "header"), "wrapped_symbols": symbols}

    def test_receipts_bind_full_snapshot_and_objects_without_mutating_source(self):
        spec = self.fixture()
        before = {str(p): builder.sha(p) for p in self.root.rglob("*") if p.is_file()}
        builder.validate_inputs(spec)
        after = {str(p): builder.sha(p) for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        self.assertFalse((self.base / "output").exists())

    def test_stale_source_rejected(self):
        spec = self.fixture()
        (self.root / builder.SOURCE_FILES[0]).write_text("changed")
        with self.assertRaisesRegex(ValueError, "snapshot changed"):
            builder.validate_inputs(spec)

    def test_post_build_full_snapshot_recheck_detects_other_source_change(self):
        spec = self.fixture()
        builder.validate_inputs(spec)
        marker = json.loads((self.root / ".i12-disposable-source-copy.json").read_text())
        snapshot = json.loads((self.root / marker["snapshot_manifest"]).read_text())
        capture = builder.bound_json(spec["capture_receipt"])
        (self.root / "tests/test_native_lifecycle_observer.py").write_text("modified while compiling")
        with self.assertRaisesRegex(ValueError, "snapshot changed"):
            builder.validate_source_snapshot(self.root, snapshot, capture["exact_written_sha256"])

    def test_post_build_capture_only_output_recheck(self):
        spec = self.fixture()
        marker = json.loads((self.root / ".i12-disposable-source-copy.json").read_text())
        snapshot = json.loads((self.root / marker["snapshot_manifest"]).read_text())
        written = builder.bound_json(spec["capture_receipt"])["exact_written_sha256"]
        output = self.file("export/generated-observer.h", "generated capture output")
        written["generated-observer.h"] = output["sha256"]
        builder.validate_source_snapshot(self.root, snapshot, written)
        (self.root / "generated-observer.h").write_text("modified while linking")
        with self.assertRaisesRegex(ValueError, "Capture output changed"):
            builder.validate_source_snapshot(self.root, snapshot, written)

    def test_stale_object_rejected(self):
        spec = self.fixture()
        (self.base / "objects/0.o").write_text("stale")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            builder.validate_inputs(spec)

    def test_wrapper_omission_rejected(self):
        spec = self.fixture()
        spec["wrapped_symbols"].pop()
        with self.assertRaisesRegex(ValueError, "Wrapper list"):
            builder.validate_inputs(spec)

    def test_output_inside_input_rejected_before_mutation(self):
        spec = self.fixture()
        spec["output"] = str(self.root / "output")
        with self.assertRaisesRegex(ValueError, "disjoint"):
            builder.validate_inputs(spec)

    def test_capture_wrong_root_rejected(self):
        spec = self.fixture()
        capture = builder.bound_json(spec["capture_receipt"])
        capture["source_copy"] = str(self.base / "other")
        spec["capture_receipt"] = self.file("capture.json", capture)
        with self.assertRaisesRegex(ValueError, "apache-current"):
            builder.validate_inputs(spec)

    def test_capture_tree_mismatch_rejected(self):
        spec = self.fixture()
        capture = builder.bound_json(spec["capture_receipt"])
        capture["source_git_tree"] = "c" * 40
        spec["capture_receipt"] = self.file("capture.json", capture)
        with self.assertRaisesRegex(ValueError, "trees disagree"):
            builder.validate_inputs(spec)

    def test_capture_manifest_change_rejected(self):
        spec = self.fixture()
        (self.root / "ci/runtime/lifecycle/i12/manifest.json").write_text("changed")
        with self.assertRaisesRegex(ValueError, "Capture manifest"):
            builder.validate_inputs(spec)

    def test_different_sdk_include_root_rejected(self):
        spec = self.fixture()
        self.file("other/include/modsecurity/transaction.h", "SDK fixture header")
        spec["sdk_include"] = str(self.base / "other/include")
        with self.assertRaisesRegex(ValueError, "selected include root"):
            builder.validate_inputs(spec)


if __name__ == "__main__":
    unittest.main()
