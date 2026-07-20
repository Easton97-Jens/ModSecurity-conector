"""Offline tests for the Parent Python workflow-version contract checker."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


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
        return tempfile.TemporaryDirectory(
            prefix="python-version-contract-", dir=os.environ.get("TMPDIR")
        )

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
            version_file.write_text("3.13.14\n", encoding="utf-8")
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
        uses: actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1 # v6.3.0
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
        uses: actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1 # v6.3.0
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
        (root / ".python-version").write_text("3.13.14\n", encoding="utf-8")

    def test_expected_inventory_has_24_normal_jobs_and_one_special_job(self) -> None:
        self.assertEqual(24, len(CHECKER.EXPECTED_NORMAL_PYTHON_JOBS))
        self.assertNotIn(
            CHECKER.CANDIDATE_VALIDATION_JOB, CHECKER.EXPECTED_NORMAL_PYTHON_JOBS
        )

    def test_valid_yaml_control_is_accepted(self) -> None:
        version, violations, detected = self.fixture_result("valid-control.yaml")
        self.assertEqual("3.13.14", version)
        self.assertEqual([], violations)
        self.assertEqual(
            {CHECKER.JobIdentity("valid-control.yaml", "fixture-job")}, detected
        )

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
            "python313-before-setup.yml",
            "versioned-python-before-setup.yml",
            "python-command-substitution-before-setup.yml",
        ):
            with self.subTest(fixture=fixture):
                self.assert_fixture_violation(fixture, "first Python use")

    def test_absent_and_non_equivalent_verifiers_are_rejected(self) -> None:
        self.assert_fixture_violation("verifier-absent.yml", "lacks exactly one")
        self.assert_fixture_violation("verifier-not-equivalent.yml", "EXPECTED_PYTHON")

    def test_setup_python_reference_requires_full_sha_and_v630_comment(self) -> None:
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
                    "actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1 # v6.3.0",
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
                self.assertEqual([], violations, violations)
                self.assertEqual(
                    {CHECKER.JobIdentity(fixture, "fixture-job")}, detected
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
                    {CHECKER.JobIdentity(fixture, "fixture-job")}, detected
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
        self.assertEqual([], violations, violations)
        self.assertEqual(set(), detected)

    def test_multiple_python_jobs_are_inventory_checked_independently(self) -> None:
        expected = {
            CHECKER.JobIdentity("multiple-python-jobs.yml", "python-one"),
            CHECKER.JobIdentity("multiple-python-jobs.yml", "python-two"),
        }
        _, violations, detected = self.fixture_root_result(
            ("multiple-python-jobs.yml",), expected
        )
        self.assertEqual([], violations, violations)
        self.assertEqual(expected, detected)

    def test_local_reusable_workflow_caller_is_rejected_not_silently_ignored(self) -> None:
        callee = CHECKER.JobIdentity("reusable-callee.yml", "callee-python")
        _, safe_violations, safe_detected = self.fixture_root_result(
            ("reusable-callee.yml",), {callee}
        )
        self.assertEqual([], safe_violations, safe_violations)
        self.assertEqual({callee}, safe_detected)

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
            completed = subprocess.run(
                [
                    sys.executable,
                    str(CHECKER_PATH),
                    "--root",
                    str(root),
                    "--json",
                ],
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        self.assertEqual(2, completed.returncode)
        payload = json.loads(completed.stdout)
        self.assertEqual("error", payload["status"])
        self.assertIn("exact Python 3.13.N", payload["violations"][0])

    def test_json_cli_reports_contract_violations_with_exit_one(self) -> None:
        with self.temporary_root() as directory:
            root = Path(directory)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            shutil.copy2(FIXTURES / "missing-setup.yml", workflows / "missing-setup.yml")
            (root / ".python-version").write_text("3.13.14\n", encoding="utf-8")
            completed = subprocess.run(
                [
                    sys.executable,
                    str(CHECKER_PATH),
                    "--root",
                    str(root),
                    "--json",
                ],
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        self.assertEqual(1, completed.returncode)
        payload = json.loads(completed.stdout)
        self.assertEqual("violations", payload["status"])
        self.assertTrue(payload["violations"])

    def test_downgrade_requires_explicit_authorization(self) -> None:
        with self.temporary_root() as directory:
            root = Path(directory)
            (root / ".github" / "workflows").mkdir(parents=True)
            version_file = root / ".python-version"
            version_file.write_text("3.13.13\n", encoding="utf-8")
            _, blocked, _ = CHECKER.evaluate_workflow_contract(
                root,
                version_file,
                previous_version="3.13.14",
                expected_normal_jobs=(),
                expected_candidate_job=None,
            )
            _, authorized, _ = CHECKER.evaluate_workflow_contract(
                root,
                version_file,
                previous_version="3.13.14",
                allow_downgrade=True,
                expected_normal_jobs=(),
                expected_candidate_job=None,
            )
        self.assertTrue(any("downgrade" in violation for violation in blocked))
        self.assertEqual([], authorized)

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
            completed = subprocess.run(
                [
                    sys.executable,
                    str(CHECKER_PATH),
                    "--root",
                    str(root),
                    "--json",
                ],
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        self.assertEqual(0, completed.returncode, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual("valid", payload["status"])
        self.assertEqual(25, len(payload["detected_python_jobs"]))


if __name__ == "__main__":
    unittest.main()
