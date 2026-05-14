#!/bin/sh
set -eu

MODSECURITY_V3_DIR="${MODSECURITY_V3_DIR:-/root/conecter/ModSecurity_V3}"
BUILD_DIR="${BUILD_DIR:-${TMPDIR:-/tmp}/modsecurity-conector-v3-api-smoke}"
SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
SOURCE_FILE="$REPO_ROOT/tests/common/v3-api-smoke/v3_api_smoke.c"
HEADER_FILE="$MODSECURITY_V3_DIR/headers/modsecurity/modsecurity.h"
LIB_FILE="$MODSECURITY_V3_DIR/src/.libs/libmodsecurity.so"
OUTPUT_FILE="$BUILD_DIR/v3_api_smoke"

if [ ! -f "$HEADER_FILE" ]; then
    echo "v3_api_smoke: blocked missing header: $HEADER_FILE" >&2
    exit 77
fi

if [ ! -f "$LIB_FILE" ]; then
    echo "v3_api_smoke: blocked missing library: $LIB_FILE" >&2
    echo "v3_api_smoke: not building ModSecurity_V3 from this script" >&2
    exit 77
fi

mkdir -p "$BUILD_DIR"

cc -std=c99 -Wall -Wextra -Werror \
    -I"$MODSECURITY_V3_DIR/headers" \
    -c "$SOURCE_FILE" \
    -o "$BUILD_DIR/v3_api_smoke.o"

c++ "$BUILD_DIR/v3_api_smoke.o" \
    -L"$MODSECURITY_V3_DIR/src/.libs" \
    -Wl,-rpath,"$MODSECURITY_V3_DIR/src/.libs" \
    -lmodsecurity \
    -o "$OUTPUT_FILE"

"$OUTPUT_FILE"
