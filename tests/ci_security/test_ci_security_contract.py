"""Parent CI-security workflow contracts for the updater maintenance path."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import shutil
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
UPDATER_PATH = ROOT / "ci" / "tools" / "update-workflow-tools.py"
TARGET = Path(".github/workflows/update-workflow-tools.yml")


def load_updater():
    spec = importlib.util.spec_from_file_location("parent_ci_security_contract_updater", UPDATER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {UPDATER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


UPDATER = load_updater()


class ParentCiSecurityContractTests(unittest.TestCase):
    def copy_update_surface(self, temporary_root: Path) -> Path:
        destination = temporary_root / "tree"
        destination.mkdir()
        for relative_text in UPDATER.ALLOWED_UPDATE_PATHS:
            source = ROOT / relative_text
            target = destination / relative_text
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        return destination

    def assert_target_rejected(self, mutate) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = self.copy_update_surface(Path(temporary_directory))
            target = root / TARGET
            target.write_text(mutate(target.read_text(encoding="utf-8")), encoding="utf-8")
            _path, lock, _digest = UPDATER.load_lock(root)
            with self.assertRaises(UPDATER.UpdateError):
                UPDATER.validate_parent_workflow_contract(root, lock)

    def test_current_parent_workflows_match_the_lock_and_target_contract(self) -> None:
        _path, lock, _digest = UPDATER.load_lock(ROOT)
        UPDATER.ensure_locked_action_workflow_coverage(ROOT, lock)
        UPDATER.validate_parent_workflow_contract(ROOT, lock)

    def test_target_keeps_required_trigger_topology_and_least_privilege_shape(self) -> None:
        text = (ROOT / TARGET).read_text(encoding="utf-8")
        self.assertIn("workflow_dispatch:", text)
        self.assertIn('cron: "17 5 * * 1"', text)
        self.assertIn("cancel-in-progress: false", text)
        self.assertLess(text.index("  resolver:"), text.index("  validator:"))
        self.assertLess(text.index("  validator:"), text.index("  publisher:"))
        self.assertLess(text.index("  publisher:"), text.index("  outcome:"))
        self.assertIn("needs: resolver", text)
        self.assertIn("needs:\n      - resolver\n      - validator", text)
        self.assertIn("permissions: {}", text)
        self.assertIn("persist-credentials: false", text)
        self.assertNotIn("pull_request_target", text)
        self.assertNotIn("--force", text)
        self.assertNotIn("auto-merge", text)

    def test_target_rejects_quoted_trigger_anchors_and_mutable_or_quoted_uses(self) -> None:
        cases = {
            "quoted-pull-request-target": lambda text: text.replace(
                "on:\n", "on:\n  'pull_request_target':\n", 1
            ),
            "yaml-anchor": lambda text: text.replace(
                "name: Update pinned workflow tools",
                "name: &unsafe Update pinned workflow tools",
                1,
            ),
            "mutable-action": lambda text: text.replace(
                "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
                "actions/checkout@v7",
                1,
            ),
            "branch-action": lambda text: text.replace(
                "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
                "actions/checkout@main",
                1,
            ),
            "short-action-sha": lambda text: text.replace(
                "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
                "actions/checkout@3d3c42e",
                1,
            ),
            "uppercase-action-sha": lambda text: text.replace(
                "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
                "actions/checkout@3D3C42E5AAC5BA805825DA76410C181273BA90B1",
                1,
            ),
            "unlocked-action": lambda text: text.replace(
                "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
                "unreviewed/action@aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                1,
            ),
            "dynamic-action": lambda text: text.replace(
                "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
                "actions/checkout@${{ github.sha }}",
                1,
            ),
            "quoted-uses-key": lambda text: text.replace(
                "uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
                '"uses": actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1',
                1,
            ),
        }
        for name, mutate in cases.items():
            with self.subTest(name=name):
                self.assert_target_rejected(mutate)

    def test_target_rejects_reader_secrets_bad_needs_writer_permissions_and_force(self) -> None:
        def publisher_permissions(text: str) -> str:
            before, publisher = text.split("  publisher:\n", 1)
            return before + "  publisher:\n" + publisher.replace(
                "    permissions:\n      contents: read",
                "    permissions:\n      contents: write",
                1,
            )

        cases = {
            "resolver-secret": lambda text: text.replace(
                "  resolver:\n", "  resolver:\n    env:\n      TOKEN: ${{ secrets.UPDATER_TOKEN }}\n", 1
            ),
            "validator-needs": lambda text: text.replace(
                "  validator:\n    needs: resolver",
                "  validator:\n    needs: publisher",
                1,
            ),
            "publisher-permissions": publisher_permissions,
            "missing-candidate-binding": lambda text: text.replace(
                "--expected-candidate-sha256", "--different-candidate-sha256"
            ),
            "forced-push": lambda text: text.replace(
                'git push origin "HEAD:refs/heads/$UPDATE_BRANCH"',
                'git push --force origin "HEAD:refs/heads/$UPDATE_BRANCH"',
                1,
            ),
        }
        for name, mutate in cases.items():
            with self.subTest(name=name):
                self.assert_target_rejected(mutate)

    def test_publisher_uses_the_pinned_repository_limited_app_token(self) -> None:
        text = (ROOT / TARGET).read_text(encoding="utf-8")
        self.assertIn(
            "actions/create-github-app-token@bcd2ba49218906704ab6c1aa796996da409d3eb1 # v3.2.0",
            text,
        )
        self.assertIn("owner: ${{ github.repository_owner }}", text)
        self.assertIn("repositories: ${{ github.repository }}", text)
        self.assertIn("permission-contents: write", text)
        self.assertIn("permission-pull-requests: write", text)
        self.assertIn("permission-workflows: write", text)
        self.assertIn("github-token: ${{ steps.publisher_app_token.outputs.token }}", text)
        self.assertNotIn("github-token: ${{ github.token }}", text)
        self.assertIn("WORKFLOW_UPDATER_APP_CLIENT_ID repository variable is missing", text)
        self.assertIn("WORKFLOW_UPDATER_APP_PRIVATE_KEY repository secret is missing", text)

    def test_existing_draft_path_binds_the_same_resolver_candidate_before_switching(self) -> None:
        text = (ROOT / TARGET).read_text(encoding="utf-8")
        self.assertIn("verify-existing-branch --root .", text)
        self.assertIn("--candidate-b64 \"$CANDIDATE_B64\"", text)
        self.assertIn("--expected-candidate-sha256 \"$CANDIDATE_SHA256\"", text)
        self.assertIn("Do not bind that candidate to its newer", text)
        self.assertIn("MAINTENANCE_PR_EXISTS", text)
        self.assertIn("expected exactly one matching maintenance branch", text)
        self.assertIn("matching Draft updater PR", text)


if __name__ == "__main__":
    unittest.main()
