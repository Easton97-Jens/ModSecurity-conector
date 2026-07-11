from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
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


class RuntimeComponentCacheIdentityTest(unittest.TestCase):
    def connector_plan(self, env: dict[str, str], archives: list[dict[str, str]]) -> dict:
        with tempfile.TemporaryDirectory(prefix="connector-cache-identity-") as temporary:
            root = Path(temporary)
            connector_root = root / "connector"
            framework_root = root / "framework"
            cache_root = root / "cache"
            (connector_root / "connectors/apache").mkdir(parents=True)
            (connector_root / "common/include").mkdir(parents=True)
            (connector_root / "common/src").mkdir(parents=True)
            (framework_root / "ci").mkdir(parents=True)
            (connector_root / "connectors/apache/input.c").write_text("int x;\n", encoding="utf-8")
            (framework_root / "ci/prepare-apache-build.sh").write_text("#!/bin/sh\n", encoding="utf-8")
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
                    "apache",
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


if __name__ == "__main__":
    unittest.main()
