#ifndef MSCONNECTOR_TRANSACTION_H
#define MSCONNECTOR_TRANSACTION_H

#include "msconnector/decision.h"
#include "msconnector/intervention.h"
#include "msconnector/phase.h"
#include "msconnector/request.h"
#include "msconnector/response.h"
#include "msconnector/status.h"

#ifdef __cplusplus
extern "C" {
#endif


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
