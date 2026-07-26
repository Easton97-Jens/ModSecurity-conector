#!/bin/sh
# Run the Parent-owned Apache harness under a bounded Valgrind soak.  The
# harness remains the sole owner of Apache configuration, process startup,
# traffic generation, graceful restart, and shutdown.  This runner provides
# instrumentation, artifact containment, timeout handling, and a
# payload-free evidence report.
set -eu

umask 077

EXIT_PASS=0
EXIT_FAIL=1
EXIT_BLOCKED=77
EXIT_NOT_RUN=78

usage() {
    echo "usage: run-apache-soak.sh memcheck|helgrind" >&2
}

mode=${1:-}
if [ "$#" -ne 1 ]; then
    usage
    exit 2
fi
case "$mode" in
    memcheck|helgrind) ;;
    *)
        usage
        exit 2
        ;;
esac

SCRIPT_DIR=$(CDPATH='' cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)
REPO_ROOT=$(CDPATH='' cd -P "$REPO_ROOT" && pwd)
HARNESS=${APACHE_SOAK_COMMAND:-$REPO_ROOT/connectors/apache/harness/run_apache_smoke.sh}
PYTHON_BIN=${PYTHON:-python3}

status=NOT_RUN
reason='not started'
exit_code=$EXIT_NOT_RUN
harness_rc=
timed_out=0
wrapper_used=0
valgrind_log_count=0
logs_truncated=0
requests_reported=0
restarts_reported=0
error_summary=0
definitely_lost=0
indirectly_lost=0
possibly_lost=0
still_reachable=0
invalid_read_count=0
invalid_write_count=0
invalid_free_count=0
double_free_count=0
use_after_free_count=0

is_uint() {
    case "${1:-}" in
        ''|*[!0-9]*) return 1 ;;
        *) return 0 ;;
    esac
}

require_uint_range() {
    value=$1
    minimum=$2
    maximum=$3
    label=$4
    if ! is_uint "$value" || [ "$value" -lt "$minimum" ] || [ "$value" -gt "$maximum" ]; then
        echo "BLOCKED: $label must be an integer from $minimum to $maximum" >&2
        exit "$EXIT_BLOCKED"
    fi
}

