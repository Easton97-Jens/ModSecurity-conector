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

join_library_path() {
    result=""
    for path in "$@"; do
        [ -n "$path" ] || continue
        if [ -n "$result" ]; then
            result="$result:$path"
        else
            result="$path"
        fi
    done
    printf '%s\n' "$result"
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

replace_loadmodule_paths() {
    load_file=$1
    modules_dir=$2
    apache_module=$3
    "$PYTHON" - "$load_file" "$modules_dir" "$apache_module" <<'PY'
import re
import sys
from pathlib import Path

path = Path(sys.argv[1])
modules_dir = sys.argv[2]
apache_module = sys.argv[3]
text = path.read_text(encoding="utf-8")
text = re.sub(r"/usr/lib/apache2/modules/(mod_[^\s\"']+\.so)", modules_dir + r"/\1", text)
if path.name == "security2.load" and apache_module:
    text = re.sub(
        r"LoadModule\s+security2_module\s+\S+",
        "LoadModule security3_module " + apache_module,
        text,
    )
path.write_text(text, encoding="utf-8")
PY
}

replace_file_text() {
    file_path=$1
    old_text=$2
    new_text=$3
    "$PYTHON" - "$file_path" "$old_text" "$new_text" <<'PY'
import sys
from pathlib import Path

path = Path(sys.argv[1])
old = sys.argv[2]
new = sys.argv[3]
text = path.read_text(encoding="utf-8")
path.write_text(text.replace(old, new), encoding="utf-8")
PY
}

write_apache_modsecurity_conf() {
    conf_file=$1
    modsecurity_conf=$2
    mrts_load=$3
    phase4_log=$4
    cat > "$conf_file" <<EOF
<IfModule security3_module>
    modsecurity on
    modsecurity_rules_file $modsecurity_conf
    modsecurity_rules_file $mrts_load
    modsecurity_phase4_mode safe
    modsecurity_phase4_log $phase4_log
    modsecurity_phase4_body_limit 1048576
</IfModule>
EOF
}

patch_modsecurity_v3_rules_config() {
    rules_conf=$1
    "$PYTHON" - "$rules_conf" <<'PY'
import sys
from pathlib import Path

path = Path(sys.argv[1])
lines = []
for line in path.read_text(encoding="utf-8").splitlines():
    if line.lstrip().startswith("SecRequestBodyInMemoryLimit "):
        lines.append("# disabled in local native staging: unsupported by libmodsecurity v3")
    else:
        lines.append(line)
path.write_text("\n".join(lines) + "\n", encoding="utf-8")
PY
}

write_native_apache_load_if_present() {
    modules_dir=$1
    load_dir=$2
    module_name=$3
    module_file=$4
    if [ -f "$modules_dir/$module_file" ]; then
        printf 'LoadModule %s_module %s/%s\n' "$module_name" "$modules_dir" "$module_file" > "$load_dir/native-$module_name.load"
    fi
}

disable_nginx_system_module_file() {
    module_file=$1
    "$PYTHON" - "$module_file" <<'PY'
import sys
from pathlib import Path

path = Path(sys.argv[1])
lines = []
for line in path.read_text(encoding="utf-8").splitlines():
    stripped = line.lstrip()
    if stripped.startswith("load_module ") or "load_module /usr/lib/nginx/" in stripped:
        lines.append("# disabled in local native staging")
    else:
        lines.append(line)
path.write_text("\n".join(lines) + "\n", encoding="utf-8")
PY
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

patch_ftw_dest_ports() {
    ftw_dir=$1
    port=$2
    "$PYTHON" - "$ftw_dir" "$port" <<'PY'
import sys
from pathlib import Path

import yaml

root = Path(sys.argv[1])
port = int(sys.argv[2])

def patch(value):
    if isinstance(value, dict):
        for key, item in list(value.items()):
            if key == "port" and item == 80:
                value[key] = port
            else:
                patch(item)
    elif isinstance(value, list):
        for item in value:
            patch(item)

for path in sorted(root.rglob("*.yaml")):
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    patch(data)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
PY
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
    mkdir -p "$stage/infra/log" "$stage/infra/run" "$stage/infra/htdocs" "$stage/infra/run/modsecurity-data"
    : > "$stage/infra/htdocs/index.html"
    cp "$MRTS_BUILD_ROOT/upstream-config-tests/mrts.load" "$stage/infra/mrts.load"
    patch_modsecurity_v3_rules_config "$stage/infra/modsecurity/modsecurity.conf"
    sed -i "s#^Listen 80#Listen $MRTS_NATIVE_APACHE_PORT#" "$stage/infra/ports.conf"
    sed -i "s#<VirtualHost \\*:80>#<VirtualHost *:$MRTS_NATIVE_APACHE_PORT>#" "$stage/infra/sites-available/000-default.conf"
    sed -i "s#http://127.0.0.1:8000/#http://127.0.0.1:$MRTS_NATIVE_BACKEND_PORT/#g" "$stage/infra/sites-available/000-default.conf"
    replace_file_text "$stage/infra/sites-available/000-default.conf" "DocumentRoot /var/www/html" "DocumentRoot $stage/infra/htdocs"
    cat >> "$stage/infra/sites-available/000-default.conf" <<EOF

<Directory "$stage/infra/htdocs">
    Require all granted
</Directory>
EOF
    write_apache_modsecurity_conf \
        "$stage/infra/mods-available/security2.conf" \
        "$stage/infra/modsecurity/modsecurity.conf" \
        "$stage/infra/mrts.load" \
        "$stage/infra/log/modsecurity-phase4.jsonl"
    write_apache_modsecurity_conf \
        "$stage/infra/mods-enabled/security2.conf" \
        "$stage/infra/modsecurity/modsecurity.conf" \
        "$stage/infra/mrts.load" \
        "$stage/infra/log/modsecurity-phase4.jsonl"
    if [ -n "${HTTPD_PREFIX:-}" ]; then
        mime_types="$HTTPD_PREFIX/conf/mime.types"
        if [ ! -f "$mime_types" ]; then
            mime_types="$stage/infra/mime.types"
            : > "$mime_types"
        fi
        replace_file_text "$stage/infra/mods-enabled/mime.conf" "TypesConfig /etc/mime.types" "TypesConfig $mime_types"
        replace_file_text "$stage/infra/mods-available/mime.conf" "TypesConfig /etc/mime.types" "TypesConfig $mime_types"
    fi
    if [ -n "${HTTPD_PREFIX:-}" ] && [ -d "$HTTPD_PREFIX/modules" ]; then
        for load_file in "$stage/infra/mods-enabled/"*.load "$stage/infra/mods-available/"*.load; do
            [ -f "$load_file" ] || continue
            replace_loadmodule_paths "$load_file" "$HTTPD_PREFIX/modules" "${APACHE_MRTS_MODULE:-${APACHE_MODULE:-}}"
        done
        write_native_apache_load_if_present "$HTTPD_PREFIX/modules" "$stage/infra/mods-enabled" log_config mod_log_config.so
        write_native_apache_load_if_present "$HTTPD_PREFIX/modules" "$stage/infra/mods-enabled" logio mod_logio.so
        write_native_apache_load_if_present "$HTTPD_PREFIX/modules" "$stage/infra/mods-enabled" unixd mod_unixd.so
    fi
    if [ -n "${APACHECTL_BIN:-}" ]; then
        replace_file_text "$stage/start.py" "'apachectl'" "'$APACHECTL_BIN'"
        replace_file_text "$stage/stop.py" "'apachectl'" "'$APACHECTL_BIN'"
    fi
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
    mkdir -p "$stage/infra/log" "$stage/infra/run" "$stage/infra/html"
    : > "$stage/infra/html/index.html"
    cp "$MRTS_BUILD_ROOT/upstream-config-tests/mrts.load" "$stage/infra/mrts.load"
    rm -f "$stage/infra/modules-enabled/"*
    ln -s ../modules-available/mod-http-modsecurity.conf "$stage/infra/modules-enabled/mod-http-modsecurity.conf"
    for module_file in "$stage/infra/modules-available/"*.conf; do
        [ -f "$module_file" ] || continue
        case "$(basename "$module_file")" in
            mod-http-modsecurity.conf) ;;
            *) disable_nginx_system_module_file "$module_file" ;;
        esac
    done
    sed -i "s#listen 80 default_server;#listen $MRTS_NATIVE_NGINX_PORT default_server;#g" "$stage/infra/sites-available/default"
    sed -i "s#listen \\[::\\]:80 default_server;#listen [::]:$MRTS_NATIVE_NGINX_PORT default_server;#g" "$stage/infra/sites-available/default"
    sed -i "s#http://127.0.0.1:8000/#http://127.0.0.1:$MRTS_NATIVE_BACKEND_PORT/#g" "$stage/infra/sites-available/default"
    replace_file_text "$stage/infra/sites-available/default" "root /var/www/html;" "root $stage/infra/html;"
    sed -i "/more_set_headers/d" "$stage/infra/sites-available/default"
    sed -i "/ssl_protocols/d;/ssl_prefer_server_ciphers/d" "$stage/infra/nginx.conf"
    if [ -n "${MRTS_NATIVE_NGINX_MODULE_DIR:-}" ]; then
        module_path="$MRTS_NATIVE_NGINX_MODULE_DIR/ngx_http_modsecurity_module.so"
        sed -i "s#^load_module .*ngx_http_modsecurity_module.so;#load_module $module_path;#" "$stage/infra/modules-available/mod-http-modsecurity.conf"
    fi
    if [ -n "${MRTS_NATIVE_NGINX_BIN:-}" ]; then
        replace_file_text "$stage/start.py" "'nginx'" "'$MRTS_NATIVE_NGINX_BIN'"
        replace_file_text "$stage/stop.py" "'nginx'" "'$MRTS_NATIVE_NGINX_BIN'"
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
            apachectl_bin="${APACHECTL_BIN:-}"
            if ! command_available "$apachectl_bin"; then
                common_missing=$(append_missing_dep "$common_missing" "apachectl" "APACHECTL_BIN")
            fi
            apache_module="${APACHE_MRTS_MODULE:-${APACHE_MODULE:-}}"
            if [ -z "$apache_module" ] || [ ! -f "$apache_module" ]; then
                common_missing=$(append_missing_dep "$common_missing" "mod_security3.so" "APACHE_MRTS_MODULE")
            fi
            apache_lib_dir="${APACHE_MRTS_MODSECURITY_LIB_DIR:-}"
            if [ -z "$apache_lib_dir" ] || [ ! -f "$apache_lib_dir/libmodsecurity.so" ]; then
                common_missing=$(append_missing_dep "$common_missing" "libmodsecurity.so" "APACHE_MRTS_MODSECURITY_LIB_DIR")
            fi
            ;;
        nginx-pr24)
            nginx_bin="${MRTS_NATIVE_NGINX_BIN:-}"
            if [ -z "$nginx_bin" ] || ! command_available "$nginx_bin"; then
                common_missing=$(append_missing_dep "$common_missing" "nginx" "MRTS_NATIVE_NGINX_BIN")
            fi
            module_path="${MRTS_NATIVE_NGINX_MODULE_DIR:-}/ngx_http_modsecurity_module.so"
            if [ ! -f "$module_path" ]; then
                common_missing=$(append_missing_dep "$common_missing" "ngx_http_modsecurity_module.so" "MRTS_NATIVE_NGINX_MODULE_DIR")
            fi
            nginx_lib_dir="${MRTS_NATIVE_NGINX_MODSECURITY_LIB_DIR:-}"
            if [ -n "$nginx_lib_dir" ] && [ ! -f "$nginx_lib_dir/libmodsecurity.so" ]; then
                common_missing=$(append_missing_dep "$common_missing" "libmodsecurity.so" "MRTS_NATIVE_NGINX_MODSECURITY_LIB_DIR")
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
            patch_ftw_dest_ports "$MRTS_BUILD_ROOT/upstream-config-tests/ftw" "$MRTS_NATIVE_APACHE_PORT" >> "$run_log" 2>&1 || {
                rc=77
                reason="Apache native FTW port patch failed"
                printf '%s\n' "$rc" > "$exit_code_file"
                write_job_json "$job_json" "$target" "BLOCKED" "$reason" "$rc" 0 "$run_log" "$summary_path"
                echo "mrts-native: target=$target BLOCKED: $reason"
                return "$rc"
            }
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
            patch_ftw_dest_ports "$MRTS_BUILD_ROOT/upstream-config-tests/ftw" "$MRTS_NATIVE_NGINX_PORT" >> "$run_log" 2>&1 || {
                rc=77
                reason="NGINX native FTW port patch failed"
                printf '%s\n' "$rc" > "$exit_code_file"
                write_job_json "$job_json" "$target" "BLOCKED" "$reason" "$rc" 0 "$run_log" "$summary_path"
                echo "mrts-native: target=$target BLOCKED: $reason"
                return "$rc"
            }
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

    case "$target" in
        apache2_ubuntu)
            apache_ld_path=$(join_library_path "${APACHE_MRTS_MODSECURITY_LIB_DIR:-}" "${HTTPD_PREFIX:+$HTTPD_PREFIX/lib}" "${EXPAT_PREFIX:+$EXPAT_PREFIX/lib}")
            if [ -n "$apache_ld_path" ]; then
                LD_LIBRARY_PATH="$apache_ld_path${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
                export LD_LIBRARY_PATH
            fi
            ;;
        nginx-pr24)
            nginx_ld_path=$(join_library_path "${MRTS_NATIVE_NGINX_MODSECURITY_LIB_DIR:-}" "${NGINX_PREFIX:+$NGINX_PREFIX/lib}")
            if [ -n "$nginx_ld_path" ]; then
                LD_LIBRARY_PATH="$nginx_ld_path${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
                export LD_LIBRARY_PATH
            fi
            ;;
    esac

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

if [ -f "$CONNECTOR_ROOT/ci/update-runtime-reports.py" ]; then
    "$PYTHON" "$CONNECTOR_ROOT/ci/update-runtime-reports.py" --connector-root "$CONNECTOR_ROOT" || report_rc=$?
fi

echo "mrts-native: report=$CONNECTOR_ROOT/reports/testing/generated/mrts-native-full.generated.md"
echo "mrts-native: report=$CONNECTOR_ROOT/reports/testing/generated/mrts-native-apache.generated.md"
echo "mrts-native: report=$CONNECTOR_ROOT/reports/testing/generated/mrts-native-nginx.generated.md"
echo "mrts-native: report=$CONNECTOR_ROOT/reports/testing/generated/mrts-native-summary.generated.md"
if [ "$report_rc" -ne 0 ] || [ "$has_fail" -ne 0 ]; then
    exit 2
fi
if [ "$has_blocked" -ne 0 ]; then
    exit 77
fi
exit 0
