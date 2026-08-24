# Connector runtime failure policy

**Language:** English | [Deutsch](runtime-failure-policy.de.md)

**Scope:** Apache, NGINX, HAProxy HTX, HAProxy SPOE/SPOP, Envoy `ext_authz`,
Envoy `ext_proc`, Traefik `forwardAuth`, Traefik Native UDS, lighttpd Stock,
and lighttpd Patched.

This document is the shared semantic contract for failures, availability, and
cleanup. It separates the intended policy (`implemented policy`) from what was
actually exercised in this checkout (`local evidence`). A source check or a
connector self-test is not a claim that every selected host and protocol was
run.

## Decision rules

The default security decision is fail-closed. A peer-local protocol failure may
close only the affected peer, but it must not turn into an allow decision for a
transaction. An explicit product setting such as SPOP `fail-mode=open` remains
an operator override and is reported as such; it is never an implicit fallback.

For the project-supplied HAProxy SPOE/SPOP closed-default examples, do not set
HAProxy's `option continue-on-error`. With `fail-mode=closed`, that HAProxy
opt-in is incompatible with the security contract: an unavailable or failed
agent may otherwise be treated as an Allow. The supplied harness leaves the
option unset. An admission or handshake failure without an ACK is a closed
SPOP transport failure for that peer; an explicit failure ACK maps to `503`.
The exact native-HAProxy client status for an unacknowledged admission close is
`NOT_EXECUTED`; it is never documented as an Allow. Peer-local admission or
handshake failure still closes only that peer and never blocks the global
accept/HELLO loop.

Every failed transaction/stream must release its transaction state, buffers,
file descriptors, goroutines/threads, and owned socket/port resources. Cleanup
is idempotent. A legitimate request on a new or reusable connection must be
able to run after a failure, unless the host itself has been deliberately
stopped. When a native engine call cannot be interrupted, the bounded shutdown
path uses a defined controlled restart rather than destroying state still used
by a worker.

### Behavior classes

The matrices below use these classes. The fields are normative for every
connector row that references the class.

| Class | Fail mode | Host action | HTTP/protocol status | Event | User/operator effect | Cleanup | Follow-up |
|---|---|---|---|---|---|---|---|
| E — engine failure | closed | Abort the current decision and terminate the transaction | Apache/NGINX/lighttpd: `500`; HAProxy/Traefik: configured closed error (`500`/`503`); Envoy: gRPC `Unavailable`/`DeadlineExceeded`, host closed response | `engine_error` plus connector error log | Current request is denied or fails visibly; operator gets an actionable error | Destroy engine transaction, release body/response buffers, close failed backend/agent stream | New request may start and is tested where `SELF_TEST_PASS` is shown |
| P — peer/protocol abort | closed for the affected transaction; peer-local close is allowed | Close/reset only the affected peer/stream; never continue with a partial decision | HTTP `400`/`502`/`503` as applicable; gRPC `Cancelled`/`Unavailable`; SPOP protocol disconnect/closed ACK | `peer_error` or `protocol_error` | One request/peer fails; other peers remain eligible | Cancel stream, close FD, discard partial frame/body, remove transaction state | A fresh peer/request is accepted; no global accept-loop block |
| I — invalid/incomplete engine result | closed | Treat the result as unusable and abort the current transaction | Same closed status as E; no partial allow | `invalid_engine_response` or `incomplete_engine_response` | Request is denied; malformed engine data is never trusted | Free parser/result buffers and destroy transaction exactly once | Follow-up request gets a fresh engine transaction |
| C — cancel/shutdown | closed for in-flight work | Propagate cancellation, close stream/connection, and stop accepting new work during shutdown | HTTP `499`/`503` or host-specific closed status; gRPC `Cancelled` | `cancelled` or `shutdown` | Current work ends; operator sees bounded shutdown or controlled restart | Idempotent cancellation, bounded worker wait, FD/UDS removal; controlled restart if an engine call remains stuck | After restart/new listener, a control request is accepted |
| L — limit/admission | closed | Reject only the over-limit request/stream before unbounded state allocation | HTTP `413`/`431`/`503`; gRPC `ResourceExhausted`; protocol limit error | `limit_rejected` | Caller receives a bounded rejection; service remains available | Release admission slot and partial buffers | A request within limits succeeds |
| A — legitimate control | configured allow/block decision | Preserve the engine and rule decision; do not change security semantics during recovery | Normal configured status, including a deliberate block | `decision` | Positive control remains positive; block control remains blocked | Normal success cleanup | Must succeed after V1–V15 failures |
| U — cleanup assertion | n/a (inherited from preceding class) | Verify process, port, UDS, stream, and transaction state are gone or defined | No stale listener/stream; preceding status remains observable | `cleanup_complete` or `cleanup_error` | Operator can safely retry/reload; leaks are actionable defects | Double cleanup is harmless; missing cleanup is a finding | Next request is not prevented by stale state |

