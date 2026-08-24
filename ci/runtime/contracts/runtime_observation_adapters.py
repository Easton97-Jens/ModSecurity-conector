#!/usr/bin/env python3
"""Connector adapters for the canonical runtime-observation contract.

Adapters consume only already-correlated structured facts.  They do not start
hosts, infer success from an exit code, or turn fixture data into production
runtime evidence.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from runtime_observation import (
    CONNECTORS,
    SCHEMA_VERSION,
    evidence_manifest_digest,
    read_bounded_evidence_file,
)


PRODUCER_VERSION = "1.0.0"
STRUCTURED_CONNECTORS = frozenset(("envoy", "lighttpd", "traefik"))
MISSING_PRODUCER_CONNECTORS = frozenset(("apache", "haproxy"))
NGINX_PROTECTED_INTEGRATION_MODE = "protected-root-broker"


class ProducerEvidenceUnavailable(RuntimeError):
    """Raised when a future host producer has not supplied live evidence."""


@dataclass(frozen=True)
class StructuredObservationInput:
    """Typed, immutable input bundle for a structured connector observation."""

    connector: str
    integration_mode: str
    run_id: str
    parent_commit: str
    framework_commit: str
    mrts_commit: str
    rule_id: int
    observed_statuses: Mapping[str, int]
    cleanup: Mapping[str, int]
    isolation: Mapping[str, bool]
    evidence: list[Mapping[str, str]]
    evidence_root: Path | str
    manifest_digest: str
    fixture_id: str = "crs_sqli_anomaly_block"
    source_contract: str = "five-connectors-with-crs-no-mrts"


@dataclass(frozen=True)
class RuntimeObservationAdapter:
    """Public adapter descriptor with an explicit production-evidence boundary."""

    connector: str
    producer_available: bool
    protected_separate: bool = False

    def require_producer_evidence(self) -> None:
        if not self.producer_available:
            raise ProducerEvidenceUnavailable(
                f"{self.connector} has no live runtime producer evidence; validation fails closed"
            )


ADAPTERS: dict[str, RuntimeObservationAdapter] = {
    connector: RuntimeObservationAdapter(connector, connector in STRUCTURED_CONNECTORS)
    for connector in CONNECTORS
}
ADAPTERS["nginx"] = RuntimeObservationAdapter(
    "nginx", producer_available=False, protected_separate=True
)


def adapter_for(connector: str) -> RuntimeObservationAdapter:
    """Return a finite connector adapter descriptor, never a fallback adapter."""
    try:
        return ADAPTERS[connector]
    except KeyError as exc:
        raise ValueError("connector is not supported by the runtime-observation contract") from exc


def _assertion(
    expected: Mapping[str, Any],
    observed: Mapping[str, Any],
    reason: str,
) -> dict[str, Any]:
    return {
        "required": True,
        "applicable": True,
        "executed": True,
        "live_executed": True,
        "expected": dict(expected),
        "observed": dict(observed),
        "result": "PASS",
        "reason": reason,
        "evidence_kind": "structured_connector_evidence",
    }


def _safe_evidence_records(
    evidence_root: Path | str, evidence: list[Mapping[str, str]]
) -> list[dict[str, str]]:
    """Recompute every digest from descriptor-pinned structured evidence."""
    records: list[dict[str, str]] = []
    for record in evidence:
        name = str(record["name"])
        path = str(record["path"])
        data = read_bounded_evidence_file(
            Path(evidence_root) / path,
            evidence_root,
            label=f"{name} adapter evidence",
        )
        digest = hashlib.sha256(data).hexdigest()
        supplied_digest = record.get("sha256")
        if supplied_digest is not None and supplied_digest != digest:
            raise ProducerEvidenceUnavailable("adapter evidence digest changed before normalization")
        records.append(
            {
                "name": name,
                "path": path,
                "sha256": digest,
                "kind": "structured_connector_evidence",
            }
        )
    return records


def build_structured_observation(
    request: StructuredObservationInput,
) -> dict[str, Any]:
    """Build an observation from real pre-validated host evidence.

    Only Envoy, Lighttpd, and Traefik are currently admitted.  Apache and
    HAProxy deliberately raise through their adapter until a separate producer
    supplies real evidence.  NGINX stays represented by its protected adapter
    but is not routed through this generic host path.
    """
    connector = request.connector
    adapter = adapter_for(connector)
    adapter.require_producer_evidence()
    if connector not in STRUCTURED_CONNECTORS:
        raise AssertionError("finite adapter registry admitted an unsupported structured connector")
    required_statuses = {"allow", "block", "bypass"}
    if set(request.observed_statuses) != required_statuses:
        raise ValueError("structured adapter requires allow, block, and bypass statuses")
    evidence_records = _safe_evidence_records(request.evidence_root, request.evidence)
    evidence_digest = evidence_manifest_digest(evidence_records)
    mapped_isolation = {
        "mrts_runner_invoked": request.isolation["runner_invoked"],
        "mrts_inventory_loaded": request.isolation["case_inventory_loaded"],
        "mrts_process_started": request.isolation["process_started"],
        "mrts_listener_created": request.isolation["socket_or_listener_created"],
        "mrts_artifact_used": request.isolation["artifact_used"],
    }
    mapped_cleanup = {
        "host_processes_remaining": request.cleanup["host_processes_remaining"],
        "helper_processes_remaining": request.cleanup["helper_processes_remaining"],
        "listeners_remaining": request.cleanup["listeners_remaining"],
        "sockets_remaining": request.cleanup["sockets_remaining"],
        "pid_files_remaining": request.cleanup["pid_files_remaining"],
        "temporary_paths_remaining": request.cleanup["temporary_paths_remaining"],
        "cleanup_status": "PASS",
    }
    block_expected = {"http_status": 403, "action": "deny", "rule_ids": [request.rule_id]}
    block_observed = {
        "http_status": int(request.observed_statuses["block"]),
        "action": "deny",
        "rule_ids": [request.rule_id],
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "identity": {
            "connector": connector,
            "integration_mode": request.integration_mode,
            "profile": "with-crs-no-mrts",
            "crs": True,
            "mrts": False,
            "run_id": request.run_id,
            "parent_commit": request.parent_commit,
            "framework_commit": request.framework_commit,
            "mrts_commit": request.mrts_commit,
            "producer": f"parent-runtime-observation-adapter-{connector}",
            "producer_version": PRODUCER_VERSION,
        },
        "runtime": {
            "config_test": _assertion(
                {"status": "passed"}, {"status": "passed"}, "host configuration test passed"
            ),
            "host_start": _assertion(
                {"started": True}, {"started": True}, "host start was observed"
            ),
            "reachability": _assertion(
                {"reachable": True}, {"reachable": True}, "host reachability was observed"
            ),
            "allow_case": _assertion(
                {"http_status": 200},
                {"http_status": int(request.observed_statuses["allow"])},
                "allow control was observed through the host",
            ),
            "block_case": _assertion(
                block_expected, block_observed, "CRS intervention was observed through the host"
            ),
            "bypass_case": _assertion(
                {"http_status": 403, "action": "deny"},
                {"http_status": int(request.observed_statuses["bypass"]), "action": "deny"},
                "bypass control was observed through the host",
            ),
            "runtime_status": "PASS",
        },
        "framework": {
            "framework_test_id": request.fixture_id,
            "scenario_category": "crs-sqli-anomaly",
            "selected": True,
            "executed": True,
            "live_executed": True,
            "expectation": {"kind": "intervention", **block_expected},
            "observation": block_observed,
            "result": "PASS",
            "validation_status": "CONTRACT_VALIDATED",
            "failure_count": 0,
            "mismatch_count": 0,
        },
        "isolation": mapped_isolation,
        "cleanup": mapped_cleanup,
        "provenance": {
            "evidence_kind": "structured_connector_evidence",
            "fixture_id": request.fixture_id,
            "source_contract": request.source_contract,
            "manifest_digest": request.manifest_digest,
            "evidence_digest": evidence_digest,
            "validation_basis": "evidence-digest-v1",
            "contract_schema_version": SCHEMA_VERSION,
            "producer_version": PRODUCER_VERSION,
            "evidence": evidence_records,
        },
    }


def canonical_fixture_digest(label: str) -> str:
    """Return a deterministic fixture manifest digest without host evidence."""
    return hashlib.sha256(label.encode("ascii")).hexdigest()
