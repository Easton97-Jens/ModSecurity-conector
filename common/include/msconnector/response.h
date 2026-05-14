#ifndef MSCONNECTOR_RESPONSE_H
#define MSCONNECTOR_RESPONSE_H

#include <stddef.h>
#include <stdint.h>

#include "msconnector/request.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct msconnector_response {
    int status;
    const char *http_version;
    const msconnector_header *headers;
    size_t header_count;
    msconnector_bytes body;
} msconnector_response;

#ifdef __cplusplus
}
#endif

#endif
