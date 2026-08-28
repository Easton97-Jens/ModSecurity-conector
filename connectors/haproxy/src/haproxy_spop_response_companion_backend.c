#include "haproxy_spop_response_companion_backend.h"

#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <sys/random.h>

#define HAPROXY_SPOP_RESPONSE_COMPANION_HANDLE_ATTEMPTS 4U

typedef struct haproxy_spop_response_companion_session_token {
  haproxy_spop_response_companion_backend *backend;
  haproxy_spop_response_companion_slot *slot;
  uint64_t lease;
} haproxy_spop_response_companion_session_token;

typedef struct haproxy_spop_response_companion_slot_generation {
  haproxy_spop_response_companion_slot *slot;
  haproxy_modsecurity_transaction *transaction;
  uint64_t lease;
  void *session_token;
} haproxy_spop_response_companion_slot_generation;

typedef struct haproxy_spop_response_companion_invoke_request {
  const haproxy_spop_response_companion_owner_command *command;
  msconnector_decision *decision;
  msconnector_error *error;
  int *transaction_consumed;
  const haproxy_spop_response_companion_slot_generation *expected_generation;
} haproxy_spop_response_companion_invoke_request;

static void set_error(msconnector_error *error, msconnector_error_code code,
                      const char *message) {
  if (error != NULL) {
    msconnector_error_set(error, code, message,
                          "haproxy_spop_response_companion_backend");
  }
}

static int valid_handle(const char *handle) {
  if (handle == NULL ||
      strlen(handle) != HAPROXY_SPOP_RESPONSE_COMPANION_HANDLE_SIZE) {
    return 0;
  }
  for (size_t i = 0; i < HAPROXY_SPOP_RESPONSE_COMPANION_HANDLE_SIZE; ++i) {
    const char c = handle[i];
    if (!((c >= '0' && c <= '9') || (c >= 'a' && c <= 'f'))) {
      return 0;
    }
  }
  return 1;
}

static int operation_is_terminal(
    haproxy_spop_response_companion_owner_operation operation) {
  return operation == HAPROXY_SPOP_RESPONSE_COMPANION_CANCEL ||
         operation == HAPROXY_SPOP_RESPONSE_COMPANION_RELEASE ||
         operation == HAPROXY_SPOP_RESPONSE_COMPANION_FAIL;
}

static int
make_handle(char output[HAPROXY_SPOP_RESPONSE_COMPANION_HANDLE_STORAGE]) {
  unsigned char random_bytes[HAPROXY_SPOP_RESPONSE_COMPANION_HANDLE_SIZE / 2U];
  size_t offset = 0U;
  while (offset < sizeof(random_bytes)) {
    const ssize_t result = getrandom(
        random_bytes + offset, sizeof(random_bytes) - offset, GRND_NONBLOCK);
    if (result > 0) {
      offset += (size_t)result;
      continue;
    }
    if (result < 0 && errno == EINTR) {
      continue;
    }
    return 0;
  }
  for (size_t i = 0; i < sizeof(random_bytes); ++i) {
    output[i * 2U] = "0123456789abcdef"[random_bytes[i] >> 4U];
    output[(i * 2U) + 1U] = "0123456789abcdef"[random_bytes[i] & 0x0fU];
  }
  output[HAPROXY_SPOP_RESPONSE_COMPANION_HANDLE_SIZE] = '\0';
  return 1;
}

static haproxy_spop_response_companion_slot *
find_slot(haproxy_spop_response_companion_backend *backend,
          const char *handle) {
  for (size_t i = 0; i < backend->capacity; ++i) {
    if (backend->slots[i].in_use &&
        strcmp(backend->slots[i].handle, handle) == 0) {
      return &backend->slots[i];
    }
  }
  return NULL;
}

/* Caller must hold backend->lock.  Keeping the token lookup and dereference
 * under the same lock as detach/free prevents a stale session opaque value
 * from racing terminal cleanup. */
static haproxy_spop_response_companion_slot *
session_slot_locked(haproxy_spop_response_companion_backend *backend,
                    const msconnector_response_companion_backend_session *session,
                    uint64_t *lease) {
  if (lease != NULL) {
    *lease = 0U;
  }
  if (backend == NULL || session == NULL || session->opaque == NULL) {
    return NULL;
  }
  /* Do not dereference an untrusted opaque value.  A token is valid only
   * while it is registered on one of this backend's bounded slots. */
  for (size_t i = 0U; i < backend->capacity; ++i) {
    haproxy_spop_response_companion_slot *slot = &backend->slots[i];
    if (slot->session_token == session->opaque) {
      const haproxy_spop_response_companion_session_token *token =
          (const haproxy_spop_response_companion_session_token *)
              session->opaque;
      if (token->backend != backend || token->slot != slot ||
          token->lease == 0U || token->lease != slot->lease) {
        return NULL;
      }
      if (lease != NULL) {
        *lease = token->lease;
      }
      return slot;
    }
  }
  return NULL;
}

