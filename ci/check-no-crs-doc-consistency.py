#!/usr/bin/env python3
"""Check that canonical No-CRS metadata, TODOs, and bilingual reports agree."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONNECTORS = ("apache", "nginx", "haproxy", "envoy", "traefik", "lighttpd")
REPORT_STATUSES = {
    "PASS",
    "FAIL",
    "BLOCKED",
    "UNSUPPORTED",
    "NOT IMPLEMENTED",
    "NOT EXECUTED",
    "IMPLEMENTED, NOT ASSERTED",
}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def read(path: Path, errors: list[str]) -> str:
    if not path.is_file():
        fail(errors, f"missing required document: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def expected_report_state(state: str) -> str:
    if state in {"unsupported_by_host_model", "not_applicable"}:
        return "UNSUPPORTED"
    if state == "not_implemented":
        return "NOT IMPLEMENTED"
    return "IMPLEMENTED, NOT ASSERTED"


def table_statuses(text: str) -> list[str]:
    statuses: list[str] = []
    for line in text.splitlines():
        if not line.startswith("|") or "---" in line:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        statuses.extend(cell for cell in cells if cell in REPORT_STATUSES or cell.isupper())
    return statuses


def main() -> int:
    errors: list[str] = []
    manifests: dict[str, dict[str, object]] = {}
    for connector in CONNECTORS:
        path = ROOT / f"connectors/{connector}/capabilities.json"
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            fail(errors, f"invalid capability manifest {path.relative_to(ROOT)}: {exc}")
            continue
        manifests[connector] = value

        todo = read(ROOT / f"connectors/{connector}/TODO.md", errors)
        for required in (
            "capabilities.json",
            "NOT EXECUTED",
            f"no-crs-baseline-{connector}",
            f"evidence-check-{connector}",
        ):
            if required not in todo:
                fail(errors, f"connectors/{connector}/TODO.md: missing canonical marker {required!r}")

        for suffix, switch in ((".md", "**Language:**"), (".de.md", "**Sprache:**")):
            report_path = ROOT / f"reports/{connector}-no-crs-baseline{suffix}"
            report = read(report_path, errors)
            if switch not in report:
                fail(errors, f"{report_path.relative_to(ROOT)}: missing bilingual language switch")
            status_match = re.search(
                r"(?:Overall canonical status|Kanonischer Gesamtstatus):\s*`([^`]+)`",
                report,
            )
            if not status_match or status_match.group(1) not in REPORT_STATUSES:
                fail(errors, f"{report_path.relative_to(ROOT)}: missing or invalid canonical status")
            static_snapshot = "No canonical No-CRS `result.json` was used" in report or "Kein kanonisches No-CRS-`result.json`" in report
            if static_snapshot and status_match and status_match.group(1) != "NOT EXECUTED":
                fail(errors, f"{report_path.relative_to(ROOT)}: snapshot without result must be NOT EXECUTED")
            if static_snapshot and re.search(r"\|\s*PASS\s*\|", report):
                fail(errors, f"{report_path.relative_to(ROOT)}: PASS cell without canonical result")

        capabilities = value.get("capabilities", {})
        if isinstance(capabilities, dict):
            english = read(ROOT / f"reports/{connector}-no-crs-baseline.md", errors)
            phase_map = {
                "phase1": "Phase 1",
                "phase2": "Phase 2",
                "phase3": "Phase 3",
                "phase4": "Phase 4",
                "event_jsonl": "Events",
            }
            static_snapshot = "No canonical No-CRS `result.json` was used" in english
            for capability, label in phase_map.items():
                entry = capabilities.get(capability, {})
                state = entry.get("state") if isinstance(entry, dict) else ""
                expected = expected_report_state(str(state))
                pattern = rf"\|\s*{re.escape(label)}\s*\|\s*{re.escape(expected)}\s*\|"
                if static_snapshot and english and not re.search(pattern, english):
                    fail(errors, f"reports/{connector}-no-crs-baseline.md: {label} disagrees with {capability}={state}")

    aggregate_en = read(ROOT / "reports/all-connectors-no-crs-baseline.md", errors)
    aggregate_de = read(ROOT / "reports/all-connectors-no-crs-baseline.de.md", errors)
    for connector in CONNECTORS:
        display = "Apache" if connector == "apache" else "NGINX" if connector == "nginx" else "HAProxy" if connector == "haproxy" else connector
        if not re.search(rf"\|\s*{re.escape(display)}\s*\|", aggregate_en, re.IGNORECASE):
            fail(errors, f"aggregate report is missing {connector}")
    for path, text in (
        ("reports/all-connectors-no-crs-baseline.md", aggregate_en),
        ("reports/all-connectors-no-crs-baseline.de.md", aggregate_de),
    ):
        if not any(status in REPORT_STATUSES for status in table_statuses(text)):
            fail(errors, f"{path}: aggregate table contains no canonical status cells")
        static_snapshot = "No canonical No-CRS `result.json` was used" in text or "Kein kanonisches No-CRS-`result.json`" in text
        if static_snapshot and re.search(r"\|\s*PASS\s*\|", text):
            fail(errors, f"{path}: PASS cell without canonical result")

    envoy_todo = read(ROOT / "connectors/envoy/TODO.md", errors)
    if "Status: targeted `minimal_runtime_smoke`" not in envoy_todo:
        fail(errors, "Envoy TODO must identify the existing targeted minimal runtime path")
    traefik_todo = read(ROOT / "connectors/traefik/TODO.md", errors)
    for marker in ("forwardBody", "request_body_mode=none", "unsupported_by_host_model"):
        if marker not in traefik_todo:
            fail(errors, f"Traefik TODO is missing architecture boundary marker {marker}")
    lighttpd_todo = read(ROOT / "connectors/lighttpd/TODO.md", errors)
    if "`implemented_not_asserted`, not verified" not in lighttpd_todo:
        fail(errors, "lighttpd TODO must keep Phase 3 implemented but unverified")

    overview_en = read(ROOT / "docs/repository-overview.md", errors)
    overview_de = read(ROOT / "docs/repository-overview.de.md", errors)
    for marker in ("Envoy", "Traefik", "lighttpd", "minimal_runtime_smoke", "capabilities.json"):
        if marker not in overview_en or marker not in overview_de:
            fail(errors, f"repository overview pair is missing {marker!r}")

    aggregate_path = ROOT / "reports/testing/generated/canonical/connector-capabilities.generated.json"
    try:
        aggregate = json.loads(aggregate_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(errors, f"invalid generated capability aggregate: {exc}")
    else:
        runtime_promotion = aggregate.get("runtime_promotion")
        if not isinstance(runtime_promotion, bool):
            fail(errors, "generated capability aggregate runtime_promotion must be Boolean")
        if runtime_promotion is True:
            runtime_evidence = aggregate.get("runtime_evidence")
            if not isinstance(runtime_evidence, dict):
                fail(errors, "runtime-promoted capability aggregate is missing runtime_evidence")
            else:
                if not isinstance(runtime_evidence.get("run_id"), str) or not runtime_evidence["run_id"]:
                    fail(errors, "runtime-promoted capability aggregate is missing its run_id")
                if runtime_evidence.get("evidence_stage") != "no_crs_baseline":
                    fail(errors, "runtime-promoted capability aggregate must use no_crs_baseline evidence")
                evidence_connectors = runtime_evidence.get("connectors")
                if not isinstance(evidence_connectors, dict) or set(evidence_connectors) != set(CONNECTORS):
                    fail(errors, "runtime-promoted capability aggregate lacks one or more connector results")
        elif runtime_promotion is not False:
            fail(errors, "generated capability aggregate has an invalid runtime_promotion value")
        generated_connectors = aggregate.get("connectors")
        if not isinstance(generated_connectors, dict) or set(generated_connectors) != set(CONNECTORS):
            fail(errors, "generated capability aggregate does not contain exactly six connectors")

    if errors:
        for error in errors:
            print(f"no-crs-doc-consistency: FAIL: {error}")
        return 1
    print("no-crs-doc-consistency: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
