#include "msconnector/json_escape.h"

static void append_json_char(char value, char *dst, size_t dst_size, size_t *position) {
    if (dst != 0 && dst_size != 0 && *position + 1U < dst_size) {
        dst[*position] = value;
    }

    ++(*position);
}

static void append_json_escape_sequence(
    char escape,
    char *dst,
    size_t dst_size,
    size_t *position) {
    append_json_char('\\', dst, dst_size, position);
    append_json_char(escape, dst, dst_size, position);
}

static void append_json_control_escape(
    unsigned char value,
    char *dst,
    size_t dst_size,
    size_t *position) {
    static const char hex[] = "0123456789abcdef";

    append_json_char('\\', dst, dst_size, position);
    append_json_char('u', dst, dst_size, position);
    append_json_char('0', dst, dst_size, position);
    append_json_char('0', dst, dst_size, position);
    append_json_char(hex[(value >> 4U) & 0x0fU], dst, dst_size, position);
    append_json_char(hex[value & 0x0fU], dst, dst_size, position);
}

size_t msconnector_json_escape(const char *src, char *dst, size_t dst_size) {
    size_t position = 0;

    if (src == 0) {
        src = "";
    }

    for (size_t index = 0; src[index] != '\0'; ++index) {
        const unsigned char value = (unsigned char)src[index];

        switch (value) {
        case '"':
            append_json_escape_sequence('"', dst, dst_size, &position);
            break;
        case '\\':
            append_json_escape_sequence('\\', dst, dst_size, &position);
            break;
        case '\n':
            append_json_escape_sequence('n', dst, dst_size, &position);
            break;
        case '\r':
            append_json_escape_sequence('r', dst, dst_size, &position);
            break;
        case '\t':
            append_json_escape_sequence('t', dst, dst_size, &position);
            break;
        default:
            if (value < 0x20U) {
                append_json_control_escape(value, dst, dst_size, &position);
            } else {
                append_json_char((char)value, dst, dst_size, &position);
            }
            break;
        }
    }

    if (dst != 0 && dst_size != 0) {
        dst[position < dst_size ? position : dst_size - 1U] = '\0';
    }

    return position;
}
