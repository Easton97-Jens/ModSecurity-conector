#ifndef MSCONNECTOR_TRAEFIK_PROVENANCE_H
#define MSCONNECTOR_TRAEFIK_PROVENANCE_H

#include "common/runtime/http_authorization_service.h"

#define MSCONNECTOR_TRAEFIK_PROVENANCE_HEADER "X-Msconnector-Trusted-Reservation"

/* Opt-in, process-owned private reservation listener. The path must not
 * exist and must have a canonical, service-owned mode-0700 parent. */
int msconnector_traefik_provenance_start(const char *path);
typedef int (*msconnector_traefik_provenance_confirm)(void *userdata,
    const char *response_handle, msconnector_error *error);
/* Callback must only touch the Common registry and must not enter MTP1.
 * It runs under the reservation lock before an Allow handle is released. */
int msconnector_traefik_provenance_start_with_confirmation(const char *path,
    msconnector_traefik_provenance_confirm confirm, void *userdata);
void msconnector_traefik_provenance_stop(void);
int msconnector_traefik_provenance_claim(void *unused,
    const msconnector_request *request,
    msconnector_http_authorization_provenance_storage *storage,
    msconnector_error *error);
int msconnector_traefik_provenance_complete(void *unused,
    const msconnector_request *request, int status, const char *response_handle,
    msconnector_error *error);

#endif