static int slot_is_owned(const haproxy_spop_response_companion_backend *backend,
                         const haproxy_spop_response_companion_slot *slot) {
  uintptr_t first;
  uintptr_t last;
  uintptr_t address;
  uintptr_t span;
  if (backend == NULL || slot == NULL || backend->slots == NULL ||
      backend->capacity == 0U ||
      backend->capacity > (UINTPTR_MAX / sizeof(*backend->slots))) {
    return 0;
  }
  first = (uintptr_t)backend->slots;
  span = backend->capacity * sizeof(*backend->slots);
  if (span > UINTPTR_MAX - first) {
    return 0;
  }
  last = first + span;
  address = (uintptr_t)slot;
  return address >= first && address < last &&
         ((address - first) % sizeof(*backend->slots)) == 0U;
}

static int
dispatch_slot(haproxy_spop_response_companion_backend *backend,
              haproxy_spop_response_companion_slot *slot,
              const haproxy_spop_response_companion_owner_command *command,
              msconnector_decision *decision, msconnector_error *error,
              int *transaction_consumed) {
  if (backend == NULL || !slot_is_owned(backend, slot) || !slot->in_use ||
      slot->transaction == NULL || backend->dispatch == NULL ||
      command == NULL || command->lease == 0U ||
      command->lease != slot->lease) {
    set_error(error, MSCONNECTOR_ERROR_CORRELATION_MISSING,
              "SPOP response companion handle lease is not active");
    return 0;
  }
  /* invoke_common/expire mark in_flight while holding backend->lock before
   * reaching here. The owner dispatch is synchronous, so no callback may
   * reclaim this slot until it returns. */
  return backend->dispatch(backend->dispatch_context, slot->transaction,
                           command, decision, error, transaction_consumed);
}

static void clear_slot_locked(haproxy_spop_response_companion_slot *slot) {
  if (slot == NULL) {
    return;
  }
  slot->in_use = 0;
  slot->claimed = 0;
  slot->in_flight = 0;
  slot->in_flight_operation = HAPROXY_SPOP_RESPONSE_COMPANION_CLAIM;
  slot->expire_pending = 0;
  slot->terminal_pending = 0;
  slot->terminal_operation = HAPROXY_SPOP_RESPONSE_COMPANION_CLAIM;
  slot->terminal_timed_out = 0;
  slot->terminal_finished = 0;
  slot->terminal_consumed = 0;
  slot->transaction = NULL;
  slot->lease = 0U;
  slot->handle[0] = '\0';
}

static void *
detach_session_token_locked(haproxy_spop_response_companion_slot *slot) {
  void *token;
  if (slot == NULL) {
    return NULL;
  }
  token = slot->session_token;
  slot->session_token = NULL;
  return token;
}

static int
clear_slot_if_match_locked(haproxy_spop_response_companion_slot *slot,
                           const haproxy_modsecurity_transaction *transaction,
                           uint64_t lease, void **detached_token) {
  int matched = 0;
  if (slot == NULL || !slot->in_use || slot->transaction != transaction ||
      slot->lease != lease || lease == 0U) {
    matched = 0;
  } else {
    if (detached_token != NULL) {
      *detached_token = detach_session_token_locked(slot);
    }
    clear_slot_locked(slot);
    matched = 1;
  }
  return matched;
}

/* Capture the generation while the backend lock still protects both the
 * session token and its slot.  Terminal callers pass this expectation back
 * to invoke_common(), so expiry/finalizer reuse between the two lock turns
 * cannot redirect an old callback to a replacement lease. */
static int capture_slot_generation_locked(
    haproxy_spop_response_companion_backend *backend,
    const msconnector_response_companion_backend_session *session,
    haproxy_spop_response_companion_slot_generation *generation) {
  haproxy_spop_response_companion_slot *slot;
  uint64_t lease = 0U;

  if (generation == NULL) {
    return 0;
  }
  memset(generation, 0, sizeof(*generation));
  slot = session_slot_locked(backend, session, &lease);
  if (slot == NULL || !slot_is_owned(backend, slot) || !slot->in_use ||
      !slot->claimed || lease == 0U || slot->transaction == NULL ||
      slot->lease != lease || slot->session_token != session->opaque) {
    return 0;
  }
  generation->slot = slot;
  generation->transaction = slot->transaction;
  generation->lease = lease;
  generation->session_token = slot->session_token;
  return 1;
}

