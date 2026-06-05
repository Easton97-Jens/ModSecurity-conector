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
HAPROXY_CFG_EXAMPLE="$CONNECTOR_DIR/poc/spoe/haproxy.cfg.example"
SPOE_AGENT_CFG_EXAMPLE="$CONNECTOR_DIR/poc/spoe/spoe-agent.conf.example"
NOTE="Build/self-test starter evidence is available via make connector-starter-checks but is not runtime smoke evidence."
PREPARE_STATUS=not-run
PREPARE_REASON=

blocked_root() {
    echo "$CONNECTOR_NAME runtime smoke: BLOCKED - $*" >&2
    exit 77
}

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
    require_build_path "$HAPROXY_BIN" HAPROXY_BIN
    require_not_connector_artifact "$RESULTS_DIR" RESULTS_DIR
    require_not_connector_artifact "$TMP_ROOT" TMP_ROOT
    require_not_connector_artifact "$LOG_ROOT" LOG_ROOT
    require_not_connector_artifact "$HAPROXY_BIN" HAPROXY_BIN
    mkdir -p "$RESULTS_DIR" "$TMP_ROOT" "$LOG_DIR"
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

detect_spoe_config() {
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
    spoe_config_status=$(detect_spoe_config)
    modsecurity_binding_status=$(detect_modsecurity_binding)
    {
        echo "BLOCKED haproxy runtime prerequisites missing"
        echo "local_haproxy_bin=${local_haproxy_bin:-missing}"
        echo "system_haproxy_bin=${system_haproxy_bin:-missing}"
        echo "prepare_status=$PREPARE_STATUS"
        echo "prepare_reason=$PREPARE_REASON"
        echo "common_acquisition_status=$common_acquisition_status"
        echo "spoa_starter_status=$spoa_starter_status"
        echo "spoe_config_status=$spoe_config_status"
        echo "modsecurity_binding_status=$modsecurity_binding_status"
    } > "$status_log"
    "$PYTHON_BIN" - "$results_jsonl" "$summary_json" "$summary_text" \
        "$CONNECTOR_NAME" "$HARNESS_PATH" "$CONNECTOR_ROOT" "$SOURCE_ROOT" \
        "$BUILD_ROOT" "$RESULTS_DIR" "$TMP_ROOT" "$LOG_ROOT" "$LOG_DIR" \
        "$starter_checks_available" "$NOTE" "$local_haproxy_bin" "$system_haproxy_bin" \
        "$PREPARE_STATUS" "$PREPARE_REASON" "$PREPARE_HAPROXY_RUNTIME" \
        "$common_acquisition_status" "$spoa_starter_status" \
        "$spoe_config_status" "$modsecurity_binding_status" "$SPOA_STARTER_BIN" \
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
    spoe_config_status,
    modsecurity_binding_status,
    spoa_starter_bin,
    haproxy_cfg_example,
    spoe_agent_cfg_example,
) = sys.argv[1:]

now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
starter_checks_available = starter_checks_available_text == "true"
blocked_reasons = []
if not local_haproxy_bin:
    blocked_reasons.append("haproxy binary missing")
    if prepare_status in {"blocked", "failed", "missing-helper"}:
        blocked_reasons.append(f"haproxy local build blocked: {prepare_reason}")
if common_acquisition_status != "defined":
    blocked_reasons.append("haproxy source/binary acquisition is not defined in common.sh")
if spoa_starter_status != "runnable":
    blocked_reasons.append("spoa agent runtime missing")
if spoe_config_status != "runnable":
    blocked_reasons.append("spoe config missing")
if modsecurity_binding_status != "present":
    blocked_reasons.append("modsecurity binding missing")
diagnostics = {
    "haproxy_binary": "present" if local_haproxy_bin else "missing",
    "haproxy_binary_path": local_haproxy_bin or None,
    "system_haproxy_binary": system_haproxy_bin or None,
    "prepare_status": prepare_status,
    "prepare_reason": prepare_reason,
    "prepare_helper": prepare_helper,
    "common_acquisition_status": common_acquisition_status,
    "spoa_starter_binary": spoa_starter_bin,
    "spoa_starter_status": spoa_starter_status,
    "spoe_config_status": spoe_config_status,
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
    "reason": "haproxy runtime prerequisites missing",
    "blocked_reasons": blocked_reasons,
    "diagnostics": diagnostics,
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
    "status": "BLOCKED",
    "counts": {"PASS": 0, "FAIL": 0, "BLOCKED": 1, "NOT_RUN": 0},
    "runtime_verified": False,
    "runtime_status": "blocked",
    "response_body_verified": False,
    "reason": "haproxy runtime prerequisites missing",
    "blocked_reasons": blocked_reasons,
    "diagnostics": diagnostics,
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
    handle.write("BLOCKED runtime-smoke-entrypoint haproxy runtime prerequisites missing\n")
    for item in blocked_reasons:
        handle.write(f"- {item}\n")
    handle.write("Runtime not verified\n")
    handle.write(f"{note}\n")
PY
}

validate_roots
ensure_local_haproxy
write_blocked_evidence
echo "$CONNECTOR_NAME runtime smoke: BLOCKED - haproxy runtime prerequisites missing"
echo "Runtime not verified"
exit 77
