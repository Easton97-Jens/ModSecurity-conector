"""Security-regression tests for Parent workflow updater boundaries."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
UPDATER_PATH = ROOT / "ci" / "tools" / "update-workflow-tools.py"
FETCHER_PATH = ROOT / "ci" / "tools" / "fetch_security_tool.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


UPDATER = load_module("parent_workflow_security_updater", UPDATER_PATH)
FETCHER = load_module("parent_workflow_security_fetcher", FETCHER_PATH)


class WorkflowSecurityRegressionTests(unittest.TestCase):
    def test_every_current_parent_workflow_uses_a_locked_immutable_action(self) -> None:
        _path, lock, _digest = UPDATER.load_lock(ROOT)
        UPDATER.ensure_locked_action_workflow_coverage(ROOT, lock)
        UPDATER.validate_parent_workflow_contract(ROOT, lock)

    def test_yaml_composition_features_fail_closed_before_semantic_checks(self) -> None:
        fixtures = {
            "anchor": "name: &unsafe workflow\n",
            "alias": "name: workflow\nvalue: *unsafe\n",
            "tag": "name: !unsafe workflow\n",
            "merge": "base: &base {name: workflow}\n<<: *base\n",
        }
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            for name, content in fixtures.items():
                with self.subTest(name=name):
                    path = temporary_root / f"{name}.yml"
                    path.write_text(content, encoding="utf-8")
                    with self.assertRaises(UPDATER.UpdateError):
                        UPDATER.checked_workflow_mapping(path, path.name)

    def test_root_and_regular_path_resolution_reject_symlinks_and_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            actual = temporary_root / "actual"
            actual.mkdir()
            alias = temporary_root / "alias"
            alias.symlink_to(actual, target_is_directory=True)
            with self.assertRaisesRegex(UPDATER.UpdateError, "non-symlink"):
                UPDATER.resolve_root(alias)
            with self.assertRaisesRegex(UPDATER.UpdateError, "traversal"):
                UPDATER.resolve_root(actual / "..")
            with self.assertRaisesRegex(UPDATER.UpdateError, "unsafe relative"):
                UPDATER.resolve_regular_file(actual, Path("../escape"))

    def test_fetcher_rejects_path_escapes_and_symlink_destinations(self) -> None:
        _path, lock, _digest = UPDATER.load_lock(ROOT)
        record = lock["tools"]["actionlint"]
        values = {
            "version": record["version"],
            "asset": record["asset"],
            "url": record["asset_url"],
            "sha256": record["sha256"],
            "executable": record["executable"],
            "upstream": record["upstream_repository"],
        }
        for key, value in (("asset", "../tool.tar.gz"), ("executable", "dir\\tool")):
            with self.subTest(key=key):
                malformed = dict(values)
                malformed[key] = value
                with self.assertRaises(ValueError):
                    FETCHER.validate_record("actionlint", malformed)

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            destination = root / "destination"
            destination.symlink_to(root, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "symlink"):
                FETCHER.fetch_record("actionlint", values, destination)
            parent_alias = root / "parent-alias"
            parent_alias.symlink_to(root, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "symlink"):
                FETCHER.fetch_record("actionlint", values, parent_alias / "tool")
            with self.assertRaisesRegex(ValueError, "traversal"):
                FETCHER.safe_destination(root / "child" / ".." / "outside")
            regular_destination = root / "regular-destination"
            regular_destination.mkdir()
            target_alias = regular_destination / "actionlint"
            target_alias.symlink_to(root / "outside")
            with self.assertRaisesRegex(ValueError, "symlink"):
                FETCHER.safe_executable_target(regular_destination, "actionlint")

        traversal = tarfile.TarInfo("../actionlint")
        symlink = tarfile.TarInfo("actionlint")
        symlink.type = tarfile.SYMTYPE
        regular = tarfile.TarInfo("actionlint")
        regular.type = tarfile.REGTYPE
        self.assertFalse(FETCHER.safe_member(traversal))
        self.assertFalse(FETCHER.safe_member(symlink))
        self.assertTrue(FETCHER.safe_member(regular))

    def test_fetcher_cli_requires_an_owned_runner_temp_child(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            runner_temp = root / "runner-temp"
            runner_temp.mkdir()
            destination = runner_temp / "security-tools"
            calls: list[tuple[str, Path]] = []

            def fake_fetch(tool: str, path: Path) -> Path:
                calls.append((tool, path))
                return path / tool

            with patch.dict(os.environ, {"RUNNER_TEMP": str(runner_temp)}):
                with patch.object(FETCHER, "fetch", side_effect=fake_fetch):
                    with patch.object(
                        sys,
                        "argv",
                        [
                            "fetch_security_tool.py",
                            "--tool",
                            "actionlint",
                            "--destination",
                            str(destination),
                        ],
                    ):
                        FETCHER.main()
                    self.assertEqual(calls, [("actionlint", destination)])
                    for unsafe in ("relative", str(root / "outside")):
                        with self.subTest(destination=unsafe):
                            with patch.object(
                                sys,
                                "argv",
                                [
                                    "fetch_security_tool.py",
                                    "--tool",
                                    "actionlint",
                                    "--destination",
                                    unsafe,
                                ],
                            ):
                                with self.assertRaises(SystemExit) as error:
                                    FETCHER.main()
                            self.assertEqual(error.exception.code, 2)
                    runner_alias = root / "runner-alias"
                    runner_alias.symlink_to(runner_temp, target_is_directory=True)
                    with patch.dict(os.environ, {"RUNNER_TEMP": str(runner_alias)}):
                        with patch.object(
                            sys,
                            "argv",
                            [
                                "fetch_security_tool.py",
                                "--tool",
                                "actionlint",
                                "--destination",
                                str(runner_alias / "security-tools"),
                            ],
                        ):
                            with self.assertRaises(SystemExit) as error:
                                FETCHER.main()
                        self.assertEqual(error.exception.code, 2)
                    self.assertEqual(calls, [("actionlint", destination)])

    def test_read_only_jobs_reject_bracket_secret_and_github_token_references(self) -> None:
        _path, lock, _digest = UPDATER.load_lock(ROOT)
        text = (ROOT / ".github/workflows/update-workflow-tools.yml").read_text(
            encoding="utf-8"
        )
        for expression in (
            "${{ secrets['UPDATER_TOKEN'] }}",
            "${{ github['token'] }}",
        ):
            with self.subTest(expression=expression), tempfile.TemporaryDirectory() as temporary_directory:
                root = Path(temporary_directory)
                workflow_dir = root / ".github/workflows"
                workflow_dir.mkdir(parents=True)
                target = workflow_dir / "update-workflow-tools.yml"
                target.write_text(
                    text.replace("  resolver:\n", f"  resolver:\n    env:\n      TOKEN: {expression}\n", 1),
                    encoding="utf-8",
                )
                lock_target = root / "ci/tooling/security-tools.lock.yml"
                lock_target.parent.mkdir(parents=True)
                lock_target.write_bytes(
                    (ROOT / "ci/tooling/security-tools.lock.yml").read_bytes()
                )
                with self.assertRaisesRegex(UPDATER.UpdateError, "must not receive secrets"):
                    UPDATER.validate_parent_workflow_contract(root, lock)

    def test_candidate_sha_binding_rejects_tampering(self) -> None:
        candidate = {"schema_version": 1, "lock_sha256": "a" * 64, "actions": {}, "tools": {}}
        expected = UPDATER.candidate_sha256(candidate)
        UPDATER.require_candidate_sha256(candidate, expected)
        candidate["tools"] = {"actionlint": {}}
        with self.assertRaisesRegex(UPDATER.UpdateError, "does not match"):
            UPDATER.require_candidate_sha256(candidate, expected)

    def test_runner_temp_must_be_owned_nonsymlink_and_absolute(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            runner_temp = root / "runner-temp"
            runner_temp.mkdir()
            with patch.dict(os.environ, {"RUNNER_TEMP": str(runner_temp)}):
                self.assertEqual(UPDATER.runner_temp_root(), runner_temp.resolve())
            alias = root / "alias"
            alias.symlink_to(runner_temp, target_is_directory=True)
            with patch.dict(os.environ, {"RUNNER_TEMP": str(alias)}):
                with self.assertRaisesRegex(UPDATER.UpdateError, "non-symlink"):
                    UPDATER.runner_temp_root()
            with patch.dict(os.environ, {"RUNNER_TEMP": "relative"}):
                with self.assertRaisesRegex(UPDATER.UpdateError, "absolute"):
                    UPDATER.runner_temp_root()


if __name__ == "__main__":
    unittest.main()
