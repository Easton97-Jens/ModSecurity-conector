#!/usr/bin/env python3
"""Require the shared exact-PR structured proof and three zero duplication metrics."""
from __future__ import annotations

import json
import os
from pathlib import Path
import runpy
import sys

GATE = runpy.run_path(str(Path(__file__).with_name("check-sonar-zero.py")))
GateError = GATE["GateError"]
PROJECT = GATE["PROJECT"]
METRICS = GATE["DUPLICATION_METRICS"]
measure_value = GATE["measure_value"]
sonar_get = GATE["sonar_get"]


def metric_values(component: dict) -> dict:
    return GATE["metric_values"](component, METRICS)


def verify_duplication(repository: str, head: str, pr: str, fetch, read_sonar=sonar_get) -> dict:
    # One owner proves provider/head/analysis freshness, complete finding counts,
    # strict Quality Gate/security and all three exact duplication measures.
    evidence = GATE["verify"](repository, head, fetch, pr=pr, read_sonar=read_sonar)
    result = {"head_sha": head, "check_id": evidence["check_id"],
              **{key: evidence[key] for key in METRICS}}
    print("sonar duplication evidence: " + json.dumps(result, sort_keys=True))
    return result


def main() -> int:
    token = os.environ.get("SONAR_CHECK_GITHUB_TOKEN", "")
    if not token:
        print("sonar-duplication: Checks credential unavailable", file=sys.stderr)
        return 2
    try:
        verify_duplication(os.environ.get("GITHUB_REPOSITORY", ""),
                           os.environ.get("PR_HEAD_SHA", ""), os.environ.get("PR_NUMBER", ""),
                           lambda path: GATE["api_get"](path, token))
    except GateError as error:
        print("sonar-duplication: " + str(error), file=sys.stderr)
        return 1
    print("sonar-duplication: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
