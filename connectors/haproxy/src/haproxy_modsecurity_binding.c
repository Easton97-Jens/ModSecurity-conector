#include "haproxy_modsecurity_binding.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <modsecurity/modsecurity.h>
#include <modsecurity/rules_set.h>
#include <modsecurity/transaction.h>

#define HAPROXY_MODSECURITY_EXPECTED_STATUS 403

static void copy_message(char *dst, size_t dst_len, const char *src) {
    if (dst == 0 || dst_len == 0) {
        return;
    }
    if (src == 0) {
        dst[0] = '\0';
        return;
    }
    snprintf(dst, dst_len, "%s", src);
}

static void init_intervention(ModSecurityIntervention *intervention) {
    intervention->status = 200;
    intervention->pause = 0;
    intervention->url = 0;
    intervention->log = 0;
    intervention->disruptive = 0;
}

static void capture_intervention(
        Transaction *transaction,
        haproxy_modsecurity_decision *decision) {
    ModSecurityIntervention intervention;

    init_intervention(&intervention);
    if (msc_intervention(transaction, &intervention) != 0) {
        decision->disruptive = intervention.disruptive;
        decision->status = intervention.status > 0 ?
            intervention.status : HAPROXY_MODSECURITY_EXPECTED_STATUS;
        copy_message(decision->log_message, sizeof(decision->log_message),
            intervention.log);
    }
    msc_intervention_cleanup(&intervention);
}

static int load_rules(
        RulesSet *rules,
        const char *rules_file,
        const char *rules_text,
        haproxy_modsecurity_decision *decision) {
    const char *rules_error = 0;
    int rc;
    int loaded = 0;

    if (rules_file != 0 && rules_file[0] != '\0') {
        rc = msc_rules_add_file(rules, rules_file, &rules_error);
        if (rc < 0) {
            copy_message(decision->log_message, sizeof(decision->log_message),
                rules_error != 0 ? rules_error : "failed to load rules file");
            if (rules_error != 0) {
                msc_rules_error_cleanup(rules_error);
            }
            return -1;
        }
        loaded = 1;
    }
    rules_error = 0;
    if (rules_text != 0 && rules_text[0] != '\0') {
        rc = msc_rules_add(rules, rules_text, &rules_error);
        if (rc < 0) {
            copy_message(decision->log_message, sizeof(decision->log_message),
                rules_error != 0 ? rules_error : "failed to load rules text");
            if (rules_error != 0) {
                msc_rules_error_cleanup(rules_error);
            }
            return -1;
        }
        loaded = 1;
    }
    if (!loaded) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "rules file is not defined");
        return -1;
    }
    return 0;
}

