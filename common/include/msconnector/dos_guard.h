#ifndef MSCONNECTOR_DOS_GUARD_H
#define MSCONNECTOR_DOS_GUARD_H

#include "msconnector/error.h"
#include "msconnector/request.h"
#include "msconnector/resource_limits.h"
#include "msconnector/response.h"

#ifdef __cplusplus
extern "C" {
#endif

int msconnector_dos_guard_check_request(const msconnector_request *request, const msconnector_resource_limits *limits, msconnector_error *error);
int msconnector_dos_guard_check_response(const msconnector_response *response, const msconnector_resource_limits *limits, msconnector_error *error);
int msconnector_dos_guard_check_event_json_size(size_t size, const msconnector_resource_limits *limits, msconnector_error *error);

#ifdef __cplusplus
}
#endif

#endif
