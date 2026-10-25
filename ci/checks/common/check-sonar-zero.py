#!/usr/bin/env python3
"""Require bounded structured Sonar evidence for the current exact PR head."""
from __future__ import annotations

from decimal import Decimal
from datetime import datetime
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

API_ROOT = "https://api.github.com/"
SONAR_ROOT = "https://sonarcloud.io/api/"
PROJECT = "Easton97-Jens_ModSecurity-conector"
CHECK_NAME = "SonarCloud Code Analysis"
MAX_RESPONSE_BYTES = 1048576
# CI analysis includes the pinned SDK build and actual selected coverage before
# upload. Wait for that bounded producer; a pending/stale result never passes.
MAX_ATTEMPTS = 240
PAGE_SIZE = 100
MAX_PAGES = 20
DUPLICATION_METRICS = ("new_duplicated_lines", "new_duplicated_blocks", "new_duplicated_lines_density")
COUNT_METRICS = ("new_violations", "new_accepted_issues", "new_security_hotspots")
RATING_METRICS = ("security_rating", "new_security_rating")
METRICS = COUNT_METRICS + RATING_METRICS + DUPLICATION_METRICS
ISSUES_ENDPOINT = "issues/search"
SONAR_ENDPOINTS = frozenset({"project_pull_requests/list", "qualitygates/project_status",
                            "measures/component", ISSUES_ENDPOINT,
                            "measures/component_tree", "duplications/show"})


class GateError(RuntimeError):
    """A finding or missing/invalid evidence prevents the strict-zero claim."""


class RejectRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise GateError("redirected evidence response rejected")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise GateError("duplicate JSON evidence field")
        result[key] = value
    return result


def read_json(request):
    opener = urllib.request.build_opener(RejectRedirects())
    try:
        with opener.open(request, timeout=15) as response:
            data = response.read(MAX_RESPONSE_BYTES + 1)
        if len(data) > MAX_RESPONSE_BYTES:
            raise GateError("evidence response exceeds the bounded limit")
        return json.loads(data, object_pairs_hook=unique_object)
    except (OSError, ValueError) as error:
        # Never print request objects, headers, bodies or credentials.
        raise GateError("official evidence could not be read") from error


def api_get(path: str, token: str):
    if not path.startswith("repos/") or ".." in path or "\n" in path:
        raise GateError("invalid repository-scoped API path")
    return read_json(urllib.request.Request(API_ROOT + path, headers={
        "Accept": "application/vnd.github+json", "Authorization": "Bearer " + token,
        "X-GitHub-Api-Version": "2022-11-28"}))


def sonar_get(endpoint: str, parameters: dict):
    if endpoint not in SONAR_ENDPOINTS:
        raise GateError("unsupported Sonar readback endpoint")
    url = SONAR_ROOT + endpoint + "?" + urllib.parse.urlencode(parameters)
    payload = read_json(urllib.request.Request(url, headers={"Accept": "application/json"}))
    if not isinstance(payload, dict):
        raise GateError("Sonar readback must be an object")
    return payload


def validate_identity(repository: str, head: str) -> None:
    if (".." in repository or
            re.fullmatch(r"[A-Za-z0-9][\w.-]*/\w[\w.-]*", repository, flags=re.ASCII) is None):
        raise GateError("invalid repository identity")
    if re.fullmatch(r"[0-9a-f]{40}", head) is None:
        raise GateError("a full pull-request head SHA is required")


def validate_pr(pr):
    if not isinstance(pr, str) or re.fullmatch(r"[1-9]\d*", pr, re.ASCII) is None:
        raise GateError("a numeric PR number is required")


def current_head(repository, pr, fetch):
    payload = fetch(f"repos/{repository}/pulls/{pr}")
    if (not isinstance(payload, dict) or type(payload.get("number")) is not int or payload.get("number") != int(pr) or
            not isinstance(payload.get("head"), dict)):
        raise GateError("invalid current PR identity")
    return payload["head"].get("sha")


def select_check(payload: dict, head: str):
    if not isinstance(payload, dict) or not isinstance(payload.get("check_runs"), list):
        raise GateError("invalid GitHub Checks inventory")
    candidates = [check for check in payload["check_runs"]
                  if isinstance(check, dict) and check.get("head_sha") == head
                  and check.get("name") == CHECK_NAME and isinstance(check.get("app"), dict)
                  and check["app"].get("slug") == "sonarqubecloud" and type(check.get("id")) is int]
    return max(candidates, key=lambda check: check["id"], default=None)


