#include "msconnector/capability_matrix.h"

const char *msconnector_capability_required_test(enum msconnector_capability_flag flag) {
    switch (flag) {
    case MSCONNECTOR_CAPABILITY_CONNECTION_METADATA: return "connection metadata smoke";
    case MSCONNECTOR_CAPABILITY_REQUEST_HEADERS: return "phase1 request header rule test";
    case MSCONNECTOR_CAPABILITY_REQUEST_BODY_BUFFERED: return "phase2 request body rule test";
    case MSCONNECTOR_CAPABILITY_REQUEST_BODY_STREAMING: return "request body streaming capability test";
    case MSCONNECTOR_CAPABILITY_RESPONSE_HEADERS: return "phase3 response header rule test";
    case MSCONNECTOR_CAPABILITY_RESPONSE_BODY_BUFFERED: return "phase4 response body rule test";
    case MSCONNECTOR_CAPABILITY_RESPONSE_BODY_STREAMING: return "response body streaming capability test";
    case MSCONNECTOR_CAPABILITY_AUDIT_LOG_ARTIFACTS: return "audit log artifact exists";
    case MSCONNECTOR_CAPABILITY_ERROR_LOG_ARTIFACTS: return "error log artifact exists";
    case MSCONNECTOR_CAPABILITY_RULE_RELOAD: return "rule reload test";
    case MSCONNECTOR_CAPABILITY_CONFIG_RELOAD: return "config reload test";
    case MSCONNECTOR_CAPABILITY_CUSTOM_TRANSACTION_ID: return "transaction id visible in event/log output";
    case MSCONNECTOR_CAPABILITY_PHASE4_HARD_ABORT: return "phase4 hard-abort-after-200 event test";
    case MSCONNECTOR_CAPABILITY_PHASE4_RULE_EVALUATION: return "phase4 rule-observed event test";
    case MSCONNECTOR_CAPABILITY_PHASE4_PRE_COMMIT_DENY: return "phase4 pre-commit deny status test";
    case MSCONNECTOR_CAPABILITY_LATE_INTERVENTION_LOG_ONLY: return "phase4 post-commit log-only event test";
    case MSCONNECTOR_CAPABILITY_LATE_INTERVENTION_ABORT: return "phase4 post-commit abort event test";
    case MSCONNECTOR_CAPABILITY_LATE_INTERVENTION_STATUS_METADATA: return "phase4 requested/original/visible status metadata test";
    case MSCONNECTOR_CAPABILITY_NONE: default: return 0;
    }
}

int msconnector_capability_has_required_test(enum msconnector_capability_flag flag) { return msconnector_capability_required_test(flag) != 0; }
