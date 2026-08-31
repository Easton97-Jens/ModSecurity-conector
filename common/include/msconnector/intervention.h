#ifndef MSCONNECTOR_INTERVENTION_H
#define MSCONNECTOR_INTERVENTION_H

#ifdef __cplusplus
extern "C" {
#endif

typedef struct msconnector_intervention {
    int disruptive;
    int status;
    const char *redirect_url;
    const char *log_message;
} msconnector_intervention;

msconnector_intervention msconnector_intervention_make(
    int disruptive,
    int status,
    const char *redirect_url,
    const char *log_message);
msconnector_intervention msconnector_intervention_none(void);
int msconnector_intervention_is_disruptive(const msconnector_intervention *intervention);

/* A native redirect is meaningful only with a nonempty URL.  Keep this
 * distinction shared so adapters do not turn an empty engine-owned buffer
 * into a host redirect. */
int msconnector_intervention_has_redirect_url(const char *redirect_url);

/* Map one disruptive native intervention onto the canonical host status.
 * Redirects retain a valid 3xx status or use 302; status-only interventions
 * retain an allowed blocking status or use the selected default block status.
 * URL syntax/ownership remains the adapter's responsibility. */
int msconnector_intervention_normalize_status(const char *redirect_url,
    int requested_status, int default_block_status);

#ifdef __cplusplus
}
#endif

#endif
