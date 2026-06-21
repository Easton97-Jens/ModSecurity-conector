#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from generated_report_utils import GENERATED_REPORTS, build_metadata, generated_json_text, generated_markdown_text

REPORT_KEY = "connector_roadmap"
GENERATOR = "ci/generate-connector-roadmap.py"
MAKE_TARGET = "refresh-connector-reports"
INPUTS = ("connectors", "Makefile", "ci", "config", "docs", "reports/testing/generated")

CONNECTORS = ("apache", "nginx", "haproxy", "envoy", "lighttpd", "traefik", "litespeed", "openresty")
PRODUCTION = {"apache", "nginx", "haproxy"}
PARTIAL = {"envoy", "lighttpd", "traefik"}

ROADMAP_SCOPE = {
    "report_scope": "roadmap_only",
    "evaluates": "repository structure, existing skeletons, technical feasibility, first proof steps, and evidence gates",
    "does_not_replace": "runtime evidence, verified-case result.json evidence, or full-matrix evidence",
    "full_matrix_results_created": False,
    "runtime_pass_fail_values_created": False,
    "merge_readiness_impact": "none",
}

STATUS_DETAILS: dict[str, dict[str, str]] = {
    "apache": {
        "why": "Existing production connector with verified runtime and full-matrix coverage.",
        "next_step": "Keep in verified runtime/full-matrix maintenance.",
    },
    "nginx": {
        "why": "Existing production connector with verified runtime and full-matrix coverage; OpenResty is NGINX-based.",
        "next_step": "Keep production coverage and optionally add OpenResty compatibility smoke under nginx later.",
    },
    "haproxy": {
        "why": "Existing production connector with verified runtime and full-matrix coverage; SPOE path is documented.",
        "next_step": "Keep production coverage and capability notes current.",
    },
    "envoy": {
        "why": "Repository has an Envoy bridge starter and harness entrypoint, but no runtime-verified Envoy integration yet.",
        "next_step": "Define and run a targeted ext_proc/ext_authz runtime smoke proof; do not start full matrix.",
    },
    "lighttpd": {
        "why": "Repository has a lighttpd bridge starter, but no native module/FastCGI/SCGI runtime integration.",
        "next_step": "Write a request-blocking feasibility note and select native-module versus sidecar/proxy architecture.",
    },
    "traefik": {
        "why": "Repository has a decision-service starter, but no Traefik Go plugin/middleware or runtime harness.",
        "next_step": "Prototype forwardAuth/decision-service feasibility before any Go plugin implementation.",
    },
    "litespeed": {
        "why": "No repository directory exists; LiteSpeed/OpenLiteSpeed is only a candidate until install/licensing proof exists.",
        "next_step": "Run OpenLiteSpeed install/start proof with one CRS/request-blocking smoke if automation allows it.",
    },
    "openresty": {
        "why": "OpenResty is based on the NGINX runtime stack and should not fork connector ownership now.",
        "next_step": "Treat as nginx runtime variant or compatibility smoke only; no separate reports or full matrix.",
    },
}

