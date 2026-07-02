#ifndef MSCONNECTOR_TRANSACTION_H
#define MSCONNECTOR_TRANSACTION_H

#include "msconnector/intervention.h"
#include "msconnector/request.h"
#include "msconnector/response.h"
#include "msconnector/status.h"

#ifdef __cplusplus
extern "C" {
#endif

enum msconnector_phase {
    MSCONNECTOR_PHASE_CONNECTION = 0,
    MSCONNECTOR_PHASE_URI = 1,
    MSCONNECTOR_PHASE_REQUEST_HEADERS = 2,
    MSCONNECTOR_PHASE_REQUEST_BODY = 3,
    MSCONNECTOR_PHASE_RESPONSE_HEADERS = 4,
    MSCONNECTOR_PHASE_RESPONSE_BODY = 5,
    MSCONNECTOR_PHASE_LOGGING = 6
};

typedef struct msconnector_transaction_view {
    const char *transaction_id;
    const msconnector_request *request;
    const msconnector_response *response;
    msconnector_intervention intervention;
} msconnector_transaction_view;

#ifdef __cplusplus
}
#endif

#endif
