#ifndef MSCONNECTOR_NGINX_DDEBUG_H
#define MSCONNECTOR_NGINX_DDEBUG_H

#include <ngx_core.h>

#ifndef MODSECURITY_SANITY_CHECKS
#define MODSECURITY_SANITY_CHECKS 0
#endif

#if defined(MODSECURITY_DDEBUG) && (MODSECURITY_DDEBUG)

#if (NGX_HAVE_VARIADIC_MACROS)
#include <stdio.h>
#define dd(...) do { \
    fprintf(stderr, "modsec *** %s: ", __func__); \
    fprintf(stderr, __VA_ARGS__); \
    fprintf(stderr, " at %s line %d.\n", __FILE__, __LINE__); \
} while (0)
#else
#include <stdarg.h>
static void dd(const char *fmt, ...) {
    (void)fmt;
}
#endif

#define dd_check_read_event_handler(r) do { \
    dd("r->read_event_handler = %s", \
        (r)->read_event_handler == ngx_http_block_reading ? \
            "ngx_http_block_reading" : \
        (r)->read_event_handler == ngx_http_test_reading ? \
            "ngx_http_test_reading" : \
        (r)->read_event_handler == ngx_http_request_empty_handler ? \
            "ngx_http_request_empty_handler" : "UNKNOWN"); \
} while (0)

#define dd_check_write_event_handler(r) do { \
    dd("r->write_event_handler = %s", \
        (r)->write_event_handler == ngx_http_handler ? \
            "ngx_http_handler" : \
        (r)->write_event_handler == ngx_http_core_run_phases ? \
            "ngx_http_core_run_phases" : \
        (r)->write_event_handler == ngx_http_request_empty_handler ? \
            "ngx_http_request_empty_handler" : "UNKNOWN"); \
} while (0)

#else

#if (NGX_HAVE_VARIADIC_MACROS)
#define dd(...)
#else
static void dd(const char *fmt, ...) {
    (void)fmt;
}
#endif

#define dd_check_read_event_handler(r) do { (void)(r); } while (0)
#define dd_check_write_event_handler(r) do { (void)(r); } while (0)

#endif

#endif
