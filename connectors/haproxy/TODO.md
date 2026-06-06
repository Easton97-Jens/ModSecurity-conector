# HAProxy Connector TODO

Status: spoa-agent-starter
Runtime status: runtime-smoke-verified for `haproxy_phase1_header_block` and `haproxy_crs_sqli_anomaly_block`

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
- [x] root compile guide documented in `COMPILE_HAPROXY.md`
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

- [x] HAProxy runtime harness implemented for `haproxy_phase1_header_block`
- [x] harness command documented
- [x] harness evidence path documented
- [x] HAProxy binary/source-build documented
- [x] HAProxy config documented
- [x] SPOE/SPOA config documented and verified for the header-block smoke
- [x] diagnostic agent endpoint documented
- [x] ModSecurity integration point documented for the header-block smoke
- [x] CRS integration point documented for the SQLi anomaly smoke
- [ ] broader HAProxy runtime harness implemented

## Phase 4: No-CRS Runtime

- [x] minimal phase-1 header-block smoke executed for
  `haproxy_phase1_header_block`
- [x] `make test-haproxy-no-crs` executed for HAProxy scope
- [x] PASS/FAIL/BLOCKED/NOT_EXECUTABLE counts documented for the No-CRS matrix
- [ ] broader No-CRS live YAML PASS/FAIL execution beyond the diagnostic alias

## Phase 5: With-CRS Runtime

- [x] minimal CRS SQLi anomaly smoke executed for
  `haproxy_crs_sqli_anomaly_block`
- [x] `make test-haproxy-with-crs` executed for HAProxy scope
- [x] CRS loaded/effective evidence documented for the minimal smoke
- [x] PASS/BLOCKED/FAIL counts documented for the minimal smoke
- [x] With-CRS matrix PASS/FAIL/BLOCKED/NOT_EXECUTABLE counts documented
- [ ] broader With-CRS live YAML PASS/FAIL execution beyond `crs_sqli_anomaly_block`

## Phase 6: Coverage Matrix

- [x] Phase 0/1/2 starter status documented
- [x] HAProxy matrix target documented with per-case BLOCKED/NOT_EXECUTABLE rows
- [x] split No-CRS and With-CRS result artifacts documented
- [ ] productive Phase 2/3/4 live status documented
- [ ] negative/pass-through live evidence documented
- [ ] audit/log live evidence documented
- [ ] RESPONSE_BODY blocking evaluated

## Phase 7: Promotion

- [ ] eligible for `adapter-owned`
- [x] eligible for `runtime-smoke-verified` for `haproxy_phase1_header_block`
- [x] eligible for `crs-verified` for `haproxy_crs_sqli_anomaly_block`
- [ ] eligible for more than `partial`