LIFECYCLE = [
    {
        "stage": "planned",
        "meaning": "Candidate is tracked but no connector directory or selected runtime architecture is required yet.",
        "required_evidence": "Roadmap entry, rationale, risks, and first proof definition.",
        "not_allowed_claims": "No runtime support, no blocking support, no CRS support, no verified-case readiness.",
    },
    {
        "stage": "skeleton",
        "meaning": "Connector directory or starter exists with README/metadata/build notes, but no real runtime proof.",
        "required_evidence": "Repo-owned scaffold, origin notes, build or self-test starter, and explicit non-runtime disclaimer.",
        "not_allowed_claims": "No production readiness, no verified runtime result, no full-matrix eligibility.",
    },
    {
        "stage": "buildable",
        "meaning": "Starter or adapter component compiles from clean checkout with documented command.",
        "required_evidence": "Build command, artifact path outside checkout, source map, and passing syntax/lint checks.",
        "not_allowed_claims": "No traffic handling or ModSecurity semantics unless runtime logs prove them.",
    },
    {
        "stage": "runtime-startable",
        "meaning": "Server/proxy and any sidecar can start locally with minimal configuration.",
        "required_evidence": "Start/stop or run script, minimal config, process logs, port allocation, and cleanup behavior.",
        "not_allowed_claims": "No verified blocking or CRS coverage without a case result and logs.",
    },
    {
        "stage": "verified-case-ready",
        "meaning": "A targeted real runtime case can produce result.json and logs under verified runtime root.",
        "required_evidence": "result.json, case-run JSON/Markdown, access/error logs or equivalent, decision/audit evidence where applicable.",
        "not_allowed_claims": "No full-matrix readiness, no broad phase coverage, no production_verified status.",
    },
    {
        "stage": "full-matrix-candidate",
        "meaning": "Full-matrix jobs are technically schedulable for the connector, but may still fail or be incomplete.",
        "required_evidence": "Matrix job definitions, runtime result producer, report integration, known limitation notes, and governance/lint pass.",
        "not_allowed_claims": "No PASS/Merge Readiness claims until generated full-matrix evidence supports them.",
    },
    {
        "stage": "production-verified",
        "meaning": "Connector passed the complete verified evidence pipeline and is included in production status.",
        "required_evidence": "Verified runtime evidence, full matrix, governance, lint, quick-check, report layout, and merge-readiness PASS.",
        "not_allowed_claims": "Do not claim if any required generated evidence is blocked, stale, or missing.",
    },
    {
        "stage": "covered-by-existing-connector",
        "meaning": "Runtime is intentionally covered as a variant of an existing connector rather than a separate connector.",
        "required_evidence": "Decision record that names owning connector and allowed future compatibility-smoke path.",
        "not_allowed_claims": "No separate full matrix, generated reports, or production connector identity.",
    },
    {
        "stage": "blocked",
        "meaning": "Implementation cannot proceed until an external, licensing, architecture, or evidence blocker is resolved.",
        "required_evidence": "Blocker description, owner/next proof, and what evidence would unblock it.",
        "not_allowed_claims": "No forward status promotion until the blocker is removed and evidenced.",
    },
]

ACCEPTANCE_CRITERIA = [
    ("connectors/<name>/README.md", "yes", "yes", "yes"),
    ("build/start/stop or run script", "build starter allowed", "yes", "yes"),
    ("minimal config", "recommended", "yes", "yes"),
    ("verified-case support", "no", "yes", "yes"),
    ("result.json", "no", "yes", "yes"),
    ("access/error logs or equivalent", "no", "yes", "yes"),
    ("audit evidence if supported", "document support", "yes if supported", "yes if supported"),
    ("decision evidence if applicable", "document support", "yes", "yes"),
    ("capability notes", "yes", "yes", "yes"),
    ("request blocking smoke", "no", "yes", "yes"),
    ("request body smoke or documented not-supported reason", "no", "yes", "yes"),
    ("clean report-governance/lint/quick-check", "yes", "yes", "yes"),
]