static int eval_request_internal(
        const haproxy_modsecurity_request *request,
        const char *rules_text,
        haproxy_modsecurity_decision *decision) {
    ModSecurity *modsec = 0;
    RulesSet *rules = 0;
    Transaction *transaction = 0;
    int rc = 1;
    const char *safe_method = request != 0 && request->method != 0 &&
        request->method[0] != '\0' ? request->method : "GET";
    const char *safe_uri = request != 0 && request->uri != 0 &&
        request->uri[0] != '\0' ? request->uri : "/";
    unsigned int i;

    if (decision == 0 || request == 0) {
        return 1;
    }
    memset(decision, 0, sizeof(*decision));
    decision->status = 200;

    modsec = msc_init();
    if (modsec == 0) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "msc_init returned null");
        goto cleanup;
    }
    msc_set_connector_info(modsec,
        "HAProxy SPOA live YAML runtime binding");

    rules = msc_create_rules_set();
    if (rules == 0) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "msc_create_rules_set returned null");
        goto cleanup;
    }
    if (load_rules(rules, request->rules_file, rules_text, decision) != 0) {
        goto cleanup;
    }

    transaction = msc_new_transaction(modsec, rules, 0);
    if (transaction == 0) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "msc_new_transaction returned null");
        goto cleanup;
    }
    if (msc_process_connection(transaction, "127.0.0.1", 49152,
            "127.0.0.1", 80) < 0) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "msc_process_connection failed");
        goto cleanup;
    }
    if (msc_process_uri(transaction, safe_uri, safe_method, "1.1") < 0) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "msc_process_uri failed");
        goto cleanup;
    }
    for (i = 0; i < request->header_count; ++i) {
        const char *name = request->headers[i].name;
        const char *value = request->headers[i].value;
        if (name == 0 || name[0] == '\0') {
            continue;
        }
        if (value == 0) {
            value = "";
        }
        if (msc_add_request_header(transaction,
                (const unsigned char *)name,
                (const unsigned char *)value) < 0) {
            copy_message(decision->log_message, sizeof(decision->log_message),
                "msc_add_request_header failed");
            goto cleanup;
        }
    }
    if (msc_process_request_headers(transaction) < 0) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "msc_process_request_headers failed");
        goto cleanup;
    }
    capture_intervention(transaction, decision);
    if (decision->disruptive != 0) {
        msc_process_logging(transaction);
        rc = 0;
        goto cleanup;
    }

    if (request->body != 0 && request->body_len > 0) {
        if (msc_append_request_body(transaction,
                request->body, (size_t)request->body_len) < 0) {
            copy_message(decision->log_message, sizeof(decision->log_message),
                "msc_append_request_body failed");
            goto cleanup;
        }
    }
    if (msc_process_request_body(transaction) < 0) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "msc_process_request_body failed");
        goto cleanup;
    }
    capture_intervention(transaction, decision);
    msc_process_logging(transaction);
    rc = 0;

cleanup:
    if (transaction != 0) {
        msc_transaction_cleanup(transaction);
    }
    if (rules != 0) {
        msc_rules_cleanup(rules);
    }
    if (modsec != 0) {
        msc_cleanup(modsec);
    }
    return rc;
}

const char *haproxy_modsecurity_binding_scope(void) {
    return "HAProxy libmodsecurity live request binding with request headers/body support";
}

int haproxy_modsecurity_eval_request(
        const haproxy_modsecurity_request *request,
        haproxy_modsecurity_decision *decision) {
    return eval_request_internal(request, 0, decision);
}

int haproxy_modsecurity_phase1_header_eval(
        const char *method,
        const char *uri,
        const char *test_header_value,
        haproxy_modsecurity_decision *decision) {
    static const char rules_text[] =
        "SecRuleEngine On\n"
        "SecRequestBodyAccess Off\n"
        "SecRule REQUEST_HEADERS:X-Haproxy-ModSecurity-Test "
        "\"@streq block\" "
        "\"id:1000001,phase:1,deny,status:403,"
        "msg:'HAProxy ModSecurity binding self-test block'\"\n";
    haproxy_modsecurity_header headers[1];
    haproxy_modsecurity_request request;

    headers[0].name = "X-Haproxy-ModSecurity-Test";
    headers[0].value = test_header_value != 0 ? test_header_value : "";
    memset(&request, 0, sizeof(request));
    request.method = method;
    request.uri = uri;
    request.headers = headers;
    request.header_count = test_header_value != 0 && test_header_value[0] != '\0' ? 1U : 0U;
    return eval_request_internal(&request, rules_text, decision);
}

int haproxy_modsecurity_phase1_header_self_test(
        haproxy_modsecurity_decision *decision) {
    int rc;

    rc = haproxy_modsecurity_phase1_header_eval("GET",
        "/haproxy-binding-self-test", "block", decision);
    if (rc != 0) {
        return rc;
    }
    if (decision != 0 && decision->disruptive != 0 &&
            decision->status == HAPROXY_MODSECURITY_EXPECTED_STATUS) {
        return 0;
    }
    if (decision != 0) {
        snprintf(decision->log_message, sizeof(decision->log_message),
            "expected disruptive status %d, got disruptive=%d status=%d",
            HAPROXY_MODSECURITY_EXPECTED_STATUS, decision->disruptive,
            decision->status);
    }
    return 1;
}

