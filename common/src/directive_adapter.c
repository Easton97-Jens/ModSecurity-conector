#include "msconnector/directive_adapter.h"
#include "msconnector/directives.h"

#include <stdio.h>
#include <string.h>

static void set_error(char *error, size_t error_len, const char *message) {
    if (error != 0 && error_len > 0U) {
        (void)snprintf(error, error_len, "%s", message);
    }
}

static const msconnector_directive_adapter_entry entries[] = {
    {0, MSCONNECTOR_DIRECTIVE_MODSECURITY, MSCONNECTOR_DIRECTIVE_MODSECURITY, MSCONNECTOR_DIRECTIVE_SCOPE_SERVER, MSCONNECTOR_DIRECTIVE_ARG_ONE, 0U},
    {0, MSCONNECTOR_DIRECTIVE_RULES, MSCONNECTOR_DIRECTIVE_RULES, MSCONNECTOR_DIRECTIVE_SCOPE_SERVER, MSCONNECTOR_DIRECTIVE_ARG_RAW, 0U},
    {0, MSCONNECTOR_DIRECTIVE_RULES_FILE, MSCONNECTOR_DIRECTIVE_RULES_FILE, MSCONNECTOR_DIRECTIVE_SCOPE_SERVER, MSCONNECTOR_DIRECTIVE_ARG_ONE, 0U},
    {0, MSCONNECTOR_DIRECTIVE_RULES_REMOTE, MSCONNECTOR_DIRECTIVE_RULES_REMOTE, MSCONNECTOR_DIRECTIVE_SCOPE_SERVER, MSCONNECTOR_DIRECTIVE_ARG_ONE, 0U},
    {0, MSCONNECTOR_DIRECTIVE_TRANSACTION_ID, MSCONNECTOR_DIRECTIVE_TRANSACTION_ID, MSCONNECTOR_DIRECTIVE_SCOPE_LOCATION, MSCONNECTOR_DIRECTIVE_ARG_ONE, 0U},
    {0, MSCONNECTOR_DIRECTIVE_TRANSACTION_ID_EXPR, MSCONNECTOR_DIRECTIVE_TRANSACTION_ID_EXPR, MSCONNECTOR_DIRECTIVE_SCOPE_LOCATION, MSCONNECTOR_DIRECTIVE_ARG_ONE, 0U},
    {0, MSCONNECTOR_DIRECTIVE_PHASE4_MODE, MSCONNECTOR_DIRECTIVE_PHASE4_MODE, MSCONNECTOR_DIRECTIVE_SCOPE_SERVER, MSCONNECTOR_DIRECTIVE_ARG_ONE, 0U},
    {0, MSCONNECTOR_DIRECTIVE_PHASE4_CONTENT_TYPES_FILE, MSCONNECTOR_DIRECTIVE_PHASE4_CONTENT_TYPES_FILE, MSCONNECTOR_DIRECTIVE_SCOPE_SERVER, MSCONNECTOR_DIRECTIVE_ARG_ONE, 0U},
    {0, MSCONNECTOR_DIRECTIVE_PHASE4_LOG, MSCONNECTOR_DIRECTIVE_PHASE4_LOG, MSCONNECTOR_DIRECTIVE_SCOPE_SERVER, MSCONNECTOR_DIRECTIVE_ARG_ONE, 0U},
    {0, MSCONNECTOR_DIRECTIVE_PHASE4_BODY_LIMIT, MSCONNECTOR_DIRECTIVE_PHASE4_BODY_LIMIT, MSCONNECTOR_DIRECTIVE_SCOPE_SERVER, MSCONNECTOR_DIRECTIVE_ARG_ONE, 0U},
    {0, MSCONNECTOR_DIRECTIVE_REQUEST_BODY_LIMIT, MSCONNECTOR_DIRECTIVE_REQUEST_BODY_LIMIT, MSCONNECTOR_DIRECTIVE_SCOPE_SERVER, MSCONNECTOR_DIRECTIVE_ARG_ONE, 0U},
    {0, MSCONNECTOR_DIRECTIVE_RESPONSE_BODY_LIMIT, MSCONNECTOR_DIRECTIVE_RESPONSE_BODY_LIMIT, MSCONNECTOR_DIRECTIVE_SCOPE_SERVER, MSCONNECTOR_DIRECTIVE_ARG_ONE, 0U},
    {0, MSCONNECTOR_DIRECTIVE_BODY_LIMIT_ACTION, MSCONNECTOR_DIRECTIVE_BODY_LIMIT_ACTION, MSCONNECTOR_DIRECTIVE_SCOPE_SERVER, MSCONNECTOR_DIRECTIVE_ARG_ONE, 0U},
    {0, MSCONNECTOR_DIRECTIVE_LATE_INTERVENTION_TIMEOUT, MSCONNECTOR_DIRECTIVE_LATE_INTERVENTION_TIMEOUT, MSCONNECTOR_DIRECTIVE_SCOPE_SERVER, MSCONNECTOR_DIRECTIVE_ARG_ONE, 0U},
    {0, MSCONNECTOR_DIRECTIVE_USE_ERROR_LOG, MSCONNECTOR_DIRECTIVE_USE_ERROR_LOG, MSCONNECTOR_DIRECTIVE_SCOPE_SERVER, MSCONNECTOR_DIRECTIVE_ARG_ONE, 0U}
};

