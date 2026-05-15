#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
BUILD_ROOT="${BUILD_ROOT:-/src/ModSecurity-conector-build}"
RESULTS_DIR="${RESULTS_DIR:-$BUILD_ROOT/results}"
APACHE_BUILD_ROOT="${APACHE_BUILD_ROOT:-$BUILD_ROOT/apache-build}"
HTTPD_PREFIX="${HTTPD_PREFIX:-$BUILD_ROOT/apache-runtime/httpd}"
APACHE_MODULE="${APACHE_MODULE:-$APACHE_BUILD_ROOT/output/apache/mod_security3.so}"
MODSECURITY_LIB_DIR="${MODSECURITY_LIB_DIR:-$APACHE_BUILD_ROOT/output/modsecurity/lib}"
REFRESH="${REFRESH:-0}"
SMOKE_CASES="${SMOKE_CASES:-}"
BUILD_HTTPD_FROM_SOURCE="${BUILD_HTTPD_FROM_SOURCE:-1}"
BUILD_PCRE2_FROM_SOURCE="${BUILD_PCRE2_FROM_SOURCE:-1}"
APACHE_BUILD_LOG_DIR="${APACHE_BUILD_LOG_DIR:-$BUILD_ROOT/logs/apache}"
APACHE_RUNTIME_LOG_DIR="${APACHE_RUNTIME_LOG_DIR:-$BUILD_ROOT/logs/apache-runtime}"

write_connector_result() {
    status=$1
    message=$2
    mkdir -p "$RESULTS_DIR"
    {
        printf '%s apache-build %s\n' "$(printf '%s' "$status" | tr '[:lower:]' '[:upper:]')" "$message"
    } > "$RESULTS_DIR/apache-summary.txt"
    printf '{\n  "apache": {\n    "build": "%s"\n  }\n}\n' "$status" > "$RESULTS_DIR/apache-summary.json"
    cp "$RESULTS_DIR/apache-summary.txt" "$RESULTS_DIR/connector-summary.txt"
}

needs_build=0
if [ "$REFRESH" = "1" ]; then
    needs_build=1
elif [ ! -x "$HTTPD_PREFIX/bin/httpd" ] || [ ! -x "$HTTPD_PREFIX/bin/apxs" ]; then
    needs_build=1
elif [ ! -f "$APACHE_MODULE" ] || [ ! -f "$MODSECURITY_LIB_DIR/libmodsecurity.so" ]; then
    needs_build=1
fi

if [ "$needs_build" -eq 1 ]; then
    echo "run_apache_smoke: preparing Apache PoC build"
    set +e
    REFRESH="$REFRESH" \
        LOG_DIR="$APACHE_BUILD_LOG_DIR" \
        BUILD_HTTPD_FROM_SOURCE="$BUILD_HTTPD_FROM_SOURCE" \
        BUILD_PCRE2_FROM_SOURCE="$BUILD_PCRE2_FROM_SOURCE" \
        sh "$REPO_ROOT/ci/prepare-apache-build.sh"
    rc=$?
    set -e
    if [ "$rc" -eq 77 ]; then
        write_connector_result blocked "prepare-apache-build blocked; see $APACHE_BUILD_LOG_DIR"
        exit 77
    fi
    if [ "$rc" -ne 0 ]; then
        write_connector_result fail "prepare-apache-build failed; see $APACHE_BUILD_LOG_DIR"
        exit "$rc"
    fi
fi

LOG_DIR="$APACHE_RUNTIME_LOG_DIR" \
    RESULTS_DIR="$RESULTS_DIR" \
    BUILD_ROOT="$BUILD_ROOT" \
    APACHE_BUILD_ROOT="$APACHE_BUILD_ROOT" \
    HTTPD_PREFIX="$HTTPD_PREFIX" \
    APACHE_MODULE="$APACHE_MODULE" \
    MODSECURITY_LIB_DIR="$MODSECURITY_LIB_DIR" \
    SMOKE_CASES="$SMOKE_CASES" \
    sh "$REPO_ROOT/connectors/apache/harness/run_apache_smoke.sh"
