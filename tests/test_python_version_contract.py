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
        directory = tempfile.TemporaryDirectory(prefix="python-version-contract-")
        lock = Path(directory.name) / "ci" / "tooling" / "security-tools.lock.yml"
        lock.parent.mkdir(parents=True)
        shutil.copy2(ROOT / "ci" / "tooling" / "security-tools.lock.yml", lock)
        return directory

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
        (root / ".python-version").write_text("3.13.14\n", encoding="utf-8")

    def test_expected_inventory_has_29_normal_jobs_and_one_special_job(self) -> None:
        self.assertEqual(29, len(CHECKER.EXPECTED_NORMAL_PYTHON_JOBS))
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

    def test_manual_mapping_parser_preserves_the_narrow_contract_shapes(self) -> None:
        self.assertEqual(("with", ""), CHECKER.mapping_entry("with:"))
        self.assertEqual(
            ("run", "python3 -c 'print(\"value: preserved\")'"),
            CHECKER.mapping_entry("run: python3 -c 'print(\"value: preserved\")'"),
        )
        self.assertEqual("fixture-job", CHECKER.job_header("fixture-job: # comment"))
        self.assertIsNone(CHECKER.job_header("fixture-job: unexpected-value"))
        self.assertIsNone(CHECKER.mapping_entry("not a mapping"))

    def test_noncanonical_semantic_job_headers_fail_closed(self) -> None:
        """No Python-bearing YAML job may be hidden from the raw source parser."""

        variants = {
            "quoted": '  "hidden-python":\n    runs-on: ubuntu-latest\n    steps:\n      - run: python3 --version\n',
            "escaped": '  "hidden-\\x70ython":\n    runs-on: ubuntu-latest\n    steps:\n      - run: python3 --version\n',
            "explicit": '  ? hidden-python\n  :\n    runs-on: ubuntu-latest\n    steps:\n      - run: python3 --version\n',
            "flow": "  hidden-python: {runs-on: ubuntu-latest, steps: [{run: python3 --version}]}\n",
            "flow-steps": "  hidden-python:\n    runs-on: ubuntu-latest\n    steps: [{run: python3 --version}]\n",
            "flow-step": "  hidden-python:\n    runs-on: ubuntu-latest\n    steps:\n      - {run: python3 --version}\n",
            "quoted-steps": '  hidden-python:\n    runs-on: ubuntu-latest\n    "steps":\n      - run: python3 --version\n',
            "escaped-run": '  hidden-python:\n    runs-on: ubuntu-latest\n    steps:\n      - "\\x72un": python3 --version\n',
            "comment-steps": "  hidden-python:\n    runs-on: ubuntu-latest\n    steps: # ordinary YAML comment\n      - run: python3 --version\n",
            "space-before-steps-colon": "  hidden-python:\n    runs-on: ubuntu-latest\n    steps :\n      - run: python3 --version\n",
            "bare-sequence-marker": "  hidden-python:\n    runs-on: ubuntu-latest\n    steps:\n      -\n        run: python3 --version\n",
            "three-space-field": "  hidden-python:\n   runs-on: ubuntu-latest\n   steps:\n     - run: python3 --version\n",
            "five-space-sequence": "  hidden-python:\n    runs-on: ubuntu-latest\n    steps:\n     - run: python3 --version\n",
            "space-before-run-colon": "  hidden-python:\n    runs-on: ubuntu-latest\n    steps:\n      - run : python3 --version\n",
        }
        for spelling, hidden_job in variants.items():
            with self.subTest(spelling=spelling), self.temporary_root() as directory:
                root = Path(directory)
                workflow_dir = root / ".github" / "workflows"
                workflow_dir.mkdir(parents=True)
                (workflow_dir / "noncanonical.yml").write_text(
                    "name: noncanonical\non: workflow_dispatch\njobs:\n"
                    + self.normal_job_block("fixture-job")
                    + hidden_job,
                    encoding="utf-8",
                )
                (root / ".python-version").write_text("3.13.14\n", encoding="utf-8")
                _, violations, detected = CHECKER.evaluate_workflow_contract(
                    root,
                    root / ".python-version",
                    expected_normal_jobs={CHECKER.JobIdentity("noncanonical.yml", "fixture-job")},
                    expected_candidate_job=None,
                )
                self.assertEqual(
                    {
                        CHECKER.JobIdentity("noncanonical.yml", "fixture-job"),
                        CHECKER.JobIdentity("noncanonical.yml", "hidden-python"),
                    },
                    detected,
                )
                self.assertTrue(
                    any(
                        "unlisted Python-related workflow job: noncanonical.yml:hidden-python" in violation
                        for violation in violations
                    ),
                    violations,
                )

        with self.temporary_root() as directory:
            root = Path(directory)
            workflow_dir = root / ".github" / "workflows"
            workflow_dir.mkdir(parents=True)
            (workflow_dir / "aliased.yml").write_text(
                "name: aliased\non: workflow_dispatch\n"
                "base_steps: &base_steps\n  - run: python3 --version\n"
                "jobs:\n  fixture-job:\n    runs-on: ubuntu-latest\n    steps: *base_steps\n",
                encoding="utf-8",
            )
            (root / ".python-version").write_text("3.13.14\n", encoding="utf-8")
            _, violations, detected = CHECKER.evaluate_workflow_contract(
                root,
                root / ".python-version",
                expected_normal_jobs={CHECKER.JobIdentity("aliased.yml", "fixture-job")},
                expected_candidate_job=None,
            )
            self.assertEqual(
                {CHECKER.JobIdentity("aliased.yml", "fixture-job")}, detected
            )
            self.assertTrue(any("uses Python" in violation for violation in violations), violations)

    def test_structural_version_and_executable_recognition_remain_ascii_only(self) -> None:
        for version in ("3.13.0", "3.13.1", "3.13.14"):
            with self.subTest(version=version):
                self.assertEqual(version, CHECKER.parse_exact_version(version, "test"))

        dotted_patch = ".".join(("3", "13", "1", "0"))
        for version in ("3.13.01", "3.13.\u0661", dotted_patch, "3.14.1"):
            with self.subTest(version=version), self.assertRaises(
                CHECKER.ContractInputError
            ):
                CHECKER.parse_exact_version(version, "test")

        for command in ("python", "python3.13.14", "pip", "pip3.13"):
            with self.subTest(command=command):
                self.assertTrue(CHECKER.is_python_or_pip_command(command))

        for command in ("python3.13.", "python3.13.\u0661", "pythonx", "pipy"):
            with self.subTest(command=command):
                self.assertFalse(CHECKER.is_python_or_pip_command(command))

    def test_linear_shell_parser_detects_commands_without_text_false_positives(self) -> None:
        self.assertEqual(
            "python3.13",
            CHECKER.direct_python_or_pip_command(
                "/opt/toolchains/python3.13 -c 'print(\"direct\")'"
            ),
        )
        self.assertEqual(
            "pip3",
            CHECKER.bare_pip_command("env TOOLCHAIN=checked pip3 --version"),
        )
        self.assertEqual("quick-check", CHECKER.python_make_target("make quick-check"))
        self.assertEqual(
            "python3",
            CHECKER.direct_python_or_pip_command(
                "status=$(python3 -c 'print(\"substitution\")')"
            ),
        )
        self.assertIsNone(CHECKER.shell_syntax_error("count=$((count + 1))"))
        self.assertIsNone(CHECKER.shell_syntax_error("IFS=$'\\t'"))
        self.assertIsNone(CHECKER.shell_syntax_error("paths=$'one\\ntwo'"))
        for launcher in (
            "exec python3 --version",
            "timeout 1 python3 --version",
            "nice python3 --version",
            "setsid python3 --version",
            "xargs python3",
            "nohup python3 --version",
            "stdbuf -oL python3 --version",
            "ionice -c 3 python3 --version",
            "taskset 0x1 python3 --version",
            "flock /tmp/python.lock python3 --version",
            "chrt -o 0 python3 --version",
            "find . -exec python3 --version \\;",
            "unknown-launcher --run python3 --version",
        ):
            with self.subTest(launcher=launcher):
                self.assertEqual(
                    "python3", CHECKER.python_interpreter_token(launcher)
                )

        self.assertIsNone(CHECKER.python_interpreter_token("echo python3"))
        self.assertIsNone(
            CHECKER.python_interpreter_token("printf '%s' python3")
        )
        for indirect in (
            "eval 'python3 --version'",
            'eval "$PYTHON --version"',
            'nohup "$PYTHON" --version',
            "nohup p${X}ython3 --version",
            "nohup ${P}ython3 --version",
            'bash -c "$PYTHON --version"',
        ):
            with self.subTest(indirect=indirect):
                self.assertIsNotNone(CHECKER.shell_syntax_error(indirect))

        harmless = CHECKER.analyze_shell_source(
            """# python3 and pip are comments, not commands.
echo \"python3 -m pip --version\"
cat <<'TEXT'
python3 -m pip --version
TEXT
printf '%s\\n' 'make quick-check'
"""
        )
        self.assertEqual((), harmless.errors)
        command_names = [
            CHECKER.static_command_basename(command.command)
            for command in harmless.commands
        ]
        self.assertEqual(["echo", "cat", "printf"], command_names)

    def test_unsupported_or_malformed_shell_syntax_fails_closed(self) -> None:
        self.assertEqual(
            "dynamic shell command head is unsupported",
            CHECKER.shell_syntax_error('"$PYTHON" --version'),
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
            "python313-before-setup.yml",
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
                    "actions/setup-python must use exactly one "
                    "actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0",
                )

    def test_setup_python_reference_tracks_the_checked_in_action_lock(self) -> None:
        """A future generic setup-python pin update cannot stale this checker."""

        with self.temporary_root() as directory:
            root = Path(directory)
            updated_sha = "a" * 40
            updated_version = "v8.1.2"
            lock = root / "ci" / "tooling" / "security-tools.lock.yml"
            lock.write_text(
                lock.read_text(encoding="utf-8")
                .replace("version: v7.0.0", f"version: {updated_version}", 1)
                .replace(
                    "commit_sha: 5fda3b95a4ea91299a34e894583c3862153e4b97",
                    f"commit_sha: {updated_sha}",
                    1,
                ),
                encoding="utf-8",
            )
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            (workflows / "locked.yml").write_text(
                "name: locked\non: workflow_dispatch\njobs:\n"
                + self.normal_job_block("fixture-job").replace(
                    "actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0",
                    f"actions/setup-python@{updated_sha} # {updated_version}",
                ),
                encoding="utf-8",
            )
            (root / ".python-version").write_text("3.13.14\n", encoding="utf-8")
            _, violations, _ = CHECKER.evaluate_workflow_contract(
                root,
                root / ".python-version",
                expected_normal_jobs={CHECKER.JobIdentity("locked.yml", "fixture-job")},
                expected_candidate_job=None,
                require_setup_lock=True,
            )
            self.assertEqual([], violations)

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

    def test_python_and_dynamic_shell_selectors_are_inventoried(self) -> None:
        cases = {
            "step-python": "    steps:\n      - shell: python\n        run: import sys; print(sys.executable)\n",
            "step-python-template": "    steps:\n      - shell: python3 {0}\n        run: import sys; print(sys.executable)\n",
            "step-dynamic": "    steps:\n      - shell: ${{ matrix.shell }}\n        run: echo safe-looking\n",
            "shell-template": "    steps:\n      - shell: bash -c \"python3 {0}\"\n        run: echo safe-looking\n",
            "pwsh-start-process": "    steps:\n      - shell: pwsh\n        run: Start-Process python3 -ArgumentList --version\n",
            "cmd-start": "    steps:\n      - shell: cmd\n        run: start /wait python3 --version\n",
            "absolute-python-shell": "    steps:\n      - shell: /tmp/evil-bin/python3 {0}\n        run: print('unsafe')\n",
            "dynamic-shell": "    steps:\n      - shell: ${{ env.EVIL_SHELL }}\n        run: echo safe-looking\n",
            "job-default": "    defaults:\n      run:\n        shell: python\n    steps:\n      - run: import sys; print(sys.executable)\n",
        }
        for name, body in cases.items():
            with self.subTest(name=name), self.temporary_root() as directory:
                root = Path(directory)
                workflows = root / ".github" / "workflows"
                workflows.mkdir(parents=True)
                (workflows / "shell.yml").write_text(
                    "name: shell\non: workflow_dispatch\njobs:\n"
                    "  fixture-job:\n    runs-on: ubuntu-latest\n" + body,
                    encoding="utf-8",
                )
                (root / ".python-version").write_text("3.13.14\n", encoding="utf-8")
                _, violations, detected = CHECKER.evaluate_workflow_contract(
                    root,
                    root / ".python-version",
                    expected_normal_jobs={CHECKER.JobIdentity("shell.yml", "fixture-job")},
                    expected_candidate_job=None,
                )
                self.assertEqual({CHECKER.JobIdentity("shell.yml", "fixture-job")}, detected)
                self.assertTrue(any("uses Python" in violation for violation in violations), violations)

        for shell in ("python", "pwsh", "cmd", "${{ env.EVIL_SHELL }}"):
            with self.subTest(default_shell=shell), self.temporary_root() as directory:
                root = Path(directory)
                workflows = root / ".github" / "workflows"
                workflows.mkdir(parents=True)
                (workflows / "workflow-default.yml").write_text(
                    "name: shell\non: workflow_dispatch\ndefaults:\n  run:\n"
                    f"    shell: {shell}\n"
                    "jobs:\n  fixture-job:\n    runs-on: ubuntu-latest\n    steps:\n"
                    "      - run: import sys; print(sys.executable)\n",
                    encoding="utf-8",
                )
                (root / ".python-version").write_text("3.13.14\n", encoding="utf-8")
                _, violations, detected = CHECKER.evaluate_workflow_contract(
                    root,
                    root / ".python-version",
                    expected_normal_jobs={CHECKER.JobIdentity("workflow-default.yml", "fixture-job")},
                    expected_candidate_job=None,
                )
                self.assertEqual(
                    {CHECKER.JobIdentity("workflow-default.yml", "fixture-job")}, detected
                )
                self.assertTrue(any("uses Python" in violation for violation in violations), violations)

    def test_interpreter_selection_mutations_and_alternate_executables_fail_closed(self) -> None:
        """Post-verifier commands must stay bound to setup-python's PATH."""

        cases = {
            "inline-path": "PATH=/usr/bin python3 --version",
            "append-path": "PATH+=:/tmp/evil-bin python3 --version",
            "export-path": "export PATH=/tmp/evil-bin",
            "env-path": "env PATH=/usr/bin python3 --version",
            "env-clear": "env -i python3 --version",
            "env-unset": "env -u PATH python3 --version",
            "command-default-path": "command -p python3 --version",
            "system-python": "/usr/bin/python3 --version",
            "alternate-python": "./tool/python3 --version",
            "versioned-python": "python3.12 --version",
            "local-venv-python": ".venv/bin/python --version",
            "dynamic-launcher": 'BIN=/tmp/evil-bin/python3; nohup "$BIN" --version',
            "github-env-format": "printf '%s=/tmp/evil-bin\\n' PATH >> \"$GITHUB_ENV\"",
            "github-env-heredoc": "cat >> \"$GITHUB_ENV\" <<'EOF'\\nPATH=/tmp/evil-bin\\nEOF",
            "github-env-split-key": 'printf "%s%s=/tmp/evil-bin\\n" P ATH >> "$GITHUB_ENV"',
            "github-path-indirect": 'target=GITHUB_PATH; printf \'/tmp\\n\' >> "${!target}"',
            "github-path-discovered-target": (
                'suffix=PATH; target="$(set | grep "^GITHUB_$suffix=" | cut -d= -f2-)"; '
                'printf "/tmp/evil-bin\\n" >> "$target"'
            ),
            "github-path-discovered-tee-target": (
                'suffix=PATH; target="$(set | grep "^GITHUB_$suffix=" | cut -d= -f2-)"; '
                'printf "/tmp/evil-bin\\n" | tee "$target"'
            ),
        }
        for name, command in cases.items():
            with self.subTest(name=name), self.temporary_root() as directory:
                root = Path(directory)
                workflows = root / ".github" / "workflows"
                workflows.mkdir(parents=True)
                (workflows / "unsafe.yml").write_text(
                    "name: unsafe\non: workflow_dispatch\njobs:\n"
                    + self.normal_job_block("fixture-job")
                    + "      - name: Attempt interpreter selection bypass\n"
                    + "        run: |\n"
                    + "          "
                    + command.replace("\n", "\n          ")
                    + "\n",
                    encoding="utf-8",
                )
                (root / ".python-version").write_text("3.13.14\n", encoding="utf-8")
                _, violations, _ = CHECKER.evaluate_workflow_contract(
                    root,
                    root / ".python-version",
                    expected_normal_jobs={CHECKER.JobIdentity("unsafe.yml", "fixture-job")},
                    expected_candidate_job=None,
                )
                self.assertTrue(violations, violations)

    def test_interpreter_selection_environment_scopes_and_setup_cardinality_fail_closed(self) -> None:
        cases = {
            "workflow-env": (
                "env:\n  PATH: /usr/bin\n",
                "",
                "",
            ),
            "job-env": (
                "",
                "    env:\n      PATH: /usr/bin\n",
                "",
            ),
            "step-env": (
                "",
                "",
                "      - name: Unsafe step environment\n"
                "        env:\n          BASH_ENV: /tmp/evil-startup\n"
                "        run: python3 --version\n",
            ),
            "extra-setup": (
                "",
                "",
                "      - name: Alternate setup action\n"
                "        uses: actions/setup-python@d2d7a03c2b6af94c45503862fba8b2bd9d2089a9 # v6.3.0\n"
                "        with:\n          python-version: '3.12'\n",
            ),
        }
        for name, (workflow_prefix, job_prefix, extra_steps) in cases.items():
            with self.subTest(name=name), self.temporary_root() as directory:
                root = Path(directory)
                workflows = root / ".github" / "workflows"
                workflows.mkdir(parents=True)
                job = self.normal_job_block("fixture-job")
                if job_prefix:
                    job = job.replace(
                        "    runs-on: ubuntu-latest\n",
                        "    runs-on: ubuntu-latest\n" + job_prefix,
                        1,
                    )
                (workflows / "unsafe.yml").write_text(
                    "name: unsafe\non: workflow_dispatch\n"
                    + workflow_prefix
                    + "jobs:\n"
                    + job
                    + extra_steps,
                    encoding="utf-8",
                )
                (root / ".python-version").write_text("3.13.14\n", encoding="utf-8")
                _, violations, _ = CHECKER.evaluate_workflow_contract(
                    root,
                    root / ".python-version",
                    expected_normal_jobs={CHECKER.JobIdentity("unsafe.yml", "fixture-job")},
                    expected_candidate_job=None,
                )
                self.assertTrue(violations, violations)

    def test_audited_pythonpath_exports_remain_valid(self) -> None:
        with self.temporary_root() as directory:
            root = Path(directory)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            (workflows / "safe.yml").write_text(
                "name: safe\non: workflow_dispatch\njobs:\n"
                + self.normal_job_block("fixture-job")
                + "      - name: Install isolated parser dependency\n"
                "        run: |\n"
                "          PYTHONPATH=\"$dependency_dir\" python3 -c 'import sys'\n"
                "          printf 'PYTHONPATH=%s\\n' \"$dependency_dir\" >> \"$GITHUB_ENV\"\n",
                encoding="utf-8",
            )
            (root / ".python-version").write_text("3.13.14\n", encoding="utf-8")
            _, violations, _ = CHECKER.evaluate_workflow_contract(
                root,
                root / ".python-version",
                expected_normal_jobs={CHECKER.JobIdentity("safe.yml", "fixture-job")},
                expected_candidate_job=None,
            )
            self.assertEqual([], violations, violations)

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
            exit_code, payload = self.cli_json_result(root)
        self.assertEqual(2, exit_code)
        self.assertEqual("error", payload["status"])
        self.assertIn("exact Python 3.13.N", payload["violations"][0])

    def test_json_cli_reports_contract_violations_with_exit_one(self) -> None:
        with self.temporary_root() as directory:
            root = Path(directory)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            shutil.copy2(FIXTURES / "missing-setup.yml", workflows / "missing-setup.yml")
            (root / ".python-version").write_text("3.13.14\n", encoding="utf-8")
            exit_code, payload = self.cli_json_result(root)
        self.assertEqual(1, exit_code)
        self.assertEqual("violations", payload["status"])
        self.assertTrue(payload["violations"])

    def test_public_cli_rejects_user_controlled_root_and_nonliteral_version_file(self) -> None:
        stderr = io.StringIO()
        argument_parser = CHECKER.parser()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit) as context:
            argument_parser.parse_args(["--root", "/not-a-repository"])
        self.assertEqual(2, context.exception.code)

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
        self.assertEqual(2, exit_code)
        payload = json.loads(output.getvalue())
        self.assertEqual("error", payload["status"])
        self.assertIn("must be exactly", payload["violations"][0])

    def test_public_cli_requires_a_regular_nonsymlink_canonical_version_file(self) -> None:
        with self.temporary_root() as directory:
            root = Path(directory)
            target = root / "version-source"
            target.write_text("3.13.14\n", encoding="utf-8")
            (root / ".python-version").symlink_to(target)
            exit_code, payload = self.cli_json_result(root)
        self.assertEqual(2, exit_code)
        self.assertIn("must not be a symlink", payload["violations"][0])

        with self.temporary_root() as directory:
            root = Path(directory)
            (root / ".python-version").mkdir()
            exit_code, payload = self.cli_json_result(root)
        self.assertEqual(2, exit_code)
        self.assertIn("must be a regular file", payload["violations"][0])

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
            exit_code, payload = self.cli_json_result(root)
        self.assertEqual(0, exit_code)
        self.assertEqual("valid", payload["status"])
        self.assertEqual(30, len(payload["detected_python_jobs"]))


if __name__ == "__main__":
    unittest.main()
