#include "msconnector/headers.h"
#include <ctype.h>
#include <string.h>

static int ci_equal_n(const char *a, size_t an, const char *b) {
    size_t i;
    if (a == 0 || b == 0 || strlen(b) != an) return 0;
    for (i = 0; i < an; ++i) if (tolower((unsigned char)a[i]) != tolower((unsigned char)b[i])) return 0;
    return 1;
}

int msconnector_header_name_equals(const msconnector_header *header, const char *name) {
    return header != 0 && ci_equal_n(header->name, header->name_size, name);
}
const msconnector_header *msconnector_headers_find(const msconnector_header *headers, size_t header_count, const char *name) {
    size_t i;
    if (headers == 0 || name == 0) return 0;
    for (i = 0; i < header_count; ++i) if (msconnector_header_name_equals(&headers[i], name)) return &headers[i];
    return 0;
}
const char *msconnector_headers_find_value(const msconnector_header *headers, size_t header_count, const char *name) {
    const msconnector_header *h = msconnector_headers_find(headers, header_count, name);
    return h == 0 ? 0 : h->value;
}
int msconnector_headers_content_type_matches(const msconnector_header *headers, size_t header_count, const char *content_type) {
    const msconnector_header *h = msconnector_headers_find(headers, header_count, "content-type");
    size_t n, i;
    if (h == 0 || h->value == 0 || content_type == 0) return 0;
    n = strlen(content_type);
    if (h->value_size < n) return 0;
    for (i = 0; i < n; ++i) if (tolower((unsigned char)h->value[i]) != tolower((unsigned char)content_type[i])) return 0;
    return h->value_size == n || h->value[n] == ';' || isspace((unsigned char)h->value[n]);
}
