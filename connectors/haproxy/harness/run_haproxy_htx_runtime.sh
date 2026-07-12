#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
CONNECTOR_DIR=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
REPO_ROOT=$(CDPATH= cd "$CONNECTOR_DIR/../.." && pwd)
BUILD_ROOT=${BUILD_ROOT:-${XDG_STATE_HOME:-${HOME:-/tmp}/.local/state}/ModSecurity-conector-build}
HAPROXY_BIN=${HAPROXY_BIN:-$BUILD_ROOT/haproxy-htx-runtime-smoke/overlay-build/worktree/haproxy}
RUNTIME_ROOT=${RUNTIME_ROOT:-$BUILD_ROOT/haproxy-htx-runtime-smoke}
EVENT_LOG_PATH=${EVENT_LOG_PATH:-$RUNTIME_ROOT/events.jsonl}
HOST_EVIDENCE_LOG_PATH=${HAPROXY_HTX_HOST_EVIDENCE_LOG_PATH:-$RUNTIME_ROOT/host-runtime-evidence.jsonl}
CANONICAL_RULES_FILE=${HAPROXY_HTX_CANONICAL_RULES_FILE:-$REPO_ROOT/modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf}
PYTHON_BIN=${PYTHON:-python3}
HELPER="$SCRIPT_DIR/haproxy_htx_smoke_helper.py"
SYNCHRONIZED_UPSTREAM="$REPO_ROOT/modules/ModSecurity-test-Framework/tests/runners/synchronized_upstream.py"
SUMMARY="$RUNTIME_ROOT/runtime-summary.txt"
VERSION_FILE="$RUNTIME_ROOT/haproxy-version.txt"
UPSTREAM_LOG="$RUNTIME_ROOT/upstream-requests.jsonl"
BUILD_PROVENANCE=${HAPROXY_HTX_BUILD_PROVENANCE:-$(dirname "$(dirname "$HAPROXY_BIN")")/overlay-build.env}
FIRST_BYTE_EVIDENCE_PATH=${FULL_LIFECYCLE_EVIDENCE_OUTPUT:-$RUNTIME_ROOT/first-byte-evidence.json}
RUN_ID=${NO_CRS_RUN_ID:-haproxy-htx-local}
upstream_pid=
haproxy_pid=
sync_upstream_pid=
streaming_client_pid=

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

cleanup_streaming_client() {
    if [ -n "$streaming_client_pid" ] && kill -0 "$streaming_client_pid" 2>/dev/null; then
        kill "$streaming_client_pid" 2>/dev/null || true
    fi
    if [ -n "$streaming_client_pid" ]; then
        set +e
        wait "$streaming_client_pid" 2>/dev/null
        set -e
    fi
    streaming_client_pid=
}

cleanup_synchronized_upstream() {
    if [ -n "$sync_upstream_pid" ] && kill -0 "$sync_upstream_pid" 2>/dev/null; then
        kill "$sync_upstream_pid" 2>/dev/null || true
    fi
    if [ -n "$sync_upstream_pid" ]; then
        set +e
        wait "$sync_upstream_pid" 2>/dev/null
        set -e
    fi
    sync_upstream_pid=
}

