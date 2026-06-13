#!/bin/sh
set -eu

CONNECTOR_ROOT="${CONNECTOR_ROOT:-$(CDPATH= cd "$(dirname "$0")/.." && pwd)}"
FRAMEWORK_ROOT="${FRAMEWORK_ROOT:-$CONNECTOR_ROOT/modules/ModSecurity-test-Framework}"
DEFAULT_STATE_HOME="${DEFAULT_STATE_HOME:-${XDG_STATE_HOME:-${HOME:-/tmp}/.local/state}}"
SOURCE_ROOT="${SOURCE_ROOT:-$DEFAULT_STATE_HOME/ModSecurity-conector-src}"
SHARED_BUILD_ROOT="${BUILD_ROOT:-$DEFAULT_STATE_HOME/ModSecurity-conector-build}"
BUILD_ROOT="$SHARED_BUILD_ROOT"
TMP_ROOT="${TMP_ROOT:-$SHARED_BUILD_ROOT/tmp}"
LOG_ROOT="${LOG_ROOT:-$SHARED_BUILD_ROOT/logs}"
MATRIX_ROOT="${MATRIX_ROOT:-$DEFAULT_STATE_HOME/ModSecurity-conector-full-matrix}"
MRTS_BUILD_ROOT="${MRTS_BUILD_ROOT:-$SHARED_BUILD_ROOT/mrts}"
PYTHON="${PYTHON:-python3}"
PYTHONDONTWRITEBYTECODE="${PYTHONDONTWRITEBYTECODE:-1}"
FORCE_ALL_CASES="${FORCE_ALL_CASES:-1}"
FULL_MATRIX_VARIANTS="${FULL_MATRIX_VARIANTS:-no-crs/no-mrts no-crs/with-mrts with-crs/no-mrts with-crs/with-mrts}"
FULL_MATRIX_CONNECTORS="${FULL_MATRIX_CONNECTORS:-apache nginx haproxy}"
FULL_MATRIX_REPORT_DIR="${FULL_MATRIX_REPORT_DIR:-$CONNECTOR_ROOT/reports/testing/generated}"
FULL_MATRIX_MANIFEST="${FULL_MATRIX_MANIFEST:-$MATRIX_ROOT/full-runtime-matrix-runs.jsonl}"
FULL_MATRIX_PORT_SPAN="${FULL_MATRIX_PORT_SPAN:-1000}"
FULL_MATRIX_PREPARE_SHARED_BUILDS="${FULL_MATRIX_PREPARE_SHARED_BUILDS:-1}"
FULL_MATRIX_PREPARE_CASE="${FULL_MATRIX_PREPARE_CASE:-action_allow_phase1_pass}"

export CONNECTOR_ROOT FRAMEWORK_ROOT SOURCE_ROOT BUILD_ROOT TMP_ROOT LOG_ROOT PYTHONDONTWRITEBYTECODE FORCE_ALL_CASES MRTS_BUILD_ROOT

REPO_ROOT="$CONNECTOR_ROOT"
. "$FRAMEWORK_ROOT/ci/common.sh"

validate_runner_paths() {
    assert_safe_runtime_path "$SHARED_BUILD_ROOT" SHARED_BUILD_ROOT || exit 77
    assert_safe_runtime_path "$TMP_ROOT" TMP_ROOT || exit 77
    assert_safe_runtime_path "$LOG_ROOT" LOG_ROOT || exit 77
    assert_safe_runtime_path "$MATRIX_ROOT" MATRIX_ROOT || exit 77
    assert_safe_runtime_path "$MRTS_BUILD_ROOT" MRTS_BUILD_ROOT || exit 77
    assert_not_system_path_for_write "$FULL_MATRIX_REPORT_DIR" FULL_MATRIX_REPORT_DIR || exit 77
    assert_not_system_path_for_write "$FULL_MATRIX_MANIFEST" FULL_MATRIX_MANIFEST || exit 77
}

