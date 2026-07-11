#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
CONNECTOR_DIR=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
REPO_ROOT=$(CDPATH= cd "$CONNECTOR_DIR/../.." && pwd)
BUILD_ROOT=${BUILD_ROOT:-${XDG_STATE_HOME:-${HOME:-/tmp}/.local/state}/ModSecurity-conector-build}
HAPROXY_BIN=${HAPROXY_BIN:-$BUILD_ROOT/haproxy-htx-runtime-smoke/overlay-build/worktree/haproxy}
RUNTIME_ROOT=${RUNTIME_ROOT:-$BUILD_ROOT/haproxy-htx-runtime-smoke}
EVENT_LOG_PATH=${EVENT_LOG_PATH:-$RUNTIME_ROOT/events.jsonl}
PYTHON_BIN=${PYTHON:-python3}
HELPER="$SCRIPT_DIR/haproxy_htx_smoke_helper.py"
SUMMARY="$RUNTIME_ROOT/runtime-summary.txt"
VERSION_FILE="$RUNTIME_ROOT/haproxy-version.txt"
BUILD_PROVENANCE="${HAPROXY_HTX_BUILD_PROVENANCE:-$(dirname "$(dirname "$HAPROXY_BIN")")/overlay-build.env}"
upstream_pid=
haproxy_pid=

missing_dependency() {
    echo "haproxy_htx_runtime: BLOCKED - $1" >&2
    exit 77
}

cleanup_haproxy() {
    if [ -n "$haproxy_pid" ] && kill -0 "$haproxy_pid" 2>/dev/null; then
        kill "$haproxy_pid" 2>/dev/null || true
    fi
    if [ -n "$haproxy_pid" ]; then
        set +e
        wait "$haproxy_pid" 2>/dev/null
        set -e
    fi
    haproxy_pid=
}

cleanup() {
    cleanup_haproxy
    if [ -n "$upstream_pid" ] && kill -0 "$upstream_pid" 2>/dev/null; then
        kill "$upstream_pid" 2>/dev/null || true
    fi
    if [ -n "$upstream_pid" ]; then
        set +e
        wait "$upstream_pid" 2>/dev/null
        set -e
    fi
}
trap cleanup EXIT HUP INT TERM

[ -x "$HAPROXY_BIN" ] || missing_dependency "patched HAProxy binary is not executable: $HAPROXY_BIN"
[ -f "$HELPER" ] || missing_dependency "HTX smoke helper is missing: $HELPER"
[ -f "$BUILD_PROVENANCE" ] || missing_dependency "HTX overlay provenance is missing: $BUILD_PROVENANCE"
command -v "$PYTHON_BIN" >/dev/null 2>&1 || missing_dependency "Python interpreter is missing: $PYTHON_BIN"

