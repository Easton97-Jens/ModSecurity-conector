# Transport-hardening and full body-phase audit

**Language:** English | [Deutsch](transport-hardening-audit.de.md)

## Verdict and scope

This is a source/API and local-host audit for the transport-hardening and full
body-phase work on `feature/all-connectors-no-crs-baseline`. It records what
the framework, connector sources, harnesses, and this machine can establish.
It is not a promotion report and it does not convert a configure flag, a
compiled mux, an internal callback failure, or a synthetic event into client
visible HTTP/1.1, HTTP/2, or HTTP/3 runtime evidence.

The framework now has a payload-free protocol-client contract, canonical
protocol provenance, and catalog coverage for negotiation, phase 1--4,
multiplexing, reset, first-byte, and no-full-buffer scenarios. No connector
has produced a newly promoted HTTP/2 or HTTP/3 full-lifecycle result as part
of this audit. Modern-protocol cases therefore remain `NOT EXECUTED` unless a
future real host run meets the complete evidence gate below.

The local client is `curl 8.18.0`: its feature list contains `HTTP2` and does
not contain `HTTP3`. A forced H2/H2C preflight can be attempted on this host;
an H3 probe is `BLOCKED` with `client_http3_unsupported` before it contacts a
connector. That is a client-environment blocker, not a claim that a connector
is unsupported by its host model.

## Audit inputs

The framework conclusions come from
`modules/ModSecurity-test-Framework/ci/protocol_client.py`,
`modules/ModSecurity-test-Framework/ci/no_crs_baseline.py`, the no-CRS
schemas, and the protocol cases in
`modules/ModSecurity-test-Framework/tests/cases/no-crs-baseline/catalog.json`.
The managed NGINX conclusion comes
from `ci/prepare-runtime-components.py`, the framework's
`modules/ModSecurity-test-Framework/ci/prepare-nginx-build.sh`, and
`connectors/nginx/harness/run_nginx_smoke.sh`.
The per-connector boundaries are the six `connectors/*/capabilities.json`
inventories, checked against their native source and harnesses. The local facts
are direct `curl --version`, `nginx -V`, `haproxy -vv`, and Apache module-list
observations; no network probe is represented as having run.

## Evidence contract

The common event and case-result contracts keep the following dimensions
separate:

| Dimension | Canonical values / rule |
|---|---|
| Requested, downstream, upstream, negotiated protocol | `http1`, `h2`, `h2c`, `h3`; downstream and upstream are never inferred from each other. |
| Transport | `tcp`, `tls_tcp`, `quic_udp`; an H3 name alone is not proof of UDP/QUIC traffic. |
| Negotiation | H2-over-TLS needs ALPN `h2`; H3 needs ALPN `h3`, observed QUIC/UDP, a stream ID, QUIC version, and only `quic_connection_id_present`, never a raw QUIC connection ID. |
| Correlation | A promotable result binds connector, integration mode, run ID, transaction ID, rule ID where applicable, phase, stream ID where applicable, and the same bounded `transport_case_id` sent by the managed client. |
| Fallback | `fallback_used` must be false. H3 uses curl `--http3-only`; fallback-capable `--http3` is rejected. |
| Strict late action | On H2/H2C/H3, a post-commit deny must be a client-observed, request-local `stream_reset` with a reset code and `transport_result=stream_reset`; it must not be relabelled as a connection abort. |

`ci/protocol_client.py` always writes these payload-free artifacts for a
managed probe:

- `client-version.txt`
- `client-features.txt`
- `client-command.txt`
- `client-protocol-observation.json`

The client sends response bodies to the null device and does not persist raw
headers, payloads, raw curl stderr, request secrets, or raw QUIC connection
identifiers. Missing stream/ALPN/QUIC provenance produces a non-promoting
result, not a guessed `PASS`.

The status words have deliberately different meanings:

- `not_implemented` means the connector source or owned harness has no such
  integration path.
- `implemented_not_asserted` means a controlled build/configuration surface
  exists, but no matching forced client and real connector evidence exists.
