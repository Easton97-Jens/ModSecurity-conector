#!/bin/sh
set -eu

connector=${1:?connector is required}
evidence_stage=${2:-no_crs_baseline}
SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
CONNECTOR_ROOT=${CONNECTOR_ROOT:-$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)}
FRAMEWORK_ROOT=${FRAMEWORK_ROOT:-$CONNECTOR_ROOT/modules/ModSecurity-test-Framework}
PYTHON=${PYTHON:-python3}
VERIFIED_RUN_ROOT=${VERIFIED_RUN_ROOT:-${RUNNER_TEMP:-${TMPDIR:-/var/tmp}}/ModSecurity-conector-verified}
# Keep the invocation-level root distinct from the connector-local raw run.
# The resolver intentionally places build/, runs/, and run-logs/ beside one
# another. Framework host checks may need to see all three as safe runtime
# descendants, so passing only CONNECTOR_RUN_ROOT would incorrectly reject the
# sibling connector build root.
CANONICAL_VERIFIED_RUN_ROOT=$VERIFIED_RUN_ROOT
BUILD_ROOT=${BUILD_ROOT:-$VERIFIED_RUN_ROOT/build}
VERIFIED_EVIDENCE_ROOT=${VERIFIED_EVIDENCE_ROOT:-$VERIFIED_RUN_ROOT/evidence}
EVIDENCE_ROOT=${EVIDENCE_ROOT:-$VERIFIED_EVIDENCE_ROOT/no-crs-evidence}
RUNTIME_RUN_ROOT=${RUNTIME_RUN_ROOT:-$VERIFIED_RUN_ROOT/runs}
RUNTIME_LOG_ROOT=${RUNTIME_LOG_ROOT:-$VERIFIED_RUN_ROOT/run-logs}
CACHE_ROOT=${CACHE_ROOT:-$VERIFIED_RUN_ROOT/cache-v2}
NO_CRS_RUN_ID=${NO_CRS_RUN_ID:-$(date -u +%Y-%m-%dT%H-%M-%SZ)-$(git -C "$CONNECTOR_ROOT" rev-parse --short=8 HEAD 2>/dev/null || printf unknown)}
NO_CRS_RULES_FILE=${NO_CRS_RULES_FILE:-$FRAMEWORK_ROOT/tests/rules/no-crs-baseline.conf}
NO_CRS_ARTIFACT_PROFILE=${NO_CRS_ARTIFACT_PROFILE:-generic}
NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR=${NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR:-}
NO_CRS_PROTOCOL_CLIENT=${NO_CRS_PROTOCOL_CLIENT:-0}
FULL_LIFECYCLE_HOST_PROFILE=${FULL_LIFECYCLE_HOST_PROFILE:-}
FULL_LIFECYCLE_EXECUTED_TARGET=${FULL_LIFECYCLE_EXECUTED_TARGET:-}
EXPECTED_RULE_ID=1100001

case "$connector" in
    apache|nginx|haproxy|envoy|traefik|lighttpd) ;;
    *) echo "usage: $0 apache|nginx|haproxy|envoy|traefik|lighttpd" >&2; exit 2 ;;
esac
case "$evidence_stage" in
    minimal_runtime_smoke|no_crs_baseline) ;;
    *) echo "usage: $0 connector [minimal_runtime_smoke|no_crs_baseline]" >&2; exit 2 ;;
esac
case "$NO_CRS_ARTIFACT_PROFILE" in
    generic|full_lifecycle) ;;
    *) echo "FAIL: unsupported NO_CRS_ARTIFACT_PROFILE: $NO_CRS_ARTIFACT_PROFILE" >&2; exit 2 ;;
esac
case "$NO_CRS_PROTOCOL_CLIENT" in
    0|false|no|"") NO_CRS_PROTOCOL_CLIENT=0 ;;
    1|true|yes) NO_CRS_PROTOCOL_CLIENT=1 ;;
    *) echo "FAIL: NO_CRS_PROTOCOL_CLIENT must be 0 or 1" >&2; exit 1 ;;
esac
if { [ -n "$NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR" ] || \
     [ "$NO_CRS_PROTOCOL_CLIENT" = 1 ]; } && \
   [ "$NO_CRS_ARTIFACT_PROFILE" != full_lifecycle ]; then
    echo "FAIL: NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR requires NO_CRS_ARTIFACT_PROFILE=full_lifecycle" >&2
    exit 1
fi
case "$NO_CRS_RUN_ID" in
    [A-Za-z0-9]* ) ;;
    *) echo "FAIL: run id must start with an ASCII letter or digit: $NO_CRS_RUN_ID" >&2; exit 1 ;;
esac
case "$NO_CRS_RUN_ID" in
    *[!A-Za-z0-9._-]*) echo "FAIL: run id contains unsafe characters: $NO_CRS_RUN_ID" >&2; exit 1 ;;
esac
if [ "${#NO_CRS_RUN_ID}" -gt 128 ]; then
    echo "FAIL: run id exceeds 128 characters" >&2
    exit 1
fi
CAPABILITIES_FILE=$CONNECTOR_ROOT/connectors/$connector/capabilities.json
RUNTIME_PATH_RESOLVER=$CONNECTOR_ROOT/ci/runtime/common/resolve-runtime-paths.py
PROFILE_RESOLVER=$CONNECTOR_ROOT/ci/runtime/lifecycle/resolve-full-lifecycle-profile.py
LOG_SANITIZER=$CONNECTOR_ROOT/ci/runtime/lifecycle/sanitize-full-lifecycle-log.py
ENGINE_ARTIFACT_WRITER=$CONNECTOR_ROOT/ci/runtime/lifecycle/write-engine-lifecycle-artifacts.py
TRANSPORT_ARTIFACT_WRITER=$CONNECTOR_ROOT/ci/runtime/lifecycle/write-transport-lifecycle-artifacts.py
SYNCHRONIZED_UPSTREAM=$FRAMEWORK_ROOT/tests/runners/synchronized_upstream.py

[ -f "$FRAMEWORK_ROOT/ci/checks/catalog/no_crs_baseline.py" ] || {
    echo "BLOCKED: canonical framework runner is missing: $FRAMEWORK_ROOT/ci/checks/catalog/no_crs_baseline.py" >&2
    exit 77
}
[ -f "$LOG_SANITIZER" ] || {
    echo "FAIL: canonical log sanitizer is missing: $LOG_SANITIZER" >&2
    exit 1
}
[ -f "$ENGINE_ARTIFACT_WRITER" ] || {
    echo "FAIL: engine lifecycle artifact writer is missing: $ENGINE_ARTIFACT_WRITER" >&2
    exit 1
}
[ -f "$TRANSPORT_ARTIFACT_WRITER" ] || {
    echo "FAIL: transport lifecycle artifact writer is missing: $TRANSPORT_ARTIFACT_WRITER" >&2
    exit 1
}
[ -f "$SYNCHRONIZED_UPSTREAM" ] || {
    echo "FAIL: synchronized upstream helper is missing: $SYNCHRONIZED_UPSTREAM" >&2
    exit 1
}
[ -f "$CAPABILITIES_FILE" ] || {
    echo "FAIL: connector capability manifest is missing: $CAPABILITIES_FILE" >&2
    exit 1
}
[ -f "$RUNTIME_PATH_RESOLVER" ] || {
    echo "FAIL: runtime path resolver is missing: $RUNTIME_PATH_RESOLVER" >&2
    exit 1
}
[ -f "$PROFILE_RESOLVER" ] || {
    echo "FAIL: full-lifecycle profile resolver is missing: $PROFILE_RESOLVER" >&2
    exit 1
}
[ -f "$NO_CRS_RULES_FILE" ] || {
    echo "FAIL: canonical no-CRS rules are missing: $NO_CRS_RULES_FILE" >&2
    exit 1
}

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

