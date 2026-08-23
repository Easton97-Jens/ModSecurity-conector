#!/usr/bin/env python3
"""Write a bounded GitHub summary for one no-CRS/with-MRTS runtime cell.

The report consumes only fixed GitHub step outcomes. It does not parse raw
runtime files or same-UID writable evidence, and it never promotes a missing
or failed runtime step to a connector capability pass.
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
    ("checkout", "Checkout exact workflow revision", "CHECKOUT_OUTCOME"),
    ("setup_python", "Locked Python toolchain", "SETUP_PYTHON_OUTCOME"),
    ("setup_go", "Locked Go toolchain", "SETUP_GO_OUTCOME"),
    ("verify_python", "Python interpreter contract", "VERIFY_PYTHON_OUTCOME"),
    ("verify_go", "Go interpreter contract", "VERIFY_GO_OUTCOME"),
    ("verify_cell", "Closed no-CRS/with-MRTS cell", "VERIFY_CELL_OUTCOME"),
    ("prepare_runtime", "Connector-isolated runtime preparation", "PREPARE_RUNTIME_OUTCOME"),
    ("runtime", "Real connector MRTS host runtime", "RUNTIME_OUTCOME"),
    ("upload_evidence", "Isolated runtime evidence publication", "UPLOAD_EVIDENCE_OUTCOME"),
)


def require_connector(value: str) -> str:
    if value not in CONNECTORS:
        raise ValueError("connector is outside the fixed no-CRS/with-MRTS runtime set")
    return value


def outcomes_from_environment(environment: Mapping[str, str]) -> dict[str, str]:
    outcomes: dict[str, str] = {}
    for key, _label, environment_name in STAGES:
        value = environment.get(environment_name, "")
        if value not in VALID_OUTCOMES:
            raise ValueError(f"{environment_name} is not a GitHub step outcome")
        outcomes[key] = value
    return outcomes


def outcome_counts(outcomes: Mapping[str, str]) -> dict[str, int]:
    counts = {"passed": 0, "failed": 0, "skipped": 0, "cancelled": 0}
    for stage, _label, _environment_name in STAGES:
        outcome = outcomes[stage]
        if outcome == "success":
            counts["passed"] += 1
        elif outcome == "failure":
            counts["failed"] += 1
        elif outcome == "skipped":
            counts["skipped"] += 1
        else:
            counts["cancelled"] += 1
    return counts


def first_nonpassing_stage(outcomes: Mapping[str, str]) -> str:
    for stage, label, _environment_name in STAGES:
        if outcomes[stage] != "success":
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
    counts = outcome_counts(outcomes)
    rows = [
        f"### {connector} — no-CRS/with-MRTS runtime overview",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Stages passed | `{counts['passed']}` |",
        f"| Stages failed | `{counts['failed']}` |",
        f"| Stages skipped | `{counts['skipped']}` |",
        f"| Stages cancelled | `{counts['cancelled']}` |",
        f"| First non-passing stage | `{first_nonpassing_stage(outcomes)}` |",
        "",
        "| Connector-local stage | Actual outcome |",
        "| --- | --- |",
    ]
    rows.extend(
        f"| {label} | `{outcomes[stage]}` |"
        for stage, label, _environment_name in STAGES
    )
    rows.extend(
        (
            "",
            "| Real runtime assertion bundle | Outcome |",
            "| --- | --- |",
            "| MRTS inventory/plan, host start, control/detection/bypass, no-CRS, cleanup | "
            f"`{runtime_bundle_outcome(outcomes['runtime'])}` |",
            "",
            "The table reports observed GitHub step outcomes only. It does not read raw "
            "runtime evidence, and a missing or failed runtime target is never promoted to "
            "a connector capability pass.",
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
