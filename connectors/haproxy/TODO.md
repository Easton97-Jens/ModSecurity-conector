# HAProxy Connector TODO

Status: spoa-agent-starter
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
- [x] no local `connectors/haproxy/tests` folder

## Phase 1: Origin / Metadata

- [x] `ORIGIN.md` added for the current repo-authored starter
- [x] `SOURCE_MAP.json` added for the current repo-authored starter
- [x] `metadata.c` and `metadata.h` added
- [x] local SPOA agent starter source documented
- [ ] upstream HAProxy source selected and documented
- [ ] upstream HAProxy integration headers/API documented
- [ ] productive-source license documented

## Phase 2: Build

- [x] metadata build-starter approach documented
- [x] metadata object build command documented
- [x] local SPOA agent starter build documented
- [x] local SPOA agent starter self-test documented
- [x] shared include/source paths documented
- [x] starter artifact path documented
- [ ] SPOP parser/library selected
- [ ] productive HAProxy adapter build approach documented
- [ ] productive include paths documented
- [ ] productive library paths documented
- [ ] productive adapter artifact path documented
- [ ] productive adapter build logs documented

## Phase 3: Harness

- [ ] HAProxy runtime harness implemented
- [ ] harness command documented
- [ ] harness evidence path documented
- [ ] HAProxy binary/container/source-build documented
- [ ] HAProxy config documented
- [ ] SPOE/SPOA config documented and verified
- [ ] starter/agent endpoint documented
- [ ] ModSecurity integration point documented

## Phase 4: No-CRS Runtime

- [ ] `make test-no-crs` executed for HAProxy scope
- [ ] PASS/FAIL/BLOCKED counts documented

## Phase 5: With-CRS Runtime

- [ ] `make test-with-crs` executed for HAProxy scope
- [ ] CRS loaded/effective evidence documented
- [ ] PASS/FAIL/BLOCKED counts documented

## Phase 6: Coverage Matrix

- [x] Phase 0/1/2 starter status documented
- [ ] productive Phase 2/3/4 status documented
- [ ] negative/pass-through status documented
- [ ] audit/log evidence documented
- [ ] RESPONSE_BODY blocking evaluated

## Phase 7: Promotion

- [ ] eligible for `adapter-owned`
- [ ] eligible for `runtime-smoke-verified`
- [ ] eligible for `crs-verified`
- [ ] eligible for more than `partial`
