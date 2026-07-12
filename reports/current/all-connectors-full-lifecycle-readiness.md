# All connectors: full-lifecycle readiness

**Language:** English | [Deutsch](all-connectors-full-lifecycle-readiness.de.md)

## 2026-07-12 canonical six-connector HTTP/1.1 core evidence

The selected real hosts completed one shared canonical run:
`six-connectors-core-final-20260712T164725Z-e16e7f1`. All six runners exited
`0`; the compact read-only core checker, first-byte, no-full-response-buffer,
event-privacy, lifecycle, transport, and promotion checks passed. The
aggregate result remains `NOT EXECUTED` only because the extended catalog is
outside this compact core scope. This is real-host Common/libmodsecurity
evidence, not a complete connector-matrix or production claim.

- **Apache — `native-httpd-module`:** P1, P2, P3, P4 rule 1100301 and Safe
  `log_only`, first-byte-before-EOS, no-full-buffer, and cleanup are `PASS`.
- **NGINX — `native-nginx-http-module`:** P1, P2, P3, P4 rule 1100301 and
  Safe `log_only`, first-byte-before-EOS, no-full-buffer, and cleanup are
  `PASS`.
- **HAProxy — `native-htx-filter`:** P1 Allow/403/429, real P2 and P3 403,
  P4 rule 1100301 Safe `log_only`, first-byte-before-EOS, no-full-buffer, and
  cleanup are `PASS`.
- **Envoy — `ext_proc`:** P1 Allow/403, P2 403, P3 403/302 redirect, P4 rule
  1100301 and Safe `log_only`, first-byte-before-EOS, no-full-buffer, and
  cleanup are `PASS`.
- **Traefik — `native-traefik-middleware`:** P1, P2, P3, P4 rule 1100301 and
  Safe `log_only`, first-byte-before-EOS, no-full-buffer, and cleanup are
  `PASS`.
- **lighttpd — `patched-native-lighttpd`:** P1, P2, P3, P4 rule 1100301 and
  Safe `log_only`, first-byte-before-EOS, no-full-buffer, and cleanup are
  `PASS` on the patched Entity-Body path.

All selected P4 Safe outcomes preserve client-visible HTTP 200 after commit;
all first-byte proofs are payload-free real-host observations made while the
upstream was paused before EOS. Strict post-commit enforcement, HTTP/2,
HTTP/3, and extended cases remain separate hardening work.

## Historical implementation-status snapshot (2026-07-11; superseded for selected core paths)

This historical snapshot records work added after the pre-implementation
source-audit baseline. It predates the canonical shared core run above; its
absence, observer, and passthrough statements are not current claims about
the selected core paths.

- **Isolated runtime roots and cache:** `ci/runtime/common/resolve-runtime-paths.py` now
  derives and validates per-connector evidence, build, run, and log roots
  beneath one caller-selected `VERIFIED_RUN_ROOT`.  The shared component cache
  is `cache-v2/shared`; callers no longer implicitly inherit another
  connector's build or evidence root.  This is resolver/cache plumbing, not
  runtime proof for any connector.
- **Apache and NGINX:** both native adapters have real-host Phase-3 deny and
  redirect exercises (403/302) plus synchronized first-byte-before-EOS
  probes. These bounded results do not verify their complete lifecycle
  matrices.
- **HAProxy:** an isolated real HAProxy 3.2.21 HTX overlay can be built and
  exercised as a native HTX observer.  Its four P1--P4 rule paths were
  observed in observer mode, while the client-visible result stayed `200`.
  This is deliberately nonpromoted observation: it proves neither
  pre-commit enforcement nor safe/strict late action, first-byte behavior, or
  no-full-buffering evidence.
- **Envoy:** a real `ext_proc` listener/service path now uses streamed request
  and response processing modes.  The current service is explicitly a
  passthrough, nonpromoted transport exercise with no Common runtime bridge or
  rule evaluation; it is not P1--P4 or enforcement evidence.
