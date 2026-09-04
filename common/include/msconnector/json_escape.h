#ifndef MSCONNECTOR_JSON_ESCAPE_H
#define MSCONNECTOR_JSON_ESCAPE_H
#include <stddef.h>
#ifdef __cplusplus
extern "C" {
#endif
/*
 * Deterministic JSON string escaping helpers.  Valid UTF-8 is retained;
 * malformed bytes are emitted as \u00XX escapes so the result remains valid
 * UTF-8 JSON. NULL input is treated as an empty string.
 */
size_t msconnector_json_escape(const char *src, char *dst, size_t dst_size);
size_t msconnector_json_escape_n(
    const char *src,
    size_t src_size,
    char *dst,
    size_t dst_size);
#ifdef __cplusplus
}
#endif
#endif
