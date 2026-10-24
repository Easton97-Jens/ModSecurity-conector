#include "msconnector/intervention.h"
#include "msconnector/block_statuses.h"

#include <string.h>

msconnector_intervention msconnector_intervention_make(
    int disruptive,
    int status,
    const char *redirect_url,
    const char *log_message) {
    msconnector_intervention intervention;
    intervention.disruptive = disruptive != 0;
    intervention.status = intervention.disruptive ? status : 0;
    intervention.redirect_url = redirect_url;
    intervention.log_message = log_message;
    return intervention;
}

msconnector_intervention msconnector_intervention_none(void) {
    return msconnector_intervention_make(0, 0, 0, 0);
}

int msconnector_intervention_is_disruptive(const msconnector_intervention *intervention) {
    return intervention != 0 && intervention->disruptive != 0;
}

int msconnector_intervention_has_redirect_url(const char *redirect_url) {
    return redirect_url != 0 && redirect_url[0] != '\0';
}

int msconnector_intervention_is_request_body_limit_rejection(
    enum msconnector_phase phase,
    const msconnector_intervention *intervention) {
    return intervention != 0 &&
        intervention->disruptive != 0 &&
        phase == MSCONNECTOR_PHASE_REQUEST_BODY &&
        intervention->status == 403 &&
        intervention->redirect_url == 0 &&
        intervention->log_message != 0 &&
        strcmp(intervention->log_message,
            MSCONNECTOR_REQUEST_BODY_LIMIT_REJECTION_LOG) == 0;
}

int msconnector_intervention_normalize_status(const char *redirect_url,
    int requested_status, int default_block_status) {
    if (msconnector_intervention_has_redirect_url(redirect_url)) {
        return requested_status >= 300 && requested_status < 400
            ? requested_status : 302;
    }
    if (msconnector_block_status_is_allowed(requested_status)) {
        return requested_status;
    }
    return msconnector_block_status_is_allowed(default_block_status)
        ? default_block_status : MSCONNECTOR_DEFAULT_BLOCK_STATUS;
}
