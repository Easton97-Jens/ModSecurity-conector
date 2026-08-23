#!/usr/bin/env python3
"""Write a bounded GitHub summary of one real CRS/no-MRTS workflow cell.

The report deliberately consumes only fixed GitHub step outcomes.  It does not
parse same-UID writable raw runtime paths, and it never turns a missing runtime
record into a successful connector capability claim.
"""

from __future__ import annotations

import argparse
import os
import re
from collections.abc import Mapping, Sequence

try:
    from github_step_summary import append_github_step_summary
except ModuleNotFoundError:
    from ci.runtime.lifecycle.github_step_summary import append_github_step_summary


CONNECTORS = frozenset(("apache", "envoy", "haproxy", "lighttpd", "traefik"))
VALID_OUTCOMES = frozenset(("success", "failure", "skipped", "cancelled"))
STAGES = (
    ("checkout", "Checkout exact Parent head", "CHECKOUT_OUTCOME"),
    ("setup_python", "Locked Python toolchain", "SETUP_PYTHON_OUTCOME"),
    ("verify_python", "Python interpreter contract", "VERIFY_PYTHON_OUTCOME"),
    ("verify_revisions", "Parent/Framework/MRTS revisions", "VERIFY_REVISIONS_OUTCOME"),
    ("install_dependencies", "Hash-locked Framework dependency", "INSTALL_DEPENDENCIES_OUTCOME"),
    ("verify_cell", "Fixed runtime-cell policy", "VERIFY_CELL_OUTCOME"),
    ("initialize_roots", "Private runtime roots", "INITIALIZE_ROOTS_OUTCOME"),
    ("prepare_crs", "Workflow CRS source preparation", "PREPARE_CRS_OUTCOME"),
    ("runtime", "Real connector runtime target", "RUNTIME_OUTCOME"),
    ("upload_evidence", "Evidence publication", "UPLOAD_EVIDENCE_OUTCOME"),
)
SECURITY_SKIPPED_STAGE = ("haproxy", "upload_evidence")


def require_connector(value: str) -> str:
    if value not in CONNECTORS:
        raise ValueError("connector is outside the fixed CRS/no-MRTS runtime set")
    return value


def outcomes_from_environment(environment: Mapping[str, str]) -> dict[str, str]:
    outcomes: dict[str, str] = {}
    for key, _label, environment_name in STAGES:
        value = environment.get(environment_name, "")
        if value not in VALID_OUTCOMES:
            raise ValueError(f"{environment_name} is not a GitHub step outcome")
        outcomes[key] = value
    return outcomes


def rendered_outcome(connector: str, stage: str, outcome: str) -> str:
    if (connector, stage) == SECURITY_SKIPPED_STAGE and outcome == "skipped":
        return "skipped_by_security_policy"
    return outcome


def outcome_counts(connector: str, outcomes: Mapping[str, str]) -> dict[str, int]:
    counts = {
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "cancelled": 0,
        "security_skipped": 0,
    }
    for stage, _label, _environment_name in STAGES:
        outcome = outcomes[stage]
        if rendered_outcome(connector, stage, outcome) == "skipped_by_security_policy":
            counts["security_skipped"] += 1
        elif outcome == "success":
            counts["passed"] += 1
        elif outcome == "failure":
            counts["failed"] += 1
        elif outcome == "skipped":
            counts["skipped"] += 1
        else:
            counts["cancelled"] += 1
    return counts


def first_nonpassing_stage(connector: str, outcomes: Mapping[str, str]) -> str:
    for stage, label, _environment_name in STAGES:
        outcome = rendered_outcome(connector, stage, outcomes[stage])
        if outcome != "success" and outcome != "skipped_by_security_policy":
            return label
    return "none"


def runtime_bundle_outcome(outcome: str) -> str:
    if outcome == "success":
        return "PASS — real target completed its fail-closed runtime assertions"
    if outcome == "failure":
        return "FAIL — runtime assertions did not complete"
    if outcome == "skipped":
        return "MISSING — runtime target did not run"
    return "CANCELLED — runtime target did not complete"


def render_summary(connector: str, outcomes: Mapping[str, str]) -> str:
    connector = require_connector(connector)
    if set(outcomes) != {stage for stage, _label, _environment_name in STAGES}:
        raise ValueError("summary outcomes do not match the fixed workflow stage set")
    if any(outcome not in VALID_OUTCOMES for outcome in outcomes.values()):
        raise ValueError("summary outcomes contain an invalid state")
    counts = outcome_counts(connector, outcomes)
    rows = [
        f"### {connector} — CRS/no-MRTS runtime overview",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Stages passed | `{counts['passed']}` |",
        f"| Stages failed | `{counts['failed']}` |",
        f"| Stages skipped | `{counts['skipped']}` |",
        f"| Stages cancelled | `{counts['cancelled']}` |",
        f"| Security-policy skips | `{counts['security_skipped']}` |",
        f"| First non-passing stage | `{first_nonpassing_stage(connector, outcomes)}` |",
        "",
        "| Stage | Actual outcome |",
        "| --- | --- |",
    ]
    rows.extend(
        f"| {label} | `{rendered_outcome(connector, stage, outcomes[stage])}` |"
        for stage, label, _environment_name in STAGES
    )
    rows.extend(
        (
            "",
            "| Real runtime assertion bundle | Outcome |",
            "| --- | --- |",
            "| Config/load, start, allow request, CRS block/rule, bypass, no-MRTS, cleanup | "
            f"`{runtime_bundle_outcome(outcomes['runtime'])}` |",
            "",
            "The table reports observed GitHub step outcomes only. A missing or failed runtime "
            "target is never promoted to a connector capability pass. HAProxy evidence publication "
            "is shown separately when skipped by the existing same-UID artifact-security policy.",
            "",
        )
    )
    return "\n".join(rows)


def main(arguments: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector", required=True)
    args = parser.parse_args(arguments)
    try:
        append_github_step_summary(
            os.environ,
            render_summary(args.connector, outcomes_from_environment(os.environ)),
        )
    except (OSError, ValueError) as error:
        print(f"FAIL: {error}", file=os.sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
