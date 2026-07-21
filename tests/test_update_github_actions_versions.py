from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "update-github-actions-versions.py"


def load_module():
    spec = importlib.util.spec_from_file_location("update_github_actions_versions", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


updater = load_module()


class FakeOfficialApi:
    """Deterministic official metadata model; no test network is permitted."""

    def __init__(self, lock, *, checkout_target: str | None = None) -> None:
        self.tag_values: dict[str, list[str]] = {}
        self.commits: dict[tuple[str, str], str] = {}
        for name, action in lock.actions.items():
            values = [action.version]
            if name == "actions/checkout" and checkout_target is not None:
                values.append(checkout_target)
                self.commits[(name, checkout_target)] = "a" * 40
            self.tag_values[name] = values
            self.commits[(name, action.version)] = action.commit_sha
        self.releases: dict[str, dict[str, object]] = {}
        for name, tool in lock.tools.items():
            policy = updater.TOOL_POLICIES[name]
            self.tag_values[policy.slug] = [tool.version]
            self.commits[(policy.slug, tool.version)] = tool.release_commit
            self.releases[policy.slug] = {
                "draft": False,
                "prerelease": False,
                "tag_name": tool.version,
                "assets": [
                    {
                        "name": tool.asset,
                        "browser_download_url": tool.url,
                        "digest": f"sha256:{tool.sha256}",
                    }
                ],
            }

    def stable_tags(self, slug: str) -> list[str]:
        return list(self.tag_values[slug])

    def tag_commit(self, slug: str, tag: str) -> str:
        return self.commits[(slug, tag)]

    def latest_release(self, slug: str) -> dict[str, object]:
        return self.releases[slug]


class UpdateGitHubActionsVersionsTest(unittest.TestCase):
    def temporary_parent_root(self) -> tuple[tempfile.TemporaryDirectory[str], Path, object]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        lock_path = root / "ci" / "tooling" / "security-tools.lock.yml"
        lock_path.parent.mkdir(parents=True)
        shutil.copy2(ROOT / "ci" / "tooling" / "security-tools.lock.yml", lock_path)
        lock = updater.read_lock(root)
        workflow = root / ".github" / "workflows" / "contract.yml"
        workflow.parent.mkdir(parents=True)
        lines = ["name: contract", "on: workflow_dispatch", "jobs:", "  check:", "    steps:"]
        for name, action in sorted(lock.actions.items()):
            action_path = f"{name}/init" if name == "github/codeql-action" else name
            if name == "google/osv-scanner-action":
                action_path = f"{name}/osv-scanner-action"
            lines.append(f"      - uses: {action_path}@{action.commit_sha} # {action.version}")
        workflow.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return temporary, root, lock

    def test_resolve_validate_and_apply_updates_only_allowlisted_parent_files(self) -> None:
        temporary, root, lock = self.temporary_parent_root()
        with temporary:
            api = FakeOfficialApi(lock, checkout_target="v7.0.2")
            candidate = updater.resolve_candidate(root, api)
            self.assertTrue(candidate.update_available)
            checkout = next(item for item in candidate.actions if item.current.name == "actions/checkout")
            self.assertEqual(checkout.target.version, "v7.0.2")
            self.assertEqual(checkout.target.commit_sha, "a" * 40)
            plan = updater.validate_candidate(root, candidate, api)
            self.assertEqual(
                set(plan),
                {Path("ci/tooling/security-tools.lock.yml"), Path(".github/workflows/contract.yml")},
            )
            changed = updater.apply_plan(root, plan)
            self.assertEqual(
                changed,
                [".github/workflows/contract.yml", "ci/tooling/security-tools.lock.yml"],
            )
            workflow = (root / ".github/workflows/contract.yml").read_text(encoding="utf-8")
            self.assertIn(f"actions/checkout@{'a' * 40} # v7.0.2", workflow)
            self.assertEqual(updater.verify_local_contract(root)["status"], "valid")

    def test_candidate_tampering_is_rejected_by_fresh_official_resolution(self) -> None:
        temporary, root, lock = self.temporary_parent_root()
        with temporary:
            api = FakeOfficialApi(lock, checkout_target="v7.0.2")
            candidate = updater.resolve_candidate(root, api)
            tampered = candidate.to_dict()
            actions = tampered["actions"]
            self.assertIsInstance(actions, list)
            actions[0]["target"]["commit_sha"] = "f" * 40
            with self.assertRaises(updater.CandidateError):
                updater.validate_candidate(root, updater.candidate_from_dict(tampered), api)

    def test_codeql_action_uses_immutable_action_tags_not_bundle_latest_release(self) -> None:
        """``releases/latest`` is a CodeQL bundle, not a workflow action tag."""

        temporary, root, lock = self.temporary_parent_root()
        with temporary:
            api = FakeOfficialApi(lock)
            api.releases["github/codeql-action"] = {
                "tag_name": "codeql-bundle-v2.26.1",
                "draft": False,
                "prerelease": False,
                "assets": [],
            }
            candidate = updater.resolve_candidate(root, api)
            codeql = next(
                item for item in candidate.actions if item.current.name == "github/codeql-action"
            )
            self.assertEqual(lock.actions["github/codeql-action"].version, codeql.target.version)
            self.assertEqual(
                lock.actions["github/codeql-action"].commit_sha,
                codeql.target.commit_sha,
            )

    def test_workflow_with_a_mutable_reference_fails_closed(self) -> None:
        temporary, root, lock = self.temporary_parent_root()
        with temporary:
            workflow = root / ".github/workflows/contract.yml"
            checkout = lock.actions["actions/checkout"]
            workflow.write_text(
                workflow.read_text(encoding="utf-8").replace(
                    f"actions/checkout@{checkout.commit_sha} # {checkout.version}",
                    f"actions/checkout@{checkout.version} # {checkout.version}",
                ),
                encoding="utf-8",
            )
            with self.assertRaises(updater.WorkflowContractError):
                updater.verify_local_contract(root)

    def test_noncanonical_or_quoted_uses_keys_fail_closed(self) -> None:
        def flow_mapping(text: str) -> str:
            lines = text.splitlines()
            for index, line in enumerate(lines):
                if line.startswith("      - uses: "):
                    lines[index] = line.replace("      - uses: ", "      - {uses: ", 1) + "}"
                    return "\n".join(lines) + "\n"
            raise AssertionError("canonical uses line was not found")

        def escaped_flow_mapping(text: str) -> str:
            return flow_mapping(text).replace("{uses:", r'{"\u0075ses":', 1)

        mutations = {
            "space-before-colon": lambda text: text.replace("      - uses:", "      - uses :", 1),
            "quoted-key": lambda text: text.replace("      - uses:", "      - 'uses':", 1),
            "explicit-key": lambda text: text.replace("      - uses: ", "      ? uses\n      : ", 1),
            "flow-mapping": flow_mapping,
            "escaped-double-quoted-key": lambda text: text.replace(
                "      - uses:", r'      - "\x75ses":', 1
            ),
            "unicode-escaped-flow-key": escaped_flow_mapping,
            "escaped-explicit-key": lambda text: text.replace(
                "      - uses: ", '      ? "\\x75ses"\n      : ', 1
            ),
            "tagged-explicit-key": lambda text: text.replace(
                "      - uses: ", "      ? !!str uses\n      : ", 1
            ),
        }
        for name, mutate in mutations.items():
            with self.subTest(mutation=name):
                temporary, root, _lock = self.temporary_parent_root()
                with temporary:
                    workflow = root / ".github/workflows/contract.yml"
                    workflow.write_text(mutate(workflow.read_text(encoding="utf-8")), encoding="utf-8")
                    with self.assertRaises(updater.WorkflowContractError):
                        updater.verify_local_contract(root)

    def test_candidate_schema_rejects_missing_allowlisted_action(self) -> None:
        temporary, root, lock = self.temporary_parent_root()
        with temporary:
            candidate = updater.resolve_candidate(root, FakeOfficialApi(lock))
            malformed = candidate.to_dict()
            actions = malformed["actions"]
            self.assertIsInstance(actions, list)
            malformed["actions"] = actions[:-1]
            with self.assertRaises(updater.CandidateError):
                updater.candidate_from_dict(malformed)

    def test_candidate_json_round_trip_is_machine_readable(self) -> None:
        temporary, root, lock = self.temporary_parent_root()
        with temporary:
            candidate = updater.resolve_candidate(root, FakeOfficialApi(lock))
            restored = updater.candidate_from_dict(json.loads(json.dumps(candidate.to_dict())))
            self.assertFalse(restored.update_available)
            self.assertEqual(restored.actions, candidate.actions)
            self.assertEqual(restored.tools, candidate.tools)


if __name__ == "__main__":
    unittest.main()
