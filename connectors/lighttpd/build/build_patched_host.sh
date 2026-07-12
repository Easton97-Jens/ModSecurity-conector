#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH='' cd "$(dirname "$0")" && pwd)
BUILD_ROOT=${BUILD_ROOT:-${XDG_STATE_HOME:-${HOME:-/tmp}/.local/state}/ModSecurity-conector-build}
PATCHED_ROOT=${LIGHTTPD_PATCHED_ROOT:-$BUILD_ROOT/lighttpd-core-patched}
PATCHED_SOURCE_DIR=${LIGHTTPD_PATCHED_SOURCE_DIR:-$PATCHED_ROOT/lighttpd-1.4.84}
CORE_BUILD_DIR=${LIGHTTPD_PATCHED_BUILD_DIR:-$PATCHED_ROOT/build-1.4.84}
STAGE_ROOT=${LIGHTTPD_PATCHED_STAGE_DIR:-$PATCHED_ROOT/stage}
CORE_BIN=$STAGE_ROOT/bin/lighttpd
MODULE_DIR=$STAGE_ROOT/modules
MODULE_PATH=$MODULE_DIR/mod_msconnector.so
CONNECTOR_BUILD_DIR=$PATCHED_ROOT/connector-build
CORE_MANIFEST=$PATCHED_ROOT/patched-core-build-info.txt
HOST_MANIFEST=$PATCHED_ROOT/patched-host-build-info.txt
NM_BIN=${NM:-nm}

blocked() {
    printf 'lighttpd_patched_host_build: BLOCKED: %s\n' "$1" >&2
    exit 77
}

sha256_file() {
    sha256sum "$1" | awk '{print $1}'
}

[ -f "$CORE_MANIFEST" ] || blocked "patched core manifest is missing; run build-lighttpd-patched-core first"
[ -x "$CORE_BIN" ] || blocked "patched lighttpd binary is missing: $CORE_BIN"
[ -f "$CORE_BUILD_DIR/config.h" ] || blocked "patched generated config.h is missing: $CORE_BUILD_DIR/config.h"
[ -f "$PATCHED_SOURCE_DIR/src/plugin.h" ] || blocked "patched plugin headers are missing"
grep -Fq LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION "$PATCHED_SOURCE_DIR/src/plugin.h" || \
    blocked "patched plugin ABI marker is missing"
[ -n "$(sed -n 's/^patch_sha256=//p' "$CORE_MANIFEST" | sed -n '1p')" ] || \
    blocked "patched core manifest is missing its patch SHA-256"
[ -n "${MODSECURITY_INCLUDE_DIR:-}" ] || blocked "MODSECURITY_INCLUDE_DIR is required"
[ -n "${MODSECURITY_LIB_DIR:-}" ] || blocked "MODSECURITY_LIB_DIR is required"
command -v "$NM_BIN" >/dev/null 2>&1 || blocked "missing nm command: $NM_BIN"
command -v sha256sum >/dev/null 2>&1 || blocked "missing sha256sum command"

BUILD_ROOT="$BUILD_ROOT" \
LIGHTTPD_CONNECTOR_OUT_DIR="$CONNECTOR_BUILD_DIR" \
LIGHTTPD_MODULE_DIR="$MODULE_DIR" \
LIGHTTPD_MSCONNECTOR_CORE_MODE=patched \
LIGHTTPD_SOURCE_DIR="$PATCHED_SOURCE_DIR" \
LIGHTTPD_BUILD_ROOT="$CORE_BUILD_DIR" \
MODSECURITY_INCLUDE_DIR="$MODSECURITY_INCLUDE_DIR" \
MODSECURITY_LIB_DIR="$MODSECURITY_LIB_DIR" \
sh "$SCRIPT_DIR/build_module.sh"

[ -f "$MODULE_PATH" ] || blocked "staged patched module is missing: $MODULE_PATH"
"$NM_BIN" -D "$MODULE_PATH" | grep -Eq '[[:space:]][Tt][[:space:]]mod_msconnector_plugin_init$' || \
    blocked "staged patched module does not export mod_msconnector_plugin_init"

HOST_MANIFEST_TMP=$HOST_MANIFEST.tmp.$$
{
    printf 'lighttpd_version=1.4.84\n'
    sed -n 's/^patch_sha256=/patch_sha256=/p' "$CORE_MANIFEST"
    printf 'core_binary=%s\n' "$CORE_BIN"
    printf 'core_binary_sha256=%s\n' "$(sha256_file "$CORE_BIN")"
    printf 'module=%s\n' "$MODULE_PATH"
    printf 'module_sha256=%s\n' "$(sha256_file "$MODULE_PATH")"
    printf 'module_build_dir=%s\n' "$CONNECTOR_BUILD_DIR"
    printf 'modsecurity_lib_dir=%s\n' "$MODSECURITY_LIB_DIR"
    printf 'plugin_hook_abi=1\n'
    printf 'response_body_mode=none\n'
    printf 'response_hook_contract=http1_entity_body_before_transfer_encoding\n'
    printf 'phase4_runtime_evidence=not_executed\n'
} > "$HOST_MANIFEST_TMP"
mv "$HOST_MANIFEST_TMP" "$HOST_MANIFEST"

printf 'lighttpd_patched_host_build: PASS binary=%s module=%s manifest=%s\n' \
    "$CORE_BIN" "$MODULE_PATH" "$HOST_MANIFEST"
