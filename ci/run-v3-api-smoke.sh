#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
SMOKE_DIR="$REPO_ROOT/src/v3-api-smoke"

MODSECURITY_V3_DIR="${MODSECURITY_V3_DIR:-/root/conecter/ModSecurity_V3}"
BUILD_DIR="${BUILD_DIR:-build/v3-api-smoke}"
CC="${CC:-cc}"
CXX="${CXX:-c++}"

export MODSECURITY_V3_DIR BUILD_DIR CC CXX

set +e
sh "$SCRIPT_DIR/check-v3-api-smoke-prereqs.sh"
rc=$?
set -e
if [ "$rc" -ne 0 ]; then
    exit "$rc"
fi

make -C "$SMOKE_DIR" run \
    MODSECURITY_V3_DIR="$MODSECURITY_V3_DIR" \
    BUILD_DIR="$BUILD_DIR" \
    CC="$CC" \
    CXX="$CXX"
