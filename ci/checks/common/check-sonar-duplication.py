#!/usr/bin/env python3
"""Require exact-head Sonar success and zero new-code duplication.

The existing Checks client owns GitHub credentials. Fixed-origin public Sonar
readback is unauthenticated, bounded and redirect-free. No scanner exclusions.
"""
from __future__ import annotations

from decimal import Decimal
import json
import os
from pathlib import Path
import re
import runpy
import sys
import urllib.error
import urllib.parse
import urllib.request

GATE = runpy.run_path(str(Path(__file__).with_name("check-sonar-zero.py")))
GateError = GATE["GateError"]
PROJECT = "Easton97-Jens_ModSecurity-conector"
METRICS = ("new_duplicated_lines", "new_duplicated_blocks", "new_duplicated_lines_density")


def summary_density(summary: str) -> Decimal:
    matches = re.findall(r"\b(\d+(?:\.\d+)?)%\s+Duplication on New Code\b", summary, re.ASCII)
    if len(matches) != 1:
        raise GateError("missing or ambiguous Sonar new-code duplication density")
    return Decimal(matches[0])


def measure_value(measure: dict) -> Decimal:
    """Accept either current period or legacy periods, never ambiguous values."""
    candidates = []
    if "value" in measure:
        candidates.append(measure["value"])
    if "period" in measure:
        period = measure["period"]
        candidates.append(period.get("value") if isinstance(period, dict) else None)
    if "periods" in measure:
        periods = measure["periods"]
        if not isinstance(periods, list) or len(periods) != 1 or not isinstance(periods[0], dict):
            raise GateError("ambiguous Sonar new-code periods")
        candidates.append(periods[0].get("value"))
    if len(candidates) != 1:
        raise GateError("missing or ambiguous Sonar measure value")
    raw = candidates[0]
    if not isinstance(raw, str) or re.fullmatch(r"\d+(?:\.\d+)?", raw, re.ASCII) is None:
        raise GateError("invalid Sonar numeric measure")
    return Decimal(raw)


def metric_values(component: dict) -> dict:
    if not isinstance(component, dict) or not isinstance(component.get("measures"), list):
        raise GateError("missing Sonar duplication measures")
    result = {}
    for measure in component["measures"]:
        if not isinstance(measure, dict) or measure.get("metric") not in METRICS:
            continue
        key = measure["metric"]
        if key in result:
            raise GateError("duplicate Sonar duplication measure")
        result[key] = measure_value(measure)
    if set(result) != set(METRICS):
        raise GateError("incomplete Sonar duplication measures; absent values are not zero")
    return result


def sonar_get(endpoint: str, parameters: dict):
    if endpoint not in {"measures/component", "measures/component_tree", "duplications/show"}:
        raise GateError("unsupported Sonar readback endpoint")
    url = "https://sonarcloud.io/api/" + endpoint + "?" + urllib.parse.urlencode(parameters)
    opener = urllib.request.build_opener(GATE["RejectRedirects"]())
    try:
        with opener.open(urllib.request.Request(url, headers={"Accept": "application/json"}), timeout=15) as response:
            data = response.read(GATE["MAX_RESPONSE_BYTES"] + 1)
        if len(data) > GATE["MAX_RESPONSE_BYTES"]:
            raise GateError("Sonar readback exceeds the bounded response limit")
        payload = json.loads(data)
        if not isinstance(payload, dict):
            raise GateError("Sonar readback must be an object")
        return payload
    except (urllib.error.URLError, ValueError) as error:
        raise GateError("public Sonar duplication readback unavailable") from error


def report_component(component: dict, pr: str, fetch) -> None:
    measures = component.get("measures", [])
    positive = any(isinstance(item, dict) and item.get("metric") == "new_duplicated_lines"
                   and measure_value(item) > 0 for item in measures)
    if positive:
        print("sonar duplicate file: " + json.dumps({
            "key": component.get("key"), "path": component.get("path"), "measures": measures,
        }, ensure_ascii=True))
        detail = fetch("duplications/show", {"key": component["key"], "pullRequest": pr})
        print("sonar duplicate blocks: " + json.dumps(detail, ensure_ascii=True)[:16000])


def report_duplicate_files(pr: str, fetch=sonar_get) -> None:
    seen = 0
    for page in range(1, 21):
        payload = fetch("measures/component_tree", {
            "component": PROJECT, "pullRequest": pr, "metricKeys": ",".join(METRICS),
            "qualifiers": "FIL", "strategy": "leaves", "ps": 500, "p": page,
        })
        components = payload.get("components", [])
        total = payload.get("paging", {}).get("total")
        if not isinstance(components, list) or type(total) is not int or total < 0:
            raise GateError("invalid duplication file inventory")
        for component in components:
            report_component(component, pr, fetch)
        seen += len(components)
        if seen >= total:
            return
        if not components:
            break
    raise GateError("duplication inventory exceeds the bounded page limit or is incomplete")


def current_head(repository: str, pr: str, fetch) -> str:
    payload = fetch(f"repos/{repository}/pulls/{pr}")
    if not isinstance(payload, dict) or not isinstance(payload.get("head"), dict):
        raise GateError("invalid current PR head response")
    return payload["head"].get("sha", "")


def verify_duplication(repository: str, head: str, pr: str, fetch, read_sonar=sonar_get) -> dict:
    if re.fullmatch(r"[1-9]\d*", pr, re.ASCII) is None:
        raise GateError("a numeric PR number is required")
    evidence = GATE["verify"](repository, head, fetch)
    if current_head(repository, pr, fetch) != head:
        raise GateError("PR head changed before duplication readback")
    check = fetch(f"repos/{repository}/check-runs/{evidence['check_id']}")
    if check.get("head_sha") != head or check.get("status") != "completed" or check.get("conclusion") != "success":
        raise GateError("Sonar duplication summary is not the completed exact-head analysis")
    density = summary_density(check.get("output", {}).get("summary", ""))
    payload = read_sonar("measures/component", {
        "component": PROJECT, "pullRequest": pr, "metricKeys": ",".join(METRICS),
    })
    values = metric_values(payload.get("component"))
    if current_head(repository, pr, fetch) != head:
        raise GateError("PR head changed during duplication readback")
    result = {"head_sha": head, "check_id": evidence["check_id"],
              "summary_density": str(density), **{key: str(value) for key, value in values.items()}}
    print("sonar duplication evidence: " + json.dumps(result, sort_keys=True))
    if density != 0 or any(value != 0 for value in values.values()):
        report_duplicate_files(pr, read_sonar)
        raise GateError("Sonar requires zero new duplicated lines, blocks and density")
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
