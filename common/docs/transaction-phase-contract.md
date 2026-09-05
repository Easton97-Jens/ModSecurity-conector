# Shared transaction and phase contract

**Language:** English | [Deutsch](transaction-phase-contract.de.md)

Status: current Common contract; source-backed adapter boundary

Architecture rationale: [ADR-003](../../docs/decisions/ADR-003-shared-p1-p4-lifecycle-semantics.md)

## Authority and derived P1–P4 meaning

This contract consolidates the existing neutral phases in
<code>common/include/msconnector/phase.h</code>, the Common engine wrapper,
Common Runtime, native adapter hooks, tests, and the architecture guide. It
does not introduce a new rule-engine phase.

| Business phase | Existing meaning | Completion point |
| --- | --- | --- |
| P1 | Request headers after Connection and URI prerequisites and before request commit. | One request-header decision. |
| P2 | Request-body ingestion. | Exactly one request end-of-stream decision. |
| P3 | Response headers before response commitment while the original status remains mutable. | One response-header decision. |
| P4 | Bounded response-body ingestion. | Exactly one response end-of-stream decision. |

Connection, URI, and Logging remain native lifecycle prerequisite or epilogue
operations, not a fifth business phase. P2/P4 receive zero or many chunks but
have exactly one EOS finalization.

A disruptive URI prerequisite may terminalize the transaction before P1 has
started. The adapter records the bounded, rule-correlated terminal decision
without fabricating a P1 begin/complete transition; its adapter event must
identify that pre-P1 provenance explicitly. A subsequent request-header
decision is P1 only when P1 actually began and completed.

## Canonical bounded state and FSM

<code>msconnector_transaction_contract</code> is the canonical metadata-only
record. It contains a bounded transaction ID, connector ID, host/host-instance
ID, current/last phase, request and response metadata, body counters and
limits, engine decision, rule ID, host action, Safe/Strict mode, error class,
timestamps, response-commit state, and cleanup state. It contains no body
pointer or payload; chunks are borrowed only for their callback.

The Common contract does not retain a zero timestamp as a lifecycle value. If
an adapter has no clock value for a transition, the contract supplies a
nonzero local value and clamps it to the latest retained lifecycle timestamp.
This keeps receipt timestamps nondecreasing without reinterpreting an explicit
adapter timestamp or claiming clock synchronization between different hosts.

The contract keeps two deliberately separate bounded identifiers. Its
<code>transaction_id</code> is the byte-identical, validated host/request
correlation key used by MRC1 and response companions. Its
<code>canonical_transaction_id</code> is generated once per Common process as
<code>txc-&lt;monotonic-time&gt;-&lt;atomic-sequence&gt;</code>; it is unique for
contract ownership even when a host reuses the same external request ID. An
atomic sequence overflow fails transaction creation rather than falling back
to a lossy or shared identifier. Neither identifier is sent across the
response-observer boundary.

Admission is fail closed. A supplied transaction ID that cannot be copied as a
bounded canonical ID (for example empty, control-byte, surrounding-whitespace,
or oversized input) does not allocate a native engine transaction and leaves
no usable legacy phase state. The legacy `NULL` state-ID compatibility input is
deliberately distinct: it creates the internal bounded
`common-transaction` contract ID without normalizing any invalid supplied ID.
After a failed admission, legacy phase, bookkeeping, metadata, decision, and
cleanup calls reject rather than treating an all-zero record as a transaction.

An adapter profile's route ID (for example <code>ext_authz</code>) selects the
implementation; it is not the transaction's host ID. Common Runtime derives
the latter from the trusted mapped server endpoint as
<code>&lt;route&gt;@&lt;server-address&gt;:&lt;port&gt;</code>, falling back only to the
stable route ID when the host supplies no endpoint. Transaction and host IDs
remain internal metadata. A request-only service returns only
<code>x-msconnector-response-handle</code>: a server-generated, 32-byte random
capability encoded as 64 lower-case hexadecimal characters. It is not derived
from <code>x-request-id</code>, and neither transaction nor host ID crosses the
response-observer boundary.

The explicit FSM allows only P1 -> P2 -> P3 -> P4. P2/P4 stay active from the
first chunk through EOS. It rejects duplicate, skipped, late, conflicting,
terminal, and cleaned phases. Cancel, timeout, body/header/event-limit, and
connector/protocol errors become terminal decisions. Early cleanup first records
a terminal <code>connector_error</code> with
<code>cleanup_incomplete</code>, then marks the transaction cleaned; it is
never silently accepted.

