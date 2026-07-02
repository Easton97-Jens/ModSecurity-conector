#include "msconnector/log_sanitize.h"
#include <stdio.h>

static char sanitized_char(char value)
{
    const unsigned char ch = (unsigned char)value;

    if (ch < 32U || ch == 127U) {
        return ' ';
    }
    return value;
}

size_t msconnector_sanitize_log_message(
    const char *src,
    size_t src_size,
    char *dst,
    size_t dst_size,
    int *truncated)
{
    size_t written = 0;

    if (truncated != 0) {
        *truncated = 0;
    }
    if (dst != 0 && dst_size > 0U) {
        dst[0] = '\0';
    }
    if (src == 0) {
        return 0;
    }

    for (size_t index = 0; index < src_size; ++index) {
        const char out = sanitized_char(src[index]);

        if (dst != 0 && dst_size > 0U && written + 1U < dst_size) {
            dst[written] = out;
        } else if (truncated != 0) {
            *truncated = 1;
        }
        ++written;
    }
    if (dst != 0 && dst_size > 0U) {
        const size_t nul_index = written < dst_size ? written : dst_size - 1U;
        dst[nul_index] = '\0';
    }
    return written;
}

size_t msconnector_redact_body_snippet(
    const unsigned char *src,
    size_t src_size,
    char *dst,
    size_t dst_size,
    int *truncated)
{
    char marker[64];
    int written;

    (void)src;
    if (truncated != 0) {
        *truncated = 0;
    }
    if (dst != 0 && dst_size > 0U) {
        dst[0] = '\0';
    }

    written = snprintf(marker, sizeof(marker), "[redacted body: %zu bytes]", src_size);
    if (written < 0) {
        return 0;
    }
    if (dst != 0 && dst_size > 0U) {
        (void)snprintf(dst, dst_size, "%s", marker);
    }
    if (truncated != 0 && (dst_size == 0U || (size_t)written >= dst_size)) {
        *truncated = 1;
    }
    return (size_t)written;
}
