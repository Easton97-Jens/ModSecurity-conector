# Apache Template Alignment

**Language:** English | [Deutsch](apache-template-alignment.de.md)

## Overall Decision

- Template alignment: aligned.
- Runtime status: partial.
- Executed runtime gates: runtime-smoke-verified for the current `/src`
  No-CRS/common scope, and crs-verified for the current `/src` With-CRS scope.
- Reason: `connectors/apache` matches the current Template scaffold,
  origin/license, metadata, build, harness, external-test, No-CRS, and
  With-CRS gates for the executed scope. It remains `partial` because
  RESPONSE_BODY blocking and the full minimum matrix are not verified.

## Gate Checklist

- [x] Scaffold structure present.
- [x] Origin/license evidence present.
- [x] Metadata present.
- [x] Build evidence present.
- [x] Harness contract present.
- [x] No local `connectors/apache/tests` folder.
- [x] External framework tests referenced.
- [x] No-CRS runtime PASS documented.
- [x] With-CRS runtime PASS documented.
- [ ] RESPONSE_BODY blocking verified.
- [ ] Full minimum matrix verified.
- [ ] Connector can be promoted beyond `partial`.

## Phase Matrix

| Phase / Gate | Template requirement | Apache evidence | No-CRS status | With-CRS status | Decision |
| --- | --- | --- | --- | --- | --- |
| Phase 0: Scaffold | README/TODO/docs/harness/src present | `connectors/apache/README.md`, `TODO.md`, `docs/`, `harness/`, `src/` | n/a | n/a | OK |
| Phase 1: Origin/Metadata | ORIGIN, SOURCE_MAP, metadata present | `connectors/apache/ORIGIN.md`, `SOURCE_MAP.json`, `metadata.c`, `metadata.h` | n/a | n/a | OK |
| Phase 2: Build | build command, include/lib paths, artifact evidence | `connectors/apache/docs/build.md`, `Makefile.am`, `configure.ac`, `/src/ModSecurity-conector-build/logs/apache/`, `/src/ModSecurity-conector-build/apache-build/output/apache/mod_security3.so` | n/a | n/a | OK for current `/src` evidence |
| Phase 3: Harness | connector harness present and documented | `connectors/apache/harness/README.md`, `run_apache_smoke.sh`, `apache_smoke.conf` | n/a | n/a | OK |
| Phase 4: No-CRS Runtime | `make test-no-crs` PASS | `/src/ModSecurity-conector-build/results/no-crs/apache-summary.txt`: 54 PASS, 0 FAIL, 0 BLOCKED | PASS | n/a | OK; runtime-smoke-verified for executed scope |
| Phase 5: With-CRS Runtime | `make test-with-crs` PASS and CRS evidence | `/src/ModSecurity-conector-build/results/with-crs/apache-summary.txt`: 55 PASS, 0 FAIL, 0 BLOCKED; `/src/coreruleset`; `/src/ModSecurity-conector-build/crs/modsecurity-crs-preamble.conf` | n/a | PASS | OK; crs-verified for executed scope |
| Phase 6: Coverage Matrix | Phase 1/2/3/4 documented separately | `connectors/apache/docs/coverage-decision-matrix.md` | PASS for executed rows | PASS for executed rows | partial unless complete |
| Phase 7: RESPONSE_BODY | blocking evidence required | `response_body_pass` is PASS/pass-through only in current result files | not verified for blocking | not verified for blocking | not verified |
| Phase 8: Negative/pass-through | pass-through evidence required | `v2_transformation_url_decode_pass_no_match` PASS in current result files | PASS for executed row | PASS for executed row | partial until full matrix documented |
| Phase 9: Audit/log | audit/log evidence required | audit-log rows are present and PASS in current summaries; full audit/log evidence is not separately complete | PASS for executed rows | PASS for executed rows | partial |
| Phase 10: Promotion | full matrix required | current evidence excludes RESPONSE_BODY blocking and full minimum matrix | partial | partial | partial |

## Runtime Evidence

- `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common`: 54 PASS / 0 FAIL / 0 BLOCKED.
- `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs`: 54 PASS / 0 FAIL / 0 BLOCKED.
- `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs`: 55 PASS / 0 FAIL / 0 BLOCKED.
- No-CRS `action_status_401_phase1_block`: expected 401, actual 401, PASS.
- With-CRS `action_status_401_phase1_block`: expected 403, actual 403, PASS.
- With-CRS `crs_sqli_anomaly_block`: expected 403, actual 403, PASS.
- `response_body_pass`: expected 200, actual 200, PASS; pass-through only, not RESPONSE_BODY blocking evidence.
- `response_header_basic`: expected 403, actual 403, PASS.
- `v2_transformation_url_decode_pass_no_match`: expected 200, actual 200, PASS.

Evidence files:

- `/src/ModSecurity-conector-build/results/apache-summary.txt`
- `/src/ModSecurity-conector-build/results/apache-results.jsonl`
- `/src/ModSecurity-conector-build/results/no-crs/apache-summary.txt`
- `/src/ModSecurity-conector-build/results/no-crs/apache-results.jsonl`
- `/src/ModSecurity-conector-build/results/with-crs/apache-summary.txt`
- `/src/ModSecurity-conector-build/results/with-crs/apache-results.jsonl`

## Open Gates

- RESPONSE_BODY blocking.
- Full minimum matrix.
- Apache-specific YAML cases: deferred; only `README.md` was found under
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/apache/`.
- Audit/log full evidence beyond executed rows.
- Negative/pass-through full evidence beyond executed rows.

## Decision

Apache is aligned with the current Template for scaffold, metadata, build,
harness, No-CRS, and With-CRS executed runtime scope.

Apache remains `partial` because RESPONSE_BODY blocking and the full minimum
matrix are not verified.
