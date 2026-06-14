#ifndef MSCONNECTOR_HAPROXY_SPOA_AGENT_STARTER_H
#define MSCONNECTOR_HAPROXY_SPOA_AGENT_STARTER_H

#include "msconnector/intervention.h"
#include "msconnector/request.h"
#include "msconnector/status.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct haproxy_spoa_agent_starter_config {
    const char *block_path;
    int block_status;
} haproxy_spoa_agent_starter_config;

haproxy_spoa_agent_starter_config haproxy_spoa_agent_starter_default_config(void);

enum msconnector_status haproxy_spoa_agent_starter_evaluate_request(
    const haproxy_spoa_agent_starter_config *config,
    const msconnector_request *request,
    msconnector_intervention *intervention);

int haproxy_spoa_agent_starter_self_test(void);
const char *haproxy_spoa_agent_starter_description(void);
const char *haproxy_spoa_agent_starter_limitations(void);

#ifdef __cplusplus
}
#endif

#endif
