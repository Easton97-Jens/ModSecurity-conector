"""Regression checks for the actionlint self-repository compatibility boundary."""

from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from ci.tools import lint_workflows


class LintWorkflowsTests(unittest.TestCase):
    def test_normalizes_only_self_repository_uses_and_preserves_columns(self):
        source = (
            "jobs:\n  call:\n    uses: $/.github/workflows/reusable.yml # reviewed\n"
            "  test:\n    steps:\n"
            "      - uses: '$/.github/actions/local'\n"
            '      - uses: "$/another-action"\n'
            "      - uses: owner/action@" + "a" * 40 + "\n"
            "        run: echo '$/literal'\n"
        )
        expected = source.replace("uses: $/", "uses: ./").replace(
            "uses: '$/", "uses: './"
        ).replace('uses: "$/', 'uses: "./')
        normalized = lint_workflows.actionlint_source(source)
        self.assertEqual(normalized, expected)
        self.assertEqual(len(normalized), len(source))

    def test_block_scalar_scripts_and_comments_are_preserved(self):
        source = (
            "jobs:\n  test:\n    steps:\n      - run: |\n"
            "          uses: $/literal\n"
            "          echo 'uses: $/another-literal'\n"
            "        # uses: $/comment\n"
            "      - uses: $/.github/actions/local\n"
        )
        self.assertEqual(
            lint_workflows.actionlint_source(source),
            source.replace("- uses: $/.github/actions/local", "- uses: ./.github/actions/local"),
        )

    def test_rejects_unsafe_self_repository_paths(self):
        for reference in ("$/../escape", "$/a/./b", "$/a//b", "$/a@master", "$/"):
            with self.subTest(reference=reference):
                with self.assertRaisesRegex(ValueError, "unsafe self-repository"):
                    lint_workflows.actionlint_source(f"    uses: {reference}\n")

    def test_runs_all_workflows_propagates_failure_and_preserves_originals(self):
        with tempfile.TemporaryDirectory() as temporary:
            paths = [Path(temporary) / name for name in ("caller.yml", "second.yml")]
            source = "jobs:\n  call:\n    uses: $/.github/workflows/reusable.yml\n"
            for path in paths:
                path.write_text(source, encoding="utf-8")
            with (
                patch.object(lint_workflows.shutil, "which", return_value=None),
                patch.object(lint_workflows.subprocess, "run", side_effect=[
                    subprocess.CompletedProcess([], 1),
                    subprocess.CompletedProcess([], 0),
                ]) as run,
            ):
                self.assertEqual(lint_workflows.lint("/checked/actionlint", paths), 1)
            self.assertEqual(run.call_count, 2)
            for path, invocation in zip(paths, run.call_args_list):
                self.assertEqual(path.read_text(encoding="utf-8"), source)
                self.assertEqual(invocation.args[0], [
                    "/checked/actionlint", "-shellcheck=", "-stdin-filename", str(path), "-",
                ])
                self.assertEqual(invocation.kwargs["input"], source.replace("uses: $/", "uses: ./"))
                self.assertEqual(invocation.kwargs["timeout"], 120)


if __name__ == "__main__":
    unittest.main()
