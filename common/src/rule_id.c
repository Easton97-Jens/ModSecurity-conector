#include "msconnector/rule_id.h"
#include <ctype.h>
#include <string.h>

static int allowed_rule_id_char(char ch)
{
    return isalnum((unsigned char)ch) || ch == '_' || ch == '-' || ch == '.' || ch == ':';
}

int msconnector_rule_id_validate(const char *value)
{
    if (value == 0 || value[0] == '\0') {
        return 0;
    }
    for (size_t index = 0; value[index] != '\0'; ++index) {
        const unsigned char ch = (unsigned char)value[index];

        if (ch < 33U || ch > 126U || !allowed_rule_id_char((char)ch)) {
            return 0;
        }
    }
    return 1;
}

int msconnector_rule_id_copy(const char *value, char *out, size_t out_len)
{
    size_t len;

    if (out != 0 && out_len > 0U) {
        out[0] = '\0';
    }
    if (!msconnector_rule_id_validate(value) || out == 0 || out_len == 0U) {
        return 0;
    }

    len = strlen(value);
    if (len >= out_len) {
        return 0;
    }
    memcpy(out, value, len + 1U);
    return 1;
}

static int copy_until(const char *start, char terminator, char *out, size_t out_len)
{
    char tmp[128];
    size_t index = 0;

    while (start[index] != '\0' && start[index] != terminator && index + 1U < sizeof(tmp)) {
        tmp[index] = start[index];
        ++index;
    }
    if (start[index] != terminator) {
        return -1;
    }
    tmp[index] = '\0';
    return msconnector_rule_id_copy(tmp, out, out_len) ? 1 : -1;
}

static int copy_colon_id(const char *start, char *out, size_t out_len)
{
    char tmp[128];
    size_t index = 0;

    while (*start == ' ') {
        ++start;
    }
    while (start[index] != '\0' && !isspace((unsigned char)start[index]) && index + 1U < sizeof(tmp)) {
        tmp[index] = start[index];
        ++index;
    }
    tmp[index] = '\0';
    if (tmp[0] == '\0') {
        return 0;
    }
    return msconnector_rule_id_copy(tmp, out, out_len) ? 1 : -1;
}

int msconnector_rule_id_extract_from_message(const char *message, char *out, size_t out_len)
{
    const char *match;

    if (message == 0) {
        return 0;
    }
    match = strstr(message, "[id \"");
    if (match != 0) {
        return copy_until(match + 5, '"', out, out_len);
    }
    match = strstr(message, "[id '");
    if (match != 0) {
        return copy_until(match + 5, '\'', out, out_len);
    }
    match = strstr(message, "id \"");
    if (match != 0) {
        return copy_until(match + 4, '"', out, out_len);
    }
    match = strstr(message, "id '");
    if (match != 0) {
        return copy_until(match + 4, '\'', out, out_len);
    }
    match = strstr(message, "id:");
    if (match != 0) {
        return copy_colon_id(match + 3, out, out_len);
    }
    return 0;
}
