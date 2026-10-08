#ifndef NGX_HTTP_MODSECURITY_CLEANUP_OBSERVATION_H
#define NGX_HTTP_MODSECURITY_CLEANUP_OBSERVATION_H

#include "msconnector/event.h"
#include "msconnector/transaction_contract.h"
#include <stdbool.h>
#include <stdio.h>

/* Call only after actual Common cleanup and the native void cleanup returned.
 * native_cleanup_completed is true only if a native transaction existed and
 * its cleanup returned. No native getter may be called after cleanup.
 * The caller supplies actual source identity separately and keeps reason alive
 * through serialization. LOGGING/allow describes cleanup, not request consent.
 * Returns 1 on construction; 0 leaves event unchanged on invalid/truncated input.
 */
static inline int
ngx_http_modsecurity_cleanup_observation(msconnector_event *event,
    char *reason, size_t reason_size, int common_return,
    const msconnector_transaction_contract *contract,
    bool native_cleanup_completed)
{
    msconnector_event observation = {0};
    const char *error_class;
    int written;
    int complete;

    if (event == NULL || reason == NULL || reason_size == 0 || contract == NULL) {
        return 0;
    }
    error_class = msconnector_transaction_error_class_name(contract->error_class);
    written = snprintf(reason, reason_size,
        "common_return=%d;common_complete=%d;native_cleanup_completed=%d;error_class=%s",
        common_return, contract->cleanup_complete,
        native_cleanup_completed ? 1 : 0, error_class);
    if (written < 0 || (size_t)written >= reason_size) {
        reason[0] = '\0';
        return 0;
    }
    complete = common_return == 0 && contract->cleanup_complete == 1;
    observation.meta.event = "transaction_cleanup";
    observation.meta.message_id = "MSCONN_TRANSACTION_CLEANUP";
    observation.decision.phase = MSCONNECTOR_PHASE_LOGGING;
    observation.decision.status = complete ? MSCONNECTOR_STATUS_OK : MSCONNECTOR_STATUS_ERROR;
    observation.decision.action = complete ? "allow" : "error";
    observation.decision.actual_action = observation.decision.action;
    observation.decision.reason = reason;
    observation.flags.cleanup_reason = contract->error_class == MSCONNECTOR_TRANSACTION_ERROR_NONE
        ? "normal" : error_class;
    *event = observation;
    return 1;
}

#endif