cleanup() {
    cleanup_streaming_client
    cleanup_haproxy
    cleanup_synchronized_upstream
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
[ -f "$SYNCHRONIZED_UPSTREAM" ] || missing_dependency "synchronized upstream helper is missing: $SYNCHRONIZED_UPSTREAM"
[ -f "$BUILD_PROVENANCE" ] || missing_dependency "HTX overlay provenance is missing: $BUILD_PROVENANCE"
[ -f "$CANONICAL_RULES_FILE" ] || missing_dependency "canonical No-CRS rules are missing: $CANONICAL_RULES_FILE"
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
case "$HOST_EVIDENCE_LOG_PATH" in
    "$RUNTIME_ROOT"/*) ;;
    *) echo "haproxy_htx_runtime: FAIL - HAPROXY_HTX_HOST_EVIDENCE_LOG_PATH must be under RUNTIME_ROOT" >&2; exit 1 ;;
esac
case "$FIRST_BYTE_EVIDENCE_PATH" in
    /*) ;;
    *) echo "haproxy_htx_runtime: FAIL - FULL_LIFECYCLE_EVIDENCE_OUTPUT must be absolute" >&2; exit 1 ;;
esac
case "$FIRST_BYTE_EVIDENCE_PATH" in
    "$REPO_ROOT"|"$REPO_ROOT"/*)
        echo "haproxy_htx_runtime: FAIL - FULL_LIFECYCLE_EVIDENCE_OUTPUT must not be inside the checkout" >&2
        exit 1
        ;;
esac
case "$RUN_ID" in
    [A-Za-z0-9]*) ;;
    *) echo "haproxy_htx_runtime: FAIL - NO_CRS_RUN_ID is unsafe" >&2; exit 1 ;;
esac
case "$RUN_ID" in
    *[!A-Za-z0-9._-]*) echo "haproxy_htx_runtime: FAIL - NO_CRS_RUN_ID is unsafe" >&2; exit 1 ;;
esac
mkdir -p "$RUNTIME_ROOT/cases"
[ ! -e "$FIRST_BYTE_EVIDENCE_PATH" ] || {
    echo "haproxy_htx_runtime: FAIL - first-byte evidence output must be fresh: $FIRST_BYTE_EVIDENCE_PATH" >&2
    exit 1
}
rm -f "$EVENT_LOG_PATH" "$HOST_EVIDENCE_LOG_PATH" "$SUMMARY" "$UPSTREAM_LOG"

"$HAPROXY_BIN" -vv >"$VERSION_FILE" 2>&1
if ! grep -Fq 'HAProxy version 3.2.21' "$VERSION_FILE"; then
    echo "haproxy_htx_runtime: FAIL - patched binary is not HAProxy 3.2.21" >&2
    sed -n '1,40p' "$VERSION_FILE" >&2 || true
    exit 1
fi

upstream_port=$("$PYTHON_BIN" "$HELPER" free-port)
"$PYTHON_BIN" "$HELPER" serve-upstream --port "$upstream_port" --request-log "$UPSTREAM_LOG" \
    >"$RUNTIME_ROOT/upstream.stdout.log" 2>"$RUNTIME_ROOT/upstream.stderr.log" &
upstream_pid=$!
phase2_upstream_request_count=not_observed
phase2_request_dispatch_observed=not_observed
phase2_host_action=enforced_reply

run_case() {
    case_name=$1
    phase=$2
    rule_id=$3
    expected_status=$4
    upstream_profile=$5
    expected_upstream_requests=$6
    host_action=$7
    listener_port=$("$PYTHON_BIN" "$HELPER" free-port)
    case_root="$RUNTIME_ROOT/cases/$case_name"
    rules_file="$case_root/rules.conf"
    config_file="$case_root/haproxy.cfg"
    log_file="$case_root/haproxy.stderr.log"
    probe_file="$case_root/client-probe.json"
    before_upstream=$("$PYTHON_BIN" "$HELPER" upstream-count --path "$UPSTREAM_LOG" --profile "$upstream_profile")

    mkdir -p "$case_root"
    "$PYTHON_BIN" "$HELPER" write-rules --path "$rules_file" --canonical-rules "$CANONICAL_RULES_FILE"
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
    if grep -Fq '91000' "$rules_file"; then
        echo "haproxy_htx_runtime: FAIL - generated $case_name rules use temporary 91000x IDs" >&2
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

    expected_log=
    case "$case_name" in
        allow)
            status=$("$PYTHON_BIN" "$HELPER" probe --url "http://127.0.0.1:$listener_port/no-crs/allow" \
                --header 'X-Request-Id: haproxy-htx-allow' --evidence-path "$probe_file")
            ;;
        phase1_403)
            status=$("$PYTHON_BIN" "$HELPER" probe --url "http://127.0.0.1:$listener_port/no-crs/deny" \
                --header 'X-Request-Id: haproxy-htx-phase1-403' --header 'X-Modsec-Smoke: block' \
                --evidence-path "$probe_file")
            expected_log="modsecurity-htx: request intervention observed; transaction_id=[A-Za-z0-9._-]+ phase=1 status=403 rule_id=$rule_id action=deny"
            ;;
        phase1_429)
            status=$("$PYTHON_BIN" "$HELPER" probe --url "http://127.0.0.1:$listener_port/no-crs/alternative-status" \
                --header 'X-Request-Id: haproxy-htx-phase1-429' --header 'X-Modsec-Smoke: alternative-status' \
                --evidence-path "$probe_file")
            expected_log="modsecurity-htx: request intervention observed; transaction_id=[A-Za-z0-9._-]+ phase=1 status=429 rule_id=$rule_id action=deny"
            ;;
        phase2_client_deny)
            status=$("$PYTHON_BIN" "$HELPER" probe --url "http://127.0.0.1:$listener_port/no-crs/request-body" \
                --method POST --data no-crs-request-body-marker --header 'Content-Type: text/plain' \
                --header 'X-Request-Id: haproxy-htx-phase2' --evidence-path "$probe_file")
            expected_log="modsecurity-htx: request-body intervention observed; transaction_id=[A-Za-z0-9._-]+ phase=2 status=403 rule_id=$rule_id action=deny"
            ;;
        phase3_403)
            status=$("$PYTHON_BIN" "$HELPER" probe --url "http://127.0.0.1:$listener_port/no-crs/response-header" \
                --header 'X-Request-Id: haproxy-htx-phase3-403' --evidence-path "$probe_file")
            expected_log="modsecurity-htx: response-header intervention observed; transaction_id=[A-Za-z0-9._-]+ phase=3 status=403 rule_id=$rule_id action=deny"
            ;;
        *) echo "haproxy_htx_runtime: FAIL - unknown case: $case_name" >&2; exit 1 ;;
    esac
    if [ "$status" != "$expected_status" ]; then
        echo "haproxy_htx_runtime: FAIL - $case_name returned $status, expected $expected_status" >&2
        exit 1
    fi
    cleanup_haproxy
    after_upstream=$("$PYTHON_BIN" "$HELPER" upstream-count --path "$UPSTREAM_LOG" --profile "$upstream_profile")
    actual_upstream_requests=$((after_upstream - before_upstream))
    case "$expected_upstream_requests" in
        0-or-1)
            case "$actual_upstream_requests" in
                0|1) ;;
                *)
                    echo "haproxy_htx_runtime: FAIL - $case_name reached upstream $actual_upstream_requests times, expected zero or one" >&2
                    exit 1
                    ;;
            esac
            ;;
        *)
            if [ "$actual_upstream_requests" -ne "$expected_upstream_requests" ]; then
                echo "haproxy_htx_runtime: FAIL - $case_name reached upstream $actual_upstream_requests times, expected $expected_upstream_requests" >&2
                exit 1
            fi
            ;;
    esac
    if [ "$case_name" = phase2_client_deny ]; then
        phase2_upstream_request_count=$actual_upstream_requests
        case "$actual_upstream_requests" in
            0)
                phase2_request_dispatch_observed=false
                ;;
            1)
                phase2_request_dispatch_observed=true
                ;;
        esac
    fi
    if [ -n "$expected_log" ] && ! grep -Eq "$expected_log" "$log_file"; then
        echo "haproxy_htx_runtime: FAIL - $case_name lacks the expected HAProxy/libmodsecurity observation" >&2
        sed -n '1,160p' "$log_file" >&2 || true
        exit 1
    fi
    if [ -n "$expected_log" ]; then
        "$PYTHON_BIN" "$HELPER" write-host-evidence --path "$HOST_EVIDENCE_LOG_PATH" \
            --case "$case_name" --phase "$phase" --rule-id "$rule_id" --probe-path "$probe_file" \
            --upstream-requests "$actual_upstream_requests" --host-action "$host_action" \
            --decision-log "$log_file"
    else
        "$PYTHON_BIN" "$HELPER" write-host-evidence --path "$HOST_EVIDENCE_LOG_PATH" \
            --case "$case_name" --phase "$phase" --rule-id "$rule_id" --probe-path "$probe_file" \
            --upstream-requests "$actual_upstream_requests" --host-action "$host_action"
    fi
    case "$host_action" in
        enforced_reply)
            if [ "$phase" -eq 3 ]; then
                "$PYTHON_BIN" "$HELPER" write-event --path "$EVENT_LOG_PATH" --case "$case_name" \
                    --decision-log "$log_file" --phase "$phase" --rule-id "$rule_id" \
                    --observed-status "$status" --host-action enforced_reply --original-http-status 200
            else
                "$PYTHON_BIN" "$HELPER" write-event --path "$EVENT_LOG_PATH" --case "$case_name" \
                    --decision-log "$log_file" --phase "$phase" --rule-id "$rule_id" \
                    --observed-status "$status" --host-action enforced_reply
            fi
            ;;
    esac
}

run_phase4_safe_barrier() {
    case_name=phase4_safe_barrier
    phase=4
    rule_id=1100301
    expected_status=200
    listener_port=$("$PYTHON_BIN" "$HELPER" free-port)
    case_root="$RUNTIME_ROOT/cases/$case_name"
    rules_file="$case_root/rules.conf"
    config_file="$case_root/haproxy.cfg"
    log_file="$case_root/haproxy.stderr.log"
    ready_file="$case_root/upstream-ready.json"
    paused_file="$case_root/upstream-paused.json"
    release_file="$case_root/upstream-release"
    server_evidence_file="$case_root/upstream-server.json"
    client_first_byte_file="$case_root/client-first-byte.json"
    client_probe_file="$case_root/client-probe.json"

    mkdir -p "$case_root"
    rm -f "$ready_file" "$paused_file" "$release_file" "$server_evidence_file" \
        "$client_first_byte_file" "$client_probe_file"

    # The upstream sends its first HTTP/1.1 body chunk, publishes that EOS is
    # still absent, and waits for this runner to release it.  That makes the
    # client-first-byte observation a real host boundary rather than a
    # post-response fixture check.
    "$PYTHON_BIN" "$SYNCHRONIZED_UPSTREAM" --serve \
        --ready-file "$ready_file" --paused-file "$paused_file" \
        --release-file "$release_file" --server-evidence-file "$server_evidence_file" \
        --timeout 10 >"$case_root/synchronized-upstream.stdout.log" \
        2>"$case_root/synchronized-upstream.stderr.log" &
    sync_upstream_pid=$!
    if ! "$PYTHON_BIN" "$HELPER" wait-file --path "$ready_file" --timeout 10; then
        echo "haproxy_htx_runtime: FAIL - $case_name synchronized upstream did not become ready" >&2
        sed -n '1,160p' "$case_root/synchronized-upstream.stderr.log" >&2 || true
        exit 1
    fi
    synchronized_upstream_port=$("$PYTHON_BIN" "$HELPER" synchronized-upstream-port --path "$ready_file")

    "$PYTHON_BIN" "$HELPER" write-rules --path "$rules_file" --canonical-rules "$CANONICAL_RULES_FILE"
    "$PYTHON_BIN" "$HELPER" write-config --path "$config_file" \
        --listen-port "$listener_port" --upstream-port "$synchronized_upstream_port" --rules-file "$rules_file"
    if grep -Eq 'filter spoe|send-spoe|http-buffer-request|wait-for-body|res\.body' "$config_file"; then
        echo "haproxy_htx_runtime: FAIL - generated $case_name config contains a compatibility/buffering directive" >&2
        exit 1
    fi
    if ! grep -Fq 'filter modsecurity-htx rules-file' "$config_file"; then
        echo "haproxy_htx_runtime: FAIL - generated $case_name config does not select modsecurity-htx" >&2
        exit 1
    fi
    if grep -Fq '91000' "$rules_file"; then
        echo "haproxy_htx_runtime: FAIL - generated $case_name rules use temporary 91000x IDs" >&2
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

    "$PYTHON_BIN" "$HELPER" streaming-probe \
        --url "http://127.0.0.1:$listener_port/no-crs/response-body" \
        --release-path "$release_file" --first-byte-path "$client_first_byte_file" \
        --evidence-path "$client_probe_file" --timeout 10 \
        >"$case_root/streaming-client.stdout.log" \
        2>"$case_root/streaming-client.stderr.log" &
    streaming_client_pid=$!
    if ! "$PYTHON_BIN" "$HELPER" wait-file --path "$paused_file" --timeout 10 || \
        ! "$PYTHON_BIN" "$HELPER" wait-file --path "$client_first_byte_file" --timeout 10; then
        echo "haproxy_htx_runtime: FAIL - $case_name did not observe a client first byte before upstream EOS" >&2
        sed -n '1,160p' "$case_root/streaming-client.stderr.log" >&2 || true
        sed -n '1,160p' "$case_root/synchronized-upstream.stderr.log" >&2 || true
        exit 1
    fi
    if ! kill -0 "$haproxy_pid" 2>/dev/null || ! kill -0 "$streaming_client_pid" 2>/dev/null; then
        echo "haproxy_htx_runtime: FAIL - $case_name host or barrier client exited before upstream release" >&2
        sed -n '1,160p' "$log_file" >&2 || true
        sed -n '1,160p' "$case_root/streaming-client.stderr.log" >&2 || true
        exit 1
    fi
    "$PYTHON_BIN" "$HELPER" write-first-byte-evidence \
        --path "$FIRST_BYTE_EVIDENCE_PATH" --paused-path "$paused_file" \
        --client-first-byte-path "$client_first_byte_file"

    : > "$release_file"
    if ! wait "$streaming_client_pid"; then
        echo "haproxy_htx_runtime: FAIL - $case_name streaming client failed after release" >&2
        sed -n '1,160p' "$case_root/streaming-client.stderr.log" >&2 || true
        exit 1
    fi
    streaming_client_pid=
    if ! wait "$sync_upstream_pid"; then
        echo "haproxy_htx_runtime: FAIL - $case_name synchronized upstream failed after release" >&2
        sed -n '1,160p' "$case_root/synchronized-upstream.stderr.log" >&2 || true
        exit 1
    fi
    sync_upstream_pid=
    "$PYTHON_BIN" "$HELPER" validate-synchronized-upstream --path "$server_evidence_file"

    status=$("$PYTHON_BIN" "$HELPER" probe-status --path "$client_probe_file")
    if [ "$status" != "$expected_status" ]; then
        echo "haproxy_htx_runtime: FAIL - $case_name returned $status, expected $expected_status" >&2
        exit 1
    fi
    expected_log="modsecurity-htx: response-body late intervention observed; transaction_id=[A-Za-z0-9._-]+ phase=4 status=403 rule_id=$rule_id requested_action=deny resolved_policy_action=log_only host_action=log_only"
    if ! grep -Eq "$expected_log" "$log_file"; then
        echo "haproxy_htx_runtime: FAIL - $case_name lacks the expected post-EOS safe intervention" >&2
        sed -n '1,160p' "$log_file" >&2 || true
        exit 1
    fi
    cleanup_haproxy
    "$PYTHON_BIN" "$HELPER" write-host-evidence --path "$HOST_EVIDENCE_LOG_PATH" \
        --case "$case_name" --phase "$phase" --rule-id "$rule_id" --probe-path "$client_probe_file" \
        --upstream-requests 1 --host-action safe_log_only --decision-log "$log_file"
    "$PYTHON_BIN" "$HELPER" write-phase4-safe-event --path "$EVENT_LOG_PATH" \
        --decision-log "$log_file" --probe-path "$client_probe_file" \
        --first-byte-evidence "$FIRST_BYTE_EVIDENCE_PATH" --run-id "$RUN_ID" \
        --transport-case-id phase4_first_byte_before_response_end
    phase4_safe_status=$status
}

run_case allow 1 0 200 ordinary 1 forwarded
run_case phase1_403 1 1100001 403 ordinary 0 enforced_reply
run_case phase1_429 1 1100002 429 ordinary 0 enforced_reply
run_case phase2_client_deny 2 1100101 403 phase2 0-or-1 enforced_reply
run_case phase3_403 3 1100201 403 phase3 1 enforced_reply
run_phase4_safe_barrier
# Append the no-rule allow event after the Phase-4 evidence.  The canonical
# selector uses the final matching HTTP 200 event for a no-rule case, so this
# must remain last to bind P1 to its own real client/upstream transaction.
"$PYTHON_BIN" "$HELPER" write-allow-event --path "$EVENT_LOG_PATH" \
    --probe-path "$RUNTIME_ROOT/cases/allow/client-probe.json" \
    --upstream-log "$UPSTREAM_LOG" --transaction-id haproxy-htx-allow

if [ "$(wc -l < "$EVENT_LOG_PATH")" -ne 6 ]; then
    echo "haproxy_htx_runtime: FAIL - expected six host-confirmed HTX events" >&2
    exit 1
fi
if [ "$(wc -l < "$HOST_EVIDENCE_LOG_PATH")" -ne 6 ]; then
    echo "haproxy_htx_runtime: FAIL - expected six host-runtime evidence records" >&2
    exit 1
fi
if grep -Fq 'no-crs-request-body-marker' "$EVENT_LOG_PATH" || \
    grep -Fq 'no-crs-response-body-marker' "$EVENT_LOG_PATH" || \
    grep -Fq 'no-crs-request-body-marker' "$HOST_EVIDENCE_LOG_PATH" || \
    grep -Fq 'no-crs-response-body-marker' "$HOST_EVIDENCE_LOG_PATH"; then
    echo "haproxy_htx_runtime: FAIL - host evidence contains a body payload sentinel" >&2
    exit 1
fi

{
    printf 'status=PASS\n'
    printf 'integration_mode=native-htx-filter\n'
    printf 'evaluation_mode=native_host_runtime_nonpromoted\n'
    printf 'rule_evaluation=libmodsecurity_host_runtime\n'
    printf 'common_runtime_bridge=false\n'
    printf 'runtime_verified=true\n'
    printf 'requests_sent=true\n'
    printf 'allowed_request_status=200\n'
    printf 'blocked_request_status=403\n'
    printf 'modsecurity_rule_id=1100001\n'
    printf 'precommit_enforcement=true\n'
    printf 'phase1_deny_client_status=403\n'
    printf 'phase1_alternative_status_client_status=429\n'
    printf 'phase3_deny_client_status=403\n'
    printf 'phase2_deny_status=403\n'
    printf 'phase2_client_status=403\n'
    printf 'phase2_upstream_request_count=%s\n' "$phase2_upstream_request_count"
    printf 'phase2_request_dispatch_observed=%s\n' "$phase2_request_dispatch_observed"
    printf 'phase2_incremental_forwarding_claimed=false\n'
    printf 'phase4_safe_status=%s\n' "$phase4_safe_status"
    printf 'phase4_end_of_stream_evaluation_status=%s\n' "$phase4_safe_status"
    printf 'phase4_first_byte_before_response_end_status=%s\n' "$phase4_safe_status"
    printf 'phase4_no_full_response_buffering_status=%s\n' "$phase4_safe_status"
    printf 'phase2_host_action=%s\n' "$phase2_host_action"
    printf 'phase4_safe_host_action=log_only\n'
    printf 'response_body_stream_observed=true\n'
    printf 'transaction_id_observed=true\n'
    printf 'payload_recorded=false\n'
    printf 'capability_promotion=not_permitted\n'
    printf 'canonical_rules_file=%s\n' "$CANONICAL_RULES_FILE"
    printf 'overlay_build_provenance=%s\n' "$BUILD_PROVENANCE"
    printf 'event_log=%s\n' "$EVENT_LOG_PATH"
    printf 'host_evidence_log=%s\n' "$HOST_EVIDENCE_LOG_PATH"
    printf 'first_byte_evidence_path=%s\n' "$FIRST_BYTE_EVIDENCE_PATH"
    printf 'first_byte_before_response_end=true\n'
    printf 'no_full_response_buffering=true\n'
    printf 'haproxy_version=%s\n' "$VERSION_FILE"
    printf 'production_ready=false\n'
} > "$SUMMARY"

cleanup
upstream_pid=
trap - EXIT HUP INT TERM
printf 'processes_stopped=yes\n' >> "$SUMMARY"
printf 'haproxy_htx_runtime: pass (real-host precommit evidence, non-promoted) summary=%s\n' "$SUMMARY"
