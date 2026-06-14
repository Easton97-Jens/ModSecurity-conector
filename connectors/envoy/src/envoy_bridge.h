#ifndef MSCONNECTOR_ENVOY_BRIDGE_H
#define MSCONNECTOR_ENVOY_BRIDGE_H

#include "msconnector/intervention.h"
#include "msconnector/request.h"
#include "msconnector/status.h"

#ifdef __cplusplus
extern "C" {
#endif

#define MSCONNECTOR_ENVOY_BRIDGE_BLOCK_HEADER "x-msconnector-block"
#define MSCONNECTOR_ENVOY_BRIDGE_BLOCK_QUERY "msconnector_block=1"

typedef struct msconnector_envoy_bridge_decision {
    enum msconnector_status status;
    msconnector_intervention intervention;
    const char *rule_id;
    const char *reason;
} msconnector_envoy_bridge_decision;

msconnector_envoy_bridge_decision msconnector_envoy_bridge_evaluate(
    const msconnector_request *request);
int msconnector_envoy_bridge_self_test(void);

#ifdef __cplusplus
}
#endif

#endif
