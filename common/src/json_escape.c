#include "msconnector/json_escape.h"
#include <string.h>

static void terminate_at_current(char *dst, size_t dst_size, size_t position) {
    if (dst != 0 && dst_size != 0) {
        dst[position < dst_size ? position : dst_size - 1U] = '\0';
    }
}

static void append_json_char(char value, char *dst, size_t dst_size, size_t *position) {
    if (dst != 0 && dst_size != 0 && *position + 1U < dst_size) {
        dst[*position] = value;
    } else {
        terminate_at_current(dst, dst_size, *position);
    }

    ++(*position);
}

static void append_json_bytes(const char *value, size_t value_size, char *dst, size_t dst_size, size_t *position) {
    if (dst != 0 && dst_size != 0 && *position + value_size < dst_size) {
        memcpy(dst + *position, value, value_size);
    } else {
        terminate_at_current(dst, dst_size, *position);
    }
    *position += value_size;
}

static void append_json_escape_sequence(
    char escape,
    char *dst,
    size_t dst_size,
    size_t *position) {
    char sequence[2];
    sequence[0] = '\\';
    sequence[1] = escape;
    append_json_bytes(sequence, sizeof(sequence), dst, dst_size, position);
}

static void append_json_control_escape(
    unsigned char value,
    char *dst,
    size_t dst_size,
    size_t *position) {
    static const char hex[] = "0123456789abcdef";

    char sequence[6];
    sequence[0] = '\\';
    sequence[1] = 'u';
    sequence[2] = '0';
    sequence[3] = '0';
    sequence[4] = hex[(value >> 4U) & 0x0fU];
    sequence[5] = hex[value & 0x0fU];
    append_json_bytes(sequence, sizeof(sequence), dst, dst_size, position);
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
