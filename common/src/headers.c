#include "msconnector/headers.h"
#include <ctype.h>
#include <string.h>

static int header_name_equal_n(const char *left, size_t left_size, const char *right) {
    if (left == 0 || right == 0 || strlen(right) != left_size) {
        return 0;
    }

    for (size_t index = 0; index < left_size; ++index) {
        if (tolower((unsigned char)left[index]) !=
            tolower((unsigned char)right[index])) {
            return 0;
        }
    }

    return 1;
}

int msconnector_header_name_equals(const msconnector_header *header, const char *name) {
    return header != 0 && header_name_equal_n(header->name, header->name_size, name);
}

const msconnector_header *msconnector_headers_find(
    const msconnector_header *headers,
    size_t header_count,
    const char *name) {
    if (headers == 0 || name == 0) {
        return 0;
    }

    for (size_t index = 0; index < header_count; ++index) {
        if (msconnector_header_name_equals(&headers[index], name)) {
            return &headers[index];
        }
    }

    return 0;
}

const char *msconnector_headers_find_value(
    const msconnector_header *headers,
    size_t header_count,
    const char *name) {
    const msconnector_header *header = msconnector_headers_find(headers, header_count, name);

    if (header == 0) {
        return 0;
    }

    return header->value;
}

int msconnector_headers_content_type_matches(
    const msconnector_header *headers,
    size_t header_count,
    const char *content_type) {
    const msconnector_header *header = msconnector_headers_find(
        headers,
        header_count,
        "content-type");

    if (header == 0 || header->value == 0 || content_type == 0) {
        return 0;
    }

    const size_t content_type_size = strlen(content_type);
    if (header->value_size < content_type_size) {
        return 0;
    }

    for (size_t index = 0; index < content_type_size; ++index) {
        if (tolower((unsigned char)header->value[index]) !=
            tolower((unsigned char)content_type[index])) {
            return 0;
        }
    }

    size_t suffix_index = content_type_size;
    while (suffix_index < header->value_size &&
        isspace((unsigned char)header->value[suffix_index])) {
        ++suffix_index;
    }

    return suffix_index == header->value_size || header->value[suffix_index] == ';';
}
