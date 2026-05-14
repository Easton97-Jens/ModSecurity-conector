#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd "$SCRIPT_DIR/../../.." && pwd)
BUILD_ROOT="${BUILD_ROOT:-/src/ModSecurity-conector-build}"
APACHE_BUILD_ROOT="${APACHE_BUILD_ROOT:-$BUILD_ROOT/apache-build}"
LOG_DIR="${LOG_DIR:-$BUILD_ROOT/logs/apache-runtime}"
RUNTIME_ROOT="${RUNTIME_ROOT:-$BUILD_ROOT/apache-runtime/phase2_args_block}"
MODSECURITY_V3_DIR="${MODSECURITY_V3_DIR:-$APACHE_BUILD_ROOT/ModSecurity_V3}"
MODSECURITY_LIB_DIR="${MODSECURITY_LIB_DIR:-$APACHE_BUILD_ROOT/output/modsecurity/lib}"
APACHE_MODULE="${APACHE_MODULE:-$APACHE_BUILD_ROOT/output/apache/mod_security3.so}"
APACHE_HTTPD_BIN="${APACHE_HTTPD:-${APACHE:-}}"
APXS_BIN="${APXS:-}"
CURL_BIN="${CURL:-}"
PORT="${PORT:-18080}"
TEMPLATE="$SCRIPT_DIR/apache_smoke.conf"
TEST_CASE="$REPO_ROOT/tests/common/cases/minimal/phase2_args_block.yaml"
STATUS_FILE="$LOG_DIR/status.txt"

blocked() {
    echo "apache_smoke: blocked $*"
    mkdir -p "$LOG_DIR"
    echo "blocked: $*" >> "$STATUS_FILE"
    exit 77
}

