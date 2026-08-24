#include "msconnector/json_escape.h"

#include <stdint.h>
#include <string.h>

static void terminate_at_current(
    char *dst,
    size_t dst_size,
    size_t position) {
    if (dst != 0 && dst_size != 0) {
        dst[position < dst_size ? position : dst_size - 1U] = '\0';
    }
}

static void append_json_char(
    char value,
    char *dst,
    size_t dst_size,
    size_t *position) {
    if (dst != 0 && dst_size != 0 && *position < dst_size - 1U) {
        dst[*position] = value;
    } else {
        terminate_at_current(dst, dst_size, *position);
    }

    if (*position != SIZE_MAX) {
        ++(*position);
    }
}

static void append_json_bytes(
    const char *value,
    size_t value_size,
    char *dst,
    size_t dst_size,
    size_t *position) {
    if (dst != 0 && dst_size != 0 && *position < dst_size &&
        value_size <= dst_size - 1U - *position) {
        memcpy(dst + *position, value, value_size);
    } else {
        terminate_at_current(dst, dst_size, *position);
    }

    if (value_size > SIZE_MAX - *position) {
        *position = SIZE_MAX;
    } else {
        *position += value_size;
    }
}

static void append_json_escape_sequence(
    char escape,
    char *dst,
    size_t dst_size,
    size_t *position) {
    char sequence[2] = {'\\', escape};

    append_json_bytes(sequence, sizeof(sequence), dst, dst_size, position);
}

static void append_json_byte_escape(
    unsigned char value,
    char *dst,
    size_t dst_size,
    size_t *position) {
    static const char hex[] = "0123456789abcdef";
    char sequence[6] = {
        '\\',
        'u',
        '0',
        '0',
        hex[(value >> 4U) & 0x0fU],
        hex[value & 0x0fU],
    };

    append_json_bytes(sequence, sizeof(sequence), dst, dst_size, position);
}

static int utf8_continuation(unsigned char value) {
    return value >= 0x80U && value <= 0xbfU;
}

static size_t valid_utf8_sequence_size(
    const unsigned char *value,
    size_t remaining) {
    if (value == NULL || remaining == 0U) {
        return 0U;
    }

    if (value[0] >= 0xc2U && value[0] <= 0xdfU) {
        return remaining >= 2U && utf8_continuation(value[1]) ? 2U : 0U;
    }

    if (value[0] == 0xe0U) {
        return remaining >= 3U && value[1] >= 0xa0U && value[1] <= 0xbfU &&
                       utf8_continuation(value[2])
                   ? 3U
                   : 0U;
    }

    if ((value[0] >= 0xe1U && value[0] <= 0xecU) ||
        (value[0] >= 0xeeU && value[0] <= 0xefU)) {
        return remaining >= 3U && utf8_continuation(value[1]) &&
                       utf8_continuation(value[2])
                   ? 3U
                   : 0U;
    }

    if (value[0] == 0xedU) {
        return remaining >= 3U && value[1] >= 0x80U && value[1] <= 0x9fU &&
                       utf8_continuation(value[2])
                   ? 3U
                   : 0U;
    }

    if (value[0] == 0xf0U) {
        return remaining >= 4U && value[1] >= 0x90U && value[1] <= 0xbfU &&
                       utf8_continuation(value[2]) && utf8_continuation(value[3])
                   ? 4U
                   : 0U;
    }

    if (value[0] >= 0xf1U && value[0] <= 0xf3U) {
        return remaining >= 4U && utf8_continuation(value[1]) &&
                       utf8_continuation(value[2]) && utf8_continuation(value[3])
                   ? 4U
                   : 0U;
    }

    if (value[0] == 0xf4U) {
        return remaining >= 4U && value[1] >= 0x80U && value[1] <= 0x8fU &&
                       utf8_continuation(value[2]) && utf8_continuation(value[3])
                   ? 4U
                   : 0U;
    }

    return 0U;
}

size_t msconnector_json_escape_n(
    const char *src,
    size_t src_size,
    char *dst,
    size_t dst_size) {
    size_t position = 0U;
    size_t index = 0U;
    const unsigned char *bytes;

    if (src == 0) {
        src_size = 0U;
    }

    bytes = (const unsigned char *)(src == NULL ? "" : src);

    while (index < src_size) {
        const unsigned char value = bytes[index];
        size_t sequence_size;

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
                append_json_byte_escape(value, dst, dst_size, &position);
            } else if (value < 0x80U) {
                append_json_char((char)value, dst, dst_size, &position);
            } else {
                sequence_size = valid_utf8_sequence_size(
                    bytes + index,
                    src_size - index);
                if (sequence_size == 0U) {
                    append_json_byte_escape(value, dst, dst_size, &position);
                } else {
                    append_json_bytes(
                        (const char *)(bytes + index),
                        sequence_size,
                        dst,
                        dst_size,
                        &position);
                    index += sequence_size - 1U;
                }
            }
            break;
        }

        ++index;
    }

    if (dst != 0 && dst_size != 0) {
        dst[position < dst_size ? position : dst_size - 1U] = '\0';
    }

    return position;
}

size_t msconnector_json_escape(
    const char *src,
    char *dst,
    size_t dst_size) {
    return msconnector_json_escape_n(
        src,
        src == NULL ? 0U : strlen(src),
        dst,
        dst_size);
}
