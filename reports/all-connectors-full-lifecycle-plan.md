# All connectors: low-latency full-lifecycle plan

**Language:** English | [Deutsch](all-connectors-full-lifecycle-plan.de.md)

## 2026-07-12 current implementation and evidence update

The implementation state below is historical where it calls the selected
Traefik and Envoy routes passthrough-only or calls HAProxy observer-only. The
current selected paths are native Traefik middleware plus a persistent local
UDS Common/libmodsecurity service, Envoy `ext_proc` plus its CGo Common bridge,
and the native HAProxy HTX filter with P1/P3 replies. The patched lighttpd
host has P1/P2/P3 evidence but no decoded-entity response-body hook.

Fresh Apache and NGINX native-host runs separately record P4 Safe `log_only`
and Strict connection-abort behavior. NGINX HTTP/2 is not selected: the
managed build's `nginx -V` lacks `--with-http_v2_module`. All unobserved
behavior remains `NOT EXECUTED`; a source route, build, or synthetic harness
does not substitute for causal host evidence.

## 2026-07-11 implementation-status update

This plan retains the pre-implementation source-audit baseline below, with the following bounded
implementation update.  None of these items promotes a connector to verified
full-lifecycle, low-latency, or production status; the older absence claims
are superseded only as described here.

- `ci/resolve-runtime-paths.py` centralizes validated per-connector evidence,
  build, run, and log roots below `VERIFIED_RUN_ROOT`, with a shared
  `cache-v2/shared` component cache.  It prevents cross-connector root/cache
  inheritance but is not connector runtime evidence.
- Apache and NGINX have real native-host P3 deny/redirect exercises (403/302)
  and synchronized first-byte-before-EOS probes. These bounded results do not
  verify their complete lifecycle matrices.
- The HAProxy 3.2.21 HTX overlay has a real native observer exercise: P1--P4
  rule paths are observed while client-visible status remains `200`.  The
  observer is deliberately nonpromoted and makes no enforcement, late-action,
  first-byte, or no-full-buffer claim.
- Envoy now has a real streamed `ext_proc` listener/service exercise.  It is
  passthrough and nonpromoted, with no Common runtime bridge or rule
  evaluation, so it is not P1--P4 evidence.
- Traefik's compatibility `forwardAuth` binary/config/start path is repaired.
  The full-lifecycle profile separately selects the native middleware in a
  pinned local-plugin host: plugin loading and router traffic are observed,
  but `PassthroughEngine` has no Common/libmodsecurity bridge and promotes no
  P1--P4, late-action, first-byte, or no-buffer capability.
- lighttpd now builds a pinned patched core with the matching module and has a
  P1 smoke exercise.  Its harness uses `response_body_mode=none`; P4 was not
  executed and no response-body-related capability is promoted.

Compatibility profiles remain separate from native-host evidence and cannot
complete this plan on their own.

The source-audit matrices and connector-finding sections below preserve the
historical snapshot. Their absence statements are retained for design
provenance and are not current claims about the HTX observer, the separate
Envoy `ext_proc` transport path, the native Traefik local-plugin host probe,
or the patched lighttpd host; the bounded current status for those paths is
above.

## Historical technical summary

This is a source-audit plan, not runtime evidence.  The six checked-in
integrations do not yet provide one verified common full-lifecycle path.  The
closest source paths are the native Apache and NGINX filters, but their
Phase-4 results still need real-host, first-byte-before-end evidence.  HAProxy
has deliberately disabled its former `http-response wait-for-body` response
sample; the selected SPOP path has no response-body route, so Phase 4 is
`not_implemented` there.  The pinned HAProxy 3.2.21 source does expose a
native HTX filter route with payload and EOS callbacks. An optional checked-in
observer overlay uses that route for bodyless requests only, but the selected
SPOP integration does not activate it or correlate a complete lifecycle. Envoy
`ext_authz` and Traefik `forwardAuth` are deliberately request-side protocols;
they are response-unavailable in those *selected modes*, not evidence that an
`ext_proc` or native-middleware route is impossible.  The native lighttpd
module explicitly disables both body modes.

The required Phase-4 wording is **incremental body ingestion; end-of-stream
Phase-4 evaluation**.  `msc_process_response_body`/the Common finish operation
is the evaluation boundary.  Nothing in this plan treats an append call as
per-chunk rule evaluation.