- `NOT EXECUTED` means a catalog/runtime claim has not been established. It
  can coexist with either of the two capability states above.
- `BLOCKED` records an environmental prerequisite, such as this host's lack
  of an HTTP/3-capable curl, without changing a connector capability state.

## Local host audit

| Item inspected | Local finding | Consequence |
|---|---|---|
| curl | `curl 8.18.0`, feature `HTTP2` present, `HTTP3` absent | H2/H2C probes may be prepared; every forced H3 probe is `BLOCKED` locally before a request. |
| NGINX runtime binary | `nginx 1.31.1 -V` has neither `--with-http_v2_module` nor `--with-http_v3_module` | This is an H1 binary. It cannot supply H2/H3 evidence, regardless of module code. |
| HAProxy runtime binary | H2 mux is listed; build reports `-OPENSSL`, `-SSL`, and `-QUIC` | The mux listing is not an H2 TLS/ALPN frontend, and it is not a QUIC/H3 path. |
| Apache runtime modules | Loaded module inventory has no `mod_http2` | The pinned Apache host cannot be used as an H2 connector path. |
| Envoy, Traefik, lighttpd CLIs | `envoy --version`, `traefik version`, and `lighttpd -V` are unavailable on this machine | No local runtime version or protocol claim is made for these hosts. |
| H2 auxiliary clients | `nghttp` and `h2load` are unavailable | They cannot substitute for the managed curl evidence on this machine. |

The managed NGINX build plumbing has explicit `h1`, `h1-h2`, and
`h1-h2-h3-quic` profiles. The latter records a pinned QUIC-capable OpenSSL
input and refuses a quiet H3 fallback build. Those profiles are build
provenance, not a statement that the locally inspected H1 binary negotiated
H2 or H3.

## Phase-0 transport and API matrix

This source/harness matrix records the selected repository integration, not a
general claim about what an upstream server might support. “No API” means that
the pinned connector and its owned harness do not wire a public, request-local
operation; it does not turn a missing test into a host-model impossibility.

| Connector | Protocol | Commit detection | Client-abort API | Stream-reset API | Upstream cancel | EOS callback | Keep-Alive behavior | Current boundary |
|---|---|---|---|---|---|---|---|---|
| Apache native module | HTTP/1.1 selected; no owned H2/H2C or H3 profile | Output filter follows response headers; its strict source branch returns `APR_ECONNABORTED` at response EOS | No raw peer-disconnect driver | No request-local H2/H3 reset is wired | No selected upstream-abort driver | `APR_BUCKET_IS_EOS` finalizes the response body once | One curl process per case; no reuse/follow-up driver | The real synchronized H1 barrier is low-latency-only; it has no transport-case/client correlation |
| NGINX native module | HTTP/1.1 selected; managed H2/H3 build profiles have no client dispatcher | Header/body filters track commitment; `last_buf`/`last_in_chain` are response EOS boundaries | Strict marks a connection error and returns `NGX_ERROR`; no raw client observation | No stream-local H2/H3 reset action is wired | No selected upstream-abort driver | Body filter completes at the actual EOS boundary | One curl process per case; no reuse/follow-up driver | H2/H3 profiles only configure/check a listener and deliberately stop before legacy H1 client dispatch |
| HAProxy HTX | HTTP/1.1 selected; no owned TLS/ALPN H2 or QUIC/H3 frontend | Native filter receives current HTX response payload blocks | No selected raw client-disconnect driver | No proven H2/H3 stream-reset API in the filter | No selected upstream-reset driver | Request/response `http_end` finalize their respective bodies once | No native keep-alive/parallel runner | The one-block P2 deny returns a real client 403 and records zero or one observed upstream requests without proving their ordering; it does not prove incremental forwarding. P4 Safe is `log_only`; Strict has no client-visible abort proof |
| Envoy ext_proc | HTTP/1.1 listener selected; no owned H2 or H3 listener | `ext_proc` receives streamed response callbacks, not a client-commit signal | Opt-in H1 probe closes a real downstream socket after one body byte; its gRPC cancellation stays explicitly unattributed | No downstream H2/H3 reset hook is wired | No selected upstream-reset attribution | Response-body `end_stream` drives Common finish; cancellation has one completion record | The cancel probe also performs a separate healthy follow-up; no modern-protocol reuse run | A gRPC close/cancel is not promoted as a downstream reset or Strict success |
| Traefik native middleware | Cleartext HTTP/1.1 `web` entry point only; no owned H2/H3 profile | Wrapped `http.ResponseWriter` records header/body commitment | `http.Hijacker` is preserved but not used as a post-commit abort claim | No H2/H3 request-local reset API is wired | Read/write failures suppress synthetic EOS but have no upstream-abort attribution | `responseWriter.finish()` emits EOS only for a complete response | Native Safe test proves same-socket HTTP/1.1 follow-up | Public middleware has no verified request-local Strict abort; H2/H3 entry points are absent |
| lighttpd patched native | HTTP/1.x patched path only; no owned H2/H3 profile | Pinned 1.4.84 hook receives borrowed identity entity bytes in `http_chunk`, before HTTP transfer framing | No selected client-abort API/test | No H2/H3 stream-reset hook | No selected upstream-abort case | Entity hook has monotonic offsets and a once-only EOS guard | No modern-protocol keep-alive run | Real P4 host, Strict, gzip/br, HTTP/2 and socket-fault evidence remain unexecuted |

