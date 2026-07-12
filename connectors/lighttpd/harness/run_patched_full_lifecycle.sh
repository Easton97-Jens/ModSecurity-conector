#!/bin/sh
set -eu

# Execute only the Phase-1/2/3 cases that the patched lighttpd host can
# truthfully support.  The patched output hook observes HTTP/1 wire bytes, so
# Phase 4 remains deliberately out of this real-host runner.

SCRIPT_DIR=$(CDPATH='' cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH='' cd "$SCRIPT_DIR/../../.." && pwd)
FRAMEWORK_ROOT=${FRAMEWORK_ROOT:-$REPO_ROOT/modules/ModSecurity-test-Framework}
BUILD_ROOT=${BUILD_ROOT:-${XDG_STATE_HOME:-${HOME:-/tmp}/.local/state}/ModSecurity-conector-build}
PATCHED_ROOT=${LIGHTTPD_PATCHED_ROOT:-$BUILD_ROOT/lighttpd-core-patched}
CORE_BIN=$PATCHED_ROOT/stage/bin/lighttpd
MODULE_PATH=$PATCHED_ROOT/stage/modules/mod_msconnector.so
HOST_MANIFEST=$PATCHED_ROOT/patched-host-build-info.txt
SMOKE_DIR=${LIGHTTPD_PATCHED_SMOKE_DIR:-$PATCHED_ROOT/smoke}
SMOKE_PORT=${LIGHTTPD_SMOKE_PORT:-18084}
RULES_FILE=${MSCONNECTOR_RULES_FILE:-${RULES_FILE:-$FRAMEWORK_ROOT/tests/rules/no-crs-baseline.conf}}
RESULTS_PATH=$SMOKE_DIR/results.jsonl
SUMMARY_PATH=$SMOKE_DIR/runtime-summary.txt
EVENT_PATH=$SMOKE_DIR/events.jsonl
ERROR_LOG=$SMOKE_DIR/lighttpd-error.log
SERVER_STDOUT=$SMOKE_DIR/runtime-smoke.stdout
SERVER_STDERR=$SMOKE_DIR/runtime-smoke.stderr
SERVER_PID=

blocked() {
    printf 'lighttpd_patched_full_lifecycle: BLOCKED: %s\n' "$1" >&2
    exit 77
}

manifest_value() {
    key=$1
    sed -n "s/^$key=//p" "$HOST_MANIFEST" | sed -n '1p'
}

cleanup() {
    if [ -n "$SERVER_PID" ] && kill -0 "$SERVER_PID" 2>/dev/null; then
        kill -TERM "$SERVER_PID" 2>/dev/null || true
        wait "$SERVER_PID" 2>/dev/null || true
    fi
}
trap cleanup EXIT HUP INT TERM

