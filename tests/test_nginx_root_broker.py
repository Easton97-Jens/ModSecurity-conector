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
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


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
            candidate_root = Path(arguments.trusted_build_root) / BROKER.CANDIDATE_DIRECTORY_NAME
            self.assertFalse((candidate_root / "runtime" / BROKER.BROKER_CONFIG_FILENAME).exists())

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
        root = BROKER.ROOT_PARENT / "broker-run-1"
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
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            BROKER.parse_arguments(
                [
                    "action",
                    "--action",
                    "validate-manifest",
                    "--broker-sha",
                    BROKER_SHA,
                    "--candidate",
                    "/tmp/candidate.json",
                    "--broker-parent",
                    "/tmp/attacker-selected-root",
                ]
            )

    def test_runtime_snapshot_is_discovered_only_below_the_trusted_build_root(self) -> None:
        with tempfile.TemporaryDirectory(prefix="nginx-root-broker-") as temporary:
            root = Path(temporary)
            trusted_build = self.private_dir(root / "trusted-build")
            reports = self.private_dir(trusted_build / BROKER.RUNTIME_REPORTS_RELATIVE)
            snapshot = self.write(reports / "runtime-env-snapshot.test.sh", "export NGINX_BINARY='/bin/false'\n")

            self.assertEqual(BROKER.runtime_snapshot_from_trusted_build(trusted_build), snapshot)

            self.write(reports / "runtime-env-snapshot.second.sh", "export NGINX_MODULE='/bin/false'\n")
            with self.assertRaisesRegex(BROKER.BrokerError, "exactly one runtime environment snapshot"):
                BROKER.runtime_snapshot_from_trusted_build(trusted_build)

    def test_prepare_from_snapshot_uses_only_the_fixed_trusted_build_layout(self) -> None:
        with tempfile.TemporaryDirectory(prefix="nginx-root-broker-") as temporary:
            root = Path(temporary)
            arguments = self.prepare_arguments(root)
            trusted_build = Path(arguments.trusted_build_root)
            prefix = self.private_dir(trusted_build / "modsecurity-prefix")
            library_root = self.private_dir(prefix / "lib")
            library = self.write(library_root / "libmodsecurity.so.3", "trusted library\n")
            reports = self.private_dir(trusted_build / BROKER.RUNTIME_REPORTS_RELATIVE)
            self.write(
                reports / "runtime-env-snapshot.test.sh",
                "\n".join(
                    (
                        f"export NGINX_BINARY='{arguments.binary}'",
                        f"export NGINX_MODULE='{arguments.module}'",
                        f"export MODSECURITY_SHARED_PREFIX='{prefix}'",
                        "",
                    )
                ),
            )

            candidate_path = BROKER.prepare_candidate_from_snapshot(arguments)

            candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
            self.assertEqual(candidate["artifacts"]["binary"]["sha256"], digest(Path(arguments.binary)))
            self.assertEqual(candidate["artifacts"]["module"]["sha256"], digest(Path(arguments.module)))
            self.assertEqual(candidate["artifacts"]["modsecurity_library"]["sha256"], digest(library))
            self.assertEqual(candidate_path.parent.parent, trusted_build / BROKER.CANDIDATE_DIRECTORY_NAME)

    def test_root_creation_rolls_back_when_chown_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="nginx-root-broker-") as temporary:
            state_base = self.private_dir(Path(temporary) / "var-lib")
            parent = state_base / BROKER.ROOT_PARENT_NAME
            run_root = parent / "broker-run-1"

            # The production path requires a root-owned state base.  Model that
            # ownership boundary while retaining a real unprivileged temporary
            # tree, so this regression test can exercise both removal paths on
            # an ordinary CI runner.
            original_directory_metadata = BROKER.directory_metadata

            def root_owned_directory_metadata(path: Path, label: str, *, owner: int | None = None) -> os.stat_result:
                metadata = original_directory_metadata(path, label)
                values = list(metadata)
                values[4] = 0
                return os.stat_result(values)

            def root_owned_stat(*args: object, **kwargs: object) -> os.stat_result:
                metadata = original_stat(*args, **kwargs)
                values = list(metadata)
                values[4] = 0
                return os.stat_result(values)

            runner_gid = os.getegid()
            with (
                mock.patch.object(BROKER, "ROOT_STATE_BASE", state_base),
                mock.patch.object(BROKER, "ROOT_PARENT", parent),
                mock.patch.object(BROKER, "directory_metadata", side_effect=root_owned_directory_metadata),
                mock.patch.object(BROKER.os, "chown", side_effect=OSError("fault-injected chown failure")),
            ):
                with self.assertRaisesRegex(OSError, "fault-injected"):
                    BROKER.secure_root_parent(runner_gid)
            self.assertFalse(parent.exists())

            BROKER.safe_mkdir(parent, BROKER.ROOT_PARENT_MODE, "test broker root parent")
            original_stat = os.stat
            with (
                mock.patch.object(BROKER, "ROOT_PARENT", parent),
                mock.patch.object(BROKER, "directory_metadata", side_effect=root_owned_directory_metadata),
                mock.patch.object(BROKER.os, "stat", side_effect=root_owned_stat),
                mock.patch.object(BROKER.os, "chown", side_effect=OSError("fault-injected chown failure")),
            ):
                with self.assertRaisesRegex(OSError, "fault-injected"):
                    BROKER.create_admitted_root(run_root, runner_gid)
            self.assertFalse(run_root.exists())

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

    def test_caller_yaml_contract_accepts_the_exact_two_immutable_broker_jobs(self) -> None:
        raw = (ROOT / ".github" / "workflows" / "run-protected-nginx-root-broker.yml").read_bytes()

        document = BROKER.parse_restricted_caller_workflow_yaml(raw)

        BROKER.validate_caller_workflow_document(
            document,
            broker_sha="e06254ea9622d214a9030b9ba786756560ace417",
            framework_sha="c71e15db7b7517b237add9fa09b3493e7bc93627",
        )

    def test_caller_yaml_contract_rejects_pin_job_variant_permission_and_secret_mutations(self) -> None:
        text = (ROOT / ".github" / "workflows" / "run-protected-nginx-root-broker.yml").read_text(
            encoding="utf-8"
        )
        broker_sha = "e06254ea9622d214a9030b9ba786756560ace417"
        framework_sha = "c71e15db7b7517b237add9fa09b3493e7bc93627"
        extra_broker_job = "\n".join(
            (
                "  run-extra-broker:",
                "    uses: Easton97-Jens/ModSecurity-conector/.github/workflows/nginx-root-broker.yml@"
                + broker_sha,
                "",
            )
        )
        mutations = {
            "mutable broker ref": (f"@{broker_sha}", "@master"),
            "mismatched broker input": (f"protected_broker_sha: {broker_sha}", "protected_broker_sha: " + "0" * 40),
            "missing protected job": ("  run-no-crs-broker:\n", "  run-no-crs-broker-missing:\n"),
            "extra protected job": ("  verify-evidence:\n", extra_broker_job + "  verify-evidence:\n"),
            "swapped variant": ("matrix_variant: no-crs", "matrix_variant: with-crs"),
            "write permission": (
                "      needs.prepare-manifests.result == 'success'\n"
                "    permissions:\n      contents: read\n"
                "    uses: Easton97-Jens/ModSecurity-conector/.github/workflows/nginx-root-broker.yml@",
                "      needs.prepare-manifests.result == 'success'\n"
                "    permissions:\n      contents: write\n"
                "    uses: Easton97-Jens/ModSecurity-conector/.github/workflows/nginx-root-broker.yml@",
            ),
            "secret inheritance": (
                f"    uses: Easton97-Jens/ModSecurity-conector/.github/workflows/nginx-root-broker.yml@{broker_sha}\n",
                "\n".join(
                    (
                        f"    uses: Easton97-Jens/ModSecurity-conector/.github/workflows/nginx-root-broker.yml@{broker_sha}",
                        "    secrets: inherit",
                        "",
                    )
                ),
            ),
            "duplicate uses": (
                f"    uses: Easton97-Jens/ModSecurity-conector/.github/workflows/nginx-root-broker.yml@{broker_sha}\n",
                "\n".join(
                    (
                        f"    uses: Easton97-Jens/ModSecurity-conector/.github/workflows/nginx-root-broker.yml@{broker_sha}",
                        f"    uses: Easton97-Jens/ModSecurity-conector/.github/workflows/nginx-root-broker.yml@{broker_sha}",
                        "",
                    )
                ),
            ),
        }
        for name, (original, replacement) in mutations.items():
            with self.subTest(name=name):
                self.assertIn(original, text)
                mutated = text.replace(original, replacement, 1)
                with self.assertRaises(BROKER.BrokerError):
                    document = BROKER.parse_restricted_caller_workflow_yaml(mutated.encode("utf-8"))
                    BROKER.validate_caller_workflow_document(
                        document,
                        broker_sha=broker_sha,
                        framework_sha=framework_sha,
                    )

    def test_caller_yaml_contract_rejects_top_level_and_unprivileged_job_mutations(self) -> None:
        raw = (ROOT / ".github" / "workflows" / "run-protected-nginx-root-broker.yml").read_bytes()
        broker_sha = "e06254ea9622d214a9030b9ba786756560ace417"
        framework_sha = "c71e15db7b7517b237add9fa09b3493e7bc93627"

        def add_extra_trigger(document: dict[str, object]) -> None:
            document["on"]["push"] = {}

        def add_extra_input(document: dict[str, object]) -> None:
            document["on"]["workflow_dispatch"]["inputs"]["matrix_variant"] = {
                "required": "true",
                "type": "string",
            }

        def add_top_level_write_permission(document: dict[str, object]) -> None:
            document["permissions"] = {"contents": "write"}

        def weaken_prepare_gate(document: dict[str, object]) -> None:
            document["jobs"]["prepare-manifests"]["if"] = "true"

        def lengthen_prepare_timeout(document: dict[str, object]) -> None:
            document["jobs"]["prepare-manifests"]["timeout-minutes"] = "999"

        def weaken_evidence_gate(document: dict[str, object]) -> None:
            document["jobs"]["verify-evidence"]["if"] = "${{ always() }}"

        def weaken_result_dependencies(document: dict[str, object]) -> None:
            document["jobs"]["result"]["needs"] = ["prepare-manifests"]

        mutations = {
            "extra trigger": add_extra_trigger,
            "extra dispatch input": add_extra_input,
            "top-level write permission": add_top_level_write_permission,
            "weakened preparation gate": weaken_prepare_gate,
            "unexpected preparation timeout": lengthen_prepare_timeout,
            "weakened evidence gate": weaken_evidence_gate,
            "weakened result dependencies": weaken_result_dependencies,
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                document = BROKER.parse_restricted_caller_workflow_yaml(raw)
                mutate(document)
                with self.assertRaises(BROKER.BrokerError):
                    BROKER.validate_caller_workflow_document(
                        document,
                        broker_sha=broker_sha,
                        framework_sha=framework_sha,
                    )

    def test_caller_yaml_contract_rejects_any_weakened_reusable_job_gate(self) -> None:
        raw = (ROOT / ".github" / "workflows" / "run-protected-nginx-root-broker.yml").read_bytes()
        broker_sha = "e06254ea9622d214a9030b9ba786756560ace417"
        framework_sha = "c71e15db7b7517b237add9fa09b3493e7bc93627"
        required_terms = (
            "github.event_name == 'workflow_dispatch'",
            "github.repository == 'Easton97-Jens/ModSecurity-conector'",
            "github.event.repository.fork == false",
            "github.ref == 'refs/heads/master'",
            "github.event.repository.default_branch == 'master'",
            "needs.prepare-manifests.result == 'success'",
        )
        for job_name in BROKER.EXPECTED_CALLER_BROKER_VARIANTS:
            for required_term in required_terms:
                with self.subTest(job_name=job_name, required_term=required_term):
                    document = BROKER.parse_restricted_caller_workflow_yaml(raw)
                    gate = document["jobs"][job_name]["if"]
                    self.assertIsInstance(gate, str)
                    self.assertIn(required_term, gate)
                    document["jobs"][job_name]["if"] = gate.replace(required_term, "true", 1)
                    with self.assertRaisesRegex(BROKER.BrokerError, "exact protected gate"):
                        BROKER.validate_caller_workflow_document(
                            document,
                            broker_sha=broker_sha,
                            framework_sha=framework_sha,
                        )

    def test_caller_yaml_contract_rejects_a_constant_true_reusable_job_gate(self) -> None:
        raw = (ROOT / ".github" / "workflows" / "run-protected-nginx-root-broker.yml").read_bytes()
        broker_sha = "e06254ea9622d214a9030b9ba786756560ace417"
        framework_sha = "c71e15db7b7517b237add9fa09b3493e7bc93627"
        document = BROKER.parse_restricted_caller_workflow_yaml(raw)
        document["jobs"]["run-no-crs-broker"]["if"] = "true"

        with self.assertRaisesRegex(BROKER.BrokerError, "exact protected gate"):
            BROKER.validate_caller_workflow_document(
                document,
                broker_sha=broker_sha,
                framework_sha=framework_sha,
            )

    def test_caller_yaml_contract_preserves_block_scalar_hash_data(self) -> None:
        raw = (ROOT / ".github" / "workflows" / "run-protected-nginx-root-broker.yml").read_bytes()
        broker_sha = "e06254ea9622d214a9030b9ba786756560ace417"
        framework_sha = "c71e15db7b7517b237add9fa09b3493e7bc93627"
        documented = BROKER.parse_restricted_caller_workflow_yaml(b"# ordinary YAML comment\n" + raw)
        BROKER.validate_caller_workflow_document(
            documented,
            broker_sha=broker_sha,
            framework_sha=framework_sha,
        )
        commented_steps = raw.replace(
            b"      - name: Check out protected master caller source\n",
            b"      - name: Check out protected master caller source\n"
            b"      # ordinary list-item comment\n",
            1,
        )
        document = BROKER.parse_restricted_caller_workflow_yaml(commented_steps)
        BROKER.validate_caller_workflow_document(
            document,
            broker_sha=broker_sha,
            framework_sha=framework_sha,
        )
        mutated = raw.replace(
            b"needs.prepare-manifests.result == 'success'",
            b"needs.prepare-manifests.result == 'success' # literal-block-data",
            1,
        )
        document = BROKER.parse_restricted_caller_workflow_yaml(mutated)
        with self.assertRaisesRegex(BROKER.BrokerError, "exact protected gate"):
            BROKER.validate_caller_workflow_document(
                document,
                broker_sha=broker_sha,
                framework_sha=framework_sha,
            )

    def test_restricted_caller_yaml_parser_rejects_indirection_duplicates_and_unsafe_encoding(self) -> None:
        invalid_documents = {
            "byte-order mark": b"\xef\xbb\xbfjobs:\n",
            "carriage return": b"jobs:\r\n",
            "tab": b"jobs:\n\trun: value\n",
            "document marker": b"---\njobs:\n",
            "anchor": b"jobs:\n  run: &anchor\n",
            "alias": b"jobs:\n  run: *anchor\n",
            "tag": b"jobs:\n  run: !unsafe value\n",
            "merge": b"jobs:\n  <<: *anchor\n",
            "flow mapping": b"jobs: {}\n",
            "duplicate key": b"jobs:\n  run: one\n  run: two\n",
        }
        for name, raw in invalid_documents.items():
            with self.subTest(name=name), self.assertRaises(BROKER.BrokerError):
                BROKER.parse_restricted_caller_workflow_yaml(raw)

    def test_caller_workflow_is_read_only_from_one_regular_git_blob(self) -> None:
        caller_sha = "d" * 40
        blob_sha = "e" * 40
        expected_entry = (
            f"100644 blob {blob_sha}\t{BROKER.EXPECTED_CALLER_WORKFLOW_PATH}\n".encode("ascii")
        )
        calls: list[tuple[str, ...]] = []

        def protected_git(_repository: Path, arguments: list[str], _label: str) -> bytes:
            calls.append(tuple(arguments))
            if arguments == ["cat-file", "-t", caller_sha]:
                return b"commit\n"
            if arguments[:2] == ["ls-tree", caller_sha]:
                return expected_entry
            if arguments == ["cat-file", "-s", blob_sha]:
                return b"9\n"
            if arguments == ["cat-file", "blob", blob_sha]:
                return b"jobs: {}\n"
            self.fail(f"unexpected Git arguments: {arguments}")

        with mock.patch.object(BROKER, "run_protected_git", side_effect=protected_git):
            raw = BROKER.read_caller_workflow_blob(Path("/protected/broker-src"), caller_sha)

        self.assertEqual(raw, b"jobs: {}\n")
        self.assertEqual(
            calls,
            [
                ("cat-file", "-t", caller_sha),
                ("ls-tree", caller_sha, "--", BROKER.EXPECTED_CALLER_WORKFLOW_PATH),
                ("cat-file", "-s", blob_sha),
                ("cat-file", "blob", blob_sha),
            ],
        )

    def test_caller_workflow_rejects_a_non_regular_git_tree_entry(self) -> None:
        caller_sha = "d" * 40
        entry = (
            f"120000 blob {'e' * 40}\t{BROKER.EXPECTED_CALLER_WORKFLOW_PATH}\n".encode("ascii")
        )

        def protected_git(_repository: Path, arguments: list[str], _label: str) -> bytes:
            if arguments == ["cat-file", "-t", caller_sha]:
                return b"commit\n"
            if arguments[:2] == ["ls-tree", caller_sha]:
                return entry
            self.fail(f"unexpected Git arguments: {arguments}")

        with mock.patch.object(BROKER, "run_protected_git", side_effect=protected_git):
            with self.assertRaisesRegex(BROKER.BrokerError, "regular Git blob"):
                BROKER.read_caller_workflow_blob(Path("/protected/broker-src"), caller_sha)

    def git_fixture(self, repository: Path, *arguments: str, input_data: bytes | None = None) -> bytes:
        completed = subprocess.run(
            ["git", "-C", os.fspath(repository), *arguments],
            check=True,
            input=input_data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return completed.stdout

    def commit_caller_workflow_fixture(
        self,
        repository: Path,
        content: bytes | None,
        *,
        mode: int = 0o644,
        symlink: bool = False,
    ) -> str:
        self.git_fixture(repository, "init", "--quiet", "--initial-branch=master")
        self.git_fixture(repository, "config", "user.email", "broker-test@example.invalid")
        self.git_fixture(repository, "config", "user.name", "Broker Test")
        workflow_path = repository / BROKER.EXPECTED_CALLER_WORKFLOW_PATH
        workflow_path.parent.mkdir(parents=True)
        if content is None:
            (repository / "README").write_text("fixture\n", encoding="utf-8")
        elif symlink:
            target = workflow_path.with_name("other.yml")
            target.write_bytes(content)
            workflow_path.symlink_to(target.name)
        else:
            workflow_path.write_bytes(content)
            workflow_path.chmod(mode)
        self.git_fixture(repository, "add", "--all")
        self.git_fixture(repository, "commit", "--quiet", "-m", "caller fixture")
        return self.git_fixture(repository, "rev-parse", "HEAD").decode("ascii").strip()

    def test_caller_workflow_uses_the_committed_blob_not_a_mutable_worktree_copy(self) -> None:
        raw = (ROOT / ".github" / "workflows" / "run-protected-nginx-root-broker.yml").read_bytes()
        broker_sha = "e06254ea9622d214a9030b9ba786756560ace417"
        framework_sha = "c71e15db7b7517b237add9fa09b3493e7bc93627"
        with tempfile.TemporaryDirectory(prefix="nginx-root-broker-git-") as temporary:
            repository = Path(temporary) / "broker-src"
            repository.mkdir()
            caller_sha = self.commit_caller_workflow_fixture(repository, raw)
            mutable_copy = repository / BROKER.EXPECTED_CALLER_WORKFLOW_PATH
            mutable_copy.write_text("jobs: {}\n", encoding="utf-8")

            with mock.patch.object(BROKER.Path, "cwd", return_value=repository):
                BROKER.validate_caller_workflow(
                    argparse.Namespace(
                        caller_sha=caller_sha,
                        broker_sha=broker_sha,
                        framework_sha=framework_sha,
                    )
                )

    def test_caller_workflow_real_git_object_rejections_are_fail_closed(self) -> None:
        valid = (ROOT / ".github" / "workflows" / "run-protected-nginx-root-broker.yml").read_bytes()
        mutable_pin = valid.replace(
            b"@e06254ea9622d214a9030b9ba786756560ace417",
            b"@master",
        )
        fixtures = {
            "absent path": (None, 0o644, False, "regular Git blob"),
            "executable workflow": (valid, 0o755, False, "regular Git blob"),
            "symlink workflow": (valid, 0o644, True, "regular Git blob"),
            "oversized workflow": (
                b"#" * (BROKER.MAX_CALLER_WORKFLOW_BYTES + 1),
                0o644,
                False,
                "exceeds the maximum",
            ),
        }
        for name, (content, mode, symlink, message) in fixtures.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory(
                prefix="nginx-root-broker-git-"
            ) as temporary:
                repository = Path(temporary) / "broker-src"
                repository.mkdir()
                caller_sha = self.commit_caller_workflow_fixture(
                    repository,
                    content,
                    mode=mode,
                    symlink=symlink,
                )
                with self.assertRaisesRegex(BROKER.BrokerError, message):
                    BROKER.read_caller_workflow_blob(repository, caller_sha)

        with tempfile.TemporaryDirectory(prefix="nginx-root-broker-git-") as temporary:
            repository = Path(temporary) / "broker-src"
            repository.mkdir()
            caller_sha = self.commit_caller_workflow_fixture(repository, mutable_pin)
            raw = BROKER.read_caller_workflow_blob(repository, caller_sha)
            document = BROKER.parse_restricted_caller_workflow_yaml(raw)
            with self.assertRaisesRegex(BROKER.BrokerError, "immutable protected broker SHA"):
                BROKER.validate_caller_workflow_document(
                    document,
                    broker_sha="e06254ea9622d214a9030b9ba786756560ace417",
                    framework_sha="c71e15db7b7517b237add9fa09b3493e7bc93627",
                )

        with tempfile.TemporaryDirectory(prefix="nginx-root-broker-git-") as temporary:
            repository = Path(temporary) / "broker-src"
            repository.mkdir()
            self.commit_caller_workflow_fixture(repository, valid)
            non_commit = self.git_fixture(
                repository,
                "hash-object",
                "-w",
                "--stdin",
                input_data=b"not a commit\n",
            ).decode("ascii").strip()
            with self.assertRaisesRegex(BROKER.BrokerError, "does not name a commit"):
                BROKER.read_caller_workflow_blob(repository, non_commit)


if __name__ == "__main__":
    unittest.main()
