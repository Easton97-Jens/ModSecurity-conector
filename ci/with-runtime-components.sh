#!/bin/sh
set -eu

CONNECTOR_ROOT="${CONNECTOR_ROOT:-$(CDPATH= cd "$(dirname "$0")/.." && pwd)}"
FRAMEWORK_ROOT="${FRAMEWORK_ROOT:-$CONNECTOR_ROOT/modules/ModSecurity-test-Framework}"
DEFAULT_STATE_HOME="${DEFAULT_STATE_HOME:-${XDG_STATE_HOME:-${HOME:-/tmp}/.local/state}}"
BUILD_ROOT="${BUILD_ROOT:-$DEFAULT_STATE_HOME/ModSecurity-conector-build}"

if [ -z "${CONNECTOR_COMPONENT_CACHE:-}" ]; then
    if [ -d /src ] && [ -w /src ]; then
        CONNECTOR_COMPONENT_CACHE=/src/ModSecurity-conector-cache
    else
        CONNECTOR_COMPONENT_CACHE="${XDG_CACHE_HOME:-${HOME:-/tmp}/.cache}/ModSecurity-conector"
    fi
fi
export CONNECTOR_ROOT FRAMEWORK_ROOT BUILD_ROOT CONNECTOR_COMPONENT_CACHE

if [ "${SKIP_RUNTIME_COMPONENT_PREPARE:-0}" != "1" ]; then
    sh "$CONNECTOR_ROOT/ci/prepare-runtime-components.sh"
fi
SKIP_RUNTIME_COMPONENT_PREPARE=1
export SKIP_RUNTIME_COMPONENT_PREPARE

runtime_env="$CONNECTOR_COMPONENT_CACHE/runtime-env.sh"
if [ -f "$runtime_env" ]; then
    # shellcheck disable=SC1090
    . "$runtime_env"
fi

exec "$@"
