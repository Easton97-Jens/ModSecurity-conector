"""Exercise the Update-submodules resolver and checkout shell against local Git.

The workflow remains the source of the shell under test.  Only ``git
ls-remote`` is replaced so the resolver never contacts the network; all tree,
gitlink, fetch, and merge-base operations use temporary local repositories.
Publisher identity checks use a read-only GitHub CLI stub and never publish.
"""

from __future__ import annotations

import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "update-submodules.yml"
VALIDATOR = ROOT / "ci" / "tools" / "validate-submodule-candidate-state.py"


class UpdateSubmodulesLocalGitTests(unittest.TestCase):
    def git(self, directory: Path, *arguments: str, input_text: str | None = None) -> str:
        completed = subprocess.run(
            ["git", "-C", str(directory), *arguments],
            input=input_text,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return completed.stdout.strip()

    def commit_file(self, repository: Path, name: str, content: str, message: str) -> str:
        (repository / name).write_text(content, encoding="utf-8")
        self.git(repository, "add", name)
        self.git(repository, "commit", "-m", message)
        return self.git(repository, "rev-parse", "HEAD")

    def make_layout(self, temporary: Path) -> tuple[Path, Path, Path, str, str]:
        framework_source = temporary / "framework-source"
        framework_source.mkdir()
        self.git(framework_source, "init")
        self.git(framework_source, "config", "user.email", "test@example.invalid")
        self.git(framework_source, "config", "user.name", "Update-submodules Test")
        current = self.commit_file(framework_source, "framework.txt", "A\n", "framework A")

        parent = temporary / "parent"
        parent.mkdir()
        self.git(parent, "init")
        self.git(parent, "config", "user.email", "test@example.invalid")
        self.git(parent, "config", "user.name", "Update-submodules Test")
        self.commit_file(parent, "README", "parent\n", "parent")
        self.git(
            parent,
            "-c",
            "protocol.file.allow=always",
            "submodule",
            "add",
            str(framework_source),
            "framework",
        )
        self.git(parent, "commit", "-m", "add framework")
        candidate = self.commit_file(framework_source, "framework.txt", "B\n", "framework B")
        return parent, parent / "framework", framework_source, current, candidate

    @staticmethod
    def workflow_step(job_name: str, step_name: str) -> str:
        workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
        steps = workflow["jobs"][job_name]["steps"]
        return next(step["run"] for step in steps if step["name"] == step_name)

    @staticmethod
    def outputs(path: Path) -> dict[str, str]:
        return dict(line.split("=", 1) for line in path.read_text(encoding="utf-8").splitlines())

    def run_resolver(
        self,
        parent: Path,
        temporary: Path,
        remote_refs: str,
        *,
        remote_status: int = 0,
    ) -> tuple[subprocess.CompletedProcess[str], Path]:
        mock_bin = temporary / "mock-bin"
        mock_bin.mkdir(exist_ok=True)
        mock_git = mock_bin / "git"
        mock_git.write_text(
            "#!/bin/sh\n"
            "set -eu\n"
            "if [ \"$1\" = ls-remote ]; then\n"
            "  printf '%s\\n' \"${MOCK_REMOTE_REFS:-}\"\n"
            "  exit \"${MOCK_REMOTE_STATUS:-0}\"\n"
            "fi\n"
            "exec /usr/bin/git \"$@\"\n",
            encoding="utf-8",
        )
        mock_git.chmod(0o700)
        output = temporary / "github-output"
        script = self.workflow_step("resolve-submodule-update", "Resolve exactly one official submodule commit")
        # GitHub evaluates this one workflow expression before starting Bash.
        # The local default models a scheduled/non-validation-only invocation.
        script = re.sub(r"\$\{\{.*?\}\}", "false", script, flags=re.DOTALL)
        environment = {
            **os.environ,
            "PATH": f"{mock_bin}:/usr/bin:/bin",
            "MOCK_REMOTE_REFS": remote_refs,
            "MOCK_REMOTE_STATUS": str(remote_status),
            "GITHUB_OUTPUT": str(output),
            "SUBMODULE_URL": "https://example.invalid/framework.git",
            "SUBMODULE_REF": "refs/heads/master",
            "SUBMODULE_PATH": "framework",
        }
        result = subprocess.run(
            ["/bin/bash", "-ceu", script],
            cwd=parent,
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        return result, output

    def run_checkout(self, parent: Path, framework_source: Path, current: str, candidate: str) -> subprocess.CompletedProcess[str]:
        script = self.workflow_step("validate-submodule-update", "Check out the resolved descendant revision")
        return subprocess.run(
            ["/bin/bash", "-ceu", script],
            cwd=parent,
            env={
                **os.environ,
                "PATH": "/usr/bin:/bin",
                "SUBMODULE_PATH": "framework",
                "SUBMODULE_URL": str(framework_source),
                "CURRENT_GITLINK_SHA": current,
                "CANDIDATE_SHA": candidate,
            },
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def capture_baseline(self, parent: Path, environment_file: Path) -> dict[str, str]:
        environment_file.touch()
        result = subprocess.run(
            [
                sys.executable,
                str(VALIDATOR),
                "capture-parent-baseline",
                "--parent-root",
                str(parent),
                "--github-env",
                str(environment_file),
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            env={**os.environ, "RUNNER_TEMP": str(environment_file.parent)},
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return self.outputs(environment_file)

    def validate_candidate(
        self, parent: Path, baseline: dict[str, str], current: str, candidate: str
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(VALIDATOR),
                "validate",
                "--parent-root",
                str(parent),
                "--submodule-path",
                "framework",
                "--current-gitlink-sha",
                current,
                "--candidate-sha",
                candidate,
                "--expected-parent-head",
                baseline["EXPECTED_PARENT_HEAD"],
                "--expected-parent-hooks-sha256",
                baseline["EXPECTED_PARENT_HOOKS_SHA256"],
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def test_noop_resolver_emits_a_successful_unchanged_result(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            parent, _framework, _source, current, _candidate = self.make_layout(Path(raw))
            result, output = self.run_resolver(parent, Path(raw), f"{current}\trefs/heads/master")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                self.outputs(output),
                {
                    "candidate_sha": current,
                    "current_sha": current,
                    "resolver_status": "resolved",
                    "changed": "false",
                    "validation_only": "false",
                },
            )
            workflow = WORKFLOW.read_text(encoding="utf-8")
            self.assertIn("outputs.changed == 'true'", workflow)
            self.assertIn("outputs.validation_only == 'false'", workflow)

    def test_forward_candidate_matches_the_real_gitlink_worktree_shape(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            temporary = Path(raw)
            parent, framework, source, current, candidate = self.make_layout(temporary)
            resolver, output = self.run_resolver(parent, temporary, f"{candidate}\trefs/heads/master")
            self.assertEqual(resolver.returncode, 0, resolver.stderr)
            self.assertEqual(self.outputs(output)["changed"], "true")

            baseline = self.capture_baseline(parent, temporary / "github-env")
            checkout = self.run_checkout(parent, source, current, candidate)
            self.assertEqual(checkout.returncode, 0, checkout.stderr)
            self.assertEqual(self.git(framework, "rev-parse", "HEAD"), candidate)
            self.assertEqual(self.git(parent, "diff", "--cached", "--quiet"), "")
            validated = self.validate_candidate(parent, baseline, current, candidate)
            self.assertEqual(validated.returncode, 0, validated.stderr)

    def test_bad_resolver_output_and_non_descendant_candidate_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            temporary = Path(raw)
            parent, _framework, source, current, candidate = self.make_layout(temporary)
            for label, remote_refs, expected in (
                ("wrong ref", f"{candidate}\trefs/heads/other", "Resolved unexpected submodule ref"),
                ("short SHA", "deadbeef\trefs/heads/master", "Resolved submodule revision is not a full SHA-1"),
                (
                    "ambiguous ref",
                    f"{candidate}\trefs/heads/master\n{current}\trefs/heads/master",
                    "Official submodule ref resolution is ambiguous",
                ),
            ):
                with self.subTest(resolver_failure=label):
                    result, _output = self.run_resolver(parent, temporary, remote_refs)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(expected, result.stderr)

            empty_tree = self.git(source, "mktree", input_text="")
            unrelated = self.git(source, "commit-tree", empty_tree, input_text="unrelated\n")
            self.git(source, "update-ref", "refs/heads/unrelated", unrelated)
            checkout = self.run_checkout(parent, source, current, unrelated)
            self.assertNotEqual(checkout.returncode, 0)
            self.assertIn("Candidate is not a descendant", checkout.stderr)


class SubmodulePublisherIdentityTests(unittest.TestCase):
    """Run the actual workflow guards with fixed, read-only API responses."""

    def setUp(self) -> None:
        workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
        self.workflow_env = workflow["env"]
        self.publisher = next(
            step
            for step in workflow["jobs"]["create-submodule-update-pr"]["steps"]
            if step.get("id") == "publish"
        )
        self.script = self.publisher["run"]
        self.prelude, separator, _rest = self.script.partition(
            "\nrequire_only_allowed_update_paths() {"
        )
        self.assertTrue(separator, "publisher prelude boundary is missing")
        self.functions = []
        for name in (
            "verify_open_pr_identity",
            "verify_open_draft_pr",
            "verify_merged_pr",
        ):
            matches = re.findall(rf"(?ms)^{name}\(\) \{{\n.*?^\}}", self.script)
            self.assertEqual(len(matches), 1, name)
            self.functions.append(matches[0])

    def run_identity_check(
        self, function: str, **overrides: str
    ) -> subprocess.CompletedProcess[str]:
        self.assertIn(function, ("verify_open_draft_pr", "verify_merged_pr"))
        environment = {
            **os.environ,
            **self.workflow_env,
            "PATH": "/usr/bin:/bin",
            "GITHUB_REPOSITORY": "owner/project",
            "EXPECTED_PR_AUTHOR": "easton97-jens-framework[bot]",
            "EXPECTED_HEAD": "a" * 40,
            "TEST_AUTHOR": "easton97-jens-framework[bot]",
            "TEST_STATE": "closed" if function == "verify_merged_pr" else "open",
            "TEST_BASE": "master",
            "TEST_HEAD_BRANCH": "chore/update-submodules",
            "TEST_HEAD_SHA": "a" * 40,
            "TEST_DRAFT": "true",
            "TEST_TITLE": self.workflow_env["PR_TITLE"],
            "TEST_BODY": self.workflow_env["PR_MARKER"],
            "TEST_AUTO_MERGE": "null",
            "TEST_BASE_REPO": "owner/project",
            "TEST_HEAD_REPO": "owner/project",
            "TEST_MERGED_AT": "2026-09-20T00:00:00Z",
            **overrides,
        }
        # No network, token, Git push, or PR mutation is available to these guards.
        gh_stub = r'''
gh() {
  if [ "$#" -ne 6 ] || [ "$1" != api ] || [ "$2" != --method ] || [ "$3" != GET ] || [ "$4" != "repos/$GITHUB_REPOSITORY/pulls/374" ] || [ "$5" != --jq ]; then
    echo "unexpected GitHub CLI invocation" >&2
    return 97
  fi
  case "$6" in
    .state) printf '%s\n' "$TEST_STATE" ;;
    .base.ref) printf '%s\n' "$TEST_BASE" ;;
    .head.ref) printf '%s\n' "$TEST_HEAD_BRANCH" ;;
    .head.sha) printf '%s\n' "$TEST_HEAD_SHA" ;;
    .draft) printf '%s\n' "$TEST_DRAFT" ;;
    .title) printf '%s\n' "$TEST_TITLE" ;;
    .user.login) printf '%s\n' "$TEST_AUTHOR" ;;
    .base.repo.full_name) printf '%s\n' "$TEST_BASE_REPO" ;;
    .head.repo.full_name) printf '%s\n' "$TEST_HEAD_REPO" ;;
    .merged_at) printf '%s\n' "$TEST_MERGED_AT" ;;
    '.body // ""') printf '%s\n' "$TEST_BODY" ;;
    *auto_merge*) printf '%s\n' "$TEST_AUTO_MERGE" ;;
    *) echo "unexpected GitHub CLI query" >&2; return 98 ;;
  esac
}
'''
        script = "\n".join(
            [self.prelude, gh_stub, *self.functions, f'{function} 374 "$EXPECTED_HEAD"']
        )
        return subprocess.run(
            ["/bin/bash", "-ceu", script],
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=10,
        )

    def test_pr_identity_is_derived_from_the_app_and_not_commit_metadata(self) -> None:
        self.assertEqual(
            self.publisher["env"]["EXPECTED_PR_AUTHOR"],
            "${{ steps.publisher_app_token.outputs.app-slug }}[bot]",
        )
        self.assertEqual(self.workflow_env["UPDATER_NAME"], "github-actions[bot]")
        self.assertIn('git config user.name "$UPDATER_NAME"', self.script)
        self.assertIn('git config user.email "$UPDATER_EMAIL"', self.script)
        self.assertNotIn('[ "$pr_author" != "$UPDATER_NAME" ]', self.script)

    def test_open_and_merged_prs_accept_only_the_configured_app(self) -> None:
        for function in ("verify_open_draft_pr", "verify_merged_pr"):
            for author in ("easton97-jens-framework[bot]", "another-updater[bot]"):
                with self.subTest(function=function, author=author):
                    result = self.run_identity_check(
                        function, EXPECTED_PR_AUTHOR=author, TEST_AUTHOR=author
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)

    def test_open_and_merged_prs_reject_other_authors(self) -> None:
        for function in ("verify_open_draft_pr", "verify_merged_pr"):
            for author in ("github-actions[bot]", "another-updater[bot]", "human", ""):
                with self.subTest(function=function, author=author):
                    result = self.run_identity_check(function, TEST_AUTHOR=author)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertNotIn("unexpected GitHub CLI", result.stderr)

    def test_missing_or_malformed_app_identity_fails_closed(self) -> None:
        for author in ("", "[bot]", "plain-slug", "bad slug[bot]"):
            with self.subTest(author=author):
                result = self.run_identity_check(
                    "verify_open_draft_pr", EXPECTED_PR_AUTHOR=author
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Publisher App PR author is missing or malformed", result.stderr)

    def test_app_identity_does_not_bypass_other_open_pr_guards(self) -> None:
        cases = (
            {"TEST_STATE": "closed"},
            {"TEST_BASE": "other"},
            {"TEST_HEAD_BRANCH": "other"},
            {"TEST_HEAD_SHA": "b" * 40},
            {"TEST_DRAFT": "false"},
            {"TEST_TITLE": "unrelated"},
            {"TEST_BODY": ""},
            {"TEST_BODY": self.workflow_env["PR_MARKER"] + "\n" + self.workflow_env["PR_MARKER"]},
            {"TEST_AUTO_MERGE": "auto-merge-present"},
            {"TEST_HEAD_REPO": "other/project"},
            {"TEST_BASE_REPO": "other/project"},
        )
        for changes in cases:
            with self.subTest(changes=changes):
                result = self.run_identity_check("verify_open_draft_pr", **changes)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn("unexpected GitHub CLI", result.stderr)

    def test_app_identity_does_not_accept_an_unmerged_pr(self) -> None:
        for merged_at in ("", "null"):
            with self.subTest(merged_at=merged_at):
                result = self.run_identity_check(
                    "verify_merged_pr", TEST_MERGED_AT=merged_at
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("not updater-conformant", result.stderr)


if __name__ == "__main__":
    unittest.main()
