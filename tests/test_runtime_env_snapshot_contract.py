from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
PREPARE_PATH = ROOT / "ci" / "prepare-runtime-components.py"
RESERVE_PATH = ROOT / "ci" / "reserve-runtime-env-snapshot.sh"
NATIVE_COMPARISON_PATH = ROOT / "ci" / "run-native-case-comparison.py"
sys.path.insert(0, str(ROOT / "ci"))
SPEC = importlib.util.spec_from_file_location(
    "runtime_env_snapshot_prepare_runtime_components", PREPARE_PATH
)
assert SPEC is not None and SPEC.loader is not None
components = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = components
SPEC.loader.exec_module(components)
NATIVE_SPEC = importlib.util.spec_from_file_location(
    "runtime_env_snapshot_native_case_comparison", NATIVE_COMPARISON_PATH
)
assert NATIVE_SPEC is not None and NATIVE_SPEC.loader is not None
native_comparison = importlib.util.module_from_spec(NATIVE_SPEC)
sys.modules[NATIVE_SPEC.name] = native_comparison
NATIVE_SPEC.loader.exec_module(native_comparison)


class RuntimeEnvironmentSnapshotContractTest(unittest.TestCase):
    def test_snapshot_is_unique_local_atomic_and_keeps_shared_compatibility_export(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-env-snapshot-") as temporary:
            root = Path(temporary)
            cache_root = root / "cache-v2" / "shared"
            output_root = root / "build" / "nginx" / "run-1" / "runtime-component-reports"
            cache_root.mkdir(parents=True)
            shared_env = cache_root / "runtime-env.sh"
            shared_env.write_text("export COMPATIBILITY_ONLY='preserved'\n", encoding="utf-8")

            first = subprocess.run(
                ["sh", str(RESERVE_PATH), str(output_root)],
                cwd=ROOT,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            second = subprocess.run(
                ["sh", str(RESERVE_PATH), str(output_root)],
                cwd=ROOT,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.assertEqual(0, first.returncode, first.stderr)
            self.assertEqual(0, second.returncode, second.stderr)
            first_snapshot = Path(first.stdout.strip())
            second_snapshot = Path(second.stdout.strip())
            self.assertNotEqual(first_snapshot, second_snapshot)
            self.assertTrue(first_snapshot.is_file())
            self.assertTrue(second_snapshot.is_file())

            components.write_runtime_env_snapshot(
                {
                    "CONNECTOR_COMPONENT_CACHE": str(cache_root),
                    "MODSECURITY_INCLUDE_DIR": "/runtime/modsecurity/include",
                    "MODSECURITY_LIB_DIR": "/runtime/modsecurity/lib",
                },
                snapshot_path=first_snapshot,
                output_root=output_root,
                target_connector="nginx",
                cache_root=cache_root,
            )

            # The mutable shared export stays untouched for reports and legacy
            # consumers.  The runner-only metadata exists only in the local
            # snapshot that replaced its placeholder atomically.
            self.assertEqual(
                "export COMPATIBILITY_ONLY='preserved'\n",
                shared_env.read_text(encoding="utf-8"),
            )
            self.assertFalse(list(output_root.glob(".runtime-env-snapshot.*.tmp-*")))
            loaded = subprocess.run(
                [
                    "sh",
                    "-c",
                    '. "$1"; printf "%s|%s|%s|%s" "$RUNTIME_COMPONENT_ENV_SNAPSHOT_TARGET" "$RUNTIME_COMPONENT_ENV_SNAPSHOT_CACHE" "$RUNTIME_COMPONENT_ENV_SNAPSHOT_SCHEMA" "$MODSECURITY_INCLUDE_DIR"',
                    "sh",
                    str(first_snapshot),
                ],
                cwd=ROOT,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.assertEqual(0, loaded.returncode, loaded.stderr)
            self.assertEqual(
                f"nginx|{cache_root}|1|/runtime/modsecurity/include",
                loaded.stdout,
            )

    def test_snapshot_writer_rejects_a_path_outside_the_invocation_report_root(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-env-snapshot-") as temporary:
            root = Path(temporary)
            output_root = root / "connector-build" / "runtime-component-reports"
            with self.assertRaisesRegex(RuntimeError, "outside_output_root"):
                components.write_runtime_env_snapshot(
                    {},
                    snapshot_path=root / "other-run" / "runtime-env.sh",
                    output_root=output_root,
                    target_connector="shared",
                    cache_root=root / "cache-v2" / "shared",
                )

    def test_with_runner_consumes_the_prepared_snapshot_without_reading_shared_env(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-env-snapshot-") as temporary:
            root = Path(temporary)
            build_root = root / "build"
            cache_root = root / "cache-v2" / "shared"
            output_root = build_root / "runtime-component-reports"
            cache_root.mkdir(parents=True)
            # If the wrapper reopened this compatibility export, this sentinel
            # would replace the snapshot value asserted below.
            (cache_root / "runtime-env.sh").write_text(
                "export MODSECURITY_INCLUDE_DIR='/wrong/shared/value'\n",
                encoding="utf-8",
            )
            snapshot = output_root / "runtime-env-snapshot.prepared.sh"
            components.write_runtime_env_snapshot(
                {
                    "CONNECTOR_COMPONENT_CACHE": str(cache_root),
                    "MODSECURITY_INCLUDE_DIR": "/correct/invocation/value",
                },
                snapshot_path=snapshot,
                output_root=output_root,
                target_connector="shared",
                cache_root=cache_root,
            )

            result = subprocess.run(
                [
                    "sh",
                    str(ROOT / "ci" / "with-runtime-components.sh"),
                    "sh",
                    "-c",
                    'printf "%s|%s" "$MODSECURITY_INCLUDE_DIR" "$RUNTIME_COMPONENT_ENV_SNAPSHOT"',
                ],
                cwd=ROOT,
                env={
                    **os.environ,
                    "CONNECTOR_ROOT": str(ROOT),
                    "FRAMEWORK_ROOT": str(ROOT / "modules" / "ModSecurity-test-Framework"),
                    "VERIFIED_RUN_ROOT": str(root),
                    "VERIFIED_BUILD_ROOT": str(build_root),
                    "BUILD_ROOT": str(build_root),
                    "CACHE_ROOT": str(cache_root.parent),
                    "VERIFIED_COMPONENT_CACHE": str(cache_root),
                    "CONNECTOR_COMPONENT_CACHE": str(cache_root),
                    "RUNTIME_REPORT_OUTPUT_ROOT": str(output_root),
                    "RUNTIME_COMPONENT_TARGET": "shared",
                    "RUNTIME_COMPONENT_ENV_SNAPSHOT": str(snapshot),
                    "SKIP_RUNTIME_COMPONENT_PREPARE": "1",
                },
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertEqual(f"/correct/invocation/value|{snapshot}", result.stdout)

    def test_native_comparison_uses_the_wrapper_snapshot_not_shared_env(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-env-snapshot-") as temporary:
            root = Path(temporary)
            cache_root = root / "cache-v2" / "shared"
            output_root = root / "build" / "runtime-component-reports"
            cache_root.mkdir(parents=True)
            (cache_root / "runtime-env.sh").write_text(
                "export MODSECURITY_INCLUDE_DIR='/wrong/shared/value'\n",
                encoding="utf-8",
            )
            snapshot = output_root / "runtime-env-snapshot.native-case.sh"
            components.write_runtime_env_snapshot(
                {
                    "CONNECTOR_COMPONENT_CACHE": str(cache_root),
                    "MODSECURITY_INCLUDE_DIR": "/correct/native-case/value",
                },
                snapshot_path=snapshot,
                output_root=output_root,
                target_connector="all",
                cache_root=cache_root,
            )

            with mock.patch.dict(
                os.environ,
                {
                    "CONNECTOR_COMPONENT_CACHE": str(cache_root),
                    "RUNTIME_REPORT_OUTPUT_ROOT": str(output_root),
                    "RUNTIME_COMPONENT_ENV_SNAPSHOT": str(snapshot),
                },
                clear=False,
            ):
                loaded = native_comparison.load_runtime_env(root)
            self.assertEqual("/correct/native-case/value", loaded["MODSECURITY_INCLUDE_DIR"])

    def test_native_comparison_does_not_fallback_to_shared_env_for_an_invalid_snapshot(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-env-snapshot-") as temporary:
            root = Path(temporary)
            cache_root = root / "cache-v2" / "shared"
            output_root = root / "build" / "runtime-component-reports"
            cache_root.mkdir(parents=True)
            (cache_root / "runtime-env.sh").write_text(
                "export MODSECURITY_INCLUDE_DIR='/wrong/shared/value'\n",
                encoding="utf-8",
            )
            outside_snapshot = root / "other-invocation" / "runtime-env.sh"

            with mock.patch.dict(
                os.environ,
                {
                    "CONNECTOR_COMPONENT_CACHE": str(cache_root),
                    "RUNTIME_REPORT_OUTPUT_ROOT": str(output_root),
                    "RUNTIME_COMPONENT_ENV_SNAPSHOT": str(outside_snapshot),
                },
                clear=False,
            ):
                loaded = native_comparison.load_runtime_env(root)
            self.assertNotEqual("/wrong/shared/value", loaded.get("MODSECURITY_INCLUDE_DIR"))

    def test_central_runners_use_the_exact_local_snapshot_not_shared_runtime_env(self) -> None:
        with_runner = (ROOT / "ci" / "with-runtime-components.sh").read_text(encoding="utf-8")
        remaining_runner = (ROOT / "ci" / "run-remaining-connector-target.sh").read_text(
            encoding="utf-8"
        )
        canonical_runner = (ROOT / "ci" / "run-no-crs-baseline.sh").read_text(
            encoding="utf-8"
        )
        stage_runner = (ROOT / "ci" / "run-connector-stage.sh").read_text(encoding="utf-8")

        for source in (with_runner, remaining_runner, canonical_runner):
            self.assertIn("runtime_env=$RUNTIME_COMPONENT_ENV_SNAPSHOT", source)
        self.assertNotIn('runtime_env="$CONNECTOR_COMPONENT_CACHE/runtime-env.sh"', with_runner)
        self.assertNotIn('runtime_env="$CONNECTOR_COMPONENT_CACHE/runtime-env.sh"', remaining_runner)
        self.assertNotIn("runtime_env=$CONNECTOR_COMPONENT_CACHE/runtime-env.sh", canonical_runner)

        self.assertIn(
            "RUNTIME_REPORT_OUTPUT_ROOT=$CONNECTOR_BUILD_ROOT/runtime-component-reports",
            canonical_runner,
        )
        self.assertIn(
            'RUNTIME_COMPONENT_ENV_SNAPSHOT="$RUNTIME_COMPONENT_ENV_SNAPSHOT"',
            canonical_runner,
        )
        self.assertIn(
            'RUNTIME_COMPONENT_ENV_SNAPSHOT="${RUNTIME_COMPONENT_ENV_SNAPSHOT:-}"',
            stage_runner,
        )
        self.assertIn(
            "--runtime-env-snapshot \"$RUNTIME_COMPONENT_ENV_SNAPSHOT\"",
            (ROOT / "ci" / "prepare-runtime-components.sh").read_text(encoding="utf-8"),
        )
        native_runner = NATIVE_COMPARISON_PATH.read_text(encoding="utf-8")
        self.assertIn("snapshot_value = env.get(\"RUNTIME_COMPONENT_ENV_SNAPSHOT\"", native_runner)
        self.assertIn("if snapshot_value:", native_runner)


if __name__ == "__main__":
    unittest.main()
