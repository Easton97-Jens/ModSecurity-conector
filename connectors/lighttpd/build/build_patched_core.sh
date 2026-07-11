#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH='' cd "$(dirname "$0")" && pwd)
CONNECTOR_DIR=$(CDPATH='' cd "$SCRIPT_DIR/.." && pwd)
REPO_ROOT=$(CDPATH='' cd "$CONNECTOR_DIR/../.." && pwd)
BUILD_ROOT=${BUILD_ROOT:-${XDG_STATE_HOME:-${HOME:-/tmp}/.local/state}/ModSecurity-conector-build}
PATCHED_ROOT=${LIGHTTPD_PATCHED_ROOT:-$BUILD_ROOT/lighttpd-core-patched}
PATCHED_SOURCE_DIR=${LIGHTTPD_PATCHED_SOURCE_DIR:-$PATCHED_ROOT/lighttpd-1.4.84}
CORE_BUILD_DIR=${LIGHTTPD_PATCHED_BUILD_DIR:-$PATCHED_ROOT/build-1.4.84}
STAGE_ROOT=${LIGHTTPD_PATCHED_STAGE_DIR:-$PATCHED_ROOT/stage}
CORE_BIN=$STAGE_ROOT/bin/lighttpd
CORE_MANIFEST=$PATCHED_ROOT/patched-core-build-info.txt
CC_BIN=${CC:-cc}
MAKE_BIN=${MAKE:-make}
NM_BIN=${NM:-nm}
MAKE_JOBS=${LIGHTTPD_MAKE_JOBS:-2}

blocked() {
    printf 'lighttpd_patched_core_build: BLOCKED: %s\n' "$1" >&2
    exit 77
}

manifest_value() {
    key=$1
    sed -n "s/^$key=//p" "$CORE_MANIFEST" | sed -n '1p'
}

sha256_file() {
    sha256sum "$1" | awk '{print $1}'
}

