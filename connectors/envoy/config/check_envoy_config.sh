#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
CONNECTOR_DIR=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
BUILD_ROOT=${BUILD_ROOT:-${XDG_STATE_HOME:-${HOME:-/tmp}/.local/state}/ModSecurity-conector-build}
SERVICE_BIN=${SERVICE_BIN:-$BUILD_ROOT/envoy-connector/msconnector_envoy_ext_authz}
CONFIG_FILE=${CONFIG_FILE:-$SCRIPT_DIR/envoy-ext-authz.conf}
RULES_FILE=${RULES_FILE:-$CONNECTOR_DIR/../../common/rules/modsecurity_targeted_smoke.conf}
EVENT_LOG_PATH=${EVENT_LOG_PATH:-$BUILD_ROOT/envoy-connector/events.jsonl}

while [ "$#" -gt 0 ]; do
    case "$1" in
        --config) CONFIG_FILE=${2:?--config requires a path}; shift 2 ;;
        --rules-file) RULES_FILE=${2:?--rules-file requires a path}; shift 2 ;;
        --event-path) EVENT_LOG_PATH=${2:?--event-path requires a path}; shift 2 ;;
        --help)
            echo "usage: $0 [--config PATH] [--rules-file PATH] [--event-path PATH]"
            exit 0
            ;;
        *) echo "envoy_config: unsupported argument: $1" >&2; exit 2 ;;
    esac
done

[ -x "$SERVICE_BIN" ] || {
    echo "envoy_config: connector service is not executable: $SERVICE_BIN" >&2
    exit 77
}

runtime_config=$(BUILD_ROOT="$BUILD_ROOT" CONFIG_FILE="$CONFIG_FILE" \
    RULES_FILE="$RULES_FILE" EVENT_LOG_PATH="$EVENT_LOG_PATH" \
    sh "$SCRIPT_DIR/prepare_envoy_config.sh")

"$SERVICE_BIN" --check-config --config "$runtime_config"
