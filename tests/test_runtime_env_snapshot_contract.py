from __future__ import annotations

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
PREPARE_PATH = ROOT / "ci" / "provisioning" / "components" / "prepare-runtime-components.py"
RESERVE_PATH = ROOT / "ci" / "runtime" / "lifecycle" / "reserve-runtime-env-snapshot.sh"
NATIVE_COMPARISON_PATH = ROOT / "ci" / "runtime" / "lifecycle" / "run-native-case-comparison.py"
sys.path.insert(0, str(ROOT / "ci" / "provisioning" / "components"))
SPEC = importlib.util.spec_from_file_location(
    "runtime_env_snapshot_prepare_runtime_components", PREPARE_PATH
)
assert SPEC is not None
assert SPEC.loader is not None
components = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = components
SPEC.loader.exec_module(components)
NATIVE_SPEC = importlib.util.spec_from_file_location(
    "runtime_env_snapshot_native_case_comparison", NATIVE_COMPARISON_PATH
)
assert NATIVE_SPEC is not None
assert NATIVE_SPEC.loader is not None
native_comparison = importlib.util.module_from_spec(NATIVE_SPEC)
sys.modules[NATIVE_SPEC.name] = native_comparison
NATIVE_SPEC.loader.exec_module(native_comparison)
MISMATCH_PATH = ROOT / "ci" / "evidence" / "reports" / "generate-verified-runtime-mismatch-analysis.py"
MISMATCH_SPEC = importlib.util.spec_from_file_location(
    "runtime_env_snapshot_verified_runtime_mismatch", MISMATCH_PATH
)
assert MISMATCH_SPEC is not None
assert MISMATCH_SPEC.loader is not None
runtime_mismatch = importlib.util.module_from_spec(MISMATCH_SPEC)
sys.modules[MISMATCH_SPEC.name] = runtime_mismatch
MISMATCH_SPEC.loader.exec_module(runtime_mismatch)


