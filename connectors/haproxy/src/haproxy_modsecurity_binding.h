#ifndef HAPROXY_MODSECURITY_BINDING_H
#define HAPROXY_MODSECURITY_BINDING_H

#ifdef __cplusplus
extern "C" {
#endif

typedef struct haproxy_modsecurity_decision {
    int disruptive;
    int status;
    char log_message[512];
} haproxy_modsecurity_decision;

const char *haproxy_modsecurity_binding_scope(void);
int haproxy_modsecurity_phase1_header_eval(
    const char *method,
    const char *uri,
    const char *test_header_value,
    haproxy_modsecurity_decision *decision);
int haproxy_modsecurity_phase1_header_self_test(
    haproxy_modsecurity_decision *decision);
int haproxy_modsecurity_crs_sqli_eval(
    const char *method,
    const char *uri,
    const char *host,
    const char *crs_preamble_file,
    haproxy_modsecurity_decision *decision);
int haproxy_modsecurity_crs_sqli_self_test(
    const char *crs_preamble_file,
    haproxy_modsecurity_decision *decision);

#ifdef __cplusplus
}
#endif

#endif
