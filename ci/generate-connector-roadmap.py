#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from generated_report_utils import GENERATED_REPORTS, build_metadata, generated_json_text, generated_markdown_text

REPORT_KEY = "connector_roadmap"
GENERATOR = "ci/generate-connector-roadmap.py"
MAKE_TARGET = "refresh-connector-reports"

CONNECTORS = ["apache", "nginx", "haproxy", "envoy", "lighttpd", "traefik", "litespeed", "openresty"]
PRODUCTION = {"apache", "nginx", "haproxy"}
PARTIAL = {"envoy", "lighttpd", "traefik"}

CAPABILITY_NOTES: dict[str, list[str]] = {
    "apache": ["production verified runtime connector", "framework runtime and full-matrix evidence present"],
    "nginx": ["production verified runtime connector", "OpenResty is initially covered as an nginx runtime variant"],
    "haproxy": ["production verified runtime connector", "SPOE-sidecar integration path is documented"],
    "envoy": [
        "partial bridge starter only; no runtime-verified Envoy adapter",
        "most realistic proof path is ext_proc or ext_authz sidecar before considering native/WASM work",
        "request/response body coverage depends on Envoy buffering/streaming mode limits",
    ],
    "lighttpd": [
        "partial bridge starter only; no native lighttpd module, FastCGI, or SCGI bridge",
        "blocking is plausible only after a selected hook/proxy architecture is proven",
    ],
    "traefik": [
        "partial decision-service starter only; no Go plugin/middleware or runtime harness",
        "direct libmodsecurity embedding is not proven; reverse-proxy/decision-service harness is lower-risk",
    ],
    "litespeed": [
        "planned candidate; no repository directory yet",
        "OpenLiteSpeed/LiteSpeed ModSecurity compatibility needs license/download/automation proof before implementation",
    ],
    "openresty": ["covered_by_nginx", "do not create a separate connector at this stage"],
}

TECHNICAL_FEASIBILITY: dict[str, dict[str, str]] = {
    "envoy": {
        "integration": "realistic via ext_proc gRPC sidecar or ext_authz decision service; WASM/Lua are possible but not currently represented in the repo",
        "blocking": "realistic for request blocking with ext_authz/ext_proc; response-body disruptive semantics require explicit filter-mode proof",
        "phases": "request headers/body and response headers/body are conceptually mappable through Envoy HTTP filters, subject to configured processing modes",
        "limits": "body coverage is governed by Envoy buffering/streaming settings and partial-body behavior; must be evidenced per case",
    },
    "lighttpd": {
        "integration": "no native ModSecurity adapter is present; needs either a native module study or proxy/sidecar bridge",
        "blocking": "realistic only after the chosen hook can stop forwarding before upstream commit",
        "phases": "request headers/body are more likely first; response phases need separate hook proof",
        "limits": "unknown until module/proxy architecture and buffering behavior are selected",
    },
    "traefik": {
        "integration": "plugin/middleware or forwardAuth-style decision service are the likely paths; direct libmodsecurity integration is not proven",
        "blocking": "request blocking is realistic through middleware/decision service; response-body blocking is higher risk",
        "phases": "request header/body first; response phases require Go middleware/harness evidence",
        "limits": "depends on plugin/middleware body buffering and Yaegi/Go runtime constraints",
    },
    "litespeed": {
        "integration": "OpenLiteSpeed and LiteSpeed Enterprise advertise ModSecurity-compatible rule support, but this repo has no connector or harness",
        "blocking": "plausible if the server's own ModSecurity engine can be driven in CI with CRS fixtures",
        "phases": "must be mapped empirically from server logs/results rather than assumed equivalent to libmodsecurity v3 connectors",
        "limits": "license, package availability, edition differences, and non-libmodsecurity engine compatibility are the main risks",
    },
}