`SELF_TEST_PASS` means a local connector-owned runtime/self-test exercised the
described path and returned success. `SOURCE_VALIDATED` means focused source or
contract tests passed. `BLOCKED_ENVIRONMENT` means the repository did not have
the selected host/runtime prerequisite. `NOT_EXECUTED` means no claim is made.

## Connector-specific policy and evidence

The following tables deliberately repeat all 17 vectors for each connector.
The class column points to the complete host action, status, event, impact,
cleanup, and follow-up contract above. Evidence is bounded to this repository.

### Vectors

| ID | Failure vector |
|---|---|
| V1 | Engine unavailable at startup |
| V2 | Engine fails during a transaction |
| V3 | Engine exceeds the configured operation timeout |
| V4 | Engine returns an invalid response |
| V5 | Engine returns an incomplete response |
| V6 | Client closes early |
| V7 | Backend/upstream closes early |
| V8 | Protocol peer sends an incomplete handshake |
| V9 | TCP, TLS, UDS, or gRPC connection resets |
| V10 | Request body ends early |
| V11 | Response body ends early |
| V12 | Host is terminated during active requests |
| V13 | Connector or agent is terminated during active requests |
| V14 | Multiple requests or streams run in parallel |
| V15 | Maximum size/resource limits are exceeded |
| V16 | Legitimate control request follows the failure |
| V17 | Cleanup is checked after success, failure, timeout, and cancel |

### Apache

| Vector | Class | Local evidence |
|---|---|---|
| V1 | E | SOURCE_VALIDATED: startup/connection failures return closed `500` and `AP_CONN_CLOSE` |
| V2 | E | SOURCE_VALIDATED: native API results require success value `1` |
| V3 | E | SOURCE_VALIDATED: operation error is terminal; host timeout run BLOCKED_ENVIRONMENT |
| V4 | I | SOURCE_VALIDATED: invalid native result is rejected |
| V5 | I | SOURCE_VALIDATED: incomplete body/header result is rejected |
| V6 | P | SOURCE_VALIDATED: connection/URI mapping failure closes request |
| V7 | P | NOT_EXECUTED: host upstream-close run |
| V8 | P | NOT_APPLICABLE: Apache module has no agent handshake |
| V9 | P | NOT_EXECUTED: live reset run |
| V10 | I | SOURCE_VALIDATED: request-body append/file failures close with `500` |
| V11 | I | SOURCE_VALIDATED: response-body append failures close with `500` |
| V12 | C | NOT_EXECUTED: live host termination |
| V13 | C | NOT_EXECUTED: live module termination |
| V14 | L | SOURCE_VALIDATED: pool cleanup is retained; parallel host run NOT_EXECUTED |
| V15 | L | SOURCE_VALIDATED: host limit remains bounded; full host run NOT_EXECUTED |
| V16 | A | SOURCE_VALIDATED: `tests/test_apache_fail_closed.py` preserves control path |
| V17 | U | SOURCE_VALIDATED: pool-owned terminal cleanup; live FD audit NOT_EXECUTED |

### NGINX

