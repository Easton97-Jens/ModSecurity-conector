#ifndef HAPROXY_MODSECURITY_BINDING_H
#define HAPROXY_MODSECURITY_BINDING_H

#include "msconnector/config.h"
#include "msconnector/crs.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct haproxy_modsecurity_decision {
    int disruptive;
    int status;
    int phase;
    int rule_id;
    int anomaly_score;
    char action[32];
    char redirect_url[1024];
    char rule_message[512];
    char matched_variable[256];
    char matched_value_snippet[256];
    char log_message[512];
} haproxy_modsecurity_decision;

typedef struct haproxy_modsecurity_header {
    const char *name;
    const char *value;
} haproxy_modsecurity_header;

typedef struct haproxy_modsecurity_request {
    const char *request_id;
    const char *client_ip;
    int client_port;
    const char *server_ip;
    int server_port;
    const char *method;
    const char *uri;
    const haproxy_modsecurity_header *headers;
    unsigned int header_count;
    const unsigned char *body;
    unsigned int body_len;
    const char *rules_file;
} haproxy_modsecurity_request;

typedef struct haproxy_modsecurity_response {
    int status;
    const char *protocol;
    const haproxy_modsecurity_header *headers;
    unsigned int header_count;
    const unsigned char *body;
    unsigned int body_len;
} haproxy_modsecurity_response;

typedef struct haproxy_modsecurity_engine_config {
    msconnector_config common_config;
    msconnector_crs_config crs_config;
    const char *connector_info;
    const char *modsecurity_conf;
    const char *crs_root;
    const char *rules_file;
    const char *rules_dir;
} haproxy_modsecurity_engine_config;

typedef struct haproxy_modsecurity_engine haproxy_modsecurity_engine;
typedef struct haproxy_modsecurity_transaction haproxy_modsecurity_transaction;

const char *haproxy_modsecurity_binding_scope(void);
int haproxy_modsecurity_engine_create(
    const haproxy_modsecurity_engine_config *config,
    haproxy_modsecurity_engine **engine,
    haproxy_modsecurity_decision *decision);
void haproxy_modsecurity_engine_destroy(haproxy_modsecurity_engine *engine);
int haproxy_modsecurity_transaction_begin(
    haproxy_modsecurity_engine *engine,
    const haproxy_modsecurity_request *request,
    haproxy_modsecurity_decision *decision,
    haproxy_modsecurity_transaction **transaction);
int haproxy_modsecurity_transaction_process_response_headers(
    haproxy_modsecurity_transaction *transaction,
    const haproxy_modsecurity_response *response,
    haproxy_modsecurity_decision *decision);
int haproxy_modsecurity_transaction_process_response_body(
    haproxy_modsecurity_transaction *transaction,
    const haproxy_modsecurity_response *response,
    haproxy_modsecurity_decision *decision);
void haproxy_modsecurity_transaction_finish(
    haproxy_modsecurity_transaction *transaction);
void haproxy_modsecurity_transaction_abort(
    haproxy_modsecurity_transaction *transaction);
int haproxy_modsecurity_eval_request(
    const haproxy_modsecurity_request *request,
    haproxy_modsecurity_decision *decision);
int haproxy_modsecurity_phase1_header_eval(
    const char *method,
    const char *uri,
    const char *test_header_value,
    haproxy_modsecurity_decision *decision);
int haproxy_modsecurity_phase1_header_self_test(
    haproxy_modsecurity_decision *decision);
int haproxy_modsecurity_request_body_self_test(
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
