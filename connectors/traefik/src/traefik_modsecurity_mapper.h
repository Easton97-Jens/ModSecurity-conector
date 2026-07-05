#ifndef TRAEFIK_MODSECURITY_MAPPER_H
#define TRAEFIK_MODSECURITY_MAPPER_H

#include <stddef.h>
#include <stdint.h>

#include "msconnector/config.h"
#include "msconnector/request.h"
#include "msconnector/request_mapper_contract.h"
#include "msconnector/response.h"
#include "msconnector/response_mapper_contract.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct traefik_modsecurity_header {
    const char *name;
    const char *value;
} traefik_modsecurity_header;

typedef struct traefik_modsecurity_request {
    const char *method;
    const char *uri;
    const char *http_version;
    const char *client_address;
    int client_port;
    const char *server_address;
    int server_port;
    const traefik_modsecurity_header *headers;
    size_t header_count;
    const uint8_t *body;
    size_t body_size;
} traefik_modsecurity_request;

typedef struct traefik_modsecurity_response {
    int status;
    const char *http_version;
    const char *content_type;
    size_t content_length;
    const traefik_modsecurity_header *headers;
    size_t header_count;
    const uint8_t *body;
    size_t body_size;
} traefik_modsecurity_response;

typedef struct traefik_modsecurity_mapped_request {
    msconnector_request request;
    msconnector_header *owned_headers;
} traefik_modsecurity_mapped_request;

typedef struct traefik_modsecurity_mapped_response {
    msconnector_response response;
    msconnector_header *owned_headers;
} traefik_modsecurity_mapped_response;

void traefik_modsecurity_config_init(msconnector_config *config);
void traefik_modsecurity_mapped_request_cleanup(traefik_modsecurity_mapped_request *mapped);
void traefik_modsecurity_mapped_response_cleanup(traefik_modsecurity_mapped_response *mapped);
int traefik_modsecurity_map_request(const traefik_modsecurity_request *src, const msconnector_request_mapper_contract *contract, msconnector_request *out, char *error, size_t error_len);
int traefik_modsecurity_map_response(const traefik_modsecurity_response *src, const msconnector_response_mapper_contract *contract, msconnector_response *out, char *error, size_t error_len);
int traefik_modsecurity_map_owned_request(const traefik_modsecurity_request *src, const msconnector_request_mapper_contract *contract, traefik_modsecurity_mapped_request *out, char *error, size_t error_len);
int traefik_modsecurity_map_owned_response(const traefik_modsecurity_response *src, const msconnector_response_mapper_contract *contract, traefik_modsecurity_mapped_response *out, char *error, size_t error_len);

#ifdef __cplusplus
}
#endif

#endif
