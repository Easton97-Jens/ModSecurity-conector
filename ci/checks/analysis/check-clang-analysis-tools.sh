#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PYTHON_BIN=${PYTHON:-python3}

command -v "$PYTHON_BIN" >/dev/null 2>&1 || {
    echo "BLOCKED: Python interpreter is unavailable: $PYTHON_BIN" >&2
    exit 77
}

exec "$PYTHON_BIN" "$SCRIPT_DIR/clang_analysis_baseline.py" \
    --check-tools \
    --clang-tidy "${CLANG_TIDY:-clang-tidy}" \
    --clang "${CLANG:-clang}" \
    --clangxx "${CLANGXX:-clang++}"
