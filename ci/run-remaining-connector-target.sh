#!/bin/sh
set -eu

connector=${1:?connector is required}
target=${2:?target is required}

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
CONNECTOR_ROOT=${CONNECTOR_ROOT:-$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)}
FRAMEWORK_ROOT=${FRAMEWORK_ROOT:-$CONNECTOR_ROOT/modules/ModSecurity-test-Framework}
VERIFIED_RUN_ROOT=${VERIFIED_RUN_ROOT:-${RUNNER_TEMP:-${TMPDIR:-/var/tmp}}/ModSecurity-conector-verified}
BUILD_ROOT=${BUILD_ROOT:-$VERIFIED_RUN_ROOT/build}
CONNECTOR_COMPONENT_CACHE=${CONNECTOR_COMPONENT_CACHE:-$VERIFIED_RUN_ROOT/component-cache}
runtime_env=$CONNECTOR_COMPONENT_CACHE/runtime-env.sh

export CONNECTOR_ROOT FRAMEWORK_ROOT VERIFIED_RUN_ROOT BUILD_ROOT CONNECTOR_COMPONENT_CACHE

case "${PYTHON:-python3}" in
    /*) ;;
    */*) PYTHON="$CONNECTOR_ROOT/${PYTHON}" ;;
    *) PYTHON=${PYTHON:-python3} ;;
esac
export PYTHON

[ -f "$FRAMEWORK_ROOT/ci/common.sh" ] || {
    echo "FAIL: framework common.sh is missing" >&2
    exit 1
}

# shellcheck disable=SC1090
. "$FRAMEWORK_ROOT/ci/common.sh"

load_runtime_env() {
    if [ -f "$runtime_env" ]; then
        # shellcheck disable=SC1090
        . "$runtime_env"
    fi
}

require_modsecurity_build_environment() {
    load_runtime_env
    if [ -f "${MODSECURITY_INCLUDE_DIR:-}/modsecurity/modsecurity.h" ] \
        && [ -d "${MODSECURITY_LIB_DIR:-}" ]; then
        return 0
    fi
    if [ "${SKIP_RUNTIME_COMPONENT_PREPARE:-0}" = "1" ]; then
        echo "FAIL: libmodsecurity build environment is missing and preparation is disabled" >&2
        return 1
    fi
    PYTHON=${PYTHON:-python3} FRAMEWORK_ROOT="$FRAMEWORK_ROOT" CONNECTOR_ROOT="$CONNECTOR_ROOT" \
        sh "$CONNECTOR_ROOT/ci/prepare-runtime-components.sh"
    load_runtime_env
    if [ ! -f "${MODSECURITY_INCLUDE_DIR:-}/modsecurity/modsecurity.h" ] \
        || [ ! -d "${MODSECURITY_LIB_DIR:-}" ]; then
        echo "FAIL: runtime preparation did not provide libmodsecurity headers and libraries" >&2
        return 1
    fi
}

require_host=0
case "$target" in
    start-smoke-*|runtime-smoke-*) require_host=1 ;;
esac

require_modsecurity_build_environment

case "$connector" in
    envoy)
        envoy_build_paths >/dev/null
        if [ "$require_host" = "1" ]; then
            ENVOY_BIN=$(require_or_provision_envoy)
            export ENVOY_BIN
        fi
        exec make -C "$CONNECTOR_ROOT/connectors/envoy" "$target" \
            BUILD_ROOT="$BUILD_ROOT" ENVOY_BIN="$ENVOY_BIN" \
            MODSECURITY_INCLUDE_DIR="$MODSECURITY_INCLUDE_DIR" \
            MODSECURITY_LIB_DIR="$MODSECURITY_LIB_DIR" \
            MODSECURITY_PREFIX="${MODSECURITY_PREFIX:-}"
        ;;
    traefik)
        traefik_build_paths >/dev/null
        if [ "$require_host" = "1" ]; then
            TRAEFIK_BIN=$(require_or_provision_traefik)
            export TRAEFIK_BIN
        fi
        exec make -C "$CONNECTOR_ROOT/connectors/traefik" "$target" \
            BUILD_ROOT="$BUILD_ROOT" TRAEFIK_BIN="$TRAEFIK_BIN" \
            MODSECURITY_INCLUDE_DIR="$MODSECURITY_INCLUDE_DIR" \
            MODSECURITY_LIB_DIR="$MODSECURITY_LIB_DIR" \
            MODSECURITY_PREFIX="${MODSECURITY_PREFIX:-}"
        ;;
    lighttpd)
        lighttpd_build_paths >/dev/null
        LIGHTTPD_BIN=$(require_or_provision_lighttpd)
        export LIGHTTPD_BIN LIGHTTPD_SOURCE_DIR LIGHTTPD_BUILD_ROOT
        export LIGHTTPD_INCLUDE_DIR LIGHTTPD_CONNECTOR_BUILD_ROOT LIGHTTPD_MODULE_DIR
        exec make -C "$CONNECTOR_ROOT/connectors/lighttpd" "$target" \
            BUILD_ROOT="$BUILD_ROOT" LIGHTTPD_BIN="$LIGHTTPD_BIN" \
            LIGHTTPD_SOURCE_DIR="$LIGHTTPD_SOURCE_DIR" \
            LIGHTTPD_BUILD_ROOT="$LIGHTTPD_BUILD_ROOT" \
            LIGHTTPD_INCLUDE_DIR="$LIGHTTPD_INCLUDE_DIR" \
            LIGHTTPD_CONNECTOR_BUILD_ROOT="$LIGHTTPD_CONNECTOR_BUILD_ROOT" \
            LIGHTTPD_MODULE_DIR="$LIGHTTPD_MODULE_DIR" \
            MODSECURITY_INCLUDE_DIR="$MODSECURITY_INCLUDE_DIR" \
            MODSECURITY_LIB_DIR="$MODSECURITY_LIB_DIR" \
            MODSECURITY_PREFIX="${MODSECURITY_PREFIX:-}"
        ;;
    *)
        echo "usage: $0 envoy|traefik|lighttpd target" >&2
        exit 2
        ;;
esac
