#ifndef MSCONNECTOR_STATUS_H
#define MSCONNECTOR_STATUS_H

#ifdef __cplusplus
extern "C" {
#endif

enum msconnector_status {
    MSCONNECTOR_STATUS_OK = 0,
    MSCONNECTOR_STATUS_ERROR = 1,
    MSCONNECTOR_STATUS_BLOCKED = 2,
    MSCONNECTOR_STATUS_UNSUPPORTED = 3
};

const char *msconnector_status_name(enum msconnector_status status);
enum msconnector_status msconnector_status_from_result(const char *result_status);

#ifdef __cplusplus
}
#endif

#endif