size_t msconnector_directive_adapter_count(void) {
    return sizeof(entries) / sizeof(entries[0]);
}

const msconnector_directive_adapter_entry *msconnector_directive_adapter_at(size_t index) {
    static msconnector_directive_adapter_entry resolved;
    if (index >= msconnector_directive_adapter_count()) {
        return 0;
    }
    resolved = entries[index];
    resolved.spec = msconnector_directive_spec_find(entries[index].canonical_name);
    return &resolved;
}

const msconnector_directive_adapter_entry *msconnector_directive_adapter_find(const char *canonical_name) {
    if (canonical_name == 0) {
        return 0;
    }
    for (size_t index = 0; index < msconnector_directive_adapter_count(); ++index) {
        if (strcmp(entries[index].canonical_name, canonical_name) == 0) {
            return msconnector_directive_adapter_at(index);
        }
    }
    return 0;
}

int msconnector_directive_adapter_validate_entry(const msconnector_directive_adapter_entry *entry, char *error, size_t error_len) {
    if (entry == 0) { set_error(error, error_len, "missing entry"); return 0; }
    if (entry->spec == 0) { set_error(error, error_len, "missing spec"); return 0; }
    if (entry->canonical_name == 0 || entry->canonical_name[0] == '\0') { set_error(error, error_len, "empty canonical_name"); return 0; }
    if (entry->host_name == 0 || entry->host_name[0] == '\0') { set_error(error, error_len, "empty host_name"); return 0; }
    if (entry->scope < MSCONNECTOR_DIRECTIVE_SCOPE_GLOBAL || entry->scope > MSCONNECTOR_DIRECTIVE_SCOPE_DIRECTORY) { set_error(error, error_len, "invalid scope"); return 0; }
    if (entry->argument_policy < MSCONNECTOR_DIRECTIVE_ARG_NONE || entry->argument_policy > MSCONNECTOR_DIRECTIVE_ARG_RAW) { set_error(error, error_len, "invalid argument_policy"); return 0; }
    if (strcmp(entry->spec->name, entry->canonical_name) != 0) { set_error(error, error_len, "spec name mismatch"); return 0; }
    return 1;
}

int msconnector_directive_adapter_validate_all(char *error, size_t error_len) {
    for (size_t index = 0; index < msconnector_directive_spec_count(); ++index) {
        const msconnector_directive_spec *spec = &msconnector_directive_specs()[index];
        if (msconnector_directive_adapter_find(spec->name) == 0) { set_error(error, error_len, "missing directive adapter"); return 0; }
    }
    for (size_t index = 0; index < msconnector_directive_adapter_count(); ++index) {
        const msconnector_directive_adapter_entry *entry = msconnector_directive_adapter_at(index);
        if (!msconnector_directive_adapter_validate_entry(entry, error, error_len)) { return 0; }
        for (size_t other = index + 1U; other < msconnector_directive_adapter_count(); ++other) {
            if (strcmp(entry->canonical_name, entries[other].canonical_name) == 0) { set_error(error, error_len, "duplicate canonical_name"); return 0; }
        }
    }
    return 1;
}