def add_unique(batch, seen, key):
    for item in batch:
        identity = item.get(key) if isinstance(item, dict) else None
        valid = type(identity) is int and identity > 0 if key == "id" else isinstance(identity, str) and bool(identity)
        if not valid or identity in seen:
            raise GateError("invalid or duplicate paginated evidence identity")
        seen.add(identity)


def page_total(value):
    if type(value) is not int or not 0 <= value <= PAGE_SIZE * MAX_PAGES:
        raise GateError("invalid or excessive evidence count")
    return value


def check_inventory(repository, head, fetch):
    rows, seen, total = [], set(), None
    prefix = f"repos/{repository}/commits/{head}/check-runs?check_name=SonarCloud%20Code%20Analysis&per_page={PAGE_SIZE}"
    for page in range(1, MAX_PAGES + 1):
        payload = fetch(prefix + f"&page={page}")
        if not isinstance(payload, dict) or not isinstance(payload.get("check_runs"), list):
            raise GateError("invalid GitHub Checks inventory")
        current = page_total(payload.get("total_count"))
        if total is not None and current != total:
            raise GateError("GitHub Checks inventory changed during pagination")
        total = current
        batch = payload["check_runs"]
        if len(batch) != min(PAGE_SIZE, total-len(rows)):
            raise GateError("partial GitHub Checks inventory")
        add_unique(batch, seen, "id")
        rows.extend(batch)
        if len(rows) == total:
            return {"check_runs": rows}
    raise GateError("incomplete GitHub Checks inventory")


def completed_provider(repository, head, fetch, sleep, attempts):
    for attempt in range(attempts):
        check = select_check(check_inventory(repository, head, fetch), head)
        if check is not None and check.get("status") == "completed":
            return check
        if attempt + 1 < attempts:
            sleep(10)
    raise GateError("no completed Sonar analysis for the exact PR head")


def annotation_inventory(repository, check, fetch):
    output = check.get("output")
    if not isinstance(output, dict):
        raise GateError("missing Sonar provider output")
    total = page_total(output.get("annotations_count"))
    rows = []
    for page in range(1, MAX_PAGES + 1):
        batch = fetch(f"repos/{repository}/check-runs/{check['id']}/annotations?per_page={PAGE_SIZE}&page={page}")
        if not isinstance(batch, list) or len(batch) != min(PAGE_SIZE, total-len(rows)):
            raise GateError("partial or inconsistent Sonar annotations")
        if any(not isinstance(item, dict) for item in batch):
            raise GateError("invalid Sonar annotation")
        rows.extend(batch)
        if len(rows) == total:
            return rows
    raise GateError("incomplete Sonar annotations")


def report_findings(repository: str, check_id: int, fetch) -> None:
    """Bound diagnostic text independently of qualification inventories."""
    annotations = fetch(f"repos/{repository}/check-runs/{check_id}/annotations?per_page=20")
    if not isinstance(annotations, list):
        raise GateError("invalid Sonar annotations")
    for annotation in annotations[:20]:
        if not isinstance(annotation, dict):
            raise GateError("invalid Sonar annotation")
        safe = {key: str(annotation.get(key, ""))[:500]
                for key in ("path", "start_line", "title", "message")}
        print("sonar finding: " + json.dumps(safe, ensure_ascii=True))


def analysis_date(row):
    value = row.get("analysisDate")
    if not isinstance(value, str) or len(value) > 128:
        raise GateError("missing or invalid Sonar analysis date")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as error:
        raise GateError("missing or invalid Sonar analysis date") from error
    if parsed.tzinfo is None:
        raise GateError("Sonar analysis date must include its timezone")
    return value


def analysis_identity(pr, head, read_sonar):
    rows = read_sonar("project_pull_requests/list", {"project": PROJECT}).get("pullRequests")
    if not isinstance(rows, list):
        raise GateError("missing Sonar PR analysis inventory")
    matches = [row for row in rows if isinstance(row, dict) and row.get("key") == pr]
    if len(matches) != 1:
        raise GateError("missing or ambiguous Sonar PR analysis")
    row = matches[0]
    if not isinstance(row.get("commit"), dict) or row["commit"].get("sha") != head:
        raise GateError("Sonar PR analysis is stale or lacks commit identity")
    if not isinstance(row.get("status"), dict) or row["status"].get("qualityGateStatus") not in ("OK", "ERROR", "WARN"):
        raise GateError("Sonar PR Quality Gate status is missing or invalid")
    return {"commit": head, "analysis_date": analysis_date(row), "quality_gate": row["status"]["qualityGateStatus"]}