For P2/P4, a successful body append is ingestion into the already active
phase, not a new phase start: later bounded chunks resume that phase and only
the matching finish operation produces EOS. An adapter borrows a chunk only for
the Common call. Where its host can forward body data, it forwards the bounded
chunk immediately after the successful append; neither Common nor the adapter
keeps a cross-callback full body. The first successful next-stage write or host
commit is the monotonic P4 commitment boundary. An EOS-only result after that
boundary is late: Safe records <code>log_only</code>; an admitted Strict
profile may use an actual, host-proven abort, but must not fabricate a
replacement HTTP status.

Runtime-backed adapters apply an explicit Strict admission gate before serving
traffic. A <code>phase4_mode=strict</code> runtime rejects a selected profile
whose immutable <code>strict_post_commit_action</code> capability is zero. That
is a startup configuration failure, not a late <code>log_only</code> fallback.
The capability is set only for a source-backed host action; a direct adapter
that does not use the Common Runtime must enforce the same condition at its own
startup boundary.

Header aggregates are capped at 256 fields and 65536 bytes. Body limits must
be nonzero. The response-companion registry has 64 fixed slots and a monotonic
TTL (30 seconds by the supplied request-only adapters). It creates a random
opaque handle at handoff, atomically permits exactly one claim, and removes an
entry on expiry, cancel, release, or shutdown. A missing, expired, malformed,
or replayed handle yields the same bounded correlation failure to the peer;
the implementation does not disclose which condition matched. Event JSONL
remains metadata-only and has a separate 16384-byte limit.

An exact P2 body-limit rejection is a canonical, rule-ID-free deny: it uses
HTTP 413, emits the bounded <code>MSCONN_EVENT_BODY_LIMIT</code> event identity,
carries no redirect, and terminalizes the transaction. The host action must be
the same HTTP 413 deny; an earlier phase's rule correlation must not be
inherited.

A live handoff records <code>handed_off</code> until the trusted observer
atomically claims it for P3; only then can companion-only P3/P4 advance the
FSM. Registry locks protect only short ownership changes, not native engine
work. Common Runtime serializes its shared native engine and integrity-chain
event state independently. On expiry, cancel, release, or shutdown the entry
is detached before native cleanup; shutdown refuses to free an in-use entry,
so the observer must quiesce first. The private <code>MRC1</code> UDS protocol
uses a fixed 12-byte frame header, bounded frames, a required first
<code>CLAIM</code>, P3 headers, monotonic commit, bounded P4 chunks, one EOS,
then outcome and release/cancel. It carries only the opaque handle at CLAIM.
Its generic payload maximum remains 65536 bytes. Only
<code>RESPONSE_HEADERS</code> may use a payload of up to 66630 bytes, so the
fixed MRC1 fields and up to 256 field-length prefixes can carry Common's
65536-byte logical name/value aggregate. This does not raise the logical
header limit: decoders still reject more than 256 fields or more than 65536
aggregate name/value bytes, and every other opcode remains limited to 65536
payload bytes.
The MRC1 family currently requires protocol version 2. Its one-byte
<code>CANCEL</code> payload is a canonical terminal cause:
<code>0=client_cancel</code>, <code>1=upstream_disconnect</code>,
<code>2=connector_error</code>, <code>3=protocol_error</code>,
<code>4=engine_timeout</code>, <code>5=engine_unavailable</code>, and
<code>6=invalid_engine_response</code>. Values 0 and 1 retain their lifecycle
meaning; values 2--6 invoke the Common failure path with that exact error
class. An observer/listener version mismatch, an unknown cause, or an observer
that cannot speak v2 is fail closed: there is no v1 or capability fallback.
An unexpected private-socket EOF is a connector error, never guessed to be an
upstream disconnect; a real upstream disconnect must be sent explicitly as
cause 1 before the peer closes.
An MRC1 result carries the canonical decision's HTTP status, not an
acknowledgement status: successful <code>allow</code>, <code>log_only</code>,
<code>drop</code>, and <code>connection_abort</code> may therefore carry
<code>0</code> when no HTTP response exists. A receiver must accept precisely
those statusless success cases for a decision-bearing operation and reject a
statusless successful <code>deny</code>, <code>redirect</code>,
<code>error</code>, or <code>unsupported</code> decision. The sole protocol
exception is the successful <code>CANCEL</code> or <code>RELEASE</code> ACK:
it has no engine decision and therefore uses the statusless <code>error</code>
sentinel. An adapter may accept that sentinel only for those two cleanup
operations, never for P1--P4. Nonzero MRC1 statuses are canonical HTTP
statuses from <code>100</code> through <code>599</code>, never an
acknowledgement code or an arbitrary three-digit value.
The Common listener requires an absolute, canonical, owner-only parent
directory, creates a 0600 socket, records its exact inode for cleanup, and on
Linux checks <code>SO_PEERCRED</code> for every peer; unsupported identity
platforms fail closed rather than falling back to TCP or mode bits alone.

