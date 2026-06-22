# lighttpd Connector TODO

Status: bridge-starter
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
- [x] no local `connectors/lighttpd/tests` folder

## Phase 1: Origin / Metadata

- [x] `ORIGIN.md` added for the current repo-owned build-starter
- [x] `SOURCE_MAP.json` added for the current repo-owned build-starter
- [x] `metadata.c` / `metadata.h` added for bridge-starter status
- [ ] upstream lighttpd source selected and documented
- [ ] upstream lighttpd license documented if source is imported

## Phase 2: Build

- [x] build-starter approach documented
- [x] build-starter command documented
- [x] bridge-starter approach documented
- [x] bridge-starter command documented
- [x] bridge-starter self-test documented
- [x] connector-neutral include paths documented
- [ ] lighttpd include paths documented
- [ ] lighttpd library paths documented
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
- [ ] production integration path selected
- [ ] lighttpd binary/container/source-build documented
- [ ] lighttpd config documented
- [ ] ModSecurity integration point documented
- [x] result JSON documented through common smoke schema
- [ ] allowed request returns expected runtime status
- [ ] blocked request returns HTTP 403 through the selected path

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
