# HAProxy Coverage Decision Matrix

Status: spoa-agent-starter
Runtime status: runtime-smoke-verified for `haproxy_phase1_header_block` and `haproxy_crs_sqli_anomaly_block`
Matrix status: partial HAProxy runtime matrix recorded; unsupported rows are
BLOCKED or NOT_EXECUTABLE, not PASS.

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
| No-CRS matrix artifact | partial, no YAML PASS | `/src/ModSecurity-conector-build/results/no-crs/haproxy-summary.json`: 141 attempted YAML rows; 0 PASS, 0 FAIL, 59 BLOCKED, 82 NOT_EXECUTABLE, 10 MAPPED_ONLY |
| With-CRS minimal SQLi runtime | PASS | `haproxy_crs_sqli_anomaly_block` smoke loads CRS and verifies SQLi block 403 plus pass 200 |
| With-CRS matrix artifact | partial, one YAML PASS | `/src/ModSecurity-conector-build/results/with-crs/haproxy-summary.json`: 141 attempted YAML rows; `crs_sqli_anomaly_block` PASS, 0 FAIL, 59 BLOCKED, 81 NOT_EXECUTABLE, 10 MAPPED_ONLY |
| Combined matrix artifact | partial | `/src/ModSecurity-conector-build/results/haproxy-summary.json`: 141 attempted YAML rows; 1 PASS, 0 FAIL, 59 BLOCKED, 81 NOT_EXECUTABLE, 10 MAPPED_ONLY |
| RESPONSE_BODY | not-verified | no blocking response-body runtime evidence recorded |
| Promotion | partial only | one exact YAML case plus one diagnostic alias are verified; RESPONSE_BODY, broader pass-through, audit/log, and full matrix scopes remain open |

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
- [x] HAProxy combined matrix artifact records one row per framework YAML case
- [x] No-CRS split matrix artifact recorded with honest BLOCKED/NOT_EXECUTABLE rows
- [x] With-CRS split matrix artifact recorded with honest BLOCKED/NOT_EXECUTABLE rows
- [ ] full SPOA agent implementation selected or completed
- [ ] productive origin/license evidence recorded
- [ ] productive runtime build evidence recorded
- [x] HAProxy enforcement path for one ModSecurity decision implemented
- [x] real HAProxy to SPOA to ModSecurity runtime harness evidenced for `haproxy_phase1_header_block`
- [x] real HAProxy to SPOA to ModSecurity runtime harness evidenced for `haproxy_crs_sqli_anomaly_block`
- [ ] broader No-CRS live YAML PASS/FAIL execution beyond the diagnostic alias
- [ ] broader With-CRS live YAML PASS/FAIL execution beyond `crs_sqli_anomaly_block`
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
| Phase 4 | No-CRS runtime | partial; diagnostic alias PASS, YAML matrix rows otherwise BLOCKED/NOT_EXECUTABLE |
| Phase 5 | With-CRS runtime | partial; `crs_sqli_anomaly_block` YAML PASS, other rows BLOCKED/NOT_EXECUTABLE |
| Phase 6 | Coverage matrix | HAProxy rows generated beside Apache/NGINX; mapped-only inventory separate |
| Phase 7 | RESPONSE_BODY | not-verified |
| Phase 8 | Negative/pass-through | not-verified |
| Phase 9 | Audit/log | not-verified |
| Phase 10 | Promotion | partial only |
