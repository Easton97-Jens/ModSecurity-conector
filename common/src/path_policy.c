#include "msconnector/path_policy.h"
#include <string.h>
int msconnector_path_is_empty(const char *p) { return p == 0 || p[0] == '\0'; }
int msconnector_path_is_absolute(const char *p) { return p && (p[0] == '/' || (p[0] && p[1] == ':')); }
int msconnector_path_has_parent_reference(const char *p) { const char *q; if (!p) return 0; if (strcmp(p, "..") == 0) return 1; if (strncmp(p, "../", 3) == 0) return 1; q = strstr(p, "/../"); if (q) return 1; q = p + strlen(p); return q >= p + 3 && strcmp(q - 3, "/..") == 0; }
