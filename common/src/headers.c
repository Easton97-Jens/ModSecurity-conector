#include "msconnector/headers.h"
#include <ctype.h>
#include <stddef.h>
#include <stdint.h>
#include <string.h>

static int is_ows(char value) { return value == ' ' || value == '\t'; }

static int header_name_equal_n(const char *left, size_t left_size, const char *right) {
    if (left == 0 || right == 0 || strlen(right) != left_size) { return 0; }
    for (size_t index = 0; index < left_size; ++index) {
        if (tolower((unsigned char)left[index]) != tolower((unsigned char)right[index])) { return 0; }
    }
    return 1;
}
int msconnector_header_name_is(const char *name, size_t name_size, const char *expected) { return header_name_equal_n(name, name_size, expected); }
int msconnector_header_name_equals(const msconnector_header *header, const char *name) { return header != 0 && header_name_equal_n(header->name, header->name_size, name); }
const msconnector_header *msconnector_headers_find_first(const msconnector_header *headers, size_t header_count, const char *name) { return msconnector_headers_find(headers, header_count, name); }
const msconnector_header *msconnector_headers_find(const msconnector_header *headers, size_t header_count, const char *name) {
    if (headers == 0 || name == 0) { return 0; }
    for (size_t index = 0; index < header_count; ++index) { if (msconnector_header_name_equals(&headers[index], name)) { return &headers[index]; } }
    return 0;
}
const msconnector_header *msconnector_headers_find_last(const msconnector_header *headers, size_t header_count, const char *name) {
    const msconnector_header *found = 0;
    if (headers == 0 || name == 0) { return 0; }
    for (size_t index = 0; index < header_count; ++index) { if (msconnector_header_name_equals(&headers[index], name)) { found = &headers[index]; } }
    return found;
}
size_t msconnector_headers_count_name(const msconnector_header *headers, size_t header_count, const char *name) {
    size_t count = 0;
    if (headers == 0 || name == 0) { return 0; }
    for (size_t index = 0; index < header_count; ++index) { if (msconnector_header_name_equals(&headers[index], name)) { ++count; } }
    return count;
}
const char *msconnector_headers_find_value(const msconnector_header *headers, size_t header_count, const char *name) {
    (void)headers;
    (void)header_count;
    (void)name;
    return 0;
}
int msconnector_headers_find_value_slice(const msconnector_header *headers, size_t header_count, const char *name, const char **value, size_t *value_size) {
    const msconnector_header *header = msconnector_headers_find(headers, header_count, name);
    if (value != 0) { *value = 0; }
    if (value_size != 0) { *value_size = 0; }
    if (header == 0 || header->value == 0) { return 0; }
    if (value != 0) { *value = header->value; }
    if (value_size != 0) { *value_size = header->value_size; }
    return 1;
}
int msconnector_headers_copy_value(const msconnector_header *headers, size_t header_count, const char *name, char *dst, size_t dst_size, int *truncated) {
    const char *value = 0;
    size_t value_size = 0;
    if (truncated != 0) { *truncated = 0; }
    if (dst != 0 && dst_size > 0U) { dst[0] = '\0'; }
    if (!msconnector_headers_find_value_slice(headers, header_count, name, &value, &value_size)) { return 0; }
    if (dst == 0 || dst_size == 0U) { if (truncated != 0) { *truncated = 1; } return 0; }
    if (value_size >= dst_size) {
        memcpy(dst, value, dst_size - 1U);
        dst[dst_size - 1U] = '\0';
        if (truncated != 0) { *truncated = 1; }
        return 0;
    }
    memcpy(dst, value, value_size);
    dst[value_size] = '\0';
    return 1;
}
int msconnector_header_is_set_cookie_name(const char *name, size_t name_size) { return msconnector_header_name_is(name, name_size, "set-cookie"); }
int msconnector_header_is_cookie_name(const char *name, size_t name_size) { return msconnector_header_name_is(name, name_size, "cookie"); }
int msconnector_header_is_content_length_name(const char *name, size_t name_size) { return msconnector_header_name_is(name, name_size, "content-length"); }
int msconnector_header_value_can_be_combined(const char *name, size_t name_size) {
    if (msconnector_header_is_set_cookie_name(name, name_size) || msconnector_header_is_cookie_name(name, name_size) || msconnector_header_is_content_length_name(name, name_size) || msconnector_header_name_is(name, name_size, "host")) { return 0; }
    return name != 0 && name_size != 0;
}
int msconnector_headers_content_type_matches(const msconnector_header *headers, size_t header_count, const char *content_type) {
    const msconnector_header *header = msconnector_headers_find(headers, header_count, "content-type");
    size_t value_index = 0;
    const size_t content_type_size = content_type == 0 ? 0U : strlen(content_type);
    size_t index;
    size_t suffix_index;
    if (header == 0 || header->value == 0 || content_type == 0) { return 0; }
    while (value_index < header->value_size && is_ows(header->value[value_index])) { ++value_index; }
    if (header->value_size - value_index < content_type_size) { return 0; }
    for (index = 0; index < content_type_size; ++index) {
        if (tolower((unsigned char)header->value[value_index + index]) != tolower((unsigned char)content_type[index])) { return 0; }
    }
    suffix_index = value_index + content_type_size;
    while (suffix_index < header->value_size && is_ows(header->value[suffix_index])) { ++suffix_index; }
    return suffix_index == header->value_size || header->value[suffix_index] == ';';
}
static int parse_decimal(const char *value, size_t size, size_t *out) {
    size_t index = 0;
    size_t result = 0;
    while (index < size && isspace((unsigned char)value[index])) { ++index; }
    if (index == size || value[index] == '+' || value[index] == '-') { return 0; }
    for (; index < size && isdigit((unsigned char)value[index]); ++index) {
        const size_t digit = (size_t)(value[index] - '0');
        if (result > (SIZE_MAX - digit) / 10U) { return 0; }
        result = result * 10U + digit;
    }
    while (index < size && isspace((unsigned char)value[index])) { ++index; }
    if (index != size) { return 0; }
    *out = result; return 1;
}
int msconnector_headers_parse_content_length(const msconnector_header *headers, size_t header_count, size_t *out) {
    int seen = 0;
    size_t parsed = 0;
    if (headers == 0) { return 0; }
    for (size_t index = 0; index < header_count; ++index) {
        size_t current = 0;
        if (!msconnector_header_is_content_length_name(headers[index].name, headers[index].name_size)) { continue; }
        if (headers[index].value == 0 || !parse_decimal(headers[index].value, headers[index].value_size, &current)) { return -1; }
        if (seen && current != parsed) { return -1; }
        parsed = current; seen = 1;
    }
    if (!seen) { return 0; }
    if (out != 0) { *out = parsed; }
    return 1;
}
const char *msconnector_headers_host(const msconnector_header *headers, size_t header_count) {
    (void)headers;
    (void)header_count;
    return 0;
}
size_t msconnector_header_sanitize_value_for_log(const char *src, size_t src_size, char *dst, size_t dst_size, int *truncated) {
    size_t written = 0;
    if (truncated != 0) { *truncated = 0; }
    if (dst != 0 && dst_size > 0) { dst[0] = '\0'; }
    if (src == 0) { return 0; }
    for (size_t index = 0; index < src_size; ++index) {
        char out = (unsigned char)src[index] < 32U || src[index] == 127 ? ' ' : src[index];
        if (dst != 0 && dst_size > 0 && written + 1U < dst_size) { dst[written] = out; }
        else if (truncated != 0) { *truncated = 1; }
        ++written;
    }
    if (dst != 0 && dst_size > 0) { dst[written < dst_size ? written : dst_size - 1U] = '\0'; }
    return written;
}
