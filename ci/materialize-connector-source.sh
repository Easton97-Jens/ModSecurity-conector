#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
. "$SCRIPT_DIR/common.sh"

PYTHON_BIN="${PYTHON_BIN:-$(ci_python)}"

exec "$PYTHON_BIN" "$SCRIPT_DIR/materialize-connector-source.py" "$@"