### Connector-specific source/API notes

- **Apache:** `output_filter` is the selected response callback. Its HTTP/1.1
  strict source branch can return `APR_ECONNABORTED`, but no public H2 reset
  operation or version-bound H2/H3 patch is wired. Filter removal and the
  normal finish path are source-level cleanup only; no H2/H3 client effect has
  been observed.
- **NGINX:** the native header and body filters own commitment and `last_buf`
  handling. The present strict path is a connection-error path, not a public
  per-stream reset API; no host patch adds one. Context cleanup is local to the
  request/filter path, while H2/H3 abort/reset and client effects remain
  `NOT EXECUTED`.
- **HAProxy:** the selected native HTX filter uses `http_payload` and
  `http_end`. It has no configured H2/H3 frontend, public reset operation, or
  transport-cancel runner. Its stream detach/end cleanup is not evidence that
  a client saw an H2/H3 reset.
- **Envoy:** the selected API is streamed `ext_proc`. The service finishes its
  own Common transaction on EOS or gRPC-context cleanup, but that context does
  not identify a downstream or upstream reset. No narrow Envoy filter or
  version-bound reset patch is present, so no client reset effect is claimed.
- **Traefik:** the middleware wraps `http.ResponseWriter` and preserves
  `Hijack`, but after commitment it deliberately records `log_only` rather
  than synthesizing an abort or reset. There is no H2/H3 entry-point patch or
  profile; `finish()` is local transaction cleanup, not a client-visible reset
  proof.
- **lighttpd:** the pinned 1.4.84 patch supplies an HTTP/1 identity
  entity-body hook in `http_chunk`, before transfer framing, with
  short-write/EAGAIN deduplication and once-only EOS. It does not establish a
  gzip/br, H2/H3, client-abort, or stream-reset path. A native H2/H3 reset
  would need a separate host API/patch and real client evidence.

## Transport-hardening and body-phase implementation update

The following update records the implemented H1 hardening boundaries without
promoting internal failures to client-visible transport outcomes.