| Vector | Class | Local evidence |
|---|---|---|
| V1 | E | SOURCE_VALIDATED: unavailable engine fails closed with `500` |
| V2 | E | SOURCE_VALIDATED: connection/URI/header native failures finalize `500` |
| V3 | E | SOURCE_VALIDATED: operation failure is terminal; live timeout BLOCKED_ENVIRONMENT |
| V4 | I | SOURCE_VALIDATED: invalid native result is rejected |
| V5 | I | SOURCE_VALIDATED: incomplete result is rejected |
| V6 | P | SOURCE_VALIDATED: request mapping failures finalize the request |
| V7 | P | NOT_EXECUTED: live upstream-close run |
| V8 | P | NOT_APPLICABLE: NGINX module has no agent handshake |
| V9 | P | NOT_EXECUTED: live TCP/TLS reset run |
| V10 | I | SOURCE_VALIDATED: request body append/file failures finalize `500` |
| V11 | I | SOURCE_VALIDATED: response body append failure finalizes `500` |
| V12 | C | NOT_EXECUTED: live worker shutdown |
| V13 | C | NOT_EXECUTED: live module termination |
| V14 | L | SOURCE_VALIDATED: worker-local errors; parallel host run NOT_EXECUTED |
| V15 | L | SOURCE_VALIDATED: bounded body mapping; full host limit run NOT_EXECUTED |
| V16 | A | SOURCE_VALIDATED: `connectors/nginx/tests/test_fail_closed_contract.py` preserves follow-up contract |
| V17 | U | SOURCE_VALIDATED: request finalization paths; live FD audit NOT_EXECUTED |

### HAProxy HTX

| Vector | Class | Local evidence |
|---|---|---|
| V1 | E | SOURCE_VALIDATED: binding rejects native engine failure |
| V2 | E | SOURCE_VALIDATED: direct native API requires result `1` |
| V3 | E | SOURCE_VALIDATED: terminal binding error; live timeout BLOCKED_ENVIRONMENT |
| V4 | I | SOURCE_VALIDATED: invalid native result is rejected |
| V5 | I | SOURCE_VALIDATED: incomplete result is rejected |
| V6 | P | SOURCE_VALIDATED: transaction-local binding error |
| V7 | P | NOT_EXECUTED: live upstream-close run |
| V8 | P | NOT_APPLICABLE: HTX route has no SPOE handshake |
| V9 | P | NOT_EXECUTED: live reset run |
| V10 | I | SOURCE_VALIDATED: request body append failure is terminal |
| V11 | I | SOURCE_VALIDATED: response body append failure is terminal |
| V12 | C | NOT_EXECUTED: live HAProxy shutdown |
| V13 | C | NOT_EXECUTED: live filter termination |
| V14 | L | SOURCE_VALIDATED: binding self-test PASS; parallel host run NOT_EXECUTED |
| V15 | L | SOURCE_VALIDATED: bounded binding input; host limit run NOT_EXECUTED |
| V16 | A | SELF_TEST_PASS: `self-test-modsecurity-binding` keeps disruptive decision `403` |
| V17 | U | SOURCE_VALIDATED: transaction cleanup path; live FD audit NOT_EXECUTED |

### HAProxy SPOE/SPOP

| Vector | Class | Local evidence |
|---|---|---|
| V1 | E | SOURCE_VALIDATED: engine startup failure is terminal for the agent |
| V2 | E | SOURCE_VALIDATED: per-peer worker keeps failure local |
| V3 | E | SOURCE_VALIDATED: handshake/operation deadlines are bounded |
| V4 | I | SOURCE_VALIDATED: malformed protocol/result is closed; default is closed |
| V5 | I | SOURCE_VALIDATED: incomplete result/handshake is closed |
| V6 | P | SELF_TEST_PASS: peer close does not terminate the agent |
| V7 | P | NOT_APPLICABLE: agent self-test has no HTTP upstream |
| V8 | P | SELF_TEST_PASS: incomplete/slow HELLO is rejected by deadline |
| V9 | P | SELF_TEST_PASS: `MSG_NOSIGNAL`/peer reset path recovers |
| V10 | P | NOT_APPLICABLE: SPOP has framed protocol data, not HTTP body hooks |
| V11 | P | NOT_APPLICABLE: SPOP has framed protocol data, not HTTP body hooks |
| V12 | C | SOURCE_VALIDATED: bounded worker reap and listener shutdown |
| V13 | C | SOURCE_VALIDATED: worker isolation prevents process-wide peer failure |
| V14 | L | SELF_TEST_PASS: parallel healthcheck/follow-up HELLO succeeds; a saturated peer is closed locally while the parent accept loop remains free |
| V15 | L | SELF_TEST_PASS: worker count `1..64`, bounded handshake/socket deadlines, and immediate peer-local close on worker saturation |
| V16 | A | SELF_TEST_PASS: valid HELLO, typed block ACK (`403`), and a follow-up HELLO after saturation remain unchanged |
| V17 | U | SELF_TEST_PASS: no listener remains after self-test; peer FDs are closed |

