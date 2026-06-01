# Traefik Connector TODO

Status: decision-service-starter
Runtime status: not-verified

Global gate definitions:

- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
- `connectors/_template/docs/coverage-decision-matrix.md`

## Phase 0: Scaffold

- [x] Connector directory created
- [x] README present
- [x] TODO present
- [x] docs present
- [x] harness contract documented
- [x] src placeholder documented
- [x] no local `connectors/traefik/tests` folder

## Phase 1: Origin / Metadata

- [x] `ORIGIN.md` added
- [x] `SOURCE_MAP.json` added
- [x] `metadata.*` added
- [ ] upstream Traefik source documented
- [ ] license documented for an upstream Traefik integration

## Phase 2: Build / Local Starter

- [x] build-starter approach documented
- [x] metadata build-starter command executed
- [x] decision-service starter implemented
- [x] decision-service starter command executed
- [x] decision-service local self-test executed
- [ ] production Traefik build approach documented
- [ ] production Traefik include paths documented
- [ ] production Traefik library paths documented
- [ ] production Traefik build artifact path documented
- [ ] production Traefik build logs documented

## Phase 3: Harness

- [ ] Traefik harness implemented
- [ ] harness command documented
- [ ] harness evidence path documented

## Phase 4: No-CRS Runtime

- [ ] `make test-no-crs` executed for Traefik scope
- [ ] PASS/FAIL/BLOCKED counts documented

## Phase 5: With-CRS Runtime

- [ ] `make test-with-crs` executed for Traefik scope
- [ ] CRS loaded/effective evidence documented
- [ ] PASS/FAIL/BLOCKED counts documented

## Phase 6: Coverage Matrix

- [ ] Phase 1/2/3/4 runtime status documented
- [ ] negative/pass-through status documented
- [ ] audit/log evidence documented
- [ ] RESPONSE_BODY blocking evaluated

## Phase 7: Promotion

- [ ] eligible for `adapter-owned`
- [ ] eligible for `runtime-smoke-verified`
- [ ] eligible for `crs-verified`
- [ ] eligible for more than `decision-service-starter`
