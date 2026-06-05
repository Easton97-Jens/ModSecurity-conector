# HAProxy Coverage Decision Matrix

Status: spoa-agent-starter
Runtime status: runtime-smoke-verified for `haproxy_phase1_header_block` and `haproxy_crs_sqli_anomaly_block`

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
| SPOE config syntax | syntax-valid | Generated under `/src/ModSecurity-conector-build/haproxy-runtime/spoe/` and checked by `haproxy -c` |
| ACK set-var encoding | verified | Local HAProxy SPOE/SPOP docs/source verify action 1, arg count 3, txn scope 2, and bool true `0x11` |
| Diagnostic HAProxy-to-agent runtime | diagnostic-enforcement-verified | `make smoke-haproxy` records fresh NOTIFY, request arg extraction, live ModSecurity 403, set-var ACK, block 403, and pass 200 for No-CRS and With-CRS minimal scopes |
| ModSecurity binding | live-enforcement-verified | local libmodsecurity C API signatures verified; HAProxy enforces the phase-1 header block and CRS SQLi anomaly decisions over SPOA |
| Productive adapter build | BLOCKED for broader adapter ownership | Full SPOA implementation and broader Framework-case evidence are missing |
| Harness | PASS for two runtime-smoke cases | `connectors/haproxy/harness/run_haproxy_smoke.sh` sets `runtime_verified: true` for the two recorded `verified_cases` only |
| No-CRS minimal phase-1 runtime | PASS | `haproxy_phase1_header_block` smoke without CRS is verified |
| Broader No-CRS matrix | not-run | no broader HAProxy-scoped No-CRS matrix evidence recorded |
| With-CRS minimal SQLi runtime | PASS | `haproxy_crs_sqli_anomaly_block` smoke loads CRS and verifies SQLi block 403 plus pass 200 |
| Broader With-CRS matrix | not-run | no broader HAProxy-scoped With-CRS matrix evidence recorded |
| RESPONSE_BODY | not-verified | no blocking response-body runtime evidence recorded |
| Promotion | partial only | two runtime-smoke cases are verified; RESPONSE_BODY, broader pass-through, audit/log, and full matrix scopes remain open |

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
- [x] live HAProxy-to-diagnostic-agent NOTIFY recorded with fresh run evidence
- [x] local libmodsecurity binding self-test recorded
- [x] verified ACK set-var encoding from local HAProxy SPOE/SPOP docs/source
- [x] live HAProxy enforcement of phase-1 header block decision recorded
- [x] local CRS preamble loaded for `haproxy_crs_sqli_anomaly_block`
- [x] live HAProxy enforcement of CRS SQLi anomaly block decision recorded
- [ ] full SPOA agent implementation selected or completed
- [ ] productive origin/license evidence recorded
- [ ] productive runtime build evidence recorded
- [x] HAProxy enforcement path for one ModSecurity decision implemented
- [x] real HAProxy to SPOA to ModSecurity runtime harness evidenced for `haproxy_phase1_header_block`
- [x] real HAProxy to SPOA to ModSecurity runtime harness evidenced for `haproxy_crs_sqli_anomaly_block`
- [ ] broader No-CRS runtime evidence recorded
- [ ] broader With-CRS runtime evidence recorded
- [ ] RESPONSE_BODY blocking evidence recorded
- [ ] negative/pass-through evidence recorded
- [ ] audit/log evidence recorded

## Phase Matrix

| Phase | Requirement | HAProxy status |
| --- | --- | --- |
| Phase 0 | Scaffold | OK |
| Phase 1 | Origin/Metadata | spoa-agent-starter |
| Phase 2 | Build | spoa-agent-starter plus ModSecurity binding self-test; productive build BLOCKED |
| Phase 3 | Harness | PASS for `haproxy_phase1_header_block` and `haproxy_crs_sqli_anomaly_block`; broader harness incomplete |
| Phase 4 | No-CRS runtime | partial; header-block smoke only |
| Phase 5 | With-CRS runtime | partial; CRS SQLi anomaly smoke only |
| Phase 6 | Coverage matrix | spoa-agent-starter documented |
| Phase 7 | RESPONSE_BODY | not-verified |
| Phase 8 | Negative/pass-through | not-verified |
| Phase 9 | Audit/log | not-verified |
| Phase 10 | Promotion | partial only |
