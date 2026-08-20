#!/bin/sh
set -eu

connector=${1:?connector is required}
target=${2:?target is required}

SCRIPT_DIR=$(CDPATH='' cd "$(dirname "$0")" && pwd)
CONNECTOR_ROOT=${CONNECTOR_ROOT:-$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)}
FRAMEWORK_ROOT=${FRAMEWORK_ROOT:-$CONNECTOR_ROOT/modules/ModSecurity-test-Framework}
VERIFIED_RUN_ROOT=${VERIFIED_RUN_ROOT:-${RUNNER_TEMP:-${TMPDIR:-/var/tmp}}/ModSecurity-conector-verified}
BUILD_ROOT=${BUILD_ROOT:-$VERIFIED_RUN_ROOT/build}
CACHE_ROOT=${CACHE_ROOT:-$VERIFIED_RUN_ROOT/cache-v2}
CONNECTOR_COMPONENT_CACHE=${CONNECTOR_COMPONENT_CACHE:-${VERIFIED_COMPONENT_CACHE:-$CACHE_ROOT/shared}}
TMP_ROOT=${TMP_ROOT:-$BUILD_ROOT/tmp}
RUNTIME_REPORT_OUTPUT_ROOT=${RUNTIME_REPORT_OUTPUT_ROOT:-$BUILD_ROOT/runtime-component-reports}
RUNTIME_COMPONENT_TARGET=${RUNTIME_COMPONENT_TARGET:-shared}
resolved_component_cache=$CONNECTOR_COMPONENT_CACHE
requested_component_target=$RUNTIME_COMPONENT_TARGET

