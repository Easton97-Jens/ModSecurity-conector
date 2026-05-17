#include "msconnector/intervention.h"

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
