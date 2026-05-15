#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
BUILD_ROOT="${BUILD_ROOT:-/src/ModSecurity-conector-build}"
RESULTS_DIR="${RESULTS_DIR:-$BUILD_ROOT/results}"
NGINX_BUILD_DIR="${NGINX_BUILD_DIR:-$BUILD_ROOT/nginx-build}"
NGINX_PREFIX="${NGINX_PREFIX:-$BUILD_ROOT/nginx-runtime/nginx}"
NGINX_BINARY="${NGINX_BINARY:-$NGINX_PREFIX/sbin/nginx}"
NGINX_MODULE="${NGINX_MODULE:-$NGINX_PREFIX/modules/ngx_http_modsecurity_module.so}"
MODSECURITY_LIB_DIR="${MODSECURITY_LIB_DIR:-$NGINX_BUILD_DIR/output/modsecurity/lib}"
REFRESH="${REFRESH:-0}"
SMOKE_CASES="${SMOKE_CASES:-}"
BUILD_NGINX_FROM_SOURCE="${BUILD_NGINX_FROM_SOURCE:-1}"
NGINX_BUILD_LOG_DIR="${NGINX_BUILD_LOG_DIR:-$BUILD_ROOT/logs/nginx}"
NGINX_RUNTIME_LOG_DIR="${NGINX_RUNTIME_LOG_DIR:-$BUILD_ROOT/logs/nginx-runtime}"

write_connector_result() {
    status=$1
    message=$2
    mkdir -p "$RESULTS_DIR"
    {
        printf '%s nginx-build %s\n' "$(printf '%s' "$status" | tr '[:lower:]' '[:upper:]')" "$message"
    } > "$RESULTS_DIR/nginx-summary.txt"
    printf '{\n  "nginx": {\n    "build": "%s"\n  }\n}\n' "$status" > "$RESULTS_DIR/nginx-summary.json"
    cp "$RESULTS_DIR/nginx-summary.txt" "$RESULTS_DIR/connector-summary.txt"
}

needs_build=0
if [ "$REFRESH" = "1" ]; then
    needs_build=1
elif [ ! -x "$NGINX_BINARY" ] || [ ! -f "$NGINX_MODULE" ]; then
    needs_build=1
elif [ ! -f "$MODSECURITY_LIB_DIR/libmodsecurity.so" ]; then
    needs_build=1
fi

if [ "$needs_build" -eq 1 ]; then
    echo "run_nginx_smoke: preparing NGINX PoC build"
    set +e
    REFRESH="$REFRESH" \
        LOG_DIR="$NGINX_BUILD_LOG_DIR" \
        BUILD_NGINX_FROM_SOURCE="$BUILD_NGINX_FROM_SOURCE" \
        sh "$REPO_ROOT/ci/prepare-nginx-build.sh"
    rc=$?
    set -e
    if [ "$rc" -eq 77 ]; then
        write_connector_result blocked "prepare-nginx-build blocked; see $NGINX_BUILD_LOG_DIR"
        exit 77
    fi
    if [ "$rc" -ne 0 ]; then
        write_connector_result fail "prepare-nginx-build failed; see $NGINX_BUILD_LOG_DIR"
        exit "$rc"
    fi
fi

LOG_DIR="$NGINX_RUNTIME_LOG_DIR" \
    RESULTS_DIR="$RESULTS_DIR" \
    BUILD_ROOT="$BUILD_ROOT" \
    NGINX_BUILD_DIR="$NGINX_BUILD_DIR" \
    NGINX_PREFIX="$NGINX_PREFIX" \
    NGINX_BINARY="$NGINX_BINARY" \
    NGINX_MODULE="$NGINX_MODULE" \
    MODSECURITY_LIB_DIR="$MODSECURITY_LIB_DIR" \
    SMOKE_CASES="$SMOKE_CASES" \
    sh "$REPO_ROOT/connectors/nginx/harness/run_nginx_smoke.sh"
