#!/usr/bin/env python3
"""Materialize an effective capability manifest for one selected host profile.

The checked-in connector manifests describe the default compatibility path in
several connectors.  A full-lifecycle run must instead record the host path it
actually selected.  This helper creates a run-local, capability-conservative
overlay; it never changes the checked-in manifest and never upgrades a
capability to ``verified``.
"""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping, Sequence


PROFILE_BY_CONNECTOR = {
    "apache": "native-httpd-module",
    "nginx": "native-nginx-http-module",
    "haproxy": "native-htx-filter",
    "envoy": "ext_proc",
    "traefik": "native-middleware",
    "lighttpd": "patched-native",
}


PROFILE_METADATA: dict[str, dict[str, str]] = {
    "apache": {
        "host_name": "Apache HTTP Server native module",
        "integration_mode": "native-httpd-module",
        "reason": "The selected full-lifecycle route is the native httpd module.",
    },
    "nginx": {
        "host_name": "NGINX native HTTP module",
        "integration_mode": "native-nginx-http-module",
        "reason": "The selected full-lifecycle route is the native NGINX HTTP module.",
    },
    "haproxy": {
        "host_name": "HAProxy 3.2.21 native HTX filter",
        "integration_mode": "native-htx-filter",
        "reason": (
            "The selected route is the patched HAProxy 3.2.21 HTX filter; it "
            "runs in observer mode and cannot promote enforcement."
        ),
    },
    "envoy": {
        "host_name": "Envoy ext_proc listener",
        "integration_mode": "ext_proc",
        "reason": (
            "The selected route is the streamed Envoy ext_proc listener; its "
            "PassthroughEngine has no Common/libmodsecurity rule-evaluation bridge."
        ),
    },
    "traefik": {
        "host_name": "Traefik native middleware",
        "integration_mode": "native-traefik-middleware",
        "reason": (
            "The selected route is the native Traefik middleware in the pinned "
            "host; its current Engine is passthrough-only and non-promotable."
        ),
    },
    "lighttpd": {
        "host_name": "lighttpd 1.4.84 patched native host",
        "integration_mode": "patched-native-lighttpd",
        "reason": (
            "The selected route is the patched lighttpd 1.4.84 core and matching "
            "module; request and response bodies remain deliberately disabled."
        ),
    },
}


# States below describe only source/transport availability.  They deliberately
# never assert a host proof or runtime promotion.  The canonical runner still
# requires a matching host event before it can turn any case into PASS.
IMPLEMENTED_NOT_ASSERTED: dict[str, tuple[str, ...]] = {
    "haproxy": (
        "connection_metadata",
        "transport_metadata",
        "request_headers",
        "request_body_incremental_ingest",
        "response_headers",
        "response_body_incremental_ingest",
        "phase1",
        "phase2",
        "phase3",
        "phase4",
        "phase4_rule_evaluation",
        "phase4_end_of_stream_evaluation",
        "no_full_response_buffering",
        "transaction_id",
        "event_jsonl",
    ),
    "envoy": (
        "transport_metadata",
        "request_headers",
        "request_body_incremental_ingest",
        "response_headers",
        "response_body_incremental_ingest",
        "no_full_response_buffering",
        "event_jsonl",
    ),
    "traefik": (
        "transport_metadata",
        "no_full_response_buffering",
    ),
    "lighttpd": (
        "connection_metadata",
        "transport_metadata",
        "request_headers",
        # The patched native host has a real P1 200/403 probe.  Keep the
        # capability available to the canonical plan without promoting it;
        # finalization still requires the run-local host event before a case
        # can become PASS.
        "deny",
        "response_headers",
        "phase1",
        "phase3",
        "transaction_id",
        "event_jsonl",
    ),
}


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read capability manifest {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"capability manifest must be an object: {path}")
    connector = payload.get("connector")
    if connector not in PROFILE_BY_CONNECTOR:
        raise ValueError(f"unsupported connector in capability manifest: {connector!r}")
    if not isinstance(payload.get("capabilities"), dict):
        raise ValueError("capability manifest is missing capabilities")
    return payload


def set_capability(
    capabilities: dict[str, Any], name: str, state: str, reason: str
) -> None:
    current = capabilities.get(name)
    if not isinstance(current, Mapping):
        raise ValueError(f"capability manifest is missing {name}")
    replacement = dict(current)
    replacement["state"] = state
    replacement["reason"] = reason
    capabilities[name] = replacement


def effective_manifest(payload: Mapping[str, Any], profile: str) -> dict[str, Any]:
    connector = str(payload.get("connector") or "")
    expected_profile = PROFILE_BY_CONNECTOR.get(connector)
    if expected_profile is None:
        raise ValueError(f"unsupported connector: {connector!r}")
    if profile != expected_profile:
        raise ValueError(
            f"invalid full-lifecycle profile {profile!r} for {connector}; "
            f"expected {expected_profile!r}"
        )

    output = deepcopy(dict(payload))
    metadata = PROFILE_METADATA[connector]
    output["host_name"] = metadata["host_name"]
    output["integration_mode"] = metadata["integration_mode"]
    output["full_lifecycle_profile"] = profile
    output["full_lifecycle_profile_reason"] = metadata["reason"]
    constraints = list(output.get("host_model_constraints") or [])
    constraints.append(f"Selected full-lifecycle host profile: {profile}. {metadata['reason']}")
    output["host_model_constraints"] = constraints

    capabilities = output["capabilities"]
    if connector in IMPLEMENTED_NOT_ASSERTED:
        # Start conservatively: compatibility-path states cannot leak into a
        # selected native profile merely because the same connector owns both.
        for name in capabilities:
            set_capability(
                capabilities,
                name,
                "not_implemented",
                f"Not asserted for selected full-lifecycle profile {profile}; no canonical host evidence exists.",
            )
        for name in IMPLEMENTED_NOT_ASSERTED[connector]:
            set_capability(
                capabilities,
                name,
                "implemented_not_asserted",
                f"Implemented or observed on selected profile {profile}, but not promoted without a canonical host run.",
            )

    return output


def write_json_atomically(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.tmp-", dir=path.parent, text=True
    )
    temporary_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_path, path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--profile", required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        output = effective_manifest(load_manifest(args.input), args.profile)
        write_json_atomically(args.output, output)
    except ValueError as exc:
        print(f"FAIL: {exc}", file=os.sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
