#!/bin/sh
set -eu

connector=${1:?connector is required}
stage=${2:?stage is required}

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
CONNECTOR_ROOT=${CONNECTOR_ROOT:-$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)}
FRAMEWORK_ROOT=${FRAMEWORK_ROOT:-$CONNECTOR_ROOT/modules/ModSecurity-test-Framework}
VERIFIED_RUN_ROOT=${VERIFIED_RUN_ROOT:-${RUNNER_TEMP:-${TMPDIR:-/var/tmp}}/ModSecurity-conector-verified}
BUILD_ROOT=${BUILD_ROOT:-$VERIFIED_RUN_ROOT/build}
CACHE_ROOT=${CACHE_ROOT:-$VERIFIED_RUN_ROOT/cache-v2}
VERIFIED_COMPONENT_CACHE=${VERIFIED_COMPONENT_CACHE:-$CACHE_ROOT/shared}
CONNECTOR_COMPONENT_CACHE=${CONNECTOR_COMPONENT_CACHE:-$VERIFIED_COMPONENT_CACHE}
TMP_ROOT=${TMP_ROOT:-$BUILD_ROOT/tmp}
LOG_ROOT=${LOG_ROOT:-$BUILD_ROOT/logs}
RESULTS_DIR=${RESULTS_DIR:-$BUILD_ROOT/stages/$connector/$stage/results}
RUNTIME_REPORT_OUTPUT_ROOT=${RUNTIME_REPORT_OUTPUT_ROOT:-$BUILD_ROOT/runtime-component-reports}
PYTHON=${PYTHON:-python3}
NO_CRS_ARTIFACT_PROFILE=${NO_CRS_ARTIFACT_PROFILE:-generic}
FULL_LIFECYCLE_HOST_PROFILE=${FULL_LIFECYCLE_HOST_PROFILE:-}
FULL_LIFECYCLE_EXECUTED_TARGET=${FULL_LIFECYCLE_EXECUTED_TARGET:-}

case "$connector" in
    apache|nginx|haproxy|envoy|traefik|lighttpd) ;;
    *) echo "usage: $0 apache|nginx|haproxy|envoy|traefik|lighttpd build|config_load|start_smoke|minimal_runtime_smoke|no_crs_baseline" >&2; exit 2 ;;
esac
case "$stage" in
    build|config_load|start_smoke|minimal_runtime_smoke|no_crs_baseline) ;;
    *) echo "usage: $0 apache|nginx|haproxy|envoy|traefik|lighttpd build|config_load|start_smoke|minimal_runtime_smoke|no_crs_baseline" >&2; exit 2 ;;
esac

expected_full_lifecycle_profile() {
    case "$1" in
        apache) printf '%s\n' native-httpd-module ;;
        nginx) printf '%s\n' native-nginx-http-module ;;
        haproxy) printf '%s\n' native-htx-filter ;;
        envoy) printf '%s\n' ext_proc ;;
        traefik) printf '%s\n' native-middleware ;;
        lighttpd) printf '%s\n' patched-native ;;
    esac
}

expected_full_lifecycle_target() {
    case "$1" in
        apache) printf '%s\n' full-lifecycle-apache ;;
        nginx) printf '%s\n' full-lifecycle-nginx ;;
        haproxy) printf '%s\n' full-lifecycle-haproxy-htx ;;
        envoy) printf '%s\n' full-lifecycle-envoy-ext-proc ;;
        traefik) printf '%s\n' full-lifecycle-traefik-native ;;
        lighttpd) printf '%s\n' full-lifecycle-lighttpd-patched ;;
    esac
}

# Full-lifecycle evidence may never fall through to a request-only or stock
# compatibility runner.  Apache and NGINX already have their selected native
# canonical drivers; the other native profiles remain explicitly BLOCKED until
# their own capability-selected canonical drivers exist.
if [ "$stage" = no_crs_baseline ] && [ "$NO_CRS_ARTIFACT_PROFILE" = full_lifecycle ]; then
    expected_profile=$(expected_full_lifecycle_profile "$connector")
    expected_target=$(expected_full_lifecycle_target "$connector")
    if [ "$FULL_LIFECYCLE_HOST_PROFILE" != "$expected_profile" ] || \
       [ "$FULL_LIFECYCLE_EXECUTED_TARGET" != "$expected_target" ]; then
        echo "FAIL: full-lifecycle stage profile/target mismatch for $connector" >&2
        exit 1
    fi
    case "$connector" in
        apache|nginx) ;;
        haproxy)
            echo "BLOCKED: native HTX is observer-only; the compatibility SPOE/SPOP runner is forbidden for full-lifecycle evidence" >&2
            exit 77
            ;;
        envoy)
            echo "BLOCKED: ext_proc has no Common/libmodsecurity canonical driver; ext_authz compatibility is forbidden for full-lifecycle evidence" >&2
            exit 77
            ;;
        traefik)
            echo "BLOCKED: native Traefik middleware is not registered in a pinned host run; forwardAuth compatibility is forbidden for full-lifecycle evidence" >&2
            exit 77
            ;;
        lighttpd)
            echo "BLOCKED: patched lighttpd has no body-capable canonical lifecycle driver; stock compatibility is forbidden for full-lifecycle evidence" >&2
            exit 77
            ;;
    esac