## Audit scope and evidence boundary

The audit inspected the branch `feature/all-connectors-no-crs-baseline`, the
connector capability declarations, host glue, harnesses, Common SDK, and the
embedded framework.  It did not run a new connector runtime.  Consequently,
source wiring is classified `implemented_not_asserted`, never `verified`.

The initial repository heads inspected were:

| Repository | Branch | Initial inspected head |
| --- | --- | --- |
| Superproject | `feature/all-connectors-no-crs-baseline` | `062e5ef` |
| Framework submodule | `feature/all-connectors-no-crs-baseline` | `3e7a085` |

The report also records the working-tree Common lifecycle and cache changes
being made on that same branch.  A later runtime run must attach its own
manifest, result, JSONL event, inventory, and host logs before any capability
is promoted.

## Status vocabulary

| State | Meaning in this report |
| --- | --- |
| `implemented_not_asserted` | Source/configuration has a real path, but no matching canonical host result proves the behavior. |
| `configured_not_exercised` | A configuration advertises a path, but the available harness has not exercised it. |
| `not_implemented` | The required path, hook, protocol, or evidence mechanism is absent or violates the requested model. |
| `unsupported_by_host_model` | The *current selected integration mode* cannot observe that phase. It is not a claim about every integration mode offered by the host. |
| `not_applicable` | A measurement has no response path to measure in the selected request-only mode. |

`UNSUPPORTED` is not a passing result, and a mapper, self-test, configuration
field, or direct Common call is not runtime evidence.

## Historical source-audit architecture matrix

The matrix distinguishes the existing path from the route that must be built
or completed. Values describe the historical pre-update audit state, not a
delivery claim or a current implementation assertion.

| Connector | Current path | New full-lifecycle path | P1 | P2 | P3 | P4 | No full response buffer | Safe | Strict | Required host patch |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Apache | Native `httpd` hooks plus input/output filters. Current buckets are inspected and passed onward in the same invocation; P2/P4 finish at EOS. | Adopt the Common chunk/finish contract at those boundaries and prove the host transport behavior. | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` (EOS evaluation) | `implemented_not_asserted` from source only | `implemented_not_asserted` | `implemented_not_asserted` | No core patch identified; real host evidence is still required. |
| NGINX | Native access, header, and body filters. Response buffers are appended per chain element and `msc_process_response_body` is called on `last_buf`; request callback remains buffered. | Retain the response filter topology, add a real request-chunk route, adopt Common chunk/finish, and prove transport behavior. | `implemented_not_asserted` | `implemented_not_asserted` (buffered only) | `implemented_not_asserted` | `implemented_not_asserted` (EOS evaluation) | `implemented_not_asserted` from source only for response | `implemented_not_asserted` | `implemented_not_asserted` | No response core patch identified; request-stream API/order and all host behavior need tests. |
| HAProxy | SPOE/SPOP agent; optional response headers, with the former response-body sample deliberately disabled. | Extend the optional source-linked HAProxy 3.2.21 HTX observer from bodyless requests to a complete correlated transaction, not a `wait-for-body` sample. | `implemented_not_asserted` | `implemented_not_asserted` (one bounded request sample) | `implemented_not_asserted` | `not_implemented` | `not_implemented` (no selected response-body route) | `not_implemented` | `not_implemented` | No core callback patch is needed: native `flt_ops.http_payload`/`http_end` exist. The checked-in observer is nonselected/bodyless-only; complete transaction correlation and host evidence remain missing. |
| Envoy | HTTP `ext_authz` authorization service before upstream. | Connector-owned gRPC `ext_proc` service and Envoy-specific proto mapper; use a supported streamed processing mode. | `implemented_not_asserted` | `configured_not_exercised` (buffered request body) | `unsupported_by_host_model` in `ext_authz`; target is `not_implemented` | `unsupported_by_host_model` in `ext_authz`; target is `not_implemented` | `unsupported_by_host_model` in request-only mode; target proof is `not_implemented` | `unsupported_by_host_model` in `ext_authz` | `unsupported_by_host_model` in `ext_authz` | No `ext_proc` service, generated proto, or config is present; no core patch is justified before a pinned-version API audit. |
| Traefik | External HTTP `forwardAuth` service before upstream. | Native Go middleware in a reproducible custom build, or another implementation that demonstrably preserves streaming interfaces. | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` in `forwardAuth`; target is `not_implemented` | `unsupported_by_host_model` in `forwardAuth`; target is `not_implemented` | `unsupported_by_host_model` in request-only mode; target proof is `not_implemented` | `unsupported_by_host_model` in `forwardAuth` | `unsupported_by_host_model` in `forwardAuth` | No middleware/`ResponseWriter` implementation exists. A custom hook is only required if the pinned public middleware API cannot perform the tested late action. |
| lighttpd | Native module runs URI-clean and response-start hooks and rejects body modes. | Native request-body path plus a pre-socket-write output hook. | `implemented_not_asserted` | `not_implemented` | `implemented_not_asserted` | `not_implemented` | `not_implemented` (no output body path to assess) | `not_implemented` | `not_implemented` | The pinned 1.4.84 public plugin ABI has no output-body/EOS hook; a versioned core/ABI patch covering the write paths is required. |

