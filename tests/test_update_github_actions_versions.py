from __future__ import annotations

import importlib.util
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "update-github-actions-versions.py"
if str(SCRIPT.parent) not in sys.path:
    sys.path.insert(0, str(SCRIPT.parent))


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


class FailingResolver(FakeResolver):
    def __init__(self, error):
        super().__init__()
        self.error = error

    def get_semver_refs(self, action):
        raise self.error


class UpdateGitHubActionsVersionsTest(unittest.TestCase):
    def test_api_url_must_be_credential_free_https(self):
        for value in (
            "http://api.github.com",
            "https://token@api.github.com",
            "https://api.github.com?redirect=evil",
            "https://api.github.com/#fragment",
        ):
            with self.subTest(value=value), self.assertRaises(updater.ActionLookupError):
                updater.GitHubActionResolver(api_url=value)

        resolver = updater.GitHubActionResolver(api_url="https://github.example/api/v3/")
        self.assertEqual(resolver.api_url, "https://github.example/api/v3")

    def test_api_response_is_bounded_before_json_decoding(self):
        class OversizedResponse:
            headers = {}

            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return None

            def read(self, limit):
                self.limit = limit
                return b" " * limit

        response = OversizedResponse()
        resolver = updater.GitHubActionResolver()
        with mock.patch.object(resolver.opener, "open", return_value=response):
            with self.assertRaisesRegex(updater.ActionLookupError, "size limit"):
                resolver._request_json("/repos/actions/checkout/tags")
        self.assertEqual(response.limit, updater.MAX_API_RESPONSE_BYTES + 1)

    def test_api_error_response_is_also_bounded(self):
        resolver = updater.GitHubActionResolver()
        error = updater.urllib.error.HTTPError(
            "https://api.github.com/repos/actions/checkout/tags",
            500,
            "failure",
            {},
            io.BytesIO(b"x" * (updater.MAX_API_RESPONSE_BYTES + 1)),
        )
        with mock.patch.object(resolver.opener, "open", side_effect=error):
            with self.assertRaisesRegex(updater.ActionLookupError, "size limit"):
                resolver._request_json("/repos/actions/checkout/tags")

    def test_api_redirects_are_not_followed(self):
        handler = updater.NoRedirectHandler()
        request = updater.urllib.request.Request("https://api.github.com/repos/example/project")
        self.assertIsNone(
            handler.redirect_request(
                request,
                None,
                302,
                "Found",
                {},
                "https://attacker.invalid/collect",
            )
        )

    def test_api_pagination_is_bounded(self):
        resolver = updater.GitHubActionResolver()
        full_page = ([{}] * 100, {})
        with mock.patch.object(resolver, "_request_json", return_value=full_page) as request:
            with self.assertRaisesRegex(updater.ActionLookupError, "page limit"):
                resolver._paged("/repos/actions/checkout/tags")
        self.assertEqual(request.call_count, updater.MAX_API_PAGES)

    def test_checkout_major_ref_updates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workflow = root / ".github/workflows/test.yml"
            workflow.parent.mkdir(parents=True)
            workflow.write_text("steps:\n  - uses: actions/checkout@v4\n", encoding="utf-8")
            rows, _ = updater.scan_workflows(root, FakeResolver({"actions/checkout": ["v4", "v5"]}), write=True)
            self.assertEqual(rows[0].status, "Updated")
            self.assertIn("actions/checkout@v5", workflow.read_text(encoding="utf-8"))

    def test_quoted_and_unquoted_actions_preserve_suffix_when_updated(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workflow = root / ".github/workflows/test.yml"
            workflow.parent.mkdir(parents=True)
            workflow.write_text(
                "steps:\n"
                "  - uses: actions/checkout@v4 # unquoted\n"
                "  - uses: \"actions/checkout@v4\" # double quoted\n"
                "  - uses: 'actions/checkout@v4' # single quoted\n",
                encoding="utf-8",
            )

            rows, _ = updater.scan_workflows(root, FakeResolver({"actions/checkout": ["v4", "v5"]}), write=True)

            self.assertEqual([row.status for row in rows], ["Updated"] * 3)
            self.assertEqual(
                workflow.read_text(encoding="utf-8"),
                "steps:\n"
                "  - uses: actions/checkout@v5 # unquoted\n"
                "  - uses: \"actions/checkout@v5\" # double quoted\n"
                "  - uses: 'actions/checkout@v5' # single quoted\n",
            )

    def test_malformed_quoted_actions_are_not_rewritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workflow = root / ".github/workflows/test.yml"
            workflow.parent.mkdir(parents=True)
            malformed = "  - uses: \"" + ("a" * 65536) + "\n"
            mismatched = "  - uses: \"actions/checkout@v4' # mismatched\n"
            contents = "steps:\n" + malformed + mismatched
            workflow.write_text(contents, encoding="utf-8")

            rows, _ = updater.scan_workflows(root, FakeResolver({"actions/checkout": ["v4", "v5"]}), write=True)

            self.assertEqual(rows, [])
            self.assertEqual(workflow.read_text(encoding="utf-8"), contents)

    def test_write_false_reports_updates_without_rewriting(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workflow = root / ".github/workflows/test.yml"
            workflow.parent.mkdir(parents=True)
            contents = "steps:\n  - uses: actions/checkout@v4 # keep\n"
            workflow.write_text(contents, encoding="utf-8")

            rows, _ = updater.scan_workflows(root, FakeResolver({"actions/checkout": ["v4", "v5"]}), write=False)

            self.assertEqual([row.status for row in rows], ["Updated"])
            self.assertEqual(workflow.read_text(encoding="utf-8"), contents)

    def test_lookup_failures_are_reported_without_an_update(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workflow = root / ".github/workflows/test.yml"
            workflow.parent.mkdir(parents=True)
            uses_line = updater.parse_uses_line(workflow, 1, "  - uses: actions/checkout@v4\n")
            self.assertIsNotNone(uses_line)

            for error in (updater.ActionLookupError("unavailable"), updater.RateLimitError("limited")):
                with self.subTest(error=type(error).__name__):
                    row, new_ref = updater.analyze_uses(
                        root,
                        uses_line,
                        FailingResolver(error),
                        module_is_submodule=False,
                        write=True,
                        allow_submodule_write=False,
                    )

                    self.assertEqual(row.status, "Error")
                    self.assertEqual(row.note, str(error))
                    self.assertIsNone(new_ref)

    def test_missing_current_ref_is_not_downgraded(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workflow = root / ".github/workflows/test.yml"
            workflow.parent.mkdir(parents=True)
            uses_line = updater.parse_uses_line(workflow, 1, "  - uses: actions/checkout@v5\n")
            self.assertIsNotNone(uses_line)

            row, new_ref = updater.analyze_uses(
                root,
                uses_line,
                FakeResolver({"actions/checkout": ["v4"]}),
                module_is_submodule=False,
                write=True,
                allow_submodule_write=False,
            )

            self.assertEqual(row.status, "Unknown")
            self.assertEqual(row.current_ref, "v5")
            self.assertEqual(row.new_ref, "v4")
            self.assertEqual(row.note, "current ref was not found in tags; not downgrading")
            self.assertIsNone(new_ref)

    def test_submodule_updates_require_explicit_write_authorization(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workflow = root / "modules/ModSecurity-test-Framework/.github/workflows/test.yml"
            workflow.parent.mkdir(parents=True)
            uses_line = updater.parse_uses_line(workflow, 1, "  - uses: actions/checkout@v4\n")
            self.assertIsNotNone(uses_line)

            row, new_ref = updater.analyze_uses(
                root,
                uses_line,
                FakeResolver({"actions/checkout": ["v4", "v5"]}),
                module_is_submodule=True,
                write=True,
                allow_submodule_write=False,
            )

            self.assertEqual(row.status, "Skipped submodule write")
            self.assertEqual(row.new_ref, "v5")
            self.assertIsNone(new_ref)

    def test_codeql_nested_action_is_parsed(self):
        parsed = updater.split_action_ref("github/codeql-action/init@v3")
        self.assertEqual(parsed, ("github/codeql-action/init", "v3"))
        self.assertEqual(updater.action_repo_slug(parsed[0]), "github/codeql-action")

    def test_action_repository_slug_rejects_path_and_url_confusion(self):
        for action in (
            "owner/../action",
            "../owner/action",
            "owner/%2e%2e/action",
            "owner:443/action",
            "owner@attacker/action",
        ):
            with self.subTest(action=action):
                self.assertIsNone(updater.action_repo_slug(action))

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
            outside_path = str(outside)

            with self.assertRaises(ValueError):
                updater.confined_report_path(root, outside_path)

    def test_report_symlink_to_outside_root_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as external_tmp:
            root = Path(tmp)
            outside = Path(external_tmp) / "actions-update-report.md"
            outside.write_text("outside", encoding="utf-8")
            report_link = root / "actions-update-report.md"
            report_link.symlink_to(outside)
            report_link_path = str(report_link)

            with self.assertRaises(ValueError):
                updater.confined_report_path(root, report_link_path)

    def test_cyclic_report_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report_link = root / "actions-update-report.md"
            report_link.symlink_to(report_link)
            report_link_path = str(report_link)

            with self.assertRaises(ValueError):
                updater.confined_report_path(root, report_link_path)

    def test_main_rejects_external_report_path_before_writing(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as external_tmp:
            root = Path(tmp)
            outside = Path(external_tmp) / "actions-update-report.md"
            workflow = root / ".github/workflows/test.yml"
            workflow.parent.mkdir(parents=True)
            workflow_contents = "steps:\n  - uses: actions/checkout@v4\n"
            workflow.write_text(workflow_contents, encoding="utf-8")
            arguments = ["--write", "--report", str(outside)]
            previous_directory = Path.cwd()
            try:
                os.chdir(root)
                with self.assertRaises(SystemExit) as error:
                    updater.main(arguments)
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
