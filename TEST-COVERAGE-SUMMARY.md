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
- runtime-blocked import inventory entries: **0** (belegte Harness-/Umgebungsblocker, keine PASS- oder XFAIL-Promotion)
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
- Snapshot: **2026-05-21** (2026-05-21 00:17:33 CEST)
- Git: branch `master`, commit `1b2264d`
- BUILD_ROOT: `/root/.local/state/ModSecurity-conector-build`
- This is a manual local runtime snapshot rendered from tracked snapshot data and local smoke summary files.
- Framework command statuses are from the local shell exit codes in this permission-fix run.
- Runtime smoke counts are from /root/.local/state/ModSecurity-conector-build/results/*-summary.json.
- The NGINX harness stages worker-facing runtime files under /tmp/ModSecurity-conector-nginx-runtime-0 in this root-run environment, avoiding unreadable /root parent directories without global chmods or system NGINX changes.
- A REFRESH=1 make smoke-nginx retry rebuilt NGINX artifacts but did not complete the runtime phase because prepare-nginx-build reported a post-build shell parse error; the subsequent make smoke-nginx runtime pass used those freshly produced artifacts.
- make smoke-nginx passed all 54 active NGINX runtime cases after the harness permission fix; the 11 previously blocked expected-200 cases now returned HTTP 200.
- response_body_pass is request/runtime pass-through evidence only; RESPONSE_BODY remains non-verified/non-promoted.
- make smoke-all was not run in this snapshot; no full-smoke PASS count is claimed.

## Framework Check Status
| Command | Status | Details |
|---|---|---|
| make setup-dev | PASS | Development dependencies available in .venv |
| make lint | PASS | Repository lint checks passed |
| make generate-test-matrix | PASS | Generated coverage docs refreshed from current metadata |
| make check-test-matrix | PASS | Generated coverage docs matched generator output after staging generated docs |
| make quick-check | PASS | Lightweight framework checks passed |
| make cloud-quick-check | PASS | Framework/generator-only cloud check passed |
| .venv/bin/python -m py_compile tests/normalizers/*.py tests/runners/*.py ci/*.py | PASS | Python files compiled |
| sh -n ci/*.sh | PASS | POSIX shell syntax check passed for ci shell scripts |
| bash -n ci/*.sh | PASS | Bash syntax check passed for ci shell scripts |
| git diff --check | PASS | No whitespace errors reported |
| diff -u /tmp/pre-connector.diff /tmp/post-connector.diff | PASS | Connector source diff snapshot is unchanged; no new connector source changes were introduced |
| git diff --exit-code -- connectors/apache/src connectors/nginx/src | BLOCKED | Non-zero because connectors/apache/src/mod_security3.c had a pre-existing unrelated local change before this fix; the pre/post connector diff snapshot is unchanged |
| git ls-files .venv | PASS | No tracked .venv files |

## Readiness / Fetch Status
| Command | Status | Details |
|---|---|---|
| make fetch-deps | NOT_RUN | Not rerun in this permission-fix pass; existing ModSecurity source tree from prior source-build smoke was reused for REFRESH=1 make smoke-nginx |
| optional installed readiness | BLOCKED | System Apache/APXS/NGINX/libmodsecurity readiness remains diagnostic only and is not required for source-build smokes |
| REFRESH=1 make smoke-nginx rebuild retry | BLOCKED | The rebuild produced NGINX artifacts, then prepare-nginx-build reported a post-build shell parse error before runtime cases; runtime validation was completed separately with make smoke-nginx using the freshly produced artifacts. |

## Runtime Smoke Status
| Command | Status | Exit | PASS | FAIL | BLOCKED | XFAIL | Evidence |
|---|---|---|---|---|---|---|---|
| REFRESH=1 make smoke-apache | PASS | 0 | 48 | 0 | 0 | 0 | /root/.local/state/ModSecurity-conector-build/results/apache-summary.json |
| make smoke-nginx | PASS | 0 | 54 | 0 | 0 | 0 | /root/.local/state/ModSecurity-conector-build/results/nginx-summary.json |
| REFRESH=1 make smoke-all | NOT_RUN | not_run | unknown | unknown | unknown | unknown | not available |

## Runtime Verified Status
- NGINX source-build smoke passed 54 runtime cases with 0 failures and 0 blocked after the harness permission fix.
- The 11 cases previously classified as NGINX harness filesystem permission blocked now pass in the current local NGINX smoke run.
- Apache latest available source-build summary remains 48 PASS, 0 FAIL, 0 BLOCKED; Apache connector source was not changed by this patch.
- The generated metadata still separates local runtime evidence from runtime_verified=true promotion; no YAML case was promoted solely from this run.
- Apache and NGINX summaries list exercised variables ARGS, ARGS_NAMES, AUDIT_LOG, FILES, REQUEST_BODY, REQUEST_COOKIES, REQUEST_HEADERS, REQUEST_URI, RESPONSE_HEADERS, and XML.
- response_body_pass is pass-through evidence only; RESPONSE_BODY remains non-verified/non-promoted and no full phase-4 compatibility claim is made.
- make smoke-all was not run; full-smoke PASS counts remain unknown.

## Offene Runtime-Probleme
- Optional installed-readiness remains diagnostic only and may be BLOCKED on systems without Apache/APXS/NGINX/libmodsecurity packages.
- RESPONSE_BODY remains non-verified/non-promoted; response-body blocking support remains xfail/mapped until stable local full-smoke evidence exists.
- XFAIL, pending, connector-gap, runtime-difference, and future/experimental YAML cases still require separate local runtime validation before promotion.
- A pre-existing unrelated local diff remains under connectors/apache/src/mod_security3.c and was intentionally not staged or modified.

## Offene Bereiche / Gaps
- Runtime verification pending: Cases mit `runtime_verified=false` oder `runtime_verified=unknown` sind nicht als Runtime-PASS zu lesen.
- RESPONSE_BODY non-verified: RESPONSE_BODY bleibt nicht promoted, auch wenn Reporting Cases erfasst.
- GitHub/Codex checks sind absichtlich leichtgewichtig und liefern keine Runtime-Kompatibilitaetsbeweise.
- XFAIL/Pending/Gaps brauchen lokale Runtime-Validierung vor einer Promotion.
- Runtime-blocked Import-Einträge sind belegte Harness-/Umgebungsblocker und keine Connector-Gap- oder Runtime-Difference-Promotion.
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
- `docs/testing/nginx-runtime-failure-classification.md`
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
