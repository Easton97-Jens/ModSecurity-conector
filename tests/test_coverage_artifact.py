"""Private synthetic identity controls, not Parent runtime/coverage evidence.

Run only after explicit active
inventory admission. Fixtures stay in a private RUNNER_TEMP child and never enter
the actual Parent collector output root. No fixture observations qualify runtime.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load_collector():
    """Lazy hook: collection imports no production collector before test admission."""
    spec = importlib.util.spec_from_file_location(
        "coverage_artifact_control_collector", ROOT / "ci/tools/collect-active-coverage.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CoverageArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.collector = load_collector()

    def setUp(self):
        from ci.lib.active_test_inventory import validate_output_root
        # Never silently fall back to /tmp or write fixtures into source.
        parent = validate_output_root(ROOT, Path(os.environ["RUNNER_TEMP"]))
        temporary = tempfile.TemporaryDirectory(prefix="coverage-artifact-control-", dir=parent)
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.source = self.base / "private-source"
        self.reports = self.base / "synthetic-reports"
        self.source.mkdir(mode=0o700)
        self.reports.mkdir(mode=0o700)
        self.revision = "a" * 40
        self.inventory_digest = "b" * 64
        self.status = ""
        self.checkout_revision = self.revision
        self.inventory = SimpleNamespace(
            digest=self.inventory_digest,
            core_case_ids=("fixture.core", "fixture.unselected"),
            offline_case_ids=("fixture.offline",))
        self.selected = ({"selector": {"kind": "go", "module": "sample/module"},
                          "cases": ({"id": "fixture.core"}, {"id": "fixture.offline"})},)
        self.write_source("product.py", "def answer():\n    return 42\n")
        self.write_source("sample/module/product.go", "package sample\nfunc Answer() int { return 42 }\n")
        dependency_names = self.collector.PYTHON_DEPENDENCY_INPUTS
        analysis_names = ("config/testing/sonar-source-roles.json", ".sonarcloud.properties",
                          "sonar-project.properties")
        for name in (*dependency_names, *analysis_names,
                     "sample/module/go.mod", "sample/module/go.sum"):
            self.write_source(name, "private identity input: " + name + "\n")
        self.build = {
            "dependency_inputs": self.hash_inputs(dependency_names),
            "analysis_inputs": self.hash_inputs(analysis_names),
            "modules": {"sample/module": {
                name: self.hash_file(self.source / "sample/module" / name)
                for name in ("go.mod", "go.sum")}},
            "modsecurity": {"producer_attestation_fixture": "not an actual SDK"},
        }
        (self.reports / "sample").mkdir(mode=0o700)
        (self.reports / "sample/go.out").write_text(
            "mode: set\nsample/product.go:2.1,2.33 1 1\n", encoding="utf-8")
        # Same real report/manifest helpers used by test_active_coverage.py.
        sources = self.collector.write_generic_report(
            self.source, {"product.py": {1: 1, 2: 0}}, self.reports / "coverage.xml")
        case_ids = ["fixture.core", "fixture.offline"]
        self.manifest = self.collector.make_manifest(
            self.source, self.reports, self.revision, self.inventory_digest,
            case_ids, sources, ["coverage.xml", "sample/go.out"],
            build_identity=copy.deepcopy(self.build),
            budget=self.collector.case_budget(self.inventory.core_case_ids,
                                             self.inventory.offline_case_ids, case_ids))
        self.manifest["go_sources"] = {
            "sample/module/product.go": self.hash_file(self.source / "sample/module/product.go")}
        self.save_manifest()
        # Inventory parsing/selection have independent controls. Only these and
        # bounded Git metadata are substituted; all asserted file checks run real.
        for replacement in (
                patch.object(self.collector, "ROOT", self.source),
                patch.object(self.collector, "load_inventory", return_value=self.inventory),
                patch.object(self.collector, "select_executions", return_value=self.selected),
                patch.object(self.collector, "git_output", side_effect=self.git_metadata),
                patch.dict(os.environ, {"GITHUB_OUTPUT": str(self.base / "github-output")})):
            replacement.start()
            self.addCleanup(replacement.stop)

    def write_source(self, name, value):
        target = self.source / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(value, encoding="utf-8")

    def hash_file(self, path):
        return self.collector.digest(self.collector.regular_bytes(path))

    def hash_inputs(self, names):
        return {name: self.hash_file(self.source / name) for name in names}

    def save_manifest(self):
        (self.reports / "manifest.json").write_text(
            json.dumps(self.manifest), encoding="utf-8")

    def git_metadata(self, *arguments):
        if arguments == ("rev-parse", "HEAD"):
            return self.checkout_revision
        if arguments == ("status", "--porcelain", "--untracked-files=normal"):
            return self.status
        raise AssertionError("unexpected Git metadata request: " + repr(arguments))

    def verify_artifact(self):
        with patch.object(self.collector, "build_identity",
                          side_effect=AssertionError("artifact consumer must not rebuild SDK")) as sdk:
            try:
                return self.collector.verify_artifact(self.reports, self.revision)
            finally:
                sdk.assert_not_called()

    def test_valid_artifact_uses_real_manifest_checks_without_sdk_build(self):
        self.assertEqual(self.verify_artifact(), 0)
        published = (self.base / "github-output").read_text(encoding="utf-8")
        self.assertIn("generic_report=" + str(self.reports / "coverage.xml"), published)
        self.assertIn("go_reports=" + str(self.reports / "sample/go.out"), published)

    def test_artifact_rejects_wrong_checkout_revision(self):
        self.checkout_revision = "c" * 40
        with self.assertRaisesRegex(self.collector.CoverageError, "another revision"):
            self.verify_artifact()

    def test_artifact_rejects_wrong_manifest_revision(self):
        self.manifest["revision"] = "c" * 40
        self.save_manifest()
        with self.assertRaisesRegex(self.collector.CoverageError, "another source revision"):
            self.verify_artifact()

    def test_artifact_rejects_changed_generic_report_hash(self):
        with (self.reports / "coverage.xml").open("ab") as stream:
            stream.write(b"\n")
        with self.assertRaisesRegex(self.collector.CoverageError, "artifact changed"):
            self.verify_artifact()

    def test_artifact_rejects_changed_go_report_hash(self):
        with (self.reports / "sample/go.out").open("ab") as stream:
            stream.write(b"\n")
        with self.assertRaisesRegex(self.collector.CoverageError, "artifact changed"):
            self.verify_artifact()

    def test_artifact_rejects_changed_generic_source_hash(self):
        self.write_source("product.py", "def answer():\n    return 99\n")
        with self.assertRaisesRegex(self.collector.CoverageError, "measured source changed"):
            self.verify_artifact()

    def test_artifact_rejects_changed_go_source_hash(self):
        self.write_source("sample/module/product.go", "package sample\nfunc Answer() int { return 99 }\n")
        with self.assertRaisesRegex(self.collector.CoverageError, "Go source changed"):
            self.verify_artifact()

    def test_artifact_rejects_changed_inventory_identity(self):
        self.manifest["inventory_sha256"] = "c" * 64
        self.save_manifest()
        with self.assertRaisesRegex(self.collector.CoverageError, "another active inventory"):
            self.verify_artifact()

    def test_artifact_rejects_changed_selected_cases(self):
        self.manifest["case_ids"][0] = "fixture.unselected"
        self.manifest["case_budget"]["selected_core_case_ids"] = ["fixture.unselected"]
        self.save_manifest()
        with self.assertRaisesRegex(self.collector.CoverageError, "complete admitted coverage group"):
            self.verify_artifact()

    def test_artifact_rejects_changed_exact_case_budget(self):
        self.manifest["case_budget"]["core_case_count"] += 1
        self.manifest["case_budget"]["total_case_count"] += 1
        self.save_manifest()
        with self.assertRaisesRegex(self.collector.CoverageError, "exact admitted core"):
            self.verify_artifact()

    def test_artifact_rejects_changed_dependency_input(self):
        self.write_source(self.collector.PYTHON_DEPENDENCY_INPUTS[0], "changed dependency\n")
        with self.assertRaisesRegex(self.collector.CoverageError, "dependency inputs changed"):
            self.verify_artifact()

    def test_artifact_rejects_changed_analysis_input(self):
        self.write_source("config/testing/sonar-source-roles.json", "changed analysis\n")
        with self.assertRaisesRegex(self.collector.CoverageError, "analysis or dependency inputs changed"):
            self.verify_artifact()

    def test_artifact_rejects_changed_module_dependency(self):
        self.write_source("sample/module/go.mod", "module changed\n")
        with self.assertRaisesRegex(self.collector.CoverageError, "module dependencies changed"):
            self.verify_artifact()

    def test_artifact_rejects_dirty_checkout(self):
        self.status = " M product.py"
        with self.assertRaisesRegex(self.collector.CoverageError, "clean source checkout"):
            self.verify_artifact()

    def test_required_verify_calls_full_sdk_build_identity(self):
        with patch.object(self.collector, "build_identity", return_value=self.build) as sdk:
            self.assertEqual(self.collector.verify(self.reports), 0)
            sdk.assert_called_once_with(self.selected)

    def test_required_verify_rejects_changed_sdk_build_identity(self):
        changed = copy.deepcopy(self.build)
        changed["modsecurity"]["producer_attestation_fixture"] = "changed"
        with patch.object(self.collector, "build_identity", return_value=changed) as sdk:
            with self.assertRaisesRegex(self.collector.CoverageError, "SDK or module dependency identity changed"):
                self.collector.verify(self.reports)
            sdk.assert_called_once_with(self.selected)


if os.environ.get("ON_DEMAND_TESTS") != "1":
    def load_tests(loader, standard_tests, pattern):
        from ci.lib.active_test_inventory import module_load_tests
        return module_load_tests(loader, standard_tests, pattern)

if __name__ == "__main__":
    unittest.main()
