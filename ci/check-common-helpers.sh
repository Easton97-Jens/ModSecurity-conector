#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
VERIFIED_RUN_ROOT="${VERIFIED_RUN_ROOT:-${RUNNER_TEMP:-${TMPDIR:-/var/tmp}}/ModSecurity-conector-verified}"
VERIFIED_BUILD_ROOT="${VERIFIED_BUILD_ROOT:-$VERIFIED_RUN_ROOT/build}"
BUILD_ROOT="${BUILD_ROOT:-$VERIFIED_BUILD_ROOT}"

CC_BIN="${CC:-cc}"
MSCONNECTOR_C_STD="${MSCONNECTOR_C_STD:-c17}"
MSCONNECTOR_CFLAGS="${MSCONNECTOR_CFLAGS:--std=$MSCONNECTOR_C_STD -Wall -Wextra -Werror}"
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
#include "msconnector/adapter_metadata.h"
#include "msconnector/artifacts.h"
#include "msconnector/body_policy.h"
#include "msconnector/config.h"
#include "msconnector/decision_action.h"
#include "msconnector/directive_spec.h"
#include "msconnector/directives.h"
#include "msconnector/event.h"
#include "msconnector/headers.h"
#include "msconnector/http_status.h"
#include "msconnector/json_escape.h"
#include "msconnector/late_intervention.h"
#include "msconnector/lifecycle_status.h"
#include "msconnector/path_policy.h"
#include "msconnector/redaction.h"
#include "msconnector/test_result.h"
#include "msconnector/transaction_state.h"

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
    {
        const struct {
            int status;
            const char *reason;
        } status_reasons[] = {
            {400, "Bad Request"},
            {401, "Unauthorized"},
            {403, "Forbidden"},
            {404, "Not Found"},
            {405, "Method Not Allowed"},
            {406, "Not Acceptable"},
            {408, "Request Timeout"},
            {409, "Conflict"},
            {410, "Gone"},
            {413, "Payload Too Large"},
            {415, "Unsupported Media Type"},
            {418, "I'm a teapot"},
            {422, "Unprocessable Content"},
            {425, "Too Early"},
            {429, "Too Many Requests"},
            {451, "Unavailable For Legal Reasons"},
            {500, "Internal Server Error"},
            {501, "Not Implemented"},
            {502, "Bad Gateway"},
            {503, "Service Unavailable"},
            {504, "Gateway Timeout"}
        };
        size_t index;

        for (index = 0; index < sizeof(status_reasons) / sizeof(status_reasons[0]); ++index) {
            assert(strcmp(msconnector_http_status_reason_phrase(status_reasons[index].status),
                status_reasons[index].reason) == 0);
            assert(msconnector_http_status_is_block_response(status_reasons[index].status));
        }
    }
    assert(strcmp(msconnector_http_status_default_message(403), "Request blocked") == 0);
    assert(strcmp(msconnector_http_status_default_message(500), "Internal error") == 0);
    assert(strcmp(msconnector_http_status_default_message(501), "Requested capability is not implemented") == 0);
    assert(strcmp(msconnector_http_status_default_message(503), "Service unavailable") == 0);
    assert(!msconnector_http_status_is_valid(99));
    assert(!msconnector_http_status_is_valid(600));
    assert(strcmp(msconnector_http_status_reason_phrase(99), "Invalid Status") == 0);
    assert(strcmp(msconnector_http_status_default_message(99), "Invalid HTTP status") == 0);
    assert(strcmp(msconnector_http_status_reason_phrase(299), "Unknown Status") == 0);
    assert(strcmp(msconnector_http_status_default_message(299), "HTTP status") == 0);
    assert(msconnector_http_status_classify(403) == MSCONNECTOR_HTTP_STATUS_CLASS_CLIENT_ERROR);
    assert(msconnector_http_status_classify(500) == MSCONNECTOR_HTTP_STATUS_CLASS_SERVER_ERROR);
    assert(msconnector_http_status_classify(302) == MSCONNECTOR_HTTP_STATUS_CLASS_REDIRECTION);
    assert(msconnector_http_status_classify(599) == MSCONNECTOR_HTTP_STATUS_CLASS_SERVER_ERROR);
    assert(msconnector_http_status_classify(99) == MSCONNECTOR_HTTP_STATUS_CLASS_UNKNOWN);
    assert(msconnector_http_status_classify(600) == MSCONNECTOR_HTTP_STATUS_CLASS_UNKNOWN);
    assert(msconnector_http_status_is_error(500));
    assert(!msconnector_http_status_is_block_response(299));
    assert(!msconnector_http_status_is_block_response(99));
    assert(!msconnector_http_status_is_block_response(200));
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


    {
        msconnector_config parent_config;
        msconnector_config child_config;
        msconnector_config merged_config;
        char error[64];
        msconnector_config_init(&parent_config);
        msconnector_config_init(&child_config);
        parent_config.enable = MSCONNECTOR_BOOL_OFF;
        child_config.enable = MSCONNECTOR_BOOL_ON;
        assert(msconnector_config_merge(&merged_config, &parent_config, &child_config));
        assert(merged_config.enable == MSCONNECTOR_BOOL_ON);
        assert(merged_config.default_block_status == MSCONNECTOR_DEFAULT_BLOCK_STATUS);
        assert(msconnector_config_validate(&merged_config, error, sizeof(error)));

        merged_config.default_block_status = 403;
        assert(msconnector_config_validate(&merged_config, error, sizeof(error)));
        merged_config.default_block_status = 200;
        error[0] = '\0';
        assert(!msconnector_config_validate(&merged_config, error, sizeof(error)));
        assert(error[0] != '\0');
        merged_config.default_block_status = 99;
        assert(!msconnector_config_validate(&merged_config, error, sizeof(error)));
        merged_config.default_block_status = 600;
        assert(!msconnector_config_validate(&merged_config, error, sizeof(error)));

        msconnector_config_init(&parent_config);
        msconnector_config_init(&child_config);
        parent_config.rules_remote_key = "parent-key";
        child_config.rules_remote_url = "https://example.invalid/rules.conf";
        assert(!msconnector_config_merge(&merged_config, &parent_config, &child_config));
        assert(merged_config.rules_remote_key == 0);
        assert(strcmp(merged_config.rules_remote_url, "https://example.invalid/rules.conf") == 0);

        msconnector_config_init(&parent_config);
        msconnector_config_init(&child_config);
        parent_config.transaction_id = "parent-id";
        child_config.transaction_id_expr = "child-expr";
        assert(msconnector_config_merge(&merged_config, &parent_config, &child_config));
        assert(merged_config.transaction_id == 0);
        assert(strcmp(merged_config.transaction_id_expr, "child-expr") == 0);

        msconnector_config_init(&parent_config);
        msconnector_config_init(&child_config);
        parent_config.transaction_id_expr = "parent-expr";
        child_config.transaction_id = "child-id";
        assert(msconnector_config_merge(&merged_config, &parent_config, &child_config));
        assert(strcmp(merged_config.transaction_id, "child-id") == 0);
        assert(merged_config.transaction_id_expr == 0);
    }
    assert(msconnector_directive_spec_find(MSCONNECTOR_DIRECTIVE_MODSECURITY) != 0);
    assert(msconnector_directive_spec_count() > 0);
    {
        const msconnector_header headers[] = {{"Content-Type", 12, "application/json; charset=utf-8", 31}};
        const msconnector_header exact[] = {{"Content-Type", 12, "application/json", 16}};
        const msconnector_header spaced[] = {{"Content-Type", 12, "application/json ; charset=utf-8", 32}};
        const msconnector_header uppercase[] = {{"Content-Type", 12, "APPLICATION/JSON", 16}};
        const msconnector_header garbage[] = {{"Content-Type", 12, "application/json garbage", 24}};
        const msconnector_header spaced_garbage[] = {{"Content-Type", 12, "application/json    garbage", 27}};
        const msconnector_header tab_garbage[] = {{"Content-Type", 12, "application/json	garbage", 24}};
        const msconnector_header suffix[] = {{"Content-Type", 12, "application/jsonx", 17}};
        const msconnector_header embedded[] = {{"Content-Type", 12, "text/application-json", 21}};
        assert(msconnector_header_name_equals(&headers[0], "content-type"));
        assert(msconnector_headers_find(headers, 1, "CONTENT-TYPE") == &headers[0]);
        assert(msconnector_headers_content_type_matches(headers, 1, "application/json"));
        assert(msconnector_headers_content_type_matches(exact, 1, "application/json"));
        assert(msconnector_headers_content_type_matches(spaced, 1, "application/json"));
        assert(msconnector_headers_content_type_matches(uppercase, 1, "application/json"));
        assert(!msconnector_headers_content_type_matches(garbage, 1, "application/json"));
        assert(!msconnector_headers_content_type_matches(spaced_garbage, 1, "application/json"));
        assert(!msconnector_headers_content_type_matches(tab_garbage, 1, "application/json"));
        assert(!msconnector_headers_content_type_matches(suffix, 1, "application/json"));
        assert(!msconnector_headers_content_type_matches(embedded, 1, "application/json"));
    }
    {
        msconnector_body_policy policy;
        msconnector_body_policy_init(&policy);
        assert(strcmp(msconnector_body_mode_name(MSCONNECTOR_BODY_MODE_BUFFERED), "buffered") == 0);
        assert(msconnector_body_mode_is_supported(policy.request_body_mode));
    }
    {
        msconnector_transaction_state state;
        msconnector_transaction_state_init(&state, "tx1");
        assert(msconnector_transaction_state_mark_phase(&state, MSCONNECTOR_PHASE_REQUEST_HEADERS));
        assert(msconnector_transaction_state_phase_processed(&state, MSCONNECTOR_PHASE_REQUEST_HEADERS));
        assert(strcmp(msconnector_phase_name(MSCONNECTOR_PHASE_LOGGING), "logging") == 0);
    }
    assert(strcmp(msconnector_decision_action_name(MSCONNECTOR_DECISION_ACTION_DENY), "deny") == 0);
    assert(msconnector_decision_action_is_disruptive(MSCONNECTOR_DECISION_ACTION_DENY));
    assert(strcmp(msconnector_late_intervention_action_name(MSCONNECTOR_LATE_INTERVENTION_LOG_ONLY), "log_only") == 0);
    {
        char escaped[32];
        assert(msconnector_json_escape("a\"b", escaped, sizeof(escaped)) == 4);
        assert(strcmp(escaped, "a\\\"b") == 0);
    }
    {
        char redacted[16];
        assert(strcmp(msconnector_redacted_string(), "[redacted]") == 0);
        assert(msconnector_redact_copy("secret", redacted, sizeof(redacted)) == strlen("[redacted]"));
        assert(strcmp(redacted, "[redacted]") == 0);
    }
    {
        msconnector_artifact_paths paths;
        msconnector_artifact_paths_init(&paths);
        assert(strcmp(msconnector_artifact_default_result_json(), "result.json") == 0);
        assert(strcmp(paths.decision_jsonl, msconnector_artifact_default_decision_jsonl()) == 0);
    }
    {
        msconnector_adapter_metadata metadata;
        msconnector_adapter_metadata_init(&metadata);
        assert(!msconnector_adapter_metadata_is_complete(&metadata));
    }
    assert(strcmp(msconnector_build_status_name(MSCONNECTOR_BUILD_STATUS_COMPILES), "compiles") == 0);
    assert(strcmp(msconnector_runtime_status_name(MSCONNECTOR_RUNTIME_STATUS_NOT_VERIFIED), "not_verified") == 0);
    assert(strcmp(msconnector_verification_status_name(MSCONNECTOR_VERIFICATION_STATUS_STATIC_ONLY), "static_only") == 0);
    {
        msconnector_test_result result;
        msconnector_test_result_init(&result);
        assert(!msconnector_test_result_passed(&result));
        result.status = MSCONNECTOR_STATUS_OK;
        result.expected_http_status = 200;
        result.actual_http_status = 200;
        assert(msconnector_test_result_passed(&result));
    }
    assert(msconnector_path_is_absolute("/tmp/result.json"));
    assert(msconnector_path_is_empty(""));
    assert(msconnector_path_has_parent_reference("../secret"));
    assert(msconnector_path_has_parent_reference("a/../secret"));
    assert(msconnector_path_has_parent_reference("..\\secret"));
    assert(msconnector_path_has_parent_reference("a\\..\\secret"));
    assert(msconnector_path_has_parent_reference("a\\../secret"));
    assert(msconnector_path_has_parent_reference("a/..\\secret"));
    assert(!msconnector_path_has_parent_reference("abc..def"));
    assert(!msconnector_path_has_parent_reference("folder..name/file"));
    assert(!msconnector_path_has_parent_reference("safe/path"));
    assert(!msconnector_path_has_parent_reference("safe\\path"));
    {
        msconnector_event event;
        char json[4096];
        char small_json[64];
        int truncated = 0;
        msconnector_event_init(&event);
        event.event = "smoke";
        assert(strcmp(msconnector_event_status_name(&event), "ok") == 0);
        assert(msconnector_event_write_json(&event, json, sizeof(json)));

        msconnector_event_set_phase4_hard_abort_after_200(
            &event,
            "nginx",
            "tx-1",
            "1001",
            "phase4 rule matched");
        assert(strcmp(event.message_id, MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200) == 0);
        assert(strcmp(event.message, "Response already started with HTTP 200; Phase 4 requested a block; connection was aborted.") == 0);
        assert(event.http_status == 200);
        assert(event.original_http_status == 200);
        assert(event.visible_http_status == 200);
        assert(event.late_intervention == 1);
        assert(event.response_started == 1);
        assert(event.headers_sent == 1);
        assert(event.connection_aborted == 1);
        assert(strcmp(event.requested_action, "deny") == 0);
        assert(strcmp(event.actual_action, "connection_abort") == 0);
        assert(strcmp(msconnector_http_status_reason_phrase(200), "OK") == 0);
        assert(strcmp(msconnector_http_status_default_message(200), "Request succeeded") == 0);
        assert(!msconnector_http_status_is_block_response(200));
        assert(msconnector_event_write_json_ex(&event, json, sizeof(json), &truncated));
        assert(!truncated);
        assert(strstr(json, "\"message_id\":\"MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200\"") != 0);
        assert(strstr(json, "Response already started with HTTP 200; Phase 4 requested a block; connection was aborted.") != 0);
        assert(strstr(json, "\"http_reason_phrase\":\"OK\"") != 0);
        assert(strstr(json, "\"http_default_message\":\"Request succeeded\"") != 0);
        assert(strstr(json, "\"requested_action\":\"deny\"") != 0);
        assert(strstr(json, "\"actual_action\":\"connection_abort\"") != 0);
        assert(strstr(json, "\"late_intervention\":true") != 0);
        assert(strstr(json, "\"connection_aborted\":true") != 0);
        assert(strstr(json, "body_payload") == 0);
        assert(strstr(json, "\"request_body\":") == 0);
        assert(strstr(json, "\"response_body\":") == 0);
        event.reason = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef";
        assert(!msconnector_event_write_json_ex(&event, json, sizeof(json), &truncated));
        assert(truncated);
        assert(strstr(json, "\"truncated\":true") != 0);
        assert(!msconnector_event_write_json(&event, json, sizeof(json)));
        assert(!msconnector_event_write_json_ex(&event, small_json, sizeof(small_json), &truncated));
        assert(truncated);
        assert(small_json[sizeof(small_json) - 1U] == '\0' || strlen(small_json) < sizeof(small_json));
    }

    return 0;
}
EOF

"$CC_BIN" $MSCONNECTOR_CFLAGS \
    -I "$REPO_ROOT/common/include" \
    "$SMOKE_C" \
    "$REPO_ROOT"/common/src/*.c \
    -o "$SMOKE_BIN"

"$SMOKE_BIN"
echo "common_helper_smoke: pass output=$OUT_DIR"
