#include "msconnector/block_statuses.h"

int msconnector_block_status_is_allowed(int status) {
    return msconnector_http_status_is_block_response(status);
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
    if (!msconnector_http_status_is_valid(status)) {
        return "Unknown";
    }
    if (msconnector_http_status_info_find(status) == 0) {
        return "Unknown";
    }
    return msconnector_http_status_reason_phrase(status);
}
