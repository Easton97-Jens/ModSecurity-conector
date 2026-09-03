from __future__ import annotations

import argparse
import importlib.util
import json
import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "traefik_runtime_smoke_security",
    ROOT / "connectors/traefik/scripts/runtime_smoke.py",
)
assert SPEC is not None
assert SPEC.loader is not None
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


class TraefikRuntimeSmokeSecurityTest(unittest.TestCase):
    @staticmethod
    def make_executable(path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        path.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
        return path

    @staticmethod
    def runtime_args(connector_binary: Path, traefik_binary: Path) -> argparse.Namespace:
        return argparse.Namespace(
            connector_binary=connector_binary,
            traefik_binary=traefik_binary,
        )

    def test_missing_runtime_root_is_blocked_without_a_shared_temporary_default(self) -> None:
        with mock.patch.dict(
            os.environ,
            {"BUILD_ROOT": "", "CONNECTOR_COMPONENT_CACHE": ""},
            clear=False,
        ):
            with self.assertRaisesRegex(RUNNER.MissingDependency, "BUILD_ROOT must be set"):
                RUNNER.require_runtime_root_from_environment("BUILD_ROOT", ROOT)

    def test_group_or_world_writable_runtime_root_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="traefik-runtime-root-") as temporary:
            root = Path(temporary) / "runtime-root"
            root.mkdir(mode=0o700)
            root.chmod(stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            with self.assertRaisesRegex(RUNNER.MissingDependency, "must not be group or world writable"):
                RUNNER.require_trusted_runtime_root(root, "BUILD_ROOT", ROOT)

        filesystem_root = Path(os.sep)
        with self.assertRaisesRegex(RUNNER.MissingDependency, "too broad"):
            RUNNER.require_trusted_runtime_root(filesystem_root, "BUILD_ROOT", ROOT)

    def test_symlinked_runtime_root_and_binary_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="traefik-runtime-root-") as temporary:
            temporary_root = Path(temporary)
            build_root = temporary_root / "build"
            build_root.mkdir(mode=0o700)
            root_alias = temporary_root / "build-alias"
            root_alias.symlink_to(build_root, target_is_directory=True)
            with self.assertRaisesRegex(RUNNER.MissingDependency, "symlink"):
                RUNNER.require_trusted_runtime_root(root_alias, "BUILD_ROOT", ROOT)

            target = self.make_executable(temporary_root / "outside" / "runner")
            binary_alias = build_root / "runner"
            binary_alias.symlink_to(target)
            with self.assertRaisesRegex(RUNNER.MissingDependency, "symlink"):
                RUNNER.require_local_executable(binary_alias, "Traefik connector binary", build_root)

    def test_cross_user_writable_binary_ancestor_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="traefik-runtime-root-") as temporary:
            build_root = Path(temporary) / "build"
            build_root.mkdir(mode=0o700)
            untrusted_directory = build_root / "untrusted"
            untrusted_directory.mkdir(mode=0o777)
            untrusted_directory.chmod(0o777)
            binary = self.make_executable(untrusted_directory / "traefik-forwardauth")
            with self.assertRaisesRegex(
                RUNNER.MissingDependency, "permits cross-user replacement"
            ):
                RUNNER.require_local_executable(binary, "Traefik connector binary", build_root)

    def test_runtime_binaries_must_be_contained_and_a_legitimate_pair_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory(prefix="traefik-runtime-root-") as temporary:
            temporary_root = Path(temporary)
            build_root = temporary_root / "build"
            component_cache = temporary_root / "cache"
            # Owner-controlled roots may be searchable by other users; only
            # group/world write access would let another user replace binaries.
            build_root.mkdir(mode=0o755)
            component_cache.mkdir(mode=0o755)
            build_root.chmod(0o755)
            component_cache.chmod(0o755)
            connector_binary = self.make_executable(build_root / "traefik-forwardauth")
            traefik_binary = self.make_executable(component_cache / "traefik")
            outside_binary = self.make_executable(temporary_root / "outside" / "traefik")
            with mock.patch.dict(
                os.environ,
                {
                    "BUILD_ROOT": str(build_root),
                    "CONNECTOR_COMPONENT_CACHE": str(component_cache),
                },
                clear=False,
            ):
                resolved_build_root, connector, traefik = RUNNER.resolve_runtime_paths(
                    self.runtime_args(connector_binary, traefik_binary), ROOT
                )
                self.assertEqual(resolved_build_root, build_root)
                self.assertEqual(connector.path, connector_binary)
                self.assertEqual(traefik.path, traefik_binary)
                outside_arguments = self.runtime_args(outside_binary, traefik_binary)
                with self.assertRaisesRegex(RUNNER.MissingDependency, "must remain below"):
                    RUNNER.resolve_runtime_paths(outside_arguments, ROOT)

    def test_trusted_executable_rejects_control_characters_before_process_start(self) -> None:
        with tempfile.TemporaryDirectory(prefix="traefik-runtime-root-") as temporary:
            build_root = Path(temporary) / "build"
            build_root.mkdir(mode=0o700)
            binary = self.make_executable(build_root / "traefik-forwardauth")
            executable = RUNNER.require_local_executable(
                binary, "Traefik connector binary", build_root
            )
            self.assertEqual(
                executable.arguments("--check-config"),
                (str(binary), "--check-config"),
            )
            with self.assertRaisesRegex(RUNNER.MissingDependency, "control characters"):
                executable.arguments("--config", "unsafe\nvalue")

    def test_runtime_artifact_writers_keep_fixed_names_below_validated_directories(self) -> None:
        with tempfile.TemporaryDirectory(prefix="traefik-runtime-root-") as temporary:
            runtime_root = Path(temporary) / "runtime"
            config_dir = runtime_root / "config"
            config_dir.mkdir(parents=True, mode=0o700)
            template = runtime_root / "template.conf"
            rules_file = runtime_root / "rules.conf"
            event_path = runtime_root / "logs" / "events.jsonl"
            template.write_text("rules_file=old\nevent_path=old\n", encoding="utf-8")
            rules_file.write_text("SecRuleEngine On\n", encoding="utf-8")

            service_config = RUNNER.write_concrete_service_config(
                template, config_dir, rules_file, event_path
            )
            result_path = RUNNER.write_runtime_result(runtime_root, {"status": "PASS"})

            self.assertEqual(service_config, config_dir / RUNNER.SERVICE_CONFIG_FILE_NAME)
            self.assertEqual(result_path, runtime_root / RUNNER.RESULT_FILE_NAME)
            self.assertIn(f"rules_file={rules_file}", service_config.read_text(encoding="utf-8"))
            self.assertIn(f"event_path={event_path}", service_config.read_text(encoding="utf-8"))
            result_path.unlink()
            result_path.symlink_to(runtime_root / "outside-result.json")
            with self.assertRaisesRegex(RUNNER.MissingDependency, "runtime artifact path is unsafe"):
                RUNNER.write_runtime_result(runtime_root, {"status": "PASS"})

    def test_result_root_must_be_a_private_build_root_descendant(self) -> None:
        with tempfile.TemporaryDirectory(prefix="traefik-runtime-root-") as temporary:
            temporary_root = Path(temporary)
            build_root = temporary_root / "build"
            build_root.mkdir(mode=0o700)
            output_root = build_root / "traefik-connector" / "runtime-smoke"
            self.assertEqual(
                RUNNER.require_private_result_root(output_root, build_root), output_root
            )

            with self.assertRaisesRegex(RUNNER.MissingDependency, "must remain below"):
                RUNNER.require_private_result_root(temporary_root / "outside", build_root)
            with self.assertRaisesRegex(RUNNER.MissingDependency, "must not be the build root"):
                RUNNER.require_private_result_root(build_root, build_root)

            replaceable = build_root / "replaceable"
            replaceable.mkdir(mode=0o777)
            replaceable.chmod(0o777)
            with self.assertRaisesRegex(RUNNER.MissingDependency, "must not be group or world writable"):
                RUNNER.require_private_result_root(replaceable / "result", build_root)

    def test_canonical_lifecycle_keeps_traefik_results_below_the_stage_build_root(self) -> None:
        lifecycle = (ROOT / "ci" / "runtime" / "lifecycle" / "run-no-crs-baseline.sh").read_text(
            encoding="utf-8"
        )
        self.assertIn("TRAEFIK_RUNTIME_ROOT=$STAGE_BUILD_ROOT/traefik-runtime", lifecycle)
        self.assertNotIn("TRAEFIK_RUNTIME_ROOT=$CONNECTOR_RUN_ROOT/traefik-runtime", lifecycle)

    def test_no_crs_consumer_uses_the_canonical_parent_lifecycle_path(self) -> None:
        with tempfile.TemporaryDirectory(prefix="traefik-no-crs-consumer-") as temporary:
            repo_root = Path(temporary) / "checkout"
            consumer = (
                repo_root
                / "ci"
                / "runtime"
                / "lifecycle"
                / "consume-no-crs-selected-cases.sh"
            )
            self.make_executable(consumer)
            with mock.patch.dict(os.environ, {"MSCONNECTOR_NO_CRS_BASELINE": "1"}, clear=False):
                RUNNER.consume_no_crs_selected_cases(repo_root)

    def test_no_crs_consumer_is_not_required_for_non_baseline_runtime_smoke(self) -> None:
        with tempfile.TemporaryDirectory(prefix="traefik-no-crs-control-") as temporary:
            with mock.patch.dict(os.environ, {"MSCONNECTOR_NO_CRS_BASELINE": ""}, clear=False):
                RUNNER.consume_no_crs_selected_cases(Path(temporary) / "checkout")

    def test_forwardauth_runtime_chain_requires_the_private_response_observer(self) -> None:
        dynamic = RUNNER.dynamic_config(
            18081,
            18082,
            Path("/run/modsecurity/traefik-forwardauth-companion.sock"),
        )
        start_smoke = (ROOT / "connectors" / "traefik" / "scripts" / "start-smoke.sh").read_text(
            encoding="utf-8"
        )
        service = (ROOT / "connectors" / "traefik" / "src" / "traefik_forwardauth_service_main.c").read_text(
            encoding="utf-8"
        )

        self.assertIn("- modsecurity-forwardauth\n      - modsecurity-response-observer", dynamic)
        self.assertIn("authResponseHeaders:\n        - X-Msconnector-Response-Handle", dynamic)
        self.assertIn("socketPath: /run/modsecurity/traefik-forwardauth-companion.sock", dynamic)
        self.assertIn("MSCONNECTOR_TRAEFIK_FORWARDAUTH_COMPANION_SOCKET", start_smoke)
        self.assertIn('getenv(\n        "MSCONNECTOR_TRAEFIK_FORWARDAUTH_COMPANION_SOCKET")', service)
        self.assertIn("plugins-local/src/$OBSERVER_MODULE", start_smoke)
        self.assertIn("__COMPANION_SOCKET__", start_smoke)

    def test_forwardauth_preserves_common_header_limit_for_actual_mrc1_framing(self) -> None:
        service = (ROOT / "connectors" / "traefik" / "src" / "traefik_forwardauth_service_main.c").read_text(
            encoding="utf-8"
        )
        observer = (ROOT / "connectors" / "traefik" / "response_observer" / "observer.go").read_text(
            encoding="utf-8"
        )
        compact = "".join(service.split())

        self.assertNotIn("traefik_response_wire_header_limit", service)
        self.assertIn(
            "msconnector_traefik_forwardauth_response_companion_set_limits(companion,"
            "msconnector_runtime_header_count_limit(runtime),"
            "msconnector_runtime_total_header_limit(runtime),",
            compact,
        )
        self.assertRegex(observer, r"maxHeaderCount\s*=\s*256")
        self.assertRegex(
            observer,
            r'maxResponseHeaderPayload\s*=\s*maxPayload\s*\+\s*2\s*\+\s*2\s*\+'
            r'\s*len\("HTTP/1\.1"\)\s*\+\s*2\s*\+\s*4\*maxHeaderCount',
        )
        self.assertIn(
            "headerBytes > maxPayload || total > maxResponseHeaderPayload", observer
        )

    def test_response_phase_evidence_requires_precommit_p3_and_safe_p4_without_bodies(self) -> None:
        with tempfile.TemporaryDirectory(prefix="traefik-response-phase-events-") as temporary:
            event_path = Path(temporary) / "events.jsonl"
            records = [
                {
                    "connector": "traefik",
                    "transaction_id": "traefik-forwardauth-p3-block",
                    "rule_id": "1000003",
                    "phase": "response_headers",
                    "status": "blocked",
                    "actual_action": "deny",
                    "response_committed": False,
                },
                {
                    "connector": "traefik",
                    "transaction_id": "traefik-forwardauth-p4-safe",
                    "rule_id": "1000004",
                    "phase": "response_body",
                    "status": "blocked",
                    "actual_action": "log_only",
                    "response_committed": True,
                    "body_bytes_seen": 28,
                },
            ]
            event_path.write_text(
                "\n".join(json.dumps(record) for record in records) + "\n",
                encoding="utf-8",
            )
            RUNNER.verify_response_phase_events(event_path)

            records[1]["response_body"] = "must-not-appear"
            event_path.write_text(
                "\n".join(json.dumps(record) for record in records) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(RuntimeError, "forbidden body payload"):
                RUNNER.verify_response_phase_events(event_path)

    def test_response_observer_staging_is_private_and_rejects_symlinks(self) -> None:
        with tempfile.TemporaryDirectory(prefix="traefik-response-observer-") as temporary:
            root = Path(temporary)
            source = root / "source"
            source.mkdir(mode=0o700)
            (source / "go.mod").write_text("module example.test/observer\n", encoding="utf-8")
            runtime_root = root / "runtime"
            runtime_root.mkdir(mode=0o700)

            RUNNER.stage_response_observer(source, runtime_root)

            staged = runtime_root / "plugins-local" / "src" / RUNNER.OBSERVER_MODULE
            self.assertTrue((staged / "go.mod").is_file())
            self.assertEqual(stat.S_IMODE((runtime_root / "plugins-local").stat().st_mode), 0o700)
            self.assertEqual(stat.S_IMODE((staged / "go.mod").stat().st_mode), 0o600)

            unsafe = root / "unsafe-source"
            unsafe.mkdir(mode=0o700)
            (unsafe / "linked").symlink_to(source / "go.mod")
            with self.assertRaisesRegex(RUNNER.MissingDependency, "contains a symlink"):
                RUNNER.stage_response_observer(unsafe, runtime_root)

    def test_start_smoke_rejects_dotdot_before_cleanup(self) -> None:
        with tempfile.TemporaryDirectory(prefix="traefik-start-root-") as temporary:
            temporary_root = Path(temporary)
            build_root = temporary_root / "build"
            allowed_root = build_root / "traefik-connector"
            target = allowed_root / "other-target"
            target.mkdir(parents=True, mode=0o700)
            sentinel = target / "must-survive"
            sentinel.write_text("keep", encoding="utf-8")
            unsafe_start_root = allowed_root / "owned" / ".." / "other-target"

            result = subprocess.run(
                ["sh", str(ROOT / "connectors/traefik/scripts/start-smoke.sh")],
                cwd=ROOT,
                env={
                    **os.environ,
                    "BUILD_ROOT": str(build_root),
                    "TRAEFIK_CONNECTOR_START_ROOT": str(unsafe_start_root),
                },
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 77)
            self.assertIn("dot components", result.stderr)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")
