"""Focused tests for the one canonical Parent runtime-observation contract."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
CONTRACTS_ROOT = ROOT / "ci" / "runtime" / "contracts"
CLI_PATH = ROOT / "ci" / "runtime" / "contracts" / "validate-runtime-observation.py"
FIXTURE_ROOT = ROOT / "tests" / "fixtures" / "runtime-observation"
sys.path.insert(0, str(CONTRACTS_ROOT))
import runtime_observation as contract  # noqa: E402
import runtime_observation_adapters as adapters  # noqa: E402

PARENT_COMMIT = "1" * 40
FRAMEWORK_COMMIT = "2" * 40
MRTS_COMMIT = "3" * 40


def fact(kind: str, value: object) -> dict[str, object]:
    return {"kind": kind, "value": value}


def assertion(
    case_id: str,
    kind: str,
    value: object,
    evidence_kind: str,
) -> dict[str, object]:
    return {
        "case_id": case_id,
        "expected": fact(kind, value),
        "observed": fact(kind, value),
        "required": True,
        "applicable": True,
        "executed": True,
        "live_executed": True,
        "result": "PASS",
        "reason": "structured live evidence matched",
        "evidence_kind": evidence_kind,
    }


def observation(
    connector: str = "envoy", profile: str = "with-crs-no-mrts"
) -> dict[str, object]:
    requirement = contract.PROFILE_REQUIREMENTS[profile]
    if connector in {"apache", "haproxy"}:
        producer = f"canonical-runtime-fixture-{connector}"
        evidence_kind = "canonical_fixture"
    elif connector == "nginx":
        producer = "protected-nginx-root-broker"
        evidence_kind = "protected_runtime_evidence"
    else:
        producer = f"parent-runtime-observation-adapter-{connector}"
        evidence_kind = "structured_connector_evidence"
    identity = {
        "connector": connector,
        "integration_mode": contract.CONNECTOR_INTEGRATION_MODES[connector],
        "profile": profile,
        "crs": requirement["crs"],
        "mrts": requirement["mrts"],
        "run_id": "contract-run",
        "parent_commit": PARENT_COMMIT,
        "framework_commit": FRAMEWORK_COMMIT,
        "mrts_commit": MRTS_COMMIT,
        "producer": producer,
        "producer_version": "1.0.0",
    }
    manifest_digest = hashlib.sha256(f"fixture:{connector}:{profile}".encode()).hexdigest()
    evidence = {
        "name": "fixture_evidence",
        "path": "fixture-evidence.json",
        "sha256": hashlib.sha256(b"fixture").hexdigest(),
        "kind": evidence_kind,
    }
    return {
        "schema_version": contract.SCHEMA_VERSION,
        "identity": identity,
        "runtime": {
            "config_test": assertion("config", "boolean", True, evidence_kind),
            "host_start": assertion("host-start", "boolean", True, evidence_kind),
            "reachability": assertion("reachability", "boolean", True, evidence_kind),
            "allow_case": assertion("allow", "http_status", 200, evidence_kind),
            "block_case": assertion("block", "action", "deny", evidence_kind),
            "bypass_case": assertion("bypass", "http_status", 403, evidence_kind),
            "runtime_status": "PASS",
        },
        "framework": {
            "framework_test_id": "runtime-contract-fixture",
            "scenario_category": requirement["scenario_category"],
            "selected": True,
            "executed": True,
            "live_executed": True,
            "expectation": fact("rule_id", 942270),
            "observation": fact("rule_id", 942270),
            "result": "PASS",
            "validation_status": contract.CONTRACT_VALIDATED,
            "failure_count": 0,
            "mismatch_count": 0,
        },
        "isolation": {
            field: bool(requirement["requires_mrts"])
            for field in contract.ISOLATION_FIELDS
        },
        "cleanup": {
            **{field: 0 for field in contract.CLEANUP_COUNTERS},
            "cleanup_status": "PASS",
        },
        "provenance": {
            "evidence_kind": evidence_kind,
            "fixture_id": "runtime-contract-fixture",
            "manifest_digest": manifest_digest,
            "evidence_digest": contract.evidence_manifest_digest([evidence]),
            "source_contract": "canonical-fixture-v1",
            "validation_basis": "evidence-digest-v1",
            "contract_schema_version": 1,
            "producer_version": "1.0.0",
            "evidence": [evidence],
        },
    }


def expected_identity(value: dict[str, object]) -> dict[str, object]:
    identity = value["identity"]
    assert isinstance(identity, dict)
    return dict(identity)


def canonical_fixture(connector: str) -> dict[str, object]:
    return json.loads(
        (FIXTURE_ROOT / f"{connector}-no-crs-no-mrts.json").read_text(encoding="utf-8")
    )


class RuntimeObservationContractTest(unittest.TestCase):
    def assert_valid(self, value: dict[str, object]) -> None:
        provenance = value["provenance"]
        assert isinstance(provenance, dict)
        policy = "fixture" if provenance["evidence_kind"] == "canonical_fixture" else "strict"
        if policy == "fixture":
            result = contract.validate_runtime_observation(value, expected_identity(value), policy)
        else:
            with tempfile.TemporaryDirectory(prefix="runtime-contract-") as temporary:
                root = Path(temporary) / "evidence"
                root.mkdir(mode=0o700)
                os.chmod(root, 0o700)
                evidence = provenance["evidence"]
                assert isinstance(evidence, list)
                for record in evidence:
                    assert isinstance(record, dict)
                    path = root / str(record["path"])
                    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
                    os.chmod(path.parent, 0o700)
                    path.write_bytes(b"fixture")
                    os.chmod(path, 0o600)
                result = contract.validate_runtime_observation(
                    value,
                    expected_identity(value),
                    {"name": policy, "evidence_root": root},
                )
        self.assertTrue(result.valid, result.errors)
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result["validation_status"], contract.CONTRACT_VALIDATED)

    def assert_invalid(
        self, value: dict[str, object], expected: dict[str, object] | None = None
    ) -> None:
        result = contract.validate_runtime_observation(
            value, expected if expected is not None else expected_identity(value), "strict"
        )
        self.assertFalse(result.valid)
        self.assertEqual(result.status, "VALIDATION_FAILED")
        self.assertTrue(result.errors)

    def test_valid_envoy_fixture(self) -> None:
        self.assert_valid(observation("envoy"))

    def test_valid_lighttpd_fixture(self) -> None:
        self.assert_valid(observation("lighttpd"))

    def test_valid_traefik_fixture(self) -> None:
        self.assert_valid(observation("traefik"))

    def test_canonical_apache_fixture_uses_common_validator(self) -> None:
        self.assert_valid(canonical_fixture("apache"))

    def test_canonical_haproxy_fixture_uses_common_validator(self) -> None:
        self.assert_valid(canonical_fixture("haproxy"))

    def test_apache_and_haproxy_have_no_lite_live_adapter(self) -> None:
        for connector in ("apache", "haproxy"):
            with self.subTest(connector=connector):
                self.assertFalse(contract.adapter_for(connector).live_producer_supported)
                with self.assertRaises(contract.RuntimeObservationError):
                    contract.require_live_adapter(connector)
        self.assertFalse(hasattr(contract, "validate_apache_lite"))
        self.assertFalse(hasattr(contract, "validate_haproxy_lite"))

    def test_apache_and_haproxy_live_claims_fail_closed_without_producers(self) -> None:
        for connector in ("apache", "haproxy"):
            with self.subTest(connector=connector):
                value = canonical_fixture(connector)
                identity = value["identity"]
                provenance = value["provenance"]
                assert isinstance(identity, dict)
                assert isinstance(provenance, dict)
                identity["producer"] = f"parent-runtime-observation-adapter-{connector}"
                provenance["evidence_kind"] = "structured_connector_evidence"
                evidence = provenance["evidence"]
                assert isinstance(evidence, list)
                evidence[0]["kind"] = "structured_connector_evidence"
                self._refresh_evidence_digest(value)
                self.assert_invalid(value)

    def test_fixture_policy_cannot_be_smuggled_into_strict_policy(self) -> None:
        value = canonical_fixture("apache")
        result = contract.validate_runtime_observation(
            value,
            expected_identity(value),
            {"name": "strict", "allow_fixture_evidence": True},
        )
        self.assertFalse(result.valid)
        self.assertEqual(result.status, "VALIDATION_FAILED")

    def test_missing_live_executed_prevents_framework_pass(self) -> None:
        value = observation()
        framework = value["framework"]
        assert isinstance(framework, dict)
        framework.pop("live_executed")
        self.assert_invalid(value)

    def test_wrong_http_status_prevents_pass(self) -> None:
        value = observation()
        runtime = value["runtime"]
        assert isinstance(runtime, dict)
        allow = runtime["allow_case"]
        assert isinstance(allow, dict)
        observed = allow["observed"]
        assert isinstance(observed, dict)
        observed["value"] = 403
        self.assert_invalid(value)

    def test_wrong_action_prevents_pass(self) -> None:
        value = observation()
        runtime = value["runtime"]
        assert isinstance(runtime, dict)
        block = runtime["block_case"]
        assert isinstance(block, dict)
        observed = block["observed"]
        assert isinstance(observed, dict)
        observed["value"] = "allow"
        self.assert_invalid(value)

    def test_wrong_rule_id_prevents_pass_when_expected(self) -> None:
        value = observation()
        framework = value["framework"]
        assert isinstance(framework, dict)
        observed = framework["observation"]
        assert isinstance(observed, dict)
        observed["value"] = 942271
        self.assert_invalid(value)

    def test_event_and_lifecycle_expectations_need_no_http_status(self) -> None:
        value = observation()
        runtime = value["runtime"]
        assert isinstance(runtime, dict)
        runtime["allow_case"] = assertion(
            "allow-event", "event", "allow-observed", "structured_connector_evidence"
        )
        runtime["block_case"] = assertion(
            "block-lifecycle", "lifecycle", "completed", "structured_connector_evidence"
        )
        self.assert_valid(value)

    def test_cleanup_expectation_needs_no_http_status(self) -> None:
        value = observation()
        framework = value["framework"]
        assert isinstance(framework, dict)
        framework["expectation"] = {
            "kind": "cleanup",
            "predicates": {"cleanup_complete": True},
        }
        framework["observation"] = {"predicates": {"cleanup_complete": True}}
        self.assert_valid(value)

    def test_wrong_connector_is_rejected(self) -> None:
        value = observation()
        expected = expected_identity(value)
        expected["connector"] = "traefik"
        self.assert_invalid(value, expected)

    def test_wrong_profile_is_rejected(self) -> None:
        value = observation()
        expected = expected_identity(value)
        expected["profile"] = "no-crs-no-mrts"
        self.assert_invalid(value, expected)

    def test_wrong_run_id_is_rejected(self) -> None:
        value = observation()
        expected = expected_identity(value)
        expected["run_id"] = "other-run"
        self.assert_invalid(value, expected)

    def test_wrong_parent_commit_is_rejected(self) -> None:
        value = observation()
        expected = expected_identity(value)
        expected["parent_commit"] = "4" * 40
        self.assert_invalid(value, expected)

    def test_wrong_framework_commit_is_rejected(self) -> None:
        value = observation()
        expected = expected_identity(value)
        expected["framework_commit"] = "5" * 40
        self.assert_invalid(value, expected)

    def test_wrong_mrts_commit_is_rejected(self) -> None:
        value = observation("envoy", "with-crs-with-mrts")
        expected = expected_identity(value)
        expected["mrts_commit"] = "6" * 40
        self.assert_invalid(value, expected)

    def test_missing_mandatory_evidence_is_rejected(self) -> None:
        value = observation()
        runtime = value["runtime"]
        assert isinstance(runtime, dict)
        runtime.pop("reachability")
        self.assert_invalid(value)

    def test_explicit_not_applicable_bypass_is_accepted(self) -> None:
        value = observation()
        runtime = value["runtime"]
        assert isinstance(runtime, dict)
        runtime["bypass_case"] = {
            "case_id": "bypass-not-applicable",
            "expected": fact("not_applicable", None),
            "observed": fact("not_applicable", None),
            "required": False,
            "applicable": False,
            "executed": False,
            "live_executed": False,
            "result": contract.NOT_APPLICABLE,
            "reason": "central profile matrix makes bypass optional",
            "evidence_kind": "structured_connector_evidence",
        }
        self.assert_valid(value)

    def test_cleanup_residue_prevents_aggregate_pass(self) -> None:
        value = observation()
        cleanup = value["cleanup"]
        assert isinstance(cleanup, dict)
        cleanup["listeners_remaining"] = 1
        self.assert_invalid(value)

    def test_no_mrts_attestation_is_checked(self) -> None:
        value = observation()
        isolation = value["isolation"]
        assert isinstance(isolation, dict)
        isolation["mrts_runner_invoked"] = True
        self.assert_invalid(value)

    def test_no_mrts_profile_still_requires_mrts_revision_identity(self) -> None:
        value = observation()
        identity = value["identity"]
        assert isinstance(identity, dict)
        identity["mrts_commit"] = contract.NOT_APPLICABLE
        self.assert_invalid(value)

    def test_mrts_attestation_is_profile_dependent(self) -> None:
        self.assert_valid(observation("envoy", "with-crs-with-mrts"))
        value = observation("envoy", "with-crs-with-mrts")
        isolation = value["isolation"]
        assert isinstance(isolation, dict)
        isolation["mrts_artifact_used"] = False
        self.assert_invalid(value)

    def test_nginx_is_representable_as_protected_separate(self) -> None:
        self.assertTrue(contract.adapter_for("nginx").protected_separate)
        self.assertFalse(contract.adapter_for("nginx").live_producer_supported)
        value = observation("nginx", "no-crs-no-mrts")
        identity = value["identity"]
        assert isinstance(identity, dict)
        self.assertEqual(identity["producer"], "protected-nginx-root-broker")
        self.assert_valid(value)

    def test_duplicate_case_id_is_rejected(self) -> None:
        value = observation()
        runtime = value["runtime"]
        assert isinstance(runtime, dict)
        block = runtime["block_case"]
        assert isinstance(block, dict)
        block["case_id"] = "allow"
        self.assert_invalid(value)

    def test_provenance_digest_mismatch_is_rejected(self) -> None:
        value = observation()
        provenance = value["provenance"]
        assert isinstance(provenance, dict)
        provenance["evidence_digest"] = "0" * 64
        self.assert_invalid(value)

    def test_missing_bound_evidence_returns_validation_failed_without_a_path_leak(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-contract-") as temporary:
            root = Path(temporary) / "evidence"
            root.mkdir(mode=0o700)
            os.chmod(root, 0o700)
            value = observation()
            result = contract.validate_runtime_observation(
                value,
                expected_identity(value),
                {"name": "strict", "evidence_root": root},
            )
            self.assertEqual(result.status, "VALIDATION_FAILED")
            self.assertIn("referenced evidence is unavailable or unsafe", result.errors)
            self.assertNotIn(str(root), " ".join(result.errors))

    def test_strict_live_claim_requires_a_private_evidence_root(self) -> None:
        value = observation()
        result = contract.validate_runtime_observation(value, expected_identity(value), "strict")
        self.assertEqual(result.status, "VALIDATION_FAILED")
        self.assertIn("live runtime evidence requires a private evidence root", result.errors)

    def test_absolute_path_and_payload_fields_are_rejected(self) -> None:
        value = observation()
        provenance = value["provenance"]
        assert isinstance(provenance, dict)
        provenance["source_contract"] = "/runner/private"
        self.assert_invalid(value)
        value = observation()
        value["payload"] = "forbidden"
        self.assert_invalid(value)

    def test_assertion_evidence_kind_must_bind_to_provenance(self) -> None:
        value = observation()
        runtime = value["runtime"]
        assert isinstance(runtime, dict)
        allow = runtime["allow_case"]
        assert isinstance(allow, dict)
        allow["evidence_kind"] = "live_runtime_evidence"
        self.assert_invalid(value)

    @staticmethod
    def _write_private(root: Path, contents: bytes, mode: int = 0o600) -> Path:
        root.mkdir(mode=0o700, parents=True, exist_ok=True)
        os.chmod(root, 0o700)
        path = root / "runtime-observation.json"
        path.write_bytes(contents)
        os.chmod(path, mode)
        return path

    @staticmethod
    def _encoded(value: dict[str, object]) -> bytes:
        return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")

    @staticmethod
    def _refresh_evidence_digest(value: dict[str, object]) -> None:
        provenance = value["provenance"]
        assert isinstance(provenance, dict)
        evidence = provenance["evidence"]
        assert isinstance(evidence, list)
        provenance["evidence_digest"] = contract.evidence_manifest_digest(evidence)

    def test_secure_reader_accepts_private_fixture(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-contract-") as temporary:
            root = Path(temporary) / "evidence"
            value = observation()
            path = self._write_private(root, self._encoded(value))
            fixture_evidence = root / "fixture-evidence.json"
            fixture_evidence.write_bytes(b"fixture")
            os.chmod(fixture_evidence, 0o600)
            self.assertEqual(contract.load_runtime_observation(path, evidence_root=root), value)

    def test_secure_reader_rejects_symlink(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-contract-") as temporary:
            root = Path(temporary) / "evidence"
            target = self._write_private(root, self._encoded(observation()))
            link = root / "observation-link.json"
            link.symlink_to(target.name)
            with self.assertRaises(contract.RuntimeObservationError):
                contract.load_runtime_observation(link, evidence_root=root)

    def test_secure_reader_rejects_hardlink(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-contract-") as temporary:
            root = Path(temporary) / "evidence"
            target = self._write_private(root, self._encoded(observation()))
            hardlink = root / "observation-hardlink.json"
            os.link(target, hardlink)
            with self.assertRaises(contract.RuntimeObservationError):
                contract.load_runtime_observation(hardlink, evidence_root=root)

    def test_secure_reader_rejects_unsafe_permissions(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-contract-") as temporary:
            root = Path(temporary) / "evidence"
            path = self._write_private(root, self._encoded(observation()), 0o644)
            with self.assertRaises(contract.RuntimeObservationError):
                contract.load_runtime_observation(path, evidence_root=root)

    def test_secure_reader_rejects_executable_file(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-contract-") as temporary:
            root = Path(temporary) / "evidence"
            path = self._write_private(root, self._encoded(observation()))
            os.chmod(path, 0o700)
            with self.assertRaises(contract.RuntimeObservationError):
                contract.load_runtime_observation(path, evidence_root=root)

    def test_secure_reader_rejects_group_writable_evidence_root(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-contract-") as temporary:
            root = Path(temporary) / "evidence"
            path = self._write_private(root, self._encoded(observation()))
            os.chmod(root, 0o770)
            with self.assertRaises(contract.RuntimeObservationError):
                contract.load_runtime_observation(path, evidence_root=root)

    def test_secure_reader_requires_exact_private_directory_modes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-contract-") as temporary:
            root = Path(temporary) / "evidence"
            path = self._write_private(root, self._encoded(observation()))
            os.chmod(root, 0o755)
            with self.assertRaises(contract.RuntimeObservationError):
                contract.load_runtime_observation(path, evidence_root=root)

            os.chmod(root, 0o700)
            nested = root / "normalized"
            nested.mkdir(mode=0o700)
            nested_path = nested / path.name
            path.rename(nested_path)
            os.chmod(nested, 0o750)
            with self.assertRaises(contract.RuntimeObservationError):
                contract.load_runtime_observation(nested_path, evidence_root=root)

    def test_secure_reader_rejects_wrong_owner(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-contract-") as temporary:
            root = Path(temporary) / "evidence"
            path = self._write_private(root, self._encoded(observation()))
            with mock.patch.object(contract.os, "geteuid", return_value=os.geteuid() + 1):
                with self.assertRaises(contract.RuntimeObservationError):
                    contract.load_runtime_observation(path, evidence_root=root)

    def test_secure_reader_rejects_malformed_json(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-contract-") as temporary:
            root = Path(temporary) / "evidence"
            path = self._write_private(root, b"{not-json")
            with self.assertRaises(contract.RuntimeObservationError):
                contract.load_runtime_observation(path, evidence_root=root)

    def test_secure_reader_rejects_duplicate_json_keys(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-contract-") as temporary:
            root = Path(temporary) / "evidence"
            path = self._write_private(root, b'{"schema_version":1,"schema_version":1}')
            with self.assertRaises(contract.RuntimeObservationError):
                contract.load_runtime_observation(path, evidence_root=root)

    def test_secure_reader_rejects_nonfinite_json_values(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-contract-") as temporary:
            root = Path(temporary) / "evidence"
            path = self._write_private(root, b'{"schema_version":NaN}')
            with self.assertRaises(contract.RuntimeObservationError):
                contract.load_runtime_observation(path, evidence_root=root)

    def test_secure_reader_rejects_oversized_file(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-contract-") as temporary:
            root = Path(temporary) / "evidence"
            path = self._write_private(root, b"x" * (contract.MAX_OBSERVATION_BYTES + 1))
            with self.assertRaises(contract.RuntimeObservationError):
                contract.load_runtime_observation(path, evidence_root=root)

    def test_canonical_writer_handles_a_short_write(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-contract-") as temporary:
            root = Path(temporary) / "evidence"
            root.mkdir(mode=0o700)
            payload = b'{"schema_version":1}'
            real_write = contract.os.write
            calls = 0

            def short_then_full(descriptor: int, data: bytes | memoryview) -> int:
                nonlocal calls
                calls += 1
                if calls == 1:
                    return real_write(descriptor, data[:1])
                return real_write(descriptor, data)

            with mock.patch.object(contract.os, "write", side_effect=short_then_full):
                path = contract.write_canonical_evidence_file(
                    "runtime-observation.json", payload, root
                )
            self.assertGreaterEqual(calls, 2)
            self.assertEqual(path.read_bytes(), payload)

    def test_file_snapshot_changes_when_file_timestamp_changes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-contract-") as temporary:
            root = Path(temporary) / "evidence"
            path = self._write_private(root, b"fixture")
            before = contract._file_snapshot(path.stat())
            current = path.stat()
            os.utime(path, ns=(current.st_atime_ns, current.st_mtime_ns + 1))
            self.assertNotEqual(before, contract._file_snapshot(path.stat()))

    def test_canonical_writer_is_private_and_refuses_overwrite(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-contract-") as temporary:
            root = Path(temporary) / "evidence"
            root.mkdir(mode=0o700)
            os.chmod(root, 0o700)
            normalized = root / "normalized"
            normalized.mkdir(mode=0o700)
            os.chmod(normalized, 0o700)
            path = contract.write_canonical_evidence_file(
                "runtime-observation.json", b'{"schema_version":1}', normalized
            )
            self.assertEqual(path.read_bytes(), b'{"schema_version":1}')
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            with self.assertRaises(contract.RuntimeObservationError):
                contract.write_canonical_evidence_file(
                    "runtime-observation.json", b'{"schema_version":1}', normalized
                )

    def test_structured_adapter_recomputes_private_evidence_digests(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-contract-") as temporary:
            root = Path(temporary) / "evidence"
            root.mkdir(mode=0o700)
            os.chmod(root, 0o700)
            records = []
            for name, contents in (
                ("host_configuration", b"host configuration"),
                ("allow_request", b"allow request"),
                ("block_audit", b"block audit"),
                ("cleanup", b"cleanup"),
            ):
                path = root / f"{name}.json"
                path.write_bytes(contents)
                os.chmod(path, 0o600)
                records.append({"name": name, "path": path.name})
            value = adapters.build_structured_observation(
                connector="envoy",
                integration_mode="ext_proc",
                run_id="adapter-run",
                parent_commit=PARENT_COMMIT,
                framework_commit=FRAMEWORK_COMMIT,
                mrts_commit=MRTS_COMMIT,
                rule_id=942270,
                observed_statuses={"allow": 200, "block": 403, "bypass": 403},
                cleanup={
                    "host_processes_remaining": 0,
                    "helper_processes_remaining": 0,
                    "listeners_remaining": 0,
                    "sockets_remaining": 0,
                    "pid_files_remaining": 0,
                    "temporary_paths_remaining": 0,
                },
                isolation={
                    "runner_invoked": False,
                    "case_inventory_loaded": False,
                    "process_started": False,
                    "socket_or_listener_created": False,
                    "artifact_used": False,
                },
                evidence=records,
                evidence_root=root,
                manifest_digest="a" * 64,
            )
            result = contract.validate_runtime_observation(
                value,
                expected_identity(value),
                {"name": "strict", "evidence_root": root},
            )
            self.assertTrue(result.valid, result.errors)
            records[0]["sha256"] = "0" * 64
            with self.assertRaises(adapters.ProducerEvidenceUnavailable):
                adapters.build_structured_observation(
                    connector="envoy",
                    integration_mode="ext_proc",
                    run_id="adapter-run",
                    parent_commit=PARENT_COMMIT,
                    framework_commit=FRAMEWORK_COMMIT,
                    mrts_commit=MRTS_COMMIT,
                    rule_id=942270,
                    observed_statuses={"allow": 200, "block": 403, "bypass": 403},
                    cleanup={
                        "host_processes_remaining": 0,
                        "helper_processes_remaining": 0,
                        "listeners_remaining": 0,
                        "sockets_remaining": 0,
                        "pid_files_remaining": 0,
                        "temporary_paths_remaining": 0,
                    },
                    isolation={
                        "runner_invoked": False,
                        "case_inventory_loaded": False,
                        "process_started": False,
                        "socket_or_listener_created": False,
                        "artifact_used": False,
                    },
                    evidence=records,
                    evidence_root=root,
                    manifest_digest="a" * 64,
                )

    def test_cli_validates_private_observation(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-contract-") as temporary:
            root = Path(temporary) / "evidence"
            value = observation()
            path = self._write_private(root, self._encoded(value))
            fixture_evidence = root / "fixture-evidence.json"
            fixture_evidence.write_bytes(b"fixture")
            os.chmod(fixture_evidence, 0o600)
            completed = subprocess.run(
                [
                    sys.executable,
                    str(CLI_PATH),
                    "--observation",
                    str(path),
                    "--evidence-root",
                    str(root),
                    "--connector",
                    "envoy",
                    "--profile",
                    "with-crs-no-mrts",
                    "--run-id",
                    "contract-run",
                    "--parent-sha",
                    PARENT_COMMIT,
                    "--framework-sha",
                    FRAMEWORK_COMMIT,
                    "--mrts-sha",
                    MRTS_COMMIT,
                    "--policy",
                    "strict",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(completed.stdout)
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["validation_status"], contract.CONTRACT_VALIDATED)

    def test_cli_returns_two_for_validation_failure(self) -> None:
        with tempfile.TemporaryDirectory(prefix="runtime-contract-") as temporary:
            root = Path(temporary) / "evidence"
            value = observation()
            path = self._write_private(root, self._encoded(value))
            fixture_evidence = root / "fixture-evidence.json"
            fixture_evidence.write_bytes(b"fixture")
            os.chmod(fixture_evidence, 0o600)
            completed = subprocess.run(
                [
                    sys.executable,
                    str(CLI_PATH),
                    "--observation",
                    str(path),
                    "--evidence-root",
                    str(root),
                    "--connector",
                    "traefik",
                    "--profile",
                    "with-crs-no-mrts",
                    "--run-id",
                    "contract-run",
                    "--parent-sha",
                    PARENT_COMMIT,
                    "--framework-sha",
                    FRAMEWORK_COMMIT,
                    "--mrts-sha",
                    MRTS_COMMIT,
                    "--policy",
                    "strict",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 2, completed.stderr)
            self.assertEqual(json.loads(completed.stdout)["status"], "VALIDATION_FAILED")

    def test_cli_requires_mrts_sha_for_every_profile(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(CLI_PATH),
                "--observation",
                "unused.json",
                "--connector",
                "envoy",
                "--profile",
                "with-crs-no-mrts",
                "--run-id",
                "contract-run",
                "--parent-sha",
                PARENT_COMMIT,
                "--framework-sha",
                FRAMEWORK_COMMIT,
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 2)
        self.assertIn("--mrts-sha", completed.stderr)

    def test_partial_policy_never_promotes_missing_evidence(self) -> None:
        value = observation()
        runtime = value["runtime"]
        assert isinstance(runtime, dict)
        runtime.pop("block_case")
        result = contract.validate_runtime_observation(value, expected_identity(value), "partial")
        self.assertFalse(result.valid)
        self.assertEqual(result.status, "PARTIAL")


if __name__ == "__main__":
    unittest.main()
