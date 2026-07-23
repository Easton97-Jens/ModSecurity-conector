"""Offline tests for the Parent Python workflow-version contract checker."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "ci" / "checks" / "common" / "check-python-version-contract.py"
FIXTURES = ROOT / "tests" / "fixtures" / "python-version-contract"


def load_checker() -> object:
    specification = importlib.util.spec_from_file_location(
        "python_version_contract_checker", CHECKER_PATH
    )
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


CHECKER = load_checker()


class PythonVersionContractTest(unittest.TestCase):
    def temporary_root(self) -> tempfile.TemporaryDirectory[str]:
        return tempfile.TemporaryDirectory(prefix="python-version-contract-")

    def cli_json_result(
        self, root: Path, *arguments: str
    ) -> tuple[int, dict[str, object]]:
        output = io.StringIO()
        with (
            mock.patch.object(CHECKER, "repository_root", return_value=root),
            contextlib.redirect_stdout(output),
        ):
            exit_code = CHECKER.main((*arguments, "--json"))
        return exit_code, json.loads(output.getvalue())

    def fixture_root_result(
        self,
        fixture_names: tuple[str, ...],
        expected_normal_jobs: set[object],
        expected_candidate_job: object | None = None,
    ) -> tuple[str, list[str], set[object]]:
        with self.temporary_root() as directory:
            root = Path(directory)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            for fixture_name in fixture_names:
                shutil.copy2(FIXTURES / fixture_name, workflows / fixture_name)
            version_file = root / ".python-version"
            version_file.write_text("3.14.6\n", encoding="utf-8")
            return CHECKER.evaluate_workflow_contract(
                root,
                version_file,
                expected_normal_jobs=expected_normal_jobs,
                expected_candidate_job=expected_candidate_job,
            )

    def fixture_result(self, fixture_name: str) -> tuple[str, list[str], set[object]]:
        identity = CHECKER.JobIdentity(fixture_name, "fixture-job")
        return self.fixture_root_result((fixture_name,), {identity})

    def assert_fixture_violation(self, fixture_name: str, expected: str) -> None:
        _, violations, _ = self.fixture_result(fixture_name)
        self.assertTrue(
            any(expected in violation for violation in violations),
            f"{fixture_name} did not report {expected!r}: {violations}",
        )

    def normal_job_block(self, job_name: str) -> str:
        return f'''  {job_name}:
    runs-on: ubuntu-latest
    steps:
      - name: Set up toolchain
        id: setup-python
        uses: actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0
        with:
          python-version-file: '.python-version'
          check-latest: false
      - name: Verify Python interpreter contract
        env:
          EXPECTED_PYTHON: ${{{{ steps.setup-python.outputs.python-path }}}}
        run: python3 ci/checks/common/check-python-interpreter-contract.py --version-file .python-version --expected-python "$EXPECTED_PYTHON"
      - name: Use Python
        run: python3 -c 'print("ok")'
'''

    def candidate_job_block(self) -> str:
        return '''  validate-python-patch:
    runs-on: ubuntu-latest
    steps:
      - name: Set up candidate Python
        id: setup-python
        uses: actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0
        with:
          python-version: ${{ needs.resolve-python-patch.outputs.version }}
          check-latest: false
      - name: Verify Python candidate interpreter contract
        env:
          EXPECTED_VERSION: ${{ needs.resolve-python-patch.outputs.version }}
          EXPECTED_PYTHON: ${{ steps.setup-python.outputs.python-path }}
        run: python3 ci/checks/common/check-python-interpreter-contract.py --expected-version "$EXPECTED_VERSION" --expected-python "$EXPECTED_PYTHON"
      - name: Validate candidate
        run: python3 scripts/update-python-version.py --check
'''

    def write_complete_contract_root(self, root: Path, candidate_override: str | None = None) -> None:
        by_workflow: dict[str, list[str]] = {}
        for identity in sorted(CHECKER.EXPECTED_NORMAL_PYTHON_JOBS):
            by_workflow.setdefault(identity.workflow, []).append(
                self.normal_job_block(identity.job)
            )
        special = CHECKER.CANDIDATE_VALIDATION_JOB
        by_workflow.setdefault(special.workflow, []).append(
            candidate_override if candidate_override is not None else self.candidate_job_block()
        )
        workflows = root / ".github" / "workflows"
        workflows.mkdir(parents=True)
        for workflow, jobs in by_workflow.items():
            (workflows / workflow).write_text(
                "name: generated test workflow\n\non:\n  workflow_dispatch:\n\njobs:\n"
                + "".join(jobs),
                encoding="utf-8",
            )
        (root / ".python-version").write_text("3.14.6\n", encoding="utf-8")

    def test_expected_inventory_has_27_normal_jobs_and_one_special_job(self) -> None:
        self.assertEqual(len(CHECKER.EXPECTED_NORMAL_PYTHON_JOBS), 27)
        self.assertNotIn(
            CHECKER.CANDIDATE_VALIDATION_JOB, CHECKER.EXPECTED_NORMAL_PYTHON_JOBS
        )

    def test_valid_yaml_control_is_accepted(self) -> None:
        version, violations, detected = self.fixture_result("valid-control.yaml")
        self.assertEqual(version, "3.14.6")
        self.assertEqual(violations, [])
        self.assertEqual(
            detected, {CHECKER.JobIdentity("valid-control.yaml", "fixture-job")}
        )

    def test_manual_mapping_parser_preserves_the_narrow_contract_shapes(self) -> None:
        self.assertEqual(CHECKER.mapping_entry("with:"), ("with", ""))
        self.assertEqual(
            CHECKER.mapping_entry("run: python3 -c 'print(\"value: preserved\")'"),
            ("run", "python3 -c 'print(\"value: preserved\")'"),
        )
        self.assertEqual(CHECKER.job_header("fixture-job: # comment"), "fixture-job")
        self.assertIsNone(CHECKER.job_header("fixture-job: unexpected-value"))
        self.assertIsNone(CHECKER.mapping_entry("not a mapping"))

    def test_structural_version_and_executable_recognition_remain_ascii_only(self) -> None:
        for version in ("3.14.0", "3.14.1", "3.14.6"):
            with self.subTest(version=version):
                self.assertEqual(version, CHECKER.parse_exact_version(version, "test"))

        dotted_patch = ".".join(("3", "14", "1", "0"))
        for version in ("3.14.01", "3.14.\u0661", dotted_patch, "3.15.1"):
            with self.subTest(version=version), self.assertRaises(
                CHECKER.ContractInputError
            ):
                CHECKER.parse_exact_version(version, "test")

        for command in ("python", "python3.14.6", "pip", "pip3.14"):
            with self.subTest(command=command):
                self.assertTrue(CHECKER.is_python_or_pip_command(command))

        for command in ("python3.14.", "python3.14.\u0661", "pythonx", "pipy"):
            with self.subTest(command=command):
                self.assertFalse(CHECKER.is_python_or_pip_command(command))

    def test_linear_shell_parser_detects_commands_without_text_false_positives(self) -> None:
        self.assertEqual(
            CHECKER.direct_python_or_pip_command(
                "/opt/toolchains/python3.14 -c 'print(\"direct\")'"
            ),
            "python3.14",
        )
        self.assertEqual(
            CHECKER.bare_pip_command("env TOOLCHAIN=checked pip3 --version"),
            "pip3",
        )
        self.assertEqual(CHECKER.python_make_target("make quick-check"), "quick-check")
        self.assertEqual(
            CHECKER.direct_python_or_pip_command(
                "status=$(python3 -c 'print(\"substitution\")')"
            ),
            "python3",
        )
        self.assertIsNone(CHECKER.shell_syntax_error("count=$((count + 1))"))

        harmless = CHECKER.analyze_shell_source(
            """# python3 and pip are comments, not commands.