fi

[ -f "$FRAMEWORK_ROOT/ci/common.sh" ] || {
    echo "BLOCKED: framework common.sh is missing: $FRAMEWORK_ROOT/ci/common.sh" >&2
    exit 77
}

case "$BUILD_ROOT" in
    /*) ;;
    *) echo "BLOCKED: BUILD_ROOT must be absolute: $BUILD_ROOT" >&2; exit 77 ;;
esac
case "$BUILD_ROOT" in
    "$CONNECTOR_ROOT"|"$CONNECTOR_ROOT"/*)
        echo "BLOCKED: BUILD_ROOT must be outside the checkout: $BUILD_ROOT" >&2
        exit 77
        ;;
esac

export CONNECTOR_ROOT FRAMEWORK_ROOT VERIFIED_RUN_ROOT BUILD_ROOT CACHE_ROOT VERIFIED_COMPONENT_CACHE CONNECTOR_COMPONENT_CACHE TMP_ROOT LOG_ROOT RESULTS_DIR
export RUNTIME_REPORT_OUTPUT_ROOT RUNTIME_ROOT RUNTIME_BASE PYTHON RUNTIME_COMPONENT_ENV_SNAPSHOT
case "$connector" in
    apache|nginx|haproxy) RUNTIME_COMPONENT_TARGET=$connector ;;
    envoy|traefik|lighttpd) RUNTIME_COMPONENT_TARGET=shared ;;
esac
export RUNTIME_COMPONENT_TARGET

run_framework_host() {
    framework_script=$1
    smoke_stage=$2
    shift 2
    exec "$CONNECTOR_ROOT/ci/with-runtime-components.sh" env \
        CONNECTOR_ROOT="$CONNECTOR_ROOT" \
        FRAMEWORK_ROOT="$FRAMEWORK_ROOT" \
        VERIFIED_RUN_ROOT="$VERIFIED_RUN_ROOT" \
        VERIFIED_COMPONENT_CACHE="$VERIFIED_COMPONENT_CACHE" \
        CACHE_ROOT="$CACHE_ROOT" \
        CONNECTOR_COMPONENT_CACHE="$CONNECTOR_COMPONENT_CACHE" \
        BUILD_ROOT="$BUILD_ROOT" \
        TMP_ROOT="$TMP_ROOT" \
        LOG_ROOT="$LOG_ROOT" \
        RESULTS_DIR="$RESULTS_DIR" \
        RUNTIME_REPORT_OUTPUT_ROOT="$RUNTIME_REPORT_OUTPUT_ROOT" \
        RUNTIME_COMPONENT_TARGET="$RUNTIME_COMPONENT_TARGET" \
        RUNTIME_COMPONENT_ENV_SNAPSHOT="${RUNTIME_COMPONENT_ENV_SNAPSHOT:-}" \
        NO_CRS_BASELINE=1 \
        NO_CRS_SELECTED_CASE_IDS="${NO_CRS_SELECTED_CASE_IDS:-}" \
        MODSECURITY_TEST_VARIANT=no-crs \
        MODSECURITY_MRTS_VARIANT=no-mrts \
        MODSECURITY_RULE_PREAMBLE_FILE="${NO_CRS_RULES_FILE:-}" \
        MSCONNECTOR_SMOKE_STAGE="$smoke_stage" \
        "$@" sh "$FRAMEWORK_ROOT/ci/$framework_script"
}

run_remaining_connector() {
    target=$1
    exec env \
        CONNECTOR_ROOT="$CONNECTOR_ROOT" \
        FRAMEWORK_ROOT="$FRAMEWORK_ROOT" \
        VERIFIED_RUN_ROOT="$VERIFIED_RUN_ROOT" \
        VERIFIED_COMPONENT_CACHE="$VERIFIED_COMPONENT_CACHE" \
        CACHE_ROOT="$CACHE_ROOT" \
        CONNECTOR_COMPONENT_CACHE="$CONNECTOR_COMPONENT_CACHE" \
        BUILD_ROOT="$BUILD_ROOT" \
        TMP_ROOT="$TMP_ROOT" \
        LOG_ROOT="$LOG_ROOT" \
        RESULTS_DIR="$RESULTS_DIR" \
        RUNTIME_ROOT="${RUNTIME_ROOT:-$BUILD_ROOT/runtime}" \
        RUNTIME_BASE="${RUNTIME_BASE:-$BUILD_ROOT/runtime}" \
        RUNTIME_REPORT_OUTPUT_ROOT="$RUNTIME_REPORT_OUTPUT_ROOT" \
        RUNTIME_COMPONENT_TARGET="$RUNTIME_COMPONENT_TARGET" \
        RUNTIME_COMPONENT_ENV_SNAPSHOT="${RUNTIME_COMPONENT_ENV_SNAPSHOT:-}" \
        sh "$CONNECTOR_ROOT/ci/run-remaining-connector-target.sh" "$connector" "$target"
}

case "$connector:$stage" in
    apache:build)
        run_framework_host run-apache-smoke.sh build
        ;;
    nginx:build)
        run_framework_host run-nginx-smoke.sh build
        ;;
    haproxy:build)
        exec "$CONNECTOR_ROOT/ci/with-runtime-components.sh" sh -eu -c '
            sh "$FRAMEWORK_ROOT/ci/prepare-haproxy-runtime.sh"
            make -C "$CONNECTOR_ROOT/connectors/haproxy" build-modsecurity-binding build-spoa-runtime \
                BUILD_ROOT="$BUILD_ROOT" REPO_ROOT="$CONNECTOR_ROOT"
        '
        ;;
    apache:config_load|nginx:config_load|haproxy:config_load)
        run_framework_host "run-$connector-smoke.sh" config_load \
            RUN_ONE_CASE=1 TEST_CASE=allow_without_marker
        ;;
    apache:start_smoke|nginx:start_smoke|haproxy:start_smoke)
        run_framework_host "run-$connector-smoke.sh" start_smoke \
            RUN_ONE_CASE=1 TEST_CASE=allow_without_marker
        ;;
    apache:minimal_runtime_smoke|nginx:minimal_runtime_smoke|haproxy:minimal_runtime_smoke)
        run_framework_host "run-$connector-smoke.sh" minimal_runtime_smoke \
            RUN_ONE_CASE=0 SMOKE_CASES="allow_without_marker deny_header_marker_403"
        ;;
    apache:no_crs_baseline|nginx:no_crs_baseline|haproxy:no_crs_baseline)
        [ -n "${NO_CRS_SELECTED_CASES:-}" ] || {
            echo "FAIL: capability-selected No-CRS runner cases are missing" >&2
            exit 1
        }
        run_framework_host "run-$connector-smoke.sh" minimal_runtime_smoke \
            RUN_ONE_CASE=0 SMOKE_CASES="$NO_CRS_SELECTED_CASES"
        ;;
    envoy:build)
        run_remaining_connector build-envoy-connector
        ;;
    traefik:build)
        run_remaining_connector build-traefik-connector
        ;;
    lighttpd:build)
        run_remaining_connector build-lighttpd-connector
        ;;
    envoy:config_load)
        run_remaining_connector check-envoy-config
        ;;
    traefik:config_load)
        run_remaining_connector check-traefik-config
        ;;
    lighttpd:config_load)
        run_remaining_connector check-lighttpd-config
        ;;
    envoy:start_smoke)
        run_remaining_connector start-smoke-envoy
        ;;
    traefik:start_smoke)
        run_remaining_connector start-smoke-traefik
        ;;
    lighttpd:start_smoke)
        run_remaining_connector start-smoke-lighttpd
        ;;
    envoy:minimal_runtime_smoke)
        run_remaining_connector runtime-smoke-envoy
        ;;
    traefik:minimal_runtime_smoke)
        run_remaining_connector runtime-smoke-traefik
        ;;
    lighttpd:minimal_runtime_smoke)
        run_remaining_connector runtime-smoke-lighttpd
        ;;
    envoy:no_crs_baseline|traefik:no_crs_baseline|lighttpd:no_crs_baseline)
        [ -n "${NO_CRS_SELECTED_CASES:-}" ] || {
            echo "FAIL: capability-selected No-CRS runner cases are missing" >&2
            exit 1
        }
        # These targets consume the plan before delegating to their narrow
        # real-host probes.  They are deliberately distinct from the legacy
        # minimal-runtime targets: remaining selected cases stay explicit in
        # canonical evidence instead of being implied by a 200/403 smoke.
        run_remaining_connector "no-crs-baseline-$connector"
        ;;
esac
