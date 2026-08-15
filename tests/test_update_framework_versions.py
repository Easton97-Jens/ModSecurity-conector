"""Regression tests for the static Framework-to-Parent pin synchronizer."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import py_compile
import shutil
import stat
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "sync_framework", ROOT / "ci/tools/sync-framework-component-versions.py"
)
assert SPEC and SPEC.loader
SYNC = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = SYNC
SPEC.loader.exec_module(SYNC)


COMMON = """
ENVOY_VERSION="${ENVOY_VERSION:-1.40.0}"
LIGHTTPD_VERSION="${LIGHTTPD_VERSION:-1.4.86}"
LIGHTTPD_SOURCE_URL="${LIGHTTPD_SOURCE_URL:-https://download.lighttpd.net/lighttpd/releases-1.4.x/}"
LIGHTTPD_DOWNLOAD_URL="${LIGHTTPD_DOWNLOAD_URL:-https://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-$LIGHTTPD_VERSION.tar.xz}"
LIGHTTPD_SHA256="${LIGHTTPD_SHA256:-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb}"
HAPROXY_VERSION="${HAPROXY_VERSION:-3.2.23}"
HAPROXY_SOURCE_URL="${HAPROXY_SOURCE_URL:-https://www.haproxy.org/download/3.2/src/haproxy-$HAPROXY_VERSION.tar.gz}"
HAPROXY_SHA256="${HAPROXY_SHA256:-cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc}"
NGINX_QUIC_TLS_LIBRARY="${NGINX_QUIC_TLS_LIBRARY:-openssl}"
NGINX_QUIC_TLS_VERSION="${NGINX_QUIC_TLS_VERSION:-4.0.1}"
NGINX_QUIC_TLS_SOURCE_URL="${NGINX_QUIC_TLS_SOURCE_URL:-https://github.com/openssl/openssl/releases/download/openssl-$NGINX_QUIC_TLS_VERSION/openssl-$NGINX_QUIC_TLS_VERSION.tar.gz}"
NGINX_QUIC_TLS_SOURCE_SHA256="${NGINX_QUIC_TLS_SOURCE_SHA256:-2db3f3a0d6ea4b59e1f094ace2c8cd536dffb87cdc39084c5afa1e6f7f37dd09}"
NGINX_SOURCE_MODE="${NGINX_SOURCE_MODE-github-release}"
NGINX_SOURCE_REPO_URL="${NGINX_SOURCE_REPO_URL-${NGINX_GITHUB_REPO-https://github.com/nginx/nginx}}"
NGINX_RELEASE_TAG="${NGINX_RELEASE_TAG-release-1.32.0}"
NGINX_SOURCE_GIT_REF="${NGINX_SOURCE_GIT_REF-$NGINX_RELEASE_TAG}"
NGINX_RELEASE_ASSET_NAME="${NGINX_RELEASE_ASSET_NAME-nginx-${NGINX_RELEASE_TAG#release-}.tar.gz}"
NGINX_SHA256="${NGINX_SHA256-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa}"
CRS_APPROVED_REPO_URL="https://github.com/coreruleset/coreruleset.git"
CRS_APPROVED_COMMIT="1111111111111111111111111111111111111111"
CRS_RELEASE_TAG="v4.29.0"
"""


class SyncFrameworkVersionsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "repo"
        shutil.copytree(ROOT, self.root)
        self.common = Path(self.temp.name) / "framework/ci/lib/common.sh"
        self.common.parent.mkdir(parents=True)
        self.common.write_text(COMMON, encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def target_bytes(self) -> dict[Path, bytes]:
        return {
            self.root / spec.relative_path: (self.root / spec.relative_path).read_bytes()
            for spec in SYNC.TARGET_REGISTRY
        }

    def test_positive_map_and_sync(self) -> None:
        changed = SYNC.synchronize(self.root, self.common, True)
        self.assertEqual(
            set(changed),
            {
                "connectors/envoy/config/envoy-ext-proc-versions.env",
                "ci/provisioning/components/prepare-runtime-components.py",
                "ci/runtime/broker/nginx_root_broker.py",
                "ci/runtime/broker/protected_nginx_broker_caller.py",
                "connectors/lighttpd/lighttpd-version.contract",
                "connectors/lighttpd/SOURCE_MAP.json",
                "connectors/haproxy/htx-overlay/version-contract.json",
                "ci/checks/evidence/check-runtime-producer-readiness.py",
                ".github/workflows/test-full-smoke-sequential.yml",
                ".github/workflows/nginx-root-broker.yml",
            },
        )
        self.assertIn(
            "ENVOY_RELEASE=1.40.0",
            (self.root / "connectors/envoy/config/envoy-ext-proc-versions.env").read_text(),
        )
        runtime = (self.root / "ci/provisioning/components/prepare-runtime-components.py").read_text()
        self.assertIn('DEFAULT_NGINX_QUIC_TLS_VERSION = "4.0.1"', runtime)
        self.assertIn('NGINX_PINNED_SOURCE_REF = "release-1.32.0"', runtime)
        self.assertIn('DEFAULT_HAPROXY_VERSION = "3.2.23"', runtime)
        readiness = (self.root / "ci/checks/evidence/check-runtime-producer-readiness.py").read_text()
        self.assertIn('CANONICAL_NGINX_RELEASE_TAG = "release-1.32.0"', readiness)
        self.assertIn('CANONICAL_NGINX_VERSION_READBACK = "nginx/1.32.0"', readiness)
        self.assertIn(
            'CRS_APPROVED_COMMIT = "1111111111111111111111111111111111111111"',
            (self.root / "ci/runtime/broker/nginx_root_broker.py").read_text(),
        )
        self.assertIn(
            'NGINX_PINNED_VERSION = "1.32.0"',
            (self.root / "ci/runtime/broker/protected_nginx_broker_caller.py").read_text(),
        )
        self.assertIn(
            "LIGHTTPD_VERSION=1.4.86",
            (self.root / "connectors/lighttpd/lighttpd-version.contract").read_text(),
        )
        self.assertIn(
            "LIGHTTPD_SHA256=bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
            (self.root / "connectors/lighttpd/lighttpd-version.contract").read_text(),
        )
        source_map = (self.root / "connectors/lighttpd/SOURCE_MAP.json").read_text()
        self.assertIn('"version": "1.4.86"', source_map)
        self.assertIn(
            '"download_url": "https://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-1.4.86.tar.xz"',
            source_map,
        )
        self.assertIn(
            '"version": "3.2.23"',
            (self.root / "connectors/haproxy/htx-overlay/version-contract.json").read_text(),
        )
        self.assertIn(
            '"sha256": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"',
            (self.root / "connectors/haproxy/htx-overlay/version-contract.json").read_text(),
        )
        for relative in (
            ".github/workflows/test-full-smoke-sequential.yml",
            ".github/workflows/nginx-root-broker.yml",
        ):
            workflow = (self.root / relative).read_text()
            self.assertIn("NGINX_RELEASE_TAG: release-1.32.0", workflow)
            self.assertIn("NGINX_RELEASE_ASSET_NAME: nginx-1.32.0.tar.gz", workflow)
        for relative in (
            "ci/provisioning/components/prepare-runtime-components.py",
            "ci/runtime/broker/nginx_root_broker.py",
            "ci/runtime/broker/protected_nginx_broker_caller.py",
        ):
            py_compile.compile(str(self.root / relative), doraise=True)

    def test_noop_after_sync(self) -> None:
        SYNC.synchronize(self.root, self.common, True)
        self.assertEqual(SYNC.synchronize(self.root, self.common, False), [])

    def test_malicious_shell_is_rejected_without_writes(self) -> None:
        before = self.target_bytes()
        self.common.write_text(
            COMMON.replace("1.40.0", "1.40.0; touch /tmp/pwned"), encoding="utf-8"
        )
        with self.assertRaises(SYNC.SyncError):
            SYNC.synchronize(self.root, self.common, True)
        self.assertEqual(before, self.target_bytes())

    def test_invalid_source_ref_or_duplicate_is_rejected(self) -> None:
        self.common.write_text(
            COMMON.replace("${NGINX_SOURCE_GIT_REF-$NGINX_RELEASE_TAG}", "release-1.32.1"),
            encoding="utf-8",
        )
        with self.assertRaises(SYNC.SyncError):
            SYNC.parse_common(self.common)
        self.common.write_text(COMMON + "ENVOY_VERSION=1.41.0\n", encoding="utf-8")
        with self.assertRaises(SYNC.SyncError):
            SYNC.parse_common(self.common)

    def test_missing_target_is_rejected_atomically(self) -> None:
        target = self.root / "ci/runtime/broker/nginx_root_broker.py"
        target.write_text(
            target.read_text().replace("CRS_APPROVED_COMMIT =", "CRS_APPROVED_COMMIT_REMOVED =", 1),
            encoding="utf-8",
        )
        before = self.target_bytes()
        with self.assertRaises(SYNC.SyncError):
            SYNC.synchronize(self.root, self.common, True)
        self.assertEqual(before, self.target_bytes())

    def test_symlinked_candidate_or_target_is_rejected_without_writes(self) -> None:
        before = self.target_bytes()
        candidate_link = Path(self.temp.name) / "candidate-link.sh"
        candidate_link.symlink_to(self.common)
        self.assertEqual(
            SYNC.main(
                ("--validate", "--repo-root", str(self.root), "--framework-common", str(candidate_link))
            ),
            2,
        )
        target = self.root / "connectors/envoy/config/envoy-ext-proc-versions.env"
        outside = Path(self.temp.name) / "outside.env"
        outside.write_bytes(b"ENVOY_RELEASE=outside\n")
        target.unlink()
        target.symlink_to(outside)
        with self.assertRaises(SYNC.SyncError):
            SYNC.synchronize(self.root, self.common, True)
        self.assertEqual(outside.read_bytes(), b"ENVOY_RELEASE=outside\n")
        for path, contents in before.items():
            if path != target:
                self.assertEqual(path.read_bytes(), contents)

    def test_special_target_and_symlinked_parent_are_rejected(self) -> None:
        target = self.root / "connectors/envoy/config/envoy-ext-proc-versions.env"
        target.unlink()
        os.mkfifo(target)
        with self.assertRaises(SYNC.SyncError):
            SYNC.synchronize(self.root, self.common, True)
        target.unlink()

        directory = self.root / "connectors/lighttpd"
        moved = self.root / "connectors/lighttpd-original"
        directory.rename(moved)
        directory.symlink_to(moved, target_is_directory=True)
        with self.assertRaises(SYNC.SyncError):
            SYNC.synchronize(self.root, self.common, True)

    def test_replacement_failure_rolls_back_and_preserves_modes(self) -> None:
        target = self.root / "connectors/envoy/config/envoy-ext-proc-versions.env"
        target.chmod(0o755)
        before = self.target_bytes()
        original_replace = SYNC._replace_file
        calls = 0

        def fail_second(*args: object) -> None:
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("injected replacement failure")
            original_replace(*args)  # type: ignore[arg-type]

        with mock.patch.object(SYNC, "_replace_file", side_effect=fail_second):
            with self.assertRaises(SYNC.SyncError):
                SYNC.synchronize(self.root, self.common, True)
        self.assertEqual(before, self.target_bytes())
        self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o755)
        self.assertEqual(list(target.parent.glob(f".{target.name}.*")), [])


if __name__ == "__main__":
    unittest.main()
