#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
CONNECTOR_ROOT=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
REPO_ROOT=$(CDPATH= cd "$CONNECTOR_ROOT/../.." && pwd)
BUILD_ROOT="${BUILD_ROOT:-${TMPDIR:-/var/tmp}/ModSecurity-conector-verified/build}"
CONNECTOR_BIN="${TRAEFIK_CONNECTOR_BIN:-$BUILD_ROOT/traefik-connector/traefik-forwardauth}"
CONFIG_PATH="${TRAEFIK_CONNECTOR_CONFIG:-$CONNECTOR_ROOT/config/traefik-forwardauth.conf}"

if [ ! -x "$CONNECTOR_BIN" ]; then
    echo "BLOCKED: Traefik forwardAuth connector binary is not executable: $CONNECTOR_BIN" >&2
    echo "Hint: run make -C connectors/traefik build-connector first." >&2
    exit 77
fi
if [ ! -f "$CONFIG_PATH" ]; then
    echo "BLOCKED: Traefik forwardAuth connector config is missing: $CONFIG_PATH" >&2
    exit 77
fi

cd "$REPO_ROOT"
exec "$CONNECTOR_BIN" --check-config --config "$CONFIG_PATH"
