#include "msconnector/status.h"

#include <string.h>

const char *msconnector_status_name(enum msconnector_status status) {
    switch (status) {
    case MSCONNECTOR_STATUS_OK:
        return "ok";
    case MSCONNECTOR_STATUS_ERROR:
        return "error";
    case MSCONNECTOR_STATUS_BLOCKED:
        return "blocked";
    case MSCONNECTOR_STATUS_UNSUPPORTED:
        return "unsupported";
    default:
        return "error";
    }
}

enum msconnector_status msconnector_status_from_result(const char *result_status) {
    if (result_status == 0) {
        return MSCONNECTOR_STATUS_ERROR;
    }
    if (strcmp(result_status, "pass") == 0) {
        return MSCONNECTOR_STATUS_OK;
    }
    if (strcmp(result_status, "blocked") == 0) {
        return MSCONNECTOR_STATUS_BLOCKED;
    }
    if (strcmp(result_status, "skipped") == 0 || strcmp(result_status, "not_executable") == 0) {
        return MSCONNECTOR_STATUS_UNSUPPORTED;
    }
    return MSCONNECTOR_STATUS_ERROR;
}