def quality_gate(pr, read_sonar):
    value = read_sonar("qualitygates/project_status", {"projectKey": PROJECT, "pullRequest": pr}).get("projectStatus")
    if not isinstance(value, dict) or value.get("status") not in ("OK", "ERROR", "WARN") or type(value.get("ignoredConditions")) is not bool:
        raise GateError("Sonar structured Quality Gate status/conditions are missing")
    conditions = value.get("conditions")
    if not isinstance(conditions, list) or any(not isinstance(row, dict) or row.get("status") not in ("OK", "ERROR", "WARN") for row in conditions):
        raise GateError("missing or inconsistent Sonar gate conditions")
    return value


def measure_value(measure: dict) -> Decimal:
    """Accept one explicit value/period only; never round or assume zero."""
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


def metric_values(component, required=METRICS):
    if not isinstance(component, dict) or not isinstance(component.get("measures"), list):
        raise GateError("missing Sonar measures")
    result = {}
    for measure in component["measures"]:
        if not isinstance(measure, dict) or measure.get("metric") not in required:
            raise GateError("unexpected Sonar measure")
        key = measure["metric"]
        if key in result:
            raise GateError("duplicate Sonar measure")
        result[key] = measure_value(measure)
    if set(result) != set(required):
        raise GateError("incomplete Sonar measures; absent values are not zero")
    return result


def read_measures(pr, read_sonar):
    component = read_sonar("measures/component", {
        "component": PROJECT, "pullRequest": pr, "metricKeys": ",".join(METRICS)}).get("component")
    if not isinstance(component, dict) or component.get("key") != PROJECT or component.get("pullRequest") != pr:
        raise GateError("Sonar measures lack explicit project/PR identity")
    return metric_values(component)


def sonar_page(payload, field, page, previous_total):
    paging = payload.get("paging")
    if (not isinstance(paging, dict) or type(paging.get("pageIndex")) is not int or
            type(paging.get("pageSize")) is not int or paging.get("pageIndex") != page or paging.get("pageSize") != PAGE_SIZE):
        raise GateError("missing or inconsistent Sonar pagination")
    total = page_total(paging.get("total"))
    if (previous_total is not None and total != previous_total) or ("total" in payload and page_total(payload["total"]) != total):
        raise GateError("Sonar inventory count changed or disagrees")
    batch = payload.get(field)
    if not isinstance(batch, list):
        raise GateError("missing Sonar inventory page")
    return total, batch


def sonar_inventory(pr, endpoint, parameters, field, read_sonar):
    rows, seen, total = [], set(), None
    for page in range(1, MAX_PAGES + 1):
        payload = read_sonar(endpoint, {**parameters, "pullRequest": pr,
                                       "sinceLeakPeriod": "true", "ps": PAGE_SIZE, "p": page})
        total, batch = sonar_page(payload, field, page, total)
        if len(batch) != min(PAGE_SIZE, total-len(rows)):
            raise GateError("partial Sonar inventory page")
        add_unique(batch, seen, "key")
        for row in batch:
            if row.get("project") != PROJECT or row.get("pullRequest", pr) != pr:
                raise GateError("Sonar finding has foreign project/PR identity")
        rows.extend(batch)
        if len(rows) == total:
            return rows
    raise GateError("incomplete Sonar inventory")


def finding_inventories(pr, values, read_sonar):
    active = sonar_inventory(pr, ISSUES_ENDPOINT, {"componentKeys": PROJECT, "issueStatuses": "OPEN,CONFIRMED"}, "issues", read_sonar)
    accepted = sonar_inventory(pr, ISSUES_ENDPOINT, {"componentKeys": PROJECT, "issueStatuses": "ACCEPTED"}, "issues", read_sonar)
    # Cloud's published hotspots/search contract does not advertise PR scope.
    # Its main-branch inventory cannot reconcile a PR. The mandatory explicit
    # PR-component new_security_hotspots measure supplies the whole zero count.
    counts = {"new_violations": len(active), "new_accepted_issues": len(accepted)}
    if any(values[key] != count for key, count in counts.items()):
        raise GateError("Sonar measures and complete finding inventories disagree")
    print("sonar inventory: " + json.dumps({"active": [row["key"] for row in active],
          "accepted": [row["key"] for row in accepted],
          "new_security_hotspots": str(values["new_security_hotspots"]),
          "hotspot_source": "explicit PR-component measure; no unscoped search"}, ensure_ascii=True))
    return counts