echo \"python3 -m pip --version\"
cat <<'TEXT'
python3 -m pip --version
TEXT
printf '%s\\n' 'make quick-check'
"""
        )
        self.assertEqual(harmless.errors, ())
        command_names = [
            CHECKER.static_command_basename(command.command)
            for command in harmless.commands
        ]
        self.assertEqual(command_names, ["echo", "cat", "printf"])

    def test_unsupported_or_malformed_shell_syntax_fails_closed(self) -> None:
        self.assertEqual(
            CHECKER.shell_syntax_error('"$PYTHON" --version'),
            "dynamic shell command head is unsupported",
        )
        malformed_error = CHECKER.shell_syntax_error("python3 -c 'unterminated")
        self.assertIsNotNone(malformed_error)
        self.assertIn("unterminated", malformed_error)
        arithmetic_error = CHECKER.shell_syntax_error(
            "count=$(( $(python3 --version) + 1 ))"
        )
        self.assertIsNotNone(arithmetic_error)
        self.assertIn("arithmetic expansion", arithmetic_error)

    def test_missing_setup_is_rejected(self) -> None:
        self.assert_fixture_violation("missing-setup.yml", "must contain exactly one")

    def test_minor_patch_and_floating_selectors_are_rejected(self) -> None:
        for fixture in (
            "wrong-minor.yml",
            "wrong-patch.yml",
            "selector-3x.yml",
            "selector-latest.yml",
            "selector-matrix.yml",
        ):
            with self.subTest(fixture=fixture):
                self.assert_fixture_violation(fixture, "must not use python-version selectors")

    def test_python_and_pip_before_setup_are_rejected(self) -> None:
        for fixture in (
            "python-before-setup.yml",
            "pip-before-setup.yml",
            "python314-before-setup.yml",
            "versioned-python-before-setup.yml",
            "python-command-substitution-before-setup.yml",
        ):
            with self.subTest(fixture=fixture):
                self.assert_fixture_violation(fixture, "first Python use")

    def test_absent_and_non_equivalent_verifiers_are_rejected(self) -> None:
        self.assert_fixture_violation("verifier-absent.yml", "lacks exactly one")
        self.assert_fixture_violation("verifier-not-equivalent.yml", "EXPECTED_PYTHON")

    def test_setup_python_reference_requires_full_sha_and_v700_comment(self) -> None:
        for fixture in (
            "setup-python-mutable-tag.yml",
            "setup-python-short-sha.yml",
            "setup-python-missing-comment.yml",
            "setup-python-wrong-comment.yml",
        ):
            with self.subTest(fixture=fixture):
                self.assert_fixture_violation(
                    fixture,
                    "actions/setup-python must use exactly "
                    "actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0",
                )

    def test_bare_pip_and_pip3_are_rejected_after_verified_setup(self) -> None:
        for fixture, command in (
            ("bare-pip.yml", "'pip'"),
            ("bare-pip3.yml", "'pip3'"),
        ):
            with self.subTest(fixture=fixture):
                self.assert_fixture_violation(fixture, f"bare pip command {command}")

    def test_make_inline_heredoc_and_python_module_pip_are_detected(self) -> None:
        for fixture in (
            "make-after-setup.yml",
            "inline-python-heredoc.yml",
            "python-module-pip.yml",
        ):
            with self.subTest(fixture=fixture):
                _, violations, detected = self.fixture_result(fixture)
                self.assertEqual(violations, [], violations)
                self.assertEqual(
                    detected, {CHECKER.JobIdentity(fixture, "fixture-job")}
                )

        self.assert_fixture_violation("make-before-setup.yml", "Make target quick-check")

    def test_python_matrix_axis_is_classified_and_rejected(self) -> None:
        for fixture in (
            "matrix-python-selector.yml",
            "matrix-version-selector.yml",
        ):
            with self.subTest(fixture=fixture):
                _, violations, detected = self.fixture_result(fixture)
                self.assertEqual(
                    detected, {CHECKER.JobIdentity(fixture, "fixture-job")}
                )
                self.assertTrue(
                    any(
                        "Python-related matrix selector" in violation
                        for violation in violations
                    ),
                    violations,
                )

    def test_shell_only_job_is_not_a_python_false_positive(self) -> None:
        _, violations, detected = self.fixture_root_result(
            ("shell-only.yml",), set()
        )
        self.assertEqual(violations, [], violations)
        self.assertEqual(set(), detected)

    def test_multiple_python_jobs_are_inventory_checked_independently(self) -> None:
        expected = {
            CHECKER.JobIdentity("multiple-python-jobs.yml", "python-one"),
            CHECKER.JobIdentity("multiple-python-jobs.yml", "python-two"),
        }
        _, violations, detected = self.fixture_root_result(
            ("multiple-python-jobs.yml",), expected
        )
        self.assertEqual(violations, [], violations)
        self.assertEqual(expected, detected)

    def test_local_reusable_workflow_caller_is_rejected_not_silently_ignored(self) -> None:
        callee = CHECKER.JobIdentity("reusable-callee.yml", "callee-python")
        _, safe_violations, safe_detected = self.fixture_root_result(
            ("reusable-callee.yml",), {callee}
        )
        self.assertEqual(safe_violations, [], safe_violations)
        self.assertEqual(safe_detected, {callee})

        caller = CHECKER.JobIdentity("reusable-caller.yml", "call-local-python")
        _, violations, detected = self.fixture_root_result(
            ("reusable-callee.yml", "reusable-caller.yml"), {callee}
        )
        self.assertIn(caller, detected)
        self.assertTrue(
            any(
                "unlisted Python-related workflow job: reusable-caller.yml:call-local-python"
                in violation
                and "job-level reusable workflow invocation" in violation
                for violation in violations
            ),
            violations,
        )

    def test_malformed_canonical_version_is_an_input_error(self) -> None:
        with self.temporary_root() as directory:
            root = Path(directory)
            (root / ".github" / "workflows").mkdir(parents=True)
            shutil.copy2(FIXTURES / "malformed-version.txt", root / ".python-version")
            exit_code, payload = self.cli_json_result(root)
        self.assertEqual(exit_code, 2)
        self.assertEqual(payload["status"], "error")
        self.assertIn("exact Python 3.14.N", payload["violations"][0])

    def test_json_cli_reports_contract_violations_with_exit_one(self) -> None:
        with self.temporary_root() as directory:
            root = Path(directory)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            shutil.copy2(FIXTURES / "missing-setup.yml", workflows / "missing-setup.yml")
            (root / ".python-version").write_text("3.14.6\n", encoding="utf-8")
            exit_code, payload = self.cli_json_result(root)
        self.assertEqual(exit_code, 1)
        self.assertEqual(payload["status"], "violations")
        self.assertTrue(payload["violations"])

    def test_public_cli_rejects_user_controlled_root_and_nonliteral_version_file(self) -> None:
        stderr = io.StringIO()
        argument_parser = CHECKER.parser()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit) as context:
            argument_parser.parse_args(["--root", "/not-a-repository"])
        self.assertEqual(context.exception.code, 2)

        output = io.StringIO()
        with (
            mock.patch.object(
                CHECKER,
                "repository_root",
                side_effect=AssertionError("repository root must not be resolved"),
            ),
            contextlib.redirect_stdout(output),
        ):
            exit_code = CHECKER.main(
                ["--version-file", "../untrusted-version", "--json"]
            )
        self.assertEqual(exit_code, 2)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["status"], "error")
        self.assertIn("must be exactly", payload["violations"][0])

    def test_public_cli_requires_a_regular_nonsymlink_canonical_version_file(self) -> None:
        with self.temporary_root() as directory:
            root = Path(directory)
            target = root / "version-source"
            target.write_text("3.14.6\n", encoding="utf-8")
            (root / ".python-version").symlink_to(target)
            exit_code, payload = self.cli_json_result(root)
        self.assertEqual(exit_code, 2)
        self.assertIn("must not be a symlink", payload["violations"][0])

        with self.temporary_root() as directory:
            root = Path(directory)
            (root / ".python-version").mkdir()
            exit_code, payload = self.cli_json_result(root)
        self.assertEqual(exit_code, 2)
        self.assertIn("must be a regular file", payload["violations"][0])

    def test_downgrade_requires_explicit_authorization(self) -> None:
        with self.temporary_root() as directory:
            root = Path(directory)
            (root / ".github" / "workflows").mkdir(parents=True)
            version_file = root / ".python-version"
            version_file.write_text("3.14.5\n", encoding="utf-8")
            _, blocked, _ = CHECKER.evaluate_workflow_contract(
                root,
                version_file,
                previous_version="3.14.6",
                expected_normal_jobs=(),
                expected_candidate_job=None,
            )
            _, authorized, _ = CHECKER.evaluate_workflow_contract(
                root,
                version_file,
                previous_version="3.14.6",
                allow_downgrade=True,
                expected_normal_jobs=(),
                expected_candidate_job=None,
            )
        self.assertTrue(any("downgrade" in violation for violation in blocked))
        self.assertEqual(authorized, [])

    def test_special_candidate_job_is_strict_about_expected_outputs(self) -> None:
        malformed = self.candidate_job_block().replace(
            "${{ needs.resolve-python-patch.outputs.version }}",
            "${{ needs.untrusted.outputs.version }}",
            1,
        )
        with self.temporary_root() as directory:
            root = Path(directory)
            self.write_complete_contract_root(root, candidate_override=malformed)
            _, violations, _ = CHECKER.evaluate_workflow_contract(
                root, root / ".python-version"
            )
        self.assertTrue(
            any("candidate setup-python must use exactly" in violation for violation in violations),
            violations,
        )

    def test_json_cli_accepts_complete_contract(self) -> None:
        with self.temporary_root() as directory:
            root = Path(directory)
            self.write_complete_contract_root(root)
            exit_code, payload = self.cli_json_result(root)
        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["status"], "valid")
        self.assertEqual(len(payload["detected_python_jobs"]), 28)


if __name__ == "__main__":
    unittest.main()
