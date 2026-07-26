#!/bin/sh
# Exercise Parent-owned Apache request-body regressions through the existing
# native harness.  The harness owns the test-only module, HTTP generation,
# and evidence; this adapter deliberately owns only safe scenario selection.
set -eu

mode=${1:?usage: run-apache-request-body-regression.sh small-allow|body-deny|large-multibucket|split-trigger-chunked|non-consuming-handler|empty-body|keep-alive-repeat|fail-closed-read-error}

SCRIPT_DIR=$(CDPATH='' cd -P "$(dirname "$0")" && pwd)
CONNECTOR_ROOT=${CONNECTOR_ROOT:-$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)}
[ -d "$CONNECTOR_ROOT" ] || {
    echo "BLOCKED: Parent checkout is missing: $CONNECTOR_ROOT" >&2
    exit 77
}
CONNECTOR_ROOT=$(CDPATH='' cd -P "$CONNECTOR_ROOT" && pwd)
FRAMEWORK_ROOT=${FRAMEWORK_ROOT:-$CONNECTOR_ROOT/modules/ModSecurity-test-Framework}

[ -d "$FRAMEWORK_ROOT" ] || {
    echo "BLOCKED: Framework checkout is missing: $FRAMEWORK_ROOT" >&2
    exit 77
}
FRAMEWORK_ROOT=$(CDPATH='' cd -P "$FRAMEWORK_ROOT" && pwd)
HARNESS=$CONNECTOR_ROOT/connectors/apache/harness/run_apache_smoke.sh
[ -f "$HARNESS" ] || {
    echo "BLOCKED: Apache harness is missing: $HARNESS" >&2
    exit 77
}

: "${BUILD_ROOT:?BUILD_ROOT is required}"
: "${RUNTIME_ROOT:?RUNTIME_ROOT is required}"
: "${LOG_DIR:?LOG_DIR is required}"
: "${PORT:?PORT is required}"
: "${APACHE_REQUEST_BODY_ROOT:?APACHE_REQUEST_BODY_ROOT is required}"

require_absolute_path() {
    label=$1
    path=$2

    case "$path" in
        /*) ;;
        *)
            echo "BLOCKED: $label must be absolute: $path" >&2
            exit 77
            ;;
    esac
    case "$path" in
        *'/../'*|*/..|*'/./'*|*/.)
            echo "BLOCKED: $label must not contain dot path segments: $path" >&2
            exit 77
            ;;
        *) ;;
    esac
}

reject_symlink_ancestors() {
    candidate=$1
    label=$2
    while [ "$candidate" != / ]; do
        if [ -L "$candidate" ]; then
            echo "BLOCKED: unsafe symlink in $label path: $candidate" >&2
            exit 77
        fi
        candidate=$(dirname "$candidate")
    done
}