static int claim(void *context, const char *handle,
                 msconnector_response_companion_backend_session *session,
                 msconnector_error *error) {
  haproxy_spop_response_companion_backend *backend = context;
  haproxy_spop_response_companion_slot *slot;
  haproxy_spop_response_companion_owner_command command;
  msconnector_decision decision;
  haproxy_spop_response_companion_session_token *token = NULL;
  uint64_t lease = 0U;
  const haproxy_modsecurity_transaction *claim_transaction = NULL;
  int transaction_consumed = 0;
  int result;
  int generation_matches;
  if (backend == NULL || session == NULL || !valid_handle(handle)) {
    set_error(error, MSCONNECTOR_ERROR_PROTOCOL,
              "invalid SPOP companion handle");
    return 0;
  }
  pthread_mutex_lock(&backend->lock);
  slot = find_slot(backend, handle);
  if (slot == NULL || slot->claimed || slot->in_flight) {
    pthread_mutex_unlock(&backend->lock);
    set_error(error, MSCONNECTOR_ERROR_CORRELATION_MISMATCH,
              "SPOP companion handle is missing or already claimed");
    return 0;
  }
  if (slot->expire_pending) {
    pthread_mutex_unlock(&backend->lock);
    set_error(error, MSCONNECTOR_ERROR_CORRELATION_EXPIRED,
              "SPOP companion handle expired before claim");
    return 0;
  }
  lease = slot->lease;
  claim_transaction = slot->transaction;
  token = calloc(1U, sizeof(*token));
  if (token == NULL) {
    pthread_mutex_unlock(&backend->lock);
    set_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
              "SPOP companion session allocation failed");
    return 0;
  }
  token->backend = backend;
  token->slot = slot;
  token->lease = lease;
  slot->claimed = 1;
  slot->in_flight = 1;
  slot->in_flight_operation = HAPROXY_SPOP_RESPONSE_COMPANION_CLAIM;
  slot->session_token = token;
  session->opaque = token;
  pthread_mutex_unlock(&backend->lock);
  memset(&command, 0, sizeof(command));
  command.operation = HAPROXY_SPOP_RESPONSE_COMPANION_CLAIM;
  command.lease = lease;
  msconnector_decision_init(&decision);
  result = dispatch_slot(backend, slot, &command, &decision, error,
                         &transaction_consumed);
  pthread_mutex_lock(&backend->lock);
  /* The transaction pointer is stable for this claim.  Capture the
   * generation before dispatch and require the exact slot identity on the
   * return path; an expire/finalizer may have freed and reused this slot
   * while the owner callback was running. */
  generation_matches = slot->in_use && slot->transaction == claim_transaction &&
                       slot->lease == lease && slot->session_token == token;
  if (!generation_matches) {
    pthread_mutex_unlock(&backend->lock);
    session->opaque = NULL;
    set_error(error, MSCONNECTOR_ERROR_CORRELATION_MISMATCH,
              "SPOP companion claim lease expired during owner dispatch");
    return 0;
  }
  if (slot->expire_pending) {
    /* Expiry won while the owner claim was running.  The owner finalizer
     * owns the token, native abort, and slot deletion; retain its
     * quarantine rather than clearing this generation locally. */
    pthread_mutex_unlock(&backend->lock);
    session->opaque = NULL;
    set_error(error, MSCONNECTOR_ERROR_CORRELATION_EXPIRED,
              "SPOP companion claim expired during owner dispatch");
    return 0;
  }
  if (!result && error != NULL && error->code == MSCONNECTOR_ERROR_TIMEOUT) {
    /* The owner task is still running; retain the quarantine bit and
     * prevent fail/expire/release from touching the native transaction. */
  } else {
    slot->in_flight = 0;
  }
  if (!result && (error == NULL || error->code != MSCONNECTOR_ERROR_TIMEOUT)) {
    void *detached = NULL;
    (void)clear_slot_if_match_locked(slot, slot->transaction, lease, &detached);
    session->opaque = NULL;
    free(detached);
  }
  pthread_mutex_unlock(&backend->lock);
  return result;
}

typedef struct haproxy_spop_response_companion_invoke_state {
  haproxy_spop_response_companion_backend *backend;
  msconnector_response_companion_backend_session *session;
  const haproxy_spop_response_companion_owner_command *command;
  msconnector_decision *decision;
  msconnector_error *error;
  int *transaction_consumed;
  haproxy_spop_response_companion_slot *slot;
  const haproxy_modsecurity_transaction *transaction;
  const void *session_token;
  uint64_t lease;
  int terminal_operation;
} haproxy_spop_response_companion_invoke_state;

static int prepare_invoke(
    haproxy_spop_response_companion_invoke_state *state,
    haproxy_spop_response_companion_backend *backend,
    msconnector_response_companion_backend_session *session,
    const haproxy_spop_response_companion_invoke_request *request) {
  const haproxy_spop_response_companion_slot_generation *expected;
  if (backend == NULL || session == NULL || request == NULL ||
      request->command == NULL || request->decision == NULL) {
    set_error(request == NULL ? NULL : request->error,
              MSCONNECTOR_ERROR_CORRELATION_MISSING,
              "SPOP companion session is missing");
    return 0;
  }
  memset(state, 0, sizeof(*state));
  state->backend = backend;
  state->session = session;
  state->command = request->command;
  state->decision = request->decision;
  state->error = request->error;
  state->transaction_consumed = request->transaction_consumed;
  state->terminal_operation = operation_is_terminal(state->command->operation);
  expected = request->expected_generation;
  pthread_mutex_lock(&backend->lock);
  state->slot = session_slot_locked(backend, session, &state->lease);
  if (expected != NULL &&
      (state->slot == NULL || state->slot != expected->slot ||
       !slot_is_owned(backend, state->slot) || !state->slot->in_use ||
       state->slot->transaction != expected->transaction ||
       state->slot->lease != expected->lease ||
       state->slot->session_token != expected->session_token ||
       session->opaque != expected->session_token)) {
    pthread_mutex_unlock(&backend->lock);
    session->opaque = NULL;
    set_error(state->error, MSCONNECTOR_ERROR_CORRELATION_EXPIRED,
              "SPOP companion session generation changed before owner dispatch");
    return 0;
  }
  if (state->slot == NULL || !slot_is_owned(backend, state->slot) ||
      state->lease == 0U || !state->slot->in_use || !state->slot->claimed ||
      state->slot->lease != state->lease ||
      state->slot->session_token != session->opaque) {
    pthread_mutex_unlock(&backend->lock);
    set_error(state->error, MSCONNECTOR_ERROR_CORRELATION_MISSING,
              "SPOP companion session is not dispatchable");
    return 0;
  }
  if (state->slot->in_flight || state->slot->terminal_pending) {
    pthread_mutex_unlock(&backend->lock);
    set_error(state->error, MSCONNECTOR_ERROR_PHASE_SEQUENCE,
              "SPOP companion session callback is still active");
    return 0;
  }
  if (state->slot->expire_pending) {
    pthread_mutex_unlock(&backend->lock);
    set_error(state->error, MSCONNECTOR_ERROR_CORRELATION_EXPIRED,
              "SPOP companion session expired before owner dispatch");
    return 0;
  }
  state->transaction = state->slot->transaction;
  state->session_token = state->slot->session_token;
  state->slot->in_flight = 1;
  state->slot->in_flight_operation = state->command->operation;
  if (state->terminal_operation) {
    state->slot->terminal_pending = 1;
    state->slot->terminal_operation = state->command->operation;
    state->slot->terminal_timed_out = 0;
    state->slot->terminal_finished = 0;
    state->slot->terminal_consumed = 0;
  }
  pthread_mutex_unlock(&backend->lock);
  return 1;
}

