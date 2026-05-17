#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
PYTHON_BIN="${PYTHON:-python3}"

"$PYTHON_BIN" "$REPO_ROOT/ci/adapter_metadata.py" check-drift
