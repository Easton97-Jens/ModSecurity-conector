"""Regression tests for the static Framework-to-Parent pin synchronizer."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import py_compile
import re
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
assert SPEC is not None
assert SPEC.loader is not None
SYNC = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = SYNC
SPEC.loader.exec_module(SYNC)


CANDIDATE_GRAMMAR_PROVENANCE = "bd69ee96e0e7082317d4afe1232bee625665eb9a"

# This is an offline grammar fixture. The SHA identifies the reproduced
# Framework candidate's assignment structure only; it is never an input or
# allowlisted version value.
CURRENT_CANDIDATE_COMMON = """\
ENVOY_VERSION="1.39.0"
LIGHTTPD_SERIES="1.4"
LIGHTTPD_RELEASE_ROOT_URL="https://download.lighttpd.net/lighttpd"
LIGHTTPD_SERIES_BASE_URL="$LIGHTTPD_RELEASE_ROOT_URL/releases-$LIGHTTPD_SERIES.x"
LIGHTTPD_VERSION="1.4.85"
LIGHTTPD_SOURCE_URL="$LIGHTTPD_SERIES_BASE_URL/"
LIGHTTPD_ARCHIVE_NAME="lighttpd-$LIGHTTPD_VERSION.tar.xz"
LIGHTTPD_DOWNLOAD_URL="$LIGHTTPD_SOURCE_URL$LIGHTTPD_ARCHIVE_NAME"
LIGHTTPD_SHA256="18de51b393bac4a6827879e1a7ff377c169e414bae92cd245091d80fc2601d13"
HAPROXY_SERIES="3.2"
HAPROXY_RELEASE_ROOT_URL="https://www.haproxy.org/download"
HAPROXY_SERIES_BASE_URL="$HAPROXY_RELEASE_ROOT_URL/$HAPROXY_SERIES/src"
HAPROXY_VERSION="3.2.22"
HAPROXY_ARCHIVE_NAME="haproxy-$HAPROXY_VERSION.tar.gz"
HAPROXY_SOURCE_URL="$HAPROXY_SERIES_BASE_URL/$HAPROXY_ARCHIVE_NAME"
HAPROXY_SHA256="afca3a26d573df53d0e1fc475dcd743ec5875e038e1476c80e871d70228ca2da"
HAPROXY_HTX_SERIES="3.2"
HAPROXY_HTX_SERIES_BASE_URL="$HAPROXY_RELEASE_ROOT_URL/$HAPROXY_HTX_SERIES/src"
HAPROXY_HTX_VERSION="3.2.22"
HAPROXY_HTX_ARCHIVE_NAME="haproxy-$HAPROXY_HTX_VERSION.tar.gz"
HAPROXY_HTX_SOURCE_URL="$HAPROXY_HTX_SERIES_BASE_URL/$HAPROXY_HTX_ARCHIVE_NAME"
HAPROXY_HTX_SHA256="afca3a26d573df53d0e1fc475dcd743ec5875e038e1476c80e871d70228ca2da"
NGINX_SOURCE_MODE="github-release"
NGINX_SOURCE_REPO_URL="https://github.com/nginx/nginx"
NGINX_RELEASE_TAG="release-1.31.3"
NGINX_SOURCE_GIT_REF="$NGINX_RELEASE_TAG"
NGINX_RELEASE_ASSET_NAME="nginx-${NGINX_RELEASE_TAG#release-}.tar.gz"
NGINX_SHA256="a7657c50811c2d92d9895395e8b873ef60398142c4db21eb647811c38f6dd525"
NGINX_QUIC_TLS_LIBRARY="${NGINX_QUIC_TLS_LIBRARY:-openssl}"
NGINX_QUIC_TLS_VERSION="4.0.1"
NGINX_QUIC_TLS_ARCHIVE_NAME="openssl-$NGINX_QUIC_TLS_VERSION.tar.gz"
NGINX_QUIC_TLS_SOURCE_URL="https://github.com/openssl/openssl/releases/download/openssl-$NGINX_QUIC_TLS_VERSION/$NGINX_QUIC_TLS_ARCHIVE_NAME"
NGINX_QUIC_TLS_SOURCE_SHA256="2db3f3a0d6ea4b59e1f094ace2c8cd536dffb87cdc39084c5afa1e6f7f37dd09"
CRS_APPROVED_REPO_URL="https://github.com/coreruleset/coreruleset.git"
CRS_APPROVED_COMMIT="ab3ccd5fcd691424ba3f320d4040c61417270193"
CRS_RELEASE_TAG="v4.29.0"
"""


def replace_rhs(common: str, name: str, rhs: str) -> str:
    replacement = f"{name}={rhs}"
    updated, count = re.subn(
        rf"(?m)^{re.escape(name)}=.*$",
        lambda _match: replacement,
        common,
    )
    if count != 1:
        raise ValueError(f"missing or duplicate fixture assignment: {name}")
    return updated


def future_series_common() -> str:
    common = CURRENT_CANDIDATE_COMMON
    for name, rhs in (
        ("LIGHTTPD_SERIES", '"1.5"'),
        ("LIGHTTPD_VERSION", '"1.5.0"'),
        ("LIGHTTPD_SHA256", '"dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"'),
        ("HAPROXY_SERIES", '"3.3"'),
        ("HAPROXY_VERSION", '"3.3.1"'),
        ("HAPROXY_SHA256", '"cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"'),
        ("HAPROXY_HTX_VERSION", '"3.2.24"'),
        ("HAPROXY_HTX_SHA256", '"eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"'),
    ):
        common = replace_rhs(common, name, rhs)
    return common


class SyncFrameworkVersionsTests(unittest.TestCase):
    def setUp(self) -> None:
        runner_temp = os.environ.get("RUNNER_TEMP")
        temporary_root = runner_temp if runner_temp and Path(runner_temp).is_dir() else None
        self.temp = tempfile.TemporaryDirectory(dir=temporary_root)
        self.root = Path(self.temp.name) / "repo"
        shutil.copytree(
            ROOT,
            self.root,
            ignore=shutil.ignore_patterns(
                ".git", "ModSecurity-test-Framework", "__pycache__", ".pytest_cache"
            ),
        )
        self.common = Path(self.temp.name) / "framework/ci/lib/common.sh"
        self.common.parent.mkdir(parents=True)
        self.write_common(CURRENT_CANDIDATE_COMMON)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_common(self, contents: str) -> None:
        self.common.write_text(contents, encoding="utf-8")

    def target_bytes(self) -> dict[Path, bytes]:
        return {
            self.root / spec.relative_path: (self.root / spec.relative_path).read_bytes()
            for spec in SYNC.TARGET_REGISTRY
        }

    def test_current_candidate_grammar_fixture_resolves_as_data(self) -> None:
        values = SYNC.parse_common(self.common)
        self.assertEqual(
            CANDIDATE_GRAMMAR_PROVENANCE,
            "bd69ee96e0e7082317d4afe1232bee625665eb9a",
        )
        self.assertEqual(values["LIGHTTPD_SERIES"], "1.4")
        self.assertEqual(
            values["LIGHTTPD_SERIES_BASE_URL"],
            "https://download.lighttpd.net/lighttpd/releases-1.4.x",
        )
        self.assertEqual(
            values["LIGHTTPD_SOURCE_URL"],
            "https://download.lighttpd.net/lighttpd/releases-1.4.x/",
        )
        self.assertEqual(
            values["LIGHTTPD_DOWNLOAD_URL"],
            "https://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-1.4.85.tar.xz",
        )
        self.assertEqual(values["HAPROXY_SOURCE_URL"].split("/")[-2], "src")
        self.assertEqual(values["HAPROXY_HTX_VERSION"], "3.2.22")
        self.assertEqual(values["NGINX_SOURCE_GIT_REF"], "release-1.31.3")
        self.assertEqual(values["NGINX_RELEASE_ASSET_NAME"], "nginx-1.31.3.tar.gz")
        self.assertEqual(values["NGINX_QUIC_TLS_ARCHIVE_NAME"], "openssl-4.0.1.tar.gz")
        self.assertEqual(values["NGINX_QUIC_TLS_LIBRARY"], "openssl")

    def test_unconsumed_framework_pins_are_ignored_as_data(self) -> None:
        self.write_common(
            CURRENT_CANDIDATE_COMMON
            + 'GO_FTW_SERIES="9.9"\nGO_FTW_RELEASE_TAG="$GO_FTW_SERIES"\n'
        )
        values = SYNC.parse_common(self.common)
        self.assertNotIn("GO_FTW_SERIES", values)
        self.assertEqual(values["LIGHTTPD_VERSION"], "1.4.85")

    def test_braced_reference_and_static_self_default_do_not_read_environment(self) -> None:
        self.write_common(
            replace_rhs(
                CURRENT_CANDIDATE_COMMON,
                "NGINX_SOURCE_GIT_REF",
                '"${NGINX_RELEASE_TAG}"',
            )
        )
        with mock.patch.dict(os.environ, {"NGINX_QUIC_TLS_LIBRARY": "attacker"}):
            values = SYNC.parse_common(self.common)
        self.assertEqual(values["NGINX_SOURCE_GIT_REF"], "release-1.31.3")
        self.assertEqual(values["NGINX_QUIC_TLS_LIBRARY"], "openssl")

    def test_resolution_budget_rejects_fanout_before_semantic_validation(self) -> None:
        reference = "$LIGHTTPD_SERIES_BASE_URL"
        repetitions = SYNC.MAX_RESOLVED_VALUE_BYTES // len(
            "https://download.lighttpd.net/lighttpd/releases-1.4.x"
        ) + 1
        self.write_common(
            replace_rhs(
                CURRENT_CANDIDATE_COMMON,
                "LIGHTTPD_SOURCE_URL",
                '"' + reference * repetitions + '"',
            )
        )
        self.assertLess(
            len(self.common.read_bytes()), SYNC.MAX_COMMON_BYTES
        )
        with self.assertRaisesRegex(SYNC.SyncError, "byte budget"):
            SYNC.parse_common(self.common)

    def test_resolution_budget_allows_normal_candidate_values(self) -> None:
        values = SYNC.parse_common(self.common)
        self.assertLess(
            sum(len(value) for value in values.values()),
            SYNC.MAX_RESOLVED_TOTAL_BYTES,
        )
        self.assertLess(
            max(map(len, values.values())),
            SYNC.MAX_RESOLVED_VALUE_BYTES,
        )

    def test_positive_future_series_map_and_sync_separates_generic_and_htx(self) -> None:
        self.write_common(future_series_common())
        changed = SYNC.synchronize(self.root, self.common, True)
        self.assertTrue(
            {
                "ci/provisioning/components/prepare-runtime-components.py",
                "connectors/lighttpd/lighttpd-version.contract",
                "connectors/lighttpd/SOURCE_MAP.json",
                "connectors/haproxy/htx-overlay/version-contract.json",
            }.issubset(changed)
        )
        runtime = (self.root / "ci/provisioning/components/prepare-runtime-components.py").read_text()
        self.assertIn('DEFAULT_NGINX_QUIC_TLS_VERSION = "4.0.1"', runtime)
        self.assertIn('DEFAULT_HAPROXY_VERSION = "3.3.1"', runtime)
        contract = (self.root / "connectors/lighttpd/lighttpd-version.contract").read_text()
        self.assertIn("LIGHTTPD_SERIES=1.5", contract)
        self.assertIn("LIGHTTPD_VERSION=1.5.0", contract)
        self.assertIn(
            "LIGHTTPD_DOWNLOAD_URL=https://download.lighttpd.net/lighttpd/releases-1.5.x/lighttpd-1.5.0.tar.xz",
            contract,
        )
        source_map = json.loads((self.root / "connectors/lighttpd/SOURCE_MAP.json").read_text())
        self.assertEqual(source_map["upstream"]["series"], "1.5")
        self.assertEqual(
            source_map["upstream"]["download_url"],
            "https://download.lighttpd.net/lighttpd/releases-1.5.x/lighttpd-1.5.0.tar.xz",
        )
        htx = json.loads(
            (self.root / "connectors/haproxy/htx-overlay/version-contract.json").read_text()
        )
        self.assertEqual(htx["version"], "3.2.24")
        self.assertEqual(
            htx["source_url"],
            "https://www.haproxy.org/download/3.2/src/haproxy-3.2.24.tar.gz",
        )
        self.assertEqual(
            htx["sha256"],
            "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
        )
        self.assertNotEqual(htx["version"], "3.3.1")
        self.assertNotIn("$", contract)
        self.assertNotIn("$", json.dumps(source_map, sort_keys=True))
        self.assertNotIn("$", json.dumps(htx, sort_keys=True))
        for relative in (
            "ci/provisioning/components/prepare-runtime-components.py",
            "ci/runtime/broker/nginx_root_broker.py",
            "ci/runtime/broker/protected_nginx_broker_caller.py",
        ):
            py_compile.compile(str(self.root / relative), doraise=True)

    def test_cli_validate_sync_check_and_second_sync_are_byte_idempotent(self) -> None:
        self.assertEqual(
            SYNC.main(
                (
                    "--validate",
                    "--repo-root",
                    str(self.root),
                    "--framework-common",
                    str(self.common),
                )
            ),
            0,
        )
        self.write_common(future_series_common())
        sync_arguments = (
            "--sync",
            "--repo-root",
            str(self.root),
            "--framework-common",
            str(self.common),
        )
        self.assertEqual(SYNC.main(sync_arguments), 0)
        after_first_sync = self.target_bytes()
        self.assertEqual(
            SYNC.main(
                (
                    "--check",
                    "--repo-root",
                    str(self.root),
                    "--framework-common",
                    str(self.common),
                )
            ),
            0,
        )
        self.assertEqual(SYNC.main(sync_arguments), 0)
        self.assertEqual(after_first_sync, self.target_bytes())

    def test_noop_after_sync(self) -> None:
        self.write_common(future_series_common())
        SYNC.synchronize(self.root, self.common, True)
        self.assertEqual(SYNC.synchronize(self.root, self.common, False), [])

    def test_unsafe_or_unknown_known_expressions_fail_closed(self) -> None:
        cycle = replace_rhs(
            CURRENT_CANDIDATE_COMMON,
            "LIGHTTPD_SERIES_BASE_URL",
            '"$LIGHTTPD_SOURCE_URL"',
        )
        cases = {
            "unknown reference": replace_rhs(
                CURRENT_CANDIDATE_COMMON, "LIGHTTPD_SOURCE_URL", '"$UNKNOWN_SOURCE"'
            ),
            "missing required": re.sub(
                r"(?m)^HAPROXY_HTX_SHA256=.*\n", "", CURRENT_CANDIDATE_COMMON
            ),
            "duplicate": CURRENT_CANDIDATE_COMMON + 'ENVOY_VERSION="1.40.0"\n',
            "cycle": cycle,
            "command substitution": replace_rhs(
                CURRENT_CANDIDATE_COMMON, "LIGHTTPD_SOURCE_URL", '"$(id)"'
            ),
            "backticks": replace_rhs(
                CURRENT_CANDIDATE_COMMON, "LIGHTTPD_SOURCE_URL", '"`id`"'
            ),
            "semicolon": replace_rhs(
                CURRENT_CANDIDATE_COMMON, "LIGHTTPD_SOURCE_URL", '"value;id"'
            ),
            "pipe": replace_rhs(
                CURRENT_CANDIDATE_COMMON, "LIGHTTPD_SOURCE_URL", '"value|id"'
            ),
            "ampersand": replace_rhs(
                CURRENT_CANDIDATE_COMMON, "LIGHTTPD_SOURCE_URL", '"value&id"'
            ),
            "double pipe": replace_rhs(
                CURRENT_CANDIDATE_COMMON, "LIGHTTPD_SOURCE_URL", '"value||id"'
            ),
            "redirection": replace_rhs(
                CURRENT_CANDIDATE_COMMON, "LIGHTTPD_SOURCE_URL", '"value>file"'
            ),
            "input redirection": replace_rhs(
                CURRENT_CANDIDATE_COMMON, "LIGHTTPD_SOURCE_URL", '"value<file"'
            ),
            "here document": replace_rhs(
                CURRENT_CANDIDATE_COMMON, "LIGHTTPD_SOURCE_URL", '"value<<EOF"'
            ),
            "unsupported default": replace_rhs(
                CURRENT_CANDIDATE_COMMON,
                "NGINX_SOURCE_GIT_REF",
                '"${NGINX_RELEASE_TAG:-release-1.31.3}"',
            ),
            "unsupported dash default": replace_rhs(
                CURRENT_CANDIDATE_COMMON,
                "NGINX_SOURCE_GIT_REF",
                '"${NGINX_RELEASE_TAG-release-1.31.3}"',
            ),
            "suffix removal": replace_rhs(
                CURRENT_CANDIDATE_COMMON,
                "NGINX_SOURCE_GIT_REF",
                '"${NGINX_RELEASE_TAG%.*}"',
            ),
            "replacement": replace_rhs(
                CURRENT_CANDIDATE_COMMON,
                "NGINX_SOURCE_GIT_REF",
                '"${NGINX_RELEASE_TAG/release-/}"',
            ),
            "indirect": replace_rhs(
                CURRENT_CANDIDATE_COMMON,
                "NGINX_SOURCE_GIT_REF",
                '"${!NGINX_RELEASE_TAG}"',
            ),
            "arithmetic": replace_rhs(
                CURRENT_CANDIDATE_COMMON, "LIGHTTPD_SOURCE_URL", '"$((1 + 1))"'
            ),
            "process substitution": replace_rhs(
                CURRENT_CANDIDATE_COMMON, "LIGHTTPD_SOURCE_URL", '"<(id)"'
            ),
            "eval": replace_rhs(
                CURRENT_CANDIDATE_COMMON, "LIGHTTPD_SOURCE_URL", '"eval value"'
            ),
            "carriage return": replace_rhs(
                CURRENT_CANDIDATE_COMMON,
                "NGINX_SOURCE_GIT_REF",
                '"$NGINX_RELEASE_TAG"\r',
            ),
            "embedded newline": replace_rhs(
                CURRENT_CANDIDATE_COMMON,
                "NGINX_SOURCE_GIT_REF",
                '"release-\n1.31.3"',
            ),
            "indented known assignment": CURRENT_CANDIDATE_COMMON.replace(
                'ENVOY_VERSION="1.39.0"', '  ENVOY_VERSION="1.39.0"'
            ),
            "unsupported self default": replace_rhs(
                CURRENT_CANDIDATE_COMMON,
                "NGINX_QUIC_TLS_LIBRARY",
                '"${NGINX_QUIC_TLS_LIBRARY:-not-openssl}"',
            ),
        }
        for label, malformed in cases.items():
            with self.subTest(label=label):
                self.write_common(malformed)
                with self.assertRaises(SYNC.SyncError):
                    SYNC.parse_common(self.common)

    def test_semantic_tuple_controls_fail_closed(self) -> None:
        cases = {
            "manipulated root": replace_rhs(
                CURRENT_CANDIDATE_COMMON,
                "LIGHTTPD_RELEASE_ROOT_URL",
                '"https://evil.example/lighttpd"',
            ),
            "credentials": replace_rhs(
                CURRENT_CANDIDATE_COMMON,
                "LIGHTTPD_RELEASE_ROOT_URL",
                '"https://user@download.lighttpd.net/lighttpd"',
            ),
            "query": replace_rhs(
                CURRENT_CANDIDATE_COMMON,
                "LIGHTTPD_RELEASE_ROOT_URL",
                '"https://download.lighttpd.net/lighttpd?query=1"',
            ),
            "fragment": replace_rhs(
                CURRENT_CANDIDATE_COMMON,
                "LIGHTTPD_RELEASE_ROOT_URL",
                '"https://download.lighttpd.net/lighttpd#fragment"',
            ),
            "foreign source host": replace_rhs(
                CURRENT_CANDIDATE_COMMON,
                "LIGHTTPD_SOURCE_URL",
                '"https://example.org/lighttpd/releases-1.4.x/"',
            ),
            "double source slash": replace_rhs(
                CURRENT_CANDIDATE_COMMON,
                "LIGHTTPD_SOURCE_URL",
                '"https://download.lighttpd.net/lighttpd/releases-1.4.x//"',
            ),
            "series version mismatch": replace_rhs(
                CURRENT_CANDIDATE_COMMON, "LIGHTTPD_SERIES", '"1.5"'
            ),
            "wrong archive": replace_rhs(
                CURRENT_CANDIDATE_COMMON, "LIGHTTPD_ARCHIVE_NAME", '"lighttpd-1.4.84.tar.xz"'
            ),
            "wrong download": replace_rhs(
                CURRENT_CANDIDATE_COMMON,
                "LIGHTTPD_DOWNLOAD_URL",
                '"https://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-1.4.85.zip"',
            ),
            "nginx ref mismatch": replace_rhs(
                CURRENT_CANDIDATE_COMMON,
                "NGINX_SOURCE_GIT_REF",
                '"release-1.31.4"',
            ),
            "nginx asset mismatch": replace_rhs(
                CURRENT_CANDIDATE_COMMON,
                "NGINX_RELEASE_ASSET_NAME",
                '"nginx-1.31.4.tar.gz"',
            ),
            "openssl archive mismatch": replace_rhs(
                CURRENT_CANDIDATE_COMMON,
                "NGINX_QUIC_TLS_ARCHIVE_NAME",
                '"openssl-4.0.0.tar.gz"',
            ),
            "openssl URL mismatch": replace_rhs(
                CURRENT_CANDIDATE_COMMON,
                "NGINX_QUIC_TLS_SOURCE_URL",
                '"https://github.com/openssl/openssl/releases/download/openssl-4.0.1/openssl-4.0.0.tar.gz"',
            ),
            "generic haproxy mismatch": replace_rhs(
                CURRENT_CANDIDATE_COMMON, "HAPROXY_SERIES", '"3.3"'
            ),
            "htx haproxy mismatch": replace_rhs(
                CURRENT_CANDIDATE_COMMON, "HAPROXY_HTX_SERIES", '"3.3"'
            ),
            "invalid sha": replace_rhs(
                CURRENT_CANDIDATE_COMMON,
                "LIGHTTPD_SHA256",
                '"zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"',
            ),
            "non-ascii digits": replace_rhs(
                CURRENT_CANDIDATE_COMMON, "LIGHTTPD_VERSION", '"١.4.85"'
            ),
        }
        for label, malformed in cases.items():
            with self.subTest(label=label):
                self.write_common(malformed)
                with self.assertRaises(SYNC.SyncError):
                    SYNC.parse_common(self.common)

    def test_parse_or_validation_failure_never_writes_targets(self) -> None:
        before = self.target_bytes()
        self.write_common(
            replace_rhs(
                CURRENT_CANDIDATE_COMMON,
                "LIGHTTPD_RELEASE_ROOT_URL",
                '"https://evil.example/lighttpd"',
            )
        )
        with self.assertRaises(SYNC.SyncError):
            SYNC.synchronize(self.root, self.common, True)
        self.assertEqual(before, self.target_bytes())

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

    def test_candidate_outside_explicit_allowed_root_is_rejected(self) -> None:
        outside = Path(self.temp.name) / "outside-common.sh"
        outside.write_text(CURRENT_CANDIDATE_COMMON, encoding="utf-8")
        with self.assertRaises(SYNC.SyncError):
            SYNC._read_regular(
                outside,
                "candidate common.sh",
                allowed_root=self.root,
            )

    def test_framework_candidate_must_be_below_runner_temp_root(self) -> None:
        with mock.patch.dict(os.environ, {"RUNNER_TEMP": str(self.root)}):
            with self.assertRaises(SYNC.SyncError):
                SYNC.parse_common(self.common)

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
        self.write_common(future_series_common())
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
