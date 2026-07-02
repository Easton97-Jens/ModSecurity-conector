#ifndef MSCONNECTOR_REQUEST_HELPERS_H
#define MSCONNECTOR_REQUEST_HELPERS_H
#include "msconnector/request.h"
#include "msconnector/resource_limits.h"
#ifdef __cplusplus
extern "C" {
#endif
void msconnector_request_init(msconnector_request *request);
int msconnector_request_validate(const msconnector_request *request);
int msconnector_request_validate_with_limits(const msconnector_request *request, const msconnector_resource_limits *limits);
int msconnector_request_has_header(const msconnector_request *request, const char *name);
const char *msconnector_request_header_value(const msconnector_request *request, const char *name);
const char *msconnector_request_content_type(const msconnector_request *request);
int msconnector_request_content_type_slice(const msconnector_request *request, const char **value, size_t *value_size);
size_t msconnector_request_content_length(const msconnector_request *request, int *status);
#ifdef __cplusplus
}
#endif
#endif
