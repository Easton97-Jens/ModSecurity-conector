#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd "$SCRIPT_DIR/../../.." && pwd)
FRAMEWORK_ROOT="${FRAMEWORK_ROOT:-$REPO_ROOT/modules/ModSecurity-test-Framework}"
[ -d "$FRAMEWORK_ROOT" ] || { echo "nginx_smoke: blocked FRAMEWORK_ROOT is missing; run git submodule update --init --recursive or set FRAMEWORK_ROOT=/path/to/ModSecurity-test-Framework"; exit 77; }
BUILD_ROOT="${BUILD_ROOT:-${XDG_STATE_HOME:-${HOME:-/tmp}/.local/state}/ModSecurity-conector-build}"
CURRENT_UID=$(id -u 2>/dev/null || printf 'unknown')
if [ -z "${NGINX_HARNESS_WORK_ROOT:-}" ]; then
    if [ "$CURRENT_UID" = "0" ]; then
        NGINX_HARNESS_PARENT="${NGINX_HARNESS_PARENT:-${TMPDIR:-/tmp}}"
    else
        NGINX_HARNESS_PARENT="${NGINX_HARNESS_PARENT:-${RUNNER_TEMP:-${TMPDIR:-/tmp}}}"
    fi
    NGINX_HARNESS_WORK_ROOT="$NGINX_HARNESS_PARENT/ModSecurity-conector-nginx-runtime-$CURRENT_UID"
fi
NGINX_BUILD_DIR="${NGINX_BUILD_DIR:-$BUILD_ROOT/nginx-build}"
NGINX_PREFIX="${NGINX_PREFIX:-$BUILD_ROOT/nginx-runtime/nginx}"
NGINX_BINARY="${NGINX_BINARY:-$NGINX_PREFIX/sbin/nginx}"
NGINX_MODULE="${NGINX_MODULE:-$NGINX_PREFIX/modules/ngx_http_modsecurity_module.so}"
MODSECURITY_LIB_DIR="${MODSECURITY_LIB_DIR:-$NGINX_BUILD_DIR/output/modsecurity/lib}"
LOG_DIR="${LOG_DIR:-$NGINX_HARNESS_WORK_ROOT/logs}"
RESULTS_DIR="${RESULTS_DIR:-$BUILD_ROOT/results}"
RUNTIME_BASE="${RUNTIME_BASE:-$NGINX_HARNESS_WORK_ROOT/runtime}"
RUNTIME_ROOT="${RUNTIME_ROOT:-}"
CURL_BIN="${CURL:-}"
PYTHON_BIN="${PYTHON:-python3}"
PYTHONDONTWRITEBYTECODE="${PYTHONDONTWRITEBYTECODE:-1}"
export PYTHONDONTWRITEBYTECODE
BASE_PORT="${PORT:-18081}"
PORT="$BASE_PORT"
PORT_SEARCH_LIMIT="${PORT_SEARCH_LIMIT:-100}"
PORT_RETRY_LIMIT="${PORT_RETRY_LIMIT:-1}"
TEMPLATE="$SCRIPT_DIR/nginx_smoke.conf"
TEST_CASE="${TEST_CASE:-}"
SMOKE_CASES="${SMOKE_CASES:-}"
CASE_SCOPE="${CASE_SCOPE:-all}"
CASE_CLI="$FRAMEWORK_ROOT/tests/runners/case_cli.py"
RUN_ONE_CASE="${RUN_ONE_CASE:-0}"
STATUS_FILE="$LOG_DIR/status.txt"
CONNECTOR_ORIGIN_SOURCE="${CONNECTOR_ORIGIN_SOURCE:-}"
CONNECTOR_ORIGIN_SOURCE_REPO="${CONNECTOR_ORIGIN_SOURCE_REPO:-}"
CONNECTOR_ORIGIN_SOURCE_URL="${CONNECTOR_ORIGIN_SOURCE_URL:-}"
CONNECTOR_ORIGIN_SOURCE_COMMIT="${CONNECTOR_ORIGIN_SOURCE_COMMIT:-}"
CONNECTOR_ORIGIN_SOURCE_VERSION="${CONNECTOR_ORIGIN_SOURCE_VERSION:-}"
CONNECTOR_ORIGIN_LICENSE="${CONNECTOR_ORIGIN_LICENSE:-}"
CONNECTOR_ORIGIN_IMPORTED_PATH="${CONNECTOR_ORIGIN_IMPORTED_PATH:-}"
NGINX_WORKER_USER="${NGINX_WORKER_USER:-nobody}"
NGINX_WORKER_GROUP="${NGINX_WORKER_GROUP:-}"
PERMISSIONS_LOG="${PERMISSIONS_LOG:-}"

