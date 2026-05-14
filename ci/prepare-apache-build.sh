#!/bin/sh
set -eu

MODSECURITY_V3_SOURCE_DIR="${MODSECURITY_V3_SOURCE_DIR:-/root/conecter/ModSecurity_V3}"
MODSECURITY_APACHE_SOURCE_DIR="${MODSECURITY_APACHE_SOURCE_DIR:-/root/conecter/ModSecurity-apache}"
BUILD_ROOT="${BUILD_ROOT:-/src/ModSecurity-conector-build}"
LOG_DIR="${LOG_DIR:-$BUILD_ROOT/logs/apache}"
REFRESH="${REFRESH:-0}"
APACHE_BUILD_ROOT="${APACHE_BUILD_ROOT:-$BUILD_ROOT/apache-build}"
V3_BUILD_DIR="$APACHE_BUILD_ROOT/ModSecurity_V3"
APACHE_CONNECTOR_BUILD_DIR="$APACHE_BUILD_ROOT/ModSecurity-apache"
OUTPUT_DIR="$APACHE_BUILD_ROOT/output"
MODSECURITY_STAGE="$OUTPUT_DIR/modsecurity"
SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)

default_jobs() {
    if command -v nproc >/dev/null 2>&1; then
        nproc
    else
        getconf _NPROCESSORS_ONLN 2>/dev/null || echo 1
    fi
}

MAKE_JOBS="${MAKE_JOBS:-$(default_jobs)}"
APXS_BIN="${APXS:-}"
APACHE_HTTPD_BIN="${APACHE_HTTPD:-${APACHE:-}}"
STATUS_FILE="$LOG_DIR/status.txt"
COMMANDS_FILE="$LOG_DIR/commands.txt"
SOURCE_INFO_FILE="$LOG_DIR/source-info.txt"
ARTIFACTS_FILE="$LOG_DIR/artifacts.txt"

blocked() {
    echo "apache_poc: blocked $*"
    mkdir -p "$LOG_DIR"
    echo "blocked: $*" >> "$STATUS_FILE"
    exit 77
}

fail() {
    echo "apache_poc: fail $*"
    mkdir -p "$LOG_DIR"
    echo "fail: $*" >> "$STATUS_FILE"
    exit 1
}

canonical_existing() {
    if [ -e "$1" ]; then
        (cd "$1" 2>/dev/null && pwd -P)
    else
        return 1
    fi
}

