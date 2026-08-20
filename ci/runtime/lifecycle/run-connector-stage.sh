#!/bin/sh
set -eu

connector=${1:?connector is required}
stage=${2:?stage is required}

SCRIPT_DIR=$(CDPATH='' cd "$(dirname "$0")" && pwd)
CONNECTOR_ROOT=${CONNECTOR_ROOT:-$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)}
FRAMEWORK_ROOT=${FRAMEWORK_ROOT:-$CONNECTOR_ROOT/modules/ModSecurity-test-Framework}
VERIFIED_RUN_ROOT=${VERIFIED_RUN_ROOT:-${RUNNER_TEMP:-${TMPDIR:-/var/tmp}}/ModSecurity-conector-verified}
BUILD_ROOT=${BUILD_ROOT:-$VERIFIED_RUN_ROOT/build}
CACHE_ROOT=${CACHE_ROOT:-$VERIFIED_RUN_ROOT/cache-v2}
VERIFIED_COMPONENT_CACHE=${VERIFIED_COMPONENT_CACHE:-$CACHE_ROOT/shared}
CONNECTOR_COMPONENT_CACHE=${CONNECTOR_COMPONENT_CACHE:-$VERIFIED_COMPONENT_CACHE}
TMP_ROOT=${TMP_ROOT:-$BUILD_ROOT/tmp}
LOG_ROOT=${LOG_ROOT:-$BUILD_ROOT/logs}
RESULTS_DIR=${RESULTS_DIR:-$BUILD_ROOT/stages/$connector/$stage/results}
RUNTIME_REPORT_OUTPUT_ROOT=${RUNTIME_REPORT_OUTPUT_ROOT:-$BUILD_ROOT/runtime-component-reports}
PYTHON=${PYTHON:-python3}
NO_CRS_ARTIFACT_PROFILE=${NO_CRS_ARTIFACT_PROFILE:-generic}
FIVE_CONNECTOR_PROFILE=${FIVE_CONNECTOR_PROFILE:-}
FULL_LIFECYCLE_HOST_PROFILE=${FULL_LIFECYCLE_HOST_PROFILE:-}
FULL_LIFECYCLE_EXECUTED_TARGET=${FULL_LIFECYCLE_EXECUTED_TARGET:-}
NO_CRS_SELECTED_CASES_MISSING_MESSAGE='FAIL: capability-selected No-CRS runner cases are missing'
readonly NO_CRS_SELECTED_CASES_MISSING_MESSAGE

case "$connector" in
    apache|nginx|haproxy|envoy|traefik|lighttpd) ;;
    *) echo "usage: $0 apache|nginx|haproxy|envoy|traefik|lighttpd build|config_load|start_smoke|minimal_runtime_smoke|no_crs_baseline|no_crs_with_mrts" >&2; exit 2 ;;
esac
case "$stage" in
    build|config_load|start_smoke|minimal_runtime_smoke|no_crs_baseline|no_crs_with_mrts) ;;
    *) echo "usage: $0 apache|nginx|haproxy|envoy|traefik|lighttpd build|config_load|start_smoke|minimal_runtime_smoke|no_crs_baseline|no_crs_with_mrts" >&2; exit 2 ;;
esac

