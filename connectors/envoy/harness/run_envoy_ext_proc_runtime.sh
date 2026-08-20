#!/bin/sh
set -eu

SCRIPT_DIR=$(
    CDPATH=
    export CDPATH
    cd "$(dirname "$0")" && pwd
)
CONNECTOR_DIR=$(
    CDPATH=
    export CDPATH
    cd "$SCRIPT_DIR/.." && pwd
)
REPO_ROOT=$(
    CDPATH=
    export CDPATH
    cd "$CONNECTOR_DIR/../.." && pwd
)
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
MSCONNECTOR_MRTS_RUNTIME=${MSCONNECTOR_MRTS_RUNTIME:-0}
if [ "$MSCONNECTOR_MRTS_RUNTIME" = 1 ]; then
    # MRTS mode must never inherit the canonical no-CRS smoke rules or an
    # incidental RULES_FILE from the caller.
    RULES_FILE=${MRTS_LOAD_FILE:-}
    RULES_SOURCE=MRTS_LOAD_FILE
elif [ -n "${MSCONNECTOR_RULES_FILE:-}" ]; then
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
TLS_RENDERER="$CONNECTOR_DIR/config/lib/tls_yaml_render.sh"
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
FULL_LIFECYCLE_EVIDENCE_OUTPUT=${FULL_LIFECYCLE_EVIDENCE_OUTPUT:-}
PHASE4_BARRIER_DIR="$RUNTIME_ROOT/phase4-first-byte-barrier"
PHASE4_BARRIER_OBSERVATION="$RUNTIME_ROOT/phase4-first-byte-observation.json"
PHASE4_BARRIER_TIMEOUT=${ENVOY_PHASE4_BARRIER_TIMEOUT_SECONDS:-10}
CHILD_STOP_ATTEMPTS=${ENVOY_CHILD_STOP_ATTEMPTS:-20}
CHILD_STOP_DELAY=${ENVOY_CHILD_STOP_DELAY_SECONDS:-0.1}
PHASE4_BARRIER_TRANSACTION_ID=envoy-ext-proc-phase4-safe
READINESS_TRANSACTION_ID=envoy-ext-proc-readiness-1
ALLOW_TRANSACTION_ID=envoy-ext-proc-allow-1
CRS_RUNTIME=${MSCONNECTOR_CRS_RUNTIME:-0}
CRS_RUNTIME_RUN_ID=${CRS_RUNTIME_RUN_ID:-}
CRS_ALLOW_TRANSACTION_ID=envoy-ext-proc-crs-allow-1
CRS_BLOCK_TRANSACTION_ID=envoy-ext-proc-crs-block-1
CRS_BYPASS_TRANSACTION_ID=envoy-ext-proc-crs-bypass-1
CRS_ALLOW_PROBE_EVIDENCE="$RUNTIME_ROOT/crs-allow-probe.json"
CRS_BLOCK_PROBE_EVIDENCE="$RUNTIME_ROOT/crs-block-probe.json"
CRS_BYPASS_PROBE_EVIDENCE="$RUNTIME_ROOT/crs-bypass-probe.json"
readonly ENVIRONMENT_LOG_LINES='1,160p'
readonly NO_CRS_REQUEST_BODY_MARKER=no-crs-request-body-marker
READINESS_PROBE_EVIDENCE="$RUNTIME_ROOT/readiness-probe.json"
ALLOW_PROBE_EVIDENCE="$RUNTIME_ROOT/allow-probe.json"
TLS_CERTIFICATE="$RUNTIME_ROOT/envoy-loopback.crt"
TLS_PRIVATE_KEY="$RUNTIME_ROOT/envoy-loopback.key"
envoy_pid=
service_pid=
upstream_pid=
envoy_start_token=
service_start_token=
upstream_start_token=

print_runtime_log() {
    log_path=$1
    if [ -f "$log_path" ] && [ ! -L "$log_path" ] &&
        ! sed -n "$ENVIRONMENT_LOG_LINES" "$log_path" >&2; then
        echo "envoy_ext_proc_runtime: diagnostic log could not be read: $log_path" >&2
    fi
}

missing_dependency() {
    reason=$1
    echo "envoy_ext_proc_runtime: BLOCKED - $reason" >&2
    exit 77
}

cleanup() {
    cleanup_status=0
    for process_spec in \
        "envoy:$envoy_pid:$envoy_start_token" \
        "ext_proc:$service_pid:$service_start_token" \
        "upstream:$upstream_pid:$upstream_start_token"; do
        process_label=${process_spec%%:*}
        process_rest=${process_spec#*:}
        process_pid=${process_rest%%:*}
        process_token=${process_rest#*:}
        if [ -n "$process_pid" ] && ! stop_owned_process "$process_pid" "$process_token" "$process_label"; then
            cleanup_status=1
        fi
    done
    rm -f "$TLS_CERTIFICATE" "$TLS_PRIVATE_KEY"
    return "$cleanup_status"
}

owned_process_start_token() {
    owned_pid=$1
    case "$owned_pid" in
        ''|*[!0-9]*) return 1 ;;
        *) ;;
    esac
    [ -r "/proc/$owned_pid/stat" ] || return 1
    owned_token=$(owned_process_stat_value "$owned_pid" starttime) || return 1
    case "$owned_token" in
        ''|*[!0-9]*) return 1 ;;
        *) ;;
    esac
    printf '%s\n' "$owned_token"
}

owned_process_stat_value() {
    owned_pid=$1
    owned_field=$2
    "$PYTHON_BIN" - "$owned_pid" "$owned_field" <<'PY'
import pathlib
import sys

pid, field = sys.argv[1:]
if not pid.isdecimal() or field not in {"state", "starttime"}:
    raise SystemExit(1)
try:
    line = pathlib.Path("/proc", pid, "stat").read_text(encoding="ascii")
except (OSError, UnicodeError):
    raise SystemExit(1)
close = line.rfind(")")
if close < 0:
    raise SystemExit(1)
post_comm = line[close + 1:].split()
if len(post_comm) < 20 or len(post_comm[0]) != 1:
    raise SystemExit(1)
value = post_comm[0] if field == "state" else post_comm[19]
if field == "starttime" and not value.isdecimal():
    raise SystemExit(1)
print(value)
PY
}

owned_process_is_current() {
    owned_pid=$1
    expected_token=$2
    current_token=$(owned_process_start_token "$owned_pid") || return 1
    [ "$current_token" = "$expected_token" ]
}

owned_process_is_zombie() {
    owned_pid=$1
    [ -r "/proc/$owned_pid/stat" ] || return 1
    owned_state=$(owned_process_stat_value "$owned_pid" state) || return 1
    [ "$owned_state" = Z ]
}

