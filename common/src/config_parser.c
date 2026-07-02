#include "msconnector/config_parser.h"
#include "msconnector/http_status.h"
#include <ctype.h>
#include <limits.h>
#include <stdint.h>
#include <string.h>

static int token_equals(const char *value, const char *expected) {
    size_t index = 0;
    if (value == 0 || expected == 0 || value[0] == '\0') { return 0; }
    for (; value[index] != '\0' && expected[index] != '\0'; ++index) {
        if (tolower((unsigned char)value[index]) != tolower((unsigned char)expected[index])) { return 0; }
    }
    return value[index] == '\0' && expected[index] == '\0';
}

int msconnector_parse_bool(const char *value, enum msconnector_bool_option *out) {
    enum msconnector_bool_option parsed;
    if (token_equals(value, "on") || token_equals(value, "true") || token_equals(value, "1") || token_equals(value, "yes")) { parsed = MSCONNECTOR_BOOL_ON; }
    else if (token_equals(value, "off") || token_equals(value, "false") || token_equals(value, "0") || token_equals(value, "no")) { parsed = MSCONNECTOR_BOOL_OFF; }
    else { return 0; }
    if (out != 0) { *out = parsed; }
    return 1;
}

int msconnector_parse_phase4_mode(const char *value, enum msconnector_phase4_mode *out) {
    enum msconnector_phase4_mode parsed;
    if (token_equals(value, "minimal")) { parsed = MSCONNECTOR_PHASE4_MODE_MINIMAL; }
    else if (token_equals(value, "safe")) { parsed = MSCONNECTOR_PHASE4_MODE_SAFE; }
    else if (token_equals(value, "strict")) { parsed = MSCONNECTOR_PHASE4_MODE_STRICT; }
    else { return 0; }
    if (out != 0) { *out = parsed; }
    return 1;
}

static int parse_positive_decimal(const char *value, size_t *out) {
    size_t result = 0;
    if (value == 0 || value[0] == '\0' || value[0] == '+' || value[0] == '-') { return 0; }
    for (size_t index = 0; value[index] != '\0'; ++index) {
        size_t digit;
        if (!isdigit((unsigned char)value[index])) { return 0; }
        digit = (size_t)(value[index] - '0');
        if (result > (SIZE_MAX - digit) / 10U) { return 0; }
        result = result * 10U + digit;
    }
    if (result == 0U) { return 0; }
    if (out != 0) { *out = result; }
    return 1;
}

int msconnector_parse_size(const char *value, size_t *out) { return parse_positive_decimal(value, out); }

int msconnector_parse_http_status(const char *value, int *out) {
    size_t parsed = 0;
    if (!parse_positive_decimal(value, &parsed) || parsed > (size_t)INT_MAX || !msconnector_http_status_is_valid((int)parsed)) { return 0; }
    if (out != 0) { *out = (int)parsed; }
    return 1;
}

int msconnector_validate_content_type_token(const char *value) {
    int slash_seen = 0;
    int type_len = 0;
    int subtype_len = 0;
    if (value == 0 || value[0] == '\0') { return 0; }
    for (size_t index = 0; value[index] != '\0'; ++index) {
        unsigned char ch = (unsigned char)value[index];
        if (ch <= 32U || ch == 127U || ch == ';') { return 0; }
        if (ch == '/') { if (slash_seen) { return 0; } slash_seen = 1; continue; }
        if (!slash_seen) { ++type_len; } else { ++subtype_len; }
    }
    return slash_seen && type_len > 0 && subtype_len > 0;
}
