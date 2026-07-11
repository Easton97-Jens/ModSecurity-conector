from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))
SPEC = importlib.util.spec_from_file_location(
    "prepare_runtime_components", ROOT / "ci/prepare-runtime-components.py"
)
assert SPEC is not None and SPEC.loader is not None
components = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(components)


class RuntimeComponentCacheContractTest(unittest.TestCase):
    def identity(
        self,
        *,
        architecture: str = "x86_64",
        patchset: str = "patch-a",
        flags: str = "-O2",
        compiler_version: str = "cc 14",
    ) -> dict:
        return components.canonical_cache_identity(
            "nginx",
            env={"TARGET_ARCHITECTURE": architecture},
            upstream_url="https://example.invalid/nginx",
            upstream_version="1.31.2",
            upstream_commit="deadbeef",
            source_sha256="source-a",
            patchset_sha256=patchset,
            configuration_flags={"CFLAGS": flags},
            toolchain={"cc": "cc", "cc_version": compiler_version},
        )

    def test_canonical_identity_covers_schema_patchset_toolchain_architecture_and_flags(self) -> None:
        baseline = self.identity()
        self.assertEqual(baseline, self.identity())
        self.assertNotEqual(baseline["cache_key"], self.identity(patchset="patch-b")["cache_key"])
        self.assertNotEqual(baseline["cache_key"], self.identity(architecture="aarch64")["cache_key"])
        self.assertNotEqual(baseline["cache_key"], self.identity(flags="-O3")["cache_key"])
        self.assertNotEqual(baseline["cache_key"], self.identity(compiler_version="cc 15")["cache_key"])
        self.assertEqual(components.CACHE_SCHEMA_VERSION, baseline["cache_schema_version"])
        self.assertEqual("patch-a", baseline["patchset_sha256"])

    def test_patchset_hash_tracks_patch_names_order_and_contents(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-cache-contract-") as temporary:
            patches = Path(temporary) / "patches"
            patches.mkdir()
            (patches / "001-first.patch").write_text("first\n", encoding="utf-8")
            (patches / "002-second.patch").write_text("second\n", encoding="utf-8")
            first = components.patchset_identity([patches])
            self.assertEqual(["001-first.patch", "002-second.patch"], first["files"])

            (patches / "001-first.patch").write_text("second\n", encoding="utf-8")
            (patches / "002-second.patch").write_text("first\n", encoding="utf-8")
            self.assertNotEqual(first["sha256"], components.patchset_identity([patches])["sha256"])

    def test_haproxy_htx_overlay_is_an_identity_input(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-cache-contract-") as temporary:
            connector_root = Path(temporary) / "connector"
            overlay = connector_root / "connectors/haproxy/htx-overlay"
            overlay.mkdir(parents=True)
            source = overlay / "haproxy_modsecurity_htx_filter.c"
            source.write_text("first\n", encoding="utf-8")
            roots = components.component_patchset_roots(connector_root, "haproxy")
            first = components.patchset_identity(roots)
            self.assertIn("haproxy_modsecurity_htx_filter.c", first["files"])
            source.write_text("second\n", encoding="utf-8")
            self.assertNotEqual(first["sha256"], components.patchset_identity(roots)["sha256"])

    def test_complete_manifest_is_required_for_a_cache_hit(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-cache-contract-") as temporary:
            cache_root = components.ensure_managed_cache_root(Path(temporary) / "cache")
            identity = self.identity()
            manifest_path = cache_root / "builds/nginx/cache-key/manifest.json"
            record = {
                "component": "nginx",
                "status": "built",
                "cache_schema_version": components.CACHE_SCHEMA_VERSION,
                "cache_identity": identity,
                "cache_key": identity["cache_key"],
            }
            components.write_cache_manifest(manifest_path, record)
            self.assertTrue(components.cache_manifest_complete(manifest_path, identity))

            incomplete = components.read_json(manifest_path)
            incomplete["status"] = "incomplete"
            components.write_json(manifest_path, incomplete)
            self.assertFalse(components.cache_manifest_complete(manifest_path, identity))

            components.write_cache_manifest(manifest_path, record)
            different_identity = self.identity(patchset="patch-b")
            self.assertFalse(components.cache_manifest_complete(manifest_path, different_identity))

    def test_connector_manifest_reuse_requires_complete_matching_contract(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-cache-contract-") as temporary:
            root = Path(temporary)
            connector_root = root / "connector"
            framework_root = root / "framework"
            cache_root = components.ensure_managed_cache_root(root / "cache")
            (connector_root / "connectors/apache").mkdir(parents=True)
            (connector_root / "common/include").mkdir(parents=True)
            (connector_root / "common/src").mkdir(parents=True)
            (framework_root / "ci").mkdir(parents=True)
            (connector_root / "connectors/apache/input.c").write_text("int x;\n", encoding="utf-8")
            (framework_root / "ci/prepare-apache-build.sh").write_text("#!/bin/sh\n", encoding="utf-8")
            with mock.patch.object(
                components,
                "compiler_identity",
                return_value={"cc": "/usr/bin/cc", "cc_version": "cc test", "cxx": "", "cxx_version": ""},
            ), mock.patch.object(components, "hash_input_paths", return_value="source-hash"):
                plan = components.connector_plan(
                    connector_root,
                    framework_root,
                    cache_root,
                    {"HTTPD_VERSION": "2.4.68"},
                    "apache",
                    {"build_id": "modsecurity-build", "prefix": "/cache/modsecurity"},
                    {"build_id": "expat-build", "prefix": "/cache/expat"},
                    [],
                )
            self.assertFalse(components.connector_manifest_ready(plan))
            components.write_connector_manifest(plan, {"status": "built", "output_paths": plan["output_paths"]})
            # A complete local manifest alone is not a cache hit.  The
            # registry-side completion marker is published only after the
            # staged entry is atomically moved into place.
            self.assertTrue(components.connector_manifest_contract_ready(plan))
            self.assertFalse(components.connector_manifest_ready(plan))
            components.write_cache_entry_completion(
                Path(plan["root"]),
                cache_root,
                component="connector:apache",
                cache_key=plan["cache_key"],
                cache_identity=plan["cache_identity"],
            )
            self.assertTrue(components.connector_manifest_ready(plan))

            manifest = components.read_json(Path(plan["manifest"]))
            self.assertEqual("complete", manifest["status"])
            manifest["status"] = "incomplete"
            components.write_json(Path(plan["manifest"]), manifest)
            self.assertFalse(components.connector_manifest_ready(plan))

    def test_connector_plan_reuses_complete_entry_when_only_root_commit_changes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-cache-contract-") as temporary:
            root = Path(temporary)
            connector_root = root / "connector"
            framework_root = root / "framework"
            cache_root = components.ensure_managed_cache_root(root / "cache")
            (connector_root / "connectors/nginx").mkdir(parents=True)
            (connector_root / "common/include").mkdir(parents=True)
            (connector_root / "common/src").mkdir(parents=True)
            (framework_root / "ci").mkdir(parents=True)
            (connector_root / "connectors/nginx/input.c").write_text("int x;\n", encoding="utf-8")
            (framework_root / "ci/prepare-nginx-build.sh").write_text("#!/bin/sh\n", encoding="utf-8")
            compiler = mock.patch.object(
                components,
                "compiler_identity",
                return_value={"cc": "/usr/bin/cc", "cc_version": "cc test", "cxx": "", "cxx_version": ""},
            )
            source_hash = mock.patch.object(components, "hash_input_paths", return_value="source-hash")
            revisions = mock.patch.object(
                components,
                "git_revision",
                side_effect=lambda path: "current-root" if path == connector_root else "framework-root",
            )
            with compiler, source_hash, revisions:
                requested_plan = components.connector_plan(
                    connector_root,
                    framework_root,
                    cache_root,
                    {"NGINX_RELEASE_TAG": "v1.31.2"},
                    "nginx",
                    {"build_id": "modsecurity-build", "prefix": "/cache/modsecurity"},
                    {"build_id": "expat-build", "prefix": "/cache/expat"},
                    [],
                )

            candidate_identity = json.loads(json.dumps(requested_plan["cache_identity"]))
            candidate_identity["extra_inputs"]["connector_commit"] = "previous-root"
            candidate_payload = dict(candidate_identity)
            candidate_payload.pop("cache_key", None)
            candidate_identity["cache_key"] = components.stable_hash(candidate_payload)
            candidate_root = cache_root / "builds/connectors/nginx" / candidate_identity["cache_key"]
            candidate_plan = components.staged_connector_plan(requested_plan, candidate_root)
            candidate_plan.update(
                connector_build_id=candidate_identity["cache_key"],
                cache_identity=candidate_identity,
                cache_key=candidate_identity["cache_key"],
            )
            components.mark_managed_cache_entry(
                candidate_root,
                cache_root,
                component="connector:nginx",
                cache_key=candidate_plan["cache_key"],
            )
            binary = Path(candidate_plan["output_paths"]["binary"])
            module = Path(candidate_plan["output_paths"]["module"])
            config = Path(candidate_plan["output_paths"]["config"])
            binary.parent.mkdir(parents=True)
            binary.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            binary.chmod(0o755)
            module.parent.mkdir(parents=True)
            module.write_text("module\n", encoding="utf-8")
            config.parent.mkdir(parents=True)
            config.write_text("events {}\n", encoding="utf-8")
            components.write_connector_manifest(
                candidate_plan,
                {"status": "built", "output_paths": candidate_plan["output_paths"]},
            )
            components.write_cache_entry_completion(
                candidate_root,
                cache_root,
                component="connector:nginx",
                cache_key=candidate_plan["cache_key"],
                cache_identity=candidate_identity,
            )

            with compiler, source_hash, revisions:
                reused_plan = components.connector_plan(
                    connector_root,
                    framework_root,
                    cache_root,
                    {"NGINX_RELEASE_TAG": "v1.31.2"},
                    "nginx",
                    {"build_id": "modsecurity-build", "prefix": "/cache/modsecurity"},
                    {"build_id": "expat-build", "prefix": "/cache/expat"},
                    [],
                )
            self.assertEqual(str(candidate_root), reused_plan["root"])
            self.assertEqual(candidate_identity["cache_key"], reused_plan["cache_key"])
            self.assertEqual("previous-root", reused_plan["reused_from_connector_commit"])
            self.assertEqual("connector_commit_only", reused_plan["cache_reuse_reason"])
            self.assertTrue(components.connector_cache_entry_complete(reused_plan))

            components.remove_managed_cache_entry_marker(candidate_root, cache_root)
            with compiler, source_hash, revisions:
                rejected_plan = components.connector_plan(
                    connector_root,
                    framework_root,
                    cache_root,
                    {"NGINX_RELEASE_TAG": "v1.31.2"},
                    "nginx",
                    {"build_id": "modsecurity-build", "prefix": "/cache/modsecurity"},
                    {"build_id": "expat-build", "prefix": "/cache/expat"},
                    [],
                )
            self.assertEqual(requested_plan["root"], rejected_plan["root"])

            changed_identity = json.loads(json.dumps(candidate_identity))
            changed_identity["extra_inputs"]["connector_source_hash"] = "different-source-hash"
            changed_payload = dict(changed_identity)
            changed_payload.pop("cache_key", None)
            changed_identity["cache_key"] = components.stable_hash(changed_payload)
            self.assertFalse(
                components.connector_cache_identity_equivalent_ignoring_connector_commit(
                    changed_identity,
                    requested_plan["cache_identity"],
                )
            )
            tampered_identity = json.loads(json.dumps(candidate_identity))
            tampered_identity["cache_key"] = "not-the-derived-key"
            self.assertFalse(
                components.connector_cache_identity_equivalent_ignoring_connector_commit(
                    tampered_identity,
                    requested_plan["cache_identity"],
                )
            )

    def test_safe_remove_refuses_root_outside_and_protected_paths(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-cache-contract-") as temporary:
            root = Path(temporary)
            cache_root = components.ensure_managed_cache_root(root / "cache")
            removable = cache_root / "builds/nginx/cache-key"
            removable.mkdir(parents=True)
            (removable / "artifact").write_text("ok\n", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "unmanaged_cache_entry_marker_missing"):
                components.safe_remove_dir(removable, cache_root)
            self.assertTrue(removable.exists())
            with self.assertRaisesRegex(RuntimeError, "unmanaged_cache_entry_marker_missing"):
                components.mark_managed_cache_entry(
                    removable,
                    cache_root,
                    component="test:nginx",
                    cache_key="cache-key",
                )

            planned_removal = cache_root / "builds/nginx/planned-cache-key"
            components.mark_managed_cache_entry(
                planned_removal,
                cache_root,
                component="test:nginx",
                cache_key="planned-cache-key",
            )
            planned_removal.mkdir(parents=True)
            (planned_removal / "artifact").write_text("ok\n", encoding="utf-8")
            components.safe_remove_dir(planned_removal, cache_root)
            self.assertFalse(planned_removal.exists())

            removable_file = cache_root / "archives/nginx/archive.tar.gz"
            removable_file.parent.mkdir(parents=True)
            removable_file.write_text("archive\n", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "unmanaged_cache_entry_marker_missing"):
                components.safe_remove_file(removable_file, cache_root)
            with self.assertRaisesRegex(RuntimeError, "unmanaged_cache_entry_marker_missing"):
                components.mark_managed_cache_entry(
                    removable_file,
                    cache_root,
                    component="test:archive",
                    cache_key="archive-key",
                )

            planned_file = cache_root / "archives/nginx/planned.tar.gz"
            components.mark_managed_cache_entry(
                planned_file,
                cache_root,
                component="test:archive",
                cache_key="planned-archive-key",
            )
            planned_file.write_text("archive\n", encoding="utf-8")
            components.safe_remove_file(planned_file, cache_root)
            self.assertFalse(planned_file.exists())

            with self.assertRaisesRegex(RuntimeError, "unsafe_remove_path_forbidden"):
                components.safe_remove_dir(cache_root, cache_root)
            with self.assertRaisesRegex(RuntimeError, "unsafe_remove_path_forbidden"):
                components.safe_remove_dir(root / "outside", cache_root)
            with self.assertRaisesRegex(RuntimeError, "unsafe_remove_path_forbidden"):
                components.safe_remove_dir(ROOT, cache_root)
            with self.assertRaisesRegex(RuntimeError, "unsafe_remove_path_forbidden"):
                components.safe_remove_dir(ROOT / "modules/ModSecurity-test-Framework", cache_root)

            protected = cache_root / "simulated-superproject"
            protected.mkdir()
            with self.assertRaisesRegex(RuntimeError, "unsafe_remove_path_forbidden"):
                components.safe_remove_dir(protected, cache_root, protected_paths=(protected,))
            self.assertTrue(protected.exists())

    def test_complete_identity_bound_manifest_can_authorize_an_entry_but_incomplete_cannot(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-cache-contract-") as temporary:
            cache_root = components.ensure_managed_cache_root(Path(temporary) / "cache")
            identity = self.identity()
            entry = cache_root / "builds/nginx" / identity["cache_key"]
            entry.mkdir(parents=True)
            components.write_cache_manifest(
                entry / "manifest.json",
                {
                    "component": "nginx",
                    "status": "built",
                    "cache_schema_version": components.CACHE_SCHEMA_VERSION,
                    "cache_identity": identity,
                    "cache_key": identity["cache_key"],
                },
            )
            self.assertTrue(components.cache_manifest_owns_entry(entry))
            with self.assertRaisesRegex(RuntimeError, "managed_cache_entry_requires_rebuild"):
                components.mark_managed_cache_entry(
                    entry,
                    cache_root,
                    component="connector:nginx",
                    cache_key=identity["cache_key"],
                )
            components.safe_remove_dir(entry, cache_root)
            self.assertFalse(entry.exists())

            incomplete = cache_root / "builds/nginx/incomplete"
            incomplete.mkdir(parents=True)
            components.write_cache_manifest(
                incomplete / "manifest.json",
                {
                    "component": "nginx",
                    "status": "blocked",
                    "cache_schema_version": components.CACHE_SCHEMA_VERSION,
                    "cache_identity": identity,
                    "cache_key": identity["cache_key"],
                },
            )
            self.assertFalse(components.cache_manifest_owns_entry(incomplete))
            with self.assertRaisesRegex(RuntimeError, "unmanaged_cache_entry_marker_missing"):
                components.safe_remove_dir(incomplete, cache_root)

    def test_corrupt_managed_archive_is_discarded_before_the_next_rebuild(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-cache-contract-") as temporary:
            cache_root = components.ensure_managed_cache_root(Path(temporary) / "cache")
            archive_dir = cache_root / "archives/nginx"
            archive_path = archive_dir / "nginx.tar.gz"
            archive_dir.mkdir(parents=True)
            archive_identity = components.archive_cache_identity(
                "nginx", "https://example.invalid/nginx.tar.gz", "", ""
            )
            components.mark_managed_cache_entry(
                archive_path,
                cache_root,
                component="archive:nginx",
                cache_key=archive_identity["cache_key"],
            )
            archive_path.write_text("not a tarball\n", encoding="utf-8")

            def write_corrupt_download(url: str, destination: Path) -> None:
                destination.write_text("still not a tarball\n", encoding="utf-8")

            with mock.patch.object(components, "download", side_effect=write_corrupt_download):
                record = components.prepare_archive(
                    "nginx",
                    "https://example.invalid/nginx.tar.gz",
                    "",
                    "",
                    archive_dir,
                    cache_root,
                )
            self.assertEqual("corrupt", record["status"])
            self.assertEqual("archive_list_failed", record["blocker_reason"])
            self.assertFalse(archive_path.exists())

    def test_archive_identity_change_rebuilds_a_same_basename_entry(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-cache-contract-") as temporary:
            cache_root = components.ensure_managed_cache_root(Path(temporary) / "cache")
            archive_dir = cache_root / "archives/nginx"
            archive_path = archive_dir / "nginx.tar.gz"
            archive_dir.mkdir(parents=True)
            old_url = "https://example.invalid/releases/v1/nginx.tar.gz"
            new_url = "https://example.invalid/releases/v2/nginx.tar.gz"
            old_key = components.archive_cache_identity("nginx", old_url, "", "")["cache_key"]
            components.mark_managed_cache_entry(
                archive_path,
                cache_root,
                component="archive:nginx",
                cache_key=old_key,
            )
            with tarfile.open(archive_path, "w:gz"):
                pass
            downloads: list[str] = []

            def download_new_archive(url: str, destination: Path) -> None:
                downloads.append(url)
                with tarfile.open(destination, "w:gz"):
                    pass

            with mock.patch.object(components, "download", side_effect=download_new_archive):
                record = components.prepare_archive("nginx", new_url, "", "", archive_dir, cache_root)

            new_key = components.archive_cache_identity("nginx", new_url, "", "")["cache_key"]
            self.assertEqual("present", record["status"])
            self.assertEqual([new_url], downloads)
            self.assertTrue(record["rebuild_required"])
            self.assertEqual("archive_cache_identity_changed", record["invalidation_reason"])
            self.assertEqual(new_key, components.read_json(components.cache_entry_marker_path(archive_path, cache_root))["cache_key"])

    def test_legacy_archive_marker_is_migrated_only_to_remove_and_rebuild(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-cache-contract-") as temporary:
            cache_root = components.ensure_managed_cache_root(Path(temporary) / "cache")
            archive_dir = cache_root / "archives/nginx"
            archive_path = archive_dir / "nginx.tar.gz"
            archive_dir.mkdir(parents=True)
            with tarfile.open(archive_path, "w:gz"):
                pass
            components.write_json(
                components.cache_entry_marker_path(archive_path, cache_root),
                {
                    "kind": "msconnector-runtime-cache-entry",
                    "schema_version": 1,
                    "cache_root": str(cache_root),
                    "entry_path": str(archive_path),
                    "component": "archive:nginx",
                    "cache_key": "legacy-key",
                },
            )
            downloads: list[str] = []

            def download_new_archive(url: str, destination: Path) -> None:
                downloads.append(url)
                with tarfile.open(destination, "w:gz"):
                    pass

            url = "https://example.invalid/nginx.tar.gz"
            with mock.patch.object(components, "download", side_effect=download_new_archive):
                record = components.prepare_archive("nginx", url, "", "", archive_dir, cache_root)

            identity = components.archive_cache_identity("nginx", url, "", "")
            marker = components.read_json(components.cache_entry_marker_path(archive_path, cache_root))
            self.assertEqual("present", record["status"])
            self.assertEqual([url], downloads)
            self.assertTrue(record["old_entry_removed"])
            self.assertEqual("cache_schema_changed", record["invalidation_reason"])
            self.assertEqual(components.CACHE_SCHEMA_VERSION, marker["schema_version"])
            self.assertEqual(identity["cache_key"], marker["cache_key"])
            self.assertEqual("complete", marker["status"])

    def test_blocked_modsecurity_manifest_claims_fresh_entry_before_writing(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-cache-contract-") as temporary:
            root = Path(temporary)
            cache_root = components.ensure_managed_cache_root(root / "cache")
            git_record = {"status": "blocked", "blocker_reason": "source unavailable"}
            toolchain = {"cc": "cc", "cc_version": "cc test", "cxx": "", "cxx_version": ""}
            with mock.patch.object(components, "toolchain_identity", return_value=toolchain):
                record = components.prepare_shared_modsecurity({}, cache_root, root / "work", git_record, {})
                paths = components.shared_modsecurity_paths(cache_root, record["build_id"])
            self.assertEqual("blocked", record["status"])
            self.assertTrue(paths["manifest"].is_file())
            self.assertTrue(components.cache_entry_marker_valid(paths["build_root"], cache_root))

            unmanaged_cache = components.ensure_managed_cache_root(root / "unmanaged-cache")
            with mock.patch.object(components, "toolchain_identity", return_value=toolchain):
                inputs = components.modsecurity_build_inputs({}, git_record, {})
            unmanaged_paths = components.shared_modsecurity_paths(unmanaged_cache, inputs["build_id"])
            unmanaged_paths["build_root"].mkdir(parents=True)
            with mock.patch.object(components, "toolchain_identity", return_value=toolchain):
                blocked = components.prepare_shared_modsecurity({}, unmanaged_cache, root / "work", git_record, {})
            self.assertEqual("blocked", blocked["status"])
            self.assertIn("unmanaged_cache_entry_marker_missing", blocked["blocker_reason"])
            self.assertFalse(unmanaged_paths["manifest"].exists())

    def test_modsecurity_builds_in_staging_then_publishes_complete_entries(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-cache-contract-") as temporary:
            root = Path(temporary)
            cache_root = components.ensure_managed_cache_root(root / "cache")
            source = root / "modsecurity-source"
            source.mkdir()
            (source / "build.sh").write_text("#!/bin/sh\n", encoding="utf-8")
            (source / "configure").write_text("#!/bin/sh\n", encoding="utf-8")
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
            make_calls = 0

            def fake_run_env(command: list[str], cwd: Path | None = None, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
                nonlocal make_calls
                if command and command[0] == "make":
                    make_calls += 1
                    assert cwd is not None
                    headers = cwd / "headers/modsecurity"
                    libs = cwd / "src/.libs"
                    headers.mkdir(parents=True, exist_ok=True)
                    libs.mkdir(parents=True, exist_ok=True)
                    (headers / "modsecurity.h").write_text("header\n", encoding="utf-8")
                    (libs / "libmodsecurity.so").write_text("library\n", encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, "", "")

            with mock.patch.object(components, "toolchain_identity", return_value=toolchain), mock.patch.object(
                components.shutil, "which", side_effect=lambda _name: "/usr/bin/tool"
            ), mock.patch.object(components, "run_env", side_effect=fake_run_env):
                record = components.prepare_shared_modsecurity({}, cache_root, root / "work", git_record, {})

            build_entry = cache_root / "builds/modsecurity" / record["cache_key"]
            prefix = cache_root / "prefix/modsecurity" / record["cache_key"]
            self.assertEqual("built", record["status"])
            self.assertTrue((prefix / "include/modsecurity/modsecurity.h").is_file())
            self.assertTrue(components.cache_manifest_complete(build_entry / "manifest.json", record["cache_identity"]))
            self.assertTrue(
                components.cache_entry_complete(
                    build_entry,
                    cache_root,
                    component="modsecurity-build",
                    cache_key=record["cache_key"],
                    cache_identity=record["cache_identity"],
                )
            )
            self.assertTrue(
                components.cache_entry_complete(
                    prefix,
                    cache_root,
                    component="modsecurity-prefix",
                    cache_key=record["cache_key"],
                    cache_identity=record["cache_identity"],
                )
            )
            self.assertFalse(any(path.name.startswith(f".{build_entry.name}.tmp-") for path in build_entry.parent.iterdir()))

            # Artifacts and the local manifest remain valid, but an incomplete
            # registry marker must force a fresh staged build instead of a
            # cache hit.
            marker_path = components.cache_entry_marker_path(build_entry, cache_root)
            marker = components.read_json(marker_path)
            marker["status"] = "incomplete"
            components.write_json(marker_path, marker)
            with mock.patch.object(components, "toolchain_identity", return_value=toolchain), mock.patch.object(
                components.shutil, "which", side_effect=lambda _name: "/usr/bin/tool"
            ), mock.patch.object(components, "run_env", side_effect=fake_run_env):
                rebuilt = components.prepare_shared_modsecurity({}, cache_root, root / "work", git_record, {})
            self.assertEqual("built", rebuilt["status"])
            self.assertEqual(2, make_calls)

            # A lost prefix sidecar can be recovered only because the complete
            # build manifest binds this exact prefix.  It authorizes deletion
            # and staged rebuild, not reuse of the markerless prefix.
            components.remove_managed_cache_entry_marker(prefix, cache_root)
            with mock.patch.object(components, "toolchain_identity", return_value=toolchain), mock.patch.object(
                components.shutil, "which", side_effect=lambda _name: "/usr/bin/tool"
            ), mock.patch.object(components, "run_env", side_effect=fake_run_env):
                rebuilt_prefix = components.prepare_shared_modsecurity({}, cache_root, root / "work", git_record, {})
            self.assertEqual("built", rebuilt_prefix["status"])
            self.assertEqual("missing_modsecurity_prefix_registry_marker", rebuilt_prefix["invalidation_reason"])
            self.assertEqual(3, make_calls)

    def test_default_expat_builds_in_a_keyed_staging_entry(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-cache-contract-") as temporary:
            root = Path(temporary)
            cache_root = components.ensure_managed_cache_root(root / "cache")
            source = root / "expat-source"
            source.mkdir()
            (source / "configure").write_text("#!/bin/sh\n", encoding="utf-8")
            git_record = {
                "status": "present",
                "path": str(source),
                "url": "https://github.com/example/expat",
                "expected_ref": "v2",
                "release_tag": "v2",
                "actual_head": "deadbeef",
                "submodule_status": "",
                "submodule_status_clean": True,
            }
            toolchain = {"cc": "cc", "cc_version": "cc test", "cxx": "", "cxx_version": ""}
            configured_prefix: Path | None = None

            def fake_run_env(command: list[str], cwd: Path | None = None, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
                nonlocal configured_prefix
                if command and str(command[0]).endswith("configure"):
                    configured_prefix = Path(next(item.split("=", 1)[1] for item in command if item.startswith("--prefix=")))
                if command[:2] == ["make", "install"]:
                    assert configured_prefix is not None
                    include = configured_prefix / "include"
                    lib = configured_prefix / "lib"
                    include.mkdir(parents=True, exist_ok=True)
                    lib.mkdir(parents=True, exist_ok=True)
                    (include / "expat.h").write_text("header\n", encoding="utf-8")
                    (lib / "libexpat.so").write_text("library\n", encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, "", "")

            with mock.patch.object(components, "toolchain_identity", return_value=toolchain), mock.patch.object(
                components.shutil, "which", side_effect=lambda _name: "/usr/bin/tool"
            ), mock.patch.object(components, "run_env", side_effect=fake_run_env):
                record = components.prepare_expat({}, cache_root, root / "work", git_record)

            entry = cache_root / "builds/expat" / record["cache_key"]
            self.assertEqual("built", record["status"])
            self.assertEqual(str(entry / "prefix"), record["prefix"])
            self.assertTrue((entry / "prefix/include/expat.h").is_file())
            self.assertTrue(components.cache_manifest_complete(entry / "manifest.json", record["cache_identity"]))
            self.assertTrue(
                components.cache_entry_complete(
                    entry,
                    cache_root,
                    component="expat",
                    cache_key=record["cache_key"],
                    cache_identity=record["cache_identity"],
                )
            )

    def test_expat_compiler_symlink_identity_survives_rebase_and_hits_cache(self) -> None:
        """A staging rebase must not canonicalize external toolchain paths.

        ``cc`` is commonly a symlink.  The cache key is calculated with the
        configured spelling, so rebasing the staged record must retain that
        spelling in the published manifest or the next target rejects it as a
        different identity and rebuilds Expat.
        """
        with tempfile.TemporaryDirectory(prefix="runtime-cache-contract-") as temporary:
            root = Path(temporary)
            cache_root = components.ensure_managed_cache_root(root / "cache")
            source = root / "expat-source"
            source.mkdir()
            (source / "configure").write_text("#!/bin/sh\n", encoding="utf-8")
            toolchain_root = root / "toolchain"
            toolchain_root.mkdir()
            compiler_target = toolchain_root / "compiler-15"
            compiler_target.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            compiler_target.chmod(0o755)
            compiler_link = toolchain_root / "cc"
            compiler_link.symlink_to(compiler_target)
            self.assertNotEqual(str(compiler_link), str(compiler_link.resolve()))

            git_record = {
                "status": "present",
                "path": str(source),
                "url": "https://github.com/example/expat",
                "expected_ref": "v2",
                "release_tag": "v2",
                "actual_head": "deadbeef",
                "submodule_status": "",
                "submodule_status_clean": True,
            }
            toolchain = {
                "cc": str(compiler_link),
                "cc_version": "compiler symlink test",
                "cxx": "",
                "cxx_version": "",
            }
            configured_prefix: Path | None = None
            make_install_calls = 0

            def fake_run_env(
                command: list[str],
                cwd: Path | None = None,
                env: dict[str, str] | None = None,
            ) -> subprocess.CompletedProcess[str]:
                nonlocal configured_prefix, make_install_calls
                if command and str(command[0]).endswith("configure"):
                    configured_prefix = Path(
                        next(item.split("=", 1)[1] for item in command if item.startswith("--prefix="))
                    )
                if command[:2] == ["make", "install"]:
                    make_install_calls += 1
                    assert configured_prefix is not None
                    include = configured_prefix / "include"
                    lib = configured_prefix / "lib"
                    include.mkdir(parents=True, exist_ok=True)
                    lib.mkdir(parents=True, exist_ok=True)
                    (include / "expat.h").write_text("header\n", encoding="utf-8")
                    (lib / "libexpat.so").write_text("library\n", encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, "", "")

            patches = (
                mock.patch.object(components, "toolchain_identity", return_value=toolchain),
                mock.patch.object(
                    components.shutil,
                    "which",
                    side_effect=lambda _name: "/usr/bin/tool",
                ),
                mock.patch.object(components, "run_env", side_effect=fake_run_env),
            )
            with patches[0], patches[1], patches[2]:
                first = components.prepare_expat(
                    {"CC": str(compiler_link)}, cache_root, root / "work", git_record
                )
                second = components.prepare_expat(
                    {"CC": str(compiler_link)}, cache_root, root / "work", git_record
                )

            entry = cache_root / "builds" / "expat" / first["cache_key"]
            manifest = components.read_json(entry / "manifest.json")
            self.assertEqual("built", first["status"])
            self.assertEqual("present", second["status"])
            self.assertEqual(1, make_install_calls)
            self.assertEqual(str(compiler_link), first["cache_identity"]["toolchain"]["cc"])
            self.assertEqual(first["cache_identity"], manifest["cache_identity"])
            self.assertTrue(
                components.cache_manifest_complete(entry / "manifest.json", first["cache_identity"])
            )
            self.assertTrue(
                components.cache_entry_complete(
                    entry,
                    cache_root,
                    component="expat",
                    cache_key=first["cache_key"],
                    cache_identity=first["cache_identity"],
                )
            )

    def test_managed_expat_overrides_publish_from_staging_and_external_paths_are_blocked(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-cache-contract-") as temporary:
            root = Path(temporary)
            cache_root = components.ensure_managed_cache_root(root / "cache")
            source = root / "expat-source"
            source.mkdir()
            (source / "configure").write_text("#!/bin/sh\n", encoding="utf-8")
            git_record = {
                "status": "present",
                "path": str(source),
                "url": "https://github.com/example/expat",
                "expected_ref": "v2",
                "release_tag": "v2",
                "actual_head": "deadbeef",
                "submodule_status": "",
                "submodule_status_clean": True,
            }
            toolchain = {"cc": "cc", "cc_version": "cc test", "cxx": "", "cxx_version": ""}
            configured_prefix: Path | None = None

            def fake_run_env(command: list[str], cwd: Path | None = None, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
                nonlocal configured_prefix
                if command and str(command[0]).endswith("configure"):
                    configured_prefix = Path(next(item.split("=", 1)[1] for item in command if item.startswith("--prefix=")))
                if command[:2] == ["make", "install"]:
                    assert configured_prefix is not None
                    include = configured_prefix / "include"
                    lib = configured_prefix / "lib"
                    include.mkdir(parents=True, exist_ok=True)
                    lib.mkdir(parents=True, exist_ok=True)
                    (include / "expat.h").write_text("header\n", encoding="utf-8")
                    (lib / "libexpat.so").write_text("library\n", encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, "", "")

            prefix = cache_root / "overrides/expat/prefix"
            build_dir = cache_root / "overrides/expat/build"
            source_copy = cache_root / "overrides/expat/source"
            env = {
                "EXPAT_PREFIX": str(prefix),
                "EXPAT_BUILD_DIR": str(build_dir),
                "EXPAT_SOURCE_COPY": str(source_copy),
            }
            with mock.patch.object(components, "toolchain_identity", return_value=toolchain), mock.patch.object(
                components.shutil, "which", side_effect=lambda _name: "/usr/bin/tool"
            ), mock.patch.object(components, "run_env", side_effect=fake_run_env):
                record = components.prepare_expat(env, cache_root, root / "work", git_record)

            self.assertEqual("built", record["status"])
            self.assertTrue(str(configured_prefix).split("/")[-1].startswith(".prefix.tmp-"))
            self.assertTrue((prefix / "include/expat.h").is_file())
            for component, entry in (("expat-prefix", prefix), ("expat-build", build_dir), ("expat-source", source_copy)):
                self.assertTrue(
                    components.cache_entry_complete(
                        entry,
                        cache_root,
                        component=component,
                        cache_key=record["cache_key"],
                        cache_identity=record["cache_identity"],
                    )
                )
            self.assertFalse(any(".tmp-" in path.name for path in prefix.parent.iterdir()))

            external_prefix = root / "external/expat-prefix"
            blocked = components.prepare_expat(
                {"EXPAT_PREFIX": str(external_prefix)},
                cache_root,
                root / "work",
                git_record,
            )
            self.assertEqual("blocked", blocked["status"])
            self.assertEqual("expat_paths_must_be_under_connector_component_cache", blocked["blocker_reason"])
            self.assertFalse(external_prefix.exists())

    def test_apache_rebuilds_complete_cache_with_broken_apxs(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-cache-contract-") as temporary:
            root = Path(temporary)
            cache_root = components.ensure_managed_cache_root(root / "cache")
            identity = components.canonical_cache_identity(
                "apache",
                env={},
                upstream_url="https://example.invalid/httpd",
                upstream_version="test",
                configuration_flags={},
                toolchain={"cc": "cc", "cc_version": "cc test"},
            )
            cache_key = identity["cache_key"]
            entry = cache_root / "builds/connectors/apache" / cache_key
            build_path = entry / "build"
            httpd_prefix = entry / "httpd"
            modsecurity_lib = root / "shared-modsecurity/lib/libmodsecurity.so"
            modsecurity_lib.parent.mkdir(parents=True)
            modsecurity_lib.write_text("library\n", encoding="utf-8")
            plan = {
                "connector": "apache",
                "connector_build_id": cache_key,
                "modsecurity_build_id": "modsecurity",
                "source_hash": "source-hash",
                "cache_key": cache_key,
                "cache_schema_version": components.CACHE_SCHEMA_VERSION,
                "cache_identity": identity,
                "cache_root": str(cache_root),
                "root": str(entry),
                "build_root": str(build_path),
                "httpd_prefix": str(httpd_prefix),
                "manifest": str(entry / "manifest.json"),
                "output_paths": {
                    "binary": str(httpd_prefix / "bin/httpd"),
                    "module": str(build_path / "output/apache/mod_security3.so"),
                    "config": str(httpd_prefix / "conf/httpd.conf"),
                },
            }
            components.mark_managed_cache_entry(entry, cache_root, component="connector:apache", cache_key=cache_key)
            entry.mkdir(parents=True)
            stale_httpd = httpd_prefix / "bin/httpd"
            stale_httpd.parent.mkdir(parents=True)
            stale_httpd.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            stale_httpd.chmod(0o755)
            stale_apxs = httpd_prefix / "bin/apxs"
            stale_apxs.write_text("#!/bin/sh\nexit 2\n", encoding="utf-8")
            stale_apxs.chmod(0o755)
            stale_module = build_path / "output/apache/mod_security3.so"
            stale_module.parent.mkdir(parents=True)
            stale_module.write_text("module\n", encoding="utf-8")
            stale_config = httpd_prefix / "conf/httpd.conf"
            stale_config.parent.mkdir(parents=True)
            stale_config.write_text("ServerRoot .\n", encoding="utf-8")
            components.write_connector_manifest(plan, {"status": "built", "output_paths": plan["output_paths"]})
            components.write_cache_entry_completion(
                entry,
                cache_root,
                component="connector:apache",
                cache_key=cache_key,
                cache_identity=identity,
            )
            self.assertTrue(components.connector_manifest_contract_ready(plan))
            self.assertFalse(components.connector_cache_entry_complete(plan))
            connector_root = root / "connector"
            framework_root = root / "framework"
            connector_root.mkdir()
            framework_root.mkdir()
            staging_prefixes: list[Path] = []

            def build_apache(*args: object, **_kwargs: object) -> subprocess.CompletedProcess[str]:
                self.assertFalse(stale_apxs.exists())
                build_env = args[1]
                assert isinstance(build_env, dict)
                active_build_path = Path(build_env["APACHE_BUILD_ROOT"])
                active_httpd_prefix = Path(build_env["HTTPD_PREFIX"])
                staging_prefixes.append(active_httpd_prefix)
                httpd = active_httpd_prefix / "bin/httpd"
                httpd.parent.mkdir(parents=True, exist_ok=True)
                httpd.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
                httpd.chmod(0o755)
                apxs = active_httpd_prefix / "bin/apxs"
                apxs.write_text(
                    "#!/bin/sh\n"
                    "set -eu\n"
                    "[ \"$#\" = 2 ] && [ \"$1\" = \"-q\" ] && [ \"$2\" = \"INCLUDEDIR\" ] || exit 2\n"
                    f"prefix=$(sed -n 's/^prefix = //p' '{active_httpd_prefix}/build/config_vars.mk')\n"
                    "printf '%s/include\\n' \"$prefix\"\n",
                    encoding="utf-8",
                )
                apxs.chmod(0o755)
                for name in ("apr-1-config", "apu-1-config"):
                    config_script = active_httpd_prefix / "bin" / name
                    config_script.write_text(
                        f"#!/bin/sh\nprefix='{active_httpd_prefix}'\n",
                        encoding="utf-8",
                    )
                    config_script.chmod(0o755)
                config_vars = active_httpd_prefix / "build/config_vars.mk"
                config_vars.parent.mkdir(parents=True, exist_ok=True)
                config_vars.write_text(f"prefix = {active_httpd_prefix}\n", encoding="utf-8")
                (active_httpd_prefix / "include").mkdir(parents=True, exist_ok=True)
                module = active_build_path / "output/apache/mod_security3.so"
                module.parent.mkdir(parents=True, exist_ok=True)
                module.write_text("module\n", encoding="utf-8")
                config = active_httpd_prefix / "conf/httpd.conf"
                config.parent.mkdir(parents=True, exist_ok=True)
                config.write_text(f"ServerRoot \"{active_httpd_prefix}\"\n", encoding="utf-8")
                return subprocess.CompletedProcess(["apache-build"], 0, "", "")

            with mock.patch.object(components, "crypt_diagnostics", return_value={"crypt_link_arg": ""}), mock.patch.object(
                components, "run_build", side_effect=build_apache
            ) as run_build:
                record = components.prepare_apache_httpd(
                    {},
                    connector_root,
                    framework_root,
                    cache_root,
                    root / "work",
                    cache_root / "sources",
                    cache_root / "archives",
                    modsecurity={"status": "built", "build_id": "modsecurity", "lib_dir": str(modsecurity_lib.parent)},
                    plan=plan,
                )
            self.assertEqual("built", record["status"])
            self.assertTrue(run_build.called)
            self.assertTrue(components.executable(entry / "httpd/bin/httpd"))
            self.assertTrue(components.executable(entry / "httpd/bin/apxs"))
            self.assertTrue(components.connector_manifest_ready(plan))
            apxs_result = subprocess.run(
                [str(entry / "httpd/bin/apxs"), "-q", "INCLUDEDIR"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(0, apxs_result.returncode, apxs_result.stderr)
            self.assertEqual(str(entry / "httpd/include"), apxs_result.stdout.strip())
            staging_prefix = staging_prefixes[0]
            for relative in ("bin/apxs", "build/config_vars.mk", "bin/apr-1-config", "bin/apu-1-config", "bin/apachectl-mrts", "conf/httpd.conf"):
                self.assertNotIn(str(staging_prefix.parent), (entry / "httpd" / relative).read_text(encoding="utf-8"))
            self.assertFalse(any(path.name.startswith(f".{entry.name}.tmp-") for path in entry.parent.iterdir()))

    def test_nginx_discards_marker_owned_partial_root_before_build(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-cache-contract-") as temporary:
            root = Path(temporary)
            cache_root = components.ensure_managed_cache_root(root / "cache")
            identity = components.canonical_cache_identity(
                "nginx",
                env={},
                upstream_url="https://example.invalid/nginx",
                upstream_version="test",
                configuration_flags={},
                toolchain={"cc": "cc", "cc_version": "cc test"},
            )
            cache_key = identity["cache_key"]
            entry = cache_root / "builds/connectors/nginx" / cache_key
            build_path = entry / "build"
            nginx_prefix = entry / "nginx"
            modsecurity_lib = root / "shared-modsecurity/lib/libmodsecurity.so"
            modsecurity_lib.parent.mkdir(parents=True)
            modsecurity_lib.write_text("library\n", encoding="utf-8")
            plan = {
                "connector": "nginx",
                "connector_build_id": cache_key,
                "modsecurity_build_id": "modsecurity",
                "source_hash": "source-hash",
                "cache_key": cache_key,
                "cache_schema_version": components.CACHE_SCHEMA_VERSION,
                "cache_identity": identity,
                "cache_root": str(cache_root),
                "root": str(entry),
                "build_root": str(build_path),
                "nginx_prefix": str(nginx_prefix),
                "manifest": str(entry / "manifest.json"),
                "output_paths": {
                    "binary": str(nginx_prefix / "sbin/nginx"),
                    "module": str(nginx_prefix / "modules/ngx_http_modsecurity_module.so"),
                    "config": str(nginx_prefix / "conf/nginx.conf"),
                },
            }
            components.mark_managed_cache_entry(entry, cache_root, component="connector:nginx", cache_key=cache_key)
            entry.mkdir(parents=True)
            partial = entry / "partial-artifact"
            partial.write_text("partial\n", encoding="utf-8")
            connector_root = root / "connector"
            framework_root = root / "framework"
            (connector_root / "common/src").mkdir(parents=True)
            framework_root.mkdir()

            def build_nginx(*args: object, **_kwargs: object) -> subprocess.CompletedProcess[str]:
                self.assertFalse(partial.exists())
                build_env = args[1]
                assert isinstance(build_env, dict)
                active_build_path = Path(build_env["NGINX_BUILD_DIR"])
                active_nginx_prefix = Path(build_env["NGINX_PREFIX"])
                binary = active_nginx_prefix / "sbin/nginx"
                binary.parent.mkdir(parents=True, exist_ok=True)
                binary.write_text("#!/bin/sh\n", encoding="utf-8")
                binary.chmod(0o755)
                module = active_nginx_prefix / "modules/ngx_http_modsecurity_module.so"
                module.parent.mkdir(parents=True, exist_ok=True)
                module.write_text("module\n", encoding="utf-8")
                config = active_nginx_prefix / "conf/nginx.conf"
                config.parent.mkdir(parents=True, exist_ok=True)
                config.write_text("events {}\n", encoding="utf-8")
                return subprocess.CompletedProcess(["nginx-build"], 0, "", "")

            with mock.patch.object(components, "run_build", side_effect=build_nginx) as run_build:
                record = components.prepare_nginx_runtime(
                    {},
                    connector_root,
                    framework_root,
                    cache_root,
                    root / "work",
                    cache_root / "sources",
                    cache_root / "archives",
                    modsecurity={"status": "built", "build_id": "modsecurity", "lib_dir": str(modsecurity_lib.parent)},
                    plan=plan,
                )
            self.assertEqual("built", record["status"])
            self.assertTrue(run_build.called)
            self.assertFalse(partial.exists())
            self.assertTrue(components.executable(entry / "nginx/sbin/nginx"))
            self.assertTrue(components.connector_manifest_ready(plan))
            self.assertFalse(any(path.name.startswith(f".{entry.name}.tmp-") for path in entry.parent.iterdir()))

    def test_go_tool_uses_identity_keyed_staging_entry_and_complete_manifest(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-cache-contract-") as temporary:
            root = Path(temporary)
            cache_root = components.ensure_managed_cache_root(root / "cache")
            source = root / "source"
            source.mkdir()
            git_record = {
                "status": "present",
                "path": str(source),
                "url": "https://github.com/example/tool",
                "expected_ref": "v1.0.0",
                "release_tag": "v1.0.0",
                "actual_head": "deadbeef",
                "submodule_status": "",
                "submodule_status_clean": True,
            }
            toolchain = {"cc": "cc", "cc_version": "cc test", "cxx": "", "cxx_version": ""}
            go_build_calls = 0

            def fake_run_env(command: list[str], cwd: Path | None = None, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
                nonlocal go_build_calls
                if command[:2] == ["/usr/bin/go", "version"] or command[:2] == ["go", "version"]:
                    return subprocess.CompletedProcess(command, 0, "go version go1.test\n", "")
                if command[:2] == ["go", "build"]:
                    go_build_calls += 1
                    output = Path(command[command.index("-o") + 1])
                    output.parent.mkdir(parents=True, exist_ok=True)
                    output.write_text("#!/bin/sh\n", encoding="utf-8")
                    output.chmod(0o755)
                    return subprocess.CompletedProcess(command, 0, "", "")
                return subprocess.CompletedProcess(command, 0, "", "")

            with mock.patch.object(components.shutil, "which", side_effect=lambda name: "/usr/bin/go" if name == "go" else None), mock.patch.object(
                components, "toolchain_identity", return_value=toolchain
            ), mock.patch.object(components, "run_env", side_effect=fake_run_env), mock.patch.object(
                components,
                "go_main_packages",
                return_value=(["example/tool"], subprocess.CompletedProcess(["go", "list"], 0, "example/tool\n", "")),
            ):
                record = components.prepare_go_tool("tool", "TOOL_BIN", cache_root, root / "work", git_record)

            entry = cache_root / "builds/go/tool" / record["cache_key"]
            binary = entry / "bin/tool"
            self.assertEqual("built", record["status"])
            self.assertEqual(str(binary), record["path"])
            self.assertTrue(components.executable(binary))
            self.assertTrue(components.cache_manifest_complete(entry / "manifest.json", record["cache_identity"]))
            self.assertTrue(
                components.cache_entry_complete(
                    entry,
                    cache_root,
                    component="go:tool",
                    cache_key=record["cache_key"],
                    cache_identity=record["cache_identity"],
                )
            )
            self.assertFalse((cache_root / "bin/tool").exists())

            # A complete local manifest and executable do not authorize a
            # Go cache hit when registry completion is missing.
            marker_path = components.cache_entry_marker_path(entry, cache_root)
            marker = components.read_json(marker_path)
            marker["status"] = "incomplete"
            components.write_json(marker_path, marker)
            with mock.patch.object(components.shutil, "which", side_effect=lambda name: "/usr/bin/go" if name == "go" else None), mock.patch.object(
                components, "toolchain_identity", return_value=toolchain
            ), mock.patch.object(components, "run_env", side_effect=fake_run_env), mock.patch.object(
                components,
                "go_main_packages",
                return_value=(["example/tool"], subprocess.CompletedProcess(["go", "list"], 0, "example/tool\n", "")),
            ):
                rebuilt = components.prepare_go_tool("tool", "TOOL_BIN", cache_root, root / "work", git_record)
            self.assertEqual("built", rebuilt["status"])
            self.assertEqual(2, go_build_calls)

            # Old per-entry markers are upgraded only long enough to remove
            # their keyed entry; the Go binary is rebuilt rather than reused.
            (entry / "manifest.json").unlink()
            legacy_marker = components.read_json(components.cache_entry_marker_path(entry, cache_root))
            legacy_marker["schema_version"] = 1
            legacy_marker.pop("status", None)
            legacy_marker.pop("cache_identity", None)
            components.write_json(components.cache_entry_marker_path(entry, cache_root), legacy_marker)
            with mock.patch.object(components.shutil, "which", side_effect=lambda name: "/usr/bin/go" if name == "go" else None), mock.patch.object(
                components, "toolchain_identity", return_value=toolchain
            ), mock.patch.object(components, "run_env", side_effect=fake_run_env), mock.patch.object(
                components,
                "go_main_packages",
                return_value=(["example/tool"], subprocess.CompletedProcess(["go", "list"], 0, "example/tool\n", "")),
            ):
                rebuilt_legacy = components.prepare_go_tool("tool", "TOOL_BIN", cache_root, root / "work", git_record)
            self.assertEqual("built", rebuilt_legacy["status"])
            self.assertEqual("cache_schema_changed", rebuilt_legacy["invalidation_reason"])
            self.assertEqual(3, go_build_calls)

    def test_atomic_directory_publication_keeps_staging_invisible_until_publish(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-cache-contract-") as temporary:
            cache_root = components.ensure_managed_cache_root(Path(temporary) / "cache")
            final_path = cache_root / "builds/nginx/cache-key"
            staging_path = components.temporary_cache_dir(final_path, cache_root)
            (staging_path / "artifact").write_text("complete\n", encoding="utf-8")
            self.assertFalse(final_path.exists())

            components.atomic_publish_dir(staging_path, final_path, cache_root)
            self.assertFalse(staging_path.exists())
            self.assertEqual("complete\n", (final_path / "artifact").read_text(encoding="utf-8"))
            with self.assertRaisesRegex(RuntimeError, "cache_publish_destination_exists"):
                components.atomic_publish_dir(final_path, final_path, cache_root)

    def test_atomic_directory_publication_respects_an_existing_publish_lock(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-cache-contract-") as temporary:
            cache_root = components.ensure_managed_cache_root(Path(temporary) / "cache")
            final_path = cache_root / "builds/nginx/cache-key"
            staging_path = components.temporary_cache_dir(final_path, cache_root)
            publish_lock = final_path.parent / f".{final_path.name}.publish.lock"
            publish_lock.mkdir()
            try:
                with self.assertRaisesRegex(RuntimeError, "cache_publish_lock_busy"):
                    components.atomic_publish_dir(staging_path, final_path, cache_root)
                self.assertTrue(staging_path.exists())
                self.assertFalse(final_path.exists())
            finally:
                publish_lock.rmdir()
                components.safe_remove_dir(staging_path, cache_root)

    @staticmethod
    def git(command: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(command, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    def test_clean_managed_git_checkout_is_reused_across_target_preparations(self) -> None:
        """The second target reuses a published ModSecurity source checkout.

        This mirrors two prepare-runtime-components target invocations: the
        first record is persisted in the shared root manifest and becomes the
        second invocation's ``previous_records`` input.  A clean, complete
        checkout must not require another staging clone just to rediscover its
        already-pinned commit.
        """
        with tempfile.TemporaryDirectory(prefix="runtime-cache-contract-") as temporary:
            root = Path(temporary)
            upstream = root / "upstream"
            upstream.mkdir()
            self.git(["git", "init"], upstream)
            self.git(["git", "config", "user.email", "cache-test@example.invalid"], upstream)
            self.git(["git", "config", "user.name", "Cache Test"], upstream)
            (upstream / "tracked.txt").write_text("pristine\n", encoding="utf-8")
            self.git(["git", "add", "tracked.txt"], upstream)
            self.git(["git", "commit", "-m", "initial"], upstream)
            commit = self.git(["git", "rev-parse", "HEAD"], upstream).stdout.strip()
            branch = self.git(["git", "branch", "--show-current"], upstream).stdout.strip()

            cache_root = components.ensure_managed_cache_root(root / "cache")
            checkout = cache_root / "sources" / "ModSecurity_V3"
            expected_url = "https://github.com/owasp-modsecurity/ModSecurity.git"
            clone_count = 0
            original_run = components.run

            def local_clone_run(
                command: list[str],
                cwd: Path | None = None,
                check: bool = False,
            ) -> subprocess.CompletedProcess[str]:
                nonlocal clone_count
                if command[:2] == ["git", "ls-remote"]:
                    return subprocess.CompletedProcess(
                        command,
                        0,
                        f"{commit}\trefs/heads/{branch}\n",
                        "",
                    )
                if command[:3] == ["git", "clone", "--recursive"]:
                    clone_count += 1
                    clone = subprocess.run(
                        ["git", "clone", "--recursive", str(upstream), command[-1]],
                        text=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                    if clone.returncode == 0:
                        subprocess.run(
                            ["git", "-C", command[-1], "remote", "set-url", "origin", expected_url],
                            text=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            check=True,
                        )
                    if check and clone.returncode != 0:
                        raise RuntimeError(clone.stderr)
                    return clone
                if len(command) >= 5 and command[:2] == ["git", "-C"] and command[3:5] == ["fetch", "--tags"]:
                    return subprocess.CompletedProcess(command, 0, "", "")
                return original_run(command, cwd=cwd, check=check)

            with mock.patch.object(components, "run", side_effect=local_clone_run):
                apache_source = components.prepare_git_component(
                    "modsecurity-v3",
                    expected_url,
                    branch,
                    checkout,
                    {},
                    strict=True,
                    cache_root=cache_root,
                )
                nginx_source = components.prepare_git_component(
                    "modsecurity-v3",
                    expected_url,
                    branch,
                    checkout,
                    {"modsecurity-v3": apache_source},
                    strict=True,
                    cache_root=cache_root,
                )

            self.assertEqual("present", apache_source["status"])
            self.assertEqual("present", nginx_source["status"])
            self.assertEqual(1, clone_count)
            self.assertEqual(commit, nginx_source["actual_head"])
            self.assertEqual(apache_source["cache_identity"], nginx_source["cache_identity"])
            self.assertTrue(
                components.git_checkout_is_reusable(
                    checkout,
                    cache_root,
                    component="source:modsecurity-v3",
                    cache_identity=nginx_source["cache_identity"],
                    expected_url=expected_url,
                    actual_head=commit,
                )
            )

    def test_dirty_managed_git_checkout_is_replaced_and_atomically_republished(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-cache-contract-") as temporary:
            root = Path(temporary)
            upstream = root / "upstream"
            upstream.mkdir()
            self.git(["git", "init"], upstream)
            self.git(["git", "config", "user.email", "cache-test@example.invalid"], upstream)
            self.git(["git", "config", "user.name", "Cache Test"], upstream)
            (upstream / "tracked.txt").write_text("pristine\n", encoding="utf-8")
            self.git(["git", "add", "tracked.txt"], upstream)
            self.git(["git", "commit", "-m", "initial"], upstream)
            commit = self.git(["git", "rev-parse", "HEAD"], upstream).stdout.strip()

            cache_root = components.ensure_managed_cache_root(root / "cache")
            checkout = cache_root / "sources/component"
            expected_url = "https://github.com/example/component"
            source_identity = components.source_cache_identity("component", expected_url, commit)
            components.mark_managed_cache_entry(
                checkout,
                cache_root,
                component="source:component",
                cache_key=source_identity["cache_key"],
            )
            self.git(["git", "clone", str(upstream), str(checkout)])
            self.git(["git", "remote", "set-url", "origin", expected_url], checkout)
            components.write_cache_entry_completion(
                checkout,
                cache_root,
                component="source:component",
                cache_key=source_identity["cache_key"],
                cache_identity=source_identity,
            )
            (checkout / "untracked.txt").write_text("dirty\n", encoding="utf-8")
            original_run = components.run

            def local_clone_run(command: list[str], cwd: Path | None = None, check: bool = False) -> subprocess.CompletedProcess[str]:
                if command[:3] == ["git", "clone", "--recursive"]:
                    clone = subprocess.run(
                        ["git", "clone", "--recursive", str(upstream), command[-1]],
                        text=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                    if clone.returncode == 0:
                        subprocess.run(
                            ["git", "-C", command[-1], "remote", "set-url", "origin", expected_url],
                            text=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            check=True,
                        )
                    if check and clone.returncode != 0:
                        raise RuntimeError(clone.stderr)
                    return clone
                if len(command) >= 5 and command[:2] == ["git", "-C"] and command[3:5] == ["fetch", "--tags"]:
                    return subprocess.CompletedProcess(command, 0, "", "")
                return original_run(command, cwd=cwd, check=check)

            with mock.patch.object(components, "run", side_effect=local_clone_run):
                record = components.prepare_git_component(
                    "component",
                    expected_url,
                    commit,
                    checkout,
                    {
                        "component": {
                            "status": "present",
                            "url": expected_url,
                            "expected_ref": commit,
                            "actual_head": commit,
                            "git_fsck": "PASS",
                        }
                    },
                    strict=True,
                    cache_root=cache_root,
                )

            self.assertEqual("present", record["status"])
            self.assertTrue(record["rebuild_required"])
            self.assertTrue(record["old_entry_removed"])
            self.assertFalse((checkout / "untracked.txt").exists())
            self.assertEqual("", self.git(["git", "status", "--porcelain"], checkout).stdout)
            self.assertFalse(any(path.name.startswith(".component.tmp-") for path in checkout.parent.iterdir()))
            self.assertTrue(
                components.cache_entry_complete(
                    checkout,
                    cache_root,
                    component="source:component",
                    cache_key=source_identity["cache_key"],
                    cache_identity=source_identity,
                )
            )

    def test_corrupt_managed_git_checkout_is_replaced_before_fetch(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-cache-contract-") as temporary:
            root = Path(temporary)
            upstream = root / "upstream"
            upstream.mkdir()
            self.git(["git", "init"], upstream)
            self.git(["git", "config", "user.email", "cache-test@example.invalid"], upstream)
            self.git(["git", "config", "user.name", "Cache Test"], upstream)
            (upstream / "tracked.txt").write_text("pristine\n", encoding="utf-8")
            self.git(["git", "add", "tracked.txt"], upstream)
            self.git(["git", "commit", "-m", "initial"], upstream)
            commit = self.git(["git", "rev-parse", "HEAD"], upstream).stdout.strip()
            cache_root = components.ensure_managed_cache_root(root / "cache")
            checkout = cache_root / "sources/component"
            expected_url = "https://github.com/example/component"
            identity = components.source_cache_identity("component", expected_url, commit)
            components.mark_managed_cache_entry(
                checkout,
                cache_root,
                component="source:component",
                cache_key=identity["cache_key"],
            )
            self.git(["git", "clone", str(upstream), str(checkout)])
            self.git(["git", "remote", "set-url", "origin", expected_url], checkout)
            components.write_cache_entry_completion(
                checkout,
                cache_root,
                component="source:component",
                cache_key=identity["cache_key"],
                cache_identity=identity,
            )
            (checkout / ".git/HEAD").write_text("not-a-valid-head\n", encoding="utf-8")
            original_run = components.run

            def local_clone_run(command: list[str], cwd: Path | None = None, check: bool = False) -> subprocess.CompletedProcess[str]:
                if command[:3] == ["git", "clone", "--recursive"]:
                    clone = subprocess.run(
                        ["git", "clone", "--recursive", str(upstream), command[-1]],
                        text=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                    if clone.returncode == 0:
                        subprocess.run(
                            ["git", "-C", command[-1], "remote", "set-url", "origin", expected_url],
                            text=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            check=True,
                        )
                    return clone
                if len(command) >= 5 and command[:2] == ["git", "-C"] and command[3:5] == ["fetch", "--tags"]:
                    return subprocess.CompletedProcess(command, 0, "", "")
                return original_run(command, cwd=cwd, check=check)

            with mock.patch.object(components, "run", side_effect=local_clone_run):
                record = components.prepare_git_component(
                    "component",
                    expected_url,
                    commit,
                    checkout,
                    {},
                    strict=True,
                    cache_root=cache_root,
                )

            self.assertEqual("present", record["status"])
            self.assertTrue(record["old_entry_removed"])
            # The old final checkout is left untouched while a verified
            # staging clone is resolved and published, so recovery is driven
            # by the incomplete published entry rather than an in-place Git
            # preflight mutation.
            self.assertEqual("resolved_source_commit_changed_or_incomplete", record["invalidation_reason"])
            self.assertEqual(commit, self.git(["git", "rev-parse", "HEAD"], checkout).stdout.strip())

    def test_moving_git_ref_uses_resolved_commit_and_never_fetches_final_checkout(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-cache-contract-") as temporary:
            root = Path(temporary)
            upstream = root / "upstream"
            upstream.mkdir()
            self.git(["git", "init"], upstream)
            self.git(["git", "config", "user.email", "cache-test@example.invalid"], upstream)
            self.git(["git", "config", "user.name", "Cache Test"], upstream)
            (upstream / "tracked.txt").write_text("first\n", encoding="utf-8")
            self.git(["git", "add", "tracked.txt"], upstream)
            self.git(["git", "commit", "-m", "first"], upstream)
            first_commit = self.git(["git", "rev-parse", "HEAD"], upstream).stdout.strip()
            branch = self.git(["git", "branch", "--show-current"], upstream).stdout.strip()

            cache_root = components.ensure_managed_cache_root(root / "cache")
            checkout = cache_root / "sources/component"
            expected_url = "https://github.com/example/component"
            first_identity = components.source_cache_identity("component", expected_url, branch, first_commit)
            components.mark_managed_cache_entry(
                checkout,
                cache_root,
                component="source:component",
                cache_key=first_identity["cache_key"],
            )
            self.git(["git", "clone", str(upstream), str(checkout)])
            self.git(["git", "remote", "set-url", "origin", expected_url], checkout)
            components.write_cache_entry_completion(
                checkout,
                cache_root,
                component="source:component",
                cache_key=first_identity["cache_key"],
                cache_identity=first_identity,
            )

            (upstream / "tracked.txt").write_text("second\n", encoding="utf-8")
            self.git(["git", "add", "tracked.txt"], upstream)
            self.git(["git", "commit", "-m", "second"], upstream)
            second_commit = self.git(["git", "rev-parse", "HEAD"], upstream).stdout.strip()
            original_run = components.run
            final_mutations: list[list[str]] = []

            def local_clone_run(command: list[str], cwd: Path | None = None, check: bool = False) -> subprocess.CompletedProcess[str]:
                if command[:2] == ["git", "ls-remote"]:
                    return subprocess.CompletedProcess(
                        command,
                        0,
                        f"{second_commit}\trefs/heads/{branch}\n",
                        "",
                    )
                if command[:3] == ["git", "clone", "--recursive"]:
                    clone = subprocess.run(
                        ["git", "clone", "--recursive", str(upstream), command[-1]],
                        text=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                    if clone.returncode == 0:
                        subprocess.run(
                            ["git", "-C", command[-1], "remote", "set-url", "origin", expected_url],
                            text=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            check=True,
                        )
                    return clone
                if len(command) >= 4 and command[:3] == ["git", "-C", str(checkout)] and command[3] in {
                    "fetch",
                    "checkout",
                    "reset",
                    "submodule",
                }:
                    final_mutations.append(command)
                if len(command) >= 5 and command[:2] == ["git", "-C"] and command[3:5] == ["fetch", "--tags"]:
                    return subprocess.CompletedProcess(command, 0, "", "")
                return original_run(command, cwd=cwd, check=check)

            with mock.patch.object(components, "run", side_effect=local_clone_run):
                record = components.prepare_git_component(
                    "component",
                    expected_url,
                    branch,
                    checkout,
                    {
                        "component": {
                            "status": "present",
                            "url": expected_url,
                            "expected_ref": branch,
                            "actual_head": first_commit,
                            "git_fsck": "PASS",
                        }
                    },
                    strict=True,
                    cache_root=cache_root,
                )

            self.assertEqual("present", record["status"])
            self.assertEqual(second_commit, record["actual_head"])
            self.assertEqual(second_commit, record["cache_identity"]["resolved_commit"])
            self.assertNotEqual(first_identity["cache_key"], record["cache_key"])
            self.assertEqual(second_commit, self.git(["git", "rev-parse", "HEAD"], checkout).stdout.strip())
            self.assertEqual("", self.git(["git", "status", "--porcelain"], checkout).stdout)
            self.assertFalse((checkout / "manifest.json").exists())
            self.assertEqual([], final_mutations)
            self.assertTrue(
                components.cache_entry_complete(
                    checkout,
                    cache_root,
                    component="source:component",
                    cache_key=record["cache_key"],
                    cache_identity=record["cache_identity"],
                )
            )


if __name__ == "__main__":
    unittest.main()
