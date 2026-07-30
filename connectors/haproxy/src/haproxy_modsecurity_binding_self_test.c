#include "haproxy_modsecurity_binding.h"

#include <stdio.h>
#include <string.h>

static void print_usage(const char *program) {
    fprintf(stderr, "usage: %s --describe|--self-test LIFECYCLE_RULES|--self-test-crs PREAMBLE\n",
        program);
}

static int lifecycle_failure(
        haproxy_modsecurity_decision *decision,
        const char *label) {
    if (decision != 0) {
        snprintf(decision->log_message, sizeof(decision->log_message),
            "body wrapper lifecycle self-test failed: %s", label);
    }
    return 1;
}

static int expect_failure(
        int rc,
        const haproxy_modsecurity_decision *observed,
        int expected_phase,
        const char *expected_message,
        const char *label,
        haproxy_modsecurity_decision *decision) {
    if (rc != 1 || observed == 0 || observed->phase != expected_phase ||
            strcmp(observed->log_message, expected_message) != 0) {
        return lifecycle_failure(decision, label);
    }
    return 0;
}

static int expect_non_disruptive(
        int rc,
        const haproxy_modsecurity_decision *observed,
        int expected_phase,
        const char *label,
        haproxy_modsecurity_decision *decision) {
    if (rc != 0 || observed == 0 || observed->phase != expected_phase ||
            observed->disruptive != 0) {
        return lifecycle_failure(decision, label);
    }
    return 0;
}

typedef int (*body_append_function)(
    haproxy_modsecurity_transaction *transaction,
    const unsigned char *body,
    unsigned int body_len,
    haproxy_modsecurity_decision *decision);

typedef int (*body_finish_function)(
    haproxy_modsecurity_transaction *transaction,
    haproxy_modsecurity_decision *decision);

struct body_wrapper_lifecycle {
    int phase;
    const char *missing_transaction_message;
    const char *missing_body_message;
    const char *append_after_eos_message;
    const char *finish_twice_message;
    const unsigned char *body;
    unsigned int body_len;
    body_append_function append;
    body_finish_function finish;
};

static int check_null_body_transaction(
        const struct body_wrapper_lifecycle *phase,
        haproxy_modsecurity_decision *observed,
        haproxy_modsecurity_decision *decision) {
    int rc = phase->append(0, phase->body, phase->body_len, observed);

    return expect_failure(rc, observed, phase->phase,
        phase->missing_transaction_message, "null body transaction", decision);
}

static int run_body_lifecycle(
        const struct body_wrapper_lifecycle *phase,
        haproxy_modsecurity_transaction *transaction,
        haproxy_modsecurity_decision *observed,
        haproxy_modsecurity_decision *decision) {
    int rc = phase->append(transaction, 0, 1U, observed);

    if (expect_failure(rc, observed, phase->phase, phase->missing_body_message,
            "null nonzero body chunk", decision) != 0) {
        return 1;
    }
    rc = phase->append(transaction, phase->body, phase->body_len, observed);
    if (expect_non_disruptive(rc, observed, phase->phase, "body append",
            decision) != 0) {
        return 1;
    }
    rc = phase->finish(transaction, observed);
    if (expect_non_disruptive(rc, observed, phase->phase, "body finish",
            decision) != 0) {
        return 1;
    }
    rc = phase->append(transaction, phase->body, phase->body_len, observed);
    if (expect_failure(rc, observed, phase->phase, phase->append_after_eos_message,
            "body append after eos", decision) != 0) {
        return 1;
    }
    rc = phase->finish(transaction, observed);
    return expect_failure(rc, observed, phase->phase, phase->finish_twice_message,
        "body finish twice", decision);
}

