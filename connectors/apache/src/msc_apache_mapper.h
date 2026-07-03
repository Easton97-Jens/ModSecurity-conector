#ifndef MSC_APACHE_MAPPER_H
#define MSC_APACHE_MAPPER_H

#include <stddef.h>
#include "httpd.h"
#include "msconnector/request.h"
#include "msconnector/request_mapper_contract.h"
#include "msconnector/response.h"
#include "msconnector/response_mapper_contract.h"

int msc_apache_map_request(
    request_rec *r,
    const msconnector_request_mapper_contract *contract,
    msconnector_request *out,
    char *error,
    size_t error_len);

int msc_apache_map_response(
    request_rec *r,
    const msconnector_response_mapper_contract *contract,
    msconnector_response *out,
    char *error,
    size_t error_len);

#endif
