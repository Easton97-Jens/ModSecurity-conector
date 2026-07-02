#ifndef MSCONNECTOR_REQUEST_HELPERS_H
#define MSCONNECTOR_REQUEST_HELPERS_H
#include "msconnector/request.h"
#ifdef __cplusplus
extern "C" {
#endif
void msconnector_request_init(msconnector_request *request);
int msconnector_request_validate(const msconnector_request *request);
int msconnector_request_has_header(const msconnector_request *request, const char *name);
const char *msconnector_request_header_value(const msconnector_request *request, const char *name);
const char *msconnector_request_content_type(const msconnector_request *request);
size_t msconnector_request_content_length(const msconnector_request *request, int *status);
#ifdef __cplusplus
}
#endif
#endif