validate_runner_paths
mkdir -p "$MATRIX_ROOT" "$FULL_MATRIX_REPORT_DIR"
: > "$FULL_MATRIX_MANIFEST"

pids=""
port_check_blocked=0

terminate_jobs() {
    for pid in $pids; do
        kill "$pid" >/dev/null 2>&1 || true
    done
    return 0
}

safe_rm_rf() {
    target=$1
    parent=$2
    label=$3

    safe_remove_runtime_path "$target" "$parent" "$label"
    return $?
}

trap 'terminate_jobs; exit 77' INT TERM

variant_base_port() {
    test_variant=$1
    mrts_variant=$2

    case "$test_variant/$mrts_variant" in
        no-crs/no-mrts) printf '%s\n' 18000 ;;
        no-crs/with-mrts) printf '%s\n' 21000 ;;
        with-crs/no-mrts) printf '%s\n' 24000 ;;
        with-crs/with-mrts) printf '%s\n' 27000 ;;
        *) echo "ERROR: unsupported variant $test_variant/$mrts_variant" >&2; return 2 ;;
    esac
    return 0
}

connector_offset() {
    connector=$1

    case "$connector" in
        apache) printf '%s\n' 0 ;;
        nginx) printf '%s\n' 1000 ;;
        haproxy) printf '%s\n' 2000 ;;
        *) echo "ERROR: unsupported connector $connector" >&2; return 2 ;;
    esac
    return 0
}

validate_matrix_connectors() {
    for connector in $FULL_MATRIX_CONNECTORS; do
        case "$connector" in
            apache|nginx|haproxy) ;;
            *) echo "ERROR: unsupported FULL_MATRIX_CONNECTORS item: $connector" >&2; return 2 ;;
        esac
    done
    return 0
}

summary_path_for() {
    results_dir=$1
    connector=$2

    printf '%s/%s-summary.json\n' "$results_dir" "$connector"
    return 0
}

shared_connector_ready() {
    connector=$1

    case "$connector" in
        apache)
            [ -x "${APACHE_HTTPD:-}" ] &&
                [ -f "${APACHE_MODULE:-}" ] &&
                [ -f "${APACHE_MRTS_MODSECURITY_LIB_DIR:-}/libmodsecurity.so" ]
            ;;
        nginx)
            [ -x "${MRTS_NATIVE_NGINX_BIN:-}" ] &&
                [ -f "${MRTS_NATIVE_NGINX_MODULE_DIR:-}/ngx_http_modsecurity_module.so" ] &&
                [ -f "${MRTS_NATIVE_NGINX_MODSECURITY_LIB_DIR:-${MODSECURITY_LIB_DIR:-}}/libmodsecurity.so" ]
            ;;
        haproxy)
            [ -x "${HAPROXY_BIN:-}" ] &&
                [ -x "${SPOA_RUNTIME_BIN:-}" ] &&
                [ -f "${MODSECURITY_BINDING_DIR:-}/paths.env" ]
            ;;
        *) return 1 ;;
    esac
}

prepare_shared_connector() {
    connector=$1
    if shared_connector_ready "$connector"; then
        return 0
    fi
    echo "full-matrix-parallel: prepared $connector build artifacts missing; runtime job will block without building"
    return 0
}

write_job_build_manifest() {
    manifest_path=$1
    connector=$2
    "$PYTHON" - "$manifest_path" "$connector" <<'PY'
import json
import os
import sys
from pathlib import Path

path = Path(sys.argv[1])
connector = sys.argv[2]
connector_id_env = {
    "apache": "APACHE_CONNECTOR_BUILD_ID",
    "nginx": "NGINX_CONNECTOR_BUILD_ID",
    "haproxy": "HAPROXY_CONNECTOR_BUILD_ID",
}.get(connector, "")
payload = {
    "connector": connector,
    "modsecurity_build_id": os.environ.get("MODSECURITY_BUILD_ID", ""),
    "modsecurity_prefix": os.environ.get("MODSECURITY_PREFIX", ""),
    "connector_build_id": os.environ.get(connector_id_env, ""),
    "runtime_build_cache_manifest": os.environ.get("RUNTIME_BUILD_CACHE_MANIFEST", ""),
    "prepared_only": os.environ.get("RUNTIME_COMPONENTS_PREPARED_ONLY", ""),
}
path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY
}

