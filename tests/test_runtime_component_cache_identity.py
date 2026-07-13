from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci" / "provisioning" / "components"))
SPEC = importlib.util.spec_from_file_location(
    "prepare_runtime_components", ROOT / "ci/provisioning/components/prepare-runtime-components.py"
)
assert SPEC is not None and SPEC.loader is not None
components = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(components)


class RuntimeComponentCacheIdentityTest(unittest.TestCase):
    def connector_plan(
        self,
        env: dict[str, str],
        archives: list[dict[str, str]],
        *,
        connector: str = "apache",
    ) -> dict:
        with tempfile.TemporaryDirectory(prefix="connector-cache-identity-") as temporary:
            root = Path(temporary)
            connector_root = root / "connector"
            framework_root = root / "framework"
            cache_root = root / "cache"
            (connector_root / f"connectors/{connector}").mkdir(parents=True)
            (connector_root / "common/include").mkdir(parents=True)
            (connector_root / "common/src").mkdir(parents=True)
            (framework_root / "ci").mkdir(parents=True)
            (connector_root / f"connectors/{connector}/input.c").write_text("int x;\n", encoding="utf-8")
            (framework_root / f"ci/provisioning/prepare-{connector}-build.sh").parent.mkdir(parents=True, exist_ok=True)
            (framework_root / f"ci/provisioning/prepare-{connector}-build.sh").write_text("#!/bin/sh\n", encoding="utf-8")
            if connector == "nginx":
                (framework_root / "ci/lib/common.sh").parent.mkdir(parents=True, exist_ok=True)
                (framework_root / "ci/lib/common.sh").write_text("#!/bin/sh\n", encoding="utf-8")
            compiler = mock.patch.object(
                components,
                "compiler_identity",
                return_value={"cc": "/usr/bin/cc", "cc_version": "cc test", "cxx": "", "cxx_version": ""},
            )
            source_hash = mock.patch.object(components, "hash_input_paths", return_value="source-hash")
            with compiler, source_hash:
                return components.connector_plan(
                    connector_root,
                    framework_root,
                    cache_root,
                    env,
                    connector,
                    {"build_id": "modsecurity-build", "prefix": "/cache/modsecurity"},
                    {"build_id": "expat-build", "prefix": "/cache/expat"},
                    archives,
                )

    def test_connector_id_changes_with_archive_content_hash(self) -> None:
        env = {"HTTPD_VERSION": "2.4.68"}
        first = self.connector_plan(env, [{"name": "httpd", "url": "https://example/httpd", "sha256": "a"}])
        second = self.connector_plan(env, [{"name": "httpd", "url": "https://example/httpd", "sha256": "b"}])
        self.assertNotEqual(first["connector_build_id"], second["connector_build_id"])

    def test_connector_id_changes_with_apr_version(self) -> None:
        first = self.connector_plan({"APR_VERSION": "1.7.5"}, [])
        second = self.connector_plan({"APR_VERSION": "1.7.6"}, [])
        self.assertNotEqual(first["connector_build_id"], second["connector_build_id"])

    def test_nginx_protocol_profile_and_pinned_quic_tls_inputs_change_cache_identity(self) -> None:
        h1 = self.connector_plan({"NGINX_PROTOCOL_PROFILE": "h1"}, [], connector="nginx")
        h2 = self.connector_plan({"NGINX_PROTOCOL_PROFILE": "h1-h2"}, [], connector="nginx")
        h3 = self.connector_plan({"NGINX_PROTOCOL_PROFILE": "h1-h2-h3-quic"}, [], connector="nginx")
        changed_tls = self.connector_plan(
            {
                "NGINX_PROTOCOL_PROFILE": "h1-h2-h3-quic",
                "NGINX_QUIC_TLS_SOURCE_SHA256": "f" * 64,
            },
            [],
            connector="nginx",
        )

        self.assertNotEqual(h1["cache_key"], h2["cache_key"])
        self.assertNotEqual(h2["cache_key"], h3["cache_key"])
        self.assertNotEqual(h3["cache_key"], changed_tls["cache_key"])
        self.assertEqual(
            "--with-http_ssl_module --with-http_v2_module --with-http_v3_module",
            h3["cache_identity"]["configuration_flags"]["NGINX_PROTOCOL_CONFIGURE_FLAGS"],
        )
        self.assertEqual("openssl", h3["nginx_protocol_build"]["tls_library"])

    def test_expat_reuse_requires_full_build_identity(self) -> None:
        with tempfile.TemporaryDirectory(prefix="expat-cache-identity-") as temporary:
            root = Path(temporary)
            cache = root / "cache"
            prefix = cache / "prefix/expat"
            (prefix / "include").mkdir(parents=True)
            (prefix / "lib").mkdir(parents=True)
            (prefix / "include/expat.h").write_text("/* expat */\n", encoding="utf-8")
            (prefix / "lib/libexpat.so").write_text("library\n", encoding="utf-8")
            components.write_json(
                prefix / "component-manifest.json",
                {"actual_head": "same-source", "build_id": "different-toolchain"},
            )
            source = root / "source"
            source.mkdir()
            with mock.patch.object(
                components,
                "compiler_identity",
                return_value={"cc": "/usr/bin/cc", "cc_version": "new compiler", "cxx": "", "cxx_version": ""},
            ):
                result = components.prepare_expat(
                    {"EXPAT_PREFIX": str(prefix), "EXPAT_BUILD_DIR": str(cache / "build/expat")},
                    cache,
                    root / "build",
                    {
                        "status": "present",
                        "actual_head": "same-source",
                        "path": str(source),
                        "submodule_status_clean": True,
                    },
                )
            self.assertNotEqual("present", result["status"])

    def test_modsecurity_identity_uses_immutable_expat_identity_not_mutable_manifest_tree(self) -> None:
        """A completed Expat prefix must not churn the shared ModSecurity key.

        Expat stores its own component manifest under the installed prefix.
        That manifest is updated at publication time, so its byte count is
        deliberately not a ModSecurity dependency.  The Cache-v2 identity is
        the immutable invalidation boundary instead.
        """
        git_record = {
            "url": "https://example.invalid/modsecurity.git",
            "expected_ref": "v3",
            "actual_head": "modsecurity-source",
            "submodule_status": "clean-submodules",
        }
        expat = {
            "actual_head": "expat-source",
            "cache_key": "expat-cache-key",
            "prefix": "/cache/builds/expat/expat-cache-key/prefix",
            "tree": {"exists": True, "file_count": 17, "total_size": 100},
            "cache_identity": {
                "cache_schema_version": 2,
                "component": "expat",
                "source_sha256": "expat-source",
                "cache_key": "expat-cache-key",
            },
        }
        later_expat = dict(expat)
        later_expat["tree"] = {
            "exists": True,
            "file_count": 18,
            "total_size": 4096,
            "sha256_manifest": "component-manifest-was-written",
        }
        toolchain = {"cc": "cc", "cc_version": "cc test", "cxx": "c++", "cxx_version": "c++ test"}
        with mock.patch.object(components, "toolchain_identity", return_value=toolchain), mock.patch.object(
            components, "patchset_identity", return_value={"sha256": "patchset", "files": []}
        ):
            first = components.modsecurity_build_inputs({}, git_record, expat, ROOT)
            second = components.modsecurity_build_inputs({}, git_record, later_expat, ROOT)

        self.assertEqual(first["dependency_hash"], second["dependency_hash"])
        self.assertEqual(first["cache_key"], second["cache_key"])

        changed_expat = dict(expat)
        changed_expat["cache_identity"] = {
            **expat["cache_identity"],
            "source_sha256": "changed-expat-source",
            "cache_key": "changed-expat-cache-key",
        }
        with mock.patch.object(components, "toolchain_identity", return_value=toolchain), mock.patch.object(
            components, "patchset_identity", return_value={"sha256": "patchset", "files": []}
        ):
            changed = components.modsecurity_build_inputs({}, git_record, changed_expat, ROOT)
        self.assertNotEqual(first["cache_key"], changed["cache_key"])


if __name__ == "__main__":
    unittest.main()