RANKING = [
    {"rank": 1, "connector": "envoy", "difficulty": "high", "risk": "medium-high", "expected_value": "high", "recommendation": "Next proof: ext_proc/ext_authz sidecar runtime smoke with request blocking and explicit body-mode evidence."},
    {"rank": 2, "connector": "litespeed", "difficulty": "medium", "risk": "high", "expected_value": "medium-high", "recommendation": "Run installation/licensing proof for OpenLiteSpeed first; do not implement until automation is proven."},
    {"rank": 3, "connector": "traefik", "difficulty": "medium-high", "risk": "high", "expected_value": "medium", "recommendation": "Prototype a decision-service/forwardAuth harness before any Go plugin work."},
    {"rank": 4, "connector": "lighttpd", "difficulty": "high", "risk": "high", "expected_value": "medium", "recommendation": "Perform hook/proxy architecture spike before implementation."},
]


def exists(root: Path, rel: str) -> bool:
    return (root / rel).exists()


def has_files(root: Path, rel: str, patterns: tuple[str, ...]) -> bool:
    base = root / rel
    return base.exists() and any(base.glob(pattern) for pattern in patterns)


def connector_row(root: Path, name: str) -> dict[str, Any]:
    directory = exists(root, f"connectors/{name}")
    if name in PRODUCTION:
        status = "production_verified"
    elif name in PARTIAL and directory:
        status = "partial_skeleton"
    elif name == "openresty":
        status = "covered_by_existing_connector"
    elif name == "litespeed":
        status = "planned"
    else:
        status = "unknown"
    build_target = "yes" if exists(root, f"connectors/{name}/Makefile") or exists(root, f"connectors/{name}/Makefile.am") or name == "nginx" and exists(root, "connectors/nginx/config") else "no"
    verified_case = "yes" if name in PRODUCTION and f"verified-{name}-case" in (root / "Makefile").read_text(encoding="utf-8") else "no"
    full_matrix = "yes" if name in PRODUCTION else "no"
    return {
        "connector": name,
        "directory": "yes" if directory else "no",
        "status": status,
        "readme": "yes" if exists(root, f"connectors/{name}/README.md") else "no",
        "build_scripts": "yes" if has_files(root, f"connectors/{name}/build", ("*.sh", "*")) or exists(root, f"connectors/{name}/Makefile") or exists(root, f"connectors/{name}/Makefile.am") or name == "nginx" else "no",
        "runtime_harness": "yes" if has_files(root, f"connectors/{name}/harness", ("*.sh", "*.conf")) else "no",
        "example_config": "yes" if has_files(root, f"connectors/{name}/harness", ("*.conf", "*.example")) or has_files(root, f"connectors/{name}/poc", ("**/*.example", "**/*.cfg")) else "no",
        "modsecurity_integration": "yes" if name in PRODUCTION else "starter_only" if name in PARTIAL else "no",
        "tests": "framework_owned" if name in PRODUCTION or name in PARTIAL else "no",
        "build_target": build_target,
        "make_targets": "yes" if name in {"apache", "nginx", "haproxy", "envoy", "lighttpd", "traefik"} else "no",
        "report_integration": "yes" if name in PRODUCTION else "roadmap_only",
        "full_matrix": full_matrix,
        "verified_case": verified_case,
        "verified_root_runtime_components": "yes" if name in PRODUCTION else "no",
        "capability_notes": CAPABILITY_NOTES.get(name, []),
        "recommendation": recommendation(name, status),
    }


def recommendation(name: str, status: str) -> str:
    if status == "production_verified":
        return "Keep in verified runtime/full-matrix maintenance."
    if name == "envoy":
        return "Recommended next connector: prove ext_proc/ext_authz runtime smoke before implementation expansion."
    if name == "litespeed":
        return "Run OpenLiteSpeed install/licensing/CRS proof before adding connector directory."
    if name == "openresty":
        return "Cover as nginx runtime variant or compatibility smoke only."
    return "Keep as scaffold until architecture and runtime harness proof exist."