prepare_shared_builds() {
    for connector in $FULL_MATRIX_CONNECTORS; do
        prepare_shared_connector "$connector"
    done
    return 0
}

prepare_batch() {
    test_variant=$1
    mrts_variant=$2
    batch_root="$MATRIX_ROOT/$test_variant/$mrts_variant/_batch"
    assert_safe_runtime_path "$batch_root" "matrix batch root" || return 77
    mkdir -p "$batch_root"
    if [ "$mrts_variant" = "with-mrts" ]; then
        echo "full-matrix-parallel: preparing MRTS for $test_variant/$mrts_variant"
        env \
            FRAMEWORK_ROOT="$FRAMEWORK_ROOT" \
            CONNECTOR_ROOT="$CONNECTOR_ROOT" \
            SOURCE_ROOT="$SOURCE_ROOT" \
            BUILD_ROOT="$SHARED_BUILD_ROOT" \
            MRTS_BUILD_ROOT="$MRTS_BUILD_ROOT" \
            TMP_ROOT="$SHARED_BUILD_ROOT/tmp" \
            LOG_ROOT="$SHARED_BUILD_ROOT/logs" \
            MODSECURITY_TEST_VARIANT="$test_variant" \
            MODSECURITY_MRTS_VARIANT="$mrts_variant" \
            MODSECURITY_MRTS_PREPARED=0 \
            PYTHONDONTWRITEBYTECODE="$PYTHONDONTWRITEBYTECODE" \
            sh -eu -c '. "$FRAMEWORK_ROOT/ci/common.sh"; . "$FRAMEWORK_ROOT/ci/mrts-common.sh"; prepare_mrts_runtime_variant' \
            > "$batch_root/mrts-prepare.log" 2>&1 || \
            echo "full-matrix-parallel: MRTS prepare failed for $test_variant/$mrts_variant; jobs will block using prepared-mode checks"
    fi
    if [ "$test_variant" = "with-crs" ]; then
        echo "full-matrix-parallel: fetching CRS source for $test_variant/$mrts_variant"
        env \
            FRAMEWORK_ROOT="$FRAMEWORK_ROOT" \
            CONNECTOR_ROOT="$CONNECTOR_ROOT" \
            SOURCE_ROOT="$SOURCE_ROOT" \
            BUILD_ROOT="$SHARED_BUILD_ROOT" \
            MRTS_BUILD_ROOT="$MRTS_BUILD_ROOT" \
            TMP_ROOT="$SHARED_BUILD_ROOT/tmp" \
            LOG_ROOT="$SHARED_BUILD_ROOT/logs" \
            PYTHONDONTWRITEBYTECODE="$PYTHONDONTWRITEBYTECODE" \
            sh "$FRAMEWORK_ROOT/ci/fetch-crs.sh" > "$batch_root/crs-fetch.log" 2>&1 || \
            echo "full-matrix-parallel: CRS fetch failed for $test_variant/$mrts_variant; jobs may block"
    fi
    return 0
}