ENVOY_OPTIONS = [
    {
        "option": "ext_proc sidecar",
        "description": "Envoy External Processing gRPC service that can inspect configured request/response processing points.",
        "pros": "Best fit for staged request/body/response experiments; external process can own ModSecurity lifecycle and evidence logs.",
        "cons": "Requires protobuf/gRPC service and careful body processing-mode limits; response-body intervention semantics need proof.",
        "proof_difficulty": "medium-high",
        "recommendation": "primary proof path together with a minimal request-blocking case",
        "request_blocking": "yes, if the processor returns a denied/modified response before upstream forwarding",
        "request_body": "possible, subject to Envoy processing mode and buffering settings",
        "response_body": "possible in concept, but not claimed until explicitly evidenced",
        "intervention_status": "map ModSecurity disruptive intervention to Envoy processor response/denied status",
        "evidence": "Envoy logs, processor logs, decision log, result.json, case-run files",
        "ci_testability": "good after pinned Envoy binary/container and deterministic ports",
        "risk": "medium-high",
    },
    {
        "option": "ext_authz service",
        "description": "Envoy authorization service that returns allow/deny before routing to upstream.",
        "pros": "Simple request blocking proof; easy to reason about 403 decisions and logs.",
        "cons": "Primarily authorization-oriented; request body/response body coverage is limited and not a full ModSecurity phase mapping.",
        "proof_difficulty": "medium",
        "recommendation": "acceptable first smoke if ext_proc is too heavy; pair with clear body/response non-goals",
        "request_blocking": "yes",
        "request_body": "limited/config-dependent; do not claim broad request-body support in first proof",
        "response_body": "no practical response-body claim for first proof",
        "intervention_status": "map deny decision to ext_authz denied response status 403",
        "evidence": "Envoy logs, authz service logs, decision log, result.json, case-run files",
        "ci_testability": "good",
        "risk": "medium",
    },
    {
        "option": "WASM filter",
        "description": "Proxy-Wasm HTTP filter embedded in Envoy filter chain.",
        "pros": "Native filter-chain placement and possible phase visibility.",
        "cons": "Higher toolchain complexity; embedding libmodsecurity or a robust bridge is risky; evidence and debugging are harder.",
        "proof_difficulty": "high",
        "recommendation": "defer until sidecar proof confirms required semantics",
        "request_blocking": "possible but not proven",
        "request_body": "possible but SDK/runtime constrained",
        "response_body": "possible but high risk",
        "intervention_status": "filter must translate decisions into local responses/stream actions",
        "evidence": "Envoy logs plus WASM module logs; more complex CI artifacts",
        "ci_testability": "moderate to poor for first proof",
        "risk": "high",
    },
    {
        "option": "Lua filter",
        "description": "Envoy Lua HTTP filter that calls or models an external decision service.",
        "pros": "Fast prototype for header/path decisions.",
        "cons": "Not a strong long-term ModSecurity integration; body and response handling are constrained.",
        "proof_difficulty": "medium",
        "recommendation": "use only as fallback feasibility spike, not preferred connector path",
        "request_blocking": "yes for simple cases",
        "request_body": "limited",
        "response_body": "not a first-proof claim",
        "intervention_status": "Lua script returns local 403 or delegates to sidecar",
        "evidence": "Envoy logs, Lua log messages, sidecar logs if used",
        "ci_testability": "good for a smoke, weak for connector semantics",
        "risk": "medium-high",
    },
    {
        "option": "reverse-proxy chain with existing connector",
        "description": "Envoy fronts an existing verified connector such as nginx or apache.",
        "pros": "Fast compatibility smoke and infrastructure proof.",
        "cons": "Does not prove an Envoy connector; ModSecurity decision belongs to downstream connector.",
        "proof_difficulty": "low-medium",
        "recommendation": "allowed only as infrastructure smoke, not as Envoy connector evidence",
        "request_blocking": "yes, but by the existing connector rather than Envoy",
        "request_body": "covered by existing connector only",
        "response_body": "covered by existing connector only",
        "intervention_status": "downstream connector returns status; Envoy only forwards it",
        "evidence": "Envoy forwarding logs plus existing connector logs",
        "ci_testability": "good",
        "risk": "low for smoke, high if misrepresented",
    },
    {
        "option": "external ModSecurity decision service",
        "description": "Standalone service owns ModSecurity transaction evaluation; Envoy calls it through ext_proc/ext_authz or another control point.",
        "pros": "Clear separation of Envoy harness and ModSecurity lifecycle; reusable for Traefik/lighttpd sidecar studies.",
        "cons": "Protocol mapping and body buffering still must be proven; not a connector by itself.",
        "proof_difficulty": "medium-high",
        "recommendation": "use as shared service behind ext_proc/ext_authz proof",
        "request_blocking": "yes through caller integration",
        "request_body": "depends on caller body delivery",
        "response_body": "depends on caller response delivery",
        "intervention_status": "service returns intervention_status and decision fields consumed by Envoy adapter layer",
        "evidence": "service decision log, ModSecurity audit/decision log, Envoy logs, result.json",
        "ci_testability": "good if implemented as deterministic local process",
        "risk": "medium",
    },
]

