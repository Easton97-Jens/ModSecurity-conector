#ifndef MSCONNECTOR_CAPABILITIES_H
#define MSCONNECTOR_CAPABILITIES_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef uint64_t msconnector_capability_flags;

enum msconnector_capability_flag {
    MSCONNECTOR_CAPABILITY_NONE = 0,
    MSCONNECTOR_CAPABILITY_CONNECTION_METADATA = 1ULL << 0,
    MSCONNECTOR_CAPABILITY_REQUEST_HEADERS = 1ULL << 1,
    MSCONNECTOR_CAPABILITY_REQUEST_BODY_BUFFERED = 1ULL << 2,
    MSCONNECTOR_CAPABILITY_REQUEST_BODY_STREAMING = 1ULL << 3,
    MSCONNECTOR_CAPABILITY_RESPONSE_HEADERS = 1ULL << 4,
    MSCONNECTOR_CAPABILITY_RESPONSE_BODY_BUFFERED = 1ULL << 5,
    MSCONNECTOR_CAPABILITY_RESPONSE_BODY_STREAMING = 1ULL << 6,
    MSCONNECTOR_CAPABILITY_AUDIT_LOG_ARTIFACTS = 1ULL << 7,
    MSCONNECTOR_CAPABILITY_ERROR_LOG_ARTIFACTS = 1ULL << 8,
    MSCONNECTOR_CAPABILITY_RULE_RELOAD = 1ULL << 9,
    MSCONNECTOR_CAPABILITY_CONFIG_RELOAD = 1ULL << 10,
    MSCONNECTOR_CAPABILITY_CUSTOM_TRANSACTION_ID = 1ULL << 11,
    MSCONNECTOR_CAPABILITY_PHASE4_HARD_ABORT = 1ULL << 12,
    MSCONNECTOR_CAPABILITY_PHASE4_RULE_EVALUATION = 1ULL << 13,
    MSCONNECTOR_CAPABILITY_PHASE4_PRE_COMMIT_DENY = 1ULL << 14,
    MSCONNECTOR_CAPABILITY_LATE_INTERVENTION_LOG_ONLY = 1ULL << 15,
    MSCONNECTOR_CAPABILITY_LATE_INTERVENTION_ABORT = 1ULL << 16,
    MSCONNECTOR_CAPABILITY_LATE_INTERVENTION_STATUS_METADATA = 1ULL << 17
};

typedef struct msconnector_capabilities {
    msconnector_capability_flags flags;
    const char *connector_name;
    const char *connector_version;
    const char *server_family;
    const char *notes;
} msconnector_capabilities;

static inline int msconnector_capabilities_has(
    const msconnector_capabilities *capabilities,
    enum msconnector_capability_flag flag) {
    return capabilities != 0 && (capabilities->flags & (msconnector_capability_flags)flag) != 0;
}

const char *msconnector_capability_name(enum msconnector_capability_flag flag);
enum msconnector_capability_flag msconnector_capability_from_name(const char *name);
msconnector_capability_flags msconnector_capabilities_add(
    msconnector_capability_flags flags,
    enum msconnector_capability_flag flag);

#ifdef __cplusplus
}
#endif

#endif
