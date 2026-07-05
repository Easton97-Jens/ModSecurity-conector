#ifndef MSCONNECTOR_GENERIC_MAPPER_H
#define MSCONNECTOR_GENERIC_MAPPER_H

#include <stddef.h>

#include "msconnector/config.h"
#include "msconnector/request.h"
#include "msconnector/request_mapper_contract.h"
#include "msconnector/response.h"
#include "msconnector/response_mapper_contract.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct msconnector_generic_request_source {
    const char *method;
    const char *uri;
    const char *http_version;
    /* hostname must be NUL-terminated when provided; header value slices are not exposed as C strings. */
    const char *hostname;
    msconnector_endpoint client;
    msconnector_endpoint server;
    const msconnector_header *headers;
    size_t header_count;
    msconnector_bytes body;
} msconnector_generic_request_source;

typedef struct msconnector_generic_response_source {
    int status;
    const char *http_version;
    const msconnector_header *headers;
    size_t header_count;
    msconnector_bytes body;
} msconnector_generic_response_source;

void msconnector_generic_config_init(msconnector_config *config);

int msconnector_generic_map_request(
    const msconnector_generic_request_source *src,
    const msconnector_request_mapper_contract *contract,
    msconnector_request *out,
    char *error,
    size_t error_len);

int msconnector_generic_map_response(
    const msconnector_generic_response_source *src,
    const msconnector_response_mapper_contract *contract,
    msconnector_response *out,
    char *error,
    size_t error_len);

#ifdef __cplusplus
}
#endif

#endif
