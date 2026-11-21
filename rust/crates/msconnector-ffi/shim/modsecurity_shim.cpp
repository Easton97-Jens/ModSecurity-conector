#include "modsecurity_shim.h"
#include <modsecurity/modsecurity.h>
#include <modsecurity/rules_set.h>
#include <modsecurity/transaction.h>
#include <modsecurity/intervention.h>
#include <cstdio>

struct MsShimEngine { modsecurity::ModSecurity *engine; };
struct MsShimRules { modsecurity::RulesSet *rules; };
struct MsShimTransaction { modsecurity::Transaction *transaction; };

extern "C" {

MsShimEngine *msc_shim_engine_new(void) {
    return new MsShimEngine{new modsecurity::ModSecurity()};
}

void msc_shim_engine_free(MsShimEngine *engine) {
    if (!engine) return;
    delete engine->engine;
    delete engine;
}

MsShimRules *msc_shim_rules_load(MsShimEngine *engine, const char *path, char *error, size_t error_len) {
    if (!engine || !path) return nullptr;
    auto *rules = new modsecurity::RulesSet();
    if (rules->loadFromUri(path) >= 0) return new MsShimRules{rules};
    if (error && error_len > 0) std::snprintf(error, error_len, "libmodsecurity rules load failed");
    delete rules;
    return nullptr;
}

void msc_shim_rules_free(MsShimRules *rules) {
    if (!rules) return;
    delete rules->rules;
    delete rules;
}

MsShimTransaction *msc_shim_transaction_new(MsShimEngine *engine, MsShimRules *rules) {
    if (!engine || !rules) return nullptr;
    auto *transaction = new modsecurity::Transaction(engine->engine, rules->rules, nullptr);
    return new MsShimTransaction{transaction};
}

void msc_shim_transaction_free(MsShimTransaction *transaction) {
    if (!transaction) return;
    delete transaction->transaction;
    delete transaction;
}

int msc_shim_process_connection(MsShimTransaction *transaction, const char *client_ip) {
    if (!transaction) return -1;
    return transaction->transaction->processConnection(client_ip ? client_ip : "127.0.0.1", 0, "127.0.0.1", 80);
}

int msc_shim_process_uri(MsShimTransaction *transaction, const char *uri, const char *protocol, const char *http_version) {
    if (!transaction || !uri) return -1;
    return transaction->transaction->processURI(
        uri,
        protocol ? protocol : "http",
        http_version ? http_version : "1.1");
}

int msc_shim_add_request_header(MsShimTransaction *transaction, const char *name, const char *value) {
    if (!transaction || !name || !value) return -1;
    return transaction->transaction->addRequestHeader(name, value);
}

int msc_shim_process_request_headers(MsShimTransaction *transaction) {
    return transaction ? transaction->transaction->processRequestHeaders() : -1;
}
int msc_shim_append_request_body(MsShimTransaction *transaction, const uint8_t *data, size_t len) {
    return transaction ? transaction->transaction->appendRequestBody(data, len) : -1;
}
int msc_shim_finish_request_body(MsShimTransaction *transaction) {
    return transaction ? transaction->transaction->processRequestBody() : -1;
}
int msc_shim_process_response_headers(MsShimTransaction *transaction, int status) {
    return transaction ? transaction->transaction->processResponseHeaders(status, "HTTP/1.1") : -1;
}
int msc_shim_append_response_body(MsShimTransaction *transaction, const uint8_t *data, size_t len) {
    return transaction ? transaction->transaction->appendResponseBody(data, len) : -1;
}
int msc_shim_finish_response_body(MsShimTransaction *transaction) {
    return transaction ? transaction->transaction->processResponseBody() : -1;
}
int msc_shim_process_logging(MsShimTransaction *transaction) {
    return transaction ? transaction->transaction->processLogging() : -1;
}
int msc_shim_disruptive_status(MsShimTransaction *transaction) {
    if (!transaction) return 0;
    modsecurity::ModSecurityIntervention intervention;
    modsecurity::intervention::clean(&intervention);
    if (!transaction->transaction->intervention(&intervention)) return 0;
    int status = intervention.status;
    modsecurity::intervention::free(&intervention);
    return status;
}

}