| Connector | Selected additional path | Real observation retained | Deliberately not promoted |
|---|---|---|---|
| Traefik | Native middleware response writer | Incomplete `Write`/`ReadFrom` prevents a false EOS; Safe verifies an H1 same-socket follow-up | HTTP/1 Strict abort and every H2/H3 reset |
| Envoy | Native `ext_proc` H1 cancel probe | Client closes after one body byte; one unattributed gRPC cancellation and an independent healthy follow-up are required | Downstream reset cause and Strict outcome |
| HAProxy | P2 `http_payload`/`http_end`, P4 response payload/EOS | Fresh 3.2.21 overlay build and real non-promoted host smoke; the one-block P2 reply records zero or one observed upstream requests without proving their ordering, and Safe is `log_only` | Incremental request forwarding, post-commit Strict abort, first-byte and client no-buffer proof |
| lighttpd | Pinned 1.4.84 entity-body hook in `http_chunk` | Borrowed identity entity bytes arrive before transfer framing; monotonic offset and one EOS prevent short-write/EAGAIN duplicate inspection | Real P4 host run, Strict abort, gzip/br, HTTP/2 and socket-fault evidence |
| Apache / NGINX | Existing native Phase-4 filters plus synchronized H1 barrier | First byte before upstream EOS remains a real-host low-latency observation | Transport-hardening PASS: no raw client/fault/upstream/keep-alive/parallel driver or causal client IDs |

### Shared transport and lifecycle contract

Common now serializes bounded metadata-only transport state: protocol/stream
identity, connection reuse, disconnect/cancel flags, reset actor/code, timeout
stage, write result, EOS state, and cleanup reason.  The source normalizer has
an explicit allowlist and rejects payloads, body snippets, credentials, full
rule messages, and raw network material.  HTTP/3 connection identity is kept
only as a `sha256:` presence-safe token.

Full-lifecycle runs write payload-free client, upstream, transport, and
cleanup logs; transport observations; connection lifecycle; barrier events;
and a hash-only effective-config manifest.  A barrier event is canonical
event JSONL with connector, integration mode, run ID, transaction, rule,
phase, event/message, and `transport_case_id`; it deliberately has no
catalog-only `case_id` field.  An observation derives its case relation only
from the explicit `transport_case_id`, which a future canonical PASS must
equal.  This prevents fixture-name inference.

The sidecars are inventory, never promotion by themselves.  They remain empty
when an existing event lacks complete client/case/transaction/lifecycle
correlation.  A future transport PASS requires a one-to-one canonical event,
observation, and lifecycle record; bound counters; and, for Strict, a
client-observed post-commit incomplete response plus a healthy independent
follow-up.  The follow-up has its own bounded correlation token and the same
non-reversible target-authority hash; it never reuses the primary token or
persists a raw URL. Diagnostic reset/abort records without a PASS remain
`NOT EXECUTED` rather than being relabelled as success.

## Protocol test infrastructure status

The managed NGINX profile now creates an ephemeral local test CA and a
separately issued one-day leaf certificate with `localhost`/`127.0.0.1` SANs.
The CA key, leaf key, CSR, certificates, and serial file are removed during
cleanup and are never copied into canonical evidence. Its applicability record
also separates `tcp_listener` and `udp_listener` (including their shared
numeric port) and records the latter as `quic_udp`. These are controlled
configuration facts, not negotiated runtime evidence.

The following remain explicit `NOT EXECUTED` gaps:

- `http3_0rtt`: no 0-RTT configuration, replay test, or transaction-semantics
  test is implemented.
- Stream control: the managed curl helper is negotiation-only. It cannot by
  itself issue or observe a stream-level reset/cancel or multiplexed peer
  streams. A sidecar is bounded supplemental provenance, never runtime reset
  proof; reset/cancel/multiplexing cases remain `NOT EXECUTED` until a dedicated
  stream-control client is provisioned.
- Modern protocol probes carry a bounded `transport_case_id` in a redacted
  request header and require the same token in the client observation,
  connector event, and canonical case result. No manually labelled client
  artifact can promote a different transaction.

## Connector/protocol matrix

The matrix states the current source/harness boundary. “Existing H1 evidence”
refers to the separately audited HTTP/1.x lifecycle work; it does not extend
to modern protocols.

