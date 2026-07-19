from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "ci" / "checks" / "evidence" / "check-runtime-producer-readiness.py"
SPEC = importlib.util.spec_from_file_location("runtime_producer_readiness", CHECKER_PATH)
assert SPEC is not None and SPEC.loader is not None
readiness = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = readiness
SPEC.loader.exec_module(readiness)


class RuntimeProducerReadinessPathPolicyTest(unittest.TestCase):
    def _payload_with_source_roots(
        self,
        *,
        runtime_source_override: str | None = None,
    ) -> tuple[dict[str, object], Path, Path]:
        with tempfile.TemporaryDirectory(prefix="runtime-producer-source-root-") as temporary:
            temporary_root = Path(temporary)
            run_root = temporary_root / "verified-run"
            canonical_source_root = temporary_root / "external-source"
            framework_root = ROOT / "modules" / "ModSecurity-test-Framework"
            environment = {
                "VERIFIED_RUN_ROOT": str(run_root),
                "VERIFIED_SOURCE_ROOT": str(run_root / "src"),
                "SOURCE_ROOT": str(canonical_source_root),
                "BUILD_ROOT": str(run_root / "build"),
                "TMP_ROOT": str(run_root / "tmp"),
                "LOG_ROOT": str(run_root / "logs"),
                "CONNECTOR_COMPONENT_CACHE": str(run_root / "cache-v2" / "shared"),
                "NGINX_HARNESS_PARENT": str(run_root / "nginx-harness"),
                "MRTS_NATIVE_ROOT": str(run_root / "build" / "mrts-native"),
            }
            common = {
                "status": "present",
                "return_code": 0,
                "path": str(framework_root / "ci" / "lib" / "common.sh"),
                "error": "",
                "env": {},
            }
            runtime_environment = (
                {"SOURCE_ROOT": runtime_source_override}
                if runtime_source_override is not None
                else {}
            )
            with (
                patch.dict(readiness.os.environ, environment, clear=True),
                patch.object(readiness, "load_common_sh", return_value=common),
                patch.object(readiness, "parse_export_file", return_value=runtime_environment),
            ):
                payload = readiness.build_payload(ROOT, framework_root, run_root / "build")
        return payload, canonical_source_root, run_root

    @staticmethod
    def _path_row(payload: dict[str, object], label: str) -> dict[str, object]:
        return next(
            row
            for row in payload["paths"]
            if isinstance(row, dict) and row.get("label") == label
        )

    def test_canonical_narrow_external_source_root_passes_readiness(self) -> None:
        """A source root accepted by the canonical policy must remain usable."""
        payload, canonical_source_root, _ = self._payload_with_source_roots()

        source_row = self._path_row(payload, "SOURCE_ROOT")
        self.assertEqual("PASS", source_row["status"])
        self.assertEqual(str(canonical_source_root), source_row["path"])

    def test_runtime_environment_cannot_replace_canonical_source_root(self) -> None:
        """A later runtime-env value must not mint an additional source root."""
        payload, _, _ = self._payload_with_source_roots(
            runtime_source_override="/etc/evidence-escape",
        )

        source_row = self._path_row(payload, "SOURCE_ROOT")
        self.assertEqual("BLOCKED", source_row["status"])
        self.assertIn("system write path", str(source_row["notes"]))

    def test_safe_external_source_sibling_is_not_authorized(self) -> None:
        """A different narrow source directory cannot inherit canonical trust."""
        with tempfile.TemporaryDirectory(prefix="runtime-producer-source-root-") as temporary:
            temporary_root = Path(temporary)
            run_root = temporary_root / "verified-run"
            canonical_source_root = temporary_root / "canonical-source"
            roots = {
                "verified_run_root": run_root,
                "verified_source_root": run_root / "src",
                "source_root": canonical_source_root,
            }

            foreign_source = readiness.check_safe_path(
                temporary_root / "foreign-source",
                "SOURCE_ROOT",
                roots,
                Path("/"),
                Path("/"),
            )
            self.assertEqual("BLOCKED", foreign_source["status"])
            self.assertIn("outside allowed runtime/cache roots", foreign_source["notes"])

    def test_project_root_argument_cannot_authorize_system_write_path(self) -> None:
        """Readiness reporting must not trust a caller-supplied project root for writes."""
        with tempfile.TemporaryDirectory(prefix="runtime-producer-path-policy-") as temporary:
            run_root = Path(temporary) / "verified-run"
            roots = {
                "verified_run_root": run_root,
                "state_home": run_root / "state",
                "build_root": run_root / "build",
                "cache_root": run_root / "cache-v2",
                "tmp_root": run_root / "tmp",
                "log_root": run_root / "logs",
                "mrts_native_root": run_root / "build" / "mrts-native",
            }

            escaped = readiness.check_safe_path(
                Path("/etc/evidence-escape"),
                "BUILD_ROOT",
                roots,
                Path("/"),
                Path("/"),
            )
            self.assertEqual("BLOCKED", escaped["status"])
            self.assertIn("system write path", escaped["notes"])

            control = readiness.check_safe_path(
                run_root / "build" / "apache",
                "BUILD_ROOT",
                roots,
                Path("/"),
                Path("/"),
            )
            self.assertEqual("PASS", control["status"])


if __name__ == "__main__":
    unittest.main()