static int
invoke_common(void *context,
              msconnector_response_companion_backend_session *session,
              const haproxy_spop_response_companion_invoke_request *request) {
  haproxy_spop_response_companion_invoke_state state;
  haproxy_spop_response_companion_owner_command owned_command;
  void *detached = NULL;
  haproxy_modsecurity_transaction *abort_transaction = NULL;
  int abort_required = 0;
  int result;
  if (!prepare_invoke(&state, context, session, request)) {
    return 0;
  }
  owned_command = *state.command;
  owned_command.lease = state.lease;
  result = dispatch_slot(state.backend, state.slot, &owned_command,
                         state.decision, state.error, state.transaction_consumed);
  pthread_mutex_lock(&state.backend->lock);
  if (!state.slot->in_use || state.slot->transaction != state.transaction ||
      state.slot->lease != state.lease ||
      state.slot->session_token != state.session_token ||
      state.session->opaque != state.session_token) {
    pthread_mutex_unlock(&state.backend->lock);
    state.session->opaque = NULL;
    set_error(state.error, MSCONNECTOR_ERROR_CORRELATION_EXPIRED,
              "SPOP companion session expired during owner dispatch");
    return 0;
  }
  if (state.slot->expire_pending) {
    pthread_mutex_unlock(&state.backend->lock);
    state.session->opaque = NULL;
    set_error(state.error, MSCONNECTOR_ERROR_CORRELATION_EXPIRED,
              "SPOP companion session expired during owner dispatch");
    return 0;
  }
  if (state.terminal_operation && !result && state.error != NULL &&
      state.error->code == MSCONNECTOR_ERROR_TIMEOUT) {
    state.slot->terminal_timed_out = 1;
    state.session->opaque = NULL;
    if (state.slot->terminal_finished) {
      abort_transaction = state.slot->transaction;
      abort_required = !state.slot->terminal_consumed;
      detached = detach_session_token_locked(state.slot);
      clear_slot_locked(state.slot);
    }
    pthread_mutex_unlock(&state.backend->lock);
    free(detached);
    if (abort_required) {
      haproxy_modsecurity_transaction_abort(abort_transaction);
    }
    return 0;
  }
  if (state.terminal_operation && !result &&
      (state.transaction_consumed == NULL || *state.transaction_consumed == 0)) {
    state.slot->terminal_pending = 0;
    state.slot->in_flight = 0;
  } else if (!state.terminal_operation &&
             (result || state.error == NULL ||
              state.error->code != MSCONNECTOR_ERROR_TIMEOUT)) {
    state.slot->in_flight = 0;
  }
  pthread_mutex_unlock(&state.backend->lock);
  return result;
}

/* The transport callbacks expose the claimed session as read-only.  Dispatch
 * uses a private capability copy because failed non-terminal callbacks are
 * rejected by the slot generation checks and must not mutate caller memory. */
static int invoke_readonly(
    void *context,
    const msconnector_response_companion_backend_session *session,
    const haproxy_spop_response_companion_invoke_request *request) {
  msconnector_response_companion_backend_session session_copy;
  session_copy = *session;
  return invoke_common(context, &session_copy, request);
}

