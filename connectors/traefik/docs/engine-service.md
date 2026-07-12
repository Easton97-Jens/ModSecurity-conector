# Persistent local engine service

**Language:** English | [Deutsch](engine-service.de.md)

This directory contains the persistent local engine behind the selected
Traefik native-middleware host probe. `traefik-engine-service` is a persistent
local Unix-domain-socket process that owns one Common/libmodsecurity runtime.
It exists because the selected Traefik local-plugin path executes the Go
middleware through Yaegi; it cannot directly link the C/C++ libmodsecurity
runtime.

`native_middleware/` selects it only when `engineMode: uds` and a private
`engineSocketPath` are supplied by the isolated host harness. The default
source configuration remains `passthrough`. The focused local tests are not
Traefik host proof; the separate pinned-host probe is targeted No-CRS evidence
only and never promotes checked-in capabilities, CRS support, Safe/Strict, or
production readiness.

## Build and local protocol test

The service must be linked against an explicit locally built libmodsecurity:

```sh
MODSECURITY_INCLUDE_DIR=/absolute/include \
MODSECURITY_LIB_DIR=/absolute/lib \
make -C connectors/traefik build-engine-service

MODSECURITY_INCLUDE_DIR=/absolute/include \
MODSECURITY_LIB_DIR=/absolute/lib \
make -C connectors/traefik test-engine-service
```

`test-engine-service` builds the C17 service, runs its parser/self-test, starts
one real local Common/libmodsecurity service process, and drives both a safe
transaction and the repository's targeted request-header deny rule over Unix
sockets. It also rejects an oversized chunk and an out-of-state outcome
acknowledgement. This is a focused service/protocol test only; it does not
start Traefik or prove a host action.

The separate real-host probe builds the service under its isolated runtime
root, starts it once, and selects `engineMode: uds` in the pinned Traefik local
plugin. When `MSCONNECTOR_RULES_FILE` is set, it loads that exact canonical
No-CRS rules file and requires rule IDs `1100001`, `1100101`, `1100201`, and
`1100301` for P1 through P4. The checked-in targeted fixture is a standalone
fallback only. The host probe requires P1 allow `200`, P1 deny `403`, P2 deny
`403`, P3 pre-commit deny `403`, and P4 safe/log-only with visible `200`; P4
strict is explicitly `NOT EXECUTED`.

The example config is
`config/traefik-engine-service.conf`. Its relative `rules_file` assumes the
repository root as the working directory. Deployments should use a trusted
absolute rules path and a private runtime directory:

```sh
cd /absolute/ModSecurity-conector
/absolute/traefik-engine-service --check-config \
  --config connectors/traefik/config/traefik-engine-service.conf
/absolute/traefik-engine-service --serve \
  --config connectors/traefik/config/traefik-engine-service.conf \
  --socket /absolute/private-runtime/traefik-engine.sock
```

The daemon refuses an existing socket path, binds with mode `0600`, and does
not unlink an arbitrary pre-existing path. It serializes Common runtime calls
behind a mutex while retaining transaction state per Unix connection. Its
process and engine persist across connections; a connection represents exactly
one transaction.

## Wire contract

`src/traefik_engine_protocol.h` is the normative protocol declaration. Frames
have the following 12-byte big-endian header:

| Bytes | Value |
| --- | --- |
| 0--3 | ASCII `MSE1` |
| 4 | protocol version `1` |
| 5 | opcode |
| 6--7 | zero reserved flags |
| 8--11 | payload length |

The maximum payload is 65,536 bytes. Every raw request or response chunk is
individually capped at 32,768 bytes. Metadata has separate caps: at most 128
headers, 256-byte header names, 8,192-byte header values, a 4,096-byte URI,
and bounded IDs/addresses. Embedded NUL bytes, trailing metadata, invalid
frame flags, invalid ordering, and duplicate EOS operations are rejected.

The client sends this ordered lifecycle:

1. `BEGIN` carries bounded request metadata and headers. It invokes Common
   connection/URI/request-header processing and returns the first decision.
2. Zero or more `REQUEST_CHUNK` frames, followed exactly once by
   `REQUEST_EOS`, append and finish the request body.
3. `RESPONSE_HEADERS`, zero or more `RESPONSE_CHUNK` frames, and exactly one
   `RESPONSE_EOS` process the response lifecycle. `RESPONSE_COMMIT` records
   the two host metadata booleans (`headers_sent`, `body_started`) immediately
   before or after the host hands bytes onward; it never buffers bytes.
4. `FINISH` invokes Common logging/finalization only after the required EOS
   calls (or after a terminal engine decision).
5. `DESTROY` is required after a successful `FINISH` and releases the Common
   transaction. EOF, malformed input, or a socket timeout also destroys an
   in-flight transaction without synthesizing a host outcome.

`RESPONSE_HEADERS` is `u16 status`, a bounded length-prefixed HTTP version,
then a bounded header list. `BEGIN` uses length-prefixed method, URI, HTTP
version, hostname, client address/port, server address/port, host request ID,
and headers in the precise order documented in the header.

Every command gets a `RESULT` frame. Its payload starts with command, result
code, requested decision action, phase, HTTP status, and lifecycle flags;
only bounded transaction ID, rule ID, and redirect URL may follow. It never
includes request/response body bytes, headers, URI values, rule messages, or
log messages.

## Outcome boundary

`OUTCOME` is sent only after the Go `ResponseWriter` has actually written the
selected host action. A failed or short response-body write produces commit
metadata only and never a host-confirmed outcome. Before response commit it
accepts only a matching requested disruptive action with an explicit
`HOST_ACTION_APPLIED` flag and matching visible status. With a run-local
`event_path`, the service calls the Common host-outcome API then: Common
retains the raw engine-decision event and writes a second event with canonical
`transport_result=http_status`.

After response headers/body have been committed, a response-body disruptive
decision can be acknowledged only as `LOG_ONLY`, with no applied-action flag
and the actual already-visible HTTP status. The service cannot reset a Traefik
response or prove a late abort, so it refuses all stronger post-commit
acknowledgements. Its host-confirmed event uses
`transport_result=log_only`. The pinned-host probe records this only as the
targeted P4 safe/log-only behavior; strict late intervention is `NOT EXECUTED`.

The host harness keeps `event_path` under its connector-specific runtime root,
sets Common integration mode to `native-traefik-middleware`, forwards the raw
JSONL artifact, and filters host-confirmed outcome events by
canonical `transport_result` values. It does not treat the raw
requested-decision event as a host action. Cancellation/disconnect coverage and
capability promotion remain separate work.
