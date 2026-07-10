#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
CONNECTOR_DIR=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
REPO_ROOT=$(CDPATH= cd "$CONNECTOR_DIR/../.." && pwd)
BUILD_ROOT=${BUILD_ROOT:-${XDG_STATE_HOME:-${HOME:-/tmp}/.local/state}/ModSecurity-conector-build}
SERVICE_BIN=${SERVICE_BIN:-$BUILD_ROOT/envoy-connector/msconnector_envoy_ext_authz}
CONFIG_FILE=${CONFIG_FILE:-$CONNECTOR_DIR/config/envoy-ext-authz.conf}
RULES_FILE=${RULES_FILE:-$REPO_ROOT/common/rules/modsecurity_targeted_smoke.conf}
EVENT_LOG_PATH=${EVENT_LOG_PATH:-$BUILD_ROOT/envoy-connector/start-smoke/events.jsonl}
PYTHON_BIN=${PYTHON:-python3}
HELPER="$SCRIPT_DIR/envoy_smoke_helper.py"
YAML_TEMPLATE="$CONNECTOR_DIR/config/envoy-ext-authz-smoke.yaml.in"
START_ROOT=${START_ROOT:-$BUILD_ROOT/envoy-connector/start-smoke}
ENVOY_CONFIG="$START_ROOT/envoy.yaml"
ENVOY_STDOUT="$START_ROOT/envoy.stdout.log"
ENVOY_STDERR="$START_ROOT/envoy.stderr.log"
SERVICE_STDOUT="$START_ROOT/service.stdout.log"
SERVICE_STDERR="$START_ROOT/service.stderr.log"
SUMMARY="$START_ROOT/start-summary.txt"
envoy_pid=
service_pid=

missing_dependency() {
    echo "envoy_start_smoke: BLOCKED - $1" >&2
    exit 77
}

cleanup() {
    for pid in "$envoy_pid" "$service_pid"; do
        if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
            kill "$pid" 2>/dev/null || true
        fi
    done
    for pid in "$envoy_pid" "$service_pid"; do
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
[ -f "$HELPER" ] || missing_dependency "smoke helper is missing: $HELPER"
[ -f "$YAML_TEMPLATE" ] || missing_dependency "Envoy config template is missing: $YAML_TEMPLATE"
command -v "$PYTHON_BIN" >/dev/null 2>&1 || missing_dependency "Python interpreter is missing: $PYTHON_BIN"

case "$START_ROOT" in
    /*) ;;
    *) echo "envoy_start_smoke: FAIL - START_ROOT must be absolute" >&2; exit 1 ;;
esac
case "$START_ROOT" in
    "$REPO_ROOT"|"$REPO_ROOT"/*)
        echo "envoy_start_smoke: FAIL - START_ROOT must not be inside the checkout" >&2
        exit 1
        ;;
esac
mkdir -p "$START_ROOT"
rm -f "$SUMMARY"

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
    --base-id "$base_id" --disable-hot-restart >"$START_ROOT/envoy-validate.stdout.log" \
    2>"$START_ROOT/envoy-validate.stderr.log"; then
    echo "envoy_start_smoke: FAIL - Envoy rejected generated config" >&2
    sed -n '1,160p' "$START_ROOT/envoy-validate.stderr.log" >&2 || true
    exit 1
fi

SERVICE_BIN="$SERVICE_BIN" BUILD_ROOT="$BUILD_ROOT" CONFIG_FILE="$CONFIG_FILE" \
    RULES_FILE="$RULES_FILE" EVENT_LOG_PATH="$EVENT_LOG_PATH" \
    LISTEN_ADDRESS=127.0.0.1 LISTEN_PORT="$authz_port" \
    sh "$SCRIPT_DIR/serve_envoy_connector.sh" >"$SERVICE_STDOUT" 2>"$SERVICE_STDERR" &
service_pid=$!

"$ENVOY_BIN" -c "$ENVOY_CONFIG" --base-id "$base_id" --disable-hot-restart \
    --log-level error >"$ENVOY_STDOUT" 2>"$ENVOY_STDERR" &
envoy_pid=$!

sleep 1
if ! kill -0 "$service_pid" 2>/dev/null; then
    echo "envoy_start_smoke: FAIL - connector service exited before liveness check" >&2
    sed -n '1,160p' "$SERVICE_STDERR" >&2 || true
    exit 1
fi
if ! kill -0 "$envoy_pid" 2>/dev/null; then
    echo "envoy_start_smoke: FAIL - Envoy exited before liveness check" >&2
    sed -n '1,160p' "$ENVOY_STDERR" >&2 || true
    exit 1
fi

{
    printf 'connector_config_check=pass\n'
    printf 'envoy_config_validate=pass\n'
    printf 'service_process_started=yes\n'
    printf 'service_pid=%s\n' "$service_pid"
    printf 'envoy_process_started=yes\n'
    printf 'envoy_pid=%s\n' "$envoy_pid"
    printf 'envoy_listen=127.0.0.1:%s\n' "$listen_port"
    printf 'authz_listen=127.0.0.1:%s\n' "$authz_port"
    printf 'requests_sent=no\n'
} > "$SUMMARY"

cleanup
envoy_pid=
service_pid=
trap - EXIT HUP INT TERM
printf 'service_process_stopped=yes\n' >> "$SUMMARY"
printf 'envoy_process_stopped=yes\n' >> "$SUMMARY"
printf 'envoy_start_smoke: pass summary=%s\n' "$SUMMARY"
