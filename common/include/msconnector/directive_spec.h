#ifndef MSCONNECTOR_DIRECTIVE_SPEC_H
#define MSCONNECTOR_DIRECTIVE_SPEC_H
#include <stddef.h>
#ifdef __cplusplus
extern "C" {
#endif
/* Global semantic directive catalog. Host connectors still register directives through their own server APIs. */
typedef enum msconnector_directive_value_type { MSCONNECTOR_DIRECTIVE_VALUE_BOOL = 0, MSCONNECTOR_DIRECTIVE_VALUE_STRING = 1, MSCONNECTOR_DIRECTIVE_VALUE_PATH = 2, MSCONNECTOR_DIRECTIVE_VALUE_ENUM = 3, MSCONNECTOR_DIRECTIVE_VALUE_SIZE = 4 } msconnector_directive_value_type;
typedef struct msconnector_directive_spec { const char *name; msconnector_directive_value_type value_type; const char *default_value; const char *allowed_values; const char *description; } msconnector_directive_spec;
const msconnector_directive_spec *msconnector_directive_specs(void);
size_t msconnector_directive_spec_count(void);
const msconnector_directive_spec *msconnector_directive_spec_find(const char *name);
#ifdef __cplusplus
}
#endif
#endif
