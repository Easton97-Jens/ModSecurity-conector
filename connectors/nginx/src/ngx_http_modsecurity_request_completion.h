#ifndef NGX_HTTP_MODSECURITY_REQUEST_COMPLETION_H
#define NGX_HTTP_MODSECURITY_REQUEST_COMPLETION_H

#include "msconnector/event.h"
#include "msconnector/transaction_contract.h"

/* This describes only the completed native/Common P1 boundary. The caller
 * must first collect intervention and reach its no-intervention continuation;
 * neither a host response nor full-request allow is observed here. All borrowed
 * metadata remains live for the synchronous request-event writer. */
static inline int
ngx_http_modsecurity_request_completion(msconnector_event *event,
    const msconnector_transaction_contract *contract, int native_result)
{
    if (event == NULL || contract == NULL || native_result != 1 ||
        contract->status != MSCONNECTOR_TRANSACTION_STATUS_WAITING_FOR_NEXT_PHASE ||
        contract->active_phase != -1 ||
        contract->last_completed_phase != MSCONNECTOR_PHASE_REQUEST_HEADERS ||
        contract->completed_phase_mask != MSCONNECTOR_TRANSACTION_PHASE_MASK_P1 ||
        contract->error_class != MSCONNECTOR_TRANSACTION_ERROR_NONE ||
        contract->cleanup_started || contract->cleanup_complete) {
        return 0;
    }
    msconnector_event_init(event);
    event->meta.message_id = "MSCONN_PHASE1_COMPLETE";
    event->meta.message = "Native request headers processing completed.";
    event->meta.event = "request_headers_complete";
    event->meta.connector = "nginx";
    event->meta.integration_mode = "native-nginx-http-module";
    event->meta.transaction_id = contract->transaction_id;
    event->decision.phase = MSCONNECTOR_PHASE_REQUEST_HEADERS;
    event->decision.status = MSCONNECTOR_STATUS_OK;
    event->decision.action = "allow";
    event->decision.requested_action = "allow";
    event->decision.actual_action = "";
    event->decision.rule_id = "";
    event->decision.reason = "native_return=1;common_completed=1";
    event->http.transport_result = "not_observable";
    return 1;
}

#endif
