# HAProxy Coverage Decision Matrix

Status: spoa-agent-starter
Runtime status: not-verified

This HAProxy matrix is connector-specific and intentionally short. The global
matrix structure and promotion rules are defined in:

- `connectors/_template/docs/coverage-decision-matrix.md`
- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`

## Current HAProxy Status

| Area | HAProxy status | Evidence |
| --- | --- | --- |
| Scaffold | OK | `connectors/haproxy/README.md`, `connectors/haproxy/TODO.md` |
| Origin/Metadata | spoa-agent-starter | `ORIGIN.md`, `SOURCE_MAP.json`, `metadata.c`, `metadata.h` |
| Metadata build | PASS | `make -C connectors/haproxy build-metadata` |
| SPOA starter build | PASS | `make -C connectors/haproxy build-spoa-starter` |
| Local self-test | PASS | `make -C connectors/haproxy self-test-spoa` |
| Local HAProxy binary prepare | PASS | framework `ci/prepare-haproxy-runtime.sh` builds HAProxy under `/src/ModSecurity-conector-build` |
| Diagnostic SPOP subset | PASS for diagnostic scope only | `make -C connectors/haproxy self-test-spoa-runtime`; minimal diagnostic SPOP handshake subset, not a full SPOA agent implementation |
| SPOE config syntax | syntax-valid only | Generated under `/src/ModSecurity-conector-build/haproxy-runtime/spoe/`; `spoe_runtime_status` remains `not-verified` |
| Productive adapter build | BLOCKED | SPOP parser/library, HAProxy runtime harness, and libmodsecurity binding strategy not selected |
| Harness | blocked prerequisite diagnostics | `connectors/haproxy/harness/run_haproxy_smoke.sh` writes BLOCKED evidence |
| No-CRS | not-run | no HAProxy-scoped runtime evidence recorded |
| With-CRS | not-run | no HAProxy-scoped CRS runtime evidence recorded |
| RESPONSE_BODY | not-verified | no blocking response-body runtime evidence recorded |
| Promotion | not allowed | runtime evidence missing |

## Gate Checklist

- [x] Scaffold files present
- [x] no local `connectors/haproxy/tests` folder
- [x] repo-authored starter origin/source map recorded
- [x] metadata build recorded
- [x] local SPOA agent starter build recorded
- [x] local SPOA agent starter self-test recorded
- [x] framework-owned HAProxy source acquisition defined and checksum-verified
- [x] local HAProxy binary prepared under `/src/ModSecurity-conector-build`
- [x] minimal diagnostic SPOP handshake subset self-test recorded
- [x] generated SPOE config is syntax-valid by `haproxy -c`
- [x] blocked runtime-smoke prerequisite diagnostics recorded
- [ ] full SPOA agent implementation selected or completed
- [ ] productive origin/license evidence recorded
- [ ] productive runtime build evidence recorded
- [ ] real HAProxy to SPOA to ModSecurity runtime harness implemented and evidenced
- [ ] No-CRS runtime evidence recorded
- [ ] With-CRS runtime evidence recorded
- [ ] RESPONSE_BODY blocking evidence recorded
- [ ] negative/pass-through evidence recorded
- [ ] audit/log evidence recorded

## Phase Matrix

| Phase | Requirement | HAProxy status |
| --- | --- | --- |
| Phase 0 | Scaffold | OK |
| Phase 1 | Origin/Metadata | spoa-agent-starter |
| Phase 2 | Build | spoa-agent-starter; productive build BLOCKED |
| Phase 3 | Harness | blocked; diagnostic SPOP subset and SPOE syntax only |
| Phase 4 | No-CRS runtime | not-run |
| Phase 5 | With-CRS runtime | not-run |
| Phase 6 | Coverage matrix | spoa-agent-starter documented |
| Phase 7 | RESPONSE_BODY | not-verified |
| Phase 8 | Negative/pass-through | not-verified |
| Phase 9 | Audit/log | not-verified |
| Phase 10 | Promotion | not allowed |