static int check_response_body_requires_headers(
        haproxy_modsecurity_transaction *transaction,
        const struct body_wrapper_lifecycle *response_phase,
        haproxy_modsecurity_decision *observed,
        haproxy_modsecurity_decision *decision) {
    int rc = response_phase->append(transaction, response_phase->body,
        response_phase->body_len, observed);

    return expect_failure(rc, observed, response_phase->phase,
        "response headers must be processed before response body chunks",
        "response append before headers", decision);
}

static int run_body_wrapper_lifecycle_self_test(
        const char *rules_file,
        haproxy_modsecurity_decision *decision) {
    static const unsigned char request_body[] = "token=allow";
    static const unsigned char response_body[] = "response=allow";
    const struct body_wrapper_lifecycle request_phase = {
        .phase = 2,
        .missing_transaction_message = "missing transaction or request body",
        .missing_body_message =
            "request body pointer is required when length is nonzero",
        .append_after_eos_message = "request body append after end-of-stream",
        .finish_twice_message = "request body may only be finalized once",
        .body = request_body,
        .body_len = (unsigned int)(sizeof(request_body) - 1U),
        .append = haproxy_modsecurity_transaction_append_request_body_chunk,
        .finish = haproxy_modsecurity_transaction_finish_request_body
    };
    const struct body_wrapper_lifecycle response_phase = {
        .phase = 4,
        .missing_transaction_message = "missing transaction or response body",
        .missing_body_message =
            "response body pointer is required when length is nonzero",
        .append_after_eos_message = "response body append after end-of-stream",
        .finish_twice_message = "response body may only be finalized once",
        .body = response_body,
        .body_len = (unsigned int)(sizeof(response_body) - 1U),
        .append = haproxy_modsecurity_transaction_append_response_body_chunk,
        .finish = haproxy_modsecurity_transaction_finish_response_body
    };
    haproxy_modsecurity_engine_config config;
    haproxy_modsecurity_engine *engine = 0;
    haproxy_modsecurity_transaction *transaction = 0;
    haproxy_modsecurity_header request_headers[2];
    haproxy_modsecurity_header response_headers[1];
    haproxy_modsecurity_request request;
    haproxy_modsecurity_response response;
    haproxy_modsecurity_decision observed;
    int result = 1;
    int rc;

    if (rules_file == 0 || rules_file[0] == '\0') {
        return lifecycle_failure(decision, "missing lifecycle rules file");
    }
    request_headers[0].name = "Content-Type";
    request_headers[0].value = "application/x-www-form-urlencoded";
    request_headers[1].name = "Content-Length";
    request_headers[1].value = "11";
    memset(&request, 0, sizeof(request));
    request.method = "POST";
    request.uri = "/haproxy-binding-lifecycle-self-test";
    request.headers = request_headers;
    request.header_count = 2U;

    response_headers[0].name = "Content-Type";
    response_headers[0].value = "text/plain";
    memset(&response, 0, sizeof(response));
    response.status = 200;
    response.protocol = "HTTP/1.1";
    response.headers = response_headers;
    response.header_count = 1U;

    memset(&config, 0, sizeof(config));
    config.rules_file = rules_file;
    rc = haproxy_modsecurity_engine_create(&config, &engine, &observed);
    if (rc != 0 || engine == 0) {
        return lifecycle_failure(decision, "engine creation");
    }

    if (check_null_body_transaction(&request_phase, &observed, decision) != 0) {
        goto cleanup;
    }
    if (check_null_body_transaction(&response_phase, &observed, decision) != 0) {
        goto cleanup;
    }

    rc = haproxy_modsecurity_transaction_begin_request(engine, &request, &observed,
        &transaction);
    if (expect_non_disruptive(rc, &observed, 1, "request begin", decision) != 0) {
        goto cleanup;
    }
    if (transaction == 0) {
        lifecycle_failure(decision, "request begin transaction");
        goto cleanup;
    }
    if (run_body_lifecycle(&request_phase, transaction, &observed, decision) != 0) {
        goto cleanup;
    }

    if (check_response_body_requires_headers(transaction, &response_phase, &observed,
            decision) != 0) {
        goto cleanup;
    }
    rc = haproxy_modsecurity_transaction_process_response_headers(transaction, &response,
        &observed);
    if (expect_non_disruptive(rc, &observed, 3, "response headers", decision) != 0) {
        goto cleanup;
    }
    if (run_body_lifecycle(&response_phase, transaction, &observed, decision) != 0) {
        goto cleanup;
    }
    result = 0;

cleanup:
    if (transaction != 0) {
        haproxy_modsecurity_transaction_finish(transaction);
    }
    haproxy_modsecurity_engine_destroy(engine);
    return result;
}

