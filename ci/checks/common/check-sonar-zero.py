#!/usr/bin/env python3
"""Require explicit zero-finding Sonar evidence for the exact pull-request head.

Read-only GitHub Checks access; no scanner exclusions, issue acceptance, token
output, dynamic API hosts, or inference of success from missing evidence.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

API_ROOT = "https://api.github.com/"
CHECK_NAME = "SonarCloud Code Analysis"
MAX_RESPONSE_BYTES = 1048576
MAX_ATTEMPTS = 30


class GateError(RuntimeError):
    """A finding or missing/invalid evidence prevents the zero-finding claim."""


class RejectRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise GateError("redirected GitHub Checks response rejected")


def api_get(path: str, token: str):
    if not path.startswith("repos/") or ".." in path or "\n" in path:
        raise GateError("invalid repository-scoped API path")
    request = urllib.request.Request(
        API_ROOT + path,
        headers={"Accept": "application/vnd.github+json",
                 "Authorization": "Bearer " + token,
                 "X-GitHub-Api-Version": "2022-11-28"},
    )
    opener = urllib.request.build_opener(RejectRedirects())
    try:
        with opener.open(request, timeout=15) as response:
            data = response.read(MAX_RESPONSE_BYTES + 1)
        if len(data) > MAX_RESPONSE_BYTES:
            raise GateError("GitHub Checks response exceeds the bounded limit")
        return json.loads(data)
    except (urllib.error.URLError, ValueError) as error:
        # Never print request objects, headers, response bodies, or credentials.
        raise GateError("GitHub Checks evidence could not be read") from error


def validate_identity(repository: str, head: str) -> None:
    if (".." in repository or
            re.fullmatch(r"[A-Za-z0-9][\w.-]*/\w[\w.-]*", repository, flags=re.ASCII) is None):
        raise GateError("invalid repository identity")
    if re.fullmatch(r"[0-9a-f]{40}", head) is None:
        raise GateError("a full pull-request head SHA is required")


def select_check(payload: dict, head: str):
    if not isinstance(payload, dict) or not isinstance(payload.get("check_runs"), list):
        raise GateError("invalid GitHub Checks inventory")
    candidates = [check for check in payload["check_runs"]
                  if isinstance(check, dict)
                  and check.get("head_sha") == head
                  and check.get("name") == CHECK_NAME
                  and isinstance(check.get("app"), dict)
                  and check["app"].get("slug") == "sonarqubecloud"
                  and type(check.get("id")) is int]
    return max(candidates, key=lambda check: check["id"], default=None)


def finding_count(summary: str, label: str) -> int:
    values = re.findall(r"\b([0-9]+)\s+" + re.escape(label) + r"\b", summary)
    if len(values) != 1:
        raise GateError("missing or ambiguous Sonar finding count: " + label)
    return int(values[0])


def check_counts(check: dict) -> dict:
    output = check.get("output")
    if not isinstance(output, dict) or not isinstance(output.get("summary"), str):
        raise GateError("Sonar summary is missing")
    annotations = output.get("annotations_count")
    if type(annotations) is not int or annotations < 0:
        raise GateError("Sonar annotation count is missing or invalid")
    return {"new_issues": finding_count(output["summary"], "New issues"),
            "new_security_hotspots": finding_count(output["summary"], "Security Hotspots"),
            "annotations": annotations}


def report_findings(repository: str, check_id: int, fetch) -> None:
    annotations = fetch(f"repos/{repository}/check-runs/{check_id}/annotations?per_page=20")
    if not isinstance(annotations, list):
        raise GateError("invalid Sonar annotations")
    for annotation in annotations[:20]:
        if not isinstance(annotation, dict):
            raise GateError("invalid Sonar annotation")
        # JSON escaping and a fixed prefix keep embedded newlines/Actions
        # commands inert. Omit raw_details and all source-code excerpts.
        safe = {key: str(annotation.get(key, ""))[:500]
                for key in ("path", "start_line", "title", "message")}
        print("sonar finding: " + json.dumps(safe, ensure_ascii=True))


def verify(repository: str, head: str, fetch, sleep=time.sleep,
           attempts: int = MAX_ATTEMPTS) -> dict:
    validate_identity(repository, head)
    if not 1 <= attempts <= MAX_ATTEMPTS:
        raise GateError("invalid bounded polling limit")
    path = f"repos/{repository}/commits/{head}/check-runs?check_name=SonarCloud%20Code%20Analysis&per_page=100"
    for attempt in range(attempts):
        check = select_check(fetch(path), head)
        if check is not None and check.get("status") == "completed":
            counts = check_counts(check)
            if counts["annotations"]:
                report_findings(repository, check["id"], fetch)
            evidence = {"head_sha": head, "check_id": check["id"], **counts}
            print("sonar evidence: " + json.dumps(evidence, sort_keys=True))
            if check.get("conclusion") != "success" or any(counts.values()):
                raise GateError("Sonar must succeed with zero new issues, hotspots, and annotations")
            return evidence
        if attempt + 1 < attempts:
            sleep(10)
    raise GateError("no completed Sonar analysis for the exact PR head; zero findings is unverified")


def main() -> int:
    token = os.environ.get("SONAR_CHECK_GITHUB_TOKEN", "")
    if not token:
        print("sonar-zero: GitHub Checks read credential is unavailable", file=sys.stderr)
        return 2
    try:
        verify(os.environ.get("GITHUB_REPOSITORY", ""),
               os.environ.get("PR_HEAD_SHA", ""), lambda path: api_get(path, token))
    except GateError as error:
        print("sonar-zero: " + str(error), file=sys.stderr)
        return 1
    print("sonar-zero: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
