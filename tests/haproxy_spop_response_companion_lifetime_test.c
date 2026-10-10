#define _POSIX_C_SOURCE 200809L

#include <assert.h>
#include <stdlib.h>
#include <string.h>

#define main haproxy_spop_diagnostic_runtime_program_main
#include "connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c"
#undef main

static void assert_delayed_owner_cannot_use_callback_storage(
    haproxy_spop_response_companion_owner_operation operation, int redirect) {
    haproxy_spop_response_companion_decision_storage *callback_storage;
    haproxy_spop_response_companion_owner_command command;
    haproxy_modsecurity_decision native_decision;
    msconnector_decision callback_decision;
    msconnector_error error;
    msconnector_response response;
    spop_bridge_task_context context;
    spop_bridge_task_result result;

    memset(&command, 0, sizeof(command));
    memset(&native_decision, 0, sizeof(native_decision));
    memset(&response, 0, sizeof(response));
    memset(&context, 0, sizeof(context));
    callback_storage = calloc(1U, sizeof(*callback_storage));
    assert(callback_storage != NULL);
    command.operation = operation;
    command.lease = 1U;
    command.decision_storage = callback_storage;
    if (operation == HAPROXY_SPOP_RESPONSE_COMPANION_RESPONSE_HEADERS) {
        response.status = 200;
        command.response = &response;
    }
    msconnector_error_init(&error);
    assert(prepare_spop_bridge_context(&context, &command, &error) == 0);
    assert(context.command.decision_storage == &context.decision_storage);
    assert(context.command.decision_storage != callback_storage);

    /* Model a caller timeout: its callback-owned decision storage is gone
     * before the delayed owner task evaluates a disruptive response. */
    free(callback_storage);
    callback_storage = NULL;
    native_decision.disruptive = 1;
    native_decision.status = redirect ? 302 : 403;
    native_decision.rule_id = operation ==
        HAPROXY_SPOP_RESPONSE_COMPANION_RESPONSE_HEADERS ? 1100201 : 1100301;
    memcpy(native_decision.action, redirect ? "redirect" : "deny",
           redirect ? sizeof("redirect") : sizeof("deny"));
    memcpy(native_decision.redirect_url, "/delayed-owner",
           sizeof("/delayed-owner"));
    memcpy(native_decision.log_message, "delayed owner decision",
           sizeof("delayed owner decision"));
    assert(set_bridge_native_decision(&context, &native_decision) == 1);
    context.decision.phase = operation ==
        HAPROXY_SPOP_RESPONSE_COMPANION_RESPONSE_HEADERS ? 3 : 4;
    assert(context.decision.rule_id == context.decision_storage.rule_id);
    assert(strcmp(context.decision.rule_id,
        context.decision.phase == 3 ? "1100201" : "1100301") == 0);
    context.success = 1;
    memset(&result, 0, sizeof(result));
    copy_spop_bridge_result(&context, &result);
    assert(result.success == 1);
    assert(result.decision.rule_id == result.decision_storage.rule_id);
    if (redirect) {
        assert(result.decision.redirect_url == result.decision_storage.redirect_url);
    }
    assert(result.decision.reason == result.decision_storage.log_message);
    memset(&context.decision_storage, 0, sizeof(context.decision_storage));
    assert(strcmp(result.decision.rule_id,
        result.decision.phase == 3 ? "1100201" : "1100301") == 0);
    callback_storage = calloc(1U, sizeof(*callback_storage));
    assert(callback_storage != NULL);
    msconnector_error_init(&error);
    assert(copy_spop_bridge_decision(&callback_decision, callback_storage,
        &result.decision, &error) == 1);
    assert(callback_decision.rule_id == callback_storage->rule_id);
    if (redirect) {
        assert(callback_decision.redirect_url == callback_storage->redirect_url);
    }
    assert(callback_decision.reason == callback_storage->log_message);
    memset(&result, 0, sizeof(result));
    assert(strcmp(callback_decision.rule_id,
        callback_decision.phase == 3 ? "1100201" : "1100301") == 0);
    assert(callback_decision.kind == (redirect ? MSCONNECTOR_DECISION_KIND_REDIRECT :
        MSCONNECTOR_DECISION_KIND_DENY));
    if (redirect) {
        assert(strcmp(callback_decision.redirect_url, "/delayed-owner") == 0);
    }
    free(callback_storage);
}

static void assert_invalid_rule_ids_fail_closed(void) {
    haproxy_spop_response_companion_decision_storage storage;
    msconnector_decision source, destination;
    msconnector_error error;
    char oversized[MSCONNECTOR_MAX_RULE_ID_LENGTH + 1U];
    const char *invalid[] = {"", "1100 301", "1100\n301", "1100/301", "1100\x80", oversized};
    memset(oversized, '1', sizeof(oversized) - 1U);
    oversized[sizeof(oversized) - 1U] = '\0';
    for (size_t index = 0U; index < sizeof(invalid) / sizeof(invalid[0]); ++index) {
        msconnector_decision_set_deny(&source, 403, invalid[index], "bounded log");
        msconnector_error_init(&error);
        assert(copy_spop_bridge_decision(&destination, &storage, &source, &error) == 0);
        msconnector_decision_set_redirect(&source, 302, "/safe", invalid[index],
            "bounded log");
        assert(copy_spop_bridge_decision(&destination, &storage, &source, &error) == 0);
    }
    /* A maximum-size valid ID survives intact; missing IDs remain missing. */
    oversized[MSCONNECTOR_MAX_RULE_ID_LENGTH - 1U] = '\0';
    msconnector_decision_set_deny(&source, 403, oversized, "bounded log");
    assert(copy_spop_bridge_decision(&destination, &storage, &source, &error) == 1);
    assert(strcmp(destination.rule_id, oversized) == 0);
    msconnector_decision_set_deny(&source, 403, NULL, "bounded log");
    assert(copy_spop_bridge_decision(&destination, &storage, &source, &error) == 1);
    assert(destination.rule_id == NULL);
    msconnector_decision_set_allow(&source);
    assert(copy_spop_bridge_decision(&destination, &storage, &source, &error) == 1);
    assert(destination.rule_id == NULL);
    source.rule_id = "1100301";
    assert(copy_spop_bridge_decision(&destination, &storage, &source, &error) == 0);

    spop_bridge_task_context context = {0};
    haproxy_modsecurity_decision native = {0};
    context.command.decision_storage = &context.decision_storage;
    native.disruptive = 1;
    native.status = 403;
    native.rule_id = -1;
    assert(set_bridge_native_decision(&context, &native) == 0);
    native.rule_id = 0;
    assert(set_bridge_native_decision(&context, &native) == 1);
    assert(context.decision.rule_id == NULL);
    native.rule_id = 1100301;
    assert(set_bridge_native_decision(&context, &native) == 1);
    assert(strcmp(context.decision.rule_id, "1100301") == 0);
    assert(context.decision.reason[0] == '\0'); /* structured ID with nolog */
    native.disruptive = 0;
    native.rule_id = 1100301;
    assert(set_bridge_native_decision(&context, &native) == 1);
    assert(context.decision.rule_id == NULL);
}

int main(void) {
    for (int redirect = 0; redirect <= 1; ++redirect) {
        assert_delayed_owner_cannot_use_callback_storage(
            HAPROXY_SPOP_RESPONSE_COMPANION_RESPONSE_HEADERS, redirect);
        assert_delayed_owner_cannot_use_callback_storage(
            HAPROXY_SPOP_RESPONSE_COMPANION_RESPONSE_EOS, redirect);
    }
    assert_invalid_rule_ids_fail_closed();
    return 0;
}