run_job() {
    test_variant=$1
    mrts_variant=$2
    connector=$3
    port=$4

    job_root="$MATRIX_ROOT/$test_variant/$mrts_variant/$connector"
    job_build_root="$job_root"
    job_tmp_root="$job_root/tmp"
    job_log_root="$job_root/logs"
    results_dir="$job_root/results"
    run_log="$job_root/run.log"
    exit_code_file="$job_root/exit.code"
    summary_path_file="$job_root/summary.path"
    job_json="$job_root/job.json"
    build_manifest="$job_root/build-manifest.json"
    summary_path=$(summary_path_for "$results_dir" "$connector")

    assert_safe_runtime_path "$job_root" "matrix job root" || exit 77
    assert_safe_runtime_path "$job_tmp_root" "matrix job tmp root" || exit 77
    assert_safe_runtime_path "$job_log_root" "matrix job log root" || exit 77
    assert_safe_runtime_path "$results_dir" "matrix job results root" || exit 77
    assert_not_system_path_for_write "$run_log" "matrix run log" || exit 77
    assert_not_system_path_for_write "$job_json" "matrix job json" || exit 77
    assert_not_system_path_for_write "$build_manifest" "matrix build manifest" || exit 77
    safe_rm_rf "$job_root" "$MATRIX_ROOT" "matrix job root"
    mkdir -p "$job_build_root" "$job_tmp_root" "$job_log_root" "$results_dir"
    : > "$run_log"
    printf '%s\n' "$summary_path" > "$summary_path_file"

    started_epoch=$(date +%s)
    started_at=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
    prepared_flag=0
    job_refresh=0
    if [ "$mrts_variant" = "with-mrts" ]; then
        prepared_flag=1
    fi
    if ! shared_connector_ready "$connector"; then
        job_refresh=1
    fi

    echo "full-matrix-parallel: job start connector=$connector variant=$test_variant/$mrts_variant port=$port" >> "$run_log"
    RUNTIME_COMPONENTS_PREPARED_ONLY=1
    export RUNTIME_COMPONENTS_PREPARED_ONLY
    write_job_build_manifest "$build_manifest" "$connector"

    common_env="FRAMEWORK_ROOT=$FRAMEWORK_ROOT CONNECTOR_ROOT=$CONNECTOR_ROOT SOURCE_ROOT=$SOURCE_ROOT BUILD_ROOT=$job_build_root MRTS_BUILD_ROOT=$MRTS_BUILD_ROOT TMP_ROOT=$job_tmp_root LOG_ROOT=$job_log_root RESULTS_DIR=$results_dir MODSECURITY_TEST_VARIANT=$test_variant MODSECURITY_MRTS_VARIANT=$mrts_variant MODSECURITY_MRTS_PREPARED=$prepared_flag FORCE_ALL_CASES=$FORCE_ALL_CASES PYTHONDONTWRITEBYTECODE=$PYTHONDONTWRITEBYTECODE PORT=$port PORT_SEARCH_LIMIT=$FULL_MATRIX_PORT_SPAN PORT_RETRY_LIMIT=1 REFRESH=$job_refresh AUTO_REFRESH_STALE_BUILD=0 CRS_RUNTIME_DIR=$job_build_root/crs MRTS_LOAD_FILE=$MRTS_BUILD_ROOT/upstream-config-tests/mrts.load SKIP_RUNTIME_COMPONENT_PREPARE=1 RUNTIME_COMPONENTS_PREPARED_ONLY=1"

    set +e
    case "$connector" in
        apache)
            env $common_env \
                APACHE_TEST_PORT="$port" \
                APACHE_BUILD_ROOT="${APACHE_BUILD_ROOT:-$SHARED_BUILD_ROOT/apache-build}" \
                APACHE_BUILD_OWNER_ROOT="$SHARED_BUILD_ROOT" \
                HTTPD_PREFIX="${HTTPD_PREFIX:-}" \
                APACHE_MODULE="${APACHE_MODULE:-}" \
                MODSECURITY_LIB_DIR="${APACHE_MRTS_MODSECURITY_LIB_DIR:-${MODSECURITY_LIB_DIR:-}}" \
                APACHE_BUILD_LOG_DIR="$job_log_root/apache-build" \
                APACHE_RUNTIME_LOG_DIR="$job_log_root/apache-runtime" \
                make -C "$CONNECTOR_ROOT" smoke-apache >> "$run_log" 2>&1
            rc=$?
            ;;
        nginx)
            nginx_harness_root="${RUNNER_TEMP:-${TMPDIR:-/tmp}}/ModSecurity-conector-full-matrix/$test_variant-$mrts_variant-nginx-$port"
            env $common_env \
                NGINX_TEST_PORT="$port" \
                NGINX_BUILD_DIR="${NGINX_BUILD_DIR:-$SHARED_BUILD_ROOT/nginx-build}" \
                NGINX_PREFIX="${NGINX_PREFIX:-}" \
                NGINX_BINARY="${MRTS_NATIVE_NGINX_BIN:-}" \
                NGINX_MODULE="${MRTS_NATIVE_NGINX_MODULE_FILE:-${MRTS_NATIVE_NGINX_MODULE_DIR:-}/ngx_http_modsecurity_module.so}" \
                MODSECURITY_LIB_DIR="${MRTS_NATIVE_NGINX_MODSECURITY_LIB_DIR:-${MODSECURITY_LIB_DIR:-}}" \
                NGINX_HARNESS_WORK_ROOT="$nginx_harness_root" \
                NGINX_RUNTIME_BASE="$nginx_harness_root/runtime" \
                NGINX_RUNTIME_LOG_DIR="$nginx_harness_root/logs" \
                make -C "$CONNECTOR_ROOT" smoke-nginx >> "$run_log" 2>&1
            rc=$?
            ;;
        haproxy)
            env $common_env \
                TMP_ROOT="$job_tmp_root" \
                LOG_ROOT="$job_log_root" \
                RESULTS_DIR="$results_dir" \
                HAPROXY_TEST_PORT="$port" \
                TEST_BACKEND_PORT=$((port + 500)) \
                HAPROXY_RUNTIME_BUILD_DIR="${HAPROXY_RUNTIME_BUILD_DIR:-$SHARED_BUILD_ROOT/haproxy-runtime-build}" \
                HAPROXY_RUNTIME_DIR="${HAPROXY_RUNTIME_DIR:-$SHARED_BUILD_ROOT/haproxy-runtime/haproxy}" \
                HAPROXY_BIN="${HAPROXY_BIN:-}" \
                SPOA_RUNTIME_BIN="${SPOA_RUNTIME_BIN:-}" \
                MODSECURITY_BINDING_DIR="${MODSECURITY_BINDING_DIR:-}" \
                LOG_DIR="$job_log_root/haproxy-runtime" \
                RUNTIME_BASE="$job_build_root/haproxy-runtime-cases" \
                make -C "$CONNECTOR_ROOT" smoke-haproxy >> "$run_log" 2>&1
            rc=$?
            ;;
        *)
            rc=2
            echo "unsupported connector: $connector" >> "$run_log"
            ;;
    esac
    set -eu
    ended_epoch=$(date +%s)
    ended_at=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
    duration=$((ended_epoch - started_epoch))
    actual_summary_path=$summary_path
    if [ ! -f "$actual_summary_path" ] && [ -f "$results_dir/force-all/$connector-summary.json" ]; then
        actual_summary_path="$results_dir/force-all/$connector-summary.json"
    fi
    printf '%s\n' "$actual_summary_path" > "$summary_path_file"
    printf '%s\n' "$rc" > "$exit_code_file"
    echo "full-matrix-parallel: job end connector=$connector variant=$test_variant/$mrts_variant rc=$rc duration=$duration" >> "$run_log"

    RUN_CONNECTOR="$connector" \
    RUN_TEST_VARIANT="$test_variant" \
    RUN_MRTS_VARIANT="$mrts_variant" \
    RUN_RC="$rc" \
    RUN_STARTED_AT="$started_at" \
    RUN_ENDED_AT="$ended_at" \
    RUN_DURATION="$duration" \
    RUN_RESULTS_DIR="$results_dir" \
    RUN_SUMMARY_PATH="$actual_summary_path" \
    RUN_LOG_PATH="$run_log" \
    "$PYTHON" - <<'PY' > "$job_json"
