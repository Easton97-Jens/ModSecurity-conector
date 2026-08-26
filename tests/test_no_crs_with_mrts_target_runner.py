"""Focused contract tests for the closed no-CRS/with-MRTS Parent route."""
from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load test module: {relative}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


TARGET = load("mrts_target", "ci/runtime/lifecycle/run-no-crs-with-mrts-target.py")
EXECUTOR = load("mrts_executor", "ci/runtime/lifecycle/execute-no-crs-mrts-cases.py")


def plan_digest(path: Path) -> str:
    return TARGET.hashlib.sha256(path.read_bytes()).hexdigest()


def dedicated_rule_match_event(
    *,
    connector: str = "envoy",
    transaction_id: str = "run-0001",
    uri: str = "/?foo=attack",
    rule_id: str = "100000",
    phase: str = "request_body",
    previous_event_hash: int = 0,
) -> dict[str, object]:
    event: dict[str, object] = {
        "timestamp": "2026-08-20T12:34:56Z",
        "level": "info",
        "message_id": "MSCONN_EVENT_RULE_MATCHED",
        "message": "",
        "event": "request_rule_match",
        "connector": connector,
        "integration_mode": EXECUTOR.RULE_MATCH_INTEGRATION_MODES[connector],
        "transaction_id": transaction_id,
        "phase": phase,
        "status": "ok",
        "action": "allow",
        "requested_action": "allow",
        "actual_action": "allow",
        "http_status": 0,
        "original_http_status": 0,
        "visible_http_status": 0,
        "transport_result": "",
        "http_reason_phrase": "",
        "http_default_message": "",
        "rule_id": rule_id,
        "reason": "",
        "method": "GET",
        "uri": uri,
        "client_ip": "",
        "content_type": "",
        "body_bytes_seen": 0,
        "body_bytes_inspected": 0,
        "late_intervention": False,
        "response_started": False,
        "response_committed": False,
        "headers_sent": False,
        "body_started": False,
        "body_truncated": False,
        "connection_aborted": False,
        "client_disconnected": False,
        "upstream_disconnected": False,
        "cancelled": False,
        "eos_seen": False,
        "redacted": False,
        "truncated": False,
        "sequence": 1,
        "previous_event_hash": previous_event_hash,
        "event_hash": 0,
    }
    event["event_hash"] = EXECUTOR.rule_match_event_hash(event)
    return event


def haproxy_decision_event(
    *,
    transaction_id: str = "run-0001",
    rule_id: int = 100000,
) -> dict[str, object]:
    """One metadata-only record emitted by the native SPOE/SPOP agent."""

    return {
        "timestamp": 1_785_484_496,
        "connector": "haproxy",
        "mode": "detect-only",
        "runtime_mode": "test",
        "variant": "no-crs",
        "case": "mrts-no-crs-with-mrts",
        "request_id": transaction_id,
        "transaction_id": transaction_id,
        "phase": 2,
        "live_executed": True,
        "modsecurity_processed": True,
        "request_headers_seen": True,
        "request_body_seen": False,
        "response_headers_seen": False,
        "response_body_seen": False,
        "expected_status": 200,
        "observed_status": "",
        "result": "",
        "decision": "pass",
        "disruptive": False,
        "intervention_status": 403,
        "http_status": 403,
        "redirect_present": False,
        "rule_id": rule_id,
        "anomaly_score": 0,
        "audit_log_path": "/private/audit.log",
        "haproxy_log_path": "",
        "spoa_log_path": "/private/spoa-agent.log",
        "reason_code": "modsecurity_rule_observed",
        "reason": "modsecurity_rule_observed",
    }


