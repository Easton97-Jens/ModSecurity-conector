#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
VERIFIED_RUN_ROOT="${VERIFIED_RUN_ROOT:-${RUNNER_TEMP:-${TMPDIR:-/var/tmp}}/ModSecurity-conector-verified}"
VERIFIED_BUILD_ROOT="${VERIFIED_BUILD_ROOT:-$VERIFIED_RUN_ROOT/build}"
BUILD_ROOT="${BUILD_ROOT:-$VERIFIED_BUILD_ROOT}"

CC_BIN="${CC:-cc}"
OUT_DIR="$BUILD_ROOT/common-helper-smoke"
SMOKE_C="$OUT_DIR/common_helper_smoke.c"
SMOKE_BIN="$OUT_DIR/common_helper_smoke"

case "$BUILD_ROOT" in
    /*) ;;
    *) echo "common_helper_smoke: BUILD_ROOT must be absolute: $BUILD_ROOT"; exit 77 ;;
esac

case "$(CDPATH= cd "$BUILD_ROOT" 2>/dev/null && pwd 2>/dev/null || printf '%s' "$BUILD_ROOT")" in
    "$REPO_ROOT"|"$REPO_ROOT"/*)
        echo "common_helper_smoke: BUILD_ROOT must not be inside the checkout: $BUILD_ROOT"
        exit 77
        ;;
esac

command -v "$CC_BIN" >/dev/null 2>&1 || {
    echo "common_helper_smoke: missing C compiler: $CC_BIN"
    exit 77
}

mkdir -p "$OUT_DIR"
cat > "$SMOKE_C" <<'EOF'
#include "msconnector/block_statuses.h"
#include "msconnector/blocking.h"
#include "msconnector/capabilities.h"
#include "msconnector/intervention.h"
#include "msconnector/origin.h"
#include "msconnector/rule_load_stats.h"
#include "msconnector/status.h"
#include "msconnector/transaction.h"

#include <assert.h>
#include <string.h>

int main(void) {
    msconnector_blocking_policy blocking_policy;
    msconnector_capabilities capabilities;
    msconnector_capability_flags flags = MSCONNECTOR_CAPABILITY_NONE;
    msconnector_intervention intervention;
    msconnector_origin origin;
    msconnector_decision decision;
    msconnector_rule_load_stats rule_stats = {1, 2, 3};
    msconnector_rule_load_stats added_stats = {4, 5, 6};

    assert(strcmp(msconnector_status_name(MSCONNECTOR_STATUS_OK), "ok") == 0);
    assert(strcmp(msconnector_status_name(MSCONNECTOR_STATUS_ERROR), "error") == 0);
    assert(strcmp(msconnector_status_name(MSCONNECTOR_STATUS_BLOCKED), "blocked") == 0);
    assert(strcmp(msconnector_status_name(MSCONNECTOR_STATUS_UNSUPPORTED), "unsupported") == 0);
    assert(msconnector_status_from_result("pass") == MSCONNECTOR_STATUS_OK);
    assert(msconnector_status_from_result("fail") == MSCONNECTOR_STATUS_ERROR);
    assert(msconnector_status_from_result("blocked") == MSCONNECTOR_STATUS_BLOCKED);
    assert(msconnector_status_from_result("not_executable") == MSCONNECTOR_STATUS_UNSUPPORTED);
    assert(msconnector_status_from_result("skipped") == MSCONNECTOR_STATUS_UNSUPPORTED);

    assert(MSCONNECTOR_DEFAULT_BLOCK_STATUS == 403);
    assert(MSCONNECTOR_DEFAULT_ERROR_STATUS == 500);
    assert(MSCONNECTOR_DEFAULT_UNSUPPORTED_STATUS == 501);
    assert(msconnector_http_status_is_valid(100));
    assert(msconnector_http_status_is_valid(599));
    assert(!msconnector_http_status_is_valid(99));
    assert(!msconnector_http_status_is_valid(600));
    assert(msconnector_block_status_is_allowed(403));
    assert(msconnector_block_status_is_allowed(501));
    assert(!msconnector_block_status_is_allowed(200));
    assert(msconnector_block_status_normalize(0) == 403);
    assert(msconnector_block_status_normalize(406) == 406);
    assert(msconnector_block_status_normalize(99) == 500);
    assert(msconnector_block_status_normalize(200) == 500);
    assert(strcmp(msconnector_http_status_name(403), "Forbidden") == 0);
    assert(strcmp(msconnector_http_status_name(501), "Not Implemented") == 0);
    assert(strcmp(msconnector_http_status_name(777), "Unknown") == 0);
    assert(strcmp(msconnector_block_action_name(MSCONNECTOR_BLOCK_ACTION_DENY), "deny") == 0);
    assert(strcmp(msconnector_block_action_name(MSCONNECTOR_BLOCK_ACTION_LOG_ONLY), "log_only") == 0);
    assert(msconnector_block_action_is_disruptive(MSCONNECTOR_BLOCK_ACTION_DENY));
    assert(!msconnector_block_action_is_disruptive(MSCONNECTOR_BLOCK_ACTION_LOG_ONLY));
    blocking_policy = msconnector_blocking_policy_make(MSCONNECTOR_BLOCK_ACTION_DENY, 406);
    assert(blocking_policy.status == 406);
    blocking_policy = msconnector_blocking_policy_make(MSCONNECTOR_BLOCK_ACTION_LOG_ONLY, 403);
    assert(blocking_policy.status == 0);

    intervention = msconnector_intervention_make(1, 403, 0, "blocked");
    assert(msconnector_intervention_is_disruptive(&intervention));
    assert(intervention.status == 403);
    intervention = msconnector_intervention_none();
    assert(!msconnector_intervention_is_disruptive(&intervention));
    assert(intervention.status == 0);
    decision = msconnector_decision_allow("allow", "allowed");
    assert(decision.status == MSCONNECTOR_STATUS_OK);
    assert(!msconnector_intervention_is_disruptive(&decision.intervention));
    assert(strcmp(decision.rule_id, "allow") == 0);
    assert(strcmp(decision.reason, "allowed") == 0);
    decision = msconnector_decision_block(403, "block", "blocked");
    assert(decision.status == MSCONNECTOR_STATUS_BLOCKED);
    assert(msconnector_intervention_is_disruptive(&decision.intervention));
    assert(decision.intervention.status == 403);

    origin = msconnector_origin_make(
        "apache",
        "https://github.com/owasp-modsecurity/ModSecurity-apache",
        "master",
        "0488c77",
        "v0.0.9-beta1",
        "Apache-2.0");
    assert(!msconnector_origin_is_empty(&origin));
    origin = msconnector_origin_make(0, 0, 0, 0, 0, 0);
    assert(msconnector_origin_is_empty(&origin));

    flags = msconnector_capabilities_add(flags, MSCONNECTOR_CAPABILITY_REQUEST_HEADERS);
    capabilities.flags = flags;
    capabilities.connector_name = "smoke";
    capabilities.connector_version = "test";
    capabilities.server_family = "none";
    capabilities.notes = "";
    assert(msconnector_capabilities_has(&capabilities, MSCONNECTOR_CAPABILITY_REQUEST_HEADERS));
    assert(!msconnector_capabilities_has(&capabilities, MSCONNECTOR_CAPABILITY_RESPONSE_HEADERS));
    assert(strcmp(msconnector_capability_name(MSCONNECTOR_CAPABILITY_REQUEST_HEADERS), "request-headers") == 0);
    assert(msconnector_capability_from_name("request-headers") == MSCONNECTOR_CAPABILITY_REQUEST_HEADERS);
    assert(strcmp(msconnector_capability_name(MSCONNECTOR_CAPABILITY_PHASE4_HARD_ABORT), "phase4-hard-abort") == 0);
    assert(msconnector_capability_from_name("phase4-hard-abort") == MSCONNECTOR_CAPABILITY_PHASE4_HARD_ABORT);
    assert(msconnector_capability_from_name("does-not-exist") == MSCONNECTOR_CAPABILITY_NONE);
    assert(rule_stats.inline_rules == 1);
    assert(rule_stats.file_rules == 2);
    assert(rule_stats.remote_rules == 3);
    msconnector_rule_load_stats_init(&rule_stats);
    assert(rule_stats.inline_rules == 0);
    assert(rule_stats.file_rules == 0);
    assert(rule_stats.remote_rules == 0);
    msconnector_rule_load_stats_add_inline(&rule_stats, 7);
    msconnector_rule_load_stats_add_file(&rule_stats, 8);
    msconnector_rule_load_stats_add_remote(&rule_stats, 9);
    assert(rule_stats.inline_rules == 7);
    assert(rule_stats.file_rules == 8);
    assert(rule_stats.remote_rules == 9);
    msconnector_rule_load_stats_add(&rule_stats, &added_stats);
    assert(rule_stats.inline_rules == 11);
    assert(rule_stats.file_rules == 13);
    assert(rule_stats.remote_rules == 15);
    return 0;
}
EOF

"$CC_BIN" -std=c99 -Wall -Wextra -Werror \
    -I "$REPO_ROOT/common/include" \
    "$REPO_ROOT/common/src/status.c" \
    "$REPO_ROOT/common/src/block_statuses.c" \
    "$REPO_ROOT/common/src/blocking.c" \
    "$REPO_ROOT/common/src/intervention.c" \
    "$REPO_ROOT/common/src/origin.c" \
    "$REPO_ROOT/common/src/capabilities.c" \
    "$REPO_ROOT/common/src/transaction.c" \
    "$SMOKE_C" \
    -o "$SMOKE_BIN"

"$SMOKE_BIN"
echo "common_helper_smoke: pass output=$OUT_DIR"