- **Traefik:** the `forwardAuth` binary build/config/start dependency path was
  repaired and remains the compatibility profile. The full-lifecycle profile
  separately selects the native middleware in a pinned local-plugin host;
  plugin loading and router traffic are observed, but `PassthroughEngine` has
  no Common/libmodsecurity bridge and promotes no lifecycle capability.
- **lighttpd:** a version-pinned patched core and matching module now build as
  a real host pair, and a P1 smoke path has been exercised.  That harness
  forces `response_body_mode=none`; Phase 4 was not executed.  It therefore
  supplies no response-body, EOS, late-action, first-byte, or no-full-buffer
  promotion.

The native/compatibility distinction remains intentional: compatibility
profiles may be useful diagnostics, but they are not evidence substitutes for
the requested native full-lifecycle routes.

The source-audit matrices and connector-finding sections below preserve the
historical snapshot. Their absence statements are retained for design
provenance and are not current claims about the HTX observer, the separate
Envoy `ext_proc` transport path, the native Traefik local-plugin host probe,
or the patched lighttpd host; the bounded current status for those paths is
above.

## Historical technical summary (pre-core snapshot)

At the time of this source-audit snapshot, no connector had a fresh shared
artifact set proving the selected P1–P4 core together. The canonical evidence
above supersedes that conclusion for the six selected HTTP/1.1 paths only; it
does not establish strict, HTTP/2, HTTP/3, or full-matrix readiness.

The decisive differences are real:

- Apache now passes each current output brigade onward before EOS and finalizes
  P2/P4 once at EOS, but it has no canonical host/first-byte runtime evidence.
- NGINX has source-level incremental body append plus EOS processing, but no
  canonical host evidence for Phase 4, late modes, or first-byte timing.
- HAProxy deliberately disables its former `wait-for-body`/`res.body` sample;
  the selected SPOP path has no response-body or Phase-4 route. The pinned
  native HTX filter API has an optional source-only observer for bodyless
  requests, but it is not selected and is not a complete lifecycle route.
- Existing Envoy `ext_authz` and Traefik `forwardAuth` integrations are
  request-only by protocol.  Their response facets are
  `unsupported_by_host_model` in those modes; the requested alternative modes
  have not been implemented.
- lighttpd’s native module explicitly turns both body paths off.

All outcome labels below are evidence-scoped.  `implemented_not_asserted`
means code exists and **not** that a run passed.  `not_implemented` means the
needed behavior/evidence route is absent.  `unsupported_by_host_model` applies
only to the named selected host mode.

## Historical audit evidence boundary (pre-core snapshot)

The historical audit snapshot is based on repository source, checked-in
capability declarations, harnesses, and Framework catalog logic on
`feature/all-connectors-no-crs-baseline`. No new canonical full-lifecycle
runtime was executed while preparing that snapshot. Later bounded exercises
are described in the update above and do not themselves promote a canonical
full-lifecycle result. Therefore every requested proof in the historical
matrix below is either `NOT EXECUTED`, `UNSUPPORTED` for a selected request-only
mode, or a source-only `implemented_not_asserted` state.

The canonical runtime artifacts required before promotion are:

```text
manifest.json
result.json
results.jsonl
events.jsonl
inventory.json
stdout.log
stderr.log
host.log
```

## Historical source-audit readiness matrix