require_absolute_path() {
    path_to_check=$1
    path_label=$2
    case "$path_to_check" in
        /*) ;;
        *)
            echo "BLOCKED: $path_label must be absolute: $path_to_check" >&2
            exit "$EXIT_BLOCKED"
            ;;
    esac
    case "/$path_to_check/" in
        */../*|*/./*)
            echo "BLOCKED: $path_label must not contain traversal segments: $path_to_check" >&2
            exit "$EXIT_BLOCKED"
            ;;
        *) ;;
    esac
}

reject_symlink_ancestors() {
    ancestor_path=$1
    while [ "$ancestor_path" != / ]; do
        if [ -L "$ancestor_path" ]; then
            echo "BLOCKED: unsafe symlink in artifact path: $ancestor_path" >&2
            exit "$EXIT_BLOCKED"
        fi
        ancestor_path=$(dirname "$ancestor_path")
    done
}

prepare_external_directory() {
    directory_candidate=$1
    directory_label=$2
    create_directory=${3:-0}

    require_absolute_path "$directory_candidate" "$directory_label"
    reject_symlink_ancestors "$directory_candidate"
    if [ "$create_directory" = 1 ]; then
        mkdir -p "$directory_candidate"
    fi
    if [ ! -d "$directory_candidate" ] || [ -L "$directory_candidate" ]; then
        echo "BLOCKED: $directory_label must be a real directory: $directory_candidate" >&2
        exit "$EXIT_BLOCKED"
    fi
    reject_symlink_ancestors "$directory_candidate"
    canonical_directory=$(CDPATH='' cd -P "$directory_candidate" && pwd)
    case "$canonical_directory" in
        "$REPO_ROOT"|"$REPO_ROOT"/*)
            echo "BLOCKED: $directory_label must be outside the source checkout: $canonical_directory" >&2
            exit "$EXIT_BLOCKED"
            ;;
        *) ;;
    esac
    printf '%s\n' "$canonical_directory"
}

require_regular_executable() {
    executable_candidate=$1
    executable_label=$2
    require_absolute_path "$executable_candidate" "$executable_label"
    if [ ! -f "$executable_candidate" ] || [ -L "$executable_candidate" ] || [ ! -x "$executable_candidate" ]; then
        echo "BLOCKED: $executable_label must be a regular executable: $executable_candidate" >&2
        exit "$EXIT_BLOCKED"
    fi
}

find_executable() {
    requested=$1
    label=$2
    if [ -n "$requested" ]; then
        case "$requested" in
            /*) resolved=$requested ;;
            *) resolved=$(command -v "$requested" 2>/dev/null || true) ;;
        esac
    else
        resolved=$(command -v "$label" 2>/dev/null || true)
    fi
    if [ -z "$resolved" ] || [ ! -f "$resolved" ] || [ ! -x "$resolved" ]; then
        printf '%s\n' ''
        return 0
    fi
    (CDPATH='' cd -P "$(dirname "$resolved")" && printf '%s/%s\n' "$(pwd)" "$(basename "$resolved")")
}

limit_log_file() {
    log_file=$1
    maximum_bytes=$2
    [ -f "$log_file" ] || return 0
    size=$(wc -c < "$log_file" | tr -d '[:space:]')
    is_uint "$size" || return 0
    if [ "$size" -le "$maximum_bytes" ]; then
        return 0
    fi
    temporary="$log_file.truncated"
    tail -c "$maximum_bytes" "$log_file" > "$temporary"
    mv "$temporary" "$log_file"
    logs_truncated=$((logs_truncated + 1))
}

limit_soak_log_aggregate() {
    remaining=$maximum_artifact_bytes

    set -- "$log_dir"/*.log "$valgrind_log_dir"/*.log
    for log_file in "$@"; do
        [ -f "$log_file" ] || continue
        limit_log_file "$log_file" "$maximum_log_bytes"
        size=$(wc -c < "$log_file" | tr -d '[:space:]')
        is_uint "$size" || continue
        if [ "$size" -gt "$remaining" ]; then
            temporary="$log_file.aggregate-truncated"
            if [ "$remaining" -gt 0 ]; then
                tail -c "$remaining" "$log_file" > "$temporary"
            else
                : > "$temporary"
            fi
            mv "$temporary" "$log_file"
            size=$(wc -c < "$log_file" | tr -d '[:space:]')
            logs_truncated=$((logs_truncated + 1))
        fi
        if [ "$size" -ge "$remaining" ]; then
            remaining=0
        else
            remaining=$((remaining - size))
        fi
    done
}

prepare_upload_bundle() {
    upload_dir=$RUN_DIR/upload
    mkdir -m 700 "$upload_dir"
    cp "$report_json" "$upload_dir/apache-soak-report.json"
    cp "$report_markdown" "$upload_dir/apache-soak-report.md"
    if [ -f "$harness_result" ] && [ ! -L "$harness_result" ]; then
        cp "$harness_result" "$upload_dir/harness-result.json"
    fi
    if [ -f "$metadata_dir/valgrind-version.txt" ] && \
        [ ! -L "$metadata_dir/valgrind-version.txt" ]; then
        cp "$metadata_dir/valgrind-version.txt" "$upload_dir/valgrind-version.txt"
    fi
    chmod 600 "$upload_dir"/*
}

validate_harness_result() {
    "$PYTHON_BIN" - "$harness_result" "$duration_seconds" \
        "$restart_interval_seconds" <<'PY'
import json
from pathlib import Path
import sys

path = Path(sys.argv[1])
duration = int(sys.argv[2])
restart_interval = int(sys.argv[3])
try:
    payload = json.loads(path.read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError) as exc:
    raise SystemExit(f"invalid harness result: {exc}")
if not isinstance(payload, dict) or payload.get("status") != "PASS":
    raise SystemExit("harness result does not report PASS")
metadata = payload.get("metadata")
if not isinstance(metadata, dict):
    raise SystemExit("harness result has no metadata object")
for key in ("httpd_version", "apxs_version", "libmodsecurity_version", "compiler", "mpm"):
    if not isinstance(metadata.get(key), str) or not metadata[key].strip():
        raise SystemExit(f"harness result is missing {key}")
requests = payload.get("requests")
if not isinstance(requests, dict):
    raise SystemExit("harness result has no requests object")
for key in ("allow", "deny", "body", "large_body", "multi_bucket"):
    if not isinstance(requests.get(key), int) or requests[key] < 1:
        raise SystemExit(f"harness result lacks successful {key} traffic")
restart_count = payload.get("restart_count")
if not isinstance(restart_count, int) or restart_count < 0:
    raise SystemExit("harness result has an invalid restart count")
if restart_count < 1:
    raise SystemExit("harness result has no verified graceful restart")
PY
}

sum_valgrind_bytes() {
    metric=$1
    shift
    awk -v metric="$metric" '
        index($0, metric) {
            value = $0
            sub(/^.*: /, "", value)
            sub(/ bytes.*$/, "", value)
            gsub(/,/, "", value)
            split(value, fields, " ")
            if (fields[1] ~ /^[0-9]+$/) {
                sum += fields[1]
            }
        }
        END { printf "%.0f\\n", sum + 0 }
    ' "$@"
}

count_valgrind_matches() {
    expression=$1
    shift
    grep -E -h "$expression" "$@" 2>/dev/null | awk 'END { print NR + 0 }'
}

sum_error_summaries() {
    awk '
        /ERROR SUMMARY: [0-9]+ errors/ && $4 ~ /^[0-9]+$/ { sum += $4 }
        END { printf "%.0f\\n", sum + 0 }
    ' "$@"
}

write_reports() {
    export APACHE_SOAK_REPORT_STATUS=$status
    export APACHE_SOAK_REPORT_REASON=$reason
    export APACHE_SOAK_REPORT_EXIT_CODE=$exit_code
    export APACHE_SOAK_PARENT_SHA=$parent_sha
    export APACHE_SOAK_MODE=$mode
    export APACHE_SOAK_DURATION_SECONDS=$duration_seconds
    export APACHE_SOAK_CONCURRENCY=$concurrency
    export APACHE_SOAK_REQUEST_TIMEOUT_SECONDS=$request_timeout_seconds
    export APACHE_SOAK_RESTART_INTERVAL_SECONDS=$restart_interval_seconds
    export APACHE_SOAK_HARD_TIMEOUT_SECONDS=$hard_timeout_seconds
    export APACHE_SOAK_HARNESS_EXIT_CODE=${harness_rc:-}
    export APACHE_SOAK_TIMED_OUT=$timed_out
    export APACHE_SOAK_WRAPPER_USED=$wrapper_used
    export APACHE_SOAK_VALGRIND_LOG_COUNT=$valgrind_log_count
    export APACHE_SOAK_LOGS_TRUNCATED=$logs_truncated
    export APACHE_SOAK_REQUESTS_REPORTED=$requests_reported
    export APACHE_SOAK_RESTARTS_REPORTED=$restarts_reported
    export APACHE_SOAK_ERROR_SUMMARY=$error_summary
    export APACHE_SOAK_DEFINITELY_LOST=$definitely_lost
    export APACHE_SOAK_INDIRECTLY_LOST=$indirectly_lost
    export APACHE_SOAK_POSSIBLY_LOST=$possibly_lost
    export APACHE_SOAK_STILL_REACHABLE=$still_reachable
    export APACHE_SOAK_INVALID_READ=$invalid_read_count
    export APACHE_SOAK_INVALID_WRITE=$invalid_write_count
    export APACHE_SOAK_INVALID_FREE=$invalid_free_count
    export APACHE_SOAK_DOUBLE_FREE=$double_free_count
    export APACHE_SOAK_USE_AFTER_FREE=$use_after_free_count
    export APACHE_SOAK_VALGRIND_VERSION_FILE=$metadata_dir/valgrind-version.txt
    export APACHE_SOAK_HARNESS_RESULT_FILE=$harness_result

    "$PYTHON_BIN" - "$report_json" "$report_markdown" <<'PY'
import json
import os
from pathlib import Path
import tempfile


def text(value: object, limit: int = 512) -> str:
    rendered = str(value or "").replace("\r", " ").replace("\n", " ").strip()
    return rendered[:limit]


def integer(name: str) -> int:
    try:
        value = int(os.environ.get(name, "0"))
    except ValueError:
        return 0
    return value if value >= 0 else 0


def read_first_line(path_value: str) -> str:
    path = Path(path_value)
    if not path.is_file() or path.is_symlink():
        return "unavailable"
    try:
        return text(path.read_text(encoding="utf-8", errors="replace").splitlines()[0])
    except (OSError, IndexError):
        return "unavailable"


def bounded_harness_metadata(path_value: str) -> tuple[dict[str, object], str]:
    path = Path(path_value)
    if not path.is_file() or path.is_symlink():
        return {}, "harness result is unavailable"
    try:
        source = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {}, f"harness result is invalid: {text(exc, 160)}"
    if not isinstance(source, dict):
        return {}, "harness result is not an object"

    metadata = source.get("metadata")
    if not isinstance(metadata, dict):
        metadata = {}
    requests = source.get("requests")
    if not isinstance(requests, dict):
        requests = source.get("request_counts")
    if not isinstance(requests, dict):
        requests = {}

    def choose(*names: str) -> str:
        for name in names:
            value = source.get(name, metadata.get(name))
            if value not in (None, ""):
                return text(value)
        return "unavailable"

    bounded_requests: dict[str, int] = {}
    for key in ("allow", "deny", "body", "large_body", "multi_bucket"):
        value = requests.get(key, 0)
        bounded_requests[key] = value if isinstance(value, int) and value >= 0 else 0
    total = requests.get("total")
    if isinstance(total, int) and total >= 0:
        bounded_requests["total"] = total

    restart_value = source.get("restart_count", source.get("restarts", 0))
    if not isinstance(restart_value, int) or restart_value < 0:
        restart_value = 0
    pid_value = source.get("real_httpd_pid", source.get("httpd_pid", 0))
    if not isinstance(pid_value, int) or pid_value < 0:
        pid_value = 0

    return {
        "httpd_version": choose("httpd_version", "apache_version"),
        "apxs_version": choose("apxs_version"),
        "libmodsecurity_version": choose("libmodsecurity_version"),
        "compiler": choose("compiler"),
        "mpm": choose("mpm"),
        "real_httpd_pid": pid_value,
        "requests": bounded_requests,
        "restart_count": restart_value,
    }, ""


def atomic_write(path: Path, payload: str) -> None:
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, 0o600)
        os.replace(temporary, path)
    finally:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass


report_json = Path(os.sys.argv[1])
report_markdown = Path(os.sys.argv[2])
harness, harness_error = bounded_harness_metadata(
    os.environ.get("APACHE_SOAK_HARNESS_RESULT_FILE", "")
)
requests = harness.get("requests", {}) if isinstance(harness, dict) else {}
request_total = requests.get("total") if isinstance(requests, dict) else None
if not isinstance(request_total, int) or request_total < 0:
    request_total = sum(value for value in requests.values() if isinstance(value, int))
payload = {
    "schema_version": 1,
    "connector": "apache",
    "status": text(os.environ.get("APACHE_SOAK_REPORT_STATUS")),
    "exit_code": integer("APACHE_SOAK_REPORT_EXIT_CODE"),
    "reason": text(os.environ.get("APACHE_SOAK_REPORT_REASON")),
    "parent_commit": text(os.environ.get("APACHE_SOAK_PARENT_SHA")),
    "runtime": {
        "mode": text(os.environ.get("APACHE_SOAK_MODE")),
        "duration_seconds": integer("APACHE_SOAK_DURATION_SECONDS"),
        "concurrency": integer("APACHE_SOAK_CONCURRENCY"),
        "request_timeout_seconds": integer("APACHE_SOAK_REQUEST_TIMEOUT_SECONDS"),
        "restart_interval_seconds": integer("APACHE_SOAK_RESTART_INTERVAL_SECONDS"),
        "hard_timeout_seconds": integer("APACHE_SOAK_HARD_TIMEOUT_SECONDS"),
        "requests_reported": request_total,
        "restarts_reported": harness.get("restart_count", 0),
    },
    "host": {
        "httpd_version": harness.get("httpd_version", "unavailable"),
        "apxs_version": harness.get("apxs_version", "unavailable"),
        "libmodsecurity_version": harness.get("libmodsecurity_version", "unavailable"),
        "compiler": harness.get("compiler", "unavailable"),
        "mpm": harness.get("mpm", "unavailable"),
        "real_httpd_pid": harness.get("real_httpd_pid", 0),
    },
    "instrumentation": {
        "valgrind_version": read_first_line(os.environ.get("APACHE_SOAK_VALGRIND_VERSION_FILE", "")),
        "wrapper_used": integer("APACHE_SOAK_WRAPPER_USED") == 1,
        "valgrind_log_count": integer("APACHE_SOAK_VALGRIND_LOG_COUNT"),
        "harness_exit_code": text(os.environ.get("APACHE_SOAK_HARNESS_EXIT_CODE")),
        "timed_out": integer("APACHE_SOAK_TIMED_OUT") == 1,
        "logs_truncated_after_analysis": integer("APACHE_SOAK_LOGS_TRUNCATED"),
    },
    "valgrind": {
        "error_summary": integer("APACHE_SOAK_ERROR_SUMMARY"),
        "definitely_lost_bytes": integer("APACHE_SOAK_DEFINITELY_LOST"),
        "indirectly_lost_bytes": integer("APACHE_SOAK_INDIRECTLY_LOST"),
        "possibly_lost_bytes": integer("APACHE_SOAK_POSSIBLY_LOST"),
        "still_reachable_bytes": integer("APACHE_SOAK_STILL_REACHABLE"),
        "invalid_read_signals": integer("APACHE_SOAK_INVALID_READ"),
        "invalid_write_signals": integer("APACHE_SOAK_INVALID_WRITE"),
        "invalid_free_signals": integer("APACHE_SOAK_INVALID_FREE"),
        "double_free_signals": integer("APACHE_SOAK_DOUBLE_FREE"),
        "use_after_free_signals": integer("APACHE_SOAK_USE_AFTER_FREE"),
        "still_reachable_interpretation": "recorded separately; it is not claimed to be leak-free",
    },
    "evidence": {
        "harness_result": "harness-result.json",
        "valgrind_logs": "logs/valgrind/",
        "report_markdown": "apache-soak-report.md",
    },
}
if harness_error:
    payload["harness_metadata_note"] = harness_error

atomic_write(report_json, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def markdown_cell(value: object) -> str:
    return text(value).replace("|", "\\|")


rows = [
    ("Status", payload["status"]),
    ("Exit code", payload["exit_code"]),
    ("Parent commit", payload["parent_commit"]),
    ("Mode", payload["runtime"]["mode"]),
    ("Duration / concurrency", f"{payload['runtime']['duration_seconds']} s / {payload['runtime']['concurrency']}"),
    ("Requests / graceful restarts", f"{payload['runtime']['requests_reported']} / {payload['runtime']['restarts_reported']}"),
    ("Apache httpd / APXS", f"{payload['host']['httpd_version']} / {payload['host']['apxs_version']}"),
    ("libmodsecurity / compiler", f"{payload['host']['libmodsecurity_version']} / {payload['host']['compiler']}"),
    ("MPM", payload["host"]["mpm"]),
    ("Valgrind", payload["instrumentation"]["valgrind_version"]),
    ("Valgrind error summary", payload["valgrind"]["error_summary"]),
    ("Definitely / indirectly / possibly lost", f"{payload['valgrind']['definitely_lost_bytes']} / {payload['valgrind']['indirectly_lost_bytes']} / {payload['valgrind']['possibly_lost_bytes']} bytes"),
    ("Still reachable", f"{payload['valgrind']['still_reachable_bytes']} bytes — not classified as leak-free"),
    ("Invalid read / write / free", f"{payload['valgrind']['invalid_read_signals']} / {payload['valgrind']['invalid_write_signals']} / {payload['valgrind']['invalid_free_signals']}"),
    ("Double-free / use-after-free signals", f"{payload['valgrind']['double_free_signals']} / {payload['valgrind']['use_after_free_signals']}"),
]
markdown = [
    f"# Apache {payload['runtime']['mode']} soak report",
    "",
    "This report is payload-free. Apache lifecycle and traffic are owned by the existing Parent harness; the runner only supplies Valgrind instrumentation, bounds, and evidence handling.",
    "",
    "| Field | Value |",
    "| --- | --- |",
]
markdown.extend(f"| {markdown_cell(name)} | {markdown_cell(value)} |" for name, value in rows)
markdown.extend(
    [
        "",
        f"Reason: {markdown_cell(payload['reason'])}",
        "",
        "A PASS requires an actual Valgrind log and wrapper invocation. `still reachable` is intentionally retained as a separate observation and is never described as leak-free.",
    ]
)
if harness_error:
    markdown.extend(["", f"Harness metadata note: {markdown_cell(harness_error)}"])
atomic_write(report_markdown, "\n".join(markdown) + "\n")
PY
}

finish() {
    if ! write_reports; then
        echo "FAIL: could not write Apache soak evidence reports" >&2
        exit "$EXIT_FAIL"
    fi
    if ! prepare_upload_bundle; then
        echo "FAIL: could not prepare bounded Apache soak upload evidence" >&2
        exit "$EXIT_FAIL"
    fi
    printf '%s: Apache %s soak: %s\n' "$status" "$mode" "$reason"
    exit "$exit_code"
}

cleanup() {
    if [ -n "${watchdog_pid:-}" ] && kill -0 "$watchdog_pid" >/dev/null 2>&1; then
        kill "$watchdog_pid" >/dev/null 2>&1 || true
        wait "$watchdog_pid" >/dev/null 2>&1 || true
    fi
    if [ -n "${harness_pid:-}" ] && kill -0 "$harness_pid" >/dev/null 2>&1; then
        # The harness runs in its own session, so this cannot signal the
        # invoking shell or unrelated processes.
        kill -TERM -- "-$harness_pid" >/dev/null 2>&1 || true
        sleep 2
        if kill -0 "$harness_pid" >/dev/null 2>&1; then
            kill -KILL -- "-$harness_pid" >/dev/null 2>&1 || true
        fi
        wait "$harness_pid" >/dev/null 2>&1 || true
    fi
}

on_signal() {
    status=FAIL
    reason='interrupted before the bounded soak completed'
    exit_code=$EXIT_FAIL
    finish
}

duration_seconds=${APACHE_SOAK_DURATION_SECONDS:-30}
concurrency=${APACHE_SOAK_CONCURRENCY:-2}
request_timeout_seconds=${APACHE_SOAK_REQUEST_TIMEOUT_SECONDS:-10}
restart_interval_seconds=${APACHE_SOAK_RESTART_INTERVAL_SECONDS:-10}
hard_timeout_seconds=${APACHE_SOAK_HARD_TIMEOUT_SECONDS:-}
maximum_log_bytes=${APACHE_SOAK_MAX_LOG_BYTES:-16777216}
maximum_artifact_bytes=${APACHE_SOAK_MAX_ARTIFACT_BYTES:-33554432}
port=${APACHE_SOAK_PORT:-18080}
enabled=${APACHE_SOAK_ENABLED:-1}

require_uint_range "$duration_seconds" 1 3600 APACHE_SOAK_DURATION_SECONDS
require_uint_range "$concurrency" 1 16 APACHE_SOAK_CONCURRENCY
require_uint_range "$request_timeout_seconds" 1 120 APACHE_SOAK_REQUEST_TIMEOUT_SECONDS
require_uint_range "$restart_interval_seconds" 1 3600 APACHE_SOAK_RESTART_INTERVAL_SECONDS
if [ -z "$hard_timeout_seconds" ]; then
    hard_timeout_seconds=$((duration_seconds + (request_timeout_seconds * 6) + 60))
fi
require_uint_range "$hard_timeout_seconds" 30 7200 APACHE_SOAK_HARD_TIMEOUT_SECONDS
require_uint_range "$maximum_log_bytes" 65536 67108864 APACHE_SOAK_MAX_LOG_BYTES
require_uint_range "$maximum_artifact_bytes" 1048576 134217728 APACHE_SOAK_MAX_ARTIFACT_BYTES
require_uint_range "$port" 1024 65535 APACHE_SOAK_PORT
if [ "$hard_timeout_seconds" -le "$duration_seconds" ]; then
    echo 'BLOCKED: APACHE_SOAK_HARD_TIMEOUT_SECONDS must exceed APACHE_SOAK_DURATION_SECONDS' >&2
    exit "$EXIT_BLOCKED"
fi
if [ "$restart_interval_seconds" -gt "$duration_seconds" ]; then
    echo 'BLOCKED: APACHE_SOAK_RESTART_INTERVAL_SECONDS must not exceed APACHE_SOAK_DURATION_SECONDS' >&2
    exit "$EXIT_BLOCKED"
fi
minimum_hard_timeout_seconds=$((duration_seconds + (request_timeout_seconds * 6) + 10))
if [ "$hard_timeout_seconds" -le "$minimum_hard_timeout_seconds" ]; then
    echo "BLOCKED: APACHE_SOAK_HARD_TIMEOUT_SECONDS must exceed $minimum_hard_timeout_seconds for bounded preflight traffic" >&2
    exit "$EXIT_BLOCKED"
fi
case "$enabled" in
    0|1) ;;
    *)
        echo 'BLOCKED: APACHE_SOAK_ENABLED must be 0 or 1' >&2
        exit "$EXIT_BLOCKED"
        ;;
esac

soak_root_input=${APACHE_SOAK_ROOT:-}
if [ -z "$soak_root_input" ]; then
    echo 'BLOCKED: APACHE_SOAK_ROOT is required and must be an external absolute directory' >&2
    exit "$EXIT_BLOCKED"
fi
SOAK_ROOT=$(prepare_external_directory "$soak_root_input" APACHE_SOAK_ROOT 1)
run_name="apache-soak-$mode-$(date -u +%Y%m%dT%H%M%SZ)-$$"
RUN_DIR=$SOAK_ROOT/$run_name
if ! mkdir -m 700 "$RUN_DIR"; then
    echo "BLOCKED: cannot create task-local soak run directory: $RUN_DIR" >&2
    exit "$EXIT_BLOCKED"
fi
metadata_dir=$RUN_DIR/metadata
log_dir=$RUN_DIR/logs
valgrind_log_dir=$log_dir/valgrind
runtime_dir=$RUN_DIR/runtime
results_dir=$RUN_DIR/results
mkdir -m 700 "$metadata_dir" "$log_dir" "$valgrind_log_dir" "$runtime_dir" "$results_dir"
report_json=$RUN_DIR/apache-soak-report.json
report_markdown=$RUN_DIR/apache-soak-report.md
harness_result=$RUN_DIR/harness-result.json
ready_file=$RUN_DIR/harness-ready
wrapper_used_file=$RUN_DIR/valgrind-wrapper-used
timeout_marker=$RUN_DIR/timeout

parent_sha=$(git -C "$REPO_ROOT" rev-parse HEAD)

trap cleanup EXIT
trap on_signal HUP INT TERM

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    status=BLOCKED
    reason="Python interpreter is unavailable: $PYTHON_BIN"
    exit_code=$EXIT_BLOCKED
    finish
fi
export PYTHONDONTWRITEBYTECODE=1

if [ "$enabled" = 0 ]; then
    status=NOT_RUN
    reason='APACHE_SOAK_ENABLED=0 requested an explicit non-run'
    exit_code=$EXIT_NOT_RUN
    finish
fi

require_regular_executable "$HARNESS" APACHE_SOAK_COMMAND
case "$HARNESS" in
    "$REPO_ROOT"/connectors/apache/harness/*) ;;
    *)
        status=BLOCKED
        reason='APACHE_SOAK_COMMAND must select a checked-in Parent Apache harness executable'
        exit_code=$EXIT_BLOCKED
        finish
        ;;
esac
if ! command -v setsid >/dev/null 2>&1; then
    status=BLOCKED
    reason='setsid is required to contain the harness and all Apache children'
    exit_code=$EXIT_BLOCKED
    finish
fi

valgrind_bin=$(find_executable "${VALGRIND_BIN:-${VALGRIND:-}}" valgrind)
if [ -z "$valgrind_bin" ]; then
    status=BLOCKED
    reason='Valgrind is unavailable; no instrumentation was started'
    exit_code=$EXIT_BLOCKED
    finish
fi
if ! "$valgrind_bin" --version > "$metadata_dir/valgrind-version.txt" 2>&1; then
    status=BLOCKED
    reason='Valgrind could not report its version; no instrumentation was started'
    exit_code=$EXIT_BLOCKED
    finish
fi

build_root_input=${BUILD_ROOT:-}
if [ -z "$build_root_input" ]; then
    status=BLOCKED
    reason='BUILD_ROOT is required for the existing Apache build and harness'
    exit_code=$EXIT_BLOCKED
    finish
fi
BUILD_ROOT=$(prepare_external_directory "$build_root_input" BUILD_ROOT 0)
apache_build_root_input=${APACHE_BUILD_ROOT:-$BUILD_ROOT/apache-build}
APACHE_BUILD_ROOT=$(prepare_external_directory "$apache_build_root_input" APACHE_BUILD_ROOT 0)

wrapper=$RUN_DIR/bin/httpd-under-$mode
mkdir -m 700 "$RUN_DIR/bin"
printf '%s\n' '#!/bin/sh' > "$wrapper"
printf '%s\n' 'set -eu' >> "$wrapper"
printf '%s\n' ': "${APACHE_SOAK_VALGRIND_BIN:?missing APACHE_SOAK_VALGRIND_BIN}"' >> "$wrapper"
printf '%s\n' ': "${APACHE_SOAK_MODE:?missing APACHE_SOAK_MODE}"' >> "$wrapper"
printf '%s\n' ': "${APACHE_SOAK_VALGRIND_LOG_PREFIX:?missing APACHE_SOAK_VALGRIND_LOG_PREFIX}"' >> "$wrapper"
printf '%s\n' ': "${APACHE_SOAK_WRAPPER_USED_FILE:?missing APACHE_SOAK_WRAPPER_USED_FILE}"' >> "$wrapper"
printf '%s\n' 'printf "%s\\n" "$$" >> "$APACHE_SOAK_WRAPPER_USED_FILE"' >> "$wrapper"
printf '%s\n' 'case "$APACHE_SOAK_MODE" in' >> "$wrapper"
printf '%s\n' '    memcheck)' >> "$wrapper"
printf '%s\n' '        exec "$APACHE_SOAK_VALGRIND_BIN" --tool=memcheck --trace-children=yes --error-exitcode=99 --leak-check=full --show-leak-kinds=definite,indirect,possible,reachable --errors-for-leak-kinds=definite,indirect,possible --log-file="${APACHE_SOAK_VALGRIND_LOG_PREFIX}.%p.log" "$@"' >> "$wrapper"
printf '%s\n' '        ;;' >> "$wrapper"
printf '%s\n' '    helgrind)' >> "$wrapper"
printf '%s\n' '        exec "$APACHE_SOAK_VALGRIND_BIN" --tool=helgrind --trace-children=yes --error-exitcode=99 --log-file="${APACHE_SOAK_VALGRIND_LOG_PREFIX}.%p.log" "$@"' >> "$wrapper"
printf '%s\n' '        ;;' >> "$wrapper"
printf '%s\n' '    *) exit 2 ;;' >> "$wrapper"
printf '%s\n' 'esac' >> "$wrapper"
chmod 700 "$wrapper"

# The generic materializer accepts the neutral external fixture only through
# its supported EXTRA_CASE_ROOTS boundary.  Do not depend on a Framework case
# name: the neutral fixture plus the fixed P2 preamble below are sufficient for
# the harness' test-only consume and non-consuming routes.  Rule text and IDs
# are intentionally not caller configurable.
request_body_conf_root=$runtime_dir/conf
mkdir -m 700 "$request_body_conf_root"
request_body_case=$request_body_conf_root/apache-soak-neutral.yaml
request_body_preamble=$request_body_conf_root/apache-soak-rules.conf
printf '%s\n' \
    'SecRuleEngine On' \
    'SecRequestBodyAccess On' \
    'SecAuditEngine RelevantOnly' \
    'SecAuditLogType Serial' \
    'SecAuditLogParts ABHZ' \
    'SecAuditLog "@@AUDIT_LOG@@"' \
    "SecAction \"id:2190500,phase:2,pass,log,t:none,msg:'Apache request-body allow control'\"" \
    "SecRule REQUEST_BODY \"@contains request-body-block-marker\" \"id:2190501,phase:2,deny,status:403,log,t:none,msg:'Apache request-body deny regression'\"" \
    > "$request_body_preamble"
printf '%s\n' \
    "name: apache_soak_$mode" \
    "title: Apache $mode soak neutral request-body fixture" \
    'category: apache-request-body-soak' \
    'portable: false' \
    'connector: apache' \
    'status: pending' \
    'no_crs_baseline: true' \
    'phase: 2' \
    'required_capabilities:' \
    '  - request_body' \
    '  - phase2' \
    '  - intervention' \
    'capabilities:' \
    '  request_body: true' \
    '  phase2: true' \
    '  intervention: true' \
    'rules: |' \
    '  SecRuleEngine On' \
    'request:' \
    '  method: POST' \
    '  path: /__request_body_consume' \
    '  headers:' \
    '    Content-Type: text/plain' \
    '  body: request-body-allow-marker' \
    'response:' \
    '  body: request-body-regression-ok' \
    '  content_type: text/plain' \
    'expect:' \
    '  status: 200' \
    '  intervention: none' > "$request_body_case"

export APACHE_SOAK_VALGRIND_BIN=$valgrind_bin
export APACHE_SOAK_VALGRIND_LOG_PREFIX=$valgrind_log_dir/$mode
export APACHE_SOAK_WRAPPER_USED_FILE=$wrapper_used_file

# `setsid` gives the watchdog a dedicated process group.
# The Parent harness owns the only httpd start and termination path; this
# runner sends signals only to that session if the bounded timeout expires.
setsid env \
    BUILD_ROOT="$BUILD_ROOT" \
    APACHE_BUILD_ROOT="$APACHE_BUILD_ROOT" \
    RUNTIME_ROOT="$runtime_dir" \
    LOG_DIR="$log_dir/harness" \
    RESULTS_DIR="$results_dir" \
    PORT="$port" \
    RUN_ONE_CASE=1 \
    TEST_CASE="$request_body_case" \
    CASE_SCOPE=all \
    EXTRA_CASE_ROOTS="$request_body_conf_root" \
    NO_CRS_BASELINE=1 \
    MODSECURITY_TEST_VARIANT=no-crs \
    APACHE_SOAK_TEST=1 \
    APACHE_SOAK_HTTPD_WRAPPER="$wrapper" \
    APACHE_SOAK_RUN_ROOT="$RUN_DIR" \
    APACHE_SOAK_DURATION_SECONDS="$duration_seconds" \
    APACHE_SOAK_CONCURRENCY="$concurrency" \
    APACHE_SOAK_REQUEST_TIMEOUT_SECONDS="$request_timeout_seconds" \
    APACHE_SOAK_RESTART_INTERVAL_SECONDS="$restart_interval_seconds" \
    APACHE_SOAK_READY_FILE="$ready_file" \
    APACHE_SOAK_RESULT_FILE="$harness_result" \
    APACHE_SOAK_VALGRIND_BIN="$valgrind_bin" \
    APACHE_SOAK_VALGRIND_LOG_PREFIX="$valgrind_log_dir/$mode" \
    APACHE_SOAK_WRAPPER_USED_FILE="$wrapper_used_file" \
    MODSECURITY_RULE_PREAMBLE_FILE="$request_body_preamble" \
    APACHE_REQUEST_BODY_REGRESSION_TEST=1 \
    APACHE_REQUEST_BODY_MODE=small-allow \
    APACHE_REQUEST_BODY_EXPECT_STATUS=200 \
    APACHE_REQUEST_BODY_LARGE_BYTES=65536 \
    APACHE_REQUEST_BODY_REPEAT_COUNT=1 \
    APACHE_REQUEST_BODY_CHUNKED=0 \
    "$HARNESS" > "$log_dir/harness.stdout.log" 2> "$log_dir/harness.stderr.log" &
harness_pid=$!

(
    sleep "$hard_timeout_seconds"
    if kill -0 "$harness_pid" >/dev/null 2>&1; then
        printf '%s\n' timeout > "$timeout_marker"
        kill -TERM -- "-$harness_pid" >/dev/null 2>&1 || true
        sleep 20
        if kill -0 "$harness_pid" >/dev/null 2>&1; then
            kill -KILL -- "-$harness_pid" >/dev/null 2>&1 || true
        fi
    fi
) &
watchdog_pid=$!

set +e
wait "$harness_pid"
harness_rc=$?
set -e
if kill -0 "$watchdog_pid" >/dev/null 2>&1; then
    kill "$watchdog_pid" >/dev/null 2>&1 || true
fi
wait "$watchdog_pid" >/dev/null 2>&1 || true
watchdog_pid=
harness_pid=

if [ -f "$timeout_marker" ]; then
    timed_out=1
fi

set -- "$valgrind_log_dir"/$mode.*.log
if [ -f "$1" ]; then
    valgrind_log_count=$#
    definitely_lost=$(sum_valgrind_bytes 'definitely lost:' "$@")
    indirectly_lost=$(sum_valgrind_bytes 'indirectly lost:' "$@")
    possibly_lost=$(sum_valgrind_bytes 'possibly lost:' "$@")
    still_reachable=$(sum_valgrind_bytes 'still reachable:' "$@")
    error_summary=$(sum_error_summaries "$@")
    invalid_read_count=$(count_valgrind_matches 'Invalid read' "$@")
    invalid_write_count=$(count_valgrind_matches 'Invalid write' "$@")
    invalid_free_count=$(count_valgrind_matches 'Invalid free|Invalid delete|Invalid realloc' "$@")
    double_free_count=$(count_valgrind_matches 'double free|Double free' "$@")
    use_after_free_count=$(count_valgrind_matches "free'd|freed" "$@")
fi
if [ -s "$wrapper_used_file" ]; then
    wrapper_used=1
fi

if [ -f "$harness_result" ] && [ ! -L "$harness_result" ]; then
    requests_reported=1
fi
harness_evidence_valid=0
if [ "$requests_reported" -eq 1 ] && [ -f "$ready_file" ] && \
    [ ! -L "$ready_file" ] && validate_harness_result; then
    harness_evidence_valid=1
fi

if [ "$timed_out" -eq 1 ]; then
    status=FAIL
    reason="hard timeout expired after $hard_timeout_seconds seconds"
    exit_code=$EXIT_FAIL
elif [ "$harness_rc" -eq "$EXIT_BLOCKED" ]; then
    status=BLOCKED
    reason='the Parent Apache harness reported blocked prerequisites'
    exit_code=$EXIT_BLOCKED
elif [ "$harness_rc" -eq "$EXIT_NOT_RUN" ]; then
    status=NOT_RUN
    reason='the Parent Apache harness reported an explicit non-run'
    exit_code=$EXIT_NOT_RUN
elif [ "$harness_rc" -ne 0 ]; then
    status=FAIL
    reason="the Parent Apache harness exited $harness_rc"
    exit_code=$EXIT_FAIL
elif [ "$harness_evidence_valid" -ne 1 ]; then
    status=FAIL
    reason='the Parent Apache harness did not produce complete bounded traffic, restart, readiness, and metadata evidence'
    exit_code=$EXIT_FAIL
elif [ "$wrapper_used" -ne 1 ] || [ "$valgrind_log_count" -eq 0 ]; then
    status=FAIL
    reason='the harness returned success without evidence of an actual Valgrind-instrumented httpd'
    exit_code=$EXIT_FAIL
elif [ "$error_summary" -ne 0 ] || [ "$definitely_lost" -ne 0 ] || [ "$invalid_read_count" -ne 0 ] || [ "$invalid_write_count" -ne 0 ] || [ "$invalid_free_count" -ne 0 ] || [ "$double_free_count" -ne 0 ] || [ "$use_after_free_count" -ne 0 ]; then
    status=FAIL
    reason='Valgrind reported a definitive leak or memory-access error'
    exit_code=$EXIT_FAIL
else
    status=PASS
    reason='actual Valgrind instrumentation completed without definitive leak or memory-access errors; non-definitive and still-reachable categories are recorded separately'
    exit_code=$EXIT_PASS
fi

limit_soak_log_aggregate

finish
