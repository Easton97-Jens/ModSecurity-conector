#ifndef MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_H
#define MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_H

#include <stddef.h>
#include <stdint.h>
#include <stdatomic.h>
#include <pthread.h>
#include <sys/types.h>

#include "msconnector/limits.h"
#include "msconnector_runtime.h"

#ifdef __cplusplus
extern "C" {
#endif

/* Private response-observer wire protocol. The frame carries only a
 * server-generated opaque capability at CLAIM; transaction and host IDs never
 * cross this boundary. All payloads are bounded before allocation. */
#define MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_SOCKET_SIZE 108U
#define MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_HANDLE_SIZE \
    MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_HANDLE_SIZE
#define MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_MAX_FRAME 65536U
#define MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_MAX_BODY_CHUNK 32768U
#define MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_DEFAULT_TIMEOUT_MS 5000U
/* The MRC1 magic identifies the private response-companion protocol family.
 * Version 2 adds typed terminal causes.  There is deliberately no v1
 * fallback: a mismatched observer/listener must fail closed instead of
 * silently collapsing an engine or protocol error into a disconnect. */
#define MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_PROTOCOL_VERSION 2U

/* Stable one-byte CANCEL payload values.  Values 0 and 1 preserve the prior
 * client-cancel/upstream-disconnect meanings; values 2--6 make a local
 * observer failure reach the canonical transaction contract without adding
 * identifiers or payloads to the private wire. */
typedef enum msconnector_response_companion_cancel_cause {
    MSCONNECTOR_RESPONSE_COMPANION_CANCEL_CLIENT_CANCEL = 0,
    MSCONNECTOR_RESPONSE_COMPANION_CANCEL_UPSTREAM_DISCONNECT = 1,
    MSCONNECTOR_RESPONSE_COMPANION_CANCEL_CONNECTOR_ERROR = 2,
    MSCONNECTOR_RESPONSE_COMPANION_CANCEL_PROTOCOL_ERROR = 3,
    MSCONNECTOR_RESPONSE_COMPANION_CANCEL_ENGINE_TIMEOUT = 4,
    MSCONNECTOR_RESPONSE_COMPANION_CANCEL_ENGINE_UNAVAILABLE = 5,
    MSCONNECTOR_RESPONSE_COMPANION_CANCEL_INVALID_ENGINE_RESPONSE = 6
} msconnector_response_companion_cancel_cause;

typedef struct msconnector_response_companion_transport_worker
    msconnector_response_companion_transport_worker;

/* The MRC1 transport owns framing, bounded parsing, connection sequencing and
 * peer identity. A backend owns the claimed transaction session. The opaque
 * session is valid only between a successful claim and one terminal
 * release/cancel/fail callback. A failed claim must leave `opaque` NULL; the
 * transport fails and invalidates any accidental partial claim. A successful
 * release or cancel and every fail callback must also clear `opaque`; a
 * violation faults the backend and rejects subsequent claims. Response
 * headers and body chunks passed to a
 * backend are borrowed and must not be retained after their callback returns.
 *
 * The transport serializes every vtable callback, including `expire`. Callbacks
 * run on the transport worker thread (or the listener thread for `expire`). A
 * backend whose native engine
 * is thread- or process-owner-bound (for example a future HAProxy SPOP
 * backend) must queue/synchronize its operation to that owner; it must never
 * dereference the native transaction directly from a detached MRC1 worker.
 */
/* Backend callback decisions borrow text pointers. The transport provides
 * this bounded session-owned scratch storage so an owner-thread bridge can
 * preserve native decision text until MRC1 has copied it after the callback.
 * It is not wire-visible and must never contain request or response bodies. */
typedef struct msconnector_response_companion_decision_storage {
    char redirect_url[MSCONNECTOR_MAX_PATH_LENGTH + 1U];
    char log_message[MSCONNECTOR_MAX_LOG_MESSAGE_LENGTH + 1U];
} msconnector_response_companion_decision_storage;

typedef struct msconnector_response_companion_backend_session {
    void *opaque;
    msconnector_response_companion_decision_storage decision_storage;
} msconnector_response_companion_backend_session;

typedef struct msconnector_response_companion_host_action {
    const msconnector_decision *decision;
    msconnector_decision_action actual_action;
    int visible_http_status;
    const char *transport_result;
    int connection_aborted;
} msconnector_response_companion_host_action;

typedef struct msconnector_response_companion_backend {
    void *context;
    /* Opt-in for backends that provide their own slot/session serialization.
     * Legacy Runtime backends remain globally serialized by default. */
    int allow_parallel_callbacks;
    int (*claim)(void *context, const char *handle,
        msconnector_response_companion_backend_session *session,
        msconnector_error *error);
    int (*process_response_headers)(void *context,
        msconnector_response_companion_backend_session *session,
        const msconnector_response *response, msconnector_decision *decision,
        msconnector_error *error);
    int (*append_response_body_chunk)(void *context,
        msconnector_response_companion_backend_session *session,
        const unsigned char *data, size_t size, msconnector_error *error);
    int (*finish_response_body)(void *context,
        msconnector_response_companion_backend_session *session,
        msconnector_decision *decision, msconnector_error *error);
    int (*set_response_commit_state)(void *context,
        const msconnector_response_companion_backend_session *session,
        int headers_sent, int body_started, msconnector_error *error);
    int (*record_host_action)(void *context,
        const msconnector_response_companion_backend_session *session,
        const msconnector_response_companion_host_action *action,
        msconnector_error *error);
    int (*cancel)(void *context,
        msconnector_response_companion_backend_session *session,
        int upstream_disconnect, msconnector_error *error);
    int (*release)(void *context,
        msconnector_response_companion_backend_session *session,
        msconnector_error *error);
    /* Must make the claimed session terminal and relinquish backend ownership.
     * The transport invalidates its opaque session immediately afterwards. */
    void (*fail)(void *context,
        msconnector_response_companion_backend_session *session,
        msconnector_transaction_error_class error_class);
    /* Optional bounded housekeeping. It is invoked from the listener thread,
     * never while a backend callback is in progress. */
    void (*expire)(void *context, uint64_t now_ms);
} msconnector_response_companion_backend;

typedef struct msconnector_response_companion_transport_config {
    /* Retained only for the backward-compatible Runtime initializer. New
     * backends use `backend` and do not expose native transaction pointers. */
    msconnector_runtime_response_companion_registry *registry;
    msconnector_response_companion_backend backend;
    char connector_id[MSCONNECTOR_TRANSACTION_CONTRACT_CONNECTOR_ID_SIZE];
    char socket_path[MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_SOCKET_SIZE];
    size_t max_header_count;
    size_t max_header_bytes;
    size_t max_response_body_bytes;
    uint64_t operation_timeout_ms;
    uid_t expected_uid;
    gid_t expected_gid;
} msconnector_response_companion_transport_config;

typedef struct msconnector_response_companion_transport_listener {
    int listener_fd;
    atomic_int running;
    atomic_int stopping;
    int listener_started;
    int identity_valid;
    uint64_t socket_device;
    uint64_t socket_inode;
    uid_t socket_owner;
    pthread_t listener_thread;
} msconnector_response_companion_transport_listener;

typedef struct msconnector_response_companion_transport_synchronization {
    int initialized;
    pthread_mutex_t worker_lock;
    pthread_cond_t workers_idle;
    pthread_mutex_t backend_lock;
    atomic_int backend_faulted;
} msconnector_response_companion_transport_synchronization;

typedef struct msconnector_response_companion_transport_workers {
    size_t worker_count;
    msconnector_response_companion_transport_worker *workers;
} msconnector_response_companion_transport_workers;

typedef struct msconnector_response_companion_transport {
    msconnector_response_companion_transport_config config;
    msconnector_response_companion_transport_listener listener;
    msconnector_response_companion_transport_synchronization synchronization;
    msconnector_response_companion_transport_workers workers;
} msconnector_response_companion_transport;

typedef struct msconnector_response_companion_transport_options {
    const char *connector_id;
    const char *socket_path;
    size_t max_header_count;
    size_t max_header_bytes;
    size_t max_response_body_bytes;
    uint64_t operation_timeout_ms;
} msconnector_response_companion_transport_options;

/* Initializes MRC1 with an explicit owner-preserving backend. The transport
 * copies the vtable; `backend->context` remains caller-owned until stop(). */
int msconnector_response_companion_transport_init_with_backend(
    msconnector_response_companion_transport *transport,
    const msconnector_response_companion_backend *backend,
    const msconnector_response_companion_transport_options *options,
    msconnector_error *error);

/* Initializes the bounded transport state. `socket_path` must name an absent
 * socket inside an existing, exact private (0700) directory owned by the
 * effective service user. `start` fails closed on unsupported peer credential
 * platforms instead of silently using a weaker identity check. */
int msconnector_response_companion_transport_init(
    msconnector_response_companion_transport *transport,
    msconnector_runtime_response_companion_registry *registry,
    const msconnector_response_companion_transport_options *options,
    msconnector_error *error);
int msconnector_response_companion_transport_start(
    msconnector_response_companion_transport *transport,
    msconnector_error *error);
/* Quiesces the listener, shuts down accepted clients, waits for all bounded
 * workers, and unlinks only the socket inode created by this transport. The
 * caller must invoke registry_shutdown() afterwards to drain unclaimed TTL
 * entries. */
int msconnector_response_companion_transport_stop(
    msconnector_response_companion_transport *transport,
    msconnector_error *error);

#ifdef __cplusplus
}
#endif

#endif
