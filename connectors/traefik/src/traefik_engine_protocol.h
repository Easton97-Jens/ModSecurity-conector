#ifndef TRAEFIK_ENGINE_PROTOCOL_H
#define TRAEFIK_ENGINE_PROTOCOL_H

/*
 * Private, local-only protocol between the Traefik Go local-plugin adapter and
 * the persistent Common/libmodsecurity engine service.  It is deliberately a
 * small framed protocol rather than an HTTP compatibility endpoint: Traefik's
 * local-plugin loader executes Go through Yaegi, so it cannot link directly to
 * the C++ libmodsecurity runtime.
 *
 * Every frame has a 12-byte network-order header:
 *
 *   bytes 0..3   ASCII "MSE1"
 *   byte  4      protocol version (1)
 *   byte  5      opcode
 *   bytes 6..7   reserved flags (must be zero)
 *   bytes 8..11  payload length (uint32, maximum
 *                TRAEFIK_ENGINE_PROTOCOL_MAX_FRAME_PAYLOAD)
 *
 * The service accepts one transaction per Unix-domain socket connection.  The
 * daemon persists across connections; a client must explicitly send FINISH
 * followed by DESTROY on a successful lifecycle. EOF/error cleanup destroys
 * an unfinished transaction without creating a host-confirmed outcome.
 *
 * BEGIN payload (all integer fields are network-order):
 *
 *   u16 method_len, method bytes
 *   u16 uri_len, uri bytes
 *   u16 http_version_len, http_version bytes
 *   u16 hostname_len, hostname bytes
 *   u16 client_address_len, client_address bytes, u16 client_port
 *   u16 server_address_len, server_address bytes, u16 server_port
 *   u16 host_request_id_len, host_request_id bytes
 *   u16 header_count
 *   repeated header_count times: u16 name_len, name bytes,
 *                                  u16 value_len, value bytes
 *
 * RESPONSE_HEADERS payload:
 *
 *   u16 status, u16 http_version_len, http_version bytes, u16 header_count,
 *   followed by the same bounded name/value header entries as BEGIN.
 *
 * REQUEST_CHUNK and RESPONSE_CHUNK carry one raw binary chunk.  They are not
 * decoded, logged, reflected in a RESULT frame, or retained by this protocol.
 * REQUEST_EOS, RESPONSE_EOS, FINISH, and DESTROY have empty payloads.
 * RESPONSE_COMMIT is exactly two bytes: headers_sent and body_started, each 0
 * or 1. OUTCOME is u8 actual_action, u8 host_flags, u16 visible_status. The
 * Go client sends it only after the underlying ResponseWriter has accepted the
 * action. When the configured Common runtime has a run-local event_path, the
 * service records a second, host-confirmed event after validating OUTCOME; the
 * raw engine-decision event remains distinct from that record.
 *
 * A post-commit disruptive response-body decision can only be acknowledged as
 * LOG_ONLY with host_flags clear and the actual already-visible HTTP status.
 * The service cannot prove or claim a late host abort. A pre-commit action
 * must match the requested disruptive action, carry HOST_ACTION_APPLIED, and
 * report the matching visible HTTP status.
 */

#include <stdint.h>

#define TRAEFIK_ENGINE_PROTOCOL_VERSION 1U
#define TRAEFIK_ENGINE_PROTOCOL_HEADER_SIZE 12U
#define TRAEFIK_ENGINE_PROTOCOL_MAX_FRAME_PAYLOAD 65536U
#define TRAEFIK_ENGINE_PROTOCOL_MAX_CHUNK 32768U
#define TRAEFIK_ENGINE_PROTOCOL_MAX_HEADERS 128U
#define TRAEFIK_ENGINE_PROTOCOL_MAX_METHOD 32U
#define TRAEFIK_ENGINE_PROTOCOL_MAX_URI 4096U
#define TRAEFIK_ENGINE_PROTOCOL_MAX_HTTP_VERSION 32U
#define TRAEFIK_ENGINE_PROTOCOL_MAX_HOSTNAME 255U
#define TRAEFIK_ENGINE_PROTOCOL_MAX_ADDRESS 255U
#define TRAEFIK_ENGINE_PROTOCOL_MAX_HOST_REQUEST_ID 256U
#define TRAEFIK_ENGINE_PROTOCOL_MAX_HEADER_NAME 256U
#define TRAEFIK_ENGINE_PROTOCOL_MAX_HEADER_VALUE 8192U
#define TRAEFIK_ENGINE_PROTOCOL_MAX_TRANSACTION_ID 256U
#define TRAEFIK_ENGINE_PROTOCOL_MAX_RULE_ID 256U
#define TRAEFIK_ENGINE_PROTOCOL_MAX_REDIRECT 2048U

enum traefik_engine_protocol_opcode {
    TRAEFIK_ENGINE_PROTOCOL_BEGIN = 1,
    TRAEFIK_ENGINE_PROTOCOL_REQUEST_CHUNK = 2,
    TRAEFIK_ENGINE_PROTOCOL_REQUEST_EOS = 3,
    TRAEFIK_ENGINE_PROTOCOL_RESPONSE_HEADERS = 4,
    TRAEFIK_ENGINE_PROTOCOL_RESPONSE_CHUNK = 5,
    TRAEFIK_ENGINE_PROTOCOL_RESPONSE_EOS = 6,
    TRAEFIK_ENGINE_PROTOCOL_RESPONSE_COMMIT = 7,
    TRAEFIK_ENGINE_PROTOCOL_FINISH = 8,
    TRAEFIK_ENGINE_PROTOCOL_DESTROY = 9,
    TRAEFIK_ENGINE_PROTOCOL_OUTCOME = 10,
    TRAEFIK_ENGINE_PROTOCOL_RESULT = 128
};

enum traefik_engine_protocol_result_code {
    TRAEFIK_ENGINE_PROTOCOL_RESULT_OK = 0,
    TRAEFIK_ENGINE_PROTOCOL_RESULT_PROTOCOL = 1,
    TRAEFIK_ENGINE_PROTOCOL_RESULT_STATE = 2,
    TRAEFIK_ENGINE_PROTOCOL_RESULT_RUNTIME = 3,
    TRAEFIK_ENGINE_PROTOCOL_RESULT_LIMIT = 4,
    TRAEFIK_ENGINE_PROTOCOL_RESULT_INTERNAL = 5
};

enum traefik_engine_protocol_result_flag {
    TRAEFIK_ENGINE_PROTOCOL_RESULT_DISRUPTIVE = 1U << 0,
    TRAEFIK_ENGINE_PROTOCOL_RESULT_LATE = 1U << 1,
    TRAEFIK_ENGINE_PROTOCOL_RESULT_REQUEST_EOS = 1U << 2,
    TRAEFIK_ENGINE_PROTOCOL_RESULT_RESPONSE_HEADERS = 1U << 3,
    TRAEFIK_ENGINE_PROTOCOL_RESULT_RESPONSE_EOS = 1U << 4,
    TRAEFIK_ENGINE_PROTOCOL_RESULT_FINISHED = 1U << 5,
    TRAEFIK_ENGINE_PROTOCOL_RESULT_DESTROYED = 1U << 6
};

enum traefik_engine_protocol_outcome_flag {
    TRAEFIK_ENGINE_PROTOCOL_OUTCOME_HOST_ACTION_APPLIED = 1U << 0
};

#endif
