# Envoy Connector TODO

Status: `compile_verified` ext_authz connector service
Runtime metadata: `minimal_runtime_smoke` / `connector-gap`

Global gate definitions:

- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`

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

## Phase 3: ModSecurity Bridge

- [x] libmodsecurity headers supplied through explicit/Framework environment
- [x] libmodsecurity library linked with local runtime rpath
- [x] ModSecurity transaction lifecycle delegated to `common/runtime`
- [x] targeted real rule evaluation executed through the Envoy ext_authz smoke

## Phase 4: Envoy Harness

- [x] connector-local `runtime-smoke-envoy` entrypoint implemented
- [x] harness command documented
- [x] missing dependencies are BLOCKED while real runtime errors fail
- [ ] root evidence writer consumes the connector-local summary/event artifacts
- [x] real Envoy ext_authz runtime harness implemented
- [x] allowed request returns HTTP 200 in the local targeted smoke
- [x] blocked request returns rule-backed HTTP 403 through Envoy ext_authz

## Phase 5: No-CRS Runtime

- [ ] `make test-no-crs` executed for Envoy scope
- [ ] PASS/FAIL/BLOCKED counts documented

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
