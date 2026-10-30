#include "haproxy_spoa_agent_starter.h"

#include <string.h>

static const char *default_block_path = "/modsecurity-haproxy-starter-block";

haproxy_spoa_agent_starter_config haproxy_spoa_agent_starter_default_config(void) {
    haproxy_spoa_agent_starter_config config;
    config.block_path = default_block_path;
    config.block_status = 403;
    return config;
}

const char *haproxy_spoa_agent_starter_description(void) {
    return "HAProxy SPOA agent starter: local request-decision logic only";
}

const char *haproxy_spoa_agent_starter_limitations(void) {
    return "no SPOP frame parser, no HAProxy runtime harness, no libmodsecurity binding, no CRS loading";
}

enum msconnector_status haproxy_spoa_agent_starter_evaluate_request(
    const haproxy_spoa_agent_starter_config *config,
    const msconnector_request *request,
    msconnector_intervention *intervention) {
    haproxy_spoa_agent_starter_config effective_config;

    if (intervention == 0) {
        return MSCONNECTOR_STATUS_ERROR;
    }

    *intervention = msconnector_intervention_none();

    if (request == 0 || request->method == 0 || request->uri == 0) {
        return MSCONNECTOR_STATUS_BLOCKED;
    }

    effective_config = config != 0 ? *config : haproxy_spoa_agent_starter_default_config();
    if (effective_config.block_path == 0 || effective_config.block_status <= 0) {
        return MSCONNECTOR_STATUS_ERROR;
    }

    if (strcmp(request->uri, effective_config.block_path) == 0) {
        *intervention = msconnector_intervention_make(
            1,
            effective_config.block_status,
            0,
            "HAProxy SPOA starter local block decision");
    }

    return MSCONNECTOR_STATUS_OK;
}
