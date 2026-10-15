#!/usr/bin/env python3
"""Package the Apache-only I12 ledger without converting partial runs into PASS.

Original contracts remain inline. Large actual observations remain in physical,
SHA256-bound packets and are addressed with JSON pointers. Unknown observations
retain their literal null values and reasons. This is a packaging adapter, not
an independent oracle evaluator or a host runner.
"""

import argparse
import copy
import importlib.util
import json
from pathlib import Path


def load_ledger():
    spec = importlib.util.spec_from_file_location("apache_i12_packaging_ledger", Path(__file__).with_name("ledger.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


LEDGER = load_ledger()
ORACLES = LEDGER.ORACLES
ROLES = LEDGER.SHARED.ROLES


def read(path):
    return json.loads(Path(path).read_text())


def ref(path):
    return ORACLES.reference(Path(path).resolve(strict=True))


def compact_observations(observations, packet_reference):
    """Reference actual values rather than copying megabytes of capture rows."""
    if set(observations) != set(ROLES):
        raise ValueError("All 35 observation roles must remain explicit")
    result = {}
    for name, item in observations.items():
        if item.get("value") is None:
            result[name] = copy.deepcopy(item)
        else:
            if packet_reference is None:
                raise ValueError("A known observation requires a physical packet reference")
            result[name] = {"observed_value_reference": {"packet_sha256": packet_reference["sha256"],
                "json_pointer": "/observations/" + name}, "applicable": item.get("applicable", True)}
    return result


def check_rows(source):
    rows = source["rows"]
    if source.get("scope") != "apache-native" or len(rows) != 155:
        raise ValueError("Packaging requires the complete Apache-only 155-row adapter output")
    if (source.get("original_ordered_id_sha256") != ORACLES.ID_SHA256 or
            source.get("original_selected_contract_sha256") != ORACLES.CONTRACT_SHA256):
        raise ValueError("Original catalog digests are missing or changed")
    seen = set()
    for row in rows:
        identity = row["run_scoped_case_id"]
        if identity in seen or not identity.startswith("I12::apache-native::") or row["leg_id"] != "apache-native":
            raise ValueError("Duplicate or foreign Apache ID")
        if row.get("required_leg") is not True or row["selected_requirement"]["run_scoped_case_id"] != identity:
            raise ValueError("Selected requirement identity or mandatory membership changed")
        if row["original_oracle"] != row["selected_requirement"]["expected_oracle"]:
            raise ValueError("Original oracle differs from the preserved selected requirement")
        seen.add(identity)
    return rows


def oracle_summary(review):
    if review is None:
        return None
    keys = ("category", "resolved", "interpretation", "scope", "effective_oracle", "independent_sources",
            "implementation_sources", "unsupported_applicability", "approved_correction", "retest")
    return {key: copy.deepcopy(review.get(key)) for key in keys}


def package(source_path, run_root, candidate_index=None, sink_readback=None):
    run_root = Path(run_root).resolve(strict=True)
    source_path = Path(source_path).resolve(strict=True)
    source = read(source_path)
    rows = check_rows(source)
    by_id = {row["run_scoped_case_id"]: row for row in rows}
    candidate_index = Path(candidate_index) if candidate_index else run_root / "candidate-index.json"
    sink_readback = Path(sink_readback) if sink_readback else run_root / "sink-readback.json"
    candidates = read(candidate_index)
    sinks = read(sink_readback)
    packets, candidate_by_id, sinks_by_id = {}, {}, {}
    attempts, run_indices = {}, []

    def packet_reference(supplied):
        receipt = ORACLES.verify_reference(supplied)
        packet = read(receipt["path"])
        digest = receipt["sha256"]
        if digest not in packets:
            keys = ("run_scoped_case_id", "actual_scenario_variant", "reviewed_by", "execution_observed", "execution_kind",
                    "run_id", "parent_sha", "evidence_branch_base", "framework_sha", "mrts_sha", "mrts_scope",
                    "effective_config_sha256", "rules_sha256", "actual_attempt", "oracle_evaluated", "oracle_sha256",
                    "outcome", "full_lifecycle_qualified", "review_checks", "unknown_fields", "scope_limits")
            packets[digest] = {"receipt": receipt, **{key: copy.deepcopy(packet.get(key)) for key in keys}}
        return receipt, packet

    def add_attempt(path):
        if not path or path in attempts:
            return
        controller = Path(path) / "controller-result.json"
        attempts[path] = {"attempt": path, "controller": ref(controller) if controller.is_file() else None}

    for entry in candidates:
        identity = entry["case_id"]
        if identity not in by_id:
            raise ValueError("Candidate index contains a foreign or unknown original ID")
        compact = {key: copy.deepcopy(entry.get(key)) for key in
                   ("attempt", "variant", "controller_exit", "extraction_error", "unknown_fields", "review_checks")}
        add_attempt(entry.get("attempt"))
        supplied = entry.get("candidate")
        if supplied:
            receipt, packet = packet_reference(supplied)
            if packet["run_scoped_case_id"] != identity:
                raise ValueError("Candidate packet cannot transfer to another selected ID")
            compact["candidate"] = receipt
            compact["actual_execution_observed"] = packet.get("execution_observed") is True
            compact["unsigned_candidate_does_not_qualify"] = True
        else:
            compact["candidate"] = None
            compact["actual_execution_observed"] = None
        candidate_by_id.setdefault(identity, []).append(compact)
    for entry in sinks["cases"]:
        identity = entry["case_id"]
        if identity not in by_id:
            raise ValueError("Sink readback contains a foreign or unknown original ID")
        evidence = [ORACLES.verify_reference(item) for item in entry.get("evidence", [])]
        add_attempt(entry.get("actual_attempt"))
        sinks_by_id.setdefault(identity, []).append({
            "fault": entry.get("fault"), "actual_attempt": entry.get("actual_attempt"),
            "controller_exit": entry.get("controller_exit"), "actual_candidate_exit": entry.get("actual_candidate_exit"),
            "full_lifecycle_qualified": entry.get("full_lifecycle_qualified"), "outcome": entry.get("outcome"),
            "source_readback": ref(sink_readback),
            "json_pointer": "/cases/" + str(sinks["cases"].index(entry)),
            "actual_clients": [{key: client.get(key) for key in
                ("role", "waited_exit", "actual_signal", "status", "entity_bytes", "entity_sha256", "backend_requests")}
                for client in entry.get("clients", [])], "evidence": evidence,
            "limitations": copy.deepcopy(entry.get("limitations")),
        })
    for path in sorted(run_root.glob("*runs/index.json")):
        records = read(path)
        run_indices.append({"reference": ref(path), "records": len(records)})
        for entry in records:
            add_attempt(entry.get("attempt"))

    packaged = []
    for row in rows:
        identity = row["run_scoped_case_id"]
        old = row["historical_result"]
        fresh = row.get("fresh_packet")
        receipt, packet = None, None
        if fresh:
            receipt, packet = packet_reference(fresh["receipt"])
            review = row.get("oracle_reconciliation")
            effective = review.get("effective_oracle") if review else row["original_oracle"]
            if effective and effective.get("unresolved_expected_value_reason"):
                effective = None
            validated = LEDGER.SHARED.reviewed_packet(receipt, row, effective)
            if any(validated[key] != fresh[key] for key in
                   ("execution_observed", "full_lifecycle_qualified", "outcome", "unknown_fields", "observations")):
                raise ValueError("Adapter's accepted packet differs from fresh shared validation")
            if (row["fresh_full_lifecycle_qualified"] != validated["full_lifecycle_qualified"] or
                    row["fresh_outcome"] != validated["outcome"] or
                    row["fresh_qualified_pass"] != (validated["full_lifecycle_qualified"] and validated["outcome"] == "PASS")):
                raise ValueError("Adapter qualification flags do not match its physical packet")
            add_attempt(packet.get("actual_attempt"))
        elif row["fresh_full_lifecycle_qualified"] or row["fresh_qualified_pass"] or row["fresh_outcome"] is not None:
            raise ValueError("No accepted packet means no fresh qualification")
        raw = candidate_by_id.get(identity, [])
        sink_cases = sinks_by_id.get(identity, [])
        observed = row["fresh_execution_observed"] or any(item["actual_execution_observed"] is True for item in raw) or any(
            item["actual_clients"] for item in sink_cases)
        qualified = row["fresh_full_lifecycle_qualified"]
        observations = row["fresh_observations"]
        observation_receipt = receipt
        # An unsigned candidate can establish physical partial measurements, but
        # it never changes the shared validator's acceptance verdict.
        if not fresh:
            actual_candidates = [item for item in raw if item.get("candidate") and item["actual_execution_observed"]]
            if actual_candidates:
                observation_receipt, actual = packet_reference(actual_candidates[-1]["candidate"])
                observations = actual["observations"]
        packaged.append({
            "run_scoped_case_id": identity, "leg_id": "apache-native", "required_leg": True,
            "selected_requirement": copy.deepcopy(row["selected_requirement"]),
            "original_oracle": copy.deepcopy(row["original_oracle"]),
            "original_54_oracle_member": bool(row["original_oracle"].get("unresolved_expected_value_reason")),
            "oracle_reconciliation": oracle_summary(row.get("oracle_reconciliation")),
            "historical": {"status": old["status"], "execution_observed": old.get("execution_observed"),
                "qualification_scope": old.get("qualification_scope"),
                "configuration_pass": old.get("qualification_scope") == "historical_configuration_only" and old["status"] == "PASS",
                "full_lifecycle_pass": old.get("qualification_scope") == "full_host_lifecycle" and old["status"] == "PASS"},
            "fresh": {"execution_observed": bool(observed), "accepted_execution_observed": row["fresh_execution_observed"],
                "full_lifecycle_qualified": qualified, "outcome": row["fresh_outcome"], "qualified_pass": row["fresh_qualified_pass"],
                "qualification": "FULL_HOST_LIFECYCLE" if qualified else "PARTIAL_HOST_MEASUREMENTS" if observed else "NOT_EXECUTED",
                "accepted_packet": receipt,
                "observation_packet": observation_receipt,
                "observations": compact_observations(observations, observation_receipt),
                "candidate_attempts": raw, "sink_attempts": sink_cases},
        })
    source_summary = copy.deepcopy(source["summary"])
    result = {"schema_version": 1, "scope": "apache-native", "i12_complete": False,
        "packaging_does_not_qualify_runtime": True,
        "original_ordered_id_sha256": source["original_ordered_id_sha256"],
        "original_selected_contract_sha256": source["original_selected_contract_sha256"],
        "source_full_ledger": ref(source_path), "source_summary": source_summary,
        "summary": {"required_cases": len(packaged),
            "fresh_actual_executed_ids_including_unqualified": sum(row["fresh"]["execution_observed"] for row in packaged),
            "fresh_full_lifecycle_pass": sum(row["fresh"]["qualified_pass"] for row in packaged),
            "fresh_full_lifecycle_fail": sum(row["fresh"]["outcome"] == "FAIL" for row in packaged),
            "fresh_partial_ids": sum(row["fresh"]["qualification"] == "PARTIAL_HOST_MEASUREMENTS" for row in packaged),
            "fresh_not_executed_ids": sum(row["fresh"]["qualification"] == "NOT_EXECUTED" for row in packaged),
            "raw_attempts": len(attempts), "original_open_oracle_subset": source_summary["original_open_oracle_subset"],
            "resolved_original_oracles": source_summary["resolved_original_oracles"],
            "unresolved_original_oracles": source_summary["unresolved_original_oracles"]},
        "input_evidence": [ref(candidate_index), ref(sink_readback)],
        "run_indices": run_indices, "raw_attempts": list(attempts.values()),
        "packet_registry": packets, "rows": packaged}
    for name in ("reviewed-packets.json", "reviewed-oracles.json"):
        path = run_root / name
        if path.is_file():
            result["input_evidence"].append(ref(path))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--candidate-index", type=Path)
    parser.add_argument("--sink-readback", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = package(args.ledger, args.run_root, args.candidate_index, args.sink_readback)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
    print(json.dumps({"output": ref(args.output), "summary": result["summary"]}))


if __name__ == "__main__":
    main()
