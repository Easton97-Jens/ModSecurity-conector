#ifndef MSCONNECTOR_HEADERS_H
#define MSCONNECTOR_HEADERS_H

#include "msconnector/request.h"

#ifdef __cplusplus
extern "C" {
#endif

/* Connector-neutral header helpers. They do not allocate and never modify caller-owned headers. */
int msconnector_header_name_equals(const msconnector_header *header, const char *name);
const msconnector_header *msconnector_headers_find(const msconnector_header *headers, size_t header_count, const char *name);
const char *msconnector_headers_find_value(const msconnector_header *headers, size_t header_count, const char *name);
int msconnector_headers_content_type_matches(const msconnector_header *headers, size_t header_count, const char *content_type);

#ifdef __cplusplus
}
#endif

#endif