int main(int argc, char **argv) {
    haproxy_modsecurity_decision decision;
    int rc;

    if (argc == 2 && strcmp(argv[1], "--describe") == 0) {
        printf("%s\n", haproxy_modsecurity_binding_scope());
        printf("limitations: self-test only; live enforcement requires make smoke-haproxy; no RESPONSE_BODY verification\n");
        return 0;
    }
    if (argc == 3 && strcmp(argv[1], "--self-test-crs") == 0) {
        rc = haproxy_modsecurity_crs_sqli_self_test(argv[2], &decision);
        if (rc == 0) {
            printf("haproxy_modsecurity_binding_crs_self_test: PASS\n");
            printf("modsecurity_binding_status: crs-self-test-verified\n");
            printf("runtime_verified: false\n");
            printf("runtime_status: blocked\n");
            printf("response_body_verified: false\n");
            printf("crs_verified: self-test-only\n");
            printf("verified_case: crs_sqli_anomaly_block\n");
            printf("crs_preamble_file: %s\n", argv[2]);
            printf("decision_status: %d\n", decision.status);
            printf("decision_disruptive: %d\n", decision.disruptive);
            return 0;
        }
        printf("haproxy_modsecurity_binding_crs_self_test: BLOCKED\n");
        printf("modsecurity_binding_status: blocked\n");
        printf("runtime_verified: false\n");
        printf("runtime_status: blocked\n");
        printf("response_body_verified: false\n");
        printf("crs_verified: false\n");
        if (decision.log_message[0] != '\0') {
            printf("reason: %s\n", decision.log_message);
        } else {
            printf("reason: CRS binding/load path missing\n");
        }
        return 77;
    }
    if (argc != 3 || strcmp(argv[1], "--self-test") != 0) {
        print_usage(argv[0]);
        return 2;
    }

    rc = haproxy_modsecurity_phase1_header_self_test(&decision);
    if (rc == 0) {
        rc = haproxy_modsecurity_request_body_self_test(&decision);
    }
    if (rc == 0) {
        rc = run_body_wrapper_lifecycle_self_test(argv[2], &decision);
    }
    if (rc == 0) {
        printf("haproxy_modsecurity_binding_self_test: PASS\n");
        printf("modsecurity_binding_status: self-test-verified\n");
        printf("runtime_verified: false\n");
        printf("runtime_status: blocked\n");
        printf("response_body_verified: false\n");
        printf("crs_verified: false\n");
        printf("request_body_verified: self-test-only\n");
        printf("request_body_lifecycle_verified: self-test-only\n");
        printf("response_body_lifecycle_verified: self-test-only\n");
        printf("decision_status: %d\n", decision.status);
        printf("decision_disruptive: %d\n", decision.disruptive);
        return 0;
    }

    printf("haproxy_modsecurity_binding_self_test: BLOCKED\n");
    printf("modsecurity_binding_status: blocked\n");
    printf("runtime_verified: false\n");
    printf("runtime_status: blocked\n");
    printf("response_body_verified: false\n");
    printf("crs_verified: false\n");
    if (decision.log_message[0] != '\0') {
        printf("reason: %s\n", decision.log_message);
    } else {
        printf("reason: modsecurity binding missing or not buildable\n");
    }
    return 77;
}