class RuntimeEnvironmentSnapshotContractTest(unittest.TestCase):
    def test_native_summary_and_mismatch_helpers_keep_outputs_with_reduced_context_parameters(self) -> None:
        with tempfile.TemporaryDirectory(prefix="native-summary-signatures-") as temporary:
            root = Path(temporary)
            with (
                mock.patch.object(native_comparison, "build_metadata", return_value={}),
                mock.patch.object(native_comparison, "generated_json_text", return_value="{}\n"),
                mock.patch.object(native_comparison, "generated_markdown_text", return_value="# test\n"),
            ):
                summary = native_comparison.write_summary_report(
                    ROOT,
                    ROOT / "modules" / "ModSecurity-test-Framework",
                    root / "verified-runs",
                    (),
                    [],
                    root / "summary",
                )

            inventory = native_comparison.inventory()
            self.assertEqual(summary["payload"]["tool_inventory"], inventory)
            self.assertTrue(Path(summary["json"]).is_file())
            self.assertTrue(Path(summary["md"]).is_file())

            matrix_root = root / "matrix"
            job_path = matrix_root / "no-crs" / "no-mrts" / "apache" / "job.json"
            job_path.parent.mkdir(parents=True)
            job_path.write_text(
                json.dumps(
                    {
                        "connector": "apache",
                        "test_variant": "no-crs",
                        "mrts_variant": "no-mrts",
                        "return_code": 1,
                        "status": "blocked",
                        "summary_path": "",
                    }
                ),
                encoding="utf-8",
            )
            incomplete = runtime_mismatch.collect_incomplete_jobs(matrix_root, root / "build", None)
            self.assertEqual(len(incomplete), 1)
            self.assertEqual(incomplete[0]["connector"], "apache")
            self.assertEqual(incomplete[0]["variant"], "no-crs/no-mrts")
            self.assertEqual(
                runtime_mismatch.variant_from_result_path(
                    matrix_root / "with-crs" / "with-mrts" / "nginx" / "nginx-summary.json",
                    matrix_root,
                    "full_matrix",
                ),
                "with-crs/with-mrts",
            )

    def test_ready_nginx_snapshot_values_bind_the_parent_common_source_root(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-env-nginx-common-source-") as temporary:
            root = Path(temporary)
            connector_root = root / "connector"
            common_source_root = connector_root / "common" / "src"
            common_source_root.mkdir(parents=True)
            cache_root = root / "cache-v2" / "shared"

            with mock.patch.dict(os.environ, {"MSCONNECTOR_COMMON_SRC": "/untrusted/job/path"}):
                values = components.nginx_runtime_environment(
                    connector_root,
                    cache_root,
                    {
                        "status": "reused",
                        "nginx_bin": "/runtime/nginx",
                        "module_dir": "/runtime/modules",
                        "module_file": "/runtime/modules/ngx_http_modsecurity_module.so",
                        "modsecurity_lib_dir": "/runtime/modsecurity/lib",
                        "build_path": "/runtime/nginx-build",
                        "nginx_prefix": "/runtime/prefix",
                        "connector_build_id": "cache-key",
                        "protocol_profile": "h1",
                    },
                )

            self.assertEqual(str(common_source_root), values["MSCONNECTOR_COMMON_SRC"])
            self.assertEqual(
                str(cache_root / "builds" / "connectors"),
                values["NGINX_BUILD_OWNER_ROOT"],
            )

    def test_unready_nginx_does_not_publish_runtime_snapshot_values(self) -> None:
        values = components.nginx_runtime_environment(
            Path("/connector"),
            Path("/cache"),
            {"status": "blocked"},
        )
        self.assertEqual(values, {})

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
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
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
                shared_env.read_text(encoding="utf-8"),
                "export COMPATIBILITY_ONLY='preserved'\n",
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
            self.assertEqual(loaded.returncode, 0, loaded.stderr)
            self.assertEqual(
                loaded.stdout,
                f"nginx|{cache_root}|1|/runtime/modsecurity/include",
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

    def test_protected_nginx_broker_snapshot_uses_only_canonical_plan_outputs(self) -> None:
        with tempfile.TemporaryDirectory(prefix="protected-nginx-broker-snapshot-") as temporary:
            root = Path(temporary)
            cache_root = root / "cache-v2" / "shared"
            plan_root = cache_root / "builds" / "connectors" / "nginx" / "cache-key"
            binary = plan_root / "nginx" / "sbin" / "nginx"
            module = plan_root / "nginx" / "modules" / components.NGINX_MODULE_FILENAME
            prefix = cache_root / "prefix" / "modsecurity" / "modsecurity-build"
            for path, contents, mode in (
                (binary, "#!/bin/sh\nexit 0\n", 0o755),
                (module, "module\n", 0o644),
                (prefix / "lib" / components.MODSECURITY_LIBRARY_FILENAME, "library\n", 0o644),
                (prefix / "include" / "modsecurity" / "modsecurity.h", "header\n", 0o644),
            ):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(contents, encoding="utf-8")
                path.chmod(mode)
            output_root = root / "build" / "runtime-component-reports"
            snapshot = output_root / "runtime-env-snapshot.protected.sh"
            plan = {
                "root": str(plan_root),
                "manifest": str(plan_root / "manifest.json"),
                "output_paths": {"binary": str(binary), "module": str(module)},
                "cache_schema_version": components.CACHE_SCHEMA_VERSION,
                "cache_key": "cache-key",
                "connector_build_id": "cache-key",
                "build_flags": json.dumps(
                    {
                        "NGINX_RELEASE_TAG": "release-1.31.3",
                        "NGINX_SOURCE_REPO_URL": "https://github.com/nginx/nginx",
                        "NGINX_SHA256": "a" * 64,
                    }
                ),
            }
            components.write_json(plan_root / "manifest.json", {"build_flags": plan["build_flags"]})
            context = {
                "target_connector": "nginx",
                "cache_root": cache_root,
                "connector_root": root / "connector",
                "framework_root": root / "framework",
                "output_root": output_root,
                "requested_runtime_env_snapshot": snapshot,
                "runtime_env_snapshot_contract": components.PROTECTED_NGINX_BROKER_SNAPSHOT_CONTRACT,
                "env": {
                    "NGINX_SOURCE_MODE": "github-release",
                    "NGINX_RELEASE_TAG": "release-1.31.3",
                    "NGINX_SOURCE_REPO_URL": "https://github.com/nginx/nginx",
                    "NGINX_SHA256": "a" * 64,
                    # These must not influence the fixed snapshot values.
                    "NGINX_BINARY": "/ambient/nginx",
                    "NGINX_MODULE": "/ambient/module.so",
                    "MRTS_NATIVE_NGINX_BIN": "/ambient/mrts-nginx",
                    "MRTS_NATIVE_NGINX_MODULE_DIR": "/ambient/mrts-modules",
                },
            }
            component_records = {
                "nginx": {"status": "reused", "nginx_bin": "/ambient/nginx"},
                "nginx_plan": plan,
                "modsecurity": {"status": "reused", "build_id": "modsecurity-build", "prefix": str(prefix)},
            }
            context["components"] = component_records
            with (
                mock.patch.object(components, "connector_manifest_ready", return_value=True),
                mock.patch.object(components, "git_revision", side_effect=["b" * 40, "c" * 40]),
            ):
                written = components.write_runtime_environment_exports(
                    context,
                    {"UNRELATED_GENERIC_EXPORT": "must-not-appear"},
                )

            self.assertEqual(written, snapshot)
            self.assertEqual(
                snapshot.read_text(encoding="utf-8"),
                "export MODSECURITY_SHARED_PREFIX='{}'\n"
                "export NGINX_BINARY='{}'\n"
                "export NGINX_MODULE='{}'\n".format(prefix, binary, module),
            )
            provenance_path = output_root / components.TRUSTED_NGINX_BROKER_PROVENANCE_FILENAME
            record = json.loads(provenance_path.read_text(encoding="utf-8"))
            self.assertEqual(set(record), {"schema_version", "producer", "nginx", "modsecurity"})
            self.assertEqual(record["nginx"]["binary"]["path"], str(binary))
            self.assertEqual(record["nginx"]["module"]["path"], str(module))
            self.assertEqual(record["modsecurity"]["prefix"], str(prefix))
            self.assertIsInstance(record["nginx"]["binary"]["mode"], int)
            self.assertEqual(provenance_path.stat().st_mode & 0o777, 0o600)
            unsigned = json.loads(json.dumps(record))
            identity = unsigned["producer"].pop("identity")
            self.assertEqual(identity, components.stable_hash(unsigned))

            # A record or snapshot is never published from an ambient or
            # otherwise noncanonical plan output path.
            rejected_snapshot = output_root / "runtime-env-snapshot.rejected.sh"
            plan["output_paths"]["binary"] = "/ambient/nginx"
            context["requested_runtime_env_snapshot"] = rejected_snapshot
            with (
                mock.patch.object(components, "connector_manifest_ready", return_value=True),
                mock.patch.object(components, "git_revision", side_effect=["b" * 40, "c" * 40]),
                self.assertRaisesRegex(RuntimeError, "plan_output_paths_not_canonical"),
            ):
                components.write_runtime_environment_exports(context, {})
            self.assertFalse(rejected_snapshot.exists())

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
                    str(ROOT / "ci" / "provisioning" / "cache" / "with-runtime-components.sh"),
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
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(result.stdout, f"/correct/invocation/value|{snapshot}")

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
                    "VERIFIED_RUN_ROOT": str(root),
                    "VERIFIED_BUILD_ROOT": str(root / "build"),
                    "BUILD_ROOT": str(root / "build"),
                    "CACHE_ROOT": str(cache_root.parent),
                    "VERIFIED_COMPONENT_CACHE": str(cache_root),
                    "CONNECTOR_COMPONENT_CACHE": str(cache_root),
                    "RUNTIME_REPORT_OUTPUT_ROOT": str(output_root),
                    "RUNTIME_COMPONENT_ENV_SNAPSHOT": str(snapshot),
                },
                clear=False,
            ):
                loaded = native_comparison.load_runtime_env()
            self.assertEqual(loaded["MODSECURITY_INCLUDE_DIR"], "/correct/native-case/value")

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
                    "VERIFIED_RUN_ROOT": str(root),
                    "VERIFIED_BUILD_ROOT": str(root / "build"),
                    "BUILD_ROOT": str(root / "build"),
                    "CACHE_ROOT": str(cache_root.parent),
                    "VERIFIED_COMPONENT_CACHE": str(cache_root),
                    "CONNECTOR_COMPONENT_CACHE": str(cache_root),
                    "RUNTIME_REPORT_OUTPUT_ROOT": str(output_root),
                    "RUNTIME_COMPONENT_ENV_SNAPSHOT": str(outside_snapshot),
                },
                clear=False,
            ):
                loaded = native_comparison.load_runtime_env()
            self.assertNotEqual(loaded.get("MODSECURITY_INCLUDE_DIR"), "/wrong/shared/value")

    def test_central_runners_use_the_exact_local_snapshot_not_shared_runtime_env(self) -> None:
        with_runner = (ROOT / "ci" / "provisioning" / "cache" / "with-runtime-components.sh").read_text(encoding="utf-8")
        remaining_runner = (ROOT / "ci" / "runtime" / "lifecycle" / "run-remaining-connector-target.sh").read_text(
            encoding="utf-8"
        )
        canonical_runner = (ROOT / "ci" / "runtime" / "lifecycle" / "run-no-crs-baseline.sh").read_text(
            encoding="utf-8"
        )
        stage_runner = (ROOT / "ci" / "runtime" / "lifecycle" / "run-connector-stage.sh").read_text(encoding="utf-8")

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
            "modsecurity_prefix=$CONNECTOR_COMPONENT_CACHE/prefix/modsecurity/$modsecurity_build_id",
            canonical_runner,
        )
        self.assertNotIn(
            "modsecurity_prefix=$CACHE_ROOT/prefix/modsecurity/$modsecurity_build_id",
            canonical_runner,
        )
        self.assertIn(
            "traefik) host_binary=${TRAEFIK_BIN:-$CONNECTOR_COMPONENT_CACHE/traefik/bin/traefik} ;;",
            canonical_runner,
        )
        self.assertIn(
            'RUNTIME_COMPONENT_ENV_SNAPSHOT="${RUNTIME_COMPONENT_ENV_SNAPSHOT:-}"',
            stage_runner,
        )
        self.assertIn(
            "--runtime-env-snapshot \"$RUNTIME_COMPONENT_ENV_SNAPSHOT\"",
            (ROOT / "ci" / "provisioning" / "components" / "prepare-runtime-components.sh").read_text(encoding="utf-8"),
        )
        native_runner = NATIVE_COMPARISON_PATH.read_text(encoding="utf-8")
        self.assertIn("snapshot_value = env.get(\"RUNTIME_COMPONENT_ENV_SNAPSHOT\"", native_runner)
        self.assertIn("if snapshot_value:", native_runner)


if __name__ == "__main__":
    unittest.main()
