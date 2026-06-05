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
MODSECURITY_BINDING_BIN="$BUILD_ROOT/haproxy-modsecurity-binding/haproxy-modsecurity-binding-self-test"
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
MODSECURITY_HEADERS_PRESENT=false
MODSECURITY_HEADER_DIR=
MODSECURITY_LIBRARY_PRESENT=false
MODSECURITY_LIBRARY_DIR=
MODSECURITY_BINDING_STATUS=not-run
MODSECURITY_BINDING_BUILD_STATUS=NOT_RUN
MODSECURITY_BINDING_SELF_TEST_STATUS=NOT_RUN
MODSECURITY_BINDING_REASON=
HAPROXY_ENFORCEMENT_STATUS=missing
HAPROXY_RUNTIME_STARTED=false
DIAGNOSTIC_AGENT_STARTED=false
HTTP_PROBE_STATUS=not-run
HTTP_BLOCK_PROBE_STATUS=not-run
HTTP_PASS_PROBE_STATUS=not-run
WITH_CRS_STATUS=BLOCKED
WITH_CRS_VERIFIED_CASE=haproxy_crs_sqli_anomaly_block
WITH_CRS_BLOCK_PROBE_STATUS=not-run
WITH_CRS_PASS_PROBE_STATUS=not-run
WITH_CRS_CRS_LOADED=false
WITH_CRS_CRS_PREAMBLE_FILE="${MODSECURITY_RULE_PREAMBLE_FILE:-${CRS_RUNTIME_DIR:-$BUILD_ROOT/crs}/modsecurity-crs-preamble.conf}"
WITH_CRS_BLOCKED_REASON="with-crs not run"
WITH_CRS_RUNTIME_LOG_DIR="$RUNTIME_LOG_DIR/with-crs"
WITH_CRS_DIAGNOSTIC_AGENT_LOG="$WITH_CRS_RUNTIME_LOG_DIR/diagnostic-agent.log"
WITH_CRS_HAPROXY_RUNTIME_LOG="$WITH_CRS_RUNTIME_LOG_DIR/haproxy-runtime.stderr.log"
WITH_CRS_HTTP_PROBE_LOG="$WITH_CRS_RUNTIME_LOG_DIR/http-probe.log"
WITH_CRS_MODSECURITY_EVIDENCE=
WITH_CRS_AGENT_CONTACT_EVIDENCE=
WITH_CRS_SET_VAR_ACK_EVIDENCE=
WITH_CRS_BINDING_SELF_TEST_STATUS=NOT_RUN
WITH_CRS_BINDING_SELF_TEST_LOG="$LOG_DIR/modsecurity-binding-crs-self-test.log"
WITH_CRS_HAPROXY_PID=
WITH_CRS_AGENT_PID=
WITH_CRS_BACKEND_PID=
HAPROXY_CONTACTED_DIAGNOSTIC_AGENT=false
AGENT_CONTACT_EVIDENCE=
AGENT_RECEIVED_NOTIFY=false
AGENT_EXTRACTED_REQUEST_ARGS=false
AGENT_ARGS_EVIDENCE=
MODSECURITY_LIVE_BINDING_VERIFIED=false
MODSECURITY_LIVE_EVIDENCE=
SPOE_SET_VAR_ACK_SENT=false
SPOE_SET_VAR_ACK_EVIDENCE=
SPOE_ACTION_ENCODING_STATUS=not-run
SPOE_ACTION_ENCODING_VERIFIED=false
SPOE_ACTION_ENCODING_REASON=
HAPROXY_ENFORCED_BLOCK=false
VERIFIED_CASE=
RUNTIME_RESULT_STATUS=BLOCKED
RUNTIME_EXIT_CODE=77
RUNTIME_VERIFIED=false
RUNTIME_STATUS=blocked
RUNTIME_REASON="haproxy runtime integration not verified"
HAPROXY_PORT=
SPOA_PORT=
AGENT_PID=
HAPROXY_PID=
BACKEND_PID=
DIAGNOSTIC_AGENT_LOG="$RUNTIME_LOG_DIR/diagnostic-agent.log"
HAPROXY_RUNTIME_LOG="$RUNTIME_LOG_DIR/haproxy-runtime.stderr.log"
HAPROXY_RUNTIME_STDOUT_LOG="$RUNTIME_LOG_DIR/haproxy-runtime.stdout.log"
HTTP_PROBE_LOG="$RUNTIME_LOG_DIR/http-probe.log"
MODSECURITY_BINDING_BUILD_LOG="$LOG_DIR/modsecurity-binding-build.log"
MODSECURITY_BINDING_SELF_TEST_LOG="$LOG_DIR/modsecurity-binding-self-test.log"
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
    if [ -n "${WITH_CRS_HAPROXY_PID:-}" ]; then
        kill "$WITH_CRS_HAPROXY_PID" 2>/dev/null || true
        wait "$WITH_CRS_HAPROXY_PID" 2>/dev/null || true
        WITH_CRS_HAPROXY_PID=
    fi
    if [ -n "${WITH_CRS_AGENT_PID:-}" ]; then
        kill "$WITH_CRS_AGENT_PID" 2>/dev/null || true
        wait "$WITH_CRS_AGENT_PID" 2>/dev/null || true
        WITH_CRS_AGENT_PID=
    fi
    if [ -n "${WITH_CRS_BACKEND_PID:-}" ]; then
        kill "$WITH_CRS_BACKEND_PID" 2>/dev/null || true
        wait "$WITH_CRS_BACKEND_PID" 2>/dev/null || true
        WITH_CRS_BACKEND_PID=
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
    require_log_path "$WITH_CRS_RUNTIME_LOG_DIR" WITH_CRS_RUNTIME_LOG_DIR
    require_build_path "$HAPROXY_BIN" HAPROXY_BIN
    require_build_path "$SPOA_RUNTIME_BIN" SPOA_RUNTIME_BIN
    require_build_path "$MODSECURITY_BINDING_BIN" MODSECURITY_BINDING_BIN
    require_build_path "$SPOE_RUNTIME_DIR" SPOE_RUNTIME_DIR
    require_build_path "$RUN_SPOE_RUNTIME_DIR" RUN_SPOE_RUNTIME_DIR
    require_build_path "$GENERATED_HAPROXY_CFG" GENERATED_HAPROXY_CFG
    require_build_path "$GENERATED_SPOE_CFG" GENERATED_SPOE_CFG
    require_build_path "$RUN_TMP_DIR" RUN_TMP_DIR
    require_build_path "$BACKEND_DOCROOT" BACKEND_DOCROOT
    require_not_connector_artifact "$WITH_CRS_RUNTIME_LOG_DIR" WITH_CRS_RUNTIME_LOG_DIR
    require_not_connector_artifact "$RESULTS_DIR" RESULTS_DIR
    require_not_connector_artifact "$TMP_ROOT" TMP_ROOT
    require_not_connector_artifact "$LOG_ROOT" LOG_ROOT
    require_not_connector_artifact "$HAPROXY_BIN" HAPROXY_BIN
    require_not_connector_artifact "$SPOA_RUNTIME_BIN" SPOA_RUNTIME_BIN
    require_not_connector_artifact "$MODSECURITY_BINDING_BIN" MODSECURITY_BINDING_BIN
    require_not_connector_artifact "$SPOE_RUNTIME_DIR" SPOE_RUNTIME_DIR
    require_not_connector_artifact "$RUN_SPOE_RUNTIME_DIR" RUN_SPOE_RUNTIME_DIR
    require_not_connector_artifact "$RUN_TMP_DIR" RUN_TMP_DIR
    require_not_connector_artifact "$RUNTIME_LOG_DIR" RUNTIME_LOG_DIR
    require_not_connector_artifact "$BACKEND_DOCROOT" BACKEND_DOCROOT
    mkdir -p "$RESULTS_DIR" "$TMP_ROOT" "$LOG_DIR" "$RUN_TMP_DIR" "$RUNTIME_LOG_DIR" "$WITH_CRS_RUNTIME_LOG_DIR"
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

