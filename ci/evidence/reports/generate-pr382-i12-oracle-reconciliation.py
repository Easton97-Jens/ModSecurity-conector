#!/usr/bin/env python3
"""Reconcile the immutable PR382 I12 oracle inventory without qualifying runtime."""

import argparse
import collections
import copy
import hashlib
import json
from pathlib import Path

ID_SHA256 = "a74761d9722b646873325ecd27ea99661f00bee67052980fa04ede0e1f1a0f6f"
CONTRACT_SHA256 = "c493e0a5d270121f65a6cd6a1f37bdf81f8d1304c2dd770322e5a9d017b2f8e2"
SELECTION_SHA256 = "c55de04134a31f0a6a4a64ac2af930a882b180c68e3da1855daf7972b90afa84"
CATEGORIES = frozenset((
    "SOURCE_CONFIRMED_EXPECTATION", "HOST_SEMANTICS_CONFIRMED",
    "ORACLE_DEFECT_CONFIRMED", "PRODUCT_DEFECT_CONFIRMED",
    "HARNESS_DEFECT_CONFIRMED", "UNSUPPORTED_CAPABILITY",
    "UNRESOLVED_ORACLE", "BLOCKED_ENVIRONMENT",
))
UNRESOLVED = frozenset(("UNRESOLVED_ORACLE", "BLOCKED_ENVIRONMENT"))
INDEPENDENT_KINDS = frozenset((
    "official_host_contract", "native_engine_contract", "protocol_contract",
    "independent_host_probe", "independent_engine_probe",
))


def canonical_digest(value):
    content = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(content.encode()).hexdigest()


