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
#include "msconnector/adapter.h"
#include "msconnector/adapter_contract.h"
#include "msconnector/adapter_metadata.h"
#include "msconnector/artifact_layout.h"
#include "msconnector/artifacts.h"
#include "msconnector/body_policy.h"
#include "msconnector/build_contract.h"
#include "msconnector/config_parser.h"
#include "msconnector/connector_manifest.h"
#include "msconnector/limits.h"
#include "msconnector/log_sanitize.h"
#include "msconnector/origin_governance.h"
#include "msconnector/request_helpers.h"
#include "msconnector/response_helpers.h"
#include "msconnector/rule_error.h"
#include "msconnector/rule_event.h"
#include "msconnector/rule_id.h"
#include "msconnector/rule_merge.h"
#include "msconnector/runtime_report.h"
#include "msconnector/test_result_json.h"
#include "msconnector/config.h"
#include "msconnector/decision_action.h"
#include "msconnector/directive_spec.h"
#include "msconnector/directives.h"
#include "msconnector/decision.h"
#include "msconnector/error.h"
#include "msconnector/event.h"
#include "msconnector/event_jsonl.h"
#include "msconnector/headers.h"
#include "msconnector/http_status.h"
#include "msconnector/json_escape.h"
#include "msconnector/capability_matrix.h"
#include "msconnector/late_intervention.h"
#include "msconnector/modsecurity_engine.h"
#include "msconnector/lifecycle_status.h"
#include "msconnector/path_policy.h"
#include "msconnector/redaction.h"
#include "msconnector/rule_loader.h"
#include "msconnector/runtime_paths.h"
#include "msconnector/test_result.h"
#include "msconnector/transaction_id.h"
#include "msconnector/transaction_state.h"

#include <assert.h>
#include <string.h>

typedef struct fake_backend_state {
    int inline_calls;
    int file_calls;
    int remote_calls;
    int init_calls;
    int cleanup_calls;
    int create_rules_calls;
    int new_transaction_calls;
    int request_headers_calls;
    int response_body_calls;
    int logging_calls;
    int fail_next;
} fake_backend_state;

static int fake_add_inline(void *userdata, void *rules_set, const char *rules, msconnector_error *error) {
    fake_backend_state *state = (fake_backend_state *)userdata;
    (void)rules_set;
    (void)rules;
    (void)error;
    if (state->fail_next) { state->fail_next = 0; return 0; }
    ++state->inline_calls;
    return 1;
}

static int fake_add_file(void *userdata, void *rules_set, const char *path, msconnector_error *error) {
    fake_backend_state *state = (fake_backend_state *)userdata;
    (void)rules_set;
    (void)path;
    (void)error;
    if (state->fail_next) { state->fail_next = 0; return 0; }
    ++state->file_calls;
    return 1;
}

static int fake_add_remote(void *userdata, void *rules_set, const char *key, const char *url, msconnector_error *error) {
    fake_backend_state *state = (fake_backend_state *)userdata;
    (void)rules_set;
    (void)key;
    (void)url;
    (void)error;
    if (state->fail_next) { state->fail_next = 0; return 0; }
    ++state->remote_calls;
    return 1;
}

static int fake_engine_init(void *userdata, msconnector_error *error) {
    fake_backend_state *state = (fake_backend_state *)userdata;
    (void)error;
    ++state->init_calls;
    return 1;
}

static void fake_engine_cleanup(void *userdata) {
    fake_backend_state *state = (fake_backend_state *)userdata;
    ++state->cleanup_calls;
}

static void *fake_create_rules(void *userdata, msconnector_error *error) {
    fake_backend_state *state = (fake_backend_state *)userdata;
    (void)error;
    ++state->create_rules_calls;
    return state;
}

static void fake_destroy_rules(void *userdata, void *rules_set) {
    (void)userdata;
    (void)rules_set;
}

static void *fake_new_transaction(void *userdata, void *rules_set, const char *transaction_id, msconnector_error *error) {
    fake_backend_state *state = (fake_backend_state *)userdata;
    (void)rules_set;
    (void)transaction_id;
    (void)error;
    ++state->new_transaction_calls;
    return state;
}

