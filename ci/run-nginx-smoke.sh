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
DEFAULT_NGINX_SOURCE_DIR="$REPO_ROOT/connectors/nginx"
MODSECURITY_NGINX_SOURCE_DIR="${MODSECURITY_NGINX_SOURCE_DIR:-$DEFAULT_NGINX_SOURCE_DIR}"
NGINX_ORIGIN_SOURCE="${NGINX_ORIGIN_SOURCE:-}"
NGINX_ORIGIN_SOURCE_REPO="${NGINX_ORIGIN_SOURCE_REPO:-}"
NGINX_ORIGIN_SOURCE_URL="${NGINX_ORIGIN_SOURCE_URL:-}"
NGINX_ORIGIN_SOURCE_COMMIT="${NGINX_ORIGIN_SOURCE_COMMIT:-}"
NGINX_ORIGIN_SOURCE_VERSION="${NGINX_ORIGIN_SOURCE_VERSION:-}"
NGINX_ORIGIN_LICENSE="${NGINX_ORIGIN_LICENSE:-}"
NGINX_ORIGIN_IMPORTED_PATH="${NGINX_ORIGIN_IMPORTED_PATH:-}"
REFRESH="${REFRESH:-0}"
SMOKE_CASES="${SMOKE_CASES:-}"
CASE_SCOPE="${CASE_SCOPE:-all}"
BUILD_NGINX_FROM_SOURCE="${BUILD_NGINX_FROM_SOURCE:-1}"
NGINX_BUILD_LOG_DIR="${NGINX_BUILD_LOG_DIR:-$BUILD_ROOT/logs/nginx}"
NGINX_RUNTIME_LOG_DIR="${NGINX_RUNTIME_LOG_DIR:-$BUILD_ROOT/logs/nginx-runtime}"
PYTHON_BIN="${PYTHON:-python3}"
DEFAULT_MODSECURITY_V3_SOURCE_DIR="/root/conecter/ModSecurity_V3"
MODSECURITY_V3_SOURCE_DIR="${MODSECURITY_V3_SOURCE_DIR:-}"

git_value() {
    git_dir=$1
    shift
    if git -C "$git_dir" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        git -C "$git_dir" "$@" 2>/dev/null || true
    fi
}

load_nginx_adapter_metadata() {
    eval "$("$PYTHON_BIN" "$REPO_ROOT/ci/adapter_metadata.py" shell nginx --prefix NGINX_ADAPTER)"
}

configure_nginx_origin() {
    load_nginx_adapter_metadata
    if [ "$MODSECURITY_NGINX_SOURCE_DIR" = "$DEFAULT_NGINX_SOURCE_DIR" ]; then
        NGINX_ORIGIN_SOURCE="${NGINX_ORIGIN_SOURCE:-$NGINX_ADAPTER_SOURCE}"
        NGINX_ORIGIN_SOURCE_REPO="${NGINX_ORIGIN_SOURCE_REPO:-$NGINX_ADAPTER_SOURCE_REPO}"
        NGINX_ORIGIN_SOURCE_URL="${NGINX_ORIGIN_SOURCE_URL:-$NGINX_ADAPTER_SOURCE_URL}"
        NGINX_ORIGIN_SOURCE_COMMIT="${NGINX_ORIGIN_SOURCE_COMMIT:-$NGINX_ADAPTER_SOURCE_COMMIT}"
        NGINX_ORIGIN_SOURCE_VERSION="${NGINX_ORIGIN_SOURCE_VERSION:-$NGINX_ADAPTER_SOURCE_VERSION}"
        NGINX_ORIGIN_LICENSE="${NGINX_ORIGIN_LICENSE:-$NGINX_ADAPTER_LICENSE}"
        NGINX_ORIGIN_IMPORTED_PATH="${NGINX_ORIGIN_IMPORTED_PATH:-$NGINX_ADAPTER_IMPORTED_PATH}"
        return
    fi
    NGINX_ORIGIN_SOURCE="${NGINX_ORIGIN_SOURCE:-external}"
    NGINX_ORIGIN_SOURCE_REPO="${NGINX_ORIGIN_SOURCE_REPO:-$NGINX_ADAPTER_SOURCE_REPO}"
    NGINX_ORIGIN_SOURCE_URL="${NGINX_ORIGIN_SOURCE_URL:-$NGINX_ADAPTER_SOURCE_URL}"
    NGINX_ORIGIN_SOURCE_COMMIT="${NGINX_ORIGIN_SOURCE_COMMIT:-$(git_value "$MODSECURITY_NGINX_SOURCE_DIR" rev-parse HEAD)}"
    NGINX_ORIGIN_SOURCE_VERSION="${NGINX_ORIGIN_SOURCE_VERSION:-$(git_value "$MODSECURITY_NGINX_SOURCE_DIR" describe --tags --always --dirty)}"
    NGINX_ORIGIN_LICENSE="${NGINX_ORIGIN_LICENSE:-$NGINX_ADAPTER_LICENSE}"
    NGINX_ORIGIN_IMPORTED_PATH="${NGINX_ORIGIN_IMPORTED_PATH:-$MODSECURITY_NGINX_SOURCE_DIR}"
}

