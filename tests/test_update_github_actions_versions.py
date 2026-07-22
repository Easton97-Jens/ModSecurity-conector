from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "update-github-actions-versions.py"


def load_module():
    spec = importlib.util.spec_from_file_location("update_github_actions_versions", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


updater = load_module()


class FakeResolver:
    rate_limited = False

    def __init__(self, refs=None):
        self.refs = refs or {}

    def get_semver_refs(self, action):
        return self.refs.get(action, ["v4", "v5"]), "tags"


class UpdateGitHubActionsVersionsTest(unittest.TestCase):
    def test_checkout_major_ref_updates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workflow = root / ".github/workflows/test.yml"
            workflow.parent.mkdir(parents=True)
            workflow.write_text("steps:\n  - uses: actions/checkout@v4\n", encoding="utf-8")
            rows, _ = updater.scan_workflows(root, FakeResolver({"actions/checkout": ["v4", "v5"]}), write=True)
            self.assertEqual(rows[0].status, "Updated")
            self.assertIn("actions/checkout@v5", workflow.read_text(encoding="utf-8"))

    def test_codeql_nested_action_is_parsed(self):
        parsed = updater.split_action_ref("github/codeql-action/init@v3")
        self.assertEqual(parsed, ("github/codeql-action/init", "v3"))
        self.assertEqual(updater.action_repo_slug(parsed[0]), "github/codeql-action")

    def test_local_action_is_skipped(self):
        row = self._single_row("  - uses: ./foo\n")
        self.assertEqual(row.status, "Skipped local")

    def test_docker_action_is_skipped(self):
        row = self._single_row("  - uses: docker://alpine:3\n")
        self.assertEqual(row.status, "Skipped docker")

    def test_sha_pinned_action_is_not_changed(self):
        sha = "a" * 40
        row = self._single_row(f"  - uses: actions/checkout@{sha}\n")
        self.assertEqual(row.status, "Pinned SHA")

    def test_dynamic_action_is_skipped(self):
        row = self._single_row("  - uses: ${{ matrix.action }}\n")
        self.assertEqual(row.status, "Skipped dynamic")

    def test_semver_major_comparison(self):
        self.assertLess(updater.compare_semver_refs("v4", "v5"), 0)

    def test_semver_patch_comparison(self):
        self.assertLess(updater.compare_semver_refs("v4.1.0", "v4.2.0"), 0)

    def test_module_path_is_classified_as_module(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            module_workflow = root / "modules/ModSecurity-test-Framework/.github/workflows/test.yml"
            module_workflow.parent.mkdir(parents=True)
            module_workflow.write_text("steps:\n  - uses: actions/checkout@v4\n", encoding="utf-8")
            self.assertEqual(updater.path_repository(root, module_workflow), "module")

    def test_module_workflow_inside_root_is_discovered(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            module_workflow = root / "modules/ModSecurity-test-Framework/.github/workflows/test.yml"
            module_workflow.parent.mkdir(parents=True)
            module_workflow.write_text("steps:\n  - uses: actions/checkout@v4\n", encoding="utf-8")

            self.assertEqual(updater.workflow_files(root), [module_workflow.resolve()])

    def test_report_rendering(self):
        row = updater.ReportRow(
            status="Updated",
            path=Path(".github/workflows/test.yml"),
            line=1,
            action="actions/checkout",
            current_ref="v4",
            new_ref="v5",
            repository="main",
            note="latest from tags",
        )
        report = updater.render_report([row], module_submodule=True)
        self.assertIn("Found `uses:` entries: 1", report)
        self.assertIn("| Updated | .github/workflows/test.yml | 1 | actions/checkout | v4 | v5 | main | latest from tags |", report)

    def test_gitignore_ignores_report(self):
        gitignore = Path(__file__).resolve().parents[1] / ".gitignore"
        self.assertIn("actions-update-report.md", gitignore.read_text(encoding="utf-8").splitlines())

    def test_external_workflow_symlink_is_not_read_or_updated(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as external_tmp:
            root = Path(tmp)
            external = Path(external_tmp) / "external-workflow.yml"
            external_contents = "steps:\n  - uses: actions/checkout@v4\n"
            external.write_text(external_contents, encoding="utf-8")
            workflow = root / ".github/workflows/external.yml"
            workflow.parent.mkdir(parents=True)
            workflow.symlink_to(external)

            rows, _ = updater.scan_workflows(
                root,
                FakeResolver({"actions/checkout": ["v4", "v5"]}),
                write=True,
            )

            self.assertEqual(rows, [])
            self.assertEqual(external.read_text(encoding="utf-8"), external_contents)

    def test_root_relative_report_path_is_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            expected = (root / "actions-update-report.md").resolve()

            self.assertEqual(updater.confined_report_path(root, "actions-update-report.md"), expected)

    def test_report_path_outside_root_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as external_tmp:
            root = Path(tmp)
            outside = Path(external_tmp) / "actions-update-report.md"

            with self.assertRaises(ValueError):
                updater.confined_report_path(root, str(outside))

    def test_report_symlink_to_outside_root_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as external_tmp:
            root = Path(tmp)
            outside = Path(external_tmp) / "actions-update-report.md"
            outside.write_text("outside", encoding="utf-8")
            report_link = root / "actions-update-report.md"
            report_link.symlink_to(outside)

            with self.assertRaises(ValueError):
                updater.confined_report_path(root, str(report_link))

    def test_cyclic_report_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report_link = root / "actions-update-report.md"
            report_link.symlink_to(report_link)

            with self.assertRaises(ValueError):
                updater.confined_report_path(root, str(report_link))

    def test_main_rejects_external_report_path_before_writing(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as external_tmp:
            root = Path(tmp)
            outside = Path(external_tmp) / "actions-update-report.md"
            workflow = root / ".github/workflows/test.yml"
            workflow.parent.mkdir(parents=True)
            workflow_contents = "steps:\n  - uses: actions/checkout@v4\n"
            workflow.write_text(workflow_contents, encoding="utf-8")
            previous_directory = Path.cwd()
            try:
                os.chdir(root)
                with self.assertRaises(SystemExit) as error:
                    updater.main(["--write", "--report", str(outside)])
            finally:
                os.chdir(previous_directory)

            self.assertEqual(error.exception.code, 2)
            self.assertFalse(outside.exists())
            self.assertEqual(workflow.read_text(encoding="utf-8"), workflow_contents)

    def test_main_writes_root_relative_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = root / "actions-update-report.md"
            previous_directory = Path.cwd()
            try:
                os.chdir(root)
                result = updater.main(["--report", report.name])
            finally:
                os.chdir(previous_directory)

            self.assertEqual(result, 0)
            self.assertTrue(report.is_file())

    def _single_row(self, uses_line):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workflow = root / ".github/workflows/test.yml"
            workflow.parent.mkdir(parents=True)
            workflow.write_text(f"steps:\n{uses_line}", encoding="utf-8")
            rows, _ = updater.scan_workflows(root, FakeResolver(), write=True)
            return rows[0]


if __name__ == "__main__":
    unittest.main()
