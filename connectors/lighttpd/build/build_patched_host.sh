#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH='' cd "$(dirname "$0")" && pwd)
LIGHTTPD_VERSION=$(sh "$SCRIPT_DIR/read_version.sh")
BUILD_ROOT=${BUILD_ROOT:-${XDG_STATE_HOME:-${HOME:-/tmp}/.local/state}/ModSecurity-conector-build}
PATCHED_ROOT=${LIGHTTPD_PATCHED_ROOT:-$BUILD_ROOT/lighttpd-core-patched}
PATCHED_SOURCE_DIR=${LIGHTTPD_PATCHED_SOURCE_DIR:-$PATCHED_ROOT/lighttpd-$LIGHTTPD_VERSION}
CORE_BUILD_DIR=${LIGHTTPD_PATCHED_BUILD_DIR:-$PATCHED_ROOT/build-$LIGHTTPD_VERSION}
STAGE_ROOT=${LIGHTTPD_PATCHED_STAGE_DIR:-$PATCHED_ROOT/stage}
CORE_BIN=$STAGE_ROOT/bin/lighttpd
MODULE_DIR=$STAGE_ROOT/modules
MODULE_PATH=$MODULE_DIR/mod_msconnector.so
PROXY_MODULE_PATH=$MODULE_DIR/mod_proxy.so
CONNECTOR_BUILD_DIR=$PATCHED_ROOT/connector-build
CORE_MANIFEST=$PATCHED_ROOT/patched-core-build-info.txt
HOST_MANIFEST=$PATCHED_ROOT/patched-host-build-info.txt
NM_BIN=${NM:-nm}

blocked() {
    reason=$1
    printf 'lighttpd_patched_host_build: BLOCKED: %s\n' "$reason" >&2
    exit 77
}

sha256_file() {
    input_path=$1
    sha256sum "$input_path" | awk '{print $1}'
}

hook_abi_from_header() {
    header=$1
    awk '
        $1 == "#define" && $2 == "LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION" {
            if ($3 !~ /^[0-9]+$/) exit 1
            value=$3
            count++
        }
        END {
            if (count != 1) exit 1
            print value
        }
    ' "$header"
}

[ -f "$CORE_MANIFEST" ] || blocked "patched core manifest is missing; run build-lighttpd-patched-core first"
[ -x "$CORE_BIN" ] || blocked "patched lighttpd binary is missing: $CORE_BIN"
[ -f "$CORE_BUILD_DIR/config.h" ] || blocked "patched generated config.h is missing: $CORE_BUILD_DIR/config.h"
[ -f "$PATCHED_SOURCE_DIR/src/plugin.h" ] || blocked "patched plugin headers are missing"
HOOK_ABI=$(hook_abi_from_header "$PATCHED_SOURCE_DIR/src/plugin.h") || \
    blocked "patched plugin ABI marker is missing or ambiguous"
[ "$HOOK_ABI" = 2 ] || blocked "patched host requires response-abort hook ABI v2, found v$HOOK_ABI"
grep -Fq 'LIGHTTPD_MSCONNECTOR_PLUGIN_ABI_VERSION' "$PATCHED_SOURCE_DIR/src/plugin.h" || \
    blocked "patched plugin ABI formula is missing"
[ -n "$(sed -n 's/^patch_sha256=//p' "$CORE_MANIFEST" | sed -n '1p')" ] || \
    blocked "patched core manifest is missing its patch SHA-256"
[ "$(sed -n 's/^plugin_hook_abi=//p' "$CORE_MANIFEST" | sed -n '1p')" = "$HOOK_ABI" ] || \
    blocked "patched core manifest does not prove the same plugin hook ABI"
[ -n "${MODSECURITY_INCLUDE_DIR:-}" ] || blocked "MODSECURITY_INCLUDE_DIR is required"
[ -n "${MODSECURITY_LIB_DIR:-}" ] || blocked "MODSECURITY_LIB_DIR is required"
command -v "$NM_BIN" >/dev/null 2>&1 || blocked "missing nm command: $NM_BIN"
command -v sha256sum >/dev/null 2>&1 || blocked "missing sha256sum command"

for symbol in plugins_call_handle_request_body plugins_call_handle_response_body plugins_call_handle_response_abort; do
    "$NM_BIN" -D "$CORE_BIN" | grep -Eq "[[:space:]][Tt][[:space:]]$symbol$" || \
        blocked "patched core does not export required hook symbol: $symbol"
done

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

# The full-lifecycle entity-body proof uses lighttpd's native HTTP/1.1 reverse
# proxy.  Keep that module next to mod_msconnector so the explicit -m runtime
# directory loads only the staged patched-host modules, never a system copy.
PROXY_MODULE_SOURCE=
for candidate in "$STAGE_ROOT/lib/mod_proxy.so" "$STAGE_ROOT/lib/lighttpd/mod_proxy.so"; do
    if [ -f "$candidate" ]; then
        PROXY_MODULE_SOURCE=$candidate
        break
    fi
done
[ -n "$PROXY_MODULE_SOURCE" ] || blocked "staged patched lighttpd mod_proxy module is missing"
cp "$PROXY_MODULE_SOURCE" "$PROXY_MODULE_PATH"
[ -f "$PROXY_MODULE_PATH" ] || blocked "staged proxy module copy is missing: $PROXY_MODULE_PATH"
"$NM_BIN" -D "$PROXY_MODULE_PATH" | grep -Eq '[[:space:]][Tt][[:space:]]mod_proxy_plugin_init$' || \
    blocked "staged proxy module does not export mod_proxy_plugin_init"

HOST_MANIFEST_TMP=$HOST_MANIFEST.tmp.$$
{
    printf 'lighttpd_version=%s\n' "$LIGHTTPD_VERSION"
    sed -n 's/^patch_sha256=/patch_sha256=/p' "$CORE_MANIFEST"
    printf 'core_binary=%s\n' "$CORE_BIN"
    printf 'core_binary_sha256=%s\n' "$(sha256_file "$CORE_BIN")"
    printf 'module=%s\n' "$MODULE_PATH"
    printf 'module_sha256=%s\n' "$(sha256_file "$MODULE_PATH")"
    printf 'proxy_module=%s\n' "$PROXY_MODULE_PATH"
    printf 'proxy_module_sha256=%s\n' "$(sha256_file "$PROXY_MODULE_PATH")"
    printf 'module_build_dir=%s\n' "$CONNECTOR_BUILD_DIR"
    printf 'modsecurity_lib_dir=%s\n' "$MODSECURITY_LIB_DIR"
    printf 'plugin_hook_abi=%s\n' "$HOOK_ABI"
    printf 'response_body_mode=none\n'
    printf 'response_hook_contract=http1_entity_body_before_transfer_encoding\n'
    printf 'phase4_runtime_evidence=not_executed\n'
} > "$HOST_MANIFEST_TMP"
mv "$HOST_MANIFEST_TMP" "$HOST_MANIFEST"

printf 'lighttpd_patched_host_build: PASS binary=%s module=%s manifest=%s\n' \
    "$CORE_BIN" "$MODULE_PATH" "$HOST_MANIFEST"