ENVOY_PROOF = {
    "name": "Minimal Envoy ext_proc/ext_authz runtime smoke",
    "scope": "targeted proof only; not a full connector and not a full-matrix producer",
    "goals": [
        "Envoy starts locally with a deterministic minimal config.",
        "A simple upstream responds through Envoy.",
        "A ModSecurity-like decision service or sidecar can emit a deny decision.",
        "A case such as action_deny_phase1 or envoy_request_blocking_smoke returns HTTP 403.",
        "Logs and decision evidence are written under the verified runtime root.",
        "No full-matrix integration is added for this proof.",
    ],
    "artifacts": [
        "connectors/envoy/README.md",
        "connectors/envoy/config/envoy.yaml",
        "connectors/envoy/harness/",
        "connectors/envoy/scripts/run-smoke.sh",
        "connectors/envoy/examples/",
    ],
    "runtime_root": "$VERIFIED_RUN_ROOT/envoy-smoke/",
    "evidence": [
        "result.json",
        "envoy access log",
        "envoy error log",
        "decision-service log",
        "modsecurity decision log, if present",
        "case-run.md",
        "case-run.json",
    ],
    "minimal_result_schema": {
        "connector": "envoy",
        "case": "envoy_request_blocking_smoke",
        "expected_status": 403,
        "actual_status": 403,
        "status": "pass",
        "decision": "deny",
        "intervention_status": 403,
        "evidence_scope": "targeted",
        "full_matrix_ready": False,
    },
    "non_goals": [
        "No CRS support in first proof.",
        "No MRTS support in first proof.",
        "No full matrix.",
        "No response-body support claim.",
        "No production_verified claim.",
        "No merge-readiness impact.",
    ],
}

LITESPEED_CANDIDATE = {
    "candidate": "LiteSpeed / OpenLiteSpeed",
    "status": "planned",
    "edition_note": "OpenLiteSpeed is likely more CI-friendly; LiteSpeed Enterprise may add license/download automation risk.",
    "install_path": "Prefer package/container proof if license and automation permit it.",
    "modsecurity_crs_support": "Must be proven with the selected edition; do not assume libmodsecurity-v3 connector parity.",
    "first_proof": "OpenLiteSpeed install/start proof plus one CRS/request-blocking smoke, if automation and licensing allow it.",
    "main_risk": "License/download automation, edition differences, ModSecurity-engine compatibility, package availability, and CI reproducibility.",
    "evidence_required": "install log, start log, minimal config, request/response transcript, result.json, access/error/audit logs if available.",
    "not_allowed_claims": "No production status, no full matrix, no CRS compatibility claim, and no phase coverage claim before evidence exists.",
}

OTHER_CONNECTOR_FEASIBILITY = [
    {
        "connector": "lighttpd",
        "current_state": "partial_skeleton",
        "blocker": "No selected native ModSecurity integration, FastCGI/SCGI bridge, or runtime harness.",
        "first_proof_step": "Request-blocking feasibility proof that selects native module versus proxy/sidecar architecture.",
        "risk": "high",
    },
    {
        "connector": "traefik",
        "current_state": "partial_skeleton",
        "blocker": "No Go plugin/middleware, no forwardAuth runtime harness, and no libmodsecurity lifecycle proof.",
        "first_proof_step": "forwardAuth/decision-service returns 403 for a known malicious request with logs and result.json.",
        "risk": "high",
    },
]

OPENRESTY_DECISION = {
    "decision": "covered_by_nginx",
    "separate_connector": "no",
    "future_option": "nginx runtime variant / compatibility smoke",
    "reason": "NGINX-based stack",
    "full_matrix": "no separate full matrix",
    "reports": "no separate generated reports",
}

WORK_ITEMS = [
    {
        "priority": 1,
        "work_item": "Envoy architecture proof spec",
        "connector": "envoy",
        "output": "documented ext_proc/ext_authz choice and non-goals",
        "acceptance_criteria": "Roadmap and onboarding docs name protocol, evidence, and blocked claims.",
    },
    {
        "priority": 2,
        "work_item": "Envoy minimal smoke harness skeleton",
        "connector": "envoy",
        "output": "envoy.yaml, run-smoke.sh, upstream/decision-service launcher plan",
        "acceptance_criteria": "Can start Envoy and upstream locally without full-matrix integration.",
    },
    {
        "priority": 3,
        "work_item": "Envoy result/evidence schema",
        "connector": "envoy",
        "output": "targeted result.json and case-run schema",
        "acceptance_criteria": "Schema includes connector, case, expected/actual status, decision, intervention_status, evidence_scope, and full_matrix_ready=false.",
    },
    {
        "priority": 4,
        "work_item": "LiteSpeed install feasibility proof",
        "connector": "litespeed",
        "output": "OpenLiteSpeed install/start feasibility notes",
        "acceptance_criteria": "Documents license/download path, automation risk, and one request-blocking proof fixture.",
    },
    {
        "priority": 5,
        "work_item": "OpenResty compatibility-smoke decision",
        "connector": "openresty",
        "output": "nginx-owned compatibility-smoke decision",
        "acceptance_criteria": "No separate connector, no separate full matrix, no separate generated reports.",
    },
    {
        "priority": 6,
        "work_item": "Lighttpd feasibility note",
        "connector": "lighttpd",
        "output": "native-module versus sidecar/proxy feasibility note",
        "acceptance_criteria": "Identifies first request-blocking hook and evidence that would prove it.",
    },
    {
        "priority": 7,
        "work_item": "Traefik forwardAuth feasibility note",
        "connector": "traefik",
        "output": "decision-service/forwardAuth proof note",
        "acceptance_criteria": "Known malicious request returns 403 with decision logs in targeted proof.",
    },
]