SPOP writes use per-send `MSG_NOSIGNAL` (and `SO_NOSIGPIPE` where available);
there is no global `SIGPIPE` ignore. Each peer is isolated in a bounded worker,
and the default malformed/failure mode is closed. The explicit open mode is an
operator choice and must be visible in configuration and evidence.

### Envoy `ext_authz`

| Vector | Class | Local evidence |
|---|---|---|
| V1 | E | SOURCE_VALIDATED: common HTTP authorization service rejects unavailable engine |
| V2 | E | SOURCE_VALIDATED: worker returns closed authorization result |
| V3 | E | SOURCE_VALIDATED: bounded connection/worker wait; live Envoy run NOT_EXECUTED |
| V4 | I | SOURCE_VALIDATED: invalid authorization response is not an allow |
| V5 | I | SOURCE_VALIDATED: incomplete response closes authorization request |
| V6 | P | SOURCE_VALIDATED: peer-local `send_all`/read failure closes worker connection |
| V7 | P | NOT_EXECUTED: Envoy upstream-close run |
| V8 | P | NOT_APPLICABLE: ext_authz uses HTTP authorization, not SPOE HELLO |
| V9 | P | SOURCE_VALIDATED: per-write `MSG_NOSIGNAL`; live reset NOT_EXECUTED |
| V10 | P | SOURCE_VALIDATED: incomplete request is denied |
| V11 | P | NOT_APPLICABLE: ext_authz does not process upstream response body |
| V12 | C | SOURCE_VALIDATED: bounded worker shutdown and socket cancellation |
| V13 | C | SOURCE_VALIDATED: worker termination returns failure, not allow |
| V14 | L | SOURCE_VALIDATED: bounded worker admission; parallel Envoy run NOT_EXECUTED |
| V15 | L | SOURCE_VALIDATED: header/body bounds are enforced before allocation |
| V16 | A | SOURCE_VALIDATED: duplicate security-header controls remain enforced |
| V17 | U | SOURCE_VALIDATED: worker socket cleanup; live process/FD audit NOT_EXECUTED |

### Envoy `ext_proc`

The current follow-up fixture asserts `pendingReceives == 0` after the idle
handler returns; mutex and forced-stop waits are deadline-bounded. An already
running uninterruptible native C destructor remains a controlled nonzero
restart path, not an in-process cancellation claim.

| Vector | Class | Local evidence |
|---|---|---|
| V1 | E | SOURCE_VALIDATED: service config/startup rejects invalid engine setup |
| V2 | E | SOURCE_VALIDATED: engine failure returns a gRPC failure, not an allow |
| V3 | E | SOURCE_VALIDATED: engine operation timeout is separate from stream idle |
| V4 | I | SOURCE_VALIDATED: invalid processing result fails the stream |
| V5 | I | SOURCE_VALIDATED: incomplete processing message fails the stream |
| V6 | P | SOURCE_VALIDATED: stream cancellation releases processing state |
| V7 | P | NOT_EXECUTED: live Envoy upstream-close run |
| V8 | P | NOT_APPLICABLE: ext_proc is gRPC, not an HTTP agent HELLO protocol |
| V9 | P | SOURCE_VALIDATED: gRPC reset maps to stream failure; live Envoy reset NOT_EXECUTED |
| V10 | P | SOURCE_VALIDATED: request-body EOF is a failed/incomplete processing stream |
| V11 | P | SOURCE_VALIDATED: response-body EOF is a failed/incomplete processing stream |
| V12 | C | SELF_TEST_PASS: `TestCommonRuntimeEngineCloseHonorsShutdownContext` holds the mutex, returns `ErrCommonRuntimeShutdownTimeout` within the deadline, and main performs controlled exit `1` |
| V13 | C | SELF_TEST_PASS: connector/agent termination follows the bounded controlled-exit `1` path; no native release is attempted while the engine call is still blocked |
| V14 | L | SELF_TEST_PASS: `go test -race ./...`; max concurrent streams is bounded |
| V15 | L | SOURCE_VALIDATED: `max_concurrent_streams <= 1024`; oversized admission is `ResourceExhausted` |
| V16 | A | SELF_TEST_PASS: idle timeout cleanup followed by a valid stream succeeds |
| V17 | U | SOURCE_VALIDATED: tagged native Common-Runtime test `TestCommonRuntimeEngineCloseHonorsShutdownContext` proves deadline-bounded cleanup and no native release; live Envoy FD audit NOT_EXECUTED |

