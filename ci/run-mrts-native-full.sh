#!/bin/sh
set -u

CONNECTOR_ROOT="${CONNECTOR_ROOT:-$(CDPATH= cd "$(dirname "$0")/.." && pwd)}"
FRAMEWORK_ROOT="${FRAMEWORK_ROOT:-$CONNECTOR_ROOT/modules/ModSecurity-test-Framework}"
DEFAULT_STATE_HOME="${DEFAULT_STATE_HOME:-${XDG_STATE_HOME:-${HOME:-/tmp}/.local/state}}"
BUILD_ROOT="${BUILD_ROOT:-$DEFAULT_STATE_HOME/ModSecurity-conector-build}"
TMP_ROOT="${TMP_ROOT:-$BUILD_ROOT/tmp}"
LOG_ROOT="${LOG_ROOT:-$BUILD_ROOT/logs}"
MRTS_ROOT="${MRTS_ROOT:-$FRAMEWORK_ROOT/tools/MRTS}"
MRTS_BUILD_ROOT="${MRTS_BUILD_ROOT:-$BUILD_ROOT/mrts}"
MRTS_NATIVE_ROOT="${MRTS_NATIVE_ROOT:-$BUILD_ROOT/mrts-native}"
MRTS_NATIVE_TARGETS="${MRTS_NATIVE_TARGETS:-apache2_ubuntu nginx-pr24}"
MRTS_NATIVE_APACHE_PORT="${MRTS_NATIVE_APACHE_PORT:-19080}"
MRTS_NATIVE_NGINX_PORT="${MRTS_NATIVE_NGINX_PORT:-19081}"
MRTS_NATIVE_BACKEND_PORT="${MRTS_NATIVE_BACKEND_PORT:-19082}"
GO_FTW_BIN="${GO_FTW_BIN:-go-ftw}"
ALBEDO_BIN="${ALBEDO_BIN:-albedo}"
PYTHON="${PYTHON:-python3}"
PYTHONDONTWRITEBYTECODE="${PYTHONDONTWRITEBYTECODE:-1}"

export CONNECTOR_ROOT FRAMEWORK_ROOT BUILD_ROOT TMP_ROOT LOG_ROOT MRTS_ROOT MRTS_BUILD_ROOT MRTS_NATIVE_ROOT GO_FTW_BIN ALBEDO_BIN PYTHONDONTWRITEBYTECODE

REPO_ROOT="$CONNECTOR_ROOT"
. "$FRAMEWORK_ROOT/ci/common.sh"

validate_runtime_paths() {
    assert_safe_runtime_path "$BUILD_ROOT" BUILD_ROOT || exit 77
    assert_safe_runtime_path "$TMP_ROOT" TMP_ROOT || exit 77
    assert_safe_runtime_path "$LOG_ROOT" LOG_ROOT || exit 77
    assert_safe_runtime_path "$MRTS_BUILD_ROOT" MRTS_BUILD_ROOT || exit 77
    assert_safe_runtime_path "$MRTS_NATIVE_ROOT" MRTS_NATIVE_ROOT || exit 77
    assert_not_system_path_for_write "$CONNECTOR_ROOT/reports/testing/generated" MRTS_NATIVE_REPORT_DIR || exit 77
}

validate_runtime_paths
mkdir -p "$MRTS_NATIVE_ROOT" "$LOG_ROOT"

json_string() {
    "$PYTHON" - "$1" <<'PY'
import json
import sys
print(json.dumps(sys.argv[1]))
PY
}

write_job_json() {
    job_json=$1
    target=$2
    status=$3
    reason=$4
    exit_code=$5
    duration=$6
    run_log=$7
    summary_path=$8
    "$PYTHON" - "$job_json" "$target" "$status" "$reason" "$exit_code" "$duration" "$run_log" "$summary_path" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
data = {
    "target": sys.argv[2],
    "status": sys.argv[3],
    "reason": sys.argv[4],
    "exit_code": int(sys.argv[5]),
    "duration_seconds": int(sys.argv[6]),
    "run_log": sys.argv[7],
    "summary_path": sys.argv[8],
    "job_json": str(path),
}
path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY
}

