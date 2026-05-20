Generated file — do not edit manually.

# ModSecurity Connector Test Coverage Overview

## Kurzzusammenfassung
- Gesamtzahl Cases: **133**
- verified/pass count (runtime_verified=true): **0**
- xfail count: **79**
- pending-runtime-verification count: **86**
- connector-gap count: **11**
- runtime-difference count: **13**
- future/experimental count: **16**
- RESPONSE_BODY cases: **19** (weiterhin **nicht verified/promoted**)

## Coverage nach Variable/Collection
| Variable | Count |
|---|---:|
| `RESPONSE_BODY` | 19 |
| `ARGS:q` | 18 |
| `REQUEST_BODY` | 10 |
| `ARGS_NAMES` | 7 |
| `REQUEST_URI` | 7 |
| `ARGS:test` | 6 |
| `REQUEST_HEADERS_NAMES` | 5 |
| `ARGS` | 4 |
| `REQUEST_COOKIES_NAMES` | 4 |
| `ARGS:probe` | 4 |
| `ARGS:param1` | 4 |
| `ARGS:a` | 4 |
| `XML` | 4 |
| `RESPONSE_HEADERS:Set-Cookie` | 4 |
| `MULTIPART_FILENAME` | 3 |
| `REQUEST_COOKIES:USER_TOKEN` | 2 |
| `FILES_NAMES` | 2 |
| `RESPONSE_HEADERS:Location` | 2 |
| `TX:SCORE` | 2 |
| `ARGS_COMBINED_SIZE` | 1 |

## Coverage nach Phase
| Phase | Count |
|---|---:|
| 1 | 35 |
| 2 | 69 |
| 3 | 11 |
| 4 | 19 |

## Coverage nach Status
| Status | Count |
|---|---:|
| imported | 47 |
| unknown | 7 |
| xfail | 79 |

## Coverage nach Scope
| Scope | Count |
|---|---:|
| common | 126 |
| apache | 0 |
| nginx | 7 |
| unknown | 0 |

