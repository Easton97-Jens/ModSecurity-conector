#ifndef MSCONNECTOR_PHASE_H
#define MSCONNECTOR_PHASE_H

#ifdef __cplusplus
extern "C" {
#endif

/*
 * Connector-neutral transaction processing phases.
 *
 * This small header exists so decision and transaction declarations can share
 * the phase enum without creating include-order cycles.
 */
enum msconnector_phase {
    MSCONNECTOR_PHASE_CONNECTION = 0,
    MSCONNECTOR_PHASE_URI = 1,
    MSCONNECTOR_PHASE_REQUEST_HEADERS = 2,
    MSCONNECTOR_PHASE_REQUEST_BODY = 3,
    MSCONNECTOR_PHASE_RESPONSE_HEADERS = 4,
    MSCONNECTOR_PHASE_RESPONSE_BODY = 5,
    MSCONNECTOR_PHASE_LOGGING = 6
};

#ifdef __cplusplus
}
#endif

#endif
