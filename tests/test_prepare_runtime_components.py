from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
LEGACY_FRAMEWORK_HAPROXY_CACHE_SHA = "784977615acfc55567e37b863309abc4a38ac877"
PINNED_EXPAT_COMMIT = "c61098da494eea1cbd091118118dcee417faacea"
sys.path.insert(0, str(ROOT / "ci" / "provisioning" / "components"))
SPEC = importlib.util.spec_from_file_location(
    "prepare_runtime_components", ROOT / "ci/provisioning/components/prepare-runtime-components.py"
)
assert SPEC is not None and SPEC.loader is not None
components = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(components)


class PrepareRuntimeComponentsTest(unittest.TestCase):
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
            "apache_connector_build_failed",
            components.map_apache_blocker(compiler_error, ["module_file:/cache/module.so"]),
        )

    def test_apache_blocker_detects_a_real_missing_expat_header(self) -> None:
        compiler_error = "src/parser.c:7:10: fatal error: expat.h: No such file or directory\n"

        self.assertEqual(
            "missing_expat_headers",
            components.map_apache_blocker(compiler_error, []),
        )

    def test_nginx_blocker_reports_connector_compile_error_before_missing_outputs(self) -> None:
        compiler_error = "src/module.c:123:28: error: field 'phase' has incomplete type\n"

        self.assertEqual(
            "nginx_connector_build_failed",
            components.map_nginx_blocker(compiler_error, ["module_file:/cache/module.so"]),
        )

    def prepare_haproxy_with(self, returncode: int, output: str) -> dict[str, object]:
        with tempfile.TemporaryDirectory(prefix="haproxy-prepare-") as temporary:
            base = Path(temporary)
            cache = base / "cache"
            components.ensure_managed_cache_root(cache)
            build = base / "build"
            sources = cache / "sources"
            archives = cache / "archives"
            connector_build = cache / "builds/connectors/haproxy/test-build"
            plan = {
                "connector": "haproxy",
                "connector_build_id": "test-build",
                "cache_key": "test-build",
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
            self.assertFalse(any(path.name.startswith(".test-build.tmp-") for path in connector_build.parent.iterdir()))
            return record

    def test_haproxy_build_failure_returning_77_is_execution_failure(self) -> None:
        record = self.prepare_haproxy_with(
            77,
            "haproxy_prepare: running haproxy-build\n"
            "haproxy_prepare: blocked command failed: make\n",
        )
        self.assertEqual("failed", record["status"])
        self.assertEqual(77, record["build_exit_code"])

    def test_haproxy_missing_prerequisite_remains_blocked(self) -> None:
        record = self.prepare_haproxy_with(
            77,
            "haproxy_prepare: blocked missing required command for build HAProxy: make\n",
        )
        self.assertEqual("blocked", record["status"])
        self.assertNotIn("build_exit_code", record)

    def haproxy_prepare_framework_root(self) -> Path:
        configured_root = os.environ.get("MODSECURITY_FRAMEWORK_TEST_ROOT")
        framework_root = (
            Path(configured_root)
            if configured_root
            else ROOT / "modules" / "ModSecurity-test-Framework"
        )
        script = framework_root / "ci" / "provisioning" / "prepare-haproxy-runtime.sh"
        if not script.is_file():
            self.fail(
                "HAProxy prepare framework source is unavailable; initialize the checked-out "
                "submodule or set MODSECURITY_FRAMEWORK_TEST_ROOT to a reviewed read-only source"
            )
        return framework_root

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
        (runtime_dir / "haproxy.provenance").write_text(
            "\n".join(
                (
                    "haproxy_version=3.2.21",
                    "haproxy_source_url=https://www.haproxy.org/download/3.2/src/haproxy-3.2.21.tar.gz",
                    "haproxy_sha256=0cb8818a26c5f888e0cb1c40f1b3acb9fb952527d1733f769ce688fedd680339",
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
            "HAPROXY_SOURCE_DIR": str(cache_root / "sources" / "haproxy" / "haproxy-3.2.21"),
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
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("ready existing provenance-verified binary", result.stdout)

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
        self.assertEqual(77, result.returncode, result.stdout + result.stderr)
        self.assertIn(
            "HAPROXY_RUNTIME_BUILD_DIR must be under BUILD_ROOT",
            result.stdout + result.stderr,
        )


if __name__ == "__main__":
    unittest.main()
