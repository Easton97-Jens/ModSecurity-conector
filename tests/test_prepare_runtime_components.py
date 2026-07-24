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

            self.assertEqual("blocked", record["status"])
            self.assertEqual("modsecurity_v3_provenance_guard_failed", record["blocker_reason"])
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

            self.assertEqual("blocked", record["status"])
            self.assertEqual("missing_modsecurity_dependency", record["blocker_reason"])
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

            self.assertEqual("passed", result["status"])
            run_env.assert_called_once()
            command = run_env.call_args.args[0]
            self.assertEqual(
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
                command,
            )
            self.assertEqual(framework_root, run_env.call_args.kwargs["cwd"])
            self.assertEqual(str(source), run_env.call_args.kwargs["env"]["MODSECURITY_V3_SOURCE_DIR"])
            self.assertEqual(
                components._TRUSTED_FRAMEWORK_GUARD_PATH,
                run_env.call_args.kwargs["env"]["PATH"],
            )
            self.assertNotIn("ENV", run_env.call_args.kwargs["env"])
            self.assertNotIn("BASH_ENV", run_env.call_args.kwargs["env"])

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
            ), mock.patch.object(components, "prepare_git_component") as prepare_git:
                record = components.prepare_framework_approved_modsecurity_v3_source(
                    {
                        "MODSECURITY_V3_GIT_URL": "https://github.com/example/unapproved",
                        "MODSECURITY_V3_GIT_REF": "mutable-ref",
                    },
                    root / "framework",
                    root / "source",
                    {},
                    strict=True,
                    cache_root=root / "cache",
                )

            self.assertEqual("blocked", record["status"])
            self.assertEqual("modsecurity_v3_provenance_configuration_failed", record["blocker_reason"])
            self.assertEqual(expected_configuration, record["provenance_configuration"])
            prepare_git.assert_not_called()

    def test_modsecurity_source_configuration_guard_passes_verified_values_to_git_preparation(self) -> None:
        with tempfile.TemporaryDirectory(prefix="modsecurity-provenance-guard-") as temporary:
            root = Path(temporary)
            source_record = {"name": "modsecurity-v3", "status": "present"}
            with mock.patch.object(
                components,
                "verify_framework_approved_modsecurity_v3_provenance",
                return_value={"status": "passed"},
            ), mock.patch.object(components, "prepare_git_component", return_value=source_record) as prepare_git:
                record = components.prepare_framework_approved_modsecurity_v3_source(
                    {
                        "MODSECURITY_V3_GIT_URL": "https://github.com/owasp-modsecurity/ModSecurity.git",
                        "MODSECURITY_V3_GIT_REF": "v3.0.15",
                    },
                    root / "framework",
                    root / "source",
                    {"modsecurity-v3": {"status": "present"}},
                    strict=True,
                    cache_root=root / "cache",
                )

            prepare_git.assert_called_once_with(
                "modsecurity-v3",
                "https://github.com/owasp-modsecurity/ModSecurity.git",
                "v3.0.15",
                root / "source",
                {"modsecurity-v3": {"status": "present"}},
                True,
                cache_root=root / "cache",
            )
            self.assertEqual("passed", record["provenance_configuration"]["status"])

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