| Connector | Existing H1 evidence | H2 downstream / TLS-ALPN | H2C | H3 downstream / QUIC / Alt-Svc | Multiplexing, reset, first-byte, no-buffer | Current modern-protocol execution |
|---|---|---|---|---|---|---|
| Apache native module | Yes, separately audited | `not_implemented`: pinned connector profile does not build/exercise `mod_http2` or an ALPN listener | `not_implemented` | `not_implemented`: no audited H3 module, QUIC listener, or Alt-Svc profile | `not_implemented`; Strict currently models only a connection abort | `NOT EXECUTED`; local module inventory has no `mod_http2` and local H3 client is blocked |
| NGINX native module | Yes, separately audited | `implemented_not_asserted`: managed `h1-h2` profile can build v2, but no forced negotiated run | `not_implemented` | `implemented_not_asserted`: managed H3/QUIC profile and Alt-Svc template exist, but no forced H3 observation | `not_implemented`: no parallel-stream isolation, request-local reset, negotiated first-byte, or no-buffer proof | `NOT EXECUTED`; inspected binary is H1-only, and H3 client is blocked |
| HAProxy HTX | Selected native lifecycle path exists | `not_implemented`: H2 mux availability does not create a TLS/ALPN frontend or owned connector run | `not_implemented` | `not_implemented`: no configured QUIC/H3 frontend or Alt-Svc profile | `not_implemented`: filter has no proven H2/H3 reset or multiplexed isolation path | `NOT EXECUTED`; no qualifying frontend and local H3 client is blocked |
| Envoy ext_proc | Yes, separately audited | `not_implemented`: selected native harness has no TLS/ALPN H2 listener | `not_implemented` | `not_implemented`: no QUIC listener or H3 Alt-Svc profile | `not_implemented`: gRPC stream closure/cancellation is not a client HTTP reset | `NOT EXECUTED`; no owned modern-protocol listener |
| Traefik native middleware | Yes, separately audited | `not_implemented`: native harness renders only a cleartext `web` entry point, with no TLS H2 listener or ALPN configuration | `not_implemented` | `not_implemented`: native harness has no H3 entry point, UDP/QUIC listener, or Alt-Svc configuration | `not_implemented`: no client-visible H2/H3 reset API or multiplexing proof | `NOT EXECUTED`; no connector-owned H2/H3 profile, and the local H3 client is blocked |
| lighttpd patched native | Yes, separately audited | Legacy H2 status is `unsupported_by_host_model`; detailed H2 path is `not_implemented` because the patch rejects H2 | `not_implemented` | `not_implemented`: pinned host has no audited H3/QUIC/Alt-Svc path | `not_implemented`: no decoded modern-protocol response hook, reset, or isolation contract | `NOT EXECUTED`; no supported native modern-protocol path |

All six connectors retain `not_implemented` for protocol-specific transaction
isolation, first-byte-before-response-end, and no-full-response-buffering
until a negotiated H2 or H3 host run supplies the matching evidence.

## Claims deliberately not made

- No H2 or H3 downstream `PASS` is claimed from a build flag, an H2 mux,
  library support, an `Alt-Svc` template, or a protocol name in configuration.
- No H3 negotiation, QUIC/UDP observation, QUIC version, or H3 stream ID is
  fabricated from curl output. The client cannot do so on this host because
  it lacks the `HTTP3` feature.
- No H2C prior-knowledge claim is made for any connector.
- A TCP connection close, Apache/NGINX connection abort, HAProxy filter
  teardown, or Envoy ext_proc/gRPC cancellation is not reported as
  `RST_STREAM`, H3 reset, or a client-visible strict outcome.
- No upstream protocol is inferred from downstream protocol, and no
  connection-level evidence is accepted as multiplexed transaction isolation.
- Existing HTTP/1.1 first-byte and buffering arguments are not promoted to H2
  or H3.

## Required evidence before promotion

For a connector/protocol pair to move beyond `NOT EXECUTED`, a real native
host run must use the forced managed client, preserve the four client
artifacts, and correlate them with bounded connector events. It must prove the
requested and negotiated protocol, transport, required ALPN, no fallback,
stream identity, and phase action. H3 additionally needs a real QUIC/UDP
observation, QUIC version, and presence-only connection-ID evidence. A strict
late deny needs post-commit client visibility, an incomplete response/EOS
state, a request-local reset, and a healthy unrelated stream for the
multiplexing cases. Until then the catalog is an execution plan, not a passed
transport matrix.