import json
import os

print(json.dumps({
    "connector": os.environ["RUN_CONNECTOR"],
    "test_variant": os.environ["RUN_TEST_VARIANT"],
    "mrts_variant": os.environ["RUN_MRTS_VARIANT"],
    "return_code": int(os.environ["RUN_RC"]),
    "started_at": os.environ["RUN_STARTED_AT"],
    "ended_at": os.environ["RUN_ENDED_AT"],
    "duration_seconds": int(os.environ["RUN_DURATION"]),
    "results_dir": os.environ["RUN_RESULTS_DIR"],
    "summary_path": os.environ["RUN_SUMMARY_PATH"],
    "log_path": os.environ["RUN_LOG_PATH"],
}, sort_keys=True))
PY
    exit "$rc"
}

append_job_json() {
    job_json=$1
    if [ -f "$job_json" ]; then
        cat "$job_json" >> "$FULL_MATRIX_MANIFEST"
        printf '\n' >> "$FULL_MATRIX_MANIFEST"
    fi
    return 0
}

collect_batch_ports() {
    ports_file=$1
    shift
    : > "$ports_file"
    for log_path in "$@"; do
        if [ -f "$log_path" ]; then
            sed -n 's/.*port=\([0-9][0-9]*\).*/\1/p' "$log_path" >> "$ports_file" || true
        fi
    done
    sort -u "$ports_file" -o "$ports_file"
    return 0
}

