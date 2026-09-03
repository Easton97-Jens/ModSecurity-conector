#ifndef HAPROXY_SPOP_RESPONSE_COMPANION_BACKEND_H
#define HAPROXY_SPOP_RESPONSE_COMPANION_BACKEND_H

#include <pthread.h>
#include <stddef.h>
#include <stdint.h>

#include "../../../common/runtime/response_companion_transport.h"
#include "haproxy_modsecurity_binding.h"

#ifdef __cplusplus
extern "C" {
#endif

#define HAPROXY_SPOP_RESPONSE_COMPANION_HANDLE_SIZE 64U
#define HAPROXY_SPOP_RESPONSE_COMPANION_HANDLE_STORAGE                         \
  (HAPROXY_SPOP_RESPONSE_COMPANION_HANDLE_SIZE + 1U)

typedef enum haproxy_spop_response_companion_owner_operation {
  HAPROXY_SPOP_RESPONSE_COMPANION_CLAIM = 0,
  HAPROXY_SPOP_RESPONSE_COMPANION_RESPONSE_HEADERS,
  HAPROXY_SPOP_RESPONSE_COMPANION_RESPONSE_BODY,
  HAPROXY_SPOP_RESPONSE_COMPANION_RESPONSE_EOS,
  HAPROXY_SPOP_RESPONSE_COMPANION_COMMIT,
  HAPROXY_SPOP_RESPONSE_COMPANION_OUTCOME,
  HAPROXY_SPOP_RESPONSE_COMPANION_CANCEL,
  HAPROXY_SPOP_RESPONSE_COMPANION_RELEASE,
  HAPROXY_SPOP_RESPONSE_COMPANION_EXPIRE,
  HAPROXY_SPOP_RESPONSE_COMPANION_FAIL
} haproxy_spop_response_companion_owner_operation;

/* Borrowed transport-session storage. The owner task may write only while
 * synchronously returning a P3/P4 decision; MRC1 copies it before a later
 * callback, terminal release, or slot reuse can invalidate the session. */
typedef msconnector_response_companion_decision_storage
    haproxy_spop_response_companion_decision_storage;

typedef struct haproxy_spop_response_companion_owner_command {
  haproxy_spop_response_companion_owner_operation operation;
  /* A non-zero lease identifies this exact handoff.  It must accompany
   * every owner operation and is checked together with the transaction
   * pointer before any delayed finalizer may mutate a slot. */
  uint64_t lease;
  /* All pointer fields are borrowed for the duration of the synchronous
   * owner dispatch only; the dispatcher must not retain them. */
  const msconnector_response *response;
  const unsigned char *body;
  size_t body_size;
  const msconnector_decision *decision;
  const char *transport_result;
  haproxy_spop_response_companion_decision_storage *decision_storage;
  msconnector_decision_action action;
  int headers_sent;
  int body_started;
  int visible_http_status;
  int connection_aborted;
  msconnector_transaction_error_class error_class;
} haproxy_spop_response_companion_owner_command;

/* Dispatch is synchronous from the transport callback's point of view. The
 * implementation must marshal the command to HAProxy's owner thread before
 * dereferencing `transaction`; the MRC1 worker never does so itself. */
typedef int (*haproxy_spop_response_companion_owner_dispatch)(
    void *context, haproxy_modsecurity_transaction *transaction,
    const haproxy_spop_response_companion_owner_command *command,
    msconnector_decision *decision, msconnector_error *error,
    int *transaction_consumed);

typedef struct haproxy_spop_response_companion_slot {
  haproxy_modsecurity_transaction *transaction;
  uint64_t lease;
  char handle[HAPROXY_SPOP_RESPONSE_COMPANION_HANDLE_STORAGE];
  uint64_t expires_at_ms;
  int in_use;
  int claimed;
  int in_flight;
  /* An owner finalizer is authoritative only for this currently dispatched
   * operation.  Lease alone cannot distinguish a delayed prior callback
   * from a later terminal operation on the same transaction. */
  haproxy_spop_response_companion_owner_operation in_flight_operation;
  int expire_pending;
  /* A terminal owner operation consumed or is about to consume the native
   * transaction.  Keep in_flight set until its backend caller clears this
   * exact generation, so expiry cannot dispatch a second terminal action. */
  int terminal_pending;
  haproxy_spop_response_companion_owner_operation terminal_operation;
  /* A timed-out terminal caller has no later cleanup turn.  The owner
   * finalizer must then clear this exact generation itself. */
  int terminal_timed_out;
  /* The owner finalizer can run before the synchronous caller receives its
   * result.  Retain its completion/consumption fact for that caller. */
  int terminal_finished;
  int terminal_consumed;
  void *session_token;
} haproxy_spop_response_companion_slot;

typedef struct haproxy_spop_response_companion_backend {
  pthread_mutex_t lock;
  haproxy_spop_response_companion_slot *slots;
  size_t capacity;
  uint64_t ttl_ms;
  uint64_t next_lease;
  void *dispatch_context;
  haproxy_spop_response_companion_owner_dispatch dispatch;
} haproxy_spop_response_companion_backend;

int haproxy_spop_response_companion_backend_init(
    haproxy_spop_response_companion_backend *backend,
    haproxy_spop_response_companion_slot *slots, size_t capacity,
    uint64_t ttl_ms, void *dispatch_context,
    haproxy_spop_response_companion_owner_dispatch dispatch,
    msconnector_error *error);
/* The transport must be stopped first. Destroy fails closed while any slot is
 * active or an owner dispatch is in flight; the mutex remains initialized in
 * that case so the caller can finish cleanup and retry. */
int haproxy_spop_response_companion_backend_destroy(
    haproxy_spop_response_companion_backend *backend, msconnector_error *error);

/* Called by the SPOP owner after P2. The returned handle is the only value
 * that may cross into MRC1. A slot is single-claim and bounded by TTL. */
int haproxy_spop_response_companion_handoff(
    haproxy_spop_response_companion_backend *backend,
    haproxy_modsecurity_transaction *transaction, uint64_t now_ms,
    char handle[HAPROXY_SPOP_RESPONSE_COMPANION_HANDLE_STORAGE],
    msconnector_error *error);

/* Produces a transport backend vtable. The backend context remains owned by
 * the caller until the transport has stopped. */
void haproxy_spop_response_companion_backend_vtable(
    haproxy_spop_response_companion_backend *backend,
    msconnector_response_companion_backend *vtable);

/* May be called periodically by the owner or supplied as the transport's
 * expire callback. Expired entries are dispatched as EXPIRE and reclaimed. */
void haproxy_spop_response_companion_backend_expire(
    haproxy_spop_response_companion_backend *backend, uint64_t now_ms);
/* Called by the owner-task finalizer after a native callback has actually
 * returned.  It records terminal completion for a synchronous caller; if
 * TTL expiry or a terminal caller timeout already owns cleanup, it deletes
 * that exact transaction/lease/owner-operation generation and aborts only
 * when the owner did not consume the native transaction. */
int haproxy_spop_response_companion_backend_dispatch_finished(
    haproxy_spop_response_companion_backend *backend,
    haproxy_modsecurity_transaction *transaction, uint64_t lease,
    haproxy_spop_response_companion_owner_operation operation,
    int transaction_consumed);

#ifdef __cplusplus
}
#endif

#endif
