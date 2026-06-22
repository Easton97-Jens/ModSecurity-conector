#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
CONNECTOR_ROOT="${CONNECTOR_ROOT:-$(CDPATH= cd "$SCRIPT_DIR/../../.." && pwd)}"
HARNESS_PATH="$SCRIPT_DIR/$(basename "$0")"

export CONNECTOR_ROOT HARNESS_PATH

sh "$CONNECTOR_ROOT/common/scripts/run_blocked_runtime_smoke.sh" \
    traefik \
    forwardAuth \
    "Traefik forwardAuth runtime smoke is blocked until a Traefik binary, forwardAuth service wiring, and libmodsecurity-backed decision service are available." \
    "traefik binary, forwardAuth runtime configuration, and libmodsecurity-backed decision service" \
    "Phase 1 targets forwardAuth; a Go plugin is explicitly out of scope."