write_connector_result() {
    status=$1
    message=$2
    mkdir -p "$RESULTS_DIR"
    "$PYTHON_BIN" "$REPO_ROOT/tests/runners/case_cli.py" summarize-empty \
        --connector nginx \
        --status "$status" \
        --message "$message" \
        --summary-json "$RESULTS_DIR/nginx-summary.json" \
        --summary-text "$RESULTS_DIR/nginx-summary.txt" \
        --connector-path real-world \
        --validation-mode real-world-connector-path \
        --server nginx \
        --server-binary "$NGINX_BINARY" \
        --module "$NGINX_MODULE" \
        --libmodsecurity "$MODSECURITY_LIB_DIR/libmodsecurity.so" \
        --origin-source "$NGINX_ORIGIN_SOURCE" \
        --origin-source-repo "$NGINX_ORIGIN_SOURCE_REPO" \
        --origin-source-url "$NGINX_ORIGIN_SOURCE_URL" \
        --origin-source-commit "$NGINX_ORIGIN_SOURCE_COMMIT" \
        --origin-source-version "$NGINX_ORIGIN_SOURCE_VERSION" \
        --origin-license "$NGINX_ORIGIN_LICENSE" \
        --origin-imported-path "$NGINX_ORIGIN_IMPORTED_PATH"
    cp "$RESULTS_DIR/nginx-summary.txt" "$RESULTS_DIR/connector-summary.txt"
}

configure_nginx_origin

print_blocked_prereq() {
    missing_path=$1
    env_name=$2
    default_path=$3
    echo "blocked: missing runtime prerequisite for ${env_name}: ${missing_path}"
    echo "blocked: set ${env_name} to a valid ModSecurity v3 source tree (current default: ${default_path})"
    echo "blocked: smoke result is BLOCKED, not FAIL"
}

resolve_modsecurity_v3_source_dir() {
    if [ -n "$MODSECURITY_V3_SOURCE_DIR" ] && [ -d "$MODSECURITY_V3_SOURCE_DIR" ]; then
        return
    fi
    if detected=$(sh "$REPO_ROOT/ci/find-modsecurity-v3.sh"); then
        MODSECURITY_V3_SOURCE_DIR="$detected"
        echo "info: auto-detected MODSECURITY_V3_SOURCE_DIR=$MODSECURITY_V3_SOURCE_DIR"
        return
    fi
}

preflight_runtime_prereqs() {
    resolve_modsecurity_v3_source_dir
    if [ ! -d "$MODSECURITY_V3_SOURCE_DIR" ]; then
        print_blocked_prereq "${MODSECURITY_V3_SOURCE_DIR:-<unset>}" MODSECURITY_V3_SOURCE_DIR "$DEFAULT_MODSECURITY_V3_SOURCE_DIR"
        write_connector_result blocked "missing MODSECURITY_V3_SOURCE_DIR: $MODSECURITY_V3_SOURCE_DIR (set env var and retry)"
        exit 77
    fi
}

