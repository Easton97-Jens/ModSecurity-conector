"""Focused contracts for shared private-runtime artifact helpers."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import stat
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
CI_LIB = ROOT / "ci" / "lib"
if str(CI_LIB) not in sys.path:
    sys.path.insert(0, str(CI_LIB))

import runtime_path_utils as RUNTIME_PATH_UTILS
from runtime_path_utils import (
    append_runtime_artifact_text,
    read_runtime_artifact_text,
    runtime_artifact_path,
    verified_runtime_artifact_root,
    write_runtime_artifact_text_atomic,
)


def load_helper(name: str, path: Path) -> object:
    specification = importlib.util.spec_from_file_location(name, path)
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


class RuntimeArtifactUtilsTest(unittest.TestCase):
    def private_root(self, temporary: str) -> Path:
        return verified_runtime_artifact_root(Path(temporary) / "runtime")

    def test_root_validation_rejects_relative_and_broad_locations(self) -> None:
        with self.assertRaisesRegex(ValueError, "must be absolute"):
            verified_runtime_artifact_root("relative-runtime")
        with self.assertRaisesRegex(ValueError, "unsafe for writes"):
            verified_runtime_artifact_root("/")

    def test_path_validation_rejects_non_descendants_and_symbolic_links(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-artifact-path-") as temporary:
            root = self.private_root(temporary)
            target = root / "artifacts" / "result.txt"
            self.assertEqual(
                runtime_artifact_path(root, target, "result"),
                target,
            )
            with self.assertRaisesRegex(ValueError, "must be absolute"):
                runtime_artifact_path(root, Path("relative.txt"), "result")
            with self.assertRaisesRegex(ValueError, "below the runtime root"):
                runtime_artifact_path(root, root, "result")
            with self.assertRaisesRegex(ValueError, "below the runtime root"):
                runtime_artifact_path(root, root.parent / "outside.txt", "result")

            final_link = root / "final-link.txt"
            final_link.symlink_to(root.parent / "outside.txt")
            with self.assertRaisesRegex(ValueError, "below the runtime root|symbolic link"):
                runtime_artifact_path(root, final_link, "result")

            escaped_parent = root / "escaped"
            escaped_parent.symlink_to(root.parent, target_is_directory=True)
            escaped_result = escaped_parent / "result.txt"
            with self.assertRaisesRegex(ValueError, "below the runtime root"):
                runtime_artifact_path(root, escaped_result, "result")

    def test_shared_text_operations_keep_regular_private_artifacts(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-artifact-text-") as temporary:
            root = self.private_root(temporary)
            target = root / "records" / "event.txt"
            self.assertEqual(
                append_runtime_artifact_text(root, target, "first\n", "event"),
                target,
            )
            append_runtime_artifact_text(root, target, "second\n", "event")
            self.assertEqual(
                read_runtime_artifact_text(root, target, "event"),
                "first\nsecond\n",
            )
            self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o600)

            write_runtime_artifact_text_atomic(root, target, "replacement\n", "event")
            self.assertEqual(
                read_runtime_artifact_text(root, target, "event"),
                "replacement\n",
            )
            self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o600)
            self.assertEqual(list(target.parent.glob(".event.txt.*.tmp")), [])

            directory = root / "directory-target"
            directory.mkdir()
            with self.assertRaisesRegex(ValueError, "regular file"):
                append_runtime_artifact_text(root, directory, "nope", "directory")
            with self.assertRaisesRegex(ValueError, "regular file"):
                write_runtime_artifact_text_atomic(root, directory, "nope", "directory")
            with self.assertRaisesRegex(ValueError, "existing regular file"):
                read_runtime_artifact_text(root, directory, "directory")

    def test_atomic_recheck_rejects_a_replaced_nonregular_destination(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-artifact-recheck-") as temporary:
            root = self.private_root(temporary)
            target = root / "observation.json"
            target.write_text("old\n", encoding="utf-8")
            original_stat = RUNTIME_PATH_UTILS.os.stat
            replacement = list(target.stat())
            replacement[0] = stat.S_IFDIR | 0o700
            target_stat_calls = 0

            def rechecked_stat(path: object, *args: object, **kwargs: object) -> os.stat_result:
                nonlocal target_stat_calls
                if (
                    path == target.name
                    and kwargs.get("dir_fd") is not None
                    and kwargs.get("follow_symlinks") is False
                ):
                    target_stat_calls += 1
                    if target_stat_calls == 2:
                        return os.stat_result(replacement)
                return original_stat(path, *args, **kwargs)

            with mock.patch.object(RUNTIME_PATH_UTILS.os, "stat", side_effect=rechecked_stat):
                with self.assertRaisesRegex(ValueError, "regular file"):
                    write_runtime_artifact_text_atomic(root, target, "new\n", "observation")

            self.assertEqual(target.read_text(encoding="utf-8"), "old\n")
            self.assertEqual(list(root.glob(".observation.json.*.tmp")), [])

    def test_atomic_name_collision_keeps_the_existing_temporary_file(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-artifact-collision-") as temporary:
            root = self.private_root(temporary)
            target = root / "observation.json"
            collision = root / ".observation.json.already-there.tmp"
            collision.write_text("retain me\n", encoding="utf-8")
            with mock.patch.object(
                RUNTIME_PATH_UTILS.secrets,
                "token_hex",
                side_effect=["already-there", "fresh-name"],
            ):
                write_runtime_artifact_text_atomic(root, target, "new\n", "observation")

            self.assertEqual(collision.read_text(encoding="utf-8"), "retain me\n")
            self.assertEqual(target.read_text(encoding="utf-8"), "new\n")
            self.assertEqual(list(root.glob(".observation.json.*.tmp")), [collision])

    def test_missing_nofollow_or_directory_support_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-artifact-flags-") as temporary:
            root = self.private_root(temporary)
            target = root / "record.txt"
            with mock.patch.object(RUNTIME_PATH_UTILS.os, "O_NOFOLLOW", None):
                with self.assertRaises(ValueError):
                    append_runtime_artifact_text(root, target, "data", "record")
            with mock.patch.object(RUNTIME_PATH_UTILS.os, "O_DIRECTORY", None):
                with self.assertRaises(ValueError):
                    append_runtime_artifact_text(root, target, "data", "record")
            self.assertFalse(target.exists())

    def test_connector_facades_preserve_serialization_and_private_modes(self) -> None:
        haproxy = load_helper(
            "haproxy_runtime_artifacts_contract",
            ROOT / "connectors/haproxy/harness/runtime_artifacts.py",
        )
        envoy = load_helper(
            "envoy_smoke_helper_artifact_contract",
            ROOT / "connectors/envoy/harness/envoy_smoke_helper.py",
        )
        with tempfile.TemporaryDirectory(prefix="runtime-artifact-facades-") as temporary:
            root = self.private_root(temporary)
            haproxy_path = root / "haproxy-events.jsonl"
            envoy_path = root / "envoy-observation.json"
            haproxy.append_text(root, haproxy_path, "event\n", "HAProxy event")
            self.assertEqual(haproxy.read_text(root, haproxy_path, "HAProxy event"), "event\n")
            self.assertEqual(stat.S_IMODE(haproxy_path.stat().st_mode), 0o600)

            envoy.write_json_atomic(root, envoy_path, {"answer": 42}, "Envoy observation")
            self.assertEqual(
                envoy_path.read_text(encoding="utf-8"),
                "{\n  \"answer\": 42\n}\n",
            )
            envoy.append_jsonl(root, root / "envoy-events.jsonl", {"event": "ok"}, "Envoy event")
            self.assertEqual(stat.S_IMODE(envoy_path.stat().st_mode), 0o600)


if __name__ == "__main__":
    unittest.main()