wait_for_owned_process_stop() {
    owned_pid=$1
    expected_token=$2
    process_label=$3
    stop_attempt=0
    while [ "$stop_attempt" -lt "$CHILD_STOP_ATTEMPTS" ]; do
        if ! kill -0 "$owned_pid" 2>/dev/null || owned_process_is_zombie "$owned_pid"; then
            return 0
        fi
        if ! owned_process_is_current "$owned_pid" "$expected_token"; then
            echo "envoy_ext_proc_runtime: refusing to signal changed $process_label PID $owned_pid" >&2
            return 1
        fi
        stop_attempt=$((stop_attempt + 1))
        sleep "$CHILD_STOP_DELAY"
    done
    return 1
}

stop_owned_process() {
    owned_pid=$1
    expected_token=$2
    process_label=$3
    if [ -z "$expected_token" ] || ! owned_process_is_current "$owned_pid" "$expected_token"; then
        if kill -0 "$owned_pid" 2>/dev/null; then
            echo "envoy_ext_proc_runtime: refusing to signal unverified $process_label PID $owned_pid" >&2
            return 1
        fi
    elif kill -0 "$owned_pid" 2>/dev/null; then
        if ! kill -TERM "$owned_pid" 2>/dev/null && kill -0 "$owned_pid" 2>/dev/null; then
            echo "envoy_ext_proc_runtime: could not send TERM to owned $process_label PID $owned_pid" >&2
            return 1
        fi
        if ! wait_for_owned_process_stop "$owned_pid" "$expected_token" "$process_label" &&
            kill -0 "$owned_pid" 2>/dev/null; then
            if ! owned_process_is_current "$owned_pid" "$expected_token"; then
                return 1
            fi
            if ! kill -KILL "$owned_pid" 2>/dev/null && kill -0 "$owned_pid" 2>/dev/null; then
                echo "envoy_ext_proc_runtime: could not send KILL to owned $process_label PID $owned_pid" >&2
                return 1
            fi
            if ! wait_for_owned_process_stop "$owned_pid" "$expected_token" "$process_label"; then
                echo "envoy_ext_proc_runtime: owned $process_label PID $owned_pid did not stop within bounded timeout" >&2
                return 1
            fi
        fi
    fi
    set +e
    wait "$owned_pid" 2>/dev/null
    set -e
    return 0
}

run_crs_runtime() {
    if ! crs_allow_status=$("$PYTHON_BIN" "$HELPER" probe \
        --runtime-root "$RUNTIME_ROOT" --tls-certificate "$TLS_CERTIFICATE" \
        --url "https://127.0.0.1:$listen_port/?id=42" \
        --method GET --data "" \
        --header "X-Request-Id: $CRS_ALLOW_TRANSACTION_ID" \
        --header "X-Framework-Run-ID: $CRS_RUNTIME_RUN_ID" \
        --header "Content-Length: 0" \
        --header "Host: crs-runtime.test" \
        --evidence-path "$CRS_ALLOW_PROBE_EVIDENCE"); then
        echo "envoy_ext_proc_runtime: FAIL - CRS allow probe could not be completed" >&2
        return 1
    fi
    if [ "$crs_allow_status" != "200" ]; then
        echo "envoy_ext_proc_runtime: FAIL - CRS allow request returned $crs_allow_status, expected 200" >&2
        return 1
    fi

    if ! crs_block_status=$("$PYTHON_BIN" "$HELPER" probe \
        --runtime-root "$RUNTIME_ROOT" --tls-certificate "$TLS_CERTIFICATE" \
        --url "https://127.0.0.1:$listen_port/?id=1%20UNION%20SELECT%20password%20FROM%20users" \
        --method GET --data "" \
        --header "X-Request-Id: $CRS_BLOCK_TRANSACTION_ID" \
        --header "X-Framework-Run-ID: $CRS_RUNTIME_RUN_ID" \
        --header "Content-Length: 0" \
        --header "Host: crs-runtime.test" \
        --evidence-path "$CRS_BLOCK_PROBE_EVIDENCE"); then
        echo "envoy_ext_proc_runtime: FAIL - CRS block probe could not be completed" >&2
        return 1
    fi
    if [ "$crs_block_status" != "403" ]; then
        echo "envoy_ext_proc_runtime: FAIL - CRS block request returned $crs_block_status, expected 403" >&2
        return 1
    fi

    # Case variation exercises the case-insensitive CRS expression through the
    # same real Envoy/ext_proc path.  It must not turn the fixture into a
    # connector-local marker check.
    if ! crs_bypass_status=$("$PYTHON_BIN" "$HELPER" probe \
        --runtime-root "$RUNTIME_ROOT" --tls-certificate "$TLS_CERTIFICATE" \
        --url "https://127.0.0.1:$listen_port/?id=1%20uNiOn%20sElEcT%20password%20fRoM%20users" \
        --method GET --data "" \
        --header "X-Request-Id: $CRS_BYPASS_TRANSACTION_ID" \
        --header "X-Framework-Run-ID: $CRS_RUNTIME_RUN_ID" \
        --header "Content-Length: 0" \
        --header "Host: crs-runtime.test" \
        --evidence-path "$CRS_BYPASS_PROBE_EVIDENCE"); then
        echo "envoy_ext_proc_runtime: FAIL - CRS bypass-class probe could not be completed" >&2
        return 1
    fi
    if [ "$crs_bypass_status" != "403" ]; then
        echo "envoy_ext_proc_runtime: FAIL - CRS bypass-class request returned $crs_bypass_status, expected 403" >&2
        return 1
    fi

    # The client probes and the Common event log are independently produced.
    # Do not materialize any verdict from expected data: wait until the raw
    # block records themselves establish the two disruptive decisions.
    crs_evidence_ready=0
    attempt=0
    while [ "$attempt" -lt 20 ]; do
        attempt=$((attempt + 1))
        if "$PYTHON_BIN" - "$COMMON_EVENT_LOG_PATH" "$COMPLETION_LOG_PATH" \
            "$CRS_ALLOW_PROBE_EVIDENCE" "$CRS_BLOCK_PROBE_EVIDENCE" \
            "$CRS_BYPASS_PROBE_EVIDENCE" "$CRS_ALLOW_TRANSACTION_ID" \
            "$CRS_BLOCK_TRANSACTION_ID" "$CRS_BYPASS_TRANSACTION_ID" \
            "$SERVICE_STDERR" <<'PY'
import json
import pathlib
import sys

event_path = pathlib.Path(sys.argv[1])
completion_path = pathlib.Path(sys.argv[2])
probe_paths = [pathlib.Path(value) for value in sys.argv[3:6]]
allow_id, block_id, bypass_id = sys.argv[6:9]
raw_service_log = pathlib.Path(sys.argv[9])

def jsonl(path):
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"missing or unsafe runtime log: {path}")
    records = []
    for line in path.read_text(encoding="utf-8", errors="strict").splitlines():
        if line:
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError("runtime record is not an object")
            records.append(value)
    return records

def probe(path, expected_status):
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"missing or unsafe client probe: {path}")
    value = json.loads(path.read_text(encoding="utf-8", errors="strict"))
    if not isinstance(value, dict) or value.get("evidence_type") != "envoy_http_client_probe":
        raise ValueError("invalid client probe evidence")
    if value.get("http_status") != expected_status or value.get("body_payload_persisted") is not False:
        raise ValueError("client probe did not observe the required status")

