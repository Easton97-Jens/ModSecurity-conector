from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import pwd
import stat
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
HELPER_PATH = ROOT / "ci/tools/prepare-readonly-submodule-validation-sandbox.py"
SPEC = importlib.util.spec_from_file_location("prepare_readonly_sandbox", HELPER_PATH)
assert SPEC is not None
assert SPEC.loader is not None
HELPER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = HELPER
SPEC.loader.exec_module(HELPER)


class PrepareReadonlySubmoduleValidationSandboxTests(unittest.TestCase):
    @staticmethod
    def identity_is_mapped_in_current_namespace(identity: HELPER.ValidatorIdentity) -> bool:
        def mapped(identifier: int, map_name: str) -> bool:
            try:
                rows = Path(f"/proc/self/{map_name}").read_text(encoding="utf-8").splitlines()
            except OSError:
                return False
            for row in rows:
                inside, _outside, count = (int(value) for value in row.split())
                if inside <= identifier < inside + count:
                    return True
            return False

        return mapped(identity.uid, "uid_map") and mapped(identity.gid, "gid_map")

    def make_layout(self, temporary: Path) -> tuple[Path, Path, Path, Path]:
        source = temporary / "source"
        framework = source / "modules" / "framework"
        runner_temp = temporary / "runner-temp"
        write = runner_temp / "readonly-validation"
        framework.mkdir(parents=True)
        framework_git = framework / ".git"
        framework_git.write_text("gitdir: ../../.git/modules/framework\n", encoding="utf-8")
        (source / ".git" / "modules" / "framework").mkdir(parents=True)
        runner_temp.mkdir()
        write.mkdir(mode=0o711)
        if os.geteuid() == 0:
            os.chown(write, 0, 0)
        os.chmod(write, 0o711)
        return source, framework, runner_temp, write

    def test_valid_control_locks_sources_and_creates_only_external_root(self) -> None:
        if os.geteuid() != 0:
            self.skipTest("locking control requires root")
        with tempfile.TemporaryDirectory(prefix="readonly-sandbox-") as raw:
            source, framework, runner_temp, write = self.make_layout(Path(raw))
            source_file = source / "input.txt"
            source_file.write_text("trusted", encoding="utf-8")
            git_module_file = source / ".git" / "modules" / "framework" / "config"
            git_module_file.parent.mkdir(parents=True, exist_ok=True)
            git_module_file.write_text("[core]", encoding="utf-8")
            arguments = HELPER.parse_args(
                [
                    "--source-root", str(source), "--framework-root", str(framework),
                    "--write-root", str(write), "--runner-temp", str(runner_temp),
                    "--validator-user", "unused", "--validator-group", "unused",
                ]
            )
            identity = HELPER.ValidatorIdentity("validator", "validator", os.getuid(), os.getgid())
            with mock.patch.object(HELPER, "resolve_validator_identity", return_value=identity):
                external, inventory_sha256 = HELPER.prepare_sandbox(arguments)
            self.assertEqual(external, write / "external")
            self.assertEqual(len(inventory_sha256), 64)
            self.assertEqual(stat.S_IMODE(write.stat().st_mode), 0o711)
            self.assertEqual(stat.S_IMODE(external.stat().st_mode), 0o700)
            self.assertEqual(external.stat().st_uid, identity.uid)
            inventory = write / HELPER.INVENTORY_FILENAME
            self.assertEqual(stat.S_IMODE(inventory.stat().st_mode), 0o600)
            self.assertEqual(source.stat().st_uid, 0)
            self.assertEqual(source_file.stat().st_uid, 0)
            self.assertEqual(source_file.stat().st_mode & 0o022, 0)
            self.assertEqual(git_module_file.stat().st_uid, 0)
            self.assertEqual(git_module_file.stat().st_mode & 0o022, 0)
            with mock.patch.object(HELPER, "resolve_validator_identity", return_value=identity):
                verified_external, verified_sha256 = HELPER.verify_sandbox(arguments)
            self.assertEqual(verified_external, external)
            self.assertEqual(verified_sha256, inventory_sha256)

    def test_real_validator_can_write_only_external_root(self) -> None:
        if os.geteuid() != 0:
            self.skipTest("privilege-drop control requires root")
        try:
            account = pwd.getpwnam("nobody")
            group = HELPER.grp.getgrgid(account.pw_gid)
        except KeyError:
            self.skipTest("the system has no nobody identity")
        identity = HELPER.resolve_validator_identity(account.pw_name, group.gr_name)
        if not self.identity_is_mapped_in_current_namespace(identity):
            self.skipTest("the nobody identity is unavailable in this user namespace")
        with tempfile.TemporaryDirectory(
            dir="/tmp", prefix="readonly-sandbox-"
        ) as raw:
            temporary = Path(raw)
            # The child needs traversal through the disposable fixture parent,
            # but no permission to list or change the guarded write root.
            os.chmod(temporary, 0o711)
            source, framework, runner_temp, write = self.make_layout(temporary)
            os.chmod(runner_temp, 0o755)
            (source / "input.txt").write_text("trusted", encoding="utf-8")
            arguments = HELPER.parse_args(
                [
                    "--source-root", str(source), "--framework-root", str(framework),
                    "--write-root", str(write), "--runner-temp", str(runner_temp),
                    "--validator-user", identity.user, "--validator-group", identity.group,
                ]
            )
            external, _inventory_sha256 = HELPER.prepare_sandbox(arguments)

            def child_exit(script: str, target: Path) -> int:
                def drop_privileges() -> None:
                    os.setgroups([])
                    os.setgid(identity.gid)
                    os.setuid(identity.uid)

                return subprocess.run(
                    ["/bin/sh", "-ceu", script, "readonly-sandbox-probe", str(target)],
                    check=False,
                    preexec_fn=drop_privileges,
                ).returncode

            cannot_write = 'if touch -- "$1" 2>/dev/null; then exit 1; fi'
            cannot_list = 'if ls -A -- "$1" >/dev/null 2>&1; then exit 1; fi'
            cannot_remove = 'if rm -- "$1" 2>/dev/null; then exit 1; fi'
            cannot_chmod = 'if chmod 600 -- "$1" 2>/dev/null; then exit 1; fi'
            can_write = 'printf allowed > "$1"'

            self.assertEqual(child_exit(cannot_write, source / "candidate-write"), 0)
            self.assertEqual(child_exit(cannot_remove, source / "input.txt"), 0)
            self.assertEqual(child_exit(cannot_chmod, source / "input.txt"), 0)
            self.assertEqual(child_exit(cannot_write, source / ".git" / "index.lock"), 0)
            self.assertEqual(child_exit(cannot_write, write / "candidate-write"), 0)
            self.assertEqual(child_exit(cannot_list, write), 0)
            external_file = external / "candidate-write"
            self.assertEqual(child_exit(can_write, external_file), 0)
            self.assertEqual(external_file.read_text(encoding="utf-8"), "allowed")
            self.assertEqual(HELPER.verify_sandbox(arguments)[0], external)

    def test_rejects_external_source_symlink_without_touching_its_target(self) -> None:
        if os.geteuid() != 0:
            self.skipTest("no-follow source-link control requires root")
        with tempfile.TemporaryDirectory(prefix="readonly-sandbox-") as raw:
            temporary = Path(raw)
            source, framework, runner_temp, write = self.make_layout(temporary)
            outside = temporary / "outside.txt"
            outside.write_text("outside", encoding="utf-8")
            original = outside.stat()
            (source / "outside-link").symlink_to(outside)
            arguments = HELPER.parse_args(
                [
                    "--source-root", str(source), "--framework-root", str(framework),
                    "--write-root", str(write), "--runner-temp", str(runner_temp),
                    "--validator-user", "unused", "--validator-group", "unused",
                ]
            )
            identity = HELPER.ValidatorIdentity("validator", "validator", os.getuid(), os.getgid())
            with mock.patch.object(HELPER, "resolve_validator_identity", return_value=identity):
                with self.assertRaisesRegex(ValueError, "symbolic link must remain inside source"):
                    HELPER.prepare_sandbox(arguments)
            current = outside.stat()
            self.assertEqual(outside.read_text(encoding="utf-8"), "outside")
            self.assertEqual((current.st_uid, current.st_gid, stat.S_IMODE(current.st_mode)), (
                original.st_uid, original.st_gid, stat.S_IMODE(original.st_mode),
            ))
            self.assertFalse((write / HELPER.EXTERNAL_DIRNAME).exists())

    def test_detects_source_inventory_mutation_after_preparation(self) -> None:
        if os.geteuid() != 0:
            self.skipTest("source-inventory mutation control requires root")
        with tempfile.TemporaryDirectory(prefix="readonly-sandbox-") as raw:
            source, framework, runner_temp, write = self.make_layout(Path(raw))
            source_file = source / "input.txt"
            source_file.write_text("before", encoding="utf-8")
            arguments = HELPER.parse_args(
                [
                    "--source-root", str(source), "--framework-root", str(framework),
                    "--write-root", str(write), "--runner-temp", str(runner_temp),
                    "--validator-user", "unused", "--validator-group", "unused",
                ]
            )
            identity = HELPER.ValidatorIdentity("validator", "validator", os.getuid(), os.getgid())
            with mock.patch.object(HELPER, "resolve_validator_identity", return_value=identity):
                HELPER.prepare_sandbox(arguments)
                source_file.write_text("after", encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "source inventory changed"):
                    HELPER.verify_sandbox(arguments)

    def test_records_an_allowed_internal_source_symlink_without_following_it(self) -> None:
        if os.geteuid() != 0:
            self.skipTest("internal source-link inventory control requires root")
        with tempfile.TemporaryDirectory(prefix="readonly-sandbox-") as raw:
            source, framework, runner_temp, write = self.make_layout(Path(raw))
            source_file = source / "input.txt"
            source_file.write_text("inside", encoding="utf-8")
            source_link = source / "inside-link"
            source_link.symlink_to("input.txt")
            arguments = HELPER.parse_args(
                [
                    "--source-root", str(source), "--framework-root", str(framework),
                    "--write-root", str(write), "--runner-temp", str(runner_temp),
                    "--validator-user", "unused", "--validator-group", "unused",
                ]
            )
            identity = HELPER.ValidatorIdentity("validator", "validator", os.getuid(), os.getgid())
            with mock.patch.object(HELPER, "resolve_validator_identity", return_value=identity):
                external, _inventory_sha256 = HELPER.prepare_sandbox(arguments)
                inventory, _inventory_digest = HELPER._read_inventory(
                    write / HELPER.INVENTORY_FILENAME
                )
                self.assertIn(
                    {"path": "inside-link", "type": "symlink", "target": "input.txt"},
                    [
                        {
                            key: entry[key]
                            for key in ("path", "type", "target")
                            if key in entry
                        }
                        for entry in inventory
                    ],
                )
                self.assertTrue(source_link.is_symlink())
                self.assertEqual(source_file.read_text(encoding="utf-8"), "inside")
                self.assertEqual(HELPER.verify_sandbox(arguments)[0], external)

    def test_rejects_unsafe_external_output_objects(self) -> None:
        if os.geteuid() != 0:
            self.skipTest("external-output controls require root")
        with tempfile.TemporaryDirectory(prefix="readonly-sandbox-") as raw:
            source, framework, runner_temp, write = self.make_layout(Path(raw))
            source_file = source / "input.txt"
            source_file.write_text("source", encoding="utf-8")
            arguments = HELPER.parse_args(
                [
                    "--source-root", str(source), "--framework-root", str(framework),
                    "--write-root", str(write), "--runner-temp", str(runner_temp),
                    "--validator-user", "unused", "--validator-group", "unused",
                ]
            )
            identity = HELPER.ValidatorIdentity("validator", "validator", os.getuid(), os.getgid())
            with mock.patch.object(HELPER, "resolve_validator_identity", return_value=identity):
                external, _inventory_sha256 = HELPER.prepare_sandbox(arguments)
                (external / "outside-link").symlink_to(source_file)
                with self.assertRaisesRegex(ValueError, "symbolic links"):
                    HELPER.verify_sandbox(arguments)
                (external / "outside-link").unlink()
                os.link(source_file, external / "source-hardlink")
                with self.assertRaisesRegex(ValueError, "hardlinks a source"):
                    HELPER._validate_external_tree(external, source, identity)
                (external / "source-hardlink").unlink()
                os.mkfifo(external / "writerless-fifo", 0o600)
                with self.assertRaisesRegex(ValueError, "unsupported file type"):
                    HELPER.verify_sandbox(arguments)
                (external / "writerless-fifo").unlink()
                unsafe_mode = external / "group-writable"
                unsafe_mode.write_text("unsafe", encoding="utf-8")
                unsafe_mode.chmod(0o660)
                with self.assertRaisesRegex(ValueError, "unsafe permissions"):
                    HELPER.verify_sandbox(arguments)

    def test_rejects_missing_write_root_without_materializing_it(self) -> None:
        with tempfile.TemporaryDirectory(prefix="readonly-sandbox-") as raw:
            temporary = Path(raw)
            source = temporary / "source"
            framework = source / "framework"
            runner_temp = temporary / "runner-temp"
            framework.mkdir(parents=True)
            runner_temp.mkdir()
            missing_write = runner_temp / "missing"
            with self.assertRaisesRegex(ValueError, "write root must be an existing directory"):
                HELPER.validate_layout(
                    source_root=str(source), framework_root=str(framework),
                    write_root=str(missing_write), runner_temp=str(runner_temp),
                )
            self.assertFalse(missing_write.exists())

    def test_rejects_symlinked_write_root_without_creating_external_directory(self) -> None:
        with tempfile.TemporaryDirectory(prefix="readonly-sandbox-") as raw:
            temporary = Path(raw)
            source, framework, runner_temp, write = self.make_layout(temporary)
            outside = temporary / "outside"
            outside.mkdir()
            write.rmdir()
            write.symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "symbolic links"):
                HELPER.validate_layout(
                    source_root=str(source), framework_root=str(framework),
                    write_root=str(write), runner_temp=str(runner_temp),
                )
            self.assertFalse((outside / "external").exists())

    def test_rejects_source_traversal_before_any_filesystem_change(self) -> None:
        with tempfile.TemporaryDirectory(prefix="readonly-sandbox-") as raw:
            source, framework, runner_temp, write = self.make_layout(Path(raw))
            traversal = f"{source}/../source"
            with self.assertRaisesRegex(ValueError, "traversal"):
                HELPER.validate_layout(
                    source_root=traversal, framework_root=str(framework),
                    write_root=str(write), runner_temp=str(runner_temp),
                )
            self.assertFalse((write / "external").exists())

    def test_rejects_write_root_inside_source_tree(self) -> None:
        with tempfile.TemporaryDirectory(prefix="readonly-sandbox-") as raw:
            temporary = Path(raw)
            source = temporary / "source"
            framework = source / "framework"
            runner_temp = source / "runner-temp"
            write = runner_temp / "write"
            source.mkdir()
            framework.mkdir()
            runner_temp.mkdir()
            write.mkdir(mode=0o711)
            if os.geteuid() == 0:
                os.chown(write, 0, 0)
            with self.assertRaisesRegex(ValueError, "disjoint"):
                HELPER.validate_layout(
                    source_root=str(source), framework_root=str(framework),
                    write_root=str(write), runner_temp=str(runner_temp),
                )

    def test_rejects_validator_in_administrative_group(self) -> None:
        account = SimpleNamespace(pw_uid=1001, pw_gid=1001)
        validator_group = SimpleNamespace(gr_gid=1001, gr_name="validator", gr_mem=[])
        sudo_group = SimpleNamespace(gr_gid=27, gr_name="sudo", gr_mem=["validator"])
        with (
            mock.patch.object(HELPER.pwd, "getpwnam", return_value=account),
            mock.patch.object(HELPER.grp, "getgrnam", return_value=validator_group),
            mock.patch.object(HELPER.grp, "getgrgid", return_value=validator_group),
            mock.patch.object(HELPER.grp, "getgrall", return_value=[sudo_group]),
        ):
            with self.assertRaisesRegex(ValueError, "must not belong"):
                HELPER.resolve_validator_identity("validator", "validator")

    def test_rejects_nonempty_write_root_without_creating_external_directory(self) -> None:
        if os.geteuid() != 0:
            self.skipTest("root-owned write-root control requires root")
        with tempfile.TemporaryDirectory(prefix="readonly-sandbox-") as raw:
            source, framework, runner_temp, write = self.make_layout(Path(raw))
            marker = write / "already-present"
            marker.write_text("not fresh", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "newly created and empty"):
                HELPER.validate_layout(
                    source_root=str(source), framework_root=str(framework),
                    write_root=str(write), runner_temp=str(runner_temp),
                )
            self.assertFalse((write / "external").exists())


if __name__ == "__main__":
    unittest.main()
