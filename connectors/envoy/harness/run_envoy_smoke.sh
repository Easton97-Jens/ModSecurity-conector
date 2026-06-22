#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
CONNECTOR_ROOT="${CONNECTOR_ROOT:-$(CDPATH= cd "$SCRIPT_DIR/../../.." && pwd)}"
FRAMEWORK_ROOT="${FRAMEWORK_ROOT:-$CONNECTOR_ROOT/modules/ModSecurity-test-Framework}"
HARNESS_PATH="$SCRIPT_DIR/$(basename "$0")"

. "$FRAMEWORK_ROOT/ci/common.sh"

export CONNECTOR_ROOT FRAMEWORK_ROOT HARNESS_PATH

sh "$CONNECTOR_ROOT/common/scripts/run_blocked_runtime_smoke.sh" \
    envoy \
    "$ENVOY_INTEGRATION_MODE" \
    ENVOY_BIN \
    envoy \
    "envoy runtime dependency not available in local common.sh-managed paths" \
    "Envoy ext_authz runtime smoke is blocked until ext_authz service wiring and a libmodsecurity-backed adapter are available." \
    "ext_authz runtime configuration and libmodsecurity-backed Envoy adapter" \
    "Phase 1 targets ext_authz; ext_proc is documented as a later phase."