preflight_runtime_prereqs

nginx_adapter_build_current() {
    manifest="$NGINX_BUILD_DIR/connector-src/materialized-source.json"
    [ -f "$manifest" ] || return 1
    "$PYTHON_BIN" - "$manifest" <<'PY'
import json
import sys

required_adapter_owned = {
    "config",
    "src/ddebug.h",
    "src/ngx_http_modsecurity_access.c",
    "src/ngx_http_modsecurity_body_filter.c",
    "src/ngx_http_modsecurity_common.h",
    "src/ngx_http_modsecurity_header_filter.c",
    "src/ngx_http_modsecurity_log.c",
    "src/ngx_http_modsecurity_module.c",
}
removed_from_build_source = {
    "SOURCE_MAP.json",
    "metadata.c",
    "metadata.h",
    "README.md",
    "src/config",
    "src/SOURCE_MAP.json",
    "src/metadata.c",
    "src/metadata.h",
    "src/README.md",
}

with open(sys.argv[1], "r", encoding="utf-8") as handle:
    manifest = json.load(handle)

entries = manifest.get("entries")
if not isinstance(entries, list):
    raise SystemExit(1)

sources_by_path = {
    entry.get("path"): entry.get("source")
    for entry in entries
    if isinstance(entry, dict)
}
if any(source == "upstream-derived" for source in sources_by_path.values()):
    raise SystemExit(1)
if any(path in sources_by_path for path in removed_from_build_source):
    raise SystemExit(1)
for path in required_adapter_owned:
    if sources_by_path.get(path) != "adapter-owned":
        raise SystemExit(1)
PY
}

needs_build=0
prepare_refresh="$REFRESH"
if [ "$REFRESH" = "1" ]; then
    needs_build=1
elif [ ! -x "$NGINX_BINARY" ] || [ ! -f "$NGINX_MODULE" ]; then
    needs_build=1
elif [ ! -f "$MODSECURITY_LIB_DIR/libmodsecurity.so" ]; then
    needs_build=1
elif [ "$MODSECURITY_NGINX_SOURCE_DIR" = "$DEFAULT_NGINX_SOURCE_DIR" ] && ! nginx_adapter_build_current; then
    echo "run_nginx_smoke: existing NGINX build predates adapter-owned materialized source; refreshing build artifacts"
    needs_build=1
    prepare_refresh=1
fi

if [ "$needs_build" -eq 1 ]; then
    echo "run_nginx_smoke: preparing NGINX PoC build"
    set +e
    REFRESH="$prepare_refresh" \
        MODSECURITY_NGINX_SOURCE_DIR="$MODSECURITY_NGINX_SOURCE_DIR" \
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
    CONNECTOR_ORIGIN_SOURCE="$NGINX_ORIGIN_SOURCE" \
    CONNECTOR_ORIGIN_SOURCE_REPO="$NGINX_ORIGIN_SOURCE_REPO" \
    CONNECTOR_ORIGIN_SOURCE_URL="$NGINX_ORIGIN_SOURCE_URL" \
    CONNECTOR_ORIGIN_SOURCE_COMMIT="$NGINX_ORIGIN_SOURCE_COMMIT" \
    CONNECTOR_ORIGIN_SOURCE_VERSION="$NGINX_ORIGIN_SOURCE_VERSION" \
    CONNECTOR_ORIGIN_LICENSE="$NGINX_ORIGIN_LICENSE" \
    CONNECTOR_ORIGIN_IMPORTED_PATH="$NGINX_ORIGIN_IMPORTED_PATH" \
    SMOKE_CASES="$SMOKE_CASES" \
    CASE_SCOPE="$CASE_SCOPE" \
    sh "$REPO_ROOT/connectors/nginx/harness/run_nginx_smoke.sh"
