#ifndef MSCONNECTOR_REDACTION_H
#define MSCONNECTOR_REDACTION_H
#include <stddef.h>
#ifdef __cplusplus
extern "C" {
#endif
/* Simple redaction helpers. Connectors remain responsible for not passing sensitive payloads. */
const char *msconnector_redacted_string(void);
size_t msconnector_redact_copy(const char *src, char *dst, size_t dst_size);
#ifdef __cplusplus
}
#endif
#endif
