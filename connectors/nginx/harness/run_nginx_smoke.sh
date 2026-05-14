#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd "$SCRIPT_DIR/../../.." && pwd)
BUILD_ROOT="${BUILD_ROOT:-/src/ModSecurity-conector-build}"
NGINX_BUILD_DIR="${NGINX_BUILD_DIR:-$BUILD_ROOT/nginx-build}"
NGINX_PREFIX="${NGINX_PREFIX:-$BUILD_ROOT/nginx-runtime/nginx}"
NGINX_BINARY="${NGINX_BINARY:-$NGINX_PREFIX/sbin/nginx}"
NGINX_MODULE="${NGINX_MODULE:-$NGINX_PREFIX/modules/ngx_http_modsecurity_module.so}"
MODSECURITY_LIB_DIR="${MODSECURITY_LIB_DIR:-$NGINX_BUILD_DIR/output/modsecurity/lib}"
LOG_DIR="${LOG_DIR:-$BUILD_ROOT/logs/nginx-runtime}"
RUNTIME_ROOT="${RUNTIME_ROOT:-$BUILD_ROOT/nginx-runtime/phase2_args_block}"
CURL_BIN="${CURL:-}"
PYTHON_BIN="${PYTHON:-python3}"
PORT="${PORT:-18081}"
TEMPLATE="$SCRIPT_DIR/nginx_smoke.conf"
TEST_CASE="$REPO_ROOT/tests/common/cases/minimal/phase2_args_block.yaml"
CASE_CLI="$REPO_ROOT/tests/runners/case_cli.py"
STATUS_FILE="$LOG_DIR/status.txt"

blocked() {
    echo "nginx_smoke: blocked $*"
    mkdir -p "$LOG_DIR"
    echo "blocked: $*" >> "$STATUS_FILE"
    exit 77
}

fail() {
    echo "nginx_smoke: fail $*"
    mkdir -p "$LOG_DIR"
    echo "fail: $*" >> "$STATUS_FILE"
    exit 1
}

