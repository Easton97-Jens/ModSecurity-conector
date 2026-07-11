#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd "$SCRIPT_DIR/../../.." && pwd)
FRAMEWORK_ROOT="${FRAMEWORK_ROOT:-$REPO_ROOT/modules/ModSecurity-test-Framework}"
[ -d "$FRAMEWORK_ROOT" ] || { echo "apache_smoke: blocked FRAMEWORK_ROOT is missing; run git submodule update --init --recursive or set FRAMEWORK_ROOT=/path/to/ModSecurity-test-Framework"; exit 77; }
BUILD_ROOT="${BUILD_ROOT:-${XDG_STATE_HOME:-${HOME:-/tmp}/.local/state}/ModSecurity-conector-build}"
APACHE_BUILD_ROOT="${APACHE_BUILD_ROOT:-$BUILD_ROOT/apache-build}"
LOG_DIR="${LOG_DIR:-$BUILD_ROOT/logs/apache-runtime}"
RESULTS_DIR="${RESULTS_DIR:-$BUILD_ROOT/results}"
if [ -n "${FORCE_ALL_CASES:-}" ] && [ "$RESULTS_DIR" = "$BUILD_ROOT/results" ]; then
    RESULTS_DIR="$BUILD_ROOT/results/force-all"
fi
RUNTIME_BASE="${RUNTIME_BASE:-$BUILD_ROOT/apache-runtime}"
RUNTIME_ROOT="${RUNTIME_ROOT:-}"
HTTPD_PREFIX="${HTTPD_PREFIX:-$BUILD_ROOT/apache-runtime/httpd}"
MODSECURITY_V3_DIR="${MODSECURITY_V3_DIR:-$APACHE_BUILD_ROOT/ModSecurity_V3}"
MODSECURITY_LIB_DIR="${MODSECURITY_LIB_DIR:-$APACHE_BUILD_ROOT/output/modsecurity/lib}"
PCRE2_PREFIX="${PCRE2_PREFIX:-$APACHE_BUILD_ROOT/output/pcre2}"
APACHE_MODULE="${APACHE_MODULE:-$APACHE_BUILD_ROOT/output/apache/mod_security3.so}"
APACHE_HTTPD_BIN="${APACHE_HTTPD:-${APACHE:-$HTTPD_PREFIX/bin/httpd}}"
APXS_BIN="${APXS:-$HTTPD_PREFIX/bin/apxs}"
CURL_BIN="${CURL:-}"
PYTHON_BIN="${PYTHON:-python3}"
PYTHONDONTWRITEBYTECODE="${PYTHONDONTWRITEBYTECODE:-1}"
export PYTHONDONTWRITEBYTECODE
BASE_PORT="${PORT:-18080}"
PORT="$BASE_PORT"
PORT_SEARCH_LIMIT="${PORT_SEARCH_LIMIT:-100}"
PORT_RETRY_LIMIT="${PORT_RETRY_LIMIT:-1}"
TEMPLATE="$SCRIPT_DIR/apache_smoke.conf"
TEST_CASE="${TEST_CASE:-}"
SMOKE_CASES="${SMOKE_CASES:-}"
CASE_SCOPE="${CASE_SCOPE:-all}"
CASE_CLI="$FRAMEWORK_ROOT/tests/runners/case_cli.py"
RUN_ONE_CASE="${RUN_ONE_CASE:-0}"
MSCONNECTOR_SMOKE_STAGE="${MSCONNECTOR_SMOKE_STAGE:-minimal_runtime_smoke}"
STATUS_FILE="$LOG_DIR/status.txt"
IFMODULE_END="</IfModule>"
CONNECTOR_ORIGIN_SOURCE="${CONNECTOR_ORIGIN_SOURCE:-}"
CONNECTOR_ORIGIN_SOURCE_REPO="${CONNECTOR_ORIGIN_SOURCE_REPO:-}"
CONNECTOR_ORIGIN_SOURCE_URL="${CONNECTOR_ORIGIN_SOURCE_URL:-}"
CONNECTOR_ORIGIN_SOURCE_COMMIT="${CONNECTOR_ORIGIN_SOURCE_COMMIT:-}"
CONNECTOR_ORIGIN_SOURCE_VERSION="${CONNECTOR_ORIGIN_SOURCE_VERSION:-}"
CONNECTOR_ORIGIN_LICENSE="${CONNECTOR_ORIGIN_LICENSE:-}"
CONNECTOR_ORIGIN_IMPORTED_PATH="${CONNECTOR_ORIGIN_IMPORTED_PATH:-}"
MODSECURITY_TEST_VARIANT="${MODSECURITY_TEST_VARIANT:-}"
MODSECURITY_RULE_PREAMBLE_FILE="${MODSECURITY_RULE_PREAMBLE_FILE:-}"
MSCONNECTOR_FULL_LIFECYCLE_SYNC="${MSCONNECTOR_FULL_LIFECYCLE_SYNC:-0}"
FULL_LIFECYCLE_EVIDENCE_OUTPUT="${FULL_LIFECYCLE_EVIDENCE_OUTPUT:-}"
SYNCHRONIZED_UPSTREAM="$FRAMEWORK_ROOT/tests/runners/synchronized_upstream.py"