A successful MRC1 handoff also requires that this private listener is live at
the moment ownership moves. <code>msconnector_response_companion_transport_ensure_running</code>
is the shared precondition: after a terminal <code>poll</code> or
<code>accept4</code> exit it joins and cleans the prior listener before it
starts a fresh private socket. Envoy ext_authz and Traefik forwardAuth cannot
treat a cached ready flag as proof, and the direct HAProxy SPOE/SPOP handoff
uses the same precondition before backend admission. An incomplete cleanup or
failed restart is a fail-closed connector error: no opaque handle is issued,
no transaction is handed off, and no transport, version, or capability
fallback is allowed.

## Uniform decisions

| Decision | Host action | Event type | Rule ID | Failure policy | Cleanup |
| --- | --- | --- | --- | --- | --- |
| Allow | allow | <code>allow</code> | none | none | normal completion |
| Block | deny | <code>rule_block</code> | required | fail closed | terminal then cleanup |
| Redirect | redirect | <code>rule_redirect</code> | required | fail closed | terminal then cleanup |
| Rate limit | rate-limit | <code>rule_rate_limit</code> | required | fail closed | terminal then cleanup |
| Log-only / Safe | log-only | <code>log_only</code> | optional | fail open | normal or terminal cleanup |
| Enforce / Strict | runtime-backed adapter: reject startup without a proven post-commit host action; otherwise deny pre-commit and use only the proven post-commit action | <code>enforce</code>; startup rejection has no transaction event | required | fail closed | terminal then cleanup |
| Engine timeout or unavailable | deny in Strict before commit, otherwise log-only | <code>engine_timeout</code> / <code>engine_unavailable</code> | none | mode/commit dependent | terminal then cleanup |
| Invalid engine response | deny in Strict before commit, otherwise log-only | <code>invalid_engine_response</code> | none | mode/commit dependent | terminal then cleanup |
| Body or resource limit | configured bounded rejection before unsafe forwarding (normally HTTP 413 for a body limit) | <code>body_limit</code> | none | fail closed | terminal then cleanup |
| Connector/protocol/early-cleanup error | deny in Strict before commit, otherwise log-only | <code>connector_error</code> / <code>protocol_error</code> | none | mode/commit dependent | terminal then cleanup |
| Client cancel / upstream disconnect | abort affected connection or stream | <code>client_cancel</code> / <code>upstream_disconnect</code> | none | stop I/O | terminal then cleanup |

A disruptive rule decision without a bounded rule ID becomes
<code>invalid_engine_response</code>, never Allow. A post-commit host must not
invent a new status or silently upgrade Safe to enforcement.

## Native intervention normalization

When a native adapter receives a disruptive <code>msc_intervention</code>, it
normalizes the status before recording the Common decision and before invoking
the host sink. This canonicalizes one native rule decision; it is distinct from
the <code>invalid_engine_response</code> error path for an engine, connector,
or protocol failure.

| Native intervention form | Canonical status |
| --- | --- |
| Nonempty redirect URL and a 3xx status | Preserve that 3xx status. |
| Nonempty redirect URL and any non-3xx status | HTTP 302. |
| No redirect URL and an allowed block status | Preserve that block status. |
| No redirect URL and every other status | The configured allowed <code>default_block_status</code>, otherwise HTTP 403. |

Adapters still validate and request-own any engine-provided redirect URL before
native cleanup. They must not expose an empty URL as a redirect, return a
successful or arbitrary 3xx status for a status-only intervention, or bypass
the normal Safe/Strict and response-commit policy after this canonicalization.

## Ten logical connector solutions

