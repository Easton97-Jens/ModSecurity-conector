#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH='' cd "$(dirname "$0")" && pwd)
BUILD_ROOT=${BUILD_ROOT:-${XDG_STATE_HOME:-${HOME:-/tmp}/.local/state}/ModSecurity-conector-build}
PATCHED_ROOT=${LIGHTTPD_PATCHED_ROOT:-$BUILD_ROOT/lighttpd-core-patched}
PATCHED_SOURCE_DIR=${LIGHTTPD_PATCHED_SOURCE_DIR:-$PATCHED_ROOT/lighttpd-1.4.84}
SMOKE_DIR=${LIGHTTPD_PATCHED_SMOKE_DIR:-${LIGHTTPD_SMOKE_DIR:-$PATCHED_ROOT/smoke}}

blocked() {
    printf 'lighttpd_patched_lifecycle_config: BLOCKED: %s\n' "$1" >&2
    exit 77
}

case "$PATCHED_ROOT" in
    /*) ;;
    *) blocked "LIGHTTPD_PATCHED_ROOT must be absolute: $PATCHED_ROOT" ;;
esac
case "$SMOKE_DIR" in
    /*) ;;
    *) blocked "LIGHTTPD_PATCHED_SMOKE_DIR must be absolute: $SMOKE_DIR" ;;
esac
[ -f "$PATCHED_SOURCE_DIR/src/plugin.h" ] || blocked "patched source is missing: $PATCHED_SOURCE_DIR"
grep -Fq LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION "$PATCHED_SOURCE_DIR/src/plugin.h" || \
    blocked "patched source does not expose the required hook ABI"

# The current output hook receives HTTP/1 wire bytes, not decoded entity bytes.
# It can therefore expose P1/P2/P3 from the real host path, but never promotes
# a response-body/Phase-4 claim.
case "${LIGHTTPD_PATCHED_REQUEST_BODY_MODE:-none}" in
    none|streaming) ;;
    *) blocked "LIGHTTPD_PATCHED_REQUEST_BODY_MODE must be none or streaming" ;;
esac
case "${LIGHTTPD_PATCHED_RESPONSE_BODY_MODE:-none}" in
    none) ;;
    *) blocked "patched lifecycle smoke cannot enable response-body inspection: output hook exposes wire bytes, not decoded entities" ;;
esac

LIGHTTPD_SMOKE_DIR="$SMOKE_DIR" \
LIGHTTPD_REQUEST_BODY_MODE="${LIGHTTPD_PATCHED_REQUEST_BODY_MODE:-none}" \
LIGHTTPD_RESPONSE_BODY_MODE=none \
LIGHTTPD_RESPONSE_HEADER_MARKER="${LIGHTTPD_PATCHED_RESPONSE_HEADER_MARKER:-}" \
exec sh "$SCRIPT_DIR/prepare_native_smoke.sh"
