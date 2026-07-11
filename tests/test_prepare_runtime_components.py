from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
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


class PrepareRuntimeComponentsTest(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
