#ifndef MSCONNECTOR_RULE_ID_H
#define MSCONNECTOR_RULE_ID_H
#include <stddef.h>
#ifdef __cplusplus
extern "C" {
#endif
int msconnector_rule_id_copy(const char *value, char *out, size_t out_len);
/* Parse the complete native libModSecurity RuleMessage metadata record.
 * Returns 1 for an unambiguous ID, 0 when no record is present, and -1 for
 * malformed/ambiguous records or insufficient output capacity. Output is
 * cleared on every non-success; free-text and bare ID snippets are unknown. */
int msconnector_rule_id_extract_from_message(const char *message, char *out, size_t out_len);
int msconnector_rule_id_validate(const char *value);
#ifdef __cplusplus
}
#endif
#endif