require_path() {
    path=$1
    label=$2
    if [ ! -e "$path" ]; then
        printf '%s missing: %s\n' "$label" "$path"
        return 1
    fi
    return 0
}

missing_tools() {
    missing=""
    for tool in "$@"; do
        if ! command_available "$tool"; then
            missing="${missing}${missing:+, }$tool"
        fi
    done
    if [ -n "$missing" ]; then
        printf '%s\n' "$missing"
        return 1
    fi
    return 0
}

command_available() {
    cmd=$1
    case "$cmd" in
        */*) [ -x "$cmd" ] ;;
        *) command -v "$cmd" >/dev/null 2>&1 ;;
    esac
}

append_missing_dep() {
    current=$1
    binary=$2
    env_var=$3
    if [ -n "$current" ]; then
        printf '%s, %s (set %s)' "$current" "$binary" "$env_var"
    else
        printf '%s (set %s)' "$binary" "$env_var"
    fi
}

prepare_mrts_outputs() {
    "$MAKE" -C "$FRAMEWORK_ROOT" mrts-generate >/dev/null
    MRTS_RULES_OUT="$MRTS_BUILD_ROOT/upstream-config-tests/rules" \
    MRTS_LOAD_FILE="$MRTS_BUILD_ROOT/upstream-config-tests/mrts.load" \
        sh "$FRAMEWORK_ROOT/ci/write-mrts-load.sh" >/dev/null
}

patch_common_ftw_config() {
    config=$1
    logfile=$2
    if [ -f "$config" ]; then
        assert_not_system_path_for_write "$config" "native FTW config" || return 77
        sed -i "s#^logfile:.*#logfile: '$(printf '%s' "$logfile" | sed 's#[\\&#]#\\\\&#g')'#" "$config"
    fi
}

stage_apache() {
    target_root=$1
    source_root="$MRTS_ROOT/config_infra/apache2_ubuntu"
    stage="$target_root/stage"
    require_path "$source_root" "MRTS apache native infrastructure" || return 1
    assert_safe_runtime_path "$target_root" "Apache native target root" || return 77
    safe_remove_runtime_path "$stage" "$target_root" "Apache native stage" || return 77
    mkdir -p "$stage"
    cp -a "$source_root/." "$stage/"
    mkdir -p "$stage/infra/log" "$stage/infra/run"
    cp "$MRTS_BUILD_ROOT/upstream-config-tests/mrts.load" "$stage/infra/mrts.load"
    sed -i "s#^Listen 80#Listen $MRTS_NATIVE_APACHE_PORT#" "$stage/infra/ports.conf"
    sed -i "s#<VirtualHost \\*:80>#<VirtualHost *:$MRTS_NATIVE_APACHE_PORT>#" "$stage/infra/sites-available/000-default.conf"
    sed -i "s#http://127.0.0.1:8000/#http://127.0.0.1:$MRTS_NATIVE_BACKEND_PORT/#g" "$stage/infra/sites-available/000-default.conf"
    patch_common_ftw_config "$stage/ftw.mrts.config.yaml" "$stage/infra/log/error.log"
    printf '%s\n' "$stage"
}

stage_nginx() {
    target_root=$1
    source_root="$FRAMEWORK_ROOT/tests/mrts/infra-overlays/nginx-pr24"
    stage="$target_root/stage"
    require_path "$source_root" "Framework NGINX PR24 overlay" || return 1
    assert_safe_runtime_path "$target_root" "NGINX native target root" || return 77
    safe_remove_runtime_path "$stage" "$target_root" "NGINX native stage" || return 77
    mkdir -p "$stage"
    cp -a "$source_root/." "$stage/"
    mkdir -p "$stage/infra/log" "$stage/infra/run"
    cp "$MRTS_BUILD_ROOT/upstream-config-tests/mrts.load" "$stage/infra/mrts.load"
    sed -i "s#listen 80 default_server;#listen $MRTS_NATIVE_NGINX_PORT default_server;#g" "$stage/infra/sites-available/default"
    sed -i "s#listen \\[::\\]:80 default_server;#listen [::]:$MRTS_NATIVE_NGINX_PORT default_server;#g" "$stage/infra/sites-available/default"
    sed -i "s#http://127.0.0.1:8000/#http://127.0.0.1:$MRTS_NATIVE_BACKEND_PORT/#g" "$stage/infra/sites-available/default"
    if [ -n "${MRTS_NATIVE_NGINX_MODULE_DIR:-}" ]; then
        module_path="$MRTS_NATIVE_NGINX_MODULE_DIR/ngx_http_modsecurity_module.so"
        sed -i "s#^load_module .*ngx_http_modsecurity_module.so;#load_module $module_path;#" "$stage/infra/modules-available/mod-http-modsecurity.conf"
    fi
    if [ -n "${MRTS_NATIVE_NGINX_BIN:-}" ]; then
        sed -i "s#'nginx'#'$(printf '%s' "$MRTS_NATIVE_NGINX_BIN" | sed \"s#'#'\\\\''#g\")'#" "$stage/start.py" "$stage/stop.py"
    fi
    patch_common_ftw_config "$stage/ftw.mrts.config.yaml" "$stage/infra/log/error.log"
    printf '%s\n' "$stage"
}

native_target_deps() {
    target=$1
    common_missing=""
    if ! command_available "$GO_FTW_BIN"; then
        common_missing=$(append_missing_dep "$common_missing" "go-ftw" "GO_FTW_BIN")
    fi
    if ! command_available "$ALBEDO_BIN"; then
        common_missing=$(append_missing_dep "$common_missing" "albedo" "ALBEDO_BIN")
    fi
    case "$target" in
        apache2_ubuntu)
            apachectl_bin="${APACHECTL_BIN:-apachectl}"
            if ! command_available "$apachectl_bin"; then
                common_missing=$(append_missing_dep "$common_missing" "apachectl" "APACHECTL_BIN")
            fi
            ;;
        nginx-pr24)
            nginx_bin="${MRTS_NATIVE_NGINX_BIN:-$(command -v nginx 2>/dev/null || true)}"
            if [ -z "$nginx_bin" ] || ! command_available "$nginx_bin"; then
                common_missing=$(append_missing_dep "$common_missing" "nginx" "MRTS_NATIVE_NGINX_BIN")
            fi
            module_path="${MRTS_NATIVE_NGINX_MODULE_DIR:-/usr/lib/nginx/modules}/ngx_http_modsecurity_module.so"
            if [ ! -f "$module_path" ]; then
                common_missing=$(append_missing_dep "$common_missing" "ngx_http_modsecurity_module.so" "MRTS_NATIVE_NGINX_MODULE_DIR")
            fi
            ;;
    esac
    if [ -n "$common_missing" ]; then
        printf '%s\n' "$common_missing"
        return 1
    fi
    return 0
}

run_native_target() {
    target=$1
    case "$target" in
        apache2_ubuntu|nginx-pr24) ;;
        *) echo "ERROR: unsupported MRTS_NATIVE_TARGETS item: $target" >&2; return 2 ;;
    esac

    target_root="$MRTS_NATIVE_ROOT/$target"
    run_log="$target_root/run.log"
    exit_code_file="$target_root/exit.code"
    job_json="$target_root/job.json"
    summary_path="$job_json"
    safe_remove_runtime_path "$target_root" "$MRTS_NATIVE_ROOT" "native target root" || return 77
    mkdir -p "$target_root"
    : > "$run_log"
    started=$(date +%s)

    echo "mrts-native: target=$target start" >> "$run_log"
    if ! prepare_mrts_outputs >> "$run_log" 2>&1; then
        rc=77
        reason="MRTS generation or mrts.load preparation failed"
        printf '%s\n' "$rc" > "$exit_code_file"
        write_job_json "$job_json" "$target" "BLOCKED" "$reason" "$rc" 0 "$run_log" "$summary_path"
        echo "mrts-native: target=$target BLOCKED: $reason"
        return "$rc"
    fi

    case "$target" in
        apache2_ubuntu)
            if ! stage=$(stage_apache "$target_root" 2>>"$run_log"); then
                rc=77
                reason="Apache native staging failed"
                printf '%s\n' "$rc" > "$exit_code_file"
                write_job_json "$job_json" "$target" "BLOCKED" "$reason" "$rc" 0 "$run_log" "$summary_path"
                echo "mrts-native: target=$target BLOCKED: $reason"
                return "$rc"
            fi
            ;;
        nginx-pr24)
            if ! stage=$(stage_nginx "$target_root" 2>>"$run_log"); then
                rc=77
                reason="NGINX PR24 native staging failed"
                printf '%s\n' "$rc" > "$exit_code_file"
                write_job_json "$job_json" "$target" "BLOCKED" "$reason" "$rc" 0 "$run_log" "$summary_path"
                echo "mrts-native: target=$target BLOCKED: $reason"
                return "$rc"
            fi
            ;;
    esac

    deps=$(native_target_deps "$target" || true)
    if [ -n "$deps" ]; then
        rc=77
        reason="missing native dependencies: $deps"
        ended=$(date +%s)
        printf '%s\n' "$rc" > "$exit_code_file"
        write_job_json "$job_json" "$target" "BLOCKED" "$reason" "$rc" "$((ended - started))" "$run_log" "$summary_path"
        echo "mrts-native: target=$target BLOCKED: $reason"
        return "$rc"
    fi

    backend_pid=""
    cleanup() {
        if [ -n "$backend_pid" ]; then
            kill "$backend_pid" >/dev/null 2>&1 || true
        fi
        "$PYTHON" "$stage/stop.py" >> "$run_log" 2>&1 || true
    }
    trap cleanup EXIT INT TERM

    "$ALBEDO_BIN" -b 127.0.0.1 -p "$MRTS_NATIVE_BACKEND_PORT" >> "$run_log" 2>&1 &
    backend_pid=$!
    "$PYTHON" "$stage/start.py" >> "$run_log" 2>&1
    start_rc=$?
    if [ "$start_rc" -ne 0 ]; then
        cleanup
        trap - EXIT INT TERM
        rc=77
        reason="native infrastructure start failed"
        ended=$(date +%s)
        printf '%s\n' "$rc" > "$exit_code_file"
        write_job_json "$job_json" "$target" "BLOCKED" "$reason" "$rc" "$((ended - started))" "$run_log" "$summary_path"
        echo "mrts-native: target=$target BLOCKED: $reason"
        return "$rc"
    fi

    "$GO_FTW_BIN" run --config "$stage/ftw.mrts.config.yaml" --dir "$MRTS_BUILD_ROOT/upstream-config-tests/ftw" --wait-for-expect-status-code 200 --fail-fast >> "$run_log" 2>&1
    rc=$?
    cleanup
    trap - EXIT INT TERM
    ended=$(date +%s)
    printf '%s\n' "$rc" > "$exit_code_file"
    if [ "$rc" -eq 0 ]; then
        write_job_json "$job_json" "$target" "PASS" "native MRTS run completed" "$rc" "$((ended - started))" "$run_log" "$summary_path"
        echo "mrts-native: target=$target PASS"
    else
        write_job_json "$job_json" "$target" "FAIL" "native MRTS go-ftw run failed" "$rc" "$((ended - started))" "$run_log" "$summary_path"
        echo "mrts-native: target=$target FAIL"
    fi
    return "$rc"
}

MAKE="${MAKE:-make}"
has_fail=0
has_blocked=0
for target in $MRTS_NATIVE_TARGETS; do
    run_native_target "$target"
    rc=$?
    if [ "$rc" -eq 0 ]; then
        :
    elif [ "$rc" -eq 77 ]; then
        has_blocked=1
    else
        has_fail=1
    fi
done

"$PYTHON" "$FRAMEWORK_ROOT/ci/generate-mrts-native-report.py" \
    --connector-root "$CONNECTOR_ROOT" \
    --framework-root "$FRAMEWORK_ROOT" \
    --native-root "$MRTS_NATIVE_ROOT" \
    --output-root "$CONNECTOR_ROOT"
report_rc=$?

echo "mrts-native: report=$CONNECTOR_ROOT/reports/testing/generated/mrts-native-full.generated.md"
if [ "$report_rc" -ne 0 ] || [ "$has_fail" -ne 0 ]; then
    exit 2
fi
if [ "$has_blocked" -ne 0 ]; then
    exit 77
fi
exit 0
