#!/bin/sh
set -eu

# Exact-head hosted gate.  Runtime components are provisioned by the caller
# with pinned NGINX provenance; this wrapper exercises the same real harness
# twice, isolating the connector's on/off error-log directive.
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/../../.." && pwd)
FRAMEWORK_ROOT=${FRAMEWORK_ROOT:-$REPO_ROOT/modules/ModSecurity-test-Framework}
[ -d "$FRAMEWORK_ROOT" ] || { echo "nginx_exact_head: missing Framework" >&2; exit 77; }

BUILD_ROOT=${BUILD_ROOT:-${RUNNER_TEMP:-/tmp}/ModSecurity-conector-nginx-exact-head}
mkdir -p "$BUILD_ROOT"
RULE_PREAMBLE=${RULE_PREAMBLE:-$FRAMEWORK_ROOT/tests/rules/no-crs-baseline.conf}
[ -f "$RULE_PREAMBLE" ] || { echo "nginx_exact_head: missing pinned no-CRS rules" >&2; exit 77; }

for mode in on off; do
    mode_root="$BUILD_ROOT/$mode"
    mkdir -p "$mode_root"
    echo "nginx_exact_head: mode=$mode"
    NGINX_USE_ERROR_LOG="$mode" \
    VERIFIED_RUN_ROOT="$mode_root" \
    BUILD_ROOT="$mode_root/build" \
    LOG_ROOT="$mode_root/logs" \
    RESULTS_DIR="$mode_root/results" \
    NGINX_HARNESS_PARENT="$mode_root/harness" \
    MODSECURITY_TEST_VARIANT=no-crs \
    NO_CRS_BASELINE=1 \
    MODSECURITY_RULE_PREAMBLE_FILE="$RULE_PREAMBLE" \
    FORCE_ALL_CASES=1 \
    TEST_CASE=phase1_header_block \
    RUN_ONE_CASE=1 \
    CASE_SCOPE=all \
    sh "$SCRIPT_DIR/run_nginx_smoke.sh"

    error_log=$(find "$mode_root" -type f -name error.log -print -quit)
    [ -n "$error_log" ] || { echo "nginx_exact_head: no error log for mode=$mode" >&2; exit 1; }
    if [ "$mode" = on ]; then
        grep -Eq '949110' "$error_log" || {
            echo "nginx_exact_head: intervention marker absent with error-log on" >&2
            exit 1
        }
    else
        if grep -Eq '949110' "$error_log"; then
            echo "nginx_exact_head: intervention marker leaked with error-log off" >&2
            exit 1
        fi
    fi
    echo "nginx_exact_head: mode=$mode runtime=passed"
done
