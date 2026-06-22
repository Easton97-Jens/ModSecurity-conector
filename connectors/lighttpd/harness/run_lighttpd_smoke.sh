#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
CONNECTOR_ROOT="${CONNECTOR_ROOT:-$(CDPATH= cd "$SCRIPT_DIR/../../.." && pwd)}"
HARNESS_PATH="$SCRIPT_DIR/$(basename "$0")"

export CONNECTOR_ROOT HARNESS_PATH

sh "$CONNECTOR_ROOT/common/scripts/run_blocked_runtime_smoke.sh" \
    lighttpd \
    architecture_spike_plus_runtime_smoke \
    LIGHTTPD_BIN \
    lighttpd \
    "lighttpd runtime dependency not available in local common.sh-managed paths" \
    "lighttpd integration mode not selected" \
    "lighttpd integration mode" \
    "Architecture spike compares native module, FastCGI/SCGI, sidecar/proxy, and mod_magnet/Lua before selecting the runtime path." \
    0