def report_duplicate_files(pr, read_sonar):
    rows, seen, total = [], set(), None
    for page in range(1, MAX_PAGES + 1):
        payload = read_sonar("measures/component_tree", {
            "component": PROJECT, "pullRequest": pr, "metricKeys": ",".join(DUPLICATION_METRICS),
            "qualifiers": "FIL", "strategy": "leaves", "metricSort": "new_duplicated_lines",
            "metricSortFilter": "withMeasuresOnly", "ps": PAGE_SIZE, "p": page})
        total, batch = sonar_page(payload, "components", page, total)
        if len(batch) != min(PAGE_SIZE, total-len(rows)):
            raise GateError("partial duplication file inventory")
        add_unique(batch, seen, "key")
        rows.extend(batch)
        if len(rows) == total:
            break
    else:
        raise GateError("incomplete duplication file inventory")
    for row in rows:
        report_duplicate_component(row, pr, read_sonar)


def report_duplicate_component(row, pr, read_sonar):
    if not isinstance(row.get("key"), str) or not row["key"].startswith(PROJECT + ":"):
        raise GateError("foreign duplication component")
    measures = row.get("measures")
    if not isinstance(measures, list):
        raise GateError("missing duplication file measures")
    matches = [item for item in measures if isinstance(item, dict) and item.get("metric") == "new_duplicated_lines"]
    if len(matches) != 1:
        raise GateError("missing or ambiguous duplicate-file line count")
    if measure_value(matches[0]) > 0:
        print("sonar duplicate file: " + json.dumps(row, ensure_ascii=True)[:16000])
        detail = read_sonar("duplications/show", {"key": row["key"], "pullRequest": pr})
        if not isinstance(detail.get("duplications"), list) or not isinstance(detail.get("files"), dict):
            raise GateError("incomplete duplicate block evidence")
        print("sonar duplicate blocks: " + json.dumps(detail, ensure_ascii=True)[:16000])


def require_zero(values, annotations):
    if annotations or any(values[key] != 0 for key in COUNT_METRICS + DUPLICATION_METRICS):
        raise GateError("Sonar requires zero new issues, accepted issues, hotspots, annotations and duplication")
    if any(values[key] != 1 for key in RATING_METRICS):
        raise GateError("Sonar Security Rating must be A")


def verify(repository: str, head: str, fetch, sleep=time.sleep, attempts: int = MAX_ATTEMPTS,
           *, pr=None, read_sonar=sonar_get) -> dict:
    validate_identity(repository, head)
    validate_pr(pr)
    if not 1 <= attempts <= MAX_ATTEMPTS:
        raise GateError("invalid bounded polling limit")
    if current_head(repository, pr, fetch) != head:
        raise GateError("PR head changed before structured readback")
    check = completed_provider(repository, head, fetch, sleep, attempts)
    annotations = annotation_inventory(repository, check, fetch)
    analysis = analysis_identity(pr, head, read_sonar)
    gate = quality_gate(pr, read_sonar)
    values = read_measures(pr, read_sonar)
    finding_inventories(pr, values, read_sonar)
    if any(values[key] > 0 for key in DUPLICATION_METRICS):
        report_duplicate_files(pr, read_sonar)
    if analysis_identity(pr, head, read_sonar) != analysis:
        raise GateError("Sonar analysis changed during structured readback")
    final = completed_provider(repository, head, fetch, sleep, 1)
    if any(final.get(key) != check.get(key) for key in ("id", "output", "conclusion")):
        raise GateError("Sonar provider changed during structured readback")
    if current_head(repository, pr, fetch) != head:
        raise GateError("PR head changed during structured readback")
    evidence = {"head_sha": head, "pr": pr, "check_id": check["id"], **analysis,
                "provider_conclusion": check.get("conclusion"), "annotations": len(annotations),
                **{key: str(value) for key, value in values.items()}}
    print("sonar evidence: " + json.dumps(evidence, sort_keys=True))
    require_zero(values, annotations)
    if (check.get("conclusion") != "success" or analysis["quality_gate"] != "OK" or
            gate["status"] != "OK" or gate["ignoredConditions"] or
            any(row["status"] != "OK" for row in gate["conditions"])):
        raise GateError("Sonar provider and Quality Gate must succeed without ignored conditions")
    return evidence


def main() -> int:
    token = os.environ.get("SONAR_CHECK_GITHUB_TOKEN", "")
    if not token:
        print("sonar-zero: GitHub Checks read credential is unavailable", file=sys.stderr)
        return 2
    try:
        verify(os.environ.get("GITHUB_REPOSITORY", ""), os.environ.get("PR_HEAD_SHA", ""),
               lambda path: api_get(path, token), pr=os.environ.get("PR_NUMBER", ""))
    except GateError as error:
        print("sonar-zero: " + str(error), file=sys.stderr)
        return 1
    print("sonar-zero: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