static int headers(void *context,
                   const msconnector_response_companion_backend_session *session,
                   const msconnector_response *response,
                   msconnector_decision *decision, msconnector_error *error) {
  haproxy_spop_response_companion_owner_command command;
  haproxy_spop_response_companion_invoke_request request;
  if (session == NULL || session->decision_storage == NULL) {
    set_error(error, MSCONNECTOR_ERROR_CORRELATION_MISSING,
              "SPOP response companion decision storage is missing");
    return 0;
  }
  memset(&command, 0, sizeof(command));
  command.operation = HAPROXY_SPOP_RESPONSE_COMPANION_RESPONSE_HEADERS;
  command.response = response;
  command.decision_storage = session->decision_storage;
  request = (haproxy_spop_response_companion_invoke_request){&command, decision,
                                                             error, NULL, NULL};
  return invoke_readonly(context, session, &request);
}
static int body(void *context,
                const msconnector_response_companion_backend_session *session,
                const unsigned char *data, size_t size,
                msconnector_error *error) {
  haproxy_spop_response_companion_owner_command command;
  msconnector_decision decision;
  haproxy_spop_response_companion_invoke_request request;
  if (session == NULL || session->decision_storage == NULL) {
    set_error(error, MSCONNECTOR_ERROR_CORRELATION_MISSING,
              "SPOP response companion decision storage is missing");
    return 0;
  }
  memset(&command, 0, sizeof(command));
  command.operation = HAPROXY_SPOP_RESPONSE_COMPANION_RESPONSE_BODY;
  command.body = data;
  command.body_size = size;
  command.decision_storage = session->decision_storage;
  msconnector_decision_init(&decision);
  request = (haproxy_spop_response_companion_invoke_request){
      &command, &decision, error, NULL, NULL};
  return invoke_readonly(context, session, &request);
}
static int eos(void *context,
               const msconnector_response_companion_backend_session *session,
               msconnector_decision *decision, msconnector_error *error) {
  haproxy_spop_response_companion_owner_command command;
  haproxy_spop_response_companion_invoke_request request;
  if (session == NULL || session->decision_storage == NULL) {
    set_error(error, MSCONNECTOR_ERROR_CORRELATION_MISSING,
              "SPOP response companion decision storage is missing");
    return 0;
  }
  memset(&command, 0, sizeof(command));
  command.operation = HAPROXY_SPOP_RESPONSE_COMPANION_RESPONSE_EOS;
  command.decision_storage = session->decision_storage;
  request = (haproxy_spop_response_companion_invoke_request){&command, decision,
                                                             error, NULL, NULL};
  return invoke_readonly(context, session, &request);
}
static int commit(void *context,
                  msconnector_response_companion_backend_session *session,
                  int headers_sent, int body_started,
                  msconnector_error *error) {
  haproxy_spop_response_companion_owner_command command;
  msconnector_decision decision;
  haproxy_spop_response_companion_invoke_request request;
  memset(&command, 0, sizeof(command));
  command.operation = HAPROXY_SPOP_RESPONSE_COMPANION_COMMIT;
  command.headers_sent = headers_sent;
  command.body_started = body_started;
  msconnector_decision_init(&decision);
  request = (haproxy_spop_response_companion_invoke_request){
      &command, &decision, error, NULL, NULL};
  return invoke_common(context, session, &request);
}
static int outcome(void *context,
                   const msconnector_response_companion_backend_session *session,
                   const msconnector_response_companion_host_action *action,
                   msconnector_error *error) {
  haproxy_spop_response_companion_owner_command command;
  msconnector_decision ignored;
  haproxy_spop_response_companion_invoke_request request;
  memset(&command, 0, sizeof(command));
  command.operation = HAPROXY_SPOP_RESPONSE_COMPANION_OUTCOME;
  command.decision = action->decision;
  command.action = action->actual_action;
  command.visible_http_status = action->visible_http_status;
  command.transport_result = action->transport_result;
  command.connection_aborted = action->connection_aborted;
  msconnector_decision_init(&ignored);
  request = (haproxy_spop_response_companion_invoke_request){&command, &ignored,
                                                             error, NULL, NULL};
  return invoke_readonly(context, session, &request);
}
static int terminal(void *context,
                    msconnector_response_companion_backend_session *session,
                    int upstream_disconnect, int release,
                    msconnector_error *error) {
  haproxy_spop_response_companion_owner_command command;
  msconnector_decision decision;
  haproxy_spop_response_companion_backend *backend = context;
  haproxy_spop_response_companion_slot_generation generation;
  void *detached = NULL;
  haproxy_modsecurity_transaction *abort_transaction = NULL;
  int abort_required = 0;
  int transaction_consumed = 0;
  haproxy_spop_response_companion_invoke_request request;
  if (backend == NULL) {
    set_error(error, MSCONNECTOR_ERROR_CORRELATION_MISSING,
              "SPOP companion backend is missing");
    return 0;
  }
  pthread_mutex_lock(&backend->lock);
  if (!capture_slot_generation_locked(backend, session, &generation)) {
    pthread_mutex_unlock(&backend->lock);
    set_error(error, MSCONNECTOR_ERROR_CORRELATION_MISSING,
              "SPOP companion session generation is missing");
    return 0;
  }
  pthread_mutex_unlock(&backend->lock);
  memset(&command, 0, sizeof(command));
  command.operation = release ? HAPROXY_SPOP_RESPONSE_COMPANION_RELEASE
                              : HAPROXY_SPOP_RESPONSE_COMPANION_CANCEL;
  command.connection_aborted = upstream_disconnect;
  msconnector_decision_init(&decision);
  request = (haproxy_spop_response_companion_invoke_request){
      &command, &decision, error, &transaction_consumed, &generation};
  if (!invoke_common(backend, session, &request)) {
    pthread_mutex_lock(&backend->lock);
    if (generation.slot != NULL && slot_is_owned(backend, generation.slot) &&
        generation.slot->in_use &&
        generation.slot->transaction == generation.transaction &&
        generation.slot->lease == generation.lease &&
        generation.slot->session_token == generation.session_token &&
        (transaction_consumed || generation.slot->terminal_finished)) {
      abort_transaction = generation.slot->transaction;
      abort_required =
          !transaction_consumed && !generation.slot->terminal_consumed;
      (void)clear_slot_if_match_locked(generation.slot, generation.transaction,
                                       generation.lease, &detached);
    }
    pthread_mutex_unlock(&backend->lock);
    if (detached != NULL) {
      session->opaque = NULL;
    }
    free(detached);
    if (abort_required) {
      haproxy_modsecurity_transaction_abort(abort_transaction);
    }
    return 0;
  }
  pthread_mutex_lock(&backend->lock);
  if (generation.slot != NULL && slot_is_owned(backend, generation.slot)) {
    (void)clear_slot_if_match_locked(generation.slot, generation.transaction,
                                     generation.lease, &detached);
  }
  pthread_mutex_unlock(&backend->lock);
  session->opaque = NULL;
  free(detached);
  return 1;
}
static int cancel(void *context,
                  msconnector_response_companion_backend_session *session,
                  int disconnected, msconnector_error *error) {
  return terminal(context, session, disconnected, 0, error);
}

