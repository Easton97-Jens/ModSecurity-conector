# Envoy Connector TODO

Status: targeted `minimal_runtime_smoke` for the real HTTP `ext_authz` request path
Canonical No-CRS status: `supported_not_verified` / `NOT EXECUTED`

Canonical capability source: `connectors/envoy/capabilities.json`.

Global gate definitions:

- `reports/archive/template-verification-nginx-apache/connector-scaffold-decisions.md`

## Phase 0: Scaffold

- [x] Connector directory created
- [x] README present
- [x] TODO present
- [x] docs present
- [x] harness contract documented
- [x] src placeholder documented
- [x] no local `connectors/envoy/tests` folder

## Phase 1: Origin / Metadata

- [x] `ORIGIN.md` added
- [x] `SOURCE_MAP.json` added
- [x] `metadata.*` added
- [x] upstream Envoy source documented as not selected/imported
- [x] imported upstream license documented as not selected because no upstream
      source was imported

## Phase 2: Bridge Starter Build

- [x] sidecar/HTTP bridge-starter approach documented
- [x] include paths documented for the bridge-starter build
- [x] bridge starter source builds
- [x] bridge CLI self-test runs
- [x] connector-owned C17 ext_authz service builds and links
- [x] Common runtime and real mapper callbacks are linked
- [x] Envoy SDK/API dependencies documented as not required for HTTP ext_authz
- [x] proxy-wasm/ext_proc dependencies documented as outside the selected path
- [ ] production adapter build logs documented

## Separate non-promoted ext_proc full-lifecycle host path

- [x] Pinned official Go Envoy proto/gRPC module and checksum lock added.
- [x] Connector-local `ExternalProcessor` stream service added with per-stream
      state, bounded incremental header/body callbacks, EOS cleanup, and
      cancellation cleanup.
- [x] Non-`BUFFERED` `STREAMED` request/response Envoy template and external
      materializer added.
- [x] Source/unit and tagged CGo tests cover chunks, EOS, cancellation,
      pre-response decisions, response commit ordering, and the conservative
      late-action result.
- [x] Replace `PassthroughEngine` in the normal executable with the reviewed
      Common/libmodsecurity transaction bridge. Source-only protobuf/unit
      builds retain passthrough only when no runtime config can be accepted.
- [x] Validate the pinned Envoy release against the materialized config and run
      a real local HTTP/1.1 P1/P2/P3/P4 Common/libmodsecurity host smoke with
      raw Common rule/action evidence and cleanup evidence.
- [x] Add an opt-in real HTTP/1.1 client-close-after-first-byte probe with an
      exactly-one unattributed terminal completion record
      (`grpc_context_canceled_unattributed` or `grpc_peer_eof`) and a healthy
      follow-up request. Its diagnostic sidecar is intentionally not canonical
      reset or client-cancel promotion evidence.
- [ ] Run HTTP/2, timeout, reset, and first-byte cases; a bridge now exists,
      but these cases remain unverified and must not be promoted.

## Phase 3: ModSecurity Bridge

- [x] libmodsecurity headers supplied through explicit/Framework environment
- [x] libmodsecurity library linked with local runtime rpath
- [x] ModSecurity transaction lifecycle delegated to `common/runtime`
- [x] targeted real rule evaluation executed through the Envoy ext_authz smoke

## Phase 4: Envoy Harness

- [x] connector-local `runtime-smoke-envoy` entrypoint implemented
- [x] harness command documented
- [x] missing dependencies are BLOCKED while real runtime errors fail
- [ ] canonical Framework evidence normalization consumes the connector-local
      summary/event artifacts and writes the shared `result.json` and manifest;
      keep this open until a current canonical run passes validation
- [x] real Envoy ext_authz runtime harness implemented
- [x] allowed request returns HTTP 200 in the local targeted smoke
- [x] blocked request returns rule-backed HTTP 403 through Envoy ext_authz

## Phase 5: No-CRS Runtime

- [ ] `make test-no-crs` executed for Envoy scope
- [ ] PASS/FAIL/BLOCKED counts documented
- [ ] Request-body delivery is exercised before Phase 2 is promoted beyond
      `configured_not_exercised`.
- [ ] `make no-crs-baseline-envoy` produces current canonical evidence.
- [ ] `make evidence-check-envoy` validates the result without treating the
      unsupported upstream response phases as failures or PASS.

## Phase 6: With-CRS Runtime

- [ ] `make test-with-crs` executed for Envoy scope
- [ ] CRS loaded/effective evidence documented
- [ ] PASS/FAIL/BLOCKED counts documented

## Phase 7: Coverage Matrix

- [ ] Phase 1/2/3/4 runtime status documented
- [ ] negative/pass-through status documented
- [ ] audit/log evidence documented
- [ ] RESPONSE_BODY blocking evaluated

## Phase 8: Promotion

- [ ] eligible for `adapter-owned`
- [ ] eligible for `runtime-smoke-verified`
- [ ] eligible for `crs-verified`
- [ ] eligible for more than `partial`

## Canonical Phase-4 architecture boundary

The selected HTTP `ext_authz` integration runs before upstream handling.  The
following source-contract facets are therefore
`unsupported_by_host_model`: `response_body_buffered`, `phase4`,
`phase4_rule_evaluation`, `phase4_pre_commit_deny`, `late_intervention`,
`late_intervention_log_only`, `late_intervention_abort`, and
`late_intervention_status_metadata`.

- [x] Classify selected Phase-4 cases as `UNSUPPORTED` with the ext_authz
      upstream-response boundary, rather than `NOT EXECUTED`.
- [ ] Do not treat request-side 200/403 evidence as response-body, late-action,
      original-status, visible-status, or connection-abort evidence.
- [ ] Reassess these states only for a different Envoy integration that actually
      receives the upstream response; that integration requires new host-path
      evidence and must not reuse ext_authz results.
