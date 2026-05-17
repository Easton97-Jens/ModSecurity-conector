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

#ifdef __cplusplus
}
#endif

#endif
