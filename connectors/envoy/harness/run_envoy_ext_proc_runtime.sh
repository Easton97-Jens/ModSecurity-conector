#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
CONNECTOR_DIR=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
REPO_ROOT=$(CDPATH= cd "$CONNECTOR_DIR/../.." && pwd)
BUILD_ROOT=${BUILD_ROOT:-${XDG_STATE_HOME:-${HOME:-/tmp}/.local/state}/ModSecurity-conector-build}
EXT_PROC_BIN=${EXT_PROC_BIN:-$BUILD_ROOT/envoy-ext-proc/msconnector_envoy_ext_proc}
EXT_PROC_CONFIG=${EXT_PROC_CONFIG:-$CONNECTOR_DIR/config/envoy-ext-proc-service.json}
RUNTIME_ROOT=${RUNTIME_ROOT:-$BUILD_ROOT/envoy-ext-proc/runtime-smoke}
COMMON_EVENT_LOG_PATH=${COMMON_EVENT_LOG_PATH:-${EVENT_LOG_PATH:-$RUNTIME_ROOT/events.jsonl}}
COMPLETION_LOG_PATH=${COMPLETION_LOG_PATH:-$RUNTIME_ROOT/completion-events.jsonl}
EXT_PROC_RUNTIME_CONFIG=${EXT_PROC_RUNTIME_CONFIG:-$RUNTIME_ROOT/envoy-ext-proc-runtime.conf}
# The canonical dispatcher exports MSCONNECTOR_RULES_FILE. Prefer it over an
# incidental make/environment RULES_FILE so this real-host runner cannot fall
# back to a connector-local smoke ruleset. Direct local invocation may still
# supply RULES_FILE, and otherwise uses the Framework's canonical baseline.
if [ -n "${MSCONNECTOR_RULES_FILE:-}" ]; then
    RULES_FILE=$MSCONNECTOR_RULES_FILE
    RULES_SOURCE=MSCONNECTOR_RULES_FILE
elif [ -n "${RULES_FILE:-}" ]; then
    RULES_SOURCE=RULES_FILE
else
    RULES_FILE=$REPO_ROOT/modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf
    RULES_SOURCE=framework_default
fi
PYTHON_BIN=${PYTHON:-python3}
HELPER="$SCRIPT_DIR/envoy_smoke_helper.py"
YAML_TEMPLATE="$CONNECTOR_DIR/config/envoy-ext-proc-streaming.yaml.in"
PREPARE_ENVOY_CONFIG="$CONNECTOR_DIR/config/prepare_envoy_ext_proc_config.sh"
PREPARE_RUNTIME_CONFIG="$CONNECTOR_DIR/config/prepare_envoy_ext_proc_runtime_config.sh"
VERSION_LOCK="$CONNECTOR_DIR/config/envoy-ext-proc-versions.env"
ENVOY_CONFIG="$RUNTIME_ROOT/envoy-ext-proc.streaming.yaml"
SUMMARY="$RUNTIME_ROOT/runtime-summary.txt"
ENVOY_STDOUT="$RUNTIME_ROOT/envoy.stdout.log"
ENVOY_STDERR="$RUNTIME_ROOT/envoy.stderr.log"
SERVICE_STDOUT="$RUNTIME_ROOT/ext-proc.stdout.log"
SERVICE_STDERR="$RUNTIME_ROOT/ext-proc.stderr.log"
UPSTREAM_STDOUT="$RUNTIME_ROOT/upstream.stdout.log"
UPSTREAM_STDERR="$RUNTIME_ROOT/upstream.stderr.log"
TRANSPORT_OBSERVATIONS="$RUNTIME_ROOT/transport-observations.diagnostic.json"
TRANSPORT_CANCEL_PROBE=${ENVOY_TRANSPORT_CANCEL_PROBE:-0}
TRANSPORT_CANCEL_ID=envoy-ext-proc-client-cancel-1
envoy_pid=
service_pid=
upstream_pid=

missing_dependency() {
    echo "envoy_ext_proc_runtime: BLOCKED - $1" >&2
    exit 77
}