## Historical cross-connector source findings

### Common lifecycle contract

The Common engine now has explicit borrowed-pointer append/finish operations in
`common/include/msconnector/modsecurity_engine.h`, and the runtime exposes
corresponding `append_*_body_chunk` and `finish_*_body` operations in
`common/runtime/msconnector_runtime.h`.  The runtime records only byte counts,
truncation, response commitment state, and bounded request/response metadata;
it must not retain a connector-owned body pointer after an append returns.

This is `implemented_not_asserted` for the Common API, not connector adoption.
Existing adapters still need to call the API at real host chunk boundaries and
to finish exactly once.  Buffered compatibility helpers remain available and
must not be used to label a path low latency.

### Response compression boundary

No checked-in connector may claim clear-text Phase-4 inspection of compressed
responses. `response_body_decompression` is `not_implemented` for Apache,
NGINX, HAProxy, and lighttpd; it is `unsupported_by_host_model` in the selected
request-only Envoy `ext_authz` and Traefik `forwardAuth` modes. A future host
run must record the observed Content-Encoding and filter/decompression order;
this capability is separate from the initial no-buffer milestone.

### Phase-4 decision model

`common/src/late_intervention.c` has the shared resolver:

- before headers/body commitment: `deny_if_possible`;
- after commitment in `minimal` or `safe`: `log_only`;
- after commitment in `strict`: `abort_connection`.

Connector code may translate `deny_if_possible` to `deny` only when the host
can still change the visible response.  A late event must preserve the actual
rule action in `requested_action`, the transport outcome in `actual_action`,
the original host status, and the visible status.  It must never state that a
post-commit 403 was sent.

### Event and capability gaps

The Common JSONL event model already has bounded metadata fields for action,
requested/actual action, statuses, transport result, and response/commit flags
(`common/include/msconnector/event.h`).  It deliberately has no body payload.
The current Common event schema and serializer also expose bounded,
payload-free `content_type`, `body_bytes_seen`, and
`body_bytes_inspected` fields.  This is source-level contract coverage only:
each connector still needs a real event that proves field population and
payload absence.

The Framework event schema accepts this bounded Common vocabulary. Its ingest
maps Common lifecycle phase labels to canonical rule phases and projects
`response_started` and `body_truncated` into the Phase-4 result model. That is
schema/normalization support, not a connector runtime event.

The Framework capability schema and full-lifecycle catalog now require terms
such as `request_body_incremental_ingest`,
`response_body_incremental_ingest`, `phase4_end_of_stream_evaluation`,
`no_full_response_buffering`, and `first_byte_before_response_end`. All six
current connector manifests are accepted by capability selection with
conservative non-verified states. Do not reinterpret a current `streaming` flag
as proof of per-chunk rule evaluation.

### Configuration parity

Common configuration owns `phase4_mode`, a content-type file, a Phase-4
event-log path, and a Phase-4 body limit. It now also defines
`request_body_limit`, `response_body_limit`, `body_limit_action`, and
`late_intervention_timeout` with validation and merge rules. The latter is a
millisecond adapter budget only: Common has no host timer or cancellation
primitive. Each connector still needs a real host mapping before directive
parity or timeout enforcement can be asserted.

