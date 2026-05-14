#ifndef MSCONNECTOR_REQUEST_H
#define MSCONNECTOR_REQUEST_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct msconnector_bytes {
    const uint8_t *data;
    size_t size;
} msconnector_bytes;

typedef struct msconnector_header {
    const char *name;
    size_t name_size;
    const char *value;
    size_t value_size;
} msconnector_header;

typedef struct msconnector_endpoint {
    const char *address;
    int port;
} msconnector_endpoint;

typedef struct msconnector_request {
    const char *method;
    const char *uri;
    const char *http_version;
    const char *hostname;
    msconnector_endpoint client;
    msconnector_endpoint server;
    const msconnector_header *headers;
    size_t header_count;
    msconnector_bytes body;
} msconnector_request;

#ifdef __cplusplus
}
#endif

#endif