| Connector | Activated integration | P1 | P2 | P3 | P4 | Late `minimal`/`safe` | Late `strict` | No-full-buffer source state | First-byte evidence | Current blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Apache | Native httpd module and filters | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted`; incremental ingestion, EOS evaluation | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` from source only | `NOT EXECUTED` | No canonical host evidence for first byte, commit timing, late modes, cleanup, or keep-alive. |
| NGINX | Native HTTP module | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted`; incremental ingest, EOS evaluation | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` from source only | `NOT EXECUTED` | Missing canonical real-host event, transport, HTTP/2, and first-byte proof. |
| HAProxy | SPOE/SPOP agent | `implemented_not_asserted` | `implemented_not_asserted` for a bounded request sample | `implemented_not_asserted` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` | Former response sample deliberately disabled. An optional HAProxy 3.2.21 HTX observer handles only bodyless requests, is nonselected, and does not correlate the full transaction. |
| Envoy | HTTP `ext_authz` | `implemented_not_asserted` | `configured_not_exercised` | `unsupported_by_host_model` | `unsupported_by_host_model` | `unsupported_by_host_model` | `unsupported_by_host_model` | `unsupported_by_host_model` for this request-only mode | `unsupported_by_host_model` | No `ext_proc` service, proto mapper, streamed config, or evidence. |
| Traefik | HTTP `forwardAuth` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `unsupported_by_host_model` | `unsupported_by_host_model` | `unsupported_by_host_model` for this request-only mode | `unsupported_by_host_model` | No native middleware/`ResponseWriter` path or custom build evidence. |
| lighttpd | Native `mod_msconnector.so` | `implemented_not_asserted` | `not_implemented` | `implemented_not_asserted` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` | `NOT EXECUTED` | Module rejects body modes; public lighttpd 1.4.84 plugin ABI has no output-body/EOS hook, so a versioned core/ABI patch is required. |

## What the historical source audit established

### Common SDK: `implemented_not_asserted`

The Common engine and runtime now expose a neutral lifecycle with explicit
borrowed body chunks and explicit finish boundaries.  The relevant interfaces
are in `common/include/msconnector/modsecurity_engine.h` and
`common/runtime/msconnector_runtime.h`:

```text
transaction_begin
process_request_headers
append_request_body_chunk
finish_request_body
process_response_headers
append_response_body_chunk
finish_response_body
transaction_finish / transaction_destroy
```

The implementation is honest about libmodsecurity semantics: append ingests a
chunk, while finish calls the native body processor.  A phase-2/phase-4 rule
may therefore be evaluated at EOS.  The pointers are borrowed only for the
call; counters are metadata rather than payload retention.

The Common late resolver is also source-present: post-commit non-strict modes
resolve to `log_only`; strict resolves to `abort_connection`; an uncommitted
response can resolve to `deny_if_possible`.  It remains `implemented_not_asserted`
until each connector invokes it around a real host commitment point.

### Canonical events: source-level contract present

`msconnector_event` has no body payload and contains action, requested/actual
action, rule ID, statuses, transport result, response state flags,
`content_type`, `body_bytes_seen`, and `body_bytes_inspected`. This is source
evidence for a metadata-only canonical event contract. Connector/run-level
field population and payload-absence evidence remains `NOT EXECUTED`.

The Framework accepts the bounded Common event vocabulary, maps Common
lifecycle phase labels to canonical rule phases, and projects
`response_started`/`body_truncated` into its Phase-4 result model. This is
schema/normalization support only, not a connector runtime event.

### Capability and directive model: partial

The Framework schema and its declarative full-lifecycle catalog now require
`*_incremental_ingest`, `phase4_end_of_stream_evaluation`,
`no_full_response_buffering`, and `first_byte_before_response_end`. Capability
selection accepts all six current manifests with conservative non-verified
states. Existing `*_streaming` spelling must not be promoted from an append
call.

Common has `phase4_mode`, a content-type file, event-log path, and a Phase-4
limit. It now also defines merge/validation semantics for
`request_body_limit`, `response_body_limit`, `body_limit_action`, and the
millisecond `late_intervention_timeout` adapter budget. Common does not own a
host timer or cancellation primitive, so timeout enforcement and connector
directive mapping remain unverified rather than implied by this contract.

### Compression boundary

