#!/bin/sh
set -u

CONNECTOR_ROOT="${CONNECTOR_ROOT:-$(CDPATH= cd "$(dirname "$0")/.." && pwd)}"
FRAMEWORK_ROOT="${FRAMEWORK_ROOT:-$CONNECTOR_ROOT/modules/ModSecurity-test-Framework}"
SOURCE_ROOT="${SOURCE_ROOT:-/src}"
SHARED_BUILD_ROOT="${BUILD_ROOT:-/src/ModSecurity-conector-build}"
MATRIX_ROOT="${MATRIX_ROOT:-/src/ModSecurity-conector-full-matrix}"
PYTHON="${PYTHON:-python3}"
PYTHONDONTWRITEBYTECODE="${PYTHONDONTWRITEBYTECODE:-1}"
FORCE_ALL_CASES="${FORCE_ALL_CASES:-1}"
FULL_MATRIX_VARIANTS="${FULL_MATRIX_VARIANTS:-no-crs/no-mrts no-crs/with-mrts with-crs/no-mrts with-crs/with-mrts}"
FULL_MATRIX_REPORT_DIR="${FULL_MATRIX_REPORT_DIR:-$CONNECTOR_ROOT/reports/testing/generated}"
FULL_MATRIX_MANIFEST="${FULL_MATRIX_MANIFEST:-$MATRIX_ROOT/full-runtime-matrix-runs.jsonl}"
FULL_MATRIX_PORT_SPAN="${FULL_MATRIX_PORT_SPAN:-1000}"
FULL_MATRIX_PREPARE_SHARED_BUILDS="${FULL_MATRIX_PREPARE_SHARED_BUILDS:-1}"
FULL_MATRIX_PREPARE_CASE="${FULL_MATRIX_PREPARE_CASE:-action_allow_phase1_pass}"

export CONNECTOR_ROOT FRAMEWORK_ROOT SOURCE_ROOT PYTHONDONTWRITEBYTECODE FORCE_ALL_CASES

mkdir -p "$MATRIX_ROOT" "$FULL_MATRIX_REPORT_DIR"
: > "$FULL_MATRIX_MANIFEST"

pids=""
port_check_blocked=0

terminate_jobs() {
    for pid in $pids; do
        kill "$pid" >/dev/null 2>&1 || true
    done
}

trap 'terminate_jobs; exit 77' INT TERM

variant_base_port() {
    case "$1/$2" in
        no-crs/no-mrts) printf '%s\n' 18000 ;;
        no-crs/with-mrts) printf '%s\n' 21000 ;;
        with-crs/no-mrts) printf '%s\n' 24000 ;;
        with-crs/with-mrts) printf '%s\n' 27000 ;;
        *) echo "ERROR: unsupported variant $1/$2" >&2; exit 2 ;;
    esac
}

connector_offset() {
    case "$1" in
        apache) printf '%s\n' 0 ;;
        nginx) printf '%s\n' 1000 ;;
        haproxy) printf '%s\n' 2000 ;;
        *) echo "ERROR: unsupported connector $1" >&2; exit 2 ;;
    esac
}

summary_path_for() {
    printf '%s/%s-summary.json\n' "$1" "$2"
}

shared_connector_ready() {
    case "$1" in
        apache)
            [ -x "$SHARED_BUILD_ROOT/apache-runtime/httpd/bin/httpd" ] &&
                [ -f "$SHARED_BUILD_ROOT/apache-build/output/apache/mod_security3.so" ] &&
                [ -f "$SHARED_BUILD_ROOT/apache-build/output/modsecurity/lib/libmodsecurity.so" ]
            ;;
        nginx)
            [ -x "$SHARED_BUILD_ROOT/nginx-runtime/nginx/sbin/nginx" ] &&
                [ -f "$SHARED_BUILD_ROOT/nginx-runtime/nginx/modules/ngx_http_modsecurity_module.so" ] &&
                [ -f "$SHARED_BUILD_ROOT/nginx-build/output/modsecurity/lib/libmodsecurity.so" ]
            ;;
        haproxy)
            [ -x "$SHARED_BUILD_ROOT/haproxy-runtime/haproxy/sbin/haproxy" ] &&
                [ -x "$SHARED_BUILD_ROOT/haproxy-spoa-runtime/haproxy-modsecurity-spoa" ] &&
                [ -f "$SHARED_BUILD_ROOT/haproxy-modsecurity-binding/paths.env" ]
            ;;
    esac
}

