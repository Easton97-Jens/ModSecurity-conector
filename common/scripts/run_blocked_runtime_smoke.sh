#!/bin/sh
set -eu

CONNECTOR_NAME=${1:?connector name is required}
INTEGRATION_MODE=${2:?integration mode is required}
SKIPPED_REASON=${3:?skipped reason is required}
MISSING_DEPENDENCY=${4:-runtime dependency unavailable}
ARCHITECTURE_DECISION=${5:-}

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
DEFAULT_CONNECTOR_ROOT=$(CDPATH= cd "$SCRIPT_DIR/../.." && pwd)
CONNECTOR_ROOT="${CONNECTOR_ROOT:-$DEFAULT_CONNECTOR_ROOT}"
CONNECTOR_ROOT=$(CDPATH= cd "$CONNECTOR_ROOT" && pwd)
CONNECTOR_DIR="$CONNECTOR_ROOT/connectors/$CONNECTOR_NAME"
HARNESS_PATH="${HARNESS_PATH:-$CONNECTOR_DIR/harness/run_${CONNECTOR_NAME}_smoke.sh}"
PYTHON_BIN="${PYTHON:-python3}"
WRITE_RESULT="$CONNECTOR_ROOT/common/scripts/write_smoke_result.py"

BUILD_ROOT="${BUILD_ROOT:-${RUNNER_TEMP:-${TMPDIR:-/var/tmp}}/ModSecurity-conector-build}"
SOURCE_ROOT="${SOURCE_ROOT:-$BUILD_ROOT/src}"
RESULTS_DIR="${RESULTS_DIR:-$BUILD_ROOT/results}"
TMP_ROOT="${TMP_ROOT:-$BUILD_ROOT/tmp}"
LOG_ROOT="${LOG_ROOT:-$BUILD_ROOT/logs}"

if [ -n "${VERIFIED_RUN_ROOT:-}" ]; then
    EVIDENCE_ROOT="${EVIDENCE_ROOT:-$VERIFIED_RUN_ROOT/$CONNECTOR_NAME-smoke}"
else
    EVIDENCE_ROOT="${EVIDENCE_ROOT:-$BUILD_ROOT/results/$CONNECTOR_NAME-smoke}"
fi
LOG_DIR="${LOG_DIR:-$EVIDENCE_ROOT/logs}"

blocked_root() {
    echo "$CONNECTOR_NAME runtime smoke: BLOCKED - $*" >&2
    exit 77
}

require_absolute() {
    path=$1
    label=$2
    case "$path" in
        /*) ;;
        *) blocked_root "$label must be absolute: $path" ;;
    esac
}

require_not_connector_artifact() {
    path=$1
    label=$2
    case "$path" in
        "$CONNECTOR_ROOT"|"$CONNECTOR_ROOT"/*)
            blocked_root "$label must not be inside connector checkout: $path"
            ;;
        *) ;;
    esac
}

starter_available() {
    if [ -f "$CONNECTOR_DIR/Makefile" ] || [ -d "$CONNECTOR_DIR/build" ]; then
        printf true
    else
        printf false
    fi
}

[ -d "$CONNECTOR_DIR" ] || blocked_root "CONNECTOR_ROOT does not contain connectors/$CONNECTOR_NAME"
[ -f "$WRITE_RESULT" ] || blocked_root "missing common smoke result helper: $WRITE_RESULT"
command -v "$PYTHON_BIN" >/dev/null 2>&1 || blocked_root "missing Python interpreter: $PYTHON_BIN"

require_absolute "$SOURCE_ROOT" SOURCE_ROOT
require_absolute "$BUILD_ROOT" BUILD_ROOT
require_absolute "$RESULTS_DIR" RESULTS_DIR
require_absolute "$TMP_ROOT" TMP_ROOT
require_absolute "$LOG_ROOT" LOG_ROOT
require_absolute "$EVIDENCE_ROOT" EVIDENCE_ROOT
require_absolute "$LOG_DIR" LOG_DIR
require_not_connector_artifact "$RESULTS_DIR" RESULTS_DIR
require_not_connector_artifact "$TMP_ROOT" TMP_ROOT
require_not_connector_artifact "$LOG_ROOT" LOG_ROOT
require_not_connector_artifact "$EVIDENCE_ROOT" EVIDENCE_ROOT
require_not_connector_artifact "$LOG_DIR" LOG_DIR

mkdir -p "$RESULTS_DIR" "$TMP_ROOT" "$LOG_ROOT" "$EVIDENCE_ROOT" "$LOG_DIR"

"$PYTHON_BIN" "$WRITE_RESULT" \
    --connector "$CONNECTOR_NAME" \
    --integration-mode "$INTEGRATION_MODE" \
    --status BLOCKED \
    --exit-code 77 \
    --runtime-verified false \
    --response-body-verified false \
    --allowed-request-status not-run \
    --blocked-request-status not-run \
    --evidence-root "$EVIDENCE_ROOT" \
    --results-dir "$RESULTS_DIR" \
    --connector-root "$CONNECTOR_ROOT" \
    --source-root "$SOURCE_ROOT" \
    --build-root "$BUILD_ROOT" \
    --tmp-root "$TMP_ROOT" \
    --log-root "$LOG_ROOT" \
    --log-dir "$LOG_DIR" \
    --harness-path "$HARNESS_PATH" \
    --skipped-reason "$SKIPPED_REASON" \
    --starter-checks-available "$(starter_available)" \
    --missing-dependency "$MISSING_DEPENDENCY" \
    --architecture-decision "$ARCHITECTURE_DECISION"

echo "$CONNECTOR_NAME runtime smoke: BLOCKED - $SKIPPED_REASON"
echo "Runtime not verified"
echo "Evidence root: $EVIDENCE_ROOT"
exit 77
