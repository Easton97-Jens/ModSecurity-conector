Generated file — do not edit manually.

# ModSecurity Connector Test Coverage Summary

## Kurzstatus
- Gesamtzahl aller YAML Cases: **133**
- verified/pass (`runtime_verified=true`): **0**
- xfail: **79**
- pending-runtime-verification (`runtime_verified=false`): **86**
- pending-runtime-verification (`runtime_verified=unknown`): **47**
- connector-gap: **11**
- runtime-difference: **13**
- future/experimental: **16**
- RESPONSE_BODY Cases: **19**

**RESPONSE_BODY ist nicht verified/promoted.** Diese Datei ist generiertes Reporting und keine Runtime-Evidenz.

## Testarten
- Common YAML Cases: **126**
- Apache-specific Cases: **0**
- NGINX-specific Cases: **7**
- xfail Cases: **79**
- mapped-only import inventory entries: **10** (nicht als runnable YAML Cases gezählt)
- pending/future compatibility Cases: **16** future/experimental; **133** nicht runtime-verified

## Statusklassen
| Status | Count |
|---|---:|
| imported | 47 |
| unknown | 7 |
| xfail | 79 |

## Scope
| Scope | Count |
|---|---:|
| common | 126 |
| apache | 0 |
| nginx | 7 |
| unknown | 0 |

## Coverage nach Variablen/Collections
| Variable / Collection | Count |
|---|---:|
| `ARGS` | 43 |
| `ARGS_NAMES` | 7 |
| `REQUEST_HEADERS` | 4 |
| `REQUEST_HEADERS_NAMES` | 5 |
| `REQUEST_COOKIES` | 2 |
| `REQUEST_COOKIES_NAMES` | 4 |
| `REQUEST_URI` | 7 |
| `REQUEST_BODY` | 10 |
| `FILES` | 2 |
| `FILES_NAMES` | 2 |
| `XML` | 5 |
| `RESPONSE_HEADERS` | 10 |
| `RESPONSE_BODY` | 19 |
| `AUDIT_LOG` | 0 |

## Coverage nach Phase
| Phase | Count |
|---|---:|
| Phase 1 | 35 |
| Phase 2 | 69 |
| Phase 3 | 11 |
| Phase 4 | 19 |

## Coverage nach Themen
| Topic | Count |
|---|---:|
| Operators | 128 |
| Transformations | 28 |
| Multipart / FILES | 11 |
| JSON | 7 |
| XML | 5 |
| Unicode / Encoding | 16 |
| XSS-like compatibility probes | 2 |
| SQLi-like compatibility probes | 2 |
| Audit-log probes | 12 |
| Response header probes | 10 |
| Response body experimental probes | 2 |

