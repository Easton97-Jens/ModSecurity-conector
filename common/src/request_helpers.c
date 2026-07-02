#include "msconnector/request_helpers.h"
#include "msconnector/headers.h"
#include <string.h>

static int nonempty(const char *value) { return value != 0 && value[0] != '\0'; }
static int valid_header_name(const msconnector_header *header) {
    if (header == 0 || header->name == 0 || header->name_size == 0U) { return 0; }
    for (size_t index = 0; index < header->name_size; ++index) { unsigned char ch = (unsigned char)header->name[index]; if (ch <= 32U || ch == 127U || ch == ':') { return 0; } }
    return header->value != 0 || header->value_size == 0U;
}
void msconnector_request_init(msconnector_request *request) { if (request != 0) { memset(request, 0, sizeof(*request)); } }
int msconnector_request_validate(const msconnector_request *request) {
    if (request == 0 || !nonempty(request->method) || !nonempty(request->uri)) { return 0; }
    if (request->header_count > 0U && request->headers == 0) { return 0; }
    for (size_t i = 0; i < request->header_count; ++i) { if (!valid_header_name(&request->headers[i])) { return 0; } }
    if (request->body.size > 0U && request->body.data == 0) { return 0; }
    return 1;
}
int msconnector_request_has_header(const msconnector_request *request, const char *name) { return request != 0 && msconnector_headers_find_first(request->headers, request->header_count, name) != 0; }
const char *msconnector_request_header_value(const msconnector_request *request, const char *name) {
    (void)request;
    (void)name;
    return 0;
}
const char *msconnector_request_content_type(const msconnector_request *request) {
    (void)request;
    return 0;
}
int msconnector_request_content_type_slice(const msconnector_request *request, const char **value, size_t *value_size) {
    if (value != 0) { *value = 0; }
    if (value_size != 0) { *value_size = 0; }
    return request != 0 && msconnector_headers_find_value_slice(request->headers, request->header_count, "content-type", value, value_size);
}
size_t msconnector_request_content_length(const msconnector_request *request, int *status) {
    size_t out = 0; int parsed = request == 0 ? -1 : msconnector_headers_parse_content_length(request->headers, request->header_count, &out);
    if (status != 0) { *status = parsed; }
    return parsed == 1 ? out : 0U;
}