case "$SMOKE_DIR" in
    /*) ;;
    *) blocked "LIGHTTPD_PATCHED_SMOKE_DIR must be absolute" ;;
esac
case "$RULES_FILE" in
    /*) ;;
    *) blocked "MSCONNECTOR_RULES_FILE must be absolute" ;;
esac
[ -f "$RULES_FILE" ] || blocked "canonical rules file is missing: $RULES_FILE"
[ -x "$CORE_BIN" ] || blocked "patched lighttpd binary is missing: $CORE_BIN"
[ -f "$MODULE_PATH" ] || blocked "patched module is missing: $MODULE_PATH"
[ -f "$HOST_MANIFEST" ] || blocked "patched host manifest is missing: $HOST_MANIFEST"
command -v curl >/dev/null 2>&1 || blocked "curl is required"
command -v python3 >/dev/null 2>&1 || blocked "python3 is required"

MODSECURITY_LIB_DIR=$(manifest_value modsecurity_lib_dir)
[ -n "$MODSECURITY_LIB_DIR" ] || blocked "patched host manifest has no libmodsecurity directory"
[ -f "$MODSECURITY_LIB_DIR/libmodsecurity.so" ] || blocked "libmodsecurity is missing"

LIGHTTPD_CONFIG=$( \
    LIGHTTPD_PATCHED_ROOT="$PATCHED_ROOT" \
    LIGHTTPD_PATCHED_SMOKE_DIR="$SMOKE_DIR" \
    LIGHTTPD_SMOKE_PORT="$SMOKE_PORT" \
    LIGHTTPD_PATCHED_REQUEST_BODY_MODE=streaming \
    LIGHTTPD_PATCHED_RESPONSE_BODY_MODE=none \
    LIGHTTPD_PATCHED_RESPONSE_HEADER_MARKER=block \
    MSCONNECTOR_RULES_FILE="$RULES_FILE" \
    sh "$SCRIPT_DIR/prepare_patched_lifecycle_smoke.sh"
)

LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH
MODULE_DIR=$(dirname "$MODULE_PATH")
if ! "$CORE_BIN" -m "$MODULE_DIR" -tt -f "$LIGHTTPD_CONFIG" \
    >"$SMOKE_DIR/runtime-config-check.stdout" \
    2>"$SMOKE_DIR/runtime-config-check.stderr"; then
    sed -n '1,200p' "$SMOKE_DIR/runtime-config-check.stderr" >&2
    printf 'lighttpd_patched_full_lifecycle: FAIL config-load\n' >&2
    exit 1
fi

: > "$ERROR_LOG"
"$CORE_BIN" -D -m "$MODULE_DIR" -f "$LIGHTTPD_CONFIG" \
    >"$SERVER_STDOUT" 2>"$SERVER_STDERR" &
SERVER_PID=$!
for attempt in 1 2 3 4 5 6 7 8 9 10; do
    if curl --silent --show-error --connect-timeout 1 --output /dev/null \
        "http://127.0.0.1:$SMOKE_PORT/"; then
        break
    fi
    sleep 1
done
kill -0 "$SERVER_PID" 2>/dev/null || {
    sed -n '1,200p' "$SERVER_STDERR" >&2
    printf 'lighttpd_patched_full_lifecycle: FAIL process did not remain alive\n' >&2
    exit 1
}

base_url=http://127.0.0.1:$SMOKE_PORT/
allow_status=$(curl --silent --show-error --output /dev/null --write-out '%{http_code}' \
    --request OPTIONS --request-target '*' \
    --header 'X-Modsec-Transaction-Id: lighttpd-p1-allow' "$base_url")
deny_status=$(curl --silent --show-error --output /dev/null --write-out '%{http_code}' \
    --request OPTIONS --request-target '*' \
    --header 'X-Modsec-Smoke: block' \
    --header 'X-Modsec-Transaction-Id: lighttpd-p1-deny' "$base_url")
alternative_status=$(curl --silent --show-error --output /dev/null --write-out '%{http_code}' \
    --request OPTIONS --request-target '*' \
    --header 'X-Modsec-Smoke: alternative-status' \
    --header 'X-Modsec-Transaction-Id: lighttpd-p1-alternative' "$base_url")
request_body_status=$(curl --silent --show-error --output /dev/null --write-out '%{http_code}' \
    --request OPTIONS --request-target '*' --data-binary 'no-crs-request-body-marker' \
    --header 'Content-Type: text/plain' \
    --header 'X-Modsec-Transaction-Id: lighttpd-p2-deny' "$base_url")
response_header_status=$(curl --silent --show-error --output /dev/null --write-out '%{http_code}' \
    --request OPTIONS \
    --header 'X-Modsec-Transaction-Id: lighttpd-p3-deny' \
    "http://127.0.0.1:$SMOKE_PORT/phase3-block")

[ "$allow_status" = 200 ] || {
    printf 'lighttpd_patched_full_lifecycle: FAIL allow_status=%s expected=200\n' "$allow_status" >&2
    exit 1
}
[ "$deny_status" = 403 ] || {
    printf 'lighttpd_patched_full_lifecycle: FAIL deny_status=%s expected=403\n' "$deny_status" >&2
    exit 1
}
[ "$alternative_status" = 429 ] || {
    printf 'lighttpd_patched_full_lifecycle: FAIL alternative_status=%s expected=429\n' "$alternative_status" >&2
    exit 1
}
[ "$request_body_status" = 403 ] || {
    printf 'lighttpd_patched_full_lifecycle: FAIL request_body_status=%s expected=403\n' "$request_body_status" >&2
    exit 1
}
[ "$response_header_status" = 403 ] || {
    printf 'lighttpd_patched_full_lifecycle: FAIL response_header_status=%s expected=403\n' "$response_header_status" >&2
    exit 1
}
[ -s "$EVENT_PATH" ] || {
    printf 'lighttpd_patched_full_lifecycle: FAIL no Common event was emitted\n' >&2
    exit 1
}

python3 "$SCRIPT_DIR/write_patched_lifecycle_results.py" \
    --events "$EVENT_PATH" \
    --output "$RESULTS_PATH" \
    --selected-case-ids "${NO_CRS_SELECTED_CASE_IDS:-}" \
    --allow-status "$allow_status" \
    --deny-status "$deny_status" \
    --alternative-status "$alternative_status" \
    --request-body-status "$request_body_status" \
    --response-header-status "$response_header_status"
if grep -Fq '"status": "FAIL"' "$RESULTS_PATH"; then
    printf 'lighttpd_patched_full_lifecycle: FAIL a host-confirmed case result did not match\n' >&2
    exit 1
fi
if grep -Eq 'msconnector (request-body|response-body) finalization failed|host-action event was not recorded' "$ERROR_LOG"; then
    sed -n '1,200p' "$ERROR_LOG" >&2
    printf 'lighttpd_patched_full_lifecycle: FAIL runtime lifecycle error\n' >&2
    exit 1
fi

{
    printf 'status=PASS\n'
    printf 'allowed_request_status=%s\n' "$allow_status"
    printf 'blocked_request_status=%s\n' "$deny_status"
    printf 'alternative_status=%s\n' "$alternative_status"
    printf 'request_body_status=%s\n' "$request_body_status"
    printf 'response_header_status=%s\n' "$response_header_status"
    printf 'events=%s\n' "$EVENT_PATH"
    printf 'results=%s\n' "$RESULTS_PATH"
    printf 'phase4=not_executed_decoded_entity_hook_unavailable\n'
} > "$SUMMARY_PATH"

kill -TERM "$SERVER_PID"
status=0
wait "$SERVER_PID" 2>/dev/null || status=$?
if [ "$status" -ne 0 ] && [ "$status" -ne 143 ]; then
    printf 'lighttpd_patched_full_lifecycle: FAIL shutdown status=%s\n' "$status" >&2
    exit 1
fi
SERVER_PID=
trap - EXIT HUP INT TERM

printf 'lighttpd_patched_full_lifecycle: PASS allow=%s deny=%s alternative=%s p2=%s p3=%s results=%s\n' \
    "$allow_status" "$deny_status" "$alternative_status" "$request_body_status" \
    "$response_header_status" "$RESULTS_PATH"
