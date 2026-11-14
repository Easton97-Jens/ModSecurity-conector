#ifndef NGX_HTTP_MODSECURITY_RESPONSE_BODY_LIMIT_H
#define NGX_HTTP_MODSECURITY_RESPONSE_BODY_LIMIT_H

#include "msconnector/intervention.h"
#include <stddef.h>

/* The supported libModSecurity appendResponseBody contract evaluates no
 * response rules: its only new disruptive result is native limit Reject.
 * The caller drains earlier phases, enters this boundary only after a valid
 * append result, and clears it before EOS rule evaluation. Require the native
 * rule-free 403 shape as well; unexpected interventions remain engine errors.
 * Free-text log content is deliberately not part of the classification. */
static inline int
ngx_http_modsecurity_is_response_body_limit_rejection(
    enum msconnector_phase phase,
    const msconnector_intervention *intervention,
    const char *rule_id, int append_active, int body_eos)
{
    return append_active && !body_eos && intervention != NULL &&
        phase == MSCONNECTOR_PHASE_RESPONSE_BODY &&
        intervention->disruptive == 1 &&
        intervention->status == 403 &&
        intervention->redirect_url == NULL &&
        (rule_id == NULL || rule_id[0] == '\0');
}

#endif
