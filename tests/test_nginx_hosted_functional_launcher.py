"""Unit coverage for the bounded Functional-A NGINX root launcher."""

from __future__ import annotations

import importlib.util
import os
import stat
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = ROOT / "connectors/nginx/harness/run_github_hosted_functional_a.py"


def load_launcher_module():
    spec = importlib.util.spec_from_file_location("nginx_functional_a_launcher", LAUNCHER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Functional-A launcher")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


LAUNCHER_MODULE = load_launcher_module()


class HostedFunctionalLauncherTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        connector = self.root / "connectors" / "nginx" / "harness"
        framework_rules = self.root / "modules" / "ModSecurity-test-Framework" / "tests" / "rules"
        connector.mkdir(parents=True)
        framework_rules.mkdir(parents=True)
        (framework_rules / "no-crs-baseline.conf").write_text("SecRuleEngine On\n", encoding="utf-8")
        exact = connector / "run_exact_head_use_error_log.sh"
        exact.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        exact.chmod(0o700)
        self.trusted_tmp = self.root / "trusted-tmp"
        self.trusted_tmp.mkdir()
        self.trusted_tmp.chmod(0o1777)
        self.job_root = self.trusted_tmp / (
            LAUNCHER_MODULE._FUNCTIONAL_JOB_ROOT_PREFIX + "fixture123"
        )
        self.job_root.mkdir(mode=0o700)
        self.job_root.chmod(0o711)
        self.verified = self.job_root / LAUNCHER_MODULE._VERIFIED_RUN_ROOT_NAME
        self.verified.mkdir(mode=0o700)
        self.verified.chmod(0o700)
        self.functional_parent = self.job_root / "ModSecurity-conector-nginx-functional-parent"
        self.functional_parent.mkdir(mode=0o711)
        self.functional_parent.chmod(0o711)
        self.prefix = self.verified / "nginx-prefix"
        (self.prefix / "sbin").mkdir(parents=True)
        (self.prefix / "modules").mkdir()
        nginx = self.prefix / "sbin" / "nginx"
        nginx.write_text("binary\n", encoding="utf-8")
        nginx.chmod(0o700)
        (self.prefix / "modules" / "ngx_http_modsecurity_module.so").write_bytes(b"module")
        self.build = self.verified / "nginx-build"
        self.build.mkdir()
        self.lib = self.verified / "modsecurity-lib"
        self.lib.mkdir()
        (self.lib / "libmodsecurity.so.3").write_bytes(b"runtime library")
        (self.lib / "libmodsecurity.so").symlink_to("libmodsecurity.so.3")
        self.env = {
            "VERIFIED_RUN_ROOT": str(self.verified),
            "NGINX_FUNCTIONAL_A_PARENT_ROOT": str(self.functional_parent),
            "NGINX_PREFIX": str(self.prefix),
            "NGINX_BUILD_DIR": str(self.build),
            "MODSECURITY_LIB_DIR": str(self.lib),
            "NGINX_FUNCTIONAL_WORKER_USER": "msconnector-nginx",
            "NGINX_FUNCTIONAL_WORKER_GROUP": "msconnector-nginx",
            "NGINX_PROTOCOL_PROFILE": "h1",
        }
        self.repo_patch = mock.patch.object(LAUNCHER_MODULE, "repository_root", return_value=self.root)
        self.tmp_root_patch = mock.patch.object(
            LAUNCHER_MODULE,
            "_require_trusted_functional_tmp_root",
            return_value=self.trusted_tmp,
        )
        self.repo_patch.start()
        self.tmp_root_patch.start()

    def tearDown(self) -> None:
        self.tmp_root_patch.stop()
        self.repo_patch.stop()
        self.tempdir.cleanup()

    def test_builds_deterministic_sudo_clean_environment_command(self) -> None:
        command = LAUNCHER_MODULE.build_root_command(self.env)
        self.assertEqual(command[:4], ["/usr/bin/sudo", "-n", "/usr/bin/env", "-i"])
        self.assertEqual(command[-2], "/bin/sh")
        self.assertEqual(command[-1], str(self.root / "connectors/nginx/harness/run_exact_head_use_error_log.sh"))
        assignments = dict(item.split("=", 1) for item in command[4:-2])
        self.assertEqual(assignments["PATH"], "/usr/bin:/bin")
        self.assertEqual(assignments["HOME"], "/nonexistent")
        self.assertEqual(
            assignments["NGINX_FUNCTIONAL_A_PARENT_ROOT"], str(self.functional_parent)
        )
        self.assertEqual(
            assignments["VERIFIED_RUN_ROOT"],
            str(self.functional_parent / "nginx-hosted-functional-a"),
        )
        self.assertEqual(
            assignments["NGINX_WORKER_USER"], self.env["NGINX_FUNCTIONAL_WORKER_USER"]
        )
        self.assertEqual(
            assignments["NGINX_WORKER_GROUP"], self.env["NGINX_FUNCTIONAL_WORKER_GROUP"]
        )
        self.assertEqual(assignments["NGINX_HOSTED_FUNCTIONAL_A"], "1")
        self.assertEqual(
            assignments["NGINX_FUNCTIONAL_A_RUNTIME_LIBRARY"],
            str(self.lib / "libmodsecurity.so.3"),
        )
        for forbidden in ("LD_PRELOAD", "LD_LIBRARY_PATH", "PYTHONPATH", "BASH_ENV", "ENV"):
            self.assertNotIn(forbidden, assignments)
        self.assertEqual(command, LAUNCHER_MODULE.build_root_command(dict(self.env)))

    def test_rejects_paths_outside_verified_root(self) -> None:
        outside = self.root / "outside"
        outside.mkdir()
        invalid = dict(self.env, NGINX_PREFIX=str(outside))
        with self.assertRaisesRegex(LAUNCHER_MODULE.FunctionalALaunchError, "below VERIFIED_RUN_ROOT"):
            LAUNCHER_MODULE.build_root_command(invalid)

    def test_rejects_unsafe_or_non_sibling_functional_parent(self) -> None:
        with self.assertRaisesRegex(
            LAUNCHER_MODULE.FunctionalALaunchError, "designated sibling"
        ):
            LAUNCHER_MODULE.build_root_command(
                dict(self.env, NGINX_FUNCTIONAL_A_PARENT_ROOT=str(self.verified / "nested"))
            )

        self.functional_parent.chmod(0o700)
        with self.assertRaisesRegex(LAUNCHER_MODULE.FunctionalALaunchError, "exactly non-enumerable mode 0711"):
            LAUNCHER_MODULE.build_root_command(self.env)
        self.functional_parent.chmod(0o711)

        self.job_root.chmod(0o700)
        try:
            with self.assertRaisesRegex(
                LAUNCHER_MODULE.FunctionalALaunchError,
                "job root must be exactly non-enumerable mode 0711",
            ):
                LAUNCHER_MODULE.build_root_command(self.env)
        finally:
            self.job_root.chmod(0o711)

    def test_rejects_correctly_bound_functional_parent_owned_by_another_user(self) -> None:
        original_lstat = Path.lstat

        def wrong_owner_lstat(path: Path) -> os.stat_result:
            metadata = original_lstat(path)
            if path == self.functional_parent:
                fields = list(metadata)
                fields[4] = os.geteuid() + 1
                return os.stat_result(fields)
            return metadata

        with mock.patch.object(Path, "lstat", new=wrong_owner_lstat):
            with self.assertRaisesRegex(
                LAUNCHER_MODULE.FunctionalALaunchError,
                "NGINX_FUNCTIONAL_A_PARENT_ROOT must be owned by the workflow runner",
            ):
                LAUNCHER_MODULE.build_root_command(self.env)

    def test_trusted_temporary_root_and_job_owner_contracts(self) -> None:
        self.tmp_root_patch.stop()
        try:
            self.assertEqual(LAUNCHER_MODULE._TRUSTED_FUNCTIONAL_TMP_ROOT, Path("/tmp"))
            sticky_root = os.stat_result(
                (stat.S_IFDIR | 0o1777, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            )
            with (
                mock.patch.object(
                    LAUNCHER_MODULE, "_require_directory", return_value=Path("/tmp")
                ),
                mock.patch.object(Path, "lstat", return_value=sticky_root),
            ):
                self.assertEqual(
                    LAUNCHER_MODULE._require_trusted_functional_tmp_root(), Path("/tmp")
                )

            unsafe_root = os.stat_result(
                (stat.S_IFDIR | 0o777, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            )
            with (
                mock.patch.object(
                    LAUNCHER_MODULE, "_require_directory", return_value=Path("/tmp")
                ),
                mock.patch.object(Path, "lstat", return_value=unsafe_root),
                self.assertRaisesRegex(
                    LAUNCHER_MODULE.FunctionalALaunchError, "root-owned sticky mode 01777"
                ),
            ):
                LAUNCHER_MODULE._require_trusted_functional_tmp_root()
        finally:
            self.tmp_root_patch.start()

        runner_uid = self.job_root.lstat().st_uid
        with mock.patch.object(LAUNCHER_MODULE.os, "geteuid", return_value=runner_uid + 1):
            with self.assertRaisesRegex(
                LAUNCHER_MODULE.FunctionalALaunchError, "job root must be owned"
            ):
                LAUNCHER_MODULE.build_root_command(self.env)

    def test_rejects_a_symlinked_functional_parent(self) -> None:
        self.functional_parent.rmdir()
        self.functional_parent.symlink_to("replacement", target_is_directory=True)
        with self.assertRaisesRegex(LAUNCHER_MODULE.FunctionalALaunchError, "symbolic link"):
            LAUNCHER_MODULE.build_root_command(self.env)

    def test_rejects_misbound_or_symlinked_functional_job_roots(self) -> None:
        misplaced_root = self.root / "misplaced-functional-job"
        misplaced_root.mkdir()
        misplaced_verified = misplaced_root / LAUNCHER_MODULE._VERIFIED_RUN_ROOT_NAME
        misplaced_verified.mkdir(mode=0o700)
        misplaced_verified.chmod(0o700)
        with self.assertRaisesRegex(
            LAUNCHER_MODULE.FunctionalALaunchError, "designated fresh /tmp job root"
        ):
            LAUNCHER_MODULE._require_private_verified_run_root(misplaced_verified)

        unexpected_verified = self.job_root / "unexpected-verified-root"
        unexpected_verified.mkdir(mode=0o700)
        unexpected_verified.chmod(0o700)
        with self.assertRaisesRegex(
            LAUNCHER_MODULE.FunctionalALaunchError, "designated private child"
        ):
            LAUNCHER_MODULE._require_private_verified_run_root(unexpected_verified)

        symlinked_root = self.trusted_tmp / (
            LAUNCHER_MODULE._FUNCTIONAL_JOB_ROOT_PREFIX + "symlink"
        )
        symlinked_root.symlink_to("replacement", target_is_directory=True)
        symlinked_verified = symlinked_root / LAUNCHER_MODULE._VERIFIED_RUN_ROOT_NAME
        with self.assertRaisesRegex(LAUNCHER_MODULE.FunctionalALaunchError, "symbolic link"):
            LAUNCHER_MODULE._require_private_verified_run_root(symlinked_verified)

    def test_rejects_symlinked_artifact_path(self) -> None:
        real = self.verified / "real-prefix"
        (real / "sbin").mkdir(parents=True)
        (real / "modules").mkdir()
        (real / "sbin" / "nginx").write_text("binary\n", encoding="utf-8")
        (real / "sbin" / "nginx").chmod(0o700)
        (real / "modules" / "ngx_http_modsecurity_module.so").write_bytes(b"module")
        symlink = self.verified / "symlink-prefix"
        symlink.symlink_to(real, target_is_directory=True)
        with self.assertRaisesRegex(LAUNCHER_MODULE.FunctionalALaunchError, "symbolic link"):
            LAUNCHER_MODULE.build_root_command(dict(self.env, NGINX_PREFIX=str(symlink)))

    def test_rejects_unbounded_worker_names_and_wrong_protocol(self) -> None:
        cases = [
            {"NGINX_FUNCTIONAL_WORKER_USER": "bad user"},
            {"NGINX_FUNCTIONAL_WORKER_GROUP": "-leading-dash"},
            {"NGINX_FUNCTIONAL_WORKER_USER": ""},
            {"NGINX_FUNCTIONAL_WORKER_GROUP": ""},
            {"NGINX_FUNCTIONAL_WORKER_USER": "x" * 65},
            {"NGINX_PROTOCOL_PROFILE": "h2"},
        ]
        for override in cases:
            with self.subTest(override=override):
                with self.assertRaises(LAUNCHER_MODULE.FunctionalALaunchError):
                    LAUNCHER_MODULE.build_root_command(dict(self.env, **override))

    def test_rejects_missing_or_non_regular_artifacts(self) -> None:
        missing = dict(self.env, MODSECURITY_LIB_DIR=str(self.verified / "missing"))
        with self.assertRaises(LAUNCHER_MODULE.FunctionalALaunchError):
            LAUNCHER_MODULE.build_root_command(missing)
        module_path = self.prefix / "modules" / "ngx_http_modsecurity_module.so"
        module_path.unlink()
        module_path.mkdir()
        with self.assertRaisesRegex(LAUNCHER_MODULE.FunctionalALaunchError, "regular file"):
            LAUNCHER_MODULE.build_root_command(self.env)

    def test_rejects_a_symlinked_runtime_library_even_when_the_generic_alias_exists(self) -> None:
        runtime_library = self.lib / "libmodsecurity.so.3"
        runtime_library.unlink()
        runtime_library.symlink_to("libmodsecurity.so")
        with self.assertRaisesRegex(LAUNCHER_MODULE.FunctionalALaunchError, "symbolic link"):
            LAUNCHER_MODULE.build_root_command(self.env)


if __name__ == "__main__":
    unittest.main()
