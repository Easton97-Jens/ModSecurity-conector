#!/usr/bin/env python3
"""Resolve and attest the closed five-connector ``no-crs`` CI profile.

This intentionally does not infer a row from a capability file: the small
checked-in inventory is the profile boundary, and rows outside it are rejected.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

_CI_ROOT = next(parent for parent in Path(__file__).resolve().parents if parent.name == "ci")
if str(_CI_ROOT / "lib") not in sys.path:
    sys.path.insert(0, str(_CI_ROOT / "lib"))

from runtime_path_utils import (  # noqa: E402
    prepare_verified_runtime_artifact_root,
    runtime_artifact_path,
    write_runtime_artifact_text_atomic,
)

PROFILE = "no-crs"
CONNECTORS = ("apache", "haproxy", "envoy", "traefik", "lighttpd")
RECEIPT_KEY = "five_connector_profile_receipt"
RECEIPT_PATH = "logs/five_connector_profile_receipt.log"
SHA256 = re.compile(r"[0-9a-f]{40,64}\Z")
RUN_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")

# This is proven row metadata, not a derived compatibility claim.  Keep the
# rows compact because this JSON is emitted directly as a GitHub matrix.
ROWS: tuple[dict[str, str], ...] = (
    {"connector": "apache", "integration_mode": "native-httpd-module", "protocol": "http1", "phase4_mode": "safe", "connector_profile": "full-lifecycle-low-latency", "evidence_scope": "source-wiring-and-baseline-only"},
    {"connector": "haproxy", "integration_mode": "spoe-spop-agent", "protocol": "http1", "phase4_mode": "not_applicable", "connector_profile": "header-compatibility", "evidence_scope": "no-response-body-host-path"},
    {"connector": "envoy", "integration_mode": "http-ext-authz-service", "protocol": "http1", "phase4_mode": "not_applicable", "connector_profile": "request-only-compatibility", "evidence_scope": "no-response-host-path"},
    {"connector": "traefik", "integration_mode": "http-forwardauth-service", "protocol": "http1", "phase4_mode": "not_applicable", "connector_profile": "request-only-compatibility", "evidence_scope": "no-response-host-path"},
    {"connector": "lighttpd", "integration_mode": "native-lighttpd-plugin", "protocol": "http1", "phase4_mode": "not_applicable", "connector_profile": "header-compatibility", "evidence_scope": "no-native-body-host-path"},
)
ROW_BY_CONNECTOR = {row["connector"]: row for row in ROWS}


def fail(message: str) -> ValueError:
    return ValueError(message)


def load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise fail(f"cannot read {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise fail(f"{label} must be a JSON object")
    return value


def profile_row(connector: str) -> dict[str, str]:
    try:
        return dict(ROW_BY_CONNECTOR[connector])
    except KeyError as exc:
        raise fail(f"connector is not in the closed {PROFILE} profile: {connector!r}") from exc


def verify_connector(connector: str, capabilities: Path) -> dict[str, str]:
    row = profile_row(connector)
    manifest = load_json(capabilities, "capability manifest")
    if manifest.get("connector") != connector:
        raise fail("capability manifest connector does not match selected row")
    if manifest.get("integration_mode") != row["integration_mode"]:
        raise fail("capability manifest integration_mode does not match selected row")
    capabilities_value = manifest.get("capabilities")
    if not isinstance(capabilities_value, dict):
        raise fail("capability manifest is missing capabilities")
    if row["protocol"] == "http1":
        http1 = capabilities_value.get("http1_content_length")
        http1_state = http1.get("state") if isinstance(http1, dict) else None
        if http1_state in {None, "not_implemented", "not_applicable", "unsupported_by_host_model"}:
            raise fail("http1 row requires an available http1_content_length capability")
    else:
        raise fail(f"unsupported profile protocol: {row['protocol']}")
    phase4 = capabilities_value.get("phase4")
    phase4_state = phase4.get("state") if isinstance(phase4, dict) else None
    if row["phase4_mode"] == "safe":
        if phase4_state in {"not_implemented", "unsupported_by_host_model", None}:
            raise fail("safe row requires a capability manifest Phase-4 path")
    elif phase4_state not in {"not_implemented", "unsupported_by_host_model"}:
        raise fail("not_applicable row requires an unavailable Phase-4 manifest state")
    return row


def verify_row(values: Mapping[str, str], capabilities: Path) -> dict[str, str]:
    connector = values.get("connector", "")
    expected = verify_connector(connector, capabilities)
    for name, expected_value in expected.items():
        if values.get(name) != expected_value:
            raise fail(f"row {name} must be {expected_value!r}, got {values.get(name)!r}")
    return expected


def _token(value: str, label: str, pattern: re.Pattern[str]) -> str:
    if not pattern.fullmatch(value):
        raise fail(f"{label} is invalid")
    return value


def receipt_payload(*, connector: str, run_id: str, connector_commit: str,
                    framework_commit: str, cleanup_status: str) -> dict[str, str | int]:
    row = profile_row(connector)
    _token(run_id, "run id", RUN_ID)
    _token(connector_commit, "connector commit", SHA256)
    _token(framework_commit, "framework commit", SHA256)
    if cleanup_status not in {"passed", "failed"}:
        raise fail("cleanup status must be passed or failed")
    return {
        "schema_version": 1,
        "profile": PROFILE,
        "connector": connector,
        "integration_mode": row["integration_mode"],
        "protocol": row["protocol"],
        "phase4_mode": row["phase4_mode"],
        "connector_profile": row["connector_profile"],
        "evidence_scope": row["evidence_scope"],
        "run_id": run_id,
        "connector_commit": connector_commit,
        "framework_commit": framework_commit,
        "cleanup_status": cleanup_status,
    }


def write_receipt(runtime_root: Path, output: Path, **values: str) -> Path:
    root = prepare_verified_runtime_artifact_root(runtime_root)
    destination = runtime_artifact_path(root, output, "five-connector profile receipt")
    payload = receipt_payload(**values)
    write_runtime_artifact_text_atomic(root, destination, json.dumps(payload, sort_keys=True) + "\n", "five-connector profile receipt")
    return destination


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", required=True, choices=(PROFILE,))
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--emit-github-matrix", action="store_true")
    action.add_argument("--emit-connectors", action="store_true")
    action.add_argument("--verify-row", action="store_true")
    action.add_argument("--verify-connector", action="store_true")
    action.add_argument("--write-receipt", action="store_true")
    parser.add_argument("--connector")
    parser.add_argument("--integration-mode")
    parser.add_argument("--protocol")
    parser.add_argument("--phase4-mode")
    parser.add_argument("--connector-profile")
    parser.add_argument("--evidence-scope")
    parser.add_argument("--capabilities", type=Path)
    parser.add_argument("--runtime-root", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--run-id")
    parser.add_argument("--connector-commit")
    parser.add_argument("--framework-commit")
    parser.add_argument("--cleanup-status")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.emit_github_matrix:
            print(json.dumps({"include": list(ROWS)}, separators=(",", ":"), sort_keys=True))
            return 0
        if args.emit_connectors:
            print("\n".join(CONNECTORS))
            return 0
        if args.verify_row:
            if not args.capabilities:
                raise fail("--verify-row requires --capabilities")
            verify_row({"connector": args.connector or "", "integration_mode": args.integration_mode or "", "protocol": args.protocol or "", "phase4_mode": args.phase4_mode or "", "connector_profile": args.connector_profile or "", "evidence_scope": args.evidence_scope or ""}, args.capabilities)
            return 0
        if args.verify_connector:
            if not args.connector or not args.capabilities:
                raise fail("--verify-connector requires --connector and --capabilities")
            verify_connector(args.connector, args.capabilities)
            return 0
        required = (args.runtime_root, args.output, args.connector, args.run_id, args.connector_commit, args.framework_commit, args.cleanup_status)
        if any(value is None for value in required):
            raise fail("--write-receipt requires runtime/output/identity/cleanup arguments")
        write_receipt(args.runtime_root, args.output, connector=args.connector, run_id=args.run_id, connector_commit=args.connector_commit, framework_commit=args.framework_commit, cleanup_status=args.cleanup_status)
        return 0
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
