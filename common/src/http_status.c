#include "msconnector/http_status.h"

#define MSCONNECTOR_HTTP_STATUS_MIN 100
#define MSCONNECTOR_HTTP_STATUS_MAX 599

static const char *const UNKNOWN_REASON_PHRASE = "Unknown Status";
static const char *const INVALID_REASON_PHRASE = "Invalid Status";
static const char *const UNKNOWN_DEFAULT_MESSAGE = "HTTP status";
static const char *const INVALID_DEFAULT_MESSAGE = "Invalid HTTP status";

static const msconnector_http_status_info http_statuses[] = {
    {200, "OK", "Request succeeded", MSCONNECTOR_HTTP_STATUS_CLASS_SUCCESS, 0},
    {302, "Found", "Redirect response", MSCONNECTOR_HTTP_STATUS_CLASS_REDIRECTION, 0},
    {400, "Bad Request", "Bad request", MSCONNECTOR_HTTP_STATUS_CLASS_CLIENT_ERROR, 1},
    {401, "Unauthorized", "Authentication required", MSCONNECTOR_HTTP_STATUS_CLASS_CLIENT_ERROR, 1},
    {403, "Forbidden", "Request blocked", MSCONNECTOR_HTTP_STATUS_CLASS_CLIENT_ERROR, 1},
    {404, "Not Found", "Resource not found", MSCONNECTOR_HTTP_STATUS_CLASS_CLIENT_ERROR, 1},
    {405, "Method Not Allowed", "Method not allowed", MSCONNECTOR_HTTP_STATUS_CLASS_CLIENT_ERROR, 1},
    {406, "Not Acceptable", "Request not acceptable", MSCONNECTOR_HTTP_STATUS_CLASS_CLIENT_ERROR, 1},
    {408, "Request Timeout", "Request timeout", MSCONNECTOR_HTTP_STATUS_CLASS_CLIENT_ERROR, 1},
    {409, "Conflict", "Request conflict", MSCONNECTOR_HTTP_STATUS_CLASS_CLIENT_ERROR, 1},
    {410, "Gone", "Resource is gone", MSCONNECTOR_HTTP_STATUS_CLASS_CLIENT_ERROR, 1},
    {413, "Payload Too Large", "Payload too large", MSCONNECTOR_HTTP_STATUS_CLASS_CLIENT_ERROR, 1},
    {415, "Unsupported Media Type", "Unsupported media type", MSCONNECTOR_HTTP_STATUS_CLASS_CLIENT_ERROR, 1},
    {418, "I'm a teapot", "Request cannot be processed", MSCONNECTOR_HTTP_STATUS_CLASS_CLIENT_ERROR, 1},
    {422, "Unprocessable Content", "Unprocessable content", MSCONNECTOR_HTTP_STATUS_CLASS_CLIENT_ERROR, 1},
    {425, "Too Early", "Request sent too early", MSCONNECTOR_HTTP_STATUS_CLASS_CLIENT_ERROR, 1},
    {429, "Too Many Requests", "Too many requests", MSCONNECTOR_HTTP_STATUS_CLASS_CLIENT_ERROR, 1},
    {451, "Unavailable For Legal Reasons", "Unavailable for legal reasons", MSCONNECTOR_HTTP_STATUS_CLASS_CLIENT_ERROR, 1},
    {500, "Internal Server Error", "Internal error", MSCONNECTOR_HTTP_STATUS_CLASS_SERVER_ERROR, 1},
    {501, "Not Implemented", "Requested capability is not implemented", MSCONNECTOR_HTTP_STATUS_CLASS_SERVER_ERROR, 1},
    {502, "Bad Gateway", "Bad gateway", MSCONNECTOR_HTTP_STATUS_CLASS_SERVER_ERROR, 1},
    {503, "Service Unavailable", "Service unavailable", MSCONNECTOR_HTTP_STATUS_CLASS_SERVER_ERROR, 1},
    {504, "Gateway Timeout", "Gateway timeout", MSCONNECTOR_HTTP_STATUS_CLASS_SERVER_ERROR, 1},
};

int msconnector_http_status_is_valid(int status) {
    return status >= MSCONNECTOR_HTTP_STATUS_MIN && status <= MSCONNECTOR_HTTP_STATUS_MAX;
}

msconnector_http_status_class msconnector_http_status_classify(int status) {
    if (!msconnector_http_status_is_valid(status)) {
        return MSCONNECTOR_HTTP_STATUS_CLASS_UNKNOWN;
    }

    if (status < 200) {
        return MSCONNECTOR_HTTP_STATUS_CLASS_INFORMATIONAL;
    }
    if (status < 300) {
        return MSCONNECTOR_HTTP_STATUS_CLASS_SUCCESS;
    }
    if (status < 400) {
        return MSCONNECTOR_HTTP_STATUS_CLASS_REDIRECTION;
    }
    if (status < 500) {
        return MSCONNECTOR_HTTP_STATUS_CLASS_CLIENT_ERROR;
    }
    return MSCONNECTOR_HTTP_STATUS_CLASS_SERVER_ERROR;
}

const msconnector_http_status_info *msconnector_http_status_info_find(int status) {
    const unsigned int count = (unsigned int)(sizeof(http_statuses) / sizeof(http_statuses[0]));

    for (unsigned int index = 0; index < count; ++index) {
        if (http_statuses[index].status == status) {
            return &http_statuses[index];
        }
    }

    return 0;
}

const char *msconnector_http_status_reason_phrase(int status) {
    const msconnector_http_status_info *info;

    if (!msconnector_http_status_is_valid(status)) {
        return INVALID_REASON_PHRASE;
    }

    info = msconnector_http_status_info_find(status);
    if (info == 0) {
        return UNKNOWN_REASON_PHRASE;
    }
    return info->reason_phrase;
}

const char *msconnector_http_status_default_message(int status) {
    const msconnector_http_status_info *info;

    if (!msconnector_http_status_is_valid(status)) {
        return INVALID_DEFAULT_MESSAGE;
    }

    info = msconnector_http_status_info_find(status);
    if (info == 0) {
        return UNKNOWN_DEFAULT_MESSAGE;
    }
    return info->default_message;
}

int msconnector_http_status_is_error(int status) {
    const msconnector_http_status_class status_class = msconnector_http_status_classify(status);
    return status_class == MSCONNECTOR_HTTP_STATUS_CLASS_CLIENT_ERROR ||
        status_class == MSCONNECTOR_HTTP_STATUS_CLASS_SERVER_ERROR;
}

int msconnector_http_status_is_block_response(int status) {
    const msconnector_http_status_info *info = msconnector_http_status_info_find(status);
    return info != 0 && info->suitable_for_blocking != 0;
}