check_ports_free() {
    ports_file=$1
    [ -s "$ports_file" ] || return 0
    "$PYTHON" - "$ports_file" <<'PY'
import socket
import sys
from pathlib import Path

busy = []
for raw in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines():
    if not raw.strip():
        continue
    port = int(raw.strip())
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind(("127.0.0.1", port))
    except OSError:
        busy.append(port)
    finally:
        sock.close()
if busy:
    print("busy ports after batch: " + " ".join(map(str, busy)), file=sys.stderr)
    sys.exit(1)
PY
    return 0
}

run_batch() {
    test_variant=$1
    mrts_variant=$2
    batch_base=$(variant_base_port "$test_variant" "$mrts_variant")
    batch_root="$MATRIX_ROOT/$test_variant/$mrts_variant/_batch"
    assert_safe_runtime_path "$batch_root" "matrix batch root" || return 77
    mkdir -p "$batch_root"
    prepare_batch "$test_variant" "$mrts_variant"

    pids=""
    job_jsons=""
    logs=""
    for connector in $FULL_MATRIX_CONNECTORS; do
        offset=$(connector_offset "$connector")
        port=$((batch_base + offset))
        job_root="$MATRIX_ROOT/$test_variant/$mrts_variant/$connector"
        run_job "$test_variant" "$mrts_variant" "$connector" "$port" &
        pid=$!
        pids="$pids $pid"
        job_jsons="$job_jsons $job_root/job.json"
        logs="$logs $job_root/run.log"
        echo "full-matrix-parallel: spawned pid=$pid connector=$connector variant=$test_variant/$mrts_variant port=$port"
    done

    batch_rc=0
    for pid in $pids; do
        if ! wait "$pid"; then
            batch_rc=1
        fi
    done
    pids=""

    for job_json in $job_jsons; do
        append_job_json "$job_json"
    done

    ports_file="$batch_root/used-ports.txt"
    collect_batch_ports "$ports_file" $logs
    if ! check_ports_free "$ports_file" > "$batch_root/port-check.log" 2>&1; then
        port_check_blocked=1
        echo "full-matrix-parallel: port cleanup check failed for $test_variant/$mrts_variant; see $batch_root/port-check.log"
    fi
    return "$batch_rc"
}

validate_matrix_connectors
prepare_shared_builds