## Historical connector plans and exact blockers

### Apache

`connectors/apache/src/msc_filters.c` now shows a genuine host integration for
request headers, request buckets, response headers, and response buckets. The
input filter appends borrowed request buckets, preserves the original buckets
for Apache, and finalizes Phase 2 once at EOS. The output filter reads only the
current bucket, appends bounded in-scope bytes, passes `bb_in` immediately to
the next filter when EOS has not arrived, and finalizes Phase 4 once at EOS.
It no longer retains `response_brigade` across filter calls.

Plan:

1. Map the native borrowed bucket/one-EOS logic to the Common chunk/finish
   contract without reintroducing connector-owned copies.
2. Track response commitment using the actual Apache state immediately around
   the downstream pass.  Pre-commit deny may use an actual status path; late
   `minimal`/`safe` is log-only and late `strict` is a controlled abort.
3. Exercise direct/proxy response, chunk boundary, keep-alive, cleanup,
   subrequest/internal-redirect/error-document handling before promotion.

### NGINX

`ngx_http_modsecurity_body_filter.c` appends each `ngx_chain_t` buffer with a
configured byte limit and calls `msc_process_response_body` only when
`last_buf` occurs.  It then invokes the next body filter with the original
`in` chain.  That is source evidence for incremental ingestion and EOS
evaluation; it is not a test that the first byte reaches a client before the
upstream ends.

The NGINX request-body callback begins only after NGINX has collected the host
request body. Phase 2 remains source-present as a buffered path, while
`request_body_incremental_ingest` is correctly `not_implemented`.

Plan:

1. Map the existing append/EOS logic to the Common API without copying a whole
   `ngx_chain_t` across filter calls.
2. Keep `phase4_pre_commit_deny` as `not_implemented` unless a real host test
   establishes an uncommitted Phase-4 decision point.  The current body filter
   runs after the response-header path.
3. Preserve real action types: the code already derives `redirect` from a
   3xx intervention rather than hard-coding `deny`.
4. Make config validation, short-write handling, content-type scope, HTTP/2,
   and safe/strict fixtures part of canonical runtime evidence.

### HAProxy

The former experimental response-body sample is deliberately disabled.  The
harness sets `HAPROXY_ENABLE_RESPONSE_BODY=0`, emits no
`http-response wait-for-body` rule, and sends no `res.body` in its SPOE
response message.  Thus the selected SPOP integration has no Phase-4
response-body route.  A synthetic agent response is not a substitute for a
host response-chunk API and cannot satisfy the no-full-buffer/first-byte
contract.

The binding now has borrowed
`haproxy_modsecurity_transaction_append_response_body_chunk` and
`...finish_response_body` primitives with EOS-only Phase-4 evaluation. That is
`implemented_not_asserted` adapter infrastructure, not a host incremental
path: no active SPOP caller supplies response-body chunks or EOS.

The pinned 3.2.21 source audit resolves the host-API question: `flt_ops`
offers `http_payload` and `http_end`, and the response analyzer invokes them
incrementally while forwarding HTX data. The current SPOE filter has no such
events. The checked-in `htx-overlay/` is a source-linked full-lifecycle path
that builds, parses `filter modsecurity-htx`, borrows current request/response
slices, and finishes each body at EOS. Its one-block P2 deny records zero or
one observed upstream requests without proving their ordering; it therefore does not establish
incremental request forwarding. It remains separate from the SPOP harness and
does not promote selected-path capabilities.

Plan:

1. Add split-request-body, limit, and client-cancel probes before claiming
   anything beyond the observed one-block P2 outcome.
2. Add a synchronized first-byte-before-response-EOS probe without a complete
   HTX copy or `wait-for-body`.
3. Keep one finish at each `http_end`; record a late result as log-only until a
   tested abort semantic exists. HAProxy’s response end is after forwarding,
   so do not manufacture a late HTTP status.
4. Model agent failure separately from a Phase-4 late abort. Do not derive
   original/visible status or commitment timing from policy defaults.

### Envoy

