from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import shlex
import stat
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
HANDOFF_PATH = ROOT / "ci" / "runtime" / "lifecycle" / "run-nginx-root-handoff.py"
SPEC = importlib.util.spec_from_file_location("nginx_root_handoff", HANDOFF_PATH)
if SPEC is None or SPEC.loader is None:
    raise ImportError("unable to load nginx root handoff module")
HANDOFF = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = HANDOFF
SPEC.loader.exec_module(HANDOFF)


class NginxRootHandoffContractTest(unittest.TestCase):
    def make_layout(self) -> tuple[tempfile.TemporaryDirectory[str], HANDOFF.HandoffRequest]:
        temporary = tempfile.TemporaryDirectory(prefix="nginx-root-handoff-")
        root = Path(temporary.name)
        connector_root = root / "checkout"
        framework_root = connector_root / "modules" / "ModSecurity-test-Framework"
        runner = framework_root / "ci" / "runtime" / "run-nginx-smoke.sh"
        runner.parent.mkdir(parents=True)
        runner.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")

        verified_root = root / "verified"
        build_root = verified_root / "build"
        cache_root = verified_root / "cache-v2"
        component_cache = cache_root / "shared"
        report_root = build_root / "runtime-component-reports"
        for directory in (
            build_root / "tmp",
            build_root / "logs",
            build_root / "results",
            build_root / "nginx-harness",
            component_cache,
            report_root,
        ):
            directory.mkdir(parents=True, exist_ok=True)

        nginx_build = component_cache / "builds" / "connectors" / "nginx" / "build-id"
        nginx_prefix = component_cache / "prefix" / "nginx" / "build-id"
        modsecurity_root = component_cache / "sources" / "modsecurity-v3"
        modsecurity_lib = component_cache / "prefix" / "modsecurity" / "build-id" / "lib"
        (nginx_build / "connector-src").mkdir(parents=True)
        (nginx_prefix / "sbin").mkdir(parents=True)
        (nginx_prefix / "modules").mkdir(parents=True)
        modsecurity_root.mkdir(parents=True)
        modsecurity_lib.mkdir(parents=True)
        (modsecurity_lib.parent / "include").mkdir()
        (nginx_build / "connector-src" / "materialized-source.json").write_text("{}\n", encoding="utf-8")
        (nginx_build / "nginx-protocol-build-provenance.txt").write_text("h1\n", encoding="utf-8")
        binary = nginx_prefix / "sbin" / "nginx"
        binary.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        binary.chmod(0o755)
        (nginx_prefix / "modules" / "ngx_http_modsecurity_module.so").write_bytes(b"module")
        (modsecurity_lib / "libmodsecurity.so").write_bytes(b"library")

        snapshot = report_root / "runtime-env.sh"
        values = {
            "CONNECTOR_COMPONENT_CACHE": str(component_cache),
            "MODSECURITY_SOURCE_DIR": str(modsecurity_root),
            "MODSECURITY_V3_SOURCE_DIR": str(modsecurity_root),
            "MODSECURITY_V3_ROOT": str(modsecurity_root),
            "NGINX_BUILD_DIR": str(nginx_build),
            "NGINX_BUILD_OWNER_ROOT": str(component_cache / "builds" / "connectors"),
            "NGINX_PREFIX": str(nginx_prefix),
            "NGINX_CONNECTOR_BUILD_ID": "build-id",
            "NGINX_PROTOCOL_PROFILE": "h1",
            "MODSECURITY_PREFIX": str(modsecurity_lib.parent),
            "MODSECURITY_SHARED_PREFIX": str(modsecurity_lib.parent),
            "MODSECURITY_INCLUDE_DIR": str(modsecurity_lib.parent / "include"),
            "MODSECURITY_LIB_DIR": str(modsecurity_lib),
            "RUNTIME_COMPONENT_ENV_SNAPSHOT": str(snapshot),
            "RUNTIME_COMPONENT_ENV_SNAPSHOT_CACHE": str(component_cache),
            "RUNTIME_COMPONENT_ENV_SNAPSHOT_SCHEMA": "1",
            "RUNTIME_COMPONENT_ENV_SNAPSHOT_TARGET": "nginx",
        }
        snapshot.write_text(
            "".join(f"export {key}={shlex.quote(value)}\n" for key, value in sorted(values.items())),
            encoding="utf-8",
        )
        request = HANDOFF.HandoffRequest(
            connector_root=connector_root,
            framework_root=framework_root,
            verified_run_root=verified_root,
            build_root=build_root,
            cache_root=cache_root,
            component_cache=component_cache,
            tmp_root=build_root / "tmp",
            log_root=build_root / "logs",
            results_dir=build_root / "results",
            report_output_root=report_root,
            snapshot=snapshot,
            python=Path(sys.executable),
            stage="config_load",
            run_one_case="1",
            test_case="allow_without_marker",
            smoke_cases="",
            selected_case_ids="",
            rule_preamble=None,
            phase4_mode="safe",
            docroot_projection=False,
            nginx_harness_parent=build_root / "nginx-harness",
            nginx_harness_work_root=None,
            runtime_root=None,
            runtime_base=None,
            evidence_root=None,
            connector_run_root=None,
            connector_log_root=None,
        )
        return temporary, request

    def rewrite_snapshot(self, request: HANDOFF.HandoffRequest, values: dict[str, str]) -> None:
        request.snapshot.write_text(
            "".join(f"export {key}={shlex.quote(value)}\n" for key, value in sorted(values.items())),
            encoding="utf-8",
        )

    def snapshot_values(self, request: HANDOFF.HandoffRequest) -> dict[str, str]:
        return HANDOFF.parse_runtime_snapshot(request.snapshot)

    def test_valid_request_reduces_snapshot_to_fixed_environment(self) -> None:
        temporary, request = self.make_layout()
        with temporary:
            validated, snapshot = HANDOFF.validate_request(request)
            environment = HANDOFF.build_environment(
                validated,
                snapshot,
                worker_user="nobody",
                worker_group="nogroup",
                projection_parent=None,
            )
        self.assertEqual(environment["MSCONNECTOR_SMOKE_STAGE"], "config_load")
        self.assertEqual(environment["NGINX_WORKER_USER"], "nobody")
        self.assertNotIn("LD_PRELOAD", environment)
        self.assertNotIn("LD_LIBRARY_PATH", environment)
        self.assertNotIn("MRTS_NATIVE_NGINX_BIN", environment)
        self.assertEqual(environment["PATH"], "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin")
        self.assertEqual(environment["NGINX_ROOT_HANDOFF"], "1")
        self.assertEqual(environment[HANDOFF.ROOT_HANDOFF_CALLER_UID_ENV], "1")

    def test_rejects_caller_supplied_internal_binding(self) -> None:
        with self.assertRaisesRegex(HANDOFF.HandoffError, "caller-supplied internal"):
            HANDOFF.validate_nginx_environment(
                {
                    "NGINX_ROOT_HANDOFF": "1",
                    HANDOFF.ROOT_HANDOFF_CALLER_UID_ENV: "1000",
                }
            )

    def test_elevated_binding_requires_canonical_matching_sudo_uid(self) -> None:
        cases = (
            ("1000", "1000", True),
            ("01", "01", False),
            ("0", "0", False),
            ("1000", "", False),
            ("1000", "1001", False),
        )
        for bound, sudo_uid, accepted in cases:
            with self.subTest(bound=bound, sudo_uid=sudo_uid), mock.patch.object(HANDOFF.os, "geteuid", return_value=0), mock.patch.dict(os.environ, {"SUDO_UID": sudo_uid}, clear=False):
                args = type("Args", (), {"bound_caller_uid": bound})()
                if accepted:
                    self.assertEqual(HANDOFF.validated_bound_caller_uid(args), 1000)
                else:
                    with self.assertRaises(HANDOFF.HandoffError):
                        HANDOFF.validated_bound_caller_uid(args)

    def test_elevated_binding_rejects_nonroot_execution(self) -> None:
        args = type("Args", (), {"bound_caller_uid": "1000"})()
        with mock.patch.object(HANDOFF.os, "geteuid", return_value=1000), self.assertRaisesRegex(HANDOFF.HandoffError, "effective uid 0"):
            HANDOFF.validated_bound_caller_uid(args)

    def test_regular_invocation_rejects_hidden_bound_caller_uid(self) -> None:
        args = type("Args", (), {"bound_caller_uid": "1000"})()
        with self.assertRaisesRegex(HANDOFF.HandoffError, "caller-supplied elevated"):
            HANDOFF.reject_unprivileged_internal_binding(args)

    def test_smoke_lock_handback_is_descriptor_safe(self) -> None:
        temporary, request = self.make_layout()
        with temporary:
            lock = request.build_root / HANDOFF.BUILD_LOCK_FILENAME
            lock.write_text("lock", encoding="utf-8")
            lock.chmod(0o600)
            original_fstat = HANDOFF.os.fstat
            changed = False

            def returned_owner(descriptor: int) -> os.stat_result:
                details = original_fstat(descriptor)
                if changed:
                    replacement = list(details)
                    replacement[4] = 1
                    return os.stat_result(replacement)
                return details

            def record_handoff(*_args: object) -> None:
                nonlocal changed
                changed = True

            with mock.patch.object(HANDOFF.os, "fchown", side_effect=record_handoff) as fchown, mock.patch.object(
                HANDOFF.os, "fstat", side_effect=returned_owner
            ):
                HANDOFF.return_smoke_lock_to_caller(request, 1)
                fchown.assert_called_once()

    def test_smoke_lock_handback_rejects_symlink(self) -> None:
        temporary, request = self.make_layout()
        with temporary:
            target = request.build_root / "target"
            target.write_text("lock", encoding="utf-8")
            (request.build_root / HANDOFF.BUILD_LOCK_FILENAME).symlink_to(target.name)
            with self.assertRaises((HANDOFF.HandoffError, OSError)):
                HANDOFF.return_smoke_lock_to_caller(request, 1)

    def test_accepts_direct_relative_libmodsecurity_soname_link(self) -> None:
        temporary, request = self.make_layout()
        with temporary:
            lib_dir = request.component_cache / "prefix" / "modsecurity" / "build-id" / "lib"
            library = lib_dir / "libmodsecurity.so"
            target = lib_dir / "libmodsecurity.so.3.0.14"
            library.unlink()
            target.write_bytes(b"library")
            library.symlink_to(target.name)
            HANDOFF.validate_request(request)

    def test_accepts_bounded_relative_libmodsecurity_soname_link_chain(self) -> None:
        temporary, request = self.make_layout()
        with temporary:
            lib_dir = request.component_cache / "prefix" / "modsecurity" / "build-id" / "lib"
            library = lib_dir / "libmodsecurity.so"
            soname = lib_dir / "libmodsecurity.so.3"
            target = lib_dir / "libmodsecurity.so.3.0.14"
            library.unlink()
            target.write_bytes(b"library")
            soname.symlink_to(target.name)
            library.symlink_to(soname.name)
            HANDOFF.validate_request(request)

    def test_rejects_libmodsecurity_soname_link_outside_its_library_directory(self) -> None:
        temporary, request = self.make_layout()
        with temporary:
            lib_dir = request.component_cache / "prefix" / "modsecurity" / "build-id" / "lib"
            library = lib_dir / "libmodsecurity.so"
            outside = request.component_cache / "outside-library"
            library.unlink()
            outside.write_bytes(b"library")
            library.symlink_to(outside)
            with self.assertRaisesRegex(HANDOFF.HandoffError, "invalid SONAME link target"):
                HANDOFF.validate_request(request)

    def test_rejects_libmodsecurity_soname_link_with_traversal(self) -> None:
        temporary, request = self.make_layout()
        with temporary:
            lib_dir = request.component_cache / "prefix" / "modsecurity" / "build-id" / "lib"
            library = lib_dir / "libmodsecurity.so"
            library.unlink()
            library.symlink_to("../libmodsecurity.so.3")
            with self.assertRaisesRegex(HANDOFF.HandoffError, "invalid SONAME link target"):
                HANDOFF.validate_request(request)

    def test_rejects_nonconventional_libmodsecurity_soname_link(self) -> None:
        temporary, request = self.make_layout()
        with temporary:
            lib_dir = request.component_cache / "prefix" / "modsecurity" / "build-id" / "lib"
            library = lib_dir / "libmodsecurity.so"
            target = lib_dir / "libmodsecurity.so.untrusted"
            library.unlink()
            target.write_bytes(b"library")
            library.symlink_to(target.name)
            with self.assertRaisesRegex(HANDOFF.HandoffError, "invalid SONAME link target"):
                HANDOFF.validate_request(request)

    def test_rejects_libmodsecurity_soname_chain_longer_than_libtool_shape(self) -> None:
        temporary, request = self.make_layout()
        with temporary:
            lib_dir = request.component_cache / "prefix" / "modsecurity" / "build-id" / "lib"
            library = lib_dir / "libmodsecurity.so"
            abi = lib_dir / "libmodsecurity.so.3"
            revision = lib_dir / "libmodsecurity.so.3.0"
            target = lib_dir / "libmodsecurity.so.3.0.14"
            library.unlink()
            target.write_bytes(b"library")
            revision.symlink_to(target.name)
            abi.symlink_to(revision.name)
            library.symlink_to(abi.name)
            with self.assertRaisesRegex(HANDOFF.HandoffError, "too many SONAME link hops"):
                HANDOFF.validate_request(request)

    def test_rejects_cyclic_libmodsecurity_soname_link(self) -> None:
        temporary, request = self.make_layout()
        with temporary:
            lib_dir = request.component_cache / "prefix" / "modsecurity" / "build-id" / "lib"
            library = lib_dir / "libmodsecurity.so"
            abi = lib_dir / "libmodsecurity.so.3"
            library.unlink()
            abi.symlink_to(abi.name)
            library.symlink_to(abi.name)
            with self.assertRaisesRegex(HANDOFF.HandoffError, "cyclic SONAME link"):
                HANDOFF.validate_request(request)

    def test_rejects_dangling_libmodsecurity_soname_link(self) -> None:
        temporary, request = self.make_layout()
        with temporary:
            lib_dir = request.component_cache / "prefix" / "modsecurity" / "build-id" / "lib"
            library = lib_dir / "libmodsecurity.so"
            library.unlink()
            library.symlink_to("libmodsecurity.so.3")
            with self.assertRaisesRegex(HANDOFF.HandoffError, "prepared libmodsecurity is missing"):
                HANDOFF.validate_request(request)

    def test_rejects_numeric_named_nonregular_libmodsecurity_soname_target(self) -> None:
        temporary, request = self.make_layout()
        with temporary:
            lib_dir = request.component_cache / "prefix" / "modsecurity" / "build-id" / "lib"
            library = lib_dir / "libmodsecurity.so"
            target = lib_dir / "libmodsecurity.so.3"
            library.unlink()
            target.mkdir()
            library.symlink_to(target.name)
            with self.assertRaisesRegex(HANDOFF.HandoffError, "regular file or a conventional SONAME link"):
                HANDOFF.validate_request(request)

    def test_rejects_nginx_binary_symlink_while_allowing_only_the_library_exception(self) -> None:
        temporary, request = self.make_layout()
        with temporary:
            binary = request.component_cache / "prefix" / "nginx" / "build-id" / "sbin" / "nginx"
            replacement = binary.parent / "nginx-replacement"
            binary.unlink()
            replacement.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            replacement.chmod(0o755)
            binary.symlink_to(replacement.name)
            with self.assertRaisesRegex(HANDOFF.HandoffError, "symbolic link"):
                HANDOFF.validate_request(request)

    def test_rejects_unknown_nginx_environment_key(self) -> None:
        with self.assertRaisesRegex(HANDOFF.HandoffError, "unapproved NGINX environment"):
            HANDOFF.validate_nginx_environment({"NGINX_ROOT_HANDOFF": "1", "NGINX_EVIL": "1"})

    def test_rejects_build_only_nginx_environment_keys(self) -> None:
        for key in (
            "NGINX_BIN",
            "NGINX_SOURCE_MODE",
            "NGINX_SOURCE_REPO_URL",
            "NGINX_GITHUB_REPO",
            "NGINX_RELEASE_TAG",
            "NGINX_SOURCE_GIT_REF",
            "NGINX_RELEASE_ASSET_NAME",
            "NGINX_SHA256",
        ):
            with self.subTest(key=key):
                with self.assertRaisesRegex(
                    HANDOFF.HandoffError, "unapproved NGINX environment"
                ):
                    HANDOFF.validate_nginx_environment(
                        {"NGINX_ROOT_HANDOFF": "1", key: "value"}
                    )

    def test_rejects_missing_root_handoff_opt_in(self) -> None:
        with self.assertRaisesRegex(HANDOFF.HandoffError, "NGINX_ROOT_HANDOFF=1"):
            HANDOFF.validate_nginx_environment({})

    def test_rejects_caller_projection_parent(self) -> None:
        with self.assertRaisesRegex(HANDOFF.HandoffError, "caller-supplied"):
            HANDOFF.validate_nginx_environment(
                {
                    "NGINX_ROOT_HANDOFF": "1",
                    "NGINX_DOCROOT_PROJECTION_PARENT": "/tmp/attacker",
                }
            )

    def test_rejects_non_allowlisted_snapshot_export(self) -> None:
        temporary, request = self.make_layout()
        with temporary:
            request.snapshot.write_text("export LD_PRELOAD='/tmp/evil.so'\n", encoding="utf-8")
            with self.assertRaisesRegex(HANDOFF.HandoffError, "unapproved key"):
                HANDOFF.parse_runtime_snapshot(request.snapshot)

    def test_rejects_snapshot_shell_payload_without_execution(self) -> None:
        temporary, request = self.make_layout()
        with temporary:
            request.snapshot.write_text("export NGINX_PREFIX='$(touch should-not-exist)'\n", encoding="utf-8")
            with self.assertRaisesRegex(HANDOFF.HandoffError, "unsafe value"):
                HANDOFF.parse_runtime_snapshot(request.snapshot)
            self.assertFalse((request.snapshot.parent / "should-not-exist").exists())

    def test_rejects_duplicate_snapshot_export(self) -> None:
        temporary, request = self.make_layout()
        with temporary:
            values = self.snapshot_values(request)
            request.snapshot.write_text(
                "".join(f"export {key}={shlex.quote(value)}\n" for key, value in sorted(values.items()))
                + f"export NGINX_PREFIX={shlex.quote(values['NGINX_PREFIX'])}\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(HANDOFF.HandoffError, "duplicate"):
                HANDOFF.parse_runtime_snapshot(request.snapshot)

    def test_rejects_snapshot_cache_mismatch(self) -> None:
        temporary, request = self.make_layout()
        with temporary:
            values = self.snapshot_values(request)
            values["RUNTIME_COMPONENT_ENV_SNAPSHOT_CACHE"] = str(request.cache_root / "wrong")
            self.rewrite_snapshot(request, values)
            with self.assertRaisesRegex(HANDOFF.HandoffError, "metadata cache mismatch"):
                HANDOFF.validate_request(request)

    def test_rejects_system_nginx_prefix(self) -> None:
        temporary, request = self.make_layout()
        with temporary:
            values = self.snapshot_values(request)
            values["NGINX_PREFIX"] = "/usr"
            self.rewrite_snapshot(request, values)
            with self.assertRaisesRegex(HANDOFF.HandoffError, "authorized root"):
                HANDOFF.validate_request(request)

    def test_rejects_snapshot_symlink(self) -> None:
        temporary, request = self.make_layout()
        with temporary:
            target = request.snapshot.parent / "snapshot-target.sh"
            target.write_text(request.snapshot.read_text(encoding="utf-8"), encoding="utf-8")
            request.snapshot.unlink()
            request.snapshot.symlink_to(target)
            with self.assertRaisesRegex(HANDOFF.HandoffError, "symbolic link"):
                HANDOFF.validate_request(request)

    def test_rejects_output_root_outside_verified_root(self) -> None:
        temporary, request = self.make_layout()
        with temporary:
            escaped = HANDOFF.HandoffRequest(**{**request.__dict__, "results_dir": request.connector_root / "results"})
            with self.assertRaisesRegex(HANDOFF.HandoffError, "RESULTS_DIR must be inside"):
                HANDOFF.validate_request(escaped)

    def test_rejects_cache_build_overlap(self) -> None:
        temporary, request = self.make_layout()
        with temporary:
            overlap = HANDOFF.HandoffRequest(**{**request.__dict__, "component_cache": request.build_root / "cache"})
            (request.build_root / "cache").mkdir()
            with self.assertRaisesRegex(HANDOFF.HandoffError, "must be inside|must not overlap"):
                HANDOFF.validate_request(overlap)

    def test_rejects_non_h1_profile(self) -> None:
        temporary, request = self.make_layout()
        with temporary:
            values = self.snapshot_values(request)
            values["NGINX_PROTOCOL_PROFILE"] = "h1-h2"
            self.rewrite_snapshot(request, values)
            with self.assertRaisesRegex(HANDOFF.HandoffError, "reviewed h1"):
                HANDOFF.validate_request(request)

    def test_rejects_arbitrary_stage_and_case_selection(self) -> None:
        temporary, request = self.make_layout()
        with temporary:
            arbitrary = HANDOFF.HandoffRequest(**{**request.__dict__, "stage": "build"})
            with self.assertRaisesRegex(HANDOFF.HandoffError, "unsupported stage"):
                HANDOFF.validate_request(arbitrary)
            invalid_case = HANDOFF.HandoffRequest(**{**request.__dict__, "test_case": "../../escape"})
            with self.assertRaisesRegex(HANDOFF.HandoffError, "fixed allow_without_marker"):
                HANDOFF.validate_request(invalid_case)

    def test_minimal_stage_requires_selected_allow_and_deny_cases(self) -> None:
        temporary, request = self.make_layout()
        with temporary:
            minimal = HANDOFF.HandoffRequest(
                **{
                    **request.__dict__,
                    "stage": "minimal_runtime_smoke",
                    "run_one_case": "0",
                    "test_case": "",
                    "smoke_cases": "allow_without_marker.yaml",
                }
            )
            with self.assertRaisesRegex(HANDOFF.HandoffError, "requires the selected allow and deny"):
                HANDOFF.validate_request(minimal)

    def test_rejects_nonroot_elevated_execution(self) -> None:
        temporary, request = self.make_layout()
        with temporary:
            validated, snapshot = HANDOFF.validate_request(request)
            with mock.patch.object(HANDOFF.os, "geteuid", return_value=1000):
                with self.assertRaisesRegex(HANDOFF.HandoffError, "effective uid 0"):
                    HANDOFF.execute_elevated(validated, snapshot)

    def test_privileged_launcher_rejects_a_runner_owned_interpreter(self) -> None:
        runner_owned = os.stat_result(
            (
                stat.S_IFREG | 0o755,
                1,
                1,
                1,
                1001,
                1001,
                0,
                0,
                0,
                0,
            )
        )
        with (
            mock.patch.object(HANDOFF.Path, "resolve", return_value=Path("/tmp/hosted-python")),
            mock.patch.object(HANDOFF.Path, "stat", return_value=runner_owned),
        ):
            with self.assertRaisesRegex(HANDOFF.HandoffError, "root-owned"):
                HANDOFF.validate_python_tool(Path("/tmp/hosted-python"))

    def test_projection_cleanup_refuses_unexpected_entries(self) -> None:
        temporary, request = self.make_layout()
        with temporary:
            parent = request.verified_run_root.parent / "projection"
            parent.mkdir()
            parent.chmod(HANDOFF.PROJECTION_PARENT_MODE)
            expected = parent.lstat()
            (parent / "unexpected").write_text("x", encoding="utf-8")
            with self.assertRaisesRegex(HANDOFF.HandoffError, "unexpected entries"):
                HANDOFF.remove_projection_parent(parent, expected)
            self.assertTrue((parent / "unexpected").exists())

    def test_projection_parent_permission_change_is_descriptor_bound(self) -> None:
        temporary, request = self.make_layout()
        with temporary:
            worker_gid = os.getegid()
            with (
                mock.patch.object(HANDOFF.os, "fchmod", wraps=HANDOFF.os.fchmod) as fchmod,
                mock.patch.object(HANDOFF.os, "fchown", wraps=HANDOFF.os.fchown) as fchown,
            ):
                parent, expected = HANDOFF.create_projection_parent(request.verified_run_root, worker_gid)
            self.assertEqual(stat.S_IMODE(expected.st_mode), HANDOFF.PROJECTION_PARENT_MODE)
            self.assertEqual(expected.st_gid, worker_gid)
            fchmod.assert_called_once()
            self.assertEqual(fchmod.call_args.args[1], HANDOFF.PROJECTION_PARENT_MODE)
            fchown.assert_called_once()
            self.assertEqual(fchown.call_args.args[1:], (-1, worker_gid))
            HANDOFF.remove_projection_parent(parent, expected)

    def test_projection_cleanup_removes_only_fixed_files(self) -> None:
        temporary, request = self.make_layout()
        with temporary:
            parent = request.verified_run_root.parent / "projection"
            docroot = parent / "docroot"
            docroot.mkdir(parents=True)
            parent.chmod(HANDOFF.PROJECTION_PARENT_MODE)
            for filename in HANDOFF.PROJECTION_FILENAMES:
                (docroot / filename).write_text(filename, encoding="utf-8")
            expected = parent.lstat()
            HANDOFF.remove_projection_parent(parent, expected)
            self.assertFalse(parent.exists())

    def test_projection_cleanup_rejects_changed_opened_descriptor(self) -> None:
        temporary, request = self.make_layout()
        with temporary:
            parent = request.verified_run_root.parent / "projection"
            parent.mkdir()
            parent.chmod(HANDOFF.PROJECTION_PARENT_MODE)
            expected = parent.lstat()
            changed = os.stat_result(
                (
                    expected.st_mode,
                    expected.st_ino + 1,
                    expected.st_dev,
                    expected.st_nlink,
                    expected.st_uid,
                    expected.st_gid,
                    expected.st_size,
                    expected.st_atime,
                    expected.st_mtime,
                    expected.st_ctime,
                )
            )
            with mock.patch.object(HANDOFF.os, "fstat", return_value=changed):
                with self.assertRaisesRegex(HANDOFF.HandoffError, "changed before cleanup"):
                    HANDOFF.remove_projection_parent(parent, expected)
            self.assertTrue(parent.is_dir())

    def test_fixed_framework_runner_must_be_direct_submodule_path(self) -> None:
        temporary, request = self.make_layout()
        with temporary:
            other_framework = request.verified_run_root / "framework"
            other_framework.mkdir(parents=True)
            altered = HANDOFF.HandoffRequest(**{**request.__dict__, "framework_root": other_framework})
            with self.assertRaisesRegex(HANDOFF.HandoffError, "fixed direct Parent submodule"):
                HANDOFF.validate_request(altered)

    def test_source_contains_no_root_shell_expansion_or_environment_preservation(self) -> None:
        source = HANDOFF_PATH.read_text(encoding="utf-8")
        self.assertIn('"/usr/bin/sudo", "-n", "--"', source)
        self.assertNotIn("sudo -E", source)
        self.assertNotIn("sudo sh -c", source)
        self.assertNotIn("shell=True", source)
        self.assertIn("parse_runtime_snapshot", source)
        self.assertIn("remove_projection_parent", source)

    def test_stage_uses_a_root_owned_launcher_only_for_the_privileged_reexec(self) -> None:
        stage = (ROOT / "ci" / "runtime" / "lifecycle" / "run-connector-stage.sh").read_text(
            encoding="utf-8"
        )
        self.assertIn("ROOT_HANDOFF_PYTHON=/usr/bin/python3", stage)
        self.assertIn(
            'exec "$PYTHON" "$CONNECTOR_ROOT/ci/runtime/lifecycle/run-nginx-root-handoff.py"',
            stage,
        )
        self.assertIn('--python "$ROOT_HANDOFF_PYTHON"', stage)
        self.assertNotIn('--python "$PYTHON"', stage)


if __name__ == "__main__":
    unittest.main()