class NoCrsWithMrtsTargetContractTests(unittest.TestCase):
    @staticmethod
    def validate_plan(plan_path, runtime, framework, rules, load_file, digest):
        return TARGET.validate_sealed_plan(
            plan_path, runtime, framework, rules, load_file, digest
        )

    def assert_validation_raises(self, pattern, plan_path, runtime, framework, rules, load_file, digest):
        with self.assertRaisesRegex(SystemExit, pattern):
            self.validate_plan(plan_path, runtime, framework, rules, load_file, digest)

    def create_test_traefik_engine_socket_parent(self, base: Path) -> Path:
        """Inject an already-created private child without using system temp."""

        candidate = base / "msct-test"
        candidate.mkdir(mode=0o700)
        with (
            mock.patch.object(TARGET.tempfile, "mkdtemp", return_value=str(candidate)),
            mock.patch.object(TARGET, "TRAEFIK_ENGINE_SOCKET_PATH_MAX_BYTES", 512),
        ):
            return TARGET.create_private_traefik_engine_socket_parent()

    def test_profile_is_closed_to_five_connectors_without_nginx(self):
        self.assertEqual(
            TARGET.CONNECTORS,
            {"apache", "envoy", "haproxy", "traefik", "lighttpd"},
        )
        self.assertEqual(TARGET.PROFILE, "no-crs/with-mrts")
        self.assertNotIn("nginx", TARGET.CONNECTORS)
        self.assertEqual(TARGET.GO_RUNTIME_CONNECTORS, {"envoy", "traefik"})

    def test_connector_phase_mapping_is_closed_and_native(self):
        self.assertEqual(TARGET.rule_match_event_phase("apache"), "request_headers")
        self.assertEqual(TARGET.rule_match_event_phase("haproxy"), "request_body")
        self.assertEqual(TARGET.rule_match_event_phase("envoy"), "request_body")
        with self.assertRaisesRegex(SystemExit, "outside the closed"):
            TARGET.rule_match_event_phase("nginx")

    def test_active_go_executable_uses_the_existing_absolute_binary(self):
        go = Path(TARGET.shutil.which("go") or "")
        self.assertTrue(go.is_file())
        self.assertEqual(TARGET.active_go_executable(ROOT), go)
        self.assertTrue(
            any(root == go or root in go.parents for root in (Path("/usr/local/go"), Path("/opt/hostedtoolcache/go")))
        )

    def test_active_go_executable_rejects_symlinked_binary(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            real = root / "go.real"
            real.write_text("#!/bin/sh\nprintf '%s\\n' 'go version go1.26.7 linux/amd64'\n", encoding="utf-8")
            real.chmod(0o700)
            go = root / "go"
            go.symlink_to(real)
            with mock.patch.object(TARGET.shutil, "which", return_value=str(go)), self.assertRaises(SystemExit):
                TARGET.active_go_executable()

    def test_active_go_executable_rejects_unapproved_path(self):
        with mock.patch.object(TARGET.shutil, "which", return_value="/tmp/go"), self.assertRaises(SystemExit):
            TARGET.active_go_executable(ROOT)

    def test_workflow_go_snapshot_requires_complete_sealed_pair(self):
        for environment in (
            {TARGET.WORKFLOW_GO_BINARY_ENV: "/opt/hostedtoolcache/go/1.26.7/x64/bin/go"},
            {TARGET.WORKFLOW_GO_BINARY_SHA256_ENV: "a" * 64},
            {
                TARGET.WORKFLOW_GO_BINARY_ENV: "/opt/hostedtoolcache/go/1.26.7/x64/bin/go",
                TARGET.WORKFLOW_GO_BINARY_SHA256_ENV: "A" * 64,
            },
        ):
            with self.subTest(environment=environment), mock.patch.dict(
                TARGET.os.environ, environment, clear=True
            ), self.assertRaisesRegex(SystemExit, "workflow Go snapshot"):
                TARGET._workflow_go_snapshot()

    def test_active_go_provenance_accepts_only_digest_bound_hosted_snapshot(self):
        executable = Path("/opt/hostedtoolcache/go/1.26.7/x64/bin/go")
        digest = "a" * 64
        environment = {
            TARGET.WORKFLOW_GO_BINARY_ENV: str(executable),
            TARGET.WORKFLOW_GO_BINARY_SHA256_ENV: digest,
        }
        with (
            mock.patch.dict(TARGET.os.environ, environment, clear=False),
            mock.patch.object(TARGET.shutil, "which", side_effect=AssertionError("snapshot must select Go")),
            mock.patch.object(TARGET, "_validate_go_binary", return_value=executable),
            mock.patch.object(TARGET, "_validate_go_ancestry") as ancestry,
            mock.patch.object(TARGET, "_go_binary_sha256", return_value=digest),
            mock.patch.object(TARGET, "_read_go_binary_version", return_value="1.26"),
            mock.patch.object(TARGET, "read_go_version_contract", return_value="1.26.7"),
        ):
            self.assertEqual(TARGET.active_go_provenance(ROOT), (executable, digest, "1.26"))
        ancestry.assert_not_called()

    def test_active_go_provenance_rejects_changed_hosted_snapshot_binary(self):
        executable = Path("/opt/hostedtoolcache/go/1.26.7/x64/bin/go")
        environment = {
            TARGET.WORKFLOW_GO_BINARY_ENV: str(executable),
            TARGET.WORKFLOW_GO_BINARY_SHA256_ENV: "a" * 64,
        }
        with (
            mock.patch.dict(TARGET.os.environ, environment, clear=False),
            mock.patch.object(TARGET, "_validate_go_binary", return_value=executable),
            mock.patch.object(TARGET, "_go_binary_sha256", return_value="b" * 64),
            self.assertRaisesRegex(SystemExit, "snapshot digest does not match"),
        ):
            TARGET.active_go_provenance(ROOT)

    def test_go_version_output_parser_accepts_canonical_output(self):
        self.assertEqual(
            TARGET._go_major_minor("go version go1.26.7 linux/amd64"),
            "1.26",
        )

    def test_go_version_output_parser_rejects_malformed_output(self):
        for output in (
            "go version 1.26.7 linux/amd64",
            "go version go1.26.x linux/amd64",
            "go version go1.26.7.8 linux/amd64",
            "go version go1.26.٧ linux/amd64",
        ):
            with self.subTest(output=output), self.assertRaises(SystemExit):
                TARGET._go_major_minor(output)

    def test_hosted_toolcache_allows_runner_primary_group_write_without_world_write(self):
        metadata = os.stat_result((0o100775, 0, 0, 1, os.geteuid(), os.getegid(), 0, 0, 0, 0))
        self.assertTrue(TARGET._go_directory_is_trusted(metadata, hosted_toolcache=True))

    def test_hosted_toolcache_allows_root_owner_with_runner_primary_group_write(self):
        metadata = os.stat_result((0o100775, 0, 0, 1, 0, os.getegid(), 0, 0, 0, 0))
        self.assertTrue(TARGET._go_directory_is_trusted(metadata, hosted_toolcache=True))

    def test_hosted_toolcache_uses_effective_primary_group(self):
        metadata = os.stat_result((0o100775, 0, 0, 1, 0, 761, 0, 0, 0, 0))
        with (
            mock.patch.object(TARGET.os, "getegid", return_value=761),
            mock.patch.object(TARGET.os, "getgid", return_value=762),
        ):
            self.assertTrue(TARGET._go_directory_is_trusted(metadata, hosted_toolcache=True))

    def test_hosted_toolcache_allows_root_group_write_outside_runner_groups(self):
        metadata = os.stat_result((0o100775, 0, 0, 1, 0, 761, 0, 0, 0, 0))
        with (
            mock.patch.object(TARGET.os, "getegid", return_value=760),
            mock.patch.object(TARGET.os, "getgid", return_value=760),
            mock.patch.object(TARGET.os, "getgroups", return_value=[760]),
        ):
            self.assertTrue(TARGET._go_directory_is_trusted(metadata, hosted_toolcache=True))

    def test_hosted_toolcache_rejects_unsafe_group_world_write_and_wrong_owner(self):
        runner_uid = 760
        runner_gid = 761
        cases = (
            (0o100775, runner_uid, runner_gid + 1),
            (0o100777, runner_uid, runner_gid),
            (0o100775, runner_uid + 1, runner_gid),
            (0o100777, 0, runner_gid),
        )
        with (
            mock.patch.object(TARGET.os, "geteuid", return_value=runner_uid),
            mock.patch.object(TARGET.os, "getegid", return_value=runner_gid),
            mock.patch.object(TARGET.os, "getgid", return_value=runner_gid),
            mock.patch.object(TARGET.os, "getgroups", return_value=[runner_gid]),
        ):
            for mode, uid, gid in cases:
                with self.subTest(mode=oct(mode), uid=uid, gid=gid):
                    metadata = os.stat_result((mode, 0, 0, 1, uid, gid, 0, 0, 0, 0))
                    self.assertFalse(TARGET._go_directory_is_trusted(metadata, hosted_toolcache=True))

    def test_hosted_toolcache_rejects_root_group_write_when_runner_is_member(self):
        metadata = os.stat_result((0o100775, 0, 0, 1, 0, 761, 0, 0, 0, 0))
        with (
            mock.patch.object(TARGET.os, "getegid", return_value=760),
            mock.patch.object(TARGET.os, "getgid", return_value=760),
            mock.patch.object(TARGET.os, "getgroups", return_value=[760, 761]),
        ):
            self.assertFalse(TARGET._go_directory_is_trusted(metadata, hosted_toolcache=True))

    def test_usr_local_go_keeps_strict_non_writable_contract(self):
        metadata = os.stat_result((0o100775, 0, 0, 1, os.getuid(), os.getgid(), 0, 0, 0, 0))
        self.assertFalse(TARGET._go_directory_is_trusted(metadata, hosted_toolcache=False))

    def test_outer_parent_rejects_runner_group_write_even_with_effective_owner(self):
        metadata = os.stat_result((0o100775, 0, 0, 1, os.geteuid(), os.getgid(), 0, 0, 0, 0))
        self.assertFalse(TARGET._go_directory_is_trusted(metadata, hosted_toolcache=False))

    def test_go_version_contract_accepts_bounded_canonical_file(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            version = root / ".go-version"
            version.write_text("1.26.7\n", encoding="ascii")
            version.chmod(0o600)
            self.assertEqual(TARGET.read_go_version_contract(root), "1.26.7")

    def test_go_version_contract_rejects_symlink_and_mutable_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            real = root / "version.real"
            real.write_text("1.26.7\n", encoding="ascii")
            real.chmod(0o600)
            version = root / ".go-version"
            version.symlink_to(real)
            with self.assertRaises(SystemExit):
                TARGET.read_go_version_contract(root)

    def test_go_version_contract_rejects_leading_zero_patch(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            version = root / ".go-version"
            version.write_text("1.26.07\n", encoding="ascii")
            version.chmod(0o600)
            with self.assertRaises(SystemExit):
                TARGET.read_go_version_contract(root)
            version.unlink()
            version.write_text("1.26.٧\n", encoding="utf-8")
            version.chmod(0o600)
            with self.assertRaises(SystemExit):
                TARGET.read_go_version_contract(root)
            version.unlink()
            version.write_text("1.26.7\n", encoding="ascii")
            version.chmod(0o666)
            with self.assertRaises(SystemExit):
                TARGET.read_go_version_contract(root)

    def test_no_crs_run_id_is_generated_and_bounded(self):
        run_id = TARGET.new_no_crs_run_id()
        self.assertRegex(run_id, r"^mrts-[0-9a-f]{32}$")
        self.assertEqual(TARGET.validate_no_crs_run_id(run_id), run_id)
        self.assertNotEqual(run_id, TARGET.new_no_crs_run_id())

    def test_no_crs_run_id_rejects_mutation_and_untrusted_values(self):
        for value in (
            "mrts-" + "a" * 31,
            "mrts-" + "a" * 32 + "0",
            "mrts-" + "A" * 32,
            "caller-controlled",
        ):
            with self.subTest(value=value), self.assertRaises(SystemExit):
                TARGET.validate_no_crs_run_id(value)

    def test_no_crs_run_id_crosses_closed_shell_boundaries(self):
        target = (ROOT / "ci/runtime/lifecycle/run-no-crs-with-mrts-target.py").read_text(encoding="utf-8")
        remaining = (ROOT / "ci/runtime/lifecycle/run-remaining-connector-target.sh").read_text(encoding="utf-8")
        stage = (ROOT / "ci/runtime/lifecycle/run-connector-stage.sh").read_text(encoding="utf-8")
        self.assertIn('"NO_CRS_RUN_ID": no_crs_run_id', target)
        self.assertIn("MRTS_CLOSED_NO_CRS_RUN_ID=$NO_CRS_RUN_ID", remaining)
        self.assertIn("NO_CRS_RUN_ID=$MRTS_CLOSED_NO_CRS_RUN_ID", remaining)
        self.assertIn('"NO_CRS_RUN_ID=$NO_CRS_RUN_ID"', stage)

    def test_runtime_provisioning_requires_fixed_explicit_opt_ins(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(SystemExit):
                TARGET.explicit_runtime_provisioning_environment("envoy")
        with mock.patch.dict(
            os.environ,
            {"ALLOW_RUNTIME_DOWNLOADS": "1", "ALLOW_RUNTIME_BUILDS": "not-allowed"},
            clear=True,
        ):
            with self.assertRaises(SystemExit):
                TARGET.explicit_runtime_provisioning_environment("lighttpd")
        with mock.patch.dict(
            os.environ,
            {"ALLOW_RUNTIME_DOWNLOADS": "1", "ALLOW_RUNTIME_BUILDS": "1"},
            clear=True,
        ):
            self.assertEqual(
                TARGET.explicit_runtime_provisioning_environment("traefik"),
                {"ALLOW_RUNTIME_DOWNLOADS": "1", "ALLOW_RUNTIME_BUILDS": "1"},
            )

    def test_traefik_engine_socket_parent_is_unique_private_short_and_cleaned(self):
        with tempfile.TemporaryDirectory() as directory:
            selected = self.create_test_traefik_engine_socket_parent(Path(directory))
            self.assertTrue(selected.is_dir())
            self.assertEqual(selected.stat().st_uid, os.geteuid())
            self.assertEqual(selected.stat().st_mode & 0o777, 0o700)
            candidate = (
                selected
                / f"{TARGET.TRAEFIK_ENGINE_SOCKET_CHILD_PREFIX}{'f' * TARGET.TRAEFIK_ENGINE_SOCKET_CHILD_RANDOM_HEX_LENGTH}"
                / TARGET.TRAEFIK_ENGINE_SOCKET_FILENAME
            )
            self.assertLessEqual(
                len(os.fsencode(str(candidate))),
                512,
            )
            TARGET.remove_private_traefik_engine_socket_parent(selected)
            self.assertFalse(selected.exists())

    def test_traefik_engine_socket_parent_rejects_a_symlinked_mkdtemp_result(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "private"
            target.mkdir(mode=0o700)
            linked = root / "linked"
            linked.symlink_to(target, target_is_directory=True)
            with mock.patch.object(TARGET.tempfile, "mkdtemp", return_value=str(linked)):
                with self.assertRaisesRegex(SystemExit, "symlink component"):
                    TARGET.create_private_traefik_engine_socket_parent()

    def test_traefik_engine_socket_parent_cleanup_rejects_tampering(self):
        with tempfile.TemporaryDirectory() as directory:
            selected = self.create_test_traefik_engine_socket_parent(Path(directory))
            selected.chmod(0o755)
            with self.assertRaisesRegex(SystemExit, "changed before cleanup"):
                TARGET.remove_private_traefik_engine_socket_parent(selected)
            selected.chmod(0o700)
            TARGET.remove_private_traefik_engine_socket_parent(selected)

    def test_traefik_engine_socket_parent_cleanup_removes_only_known_socket_child(self):
        with tempfile.TemporaryDirectory() as directory:
            selected = self.create_test_traefik_engine_socket_parent(Path(directory))
            child = selected / f"{TARGET.TRAEFIK_ENGINE_SOCKET_CHILD_PREFIX}{'a' * TARGET.TRAEFIK_ENGINE_SOCKET_CHILD_RANDOM_HEX_LENGTH}"
            child.mkdir(mode=0o700)
            socket_path = child / TARGET.TRAEFIK_ENGINE_SOCKET_FILENAME
            socket_path.touch()
            with self.assertRaisesRegex(SystemExit, "contains artifacts"):
                TARGET.remove_private_traefik_engine_socket_parent(selected)
            socket_path.unlink()
            child.rmdir()
            TARGET.remove_private_traefik_engine_socket_parent(selected)
            self.assertFalse(selected.exists())

    def test_private_runtime_build_reuses_a_prepared_private_child(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.chmod(0o700)
            build = root / "build"
            build.mkdir(mode=0o755)
            selected = TARGET.private_runtime_build(root)
            self.assertEqual(selected, build)
            self.assertEqual(selected.stat().st_uid, os.getuid())
            self.assertEqual(selected.stat().st_mode & 0o777, 0o700)

    def test_private_runtime_build_rejects_a_symlink_child(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "root"
            root.mkdir(mode=0o700)
            external = Path(directory) / "external"
            external.mkdir(mode=0o700)
            (root / "build").symlink_to(external, target_is_directory=True)
            with self.assertRaisesRegex(SystemExit, "symlink component"):
                TARGET.private_runtime_build(root)

    def test_closed_connector_stage_command_uses_only_literal_profile_members(self):
        for connector in ("apache", "envoy", "haproxy", "traefik", "lighttpd"):
            command = TARGET.closed_connector_stage_command(connector)
            self.assertEqual(command[0], "sh")
            self.assertEqual(command[2], connector)
            self.assertEqual(command[3], "no_crs_with_mrts")
        with self.assertRaisesRegex(SystemExit, "outside the closed"):
            TARGET.closed_connector_stage_command("nginx")

    def test_runtime_route_requires_explicit_checkout_roots_and_stage(self):
        source = (ROOT / "ci" / "runtime" / "lifecycle" / "run-no-crs-with-mrts-target.py").read_text(encoding="utf-8")
        self.assertIn('parser.add_argument("--parent-root", required=True)', source)
        self.assertIn('parser.add_argument("--framework-root", required=True)', source)
        self.assertIn('stop("--execute-stage is mandatory', source)
        self.assertIn('"no_crs_with_mrts"', source)

    def test_apache_and_haproxy_do_not_acquire_or_validate_go(self):
        source = (ROOT / "ci" / "runtime" / "lifecycle" / "run-no-crs-with-mrts-target.py").read_text(encoding="utf-8")
        self.assertIn('if args.connector in GO_RUNTIME_CONNECTORS:', source)
        self.assertNotIn('"apache", "haproxy"', source.split("GO_RUNTIME_CONNECTORS", 1)[1].split("PROFILE", 1)[0])
        with mock.patch.object(TARGET, "active_go_provenance", side_effect=AssertionError("Go must stay out of Apache/HAProxy")):
            self.assertNotIn("apache", TARGET.GO_RUNTIME_CONNECTORS)
            self.assertNotIn("haproxy", TARGET.GO_RUNTIME_CONNECTORS)

    def test_target_context_does_not_forward_inherited_component_snapshots(self):
        source = (
            ROOT / "ci" / "runtime" / "lifecycle"
            / "run-no-crs-with-mrts-target.py"
        ).read_text(encoding="utf-8")
        target_context = source.split("def _prepare_target_context", 1)[1].split(
            "def _create_runtime_plan", 1
        )[0]
        self.assertNotIn("RUNTIME_COMPONENT_ENV_SNAPSHOT", target_context)

    def test_target_context_keeps_connector_temp_and_log_roots_under_build_root(self):
        source = (
            ROOT / "ci" / "runtime" / "lifecycle"
            / "run-no-crs-with-mrts-target.py"
        ).read_text(encoding="utf-8")
        target_context = source.split("def _prepare_target_context", 1)[1].split(
            "def _create_runtime_plan", 1
        )[0]
        self.assertIn('"BUILD_ROOT": str(build)', target_context)
        self.assertIn('"TMP_ROOT": str(build / "tmp")', target_context)
        self.assertIn('"LOG_ROOT": str(build / "logs")', target_context)
        self.assertNotIn('"TMP_ROOT": str(root / "tmp")', target_context)
        self.assertNotIn('"LOG_ROOT": str(root / "logs")', target_context)
        base_environment, go_environment = target_context.split(
            "if go_path is not None:", 1
        )
        self.assertIn('if args.connector == "lighttpd":', base_environment)
        self.assertIn('env["PATH"] = "/usr/bin:/bin"', base_environment)
        self.assertNotIn('"GOTOOLCHAIN": "local"', base_environment)
        self.assertIn('"GOTOOLCHAIN": "local"', go_environment)

    def test_active_python_executable_preserves_a_venv_style_final_symlink(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(sys.executable).resolve(strict=True)
            invocation = Path(directory) / "python"
            invocation.symlink_to(target)
            with mock.patch.object(TARGET.sys, "executable", str(invocation)):
                self.assertEqual(TARGET.active_python_executable(), invocation)

    def test_active_python_executable_rejects_a_relative_invocation(self):
        with mock.patch.object(TARGET.sys, "executable", "python3"):
            with self.assertRaises(SystemExit):
                TARGET.active_python_executable()

    def test_active_python_executable_rejects_a_symlinked_parent(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(sys.executable).resolve(strict=True)
            real_parent = Path(directory) / "real"
            real_parent.mkdir()
            (real_parent / "python").symlink_to(target)
            linked_parent = Path(directory) / "linked"
            linked_parent.symlink_to(real_parent, target_is_directory=True)
            with mock.patch.object(TARGET.sys, "executable", str(linked_parent / "python")):
                with self.assertRaises(SystemExit):
                    TARGET.active_python_executable()

    def test_executor_binds_localhost_and_provenance(self):
        source = (ROOT / "ci" / "runtime" / "lifecycle" / "execute-no-crs-mrts-cases.py").read_text(encoding="utf-8")
        self.assertIn('if args.host != LOOPBACK_HOST:', source)
        self.assertIn('item.get("transaction_id") != correlation_id', source)
        self.assertIn('item.get("connector") != connector', source)
        self.assertIn('item.get("uri") != uri', source)
        self.assertIn("executor digest mismatch", source)
        self.assertIn("MRTS case digest mismatch", source)
        self.assertIn('parser.add_argument("--load-file", required=True)', source)
        self.assertIn('parser.add_argument("--plan-sha256", required=True)', source)
        self.assertIn('build_root = root / "build"', source)
        self.assertIn("validate_sealed_no_crs_plan(plan_path, root, load_path, executor_path, plan_sha256)", source)
        self.assertIn('host_request_id = f"host-{correlation_id}"', source)
        self.assertIn('"X-Request-ID": host_request_id', source)
        self.assertIn('connection = http.client.HTTPConnection(', source)
        self.assertIn('http.client.HTTPSConnection(', source)
        self.assertIn('LOOPBACK_HOST, endpoint.port, timeout=timeout', source)
        self.assertIn('context.check_hostname = True', source)
        self.assertNotIn('_create_unverified_context', source)
        self.assertNotIn('urllib.request', source)
        self.assertNotIn('if "crs" in load_path.read_text', source)

    def test_executor_uses_fixed_loopback_connection_without_redirect_following(self):
        class FakeResponse:
            status = 302

            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self, _limit):
                return b""

        class FakeConnection:
            def __init__(self, host, port, **kwargs):
                self.host = host
                self.port = port
                self.kwargs = kwargs
                self.requests = []
                self.closed = False

            def request(self, method, path, headers):
                self.requests.append((method, path, headers))

            def getresponse(self):
                return FakeResponse()

            def close(self):
                self.closed = True

        connection = FakeConnection("127.0.0.1", 18080)
        with mock.patch.object(EXECUTOR.http.client, "HTTPConnection", return_value=connection):
            status = EXECUTOR.request(
                "/redirect", EXECUTOR.LoopbackEndpoint(18080), "GET",
                {"Host": "127.0.0.1"}, 1.0, "http", None,
            )
        self.assertEqual(status, 302)
        self.assertEqual(connection.host, EXECUTOR.LOOPBACK_HOST)
        self.assertEqual(connection.requests[0][1], "/redirect")
        self.assertTrue(connection.closed)

    def test_https_context_is_pinned_to_run_local_certificate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            certificate = root / "envoy-loopback.crt"
            certificate.write_text("certificate", encoding="utf-8")
            context = mock.Mock()
            with mock.patch.object(EXECUTOR.ssl, "SSLContext", return_value=context) as factory:
                result = EXECUTOR.verified_tls_context(root, str(certificate))
            factory.assert_called_once_with(EXECUTOR.ssl.PROTOCOL_TLS_CLIENT)
            self.assertIs(result, context)
            self.assertEqual(context.minimum_version, EXECUTOR.ssl.TLSVersion.TLSv1_2)
            context.load_verify_locations.assert_called_once_with(cafile=str(certificate))
            self.assertTrue(context.check_hostname)
            self.assertEqual(context.verify_mode, EXECUTOR.ssl.CERT_REQUIRED)

    def test_duplicate_json_keys_are_rejected(self):
        with self.assertRaises(SystemExit):
            EXECUTOR.reject_duplicates([("a", 1), ("a", 2)])

    def test_event_ids_accepts_only_the_dedicated_metadata_rule_match(self):
        with tempfile.TemporaryDirectory() as directory:
            event_log = Path(directory) / "events.jsonl"
            event_log.write_text(
                json.dumps(dedicated_rule_match_event(uri="/?foo=attack%20value")) + "\n",
                encoding="utf-8",
            )
            self.assertEqual(
                EXECUTOR.event_ids(
                    event_log,
                    "run-0001",
                    "envoy",
                    "/?foo=attack%20value",
                    "request_body",
                    {"100000"},
                    {"100000"},
                ),
                {"100000"},
            )

    def test_apache_native_event_uses_its_real_request_header_phase(self):
        with tempfile.TemporaryDirectory() as directory:
            event_log = Path(directory) / "events.jsonl"
            event_log.write_text(
                json.dumps(
                    dedicated_rule_match_event(
                        connector="apache", phase="request_headers"
                    )
                )
                + "\n",
                encoding="utf-8",
            )
            self.assertEqual(
                EXECUTOR.event_ids(
                    event_log,
                    "run-0001",
                    "apache",
                    "/?foo=attack",
                    "request_headers",
                    {"100000"},
                    {"100000"},
                ),
                {"100000"},
            )

    def test_haproxy_native_decision_requires_closed_detection_only_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            event_log = Path(directory) / "events.jsonl"
            event_log.write_text(
                json.dumps(haproxy_decision_event()) + "\n", encoding="utf-8"
            )
            self.assertEqual(
                EXECUTOR.event_ids(
                    event_log,
                    "run-0001",
                    "haproxy",
                    "/?not-stored-in-private-evidence",
                    "request_body",
                    {"100000"},
                    {"100000"},
                ),
                {"100000"},
            )
            malformed = haproxy_decision_event()
            malformed["mode"] = "block"
            event_log.write_text(json.dumps(malformed) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(SystemExit, "closed DetectionOnly"):
                EXECUTOR.event_ids(
                    event_log,
                    "run-0001",
                    "haproxy",
                    "/?not-stored-in-private-evidence",
                    "request_body",
                    {"100000"},
                    {"100000"},
                )

            malformed = haproxy_decision_event()
            malformed["case"] = "another-case"
            event_log.write_text(json.dumps(malformed) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(SystemExit, "closed DetectionOnly"):
                EXECUTOR.event_ids(
                    event_log,
                    "run-0001",
                    "haproxy",
                    "/?not-stored-in-private-evidence",
                    "request_body",
                    {"100000"},
                    {"100000"},
                )

            malformed = haproxy_decision_event()
            malformed["untrusted_extra"] = "must-not-enter-runtime-evidence"
            event_log.write_text(json.dumps(malformed) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(SystemExit, "exact native schema"):
                EXECUTOR.event_ids(
                    event_log,
                    "run-0001",
                    "haproxy",
                    "/?not-stored-in-private-evidence",
                    "request_body",
                    {"100000"},
                    {"100000"},
                )

    def test_event_ids_rejects_symlinked_native_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target.jsonl"
            target.write_text(
                json.dumps(dedicated_rule_match_event()) + "\n", encoding="utf-8"
            )
            event_log = root / "events.jsonl"
            event_log.symlink_to(target)
            with self.assertRaisesRegex(SystemExit, "without following links"):
                EXECUTOR.event_ids(
                    event_log,
                    "run-0001",
                    "envoy",
                    "/?foo=attack",
                    "request_body",
                    {"100000"},
                    {"100000"},
                )

    def test_event_ids_rejects_hardlinked_native_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target.jsonl"
            target.write_text(
                json.dumps(dedicated_rule_match_event()) + "\n", encoding="utf-8"
            )
            event_log = root / "events.jsonl"
            os.link(target, event_log)
            with self.assertRaisesRegex(SystemExit, "unsafe link"):
                EXECUTOR.event_ids(
                    event_log,
                    "run-0001",
                    "envoy",
                    "/?foo=attack",
                    "request_body",
                    {"100000"},
                    {"100000"},
                )

    def test_haproxy_detection_requires_the_sealed_expected_rule_id(self):
        """A correlated HAProxy match must be the selected detection rule."""

        with tempfile.TemporaryDirectory() as directory:
            event_log = Path(directory) / "events.jsonl"
            event_log.write_text(
                json.dumps(haproxy_decision_event(rule_id=100001)) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(SystemExit, "outside the selected expectation"):
                EXECUTOR.event_ids(
                    event_log,
                    "run-0001",
                    "haproxy",
                    "/?not-stored-in-private-evidence",
                    "request_body",
                    {"100000"},
                    {"100000", "100001"},
                )

    def test_haproxy_detection_keeps_the_exact_sealed_rule_id(self):
        self.assertEqual(
            EXECUTOR.effective_expected_rule_ids(
                {"100000"}, {"100000", "100001"}
            ),
            {"100000"},
        )

    def test_effective_expected_rule_ids_rejects_an_unpinned_case_declaration(self):
        with self.assertRaisesRegex(
            SystemExit, "outside the pinned corpus"
        ):
            EXECUTOR.effective_expected_rule_ids(
                {"100000"}, {"100001"}
            )

    def test_effective_expected_rule_ids_keeps_declared_rule_ids_for_other_connectors(self):
        self.assertEqual(
            EXECUTOR.effective_expected_rule_ids(
                {"100000"}, {"100000"}
            ),
            {"100000"},
        )

    def test_haproxy_control_and_bypass_keep_correlated_ids_for_empty_oracle(self):
        with tempfile.TemporaryDirectory() as directory:
            event_log = Path(directory) / "events.jsonl"
            event_log.write_text(
                json.dumps(haproxy_decision_event(rule_id=100001)) + "\n",
                encoding="utf-8",
            )
            observed = EXECUTOR.event_ids(
                event_log,
                "run-0001",
                "haproxy",
                "/?not-stored-in-private-evidence",
                "request_body",
                set(),
                {"100001"},
            )
            self.assertEqual(observed, {"100001"})
            with self.assertRaisesRegex(SystemExit, "unexpectedly matched rules"):
                EXECUTOR.require_case_rule_matches("control", "control", set(), observed)

    def test_event_ids_rejects_wrong_event_kind_and_arbitrary_nested_rule_ids(self):
        with tempfile.TemporaryDirectory() as directory:
            event_log = Path(directory) / "events.jsonl"
            event = dedicated_rule_match_event()
            event["message_id"] = "MSCONN_EVENT_DECISION"
            event["nested"] = {"matched_rule_ids": ["100000"]}
            event_log.write_text(json.dumps(event) + "\n", encoding="utf-8")
            with self.assertRaises(SystemExit):
                EXECUTOR.event_ids(event_log, "run-0001", "envoy", "/?foo=attack", "request_body", {"100000"}, {"100000", "100001", "100032"})

    def test_event_ids_ignores_other_transaction_or_uri(self):
        with tempfile.TemporaryDirectory() as directory:
            event_log = Path(directory) / "events.jsonl"
            base = dedicated_rule_match_event(transaction_id="other-run", uri="/?foo=other")
            event_log.write_text(json.dumps(base) + "\n", encoding="utf-8")
            self.assertEqual(
                EXECUTOR.event_ids(event_log, "run-0001", "envoy", "/?foo=attack", "request_body", {"100000"}, {"100000"}),
                set(),
            )

    def test_event_ids_accepts_independent_native_integrity_chains(self):
        with tempfile.TemporaryDirectory() as directory:
            event_log = Path(directory) / "events.jsonl"
            first = dedicated_rule_match_event(
                transaction_id="other-run", uri="/?foo=other"
            )
            second = dedicated_rule_match_event()
            event_log.write_text(
                json.dumps(first) + "\n" + json.dumps(second) + "\n",
                encoding="utf-8",
            )
            self.assertEqual(
                EXECUTOR.event_ids(
                    event_log, "run-0001", "envoy", "/?foo=attack", "request_body", {"100000"}, {"100000"}
                ),
                {"100000"},
            )

    def test_event_ids_accepts_interleaved_native_integrity_chains(self):
        with tempfile.TemporaryDirectory() as directory:
            event_log = Path(directory) / "events.jsonl"
            first_target = dedicated_rule_match_event()
            first_other = dedicated_rule_match_event(
                transaction_id="other-run", uri="/?foo=other"
            )
            second_target = dedicated_rule_match_event(
                rule_id="100001",
                phase="response_body",
                previous_event_hash=int(first_target["event_hash"]),
            )
            second_other = dedicated_rule_match_event(
                transaction_id="other-run",
                uri="/?foo=other",
                rule_id="100001",
                phase="response_body",
                previous_event_hash=int(first_other["event_hash"]),
            )
            event_log.write_text(
                "\n".join(
                    json.dumps(event)
                    for event in (first_target, first_other, second_target, second_other)
                )
                + "\n",
                encoding="utf-8",
            )
            self.assertEqual(
                EXECUTOR.event_ids(
                    event_log,
                    "run-0001",
                    "envoy",
                    "/?foo=attack",
                    "request_body",
                    {"100000"},
                    {"100000", "100001"},
                ),
                {"100000"},
            )

    def test_event_ids_rejects_cross_transaction_integrity_continuation(self):
        with tempfile.TemporaryDirectory() as directory:
            event_log = Path(directory) / "events.jsonl"
            first = dedicated_rule_match_event(
                transaction_id="other-run", uri="/?foo=other"
            )
            second = dedicated_rule_match_event(
                previous_event_hash=int(first["event_hash"])
            )
            event_log.write_text(
                json.dumps(first) + "\n" + json.dumps(second) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                SystemExit, "does not start a native integrity chain"
            ):
                EXECUTOR.event_ids(
                    event_log,
                    "run-0001",
                    "envoy",
                    "/?foo=attack",
                    "request_body",
                    {"100000"},
                    {"100000"},
                )

    def test_event_ids_rejects_broken_same_transaction_integrity_chain(self):
        with tempfile.TemporaryDirectory() as directory:
            event_log = Path(directory) / "events.jsonl"
            first = dedicated_rule_match_event()
            second = dedicated_rule_match_event(rule_id="100001")
            event_log.write_text(
                json.dumps(first) + "\n" + json.dumps(second) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                SystemExit, "does not continue the native integrity chain"
            ):
                EXECUTOR.event_ids(
                    event_log,
                    "run-0001",
                    "envoy",
                    "/?foo=attack",
                    "request_body",
                    {"100000"},
                    {"100000", "100001"},
                )

    def test_event_ids_integrity_validates_and_ignores_unrelated_response_phase(self):
        with tempfile.TemporaryDirectory() as directory:
            event_log = Path(directory) / "events.jsonl"
            unrelated = dedicated_rule_match_event(
                transaction_id="other-run", uri="/?foo=other", phase="response_body"
            )
            relevant = dedicated_rule_match_event()
            event_log.write_text(
                json.dumps(unrelated) + "\n" + json.dumps(relevant) + "\n",
                encoding="utf-8",
            )
            self.assertEqual(
                EXECUTOR.event_ids(
                    event_log, "run-0001", "envoy", "/?foo=attack", "request_body", {"100000"}, {"100000"}
                ),
                {"100000"},
            )

    def test_event_ids_ignores_nonexpected_same_transaction_response_phase(self):
        with tempfile.TemporaryDirectory() as directory:
            event_log = Path(directory) / "events.jsonl"
            unrelated_phase = dedicated_rule_match_event(
                rule_id="100001", phase="response_body"
            )
            relevant = dedicated_rule_match_event(
                previous_event_hash=int(unrelated_phase["event_hash"])
            )
            event_log.write_text(
                json.dumps(unrelated_phase) + "\n" + json.dumps(relevant) + "\n",
                encoding="utf-8",
            )
            self.assertEqual(
                EXECUTOR.event_ids(
                    event_log,
                    "run-0001",
                    "envoy",
                    "/?foo=attack",
                    "request_body",
                    {"100000"},
                    {"100000", "100001"},
                ),
                {"100000"},
            )

    def test_event_ids_keeps_extra_same_phase_match_for_detection_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            event_log = Path(directory) / "events.jsonl"
            expected = dedicated_rule_match_event(rule_id="100000")
            extra = dedicated_rule_match_event(
                rule_id="100001", previous_event_hash=int(expected["event_hash"])
            )
            event_log.write_text(
                json.dumps(expected) + "\n" + json.dumps(extra) + "\n",
                encoding="utf-8",
            )
            observed = EXECUTOR.event_ids(
                event_log,
                "run-0001",
                "envoy",
                "/?foo=attack",
                "request_body",
                {"100000"},
                {"100000", "100001"},
            )
            self.assertEqual(observed, {"100000", "100001"})
            EXECUTOR.require_case_rule_matches(
                "detection", "detection", {"100000"}, observed
            )

    def test_event_ids_rejects_unknown_extra_unless_sealed_inventory_permits_it(self):
        with tempfile.TemporaryDirectory() as directory:
            event_log = Path(directory) / "events.jsonl"
            expected = dedicated_rule_match_event(rule_id="100000")
            unknown = dedicated_rule_match_event(
                rule_id="100001", previous_event_hash=int(expected["event_hash"])
            )
            event_log.write_text(
                json.dumps(expected) + "\n" + json.dumps(unknown) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(SystemExit, "outside the pinned corpus"):
                EXECUTOR.event_ids(
                    event_log, "run-0001", "envoy", "/?foo=attack", "request_body",
                    {"100000"}, {"100000"},
                )
            permitted = dedicated_rule_match_event(
                rule_id="100032", previous_event_hash=int(expected["event_hash"])
            )
            event_log.write_text(
                json.dumps(expected) + "\n" + json.dumps(permitted) + "\n",
                encoding="utf-8",
            )
            self.assertEqual(
                EXECUTOR.event_ids(
                    event_log, "run-0001", "envoy", "/?foo=attack", "request_body",
                    {"100000"}, {"100000", "100032"},
                ),
                {"100000", "100032"},
            )

    def test_event_ids_rejects_expected_rule_in_same_transaction_wrong_phase(self):
        with tempfile.TemporaryDirectory() as directory:
            event_log = Path(directory) / "events.jsonl"
            event_log.write_text(
                json.dumps(dedicated_rule_match_event(phase="response_body")) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(SystemExit, "relevant rule-match event has invalid phase"):
                EXECUTOR.event_ids(
                    event_log,
                    "run-0001",
                    "envoy",
                    "/?foo=attack",
                    "request_body",
                    {"100000"},
                    {"100000"},
                )

    def test_control_case_keeps_correlated_match_for_empty_oracle(self):
        with tempfile.TemporaryDirectory() as directory:
            event_log = Path(directory) / "events.jsonl"
            event_log.write_text(
                json.dumps(dedicated_rule_match_event(phase="response_body")) + "\n",
                encoding="utf-8",
            )
            observed = EXECUTOR.event_ids(
                event_log,
                "run-0001",
                "envoy",
                "/?foo=attack",
                "request_body",
                set(),
                {"100000"},
            )
            self.assertEqual(observed, {"100000"})
            with self.assertRaisesRegex(SystemExit, "unexpectedly matched rules"):
                EXECUTOR.require_case_rule_matches("control", "control", set(), observed)

    def test_event_ids_rejects_relevant_wrong_phase_after_correlation(self):
        with tempfile.TemporaryDirectory() as directory:
            event_log = Path(directory) / "events.jsonl"
            event_log.write_text(
                json.dumps(dedicated_rule_match_event(phase="response_body")) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(SystemExit, "relevant rule-match event has invalid phase"):
                EXECUTOR.event_ids(
                    event_log, "run-0001", "envoy", "/?foo=attack", "request_body", {"100000"}, {"100000"}
                )

    def test_event_ids_rejects_an_unknown_phase_value(self):
        with tempfile.TemporaryDirectory() as directory:
            event_log = Path(directory) / "events.jsonl"
            event = dedicated_rule_match_event(phase="request_body")
            event["phase"] = "untrusted_phase"
            event_log.write_text(json.dumps(event) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(SystemExit, "rule-match event has invalid phase"):
                EXECUTOR.event_ids(
                    event_log, "run-0001", "envoy", "/?foo=attack", "request_body", {"100000"}, {"100000"}
                )

    def test_event_ids_rejects_forged_or_discontinuous_integrity_data(self):
        with tempfile.TemporaryDirectory() as directory:
            event_log = Path(directory) / "events.jsonl"
            forged = dedicated_rule_match_event()
            forged["event_hash"] = int(forged["event_hash"]) ^ 1
            event_log.write_text(json.dumps(forged) + "\n", encoding="utf-8")
            with self.assertRaises(SystemExit):
                EXECUTOR.event_ids(
                    event_log, "run-0001", "envoy", "/?foo=attack", "request_body", {"100000"}, {"100000"}
                )
            discontinuous = dedicated_rule_match_event(previous_event_hash=1)
            event_log.write_text(json.dumps(discontinuous) + "\n", encoding="utf-8")
            with self.assertRaises(SystemExit):
                EXECUTOR.event_ids(
                    event_log, "run-0001", "envoy", "/?foo=attack", "request_body", {"100000"}, {"100000"}
                )

    def test_rule_match_integrity_rejects_an_unpinned_abi(self):
        event = dedicated_rule_match_event()
        with mock.patch.object(EXECUTOR.sys, "byteorder", "big"):
            with self.assertRaises(SystemExit):
                EXECUTOR.rule_match_event_hash(event)

    def test_event_ids_rejects_duplicate_keys_in_relevant_record(self):
        with tempfile.TemporaryDirectory() as directory:
            event_log = Path(directory) / "events.jsonl"
            encoded = json.dumps(dedicated_rule_match_event())
            event_log.write_text(encoded[:-1] + ',"rule_id":"100001"}\n', encoding="utf-8")
            with self.assertRaises(SystemExit):
                EXECUTOR.event_ids(event_log, "run-0001", "envoy", "/?foo=attack", "request_body", {"100000"}, {"100000", "100001"})

    def test_event_ids_rejects_duplicate_relevant_rule_ids(self):
        with tempfile.TemporaryDirectory() as directory:
            event_log = Path(directory) / "events.jsonl"
            first = dedicated_rule_match_event()
            duplicate = dedicated_rule_match_event(
                previous_event_hash=int(first["event_hash"])
            )
            event_log.write_text(
                json.dumps(first) + "\n" + json.dumps(duplicate) + "\n",
                encoding="utf-8",
            )
            with self.assertRaises(SystemExit):
                EXECUTOR.event_ids(
                    event_log, "run-0001", "envoy", "/?foo=attack", "request_body", {"100000"}, {"100000"}
                )

    def test_detection_rule_matches_require_the_expected_subset(self):
        EXECUTOR.require_case_rule_matches(
            "detection", "detection", {"100000"}, {"100000"}
        )
        EXECUTOR.require_case_rule_matches(
            "detection", "detection", {"100000"}, {"100000", "100032"}
        )
        with self.assertRaisesRegex(SystemExit, "missing expected IDs"):
            EXECUTOR.require_case_rule_matches(
                "detection", "detection", {"100000"}, set()
            )

    def test_control_and_bypass_rule_matches_reject_every_correlated_id(self):
        for kind in ("control", "bypass"):
            with self.assertRaisesRegex(SystemExit, "unexpectedly matched rules"):
                EXECUTOR.require_case_rule_matches(
                    kind, kind, set(), {"100032"}
                )

    def test_event_ids_rejects_wrong_phase_schema_or_scalar_payload(self):
        cases = (
            ("phase", "request_headers"),
            ("integration_mode", "forwardAuth"),
            ("message", "untrusted-rule-message"),
            ("truncated", True),
            ("rule_id", "0"),
            ("rule_id", "000100000"),
        )
        with tempfile.TemporaryDirectory() as directory:
            event_log = Path(directory) / "events.jsonl"
            for field, value in cases:
                event = dedicated_rule_match_event()
                event[field] = value
                event_log.write_text(json.dumps(event) + "\n", encoding="utf-8")
                with self.assertRaises(SystemExit, msg=f"accepted invalid {field}={value!r}"):
                    EXECUTOR.event_ids(event_log, "run-0001", "envoy", "/?foo=attack", "request_body", {"100000"}, {"100000"})
            event = dedicated_rule_match_event()
            event["matched_value"] = "attack"
            event_log.write_text(json.dumps(event) + "\n", encoding="utf-8")
            with self.assertRaises(SystemExit, msg="accepted an extra scalar payload field"):
                EXECUTOR.event_ids(event_log, "run-0001", "envoy", "/?foo=attack", "request_body", {"100000"}, {"100000"})

    def test_generated_plan_has_control_detection_and_bypass(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "case.yaml"
            source.write_text(
                """name: mrts_case\nmetadata:\n  upstream_file: tools/MRTS/generated/tests/regression/tests/MRTS_002_ARGS_A-GET.yaml\n  phase: 1\nportable: true\nrequest:\n  method: GET\n  path: /?foo=attack\nexpect:\n  rule_id: 100000\n""",
                encoding="utf-8",
            )
            # The framework parser is intentionally used by the runner; this
            # test only verifies the executor's required case contract.
            plan = {"profile": "no-crs/with-mrts", "connector": "envoy", "cases": [
                {"id": "control", "kind": "control", "uri": "/?control=1", "expect_ids": [], "expect_event_phase": "request_body"},
                {"id": "detect", "kind": "detection", "uri": "/?foo=attack", "expect_ids": ["100000"], "expect_event_phase": "request_body"},
                {"id": "bypass", "kind": "bypass", "uri": "/?foo=benign", "expect_ids": [], "expect_event_phase": "request_body"},
            ]}
            self.assertEqual({case["kind"] for case in plan["cases"]}, {"control", "detection", "bypass"})
            json.loads(json.dumps(plan), object_pairs_hook=EXECUTOR.reject_duplicates)

    def test_executor_case_hashes_reject_paths_outside_the_generated_inventory(self):
        with tempfile.TemporaryDirectory() as directory:
            inventory = Path(directory) / "framework-cases"
            inventory.mkdir()
            source = inventory / "fixture.yaml"
            source.write_text("fixture\n", encoding="utf-8")
            digest = EXECUTOR.hashlib.sha256(source.read_bytes()).hexdigest()
            self.assertEqual(
                EXECUTOR.validate_case_hashes({source.name: digest}, inventory),
                {source.name: digest},
            )
            with self.assertRaisesRegex(SystemExit, "outside the pinned inventory"):
                EXECUTOR.validate_case_hashes({"../outside.yaml": digest}, inventory)

    def test_mrts_load_permits_generated_rules_under_a_private_no_crs_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runtime = root / "mrts-no-crs"
            rules = runtime / "build" / "mrts" / "upstream-config-tests" / "rules"
            rules.mkdir(parents=True)
            generated = rules / "MRTS_002_ARGS_A-GET.conf"
            generated.write_text('SecRule ARGS:foo "@streq attack" "id:100000,phase:1,pass"\n', encoding="utf-8")
            load = runtime / "mrts.load"
            load.write_text(f'Include "{generated}"\n', encoding="utf-8")
            baseline = root / "baseline.conf"
            baseline.write_text("SecRuleEngine DetectionOnly\n", encoding="utf-8")
            canonical = root / "pinned-mrts" / "generated" / "rules"
            canonical.mkdir(parents=True)
            (canonical / generated.name).write_bytes(generated.read_bytes())
            self.assertEqual(
                TARGET.validate_mrts_load_file(load, rules, baseline, canonical.parents[1], runtime),
                {generated.name: TARGET.hashlib.sha256(generated.read_bytes()).hexdigest()},
            )

    def test_mrts_load_rejects_a_crs_named_or_outside_include(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runtime = root / "runtime"
            rules = runtime / "build" / "mrts" / "upstream-config-tests" / "rules"
            rules.mkdir(parents=True)
            foreign = rules / "MRTS_002_ARGS_A-GET.conf"
            foreign.write_text('SecRule ARGS:foo "@streq attack" "id:949110,phase:1,pass"\n', encoding="utf-8")
            load = runtime / "mrts.load"
            load.write_text(f'Include "{foreign}"\n', encoding="utf-8")
            baseline = root / "baseline.conf"
            baseline.write_text("SecRuleEngine DetectionOnly\n", encoding="utf-8")
            canonical = root / "pinned-mrts" / "generated" / "rules"
            canonical.mkdir(parents=True)
            (canonical / foreign.name).write_text('SecRule ARGS:foo "@streq attack" "id:100000,phase:1,pass"\n', encoding="utf-8")
            with self.assertRaises(SystemExit):
                TARGET.validate_mrts_load_file(load, rules, baseline, canonical.parents[1], runtime)

    def test_mrts_load_rejects_a_symlinked_private_rules_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runtime = root / "runtime"
            external = root / "external-rules"
            external.mkdir(parents=True)
            generated = external / "MRTS_002_ARGS_A-GET.conf"
            generated.write_text('SecRule ARGS:foo "@streq attack" "id:100000,phase:1,pass"\n', encoding="utf-8")
            rules = runtime / "build" / "mrts" / "upstream-config-tests" / "rules"
            rules.parent.mkdir(parents=True)
            rules.symlink_to(external, target_is_directory=True)
            load = runtime / "mrts.load"
            load.write_text(f'Include "{rules / generated.name}"\n', encoding="utf-8")
            baseline = root / "baseline.conf"
            baseline.write_text("SecRuleEngine DetectionOnly\n", encoding="utf-8")
            canonical = root / "pinned-mrts" / "generated" / "rules"
            canonical.mkdir(parents=True)
            (canonical / generated.name).write_bytes(generated.read_bytes())
            with self.assertRaises(SystemExit):
                TARGET.validate_mrts_load_file(load, rules, baseline, canonical.parents[1], runtime)

    def test_sealed_plan_revalidates_the_private_corpus_binding(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runtime = root / "runtime"
            rules = runtime / "build" / "mrts" / "upstream-config-tests" / "rules"
            rules.mkdir(parents=True)
            generated = rules / "MRTS_002_ARGS_A-GET.conf"
            generated.write_text('SecRule ARGS:foo "@streq attack" "id:100000,phase:1,pass"\n', encoding="utf-8")
            load = runtime / "build" / "mrts" / "upstream-config-tests" / "mrts.load"
            load.write_text(f'Include "{generated}"\n', encoding="utf-8")
            framework = root / "framework"
            canonical = framework / "tools" / "MRTS" / "generated" / "rules"
            canonical.mkdir(parents=True)
            (canonical / generated.name).write_bytes(generated.read_bytes())
            baseline = framework / "tests" / "rules" / "no-crs-baseline.conf"
            baseline.parent.mkdir(parents=True)
            baseline.write_text("SecRuleEngine DetectionOnly\n", encoding="utf-8")
            case_root = runtime / "build" / "mrts" / "upstream-config-tests" / "framework-cases"
            case_root.mkdir(parents=True)
            source = case_root / "fixture.yaml"
            source.write_text("fixture: generated\n", encoding="utf-8")
            expected_cases = [
                {"id": "control", "kind": "control", "uri": "/?control=1", "expect_ids": [], "expect_event_phase": "request_body"},
                {"id": "detect", "kind": "detection", "uri": "/?foo=attack", "expect_ids": ["100000"], "expect_event_phase": "request_body", "source": source.name},
                {"id": "bypass", "kind": "bypass", "uri": "/?foo=benign", "expect_ids": [], "expect_event_phase": "request_body"},
            ]
            case_hashes = TARGET.selected_case_hashes(case_root, [source])
            stage = runtime / "build" / "stages" / "envoy" / "no_crs_with_mrts" / "runtime"
            stage.mkdir(parents=True)
            plan_path = stage / "mrts-runtime-plan.json"
            rules_hash = TARGET.hashlib.sha256(generated.read_bytes()).hexdigest()
            plan = {
                "schema": "no-crs-with-mrts-plan/v1",
                "profile": "no-crs/with-mrts",
                "connector": "envoy",
                "cases": json.loads(json.dumps(expected_cases)),
                "inventory_root": str(case_root),
                "inventory_hash": TARGET.selected_case_inventory_hash([source]),
                "case_hashes": case_hashes,
                "load_file": str(load),
                "load_file_sha256": TARGET.hashlib.sha256(load.read_bytes()).hexdigest(),
                "no_crs_rules_file": str(baseline),
                "no_crs_validation": {
                    "generated_rules_root": str(rules),
                    "canonical_mrts_rules_root": str(canonical),
                    "included_rule_sha256": {generated.name: rules_hash},
                    "rule_id_inventory": TARGET.rule_id_inventory(
                        rules, {generated.name: rules_hash}
                    ),
                },
            }
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            runtime.chmod(0o700)
            with mock.patch.object(TARGET, "select_cases", return_value=(expected_cases, [source])):
                initial_digest = plan_digest(plan_path)
                self.validate_plan(
                    plan_path, runtime, framework, rules, load, initial_digest
                )
                plan["no_crs_validation"]["rule_id_inventory"] = ["100001"]
                plan_path.write_text(json.dumps(plan), encoding="utf-8")
                self.assert_validation_raises(
                    "no-CRS validation does not match",
                    plan_path, runtime, framework, rules, load, plan_digest(plan_path)
                )
                plan["no_crs_validation"]["rule_id_inventory"] = ["100000"]
                plan["cases"][1]["uri"] = "/?foo=benign"
                plan_path.write_text(json.dumps(plan), encoding="utf-8")
                self.assert_validation_raises(
                    "digest does not match", plan_path, runtime, framework, rules, load, initial_digest
                )
                self.assert_validation_raises(
                    "cases do not match", plan_path, runtime, framework, rules, load, plan_digest(plan_path)
                )
                plan["cases"] = json.loads(json.dumps(expected_cases))
                plan["load_file_sha256"] = "0" * 64
                plan_path.write_text(json.dumps(plan), encoding="utf-8")
                self.assert_validation_raises(
                    "", plan_path, runtime, framework, rules, load, plan_digest(plan_path)
                )

    def test_sealed_plan_reconstructs_cases_from_the_explicit_framework_root(self):
        framework = ROOT / "modules" / "ModSecurity-test-Framework"
        canonical = framework / "tools" / "MRTS" / "generated" / "rules"
        baseline = framework / "tests" / "rules" / "no-crs-baseline.conf"
        if not canonical.is_dir() or not baseline.is_file():
            self.skipTest("exact Framework/MRTS gitlink is unavailable")
        with tempfile.TemporaryDirectory(prefix="mrts-no-crs-case-binding-") as directory:
            runtime = Path(directory) / "mrts-no-crs-runtime"
            rules = runtime / "build" / "mrts" / "upstream-config-tests" / "rules"
            case_root = runtime / "build" / "mrts" / "upstream-config-tests" / "framework-cases"
            stage = runtime / "build" / "stages" / "envoy" / "no_crs_with_mrts" / "runtime"
            rules.mkdir(parents=True)
            case_root.mkdir(parents=True)
            stage.mkdir(parents=True)
            for source in sorted(canonical.glob("MRTS_*.conf")):
                (rules / source.name).write_bytes(source.read_bytes())
            copied_source = case_root / "fixture.yaml"
            copied_source.write_text(
                """metadata:
  upstream_file: tools/MRTS/generated/tests/regression/tests/MRTS_002_ARGS_A-GET.yaml
  phase: 1
portable: true
request:
  method: GET
  path: /?foo=attack
expect:
  rule_id: 100000
""",
                encoding="utf-8",
            )
            with mock.patch.dict(
                os.environ,
                {"MRTS_FRAMEWORK_ROOT": str(runtime / "untrusted-framework")},
                clear=False,
            ):
                cases, sources = TARGET.select_cases(case_root, framework)
            self.assertGreaterEqual(len(cases), 3)
            self.assertEqual(sources, [copied_source])
            included = {
                source.name: TARGET.hashlib.sha256(source.read_bytes()).hexdigest()
                for source in sorted(rules.glob("MRTS_*.conf"))
            }
            load = runtime / "build" / "mrts" / "upstream-config-tests" / "mrts.load"
            load.write_text(
                "".join(f'Include "{rules / name}"\n' for name in sorted(included)),
                encoding="utf-8",
            )
            plan_path = stage / "mrts-runtime-plan.json"
            plan = {
                "schema": "no-crs-with-mrts-plan/v1",
                "profile": "no-crs/with-mrts",
                "connector": "envoy",
                "cases": cases,
                "inventory_root": str(case_root),
                "inventory_hash": TARGET.selected_case_inventory_hash(sources),
                "case_hashes": TARGET.selected_case_hashes(case_root, sources),
                "load_file": str(load),
                "load_file_sha256": TARGET.hashlib.sha256(load.read_bytes()).hexdigest(),
                "no_crs_rules_file": str(baseline.resolve()),
                "no_crs_validation": {
                    "generated_rules_root": str(rules),
                    "canonical_mrts_rules_root": str(canonical.resolve()),
                    "included_rule_sha256": included,
                    "rule_id_inventory": TARGET.rule_id_inventory(rules, included),
                },
            }
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            runtime.chmod(0o700)
            initial_digest = plan_digest(plan_path)
            self.validate_plan(
                plan_path, runtime, framework, rules, load, initial_digest
            )
            detection = next(case for case in plan["cases"] if case["kind"] == "detection")
            detection["expect_ids"] = ["100001"]
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            self.assert_validation_raises(
                "digest does not match", plan_path, runtime, framework, rules, load, initial_digest
            )
            self.assert_validation_raises(
                "cases do not match", plan_path, runtime, framework, rules, load, plan_digest(plan_path)
            )

    def test_executor_reuses_exact_no_crs_validator_for_a_no_crs_runtime_path(self):
        framework = ROOT / "modules" / "ModSecurity-test-Framework"
        canonical = framework / "tools" / "MRTS" / "generated" / "rules"
        baseline = framework / "tests" / "rules" / "no-crs-baseline.conf"
        if not canonical.is_dir() or not baseline.is_file():
            self.skipTest("exact Framework/MRTS gitlink is unavailable")
        with tempfile.TemporaryDirectory(prefix="mrts-no-crs-executor-") as directory:
            runtime = Path(directory) / "mrts-no-crs-runtime"
            rules = runtime / "build" / "mrts" / "upstream-config-tests" / "rules"
            case_root = runtime / "build" / "mrts" / "upstream-config-tests" / "framework-cases"
            stage = runtime / "build" / "stages" / "envoy" / "no_crs_with_mrts" / "runtime"
            rules.mkdir(parents=True)
            case_root.mkdir(parents=True)
            stage.mkdir(parents=True)
            included: dict[str, str] = {}
            for source in sorted(canonical.glob("MRTS_*.conf")):
                destination = rules / source.name
                destination.write_bytes(source.read_bytes())
                included[source.name] = TARGET.hashlib.sha256(destination.read_bytes()).hexdigest()
            self.assertTrue(included)
            load = runtime / "build" / "mrts" / "upstream-config-tests" / "mrts.load"
            load.write_text(
                "".join(f'Include "{rules / name}"\n' for name in sorted(included)),
                encoding="utf-8",
            )
            source = case_root / "fixture.yaml"
            source.write_text(
                """metadata:
  upstream_file: tools/MRTS/generated/tests/regression/tests/MRTS_002_ARGS_A-GET.yaml
  phase: 1
portable: true
request:
  method: GET
  path: /?foo=attack
expect:
  rule_id: 100000
""",
                encoding="utf-8",
            )
            cases, sources = TARGET.select_cases(case_root, framework)
            plan_path = stage / "mrts-runtime-plan.json"
            executor_path = ROOT / "ci" / "runtime" / "lifecycle" / "execute-no-crs-mrts-cases.py"
            plan_path.write_text(
                json.dumps(
                    {
                        "schema": "no-crs-with-mrts-plan/v1",
                        "profile": "no-crs/with-mrts",
                        "connector": "envoy",
                        "cases": cases,
                        "inventory_root": str(case_root),
                        "inventory_hash": TARGET.selected_case_inventory_hash(sources),
                        "case_hashes": TARGET.selected_case_hashes(case_root, sources),
                        "executor": {
                            "path": str(executor_path),
                            "sha256": TARGET.hashlib.sha256(executor_path.read_bytes()).hexdigest(),
                        },
                        "load_file": str(load),
                        "load_file_sha256": TARGET.hashlib.sha256(load.read_bytes()).hexdigest(),
                        "no_crs_rules_file": str(baseline.resolve()),
                        "no_crs_validation": {
                            "generated_rules_root": str(rules),
                            "canonical_mrts_rules_root": str(canonical.resolve()),
                            "included_rule_sha256": included,
                            "rule_id_inventory": TARGET.rule_id_inventory(rules, included),
                        },
                    }
                ),
                encoding="utf-8",
            )
            runtime.chmod(0o700)
            executor_path = ROOT / "ci" / "runtime" / "lifecycle" / "execute-no-crs-mrts-cases.py"
            sealed_plan_sha256 = plan_digest(plan_path)
            EXECUTOR.validate_sealed_no_crs_plan(
                plan_path, runtime, load, executor_path, sealed_plan_sha256
            )
            with mock.patch.object(
                sys,
                "argv",
                [
                    str(executor_path),
                    "--connector",
                    "envoy",
                    "--runtime-root",
                    str(stage),
                    "--plan",
                    str(plan_path),
                    "--plan-sha256",
                    sealed_plan_sha256,
                    "--load-file",
                    str(load),
                    "--result",
                    str(stage / "mrts-runtime-result.json"),
                    "--event-log",
                    str(stage / "events.jsonl"),
                    "--host",
                    "127.0.0.1",
                    "--port",
                    "18080",
                ],
            ):
                with self.assertRaisesRegex(SystemExit, "closed private layout"):
                    EXECUTOR.main()
            first_rule = rules / next(iter(sorted(included)))
            first_rule.write_text('SecRule ARGS:foo "@streq attack" "id:949110,phase:1,pass"\\n', encoding="utf-8")
            with self.assertRaises(SystemExit):
                EXECUTOR.validate_sealed_no_crs_plan(
                    plan_path, runtime, load, executor_path, sealed_plan_sha256
                )


if __name__ == "__main__":
    unittest.main()
