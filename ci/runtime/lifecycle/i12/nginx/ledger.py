#!/usr/bin/env python3
"""Append NGINX evidence without rewriting the original 140 selected contracts.

Packet input is a JSON list. Each entry has packet (a physical SHA256 reference),
request_identity (physical_request_path and transaction_id), and optionally
effective_oracle (a review_record input for the unchanged central reconciler).
This emitter validates evidence; it does not manufacture measurements or oracles.
"""

import argparse
import copy
import importlib.util
import json
from pathlib import Path


BASELINE_SHA256 = "a3a901db7d70884d2f491c95246629071cd55280ad94ee0fd86049c2e954c7ff"
ROOT = Path(__file__).resolve().parents[5]
SPEC = importlib.util.spec_from_file_location(
    "i12_shared_ledger", ROOT / "ci/evidence/reports/generate-pr382-i12-lifecycle-ledger.py"
)
SHARED = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SHARED)
ORACLES = SHARED.ORACLES


def selected_rows(baseline):
    """Keep the original order and the complete historical rows, including revisions."""
    rows = [row for row in baseline["rows"] if row["leg_id"] == "nginx-native"]
    ids = [row["run_scoped_case_id"] for row in rows]
    if len(rows) != 140 or len(set(ids)) != 140:
        raise ValueError("NGINX baseline must contain exactly 140 unique original IDs")
    for row in rows:
        if (not row["run_scoped_case_id"].startswith("I12::nginx-native::") or
                row.get("required_leg") is not True or
                row["selected_requirement"]["run_scoped_case_id"] != row["run_scoped_case_id"]):
            raise ValueError("Original NGINX selected identity or membership changed")
    return rows


def effective_review(row, supplied):
    if supplied is not None:
        if supplied.get("run_scoped_case_id") != row["run_scoped_case_id"]:
            raise ValueError("Oracle review must bind the same original ID")
        review = ORACLES.review_record(supplied, row)
    else:
        review = copy.deepcopy(row.get("oracle_reconciliation"))
    oracle = (review.get("effective_oracle") if review else
              row["selected_requirement"]["expected_oracle"])
    if (not oracle or oracle.get("unresolved_expected_value_reason") or
            (review and not review.get("resolved"))):
        oracle = None
    return review, oracle


def physical_identity(identity, packet, reviewed):
    """Bind one request file to the selected client receipt and native transaction."""
    request = ORACLES.reference(identity["physical_request_path"])
    transaction = reviewed["observations"]["native_transaction_id"]["value"]
    if isinstance(transaction, dict):
        transaction = transaction.get("value")
    if not transaction or identity.get("transaction_id") != transaction:
        raise ValueError("Request identity differs from observed native transaction")
    matched = False
    observed_run = None
    for proof in reviewed["observations"]["client_exit"].get("evidence", []):
        receipt_path = Path(proof["path"])
        try:
            receipt = json.loads(receipt_path.read_text())
        except (UnicodeError, json.JSONDecodeError):
            continue
        if not isinstance(receipt, dict) or receipt.get("selected_id") != packet["run_scoped_case_id"]:
            continue
        receipt_run = receipt.get("run_id") or receipt.get("roles", {}).get("run_id")
        if not receipt_run or receipt_run != packet["run_id"]:
            raise ValueError("Packet run ID differs from the actual selected client receipt run")
        for client in receipt.get("clients", []):
            argv = client.get("argv", [])
            if client.get("label") != "selected" or "--request" not in argv:
                continue
            index = argv.index("--request") + 1
            if index >= len(argv):
                continue
            # Isolation receipts retain the in-host argv. The exported physical
            # file must be that receipt's exact sibling, not a same-byte alias.
            exported = receipt_path.parent / Path(argv[index]).name
            if (str(exported) == request["path"] and
                    client.get("observation", {}).get("request_sha256") == request["sha256"]):
                matched = True
                observed_run = receipt_run
    if not matched:
        raise ValueError("Request path is not bound to the selected physical client proof")
    selected_native = []
    for proof in reviewed["observations"]["native_transaction_id"].get("evidence", []):
        for line in Path(proof["path"]).read_text().splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("transaction_id") == transaction:
                selected_native.append(row)
    if not selected_native:
        raise ValueError("No physical native rows bind the selected transaction")
    for row in selected_native:
        for field, expected in (("run", observed_run), ("profile", packet["leg_id"]),
                                ("case", packet["run_scoped_case_id"])):
            if field in row and row[field] != expected:
                raise ValueError("Selected native raw run/profile/case differs from packet identity")
    return {"physical_request": request, "transaction_id": transaction,
            "run_id": observed_run}


