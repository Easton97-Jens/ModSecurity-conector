#!/bin/sh
set -eu

CONNECTOR_NAME=haproxy
SOURCE_ROOT="${SOURCE_ROOT:-/src}"
BUILD_ROOT="${BUILD_ROOT:-/src/ModSecurity-conector-build}"
RESULTS_DIR="${RESULTS_DIR:-$BUILD_ROOT/results}"
TMP_ROOT="${TMP_ROOT:-$BUILD_ROOT/tmp}"
LOG_ROOT="${LOG_ROOT:-$BUILD_ROOT/logs}"
SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
HARNESS_PATH="$SCRIPT_DIR/$(basename "$0")"
DEFAULT_CONNECTOR_ROOT=$(CDPATH= cd "$SCRIPT_DIR/../../.." && pwd)
CONNECTOR_ROOT="${CONNECTOR_ROOT:-$DEFAULT_CONNECTOR_ROOT}"
CONNECTOR_ROOT=$(CDPATH= cd "$CONNECTOR_ROOT" && pwd)
CONNECTOR_DIR="$CONNECTOR_ROOT/connectors/$CONNECTOR_NAME"
LOG_DIR="$LOG_ROOT/$CONNECTOR_NAME-runtime-smoke"
COMMON_SH="$CONNECTOR_ROOT/modules/ModSecurity-test-Framework/ci/common.sh"
FRAMEWORK_ROOT="$CONNECTOR_ROOT/modules/ModSecurity-test-Framework"
if [ -f "$COMMON_SH" ]; then
    . "$COMMON_SH"
fi
PYTHON_BIN="${PYTHON:-$(ci_python 2>/dev/null || printf python3)}"
PREPARE_HAPROXY_RUNTIME="$FRAMEWORK_ROOT/ci/prepare-haproxy-runtime.sh"
HAPROXY_BIN="${HAPROXY_BIN:-$BUILD_ROOT/haproxy-runtime/haproxy/sbin/haproxy}"
SPOA_STARTER_BIN="$BUILD_ROOT/haproxy-build-starter/haproxy-spoa-agent-starter"
SPOA_RUNTIME_BIN="$BUILD_ROOT/haproxy-spoa-runtime/haproxy-spoa-diagnostic-runtime"
SPOE_RUNTIME_DIR="$BUILD_ROOT/haproxy-runtime/spoe"
HAPROXY_CFG_EXAMPLE="$CONNECTOR_DIR/poc/spoe/haproxy.cfg.example"
SPOE_AGENT_CFG_EXAMPLE="$CONNECTOR_DIR/poc/spoe/spoe-agent.conf.example"
NOTE="Build/self-test starter evidence is available via make connector-starter-checks but is not runtime smoke evidence."
RUN_ID="${RUN_ID:-$CONNECTOR_NAME-$(date -u +%Y%m%dT%H%M%SZ)-$$}"
RUN_TMP_DIR="$TMP_ROOT/$CONNECTOR_NAME/$RUN_ID"
RUNTIME_LOG_DIR="$LOG_ROOT/$CONNECTOR_NAME/$RUN_ID"
RUN_SPOE_RUNTIME_DIR="$SPOE_RUNTIME_DIR/$RUN_ID"
GENERATED_HAPROXY_CFG="$RUN_SPOE_RUNTIME_DIR/haproxy.cfg"
GENERATED_SPOE_CFG="$RUN_SPOE_RUNTIME_DIR/spoe-agent.conf"
PREPARE_STATUS=not-run
PREPARE_REASON=
SPOA_RUNTIME_STATUS=not-run
SPOA_PROTOCOL_RUNTIME_VERIFIED=false
SPOA_RUNTIME_REASON=
SPOE_CONFIG_STATUS=not-run
SPOE_RUNTIME_STATUS=not-verified
SPOE_RUNTIME_VERIFIED=false
SPOE_RUNTIME_BLOCKER="spoe runtime integration not verified"
HAPROXY_RUNTIME_STARTED=false
DIAGNOSTIC_AGENT_STARTED=false
HTTP_PROBE_STATUS=not-run
HAPROXY_CONTACTED_DIAGNOSTIC_AGENT=false
AGENT_CONTACT_EVIDENCE=
HAPROXY_PORT=
SPOA_PORT=
AGENT_PID=
HAPROXY_PID=
BACKEND_PID=
DIAGNOSTIC_AGENT_LOG="$RUNTIME_LOG_DIR/diagnostic-agent.log"
HAPROXY_RUNTIME_LOG="$RUNTIME_LOG_DIR/haproxy-runtime.stderr.log"
HAPROXY_RUNTIME_STDOUT_LOG="$RUNTIME_LOG_DIR/haproxy-runtime.stdout.log"
HTTP_PROBE_LOG="$RUNTIME_LOG_DIR/http-probe.log"
BACKEND_DOCROOT="$RUN_TMP_DIR/backend-docroot"
BACKEND_RUNTIME_LOG="$RUNTIME_LOG_DIR/backend.stderr.log"
BACKEND_RUNTIME_STDOUT_LOG="$RUNTIME_LOG_DIR/backend.stdout.log"
BACKEND_RUNTIME_STARTED=false
BACKEND_PORT=

blocked_root() {
    echo "$CONNECTOR_NAME runtime smoke: BLOCKED - $*" >&2
    exit 77
}