for variant in $FULL_MATRIX_VARIANTS; do
    case "$variant" in
        */*) ;;
        *) echo "ERROR: invalid FULL_MATRIX_VARIANTS item: $variant" >&2; exit 2 ;;
    esac
    test_variant=${variant%/*}
    mrts_variant=${variant#*/}
    echo "full-matrix-parallel: batch start $test_variant/$mrts_variant"
    run_batch "$test_variant" "$mrts_variant" || true
    echo "full-matrix-parallel: batch end $test_variant/$mrts_variant"
done

set +e
"$PYTHON" "$CONNECTOR_ROOT/ci/generate-full-runtime-matrix.py" \
    --connector-root "$CONNECTOR_ROOT" \
    --framework-root "$FRAMEWORK_ROOT" \
    --build-root "$MATRIX_ROOT" \
    --log-root "$MATRIX_ROOT" \
    --manifest "$FULL_MATRIX_MANIFEST" \
    --output-dir "$FULL_MATRIX_REPORT_DIR"
report_rc=$?

"$PYTHON" "$FRAMEWORK_ROOT/ci/generate-connector-work-queue.py" \
    --connector-root "$CONNECTOR_ROOT" \
    --framework-root "$FRAMEWORK_ROOT" \
    --output-root "$CONNECTOR_ROOT" \
    --full-runtime-matrix "$FULL_MATRIX_REPORT_DIR/full-runtime-matrix.generated.json"
work_queue_rc=$?

"$PYTHON" "$FRAMEWORK_ROOT/ci/generate-phase-work-queue.py" \
    --connector-root "$CONNECTOR_ROOT" \
    --framework-root "$FRAMEWORK_ROOT" \
    --output-root "$CONNECTOR_ROOT" \
    --connector-work-queue "$FULL_MATRIX_REPORT_DIR/connector-work-queue.generated.json" \
    --phase-coverage "$FULL_MATRIX_REPORT_DIR/phase-coverage.generated.md" \
    --full-runtime-matrix "$FULL_MATRIX_REPORT_DIR/full-runtime-matrix.generated.json"
phase_work_queue_rc=$?

"$PYTHON" "$CONNECTOR_ROOT/ci/generate-nolog-audit-evidence-analysis.py" \
    --connector-root "$CONNECTOR_ROOT" \
    --framework-root "$FRAMEWORK_ROOT" \
    --output-dir "$FULL_MATRIX_REPORT_DIR"
nolog_audit_evidence_rc=$?
set -eu

echo "full-matrix-parallel: manifest=$FULL_MATRIX_MANIFEST"
echo "full-matrix-parallel: report=$FULL_MATRIX_REPORT_DIR/full-runtime-matrix.generated.md"
echo "full-matrix-parallel: work_queue=$FULL_MATRIX_REPORT_DIR/connector-work-queue.generated.md"
echo "full-matrix-parallel: phase_work_queue=$FULL_MATRIX_REPORT_DIR/phase-work-queue.generated.md"

if [ "$report_rc" -ne 0 ] || [ "$work_queue_rc" -ne 0 ] || [ "$phase_work_queue_rc" -ne 0 ] || [ "$nolog_audit_evidence_rc" -ne 0 ]; then
    exit 2
fi

"$PYTHON" - "$FULL_MATRIX_REPORT_DIR/full-runtime-matrix.generated.json" "$port_check_blocked" <<'PY'
import json
import sys
from pathlib import Path

data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
port_blocked = int(sys.argv[2])
has_fail = False
has_blocked = bool(port_blocked)
for run in data.get("runs", []):
    if run.get("fail", 0) or run.get("outcome") == "FAIL":
        has_fail = True
    if run.get("blocked", 0) or run.get("missing_summary"):
        has_blocked = True
if has_fail:
    sys.exit(2)
if has_blocked:
    sys.exit(77)
sys.exit(0)
PY
