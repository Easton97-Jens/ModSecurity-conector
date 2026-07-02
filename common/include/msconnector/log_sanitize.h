#ifndef MSCONNECTOR_LOG_SANITIZE_H
#define MSCONNECTOR_LOG_SANITIZE_H
#include <stddef.h>
#ifdef __cplusplus
extern "C" {
#endif
size_t msconnector_sanitize_log_message(const char *src, size_t src_size, char *dst, size_t dst_size, int *truncated);
size_t msconnector_redact_body_snippet(const unsigned char *src, size_t src_size, char *dst, size_t dst_size, int *truncated);
#ifdef __cplusplus
}
#endif
#endif