static int release(void *context,
                   msconnector_response_companion_backend_session *session,
                   msconnector_error *error) {
  return terminal(context, session, 0, 1, error);
}

static void expire_callback(void *context, uint64_t now_ms) {
  haproxy_spop_response_companion_backend_expire(
      (haproxy_spop_response_companion_backend *)context, now_ms);
}

static int set_commit(void *context,
                      const msconnector_response_companion_backend_session *session,
                      int headers_sent, int body_started,
                      msconnector_error *error) {
  msconnector_response_companion_backend_session session_copy = *session;
  return commit(context, &session_copy, headers_sent, body_started, error);
}

static int record(void *context,
                  const msconnector_response_companion_backend_session *session,
                  const msconnector_response_companion_host_action *action,
                  msconnector_error *error) {
  return outcome(context, session, action, error);
}
static void fail(void *context,
                 msconnector_response_companion_backend_session *session,
                 msconnector_transaction_error_class error_class) {
  haproxy_spop_response_companion_backend *backend = context;
  haproxy_spop_response_companion_slot_generation generation;
  haproxy_spop_response_companion_owner_command command;
  msconnector_decision decision;
  msconnector_error error;
  void *detached = NULL;
  haproxy_modsecurity_transaction *abort_transaction = NULL;
  int abort_required = 0;
  int transaction_consumed = 0;
  haproxy_spop_response_companion_invoke_request request;
  if (backend == NULL) {
    return;
  }
  pthread_mutex_lock(&backend->lock);
  if (!capture_slot_generation_locked(backend, session, &generation)) {
    pthread_mutex_unlock(&backend->lock);
    if (session != NULL) {
      session->opaque = NULL;
    }
    return;
  }
  pthread_mutex_unlock(&backend->lock);
  memset(&command, 0, sizeof(command));
  command.operation = HAPROXY_SPOP_RESPONSE_COMPANION_FAIL;
  command.error_class = error_class;
  msconnector_decision_init(&decision);
  msconnector_error_init(&error);
  request = (haproxy_spop_response_companion_invoke_request){
      &command, &decision, &error, &transaction_consumed, &generation};
  if (!invoke_common(backend, session, &request)) {
    /* Any non-dispatchable state is terminal-pending. In particular,
     * PHASE_SEQUENCE means an owner callback is still in flight; never
     * clear the native transaction until its finalizer reports return. */
    pthread_mutex_lock(&backend->lock);
    if (generation.slot != NULL && slot_is_owned(backend, generation.slot) &&
        generation.slot->in_use &&
        generation.slot->transaction == generation.transaction &&
        generation.slot->lease == generation.lease &&
        generation.slot->session_token == generation.session_token) {
      if (transaction_consumed || generation.slot->terminal_finished) {
        abort_transaction = generation.slot->transaction;
        abort_required =
            !transaction_consumed && !generation.slot->terminal_consumed;
        (void)clear_slot_if_match_locked(generation.slot,
                                         generation.transaction,
                                         generation.lease, &detached);
      } else {
        generation.slot->expire_pending = 1;
      }
    }
    pthread_mutex_unlock(&backend->lock);
    if (detached != NULL) {
      session->opaque = NULL;
    }
    free(detached);
    if (abort_required) {
      haproxy_modsecurity_transaction_abort(abort_transaction);
    }
    return;
  }
  pthread_mutex_lock(&backend->lock);
  (void)clear_slot_if_match_locked(generation.slot, generation.transaction,
                                   generation.lease, &detached);
  pthread_mutex_unlock(&backend->lock);
  free(detached);
  session->opaque = NULL;
}