| Solution | P1/P2 route | P3/P4 route | Current boundary |
| --- | --- | --- | --- |
| Apache | native module | native filters | Direct contract; each bounded pre-EOS response-data bucket is appended once and immediately passed to the next filter. The terminal EOS fragment finishes P4 exactly once; a later result follows the common post-commit policy. |
| NGINX | native access/body callbacks | native header/body filters | Direct contract; file-backed request bodies contribute their actual file offset to P2's bounded counter. File-only P4 buffers are read into one reusable 32 KiB scratch range and appended exactly once; malformed or short file reads fail closed before forwarding. |
| HAProxy HTX | HTX filter | HTX filter | Direct profile <code>haproxy-htx</code> / <code>htx-filter</code>. |
| HAProxy SPOE/SPOP | SPOP notifications | mandatory native-HTX response companion | Common profile <code>haproxy-spoe-spop</code> / <code>spoe-spop-agent</code> routes P1/P2 directly and P3/P4 through the companion. Raw SPOP notifications, including optional response headers, are not a response DATA/EOS boundary; native-HTX is selected only through an explicit fail-closed private-UDS/peer-identity/body-limit gate and has current-source local harness evidence. |
| Envoy ext_authz | authorization service | mandatory MRC1 response companion | Same live Common/native transaction is retained behind a single-claim opaque handle; the Envoy response observer supplies P3/P4. |
| Envoy ext_proc | ext_proc CGo Common bridge | ext_proc CGo Common bridge | Direct streaming profile <code>envoy-ext-proc</code> / <code>ext_proc</code>. |
| Traefik forwardAuth | authorization service | mandatory MRC1 response companion | Same live-transaction, fixed-capacity, TTL-bounded opaque-handle P3/P4 model as ext_authz; the response-observer middleware supplies P3/P4. |
| Traefik Native UDS | native middleware | native middleware | Direct profile <code>traefik-native-uds</code> / <code>native-traefik-middleware</code>. |
| lighttpd Stock | traffic-owning Common Runtime sidecar | same sidecar | Canonical profile `lighttpd-stock` / `stock-lighttpd-sidecar`: a private loopback HTTP/1.1 sidecar owns the complete exchange, immediately forwards each bounded P4 chunk after append, and finishes P4 once at EOS. The native `stock-lighttpd` route is an explicit noncanonical P1/P3 compatibility translation, never a fallback. |
| lighttpd Patched | patched request-range hook | patched response-entity hook | Direct profile <code>lighttpd-patched</code> / <code>patched-native-lighttpd</code>. |

<code>ext_authz</code> and <code>forwardAuth</code> are each one logical
connector solution. The companion retains the same native rule transaction,
not a reconstructed P1/P2 snapshot, so P3/P4 evaluate with the same request
context. The authorization response handle may travel only along the local
response-observer chain. For Envoy, that is its internal upstream-header path
to the immediately following observer, which strips the header before the real
application upstream; Traefik keeps it within the local observer chain. Envoy uses
the supplied private-UDS ext_proc response-observer process; Traefik uses the
supplied local response-observer middleware after forwardAuth. Both observers
send P3 before host commitment, P4/EOS after it, record a late result only as
log-only, and close/cancel on malformed results or cleanup failure. A
configuration that omits either observer has no P3/P4 coverage and is a
configuration error, not a reason to label P3/P4 as not-applicable. The
provided Envoy harness requires the observer binary and its owner-only socket;
the live filter is fail-closed when that observer cannot serve a request.

The source includes the Common MRC1 listener and the Envoy/Traefik observer
artifacts and wiring templates. They are source/component evidence, not a
claim that a particular deployed Envoy or Traefik instance has loaded the
templates or produced live host traffic. Operators must create the private
parent directory, wire the handle header only along the local chain, start the
response observer before the request-only authorization service, and quiesce
the observer and companion before runtime shutdown.

The Envoy deployment additionally carries a fixed local
<code>x-msconnector-terminal-authz: 1</code> marker on a terminal ext_authz
P1/P2 reply. The response observer permits a response-only callback only when
that exact marker is present and no observer request phase was seen; it strips
the marker before the client. A missing handle alone is always fail-closed.
Before response commitment, neither supplied Envoy nor Traefik response
observer has a demonstrated stream-reset primitive through its host adapter:
a statusless <code>drop</code> or <code>connection_abort</code> is therefore
recorded as the actual fail-closed HTTP deny and returned as HTTP 503, never
reported as a reset or silently converted to HTTP 200. After commitment, the
canonical Safe/log-only late-outcome rule remains in force.

Stock lighttpd is different from those request-only protocols: the selected
`stock-lighttpd-sidecar` is the traffic owner. It accepts only explicitly
configured literal loopback (`127.0.0.1`) HTTP/1.1 connections, keeps one
bounded worker exchange, and forwards to the private unchanged Stock backend.
The worker owns P1--P4 and cleanup in one process, so no cross-process
correlation handle or TTL registry is needed. The native Stock module route
remains an explicit P1/P3-only compatibility translation and must not be
silently enabled beside, or substituted for, the sidecar. Sidecar event JSONL
contains only bounded metadata and counters; request or response body payloads
never enter events.

