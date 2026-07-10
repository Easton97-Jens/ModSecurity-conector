#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH='' cd "$(dirname "$0")" && pwd)
CONNECTOR_DIR=$(CDPATH='' cd "$SCRIPT_DIR/.." && pwd)
REPO_ROOT=$(CDPATH='' cd "$CONNECTOR_DIR/../.." && pwd)
BUILD_ROOT=${BUILD_ROOT:-${XDG_STATE_HOME:-${HOME:-/tmp}/.local/state}/ModSecurity-conector-build}
OUT_DIR=$BUILD_ROOT/lighttpd-bridge-starter
CC_BIN=${CC:-cc}

case "$BUILD_ROOT" in
    /*) ;;
    *) echo "lighttpd_bridge_starter: BLOCKED: BUILD_ROOT must be absolute: $BUILD_ROOT"; exit 77 ;;
esac

case "$(CDPATH='' cd "$BUILD_ROOT" 2>/dev/null && pwd 2>/dev/null || printf '%s' "$BUILD_ROOT")" in
    "$REPO_ROOT"|"$REPO_ROOT"/*)
        echo "lighttpd_bridge_starter: BLOCKED: BUILD_ROOT must not be inside the checkout: $BUILD_ROOT"
        exit 77
        ;;
    *) ;;
esac

command -v "$CC_BIN" >/dev/null 2>&1 || {
    echo "lighttpd_bridge_starter: BLOCKED: missing C compiler: $CC_BIN"
    exit 77
}

mkdir -p "$OUT_DIR"

MSCONNECTOR_C_STD=${MSCONNECTOR_C_STD:-c17}

"$CC_BIN" -std="$MSCONNECTOR_C_STD" -Wall -Wextra -Werror \
    -I "$REPO_ROOT" \
    -I "$REPO_ROOT/common/include" \
    "$REPO_ROOT/common/src/capabilities.c" \
    "$REPO_ROOT/common/src/intervention.c" \
    "$REPO_ROOT/common/src/origin.c" \
    "$REPO_ROOT/common/src/status.c" \
    "$REPO_ROOT/common/src/transaction.c" \
    "$CONNECTOR_DIR/metadata.c" \
    "$CONNECTOR_DIR/src/lighttpd_bridge.c" \
    "$CONNECTOR_DIR/src/lighttpd_bridge_main.c" \
    -o "$OUT_DIR/lighttpd-bridge-starter"

printf 'lighttpd_bridge_starter_build: PASS output=%s\n' "$OUT_DIR/lighttpd-bridge-starter"
