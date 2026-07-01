#include "msconnector/block_statuses.h"

int msconnector_http_status_is_valid(int status) {
    return status >= 100 && status <= 599;
}

int msconnector_block_status_is_allowed(int status) {
    switch (status) {
    case 400:
    case 401:
    case 403:
    case 404:
    case 405:
    case 406:
    case 408:
    case 409:
    case 410:
    case 413:
    case 415:
    case 418:
    case 422:
    case 425:
    case 429:
    case 451:
    case 500:
    case 501:
    case 502:
    case 503:
    case 504:
        return 1;
    default:
        return 0;
    }
}

int msconnector_block_status_normalize(int requested_status) {
    if (requested_status == 0) {
        return MSCONNECTOR_DEFAULT_BLOCK_STATUS;
    }
    if (!msconnector_http_status_is_valid(requested_status)) {
        return MSCONNECTOR_DEFAULT_ERROR_STATUS;
    }
    if (!msconnector_block_status_is_allowed(requested_status)) {
        return MSCONNECTOR_DEFAULT_ERROR_STATUS;
    }
    return requested_status;
}

const char *msconnector_http_status_name(int status) {
    switch (status) {
    case 400:
        return "Bad Request";
    case 401:
        return "Unauthorized";
    case 403:
        return "Forbidden";
    case 404:
        return "Not Found";
    case 405:
        return "Method Not Allowed";
    case 406:
        return "Not Acceptable";
    case 408:
        return "Request Timeout";
    case 409:
        return "Conflict";
    case 410:
        return "Gone";
    case 413:
        return "Content Too Large";
    case 415:
        return "Unsupported Media Type";
    case 418:
        return "I'm a teapot";
    case 422:
        return "Unprocessable Content";
    case 425:
        return "Too Early";
    case 429:
        return "Too Many Requests";
    case 451:
        return "Unavailable For Legal Reasons";
    case 500:
        return "Internal Server Error";
    case 501:
        return "Not Implemented";
    case 502:
        return "Bad Gateway";
    case 503:
        return "Service Unavailable";
    case 504:
        return "Gateway Timeout";
    default:
        return "Unknown";
    }
}