validate_mrts_stage_inputs() {
    [ "$connector" = envoy ] || [ "$connector" = traefik ] || [ "$connector" = lighttpd ] || {
        echo "FAIL: no_crs_with_mrts is closed to envoy, traefik, and lighttpd" >&2
        exit 2
    }
    [ "${MSCONNECTOR_MRTS_RUNTIME:-}" = 1 ] || {
        echo "FAIL: no_crs_with_mrts requires MSCONNECTOR_MRTS_RUNTIME=1" >&2
        exit 2
    }
    [ -n "${MRTS_RUNTIME_PLAN:-}" ] || { echo "FAIL: MRTS_RUNTIME_PLAN is required" >&2; exit 2; }
    [ -n "${MRTS_RUNTIME_RESULT:-}" ] || { echo "FAIL: MRTS_RUNTIME_RESULT is required" >&2; exit 2; }
    [ -n "${MRTS_RUNTIME_EXECUTOR:-}" ] || { echo "FAIL: MRTS_RUNTIME_EXECUTOR is required" >&2; exit 2; }
    [ -n "${MRTS_RUNTIME_EXECUTOR_SHA256:-}" ] || { echo "FAIL: MRTS_RUNTIME_EXECUTOR_SHA256 is required" >&2; exit 2; }
    [ -n "${MRTS_RUNTIME_RULES_ROOT:-}" ] || { echo "FAIL: MRTS_RUNTIME_RULES_ROOT is required" >&2; exit 2; }
    [ -n "${MRTS_LOAD_FILE:-}" ] || { echo "FAIL: MRTS_LOAD_FILE is required" >&2; exit 2; }
    [ -n "${MRTS_CASE_ROOT:-}" ] || { echo "FAIL: MRTS_CASE_ROOT is required" >&2; exit 2; }
    MRTS_PYTHON_BIN=${PYTHON_BIN:-${PYTHON:-}}
    [ -n "$MRTS_PYTHON_BIN" ] || { echo "FAIL: no_crs_with_mrts requires an explicit PYTHON_BIN or PYTHON" >&2; exit 2; }
    case "$MRTS_PYTHON_BIN" in
        /*) ;;
        *) echo "FAIL: MRTS Python interpreter must be an absolute path" >&2; exit 77 ;;
    esac
    if [ -n "${PYTHON_BIN:-}" ] && [ -n "${PYTHON:-}" ] && [ "$PYTHON_BIN" != "$PYTHON" ]; then
        echo "FAIL: PYTHON_BIN and PYTHON disagree" >&2
        exit 77
    fi
    [ -f "$MRTS_PYTHON_BIN" ] || { echo "FAIL: MRTS Python interpreter is not a regular file: $MRTS_PYTHON_BIN" >&2; exit 77; }
    [ -x "$MRTS_PYTHON_BIN" ] || { echo "FAIL: MRTS Python interpreter is not executable: $MRTS_PYTHON_BIN" >&2; exit 77; }
    [ ! -L "$MRTS_PYTHON_BIN" ] || { echo "FAIL: MRTS Python interpreter must not be a symlink" >&2; exit 77; }
    case "$MRTS_RUNTIME_PLAN:$MRTS_RUNTIME_RESULT:$MRTS_RUNTIME_EXECUTOR:$MRTS_RUNTIME_RULES_ROOT:$MRTS_LOAD_FILE:$MRTS_CASE_ROOT" in
        *[!A-Za-z0-9_./:-]*) echo "FAIL: MRTS runtime paths contain unsafe characters" >&2; exit 2 ;;
    esac
    case "$MRTS_RUNTIME_PLAN:$MRTS_RUNTIME_RESULT:$MRTS_RUNTIME_EXECUTOR:$MRTS_RUNTIME_RULES_ROOT:$MRTS_LOAD_FILE:$MRTS_CASE_ROOT" in
        /*:/*:/*:/*:/*:/*) ;;
        *) echo "FAIL: MRTS runtime inputs must be absolute paths" >&2; exit 2 ;;
    esac
    case "$MRTS_RUNTIME_EXECUTOR_SHA256" in
        *[!0-9a-f]*) echo "FAIL: MRTS_RUNTIME_EXECUTOR_SHA256 must be a lowercase SHA-256 digest" >&2; exit 2 ;;
    esac
    [ "${#MRTS_RUNTIME_EXECUTOR_SHA256}" -eq 64 ] || {
        echo "FAIL: MRTS_RUNTIME_EXECUTOR_SHA256 must be a SHA-256 digest" >&2
        exit 2
    }
    case "$MRTS_RUNTIME_PLAN:$MRTS_RUNTIME_RESULT" in
        "$CONNECTOR_ROOT"/*:*|*:"$CONNECTOR_ROOT"/*)
            echo "FAIL: MRTS plan/result must be outside the checkout" >&2
            exit 77
            ;;
    esac
    case "$MRTS_LOAD_FILE" in
        "$VERIFIED_RUN_ROOT"/*) ;;
        *) echo "FAIL: MRTS_LOAD_FILE must remain under the private runtime root" >&2; exit 77 ;;
    esac
    case "$MRTS_CASE_ROOT" in
        "$VERIFIED_RUN_ROOT"/*) ;;
        *) echo "FAIL: MRTS_CASE_ROOT must remain under the private runtime root" >&2; exit 77 ;;
    esac
    case "$MRTS_RUNTIME_PLAN:$MRTS_RUNTIME_RESULT" in
        "$VERIFIED_RUN_ROOT"/*:*|*:"$VERIFIED_RUN_ROOT"/*) ;;
        *) echo "FAIL: MRTS plan/result must remain under the private runtime root" >&2; exit 77 ;;
    esac
    [ -f "$MRTS_RUNTIME_PLAN" ] || { echo "FAIL: MRTS runtime plan is missing: $MRTS_RUNTIME_PLAN" >&2; exit 77; }
    [ ! -L "$MRTS_RUNTIME_PLAN" ] || { echo "FAIL: MRTS runtime plan must not be a symlink" >&2; exit 77; }
    result_parent=$(dirname "$MRTS_RUNTIME_RESULT")
    [ -d "$result_parent" ] || { echo "FAIL: MRTS runtime result parent is missing: $result_parent" >&2; exit 77; }
    [ ! -L "$MRTS_RUNTIME_RESULT" ] || { echo "FAIL: MRTS runtime result must not be a symlink" >&2; exit 77; }
    expected_mrts_executor=$CONNECTOR_ROOT/ci/runtime/lifecycle/execute-no-crs-mrts-cases.py
    [ "$MRTS_RUNTIME_EXECUTOR" = "$expected_mrts_executor" ] || { echo "FAIL: MRTS runtime executor path is not approved" >&2; exit 77; }
    [ -f "$MRTS_RUNTIME_EXECUTOR" ] || { echo "FAIL: MRTS runtime executor is not a regular file: $MRTS_RUNTIME_EXECUTOR" >&2; exit 77; }
    [ -r "$MRTS_RUNTIME_EXECUTOR" ] || { echo "FAIL: MRTS runtime executor is not readable: $MRTS_RUNTIME_EXECUTOR" >&2; exit 77; }
    [ ! -L "$MRTS_RUNTIME_EXECUTOR" ] || { echo "FAIL: MRTS runtime executor must not be a symlink" >&2; exit 77; }
    actual_mrts_executor_sha256=$("$MRTS_PYTHON_BIN" -c 'import hashlib, pathlib, sys; print(hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest())' "$MRTS_RUNTIME_EXECUTOR") || {
        echo "FAIL: MRTS runtime executor digest calculation failed" >&2
        exit 77
    }
    [ "$actual_mrts_executor_sha256" = "$MRTS_RUNTIME_EXECUTOR_SHA256" ] || {
        echo "FAIL: MRTS runtime executor digest mismatch" >&2
        exit 77
    }
    if ! "$MRTS_PYTHON_BIN" -c 'import json, sys
def reject_duplicates(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("duplicate JSON key")
        value[key] = item
    return value
with open(sys.argv[1], encoding="utf-8") as stream:
    plan = json.load(stream, object_pairs_hook=reject_duplicates)
executor = plan.get("executor") if isinstance(plan, dict) else None
if not isinstance(executor, dict) or executor.get("path") != sys.argv[2] or executor.get("sha256") != sys.argv[3]:
    raise SystemExit(1)' "$MRTS_RUNTIME_PLAN" "$expected_mrts_executor" "$MRTS_RUNTIME_EXECUTOR_SHA256"; then
        echo "FAIL: sealed MRTS plan executor identity does not match the approved executor" >&2
        exit 77
    fi
    [ -d "$MRTS_RUNTIME_RULES_ROOT" ] || { echo "FAIL: MRTS runtime rules root is not a directory: $MRTS_RUNTIME_RULES_ROOT" >&2; exit 77; }
    [ ! -L "$MRTS_RUNTIME_RULES_ROOT" ] || { echo "FAIL: MRTS runtime rules root must not be a symlink" >&2; exit 77; }
    [ -f "$MRTS_LOAD_FILE" ] || { echo "FAIL: MRTS_LOAD_FILE is not a regular file: $MRTS_LOAD_FILE" >&2; exit 77; }
    [ ! -L "$MRTS_LOAD_FILE" ] || { echo "FAIL: MRTS_LOAD_FILE must not be a symlink" >&2; exit 77; }
    [ -d "$MRTS_CASE_ROOT" ] || { echo "FAIL: MRTS_CASE_ROOT is not a directory: $MRTS_CASE_ROOT" >&2; exit 77; }
    [ ! -L "$MRTS_CASE_ROOT" ] || { echo "FAIL: MRTS_CASE_ROOT must not be a symlink" >&2; exit 77; }
    sealed_plan_validator=$CONNECTOR_ROOT/ci/runtime/lifecycle/run-no-crs-with-mrts-target.py
    [ -f "$sealed_plan_validator" ] && [ ! -L "$sealed_plan_validator" ] || {
        echo "FAIL: sealed MRTS plan validator is unavailable" >&2
        exit 77
    }
    if ! "$MRTS_PYTHON_BIN" "$sealed_plan_validator" --validate-sealed-plan \
        --plan "$MRTS_RUNTIME_PLAN" --runtime-root "$VERIFIED_RUN_ROOT" \
        --framework-root "$FRAMEWORK_ROOT" --rules-root "$MRTS_RUNTIME_RULES_ROOT" \
        --load-file "$MRTS_LOAD_FILE"; then
        echo "FAIL: sealed MRTS plan no-CRS validation failed" >&2
        exit 77
    fi
    export MRTS_PYTHON_BIN
}

if [ "$stage" = no_crs_with_mrts ]; then
    validate_mrts_stage_inputs
fi

# A profile-selected stage has no fallback route.  The shared generic runner
# still serves the existing master connector targets when no profile is set,
# while the reusable five-connector workflow gets one closed source of truth
# before any host-specific dispatch can start.
if [ -n "$FIVE_CONNECTOR_PROFILE" ]; then
    FIVE_CONNECTOR_PROFILE_RESOLVER=$CONNECTOR_ROOT/ci/runtime/lifecycle/five-connector-no-crs-profile.py
    [ -f "$FIVE_CONNECTOR_PROFILE_RESOLVER" ] || {
        echo "FAIL: five-connector profile resolver is missing: $FIVE_CONNECTOR_PROFILE_RESOLVER" >&2
        exit 1
    }
    "$PYTHON" "$FIVE_CONNECTOR_PROFILE_RESOLVER" \
        --profile "$FIVE_CONNECTOR_PROFILE" \
        --verify-connector \
        --connector "$connector"
fi

expected_full_lifecycle_profile() {
    requested_connector=$1
    case "$requested_connector" in
        apache) printf '%s\n' native-httpd-module ;;
        nginx) printf '%s\n' native-nginx-http-module ;;
        haproxy) printf '%s\n' native-htx-filter ;;
        envoy) printf '%s\n' ext_proc ;;
        traefik) printf '%s\n' native-middleware ;;
        lighttpd) printf '%s\n' patched-native ;;
        *) return 1 ;;
    esac
}

expected_full_lifecycle_target() {
    requested_connector=$1
    case "$requested_connector" in
        apache) printf '%s\n' full-lifecycle-apache ;;
        nginx) printf '%s\n' full-lifecycle-nginx ;;
        haproxy) printf '%s\n' full-lifecycle-haproxy-htx ;;
        envoy) printf '%s\n' full-lifecycle-envoy-ext-proc ;;
        traefik) printf '%s\n' full-lifecycle-traefik-native ;;
        lighttpd) printf '%s\n' full-lifecycle-lighttpd-patched ;;
        *) return 1 ;;
    esac
}

# Full-lifecycle evidence may never fall through to a request-only or stock
# compatibility runner. Every connector below dispatches a profile-specific
# native host route; any case without matching raw host evidence remains
# non-promoted instead of borrowing compatibility evidence.
if [ "$stage" = no_crs_baseline ] && [ "$NO_CRS_ARTIFACT_PROFILE" = full_lifecycle ]; then
    expected_profile=$(expected_full_lifecycle_profile "$connector")
    expected_target=$(expected_full_lifecycle_target "$connector")
    if [ "$FULL_LIFECYCLE_HOST_PROFILE" != "$expected_profile" ] || \
       [ "$FULL_LIFECYCLE_EXECUTED_TARGET" != "$expected_target" ]; then
        echo "FAIL: full-lifecycle stage profile/target mismatch for $connector" >&2
        exit 1
    fi
fi

[ -f "$FRAMEWORK_ROOT/ci/lib/common.sh" ] || {
    echo "BLOCKED: framework common.sh is missing: $FRAMEWORK_ROOT/ci/lib/common.sh" >&2
    exit 77
}

case "$BUILD_ROOT" in
    /*) ;;
    *) echo "BLOCKED: BUILD_ROOT must be absolute: $BUILD_ROOT" >&2; exit 77 ;;
esac
case "$BUILD_ROOT" in
    "$CONNECTOR_ROOT"|"$CONNECTOR_ROOT"/*)
        echo "BLOCKED: BUILD_ROOT must be outside the checkout: $BUILD_ROOT" >&2
        exit 77
        ;;
    *) ;;
esac

assert_no_symlink_components() {
    checked_path=$1
    checked_label=$2
    while [ "$checked_path" != / ]; do
        if [ -L "$checked_path" ]; then
            echo "FAIL: $checked_label contains a symlink component: $checked_path" >&2
            return 1
        fi
        checked_path=$(dirname "$checked_path")
    done
}

prepare_private_mrts_directory() {
    private_directory=$1
    private_parent=$2
    private_label=$3
    case "$private_directory" in
        "$private_parent"/*) ;;
        *) echo "FAIL: $private_label escapes its private runtime root" >&2; return 1 ;;
    esac
    assert_no_symlink_components "$private_parent" "$private_label" || return 1
    mkdir -p "$private_directory" || {
        echo "FAIL: cannot create $private_label" >&2
        return 1
    }
    assert_no_symlink_components "$private_directory" "$private_label" || return 1
    [ -d "$private_directory" ] || {
        echo "FAIL: $private_label is not a directory" >&2
        return 1
    }
    private_owner=$(stat -c '%u' "$private_directory") || {
        echo "FAIL: cannot inspect $private_label ownership" >&2
        return 1
    }
    [ "$private_owner" = "$(id -u)" ] || {
        echo "FAIL: $private_label is not owned by the current user" >&2
        return 1
    }
    chmod 700 "$private_directory" || {
        echo "FAIL: cannot protect $private_label" >&2
        return 1
    }
}

prepare_mrts_toolchain_roots() {
    case "$VERIFIED_RUN_ROOT:$TMP_ROOT" in
        /*:/*) ;;
        *) echo "FAIL: MRTS private runtime roots must be absolute" >&2; exit 77 ;;
    esac
    case "$VERIFIED_RUN_ROOT:$TMP_ROOT" in
        "$CONNECTOR_ROOT"*|*:"$CONNECTOR_ROOT"*)
            echo "FAIL: MRTS private runtime roots must be outside the checkout" >&2
            exit 77
            ;;
    esac
    case "$TMP_ROOT" in
        "$VERIFIED_RUN_ROOT"/*) ;;
        *) echo "FAIL: TMP_ROOT must remain under the verified private runtime root" >&2; exit 77 ;;
    esac
    prepare_private_mrts_directory "$VERIFIED_RUN_ROOT" "$(dirname "$VERIFIED_RUN_ROOT")" "verified runtime root" || exit 77
    prepare_private_mrts_directory "$TMP_ROOT" "$VERIFIED_RUN_ROOT" "MRTS temporary root" || exit 77
    MRTS_TOOLCHAIN_ROOT=$VERIFIED_RUN_ROOT/mrts-toolchain/$connector
    MRTS_HOME=$MRTS_TOOLCHAIN_ROOT/home
    MRTS_XDG_CACHE_HOME=$MRTS_TOOLCHAIN_ROOT/xdg-cache
    MRTS_GOPATH=$MRTS_TOOLCHAIN_ROOT/gopath
    MRTS_GOMODCACHE=$MRTS_GOPATH/pkg/mod
    MRTS_GOCACHE=$MRTS_TOOLCHAIN_ROOT/go-build-cache
    MRTS_GOTMPDIR=$TMP_ROOT/mrts-go/$connector
    MRTS_TMPDIR=$TMP_ROOT/mrts-tmp/$connector
    for private_dir in "$MRTS_TOOLCHAIN_ROOT" "$MRTS_HOME" "$MRTS_XDG_CACHE_HOME" "$MRTS_GOPATH" "$MRTS_GOMODCACHE" "$MRTS_GOCACHE"; do
        prepare_private_mrts_directory "$private_dir" "$VERIFIED_RUN_ROOT" "MRTS toolchain directory" || exit 77
    done
    for private_dir in "$MRTS_GOTMPDIR" "$MRTS_TMPDIR"; do
        prepare_private_mrts_directory "$private_dir" "$TMP_ROOT" "MRTS temporary directory" || exit 77
    done
    export MRTS_TOOLCHAIN_ROOT MRTS_HOME MRTS_XDG_CACHE_HOME MRTS_GOPATH MRTS_GOMODCACHE MRTS_GOCACHE MRTS_GOTMPDIR MRTS_TMPDIR
}

if [ "$stage" = no_crs_with_mrts ]; then
    prepare_mrts_toolchain_roots
fi

export CONNECTOR_ROOT FRAMEWORK_ROOT VERIFIED_RUN_ROOT BUILD_ROOT CACHE_ROOT VERIFIED_COMPONENT_CACHE CONNECTOR_COMPONENT_CACHE TMP_ROOT LOG_ROOT RESULTS_DIR
export RUNTIME_REPORT_OUTPUT_ROOT RUNTIME_ROOT RUNTIME_BASE PYTHON RUNTIME_COMPONENT_ENV_SNAPSHOT
case "$connector" in
    apache|nginx|haproxy) RUNTIME_COMPONENT_TARGET=$connector ;;
    envoy|traefik|lighttpd) RUNTIME_COMPONENT_TARGET=shared ;;
    *)
        echo "FAIL: unsupported connector runtime-component target: $connector" >&2
        exit 2
        ;;
esac
export RUNTIME_COMPONENT_TARGET

run_framework_host() {
    framework_script=$1
    smoke_stage=$2
    shift 2
    exec "$CONNECTOR_ROOT/ci/provisioning/cache/with-runtime-components.sh" env \
        CONNECTOR_ROOT="$CONNECTOR_ROOT" \
        FRAMEWORK_ROOT="$FRAMEWORK_ROOT" \
        VERIFIED_RUN_ROOT="$VERIFIED_RUN_ROOT" \
        VERIFIED_COMPONENT_CACHE="$VERIFIED_COMPONENT_CACHE" \
        CACHE_ROOT="$CACHE_ROOT" \
        CONNECTOR_COMPONENT_CACHE="$CONNECTOR_COMPONENT_CACHE" \
        BUILD_ROOT="$BUILD_ROOT" \
        TMP_ROOT="$TMP_ROOT" \
        LOG_ROOT="$LOG_ROOT" \
        RESULTS_DIR="$RESULTS_DIR" \
        RUNTIME_REPORT_OUTPUT_ROOT="$RUNTIME_REPORT_OUTPUT_ROOT" \
        RUNTIME_COMPONENT_TARGET="$RUNTIME_COMPONENT_TARGET" \
        RUNTIME_COMPONENT_ENV_SNAPSHOT="${RUNTIME_COMPONENT_ENV_SNAPSHOT:-}" \
        NO_CRS_BASELINE=1 \
        NO_CRS_SELECTED_CASE_IDS="${NO_CRS_SELECTED_CASE_IDS:-}" \
        MODSECURITY_TEST_VARIANT=no-crs \
        MODSECURITY_MRTS_VARIANT=no-mrts \
        MODSECURITY_RULE_PREAMBLE_FILE="${NO_CRS_RULES_FILE:-}" \
        MSCONNECTOR_SMOKE_STAGE="$smoke_stage" \
        "$@" sh "$FRAMEWORK_ROOT/ci/runtime/$framework_script"
}

run_remaining_connector() {
    target=$1
    if [ "$stage" = no_crs_with_mrts ]; then
        exec env -i \
            PATH=/usr/local/go/bin:/usr/bin:/bin \
            HOME="$MRTS_HOME" \
            XDG_CACHE_HOME="$MRTS_XDG_CACHE_HOME" \
            GOPATH="$MRTS_GOPATH" \
            GOMODCACHE="$MRTS_GOMODCACHE" \
            GOCACHE="$MRTS_GOCACHE" \
            GOTMPDIR="$MRTS_GOTMPDIR" \
            TMPDIR="$MRTS_TMPDIR" \
            GOENV=off \
            PYTHON="$MRTS_PYTHON_BIN" \
            PYTHON_BIN="$MRTS_PYTHON_BIN" \
            CONNECTOR_ROOT="$CONNECTOR_ROOT" \
            FRAMEWORK_ROOT="$FRAMEWORK_ROOT" \
            VERIFIED_RUN_ROOT="$VERIFIED_RUN_ROOT" \
            VERIFIED_COMPONENT_CACHE="$VERIFIED_COMPONENT_CACHE" \
            CONNECTOR_COMPONENT_CACHE="$CONNECTOR_COMPONENT_CACHE" \
            CACHE_ROOT="$CACHE_ROOT" \
            BUILD_ROOT="$BUILD_ROOT" \
            TMP_ROOT="$TMP_ROOT" \
            LOG_ROOT="$LOG_ROOT" \
            RESULTS_DIR="$RESULTS_DIR" \
            RUNTIME_ROOT="$BUILD_ROOT/stages/$connector/no_crs_with_mrts/runtime" \
            RUNTIME_BASE="$BUILD_ROOT/stages/$connector/no_crs_with_mrts/runtime" \
            RUNTIME_REPORT_OUTPUT_ROOT="$RUNTIME_REPORT_OUTPUT_ROOT" \
            RUNTIME_COMPONENT_TARGET="$RUNTIME_COMPONENT_TARGET" \
            RUNTIME_COMPONENT_ENV_SNAPSHOT="${RUNTIME_COMPONENT_ENV_SNAPSHOT:-}" \
            MSCONNECTOR_MRTS_STAGE=no_crs_with_mrts \
            MSCONNECTOR_MRTS_RUNTIME=1 \
            NO_CRS_BASELINE=1 \
            MODSECURITY_TEST_VARIANT=no-crs \
            MODSECURITY_MRTS_VARIANT=with-mrts \
            MRTS_RUNTIME_PLAN="$MRTS_RUNTIME_PLAN" \
            MRTS_RUNTIME_RESULT="$MRTS_RUNTIME_RESULT" \
            MRTS_RUNTIME_EXECUTOR="$MRTS_RUNTIME_EXECUTOR" \
            MRTS_RUNTIME_EXECUTOR_SHA256="$MRTS_RUNTIME_EXECUTOR_SHA256" \
            MRTS_RUNTIME_RULES_ROOT="$MRTS_RUNTIME_RULES_ROOT" \
            MRTS_LOAD_FILE="$MRTS_LOAD_FILE" \
            MRTS_CASE_ROOT="$MRTS_CASE_ROOT" \
            MSCONNECTOR_RULES_FILE="$MRTS_LOAD_FILE" \
            NO_CRS_RULES_FILE="$MRTS_LOAD_FILE" \
            RULES_FILE="$MRTS_LOAD_FILE" \
            MODSECURITY_RULE_PREAMBLE_FILE="$MRTS_LOAD_FILE" \
            GO=/usr/local/go/bin/go \
            GOTOOLCHAIN=local \
            sh "$CONNECTOR_ROOT/ci/runtime/lifecycle/run-remaining-connector-target.sh" "$connector" "$target"
    fi
    exec env \
        CONNECTOR_ROOT="$CONNECTOR_ROOT" \
        FRAMEWORK_ROOT="$FRAMEWORK_ROOT" \
        VERIFIED_RUN_ROOT="$VERIFIED_RUN_ROOT" \
        VERIFIED_COMPONENT_CACHE="$VERIFIED_COMPONENT_CACHE" \
        CACHE_ROOT="$CACHE_ROOT" \
        CONNECTOR_COMPONENT_CACHE="$CONNECTOR_COMPONENT_CACHE" \
        BUILD_ROOT="$BUILD_ROOT" \
        TMP_ROOT="$TMP_ROOT" \
        LOG_ROOT="$LOG_ROOT" \
        RESULTS_DIR="$RESULTS_DIR" \
        RUNTIME_ROOT="${RUNTIME_ROOT:-$BUILD_ROOT/runtime}" \
        RUNTIME_BASE="${RUNTIME_BASE:-$BUILD_ROOT/runtime}" \
        RUNTIME_REPORT_OUTPUT_ROOT="$RUNTIME_REPORT_OUTPUT_ROOT" \
        RUNTIME_COMPONENT_TARGET="$RUNTIME_COMPONENT_TARGET" \
        RUNTIME_COMPONENT_ENV_SNAPSHOT="${RUNTIME_COMPONENT_ENV_SNAPSHOT:-}" \
        TRAEFIK_ENGINE_SOCKET_PARENT="${TRAEFIK_ENGINE_SOCKET_PARENT:-}" \
        sh "$CONNECTOR_ROOT/ci/runtime/lifecycle/run-remaining-connector-target.sh" "$connector" "$target"
}

run_full_lifecycle_haproxy_htx() {
    # The overlay build is connector-local while its pinned source and
    # libmodsecurity prerequisites remain in Cache-v2 shared components.
    # Its raw native HTX records are collected only from this selected host.
    case "$PYTHON" in
        /*) python_bin=$PYTHON ;;
        */*) python_bin=$CONNECTOR_ROOT/$PYTHON ;;
        *) python_bin=$PYTHON ;;
    esac
    # shellcheck disable=SC2016 # The explicitly invoked inner shell expands this script.
    exec "$CONNECTOR_ROOT/ci/provisioning/cache/with-runtime-components.sh" env PYTHON="$python_bin" sh -eu -c '
        : "${HAPROXY_SOURCE_DIR:?HAProxy source was not provisioned}"
        : "${MODSECURITY_INCLUDE_DIR:?libmodsecurity headers were not provisioned}"
        : "${MODSECURITY_LIB_DIR:?libmodsecurity library was not provisioned}"
        make -C "$CONNECTOR_ROOT/connectors/haproxy" runtime-smoke-haproxy-htx \
            BUILD_ROOT="$BUILD_ROOT" REPO_ROOT="$CONNECTOR_ROOT" \
            HAPROXY_HTX_SOURCE_DIR="$HAPROXY_SOURCE_DIR" \
            HAPROXY_HTX_RUNTIME_ROOT="$RUNTIME_ROOT" \
            HAPROXY_HTX_BUILD_DIR="$RUNTIME_ROOT/overlay-build" \
            HAPROXY_HTX_BIN="$RUNTIME_ROOT/overlay-build/worktree/haproxy" \
            HAPROXY_HTX_EVENT_LOG_PATH="$RUNTIME_ROOT/events.jsonl" \
            PYTHON="$PYTHON"
    '
}