prepare_shared_connector() {
    connector=$1
    if [ "$FULL_MATRIX_PREPARE_SHARED_BUILDS" != "1" ] || shared_connector_ready "$connector"; then
        return 0
    fi
    prep_root="$MATRIX_ROOT/_prepare/$connector"
    mkdir -p "$prep_root"
    echo "full-matrix-parallel: preparing shared $connector build artifacts"
    set +e
    env \
        FRAMEWORK_ROOT="$FRAMEWORK_ROOT" \
        CONNECTOR_ROOT="$CONNECTOR_ROOT" \
        SOURCE_ROOT="$SOURCE_ROOT" \
        BUILD_ROOT="$SHARED_BUILD_ROOT" \
        TMP_ROOT="$SHARED_BUILD_ROOT/tmp" \
        LOG_ROOT="$SHARED_BUILD_ROOT/logs" \
        RESULTS_DIR="$prep_root/results" \
        REFRESH=1 \
        MODSECURITY_TEST_VARIANT="no-crs" \
        MODSECURITY_MRTS_VARIANT="no-mrts" \
        MODSECURITY_MRTS_PREPARED=0 \
        SMOKE_CASES="$FULL_MATRIX_PREPARE_CASE" \
        FORCE_ALL_CASES=0 \
        PYTHONDONTWRITEBYTECODE="$PYTHONDONTWRITEBYTECODE" \
        make -C "$CONNECTOR_ROOT" "smoke-$connector" > "$prep_root/run.log" 2>&1
    rc=$?
    set -u
    printf '%s\n' "$rc" > "$prep_root/exit.code"
    if [ "$rc" -ne 0 ]; then
        echo "full-matrix-parallel: shared $connector prepare exited $rc; runtime jobs will report blockers if artifacts are unavailable"
    fi
    return 0
}

prepare_shared_builds() {
    prepare_shared_connector apache
    prepare_shared_connector nginx
    prepare_shared_connector haproxy
}

