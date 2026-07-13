#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
CONNECTOR_ROOT=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
REPO_ROOT=$(CDPATH= cd "$CONNECTOR_ROOT/../.." && pwd)
BUILD_ROOT="${BUILD_ROOT:-${TMPDIR:-/var/tmp}/ModSecurity-conector-verified/build}"
COMPONENT_CACHE="${CONNECTOR_COMPONENT_CACHE:-${TMPDIR:-/var/tmp}/ModSecurity-conector-verified/cache-v2/shared}"
CONNECTOR_BIN="${TRAEFIK_CONNECTOR_BIN:-$BUILD_ROOT/traefik-connector/traefik-forwardauth}"
TRAEFIK_BIN="${TRAEFIK_BIN:-$COMPONENT_CACHE/traefik/bin/traefik}"
CONFIG_PATH="${TRAEFIK_CONNECTOR_CONFIG:-$CONNECTOR_ROOT/config/traefik-forwardauth.conf}"
TRAEFIK_TEMPLATE="${TRAEFIK_CONNECTOR_TRAEFIK_CONFIG:-$CONNECTOR_ROOT/config/traefik-forwardauth-dynamic.yaml}"
SERVICE_LISTEN="${TRAEFIK_CONNECTOR_LISTEN:-127.0.0.1:19090}"
TRAEFIK_LISTEN="${TRAEFIK_START_LISTEN:-127.0.0.1:19080}"
UPSTREAM_ADDRESS="${TRAEFIK_START_UPSTREAM:-127.0.0.1:19091}"
START_ROOT="${TRAEFIK_CONNECTOR_START_ROOT:-$BUILD_ROOT/traefik-connector/start-smoke}"
SERVICE_STDOUT="$START_ROOT/service.stdout.log"
SERVICE_STDERR="$START_ROOT/service.stderr.log"
TRAEFIK_STDOUT="$START_ROOT/traefik.stdout.log"
TRAEFIK_STDERR="$START_ROOT/traefik.stderr.log"
CONFIG_STDOUT="$START_ROOT/config-check.stdout.log"
CONFIG_STDERR="$START_ROOT/config-check.stderr.log"
SERVICE_PID_FILE="$START_ROOT/service.pid"
TRAEFIK_PID_FILE="$START_ROOT/traefik.pid"
TRAEFIK_CONFIG="$START_ROOT/traefik-dynamic.yaml"
service_pid=""
traefik_pid=""

