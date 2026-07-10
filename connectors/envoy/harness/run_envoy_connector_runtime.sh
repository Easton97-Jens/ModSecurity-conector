#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
CONNECTOR_DIR=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
REPO_ROOT=$(CDPATH= cd "$CONNECTOR_DIR/../.." && pwd)
BUILD_ROOT=${BUILD_ROOT:-${XDG_STATE_HOME:-${HOME:-/tmp}/.local/state}/ModSecurity-conector-build}
SERVICE_BIN=${SERVICE_BIN:-$BUILD_ROOT/envoy-connector/msconnector_envoy_ext_authz}
CONFIG_FILE=${CONFIG_FILE:-$CONNECTOR_DIR/config/envoy-ext-authz.conf}
RULES_FILE=${RULES_FILE:-$REPO_ROOT/common/rules/modsecurity_targeted_smoke.conf}
RUNTIME_ROOT=${RUNTIME_ROOT:-$BUILD_ROOT/envoy-connector/runtime-smoke}
EVENT_LOG_PATH=${EVENT_LOG_PATH:-$RUNTIME_ROOT/events.jsonl}
PYTHON_BIN=${PYTHON:-python3}
HELPER="$SCRIPT_DIR/envoy_smoke_helper.py"
YAML_TEMPLATE="$CONNECTOR_DIR/config/envoy-ext-authz-smoke.yaml.in"
ENVOY_CONFIG="$RUNTIME_ROOT/envoy.yaml"
SUMMARY="$RUNTIME_ROOT/runtime-summary.txt"
ENVOY_STDOUT="$RUNTIME_ROOT/envoy.stdout.log"
ENVOY_STDERR="$RUNTIME_ROOT/envoy.stderr.log"
SERVICE_STDOUT="$RUNTIME_ROOT/service.stdout.log"
SERVICE_STDERR="$RUNTIME_ROOT/service.stderr.log"
UPSTREAM_STDOUT="$RUNTIME_ROOT/upstream.stdout.log"
UPSTREAM_STDERR="$RUNTIME_ROOT/upstream.stderr.log"
envoy_pid=
service_pid=
upstream_pid=