if [ "$NO_CRS_ARTIFACT_PROFILE" = full_lifecycle ]; then
    expected_profile=$(expected_full_lifecycle_profile "$connector")
    expected_target=$(expected_full_lifecycle_target "$connector")
    if [ "$FULL_LIFECYCLE_HOST_PROFILE" != "$expected_profile" ]; then
        echo "FAIL: full-lifecycle $connector requires host profile $expected_profile; got ${FULL_LIFECYCLE_HOST_PROFILE:-unset}" >&2
        exit 1
    fi
    if [ -z "$FULL_LIFECYCLE_EXECUTED_TARGET" ]; then
        FULL_LIFECYCLE_EXECUTED_TARGET=$expected_target
    fi
    if [ "$FULL_LIFECYCLE_EXECUTED_TARGET" != "$expected_target" ]; then
        echo "FAIL: full-lifecycle $connector requires target $expected_target; got $FULL_LIFECYCLE_EXECUTED_TARGET" >&2
        exit 1
    fi
elif [ -n "$FULL_LIFECYCLE_HOST_PROFILE$FULL_LIFECYCLE_EXECUTED_TARGET" ]; then
    echo "FAIL: full-lifecycle profile variables require NO_CRS_ARTIFACT_PROFILE=full_lifecycle" >&2
    exit 1
fi

# One resolver owns every connector-local path.  It deliberately does not use
# legacy connector-specific environment variables, which prevents a later
# stage from inheriting another connector's build or run root.
runtime_paths=$("$PYTHON" "$RUNTIME_PATH_RESOLVER" \
    --connector "$connector" \
    --run-id "$NO_CRS_RUN_ID" \
    --invocation-root "$CANONICAL_VERIFIED_RUN_ROOT" \
    --evidence-root "$EVIDENCE_ROOT" \
    --build-root "$BUILD_ROOT" \
    --run-root "$RUNTIME_RUN_ROOT" \
    --log-root "$RUNTIME_LOG_ROOT" \
    --cache-root "$CACHE_ROOT" \
    --format shell) || {
    echo "FAIL: unable to resolve isolated runtime paths for $connector/$NO_CRS_RUN_ID" >&2
    exit 1
}
# The resolver emits shell-quoted export assignments only.  It validates every
# input before output and performs no filesystem mutation.
# shellcheck disable=SC2086
eval "$runtime_paths"
EVIDENCE_ROOT=$(dirname "$(dirname "$EVIDENCE_RUN_ROOT")")
BUILD_ROOT=$CONNECTOR_BUILD_ROOT
CONNECTOR_COMPONENT_CACHE=$SHARED_COMPONENT_CACHE
VERIFIED_COMPONENT_CACHE=$SHARED_COMPONENT_CACHE
CACHE_ROOT=$(dirname "$SHARED_COMPONENT_CACHE")
RUN_DIR=$EVIDENCE_RUN_ROOT
RAW_DIR=$CONNECTOR_RUN_ROOT
LOG_DIR=$CONNECTOR_LOG_ROOT
RESULTS_DIR=$CONNECTOR_RUN_ROOT/results
HOST_RUNTIME_ROOT=$CONNECTOR_RUN_ROOT/host-runtime
HOST_LOG_ROOT=$CONNECTOR_LOG_ROOT/host
HOST_TMP_ROOT=$CONNECTOR_RUN_ROOT/tmp
STAGE_BUILD_ROOT=$CONNECTOR_BUILD_ROOT
STAGE_TMP_ROOT=$HOST_TMP_ROOT
STAGE_LOG_ROOT=$HOST_LOG_ROOT
STAGE_RESULTS_DIR=$RESULTS_DIR
STAGE_RUNTIME_ROOT=$HOST_RUNTIME_ROOT
# The Framework HAProxy smoke contract requires its build, temporary, log,
# and result roots to be nested together. This is a disposable *host work*
# directory inside the already-isolated raw run, not the connector build root
# resolved above; shared component artifacts still remain under
# CONNECTOR_BUILD_ROOT and Cache-v2.
case "$connector" in
    haproxy)
        STAGE_BUILD_ROOT=$CONNECTOR_RUN_ROOT/haproxy-host-work
        STAGE_TMP_ROOT=$STAGE_BUILD_ROOT/tmp
        STAGE_LOG_ROOT=$STAGE_BUILD_ROOT/logs
        STAGE_RESULTS_DIR=$STAGE_BUILD_ROOT/results
        STAGE_RUNTIME_ROOT=$STAGE_BUILD_ROOT/runtime
        ;;
esac
NGINX_RUN_ROOT=$CONNECTOR_RUN_ROOT/nginx-harness
TRAEFIK_RUNTIME_ROOT=$CONNECTOR_RUN_ROOT/traefik-runtime
LIGHTTPD_RUNTIME_ROOT=$CONNECTOR_RUN_ROOT/lighttpd-runtime
PLAN=$CONNECTOR_RUN_ROOT/plan.json
SOURCE_RESULT=$CONNECTOR_RUN_ROOT/source-result.json
NORMALIZED_EVENTS=$CONNECTOR_RUN_ROOT/events.normalized.jsonl
SOURCE_EVENT_SCRUB_LOG=$CONNECTOR_LOG_ROOT/source-event-scrub.log
CANONICAL_STDOUT_LOG=$CONNECTOR_LOG_ROOT/stdout.canonical.log
CANONICAL_STDERR_LOG=$CONNECTOR_LOG_ROOT/stderr.canonical.log
CANONICAL_HOST_LOG=$CONNECTOR_LOG_ROOT/host.canonical.log
FIRST_BYTE_EVIDENCE=$CONNECTOR_RUN_ROOT/first-byte-evidence.json
FIRST_BYTE_EVIDENCE_SOURCE=${FIRST_BYTE_EVIDENCE_SOURCE:-}
ENGINE_ARTIFACT_DIR=$CONNECTOR_RUN_ROOT/engine-artifacts
ENGINE_VERSION_ARTIFACT=$ENGINE_ARTIFACT_DIR/engine-version.txt
ENGINE_LIBRARY_SHA256_ARTIFACT=$ENGINE_ARTIFACT_DIR/engine-library-sha256.txt
RULESET_SHA256_ARTIFACT=$ENGINE_ARTIFACT_DIR/ruleset-sha256.txt
TRANSACTION_COUNTS_ARTIFACT=$ENGINE_ARTIFACT_DIR/transaction-counts.json
LIFECYCLE_COUNTERS_ARTIFACT=$ENGINE_ARTIFACT_DIR/lifecycle-counters.json
TRANSPORT_ARTIFACT_DIR=$CONNECTOR_RUN_ROOT/transport-artifacts
CLIENT_TRANSPORT_LOG=$TRANSPORT_ARTIFACT_DIR/client.log
UPSTREAM_TRANSPORT_LOG=$TRANSPORT_ARTIFACT_DIR/upstream.log
TRANSPORT_LOG=$TRANSPORT_ARTIFACT_DIR/transport.log
CLEANUP_TRANSPORT_LOG=$TRANSPORT_ARTIFACT_DIR/cleanup.log
TRANSPORT_OBSERVATIONS_ARTIFACT=$TRANSPORT_ARTIFACT_DIR/transport-observations.json
CONNECTION_LIFECYCLE_ARTIFACT=$TRANSPORT_ARTIFACT_DIR/connection-lifecycle.json
BARRIER_EVENTS_ARTIFACT=$TRANSPORT_ARTIFACT_DIR/barrier-events.jsonl
EFFECTIVE_CONFIG_ARTIFACT_DIR=$CONNECTOR_RUN_ROOT/effective-config
EFFECTIVE_CONFIG_MANIFEST=$EFFECTIVE_CONFIG_ARTIFACT_DIR/manifest.json
EFFECTIVE_CAPABILITIES_FILE=$CAPABILITIES_FILE
protocol_client_artifact_optional=0
if [ "$NO_CRS_PROTOCOL_CLIENT" = 1 ] && [ -z "$NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR" ]; then
    # The raw run does not exist yet, so only the canonical runner can choose
    # this safe location. A host that cannot reach its selected protocol path
    # may leave the optional bundle absent; that remains non-promoting.
    NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR=$RAW_DIR/protocol-client
    protocol_client_artifact_optional=1
