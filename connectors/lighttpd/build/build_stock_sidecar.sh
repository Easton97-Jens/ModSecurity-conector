#!/bin/sh
set -eu

AWK_FIRST='{print $1}'

SCRIPT_DIR=$(CDPATH='' cd "$(dirname "$0")" && pwd)
CONNECTOR_DIR=$(CDPATH='' cd "$SCRIPT_DIR/.." && pwd)
REPO_ROOT=$(CDPATH='' cd "$CONNECTOR_DIR/../.." && pwd)
BUILD_ROOT=${BUILD_ROOT:-}
OUT_DIR=${LIGHTTPD_STOCK_SIDECAR_OUT_DIR:-$BUILD_ROOT/lighttpd-stock-sidecar}
CC_BIN=${CC:-cc}
MSCONNECTOR_C_STD=${MSCONNECTOR_C_STD:-c17}

blocked() {
    blocked_message=$1
    printf 'lighttpd_stock_sidecar_build: BLOCKED: %s\n' "$blocked_message"
    exit 77
}

case "$BUILD_ROOT" in
    '') blocked "BUILD_ROOT is required" ;;
    /*) ;;
    *) blocked "BUILD_ROOT must be absolute: $BUILD_ROOT" ;;
esac
case "$OUT_DIR" in
    /*) ;;
    *) blocked "LIGHTTPD_STOCK_SIDECAR_OUT_DIR must be absolute: $OUT_DIR" ;;
esac
case "$(CDPATH='' cd "$BUILD_ROOT" 2>/dev/null && pwd 2>/dev/null || printf '%s' "$BUILD_ROOT")" in
    "$REPO_ROOT"|"$REPO_ROOT"/*) blocked "BUILD_ROOT must not be inside the checkout" ;;
    *) ;;
esac
case "$(CDPATH='' cd "$OUT_DIR" 2>/dev/null && pwd 2>/dev/null || printf '%s' "$OUT_DIR")" in
    "$REPO_ROOT"|"$REPO_ROOT"/*) blocked "LIGHTTPD_STOCK_SIDECAR_OUT_DIR must not be inside the checkout" ;;
    *) ;;
esac

[ -n "${MODSECURITY_INCLUDE_DIR:-}" ] || blocked "MODSECURITY_INCLUDE_DIR is required"
[ -n "${MODSECURITY_LIB_DIR:-}" ] || blocked "MODSECURITY_LIB_DIR is required"
case "$MODSECURITY_INCLUDE_DIR" in /*) ;; *) blocked "MODSECURITY_INCLUDE_DIR must be absolute" ;; esac
case "$MODSECURITY_LIB_DIR" in /*) ;; *) blocked "MODSECURITY_LIB_DIR must be absolute" ;; esac
[ -f "$MODSECURITY_INCLUDE_DIR/modsecurity/modsecurity.h" ] || \
    blocked "modsecurity/modsecurity.h is missing below MODSECURITY_INCLUDE_DIR"
[ -f "$MODSECURITY_LIB_DIR/libmodsecurity.so" ] || \
    blocked "libmodsecurity.so is missing below MODSECURITY_LIB_DIR"
command -v "$CC_BIN" >/dev/null 2>&1 || blocked "missing C compiler: $CC_BIN"
command -v sha256sum >/dev/null 2>&1 || blocked "missing sha256sum"
command -v git >/dev/null 2>&1 || blocked "missing git"
command -v awk >/dev/null 2>&1 || blocked "missing awk"
command -v mktemp >/dev/null 2>&1 || blocked "missing mktemp"

mkdir -p "$OUT_DIR"

compile_runtime_binary() {
    output=$1
    source=$2
    main_define=$3
    "$CC_BIN" \
        -std="$MSCONNECTOR_C_STD" \
        -Wall \
        -Wextra \
        -Werror \
        -pthread \
        $main_define \
        -I "$REPO_ROOT" \
        -I "$REPO_ROOT/common/include" \
        -I "$REPO_ROOT/common/runtime" \
        -I "$CONNECTOR_DIR/stock_sidecar" \
        -I "$MODSECURITY_INCLUDE_DIR" \
        "$source" \
        "$REPO_ROOT/common/runtime/msconnector_runtime.c" \
        "$REPO_ROOT/connectors/profile_registry.c" \
        "$REPO_ROOT"/common/src/*.c \
        -L "$MODSECURITY_LIB_DIR" \
        "-Wl,-rpath,$MODSECURITY_LIB_DIR" \
        -lmodsecurity \
        -lcrypto \
        -lyajl \
        -o "$output"
}

compile_runtime_binary \
    "$OUT_DIR/lighttpd-stock-sidecar" \
    "$CONNECTOR_DIR/stock_sidecar/stock_sidecar.c" \
    -DMSCONNECTOR_STOCK_SIDECAR_MAIN
compile_runtime_binary \
    "$OUT_DIR/runtime-begin-smoke" \
    "$CONNECTOR_DIR/stock_sidecar/runtime_begin_smoke.c" \
    ''

source_inputs_sha256() {
    (
        for source in \
            "$CONNECTOR_DIR/stock_sidecar/stock_sidecar.c" \
            "$CONNECTOR_DIR/stock_sidecar/runtime_begin_smoke.c" \
            "$CONNECTOR_DIR/stock_sidecar/stock_sidecar.h" \
            "$REPO_ROOT/common/runtime/msconnector_runtime.c" \
            "$REPO_ROOT/common/runtime/msconnector_runtime.h" \
            "$REPO_ROOT/connectors/profile_registry.c" \
            "$REPO_ROOT/connectors/profile_registry.h" \
            "$REPO_ROOT/common/src/header_validation_internal.h" \
            "$REPO_ROOT"/common/src/*.c \
            "$REPO_ROOT"/common/include/msconnector/*.h
        do
            source_relative=${source#"$REPO_ROOT"/}
            printf '%s\000' "$source_relative"
            sha256sum "$source" | awk "$AWK_FIRST"
        done
    ) | sha256sum | awk "$AWK_FIRST"
}

parent_commit=$(git -C "$REPO_ROOT" rev-parse HEAD) || blocked "cannot determine Parent commit"
case "$parent_commit" in
    ''|*[!0-9a-f]*) blocked "invalid Parent commit" ;;
    *) ;;
esac
case ${#parent_commit} in
    40|64) ;;
    *) blocked "invalid Parent commit" ;;
esac
git_status=0
git -C "$REPO_ROOT" diff --quiet HEAD -- || git_status=$?
case "$git_status" in
    0) parent_source_tree_state=clean ;;
    1) parent_source_tree_state=dirty ;;
    *) blocked "cannot determine Parent source-tree state" ;;
esac
sidecar_binary_sha256=$(sha256sum "$OUT_DIR/lighttpd-stock-sidecar" | awk "$AWK_FIRST")
runtime_begin_smoke_sha256=$(sha256sum "$OUT_DIR/runtime-begin-smoke" | awk "$AWK_FIRST")
sidecar_source_inputs_sha256=$(source_inputs_sha256)
modsecurity_library_sha256=$(sha256sum "$MODSECURITY_LIB_DIR/libmodsecurity.so" | awk "$AWK_FIRST")
artifact_manifest="$OUT_DIR/stock-sidecar-artifact.manifest"
artifact_manifest_tmp=$(mktemp "$OUT_DIR/.stock-sidecar-artifact.manifest.XXXXXX") || \
    blocked "cannot create Stock lighttpd Sidecar artifact manifest"

{
    printf 'schema_version=1\n'
    printf 'artifact_kind=lighttpd_stock_sidecar\n'
    printf 'connector_id=lighttpd\n'
    printf 'integration_mode=stock-lighttpd-sidecar\n'
    printf 'parent_commit_sha=%s\n' "$parent_commit"
    printf 'parent_source_tree_state=%s\n' "$parent_source_tree_state"
    printf 'c_standard=%s\n' "$MSCONNECTOR_C_STD"
    printf 'sidecar_path=%s\n' "$OUT_DIR/lighttpd-stock-sidecar"
    printf 'sidecar_binary_sha256=%s\n' "$sidecar_binary_sha256"
    printf 'runtime_begin_smoke_path=%s\n' "$OUT_DIR/runtime-begin-smoke"
    printf 'runtime_begin_smoke_sha256=%s\n' "$runtime_begin_smoke_sha256"
    printf 'sidecar_source_inputs_sha256=%s\n' "$sidecar_source_inputs_sha256"
    printf 'modsecurity_library_sha256=%s\n' "$modsecurity_library_sha256"
} > "$artifact_manifest_tmp"
chmod 0444 "$artifact_manifest_tmp"
mv -f "$artifact_manifest_tmp" "$artifact_manifest" || \
    blocked "cannot publish Stock lighttpd Sidecar artifact manifest"

{
    printf 'c_standard=%s\n' "$MSCONNECTOR_C_STD"
    printf 'connector_id=lighttpd\n'
    printf 'integration_mode=stock-lighttpd-sidecar\n'
    printf 'listen_scope=literal_ipv4_loopback_only\n'
    printf 'upstream_scope=literal_ipv4_loopback_only\n'
    printf 'sidecar=%s\n' "$OUT_DIR/lighttpd-stock-sidecar"
    printf 'runtime_begin_smoke=%s\n' "$OUT_DIR/runtime-begin-smoke"
    printf 'modsecurity_include_dir=%s\n' "$MODSECURITY_INCLUDE_DIR"
    printf 'modsecurity_lib_dir=%s\n' "$MODSECURITY_LIB_DIR"
    printf 'artifact_manifest=%s\n' "$artifact_manifest"
} > "$OUT_DIR/build-info.txt"

printf 'lighttpd_stock_sidecar_build: PASS output=%s\n' "$OUT_DIR/lighttpd-stock-sidecar"