load_connector_adapter_metadata() {
    eval "$(CONNECTOR_ROOT="$REPO_ROOT" "$PYTHON_BIN" "$FRAMEWORK_ROOT/ci/adapter_metadata.py" shell nginx --prefix CONNECTOR_ADAPTER)"
    CONNECTOR_ORIGIN_SOURCE="${CONNECTOR_ORIGIN_SOURCE:-$CONNECTOR_ADAPTER_SOURCE}"
    CONNECTOR_ORIGIN_SOURCE_REPO="${CONNECTOR_ORIGIN_SOURCE_REPO:-$CONNECTOR_ADAPTER_SOURCE_REPO}"
    CONNECTOR_ORIGIN_SOURCE_URL="${CONNECTOR_ORIGIN_SOURCE_URL:-$CONNECTOR_ADAPTER_SOURCE_URL}"
    CONNECTOR_ORIGIN_SOURCE_COMMIT="${CONNECTOR_ORIGIN_SOURCE_COMMIT:-$CONNECTOR_ADAPTER_SOURCE_COMMIT}"
    CONNECTOR_ORIGIN_SOURCE_VERSION="${CONNECTOR_ORIGIN_SOURCE_VERSION:-$CONNECTOR_ADAPTER_SOURCE_VERSION}"
    CONNECTOR_ORIGIN_LICENSE="${CONNECTOR_ORIGIN_LICENSE:-$CONNECTOR_ADAPTER_LICENSE}"
    CONNECTOR_ORIGIN_IMPORTED_PATH="${CONNECTOR_ORIGIN_IMPORTED_PATH:-$CONNECTOR_ADAPTER_IMPORTED_PATH}"
}

load_connector_adapter_metadata

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

ensure_dir_755() {
    for path in "$@"; do
        install -d -m 755 "$path"
    done
}

nginx_worker_group() {
    if [ -n "$NGINX_WORKER_GROUP" ]; then
        printf '%s\n' "$NGINX_WORKER_GROUP"
        return 0
    fi
    id -gn "$NGINX_WORKER_USER" 2>/dev/null || printf '%s\n' "$NGINX_WORKER_USER"
}

write_permission_diagnostics() {
    log_file=${PERMISSIONS_LOG:-$LOG_DIR/permissions.log}
    mkdir -p "$(dirname "$log_file")"
    {
        echo "nginx_harness_permissions:"
        echo "  effective_user=$(id -un 2>/dev/null || printf unknown)"
        echo "  effective_uid=$CURRENT_UID"
        echo "  nginx_worker_user_hint=$NGINX_WORKER_USER"
        echo "  nginx_worker_group_hint=$(nginx_worker_group)"
        echo "  build_root=$BUILD_ROOT"
        echo "  nginx_harness_work_root=$NGINX_HARNESS_WORK_ROOT"
        echo "  runtime_base=$RUNTIME_BASE"
        echo "  runtime_root=$RUNTIME_ROOT"
        echo "  log_dir=$LOG_DIR"
        echo "  docroot=${DOCROOT:-}"
        echo
        for path in \
            "$NGINX_HARNESS_WORK_ROOT" \
            "$RUNTIME_BASE" \
            "$RUNTIME_ROOT" \
            "$LOG_DIR" \
            "${LOG_DIR}/audit" \
            "${DOCROOT:-}" \
            "${DOCROOT:-}/index.html" \
            "${DOCROOT:-}/__modsec_smoke_ready" \
            "${NGINX_PHASE4_LOG_FILE:-}" \
            "${CONFIG_FILE:-}" \
            "${RULES_FILE:-}"
        do
            [ -n "$path" ] || continue
            echo "-- $path"
            if [ -e "$path" ]; then
                stat -c '%A %U %G %n' "$path" 2>/dev/null || ls -ld "$path" 2>/dev/null || true
                if command -v namei >/dev/null 2>&1; then
                    namei -l "$path" 2>/dev/null || true
                fi
            else
                echo "missing"
            fi
            echo
        done
    } > "$log_file"
}