validate_mrts_direct_invocation() {
    case "$connector:$target" in
        envoy:runtime-smoke-envoy-ext-proc|traefik:runtime-smoke-traefik-native|lighttpd:runtime-smoke-lighttpd-patched) ;;
        *) echo "FAIL: no_crs_with_mrts target is not an approved real-host route: $connector:$target" >&2; exit 2 ;;
    esac
    [ "${MSCONNECTOR_MRTS_RUNTIME:-}" = 1 ] || { echo "FAIL: no_crs_with_mrts requires MSCONNECTOR_MRTS_RUNTIME=1" >&2; exit 2; }
    [ "${ALLOW_RUNTIME_DOWNLOADS:-}" = 1 ] && [ "${ALLOW_RUNTIME_BUILDS:-}" = 1 ] || {
        echo "FAIL: no_crs_with_mrts requires explicit ALLOW_RUNTIME_DOWNLOADS=1 and ALLOW_RUNTIME_BUILDS=1" >&2
        exit 77
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
        "$CONNECTOR_ROOT"/*:*|*:"$CONNECTOR_ROOT"/*) echo "FAIL: MRTS plan/result must be outside the checkout" >&2; exit 77 ;;
    esac
    case "$MRTS_RUNTIME_PLAN:$MRTS_RUNTIME_RESULT" in
        "$VERIFIED_RUN_ROOT"/*:*|*:"$VERIFIED_RUN_ROOT"/*) ;;
        *) echo "FAIL: MRTS plan/result must remain under the private runtime root" >&2; exit 77 ;;
    esac
    case "$MRTS_LOAD_FILE" in
        "$VERIFIED_RUN_ROOT"/*) ;;
        *) echo "FAIL: MRTS_LOAD_FILE must remain under the private runtime root" >&2; exit 77 ;;
    esac
    case "$MRTS_CASE_ROOT" in
        "$VERIFIED_RUN_ROOT"/*) ;;
        *) echo "FAIL: MRTS_CASE_ROOT must remain under the private runtime root" >&2; exit 77 ;;
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
    if [ "$connector" = traefik ]; then
        [ "${GOTOOLCHAIN:-}" = local ] || { echo "FAIL: Traefik MRTS runtime requires GOTOOLCHAIN=local" >&2; exit 77; }
        [ "${GO:-}" = /usr/local/go/bin/go ] || { echo "FAIL: Traefik MRTS runtime requires the trusted direct Go binary" >&2; exit 77; }
        [ -x /usr/local/go/bin/go ] || { echo "FAIL: trusted direct Go binary is unavailable" >&2; exit 77; }
    fi
}

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

if [ "${MSCONNECTOR_MRTS_STAGE:-}" = no_crs_with_mrts ]; then
    validate_mrts_direct_invocation
    # Direct callers cannot use inherited component, selector, or artifact
    # paths. The closed dispatcher supplies these values from the verified
    # component snapshot below.
    unset RULES_FILE MSCONNECTOR_RULES_FILE NO_CRS_RULES_FILE MODSECURITY_RULE_PREAMBLE_FILE
    unset ENVOY_BIN ENVOY_COMPONENT_ROOT ENVOY_SOURCE_ROOT ENVOY_BUILD_ROOT
    unset TRAEFIK_BIN TRAEFIK_COMPONENT_ROOT TRAEFIK_SOURCE_ROOT TRAEFIK_BUILD_ROOT TRAEFIK_ARCHIVE
    unset LIGHTTPD_BIN LIGHTTPD_COMPONENT_ROOT LIGHTTPD_SOURCE_DIR LIGHTTPD_BUILD_ROOT
    unset LIGHTTPD_INCLUDE_DIR LIGHTTPD_CONNECTOR_BUILD_ROOT LIGHTTPD_MODULE_DIR
    unset ENVOY_EXT_PROC_RUNTIME_ROOT ENVOY_RESULT_ROOT TRAEFIK_NATIVE_RUNTIME_ROOT TRAEFIK_RESULT_ROOT
    unset LIGHTTPD_PATCHED_ROOT LIGHTTPD_PATCHED_SMOKE_DIR
    prepare_mrts_toolchain_roots
    RUNTIME_ROOT=$BUILD_ROOT/stages/$connector/no_crs_with_mrts/runtime
    RUNTIME_BASE=$RUNTIME_ROOT
    NO_CRS_BASELINE=1
    MODSECURITY_TEST_VARIANT=no-crs
    MODSECURITY_MRTS_VARIANT=with-mrts
    MSCONNECTOR_RULES_FILE=$MRTS_LOAD_FILE
    NO_CRS_RULES_FILE=$MRTS_LOAD_FILE
    RULES_FILE=$MRTS_LOAD_FILE
    MODSECURITY_RULE_PREAMBLE_FILE=$MRTS_LOAD_FILE
    GO=/usr/local/go/bin/go
    GOTOOLCHAIN=local
    PYTHON=$MRTS_PYTHON_BIN
    PYTHON_BIN=$MRTS_PYTHON_BIN
    PATH=/usr/local/go/bin:/usr/bin:/bin
    HOME=$MRTS_HOME
    XDG_CACHE_HOME=$MRTS_XDG_CACHE_HOME
    GOPATH=$MRTS_GOPATH
    GOMODCACHE=$MRTS_GOMODCACHE
    GOCACHE=$MRTS_GOCACHE
    GOTMPDIR=$MRTS_GOTMPDIR
    TMPDIR=$MRTS_TMPDIR
    GOENV=off
    ALLOW_RUNTIME_DOWNLOADS=1
    ALLOW_RUNTIME_BUILDS=1
    MRTS_CLOSED_CONNECTOR_ROOT=$CONNECTOR_ROOT
    MRTS_CLOSED_FRAMEWORK_ROOT=$FRAMEWORK_ROOT
    MRTS_CLOSED_VERIFIED_RUN_ROOT=$VERIFIED_RUN_ROOT
    MRTS_CLOSED_BUILD_ROOT=$BUILD_ROOT
    MRTS_CLOSED_CACHE_ROOT=$CACHE_ROOT
    MRTS_CLOSED_TMP_ROOT=$TMP_ROOT
    MRTS_CLOSED_LOG_ROOT=$LOG_ROOT
    MRTS_CLOSED_RESULTS_DIR=$RESULTS_DIR
    MRTS_CLOSED_RUNTIME_ROOT=$RUNTIME_ROOT
    MRTS_CLOSED_RUNTIME_BASE=$RUNTIME_BASE
    MRTS_CLOSED_RUNTIME_REPORT_OUTPUT_ROOT=$RUNTIME_REPORT_OUTPUT_ROOT
    MRTS_CLOSED_COMPONENT_TARGET=$requested_component_target
    MRTS_CLOSED_COMPONENT_CACHE=$resolved_component_cache
    MRTS_CLOSED_STAGE=$MSCONNECTOR_MRTS_STAGE
    MRTS_CLOSED_PATH=$PATH
    MRTS_CLOSED_GO=$GO
    MRTS_CLOSED_GOTOOLCHAIN=$GOTOOLCHAIN
    MRTS_CLOSED_PYTHON=$PYTHON
    MRTS_CLOSED_HOME=$HOME
    MRTS_CLOSED_XDG_CACHE_HOME=$XDG_CACHE_HOME
    MRTS_CLOSED_GOPATH=$GOPATH
    MRTS_CLOSED_GOMODCACHE=$GOMODCACHE
    MRTS_CLOSED_GOCACHE=$GOCACHE
    MRTS_CLOSED_GOTMPDIR=$GOTMPDIR
    MRTS_CLOSED_TMPDIR=$TMPDIR
    MRTS_CLOSED_GOENV=$GOENV
    MRTS_CLOSED_ALLOW_RUNTIME_DOWNLOADS=1
    MRTS_CLOSED_ALLOW_RUNTIME_BUILDS=1
    MRTS_CLOSED_PLAN=$MRTS_RUNTIME_PLAN
    MRTS_CLOSED_RESULT=$MRTS_RUNTIME_RESULT
    MRTS_CLOSED_EXECUTOR=$MRTS_RUNTIME_EXECUTOR
    MRTS_CLOSED_EXECUTOR_SHA256=$MRTS_RUNTIME_EXECUTOR_SHA256
    MRTS_CLOSED_RULES_ROOT=$MRTS_RUNTIME_RULES_ROOT
    MRTS_CLOSED_LOAD_FILE=$MRTS_LOAD_FILE
    MRTS_CLOSED_CASE_ROOT=$MRTS_CASE_ROOT
    readonly MRTS_CLOSED_CONNECTOR_ROOT MRTS_CLOSED_FRAMEWORK_ROOT MRTS_CLOSED_VERIFIED_RUN_ROOT MRTS_CLOSED_BUILD_ROOT MRTS_CLOSED_CACHE_ROOT MRTS_CLOSED_TMP_ROOT MRTS_CLOSED_LOG_ROOT MRTS_CLOSED_RESULTS_DIR MRTS_CLOSED_RUNTIME_ROOT MRTS_CLOSED_RUNTIME_BASE MRTS_CLOSED_RUNTIME_REPORT_OUTPUT_ROOT MRTS_CLOSED_COMPONENT_TARGET MRTS_CLOSED_COMPONENT_CACHE MRTS_CLOSED_STAGE MRTS_CLOSED_PATH MRTS_CLOSED_GO MRTS_CLOSED_GOTOOLCHAIN MRTS_CLOSED_PYTHON MRTS_CLOSED_HOME MRTS_CLOSED_XDG_CACHE_HOME MRTS_CLOSED_GOPATH MRTS_CLOSED_GOMODCACHE MRTS_CLOSED_GOCACHE MRTS_CLOSED_GOTMPDIR MRTS_CLOSED_TMPDIR MRTS_CLOSED_GOENV MRTS_CLOSED_ALLOW_RUNTIME_DOWNLOADS MRTS_CLOSED_ALLOW_RUNTIME_BUILDS MRTS_CLOSED_PLAN MRTS_CLOSED_RESULT MRTS_CLOSED_EXECUTOR MRTS_CLOSED_EXECUTOR_SHA256 MRTS_CLOSED_RULES_ROOT MRTS_CLOSED_LOAD_FILE MRTS_CLOSED_CASE_ROOT
    export RUNTIME_ROOT RUNTIME_BASE NO_CRS_BASELINE MODSECURITY_TEST_VARIANT MODSECURITY_MRTS_VARIANT MRTS_LOAD_FILE MRTS_CASE_ROOT MRTS_RUNTIME_EXECUTOR_SHA256 MSCONNECTOR_RULES_FILE NO_CRS_RULES_FILE RULES_FILE MODSECURITY_RULE_PREAMBLE_FILE GO GOTOOLCHAIN PYTHON PYTHON_BIN HOME XDG_CACHE_HOME GOPATH GOMODCACHE GOCACHE GOTMPDIR TMPDIR GOENV ALLOW_RUNTIME_DOWNLOADS ALLOW_RUNTIME_BUILDS
fi

export CONNECTOR_ROOT FRAMEWORK_ROOT VERIFIED_RUN_ROOT BUILD_ROOT CACHE_ROOT CONNECTOR_COMPONENT_CACHE TMP_ROOT
export RUNTIME_REPORT_OUTPUT_ROOT RUNTIME_COMPONENT_TARGET

case "${PYTHON:-python3}" in
    /*) ;;
    */*) PYTHON="$CONNECTOR_ROOT/${PYTHON}" ;;
    *) PYTHON=${PYTHON:-python3} ;;
