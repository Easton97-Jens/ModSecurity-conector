"""Focused Parent contracts for the constrained workflow-tool updater."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
UPDATER_PATH = ROOT / "ci" / "tools" / "update-workflow-tools.py"


def load_updater():
    spec = importlib.util.spec_from_file_location("parent_workflow_tool_updater", UPDATER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {UPDATER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


UPDATER = load_updater()


class WorkflowToolUpdaterTests(unittest.TestCase):
    def lock(self) -> tuple[Path, dict[str, object], str]:
        return UPDATER.load_lock(ROOT)

    def action_candidate(
        self, lock_digest: str, version: str, commit: str
    ) -> dict[str, object]:
        _path, lock, _digest = self.lock()
        baseline = lock["actions"]["actions/checkout"]
        return {
            "schema_version": UPDATER.CANDIDATE_SCHEMA_VERSION,
            "lock_sha256": lock_digest,
            "actions": {
                "actions/checkout": {
                    "version": version,
                    "immutable_commit": commit,
                    "upstream_release": (
                        f"{baseline['upstream_repository']}/releases/tag/{version}"
                    ),
                }
            },
            "tools": {},
        }

    def copied_update_root(self, destination: Path) -> Path:
        destination.mkdir(parents=True)
        for relative_text in UPDATER.ALLOWED_UPDATE_PATHS:
            source = ROOT / relative_text
            target = destination / relative_text
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        return destination

    def test_parent_lock_normalizes_actions_tools_and_workflow_coverage(self) -> None:
        _path, lock, _digest = self.lock()
        self.assertIn("actions/create-github-app-token", lock["actions"])
        self.assertIn("actionlint", lock["tools"])
        self.assertEqual(
            lock["actions"]["actions/create-github-app-token"]["immutable_commit"],
            "bcd2ba49218906704ab6c1aa796996da409d3eb1",
        )
        self.assertEqual(
            lock["tools"]["actionlint"]["asset_url"],
            "https://github.com/rhysd/actionlint/releases/download/"
            "v1.7.12/actionlint_1.7.12_linux_amd64.tar.gz",
        )
        UPDATER.ensure_locked_action_workflow_coverage(ROOT, lock)
        UPDATER.validate_parent_workflow_contract(ROOT, lock)

    def test_parent_lock_schema_fails_closed_for_malformed_provenance(self) -> None:
        raw = UPDATER.yaml.safe_load(
            (ROOT / "ci/tooling/security-tools.lock.yml").read_text(encoding="utf-8")
        )
        cases = {
            "unexpected-top-level": lambda data: data.__setitem__("unexpected", True),
            "missing-action-field": lambda data: data["pinned_actions"]
            ["actions/checkout"].pop("version"),
            "action-commit-uppercase": lambda data: data["pinned_actions"]
            ["actions/checkout"].__setitem__("commit_sha", "A" * 40),
            "mismatched-action-upstream": lambda data: data["pinned_actions"]
            ["actions/checkout"].__setitem__("upstream", "https://github.com/other/repository"),
            "tool-asset-traversal": lambda data: data["tools"]["actionlint"].__setitem__(
                "asset", "../escape.tar.gz"
            ),
            "tool-url-mismatch": lambda data: data["tools"]["actionlint"].__setitem__(
                "url", "https://example.invalid/tool.tar.gz"
            ),
            "tool-digest-uppercase": lambda data: data["tools"]["actionlint"].__setitem__(
                "sha256", "A" * 64
            ),
            "tool-executable-traversal": lambda data: data["tools"]["actionlint"].__setitem__(
                "executable", "../actionlint"
            ),
        }
        for name, mutate in cases.items():
            with self.subTest(name=name):
                malformed = deepcopy(raw)
                mutate(malformed)
                with self.assertRaises(UPDATER.UpdateError):
                    UPDATER.normalise_parent_lock(malformed)

    def test_candidate_rejects_noop_downgrade_and_wrong_lock_digest(self) -> None:
        _path, lock, digest = self.lock()
        empty = {
            "schema_version": UPDATER.CANDIDATE_SCHEMA_VERSION,
            "lock_sha256": digest,
            "actions": {},
            "tools": {},
        }
        changes = UPDATER.validate_candidate_shape(empty, lock, digest)
        UPDATER.require_candidate_updates(changes, False)
        with self.assertRaisesRegex(UPDATER.UpdateError, "must contain"):
            UPDATER.require_candidate_updates(changes, True)

        for version, expected in (("v7.0.1", "no-op"), ("v7.0.0", "downgrade")):
            with self.subTest(version=version):
                candidate = self.action_candidate(digest, version, "a" * 40)
                with self.assertRaises(UPDATER.UpdateError):
                    UPDATER.validate_candidate_shape(candidate, lock, digest)

        candidate = self.action_candidate("0" * 64, "v7.0.2", "a" * 40)
        with self.assertRaisesRegex(UPDATER.UpdateError, "current trusted lock"):
            UPDATER.validate_candidate_shape(candidate, lock, digest)
        with self.assertRaisesRegex(UPDATER.UpdateError, "allow-listed"):
            UPDATER.lock_record(lock, "actions", "unreviewed/action")
        with self.assertRaisesRegex(UPDATER.UpdateError, "base64"):
            UPDATER.decode_candidate("not-base64")
        for release in (
            {"draft": True, "prerelease": False, "tag_name": "v9.9.9"},
            {"draft": False, "prerelease": True, "tag_name": "v9.9.9"},
        ):
            with self.assertRaises(UPDATER.UpdateError):
                UPDATER.stable_release_tag(release, "fixture")

    def test_apply_candidate_preserves_parent_lock_schema_and_allowlist(self) -> None:
        _path, lock, digest = self.lock()
        candidate = self.action_candidate(digest, "v7.0.2", "a" * 40)
        with tempfile.TemporaryDirectory() as temporary_directory:
            proposed = self.copied_update_root(Path(temporary_directory) / "tree")
            changed = UPDATER.apply_candidate(proposed, candidate)
            self.assertIn("ci/tooling/security-tools.lock.yml", changed)
            self.assertTrue(
                any(path.startswith(".github/workflows/") for path in changed)
            )
            self.assertTrue(set(changed).issubset(UPDATER.ALLOWED_UPDATE_PATHS))
            raw_lock = (proposed / "ci/tooling/security-tools.lock.yml").read_text(
                encoding="utf-8"
            )
            self.assertIn("commit_sha: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", raw_lock)
            self.assertNotIn("immutable_commit:", raw_lock)
            _path, resulting_lock, _digest = UPDATER.load_lock(proposed)
            UPDATER.validate_parent_workflow_contract(proposed, resulting_lock)

    def test_candidate_files_are_confined_to_private_runner_temp(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            runner_temp = temporary_root / "runner-temp"
            outside = temporary_root / "outside"
            runner_temp.mkdir(mode=0o700)
            outside.mkdir()
            candidate_path = runner_temp / "nested" / "candidate.json"
            candidate = {"schema_version": 1}
            with patch.dict(os.environ, {"RUNNER_TEMP": str(runner_temp)}):
                UPDATER.write_candidate(candidate_path, candidate)
                self.assertEqual(candidate, UPDATER.read_candidate(candidate_path))
                self.assertEqual(candidate_path.stat().st_mode & 0o777, 0o600)
                with self.assertRaisesRegex(UPDATER.UpdateError, "overwrite"):
                    UPDATER.write_candidate(candidate_path, candidate)
                with self.assertRaisesRegex(UPDATER.UpdateError, "strict child"):
                    UPDATER.runner_temp_path(
                        runner_temp / ".." / "outside" / "candidate.json",
                        for_write=True,
                    )
                redirected = runner_temp / "redirected"
                redirected.symlink_to(outside, target_is_directory=True)
                with self.assertRaisesRegex(UPDATER.UpdateError, "symlink"):
                    UPDATER.write_candidate(redirected / "candidate.json", candidate)

    def test_candidate_tool_validation_uses_parent_checksum_fetcher_interface(self) -> None:
        _path, lock, _digest = self.lock()
        calls: list[tuple[str, dict[str, str], Path]] = []

        class FakeFetcher:
            @staticmethod
            def fetch_record(
                name: str, record: dict[str, str], destination: Path
            ) -> Path:
                calls.append((name, record, destination))
                return destination / record["executable"]

        changed_tool = deepcopy(lock["tools"]["actionlint"])
        with tempfile.TemporaryDirectory() as temporary_directory:
            runner_temp = Path(temporary_directory) / "runner-temp"
            runner_temp.mkdir(mode=0o700)
            with (
                patch.dict(os.environ, {"RUNNER_TEMP": str(runner_temp)}),
                patch.object(UPDATER, "load_fetcher_module", return_value=FakeFetcher),
            ):
                UPDATER.verify_changed_tool_assets(
                    {"actions": {}, "tools": {"actionlint": changed_tool}},
                    runner_temp / "tool-validation",
                )
        self.assertEqual(len(calls), 1)
        name, record, destination = calls[0]
        self.assertEqual(name, "actionlint")
        self.assertEqual(record["url"], changed_tool["asset_url"])
        self.assertEqual(destination.name, "actionlint")

    def test_proposed_tree_validation_never_modifies_source_checkout(self) -> None:
        _path, _lock, digest = self.lock()
        candidate = self.action_candidate(digest, "v7.0.2", "a" * 40)
        source_lock = (ROOT / "ci/tooling/security-tools.lock.yml").read_bytes()
        with tempfile.TemporaryDirectory() as temporary_directory:
            runner_temp = Path(temporary_directory) / "runner-temp"
            runner_temp.mkdir(mode=0o700)
            with patch.dict(os.environ, {"RUNNER_TEMP": str(runner_temp)}):
                UPDATER.validate_proposed_tree(ROOT, candidate)
            self.assertEqual(list(runner_temp.iterdir()), [])
        self.assertEqual(
            source_lock,
            (ROOT / "ci/tooling/security-tools.lock.yml").read_bytes(),
        )

    def test_scope_verification_rejects_unallowlisted_paths(self) -> None:
        result = subprocess.CompletedProcess(
            ["git"],
            0,
            b"M\0README.md\0",
            b"",
        )
        with patch.object(UPDATER.subprocess, "run", return_value=result):
            with self.assertRaisesRegex(UPDATER.UpdateError, "README.md"):
                UPDATER.verify_git_scope(ROOT, staged=True)

    def test_existing_draft_branch_must_match_the_default_base_candidate(self) -> None:
        lock_path, base_lock, _digest = self.lock()
        base_blob = lock_path.read_bytes()
        base_digest = hashlib.sha256(base_blob).hexdigest()
        candidate = self.action_candidate(base_digest, "v7.0.2", "a" * 40)
        matching_head = deepcopy(base_lock)
        matching_head["actions"]["actions/checkout"].update(
            {
                "version": "v7.0.2",
                "immutable_commit": "a" * 40,
                "upstream_release": "https://github.com/actions/checkout/releases/tag/v7.0.2",
            }
        )

        def verify(head_lock: dict[str, object]) -> None:
            with (
                patch.object(UPDATER, "verify_git_scope"),
                patch.object(
                    UPDATER,
                    "git_lock_blob_data",
                    side_effect=[(base_blob, base_lock), (b"head", head_lock)],
                ),
                patch.object(UPDATER, "verify_existing_branch_lock_records"),
                patch.object(UPDATER, "verify_existing_branch_generated_blobs"),
            ):
                UPDATER.verify_existing_branch(
                    ROOT,
                    "origin/master",
                    "origin/automation/update-modsecurity-connector-workflow-tools",
                    candidate,
                    UPDATER.candidate_sha256(candidate),
                )

        verify(matching_head)
        mismatched_head = deepcopy(matching_head)
        mismatched_head["actions"]["actions/checkout"].update(
            {
                "version": "v7.0.3",
                "immutable_commit": "b" * 40,
                "upstream_release": "https://github.com/actions/checkout/releases/tag/v7.0.3",
            }
        )
        with (
            patch.object(UPDATER, "verify_git_scope"),
            patch.object(
                UPDATER,
                "git_lock_blob_data",
                side_effect=[(base_blob, base_lock), (b"head", mismatched_head)],
            ),
            patch.object(UPDATER, "verify_existing_branch_lock_records"),
            patch.object(UPDATER, "verify_existing_branch_generated_blobs"),
        ):
            with self.assertRaisesRegex(UPDATER.UpdateError, "does not match"):
                UPDATER.verify_existing_branch(
                    ROOT,
                    "origin/master",
                    "origin/automation/update-modsecurity-connector-workflow-tools",
                    candidate,
                    UPDATER.candidate_sha256(candidate),
                )


if __name__ == "__main__":
    unittest.main()
