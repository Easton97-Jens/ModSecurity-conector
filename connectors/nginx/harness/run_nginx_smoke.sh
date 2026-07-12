#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd "$SCRIPT_DIR/../../.." && pwd)
FRAMEWORK_ROOT="${FRAMEWORK_ROOT:-$REPO_ROOT/modules/ModSecurity-test-Framework}"
[ -d "$FRAMEWORK_ROOT" ] || { echo "nginx_smoke: blocked FRAMEWORK_ROOT is missing; run git submodule update --init --recursive or set FRAMEWORK_ROOT=/path/to/ModSecurity-test-Framework"; exit 77; }
VERIFIED_RUN_ROOT="${VERIFIED_RUN_ROOT:-${RUNNER_TEMP:-${TMPDIR:-/var/tmp}}/ModSecurity-conector-verified}"
VERIFIED_BUILD_ROOT="${VERIFIED_BUILD_ROOT:-$VERIFIED_RUN_ROOT/build}"
BUILD_ROOT="${BUILD_ROOT:-$VERIFIED_BUILD_ROOT}"
NGINX_HARNESS_PARENT="${NGINX_HARNESS_PARENT:-$VERIFIED_RUN_ROOT/nginx-harness}"
CURRENT_UID=$(id -u 2>/dev/null || printf 'unknown')
if [ -z "${NGINX_HARNESS_WORK_ROOT:-}" ]; then
    if [ "$CURRENT_UID" = "0" ]; then
        parent_perms=$(stat -c '%A' "$NGINX_HARNESS_PARENT" 2>/dev/null || printf '')
        case "$parent_perms" in
            ?????????[xt]) ;;
            *)
                fallback_parent="/var/tmp"
                fallback_perms=$(stat -c '%A' "$fallback_parent" 2>/dev/null || printf '')
                case "$fallback_perms" in
                    ?????????[xt]) NGINX_HARNESS_PARENT="$fallback_parent" ;;
                    *) ;;
                esac
                ;;
        esac
    fi
    if [ ! -d "$NGINX_HARNESS_PARENT" ]; then
        install -d -m 755 "$NGINX_HARNESS_PARENT"
    fi
    NGINX_HARNESS_WORK_ROOT=$(mktemp -d "$NGINX_HARNESS_PARENT/ModSecurity-conector-nginx-runtime-$CURRENT_UID-XXXXXX")
fi
NGINX_BUILD_DIR="${NGINX_BUILD_DIR:-$BUILD_ROOT/nginx-build}"
NGINX_PREFIX="${NGINX_PREFIX:-$BUILD_ROOT/nginx-runtime/nginx}"
NGINX_BINARY="${NGINX_BINARY:-$NGINX_PREFIX/sbin/nginx}"
NGINX_MODULE="${NGINX_MODULE:-$NGINX_PREFIX/modules/ngx_http_modsecurity_module.so}"
MODSECURITY_LIB_DIR="${MODSECURITY_LIB_DIR:-$NGINX_BUILD_DIR/output/modsecurity/lib}"
LOG_DIR="${LOG_DIR:-$NGINX_HARNESS_WORK_ROOT/logs}"
RESULTS_DIR="${RESULTS_DIR:-$BUILD_ROOT/results}"
if [ -n "${FORCE_ALL_CASES:-}" ] && [ "$RESULTS_DIR" = "$BUILD_ROOT/results" ]; then
    RESULTS_DIR="$BUILD_ROOT/results/force-all"