NOT_ALLOWED_BEFORE_FULL_MATRIX = [
    "production_verified status",
    "merge-readiness contribution",
    "full-matrix PASS/FAIL counts",
    "CRS support across variants",
    "MRTS support",
    "response-body blocking support",
    "phase coverage parity with apache/nginx/haproxy",
    "runtime capability claims without result.json and logs",
]


def exists(root: Path, rel: str) -> bool:
    return (root / rel).exists()


def has_files(root: Path, rel: str, patterns: tuple[str, ...]) -> bool:
    base = root / rel
    return base.exists() and any(base.glob(pattern) for pattern in patterns)


def connector_status(name: str, directory: bool) -> str:
    if name in PRODUCTION:
        return "production_verified"
    if name in PARTIAL and directory:
        return "partial_skeleton"
    if name == "openresty":
        return "covered_by_existing_connector"
    if name == "litespeed":
        return "planned"
    return "unknown"


def connector_row(root: Path, name: str) -> dict[str, Any]:
    directory = exists(root, f"connectors/{name}")
    status = connector_status(name, directory)
    build_target = (
        exists(root, f"connectors/{name}/Makefile")
        or exists(root, f"connectors/{name}/Makefile.am")
        or (name == "nginx" and exists(root, "connectors/nginx/config"))
    )
    makefile_text = (root / "Makefile").read_text(encoding="utf-8")
    verified_case = name in PRODUCTION and f"verified-{name}-case" in makefile_text
    runtime_evidence = "yes" if name in PRODUCTION else "targeted proof required" if name in PARTIAL else "no"
    full_matrix = "yes" if name in PRODUCTION else "no"
    details = STATUS_DETAILS[name]
    return {
        "connector": name,
        "directory": "yes" if directory else "no",
        "current_status": status,
        "why": details["why"],
        "next_step": details["next_step"],
        "runtime_evidence": runtime_evidence,
        "full_matrix": full_matrix,
        "readme": "yes" if exists(root, f"connectors/{name}/README.md") else "no",
        "build_scripts": "yes" if has_files(root, f"connectors/{name}/build", ("*.sh", "*")) or build_target else "no",
        "runtime_harness": "yes" if has_files(root, f"connectors/{name}/harness", ("*.sh", "*.conf")) else "no",
        "example_config": "yes" if has_files(root, f"connectors/{name}/harness", ("*.conf", "*.example")) or has_files(root, f"connectors/{name}/poc", ("**/*.example", "**/*.cfg")) else "no",
        "modsecurity_integration": "yes" if name in PRODUCTION else "starter_only" if name in PARTIAL else "no",
        "tests": "framework_owned" if name in PRODUCTION or name in PARTIAL else "no",
        "build_target": "yes" if build_target else "no",
        "make_targets": "yes" if name in {"apache", "nginx", "haproxy", "envoy", "lighttpd", "traefik"} else "no",
        "report_integration": "yes" if name in PRODUCTION else "roadmap_only",
        "verified_case": "yes" if verified_case else "no",
        "verified_root_runtime_components": "yes" if name in PRODUCTION else "no",
    }