The only checked-in service is `envoy_ext_authz_service_main.c`; the template
configures HTTP `ext_authz` and its `with_request_body` block.  There is no
`ext_proc` configuration, protobuf service, generated gRPC code, or
processing-mode selection.  In this existing mode P3/P4/late intervention are
`unsupported_by_host_model`, because authorization completes before upstream
response processing.

Plan:

1. Preserve `ext_authz` as request-only compatibility mode.
2. Add a connector-local `ext_proc` service and mapper; do not place Envoy or
   protobuf types in `common/`.
3. Verify the pinned Envoy API supports a streamed request/response mode before
   choosing it.  Do not default to `BUFFERED` or `BUFFERED_PARTIAL`.
4. Maintain per-request state across gRPC messages; propagate cancel,
   timeout, client disconnect, and clean shutdown.  After commit, report
   log-only or a documented stream reset rather than a fictitious 403.

### Traefik

The only checked-in execution path is
`traefik_forwardauth_service_main.c` plus `forwardAuth` configuration.  It has
no native Go middleware, no custom Traefik build, and no `ResponseWriter`
wrapper.  Therefore it cannot inspect response headers/body or control a
post-commit response.  This is an `unsupported_by_host_model` boundary for
the selected forwardAuth profile and a `not_implemented` full-lifecycle route.

Plan:

1. Keep forwardAuth request-only compatibility mode.
2. Build and test a native middleware against the pinned Traefik version.
   Its wrapper must preserve `http.ResponseWriter`, `http.Flusher`, and each
   optional interface that the underlying writer supports (`Hijacker`,
   `Pusher`, and `io.ReaderFrom` where applicable).
3. Execute Phase 3 in `WriteHeader`, append every `Write` chunk before passing
   it through, and finish Phase 4 at request completion without a recorder.
4. If the tested public API cannot abort a committed HTTP/1.1 or HTTP/2 stream,
   record that precise limit and introduce a versioned custom-build hook only
   after that evidence.

### lighttpd

`module/mod_msconnector.c` registers only URI-clean, response-start, and
request-reset hooks.  During setup it rejects every configuration whose
request or response body mapper contract is not `UNSUPPORTED`; its mapper
sets body data to null/zero.  The pinned lighttpd 1.4.84 public plugin ABI
contains no output-body/chunk/EOS callback: `handle_response_start` is before
header write, while the core writes the response queue directly afterwards.
This is a concrete public-ABI boundary, not an assumption about the module.

The current reset path deliberately does not call `finish_response_body` while
`response_body_mode=none`; the patched-host smoke fails if that finalization is
attempted. With no body chunk ever supplied, this is not Phase-4 body-rule or
output-hook evidence.

Plan:

1. Inspect the request-body queue and implement bounded borrowed request
   chunks plus one Phase-2 finish path.
2. Keep the real `handle_response_start` Phase-3 path and prove a pre-commit
   response-header intervention.
3. Add a narrowly scoped, versioned core/ABI output-filter patch. It must
   cover current chunks, EOS, error/abort, cleanup, and the relevant HTTP/1.x
   and HTTP/2 write paths; a plain plugin cannot supply that boundary.
4. Add reset/cleanup paths for normal, client-abort, upstream-abort, and
   keep-alive reuse without retaining payloads.

## Canonical evidence plan

The Framework’s No-CRS catalog is the required home; it now has a declarative
`full-lifecycle/` subcatalog and its catalog check passes with 104 cases. These
fixtures explicitly remain future / `not_executed_until_real_host`; this is
catalog-contract evidence, not a connector runtime PASS. Capability selection
accepts the current six manifests with conservative states. The subcatalog
covers:

- P1 allow, deny, alternative status, redirect, and transaction ID;
- P2 body marker split across chunks, exact/over limit, truncation, and
  metadata-only event;
- P3 header rule, pre-commit deny/redirect, and original/visible status;
- P4 observed rule, split marker, explicit EOS evaluation, pre-commit only
  where proved, and distinct `minimal`, `safe`, and `strict` late results;
- in/out/missing/charset content types plus invalid and wildcard scope files;
- HTTP/1.1 length and chunked responses, keep-alive, sequential and parallel
  requests, HTTP/2 where supported, and client/upstream abort;
- metadata-only event inspection, including the absence of body and match
  values.

