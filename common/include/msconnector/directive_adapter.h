#ifndef MSCONNECTOR_DIRECTIVE_ADAPTER_H
#define MSCONNECTOR_DIRECTIVE_ADAPTER_H

#include <stddef.h>

#include "msconnector/directive_spec.h"

#ifdef __cplusplus
extern "C" {
#endif

/* Connector-neutral directive adapter catalog. Host adapters translate these
 * entries into their own server directive registration types; this contract
 * does not represent runtime adoption by any existing connector.
 */
typedef enum msconnector_directive_scope {
    MSCONNECTOR_DIRECTIVE_SCOPE_GLOBAL = 0,
    MSCONNECTOR_DIRECTIVE_SCOPE_SERVER,
    MSCONNECTOR_DIRECTIVE_SCOPE_LOCATION,
    MSCONNECTOR_DIRECTIVE_SCOPE_DIRECTORY
} msconnector_directive_scope;

typedef enum msconnector_directive_argument_policy {
    MSCONNECTOR_DIRECTIVE_ARG_NONE = 0,
    MSCONNECTOR_DIRECTIVE_ARG_ONE,
    MSCONNECTOR_DIRECTIVE_ARG_ONE_OR_MORE,
    MSCONNECTOR_DIRECTIVE_ARG_RAW
} msconnector_directive_argument_policy;

typedef struct msconnector_directive_adapter_entry {
    const msconnector_directive_spec *spec;
    const char *canonical_name;
    const char *host_name;
    msconnector_directive_scope scope;
    msconnector_directive_argument_policy argument_policy;
    unsigned flags;
} msconnector_directive_adapter_entry;

size_t msconnector_directive_adapter_count(void);
const msconnector_directive_adapter_entry *msconnector_directive_adapter_at(size_t index);
const msconnector_directive_adapter_entry *msconnector_directive_adapter_find(const char *canonical_name);
int msconnector_directive_adapter_validate_entry(const msconnector_directive_adapter_entry *entry, char *error, size_t error_len);
int msconnector_directive_adapter_validate_all(char *error, size_t error_len);

#ifdef __cplusplus
}
#endif

#endif
