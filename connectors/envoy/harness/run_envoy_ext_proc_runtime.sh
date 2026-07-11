#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
CONNECTOR_DIR=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
REPO_ROOT=$(CDPATH= cd "$CONNECTOR_DIR/../.." && pwd)
BUILD_ROOT=${BUILD_ROOT:-${XDG_STATE_HOME:-${HOME:-/tmp}/.local/state}/ModSecurity-conector-build}
EXT_PROC_BIN=${EXT_PROC_BIN:-$BUILD_ROOT/envoy-ext-proc/msconnector_envoy_ext_proc}
EXT_PROC_CONFIG=${EXT_PROC_CONFIG:-$CONNECTOR_DIR/config/envoy-ext-proc-service.json}
RUNTIME_ROOT=${RUNTIME_ROOT:-$BUILD_ROOT/envoy-ext-proc/runtime-smoke}
EVENT_LOG_PATH=${EVENT_LOG_PATH:-$RUNTIME_ROOT/events.jsonl}
PYTHON_BIN=${PYTHON:-python3}
HELPER="$SCRIPT_DIR/envoy_smoke_helper.py"
YAML_TEMPLATE="$CONNECTOR_DIR/config/envoy-ext-proc-streaming.yaml.in"
PREPARE_ENVOY_CONFIG="$CONNECTOR_DIR/config/prepare_envoy_ext_proc_config.sh"
VERSION_LOCK="$CONNECTOR_DIR/config/envoy-ext-proc-versions.env"
ENVOY_CONFIG="$RUNTIME_ROOT/envoy-ext-proc.streaming.yaml"
SUMMARY="$RUNTIME_ROOT/runtime-summary.txt"
ENVOY_STDOUT="$RUNTIME_ROOT/envoy.stdout.log"
ENVOY_STDERR="$RUNTIME_ROOT/envoy.stderr.log"
SERVICE_STDOUT="$RUNTIME_ROOT/ext-proc.stdout.log"
SERVICE_STDERR="$RUNTIME_ROOT/ext-proc.stderr.log"
UPSTREAM_STDOUT="$RUNTIME_ROOT/upstream.stdout.log"
UPSTREAM_STDERR="$RUNTIME_ROOT/upstream.stderr.log"
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
[ -f "$VERSION_LOCK" ] || missing_dependency "Envoy ext_proc version lock is missing: $VERSION_LOCK"
[ -f "$HELPER" ] || missing_dependency "smoke helper is missing: $HELPER"
command -v "$PYTHON_BIN" >/dev/null 2>&1 || missing_dependency "Python interpreter is missing: $PYTHON_BIN"

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
case "$EVENT_LOG_PATH" in
    "$RUNTIME_ROOT"/*) ;;
    *) echo "envoy_ext_proc_runtime: FAIL - EVENT_LOG_PATH must be under RUNTIME_ROOT" >&2; exit 1 ;;
esac
mkdir -p "$RUNTIME_ROOT"
rm -f "$EVENT_LOG_PATH" "$SUMMARY"

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

if ! grep -Fq 'name: envoy.filters.http.ext_proc' "$ENVOY_CONFIG" || \
    grep -Fq 'name: envoy.filters.http.ext_authz' "$ENVOY_CONFIG" || \
    ! grep -Fq 'request_body_mode: STREAMED' "$ENVOY_CONFIG" || \
    ! grep -Fq 'response_body_mode: STREAMED' "$ENVOY_CONFIG"; then
    echo "envoy_ext_proc_runtime: FAIL - generated config does not select streamed ext_proc only" >&2
    exit 1
fi

"$EXT_PROC_BIN" --check-config --config "$EXT_PROC_CONFIG" \
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
    >"$UPSTREAM_STDOUT" 2>"$UPSTREAM_STDERR" &
upstream_pid=$!

EXT_PROC_BIN="$EXT_PROC_BIN" EXT_PROC_CONFIG="$EXT_PROC_CONFIG" \
    EVENT_LOG_PATH="$EVENT_LOG_PATH" LISTEN_ADDRESS=127.0.0.1 \
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

event_ready=0
attempt=0
while [ "$attempt" -lt 20 ]; do
    attempt=$((attempt + 1))
    if [ -s "$EVENT_LOG_PATH" ] && \
        grep -Fq '"transaction_id":"envoy-ext-proc-stream-1"' "$EVENT_LOG_PATH" && \
        grep -Fq '"integration_mode":"ext_proc"' "$EVENT_LOG_PATH" && \
        grep -Fq '"evaluation_mode":"passthrough_nonpromoted"' "$EVENT_LOG_PATH" && \
        grep -Fq '"rule_evaluation":"not_wired"' "$EVENT_LOG_PATH" && \
        grep -Eq '"request_body_bytes":[1-9][0-9]*' "$EVENT_LOG_PATH" && \
        grep -Eq '"response_body_bytes":[1-9][0-9]*' "$EVENT_LOG_PATH"; then
        event_ready=1
        break
    fi
    sleep 1
done
if [ "$event_ready" -ne 1 ]; then
    echo "envoy_ext_proc_runtime: FAIL - missing streamed ext_proc metadata evidence" >&2
    sed -n '1,80p' "$EVENT_LOG_PATH" >&2 || true
    exit 1
fi
if grep -Fq 'request-body-for-ext-proc' "$EVENT_LOG_PATH" || \
    grep -Fq 'envoy connector upstream ok' "$EVENT_LOG_PATH"; then
    echo "envoy_ext_proc_runtime: FAIL - metadata evidence contains a body payload" >&2
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

{
    printf 'status=PASS\n'
    printf 'integration_mode=ext_proc\n'
    printf 'envoy_release=%s\n' "$pinned_envoy_release"
    printf 'evaluation_mode=passthrough_nonpromoted\n'
    printf 'rule_evaluation=not_wired\n'
    printf 'common_runtime_bridge=false\n'
    printf 'capability_promotion=not_permitted\n'
    printf 'allowed_request_status=%s\n' "$allowed_status"
    printf 'streamed_request_status=%s\n' "$streamed_status"
    printf 'request_body_stream_observed=true\n'
    printf 'response_body_stream_observed=true\n'
    printf 'event_log=%s\n' "$EVENT_LOG_PATH"
    printf 'envoy_config=%s\n' "$ENVOY_CONFIG"
    printf 'response_body_rule_evaluation=not_implemented\n'
    printf 'production_ready=false\n'
} > "$SUMMARY"

cleanup
envoy_pid=
service_pid=
upstream_pid=
trap - EXIT HUP INT TERM
printf 'processes_stopped=yes\n' >> "$SUMMARY"
printf 'envoy_ext_proc_runtime: pass (non-promoted) summary=%s\n' "$SUMMARY"
