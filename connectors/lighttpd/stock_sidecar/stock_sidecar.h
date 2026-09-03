#ifndef MSCONNECTOR_STOCK_SIDECAR_H
#define MSCONNECTOR_STOCK_SIDECAR_H

/* Traffic-owning HTTP/1.1 reverse proxy used for the Stock-lighttpd route.
 * The implementation intentionally closes the client connection after one
 * exchange; this makes transaction ownership and cleanup deterministic while
 * retaining a sequential, independently testable request path. */
int msconnector_stock_sidecar_main(int argc, char **argv);

#endif
