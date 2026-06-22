#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
CONNECTOR_ROOT="${CONNECTOR_ROOT:-$(CDPATH= cd "$SCRIPT_DIR/../../.." && pwd)}"
HARNESS_PATH="$SCRIPT_DIR/$(basename "$0")"

export CONNECTOR_ROOT HARNESS_PATH

sh "$CONNECTOR_ROOT/common/scripts/run_blocked_runtime_smoke.sh" \
    envoy \
    ext_authz \
    "Envoy ext_authz runtime smoke is blocked until an Envoy binary, ext_authz service wiring, and libmodsecurity-backed adapter are available." \
    "envoy binary, ext_authz runtime configuration, and libmodsecurity-backed Envoy adapter" \
    "Phase 1 targets ext_authz; ext_proc is documented as a later phase."