The engine operation timeout and server-side stream-idle timeout are separate.
Activity is one complete `ProcessingRequest`; a valid message and its response
reset the idle timer. Regularly active long-lived streams are therefore not
expired merely because the engine operation timeout exists. Admission is
bounded by gRPC `MaxConcurrentStreams` and the service limit.

### Traefik `forwardAuth`

| Vector | Class | Local evidence |
|---|---|---|
| V1 | E | SOURCE_VALIDATED: common authorization service fails closed on engine unavailability |
| V2 | E | SOURCE_VALIDATED: worker/authorization failure is not an allow |
| V3 | E | SOURCE_VALIDATED: bounded worker timeout; live Traefik forwardAuth run NOT_EXECUTED |
| V4 | I | SOURCE_VALIDATED: invalid auth response is rejected |
| V5 | I | SOURCE_VALIDATED: incomplete auth response is rejected |
| V6 | P | SOURCE_VALIDATED: peer-local authorization connection closes |
| V7 | P | NOT_EXECUTED: live upstream-close run |
| V8 | P | NOT_APPLICABLE: forwardAuth has no SPOE HELLO |
| V9 | P | SOURCE_VALIDATED: per-write `MSG_NOSIGNAL`; live reset NOT_EXECUTED |
| V10 | P | SOURCE_VALIDATED: incomplete authorization request is denied |
| V11 | P | NOT_APPLICABLE: forwardAuth does not inspect upstream response body |
| V12 | C | SOURCE_VALIDATED: bounded authorization worker shutdown |
| V13 | C | SOURCE_VALIDATED: worker exit cannot become an allow |
| V14 | L | SOURCE_VALIDATED: bounded worker admission; live parallel run NOT_EXECUTED |
| V15 | L | SOURCE_VALIDATED: bounded header/body handling |
| V16 | A | SOURCE_VALIDATED: normal authorization control remains unchanged |
| V17 | U | SOURCE_VALIDATED: worker sockets are closed; live Traefik FD audit NOT_EXECUTED |

### Traefik Native UDS

| Vector | Class | Local evidence |
|---|---|---|
| V1 | E | SELF_TEST_PASS: engine service startup/configuration checks are bounded |
| V2 | E | SELF_TEST_PASS: engine failure is returned as a protocol error |
| V3 | E | SOURCE_VALIDATED: worker/engine waits have bounded shutdown handling |
| V4 | I | SELF_TEST_PASS: malformed engine response is rejected |
| V5 | I | SELF_TEST_PASS: incomplete response is rejected |
| V6 | P | SELF_TEST_PASS: reset peer is isolated and follow-up request succeeds |
| V7 | P | NOT_EXECUTED: live Traefik upstream-close run |
| V8 | P | SELF_TEST_PASS: framed protocol validation rejects incomplete input |
| V9 | P | SELF_TEST_PASS: UDS reset path does not kill service |
| V10 | P | SOURCE_VALIDATED: incomplete request frame is rejected |
| V11 | P | SELF_TEST_PASS: incomplete/oversized response is rejected |
| V12 | C | SOURCE_VALIDATED: active sockets are shut down during service stop |
| V13 | C | SOURCE_VALIDATED: bounded worker wait uses controlled restart on stuck engine |
| V14 | L | SELF_TEST_PASS: worker admission remains bounded and listener survives peer failure |
| V15 | L | SELF_TEST_PASS: response and frame limits are enforced |
| V16 | A | SELF_TEST_PASS: valid request after reset succeeds |
| V17 | U | SELF_TEST_PASS: UDS is removed only when owned; replacement sentinel survives |