int haproxy_modsecurity_request_body_self_test(
        haproxy_modsecurity_decision *decision) {
    static const char rules_text[] =
        "SecRuleEngine On\n"
        "SecRequestBodyAccess On\n"
        "SecRule ARGS:token \"@streq block\" "
        "\"id:1000002,phase:2,deny,status:403,"
        "msg:'HAProxy ModSecurity binding request-body self-test block'\"\n";
    static const unsigned char body[] = "token=block";
    haproxy_modsecurity_header headers[2];
    haproxy_modsecurity_request request;
    int rc;

    headers[0].name = "Content-Type";
    headers[0].value = "application/x-www-form-urlencoded";
    headers[1].name = "Content-Length";
    headers[1].value = "11";
    memset(&request, 0, sizeof(request));
    request.method = "POST";
    request.uri = "/haproxy-binding-body-self-test";
    request.headers = headers;
    request.header_count = 2U;
    request.body = body;
    request.body_len = (unsigned int)(sizeof(body) - 1U);
    rc = eval_request_internal(&request, rules_text, decision);
    if (rc != 0) {
        return rc;
    }
    if (decision != 0 && decision->disruptive != 0 &&
            decision->status == HAPROXY_MODSECURITY_EXPECTED_STATUS) {
        return 0;
    }
    if (decision != 0) {
        snprintf(decision->log_message, sizeof(decision->log_message),
            "expected request-body disruptive status %d, got disruptive=%d status=%d",
            HAPROXY_MODSECURITY_EXPECTED_STATUS, decision->disruptive,
            decision->status);
    }
    return 1;
}

int haproxy_modsecurity_crs_sqli_eval(
        const char *method,
        const char *uri,
        const char *host,
        const char *crs_preamble_file,
        haproxy_modsecurity_decision *decision) {
    static const char rules_text[] =
        "SecRuleEngine On\n"
        "SecAction \"id:199901,phase:2,pass,nolog\"\n";
    haproxy_modsecurity_header headers[1];
    haproxy_modsecurity_request request;

    headers[0].name = "Host";
    headers[0].value = host != 0 && host[0] != '\0' ? host : "localhost";
    memset(&request, 0, sizeof(request));
    request.method = method;
    request.uri = uri;
    request.headers = headers;
    request.header_count = 1U;
    request.rules_file = crs_preamble_file;
    return eval_request_internal(&request, rules_text, decision);
}

int haproxy_modsecurity_crs_sqli_self_test(
        const char *crs_preamble_file,
        haproxy_modsecurity_decision *decision) {
    haproxy_modsecurity_decision pass_decision;
    int rc;

    rc = haproxy_modsecurity_crs_sqli_eval("GET",
        "/?id=1%20UNION%20SELECT%20password%20FROM%20users",
        "localhost", crs_preamble_file, decision);
    if (rc != 0) {
        return rc;
    }
    if (decision == 0 || decision->disruptive == 0 ||
            decision->status != HAPROXY_MODSECURITY_EXPECTED_STATUS) {
        if (decision != 0) {
            snprintf(decision->log_message, sizeof(decision->log_message),
                "expected CRS disruptive status %d, got disruptive=%d status=%d",
                HAPROXY_MODSECURITY_EXPECTED_STATUS,
                decision->disruptive, decision->status);
        }
        return 1;
    }

    rc = haproxy_modsecurity_crs_sqli_eval("GET", "/diagnostic.txt",
        "localhost", crs_preamble_file, &pass_decision);
    if (rc != 0) {
        if (decision != 0) {
            copy_message(decision->log_message, sizeof(decision->log_message),
                pass_decision.log_message);
        }
        return rc;
    }
    if (pass_decision.disruptive != 0) {
        if (decision != 0) {
            snprintf(decision->log_message, sizeof(decision->log_message),
                "expected CRS pass probe to be non-disruptive, got status=%d",
                pass_decision.status);
        }
        return 1;
    }
    return 0;
}
