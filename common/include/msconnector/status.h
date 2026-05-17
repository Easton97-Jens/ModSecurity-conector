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

#ifdef __cplusplus
}
#endif

#endif
