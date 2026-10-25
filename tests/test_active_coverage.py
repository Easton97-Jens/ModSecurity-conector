"""Independent line-report, build-identity and native profiler controls."""
from __future__ import annotations

import dis
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

from ci.lib.active_coverage import (CoverageError, compile_instrumented,
                                    gcov_lines, go_lines, make_manifest, python_lines,
                                    validate_manifest, write_generic_report)
from ci.lib.python_coverage_bootstrap import provision_bootstrap


class ActiveCoverageTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="active-coverage-control-", dir=os.environ.get("RUNNER_TEMP"))
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root = self.base / "source"
        self.output = self.base / "reports"
        self.root.mkdir(mode=0o700)
        self.output.mkdir(mode=0o700)
        (self.root / "product.py").write_text("def answer():\n    return 42\n", encoding="utf-8")
        self.revision = "a" * 40
        self.inventory = "b" * 64

    def manifest(self):
        sources = write_generic_report(self.root, {"product.py": {1: 1, 2: 0}}, self.output / "coverage.xml")
        return make_manifest(self.root, self.output, self.revision, self.inventory,
                             ["coverage.fixture"], sources, ["coverage.xml"])

    def test_generic_report_uses_real_line_counts(self):
        source = self.root / "product.py"
        program = "def numbers():\n    yield 42\n    yield 99\n\ndef answer():\n    values = numbers()\n    return next(values)\n\nprint(answer())\n"
        source.write_text(program, encoding="utf-8")
        compiled = compile(program, str(source), "exec", dont_inherit=True)
        numbers = next(value for value in compiled.co_consts
                       if isinstance(value, types.CodeType) and value.co_name == "numbers")
        self.assertIn(None, [line for _, line in dis.findlinestarts(numbers)])
        overlay = provision_bootstrap(self.output, self.root, "coverage.fixture.generator")
        child = subprocess.run([sys.executable, str(source)], cwd=self.root,
                               env={**os.environ, **overlay}, check=False,
                               capture_output=True, text=True)
        self.assertEqual(child.returncode, 0, child.stderr)
        self.assertEqual(child.stdout.strip(), "42")
        records = sorted((self.output / "python-subprocess").glob("*.json"))
        self.assertEqual(len(records), 1)
        raw = records[0]
        recorded = json.loads(raw.read_text(encoding="utf-8"))
        self.assertEqual(recorded["target"], "coverage.fixture.generator:subprocess")
        self.assertGreater(recorded["files"]["product.py"]["2"], 0)
        self.assertNotIn("3", recorded["files"]["product.py"])
        observations = {}
        python_lines(raw, self.root, observations)
        self.assertGreater(observations["product.py"][2], 0)
        self.assertEqual(observations["product.py"][3], 0)
        sources = write_generic_report(self.root, observations, self.output / "coverage.xml")
        make_manifest(self.root, self.output, self.revision, self.inventory,
                      ["coverage.fixture"], sources,
                      ["coverage.xml", raw.relative_to(self.output).as_posix()])
        report = ET.parse(self.output / "coverage.xml").getroot()
        self.assertEqual(report.attrib, {"version": "1"})
        self.assertEqual(report[0].attrib, {"path": "product.py"})
        reported = {int(line.attrib["lineNumber"]): line.attrib["covered"] for line in report[0]}
        self.assertEqual(reported[2], "true")
        self.assertEqual(reported[3], "false")
        self.assertTrue(all(number > 0 for number in reported))

    def test_report_rejects_source_path_escape(self):
        observations = {"../outside.py": {1: 1}}
        with self.assertRaises(CoverageError):
            write_generic_report(self.root, observations, self.output / "coverage.xml")
        self.assertFalse((self.output / "coverage.xml").exists())

    def test_manifest_rejects_changed_source(self):
        manifest = self.manifest()
        (self.root / "product.py").write_text("def answer():\n    return 41\n", encoding="utf-8")
        with self.assertRaisesRegex(CoverageError, "source changed"):
            validate_manifest(manifest, self.root, self.output, self.revision, self.inventory)

    def test_manifest_rejects_changed_report(self):
        manifest = self.manifest()
        (self.output / "coverage.xml").write_bytes(b"<coverage version='1'/>")
        with self.assertRaisesRegex(CoverageError, "artifact changed"):
            validate_manifest(manifest, self.root, self.output, self.revision, self.inventory)

    def test_manifest_rejects_foreign_revision(self):
        manifest = self.manifest()
        foreign_revision = "c" * 40
        with self.assertRaisesRegex(CoverageError, "another source revision"):
            validate_manifest(manifest, self.root, self.output, foreign_revision, self.inventory)

    def test_manifest_rejects_foreign_inventory(self):
        manifest = self.manifest()
        foreign_inventory = "d" * 64
        with self.assertRaisesRegex(CoverageError, "another active inventory"):
            validate_manifest(manifest, self.root, self.output, self.revision, foreign_inventory)

    def test_go_blocks_map_to_current_module_source(self):
        module = "connectors/example"
        directory = self.root / module
        directory.mkdir(parents=True)
        (directory / "go.mod").write_text("module example.org/reviewed\n\ngo 1.26\n", encoding="utf-8")
        (directory / "product.go").write_text("package fixture\nfunc answer() int { return 42 }\n", encoding="utf-8")
        profile = self.output / "go.out"
        profile.write_text("mode: atomic\nexample.org/reviewed/product.go:2.19,2.32 1 3\n", encoding="utf-8")
        observed = {}
        go_lines(profile, self.root, module, observed)
        self.assertEqual(observed, {module + "/product.go": {2: 3}})

    def test_compiler_notes_preserve_real_source_identity(self):
        self.assertIsNotNone(shutil.which("cc"), "native coverage control requires cc")
        self.assertIsNotNone(shutil.which("gcov"), "native coverage control requires gcov")
        source = self.root / "measured.c"
        source.write_text("int answer(void) { return 42; }\nint main(void) { return answer() == 42 ? 0 : 1; }\n", encoding="utf-8")
        directory = self.output / "native"
        notes = directory / "gcov-notes"
        data = directory / "gcov-data"
        notes.mkdir(mode=0o700, parents=True)
        data.mkdir(mode=0o700)
        binary = self.base / "actual-native"
        unrelated = self.base / "actual-native-asan-measured.gcno"
        unrelated.write_bytes(b"unrelated prior compiler output\n")
        with patch.dict(os.environ, {"ACTIVE_COVERAGE_NOTES": str(notes),
                                     "GCOV_PREFIX": str(data), "GCOV_PREFIX_STRIP": "0"}):
            compiled = compile_instrumented(["cc", str(source), "-o", str(binary)])
            self.assertEqual(compiled, 0)
            executed = subprocess.run([str(binary)], check=False)
            self.assertEqual(executed.returncode, 0)
        unrelated_copy = notes / unrelated.relative_to(unrelated.anchor)
        self.assertFalse(unrelated_copy.exists(), "compiler copied notes from an unrelated output")
        self.assertTrue(list(notes.rglob("*.gcno")))
        self.assertTrue(list(data.rglob("*.gcda")))
        observed = {}
        reports = gcov_lines(directory, self.root, observed)
        self.assertTrue(reports)
        self.assertEqual(set(observed), {"measured.c"})
        self.assertGreater(observed["measured.c"][1], 0)

    def test_unsafe_compiler_argument_rejected_before_process(self):
        source = self.root / "safe.c"
        source.write_text("int main(void) { return 0; }\n", encoding="utf-8")
        payload = self.base / "payload.o"
        payload.write_text("INPUT(/outside/unapproved.so)\n", encoding="utf-8")
        arguments = ["cc", str(source), str(payload),
                     "-o", str(self.base / "unsafe-output")]
        with patch("ci.lib.active_coverage.subprocess.run") as process:
            with self.assertRaisesRegex(
                    CoverageError,
                    "^compiler object or shared library must have a genuine ELF header$"):
                compile_instrumented(arguments)
            process.assert_not_called()

# Parent default discovery uses the one admitted active-case inventory.
if __import__("os").environ.get("ON_DEMAND_TESTS") != "1":
    def load_tests(loader, standard_tests, pattern):
        from ci.lib.active_test_inventory import module_load_tests
        return module_load_tests(loader, standard_tests, pattern)
