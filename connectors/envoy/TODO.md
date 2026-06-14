# Envoy Connector TODO

Status: bridge-starter
Runtime status: not-verified

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
- [ ] Envoy SDK/API include paths documented
- [ ] Envoy/proxy-wasm/ext_proc library paths documented
- [ ] production adapter build logs documented

## Phase 3: ModSecurity Bridge

- [ ] libmodsecurity headers located
- [ ] libmodsecurity library located
- [ ] ModSecurity transaction lifecycle implemented
- [ ] real rule evaluation self-test executed

## Phase 4: Envoy Harness

- [ ] Envoy harness implemented
- [ ] harness command documented
- [ ] harness evidence path documented

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
