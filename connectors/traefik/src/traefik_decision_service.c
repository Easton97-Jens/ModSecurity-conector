#include "traefik_decision_service.h"

#include <string.h>

static int string_equals(const char *left, const char *right) {
    return left != 0 && right != 0 && strcmp(left, right) == 0;
}

static int header_matches(
    const msconnector_header *header,
    const char *name,
    size_t name_size,
    const char *value,
    size_t value_size) {
    if (header == 0 || name == 0 || value == 0 || header->name == 0 || header->value == 0) {
        return 0;
    }

    return header->name_size == name_size && header->value_size == value_size &&
        strncmp(header->name, name, name_size) == 0 &&
        strncmp(header->value, value, value_size) == 0;
}

static int has_block_header(const msconnector_request *request) {
    if (request == 0 || request->headers == 0) {
        return 0;
    }

    for (size_t index = 0; index < request->header_count; ++index) {
        if (header_matches(
                &request->headers[index],
                "X-ModSecurity-Connector-Decision",
                sizeof("X-ModSecurity-Connector-Decision") - 1U,
                "block",
                sizeof("block") - 1U)) {
            return 1;
        }
    }

    return 0;
}

msconnector_traefik_decision_result msconnector_traefik_decide_request(
    const msconnector_request *request) {
    msconnector_traefik_decision_result result;

    if (request == 0) {
        return msconnector_decision_make(
            MSCONNECTOR_STATUS_ERROR,
            msconnector_intervention_make(1, 500, 0, "missing request"),
            0,
            "missing-request");
    }

    if (string_equals(request->uri, "/__traefik_decision_service_block") || has_block_header(request)) {
        return msconnector_decision_block(
            403,
            "traefik-local-starter-block-rule",
            "local decision-service starter block");
    }

    result = msconnector_decision_allow(0, "local-starter-allow");
    return result;
}

int msconnector_traefik_decision_service_self_test(void) {
    const msconnector_header block_header = {
        "X-ModSecurity-Connector-Decision",
        sizeof("X-ModSecurity-Connector-Decision") - 1,
        "block",
        sizeof("block") - 1
    };
    const msconnector_request allow_request = {
        "GET",
        "/",
        "HTTP/1.1",
        "example.test",
        {"127.0.0.1", 12345},
        {"127.0.0.1", 8080},
        0,
        0,
        {0, 0}
    };
    const msconnector_request uri_block_request = {
        "GET",
        "/__traefik_decision_service_block",
        "HTTP/1.1",
        "example.test",
        {"127.0.0.1", 12345},
        {"127.0.0.1", 8080},
        0,
        0,
        {0, 0}
    };
    const msconnector_request header_block_request = {
        "GET",
        "/",
        "HTTP/1.1",
        "example.test",
        {"127.0.0.1", 12345},
        {"127.0.0.1", 8080},
        &block_header,
        1,
        {0, 0}
    };
    msconnector_traefik_decision_result result;

    result = msconnector_traefik_decide_request(&allow_request);
    if (result.status != MSCONNECTOR_STATUS_OK ||
        msconnector_intervention_is_disruptive(&result.intervention)) {
        return 1;
    }

    result = msconnector_traefik_decide_request(&uri_block_request);
    if (result.status != MSCONNECTOR_STATUS_BLOCKED ||
        !msconnector_intervention_is_disruptive(&result.intervention) ||
        result.intervention.status != 403) {
        return 1;
    }

    result = msconnector_traefik_decide_request(&header_block_request);
    if (result.status != MSCONNECTOR_STATUS_BLOCKED ||
        !msconnector_intervention_is_disruptive(&result.intervention) ||
        result.intervention.status != 403) {
        return 1;
    }

    return 0;
}
