#include "msconnector/response_helpers.h"
#include "msconnector/headers.h"
#include "msconnector/http_status.h"
#include <string.h>

static int valid_header_name(const msconnector_header *header) {
    if (header == 0 || header->name == 0 || header->name_size == 0U) { return 0; }
    for (size_t index = 0; index < header->name_size; ++index) { unsigned char ch = (unsigned char)header->name[index]; if (ch <= 32U || ch == 127U || ch == ':') { return 0; } }
    return header->value != 0 || header->value_size == 0U;
}
void msconnector_response_init(msconnector_response *response) { if (response != 0) { memset(response, 0, sizeof(*response)); } }
int msconnector_response_validate(const msconnector_response *response) {
    if (response == 0) { return 0; }
    if (response->status != 0 && !msconnector_http_status_is_valid(response->status)) { return 0; }
    if (response->header_count > 0U && response->headers == 0) { return 0; }
    for (size_t i = 0; i < response->header_count; ++i) { if (!valid_header_name(&response->headers[i])) { return 0; } }
    if (response->body.size > 0U && response->body.data == 0) { return 0; }
    return 1;
}
int msconnector_response_has_header(const msconnector_response *response, const char *name) { return response != 0 && msconnector_headers_find_first(response->headers, response->header_count, name) != 0; }
const char *msconnector_response_header_value(const msconnector_response *response, const char *name) {
    (void)response;
    (void)name;
    return 0;
}
const char *msconnector_response_content_type(const msconnector_response *response) {
    (void)response;
    return 0;
}
int msconnector_response_content_type_slice(const msconnector_response *response, const char **value, size_t *value_size) {
    if (value != 0) { *value = 0; }
    if (value_size != 0) { *value_size = 0; }
    return response != 0 && msconnector_headers_find_value_slice(response->headers, response->header_count, "content-type", value, value_size);
}
size_t msconnector_response_content_length(const msconnector_response *response, int *status) {
    size_t out = 0; int parsed = response == 0 ? -1 : msconnector_headers_parse_content_length(response->headers, response->header_count, &out);
    if (status != 0) { *status = parsed; }
    return parsed == 1 ? out : 0U;
}
