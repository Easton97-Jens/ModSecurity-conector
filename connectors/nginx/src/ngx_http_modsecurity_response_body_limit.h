#ifndef NGX_HTTP_MODSECURITY_RESPONSE_BODY_LIMIT_H
#define NGX_HTTP_MODSECURITY_RESPONSE_BODY_LIMIT_H

#include "msconnector/intervention.h"
#include <stddef.h>
#include <string.h>

/* libModSecurity's native SecResponseBodyLimitAction Reject intervention is
 * rule-ID-free. Recognize only its exact observed signature; all other
 * interventions must retain the ordinary rule-ID validation contract.
 * The log is a valid Engine-owned NUL-terminated string. Compare at most
 * sizeof(expected) bytes, including the terminator, to reject suffixes. */
static inline int
ngx_http_modsecurity_is_response_body_limit_rejection(
    enum msconnector_phase phase,
    const msconnector_intervention *intervention,
    const char *rule_id)
{
    static const char expected[] =
        "Response body limit is marked to reject the request";

    return intervention != NULL &&
        phase == MSCONNECTOR_PHASE_RESPONSE_BODY &&
        intervention->disruptive == 1 &&
        intervention->status == 403 &&
        intervention->redirect_url == NULL &&
        (rule_id == NULL || rule_id[0] == '\0') &&
        intervention->log_message != NULL &&
        strncmp(intervention->log_message, expected, sizeof(expected)) == 0;
}

#endif