esac
export PYTHON

[ -f "$FRAMEWORK_ROOT/ci/lib/common.sh" ] || {
    echo "FAIL: framework common.sh is missing" >&2
    exit 1
}

# shellcheck disable=SC1091 # FRAMEWORK_ROOT is a validated exact Parent gitlink path resolved at runtime.
. "$FRAMEWORK_ROOT/ci/lib/common.sh"
assert_safe_runtime_path "$RUNTIME_REPORT_OUTPUT_ROOT" RUNTIME_REPORT_OUTPUT_ROOT || exit 77
assert_not_system_path_for_write "$RUNTIME_REPORT_OUTPUT_ROOT" RUNTIME_REPORT_OUTPUT_ROOT || exit 77

if [ -z "${RUNTIME_COMPONENT_ENV_SNAPSHOT:-}" ]; then
    RUNTIME_COMPONENT_ENV_SNAPSHOT=$(sh "$CONNECTOR_ROOT/ci/runtime/lifecycle/reserve-runtime-env-snapshot.sh" "$RUNTIME_REPORT_OUTPUT_ROOT") || exit $?
    snapshot_reserved_here=1
else
    snapshot_reserved_here=0
fi
runtime_env=$RUNTIME_COMPONENT_ENV_SNAPSHOT
case "$runtime_env" in
    "$RUNTIME_REPORT_OUTPUT_ROOT"/*) ;;
    *)
        echo "FAIL: runtime environment snapshot must remain under RUNTIME_REPORT_OUTPUT_ROOT: $runtime_env" >&2
        exit 1
        ;;
esac
if [ "${MSCONNECTOR_MRTS_STAGE:-}" = no_crs_with_mrts ]; then
    MRTS_CLOSED_RUNTIME_ENV=$runtime_env
    readonly MRTS_CLOSED_RUNTIME_ENV
fi
export RUNTIME_COMPONENT_ENV_SNAPSHOT

ensure_runtime_env_snapshot() {
    if [ -s "$runtime_env" ]; then
        return 0
    fi
    # A SKIP_RUNTIME_COMPONENT_PREPARE caller may reuse an inherited snapshot,
    # but it may not fall back to the mutable shared runtime-env.sh.  Materialize
    # a target-bound local snapshot when none was supplied.
    set +e
    sh "$CONNECTOR_ROOT/ci/provisioning/components/prepare-runtime-components.sh"
    prepare_rc=$?
    set -e
    if [ "$prepare_rc" -ne 0 ]; then
        if [ "$snapshot_reserved_here" -eq 1 ]; then
            rm -f "$runtime_env"
        fi
        return "$prepare_rc"
    fi
    [ -s "$runtime_env" ] || {
        echo "FAIL: runtime component preparation did not publish an invocation-local environment snapshot: $runtime_env" >&2
        return 1
    }
}

load_runtime_env() {
    [ -s "$runtime_env" ] || {
        echo "FAIL: runtime environment snapshot is missing: $runtime_env" >&2
        return 1
    }
    [ ! -L "$runtime_env" ] || {
        echo "FAIL: runtime environment snapshot must not be a symlink: $runtime_env" >&2
        return 1
    }
    # shellcheck disable=SC1090
    . "$runtime_env"
    if [ "${MRTS_CLOSED_STAGE:-}" = no_crs_with_mrts ]; then
        runtime_env=$MRTS_CLOSED_RUNTIME_ENV
        RUNTIME_COMPONENT_ENV_SNAPSHOT=$MRTS_CLOSED_RUNTIME_ENV
        requested_component_target=$MRTS_CLOSED_COMPONENT_TARGET
        resolved_component_cache=$MRTS_CLOSED_COMPONENT_CACHE
    fi
    case "$requested_component_target:${RUNTIME_COMPONENT_ENV_SNAPSHOT_TARGET:-}" in
        shared:shared|shared:all|all:all|apache:apache|nginx:nginx|haproxy:haproxy) ;;
        *)
            echo "FAIL: runtime environment snapshot target mismatch: requested=$requested_component_target snapshot=${RUNTIME_COMPONENT_ENV_SNAPSHOT_TARGET:-unset}" >&2
            return 1
            ;;
    esac
    if [ "${RUNTIME_COMPONENT_ENV_SNAPSHOT_CACHE:-}" != "$resolved_component_cache" ]; then
        echo "FAIL: runtime environment snapshot cache mismatch: expected=$resolved_component_cache snapshot=${RUNTIME_COMPONENT_ENV_SNAPSHOT_CACHE:-unset}" >&2
        return 1
    fi
    # A generated environment may carry useful toolchain paths, but it never
    # gets to redirect this invocation away from its Cache-v2 shared root.
    CONNECTOR_COMPONENT_CACHE=$resolved_component_cache
    VERIFIED_COMPONENT_CACHE=$resolved_component_cache
    RUNTIME_COMPONENT_ENV_SNAPSHOT=$runtime_env
    RUNTIME_COMPONENT_TARGET=$requested_component_target
    export CACHE_ROOT VERIFIED_COMPONENT_CACHE CONNECTOR_COMPONENT_CACHE
    export RUNTIME_COMPONENT_ENV_SNAPSHOT RUNTIME_COMPONENT_TARGET
    reassert_mrts_closed_environment
}

reassert_mrts_closed_environment() {
    [ "${MRTS_CLOSED_STAGE:-}" = no_crs_with_mrts ] || return 0
    CONNECTOR_ROOT=$MRTS_CLOSED_CONNECTOR_ROOT
    FRAMEWORK_ROOT=$MRTS_CLOSED_FRAMEWORK_ROOT
    VERIFIED_RUN_ROOT=$MRTS_CLOSED_VERIFIED_RUN_ROOT
    BUILD_ROOT=$MRTS_CLOSED_BUILD_ROOT
    CACHE_ROOT=$MRTS_CLOSED_CACHE_ROOT
    TMP_ROOT=$MRTS_CLOSED_TMP_ROOT
    LOG_ROOT=$MRTS_CLOSED_LOG_ROOT
    RESULTS_DIR=$MRTS_CLOSED_RESULTS_DIR
    RUNTIME_ROOT=$MRTS_CLOSED_RUNTIME_ROOT
    RUNTIME_BASE=$MRTS_CLOSED_RUNTIME_BASE
    RUNTIME_REPORT_OUTPUT_ROOT=$MRTS_CLOSED_RUNTIME_REPORT_OUTPUT_ROOT
    PATH=$MRTS_CLOSED_PATH
    GO=$MRTS_CLOSED_GO
    GOTOOLCHAIN=$MRTS_CLOSED_GOTOOLCHAIN
    PYTHON=$MRTS_CLOSED_PYTHON
    PYTHON_BIN=$MRTS_CLOSED_PYTHON
    HOME=$MRTS_CLOSED_HOME
    XDG_CACHE_HOME=$MRTS_CLOSED_XDG_CACHE_HOME
    GOPATH=$MRTS_CLOSED_GOPATH
    GOMODCACHE=$MRTS_CLOSED_GOMODCACHE
    GOCACHE=$MRTS_CLOSED_GOCACHE
    GOTMPDIR=$MRTS_CLOSED_GOTMPDIR
    TMPDIR=$MRTS_CLOSED_TMPDIR
    GOENV=$MRTS_CLOSED_GOENV
    ALLOW_RUNTIME_DOWNLOADS=$MRTS_CLOSED_ALLOW_RUNTIME_DOWNLOADS
    ALLOW_RUNTIME_BUILDS=$MRTS_CLOSED_ALLOW_RUNTIME_BUILDS
    MRTS_RUNTIME_PLAN=$MRTS_CLOSED_PLAN
    MRTS_RUNTIME_RESULT=$MRTS_CLOSED_RESULT
    MRTS_RUNTIME_EXECUTOR=$MRTS_CLOSED_EXECUTOR
    MRTS_RUNTIME_EXECUTOR_SHA256=$MRTS_CLOSED_EXECUTOR_SHA256
    MRTS_RUNTIME_RULES_ROOT=$MRTS_CLOSED_RULES_ROOT
    MRTS_LOAD_FILE=$MRTS_CLOSED_LOAD_FILE
    MRTS_CASE_ROOT=$MRTS_CLOSED_CASE_ROOT
    MSCONNECTOR_MRTS_STAGE=$MRTS_CLOSED_STAGE
    MSCONNECTOR_MRTS_RUNTIME=1
    NO_CRS_BASELINE=1
    MODSECURITY_TEST_VARIANT=no-crs
    MODSECURITY_MRTS_VARIANT=with-mrts
    MSCONNECTOR_RULES_FILE=$MRTS_LOAD_FILE
    NO_CRS_RULES_FILE=$MRTS_LOAD_FILE
    RULES_FILE=$MRTS_LOAD_FILE
    MODSECURITY_RULE_PREAMBLE_FILE=$MRTS_LOAD_FILE
    prepare_mrts_toolchain_roots
    [ "$GO" = /usr/local/go/bin/go ] && [ "$GOTOOLCHAIN" = local ] && [ "$GOENV" = off ] || {
        echo "FAIL: MRTS Go toolchain controls were not preserved after runtime snapshot load" >&2
        return 77
    }
    [ "$PYTHON" = "$MRTS_CLOSED_PYTHON" ] && [ "$PYTHON_BIN" = "$MRTS_CLOSED_PYTHON" ] || {
        echo "FAIL: MRTS Python toolchain controls were not preserved after runtime snapshot load" >&2
        return 77
    }
    [ -f "$PYTHON_BIN" ] && [ -x "$PYTHON_BIN" ] && [ ! -L "$PYTHON_BIN" ] || {
        echo "FAIL: MRTS Python interpreter is invalid after runtime snapshot load" >&2
        return 77
    }
    [ -x "$GO" ] || {
        echo "FAIL: trusted Go binary is unavailable after runtime snapshot load" >&2
        return 77
    }
    export CONNECTOR_ROOT FRAMEWORK_ROOT VERIFIED_RUN_ROOT BUILD_ROOT CACHE_ROOT TMP_ROOT LOG_ROOT RESULTS_DIR RUNTIME_ROOT RUNTIME_BASE RUNTIME_REPORT_OUTPUT_ROOT PATH GO GOTOOLCHAIN PYTHON PYTHON_BIN HOME XDG_CACHE_HOME GOPATH GOMODCACHE GOCACHE GOTMPDIR TMPDIR GOENV ALLOW_RUNTIME_DOWNLOADS ALLOW_RUNTIME_BUILDS MRTS_RUNTIME_PLAN MRTS_RUNTIME_RESULT MRTS_RUNTIME_EXECUTOR MRTS_RUNTIME_EXECUTOR_SHA256 MRTS_RUNTIME_RULES_ROOT MRTS_LOAD_FILE MRTS_CASE_ROOT MSCONNECTOR_MRTS_STAGE MSCONNECTOR_MRTS_RUNTIME NO_CRS_BASELINE MODSECURITY_TEST_VARIANT MODSECURITY_MRTS_VARIANT MSCONNECTOR_RULES_FILE NO_CRS_RULES_FILE RULES_FILE MODSECURITY_RULE_PREAMBLE_FILE
}

run_make_target() {
    mkdir -p "$TMP_ROOT"
    make_log=$(mktemp "$TMP_ROOT/remaining-connector-make.XXXXXX")
    set +e
    make "$@" >"$make_log" 2>&1
    make_rc=$?
    set -e
    cat "$make_log"
    if [ "$make_rc" -eq 2 ] \
        && grep -Eq '(^|:)[[:space:]]*\*\*\*.*Error 77' "$make_log" \
        && grep -q 'BLOCKED:' "$make_log" \
        && ! grep -q '^FAIL:' "$make_log"; then
        rm -f "$make_log"
        return 77
    fi
    rm -f "$make_log"
    return "$make_rc"
}

require_modsecurity_build_environment() {
    ensure_runtime_env_snapshot || return $?
    load_runtime_env
    if [ -f "${MODSECURITY_INCLUDE_DIR:-}/modsecurity/modsecurity.h" ] \
        && [ -d "${MODSECURITY_LIB_DIR:-}" ]; then
        return 0
    fi
    if [ "${SKIP_RUNTIME_COMPONENT_PREPARE:-0}" = "1" ]; then
        echo "FAIL: libmodsecurity build environment is missing and preparation is disabled" >&2
        return 1
    fi
    env PYTHON="${PYTHON:-python3}" FRAMEWORK_ROOT="$FRAMEWORK_ROOT" CONNECTOR_ROOT="$CONNECTOR_ROOT" \
        sh "$CONNECTOR_ROOT/ci/provisioning/components/prepare-runtime-components.sh"
    ensure_runtime_env_snapshot || return $?
    load_runtime_env
    if [ ! -f "${MODSECURITY_INCLUDE_DIR:-}/modsecurity/modsecurity.h" ] \
        || [ ! -d "${MODSECURITY_LIB_DIR:-}" ]; then
        echo "FAIL: runtime preparation did not provide libmodsecurity headers and libraries" >&2
        return 1
    fi
}

require_host=0
case "$target" in
    start-smoke-*|runtime-smoke-*|no-crs-baseline-*) require_host=1 ;;
    *) ;;
esac

require_modsecurity_build_environment

case "$connector" in
    envoy)
        envoy_build_paths >/dev/null
        if [ "$require_host" = "1" ]; then
            ENVOY_BIN=$(require_or_provision_envoy)
            export ENVOY_BIN
        fi
        if [ "${MSCONNECTOR_MRTS_STAGE:-}" = no_crs_with_mrts ]; then
            ext_proc_runtime_root=$RUNTIME_ROOT
        else
            ext_proc_runtime_root=${PARENT_HOST_RUNTIME_ROOT:-${ENVOY_EXT_PROC_RUNTIME_ROOT:-${ENVOY_RESULT_ROOT:-${RUNTIME_ROOT:-$BUILD_ROOT/envoy-ext-proc/runtime-smoke}}}}
        fi
        ext_proc_event_log=${ENVOY_EXT_PROC_EVENT_LOG_PATH:-$ext_proc_runtime_root/events.jsonl}
        run_make_target -C "$CONNECTOR_ROOT/connectors/envoy" "$target" \
            BUILD_ROOT="$BUILD_ROOT" ENVOY_BIN="$ENVOY_BIN" \
            EXT_PROC_RUNTIME_ROOT="$ext_proc_runtime_root" \
            EXT_PROC_RUNTIME_EVENT_LOG_PATH="$ext_proc_event_log" \
            MODSECURITY_INCLUDE_DIR="$MODSECURITY_INCLUDE_DIR" \
            MODSECURITY_LIB_DIR="$MODSECURITY_LIB_DIR" \
            MODSECURITY_PREFIX="${MODSECURITY_PREFIX:-}"
        ;;
    traefik)
        traefik_build_paths >/dev/null
        if [ "$require_host" = "1" ]; then
            TRAEFIK_BIN=$(require_or_provision_traefik)
            export TRAEFIK_BIN
        fi
        if [ "${MSCONNECTOR_MRTS_STAGE:-}" = no_crs_with_mrts ]; then
            traefik_native_runtime_root=$RUNTIME_ROOT
        else
            traefik_native_runtime_root=${PARENT_HOST_RUNTIME_ROOT:-${TRAEFIK_NATIVE_RUNTIME_ROOT:-${TRAEFIK_RESULT_ROOT:-${RUNTIME_ROOT:-$BUILD_ROOT/traefik-native-middleware/runtime-smoke}}}}
        fi
        TRAEFIK_NATIVE_RUNTIME_ROOT=$traefik_native_runtime_root
        MODSECURITY_PREFIX=${MODSECURITY_PREFIX:-}
        export TRAEFIK_BIN TRAEFIK_NATIVE_RUNTIME_ROOT
        export MODSECURITY_INCLUDE_DIR MODSECURITY_LIB_DIR MODSECURITY_PREFIX
        run_make_target -C "$CONNECTOR_ROOT/connectors/traefik" "$target"
        ;;
    lighttpd)
        lighttpd_build_paths >/dev/null
        LIGHTTPD_BIN=$(require_or_provision_lighttpd)
        export LIGHTTPD_BIN LIGHTTPD_SOURCE_DIR LIGHTTPD_BUILD_ROOT
        export LIGHTTPD_INCLUDE_DIR LIGHTTPD_CONNECTOR_BUILD_ROOT LIGHTTPD_MODULE_DIR
        if [ "${MSCONNECTOR_MRTS_STAGE:-}" = no_crs_with_mrts ]; then
            lighttpd_patched_root=$BUILD_ROOT/lighttpd-core-patched
            lighttpd_patched_smoke_dir=$RUNTIME_ROOT
        else
            lighttpd_patched_root=${LIGHTTPD_PATCHED_ROOT:-$BUILD_ROOT/lighttpd-core-patched}
            lighttpd_patched_smoke_dir=${PARENT_HOST_RUNTIME_ROOT:-${LIGHTTPD_PATCHED_SMOKE_DIR:-${RUNTIME_ROOT:-$BUILD_ROOT/lighttpd-patched-smoke}}}
        fi
        run_make_target -C "$CONNECTOR_ROOT/connectors/lighttpd" "$target" \
            BUILD_ROOT="$BUILD_ROOT" LIGHTTPD_BIN="$LIGHTTPD_BIN" \
            LIGHTTPD_SOURCE_DIR="$LIGHTTPD_SOURCE_DIR" \
            LIGHTTPD_BUILD_ROOT="$LIGHTTPD_BUILD_ROOT" \
            LIGHTTPD_INCLUDE_DIR="$LIGHTTPD_INCLUDE_DIR" \
            LIGHTTPD_CONNECTOR_BUILD_ROOT="$LIGHTTPD_CONNECTOR_BUILD_ROOT" \
            LIGHTTPD_MODULE_DIR="$LIGHTTPD_MODULE_DIR" \
            LIGHTTPD_PATCHED_ROOT="$lighttpd_patched_root" \
            LIGHTTPD_PATCHED_SMOKE_DIR="$lighttpd_patched_smoke_dir" \
            MODSECURITY_INCLUDE_DIR="$MODSECURITY_INCLUDE_DIR" \
            MODSECURITY_LIB_DIR="$MODSECURITY_LIB_DIR" \
            MODSECURITY_PREFIX="${MODSECURITY_PREFIX:-}"
        ;;
    *)
        echo "usage: $0 envoy|traefik|lighttpd target" >&2
        exit 2
        ;;
esac
