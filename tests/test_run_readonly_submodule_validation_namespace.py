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
HELPER_PATH = ROOT / "ci/tools/run-readonly-submodule-validation-namespace.py"
SPEC = importlib.util.spec_from_file_location("readonly_namespace_runner", HELPER_PATH)
assert SPEC is not None
assert SPEC.loader is not None
HELPER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = HELPER
SPEC.loader.exec_module(HELPER)


class ReadonlySubmoduleValidationNamespaceTests(unittest.TestCase):
    def test_procfs_target_is_the_exported_literal_target(self) -> None:
        self.assertEqual(HELPER.PROCFS_TARGET, Path("/proc"))

    def test_identity_rejects_privileged_or_missing_account_topologies(self) -> None:
        account = SimpleNamespace(pw_uid=1001, pw_gid=1001)
        validator = SimpleNamespace(gr_name="validator", gr_gid=1001, gr_mem=())
        primary = SimpleNamespace(gr_name="validator", gr_gid=1001, gr_mem=())
        cases = {
            "root uid": (SimpleNamespace(pw_uid=0, pw_gid=1001), validator, primary, [validator], True),
            "requested gid zero": (account, SimpleNamespace(gr_name="validator", gr_gid=0, gr_mem=()), primary, [validator], True),
            "primary gid zero": (SimpleNamespace(pw_uid=1001, pw_gid=0), validator, SimpleNamespace(gr_name="root", gr_gid=0, gr_mem=()), [validator], True),
            "primary root name": (account, validator, SimpleNamespace(gr_name="root", gr_gid=1001, gr_mem=()), [validator], True),
            "root membership": (account, validator, primary, [validator, SimpleNamespace(gr_name="root", gr_gid=100, gr_mem=("validator",))], True),
            "missing membership": (account, validator, SimpleNamespace(gr_name="other", gr_gid=1001, gr_mem=()), [SimpleNamespace(gr_name="other", gr_gid=1001, gr_mem=())], True),
            "sudo membership": (account, validator, primary, [validator, SimpleNamespace(gr_name="sudo", gr_gid=27, gr_mem=("validator",))], True),
            "wheel membership": (account, validator, primary, [validator, SimpleNamespace(gr_name="wheel", gr_gid=10, gr_mem=("validator",))], True),
            "admin membership": (account, validator, primary, [validator, SimpleNamespace(gr_name="admin", gr_gid=20, gr_mem=("validator",))], True),
        }
        for name, (case_account, requested, case_primary, groups, rejects) in cases.items():
            with self.subTest(name=name), mock.patch.object(HELPER.pwd, "getpwnam", return_value=case_account), mock.patch.object(HELPER.grp, "getgrnam", return_value=requested), mock.patch.object(HELPER.grp, "getgrgid", return_value=case_primary), mock.patch.object(HELPER.grp, "getgrall", return_value=groups):
                if rejects:
                    with self.assertRaises(ValueError):
                        HELPER._identity("validator", "validator")
        for missing in ("user", "group"):
            with self.subTest(missing=missing), mock.patch.object(HELPER.pwd, "getpwnam", side_effect=KeyError() if missing == "user" else lambda _name: account), mock.patch.object(HELPER.grp, "getgrnam", side_effect=KeyError() if missing == "group" else lambda _name: validator), mock.patch.object(HELPER.grp, "getgrgid", return_value=primary):
                with self.assertRaisesRegex(ValueError, "must already exist"):
                    HELPER._identity("validator", "validator")

    def test_no_new_privileges_fails_closed_when_prctl_is_rejected(self) -> None:
        with mock.patch.object(HELPER.LIBC, "prctl", return_value=0) as prctl:
            HELPER._set_no_new_privs()
        prctl.assert_called_once_with(HELPER.PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0)
        with mock.patch.object(HELPER.LIBC, "prctl", return_value=-1), mock.patch.object(HELPER.ctypes, "get_errno", return_value=1):
            with self.assertRaisesRegex(OSError, "no_new_privs"):
                HELPER._set_no_new_privs()

    def test_cli_requires_all_physical_roots_and_identity(self) -> None:
        required = [
            "--source-root", "/source", "--framework-root", "/source/modules/framework",
            "--write-root", "/write", "--external-root", "/write/external",
            "--validator-user", "validator", "--validator-group", "validator",
            "--python", "/usr/bin/python3",
        ]
        with self.assertRaises(SystemExit):
            HELPER.parse_args(required)
        arguments = HELPER.parse_args(
            required + ["--namespace-parent", "/tmp/modsecurity-readonly-namespace.test"]
        )
        self.assertEqual(arguments.namespace_parent, "/tmp/modsecurity-readonly-namespace.test")
        self.assertEqual(arguments.external_root, "/write/external")

    def test_namespace_parent_validation_rejects_untrusted_topologies(self) -> None:
        parent = Path("/tmp/modsecurity-readonly-namespace.test")
        directory = stat.S_IFDIR
        valid_tmp = SimpleNamespace(st_mode=directory | 0o1777, st_uid=0, st_gid=0)
        valid_parent = SimpleNamespace(st_mode=directory | 0o750, st_uid=0, st_gid=4242)
        with mock.patch.object(
            HELPER.os, "lstat", side_effect=(valid_tmp, valid_parent)
        ), mock.patch.object(HELPER.os, "scandir", return_value=[]):
            HELPER._validate_namespace_parent(parent, 4242)
        cases = {
            "bad tmp ancestor": (SimpleNamespace(st_mode=directory | 0o777, st_uid=0, st_gid=0), valid_parent, []),
            "wrong owner": (valid_tmp, SimpleNamespace(st_mode=directory | 0o750, st_uid=1, st_gid=4242), []),
            "wrong group": (valid_tmp, SimpleNamespace(st_mode=directory | 0o750, st_uid=0, st_gid=1), []),
            "wrong mode": (valid_tmp, SimpleNamespace(st_mode=directory | 0o755, st_uid=0, st_gid=4242), []),
            "nonempty": (valid_tmp, valid_parent, [SimpleNamespace(name="unexpected")]),
        }
        with self.assertRaisesRegex(ValueError, "sticky ancestor"):
            HELPER._validate_namespace_parent(Path("/tmp"), 4242)
        for name, (tmp_metadata, parent_metadata, contents) in cases.items():
            with self.subTest(name=name), mock.patch.object(
                HELPER.os, "lstat", side_effect=(tmp_metadata, parent_metadata)
            ), mock.patch.object(HELPER.os, "scandir", return_value=contents):
                with self.assertRaises(ValueError):
                    HELPER._validate_namespace_parent(parent, 4242)

    def test_main_blocks_runtime_errors_including_namespace_unavailability(self) -> None:
        for error in (RuntimeError("unsafe mount layout"), HELPER.NamespaceUnavailable("unshare denied")):
            with self.subTest(error=type(error).__name__), mock.patch.object(
                HELPER, "parse_args", return_value=SimpleNamespace()
            ), mock.patch.object(HELPER, "run", side_effect=error), mock.patch.object(
                HELPER.sys, "stderr"
            ) as stderr:
                self.assertEqual(HELPER.main([]), 2)
                self.assertIn(str(error), "".join(call.args[0] for call in stderr.write.call_args_list))

    def test_run_fails_closed_and_removes_mount_layout_after_unexpected_setup_errors(self) -> None:
        for error_type in (OSError, RuntimeError):
            with self.subTest(error_type=error_type.__name__), tempfile.TemporaryDirectory() as raw:
                root = Path(raw)
                source = root / "source"
                framework = source / "modules" / "framework"
                write_root = root / "write"
                external = write_root / "external"
                namespace_parent = root / "namespace-parent"
                framework.mkdir(parents=True)
                external.mkdir(parents=True)
                namespace_parent.mkdir()
                mount_root = namespace_parent / "mount-root"
                (mount_root / "source").mkdir(parents=True)
                (mount_root / "external").mkdir()
                os.chmod(write_root, 0o711)
                os.chmod(external, 0o700)
                arguments = SimpleNamespace(
                    source_root=str(source), framework_root=str(framework),
                    write_root=str(write_root), external_root=str(external),
                    namespace_parent=str(namespace_parent), python=sys.executable,
                    validator_user="validator", validator_group="validator",
                )
                with mock.patch.object(HELPER.os, "geteuid", return_value=0), mock.patch.object(
                    HELPER,
                    "_validated_configuration",
                    return_value=(
                        source, framework, write_root, external, namespace_parent,
                        Path(sys.executable), os.getuid(), os.getgid(),
                    ),
                ), mock.patch.object(HELPER, "_create_mount_layout", return_value=mount_root
                ), mock.patch.object(HELPER, "_mountinfo_for", return_value=[]), mock.patch.object(
                    HELPER.os, "fork", return_value=1
                ), mock.patch.object(HELPER.os, "waitpid", side_effect=error_type("unexpected setup failure")):
                    with self.assertRaises(error_type):
                        HELPER.run(arguments)
                self.assertFalse(mount_root.exists())

    def test_candidate_environment_uses_only_namespace_views_for_sources(self) -> None:
        source = Path("/tmp/task/source")
        external = Path("/tmp/task/external")
        environment = HELPER._candidate_environment(
            source, Path("modules/ModSecurity-test-Framework"), external, Path("/tmp/task"), Path("/usr/bin/python3")
        )
        self.assertEqual(environment["GITHUB_WORKSPACE"], str(source))
        self.assertEqual(
            environment["FRAMEWORK_ROOT"], "/tmp/task/source/modules/ModSecurity-test-Framework"
        )
        self.assertEqual(environment["PATH"], HELPER.SAFE_PATH)
        self.assertEqual(environment["GITHUB_ACTIONS"], "true")
        self.assertEqual(environment["BUILD_ROOT"], "/tmp/task/external/build")
        self.assertEqual(environment["VALIDATION_WRITE_ROOT"], "/tmp/task")
        self.assertNotIn("SUDO", " ".join(environment))
        self.assertEqual(
            set(environment),
            {
                "PATH", "PYTHON", "HOME", "TMPDIR", "TMP", "TEMP", "XDG_CACHE_HOME",
                "XDG_CONFIG_HOME", "XDG_DATA_HOME", "XDG_STATE_HOME", "PIP_CACHE_DIR",
                "PYTHONPYCACHEPREFIX", "PYTHONUSERBASE", "PYTHONPATH", "PYTHONNOUSERSITE",
                "PYTHONDONTWRITEBYTECODE", "GIT_CONFIG_GLOBAL", "GIT_CONFIG_NOSYSTEM",
                "GIT_OPTIONAL_LOCKS", "GITHUB_ACTIONS", "GITHUB_WORKSPACE", "FRAMEWORK_ROOT", "VALIDATOR_EXTERNAL_ROOT",
                "BUILD_ROOT",
                "VALIDATION_WRITE_ROOT", "VERIFIED_RUN_ROOT", "VERIFIED_STATE_ROOT", "VERIFIED_BUILD_ROOT",
                "VERIFIED_SOURCE_ROOT", "VERIFIED_TMP_ROOT", "VERIFIED_LOG_ROOT", "CACHE_ROOT",
                "VERIFIED_COMPONENT_CACHE", "CONNECTOR_COMPONENT_CACHE", "VERIFIED_EVIDENCE_ROOT",
                "EVIDENCE_ROOT", "RUNTIME_EVIDENCE_ROOT", "RUNTIME_RUN_ROOT", "RUNTIME_LOG_ROOT",
                "SOURCE_ROOT", "TMP_ROOT", "LOG_ROOT", "MATRIX_ROOT",
            },
        )
        for key, value in environment.items():
            if key not in {
                "PATH", "PYTHON", "GITHUB_ACTIONS", "GITHUB_WORKSPACE", "FRAMEWORK_ROOT", "PYTHONNOUSERSITE",
                "PYTHONDONTWRITEBYTECODE", "GIT_CONFIG_NOSYSTEM", "GIT_OPTIONAL_LOCKS", "VALIDATION_WRITE_ROOT",
            }:
                self.assertTrue(value.startswith(str(external)), key)

    def test_rejects_external_root_outside_the_physical_write_root(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            source = root / "source"; framework = source / "modules" / "framework"
            source.mkdir(); framework.mkdir(parents=True)
            write = root / "write"; external = root / "outside"; write.mkdir(); external.mkdir()
            os.chmod(write, 0o711); os.chmod(external, 0o700)
            arguments = HELPER.parse_args(
                ["--source-root", str(source), "--framework-root", str(framework),
                 "--write-root", str(write), "--external-root", str(external),
                 "--validator-user", "nobody", "--validator-group", "nogroup", "--python", sys.executable,
                 "--namespace-parent", "/tmp/modsecurity-readonly-namespace.test"]
            )
            # The topology validation is intentionally tested independently
            # from the production root gate: hosted lint invokes this module
            # as an ordinary runner user.
            with mock.patch.object(HELPER.os, "geteuid", return_value=0):
                with self.assertRaisesRegex(ValueError, "exactly the write root external child"):
                    HELPER.run(arguments)

    def test_mount_verifier_rejects_missing_readonly_or_security_flags(self) -> None:
        target = Path("/tmp/namespace-test-target")
        with mock.patch.object(HELPER, "_mountinfo_for", return_value=["1 2 0:1 / /tmp/namespace-test-target rw - ext4 /dev/x rw"]):
            with self.assertRaisesRegex(RuntimeError, "unsafe mount flags"):
                HELPER._verify_mount(target, readonly=True)

    def test_procfs_verifier_requires_one_hardened_proc_mount_at_literal_target(self) -> None:
        hardened = "99 1 0:42 / /proc ro,nosuid,nodev,noexec - proc proc rw"
        inherited = "98 1 0:42 / /proc rw,nosuid,nodev,noexec - proc proc rw"
        with mock.patch.object(HELPER, "_mountinfo_for", return_value=[inherited, hardened]):
            HELPER._verify_procfs(HELPER.PROCFS_TARGET)
        for rows in (
            [inherited],
            ["99 1 0:42 / /proc ro,nosuid,nodev - proc proc rw"],
            ["99 1 0:42 / /proc ro,nosuid,nodev,noexec - sysfs sysfs rw"],
            [hardened, hardened],
        ):
            with self.subTest(rows=rows), mock.patch.object(HELPER, "_mountinfo_for", return_value=rows):
                with self.assertRaisesRegex(RuntimeError, "hardened procfs"):
                    HELPER._verify_procfs(HELPER.PROCFS_TARGET)
        with self.assertRaisesRegex(RuntimeError, "literal /proc"):
            HELPER._verify_procfs(Path("/untrusted-proc"))

    def test_procfs_verification_failure_never_runs_candidate_and_restores_proc(self) -> None:
        class ChildExit(BaseException):
            pass

        source = Path("/source")
        framework = source / "modules/framework"
        external = Path("/external")
        mount_root = Path("/mount-root")
        candidate = mock.Mock()
        with mock.patch.object(HELPER, "_unshare"), mock.patch.object(
            HELPER, "_mount"
        ) as mount, mock.patch.object(HELPER, "_verify_mount"), mock.patch.object(
            HELPER, "_mountinfo_for", return_value=[]
        ), mock.patch.object(HELPER.os, "pipe", return_value=(30, 31)), mock.patch.object(
            HELPER.os, "fork", return_value=0
        ), mock.patch.object(HELPER.os, "close"), mock.patch.object(
            HELPER.os, "_exit", side_effect=ChildExit
        ), mock.patch.object(HELPER, "_verify_procfs", side_effect=RuntimeError("proc verification failed")), mock.patch.object(
            HELPER, "_umount"
        ) as umount, mock.patch.object(HELPER, "_set_no_new_privs") as no_new_privs:
            with self.assertRaises(ChildExit):
                HELPER._namespace_child(source, framework, external, mount_root, Path("/python"), 1000, 1000, candidate)
        candidate.assert_not_called()
        no_new_privs.assert_not_called()
        mount.assert_any_call("proc", HELPER.PROCFS_TARGET, HELPER.MS_RDONLY | HELPER.MS_NOSUID | HELPER.MS_NODEV | HELPER.MS_NOEXEC, "proc")
        umount.assert_called_once_with(HELPER.PROCFS_TARGET)

    def test_parent_restores_procfs_only_after_waiting_for_pid_one(self) -> None:
        source = Path("/source")
        framework = source / "modules/framework"
        external = Path("/external")
        mount_root = Path("/mount-root")
        events: list[tuple[str, object]] = []

        def waitpid(pid: int, options: int) -> tuple[int, int]:
            events.append(("waitpid", pid))
            self.assertEqual(options, 0)
            return pid, 0

        def umount(target: Path) -> None:
            events.append(("umount", target))

        mountinfo = mock.Mock(side_effect=[
            ["inherited-proc"],
            ["inherited-proc"],
        ])
        with mock.patch.object(HELPER, "_unshare"), mock.patch.object(
            HELPER, "_mount"
        ), mock.patch.object(HELPER, "_verify_mount"), mock.patch.object(
            HELPER, "_mountinfo_for", mountinfo
        ), mock.patch.object(HELPER.os, "pipe", return_value=(30, 31)), mock.patch.object(
            HELPER.os, "fork", return_value=4321
        ), mock.patch.object(HELPER.os, "close"), mock.patch.object(
            HELPER.os, "read", return_value=b"1"
        ), mock.patch.object(HELPER.os, "waitpid", side_effect=waitpid), mock.patch.object(
            HELPER, "_umount", side_effect=umount
        ):
            result = HELPER._namespace_child(
                source, framework, external, mount_root, Path("/python"), 1000, 1000
            )

        self.assertEqual(result, 0)
        self.assertEqual(
            events,
            [
                ("waitpid", 4321),
                ("umount", HELPER.PROCFS_TARGET),
                ("umount", mount_root / "external"),
                ("umount", mount_root / "source"),
            ],
        )
        self.assertEqual(mountinfo.call_args_list[0], mock.call(HELPER.PROCFS_TARGET))
        self.assertEqual(mountinfo.call_args_list[1], mock.call(HELPER.PROCFS_TARGET))

    def test_post_ready_child_failure_transfers_procfs_cleanup_to_parent(self) -> None:
        class ChildExit(BaseException):
            pass

        candidate_arguments = (
            Path("/source"),
            Path("modules/framework"),
            Path("/external"),
            Path("/mount-root"),
            Path("/python"),
            1000,
            1000,
        )
        readiness = bytearray()
        candidate = mock.Mock()

        def write(_descriptor: int, value: bytes) -> int:
            readiness.extend(value)
            return len(value)

        child_umount = mock.Mock()
        with mock.patch.object(HELPER, "_mount"), mock.patch.object(
            HELPER, "_verify_procfs"
        ), mock.patch.object(HELPER.os, "write", side_effect=write) as child_write, mock.patch.object(
            HELPER.os, "close"
        ), mock.patch.object(
            HELPER, "_set_no_new_privs", side_effect=RuntimeError("no_new_privs failed")
        ), mock.patch.object(HELPER, "_umount", child_umount), mock.patch.object(
            HELPER.os, "_exit", side_effect=ChildExit
        ):
            with self.assertRaises(ChildExit):
                HELPER._run_pid1_candidate(
                    candidate_arguments,
                    candidate,
                    (30, 31),
                    ["inherited-proc"],
                )

        child_write.assert_called_once_with(31, b"1")
        self.assertEqual(bytes(readiness), b"1")
        candidate.assert_not_called()
        child_umount.assert_not_called()

        parent_umount = mock.Mock()
        parent_read = mock.Mock(return_value=bytes(readiness))
        with mock.patch.object(HELPER, "_unshare"), mock.patch.object(
            HELPER, "_mount"
        ), mock.patch.object(HELPER, "_verify_mount"), mock.patch.object(
            HELPER, "_mountinfo_for", side_effect=[["inherited-proc"], ["inherited-proc"]]
        ), mock.patch.object(HELPER.os, "pipe", return_value=(30, 31)), mock.patch.object(
            HELPER.os, "fork", return_value=4321
        ), mock.patch.object(HELPER.os, "close"), mock.patch.object(
            HELPER.os, "read", parent_read
        ), mock.patch.object(HELPER.os, "waitpid", return_value=(4321, 127 << 8)), mock.patch.object(
            HELPER, "_umount", parent_umount
        ):
            result = HELPER._namespace_child(
                Path("/source"),
                Path("/source/modules/framework"),
                Path("/external"),
                Path("/mount-root"),
                Path("/python"),
                1000,
                1000,
            )

        self.assertEqual(result, 127)
        parent_read.assert_called_once_with(30, 1)
        self.assertEqual(
            [call for call in parent_umount.call_args_list if call == mock.call(HELPER.PROCFS_TARGET)],
            [mock.call(HELPER.PROCFS_TARGET)],
        )

    def test_mount_layout_forces_traversable_root_validator_modes_despite_umask(self) -> None:
        if os.geteuid() != 0:
            self.skipTest("root ownership verification is unavailable")
        with tempfile.TemporaryDirectory() as raw:
            validator_gid = os.getgid()
            previous_umask = os.umask(0o077)
            try:
                root = HELPER._create_mount_layout(Path(raw), validator_gid)
            finally:
                os.umask(previous_umask)
            try:
                self.assertEqual(root.parent, Path(raw))
                self.assertEqual(root.name, "mount-root")
                for path in (root, root / "source", root / "external"):
                    metadata = os.lstat(path)
                    self.assertEqual((metadata.st_uid, metadata.st_gid), (0, validator_gid))
                    self.assertEqual(stat.S_IMODE(metadata.st_mode), 0o750)
                    self.assertTrue(stat.S_ISDIR(metadata.st_mode))
                    self.assertFalse(stat.S_ISLNK(metadata.st_mode))
            finally:
                os.rmdir(root / "source"); os.rmdir(root / "external"); os.rmdir(root)

    def test_launcher_never_uses_tempfile_or_python_chmod_for_mount_layout(self) -> None:
        launcher = HELPER_PATH.read_text(encoding="utf-8")
        self.assertNotIn("tempfile", launcher)
        self.assertNotIn("os.chmod(", launcher)

    def test_fixed_candidate_program_keeps_all_isolation_probes_and_pid1_exec(self) -> None:
        program = HELPER._candidate_script()
        for required in (
            "umask 077", "CapEff", "NoNewPrivs", "GITHUB_WORKSPACE/.git", "FRAMEWORK_ROOT/.git",
            "VALIDATION_WRITE_ROOT/.readonly-validator-guard-probe", "/usr/bin/sudo",
            "/usr/bin/mount -o remount,rw", "VALIDATOR_EXTERNAL_ROOT/write-probe",
            "-m pip install", "exec make", "safe.directory", "expect_blocked mv",
            "expect_blocked rm", "expect_blocked chmod",
        ):
            self.assertIn(required, program)
        self.assertIn('exec make PYTHON="$PYTHON" quick-check', program)
        self.assertNotIn('exec make PYTHON="$PYTHON" BUILD_ROOT=', program)
        self.assertNotIn("eval ", program)

    def test_environment_build_root_does_not_override_nested_make_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            fixture_build_root = root / "fixture-build"
            (root / "parent.mk").write_text(
                ".PHONY: check\n"
                "check:\n"
                "\t@$(MAKE) --no-print-directory -f child.mk verify\n",
                encoding="utf-8",
            )
            (root / "child.mk").write_text(
                f"BUILD_ROOT := {fixture_build_root}\n"
                ".PHONY: verify\n"
                "verify:\n"
                f"\t@test \"$(BUILD_ROOT)\" = \"{fixture_build_root}\"\n",
                encoding="utf-8",
            )
            environment = os.environ.copy()
            environment["BUILD_ROOT"] = str(root / "candidate-external" / "build")

            environment_result = subprocess.run(
                ["make", "--no-print-directory", "-f", "parent.mk", "check"],
                cwd=root,
                env=environment,
                check=False,
                capture_output=True,
                text=True,
            )
            command_line_result = subprocess.run(
                [
                    "make", "--no-print-directory", "-f", "parent.mk",
                    f"BUILD_ROOT={environment['BUILD_ROOT']}", "check",
                ],
                cwd=root,
                env=environment,
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(environment_result.returncode, 0, environment_result.stderr)
            self.assertNotEqual(command_line_result.returncode, 0)

    def test_privileged_namespace_mount_integration(self) -> None:
        """Exercise a real private read-only bind mount when the kernel permits it."""
        if os.geteuid() != 0 or sys.platform != "linux":
            self.skipTest("mount/PID namespace capability is unavailable")
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw); source = root / "source"; target = root / "target"
            source.mkdir(); target.mkdir()
            child = os.fork()
            if child == 0:
                try:
                    HELPER._unshare()
                    HELPER._mount(None, Path("/"), HELPER.MS_REC | HELPER.MS_PRIVATE)
                    HELPER._mount(str(source), target, HELPER.MS_BIND)
                    HELPER._mount(None, target, HELPER.MS_BIND | HELPER.MS_REMOUNT | HELPER.MS_RDONLY | HELPER.MS_NOSUID | HELPER.MS_NODEV)
                    HELPER._verify_mount(target, readonly=True)
                    before_proc = HELPER._mountinfo_for(Path("/proc"))
                    HELPER._mount("proc", Path("/proc"), HELPER.MS_RDONLY | HELPER.MS_NOSUID | HELPER.MS_NODEV | HELPER.MS_NOEXEC, "proc")
                    HELPER._verify_procfs(Path("/proc"))
                    HELPER._umount(Path("/proc"))
                    if HELPER._mountinfo_for(Path("/proc")) != before_proc:
                        os._exit(1)
                    HELPER._umount(target)
                except HELPER.NamespaceUnavailable:
                    os._exit(125)
                except BaseException:
                    os._exit(1)
                os._exit(0)
            _pid, status = os.waitpid(child, 0)
            code = os.waitstatus_to_exitcode(status)
            if code == 125:
                self.skipTest("mount/PID namespace capability is unavailable")
            self.assertEqual(code, 0)

    def test_privileged_candidate_cannot_mutate_mounts_or_outlive_pid1(self) -> None:
        """Exercise drop, read-only views, external output, and PID-namespace reaping."""
        if os.geteuid() != 0 or sys.platform != "linux":
            self.skipTest("mount/PID namespace capability is unavailable")
        try:
            account = pwd.getpwnam("nobody")
            group = HELPER.grp.getgrgid(account.pw_gid)
        except KeyError:
            self.skipTest("dedicated unprivileged identity capability is unavailable")

        def mapped(identifier: int, map_name: str) -> bool:
            for row in Path(f"/proc/self/{map_name}").read_text(encoding="utf-8").splitlines():
                inside, _outside, count = (int(value) for value in row.split())
                if inside <= identifier < inside + count:
                    return True
            return False

        if not mapped(account.pw_uid, "uid_map") or not mapped(group.gr_gid, "gid_map"):
            self.skipTest("dedicated unprivileged identity capability is unavailable")
        host_proc_before = HELPER._mountinfo_for(Path("/proc"))
        # The validator must traverse every fixture ancestor after its UID drop.
        # The task-local TMPDIR may be root-only, so use the host's sticky /tmp.
        with tempfile.TemporaryDirectory(dir="/tmp", prefix="readonly-namespace-") as raw:
            root = Path(raw); os.chmod(root, 0o755)
            source = root / "source"; framework = source / "modules" / "framework"
            framework.mkdir(parents=True); (source / ".git" / "modules").mkdir(parents=True)
            (framework / ".git").mkdir(); (source / "Makefile").write_text("parent", encoding="utf-8")
            (framework / "Makefile").write_text("framework", encoding="utf-8")
            external = root / "external"; external.mkdir(); os.chown(external, account.pw_uid, group.gr_gid); os.chmod(external, 0o700)
            mount_root = root / "mount-root"; mount_root.mkdir(mode=0o755)
            (mount_root / "source").mkdir(mode=0o755); (mount_root / "external").mkdir(mode=0o755)
            ready_read, ready_write = os.pipe()
            control_read, control_write = os.pipe()
            release_read, release_write = os.pipe()

            def candidate(source_view: Path, framework_relative: Path, external_view: Path, _guard: Path, _python: Path, uid: int, gid: int) -> None:
                if "NoNewPrivs:\t1" not in Path("/proc/self/status").read_text(encoding="utf-8"):
                    os._exit(1)
                local_pid = os.getpid()
                if local_pid != 1 or not Path(f"/proc/{local_pid}/task/{local_pid}").is_dir():
                    os._exit(1)
                if os.readlink("/proc/self/ns/pid") != os.readlink(f"/proc/{local_pid}/ns/pid"):
                    os._exit(1)
                os.setgroups([]); os.setgid(gid); os.setuid(uid); os.chdir(source_view)
                framework_view = source_view / framework_relative
                def blocked(operation: object) -> None:
                    with self.assertRaises(OSError):
                        operation()  # type: ignore[operator]
                blocked(lambda: (source_view / "create").touch())
                blocked(lambda: (framework_view / "create").touch())
                blocked(lambda: (source_view / ".git" / "index.lock").touch())
                blocked(lambda: (framework_view / ".git" / "index.lock").touch())
                blocked(lambda: os.chmod(source_view / "Makefile", 0o600))
                blocked(lambda: os.chmod(framework_view / "Makefile", 0o600))
                blocked(lambda: os.chmod(source_view / ".git", 0o600))
                blocked(lambda: os.chmod(framework_view / ".git", 0o600))
                blocked(lambda: os.rename(source_view / "Makefile", source_view / "renamed"))
                blocked(lambda: os.rename(framework_view / "Makefile", framework_view / "renamed"))
                blocked(lambda: os.rename(source_view / ".git", source_view / "renamed-git"))
                blocked(lambda: os.rename(framework_view / ".git", framework_view / "renamed-git"))
                blocked(lambda: os.unlink(source_view / "Makefile"))
                blocked(lambda: os.unlink(framework_view / "Makefile"))
                (external_view / "candidate-output").write_text("allowed", encoding="utf-8")
                background = os.fork()
                if background == 0:
                    os.close(release_read)
                    os.write(ready_write, b"ready")
                    os.read(control_read, 1)
                    (external_view / "background-after-pid1").touch()
                    os._exit(0)
                os.close(control_read)
                os.close(ready_write)
                os.read(release_read, 1)
                os.close(release_read)
                os._exit(0)

            child = os.fork()
            if child == 0:
                os.close(ready_read); os.close(control_write); os.close(release_write)
                try:
                    os._exit(HELPER._namespace_child(
                        source, framework, external, mount_root, Path(sys.executable), account.pw_uid,
                        group.gr_gid, candidate, (ready_write, control_read, release_read),
                    ))
                except HELPER.NamespaceUnavailable:
                    os._exit(125)
                except BaseException:
                    os._exit(1)
            os.close(ready_write); os.close(control_read); os.close(release_read)
            ready = os.read(ready_read, 8); os.close(ready_read)
            if ready == b"ready":
                os.write(release_write, b"exit")
            os.close(release_write)
            _pid, status = os.waitpid(child, 0)
            code = os.waitstatus_to_exitcode(status)
            if code == 125:
                os.close(control_write)
                self.skipTest("mount/PID namespace capability is unavailable")
            self.assertEqual(code, 0)
            self.assertEqual((external / "candidate-output").read_text(encoding="utf-8"), "allowed")
            self.assertEqual((source / "Makefile").read_text(encoding="utf-8"), "parent")
            self.assertFalse((source / "background-write").exists())
            self.assertFalse(HELPER._mountinfo_for(mount_root))
            self.assertEqual(ready, b"ready")
            with self.assertRaises(BrokenPipeError):
                os.write(control_write, b"continue")
            os.close(control_write)
            self.assertFalse((external / "background-after-pid1").exists())
            os.rmdir(mount_root / "source"); os.rmdir(mount_root / "external"); os.rmdir(mount_root)
        self.assertEqual(HELPER._mountinfo_for(Path("/proc")), host_proc_before)


if __name__ == "__main__":
    unittest.main()