cleanup() {
    for pid in "$envoy_pid" "$service_pid" "$upstream_pid"; do
        if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
            kill "$pid" 2>/dev/null || true
        fi
    done
    for pid in "$envoy_pid" "$service_pid" "$upstream_pid"; do
        if [ -n "$pid" ]; then
            set +e
            wait "$pid" 2>/dev/null
            set -e
        fi
    done
}
trap cleanup EXIT HUP INT TERM

[ -n "${ENVOY_BIN:-}" ] || missing_dependency "ENVOY_BIN is required"
[ -x "$ENVOY_BIN" ] || missing_dependency "ENVOY_BIN is not executable: $ENVOY_BIN"
[ -x "$EXT_PROC_BIN" ] || missing_dependency "ext_proc service is not executable: $EXT_PROC_BIN"
[ -f "$EXT_PROC_CONFIG" ] || missing_dependency "ext_proc service config is missing: $EXT_PROC_CONFIG"
[ -f "$YAML_TEMPLATE" ] || missing_dependency "Envoy ext_proc template is missing: $YAML_TEMPLATE"
[ -x "$PREPARE_ENVOY_CONFIG" ] || missing_dependency "Envoy ext_proc config materializer is missing: $PREPARE_ENVOY_CONFIG"
[ -f "$PREPARE_RUNTIME_CONFIG" ] || missing_dependency "Common runtime config materializer is missing: $PREPARE_RUNTIME_CONFIG"
[ -f "$VERSION_LOCK" ] || missing_dependency "Envoy ext_proc version lock is missing: $VERSION_LOCK"
[ -f "$HELPER" ] || missing_dependency "smoke helper is missing: $HELPER"
command -v "$PYTHON_BIN" >/dev/null 2>&1 || missing_dependency "Python interpreter is missing: $PYTHON_BIN"
[ -f "$RULES_FILE" ] || missing_dependency "canonical rules file is missing: $RULES_FILE"
resolved_rules_file=$("$PYTHON_BIN" -c 'import pathlib,sys; print(pathlib.Path(sys.argv[1]).resolve(strict=True))' "$RULES_FILE") || {
    echo "envoy_ext_proc_runtime: FAIL - could not resolve canonical rules file: $RULES_FILE" >&2
    exit 1
}

