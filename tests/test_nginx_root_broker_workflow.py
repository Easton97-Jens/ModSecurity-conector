"""Static trust-boundary contract for the immutable broker workflow."""

from __future__ import annotations

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "nginx-root-broker.yml"


def step_block(workflow: str, name: str) -> str:
    marker = f"      - name: {name}\n"
    start = workflow.index(marker)
    end = workflow.find("\n      - name:", start + len(marker))
    return workflow[start:] if end == -1 else workflow[start:end]


def binding_failure_errors(workflow: str) -> list[str]:
    """Return static violations that could run work after caller binding fails."""

    errors: list[str] = []
    marker = "      - name: Validate immutable protected caller workflow object\n"
    if marker not in workflow:
        return ["missing caller binding step"]
    before_binding = workflow[: workflow.index(marker)]
    binding_step = step_block(workflow, "Validate immutable protected caller workflow object")
    if "continue-on-error:" in binding_step:
        errors.append("caller binding step can continue after failure")
    if "\n        if:" in binding_step:
        errors.append("caller binding step can be skipped")
    if "set -euo pipefail" not in binding_step:
        errors.append("caller binding step lacks fail-fast shell options")
    if (
        "set +e" in binding_step
        or "set +o errexit" in binding_step
        or "||" in binding_step
    ):
        errors.append("caller binding command can suppress a failure")
    expected_command_start = (
        "          python3 -I ci/runtime/broker/nginx_root_broker.py validate-caller-workflow \\\n"
    )
    if expected_command_start not in binding_step:
        errors.append("caller binding command has an unexpected invocation")
    expected_terminal_command = '            --framework-sha "$EXPECTED_FRAMEWORK_SHA"'
    if not binding_step.rstrip().endswith(expected_terminal_command):
        errors.append("caller binding command is not terminal")
    for name in ("BROKER_MANIFEST", "BROKER_PROJECTION", "BROKER_ARTIFACT_EVIDENCE"):
        if f"{name}=" in before_binding:
            errors.append(f"{name} is recorded before caller binding")
    for name in (
        "Download declarative caller manifest",
        "Build only trusted protected-source artifacts without root",
        "Build a protected immutable OWASP CRS bundle without root",
        "Produce a non-executable trusted candidate manifest",
        "Admit only verified artifacts into the root-owned broker root",
        "Run fixed root-only NGINX actions",
    ):
        if "\n        if:" in step_block(workflow, name):
            errors.append(f"{name} can bypass a failed caller binding")
    guarded_steps = {
        "Stage the fixed root-to-user evidence outside the cleanup root": "env.BROKER_PROJECTION != ''",
        "Stop and verify root cleanup": "env.BROKER_MANIFEST != ''",
        "Upload bounded root-to-user evidence": "env.BROKER_ARTIFACT_EVIDENCE != ''",
    }
    for name, required_guard in guarded_steps.items():
        block = step_block(workflow, name)
        if "if: ${{ always() &&" not in block or required_guard not in block:
            errors.append(f"{name} has no bounded post-admission guard")
    return errors