case "$connector:$stage" in
    apache:build)
        run_framework_host run-apache-smoke.sh build
        ;;
    nginx:build)
        run_framework_host run-nginx-smoke.sh build
        ;;
    haproxy:build)
        # shellcheck disable=SC2016 # The explicitly invoked inner shell expands this script.
        exec "$CONNECTOR_ROOT/ci/provisioning/cache/with-runtime-components.sh" sh -eu -c '
            sh "$FRAMEWORK_ROOT/ci/provisioning/prepare-haproxy-runtime.sh"
            make -C "$CONNECTOR_ROOT/connectors/haproxy" build-modsecurity-binding build-spoa-runtime \
                BUILD_ROOT="$BUILD_ROOT" REPO_ROOT="$CONNECTOR_ROOT"
        '
        ;;
    apache:config_load|nginx:config_load|haproxy:config_load)
        run_framework_host "run-$connector-smoke.sh" config_load \
            RUN_ONE_CASE=1 TEST_CASE=allow_without_marker
        ;;
    apache:start_smoke|nginx:start_smoke|haproxy:start_smoke)
        run_framework_host "run-$connector-smoke.sh" start_smoke \
            RUN_ONE_CASE=1 TEST_CASE=allow_without_marker
        ;;
    apache:minimal_runtime_smoke|nginx:minimal_runtime_smoke|haproxy:minimal_runtime_smoke)
        run_framework_host "run-$connector-smoke.sh" minimal_runtime_smoke \
            RUN_ONE_CASE=0 SMOKE_CASES="allow_without_marker deny_header_marker_403"
        ;;
    haproxy:no_crs_baseline)
        if [ "$NO_CRS_ARTIFACT_PROFILE" = full_lifecycle ]; then
            # This helper execs the HTX observer.  Do not continue into the
            # SPOE/SPOP compatibility runner after a native full profile.
            run_full_lifecycle_haproxy_htx
        else
            [ -n "${NO_CRS_SELECTED_CASES:-}" ] || {
                echo "$NO_CRS_SELECTED_CASES_MISSING_MESSAGE" >&2
                exit 1
            }
            run_framework_host "run-$connector-smoke.sh" minimal_runtime_smoke \
                RUN_ONE_CASE=0 SMOKE_CASES="$NO_CRS_SELECTED_CASES"
        fi
        ;;
    apache:no_crs_baseline|nginx:no_crs_baseline)
        [ -n "${NO_CRS_SELECTED_CASES:-}" ] || {
            echo "$NO_CRS_SELECTED_CASES_MISSING_MESSAGE" >&2
            exit 1
        }
        run_framework_host "run-$connector-smoke.sh" minimal_runtime_smoke \
            RUN_ONE_CASE=0 SMOKE_CASES="$NO_CRS_SELECTED_CASES"
        ;;
    envoy:build)
        run_remaining_connector build-envoy-connector
        ;;
    traefik:build)
        run_remaining_connector build-traefik-connector
        ;;
    lighttpd:build)
        run_remaining_connector build-lighttpd-connector
        ;;
    envoy:config_load)
        run_remaining_connector check-envoy-config
        ;;
    traefik:config_load)
        run_remaining_connector check-traefik-config
        ;;
    lighttpd:config_load)
        run_remaining_connector check-lighttpd-config
        ;;
    envoy:start_smoke)
        run_remaining_connector start-smoke-envoy
        ;;
    traefik:start_smoke)
        run_remaining_connector start-smoke-traefik
        ;;
    lighttpd:start_smoke)
        run_remaining_connector start-smoke-lighttpd
        ;;
    envoy:minimal_runtime_smoke)
        run_remaining_connector runtime-smoke-envoy
        ;;
    traefik:minimal_runtime_smoke)
        run_remaining_connector runtime-smoke-traefik
        ;;
    lighttpd:minimal_runtime_smoke)
        run_remaining_connector runtime-smoke-lighttpd
        ;;
    envoy:no_crs_baseline)
        if [ "$NO_CRS_ARTIFACT_PROFILE" = full_lifecycle ]; then
            # run_remaining_connector execs: ext_proc must not fall through
            # into the ext_authz compatibility target.
            run_remaining_connector runtime-smoke-envoy-ext-proc
        else
            [ -n "${NO_CRS_SELECTED_CASES:-}" ] || {
                echo "$NO_CRS_SELECTED_CASES_MISSING_MESSAGE" >&2
                exit 1
            }
            run_remaining_connector no-crs-baseline-envoy
        fi
        ;;
    envoy:no_crs_with_mrts)
        run_remaining_connector runtime-smoke-envoy-ext-proc
        ;;
    traefik:no_crs_with_mrts)
        run_remaining_connector runtime-smoke-traefik-native
        ;;
    lighttpd:no_crs_with_mrts)
        run_remaining_connector runtime-smoke-lighttpd-patched
        ;;
    traefik:no_crs_baseline)
        if [ "$NO_CRS_ARTIFACT_PROFILE" = full_lifecycle ]; then
            # run_remaining_connector execs: this native local-plugin host
            # must not inherit forwardAuth compatibility evidence.
            run_remaining_connector runtime-smoke-traefik-native
        else
            [ -n "${NO_CRS_SELECTED_CASES:-}" ] || {
                echo "$NO_CRS_SELECTED_CASES_MISSING_MESSAGE" >&2
                exit 1
            }
            run_remaining_connector no-crs-baseline-traefik
        fi
        ;;
    lighttpd:no_crs_baseline)
        if [ "$NO_CRS_ARTIFACT_PROFILE" = full_lifecycle ]; then
            # run_remaining_connector execs: a patched native host may not
            # be replaced by the stock compatibility smoke.
            run_remaining_connector runtime-smoke-lighttpd-patched
        else
            [ -n "${NO_CRS_SELECTED_CASES:-}" ] || {
                echo "$NO_CRS_SELECTED_CASES_MISSING_MESSAGE" >&2
                exit 1
            }
            # These targets consume the plan before delegating to their narrow
            # real-host probes. They are deliberately distinct from the legacy
            # minimal-runtime targets: selected cases stay explicit in canonical
            # evidence instead of being implied by a 200/403 smoke.
            run_remaining_connector no-crs-baseline-lighttpd
        fi
        ;;
    *)
        echo "FAIL: unsupported connector stage dispatch: $connector:$stage" >&2
        exit 2
        ;;
esac