`response_body_decompression` is `not_implemented` for Apache, NGINX,
HAProxy, and lighttpd. It is `unsupported_by_host_model` in the selected
request-only Envoy `ext_authz` and Traefik `forwardAuth` modes. No report or
future result may call compressed response bytes clear-text inspection until a
host path records Content-Encoding and filter/decompression ordering.

## Historical per-connector findings

### Apache

**Source result:** Partial native lifecycle, `implemented_not_asserted`.

The input filter calls `msc_append_request_body`, preserves Apache-owned
buckets, and calls `msc_process_request_body` once at EOS. Response headers
are mapped before response-body handling. The output filter reads and appends
only the current bounded response bytes, calls the next filter with `bb_in`
before EOS, and calls `msc_process_response_body` once at EOS. The prior
cross-call `response_brigade` accumulation is removed.

`minimal`/`safe` log-only and `strict` abort code branches exist.  They are not
evidence of actual response commitment handling, connection reuse behavior,
or client-visible transport. Phase 4 remains source-only until a host run
proves the synchronized first-byte case and all relevant transport behavior.

**Required evidence:** P2 split chunks; P3 before-commit status; P4 rule at
EOS; in-scope/missing content type; safe unchanged response; strict controlled
abort; HTTP/1.1 keep-alive; cleanup; and the synchronized upstream proof.

### NGINX

**Source result:** Closest existing no-full-chain source topology,
`implemented_not_asserted`.

The body filter loops through the current `ngx_chain_t`, calls
`msc_append_response_body` for each allowed buffer, and calls
`msc_process_response_body` only when `last_buf` is seen.  It forwards the
original chain to the next filter rather than retaining a cross-call chain.
This supports the precise source statement *incremental body ingestion with
end-of-stream Phase-4 evaluation*.  It does not prove a client received an
early byte, and it does not prove a phase-4 rule runs per chunk.

The request-body callback starts after NGINX has collected the host request
body. P2 remains source-present as a buffered phase, but
`request_body_incremental_ingest` is `not_implemented`.

The Phase-4 handler maps a 3xx intervention to requested `redirect`, logs a
post-commit safe outcome as `log_only`, and marks strict as a connection error.
These branches need actual HTTP/1.1 and HTTP/2 host evidence.  A Phase-4
pre-commit denial remains `not_implemented`: the current body-filter timing is
after the response-header path and no real uncommitted body decision point has
been shown.

**Required evidence:** config-error test, direct/proxy paths, in/out/missing
content types, redirect as redirect, safe and strict distinct events, short
write error handling, HTTP/2 fixture with in-scope content type, and the
synchronized first-byte proof.

### HAProxy

**Source result:** No selected response-body or Phase-4 path.

The former experimental Phase-4 sample is deliberately disabled:
`run_haproxy_smoke.sh` sets `HAPROXY_ENABLE_RESPONSE_BODY=0`, emits no
`http-response wait-for-body` directive, and sends no `res.body` in a
`check-response` SPOE message. The current SPOP path therefore cannot
establish response-body delivery, Phase-4 evaluation, post-commit
intervention, or the first-byte property. `phase4`, late intervention,
log-only, strict abort, and late status metadata are correctly
`not_implemented` in the current capability file.

The binding now exposes borrowed append-response-chunk and EOS-finish
primitives. This is `implemented_not_asserted` adapter infrastructure only:
no active SPOP caller supplies response-body chunks or EOS. The separate
source-linked HTX full-lifecycle path builds against HAProxy 3.2.21, appends
borrowed request/response data, and finishes both bodies at their EOS. Its
one-block P2 deny records zero or one observed upstream requests without
proving their ordering, so it is not incremental-forwarding, no-buffer, or first-byte evidence. Those
capabilities for the selected SPOP path therefore remain `not_implemented`.

**Required route:** HAProxy 3.2.21 already exposes `flt_ops.http_payload` and
`http_end` through its HTX filter API. The checked-in source-linked filter owns
the P1–P4 transaction, but still needs real split-body, first-byte, and
post-commit transport evidence. It must retain per-stream state only, never
enable `wait-for-body` for P4 blocking, and separate agent failure from an
intentional post-commit abort. A late HTTP status must not be claimed.

