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
DEFAULT_APACHE_SOURCE_DIR="$REPO_ROOT/connectors/apache/upstream"
MODSECURITY_APACHE_SOURCE_DIR="${MODSECURITY_APACHE_SOURCE_DIR:-$DEFAULT_APACHE_SOURCE_DIR}"
APACHE_ORIGIN_SOURCE="${APACHE_ORIGIN_SOURCE:-}"
APACHE_ORIGIN_SOURCE_REPO="${APACHE_ORIGIN_SOURCE_REPO:-}"
APACHE_ORIGIN_SOURCE_COMMIT="${APACHE_ORIGIN_SOURCE_COMMIT:-}"
APACHE_ORIGIN_SOURCE_VERSION="${APACHE_ORIGIN_SOURCE_VERSION:-}"
APACHE_ORIGIN_LICENSE="${APACHE_ORIGIN_LICENSE:-Apache-2.0}"
APACHE_ORIGIN_IMPORTED_PATH="${APACHE_ORIGIN_IMPORTED_PATH:-$MODSECURITY_APACHE_SOURCE_DIR}"
REFRESH="${REFRESH:-0}"
SMOKE_CASES="${SMOKE_CASES:-}"
CASE_SCOPE="${CASE_SCOPE:-all}"
BUILD_HTTPD_FROM_SOURCE="${BUILD_HTTPD_FROM_SOURCE:-1}"
BUILD_PCRE2_FROM_SOURCE="${BUILD_PCRE2_FROM_SOURCE:-1}"
APACHE_BUILD_LOG_DIR="${APACHE_BUILD_LOG_DIR:-$BUILD_ROOT/logs/apache}"
APACHE_RUNTIME_LOG_DIR="${APACHE_RUNTIME_LOG_DIR:-$BUILD_ROOT/logs/apache-runtime}"

git_value() {
    git_dir=$1
    shift
    if git -C "$git_dir" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        git -C "$git_dir" "$@" 2>/dev/null || true
    fi
}

configure_apache_origin() {
    if [ "$MODSECURITY_APACHE_SOURCE_DIR" = "$DEFAULT_APACHE_SOURCE_DIR" ]; then
        APACHE_ORIGIN_SOURCE="${APACHE_ORIGIN_SOURCE:-monorepo-upstream}"
        APACHE_ORIGIN_SOURCE_REPO="${APACHE_ORIGIN_SOURCE_REPO:-ModSecurity-apache}"
        APACHE_ORIGIN_SOURCE_COMMIT="${APACHE_ORIGIN_SOURCE_COMMIT:-0488c77f69669584324b70460614a382224b4883}"
        APACHE_ORIGIN_SOURCE_VERSION="${APACHE_ORIGIN_SOURCE_VERSION:-v0.0.9-beta1-26-g0488c77}"
        return
    fi
    APACHE_ORIGIN_SOURCE="${APACHE_ORIGIN_SOURCE:-external}"
    APACHE_ORIGIN_SOURCE_REPO="${APACHE_ORIGIN_SOURCE_REPO:-ModSecurity-apache}"
    APACHE_ORIGIN_SOURCE_COMMIT="${APACHE_ORIGIN_SOURCE_COMMIT:-$(git_value "$MODSECURITY_APACHE_SOURCE_DIR" rev-parse HEAD)}"
    APACHE_ORIGIN_SOURCE_VERSION="${APACHE_ORIGIN_SOURCE_VERSION:-$(git_value "$MODSECURITY_APACHE_SOURCE_DIR" describe --tags --always --dirty)}"
}

write_connector_result() {
    status=$1
    message=$2
    mkdir -p "$RESULTS_DIR"
    {
        printf '%s apache-build %s\n' "$(printf '%s' "$status" | tr '[:lower:]' '[:upper:]')" "$message"
    } > "$RESULTS_DIR/apache-summary.txt"
    python3 - "$RESULTS_DIR/apache-summary.json" "$status" "$HTTPD_PREFIX/bin/httpd" "$APACHE_MODULE" "$MODSECURITY_LIB_DIR/libmodsecurity.so" "$APACHE_ORIGIN_SOURCE" "$APACHE_ORIGIN_SOURCE_REPO" "$APACHE_ORIGIN_SOURCE_COMMIT" "$APACHE_ORIGIN_SOURCE_VERSION" "$APACHE_ORIGIN_LICENSE" "$APACHE_ORIGIN_IMPORTED_PATH" <<'PY'
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
    "apache": {
        "audit_behavior": "unstable",
        "build": status,
        "connector_path": "real-world",
        "environment": environment,
        "intervention_model": "msconnector_intervention",
        "origin_model": "msconnector_origin",
        "validation_mode": "real-world-connector-path",
        "status_model": "msconnector_status",
        "server": "apache",
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
    cp "$RESULTS_DIR/apache-summary.txt" "$RESULTS_DIR/connector-summary.txt"
}

configure_apache_origin

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
        MODSECURITY_APACHE_SOURCE_DIR="$MODSECURITY_APACHE_SOURCE_DIR" \
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
    CONNECTOR_ORIGIN_SOURCE="$APACHE_ORIGIN_SOURCE" \
    CONNECTOR_ORIGIN_SOURCE_REPO="$APACHE_ORIGIN_SOURCE_REPO" \
    CONNECTOR_ORIGIN_SOURCE_COMMIT="$APACHE_ORIGIN_SOURCE_COMMIT" \
    CONNECTOR_ORIGIN_SOURCE_VERSION="$APACHE_ORIGIN_SOURCE_VERSION" \
    CONNECTOR_ORIGIN_LICENSE="$APACHE_ORIGIN_LICENSE" \
    CONNECTOR_ORIGIN_IMPORTED_PATH="$APACHE_ORIGIN_IMPORTED_PATH" \
    SMOKE_CASES="$SMOKE_CASES" \
    CASE_SCOPE="$CASE_SCOPE" \
    sh "$REPO_ROOT/connectors/apache/harness/run_apache_smoke.sh"
