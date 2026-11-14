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

/* RuleMessage::_details() in the supported libModSecurity C API is a
 * serialized record, not an arbitrary collection of bracketed substrings.
 * The C callback does not expose the C++ RuleMessage metadata selector.
 * Keep the complete field order and optional _errorLogTail() as the framing
 * contract. In particular, matched data before this record is untrusted. */
static int field_starts(const char *cursor, const char *name)
{
    size_t length = strlen(name);

    return cursor[0] == '[' && strncmp(cursor + 1, name, length) == 0 &&
        cursor[length + 1U] == ' ' && cursor[length + 2U] == '"';
}

static int hex_digit(char ch)
{
    return (ch >= '0' && ch <= '9') || (ch >= 'a' && ch <= 'f') ||
        (ch >= 'A' && ch <= 'F');
}

/* toHexIfNeeded() emits literal \xHH escapes. Only selected fields escape
 * quotes/backslashes; file/msg/host/URI/ref are raw printable strings. Never
 * decode escapes while finding delimiters: \x22 cannot close a value.
 * Quotes without a following ']' are literal in the raw Engine fields. */
static int parse_field(const char **cursor, const char *name, int escaped,
    int decimal, const char **value, size_t *value_length)
{
    const char *start;
    const char *next;

    if (!field_starts(*cursor, name)) {
        return 0;
    }
    start = *cursor + strlen(name) + 3U;
    next = start;
    while (*next != '\0' && !(next[0] == '"' && next[1] == ']')) {
        unsigned char ch = (unsigned char)*next;

        if (ch < 32U || ch > 126U || (decimal && (ch < '0' || ch > '9'))) {
            return 0;
        }
        if (escaped && ch == '\\') {
            if (next[1] != 'x' || !hex_digit(next[2]) ||
                next[2] == '\0' || next[3] == '\0' || !hex_digit(next[3])) {
                return 0;
            }
            next += 4;
        } else {
            if (escaped && ch == '"') {
                return 0;
            }
            ++next;
        }
    }
    if (*next == '\0' || (decimal && next == start)) {
        return 0;
    }
    if (value != NULL) {
        *value = start;
        *value_length = (size_t)(next - start);
    }
    *cursor = next + 2;
    return 1;
}

static int next_field(const char **cursor, const char *name, int escaped,
    int decimal)
{
    if (**cursor != ' ') {
        return 0;
    }
    ++*cursor;
    return parse_field(cursor, name, escaped, decimal, NULL, NULL);
}

static int parse_metadata(const char *cursor, const char **rule_id,
    size_t *rule_id_length)
{
    if (!parse_field(&cursor, "file", 0, 0, NULL, NULL) ||
        !next_field(&cursor, "line", 0, 1) || *cursor != ' ') {
        return 0;
    }
    ++cursor;
    if (!parse_field(&cursor, "id", 0, 1, rule_id, rule_id_length) ||
        !next_field(&cursor, "rev", 1, 0) ||
        !next_field(&cursor, "msg", 0, 0) ||
        !next_field(&cursor, "data", 1, 0) ||
        !next_field(&cursor, "severity", 0, 1) ||
        !next_field(&cursor, "ver", 1, 0) ||
        !next_field(&cursor, "maturity", 0, 1) ||
        !next_field(&cursor, "accuracy", 0, 1)) {
        return 0;
    }
    while (*cursor == ' ' && field_starts(cursor + 1, "tag")) {
        if (!next_field(&cursor, "tag", 1, 0)) {
            return 0;
        }
    }
    if (!next_field(&cursor, "hostname", 0, 0) ||
        !next_field(&cursor, "uri", 0, 0) ||
        !next_field(&cursor, "unique_id", 0, 0) ||
        !next_field(&cursor, "ref", 0, 0)) {
        return 0;
    }
    if (*cursor == ' ') {
        if (!next_field(&cursor, "hostname", 0, 0) ||
            !next_field(&cursor, "uri", 0, 0) ||
            !next_field(&cursor, "unique_id", 0, 0)) {
            return 0;
        }
    }
    return *cursor == '\0';
}

int msconnector_rule_id_extract_from_message(const char *message, char *out, size_t out_len)
{
    const char *metadata;
    const char *rule_id;
    size_t length;

    if (out != NULL && out_len > 0U) {
        out[0] = '\0';
    }
    if (message == NULL || out == NULL || out_len == 0U) {
        return 0;
    }
    metadata = strstr(message, "[file \"");
    if (metadata == NULL) {
        return 0;
    }
    /* Raw fields can contain delimiter-looking content. Reject every extra
     * candidate, even an invalid one: choosing the sole successfully parsed
     * suffix could otherwise trust a forged record embedded in a raw URI.
     * The same conservative rule covers a forged prefix before real details. */
    if ((metadata != message && metadata[-1] != ' ') ||
        strstr(metadata + 1, "[file \"") != NULL ||
        !parse_metadata(metadata, &rule_id, &length) || length >= out_len) {
        return -1;
    }
    memcpy(out, rule_id, length);
    out[length] = '\0';
    return 1;
}
