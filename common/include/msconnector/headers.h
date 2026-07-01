#ifndef MSCONNECTOR_HEADERS_H
#define MSCONNECTOR_HEADERS_H

#include "msconnector/request.h"

#ifdef __cplusplus
extern "C" {
#endif

/* Connector-neutral header helpers. They do not allocate and never modify caller-owned headers. */
int msconnector_header_name_equals(const msconnector_header *header, const char *name);
int msconnector_header_name_is(const char *name, size_t name_size, const char *expected);
const msconnector_header *msconnector_headers_find(const msconnector_header *headers, size_t header_count, const char *name);
const msconnector_header *msconnector_headers_find_first(const msconnector_header *headers, size_t header_count, const char *name);
const msconnector_header *msconnector_headers_find_last(const msconnector_header *headers, size_t header_count, const char *name);
size_t msconnector_headers_count_name(const msconnector_header *headers, size_t header_count, const char *name);
const char *msconnector_headers_find_value(const msconnector_header *headers, size_t header_count, const char *name);
int msconnector_headers_content_type_matches(const msconnector_header *headers, size_t header_count, const char *content_type);
int msconnector_header_is_set_cookie_name(const char *name, size_t name_size);
int msconnector_header_is_cookie_name(const char *name, size_t name_size);
int msconnector_header_is_content_length_name(const char *name, size_t name_size);
int msconnector_header_value_can_be_combined(const char *name, size_t name_size);
int msconnector_headers_parse_content_length(const msconnector_header *headers, size_t header_count, size_t *out);
const char *msconnector_headers_host(const msconnector_header *headers, size_t header_count);
size_t msconnector_header_sanitize_value_for_log(const char *src, size_t src_size, char *dst, size_t dst_size, int *truncated);

#ifdef __cplusplus
}
#endif

#endif
