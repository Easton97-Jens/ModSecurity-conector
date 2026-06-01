#ifndef MSCONNECTOR_TRAEFIK_DECISION_SERVICE_H
#define MSCONNECTOR_TRAEFIK_DECISION_SERVICE_H

#include "msconnector/intervention.h"
#include "msconnector/request.h"
#include "msconnector/status.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct msconnector_traefik_decision_result {
    enum msconnector_status status;
    msconnector_intervention intervention;
    const char *reason;
} msconnector_traefik_decision_result;

msconnector_traefik_decision_result msconnector_traefik_decide_request(
    const msconnector_request *request);
int msconnector_traefik_decision_service_self_test(void);

#ifdef __cplusplus
}
#endif

#endif