case "$START_ROOT" in
    /*) ;;
    *) echo "BLOCKED: TRAEFIK_CONNECTOR_START_ROOT must be absolute: $START_ROOT" >&2; exit 77 ;;
esac
case "$START_ROOT" in
    /|/tmp|/var/tmp)
        echo "BLOCKED: TRAEFIK_CONNECTOR_START_ROOT is too broad: $START_ROOT" >&2
        exit 77
        ;;
esac
case "$START_ROOT" in
    "$REPO_ROOT"|"$REPO_ROOT"/*)
        echo "BLOCKED: start-smoke output must be outside the checkout: $START_ROOT" >&2
        exit 77
        ;;
esac
if [ -L "$START_ROOT" ]; then
    echo "BLOCKED: TRAEFIK_CONNECTOR_START_ROOT must not be a symlink: $START_ROOT" >&2
    exit 77
fi

require_executable() {
    executable=$1
    label=$2
    case "$executable" in
        /*) ;;
        *) echo "BLOCKED: $label binary must be an absolute path: $executable" >&2; exit 77 ;;
    esac
    case "$executable" in
        /usr/*|/bin/*|/sbin/*|/opt/*)
            echo "BLOCKED: $label binary must not use a global system path: $executable" >&2
            exit 77
            ;;
    esac
    if [ ! -x "$executable" ]; then
        echo "BLOCKED: $label binary is not executable: $executable" >&2
        exit 77
    fi
}

require_loopback_address() {
    address=$1
    label=$2
    case "$address" in
        127.0.0.1:*) port=${address#127.0.0.1:} ;;
        *) echo "BLOCKED: $label must use 127.0.0.1:PORT: $address" >&2; exit 77 ;;
    esac
    case "$port" in
        ''|*[!0-9]*) echo "BLOCKED: $label has an invalid port: $address" >&2; exit 77 ;;
    esac
}

require_executable "$CONNECTOR_BIN" "Traefik forwardAuth connector"
require_executable "$TRAEFIK_BIN" "Traefik"
require_loopback_address "$SERVICE_LISTEN" "TRAEFIK_CONNECTOR_LISTEN"
require_loopback_address "$TRAEFIK_LISTEN" "TRAEFIK_START_LISTEN"
require_loopback_address "$UPSTREAM_ADDRESS" "TRAEFIK_START_UPSTREAM"
if [ ! -f "$CONFIG_PATH" ]; then
    echo "BLOCKED: Traefik forwardAuth connector config is missing: $CONFIG_PATH" >&2
    exit 77
fi
if [ ! -f "$TRAEFIK_TEMPLATE" ]; then
    echo "BLOCKED: Traefik File Provider config template is missing: $TRAEFIK_TEMPLATE" >&2
    exit 77
fi

cleanup() {
    if [ -n "$traefik_pid" ] && kill -0 "$traefik_pid" 2>/dev/null; then
        kill "$traefik_pid" 2>/dev/null || true
        wait "$traefik_pid" 2>/dev/null || true
    fi
    if [ -n "$service_pid" ] && kill -0 "$service_pid" 2>/dev/null; then
        kill "$service_pid" 2>/dev/null || true
        wait "$service_pid" 2>/dev/null || true
    fi
    rm -f "$SERVICE_PID_FILE" "$TRAEFIK_PID_FILE"
}
trap cleanup EXIT HUP INT TERM

rm -rf "$START_ROOT"
mkdir -p "$START_ROOT"
sed \
    -e "s|__AUTH_ADDRESS__|$SERVICE_LISTEN|g" \
    -e "s|__UPSTREAM_ADDRESS__|$UPSTREAM_ADDRESS|g" \
    "$TRAEFIK_TEMPLATE" > "$TRAEFIK_CONFIG"

(
    cd "$REPO_ROOT"
    exec "$CONNECTOR_BIN" --check-config --config "$CONFIG_PATH"
) >"$CONFIG_STDOUT" 2>"$CONFIG_STDERR" || {
    rc=$?
    echo "FAIL: Traefik connector config check failed (rc=$rc)" >&2
    sed -n '1,160p' "$CONFIG_STDERR" >&2
    exit "$rc"
}

(
    cd "$REPO_ROOT"
    exec "$CONNECTOR_BIN" \
        --serve \
        --config "$CONFIG_PATH" \
        --listen "$SERVICE_LISTEN"
) >"$SERVICE_STDOUT" 2>"$SERVICE_STDERR" &
service_pid=$!
printf '%s\n' "$service_pid" > "$SERVICE_PID_FILE"

"$TRAEFIK_BIN" \
    "--entryPoints.web.address=$TRAEFIK_LISTEN" \
    "--providers.file.filename=$TRAEFIK_CONFIG" \
    --providers.file.watch=false \
    --api=false \
    --log.level=ERROR \
    --global.sendAnonymousUsage=false \
    >"$TRAEFIK_STDOUT" 2>"$TRAEFIK_STDERR" &
traefik_pid=$!
printf '%s\n' "$traefik_pid" > "$TRAEFIK_PID_FILE"

attempt=0
while [ "$attempt" -lt 20 ]; do
    if ! kill -0 "$service_pid" 2>/dev/null; then
        wait "$service_pid" || rc=$?
        rc=${rc:-1}
        echo "FAIL: Traefik forwardAuth service exited during start smoke (rc=$rc)" >&2
        sed -n '1,160p' "$SERVICE_STDERR" >&2
        exit "$rc"
    fi
    if ! kill -0 "$traefik_pid" 2>/dev/null; then
        wait "$traefik_pid" || rc=$?
        rc=${rc:-1}
        echo "FAIL: Traefik exited during start smoke (rc=$rc)" >&2
        sed -n '1,160p' "$TRAEFIK_STDERR" >&2
        exit "$rc"
    fi
    attempt=$((attempt + 1))
    sleep 0.1
done

if [ -s "$TRAEFIK_STDERR" ]; then
    echo "FAIL: Traefik reported a configuration/start error" >&2
    sed -n '1,160p' "$TRAEFIK_STDERR" >&2
    exit 1
fi

printf 'traefik_connector_start_smoke=pass\n'
printf 'service_listen=%s\n' "$SERVICE_LISTEN"
printf 'traefik_listen=%s\n' "$TRAEFIK_LISTEN"
printf 'service_pid=%s\n' "$service_pid"
printf 'traefik_pid=%s\n' "$traefik_pid"
printf 'traefik_config=%s\n' "$TRAEFIK_CONFIG"
printf 'service_stdout_log=%s\n' "$SERVICE_STDOUT"
printf 'service_stderr_log=%s\n' "$SERVICE_STDERR"
printf 'traefik_stdout_log=%s\n' "$TRAEFIK_STDOUT"
printf 'traefik_stderr_log=%s\n' "$TRAEFIK_STDERR"
