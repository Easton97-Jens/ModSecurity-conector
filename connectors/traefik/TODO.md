# Traefik Connector TODO

Status: minimal_runtime_smoke (forwardAuth request path only)
Runtime status: connector-gap outside the targeted request-header proof

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
- [x] connector-owned forwardAuth service entry point implemented
- [x] C17 compile/link-only connector build implemented
- [x] libmodsecurity include paths supplied explicitly
- [x] libmodsecurity library paths supplied explicitly
- [x] connector service artifact path documented
- [x] config-check and process-only start-smoke separated from build
- [ ] production Traefik build logs documented

## Phase 3: Harness

- [x] `make smoke-traefik` targeted runtime-smoke entrypoint implemented
- [x] harness command documented
- [x] BLOCKED evidence path documented
- [x] common smoke result writer used instead of connector-local JSON writer
- [x] connector-local real Traefik -> forwardAuth -> service harness implemented
- [ ] allowed request returns expected runtime status
- [ ] blocked request returns HTTP 403 through forwardAuth
- [ ] Go plugin remains excluded from Phase 1

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
- [ ] eligible for promotion beyond targeted `minimal_runtime_smoke`
- [ ] current-commit runtime evidence promotes service source beyond `connector-gap`
