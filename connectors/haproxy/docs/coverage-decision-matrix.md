# HAProxy Coverage Decision Matrix

Status: production-spoa-runtime (partial)
Runtime status: live YAML execution through HAProxy, SPOA/SPOP, and
libmodsecurity using `haproxy-modsecurity-spoa`.
Matrix status: partial HAProxy runtime matrix recorded from live summary
evidence; unsupported rows are BLOCKED or NOT_EXECUTABLE, not PASS.

This HAProxy matrix is connector-specific and intentionally short. The global
matrix structure and promotion rules are defined in:

- `connectors/_template/docs/coverage-decision-matrix.md`
- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`

The complete local compile and verification flow is documented in the root
guide: [`COMPILE_HAPROXY.md`](../../../COMPILE_HAPROXY.md).

## Current HAProxy Status

| Area | HAProxy status | Evidence |
| --- | --- | --- |
| Scaffold | OK | `connectors/haproxy/README.md`, `connectors/haproxy/TODO.md` |
| Origin/Metadata | spoa-agent-starter | `ORIGIN.md`, `SOURCE_MAP.json`, `metadata.c`, `metadata.h` |
| Metadata build | PASS | `make -C connectors/haproxy build-metadata` |
| SPOA starter build | PASS | `make -C connectors/haproxy build-spoa-starter` |
| Local self-test | PASS | `make -C connectors/haproxy self-test-spoa` |
| Local HAProxy binary prepare | PASS | framework `ci/prepare-haproxy-runtime.sh` builds HAProxy under `/src/ModSecurity-conector-build` |
| SPOP runtime | PASS for protocol self-test; live gate is smoke | `make -C connectors/haproxy self-test-spoa-runtime`; `make smoke-haproxy` exercises the production agent with HAProxy |
| SPOE config syntax | syntax-valid | Generated under `/src/ModSecurity-conector-build/haproxy-runtime/spoe/` and checked by `haproxy -c` |
| ACK set-var encoding | verified | Local HAProxy SPOE/SPOP docs/source verify action 1, arg count 3, txn scope 2, and bool true `0x11` |
| HAProxy-to-agent runtime | live-verified | `make smoke-haproxy` records fresh NOTIFY, request/response arg extraction, materialized rules, live ModSecurity decisions, set-var ACK, and asserted curl status for shared YAML cases |
| ModSecurity binding | live-enforcement-verified | local libmodsecurity C API signatures verified; HAProxy enforces YAML decisions over SPOA/SPOP |
| Productive adapter build | PASS for current SPOA runtime | `build-spoa-runtime` builds `haproxy-modsecurity-spoa`; deployment and harness use that same binary/code path |
| Harness | PASS for shared executable YAML cases | `connectors/haproxy/harness/run_haproxy_smoke.sh` sets `live_executed: true` for live PASS/FAIL rows |
| No-CRS matrix artifact | partial live runtime | `/src/ModSecurity-conector-build/results/no-crs/haproxy-summary.json`: 54 PASS, 0 FAIL, 0 BLOCKED, 0 NOT_EXECUTABLE |
| With-CRS matrix artifact | partial live runtime | `/src/ModSecurity-conector-build/results/with-crs/haproxy-summary.json`: 55 PASS, 0 FAIL, 0 BLOCKED, 0 NOT_EXECUTABLE, including `crs_sqli_anomaly_block` |
| Combined matrix artifact | partial live runtime | `/src/ModSecurity-conector-build/results/haproxy-summary.json`: generated from the latest selected variant summary |
| Request-side variables | verified | `REQUEST_URI`, `REQUEST_HEADERS`, `REQUEST_HEADERS_NAMES`, `ARGS`, `ARGS_NAMES`, `REQUEST_COOKIES`, `REQUEST_COOKIES_NAMES`, `REQUEST_BODY`, `FILES`, `XML` |
| Response headers | verified | phase-3 response-header cases execute through `http-response send-spoe-group` and decision logs record response headers seen |
| Body/frame limit | partial | HAProxy request buffering with `tune.bufsize 65536`, SPOE `max-frame-size 65532`, and one `req.body` argument; larger or multi-frame bodies are not proven |
| RESPONSE_BODY | experimental non-promoted | bounded phase-4 probes execute with `wait-for-body`, response-body limits, and timeout metadata only |
| Audit/log | verified for live audit cases | audit assertions use real libmodsecurity audit output, not synthesized audit rows |
| Promotion | partial only | request phases, response headers, audit, redirect where supported, and fixed disruptive statuses are live; full `RESPONSE_BODY` remains non-promoted |

## Gate Checklist

- [x] Scaffold files present
- [x] no local `connectors/haproxy/tests` folder
- [x] repo-authored starter origin/source map recorded
- [x] metadata build recorded
- [x] local SPOA agent starter build recorded
- [x] local SPOA agent starter self-test recorded
- [x] framework-owned HAProxy source acquisition defined and checksum-verified
- [x] local HAProxy binary prepared under `/src/ModSecurity-conector-build`
- [x] SPOP protocol self-test recorded
- [x] generated SPOE config is syntax-valid by `haproxy -c`
- [x] live HAProxy-to-SPOP-runtime NOTIFY recorded with fresh run evidence
- [x] local libmodsecurity binding self-test recorded
- [x] verified ACK set-var encoding from local HAProxy SPOE/SPOP docs/source
- [x] live HAProxy enforcement of materialized YAML decisions recorded
- [x] local CRS preamble loaded for `crs_sqli_anomaly_block`
- [x] live HAProxy enforcement of CRS SQLi anomaly block decision recorded
- [x] HAProxy combined artifact records live shared executable YAML case evidence
- [x] No-CRS split matrix artifact recorded with honest PASS/FAIL/BLOCKED rows
- [x] With-CRS split matrix artifact recorded with honest PASS/FAIL/BLOCKED rows
- [x] production SPOA agent implementation selected or completed for current partial scope
- [x] productive origin/license evidence recorded for repo-owned implementation
- [x] productive runtime build evidence recorded
- [x] HAProxy enforcement path for ModSecurity decisions implemented
- [x] real HAProxy to SPOA/SPOP to ModSecurity runtime harness evidenced for shared executable YAML cases
- [x] broader No-CRS live YAML PASS/FAIL execution across shared executable cases
- [x] broader With-CRS live YAML PASS/FAIL execution across shared executable cases
- [x] negative/pass-through evidence recorded for request-side clean probes
- [x] bounded experimental RESPONSE_BODY blocking evidence recorded
- [x] audit/log evidence recorded

## Phase Matrix

| Phase | Requirement | HAProxy status |
| --- | --- | --- |
| Phase 0 | Scaffold | OK |
| Phase 1 | Origin/Metadata | spoa-agent-starter |
| Phase 2 | Build | production `haproxy-modsecurity-spoa` plus ModSecurity binding self-test |
| Phase 3 | Harness | live per-YAML HAProxy harness implemented |
| Phase 4 | No-CRS runtime | partial; 54 PASS, 0 FAIL, 0 BLOCKED, 0 NOT_EXECUTABLE |
| Phase 5 | With-CRS runtime | partial; 55 PASS, 0 FAIL, 0 BLOCKED, 0 NOT_EXECUTABLE including `crs_sqli_anomaly_block` |
| Phase 6 | Coverage matrix | HAProxy rows generated beside Apache/NGINX; mapped-only inventory separate |
| Phase 7 | RESPONSE_BODY | bounded experimental/non-promoted |
| Phase 8 | Negative/pass-through | verified for request-side clean probes |
| Phase 9 | Audit/log | verified for live audit cases |
| Phase 10 | Promotion | partial only |