static void fake_free_transaction(void *userdata, void *transaction) {
    (void)userdata;
    (void)transaction;
}

static int fake_process_request_headers(void *userdata, void *transaction, const msconnector_request *request, msconnector_decision *decision, msconnector_error *error) {
    fake_backend_state *state = (fake_backend_state *)userdata;
    (void)transaction;
    (void)request;
    (void)error;
    ++state->request_headers_calls;
    if (decision != 0) { msconnector_decision_set_allow(decision); }
    return 1;
}

static int fake_process_response_body(void *userdata, void *transaction, const msconnector_response *response, msconnector_decision *decision, msconnector_error *error) {
    fake_backend_state *state = (fake_backend_state *)userdata;
    (void)transaction;
    (void)response;
    (void)error;
    ++state->response_body_calls;
    if (decision != 0) { msconnector_decision_set_connection_abort(decision, "900", "phase4"); }
    return 1;
}

static int fake_process_logging(void *userdata, void *transaction, msconnector_error *error) {
    fake_backend_state *state = (fake_backend_state *)userdata;
    (void)transaction;
    (void)error;
    ++state->logging_calls;
    return 1;
}

static int fake_expr_eval(void *userdata, const msconnector_request *request, char *out, size_t out_len) {
    (void)userdata;
    (void)request;
    if (out_len < 8U) { return 0; }
    strcpy(out, "expr-id");
    return 1;
}

static msconnector_adapter_metadata fake_metadata;
static msconnector_capabilities fake_capabilities;

static const msconnector_adapter_metadata *fake_adapter_metadata(void *userdata) {
    (void)userdata;
    return &fake_metadata;
}

static const msconnector_capabilities *fake_adapter_capabilities(void *userdata) {
    (void)userdata;
    return &fake_capabilities;
}