def python_version_materialization_errors(workflow: str) -> list[str]:
    """Return static violations for the broker-controlled Python version file."""

    required_steps = (
        "Verify protected source, caller commit, and dependency identity",
        "Materialize verified broker Python version contract",
        "Set up protected broker Python",
        "Verify Python interpreter contract",
        "Validate immutable protected caller workflow object",
    )
    if any(f"      - name: {name}\n" not in workflow for name in required_steps):
        return ["missing protected Python-version workflow step"]

    errors: list[str] = []
    source_step = step_block(
        workflow, "Verify protected source, caller commit, and dependency identity"
    )
    materialization_step = step_block(
        workflow, "Materialize verified broker Python version contract"
    )
    expected_materialization_step = "\n".join(
        (
            "      - name: Materialize verified broker Python version contract",
            "        working-directory: broker-src",
            "        run: |",
            "          set -euo pipefail",
            "          source_path=.python-version",
            '          destination="$GITHUB_WORKSPACE/.python-version"',
            '          test ! -L "$source_path"',
            '          test -f "$source_path"',
            '          expected=$(git rev-parse "$BROKER_SHA:$source_path")',
            '          actual=$(git hash-object "$source_path")',
            '          test "$actual" = "$expected"',
            '          test ! -e "$destination"',
            '          test ! -L "$destination"',
            '          install -m 0644 "$source_path" "$destination"',
            '          test ! -L "$destination"',
            '          cmp -- "$source_path" "$destination"',
        )
    )
    if materialization_step.rstrip() != expected_materialization_step:
        errors.append("protected Python-version materialization has an unexpected command surface")
    if "continue-on-error:" in materialization_step:
        errors.append("protected Python-version materialization can continue after failure")
    if "\n        if:" in materialization_step:
        errors.append("protected Python-version materialization can be skipped")
    if "set -euo pipefail" not in materialization_step:
        errors.append("protected Python-version materialization lacks fail-fast shell options")
    if (
        "set +e" in materialization_step
        or "set +o errexit" in materialization_step
        or "||" in materialization_step
    ):
        errors.append("protected Python-version materialization can suppress a failure")
    if "verify_broker_source .python-version" not in source_step:
        errors.append("broker Python version blob is not verified before materialization")
    for required in (
        "source_path=.python-version",
        'destination="$GITHUB_WORKSPACE/.python-version"',
        'expected=$(git rev-parse "$BROKER_SHA:$source_path")',
        'actual=$(git hash-object "$source_path")',
        'test ! -e "$destination"',
        'test ! -L "$destination"',
        'install -m 0644 "$source_path" "$destination"',
        'cmp -- "$source_path" "$destination"',
    ):
        if required not in materialization_step:
            errors.append(f"missing protected Python-version materialization control: {required}")

    source_verification = workflow.index("verify_broker_source .python-version")
    materialization = workflow.index("Materialize verified broker Python version contract")
    setup = workflow.index("Set up protected broker Python")
    verifier = workflow.index("Verify Python interpreter contract")
    caller_binding = workflow.index("Validate immutable protected caller workflow object")
    if not source_verification < materialization < setup < verifier < caller_binding:
        errors.append("protected Python-version materialization has an unsafe order")
    return errors


def runtime_component_snapshot_contract_errors(workflow: str) -> list[str]:
    """Return static violations for the fixed protected build snapshot selector."""

    build_step_name = "Build only trusted protected-source artifacts without root"
    required_selection = (
        "          RUNTIME_COMPONENT_SNAPSHOT_CONTRACT: protected-nginx-broker"
    )
    if f"      - name: {build_step_name}\n" not in workflow:
        return ["missing protected build step"]

    errors: list[str] = []
    build_step = step_block(workflow, build_step_name)
    if workflow.count(required_selection) != 1:
        errors.append("snapshot selector is not unique and fixed")
    if required_selection not in build_step:
        errors.append("snapshot selector is outside the trusted build step")
    if "\n        if:" in build_step:
        errors.append("trusted build step can conditionally select a snapshot contract")
    if "continue-on-error:" in build_step:
        errors.append("trusted build step can continue after snapshot preparation failure")
    if "RUNTIME_COMPONENT_SNAPSHOT_CONTRACT: ${{" in workflow:
        errors.append("snapshot selector accepts a mutable expression")
    if "inputs.runtime_component_snapshot_contract" in workflow:
        errors.append("snapshot selector accepts a caller input")
    if required_selection in workflow:
        selection = workflow.index(required_selection)
        fetch_dependencies = workflow.index("make fetch-deps")
        prepare_from_snapshot = workflow.index("prepare-from-snapshot")
        if not selection < fetch_dependencies < prepare_from_snapshot:
            errors.append("snapshot selector does not precede dependency and candidate preparation")
    return errors