## Latest Local Runtime Validation Snapshot
- Snapshot: **2026-05-20** (2026-05-20 12:56:33 CEST)
- Git: branch `master`, commit `63ae69b`
- BUILD_ROOT: `/root/.local/state/ModSecurity-conector-build`
- This is a manual local runtime snapshot rendered from tracked snapshot data and local smoke summary files.
- Framework command statuses are from the local shell exit codes in this run.
- Runtime smoke counts are from /root/.local/state/ModSecurity-conector-build/results/*-summary.json.
- The NGINX smoke failed, so make smoke-all was not run and no full-smoke PASS count is claimed.
- RESPONSE_BODY remains not verified/promoted by this snapshot.

## Framework Check Status
| Command | Status | Details |
|---|---|---|
| git status --short --branch | PASS | Clean branch at start: ## master...origin/master |
| git diff --check | PASS | No whitespace errors reported |
| git diff --exit-code -- connectors/apache/src connectors/nginx/src | PASS | No connector source changes |
| rg "write-expected-audit-log.py|expected-audit-log" . | PASS | No stale expected audit log helper references found |
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
| Connector | Case | Expected | Actual |
|---|---|---|---|
| nginx | phase2_args_pass | 200 | 403 |
| nginx | action_allow_phase1_pass | 200 | 403 |
| nginx | response_body_pass | 200 | 403 |
| nginx | v2_transformation_url_decode_pass_no_match | 200 | 403 |
| nginx | v3_args_names_get_pass_no_match | 200 | 403 |
| nginx | v3_request_cookies_names_pass_no_match | 200 | 403 |
| nginx | v3_request_cookies_pass_no_match | 200 | 403 |
| nginx | v3_request_headers_names_pass_no_match | 200 | 403 |
| nginx | nginx_phase4_content_type_out_of_scope | 200 | 403 |
| nginx | nginx_phase4_minimal_log_only | 200 | 403 |
| nginx | nginx_phase4_safe_log_only | 200 | 403 |

## Runtime Verified Status
- Apache source-build smoke passed 48 runtime cases with 0 failures.
- NGINX source-build smoke executed 54 runtime cases but failed 11, so NGINX is not fully runtime-verified by this snapshot.
- The YAML coverage metadata still reports runtime_verified=true as 0 because no generated metadata was promoted from this local run.
- Apache and NGINX summaries both list exercised variables ARGS, ARGS_NAMES, AUDIT_LOG, FILES, REQUEST_BODY, REQUEST_COOKIES, REQUEST_HEADERS, REQUEST_URI, RESPONSE_HEADERS, and XML; RESPONSE_BODY is not promoted.
- make smoke-all was not run after the NGINX failure; full-smoke PASS counts remain unknown.

## Offene Runtime-Probleme
- Optional installed-readiness remains BLOCKED because system Apache/APXS/NGINX/libmodsecurity are not installed.
- NGINX pass-through/no-match cases returned 403 instead of 200 in this local run.
- NGINX phase 4 response-body/log-only cases returned 403 instead of 200 in this local run.
- RESPONSE_BODY remains non-verified/non-promoted.
- XFAIL, pending, connector-gap, runtime-difference, and future/experimental YAML cases still require separate local runtime validation before promotion.

## Offene Bereiche / Gaps
- Runtime verification pending: Cases mit `runtime_verified=false` oder `runtime_verified=unknown` sind nicht als Runtime-PASS zu lesen.
- RESPONSE_BODY non-verified: RESPONSE_BODY bleibt nicht promoted, auch wenn Reporting Cases erfasst.
- GitHub/Codex checks sind absichtlich leichtgewichtig und liefern keine Runtime-Kompatibilitaetsbeweise.
- XFAIL/Pending/Gaps brauchen lokale Runtime-Validierung vor einer Promotion.
- `installed-readiness` ist Komponenten-Erkennung/Readiness, keine Runtime-Ausführung.
- Es gibt keinen separaten Artefakt-Reuse-Smoke-Pfad; Runtime-Validierung erfolgt per frischem Source-Build.
- `make smoke-all` bleibt die autoritative Quelle für echte Runtime-PASS-Zahlen.

## Kommandos
- `make quick-check`
- `make quick-all`
- `make cloud-quick-check`
- `make installed-readiness`
- `make smoke-apache`
- `make smoke-nginx`
- `make smoke-all`
- `make generate-test-matrix`
- `make check-test-matrix`

## Detaildokumente
- `docs/testing/test-coverage-overview.md`
- `docs/testing/generated/case-matrix.generated.md`
- `docs/testing/generated/coverage-summary.generated.md`
- `docs/testing/generated/xfail-summary.generated.md`
- `docs/testing/generated/connector-gap-summary.generated.md`
- `docs/testing/generated/phase-coverage.generated.md`
- `docs/testing/runtime-validation-snapshot.json`
- `docs/testing/response-body-blocking-investigation.md`
- `docs/testing/compatibility.md`

## Wichtiger Hinweis
Generated coverage != runtime evidence.
Full runtime validation is local.
GitHub/Codex checks are intentionally lightweight.
XFAIL/pending/gap cases need local runtime validation.
Die generierte Coverage-Dokumentation ist Reporting. Sie ersetzt keine Runtime-Evidenz.
Full runtime validation ist lokal; GitHub/Codex checks sind absichtlich leichtgewichtig.
XFAIL/Pending/Gaps brauchen lokale Runtime-Validierung vor einer Promotion.
`make smoke-all` bleibt die autoritative Quelle für echte PASS-Zahlen.
Keine PASS-Zahlen werden aus dieser Datei abgeleitet, wenn `make smoke-all` nicht vollständig lief.
Keine RESPONSE_BODY-Promotion ohne stabile Full-Smoke-Runtime-Evidenz.