fi
FULL_LIFECYCLE_STAGE_REASON=
if [ "$NO_CRS_ARTIFACT_PROFILE" = full_lifecycle ]; then
    EFFECTIVE_CAPABILITIES_FILE=$CONNECTOR_BUILD_ROOT/effective-full-lifecycle-capabilities.json
    "$PYTHON" "$PROFILE_RESOLVER" \
        --input "$CAPABILITIES_FILE" \
        --output "$EFFECTIVE_CAPABILITIES_FILE" \
        --profile "$FULL_LIFECYCLE_HOST_PROFILE" || {
        echo "FAIL: unable to materialize effective full-lifecycle capabilities" >&2
        exit 1
    }
    CAPABILITIES_FILE=$EFFECTIVE_CAPABILITIES_FILE
    case "$connector" in
        haproxy)
            FULL_LIFECYCLE_STAGE_REASON="native HTX host runs real libmodsecurity P1--P4 with a host-buffered P2 classification, end-of-stream Phase-4 evaluation, and a safe HTTP/1.1 first-byte barrier"
            ;;
        envoy)
            FULL_LIFECYCLE_STAGE_REASON="native ext_proc host streams through Common/libmodsecurity with P1/P2/P3 and safe P4 host outcomes; strict post-commit reset remains not executed"
            ;;
        traefik)
            FULL_LIFECYCLE_STAGE_REASON="native Traefik middleware reaches a persistent local Common/libmodsecurity UDS service with P1/P2/P3 and safe P4 host outcomes; strict post-commit reset remains not executed"
            ;;
        lighttpd)
            FULL_LIFECYCLE_STAGE_REASON="patched lighttpd host runs real request/response entity-body ingestion before HTTP/1 transfer framing, end-of-stream Phase-4 evaluation, and a safe HTTP/1.1 first-byte barrier"
            ;;
    esac
fi
canonical_rules_file=$("$PYTHON" -c 'import pathlib,sys; print(pathlib.Path(sys.argv[1]).resolve(strict=True))' \
    "$FRAMEWORK_ROOT/tests/rules/no-crs-baseline.conf") || {
    echo "FAIL: cannot resolve canonical framework rules" >&2
    exit 1
}
executed_rules_file=$("$PYTHON" -c 'import pathlib,sys; print(pathlib.Path(sys.argv[1]).resolve(strict=True))' \
    "$NO_CRS_RULES_FILE") || {
    echo "FAIL: cannot resolve requested no-CRS rules" >&2
    exit 1
}
if [ "$executed_rules_file" != "$canonical_rules_file" ]; then
    echo "FAIL: canonical baseline may only execute $canonical_rules_file" >&2
    exit 1
fi
NO_CRS_RULES_FILE=$canonical_rules_file