def reference(path):
    """Bind only a physical regular file, including all parent path components."""
    path = Path(path)
    if not path.is_absolute() or path.resolve(strict=True) != path or not path.is_file():
        raise ValueError(f"Evidence is not a physical absolute regular file: {path}")
    data = path.read_bytes()
    return {"path": str(path), "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}


def verify_reference(supplied):
    observed = reference(supplied["path"])
    if observed["sha256"] != supplied.get("sha256"):
        raise ValueError("Evidence content does not match its recorded SHA256")
    if "bytes" in supplied and observed["bytes"] != supplied["bytes"]:
        raise ValueError("Evidence byte length changed")
    return {**supplied, **observed}


def original_contracts(requirements, selection):
    rows = requirements["rows"]
    ids = [row["run_scoped_case_id"] for row in rows]
    if len(ids) != 1484 or len(set(ids)) != 1484:
        raise ValueError("Original I12 catalog must contain exactly 1484 unique IDs")
    if hashlib.sha256(("\n".join(ids) + "\n").encode()).hexdigest() != ID_SHA256:
        raise ValueError("Original ordered ID stream changed")
    contracts = [row["selected_requirement"] for row in rows]
    if canonical_digest(contracts) != CONTRACT_SHA256:
        raise ValueError("Original selected contracts or original oracles changed")
    selected = [case for leg in selection["legs"] for case in leg["required_cases"]]
    if selected != contracts:
        raise ValueError("Catalog no longer matches the original source selection")
    membership = [(leg["leg_id"], leg["required_leg"]) for leg in selection["legs"] for _ in leg["required_cases"]]
    for row, (leg_id, required_leg) in zip(rows, membership, strict=True):
        if row["leg_id"] != leg_id or row["required_leg"] is not required_leg:
            raise ValueError("Original selected profile or diagnostic membership changed")
        if row["selected_requirement"]["run_scoped_case_id"] != row["run_scoped_case_id"]:
            raise ValueError("Selected ID differs from catalog row ID")
        if row["run_scoped_case_id"].split("::")[1] != row["leg_id"]:
            raise ValueError("Catalog profile identity changed")
    if sum(row["required_leg"] is True for row in rows) != 1406:
        raise ValueError("Original required/diagnostic membership changed")
    return rows


def group_requirement(contract):
    """Inventory groups describe missing work; they never supply expected values."""
    name = contract["case_id"].lower()
    if contract["origin"] == "historical_reproduction":
        return "historical_fixture_binding"
    groups = (
        ("correlation_lease", ("correlation", "lease", "ttl", "companion")),
        ("physical_event_sink", ("event-sink",)),
        ("native_body_semantics", ("request-", "response-", "body-", "native-body", "native-file", "native-memory")),
        ("commit_action", ("commit", "redirect", "profile-", "first-byte", "second-response")),
        ("transport_cleanup", ("cancel", "eos", "reset", "rst", "neighbor", "reentry", "callback", "cleanup", "reuse")),
        ("resource_identity", ("capacity", "spool", "uid", "nobody", "binary", "provenance", "reserve", "readmission")),
        ("sample_frame_scope", ("sample", "frame", "buffer", "32768", "metadata")),
    )
    for group, terms in groups:
        if any(term in name for term in terms):
            return group
    return "missing_effective_fixture_and_oracle"


def evidence_sources(record):
    independent = [verify_reference(item) for item in record.get("independent_sources", [])]
    if not independent or any(item.get("kind") not in INDEPENDENT_KINDS for item in independent):
        raise ValueError("Resolution needs a supported independent source")
    if any(not item.get("revision") for item in independent):
        raise ValueError("Independent source revision/version is missing")
    implementation = [verify_reference(item) for item in record.get("implementation_sources", [])]
    if {item["sha256"] for item in independent} & {item["sha256"] for item in implementation}:
        raise ValueError("Implementation bytes cannot also serve as independent confirmation")
    return independent, implementation


def validate_retest(supplied, case_id, leg_id, expectation):
    receipt_ref = verify_reference(supplied)
    receipt = json.loads(Path(receipt_ref["path"]).read_text())
    if receipt.get("execution_observed") is not True:
        raise ValueError("Retest requires an observed actual execution")
    if receipt.get("run_scoped_case_id") != case_id or receipt.get("leg_id") != leg_id:
        raise ValueError("Retest cannot transfer from another case or sibling profile")
    if receipt.get("oracle_sha256") != canonical_digest(expectation):
        raise ValueError("Retest was not evaluated against the reviewed effective oracle")
    for field in ("run_id", "parent_sha", "effective_config_sha256", "rules_sha256"):
        if not receipt.get(field):
            raise ValueError(f"Retest lacks actual identity binding: {field}")
    if receipt.get("oracle_evaluated") is not True or receipt.get("outcome") not in ("PASS", "FAIL"):
        raise ValueError("Retest needs explicit observed oracle evaluation")
    if not receipt.get("actual_observations") or not receipt.get("measurement_evidence"):
        raise ValueError("Retest lacks independent actual measurements")
    measurements = [verify_reference(item) for item in receipt["measurement_evidence"]]
    return {"receipt": receipt_ref, "measurement_evidence": measurements,
            "outcome": receipt["outcome"], "full_lifecycle_qualified": False}


def validate_unsupported_applicability(supplied, row, independent):
    receipt_ref = verify_reference(supplied)
    receipt = json.loads(Path(receipt_ref["path"]).read_text())
    if receipt.get("run_scoped_case_id") != row["run_scoped_case_id"] or receipt.get("leg_id") != row["leg_id"]:
        raise ValueError("Unsupported applicability cannot transfer between IDs or profiles")
    if receipt.get("capability_supported") is not False:
        raise ValueError("Unsupported disposition needs an explicit negative capability proof")
    if not receipt.get("parent_sha") or not receipt.get("effective_config_sha256"):
        raise ValueError("Unsupported applicability lacks source/config identity")
    proof = [verify_reference(item) for item in receipt.get("capability_evidence", [])]
    if not proof or not {item["sha256"] for item in proof} & {item["sha256"] for item in independent}:
        raise ValueError("Unsupported applicability lacks independent capability evidence")
    return {"receipt": receipt_ref, "capability_evidence": proof}


def validate_traefik_expected_absence(record, row, effective, independent, missing):
    """Review known absence without supplying a status, phase or runtime fact.

    Ordinary unresolved nulls remain errors. Only separately approved primary
    host/protocol sources can establish absence for an exact Traefik contract.
    Host execution and all applicable lifecycle observations remain separate.
    """
    approval = record.get("expected_absence")
    routes = {"traefik-native-uds", "traefik-forwardauth-request",
              "traefik-forwardauth-response-companion"}
    selected = row["selected_requirement"]
    identity = row["run_scoped_case_id"]
    if (not isinstance(approval, dict) or row.get("leg_id") not in routes
            or identity != f"I12::{row['leg_id']}::{selected.get('case_id')}"
            or selected.get("run_scoped_case_id") != identity
            or record.get("run_scoped_case_id") != identity):
        raise ValueError("Effective oracle still lacks an applicable expectation; exact absence approval required")
    expected = {"schema_version": 1, "reviewed_by": "root", "run_scoped_case_id": identity,
                "leg_id": row["leg_id"], "selected_requirement_sha256": canonical_digest(selected),
                "original_oracle_sha256": canonical_digest(selected["expected_oracle"])}
    if (type(approval.get("schema_version")) is not int
            or any(approval.get(name) != value for name, value in expected.items())
            or set(approval) != {*expected, "fields"}):
        raise ValueError("Expected absence needs separate Root review of the exact original contract")
    fields = approval.get("fields")
    if not isinstance(fields, dict) or not missing or set(fields) != missing:
        raise ValueError("Expected absence must cover exactly the literal null expectation fields")
    kinds = {"native_result": "no_native_decision", "phase": "no_native_phase",
             "visible_status": "no_http_response"}
    sources = {(p["path"], p["sha256"], p.get("kind"), p.get("revision")) for p in independent}
    reviewed = copy.deepcopy(approval)
    for field, supplied in fields.items():
        if (field not in effective or not isinstance(supplied, dict)
                or set(supplied) != {"kind", "reason", "proof"}
                or supplied.get("kind") != kinds[field]
                or not isinstance(supplied.get("reason"), str) or not supplied["reason"].strip()):
            raise ValueError("Expected absence needs an explicit typed reason for each literal null")
        proof = [verify_reference(item) for item in supplied.get("proof", [])]
        if (not proof or any((p["path"], p["sha256"], p.get("kind"), p.get("revision"))
                             not in sources for p in proof)
                or any(p.get("kind") not in {"official_host_contract", "protocol_contract",
                                              "native_engine_contract"} for p in proof)
                or not {"official_host_contract", "protocol_contract"} <= {p.get("kind") for p in proof}):
            raise ValueError("Expected absence requires independently reviewed primary host and protocol sources")
        reviewed["fields"][field]["proof"] = proof
    return reviewed


def review_record(record, row):
    category = record.get("category")
    if category not in CATEGORIES:
        raise ValueError("Unsupported oracle category")
    if record.get("reviewed_by") != "root" or record.get("leg_id") != row["leg_id"]:
        raise ValueError("Oracle disposition requires Root review of the exact profile")
    if not record.get("interpretation") or not record.get("scope"):
        raise ValueError("Oracle disposition needs an interpretation and scope")
    original = row["selected_requirement"]["expected_oracle"]
    effective = copy.deepcopy(original)
    independent, implementation = [], []
    if category not in UNRESOLVED or record.get("independent_sources"):
        independent, implementation = evidence_sources(record)
    applicability = None
    if category == "UNSUPPORTED_CAPABILITY":
        if not record.get("applicability_receipt"):
            raise ValueError("Unsupported capability needs an independently bound per-ID applicability receipt")
        applicability = validate_unsupported_applicability(record["applicability_receipt"], row, independent)
    correction = record.get("approved_correction")
    resolution = record.get("resolved_expectation")
    if correction is not None:
        if category != "ORACLE_DEFECT_CONFIRMED":
            raise ValueError("Only an independently confirmed oracle defect permits correction")
        if correction.get("reviewed_by") != "root" or not correction.get("reason"):
            raise ValueError("Correction lacks a separate Root approval and reason")
        proof = [verify_reference(item) for item in correction.get("proof", [])]
        if not proof or not {item["sha256"] for item in proof} & {item["sha256"] for item in independent}:
            raise ValueError("Correction lacks independently verified proof")
        effective = copy.deepcopy(correction["expected_oracle"])
    elif category == "ORACLE_DEFECT_CONFIRMED":
        raise ValueError("Confirmed oracle defect requires a separately approved correction")
    if resolution is not None:
        if category not in ("SOURCE_CONFIRMED_EXPECTATION", "HOST_SEMANTICS_CONFIRMED"):
            raise ValueError("Resolution cannot conceal product/harness defects or unresolved conflicts")
        if not original.get("unresolved_expected_value_reason"):
            raise ValueError("An existing oracle requires explicit correction rather than replacement")
        effective = copy.deepcopy(resolution)
    resolved = category not in UNRESOLVED
    absence = None
    if resolved and category != "UNSUPPORTED_CAPABILITY":
        if effective.get("unresolved_expected_value_reason"):
            raise ValueError("A resolved oracle must provide an independently bound expectation")
        if effective.get("physical_evidence_not_projection") is not True:
            raise ValueError("Effective oracle must preserve physical evidence requirement")
        missing = {field for field in ("native_result", "visible_status", "phase")
                   if effective.get(field) is None}
        if missing or record.get("expected_absence") is not None:
            absence = validate_traefik_expected_absence(record, row, effective, independent, missing)
    retest = None
    if record.get("retest") is not None:
        if not resolved or category == "UNSUPPORTED_CAPABILITY":
            raise ValueError("Unresolved or unsupported expectation cannot receive a passing retest")
        retest = validate_retest(record["retest"], row["run_scoped_case_id"], row["leg_id"], effective)
    return {"category": category, "resolved": resolved,
            "interpretation": record["interpretation"], "scope": record["scope"],
            "independent_sources": independent, "implementation_sources": implementation,
            "unsupported_applicability": applicability,
            "approved_correction": copy.deepcopy(correction), "effective_oracle": effective,
            "retest": retest, "full_lifecycle_qualified": False,
            **({"expected_absence": absence} if absence is not None else {})}


def reconcile(requirements, selection, records):
    rows = original_contracts(requirements, selection)
    unresolved_ids = [row["run_scoped_case_id"] for row in rows
                      if row["selected_requirement"]["expected_oracle"].get("unresolved_expected_value_reason")]
    if len(unresolved_ids) != 596:
        raise ValueError("Original 596-member unresolved subset changed")
    reviews = {}
    row_by_id = {row["run_scoped_case_id"]: row for row in rows}
    for record in records:
        case_id = record["run_scoped_case_id"]
        if case_id not in row_by_id or case_id in reviews:
            raise ValueError("Reviewed record has an unknown or duplicate original case ID")
        reviews[case_id] = review_record(record, row_by_id[case_id])
    inventory, supplemental = [], []
    for row in rows:
        case_id = row["run_scoped_case_id"]
        in_subset = case_id in unresolved_ids
        if not in_subset and case_id not in reviews:
            continue
        contract = row["selected_requirement"]
        entry = {"run_scoped_case_id": case_id, "leg_id": row["leg_id"],
                 "required_leg": row["required_leg"], "original_596_member": in_subset,
                 "original_oracle": copy.deepcopy(contract["expected_oracle"]),
                 "original_selected_requirement": copy.deepcopy(contract),
                 "original_source_revision": copy.deepcopy(selection["revisions"]),
                 "original_source_hashes": copy.deepcopy(selection["source_hashes"]),
                 "rootcause_group": group_requirement(contract),
                 "category": "UNRESOLVED_ORACLE", "resolved": False,
                 "interpretation": "No independently approved exact selected fixture/oracle binding.",
                 "scope": row["leg_id"], "independent_sources": [],
                 "implementation_sources": [], "approved_correction": None,
                 "effective_oracle": None, "retest": None,
                 "full_lifecycle_qualified": False}
        if case_id in reviews:
            entry.update(reviews[case_id])
        (inventory if in_subset else supplemental).append(entry)
    resolved = sum(entry["resolved"] for entry in inventory)
    return {"schema_version": 1, "original_ordered_ids": list(row_by_id),
            "original_selected_contracts": [copy.deepcopy(row["selected_requirement"]) for row in rows],
            "original_ordered_id_sha256": ID_SHA256,
            "original_selected_contract_sha256": CONTRACT_SHA256,
            "original_596_ordered_ids": unresolved_ids,
            "original_596_membership_sha256": canonical_digest(unresolved_ids),
            "summary": {"original_ids": 1484, "original_required_ids": 1406,
                        "original_diagnostic_ids": 78, "original_open_oracles": 596,
                        "resolved_original_oracles": resolved, "unresolved_original_oracles": 596 - resolved,
                        "actually_retested_original_oracles": sum(entry["retest"] is not None for entry in inventory),
                        "unsupported_original_oracles": sum(entry["category"] == "UNSUPPORTED_CAPABILITY" for entry in inventory),
                        "supplemental_original_oracle_dispositions": len(supplemental),
                        "full_lifecycle_qualification_performed": False,
                        "baseline_config_parser_pass": sum(row["status"] == "PASS" for row in rows),
                        "baseline_observed_ids": sum(row.get("execution_observed") is True for row in rows),
                        "categories": dict(collections.Counter(entry["category"] for entry in inventory)),
                        "rootcause_groups": dict(collections.Counter(entry["rootcause_group"] for entry in inventory)),
                        "by_profile": dict(collections.Counter(entry["leg_id"] for entry in inventory))},
            "oracle_matrix": inventory, "supplemental_dispositions": supplemental}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--requirements", type=Path, required=True)
    parser.add_argument("--original-selection", type=Path, required=True)
    parser.add_argument("--reviewed-records", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    inputs = [reference(path) for path in (args.requirements, args.original_selection, args.reviewed_records)]
    if inputs[1]["sha256"] != SELECTION_SHA256:
        raise ValueError("Immutable original source selection bytes changed")
    matrix = reconcile(json.loads(args.requirements.read_text()), json.loads(args.original_selection.read_text()),
                       json.loads(args.reviewed_records.read_text())["records"])
    matrix["input_evidence"] = inputs
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "oracle-reconciliation.json"
    with output.open("x", encoding="utf-8") as stream:
        json.dump(matrix, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
    print(json.dumps({"output": reference(output.absolute()), "summary": matrix["summary"]}))


if __name__ == "__main__":
    main()
