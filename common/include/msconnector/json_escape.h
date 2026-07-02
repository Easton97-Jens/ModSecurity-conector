#ifndef MSCONNECTOR_JSON_ESCAPE_H
#define MSCONNECTOR_JSON_ESCAPE_H
#include <stddef.h>
#ifdef __cplusplus
extern "C" {
#endif
/* Deterministic JSON string escaping helper. NULL input is treated as an empty string. */
size_t msconnector_json_escape(const char *src, char *dst, size_t dst_size);
#ifdef __cplusplus
}
#endif
#endif
