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
};

const char *msconnector_capability_name(enum msconnector_capability_flag flag) {
    unsigned int index;
    for (index = 0; index < sizeof(capability_names) / sizeof(capability_names[0]); ++index) {
        if (capability_names[index].flag == flag) {
            return capability_names[index].name;
        }
    }
    return "unknown";
}

enum msconnector_capability_flag msconnector_capability_from_name(const char *name) {
    unsigned int index;
    if (name == 0) {
        return MSCONNECTOR_CAPABILITY_NONE;
    }
    for (index = 0; index < sizeof(capability_names) / sizeof(capability_names[0]); ++index) {
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
