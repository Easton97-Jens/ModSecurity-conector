#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH='' cd "$(dirname "$0")" && pwd)
CONNECTOR_DIR=$(CDPATH='' cd "$SCRIPT_DIR/.." && pwd)
REPO_ROOT=$(CDPATH='' cd "$CONNECTOR_DIR/../.." && pwd)
BUILD_ROOT=${BUILD_ROOT:-${XDG_STATE_HOME:-${HOME:-/tmp}/.local/state}/ModSecurity-conector-build}
SMOKE_DIR=${LIGHTTPD_SMOKE_DIR:-$BUILD_ROOT/lighttpd-connector/smoke}
SMOKE_PORT=${LIGHTTPD_SMOKE_PORT:-18084}
RULES_FILE=${MSCONNECTOR_RULES_FILE:-$REPO_ROOT/common/rules/modsecurity_targeted_smoke.conf}
RUNTIME_CONFIG=$SMOKE_DIR/msconnector-runtime.conf
LIGHTTPD_CONFIG=$SMOKE_DIR/lighttpd.conf
EVENT_PATH=$SMOKE_DIR/events.jsonl

blocked() {
    printf 'lighttpd_native_smoke_config: BLOCKED: %s\n' "$1" >&2
    exit 77
}

case "$BUILD_ROOT" in
    /*) ;;
    *) blocked "BUILD_ROOT must be absolute: $BUILD_ROOT" ;;
esac
case "$SMOKE_DIR" in
    /*) ;;
    *) blocked "LIGHTTPD_SMOKE_DIR must be absolute: $SMOKE_DIR" ;;
esac
case "$SMOKE_PORT" in
    ''|*[!0-9]*) blocked "LIGHTTPD_SMOKE_PORT must be numeric" ;;
    *) ;;
esac
if [ "$SMOKE_PORT" -lt 1024 ] || [ "$SMOKE_PORT" -gt 65535 ]; then
    blocked "LIGHTTPD_SMOKE_PORT must be between 1024 and 65535"
fi
[ -f "$RULES_FILE" ] || blocked "smoke rules file is missing: $RULES_FILE"

mkdir -p "$SMOKE_DIR/document-root" "$SMOKE_DIR/upload"
: > "$EVENT_PATH"
printf '%s\n' 'lighttpd native connector smoke' > "$SMOKE_DIR/document-root/index.html"

{
    printf 'enabled=on\n'
    printf 'rules_file=%s\n' "$RULES_FILE"
    printf 'transaction_id_header=x-request-id\n'
    printf 'request_body_mode=none\n'
    printf 'response_body_mode=none\n'
    printf 'request_body_limit=1048576\n'
    printf 'response_body_limit=1048576\n'
    printf 'default_block_status=403\n'
    printf 'default_error_status=500\n'
    printf 'max_header_count=256\n'
    printf 'max_header_name_size=256\n'
    printf 'max_header_value_size=8192\n'
    printf 'max_total_header_bytes=65536\n'
    printf 'max_event_json_bytes=16384\n'
    printf 'event_path=%s\n' "$EVENT_PATH"
} > "$RUNTIME_CONFIG"

escape_lighttpd_string() {
    printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'
}

DOCUMENT_ROOT_ESCAPED=$(escape_lighttpd_string "$SMOKE_DIR/document-root")
ERROR_LOG_ESCAPED=$(escape_lighttpd_string "$SMOKE_DIR/lighttpd-error.log")
PID_FILE_ESCAPED=$(escape_lighttpd_string "$SMOKE_DIR/lighttpd.pid")
UPLOAD_DIR_ESCAPED=$(escape_lighttpd_string "$SMOKE_DIR/upload")
RUNTIME_CONFIG_ESCAPED=$(escape_lighttpd_string "$RUNTIME_CONFIG")

{
    printf 'server.compat-module-load = "disable"\n'
    printf 'server.modules = ( "mod_msconnector" )\n'
    printf 'server.document-root = "%s"\n' "$DOCUMENT_ROOT_ESCAPED"
    printf 'server.bind = "127.0.0.1"\n'
    printf 'server.port = %s\n' "$SMOKE_PORT"
    printf 'server.errorlog = "%s"\n' "$ERROR_LOG_ESCAPED"
    printf 'server.pid-file = "%s"\n' "$PID_FILE_ESCAPED"
    printf 'server.upload-dirs = ( "%s" )\n' "$UPLOAD_DIR_ESCAPED"
    printf 'msconnector.enabled = "enable"\n'
    printf 'msconnector.config-file = "%s"\n' "$RUNTIME_CONFIG_ESCAPED"
} > "$LIGHTTPD_CONFIG"

printf '%s\n' "$LIGHTTPD_CONFIG"