verify_spoe_action_encoding() {
    haproxy_source_dir="${HAPROXY_SOURCE_DIR:-}"
    if [ -z "$haproxy_source_dir" ] && [ -n "${HAPROXY_VERSION:-}" ]; then
        haproxy_source_dir="$SOURCE_ROOT/haproxy/haproxy-$HAPROXY_VERSION"
    fi
    if [ -z "$haproxy_source_dir" ]; then
        SPOE_ACTION_ENCODING_STATUS=blocked
        SPOE_ACTION_ENCODING_REASON="HAProxy source path is not defined in common.sh"
        return
    fi
    doc_spoe="$haproxy_source_dir/doc/SPOE.txt"
    spoe_t="$haproxy_source_dir/include/haproxy/spoe-t.h"
    spoe_h="$haproxy_source_dir/include/haproxy/spoe.h"
    flt_spoe="$haproxy_source_dir/src/flt_spoe.c"
    if [ ! -f "$doc_spoe" ] || [ ! -f "$spoe_t" ] || [ ! -f "$spoe_h" ] || [ ! -f "$flt_spoe" ]; then
        SPOE_ACTION_ENCODING_STATUS=blocked
        SPOE_ACTION_ENCODING_REASON="local HAProxy SPOE/SPOP docs or source files missing"
        return
    fi
    if ! grep -q 'SET-VAR[[:space:]]*: <1>' "$doc_spoe"; then
        SPOE_ACTION_ENCODING_STATUS=blocked
        SPOE_ACTION_ENCODING_REASON="set-var action type not verified in local SPOE.txt"
        return
    fi
    if ! grep -q 'NB-ARGS[[:space:]]*: <3>' "$doc_spoe"; then
        SPOE_ACTION_ENCODING_STATUS=blocked
        SPOE_ACTION_ENCODING_REASON="set-var arg count not verified in local SPOE.txt"
        return
    fi
    if ! grep -q 'TRANSACTION[[:space:]]*: <2>' "$doc_spoe"; then
        SPOE_ACTION_ENCODING_STATUS=blocked
        SPOE_ACTION_ENCODING_REASON="transaction scope encoding not verified in local SPOE.txt"
        return
    fi
    if ! grep -q 'SPOP_ACT_T_SET_VAR[[:space:]]*=[[:space:]]*1' "$spoe_t"; then
        SPOE_ACTION_ENCODING_STATUS=blocked
        SPOE_ACTION_ENCODING_REASON="SPOP_ACT_T_SET_VAR value not verified in local spoe-t.h"
        return
    fi
    if ! awk '/SPOP_SCOPE_PROC[[:space:]]*=[[:space:]]*0/{proc=1} proc && /SPOP_SCOPE_SESS/{sess=1} sess && /SPOP_SCOPE_TXN/{txn=1} END { exit txn ? 0 : 1 }' "$spoe_t"; then
        SPOE_ACTION_ENCODING_STATUS=blocked
        SPOE_ACTION_ENCODING_REASON="SPOP_SCOPE_TXN sequence not verified in local spoe-t.h"
        return
    fi
    if ! grep -q '#define SPOP_DATA_FL_TRUE[[:space:]]*0x10' "$spoe_t"; then
        SPOE_ACTION_ENCODING_STATUS=blocked
        SPOE_ACTION_ENCODING_REASON="bool true flag not verified in local spoe-t.h"
        return
    fi
    if ! awk '/enum spop_data_type/{inside=1} inside && /SPOP_DATA_T_NULL[[:space:]]*=[[:space:]]*0/{null_seen=1} null_seen && /SPOP_DATA_T_BOOL/{bool_seen=1} END { exit bool_seen ? 0 : 1 }' "$spoe_t"; then
        SPOE_ACTION_ENCODING_STATUS=blocked
        SPOE_ACTION_ENCODING_REASON="bool type value not verified in local spoe-t.h"
        return
    fi
    if ! grep -q 'SPOP_DATA_T_BOOL' "$spoe_h" || ! grep -q 'SPOP_DATA_FL_TRUE' "$spoe_h"; then
        SPOE_ACTION_ENCODING_STATUS=blocked
        SPOE_ACTION_ENCODING_REASON="bool encode/decode path not verified in local spoe.h"
        return
    fi
    if ! grep -q 'spoe_decode_action_set_var' "$flt_spoe" || ! grep -q 'spoe_decode_data' "$flt_spoe"; then
        SPOE_ACTION_ENCODING_STATUS=blocked
        SPOE_ACTION_ENCODING_REASON="set-var ACK decode path not verified in local flt_spoe.c"
        return
    fi
    SPOE_ACTION_ENCODING_STATUS=verified
    SPOE_ACTION_ENCODING_VERIFIED=true
    SPOE_ACTION_ENCODING_REASON="set-var action=1 arg_count=3 txn_scope=2 bool_true=0x11 verified from local HAProxy SPOE/SPOP docs and source"
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
        SPOA_RUNTIME_REASON="minimal diagnostic SPOP handshake subset self-test passed with verified set-var ACK path"
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
    header_value=${4:-}
    expected_status=${5:-200}
    request_uri=${6:-/diagnostic.txt}
    "$PYTHON_BIN" - "$port" "$status_file" "$response_file" "$header_value" "$expected_status" "$request_uri" <<'PY'
import socket
import sys

port = int(sys.argv[1])
status_file = sys.argv[2]
response_file = sys.argv[3]
header_value = sys.argv[4]
expected_status = sys.argv[5]
request_uri = sys.argv[6]
status = "probe-error"
data = b""
try:
    with socket.create_connection(("127.0.0.1", port), timeout=3) as sock:
        request = (
            "GET " + request_uri + " HTTP/1.1\r\n"
            "Host: 127.0.0.1\r\n"
        )
        if header_value:
            request += "X-Haproxy-ModSecurity-Test: " + header_value + "\r\n"
        request += "Connection: close\r\n\r\n"
        sock.sendall(request.encode("ascii"))
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
sys.exit(0 if status == expected_status else 1)
PY
}

agent_evidence_after_marker() {
    marker=$1
    log_file=$2
    pattern=$3
    evidence_file=$4
    [ -f "$log_file" ] || return 1
    awk -v marker="$marker" -v pattern="$pattern" '
        index($0, marker) { seen = 1; next }
        seen && index($0, pattern) { found = 1; print; exit }
        END { exit found ? 0 : 1 }
    ' "$log_file" >"$evidence_file"
}

