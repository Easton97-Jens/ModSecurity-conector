#!/usr/bin/env python3
"""Write a bounded GitHub summary of one real CRS/no-MRTS workflow cell.

The report deliberately consumes only fixed GitHub step outcomes.  It does not
parse same-UID writable raw runtime paths, and it never turns a missing runtime
record into a successful connector capability claim.
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
        rendered_outcome as _rendered_outcome,
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
        rendered_outcome as _rendered_outcome,
        require_connector as _require_connector,
        render_profile_summary,
        run_summary,
    )


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
    return _require_connector(value, "CRS/no-MRTS")


def outcomes_from_environment(environment: Mapping[str, str]) -> dict[str, str]:
    return _outcomes_from_environment(environment, STAGES)


def rendered_outcome(connector: str, stage: str, outcome: str) -> str:
    return _rendered_outcome(connector, stage, outcome, SECURITY_SKIPPED_STAGE)


def outcome_counts(connector: str, outcomes: Mapping[str, str]) -> dict[str, int]:
    return _outcome_counts(connector, outcomes, STAGES, SECURITY_SKIPPED_STAGE)


def first_nonpassing_stage(connector: str, outcomes: Mapping[str, str]) -> str:
    return _first_nonpassing_stage(connector, outcomes, STAGES, SECURITY_SKIPPED_STAGE)


def render_summary(connector: str, outcomes: Mapping[str, str]) -> str:
    connector = require_connector(connector)
    return render_profile_summary(
        connector,
        outcomes,
        STAGES,
        profile_title="CRS/no-MRTS runtime overview",
        stage_heading="Stage",
        runtime_label="Config/load, start, allow request, CRS block/rule, bypass, no-MRTS, cleanup",
        note=(
            "The table reports observed GitHub step outcomes only. A missing or failed runtime "
            "target is never promoted to a connector capability pass. HAProxy evidence publication "
            "is shown separately when skipped by the existing same-UID artifact-security policy."
        ),
        security_skipped_stage=SECURITY_SKIPPED_STAGE,
    )


def main(arguments: Sequence[str] | None = None) -> int:
    return run_summary(arguments, stages=STAGES, render_summary=render_summary)


if __name__ == "__main__":
    raise SystemExit(main())
