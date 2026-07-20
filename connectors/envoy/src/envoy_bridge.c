#include "envoy_bridge.h"

#include <string.h>

static int string_equals(const char *left, size_t left_size, const char *right, size_t right_size) {
    if (left == 0 || right == 0) {
        return 0;
    }
    return left_size == right_size && memcmp(left, right, right_size) == 0;
}

static int value_is_block(const char *value, size_t value_size) {
    return string_equals(value, value_size, "1", sizeof("1") - 1U) ||
        string_equals(value, value_size, "true", sizeof("true") - 1U) ||
        string_equals(value, value_size, "block", sizeof("block") - 1U);
}

static int uri_contains_bridge_block_query(const char *uri) {
    return uri != 0 && strstr(uri, MSCONNECTOR_ENVOY_BRIDGE_BLOCK_QUERY) != 0;
}

static int request_has_bridge_block_header(const msconnector_request *request) {
    if (request == 0 || request->headers == 0) {
        return 0;
    }
    for (size_t index = 0; index < request->header_count; ++index) {
        const msconnector_header *header = &request->headers[index];
        if (string_equals(header->name, header->name_size,
                MSCONNECTOR_ENVOY_BRIDGE_BLOCK_HEADER,
                sizeof(MSCONNECTOR_ENVOY_BRIDGE_BLOCK_HEADER) - 1U) &&
            value_is_block(header->value, header->value_size)) {
            return 1;
        }
    }
    return 0;
}

static msconnector_envoy_bridge_decision allow_decision(void) {
    return msconnector_decision_allow(
        "envoy-bridge-self-test-allow",
        "no bridge self-test blocking signal");
}

static msconnector_envoy_bridge_decision block_decision(const char *rule_id, const char *reason) {
    return msconnector_decision_block(403, rule_id, reason);
}

msconnector_envoy_bridge_decision msconnector_envoy_bridge_evaluate(
    const msconnector_request *request) {
    if (request_has_bridge_block_header(request)) {
        return block_decision("envoy-bridge-self-test-header",
            "bridge self-test header requested block");
    }
    if (request != 0 && uri_contains_bridge_block_query(request->uri)) {
        return block_decision("envoy-bridge-self-test-uri",
            "bridge self-test URI query requested block");
    }
    return allow_decision();
}

int msconnector_envoy_bridge_self_test(void) {
    const msconnector_header block_headers[] = {
        {MSCONNECTOR_ENVOY_BRIDGE_BLOCK_HEADER,
            sizeof(MSCONNECTOR_ENVOY_BRIDGE_BLOCK_HEADER) - 1,
            "1",
            1}
    };
    const msconnector_request allow_request = {
        "GET",
        "/allowed",
        "HTTP/1.1",
        "example.test",
        {"127.0.0.1", 12345},
        {"127.0.0.1", 10000},
        0,
        0,
        {0, 0}
    };
    const msconnector_request header_block_request = {
        "GET",
        "/blocked-by-header",
        "HTTP/1.1",
        "example.test",
        {"127.0.0.1", 12345},
        {"127.0.0.1", 10000},
        block_headers,
        sizeof(block_headers) / sizeof(block_headers[0]),
        {0, 0}
    };
    const msconnector_request uri_block_request = {
        "GET",
        "/blocked?msconnector_block=1",
        "HTTP/1.1",
        "example.test",
        {"127.0.0.1", 12345},
        {"127.0.0.1", 10000},
        0,
        0,
        {0, 0}
    };
    msconnector_envoy_bridge_decision allow_result;
    msconnector_envoy_bridge_decision header_block_result;
    msconnector_envoy_bridge_decision uri_block_result;

    allow_result = msconnector_envoy_bridge_evaluate(&allow_request);
    header_block_result = msconnector_envoy_bridge_evaluate(&header_block_request);
    uri_block_result = msconnector_envoy_bridge_evaluate(&uri_block_request);

    if (allow_result.status != MSCONNECTOR_STATUS_OK ||
        msconnector_intervention_is_disruptive(&allow_result.intervention)) {
        return 1;
    }
    if (header_block_result.status != MSCONNECTOR_STATUS_BLOCKED ||
        !msconnector_intervention_is_disruptive(&header_block_result.intervention) ||
        header_block_result.intervention.status != 403) {
        return 1;
    }
    if (uri_block_result.status != MSCONNECTOR_STATUS_BLOCKED ||
        !msconnector_intervention_is_disruptive(&uri_block_result.intervention) ||
        uri_block_result.intervention.status != 403) {
        return 1;
    }
    return 0;
}