load_connector_adapter_metadata() {
    eval "$(CONNECTOR_ROOT="$REPO_ROOT" "$PYTHON_BIN" "$FRAMEWORK_ROOT/ci/adapter_metadata.py" shell apache --prefix CONNECTOR_ADAPTER)"
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

not_executable() {
    echo "apache_smoke: not_executable $*"
    mkdir -p "$LOG_DIR"
    echo "not_executable: $*" >> "$STATUS_FILE"
    exit 78
}

configtest_case_not_executable() {
    grep -E "Rules error|modsecurity-smoke\\.conf|modsecurity_rules_file|modsecurity_rules" \
        "$LOG_DIR/configtest.log" >/dev/null 2>&1
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
        --connector apache \
        --scope "$CASE_SCOPE" \
        --test-case "$item"
}

list_case_files() {
    args="--repo-root $REPO_ROOT --framework-root $FRAMEWORK_ROOT --connector-root $REPO_ROOT --connector apache --scope $CASE_SCOPE"
    if [ -n "$TEST_CASE" ]; then
        "$PYTHON_BIN" "$CASE_CLI" list-cases \
            --repo-root "$REPO_ROOT" \
            --framework-root "$FRAMEWORK_ROOT" \
            --connector-root "$REPO_ROOT" \
            --connector apache \
            --scope "$CASE_SCOPE" \
            --test-case "$TEST_CASE"
        return
    fi
    if [ -n "$SMOKE_CASES" ]; then
        "$PYTHON_BIN" "$CASE_CLI" list-cases \
            --repo-root "$REPO_ROOT" \
            --framework-root "$FRAMEWORK_ROOT" \
            --connector-root "$REPO_ROOT" \
            --connector apache \
            --scope "$CASE_SCOPE" \
            --smoke-cases "$SMOKE_CASES"
        return
    fi
    # shellcheck disable=SC2086
    "$PYTHON_BIN" "$CASE_CLI" list-cases $args
}

write_case_result() {
    case_path=$1
    case_status=$2
    actual_status=${3:-}
    output=$4
    observed_transport=${5:-http_status}
    reason=${6:-}
    output_dir=$(dirname "$output")
    if [ -n "$actual_status" ]; then
        "$PYTHON_BIN" "$CASE_CLI" case-info \
            --case "$case_path" \
            --connector apache \
            --status "$case_status" \
            --actual-status "$actual_status" \
            --observed-transport-result "$observed_transport" \
            --reason "$reason" \
            --response-body-file "$output_dir/response-body.txt" \
            --audit-log-file "$output_dir/audit.log" \
            --access-log-file "$output_dir/access.log" \
            --error-log-file "$output_dir/error.log" \
            --phase4-log-file "$output_dir/phase4.log" \
            --output "$output"
    else
        "$PYTHON_BIN" "$CASE_CLI" case-info \
            --case "$case_path" \
            --connector apache \
            --status "$case_status" \
            --observed-transport-result "$observed_transport" \
            --reason "$reason" \
            --response-body-file "$output_dir/response-body.txt" \
            --audit-log-file "$output_dir/audit.log" \
            --access-log-file "$output_dir/access.log" \
            --error-log-file "$output_dir/error.log" \
            --phase4-log-file "$output_dir/phase4.log" \
            --output "$output"
    fi
}

run_all_cases() {
    require_absolute_generated_path "$BUILD_ROOT" "BUILD_ROOT"
    require_absolute_generated_path "$LOG_DIR" "LOG_DIR"
    require_absolute_generated_path "$RESULTS_DIR" "RESULTS_DIR"
    require_absolute_generated_path "$RUNTIME_BASE" "RUNTIME_BASE"

    mkdir -p "$LOG_DIR" "$RESULTS_DIR"
    summary_file="$RESULTS_DIR/apache-summary.txt"
    json_file="$RESULTS_DIR/apache-summary.json"
    results_jsonl="$RESULTS_DIR/apache-results.jsonl"
    connector_summary="$RESULTS_DIR/connector-summary.txt"
    : > "$summary_file"
    : > "$results_jsonl"

    cases=$(list_case_files) || exit 1
    if [ -z "$cases" ]; then
        echo "apache_smoke: fail no shared smoke cases found" >&2
        exit 1
    fi

    any_fail=0
    any_blocked=0
    any_not_executable=0
    index=0
    for case_path in $cases; do
        case_name=$(basename "$case_path" .yaml)
        case_log_dir="$LOG_DIR/$case_name"
        case_runtime="$RUNTIME_BASE/$case_name"
        case_port=$((BASE_PORT + index))
        echo "apache_smoke: running case=$case_name port=$case_port"
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
        elif [ "$rc" -eq 78 ]; then
            case_status=not_executable
            case_status_upper=NOT_EXECUTABLE
            any_not_executable=1
        elif [ "$rc" -ne 0 ]; then
            case_status=fail
            case_status_upper=FAIL
            any_fail=1
        fi
        actual_status=""
        if [ -f "$case_log_dir/observed-status.txt" ]; then
            actual_status=$(cat "$case_log_dir/observed-status.txt")
        fi
        observed_transport=http_status
        if [ -f "$case_log_dir/observed-transport-result.txt" ]; then
            observed_transport=$(cat "$case_log_dir/observed-transport-result.txt")
        fi
        reason=""
        if [ -f "$case_log_dir/status.txt" ]; then
            reason=$(tail -n 1 "$case_log_dir/status.txt")
        fi
        write_case_result "$case_path" "$case_status" "$actual_status" "$case_log_dir/result.json" "$observed_transport" "$reason" || true
        if [ -f "$case_log_dir/result.json" ]; then
            cat "$case_log_dir/result.json" >> "$results_jsonl"
        fi
        echo "$case_status_upper $case_name" | tee -a "$summary_file"
        index=$((index + 1))
    done

    "$PYTHON_BIN" "$CASE_CLI" summarize-results \
        --connector apache \
        --input-jsonl "$results_jsonl" \
        --summary-json "$json_file" \
        --summary-text "$summary_file" \
        --import-status-file "$REPO_ROOT/config/testing/import-status.json" \
        --connector-path real-world \
        --validation-mode real-world-connector-path \
        --server apache \
        --server-binary "$APACHE_HTTPD_BIN" \
        --module "$APACHE_MODULE" \
        --libmodsecurity "$MODSECURITY_LIB_DIR/libmodsecurity.so" \
        --origin-source "$CONNECTOR_ORIGIN_SOURCE" \
        --origin-source-repo "$CONNECTOR_ORIGIN_SOURCE_REPO" \
        --origin-source-url "$CONNECTOR_ORIGIN_SOURCE_URL" \
        --origin-source-commit "$CONNECTOR_ORIGIN_SOURCE_COMMIT" \
        --origin-source-version "$CONNECTOR_ORIGIN_SOURCE_VERSION" \
        --origin-license "$CONNECTOR_ORIGIN_LICENSE" \
        --origin-imported-path "$CONNECTOR_ORIGIN_IMPORTED_PATH" \
        --runtime-mode "$([ -n "${FORCE_ALL_CASES:-}" ] && printf force-all || printf default)" \
        --command "$([ -n "${FORCE_ALL_CASES:-}" ] && printf 'FORCE_ALL_CASES=1 make smoke-apache' || printf 'make smoke-apache')" \
        --exit-status "$([ "$any_fail" -ne 0 ] && printf 1 || { [ "$any_blocked" -ne 0 ] && printf 77 || printf 0; })" \
        --per-case-result-root "$LOG_DIR"
    cp "$summary_file" "$connector_summary"

    if [ "$any_fail" -ne 0 ]; then
        exit 1
    fi
    if [ "$any_blocked" -ne 0 ]; then
        exit 77
    fi
    exit 0
}

find_apache() {
    if [ -n "$APACHE_HTTPD_BIN" ]; then
        printf '%s\n' "$APACHE_HTTPD_BIN"
    fi
}

find_apxs() {
    if [ -n "$APXS_BIN" ]; then
        printf '%s\n' "$APXS_BIN"
    fi
}

find_curl() {
    if [ -n "$CURL_BIN" ]; then
        printf '%s\n' "$CURL_BIN"
        return 0
    fi
    command -v curl 2>/dev/null || true
}

apache_modules_dir() {
    # APXS records its original staging prefix.  A managed Apache cache is
    # atomically published after the build, so use the final install prefix
    # first rather than trusting that historical path in apxs.
    if [ -d "$HTTPD_PREFIX/modules" ]; then
        printf '%s\n' "$HTTPD_PREFIX/modules"
        return 0
    fi
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
                echo "$IFMODULE_END"
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
                echo "$IFMODULE_END"
                echo "$IFMODULE_END"
                echo "$IFMODULE_END"
            } >> "$output"
            return 0
        fi
    done
    return 0
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
        -e "s|@@MODULES_FILE@@|$(escape_sed "$MODULES_FILE")|g" \
        -e "s|@@APACHE_MODULE@@|$(escape_sed "$APACHE_MODULE")|g" \
        -e "s|@@DOCROOT@@|$(escape_sed "$DOCROOT")|g" \
        -e "s|@@APACHE_BACKEND_PROXY_FILE@@|$(escape_sed "$APACHE_BACKEND_PROXY_FILE")|g" \
        -e "s|@@RULES_FILE@@|$(escape_sed "$RULES_FILE")|g" \
        -e "s|@@APACHE_PHASE4_LOG@@|$(escape_sed "$APACHE_PHASE4_LOG_FILE")|g" \
        "$TEMPLATE" > "$CONFIG_FILE"
}