fi
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
NO_CRS_SELECTED_CASE_IDS="${NO_CRS_SELECTED_CASE_IDS:-}"
CASE_SCOPE="${CASE_SCOPE:-all}"
CASE_CLI="$FRAMEWORK_ROOT/tests/runners/case_cli.py"
RUN_ONE_CASE="${RUN_ONE_CASE:-0}"
MSCONNECTOR_SMOKE_STAGE="${MSCONNECTOR_SMOKE_STAGE:-minimal_runtime_smoke}"
STATUS_FILE="$LOG_DIR/status.txt"
CONNECTOR_ORIGIN_SOURCE="${CONNECTOR_ORIGIN_SOURCE:-}"
CONNECTOR_ORIGIN_SOURCE_REPO="${CONNECTOR_ORIGIN_SOURCE_REPO:-}"
CONNECTOR_ORIGIN_SOURCE_URL="${CONNECTOR_ORIGIN_SOURCE_URL:-}"
CONNECTOR_ORIGIN_SOURCE_COMMIT="${CONNECTOR_ORIGIN_SOURCE_COMMIT:-}"
CONNECTOR_ORIGIN_SOURCE_VERSION="${CONNECTOR_ORIGIN_SOURCE_VERSION:-}"
CONNECTOR_ORIGIN_LICENSE="${CONNECTOR_ORIGIN_LICENSE:-}"
CONNECTOR_ORIGIN_IMPORTED_PATH="${CONNECTOR_ORIGIN_IMPORTED_PATH:-}"
MODSECURITY_TEST_VARIANT="${MODSECURITY_TEST_VARIANT:-}"
MODSECURITY_RULE_PREAMBLE_FILE="${MODSECURITY_RULE_PREAMBLE_FILE:-}"
NGINX_WORKER_USER="${NGINX_WORKER_USER:-nobody}"
NGINX_WORKER_GROUP="${NGINX_WORKER_GROUP:-}"
PERMISSIONS_LOG="${PERMISSIONS_LOG:-}"
MSCONNECTOR_FULL_LIFECYCLE_SYNC="${MSCONNECTOR_FULL_LIFECYCLE_SYNC:-0}"
FULL_LIFECYCLE_EVIDENCE_OUTPUT="${FULL_LIFECYCLE_EVIDENCE_OUTPUT:-}"
SYNCHRONIZED_UPSTREAM="$FRAMEWORK_ROOT/tests/runners/synchronized_upstream.py"

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

not_executable() {
    echo "nginx_smoke: not_executable $*"
    mkdir -p "$LOG_DIR"
    echo "not_executable: $*" >> "$STATUS_FILE"
    exit 78
}

