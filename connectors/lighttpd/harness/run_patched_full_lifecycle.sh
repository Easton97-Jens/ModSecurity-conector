#!/bin/sh
set -eu

# Exercise the patched Lighttpd 1.4.84 native module through its HTTP/1.1
# entity-body hook.  The P4 path is deliberately limited to identity entities
# proxied by mod_proxy; no H2/H3, compression, file, or zero-copy route is
# represented here.

SCRIPT_DIR=$(CDPATH='' cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH='' cd "$SCRIPT_DIR/../../.." && pwd)
FRAMEWORK_ROOT=${FRAMEWORK_ROOT:-$REPO_ROOT/modules/ModSecurity-test-Framework}
BUILD_ROOT=${BUILD_ROOT:-${XDG_STATE_HOME:-${HOME:-/tmp}/.local/state}/ModSecurity-conector-build}
PATCHED_ROOT=${LIGHTTPD_PATCHED_ROOT:-$BUILD_ROOT/lighttpd-core-patched}
CORE_BIN=$PATCHED_ROOT/stage/bin/lighttpd
MODULE_PATH=$PATCHED_ROOT/stage/modules/mod_msconnector.so
PROXY_MODULE_PATH=$PATCHED_ROOT/stage/modules/mod_proxy.so
HOST_MANIFEST=$PATCHED_ROOT/patched-host-build-info.txt
SMOKE_DIR=${LIGHTTPD_PATCHED_SMOKE_DIR:-$PATCHED_ROOT/smoke}
SMOKE_PORT=${LIGHTTPD_SMOKE_PORT:-18084}
RULES_FILE=${MSCONNECTOR_RULES_FILE:-${RULES_FILE:-$FRAMEWORK_ROOT/tests/rules/no-crs-baseline.conf}}
PYTHON_BIN=${PYTHON:-python3}
SYNCHRONIZED_UPSTREAM=$FRAMEWORK_ROOT/tests/runners/synchronized_upstream.py
ENTITY_FIXTURE_UPSTREAM=$SCRIPT_DIR/lighttpd_http1_entity_fixture_upstream.py
FIRST_BYTE_METADATA=$SCRIPT_DIR/write_patched_first_byte_metadata.py
RESULT_WRITER=$SCRIPT_DIR/write_patched_lifecycle_results.py
RESULTS_PATH=$SMOKE_DIR/results.jsonl
SUMMARY_PATH=$SMOKE_DIR/runtime-summary.txt
EVENT_PATH=$SMOKE_DIR/events.jsonl
ERROR_LOG=$SMOKE_DIR/lighttpd-error.log
SERVER_STDOUT=$SMOKE_DIR/runtime-smoke.stdout
SERVER_STDERR=$SMOKE_DIR/runtime-smoke.stderr
FIRST_BYTE_EVIDENCE=${FULL_LIFECYCLE_EVIDENCE_OUTPUT:-$SMOKE_DIR/first-byte-evidence.json}
FIRST_BYTE_DIR=$SMOKE_DIR/first-byte
FIXTURE_DIR=$SMOKE_DIR/entity-fixtures
P4_CONTENT_LENGTH_EVENTS=$SMOKE_DIR/phase4-content-length-events.jsonl
P4_CHUNKED_EVENTS=$SMOKE_DIR/phase4-chunked-events.jsonl
P4_BARRIER_EVENTS=$SMOKE_DIR/phase4-barrier-events.jsonl
P4_PROJECTED_EVENTS=$SMOKE_DIR/phase4-barrier-eos-events.jsonl
P4_SUMMARY_JSON=$SMOKE_DIR/phase4-safe-summary.json
SERVER_PID=
FIXTURE_PID=
BARRIER_PID=
BARRIER_RELEASE_FILE=

blocked() {
    printf 'lighttpd_patched_full_lifecycle: BLOCKED: %s\n' "$1" >&2
    exit 77
}

fail() {
    printf 'lighttpd_patched_full_lifecycle: FAIL %s\n' "$1" >&2
    exit 1
}

manifest_value() {
    key=$1
    sed -n "s/^$key=//p" "$HOST_MANIFEST" | sed -n '1p'
}

stop_child() {
    child_pid=$1
    [ -n "$child_pid" ] || return 0
    if kill -0 "$child_pid" 2>/dev/null; then
        kill -TERM "$child_pid" 2>/dev/null || true
    fi
    wait "$child_pid" 2>/dev/null || true
}

