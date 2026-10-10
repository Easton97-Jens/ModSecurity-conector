/* Post-return elapsed budget, not a hard deadline or engine interruption. */
#ifndef NGX_HTTP_MODSECURITY_ENGINE_CALL_BUDGET_H
#define NGX_HTTP_MODSECURITY_ENGINE_CALL_BUDGET_H

#include <stdint.h>
#include <time.h>

typedef struct {
    uint64_t start_ns;
    uint64_t elapsed_ns;
    uint64_t budget_ns;
    int enabled;
    int valid;
} ngx_http_modsecurity_engine_call_budget;

static inline int
ngx_http_modsecurity_engine_budget_timestamp(const struct timespec *value,
    uint64_t *result)
{
    uint64_t seconds;
    if (value == NULL || result == NULL || value->tv_sec < 0 ||
        value->tv_nsec < 0 || value->tv_nsec >= 1000000000L) {
        return 0;
    }
    seconds = (uint64_t)value->tv_sec;
    if (seconds > (UINT64_MAX - (uint64_t)value->tv_nsec) / UINT64_C(1000000000)) {
        return 0;
    }
    *result = seconds * UINT64_C(1000000000) + (uint64_t)value->tv_nsec;
    return 1;
}

/* 0 disabled, 1 measured, -1 invalid. Caller supplies CLOCK_MONOTONIC. */
static inline int
ngx_http_modsecurity_engine_budget_begin(ngx_http_modsecurity_engine_call_budget *value,
    uint64_t budget_ms, const struct timespec *start)
{
    if (value == NULL) {
        return -1;
    }
    value->start_ns = 0;
    value->elapsed_ns = 0;
    value->budget_ns = 0;
    value->enabled = budget_ms != 0;
    value->valid = 0;
    if (!value->enabled) {
        value->valid = 1;
        return 0;
    }
    if (budget_ms > UINT64_MAX / UINT64_C(1000000) ||
        !ngx_http_modsecurity_engine_budget_timestamp(start, &value->start_ns)) {
        return -1;
    }
    value->budget_ns = budget_ms * UINT64_C(1000000);
    value->valid = 1;
    return 1;
}

/* 2 over budget, 1 at/below budget, 0 disabled, -1 invalid clock. */
static inline int
ngx_http_modsecurity_engine_budget_finish(ngx_http_modsecurity_engine_call_budget *value,
    const struct timespec *end)
{
    uint64_t end_ns;
    if (value == NULL || !value->valid) {
        return -1;
    }
    if (!value->enabled) {
        return 0;
    }
    if (!ngx_http_modsecurity_engine_budget_timestamp(end, &end_ns) ||
        end_ns < value->start_ns) {
        return -1;
    }
    value->elapsed_ns = end_ns - value->start_ns;
    return value->elapsed_ns > value->budget_ns ? 2 : 1;
}

#endif