read_evidence_line() {
    evidence_file=$1
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
        echo "    http-request deny status 403 if { var(txn.modsecdiag.blocked) -m bool }"
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
        echo "    register-var-names blocked"
        echo "    option continue-on-error"
        echo "    timeout hello 1s"
        echo "    timeout idle 3s"
        echo "    timeout processing 1s"
        echo "    use-backend be_spoa_diagnostic"
        echo
        echo "spoe-group diagnostic-request"
        echo "    messages check-request"
        echo
        echo "spoe-message check-request"
        echo "    args method=method path=path uri=url host=req.hdr(Host) test_header=req.hdr(X-Haproxy-ModSecurity-Test)"
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
    block_status_file="$RUNTIME_LOG_DIR/http-block-probe.status"
    block_response_file="$RUNTIME_LOG_DIR/http-block-probe.response"
    pass_status_file="$RUNTIME_LOG_DIR/http-pass-probe.status"
    pass_response_file="$RUNTIME_LOG_DIR/http-pass-probe.response"
    marker="run_id=$RUN_ID haproxy_start_marker"

    if [ "$SPOE_ACTION_ENCODING_VERIFIED" != "true" ]; then
        SPOE_RUNTIME_BLOCKER="spoe action encoding not verified"
        return
    fi
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
    "$HAPROXY_BIN" -db -f "$GENERATED_HAPROXY_CFG" \
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
    block_probe_rc=1
    i=0
    while [ "$i" -lt 30 ]; do
        run_http_probe "$HAPROXY_PORT" "$block_status_file" "$block_response_file" block 403 >>"$HTTP_PROBE_LOG" 2>&1
        block_probe_rc=$?
        if [ "$block_probe_rc" -eq 0 ]; then
            break
        fi
        i=$((i + 1))
        sleep 0.1
    done
    pass_probe_rc=1
    i=0
    while [ "$i" -lt 30 ]; do
        run_http_probe "$HAPROXY_PORT" "$pass_status_file" "$pass_response_file" "" 200 >>"$HTTP_PROBE_LOG" 2>&1
        pass_probe_rc=$?
        if [ "$pass_probe_rc" -eq 0 ]; then
            break
        fi
        i=$((i + 1))
        sleep 0.1
    done
    set -e
    if [ -f "$block_status_file" ]; then
        HTTP_BLOCK_PROBE_STATUS=$(sed -n '1p' "$block_status_file")
    else
        HTTP_BLOCK_PROBE_STATUS=probe-error
    fi
    if [ -f "$pass_status_file" ]; then
        HTTP_PASS_PROBE_STATUS=$(sed -n '1p' "$pass_status_file")
    else
        HTTP_PASS_PROBE_STATUS=probe-error
    fi
    HTTP_PROBE_STATUS="block:$HTTP_BLOCK_PROBE_STATUS pass:$HTTP_PASS_PROBE_STATUS"
    if agent_evidence_after_marker "$marker" "$DIAGNOSTIC_AGENT_LOG" "NOTIFY received" "$RUNTIME_LOG_DIR/agent-notify-evidence.txt"; then
        AGENT_RECEIVED_NOTIFY=true
        HAPROXY_CONTACTED_DIAGNOSTIC_AGENT=true
        AGENT_CONTACT_EVIDENCE=$(read_evidence_line "$RUNTIME_LOG_DIR/agent-notify-evidence.txt")
    fi
    if agent_evidence_after_marker "$marker" "$DIAGNOSTIC_AGENT_LOG" "NOTIFY request args extracted method_present=1 path_present=1 uri_present=1 host_present=1 test_header_present=1" "$RUNTIME_LOG_DIR/agent-args-evidence.txt"; then
        AGENT_EXTRACTED_REQUEST_ARGS=true
        AGENT_ARGS_EVIDENCE=$(read_evidence_line "$RUNTIME_LOG_DIR/agent-args-evidence.txt")
    fi
    if agent_evidence_after_marker "$marker" "$DIAGNOSTIC_AGENT_LOG" "MODSECURITY live decision disruptive=1 status=403" "$RUNTIME_LOG_DIR/modsecurity-live-evidence.txt"; then
        MODSECURITY_LIVE_BINDING_VERIFIED=true
        MODSECURITY_LIVE_EVIDENCE=$(read_evidence_line "$RUNTIME_LOG_DIR/modsecurity-live-evidence.txt")
    fi
    if agent_evidence_after_marker "$marker" "$DIAGNOSTIC_AGENT_LOG" "ACK set-var txn.blocked true sent" "$RUNTIME_LOG_DIR/spoe-set-var-ack-evidence.txt"; then
        SPOE_SET_VAR_ACK_SENT=true
        SPOE_SET_VAR_ACK_EVIDENCE=$(read_evidence_line "$RUNTIME_LOG_DIR/spoe-set-var-ack-evidence.txt")
    fi
    if [ "$HTTP_BLOCK_PROBE_STATUS" = "403" ]; then
        HAPROXY_ENFORCED_BLOCK=true
    fi
    if [ "$AGENT_RECEIVED_NOTIFY" != "true" ]; then
        SPOE_RUNTIME_BLOCKER="agent did not receive notify"
        return
    fi
    if [ "$AGENT_EXTRACTED_REQUEST_ARGS" != "true" ]; then
        SPOE_RUNTIME_BLOCKER="agent did not extract request args"
        return
    fi
    if [ "$MODSECURITY_LIVE_BINDING_VERIFIED" != "true" ]; then
        SPOE_RUNTIME_BLOCKER="modsecurity live binding failed"
        return
    fi
    if [ "$SPOE_SET_VAR_ACK_SENT" != "true" ]; then
        SPOE_RUNTIME_BLOCKER="spoe set-var ack not sent"
        return
    fi
    if [ "$HAPROXY_ENFORCED_BLOCK" != "true" ] || [ "$block_probe_rc" -ne 0 ]; then
        SPOE_RUNTIME_BLOCKER="haproxy did not enforce block decision"
        return
    fi
    if [ "$HTTP_PASS_PROBE_STATUS" != "200" ] || [ "$pass_probe_rc" -ne 0 ]; then
        SPOE_RUNTIME_BLOCKER="pass probe failed"
        return
    fi
    SPOE_RUNTIME_STATUS=diagnostic-enforcement-verified
    SPOE_RUNTIME_VERIFIED=true
    SPOE_RUNTIME_BLOCKER=
    HAPROXY_ENFORCEMENT_STATUS=verified
    MODSECURITY_BINDING_STATUS=live-enforcement-verified
    VERIFIED_CASE=haproxy_phase1_header_block
    RUNTIME_RESULT_STATUS=PASS
    RUNTIME_EXIT_CODE=0
    RUNTIME_VERIFIED=true
    RUNTIME_STATUS=runtime-smoke-verified
    RUNTIME_REASON="haproxy_phase1_header_block runtime smoke verified"
}

prepare_crs_for_haproxy() {
    prepare_log="$WITH_CRS_RUNTIME_LOG_DIR/prepare-crs.log"
    if [ -f "$WITH_CRS_CRS_PREAMBLE_FILE" ]; then
        return 0
    fi
    if [ ! -d "${CRS_SOURCE_DIR:-$SOURCE_ROOT/coreruleset}" ]; then
        WITH_CRS_BLOCKED_REASON="CRS source missing: ${CRS_SOURCE_DIR:-$SOURCE_ROOT/coreruleset}"
        return 77
    fi
    if [ ! -f "$FRAMEWORK_ROOT/ci/prepare-crs.sh" ]; then
        WITH_CRS_BLOCKED_REASON="CRS prepare helper missing"
        return 77
    fi
    set +e
    SOURCE_ROOT="$SOURCE_ROOT" \
        BUILD_ROOT="$BUILD_ROOT" \
        TMP_ROOT="$TMP_ROOT" \
        LOG_ROOT="$LOG_ROOT" \
        CONNECTOR_ROOT="$CONNECTOR_ROOT" \
        FRAMEWORK_ROOT="$FRAMEWORK_ROOT" \
        sh "$FRAMEWORK_ROOT/ci/prepare-crs.sh" >"$prepare_log" 2>&1
    rc=$?
    set -e
    if [ "$rc" -ne 0 ]; then
        WITH_CRS_BLOCKED_REASON="CRS prepare blocked with exit code $rc"
        return 77
    fi
    if [ ! -f "$WITH_CRS_CRS_PREAMBLE_FILE" ]; then
        WITH_CRS_BLOCKED_REASON="CRS preamble missing after prepare: $WITH_CRS_CRS_PREAMBLE_FILE"
        return 77
    fi
    return 0
}

run_modsecurity_binding_crs_self_test() {
    if ! prepare_crs_for_haproxy; then
        WITH_CRS_BINDING_SELF_TEST_STATUS=BLOCKED
        return 77
    fi
    set +e
    BUILD_ROOT="$BUILD_ROOT" \
        REPO_ROOT="$CONNECTOR_ROOT" \
        MODSECURITY_RULE_PREAMBLE_FILE="$WITH_CRS_CRS_PREAMBLE_FILE" \
        make -C "$CONNECTOR_DIR" self-test-modsecurity-binding-crs >"$WITH_CRS_BINDING_SELF_TEST_LOG" 2>&1
    rc=$?
    set -e
    if [ "$rc" -eq 0 ]; then
        WITH_CRS_BINDING_SELF_TEST_STATUS=PASS
        return 0
    fi
    if [ "$rc" -eq 77 ]; then
        WITH_CRS_BINDING_SELF_TEST_STATUS=BLOCKED
        WITH_CRS_BLOCKED_REASON="crs binding/load path missing"
        return 77
    fi
    WITH_CRS_BINDING_SELF_TEST_STATUS=FAIL
    WITH_CRS_BLOCKED_REASON="CRS binding self-test failed with exit code $rc"
    return 1
}

