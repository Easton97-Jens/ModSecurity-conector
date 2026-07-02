#include "msconnector/rule_id.h"
#include <ctype.h>
#include <string.h>
static int allowed(char ch) { return isalnum((unsigned char)ch) || ch == '_' || ch == '-' || ch == '.' || ch == ':'; }
int msconnector_rule_id_validate(const char *value) { if (value == 0 || value[0] == '\0') { return 0; } for (size_t i = 0; value[i] != '\0'; ++i) { unsigned char ch = (unsigned char)value[i]; if (ch < 33U || ch > 126U || !allowed((char)ch)) { return 0; } } return 1; }
int msconnector_rule_id_copy(const char *value, char *out, size_t out_len) { size_t len; if (out != 0 && out_len > 0U) { out[0] = '\0'; } if (!msconnector_rule_id_validate(value) || out == 0 || out_len == 0U) { return 0; } len = strlen(value); if (len >= out_len) { return 0; } memcpy(out, value, len + 1U); return 1; }
static int copy_until(const char *start, char terminator, char *out, size_t out_len) { char tmp[128]; size_t i = 0; while (start[i] != '\0' && start[i] != terminator && i + 1U < sizeof(tmp)) { tmp[i] = start[i]; ++i; } if (start[i] != terminator) { return -1; } tmp[i] = '\0'; return msconnector_rule_id_copy(tmp, out, out_len) ? 1 : -1; }
int msconnector_rule_id_extract_from_message(const char *message, char *out, size_t out_len) {
    const char *p; if (message == 0) { return 0; }
    p = strstr(message, "[id \""); if (p != 0) { return copy_until(p + 5, '"', out, out_len); }
    p = strstr(message, "[id '"); if (p != 0) { return copy_until(p + 5, '\'', out, out_len); }
    p = strstr(message, "id \""); if (p != 0) { return copy_until(p + 4, '"', out, out_len); }
    p = strstr(message, "id '"); if (p != 0) { return copy_until(p + 4, '\'', out, out_len); }
    p = strstr(message, "id:"); if (p != 0) { char tmp[128]; size_t i = 0; p += 3; while (*p == ' ') { ++p; } while (p[i] != '\0' && !isspace((unsigned char)p[i]) && i + 1U < sizeof(tmp)) { tmp[i] = p[i]; ++i; } tmp[i] = '\0'; return tmp[0] == '\0' ? 0 : (msconnector_rule_id_copy(tmp, out, out_len) ? 1 : -1); }
    return 0;
}