class TrustedNginxRootBrokerWorkflowTest(unittest.TestCase):
    def setUp(self) -> None:
        self.workflow = WORKFLOW.read_text(encoding="utf-8")

    def test_workflow_is_reusable_read_only_and_refuses_pr_trigger_modes(self) -> None:
        self.assertIn("  workflow_call:\n", self.workflow)
        self.assertNotIn("  pull_request:", self.workflow)
        self.assertNotIn("  pull_request_target:", self.workflow)
        self.assertIn("permissions:\n  contents: read", self.workflow)
        self.assertIn("github.event_name == 'workflow_dispatch'", self.workflow)
        self.assertNotIn("github.event_name == 'workflow_dispatch' || github.event_name == 'schedule'", self.workflow)
        self.assertIn("github.repository == 'Easton97-Jens/ModSecurity-conector'", self.workflow)
        self.assertIn("github.event.repository.fork == false", self.workflow)
        self.assertIn("github.ref == 'refs/heads/master'", self.workflow)
        self.assertIn("github.event.repository.default_branch == 'master'", self.workflow)
        self.assertNotIn("secrets.", self.workflow)
        self.assertNotIn("id-token: write", self.workflow)

    def test_broker_source_is_immutable_and_bound_to_the_protected_caller_commit(self) -> None:
        self.assertIn("ACTUAL_CALLER_WORKFLOW_REF: ${{ github.workflow_ref }}", self.workflow)
        self.assertIn(
            "EXPECTED_CALLER_WORKFLOW_REF: Easton97-Jens/ModSecurity-conector/.github/workflows/run-protected-nginx-root-broker.yml@refs/heads/master",
            self.workflow,
        )
        self.assertIn('test "$ACTUAL_CALLER_WORKFLOW_REF" = "$EXPECTED_CALLER_WORKFLOW_REF"', self.workflow)
        self.assertNotIn("EXPECTED_WORKFLOW_REF:", self.workflow)
        self.assertIn("CALLER_SHA: ${{ github.sha }}", self.workflow)
        self.assertIn("CALLER_WORKFLOW_SHA: ${{ github.workflow_sha }}", self.workflow)
        for expected in (
            'test "$CALLER_REPOSITORY" = Easton97-Jens/ModSecurity-conector',
            'test "$CALLER_REF" = refs/heads/master',
            'test "$CALLER_EVENT_NAME" = workflow_dispatch',
            'test "$CALLER_FORK" = false',
            'test "$CALLER_DEFAULT_BRANCH" = master',
            'test "$CALLER_WORKFLOW_SHA" = "$CALLER_SHA"',
            'git cat-file -e "$CALLER_SHA^{commit}"',
            'git merge-base --is-ancestor "$CALLER_SHA" FETCH_HEAD',
            'git merge-base --is-ancestor "$BROKER_SHA" "$CALLER_SHA"',
        ):
            self.assertIn(expected, self.workflow)
        self.assertIn("repository: Easton97-Jens/ModSecurity-conector", self.workflow)
        self.assertIn("ref: ${{ inputs.protected_broker_sha }}", self.workflow)
        self.assertIn("path: broker-src", self.workflow)
        self.assertIn("fetch-depth: 0", self.workflow)
        self.assertIn("submodules: recursive", self.workflow)
        self.assertIn("persist-credentials: false", self.workflow)
        self.assertIn("clean: true", self.workflow)
        self.assertIn('test "$(git rev-parse HEAD)" = "$BROKER_SHA"', self.workflow)
        self.assertIn('git merge-base --is-ancestor "$BROKER_SHA" FETCH_HEAD', self.workflow)
        self.assertIn('git ls-tree "$BROKER_SHA" -- modules/ModSecurity-test-Framework', self.workflow)
        self.assertIn('git rev-parse "$BROKER_SHA:modules/ModSecurity-test-Framework"', self.workflow)
        self.assertIn('test "$framework_gitlink" = "$EXPECTED_FRAMEWORK_SHA"', self.workflow)
        self.assertIn('git submodule status --recursive', self.workflow)
        self.assertIn('tools/MRTS status --porcelain', self.workflow)
        self.assertIn("verify_broker_source .github/workflows/nginx-root-broker.yml", self.workflow)
        self.assertIn('git rev-parse "$BROKER_SHA:$source_path"', self.workflow)
        self.assertIn("git hash-object \"$source_path\"", self.workflow)
        self.assertIn("verify_broker_source ci/runtime/broker/nginx_root_broker.py", self.workflow)
        self.assertIn("verify_broker_source .python-version", self.workflow)
        self.assertIn("Materialize verified broker Python version contract", self.workflow)
        self.assertIn('destination="$GITHUB_WORKSPACE/.python-version"', self.workflow)
        self.assertIn('test ! -e "$destination"', self.workflow)
        self.assertIn('install -m 0644 "$source_path" "$destination"', self.workflow)
        self.assertIn("id: setup-python", self.workflow)
        self.assertIn("python-version-file: .python-version", self.workflow)
        self.assertIn("Verify Python interpreter contract", self.workflow)
        self.assertIn("Validate immutable protected caller workflow object", self.workflow)
        self.assertIn("validate-caller-workflow", self.workflow)
        self.assertIn('"$CALLER_SHA"', self.workflow)
        self.assertIn("/usr/bin/python3 -I ci/runtime/broker/nginx_root_broker.py", self.workflow)
        self.assertNotIn("@master", self.workflow)
        self.assertNotIn("@fix/f-gs-003-pin-nginx-full-smoke", self.workflow)
        self.assertNotIn("uses: ./", self.workflow)

    def test_binding_closes_before_artifacts_build_candidate_or_root(self) -> None:
        binding = self.workflow.index("Validate immutable protected caller workflow object")
        for later in (
            "Download declarative caller manifest",
            "Build only trusted protected-source artifacts without root",
            "make fetch-deps",
            "Produce a non-executable trusted candidate manifest",
            "Admit only verified artifacts into the root-owned broker root",
            "sudo -- /usr/bin/python3 -I ci/runtime/broker/nginx_root_broker.py action",
        ):
            self.assertLess(binding, self.workflow.index(later), later)
        for action in (
            "config-test",
            "start",
            "verify-runtime-profile",
            "verify-master-worker-identity",
            "stop",
            "project-evidence",
        ):
            self.assertIn(
                "\n".join(
                    (
                        "          verify_broker_source",
                        "          sudo -- /usr/bin/python3 -I ci/runtime/broker/nginx_root_broker.py "
                        f"action --action {action}",
                    )
                ),
                self.workflow,
            )
        self.assertIn("verify_broker_source\n          manifest=$(sudo -- /usr/bin/python3 -I", self.workflow)
        self.assertIn("verify_broker_source\n          set +e\n          sudo -- /usr/bin/python3 -I", self.workflow)
        self.assertIn(
            "set -e\n          verify_broker_source\n          set +e\n          sudo -- /usr/bin/python3 -I",
            self.workflow,
        )

    def test_verified_broker_python_version_precedes_setup_and_python_use(self) -> None:
        self.assertEqual(python_version_materialization_errors(self.workflow), [])
        materialization_start = self.workflow.index(
            "      - name: Materialize verified broker Python version contract\n"
        )
        setup_start = self.workflow.index("      - name: Set up protected broker Python\n")
        verifier_start = self.workflow.index("      - name: Verify Python interpreter contract\n")
        materialization_after_setup = (
            self.workflow[:materialization_start]
            + self.workflow[setup_start:verifier_start]
            + self.workflow[materialization_start:setup_start]
            + self.workflow[verifier_start:]
        )
        mutations = {
            "uses workspace source": (
                "source_path=.python-version",
                "source_path=$GITHUB_WORKSPACE/.python-version",
            ),
            "accepts an existing destination": ('test ! -e "$destination"', "true"),
            "materialization error can continue": (
                "      - name: Materialize verified broker Python version contract\n"
                "        working-directory:",
                "      - name: Materialize verified broker Python version contract\n"
                "        continue-on-error: true\n"
                "        working-directory:",
            ),
            "materialization can be skipped": (
                "      - name: Materialize verified broker Python version contract\n"
                "        working-directory:",
                "      - name: Materialize verified broker Python version contract\n"
                "        if: ${{ false }}\n"
                "        working-directory:",
            ),
            "materialization disables errexit": (
                "      - name: Materialize verified broker Python version contract\n"
                "        working-directory: broker-src\n"
                "        run: |\n"
                "          set -euo pipefail\n",
                "      - name: Materialize verified broker Python version contract\n"
                "        working-directory: broker-src\n"
                "        run: |\n"
                "          set -euo pipefail\n"
                "          set +o errexit\n",
            ),
            "materialization suppresses a failed destination check": (
                'test ! -e "$destination"',
                'test ! -e "$destination" || true',
            ),
            "materialization absorbs a failed destination check": (
                'test ! -e "$destination"',
                'if test ! -e "$destination"; then :; else :; fi',
            ),
        }
        for name, (original, replacement) in mutations.items():
            with self.subTest(name=name):
                self.assertIn(original, self.workflow)
                mutated = self.workflow.replace(original, replacement, 1)
                self.assertNotEqual(python_version_materialization_errors(mutated), [])
        self.assertNotEqual(
            python_version_materialization_errors(materialization_after_setup), []
        )

    def test_binding_failure_cannot_create_candidate_or_broker_evidence(self) -> None:
        self.assertEqual(binding_failure_errors(self.workflow), [])
        mutations = {
            "manifest state before binding": (
                '          test "$ACTUAL_CALLER_WORKFLOW_REF" = "$EXPECTED_CALLER_WORKFLOW_REF"',
                '          echo "BROKER_MANIFEST=unsafe" >> "$GITHUB_ENV"\n'
                '          test "$ACTUAL_CALLER_WORKFLOW_REF" = "$EXPECTED_CALLER_WORKFLOW_REF"',
            ),
            "binding error can continue": (
                "      - name: Validate immutable protected caller workflow object\n"
                "        working-directory:",
                "      - name: Validate immutable protected caller workflow object\n"
                "        continue-on-error: true\n"
                "        working-directory:",
            ),
            "binding can be skipped": (
                "      - name: Validate immutable protected caller workflow object\n"
                "        working-directory:",
                "      - name: Validate immutable protected caller workflow object\n"
                "        if: ${{ false }}\n"
                "        working-directory:",
            ),
            "binding command suppresses an error": (
                '            --framework-sha "$EXPECTED_FRAMEWORK_SHA"',
                '            --framework-sha "$EXPECTED_FRAMEWORK_SHA" || true',
            ),
            "binding command disables errexit": (
                "      - name: Validate immutable protected caller workflow object\n"
                "        working-directory: broker-src\n"
                "        run: |\n"
                "          set -euo pipefail\n",
                "      - name: Validate immutable protected caller workflow object\n"
                "        working-directory: broker-src\n"
                "        run: |\n"
                "          set -euo pipefail\n"
                "          set +o errexit\n",
            ),
            "binding command negates an error": (
                "          python3 -I ci/runtime/broker/nginx_root_broker.py validate-caller-workflow \\\n",
                "          ! python3 -I ci/runtime/broker/nginx_root_broker.py validate-caller-workflow \\\n",
            ),
            "binding command is not terminal": (
                '            --framework-sha "$EXPECTED_FRAMEWORK_SHA"',
                '            --framework-sha "$EXPECTED_FRAMEWORK_SHA"\n          true',
            ),
            "artifact download always runs": (
                "      - name: Download declarative caller manifest\n        uses:",
                "      - name: Download declarative caller manifest\n"
                "        if: ${{ always() }}\n        uses:",
            ),
            "candidate build always runs": (
                "      - name: Build only trusted protected-source artifacts without root\n"
                "        working-directory:",
                "      - name: Build only trusted protected-source artifacts without root\n"
                "        if: ${{ always() }}\n        working-directory:",
            ),
            "candidate root admission always runs": (
                "      - name: Admit only verified artifacts into the root-owned broker root\n"
                "        working-directory:",
                "      - name: Admit only verified artifacts into the root-owned broker root\n"
                "        if: ${{ always() }}\n        working-directory:",
            ),
            "stage guard weakened": (
                "env.BROKER_PROJECTION != ''",
                "true",
            ),
            "cleanup guard weakened": (
                "env.BROKER_MANIFEST != ''",
                "true",
            ),
            "upload guard weakened": (
                "env.BROKER_ARTIFACT_EVIDENCE != ''",
                "true",
            ),
        }
        for name, (original, replacement) in mutations.items():
            with self.subTest(name=name):
                self.assertIn(original, self.workflow)
                mutated = self.workflow.replace(original, replacement, 1)
                self.assertNotEqual(binding_failure_errors(mutated), [])

    def test_root_invocation_is_fixed_after_unprivileged_protected_build(self) -> None:
        self.assertLess(
            self.workflow.index("Build only trusted protected-source artifacts without root"),
            self.workflow.index("Build a protected immutable OWASP CRS bundle without root"),
        )
        self.assertLess(
            self.workflow.index("Build a protected immutable OWASP CRS bundle without root"),
            self.workflow.index("Admit only verified artifacts into the root-owned broker root"),
        )
        self.assertIn("make fetch-deps", self.workflow)
        self.assertIn("prepare-fresh-crs-source.sh", self.workflow)
        self.assertIn("ci/provisioning/fetch-crs.sh", self.workflow)
        self.assertIn("prepare-crs-bundle", self.workflow)
        self.assertIn("prepare-from-snapshot", self.workflow)
        self.assertIn("sudo -- /usr/bin/python3 -I ci/runtime/broker/nginx_root_broker.py action", self.workflow)
        for action in (
            "validate-manifest",
            "config-test",
            "start",
            "verify-runtime-profile",
            "verify-master-worker-identity",
            "project-evidence",
            "stop",
            "cleanup-status",
        ):
            self.assertIn(action, self.workflow)
        for forbidden in ("sudo -E", "sudo sh -c", "sudo bash -c", "systemctl", "service "):
            self.assertNotIn(forbidden, self.workflow)
        for forbidden in ("--broker-parent", "--staging-root", "--runtime-snapshot"):
            self.assertNotIn(forbidden, self.workflow)

    def test_runtime_component_snapshot_contract_is_fixed_before_build_and_candidate_use(self) -> None:
        self.assertEqual(runtime_component_snapshot_contract_errors(self.workflow), [])
        required_selection = (
            "          RUNTIME_COMPONENT_SNAPSHOT_CONTRACT: protected-nginx-broker"
        )
        build_step_header = (
            "      - name: Build only trusted protected-source artifacts without root\n"
            "        working-directory:"
        )
        mutations = {
            "selector omitted": (required_selection, ""),
            "selector accepts caller expression": (
                required_selection,
                "          RUNTIME_COMPONENT_SNAPSHOT_CONTRACT: ${{ inputs.runtime_component_snapshot_contract }}",
            ),
            "selector duplicated outside the trusted build": (
                required_selection,
                "\n".join((required_selection, required_selection)),
            ),
            "trusted build conditionally selects the contract": (
                build_step_header,
                "      - name: Build only trusted protected-source artifacts without root\n"
                "        if: ${{ github.ref == 'refs/heads/master' }}\n"
                "        working-directory:",
            ),
        }
        for name, (original, replacement) in mutations.items():
            with self.subTest(name=name):
                self.assertIn(original, self.workflow)
                mutated = self.workflow.replace(original, replacement, 1)
                self.assertNotEqual(runtime_component_snapshot_contract_errors(mutated), [])

    def test_bounded_evidence_is_staged_before_descriptor_cleanup_and_records_its_outcome(self) -> None:
        self.assertLess(
            self.workflow.index("Run fixed root-only NGINX actions"),
            self.workflow.index("Stage the fixed root-to-user evidence outside the cleanup root"),
        )
        self.assertLess(
            self.workflow.index("Stage the fixed root-to-user evidence outside the cleanup root"),
            self.workflow.index("Stop and verify root cleanup"),
        )
        self.assertLess(
            self.workflow.index("Stop and verify root cleanup"),
            self.workflow.index("Upload bounded root-to-user evidence"),
        )
        for filename in (
            "identity.json",
            "runtime.json",
            "policy.json",
            "nginx-access.log",
            "nginx-error.log",
            "nginx-audit.log",
            "cleanup.json",
        ):
            self.assertIn(filename, self.workflow)
        self.assertIn('"cleanup_status":"%s"', self.workflow)
        self.assertNotIn("cp -r", self.workflow)
        self.assertNotIn("tar ", self.workflow)

    def test_caller_data_is_limited_to_a_declarative_artifact_and_pinned_inputs(self) -> None:
        for field in (
            "caller_manifest_artifact",
            "parent_head_sha",
            "framework_sha",
            "protected_broker_sha",
            "matrix_variant",
            "run_id",
        ):
            self.assertIn(f"      {field}:\n", self.workflow)
        self.assertIn("Download declarative caller manifest", self.workflow)
        self.assertIn("caller-manifest.json", self.workflow)
        self.assertIn("--expected-parent-head \"$EXPECTED_PARENT_HEAD\"", self.workflow)
        self.assertIn("--expected-framework-sha \"$EXPECTED_FRAMEWORK_SHA\"", self.workflow)
        self.assertIn("--expected-run-id \"$BROKER_RUN_ID\"", self.workflow)
        self.assertIn("--expected-matrix-variant \"$BROKER_VARIANT\"", self.workflow)
        self.assertNotIn("github.event.pull_request.head.sha", self.workflow)
        self.assertNotIn("GITHUB_TOKEN", self.workflow)

    def test_actions_are_full_sha_pinned(self) -> None:
        for action in re.findall(r"uses:\s+([^\s]+)", self.workflow):
            self.assertRegex(action, r"^[\w.-]+/[\w.-]+@[0-9a-f]{40}$")


if __name__ == "__main__":
    unittest.main()
