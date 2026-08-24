/*
 * Manual smoke command (from the repository root):
 *
 *   cc -std=c17 -Wall -Wextra -Werror -Icommon/include \
 *     tests/test_resource_limits_hard_caps.c \
 *     common/src/resource_limits.c common/src/limits.c common/src/config.c \
 *     common/src/body_policy.c common/src/block_statuses.c common/src/http_status.c \
 *     -o /var/tmp/msconnector-resource-limits-hard-caps && \
 *   /var/tmp/msconnector-resource-limits-hard-caps
 *
 * This deliberately exercises the public validation boundaries.  The body
 * configuration contract is 10 MiB even though the smaller internal buffer
 * defaults remain implementation details of individual processing paths.
 */
#include "msconnector/config.h"
#include "msconnector/limits.h"
#include "msconnector/resource_limits.h"

#include <assert.h>
#include <stddef.h>
#include <stdio.h>

static void test_resource_limits(void) {
    msconnector_resource_limits limits;

    msconnector_resource_limits_init(&limits);
    assert(msconnector_resource_limits_validate(&limits));

#define ASSERT_LIMIT_REJECTED(member, cap) do { \
        msconnector_resource_limits_init(&limits); \
        limits.member = (cap) + 1U; \
        assert(!msconnector_resource_limits_validate(&limits)); \
    } while (0)

    ASSERT_LIMIT_REJECTED(max_header_count, MSCONNECTOR_MAX_HEADER_COUNT);
    ASSERT_LIMIT_REJECTED(max_header_name_size, MSCONNECTOR_MAX_HEADER_NAME_LENGTH);
    ASSERT_LIMIT_REJECTED(max_header_value_size, MSCONNECTOR_MAX_HEADER_VALUE_LENGTH);
    ASSERT_LIMIT_REJECTED(max_total_header_bytes, MSCONNECTOR_MAX_TOTAL_HEADER_BYTES);
    ASSERT_LIMIT_REJECTED(max_event_json_bytes, MSCONNECTOR_MAX_EVENT_JSON_BYTES);

    /* The configured body policy has a separate, documented 10 MiB cap. */
    ASSERT_LIMIT_REJECTED(max_request_body_bytes, MSCONNECTOR_MAX_CONFIG_BODY_BYTES);
    ASSERT_LIMIT_REJECTED(max_response_body_bytes, MSCONNECTOR_MAX_CONFIG_BODY_BYTES);

#undef ASSERT_LIMIT_REJECTED
}
static void test_config_body_limits(void) {
    msconnector_config config;

    msconnector_config_init(&config);
    msconnector_config_apply_defaults(&config);
    assert(msconnector_config_validate(&config, 0, 0));

    config.phase4_body_limit = MSCONNECTOR_MAX_CONFIG_BODY_BYTES;
    config.request_body_limit = MSCONNECTOR_MAX_CONFIG_BODY_BYTES;
    config.response_body_limit = MSCONNECTOR_MAX_CONFIG_BODY_BYTES;
    assert(msconnector_config_validate(&config, 0, 0));

    config.phase4_body_limit = MSCONNECTOR_MAX_CONFIG_BODY_BYTES + 1U;
    assert(!msconnector_config_validate(&config, 0, 0));
    config.phase4_body_limit = MSCONNECTOR_MAX_CONFIG_BODY_BYTES;

    config.request_body_limit = MSCONNECTOR_MAX_CONFIG_BODY_BYTES + 1U;
    assert(!msconnector_config_validate(&config, 0, 0));
    config.request_body_limit = MSCONNECTOR_MAX_CONFIG_BODY_BYTES;

    config.response_body_limit = MSCONNECTOR_MAX_CONFIG_BODY_BYTES + 1U;
    assert(!msconnector_config_validate(&config, 0, 0));
}

int main(void) {
    test_resource_limits();
    test_config_body_limits();
    puts("resource-limit hard-cap smoke: passed");
    return 0;
}
