#include "msconnector/directive_spec.h"
#include "msconnector/directives.h"
#include <string.h>

static const msconnector_directive_spec specs[] = {
    {MSCONNECTOR_DIRECTIVE_MODSECURITY, MSCONNECTOR_DIRECTIVE_VALUE_BOOL, "off", "on|off", "Enable or disable connector processing."},
    {MSCONNECTOR_DIRECTIVE_RULES, MSCONNECTOR_DIRECTIVE_VALUE_STRING, 0, 0, "Inline rules text."},
    {MSCONNECTOR_DIRECTIVE_RULES_FILE, MSCONNECTOR_DIRECTIVE_VALUE_PATH, 0, 0, "Rules file path."},
    {MSCONNECTOR_DIRECTIVE_RULES_REMOTE, MSCONNECTOR_DIRECTIVE_VALUE_STRING, 0, "key url", "Remote rules key and URL."},
    {MSCONNECTOR_DIRECTIVE_TRANSACTION_ID, MSCONNECTOR_DIRECTIVE_VALUE_STRING, 0, 0, "Static transaction ID."},
    {MSCONNECTOR_DIRECTIVE_TRANSACTION_ID_EXPR, MSCONNECTOR_DIRECTIVE_VALUE_STRING, 0, 0, "Connector-parsed transaction ID expression."},
    {MSCONNECTOR_DIRECTIVE_PHASE4_MODE, MSCONNECTOR_DIRECTIVE_VALUE_ENUM, "safe", "minimal|safe|strict", "Response-body handling mode model."},
    {MSCONNECTOR_DIRECTIVE_PHASE4_CONTENT_TYPES_FILE, MSCONNECTOR_DIRECTIVE_VALUE_PATH, 0, 0, "Content types file for response-body policy."},
    {MSCONNECTOR_DIRECTIVE_PHASE4_LOG, MSCONNECTOR_DIRECTIVE_VALUE_PATH, 0, 0, "Phase 4 log path."},
    {MSCONNECTOR_DIRECTIVE_PHASE4_BODY_LIMIT, MSCONNECTOR_DIRECTIVE_VALUE_SIZE, "1048576", 0, "Phase 4 body limit."},
    {MSCONNECTOR_DIRECTIVE_USE_ERROR_LOG, MSCONNECTOR_DIRECTIVE_VALUE_BOOL, "on", "on|off", "Use connector error log."}
};

const msconnector_directive_spec *msconnector_directive_specs(void) {
    return specs;
}

size_t msconnector_directive_spec_count(void) {
    return sizeof(specs) / sizeof(specs[0]);
}

const msconnector_directive_spec *msconnector_directive_spec_find(const char *name) {
    if (name == 0) {
        return 0;
    }

    for (size_t index = 0; index < msconnector_directive_spec_count(); ++index) {
        if (strcmp(specs[index].name, name) == 0) {
            return &specs[index];
        }
    }

    return 0;
}
