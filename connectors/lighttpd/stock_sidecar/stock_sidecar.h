#ifndef MSCONNECTOR_STOCK_SIDECAR_H
#define MSCONNECTOR_STOCK_SIDECAR_H

/* Traffic-owning HTTP/1.1 reverse proxy used for the Stock-lighttpd route.
 * Sequential HTTP/1.1 reuse is bounded to 32 exchanges, each with independent
 * Common ownership and an absolute deadline; idle sockets share that timeout.
 * Explicit close, incomplete bodies and failed cleanup close the connection.
 * Follow-up bytes visible before final response headers force close; bytes
 * arriving later are parsed as a fresh exchange after the prior cleanup.
 * HTTP/1.0 and unsupported framing remain rejected. */
int msconnector_stock_sidecar_main(int argc, char **argv);

#endif
