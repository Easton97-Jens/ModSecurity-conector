#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
FRAMEWORK_ROOT="${FRAMEWORK_ROOT:-$REPO_ROOT/modules/ModSecurity-test-Framework}"
[ -d "$FRAMEWORK_ROOT" ] || { echo "adapter_helper_smoke: missing FRAMEWORK_ROOT; run git submodule update --init --recursive or set FRAMEWORK_ROOT=/path/to/ModSecurity-test-Framework"; exit 77; }
VERIFIED_RUN_ROOT="${VERIFIED_RUN_ROOT:-${RUNNER_TEMP:-${TMPDIR:-/var/tmp}}/ModSecurity-conector-verified}"
VERIFIED_BUILD_ROOT="${VERIFIED_BUILD_ROOT:-$VERIFIED_RUN_ROOT/build}"
BUILD_ROOT="${BUILD_ROOT:-$VERIFIED_BUILD_ROOT}"

CC_BIN="${CC:-cc}"
PYTHON_BIN="${PYTHON_BIN:-${PYTHON:-$(if [ -x "$REPO_ROOT/.venv/bin/python" ]; then printf '%s' "$REPO_ROOT/.venv/bin/python"; else printf '%s' python3; fi)}}"
OUT_DIR="$BUILD_ROOT/adapter-helper-smoke"
SMOKE_C="$OUT_DIR/adapter_helper_smoke.c"
SMOKE_BIN="$OUT_DIR/adapter_helper_smoke"

case "$BUILD_ROOT" in
    /*) ;;
    *) echo "adapter_helper_smoke: BUILD_ROOT must be absolute: $BUILD_ROOT"; exit 77 ;;
esac

case "$(CDPATH= cd "$BUILD_ROOT" 2>/dev/null && pwd 2>/dev/null || printf '%s' "$BUILD_ROOT")" in
    "$REPO_ROOT"|"$REPO_ROOT"/*)
        echo "adapter_helper_smoke: BUILD_ROOT must not be inside the checkout: $BUILD_ROOT"
        exit 77
        ;;
esac

command -v "$CC_BIN" >/dev/null 2>&1 || {
    echo "adapter_helper_smoke: missing C compiler: $CC_BIN"
    exit 77
}

mkdir -p "$OUT_DIR"
CONNECTOR_ROOT="$REPO_ROOT" "$PYTHON_BIN" "$FRAMEWORK_ROOT/ci/adapter_metadata.py" c-smoke > "$SMOKE_C"

"$CC_BIN" -std=c99 -Wall -Wextra -Werror \
    -I "$REPO_ROOT" \
    -I "$REPO_ROOT/common/include" \
    "$REPO_ROOT/common/src/origin.c" \
    "$REPO_ROOT/connectors/apache/metadata.c" \
    "$REPO_ROOT/connectors/nginx/metadata.c" \
    "$SMOKE_C" \
    -o "$SMOKE_BIN"

"$SMOKE_BIN"
echo "adapter_helper_smoke: pass output=$OUT_DIR"