def candidate_ranking() -> list[dict[str, str | int]]:
    return [
        {
            "rank": 1,
            "connector": "envoy",
            "difficulty": "high",
            "risk": "medium-high",
            "expected_value": "high",
            "recommendation": "Next proof: targeted ext_proc/ext_authz runtime smoke with request blocking and explicit non-goals.",
        },
        {
            "rank": 2,
            "connector": "litespeed",
            "difficulty": "medium",
            "risk": "high",
            "expected_value": "medium-high",
            "recommendation": "Run OpenLiteSpeed installation/licensing proof before adding a connector directory.",
        },
        {
            "rank": 3,
            "connector": "traefik",
            "difficulty": "medium-high",
            "risk": "high",
            "expected_value": "medium",
            "recommendation": "Prototype forwardAuth/decision-service feasibility before any Go plugin work.",
        },
        {
            "rank": 4,
            "connector": "lighttpd",
            "difficulty": "high",
            "risk": "high",
            "expected_value": "medium",
            "recommendation": "Perform hook/proxy architecture spike before implementation.",
        },
    ]


def render_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(str(item).replace("|", "\\|") for item in row) + " |")
    return lines


def render_markdown(payload: dict[str, Any]) -> str:
    lines: list[str] = ["# Connector Roadmap", ""]
    scope = payload["roadmap_scope"]
    lines += [
        "## Roadmap Scope",
        "",
        "This report is `roadmap_only`. It evaluates repository structure, existing skeletons, technical feasibility, and first proof steps.",
        "It does not replace runtime evidence, does not generate full-matrix results, does not fabricate PASS/FAIL values, and must not influence Merge Readiness.",
        "",
    ]
    lines += render_table(
        ["Field", "Value"],
        [
            ["report_scope", scope["report_scope"]],
            ["evaluates", scope["evaluates"]],
            ["does_not_replace", scope["does_not_replace"]],
            ["full_matrix_results_created", scope["full_matrix_results_created"]],
            ["runtime_pass_fail_values_created", scope["runtime_pass_fail_values_created"]],
            ["merge_readiness_impact", scope["merge_readiness_impact"]],
        ],
    )
    lines += ["", "## Connector Status Matrix", ""]
    lines += render_table(
        ["Connector", "Directory", "Current Status", "Why", "Next Step", "Runtime Evidence?", "Full-Matrix?"],
        [
            [row["connector"], row["directory"], row["current_status"], row["why"], row["next_step"], row["runtime_evidence"], row["full_matrix"]]
            for row in payload["connector_status_matrix"]
        ],
    )
    lines += ["", "## Connector Candidate Ranking", ""]
    lines += render_table(
        ["Rank", "Connector", "Difficulty", "Risk", "Expected Value", "Recommendation"],
        [[item["rank"], item["connector"], item["difficulty"], item["risk"], item["expected_value"], item["recommendation"]] for item in payload["connector_candidate_ranking"]],
    )
    lines += ["", "## Connector Lifecycle", ""]
    lines += render_table(
        ["Stage", "Meaning", "Required Evidence", "Not Allowed Claims"],
        [[item["stage"], item["meaning"], item["required_evidence"], item["not_allowed_claims"]] for item in payload["connector_lifecycle"]],
    )
    lines += ["", "## New Connector Acceptance Criteria", ""]
    lines += render_table(
        ["Requirement", "Required for Skeleton", "Required for Verified-Case", "Required for Full-Matrix"],
        payload["new_connector_acceptance_criteria"],
    )
    lines += ["", "## Envoy Architecture Options", ""]
    lines += render_table(
        ["Option", "Description", "Pros", "Cons", "Proof Difficulty", "Recommendation"],
        [[item["option"], item["description"], item["pros"], item["cons"], item["proof_difficulty"], item["recommendation"]] for item in payload["envoy_architecture_options"]],
    )
    lines += ["", "### Envoy Option Capability Checks", ""]
    lines += render_table(
        ["Option", "Request Blocking", "Request Body", "Response Body", "Intervention Status", "Evidence", "CI Testability", "Risk"],
        [
            [item["option"], item["request_blocking"], item["request_body"], item["response_body"], item["intervention_status"], item["evidence"], item["ci_testability"], item["risk"]]
            for item in payload["envoy_architecture_options"]
        ],
    )
    proof = payload["recommended_envoy_proof"]
    lines += ["", "## Recommended Envoy Proof", ""]
    lines += render_table(
        ["Field", "Value"],
        [
            ["name", proof["name"]],
            ["scope", proof["scope"]],
            ["runtime_root", proof["runtime_root"]],
            ["goals", "<br>".join(proof["goals"])],
            ["artifacts", "<br>".join(proof["artifacts"])],
            ["evidence", "<br>".join(proof["evidence"])],
        ],
    )
    lines += ["", "### Envoy Minimal Result Schema", "", "```json"]
    lines += [
        "{",
        '  "connector": "envoy",',
        '  "case": "envoy_request_blocking_smoke",',
        '  "expected_status": 403,',
        '  "actual_status": 403,',
        '  "status": "pass",',
        '  "decision": "deny",',
        '  "intervention_status": 403,',
        '  "evidence_scope": "targeted",',
        '  "full_matrix_ready": false',
        "}",
    ]
    lines += ["```", "", "### Envoy Non-Goals", ""]
    lines += [f"- {item}" for item in proof["non_goals"]]
    litespeed = payload["litespeed_candidate"]
    lines += ["", "## LiteSpeed / OpenLiteSpeed Candidate", ""]
    lines += render_table(
        ["Field", "Value"],
        [[key, value] for key, value in litespeed.items()],
    )
    lines += ["", "## Lighttpd and Traefik Feasibility", ""]
    lines += render_table(
        ["Connector", "Current State", "Blocker", "First Proof Step", "Risk"],
        [[item["connector"], item["current_state"], item["blocker"], item["first_proof_step"], item["risk"]] for item in payload["lighttpd_traefik_feasibility"]],
    )
    lines += ["", "## OpenResty Decision", ""]
    lines += render_table(
        ["Field", "Value"],
        [[key, value] for key, value in payload["openresty_decision"].items()],
    )
    lines += ["", "## New Connector Work Items", ""]
    lines += render_table(
        ["Priority", "Work Item", "Connector", "Output", "Acceptance Criteria"],
        [[item["priority"], item["work_item"], item["connector"], item["output"], item["acceptance_criteria"]] for item in payload["new_connector_work_items"]],
    )
    lines += ["", "## Claims Not Allowed Before Full-Matrix Evidence", ""]
    lines += [f"- {item}" for item in payload["not_allowed_before_full_matrix"]]
    lines += ["", "## Recommended Next Connector", ""]
    lines += render_table(
        ["Field", "Value"],
        [
            ["Connector", "envoy"],
            ["First proof", proof["name"]],
            ["Why", STATUS_DETAILS["envoy"]["why"]],
            ["Non-goals", "<br>".join(proof["non_goals"])],
        ],
    )
    return "\n".join(lines)