configtest_case_not_executable() {
    grep -E "Rules error|modsecurity-smoke\\.conf|modsecurity_rules_file|modsecurity_rules" \
        "$LOG_DIR/configtest.log" >/dev/null 2>&1
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

append_worker_preflight_record() {
    check_name=$1
    check_status=$2
    check_path=$3
    check_notes=$4
    preflight_file="${NGINX_WORKER_PREFLIGHT_FILE:-$LOG_DIR/nginx-worker-preflight.jsonl}"
    mkdir -p "$(dirname "$preflight_file")"
    "$PYTHON_BIN" - "$preflight_file" "$check_name" "$check_status" "$check_path" "$check_notes" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
record = {
    "check": sys.argv[2],
    "status": sys.argv[3],
    "path": sys.argv[4],
    "notes": sys.argv[5],
}
with path.open("a", encoding="utf-8") as handle:
    handle.write(json.dumps(record, sort_keys=True) + "\n")
PY
}

nginx_worker_can_access() {
    access_mode=$1
    access_path=$2
    if command -v runuser >/dev/null 2>&1 && [ "$CURRENT_UID" = "0" ] && id "$NGINX_WORKER_USER" >/dev/null 2>&1; then
        runuser -u "$NGINX_WORKER_USER" -- test "$access_mode" "$access_path"
        return $?
    fi
    test "$access_mode" "$access_path"
}

nginx_worker_access_notes() {
    if command -v runuser >/dev/null 2>&1 && [ "$CURRENT_UID" = "0" ] && id "$NGINX_WORKER_USER" >/dev/null 2>&1; then
        printf 'checked with runuser -u %s' "$NGINX_WORKER_USER"
    else
        printf 'runuser worker check unavailable; used current process stat/test fallback'
    fi
}

preflight_nginx_worker_docroot() {
    preflight_file="${NGINX_WORKER_PREFLIGHT_FILE:-$LOG_DIR/nginx-worker-preflight.jsonl}"
    : > "$preflight_file"
    preflight_failed=0
    index_file="$DOCROOT/index.html"

    case "$NGINX_HARNESS_PARENT" in
        /root|/root/*)
            append_worker_preflight_record "Path under /root" "FAIL" "$NGINX_HARNESS_PARENT" "NGINX_HARNESS_PARENT must not be under /root"
            preflight_failed=1
            ;;
        *)
            append_worker_preflight_record "Path under /root" "PASS" "$NGINX_HARNESS_PARENT" "NGINX_HARNESS_PARENT is outside /root"
            ;;
    esac
    case "$NGINX_HARNESS_WORK_ROOT" in
        /root|/root/*)
            append_worker_preflight_record "Work root under /root" "FAIL" "$NGINX_HARNESS_WORK_ROOT" "NGINX_HARNESS_WORK_ROOT must not be under /root"
            preflight_failed=1
            ;;
        *)
            append_worker_preflight_record "Work root under /root" "PASS" "$NGINX_HARNESS_WORK_ROOT" "NGINX_HARNESS_WORK_ROOT is outside /root"
            ;;
    esac

    if [ -f "$index_file" ]; then
        append_worker_preflight_record "DOCROOT/index.html exists" "PASS" "$index_file" "materialized before NGINX start"
    else
        append_worker_preflight_record "DOCROOT/index.html exists" "FAIL" "$index_file" "materialized docroot index is missing"
        preflight_failed=1
    fi

    if command -v namei >/dev/null 2>&1; then
        namei -l "$index_file" > "$LOG_DIR/namei-docroot-index.log" 2>&1 || true
    else
        printf '%s\n' "namei unavailable" > "$LOG_DIR/namei-docroot-index.log"
    fi

    access_notes=$(nginx_worker_access_notes)
    if nginx_worker_can_access -x "$NGINX_HARNESS_PARENT"; then
        append_worker_preflight_record "Harness parent traversable" "PASS" "$NGINX_HARNESS_PARENT" "$access_notes"
    else
        append_worker_preflight_record "Harness parent traversable" "FAIL" "$NGINX_HARNESS_PARENT" "$access_notes"
        preflight_failed=1
    fi
    if nginx_worker_can_access -x "$DOCROOT"; then
        append_worker_preflight_record "NGINX worker can traverse docroot" "PASS" "$DOCROOT" "$access_notes"
    else
        append_worker_preflight_record "NGINX worker can traverse docroot" "FAIL" "$DOCROOT" "$access_notes"
        preflight_failed=1
    fi
    if nginx_worker_can_access -r "$index_file"; then
        append_worker_preflight_record "htdocs/index.html readable by worker" "PASS" "$index_file" "$access_notes"
    else
        append_worker_preflight_record "htdocs/index.html readable by worker" "FAIL" "$index_file" "$access_notes"
        preflight_failed=1
    fi
    append_worker_preflight_record "try_files fallback guarded" "$([ "$preflight_failed" -eq 0 ] && printf PASS || printf FAIL)" "$index_file" "docroot readability is checked before try_files /index.html can loop"

    if [ "$preflight_failed" -ne 0 ]; then
        write_permission_diagnostics
        echo "BLOCKED: nginx worker cannot access harness docroot"
        blocked "nginx worker cannot access harness docroot"
    fi
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

append_smoke_case() {
    fixture=$1
    case " $SMOKE_CASES " in
        *" $fixture "*|*" $fixture.yaml "*) return 0 ;;
    esac
    SMOKE_CASES="${SMOKE_CASES}${SMOKE_CASES:+ }$fixture"
}

append_selected_phase4_fixtures() {
    # The canonical catalog remains connector-neutral.  NGINX maps only its
    # real, post-header safe/strict host paths to dedicated fixtures, whose
    # YAML names are the canonical case IDs.  Never synthesize a pre-commit
    # result from this body-filter path.
    case "${NO_CRS_BASELINE:-}" in
        1|true|TRUE|yes|YES|on|ON) ;;
        *) return 0 ;;
    esac
    [ "$RUN_ONE_CASE" != "1" ] || return 0
    [ -n "$NO_CRS_SELECTED_CASE_IDS" ] || return 0

    set -f
    for case_id in $NO_CRS_SELECTED_CASE_IDS; do
        case "$case_id" in
            phase4_deny_after_commit_log_only)
                append_smoke_case nginx_phase4_deny_after_commit_log_only
                ;;
            phase4_deny_after_commit_abort)
                append_smoke_case nginx_phase4_deny_after_commit_abort
                ;;
            *[!A-Za-z0-9_]*|"")
                set +f
                blocked "unsafe canonical case id: $case_id"
                ;;
            *)
                # Other canonical IDs either have a catalog-owned runner
                # fixture or are derived from the real safe/strict events.
                ;;
        esac
    done
    set +f
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
            --connector nginx \
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
            --connector nginx \
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
    summary_file="$RESULTS_DIR/nginx-summary.txt"
    json_file="$RESULTS_DIR/nginx-summary.json"
    results_jsonl="$RESULTS_DIR/nginx-results.jsonl"
    connector_summary="$RESULTS_DIR/connector-summary.txt"
    : > "$summary_file"
    : > "$results_jsonl"

    append_selected_phase4_fixtures
    cases=$(list_case_files) || exit 1
    if [ -z "$cases" ]; then
        echo "nginx_smoke: fail no shared smoke cases found" >&2
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
        --origin-imported-path "$CONNECTOR_ORIGIN_IMPORTED_PATH" \
        --runtime-mode "$([ -n "${FORCE_ALL_CASES:-}" ] && printf force-all || printf default)" \
        --command "$([ -n "${FORCE_ALL_CASES:-}" ] && printf 'FORCE_ALL_CASES=1 make smoke-nginx' || printf 'make smoke-nginx')" \
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

find_curl() {
    if [ -n "$CURL_BIN" ]; then
        printf '%s\n' "$CURL_BIN"
        return 0
    fi
    command -v curl 2>/dev/null || true
}

record_nginx_http2_applicability() {
    version_log="$LOG_DIR/nginx-version.log"
    applicability_file="$LOG_DIR/nginx-http2-applicability.json"

    if ! "$NGINX_BINARY" -V > "$version_log" 2>&1; then
        blocked "NGINX host probe failed: $NGINX_BINARY -V; see $version_log"
    fi

    "$PYTHON_BIN" - "$version_log" "$applicability_file" "$NGINX_BINARY" <<'PY'
import json
import sys
from pathlib import Path

version_log = Path(sys.argv[1])
output = Path(sys.argv[2])
binary = sys.argv[3]
configure_output = version_log.read_text(encoding="utf-8", errors="replace")
http2_enabled = "--with-http_v2_module" in configure_output

payload = {
    "evidence_origin": "real_host_build",
    "nginx_binary": binary,
    "nginx_v_log": str(version_log),
    "http2_configure_flag": http2_enabled,
    # A build flag alone is not HTTP/2 lifecycle evidence.  The current native
    # harness has no selected HTTP/2-specific case or TLS/h2c listener setup.
    "status": "NOT_EXECUTED" if http2_enabled else "NOT_APPLICABLE",
    "reason": (
        "host advertises --with-http_v2_module, but this invocation has no "
        "connector-owned HTTP/2 case or HTTP/2 listener configuration"
        if http2_enabled
        else "nginx -V lacks --with-http_v2_module; HTTP/2 cannot be exercised"
    ),
}
output.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")
PY
}

escape_sed() {
    raw_value=$1
    printf '%s' "$raw_value" | sed 's/[&|]/\\&/g'
}

render_config() {
    NGINX_PHASE4_MODE_DIRECTIVE=""
    case "${NGINX_PHASE4_MODE:-}" in
        "") ;;
        minimal|safe|strict)
            NGINX_PHASE4_MODE_DIRECTIVE="modsecurity_phase4_mode $NGINX_PHASE4_MODE;"
            ;;
        *)
            fail "unsupported generated NGINX_PHASE4_MODE=$NGINX_PHASE4_MODE"
            ;;
    esac
    sed \
        -e "s|@@RUNTIME_ROOT@@|$(escape_sed "$RUNTIME_ROOT")|g" \
        -e "s|@@LOG_DIR@@|$(escape_sed "$LOG_DIR")|g" \
        -e "s|@@PORT@@|$(escape_sed "$PORT")|g" \
        -e "s|@@NGINX_MODULE@@|$(escape_sed "$NGINX_MODULE")|g" \
        -e "s|@@DOCROOT@@|$(escape_sed "$DOCROOT")|g" \
        -e "s|@@RULES_FILE@@|$(escape_sed "$RULES_FILE")|g" \
        -e "s|@@NGINX_PHASE4_LOG@@|$(escape_sed "$NGINX_PHASE4_LOG_FILE")|g" \
        -e "s|@@NGINX_PHASE4_MODE_DIRECTIVE@@|$(escape_sed "$NGINX_PHASE4_MODE_DIRECTIVE")|g" \
        -e "s|@@NGINX_LOCATION_DIRECTIVES@@|$(escape_sed "$NGINX_LOCATION_DIRECTIVES_FILE")|g" \
        -e "s|@@NGINX_LOCATION_HANDLER_DIRECTIVES@@|$(escape_sed "$NGINX_LOCATION_HANDLER_DIRECTIVES_FILE")|g" \
        "$TEMPLATE" > "$CONFIG_FILE"
}

cleanup() {
    if [ -n "${SYNCHRONIZED_UPSTREAM_PID:-}" ] && kill -0 "$SYNCHRONIZED_UPSTREAM_PID" >/dev/null 2>&1; then
        [ -n "${SYNCHRONIZED_RELEASE_FILE:-}" ] && : > "$SYNCHRONIZED_RELEASE_FILE"
        kill "$SYNCHRONIZED_UPSTREAM_PID" >/dev/null 2>&1 || true
        wait "$SYNCHRONIZED_UPSTREAM_PID" >/dev/null 2>&1 || true
    fi
    if [ -n "${NGINX_PID:-}" ] && kill -0 "$NGINX_PID" >/dev/null 2>&1; then
        kill "$NGINX_PID" >/dev/null 2>&1 || true
        wait "$NGINX_PID" >/dev/null 2>&1 || true
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
    [ -s "$NGINX_PHASE4_LOG_FILE" ] || fail "Phase-4 host log is missing after synchronized response"
    FIRST_BYTE_HOST_METADATA="$SYNCHRONIZED_DIR/host-metadata.json"
    "$PYTHON_BIN" "$REPO_ROOT/ci/write-first-byte-host-metadata.py" \
        --phase4-log "$NGINX_PHASE4_LOG_FILE" --output "$FIRST_BYTE_HOST_METADATA" || \
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
            if configtest_case_not_executable; then
                not_executable "NGINX rejected generated ModSecurity rules; see $LOG_DIR/configtest.log"
            fi
            fail "NGINX configtest failed; see $LOG_DIR/configtest.log"
        fi

        if [ "$MSCONNECTOR_SMOKE_STAGE" = "config_load" ]; then
            return 0
        fi

        "$NGINX_BINARY" -p "$RUNTIME_ROOT" -c "$CONFIG_FILE" > "$LOG_DIR/nginx-stdout.log" 2>&1 &
        NGINX_PID=$!

        if [ "$MSCONNECTOR_SMOKE_STAGE" = "start_smoke" ]; then
            sleep 1
            if kill -0 "$NGINX_PID" >/dev/null 2>&1; then
                return 0
            fi
            fail "NGINX exited during request-free start smoke; see $LOG_DIR/nginx-stdout.log and $LOG_DIR/error.log"
        fi

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
    grep -Eqi '(^|[^[:alnum:]_])RESPONSE_HEADERS([[:space:]:]|$)' "$RULES_FILE"
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
        --fixture-file "$RESPONSE_HEADER_FIXTURE_FILE" \
        >"$LOG_DIR/response-header-backend.stdout.log" \
        2>"$LOG_DIR/response-header-backend.stderr.log" &
    RESPONSE_HEADER_BACKEND_PID=$!
    wait_tcp_port "$RESPONSE_HEADER_BACKEND_PORT" || blocked "response-header backend failed to start"
}

write_location_handler_directives() {
    output=$1
    : > "$output"
    if response_header_backend_needed; then
        {
            echo "# Generated proxy route for response-header smoke cases."
            echo "proxy_pass http://127.0.0.1:$RESPONSE_HEADER_BACKEND_PORT;"
            # The synchronized first-byte proof observes a client-visible
            # chunk while the upstream is paused.  NGINX's default proxy
            # buffering can defer that chunk until EOS, which would test its
            # buffer policy rather than the connector's forwarding path.
            if [ "$MSCONNECTOR_FULL_LIFECYCLE_SYNC" = "1" ]; then
                echo "proxy_buffering off;"
            fi
            echo "proxy_set_header Host \$host;"
        } > "$output"
        return 0
    fi
    {
        echo "error_page 405 =200 /index.html;"
        echo "try_files \$uri \$uri/ /index.html;"
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
echo "nginx_smoke: MODSECURITY_TEST_VARIANT=$MODSECURITY_TEST_VARIANT"
echo "nginx_smoke: MSCONNECTOR_SMOKE_STAGE=$MSCONNECTOR_SMOKE_STAGE"
if [ -n "$MODSECURITY_RULE_PREAMBLE_FILE" ]; then
    echo "nginx_smoke: MODSECURITY_RULE_PREAMBLE_FILE=$MODSECURITY_RULE_PREAMBLE_FILE"
fi

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
	    "$LOG_DIR/nginx-version.log" \
	    "$LOG_DIR/nginx-http2-applicability.json" \
    "$LOG_DIR/curl-attack.err" \
	    "$LOG_DIR/curl-ready.err" \
	    "$LOG_DIR/nginx.log" \
	    "$LOG_DIR/nginx-stdout.log" \
	    "$LOG_DIR/phase4.log" \
	    "$LOG_DIR/response-body.txt" \
	    "$LOG_DIR/audit.log" \
	    "$RUNTIME_ROOT/nginx.pid"
rm -f "$LOG_DIR/audit/"*

case "$MSCONNECTOR_SMOKE_STAGE" in
    config_load|start_smoke|minimal_runtime_smoke) ;;
    *) fail "unsupported MSCONNECTOR_SMOKE_STAGE=$MSCONNECTOR_SMOKE_STAGE" ;;
esac

if [ "$MSCONNECTOR_SMOKE_STAGE" = "minimal_runtime_smoke" ]; then
    CURL_BIN=$(find_curl)
else
    CURL_BIN=
fi

[ -x "$NGINX_BINARY" ] || blocked "missing executable NGINX binary: $NGINX_BINARY"
[ -f "$NGINX_MODULE" ] || blocked "missing NGINX ModSecurity dynamic module: $NGINX_MODULE"
record_nginx_http2_applicability
if [ "$MSCONNECTOR_SMOKE_STAGE" = "minimal_runtime_smoke" ]; then
    [ -n "$CURL_BIN" ] || blocked "missing curl; set CURL=/path/to/curl"
    [ -x "$CURL_BIN" ] || blocked "curl is not executable: $CURL_BIN"
fi
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
NGINX_LOCATION_HANDLER_DIRECTIVES_FILE="$RUNTIME_ROOT/conf/nginx-location-handler-directives.conf"
NGINX_PHASE4_LOG_FILE="$LOG_DIR/phase4.log"
RESPONSE_HEADER_FIXTURE_FILE="$RUNTIME_ROOT/conf/response-header-fixture.json"

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
	    --rules-preamble-file "$MODSECURITY_RULE_PREAMBLE_FILE" \
	    --nginx-location-directives-file "$NGINX_LOCATION_DIRECTIVES_FILE" \
	    --nginx-runtime-config-dir "$RUNTIME_ROOT/conf" \
	    --nginx-phase4-log-file "$NGINX_PHASE4_LOG_FILE" > "$LOG_DIR/case-materialize.log" 2>&1; then
    not_executable "failed to materialize shared case; see $LOG_DIR/case-materialize.log"
fi
. "$CASE_ENV_FILE"
if ! "$PYTHON_BIN" "$REPO_ROOT/ci/harness-case-metadata.py" response-header-fixture \
    --case "$TEST_CASE" \
    --framework-root "$FRAMEWORK_ROOT" \
    --output "$RESPONSE_HEADER_FIXTURE_FILE" > "$LOG_DIR/response-header-fixture.log" 2>&1; then
    not_executable "failed to materialize response-header backend fixture; see $LOG_DIR/response-header-fixture.log"
fi
start_response_header_backend
write_location_handler_directives "$NGINX_LOCATION_HANDLER_DIRECTIVES_FILE"
ensure_worker_runtime_permissions
preflight_nginx_worker_docroot

LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR:$NGINX_PREFIX/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH

trap cleanup EXIT INT TERM
start_server

if [ "$MSCONNECTOR_SMOKE_STAGE" = "config_load" ]; then
    echo "nginx_smoke: pass config_load (no process started, no request sent)"
    exit 0
fi
if [ "$MSCONNECTOR_SMOKE_STAGE" = "start_smoke" ]; then
    echo "nginx_smoke: pass start_smoke (request-free host liveness verified)"
    exit 0
fi

if [ "$MSCONNECTOR_FULL_LIFECYCLE_SYNC" = "1" ]; then
    send_synchronized_first_byte_request
    echo "nginx_smoke: pass synchronized-first-byte"
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
	    --phase4-log-file "$NGINX_PHASE4_LOG_FILE" \
	    --status-file "$STATUS_FILE" > "$LOG_DIR/case-assert.log" 2>&1; then
    write_case_result "$TEST_CASE" pass "$http_status" "$LOG_DIR/result.json" "$observed_transport_result" || true
    echo "nginx_smoke: pass case=$CASE_NAME status=$http_status"
    exit 0
fi

reason=$(cat "$LOG_DIR/case-assert.log" 2>/dev/null || true)
if [ "$curl_rc" -ne 0 ]; then
    reason="curl attack request failed rc=$curl_rc; $reason"
fi
write_case_result "$TEST_CASE" fail "$http_status" "$LOG_DIR/result.json" "$observed_transport_result" "$reason" || true
if [ "$http_status" = "403" ] && nginx_docroot_permission_denied; then
    write_case_result "$TEST_CASE" blocked "$http_status" "$LOG_DIR/result.json" "$observed_transport_result" "NGINX could not read generated docroot" || true
    write_permission_diagnostics
    blocked "NGINX could not read generated docroot; see $LOG_DIR/error.log and $LOG_DIR/permissions.log"
fi
echo "nginx_smoke: fail case=$CASE_NAME observed=$http_status expected=$EXPECT_STATUS"
exit 1
