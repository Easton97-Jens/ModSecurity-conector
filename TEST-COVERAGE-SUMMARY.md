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
- runtime-executable YAML Cases: **54**
- mapped-only import inventory entries: **10**

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

## Runtime Matrix Status
| Connector | PASS | FAIL | BLOCKED | XFAIL | NOT EXECUTED |
|---|---:|---:|---:|---:|---:|
| Apache | 48 | 0 | 0 | 78 | 7 |
| NGINX | 54 | 0 | 0 | 79 | 0 |

- Apache executed runtime cases from latest summary: **48**
- NGINX executed runtime cases from latest summary: **54**
- Apache runtime XFAIL observations from latest summary: **0**
- NGINX runtime XFAIL observations from latest summary: **0**
- Apache NOT EXECUTED YAML rows: **7**
- NGINX NOT EXECUTED YAML rows: **0**
- mapped-only import inventory entries: **10**
- Runtime Matrix Detail: `docs/testing/generated/runtime-matrix.generated.md`
- Apache per-case results: `docs/testing/generated/apache-runtime-results.generated.md`
- NGINX per-case results: `docs/testing/generated/nginx-runtime-results.generated.md`
- PASS/BLOCKED/FAIL counts here come only from tracked runtime snapshot evidence; xfail/pending cases are not promoted.
- RESPONSE_BODY remains non-verified even when a pass-through runtime case returns HTTP 200.

## Latest Local Runtime Validation Snapshot
- Snapshot: **2026-05-21** (2026-05-21 01:28:55 CEST)
- Git: branch `master`, commit `d3b6c89`
- BUILD_ROOT: `/root/.local/state/ModSecurity-conector-build`
- This is a manual local runtime snapshot rendered from tracked snapshot data and local smoke summary files.
- Runtime matrix snapshot generated from local Apache and NGINX smoke summary JSON files.
- Per-case PASS/FAIL/BLOCKED/XFAIL values are runtime evidence for this local run only.
- No xfail/pending YAML case is promoted by this snapshot.
- RESPONSE_BODY remains non-verified/non-promoted, including pass-through response-body probes.
- Mapped-only import inventory entries remain visible but are not executed runtime cases.
- make smoke-all is not implied by separate Apache/NGINX runtime matrix runs.

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
| REFRESH=1 make smoke-nginx | PASS | 0 | 54 | 0 | 0 | 0 | /root/.local/state/ModSecurity-conector-build/results/nginx-summary.json |
| REFRESH=1 make smoke-all | NOT_RUN | not_run | unknown | unknown | unknown | unknown | not available |

## Runtime Verified Status
- Runtime matrix records current local Apache and NGINX per-case smoke evidence.
- PASS in this snapshot means the case was executed by that connector's smoke harness and matched the case expectation in the summary JSON.
- XFAIL, pending, connector-gap, runtime-difference, future, and mapped-only inventory are not promoted by this snapshot.
- RESPONSE_BODY remains non-verified/non-promoted.
- make smoke-all was not run by runtime-matrix; full-smoke PASS counts remain unknown.

## Offene Runtime-Probleme
- Mapped-only import inventory entries are not executable YAML runtime cases.
- XFAIL/pending/future/connector-gap/runtime-difference cases require separate evidence before any status change.
- RESPONSE_BODY remains experimental/non-verified.

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
- `make runtime-matrix`
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
- `docs/testing/generated/runtime-matrix.generated.md`
- `docs/testing/generated/apache-runtime-results.generated.md`
- `docs/testing/generated/nginx-runtime-results.generated.md`
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
