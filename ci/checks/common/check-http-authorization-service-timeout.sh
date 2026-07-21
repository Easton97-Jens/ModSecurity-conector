#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)
VERIFIED_RUN_ROOT="${VERIFIED_RUN_ROOT:-${RUNNER_TEMP:-${TMPDIR:-/var/tmp}}/ModSecurity-conector-verified}"
VERIFIED_BUILD_ROOT="${VERIFIED_BUILD_ROOT:-$VERIFIED_RUN_ROOT/build}"
BUILD_ROOT="${BUILD_ROOT:-$VERIFIED_BUILD_ROOT}"
CC_BIN="${CC:-cc}"
MSCONNECTOR_C_STD="${MSCONNECTOR_C_STD:-c17}"
MSCONNECTOR_CFLAGS="${MSCONNECTOR_CFLAGS:--std=$MSCONNECTOR_C_STD -Wall -Wextra -Werror}"
OUT_DIR="$BUILD_ROOT/http-authorization-service-timeout-smoke"
TEST_SOURCE="$REPO_ROOT/ci/checks/common/http_authorization_service_timeout_smoke.c"
TEST_BINARY="$OUT_DIR/http_authorization_service_timeout_smoke"

case "$BUILD_ROOT" in
    /*) ;;
    *) echo "http_authorization_service_timeout_smoke: BUILD_ROOT must be absolute" >&2; exit 77 ;;
esac
case "$(CDPATH= cd "$BUILD_ROOT" 2>/dev/null && pwd 2>/dev/null || printf '%s' "$BUILD_ROOT")" in
    "$REPO_ROOT"|"$REPO_ROOT"/*)
        echo "http_authorization_service_timeout_smoke: BUILD_ROOT must not be inside the checkout" >&2
        exit 77
        ;;
esac
if [ -L "$OUT_DIR" ]; then
    echo "http_authorization_service_timeout_smoke: output directory must not be a symlink" >&2
    exit 77
fi
command -v "$CC_BIN" >/dev/null 2>&1 || {
    echo "http_authorization_service_timeout_smoke: missing C compiler: $CC_BIN" >&2
    exit 77
}

mkdir -p "$OUT_DIR"
"$CC_BIN" $MSCONNECTOR_CFLAGS \
    -I "$REPO_ROOT" \
    -I "$REPO_ROOT/common/include" \
    -I "$REPO_ROOT/common/runtime" \
    "$TEST_SOURCE" \
    "$REPO_ROOT/common/runtime/http_authorization_service.c" \
    "$REPO_ROOT"/common/src/*.c \
    -o "$TEST_BINARY"
"$TEST_BINARY"

printf 'http_authorization_service_timeout_smoke: pass output=%s\n' "$OUT_DIR"
