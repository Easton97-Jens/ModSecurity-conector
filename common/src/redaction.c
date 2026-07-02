#include "msconnector/redaction.h"
#include <string.h>
const char *msconnector_redacted_string(void) { return "[redacted]"; }
size_t msconnector_redact_copy(const char *src, char *dst, size_t n) { const char *r = msconnector_redacted_string(); size_t len = strlen(r); (void)src; if (dst && n) { size_t copy = len < n - 1 ? len : n - 1; memcpy(dst, r, copy); dst[copy] = '\0'; } return len; }
