# lighttpd Connector TODO

Status: bridge-starter plus sidecar_proxy runtime-smoke path
Runtime status: locally verifiable with a staged lighttpd binary

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
- [x] no local `connectors/lighttpd/tests` folder

## Phase 1: Origin / Metadata

- [x] `ORIGIN.md` added for the current repo-owned build-starter
- [x] `SOURCE_MAP.json` added for the current repo-owned build-starter
- [x] `metadata.c` / `metadata.h` added for bridge-starter status
- [x] upstream lighttpd source selected and documented for local runtime build
- [ ] upstream lighttpd license documented if source is imported into repo source

## Phase 2: Build

- [x] build-starter approach documented
- [x] build-starter command documented
- [x] bridge-starter approach documented
- [x] bridge-starter command documented
- [x] bridge-starter self-test documented
- [x] connector-neutral include paths documented
- [x] pinned lighttpd source build documented
- [x] expected local lighttpd binary path documented
- [ ] native-module lighttpd include paths documented
- [ ] native-module lighttpd library paths documented
- [x] build-starter artifact path documented
- [x] bridge-starter artifact path documented
- [x] starter logs documented
- [ ] native lighttpd module implemented
- [ ] FastCGI/SCGI bridge implemented

## Phase 3: Harness

- [x] `make smoke-lighttpd` targeted runtime-smoke entrypoint implemented
- [x] harness command documented
- [x] BLOCKED evidence path documented
- [x] common smoke result writer used instead of connector-local JSON writer
- [x] integration options evaluated; sidecar/proxy documented as recommended Phase 1 mode
- [x] Phase 1 integration path selected: `sidecar_proxy`
- [x] lighttpd binary/source-build documented
- [x] generated lighttpd config documented
- [x] sidecar decision boundary documented
- [x] targeted libmodsecurity smoke command documented
- [x] result JSON documented through common smoke schema
- [x] allowed request returns expected runtime status when local binary is available
- [x] blocked request returns HTTP 403 through the selected path when local binary is available
- [ ] production hardening for sidecar_proxy documented

## Phase 4: No-CRS Runtime

- [ ] `make test-no-crs` executed for lighttpd scope
- [ ] PASS/FAIL/BLOCKED counts documented

## Phase 5: With-CRS Runtime

- [ ] `make test-with-crs` executed for lighttpd scope
- [ ] CRS loaded/effective evidence documented
- [ ] PASS/FAIL/BLOCKED counts documented

## Phase 6: Coverage Matrix

- [ ] Phase 1/2/3/4 runtime status documented
- [ ] negative/pass-through status documented
- [ ] audit/log evidence documented
- [ ] RESPONSE_BODY blocking evaluated

## Phase 7: Promotion

- [ ] eligible for `adapter-owned`
- [x] eligible for `bridge-starter`
- [ ] eligible for `runtime-smoke-verified`
- [ ] eligible for `crs-verified`
- [ ] eligible for more than `partial`