def disruptive(records, transaction_id):
    matches = [
        record for record in records
        if record.get("connector") == "envoy"
        and record.get("integration_mode") == "ext_proc"
        and record.get("transaction_id") == transaction_id
        and record.get("requested_action") == "deny"
        and record.get("actual_action") == "deny"
        and record.get("visible_http_status") == 403
    ]
    if len(matches) != 1:
        raise ValueError("missing uniquely correlated CRS deny event")

def canonical_trigger(path, transaction_id):
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"missing or unsafe ModSecurity log: {path}")
    if path.stat().st_size > 2 * 1024 * 1024:
        raise ValueError("ModSecurity log exceeds the bounded CRS-evidence limit")
    marker = f'[unique_id "{transaction_id}"]'
    matches = [
        line for line in path.read_text(encoding="utf-8", errors="strict").splitlines()
        if '[id "942270"]' in line
        and "REQUEST-942-APPLICATION-ATTACK-SQLI.conf" in line
        and marker in line
    ]
    if len(matches) != 1:
        raise ValueError("missing uniquely correlated canonical CRS trigger")

probes = [(probe_paths[0], 200), (probe_paths[1], 403), (probe_paths[2], 403)]
for path, status in probes:
    probe(path, status)
events = jsonl(event_path)
completions = jsonl(completion_path)
disruptive(events, block_id)
disruptive(events, bypass_id)
canonical_trigger(raw_service_log, block_id)
canonical_trigger(raw_service_log, bypass_id)
allow_completions = [
    record for record in completions
    if record.get("transaction_id") == allow_id
    and record.get("event") == "ext_proc_stream_complete"
    and record.get("integration_mode") == "ext_proc"
    and record.get("close_reason") == "response_end_of_stream"
]
if len(allow_completions) != 1:
    raise ValueError("missing uniquely correlated CRS allow completion")
PY
        then
            crs_evidence_ready=1
            break
        fi
        sleep 1
    done
    if [ "$crs_evidence_ready" -ne 1 ]; then
        echo "envoy_ext_proc_runtime: FAIL - missing raw CRS decision or correlation evidence" >&2
        print_runtime_log "$COMMON_EVENT_LOG_PATH"
        print_runtime_log "$COMPLETION_LOG_PATH"
        return 1
    fi

    for process_pair in "envoy:$envoy_pid" "ext_proc:$service_pid" "upstream:$upstream_pid"; do
        process_name=${process_pair%%:*}
        process_id=${process_pair##*:}
        if ! kill -0 "$process_id" 2>/dev/null; then
            echo "envoy_ext_proc_runtime: FAIL - $process_name was not stable after CRS requests" >&2
            return 1
        fi
    done

    {
        printf 'status=PASS\n'
        printf 'connector=envoy\n'
        printf 'integration_mode=ext_proc\n'
        printf 'runtime_profile=with-crs-no-mrts\n'
        printf 'run_id=%s\n' "$CRS_RUNTIME_RUN_ID"
        printf 'allow_request_id=%s\n' "$CRS_ALLOW_TRANSACTION_ID"
        printf 'allow_observed_status=%s\n' "$crs_allow_status"
        printf 'block_request_id=%s\n' "$CRS_BLOCK_TRANSACTION_ID"
        printf 'block_observed_status=%s\n' "$crs_block_status"
        printf 'bypass_request_id=%s\n' "$CRS_BYPASS_TRANSACTION_ID"
        printf 'bypass_observed_status=%s\n' "$crs_bypass_status"
        printf 'canonical_trigger_rule_id=942270\n'
        printf 'event_log=%s\n' "$COMMON_EVENT_LOG_PATH"
        printf 'completion_log=%s\n' "$COMPLETION_LOG_PATH"
        printf 'modsecurity_log=%s\n' "$SERVICE_STDERR"
        printf 'rules_file=%s\n' "$resolved_rules_file"
    } > "$SUMMARY"
}

verify_mrts_runtime_cleanup() {
    cleanup
    for process_pair in "envoy:$envoy_pid" "ext_proc:$service_pid" "upstream:$upstream_pid"; do
        process_name=${process_pair%%:*}
        process_id=${process_pair##*:}
        if [ -n "$process_id" ] && kill -0 "$process_id" 2>/dev/null; then
            echo "envoy_ext_proc_runtime: FAIL - MRTS cleanup left $process_name process $process_id alive" >&2
            return 1
        fi
    done
    if ! "$PYTHON_BIN" - "$listen_port" "$upstream_port" "$ext_proc_port" "$admin_port" <<'PY'
import socket
import sys

for raw_port in sys.argv[1:]:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("127.0.0.1", int(raw_port)))
    except OSError as exc:
        raise SystemExit(f"listener remains on 127.0.0.1:{raw_port}: {exc}")
    finally:
        sock.close()
PY
    then
        echo "envoy_ext_proc_runtime: FAIL - MRTS cleanup left an owned listener active" >&2
        return 1
    fi
    envoy_pid=
    service_pid=
    upstream_pid=
    trap - EXIT HUP INT TERM
}

