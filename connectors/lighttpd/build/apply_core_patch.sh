#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH='' cd "$(dirname "$0")" && pwd)
CONNECTOR_DIR=$(CDPATH='' cd "$SCRIPT_DIR/.." && pwd)
REPO_ROOT=$(CDPATH='' cd "$CONNECTOR_DIR/../.." && pwd)
PATCH_FILE=$CONNECTOR_DIR/patches/0001-lighttpd-1.4.84-msconnector-stream-hooks.patch
BUILD_ROOT=${BUILD_ROOT:-${XDG_STATE_HOME:-${HOME:-/tmp}/.local/state}/ModSecurity-conector-build}

blocked() {
    printf 'lighttpd_core_patch: BLOCKED: %s\n' "$1"
    exit 77
}

[ "$#" -eq 1 ] || blocked "usage: $0 --check|--apply"
[ -n "${LIGHTTPD_SOURCE_DIR:-}" ] || blocked "LIGHTTPD_SOURCE_DIR is required"

case "$LIGHTTPD_SOURCE_DIR" in
    /*) ;;
    *) blocked "LIGHTTPD_SOURCE_DIR must be absolute: $LIGHTTPD_SOURCE_DIR" ;;
esac
case "$BUILD_ROOT" in
    /*) ;;
    *) blocked "BUILD_ROOT must be absolute: $BUILD_ROOT" ;;
esac

SOURCE_DIR=$(CDPATH='' cd "$LIGHTTPD_SOURCE_DIR" 2>/dev/null && pwd) || \
    blocked "LIGHTTPD_SOURCE_DIR is not accessible: $LIGHTTPD_SOURCE_DIR"
PATCHED_SOURCE_DIR=${LIGHTTPD_PATCHED_SOURCE_DIR:-$BUILD_ROOT/lighttpd-core-patched/lighttpd-1.4.84}
case "$PATCHED_SOURCE_DIR" in
    /*) ;;
    *) blocked "LIGHTTPD_PATCHED_SOURCE_DIR must be absolute: $PATCHED_SOURCE_DIR" ;;
esac
case "$PATCHED_SOURCE_DIR" in
    "$REPO_ROOT"|"$REPO_ROOT"/*)
        blocked "LIGHTTPD_PATCHED_SOURCE_DIR must not be inside the checkout"
        ;;
esac

[ -f "$PATCH_FILE" ] || blocked "missing versioned patch: $PATCH_FILE"
[ -f "$SOURCE_DIR/src/plugin.h" ] || blocked "not a lighttpd source tree"
[ -f "$SOURCE_DIR/configure.ac" ] || blocked "missing configure.ac"
grep -Fq 'AC_INIT([lighttpd],[1.4.84]' "$SOURCE_DIR/configure.ac" || \
    blocked "patch is pinned to lighttpd 1.4.84"
command -v patch >/dev/null 2>&1 || blocked "missing patch command"

case "$1" in
--check)
    patch --dry-run --forward -p1 -d "$SOURCE_DIR" < "$PATCH_FILE"
    printf 'lighttpd_core_patch: PASS mode=check version=1.4.84 source=%s\n' "$SOURCE_DIR"
    ;;
--apply)
    if [ -e "$PATCHED_SOURCE_DIR" ]; then
        if [ -f "$PATCHED_SOURCE_DIR/src/plugin.h" ] && \
           grep -Fq LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION \
               "$PATCHED_SOURCE_DIR/src/plugin.h"; then
            printf 'lighttpd_core_patch: PASS mode=already-applied patched_source=%s\n' \
                "$PATCHED_SOURCE_DIR"
            exit 0
        fi
        blocked "refusing to replace existing non-patched source directory: $PATCHED_SOURCE_DIR"
    fi
    parent_dir=$(dirname "$PATCHED_SOURCE_DIR")
    mkdir -p "$parent_dir"
    temp_dir=$PATCHED_SOURCE_DIR.tmp.$$
    trap 'rm -rf "$temp_dir"' EXIT HUP INT TERM
    cp -a "$SOURCE_DIR/." "$temp_dir"
    patch --forward -p1 -d "$temp_dir" < "$PATCH_FILE"
    grep -Fq LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION \
        "$temp_dir/src/plugin.h" || blocked "patched plugin ABI marker was not found"
    mv "$temp_dir" "$PATCHED_SOURCE_DIR"
    trap - EXIT HUP INT TERM
    printf 'lighttpd_core_patch: PASS mode=apply version=1.4.84 patched_source=%s\n' \
        "$PATCHED_SOURCE_DIR"
    ;;
*)
    blocked "usage: $0 --check|--apply"
    ;;
esac
