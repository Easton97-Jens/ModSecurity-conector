#!/bin/sh
set -eu

CONNECTOR_NAME=haproxy
SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd "$SCRIPT_DIR/../../.." && pwd)
FRAMEWORK_ROOT="${FRAMEWORK_ROOT:-$REPO_ROOT/modules/ModSecurity-test-Framework}"
[ -d "$FRAMEWORK_ROOT" ] || { echo "haproxy_smoke: blocked FRAMEWORK_ROOT is missing; run git submodule update --init --recursive or set FRAMEWORK_ROOT=/path/to/ModSecurity-test-Framework"; exit 77; }

SOURCE_ROOT="${SOURCE_ROOT:-/src}"
BUILD_ROOT="${BUILD_ROOT:-/src/ModSecurity-conector-build}"
if [ "${FORCE_ALL_CASES:-0}" = "1" ] && [ -z "${RESULTS_DIR+x}" ]; then
    RESULTS_DIR="$BUILD_ROOT/results/force-all"
else
    RESULTS_DIR="${RESULTS_DIR:-$BUILD_ROOT/results}"
fi
TMP_ROOT="${TMP_ROOT:-$BUILD_ROOT/tmp}"
LOG_ROOT="${LOG_ROOT:-$BUILD_ROOT/logs}"
LOG_DIR="${LOG_DIR:-$LOG_ROOT/haproxy-runtime}"
RUNTIME_BASE="${RUNTIME_BASE:-$BUILD_ROOT/haproxy-runtime-cases}"
RUNTIME_ROOT="${RUNTIME_ROOT:-}"
HAPROXY_BIN="${HAPROXY_BIN:-$BUILD_ROOT/haproxy-runtime/haproxy/sbin/haproxy}"
SPOA_RUNTIME_BIN="${SPOA_RUNTIME_BIN:-$BUILD_ROOT/haproxy-spoa-runtime/haproxy-modsecurity-spoa}"
MODSECURITY_BINDING_DIR="${MODSECURITY_BINDING_DIR:-$BUILD_ROOT/haproxy-modsecurity-binding}"
PREPARE_HAPROXY_RUNTIME="$FRAMEWORK_ROOT/ci/prepare-haproxy-runtime.sh"
CASE_CLI="$FRAMEWORK_ROOT/tests/runners/case_cli.py"
CURL_BIN="${CURL:-}"
PYTHON_BIN="${PYTHON:-python3}"
PYTHONDONTWRITEBYTECODE="${PYTHONDONTWRITEBYTECODE:-1}"
export PYTHONDONTWRITEBYTECODE
BASE_PORT="${PORT:-18082}"
PORT="$BASE_PORT"
PORT_SEARCH_LIMIT="${PORT_SEARCH_LIMIT:-100}"
PORT_RETRY_LIMIT="${PORT_RETRY_LIMIT:-1}"
HAPROXY_SPOA_PORT_OFFSET="${HAPROXY_SPOA_PORT_OFFSET:-12000}"
HAPROXY_BACKEND_PORT_OFFSET="${HAPROXY_BACKEND_PORT_OFFSET:-24000}"
TEST_CASE="${TEST_CASE:-}"
SMOKE_CASES="${SMOKE_CASES:-}"
CASE_SCOPE="${CASE_SCOPE:-all}"
RUN_ONE_CASE="${RUN_ONE_CASE:-0}"
STATUS_FILE="$LOG_DIR/status.txt"
MODSECURITY_TEST_VARIANT="${MODSECURITY_TEST_VARIANT:-no-crs}"
MODSECURITY_RULE_PREAMBLE_FILE="${MODSECURITY_RULE_PREAMBLE_FILE:-}"
export MODSECURITY_TEST_VARIANT

CONNECTOR_ORIGIN_SOURCE="${CONNECTOR_ORIGIN_SOURCE:-}"
CONNECTOR_ORIGIN_SOURCE_REPO="${CONNECTOR_ORIGIN_SOURCE_REPO:-}"
CONNECTOR_ORIGIN_SOURCE_URL="${CONNECTOR_ORIGIN_SOURCE_URL:-}"
CONNECTOR_ORIGIN_SOURCE_COMMIT="${CONNECTOR_ORIGIN_SOURCE_COMMIT:-}"
CONNECTOR_ORIGIN_SOURCE_VERSION="${CONNECTOR_ORIGIN_SOURCE_VERSION:-}"
CONNECTOR_ORIGIN_LICENSE="${CONNECTOR_ORIGIN_LICENSE:-}"
CONNECTOR_ORIGIN_IMPORTED_PATH="${CONNECTOR_ORIGIN_IMPORTED_PATH:-}"

load_connector_adapter_metadata() {
    metadata_shell=$(CONNECTOR_ROOT="$REPO_ROOT" "$PYTHON_BIN" "$FRAMEWORK_ROOT/ci/adapter_metadata.py" shell haproxy --prefix CONNECTOR_ADAPTER 2>/dev/null || true)
    [ -n "$metadata_shell" ] || return 0
    eval "$metadata_shell"
    CONNECTOR_ORIGIN_SOURCE="${CONNECTOR_ORIGIN_SOURCE:-$CONNECTOR_ADAPTER_SOURCE}"
    CONNECTOR_ORIGIN_SOURCE_REPO="${CONNECTOR_ORIGIN_SOURCE_REPO:-$CONNECTOR_ADAPTER_SOURCE_REPO}"
    CONNECTOR_ORIGIN_SOURCE_URL="${CONNECTOR_ORIGIN_SOURCE_URL:-$CONNECTOR_ADAPTER_SOURCE_URL}"
    CONNECTOR_ORIGIN_SOURCE_COMMIT="${CONNECTOR_ORIGIN_SOURCE_COMMIT:-$CONNECTOR_ADAPTER_SOURCE_COMMIT}"
    CONNECTOR_ORIGIN_SOURCE_VERSION="${CONNECTOR_ORIGIN_SOURCE_VERSION:-$CONNECTOR_ADAPTER_SOURCE_VERSION}"
    CONNECTOR_ORIGIN_LICENSE="${CONNECTOR_ORIGIN_LICENSE:-$CONNECTOR_ADAPTER_LICENSE}"
    CONNECTOR_ORIGIN_IMPORTED_PATH="${CONNECTOR_ORIGIN_IMPORTED_PATH:-$CONNECTOR_ADAPTER_IMPORTED_PATH}"
}