### Envoy

**Source result:** Request-only compatibility path.

The Envoy connector’s main program registers the generic HTTP authorization
service with profile `ext_authz`.  The YAML config uses `envoy.filters.http.ext_authz`
and forwards an optional bounded request body.  It has no `ext_proc` service,
gRPC/protobuf artifacts, `processing_mode`, or response message handler.

Thus response headers, response body, Phase 3, Phase 4, safe, strict, and
first-byte behavior are `unsupported_by_host_model` for the activated
`ext_authz` mode. The future `ext_proc` capability is
`not_implemented`, not `unsupported_by_host_model`: no source audit has shown
the pinned Envoy to lack a suitable route.

**Required route:** preserve ext_authz; add and test an `ext_proc` service that
streams request/response body chunks, manages cancellation/timeouts/state, and
uses a verified Envoy reset/abort semantic after commitment.

### Traefik

**Source result:** Request-only compatibility path.

The main program registers a generic HTTP authorization service with profile
`forwardAuth`; the dynamic config selects only `forwardAuth`.  No Go
middleware, `ResponseWriter` wrapper, custom build, flush/hijack handling, or
response hook exists.  The checked-in config also does not enable the
buffering `forwardBody` request option.

P3/P4 and late actions are `unsupported_by_host_model` in forwardAuth, while
the desired full middleware is `not_implemented`.  This distinction is
important: it does not call Traefik itself incapable, and it does not pretend
that an ordinary forwardAuth error can retract bytes already sent.

**Required route:** a pinned native Go middleware that preserves all relevant
writer interfaces, invokes P3 before `WriteHeader`, ingests each `Write` chunk
without a recorder, and has a verified HTTP/1.1/HTTP/2 post-commit strict
strategy or a documented host API boundary.

### lighttpd

**Source result:** Native P1/P3-only module.

The module registers URI-clean, response-start, and request-reset callbacks.
At configuration time it requires both body contracts to be unsupported; its
mapper supplies null/zero bodies.  The real `handle_response_start` route
means P3 is source-present, but no Phase-3 rule result was run in this audit.
There is no request-body hook, output chunk hook, or checked-in versioned
patch. The public lighttpd 1.4.84 plugin ABI has no generic output-body/EOS
callback; `handle_response_start` precedes header write and the core later
writes the queue directly. Therefore P2/P4/safe/strict and first-byte proof are
`not_implemented`, rather than falsely `unsupported_by_host_model`.

The current reset path deliberately does not call `finish_response_body` while
`response_body_mode=none`; the patched-host smoke fails if that finalization is
attempted. Because no response chunk reaches the runtime, this is not Phase-4
body-rule or output-hook evidence.

**Required route:** implement native borrowed request chunks and cleanup, then
add a narrowly versioned core/ABI output-filter hook covering current chunks,
EOS, abort, cleanup, and relevant HTTP/1.x/HTTP/2 write paths. A normal
response-start hook does not constitute a Phase-4 or late-intervention hook.

## Historical tests and provisioning snapshot (pre-core)

The following test/cache discussion predates the canonical core run. It is
retained for provenance and does not describe the current selected core-case
statuses.

The Framework No-CRS catalog now contains a declarative `full-lifecycle/`
subcatalog. Its catalog check passes with 104 cases, while every new fixture is
marked future / `not_executed_until_real_host`. This is
`implemented_not_asserted` catalog-contract evidence, not runtime evidence.
Capability selection accepts all six current manifests with conservative states.
Runtime statuses are `NOT EXECUTED`. The coverage remains within the one result
schema:

