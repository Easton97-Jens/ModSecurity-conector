"""Focused safety tests for repository-owned Python update PR selection."""

from __future__ import annotations

import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "select-python-update-pr.py"
SPEC = importlib.util.spec_from_file_location("select_python_update_pr", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SelectPythonUpdatePullRequestTests(unittest.TestCase):
    repository = "Easton97-Jens/ModSecurity-conector"
    owner = "Easton97-Jens"
    base = "master"
    branch = "automation/update-python-313"

    def response(self, **overrides: object) -> list[dict[str, object]]:
        record: dict[str, object] = {
            "number": 123,
            "draft": True,
            "head": {
                "ref": self.branch,
                "label": f"{self.owner}:{self.branch}",
                "repo": {
                    "full_name": self.repository,
                    "owner": {"login": self.owner},
                },
            },
            "base": {
                "ref": self.base,
                "repo": {"full_name": self.repository},
            },
        }
        record.update(overrides)
        return [record]

    def select(self, response: object) -> int | None:
        return MODULE.select_update_pull_request(
            response,
            repository=self.repository,
            owner=self.owner,
            base_branch=self.base,
            update_branch=self.branch,
        )

    def test_accepts_only_the_repository_owned_draft_default_branch_pr(self) -> None:
        self.assertEqual(self.select(self.response()), 123)
        self.assertIsNone(self.select([]))

    def test_rejects_same_name_fork_pr(self) -> None:
        response = self.response(
            head={
                "ref": self.branch,
                "label": f"attacker:{self.branch}",
                "repo": {
                    "full_name": "attacker/ModSecurity-conector",
                    "owner": {"login": "attacker"},
                },
            }
        )
        with self.assertRaises(MODULE.SelectionError):
            self.select(response)

    def test_rejects_wrong_base_or_non_draft_pr(self) -> None:
        for response in (
            self.response(base={"ref": "release", "repo": {"full_name": self.repository}}),
            self.response(draft=False),
        ):
            with self.assertRaises(MODULE.SelectionError):
                self.select(response)

    def test_rejects_multiple_or_malformed_matches(self) -> None:
        with self.assertRaises(MODULE.SelectionError):
            self.select(self.response() + self.response(number=124))
        with self.assertRaises(MODULE.SelectionError):
            self.select([{ "number": "123" }])

    def test_cli_emits_only_a_numeric_identifier_and_rejects_bad_json(self) -> None:
        with tempfile.TemporaryDirectory(prefix="python-update-pr-selection-") as directory:
            path = Path(directory) / "pulls.json"
            path.write_text(json.dumps(self.response()), encoding="utf-8")
            output = io.StringIO()
            errors = io.StringIO()
            self.assertEqual(
                MODULE.main(
                    [
                        "--input", str(path), "--repository", self.repository,
                        "--owner", self.owner, "--base", self.base, "--branch", self.branch,
                    ],
                    output=output,
                    error_output=errors,
                ),
                0,
            )
            self.assertEqual(output.getvalue(), "123\n")
            self.assertEqual(errors.getvalue(), "")

            path.write_text("{not json", encoding="utf-8")
            output = io.StringIO()
            errors = io.StringIO()
            self.assertEqual(
                MODULE.main(
                    [
                        "--input", str(path), "--repository", self.repository,
                        "--owner", self.owner, "--base", self.base, "--branch", self.branch,
                    ],
                    output=output,
                    error_output=errors,
                ),
                1,
            )
            self.assertEqual(output.getvalue(), "")
            self.assertIn("selection failed", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