fail() {
    echo "apache_smoke: fail $*"
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

find_apache() {
    if [ -n "$APACHE_HTTPD_BIN" ]; then
        printf '%s\n' "$APACHE_HTTPD_BIN"
        return 0
    fi
    command -v apache2 2>/dev/null || command -v httpd 2>/dev/null || true
}

find_apxs() {
    if [ -n "$APXS_BIN" ]; then
        printf '%s\n' "$APXS_BIN"
        return 0
    fi
    command -v apxs 2>/dev/null || command -v apxs2 2>/dev/null || true
}

find_curl() {
    if [ -n "$CURL_BIN" ]; then
        printf '%s\n' "$CURL_BIN"
        return 0
    fi
    command -v curl 2>/dev/null || true
}

apache_modules_dir() {
    if [ -n "$APXS_BIN" ] && [ -x "$APXS_BIN" ]; then
        dir=$("$APXS_BIN" -q LIBEXECDIR 2>/dev/null || true)
        if [ -n "$dir" ]; then
            printf '%s\n' "$dir"
            return 0
        fi
        libdir=$("$APXS_BIN" -q LIBDIR 2>/dev/null || true)
        if [ -n "$libdir" ]; then
            printf '%s/modules\n' "$libdir"
            return 0
        fi
    fi
    return 1
}

append_load_if_exists() {
    module_name=$1
    file_name=$2
    modules_dir=$3
    output=$4
    module_path="$modules_dir/$file_name"
    if [ -f "$module_path" ]; then
        {
            echo "<IfModule !$module_name>"
            echo "LoadModule $module_name \"$module_path\""
            echo "</IfModule>"
        } >> "$output"
    fi
}

append_mpm_if_needed() {
    modules_dir=$1
    output=$2
    for candidate in \
        "mpm_event_module mod_mpm_event.so" \
        "mpm_worker_module mod_mpm_worker.so" \
        "mpm_prefork_module mod_mpm_prefork.so"
    do
        module_name=${candidate% *}
        file_name=${candidate#* }
        module_path="$modules_dir/$file_name"
        if [ -f "$module_path" ]; then
            {
                echo "<IfModule !mpm_event_module>"
                echo "<IfModule !mpm_worker_module>"
                echo "<IfModule !mpm_prefork_module>"
                echo "LoadModule $module_name \"$module_path\""
                echo "</IfModule>"
                echo "</IfModule>"
                echo "</IfModule>"
            } >> "$output"
            return 0
        fi
    done
    return 0
}

escape_sed() {
    printf '%s' "$1" | sed 's/[&|]/\\&/g'
}

render_config() {
    sed \
        -e "s|@@RUNTIME_ROOT@@|$(escape_sed "$RUNTIME_ROOT")|g" \
        -e "s|@@PORT@@|$(escape_sed "$PORT")|g" \
        -e "s|@@MODULES_FILE@@|$(escape_sed "$MODULES_FILE")|g" \
        -e "s|@@APACHE_MODULE@@|$(escape_sed "$APACHE_MODULE")|g" \
        -e "s|@@DOCROOT@@|$(escape_sed "$DOCROOT")|g" \
        -e "s|@@RULES_FILE@@|$(escape_sed "$RULES_FILE")|g" \
        "$TEMPLATE" > "$CONFIG_FILE"
}

cleanup() {
    if [ -n "${HTTPD_PID:-}" ] && kill -0 "$HTTPD_PID" >/dev/null 2>&1; then
        kill "$HTTPD_PID" >/dev/null 2>&1 || true
        wait "$HTTPD_PID" >/dev/null 2>&1 || true
    fi
}

echo "apache_smoke: BUILD_ROOT=$BUILD_ROOT"
echo "apache_smoke: APACHE_BUILD_ROOT=$APACHE_BUILD_ROOT"
echo "apache_smoke: RUNTIME_ROOT=$RUNTIME_ROOT"
echo "apache_smoke: LOG_DIR=$LOG_DIR"
echo "apache_smoke: APACHE_MODULE=$APACHE_MODULE"
echo "apache_smoke: TEST_CASE=$TEST_CASE"

require_absolute_generated_path "$BUILD_ROOT" "BUILD_ROOT"
require_absolute_generated_path "$APACHE_BUILD_ROOT" "APACHE_BUILD_ROOT"
require_absolute_generated_path "$RUNTIME_ROOT" "RUNTIME_ROOT"
require_absolute_generated_path "$LOG_DIR" "LOG_DIR"

mkdir -p "$LOG_DIR" "$RUNTIME_ROOT/conf" "$RUNTIME_ROOT/logs" "$RUNTIME_ROOT/htdocs" "$RUNTIME_ROOT/run"
: > "$STATUS_FILE"

APACHE_HTTPD_BIN=$(find_apache)
APXS_BIN=$(find_apxs)
CURL_BIN=$(find_curl)

[ -n "$APACHE_HTTPD_BIN" ] || blocked "missing Apache httpd executable; set APACHE_HTTPD=/path/to/apache2-or-httpd"
[ -x "$APACHE_HTTPD_BIN" ] || blocked "Apache executable is not executable: $APACHE_HTTPD_BIN"
[ -n "$CURL_BIN" ] || blocked "missing curl; set CURL=/path/to/curl"
[ -x "$CURL_BIN" ] || blocked "curl is not executable: $CURL_BIN"
[ -f "$APACHE_MODULE" ] || blocked "missing Apache connector module: $APACHE_MODULE"

if [ ! -f "$MODSECURITY_LIB_DIR/libmodsecurity.so" ]; then
    if [ -f "$MODSECURITY_V3_DIR/src/.libs/libmodsecurity.so" ]; then
        MODSECURITY_LIB_DIR="$MODSECURITY_V3_DIR/src/.libs"
    else
        blocked "missing libmodsecurity.so in staged or build-copy library directories"
    fi
fi

MODULES_FILE="$RUNTIME_ROOT/conf/modules.load"
CONFIG_FILE="$RUNTIME_ROOT/conf/httpd.conf"
RULES_FILE="$RUNTIME_ROOT/conf/modsecurity-smoke.conf"
DOCROOT="$RUNTIME_ROOT/htdocs"
RESPONSE_BODY="$LOG_DIR/response-body.txt"

echo "TEST-OK-IF-YOU-SEE-THIS" > "$DOCROOT/index.html"
cat > "$RULES_FILE" <<'RULES'
SecRuleEngine On
SecRule ARGS:test "@streq attack" "id:1001,phase:2,deny,status:403"
RULES

: > "$MODULES_FILE"
if modules_dir=$(apache_modules_dir); then
    append_mpm_if_needed "$modules_dir" "$MODULES_FILE"
    append_load_if_exists "authz_core_module" "mod_authz_core.so" "$modules_dir" "$MODULES_FILE"
    append_load_if_exists "authz_host_module" "mod_authz_host.so" "$modules_dir" "$MODULES_FILE"
    append_load_if_exists "unixd_module" "mod_unixd.so" "$modules_dir" "$MODULES_FILE"
    append_load_if_exists "dir_module" "mod_dir.so" "$modules_dir" "$MODULES_FILE"
    append_load_if_exists "mime_module" "mod_mime.so" "$modules_dir" "$MODULES_FILE"
fi

render_config

LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH

if ! "$APACHE_HTTPD_BIN" -t -f "$CONFIG_FILE" > "$LOG_DIR/configtest.log" 2>&1; then
    fail "Apache configtest failed; see $LOG_DIR/configtest.log"
fi

trap cleanup EXIT INT TERM
"$APACHE_HTTPD_BIN" -X -f "$CONFIG_FILE" > "$LOG_DIR/httpd.log" 2>&1 &
HTTPD_PID=$!

ready=0
i=0
while [ "$i" -lt 30 ]; do
    if ! kill -0 "$HTTPD_PID" >/dev/null 2>&1; then
        fail "Apache exited before request; see $LOG_DIR/httpd.log"
    fi
    if "$CURL_BIN" -sS -o /dev/null "http://127.0.0.1:$PORT/" >/dev/null 2>"$LOG_DIR/curl-ready.err"; then
        ready=1
        break
    fi
    i=$((i + 1))
    sleep 1
done

[ "$ready" -eq 1 ] || fail "Apache did not become ready on 127.0.0.1:$PORT"

set +e
http_status=$("$CURL_BIN" -sS -o "$RESPONSE_BODY" -w "%{http_code}" "http://127.0.0.1:$PORT/?test=attack" 2>"$LOG_DIR/curl-attack.err")
curl_rc=$?
set -e

if [ "$curl_rc" -ne 0 ]; then
    fail "curl attack request failed rc=$curl_rc; see $LOG_DIR/curl-attack.err"
fi

if [ "$http_status" = "403" ]; then
    echo "pass: apache smoke HTTP 403 observed" >> "$STATUS_FILE"
    echo "apache_smoke: pass status=403"
    exit 0
fi

echo "fail: expected HTTP 403, observed HTTP $http_status" >> "$STATUS_FILE"
echo "apache_smoke: fail expected=403 observed=$http_status"
exit 1
