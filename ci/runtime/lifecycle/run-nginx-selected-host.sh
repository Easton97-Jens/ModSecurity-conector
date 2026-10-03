#!/bin/sh
# Configuration-only invocations supplement, never replace, real HTTP cases.
set -eu

SCRIPT_DIR=$(CDPATH='' cd "$(dirname "$0")" && pwd)
: "${FRAMEWORK_ROOT:?FRAMEWORK_ROOT is required}"
host_rc=0
sh "$FRAMEWORK_ROOT/ci/runtime/run-nginx-smoke.sh" || host_rc=$?
config_rc=0
"${PYTHON:-python3}" "$SCRIPT_DIR/run-selected-nginx-configtests.py" || config_rc=$?
if [ "$host_rc" -ne 0 ]; then
    exit "$host_rc"
fi
exit "$config_rc"