## Latest Local Runtime Validation Snapshot
- Snapshot: **2026-05-20** (2026-05-20 13:29:32 CEST)
- Git: branch `master`, commit `efe2dfb`
- BUILD_ROOT: `/root/.local/state/ModSecurity-conector-build`
- This is a manual local runtime snapshot rendered from tracked snapshot data and local smoke summary files.
- Framework command statuses are from the local shell exit codes in this run.
- Runtime smoke counts are from /root/.local/state/ModSecurity-conector-build/results/*-summary.json.
- The GitHub common-structure metadata failure was fixed by quoting known_limitations Classification entries so they parse as strings.
- The NGINX smoke failed, so make smoke-all was not run and no full-smoke PASS count is claimed.
- RESPONSE_BODY remains not verified/promoted by this snapshot.
- Follow-up log triage classified the 11 NGINX 403 results as harness filesystem permission blocked: NGINX error.log reports generated htdocs/index.html forbidden (13: Permission denied). They are not connector-gap, runtime-difference, or bug proof.

## Framework Check Status
| Command | Status | Details |
|---|---|---|
| git status --short --branch | PASS | Branch at start: ## master...origin/master [ahead 1] |
| git diff --check | PASS | No whitespace errors reported |
| git diff --exit-code -- connectors/apache/src connectors/nginx/src | PASS | No connector source changes |
| rg "write-expected-audit-log.py|expected-audit-log" . | PASS | No stale expected audit log helper references found |
| PyYAML parse and known_limitations audit | PASS | All tests/**/*.yaml parsed; known_limitations and case_known_limitations lists contain only strings |
| local common-structure materialize/list/write-case-matrix reproduction | PASS | tests/runners/case_cli.py and ci/write-case-matrix.py completed without the case_known_limitations validation exception |
| make setup-dev | PASS | Development dependencies available in .venv |
| make lint | PASS | actionlint unavailable message was non-fatal |
| make generate-test-matrix | PASS | Generated coverage docs refreshed |
| make check-test-matrix | PASS | Generated coverage docs matched generator output |
| make quick-check | PASS | Lightweight framework checks passed |
| make cloud-quick-check | PASS | Framework/generator-only cloud check passed |
| .venv/bin/python -m py_compile tests/normalizers/*.py tests/runners/*.py ci/*.py | PASS | Python files compiled |
| sh -n ci/*.sh | PASS | POSIX shell syntax check passed for ci shell scripts |
| bash -n ci/*.sh | PASS | Bash syntax check passed for ci shell scripts |

## Readiness / Fetch Status
| Command | Status | Details |
|---|---|---|
| make doctor-quick (before fetch-deps) | PASS | Source-build readiness ran with warnings because ModSecurity_V3 sources were not present yet |
| optional installed readiness | BLOCKED | System Apache/APXS/NGINX/libmodsecurity were not found; this is diagnostic only and does not block source-build smokes |
| make fetch-deps | PASS | Fetched ModSecurity core from configured source; Apache/NGINX connector sources remained repo-local |
| make doctor-quick (after fetch-deps) | PASS | Source-build readiness found /root/.local/state/ModSecurity-conector-build/sources/ModSecurity_V3; optional installed readiness still BLOCKED |

## Runtime Smoke Status
| Command | Status | Exit | PASS | FAIL | BLOCKED | XFAIL | Evidence |
|---|---|---|---|---|---|---|---|
| REFRESH=1 make smoke-apache | PASS | 0 | 48 | 0 | 0 | 0 | /root/.local/state/ModSecurity-conector-build/results/apache-summary.json |
| REFRESH=1 make smoke-nginx | FAIL | 2 | 43 | 11 | 0 | 0 | /root/.local/state/ModSecurity-conector-build/results/nginx-summary.json |
| REFRESH=1 make smoke-all | NOT_RUN | not_run | unknown | unknown | unknown | unknown | not available |

## Runtime FAIL Details
| Connector | Case | Expected | Actual | Assessment |
|---|---|---|---|---|
| nginx | phase2_args_pass | 200 | 403 | BLOCKED: NGINX harness filesystem permission denied while serving generated htdocs/index.html; rerun with an NGINX-readable BUILD_ROOT/harness before connector classification |
| nginx | action_allow_phase1_pass | 200 | 403 | BLOCKED: NGINX harness filesystem permission denied while serving generated htdocs/index.html; rerun with an NGINX-readable BUILD_ROOT/harness before connector classification |
| nginx | response_body_pass | 200 | 403 | BLOCKED: NGINX harness filesystem permission denied while serving generated htdocs/index.html; rerun with an NGINX-readable BUILD_ROOT/harness before connector classification; RESPONSE_BODY remains non-verified/non-promoted |
| nginx | v2_transformation_url_decode_pass_no_match | 200 | 403 | BLOCKED: NGINX harness filesystem permission denied while serving generated htdocs/index.html; rerun with an NGINX-readable BUILD_ROOT/harness before connector classification |
| nginx | v3_args_names_get_pass_no_match | 200 | 403 | BLOCKED: NGINX harness filesystem permission denied while serving generated htdocs/index.html; rerun with an NGINX-readable BUILD_ROOT/harness before connector classification |
| nginx | v3_request_cookies_names_pass_no_match | 200 | 403 | BLOCKED: NGINX harness filesystem permission denied while serving generated htdocs/index.html; rerun with an NGINX-readable BUILD_ROOT/harness before connector classification |
| nginx | v3_request_cookies_pass_no_match | 200 | 403 | BLOCKED: NGINX harness filesystem permission denied while serving generated htdocs/index.html; rerun with an NGINX-readable BUILD_ROOT/harness before connector classification |
| nginx | v3_request_headers_names_pass_no_match | 200 | 403 | BLOCKED: NGINX harness filesystem permission denied while serving generated htdocs/index.html; rerun with an NGINX-readable BUILD_ROOT/harness before connector classification |
| nginx | nginx_phase4_content_type_out_of_scope | 200 | 403 | BLOCKED: NGINX harness filesystem permission denied before phase-4 log-only behavior could be classified; phase4.log missing/empty; not connector-gap/runtime-difference proof and not RESPONSE_BODY promotion |
| nginx | nginx_phase4_minimal_log_only | 200 | 403 | BLOCKED: NGINX harness filesystem permission denied before phase-4 log-only behavior could be classified; phase4.log missing/empty; not connector-gap/runtime-difference proof and not RESPONSE_BODY promotion |
| nginx | nginx_phase4_safe_log_only | 200 | 403 | BLOCKED: NGINX harness filesystem permission denied before phase-4 log-only behavior could be classified; phase4.log missing/empty; not connector-gap/runtime-difference proof and not RESPONSE_BODY promotion |

## Runtime Verified Status
- Apache source-build smoke passed 48 runtime cases with 0 failures.
- NGINX source-build smoke executed 54 runtime cases; 43 passed and 11 expected-200 cases are blocked by generated docroot permissions, so NGINX is not fully runtime-verified by this snapshot.
- The 11 NGINX 403 results are classified as harness/filesystem blocked, not as connector-gap, runtime-difference, or likely bug evidence.
- No pass promotion, xfail promotion, or import PASS claim was made from the blocked NGINX cases.
- The YAML coverage metadata still reports runtime_verified=true as 0 because no generated metadata was promoted from this local run.
- Apache and NGINX summaries both list exercised variables ARGS, ARGS_NAMES, AUDIT_LOG, FILES, REQUEST_BODY, REQUEST_COOKIES, REQUEST_HEADERS, REQUEST_URI, RESPONSE_HEADERS, and XML; RESPONSE_BODY is not promoted.
- make smoke-all was not run after the NGINX failure; full-smoke PASS counts remain unknown.

## Offene Runtime-Probleme
- Optional installed-readiness remains BLOCKED because system Apache/APXS/NGINX/libmodsecurity are not installed.
- NGINX pass-through/no-match runtime classification is blocked by generated docroot permission denial in this local run.
- NGINX phase 4 response-body/log-only runtime classification is blocked by generated docroot permission denial and missing/empty phase4.log in this local run.
- The blocked NGINX cases need rerun with an NGINX-readable BUILD_ROOT or harness permission fix before any PASS, xfail, connector-gap, runtime-difference, or bug classification.
- RESPONSE_BODY remains non-verified/non-promoted.
- XFAIL, pending, connector-gap, runtime-difference, and future/experimental YAML cases still require separate local runtime validation before promotion.

## Top offene Gaps
- Siehe `docs/testing/generated/connector-gap-summary.generated.md` für detaillierte Einträge.

## Verified Runtime Coverage
- Runtime-verified ist nur das, was als `runtime_verified=true` klassifiziert ist.

## Pending Runtime Verification
- Fälle mit `runtime_verified=false/unknown` sind nicht als Runtime-PASS zu lesen.

## XFAIL / Known Gap Coverage
- XFAIL/Pending/Future/Experimental Fälle sind in der XFAIL-Summary gelistet.
- XFAIL/Pending/Gaps brauchen lokale Runtime-Validierung vor einer Promotion.

## Connector Gap / Runtime Difference Coverage
- Connector-Gap und Runtime-Difference sind explizit separat ausgewiesen.

## Phase 3/4 Outbound Coverage
- Phase 3/4 Fälle sind in `phase-coverage.generated.md` und der Matrix enthalten.

## RESPONSE_BODY Status
- RESPONSE_BODY bleibt nicht verified/promoted.

## Cloud/Quick/Full Smoke Bedeutung
- Generated coverage != runtime evidence.
- Full runtime validation is local.
- GitHub/Codex checks are intentionally lightweight.
- XFAIL/pending/gap cases need local runtime validation.
- GitHub/Codex checks sind absichtlich leichtgewichtig und liefern keine Runtime-Kompatibilitaetsbeweise.
- Full runtime validation ist lokal.
- `make smoke-all` bleibt autoritativ für Runtime-Evidenz.

## Generated Artefakte
- `docs/testing/generated/case-matrix.generated.md`
- `docs/testing/generated/coverage-summary.generated.md`
- `docs/testing/generated/xfail-summary.generated.md`
- `docs/testing/generated/connector-gap-summary.generated.md`
- `docs/testing/generated/phase-coverage.generated.md`

## Hinweis
- Generated summaries ersetzen keine Full-Smoke Runtime-Evidenz.
- Keine RESPONSE_BODY-Promotion ohne stabile Vollbelege.