missing_dependency() {
    echo "envoy_runtime_smoke: BLOCKED - $1" >&2
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
[ -x "$SERVICE_BIN" ] || missing_dependency "connector service is not executable: $SERVICE_BIN"
[ -f "$RULES_FILE" ] || missing_dependency "rules file is missing: $RULES_FILE"
[ -f "$YAML_TEMPLATE" ] || missing_dependency "Envoy config template is missing: $YAML_TEMPLATE"
[ -f "$HELPER" ] || missing_dependency "smoke helper is missing: $HELPER"
command -v "$PYTHON_BIN" >/dev/null 2>&1 || missing_dependency "Python interpreter is missing: $PYTHON_BIN"

case "$RUNTIME_ROOT" in
    /*) ;;
    *) echo "envoy_runtime_smoke: FAIL - RUNTIME_ROOT must be absolute" >&2; exit 1 ;;
esac
case "$RUNTIME_ROOT" in
    "$REPO_ROOT"|"$REPO_ROOT"/*)
        echo "envoy_runtime_smoke: FAIL - RUNTIME_ROOT must not be inside the checkout" >&2
        exit 1
        ;;
esac
mkdir -p "$RUNTIME_ROOT"
case "$EVENT_LOG_PATH" in
    "$RUNTIME_ROOT"/*) ;;
    *)
        echo "envoy_runtime_smoke: FAIL - EVENT_LOG_PATH must be under RUNTIME_ROOT" >&2
        exit 1
        ;;
esac
rm -f "$EVENT_LOG_PATH" "$SUMMARY"

set -- $("$PYTHON_BIN" "$HELPER" free-ports --count 4)
listen_port=${ENVOY_SMOKE_PORT:-$1}
upstream_port=${ENVOY_UPSTREAM_PORT:-$2}
authz_port=${ENVOY_AUTHZ_PORT:-$3}
admin_port=${ENVOY_ADMIN_PORT:-$4}
base_id=$(((listen_port + admin_port) % 100000))

sed \
    -e "s|@LISTEN_PORT@|$listen_port|g" \
    -e "s|@UPSTREAM_PORT@|$upstream_port|g" \
    -e "s|@AUTHZ_PORT@|$authz_port|g" \
    -e "s|@ADMIN_PORT@|$admin_port|g" \
    "$YAML_TEMPLATE" > "$ENVOY_CONFIG"

SERVICE_BIN="$SERVICE_BIN" BUILD_ROOT="$BUILD_ROOT" CONFIG_FILE="$CONFIG_FILE" \
    RULES_FILE="$RULES_FILE" EVENT_LOG_PATH="$EVENT_LOG_PATH" \
    sh "$CONNECTOR_DIR/config/check_envoy_config.sh"

if ! "$ENVOY_BIN" --mode validate -c "$ENVOY_CONFIG" \
    --base-id "$base_id" --disable-hot-restart >"$RUNTIME_ROOT/envoy-validate.stdout.log" \
    2>"$RUNTIME_ROOT/envoy-validate.stderr.log"; then
    echo "envoy_runtime_smoke: FAIL - Envoy rejected generated config" >&2
    sed -n '1,160p' "$RUNTIME_ROOT/envoy-validate.stderr.log" >&2 || true
    exit 1
fi

"$PYTHON_BIN" "$HELPER" serve-upstream --port "$upstream_port" \
    >"$UPSTREAM_STDOUT" 2>"$UPSTREAM_STDERR" &
upstream_pid=$!

SERVICE_BIN="$SERVICE_BIN" BUILD_ROOT="$BUILD_ROOT" CONFIG_FILE="$CONFIG_FILE" \
    RULES_FILE="$RULES_FILE" EVENT_LOG_PATH="$EVENT_LOG_PATH" \
    LISTEN_ADDRESS=127.0.0.1 LISTEN_PORT="$authz_port" \
    sh "$SCRIPT_DIR/serve_envoy_connector.sh" >"$SERVICE_STDOUT" 2>"$SERVICE_STDERR" &
service_pid=$!

"$ENVOY_BIN" -c "$ENVOY_CONFIG" --base-id "$base_id" --disable-hot-restart \
    --log-level error >"$ENVOY_STDOUT" 2>"$ENVOY_STDERR" &
envoy_pid=$!

allowed_status=
attempt=0
while [ "$attempt" -lt 30 ]; do
    attempt=$((attempt + 1))
    for process_pair in "envoy:$envoy_pid" "service:$service_pid" "upstream:$upstream_pid"; do
        process_name=${process_pair%%:*}
        process_id=${process_pair##*:}
        if ! kill -0 "$process_id" 2>/dev/null; then
            echo "envoy_runtime_smoke: FAIL - $process_name process exited early" >&2
            sed -n '1,160p' "$ENVOY_STDERR" >&2 || true
            sed -n '1,160p' "$SERVICE_STDERR" >&2 || true
            exit 1
        fi
    done
    set +e
    allowed_status=$("$PYTHON_BIN" "$HELPER" probe \
        --url "http://127.0.0.1:$listen_port/allowed" \
        --header "X-Request-Id: envoy-allow-1" 2>/dev/null)
    probe_rc=$?
    set -e
    if [ "$probe_rc" -eq 0 ] && [ "$allowed_status" = "200" ]; then
        break
    fi
    sleep 1
done

if [ "$allowed_status" != "200" ]; then
    echo "envoy_runtime_smoke: FAIL - allowed request returned ${allowed_status:-no status}, expected 200" >&2
    exit 1
fi

if ! blocked_status=$("$PYTHON_BIN" "$HELPER" probe \
    --url "http://127.0.0.1:$listen_port/blocked" \
    --header "X-Request-Id: envoy-block-1" \
    --header "X-Modsec-Smoke: block"); then
    echo "envoy_runtime_smoke: FAIL - blocked request could not be completed" >&2
    exit 1
fi
if [ "$blocked_status" != "403" ]; then
    echo "envoy_runtime_smoke: FAIL - blocked request returned $blocked_status, expected 403" >&2
    exit 1
fi
if [ ! -s "$EVENT_LOG_PATH" ]; then
    echo "envoy_runtime_smoke: FAIL - metadata event log was not produced: $EVENT_LOG_PATH" >&2
    exit 1
fi
if ! grep -q '"rule_id":"1000001"' "$EVENT_LOG_PATH" ||
    ! grep -q '"transaction_id":"envoy-block-1"' "$EVENT_LOG_PATH"; then
    echo "envoy_runtime_smoke: FAIL - event log lacks rule/transaction evidence" >&2
    exit 1
fi
for process_pair in "envoy:$envoy_pid" "service:$service_pid" "upstream:$upstream_pid"; do
    process_name=${process_pair%%:*}
    process_id=${process_pair##*:}
    if ! kill -0 "$process_id" 2>/dev/null; then
        echo "envoy_runtime_smoke: FAIL - $process_name was not stable after requests" >&2
        exit 1
    fi
done

{
    printf 'status=PASS\n'
    printf 'integration_mode=ext_authz\n'
    printf 'allowed_request_status=%s\n' "$allowed_status"
    printf 'blocked_request_status=%s\n' "$blocked_status"
    printf 'rule_id=1000001\n'
    printf 'event_log=%s\n' "$EVENT_LOG_PATH"
    printf 'envoy_config=%s\n' "$ENVOY_CONFIG"
    printf 'response_body_verified=false\n'
    printf 'production_ready=false\n'
} > "$SUMMARY"

cleanup
envoy_pid=
service_pid=
upstream_pid=
trap - EXIT HUP INT TERM
printf 'processes_stopped=yes\n' >> "$SUMMARY"
printf 'envoy_runtime_smoke: pass summary=%s\n' "$SUMMARY"
