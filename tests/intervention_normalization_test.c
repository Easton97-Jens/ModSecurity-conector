#include <stdio.h>

#include "msconnector/intervention.h"
#include "msconnector/phase.h"

static int failures;

#define CHECK(condition) do { \
    if (!(condition)) { \
        fprintf(stderr, "FAIL:%s:%d: %s\\n", __FILE__, __LINE__, #condition); \
        ++failures; \
    } \
} while (0)

int main(void)
{
    const msconnector_intervention native_request_body_limit =
        msconnector_intervention_make(1, 403, NULL,
            MSCONNECTOR_REQUEST_BODY_LIMIT_REJECTION_LOG);
    const msconnector_intervention native_request_body_limit_with_url =
        msconnector_intervention_make(1, 403, "",
            MSCONNECTOR_REQUEST_BODY_LIMIT_REJECTION_LOG);
    const msconnector_intervention native_request_body_limit_with_status =
        msconnector_intervention_make(1, 413, NULL,
            MSCONNECTOR_REQUEST_BODY_LIMIT_REJECTION_LOG);
    const msconnector_intervention native_request_body_limit_with_log =
        msconnector_intervention_make(1, 403, NULL, "ordinary rule intervention");

    CHECK(msconnector_intervention_has_redirect_url(NULL) == 0);
    CHECK(msconnector_intervention_has_redirect_url("") == 0);
    CHECK(msconnector_intervention_has_redirect_url("/blocked") == 1);

    CHECK(msconnector_intervention_normalize_status(NULL, 403, 451) == 403);
    CHECK(msconnector_intervention_normalize_status(NULL, 429, 451) == 429);
    CHECK(msconnector_intervention_normalize_status(NULL, 200, 451) == 451);
    CHECK(msconnector_intervention_normalize_status(NULL, 204, 451) == 451);
    CHECK(msconnector_intervention_normalize_status(NULL, 299, 451) == 451);
    CHECK(msconnector_intervention_normalize_status(NULL, 302, 451) == 451);
    CHECK(msconnector_intervention_normalize_status(NULL, 600, 451) == 451);
    CHECK(msconnector_intervention_normalize_status(NULL, 200, 299) == 403);

    CHECK(msconnector_intervention_normalize_status("/blocked", 301, 451) == 301);
    CHECK(msconnector_intervention_normalize_status("/blocked", 399, 451) == 399);
    CHECK(msconnector_intervention_normalize_status("/blocked", 200, 451) == 302);
    CHECK(msconnector_intervention_normalize_status("/blocked", 204, 451) == 302);
    CHECK(msconnector_intervention_normalize_status("/blocked", 299, 451) == 302);
    CHECK(msconnector_intervention_normalize_status("/blocked", 600, 451) == 302);

    CHECK(msconnector_intervention_is_request_body_limit_rejection(
        MSCONNECTOR_PHASE_REQUEST_BODY, &native_request_body_limit) == 1);
    CHECK(msconnector_intervention_is_request_body_limit_rejection(
        MSCONNECTOR_PHASE_REQUEST_HEADERS, &native_request_body_limit) == 0);
    CHECK(msconnector_intervention_is_request_body_limit_rejection(
        MSCONNECTOR_PHASE_REQUEST_BODY,
        &native_request_body_limit_with_url) == 0);
    CHECK(msconnector_intervention_is_request_body_limit_rejection(
        MSCONNECTOR_PHASE_REQUEST_BODY,
        &native_request_body_limit_with_status) == 0);
    CHECK(msconnector_intervention_is_request_body_limit_rejection(
        MSCONNECTOR_PHASE_REQUEST_BODY,
        &native_request_body_limit_with_log) == 0);

    return failures == 0 ? 0 : 1;
}