case "$RUNTIME_ROOT" in
    /*) ;;
    *) echo "haproxy_htx_runtime: FAIL - RUNTIME_ROOT must be absolute" >&2; exit 1 ;;
esac
case "$RUNTIME_ROOT" in
    "$REPO_ROOT"|"$REPO_ROOT"/*)
        echo "haproxy_htx_runtime: FAIL - RUNTIME_ROOT must not be inside the checkout" >&2
        exit 1
        ;;
esac
case "$EVENT_LOG_PATH" in
    "$RUNTIME_ROOT"/*) ;;
    *) echo "haproxy_htx_runtime: FAIL - EVENT_LOG_PATH must be under RUNTIME_ROOT" >&2; exit 1 ;;
esac
mkdir -p "$RUNTIME_ROOT/cases"
rm -f "$EVENT_LOG_PATH" "$SUMMARY"

"$HAPROXY_BIN" -vv >"$VERSION_FILE" 2>&1
if ! grep -Fq 'HAProxy version 3.2.21' "$VERSION_FILE"; then
    echo "haproxy_htx_runtime: FAIL - patched binary is not HAProxy 3.2.21" >&2
    sed -n '1,40p' "$VERSION_FILE" >&2 || true
    exit 1
fi

upstream_port=$("$PYTHON_BIN" "$HELPER" free-port)
"$PYTHON_BIN" "$HELPER" serve-upstream --port "$upstream_port" \
    >"$RUNTIME_ROOT/upstream.stdout.log" 2>"$RUNTIME_ROOT/upstream.stderr.log" &
upstream_pid=$!

run_case() {
    case_name=$1
    phase=$2
    rule_id=$3
    request_header_id=$4
    host_action=$5
    listener_port=$("$PYTHON_BIN" "$HELPER" free-port)
    case_root="$RUNTIME_ROOT/cases/$case_name"
    rules_file="$case_root/rules.conf"
    config_file="$case_root/haproxy.cfg"
    log_file="$case_root/haproxy.stderr.log"

    mkdir -p "$case_root"
    "$PYTHON_BIN" "$HELPER" write-rules --path "$rules_file" --case "$case_name"
    "$PYTHON_BIN" "$HELPER" write-config --path "$config_file" \
        --listen-port "$listener_port" --upstream-port "$upstream_port" --rules-file "$rules_file"
    if grep -Eq 'filter spoe|send-spoe|http-buffer-request|wait-for-body|res\.body' "$config_file"; then
        echo "haproxy_htx_runtime: FAIL - generated $case_name config contains a compatibility/buffering directive" >&2
        exit 1
    fi
    if ! grep -Fq 'filter modsecurity-htx rules-file' "$config_file"; then
        echo "haproxy_htx_runtime: FAIL - generated $case_name config does not select modsecurity-htx" >&2
        exit 1
    fi
    if ! "$HAPROXY_BIN" -c -f "$config_file" >"$case_root/config-check.stdout.log" \
        2>"$case_root/config-check.stderr.log"; then
        echo "haproxy_htx_runtime: FAIL - HAProxy rejected $case_name HTX config" >&2
        sed -n '1,160p' "$case_root/config-check.stderr.log" >&2 || true
        exit 1
    fi

    "$HAPROXY_BIN" -db -f "$config_file" >"$case_root/haproxy.stdout.log" 2>"$log_file" &
    haproxy_pid=$!
    ready=0
    attempt=0
    while [ "$attempt" -lt 30 ]; do
        attempt=$((attempt + 1))
        if ! kill -0 "$haproxy_pid" 2>/dev/null; then
            echo "haproxy_htx_runtime: FAIL - $case_name HAProxy exited early" >&2
            sed -n '1,160p' "$log_file" >&2 || true
            exit 1
        fi
        if "$PYTHON_BIN" "$HELPER" wait-port --port "$listener_port" >/dev/null 2>&1; then
            ready=1
            break
        fi
        sleep 1
    done
    if [ "$ready" -ne 1 ]; then
        echo "haproxy_htx_runtime: FAIL - $case_name listener did not become ready" >&2
        exit 1
    fi

    case "$case_name" in
        phase1)
            status=$("$PYTHON_BIN" "$HELPER" probe --url "http://127.0.0.1:$listener_port/phase1" \
                --header "X-Request-Id: $request_header_id" --header "X-Modsec-Htx: htx-phase1-marker")
            expected_log="modsecurity-htx: request intervention observed; transaction_id=[A-Za-z0-9._-]+ phase=1 status=403 rule_id=$rule_id action=deny"
            ;;
        phase2)
            status=$("$PYTHON_BIN" "$HELPER" probe --url "http://127.0.0.1:$listener_port/phase2" \
                --method POST --data htx-request-body-marker --header "X-Request-Id: $request_header_id")
            expected_log="modsecurity-htx: request-body intervention observed; transaction_id=[A-Za-z0-9._-]+ phase=2 status=403 rule_id=$rule_id action=deny"
            ;;
        phase3)
            status=$("$PYTHON_BIN" "$HELPER" probe --url "http://127.0.0.1:$listener_port/phase3" \
                --header "X-Request-Id: $request_header_id")
            expected_log="modsecurity-htx: response-header intervention observed; transaction_id=[A-Za-z0-9._-]+ phase=3 status=403 rule_id=$rule_id action=deny"
            ;;
        phase4)
            status=$("$PYTHON_BIN" "$HELPER" probe --url "http://127.0.0.1:$listener_port/phase4" \
                --header "X-Request-Id: $request_header_id")
            expected_log="modsecurity-htx: response-body late intervention observed; transaction_id=[A-Za-z0-9._-]+ phase=4 status=403 rule_id=$rule_id requested_action=deny resolved_policy_action=log_only host_action=not_attempted"
            ;;
        *) echo "haproxy_htx_runtime: FAIL - unknown case: $case_name" >&2; exit 1 ;;
    esac
    if [ "$status" != "200" ]; then
        echo "haproxy_htx_runtime: FAIL - $case_name returned $status, expected observer-mode 200" >&2
        exit 1
    fi
    cleanup_haproxy
    if ! grep -Eq "$expected_log" "$log_file"; then
        echo "haproxy_htx_runtime: FAIL - $case_name lacks expected metadata-only HTX observation" >&2
        sed -n '1,160p' "$log_file" >&2 || true
        exit 1
    fi
    observed_transaction_id=$(sed -n 's/.*transaction_id=\([A-Za-z0-9._-][A-Za-z0-9._-]*\) phase=.*/\1/p' "$log_file" | tail -n 1)
    if [ -z "$observed_transaction_id" ]; then
        echo "haproxy_htx_runtime: FAIL - $case_name did not expose a safe HAProxy transaction id" >&2
        exit 1
    fi
    "$PYTHON_BIN" "$HELPER" write-event --path "$EVENT_LOG_PATH" --case "$case_name" \
        --transaction-id "$observed_transaction_id" --phase "$phase" --rule-id "$rule_id" \
        --observed-status "$status" --host-action "$host_action"
}