prepare_external_root() {
    label=$1
    path=$2
    create=${3:-0}

    require_absolute_path "$label" "$path"
    reject_symlink_ancestors "$path" "$label"
    if [ "$create" = 1 ]; then
        mkdir -p "$path"
    fi
    if [ ! -d "$path" ] || [ -L "$path" ]; then
        echo "BLOCKED: $label must be a real directory: $path" >&2
        exit 77
    fi
    reject_symlink_ancestors "$path" "$label"
    canonical=$(CDPATH='' cd -P "$path" && pwd)
    case "$canonical" in
        /|/tmp|/var/tmp|/var/tmp/codex)
            echo "BLOCKED: $label must name a task-owned child directory: $canonical" >&2
            exit 77
            ;;
        "$CONNECTOR_ROOT"|"$CONNECTOR_ROOT"/*|"$FRAMEWORK_ROOT"|"$FRAMEWORK_ROOT"/*)
            echo "BLOCKED: $label must be outside a source checkout: $canonical" >&2
            exit 77
            ;;
        *) ;;
    esac
    printf '%s\n' "$canonical"
}

prepare_run_child() {
    label=$1
    path=$2
    case "$path" in
        "$REQUEST_BODY_ROOT"/*) ;;
        *)
            echo "BLOCKED: $label must be a child of APACHE_REQUEST_BODY_ROOT: $path" >&2
            exit 77
            ;;
    esac
    canonical=$(prepare_external_root "$label" "$path" 1)
    case "$canonical" in
        "$REQUEST_BODY_ROOT"/*) printf '%s\n' "$canonical" ;;
        *)
            echo "BLOCKED: $label escapes APACHE_REQUEST_BODY_ROOT after canonicalization: $canonical" >&2
            exit 77
            ;;
    esac
}

REQUEST_BODY_ROOT=$(prepare_external_root APACHE_REQUEST_BODY_ROOT "$APACHE_REQUEST_BODY_ROOT" 1)
BUILD_ROOT=$(prepare_external_root BUILD_ROOT "$BUILD_ROOT" 0)
RUNTIME_ROOT=$(prepare_run_child RUNTIME_ROOT "$RUNTIME_ROOT")
LOG_DIR=$(prepare_run_child LOG_DIR "$LOG_DIR")

case "$PORT" in
    *[!0-9]*|'')
        echo "BLOCKED: PORT must be a numeric TCP port: $PORT" >&2
        exit 77
        ;;
    *) ;;
esac
if [ "$PORT" -lt 1 ] || [ "$PORT" -gt 65535 ]; then
    echo "BLOCKED: PORT must be between 1 and 65535: $PORT" >&2
    exit 77
fi

# Keep all request shapes and expected outcomes literal.  The test-only
# read-error route is an explicit lower input-chain failure, so it must either
# return the documented fail-closed status or fail the harness; it cannot be
# silently converted into an allow result.
case "$mode" in
    small-allow)
        expect_status=200
        large_bytes=0
        repeat_count=1
        chunked=0
        ;;
    body-deny)
        expect_status=403
        large_bytes=0
        repeat_count=1
        chunked=0
        ;;
    large-multibucket)
        expect_status=200
        large_bytes=1048577
        repeat_count=1
        chunked=0
        ;;
    split-trigger-chunked)
        expect_status=403
        large_bytes=64
        repeat_count=1
        chunked=1
        ;;
    non-consuming-handler)
        expect_status=403
        large_bytes=64
        repeat_count=1
        chunked=0
        ;;
    empty-body)
        expect_status=200
        large_bytes=0
        repeat_count=1
        chunked=0
        ;;
    keep-alive-repeat)
        expect_status=200
        large_bytes=64
        repeat_count=8
        chunked=0
        ;;
    fail-closed-read-error)
        # The local unread-body guard maps a non-HTTP discard failure to 400.
        # A harness without a deterministic injector must report BLOCKED (77),
        # never turn this control into an allow result.
        expect_status=400
        large_bytes=64
        repeat_count=1
        chunked=0
        ;;
    *)
        echo "usage: run-apache-request-body-regression.sh small-allow|body-deny|large-multibucket|split-trigger-chunked|non-consuming-handler|empty-body|keep-alive-repeat|fail-closed-read-error" >&2
        exit 2
        ;;
esac

request_path=/__request_body_consume
if [ "$mode" = non-consuming-handler ]; then
    request_path=/__request_body_nonconsume
fi

# The generic case materializer admits an external explicit case only when it
# is registered through its supported EXTRA_CASE_ROOTS boundary.  Register
# exactly this task-local configuration directory; do not widen the Framework
# search path or alter Framework-owned cases.  Runtime configuration remains
# confined to the validated task-owned runtime root and contains no payload
# beyond the small, fixed test markers above.
REQUEST_BODY_CONF_ROOT=$RUNTIME_ROOT/conf
REQUEST_BODY_CASE_FILE=$REQUEST_BODY_CONF_ROOT/apache-request-body-$mode.yaml
REQUEST_BODY_RULE_PREAMBLE_FILE=$REQUEST_BODY_CONF_ROOT/apache-request-body-$mode-rules.conf
umask 077
mkdir -p "$REQUEST_BODY_CONF_ROOT"

# The preamble establishes the common P2/audit boundary.  These fixed rules
# make every request emit the allow control (2190500) and deny only the fixed
# block marker (2190501); the harness shapes bodies for each literal mode.
# This deliberately avoids accepting arbitrary caller-provided rule text or
# rule IDs.
printf '%s\n' \
    'SecRuleEngine On' \
    'SecRequestBodyAccess On' \
    'SecAuditEngine RelevantOnly' \
    'SecAuditLogType Serial' \
    'SecAuditLogParts ABHZ' \
    'SecAuditLog "@@AUDIT_LOG@@"' \
    "SecAction \"id:2190500,phase:2,pass,log,t:none,msg:'Apache request-body allow control'\"" \
    "SecRule REQUEST_BODY \"@contains request-body-block-marker\" \"id:2190501,phase:2,deny,status:403,log,t:none,msg:'Apache request-body deny regression'\"" \
    > "$REQUEST_BODY_RULE_PREAMBLE_FILE"

# The test-only harness module selects the consuming/non-consuming handler
# from APACHE_REQUEST_BODY_MODE and replaces this basic POST-200 fixture with
# the mode-specific route/body request it drives over the real Apache input
# chain.  The declarative case remains deliberately neutral for materializing
# the test server when a mode uses a custom transport shape.
printf '%s\n' \
    "name: apache_request_body_$mode" \
    "title: Apache request-body $mode regression" \
    'category: apache-request-body-regression' \
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
    "  path: $request_path" \
    '  headers:' \
    '    Content-Type: text/plain' \
    '  body: request-body-allow-marker' \
    'response:' \
    '  body: request-body-regression-ok' \
    '  content_type: text/plain' \
    'expect:' \
    '  status: 200' \
    '  intervention: none' > "$REQUEST_BODY_CASE_FILE"

exec env \
    FRAMEWORK_ROOT="$FRAMEWORK_ROOT" \
    BUILD_ROOT="$BUILD_ROOT" \
    RUNTIME_ROOT="$RUNTIME_ROOT" \
    LOG_DIR="$LOG_DIR" \
    PORT="$PORT" \
    RUN_ONE_CASE=1 \
    TEST_CASE="$REQUEST_BODY_CASE_FILE" \
    CASE_SCOPE=all \
    EXTRA_CASE_ROOTS="$REQUEST_BODY_CONF_ROOT" \
    NO_CRS_BASELINE=1 \
    MODSECURITY_TEST_VARIANT=no-crs \
    MODSECURITY_RULE_PREAMBLE_FILE="$REQUEST_BODY_RULE_PREAMBLE_FILE" \
    MSCONNECTOR_SMOKE_STAGE=minimal_runtime_smoke \
    APACHE_REQUEST_BODY_REGRESSION_TEST=1 \
    APACHE_REQUEST_BODY_MODE="$mode" \
    APACHE_REQUEST_BODY_EXPECT_STATUS="$expect_status" \
    APACHE_REQUEST_BODY_LARGE_BYTES="$large_bytes" \
    APACHE_REQUEST_BODY_REPEAT_COUNT="$repeat_count" \
    APACHE_REQUEST_BODY_CHUNKED="$chunked" \
  sh "$HARNESS"
