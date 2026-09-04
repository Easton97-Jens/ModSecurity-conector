"""Regression tests for the unprivileged exact-head candidate artifact packer."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "ci/runtime/broker/protected_nginx_exact_head_builder.py"
SHA = "a" * 40
BASE = "b" * 40


def load_module() -> object:
    spec = importlib.util.spec_from_file_location("protected_exact_head_builder", MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


B = load_module()


class CandidateBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.task_root = self.root / "task"
        self.task_root.mkdir(mode=0o700)
        self.build_root = self.task_root / "build"
        self.build_root.mkdir(mode=0o700)
        self.lib_dir = self.build_root / "lib"
        self.lib_dir.mkdir(mode=0o700)
        self.nginx_build = self.build_root / "nginx-build"
        (self.nginx_build / "verified-archives").mkdir(parents=True, mode=0o700)
        self.binary = self.build_root / "nginx-bin"
        self.module = self.build_root / "module.so"
        self.library = self.lib_dir / "libmodsecurity.so.3"
        self.archive = self.nginx_build / "verified-archives" / "nginx-1.31.4.tar.gz"
        for path, content in (
            (self.binary, b"binary"),
            (self.module, b"module"),
            (self.library, b"library"),
            (self.archive, b"source archive"),
        ):
            path.write_bytes(content)
            path.chmod(0o600)
        self.snapshot = self.task_root / "runtime.env"
        self.snapshot.write_text(
            "\n".join(
                (
                    "export RUNTIME_COMPONENT_ENV_SNAPSHOT_TARGET='nginx'",
                    "export MRTS_NATIVE_NGINX_BIN='" + str(self.binary) + "'",
                    "export MRTS_NATIVE_NGINX_MODULE_FILE='" + str(self.module) + "'",
                    "export MRTS_NATIVE_NGINX_MODSECURITY_LIB_DIR='" + str(self.lib_dir) + "'",
                    "export NGINX_BUILD_DIR='" + str(self.nginx_build) + "'",
                    "export NGINX_PREFIX='" + str(self.build_root / "prefix") + "'",
                )
            )
            + "\n",
            encoding="utf-8",
        )
        self.snapshot.chmod(0o600)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def package_args(self) -> argparse.Namespace:
        return argparse.Namespace(
            expected_pr_head=SHA,
            trusted_dispatcher_base_sha=BASE,
            run_id="run-1",
            task_root=str(self.task_root),
            build_root=str(self.build_root),
            runtime_snapshot=str(self.snapshot),
            output_root=str(self.task_root / "artifacts"),
        )

    def test_packages_only_fixed_files_with_independent_digests(self) -> None:
        archive_digest = hashlib.sha256(self.archive.read_bytes()).hexdigest()
        with mock.patch.object(B, "EXPECTED_NGINX_SOURCE_SHA256", archive_digest):
            manifest_path = B.package(self.package_args())
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(payload["tested_pr_head"], SHA)
        self.assertEqual(payload["trusted_dispatcher_base_sha"], BASE)
        self.assertEqual(payload["nginx_source_digest"], archive_digest)
        self.assertEqual(set(payload["artifacts"]), {"nginx", "module", "library"})
        self.assertEqual(
            {child.name for child in manifest_path.parent.iterdir()},
            {"nginx", "ngx_http_modsecurity_module.so", "libmodsecurity.so.3", "artifact-manifest.json"},
        )
        for record in payload["artifacts"].values():
            copied = manifest_path.parent / record["filename"]
            self.assertEqual(record["sha256"], hashlib.sha256(copied.read_bytes()).hexdigest())
            self.assertEqual(copied.stat().st_nlink, 1)

    def test_rejects_source_archive_digest_mismatch(self) -> None:
        with self.assertRaisesRegex(B.BuilderError, "source archive digest"):
            B.package(self.package_args())

    def test_rejects_hardlink_and_symlink_candidate_artifacts(self) -> None:
        linked = self.build_root / "hard-linked-module.so"
        os.link(self.module, linked)
        text = self.snapshot.read_text(encoding="utf-8").replace(str(self.module), str(linked))
        self.snapshot.write_text(text, encoding="utf-8")
        archive_digest = hashlib.sha256(self.archive.read_bytes()).hexdigest()
        with mock.patch.object(B, "EXPECTED_NGINX_SOURCE_SHA256", archive_digest):
            with self.assertRaisesRegex(B.BuilderError, "single-link"):
                B.package(self.package_args())
        linked.unlink()
        self.snapshot.write_text(
            self.snapshot.read_text(encoding="utf-8").replace(str(linked), str(self.module)),
            encoding="utf-8",
        )
        self.snapshot.chmod(0o600)
        escaped = self.root / "escaped.so"
        escaped.write_bytes(b"escaped")
        self.module.unlink()
        self.module.symlink_to(escaped)
        arguments = self.package_args()
        arguments.output_root = str(self.task_root / "artifacts-second")
        with mock.patch.object(B, "EXPECTED_NGINX_SOURCE_SHA256", archive_digest):
            with self.assertRaisesRegex(B.BuilderError, "symbolic link"):
                B.package(arguments)

    def test_rejects_snapshot_path_escape_and_non_declarative_content(self) -> None:
        archive_digest = hashlib.sha256(self.archive.read_bytes()).hexdigest()
        self.snapshot.write_text("export MRTS_NATIVE_NGINX_BIN='$(id)'\n", encoding="utf-8")
        self.snapshot.chmod(0o600)
        with mock.patch.object(B, "EXPECTED_NGINX_SOURCE_SHA256", archive_digest):
            with self.assertRaises(B.BuilderError):
                B.package(self.package_args())
        self.snapshot.write_text(
            self.snapshot.read_text(encoding="utf-8") + "echo unsafe\n", encoding="utf-8"
        )
        with mock.patch.object(B, "EXPECTED_NGINX_SOURCE_SHA256", archive_digest):
            with self.assertRaises(B.BuilderError):
                B.package(self.package_args())

    def test_clean_build_environment_has_no_inherited_token_or_loader_input(self) -> None:
        arguments = argparse.Namespace(task_root=str(self.task_root), candidate_root=str(self.root / "candidate"))
        environment = B.build_environment(arguments)
        self.assertEqual(environment["PATH"], "/usr/bin:/bin")
        self.assertNotIn("GITHUB_TOKEN", environment)
        self.assertNotIn("LD_PRELOAD", environment)
        self.assertNotIn("PYTHONPATH", environment)
        self.assertEqual(environment["NGINX_RELEASE_TAG"], "release-1.31.4")

    def test_build_invokes_only_fixed_unprivileged_make_vector(self) -> None:
        candidate = self.root / "candidate"
        candidate.mkdir(mode=0o700)
        (candidate / "modules" / "ModSecurity-test-Framework").mkdir(parents=True, mode=0o700)
        arguments = argparse.Namespace(
            expected_pr_head=SHA,
            trusted_dispatcher_base_sha=BASE,
            run_id="run-1",
            task_root=str(self.task_root),
            candidate_root=str(candidate),
            output_root=str(self.task_root / "artifacts"),
        )
        reports = self.task_root / "runtime-component-reports"
        reports.mkdir(mode=0o700)
        snapshot = reports / "runtime-env-snapshot.one.sh"
        snapshot.write_text("export RUNTIME_COMPONENT_ENV_SNAPSHOT_TARGET='nginx'\n", encoding="utf-8")
        snapshot.chmod(0o600)
        with mock.patch.object(B.subprocess, "run") as run, mock.patch.object(B, "package", return_value=Path("/safe/artifact-manifest.json")) as package:
            output = B.run_candidate_build(arguments)
        self.assertEqual(output, Path("/safe/artifact-manifest.json"))
        command = run.call_args.args[0]
        self.assertEqual(command, ["/usr/bin/make", "-C", str(candidate), "fetch-deps"])
        self.assertNotIn("sudo", command)
        environment = run.call_args.kwargs["env"]
        self.assertEqual(environment["PATH"], "/usr/bin:/bin")
        self.assertNotIn("GITHUB_TOKEN", environment)
        package.assert_called_once()


if __name__ == "__main__":
    unittest.main()