blocked() {
    echo "haproxy_smoke: blocked $*"
    mkdir -p "$LOG_DIR"
    echo "blocked: $*" >> "$STATUS_FILE"
    exit 77
}

fail() {
    echo "haproxy_smoke: fail $*"
    mkdir -p "$LOG_DIR"
    echo "fail: $*" >> "$STATUS_FILE"
    exit 1
}

require_absolute() {
    path=$1
    label=$2
    case "$path" in
        /*) ;;
        *) blocked "$label must be absolute: $path" ;;
    esac
}

require_under_source_root() {
    path=$1
    label=$2
    require_absolute "$path" "$label"
    case "$path" in
        /src|/src/*) ;;
        *) blocked "$label must be under /src: $path" ;;
    esac
}

require_under_runtime_root() {
    path=$1
    label=$2
    state_root="${XDG_STATE_HOME:-${HOME:-}/.local/state}"

    require_absolute "$path" "$label"
    case "$path" in
        /src|/src/*|/tmp|/tmp/*) return 0 ;;
    esac
    if [ -n "$state_root" ]; then
        case "$path" in
            "$state_root"|"$state_root"/*) return 0 ;;
        esac
    fi
    blocked "$label must be under /src, /tmp, or XDG state home: $path"
}

require_under_build_root() {
    path=$1
    label=$2
    require_absolute "$path" "$label"
    case "$path" in
        "$BUILD_ROOT"|"$BUILD_ROOT"/*) ;;
        *) blocked "$label must stay under BUILD_ROOT: $path" ;;
    esac
}

require_generated_roots() {
    require_under_source_root "$SOURCE_ROOT" SOURCE_ROOT
    require_under_runtime_root "$BUILD_ROOT" BUILD_ROOT
    require_under_build_root "$RESULTS_DIR" RESULTS_DIR
    require_under_build_root "$TMP_ROOT" TMP_ROOT
    require_under_build_root "$LOG_ROOT" LOG_ROOT
    require_under_build_root "$LOG_DIR" LOG_DIR
    require_under_build_root "$RUNTIME_BASE" RUNTIME_BASE
    [ -f "$CASE_CLI" ] || blocked "shared case CLI missing: $CASE_CLI"
}

find_curl() {
    if [ -n "$CURL_BIN" ]; then
        printf '%s\n' "$CURL_BIN"
        return 0
    fi
    command -v curl 2>/dev/null || true
}

resolve_case_path() {
    item=$1
    "$PYTHON_BIN" "$CASE_CLI" list-cases \
        --repo-root "$REPO_ROOT" \
        --framework-root "$FRAMEWORK_ROOT" \
        --connector-root "$REPO_ROOT" \
        --connector haproxy \
        --scope "$CASE_SCOPE" \
        --test-case "$item"
}

list_case_files() {
    if [ -n "$TEST_CASE" ]; then
        "$PYTHON_BIN" "$CASE_CLI" list-cases \
            --repo-root "$REPO_ROOT" \
            --framework-root "$FRAMEWORK_ROOT" \
            --connector-root "$REPO_ROOT" \
            --connector haproxy \
            --scope "$CASE_SCOPE" \
            --test-case "$TEST_CASE"
        return
    fi
    if [ -n "$SMOKE_CASES" ]; then
        "$PYTHON_BIN" "$CASE_CLI" list-cases \
            --repo-root "$REPO_ROOT" \
            --framework-root "$FRAMEWORK_ROOT" \
            --connector-root "$REPO_ROOT" \
            --connector haproxy \
            --scope "$CASE_SCOPE" \
            --smoke-cases "$SMOKE_CASES"
        return
    fi
    "$PYTHON_BIN" "$CASE_CLI" list-cases \
        --repo-root "$REPO_ROOT" \
        --framework-root "$FRAMEWORK_ROOT" \
        --connector-root "$REPO_ROOT" \
        --connector haproxy \
        --scope "$CASE_SCOPE"
}

write_case_result() {
    case_path=$1
    case_status=$2
    actual_status=${3:-}
    output=$4
    if [ -n "$actual_status" ]; then
        "$PYTHON_BIN" "$CASE_CLI" case-info \
            --case "$case_path" \
            --connector haproxy \
            --status "$case_status" \
            --actual-status "$actual_status" \
            --output "$output"
    else
        "$PYTHON_BIN" "$CASE_CLI" case-info \
            --case "$case_path" \
            --connector haproxy \
            --status "$case_status" \
            --output "$output"
    fi
    enrich_case_result "$output" || true
}

enrich_case_result() {
    output=$1
    "$PYTHON_BIN" - "$output" <<'PY'
import json
import sys
from pathlib import Path

result_path = Path(sys.argv[1])
if not result_path.exists():
    raise SystemExit(0)
case_dir = result_path.parent
decision_path = case_dir / "decision.jsonl"
entries = []
if decision_path.exists():
    for line in decision_path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            entries.append(json.loads(line))
        except Exception:
            pass
data = json.loads(result_path.read_text(encoding="utf-8"))
data["case"] = data.get("case") or data.get("name")
data["decision_log"] = str(decision_path)
data["decision_log_path"] = str(decision_path)
data["haproxy_log_path"] = str(case_dir / "haproxy.stderr.log")
data["spoa_log_path"] = str(case_dir / "spoa-agent.log")
data["evidence_path"] = str(result_path)
for audit_candidate in (
    case_dir / "audit.log",
    case_dir / "modsec_audit.log",
    case_dir / "audit" / "audit.log",
):
    if audit_candidate.exists():
        data["audit_log_path"] = str(audit_candidate)
        break
data["evidence"] = (
    f"decision_log={decision_path}; haproxy_log={case_dir / 'haproxy.stderr.log'}; "
    f"spoa_log={case_dir / 'spoa-agent.log'}"
)
if entries:
    last = entries[-1]
    data.setdefault("reason", last.get("reason", ""))
    data["modsecurity_processed"] = any(bool(item.get("modsecurity_processed")) for item in entries)
    data["request_headers_seen"] = any(bool(item.get("request_headers_seen")) for item in entries)
    data["request_body_seen"] = any(bool(item.get("request_body_seen")) for item in entries)
    data["response_headers_seen"] = any(bool(item.get("response_headers_seen")) for item in entries)
    data["response_body_seen"] = any(bool(item.get("response_body_seen")) for item in entries)
    data["decision_entries"] = len(entries)
result_path.write_text(json.dumps(data, sort_keys=True) + "\n", encoding="utf-8")
PY
}

enrich_summary_metadata() {
    summary_json=$1
    results_jsonl=$2
    exit_status=$3
    command_label=$4
    "$PYTHON_BIN" - "$summary_json" "$results_jsonl" "$RESULTS_DIR" "$LOG_DIR" "$exit_status" "$command_label" <<'PY'
import json
import os
import sys
from pathlib import Path

summary_path = Path(sys.argv[1])
jsonl_path = Path(sys.argv[2])
results_dir = Path(sys.argv[3])
case_result_root = Path(sys.argv[4])
exit_status = int(sys.argv[5])
command_label = sys.argv[6]

if not summary_path.exists():
    raise SystemExit(0)

data = json.loads(summary_path.read_text(encoding="utf-8"))
connector = data.setdefault("haproxy", {})
summary = connector.setdefault("summary", {})
cases = connector.setdefault("cases", {})
runtime_mode = "force-all" if os.environ.get("FORCE_ALL_CASES") == "1" else "default"

attempted_statuses = ("pass", "fail", "blocked", "not_executable")
attempted = sum(int(summary.get(status, 0) or 0) for status in attempted_statuses)
connector["runtime_mode"] = runtime_mode
connector["attempted"] = attempted
connector["total_cases"] = len(cases)
connector["evidence_root"] = str(results_dir)
connector["jsonl_path"] = str(jsonl_path)
connector["per_case_result_root"] = str(case_result_root)
connector["command"] = command_label
connector["exit_status"] = exit_status
connector["failed_due_to_live_mismatches"] = bool(int(summary.get("fail", 0) or 0) > 0 and exit_status != 0)

for name, row in cases.items():
    if not isinstance(row, dict):
        continue
    row.setdefault("case", name)
    row.setdefault("expected", row.get("expected_status"))
    row.setdefault("observed", row.get("actual_status"))
    row.setdefault("decision_log_path", row.get("decision_log"))
    if not row.get("evidence_path"):
        log_path = row.get("spoa_log_path") or row.get("haproxy_log_path") or row.get("decision_log_path")
        if log_path:
            row["evidence_path"] = str(Path(log_path).parent / "result.json")
    if not row.get("audit_log_path") and row.get("evidence_path"):
        case_dir = Path(row["evidence_path"]).parent
        for audit_candidate in (
            case_dir / "audit.log",
            case_dir / "modsec_audit.log",
            case_dir / "audit" / "audit.log",
        ):
            if audit_candidate.exists():
                row["audit_log_path"] = str(audit_candidate)
                break
    if not row.get("reason") and row.get("status") == "fail":
        expected = row.get("expected_status", row.get("expected"))
        observed = row.get("actual_status", row.get("observed"))
        if expected not in (None, "") or observed not in (None, ""):
            row["reason"] = f"expected HTTP {expected}; observed HTTP {observed}"
    row.setdefault("live_executed", row.get("status") in ("pass", "fail", "blocked"))

summary_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY
}

case_runtime_shape() {
    "$PYTHON_BIN" - "$FRAMEWORK_ROOT" "$TEST_CASE" <<'PY'
import os
import sys
from pathlib import Path

framework = Path(sys.argv[1])
case_path = sys.argv[2]
sys.path.insert(0, str(framework / "tests" / "runners"))
from runner_core import effective_expect, load_case  # noqa: E402

case = load_case(case_path)
caps = {str(value).replace("_", "-") for value in (case.get("capabilities", []) or [])}
if isinstance(case.get("capabilities"), dict):
    caps = {str(key).replace("_", "-") for key, value in case["capabilities"].items() if value}
expect = effective_expect(case)
intervention = str(expect.get("intervention", ""))
status = int(expect.get("status", 0))
response_headers = bool(caps.intersection({"phase3", "phase4", "response-headers", "response-body"}))
response_body = bool(caps.intersection({"phase4", "response-body"}))
print(f"HAPROXY_ENABLE_RESPONSE_HEADERS={1 if response_headers else 0}")
print(f"HAPROXY_ENABLE_RESPONSE_BODY={1 if response_body else 0}")
print(f"HAPROXY_EXPECT_INTERVENTION={intervention!r}")
print(f"HAPROXY_EXPECT_STATUS={status}")
print("HAPROXY_NOT_EXECUTABLE_REASON=''")
PY
}

mark_not_executable() {
    reason=$1
    write_case_result "$TEST_CASE" not_executable "" "$LOG_DIR/result.json" || true
    "$PYTHON_BIN" - "$LOG_DIR/result.json" "$reason" <<'PY' || true
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
reason = sys.argv[2]
if path.exists():
    data = json.loads(path.read_text(encoding="utf-8"))
    data["reason"] = reason
    path.write_text(json.dumps(data, sort_keys=True) + "\n", encoding="utf-8")
PY
    echo "haproxy_smoke: not_executable $reason"
    exit 0
}

rule_parse_startup_is_not_executable() {
    [ -f "$LOG_DIR/spoa-runtime.stderr.log" ] || return 1
    grep -q "failed to initialize ModSecurity engine: Rules error" "$LOG_DIR/spoa-runtime.stderr.log"
}

run_all_cases() {
    require_generated_roots
    load_connector_adapter_metadata
    mkdir -p "$LOG_DIR" "$RESULTS_DIR" "$RUNTIME_BASE"
    summary_file="$RESULTS_DIR/haproxy-summary.txt"
    json_file="$RESULTS_DIR/haproxy-summary.json"
    results_jsonl="$RESULTS_DIR/haproxy-results.jsonl"
    connector_summary="$RESULTS_DIR/connector-summary.txt"
    : > "$summary_file"
    : > "$results_jsonl"

    cases=$(list_case_files) || exit 1
    if [ -z "$cases" ]; then
        echo "haproxy_smoke: fail no shared smoke cases found" >&2
        exit 1
    fi

    any_fail=0
    any_blocked=0
    any_pass=0
    index=0
    for case_path in $cases; do
        case_name=$(basename "$case_path" .yaml)
        case_log_dir="$LOG_DIR/$case_name"
        case_runtime="$RUNTIME_BASE/$case_name"
        case_port=$((BASE_PORT + index))
        echo "haproxy_smoke: running case=$case_name port=$case_port"
        set +e
        RUN_ONE_CASE=1 \
            TEST_CASE="$case_path" \
            LOG_DIR="$case_log_dir" \
            RUNTIME_ROOT="$case_runtime" \
            PORT="$case_port" \
            FRAMEWORK_ROOT="$FRAMEWORK_ROOT" \
            MODSECURITY_TEST_VARIANT="$MODSECURITY_TEST_VARIANT" \
            MODSECURITY_RULE_PREAMBLE_FILE="$MODSECURITY_RULE_PREAMBLE_FILE" \
            sh "$0"
        rc=$?
        set -e
        case_status=pass
        case_status_upper=PASS
        if [ "$rc" -eq 77 ]; then
            case_status=blocked
            case_status_upper=BLOCKED
            any_blocked=1
        elif [ "$rc" -ne 0 ]; then
            case_status=fail
            case_status_upper=FAIL
            any_fail=1
        else
            any_pass=1
        fi
        if [ -f "$case_log_dir/result.json" ]; then
            existing_status=$("$PYTHON_BIN" - "$case_log_dir/result.json" <<'PY' || true
import json
import sys
try:
    print(json.load(open(sys.argv[1], encoding="utf-8")).get("status", ""))
except Exception:
    print("")
PY
)
            if [ "$existing_status" = "not_executable" ]; then
                case_status=not_executable
                case_status_upper=NOT_EXECUTABLE
            fi
        fi
        actual_status=""
        if [ -f "$case_log_dir/observed-status.txt" ]; then
            actual_status=$(cat "$case_log_dir/observed-status.txt")
        fi
        write_case_result "$case_path" "$case_status" "$actual_status" "$case_log_dir/result.json" || true
        if [ -f "$case_log_dir/result.json" ]; then
            cat "$case_log_dir/result.json" >> "$results_jsonl"
        fi
        echo "$case_status_upper $case_name" | tee -a "$summary_file"
        index=$((index + 1))
    done

    if [ -f "$MODSECURITY_BINDING_DIR/paths.env" ]; then
        . "$MODSECURITY_BINDING_DIR/paths.env"
    fi
    "$PYTHON_BIN" "$CASE_CLI" summarize-results \
        --connector haproxy \
        --input-jsonl "$results_jsonl" \
        --summary-json "$json_file" \
        --summary-text "$summary_file" \
        --import-status-file "$REPO_ROOT/config/testing/import-status.json" \
        --connector-path real-world \
        --validation-mode real-world-connector-path \
        --server haproxy \
        --server-binary "$HAPROXY_BIN" \
        --module "$SPOA_RUNTIME_BIN" \
        --libmodsecurity "${MODSECURITY_LIB_DIR:-}" \
        --origin-source "$CONNECTOR_ORIGIN_SOURCE" \
        --origin-source-repo "$CONNECTOR_ORIGIN_SOURCE_REPO" \
        --origin-source-url "$CONNECTOR_ORIGIN_SOURCE_URL" \
        --origin-source-commit "$CONNECTOR_ORIGIN_SOURCE_COMMIT" \
        --origin-source-version "$CONNECTOR_ORIGIN_SOURCE_VERSION" \
        --origin-license "$CONNECTOR_ORIGIN_LICENSE" \
        --origin-imported-path "$CONNECTOR_ORIGIN_IMPORTED_PATH"
    cp "$summary_file" "$connector_summary"

    planned_exit_status=0
    if [ "$any_fail" -ne 0 ]; then
        planned_exit_status=1
    elif [ "$any_pass" -eq 0 ] && [ "$any_blocked" -ne 0 ]; then
        planned_exit_status=77
    fi
    command_label="make smoke-haproxy"
    if [ "${FORCE_ALL_CASES:-0}" = "1" ]; then
        command_label="FORCE_ALL_CASES=1 make smoke-haproxy"
    fi
    enrich_summary_metadata "$json_file" "$results_jsonl" "$planned_exit_status" "$command_label" || true
    exit "$planned_exit_status"
}

pick_tcp_port() {
    "$PYTHON_BIN" - <<'PY'
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind(("127.0.0.1", 0))
    print(sock.getsockname()[1])
PY
}

select_offset_port() {
    base_port=$1
    offset=$2
    search_limit=$3
    start_port=$((base_port + offset))
    if [ "$start_port" -gt 65000 ]; then
        pick_tcp_port
        return
    fi
    select_free_port "$start_port" "$search_limit"
}

port_is_free() {
    port_to_probe=$1
    "$PYTHON_BIN" - "$port_to_probe" <<'PY'
import socket
import sys

port = int(sys.argv[1])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.bind(("127.0.0.1", port))
except OSError:
    raise SystemExit(1)
finally:
    sock.close()
PY
}

select_free_port() {
    start_port=$1
    search_limit=$2
    offset=0
    while [ "$offset" -lt "$search_limit" ]; do
        candidate=$((start_port + offset))
        if port_is_free "$candidate"; then
            printf '%s\n' "$candidate"
            return 0
        fi
        offset=$((offset + 1))
    done
    return 1
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

ensure_local_haproxy() {
    if [ -x "$HAPROXY_BIN" ]; then
        return 0
    fi
    if [ "${RUNTIME_COMPONENTS_PREPARED_ONLY:-0}" = "1" ]; then
        blocked "prepared HAProxy binary missing: $HAPROXY_BIN"
    fi
    [ -x "$PREPARE_HAPROXY_RUNTIME" ] || blocked "prepare-haproxy-runtime helper missing"
    SOURCE_ROOT="$SOURCE_ROOT" \
        BUILD_ROOT="$BUILD_ROOT" \
        TMP_ROOT="$TMP_ROOT" \
        LOG_ROOT="$LOG_ROOT" \
        CONNECTOR_ROOT="$REPO_ROOT" \
        FRAMEWORK_ROOT="$FRAMEWORK_ROOT" \
        sh "$PREPARE_HAPROXY_RUNTIME" >"$LOG_DIR/prepare-haproxy-runtime.log" 2>&1 || \
        blocked "prepare-haproxy-runtime failed; see $LOG_DIR/prepare-haproxy-runtime.log"
    [ -x "$HAPROXY_BIN" ] || blocked "local HAProxy binary missing after prepare: $HAPROXY_BIN"
}

ensure_spoa_runtime() {
    if [ -x "$SPOA_RUNTIME_BIN" ] && [ -f "$MODSECURITY_BINDING_DIR/paths.env" ]; then
        . "$MODSECURITY_BINDING_DIR/paths.env"
        export MODSECURITY_INCLUDE_DIR MODSECURITY_LIB_DIR
        [ -n "${MODSECURITY_LIB_DIR:-}" ] || blocked "ModSecurity library directory missing from paths.env"
        return 0
    fi
    if [ "${RUNTIME_COMPONENTS_PREPARED_ONLY:-0}" = "1" ]; then
        blocked "prepared HAProxy ModSecurity binding/SPOA runtime missing: $SPOA_RUNTIME_BIN"
    fi
    BUILD_ROOT="$BUILD_ROOT" \
        TMP_ROOT="$TMP_ROOT" \
        LOG_ROOT="$LOG_ROOT" \
        REPO_ROOT="$REPO_ROOT" \
        make -C "$REPO_ROOT/connectors/haproxy" build-modsecurity-binding build-spoa-runtime >"$LOG_DIR/haproxy-build.log" 2>&1 || \
        blocked "HAProxy ModSecurity binding/SPOA runtime build failed; see $LOG_DIR/haproxy-build.log"
    [ -x "$SPOA_RUNTIME_BIN" ] || blocked "SPOA runtime missing after build: $SPOA_RUNTIME_BIN"
    [ -f "$MODSECURITY_BINDING_DIR/paths.env" ] || blocked "ModSecurity binding paths missing: $MODSECURITY_BINDING_DIR/paths.env"
    . "$MODSECURITY_BINDING_DIR/paths.env"
    export MODSECURITY_INCLUDE_DIR MODSECURITY_LIB_DIR
    [ -n "${MODSECURITY_LIB_DIR:-}" ] || blocked "ModSecurity library directory missing from paths.env"
}

cleanup() {
    if [ -n "${HAPROXY_PID:-}" ] && kill -0 "$HAPROXY_PID" >/dev/null 2>&1; then
        kill "$HAPROXY_PID" >/dev/null 2>&1 || true
        wait "$HAPROXY_PID" >/dev/null 2>&1 || true
    fi
    if [ -n "${AGENT_PID:-}" ] && kill -0 "$AGENT_PID" >/dev/null 2>&1; then
        kill "$AGENT_PID" >/dev/null 2>&1 || true
        wait "$AGENT_PID" >/dev/null 2>&1 || true
    fi
    if [ -n "${BACKEND_PID:-}" ] && kill -0 "$BACKEND_PID" >/dev/null 2>&1; then
        kill "$BACKEND_PID" >/dev/null 2>&1 || true
        wait "$BACKEND_PID" >/dev/null 2>&1 || true
    fi
}

write_haproxy_config() {
    mkdir -p "$RUNTIME_ROOT/conf"
    {
        echo "global"
        echo "    log stdout format raw local0"
        echo "    tune.bufsize 65536"
        echo "    pidfile $RUNTIME_ROOT/haproxy.pid"
        echo
        echo "defaults"
        echo "    mode http"
        echo "    timeout connect 1s"
        echo "    timeout client 5s"
        echo "    timeout server 5s"
        echo
        echo "frontend fe_haproxy_modsecurity"
        echo "    bind 127.0.0.1:$PORT"
        echo "    unique-id-format %[uuid()]"
        echo "    unique-id-header X-Request-ID"
        echo "    option http-buffer-request"
        if [ "${HAPROXY_ENABLE_RESPONSE_BODY:-0}" = "1" ]; then
            echo "    http-response wait-for-body time 50ms at-least 1"
        fi
        echo "    filter spoe engine modsecurity config $SPOE_CFG"
        echo "    http-request send-spoe-group modsecurity request-check"
        echo "    http-request redirect location %[var(txn.modsec.redirect_url)] code 302 if { var(txn.modsec.action) -m str redirect } { var(txn.modsec.redirect_url) -m found }"
        echo "    http-request silent-drop if { var(txn.modsec.action) -m str drop }"
        echo "    http-request deny status 401 if { var(txn.modsec.status) -m int 401 }"
        echo "    http-request deny status 403 if { var(txn.modsec.blocked) -m bool }"
        echo "    http-request deny status 406 if { var(txn.modsec.status) -m int 406 }"
        echo "    http-request deny status 429 if { var(txn.modsec.status) -m int 429 }"
        echo "    http-request deny status 503 if { var(txn.modsec.status) -m int 503 }"
        if [ "${HAPROXY_ENABLE_RESPONSE_HEADERS:-0}" = "1" ]; then
            echo "    http-response set-header Last-Modified \"Wed, 21 Oct 2015 07:28:00 GMT\""
            echo "    http-response set-header Content-Type \"text/html; charset=utf-8\""
            echo "    http-response set-header Location \"/encoded%%2Ftarget\""
            echo "    http-response add-header Set-Cookie \"session=token\""
            echo "    http-response add-header Set-Cookie \"a=b\""
            echo "    http-response send-spoe-group modsecurity response-check"
            echo "    http-response silent-drop if { var(txn.modsec.action) -m str drop }"
            echo "    http-response deny status 401 if { var(txn.modsec.status) -m int 401 }"
            echo "    http-response deny status 403 if { var(txn.modsec.blocked) -m bool }"
            echo "    http-response deny status 406 if { var(txn.modsec.status) -m int 406 }"
            echo "    http-response deny status 429 if { var(txn.modsec.status) -m int 429 }"
            echo "    http-response deny status 503 if { var(txn.modsec.status) -m int 503 }"
        fi
        echo "    default_backend be_haproxy_smoke_app"
        echo
        echo "backend be_haproxy_smoke_app"
        echo "    mode http"
        echo "    server app1 127.0.0.1:$BACKEND_PORT"
        echo
        echo "backend be_spoa_modsecurity"
        echo "    mode spop"
        echo "    balance roundrobin"
        echo "    timeout connect 1s"
        echo "    timeout server 3s"
        echo "    server spoa1 127.0.0.1:$SPOA_PORT"
    } > "$HAPROXY_CFG"
    {
        echo "[modsecurity]"
        echo
        echo "spoe-agent modsecurity-agent"
        if [ "${HAPROXY_ENABLE_RESPONSE_HEADERS:-0}" = "1" ]; then
            echo "    groups request-check response-check"
        else
            echo "    groups request-check"
        fi
        echo "    option var-prefix modsec"
        echo "    register-var-names blocked action status redirect_url rule_id phase error"
        echo "    max-frame-size 65532"
        echo "    option continue-on-error"
        echo "    timeout hello 1s"
        echo "    timeout idle 3s"
        echo "    timeout processing 2s"
        echo "    use-backend be_spoa_modsecurity"
        echo
        echo "spoe-group request-check"
        echo "    messages check-request"
        echo
        echo "spoe-message check-request"
        echo "    args request_id=unique-id client_ip=src client_port=src_port server_ip=dst server_port=dst_port method=method path=path uri=url host=req.hdr(host) headers_bin=req.hdrs_bin headers=req.hdrs body=req.body body_len=req.body_len"
        if [ "${HAPROXY_ENABLE_RESPONSE_HEADERS:-0}" = "1" ]; then
            echo
            echo "spoe-group response-check"
            echo "    messages check-response"
            echo
            echo "spoe-message check-response"
            if [ "${HAPROXY_ENABLE_RESPONSE_BODY:-0}" = "1" ]; then
                echo "    args request_id=unique-id response_status=txn.status response_headers_bin=res.hdrs_bin response_headers=res.hdrs response_header_last_modified=res.hdr(Last-Modified) response_header_content_type=res.hdr(Content-Type) response_header_location=res.hdr(Location) response_header_set_cookie=res.hdr(Set-Cookie) response_header_server=res.hdr(Server) response_body=res.body response_body_len=res.body_len"
            else
                echo "    args request_id=unique-id response_status=txn.status response_headers_bin=res.hdrs_bin response_headers=res.hdrs response_header_last_modified=res.hdr(Last-Modified) response_header_content_type=res.hdr(Content-Type) response_header_location=res.hdr(Location) response_header_set_cookie=res.hdr(Set-Cookie) response_header_server=res.hdr(Server)"
            fi
        fi
    } > "$SPOE_CFG"
}

start_backend() {
    "$PYTHON_BIN" - "$BACKEND_PORT" "$DOCROOT/index.html" \
        >"$LOG_DIR/backend.stdout.log" \
        2>"$LOG_DIR/backend.stderr.log" <<'PY' &
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys

PORT = int(sys.argv[1])
BODY = Path(sys.argv[2]).read_bytes()


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "ModSecurityHarness/1.0"
    sys_version = ""

    def do_HEAD(self):
        self._send_headers()

    def do_GET(self):
        self._send_headers()
        self.wfile.write(BODY)

    def do_POST(self):
        self._discard_request_body()
        self._send_headers()
        self.wfile.write(BODY)

    def _discard_request_body(self):
        try:
            length = int(self.headers.get("Content-Length", "0") or "0")
        except ValueError:
            length = 0
        if length > 0:
            self.rfile.read(length)

    def _send_headers(self):
        self.send_response(200)
        self.send_header("Last-Modified", "Wed, 21 Oct 2015 07:28:00 GMT")
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Location", "/encoded%2Ftarget")
        self.send_header("Set-Cookie", "session=token")
        self.send_header("Set-Cookie", "a=b")
        self.send_header("Content-Length", str(len(BODY)))
        self.end_headers()

    def log_message(self, fmt, *args):
        sys.stderr.write((fmt % args) + "\n")


ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
PY
    BACKEND_PID=$!
    wait_tcp_port "$BACKEND_PORT" || blocked "backend failed to start on 127.0.0.1:$BACKEND_PORT"
}

start_agent() {
    ready_file="$RUNTIME_ROOT/spoa.ready"
    pid_file="$RUNTIME_ROOT/spoa.pid"
    port_file="$RUNTIME_ROOT/spoa.port"
    response_header_arg=
    response_body_limit=0
    if [ "${HAPROXY_ENABLE_RESPONSE_HEADERS:-0}" = "1" ]; then
        response_header_arg=--enable-response-headers
    fi
    if [ "${HAPROXY_ENABLE_RESPONSE_BODY:-0}" = "1" ]; then
        response_body_limit="${HAPROXY_RESPONSE_BODY_LIMIT:-32768}"
    fi
    LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" \
        "$SPOA_RUNTIME_BIN" \
            --listen "127.0.0.1:$SPOA_PORT" \
            --ready-file "$ready_file" \
            --pid-file "$pid_file" \
            --port-file "$port_file" \
            --log-file "$LOG_DIR/spoa-agent.log" \
            --decision-log "$LOG_DIR/decision.jsonl" \
            --audit-log "$AUDIT_LOG_FILE" \
            --rules-file "$RULES_FILE" \
            --mode block \
            --fail-mode closed \
            --runtime-mode test \
            --variant "$MODSECURITY_TEST_VARIANT" \
            --case "$CASE_NAME" \
            --expected-status "$EXPECT_STATUS" \
            --request-body-limit 65532 \
            --response-body-limit "$response_body_limit" \
            --response-body-timeout 50 \
            $response_header_arg \
            >"$LOG_DIR/spoa-runtime.stdout.log" \
            2>"$LOG_DIR/spoa-runtime.stderr.log" &
    AGENT_PID=$!
    i=0
    while [ "$i" -lt 50 ]; do
        if [ -f "$ready_file" ] && kill -0 "$AGENT_PID" 2>/dev/null; then
            return 0
        fi
        i=$((i + 1))
        sleep 0.1
    done
    if rule_parse_startup_is_not_executable; then
        mark_not_executable "ModSecurity rule parse failed for generated case; see $LOG_DIR/spoa-runtime.stderr.log"
    fi
    blocked "SPOA runtime failed to start; see $LOG_DIR/spoa-runtime.stderr.log"
}

start_haproxy() {
    write_haproxy_config
    if ! "$HAPROXY_BIN" -c -f "$HAPROXY_CFG" >"$LOG_DIR/haproxy-configtest.log" 2>&1; then
        blocked "HAProxy configtest failed; see $LOG_DIR/haproxy-configtest.log"
    fi
    "$HAPROXY_BIN" -db -f "$HAPROXY_CFG" >"$LOG_DIR/haproxy.stdout.log" 2>"$LOG_DIR/haproxy.stderr.log" &
    HAPROXY_PID=$!
    sleep 0.2
    kill -0 "$HAPROXY_PID" >/dev/null 2>&1 || blocked "HAProxy exited before request; see $LOG_DIR/haproxy.stderr.log"
}

send_case_request() {
    set -- "$CURL_BIN" -sS -X "$REQUEST_METHOD" -o "$RESPONSE_BODY" -w "%{http_code}"
    if [ -n "${REQUEST_HEADERS_FILE:-}" ] && [ -s "$REQUEST_HEADERS_FILE" ]; then
        while IFS= read -r header_line || [ -n "$header_line" ]; do
            [ -n "$header_line" ] || continue
            set -- "$@" -H "$header_line"
        done < "$REQUEST_HEADERS_FILE"
    fi
    if [ "${REQUEST_HAS_BODY:-0}" = "1" ]; then
        set -- "$@" --data-binary "@$REQUEST_BODY_FILE"
    fi
    request_url_path=$(quote_request_path "$REQUEST_PATH")
    set -- "$@" "http://127.0.0.1:$PORT$request_url_path"
    "$@" 2>"$LOG_DIR/curl-attack.err"
}

quote_request_path() {
    "$PYTHON_BIN" - "$1" <<'PY'
import sys
from urllib.parse import quote

print(quote(sys.argv[1], safe="/:?&=%+$,;@[]!'()*"))
PY
}

if [ "$RUN_ONE_CASE" != "1" ]; then
    run_all_cases
fi

require_generated_roots
load_connector_adapter_metadata
if [ -z "$TEST_CASE" ]; then
    TEST_CASE="phase2_args_block"
fi
TEST_CASE=$(resolve_case_path "$TEST_CASE") || exit 1
case_name=$(basename "$TEST_CASE" .yaml)
if [ -z "$RUNTIME_ROOT" ]; then
    RUNTIME_ROOT="$RUNTIME_BASE/$case_name"
fi
STATUS_FILE="$LOG_DIR/status.txt"

echo "haproxy_smoke: BUILD_ROOT=$BUILD_ROOT"
echo "haproxy_smoke: HAPROXY_BIN=$HAPROXY_BIN"
echo "haproxy_smoke: SPOA_RUNTIME_BIN=$SPOA_RUNTIME_BIN"
echo "haproxy_smoke: RUNTIME_ROOT=$RUNTIME_ROOT"
echo "haproxy_smoke: LOG_DIR=$LOG_DIR"
echo "haproxy_smoke: TEST_CASE=$TEST_CASE"
echo "haproxy_smoke: CASE_SCOPE=$CASE_SCOPE"
echo "haproxy_smoke: MODSECURITY_TEST_VARIANT=$MODSECURITY_TEST_VARIANT"
if [ -n "$MODSECURITY_RULE_PREAMBLE_FILE" ]; then
    echo "haproxy_smoke: MODSECURITY_RULE_PREAMBLE_FILE=$MODSECURITY_RULE_PREAMBLE_FILE"
fi

require_under_build_root "$RUNTIME_ROOT" RUNTIME_ROOT
mkdir -p "$LOG_DIR" "$LOG_DIR/audit" "$RUNTIME_ROOT/conf" "$RUNTIME_ROOT/htdocs"
: > "$STATUS_FILE"
rm -f "$LOG_DIR/"*.log \
    "$LOG_DIR/"*.err \
    "$LOG_DIR/observed-status.txt" \
    "$LOG_DIR/response-body.txt" \
    "$LOG_DIR/audit.log" \
    "$LOG_DIR/decision.jsonl" \
    "$LOG_DIR/spoa-agent.log" \
    "$RUNTIME_ROOT/conf/"*.conf \
    "$RUNTIME_ROOT/conf/"*.txt \
    "$RUNTIME_ROOT/conf/"*.bin \
    "$RUNTIME_ROOT/conf/"*.env \
    "$RUNTIME_ROOT/"*.pid \
    "$RUNTIME_ROOT/"*.ready \
    "$RUNTIME_ROOT/"*.port 2>/dev/null || true
rm -f "$LOG_DIR/audit/"* 2>/dev/null || true

CURL_BIN=$(find_curl)
[ -n "$CURL_BIN" ] || blocked "missing curl; set CURL=/path/to/curl"
[ -x "$CURL_BIN" ] || blocked "curl is not executable: $CURL_BIN"

ensure_local_haproxy
ensure_spoa_runtime

RULES_FILE="$RUNTIME_ROOT/conf/modsecurity-smoke.conf"
CASE_ENV_FILE="$RUNTIME_ROOT/conf/case.env"
REQUEST_HEADERS_FILE="$RUNTIME_ROOT/conf/request-headers.txt"
REQUEST_BODY_FILE="$RUNTIME_ROOT/conf/request-body.bin"
AUDIT_LOG_FILE="$LOG_DIR/audit.log"
AUDIT_LOG_DIR="$LOG_DIR/audit"
DOCROOT="$RUNTIME_ROOT/htdocs"
RESPONSE_BODY="$LOG_DIR/response-body.txt"
HAPROXY_CFG="$RUNTIME_ROOT/conf/haproxy.cfg"
SPOE_CFG="$RUNTIME_ROOT/conf/spoe-agent.conf"

if [ "$MODSECURITY_TEST_VARIANT" = "with-crs" ] && [ -z "$MODSECURITY_RULE_PREAMBLE_FILE" ]; then
    blocked "MODSECURITY_RULE_PREAMBLE_FILE is required for MODSECURITY_TEST_VARIANT=with-crs; run make prepare-crs"
fi

if ! "$PYTHON_BIN" "$CASE_CLI" materialize \
    --case "$TEST_CASE" \
    --rules-file "$RULES_FILE" \
    --env-file "$CASE_ENV_FILE" \
    --headers-file "$REQUEST_HEADERS_FILE" \
    --body-file "$REQUEST_BODY_FILE" \
    --docroot "$DOCROOT" \
    --audit-log-file "$AUDIT_LOG_FILE" \
    --audit-log-dir "$AUDIT_LOG_DIR" \
    --rules-preamble-file "$MODSECURITY_RULE_PREAMBLE_FILE" > "$LOG_DIR/case-materialize.log" 2>&1; then
    blocked "failed to materialize shared case; see $LOG_DIR/case-materialize.log"
fi
. "$CASE_ENV_FILE"

eval "$(case_runtime_shape)"
if [ -n "${HAPROXY_NOT_EXECUTABLE_REASON:-}" ]; then
    mark_not_executable "$HAPROXY_NOT_EXECUTABLE_REASON"
fi

PORT=$(select_free_port "$PORT" "$PORT_SEARCH_LIMIT") || blocked "no free localhost port found from $PORT within $PORT_SEARCH_LIMIT attempts"
SPOA_PORT=$(select_offset_port "$PORT" "$HAPROXY_SPOA_PORT_OFFSET" "$PORT_SEARCH_LIMIT") || blocked "no free local SPOA port found from $((PORT + HAPROXY_SPOA_PORT_OFFSET)) within $PORT_SEARCH_LIMIT attempts"
BACKEND_PORT=$(select_offset_port "$PORT" "$HAPROXY_BACKEND_PORT_OFFSET" "$PORT_SEARCH_LIMIT") || blocked "no free local backend port found from $((PORT + HAPROXY_BACKEND_PORT_OFFSET)) within $PORT_SEARCH_LIMIT attempts"
trap cleanup EXIT INT TERM
start_backend
start_agent
start_haproxy

set +e
http_status=$(send_case_request)
curl_rc=$?
set -e
printf '%s\n' "$http_status" > "$LOG_DIR/observed-status.txt"

if [ "$curl_rc" -ne 0 ]; then
    write_case_result "$TEST_CASE" fail "$http_status" "$LOG_DIR/result.json" || true
    fail "curl attack request failed rc=$curl_rc; see $LOG_DIR/curl-attack.err"
fi

if "$PYTHON_BIN" "$CASE_CLI" assert-status \
    --case "$TEST_CASE" \
    --actual-status "$http_status" \
    --response-body-file "$RESPONSE_BODY" \
    --audit-log-file "$AUDIT_LOG_FILE" \
    --status-file "$STATUS_FILE" > "$LOG_DIR/case-assert.log" 2>&1; then
    write_case_result "$TEST_CASE" pass "$http_status" "$LOG_DIR/result.json" || true
    echo "haproxy_smoke: pass case=$CASE_NAME status=$http_status"
    exit 0
fi

write_case_result "$TEST_CASE" fail "$http_status" "$LOG_DIR/result.json" || true
echo "haproxy_smoke: fail case=$CASE_NAME observed=$http_status expected=$EXPECT_STATUS"
exit 1
