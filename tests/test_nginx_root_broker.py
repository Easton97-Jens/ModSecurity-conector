"""Focused contracts for the protected NGINX root broker.

These tests exercise the declarative boundary without starting NGINX or
requiring passwordless sudo.  A later protected-master workflow is responsible
for the real root/master/worker runtime proof.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
BROKER_PATH = ROOT / "ci" / "runtime" / "broker" / "nginx_root_broker.py"
SPEC = importlib.util.spec_from_file_location("nginx_root_broker", BROKER_PATH)
assert SPEC is not None
assert SPEC.loader is not None
BROKER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = BROKER
SPEC.loader.exec_module(BROKER)


BROKER_SHA = "a" * 40
PARENT_SHA = "b" * 40
FRAMEWORK_SHA = "c" * 40


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class TrustedNginxRootBrokerTest(unittest.TestCase):
    def private_dir(self, path: Path) -> Path:
        path.mkdir(parents=True, mode=0o700)
        path.chmod(0o700)
        return path

    def write(self, path: Path, text: str, mode: int = 0o600) -> Path:
        path.write_text(text, encoding="utf-8")
        path.chmod(mode)
        return path

    def caller_manifest(self, root: Path, **overrides: object) -> Path:
        payload: dict[str, object] = {
            "schema_version": BROKER.SCHEMA_VERSION,
            "run_id": "broker-run-1",
            "matrix_variant": "no-crs",
            "parent_head_sha": PARENT_SHA,
            "framework_sha": FRAMEWORK_SHA,
            "protected_broker_sha": BROKER_SHA,
        }
        payload.update(overrides)
        path = root / "caller-manifest.json"
        self.write(path, json.dumps(payload) + "\n")
        return path

    def prepare_arguments(self, root: Path, **overrides: object) -> argparse.Namespace:
        build = self.private_dir(root / "trusted-build")
        binary = self.write(build / "nginx", "trusted binary\n", 0o700)
        module = self.write(build / "ngx_http_modsecurity_module.so", "trusted module\n")
        library = self.write(build / "libmodsecurity.so", "trusted library\n")
        caller = self.caller_manifest(root)
        values: dict[str, object] = {
            "caller_manifest": str(caller),
            "staging_root": str(root / "broker-staging"),
            "trusted_build_root": str(build),
            "broker_sha": BROKER_SHA,
            "binary": str(binary),
            "binary_sha256": digest(binary),
            "module": str(module),
            "module_sha256": digest(module),
            "modsecurity_library": str(library),
            "library_sha256": digest(library),
            "nginx_version": "1.31.3",
            "worker_user": "www-data",
            "loopback": "127.0.0.1",
            "port": 18443,
        }
        values.update(overrides)
        return argparse.Namespace(**values)

    def test_valid_declarative_manifest_copies_only_verified_build_artifacts(self) -> None:
        with tempfile.TemporaryDirectory(prefix="nginx-root-broker-") as temporary:
            root = Path(temporary)
            arguments = self.prepare_arguments(root)

            candidate_path = BROKER.prepare_candidate(arguments)

            candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
            self.assertEqual(candidate["run_id"], "broker-run-1")
            self.assertEqual(candidate["protected_broker_sha"], BROKER_SHA)
            self.assertEqual(candidate["producer"]["source_commit"], BROKER_SHA)
            self.assertEqual(candidate["artifacts"]["binary"]["sha256"], arguments.binary_sha256)
            self.assertTrue(Path(candidate["artifacts"]["binary"]["path"]).is_file())
            self.assertFalse((Path(arguments.staging_root) / "runtime" / "nginx.conf").exists())

    def test_empty_or_unknown_caller_manifest_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="nginx-root-broker-") as temporary:
            root = Path(temporary)
            arguments = self.prepare_arguments(root)
            Path(arguments.caller_manifest).write_text("{}\n", encoding="utf-8")
            with self.assertRaisesRegex(BROKER.BrokerError, "missing fields"):
                BROKER.prepare_candidate(arguments)

            arguments = self.prepare_arguments(root / "unknown")
            caller = json.loads(Path(arguments.caller_manifest).read_text(encoding="utf-8"))
            caller["command"] = "/bin/sh"
            Path(arguments.caller_manifest).write_text(json.dumps(caller) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(BROKER.BrokerError, "unknown fields"):
                BROKER.prepare_candidate(arguments)

    def test_rejects_untrusted_artifact_paths_and_digest_mismatches(self) -> None:
        with tempfile.TemporaryDirectory(prefix="nginx-root-broker-") as temporary:
            root = Path(temporary)
            arguments = self.prepare_arguments(root)
            outside = self.write(root / "outside-nginx", "outside\n", 0o700)
            arguments.binary = str(outside)
            arguments.binary_sha256 = digest(outside)
            with self.assertRaisesRegex(BROKER.BrokerError, "inside the trusted build root"):
                BROKER.prepare_candidate(arguments)

            arguments = self.prepare_arguments(root / "mismatch")
            arguments.module_sha256 = "0" * 64
            with self.assertRaisesRegex(BROKER.BrokerError, "digest does not match"):
                BROKER.prepare_candidate(arguments)

    def test_rejects_mismatched_caller_head_and_framework_bindings(self) -> None:
        with tempfile.TemporaryDirectory(prefix="nginx-root-broker-") as temporary:
            root = Path(temporary)
            arguments = self.prepare_arguments(root, expected_parent_head="d" * 40)
            with self.assertRaisesRegex(BROKER.BrokerError, "parent_head_sha does not match"):
                BROKER.prepare_candidate(arguments)

            arguments = self.prepare_arguments(root / "framework", expected_framework_sha="d" * 40)
            with self.assertRaisesRegex(BROKER.BrokerError, "framework_sha does not match"):
                BROKER.prepare_candidate(arguments)

            arguments = self.prepare_arguments(root / "run-id", expected_run_id="other-run")
            with self.assertRaisesRegex(BROKER.BrokerError, "run_id does not match"):
                BROKER.prepare_candidate(arguments)

            arguments = self.prepare_arguments(root / "variant", expected_matrix_variant="with-crs")
            with self.assertRaisesRegex(BROKER.BrokerError, "matrix_variant does not match"):
                BROKER.prepare_candidate(arguments)

    def test_rejects_symlinked_artifacts_and_root_worker(self) -> None:
        with tempfile.TemporaryDirectory(prefix="nginx-root-broker-") as temporary:
            root = Path(temporary)
            arguments = self.prepare_arguments(root)
            binary = Path(arguments.binary)
            target = self.write(binary.parent / "real-nginx", "binary\n", 0o700)
            binary.unlink()
            binary.symlink_to(target)
            arguments.binary_sha256 = digest(target)
            with self.assertRaisesRegex(BROKER.BrokerError, "symlink"):
                BROKER.prepare_candidate(arguments)

            arguments = self.prepare_arguments(root / "root-worker", worker_user="root")
            with self.assertRaisesRegex(BROKER.BrokerError, "must not be root"):
                BROKER.prepare_candidate(arguments)

    def test_strict_final_manifest_rejects_broker_digest_and_projection_tampering(self) -> None:
        root = Path("/var/tmp") / BROKER.ROOT_PARENT_NAME / "broker-run-1"
        payload: dict[str, object] = {
            "schema_version": BROKER.SCHEMA_VERSION,
            "run_id": "broker-run-1",
            "matrix_variant": "no-crs",
            "parent_head_sha": PARENT_SHA,
            "framework_sha": FRAMEWORK_SHA,
            "protected_broker_sha": BROKER_SHA,
            "runner_uid": 1000,
            "runner_gid": 1000,
            "worker": {"name": "www-data", "uid": 33, "gid": 33},
            "network": {"address": "127.0.0.1", "port": 18443},
            "broker_root": str(root),
            "artifacts": {
                "binary": {"path": str(root / "artifacts/nginx"), "sha256": "1" * 64},
                "module": {"path": str(root / "artifacts/module.so"), "sha256": "2" * 64},
                "modsecurity_library": {"path": str(root / "artifacts/libmodsecurity.so"), "sha256": "3" * 64},
            },
            "nginx_version": "1.31.3",
            "runtime": {
                "root": str(root / "runtime"),
                "config": str(root / "runtime/nginx.conf"),
                "rules": str(root / "runtime/broker-rules.conf"),
                "docroot": str(root / "runtime/docroot"),
                "pid": str(root / "runtime/nginx.pid"),
                "access_log": str(root / "runtime/logs/nginx-access.log"),
                "error_log": str(root / "runtime/logs/nginx-error.log"),
                "state": str(root / "control/state.json"),
            },
            "projection": {
                "source_root": str(root / "evidence-source"),
                "target_root": str(root / "evidence-published"),
            },
            "expected_evidence": list(BROKER.EXPECTED_EVIDENCE),
            "producer": {"source_commit": BROKER_SHA, "workflow_commit": BROKER_SHA},
        }
        records = [dict(name=name, **record) for name, record in payload["artifacts"].items()]  # type: ignore[index,union-attr]
        payload["artifact_digest"] = BROKER.artifact_set_digest(records)

        with tempfile.TemporaryDirectory(prefix="nginx-root-broker-") as temporary:
            path = Path(temporary) / "manifest.json"
            self.write(path, json.dumps(payload) + "\n")
            self.assertEqual(BROKER.validated_final_manifest(path, BROKER_SHA)["run_id"], "broker-run-1")

            payload["protected_broker_sha"] = "d" * 40
            self.write(path, json.dumps(payload) + "\n")
            with self.assertRaisesRegex(BROKER.BrokerError, "mismatch"):
                BROKER.validated_final_manifest(path, BROKER_SHA)

            payload["protected_broker_sha"] = BROKER_SHA
            payload["projection"] = {"source_root": str(root / "evidence-source")}
            self.write(path, json.dumps(payload) + "\n")
            with self.assertRaisesRegex(BROKER.BrokerError, "projection paths"):
                BROKER.validated_final_manifest(path, BROKER_SHA)

            payload["projection"] = {
                "source_root": str(root / "evidence-source"),
                "target_root": str(root / "evidence-published"),
            }
            payload["artifacts"]["binary"]["path"] = str(root / "artifacts" / "other-nginx")  # type: ignore[index]
            self.write(path, json.dumps(payload) + "\n")
            validated = BROKER.validated_final_manifest(path, BROKER_SHA)
            with self.assertRaisesRegex(BROKER.BrokerError, "fixed broker artifact path"):
                BROKER.manifest_paths(validated)

    def test_action_parser_has_no_general_command_surface(self) -> None:
        source = BROKER_PATH.read_text(encoding="utf-8")
        self.assertNotIn("shell=True", source)
        self.assertNotIn("sudo -E", source)
        self.assertNotIn("sudo sh -c", source)
        self.assertNotIn("sudo bash -c", source)
        self.assertIn("choices=sorted(ALLOWED_ACTIONS)", source)
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            BROKER.parse_arguments(["action", "--action", "arbitrary-command", "--broker-sha", BROKER_SHA])

    def test_descriptor_cleanup_removes_special_entries_without_following_links(self) -> None:
        with tempfile.TemporaryDirectory(prefix="nginx-root-broker-") as temporary:
            root = Path(temporary)
            private = self.private_dir(root / "private")
            outside = self.write(root / "outside", "outside remains\n")
            self.write(private / "regular", "remove me\n")
            (private / "link").symlink_to(outside)
            os.mkfifo(private / "fifo")

            descriptor = os.open(private, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
            try:
                BROKER.remove_directory_contents_no_follow(
                    descriptor,
                    os.fstat(descriptor).st_dev,
                    "test private root",
                )
            finally:
                os.close(descriptor)
            private.rmdir()
            self.assertFalse(private.exists())
            self.assertEqual(outside.read_text(encoding="utf-8"), "outside remains\n")

    def test_projection_rejects_symlink_or_special_inputs_before_copy(self) -> None:
        with tempfile.TemporaryDirectory(prefix="nginx-root-broker-") as temporary:
            root = Path(temporary)
            target = self.write(root / "target", "evidence\n")
            linked = root / "linked-evidence"
            linked.symlink_to(target)
            with self.assertRaisesRegex(BROKER.BrokerError, "single-link regular"):
                BROKER.open_regular_no_follow(linked, "linked evidence")

            fifo = root / "evidence.fifo"
            os.mkfifo(fifo)
            with self.assertRaisesRegex(BROKER.BrokerError, "single-link regular"):
                BROKER.open_regular_no_follow(fifo, "FIFO evidence")


if __name__ == "__main__":
    unittest.main()