run_live_with_crs_diagnostic() {
    with_crs_tmp_dir="$RUN_TMP_DIR/with-crs"
    with_crs_spoe_dir="$RUN_SPOE_RUNTIME_DIR/with-crs"
    with_crs_haproxy_cfg="$with_crs_spoe_dir/haproxy.cfg"
    with_crs_spoe_cfg="$with_crs_spoe_dir/spoe-agent.conf"
    with_crs_syntax_log="$WITH_CRS_RUNTIME_LOG_DIR/spoe-config-syntax.log"
    with_crs_docroot="$with_crs_tmp_dir/backend-docroot"
    with_crs_backend_log="$WITH_CRS_RUNTIME_LOG_DIR/backend.stderr.log"
    with_crs_backend_stdout_log="$WITH_CRS_RUNTIME_LOG_DIR/backend.stdout.log"
    with_crs_haproxy_stdout_log="$WITH_CRS_RUNTIME_LOG_DIR/haproxy-runtime.stdout.log"
    with_crs_agent_stdout_log="$WITH_CRS_RUNTIME_LOG_DIR/diagnostic-agent.stdout.log"
    with_crs_agent_stderr_log="$WITH_CRS_RUNTIME_LOG_DIR/diagnostic-agent.stderr.log"
    with_crs_agent_ready="$with_crs_tmp_dir/diagnostic-agent.ready"
    with_crs_agent_pid_file="$with_crs_tmp_dir/diagnostic-agent.pid"
    with_crs_agent_port_file="$with_crs_tmp_dir/diagnostic-agent.port"
    with_crs_block_status_file="$WITH_CRS_RUNTIME_LOG_DIR/http-block-probe.status"
    with_crs_block_response_file="$WITH_CRS_RUNTIME_LOG_DIR/http-block-probe.response"
    with_crs_pass_status_file="$WITH_CRS_RUNTIME_LOG_DIR/http-pass-probe.status"
    with_crs_pass_response_file="$WITH_CRS_RUNTIME_LOG_DIR/http-pass-probe.response"
    with_crs_marker="run_id=$RUN_ID scope=with-crs haproxy_start_marker"
    with_crs_haproxy_port=
    with_crs_spoa_port=
    with_crs_backend_port=

    mkdir -p "$WITH_CRS_RUNTIME_LOG_DIR" "$with_crs_tmp_dir" "$with_crs_spoe_dir" "$with_crs_docroot"
    : >"$WITH_CRS_DIAGNOSTIC_AGENT_LOG"
    : >"$WITH_CRS_HAPROXY_RUNTIME_LOG"
    : >"$WITH_CRS_HTTP_PROBE_LOG"

    if [ "$SPOE_ACTION_ENCODING_VERIFIED" != "true" ]; then
        WITH_CRS_BLOCKED_REASON="spoe action encoding not verified"
        return
    fi
    if [ "$SPOA_RUNTIME_STATUS" != "diagnostic-spop-handshake-subset" ] || [ ! -x "$SPOA_RUNTIME_BIN" ]; then
        WITH_CRS_BLOCKED_REASON="diagnostic spoa agent runtime missing"
        return
    fi
    if ! run_modsecurity_binding_crs_self_test; then
        return
    fi

    with_crs_haproxy_port=$(pick_tcp_port)
    with_crs_spoa_port=$(pick_tcp_port)
    with_crs_backend_port=$(pick_tcp_port)
    {
        echo "global"
        echo "    log stdout format raw local0"
        echo "    pidfile $with_crs_tmp_dir/haproxy.pid"
        echo
        echo "defaults"
        echo "    mode http"
        echo "    timeout connect 1s"
        echo "    timeout client 5s"
        echo "    timeout server 5s"
        echo
        echo "frontend fe_haproxy_spoe_diagnostic"
        echo "    bind 127.0.0.1:$with_crs_haproxy_port"
        echo "    filter spoe engine modsecurity-diagnostic config $with_crs_spoe_cfg"
        echo "    http-request send-spoe-group modsecurity-diagnostic diagnostic-request"
        echo "    http-request deny status 403 if { var(txn.modsecdiag.blocked) -m bool }"
        echo "    default_backend be_haproxy_diagnostic_app"
        echo
        echo "backend be_haproxy_diagnostic_app"
        echo "    mode http"
        echo "    server app1 127.0.0.1:$with_crs_backend_port"
        echo
        echo "backend be_spoa_diagnostic"
        echo "    mode spop"
        echo "    balance roundrobin"
        echo "    timeout connect 1s"
        echo "    timeout server 3s"
        echo "    server spoa1 127.0.0.1:$with_crs_spoa_port"
    } >"$with_crs_haproxy_cfg"
    {
        echo "[modsecurity-diagnostic]"
        echo
        echo "spoe-agent modsecurity-diagnostic-agent"
        echo "    groups diagnostic-request"
        echo "    option var-prefix modsecdiag"
        echo "    register-var-names blocked"
        echo "    option continue-on-error"
        echo "    timeout hello 1s"
        echo "    timeout idle 3s"
        echo "    timeout processing 1s"
        echo "    use-backend be_spoa_diagnostic"
        echo
        echo "spoe-group diagnostic-request"
        echo "    messages check-request"
        echo
        echo "spoe-message check-request"
        echo "    args method=method path=path uri=url host=req.hdr(Host) test_header=req.hdr(X-Haproxy-ModSecurity-Test)"
    } >"$with_crs_spoe_cfg"
    set +e
    "$HAPROXY_BIN" -c -f "$with_crs_haproxy_cfg" >"$with_crs_syntax_log" 2>&1
    rc=$?
    set -e
    if [ "$rc" -ne 0 ]; then
        WITH_CRS_BLOCKED_REASON="with-crs haproxy runtime config failed"
        return
    fi

    printf 'haproxy with-crs diagnostic backend for %s\n' "$RUN_ID" >"$with_crs_docroot/diagnostic.txt"
    "$PYTHON_BIN" -m http.server "$with_crs_backend_port" \
        --bind 127.0.0.1 \
        --directory "$with_crs_docroot" \
        >"$with_crs_backend_stdout_log" \
        2>"$with_crs_backend_log" &
    WITH_CRS_BACKEND_PID=$!
    if ! wait_tcp_port "$with_crs_backend_port"; then
        WITH_CRS_BLOCKED_REASON="with-crs diagnostic backend failed to start"
        return
    fi
    "$SPOA_RUNTIME_BIN" --serve \
        --host 127.0.0.1 \
        --port "$with_crs_spoa_port" \
        --ready-file "$with_crs_agent_ready" \
        --pid-file "$with_crs_agent_pid_file" \
        --port-file "$with_crs_agent_port_file" \
        --log-file "$WITH_CRS_DIAGNOSTIC_AGENT_LOG" \
        --crs-preamble-file "$WITH_CRS_CRS_PREAMBLE_FILE" \
        >"$with_crs_agent_stdout_log" \
        2>"$with_crs_agent_stderr_log" &
    WITH_CRS_AGENT_PID=$!
    i=0
    while [ "$i" -lt 50 ]; do
        if [ -f "$with_crs_agent_ready" ] && kill -0 "$WITH_CRS_AGENT_PID" 2>/dev/null; then
            break
        fi
        i=$((i + 1))
        sleep 0.1
    done
    if ! kill -0 "$WITH_CRS_AGENT_PID" 2>/dev/null; then
        WITH_CRS_BLOCKED_REASON="with-crs diagnostic spoa agent failed to start"
        return
    fi
    printf '%s epoch=%s\n' "$with_crs_marker" "$(date -u +%s)" >>"$WITH_CRS_DIAGNOSTIC_AGENT_LOG"
    "$HAPROXY_BIN" -db -f "$with_crs_haproxy_cfg" \
        >"$with_crs_haproxy_stdout_log" \
        2>"$WITH_CRS_HAPROXY_RUNTIME_LOG" &
    WITH_CRS_HAPROXY_PID=$!
    sleep 0.2
    if ! kill -0 "$WITH_CRS_HAPROXY_PID" 2>/dev/null; then
        WITH_CRS_BLOCKED_REASON="with-crs haproxy runtime failed to start"
        return
    fi

    set +e
    block_probe_rc=1
    i=0
    while [ "$i" -lt 30 ]; do
        run_http_probe "$with_crs_haproxy_port" "$with_crs_block_status_file" "$with_crs_block_response_file" "" 403 "/?id=1%20UNION%20SELECT%20password%20FROM%20users" >>"$WITH_CRS_HTTP_PROBE_LOG" 2>&1
        block_probe_rc=$?
        if [ "$block_probe_rc" -eq 0 ]; then
            break
        fi
        i=$((i + 1))
        sleep 0.1
    done
    pass_probe_rc=1
    i=0
    while [ "$i" -lt 30 ]; do
        run_http_probe "$with_crs_haproxy_port" "$with_crs_pass_status_file" "$with_crs_pass_response_file" "" 200 "/diagnostic.txt" >>"$WITH_CRS_HTTP_PROBE_LOG" 2>&1
        pass_probe_rc=$?
        if [ "$pass_probe_rc" -eq 0 ]; then
            break
        fi
        i=$((i + 1))
        sleep 0.1
    done
    set -e
    if [ -f "$with_crs_block_status_file" ]; then
        WITH_CRS_BLOCK_PROBE_STATUS=$(sed -n '1p' "$with_crs_block_status_file")
    else
        WITH_CRS_BLOCK_PROBE_STATUS=probe-error
    fi
    if [ -f "$with_crs_pass_status_file" ]; then
        WITH_CRS_PASS_PROBE_STATUS=$(sed -n '1p' "$with_crs_pass_status_file")
    else
        WITH_CRS_PASS_PROBE_STATUS=probe-error
    fi
    if agent_evidence_after_marker "$with_crs_marker" "$WITH_CRS_DIAGNOSTIC_AGENT_LOG" "NOTIFY received" "$WITH_CRS_RUNTIME_LOG_DIR/agent-notify-evidence.txt"; then
        WITH_CRS_AGENT_CONTACT_EVIDENCE=$(read_evidence_line "$WITH_CRS_RUNTIME_LOG_DIR/agent-notify-evidence.txt")
    fi
    if agent_evidence_after_marker "$with_crs_marker" "$WITH_CRS_DIAGNOSTIC_AGENT_LOG" "CRS loaded preamble=$WITH_CRS_CRS_PREAMBLE_FILE" "$WITH_CRS_RUNTIME_LOG_DIR/crs-loaded-evidence.txt"; then
        WITH_CRS_CRS_LOADED=true
    fi
    if agent_evidence_after_marker "$with_crs_marker" "$WITH_CRS_DIAGNOSTIC_AGENT_LOG" "CRS live decision disruptive=1 status=403" "$WITH_CRS_RUNTIME_LOG_DIR/crs-live-evidence.txt"; then
        WITH_CRS_MODSECURITY_EVIDENCE=$(read_evidence_line "$WITH_CRS_RUNTIME_LOG_DIR/crs-live-evidence.txt")
    fi
    if agent_evidence_after_marker "$with_crs_marker" "$WITH_CRS_DIAGNOSTIC_AGENT_LOG" "ACK set-var txn.blocked true sent" "$WITH_CRS_RUNTIME_LOG_DIR/spoe-set-var-ack-evidence.txt"; then
        WITH_CRS_SET_VAR_ACK_EVIDENCE=$(read_evidence_line "$WITH_CRS_RUNTIME_LOG_DIR/spoe-set-var-ack-evidence.txt")
    fi
    if [ -z "$WITH_CRS_AGENT_CONTACT_EVIDENCE" ]; then
        WITH_CRS_STATUS=FAIL
        WITH_CRS_BLOCKED_REASON="with-crs agent did not receive notify"
        return
    fi
    if [ "$WITH_CRS_CRS_LOADED" != "true" ]; then
        WITH_CRS_STATUS=FAIL
        WITH_CRS_BLOCKED_REASON="with-crs CRS loaded evidence missing"
        return
    fi
    if [ -z "$WITH_CRS_MODSECURITY_EVIDENCE" ]; then
        WITH_CRS_STATUS=FAIL
        WITH_CRS_BLOCKED_REASON="with-crs modsecurity CRS decision missing"
        return
    fi
    if [ -z "$WITH_CRS_SET_VAR_ACK_EVIDENCE" ]; then
        WITH_CRS_STATUS=FAIL
        WITH_CRS_BLOCKED_REASON="with-crs set-var ACK missing"
        return
    fi
    if [ "$WITH_CRS_BLOCK_PROBE_STATUS" != "403" ] || [ "$block_probe_rc" -ne 0 ]; then
        WITH_CRS_STATUS=FAIL
        WITH_CRS_BLOCKED_REASON="with-crs block probe did not return 403"
        return
    fi
    if [ "$WITH_CRS_PASS_PROBE_STATUS" != "200" ] || [ "$pass_probe_rc" -ne 0 ]; then
        WITH_CRS_STATUS=FAIL
        WITH_CRS_BLOCKED_REASON="with-crs pass probe did not return 200"
        return
    fi
    WITH_CRS_STATUS=PASS
    WITH_CRS_BLOCKED_REASON=
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

find_modsecurity_header_dir() {
    for candidate in \
        "$BUILD_ROOT/nginx-build/output/modsecurity/include" \
        "$BUILD_ROOT/apache-build/output/modsecurity/include" \
        "$SOURCE_ROOT/ModSecurity_V3/headers"
    do
        if [ -f "$candidate/modsecurity/modsecurity.h" ] &&
                [ -f "$candidate/modsecurity/rules_set.h" ] &&
                [ -f "$candidate/modsecurity/transaction.h" ]; then
            printf '%s' "$candidate"
            return 0
        fi
    done
    return 1
}

find_modsecurity_lib_dir() {
    for candidate in \
        "$BUILD_ROOT/nginx-build/output/modsecurity/lib" \
        "$BUILD_ROOT/apache-build/output/modsecurity/lib" \
        "$BUILD_ROOT/nginx-build/ModSecurity_V3/src/.libs" \
        "$BUILD_ROOT/apache-build/ModSecurity_V3/src/.libs"
    do
        if [ -f "$candidate/libmodsecurity.so" ] || [ -f "$candidate/libmodsecurity.a" ]; then
            printf '%s' "$candidate"
            return 0
        fi
    done
    return 1
}

detect_modsecurity_prereqs() {
    MODSECURITY_HEADER_DIR=$(find_modsecurity_header_dir || true)
    if [ -n "$MODSECURITY_HEADER_DIR" ]; then
        MODSECURITY_HEADERS_PRESENT=true
    else
        MODSECURITY_HEADERS_PRESENT=false
    fi
    MODSECURITY_LIBRARY_DIR=$(find_modsecurity_lib_dir || true)
    if [ -n "$MODSECURITY_LIBRARY_DIR" ]; then
        MODSECURITY_LIBRARY_PRESENT=true
    else
        MODSECURITY_LIBRARY_PRESENT=false
    fi
}

run_modsecurity_binding_self_test() {
    detect_modsecurity_prereqs
    if [ "$MODSECURITY_HEADERS_PRESENT" != "true" ]; then
        MODSECURITY_BINDING_STATUS=blocked
        MODSECURITY_BINDING_BUILD_STATUS=BLOCKED
        MODSECURITY_BINDING_SELF_TEST_STATUS=NOT_RUN
        MODSECURITY_BINDING_REASON="libmodsecurity headers missing"
        return
    fi
    if [ "$MODSECURITY_LIBRARY_PRESENT" != "true" ]; then
        MODSECURITY_BINDING_STATUS=blocked
        MODSECURITY_BINDING_BUILD_STATUS=BLOCKED
        MODSECURITY_BINDING_SELF_TEST_STATUS=NOT_RUN
        MODSECURITY_BINDING_REASON="libmodsecurity library missing"
        return
    fi
    if [ ! -f "$CONNECTOR_DIR/Makefile" ]; then
        MODSECURITY_BINDING_STATUS=blocked
        MODSECURITY_BINDING_BUILD_STATUS=BLOCKED
        MODSECURITY_BINDING_SELF_TEST_STATUS=NOT_RUN
        MODSECURITY_BINDING_REASON="connector Makefile missing"
        return
    fi

    set +e
    BUILD_ROOT="$BUILD_ROOT" \
        REPO_ROOT="$CONNECTOR_ROOT" \
        make -C "$CONNECTOR_DIR" build-modsecurity-binding >"$MODSECURITY_BINDING_BUILD_LOG" 2>&1
    rc=$?
    set -e
    if [ "$rc" -eq 0 ]; then
        MODSECURITY_BINDING_BUILD_STATUS=PASS
    elif [ "$rc" -eq 77 ]; then
        MODSECURITY_BINDING_STATUS=blocked
        MODSECURITY_BINDING_BUILD_STATUS=BLOCKED
        MODSECURITY_BINDING_SELF_TEST_STATUS=NOT_RUN
        MODSECURITY_BINDING_REASON="local libmodsecurity API signatures or binding build blocked"
        return
    else
        MODSECURITY_BINDING_STATUS=blocked
        MODSECURITY_BINDING_BUILD_STATUS=FAIL
        MODSECURITY_BINDING_SELF_TEST_STATUS=NOT_RUN
        MODSECURITY_BINDING_REASON="modsecurity binding build failed with exit code $rc"
        return
    fi

    set +e
    BUILD_ROOT="$BUILD_ROOT" \
        REPO_ROOT="$CONNECTOR_ROOT" \
        make -C "$CONNECTOR_DIR" self-test-modsecurity-binding >"$MODSECURITY_BINDING_SELF_TEST_LOG" 2>&1
    rc=$?
    set -e
    if [ "$rc" -eq 0 ]; then
        MODSECURITY_BINDING_STATUS=self-test-verified
        MODSECURITY_BINDING_SELF_TEST_STATUS=PASS
        MODSECURITY_BINDING_REASON="phase-1 header block self-test passed with local libmodsecurity C API"
    elif [ "$rc" -eq 77 ]; then
        MODSECURITY_BINDING_STATUS=blocked
        MODSECURITY_BINDING_SELF_TEST_STATUS=BLOCKED
        MODSECURITY_BINDING_REASON="modsecurity binding self-test blocked"
    else
        MODSECURITY_BINDING_STATUS=blocked
        MODSECURITY_BINDING_SELF_TEST_STATUS=FAIL
        MODSECURITY_BINDING_REASON="modsecurity binding self-test failed with exit code $rc"
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
    verify_spoe_action_encoding
    run_modsecurity_binding_self_test
    run_spoa_runtime_self_test
    write_generated_spoe_config
    run_live_spoe_diagnostic
    run_live_with_crs_diagnostic
    if [ "$WITH_CRS_STATUS" = "PASS" ]; then
        RUNTIME_REASON="haproxy_phase1_header_block and haproxy_crs_sqli_anomaly_block runtime smoke verified"
    elif [ "$WITH_CRS_STATUS" = "FAIL" ]; then
        RUNTIME_RESULT_STATUS=FAIL
        RUNTIME_EXIT_CODE=1
        RUNTIME_STATUS=runtime-smoke-failed
        RUNTIME_REASON="$WITH_CRS_BLOCKED_REASON"
    fi
    example_spoe_config_status=$(detect_example_spoe_config)
    {
        echo "$RUNTIME_RESULT_STATUS $RUNTIME_REASON"
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
        echo "spoe_action_encoding_status=$SPOE_ACTION_ENCODING_STATUS"
        echo "spoe_action_encoding_verified=$SPOE_ACTION_ENCODING_VERIFIED"
        echo "spoe_action_encoding_reason=$SPOE_ACTION_ENCODING_REASON"
        echo "spoe_runtime_status=$SPOE_RUNTIME_STATUS"
        echo "spoe_runtime_verified=$SPOE_RUNTIME_VERIFIED"
        echo "spoe_runtime_blocker=${SPOE_RUNTIME_BLOCKER:-none}"
        echo "haproxy_runtime_started=$HAPROXY_RUNTIME_STARTED"
        echo "diagnostic_agent_started=$DIAGNOSTIC_AGENT_STARTED"
        echo "diagnostic_backend_started=$BACKEND_RUNTIME_STARTED"
        echo "http_probe_status=$HTTP_PROBE_STATUS"
        echo "http_block_probe_status=$HTTP_BLOCK_PROBE_STATUS"
        echo "http_pass_probe_status=$HTTP_PASS_PROBE_STATUS"
        echo "haproxy_contacted_diagnostic_agent=$HAPROXY_CONTACTED_DIAGNOSTIC_AGENT"
        echo "agent_received_notify=$AGENT_RECEIVED_NOTIFY"
        echo "agent_extracted_request_args=$AGENT_EXTRACTED_REQUEST_ARGS"
        echo "agent_contact_evidence=$AGENT_CONTACT_EVIDENCE"
        echo "agent_args_evidence=$AGENT_ARGS_EVIDENCE"
        echo "modsecurity_live_binding_verified=$MODSECURITY_LIVE_BINDING_VERIFIED"
        echo "modsecurity_live_evidence=$MODSECURITY_LIVE_EVIDENCE"
        echo "spoe_set_var_ack_sent=$SPOE_SET_VAR_ACK_SENT"
        echo "spoe_set_var_ack_evidence=$SPOE_SET_VAR_ACK_EVIDENCE"
        echo "example_spoe_config_status=$example_spoe_config_status"
        echo "modsecurity_headers_present=$MODSECURITY_HEADERS_PRESENT"
        echo "modsecurity_header_dir=$MODSECURITY_HEADER_DIR"
        echo "modsecurity_library_present=$MODSECURITY_LIBRARY_PRESENT"
        echo "modsecurity_library_dir=$MODSECURITY_LIBRARY_DIR"
        echo "modsecurity_binding_status=$MODSECURITY_BINDING_STATUS"
        echo "modsecurity_binding_build_status=$MODSECURITY_BINDING_BUILD_STATUS"
        echo "modsecurity_binding_self_test_status=$MODSECURITY_BINDING_SELF_TEST_STATUS"
        echo "modsecurity_binding_reason=$MODSECURITY_BINDING_REASON"
        echo "haproxy_enforcement_status=$HAPROXY_ENFORCEMENT_STATUS"
        echo "haproxy_enforced_block=$HAPROXY_ENFORCED_BLOCK"
        echo "runtime_verified=$RUNTIME_VERIFIED"
        echo "runtime_status=$RUNTIME_STATUS"
        echo "verified_case=$VERIFIED_CASE"
        echo "with_crs_status=$WITH_CRS_STATUS"
        echo "with_crs_verified_case=$WITH_CRS_VERIFIED_CASE"
        echo "with_crs_block_probe_status=$WITH_CRS_BLOCK_PROBE_STATUS"
        echo "with_crs_pass_probe_status=$WITH_CRS_PASS_PROBE_STATUS"
        echo "with_crs_crs_loaded=$WITH_CRS_CRS_LOADED"
        echo "with_crs_crs_preamble_file=$WITH_CRS_CRS_PREAMBLE_FILE"
        echo "with_crs_reason=${WITH_CRS_BLOCKED_REASON:-none}"
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
        "$example_spoe_config_status" "$MODSECURITY_BINDING_STATUS" "$MODSECURITY_HEADERS_PRESENT" \
        "$MODSECURITY_HEADER_DIR" "$MODSECURITY_LIBRARY_PRESENT" "$MODSECURITY_LIBRARY_DIR" \
        "$MODSECURITY_BINDING_BUILD_STATUS" "$MODSECURITY_BINDING_SELF_TEST_STATUS" \
        "$MODSECURITY_BINDING_REASON" "$MODSECURITY_BINDING_BIN" "$MODSECURITY_BINDING_BUILD_LOG" \
        "$MODSECURITY_BINDING_SELF_TEST_LOG" "$HAPROXY_ENFORCEMENT_STATUS" "$SPOA_STARTER_BIN" \
        "$HAPROXY_CFG_EXAMPLE" "$SPOE_AGENT_CFG_EXAMPLE" "$SPOE_ACTION_ENCODING_STATUS" \
        "$SPOE_ACTION_ENCODING_VERIFIED" "$SPOE_ACTION_ENCODING_REASON" "$HTTP_BLOCK_PROBE_STATUS" \
        "$HTTP_PASS_PROBE_STATUS" "$AGENT_RECEIVED_NOTIFY" "$AGENT_EXTRACTED_REQUEST_ARGS" \
        "$AGENT_ARGS_EVIDENCE" "$MODSECURITY_LIVE_BINDING_VERIFIED" "$MODSECURITY_LIVE_EVIDENCE" \
        "$SPOE_SET_VAR_ACK_SENT" "$SPOE_SET_VAR_ACK_EVIDENCE" "$HAPROXY_ENFORCED_BLOCK" \
        "$RUNTIME_RESULT_STATUS" "$RUNTIME_EXIT_CODE" "$RUNTIME_VERIFIED" "$RUNTIME_STATUS" \
        "$RUNTIME_REASON" "$VERIFIED_CASE" "$WITH_CRS_STATUS" "$WITH_CRS_VERIFIED_CASE" \
        "$WITH_CRS_BLOCK_PROBE_STATUS" "$WITH_CRS_PASS_PROBE_STATUS" "$WITH_CRS_CRS_LOADED" \
        "$WITH_CRS_CRS_PREAMBLE_FILE" "$WITH_CRS_BLOCKED_REASON" "$WITH_CRS_RUNTIME_LOG_DIR" \
        "$WITH_CRS_DIAGNOSTIC_AGENT_LOG" "$WITH_CRS_HAPROXY_RUNTIME_LOG" "$WITH_CRS_HTTP_PROBE_LOG" \
        "$WITH_CRS_MODSECURITY_EVIDENCE" "$WITH_CRS_AGENT_CONTACT_EVIDENCE" \
        "$WITH_CRS_SET_VAR_ACK_EVIDENCE" "$WITH_CRS_BINDING_SELF_TEST_STATUS" \
        "$WITH_CRS_BINDING_SELF_TEST_LOG" <<'PY'
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
    modsecurity_headers_present_text,
    modsecurity_header_dir,
    modsecurity_library_present_text,
    modsecurity_library_dir,
    modsecurity_binding_build_status,
    modsecurity_binding_self_test_status,
    modsecurity_binding_reason,
    modsecurity_binding_binary,
    modsecurity_binding_build_log,
    modsecurity_binding_self_test_log,
    haproxy_enforcement_status,
    spoa_starter_bin,
    haproxy_cfg_example,
    spoe_agent_cfg_example,
    spoe_action_encoding_status,
    spoe_action_encoding_verified_text,
    spoe_action_encoding_reason,
    http_block_probe_status,
    http_pass_probe_status,
    agent_received_notify_text,
    agent_extracted_request_args_text,
    agent_args_evidence,
    modsecurity_live_binding_verified_text,
    modsecurity_live_evidence,
    spoe_set_var_ack_sent_text,
    spoe_set_var_ack_evidence,
    haproxy_enforced_block_text,
    runtime_result_status,
    runtime_exit_code_text,
    runtime_verified_text,
    runtime_status,
    runtime_reason,
    verified_case,
    with_crs_status,
    with_crs_verified_case,
    with_crs_block_probe_status,
    with_crs_pass_probe_status,
    with_crs_crs_loaded_text,
    with_crs_crs_preamble_file,
    with_crs_blocked_reason,
    with_crs_runtime_log_dir,
    with_crs_diagnostic_agent_log,
    with_crs_haproxy_runtime_log,
    with_crs_http_probe_log,
    with_crs_modsecurity_evidence,
    with_crs_agent_contact_evidence,
    with_crs_set_var_ack_evidence,
    with_crs_binding_self_test_status,
    with_crs_binding_self_test_log,
) = sys.argv[1:]

now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
starter_checks_available = starter_checks_available_text == "true"
spoa_protocol_runtime_verified = spoa_protocol_runtime_verified_text == "true"
spoe_runtime_verified = spoe_runtime_verified_text == "true"
spoe_action_encoding_verified = spoe_action_encoding_verified_text == "true"
haproxy_runtime_started = haproxy_runtime_started_text == "true"
diagnostic_agent_started = diagnostic_agent_started_text == "true"
diagnostic_backend_started = diagnostic_backend_started_text == "true"
haproxy_contacted_diagnostic_agent = haproxy_contacted_diagnostic_agent_text == "true"
agent_received_notify = agent_received_notify_text == "true"
agent_extracted_request_args = agent_extracted_request_args_text == "true"
modsecurity_live_binding_verified = modsecurity_live_binding_verified_text == "true"
spoe_set_var_ack_sent = spoe_set_var_ack_sent_text == "true"
haproxy_enforced_block = haproxy_enforced_block_text == "true"
modsecurity_headers_present = modsecurity_headers_present_text == "true"
modsecurity_library_present = modsecurity_library_present_text == "true"
runtime_exit_code = int(runtime_exit_code_text)
runtime_verified = runtime_verified_text == "true"
runtime_passed = runtime_result_status == "PASS" and runtime_exit_code == 0 and runtime_verified
with_crs_crs_loaded = with_crs_crs_loaded_text == "true"
crs_verified = with_crs_status == "PASS" and with_crs_crs_loaded
verified_cases = [verified_case] if verified_case else []
if crs_verified and with_crs_verified_case not in verified_cases:
    verified_cases.append(with_crs_verified_case)
no_crs = {
    "status": "PASS" if runtime_verified and verified_case == "haproxy_phase1_header_block" else runtime_result_status,
    "verified_case": "haproxy_phase1_header_block",
    "block_probe_status": int(http_block_probe_status) if http_block_probe_status.isdigit() else http_block_probe_status,
    "pass_probe_status": int(http_pass_probe_status) if http_pass_probe_status.isdigit() else http_pass_probe_status,
}
with_crs = {
    "status": with_crs_status,
    "verified_case": with_crs_verified_case,
    "block_probe_status": int(with_crs_block_probe_status) if with_crs_block_probe_status.isdigit() else with_crs_block_probe_status,
    "pass_probe_status": int(with_crs_pass_probe_status) if with_crs_pass_probe_status.isdigit() else with_crs_pass_probe_status,
    "crs_loaded": with_crs_crs_loaded,
    "crs_preamble_file": with_crs_crs_preamble_file or None,
    "blocked_reason": with_crs_blocked_reason or None,
    "runtime_log_dir": with_crs_runtime_log_dir,
    "diagnostic_agent_log": with_crs_diagnostic_agent_log,
    "haproxy_runtime_log": with_crs_haproxy_runtime_log,
    "http_probe_log": with_crs_http_probe_log,
    "modsecurity_evidence": with_crs_modsecurity_evidence or None,
    "agent_contact_evidence": with_crs_agent_contact_evidence or None,
    "spoe_set_var_ack_evidence": with_crs_set_var_ack_evidence or None,
    "binding_self_test_status": with_crs_binding_self_test_status,
    "binding_self_test_log": with_crs_binding_self_test_log,
}
blocked_reasons = []
if runtime_passed:
    blocked_reasons = []
elif not local_haproxy_bin:
    blocked_reasons.append("haproxy binary missing")
    if prepare_status in {"blocked", "failed", "missing-helper"}:
        blocked_reasons.append(f"haproxy local build blocked: {prepare_reason}")
if not runtime_passed and common_acquisition_status != "defined":
    blocked_reasons.append("haproxy source/binary acquisition is not defined in common.sh")
if not runtime_passed and not spoe_action_encoding_verified:
    blocked_reasons.append(spoe_runtime_blocker or "spoe action encoding not verified")
if not runtime_passed and spoa_agent_runtime_status != "diagnostic-spop-handshake-subset":
    blocked_reasons.append("spoa agent runtime missing")
if not runtime_passed and spoe_config_status != "syntax-valid":
    blocked_reasons.append("spoe config missing")
elif not runtime_passed and not spoe_runtime_verified:
    blocked_reasons.append(spoe_runtime_blocker or "spoe runtime integration not verified")
if runtime_passed:
    pass
elif modsecurity_binding_status == "self-test-verified":
    blocked_reasons.append("haproxy enforcement path missing")
    blocked_reasons.append("framework case runtime not implemented")
else:
    blocked_reasons.append("modsecurity binding missing or not buildable")

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
    "spoe_action_encoding_status": spoe_action_encoding_status,
    "spoe_action_encoding_verified": spoe_action_encoding_verified,
    "spoe_action_encoding_reason": spoe_action_encoding_reason or None,
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
    "http_block_probe_status": http_block_probe_status,
    "http_pass_probe_status": http_pass_probe_status,
    "haproxy_contacted_diagnostic_agent": haproxy_contacted_diagnostic_agent,
    "agent_received_notify": agent_received_notify,
    "agent_extracted_request_args": agent_extracted_request_args,
    "agent_contact_evidence": agent_contact_evidence or None,
    "agent_args_evidence": agent_args_evidence or None,
    "modsecurity_live_binding_verified": modsecurity_live_binding_verified,
    "modsecurity_live_evidence": modsecurity_live_evidence or None,
    "spoe_set_var_ack_sent": spoe_set_var_ack_sent,
    "spoe_set_var_ack_evidence": spoe_set_var_ack_evidence or None,
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
    "modsecurity_headers_present": modsecurity_headers_present,
    "modsecurity_header_dir": modsecurity_header_dir or None,
    "modsecurity_library_present": modsecurity_library_present,
    "modsecurity_library_dir": modsecurity_library_dir or None,
    "modsecurity_binding_build_status": modsecurity_binding_build_status,
    "modsecurity_binding_self_test_status": modsecurity_binding_self_test_status,
    "modsecurity_binding_reason": modsecurity_binding_reason or None,
    "modsecurity_binding_binary": modsecurity_binding_binary,
    "modsecurity_binding_build_log": modsecurity_binding_build_log,
    "modsecurity_binding_self_test_log": modsecurity_binding_self_test_log,
    "haproxy_enforcement_status": haproxy_enforcement_status,
    "haproxy_enforced_block": haproxy_enforced_block,
    "verified_case": verified_case or None,
    "verified_cases": verified_cases,
    "no_crs": no_crs,
    "with_crs": with_crs,
    "crs_verified": crs_verified,
}
record = {
    "connector": connector,
    "check": "runtime-smoke-entrypoint",
    "command": f"make smoke-{connector}",
    "test_type": "runtime-smoke",
    "status": runtime_result_status,
    "exit_code": runtime_exit_code,
    "runtime_verified": runtime_verified,
    "runtime_status": runtime_status,
    "response_body_verified": False,
    "crs_verified": crs_verified,
    "reason": runtime_reason,
    "blocked_reasons": blocked_reasons,
    "diagnostics": diagnostics,
    "verified_case": verified_case or None,
    "verified_cases": verified_cases,
    "no_crs": no_crs,
    "with_crs": with_crs,
    "run_id": run_id,
    "haproxy_runtime_started": haproxy_runtime_started,
    "diagnostic_agent_started": diagnostic_agent_started,
    "diagnostic_backend_started": diagnostic_backend_started,
    "http_probe_status": http_probe_status,
    "http_block_probe_status": http_block_probe_status,
    "http_pass_probe_status": http_pass_probe_status,
    "haproxy_contacted_diagnostic_agent": haproxy_contacted_diagnostic_agent,
    "agent_received_notify": agent_received_notify,
    "agent_extracted_request_args": agent_extracted_request_args,
    "agent_contact_evidence": agent_contact_evidence or None,
    "agent_args_evidence": agent_args_evidence or None,
    "modsecurity_live_binding_verified": modsecurity_live_binding_verified,
    "modsecurity_live_evidence": modsecurity_live_evidence or None,
    "spoe_set_var_ack_sent": spoe_set_var_ack_sent,
    "spoe_set_var_ack_evidence": spoe_set_var_ack_evidence or None,
    "diagnostic_agent_log": diagnostic_agent_log,
    "haproxy_runtime_log": haproxy_runtime_log,
    "haproxy_binary": "present" if local_haproxy_bin else "missing",
    "spoa_agent_runtime_status": spoa_agent_runtime_status,
    "spoa_protocol_runtime_verified": spoa_protocol_runtime_verified,
    "spoe_config_status": spoe_config_status,
    "spoe_action_encoding_status": spoe_action_encoding_status,
    "spoe_action_encoding_verified": spoe_action_encoding_verified,
    "spoe_runtime_status": spoe_runtime_status,
    "spoe_runtime_verified": spoe_runtime_verified,
    "modsecurity_binding_status": modsecurity_binding_status,
    "modsecurity_headers_present": modsecurity_headers_present,
    "modsecurity_library_present": modsecurity_library_present,
    "modsecurity_binding_build_status": modsecurity_binding_build_status,
    "modsecurity_binding_self_test_status": modsecurity_binding_self_test_status,
    "haproxy_enforcement_status": haproxy_enforcement_status,
    "haproxy_enforced_block": haproxy_enforced_block,
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
    "status": runtime_result_status,
    "counts": {
        "PASS": 1 if runtime_result_status == "PASS" else 0,
        "FAIL": 1 if runtime_result_status == "FAIL" else 0,
        "BLOCKED": 1 if runtime_result_status == "BLOCKED" else 0,
        "NOT_RUN": 0,
    },
    "runtime_verified": runtime_verified,
    "runtime_status": runtime_status,
    "response_body_verified": False,
    "crs_verified": crs_verified,
    "reason": runtime_reason,
    "blocked_reasons": blocked_reasons,
    "diagnostics": diagnostics,
    "verified_case": verified_case or None,
    "verified_cases": verified_cases,
    "no_crs": no_crs,
    "with_crs": with_crs,
    "haproxy_runtime_started": haproxy_runtime_started,
    "diagnostic_agent_started": diagnostic_agent_started,
    "diagnostic_backend_started": diagnostic_backend_started,
    "http_probe_status": http_probe_status,
    "http_block_probe_status": http_block_probe_status,
    "http_pass_probe_status": http_pass_probe_status,
    "haproxy_contacted_diagnostic_agent": haproxy_contacted_diagnostic_agent,
    "agent_received_notify": agent_received_notify,
    "agent_extracted_request_args": agent_extracted_request_args,
    "agent_contact_evidence": agent_contact_evidence or None,
    "agent_args_evidence": agent_args_evidence or None,
    "modsecurity_live_binding_verified": modsecurity_live_binding_verified,
    "modsecurity_live_evidence": modsecurity_live_evidence or None,
    "spoe_set_var_ack_sent": spoe_set_var_ack_sent,
    "spoe_set_var_ack_evidence": spoe_set_var_ack_evidence or None,
    "diagnostic_agent_log": diagnostic_agent_log,
    "haproxy_runtime_log": haproxy_runtime_log,
    "haproxy_binary": "present" if local_haproxy_bin else "missing",
    "spoa_agent_runtime_status": spoa_agent_runtime_status,
    "spoa_protocol_runtime_verified": spoa_protocol_runtime_verified,
    "spoe_config_status": spoe_config_status,
    "spoe_action_encoding_status": spoe_action_encoding_status,
    "spoe_action_encoding_verified": spoe_action_encoding_verified,
    "spoe_action_encoding_reason": spoe_action_encoding_reason or None,
    "spoe_runtime_status": spoe_runtime_status,
    "spoe_runtime_verified": spoe_runtime_verified,
    "modsecurity_binding_status": modsecurity_binding_status,
    "modsecurity_headers_present": modsecurity_headers_present,
    "modsecurity_library_present": modsecurity_library_present,
    "modsecurity_binding_build_status": modsecurity_binding_build_status,
    "modsecurity_binding_self_test_status": modsecurity_binding_self_test_status,
    "haproxy_enforcement_status": haproxy_enforcement_status,
    "haproxy_enforced_block": haproxy_enforced_block,
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
    handle.write(runtime_result_status + " runtime-smoke-entrypoint " + runtime_reason + "\n")
    handle.write("spoa_agent_runtime_status: " + spoa_agent_runtime_status + "\n")
    handle.write("spoa_protocol_runtime_verified: " + str(spoa_protocol_runtime_verified).lower() + "\n")
    handle.write("spoe_config_status: " + spoe_config_status + "\n")
    handle.write("spoe_action_encoding_status: " + spoe_action_encoding_status + "\n")
    handle.write("spoe_action_encoding_verified: " + str(spoe_action_encoding_verified).lower() + "\n")
    handle.write("spoe_runtime_status: " + spoe_runtime_status + "\n")
    handle.write("spoe_runtime_verified: " + str(spoe_runtime_verified).lower() + "\n")
    handle.write("haproxy_runtime_started: " + str(haproxy_runtime_started).lower() + "\n")
    handle.write("diagnostic_agent_started: " + str(diagnostic_agent_started).lower() + "\n")
    handle.write("diagnostic_backend_started: " + str(diagnostic_backend_started).lower() + "\n")
    handle.write("http_probe_status: " + http_probe_status + "\n")
    handle.write("http_block_probe_status: " + http_block_probe_status + "\n")
    handle.write("http_pass_probe_status: " + http_pass_probe_status + "\n")
    handle.write("haproxy_contacted_diagnostic_agent: " + str(haproxy_contacted_diagnostic_agent).lower() + "\n")
    handle.write("agent_received_notify: " + str(agent_received_notify).lower() + "\n")
    handle.write("agent_extracted_request_args: " + str(agent_extracted_request_args).lower() + "\n")
    if agent_contact_evidence:
        handle.write("agent_contact_evidence: " + agent_contact_evidence + "\n")
    if agent_args_evidence:
        handle.write("agent_args_evidence: " + agent_args_evidence + "\n")
    handle.write("modsecurity_live_binding_verified: " + str(modsecurity_live_binding_verified).lower() + "\n")
    if modsecurity_live_evidence:
        handle.write("modsecurity_live_evidence: " + modsecurity_live_evidence + "\n")
    handle.write("spoe_set_var_ack_sent: " + str(spoe_set_var_ack_sent).lower() + "\n")
    if spoe_set_var_ack_evidence:
        handle.write("spoe_set_var_ack_evidence: " + spoe_set_var_ack_evidence + "\n")
    handle.write("modsecurity_headers_present: " + str(modsecurity_headers_present).lower() + "\n")
    handle.write("modsecurity_library_present: " + str(modsecurity_library_present).lower() + "\n")
    handle.write("modsecurity_binding_status: " + modsecurity_binding_status + "\n")
    handle.write("modsecurity_binding_build_status: " + modsecurity_binding_build_status + "\n")
    handle.write("modsecurity_binding_self_test_status: " + modsecurity_binding_self_test_status + "\n")
    handle.write("haproxy_enforcement_status: " + haproxy_enforcement_status + "\n")
    handle.write("haproxy_enforced_block: " + str(haproxy_enforced_block).lower() + "\n")
    handle.write("runtime_verified: " + str(runtime_verified).lower() + "\n")
    handle.write("runtime_status: " + runtime_status + "\n")
    if verified_case:
        handle.write("verified_case: " + verified_case + "\n")
    if verified_cases:
        handle.write("verified_cases: " + ", ".join(verified_cases) + "\n")
    handle.write("no_crs.status: " + no_crs["status"] + "\n")
    handle.write("no_crs.verified_case: " + no_crs["verified_case"] + "\n")
    handle.write("no_crs.block_probe_status: " + str(no_crs["block_probe_status"]) + "\n")
    handle.write("no_crs.pass_probe_status: " + str(no_crs["pass_probe_status"]) + "\n")
    handle.write("with_crs.status: " + with_crs["status"] + "\n")
    handle.write("with_crs.verified_case: " + with_crs["verified_case"] + "\n")
    handle.write("with_crs.block_probe_status: " + str(with_crs["block_probe_status"]) + "\n")
    handle.write("with_crs.pass_probe_status: " + str(with_crs["pass_probe_status"]) + "\n")
    handle.write("with_crs.crs_loaded: " + str(with_crs["crs_loaded"]).lower() + "\n")
    handle.write("with_crs.crs_preamble_file: " + str(with_crs["crs_preamble_file"]) + "\n")
    if with_crs["blocked_reason"]:
        handle.write("with_crs.blocked_reason: " + with_crs["blocked_reason"] + "\n")
    if with_crs["modsecurity_evidence"]:
        handle.write("with_crs.modsecurity_evidence: " + with_crs["modsecurity_evidence"] + "\n")
    handle.write("crs_verified: " + str(crs_verified).lower() + "\n")
    handle.write("response_body_verified: false\n")
    for item in blocked_reasons:
        handle.write(f"- {item}\n")
    if not runtime_verified:
        handle.write("Runtime not verified\n")
    handle.write("The SPOA diagnostic runtime is a minimal diagnostic SPOP handshake subset, not a full SPOA agent implementation.\n")
    handle.write(f"{note}\n")
PY
}

validate_roots
ensure_local_haproxy
write_blocked_evidence
echo "$CONNECTOR_NAME runtime smoke: $RUNTIME_RESULT_STATUS - $RUNTIME_REASON"
if [ "$RUNTIME_VERIFIED" != "true" ]; then
    echo "Runtime not verified"
fi
exit "$RUNTIME_EXIT_CODE"