int haproxy_spop_response_companion_backend_init(
    haproxy_spop_response_companion_backend *backend,
    haproxy_spop_response_companion_slot *slots, size_t capacity,
    uint64_t ttl_ms, void *dispatch_context,
    haproxy_spop_response_companion_owner_dispatch dispatch,
    msconnector_error *error) {
  if (backend == NULL || slots == NULL || capacity == 0 || ttl_ms == 0 ||
      dispatch == NULL) {
    set_error(error, MSCONNECTOR_ERROR_INVALID_CONFIG,
              "invalid SPOP companion backend configuration");
    return 0;
  }
  memset(backend, 0, sizeof(*backend));
  backend->slots = slots;
  backend->capacity = capacity;
  backend->ttl_ms = ttl_ms;
  backend->next_lease = 1U;
  backend->dispatch_context = dispatch_context;
  backend->dispatch = dispatch;
  if (pthread_mutex_init(&backend->lock, NULL) != 0) {
    set_error(error, MSCONNECTOR_ERROR_INTERNAL,
              "SPOP companion mutex initialization failed");
    return 0;
  }
  memset(slots, 0, capacity * sizeof(*slots));
  return 1;
}
int haproxy_spop_response_companion_backend_destroy(
    haproxy_spop_response_companion_backend *backend,
    msconnector_error *error) {
  if (backend == NULL || backend->slots == NULL) {
    set_error(error, MSCONNECTOR_ERROR_INVALID_CONFIG,
              "invalid SPOP companion backend destroy");
    return 0;
  }
  pthread_mutex_lock(&backend->lock);
  for (size_t i = 0; i < backend->capacity; ++i) {
    if (backend->slots[i].in_use || backend->slots[i].in_flight) {
      pthread_mutex_unlock(&backend->lock);
      set_error(error, MSCONNECTOR_ERROR_PHASE_SEQUENCE,
                "stop the response companion transport before destroy");
      return 0;
    }
  }
  pthread_mutex_unlock(&backend->lock);
  if (pthread_mutex_destroy(&backend->lock) != 0) {
    set_error(error, MSCONNECTOR_ERROR_INTERNAL,
              "SPOP companion mutex destroy failed");
    return 0;
  }
  return 1;
}
int haproxy_spop_response_companion_handoff(
    haproxy_spop_response_companion_backend *backend,
    haproxy_modsecurity_transaction *transaction, uint64_t now_ms,
    char handle[HAPROXY_SPOP_RESPONSE_COMPANION_HANDLE_STORAGE],
    msconnector_error *error) {
  size_t i;
  if (backend == NULL || transaction == NULL || handle == NULL) {
    set_error(error, MSCONNECTOR_ERROR_INVALID_CONFIG,
              "invalid SPOP companion handoff");
    return 0;
  }
  if (backend->ttl_ms > UINT64_MAX - now_ms) {
    set_error(error, MSCONNECTOR_ERROR_INVALID_CONFIG,
              "SPOP companion TTL overflows the monotonic deadline");
    return 0;
  }
  pthread_mutex_lock(&backend->lock);
  for (i = 0; i < backend->capacity; ++i) {
    if (!backend->slots[i].in_use) {
      break;
    }
  }
  if (i == backend->capacity) {
    pthread_mutex_unlock(&backend->lock);
    set_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
              "SPOP companion capacity exhausted");
    return 0;
  }
  if (backend->next_lease == 0U || backend->next_lease == UINT64_MAX) {
    pthread_mutex_unlock(&backend->lock);
    set_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
              "SPOP companion lease space exhausted");
    return 0;
  }
  {
    int unique = 0;
    for (unsigned int attempt = 0U;
         attempt < HAPROXY_SPOP_RESPONSE_COMPANION_HANDLE_ATTEMPTS; ++attempt) {
      if (!make_handle(backend->slots[i].handle)) {
        pthread_mutex_unlock(&backend->lock);
        set_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
                  "non-blocking operating-system randomness is unavailable");
        return 0;
      }
      if (find_slot(backend, backend->slots[i].handle) == NULL) {
        unique = 1;
        break;
      }
    }
    if (!unique) {
      pthread_mutex_unlock(&backend->lock);
      set_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
                "SPOP companion handle uniqueness budget exhausted");
      return 0;
    }
  }
  backend->slots[i].transaction = transaction;
  backend->slots[i].lease = backend->next_lease++;
  backend->slots[i].expires_at_ms = now_ms + backend->ttl_ms;
  backend->slots[i].in_use = 1;
  backend->slots[i].claimed = 0;
  backend->slots[i].in_flight = 0;
  backend->slots[i].in_flight_operation = HAPROXY_SPOP_RESPONSE_COMPANION_CLAIM;
  backend->slots[i].expire_pending = 0;
  backend->slots[i].terminal_pending = 0;
  backend->slots[i].terminal_operation = HAPROXY_SPOP_RESPONSE_COMPANION_CLAIM;
  backend->slots[i].terminal_timed_out = 0;
  backend->slots[i].terminal_finished = 0;
  backend->slots[i].terminal_consumed = 0;
  memcpy(handle, backend->slots[i].handle, sizeof(backend->slots[i].handle));
  pthread_mutex_unlock(&backend->lock);
  return 1;
}
void haproxy_spop_response_companion_backend_vtable(
    haproxy_spop_response_companion_backend *backend,
    msconnector_response_companion_backend *vtable) {
  memset(vtable, 0, sizeof(*vtable));
  vtable->context = backend;
  vtable->allow_parallel_callbacks = 1;
  vtable->claim = claim;
  vtable->process_response_headers = headers;
  vtable->append_response_body_chunk = body;
  vtable->finish_response_body = eos;
  vtable->set_response_commit_state = set_commit;
  vtable->record_host_action = record;
  vtable->cancel = cancel;
  vtable->release = release;
  vtable->fail = fail;
  vtable->expire = expire_callback;
}
int haproxy_spop_response_companion_backend_dispatch_finished(
    haproxy_spop_response_companion_backend *backend,
    haproxy_modsecurity_transaction *transaction, uint64_t lease,
    haproxy_spop_response_companion_owner_operation operation,
    int transaction_consumed) {
  int pending = 0;
  int cleanup_required = 0;
  const haproxy_modsecurity_transaction *abort_transaction = NULL;
  if (backend == NULL || transaction == NULL || lease == 0U) {
    return 0;
  }
  pthread_mutex_lock(&backend->lock);
  for (size_t i = 0; i < backend->capacity; ++i) {
    haproxy_spop_response_companion_slot *slot = &backend->slots[i];
    if (slot->in_use && slot->transaction == transaction &&
        slot->lease == lease) {
      int terminal_finalizer;

      /* The owner queue can destroy a completed earlier task after a
       * later operation has begun.  Do not let that stale finalizer
       * clear, consume, or abort the current in-flight operation. */
      if (!slot->in_flight || slot->in_flight_operation != operation) {
        continue;
      }
      pending = slot->expire_pending;
      terminal_finalizer =
          slot->terminal_pending && slot->terminal_operation == operation;
      if (terminal_finalizer) {
        slot->terminal_finished = 1;
        slot->terminal_consumed = transaction_consumed != 0;
      }
      cleanup_required =
          pending || (terminal_finalizer && slot->terminal_timed_out);
      abort_transaction =
          cleanup_required && !transaction_consumed ? transaction : NULL;
      if (cleanup_required) {
        void *detached = detach_session_token_locked(slot);
        clear_slot_locked(slot);
        free(detached);
      } else if (!terminal_finalizer) {
        /* For normal callbacks the owner finalizer releases the
         * callback guard.  A terminal operation must retain it until
         * terminal()/fail() atomically deletes this generation. */
        slot->in_flight = 0;
      }
      break;
    }
  }
  pthread_mutex_unlock(&backend->lock);
  if (abort_transaction) {
    haproxy_modsecurity_transaction_abort(transaction);
  }
  return pending;
}
void haproxy_spop_response_companion_backend_expire(
    haproxy_spop_response_companion_backend *backend, uint64_t now_ms) {
  if (backend == NULL) {
    return;
  }
  for (size_t i = 0U; i < backend->capacity; ++i) {
    haproxy_spop_response_companion_slot *slot = &backend->slots[i];
    int result;
    int transaction_consumed = 0;
    uint64_t lease;
    const haproxy_modsecurity_transaction *transaction;
    haproxy_spop_response_companion_owner_command command;
    msconnector_decision decision;
    msconnector_error error;

    pthread_mutex_lock(&backend->lock);
    if (!slot->in_use || now_ms < slot->expires_at_ms) {
      pthread_mutex_unlock(&backend->lock);
      continue;
    }
    if (slot->in_flight) {
      slot->expire_pending = 1;
      pthread_mutex_unlock(&backend->lock);
      continue;
    }
    lease = slot->lease;
    transaction = slot->transaction;
    /* Mark expiry before owner dispatch.  Its finalizer can run before
     * this caller reacquires the lock; it must already see that expiry
     * owns cleanup for this exact transaction/lease generation. */
    slot->expire_pending = 1;
    slot->in_flight = 1;
    slot->in_flight_operation = HAPROXY_SPOP_RESPONSE_COMPANION_EXPIRE;
    pthread_mutex_unlock(&backend->lock);

    memset(&command, 0, sizeof(command));
    command.operation = HAPROXY_SPOP_RESPONSE_COMPANION_EXPIRE;
    command.lease = lease;
    command.error_class = MSCONNECTOR_TRANSACTION_ERROR_CORRELATION_EXPIRED;
    msconnector_decision_init(&decision);
    msconnector_error_init(&error);
    result = dispatch_slot(backend, slot, &command, &decision, &error,
                           &transaction_consumed);

    pthread_mutex_lock(&backend->lock);
    if (!slot->in_use || slot->transaction != transaction ||
        slot->lease != lease) {
      pthread_mutex_unlock(&backend->lock);
      continue;
    }
    if (result || transaction_consumed) {
      void *detached = detach_session_token_locked(slot);
      clear_slot_locked(slot);
      free(detached);
    } else {
      slot->expire_pending = 1;
      if (error.code != MSCONNECTOR_ERROR_TIMEOUT) {
        /* No owner task remains for a non-timeout failure.  Keep the
         * expired generation unavailable, but permit a later EXPIRE
         * retry to own its cleanup. */
        slot->in_flight = 0;
      }
    }
    pthread_mutex_unlock(&backend->lock);
  }
}
