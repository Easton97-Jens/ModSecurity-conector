#!/usr/bin/env python3
"""Write a bounded GitHub summary for one no-CRS/with-MRTS runtime cell.

The report consumes only fixed GitHub step outcomes. It does not parse raw
runtime files or same-UID writable evidence, and it never promotes a missing
or failed runtime step to a connector capability pass.
"""

from __future__ import annotations

import os
from collections.abc import Mapping, Sequence

try:
    from github_step_summary import (
        append_github_step_summary,
        first_nonpassing_stage as _first_nonpassing_stage,
        outcome_counts as _outcome_counts,
        outcomes_from_environment as _outcomes_from_environment,
        require_connector as _require_connector,
        render_profile_summary,
        run_summary,
    )
except ModuleNotFoundError:
    from ci.runtime.lifecycle.github_step_summary import (
        append_github_step_summary,
        first_nonpassing_stage as _first_nonpassing_stage,
        outcome_counts as _outcome_counts,
        outcomes_from_environment as _outcomes_from_environment,
        require_connector as _require_connector,
        render_profile_summary,
        run_summary,
    )


STAGES = (
    ("checkout", "Checkout exact workflow revision", "CHECKOUT_OUTCOME"),
    ("setup_python", "Locked Python toolchain", "SETUP_PYTHON_OUTCOME"),
    ("setup_go", "Locked Go toolchain", "SETUP_GO_OUTCOME"),
    ("verify_python", "Python interpreter contract", "VERIFY_PYTHON_OUTCOME"),
    ("verify_go", "Go interpreter contract", "VERIFY_GO_OUTCOME"),
    ("snapshot_go", "Verified setup-Go binary provenance", "SNAPSHOT_GO_OUTCOME"),
    ("verify_cell", "Closed no-CRS/with-MRTS cell", "VERIFY_CELL_OUTCOME"),
    ("prepare_runtime", "Connector-isolated runtime preparation", "PREPARE_RUNTIME_OUTCOME"),
    ("runtime", "Real connector MRTS host runtime", "RUNTIME_OUTCOME"),
    ("upload_evidence", "Isolated runtime evidence publication", "UPLOAD_EVIDENCE_OUTCOME"),
)
TARGET_GO_PROVENANCE_STAGE = "snapshot_go"
TARGET_GO_PROVENANCE_NOT_APPLICABLE_CONNECTORS = frozenset(("apache", "haproxy"))


def require_connector(value: str) -> str:
    return _require_connector(value, "no-CRS/with-MRTS")


def outcomes_from_environment(environment: Mapping[str, str]) -> dict[str, str]:
    return _outcomes_from_environment(environment, STAGES)


def _summary_stages(
    connector: str, outcomes: Mapping[str, str]
) -> tuple[tuple[str, str, str], ...]:
    """Exclude only the intentionally absent target-Go snapshot from metrics."""

    if connector not in TARGET_GO_PROVENANCE_NOT_APPLICABLE_CONNECTORS:
        return STAGES
    return tuple(
        stage
        for stage in STAGES
        if not (
            stage[0] == TARGET_GO_PROVENANCE_STAGE
            and outcomes[TARGET_GO_PROVENANCE_STAGE] == "skipped"
        )
    )


def outcome_counts(outcomes: Mapping[str, str], connector: str = "") -> dict[str, int]:
    return _outcome_counts("", outcomes, _summary_stages(connector, outcomes))


def first_nonpassing_stage(outcomes: Mapping[str, str], connector: str = "") -> str:
    return _first_nonpassing_stage("", outcomes, _summary_stages(connector, outcomes))


def render_summary(connector: str, outcomes: Mapping[str, str]) -> str:
    connector = require_connector(connector)
    stages = _summary_stages(connector, outcomes)
    summary = render_profile_summary(
        connector,
        {stage: outcomes[stage] for stage, _label, _environment_name in stages},
        stages,
        profile_title="no-CRS/with-MRTS runtime overview",
        stage_heading="Connector-local stage",
        runtime_label="MRTS inventory/plan, host start, control/detection/bypass, no-CRS, cleanup",
        note=(
            "The table reports observed GitHub step outcomes only. It does not read raw "
            "runtime evidence, and a missing or failed runtime target is never promoted to "
            "a connector capability pass."
        ),
    )
    if (
        connector in TARGET_GO_PROVENANCE_NOT_APPLICABLE_CONNECTORS
        and outcomes[TARGET_GO_PROVENANCE_STAGE] == "skipped"
    ):
        marker = "| Connector-local stage | Actual outcome |\n| --- | --- |\n"
        summary = summary.replace(
            marker,
            marker + "| Verified setup-Go binary provenance | `not_applicable` |\n",
            1,
        )
        summary = summary.replace(
            "a connector capability pass.",
            "a connector capability pass. The target-Go provenance snapshot is intentionally "
            "not applicable to this connector and is excluded from pass/fail metrics.",
            1,
        )
    return summary


def main(arguments: Sequence[str] | None = None) -> int:
    return run_summary(arguments, stages=STAGES, render_summary=render_summary)


if __name__ == "__main__":
    raise SystemExit(main())