cleanup() {
    if [ -n "$BARRIER_RELEASE_FILE" ]; then
        : > "$BARRIER_RELEASE_FILE" 2>/dev/null || true
    fi
    stop_child "$SERVER_PID"
    stop_child "$FIXTURE_PID"
    stop_child "$BARRIER_PID"
}
trap cleanup EXIT HUP INT TERM

wait_for_file() {
    path=$1
    label=$2
    child_pid=$3
    attempt=0
    while [ "$attempt" -lt 30 ]; do
        [ -f "$path" ] && return 0
        if ! kill -0 "$child_pid" 2>/dev/null; then
            blocked "$label exited before publishing its control record"
        fi
        attempt=$((attempt + 1))
        sleep 1
    done
    blocked "$label did not publish its control record"
}

ready_port() {
    "$PYTHON_BIN" - "$1" <<'PY'
import json
import sys

value = json.load(open(sys.argv[1], encoding="utf-8"))
port = value.get("upstream_port")
if not isinstance(port, int) or isinstance(port, bool) or not 1 <= port <= 65535:
    raise SystemExit(1)
print(port)
PY
}

event_cursor() {
    if [ -f "$EVENT_PATH" ]; then
        awk 'END { print NR + 0 }' "$EVENT_PATH"
    else
        printf '0\n'
    fi
}

snapshot_events() {
    first_line=$1
    destination=$2
    last_line=$(event_cursor)
    : > "$destination"
    if [ "$last_line" -gt "$first_line" ]; then
        sed -n "$((first_line + 1)),$last_line p" "$EVENT_PATH" > "$destination"
    fi
}