ensure_worker_runtime_permissions() {
    chmod -R u+rwX,go+rX "$NGINX_HARNESS_WORK_ROOT" 2>/dev/null || true
    if [ "$CURRENT_UID" = "0" ]; then
        worker_group=$(nginx_worker_group)
        chown -R "$NGINX_WORKER_USER:$worker_group" "$NGINX_HARNESS_WORK_ROOT" 2>/dev/null || true
        chmod -R u+rwX,go+rX "$NGINX_HARNESS_WORK_ROOT" 2>/dev/null || true
    fi
    write_permission_diagnostics
}

nginx_docroot_permission_denied() {
    [ -f "$LOG_DIR/error.log" ] || return 1
    grep -E "htdocs/index\\.html.*Permission denied|htdocs/index\\.html.*forbidden \\(13: Permission denied\\)" "$LOG_DIR/error.log" >/dev/null 2>&1
}

require_absolute_generated_path() {
    path=$1
    label=$2
    case "$path" in
        /*) ;;
        *) blocked "$label must be absolute: $path" ;;
    esac
    case "$path" in
        "$REPO_ROOT"|"$REPO_ROOT"/*|"$FRAMEWORK_ROOT"|"$FRAMEWORK_ROOT"/*)
            blocked "$label is inside a read-only or source checkout: $path"
            ;;
        *) ;;
    esac
}

resolve_case_path() {
    item=$1
    "$PYTHON_BIN" "$CASE_CLI" list-cases \
        --repo-root "$REPO_ROOT" \
        --framework-root "$FRAMEWORK_ROOT" \
        --connector-root "$REPO_ROOT" \
        --connector nginx \
        --scope "$CASE_SCOPE" \
        --test-case "$item"
}

list_case_files() {
    if [ -n "$TEST_CASE" ]; then
        "$PYTHON_BIN" "$CASE_CLI" list-cases \
            --repo-root "$REPO_ROOT" \
            --framework-root "$FRAMEWORK_ROOT" \
            --connector-root "$REPO_ROOT" \
            --connector nginx \
            --scope "$CASE_SCOPE" \
            --test-case "$TEST_CASE"
        return
    fi
    if [ -n "$SMOKE_CASES" ]; then
        "$PYTHON_BIN" "$CASE_CLI" list-cases \
            --repo-root "$REPO_ROOT" \
            --framework-root "$FRAMEWORK_ROOT" \
            --connector-root "$REPO_ROOT" \
            --connector nginx \
            --scope "$CASE_SCOPE" \
            --smoke-cases "$SMOKE_CASES"
        return
    fi
    "$PYTHON_BIN" "$CASE_CLI" list-cases \
        --repo-root "$REPO_ROOT" \
        --framework-root "$FRAMEWORK_ROOT" \
        --connector-root "$REPO_ROOT" \
        --connector nginx \
        --scope "$CASE_SCOPE"
}

write_case_result() {
    case_path=$1
    case_status=$2
    actual_status=${3:-}
    output=$4
    if [ -n "$actual_status" ]; then
        "$PYTHON_BIN" "$CASE_CLI" case-info \
            --case "$case_path" \
            --connector nginx \
            --status "$case_status" \
            --actual-status "$actual_status" \
            --output "$output"
    else
        "$PYTHON_BIN" "$CASE_CLI" case-info \
            --case "$case_path" \
            --connector nginx \
            --status "$case_status" \
            --output "$output"
    fi
}

run_all_cases() {
    require_absolute_generated_path "$BUILD_ROOT" "BUILD_ROOT"
    require_absolute_generated_path "$LOG_DIR" "LOG_DIR"
    require_absolute_generated_path "$RESULTS_DIR" "RESULTS_DIR"
    require_absolute_generated_path "$RUNTIME_BASE" "RUNTIME_BASE"

    mkdir -p "$LOG_DIR" "$RESULTS_DIR"
    summary_file="$RESULTS_DIR/nginx-summary.txt"
    json_file="$RESULTS_DIR/nginx-summary.json"
    results_jsonl="$RESULTS_DIR/nginx-results.jsonl"
    connector_summary="$RESULTS_DIR/connector-summary.txt"
    : > "$summary_file"
    : > "$results_jsonl"

    cases=$(list_case_files) || exit 1
    if [ -z "$cases" ]; then
        echo "nginx_smoke: fail no shared smoke cases found" >&2
        exit 1
    fi

    any_fail=0
    any_blocked=0
    index=0
    for case_path in $cases; do
        case_name=$(basename "$case_path" .yaml)
        case_log_dir="$LOG_DIR/$case_name"
        case_runtime="$RUNTIME_BASE/$case_name"
        case_port=$((BASE_PORT + index))
        echo "nginx_smoke: running case=$case_name port=$case_port"
        set +e
        RUN_ONE_CASE=1 \
            TEST_CASE="$case_path" \
            LOG_DIR="$case_log_dir" \
            RUNTIME_ROOT="$case_runtime" \
            PORT="$case_port" \
            sh "$0"
        rc=$?
        set -e
        case_status=pass
        case_status_upper=PASS
        if [ "$rc" -eq 77 ]; then
            case_status=blocked
            case_status_upper=BLOCKED
            any_blocked=1
        elif [ "$rc" -ne 0 ]; then
            case_status=fail
            case_status_upper=FAIL
            any_fail=1
        fi
        actual_status=""
        if [ -f "$case_log_dir/observed-status.txt" ]; then
            actual_status=$(cat "$case_log_dir/observed-status.txt")
        fi
        write_case_result "$case_path" "$case_status" "$actual_status" "$case_log_dir/result.json" || true
        if [ -f "$case_log_dir/result.json" ]; then
            cat "$case_log_dir/result.json" >> "$results_jsonl"
        fi
        echo "$case_status_upper $case_name" | tee -a "$summary_file"
        index=$((index + 1))
    done

    "$PYTHON_BIN" "$CASE_CLI" summarize-results \
        --connector nginx \
        --input-jsonl "$results_jsonl" \
        --summary-json "$json_file" \
        --summary-text "$summary_file" \
        --import-status-file "$REPO_ROOT/config/testing/import-status.json" \
        --connector-path real-world \
        --validation-mode real-world-connector-path \
        --server nginx \
        --server-binary "$NGINX_BINARY" \
        --module "$NGINX_MODULE" \
        --libmodsecurity "$MODSECURITY_LIB_DIR/libmodsecurity.so" \
        --origin-source "$CONNECTOR_ORIGIN_SOURCE" \
        --origin-source-repo "$CONNECTOR_ORIGIN_SOURCE_REPO" \
        --origin-source-url "$CONNECTOR_ORIGIN_SOURCE_URL" \
        --origin-source-commit "$CONNECTOR_ORIGIN_SOURCE_COMMIT" \
        --origin-source-version "$CONNECTOR_ORIGIN_SOURCE_VERSION" \
        --origin-license "$CONNECTOR_ORIGIN_LICENSE" \
        --origin-imported-path "$CONNECTOR_ORIGIN_IMPORTED_PATH"
    cp "$summary_file" "$connector_summary"

    if [ "$any_fail" -ne 0 ]; then
        exit 1
    fi
    if [ "$any_blocked" -ne 0 ]; then
        exit 77
    fi
    exit 0
}

find_curl() {
    if [ -n "$CURL_BIN" ]; then
        printf '%s\n' "$CURL_BIN"
        return 0
    fi
    command -v curl 2>/dev/null || true
}

escape_sed() {
    raw_value=$1
    printf '%s' "$raw_value" | sed 's/[&|]/\\&/g'
}

render_config() {
    sed \
        -e "s|@@RUNTIME_ROOT@@|$(escape_sed "$RUNTIME_ROOT")|g" \
        -e "s|@@LOG_DIR@@|$(escape_sed "$LOG_DIR")|g" \
        -e "s|@@PORT@@|$(escape_sed "$PORT")|g" \
        -e "s|@@NGINX_MODULE@@|$(escape_sed "$NGINX_MODULE")|g" \
        -e "s|@@DOCROOT@@|$(escape_sed "$DOCROOT")|g" \
        -e "s|@@RULES_FILE@@|$(escape_sed "$RULES_FILE")|g" \
        -e "s|@@NGINX_LOCATION_DIRECTIVES@@|$(escape_sed "$NGINX_LOCATION_DIRECTIVES_FILE")|g" \
        "$TEMPLATE" > "$CONFIG_FILE"
}

cleanup() {
    if [ -n "${NGINX_PID:-}" ] && kill -0 "$NGINX_PID" >/dev/null 2>&1; then
        kill "$NGINX_PID" >/dev/null 2>&1 || true
        wait "$NGINX_PID" >/dev/null 2>&1 || true
    fi
    if [ -n "${RUNTIME_PID_FILE:-}" ]; then
        rm -f "$RUNTIME_PID_FILE"
    fi
}

port_is_free() {
    port_to_probe=$1
    "$PYTHON_BIN" - "$port_to_probe" <<'PY'
import socket
import sys

port = int(sys.argv[1])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.bind(("127.0.0.1", port))
except OSError:
    raise SystemExit(1)
finally:
    sock.close()
PY
}

select_free_port() {
    start_port=$1
    search_limit=$2
    offset=0
    while [ "$offset" -lt "$search_limit" ]; do
        candidate=$((start_port + offset))
        if port_is_free "$candidate"; then
            printf '%s\n' "$candidate"
            return 0
        fi
        offset=$((offset + 1))
    done
    return 1
}

stop_stale_runtime_pid() {
    pid_file=$1
    [ -f "$pid_file" ] || return 0
    case "$pid_file" in
        "$BUILD_ROOT"/*|"$RUNTIME_BASE"/*|"$NGINX_HARNESS_WORK_ROOT"/*) ;;
        *) blocked "runtime pid file is outside allowed generated runtime roots: $pid_file" ;;
    esac
    stale_pid=$(cat "$pid_file" 2>/dev/null || true)
    case "$stale_pid" in
        ""|*[!0-9]*)
            rm -f "$pid_file"
            return 0
            ;;
        *) ;;
    esac
    if ! kill -0 "$stale_pid" >/dev/null 2>&1; then
        rm -f "$pid_file"
        return 0
    fi
    stale_cmd=$(tr '\0' ' ' < "/proc/$stale_pid/cmdline" 2>/dev/null || true)
    case "$stale_cmd" in
        *"$RUNTIME_ROOT"*) ;;
        *)
            blocked "runtime pid file points to non-smoke process pid=$stale_pid command=$stale_cmd"
            ;;
    esac
    echo "nginx_smoke: stopping stale runtime process pid=$stale_pid"
    kill "$stale_pid" >/dev/null 2>&1 || true
    wait_count=0
    while kill -0 "$stale_pid" >/dev/null 2>&1 && [ "$wait_count" -lt 10 ]; do
        wait_count=$((wait_count + 1))
        sleep 1
    done
    if kill -0 "$stale_pid" >/dev/null 2>&1; then
        blocked "stale runtime process did not stop pid=$stale_pid"
    fi
    rm -f "$pid_file"
}

bind_conflict_seen() {
    grep -E "Address already in use|could not bind|bind\\(\\)" \
        "$LOG_DIR/nginx-stdout.log" \
        "$LOG_DIR/error.log" >/dev/null 2>&1
}

start_server() {
    attempt=0
    while :; do
        selected_port=$(select_free_port "$PORT" "$PORT_SEARCH_LIMIT") || \
            blocked "no free localhost port found from $PORT within $PORT_SEARCH_LIMIT attempts"
        if [ "$selected_port" != "$PORT" ]; then
            echo "nginx_smoke: selected free port=$selected_port after requested port=$PORT was unavailable"
            echo "info: selected port $selected_port after requested port $PORT was unavailable" >> "$STATUS_FILE"
        fi
        PORT="$selected_port"
        render_config

        if ! "$NGINX_BINARY" -t -p "$RUNTIME_ROOT" -c "$CONFIG_FILE" > "$LOG_DIR/configtest.log" 2>&1; then
            fail "NGINX configtest failed; see $LOG_DIR/configtest.log"
        fi

        "$NGINX_BINARY" -p "$RUNTIME_ROOT" -c "$CONFIG_FILE" > "$LOG_DIR/nginx-stdout.log" 2>&1 &
        NGINX_PID=$!

        ready=0
        i=0
        while [ "$i" -lt 30 ]; do
            if ! kill -0 "$NGINX_PID" >/dev/null 2>&1; then
                if [ "$attempt" -lt "$PORT_RETRY_LIMIT" ] && bind_conflict_seen; then
                    cleanup
                    attempt=$((attempt + 1))
                    PORT=$((PORT + 1))
                    echo "nginx_smoke: retrying after bind conflict attempt=$attempt"
                    echo "info: retrying after bind conflict attempt=$attempt" >> "$STATUS_FILE"
                    continue 2
                fi
                fail "NGINX exited before request; see $LOG_DIR/nginx-stdout.log and $LOG_DIR/error.log"
            fi
            if "$CURL_BIN" -sS -o /dev/null "http://127.0.0.1:$PORT/__modsec_smoke_ready" >/dev/null 2>"$LOG_DIR/curl-ready.err"; then
                ready=1
                break
            fi
            i=$((i + 1))
            sleep 1
        done

        if [ "$ready" -eq 1 ]; then
            return 0
        fi
        fail "NGINX did not become ready on 127.0.0.1:$PORT"
    done
}

send_case_request() {
    set -- "$CURL_BIN" -sS -X "$REQUEST_METHOD" -o "$RESPONSE_BODY" -w "%{http_code}"
    if [ -n "${REQUEST_HEADERS_FILE:-}" ] && [ -s "$REQUEST_HEADERS_FILE" ]; then
        while IFS= read -r header_line || [ -n "$header_line" ]; do
            [ -n "$header_line" ] || continue
            set -- "$@" -H "$header_line"
        done < "$REQUEST_HEADERS_FILE"
    fi
    if [ "${REQUEST_HAS_BODY:-0}" = "1" ]; then
        set -- "$@" --data-binary "@$REQUEST_BODY_FILE"
    fi
    set -- "$@" "http://127.0.0.1:$PORT$REQUEST_PATH"
    "$@" 2>"$LOG_DIR/curl-attack.err"
}

if [ "$RUN_ONE_CASE" != "1" ]; then
    run_all_cases
fi

if [ -z "$TEST_CASE" ]; then
    TEST_CASE="phase2_args_block"
fi
TEST_CASE=$(resolve_case_path "$TEST_CASE") || exit 1
case_name=$(basename "$TEST_CASE" .yaml)
if [ -z "$RUNTIME_ROOT" ]; then
    RUNTIME_ROOT="$RUNTIME_BASE/$case_name"
fi
STATUS_FILE="$LOG_DIR/status.txt"

echo "nginx_smoke: BUILD_ROOT=$BUILD_ROOT"
echo "nginx_smoke: NGINX_BUILD_DIR=$NGINX_BUILD_DIR"
echo "nginx_smoke: NGINX_PREFIX=$NGINX_PREFIX"
echo "nginx_smoke: NGINX_BINARY=$NGINX_BINARY"
echo "nginx_smoke: NGINX_MODULE=$NGINX_MODULE"
echo "nginx_smoke: NGINX_HARNESS_WORK_ROOT=$NGINX_HARNESS_WORK_ROOT"
echo "nginx_smoke: RUNTIME_ROOT=$RUNTIME_ROOT"
echo "nginx_smoke: LOG_DIR=$LOG_DIR"
echo "nginx_smoke: TEST_CASE=$TEST_CASE"
echo "nginx_smoke: CASE_SCOPE=$CASE_SCOPE"

require_absolute_generated_path "$BUILD_ROOT" "BUILD_ROOT"
require_absolute_generated_path "$NGINX_BUILD_DIR" "NGINX_BUILD_DIR"
require_absolute_generated_path "$NGINX_PREFIX" "NGINX_PREFIX"
require_absolute_generated_path "$RUNTIME_ROOT" "RUNTIME_ROOT"
require_absolute_generated_path "$LOG_DIR" "LOG_DIR"

RUNTIME_PID_FILE="$RUNTIME_ROOT/nginx.pid"

ensure_dir_755 "$NGINX_HARNESS_WORK_ROOT" "$RUNTIME_BASE" "$LOG_DIR" "$LOG_DIR/audit" "$RUNTIME_ROOT" "$RUNTIME_ROOT/conf" "$RUNTIME_ROOT/htdocs" \
    "$RUNTIME_ROOT/client_body_temp" "$RUNTIME_ROOT/proxy_temp" \
    "$RUNTIME_ROOT/fastcgi_temp" "$RUNTIME_ROOT/uwsgi_temp" \
    "$RUNTIME_ROOT/scgi_temp"
: > "$STATUS_FILE"
stop_stale_runtime_pid "$RUNTIME_PID_FILE"
rm -f "$LOG_DIR/configtest.log" \
    "$LOG_DIR/curl-attack.err" \
	    "$LOG_DIR/curl-ready.err" \
	    "$LOG_DIR/nginx.log" \
	    "$LOG_DIR/nginx-stdout.log" \
	    "$LOG_DIR/phase4.log" \
	    "$LOG_DIR/response-body.txt" \
	    "$LOG_DIR/audit.log" \
	    "$RUNTIME_ROOT/nginx.pid"
rm -f "$LOG_DIR/audit/"*

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
REQUEST_HEADERS_FILE="$RUNTIME_ROOT/conf/request-headers.txt"
REQUEST_BODY_FILE="$RUNTIME_ROOT/conf/request-body.bin"
AUDIT_LOG_FILE="$LOG_DIR/audit.log"
AUDIT_LOG_DIR="$LOG_DIR/audit"
NGINX_LOCATION_DIRECTIVES_FILE="$RUNTIME_ROOT/conf/nginx-location-directives.conf"
NGINX_PHASE4_LOG_FILE="$LOG_DIR/phase4.log"

ensure_worker_runtime_permissions
if ! "$PYTHON_BIN" "$CASE_CLI" materialize \
    --case "$TEST_CASE" \
    --rules-file "$RULES_FILE" \
    --env-file "$CASE_ENV_FILE" \
    --headers-file "$REQUEST_HEADERS_FILE" \
    --body-file "$REQUEST_BODY_FILE" \
	    --docroot "$DOCROOT" \
	    --audit-log-file "$AUDIT_LOG_FILE" \
	    --audit-log-dir "$AUDIT_LOG_DIR" \
	    --nginx-location-directives-file "$NGINX_LOCATION_DIRECTIVES_FILE" \
	    --nginx-runtime-config-dir "$RUNTIME_ROOT/conf" \
	    --nginx-phase4-log-file "$NGINX_PHASE4_LOG_FILE" > "$LOG_DIR/case-materialize.log" 2>&1; then
    blocked "failed to materialize shared case; see $LOG_DIR/case-materialize.log"
fi
ensure_worker_runtime_permissions
. "$CASE_ENV_FILE"

LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR:$NGINX_PREFIX/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH

trap cleanup EXIT INT TERM
start_server

set +e
http_status=$(send_case_request)
curl_rc=$?
set -e
printf '%s\n' "$http_status" > "$LOG_DIR/observed-status.txt"

if [ "$curl_rc" -ne 0 ]; then
    write_case_result "$TEST_CASE" fail "$http_status" "$LOG_DIR/result.json" || true
    fail "curl attack request failed rc=$curl_rc; see $LOG_DIR/curl-attack.err"
fi

if "$PYTHON_BIN" "$CASE_CLI" assert-status \
    --case "$TEST_CASE" \
	    --actual-status "$http_status" \
	    --response-body-file "$RESPONSE_BODY" \
	    --audit-log-file "$AUDIT_LOG_FILE" \
	    --nginx-phase4-log-file "$NGINX_PHASE4_LOG_FILE" \
	    --status-file "$STATUS_FILE" > "$LOG_DIR/case-assert.log" 2>&1; then
    write_case_result "$TEST_CASE" pass "$http_status" "$LOG_DIR/result.json" || true
    echo "nginx_smoke: pass case=$CASE_NAME status=$http_status"
    exit 0
fi

write_case_result "$TEST_CASE" fail "$http_status" "$LOG_DIR/result.json" || true
if [ "$http_status" = "403" ] && nginx_docroot_permission_denied; then
    write_case_result "$TEST_CASE" blocked "$http_status" "$LOG_DIR/result.json" || true
    write_permission_diagnostics
    blocked "NGINX could not read generated docroot; see $LOG_DIR/error.log and $LOG_DIR/permissions.log"
fi
echo "nginx_smoke: fail case=$CASE_NAME observed=$http_status expected=$EXPECT_STATUS"
exit 1
