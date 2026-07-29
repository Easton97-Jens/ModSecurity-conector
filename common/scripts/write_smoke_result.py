#!/usr/bin/env python3
"""Write connector-neutral runtime smoke evidence.

This helper intentionally lives outside the public C headers. It centralizes
the JSON/text evidence contract used by open connector harnesses without
turning harness metadata into a runtime ABI.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


_CI_LIB = Path(__file__).resolve().parents[2] / "ci" / "lib"
if str(_CI_LIB) not in sys.path:
    sys.path.insert(0, str(_CI_LIB))

from runtime_path_utils import ensure_safe_runtime_directory, is_safe_runtime_root, verified_runtime_paths


DEFAULT_NOTE = (
    "Build/self-test starter evidence is available via make connector-starter-checks "
    "but is not runtime smoke evidence."
)
DEFAULT_CLAIMS_NOT_ALLOWED = (
    "production_ready=true",
    "full_matrix_ready=true",
    "crs_complete=true",
    "response_body_verified=true",
)
COMMON_COMPONENTS = (
    "msconnector/request.h",
    "msconnector/response.h",
    "msconnector/intervention.h",
    "msconnector/status.h",
    "msconnector/logging.h",
    "msconnector/capabilities.h",
    "msconnector/origin.h",
    "msconnector/transaction.h",
)
OUTPUT_PATH_ARGUMENTS = (
    ("evidence_root", "evidence_root"),
    ("results_dir", "results_dir"),
    ("tmp_root", "tmp_root"),
    ("log_root", "log_root"),
    ("log_dir", "log_dir"),
)
CONNECTOR_NAME_PATTERN = re.compile(r"[a-z0-9][a-z0-9_-]*")


def optional_int(value: str | None) -> int | None:
    if value in (None, "", "null", "none", "not-run"):
        return None
    return int(value)


def bool_text(value: str) -> bool:
    return value.lower() in {"1", "true", "yes", "on"}


def normalize_status(status: str) -> str:
    return status.upper()


def runtime_status_for(status: str, runtime_verified: bool) -> str:
    if runtime_verified:
        return "verified"
    if status == "BLOCKED":
        return "blocked"
    if status == "PASS":
        return "ok"
    return "error"


def require_safe_connector_name(value: str) -> str:
    if CONNECTOR_NAME_PATTERN.fullmatch(value) is None:
        raise SystemExit(f"BLOCKED: connector is not a safe output filename component: {value}")
    return value


def require_verified_output_directory(path: Path, label: str, runtime_root: Path) -> Path:
    text = str(path)
    if not path.is_absolute():
        raise SystemExit(f"BLOCKED: {label} must be absolute: {text}")
    try:
        resolved = path.resolve(strict=False)
    except (OSError, RuntimeError) as exc:
        raise SystemExit(f"BLOCKED: {label} cannot be resolved: {text}: {exc}") from exc
    try:
        resolved.relative_to(runtime_root)
    except ValueError as exc:
        raise SystemExit(
            f"BLOCKED: {label} is outside the verified runtime root: {resolved}"
        ) from exc
    try:
        return ensure_safe_runtime_directory(path)
    except ValueError as exc:
        raise SystemExit(f"BLOCKED: {label} is not a safe runtime directory: {text}: {exc}") from exc


def verified_output_directories(args: argparse.Namespace) -> dict[str, Path]:
    try:
        verified_paths = verified_runtime_paths(os.environ)
    except ValueError as exc:
        raise SystemExit(f"BLOCKED: invalid verified runtime paths: {exc}") from exc
    runtime_root = Path(verified_paths["VERIFIED_RUN_ROOT"])
    if not is_safe_runtime_root(runtime_root):
        raise SystemExit(f"BLOCKED: VERIFIED_RUN_ROOT is unsafe: {runtime_root}")
    return {
        name: require_verified_output_directory(Path(getattr(args, name)), label, runtime_root)
        for name, label in OUTPUT_PATH_ARGUMENTS
    }


def open_private_output_file(path: Path):
    no_follow = getattr(os, "O_NOFOLLOW", None)
    if no_follow is None:
        raise SystemExit("BLOCKED: safe output files require O_NOFOLLOW support")
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | no_follow, 0o600)
    except OSError as exc:
        raise SystemExit(f"BLOCKED: cannot open safe output file: {path}: {exc}") from exc
    os.fchmod(descriptor, 0o600)
    return os.fdopen(descriptor, "w", encoding="utf-8")


def write_json(path: Path, data: object) -> None:
    with open_private_output_file(path) as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
        handle.write("\n")


def write_jsonl(path: Path, record: object) -> None:
    with open_private_output_file(path) as handle:
        handle.write(json.dumps(record, sort_keys=True))
        handle.write("\n")


def write_text(path: Path, text: str) -> None:
    with open_private_output_file(path) as handle:
        handle.write(text)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--connector", required=True)
    parser.add_argument("--integration-mode", required=True)
    parser.add_argument("--status", default="BLOCKED")
    parser.add_argument("--exit-code", type=int, default=77)
    parser.add_argument("--runtime-verified", default="false")
    parser.add_argument("--response-body-verified", default="false")
    parser.add_argument("--allowed-request-status")
    parser.add_argument("--blocked-request-status")
    parser.add_argument("--decision-backend", default="simple")
    parser.add_argument("--modsecurity-ruleset", default="")
    parser.add_argument("--modsecurity-smoke-case", default="")
    parser.add_argument("--modsecurity-backend-verified", default="false")
    parser.add_argument("--modsecurity-rule-file", default="")
    parser.add_argument("--modsecurity-rule-id", default="")
    parser.add_argument("--modsecurity-rule-loaded", default="false")
    parser.add_argument("--request-body-smoke-verified", default="false")
    parser.add_argument("--request-body-access-enabled", default="false")
    parser.add_argument("--request-body-rule-file", default="")
    parser.add_argument("--request-body-rule-id", default="")
    parser.add_argument("--request-body-rule-loaded", default="false")
    parser.add_argument("--request-method", default="")
    parser.add_argument("--blocked-body-marker", default="")
    parser.add_argument("--intervention-status")
    parser.add_argument("--audit-log-path", default="")
    parser.add_argument("--decision-log-path", default="")
    parser.add_argument("--lighttpd-binary-verified", default="false")
    parser.add_argument("--lighttpd-http-verified", default="false")
    parser.add_argument("--sidecar-proxy-verified", default="false")
    parser.add_argument("--lighttpd-log-path", default="")
    parser.add_argument("--upstream-log-path", default="")
    parser.add_argument("--request-transcript-path", default="")
    parser.add_argument("--modsecurity-include-dir", default="")
    parser.add_argument("--modsecurity-lib-dir", default="")
    parser.add_argument("--modsecurity-lib-file", default="")
    parser.add_argument("--modsecurity-pkg-config-path", default="")
    parser.add_argument("--modsecurity-prefix", default="")
    parser.add_argument("--modsecurity-manifest", default="")
    parser.add_argument("--evidence-root", required=True)
    parser.add_argument("--results-dir", required=True)
    parser.add_argument("--connector-root", required=True)
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--build-root", required=True)
    parser.add_argument("--tmp-root", required=True)
    parser.add_argument("--log-root", required=True)
    parser.add_argument("--log-dir", required=True)
    parser.add_argument("--harness-path", required=True)
    parser.add_argument("--skipped-reason", required=True)
    parser.add_argument("--resolved-runtime-binary", default="")
    parser.add_argument("--runtime-binary-env-var", default="")
    parser.add_argument("--runtime-binary-name", default="")
    parser.add_argument("--runtime-lookup-root", action="append", default=[])
    parser.add_argument("--note", default=DEFAULT_NOTE)
    parser.add_argument("--starter-checks-available", default="false")
    parser.add_argument("--missing-dependency", action="append", default=[])
    parser.add_argument("--claim-not-allowed", action="append", default=[])
    parser.add_argument("--architecture-decision", default="")
    parser.add_argument("--crs-repo-url", default="")
    parser.add_argument("--crs-git-ref", default="")
    parser.add_argument("--crs-source-dir", default="")
    parser.add_argument("--crs-runtime-dir", default="")
    parser.add_argument("--crs-version", default="")
    parser.add_argument("--crs-smoke-case", default="")
    parser.add_argument("--crs-minimal-smoke-verified", default="false")
    parser.add_argument("--crs-secondary-smoke-verified", default="false")
    parser.add_argument("--crs-rule-id", default="")
    parser.add_argument("--crs-rule-message", default="")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    connector = require_safe_connector_name(args.connector)
    status = normalize_status(args.status)
    output_directories = verified_output_directories(args)
    evidence_root = output_directories["evidence_root"]
    results_dir = output_directories["results_dir"]
    log_dir = output_directories["log_dir"]

    runtime_verified = bool_text(args.runtime_verified)
    response_body_verified = bool_text(args.response_body_verified)
    starter_checks_available = bool_text(args.starter_checks_available)
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    runtime_status = runtime_status_for(status, runtime_verified)
    claims_not_allowed = args.claim_not_allowed or list(DEFAULT_CLAIMS_NOT_ALLOWED)
    if not runtime_verified and "runtime_verified=true" not in claims_not_allowed:
        claims_not_allowed.insert(0, "runtime_verified=true")
    modsecurity_backend_verified = bool_text(args.modsecurity_backend_verified)
    modsecurity_rule_loaded = bool_text(args.modsecurity_rule_loaded)
    request_body_smoke_verified = bool_text(args.request_body_smoke_verified)
    request_body_access_enabled = bool_text(args.request_body_access_enabled)
    request_body_rule_loaded = bool_text(args.request_body_rule_loaded)
    crs_minimal_smoke_verified = bool_text(args.crs_minimal_smoke_verified)
    crs_secondary_smoke_verified = bool_text(args.crs_secondary_smoke_verified)
    lighttpd_binary_verified = bool_text(args.lighttpd_binary_verified)
    lighttpd_http_verified = bool_text(args.lighttpd_http_verified)
    sidecar_proxy_verified = bool_text(args.sidecar_proxy_verified)
    if not modsecurity_backend_verified and "modsecurity_backend_verified=true" not in claims_not_allowed:
        claims_not_allowed.append("modsecurity_backend_verified=true")
    if not request_body_smoke_verified and "request_body_smoke_verified=true" not in claims_not_allowed:
        claims_not_allowed.append("request_body_smoke_verified=true")
    if not crs_minimal_smoke_verified and "crs_minimal_smoke_verified=true" not in claims_not_allowed:
        claims_not_allowed.append("crs_minimal_smoke_verified=true")
    if not crs_secondary_smoke_verified and "crs_secondary_smoke_verified=true" not in claims_not_allowed:
        claims_not_allowed.append("crs_secondary_smoke_verified=true")
    missing_dependencies = args.missing_dependency
    allowed_request_status = optional_int(args.allowed_request_status)
    blocked_request_status = optional_int(args.blocked_request_status)
    intervention_status = optional_int(args.intervention_status)
    resolved_runtime_binary = args.resolved_runtime_binary or None
    runtime_lookup_roots = []
    for root in args.runtime_lookup_root:
        if root and root not in runtime_lookup_roots:
            runtime_lookup_roots.append(root)
    runtime_inventory = {
        "binary_env_var": args.runtime_binary_env_var or None,
        "binary_name": args.runtime_binary_name or None,
        "lookup_roots": runtime_lookup_roots,
        "resolved_runtime_binary": resolved_runtime_binary,
        "state": "resolved" if resolved_runtime_binary else "missing",
    }

    result = {
        "allowed_request_status": allowed_request_status,
        "architecture_decision": args.architecture_decision or None,
        "blocked_body_marker": args.blocked_body_marker or None,
        "blocked_request_status": blocked_request_status,
        "claims_not_allowed": claims_not_allowed,
        "common_msconnector_components": list(COMMON_COMPONENTS),
        "connector": connector,
        "crs_complete": False,
        "crs_git_ref": args.crs_git_ref or None,
        "crs_minimal_smoke_verified": crs_minimal_smoke_verified,
        "crs_repo_url": args.crs_repo_url or None,
        "crs_rule_id": args.crs_rule_id or None,
        "crs_rule_message": args.crs_rule_message or None,
        "crs_runtime_dir": args.crs_runtime_dir or None,
        "crs_secondary_smoke_verified": crs_secondary_smoke_verified,
        "crs_smoke_case": args.crs_smoke_case or None,
        "crs_source_dir": args.crs_source_dir or None,
        "crs_version": args.crs_version or None,
        "decision_backend": args.decision_backend,
        "decision_log_path": args.decision_log_path or None,
        "evidence_root": str(evidence_root),
        "exit_code": args.exit_code,
        "full_matrix_ready": False,
        "integration_mode": args.integration_mode,
        "intervention_status": intervention_status,
        "lighttpd_binary_verified": lighttpd_binary_verified,
        "lighttpd_http_verified": lighttpd_http_verified,
        "lighttpd_log_path": args.lighttpd_log_path or None,
        "missing_dependencies": missing_dependencies,
        "modsecurity_backend_verified": modsecurity_backend_verified,
        "modsecurity_dependency_inventory": {
            "include_dir": args.modsecurity_include_dir or None,
            "lib_dir": args.modsecurity_lib_dir or None,
            "lib_file": args.modsecurity_lib_file or None,
            "manifest": args.modsecurity_manifest or None,
            "pkg_config_path": args.modsecurity_pkg_config_path or None,
            "prefix": args.modsecurity_prefix or None,
        },
        "modsecurity_rule_file": args.modsecurity_rule_file or None,
        "modsecurity_rule_id": args.modsecurity_rule_id or None,
        "modsecurity_rule_loaded": modsecurity_rule_loaded,
        "modsecurity_ruleset": args.modsecurity_ruleset or None,
        "modsecurity_smoke_case": args.modsecurity_smoke_case or None,
        "audit_log_path": args.audit_log_path or None,
        "production_ready": False,
        "response_body_verified": response_body_verified,
        "resolved_runtime_binary": resolved_runtime_binary,
        "request_body_access_enabled": request_body_access_enabled,
        "request_body_rule_file": args.request_body_rule_file or None,
        "request_body_rule_id": args.request_body_rule_id or None,
        "request_body_rule_loaded": request_body_rule_loaded,
        "request_body_smoke_verified": request_body_smoke_verified,
        "request_method": args.request_method or None,
        "request_transcript_path": args.request_transcript_path or None,
        "runtime_inventory": runtime_inventory,
        "runtime_status": runtime_status,
        "runtime_verified": runtime_verified,
        "sidecar_proxy_verified": sidecar_proxy_verified,
        "skipped_reason": args.skipped_reason,
        "status": status,
        "timestamp": timestamp,
        "upstream_log_path": args.upstream_log_path or None,
    }

    record = {
        **result,
        "check": "runtime-smoke-entrypoint",
        "command": f"make smoke-{connector}",
        "generated_at": timestamp,
        "harness_path": args.harness_path,
        "installs_global_artifacts": False,
        "note": args.note,
        "starter_checks_available": starter_checks_available,
        "test_type": "runtime-smoke",
    }

    counts = {"PASS": 0, "FAIL": 0, "BLOCKED": 0, "NOT_RUN": 0}
    counts[status] = counts.get(status, 0) + 1
    summary = {
        "build_root": args.build_root,
        "connector": connector,
        "connector_root": args.connector_root,
        "counts": counts,
        "evidence_root": str(evidence_root),
        "generated_at": timestamp,
        "harness_path": args.harness_path,
        "installs_global_artifacts": False,
        "integration_mode": args.integration_mode,
        "lighttpd_binary_verified": lighttpd_binary_verified,
        "lighttpd_http_verified": lighttpd_http_verified,
        "log_dir": args.log_dir,
        "log_root": args.log_root,
        "note": args.note,
        "reason": args.skipped_reason,
        "response_body_verified": response_body_verified,
        "results": [record],
        "results_dir": str(results_dir),
        "runtime_status": runtime_status,
        "runtime_verified": runtime_verified,
        "sidecar_proxy_verified": sidecar_proxy_verified,
        "source_root": args.source_root,
        "starter_checks_available": starter_checks_available,
        "status": status,
        "tmp_root": args.tmp_root,
    }

    runtime_text = "Runtime verified" if runtime_verified else "Runtime not verified"
    status_text = (
        f"{status} {connector}-runtime-smoke {args.skipped_reason}\n"
        f"{runtime_text}\n"
        f"Evidence root: {evidence_root}\n"
        f"{args.note}\n"
    )

    write_json(evidence_root / "result.json", result)
    if args.modsecurity_ruleset == "crs" and args.crs_smoke_case == "secondary":
        write_json(evidence_root / "crs-secondary-result.json", result)
    elif args.modsecurity_ruleset == "crs":
        write_json(evidence_root / "crs-result.json", result)
    elif args.modsecurity_ruleset == "targeted" and args.modsecurity_smoke_case == "request_body":
        write_json(evidence_root / "request-body-result.json", result)
    elif args.modsecurity_ruleset == "targeted" and args.decision_backend == "libmodsecurity":
        write_json(evidence_root / "targeted-result.json", result)
    elif args.decision_backend == "simple":
        write_json(evidence_root / "runtime-result.json", result)
    write_jsonl(evidence_root / "results.jsonl", record)
    write_json(evidence_root / "summary.json", summary)
    write_text(evidence_root / "summary.txt", status_text)
    write_text(log_dir / "status.log", status_text)

    write_jsonl(results_dir / f"{connector}-results.jsonl", record)
    write_json(results_dir / f"{connector}-summary.json", summary)
    write_text(results_dir / f"{connector}-summary.txt", status_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
