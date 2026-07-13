#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
CONNECTOR_DIR=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
REPO_ROOT=$(CDPATH= cd "$CONNECTOR_DIR/../.." && pwd)
BUILD_ROOT=${BUILD_ROOT:-${XDG_STATE_HOME:-${HOME:-/tmp}/.local/state}/ModSecurity-conector-build}
RULES_FILE=${MSCONNECTOR_RULES_FILE:-${RULES_FILE:-$REPO_ROOT/modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf}}
OUTPUT_CONFIG=${OUTPUT_CONFIG:-$BUILD_ROOT/envoy-ext-proc/config/envoy-ext-proc-runtime.conf}
EVENT_PATH=${EVENT_PATH:-}

absolute_existing_file() {
    input=$1
    case "$input" in
        /*) candidate=$input ;;
        *) candidate=$(CDPATH= cd "$(dirname "$input")" && pwd)/$(basename "$input") ;;
    esac
    [ -f "$candidate" ] || return 1
    printf '%s\n' "$candidate"
}

absolute_path() {
    case "$1" in
        /*) printf '%s\n' "$1" ;;
        *) printf '%s/%s\n' "$(pwd)" "$1" ;;
    esac
}

RULES_FILE=$(absolute_existing_file "$RULES_FILE") || {
    echo "envoy_ext_proc_runtime_config: rules file is not available: $RULES_FILE" >&2
    exit 77
}
OUTPUT_CONFIG=$(absolute_path "$OUTPUT_CONFIG")
if [ -n "$EVENT_PATH" ]; then
    EVENT_PATH=$(absolute_path "$EVENT_PATH")
fi

case "$OUTPUT_CONFIG" in
    "$REPO_ROOT"|"$REPO_ROOT"/*)
        echo "envoy_ext_proc_runtime_config: generated runtime config must not be inside the checkout: $OUTPUT_CONFIG" >&2
        exit 2
        ;;
esac

mkdir -p "$(dirname "$OUTPUT_CONFIG")"
if [ -n "$EVENT_PATH" ]; then
    mkdir -p "$(dirname "$EVENT_PATH")"
fi
umask 077
{
    printf '%s\n' '# Generated outside the checkout for the real Envoy ext_proc bridge.'
    printf '%s\n' '# event_path, when supplied, is the Common Runtime raw decision JSONL.'
    printf '%s\n' 'enabled=on'
    printf 'rules_file=%s\n' "$RULES_FILE"
    printf '%s\n' 'transaction_id_header=x-request-id'
    printf '%s\n' 'request_body_mode=streaming'
    printf '%s\n' 'response_body_mode=streaming'
    printf '%s\n' 'request_body_limit=10485760'
    printf '%s\n' 'response_body_limit=10485760'
    printf '%s\n' 'body_limit_action=reject'
    printf '%s\n' 'phase4_mode=safe'
    printf '%s\n' 'default_block_status=403'
    printf '%s\n' 'default_error_status=500'
    printf '%s\n' 'use_error_log=off'
    printf '%s\n' 'max_header_count=128'
    printf '%s\n' 'max_header_name_size=256'
    printf '%s\n' 'max_header_value_size=8192'
    printf '%s\n' 'max_total_header_bytes=32768'
    printf '%s\n' 'max_event_json_bytes=16384'
    if [ -n "$EVENT_PATH" ]; then
        printf 'event_path=%s\n' "$EVENT_PATH"
    fi
} > "$OUTPUT_CONFIG"
chmod 600 "$OUTPUT_CONFIG"

printf '%s\n' "$OUTPUT_CONFIG"