case "$RUN_DIR" in
    /*) ;;
    *) echo "BLOCKED: canonical run directory must be absolute: $RUN_DIR" >&2; exit 77 ;;
esac
case "$RUN_DIR" in
    "$CONNECTOR_ROOT"|"$CONNECTOR_ROOT"/*)
        echo "BLOCKED: canonical evidence must be outside the checkout: $RUN_DIR" >&2
        exit 77
        ;;
esac

reject_symlink_components() {
    candidate=$1
    while [ "$candidate" != / ]; do
        if [ -L "$candidate" ]; then
            echo "FAIL: evidence path must not contain symlinks: $candidate" >&2
            exit 1
        fi
        candidate=$(dirname "$candidate")
    done
}

case "$RAW_DIR" in
    /*) ;;
    *) echo "BLOCKED: raw evidence directory must be absolute: $RAW_DIR" >&2; exit 77 ;;
esac
case "$RAW_DIR" in
    "$CONNECTOR_ROOT"|"$CONNECTOR_ROOT"/*)
        echo "BLOCKED: raw evidence must be outside the checkout: $RAW_DIR" >&2
        exit 77
        ;;
esac
reject_symlink_components "$RUN_DIR"
reject_symlink_components "$RAW_DIR"
if [ -n "$NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR" ]; then
    case "$NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR" in
        /*) ;;
        *) echo "FAIL: NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR must be absolute" >&2; exit 1 ;;
    esac
    # The harness is allowed to create the directory later, but it must be
    # scoped to this invocation's disposable raw run rather than an arbitrary
    # external tree.  Resolve and re-check it after the stage has finished.
    case "$NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR" in
        "$RAW_DIR"/*) ;;
        *) echo "FAIL: NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR must remain inside this raw run" >&2; exit 1 ;;
    esac
    reject_symlink_components "$NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR"
fi
if [ -e "$RUN_DIR" ] || [ -L "$RUN_DIR" ]; then
    echo "FAIL: canonical run directory already exists; choose a fresh run id: $RUN_DIR" >&2
    exit 1
fi
if [ -e "$RAW_DIR" ] || [ -L "$RAW_DIR" ]; then
    echo "FAIL: raw evidence directory already exists; choose a fresh run id: $RAW_DIR" >&2
    exit 1
fi

mkdir -p "$RAW_DIR" "$LOG_DIR" "$RESULTS_DIR"

# Reserve one exact local runtime-env destination before entering the stage.
# The stage receives this path unchanged, and this canonical runner later
# reads only that file for host inventory.  It must never reopen the mutable
# shared Cache-v2 runtime-env.sh after a concurrent connector preparation.
RUNTIME_REPORT_OUTPUT_ROOT=$CONNECTOR_BUILD_ROOT/runtime-component-reports
case "$connector" in
    apache|nginx|haproxy) canonical_runtime_component_target=$connector ;;
    envoy|traefik|lighttpd) canonical_runtime_component_target=shared ;;
esac
reject_symlink_components "$RUNTIME_REPORT_OUTPUT_ROOT"
if [ -z "${RUNTIME_COMPONENT_ENV_SNAPSHOT:-}" ]; then
    RUNTIME_COMPONENT_ENV_SNAPSHOT=$(sh "$CONNECTOR_ROOT/ci/runtime/lifecycle/reserve-runtime-env-snapshot.sh" "$RUNTIME_REPORT_OUTPUT_ROOT") || exit $?
    snapshot_reserved_here=1
else
    snapshot_reserved_here=0
fi
case "$RUNTIME_COMPONENT_ENV_SNAPSHOT" in
    "$RUNTIME_REPORT_OUTPUT_ROOT"/*) ;;
    *)
        echo "FAIL: canonical runtime environment snapshot must be under this connector build root: $RUNTIME_COMPONENT_ENV_SNAPSHOT" >&2
        exit 1
        ;;
esac
reject_symlink_components "$RUNTIME_COMPONENT_ENV_SNAPSHOT"
export RUNTIME_COMPONENT_ENV_SNAPSHOT

"$PYTHON" "$FRAMEWORK_ROOT/ci/checks/catalog/no_crs_baseline.py" select \
    --connector "$connector" \
    --capabilities "$CAPABILITIES_FILE" \
    --evidence-stage "$evidence_stage" \
    --artifact-profile "$NO_CRS_ARTIFACT_PROFILE" \
    --output "$PLAN"
NO_CRS_SELECTED_CASES=$("$PYTHON" -c '
import json, sys
plan = json.load(open(sys.argv[1], encoding="utf-8"))
print(" ".join(
    str(item["runner_case"]) for item in plan.get("cases", [])
    if item.get("selection_status") == "SELECTED" and item.get("runner_case")
))
' "$PLAN")
NO_CRS_SELECTED_CASE_IDS=$("$PYTHON" -c '
import json, sys
plan = json.load(open(sys.argv[1], encoding="utf-8"))
print(" ".join(
    str(item["case_id"]) for item in plan.get("cases", [])
    if item.get("selection_status") == "SELECTED" and item.get("case_id")
))
' "$PLAN")
if [ "$NO_CRS_ARTIFACT_PROFILE" != full_lifecycle ] || \
   [ "$connector" = apache ] || [ "$connector" = nginx ]; then
    case " $NO_CRS_SELECTED_CASES " in
        *" allow_without_marker.yaml "*) ;;
        *) echo "FAIL: canonical plan does not select mandatory allow runner case" >&2; exit 1 ;;
    esac
    case " $NO_CRS_SELECTED_CASES " in
        *" deny_header_marker_403.yaml "*) ;;
        *) echo "FAIL: canonical plan does not select mandatory deny runner case" >&2; exit 1 ;;
    esac
else
    # A native profile that has no executable capability yet is still a useful
    # canonical record: it finalizes as NOT_EXECUTED/BLOCKED instead of being
    # silently rerouted through its compatibility implementation.
    echo "INFO: $connector/$FULL_LIFECYCLE_HOST_PROFILE has no mandatory compatibility-case requirement"
fi

executed_target=no-crs-baseline-$connector
if [ "$NO_CRS_ARTIFACT_PROFILE" = full_lifecycle ]; then
    executed_target=$FULL_LIFECYCLE_EXECUTED_TARGET
fi

"$PYTHON" "$FRAMEWORK_ROOT/ci/checks/catalog/no_crs_baseline.py" init \
    --connector "$connector" \
    --capabilities "$CAPABILITIES_FILE" \
    --plan "$PLAN" \
    --run-dir "$RUN_DIR" \
    --connector-root "$CONNECTOR_ROOT" \
    --run-id "$NO_CRS_RUN_ID" \
    --evidence-stage "$evidence_stage" \
    --artifact-profile "$NO_CRS_ARTIFACT_PROFILE" \
    --host-profile "${FULL_LIFECYCLE_HOST_PROFILE:-default}" \
    --executed-target "$executed_target" \
    --host-version not_provisioned \
    --libmodsecurity-version not_provisioned

started_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)
set +e
CONNECTOR_ROOT="$CONNECTOR_ROOT" \
FRAMEWORK_ROOT="$FRAMEWORK_ROOT" \
VERIFIED_RUN_ROOT="$CANONICAL_VERIFIED_RUN_ROOT" \
VERIFIED_BUILD_ROOT="$STAGE_BUILD_ROOT" \
VERIFIED_TMP_ROOT="$STAGE_TMP_ROOT" \
VERIFIED_LOG_ROOT="$STAGE_LOG_ROOT" \
VERIFIED_COMPONENT_CACHE="$SHARED_COMPONENT_CACHE" \
CACHE_ROOT="$CACHE_ROOT" \
CONNECTOR_COMPONENT_CACHE="$SHARED_COMPONENT_CACHE" \
BUILD_ROOT="$STAGE_BUILD_ROOT" \
TMP_ROOT="$STAGE_TMP_ROOT" \
LOG_ROOT="$STAGE_LOG_ROOT" \
RESULTS_DIR="$STAGE_RESULTS_DIR" \
RUNTIME_ROOT="$STAGE_RUNTIME_ROOT" \
RUNTIME_BASE="$STAGE_RUNTIME_ROOT" \
RUNTIME_REPORT_OUTPUT_ROOT="$RUNTIME_REPORT_OUTPUT_ROOT" \
RUNTIME_COMPONENT_TARGET="$canonical_runtime_component_target" \
RUNTIME_COMPONENT_ENV_SNAPSHOT="$RUNTIME_COMPONENT_ENV_SNAPSHOT" \
APACHE_RUNTIME_LOG_DIR="$HOST_RUNTIME_ROOT/apache-runtime" \
NGINX_HARNESS_PARENT="$RAW_DIR" \
NGINX_HARNESS_WORK_ROOT="$NGINX_RUN_ROOT" \
RUNTIME_EVENT_LOG_PATH="$STAGE_RUNTIME_ROOT/events.jsonl" \
HAPROXY_HTX_RUNTIME_ROOT="$STAGE_RUNTIME_ROOT" \
HAPROXY_HTX_EVENT_LOG_PATH="$STAGE_RUNTIME_ROOT/events.jsonl" \
ENVOY_RUNTIME_ROOT="$HOST_RUNTIME_ROOT" \
ENVOY_CONFIG_ROOT="$HOST_RUNTIME_ROOT/config" \
ENVOY_LOG_ROOT="$HOST_LOG_ROOT" \
ENVOY_RESULT_ROOT="$HOST_RUNTIME_ROOT" \
ENVOY_EXT_PROC_RUNTIME_ROOT="$HOST_RUNTIME_ROOT" \
ENVOY_EXT_PROC_EVENT_LOG_PATH="$HOST_RUNTIME_ROOT/events.jsonl" \
TRAEFIK_CONFIG_ROOT="$TRAEFIK_RUNTIME_ROOT/config" \
TRAEFIK_LOG_ROOT="$HOST_LOG_ROOT/traefik" \
TRAEFIK_RESULT_ROOT="$TRAEFIK_RUNTIME_ROOT" \
TRAEFIK_NATIVE_RUNTIME_ROOT="$TRAEFIK_RUNTIME_ROOT" \
TRAEFIK_BUILD_ROOT="$CONNECTOR_BUILD_ROOT/traefik-connector" \
TRAEFIK_CONNECTOR_BUILD_DIR="$CONNECTOR_BUILD_ROOT/traefik-connector" \
TRAEFIK_CONNECTOR_BIN="$CONNECTOR_BUILD_ROOT/traefik-connector/traefik-forwardauth" \
TRAEFIK_CONNECTOR_START_ROOT="$CONNECTOR_RUN_ROOT/traefik-start-smoke" \
TRAEFIK_NATIVE_MIDDLEWARE_BUILD_DIR="$CONNECTOR_BUILD_ROOT/traefik-native-middleware" \
TRAEFIK_CONNECTOR_RESULT_ROOT="$TRAEFIK_RUNTIME_ROOT" \
LIGHTTPD_CONFIG_ROOT="$LIGHTTPD_RUNTIME_ROOT/config" \
LIGHTTPD_LOG_ROOT="$HOST_LOG_ROOT/lighttpd" \
LIGHTTPD_RESULT_ROOT="$LIGHTTPD_RUNTIME_ROOT" \
LIGHTTPD_CONNECTOR_BUILD_ROOT="$CONNECTOR_BUILD_ROOT/lighttpd-connector" \
LIGHTTPD_MODULE_DIR="$CONNECTOR_BUILD_ROOT/lighttpd-connector/modules" \
LIGHTTPD_SMOKE_DIR="$LIGHTTPD_RUNTIME_ROOT" \
LIGHTTPD_PATCHED_ROOT="$HOST_RUNTIME_ROOT/lighttpd-patched" \
LIGHTTPD_PATCHED_SMOKE_DIR="$LIGHTTPD_RUNTIME_ROOT" \
RULES_FILE="$NO_CRS_RULES_FILE" \
MSCONNECTOR_RULES_FILE="$NO_CRS_RULES_FILE" \
NO_CRS_RULES_FILE="$NO_CRS_RULES_FILE" \
NO_CRS_SELECTED_CASES="$NO_CRS_SELECTED_CASES" \
NO_CRS_SELECTED_CASE_IDS="$NO_CRS_SELECTED_CASE_IDS" \
NO_CRS_ARTIFACT_PROFILE="$NO_CRS_ARTIFACT_PROFILE" \
NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR="$NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR" \
FULL_LIFECYCLE_HOST_PROFILE="$FULL_LIFECYCLE_HOST_PROFILE" \
FULL_LIFECYCLE_EXECUTED_TARGET="$FULL_LIFECYCLE_EXECUTED_TARGET" \
FULL_LIFECYCLE_EVIDENCE_OUTPUT="$FIRST_BYTE_EVIDENCE" \
MSCONNECTOR_EXPECTED_RULE_ID="$EXPECTED_RULE_ID" \
NO_CRS_RUN_ID="$NO_CRS_RUN_ID" \
sh "$CONNECTOR_ROOT/ci/runtime/lifecycle/run-connector-stage.sh" "$connector" "$evidence_stage" \
    >"$LOG_DIR/stdout.log" 2>"$LOG_DIR/stderr.log"
stage_rc=$?
set -e
ended_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)
PROCESS_CLEANUP_LOG=$LOG_DIR/process-cleanup.log
if ps -eo pid=,comm=,args= | MSCONNECTOR_PROCESS_ROOT="$CONNECTOR_RUN_ROOT" awk '
    BEGIN { root=ENVIRON["MSCONNECTOR_PROCESS_ROOT"] }
    index($0, root) > 0 && ($2 ~ /^(httpd|apache2|nginx|haproxy|envoy|traefik|lighttpd|spoa|msconnector)/ || ($2 ~ /^python/ && $0 ~ /serve-upstream/)) { print $1, $2; found=1 }
    END { exit(found ? 1 : 0) }
' > "$PROCESS_CLEANUP_LOG"; then
    printf 'none\n' > "$PROCESS_CLEANUP_LOG"
else
    cleanup_rc=$?
    if [ "$cleanup_rc" -eq 1 ] && [ -s "$PROCESS_CLEANUP_LOG" ]; then
        echo "FAIL: connector processes remain after canonical run; see $PROCESS_CLEANUP_LOG" >&2
        stage_rc=1
    else
        echo "FAIL: unable to verify connector process cleanup" >&2
        printf 'process-check-failed rc=%s\n' "$cleanup_rc" > "$PROCESS_CLEANUP_LOG"
        stage_rc=1
    fi
fi

# Apache and NGINX have native proxy/filter paths with synchronized barrier
# support. Run their additional proof separately so the client can be observed
# while the upstream is deliberately paused. Other selected host routes retain
# a diagnostic-only barrier until they publish equivalent real-host evidence.
if [ "$NO_CRS_ARTIFACT_PROFILE" = full_lifecycle ]; then
    case "$connector" in
        apache|nginx)
            run_native_first_byte=1
            if [ "$connector" = nginx ] && \
               [ "${NGINX_DOWNSTREAM_PROTOCOL:-http1}" != http1 ]; then
                # The synchronized helper is an H1-only proof. A selected
                # H2/H3 listener must not inherit its H1 result or turn its
                # honest non-execution into a runner failure.
                run_native_first_byte=0
                echo "INFO: skipping H1 native first-byte helper for NGINX downstream ${NGINX_DOWNSTREAM_PROTOCOL}" >&2
            fi
            if [ "$run_native_first_byte" -eq 1 ]; then
                native_first_byte_rc=0
                CONNECTOR_ROOT="$CONNECTOR_ROOT" \
                FRAMEWORK_ROOT="$FRAMEWORK_ROOT" \
                BUILD_ROOT="$BUILD_ROOT" \
                RESULTS_DIR="$RESULTS_DIR" \
                HOST_RUNTIME_ROOT="$HOST_RUNTIME_ROOT" \
                HOST_LOG_ROOT="$HOST_LOG_ROOT" \
                NO_CRS_RULES_FILE="$NO_CRS_RULES_FILE" \
                FULL_LIFECYCLE_EVIDENCE_OUTPUT="$FIRST_BYTE_EVIDENCE" \
                SKIP_RUNTIME_COMPONENT_PREPARE=1 \
                sh "$CONNECTOR_ROOT/ci/runtime/lifecycle/run-native-first-byte.sh" "$connector" || native_first_byte_rc=$?
                if [ "$native_first_byte_rc" -ne 0 ]; then
                    stage_rc=$native_first_byte_rc
                fi
            fi
            ;;
    esac
fi

source_results=
source_result=
source_events=
source_first_byte_results=$STAGE_RESULTS_DIR/$connector-first-byte-results.jsonl
case "$connector" in
    apache|nginx)
        source_results=$STAGE_RESULTS_DIR/$connector-results.jsonl
        source_result=$STAGE_RESULTS_DIR/$connector-summary.json
        ;;
    haproxy)
        if [ "$NO_CRS_ARTIFACT_PROFILE" = full_lifecycle ]; then
            source_result=$STAGE_RUNTIME_ROOT/runtime-summary.txt
            source_events=$STAGE_RUNTIME_ROOT/events.jsonl
        else
            source_results=$STAGE_RESULTS_DIR/$connector-results.jsonl
            source_result=$STAGE_RESULTS_DIR/$connector-summary.json
        fi
        ;;
    envoy)
        source_result=$HOST_RUNTIME_ROOT/runtime-summary.txt
        source_events=$HOST_RUNTIME_ROOT/events.jsonl
        ;;
    traefik)
        source_result=$TRAEFIK_RUNTIME_ROOT/result.json
        source_events=$TRAEFIK_RUNTIME_ROOT/logs/events.jsonl
        ;;
    lighttpd)
        source_results=$LIGHTTPD_RUNTIME_ROOT/results.jsonl
        source_result=$LIGHTTPD_RUNTIME_ROOT/runtime-summary.txt
        source_events=$LIGHTTPD_RUNTIME_ROOT/events.jsonl
        ;;
esac

set -- \
    --connector "$connector" \
    --stage-rc "$stage_rc" \
    --expected-rule-id "$EXPECTED_RULE_ID" \
    --catalog "$FRAMEWORK_ROOT/tests/cases/no-crs-baseline/catalog.json" \
    --stdout "$LOG_DIR/stdout.log" \
    --stderr "$LOG_DIR/stderr.log" \
    --allowed-source-root "$RAW_DIR" \
    --scrub-source-events \
    --source-event-scrub-log "$SOURCE_EVENT_SCRUB_LOG" \
    --events-output "$NORMALIZED_EVENTS" \
    --output "$SOURCE_RESULT"
if [ -n "$source_result" ] && [ -f "$source_result" ]; then
    set -- "$@" --source-result "$source_result"
fi
if [ -n "$source_results" ] && [ -f "$source_results" ]; then
    set -- "$@" --source-results-jsonl "$source_results"
fi
if [ -f "$source_first_byte_results" ]; then
    set -- "$@" --source-results-jsonl "$source_first_byte_results"
fi
if [ -n "$source_events" ] && [ -f "$source_events" ]; then
    set -- "$@" --source-events "$source_events"
fi
"$PYTHON" "$CONNECTOR_ROOT/ci/runtime/lifecycle/collect-no-crs-source.py" "$@"

# Raw host logs remain in the disposable run directory.  Canonical evidence
# receives only bounded, sentinel-free diagnostics plus a metadata-only host
# summary, so body fixtures and credentials cannot be retained accidentally.
"$PYTHON" "$LOG_SANITIZER" --input "$LOG_DIR/stdout.log" \
    --output "$CANONICAL_STDOUT_LOG" --label "${connector}-stage-stdout"
"$PYTHON" "$LOG_SANITIZER" --input "$LOG_DIR/stderr.log" \
    --output "$CANONICAL_STDERR_LOG" --label "${connector}-stage-stderr"
{
    printf 'connector=%s\n' "$connector"
    printf 'evidence_stage=%s\n' "$evidence_stage"
    printf 'artifact_profile=%s\n' "$NO_CRS_ARTIFACT_PROFILE"
    printf 'host_profile=%s\n' "${FULL_LIFECYCLE_HOST_PROFILE:-default}"
    printf 'executed_target=%s\n' "$executed_target"
    printf 'stage_exit_code=%s\n' "$stage_rc"
    printf 'process_cleanup_log=%s\n' "$(basename "$PROCESS_CLEANUP_LOG")"
    "$PYTHON" - "$LOG_DIR/stdout.log" "$LOG_DIR/stderr.log" <<'PY'
import hashlib
import sys
from pathlib import Path

for label, value in zip(("stage_stdout", "stage_stderr"), sys.argv[1:]):
    raw = Path(value).read_bytes() if Path(value).is_file() else b""
    print(f"{label}_sha256={hashlib.sha256(raw).hexdigest()}")
    print(f"{label}_bytes={len(raw)}")
PY
} > "$CANONICAL_HOST_LOG"
if [ ! -f "$NORMALIZED_EVENTS" ]; then
    : > "$NORMALIZED_EVENTS"
fi
if [ "$NO_CRS_ARTIFACT_PROFILE" = full_lifecycle ]; then
    "$PYTHON" "$TRANSPORT_ARTIFACT_WRITER" \
        --connector "$connector" \
        --run-id "$NO_CRS_RUN_ID" \
        --events "$NORMALIZED_EVENTS" \
        --output-dir "$TRANSPORT_ARTIFACT_DIR" || {
            echo "FAIL: unable to write payload-free transport lifecycle artifacts" >&2
            exit 1
        }
    for transport_artifact in \
        "$CLIENT_TRANSPORT_LOG" \
        "$UPSTREAM_TRANSPORT_LOG" \
        "$TRANSPORT_LOG" \
        "$CLEANUP_TRANSPORT_LOG" \
        "$TRANSPORT_OBSERVATIONS_ARTIFACT" \
        "$CONNECTION_LIFECYCLE_ARTIFACT" \
        "$BARRIER_EVENTS_ARTIFACT"; do
        if [ ! -f "$transport_artifact" ] || [ -L "$transport_artifact" ]; then
            echo "FAIL: required transport artifact is missing or unsafe: $transport_artifact" >&2
            exit 1
        fi
    done
fi
if [ "$NO_CRS_ARTIFACT_PROFILE" = full_lifecycle ]; then
    if [ -n "$FIRST_BYTE_EVIDENCE_SOURCE" ]; then
        case "$FIRST_BYTE_EVIDENCE_SOURCE" in
            /*) ;;
            *) echo "FAIL: FIRST_BYTE_EVIDENCE_SOURCE must be absolute" >&2; exit 1 ;;
        esac
        case "$FIRST_BYTE_EVIDENCE_SOURCE" in
            "$RAW_DIR"/*) ;;
            *) echo "FAIL: FIRST_BYTE_EVIDENCE_SOURCE must remain inside this raw run: $FIRST_BYTE_EVIDENCE_SOURCE" >&2; exit 1 ;;
        esac
        [ ! -L "$FIRST_BYTE_EVIDENCE_SOURCE" ] || {
            echo "FAIL: FIRST_BYTE_EVIDENCE_SOURCE must not be a symlink" >&2
            exit 1
        }
        [ -f "$FIRST_BYTE_EVIDENCE_SOURCE" ] || {
            echo "FAIL: FIRST_BYTE_EVIDENCE_SOURCE is missing: $FIRST_BYTE_EVIDENCE_SOURCE" >&2
            exit 1
        }
        if [ "$FIRST_BYTE_EVIDENCE_SOURCE" != "$FIRST_BYTE_EVIDENCE" ]; then
            cp "$FIRST_BYTE_EVIDENCE_SOURCE" "$FIRST_BYTE_EVIDENCE"
        fi
    elif [ ! -f "$FIRST_BYTE_EVIDENCE" ]; then
        # Preserve an explicit synthetic barrier observation when no connector
        # harness supplied a real-host one.  The Framework records its origin
        # and refuses to promote either low-latency capability from it.
        "$PYTHON" "$SYNCHRONIZED_UPSTREAM" --output "$FIRST_BYTE_EVIDENCE" \
            >"$LOG_DIR/synchronized-upstream.stdout.log" \
            2>"$LOG_DIR/synchronized-upstream.stderr.log" || true
        [ -f "$FIRST_BYTE_EVIDENCE" ] || {
            echo "FAIL: synchronized first-byte diagnostic did not produce evidence" >&2
            exit 1
        }
    fi
fi

host_version=not_provisioned
host_binary=
runtime_env=$RUNTIME_COMPONENT_ENV_SNAPSHOT
if [ -s "$runtime_env" ]; then
    snapshot_path_valid=1
    case "$runtime_env" in
        "$CONNECTOR_BUILD_ROOT/runtime-component-reports"/*) ;;
        *)
            echo "FAIL: canonical runtime environment snapshot escaped its connector build root: $runtime_env" >&2
            stage_rc=1
            snapshot_path_valid=0
            ;;
    esac
    if [ "$snapshot_path_valid" -eq 1 ]; then
        reject_symlink_components "$runtime_env"
        # This is the exact invocation-local file passed to run-connector-stage,
        # not the mutable shared Cache-v2 compatibility export.
        # shellcheck disable=SC1090
        . "$runtime_env"
        case "$canonical_runtime_component_target:${RUNTIME_COMPONENT_ENV_SNAPSHOT_TARGET:-}" in
            apache:apache|nginx:nginx|haproxy:haproxy|shared:shared|shared:all) ;;
            *)
                echo "FAIL: canonical runtime environment snapshot target mismatch: requested=$canonical_runtime_component_target snapshot=${RUNTIME_COMPONENT_ENV_SNAPSHOT_TARGET:-unset}" >&2
                stage_rc=1
                ;;
        esac
        if [ "${RUNTIME_COMPONENT_ENV_SNAPSHOT_CACHE:-}" != "$SHARED_COMPONENT_CACHE" ]; then
            echo "FAIL: canonical runtime environment snapshot cache mismatch: expected=$SHARED_COMPONENT_CACHE snapshot=${RUNTIME_COMPONENT_ENV_SNAPSHOT_CACHE:-unset}" >&2
            stage_rc=1
        fi
    fi
elif [ "$stage_rc" -eq 0 ]; then
    echo "FAIL: canonical stage completed without its invocation-local runtime environment snapshot: $runtime_env" >&2
    stage_rc=1
elif [ "$snapshot_reserved_here" -eq 1 ]; then
    # Full-lifecycle BLOCKED profiles may exit before any component resolver
    # runs.  Do not leave their empty reservation behind as if it were usable
    # evidence.
    rm -f "$runtime_env"
fi
# A snapshot may supply toolchain paths, but never gets to redirect the
# resolver-selected cache or the connector-local build root used for inventory.
CONNECTOR_COMPONENT_CACHE=$SHARED_COMPONENT_CACHE
VERIFIED_COMPONENT_CACHE=$SHARED_COMPONENT_CACHE
RUNTIME_COMPONENT_ENV_SNAPSHOT=$runtime_env
# Store only an allowlisted hash inventory for effective configuration.  Raw
# rules and host configuration can contain fixture payloads or credentials and
# must remain in the disposable run root.
if [ "$NO_CRS_ARTIFACT_PROFILE" = full_lifecycle ]; then
    set -- \
        --connector "$connector" \
        --run-id "$NO_CRS_RUN_ID" \
        --effective-config-dir "$EFFECTIVE_CONFIG_ARTIFACT_DIR" \
        --config-file "capabilities.json=$CAPABILITIES_FILE" \
        --config-file "rules/no-crs-baseline.conf=$NO_CRS_RULES_FILE"
    if [ -s "$runtime_env" ]; then
        set -- "$@" --config-file "runtime-components.env=$runtime_env"
    fi
    "$PYTHON" "$TRANSPORT_ARTIFACT_WRITER" "$@" || {
        echo "FAIL: unable to write effective configuration inventory" >&2
        exit 1
    }
    if [ ! -f "$EFFECTIVE_CONFIG_MANIFEST" ] || [ -L "$EFFECTIVE_CONFIG_MANIFEST" ]; then
        echo "FAIL: effective configuration inventory is missing or unsafe" >&2
        exit 1
    fi
fi
# Inventory must describe this connector's isolated build root even if a
# concurrent connector invocation generated another shared compatibility file.
BUILD_ROOT=$CONNECTOR_BUILD_ROOT
case "$connector" in
    apache) host_binary=${APACHE_HTTPD:-$BUILD_ROOT/apache-runtime/httpd/bin/httpd} ;;
    nginx) host_binary=${MRTS_NATIVE_NGINX_BIN:-$BUILD_ROOT/nginx-runtime/nginx/sbin/nginx} ;;
    haproxy)
        if [ "$NO_CRS_ARTIFACT_PROFILE" = full_lifecycle ]; then
            host_binary=$STAGE_RUNTIME_ROOT/overlay-build/worktree/haproxy
        else
            host_binary=${HAPROXY_BIN:-$BUILD_ROOT/haproxy-runtime/haproxy/sbin/haproxy}
        fi
        ;;
    envoy) host_binary=$CONNECTOR_COMPONENT_CACHE/envoy/bin/envoy ;;
    traefik) host_binary=$CONNECTOR_COMPONENT_CACHE/traefik/bin/traefik ;;
    lighttpd)
        if [ "$NO_CRS_ARTIFACT_PROFILE" = full_lifecycle ]; then
            host_binary=$HOST_RUNTIME_ROOT/lighttpd-patched/stage/bin/lighttpd
        else
            host_binary=$CONNECTOR_COMPONENT_CACHE/lighttpd/bin/lighttpd
        fi
        ;;
esac
if [ -x "$host_binary" ]; then
    case "$connector" in
        apache)
            apache_runtime_lib=$(dirname "$(dirname "$host_binary")")/lib
            host_version=$(LD_LIBRARY_PATH="$apache_runtime_lib:${MODSECURITY_LIB_DIR:-}:${LD_LIBRARY_PATH:-}" \
                "$host_binary" -v 2>&1 | sed -n '/./{p;q;}')
            ;;
        nginx) host_version=$($host_binary -v 2>&1 | sed -n '/./{p;q;}') ;;
        haproxy) host_version=$($host_binary -v 2>&1 | sed -n '/./{p;q;}') ;;
        envoy) host_version=$($host_binary --version 2>&1 | sed -n '/./{p;q;}') ;;
        traefik) host_version=$($host_binary version 2>&1 | sed -n '/./{p;q;}') ;;
        lighttpd) host_version=$($host_binary -v 2>&1 | sed -n '/./{p;q;}') ;;
    esac
fi
[ -n "$host_version" ] || host_version=unknown

libmodsecurity_version=not_provisioned
component_manifest=$CONNECTOR_COMPONENT_CACHE/manifest.json
if [ -f "$component_manifest" ]; then
    libmodsecurity_version=$($PYTHON - "$component_manifest" <<'PY'
import json
import sys

try:
    component = json.load(open(sys.argv[1], encoding="utf-8")).get("modsecurity", {})
except (OSError, ValueError):
    component = {}
if component.get("status") in {"built", "reused", "present"} and component.get("actual_sha") and component.get("build_id"):
    print(f"git:{component['actual_sha']};build:{component['build_id']}")
else:
    print("not_provisioned")
PY
    )
fi

# Full-lifecycle engine sidecars are an inventory of the exact current raw
# host run.  They do not feed capability selection or promotion: canonical
# PASS still requires the normal transaction-bound host event evidence.
if [ "$NO_CRS_ARTIFACT_PROFILE" = full_lifecycle ] && [ "$stage_rc" -eq 0 ]; then
    libmodsecurity_library=${MODSECURITY_LIB_FILE:-}
    if [ -z "$libmodsecurity_library" ] || [ ! -f "$libmodsecurity_library" ]; then
        libmodsecurity_library=${MODSECURITY_LIB_DIR:-}/libmodsecurity.so
    fi
    if [ ! -f "$libmodsecurity_library" ]; then
        echo "FAIL: full-lifecycle engine library is unavailable for provenance: $libmodsecurity_library" >&2
        exit 1
    fi
    "$PYTHON" "$ENGINE_ARTIFACT_WRITER" \
        --connector "$connector" \
        --source-result "$SOURCE_RESULT" \
        --source-events "$NORMALIZED_EVENTS" \
        --rules-file "$NO_CRS_RULES_FILE" \
        --libmodsecurity-version "$libmodsecurity_version" \
        --libmodsecurity-library "$libmodsecurity_library" \
        --stage-exit-code "$stage_rc" \
        --transport-lifecycle "$CONNECTION_LIFECYCLE_ARTIFACT" \
        --output-dir "$ENGINE_ARTIFACT_DIR" || {
            echo "FAIL: unable to write full-lifecycle engine artifacts" >&2
            exit 1
        }
    for engine_artifact in \
        "$ENGINE_VERSION_ARTIFACT" \
        "$ENGINE_LIBRARY_SHA256_ARTIFACT" \
        "$RULESET_SHA256_ARTIFACT" \
        "$TRANSACTION_COUNTS_ARTIFACT" \
        "$LIFECYCLE_COUNTERS_ARTIFACT"; do
        if [ ! -s "$engine_artifact" ]; then
            echo "FAIL: required full-lifecycle engine artifact is missing: $engine_artifact" >&2
            exit 1
        fi
    done
fi

set -- \
    finalize \
    --run-dir "$RUN_DIR" \
    --connector-root "$CONNECTOR_ROOT" \
    --capabilities "$CAPABILITIES_FILE" \
    --source-result "$SOURCE_RESULT" \
    --stdout-log "$CANONICAL_STDOUT_LOG" \
    --stderr-log "$CANONICAL_STDERR_LOG" \
    --source-log "process_cleanup=$PROCESS_CLEANUP_LOG" \
    --source-log "source_event_scrub=$SOURCE_EVENT_SCRUB_LOG" \
    --stage-rc "$stage_rc" \
    --host-version "$host_version" \
    --libmodsecurity-version "$libmodsecurity_version" \
    --started-at "$started_at" \
    --ended-at "$ended_at"
if [ -n "$FULL_LIFECYCLE_STAGE_REASON" ]; then
    set -- "$@" --stage-reason "$FULL_LIFECYCLE_STAGE_REASON"
fi
if [ "$NO_CRS_ARTIFACT_PROFILE" = full_lifecycle ] || [ -s "$NORMALIZED_EVENTS" ]; then
    set -- "$@" --source-events "$NORMALIZED_EVENTS"
fi
if [ "$NO_CRS_ARTIFACT_PROFILE" = full_lifecycle ]; then
    set -- "$@" --host-log "$CANONICAL_HOST_LOG" \
        --first-byte-evidence "$FIRST_BYTE_EVIDENCE" \
        --source-artifact "client_log=$CLIENT_TRANSPORT_LOG" \
        --source-artifact "upstream_log=$UPSTREAM_TRANSPORT_LOG" \
        --source-artifact "transport_log=$TRANSPORT_LOG" \
        --source-artifact "cleanup_log=$CLEANUP_TRANSPORT_LOG" \
        --source-artifact "transport_observations=$TRANSPORT_OBSERVATIONS_ARTIFACT" \
        --source-artifact "connection_lifecycle=$CONNECTION_LIFECYCLE_ARTIFACT" \
        --source-artifact "barrier_events=$BARRIER_EVENTS_ARTIFACT" \
        --source-artifact "effective_config=$EFFECTIVE_CONFIG_ARTIFACT_DIR"
    if [ "$stage_rc" -eq 0 ]; then
        set -- "$@" \
            --source-artifact "engine_version=$ENGINE_VERSION_ARTIFACT" \
            --source-artifact "engine_library_sha256=$ENGINE_LIBRARY_SHA256_ARTIFACT" \
            --source-artifact "ruleset_sha256=$RULESET_SHA256_ARTIFACT" \
            --source-artifact "transaction_counts=$TRANSACTION_COUNTS_ARTIFACT" \
            --source-artifact "lifecycle_counters=$LIFECYCLE_COUNTERS_ARTIFACT"
    fi
fi
if [ -n "$NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR" ]; then
    if [ ! -d "$NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR" ] || \
       [ -L "$NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR" ]; then
        if [ "$protocol_client_artifact_optional" = 1 ]; then
            echo "INFO: optional protocol client did not publish a bundle; no protocol capability is promoted" >&2
            protocol_client_artifact_dir=
        else
            echo "FAIL: protocol client artifact directory is missing or unsafe" >&2
            exit 1
        fi
    else
        reject_symlink_components "$NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR"
        protocol_client_artifact_dir=$("$PYTHON" - \
            "$NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR" "$RAW_DIR" <<'PY'
import sys
from pathlib import Path

candidate = Path(sys.argv[1]).resolve(strict=True)
raw_root = Path(sys.argv[2]).resolve(strict=True)
if candidate == raw_root or raw_root not in candidate.parents:
    raise SystemExit("protocol client artifact directory escaped the current raw run")
print(candidate)
PY
        ) || {
            echo "FAIL: protocol client artifact directory escaped the current raw run" >&2
            exit 1
        }
    fi
else
    protocol_client_artifact_dir=
fi
if [ -n "$protocol_client_artifact_dir" ]; then
    set -- "$@" --protocol-client-artifact-dir "$protocol_client_artifact_dir"
fi

set +e
"$PYTHON" "$FRAMEWORK_ROOT/ci/checks/catalog/no_crs_baseline.py" "$@"
finalize_rc=$?
set -e
if [ "$finalize_rc" -ne 0 ]; then
    exit "$finalize_rc"
fi
latest_file=$EVIDENCE_ROOT/$connector/latest-run-id
reject_symlink_components "$latest_file"
latest_tmp=$EVIDENCE_ROOT/$connector/.latest-run-id.tmp-$$
umask 077
printf '%s\n' "$NO_CRS_RUN_ID" > "$latest_tmp"
mv -f "$latest_tmp" "$latest_file"
if [ "$stage_rc" -eq 77 ]; then
    exit 77
fi
if [ "$stage_rc" -ne 0 ]; then
    exit "$stage_rc"
fi
exit 0
