#!/usr/bin/env python3
"""Apache-only I12 acceptance ledger; historical results never become fresh tests.

Packet and oracle review use the existing shared validators unchanged. This
adapter inventories evidence; it does not execute cases or infer observations.
"""

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path


def load_shared():
    path = Path(__file__).resolve().parents[3] / "evidence/reports/generate-pr382-i12-lifecycle-ledger.py"
    spec = importlib.util.spec_from_file_location("apache_i12_shared_ledger", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SHARED = load_shared()
ORACLES = SHARED.ORACLES


def apache_rows(baseline):
    """Check the immutable complete catalog before selecting the Apache slice."""
    rows = baseline["rows"]
    ids = [row["run_scoped_case_id"] for row in rows]
    if len(ids) != 1484 or len(set(ids)) != 1484:
        raise ValueError("Baseline requires all 1484 unique original IDs")
    if hashlib.sha256(("\n".join(ids) + "\n").encode()).hexdigest() != ORACLES.ID_SHA256:
        raise ValueError("Original ordered IDs changed")
    if ORACLES.canonical_digest([row["selected_requirement"] for row in rows]) != ORACLES.CONTRACT_SHA256:
        raise ValueError("Original selected requirements or oracles changed")
    for row in rows:
        if (row["run_scoped_case_id"].split("::")[1] != row["leg_id"] or
                row["selected_requirement"]["run_scoped_case_id"] != row["run_scoped_case_id"]):
            raise ValueError("Baseline case/profile identity changed")
    selected = [row for row in rows if row["leg_id"] == "apache-native"]
    if len(selected) != 155 or any(row["required_leg"] is not True for row in selected):
        raise ValueError("Apache requires exactly 155 mandatory cases")
    return selected


def build_ledger(baseline, packets, oracle_records=(), expected_identity=None):
    original = apache_rows(baseline)
    by_id = {row["run_scoped_case_id"]: row for row in original}
    reviews = {}
    for record in oracle_records:
        identity = record["run_scoped_case_id"]
        if identity not in by_id or identity in reviews:
            raise ValueError("Unknown, foreign or duplicate Apache oracle ID")
        reviews[identity] = ORACLES.review_record(record, by_id[identity])
    observations = {}
    for supplied in packets:
        ref = ORACLES.verify_reference(supplied)
        packet = json.loads(Path(ref["path"]).read_text())
        identity = packet["run_scoped_case_id"]
        if identity not in by_id or identity in observations:
            raise ValueError("Unknown, foreign or duplicate Apache packet ID")
        for name, value in (expected_identity or {}).items():
            if packet.get(name) != value:
                raise ValueError(f"Packet does not bind expected identity: {name}")
        row = by_id[identity]
        review = reviews.get(identity, row.get("oracle_reconciliation"))
        oracle = (review.get("effective_oracle") if review else
                  row["selected_requirement"]["expected_oracle"])
        if oracle and oracle.get("unresolved_expected_value_reason"):
            oracle = None
        observations[identity] = SHARED.reviewed_packet(ref, row, oracle)
    rows = []
    for old in original:
        identity = old["run_scoped_case_id"]
        fresh = observations.get(identity)
        qualified = fresh is not None and fresh["full_lifecycle_qualified"]
        rows.append({
            "run_scoped_case_id": identity, "leg_id": "apache-native", "required_leg": True,
            "selected_requirement": copy.deepcopy(old["selected_requirement"]),
            "original_oracle": copy.deepcopy(old["selected_requirement"]["expected_oracle"]),
            "historical_result": copy.deepcopy(old),
            "oracle_reconciliation": copy.deepcopy(reviews.get(identity, old.get("oracle_reconciliation"))),
            "fresh_packet": fresh,
            "fresh_observations": copy.deepcopy(fresh["observations"]) if fresh else {
                name: {"value": None, "reason": "No newly reviewed Apache host packet for this original ID."}
                for name in SHARED.ROLES},
            "fresh_execution_observed": fresh is not None,
            "fresh_full_lifecycle_qualified": qualified,
            "fresh_outcome": fresh["outcome"] if qualified else None,
            "fresh_qualified_pass": qualified and fresh["outcome"] == "PASS",
        })
    subset = [row for row in rows if row["original_oracle"].get("unresolved_expected_value_reason")]
    resolved = sum(bool(row["oracle_reconciliation"] and row["oracle_reconciliation"].get("resolved"))
                   for row in subset)
    return {
        "schema_version": 1, "scope": "apache-native", "i12_complete": False,
        "original_ordered_id_sha256": ORACLES.ID_SHA256,
        "original_selected_contract_sha256": ORACLES.CONTRACT_SHA256,
        "summary": {
            "required_cases": 155,
            "historical_executed": sum(row.get("execution_observed") is True for row in original),
            "historical_configuration_pass": sum(row.get("qualification_scope") == "historical_configuration_only"
                                                 and row["status"] == "PASS" for row in original),
            "historical_full_lifecycle_pass": sum(row.get("qualification_scope") == "full_host_lifecycle"
                                                  and row["status"] == "PASS" for row in original),
            "fresh_executed": sum(row["fresh_execution_observed"] for row in rows),
            "fresh_full_lifecycle_pass": sum(row["fresh_qualified_pass"] for row in rows),
            "fresh_full_lifecycle_fail": sum(row["fresh_outcome"] == "FAIL" for row in rows),
            "missing_fresh_full_qualification": sum(not row["fresh_full_lifecycle_qualified"] for row in rows),
            "original_open_oracle_subset": len(subset),
            "resolved_original_oracles": resolved,
            "unresolved_original_oracles": len(subset) - resolved,
        }, "rows": rows,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("baseline-ledger", "reviewed-packets", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--reviewed-oracles", type=Path)
    parser.add_argument("--expected-run-id")
    parser.add_argument("--expected-parent-sha")
    args = parser.parse_args()
    inputs = [ORACLES.reference(path.absolute()) for path in
              (args.baseline_ledger, args.reviewed_packets)]
    records = []
    if args.reviewed_oracles:
        inputs.append(ORACLES.reference(args.reviewed_oracles.absolute()))
        records = json.loads(args.reviewed_oracles.read_text())["records"]
    expected = {name: value for name, value in
                (("run_id", args.expected_run_id), ("parent_sha", args.expected_parent_sha)) if value is not None}
    result = build_ledger(json.loads(args.baseline_ledger.read_text()),
                          json.loads(args.reviewed_packets.read_text())["packets"], records, expected)
    result["input_evidence"] = inputs
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
    print(json.dumps({"output": ORACLES.reference(args.output.absolute()), "summary": result["summary"]}))


if __name__ == "__main__":
    main()
