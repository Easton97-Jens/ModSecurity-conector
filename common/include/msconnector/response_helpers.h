#ifndef MSCONNECTOR_RESPONSE_HELPERS_H
#define MSCONNECTOR_RESPONSE_HELPERS_H
#include "msconnector/response.h"
#ifdef __cplusplus
extern "C" {
#endif
void msconnector_response_init(msconnector_response *response);
int msconnector_response_validate(const msconnector_response *response);
int msconnector_response_has_header(const msconnector_response *response, const char *name);
const char *msconnector_response_header_value(const msconnector_response *response, const char *name);
const char *msconnector_response_content_type(const msconnector_response *response);
size_t msconnector_response_content_length(const msconnector_response *response, int *status);
#ifdef __cplusplus
}
#endif
#endif
