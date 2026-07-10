#ifndef LIGHTTPD_MODSECURITY_MAPPER_H
#define LIGHTTPD_MODSECURITY_MAPPER_H

#include <stddef.h>

#include "msconnector/config.h"
#include "msconnector/generic_mapper.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct request_st request_st;

typedef struct lighttpd_modsecurity_map_storage {
    msconnector_header *headers;
    size_t header_count;
} lighttpd_modsecurity_map_storage;

#define lighttpd_modsecurity_config_init msconnector_generic_config_init

void lighttpd_modsecurity_map_storage_init(
    lighttpd_modsecurity_map_storage *storage);

void lighttpd_modsecurity_map_storage_free(
    lighttpd_modsecurity_map_storage *storage);

int lighttpd_modsecurity_map_request(
    const request_st *request,
    const msconnector_request_mapper_contract *contract,
    size_t total_header_limit,
    lighttpd_modsecurity_map_storage *storage,
    msconnector_request *out,
    char *error,
    size_t error_len);

int lighttpd_modsecurity_map_response(
    const request_st *request,
    const msconnector_response_mapper_contract *contract,
    size_t total_header_limit,
    lighttpd_modsecurity_map_storage *storage,
    msconnector_response *out,
    char *error,
    size_t error_len);

#ifdef __cplusplus
}
#endif

#endif
