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
DEFAULT_APACHE_SOURCE_DIR="$REPO_ROOT/connectors/apache"
MODSECURITY_APACHE_SOURCE_DIR="${MODSECURITY_APACHE_SOURCE_DIR:-$DEFAULT_APACHE_SOURCE_DIR}"
APACHE_ORIGIN_SOURCE="${APACHE_ORIGIN_SOURCE:-}"
APACHE_ORIGIN_SOURCE_REPO="${APACHE_ORIGIN_SOURCE_REPO:-}"
APACHE_ORIGIN_SOURCE_URL="${APACHE_ORIGIN_SOURCE_URL:-}"
APACHE_ORIGIN_SOURCE_COMMIT="${APACHE_ORIGIN_SOURCE_COMMIT:-}"
APACHE_ORIGIN_SOURCE_VERSION="${APACHE_ORIGIN_SOURCE_VERSION:-}"
APACHE_ORIGIN_LICENSE="${APACHE_ORIGIN_LICENSE:-}"
APACHE_ORIGIN_IMPORTED_PATH="${APACHE_ORIGIN_IMPORTED_PATH:-}"
REFRESH="${REFRESH:-0}"
SMOKE_CASES="${SMOKE_CASES:-}"
CASE_SCOPE="${CASE_SCOPE:-all}"
BUILD_HTTPD_FROM_SOURCE="${BUILD_HTTPD_FROM_SOURCE:-1}"
BUILD_PCRE2_FROM_SOURCE="${BUILD_PCRE2_FROM_SOURCE:-1}"
APACHE_BUILD_LOG_DIR="${APACHE_BUILD_LOG_DIR:-$BUILD_ROOT/logs/apache}"
APACHE_RUNTIME_LOG_DIR="${APACHE_RUNTIME_LOG_DIR:-$BUILD_ROOT/logs/apache-runtime}"
PYTHON_BIN="${PYTHON:-python3}"

git_value() {
    git_dir=$1
    shift
    if git -C "$git_dir" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        git -C "$git_dir" "$@" 2>/dev/null || true
    fi
}

load_apache_adapter_metadata() {
    eval "$("$PYTHON_BIN" "$REPO_ROOT/ci/adapter_metadata.py" shell apache --prefix APACHE_ADAPTER)"
}

configure_apache_origin() {
    load_apache_adapter_metadata
    if [ "$MODSECURITY_APACHE_SOURCE_DIR" = "$DEFAULT_APACHE_SOURCE_DIR" ]; then
        APACHE_ORIGIN_SOURCE="${APACHE_ORIGIN_SOURCE:-$APACHE_ADAPTER_SOURCE}"
        APACHE_ORIGIN_SOURCE_REPO="${APACHE_ORIGIN_SOURCE_REPO:-$APACHE_ADAPTER_SOURCE_REPO}"
        APACHE_ORIGIN_SOURCE_URL="${APACHE_ORIGIN_SOURCE_URL:-$APACHE_ADAPTER_SOURCE_URL}"
        APACHE_ORIGIN_SOURCE_COMMIT="${APACHE_ORIGIN_SOURCE_COMMIT:-$APACHE_ADAPTER_SOURCE_COMMIT}"
        APACHE_ORIGIN_SOURCE_VERSION="${APACHE_ORIGIN_SOURCE_VERSION:-$APACHE_ADAPTER_SOURCE_VERSION}"
        APACHE_ORIGIN_LICENSE="${APACHE_ORIGIN_LICENSE:-$APACHE_ADAPTER_LICENSE}"
        APACHE_ORIGIN_IMPORTED_PATH="${APACHE_ORIGIN_IMPORTED_PATH:-$APACHE_ADAPTER_IMPORTED_PATH}"
        return
    fi
    APACHE_ORIGIN_SOURCE="${APACHE_ORIGIN_SOURCE:-external}"
    APACHE_ORIGIN_SOURCE_REPO="${APACHE_ORIGIN_SOURCE_REPO:-$APACHE_ADAPTER_SOURCE_REPO}"
    APACHE_ORIGIN_SOURCE_URL="${APACHE_ORIGIN_SOURCE_URL:-$APACHE_ADAPTER_SOURCE_URL}"
    APACHE_ORIGIN_SOURCE_COMMIT="${APACHE_ORIGIN_SOURCE_COMMIT:-$(git_value "$MODSECURITY_APACHE_SOURCE_DIR" rev-parse HEAD)}"
    APACHE_ORIGIN_SOURCE_VERSION="${APACHE_ORIGIN_SOURCE_VERSION:-$(git_value "$MODSECURITY_APACHE_SOURCE_DIR" describe --tags --always --dirty)}"
    APACHE_ORIGIN_LICENSE="${APACHE_ORIGIN_LICENSE:-$APACHE_ADAPTER_LICENSE}"
    APACHE_ORIGIN_IMPORTED_PATH="${APACHE_ORIGIN_IMPORTED_PATH:-$MODSECURITY_APACHE_SOURCE_DIR}"
}