## P4 implementation and evidence matrix

This matrix records the ten logical solutions, not a replacement host profile.
<code>implemented</code> means that the shared contract is present in the
selected source/adapter boundary; <code>verified</code> means that this task
actually ran the stated bounded component check; <code>pending</code> means
that direct host/runtime evidence is still required. It does not promote source
evidence to a production claim.

| Logical solution | P4 state | Current evidence and boundary |
| --- | --- | --- |
| Apache | implemented | Progressive pre-EOS filter forwarding and one EOS finish are source-wired and covered by the focused wiring test; no current native Apache host run is claimed. |
| NGINX | implemented | Its native filter appends NGINX's memory-authoritative current range or bounded file-only scratch chunks, forwards the chain without a connector-owned full response, and finishes P4 at actual EOS. A malformed or short file read fails closed before forwarding; fresh native-host runtime evidence is pending. |
| HAProxy HTX | implemented | The native HTX profile maps current body blocks and HTTP end-of-message to the shared contract; strict post-commit wire behavior remains separate host evidence. |
| HAProxy SPOE/SPOP | implemented | The logical solution requires the mandatory private HTX P3/P4 companion. Bare SPOP is unsupported for response DATA/EOS and is never a P4 fallback. |
| Envoy ext_authz | implemented | The logical solution requires its single-claim response observer. Bare ext_authz is unsupported for upstream response phases and is never marked not applicable. Its runtime rejects Strict admission until a post-commit host action is proven. |
| Envoy ext_proc | implemented | The streamed ext_proc profile maps response headers, bounded body chunks, and EOS to the shared contract. Its runtime rejects Strict admission until a post-commit host action is proven. |
| Traefik forwardAuth | implemented | The logical solution requires its response-observer middleware. Bare forwardAuth is unsupported for upstream response phases and is never marked not applicable. Its runtime rejects Strict admission until a post-commit host action is proven. |
| Traefik Native UDS | implemented | The direct native UDS profile owns P3/P4 and EOS under the shared contract. Its runtime rejects Strict admission until a post-commit host action is proven. |
| lighttpd Stock | verified | The traffic-owning private-loopback sidecar's actual 11-test component run covers multi-chunk P2/P4, EOS, Safe/Strict late behavior, limits, cancel, cleanup, and reuse; it is not an unmodified native Stock-host run. |
| lighttpd Patched | pending | The patched identity-entity source/build path has the shared hook contract, but no current selected host P4 runtime evidence is attached. Its runtime rejects Strict admission until a post-commit host action is proven. |

The raw response-blind protocol boundaries (SPOP, bare ext_authz, and bare
forwardAuth) are <code>unsupported</code> for P4 rather than
<code>not_applicable</code>. Their mandatory companions make the listed
logical connector solution P1--P4 complete without reconstructing a
transaction or silently falling back.

## Safety and validation boundary

- Header, body, registry, and event limits fail rather than retain unbounded state.
- Event JSONL contains counters and bounded metadata only, never body payloads.
- Event JSONL and its corresponding integrity hash redact a non-empty literal
  query as `?<redacted>` while preserving the raw URI for WAF processing.
  Historical event or audit logs may still contain query secrets; restrict
  access and rotate them according to the retention policy.
- P3 completes before response commitment; commit is monotonic and rejected after finish.
- Named integration modes resolve to an exact profile; unknown modes do not fall back.
- All error, cancel, timeout, expiry, and normal paths use canonical cleanup.

The focused contract test exercises the ten profiles, valid and invalid
sequences, duplicate and missing phases, body/header/event-limit policy,
invalid decisions, cancel, timeout, cleanup, parallel registration, and reuse.
The live companion component test additionally exercises ownership handoff and
claim, P3/P4, TTL expiry, cancel, parallel transactions, stream reuse, and
shutdown cleanup. Native host compilation and live transport evidence remain
separate from these unit/component checks.

## Related references

- [Common design](design.md)
- [Architecture](../../docs/architecture.md)
- [Envoy connector guide](../../docs/connectors/envoy.md)
- [Traefik connector guide](../../docs/connectors/traefik.md)
- [lighttpd connector guide](../../docs/connectors/lighttpd.md)
