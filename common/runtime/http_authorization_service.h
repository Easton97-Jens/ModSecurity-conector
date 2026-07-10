#ifndef MSCONNECTOR_HTTP_AUTHORIZATION_SERVICE_H
#define MSCONNECTOR_HTTP_AUTHORIZATION_SERVICE_H

#include <stddef.h>

#include "msconnector/generic_mapper.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef int (*msconnector_runtime_request_mapper)(
    const msconnector_generic_request_source *source,
    const msconnector_request_mapper_contract *contract,
    msconnector_request *request,
    char *error,
    size_t error_len);

typedef int (*msconnector_runtime_response_mapper)(
    const msconnector_generic_response_source *source,
    const msconnector_response_mapper_contract *contract,
    msconnector_response *response,
    char *error,
    size_t error_len);

typedef struct msconnector_http_authorization_profile {
    const char *connector_name;
    const char *integration_mode;
    const char *const *original_uri_headers;
    size_t original_uri_header_count;
    msconnector_runtime_request_mapper map_request;
    msconnector_runtime_response_mapper map_response;
} msconnector_http_authorization_profile;

/*
 * Supported CLI:
 *   --check-config --config PATH
 *   --serve --config PATH --listen HOST:PORT
 *
 * The service is intentionally request-phase only. A profile's response
 * mapper is linked and contract-checked, but upstream response inspection is
 * outside HTTP authorization protocols.
 */
int msconnector_http_authorization_service_main(
    int argc,
    char **argv,
    const msconnector_http_authorization_profile *profile);

#ifdef __cplusplus
}
#endif

#endif