case "$SMOKE_DIR" in
    /*) ;;
    *) blocked "LIGHTTPD_PATCHED_SMOKE_DIR must be absolute" ;;
esac
case "$RULES_FILE" in
    /*) ;;
    *) blocked "MSCONNECTOR_RULES_FILE must be absolute" ;;
esac
case "$FIRST_BYTE_EVIDENCE" in
    /*) ;;
    *) blocked "FULL_LIFECYCLE_EVIDENCE_OUTPUT must be absolute" ;;
esac
[ -f "$RULES_FILE" ] || blocked "canonical rules file is missing: $RULES_FILE"
[ -x "$CORE_BIN" ] || blocked "patched lighttpd binary is missing: $CORE_BIN"
[ -f "$MODULE_PATH" ] || blocked "patched module is missing: $MODULE_PATH"
[ -f "$PROXY_MODULE_PATH" ] || blocked "patched mod_proxy module is missing: $PROXY_MODULE_PATH"
[ -f "$HOST_MANIFEST" ] || blocked "patched host manifest is missing: $HOST_MANIFEST"
[ -f "$SYNCHRONIZED_UPSTREAM" ] || blocked "synchronized upstream helper is missing: $SYNCHRONIZED_UPSTREAM"
[ -f "$ENTITY_FIXTURE_UPSTREAM" ] || blocked "HTTP/1.1 entity fixture helper is missing"
[ -f "$FIRST_BYTE_METADATA" ] || blocked "Lighttpd first-byte metadata helper is missing"
[ -f "$RESULT_WRITER" ] || blocked "Lighttpd result writer is missing"
command -v curl >/dev/null 2>&1 || blocked "curl is required"
command -v "$PYTHON_BIN" >/dev/null 2>&1 || blocked "python3 is required"

MODSECURITY_LIB_DIR=$(manifest_value modsecurity_lib_dir)
[ -n "$MODSECURITY_LIB_DIR" ] || blocked "patched host manifest has no libmodsecurity directory"
[ -f "$MODSECURITY_LIB_DIR/libmodsecurity.so" ] || blocked "libmodsecurity is missing"

mkdir -p "$SMOKE_DIR" "$FIRST_BYTE_DIR" "$FIXTURE_DIR"
for generated in \
    "$FIRST_BYTE_DIR/upstream-ready.json" \
    "$FIRST_BYTE_DIR/upstream-paused.json" \
    "$FIRST_BYTE_DIR/upstream-release" \
    "$FIRST_BYTE_DIR/upstream-server.json" \
    "$FIRST_BYTE_DIR/client-body.bin" \
    "$FIRST_BYTE_DIR/host-metadata.json" \
    "$FIXTURE_DIR/upstream-ready.json" \
    "$FIXTURE_DIR/result.json"; do
    rm -f "$generated"
done

"$PYTHON_BIN" "$ENTITY_FIXTURE_UPSTREAM" \
    --ready-file "$FIXTURE_DIR/upstream-ready.json" \
    --result-file "$FIXTURE_DIR/result.json" \
    --timeout 30 >"$FIXTURE_DIR/upstream.stdout" \
    2>"$FIXTURE_DIR/upstream.stderr" &
FIXTURE_PID=$!
wait_for_file "$FIXTURE_DIR/upstream-ready.json" "HTTP/1.1 entity fixture" "$FIXTURE_PID"
FIXTURE_PORT=$(ready_port "$FIXTURE_DIR/upstream-ready.json") || \
    blocked "HTTP/1.1 entity fixture ready record has no valid port"

BARRIER_RELEASE_FILE=$FIRST_BYTE_DIR/upstream-release
"$PYTHON_BIN" "$SYNCHRONIZED_UPSTREAM" --serve \
    --ready-file "$FIRST_BYTE_DIR/upstream-ready.json" \
    --paused-file "$FIRST_BYTE_DIR/upstream-paused.json" \
    --release-file "$BARRIER_RELEASE_FILE" \
    --server-evidence-file "$FIRST_BYTE_DIR/upstream-server.json" \
    --timeout 30 >"$FIRST_BYTE_DIR/upstream.stdout" \
    2>"$FIRST_BYTE_DIR/upstream.stderr" &
BARRIER_PID=$!
wait_for_file "$FIRST_BYTE_DIR/upstream-ready.json" "synchronized upstream" "$BARRIER_PID"
BARRIER_PORT=$(ready_port "$FIRST_BYTE_DIR/upstream-ready.json") || \
    blocked "synchronized upstream ready record has no valid port"

LIGHTTPD_CONFIG=$( \
    LIGHTTPD_PATCHED_ROOT="$PATCHED_ROOT" \
    LIGHTTPD_PATCHED_SMOKE_DIR="$SMOKE_DIR" \
    LIGHTTPD_SMOKE_PORT="$SMOKE_PORT" \
    LIGHTTPD_PATCHED_REQUEST_BODY_MODE=streaming \
    LIGHTTPD_PATCHED_RESPONSE_BODY_MODE=streaming \
    LIGHTTPD_PATCHED_RESPONSE_HEADER_MARKER=block \
    LIGHTTPD_PROXY_BARRIER_PORT="$BARRIER_PORT" \
    LIGHTTPD_PROXY_FIXTURE_PORT="$FIXTURE_PORT" \
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
    fail "config-load"
fi

: > "$ERROR_LOG"
"$CORE_BIN" -D -m "$MODULE_DIR" -f "$LIGHTTPD_CONFIG" \
    >"$SERVER_STDOUT" 2>"$SERVER_STDERR" &
SERVER_PID=$!
server_ready=0
for attempt in 1 2 3 4 5 6 7 8 9 10; do
    if curl --silent --show-error --connect-timeout 1 --output /dev/null \
        "http://127.0.0.1:$SMOKE_PORT/"; then
        server_ready=1
        break
    fi
    sleep 1
done
[ "$server_ready" -eq 1 ] || {
    sed -n '1,200p' "$SERVER_STDERR" >&2
    fail "process did not become ready"
}
kill -0 "$SERVER_PID" 2>/dev/null || {
    sed -n '1,200p' "$SERVER_STDERR" >&2
    fail "process did not remain alive"
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

[ "$allow_status" = 200 ] || fail "allow_status=$allow_status expected=200"
[ "$deny_status" = 403 ] || fail "deny_status=$deny_status expected=403"
[ "$alternative_status" = 429 ] || fail "alternative_status=$alternative_status expected=429"
[ "$request_body_status" = 403 ] || fail "request_body_status=$request_body_status expected=403"
[ "$response_header_status" = 403 ] || fail "response_header_status=$response_header_status expected=403"

content_length_cursor=$(event_cursor)
content_length_status=$(curl --http1.1 --silent --show-error --no-buffer \
    --dump-header "$FIXTURE_DIR/content-length.headers" --output /dev/null --write-out '%{http_code}' \
    --header 'X-Modsec-Transaction-Id: lighttpd-p4-content-length' \
    "http://127.0.0.1:$SMOKE_PORT/p4/fixture/content-length")
snapshot_events "$content_length_cursor" "$P4_CONTENT_LENGTH_EVENTS"
[ "$content_length_status" = 200 ] || fail "Content-Length entity status=$content_length_status expected=200"
grep -Eqi '^Content-Length:[[:space:]]*[0-9]+' "$FIXTURE_DIR/content-length.headers" || \
    fail "Content-Length entity response lost its Content-Length boundary"
if grep -Eqi '^Transfer-Encoding:[[:space:]]*chunked' "$FIXTURE_DIR/content-length.headers"; then
    fail "Content-Length entity response was relabelled as chunked"
fi

chunked_cursor=$(event_cursor)
chunked_status=$(curl --http1.1 --silent --show-error --no-buffer \
    --dump-header "$FIXTURE_DIR/chunked.headers" --output /dev/null --write-out '%{http_code}' \
    --header 'X-Modsec-Transaction-Id: lighttpd-p4-chunked' \
    "http://127.0.0.1:$SMOKE_PORT/p4/fixture/chunked")
snapshot_events "$chunked_cursor" "$P4_CHUNKED_EVENTS"
[ "$chunked_status" = 200 ] || fail "chunked entity status=$chunked_status expected=200"
grep -Eqi '^Transfer-Encoding:[[:space:]]*chunked' "$FIXTURE_DIR/chunked.headers" || \
    fail "chunked entity response lost its chunked boundary"

if ! wait "$FIXTURE_PID"; then
    sed -n '1,200p' "$FIXTURE_DIR/upstream.stderr" >&2
    fail "HTTP/1.1 entity fixture failed"
fi
FIXTURE_PID=

barrier_cursor=$(event_cursor)
: > "$FIRST_BYTE_DIR/client-body.bin"
curl --http1.1 --silent --show-error --no-buffer --output "$FIRST_BYTE_DIR/client-body.bin" \
    --write-out '%{http_code}' \
    --header 'X-Modsec-Transaction-Id: lighttpd-p4-barrier' \
    "http://127.0.0.1:$SMOKE_PORT/p4/barrier/first-byte" \
    >"$FIRST_BYTE_DIR/client-status.txt" 2>"$FIRST_BYTE_DIR/client.stderr" &
FIRST_BYTE_CLIENT_PID=$!
first_byte_observed=0
attempt=0
while [ "$attempt" -lt 300 ]; do
    if [ -f "$FIRST_BYTE_DIR/upstream-paused.json" ] && \
       [ -s "$FIRST_BYTE_DIR/client-body.bin" ]; then
        first_byte_observed=1
        break
    fi
    if ! kill -0 "$FIRST_BYTE_CLIENT_PID" 2>/dev/null; then
        break
    fi
    attempt=$((attempt + 1))
    sleep 0.1
done
: > "$BARRIER_RELEASE_FILE"
if ! wait "$FIRST_BYTE_CLIENT_PID"; then
    sed -n '1,120p' "$FIRST_BYTE_DIR/client.stderr" >&2
    fail "synchronized HTTP/1.1 client failed after upstream release"
fi
[ "$first_byte_observed" -eq 1 ] || fail "client did not receive a first body byte while upstream was paused"
phase4_safe_status=$(cat "$FIRST_BYTE_DIR/client-status.txt" 2>/dev/null || true)
[ "$phase4_safe_status" = 200 ] || fail "synchronized safe response status=$phase4_safe_status expected=200"
snapshot_events "$barrier_cursor" "$P4_BARRIER_EVENTS"
[ -s "$P4_BARRIER_EVENTS" ] || fail "synchronized barrier produced no P4 host event"

"$PYTHON_BIN" "$FIRST_BYTE_METADATA" \
    --events "$P4_BARRIER_EVENTS" --output "$FIRST_BYTE_DIR/host-metadata.json" || \
    fail "could not derive bounded Lighttpd P4 metadata"
"$PYTHON_BIN" "$SYNCHRONIZED_UPSTREAM" --merge-evidence \
    --paused-file "$FIRST_BYTE_DIR/upstream-paused.json" \
    --client-first-byte-file "$FIRST_BYTE_DIR/client-body.bin" \
    --host-metadata-json "$FIRST_BYTE_DIR/host-metadata.json" \
    --evidence-origin real_host \
    --output "$FIRST_BYTE_EVIDENCE" || \
    fail "could not write payload-free synchronized first-byte evidence"
rm -f "$FIRST_BYTE_DIR/client-body.bin"
if ! wait "$BARRIER_PID"; then
    sed -n '1,200p' "$FIRST_BYTE_DIR/upstream.stderr" >&2
    fail "synchronized upstream failed"
fi
BARRIER_PID=
BARRIER_RELEASE_FILE=

[ -s "$EVENT_PATH" ] || fail "no Common event was emitted"
"$PYTHON_BIN" "$RESULT_WRITER" \
    --events "$EVENT_PATH" \
    --output "$RESULTS_PATH" \
    --selected-case-ids "${NO_CRS_SELECTED_CASE_IDS:-}" \
    --allow-status "$allow_status" \
    --deny-status "$deny_status" \
    --alternative-status "$alternative_status" \
    --request-body-status "$request_body_status" \
    --response-header-status "$response_header_status" \
    --phase4-safe-events "$P4_BARRIER_EVENTS" \
    --phase4-projected-events-output "$P4_PROJECTED_EVENTS" \
    --phase4-safe-status "$phase4_safe_status" \
    --phase4-first-byte-evidence "$FIRST_BYTE_EVIDENCE" \
    --content-length-events "$P4_CONTENT_LENGTH_EVENTS" \
    --chunked-events "$P4_CHUNKED_EVENTS" \
    --entity-fixture-result "$FIXTURE_DIR/result.json" \
    --phase4-summary-output "$P4_SUMMARY_JSON"
if grep -Fq '"status": "FAIL"' "$RESULTS_PATH"; then
    fail "a host-confirmed case result did not match"
fi
if grep -Eq 'msconnector (request-body|response-body) finalization failed|host-action event was not recorded' "$ERROR_LOG"; then
    sed -n '1,200p' "$ERROR_LOG" >&2
    fail "runtime lifecycle error"
fi

{
    printf 'status=PASS\n'
    printf 'requests_sent=true\n'
    printf 'runtime_verified=true\n'
    printf 'rule_evaluation=libmodsecurity_host_runtime\n'
    printf 'allowed_request_status=%s\n' "$allow_status"
    printf 'blocked_request_status=%s\n' "$deny_status"
    printf 'alternative_status=%s\n' "$alternative_status"
    printf 'request_body_status=%s\n' "$request_body_status"
    printf 'response_header_status=%s\n' "$response_header_status"
    "$PYTHON_BIN" - "$P4_SUMMARY_JSON" <<'PY'
import json
import sys

value = json.load(open(sys.argv[1], encoding="utf-8"))
for key in (
    "phase4_safe_status",
    "p4_safe_log_only_status",
    "phase4_end_of_stream_evaluation_status",
    "phase4_first_byte_before_response_end_status",
    "phase4_no_full_response_buffering_status",
    "phase4_rule_id",
    "phase4_requested_action",
    "phase4_actual_action",
    "phase4_late_intervention",
    "phase4_late_intervention_mode",
    "phase4_headers_sent",
    "phase4_body_started",
    "phase4_response_committed",
    "phase4_connection_aborted",
    "phase4_transport_result",
    "phase4_entity_eos_finalized_once",
    "phase4_host_action_events",
    "http1_content_length_entity_bytes",
    "http1_chunked_entity_bytes",
):
    item = value[key]
    if isinstance(item, bool):
        item = str(item).lower()
    print(f"{key}={item}")
PY
    printf 'first_byte_evidence=%s\n' "$FIRST_BYTE_EVIDENCE"
    printf 'phase4_barrier_events=%s\n' "$P4_PROJECTED_EVENTS"
    printf 'content_length_events=%s\n' "$P4_CONTENT_LENGTH_EVENTS"
    printf 'chunked_events=%s\n' "$P4_CHUNKED_EVENTS"
    printf 'events=%s\n' "$EVENT_PATH"
    printf 'results=%s\n' "$RESULTS_PATH"
} > "$SUMMARY_PATH"

if kill -0 "$SERVER_PID" 2>/dev/null; then
    kill -TERM "$SERVER_PID" 2>/dev/null || true
fi
server_status=0
set +e
wait "$SERVER_PID"
server_status=$?
set -e
if [ "$server_status" -ne 0 ] && [ "$server_status" -ne 143 ]; then
    fail "shutdown status=$server_status"
fi
SERVER_PID=
trap - EXIT HUP INT TERM

printf 'lighttpd_patched_full_lifecycle: PASS allow=%s deny=%s alternative=%s p2=%s p3=%s p4-safe=%s results=%s\n' \
    "$allow_status" "$deny_status" "$alternative_status" "$request_body_status" \
    "$response_header_status" "$phase4_safe_status" "$RESULTS_PATH"
