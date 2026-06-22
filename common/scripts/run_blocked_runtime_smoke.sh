#!/bin/sh
set -eu

CONNECTOR_NAME=${1:?connector name is required}
INTEGRATION_MODE=${2:?integration mode is required}
BINARY_ENV_VAR=${3:?runtime binary environment variable is required}
BINARY_NAME=${4:?runtime binary name is required}
MISSING_BINARY_REASON=${5:?missing binary skipped reason is required}
POST_LOOKUP_BLOCKED_REASON=${6:?post lookup skipped reason is required}
POST_LOOKUP_MISSING_DEPENDENCY=${7:?post lookup missing dependency is required}
ARCHITECTURE_DECISION=${8:-}
INTEGRATION_MODE_SELECTED=${9:-1}

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
DEFAULT_CONNECTOR_ROOT=$(CDPATH= cd "$SCRIPT_DIR/../.." && pwd)
CONNECTOR_ROOT="${CONNECTOR_ROOT:-$DEFAULT_CONNECTOR_ROOT}"
CONNECTOR_ROOT=$(CDPATH= cd "$CONNECTOR_ROOT" && pwd)
FRAMEWORK_ROOT="${FRAMEWORK_ROOT:-$CONNECTOR_ROOT/modules/ModSecurity-test-Framework}"
CONNECTOR_DIR="$CONNECTOR_ROOT/connectors/$CONNECTOR_NAME"
HARNESS_PATH="${HARNESS_PATH:-$CONNECTOR_DIR/harness/run_${CONNECTOR_NAME}_smoke.sh}"
CONNECTOR_SMOKE_SCRIPT_DIR="$FRAMEWORK_ROOT/ci"

export CONNECTOR_ROOT FRAMEWORK_ROOT HARNESS_PATH CONNECTOR_SMOKE_SCRIPT_DIR

. "$FRAMEWORK_ROOT/ci/connector-smoke-common.sh"

[ -d "$CONNECTOR_DIR" ] || connector_skip_missing_dependency \
    "$CONNECTOR_NAME" \
    "$INTEGRATION_MODE" \
    "connector directory missing" \
    "$CONNECTOR_NAME" \
    "$ARCHITECTURE_DECISION"

runtime_binary=""
runtime_missing_dependency=""
if runtime_binary=$(find_runtime_binary "$BINARY_ENV_VAR" "$BINARY_NAME"); then
    :
else
    runtime_missing_dependency="$BINARY_NAME"
fi

if [ "$INTEGRATION_MODE_SELECTED" != "1" ]; then
    if [ -z "$runtime_missing_dependency" ]; then
        runtime_missing_dependency="$POST_LOOKUP_MISSING_DEPENDENCY"
    fi
    connector_skip_missing_dependency \
        "$CONNECTOR_NAME" \
        "$INTEGRATION_MODE" \
        "$POST_LOOKUP_BLOCKED_REASON" \
        "$runtime_missing_dependency" \
        "$ARCHITECTURE_DECISION"
fi

if [ -z "$runtime_binary" ]; then
    connector_skip_missing_dependency \
        "$CONNECTOR_NAME" \
        "$INTEGRATION_MODE" \
        "$MISSING_BINARY_REASON" \
        "$BINARY_NAME" \
        "$ARCHITECTURE_DECISION"
fi

connector_skip_missing_dependency \
    "$CONNECTOR_NAME" \
    "$INTEGRATION_MODE" \
    "$POST_LOOKUP_BLOCKED_REASON" \
    "$POST_LOOKUP_MISSING_DEPENDENCY" \
    "$ARCHITECTURE_DECISION"