require_absolute_generated_path() {
    path=$1
    label=$2
    case "$path" in
        /*) ;;
        *) blocked "$label must be an absolute generated path: $path" ;;
    esac
    case "$path" in
        "$REPO_ROOT"|"$REPO_ROOT"/*|/root/conecter/*)
            blocked "$label is inside a read-only or source checkout: $path"
            ;;
    esac
}

safe_remove_dir() {
    target=$1
    real_target=$(canonical_existing "$target")
    case "$real_target" in
        /|/src|/tmp|/var|/home|/root|"$REPO_ROOT"|"$BUILD_ROOT"|/root/conecter/*)
            blocked "unsafe REFRESH target: $real_target"
            ;;
    esac
    rm -rf "$target"
}

find_apxs() {
    if [ -n "$APXS_BIN" ]; then
        printf '%s\n' "$APXS_BIN"
        return 0
    fi
    command -v apxs 2>/dev/null || command -v apxs2 2>/dev/null || true
}

find_apache() {
    if [ -n "$APACHE_HTTPD_BIN" ]; then
        printf '%s\n' "$APACHE_HTTPD_BIN"
        return 0
    fi
    command -v apache2 2>/dev/null || command -v httpd 2>/dev/null || true
}

run_logged() {
    label=$1
    cwd=$2
    shift 2
    log_file="$LOG_DIR/$label.log"
    {
        echo "[$label]"
        echo "cwd=$cwd"
        echo "command=$*"
        echo
    } >> "$COMMANDS_FILE"
    echo "apache_poc: running $label"
    if (cd "$cwd" && "$@") >"$log_file" 2>&1; then
        echo "pass: $label log=$log_file" >> "$STATUS_FILE"
        return 0
    fi
    rc=$?
    echo "blocked: $label rc=$rc log=$log_file" >> "$STATUS_FILE"
    echo "apache_poc: blocked command failed: $*"
    echo "apache_poc: see log: $log_file"
    exit 77
}

write_git_info() {
    label=$1
    path=$2
    {
        echo "[$label]"
        echo "path=$path"
        if git -C "$path" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
            echo "branch=$(git -C "$path" rev-parse --abbrev-ref HEAD)"
            echo "commit=$(git -C "$path" rev-parse HEAD)"
            echo "describe=$(git -C "$path" describe --tags --always --dirty 2>/dev/null || true)"
        else
            echo "git=not-a-git-checkout"
        fi
        echo
    } >> "$SOURCE_INFO_FILE"
}

stage_modsecurity() {
    header_dir="$V3_BUILD_DIR/headers"
    lib_dir="$V3_BUILD_DIR/src/.libs"
    lib_log="$LOG_DIR/stage-modsecurity-library.log"
    if [ ! -f "$header_dir/modsecurity/modsecurity.h" ]; then
        blocked "missing built v3 header: $header_dir/modsecurity/modsecurity.h"
    fi
    if [ ! -f "$lib_dir/libmodsecurity.so" ]; then
        blocked "missing built v3 library: $lib_dir/libmodsecurity.so"
    fi

    mkdir -p "$MODSECURITY_STAGE/include" "$MODSECURITY_STAGE/lib"
    run_logged stage-modsecurity-headers "$V3_BUILD_DIR" cp -a "$header_dir/." "$MODSECURITY_STAGE/include/"
    {
        echo "[stage-modsecurity-library]"
        echo "cwd=$V3_BUILD_DIR"
        echo "command=cp -a $lib_dir/libmodsecurity.so* $MODSECURITY_STAGE/lib/"
        echo
    } >> "$COMMANDS_FILE"
    if cp -a "$lib_dir"/libmodsecurity.so* "$MODSECURITY_STAGE/lib/" >"$lib_log" 2>&1; then
        echo "pass: stage-modsecurity-library log=$lib_log" >> "$STATUS_FILE"
    else
        echo "blocked: stage-modsecurity-library log=$lib_log" >> "$STATUS_FILE"
        echo "apache_poc: blocked unable to stage libmodsecurity; see $lib_log"
        exit 77
    fi
    {
        echo "modsecurity_stage=$MODSECURITY_STAGE"
        echo "modsecurity_header=$MODSECURITY_STAGE/include/modsecurity/modsecurity.h"
        echo "modsecurity_library=$MODSECURITY_STAGE/lib/libmodsecurity.so"
    } >> "$ARTIFACTS_FILE"
}

echo "apache_poc: MODSECURITY_V3_SOURCE_DIR=$MODSECURITY_V3_SOURCE_DIR"
echo "apache_poc: MODSECURITY_APACHE_SOURCE_DIR=$MODSECURITY_APACHE_SOURCE_DIR"
echo "apache_poc: BUILD_ROOT=$BUILD_ROOT"
echo "apache_poc: APACHE_BUILD_ROOT=$APACHE_BUILD_ROOT"
echo "apache_poc: LOG_DIR=$LOG_DIR"

require_absolute_generated_path "$BUILD_ROOT" "BUILD_ROOT"
require_absolute_generated_path "$APACHE_BUILD_ROOT" "APACHE_BUILD_ROOT"
require_absolute_generated_path "$LOG_DIR" "LOG_DIR"
require_absolute_generated_path "$OUTPUT_DIR" "OUTPUT_DIR"

[ -d "$MODSECURITY_V3_SOURCE_DIR" ] || blocked "missing MODSECURITY_V3_SOURCE_DIR: $MODSECURITY_V3_SOURCE_DIR"
[ -d "$MODSECURITY_APACHE_SOURCE_DIR" ] || blocked "missing MODSECURITY_APACHE_SOURCE_DIR: $MODSECURITY_APACHE_SOURCE_DIR"

if [ -e "$APACHE_BUILD_ROOT" ]; then
    if [ "$REFRESH" != "1" ]; then
        blocked "build directory exists: $APACHE_BUILD_ROOT; set REFRESH=1 to replace it"
    fi
    safe_remove_dir "$APACHE_BUILD_ROOT"
fi

mkdir -p "$APACHE_BUILD_ROOT" "$LOG_DIR" "$OUTPUT_DIR"
: > "$STATUS_FILE"
: > "$COMMANDS_FILE"
: > "$SOURCE_INFO_FILE"
: > "$ARTIFACTS_FILE"

write_git_info "modsecurity-v3-source" "$MODSECURITY_V3_SOURCE_DIR"
write_git_info "modsecurity-apache-source" "$MODSECURITY_APACHE_SOURCE_DIR"

run_logged copy-modsecurity-v3 "$APACHE_BUILD_ROOT" cp -a "$MODSECURITY_V3_SOURCE_DIR" "$V3_BUILD_DIR"
run_logged copy-modsecurity-apache "$APACHE_BUILD_ROOT" cp -a "$MODSECURITY_APACHE_SOURCE_DIR" "$APACHE_CONNECTOR_BUILD_DIR"
write_git_info "modsecurity-v3-build-copy" "$V3_BUILD_DIR"
write_git_info "modsecurity-apache-build-copy" "$APACHE_CONNECTOR_BUILD_DIR"

APXS_BIN=$(find_apxs)
APACHE_HTTPD_BIN=$(find_apache)
if [ -z "$APXS_BIN" ]; then
    blocked "missing APXS; set APXS=/path/to/apxs or install apache development tools"
fi
if [ ! -x "$APXS_BIN" ]; then
    blocked "APXS is not executable: $APXS_BIN"
fi
if [ -z "$APACHE_HTTPD_BIN" ]; then
    blocked "missing Apache httpd executable; set APACHE_HTTPD=/path/to/apache2-or-httpd"
fi
if [ ! -x "$APACHE_HTTPD_BIN" ]; then
    blocked "Apache executable is not executable: $APACHE_HTTPD_BIN"
fi

{
    echo "[apache-tools]"
    echo "APXS=$APXS_BIN"
    "$APXS_BIN" -q CC 2>/dev/null || true
    "$APXS_BIN" -q LIBEXECDIR 2>/dev/null || true
    echo "APACHE_HTTPD=$APACHE_HTTPD_BIN"
    "$APACHE_HTTPD_BIN" -v 2>/dev/null || true
    echo
} >> "$SOURCE_INFO_FILE"

run_logged v3-git-submodule-update "$V3_BUILD_DIR" git submodule update --init --recursive
run_logged v3-build-sh "$V3_BUILD_DIR" ./build.sh
run_logged v3-configure "$V3_BUILD_DIR" ./configure
run_logged v3-make "$V3_BUILD_DIR" make "-j$MAKE_JOBS"
stage_modsecurity

run_logged apache-autogen "$APACHE_CONNECTOR_BUILD_DIR" ./autogen.sh
run_logged apache-configure "$APACHE_CONNECTOR_BUILD_DIR" ./configure "--with-libmodsecurity=$MODSECURITY_STAGE" "--with-apxs=$APXS_BIN" "--with-apache=$APACHE_HTTPD_BIN"
run_logged apache-make "$APACHE_CONNECTOR_BUILD_DIR" make

module_candidate="$APACHE_CONNECTOR_BUILD_DIR/src/.libs/mod_security3.so"
if [ ! -f "$module_candidate" ]; then
    fail "Apache connector build completed without expected module: $module_candidate"
fi

mkdir -p "$OUTPUT_DIR/apache"
cp -a "$module_candidate" "$OUTPUT_DIR/apache/mod_security3.so"
{
    echo "apache_module=$OUTPUT_DIR/apache/mod_security3.so"
    echo "apache_module_build_copy=$module_candidate"
} >> "$ARTIFACTS_FILE"

echo "pass: apache connector module built" >> "$STATUS_FILE"
echo "apache_poc: pass module=$OUTPUT_DIR/apache/mod_security3.so"
