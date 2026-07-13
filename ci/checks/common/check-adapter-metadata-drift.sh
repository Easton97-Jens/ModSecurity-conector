#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)
FRAMEWORK_ROOT="${FRAMEWORK_ROOT:-$REPO_ROOT/modules/ModSecurity-test-Framework}"
[ -d "$FRAMEWORK_ROOT" ] || { echo "adapter_metadata_drift: missing FRAMEWORK_ROOT; run git submodule update --init --recursive or set FRAMEWORK_ROOT=/path/to/ModSecurity-test-Framework"; exit 77; }

PYTHON_BIN="${PYTHON_BIN:-${PYTHON:-$(if [ -x "$REPO_ROOT/.venv/bin/python" ]; then printf '%s' "$REPO_ROOT/.venv/bin/python"; else printf '%s' python3; fi)}}"

FRAMEWORK_ROOT="$FRAMEWORK_ROOT" CONNECTOR_ROOT="$REPO_ROOT" "$PYTHON_BIN" "$FRAMEWORK_ROOT/ci/lib/adapter_metadata.py" check-drift
