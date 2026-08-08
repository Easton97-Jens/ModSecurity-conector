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

    def test_full_smoke_nginx_snapshot_fails_closed_without_a_valid_managed_contract(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-env-nginx-contract-") as temporary:
            root = Path(temporary)
            connector_root = root / "connector"
            cache_root = root / "cache"
            ready_nginx = {
                "status": "built",
                "require_pinned_provenance": True,
                "nginx_bin": str(cache_root / "builds/connectors/nginx/cache-key/nginx/sbin/nginx"),
                "module_dir": str(cache_root / "builds/connectors/nginx/cache-key/nginx/modules"),
                "module_file": str(
                    cache_root / "builds/connectors/nginx/cache-key/nginx/modules/ngx_http_modsecurity_module.so"
                ),
                "modsecurity_lib_dir": str(cache_root / "modsecurity/lib"),
                "build_path": str(cache_root / "builds/connectors/nginx/cache-key/build"),
                "nginx_prefix": str(cache_root / "builds/connectors/nginx/cache-key/nginx"),
                "connector_build_id": "cache-key",
                "protocol_profile": "h1",
            }

            self.assertEqual(
                components.nginx_runtime_environment(connector_root, cache_root, ready_nginx),
                {},
            )
            self.assertEqual(
                components.nginx_runtime_environment(
                    connector_root,
                    cache_root,
                    {**ready_nginx, "runtime_contract_valid": False},
                ),
                {},
            )

            values = components.nginx_runtime_environment(
                connector_root,
                cache_root,
                {**ready_nginx, "runtime_contract_valid": True},
            )
            self.assertEqual(values["MRTS_NATIVE_NGINX_BIN"], ready_nginx["nginx_bin"])
            self.assertEqual(values["NGINX_PREFIX"], ready_nginx["nginx_prefix"])
            self.assertEqual(
                values["MSCONNECTOR_COMMON_SRC"],
                str(connector_root / "common" / "src"),
            )

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

    def test_full_smoke_matrix_pins_the_complete_nginx_release_tuple_for_both_variants(self) -> None:
        """The job-level NGINX tuple applies equally to both CRS variants.

        Keeping the assertion at the workflow boundary prevents a later matrix
        edit from silently reintroducing a floating NGINX source for one
        full-smoke variant while the other remains pinned.
        """
        workflow = (ROOT / ".github" / "workflows" / "test-full-smoke-sequential.yml").read_text(
            encoding="utf-8"
        )
        matrix_start = workflow.index("      matrix:\n        variant:\n")
        env_start = workflow.index("    env:\n", matrix_start)
        steps_start = workflow.index("    steps:\n", env_start)
        matrix_block = workflow[matrix_start:env_start]
        nginx_env = workflow[env_start:steps_start]

        for variant in ("no-crs", "with-crs"):
            with self.subTest(variant=variant):
                self.assertIn(f"          - {variant}\n", matrix_block)
                self.assertIn('BUILD_NGINX_FROM_SOURCE: "1"', nginx_env)
                self.assertIn("NGINX_SOURCE_MODE: github-release", nginx_env)
                self.assertIn("NGINX_SOURCE_REPO_URL: https://github.com/nginx/nginx", nginx_env)
                self.assertIn("NGINX_RELEASE_TAG: release-1.31.3", nginx_env)
                self.assertIn("NGINX_SOURCE_GIT_REF: release-1.31.3", nginx_env)
                self.assertIn("NGINX_RELEASE_ASSET_NAME: nginx-1.31.3.tar.gz", nginx_env)
                self.assertIn(
                    "NGINX_SHA256: a7657c50811c2d92d9895395e8b873ef60398142c4db21eb647811c38f6dd525",
                    nginx_env,
                )
                self.assertIn('NGINX_REQUIRE_PINNED_PROVENANCE: "1"', nginx_env)

        self.assertNotIn("NGINX_RELEASE_TAG: latest", nginx_env)
        self.assertNotIn("NGINX_SOURCE_GIT_REF: latest", nginx_env)
        self.assertNotIn("NGINX_GITHUB_REPO:", nginx_env)
        self.assertNotRegex(
            nginx_env,
            r"""(?m)^\s*(?:["']MODSECURITY_GIT_REF["']|MODSECURITY_GIT_REF)\s*:""",
        )

    def test_make_does_not_materialize_an_empty_nginx_github_repo_alias(self) -> None:
        environment = os.environ.copy()
        environment.pop("NGINX_GITHUB_REPO", None)
        result = subprocess.run(
            [
                "make",
                "--no-print-directory",
                "--silent",
                "--eval=assert-nginx-github-repo-is-unset: ; @printenv NGINX_GITHUB_REPO >/dev/null; test $$? -eq 1; FRAMEWORK_ROOT=$(CURDIR)/modules/ModSecurity-test-Framework NGINX_SOURCE_REPO_URL=https://github.com/nginx/nginx sh -eu -c '. \"$$FRAMEWORK_ROOT/ci/lib/common.sh\"; test \"$$NGINX_GITHUB_REPO\" = \"$$NGINX_SOURCE_REPO_URL\"'",
                "assert-nginx-github-repo-is-unset",
            ],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_make_preserves_an_absent_apr_util_tuple_for_framework_defaults(self) -> None:
        environment = os.environ.copy()
        for variable in (
            "APR_UTIL_VERSION",
            "APR_UTIL_SOURCE_URL",
            "APR_UTIL_SHA256",
            "APR_UTIL_SHA256_URL",
        ):
            environment.pop(variable, None)
        assertion = (
            "assert-apr-util-provenance-is-unset: ; @"
            "for variable in APR_UTIL_VERSION APR_UTIL_SOURCE_URL APR_UTIL_SHA256 "
            "APR_UTIL_SHA256_URL; do if printenv $$variable >/dev/null; then exit 1; "
            "fi; done; FRAMEWORK_ROOT=$(CURDIR)/modules/ModSecurity-test-Framework "
            "sh -eu -c '. \"$$FRAMEWORK_ROOT/ci/lib/common.sh\"; "
            "test \"$$APR_UTIL_VERSION\" = \"1.6.4\"; "
            "test \"$$APR_UTIL_SOURCE_URL\" = "
            "\"https://downloads.apache.org/apr/apr-util-1.6.4.tar.bz2\"; "
            "test \"$$APR_UTIL_SHA256\" = "
            "\"3e2ae08f40efa0c3701e54a954cefa08242de22a69f91a8ae44fc1e624ba309b\"; "
            "test \"$$APR_UTIL_SHA256_URL\" = "
            "\"https://downloads.apache.org/apr/apr-util-1.6.4.tar.bz2.sha256\"'"
        )
        result = subprocess.run(
            [
                "make",
                "--no-print-directory",
                "--silent",
                f"--eval={assertion}",
                "assert-apr-util-provenance-is-unset",
            ],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_make_forwards_an_explicit_empty_apr_util_override_to_the_guard(self) -> None:
        assertion = (
            "assert-empty-apr-util-override-is-rejected: ; @"
            "FRAMEWORK_ROOT=$(CURDIR)/modules/ModSecurity-test-Framework "
            "sh -eu -c '. \"$$FRAMEWORK_ROOT/ci/lib/common.sh\"; "
            "ci_require_apr_util_pinned_provenance'"
        )
        for variable in (
            "APR_UTIL_VERSION",
            "APR_UTIL_SOURCE_URL",
            "APR_UTIL_SHA256",
            "APR_UTIL_SHA256_URL",
        ):
            with self.subTest(variable=variable):
                environment = os.environ.copy()
                environment[variable] = ""
                result = subprocess.run(
                    [
                        "make",
                        "--no-print-directory",
                        "--silent",
                        f"--eval={assertion}",
                        "assert-empty-apr-util-override-is-rejected",
                    ],
                    cwd=ROOT,
                    env=environment,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertNotEqual(result.returncode, 0, result.stderr)
                self.assertIn(f"{variable} override is not permitted", result.stdout)

    def test_make_forwards_a_mismatched_apr_util_override_to_the_guard(self) -> None:
        assertion = (
            "assert-mismatched-apr-util-override-is-rejected: ; @"
            "FRAMEWORK_ROOT=$(CURDIR)/modules/ModSecurity-test-Framework "
            "sh -eu -c '. \"$$FRAMEWORK_ROOT/ci/lib/common.sh\"; "
            "ci_require_apr_util_pinned_provenance'"
        )
        for variable in (
            "APR_UTIL_VERSION",
            "APR_UTIL_SOURCE_URL",
            "APR_UTIL_SHA256",
            "APR_UTIL_SHA256_URL",
        ):
            with self.subTest(variable=variable):
                environment = os.environ.copy()
                environment[variable] = "untrusted-value"
                result = subprocess.run(
                    [
                        "make",
                        "--no-print-directory",
                        "--silent",
                        f"--eval={assertion}",
                        "assert-mismatched-apr-util-override-is-rejected",
                    ],
                    cwd=ROOT,
                    env=environment,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertNotEqual(result.returncode, 0, result.stderr)
                self.assertIn(f"{variable} override is not permitted", result.stdout)

    def test_full_smoke_cleanup_is_opt_in_and_skipping_it_keeps_the_matrix_eligible(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "test-full-smoke-sequential.yml").read_text(
            encoding="utf-8"
        )
        dispatch_start = workflow.index("  workflow_dispatch:\n")
        permissions_start = workflow.index("\npermissions:\n", dispatch_start)
        dispatch = workflow[dispatch_start:permissions_start]
        cleanup_start = workflow.index("  cleanup-artifacts:\n")
        matrix_start = workflow.index("  manual-heavy-runtime-validation:\n", cleanup_start)
        cleanup_job = workflow[cleanup_start:matrix_start]
        matrix_job = workflow[matrix_start:]

        self.assertIn("cleanup_artifacts:\n", dispatch)
        self.assertIn("required: false", dispatch)
        self.assertIn("default: false", dispatch)
        self.assertIn("type: boolean", dispatch)
        self.assertIn("if: ${{ inputs.cleanup_artifacts }}", cleanup_job)
        self.assertIn("needs: cleanup-artifacts", matrix_job)
        self.assertIn("if: ${{ always() }}", matrix_job)

    def test_full_smoke_variants_use_isolated_verified_state_and_pycache_roots(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "test-full-smoke-sequential.yml").read_text(
            encoding="utf-8"
        )
        paths_start = workflow.index("      - name: Initialize paths\n")
        next_step = workflow.index("\n      - name: Lint and py-compile\n", paths_start)
        initialize_paths = workflow[paths_start:next_step]

        self.assertIn(
            'verified_root="$RUNNER_TEMP/ModSecurity-conector-verified-${{ matrix.variant }}"',
            initialize_paths,
        )
        self.assertIn('echo "XDG_STATE_HOME=$verified_root/state"', initialize_paths)
        self.assertIn('echo "PYTHONPYCACHEPREFIX=$verified_root/python-pycache"', initialize_paths)
        self.assertNotIn(
            'verified_root="$RUNNER_TEMP/ModSecurity-conector-verified"',
            initialize_paths,
        )


if __name__ == "__main__":
    unittest.main()