require_absolute_outside_checkout() {
    path=$1
    label=$2
    case "$path" in
        /*) ;;
        *) blocked "$label must be absolute: $path" ;;
    esac
    case "$(CDPATH='' cd "$path" 2>/dev/null && pwd 2>/dev/null || printf '%s' "$path")" in
        "$REPO_ROOT"|"$REPO_ROOT"/*)
            blocked "$label must not be inside the checkout: $path"
            ;;
        *) ;;
    esac
}

verify_core() {
    [ -x "$CORE_BIN" ] || blocked "staged patched lighttpd binary is missing: $CORE_BIN"
    [ -f "$CORE_BUILD_DIR/config.h" ] || blocked "patched generated config.h is missing: $CORE_BUILD_DIR/config.h"
    grep -Fq LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION "$PATCHED_SOURCE_DIR/src/plugin.h" || \
        blocked "patched plugin ABI marker is missing from $PATCHED_SOURCE_DIR"
    "$CORE_BIN" -v 2>&1 | grep -Fq 'lighttpd/1.4.84' || \
        blocked "staged binary does not report lighttpd/1.4.84"
    for symbol in plugins_call_handle_request_body plugins_call_handle_response_body; do
        "$NM_BIN" -D "$CORE_BIN" | grep -Eq "[[:space:]][Tt][[:space:]]$symbol$" || \
            blocked "patched binary does not export required hook symbol: $symbol"
    done
}

[ -n "${LIGHTTPD_SOURCE_DIR:-}" ] || blocked "LIGHTTPD_SOURCE_DIR is required"
case "$MAKE_JOBS" in
    [1-9]|[1-9][0-9]*) ;;
    *) blocked "LIGHTTPD_MAKE_JOBS must be a positive integer" ;;
esac
command -v "$CC_BIN" >/dev/null 2>&1 || blocked "missing C compiler: $CC_BIN"
command -v "$MAKE_BIN" >/dev/null 2>&1 || blocked "missing make command: $MAKE_BIN"
command -v "$NM_BIN" >/dev/null 2>&1 || blocked "missing nm command: $NM_BIN"
command -v sha256sum >/dev/null 2>&1 || blocked "missing sha256sum command"

require_absolute_outside_checkout "$BUILD_ROOT" "BUILD_ROOT"
require_absolute_outside_checkout "$PATCHED_ROOT" "LIGHTTPD_PATCHED_ROOT"
require_absolute_outside_checkout "$PATCHED_SOURCE_DIR" "LIGHTTPD_PATCHED_SOURCE_DIR"
require_absolute_outside_checkout "$CORE_BUILD_DIR" "LIGHTTPD_PATCHED_BUILD_DIR"
require_absolute_outside_checkout "$STAGE_ROOT" "LIGHTTPD_PATCHED_STAGE_DIR"
require_absolute_outside_checkout "$LIGHTTPD_SOURCE_DIR" "LIGHTTPD_SOURCE_DIR"

case "$PATCHED_SOURCE_DIR" in
    "$PATCHED_ROOT"/*) ;;
    *) blocked "LIGHTTPD_PATCHED_SOURCE_DIR must be below LIGHTTPD_PATCHED_ROOT" ;;
esac
case "$CORE_BUILD_DIR" in
    "$PATCHED_ROOT"/*) ;;
    *) blocked "LIGHTTPD_PATCHED_BUILD_DIR must be below LIGHTTPD_PATCHED_ROOT" ;;
esac
case "$STAGE_ROOT" in
    "$PATCHED_ROOT"/*) ;;
    *) blocked "LIGHTTPD_PATCHED_STAGE_DIR must be below LIGHTTPD_PATCHED_ROOT" ;;
esac

SOURCE_DIR=$(CDPATH='' cd "$LIGHTTPD_SOURCE_DIR" 2>/dev/null && pwd) || \
    blocked "LIGHTTPD_SOURCE_DIR is not accessible: $LIGHTTPD_SOURCE_DIR"
[ -f "$SOURCE_DIR/configure.ac" ] || blocked "LIGHTTPD_SOURCE_DIR is not a lighttpd source tree"
grep -Fq 'AC_INIT([lighttpd],[1.4.84]' "$SOURCE_DIR/configure.ac" || \
    blocked "patched core build is pinned to lighttpd 1.4.84"

BUILD_ROOT="$BUILD_ROOT" \
LIGHTTPD_SOURCE_DIR="$SOURCE_DIR" \
LIGHTTPD_PATCHED_SOURCE_DIR="$PATCHED_SOURCE_DIR" \
sh "$SCRIPT_DIR/apply_core_patch.sh" --apply

[ -f "$PATCHED_SOURCE_DIR/.msconnector-lighttpd-patch.sha256" ] || \
    blocked "patched source is missing its patch identity stamp"
PATCH_SHA256=$(cat "$PATCHED_SOURCE_DIR/.msconnector-lighttpd-patch.sha256")
case "$PATCH_SHA256" in
    ????????*) ;;
    *) blocked "patched source has an invalid patch identity stamp" ;;
esac

if [ -f "$CORE_MANIFEST" ]; then
    [ "$(manifest_value lighttpd_version)" = 1.4.84 ] || \
        blocked "existing patched core manifest has an unexpected lighttpd version"
    [ "$(manifest_value patch_sha256)" = "$PATCH_SHA256" ] || \
        blocked "existing patched core was built with a different patch; clean $PATCHED_ROOT first"
    verify_core
    [ "$(manifest_value binary_sha256)" = "$(sha256_file "$CORE_BIN")" ] || \
        blocked "staged patched binary does not match its build manifest"
    printf 'lighttpd_patched_core_build: PASS mode=reused binary=%s patch_sha256=%s\n' \
        "$CORE_BIN" "$PATCH_SHA256"
    exit 0
fi

if [ -e "$CORE_BUILD_DIR" ] || [ -e "$STAGE_ROOT" ]; then
    blocked "incomplete patched build exists; inspect or remove managed directory: $PATCHED_ROOT"
fi

[ -x "$PATCHED_SOURCE_DIR/configure" ] || blocked "patched source configure script is missing or not executable"
mkdir -p "$CORE_BUILD_DIR"
if [ -n "${LIGHTTPD_PATCHED_CFLAGS:-}" ]; then
    (cd "$CORE_BUILD_DIR" && \
        CC="$CC_BIN" CFLAGS="$LIGHTTPD_PATCHED_CFLAGS" "$PATCHED_SOURCE_DIR/configure" \
            --prefix="$STAGE_ROOT" \
            --bindir="$STAGE_ROOT/bin" \
            --sbindir="$STAGE_ROOT/bin" \
            --libdir="$STAGE_ROOT/lib") >"$CORE_BUILD_DIR/configure.log" 2>&1
else
    (cd "$CORE_BUILD_DIR" && \
        CC="$CC_BIN" "$PATCHED_SOURCE_DIR/configure" \
            --prefix="$STAGE_ROOT" \
            --bindir="$STAGE_ROOT/bin" \
            --sbindir="$STAGE_ROOT/bin" \
            --libdir="$STAGE_ROOT/lib") >"$CORE_BUILD_DIR/configure.log" 2>&1
fi
"$MAKE_BIN" -C "$CORE_BUILD_DIR" -j "$MAKE_JOBS" >"$CORE_BUILD_DIR/make.log" 2>&1
"$MAKE_BIN" -C "$CORE_BUILD_DIR" install >"$CORE_BUILD_DIR/install.log" 2>&1

verify_core
MANIFEST_TMP=$CORE_MANIFEST.tmp.$$
{
    printf 'lighttpd_version=1.4.84\n'
    printf 'patch_sha256=%s\n' "$PATCH_SHA256"
    printf 'patched_source_dir=%s\n' "$PATCHED_SOURCE_DIR"
    printf 'core_build_dir=%s\n' "$CORE_BUILD_DIR"
    printf 'stage_root=%s\n' "$STAGE_ROOT"
    printf 'binary=%s\n' "$CORE_BIN"
    printf 'binary_sha256=%s\n' "$(sha256_file "$CORE_BIN")"
    printf 'plugin_hook_abi=1\n'
    printf 'response_hook_contract=http1_wire_output_only_not_decoded_entity\n'
} > "$MANIFEST_TMP"
mv "$MANIFEST_TMP" "$CORE_MANIFEST"

printf 'lighttpd_patched_core_build: PASS mode=build binary=%s patch_sha256=%s\n' \
    "$CORE_BIN" "$PATCH_SHA256"
