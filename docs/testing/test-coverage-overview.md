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

## Runtime Matrix Status
- Runtime-executable YAML cases: **54**
| Connector | PASS | FAIL | BLOCKED | XFAIL | NOT EXECUTED |
|---|---:|---:|---:|---:|---:|
| Apache | 48 | 0 | 0 | 78 | 7 |
| NGINX | 54 | 0 | 0 | 79 | 0 |
- Apache executed runtime cases from latest summary: **48**
- NGINX executed runtime cases from latest summary: **54**
- Apache runtime XFAIL observations from latest summary: **0**
- NGINX runtime XFAIL observations from latest summary: **0**
- Details: `docs/testing/generated/runtime-matrix.generated.md`

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
