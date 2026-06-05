#include "haproxy_modsecurity_binding.h"

#include <stdio.h>
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

const char *haproxy_modsecurity_binding_scope(void) {
    return "HAProxy libmodsecurity phase-1 header binding self-test only";
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
    ModSecurity *modsec = 0;
    RulesSet *rules = 0;
    Transaction *transaction = 0;
    const char *rules_error = 0;
    ModSecurityIntervention intervention;
    int rc = 1;
    const char *safe_method = method != 0 && method[0] != '\0' ? method : "GET";
    const char *safe_uri = uri != 0 && uri[0] != '\0' ? uri : "/";

    if (decision == 0) {
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
        "HAProxy diagnostic SPOA ModSecurity phase-1 binding");

    rules = msc_create_rules_set();
    if (rules == 0) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "msc_create_rules_set returned null");
        goto cleanup;
    }
    if (msc_rules_add(rules, rules_text, &rules_error) < 0) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            rules_error != 0 ? rules_error : "msc_rules_add failed");
        if (rules_error != 0) {
            msc_rules_error_cleanup(rules_error);
        }
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
    if (test_header_value != 0 && test_header_value[0] != '\0') {
        if (msc_add_request_header(transaction,
                (const unsigned char *)"X-Haproxy-ModSecurity-Test",
                (const unsigned char *)test_header_value) < 0) {
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

    intervention.status = 200;
    intervention.pause = 0;
    intervention.url = 0;
    intervention.log = 0;
    intervention.disruptive = 0;
    if (msc_intervention(transaction, &intervention) != 0) {
        decision->disruptive = intervention.disruptive;
        decision->status = intervention.status;
        copy_message(decision->log_message, sizeof(decision->log_message),
            intervention.log);
    }
    msc_intervention_cleanup(&intervention);
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

int haproxy_modsecurity_crs_sqli_eval(
        const char *method,
        const char *uri,
        const char *host,
        const char *crs_preamble_file,
        haproxy_modsecurity_decision *decision) {
    static const char local_rules_text[] =
        "SecRuleEngine On\n"
        "SecAction \"id:199901,phase:2,pass,nolog\"\n";
    ModSecurity *modsec = 0;
    RulesSet *rules = 0;
    Transaction *transaction = 0;
    const char *rules_error = 0;
    ModSecurityIntervention intervention;
    int rc = 1;
    const char *safe_method = method != 0 && method[0] != '\0' ? method : "GET";
    const char *safe_uri = uri != 0 && uri[0] != '\0' ? uri : "/";
    const char *safe_host = host != 0 && host[0] != '\0' ? host : "localhost";

    if (decision == 0) {
        return 1;
    }
    memset(decision, 0, sizeof(*decision));
    decision->status = 200;

    if (crs_preamble_file == 0 || crs_preamble_file[0] == '\0') {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "CRS preamble file is not defined");
        return 1;
    }

    modsec = msc_init();
    if (modsec == 0) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "msc_init returned null");
        goto cleanup;
    }
    msc_set_connector_info(modsec,
        "HAProxy diagnostic SPOA ModSecurity CRS binding");

    rules = msc_create_rules_set();
    if (rules == 0) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "msc_create_rules_set returned null");
        goto cleanup;
    }
    if (msc_rules_add_file(rules, crs_preamble_file, &rules_error) < 0) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            rules_error != 0 ? rules_error : "msc_rules_add_file failed");
        if (rules_error != 0) {
            msc_rules_error_cleanup(rules_error);
        }
        goto cleanup;
    }
    if (msc_rules_add(rules, local_rules_text, &rules_error) < 0) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            rules_error != 0 ? rules_error : "msc_rules_add local CRS case failed");
        if (rules_error != 0) {
            msc_rules_error_cleanup(rules_error);
        }
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
    if (msc_add_request_header(transaction,
            (const unsigned char *)"Host",
            (const unsigned char *)safe_host) < 0) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "msc_add_request_header Host failed");
        goto cleanup;
    }
    if (msc_process_request_headers(transaction) < 0) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "msc_process_request_headers failed");
        goto cleanup;
    }
    if (msc_process_request_body(transaction) < 0) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "msc_process_request_body failed");
        goto cleanup;
    }

    intervention.status = 200;
    intervention.pause = 0;
    intervention.url = 0;
    intervention.log = 0;
    intervention.disruptive = 0;
    if (msc_intervention(transaction, &intervention) != 0) {
        decision->disruptive = intervention.disruptive;
        decision->status = intervention.status;
        copy_message(decision->log_message, sizeof(decision->log_message),
            intervention.log);
    }
    msc_intervention_cleanup(&intervention);
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
