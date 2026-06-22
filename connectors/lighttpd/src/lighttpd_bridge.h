#ifndef MSCONNECTOR_LIGHTTPD_BRIDGE_H
#define MSCONNECTOR_LIGHTTPD_BRIDGE_H

#include "msconnector/capabilities.h"
#include "msconnector/intervention.h"
#include "msconnector/request.h"
#include "msconnector/status.h"
#include "msconnector/transaction.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef msconnector_decision msconnector_lighttpd_bridge_decision;

const char *msconnector_lighttpd_bridge_starter_kind(void);
msconnector_capabilities msconnector_lighttpd_bridge_starter_capabilities(void);
msconnector_request msconnector_lighttpd_bridge_make_probe_request(
    const char *method,
    const char *uri);
msconnector_lighttpd_bridge_decision msconnector_lighttpd_bridge_evaluate_probe(
    const msconnector_request *request);
enum msconnector_status msconnector_lighttpd_bridge_self_test(void);

#ifdef __cplusplus
}
#endif

#endif
