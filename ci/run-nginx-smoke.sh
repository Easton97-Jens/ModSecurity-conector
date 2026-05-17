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
DEFAULT_NGINX_SOURCE_DIR="$REPO_ROOT/connectors/nginx/upstream"
MODSECURITY_NGINX_SOURCE_DIR="${MODSECURITY_NGINX_SOURCE_DIR:-$DEFAULT_NGINX_SOURCE_DIR}"
NGINX_ORIGIN_SOURCE="${NGINX_ORIGIN_SOURCE:-}"
NGINX_ORIGIN_SOURCE_REPO="${NGINX_ORIGIN_SOURCE_REPO:-}"
NGINX_ORIGIN_SOURCE_COMMIT="${NGINX_ORIGIN_SOURCE_COMMIT:-}"
NGINX_ORIGIN_SOURCE_VERSION="${NGINX_ORIGIN_SOURCE_VERSION:-}"
NGINX_ORIGIN_LICENSE="${NGINX_ORIGIN_LICENSE:-Apache-2.0}"
NGINX_ORIGIN_IMPORTED_PATH="${NGINX_ORIGIN_IMPORTED_PATH:-$MODSECURITY_NGINX_SOURCE_DIR}"
REFRESH="${REFRESH:-0}"
SMOKE_CASES="${SMOKE_CASES:-}"
CASE_SCOPE="${CASE_SCOPE:-all}"
BUILD_NGINX_FROM_SOURCE="${BUILD_NGINX_FROM_SOURCE:-1}"
NGINX_BUILD_LOG_DIR="${NGINX_BUILD_LOG_DIR:-$BUILD_ROOT/logs/nginx}"
NGINX_RUNTIME_LOG_DIR="${NGINX_RUNTIME_LOG_DIR:-$BUILD_ROOT/logs/nginx-runtime}"

git_value() {
    git_dir=$1
    shift
    if git -C "$git_dir" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        git -C "$git_dir" "$@" 2>/dev/null || true
    fi
}

configure_nginx_origin() {
    if [ "$MODSECURITY_NGINX_SOURCE_DIR" = "$DEFAULT_NGINX_SOURCE_DIR" ]; then
        NGINX_ORIGIN_SOURCE="${NGINX_ORIGIN_SOURCE:-monorepo-upstream}"
        NGINX_ORIGIN_SOURCE_REPO="${NGINX_ORIGIN_SOURCE_REPO:-ModSecurity-nginx}"
        NGINX_ORIGIN_SOURCE_COMMIT="${NGINX_ORIGIN_SOURCE_COMMIT:-9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846}"
        NGINX_ORIGIN_SOURCE_VERSION="${NGINX_ORIGIN_SOURCE_VERSION:-v1.0.4-14-g9eb44fd}"
        return
    fi
    NGINX_ORIGIN_SOURCE="${NGINX_ORIGIN_SOURCE:-external}"
    NGINX_ORIGIN_SOURCE_REPO="${NGINX_ORIGIN_SOURCE_REPO:-ModSecurity-nginx}"
    NGINX_ORIGIN_SOURCE_COMMIT="${NGINX_ORIGIN_SOURCE_COMMIT:-$(git_value "$MODSECURITY_NGINX_SOURCE_DIR" rev-parse HEAD)}"
    NGINX_ORIGIN_SOURCE_VERSION="${NGINX_ORIGIN_SOURCE_VERSION:-$(git_value "$MODSECURITY_NGINX_SOURCE_DIR" describe --tags --always --dirty)}"
}

write_connector_result() {
    status=$1
    message=$2
    mkdir -p "$RESULTS_DIR"
    {
        printf '%s nginx-build %s\n' "$(printf '%s' "$status" | tr '[:lower:]' '[:upper:]')" "$message"
    } > "$RESULTS_DIR/nginx-summary.txt"
    python3 - "$RESULTS_DIR/nginx-summary.json" "$status" "$NGINX_BINARY" "$NGINX_MODULE" "$MODSECURITY_LIB_DIR/libmodsecurity.so" "$NGINX_ORIGIN_SOURCE" "$NGINX_ORIGIN_SOURCE_REPO" "$NGINX_ORIGIN_SOURCE_COMMIT" "$NGINX_ORIGIN_SOURCE_VERSION" "$NGINX_ORIGIN_LICENSE" "$NGINX_ORIGIN_IMPORTED_PATH" <<'PY'
import json
import os
import sys

(
    output,
    status,
    server_binary,
    module,
    libmodsecurity,
    origin_source,
    origin_source_repo,
    origin_source_commit,
    origin_source_version,
    origin_license,
    origin_imported_path,
) = sys.argv[1:]
environment = os.environ.get("SMOKE_ENVIRONMENT") or (
    "github-actions" if os.environ.get("GITHUB_ACTIONS", "").lower() == "true" else "local"
)
summary = {
    "nginx": {
        "audit_behavior": "unstable",
        "build": status,
        "connector_path": "real-world",
        "environment": environment,
        "intervention_model": "msconnector_intervention",
        "origin_model": "msconnector_origin",
        "validation_mode": "real-world-connector-path",
        "status_model": "msconnector_status",
        "server": "nginx",
        "server_binary": server_binary,
        "module": module,
        "libmodsecurity": libmodsecurity,
        "origin": {
            "source": origin_source,
            "source_repo": origin_source_repo,
            "source_commit": origin_source_commit,
            "source_version": origin_source_version,
            "license": origin_license,
            "imported_path": origin_imported_path,
        },
        "verified_variables": [],
        "summary": {
            "pass": 0,
            "fail": 1 if status == "fail" else 0,
            "blocked": 1 if status == "blocked" else 0,
            "skipped": 0,
            "xfail": 0,
        },
        "cases": {},
    }
}
with open(output, "w", encoding="utf-8") as handle:
    json.dump(summary, handle, indent=2, sort_keys=True)
    handle.write("\n")
PY
    cp "$RESULTS_DIR/nginx-summary.txt" "$RESULTS_DIR/connector-summary.txt"
}

configure_nginx_origin

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
    CONNECTOR_ORIGIN_SOURCE_COMMIT="$NGINX_ORIGIN_SOURCE_COMMIT" \
    CONNECTOR_ORIGIN_SOURCE_VERSION="$NGINX_ORIGIN_SOURCE_VERSION" \
    CONNECTOR_ORIGIN_LICENSE="$NGINX_ORIGIN_LICENSE" \
    CONNECTOR_ORIGIN_IMPORTED_PATH="$NGINX_ORIGIN_IMPORTED_PATH" \
    SMOKE_CASES="$SMOKE_CASES" \
    CASE_SCOPE="$CASE_SCOPE" \
    sh "$REPO_ROOT/connectors/nginx/harness/run_nginx_smoke.sh"