run_case phase1 1 910001 haproxy-htx-phase1 not_enforced
run_case phase2 2 910002 haproxy-htx-phase2 not_enforced
run_case phase3 3 910003 haproxy-htx-phase3 not_enforced
run_case phase4 4 910004 haproxy-htx-phase4 not_attempted

if [ "$(wc -l < "$EVENT_LOG_PATH")" -ne 4 ]; then
    echo "haproxy_htx_runtime: FAIL - expected four HTX metadata events" >&2
    exit 1
fi
if grep -Fq 'htx-request-body-marker' "$EVENT_LOG_PATH" || \
    grep -Fq 'haproxy-htx-response-body-marker' "$EVENT_LOG_PATH"; then
    echo "haproxy_htx_runtime: FAIL - metadata evidence contains a body payload" >&2
    exit 1
fi

{
    printf 'status=PASS\n'
    printf 'integration_mode=native_htx_filter\n'
    printf 'evaluation_mode=observer_nonpromoted\n'
    printf 'rule_evaluation=libmodsecurity_observed\n'
    printf 'common_runtime_bridge=false\n'
    printf 'precommit_enforcement=false\n'
    printf 'phase1_observed_client_status=200\n'
    printf 'phase2_observed_client_status=200\n'
    printf 'phase3_observed_client_status=200\n'
    printf 'phase4_observed_client_status=200\n'
    printf 'phase4_safe_host_action=not_attempted\n'
    printf 'response_body_stream_observed=true\n'
    printf 'transaction_id_observed=true\n'
    printf 'payload_recorded=false\n'
    printf 'capability_promotion=not_permitted\n'
    printf 'overlay_build_provenance=%s\n' "$BUILD_PROVENANCE"
    printf 'event_log=%s\n' "$EVENT_LOG_PATH"
    printf 'haproxy_version=%s\n' "$VERSION_FILE"
    printf 'production_ready=false\n'
} > "$SUMMARY"

cleanup
upstream_pid=
trap - EXIT HUP INT TERM
printf 'processes_stopped=yes\n' >> "$SUMMARY"
printf 'haproxy_htx_runtime: pass (non-promoted) summary=%s\n' "$SUMMARY"
