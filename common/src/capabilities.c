#include "msconnector/capabilities.h"

#include <string.h>

typedef struct capability_name_entry {
    enum msconnector_capability_flag flag;
    const char *name;
} capability_name_entry;

static const capability_name_entry capability_names[] = {
    {MSCONNECTOR_CAPABILITY_NONE, "none"},
    {MSCONNECTOR_CAPABILITY_CONNECTION_METADATA, "connection-metadata"},
    {MSCONNECTOR_CAPABILITY_REQUEST_HEADERS, "request-headers"},
    {MSCONNECTOR_CAPABILITY_REQUEST_BODY_BUFFERED, "request-body-buffered"},
    {MSCONNECTOR_CAPABILITY_REQUEST_BODY_STREAMING, "request-body-streaming"},
    {MSCONNECTOR_CAPABILITY_RESPONSE_HEADERS, "response-headers"},
    {MSCONNECTOR_CAPABILITY_RESPONSE_BODY_BUFFERED, "response-body-buffered"},
    {MSCONNECTOR_CAPABILITY_RESPONSE_BODY_STREAMING, "response-body-streaming"},
    {MSCONNECTOR_CAPABILITY_AUDIT_LOG_ARTIFACTS, "audit-log-artifacts"},
    {MSCONNECTOR_CAPABILITY_ERROR_LOG_ARTIFACTS, "error-log-artifacts"},
    {MSCONNECTOR_CAPABILITY_RULE_RELOAD, "rule-reload"},
    {MSCONNECTOR_CAPABILITY_CONFIG_RELOAD, "config-reload"},
    {MSCONNECTOR_CAPABILITY_CUSTOM_TRANSACTION_ID, "custom-transaction-id"},
    {MSCONNECTOR_CAPABILITY_PHASE4_HARD_ABORT, "phase4-hard-abort"},
    {MSCONNECTOR_CAPABILITY_PHASE4_RULE_EVALUATION, "phase4-rule-evaluation"},
    {MSCONNECTOR_CAPABILITY_PHASE4_PRE_COMMIT_DENY, "phase4-pre-commit-deny"},
    {MSCONNECTOR_CAPABILITY_LATE_INTERVENTION_LOG_ONLY, "late-intervention-log-only"},
    {MSCONNECTOR_CAPABILITY_LATE_INTERVENTION_ABORT, "late-intervention-abort"},
    {MSCONNECTOR_CAPABILITY_LATE_INTERVENTION_STATUS_METADATA, "late-intervention-status-metadata"},
};

const char *msconnector_capability_name(enum msconnector_capability_flag flag) {
    for (unsigned int index = 0; index < sizeof(capability_names) / sizeof(capability_names[0]); ++index) {
        if (capability_names[index].flag == flag) {
            return capability_names[index].name;
        }
    }
    return "unknown";
}

enum msconnector_capability_flag msconnector_capability_from_name(const char *name) {
    if (name == 0) {
        return MSCONNECTOR_CAPABILITY_NONE;
    }
    for (unsigned int index = 0; index < sizeof(capability_names) / sizeof(capability_names[0]); ++index) {
        if (strcmp(capability_names[index].name, name) == 0) {
            return capability_names[index].flag;
        }
    }
    return MSCONNECTOR_CAPABILITY_NONE;
}

msconnector_capability_flags msconnector_capabilities_add(
    msconnector_capability_flags flags,
    enum msconnector_capability_flag flag) {
    return flags | (msconnector_capability_flags)flag;
}
