"""Unit coverage for the bounded Functional-A NGINX root launcher."""

from __future__ import annotations

import importlib.util
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
        self.verified = self.root / "verified"
        self.verified.mkdir()
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
        (self.lib / "libmodsecurity.so").write_bytes(b"library")
        self.env = {
            "VERIFIED_RUN_ROOT": str(self.verified),
            "NGINX_PREFIX": str(self.prefix),
            "NGINX_BUILD_DIR": str(self.build),
            "MODSECURITY_LIB_DIR": str(self.lib),
            "NGINX_FUNCTIONAL_WORKER_USER": "msconnector-nginx",
            "NGINX_FUNCTIONAL_WORKER_GROUP": "msconnector-nginx",
            "NGINX_PROTOCOL_PROFILE": "h1",
        }
        self.repo_patch = mock.patch.object(LAUNCHER_MODULE, "repository_root", return_value=self.root)
        self.repo_patch.start()

    def tearDown(self) -> None:
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
            assignments["NGINX_FUNCTIONAL_A_PARENT_ROOT"], str(self.verified)
        )
        self.assertEqual(assignments["NGINX_HOSTED_FUNCTIONAL_A"], "1")
        for forbidden in ("LD_PRELOAD", "LD_LIBRARY_PATH", "PYTHONPATH", "BASH_ENV", "ENV"):
            self.assertNotIn(forbidden, assignments)
        self.assertEqual(command, LAUNCHER_MODULE.build_root_command(dict(self.env)))

    def test_rejects_paths_outside_verified_root(self) -> None:
        outside = self.root / "outside"
        outside.mkdir()
        invalid = dict(self.env, NGINX_PREFIX=str(outside))
        with self.assertRaisesRegex(LAUNCHER_MODULE.FunctionalALaunchError, "below VERIFIED_RUN_ROOT"):
            LAUNCHER_MODULE.build_root_command(invalid)

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


if __name__ == "__main__":
    unittest.main()