require_absolute_generated_path() {
    path=$1
    label=$2
    case "$path" in
        /*) ;;
        *) blocked "$label must be absolute: $path" ;;
    esac
    case "$path" in
        "$REPO_ROOT"|"$REPO_ROOT"/*|/root/conecter/*)
            blocked "$label is inside a read-only or source checkout: $path"
            ;;
    esac
}

find_curl() {
    if [ -n "$CURL_BIN" ]; then
        printf '%s\n' "$CURL_BIN"
        return 0
    fi
    command -v curl 2>/dev/null || true
}

escape_sed() {
    printf '%s' "$1" | sed 's/[&|]/\\&/g'
}

render_config() {
    sed \
        -e "s|@@RUNTIME_ROOT@@|$(escape_sed "$RUNTIME_ROOT")|g" \
        -e "s|@@LOG_DIR@@|$(escape_sed "$LOG_DIR")|g" \
        -e "s|@@PORT@@|$(escape_sed "$PORT")|g" \
        -e "s|@@NGINX_MODULE@@|$(escape_sed "$NGINX_MODULE")|g" \
        -e "s|@@DOCROOT@@|$(escape_sed "$DOCROOT")|g" \
        -e "s|@@RULES_FILE@@|$(escape_sed "$RULES_FILE")|g" \
        "$TEMPLATE" > "$CONFIG_FILE"
}

cleanup() {
    if [ -n "${NGINX_PID:-}" ] && kill -0 "$NGINX_PID" >/dev/null 2>&1; then
        kill "$NGINX_PID" >/dev/null 2>&1 || true
        wait "$NGINX_PID" >/dev/null 2>&1 || true
    fi
}

echo "nginx_smoke: BUILD_ROOT=$BUILD_ROOT"
echo "nginx_smoke: NGINX_BUILD_DIR=$NGINX_BUILD_DIR"
echo "nginx_smoke: NGINX_PREFIX=$NGINX_PREFIX"
echo "nginx_smoke: NGINX_BINARY=$NGINX_BINARY"
echo "nginx_smoke: NGINX_MODULE=$NGINX_MODULE"
echo "nginx_smoke: RUNTIME_ROOT=$RUNTIME_ROOT"
echo "nginx_smoke: LOG_DIR=$LOG_DIR"
echo "nginx_smoke: TEST_CASE=$TEST_CASE"

require_absolute_generated_path "$BUILD_ROOT" "BUILD_ROOT"
require_absolute_generated_path "$NGINX_BUILD_DIR" "NGINX_BUILD_DIR"
require_absolute_generated_path "$NGINX_PREFIX" "NGINX_PREFIX"
require_absolute_generated_path "$RUNTIME_ROOT" "RUNTIME_ROOT"
require_absolute_generated_path "$LOG_DIR" "LOG_DIR"

mkdir -p "$LOG_DIR" "$RUNTIME_ROOT/conf" "$RUNTIME_ROOT/htdocs" \
    "$RUNTIME_ROOT/client_body_temp" "$RUNTIME_ROOT/proxy_temp" \
    "$RUNTIME_ROOT/fastcgi_temp" "$RUNTIME_ROOT/uwsgi_temp" \
    "$RUNTIME_ROOT/scgi_temp"
rm -f "$LOG_DIR/configtest.log" \
    "$LOG_DIR/curl-attack.err" \
    "$LOG_DIR/curl-ready.err" \
    "$LOG_DIR/nginx.log" \
    "$LOG_DIR/nginx-stdout.log" \
    "$LOG_DIR/response-body.txt" \
    "$RUNTIME_ROOT/nginx.pid"
: > "$STATUS_FILE"

CURL_BIN=$(find_curl)

[ -x "$NGINX_BINARY" ] || blocked "missing executable NGINX binary: $NGINX_BINARY"
[ -f "$NGINX_MODULE" ] || blocked "missing NGINX ModSecurity dynamic module: $NGINX_MODULE"
[ -n "$CURL_BIN" ] || blocked "missing curl; set CURL=/path/to/curl"
[ -x "$CURL_BIN" ] || blocked "curl is not executable: $CURL_BIN"
[ -f "$MODSECURITY_LIB_DIR/libmodsecurity.so" ] || blocked "missing staged libmodsecurity.so: $MODSECURITY_LIB_DIR/libmodsecurity.so"

CONFIG_FILE="$RUNTIME_ROOT/conf/nginx.conf"
RULES_FILE="$RUNTIME_ROOT/conf/modsecurity-smoke.conf"
DOCROOT="$RUNTIME_ROOT/htdocs"
RESPONSE_BODY="$LOG_DIR/response-body.txt"
CASE_ENV_FILE="$RUNTIME_ROOT/conf/case.env"

echo "TEST-OK-IF-YOU-SEE-THIS" > "$DOCROOT/index.html"
if ! "$PYTHON_BIN" "$CASE_CLI" materialize \
    --case "$TEST_CASE" \
    --rules-file "$RULES_FILE" \
    --env-file "$CASE_ENV_FILE" > "$LOG_DIR/case-materialize.log" 2>&1; then
    blocked "failed to materialize shared case; see $LOG_DIR/case-materialize.log"
fi
. "$CASE_ENV_FILE"

render_config

LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR:$NGINX_PREFIX/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH

if ! "$NGINX_BINARY" -t -p "$RUNTIME_ROOT" -c "$CONFIG_FILE" > "$LOG_DIR/configtest.log" 2>&1; then
    fail "NGINX configtest failed; see $LOG_DIR/configtest.log"
fi

trap cleanup EXIT INT TERM
"$NGINX_BINARY" -p "$RUNTIME_ROOT" -c "$CONFIG_FILE" > "$LOG_DIR/nginx-stdout.log" 2>&1 &
NGINX_PID=$!

ready=0
i=0
while [ "$i" -lt 30 ]; do
    if ! kill -0 "$NGINX_PID" >/dev/null 2>&1; then
        fail "NGINX exited before request; see $LOG_DIR/nginx-stdout.log and $LOG_DIR/error.log"
    fi
    if "$CURL_BIN" -sS -o /dev/null "http://127.0.0.1:$PORT/" >/dev/null 2>"$LOG_DIR/curl-ready.err"; then
        ready=1
        break
    fi
    i=$((i + 1))
    sleep 1
done

[ "$ready" -eq 1 ] || fail "NGINX did not become ready on 127.0.0.1:$PORT"

set +e
http_status=$("$CURL_BIN" -sS -X "$REQUEST_METHOD" -o "$RESPONSE_BODY" -w "%{http_code}" "http://127.0.0.1:$PORT$REQUEST_PATH" 2>"$LOG_DIR/curl-attack.err")
curl_rc=$?
set -e

if [ "$curl_rc" -ne 0 ]; then
    fail "curl attack request failed rc=$curl_rc; see $LOG_DIR/curl-attack.err"
fi

if "$PYTHON_BIN" "$CASE_CLI" assert-status \
    --case "$TEST_CASE" \
    --actual-status "$http_status" \
    --status-file "$STATUS_FILE" > "$LOG_DIR/case-assert.log" 2>&1; then
    echo "nginx_smoke: pass status=$http_status"
    exit 0
fi

echo "nginx_smoke: fail observed=$http_status expected=$EXPECT_STATUS"
exit 1