cleanup() {
    if [ -n "${SYNCHRONIZED_UPSTREAM_PID:-}" ] && kill -0 "$SYNCHRONIZED_UPSTREAM_PID" >/dev/null 2>&1; then
        [ -n "${SYNCHRONIZED_RELEASE_FILE:-}" ] && : > "$SYNCHRONIZED_RELEASE_FILE"
        kill "$SYNCHRONIZED_UPSTREAM_PID" >/dev/null 2>&1 || true
        wait "$SYNCHRONIZED_UPSTREAM_PID" >/dev/null 2>&1 || true
    fi
    if [ -n "${HTTPD_PID:-}" ] && kill -0 "$HTTPD_PID" >/dev/null 2>&1; then
        kill "$HTTPD_PID" >/dev/null 2>&1 || true
        wait "$HTTPD_PID" >/dev/null 2>&1 || true
    fi
    if [ -n "${RESPONSE_HEADER_BACKEND_PID:-}" ] && kill -0 "$RESPONSE_HEADER_BACKEND_PID" >/dev/null 2>&1; then
        kill "$RESPONSE_HEADER_BACKEND_PID" >/dev/null 2>&1 || true
        wait "$RESPONSE_HEADER_BACKEND_PID" >/dev/null 2>&1 || true
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

port_accepts_tcp() {
    port_to_probe=$1
    "$PYTHON_BIN" - "$port_to_probe" <<'PY'
import socket
import sys

port = int(sys.argv[1])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(0.2)
try:
    sock.connect(("127.0.0.1", port))
except OSError:
    raise SystemExit(1)
finally:
    sock.close()
PY
}

wait_tcp_port() {
    port_to_probe=$1
    i=0
    while [ "$i" -lt 30 ]; do
        if port_accepts_tcp "$port_to_probe"; then
            return 0
        fi
        i=$((i + 1))
        sleep 1
    done
    return 1
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

start_synchronized_upstream() {
    [ "$MSCONNECTOR_FULL_LIFECYCLE_SYNC" = "1" ] || return 0
    [ -f "$SYNCHRONIZED_UPSTREAM" ] || blocked "missing synchronized upstream helper: $SYNCHRONIZED_UPSTREAM"
    SYNCHRONIZED_DIR="$RUNTIME_ROOT/first-byte"
    SYNCHRONIZED_READY_FILE="$SYNCHRONIZED_DIR/upstream-ready.json"
    SYNCHRONIZED_PAUSED_FILE="$SYNCHRONIZED_DIR/upstream-paused.json"
    SYNCHRONIZED_RELEASE_FILE="$SYNCHRONIZED_DIR/upstream-release"
    SYNCHRONIZED_SERVER_EVIDENCE_FILE="$SYNCHRONIZED_DIR/upstream-server.json"
    rm -rf "$SYNCHRONIZED_DIR"
    mkdir -p "$SYNCHRONIZED_DIR"
    "$PYTHON_BIN" "$SYNCHRONIZED_UPSTREAM" --serve \
        --ready-file "$SYNCHRONIZED_READY_FILE" \
        --paused-file "$SYNCHRONIZED_PAUSED_FILE" \
        --release-file "$SYNCHRONIZED_RELEASE_FILE" \
        --server-evidence-file "$SYNCHRONIZED_SERVER_EVIDENCE_FILE" \
        --timeout 30 >"$LOG_DIR/synchronized-upstream.stdout.log" \
        2>"$LOG_DIR/synchronized-upstream.stderr.log" &
    SYNCHRONIZED_UPSTREAM_PID=$!
    i=0
    while [ "$i" -lt 30 ]; do
        if [ -f "$SYNCHRONIZED_READY_FILE" ]; then
            break
        fi
        if ! kill -0 "$SYNCHRONIZED_UPSTREAM_PID" >/dev/null 2>&1; then
            blocked "synchronized upstream exited before publishing its address"
        fi
        i=$((i + 1))
        sleep 1
    done
    [ -f "$SYNCHRONIZED_READY_FILE" ] || blocked "synchronized upstream did not publish its address"
    RESPONSE_HEADER_BACKEND_PORT=$("$PYTHON_BIN" - "$SYNCHRONIZED_READY_FILE" <<'PY'
import json
import sys
payload = json.load(open(sys.argv[1], encoding="utf-8"))
port = payload.get("upstream_port")
if not isinstance(port, int) or port < 1 or port > 65535:
    raise SystemExit(1)
print(port)
PY
    ) || blocked "synchronized upstream ready record has no valid port"
}

send_synchronized_first_byte_request() {
    [ "$MSCONNECTOR_FULL_LIFECYCLE_SYNC" = "1" ] || return 1
    [ -n "$FULL_LIFECYCLE_EVIDENCE_OUTPUT" ] || fail "FULL_LIFECYCLE_EVIDENCE_OUTPUT is required for synchronized lifecycle mode"
    request_url_path=$(quote_request_path "$REQUEST_PATH")
    : > "$RESPONSE_BODY"
    "$CURL_BIN" -sS --no-buffer -X GET -o "$RESPONSE_BODY" -w "%{http_code}" \
        "http://127.0.0.1:$PORT$request_url_path" >"$LOG_DIR/first-byte-status.txt" \
        2>"$LOG_DIR/first-byte-client.err" &
    FIRST_BYTE_CLIENT_PID=$!
    observed_first_byte=0
    i=0
    while [ "$i" -lt 300 ]; do
        if [ -f "$SYNCHRONIZED_PAUSED_FILE" ] && [ -s "$RESPONSE_BODY" ]; then
            observed_first_byte=1
            break
        fi
        if ! kill -0 "$FIRST_BYTE_CLIENT_PID" >/dev/null 2>&1; then
            break
        fi
        i=$((i + 1))
        sleep 0.1
    done
    : > "$SYNCHRONIZED_RELEASE_FILE"
    set +e
    wait "$FIRST_BYTE_CLIENT_PID"
    client_rc=$?
    set -e
    [ "$observed_first_byte" -eq 1 ] || fail "client did not receive a first response byte while upstream was paused"
    [ "$client_rc" -eq 0 ] || fail "synchronized client failed after upstream release rc=$client_rc"
    http_status=$(cat "$LOG_DIR/first-byte-status.txt" 2>/dev/null || true)
    [ "$http_status" = "200" ] || fail "synchronized safe response status was not 200: $http_status"
    [ -s "$APACHE_PHASE4_LOG_FILE" ] || fail "Phase-4 host log is missing after synchronized response"
    FIRST_BYTE_HOST_METADATA="$SYNCHRONIZED_DIR/host-metadata.json"
    "$PYTHON_BIN" "$REPO_ROOT/ci/write-first-byte-host-metadata.py" \
        --phase4-log "$APACHE_PHASE4_LOG_FILE" --output "$FIRST_BYTE_HOST_METADATA" || \
        fail "could not derive bounded host metadata from the Phase-4 event"
    "$PYTHON_BIN" "$SYNCHRONIZED_UPSTREAM" --merge-evidence \
        --paused-file "$SYNCHRONIZED_PAUSED_FILE" \
        --client-first-byte-file "$RESPONSE_BODY" \
        --host-metadata-json "$FIRST_BYTE_HOST_METADATA" \
        --evidence-origin real_host \
        --output "$FULL_LIFECYCLE_EVIDENCE_OUTPUT" || \
        fail "could not write synchronized first-byte evidence"
    printf '%s\n' "$http_status" > "$LOG_DIR/observed-status.txt"
    printf '%s\n' "http_status" > "$LOG_DIR/observed-transport-result.txt"
    return 0
}

stop_stale_runtime_pid() {
    pid_file=$1
    [ -f "$pid_file" ] || return 0
    case "$pid_file" in
        "$BUILD_ROOT"/*) ;;
        *) blocked "runtime pid file is outside BUILD_ROOT: $pid_file" ;;
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
    echo "apache_smoke: stopping stale runtime process pid=$stale_pid"
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
    grep -E "Address already in use|could not bind|make_sock.*could not bind" \
        "$LOG_DIR/httpd.log" \
        "$LOG_DIR/error.log" \
        "$RUNTIME_ROOT/logs/error.log" >/dev/null 2>&1
}

start_server() {
    attempt=0
    while :; do
        selected_port=$(select_free_port "$PORT" "$PORT_SEARCH_LIMIT") || \
            blocked "no free localhost port found from $PORT within $PORT_SEARCH_LIMIT attempts"
        if [ "$selected_port" != "$PORT" ]; then
            echo "apache_smoke: selected free port=$selected_port after requested port=$PORT was unavailable"
            echo "info: selected port $selected_port after requested port $PORT was unavailable" >> "$STATUS_FILE"
        fi
        PORT="$selected_port"
        render_config

        if ! "$APACHE_HTTPD_BIN" -t -f "$CONFIG_FILE" > "$LOG_DIR/configtest.log" 2>&1; then
            if configtest_case_not_executable; then
                not_executable "Apache rejected generated ModSecurity rules; see $LOG_DIR/configtest.log"
            fi
            fail "Apache configtest failed; see $LOG_DIR/configtest.log"
        fi

        if [ "$MSCONNECTOR_SMOKE_STAGE" = "config_load" ]; then
            return 0
        fi

        "$APACHE_HTTPD_BIN" -X -f "$CONFIG_FILE" > "$LOG_DIR/httpd.log" 2>&1 &
        HTTPD_PID=$!

        if [ "$MSCONNECTOR_SMOKE_STAGE" = "start_smoke" ]; then
            sleep 1
            if kill -0 "$HTTPD_PID" >/dev/null 2>&1; then
                return 0
            fi
            fail "Apache exited during request-free start smoke; see $LOG_DIR/httpd.log"
        fi

        ready=0
        i=0
        while [ "$i" -lt 30 ]; do
            if ! kill -0 "$HTTPD_PID" >/dev/null 2>&1; then
                if [ "$attempt" -lt "$PORT_RETRY_LIMIT" ] && bind_conflict_seen; then
                    cleanup
                    attempt=$((attempt + 1))
                    PORT=$((PORT + 1))
                    echo "apache_smoke: retrying after bind conflict attempt=$attempt"
                    echo "info: retrying after bind conflict attempt=$attempt" >> "$STATUS_FILE"
                    continue 2
                fi
                fail "Apache exited before request; see $LOG_DIR/httpd.log"
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
        fail "Apache did not become ready on 127.0.0.1:$PORT"
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
    request_url_path=$(quote_request_path "$REQUEST_PATH")
    set -- "$@" "http://127.0.0.1:$PORT$request_url_path"
    "$@" 2>"$LOG_DIR/curl-attack.err"
}

quote_request_path() {
    request_path=$1
    "$PYTHON_BIN" - "$request_path" <<'PY'
import sys
from urllib.parse import quote

print(quote(sys.argv[1], safe="/:?&=%+$,;@[]!'()*"))
PY
}

response_header_backend_needed() {
    [ "$MSCONNECTOR_FULL_LIFECYCLE_SYNC" = "1" ] && return 0
    grep -Eq "RESPONSE_HEADERS:([Cc]ontent-[Tt]ype|[Ll]ocation|[Ss]et-[Cc]ookie)" "$RULES_FILE"
}

start_response_header_backend() {
    response_header_backend_needed || return 0
    if [ "$MSCONNECTOR_FULL_LIFECYCLE_SYNC" = "1" ]; then
        start_synchronized_upstream
        return 0
    fi
    RESPONSE_HEADER_BACKEND_PORT=$(select_free_port $((PORT + 1000)) "$PORT_SEARCH_LIMIT") || \
        blocked "no free response-header backend port found"
    "$PYTHON_BIN" "$REPO_ROOT/ci/response-header-test-backend.py" \
        --port "$RESPONSE_HEADER_BACKEND_PORT" \
        --body-file "$DOCROOT/index.html" \
        --safe-root "$RUNTIME_ROOT" \
        >"$LOG_DIR/response-header-backend.stdout.log" \
        2>"$LOG_DIR/response-header-backend.stderr.log" &
    RESPONSE_HEADER_BACKEND_PID=$!
    wait_tcp_port "$RESPONSE_HEADER_BACKEND_PORT" || blocked "response-header backend failed to start"
}

write_backend_proxy_directives() {
    output=$1
    : > "$output"
    response_header_backend_needed || return 0
    {
        echo "# Generated proxy route for response-header smoke cases."
        echo "<IfModule proxy_module>"
        echo "<IfModule proxy_http_module>"
        echo "ProxyPass \"/__modsec_smoke_ready\" \"!\""
        echo "ProxyPass \"/\" \"http://127.0.0.1:$RESPONSE_HEADER_BACKEND_PORT/\""
        echo "ProxyPassReverse \"/\" \"http://127.0.0.1:$RESPONSE_HEADER_BACKEND_PORT/\""
        echo "$IFMODULE_END"
        echo "$IFMODULE_END"
    } > "$output"
}

require_crs_preamble_if_needed() {
    if [ "$MODSECURITY_TEST_VARIANT" = "with-crs" ] && [ -z "$MODSECURITY_RULE_PREAMBLE_FILE" ]; then
        blocked "MODSECURITY_RULE_PREAMBLE_FILE is required for MODSECURITY_TEST_VARIANT=with-crs; run make test-with-crs or make prepare-crs"
    fi
}

require_crs_preamble_if_needed

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

echo "apache_smoke: BUILD_ROOT=$BUILD_ROOT"
echo "apache_smoke: APACHE_BUILD_ROOT=$APACHE_BUILD_ROOT"
echo "apache_smoke: HTTPD_PREFIX=$HTTPD_PREFIX"
echo "apache_smoke: RUNTIME_ROOT=$RUNTIME_ROOT"
echo "apache_smoke: LOG_DIR=$LOG_DIR"
echo "apache_smoke: APACHE_MODULE=$APACHE_MODULE"
echo "apache_smoke: TEST_CASE=$TEST_CASE"
echo "apache_smoke: CASE_SCOPE=$CASE_SCOPE"
echo "apache_smoke: MODSECURITY_TEST_VARIANT=$MODSECURITY_TEST_VARIANT"
echo "apache_smoke: MSCONNECTOR_SMOKE_STAGE=$MSCONNECTOR_SMOKE_STAGE"
if [ -n "$MODSECURITY_RULE_PREAMBLE_FILE" ]; then
    echo "apache_smoke: MODSECURITY_RULE_PREAMBLE_FILE=$MODSECURITY_RULE_PREAMBLE_FILE"
fi

require_absolute_generated_path "$BUILD_ROOT" "BUILD_ROOT"
require_absolute_generated_path "$APACHE_BUILD_ROOT" "APACHE_BUILD_ROOT"
require_absolute_generated_path "$HTTPD_PREFIX" "HTTPD_PREFIX"
require_absolute_generated_path "$RUNTIME_ROOT" "RUNTIME_ROOT"
require_absolute_generated_path "$LOG_DIR" "LOG_DIR"

RUNTIME_PID_FILE="$RUNTIME_ROOT/logs/httpd.pid"

mkdir -p "$LOG_DIR" "$LOG_DIR/audit" "$RUNTIME_ROOT/conf" "$RUNTIME_ROOT/logs" "$RUNTIME_ROOT/htdocs" "$RUNTIME_ROOT/run"
: > "$STATUS_FILE"
stop_stale_runtime_pid "$RUNTIME_PID_FILE"
rm -f "$RUNTIME_ROOT/logs/"* \
    "$LOG_DIR/configtest.log" \
    "$LOG_DIR/curl-attack.err" \
    "$LOG_DIR/curl-ready.err" \
    "$LOG_DIR/httpd.log" \
    "$LOG_DIR/access.log" \
    "$LOG_DIR/error.log" \
    "$LOG_DIR/phase4.log" \
    "$LOG_DIR/response-body.txt" \
    "$LOG_DIR/audit.log"
rm -f "$LOG_DIR/audit/"*

APACHE_HTTPD_BIN=$(find_apache)
APXS_BIN=$(find_apxs)
case "$MSCONNECTOR_SMOKE_STAGE" in
    config_load|start_smoke|minimal_runtime_smoke) ;;
    *) fail "unsupported MSCONNECTOR_SMOKE_STAGE=$MSCONNECTOR_SMOKE_STAGE" ;;
esac

if [ "$MSCONNECTOR_SMOKE_STAGE" = "minimal_runtime_smoke" ]; then
    CURL_BIN=$(find_curl)
else
    CURL_BIN=
fi

[ -n "$APACHE_HTTPD_BIN" ] || blocked "missing Apache httpd executable; set APACHE_HTTPD=/path/to/apache2-or-httpd"
[ -x "$APACHE_HTTPD_BIN" ] || blocked "Apache executable is not executable: $APACHE_HTTPD_BIN"
if [ "$MSCONNECTOR_SMOKE_STAGE" = "minimal_runtime_smoke" ]; then
    [ -n "$CURL_BIN" ] || blocked "missing curl; set CURL=/path/to/curl"
    [ -x "$CURL_BIN" ] || blocked "curl is not executable: $CURL_BIN"
fi
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
MIME_TYPES_FILE="$RUNTIME_ROOT/conf/mime.types"
DOCROOT="$RUNTIME_ROOT/htdocs"
APACHE_BACKEND_PROXY_FILE="$RUNTIME_ROOT/conf/backend-proxy.conf"
RESPONSE_BODY="$LOG_DIR/response-body.txt"
CASE_ENV_FILE="$RUNTIME_ROOT/conf/case.env"
REQUEST_HEADERS_FILE="$RUNTIME_ROOT/conf/request-headers.txt"
REQUEST_BODY_FILE="$RUNTIME_ROOT/conf/request-body.bin"
AUDIT_LOG_FILE="$LOG_DIR/audit.log"
AUDIT_LOG_DIR="$LOG_DIR/audit"
APACHE_PHASE4_LOG_FILE="$LOG_DIR/phase4.log"

if [ -f "$HTTPD_PREFIX/conf/mime.types" ]; then
    cp -a "$HTTPD_PREFIX/conf/mime.types" "$MIME_TYPES_FILE"
else
    : > "$MIME_TYPES_FILE"
fi
if ! "$PYTHON_BIN" "$CASE_CLI" materialize \
    --case "$TEST_CASE" \
    --rules-file "$RULES_FILE" \
    --env-file "$CASE_ENV_FILE" \
    --headers-file "$REQUEST_HEADERS_FILE" \
    --body-file "$REQUEST_BODY_FILE" \
    --docroot "$DOCROOT" \
    --audit-log-file "$AUDIT_LOG_FILE" \
    --audit-log-dir "$AUDIT_LOG_DIR" \
    --rules-preamble-file "$MODSECURITY_RULE_PREAMBLE_FILE" > "$LOG_DIR/case-materialize.log" 2>&1; then
    not_executable "failed to materialize shared case; see $LOG_DIR/case-materialize.log"
fi
. "$CASE_ENV_FILE"
start_response_header_backend
write_backend_proxy_directives "$APACHE_BACKEND_PROXY_FILE"

: > "$MODULES_FILE"
if modules_dir=$(apache_modules_dir); then
    append_mpm_if_needed "$modules_dir" "$MODULES_FILE"
    append_load_if_exists "authz_core_module" "mod_authz_core.so" "$modules_dir" "$MODULES_FILE"
    append_load_if_exists "authz_host_module" "mod_authz_host.so" "$modules_dir" "$MODULES_FILE"
    append_load_if_exists "unixd_module" "mod_unixd.so" "$modules_dir" "$MODULES_FILE"
    append_load_if_exists "dir_module" "mod_dir.so" "$modules_dir" "$MODULES_FILE"
    append_load_if_exists "mime_module" "mod_mime.so" "$modules_dir" "$MODULES_FILE"
    append_load_if_exists "proxy_module" "mod_proxy.so" "$modules_dir" "$MODULES_FILE"
    append_load_if_exists "proxy_http_module" "mod_proxy_http.so" "$modules_dir" "$MODULES_FILE"
    append_load_if_exists "log_config_module" "mod_log_config.so" "$modules_dir" "$MODULES_FILE"
fi

LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR:$HTTPD_PREFIX/lib:$PCRE2_PREFIX/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH

trap cleanup EXIT INT TERM
start_server

if [ "$MSCONNECTOR_SMOKE_STAGE" = "config_load" ]; then
    echo "apache_smoke: pass config_load (no process started, no request sent)"
    exit 0
fi
if [ "$MSCONNECTOR_SMOKE_STAGE" = "start_smoke" ]; then
    echo "apache_smoke: pass start_smoke (request-free host liveness verified)"
    exit 0
fi

if [ "$MSCONNECTOR_FULL_LIFECYCLE_SYNC" = "1" ]; then
    send_synchronized_first_byte_request
    echo "apache_smoke: pass synchronized-first-byte"
    exit 0
fi

set +e
http_status=$(send_case_request)
curl_rc=$?
set -e
observed_transport_result=http_status
if [ "$curl_rc" -ne 0 ]; then
    observed_transport_result=connection_aborted
fi
printf '%s\n' "$http_status" > "$LOG_DIR/observed-status.txt"
printf '%s\n' "$observed_transport_result" > "$LOG_DIR/observed-transport-result.txt"

if "$PYTHON_BIN" "$CASE_CLI" assert-status \
    --case "$TEST_CASE" \
    --actual-status "$http_status" \
    --observed-transport-result "$observed_transport_result" \
    --response-body-file "$RESPONSE_BODY" \
    --audit-log-file "$AUDIT_LOG_FILE" \
    --phase4-log-file "$APACHE_PHASE4_LOG_FILE" \
    --status-file "$STATUS_FILE" > "$LOG_DIR/case-assert.log" 2>&1; then
    write_case_result "$TEST_CASE" pass "$http_status" "$LOG_DIR/result.json" "$observed_transport_result" || true
    echo "apache_smoke: pass case=$CASE_NAME status=$http_status"
    exit 0
fi

reason=$(cat "$LOG_DIR/case-assert.log" 2>/dev/null || true)
if [ "$curl_rc" -ne 0 ]; then
    reason="curl attack request failed rc=$curl_rc; $reason"
fi
write_case_result "$TEST_CASE" fail "$http_status" "$LOG_DIR/result.json" "$observed_transport_result" "$reason" || true
echo "apache_smoke: fail case=$CASE_NAME observed=$http_status expected=$EXPECT_STATUS"
exit 1