validate_mrts_runtime_inputs() {
    case "$MSCONNECTOR_MRTS_RUNTIME" in
        0) return 0 ;;
        1) ;;
        *) echo "envoy_ext_proc_runtime: FAIL - MSCONNECTOR_MRTS_RUNTIME must be 0 or 1" >&2; exit 1 ;;
    esac
    [ -n "${MRTS_RUNTIME_EXECUTOR:-}" ] || missing_dependency "MRTS_RUNTIME_EXECUTOR is required for MRTS runtime mode"
    [ -n "${MRTS_RUNTIME_PLAN:-}" ] || missing_dependency "MRTS_RUNTIME_PLAN is required for MRTS runtime mode"
    [ -n "${MRTS_RUNTIME_RESULT:-}" ] || missing_dependency "MRTS_RUNTIME_RESULT is required for MRTS runtime mode"
    [ -n "${MRTS_LOAD_FILE:-}" ] || missing_dependency "MRTS_LOAD_FILE is required for MRTS runtime mode"
    case "$MRTS_RUNTIME_EXECUTOR" in /*) ;; *) echo "envoy_ext_proc_runtime: FAIL - MRTS_RUNTIME_EXECUTOR must be absolute" >&2; exit 1 ;; esac
    case "$MRTS_RUNTIME_PLAN" in /*) ;; *) echo "envoy_ext_proc_runtime: FAIL - MRTS_RUNTIME_PLAN must be absolute" >&2; exit 1 ;; esac
    case "$MRTS_RUNTIME_RESULT" in /*) ;; *) echo "envoy_ext_proc_runtime: FAIL - MRTS_RUNTIME_RESULT must be absolute" >&2; exit 1 ;; esac
    case "$MRTS_LOAD_FILE" in /*) ;; *) echo "envoy_ext_proc_runtime: FAIL - MRTS_LOAD_FILE must be absolute" >&2; exit 1 ;; esac
    [ -f "$MRTS_RUNTIME_EXECUTOR" ] || missing_dependency "MRTS_RUNTIME_EXECUTOR is not a regular file: $MRTS_RUNTIME_EXECUTOR"
    [ -r "$MRTS_RUNTIME_EXECUTOR" ] || missing_dependency "MRTS_RUNTIME_EXECUTOR is not readable: $MRTS_RUNTIME_EXECUTOR"
    [ -f "$MRTS_RUNTIME_PLAN" ] || missing_dependency "MRTS_RUNTIME_PLAN is missing: $MRTS_RUNTIME_PLAN"
    [ -f "$MRTS_LOAD_FILE" ] || missing_dependency "MRTS_LOAD_FILE is missing: $MRTS_LOAD_FILE"
    [ ! -L "$MRTS_RUNTIME_EXECUTOR" ] || { echo "envoy_ext_proc_runtime: FAIL - MRTS_RUNTIME_EXECUTOR must not be a symlink" >&2; exit 1; }
    [ ! -L "$MRTS_RUNTIME_PLAN" ] || { echo "envoy_ext_proc_runtime: FAIL - MRTS_RUNTIME_PLAN must not be a symlink" >&2; exit 1; }
    [ ! -L "$MRTS_LOAD_FILE" ] || { echo "envoy_ext_proc_runtime: FAIL - MRTS_LOAD_FILE must not be a symlink" >&2; exit 1; }
    if ! "$PYTHON_BIN" - "$MRTS_RUNTIME_EXECUTOR" "$MRTS_RUNTIME_PLAN" "$MRTS_RUNTIME_RESULT" "$MRTS_LOAD_FILE" <<'PY'
import pathlib
import sys

for raw in sys.argv[1:]:
    path = pathlib.Path(raw)
    for parent in (path, *path.parents):
        if parent.exists() and parent.is_symlink():
            raise SystemExit(f"symlink path component: {parent}")
PY
    then
        echo "envoy_ext_proc_runtime: FAIL - MRTS runtime input contains a symlink path component" >&2
        exit 1
    fi
    case "$MRTS_RUNTIME_PLAN" in
        "$RUNTIME_ROOT"/*) ;;
        *) echo "envoy_ext_proc_runtime: FAIL - MRTS_RUNTIME_PLAN must be under RUNTIME_ROOT" >&2; exit 1 ;;
    esac
    case "$MRTS_RUNTIME_RESULT" in
        "$RUNTIME_ROOT"/*) ;;
        *) echo "envoy_ext_proc_runtime: FAIL - MRTS_RUNTIME_RESULT must be under RUNTIME_ROOT" >&2; exit 1 ;;
    esac
    if ! "$PYTHON_BIN" - "$RUNTIME_ROOT" "$MRTS_RUNTIME_PLAN" "$MRTS_RUNTIME_RESULT" <<'PY'
import pathlib
import sys

root = pathlib.Path(sys.argv[1]).resolve()
for raw in sys.argv[2:]:
    candidate = pathlib.Path(raw).resolve(strict=False)
    try:
        candidate.relative_to(root)
    except ValueError:
        raise SystemExit(f"runtime path escapes root: {candidate}")
PY
    then
        echo "envoy_ext_proc_runtime: FAIL - MRTS runtime path escapes RUNTIME_ROOT" >&2
        exit 1
    fi
    [ ! -e "$MRTS_RUNTIME_RESULT" ] && [ ! -L "$MRTS_RUNTIME_RESULT" ] || {
        echo "envoy_ext_proc_runtime: FAIL - MRTS_RUNTIME_RESULT must not already exist" >&2
        exit 1
    }
    result_parent=$(dirname "$MRTS_RUNTIME_RESULT")
    [ -d "$result_parent" ] || { echo "envoy_ext_proc_runtime: FAIL - MRTS_RUNTIME_RESULT parent is missing" >&2; exit 1; }
    [ ! -L "$result_parent" ] || { echo "envoy_ext_proc_runtime: FAIL - MRTS_RUNTIME_RESULT parent must not be a symlink" >&2; exit 1; }
    sealed_plan_validator=$CONNECTOR_ROOT/ci/runtime/lifecycle/run-no-crs-with-mrts-target.py
    [ -f "$sealed_plan_validator" ] && [ ! -L "$sealed_plan_validator" ] || {
        echo "envoy_ext_proc_runtime: FAIL - sealed MRTS plan validator is unavailable" >&2
        exit 1
    }
    if ! "$PYTHON_BIN" "$sealed_plan_validator" --validate-sealed-plan \
        --plan "$MRTS_RUNTIME_PLAN" --runtime-root "$VERIFIED_RUN_ROOT" \
        --framework-root "$FRAMEWORK_ROOT" --rules-root "$MRTS_RUNTIME_RULES_ROOT" \
        --load-file "$MRTS_LOAD_FILE"; then
        echo "envoy_ext_proc_runtime: FAIL - sealed MRTS plan no-CRS validation failed" >&2
        exit 1
    fi
    grep -Eq '^[[:space:]]*Include[[:space:]]+' "$MRTS_LOAD_FILE" || {
        echo "envoy_ext_proc_runtime: FAIL - MRTS_LOAD_FILE contains no rule includes" >&2
        exit 1
    }
}

[ -n "${ENVOY_BIN:-}" ] || missing_dependency "ENVOY_BIN is required"
[ -x "$ENVOY_BIN" ] || missing_dependency "ENVOY_BIN is not executable: $ENVOY_BIN"
[ -x "$EXT_PROC_BIN" ] || missing_dependency "ext_proc service is not executable: $EXT_PROC_BIN"
[ -f "$EXT_PROC_CONFIG" ] || missing_dependency "ext_proc service config is missing: $EXT_PROC_CONFIG"
[ -f "$YAML_TEMPLATE" ] || missing_dependency "Envoy ext_proc template is missing: $YAML_TEMPLATE"
[ -x "$PREPARE_ENVOY_CONFIG" ] || missing_dependency "Envoy ext_proc config materializer is missing: $PREPARE_ENVOY_CONFIG"
[ -f "$PREPARE_RUNTIME_CONFIG" ] || missing_dependency "Common runtime config materializer is missing: $PREPARE_RUNTIME_CONFIG"
[ -f "$VERSION_LOCK" ] || missing_dependency "Envoy ext_proc version lock is missing: $VERSION_LOCK"
[ -f "$HELPER" ] || missing_dependency "smoke helper is missing: $HELPER"
[ -f "$TLS_RENDERER" ] || missing_dependency "TLS YAML renderer is missing: $TLS_RENDERER"
command -v "$PYTHON_BIN" >/dev/null 2>&1 || missing_dependency "Python interpreter is missing: $PYTHON_BIN"
case "$CRS_RUNTIME" in
    0|1) ;;
    *) echo "envoy_ext_proc_runtime: FAIL - MSCONNECTOR_CRS_RUNTIME must be 0 or 1" >&2; exit 1 ;;
esac
if [ "$CRS_RUNTIME" = 1 ] && [ "$MSCONNECTOR_MRTS_RUNTIME" = 1 ]; then
    echo "envoy_ext_proc_runtime: FAIL - CRS and MRTS runtime modes are mutually exclusive" >&2
    exit 1
fi
if [ "$CRS_RUNTIME" = 1 ]; then
    # The framework supplies a run-scoped identifier.  Keep it short enough
    # that the derived wire IDs remain bounded, and derive every CRS request
    # ID from it so independent matrix runs cannot collide in raw evidence.
    case "$CRS_RUNTIME_RUN_ID" in
        ''|*[!A-Za-z0-9._-]*)
            echo "envoy_ext_proc_runtime: FAIL - CRS_RUNTIME_RUN_ID must be a bounded safe token" >&2
            exit 1
            ;;
        *) ;;
    esac
    if [ "${#CRS_RUNTIME_RUN_ID}" -gt 48 ]; then
        echo "envoy_ext_proc_runtime: FAIL - CRS_RUNTIME_RUN_ID exceeds 48 characters" >&2
        exit 1
    fi
    CRS_ALLOW_TRANSACTION_ID="envoy-ext-proc-crs-${CRS_RUNTIME_RUN_ID}-allow"
    CRS_BLOCK_TRANSACTION_ID="envoy-ext-proc-crs-${CRS_RUNTIME_RUN_ID}-block"
    CRS_BYPASS_TRANSACTION_ID="envoy-ext-proc-crs-${CRS_RUNTIME_RUN_ID}-bypass"
fi
# shellcheck disable=SC1090 # Runtime path is a connector-owned, prevalidated renderer.
. "$TLS_RENDERER"
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
    *) ;;
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
case "$PHASE4_BARRIER_DIR" in
    "$RUNTIME_ROOT"/*) ;;
    *) echo "envoy_ext_proc_runtime: FAIL - phase-4 barrier directory must be under RUNTIME_ROOT" >&2; exit 1 ;;
esac
case "$PHASE4_BARRIER_OBSERVATION" in
    "$RUNTIME_ROOT"/*) ;;
    *) echo "envoy_ext_proc_runtime: FAIL - phase-4 barrier observation must be under RUNTIME_ROOT" >&2; exit 1 ;;
esac
case "$ALLOW_PROBE_EVIDENCE" in
    "$RUNTIME_ROOT"/*) ;;
    *) echo "envoy_ext_proc_runtime: FAIL - allow probe evidence must be under RUNTIME_ROOT" >&2; exit 1 ;;
esac
for crs_probe_evidence in "$CRS_ALLOW_PROBE_EVIDENCE" "$CRS_BLOCK_PROBE_EVIDENCE" "$CRS_BYPASS_PROBE_EVIDENCE"; do
    case "$crs_probe_evidence" in
        "$RUNTIME_ROOT"/*) ;;
        *) echo "envoy_ext_proc_runtime: FAIL - CRS probe evidence must be under RUNTIME_ROOT" >&2; exit 1 ;;
    esac
done
case "$TRANSPORT_CANCEL_PROBE" in
    0|1) ;;
    *) echo "envoy_ext_proc_runtime: FAIL - ENVOY_TRANSPORT_CANCEL_PROBE must be 0 or 1" >&2; exit 1 ;;
esac
if [ "${NO_CRS_ARTIFACT_PROFILE:-}" = full_lifecycle ] && [ -z "$FULL_LIFECYCLE_EVIDENCE_OUTPUT" ]; then
    echo "envoy_ext_proc_runtime: FAIL - full_lifecycle requires FULL_LIFECYCLE_EVIDENCE_OUTPUT" >&2
    exit 1
fi
if [ -n "$FULL_LIFECYCLE_EVIDENCE_OUTPUT" ]; then
    case "$FULL_LIFECYCLE_EVIDENCE_OUTPUT" in
        /*) ;;
        *) echo "envoy_ext_proc_runtime: FAIL - first-byte evidence output must be absolute" >&2; exit 1 ;;
    esac
    case "$FULL_LIFECYCLE_EVIDENCE_OUTPUT" in
        "$REPO_ROOT"|"$REPO_ROOT"/*)
            echo "envoy_ext_proc_runtime: FAIL - first-byte evidence output must be outside the checkout" >&2
            exit 1
            ;;
        *) ;;
    esac
fi
if ! "$PYTHON_BIN" "$HELPER" prepare-runtime-root --runtime-root "$RUNTIME_ROOT"; then
    echo "envoy_ext_proc_runtime: FAIL - RUNTIME_ROOT is unsafe for private runtime artifacts" >&2
    exit 1
fi
validate_mrts_runtime_inputs
trap cleanup EXIT HUP INT TERM
mkdir -p "$PHASE4_BARRIER_DIR"
rm -f "$COMMON_EVENT_LOG_PATH" "$COMPLETION_LOG_PATH" "$SUMMARY" "$EXT_PROC_RUNTIME_CONFIG" \
    "$TRANSPORT_OBSERVATIONS" "$PHASE4_BARRIER_OBSERVATION" \
    "$ALLOW_PROBE_EVIDENCE" "$CRS_ALLOW_PROBE_EVIDENCE" "$CRS_BLOCK_PROBE_EVIDENCE" \
    "$CRS_BYPASS_PROBE_EVIDENCE" "$TLS_CERTIFICATE" "$TLS_PRIVATE_KEY" \
    "$PHASE4_BARRIER_DIR/upstream-paused.json" "$PHASE4_BARRIER_DIR/release" \
    "$PHASE4_BARRIER_DIR/upstream-completed.json"

pinned_envoy_release=$(sed -n 's/^ENVOY_RELEASE=//p' "$VERSION_LOCK")
[ -n "$pinned_envoy_release" ] || {
    echo "envoy_ext_proc_runtime: FAIL - version lock has no ENVOY_RELEASE" >&2
    exit 1
}
if ! "$ENVOY_BIN" --version >"$RUNTIME_ROOT/envoy-version.txt" 2>&1; then
    echo "envoy_ext_proc_runtime: FAIL - could not read Envoy version" >&2
    exit 1
fi
command -v sha256sum >/dev/null 2>&1 || missing_dependency "sha256sum is required for Envoy runtime provenance"
sha256sum "$ENVOY_BIN" | awk '{print $1}' >"$RUNTIME_ROOT/envoy-binary-sha256.txt"
test -s "$RUNTIME_ROOT/envoy-binary-sha256.txt" || {
    echo "envoy_ext_proc_runtime: FAIL - could not record Envoy binary SHA-256" >&2
    exit 1
}
envoy_version=$(cat "$RUNTIME_ROOT/envoy-version.txt")
case "$envoy_version" in
    *"/$pinned_envoy_release/"*|*"version: $pinned_envoy_release"*) ;;
    *)
        echo "envoy_ext_proc_runtime: FAIL - Envoy does not match pinned $pinned_envoy_release" >&2
        print_runtime_log "$RUNTIME_ROOT/envoy-version.txt"
        exit 1
        ;;
esac

free_ports=$("$PYTHON_BIN" "$HELPER" free-ports --count 4)
case "$free_ports" in
    *'
'*) echo "envoy_ext_proc_runtime: FAIL - free-ports returned multiple lines" >&2; exit 1 ;;
esac
IFS=' ' read -r default_listen_port default_upstream_port default_ext_proc_port default_admin_port extra_port <<EOF
$free_ports
EOF
[ -n "${default_listen_port:-}" ] && [ -n "${default_upstream_port:-}" ] && \
    [ -n "${default_ext_proc_port:-}" ] && [ -n "${default_admin_port:-}" ] && \
    [ -z "${extra_port:-}" ] || {
    echo "envoy_ext_proc_runtime: FAIL - free-ports did not return exactly four ports" >&2
    exit 1
}
listen_port=${ENVOY_SMOKE_PORT:-$default_listen_port}
upstream_port=${ENVOY_UPSTREAM_PORT:-$default_upstream_port}
ext_proc_port=${ENVOY_EXT_PROC_PORT:-$default_ext_proc_port}
admin_port=${ENVOY_ADMIN_PORT:-$default_admin_port}
if ! base_id=$("$PYTHON_BIN" - "$listen_port" "$upstream_port" "$ext_proc_port" "$admin_port" <<'PY'
import sys

ports = []
for raw in sys.argv[1:]:
    if not raw.isascii() or not raw.isdecimal():
        raise SystemExit(f"non-numeric port: {raw!r}")
    port = int(raw)
    if not 1 <= port <= 65535:
        raise SystemExit(f"out-of-range port: {port}")
    ports.append(port)
if len(set(ports)) != len(ports):
    raise SystemExit("ports must be distinct")
print((ports[0] + ports[3]) % 100000)
PY
); then
    echo "envoy_ext_proc_runtime: FAIL - invalid Envoy runtime port selection" >&2
    exit 1
fi

command -v openssl >/dev/null 2>&1 || missing_dependency "openssl is required for the private loopback TLS certificate"
if ! create_private_loopback_tls "$TLS_CERTIFICATE" "$TLS_PRIVATE_KEY"; then
    echo "envoy_ext_proc_runtime: FAIL - could not create the private loopback TLS certificate" >&2
    exit 1
fi

OUTPUT_CONFIG="$ENVOY_CONFIG" LISTEN_PORT="$listen_port" \
    UPSTREAM_PORT="$upstream_port" EXT_PROC_PORT="$ext_proc_port" \
    ADMIN_PORT="$admin_port" TEMPLATE="$YAML_TEMPLATE" \
    TLS_CERTIFICATE="$TLS_CERTIFICATE" TLS_PRIVATE_KEY="$TLS_PRIVATE_KEY" \
    sh "$PREPARE_ENVOY_CONFIG" >/dev/null
OUTPUT_CONFIG="$EXT_PROC_RUNTIME_CONFIG" RULES_FILE="$RULES_FILE" EVENT_PATH="$COMMON_EVENT_LOG_PATH" \
    sh "$PREPARE_RUNTIME_CONFIG" >/dev/null

if ! grep -Fq 'name: envoy.filters.http.ext_proc' "$ENVOY_CONFIG" || \
    grep -Fq 'name: envoy.filters.http.ext_authz' "$ENVOY_CONFIG" || \
    ! grep -Fq 'request_body_mode: STREAMED' "$ENVOY_CONFIG" || \
    ! grep -Fq 'response_body_mode: STREAMED' "$ENVOY_CONFIG" || \
    ! grep -Fq 'name: envoy.transport_sockets.tls' "$ENVOY_CONFIG" || \
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
    print_runtime_log "$RUNTIME_ROOT/envoy-validate.stderr.log"
    exit 1
fi

"$PYTHON_BIN" "$HELPER" serve-upstream --port "$upstream_port" \
    --runtime-root "$RUNTIME_ROOT" \
    --tls-certificate "$TLS_CERTIFICATE" \
    --tls-private-key "$TLS_PRIVATE_KEY" \
    --client-cancel-delay "${ENVOY_CLIENT_CANCEL_DELAY_SECONDS:-5}" \
    --phase4-barrier-dir "$PHASE4_BARRIER_DIR" \
    --phase4-barrier-timeout "$PHASE4_BARRIER_TIMEOUT" \
        >"$UPSTREAM_STDOUT" 2>"$UPSTREAM_STDERR" &
upstream_pid=$!
upstream_start_token=$(owned_process_start_token "$upstream_pid") || {
    echo "envoy_ext_proc_runtime: FAIL - could not capture upstream process identity" >&2
    exit 1
}

EXT_PROC_BIN="$EXT_PROC_BIN" EXT_PROC_CONFIG="$EXT_PROC_CONFIG" \
    EXT_PROC_RUNTIME_CONFIG="$EXT_PROC_RUNTIME_CONFIG" \
    EVENT_LOG_PATH="$COMPLETION_LOG_PATH" LISTEN_ADDRESS=127.0.0.1 \
    LISTEN_PORT="$ext_proc_port" sh "$SCRIPT_DIR/serve_envoy_ext_proc.sh" \
    >"$SERVICE_STDOUT" 2>"$SERVICE_STDERR" &
service_pid=$!
service_start_token=$(owned_process_start_token "$service_pid") || {
    echo "envoy_ext_proc_runtime: FAIL - could not capture ext_proc process identity" >&2
    exit 1
}

"$ENVOY_BIN" -c "$ENVOY_CONFIG" --base-id "$base_id" --disable-hot-restart \
    --log-level error >"$ENVOY_STDOUT" 2>"$ENVOY_STDERR" &
envoy_pid=$!
envoy_start_token=$(owned_process_start_token "$envoy_pid") || {
    echo "envoy_ext_proc_runtime: FAIL - could not capture Envoy process identity" >&2
    exit 1
}

readiness_status=
attempt=0
while [ "$attempt" -lt 30 ]; do
    attempt=$((attempt + 1))
    for process_pair in "envoy:$envoy_pid" "ext_proc:$service_pid" "upstream:$upstream_pid"; do
        process_name=${process_pair%%:*}
        process_id=${process_pair##*:}
        if ! kill -0 "$process_id" 2>/dev/null; then
            echo "envoy_ext_proc_runtime: FAIL - $process_name process exited early" >&2
            print_runtime_log "$ENVOY_STDERR"
            print_runtime_log "$SERVICE_STDERR"
            exit 1
        fi
    done
    set +e
    readiness_status=$("$PYTHON_BIN" "$HELPER" probe \
        --runtime-root "$RUNTIME_ROOT" --tls-certificate "$TLS_CERTIFICATE" \
        --url "https://127.0.0.1:$listen_port/allowed" \
        --header "X-Request-Id: $READINESS_TRANSACTION_ID" \
        --evidence-path "$READINESS_PROBE_EVIDENCE" 2>/dev/null)
    probe_rc=$?
    set -e
    if [ "$probe_rc" -eq 0 ] && [ "$readiness_status" = "200" ]; then
        break
    fi
    sleep 1
done

if [ "$readiness_status" != "200" ]; then
    echo "envoy_ext_proc_runtime: FAIL - readiness request returned ${readiness_status:-no status}, expected 200" >&2
    exit 1
fi

if [ "$CRS_RUNTIME" = 1 ]; then
    run_crs_runtime
    cleanup
    envoy_pid=
    service_pid=
    upstream_pid=
    trap - EXIT HUP INT TERM
    printf 'processes_stopped=yes\n' >> "$SUMMARY"
    printf 'envoy_ext_proc_runtime: pass (CRS runtime) summary=%s\n' "$SUMMARY"
elif [ "$MSCONNECTOR_MRTS_RUNTIME" = 1 ]; then
    # The executor owns MRTS case selection and result construction.  Run it
    # against the live host immediately after readiness; the fixed baseline
    # probes below use rules that are intentionally not part of MRTS mode.
    set +e
    "$PYTHON_BIN" "$MRTS_RUNTIME_EXECUTOR" \
        --connector envoy \
        --runtime-root "$RUNTIME_ROOT" \
        --plan "$MRTS_RUNTIME_PLAN" \
        --result "$MRTS_RUNTIME_RESULT" \
        --load-file "$MRTS_LOAD_FILE" \
        --event-log "$COMMON_EVENT_LOG_PATH" \
        --scheme https \
        --host 127.0.0.1 \
        --port "$listen_port" \
        --tls-insecure
    mrts_executor_rc=$?
    set -e
    if [ "$mrts_executor_rc" -ne 0 ]; then
        echo "envoy_ext_proc_runtime: FAIL - MRTS runtime executor failed (exit $mrts_executor_rc)" >&2
        exit "$mrts_executor_rc"
    fi
    [ -f "$MRTS_RUNTIME_RESULT" ] && [ ! -L "$MRTS_RUNTIME_RESULT" ] && [ -s "$MRTS_RUNTIME_RESULT" ] || {
        echo "envoy_ext_proc_runtime: FAIL - MRTS runtime executor produced no safe result" >&2
        exit 1
    }
    for process_pair in "envoy:$envoy_pid" "ext_proc:$service_pid" "upstream:$upstream_pid"; do
        process_name=${process_pair%%:*}
        process_id=${process_pair##*:}
        if ! kill -0 "$process_id" 2>/dev/null; then
            echo "envoy_ext_proc_runtime: FAIL - $process_name exited during MRTS execution" >&2
            exit 1
        fi
    done
    if ! verify_mrts_runtime_cleanup; then
        exit 1
    fi
    {
        printf 'status=PASS\n'
        printf 'connector=envoy\n'
        printf 'integration_mode=ext_proc\n'
        printf 'mrts_runtime=true\n'
        printf 'mrts_runtime_plan=%s\n' "$MRTS_RUNTIME_PLAN"
        printf 'mrts_runtime_result=%s\n' "$MRTS_RUNTIME_RESULT"
        printf 'mrts_load_file=%s\n' "$resolved_rules_file"
        printf 'envoy_release=%s\n' "$pinned_envoy_release"
        printf 'envoy_binary_path=%s\n' "$ENVOY_BIN"
        printf 'envoy_binary_sha256=%s\n' "$(cat "$RUNTIME_ROOT/envoy-binary-sha256.txt")"
        printf 'envoy_version_file=%s\n' "$RUNTIME_ROOT/envoy-version.txt"
        printf 'host_readiness_status=%s\n' "$readiness_status"
        printf 'event_log=%s\n' "$COMMON_EVENT_LOG_PATH"
        printf 'cleanup=passed\n'
    } > "$SUMMARY"
    exit 0
fi

if ! allowed_status=$("$PYTHON_BIN" "$HELPER" probe \
    --runtime-root "$RUNTIME_ROOT" --tls-certificate "$TLS_CERTIFICATE" \
    --url "https://127.0.0.1:$listen_port/allowed" \
    --header "X-Request-Id: $ALLOW_TRANSACTION_ID" \
    --evidence-path "$ALLOW_PROBE_EVIDENCE"); then
    echo "envoy_ext_proc_runtime: FAIL - allowed probe could not be completed" >&2
    exit 1
fi
if [ "$allowed_status" != "200" ]; then
    echo "envoy_ext_proc_runtime: FAIL - allowed request returned $allowed_status, expected 200" >&2
    exit 1
fi

if ! streamed_status=$("$PYTHON_BIN" "$HELPER" probe \
    --runtime-root "$RUNTIME_ROOT" --tls-certificate "$TLS_CERTIFICATE" \
    --url "https://127.0.0.1:$listen_port/streamed" --method POST \
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
    --runtime-root "$RUNTIME_ROOT" --tls-certificate "$TLS_CERTIFICATE" \
    --url "https://127.0.0.1:$listen_port/phase1-deny" \
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
    --runtime-root "$RUNTIME_ROOT" --tls-certificate "$TLS_CERTIFICATE" \
    --url "https://127.0.0.1:$listen_port/phase2-deny" --method POST \
    --data "$NO_CRS_REQUEST_BODY_MARKER" \
    --header "X-Request-Id: envoy-ext-proc-phase2-deny"); then
    echo "envoy_ext_proc_runtime: FAIL - phase-2 deny probe could not be completed" >&2
    exit 1
fi
if [ "$phase2_deny_status" != "403" ]; then
    echo "envoy_ext_proc_runtime: FAIL - phase-2 deny returned $phase2_deny_status, expected 403" >&2
    exit 1
fi

if ! phase3_deny_status=$("$PYTHON_BIN" "$HELPER" probe \
    --runtime-root "$RUNTIME_ROOT" --tls-certificate "$TLS_CERTIFICATE" \
    --url "https://127.0.0.1:$listen_port/phase3-block" \
    --header "X-Request-Id: envoy-ext-proc-phase3-deny"); then
    echo "envoy_ext_proc_runtime: FAIL - phase-3 deny probe could not be completed" >&2
    exit 1
fi
if [ "$phase3_deny_status" != "403" ]; then
    echo "envoy_ext_proc_runtime: FAIL - phase-3 deny returned $phase3_deny_status, expected 403" >&2
    exit 1
fi

if ! phase3_redirect_status=$("$PYTHON_BIN" "$HELPER" probe \
    --runtime-root "$RUNTIME_ROOT" --tls-certificate "$TLS_CERTIFICATE" \
    --url "https://127.0.0.1:$listen_port/phase3-redirect" --no-redirect \
    --header "X-Request-Id: envoy-ext-proc-phase3-redirect"); then
    echo "envoy_ext_proc_runtime: FAIL - phase-3 redirect probe could not be completed" >&2
    exit 1
fi
if [ "$phase3_redirect_status" != "302" ]; then
    echo "envoy_ext_proc_runtime: FAIL - phase-3 redirect returned $phase3_redirect_status, expected 302" >&2
    exit 1
fi

if ! phase4_barrier_observation=$("$PYTHON_BIN" "$HELPER" phase4-first-byte \
    --runtime-root "$RUNTIME_ROOT" --tls-certificate "$TLS_CERTIFICATE" \
    --host 127.0.0.1 --port "$listen_port" --path /phase4-marker \
    --header "X-Request-Id: $PHASE4_BARRIER_TRANSACTION_ID" \
    --barrier-dir "$PHASE4_BARRIER_DIR" --timeout "$PHASE4_BARRIER_TIMEOUT" \
    --output "$PHASE4_BARRIER_OBSERVATION"); then
    echo "envoy_ext_proc_runtime: FAIL - phase-4 synchronized first-byte probe could not be completed" >&2
    exit 1
fi
phase4_safe_status=$("$PYTHON_BIN" -c 'import json,sys; print(json.loads(sys.argv[1])["http_status"])' "$phase4_barrier_observation") || {
    echo "envoy_ext_proc_runtime: FAIL - phase-4 first-byte observation is malformed" >&2
    exit 1
}
if [ "$phase4_safe_status" != "200" ]; then
    echo "envoy_ext_proc_runtime: FAIL - phase-4 safe mode returned $phase4_safe_status, expected 200" >&2
    exit 1
fi
if ! phase4_followup_status=$("$PYTHON_BIN" "$HELPER" probe \
    --runtime-root "$RUNTIME_ROOT" --tls-certificate "$TLS_CERTIFICATE" \
    --url "https://127.0.0.1:$listen_port/allowed" \
    --header "X-Request-Id: envoy-ext-proc-phase4-followup"); then
    echo "envoy_ext_proc_runtime: FAIL - follow-up request after phase-4 barrier could not be completed" >&2
    exit 1
fi
if [ "$phase4_followup_status" != "200" ]; then
    echo "envoy_ext_proc_runtime: FAIL - follow-up request after phase-4 barrier returned $phase4_followup_status, expected 200" >&2
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
    print_runtime_log "$COMPLETION_LOG_PATH"
    exit 1
fi
if grep -Fq 'request-body-for-ext-proc' "$COMPLETION_LOG_PATH" || \
    grep -Fq 'envoy connector upstream ok' "$COMPLETION_LOG_PATH" || \
    grep -Fq "$NO_CRS_REQUEST_BODY_MARKER" "$COMPLETION_LOG_PATH" || \
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
    print_runtime_log "$COMMON_EVENT_LOG_PATH"
    exit 1
fi
if grep -Fq 'request-body-for-ext-proc' "$COMMON_EVENT_LOG_PATH" || \
    grep -Fq 'envoy connector upstream ok' "$COMMON_EVENT_LOG_PATH" || \
    grep -Fq "$NO_CRS_REQUEST_BODY_MARKER" "$COMMON_EVENT_LOG_PATH" || \
    grep -Fq 'no-crs-response-body-marker' "$COMMON_EVENT_LOG_PATH"; then
    echo "envoy_ext_proc_runtime: FAIL - Common raw event evidence contains a body payload" >&2
    exit 1
fi
# The helper refuses to write either artifact unless the exact P4 safe
# Common/libmodsecurity event for this transaction is already present.  It
# copies only bounded counters/status metadata and adds the client/upstream
# barrier facts; neither response fixture is ever written into JSONL.
if [ -n "$FULL_LIFECYCLE_EVIDENCE_OUTPUT" ]; then
    if ! "$PYTHON_BIN" "$HELPER" write-phase4-first-byte-evidence \
        --runtime-root "$RUNTIME_ROOT" \
        --event-log "$COMMON_EVENT_LOG_PATH" \
        --observation "$PHASE4_BARRIER_OBSERVATION" \
        --transaction-id "$PHASE4_BARRIER_TRANSACTION_ID" \
        --evidence-output "$FULL_LIFECYCLE_EVIDENCE_OUTPUT" \
        --run-id "${NO_CRS_RUN_ID:-}" >/dev/null; then
        echo "envoy_ext_proc_runtime: FAIL - could not bind phase-4 first-byte evidence to the Common event" >&2
        exit 1
    fi
else
    if ! "$PYTHON_BIN" "$HELPER" write-phase4-first-byte-evidence \
        --runtime-root "$RUNTIME_ROOT" \
        --event-log "$COMMON_EVENT_LOG_PATH" \
        --observation "$PHASE4_BARRIER_OBSERVATION" \
        --transaction-id "$PHASE4_BARRIER_TRANSACTION_ID" \
        --run-id "${NO_CRS_RUN_ID:-}" >/dev/null; then
        echo "envoy_ext_proc_runtime: FAIL - could not append phase-4 first-byte barrier event" >&2
        exit 1
    fi
fi
if [ -n "$FULL_LIFECYCLE_EVIDENCE_OUTPUT" ] && [ ! -s "$FULL_LIFECYCLE_EVIDENCE_OUTPUT" ]; then
    echo "envoy_ext_proc_runtime: FAIL - phase-4 first-byte evidence was not written" >&2
    exit 1
fi
if grep -Fq 'no-crs-response-body-marker' "$COMMON_EVENT_LOG_PATH" || \
    grep -Fq "$NO_CRS_REQUEST_BODY_MARKER" "$COMMON_EVENT_LOG_PATH"; then
    echo "envoy_ext_proc_runtime: FAIL - phase-4 barrier event persisted a body payload" >&2
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
        --runtime-root "$RUNTIME_ROOT" --tls-certificate "$TLS_CERTIFICATE" \
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
            *) ;;
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
        --runtime-root "$RUNTIME_ROOT" --tls-certificate "$TLS_CERTIFICATE" \
        --url "https://127.0.0.1:$listen_port/allowed" \
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
if ! "$PYTHON_BIN" "$HELPER" write-allow-event \
    --runtime-root "$RUNTIME_ROOT" \
    --event-log "$COMMON_EVENT_LOG_PATH" \
    --probe-evidence "$ALLOW_PROBE_EVIDENCE" \
    --completion-log "$COMPLETION_LOG_PATH" \
    --transaction-id "$ALLOW_TRANSACTION_ID" >/dev/null; then
    echo "envoy_ext_proc_runtime: FAIL - could not bind the P1 allow response to its ext_proc completion" >&2
    exit 1
fi
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
    printf 'envoy_binary_sha256=%s\n' "$(cat "$RUNTIME_ROOT/envoy-binary-sha256.txt")"
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
    printf 'phase4_rule_observed_status=%s\n' "$phase4_safe_status"
    printf 'phase4_safe_status=%s\n' "$phase4_safe_status"
    printf 'phase4_end_of_stream_evaluation_status=%s\n' "$phase4_safe_status"
    printf 'phase4_first_byte_before_response_end_status=%s\n' "$phase4_safe_status"
    printf 'phase4_no_full_response_buffering_status=%s\n' "$phase4_safe_status"
    printf 'phase4_first_byte_followup_status=%s\n' "$phase4_followup_status"
    printf 'phase4_first_byte_observation=%s\n' "$PHASE4_BARRIER_OBSERVATION"
    printf 'phase4_first_byte_evidence=%s\n' "${FULL_LIFECYCLE_EVIDENCE_OUTPUT:-not_written}"
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
