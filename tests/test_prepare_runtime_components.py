from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from tests.framework_test_trust import trusted_framework_root


ROOT = Path(__file__).resolve().parents[1]
LEGACY_FRAMEWORK_HAPROXY_CACHE_SHA = "784977615acfc55567e37b863309abc4a38ac877"
PINNED_EXPAT_COMMIT = "c61098da494eea1cbd091118118dcee417faacea"
PINNED_NGINX_RELEASE_TUPLE = {
    "NGINX_SOURCE_MODE": "github-release",
    "NGINX_SOURCE_REPO_URL": "https://github.com/nginx/nginx",
    "NGINX_RELEASE_TAG": "release-1.31.3",
    "NGINX_SOURCE_GIT_REF": "release-1.31.3",
    "NGINX_RELEASE_ASSET_NAME": "nginx-1.31.3.tar.gz",
    "NGINX_SHA256": "a7657c50811c2d92d9895395e8b873ef60398142c4db21eb647811c38f6dd525",
}
PINNED_NGINX_RELEASE_ASSET_URL = (
    "https://github.com/nginx/nginx/releases/download/release-1.31.3/nginx-1.31.3.tar.gz"
)
TEST_HAPROXY_LOCKED_VERSION = "3.2.22"
TEST_HAPROXY_LOCKED_SOURCE_URL = "https://www.haproxy.org/download/3.2/src/haproxy-3.2.22.tar.gz"
TEST_HAPROXY_LOCKED_SHA256 = "afca3a26d573df53d0e1fc475dcd743ec5875e038e1476c80e871d70228ca2da"
TEST_HAPROXY_UNAPPROVED_FUTURE_VERSION = "3.2.9001"
TEST_HAPROXY_UNAPPROVED_FUTURE_SOURCE_URL = (
    "https://www.haproxy.org/download/3.2/src/haproxy-3.2.9001.tar.gz"
)
TEST_HAPROXY_UNAPPROVED_FUTURE_SHA256 = "b" * 64
_MISSING_MODULE = object()