write_connector_result() {
    status=$1
    message=$2
    mkdir -p "$RESULTS_DIR"
    "$PYTHON_BIN" "$REPO_ROOT/tests/runners/case_cli.py" summarize-empty \
        --connector apache \
        --status "$status" \
        --message "$message" \
        --summary-json "$RESULTS_DIR/apache-summary.json" \
        --summary-text "$RESULTS_DIR/apache-summary.txt" \
        --connector-path real-world \
        --validation-mode real-world-connector-path \
        --server apache \
        --server-binary "$HTTPD_PREFIX/bin/httpd" \
        --module "$APACHE_MODULE" \
        --libmodsecurity "$MODSECURITY_LIB_DIR/libmodsecurity.so" \
        --origin-source "$APACHE_ORIGIN_SOURCE" \
        --origin-source-repo "$APACHE_ORIGIN_SOURCE_REPO" \
        --origin-source-url "$APACHE_ORIGIN_SOURCE_URL" \
        --origin-source-commit "$APACHE_ORIGIN_SOURCE_COMMIT" \
        --origin-source-version "$APACHE_ORIGIN_SOURCE_VERSION" \
        --origin-license "$APACHE_ORIGIN_LICENSE" \
        --origin-imported-path "$APACHE_ORIGIN_IMPORTED_PATH"
    cp "$RESULTS_DIR/apache-summary.txt" "$RESULTS_DIR/connector-summary.txt"
}

configure_apache_origin

apache_adapter_build_current() {
    manifest="$APACHE_BUILD_ROOT/connector-src/materialized-source.json"
    [ -f "$manifest" ] || return 1
    "$PYTHON_BIN" - "$manifest" <<'PY'
import json
import sys

required_adapter_owned = {
    "autogen.sh",
    "configure.ac",
    "Makefile.am",
    "build/apxs-wrapper.in",
    "build/ax_prog_apache.m4",
    "build/find_apxs.m4",
    "build/find_libmodsec.m4",
    "src/mod_security3.c",
    "src/mod_security3.h",
    "src/msc_config.c",
    "src/msc_config.h",
    "src/msc_filters.c",
    "src/msc_filters.h",
    "src/msc_utils.c",
    "src/msc_utils.h",
    "t/conf/extra.conf.in",
    "tests/run-regression-tests.pl.in",
    "tests/regression/server_root/conf/httpd.conf.in",
    "tests/regression/misc/40-secRemoteRules.t.in",
    "tests/regression/misc/50-ipmatchfromfile-external.t.in",
    "tests/regression/misc/60-pmfromfile-external.t.in",
}
removed_from_source_tree = {
    "AUTHORS",
    "CHANGES",
    "LICENSE",
    "README.md",
    "SOURCE_MAP.json",
    "metadata.c",
    "metadata.h",
    "src/SOURCE_MAP.json",
    "src/metadata.c",
    "src/metadata.h",
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
if any(path in sources_by_path for path in removed_from_source_tree):
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
elif [ ! -x "$HTTPD_PREFIX/bin/httpd" ] || [ ! -x "$HTTPD_PREFIX/bin/apxs" ]; then
    needs_build=1
elif [ ! -f "$APACHE_MODULE" ] || [ ! -f "$MODSECURITY_LIB_DIR/libmodsecurity.so" ]; then
    needs_build=1
elif [ "$MODSECURITY_APACHE_SOURCE_DIR" = "$DEFAULT_APACHE_SOURCE_DIR" ] && ! apache_adapter_build_current; then
    echo "run_apache_smoke: existing Apache build predates adapter-owned materialized source; refreshing build artifacts"
    needs_build=1
    prepare_refresh=1
fi

if [ "$needs_build" -eq 1 ]; then
    echo "run_apache_smoke: preparing Apache PoC build"
    set +e
    REFRESH="$prepare_refresh" \
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
    CONNECTOR_ORIGIN_SOURCE_URL="$APACHE_ORIGIN_SOURCE_URL" \
    CONNECTOR_ORIGIN_SOURCE_COMMIT="$APACHE_ORIGIN_SOURCE_COMMIT" \
    CONNECTOR_ORIGIN_SOURCE_VERSION="$APACHE_ORIGIN_SOURCE_VERSION" \
    CONNECTOR_ORIGIN_LICENSE="$APACHE_ORIGIN_LICENSE" \
    CONNECTOR_ORIGIN_IMPORTED_PATH="$APACHE_ORIGIN_IMPORTED_PATH" \
    SMOKE_CASES="$SMOKE_CASES" \
    CASE_SCOPE="$CASE_SCOPE" \
    sh "$REPO_ROOT/connectors/apache/harness/run_apache_smoke.sh"
