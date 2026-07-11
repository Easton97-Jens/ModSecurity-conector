#!/bin/sh
# Exercise the Apache/NGINX native module through a real reverse-proxy path
# while the Framework's upstream daemon is paused after its first chunk.
set -eu

connector=${1:?connector is required}
SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
CONNECTOR_ROOT=${CONNECTOR_ROOT:-$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)}
FRAMEWORK_ROOT=${FRAMEWORK_ROOT:-$CONNECTOR_ROOT/modules/ModSecurity-test-Framework}
PYTHON=${PYTHON:-python3}
BUILD_ROOT=${BUILD_ROOT:?BUILD_ROOT is required}
RESULTS_DIR=${RESULTS_DIR:?RESULTS_DIR is required}
HOST_RUNTIME_ROOT=${HOST_RUNTIME_ROOT:?HOST_RUNTIME_ROOT is required}
HOST_LOG_ROOT=${HOST_LOG_ROOT:?HOST_LOG_ROOT is required}
NO_CRS_RULES_FILE=${NO_CRS_RULES_FILE:?NO_CRS_RULES_FILE is required}
FULL_LIFECYCLE_EVIDENCE_OUTPUT=${FULL_LIFECYCLE_EVIDENCE_OUTPUT:?FULL_LIFECYCLE_EVIDENCE_OUTPUT is required}

case "$connector" in
    apache)
        harness=$CONNECTOR_ROOT/connectors/apache/harness/run_apache_smoke.sh
        port=${FULL_LIFECYCLE_APACHE_PORT:-19280}
        ;;
    nginx)
        harness=$CONNECTOR_ROOT/connectors/nginx/harness/run_nginx_smoke.sh
        port=${FULL_LIFECYCLE_NGINX_PORT:-19281}
        ;;
    *) echo "usage: $0 apache|nginx" >&2; exit 2 ;;
esac

[ -f "$harness" ] || { echo "BLOCKED: native harness is missing: $harness" >&2; exit 77; }
[ -f "$FRAMEWORK_ROOT/tests/runners/synchronized_upstream.py" ] || {
    echo "BLOCKED: synchronized upstream helper is missing" >&2
    exit 77
}

runtime_root=$HOST_RUNTIME_ROOT/first-byte-$connector
log_root=$HOST_LOG_ROOT/$connector-first-byte
results_output=$RESULTS_DIR/$connector-first-byte-results.jsonl
mkdir -p "$RESULTS_DIR" "$HOST_RUNTIME_ROOT" "$HOST_LOG_ROOT"

set +e
RUNTIME_COMPONENT_TARGET=$connector \
CONNECTOR_ROOT="$CONNECTOR_ROOT" \
FRAMEWORK_ROOT="$FRAMEWORK_ROOT" \
BUILD_ROOT="$BUILD_ROOT" \
FULL_LIFECYCLE_EVIDENCE_OUTPUT="$FULL_LIFECYCLE_EVIDENCE_OUTPUT" \
NO_CRS_RULES_FILE="$NO_CRS_RULES_FILE" \
"$CONNECTOR_ROOT/ci/with-runtime-components.sh" env \
    RUN_ONE_CASE=1 \
    TEST_CASE="$FRAMEWORK_ROOT/tests/cases/no-crs-baseline/allow_without_marker.yaml" \
    CASE_SCOPE=all \
    MSCONNECTOR_SMOKE_STAGE=minimal_runtime_smoke \
    MSCONNECTOR_FULL_LIFECYCLE_SYNC=1 \
    NO_CRS_BASELINE=1 \
    MODSECURITY_TEST_VARIANT=no-crs \
    MODSECURITY_RULE_PREAMBLE_FILE="$NO_CRS_RULES_FILE" \
    RESULTS_DIR="$RESULTS_DIR" \
    RUNTIME_ROOT="$runtime_root" \
    RUNTIME_BASE="$HOST_RUNTIME_ROOT" \
    LOG_DIR="$log_root" \
    PORT="$port" \
    NGINX_HARNESS_PARENT="$HOST_RUNTIME_ROOT" \
    NGINX_HARNESS_WORK_ROOT="$HOST_RUNTIME_ROOT/nginx-harness" \
    "$harness"
rc=$?
set -e
if [ "$rc" -ne 0 ]; then
    exit "$rc"
fi

phase4_log=$log_root/phase4.log
[ -s "$phase4_log" ] || {
    echo "FAIL: native first-byte run completed without a Phase-4 event: $phase4_log" >&2
    exit 1
}
[ -f "$FULL_LIFECYCLE_EVIDENCE_OUTPUT" ] || {
    echo "FAIL: native first-byte run completed without barrier evidence" >&2
    exit 1
}
"$PYTHON" "$CONNECTOR_ROOT/ci/write-first-byte-source-results.py" \
    --connector "$connector" \
    --phase4-log "$phase4_log" \
    --first-byte-evidence "$FULL_LIFECYCLE_EVIDENCE_OUTPUT" \
    --output "$results_output"
printf 'native_first_byte_connector=%s\n' "$connector"
printf 'native_first_byte_phase4_log=%s\n' "$phase4_log"
printf 'native_first_byte_evidence=%s\n' "$FULL_LIFECYCLE_EVIDENCE_OUTPUT"
printf 'native_first_byte_results=%s\n' "$results_output"
