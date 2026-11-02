#include "msconnector/late_intervention.h"

#include <string.h>

const char *msconnector_protocol_kind_name(
    msconnector_protocol_kind protocol) {
    switch (protocol) {
    case MSCONNECTOR_PROTOCOL_HTTP_1_1:
        return "http1";
    case MSCONNECTOR_PROTOCOL_HTTP_2:
        return "h2";
    case MSCONNECTOR_PROTOCOL_HTTP_3:
        return "h3";
    case MSCONNECTOR_PROTOCOL_UNKNOWN:
    default:
        return "unknown";
    }
}

msconnector_protocol_kind msconnector_protocol_kind_parse(const char *value) {
    if (value == 0 || value[0] == '\0') {
        return MSCONNECTOR_PROTOCOL_UNKNOWN;
    }

    if (strcmp(value, "1.1") == 0 || strcmp(value, "HTTP/1.1") == 0 ||
        strcmp(value, "HTTP 1.1") == 0 || strcmp(value, "http1") == 0 ||
        strcmp(value, "h1") == 0) {
        return MSCONNECTOR_PROTOCOL_HTTP_1_1;
    }
    if (strcmp(value, "2") == 0 || strcmp(value, "2.0") == 0 ||
        strcmp(value, "HTTP/2") == 0 || strcmp(value, "HTTP/2.0") == 0 ||
        strcmp(value, "HTTP 2") == 0 || strcmp(value, "HTTP 2.0") == 0 ||
        strcmp(value, "http2") == 0 || strcmp(value, "h2") == 0) {
        return MSCONNECTOR_PROTOCOL_HTTP_2;
    }
    if (strcmp(value, "3") == 0 || strcmp(value, "3.0") == 0 ||
        strcmp(value, "HTTP/3") == 0 || strcmp(value, "HTTP/3.0") == 0 ||
        strcmp(value, "HTTP 3") == 0 || strcmp(value, "HTTP 3.0") == 0 ||
        strcmp(value, "http3") == 0 || strcmp(value, "h3") == 0) {
        return MSCONNECTOR_PROTOCOL_HTTP_3;
    }
    return MSCONNECTOR_PROTOCOL_UNKNOWN;
}

int msconnector_protocol_is_multiplexed(msconnector_protocol_kind protocol) {
	return protocol == MSCONNECTOR_PROTOCOL_HTTP_2 ||
		protocol == MSCONNECTOR_PROTOCOL_HTTP_3;
}

static msconnector_late_intervention_action
msconnector_late_intervention_policy_action_sanitize(
    msconnector_late_intervention_action action) {
    switch (action) {
    case MSCONNECTOR_LATE_INTERVENTION_LOG_ONLY:
    case MSCONNECTOR_LATE_INTERVENTION_DENY_IF_POSSIBLE:
    case MSCONNECTOR_LATE_INTERVENTION_ABORT_CONNECTION:
        return action;
    case MSCONNECTOR_LATE_INTERVENTION_STREAM_RESET:
    default:
        /* A reset is safe only after resolve_for_context has verified the
         * multiplexed transport, stream identity, and host capability. */
        return MSCONNECTOR_LATE_INTERVENTION_LOG_ONLY;
    }
}

void msconnector_late_intervention_policy_init(
    msconnector_late_intervention_policy *policy) {
    if (policy == 0) {
        return;
    }

    policy->default_action = MSCONNECTOR_LATE_INTERVENTION_LOG_ONLY;
    policy->strict_action = MSCONNECTOR_LATE_INTERVENTION_ABORT_CONNECTION;
}

void msconnector_late_intervention_context_init(
    msconnector_late_intervention_context *context) {
    if (context == 0) {
        return;
    }

    context->protocol = MSCONNECTOR_PROTOCOL_UNKNOWN;
    context->stream_id = 0U;
    context->has_stream_id = 0;
    context->input_ended = 0;
    context->output_ended = 0;
    context->response_headers_committed = 0;
    context->response_body_started = 0;
    context->stream_reset_supported = 0;
}

const char *msconnector_late_intervention_action_name(
    msconnector_late_intervention_action action) {
    switch (action) {
    case MSCONNECTOR_LATE_INTERVENTION_LOG_ONLY:
        return "log_only";
    case MSCONNECTOR_LATE_INTERVENTION_DENY_IF_POSSIBLE:
        return "deny_if_possible";
    case MSCONNECTOR_LATE_INTERVENTION_ABORT_CONNECTION:
        return "abort_connection";
    case MSCONNECTOR_LATE_INTERVENTION_STREAM_RESET:
        return "stream_reset";
    default:
        return "unknown";
    }
}

msconnector_late_intervention_action msconnector_late_intervention_resolve(
    const msconnector_late_intervention_policy *policy,
    int response_headers_committed,
    int response_body_started,
    int strict_mode) {
    msconnector_late_intervention_policy fallback_policy;

    if (policy == 0) {
        msconnector_late_intervention_policy_init(&fallback_policy);
        policy = &fallback_policy;
    }

    if (response_headers_committed || response_body_started) {
        if (strict_mode) {
            return msconnector_late_intervention_policy_action_sanitize(
                policy->strict_action);
        }
        return msconnector_late_intervention_policy_action_sanitize(
            policy->default_action);
    }

    return MSCONNECTOR_LATE_INTERVENTION_DENY_IF_POSSIBLE;
}

msconnector_late_intervention_action
msconnector_late_intervention_resolve_for_context(
    const msconnector_late_intervention_policy *policy,
    const msconnector_late_intervention_context *context,
    int strict_mode) {
    msconnector_late_intervention_context fallback_context;
    msconnector_late_intervention_action action;

    if (context == 0) {
        msconnector_late_intervention_context_init(&fallback_context);
        context = &fallback_context;
    }

    if (context->output_ended) {
        return MSCONNECTOR_LATE_INTERVENTION_LOG_ONLY;
    }

    action = msconnector_late_intervention_resolve(policy,
        context->response_headers_committed,
        context->response_body_started, strict_mode);
    if (action != MSCONNECTOR_LATE_INTERVENTION_ABORT_CONNECTION ||
        !msconnector_protocol_is_multiplexed(context->protocol) ||
        !context->has_stream_id || !context->stream_reset_supported ||
        /* HTTP/2 stream zero is connection control and can never carry a
         * RST_STREAM. HTTP/3 stream zero remains a valid request stream. */
        (context->protocol == MSCONNECTOR_PROTOCOL_HTTP_2 &&
         context->stream_id == 0U)) {
        return action;
    }

    return MSCONNECTOR_LATE_INTERVENTION_STREAM_RESET;
}
