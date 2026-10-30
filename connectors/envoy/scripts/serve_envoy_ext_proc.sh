#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
CONNECTOR_DIR=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
BUILD_ROOT=${BUILD_ROOT:-${XDG_STATE_HOME:-${HOME:-/tmp}/.local/state}/ModSecurity-conector-build}
EXT_PROC_BIN=${EXT_PROC_BIN:-$BUILD_ROOT/envoy-ext-proc/msconnector_envoy_ext_proc}
EXT_PROC_CONFIG=${EXT_PROC_CONFIG:-$CONNECTOR_DIR/config/envoy-ext-proc-service.json}
EXT_PROC_RUNTIME_CONFIG=${EXT_PROC_RUNTIME_CONFIG:-}
EVENT_LOG_PATH=${EVENT_LOG_PATH:-$BUILD_ROOT/envoy-ext-proc/events.jsonl}
LISTEN_ADDRESS=${LISTEN_ADDRESS:-127.0.0.1}
LISTEN_PORT=${LISTEN_PORT:-18083}

while [ "$#" -gt 0 ]; do
    case "$1" in
        --config) EXT_PROC_CONFIG=${2:?--config requires a path}; shift 2 ;;
        --runtime-config) EXT_PROC_RUNTIME_CONFIG=${2:?--runtime-config requires a path}; shift 2 ;;
        --event-path) EVENT_LOG_PATH=${2:?--event-path requires a path}; shift 2 ;;
        --listen) LISTEN_ADDRESS=${2%%:*}; LISTEN_PORT=${2##*:}; shift 2 ;;
        --help)
            echo "usage: $0 [--config PATH] [--runtime-config PATH] [--event-path PATH] [--listen HOST:PORT]"
            exit 0
            ;;
        *) echo "envoy_ext_proc_service: unsupported argument: $1" >&2; exit 2 ;;
    esac
done

[ -x "$EXT_PROC_BIN" ] || {
    echo "envoy_ext_proc_service: service is not executable: $EXT_PROC_BIN" >&2
    exit 77
}
[ -f "$EXT_PROC_CONFIG" ] || {
    echo "envoy_ext_proc_service: config is missing: $EXT_PROC_CONFIG" >&2
    exit 77
}
[ -n "$EXT_PROC_RUNTIME_CONFIG" ] || {
    echo "envoy_ext_proc_service: Common runtime config is required" >&2
    exit 77
}
[ -f "$EXT_PROC_RUNTIME_CONFIG" ] || {
    echo "envoy_ext_proc_service: Common runtime config is missing: $EXT_PROC_RUNTIME_CONFIG" >&2
    exit 77
}
case "$EVENT_LOG_PATH" in
    /*) ;;
    *) echo "envoy_ext_proc_service: event path must be absolute: $EVENT_LOG_PATH" >&2; exit 2 ;;
esac

exec "$EXT_PROC_BIN" --config "$EXT_PROC_CONFIG" \
    --runtime-config "$EXT_PROC_RUNTIME_CONFIG" \
    --listen "$LISTEN_ADDRESS:$LISTEN_PORT" --event-log "$EVENT_LOG_PATH"