| Evidence area | Required current status |
| --- | --- |
| P1/P2/P3/P4 cases and action metadata | `NOT EXECUTED` until host artifacts exist |
| Safe/minimal late log-only | `NOT EXECUTED` for Apache/NGINX; `UNSUPPORTED` only in current Envoy/Traefik request-only modes |
| Strict controlled abort | `NOT EXECUTED` for Apache/NGINX; `not_implemented` for HAProxy/lighttpd; `UNSUPPORTED` only in current Envoy/Traefik request-only modes |
| Synchronized no-buffer/first-byte fixture | `not_implemented` as evidence until a fixture and host result exist |
| HTTP/2 | `NOT EXECUTED` unless a particular host path and artifact prove it |
| Payload privacy | Common event schema is payload-free by design; connector/run-level proof remains `NOT EXECUTED` |

## Cache and provisioning readiness

Runtime cache integrity is a prerequisite for evidence, not a substitute for
it. The cache upgrade is `implemented_not_asserted`: current Framework Python
test discovery passes 54 tests. Superproject test results are tracked
separately and are not counted here. A fresh, managed shared-component provisioning run
also recovered an interrupted cache root and atomically built Expat `R_2_8_2`
and libmodsecurity from `v3/master`, each with a complete manifest and
expected artifacts. Apache, NGINX, and HAProxy were deliberately
`not_selected`; no connector host binary was built, configured, started, or
used as lifecycle evidence. Cache schema v2 records resolved
upstream/source/patch-set hashes, compiler, linker/build-tool version data,
architecture, flags, connector/framework commits, and build profile. A
reusable entry must have matching registry completion, identity, status
`complete`, and expected artifacts.

Missing or incomplete manifests trigger rebuild rather than manifest repair for
Expat, ModSecurity, Apache, NGINX, and HAProxy. Managed source Git checkouts
that are dirty/untracked, have an unexpected origin, fail fsck, or resolve a
moving ref to a new commit are removed only below a marked managed cache root,
rebuilt in a temporary clone, checked, and atomically published. Registry
completion is kept outside Git worktrees, so it cannot create a dirty source
cache. The audit does not authorize cleaning the superproject, Framework
repository, submodule, or an unknown checkout. Envoy, Traefik, and lighttpd
have no new custom cache pipeline in this provisioner, so no equivalent
coverage claim is made for them. No connector capability is promoted merely
because a binary was restored from cache.

Safe removal now requires per-entry ownership: either a marker registered
before creation and bound to the cache root, path, schema, component, and key,
or a complete schema-v2 manifest with a self-consistent identity/key bound to
that exact entry. Existing unmarked entries are rejected rather than being
claimed immediately before deletion. This is source and unit/contract evidence,
not host-runtime evidence.

## Stricter criteria beyond this compact core milestone

These are deliberately stricter capability/production promotion criteria.
They remain beyond the compact functional completion recorded above, including
Strict behavior, limits, keep-alive, and applicable protocol-specific paths.

Each connector may move beyond `implemented_not_asserted` only when one run
proves all applicable items through a real host path:

1. P1, P2, P3, and P4 use host lifecycle hooks rather than mapper/self-test
   shortcuts.
2. Response bodies are incrementally ingested and P4 ends once at EOS.
3. The first permissible response byte reaches the client while the synchronized
   upstream is still paused; no connector-owned complete response buffer exists.
4. Pre-commit action has a real visible status/redirect where the host permits
   it; post-commit requested and actual actions are separate.
5. Minimal/safe prove log-only with unchanged visible status; strict proves a
   documented controlled connection/stream abort where supported.
6. Events are canonical, metadata-only, bounded, and contain the required
   status/action/commit/limit fields.
7. Cleanup, keep-alive, limits, content-type scope, and applicable protocol
   paths are evidenced by the required artifact set.

## Claims deliberately not made

This readiness report does not state production readiness/hardening, runtime
or security verification, CRS verification/completeness, full-matrix
verification, zero latency/overhead, a guaranteed late Phase-4 HTTP status, or
that all six connectors are fully verified.