def markdown(payload: dict[str, Any]) -> str:
    lines = ["# Connector Roadmap", "", "Roadmap-only generated report. It does not create runtime PASS/FAIL values and does not add full-matrix rows for unimplemented connectors.", ""]
    lines += ["## Connector Status Matrix", "", "| Connector | Directory | Status | Build Target | Verified Case | Full Matrix | Notes |", "|---|---|---|---|---|---|---|"]
    for row in payload["connector_status_matrix"]:
        notes = "; ".join(row["capability_notes"])
        lines.append(f"| {row['connector']} | {row['directory']} | {row['status']} | {row['build_target']} | {row['verified_case']} | {row['full_matrix']} | {notes} |")
    lines += ["", "## Connector Candidate Ranking", "", "| Rank | Connector | Difficulty | Risk | Expected Value | Recommendation |", "|---:|---|---|---|---|---|"]
    for row in payload["connector_candidate_ranking"]:
        lines.append(f"| {row['rank']} | {row['connector']} | {row['difficulty']} | {row['risk']} | {row['expected_value']} | {row['recommendation']} |")
    lines += ["", "## OpenResty Decision", "", "| Field | Value |", "|---|---|", "| Decision | covered_by_nginx |", "| Separate connector | no |", "| Reason | NGINX-based runtime |"]
    lines += ["", "## LiteSpeed Candidate", "", "| Field | Value |", "|---|---|", "| Candidate | LiteSpeed / OpenLiteSpeed |", "| Status | planned |", "| Key risks | license/download automation, edition differences, ModSecurity-engine compatibility, CI installability |", "| Next proof step | OpenLiteSpeed package/container install proof with one CRS blocking fixture and captured evidence |"]
    lines += ["", "## Technical Feasibility", ""]
    for name, data in payload["technical_feasibility"].items():
        lines += [f"### {name}", "", "| Field | Assessment |", "|---|---|"]
        for key, value in data.items():
            lines.append(f"| {key} | {value} |")
        lines.append("")
    lines += ["## Recommended Next Connector", "", payload["recommended_next_connector"]]
    return "\n".join(lines)


def build_payload(root: Path) -> dict[str, Any]:
    rows = [connector_row(root, name) for name in CONNECTORS]
    return {
        "report_scope": "roadmap_only",
        "runtime_values_invented": False,
        "full_matrix_rows_added": False,
        "connector_status_matrix": rows,
        "connector_candidate_ranking": RANKING,
        "openresty_decision": {"decision": "covered_by_nginx", "separate_connector": "no", "reason": "NGINX-based runtime"},
        "litespeed_candidate": {"candidate": "LiteSpeed / OpenLiteSpeed", "status": "planned", "key_risks": ["license/download automation", "edition differences", "ModSecurity-engine compatibility", "CI installability"], "next_proof_step": "OpenLiteSpeed package/container install proof with one CRS blocking fixture and captured evidence"},
        "technical_feasibility": TECHNICAL_FEASIBILITY,
        "recommended_next_connector": "envoy",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector-root", type=Path, default=Path.cwd())
    parser.add_argument("--framework-root", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args()
    root = args.connector_root.resolve()
    output_dir = (args.output_dir or root / "reports/testing/generated/manifest").resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    inputs = ["connectors", "Makefile", "ci", "config", "docs", "reports/testing/generated"]
    payload = build_payload(root)
    metadata = build_metadata(generated_by=GENERATOR, make_target=MAKE_TARGET, connector_root=root, framework_root=args.framework_root, inputs=inputs, report_key=REPORT_KEY, extra={"report_scope": "roadmap_only"})
    json_path = output_dir / GENERATED_REPORTS[REPORT_KEY].filename("json")
    md_path = output_dir / GENERATED_REPORTS[REPORT_KEY].filename("md")
    json_path.write_text(generated_json_text(payload, metadata), encoding="utf-8")
    md_path.write_text(generated_markdown_text(markdown(payload), metadata), encoding="utf-8")
    print("connector-roadmap: wrote roadmap_only report")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