The first-byte proof must use a synchronized upstream: it sends headers and
one body chunk, waits, the client receives that chunk, then the upstream is
released.  A pass requires receipt while the upstream is still unfinished;
wall-clock-only thresholds are insufficient.  Until that fixture produces a
real host result, both `no_full_response_buffering` and
`first_byte_before_response_end` stay unasserted/not implemented as evidence
capabilities.

## Delivery order

1. Use the implemented immutable cache identity, manifest validation, safe
   invalidation, and disposable patch/build trees; prove it again during a real
   host rebuild.
2. Finish and test Common chunk/finish, status, event, and capability
   contracts.
3. Exercise Apache's now pass-through output path.
4. Stabilize and exercise NGINX’s existing incremental/EOS topology.
5. Add Envoy `ext_proc` and Traefik native middleware paths.
6. Add lighttpd request/output hooks, with a patch only if source audit proves
   it necessary.
7. Add a HAProxy native incremental filter route or a minimal versioned patch.
8. Run the capability-selected common catalog and attach artifacts per host.

## Source index

- Common: `common/include/msconnector/modsecurity_engine.h`,
  `common/runtime/msconnector_runtime.{h,c}`, `common/src/late_intervention.c`,
  and `common/{include,src}/msconnector/event.*`.
- Apache: `connectors/apache/src/msc_filters.c` and the Apache harness.
- NGINX: `connectors/nginx/src/ngx_http_modsecurity_{access,header_filter,body_filter}.c`.
- HAProxy: `connectors/haproxy/harness/run_haproxy_smoke.sh`,
  `src/haproxy_spop_diagnostic_runtime.c`, and
  `src/haproxy_modsecurity_binding.c`, plus the nonselected
  `htx-overlay/` source-linked observer.
- Envoy: `connectors/envoy/src/envoy_ext_authz_service_main.c` and
  `config/envoy-ext-authz-smoke.yaml.in`.
- Traefik: `connectors/traefik/src/traefik_forwardauth_service_main.c` and
  `config/traefik-forwardauth-dynamic.yaml`.
- lighttpd: `connectors/lighttpd/module/mod_msconnector.c`.
- Framework: `modules/ModSecurity-test-Framework/tests/cases/no-crs-baseline/`
  and `ci/no_crs_baseline.py`.

## Runtime provisioning status

The cache contract is now `implemented_not_asserted` with unit/contract
evidence: current Framework Python test discovery passes 54 tests.
Superproject test results are tracked separately and are not counted here. A fresh managed
shared-component provision also completed after recovery of a deliberately
interrupted cache root: Expat `R_2_8_2` and libmodsecurity from `v3/master`
were rebuilt and published with `status=complete`. Apache, NGINX, and HAProxy
were intentionally `not_selected`; no connector host binary was built,
configured, started, or used as P1–P4 evidence.
`ci/prepare-runtime-components.py` uses cache schema v2 and keys reusable
entries by resolved upstream commit/source and patch-set hashes, compiler,
linker/build-tool version data, architecture, flags, connector/framework
commits, and build profile. A hit requires matching registry completion,
complete manifest, identity, and expected artifacts.

Missing/incomplete manifests cause a rebuild rather than a manifest repair for
Expat, ModSecurity, Apache, NGINX, and HAProxy. A managed source Git checkout
that is dirty/untracked, has an unexpected origin, fails fsck, or resolves to
a changed moving ref is discarded only below a marked managed cache root,
re-cloned in a temporary directory, checked, and atomically published.
Registry completion stays outside Git worktrees so it cannot make a source
cache dirty. Envoy, Traefik, and lighttpd have no new custom cache pipeline in
this component provisioner; this report makes no equivalent cache-coverage
claim for them.

Per-entry deletion ownership is now source-present: a safe remove requires a
marker registered before entry creation (binding root, path, schema, component,
and cache key), or a complete schema-v2 manifest with a self-consistent
identity/key bound to that exact entry. Existing unmarked entries are rejected,
not retroactively claimed. This remains unit/contract evidence rather than a
host-runtime rebuild result.

## Claims deliberately not made

This plan does not claim production readiness or hardening, runtime or security
verification, CRS verification/completeness, full-matrix verification, zero
latency/overhead, a guaranteed post-commit Phase-4 HTTP status, or that all
connectors are fully verified.