static int fake_adapter_phase(void *userdata, msconnector_transaction_view *tx, msconnector_decision *decision, msconnector_error *error) {
    (void)userdata;
    (void)tx;
    (void)error;
    if (decision != 0) { msconnector_decision_set_allow(decision); }
    return 1;
}

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
        merged_config.default_block_status = 403;
        merged_config.default_error_status = 500;
        assert(msconnector_config_validate(&merged_config, error, sizeof(error)));
        merged_config.default_error_status = 503;
        assert(msconnector_config_validate(&merged_config, error, sizeof(error)));
        merged_config.default_error_status = 200;
        assert(!msconnector_config_validate(&merged_config, error, sizeof(error)));
        merged_config.default_error_status = 302;
        assert(!msconnector_config_validate(&merged_config, error, sizeof(error)));
        merged_config.default_error_status = 500;
        merged_config.unsupported_status = 501;
        assert(msconnector_config_validate(&merged_config, error, sizeof(error)));
        merged_config.unsupported_status = 500;
        assert(msconnector_config_validate(&merged_config, error, sizeof(error)));
        merged_config.unsupported_status = 200;
        assert(!msconnector_config_validate(&merged_config, error, sizeof(error)));
        merged_config.unsupported_status = 302;
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
        const msconnector_header leading[] = {{"Content-Type", 12, "  application/json", 18}};
        const msconnector_header leading_param[] = {{"Content-Type", 12, " 	 application/json ; charset=utf-8", 34}};
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
        assert(msconnector_headers_content_type_matches(leading, 1, "application/json"));
        assert(msconnector_headers_content_type_matches(leading_param, 1, "application/json"));
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
        metadata.connector_name = ""; metadata.server_family = "server"; metadata.source_kind = "imported";
        metadata.imported_path = "common"; metadata.build_status = "build"; metadata.runtime_status = "runtime"; metadata.verification_status = "verified";
        assert(!msconnector_adapter_metadata_is_complete(&metadata));
        metadata.connector_name = "common";
        assert(msconnector_adapter_metadata_is_complete(&metadata));
        metadata.imported_path = "";
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
    assert(msconnector_path_is_absolute("\\tmp\\out"));
    assert(msconnector_path_is_absolute("\\\\server\\share\\out"));
    assert(msconnector_path_is_absolute("C:\\tmp\\out"));
    assert(msconnector_path_is_absolute("C:/tmp/out"));
    assert(!msconnector_path_is_absolute("safe/path"));
    assert(!msconnector_path_is_absolute("safe\\path"));
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
        const msconnector_header headers[] = {
            {"Content-Length", 14, " 42 ", 4},
            {"content-length", 14, "42", 2},
            {"Set-Cookie", 10, "a=b", 3},
            {"Host", 4, "example.test", 12},
            {"X-Test", 6, "first", 5},
            {"x-test", 6, "last", 4}
        };
        const msconnector_header conflicting[] = {
            {"Content-Length", 14, "42", 2},
            {"Content-Length", 14, "43", 2}
        };
        const msconnector_header invalid_cl[] = {{"Content-Length", 14, "+1", 2}};
        size_t content_length = 0;
        char sanitized[8];
        int truncated = 0;
        assert(msconnector_headers_count_name(headers, 6, "x-test") == 2U);
        assert(msconnector_headers_find_first(headers, 6, "x-test") == &headers[4]);
        assert(msconnector_headers_find_last(headers, 6, "x-test") == &headers[5]);
        assert(!msconnector_header_value_can_be_combined("Set-Cookie", 10));
        assert(!msconnector_header_value_can_be_combined("Content-Length", 14));
        assert(msconnector_header_value_can_be_combined("Accept", 6));
        assert(msconnector_headers_parse_content_length(headers, 6, &content_length) == 1);
        assert(content_length == 42U);
        assert(msconnector_headers_parse_content_length(conflicting, 2, &content_length) == -1);
        assert(msconnector_headers_parse_content_length(invalid_cl, 1, &content_length) == -1);
        assert(strcmp(msconnector_headers_host(headers, 6), "example.test") == 0);
        assert(msconnector_header_sanitize_value_for_log("a\r\nb", 4, sanitized, sizeof(sanitized), &truncated) == 4U);
        assert(strcmp(sanitized, "a  b") == 0);
        assert(!truncated);
        assert(msconnector_header_sanitize_value_for_log("abcdef", 6, sanitized, 4, &truncated) == 6U);
        assert(truncated);
    }
    {
        msconnector_event event;
        char json[2048];
        msconnector_decision model_decision;
        msconnector_decision_set_allow(&model_decision);
        assert(msconnector_decision_is_allow(&model_decision));
        msconnector_decision_set_log_only(&model_decision, "observe");
        assert(!msconnector_decision_is_disruptive(&model_decision));
        msconnector_decision_set_deny(&model_decision, 0, "1", "deny");
        assert(msconnector_decision_is_deny(&model_decision));
        assert(model_decision.http_status == 403);
        msconnector_decision_set_deny(&model_decision, 406, "1", "deny");
        assert(model_decision.http_status == 406);
        msconnector_decision_set_deny(&model_decision, 429, "1", "deny");
        assert(model_decision.http_status == 429);
        msconnector_decision_set_deny(&model_decision, 200, "1", "deny");
        assert(model_decision.http_status == 500);
        msconnector_decision_set_redirect(&model_decision, 302, "https://example.test/", "2", "redirect");
        assert(msconnector_decision_is_redirect(&model_decision));
        assert(strcmp(model_decision.redirect_url, "https://example.test/") == 0);
        msconnector_decision_set_drop(&model_decision, "3", "drop");
        assert(msconnector_decision_is_drop(&model_decision));
        msconnector_decision_set_connection_abort(&model_decision, "4", "abort");
        assert(msconnector_decision_is_connection_abort(&model_decision));
        msconnector_decision_set_unsupported(&model_decision, "unsupported");
        assert(model_decision.http_status == 501);
        msconnector_decision_set_error(&model_decision, 0, "error");
        assert(model_decision.http_status == 500);
        assert(msconnector_decision_to_event(&model_decision, &event, "common", "tx-decision"));
        assert(msconnector_event_write_json(&event, json, sizeof(json)));
        assert(strstr(json, "\"message_id\":") != 0);
        assert(strstr(json, "\"action\":\"error\"") != 0);
        assert(strstr(json, "\"request_body\":") == 0);
        assert(strstr(json, "\"response_body\":") == 0);
    }
    {
        msconnector_error error;
        msconnector_event event;
        char json[1024];
        msconnector_error_init(&error);
        assert(strcmp(msconnector_error_code_name(MSCONNECTOR_ERROR_TIMEOUT), "timeout") == 0);
        assert(msconnector_error_default_message(MSCONNECTOR_ERROR_INTERNAL) != 0);
        assert(msconnector_error_status(MSCONNECTOR_ERROR_UNSUPPORTED_CAPABILITY) == MSCONNECTOR_STATUS_UNSUPPORTED);
        assert(msconnector_error_http_status(MSCONNECTOR_ERROR_TIMEOUT) == 504);
        assert(msconnector_error_is_fatal(MSCONNECTOR_ERROR_INTERNAL));
        msconnector_error_set(&error, MSCONNECTOR_ERROR_RULE_PARSE_FAILED, "parse failed", "smoke");
        assert(msconnector_error_to_event(&error, &event, "common", "tx-error"));
        assert(msconnector_event_write_json(&event, json, sizeof(json)));
        assert(strstr(json, "parse failed") != 0);
    }
    {
        fake_backend_state state = {0};
        msconnector_rule_loader_backend backend = {&state, fake_add_inline, fake_add_file, fake_add_remote};
        msconnector_rule_loader loader;
        msconnector_error error;
        msconnector_config config;
        const msconnector_rule_load_stats *stats;
        msconnector_rule_loader_init(&loader, &state, &backend);
        assert(msconnector_rule_loader_add_inline(&loader, "SecRule ARGS x", &error));
        assert(msconnector_rule_loader_add_file(&loader, "rules.conf", &error));
        assert(msconnector_rule_loader_add_remote(&loader, "key", "https://example.test/rules", &error));
        stats = msconnector_rule_loader_stats(&loader);
        assert(stats->inline_rules == 1);
        assert(stats->file_rules == 1);
        assert(stats->remote_rules == 1);
        assert(!msconnector_rule_loader_add_remote(&loader, 0, "url", &error));
        assert(!msconnector_rule_loader_add_file(&loader, "../rules.conf", &error));
        state.fail_next = 1;
        assert(!msconnector_rule_loader_add_inline(&loader, "fail", &error));
        assert(stats->inline_rules == 1);
        msconnector_config_init(&config);
        config.rules_inline = "inline";
        config.rules_file = "rules.conf";
        config.rules_remote_key = "key";
        config.rules_remote_url = "url";
        assert(msconnector_rule_loader_load_config(&loader, &config, &error));
        assert(state.inline_calls >= 2);
        assert(state.file_calls >= 2);
        assert(state.remote_calls >= 2);
    }
    {
        fake_backend_state state = {0};
        msconnector_modsecurity_engine_ops ops;
        msconnector_modsecurity_engine engine;
        msconnector_modsecurity_transaction tx;
        msconnector_decision engine_decision;
        msconnector_error error;
        memset(&ops, 0, sizeof(ops));
        ops.userdata = &state;
        ops.init = fake_engine_init;
        ops.cleanup = fake_engine_cleanup;
        ops.create_rules_set = fake_create_rules;
        ops.destroy_rules_set = fake_destroy_rules;
        ops.new_transaction = fake_new_transaction;
        ops.free_transaction = fake_free_transaction;
        ops.process_request_headers = fake_process_request_headers;
        ops.process_response_body = fake_process_response_body;
        ops.process_logging = fake_process_logging;
        msconnector_modsecurity_engine_init(&engine, &ops);
        assert(msconnector_modsecurity_engine_start(&engine, &error));
        assert(msconnector_modsecurity_engine_create_rules(&engine, &error));
        assert(msconnector_modsecurity_transaction_init(&tx, &engine, "tx-engine", &error));
        assert(msconnector_modsecurity_process_request_headers(&tx, 0, &engine_decision, &error));
        assert(msconnector_transaction_state_phase_processed(&tx.state, MSCONNECTOR_PHASE_REQUEST_HEADERS));
        assert(msconnector_modsecurity_process_response_body(&tx, 0, &engine_decision, &error));
        assert(msconnector_decision_is_connection_abort(&engine_decision));
        assert(msconnector_modsecurity_process_logging(&tx, &error));
        assert(msconnector_transaction_state_phase_processed(&tx.state, MSCONNECTOR_PHASE_LOGGING));
        msconnector_modsecurity_transaction_cleanup(&tx);
        msconnector_modsecurity_transaction_cleanup(&tx);
        msconnector_modsecurity_engine_cleanup(&engine);
        msconnector_modsecurity_engine_cleanup(&engine);
        memset(&ops, 0, sizeof(ops));
        msconnector_modsecurity_engine_init(&engine, &ops);
        assert(!msconnector_modsecurity_engine_start(&engine, &error));
    }
    {
        msconnector_config config;
        msconnector_request request;
        msconnector_header headers[] = {{"X-Request-ID", 12, "header-id", 9}};
        msconnector_transaction_id_context ctx;
        msconnector_transaction_id_result result;
        msconnector_error error;
        memset(&request, 0, sizeof(request));
        request.headers = headers;
        request.header_count = 1;
        msconnector_config_init(&config);
        memset(&ctx, 0, sizeof(ctx));
        ctx.config = &config;
        ctx.request = &request;
        ctx.header_name = "X-Request-ID";
        ctx.host_request_id = "host-id";
        ctx.fallback_id = "fallback-id";
        config.transaction_id = "static-id";
        assert(msconnector_transaction_id_resolve(&ctx, &result, &error));
        assert(result.source == MSCONNECTOR_TRANSACTION_ID_SOURCE_STATIC);
        config.transaction_id = 0;
        config.transaction_id_expr = "expr";
        ctx.expr_eval = fake_expr_eval;
        assert(msconnector_transaction_id_resolve(&ctx, &result, &error));
        assert(strcmp(result.value, "expr-id") == 0);
        ctx.expr_eval = 0;
        assert(!msconnector_transaction_id_resolve(&ctx, &result, &error));
        config.transaction_id_expr = 0;
        assert(msconnector_transaction_id_resolve(&ctx, &result, &error));
        assert(result.source == MSCONNECTOR_TRANSACTION_ID_SOURCE_HOST);
        ctx.host_request_id = 0;
        assert(msconnector_transaction_id_resolve(&ctx, &result, &error));
        assert(result.source == MSCONNECTOR_TRANSACTION_ID_SOURCE_HEADER);
        ctx.header_name = 0;
        assert(msconnector_transaction_id_resolve(&ctx, &result, &error));
        assert(result.source == MSCONNECTOR_TRANSACTION_ID_SOURCE_FALLBACK);
        assert(!msconnector_transaction_id_validate("bad\nid"));
        assert(!msconnector_transaction_id_validate("  spaced"));
        assert(!msconnector_transaction_id_copy("01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567", result.value, sizeof(result.value)));
        assert(strcmp(msconnector_transaction_id_source_name(MSCONNECTOR_TRANSACTION_ID_SOURCE_HEADER), "header") == 0);
    }
    {
        msconnector_event event;
        char json[4096];
        char small_json[64];
        int truncated = 0;
        msconnector_event_init(&event);
        event.meta.event = "smoke";
        assert(strcmp(msconnector_event_status_name(&event), "ok") == 0);
        assert(msconnector_event_write_json(&event, json, sizeof(json)));

        msconnector_event_set_phase4_hard_abort_after_200(
            &event,
            "nginx",
            "tx-1",
            "1001",
            "phase4 rule matched");
        assert(strcmp(event.meta.message_id, MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200) == 0);
        assert(strcmp(event.meta.message, "Response already started with HTTP 200; Phase 4 requested a block; connection was aborted.") == 0);
        assert(event.http.http_status == 200);
        assert(event.http.original_http_status == 200);
        assert(event.http.visible_http_status == 200);
        assert(event.flags.late_intervention == 1);
        assert(event.flags.response_started == 1);
        assert(event.flags.headers_sent == 1);
        assert(event.flags.body_started == 1);
        assert(event.flags.connection_aborted == 1);
        assert(strcmp(event.decision.requested_action, "deny") == 0);
        assert(strcmp(event.decision.actual_action, "connection_abort") == 0);
        assert(strcmp(event.decision.action, "connection_abort") == 0);
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
        event.decision.reason = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef";
        assert(!msconnector_event_write_json_ex(&event, json, sizeof(json), &truncated));
        assert(truncated);
        assert(strstr(json, "\"truncated\":true") != 0);
        assert(!msconnector_event_write_json(&event, json, sizeof(json)));
        assert(!msconnector_event_write_json_ex(&event, small_json, sizeof(small_json), &truncated));
        assert(truncated);
        assert(small_json[sizeof(small_json) - 1U] == '\0' || strlen(small_json) < sizeof(small_json));
    }
    {
        msconnector_adapter adapter;
        msconnector_adapter_contract_result contract_result;
        msconnector_adapter_init(&adapter);
        assert(!msconnector_adapter_has_metadata(&adapter));
        msconnector_adapter_metadata_init(&fake_metadata);
        fake_metadata.connector_name = "common"; fake_metadata.server_family = "none"; fake_metadata.source_kind = "scaffold";
        fake_metadata.imported_path = "common"; fake_metadata.build_status = "static"; fake_metadata.runtime_status = "not_integrated"; fake_metadata.verification_status = "smoke";
        fake_capabilities.flags = MSCONNECTOR_CAPABILITY_REQUEST_HEADERS;
        fake_capabilities.connector_name = "common"; fake_capabilities.connector_version = "0"; fake_capabilities.server_family = "none"; fake_capabilities.notes = "common only";
        adapter.metadata = fake_adapter_metadata; adapter.capabilities = fake_adapter_capabilities; adapter.process_request_headers = fake_adapter_phase;
        assert(msconnector_adapter_has_metadata(&adapter));
        assert(msconnector_adapter_has_capabilities(&adapter));
        assert(msconnector_adapter_supports_phase(&adapter, MSCONNECTOR_PHASE_REQUEST_HEADERS));
        assert(!msconnector_adapter_supports_phase(&adapter, MSCONNECTOR_PHASE_RESPONSE_BODY));
        msconnector_adapter_contract_result_init(&contract_result);
        assert(msconnector_adapter_contract_validate(&adapter, &contract_result));
        assert(contract_result.ok);
    }
    {
        assert(msconnector_capability_has_required_test(MSCONNECTOR_CAPABILITY_PHASE4_HARD_ABORT));
        assert(strcmp(msconnector_capability_required_test(MSCONNECTOR_CAPABILITY_REQUEST_HEADERS), "phase1 request header rule test") == 0);
        assert(msconnector_capability_required_test(MSCONNECTOR_CAPABILITY_NONE) == 0);
    }
    {
        msconnector_artifact_layout layout;
        char joined[128];
        msconnector_artifact_layout_init(&layout);
        assert(strcmp(layout.result_json, "result.json") == 0);
        assert(strcmp(msconnector_artifact_name_decision_jsonl(), "decision.jsonl") == 0);
        assert(msconnector_runtime_path_join("/tmp/root", layout.decision_jsonl, joined, sizeof(joined)));
        assert(strcmp(joined, "/tmp/root/decision.jsonl") == 0);
        assert(!msconnector_runtime_path_join("/tmp/root", "/absolute", joined, sizeof(joined)));
        assert(!msconnector_runtime_path_join("/tmp/root", "\\absolute", joined, sizeof(joined)));
        assert(!msconnector_runtime_path_join("/tmp/root", "..\\secret", joined, sizeof(joined)));
        assert(!msconnector_runtime_path_join("/tmp/root", "../secret", joined, sizeof(joined)));
        assert(!msconnector_runtime_path_join("/tmp/root", "decision.jsonl", joined, 8));
    }
    {
        msconnector_event event;
        char line[4096];
        int truncated = 0;
        msconnector_event_set_phase4_hard_abort_after_200(&event, "common", "tx-jsonl", "1", "jsonl");
        assert(msconnector_event_write_jsonl_line(&event, line, sizeof(line), &truncated));
        assert(!truncated);
        assert(line[strlen(line) - 1U] == '\n');
        assert(strstr(line, "request_body") == 0);
        assert(!msconnector_event_write_jsonl_line(&event, line, 16, &truncated));
        assert(truncated);
    }

    {
        enum msconnector_bool_option bool_value;
        enum msconnector_phase4_mode mode_value;
        size_t parsed_size = 0;
        int parsed_status = 0;
        assert(msconnector_parse_bool("ON", &bool_value) && bool_value == MSCONNECTOR_BOOL_ON);
        assert(msconnector_parse_bool("no", &bool_value) && bool_value == MSCONNECTOR_BOOL_OFF);
        assert(!msconnector_parse_bool("on garbage", &bool_value));
        assert(msconnector_parse_phase4_mode("strict", &mode_value) && mode_value == MSCONNECTOR_PHASE4_MODE_STRICT);
        assert(!msconnector_parse_phase4_mode("unsafe", &mode_value));
        assert(msconnector_parse_size("128", &parsed_size) && parsed_size == 128U);
        assert(!msconnector_parse_size("0", &parsed_size));
        assert(!msconnector_parse_size("1.5", &parsed_size));
        assert(msconnector_parse_http_status("403", &parsed_status) && parsed_status == 403);
        assert(!msconnector_parse_http_status("99", &parsed_status));
        assert(!msconnector_parse_http_status("600", &parsed_status));
        assert(msconnector_validate_content_type_token("application/json"));
        assert(!msconnector_validate_content_type_token("application/json; charset=utf-8"));
        assert(!msconnector_validate_content_type_token("application json"));
    }
    {
        msconnector_request request;
        msconnector_response response;
        msconnector_header headers[] = {{"Content-Type", 12, "application/json", 16}, {"Content-Length", 14, "123", 3}};
        int cl_status = 0;
        msconnector_request_init(&request);
        assert(!msconnector_request_validate(&request));
        request.method = "GET"; request.uri = "/"; request.headers = headers; request.header_count = 2;
        assert(msconnector_request_validate(&request));
        assert(msconnector_request_has_header(&request, "content-type"));
        assert(strcmp(msconnector_request_content_type(&request), "application/json") == 0);
        assert(msconnector_request_content_length(&request, &cl_status) == 123U && cl_status == 1);
        request.headers = 0; request.header_count = 1;
        assert(!msconnector_request_validate(&request));
        msconnector_response_init(&response);
        assert(msconnector_response_validate(&response));
        response.status = 200; response.headers = headers; response.header_count = 2;
        assert(msconnector_response_validate(&response));
        assert(msconnector_response_has_header(&response, "CONTENT-LENGTH"));
        assert(strcmp(msconnector_response_content_type(&response), "application/json") == 0);
        assert(msconnector_response_content_length(&response, &cl_status) == 123U && cl_status == 1);
        response.status = 99;
        assert(!msconnector_response_validate(&response));
    }
    {
        msconnector_rule_collection parent_rules, child_rules, merged_rules;
        msconnector_error rule_error;
        msconnector_event rule_event;
        msconnector_test_result json_result;
        char json[1024];
        int truncated = 0;
        msconnector_rule_collection_init(&parent_rules);
        parent_rules.inline_rules = "parent"; parent_rules.rules_remote_key = "key"; parent_rules.rules_remote_url = "url";
        msconnector_rule_collection_init(&child_rules);
        child_rules.rules_file = "child.conf";
        assert(msconnector_rule_collection_merge(&merged_rules, &parent_rules, &child_rules));
        assert(strcmp(merged_rules.inline_rules, "parent") == 0);
        assert(strcmp(merged_rules.rules_file, "child.conf") == 0);
        child_rules.rules_remote_key = "child-key"; child_rules.rules_remote_url = 0;
        assert(!msconnector_rule_collection_merge(&merged_rules, &parent_rules, &child_rules));
        msconnector_rule_error_set_parse_failed(&rule_error, "rules.conf");
        assert(rule_error.code == MSCONNECTOR_ERROR_RULE_PARSE_FAILED);
        assert(msconnector_rule_error_event(&rule_error, &rule_event, "common", "tx-rule"));
        assert(msconnector_event_write_json(&rule_event, json, sizeof(json)));
        msconnector_rule_error_clear(&rule_error);
        assert(rule_error.code == MSCONNECTOR_ERROR_NONE);
        assert(msconnector_rule_load_event(&rule_stats, &rule_event, "common", "tx-rule"));
        assert(msconnector_event_write_json(&rule_event, json, sizeof(json)));
        assert(strstr(json, "request_body") == 0);
        msconnector_test_result_init(&json_result);
        json_result.connector = "common"; json_result.case_name = "json"; json_result.status = MSCONNECTOR_STATUS_OK; json_result.expected_http_status = 200; json_result.actual_http_status = 200; json_result.reason = "escaped \"reason\"";
        assert(msconnector_test_result_write_json(&json_result, json, sizeof(json), &truncated));
        assert(!truncated);
        assert(strstr(json, "\"case\"") != 0);
        assert(!msconnector_test_result_write_json(&json_result, json, 8, &truncated));
        assert(truncated);
    }
    {
        msconnector_adapter_metadata metadata;
        msconnector_connector_manifest manifest;
        msconnector_runtime_report report;
        msconnector_origin_governance governance;
        char json[1024];
        int truncated = 0;
        msconnector_adapter_metadata_init(&metadata);
        metadata.connector_name = "common"; metadata.server_family = "none"; metadata.source_kind = "scaffold"; metadata.imported_path = "common"; metadata.build_status = "static"; metadata.runtime_status = "not_integrated"; metadata.verification_status = "smoke";
        metadata.capabilities.flags = MSCONNECTOR_CAPABILITY_REQUEST_HEADERS; metadata.origin.source_repository = "repo"; metadata.origin.source_branch = "branch"; metadata.origin.source_commit = "commit"; metadata.origin.source_describe = "describe"; metadata.origin.license = "Apache-2.0";
        msconnector_connector_manifest_init(&manifest);
        assert(msconnector_connector_manifest_from_metadata(&manifest, &metadata));
        assert(msconnector_connector_manifest_write_json(&manifest, json, sizeof(json), &truncated));
        msconnector_runtime_report_init(&report);
        report.connector = "common"; report.case_name = "case"; report.status = MSCONNECTOR_STATUS_OK; report.capability = "request-headers"; report.artifact_result_json = "result.json"; report.artifact_decision_jsonl = "decision.jsonl"; report.reason = "static skeleton";
        assert(msconnector_runtime_report_write_json(&report, json, sizeof(json), &truncated));
        msconnector_origin_governance_init(&governance);
        assert(msconnector_origin_governance_from_metadata(&governance, &metadata));
        assert(msconnector_origin_governance_is_complete(&governance));
    }
    {
        char out[128];
        int truncated = 0;
        const unsigned char body[] = {'s','e','c','r','e','t'};
        assert(msconnector_build_contract_target_count() == 7U);
        assert(msconnector_build_contract_target_is_standard("smoke"));
        assert(!msconnector_build_contract_target_is_standard("deploy"));
        assert(msconnector_limit_header_count() > 0U);
        assert(msconnector_limit_transaction_id_length() >= 128U);
        assert(msconnector_limit_log_message_length() >= 256U);
        assert(msconnector_rule_id_validate("123"));
        assert(msconnector_rule_id_extract_from_message("[id \"123\"]", out, sizeof(out)) == 1);
        assert(strcmp(out, "123") == 0);
        assert(msconnector_rule_id_extract_from_message("no id", out, sizeof(out)) == 0);
        assert(!msconnector_rule_id_validate("bad\nid"));
        assert(msconnector_sanitize_log_message("a\r\nb", 4, out, sizeof(out), &truncated) == 4U);
        assert(strcmp(out, "a  b") == 0);
        assert(msconnector_redact_body_snippet(body, sizeof(body), out, sizeof(out), &truncated) > 0U);
        assert(strstr(out, "6 bytes") != 0);
        assert(strstr(out, "secret") == 0);
        assert(msconnector_redact_body_snippet(body, sizeof(body), out, 8, &truncated) > 0U);
        assert(truncated);
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