def build_payload(root: Path) -> dict[str, Any]:
    rows = [connector_row(root, name) for name in CONNECTORS]
    return {
        "roadmap_scope": ROADMAP_SCOPE,
        "report_scope": ROADMAP_SCOPE["report_scope"],
        "runtime_values_invented": False,
        "full_matrix_rows_added": False,
        "merge_readiness_impact": "none",
        "connector_status_matrix": rows,
        "connector_candidate_ranking": candidate_ranking(),
        "connector_lifecycle": LIFECYCLE,
        "new_connector_acceptance_criteria": [list(item) for item in ACCEPTANCE_CRITERIA],
        "envoy_architecture_options": ENVOY_OPTIONS,
        "recommended_envoy_proof": ENVOY_PROOF,
        "litespeed_candidate": LITESPEED_CANDIDATE,
        "lighttpd_traefik_feasibility": OTHER_CONNECTOR_FEASIBILITY,
        "openresty_decision": OPENRESTY_DECISION,
        "new_connector_work_items": WORK_ITEMS,
        "not_allowed_before_full_matrix": NOT_ALLOWED_BEFORE_FULL_MATRIX,
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
    payload = build_payload(root)
    metadata = build_metadata(
        generated_by=GENERATOR,
        make_target=MAKE_TARGET,
        connector_root=root,
        framework_root=args.framework_root,
        inputs=INPUTS,
        report_key=REPORT_KEY,
        extra={"report_scope": ROADMAP_SCOPE["report_scope"], "merge_readiness_impact": "none"},
    )
    json_path = output_dir / GENERATED_REPORTS[REPORT_KEY].filename("json")
    md_path = output_dir / GENERATED_REPORTS[REPORT_KEY].filename("md")
    json_path.write_text(generated_json_text(payload, metadata), encoding="utf-8")
    md_path.write_text(generated_markdown_text(render_markdown(payload), metadata), encoding="utf-8")
    print("connector-roadmap: wrote roadmap_only report")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