cleanup_runtime() {
    if [ -n "${HAPROXY_PID:-}" ]; then
        kill "$HAPROXY_PID" 2>/dev/null || true
        wait "$HAPROXY_PID" 2>/dev/null || true
        HAPROXY_PID=
    fi
    if [ -n "${AGENT_PID:-}" ]; then
        kill "$AGENT_PID" 2>/dev/null || true
        wait "$AGENT_PID" 2>/dev/null || true
        AGENT_PID=
    fi
    if [ -n "${BACKEND_PID:-}" ]; then
        kill "$BACKEND_PID" 2>/dev/null || true
        wait "$BACKEND_PID" 2>/dev/null || true
        BACKEND_PID=
    fi
}

trap cleanup_runtime EXIT INT TERM

require_src_path() {
    path=$1
    label=$2
    case "$path" in
        /src|/src/*) ;;
        /*) blocked_root "$label must be under /src: $path" ;;
        *) blocked_root "$label must be absolute and under /src: $path" ;;
    esac
}

require_build_path() {
    path=$1
    label=$2
    case "$path" in
        "$BUILD_ROOT"|"$BUILD_ROOT"/*) ;;
        *) blocked_root "$label must be under BUILD_ROOT: $path" ;;
    esac
}

require_results_path() {
    path=$1
    label=$2
    case "$path" in
        "$BUILD_ROOT/results"|"$BUILD_ROOT/results"/*) ;;
        *) blocked_root "$label must be under BUILD_ROOT/results: $path" ;;
    esac
}

require_log_path() {
    path=$1
    label=$2
    case "$path" in
        "$BUILD_ROOT/logs"|"$BUILD_ROOT/logs"/*) ;;
        *) blocked_root "$label must be under BUILD_ROOT/logs: $path" ;;
    esac
}

require_not_connector_artifact() {
    path=$1
    label=$2
    case "$path" in
        "$CONNECTOR_DIR"|"$CONNECTOR_DIR"/*) blocked_root "$label must not be inside connector checkout: $path" ;;
        *) ;;
    esac
}

validate_roots() {
    [ -d "$CONNECTOR_DIR" ] || blocked_root "CONNECTOR_ROOT does not contain connectors/$CONNECTOR_NAME"
    command -v "$PYTHON_BIN" >/dev/null 2>&1 || blocked_root "missing Python interpreter: $PYTHON_BIN"
    require_src_path "$SOURCE_ROOT" SOURCE_ROOT
    require_src_path "$BUILD_ROOT" BUILD_ROOT
    require_results_path "$RESULTS_DIR" RESULTS_DIR
    require_build_path "$TMP_ROOT" TMP_ROOT
    require_log_path "$LOG_ROOT" LOG_ROOT
    require_log_path "$LOG_DIR" LOG_DIR
    require_log_path "$RUNTIME_LOG_DIR" RUNTIME_LOG_DIR
    require_build_path "$HAPROXY_BIN" HAPROXY_BIN
    require_build_path "$SPOA_RUNTIME_BIN" SPOA_RUNTIME_BIN
    require_build_path "$SPOE_RUNTIME_DIR" SPOE_RUNTIME_DIR
    require_build_path "$RUN_SPOE_RUNTIME_DIR" RUN_SPOE_RUNTIME_DIR
    require_build_path "$GENERATED_HAPROXY_CFG" GENERATED_HAPROXY_CFG
    require_build_path "$GENERATED_SPOE_CFG" GENERATED_SPOE_CFG
    require_build_path "$RUN_TMP_DIR" RUN_TMP_DIR
    require_build_path "$BACKEND_DOCROOT" BACKEND_DOCROOT
    require_not_connector_artifact "$RESULTS_DIR" RESULTS_DIR
    require_not_connector_artifact "$TMP_ROOT" TMP_ROOT
    require_not_connector_artifact "$LOG_ROOT" LOG_ROOT
    require_not_connector_artifact "$HAPROXY_BIN" HAPROXY_BIN
    require_not_connector_artifact "$SPOA_RUNTIME_BIN" SPOA_RUNTIME_BIN
    require_not_connector_artifact "$SPOE_RUNTIME_DIR" SPOE_RUNTIME_DIR
    require_not_connector_artifact "$RUN_SPOE_RUNTIME_DIR" RUN_SPOE_RUNTIME_DIR
    require_not_connector_artifact "$RUN_TMP_DIR" RUN_TMP_DIR
    require_not_connector_artifact "$RUNTIME_LOG_DIR" RUNTIME_LOG_DIR
    require_not_connector_artifact "$BACKEND_DOCROOT" BACKEND_DOCROOT
    mkdir -p "$RESULTS_DIR" "$TMP_ROOT" "$LOG_DIR" "$RUN_TMP_DIR" "$RUNTIME_LOG_DIR"
}

starter_available() {
    if [ -f "$CONNECTOR_DIR/Makefile" ] || [ -d "$CONNECTOR_DIR/build" ]; then
        printf true
    else
        printf false
    fi
}

detect_common_acquisition() {
    if [ ! -f "$COMMON_SH" ]; then
        printf missing-common
        return
    fi
    if grep -E '^HAPROXY_.*(URL|REF|SRC|SOURCE|BIN|BINARY|FETCH)' "$COMMON_SH" >/dev/null 2>&1; then
        printf defined
    else
        printf not-defined
    fi
}

read_prepare_reason() {
    status_file="$LOG_ROOT/haproxy-prepare/status.txt"
    if [ -f "$status_file" ]; then
        reason=$(grep '^blocked: ' "$status_file" | tail -n 1 | sed 's/^blocked: //')
        if [ -n "$reason" ]; then
            printf '%s' "$reason"
            return
        fi
    fi
    printf 'local HAProxy prepare did not produce a runtime binary'
}

ensure_local_haproxy() {
    if [ -x "$HAPROXY_BIN" ]; then
        PREPARE_STATUS=not-needed
        PREPARE_REASON="local HAProxy binary already exists"
        return
    fi
    if [ ! -x "$PREPARE_HAPROXY_RUNTIME" ]; then
        PREPARE_STATUS=missing-helper
        PREPARE_REASON="prepare-haproxy-runtime helper missing"
        return
    fi
    set +e
    SOURCE_ROOT="$SOURCE_ROOT" \
        BUILD_ROOT="$BUILD_ROOT" \
        TMP_ROOT="$TMP_ROOT" \
        LOG_ROOT="$LOG_ROOT" \
        CONNECTOR_ROOT="$CONNECTOR_ROOT" \
        FRAMEWORK_ROOT="$FRAMEWORK_ROOT" \
        sh "$PREPARE_HAPROXY_RUNTIME" >"$LOG_DIR/prepare-haproxy-runtime.log" 2>&1
    rc=$?
    set -e
    if [ "$rc" -eq 0 ] && [ -x "$HAPROXY_BIN" ]; then
        PREPARE_STATUS=ready
        PREPARE_REASON="local HAProxy binary prepared"
        return
    fi
    if [ "$rc" -eq 77 ]; then
        PREPARE_STATUS=blocked
        PREPARE_REASON=$(read_prepare_reason)
        return
    fi
    PREPARE_STATUS=failed
    PREPARE_REASON="prepare-haproxy-runtime failed with exit code $rc"
}

detect_spoa_starter() {
    if [ ! -x "$SPOA_STARTER_BIN" ]; then
        printf missing
        return
    fi
    if "$SPOA_STARTER_BIN" --describe >"$LOG_DIR/spoa-starter-describe.log" 2>&1; then
        printf self-test-only
    else
        printf describe-failed
    fi
}

run_spoa_runtime_self_test() {
    stdout_log="$LOG_DIR/spoa-runtime-self-test.stdout.log"
    stderr_log="$LOG_DIR/spoa-runtime-self-test.stderr.log"
    if [ ! -f "$CONNECTOR_DIR/Makefile" ]; then
        SPOA_RUNTIME_STATUS=missing
        SPOA_RUNTIME_REASON="connector Makefile missing"
        return
    fi
    set +e
    BUILD_ROOT="$BUILD_ROOT" \
        TMP_ROOT="$TMP_ROOT" \
        LOG_ROOT="$LOG_ROOT" \
        REPO_ROOT="$CONNECTOR_ROOT" \
        make -C "$CONNECTOR_DIR" self-test-spoa-runtime >"$stdout_log" 2>"$stderr_log"
    rc=$?
    set -e
    if [ "$rc" -eq 0 ] && [ -x "$SPOA_RUNTIME_BIN" ]; then
        SPOA_RUNTIME_STATUS=diagnostic-spop-handshake-subset
        SPOA_PROTOCOL_RUNTIME_VERIFIED=true
        SPOA_RUNTIME_REASON="minimal diagnostic SPOP handshake subset self-test passed"
        return
    fi
    if [ "$rc" -eq 77 ]; then
        SPOA_RUNTIME_STATUS=blocked
        SPOA_RUNTIME_REASON="minimal diagnostic SPOP handshake subset self-test blocked"
        return
    fi
    SPOA_RUNTIME_STATUS=failed
    SPOA_RUNTIME_REASON="minimal diagnostic SPOP handshake subset self-test failed with exit code $rc"
}

pick_tcp_port() {
    "$PYTHON_BIN" - <<'PY'
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind(("127.0.0.1", 0))
    print(sock.getsockname()[1])
PY
}

wait_tcp_port() {
    port=$1
    "$PYTHON_BIN" - "$port" <<'PY'
import socket
import sys
import time

port = int(sys.argv[1])
deadline = time.time() + 5
while time.time() < deadline:
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=0.2):
            sys.exit(0)
    except OSError:
        time.sleep(0.1)
sys.exit(1)
PY
}

run_http_probe() {
    port=$1
    status_file=$2
    response_file=$3
    "$PYTHON_BIN" - "$port" "$status_file" "$response_file" <<'PY'
import socket
import sys

port = int(sys.argv[1])
status_file = sys.argv[2]
response_file = sys.argv[3]
status = "probe-error"
data = b""
try:
    with socket.create_connection(("127.0.0.1", port), timeout=3) as sock:
        sock.sendall(
            b"GET /diagnostic.txt HTTP/1.1\r\n"
            b"Host: 127.0.0.1\r\n"
            b"Connection: close\r\n\r\n"
        )
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
    first = data.splitlines()[0].decode("ascii", "replace") if data else ""
    parts = first.split()
    if len(parts) >= 2 and parts[1].isdigit():
        status = parts[1]
except Exception as exc:
    status = "probe-error:" + str(exc)
with open(status_file, "w", encoding="utf-8") as handle:
    handle.write(status + "\n")
with open(response_file, "wb") as handle:
    handle.write(data)
sys.exit(0 if status in {"200", "204"} else 1)
PY
}

agent_contact_after_marker() {
    marker=$1
    log_file=$2
    [ -f "$log_file" ] || return 1
    awk -v marker="$marker" '
        index($0, marker) { seen = 1; next }
        seen && /HELLO received/ { found = 1; print; exit }
        END { exit found ? 0 : 1 }
    ' "$log_file" >"$RUNTIME_LOG_DIR/agent-contact-evidence.txt"
}

read_agent_contact_evidence() {
    evidence_file="$RUNTIME_LOG_DIR/agent-contact-evidence.txt"
    if [ -s "$evidence_file" ]; then
        sed -n '1p' "$evidence_file"
    fi
}

write_generated_spoe_config() {
    syntax_log="$LOG_DIR/spoe-config-syntax.log"
    if [ ! -x "$HAPROXY_BIN" ]; then
        SPOE_CONFIG_STATUS=missing
        return
    fi
    HAPROXY_PORT=$(pick_tcp_port)
    SPOA_PORT=$(pick_tcp_port)
    BACKEND_PORT=$(pick_tcp_port)
    if [ "$HAPROXY_PORT" = "$SPOA_PORT" ]; then
        SPOA_PORT=$(pick_tcp_port)
    fi
    if [ "$BACKEND_PORT" = "$HAPROXY_PORT" ] || [ "$BACKEND_PORT" = "$SPOA_PORT" ]; then
        BACKEND_PORT=$(pick_tcp_port)
    fi
    syntax_log="$RUNTIME_LOG_DIR/spoe-config-syntax.log"
    mkdir -p "$RUN_SPOE_RUNTIME_DIR"
    {
        echo "global"
        echo "    log stdout format raw local0"
        echo "    pidfile $RUN_TMP_DIR/haproxy.pid"
        echo
        echo "defaults"
        echo "    mode http"
        echo "    timeout connect 1s"
        echo "    timeout client 5s"
        echo "    timeout server 5s"
        echo
        echo "frontend fe_haproxy_spoe_diagnostic"
        echo "    bind 127.0.0.1:$HAPROXY_PORT"
        echo "    filter spoe engine modsecurity-diagnostic config $GENERATED_SPOE_CFG"
        echo "    http-request send-spoe-group modsecurity-diagnostic diagnostic-request"
        echo "    default_backend be_haproxy_diagnostic_app"
        echo
        echo "backend be_haproxy_diagnostic_app"
        echo "    mode http"
        echo "    server app1 127.0.0.1:$BACKEND_PORT"
        echo
        echo "backend be_spoa_diagnostic"
        echo "    mode spop"
        echo "    balance roundrobin"
        echo "    timeout connect 1s"
        echo "    timeout server 3s"
        echo "    server spoa1 127.0.0.1:$SPOA_PORT"
    } >"$GENERATED_HAPROXY_CFG"
    {
        echo "[modsecurity-diagnostic]"
        echo
        echo "spoe-agent modsecurity-diagnostic-agent"
        echo "    groups diagnostic-request"
        echo "    option var-prefix modsecdiag"
        echo "    option continue-on-error"
        echo "    timeout hello 1s"
        echo "    timeout idle 3s"
        echo "    timeout processing 1s"
        echo "    use-backend be_spoa_diagnostic"
        echo
        echo "spoe-group diagnostic-request"
        echo "    messages check-client"
        echo
        echo "spoe-message check-client"
        echo "    args ip=src"
    } >"$GENERATED_SPOE_CFG"
    set +e
    "$HAPROXY_BIN" -c -f "$GENERATED_HAPROXY_CFG" >"$syntax_log" 2>&1
    rc=$?
    set -e
    if [ "$rc" -eq 0 ]; then
        SPOE_CONFIG_STATUS=syntax-valid
    else
        SPOE_CONFIG_STATUS=syntax-blocked
        SPOE_RUNTIME_BLOCKER="haproxy runtime config failed"
    fi
}

run_live_spoe_diagnostic() {
    agent_ready="$RUN_TMP_DIR/diagnostic-agent.ready"
    agent_pid_file="$RUN_TMP_DIR/diagnostic-agent.pid"
    agent_port_file="$RUN_TMP_DIR/diagnostic-agent.port"
    http_status_file="$RUNTIME_LOG_DIR/http-probe.status"
    http_response_file="$RUNTIME_LOG_DIR/http-probe.response"
    marker="run_id=$RUN_ID haproxy_start_marker"

    if [ "$SPOE_CONFIG_STATUS" != "syntax-valid" ]; then
        SPOE_RUNTIME_BLOCKER="haproxy runtime config failed"
        return
    fi
    if [ "$SPOA_RUNTIME_STATUS" != "diagnostic-spop-handshake-subset" ]; then
        SPOE_RUNTIME_BLOCKER="diagnostic spoa agent failed to start"
        return
    fi
    if [ ! -x "$SPOA_RUNTIME_BIN" ]; then
        SPOE_RUNTIME_BLOCKER="diagnostic spoa agent failed to start"
        return
    fi
    : >"$DIAGNOSTIC_AGENT_LOG"
    : >"$HAPROXY_RUNTIME_LOG"
    : >"$HAPROXY_RUNTIME_STDOUT_LOG"
    : >"$HTTP_PROBE_LOG"
    : >"$BACKEND_RUNTIME_LOG"
    : >"$BACKEND_RUNTIME_STDOUT_LOG"
    if ! start_diagnostic_backend; then
        SPOE_RUNTIME_BLOCKER="diagnostic backend failed to start"
        return
    fi
    "$SPOA_RUNTIME_BIN" --serve \
        --host 127.0.0.1 \
        --port "$SPOA_PORT" \
        --ready-file "$agent_ready" \
        --pid-file "$agent_pid_file" \
        --port-file "$agent_port_file" \
        --log-file "$DIAGNOSTIC_AGENT_LOG" \
        >"$RUNTIME_LOG_DIR/diagnostic-agent.stdout.log" \
        2>"$RUNTIME_LOG_DIR/diagnostic-agent.stderr.log" &
    AGENT_PID=$!
    i=0
    while [ "$i" -lt 50 ]; do
        if [ -f "$agent_ready" ] && kill -0 "$AGENT_PID" 2>/dev/null; then
            DIAGNOSTIC_AGENT_STARTED=true
            break
        fi
        i=$((i + 1))
        sleep 0.1
    done
    if [ "$DIAGNOSTIC_AGENT_STARTED" != "true" ]; then
        SPOE_RUNTIME_BLOCKER="diagnostic spoa agent failed to start"
        return
    fi
    printf '%s epoch=%s\n' "$marker" "$(date -u +%s)" >>"$DIAGNOSTIC_AGENT_LOG"
    "$HAPROXY_BIN" -W -db -f "$GENERATED_HAPROXY_CFG" \
        >"$HAPROXY_RUNTIME_STDOUT_LOG" \
        2>"$HAPROXY_RUNTIME_LOG" &
    HAPROXY_PID=$!
    sleep 0.2
    if ! kill -0 "$HAPROXY_PID" 2>/dev/null; then
        SPOE_RUNTIME_BLOCKER="haproxy runtime failed to start"
        return
    fi
    HAPROXY_RUNTIME_STARTED=true
    set +e
    probe_rc=1
    i=0
    while [ "$i" -lt 30 ]; do
        run_http_probe "$HAPROXY_PORT" "$http_status_file" "$http_response_file" >"$HTTP_PROBE_LOG" 2>&1
        probe_rc=$?
        if [ "$probe_rc" -eq 0 ]; then
            break
        fi
        i=$((i + 1))
        sleep 0.1
    done
    set -e
    if [ -f "$http_status_file" ]; then
        HTTP_PROBE_STATUS=$(sed -n '1p' "$http_status_file")
    else
        HTTP_PROBE_STATUS=probe-error
    fi
    if [ "$probe_rc" -ne 0 ]; then
        SPOE_RUNTIME_BLOCKER="http probe failed"
        return
    fi
    i=0
    while [ "$i" -lt 30 ]; do
        if agent_contact_after_marker "$marker" "$DIAGNOSTIC_AGENT_LOG"; then
            HAPROXY_CONTACTED_DIAGNOSTIC_AGENT=true
            AGENT_CONTACT_EVIDENCE=$(read_agent_contact_evidence)
            SPOE_RUNTIME_STATUS=diagnostic-handshake-verified
            SPOE_RUNTIME_VERIFIED=true
            SPOE_RUNTIME_BLOCKER=
            return
        fi
        i=$((i + 1))
        sleep 0.1
    done
    SPOE_RUNTIME_BLOCKER="haproxy did not contact diagnostic spoa agent"
}

detect_example_spoe_config() {
    if [ ! -f "$HAPROXY_CFG_EXAMPLE" ] || [ ! -f "$SPOE_AGENT_CFG_EXAMPLE" ]; then
        printf missing
        return
    fi
    if grep -q 'example_only: true' "$HAPROXY_CFG_EXAMPLE" && grep -q 'example_only: true' "$SPOE_AGENT_CFG_EXAMPLE"; then
        printf example-only
    else
        printf not-verified
    fi
}

start_diagnostic_backend() {
    mkdir -p "$BACKEND_DOCROOT"
    printf 'haproxy diagnostic backend for %s\n' "$RUN_ID" >"$BACKEND_DOCROOT/diagnostic.txt"
    "$PYTHON_BIN" -m http.server "$BACKEND_PORT" \
        --bind 127.0.0.1 \
        --directory "$BACKEND_DOCROOT" \
        >"$BACKEND_RUNTIME_STDOUT_LOG" \
        2>"$BACKEND_RUNTIME_LOG" &
    BACKEND_PID=$!
    if wait_tcp_port "$BACKEND_PORT"; then
        BACKEND_RUNTIME_STARTED=true
        return 0
    fi
    BACKEND_RUNTIME_STARTED=false
    return 1
}

detect_modsecurity_binding() {
    if grep -R -E 'msc_new_transaction|modsecurity/modsecurity.h|modsecurity/transaction.h' "$CONNECTOR_DIR/src" "$CONNECTOR_DIR"/*.c "$CONNECTOR_DIR"/*.h >/dev/null 2>&1; then
        printf present
    else
        printf missing
    fi
}

write_blocked_evidence() {
    results_jsonl="$RESULTS_DIR/$CONNECTOR_NAME-results.jsonl"
    summary_json="$RESULTS_DIR/$CONNECTOR_NAME-summary.json"
    summary_text="$RESULTS_DIR/$CONNECTOR_NAME-summary.txt"
    status_log="$LOG_DIR/status.log"
    starter_checks_available=$(starter_available)
    local_haproxy_bin=
    if [ -x "$HAPROXY_BIN" ]; then
        local_haproxy_bin="$HAPROXY_BIN"
    fi
    system_haproxy_bin=$(command -v haproxy 2>/dev/null || true)
    common_acquisition_status=$(detect_common_acquisition)
    spoa_starter_status=$(detect_spoa_starter)
    run_spoa_runtime_self_test
    write_generated_spoe_config
    run_live_spoe_diagnostic
    example_spoe_config_status=$(detect_example_spoe_config)
    modsecurity_binding_status=$(detect_modsecurity_binding)
    {
        echo "BLOCKED haproxy runtime integration not verified"
        echo "run_id=$RUN_ID"
        echo "local_haproxy_bin=${local_haproxy_bin:-missing}"
        echo "system_haproxy_bin=${system_haproxy_bin:-missing}"
        echo "prepare_status=$PREPARE_STATUS"
        echo "prepare_reason=$PREPARE_REASON"
        echo "common_acquisition_status=$common_acquisition_status"
        echo "spoa_starter_status=$spoa_starter_status"
        echo "spoa_agent_runtime_status=$SPOA_RUNTIME_STATUS"
        echo "spoa_protocol_runtime_verified=$SPOA_PROTOCOL_RUNTIME_VERIFIED"
        echo "spoe_config_status=$SPOE_CONFIG_STATUS"
        echo "spoe_runtime_status=$SPOE_RUNTIME_STATUS"
        echo "spoe_runtime_verified=$SPOE_RUNTIME_VERIFIED"
        echo "spoe_runtime_blocker=${SPOE_RUNTIME_BLOCKER:-none}"
        echo "haproxy_runtime_started=$HAPROXY_RUNTIME_STARTED"
        echo "diagnostic_agent_started=$DIAGNOSTIC_AGENT_STARTED"
        echo "diagnostic_backend_started=$BACKEND_RUNTIME_STARTED"
        echo "http_probe_status=$HTTP_PROBE_STATUS"
        echo "haproxy_contacted_diagnostic_agent=$HAPROXY_CONTACTED_DIAGNOSTIC_AGENT"
        echo "agent_contact_evidence=$AGENT_CONTACT_EVIDENCE"
        echo "example_spoe_config_status=$example_spoe_config_status"
        echo "modsecurity_binding_status=$modsecurity_binding_status"
    } > "$status_log"
    "$PYTHON_BIN" - "$results_jsonl" "$summary_json" "$summary_text" \
        "$CONNECTOR_NAME" "$HARNESS_PATH" "$CONNECTOR_ROOT" "$SOURCE_ROOT" \
        "$BUILD_ROOT" "$RESULTS_DIR" "$TMP_ROOT" "$LOG_ROOT" "$LOG_DIR" \
        "$starter_checks_available" "$NOTE" "$local_haproxy_bin" "$system_haproxy_bin" \
        "$PREPARE_STATUS" "$PREPARE_REASON" "$PREPARE_HAPROXY_RUNTIME" \
        "$common_acquisition_status" "$spoa_starter_status" "$SPOA_RUNTIME_STATUS" \
        "$SPOA_PROTOCOL_RUNTIME_VERIFIED" "$SPOA_RUNTIME_REASON" "$SPOA_RUNTIME_BIN" \
        "$SPOE_CONFIG_STATUS" "$SPOE_RUNTIME_STATUS" "$SPOE_RUNTIME_VERIFIED" \
        "$SPOE_RUNTIME_BLOCKER" "$GENERATED_HAPROXY_CFG" "$GENERATED_SPOE_CFG" \
        "$RUNTIME_LOG_DIR/spoe-config-syntax.log" "$RUN_ID" "$RUN_TMP_DIR" \
        "$RUNTIME_LOG_DIR" "$HAPROXY_RUNTIME_STARTED" "$DIAGNOSTIC_AGENT_STARTED" \
        "$BACKEND_RUNTIME_STARTED" "$HTTP_PROBE_STATUS" "$HAPROXY_CONTACTED_DIAGNOSTIC_AGENT" \
        "$AGENT_CONTACT_EVIDENCE" "$DIAGNOSTIC_AGENT_LOG" "$HAPROXY_RUNTIME_LOG" \
        "$HTTP_PROBE_LOG" "$BACKEND_RUNTIME_LOG" "$HAPROXY_PORT" "$SPOA_PORT" "$BACKEND_PORT" \
        "$example_spoe_config_status" "$modsecurity_binding_status" "$SPOA_STARTER_BIN" \
        "$HAPROXY_CFG_EXAMPLE" "$SPOE_AGENT_CFG_EXAMPLE" <<'PY'
import json
import sys
from datetime import datetime, timezone

(
    results_jsonl,
    summary_json,
    summary_text,
    connector,
    harness_path,
    connector_root,
    source_root,
    build_root,
    results_dir,
    tmp_root,
    log_root,
    log_dir,
    starter_checks_available_text,
    note,
    local_haproxy_bin,
    system_haproxy_bin,
    prepare_status,
    prepare_reason,
    prepare_helper,
    common_acquisition_status,
    spoa_starter_status,
    spoa_agent_runtime_status,
    spoa_protocol_runtime_verified_text,
    spoa_runtime_reason,
    spoa_agent_runtime_binary,
    spoe_config_status,
    spoe_runtime_status,
    spoe_runtime_verified_text,
    spoe_runtime_blocker,
    generated_haproxy_config,
    generated_spoe_config,
    spoe_config_syntax_log,
    run_id,
    run_tmp_dir,
    runtime_log_dir,
    haproxy_runtime_started_text,
    diagnostic_agent_started_text,
    diagnostic_backend_started_text,
    http_probe_status,
    haproxy_contacted_diagnostic_agent_text,
    agent_contact_evidence,
    diagnostic_agent_log,
    haproxy_runtime_log,
    http_probe_log,
    backend_runtime_log,
    haproxy_port,
    spoa_port,
    backend_port,
    example_spoe_config_status,
    modsecurity_binding_status,
    spoa_starter_bin,
    haproxy_cfg_example,
    spoe_agent_cfg_example,
) = sys.argv[1:]

now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
starter_checks_available = starter_checks_available_text == "true"
spoa_protocol_runtime_verified = spoa_protocol_runtime_verified_text == "true"
spoe_runtime_verified = spoe_runtime_verified_text == "true"
haproxy_runtime_started = haproxy_runtime_started_text == "true"
diagnostic_agent_started = diagnostic_agent_started_text == "true"
diagnostic_backend_started = diagnostic_backend_started_text == "true"
haproxy_contacted_diagnostic_agent = haproxy_contacted_diagnostic_agent_text == "true"
blocked_reasons = []
if not local_haproxy_bin:
    blocked_reasons.append("haproxy binary missing")
    if prepare_status in {"blocked", "failed", "missing-helper"}:
        blocked_reasons.append(f"haproxy local build blocked: {prepare_reason}")
if common_acquisition_status != "defined":
    blocked_reasons.append("haproxy source/binary acquisition is not defined in common.sh")
if spoa_agent_runtime_status != "diagnostic-spop-handshake-subset":
    blocked_reasons.append("spoa agent runtime missing")
if spoe_config_status != "syntax-valid":
    blocked_reasons.append("spoe config missing")
elif not spoe_runtime_verified:
    blocked_reasons.append(spoe_runtime_blocker or "spoe runtime integration not verified")
if modsecurity_binding_status != "present":
    blocked_reasons.append("modsecurity binding missing")

diagnostics = {
    "run_id": run_id,
    "haproxy_binary": "present" if local_haproxy_bin else "missing",
    "haproxy_binary_path": local_haproxy_bin or None,
    "system_haproxy_binary": system_haproxy_bin or None,
    "prepare_status": prepare_status,
    "prepare_reason": prepare_reason,
    "prepare_helper": prepare_helper,
    "common_acquisition_status": common_acquisition_status,
    "spoa_starter_binary": spoa_starter_bin,
    "spoa_starter_status": spoa_starter_status,
    "spoa_agent_runtime_binary": spoa_agent_runtime_binary,
    "spoa_agent_runtime_status": spoa_agent_runtime_status,
    "spoa_protocol_runtime_verified": spoa_protocol_runtime_verified,
    "spoa_runtime_reason": spoa_runtime_reason,
    "spoa_runtime_self_test_stdout": f"{log_dir}/spoa-runtime-self-test.stdout.log",
    "spoa_runtime_self_test_stderr": f"{log_dir}/spoa-runtime-self-test.stderr.log",
    "spoe_config_status": spoe_config_status,
    "spoe_runtime_status": spoe_runtime_status,
    "spoe_runtime_verified": spoe_runtime_verified,
    "spoe_runtime_blocker": spoe_runtime_blocker or None,
    "generated_haproxy_config": generated_haproxy_config,
    "generated_spoe_config": generated_spoe_config,
    "spoe_config_syntax_log": spoe_config_syntax_log,
    "run_tmp_dir": run_tmp_dir,
    "runtime_log_dir": runtime_log_dir,
    "haproxy_runtime_started": haproxy_runtime_started,
    "diagnostic_agent_started": diagnostic_agent_started,
    "diagnostic_backend_started": diagnostic_backend_started,
    "http_probe_status": http_probe_status,
    "haproxy_contacted_diagnostic_agent": haproxy_contacted_diagnostic_agent,
    "agent_contact_evidence": agent_contact_evidence or None,
    "diagnostic_agent_log": diagnostic_agent_log,
    "haproxy_runtime_log": haproxy_runtime_log,
    "http_probe_log": http_probe_log,
    "backend_runtime_log": backend_runtime_log,
    "haproxy_port": int(haproxy_port) if haproxy_port.isdigit() else None,
    "spoa_port": int(spoa_port) if spoa_port.isdigit() else None,
    "backend_port": int(backend_port) if backend_port.isdigit() else None,
    "example_spoe_config_status": example_spoe_config_status,
    "haproxy_config_example": haproxy_cfg_example,
    "spoe_agent_config_example": spoe_agent_cfg_example,
    "modsecurity_binding_status": modsecurity_binding_status,
}
record = {
    "connector": connector,
    "check": "runtime-smoke-entrypoint",
    "command": f"make smoke-{connector}",
    "test_type": "runtime-smoke",
    "status": "BLOCKED",
    "exit_code": 77,
    "runtime_verified": False,
    "runtime_status": "blocked",
    "response_body_verified": False,
    "crs_verified": False,
    "reason": "haproxy runtime integration not verified",
    "blocked_reasons": blocked_reasons,
    "diagnostics": diagnostics,
    "run_id": run_id,
    "haproxy_runtime_started": haproxy_runtime_started,
    "diagnostic_agent_started": diagnostic_agent_started,
    "diagnostic_backend_started": diagnostic_backend_started,
    "http_probe_status": http_probe_status,
    "haproxy_contacted_diagnostic_agent": haproxy_contacted_diagnostic_agent,
    "agent_contact_evidence": agent_contact_evidence or None,
    "diagnostic_agent_log": diagnostic_agent_log,
    "haproxy_runtime_log": haproxy_runtime_log,
    "haproxy_binary": "present" if local_haproxy_bin else "missing",
    "spoa_agent_runtime_status": spoa_agent_runtime_status,
    "spoa_protocol_runtime_verified": spoa_protocol_runtime_verified,
    "spoe_config_status": spoe_config_status,
    "spoe_runtime_status": spoe_runtime_status,
    "spoe_runtime_verified": spoe_runtime_verified,
    "modsecurity_binding_status": modsecurity_binding_status,
    "starter_checks_available": starter_checks_available,
    "installs_global_artifacts": False,
    "harness_path": harness_path,
    "generated_at": now,
    "note": note,
}
summary = {
    "connector": connector,
    "generated_at": now,
    "connector_root": connector_root,
    "source_root": source_root,
    "build_root": build_root,
    "results_dir": results_dir,
    "tmp_root": tmp_root,
    "log_root": log_root,
    "log_dir": log_dir,
    "runtime_log_dir": runtime_log_dir,
    "run_id": run_id,
    "run_tmp_dir": run_tmp_dir,
    "status": "BLOCKED",
    "counts": {"PASS": 0, "FAIL": 0, "BLOCKED": 1, "NOT_RUN": 0},
    "runtime_verified": False,
    "runtime_status": "blocked",
    "response_body_verified": False,
    "crs_verified": False,
    "reason": "haproxy runtime integration not verified",
    "blocked_reasons": blocked_reasons,
    "diagnostics": diagnostics,
    "haproxy_runtime_started": haproxy_runtime_started,
    "diagnostic_agent_started": diagnostic_agent_started,
    "diagnostic_backend_started": diagnostic_backend_started,
    "http_probe_status": http_probe_status,
    "haproxy_contacted_diagnostic_agent": haproxy_contacted_diagnostic_agent,
    "agent_contact_evidence": agent_contact_evidence or None,
    "diagnostic_agent_log": diagnostic_agent_log,
    "haproxy_runtime_log": haproxy_runtime_log,
    "haproxy_binary": "present" if local_haproxy_bin else "missing",
    "spoa_agent_runtime_status": spoa_agent_runtime_status,
    "spoa_protocol_runtime_verified": spoa_protocol_runtime_verified,
    "spoe_config_status": spoe_config_status,
    "spoe_runtime_status": spoe_runtime_status,
    "spoe_runtime_verified": spoe_runtime_verified,
    "modsecurity_binding_status": modsecurity_binding_status,
    "starter_checks_available": starter_checks_available,
    "installs_global_artifacts": False,
    "harness_path": harness_path,
    "note": note,
    "results": [record],
}
with open(results_jsonl, "w", encoding="utf-8") as handle:
    handle.write(json.dumps(record, sort_keys=True))
    handle.write("\n")
with open(summary_json, "w", encoding="utf-8") as handle:
    json.dump(summary, handle, indent=2, sort_keys=True)
    handle.write("\n")
with open(summary_text, "w", encoding="utf-8") as handle:
    handle.write("BLOCKED runtime-smoke-entrypoint haproxy runtime integration not verified\n")
    handle.write("spoa_agent_runtime_status: " + spoa_agent_runtime_status + "\n")
    handle.write("spoa_protocol_runtime_verified: " + str(spoa_protocol_runtime_verified).lower() + "\n")
    handle.write("spoe_config_status: " + spoe_config_status + "\n")
    handle.write("spoe_runtime_status: " + spoe_runtime_status + "\n")
    handle.write("spoe_runtime_verified: " + str(spoe_runtime_verified).lower() + "\n")
    handle.write("haproxy_runtime_started: " + str(haproxy_runtime_started).lower() + "\n")
    handle.write("diagnostic_agent_started: " + str(diagnostic_agent_started).lower() + "\n")
    handle.write("diagnostic_backend_started: " + str(diagnostic_backend_started).lower() + "\n")
    handle.write("http_probe_status: " + http_probe_status + "\n")
    handle.write("haproxy_contacted_diagnostic_agent: " + str(haproxy_contacted_diagnostic_agent).lower() + "\n")
    if agent_contact_evidence:
        handle.write("agent_contact_evidence: " + agent_contact_evidence + "\n")
    for item in blocked_reasons:
        handle.write(f"- {item}\n")
    handle.write("Runtime not verified\n")
    handle.write("The SPOA diagnostic runtime is a minimal diagnostic SPOP handshake subset, not a full SPOA agent implementation.\n")
    handle.write(f"{note}\n")
PY
}

validate_roots
ensure_local_haproxy
write_blocked_evidence
echo "$CONNECTOR_NAME runtime smoke: BLOCKED - haproxy runtime integration not verified"
echo "Runtime not verified"
exit 77
