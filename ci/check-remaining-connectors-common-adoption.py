#!/usr/bin/env python3
"""Verify live Common SDK adoption by Envoy, Traefik and lighttpd."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONNECTORS = ("envoy", "traefik", "lighttpd")
ALLOWED_EVIDENCE_STATUS = {
    "not_verified",
    "connector-gap",
    "compile_verified",
    "link_verified",
    "config_load_verified",
    "start_smoke_verified",
    "minimal_runtime_smoke",
    "partial_runtime_path",
    "requires_runtime_evidence",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""


def require(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def connector_checks(connector: str, errors: list[str]) -> None:
    base = ROOT / "connectors" / connector
    mapper_header = base / "src" / f"{connector}_modsecurity_mapper.h"
    mapper_source = base / "src" / f"{connector}_modsecurity_mapper.c"
    header_text = read(mapper_header)
    source_text = read(mapper_source)
    require(errors, mapper_header.is_file(), f"{connector}: mapper header missing")
    require(errors, mapper_source.is_file(), f"{connector}: mapper source missing")
    require(
        errors,
        "msconnector_generic_map_request" in source_text,
        f"{connector}: request mapper does not call Common generic mapper",
    )
    require(
        errors,
        "msconnector_generic_map_response" in source_text,
        f"{connector}: response mapper does not call Common generic mapper",
    )
    require(
        errors,
        "msconnector_generic_config_init" in source_text + header_text,
        f"{connector}: config is not initialized through Common",
    )

    config_dir = base / "config"
    configs = list(config_dir.glob("*.conf")) if config_dir.is_dir() else []
    require(errors, bool(configs), f"{connector}: connector runtime config missing")
    config_text = "\n".join(read(path) for path in configs)
    for key in (
        "enabled=",
        "rules_file=",
        "transaction_id_header=",
        "request_body_mode=",
        "response_body_mode=",
        "request_body_limit=",
        "default_block_status=",
        "default_error_status=",
        "event_path=",
        "max_header_count=",
        "max_total_header_bytes=",
    ):
        require(errors, key in config_text, f"{connector}: config does not map {key[:-1]}")

    metadata = read(base / "metadata.c")
    require(
        errors,
        '"connector-gap"' in metadata or '"partial_runtime_path"' in metadata,
        f"{connector}: connector-gap or partial-runtime boundary missing",
    )
    require(
        errors,
        any(f'"{status}"' in metadata for status in ALLOWED_EVIDENCE_STATUS),
        f"{connector}: metadata has no allowed evidence status",
    )
    source_map = read(base / "SOURCE_MAP.json")
    require(
        errors,
        any(status in source_map for status in ALLOWED_EVIDENCE_STATUS),
        f"{connector}: SOURCE_MAP has no allowed evidence status",
    )

    tree_text = "\n".join(
        read(path)
        for path in base.rglob("*")
        if path.is_file() and path.suffix.lower() in {".c", ".h", ".md", ".json", ".sh", ".py"}
    )
    forbidden_positive_claims = (
        r'production_ready[" ]*[:=][" ]*true',
        r'full_matrix_ready[" ]*[:=][" ]*true',
        r'crs_complete[" ]*[:=][" ]*true',
        r'response_body_verified[" ]*[:=][" ]*true',
        r'security_verified[" ]*[:=][" ]*true',
    )
    for pattern in forbidden_positive_claims:
        require(
            errors,
            re.search(pattern, tree_text, flags=re.IGNORECASE) is None,
            f"{connector}: forbidden positive claim matches {pattern}",
        )
    require(
        errors,
        "free((void *)" not in tree_text,
        f"{connector}: const-dropping ownership cleanup found",
    )

    if connector == "envoy":
        host = read(base / "src" / "envoy_ext_authz_service_main.c")
        runtime = read(base / "harness" / "run_envoy_connector_runtime.sh")
        require(errors, '"ext_authz"' in host, "envoy: ext_authz profile missing")
        require(
            errors,
            "msconnector_http_authorization_service_main" in host,
            "envoy: connector-owned authorization service missing",
        )
        require(errors, "ENVOY_BIN" in runtime and "403" in runtime, "envoy: real host runtime smoke missing")
    elif connector == "traefik":
        host = read(base / "src" / "traefik_forwardauth_service_main.c")
        runtime = read(base / "scripts" / "runtime-smoke.sh") + read(base / "scripts" / "runtime_smoke.py")
        require(errors, '"forwardAuth"' in host, "traefik: forwardAuth profile missing")
        require(
            errors,
            "msconnector_http_authorization_service_main" in host,
            "traefik: connector-owned authorization service missing",
        )
        require(errors, "TRAEFIK_BIN" in runtime and "403" in runtime, "traefik: real host runtime smoke missing")
    else:
        module = read(base / "module" / "mod_msconnector.c")
        for token in (
            "mod_msconnector_plugin_init",
            "handle_uri_clean",
            "handle_response_start",
            "handle_request_reset",
            "config_plugin_values_init",
            "msconnector_runtime_transaction_begin",
            "msconnector_runtime_transaction_process_response",
            "msconnector_runtime_transaction_finish",
        ):
            require(errors, token in module, f"lighttpd: native module missing {token}")


def shared_runtime_checks(errors: list[str]) -> None:
    runtime = read(ROOT / "common" / "runtime" / "msconnector_runtime.c")
    service = read(ROOT / "common" / "runtime" / "http_authorization_service.c")
    for token in (
        "msconnector_config_init",
        "msconnector_config_apply_defaults",
        "msconnector_config_validate",
        "msconnector_parse_bool",
        "msconnector_directive_adapter_validate_all",
        "msconnector_rule_loader_load_config",
        "msconnector_modsecurity_engine_start",
        "msconnector_modsecurity_transaction_init",
        "msconnector_transaction_id_resolve",
        "msconnector_decision_action_from_decision",
        "msconnector_event_write_jsonl_line",
        "msconnector_resource_limits_init",
        "msconnector_dos_guard_check_request",
        "msconnector_flow_guard_mark_validated",
        "msconnector_integrity_event_hash",
        "msconnector_alloc_checked",
    ):
        require(errors, token in runtime, f"shared remaining-connector runtime missing {token}")
    for invariant in (
        "content_length > body_limit",
        "header_count > 0U",
        "request->body.size > 0U",
    ):
        require(errors, invariant in runtime + service, f"shared runtime missing invariant {invariant}")
    require(errors, "body_payload" not in runtime, "shared event path exposes a body payload field")
    require(errors, "request_body_payload" not in runtime, "shared event path exposes request body payload")
    require(errors, "response_body_payload" not in runtime, "shared event path exposes response body payload")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connector", choices=CONNECTORS)
    args = parser.parse_args()
    errors: list[str] = []
    shared_runtime_checks(errors)
    selected = (args.connector,) if args.connector else CONNECTORS
    for connector in selected:
        connector_checks(connector, errors)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    label = args.connector or "all"
    print(f"remaining connector common adoption: ok ({label})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
