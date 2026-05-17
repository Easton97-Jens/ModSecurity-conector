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

#ifdef __cplusplus
}
#endif

#endif