The Native UDS shutdown path bounds the worker wait. If an uninterruptible
engine call remains after active sockets are shut down, the service removes its
owned socket and exits through the documented controlled-restart path; it does
not free state still reachable by a worker.

### lighttpd Stock

| Vector | Class | Local evidence |
|---|---|---|
| V1 | E | SELF_TEST_PASS: stock host runtime smoke started, returned baseline `200`, and recorded the connector event |
| V2 | E | NOT_EXECUTED: in-transaction engine failure |
| V3 | E | NOT_EXECUTED: live timeout run |
| V4 | I | NOT_EXECUTED: invalid engine result |
| V5 | I | NOT_EXECUTED: incomplete engine result |
| V6 | P | NOT_EXECUTED: live client-close run |
| V7 | P | NOT_EXECUTED: live backend-close run |
| V8 | P | NOT_APPLICABLE: Stock module has no agent handshake |
| V9 | P | NOT_EXECUTED: live reset run |
| V10 | I | NOT_EXECUTED: premature request-body end |
| V11 | I | NOT_EXECUTED: premature response-body end |
| V12 | C | NOT_EXECUTED: live Stock shutdown |
| V13 | C | NOT_EXECUTED: live module termination |
| V14 | L | NOT_EXECUTED: parallel host run |
| V15 | L | NOT_EXECUTED: maximum size/resource limit |
| V16 | A | SELF_TEST_PASS: stock runtime smoke observed baseline `200` and rule block `403` |
| V17 | U | SELF_TEST_PASS: smoke observed connector event and listener cleanup |

### lighttpd Patched

| Vector | Class | Local evidence |
|---|---|---|
| V1 | E | SELF_TEST_PASS: patched host runtime smoke started, returned baseline `200`, and recorded the connector event |
| V2 | E | NOT_EXECUTED: in-transaction engine failure |
| V3 | E | NOT_EXECUTED: live patched-host timeout run |
| V4 | I | NOT_EXECUTED: invalid engine result |
| V5 | I | NOT_EXECUTED: incomplete engine result |
| V6 | P | NOT_EXECUTED: live client-close run |
| V7 | P | NOT_EXECUTED: live backend-close run |
| V8 | P | NOT_APPLICABLE: patched module has no agent handshake |
| V9 | P | NOT_EXECUTED: live reset run |
| V10 | I | NOT_EXECUTED: premature request-body end |
| V11 | I | NOT_EXECUTED: premature response-body end |
| V12 | C | NOT_EXECUTED: live patched-host shutdown |
| V13 | C | NOT_EXECUTED: live module termination |
| V14 | L | NOT_EXECUTED: parallel host run |
| V15 | L | NOT_EXECUTED: maximum size/resource limit |
| V16 | A | SELF_TEST_PASS: patched runtime smoke observed baseline `200` and rule block `403` |
| V17 | U | SELF_TEST_PASS: smoke observed connector event and listener cleanup |

## Configuration-documentation boundary

The generated files under `examples/*/configuration-reference*.md` were not
edited. Their generator and its CI checks are outside this task's scope.
`connectors/haproxy` source/direct documentation is canonical for the SPOP
worker default and bounds, and the Envoy `ext_proc` service JSON/direct
documentation is canonical for stream-idle and concurrent-stream settings until
the generator can be changed in a separately authorized CI task. This is a
documented evidence boundary, not an assertion that generated references are
current.

## Residual risks and required next evidence

The local source and focused self-tests cover the implemented safety controls,
including the SPOP peer-isolation runtime test, Traefik UDS runtime test, and
Envoy `go test -race ./...`. Full live host runs for all ten routes, complete
TLS/HTTP/2/HTTP/3 matrices, and process/FD leak audits remain
`BLOCKED_ENVIRONMENT` or `NOT EXECUTED` where shown above. In particular,
uninterruptible native engine calls can require the documented controlled
restart; they must not be described as graceful in-process cancellation until a
host-specific test proves it.

Before closing a finding, rerun its original reproducer and its positive
follow-up control against the selected host, retain event/process/port/UDS
evidence, and then update the corresponding finding record.
