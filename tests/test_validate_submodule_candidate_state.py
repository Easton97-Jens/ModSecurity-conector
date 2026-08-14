from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "ci/tools/validate-submodule-candidate-state.py"


class ValidateSubmoduleCandidateStateTests(unittest.TestCase):
    def git(self, directory: Path, *arguments: str) -> str:
        completed = subprocess.run(
            ["git", "-C", str(directory), *arguments], check=True, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        return completed.stdout.strip()

    def commit_file(self, repository: Path, name: str, content: str, message: str) -> str:
        (repository / name).write_text(content, encoding="utf-8")
        self.git(repository, "add", name)
        self.git(repository, "commit", "-m", message)
        return self.git(repository, "rev-parse", "HEAD")

    def make_layout(self, temporary: Path, *, nested: bool = False) -> tuple[Path, Path, str, str]:
        framework = temporary / "framework-source"
        framework.mkdir()
        self.git(framework, "init")
        self.git(framework, "config", "user.email", "test@example.invalid")
        self.git(framework, "config", "user.name", "Validator Test")
        framework_a = self.commit_file(framework, "framework.txt", "A\n", "framework A")
        if nested:
            nested_source = temporary / "nested-source"
            nested_source.mkdir()
            self.git(nested_source, "init")
            self.git(nested_source, "config", "user.email", "test@example.invalid")
            self.git(nested_source, "config", "user.name", "Validator Test")
            self.commit_file(nested_source, "nested.txt", "nested\n", "nested")
            self.git(framework, "-c", "protocol.file.allow=always", "submodule", "add", str(nested_source), "nested")
            self.git(framework, "commit", "-m", "add nested")
            framework_a = self.git(framework, "rev-parse", "HEAD")

        parent = temporary / "parent"
        parent.mkdir()
        self.git(parent, "init")
        self.git(parent, "config", "user.email", "test@example.invalid")
        self.git(parent, "config", "user.name", "Validator Test")
        self.commit_file(parent, "README", "parent\n", "parent")
        self.git(parent, "-c", "protocol.file.allow=always", "submodule", "add", str(framework), "framework")
        # The submodule clone deliberately does not inherit the source
        # repository's local identity. Configure this fixture worktree so the
        # forward-candidate commits are independent of a developer's global
        # Git configuration, as they are on GitHub-hosted runners.
        self.git(parent / "framework", "config", "user.email", "test@example.invalid")
        self.git(parent / "framework", "config", "user.name", "Validator Test")
        self.git(parent, "commit", "-m", "add framework")
        if nested:
            self.git(parent, "-c", "protocol.file.allow=always", "submodule", "update", "--init", "--recursive")
        parent_head = self.git(parent, "rev-parse", "HEAD")
        return parent, parent / "framework", framework_a, parent_head

    def capture_result(
        self, parent: Path, environment: Path, *, runner_temp: Path | None = None
    ) -> subprocess.CompletedProcess[str]:
        command_environment = os.environ.copy()
        command_environment["RUNNER_TEMP"] = str(runner_temp or environment.parent)
        return subprocess.run(
            [sys.executable, str(VALIDATOR), "capture-parent-baseline", "--parent-root", str(parent), "--github-env", str(environment)],
            check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            env=command_environment,
            timeout=10,
        )

    def run_capture(self, parent: Path, environment: Path) -> dict[str, str]:
        environment.touch()
        result = self.capture_result(parent, environment)
        self.assertEqual(result.returncode, 0, result.stderr)
        return dict(line.split("=", 1) for line in environment.read_text(encoding="utf-8").splitlines())

    def run_validate(
        self,
        parent: Path,
        baseline: dict[str, str],
        current: str,
        candidate: str,
        *,
        submodule_path: str = "framework",
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable, str(VALIDATOR), "validate", "--parent-root", str(parent),
                "--submodule-path", submodule_path, "--current-gitlink-sha", current,
                "--candidate-sha", candidate, "--expected-parent-head", baseline["EXPECTED_PARENT_HEAD"],
                "--expected-parent-hooks-sha256", baseline["EXPECTED_PARENT_HOOKS_SHA256"],
            ], check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )

    def assert_code(self, result: subprocess.CompletedProcess[str], code: str) -> None:
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(result.stderr.startswith(f"ERROR:{code}"), result.stderr)

    def test_noop_and_forward_candidate_allow_only_gitlink_worktree_divergence(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            parent, framework, current, _head = self.make_layout(Path(raw))
            baseline = self.run_capture(parent, Path(raw) / "github-env")
            noop = self.run_validate(parent, baseline, current, current)
            self.assertEqual(noop.returncode, 0, noop.stderr)
            candidate = self.commit_file(framework, "framework.txt", "B\n", "framework B")
            forward = self.run_validate(parent, baseline, current, candidate)
            self.assertEqual(forward.returncode, 0, forward.stderr)

    def test_parent_changes_and_wrong_candidate_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            parent, framework, current, _head = self.make_layout(Path(raw))
            baseline = self.run_capture(parent, Path(raw) / "github-env")
            candidate = self.commit_file(framework, "framework.txt", "B\n", "framework B")
            (parent / "README").write_text("changed\n", encoding="utf-8")
            self.git(parent, "add", "README")
            staged = self.run_validate(parent, baseline, current, candidate)
            self.assert_code(staged, "PARENT_OUTSIDE_SUBMODULE_DIRTY")
            self.assertIn('state="index"', staged.stderr)
            self.assertIn('paths=["README"]', staged.stderr)
            self.git(parent, "reset", "README")
            self.assert_code(self.run_validate(parent, baseline, current, candidate), "PARENT_OUTSIDE_SUBMODULE_DIRTY")
            self.git(parent, "checkout", "--", "README")
            (parent / "untracked").write_text("x", encoding="utf-8")
            self.assert_code(self.run_validate(parent, baseline, current, candidate), "PARENT_OUTSIDE_SUBMODULE_DIRTY")
            (parent / "untracked").unlink()
            self.assert_code(self.run_validate(parent, baseline, current, current), "FRAMEWORK_CANDIDATE_MISMATCH")

    def test_parent_head_change_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            parent, framework, current, _head = self.make_layout(Path(raw))
            baseline = self.run_capture(parent, Path(raw) / "github-env")
            self.commit_file(parent, "later", "later\n", "later")
            self.assert_code(self.run_validate(parent, baseline, current, current), "PARENT_HEAD_CHANGED")

    def test_malformed_revision_argument_is_rejected_before_git_state_checks(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            parent, _framework, current, _head = self.make_layout(Path(raw))
            baseline = self.run_capture(parent, Path(raw) / "github-env")
            self.assert_code(self.run_validate(parent, baseline, current, "short"), "CANDIDATE_SHA_INVALID")

    def test_capture_rejects_github_env_outside_runner_temp_or_via_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            temporary = Path(raw)
            parent, _framework, _current, _head = self.make_layout(temporary)
            runner_temp = temporary / "runner-temp"
            runner_temp.mkdir()
            outside = temporary / "outside-env"
            outside.touch()
            self.assert_code(
                self.capture_result(parent, outside, runner_temp=runner_temp), "GITHUB_ENV_INVALID"
            )
            traversal = runner_temp / ".." / "outside-env"
            self.assert_code(
                self.capture_result(parent, traversal, runner_temp=runner_temp), "GITHUB_ENV_INVALID"
            )
            symlink = runner_temp / "symlink-env"
            symlink.symlink_to(outside)
            self.assert_code(
                self.capture_result(parent, symlink, runner_temp=runner_temp), "GITHUB_ENV_INVALID"
            )
            hardlink = runner_temp / "hardlink-env"
            os.link(outside, hardlink)
            self.assert_code(
                self.capture_result(parent, hardlink, runner_temp=runner_temp), "GITHUB_ENV_INVALID"
            )
            fifo = runner_temp / "fifo-env"
            os.mkfifo(fifo)
            self.assert_code(
                self.capture_result(parent, fifo, runner_temp=runner_temp), "GITHUB_ENV_INVALID"
            )
            linked_directory = runner_temp / "linked-directory"
            linked_directory.symlink_to(temporary)
            self.assert_code(
                self.capture_result(
                    parent, linked_directory / "outside-env", runner_temp=runner_temp
                ),
                "GITHUB_ENV_INVALID",
            )
            self.assertEqual(outside.read_text(encoding="utf-8"), "")

    def test_capture_rejects_missing_runner_temp_and_accepts_runner_file(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            temporary = Path(raw)
            parent, _framework, _current, _head = self.make_layout(temporary)
            runner_temp = temporary / "runner-temp"
            runner_temp.mkdir()
            environment = runner_temp / "github-env"
            environment.touch()
            success = self.capture_result(parent, environment, runner_temp=runner_temp)
            self.assertEqual(success.returncode, 0, success.stderr)
            missing_root = temporary / "missing-runner-temp"
            self.assert_code(
                self.capture_result(parent, environment, runner_temp=missing_root), "GITHUB_ENV_INVALID"
            )
            os.chmod(runner_temp, 0o777)
            self.assert_code(
                self.capture_result(parent, environment, runner_temp=runner_temp), "GITHUB_ENV_INVALID"
            )
            self.assert_code(
                self.capture_result(parent, environment, runner_temp=Path("/")), "GITHUB_ENV_INVALID"
            )

    def test_capture_rejects_missing_and_unsafe_hook_inventory_entries(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            temporary = Path(raw)
            parent, _framework, _current, _head = self.make_layout(temporary)
            hooks = Path(self.git(parent, "rev-parse", "--git-path", "hooks"))
            if not hooks.is_absolute():
                hooks = parent / hooks

            def capture_error(name: str, code: str) -> None:
                environment = temporary / f"github-env-{name}"
                environment.touch()
                self.assert_code(self.capture_result(parent, environment), code)

            backup = hooks.with_name("hooks-backup")
            hooks.rename(backup)
            capture_error("missing", "PARENT_HOOKS_MISSING")
            hooks.write_text("not a directory\n", encoding="utf-8")
            capture_error("file", "PARENT_HOOKS_UNSAFE")
            hooks.unlink()
            hooks.symlink_to(backup, target_is_directory=True)
            capture_error("symlink", "PARENT_HOOKS_UNSAFE")
            hooks.unlink()
            hooks.mkdir()
            (hooks / "symlink-entry").symlink_to(backup, target_is_directory=True)
            capture_error("entry-symlink", "PARENT_HOOKS_UNSAFE")
            (hooks / "symlink-entry").unlink()
            os.mkfifo(hooks / "special-entry")
            capture_error("entry-special", "PARENT_HOOKS_UNSAFE")

    def test_submodule_path_escape_arguments_are_rejected_before_path_construction(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            parent, _framework, current, _head = self.make_layout(Path(raw))
            baseline = self.run_capture(parent, Path(raw) / "github-env")
            for malicious_path in ("../framework", "framework/../README", "/tmp/framework", ":(top)framework"):
                with self.subTest(malicious_path=malicious_path):
                    result = self.run_validate(
                        parent, baseline, current, current, submodule_path=malicious_path
                    )
                    self.assert_code(result, "SUBMODULE_PATH_INVALID")

    def test_framework_and_recursive_nested_dirty_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            parent, framework, current, _head = self.make_layout(Path(raw), nested=True)
            baseline = self.run_capture(parent, Path(raw) / "github-env")
            (framework / "framework.txt").write_text("changed\n", encoding="utf-8")
            tracked_dirty = self.run_validate(parent, baseline, current, current)
            self.assert_code(tracked_dirty, "FRAMEWORK_DIRTY")
            self.assertIn('state="worktree"', tracked_dirty.stderr)
            self.git(framework, "checkout", "--", "framework.txt")
            (framework / "untracked").write_text("x", encoding="utf-8")
            self.assert_code(self.run_validate(parent, baseline, current, current), "FRAMEWORK_DIRTY")
            (framework / "untracked").unlink()
            (framework / "nested" / "untracked").write_text("x", encoding="utf-8")
            self.assert_code(self.run_validate(parent, baseline, current, current), "FRAMEWORK_SUBMODULE_DIRTY")

    def test_staged_parent_or_recursive_gitlink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            parent, framework, current, _head = self.make_layout(Path(raw), nested=True)
            baseline = self.run_capture(parent, Path(raw) / "github-env")
            candidate = self.commit_file(framework, "framework.txt", "B\n", "framework B")

            # A staged Parent Gitlink must not be confused with the allowed
            # unstaged worktree candidate divergence.
            self.git(parent, "add", "framework")
            staged_parent = self.run_validate(parent, baseline, current, candidate)
            self.assert_code(staged_parent, "PARENT_OUTSIDE_SUBMODULE_DIRTY")
            self.assertIn('scope="parent-index"', staged_parent.stderr)
            self.assertIn('state="index"', staged_parent.stderr)
            self.git(parent, "reset", "framework")

            # A staged recursive Gitlink was previously hidden by the nested
            # path exclusion.  The Framework index must now be globally clean.
            nested = framework / "nested"
            self.git(nested, "config", "user.email", "test@example.invalid")
            self.git(nested, "config", "user.name", "Validator Test")
            self.commit_file(nested, "nested.txt", "changed\n", "nested B")
            self.git(framework, "add", "nested")
            staged_nested = self.run_validate(parent, baseline, current, candidate)
            self.assert_code(staged_nested, "FRAMEWORK_DIRTY")
            self.assertIn('scope="framework-index"', staged_nested.stderr)
            self.assertIn('state="index"', staged_nested.stderr)

    def test_hook_and_gitmodules_mutation_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            parent, framework, current, _head = self.make_layout(Path(raw))
            environment = Path(raw) / "github-env"
            baseline = self.run_capture(parent, environment)
            hooks = Path(self.git(parent, "rev-parse", "--git-path", "hooks"))
            if not hooks.is_absolute():
                hooks = parent / hooks
            (hooks / "pre-commit").write_text("#!/bin/sh\n", encoding="utf-8")
            self.assert_code(self.run_validate(parent, baseline, current, current), "PARENT_HOOKS_CHANGED")
            (hooks / "pre-commit").unlink()
            (parent / ".gitmodules").write_text("[submodule \"other\"]\n\tpath = other\n", encoding="utf-8")
            self.assert_code(self.run_validate(parent, baseline, current, current), "PARENT_GITMODULES_INVALID")


if __name__ == "__main__":
    unittest.main()