case "$RUNTIME_ROOT" in
    /*) ;;
    *) echo "envoy_ext_proc_runtime: FAIL - RUNTIME_ROOT must be absolute" >&2; exit 1 ;;
esac
case "$RUNTIME_ROOT" in
    "$REPO_ROOT"|"$REPO_ROOT"/*)
        echo "envoy_ext_proc_runtime: FAIL - RUNTIME_ROOT must not be inside the checkout" >&2
        exit 1
        ;;
esac
case "$COMMON_EVENT_LOG_PATH" in
    "$RUNTIME_ROOT"/*) ;;
    *) echo "envoy_ext_proc_runtime: FAIL - Common event log must be under RUNTIME_ROOT" >&2; exit 1 ;;
esac
case "$COMPLETION_LOG_PATH" in
    "$RUNTIME_ROOT"/*) ;;
    *) echo "envoy_ext_proc_runtime: FAIL - completion log must be under RUNTIME_ROOT" >&2; exit 1 ;;
esac
case "$EXT_PROC_RUNTIME_CONFIG" in
    "$RUNTIME_ROOT"/*) ;;
    *) echo "envoy_ext_proc_runtime: FAIL - EXT_PROC_RUNTIME_CONFIG must be under RUNTIME_ROOT" >&2; exit 1 ;;
esac
case "$TRANSPORT_OBSERVATIONS" in
    "$RUNTIME_ROOT"/*) ;;
    *) echo "envoy_ext_proc_runtime: FAIL - transport observations must be under RUNTIME_ROOT" >&2; exit 1 ;;
esac
case "$TRANSPORT_CANCEL_PROBE" in
    0|1) ;;
    *) echo "envoy_ext_proc_runtime: FAIL - ENVOY_TRANSPORT_CANCEL_PROBE must be 0 or 1" >&2; exit 1 ;;
esac
mkdir -p "$RUNTIME_ROOT"
rm -f "$COMMON_EVENT_LOG_PATH" "$COMPLETION_LOG_PATH" "$SUMMARY" "$EXT_PROC_RUNTIME_CONFIG" "$TRANSPORT_OBSERVATIONS"

pinned_envoy_release=$(sed -n 's/^ENVOY_RELEASE=//p' "$VERSION_LOCK")
[ -n "$pinned_envoy_release" ] || {
    echo "envoy_ext_proc_runtime: FAIL - version lock has no ENVOY_RELEASE" >&2
    exit 1
}
if ! "$ENVOY_BIN" --version >"$RUNTIME_ROOT/envoy-version.txt" 2>&1; then
    echo "envoy_ext_proc_runtime: FAIL - could not read Envoy version" >&2
    exit 1
fi
envoy_version=$(cat "$RUNTIME_ROOT/envoy-version.txt")
case "$envoy_version" in
    *"/$pinned_envoy_release/"*|*"version: $pinned_envoy_release"*) ;;
    *)
        echo "envoy_ext_proc_runtime: FAIL - Envoy does not match pinned $pinned_envoy_release" >&2
        sed -n '1,20p' "$RUNTIME_ROOT/envoy-version.txt" >&2 || true
        exit 1
        ;;
esac

set -- $("$PYTHON_BIN" "$HELPER" free-ports --count 4)
listen_port=${ENVOY_SMOKE_PORT:-$1}
upstream_port=${ENVOY_UPSTREAM_PORT:-$2}
ext_proc_port=${ENVOY_EXT_PROC_PORT:-$3}
admin_port=${ENVOY_ADMIN_PORT:-$4}
base_id=$(((listen_port + admin_port) % 100000))

OUTPUT_CONFIG="$ENVOY_CONFIG" LISTEN_PORT="$listen_port" \
    UPSTREAM_PORT="$upstream_port" EXT_PROC_PORT="$ext_proc_port" \
    ADMIN_PORT="$admin_port" TEMPLATE="$YAML_TEMPLATE" \
    sh "$PREPARE_ENVOY_CONFIG" >/dev/null
OUTPUT_CONFIG="$EXT_PROC_RUNTIME_CONFIG" RULES_FILE="$RULES_FILE" EVENT_PATH="$COMMON_EVENT_LOG_PATH" \
    sh "$PREPARE_RUNTIME_CONFIG" >/dev/null

if ! grep -Fq 'name: envoy.filters.http.ext_proc' "$ENVOY_CONFIG" || \
    grep -Fq 'name: envoy.filters.http.ext_authz' "$ENVOY_CONFIG" || \
    ! grep -Fq 'request_body_mode: STREAMED' "$ENVOY_CONFIG" || \
    ! grep -Fq 'response_body_mode: STREAMED' "$ENVOY_CONFIG" || \
    ! grep -Fq 'request_trailer_mode: SEND' "$ENVOY_CONFIG" || \
    ! grep -Fq 'response_trailer_mode: SEND' "$ENVOY_CONFIG" || \
    ! grep -Fq 'request_attributes:' "$ENVOY_CONFIG"; then
    echo "envoy_ext_proc_runtime: FAIL - generated config does not select streamed ext_proc only" >&2
    exit 1
fi
for required_attribute in request.protocol source.address source.port destination.address destination.port; do
    if ! grep -Fq "$required_attribute" "$ENVOY_CONFIG"; then
        echo "envoy_ext_proc_runtime: FAIL - generated config is missing required ext_proc attribute: $required_attribute" >&2
        exit 1
    fi
done

for required_setting in request_body_mode=streaming response_body_mode=streaming phase4_mode=safe; do
    if ! grep -Fqx "$required_setting" "$EXT_PROC_RUNTIME_CONFIG"; then
        echo "envoy_ext_proc_runtime: FAIL - generated Common runtime config is missing $required_setting" >&2
        exit 1
    fi
done
if ! grep -Fqx "event_path=$COMMON_EVENT_LOG_PATH" "$EXT_PROC_RUNTIME_CONFIG"; then
    echo "envoy_ext_proc_runtime: FAIL - Common runtime config does not select the run-local raw event log" >&2
    exit 1
fi
if ! grep -Fqx "rules_file=$resolved_rules_file" "$EXT_PROC_RUNTIME_CONFIG"; then
    echo "envoy_ext_proc_runtime: FAIL - Common runtime config did not load the canonical rules file" >&2
    exit 1
fi

"$EXT_PROC_BIN" --check-config --config "$EXT_PROC_CONFIG" \
    --runtime-config "$EXT_PROC_RUNTIME_CONFIG" \
    >"$RUNTIME_ROOT/ext-proc-config-check.stdout.log" \
    2>"$RUNTIME_ROOT/ext-proc-config-check.stderr.log"

if ! "$ENVOY_BIN" --mode validate -c "$ENVOY_CONFIG" \
    --base-id "$base_id" --disable-hot-restart >"$RUNTIME_ROOT/envoy-validate.stdout.log" \
    2>"$RUNTIME_ROOT/envoy-validate.stderr.log"; then
    echo "envoy_ext_proc_runtime: FAIL - Envoy rejected generated config" >&2
    sed -n '1,160p' "$RUNTIME_ROOT/envoy-validate.stderr.log" >&2 || true
    exit 1
fi

"$PYTHON_BIN" "$HELPER" serve-upstream --port "$upstream_port" \
    --client-cancel-delay "${ENVOY_CLIENT_CANCEL_DELAY_SECONDS:-5}" \
    >"$UPSTREAM_STDOUT" 2>"$UPSTREAM_STDERR" &
upstream_pid=$!

EXT_PROC_BIN="$EXT_PROC_BIN" EXT_PROC_CONFIG="$EXT_PROC_CONFIG" \
    EXT_PROC_RUNTIME_CONFIG="$EXT_PROC_RUNTIME_CONFIG" \
    EVENT_LOG_PATH="$COMPLETION_LOG_PATH" LISTEN_ADDRESS=127.0.0.1 \
    LISTEN_PORT="$ext_proc_port" sh "$SCRIPT_DIR/serve_envoy_ext_proc.sh" \
    >"$SERVICE_STDOUT" 2>"$SERVICE_STDERR" &
service_pid=$!

"$ENVOY_BIN" -c "$ENVOY_CONFIG" --base-id "$base_id" --disable-hot-restart \
    --log-level error >"$ENVOY_STDOUT" 2>"$ENVOY_STDERR" &
envoy_pid=$!

allowed_status=
attempt=0
while [ "$attempt" -lt 30 ]; do
    attempt=$((attempt + 1))
    for process_pair in "envoy:$envoy_pid" "ext_proc:$service_pid" "upstream:$upstream_pid"; do
        process_name=${process_pair%%:*}
        process_id=${process_pair##*:}
        if ! kill -0 "$process_id" 2>/dev/null; then
            echo "envoy_ext_proc_runtime: FAIL - $process_name process exited early" >&2
            sed -n '1,160p' "$ENVOY_STDERR" >&2 || true
            sed -n '1,160p' "$SERVICE_STDERR" >&2 || true
            exit 1
        fi
    done
    set +e
    allowed_status=$("$PYTHON_BIN" "$HELPER" probe \
        --url "http://127.0.0.1:$listen_port/allowed" \
        --header "X-Request-Id: envoy-ext-proc-allow-1" 2>/dev/null)
    probe_rc=$?
    set -e
    if [ "$probe_rc" -eq 0 ] && [ "$allowed_status" = "200" ]; then
        break
    fi
    sleep 1
done

if [ "$allowed_status" != "200" ]; then
    echo "envoy_ext_proc_runtime: FAIL - allowed request returned ${allowed_status:-no status}, expected 200" >&2
    exit 1
fi

if ! streamed_status=$("$PYTHON_BIN" "$HELPER" probe \
    --url "http://127.0.0.1:$listen_port/streamed" --method POST \
    --data "request-body-for-ext-proc" \
    --header "X-Request-Id: envoy-ext-proc-stream-1"); then
    echo "envoy_ext_proc_runtime: FAIL - streamed request could not be completed" >&2
    exit 1
fi
if [ "$streamed_status" != "200" ]; then
    echo "envoy_ext_proc_runtime: FAIL - streamed request returned $streamed_status, expected 200" >&2
    exit 1
fi

if ! phase1_deny_status=$("$PYTHON_BIN" "$HELPER" probe \
    --url "http://127.0.0.1:$listen_port/phase1-deny" \
    --header "X-Request-Id: envoy-ext-proc-phase1-deny" \
    --header "X-Modsec-Smoke: block"); then
    echo "envoy_ext_proc_runtime: FAIL - phase-1 deny probe could not be completed" >&2
    exit 1
fi
if [ "$phase1_deny_status" != "403" ]; then
    echo "envoy_ext_proc_runtime: FAIL - phase-1 deny returned $phase1_deny_status, expected 403" >&2
    exit 1
fi

if ! phase2_deny_status=$("$PYTHON_BIN" "$HELPER" probe \
    --url "http://127.0.0.1:$listen_port/phase2-deny" --method POST \
    --data "no-crs-request-body-marker" \
    --header "X-Request-Id: envoy-ext-proc-phase2-deny"); then
    echo "envoy_ext_proc_runtime: FAIL - phase-2 deny probe could not be completed" >&2
    exit 1
fi
if [ "$phase2_deny_status" != "403" ]; then
    echo "envoy_ext_proc_runtime: FAIL - phase-2 deny returned $phase2_deny_status, expected 403" >&2
    exit 1
fi

if ! phase3_deny_status=$("$PYTHON_BIN" "$HELPER" probe \
    --url "http://127.0.0.1:$listen_port/phase3-block" \
    --header "X-Request-Id: envoy-ext-proc-phase3-deny"); then
    echo "envoy_ext_proc_runtime: FAIL - phase-3 deny probe could not be completed" >&2
    exit 1
fi
if [ "$phase3_deny_status" != "403" ]; then
    echo "envoy_ext_proc_runtime: FAIL - phase-3 deny returned $phase3_deny_status, expected 403" >&2
    exit 1
fi

if ! phase3_redirect_status=$("$PYTHON_BIN" "$HELPER" probe \
    --url "http://127.0.0.1:$listen_port/phase3-redirect" --no-redirect \
    --header "X-Request-Id: envoy-ext-proc-phase3-redirect"); then
    echo "envoy_ext_proc_runtime: FAIL - phase-3 redirect probe could not be completed" >&2
    exit 1
fi
if [ "$phase3_redirect_status" != "302" ]; then
    echo "envoy_ext_proc_runtime: FAIL - phase-3 redirect returned $phase3_redirect_status, expected 302" >&2
    exit 1
fi

if ! phase4_safe_status=$("$PYTHON_BIN" "$HELPER" probe \
    --url "http://127.0.0.1:$listen_port/phase4-marker" \
    --header "X-Request-Id: envoy-ext-proc-phase4-safe"); then
    echo "envoy_ext_proc_runtime: FAIL - phase-4 safe probe could not be completed" >&2
    exit 1
fi
if [ "$phase4_safe_status" != "200" ]; then
    echo "envoy_ext_proc_runtime: FAIL - phase-4 safe mode returned $phase4_safe_status, expected 200" >&2
    exit 1
fi

event_ready=0
attempt=0
while [ "$attempt" -lt 20 ]; do
    attempt=$((attempt + 1))
    if [ -s "$COMPLETION_LOG_PATH" ] && \
        grep -Fq '"transaction_id":"envoy-ext-proc-stream-1"' "$COMPLETION_LOG_PATH" && \
        grep -Fq '"integration_mode":"ext_proc"' "$COMPLETION_LOG_PATH" && \
        grep -Fq '"evaluation_mode":"common_libmodsecurity_nonpromoted"' "$COMPLETION_LOG_PATH" && \
        grep -Fq '"rule_evaluation":"libmodsecurity"' "$COMPLETION_LOG_PATH" && \
        grep -Eq '"request_body_bytes":[1-9][0-9]*' "$COMPLETION_LOG_PATH" && \
        grep -Eq '"response_body_bytes":[1-9][0-9]*' "$COMPLETION_LOG_PATH"; then
        event_ready=1
        break
    fi
    sleep 1
done
if [ "$event_ready" -ne 1 ]; then
    echo "envoy_ext_proc_runtime: FAIL - missing streamed ext_proc metadata evidence" >&2
    sed -n '1,80p' "$COMPLETION_LOG_PATH" >&2 || true
    exit 1
fi
if grep -Fq 'request-body-for-ext-proc' "$COMPLETION_LOG_PATH" || \
    grep -Fq 'envoy connector upstream ok' "$COMPLETION_LOG_PATH" || \
    grep -Fq 'no-crs-request-body-marker' "$COMPLETION_LOG_PATH" || \
    grep -Fq 'no-crs-response-body-marker' "$COMPLETION_LOG_PATH"; then
    echo "envoy_ext_proc_runtime: FAIL - metadata evidence contains a body payload" >&2
    exit 1
fi

raw_event_ready=0
attempt=0
while [ "$attempt" -lt 20 ]; do
    attempt=$((attempt + 1))
    if [ -s "$COMMON_EVENT_LOG_PATH" ] && \
        grep -Fq '"connector":"envoy"' "$COMMON_EVENT_LOG_PATH" && \
        grep -Fq '"integration_mode":"ext_proc"' "$COMMON_EVENT_LOG_PATH" && \
        grep -Fq '"rule_id":"1100001"' "$COMMON_EVENT_LOG_PATH" && \
        grep -Fq '"rule_id":"1100101"' "$COMMON_EVENT_LOG_PATH" && \
        grep -Fq '"rule_id":"1100201"' "$COMMON_EVENT_LOG_PATH" && \
        grep -Fq '"rule_id":"1100202"' "$COMMON_EVENT_LOG_PATH" && \
        grep -Fq '"rule_id":"1100301"' "$COMMON_EVENT_LOG_PATH" && \
        grep -Fq '"transport_result":"http_status"' "$COMMON_EVENT_LOG_PATH" && \
        grep -Fq '"transport_result":"log_only"' "$COMMON_EVENT_LOG_PATH" && \
        grep -Fq '"actual_action":"log_only"' "$COMMON_EVENT_LOG_PATH"; then
        raw_event_ready=1
        break
    fi
    sleep 1
done
if [ "$raw_event_ready" -ne 1 ]; then
    echo "envoy_ext_proc_runtime: FAIL - missing Common/libmodsecurity raw decision evidence" >&2
    sed -n '1,160p' "$COMMON_EVENT_LOG_PATH" >&2 || true
    exit 1
fi
if grep -Fq 'request-body-for-ext-proc' "$COMMON_EVENT_LOG_PATH" || \
    grep -Fq 'envoy connector upstream ok' "$COMMON_EVENT_LOG_PATH" || \
    grep -Fq 'no-crs-request-body-marker' "$COMMON_EVENT_LOG_PATH" || \
    grep -Fq 'no-crs-response-body-marker' "$COMMON_EVENT_LOG_PATH"; then
    echo "envoy_ext_proc_runtime: FAIL - Common raw event evidence contains a body payload" >&2
    exit 1
fi
for process_pair in "envoy:$envoy_pid" "ext_proc:$service_pid" "upstream:$upstream_pid"; do
    process_name=${process_pair%%:*}
    process_id=${process_pair##*:}
    if ! kill -0 "$process_id" 2>/dev/null; then
        echo "envoy_ext_proc_runtime: FAIL - $process_name was not stable after requests" >&2
        exit 1
    fi
done

# Envoy's ext_proc gRPC cancellation is explicitly opt-in because it is a
# longer-running transport probe, not a normal PR smoke.  The real client
# closes only after it receives a response body byte.  The service can prove
# one cleanup record but must retain its documented inability to attribute the
# gRPC cancellation to a specific downstream reset cause.
cancel_client_result=NOT_EXECUTED
cancel_transport_result=not_executed
cancel_completion_reason=NOT_EXECUTED
cancel_first_byte_received=false
cancel_followup_result=not_executed
if [ "$TRANSPORT_CANCEL_PROBE" = 1 ]; then
    if ! cancel_observation=$("$PYTHON_BIN" "$HELPER" client-cancel \
        --host 127.0.0.1 --port "$listen_port" --path /client-cancel \
        --header "X-Request-Id: $TRANSPORT_CANCEL_ID"); then
        echo "envoy_ext_proc_runtime: FAIL - client-cancel probe could not receive the first response byte" >&2
        exit 1
    fi
    cancel_status=$("$PYTHON_BIN" -c 'import json,sys; print(json.loads(sys.argv[1])["http_status"])' "$cancel_observation") || {
        echo "envoy_ext_proc_runtime: FAIL - client-cancel observation is malformed" >&2
        exit 1
    }
    cancel_first_byte=$("$PYTHON_BIN" -c 'import json,sys; print(str(bool(json.loads(sys.argv[1])["first_body_byte_received"])).lower())' "$cancel_observation") || {
        echo "envoy_ext_proc_runtime: FAIL - client-cancel observation has no first-byte result" >&2
        exit 1
    }
    if [ "$cancel_status" != 200 ] || [ "$cancel_first_byte" != true ]; then
        echo "envoy_ext_proc_runtime: FAIL - client-cancel probe did not observe HTTP 200 plus one body byte" >&2
        exit 1
    fi
    cancel_ready=0
    attempt=0
    while [ "$attempt" -lt 20 ]; do
        attempt=$((attempt + 1))
        cancel_completion_state=$("$PYTHON_BIN" - "$COMPLETION_LOG_PATH" "$TRANSPORT_CANCEL_ID" <<'PY'
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
transaction_id = sys.argv[2]
records = []
if path.is_file():
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict) and value.get("transaction_id") == transaction_id:
            records.append(value)
if len(records) != 1:
    print(f"count={len(records)}")
elif records[0].get("close_reason") not in {
    "grpc_context_canceled_unattributed",
    "grpc_peer_eof",
}:
    print("reason=" + str(records[0].get("close_reason")))
else:
    print("valid=" + str(records[0].get("close_reason")))
PY
) || cancel_completion_state=invalid
        case "$cancel_completion_state" in
            valid=grpc_context_canceled_unattributed|valid=grpc_peer_eof)
                cancel_completion_reason=${cancel_completion_state#valid=}
                cancel_ready=1
                break
                ;;
        esac
        sleep 1
    done
    if [ "$cancel_ready" -ne 1 ]; then
        echo "envoy_ext_proc_runtime: FAIL - expected exactly one unattributed ext_proc terminal completion, got ${cancel_completion_state:-missing}" >&2
        exit 1
    fi
    cancel_client_result=client_closed_after_first_response_chunk
    cancel_transport_result=client_cancelled
    cancel_first_byte_received=true
    if ! cancel_followup_status=$("$PYTHON_BIN" "$HELPER" probe \
        --url "http://127.0.0.1:$listen_port/allowed" \
        --header "X-Request-Id: envoy-ext-proc-client-cancel-followup"); then
        echo "envoy_ext_proc_runtime: FAIL - follow-up request after client cancel could not be completed" >&2
        exit 1
    fi
    if [ "$cancel_followup_status" != 200 ]; then
        echo "envoy_ext_proc_runtime: FAIL - follow-up request after client cancel returned $cancel_followup_status, expected 200" >&2
        exit 1
    fi
    cancel_followup_result=completed
fi

host_survived=true
for process_pair in "envoy:$envoy_pid" "ext_proc:$service_pid" "upstream:$upstream_pid"; do
    process_name=${process_pair%%:*}
    process_id=${process_pair##*:}
    if ! kill -0 "$process_id" 2>/dev/null; then
        host_survived=false
        echo "envoy_ext_proc_runtime: FAIL - $process_name was not stable after transport observation" >&2
        exit 1
    fi
done
"$PYTHON_BIN" - "$TRANSPORT_OBSERVATIONS" "$TRANSPORT_CANCEL_PROBE" \
    "$cancel_client_result" "$cancel_transport_result" "$cancel_completion_reason" \
    "$cancel_first_byte_received" "$host_survived" "$cancel_followup_result" <<'PY'
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
executed = sys.argv[2] == "1"
payload = {
    "artifact_profile": "ext-proc-transport-diagnostic-nonpromoting",
    "capability_promotion": "not_permitted",
    "canonical_evidence": False,
    "causal_attribution": "ext_proc completion is intentionally unattributed; no downstream reset cause is claimed",
    "client_result": sys.argv[3],
    "connector": "envoy",
    "diagnostic_case": "client_disconnect_after_first_response_chunk",
    "diagnostic_only": True,
    "eos_received": False,
    "execution": "EXECUTED" if executed else "NOT_EXECUTED",
    "first_byte_received": sys.argv[6] == "true",
    "followup_request_result": sys.argv[8],
    "host_survived": sys.argv[7] == "true",
    "integration_mode": "ext_proc",
    "processor_completion_reason": sys.argv[5],
    "protocol": "http1",
    "response_committed": executed,
    "schema_version": 1,
    "strict": {
        "client_visible_abort": False,
        "reason": "ext_proc has no verified post-commit downstream reset API; gRPC failures are not reset evidence.",
        "state": "NOT_EXECUTED",
    },
    "transport_result": sys.argv[4],
}
path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY

{
    printf 'status=PASS\n'
    printf 'connector=envoy\n'
    printf 'integration_mode=ext_proc\n'
    printf 'envoy_release=%s\n' "$pinned_envoy_release"
    printf 'evaluation_mode=common_libmodsecurity_nonpromoted\n'
    printf 'rule_evaluation=libmodsecurity\n'
    printf 'common_runtime_bridge=true\n'
    printf 'capability_promotion=not_permitted\n'
    printf 'allowed_request_status=%s\n' "$allowed_status"
    printf 'streamed_request_status=%s\n' "$streamed_status"
    printf 'phase1_deny_status=%s\n' "$phase1_deny_status"
    printf 'phase2_deny_status=%s\n' "$phase2_deny_status"
    printf 'phase3_deny_status=%s\n' "$phase3_deny_status"
    printf 'phase3_redirect_status=%s\n' "$phase3_redirect_status"
    printf 'phase4_safe_status=%s\n' "$phase4_safe_status"
    printf 'request_body_stream_observed=true\n'
    printf 'response_body_stream_observed=true\n'
    printf 'transport_cancel_probe=%s\n' "$TRANSPORT_CANCEL_PROBE"
    printf 'transport_cancel_client_result=%s\n' "$cancel_client_result"
    printf 'transport_cancel_completion_reason=%s\n' "$cancel_completion_reason"
    printf 'transport_cancel_followup_result=%s\n' "$cancel_followup_result"
    printf 'transport_observations=%s\n' "$TRANSPORT_OBSERVATIONS"
    printf 'event_log=%s\n' "$COMMON_EVENT_LOG_PATH"
    printf 'completion_log=%s\n' "$COMPLETION_LOG_PATH"
    printf 'envoy_config=%s\n' "$ENVOY_CONFIG"
    printf 'common_runtime_config=%s\n' "$EXT_PROC_RUNTIME_CONFIG"
    printf 'rules_file=%s\n' "$resolved_rules_file"
    printf 'rules_source=%s\n' "$RULES_SOURCE"
    printf 'response_body_rule_evaluation=raw_common_event_and_host_safe_log_only\n'
    printf 'production_ready=false\n'
} > "$SUMMARY"

cleanup
envoy_pid=
service_pid=
upstream_pid=
trap - EXIT HUP INT TERM
printf 'processes_stopped=yes\n' >> "$SUMMARY"
printf 'envoy_ext_proc_runtime: pass (non-promoted) summary=%s\n' "$SUMMARY"
