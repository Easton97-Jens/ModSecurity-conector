#include "connectors/lighttpd/src/lighttpd_bridge.h"

#include <string.h>

const char *msconnector_lighttpd_bridge_starter_kind(void) {
    return "decision-service-bridge-starter";
}

msconnector_capabilities msconnector_lighttpd_bridge_starter_capabilities(void) {
    msconnector_capabilities capabilities;
    capabilities.flags = MSCONNECTOR_CAPABILITY_NONE;
    capabilities.connector_name = "lighttpd bridge starter";
    capabilities.connector_version = "not-runtime-verified";
    capabilities.server_family = "lighttpd";
    capabilities.notes = "local decision-service bridge starter only; no lighttpd traffic, FastCGI/SCGI protocol, or libmodsecurity runtime integration";
    return capabilities;
}

msconnector_request msconnector_lighttpd_bridge_make_probe_request(
    const char *method,
    const char *uri) {
    msconnector_request request;
    memset(&request, 0, sizeof(request));
    request.method = method;
    request.uri = uri;
    request.http_version = "HTTP/1.1";
    request.hostname = "localhost";
    return request;
}

msconnector_lighttpd_bridge_decision msconnector_lighttpd_bridge_evaluate_probe(
    const msconnector_request *request) {
    msconnector_lighttpd_bridge_decision decision;

    if (request == 0 || request->method == 0 || request->uri == 0) {
        decision.status = MSCONNECTOR_STATUS_ERROR;
        decision.intervention = msconnector_intervention_none();
        decision.reason = "invalid local probe request";
        return decision;
    }

    decision.status = MSCONNECTOR_STATUS_BLOCKED;
    decision.intervention = msconnector_intervention_none();
    decision.reason = "blocked: bridge starter has no lighttpd runtime hook, FastCGI/SCGI protocol adapter, or libmodsecurity integration";
    return decision;
}

enum msconnector_status msconnector_lighttpd_bridge_self_test(void) {
    msconnector_capabilities capabilities;
    msconnector_request request;
    msconnector_lighttpd_bridge_decision decision;

    capabilities = msconnector_lighttpd_bridge_starter_capabilities();
    if (capabilities.flags != MSCONNECTOR_CAPABILITY_NONE) {
        return MSCONNECTOR_STATUS_ERROR;
    }
    if (strcmp(msconnector_lighttpd_bridge_starter_kind(), "decision-service-bridge-starter") != 0) {
        return MSCONNECTOR_STATUS_ERROR;
    }

    request = msconnector_lighttpd_bridge_make_probe_request("GET", "/");
    decision = msconnector_lighttpd_bridge_evaluate_probe(&request);
    if (decision.status != MSCONNECTOR_STATUS_BLOCKED) {
        return MSCONNECTOR_STATUS_ERROR;
    }
    if (msconnector_intervention_is_disruptive(&decision.intervention)) {
        return MSCONNECTOR_STATUS_ERROR;
    }
    return MSCONNECTOR_STATUS_OK;
}