prepare_batch() {
    test_variant=$1
    mrts_variant=$2
    batch_root="$MATRIX_ROOT/$test_variant/$mrts_variant/_batch"
    mkdir -p "$batch_root"
    if [ "$mrts_variant" = "with-mrts" ]; then
        echo "full-matrix-parallel: preparing MRTS for $test_variant/$mrts_variant"
        env \
            FRAMEWORK_ROOT="$FRAMEWORK_ROOT" \
            CONNECTOR_ROOT="$CONNECTOR_ROOT" \
            SOURCE_ROOT="$SOURCE_ROOT" \
            BUILD_ROOT="$SHARED_BUILD_ROOT" \
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
            TMP_ROOT="$SHARED_BUILD_ROOT/tmp" \
            LOG_ROOT="$SHARED_BUILD_ROOT/logs" \
            PYTHONDONTWRITEBYTECODE="$PYTHONDONTWRITEBYTECODE" \
            sh "$FRAMEWORK_ROOT/ci/fetch-crs.sh" > "$batch_root/crs-fetch.log" 2>&1 || \
            echo "full-matrix-parallel: CRS fetch failed for $test_variant/$mrts_variant; jobs may block"
    fi
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
    summary_path=$(summary_path_for "$results_dir" "$connector")

    rm -rf "$job_root"
    mkdir -p "$job_build_root" "$job_tmp_root" "$job_log_root" "$results_dir"
    : > "$run_log"
    printf '%s\n' "$summary_path" > "$summary_path_file"

    started_epoch=$(date +%s)
    started_at=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
    prepared_flag=0
    if [ "$mrts_variant" = "with-mrts" ]; then
        prepared_flag=1
    fi

    echo "full-matrix-parallel: job start connector=$connector variant=$test_variant/$mrts_variant port=$port" >> "$run_log"

    common_env="FRAMEWORK_ROOT=$FRAMEWORK_ROOT CONNECTOR_ROOT=$CONNECTOR_ROOT SOURCE_ROOT=$SOURCE_ROOT BUILD_ROOT=$job_build_root TMP_ROOT=$job_tmp_root LOG_ROOT=$job_log_root RESULTS_DIR=$results_dir MODSECURITY_TEST_VARIANT=$test_variant MODSECURITY_MRTS_VARIANT=$mrts_variant MODSECURITY_MRTS_PREPARED=$prepared_flag FORCE_ALL_CASES=$FORCE_ALL_CASES PYTHONDONTWRITEBYTECODE=$PYTHONDONTWRITEBYTECODE PORT=$port PORT_SEARCH_LIMIT=$FULL_MATRIX_PORT_SPAN PORT_RETRY_LIMIT=1 REFRESH=0 AUTO_REFRESH_STALE_BUILD=0 CRS_RUNTIME_DIR=$job_build_root/crs MRTS_LOAD_FILE=$FRAMEWORK_ROOT/tests/mrts/generated/mrts.load"

    set +e
    case "$connector" in
        apache)
            env $common_env \
                APACHE_TEST_PORT="$port" \
                APACHE_BUILD_ROOT="$SHARED_BUILD_ROOT/apache-build" \
                HTTPD_PREFIX="$SHARED_BUILD_ROOT/apache-runtime/httpd" \
                APACHE_MODULE="$SHARED_BUILD_ROOT/apache-build/output/apache/mod_security3.so" \
                MODSECURITY_LIB_DIR="$SHARED_BUILD_ROOT/apache-build/output/modsecurity/lib" \
                APACHE_BUILD_LOG_DIR="$job_log_root/apache-build" \
                APACHE_RUNTIME_LOG_DIR="$job_log_root/apache-runtime" \
                make -C "$CONNECTOR_ROOT" smoke-apache >> "$run_log" 2>&1
            rc=$?
            ;;
        nginx)
            env $common_env \
                NGINX_TEST_PORT="$port" \
                NGINX_BUILD_DIR="$SHARED_BUILD_ROOT/nginx-build" \
                NGINX_PREFIX="$SHARED_BUILD_ROOT/nginx-runtime/nginx" \
                NGINX_BINARY="$SHARED_BUILD_ROOT/nginx-runtime/nginx/sbin/nginx" \
                NGINX_MODULE="$SHARED_BUILD_ROOT/nginx-runtime/nginx/modules/ngx_http_modsecurity_module.so" \
                MODSECURITY_LIB_DIR="$SHARED_BUILD_ROOT/nginx-build/output/modsecurity/lib" \
                NGINX_HARNESS_WORK_ROOT="$job_tmp_root/nginx-harness" \
                NGINX_RUNTIME_BASE="$job_tmp_root/nginx-runtime" \
                NGINX_RUNTIME_LOG_DIR="$job_log_root/nginx-runtime" \
                make -C "$CONNECTOR_ROOT" smoke-nginx >> "$run_log" 2>&1
            rc=$?
            ;;
        haproxy)
            env $common_env \
                HAPROXY_TEST_PORT="$port" \
                TEST_BACKEND_PORT=$((port + 500)) \
                HAPROXY_RUNTIME_BUILD_DIR="$SHARED_BUILD_ROOT/haproxy-runtime-build" \
                HAPROXY_RUNTIME_DIR="$SHARED_BUILD_ROOT/haproxy-runtime/haproxy" \
                HAPROXY_BIN="$SHARED_BUILD_ROOT/haproxy-runtime/haproxy/sbin/haproxy" \
                SPOA_RUNTIME_BIN="$SHARED_BUILD_ROOT/haproxy-spoa-runtime/haproxy-modsecurity-spoa" \
                MODSECURITY_BINDING_DIR="$SHARED_BUILD_ROOT/haproxy-modsecurity-binding" \
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
    set -u
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
}

run_batch() {
    test_variant=$1
    mrts_variant=$2
    batch_base=$(variant_base_port "$test_variant" "$mrts_variant")
    batch_root="$MATRIX_ROOT/$test_variant/$mrts_variant/_batch"
    mkdir -p "$batch_root"
    prepare_batch "$test_variant" "$mrts_variant"

    pids=""
    job_jsons=""
    logs=""
    for connector in apache nginx haproxy; do
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
        wait "$pid"
        rc=$?
        if [ "$rc" -ne 0 ]; then
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

echo "full-matrix-parallel: manifest=$FULL_MATRIX_MANIFEST"
echo "full-matrix-parallel: report=$FULL_MATRIX_REPORT_DIR/full-runtime-matrix.generated.md"
echo "full-matrix-parallel: work_queue=$FULL_MATRIX_REPORT_DIR/connector-work-queue.generated.md"

if [ "$report_rc" -ne 0 ] || [ "$work_queue_rc" -ne 0 ]; then
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