def load_parent_prepare_runtime_components():
    """Load the Parent subject without retaining its generic helper module.

    The pinned Framework has an independent ``generated_report_utils`` module.
    Tests must bind the Parent implementation while this module is executing,
    then restore any pre-existing generic import for the surrounding test
    process.
    """

    previous_path = list(sys.path)
    previous_generated_report_utils = sys.modules.pop("generated_report_utils", _MISSING_MODULE)
    spec = importlib.util.spec_from_file_location(
        "parent_prepare_runtime_components_for_tests",
        ROOT / "ci/provisioning/components/prepare-runtime-components.py",
    )
    if spec is None or spec.loader is None:
        raise ImportError("unable to load prepare-runtime-components test module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        sys.path.insert(0, str(ROOT / "ci" / "lib"))
        sys.path.insert(0, str(ROOT / "ci" / "provisioning" / "components"))
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(spec.name, None)
        raise
    finally:
        sys.path[:] = previous_path
        sys.modules.pop("generated_report_utils", None)
        if previous_generated_report_utils is not _MISSING_MODULE:
            sys.modules["generated_report_utils"] = previous_generated_report_utils
    return module


components = load_parent_prepare_runtime_components()


class PrepareRuntimeComponentsTest(unittest.TestCase):
    def test_nginx_common_source_staging_includes_required_private_header(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root = Path(temporary) / "connector"
            common_source_root = connector_root / "common" / "src"
            common_source_root.mkdir(parents=True)
            (common_source_root / "request_helpers.c").write_text(
                '#include "header_validation_internal.h"\n',
                encoding="utf-8",
            )
            (common_source_root / "header_validation_internal.h").write_text(
                "#pragma once\n",
                encoding="utf-8",
            )
            (common_source_root / "not-a-build-input.txt").write_text(
                "must not be staged\n",
                encoding="utf-8",
            )

            staged = components.copy_nginx_common_sources(
                connector_root,
                {"root": str(Path(temporary) / "build")},
            )

            self.assertEqual(
                (staged / "request_helpers.c").read_text(encoding="utf-8"),
                '#include "header_validation_internal.h"\n',
            )
            self.assertEqual(
                (staged / "header_validation_internal.h").read_text(encoding="utf-8"),
                "#pragma once\n",
            )
            self.assertFalse((staged / "not-a-build-input.txt").exists())

    def test_require_staging_path_rejects_absence_and_preserves_path(self) -> None:
        staging_path = Path("staging")

        self.assertEqual(staging_path, components.require_staging_path(staging_path))
        with self.assertRaisesRegex(RuntimeError, "staging cache entry is required"):
            components.require_staging_path(None)

    def test_require_full_immutable_git_commit_accepts_only_full_commit_ids(self) -> None:
        self.assertEqual(
            components.require_full_immutable_git_commit(PINNED_EXPAT_COMMIT, "EXPAT_GIT_REF"),
            PINNED_EXPAT_COMMIT,
        )
        for mutable_or_abbreviated_ref in ("master", "R_2_8_2", "refs/tags/R_2_8_2", "c61098d"):
            with self.subTest(ref=mutable_or_abbreviated_ref):
                with self.assertRaisesRegex(RuntimeError, "full immutable Git commit ID"):
                    components.require_full_immutable_git_commit(
                        mutable_or_abbreviated_ref,
                        "EXPAT_GIT_REF",
                    )

    def test_github_repo_url_config_preserves_canonical_and_rejection_policy(self) -> None:
        github = "https://github.com"
        repo = "owner/repo"
        canonical = f"{github}/{repo}"

        self.assertEqual(
            components.require_https_github_repo_url(f" {canonical}.git "),
            canonical,
        )
        components.validate_https_url_config({"CRS_REPO_URL": canonical})

        for invalid_url in (
            f"http://github.com/{repo}",
            f"https://example.invalid/{repo}",
            f"{github}:443/{repo}",
            f"{canonical}?ref=main",
            f"{canonical}#release",
            f"{github}/owner",
            f"{canonical}/extra",
        ):
            with self.subTest(url=invalid_url):
                with self.assertRaises(RuntimeError):
                    components.validate_https_url_config({"CRS_REPO_URL": invalid_url})

        unused_nginx_urls = {
            "CRS_REPO_URL": canonical,
            "NGINX_SOURCE_REPO_URL": f"http://github.com/{repo}",
            "NGINX_QUIC_TLS_SOURCE_URL": "http://example.invalid/quic.tar.gz",
        }
        for target in ("shared", "apache", "haproxy"):
            with self.subTest(target=target):
                components.validate_https_url_config(unused_nginx_urls, target)
        for target in ("all", "nginx"):
            with self.subTest(nginx_target=target):
                with self.assertRaises(RuntimeError):
                    components.validate_https_url_config(unused_nginx_urls, target)

    def test_required_runtime_component_sources_scope_all_and_nginx_only_inputs(self) -> None:
        """Unrelated NGINX and optional-tool pins cannot block selected hosts."""

        non_nginx_env = {
            "EXPAT_SOURCE_URL": "https://github.com/libexpat/libexpat",
            "EXPAT_GIT_REF": PINNED_EXPAT_COMMIT,
            **PINNED_NGINX_RELEASE_TUPLE,
            "NGINX_RELEASE_TAG": "release-1.31.4",
            "NGINX_SOURCE_GIT_REF": "release-1.31.4",
        }
        all_env = {
            **non_nginx_env,
            "GO_FTW_SOURCE_URL": "https://github.com/example/go-ftw",
            "GO_FTW_PROMPT_EXPECTED_LATEST": "v1.0.0",
            "ALBEDO_SOURCE_URL": "https://github.com/example/albedo",
            "ALBEDO_PROMPT_EXPECTED_LATEST": "v1.0.0",
        }

        with (
            mock.patch.object(components, "validate_https_url_config"),
            mock.patch.object(components, "require_apr_util_pinned_provenance", return_value={}),
        ):
            for target_connector in ("shared", "apache", "haproxy"):
                with self.subTest(target_connector=target_connector):
                    values = components.required_runtime_component_sources(
                        non_nginx_env,
                        strict=False,
                        target_connector=target_connector,
                    )
                    self.assertEqual(values["expat_git_ref"], PINNED_EXPAT_COMMIT)
                    self.assertNotIn("nginx_pinned_provenance", values)
                    self.assertNotIn("go_ftw_source_url", values)
                    self.assertNotIn("albedo_source_url", values)

            with self.assertRaisesRegex(RuntimeError, "nginx_pinned_provenance_ref_mismatch"):
                components.required_runtime_component_sources(
                    non_nginx_env,
                    strict=False,
                    target_connector="nginx",
                )
            with self.assertRaisesRegex(RuntimeError, "nginx_pinned_provenance_ref_mismatch"):
                components.required_runtime_component_sources(
                    all_env,
                    strict=False,
                    target_connector="all",
                )

        with (
            mock.patch.object(components, "validate_https_url_config"),
            mock.patch.object(components, "require_apr_util_pinned_provenance", return_value={}),
        ):
            with self.assertRaisesRegex(
                RuntimeError,
                "missing required runtime component config: GO_FTW_SOURCE_URL",
            ):
                components.required_runtime_component_sources(
                    {
                        "EXPAT_SOURCE_URL": "https://github.com/libexpat/libexpat",
                        "EXPAT_GIT_REF": PINNED_EXPAT_COMMIT,
                    },
                    strict=False,
                    target_connector="all",
                )

    def test_required_runtime_component_sources_keeps_global_url_guard_for_every_target(self) -> None:
        """Target scoping never bypasses the common source URL trust boundary."""

        for target_connector in ("shared", "apache", "haproxy", "nginx", "all"):
            with self.subTest(target_connector=target_connector):
                with mock.patch.object(
                    components,
                    "validate_https_url_config",
                    side_effect=RuntimeError("invalid_runtime_source_url"),
                ):
                    with self.assertRaisesRegex(RuntimeError, "invalid_runtime_source_url"):
                        components.required_runtime_component_sources(
                            {},
                            strict=False,
                            target_connector=target_connector,
                        )

    def test_pinned_nginx_release_tuple_uses_only_the_direct_release_asset(self) -> None:
        archive_root = Path("cache/archives")
        cache_root = Path("cache")
        prepared = {
            "name": "nginx",
            "url": PINNED_NGINX_RELEASE_ASSET_URL,
            "expected_sha256": PINNED_NGINX_RELEASE_TUPLE["NGINX_SHA256"],
            "status": "present",
            "checksum_status": "PASS",
        }
        with (
            mock.patch.object(components, "urlopen_bytes") as network,
            mock.patch.object(components, "prepare_archive", return_value=prepared) as prepare_archive,
        ):
            records = components.nginx_archive_records(
                dict(PINNED_NGINX_RELEASE_TUPLE),
                archive_root,
                cache_root,
            )

        network.assert_not_called()
        prepare_archive.assert_called_once()
        args, _kwargs = prepare_archive.call_args
        self.assertEqual(args[0], "nginx")
        self.assertEqual(args[1], PINNED_NGINX_RELEASE_ASSET_URL)
        self.assertEqual(args[2], PINNED_NGINX_RELEASE_TUPLE["NGINX_SHA256"])
        self.assertNotIn("/releases/latest", args[1])
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["status"], "present")
        self.assertEqual(records[0]["url"], PINNED_NGINX_RELEASE_ASSET_URL)
        self.assertEqual(records[0]["release_tag"], "release-1.31.3")
        self.assertEqual(records[0]["source_ref"], "release-1.31.3")
        self.assertEqual(records[0]["release_asset_name"], "nginx-1.31.3.tar.gz")
        self.assertEqual(
            records[0]["expected_sha256"],
            PINNED_NGINX_RELEASE_TUPLE["NGINX_SHA256"],
        )

    def test_nginx_archive_records_reject_invalid_provenance_before_side_effects(self) -> None:
        invalid_cases: dict[str, dict[str, str]] = {
            "source_mode": {"NGINX_SOURCE_MODE": "git"},
            "missing_release_tag": {"NGINX_RELEASE_TAG": ""},
            "missing_source_ref": {"NGINX_SOURCE_GIT_REF": ""},
            "tag_latest": {"NGINX_RELEASE_TAG": "latest"},
            "ref_latest": {"NGINX_SOURCE_GIT_REF": "latest"},
            "missing_sha256": {"NGINX_SHA256": ""},
            "empty_sha256": {"NGINX_SHA256": ""},
            "whitespace_sha256": {"NGINX_SHA256": "   "},
            "malformed_sha256": {"NGINX_SHA256": "not-a-sha256"},
            "tag_ref_mismatch": {"NGINX_SOURCE_GIT_REF": "release-1.31.2"},
            "asset_mismatch": {"NGINX_RELEASE_ASSET_NAME": "nginx-1.31.2.tar.gz"},
            "wrong_repo": {"NGINX_SOURCE_REPO_URL": "https://github.com/example/nginx"},
            "github_repo_alias_mismatch": {"NGINX_GITHUB_REPO": "https://github.com/example/nginx"},
        }

        for name, overrides in invalid_cases.items():
            with self.subTest(case=name):
                env = dict(PINNED_NGINX_RELEASE_TUPLE)
                env.update(overrides)
                if name == "missing_release_tag":
                    env.pop("NGINX_RELEASE_TAG")
                if name == "missing_source_ref":
                    env.pop("NGINX_SOURCE_GIT_REF")
                if name == "missing_sha256":
                    env.pop("NGINX_SHA256")
                with (
                    mock.patch.object(components, "urlopen_bytes") as network,
                    mock.patch.object(components, "download") as download,
                    mock.patch.object(components, "prepare_archive") as prepare_archive,
                    mock.patch.object(components, "mark_managed_cache_entry") as mark_cache,
                    mock.patch.object(
                        components, "write_cache_entry_completion"
                    ) as complete_cache,
                    mock.patch.object(components, "archive_can_list") as inspect_archive,
                ):
                    records = components.nginx_archive_records(
                        env,
                        Path("cache/archives"),
                        Path("cache"),
                    )

                self.assertEqual(len(records), 1)
                self.assertEqual(records[0]["status"], "blocked")
                self.assertTrue(records[0]["blocker_reason"])
                network.assert_not_called()
                download.assert_not_called()
                prepare_archive.assert_not_called()
                mark_cache.assert_not_called()
                complete_cache.assert_not_called()
                inspect_archive.assert_not_called()

    def test_required_runtime_component_sources_scopes_nginx_preflight_to_nginx_targets(
        self,
    ) -> None:
        mismatched_nginx = dict(PINNED_NGINX_RELEASE_TUPLE)
        mismatched_nginx.update(
            {
                "NGINX_RELEASE_TAG": "release-1.31.4",
                "NGINX_SOURCE_GIT_REF": "release-1.31.4",
            }
        )
        with self.assertRaisesRegex(RuntimeError, "unsupported_runtime_component_target:unknown"):
            components.required_runtime_component_sources(
                {},
                strict=False,
                target_connector="unknown",
            )
        for target in ("shared", "apache", "haproxy"):
            with self.subTest(target=target):
                with (
                    mock.patch.object(components, "validate_https_url_config"),
                    mock.patch.object(
                        components,
                        "require_apr_util_pinned_provenance",
                        return_value={"component": "apr-util"},
                    ),
                    mock.patch.object(components, "require_env_value", return_value="required-source"),
                    mock.patch.object(
                        components,
                        "nginx_protocol_build_inputs",
                        side_effect=AssertionError(
                            "non-NGINX target must not read NGINX protocol inputs"
                        ),
                    ) as nginx_protocol,
                ):
                    values = components.required_runtime_component_sources(
                        mismatched_nginx,
                        strict=False,
                        target_connector=target,
                    )

            self.assertNotIn("nginx_pinned_provenance", values)
            self.assertNotIn("nginx_require_pinned_provenance", values)
            nginx_protocol.assert_not_called()

        for target in ("all", "nginx"):
            with self.subTest(target=target):
                with (
                    mock.patch.object(components, "validate_https_url_config"),
                    mock.patch.object(
                        components,
                        "require_apr_util_pinned_provenance",
                        return_value={"component": "apr-util"},
                    ),
                    mock.patch.object(components, "require_env_value", return_value="required-source"),
                    mock.patch.object(components, "nginx_protocol_build_inputs") as nginx_protocol,
                ):
                    with self.assertRaisesRegex(RuntimeError, "nginx_pinned_provenance_ref_mismatch"):
                        components.required_runtime_component_sources(
                            mismatched_nginx,
                            strict=False,
                            target_connector=target,
                        )

            nginx_protocol.assert_not_called()

        for target in ("all", "nginx"):
            with self.subTest(protocol_target=target):
                with (
                    mock.patch.object(components, "validate_https_url_config"),
                    mock.patch.object(
                        components,
                        "require_apr_util_pinned_provenance",
                        return_value={"component": "apr-util"},
                    ),
                    mock.patch.object(components, "require_env_value", return_value="required-source"),
                    mock.patch.object(
                        components,
                        "nginx_protocol_build_inputs",
                        side_effect=RuntimeError("nginx_protocol_validation"),
                    ),
                ):
                    with self.assertRaisesRegex(RuntimeError, "nginx_protocol_validation"):
                        components.required_runtime_component_sources(
                            dict(PINNED_NGINX_RELEASE_TUPLE),
                            strict=False,
                            target_connector=target,
                        )

    def test_prepare_native_component_records_builds_nginx_plan_only_for_nginx_target(
        self,
    ) -> None:
        paths = {
            "sources_root": Path("cache/sources"),
            "archives_root": Path("cache/archives"),
        }
        for target, expects_nginx_plan in (
            ("shared", False),
            ("apache", False),
            ("haproxy", False),
            ("all", True),
            ("nginx", True),
        ):
            context = {
                "env": {},
                "cache_root": Path("cache"),
                "build_root": Path("build"),
                "connector_root": ROOT,
                "framework_root": ROOT,
                "target_connector": target,
            }
            with self.subTest(target=target):
                with (
                    mock.patch.object(components, "prepare_expat", return_value={"status": "present"}),
                    mock.patch.object(
                        components,
                        "prepare_shared_modsecurity",
                        return_value={"status": "present", "build_id": "modsecurity"},
                    ),
                    mock.patch.object(
                        components,
                        "connector_plan",
                        side_effect=lambda *args: {"connector": args[4]},
                    ) as connector_plan,
                    mock.patch.object(
                        components, "prepare_apache_httpd", return_value={"status": "present"}
                    ),
                    mock.patch.object(
                        components, "prepare_nginx_runtime", return_value={"status": "present"}
                    ),
                    mock.patch.object(
                        components, "prepare_haproxy_runtime", return_value={"status": "present"}
                    ),
                    mock.patch.object(components, "prepare_go_tool", return_value={"status": "present"}),
                ):
                    records = components.prepare_native_component_records(context, paths, [], [])

            planned_connectors = [call.args[4] for call in connector_plan.call_args_list]
            self.assertEqual("nginx" in planned_connectors, expects_nginx_plan)
            if expects_nginx_plan:
                self.assertEqual(records["nginx_plan"]["connector"], "nginx")
            else:
                self.assertEqual(records["nginx_plan"], {})

    def test_runtime_component_report_describes_strict_expat_and_cache_fsck_accurately(self) -> None:
        report = components.markdown_report(
            {
                "generated_at": "2026-07-26T00:00:00Z",
                "cache_root": "/tmp/runtime-components",
                "git_components": [],
                "archives": [],
                "dependencies": [],
            }
        )

        self.assertIn(
            "go-ftw and albedo use release-tag resolution; Expat uses release resolution only outside strict evidence runs.",
            report,
        )
        self.assertIn(
            "RUNTIME_COMPONENT_STRICT_VERIFY=1` requires a fresh-clone or prior-cache full git fsck PASS",
            report,
        )
        self.assertNotIn("go-ftw, albedo, and expat are prepared from explicit release-tag sources.", report)
        self.assertNotIn("forces full git fsck", report)

    def test_immutable_expat_rejects_mutable_ref_before_git_or_release_lookup(self) -> None:
        with (
            mock.patch.object(components, "prepare_git_component") as prepare_git,
            mock.patch.object(components, "resolve_latest_github_release_tag") as resolve_latest,
        ):
            record = components.prepare_immutable_git_component(
                "expat",
                "https://github.com/libexpat/libexpat",
                "master",
                Path("cache/git/libexpat"),
                {},
                strict=True,
            )

        self.assertEqual(record["status"], "blocked")
        self.assertIn("full immutable Git commit ID", record["blocker_reason"])
        self.assertFalse(record["immutable_commit_verified"])
        prepare_git.assert_not_called()
        resolve_latest.assert_not_called()

    def test_immutable_expat_uses_pinned_commit_without_latest_release_lookup(self) -> None:
        prepared_record = {
            "name": "expat",
            "url": "https://github.com/libexpat/libexpat",
            "expected_ref": PINNED_EXPAT_COMMIT,
            "actual_head": PINNED_EXPAT_COMMIT,
            "status": "present",
        }
        with (
            mock.patch.object(components, "prepare_git_component", return_value=prepared_record) as prepare_git,
            mock.patch.object(components, "resolve_latest_github_release_tag") as resolve_latest,
        ):
            record = components.prepare_immutable_git_component(
                "expat",
                "https://github.com/libexpat/libexpat",
                PINNED_EXPAT_COMMIT,
                Path("cache/git/libexpat"),
                {},
                strict=True,
            )

        prepare_git.assert_called_once_with(
            "expat",
            "https://github.com/libexpat/libexpat",
            PINNED_EXPAT_COMMIT,
            Path("cache/git/libexpat"),
            {},
            True,
            cache_root=None,
        )
        resolve_latest.assert_not_called()
        self.assertEqual(record["status"], "present")
        self.assertEqual(record["expected_ref"], PINNED_EXPAT_COMMIT)
        self.assertEqual(record["actual_head"], PINNED_EXPAT_COMMIT)
        self.assertTrue(record["immutable_commit_verified"])
        self.assertEqual(record["release_lookup_status"], "not_applicable_immutable_commit")

    def test_immutable_expat_blocks_checkout_record_for_a_different_commit(self) -> None:
        different_commit = "f" * 40
        with mock.patch.object(
            components,
            "prepare_git_component",
            return_value={
                "name": "expat",
                "url": "https://github.com/libexpat/libexpat",
                "expected_ref": PINNED_EXPAT_COMMIT,
                "actual_head": different_commit,
                "status": "present",
            },
        ):
            record = components.prepare_immutable_git_component(
                "expat",
                "https://github.com/libexpat/libexpat",
                PINNED_EXPAT_COMMIT,
                Path("cache/git/libexpat"),
                {},
                strict=True,
            )

        self.assertEqual(record["status"], "blocked")
        self.assertEqual(record["blocker_reason"], "immutable_git_checkout_record_mismatch")
        self.assertFalse(record["immutable_commit_verified"])

    def test_strict_expat_path_uses_only_the_immutable_component_preparer(self) -> None:
        with (
            mock.patch.object(
                components,
                "prepare_immutable_git_component",
                return_value={"status": "present", "immutable_commit_verified": True},
            ) as prepare_immutable,
            mock.patch.object(components, "prepare_release_git_component") as prepare_release,
        ):
            record = components.prepare_expat_git_component(
                "https://github.com/libexpat/libexpat",
                PINNED_EXPAT_COMMIT,
                "master",
                Path("cache/git/libexpat"),
                {},
                strict=True,
            )

        prepare_immutable.assert_called_once_with(
            "expat",
            "https://github.com/libexpat/libexpat",
            PINNED_EXPAT_COMMIT,
            Path("cache/git/libexpat"),
            {},
            True,
            cache_root=None,
        )
        prepare_release.assert_not_called()
        self.assertTrue(record["immutable_commit_verified"])

    def test_non_strict_expat_path_preserves_release_resolution_compatibility(self) -> None:
        with (
            mock.patch.object(components, "prepare_immutable_git_component") as prepare_immutable,
            mock.patch.object(
                components,
                "prepare_release_git_component",
                return_value={"status": "present", "release_tag": "R_2_8_2"},
            ) as prepare_release,
        ):
            record = components.prepare_expat_git_component(
                "https://github.com/libexpat/libexpat",
                "master",
                "master",
                Path("cache/git/libexpat"),
                {},
                strict=False,
            )

        prepare_immutable.assert_not_called()
        prepare_release.assert_called_once_with(
            "expat",
            "https://github.com/libexpat/libexpat",
            "master",
            Path("cache/git/libexpat"),
            {},
            False,
            cache_root=None,
        )
        self.assertEqual(record["release_tag"], "R_2_8_2")

    def test_optional_release_components_still_resolve_the_latest_release(self) -> None:
        for name in ("go-ftw", "albedo"):
            with self.subTest(component=name):
                prepared_record = {
                    "name": name,
                    "url": f"https://github.com/coreruleset/{name}",
                    "expected_ref": "v1.2.3",
                    "actual_head": PINNED_EXPAT_COMMIT,
                    "status": "present",
                }
                with (
                    mock.patch.object(
                        components,
                        "resolve_latest_github_release_tag",
                        return_value=("v1.2.3", "https://example.invalid/release", "network"),
                    ) as resolve_latest,
                    mock.patch.object(
                        components,
                        "prepare_git_component",
                        return_value=prepared_record,
                    ) as prepare_git,
                ):
                    record = components.prepare_release_git_component(
                        name,
                        f"https://github.com/coreruleset/{name}",
                        "v1.0.0",
                        Path(f"cache/git/{name}"),
                        {},
                        strict=True,
                        optional=True,
                    )

                resolve_latest.assert_called_once()
                prepare_git.assert_called_once_with(
                    name,
                    f"https://github.com/coreruleset/{name}",
                    "v1.2.3",
                    Path(f"cache/git/{name}"),
                    {},
                    True,
                    cache_root=None,
                )
                self.assertEqual(record["release_lookup_status"], "network")
                self.assertTrue(record["optional"])

    def test_apache_blocker_does_not_misclassify_expat_include_path(self) -> None:
        compiler_error = (
            "gcc -I/cache/builds/expat/cache-key/prefix/include -c src/msc_filters.c\n"
            "src/msc_filters.c:51:9: error: implicit declaration of function 'helper'\n"
        )

        self.assertEqual(
            components.map_apache_blocker(compiler_error, ["module_file:/cache/module.so"]),
            "apache_connector_build_failed",
        )

    def test_apache_blocker_detects_a_real_missing_expat_header(self) -> None:
        compiler_error = "src/parser.c:7:10: fatal error: expat.h: No such file or directory\n"

        self.assertEqual(
            components.map_apache_blocker(compiler_error, []),
            "missing_expat_headers",
        )

    def test_apache_blocker_keeps_profile_registry_compile_failure_distinct_from_libmodsecurity(self) -> None:
        compiler_error = (
            "gcc -L/cache/modsecurity/lib -lmodsecurity -c src/mod_security3.c\n"
            "src/mod_security3.c:14:10: fatal error: connectors/profile_registry.h: "
            "No such file or directory\n"
        )

        self.assertEqual(
            components.map_apache_blocker(compiler_error, []),
            "apache_connector_build_failed",
        )

    def test_apache_blocker_detects_a_real_missing_libmodsecurity_linker_error(self) -> None:
        compiler_error = "/usr/bin/ld: cannot find -lmodsecurity\n"

        self.assertEqual(
            components.map_apache_blocker(compiler_error, []),
            "missing_libmodsecurity_build",
        )

    def test_apache_build_environment_disables_archive_owner_restoration(self) -> None:
        environment = components.apache_build_environment(
            {"TAR_OPTIONS": "--same-owner"},
            Path("/connector"),
            Path("/framework"),
            Path("/cache"),
            Path("/build"),
            Path("/sources"),
            Path("/archives"),
            {"prefix": "/modsecurity-prefix", "build_id": "modsecurity-build"},
            {
                "expat_lib_dir": "/expat/lib",
                "expat_pkg_config_path": "/expat/lib/pkgconfig",
                "apache_build_root": Path("/apache-build"),
                "httpd_prefix": Path("/httpd-prefix"),
                "expat_cppflags": "-I/expat/include",
                "expat_ldflags": "-L/expat/lib",
                "apache_libs": "-lexpat",
                "crypt_link_arg": "-lcrypt",
            },
        )

        self.assertEqual(environment["TAR_OPTIONS"], "--no-same-owner")

    def test_expat_autotools_stops_when_autoreconf_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="expat-autoreconf-") as temporary:
            root = Path(temporary)
            source_dir = root / "source"
            source_dir.mkdir()
            with mock.patch.object(components, "run_expat_build_step", return_value=False) as run_step:
                result = components.run_expat_autotools_build(
                    source_dir,
                    root / "build",
                    root / "prefix",
                    {},
                    [],
                    root / "build.log",
                    {},
                )

        self.assertFalse(result)
        run_step.assert_called_once()
        self.assertEqual(run_step.call_args.args[0], "expat-autoreconf")

    def test_nginx_blocker_reports_connector_compile_error_before_missing_outputs(self) -> None:
        compiler_error = "src/module.c:123:28: error: field 'phase' has incomplete type\n"

        self.assertEqual(
            components.map_nginx_blocker(compiler_error, ["module_file:/cache/module.so"]),
            "nginx_connector_build_failed",
        )

    def test_shared_modsecurity_blocks_before_build_sinks_when_framework_guard_rejects(self) -> None:
        with tempfile.TemporaryDirectory(prefix="modsecurity-provenance-guard-") as temporary:
            root = Path(temporary)
            cache_root = components.ensure_managed_cache_root(root / "cache")
            source = root / "source"
            source.mkdir()
            git_record = {
                "status": "present",
                "path": str(source),
                "url": "https://github.com/example/modsecurity",
                "expected_ref": "v3",
                "actual_head": "deadbeef",
                "submodule_status": "",
                "submodule_status_clean": True,
            }
            toolchain = {"cc": "cc", "cc_version": "cc test", "cxx": "", "cxx_version": ""}
            provenance = {
                "status": "blocked",
                "blocker_reason": "framework_modsecurity_v3_provenance_guard_rejected",
                "details": "BLOCKED: unexpected immutable checkout",
            }
            with mock.patch.object(components, "toolchain_identity", return_value=toolchain), mock.patch.object(
                components,
                "verify_framework_approved_modsecurity_v3_checkout",
                return_value=provenance,
            ), mock.patch.object(components.shutil, "copytree") as copytree, mock.patch.object(
                components, "run_env"
            ) as run_env, mock.patch.object(components, "copy_modsecurity_outputs") as copy_outputs, mock.patch.object(
                components, "atomic_publish_dir"
            ) as publish:
                record = components.prepare_shared_modsecurity(
                    {},
                    cache_root,
                    root / "work",
                    git_record,
                    {},
                    framework_root=root / "framework",
                )

            self.assertEqual(record["status"], "blocked")
            self.assertEqual(record["blocker_reason"], "modsecurity_v3_provenance_guard_failed")
            self.assertEqual(provenance, record["provenance_verification"])
            self.assertFalse(Path(str(record["build_root"])).exists())
            self.assertFalse(Path(str(record["prefix"])).exists())
            copytree.assert_not_called()
            run_env.assert_not_called()
            copy_outputs.assert_not_called()
            publish.assert_not_called()

    def test_shared_modsecurity_allows_normal_preflight_after_framework_guard_passes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="modsecurity-provenance-guard-") as temporary:
            root = Path(temporary)
            cache_root = components.ensure_managed_cache_root(root / "cache")
            source = root / "source"
            source.mkdir()
            framework_root = root / "framework"
            git_record = {
                "status": "present",
                "path": str(source),
                "url": "https://github.com/example/modsecurity",
                "expected_ref": "v3",
                "actual_head": "deadbeef",
                "submodule_status": "",
                "submodule_status_clean": True,
            }
            toolchain = {"cc": "cc", "cc_version": "cc test", "cxx": "", "cxx_version": ""}
            with mock.patch.object(components, "toolchain_identity", return_value=toolchain), mock.patch.object(
                components,
                "verify_framework_approved_modsecurity_v3_checkout",
                return_value={"status": "passed"},
            ) as provenance_guard, mock.patch.object(
                components, "first_missing_tool", return_value="missing_make"
            ), mock.patch.object(components, "resolve_compiler", return_value="/usr/bin/cc"), mock.patch.object(
                components.shutil, "copytree"
            ) as copytree:
                record = components.prepare_shared_modsecurity(
                    {},
                    cache_root,
                    root / "work",
                    git_record,
                    {},
                    framework_root=framework_root,
                )

            self.assertEqual(record["status"], "blocked")
            self.assertEqual(record["blocker_reason"], "missing_modsecurity_dependency")
            provenance_guard.assert_called_once_with({}, framework_root, source.resolve())
            copytree.assert_not_called()

    def test_framework_modsecurity_guard_passes_paths_as_positional_arguments(self) -> None:
        with tempfile.TemporaryDirectory(prefix="modsecurity-provenance-guard-") as temporary:
            root = Path(temporary)
            framework_root = root / "framework"
            common = framework_root / "ci/lib/common.sh"
            common.parent.mkdir(parents=True)
            common.write_text("# tested through a mocked subprocess\n", encoding="utf-8")
            source = root / "source;not-shell"
            source.mkdir()
            completed = subprocess.CompletedProcess([], 0, "", "")
            with mock.patch.object(components, "run_env", return_value=completed) as run_env:
                result = components.verify_framework_approved_modsecurity_v3_checkout(
                    {
                        "MODSECURITY_V3_GIT_URL": "https://github.com/owasp-modsecurity/ModSecurity.git",
                        "PATH": str(root / "attacker-controlled-path"),
                        "ENV": str(root / "attacker-shell-hook"),
                        "BASH_ENV": str(root / "attacker-bash-hook"),
                    },
                    framework_root,
                    source,
                )

            self.assertEqual(result["status"], "passed")
            run_env.assert_called_once()
            command = run_env.call_args.args[0]
            self.assertEqual(
                command,
                [
                    str(
                        components.verified_host_guard_executable(
                            components._TRUSTED_FRAMEWORK_GUARD_SHELL,
                            "framework_guard_shell",
                        )
                    ),
                    "-c",
                    components._FRAMEWORK_MODSECURITY_V3_GUARD,
                    "framework-modsecurity-v3-provenance-guard",
                    str(common),
                    str(source),
                ],
            )
            self.assertEqual(framework_root, run_env.call_args.kwargs["cwd"])
            self.assertEqual(str(source), run_env.call_args.kwargs["env"]["MODSECURITY_V3_SOURCE_DIR"])
            self.assertEqual(
                components._TRUSTED_FRAMEWORK_GUARD_PATH,
                run_env.call_args.kwargs["env"]["PATH"],
            )
            self.assertNotIn("ENV", run_env.call_args.kwargs["env"])
            self.assertNotIn("BASH_ENV", run_env.call_args.kwargs["env"])

    def test_framework_modsecurity_guard_keeps_only_original_pin_inputs(self) -> None:
        """A re-sourced Framework guard must not inherit its own pin exports."""
        with tempfile.TemporaryDirectory(prefix="modsecurity-provenance-guard-") as temporary:
            root = Path(temporary)
            framework_root = root / "framework"
            common = framework_root / "ci/lib/common.sh"
            common.parent.mkdir(parents=True)
            common.write_text("# tested through a mocked subprocess\n", encoding="utf-8")
            source = root / "source"
            source.mkdir()
            completed = subprocess.CompletedProcess([], 0, "", "")
            loaded_framework_environment = {
                "CONNECTOR_ROOT": str(root / "connector"),
                "FRAMEWORK_ROOT": str(framework_root),
                "VERIFIED_RUN_ROOT": str(root / "verified-run"),
                "ENVOY_VERSION": "1.39.0",
                "TRAEFIK_VERSION": "3.7.10",
                "LIGHTTPD_VERSION": "1.4.85",
                "CI_INHERITED_UPSTREAM_ENV": "ENVOY_VERSION=1.39.0",
            }
            with mock.patch.dict(
                os.environ,
                {"ENVOY_VERSION": "caller-override"},
                clear=True,
            ), mock.patch.object(components, "run_env", return_value=completed) as run_env:
                result = components.verify_framework_approved_modsecurity_v3_checkout(
                    loaded_framework_environment,
                    framework_root,
                    source,
                )

            self.assertEqual(result["status"], "passed")
            guard_env = run_env.call_args.kwargs["env"]
            self.assertEqual(guard_env["ENVOY_VERSION"], "caller-override")
            self.assertNotIn("TRAEFIK_VERSION", guard_env)
            self.assertNotIn("LIGHTTPD_VERSION", guard_env)
            self.assertNotIn("CI_INHERITED_UPSTREAM_ENV", guard_env)
            self.assertEqual(guard_env["CONNECTOR_ROOT"], str(root / "connector"))
            self.assertEqual(guard_env["FRAMEWORK_ROOT"], str(framework_root))
            self.assertEqual(guard_env["VERIFIED_RUN_ROOT"], str(root / "verified-run"))
            self.assertEqual(guard_env["MODSECURITY_V3_SOURCE_DIR"], str(source))

    def test_framework_modsecurity_provisioning_bridge_passes_destination_as_positional_argument(self) -> None:
        with tempfile.TemporaryDirectory(prefix="modsecurity-provisioning-bridge-") as temporary:
            root = Path(temporary)
            framework_root = root / "framework"
            common = framework_root / "ci/lib/common.sh"
            common.parent.mkdir(parents=True)
            common.write_text("# tested through a mocked subprocess\n", encoding="utf-8")
            destination = root / "source;not-shell"
            completed = subprocess.CompletedProcess([], 0, "", "")
            with mock.patch.object(components, "run_env", return_value=completed) as run_env:
                result = components.provision_framework_approved_modsecurity_v3_checkout(
                    {
                        "PATH": str(root / "attacker-controlled-path"),
                        "ENV": str(root / "attacker-shell-hook"),
                        "BASH_ENV": str(root / "attacker-bash-hook"),
                    },
                    framework_root,
                    destination,
                )

            self.assertEqual(result["status"], "passed")
            run_env.assert_called_once()
            command = run_env.call_args.args[0]
            self.assertEqual(
                command,
                [
                    str(
                        components.verified_host_guard_executable(
                            components._TRUSTED_FRAMEWORK_GUARD_SHELL,
                            "framework_guard_shell",
                        )
                    ),
                    "-c",
                    components._FRAMEWORK_MODSECURITY_V3_PROVISIONING_BRIDGE,
                    "framework-modsecurity-v3-provisioning-bridge",
                    str(common),
                    str(destination),
                ],
            )
            self.assertEqual(framework_root, run_env.call_args.kwargs["cwd"])
            self.assertEqual(str(destination), run_env.call_args.kwargs["env"]["MODSECURITY_V3_SOURCE_DIR"])
            self.assertEqual(
                components._TRUSTED_FRAMEWORK_GUARD_PATH,
                run_env.call_args.kwargs["env"]["PATH"],
            )
            self.assertNotIn("ENV", run_env.call_args.kwargs["env"])
            self.assertNotIn("BASH_ENV", run_env.call_args.kwargs["env"])

    def test_framework_modsecurity_metadata_uses_trusted_git_with_scrubbed_environment(self) -> None:
        with tempfile.TemporaryDirectory(prefix="modsecurity-provenance-metadata-") as temporary:
            source = Path(temporary) / "source;not-shell"
            completed = subprocess.CompletedProcess([], 0, "approved-head\n", "")
            with mock.patch.dict(
                os.environ,
                {
                    "GIT_CONFIG_COUNT": "7",
                    "GIT_DIR": str(source / "attacker-git-dir"),
                    "LD_PRELOAD": str(source / "attacker-loader"),
                },
            ), mock.patch.object(components, "run_env", return_value=completed) as run_env:
                output = components.trusted_framework_modsecurity_v3_git_output(source, "rev-parse", "HEAD")

            self.assertEqual(output, "approved-head")
            self.assertEqual(
                run_env.call_args.args[0],
                [
                    str(
                        components.verified_host_guard_executable(
                            components._TRUSTED_FRAMEWORK_GUARD_GIT,
                            "framework_guard_git",
                        )
                    ),
                    "-c",
                    "core.hooksPath=/dev/null",
                    "-c",
                    "core.fsmonitor=false",
                    "-c",
                    "core.useBuiltinFSMonitor=false",
                    "-C",
                    str(source),
                    "rev-parse",
                    "HEAD",
                ],
            )
            self.assertEqual(
                run_env.call_args.kwargs["env"],
                {
                    "PATH": components._TRUSTED_FRAMEWORK_GUARD_PATH,
                    "LC_ALL": "C",
                    "GIT_CONFIG_NOSYSTEM": "1",
                    "GIT_CONFIG_GLOBAL": os.devnull,
                    "GIT_CONFIG_COUNT": "0",
                    "GIT_OPTIONAL_LOCKS": "0",
                    "GIT_ATTR_NOSYSTEM": "1",
                    "GIT_NO_REPLACE_OBJECTS": "1",
                },
            )

    def test_modsecurity_source_configuration_guard_blocks_before_git_preparation(self) -> None:
        with tempfile.TemporaryDirectory(prefix="modsecurity-provenance-guard-") as temporary:
            root = Path(temporary)
            expected_configuration = {
                "status": "blocked",
                "blocker_reason": "framework_modsecurity_v3_provenance_guard_rejected",
                "details": "BLOCKED: immutable source configuration mismatch",
            }
            with mock.patch.object(
                components,
                "verify_framework_approved_modsecurity_v3_provenance",
                return_value=expected_configuration,
            ), mock.patch.object(
                components, "provision_framework_approved_modsecurity_v3_checkout"
            ) as bridge, mock.patch.object(components, "prepare_git_component") as prepare_git:
                record = components.prepare_framework_approved_modsecurity_v3_source(
                    {
                        "MODSECURITY_V3_GIT_URL": "https://github.com/example/unapproved",
                        "MODSECURITY_V3_GIT_REF": "mutable-ref",
                    },
                    root / "framework",
                    root / "source",
                    cache_root=root / "cache",
                )

            self.assertEqual(record["status"], "blocked")
            self.assertEqual(record["blocker_reason"], "modsecurity_v3_provenance_configuration_failed")
            self.assertEqual(expected_configuration, record["provenance_configuration"])
            bridge.assert_not_called()
            prepare_git.assert_not_called()

    def test_modsecurity_source_uses_framework_bridge_and_records_approved_provenance(self) -> None:
        with tempfile.TemporaryDirectory(prefix="modsecurity-provenance-guard-") as temporary:
            root = Path(temporary)
            cache_root = components.ensure_managed_cache_root(root / "cache")
            source = cache_root / "sources" / "modsecurity-v3"
            expected_head = "a" * 40
            configuration = {"status": "passed", "details": "approved source configuration"}
            provisioned_paths: list[Path] = []

            def provision(
                _env: dict[str, str],
                _framework_root: Path,
                destination: Path,
            ) -> dict[str, object]:
                self.assertFalse(destination.exists())
                self.assertFalse(destination.is_symlink())
                self.assertTrue(destination.name.startswith(".modsecurity-v3.tmp-"))
                provisioned_paths.append(destination)
                destination.mkdir()
                return {"status": "passed", "source_path": str(destination)}

            def git_metadata(path: Path, *args: str) -> str:
                self.assertEqual(provisioned_paths[0], path)
                if args == ("rev-parse", "HEAD"):
                    return expected_head
                if args == components.GIT_STATUS_SHORT_ARGS:
                    return ""
                if args == components.GIT_SUBMODULE_STATUS_RECURSIVE_ARGS:
                    return ""
                self.fail(f"unexpected local Git metadata request: {args}")

            with mock.patch.object(
                components,
                "verify_framework_approved_modsecurity_v3_provenance",
                return_value=configuration,
            ), mock.patch.object(
                components,
                "provision_framework_approved_modsecurity_v3_checkout",
                side_effect=provision,
            ) as bridge, mock.patch.object(
                components,
                "verify_framework_approved_modsecurity_v3_checkout",
                side_effect=lambda _env, _framework_root, checkout: {
                    "status": "passed",
                    "source_path": str(checkout),
                },
            ) as verification, mock.patch.object(
                components, "trusted_framework_modsecurity_v3_git_output", side_effect=git_metadata
            ), mock.patch.object(components, "prepare_git_component") as prepare_git:
                record = components.prepare_framework_approved_modsecurity_v3_source(
                    {
                        "MODSECURITY_V3_GIT_URL": "https://github.com/owasp-modsecurity/ModSecurity.git",
                        "MODSECURITY_V3_GIT_REF": "v3.0.15",
                    },
                    root / "framework",
                    source,
                    cache_root=cache_root,
                )

            bridge.assert_called_once_with(
                {
                    "MODSECURITY_V3_GIT_URL": "https://github.com/owasp-modsecurity/ModSecurity.git",
                    "MODSECURITY_V3_GIT_REF": "v3.0.15",
                },
                root / "framework",
                provisioned_paths[0],
            )
            verification.assert_called_once_with(
                {
                    "MODSECURITY_V3_GIT_URL": "https://github.com/owasp-modsecurity/ModSecurity.git",
                    "MODSECURITY_V3_GIT_REF": "v3.0.15",
                },
                root / "framework",
                provisioned_paths[0],
            )
            prepare_git.assert_not_called()
            self.assertEqual(record["status"], "present")
            self.assertEqual(record["approved_acquisition"], "framework_approved_v3_bridge")
            self.assertEqual(source, Path(str(record["path"])))
            self.assertTrue(source.is_dir())
            self.assertFalse(provisioned_paths[0].exists())
            self.assertEqual(expected_head, record["actual_head"])
            self.assertEqual(record["git_fsck"], "PASS")
            self.assertTrue(record["submodule_status_clean"])
            self.assertEqual(configuration, record["provenance_configuration"])
            self.assertEqual(record["provenance_provisioning"]["status"], "passed")
            self.assertEqual(record["provenance_verification"]["status"], "passed")
            self.assertIn("cache_identity", record)
            self.assertIn("cache_key", record)

    def test_modsecurity_source_reuses_only_a_framework_revalidated_complete_cache_entry(self) -> None:
        with tempfile.TemporaryDirectory(prefix="modsecurity-provenance-cache-reuse-") as temporary:
            root = Path(temporary)
            cache_root = components.ensure_managed_cache_root(root / "cache")
            source = cache_root / "sources" / "modsecurity-v3"
            environment = {
                "MODSECURITY_V3_GIT_URL": "https://github.com/owasp-modsecurity/ModSecurity.git",
                "MODSECURITY_V3_GIT_REF": "v3.0.15",
            }
            expected_head = "b" * 40
            identity = components.source_cache_identity(
                "modsecurity-v3",
                environment["MODSECURITY_V3_GIT_URL"],
                environment["MODSECURITY_V3_GIT_REF"],
                expected_head,
            )
            components.mark_managed_cache_entry(
                source,
                cache_root,
                component="source:modsecurity-v3",
                cache_key=str(identity["cache_key"]),
            )
            source.parent.mkdir(parents=True)
            source.mkdir()
            components.write_cache_entry_completion(
                source,
                cache_root,
                component="source:modsecurity-v3",
                cache_key=str(identity["cache_key"]),
                cache_identity=identity,
            )

            def git_metadata(path: Path, *args: str) -> str:
                self.assertEqual(path, source)
                if args == ("rev-parse", "HEAD"):
                    return expected_head
                if args == components.GIT_STATUS_SHORT_ARGS:
                    return ""
                if args == components.GIT_SUBMODULE_STATUS_RECURSIVE_ARGS:
                    return ""
                self.fail(f"unexpected local Git metadata request: {args}")

            verification = {"status": "passed", "source_path": str(source)}
            with mock.patch.object(
                components,
                "verify_framework_approved_modsecurity_v3_provenance",
                return_value={"status": "passed"},
            ), mock.patch.object(
                components,
                "verify_framework_approved_modsecurity_v3_checkout",
                return_value=verification,
            ) as checkout_verification, mock.patch.object(
                components,
                "trusted_framework_modsecurity_v3_git_output",
                side_effect=git_metadata,
            ), mock.patch.object(
                components,
                "provision_framework_approved_modsecurity_v3_checkout",
            ) as bridge, mock.patch.object(components, "prepare_git_component") as prepare_git:
                record = components.prepare_framework_approved_modsecurity_v3_source(
                    environment,
                    root / "framework",
                    source,
                    cache_root=cache_root,
                )

            checkout_verification.assert_called_once_with(environment, root / "framework", source)
            bridge.assert_not_called()
            prepare_git.assert_not_called()
            self.assertEqual(record["status"], "present")
            self.assertEqual(record["approved_acquisition"], "framework_approved_v3_cache_reuse")
            self.assertEqual(record["provenance_verification"], verification)
            self.assertEqual(record["cache_key"], identity["cache_key"])
            self.assertTrue(components.cache_entry_complete(
                source,
                cache_root,
                component="source:modsecurity-v3",
                cache_key=str(identity["cache_key"]),
                cache_identity=identity,
            ))

    def test_modsecurity_source_bridge_failure_preserves_published_cache_without_generic_fallback(self) -> None:
        with tempfile.TemporaryDirectory(prefix="modsecurity-provenance-guard-") as temporary:
            root = Path(temporary)
            cache_root = components.ensure_managed_cache_root(root / "cache")
            source = cache_root / "sources" / "modsecurity-v3"
            components.mark_managed_cache_entry(
                source,
                cache_root,
                component="source:modsecurity-v3",
                cache_key="published-cache-entry",
            )
            source.parent.mkdir(parents=True)
            source.mkdir()
            sentinel = source / "preserve-on-bridge-failure"
            sentinel.write_text("published cache must remain untouched", encoding="utf-8")
            bridge_failure = {
                "status": "blocked",
                "blocker_reason": "framework_modsecurity_v3_provenance_guard_rejected",
                "details": "BLOCKED: bridge could not provision source",
            }
            with mock.patch.object(
                components,
                "verify_framework_approved_modsecurity_v3_provenance",
                return_value={"status": "passed"},
            ), mock.patch.object(
                components,
                "verify_framework_approved_modsecurity_v3_checkout",
                return_value={"status": "blocked"},
            ), mock.patch.object(
                components,
                "provision_framework_approved_modsecurity_v3_checkout",
                return_value=bridge_failure,
            ) as bridge, mock.patch.object(components, "prepare_git_component") as prepare_git:
                record = components.prepare_framework_approved_modsecurity_v3_source(
                    {
                        "MODSECURITY_V3_GIT_URL": "https://github.com/owasp-modsecurity/ModSecurity.git",
                        "MODSECURITY_V3_GIT_REF": "v3.0.15",
                    },
                    root / "framework",
                    source,
                    cache_root=cache_root,
                )

            bridge.assert_called_once()
            prepare_git.assert_not_called()
            self.assertEqual(record["status"], "blocked")
            self.assertEqual(record["blocker_reason"], "modsecurity_v3_framework_provisioning_failed")
            self.assertEqual(bridge_failure, record["provenance_provisioning"])
            self.assertTrue(sentinel.is_file())
            self.assertTrue(components.cache_entry_marker_valid(source, cache_root))
            self.assertEqual(list(source.parent.glob(".modsecurity-v3.tmp-*")), [])

            with mock.patch.object(
                components,
                "toolchain_identity",
                return_value={"cc": "cc", "cc_version": "cc test", "cxx": "", "cxx_version": ""},
            ), mock.patch.object(components.shutil, "copytree") as copytree, mock.patch.object(
                components, "run_env"
            ) as run_env, mock.patch.object(components, "copy_modsecurity_outputs") as copy_outputs, mock.patch.object(
                components, "atomic_publish_dir"
            ) as publish:
                build_record = components.prepare_shared_modsecurity(
                    {},
                    cache_root,
                    root / "work",
                    record,
                    {},
                    framework_root=root / "framework",
                )

            self.assertEqual(build_record["status"], "blocked")
            self.assertEqual(build_record["blocker_reason"], "modsecurity_v3_framework_provisioning_failed")
            copytree.assert_not_called()
            run_env.assert_not_called()
            copy_outputs.assert_not_called()
            publish.assert_not_called()

    def test_modsecurity_source_post_provision_guard_failure_preserves_published_cache_without_publish_or_generic_fallback(
        self,
    ) -> None:
        """A rejected post-provision guard must discard only the staging checkout."""
        with tempfile.TemporaryDirectory(prefix="modsecurity-provenance-guard-") as temporary:
            root = Path(temporary)
            cache_root = components.ensure_managed_cache_root(root / "cache")
            source = cache_root / "sources" / "modsecurity-v3"
            component = "source:modsecurity-v3"
            environment = {
                "MODSECURITY_V3_GIT_URL": "https://github.com/owasp-modsecurity/ModSecurity.git",
                "MODSECURITY_V3_GIT_REF": "v3.0.15",
            }
            published_identity = components.source_cache_identity(
                "modsecurity-v3",
                environment["MODSECURITY_V3_GIT_URL"],
                environment["MODSECURITY_V3_GIT_REF"],
            )
            components.mark_managed_cache_entry(
                source,
                cache_root,
                component=component,
                cache_key=str(published_identity["cache_key"]),
            )
            source.parent.mkdir(parents=True)
            source.mkdir()
            sentinel = source / "preserve-on-post-provision-guard-failure"
            sentinel.write_text("published cache must remain untouched", encoding="utf-8")
            components.write_cache_entry_completion(
                source,
                cache_root,
                component=component,
                cache_key=str(published_identity["cache_key"]),
                cache_identity=published_identity,
            )
            self.assertTrue(
                components.cache_entry_complete(
                    source,
                    cache_root,
                    component=component,
                    cache_key=str(published_identity["cache_key"]),
                    cache_identity=published_identity,
                )
            )

            staging_paths: list[Path] = []
            cache_reuse_rejection = {
                "status": "blocked",
                "blocker_reason": "framework_modsecurity_v3_provenance_guard_rejected",
                "details": "BLOCKED: existing cache needs replacement",
            }
            post_provision_rejection = {
                "status": "blocked",
                "blocker_reason": "framework_modsecurity_v3_provenance_guard_rejected",
                "details": "BLOCKED: bridge-created checkout failed Framework verification",
            }

            def provision(
                _env: dict[str, str],
                _framework_root: Path,
                destination: Path,
            ) -> dict[str, object]:
                self.assertFalse(destination.exists())
                self.assertFalse(destination.is_symlink())
                self.assertTrue(components.cache_entry_marker_valid(destination, cache_root))
                staging_marker = components.read_json(components.cache_entry_marker_path(destination, cache_root))
                self.assertEqual(staging_marker["component"], component)
                self.assertEqual(str(published_identity["cache_key"]), staging_marker["cache_key"])
                self.assertNotEqual(staging_marker.get("status"), "complete")
                destination.mkdir()
                (destination / "bridge-created-partial-checkout").write_text("partial", encoding="utf-8")
                staging_paths.append(destination)
                return {"status": "passed", "source_path": str(destination)}

            with mock.patch.object(
                components,
                "verify_framework_approved_modsecurity_v3_provenance",
                return_value={"status": "passed"},
            ), mock.patch.object(
                components,
                "provision_framework_approved_modsecurity_v3_checkout",
                side_effect=provision,
            ) as bridge, mock.patch.object(
                components,
                "verify_framework_approved_modsecurity_v3_checkout",
                side_effect=[cache_reuse_rejection, post_provision_rejection],
            ) as verification, mock.patch.object(
                components, "write_cache_entry_completion"
            ) as completion, mock.patch.object(components, "atomic_publish_dir") as publish, mock.patch.object(
                components, "prepare_git_component"
            ) as prepare_git:
                record = components.prepare_framework_approved_modsecurity_v3_source(
                    environment,
                    root / "framework",
                    source,
                    cache_root=cache_root,
                )

            bridge.assert_called_once_with(environment, root / "framework", staging_paths[0])
            self.assertEqual(
                verification.call_args_list,
                [
                    mock.call(environment, root / "framework", source),
                    mock.call(environment, root / "framework", staging_paths[0]),
                ],
            )
            completion.assert_not_called()
            publish.assert_not_called()
            prepare_git.assert_not_called()
            self.assertEqual(record["status"], "blocked")
            self.assertEqual(record["blocker_reason"], "modsecurity_v3_provenance_guard_failed")
            self.assertEqual(post_provision_rejection, record["provenance_verification"])
            self.assertTrue(sentinel.is_file())
            self.assertTrue(
                components.cache_entry_complete(
                    source,
                    cache_root,
                    component=component,
                    cache_key=str(published_identity["cache_key"]),
                    cache_identity=published_identity,
                )
            )
            self.assertFalse(staging_paths[0].exists())
            self.assertFalse(staging_paths[0].is_symlink())
            self.assertFalse(components.cache_entry_marker_path(staging_paths[0], cache_root).exists())
            self.assertEqual(list(source.parent.glob(".modsecurity-v3.tmp-*")), [])

    def prepare_haproxy_with(self, returncode: int, output: str) -> dict[str, object]:
        with tempfile.TemporaryDirectory(prefix="haproxy-prepare-") as temporary:
            base = Path(temporary)
            cache = base / "cache"
            components.ensure_managed_cache_root(cache)
            build = base / "build"
            sources = cache / "sources"
            archives = cache / "archives"
            connector_build = cache / "builds/connectors/haproxy/test-build"
            cache_identity_payload = {
                "cache_schema_version": components.CACHE_SCHEMA_VERSION,
                "component": "haproxy",
                "extra_inputs": {"connector_source_hash": "source-hash"},
            }
            cache_key = components.stable_hash(cache_identity_payload)
            cache_identity = {**cache_identity_payload, "cache_key": cache_key}
            plan = {
                "connector": "haproxy",
                "connector_build_id": cache_key,
                "cache_key": cache_key,
                "cache_identity": cache_identity,
                "cache_root": str(cache),
                "root": str(connector_build),
                "modsecurity_build_id": "modsecurity-build",
                "source_hash": "source-hash",
                "build_flags": "{}",
                "build_root": str(connector_build),
                "manifest": str(connector_build / "manifest.json"),
                "output_paths": {},
            }
            completed = subprocess.CompletedProcess(
                args=["prepare-haproxy-runtime.sh"],
                returncode=returncode,
                stdout=output,
                stderr="",
            )
            with mock.patch.object(components, "run_build", return_value=completed):
                record = components.prepare_haproxy_runtime(
                    {},
                    ROOT,
                    ROOT / "modules/ModSecurity-test-Framework",
                    cache,
                    build,
                    sources,
                    archives,
                    {"status": "built", "build_id": "modsecurity-build"},
                    plan,
                )
            self.assertFalse(connector_build.exists())
            self.assertFalse(any(path.name.startswith(f".{cache_key}.tmp-") for path in connector_build.parent.iterdir()))
            return record

    def prepare_haproxy_binding_failure_with(
        self,
        returncode: int,
        output: str,
    ) -> tuple[dict[str, object], str, tuple[tuple[Path, bool], ...]]:
        with tempfile.TemporaryDirectory(prefix="haproxy-binding-failure-") as temporary:
            root = Path(temporary)
            cache = root / "cache"
            components.ensure_managed_cache_root(cache)
            plan = self.haproxy_runtime_plan(cache)
            prep = subprocess.CompletedProcess(
                args=["prepare-haproxy-runtime.sh"],
                returncode=0,
                stdout="haproxy_prepare: ready\n",
                stderr="",
            )
            binding = subprocess.CompletedProcess(
                args=["make"],
                returncode=returncode,
                stdout="",
                stderr=output,
            )

            def prepare_with_runtime_binary(
                _script: Path,
                environment: dict[str, str],
                _cwd: Path,
                _log_path: Path,
            ) -> subprocess.CompletedProcess[str]:
                binary = Path(environment["HAPROXY_BIN"])
                binary.parent.mkdir(parents=True, exist_ok=True)
                binary.write_text("#!/bin/sh\n", encoding="utf-8")
                binary.chmod(0o700)
                return prep

            with mock.patch.object(components, "run_build", side_effect=prepare_with_runtime_binary), mock.patch.object(
                components, "run_haproxy_binding_build", return_value=binding
            ), mock.patch.object(components, "safe_remove_dir", wraps=components.safe_remove_dir) as cleanup, mock.patch(
                "sys.stderr", new_callable=io.StringIO
            ) as stderr:
                record = components.prepare_haproxy_runtime(
                    {},
                    ROOT,
                    ROOT / "modules/ModSecurity-test-Framework",
                    cache,
                    root / "build",
                    cache / "sources",
                    cache / "archives",
                    {"status": "built", "build_id": "modsecurity-build"},
                    plan,
                )
                diagnostic = stderr.getvalue()
                cleanup_observations = tuple(
                    (Path(call.args[0]), Path(call.args[0]).exists())
                    for call in cleanup.call_args_list
                )
        return record, diagnostic, cleanup_observations

    def haproxy_runtime_plan(
        self,
        cache_root: Path,
        *,
        source_hash: str = "source-hash",
    ) -> dict[str, object]:
        cache_identity_payload = {
            "cache_schema_version": components.CACHE_SCHEMA_VERSION,
            "component": "haproxy",
            "extra_inputs": {"connector_source_hash": source_hash},
        }
        cache_key = components.stable_hash(cache_identity_payload)
        cache_identity = {**cache_identity_payload, "cache_key": cache_key}
        cache_entry = cache_root / "builds" / "connectors" / "haproxy" / cache_key
        return {
            "connector": "haproxy",
            "connector_build_id": cache_key,
            "cache_key": cache_key,
            "cache_identity": cache_identity,
            "cache_root": str(cache_root),
            "root": str(cache_entry),
            "build_root": str(cache_entry),
            "manifest": str(cache_entry / "manifest.json"),
            "source_hash": source_hash,
            "output_paths": {},
        }

    def test_haproxy_runtime_context_contains_all_mutable_outputs_under_invocation_build_root(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(prefix="haproxy-runtime-context-") as temporary:
            root = Path(temporary)
            cache_root = root / "cache"
            build_root = root / "invocation-build"
            plan = self.haproxy_runtime_plan(cache_root)

            context = components.haproxy_runtime_context(plan, build_root)
            prep_env = components.haproxy_prepare_environment(
                {},
                ROOT,
                ROOT / "modules/ModSecurity-test-Framework",
                cache_root,
                build_root,
                cache_root / "sources",
                cache_root / "archives",
                context,
            )

            expected_root = (
                build_root
                / "runtime-components"
                / "haproxy"
                / str(plan["cache_key"])
            ).resolve()
            self.assertEqual(context["root"], expected_root)
            self.assertEqual(prep_env["BUILD_ROOT"], str(build_root.resolve()))
            self.assertEqual(prep_env["LOG_DIR"], str(context["framework_log_dir"]))
            self.assertEqual(
                components.connector_output_layout(
                    "haproxy",
                    Path(str(plan["root"])),
                )["output_paths"],
                {},
            )
            mutable_paths = (
                context["root"],
                context["haproxy_runtime_build_dir"],
                context["haproxy_runtime_build_worktree"],
                context["haproxy_runtime_dir"],
                context["haproxy_bin"],
                context["binding_dir"],
                context["spoa_dir"],
                context["spoa_bin"],
                context["paths_env"],
                context["log_path"],
                context["framework_log_dir"],
                context["framework_build_log"],
            )
            for path in mutable_paths:
                with self.subTest(path=path):
                    self.assertNotEqual(path, build_root.resolve())
                    self.assertTrue(components.is_within(path, build_root))
                    self.assertFalse(components.is_within(path, cache_root))
            self.assertEqual(
                prep_env["HAPROXY_RUNTIME_BUILD_WORKTREE"],
                str(context["haproxy_runtime_build_worktree"]),
            )
            self.assertEqual(
                components.haproxy_runtime_context(plan, build_root)["root"],
                expected_root,
            )

    def test_haproxy_runtime_context_rejects_cache_owned_mutable_output_root(self) -> None:
        with tempfile.TemporaryDirectory(prefix="haproxy-cache-output-rejection-") as temporary:
            cache_root = Path(temporary) / "cache"
            plan = self.haproxy_runtime_plan(cache_root)

            with self.assertRaisesRegex(
                RuntimeError,
                "haproxy_runtime_output_overlaps_component_cache",
            ):
                components.haproxy_runtime_context(plan, cache_root / "mutable-build")

    def test_haproxy_runtime_preclaim_allows_incomplete_runtime_cleanup(self) -> None:
        with tempfile.TemporaryDirectory(prefix="haproxy-runtime-preclaim-") as temporary:
            root = Path(temporary)
            plan = self.haproxy_runtime_plan(root / "cache")
            context = components.haproxy_runtime_context(plan, root / "build")
            self.assertEqual(components.claim_haproxy_runtime_entry(plan, context), "")
            marker = components.read_json(
                components.cache_entry_marker_path(context["root"], context["build_root"])
            )
            self.assertEqual(marker["component"], "runtime:haproxy")
            self.assertEqual(marker["cache_key"], plan["cache_key"])
            self.assertTrue(context["root"].is_dir())
            self.assertFalse(context["root"].is_symlink())

            record: dict[str, object] = {}
            self.assertEqual(
                components.reconcile_haproxy_cached_entry(plan, context, record),
                "",
            )
            self.assertFalse(context["root"].exists())
            self.assertEqual(record["invalidation_reason"], "missing_or_incomplete_haproxy_runtime")

    def test_haproxy_runtime_preclaim_rejects_a_concurrently_created_root(self) -> None:
        with tempfile.TemporaryDirectory(prefix="haproxy-runtime-race-") as temporary:
            root = Path(temporary)
            plan = self.haproxy_runtime_plan(root / "cache")
            context = components.haproxy_runtime_context(plan, root / "build")
            original_mark = components.mark_managed_cache_entry

            def mark_then_create(*args: object, **kwargs: object) -> None:
                original_mark(*args, **kwargs)
                context["root"].mkdir(parents=True)

            with mock.patch.object(
                components,
                "mark_managed_cache_entry",
                side_effect=mark_then_create,
            ):
                error = components.claim_haproxy_runtime_entry(plan, context)

            self.assertEqual(error, f"haproxy_runtime_root_already_exists: {context['root']}")
            self.assertFalse(
                components.cache_entry_marker_valid(context["root"], context["build_root"])
            )

    def test_haproxy_runtime_reuse_requires_a_preclaimed_runtime_entry(self) -> None:
        with tempfile.TemporaryDirectory(prefix="haproxy-runtime-unowned-reuse-") as temporary:
            root = Path(temporary)
            plan = self.haproxy_runtime_plan(root / "cache")
            context = components.haproxy_runtime_context(plan, root / "build")
            for executable_path in (context["haproxy_bin"], context["spoa_bin"]):
                executable_path.parent.mkdir(parents=True, exist_ok=True)
                executable_path.write_text("#!/bin/sh\n", encoding="utf-8")
                executable_path.chmod(0o700)
            context["paths_env"].parent.mkdir(parents=True, exist_ok=True)
            context["paths_env"].write_text("HAPROXY_BIN=unused\n", encoding="utf-8")

            with mock.patch.object(components, "connector_manifest_ready", return_value=True):
                self.assertFalse(components.haproxy_cached_entry_reusable(plan, context))

    def test_haproxy_runtime_context_rejects_build_key_path_escape(self) -> None:
        with tempfile.TemporaryDirectory(prefix="haproxy-build-key-escape-") as temporary:
            root = Path(temporary)
            plan = self.haproxy_runtime_plan(root / "cache")
            plan["connector_build_id"] = "../escape"
            plan["cache_key"] = "../escape"
            plan["cache_identity"]["cache_key"] = "../escape"  # type: ignore[index]

            with self.assertRaisesRegex(RuntimeError, "unsafe_haproxy_runtime_build_key"):
                components.haproxy_runtime_context(plan, root / "build")

    def test_haproxy_runtime_context_rejects_source_build_key_mismatch(self) -> None:
        with tempfile.TemporaryDirectory(prefix="haproxy-build-key-mismatch-") as temporary:
            root = Path(temporary)
            for field, different_value in (
                ("connector_build_id", "different-build-key"),
                ("source_hash", "different-source-hash"),
            ):
                with self.subTest(field=field):
                    plan = self.haproxy_runtime_plan(root / "cache")
                    plan[field] = different_value
                    with self.assertRaisesRegex(
                        RuntimeError,
                        "haproxy_source_build_key_mismatch",
                    ):
                        components.haproxy_runtime_context(plan, root / "build")

    def test_haproxy_build_failure_returning_77_is_execution_failure(self) -> None:
        record = self.prepare_haproxy_with(
            77,
            "haproxy_prepare: running haproxy-build\n"
            "haproxy_prepare: blocked command failed: make\n",
        )
        self.assertEqual(record["status"], "failed")
        self.assertEqual(record["build_exit_code"], 77)

    def test_haproxy_binding_failure_diagnostic_is_bounded_and_opaque(self) -> None:
        proc = subprocess.CompletedProcess(
            args=["make"],
            returncode=2,
            stdout=(
                "cc1: fatal error: modsecurity/transaction.h: No such file or directory "
                "Authorization: Bearer hidden\x1b[31m\N{RIGHT-TO-LEFT OVERRIDE}\n"
                "FAIL: binding compile failed error: -DAPI_SECRET=super-secret-token "
                "body=must-not-appear https://example.invalid/private\x00\n"
            ),
            stderr="FAIL: HAProxy ModSecurity binding source did not compile\n",
        )

        diagnostics = components.haproxy_failure_diagnostic_lines(proc)
        rendered = "\n".join(diagnostics)

        self.assertIn("classification=compiler_fatal_error", rendered)
        self.assertIn("missing_header=transaction.h", rendered)
        self.assertIn("classification=compiler_error", rendered)
        self.assertIn("build_step=modsecurity_binding_source_compile", rendered)
        self.assertNotIn("super-secret-token", rendered)
        self.assertNotIn("must-not-appear", rendered)
        self.assertNotIn("https://example.invalid/private", rendered)
        self.assertNotIn("hidden", rendered)
        self.assertNotIn("\x1b", rendered)
        self.assertNotIn("\N{RIGHT-TO-LEFT OVERRIDE}", rendered)
        self.assertNotIn("\x00", rendered)
        self.assertLessEqual(len(diagnostics), components.HAPROXY_FAILURE_DIAGNOSTIC_MAX_LINES)

    def test_haproxy_binding_failure_preserves_status_and_emits_safe_summary(self) -> None:
        record, diagnostic, _ = self.prepare_haproxy_binding_failure_with(
            23,
            "FAIL: HAProxy ModSecurity binding self-test source did not compile\n"
            "Authorization: Bearer hidden \x1b[31mhttps://example.invalid/private"
            "\N{RIGHT-TO-LEFT OVERRIDE}\n",
        )
        self.assertEqual(record["status"], "failed")
        self.assertEqual(record["blocker_reason"], "haproxy_connector_build_failed")
        self.assertEqual(record["build_exit_code"], 23)
        self.assertIn("target=build-modsecurity-binding build-spoa-runtime", diagnostic)
        self.assertIn("build_log=private_task_owned_haproxy-build.log", diagnostic)
        self.assertIn("build_step=modsecurity_binding_self_test_source_compile", diagnostic)
        self.assertNotIn("hidden", diagnostic)
        self.assertNotIn("https://example.invalid/private", diagnostic)
        self.assertNotIn("\x1b", diagnostic)
        self.assertNotIn("\N{RIGHT-TO-LEFT OVERRIDE}", diagnostic)

    def test_haproxy_binding_missing_artifacts_remain_failure(self) -> None:
        record, diagnostic, _ = self.prepare_haproxy_binding_failure_with(0, "unclassified output\n")

        self.assertEqual(record["status"], "failed")
        self.assertEqual(record["blocker_reason"], "haproxy_connector_build_failed")
        self.assertEqual(record["build_exit_code"], 0)
        self.assertIn("missing_artifact=spoa_runtime_binary", diagnostic)
        self.assertIn("missing_artifact=modsecurity_binding_paths", diagnostic)
        self.assertNotIn("unclassified output", diagnostic)

    def test_haproxy_binding_failure_cleans_transactional_staging(self) -> None:
        record, _, cleanup_observations = self.prepare_haproxy_binding_failure_with(
            2,
            "fatal error: required-header.h: No such file or directory\n",
        )

        self.assertEqual(record["status"], "failed")
        self.assertEqual(len(cleanup_observations), 1)
        cleanup_path, exists_after_cleanup = cleanup_observations[0]
        self.assertIn(".tmp-", cleanup_path.name)
        self.assertFalse(exists_after_cleanup)

    def test_haproxy_binding_failure_diagnostic_limits_classifications_and_handles_empty_output(self) -> None:
        proc = subprocess.CompletedProcess(
            args=["make"],
            returncode=2,
            stdout=(
                "fatal error: modsecurity/modsecurity.h: No such file or directory\n"
                "fatal error: modsecurity/rules_set.h: No such file or directory\n"
                "fatal error: modsecurity/transaction.h: No such file or directory\n"
                "FAIL: HAProxy ModSecurity binding source did not compile\n"
                "FAIL: HAProxy ModSecurity binding self-test source did not compile\n"
                "FAIL: HAProxy ModSecurity binding self-test did not link\n"
            ),
            stderr=None,
        )

        diagnostics = components.haproxy_failure_diagnostic_lines(proc)

        self.assertEqual(len(diagnostics), components.HAPROXY_FAILURE_DIAGNOSTIC_MAX_LINES)
        self.assertEqual(diagnostics[-1], "[classification list truncated]")
        self.assertEqual(
            components.haproxy_failure_diagnostic_lines(
                subprocess.CompletedProcess(args=["make"], returncode=2, stdout=None, stderr=None)
            ),
            [],
        )

    def test_haproxy_binding_failure_diagnostic_keeps_order_at_exact_limit(self) -> None:
        proc = subprocess.CompletedProcess(
            args=["make"],
            returncode=2,
            stdout=(
                "fatal error: modsecurity/modsecurity.h: No such file or directory\n"
                "fatal error: modsecurity/rules_set.h: No such file or directory\n"
                "fatal error: modsecurity/transaction.h: No such file or directory\n"
                "FAIL: HAProxy ModSecurity binding source did not compile for diagnostic SPOP runtime\n"
                "FAIL: HAProxy ModSecurity SPOA runtime source did not compile\n"
                "FAIL: HAProxy ModSecurity binding source did not compile\n"
            ),
            stderr=None,
        )

        self.assertEqual(
            components.haproxy_failure_diagnostic_lines(proc),
            [
                components.HAPROXY_DIAGNOSTIC_COMPILER_FATAL_ERROR,
                "missing_header=modsecurity.h",
                "missing_header=rules_set.h",
                "missing_header=transaction.h",
                components.HAPROXY_DIAGNOSTIC_COMPILER_ERROR,
                "build_step=spoa_binding_source_compile",
                "build_step=spoa_runtime_source_compile",
                "build_step=modsecurity_binding_source_compile",
            ],
        )

    def test_haproxy_binding_failure_diagnostic_accepts_known_stdout_or_stderr_only(self) -> None:
        known_message = "FAIL: HAProxy ModSecurity SPOA runtime source did not compile\n"
        expected = {"classification=compiler_error", "build_step=spoa_runtime_source_compile"}

        for output_name in ("stdout", "stderr"):
            with self.subTest(output_name=output_name):
                proc = subprocess.CompletedProcess(
                    args=["make"],
                    returncode=2,
                    stdout=known_message if output_name == "stdout" else "",
                    stderr=known_message if output_name == "stderr" else "",
                )
                self.assertEqual(set(components.haproxy_failure_diagnostic_lines(proc)), expected)

        rejected = subprocess.CompletedProcess(
            args=["make"],
            returncode=2,
            stdout=(
                "FAIL: build https://example.invalid/Authorization: Bearer hidden\n"
                "error: body=must-not-appear API_SECRET=super-secret-token\n"
            ),
            stderr=None,
        )
        self.assertEqual(components.haproxy_failure_diagnostic_lines(rejected), [])

    def test_haproxy_binding_build_replaces_invalid_tool_output_without_broadening_run_env(self) -> None:
        command = [
            sys.executable,
            "-c",
            "import sys; sys.stderr.buffer.write(bytes([255]) + b'\\nFAIL: HAProxy Common SDK source did not compile: /private/source.c\\n'); raise SystemExit(2)",
        ]

        with self.assertRaises(UnicodeDecodeError):
            components.run_env(command)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            tools = root / "tools"
            tools.mkdir()
            fake_make = tools / "make"
            fake_make.write_text(
                "#!" + sys.executable + "\n" + command[2] + "\n",
                encoding="utf-8",
            )
            fake_make.chmod(0o700)
            log_path = root / "private-build.log"

            proc = components.run_haproxy_binding_build(
                root / "connector",
                {"PATH": str(tools)},
                log_path,
            )
            logged_output = log_path.read_text(encoding="utf-8")

        self.assertEqual(proc.returncode, 2)
        self.assertEqual(proc.stdout, "")
        self.assertEqual(proc.stderr, "\ufffd\nFAIL: HAProxy Common SDK source did not compile: /private/source.c\n")
        self.assertIn("\ufffd", logged_output)
        self.assertEqual(
            components.haproxy_failure_diagnostic_lines(proc),
            [
                components.HAPROXY_DIAGNOSTIC_COMPILER_ERROR,
                "build_step=modsecurity_common_sdk_source_compile",
            ],
        )

    def test_haproxy_binding_failure_diagnostic_scans_stderr_before_stdout_with_fixed_values(self) -> None:
        proc = subprocess.CompletedProcess(
            args=["make"],
            returncode=2,
            stdout=(
                "FAIL: HAProxy ModSecurity SPOA runtime did not link with libmodsecurity\n"
                "Authorization: Bearer hidden\n"
            ),
            stderr=(
                "BLOCKED: HAProxy libModSecurity resolver: /private/resolver-token\n"
                "FAIL: HAProxy Common SDK source did not compile: /private/source.c\n"
            ),
        )

        diagnostics = components.haproxy_failure_diagnostic_lines(proc)

        self.assertEqual(
            diagnostics,
            [
                components.HAPROXY_DIAGNOSTIC_RESOLVER_ERROR,
                "build_step=modsecurity_resolver",
                components.HAPROXY_DIAGNOSTIC_COMPILER_ERROR,
                "build_step=modsecurity_common_sdk_source_compile",
                components.HAPROXY_DIAGNOSTIC_LINKER_ERROR,
                "build_step=spoa_runtime_link",
            ],
        )
        rendered = "\n".join(diagnostics)
        self.assertNotIn("/private", rendered)
        self.assertNotIn("hidden", rendered)

    def test_haproxy_binding_failure_diagnostic_stops_after_bounded_untrusted_output(self) -> None:
        proc = subprocess.CompletedProcess(
            args=["make"],
            returncode=2,
            stdout="FAIL: HAProxy Common SDK source did not compile: /private/stdout-source.c\n",
            stderr=(
                "Authorization: Bearer hidden\n"
                * components.HAPROXY_FAILURE_DIAGNOSTIC_SCAN_MAX_LINES
                + "FAIL: HAProxy Common SDK source did not compile: /private/source.c\n"
            ),
        )

        diagnostics = components.haproxy_failure_diagnostic_lines(proc)

        self.assertEqual(
            diagnostics,
            [
                components.HAPROXY_DIAGNOSTIC_COMPILER_ERROR,
                "build_step=modsecurity_common_sdk_source_compile",
            ],
        )
        self.assertNotIn("hidden", "\n".join(diagnostics))

    def test_haproxy_binding_failure_diagnostic_accepts_maximum_line_and_stops_on_overlong_line(self) -> None:
        marker = "FAIL: HAProxy Common SDK source did not compile: /private/source.c\n"
        maximum_line = "x" * components.HAPROXY_FAILURE_DIAGNOSTIC_MAX_LINE_CHARS
        expected = [
            components.HAPROXY_DIAGNOSTIC_COMPILER_ERROR,
            "build_step=modsecurity_common_sdk_source_compile",
        ]

        accepted = subprocess.CompletedProcess(
            args=["make"], returncode=2, stdout="", stderr=f"{maximum_line}\n{marker}"
        )
        rejected = subprocess.CompletedProcess(
            args=["make"], returncode=2, stdout="", stderr=f"{maximum_line}x\n{marker}"
        )

        self.assertEqual(components.haproxy_failure_diagnostic_lines(accepted), expected)
        self.assertEqual(components.haproxy_failure_diagnostic_lines(rejected), [])

    def test_haproxy_binding_failure_footer_emits_first_allowlisted_target(self) -> None:
        proc = subprocess.CompletedProcess(
            args=["make"],
            returncode=2,
            stdout=(
                "make: *** [Makefile:12: build-spoa-runtime] Error 2\n"
            ),
            stderr=(
                "make[1]: *** [build-modsecurity-binding] Error 2\n"
                "make: *** [Makefile:13: build-spoa-runtime] Error 2\n"
            ),
        )

        self.assertEqual(
            components.haproxy_failure_target_from_footers(proc),
            "build-modsecurity-binding",
        )
        self.assertIn(
            "target_failure=build-modsecurity-binding",
            components.haproxy_failure_diagnostic_lines(proc),
        )

    def test_haproxy_binding_failure_footer_accepts_exact_make_grammar(self) -> None:
        expected_target_paths = {
            "build-modsecurity-binding": "/task/haproxy-modsecurity-binding-self-test",
            "build-spoa-runtime": "/task/haproxy-modsecurity-spoa",
        }
        cases = (
            ("make: *** [build-modsecurity-binding] Error 2", "build-modsecurity-binding"),
            ("make[001]: *** [Makefile:7:\tbuild-spoa-runtime] Error 12", "build-spoa-runtime"),
            (
                "make[0]: *** [Makefile:224:/task/haproxy-modsecurity-binding-self-test] Error 2",
                "build-modsecurity-binding",
            ),
            ("make: *** [Makefile:198:/task/haproxy-modsecurity-spoa] Error 2", "build-spoa-runtime"),
        )

        for footer, expected_target in cases:
            with self.subTest(footer=footer):
                proc = subprocess.CompletedProcess(
                    args=["make"], returncode=2, stdout="", stderr=f"{footer}\n"
                )
                self.assertEqual(
                    components.haproxy_failure_target_from_footers(proc, expected_target_paths),
                    expected_target,
                )

    def test_haproxy_binding_failure_footer_rejects_malformed_or_adversarial_grammar(self) -> None:
        adversarial_prefix = "location:1:" * 2048
        footers = (
            "make[one]: *** [build-modsecurity-binding] Error 2",
            "make[１２]: *** [build-modsecurity-binding] Error 2",
            "make: *** [build-modsecurity-binding] Error ٢",
            "make: *** [build-modsecurity-binding] Error",
            "make: *** [build-modsecurity-binding] Error 2 unexpected",
            f"make: *** [{adversarial_prefix}build-modsecurity-binding Error 2",
        )

        for footer in footers:
            with self.subTest(footer=footer[:80]):
                proc = subprocess.CompletedProcess(
                    args=["make"], returncode=2, stdout="", stderr=f"{footer}\n"
                )
                self.assertIsNone(components.haproxy_failure_target_from_footers(proc))
                self.assertNotIn("target_failure=", components.haproxy_failure_diagnostic_lines(proc))

    def test_haproxy_binding_failure_footer_maps_only_the_expected_output_path(self) -> None:
        expected_target_paths = {
            "build-modsecurity-binding": "/task/build/haproxy-modsecurity-binding/"
            "haproxy-modsecurity-binding-self-test",
            "build-spoa-runtime": "/task/build/haproxy-spoa-runtime/haproxy-modsecurity-spoa",
        }
        proc = subprocess.CompletedProcess(
            args=["make"],
            returncode=2,
            stdout="",
            stderr=(
                "make: *** [Makefile:224: /task/build/haproxy-modsecurity-binding/"
                "haproxy-modsecurity-binding-self-test] Error 2\n"
            ),
        )
        spoa = subprocess.CompletedProcess(
            args=["make"],
            returncode=2,
            stdout="",
            stderr=(
                "make: *** [Makefile:198: /task/build/haproxy-spoa-runtime/"
                "haproxy-modsecurity-spoa] Error 2\n"
            ),
        )
        ordered = subprocess.CompletedProcess(
            args=["make"],
            returncode=2,
            stdout="",
            stderr=proc.stderr + spoa.stderr,
        )
        rejected = subprocess.CompletedProcess(
            args=["make"],
            returncode=2,
            stdout="",
            stderr=(
                "make: *** [Makefile:224: /other/build/haproxy-modsecurity-binding/"
                "haproxy-modsecurity-binding-self-test] Error 2\n"
            ),
        )

        self.assertEqual(
            components.haproxy_failure_target_from_footers(proc, expected_target_paths),
            "build-modsecurity-binding",
        )
        self.assertIn(
            "target_failure=build-modsecurity-binding",
            components.haproxy_failure_diagnostic_lines(proc, expected_target_paths),
        )
        self.assertIsNone(
            components.haproxy_failure_target_from_footers(rejected, expected_target_paths)
        )
        self.assertNotIn(
            "target_failure=",
            components.haproxy_failure_diagnostic_lines(rejected, expected_target_paths),
        )
        self.assertEqual(
            components.haproxy_failure_target_from_footers(spoa, expected_target_paths),
            "build-spoa-runtime",
        )
        self.assertEqual(
            components.haproxy_failure_target_from_footers(ordered, expected_target_paths),
            "build-modsecurity-binding",
        )

    def test_haproxy_binding_failure_footer_ignores_stdout_target_like_text(self) -> None:
        proc = subprocess.CompletedProcess(
            args=["make"],
            returncode=2,
            stdout="make: *** [Makefile:12: build-modsecurity-binding] Error 2\n",
            stderr="compiler output only\n",
        )

        self.assertIsNone(components.haproxy_failure_target_from_footers(proc))
        self.assertNotIn(
            "target_failure=",
            components.haproxy_failure_diagnostic_lines(proc),
        )

    def test_haproxy_binding_failure_footer_rejects_unallowlisted_or_hostile_target(self) -> None:
        proc = subprocess.CompletedProcess(
            args=["make"],
            returncode=2,
            stdout="make: *** [Makefile:11: build-spoa-runtime] Error 2\n",
            stderr=(
                "make: *** [Makefile:12: not-allowlisted] Error 2\n"
                "make: *** [Makefile:13: build-modsecurity-binding; touch /tmp/pwned] Error 2\n"
            ),
        )

        self.assertIsNone(components.haproxy_failure_target_from_footers(proc))
        self.assertNotIn(
            "target_failure=",
            components.haproxy_failure_diagnostic_lines(proc),
        )

    def test_haproxy_binding_failure_footer_keeps_failed_status_exit_and_safe_summary(self) -> None:
        record, diagnostic, _ = self.prepare_haproxy_binding_failure_with(
            17,
            "make: *** [Makefile:24: build-modsecurity-binding] Error 2\n"
            "Authorization: Bearer hidden\n",
        )

        self.assertEqual(record["status"], "failed")
        self.assertEqual(record["build_exit_code"], 17)
        self.assertIn("target_failure=build-modsecurity-binding", diagnostic)
        self.assertNotIn("Makefile:24", diagnostic)
        self.assertNotIn("hidden", diagnostic)

    def test_haproxy_missing_prerequisite_remains_blocked(self) -> None:
        record = self.prepare_haproxy_with(
            77,
            "haproxy_prepare: blocked missing required command for build HAProxy: make\n",
        )
        self.assertEqual(record["status"], "blocked")
        self.assertNotIn("build_exit_code", record)

    def haproxy_prepare_framework_root(self) -> Path:
        configured_root = os.environ.get("MODSECURITY_FRAMEWORK_TEST_ROOT")
        framework_root = (
            Path(configured_root)
            if configured_root
            else ROOT / "modules" / "ModSecurity-test-Framework"
        )
        trusted_root, error = trusted_framework_root(ROOT, framework_root)
        if trusted_root is None:
            self.skipTest(error)
        script = trusted_root / "ci" / "provisioning" / "prepare-haproxy-runtime.sh"
        if not script.is_file():
            self.fail(
                "HAProxy prepare framework source is unavailable; initialize the checked-out "
                "submodule or set MODSECURITY_FRAMEWORK_TEST_ROOT to a reviewed read-only source"
            )
        return trusted_root

    def haproxy_prepare_enforces_split_build_root_containment(self, framework_root: Path) -> bool:
        script = framework_root / "ci" / "provisioning" / "prepare-haproxy-runtime.sh"
        source = script.read_text(encoding="utf-8")
        return all(
            f'require_under_build_root "${name}" {name}' in source
            for name in (
                "HAPROXY_RUNTIME_BUILD_DIR",
                "HAPROXY_RUNTIME_BUILD_WORKTREE",
                "HAPROXY_RUNTIME_DIR",
                "HAPROXY_BIN",
            )
        )

    def haproxy_prepare_framework_revision(self, framework_root: Path) -> str:
        result = subprocess.run(
            ["git", "-C", str(framework_root), "rev-parse", "HEAD"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        revision = result.stdout.strip()
        if result.returncode != 0 or len(revision) != 40:
            self.fail(
                "HAProxy prepare Framework source must expose a checked-out revision for "
                f"the split-BUILD_ROOT containment control: {result.stderr}"
            )
        return revision

    def managed_haproxy_cache_environment(
        self,
        root: Path,
        *,
        managed: bool,
        separate_build_root: bool = False,
        haproxy_version: str = TEST_HAPROXY_LOCKED_VERSION,
        haproxy_source_url: str = TEST_HAPROXY_LOCKED_SOURCE_URL,
        haproxy_sha256: str = TEST_HAPROXY_LOCKED_SHA256,
    ) -> dict[str, str]:
        cache_root = root / "cache-v2" / "shared"
        cache_root.mkdir(parents=True)
        identity = {
            "cache_schema_version": 2,
            "component": "haproxy",
            "configuration_flags": {},
        }
        cache_key = hashlib.sha256(
            json.dumps(identity, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        identity["cache_key"] = cache_key
        entry = cache_root / "builds" / "connectors" / "haproxy" / cache_key
        runtime_build = entry / "haproxy-runtime-build"
        runtime_worktree = runtime_build / "worktree"
        runtime_dir = entry / "haproxy-runtime" / "haproxy"
        binary = runtime_dir / "sbin" / "haproxy"
        runtime_worktree.mkdir(parents=True)
        binary.parent.mkdir(parents=True)
        binary.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        binary.chmod(0o755)
        binary_sha256 = hashlib.sha256(binary.read_bytes()).hexdigest()
        (runtime_dir / "haproxy.provenance").write_text(
            "\n".join(
                (
                    f"haproxy_version={haproxy_version}",
                    f"haproxy_source_url={haproxy_source_url}",
                    f"haproxy_sha256={haproxy_sha256}",
                    f"haproxy_binary_sha256={binary_sha256}",
                    "",
                )
            ),
            encoding="utf-8",
        )
        (entry / "manifest.json").write_text(
            json.dumps(
                {
                    "status": "complete",
                    "cache_schema_version": 2,
                    "connector": "haproxy",
                    "build_root": str(entry),
                    "connector_build_id": cache_key,
                    "cache_key": cache_key,
                    "cache_identity": identity,
                },
                sort_keys=True,
            ),
            encoding="utf-8",
        )

        if managed:
            (cache_root / ".msconnector-runtime-cache-root.json").write_text(
                json.dumps(
                    {
                        "kind": "msconnector-runtime-cache-root",
                        "schema_version": 2,
                        "cache_root": str(cache_root),
                    },
                    sort_keys=True,
                ),
                encoding="utf-8",
            )
            marker_key = hashlib.sha256(
                json.dumps({"entry_path": str(entry)}, sort_keys=True, separators=(",", ":")).encode("utf-8")
            ).hexdigest()
            marker_dir = cache_root / ".msconnector-runtime-cache-entries"
            marker_dir.mkdir()
            (marker_dir / f"{marker_key}.json").write_text(
                json.dumps(
                    {
                        "kind": "msconnector-runtime-cache-entry",
                        "schema_version": 2,
                        "cache_root": str(cache_root),
                        "entry_path": str(entry),
                        "component": "connector:haproxy",
                        "cache_key": cache_key,
                        "cache_identity": identity,
                        "status": "complete",
                    },
                    sort_keys=True,
                ),
                encoding="utf-8",
            )

        build_root = root / "connector-run" / "build" if separate_build_root else entry
        return {
            "CONNECTOR_ROOT": str(ROOT),
            "FRAMEWORK_ROOT": str(self.haproxy_prepare_framework_root()),
            "VERIFIED_RUN_ROOT": str(root / "connector-run"),
            "CACHE_ROOT": str(cache_root.parent),
            "VERIFIED_COMPONENT_CACHE": str(cache_root),
            "CONNECTOR_COMPONENT_CACHE": str(cache_root),
            "SOURCE_ROOT": str(cache_root / "sources"),
            "BUILD_ROOT": str(build_root),
            "TMP_ROOT": str(build_root / "tmp"),
            "LOG_ROOT": str(build_root / "logs"),
            "LOG_DIR": str(build_root / "logs" / "haproxy-prepare"),
            "HAPROXY_SOURCE_ROOT": str(cache_root / "sources" / "haproxy"),
            "HAPROXY_DOWNLOAD_DIR": str(cache_root / "archives" / "haproxy"),
            "HAPROXY_VERSION": haproxy_version,
            "HAPROXY_SOURCE_URL": haproxy_source_url,
            "HAPROXY_SHA256_URL": f"{haproxy_source_url}.sha256",
            "HAPROXY_SHA256": haproxy_sha256,
            "HAPROXY_SOURCE_DIR": str(cache_root / "sources" / "haproxy" / f"haproxy-{haproxy_version}"),
            "HAPROXY_RUNTIME_BUILD_DIR": str(runtime_build),
            "HAPROXY_RUNTIME_BUILD_WORKTREE": str(runtime_worktree),
            "HAPROXY_RUNTIME_DIR": str(runtime_dir),
            "HAPROXY_BIN": str(binary),
            "PYTHON": sys.executable,
        }

    def run_haproxy_prepare_with_shared_cache(self, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
        framework_root = Path(env["FRAMEWORK_ROOT"])
        return subprocess.run(
            ["sh", str(framework_root / "ci" / "provisioning" / "prepare-haproxy-runtime.sh")],
            cwd=ROOT,
            env={**os.environ, **env},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def test_haproxy_prepare_reuses_complete_managed_shared_cache_entry(self) -> None:
        with tempfile.TemporaryDirectory(prefix="haproxy-managed-cache-") as temporary:
            result = self.run_haproxy_prepare_with_shared_cache(
                self.managed_haproxy_cache_environment(Path(temporary), managed=True)
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("ready existing provenance-verified binary", result.stdout)

    def test_haproxy_prepare_reuses_complete_entry_without_cache_marker(self) -> None:
        with tempfile.TemporaryDirectory(prefix="haproxy-unmanaged-cache-") as temporary:
            result = self.run_haproxy_prepare_with_shared_cache(
                self.managed_haproxy_cache_environment(Path(temporary), managed=False)
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("ready existing provenance-verified binary", result.stdout)

    def test_haproxy_prepare_does_not_rebuild_a_verified_runtime_binary(self) -> None:
        with tempfile.TemporaryDirectory(prefix="haproxy-verified-runtime-") as temporary:
            env = self.managed_haproxy_cache_environment(Path(temporary), managed=True)
            result = self.run_haproxy_prepare_with_shared_cache(env)
            self.assertFalse((Path(env["HAPROXY_RUNTIME_BUILD_WORKTREE"]) / "Makefile").exists())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("ready existing provenance-verified binary", result.stdout)

    def test_haproxy_prepare_rejects_unapproved_future_provenance_before_runtime_lock(self) -> None:
        with tempfile.TemporaryDirectory(prefix="haproxy-future-pin-") as temporary:
            env = self.managed_haproxy_cache_environment(
                Path(temporary),
                managed=True,
                haproxy_version=TEST_HAPROXY_UNAPPROVED_FUTURE_VERSION,
                haproxy_source_url=TEST_HAPROXY_UNAPPROVED_FUTURE_SOURCE_URL,
                haproxy_sha256=TEST_HAPROXY_UNAPPROVED_FUTURE_SHA256,
            )
            result = self.run_haproxy_prepare_with_shared_cache(env)
            self.assertEqual(env["HAPROXY_VERSION"], TEST_HAPROXY_UNAPPROVED_FUTURE_VERSION)
            self.assertEqual(env["HAPROXY_SOURCE_URL"], TEST_HAPROXY_UNAPPROVED_FUTURE_SOURCE_URL)
            self.assertEqual(env["HAPROXY_SHA256"], TEST_HAPROXY_UNAPPROVED_FUTURE_SHA256)
            self.assertEqual(
                Path(env["HAPROXY_SOURCE_DIR"]).name,
                f"haproxy-{TEST_HAPROXY_UNAPPROVED_FUTURE_VERSION}",
            )
        self.assertEqual(result.returncode, 77, result.stdout + result.stderr)
        self.assertIn(
            "BLOCKED: HAPROXY_VERSION override is not permitted",
            result.stdout + result.stderr,
        )
        self.assertNotIn("runtime-component-lock:", result.stdout + result.stderr)

    def test_haproxy_prepare_rejects_shared_cache_runtime_with_separate_build_root(self) -> None:
        framework_root = self.haproxy_prepare_framework_root()
        if not self.haproxy_prepare_enforces_split_build_root_containment(framework_root):
            revision = self.haproxy_prepare_framework_revision(framework_root)
            if revision == LEGACY_FRAMEWORK_HAPROXY_CACHE_SHA:
                self.skipTest(
                    "the current Parent gitlink predates the candidate split-BUILD_ROOT containment "
                    "control; the Update submodules candidate must exercise this negative control"
                )
            self.fail(
                "selected Framework revision lacks required split-BUILD_ROOT HAProxy containment: "
                f"{revision}"
            )
        with tempfile.TemporaryDirectory(prefix="haproxy-split-build-root-") as temporary:
            env = self.managed_haproxy_cache_environment(
                Path(temporary),
                managed=True,
                separate_build_root=True,
            )
            result = self.run_haproxy_prepare_with_shared_cache(env)
        self.assertEqual(result.returncode, 77, result.stdout + result.stderr)
        self.assertIn(
            "HAPROXY_RUNTIME_BUILD_DIR must be under BUILD_ROOT",
            result.stdout + result.stderr,
        )


if __name__ == "__main__":
    unittest.main()