def build_ledger(baseline, packets):
    original = selected_rows(baseline)
    by_id = {row["run_scoped_case_id"]: row for row in original}
    additions, request_paths, transactions = {}, set(), set()
    historical_requests, historical_transactions = {}, {}
    for row in original:
        old = row.get("current_lifecycle_packet")
        if row.get("qualification_scope") != "full_host_lifecycle" or not old:
            continue
        old_packet = json.loads(Path(ORACLES.verify_reference(old["receipt"])["path"]).read_text())
        transaction = old["observations"]["native_transaction_id"]["value"]
        if isinstance(transaction, dict):
            transaction = transaction.get("value")
        historical_transactions[(old_packet["run_id"], transaction)] = row["run_scoped_case_id"]
        for proof in old["observations"]["client_exit"].get("evidence", []):
            receipt_path = Path(ORACLES.verify_reference(proof)["path"])
            receipt = json.loads(receipt_path.read_text())
            for client in receipt.get("clients", []):
                argv = client.get("argv", [])
                if client.get("label") == "selected" and "--request" in argv:
                    position = argv.index("--request") + 1
                    if position < len(argv):
                        path = str(receipt_path.parent / Path(argv[position]).name)
                        historical_requests[path] = row["run_scoped_case_id"]
    for record in packets:
        reference = ORACLES.verify_reference(record["packet"])
        packet = json.loads(Path(reference["path"]).read_text())
        case_id = packet.get("run_scoped_case_id")
        if case_id not in by_id or case_id in additions:
            raise ValueError("Unknown or duplicate original packet ID")
        review, oracle = effective_review(by_id[case_id], record.get("effective_oracle"))
        reviewed = SHARED.reviewed_packet(reference, by_id[case_id], oracle)
        if packet.get("outcome") == "PASS" and oracle is None:
            raise ValueError("An unresolved oracle cannot receive a PASS")
        identity = physical_identity(record["request_identity"], packet, reviewed)
        path = identity["physical_request"]["path"]
        transaction = (identity["run_id"], identity["transaction_id"])
        if (path in request_paths or transaction in transactions or
                historical_requests.get(path, case_id) != case_id or
                historical_transactions.get(transaction, case_id) != case_id):
            raise ValueError("A physical request or run/native transaction cannot qualify another ID")
        request_paths.add(path)
        transactions.add(transaction)
        additions[case_id] = {"packet": reviewed, "oracle_review": review,
                              "request_identity": identity}
    rows = []
    for original_row in original:
        case_id = original_row["run_scoped_case_id"]
        addition = additions.get(case_id)
        old_qualified = original_row.get("qualification_scope") == "full_host_lifecycle"
        qualified = (addition["packet"]["full_lifecycle_qualified"] if addition else old_qualified)
        status = (addition["packet"]["outcome"] if addition and qualified else
                  "PARTIAL_HOST_MEASUREMENTS" if addition else original_row["status"])
        rows.append({"run_scoped_case_id": case_id, "leg_id": "nginx-native",
                     "selected_requirement": copy.deepcopy(original_row["selected_requirement"]),
                     "baseline": copy.deepcopy(original_row), "new_evidence": addition,
                     "new_status": status, "full_lifecycle_qualified": qualified})
    unknown = [row for row in rows if row["selected_requirement"]["expected_oracle"].get(
        "unresolved_expected_value_reason")]
    resolved_before = sum(bool((row["baseline"].get("oracle_reconciliation") or {}).get("resolved"))
                          for row in unknown)
    newly_resolved = [row for row in unknown if row["new_evidence"] and
                      not (row["baseline"].get("oracle_reconciliation") or {}).get("resolved") and
                      (row["new_evidence"]["oracle_review"] or {}).get("resolved")]
    return {"schema_version": 1, "profile": "nginx-native",
            "baseline_catalog_identity": {key: baseline.get(key) for key in (
                "original_ordered_id_sha256", "original_selected_contract_sha256")},
            "summary": {"original_ids": len(rows), "original_open_oracles": len(unknown),
                        "baseline_resolved_original_oracles": resolved_before,
                        "baseline_unresolved_original_oracles": len(unknown) - resolved_before,
                        "newly_resolved_original_oracles": len(newly_resolved),
                        "new_source_confirmed_original_oracles": sum(
                            row["new_evidence"]["oracle_review"]["category"] == "SOURCE_CONFIRMED_EXPECTATION"
                            for row in newly_resolved),
                        "remaining_original_open_oracles": len(unknown) - resolved_before - len(newly_resolved),
                        "historical_rows_with_partial_execution": 97,
                        "historical_execution_composition": {
                            "native": 42, "canonical": 14, "configuration": 10, "derived": 31},
                        "new_qualified_original_ids": sum(
                            item["packet"]["full_lifecycle_qualified"] for item in additions.values()),
                        "newly_qualified_original_ids": sum(
                            item["packet"]["full_lifecycle_qualified"] and
                            by_id[case_id].get("qualification_scope") != "full_host_lifecycle"
                            for case_id, item in additions.items()),
                        "retested_previously_qualified_original_ids": sum(
                            item["packet"]["full_lifecycle_qualified"] and
                            by_id[case_id].get("qualification_scope") == "full_host_lifecycle"
                            for case_id, item in additions.items()),
                        "new_selected_physical_host_requests": len(request_paths),
                        "distinct_full_lifecycle_qualified_original_ids": sum(
                            row["full_lifecycle_qualified"] for row in rows),
                        "full_lifecycle_pass": sum(row["full_lifecycle_qualified"] and
                                                   row["new_status"] == "PASS" for row in rows),
                        "full_lifecycle_fail": sum(row["full_lifecycle_qualified"] and
                                                   row["new_status"] == "FAIL" for row in rows)},
            "rows": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("baseline", "packets", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    baseline_ref = ORACLES.reference(args.baseline)
    if baseline_ref["sha256"] != BASELINE_SHA256:
        raise ValueError("Immutable PR410 baseline SHA256 changed")
    packets_ref = ORACLES.reference(args.packets)
    result = build_ledger(json.loads(args.baseline.read_text()), json.loads(args.packets.read_text()))
    result["inputs"] = {"baseline": baseline_ref, "packets": packets_ref}
    with args.output.open("x", encoding="utf-8") as output:
        json.dump(result, output, indent=2, ensure_ascii=False)
        output.write("\n")


if __name__ == "__main__":
    main()
