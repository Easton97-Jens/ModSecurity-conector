#!/bin/sh
set -eu

connector=${1:?connector is required}
evidence_stage=${2:-no_crs_baseline}
SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
CONNECTOR_ROOT=${CONNECTOR_ROOT:-$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)}
FRAMEWORK_ROOT=${FRAMEWORK_ROOT:-$CONNECTOR_ROOT/modules/ModSecurity-test-Framework}
PYTHON=${PYTHON:-python3}
VERIFIED_RUN_ROOT=${VERIFIED_RUN_ROOT:-${RUNNER_TEMP:-${TMPDIR:-/var/tmp}}/ModSecurity-conector-verified}
BUILD_ROOT=${BUILD_ROOT:-$VERIFIED_RUN_ROOT/build}
EVIDENCE_ROOT=${EVIDENCE_ROOT:-$BUILD_ROOT/no-crs-evidence}
NO_CRS_RUN_ID=${NO_CRS_RUN_ID:-$(date -u +%Y-%m-%dT%H-%M-%SZ)-$(git -C "$CONNECTOR_ROOT" rev-parse --short=8 HEAD 2>/dev/null || printf unknown)}
NO_CRS_RULES_FILE=${NO_CRS_RULES_FILE:-$FRAMEWORK_ROOT/tests/rules/no-crs-baseline.conf}
NO_CRS_RAW_ROOT=${NO_CRS_RAW_ROOT:-$BUILD_ROOT/canonical-raw/$evidence_stage}
NO_CRS_ARTIFACT_PROFILE=${NO_CRS_ARTIFACT_PROFILE:-generic}
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
case "$EVIDENCE_ROOT:$NO_CRS_RAW_ROOT" in
    /*:/*) ;;
    *) echo "BLOCKED: evidence roots must be absolute" >&2; exit 77 ;;
esac
if ! EVIDENCE_ROOT=$("$PYTHON" -c 'import os,sys; print(os.path.abspath(sys.argv[1]))' "$EVIDENCE_ROOT") ||
   ! NO_CRS_RAW_ROOT=$("$PYTHON" -c 'import os,sys; print(os.path.abspath(sys.argv[1]))' "$NO_CRS_RAW_ROOT"); then
    echo "BLOCKED: Python is required to normalize evidence roots" >&2
    exit 77
fi

CAPABILITIES_FILE=$CONNECTOR_ROOT/connectors/$connector/capabilities.json
RUN_DIR=$EVIDENCE_ROOT/$connector/$NO_CRS_RUN_ID
RAW_DIR=$NO_CRS_RAW_ROOT/$connector/$NO_CRS_RUN_ID
LOG_DIR=$RAW_DIR/logs
RESULTS_DIR=$RAW_DIR/results
HOST_RUNTIME_ROOT=$RESULTS_DIR/host-runtime
HOST_LOG_ROOT=$RAW_DIR/host-logs
HOST_TMP_ROOT=$RAW_DIR/tmp
NGINX_RUN_ROOT=$RAW_DIR/nginx-harness
TRAEFIK_RUNTIME_ROOT=$RESULTS_DIR/traefik-runtime
LIGHTTPD_RUNTIME_ROOT=$RESULTS_DIR/lighttpd-runtime
PLAN=$RAW_DIR/plan.json
SOURCE_RESULT=$RAW_DIR/source-result.json
NORMALIZED_EVENTS=$RAW_DIR/events.normalized.jsonl
SOURCE_EVENT_SCRUB_LOG=$LOG_DIR/source-event-scrub.log
CANONICAL_STDOUT_LOG=$LOG_DIR/stdout.canonical.log
CANONICAL_STDERR_LOG=$LOG_DIR/stderr.canonical.log
CANONICAL_HOST_LOG=$LOG_DIR/host.canonical.log
LOG_SANITIZER=$CONNECTOR_ROOT/ci/sanitize-full-lifecycle-log.py
SYNCHRONIZED_UPSTREAM=$FRAMEWORK_ROOT/tests/runners/synchronized_upstream.py
FIRST_BYTE_EVIDENCE=$RAW_DIR/first-byte-evidence.json
FIRST_BYTE_EVIDENCE_SOURCE=${FIRST_BYTE_EVIDENCE_SOURCE:-}

[ -f "$FRAMEWORK_ROOT/ci/no_crs_baseline.py" ] || {
    echo "BLOCKED: canonical framework runner is missing: $FRAMEWORK_ROOT/ci/no_crs_baseline.py" >&2
    exit 77
}
[ -f "$LOG_SANITIZER" ] || {
    echo "FAIL: canonical log sanitizer is missing: $LOG_SANITIZER" >&2
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
[ -f "$NO_CRS_RULES_FILE" ] || {
    echo "FAIL: canonical no-CRS rules are missing: $NO_CRS_RULES_FILE" >&2
    exit 1
}
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
if [ -e "$RUN_DIR" ] || [ -L "$RUN_DIR" ]; then
    echo "FAIL: canonical run directory already exists; choose a fresh run id: $RUN_DIR" >&2
    exit 1
fi
if [ -e "$RAW_DIR" ] || [ -L "$RAW_DIR" ]; then
    echo "FAIL: raw evidence directory already exists; choose a fresh run id: $RAW_DIR" >&2
    exit 1
fi

mkdir -p "$RAW_DIR" "$LOG_DIR" "$RESULTS_DIR"

"$PYTHON" "$FRAMEWORK_ROOT/ci/no_crs_baseline.py" select \
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
case " $NO_CRS_SELECTED_CASES " in
    *" allow_without_marker.yaml "*) ;;
    *) echo "FAIL: canonical plan does not select mandatory allow runner case" >&2; exit 1 ;;
esac
case " $NO_CRS_SELECTED_CASES " in
    *" deny_header_marker_403.yaml "*) ;;
    *) echo "FAIL: canonical plan does not select mandatory deny runner case" >&2; exit 1 ;;
esac

"$PYTHON" "$FRAMEWORK_ROOT/ci/no_crs_baseline.py" init \
    --connector "$connector" \
    --capabilities "$CAPABILITIES_FILE" \
    --plan "$PLAN" \
    --run-dir "$RUN_DIR" \
    --connector-root "$CONNECTOR_ROOT" \
    --run-id "$NO_CRS_RUN_ID" \
    --evidence-stage "$evidence_stage" \
    --artifact-profile "$NO_CRS_ARTIFACT_PROFILE" \
    --executed-target "$([ "$evidence_stage" = no_crs_baseline ] && printf no-crs-baseline || printf runtime-smoke)-$connector" \
    --host-version not_provisioned \
    --libmodsecurity-version not_provisioned

started_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)
set +e
CONNECTOR_ROOT="$CONNECTOR_ROOT" \
FRAMEWORK_ROOT="$FRAMEWORK_ROOT" \
VERIFIED_RUN_ROOT="$VERIFIED_RUN_ROOT" \
BUILD_ROOT="$BUILD_ROOT" \
TMP_ROOT="$HOST_TMP_ROOT" \
LOG_ROOT="$HOST_LOG_ROOT" \
RESULTS_DIR="$RESULTS_DIR" \
RUNTIME_ROOT="$HOST_RUNTIME_ROOT" \
RUNTIME_BASE="$HOST_RUNTIME_ROOT" \
APACHE_RUNTIME_LOG_DIR="$HOST_LOG_ROOT/apache-runtime" \
NGINX_HARNESS_PARENT="$RAW_DIR" \
NGINX_HARNESS_WORK_ROOT="$NGINX_RUN_ROOT" \
RUNTIME_EVENT_LOG_PATH="$HOST_RUNTIME_ROOT/events.jsonl" \
TRAEFIK_CONNECTOR_RESULT_ROOT="$TRAEFIK_RUNTIME_ROOT" \
LIGHTTPD_SMOKE_DIR="$LIGHTTPD_RUNTIME_ROOT" \
RULES_FILE="$NO_CRS_RULES_FILE" \
MSCONNECTOR_RULES_FILE="$NO_CRS_RULES_FILE" \
NO_CRS_RULES_FILE="$NO_CRS_RULES_FILE" \
NO_CRS_SELECTED_CASES="$NO_CRS_SELECTED_CASES" \
NO_CRS_SELECTED_CASE_IDS="$NO_CRS_SELECTED_CASE_IDS" \
NO_CRS_ARTIFACT_PROFILE="$NO_CRS_ARTIFACT_PROFILE" \
FULL_LIFECYCLE_EVIDENCE_OUTPUT="$FIRST_BYTE_EVIDENCE" \
MSCONNECTOR_EXPECTED_RULE_ID="$EXPECTED_RULE_ID" \
NO_CRS_RUN_ID="$NO_CRS_RUN_ID" \
sh "$CONNECTOR_ROOT/ci/run-connector-stage.sh" "$connector" "$evidence_stage" \
    >"$LOG_DIR/stdout.log" 2>"$LOG_DIR/stderr.log"
stage_rc=$?
set -e
ended_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)
PROCESS_CLEANUP_LOG=$LOG_DIR/process-cleanup.log
if ps -eo pid=,comm=,args= | MSCONNECTOR_PROCESS_ROOT="$VERIFIED_RUN_ROOT" awk '
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

# Apache and NGINX have native proxy/filter paths.  Run their additional
# synchronized upstream proof separately from the ordinary case runner so the
# client can be observed while the upstream is deliberately paused.  Other
# connectors retain a diagnostic-only synthetic barrier until their selected
# full-lifecycle host integration exists.
if [ "$NO_CRS_ARTIFACT_PROFILE" = full_lifecycle ]; then
    case "$connector" in
        apache|nginx)
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
            sh "$CONNECTOR_ROOT/ci/run-native-first-byte.sh" "$connector" || native_first_byte_rc=$?
            if [ "$native_first_byte_rc" -ne 0 ]; then
                stage_rc=$native_first_byte_rc
            fi
            ;;
    esac
fi

source_results=
source_result=
source_events=
source_first_byte_results=$RESULTS_DIR/$connector-first-byte-results.jsonl
case "$connector" in
    apache|nginx|haproxy)
        source_results=$RESULTS_DIR/$connector-results.jsonl
        source_result=$RESULTS_DIR/$connector-summary.json
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
"$PYTHON" "$CONNECTOR_ROOT/ci/collect-no-crs-source.py" "$@"

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
runtime_env=$VERIFIED_RUN_ROOT/component-cache/runtime-env.sh
if [ -f "$runtime_env" ]; then
    reject_symlink_components "$runtime_env"
    # Generated by the trusted component provisioner and restricted to export
    # statements with shell-quoted local runtime paths.
    # shellcheck disable=SC1090
    . "$runtime_env"
fi
case "$connector" in
    apache) host_binary=${APACHE_HTTPD:-$BUILD_ROOT/apache-runtime/httpd/bin/httpd} ;;
    nginx) host_binary=${MRTS_NATIVE_NGINX_BIN:-$BUILD_ROOT/nginx-runtime/nginx/sbin/nginx} ;;
    haproxy) host_binary=${HAPROXY_BIN:-$BUILD_ROOT/haproxy-runtime/haproxy/sbin/haproxy} ;;
    envoy) host_binary=$VERIFIED_RUN_ROOT/component-cache/envoy/bin/envoy ;;
    traefik) host_binary=$VERIFIED_RUN_ROOT/component-cache/traefik/bin/traefik ;;
    lighttpd) host_binary=$VERIFIED_RUN_ROOT/component-cache/lighttpd/bin/lighttpd ;;
esac
if [ -x "$host_binary" ]; then
    case "$connector" in
        apache) host_version=$($host_binary -v 2>&1 | sed -n '/./{p;q;}') ;;
        nginx) host_version=$($host_binary -v 2>&1 | sed -n '/./{p;q;}') ;;
        haproxy) host_version=$($host_binary -v 2>&1 | sed -n '/./{p;q;}') ;;
        envoy) host_version=$($host_binary --version 2>&1 | sed -n '/./{p;q;}') ;;
        traefik) host_version=$($host_binary version 2>&1 | sed -n '/./{p;q;}') ;;
        lighttpd) host_version=$($host_binary -v 2>&1 | sed -n '/./{p;q;}') ;;
    esac
fi
[ -n "$host_version" ] || host_version=unknown

libmodsecurity_version=not_provisioned
component_manifest=$VERIFIED_RUN_ROOT/component-cache/manifest.json
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
if [ "$NO_CRS_ARTIFACT_PROFILE" = full_lifecycle ] || [ -s "$NORMALIZED_EVENTS" ]; then
    set -- "$@" --source-events "$NORMALIZED_EVENTS"
fi
if [ "$NO_CRS_ARTIFACT_PROFILE" = full_lifecycle ]; then
    set -- "$@" --host-log "$CANONICAL_HOST_LOG" \
        --first-byte-evidence "$FIRST_BYTE_EVIDENCE"
fi

set +e
"$PYTHON" "$FRAMEWORK_ROOT/ci/no_crs_baseline.py" "$@"
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
