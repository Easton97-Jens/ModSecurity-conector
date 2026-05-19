Generated file — do not edit manually.

# ModSecurity Connector Test Coverage Overview

## Kurzzusammenfassung
- Gesamtzahl Cases: **133**
- verified/pass count (runtime_verified=true): **0**
- xfail count: **69**
- pending-runtime-verification count: **86**
- connector-gap count: **11**
- runtime-difference count: **13**
- future/experimental count: **16**
- RESPONSE_BODY cases: **18** (weiterhin **nicht verified/promoted**)

## Coverage nach Variable/Collection
| Variable | Count |
|---|---:|
| `RESPONSE_BODY` | 18 |
| `ARGS:q` | 13 |
| `ARGS_NAMES` | 7 |
| `REQUEST_BODY` | 7 |
| `REQUEST_URI` | 7 |
| `ARGS:test` | 6 |
| `REQUEST_HEADERS_NAMES` | 5 |
| `ARGS` | 4 |
| `REQUEST_COOKIES_NAMES` | 4 |
| `ARGS:probe` | 4 |
| `ARGS:param1` | 4 |
| `ARGS:a` | 4 |
| `RESPONSE_HEADERS:Set-Cookie` | 4 |
| `MULTIPART_FILENAME` | 3 |
| `XML` | 3 |
| `REQUEST_COOKIES:USER_TOKEN` | 2 |
| `FILES_NAMES` | 2 |
| `RESPONSE_HEADERS:Location` | 2 |
| `TX:SCORE` | 2 |
| `ARGS_COMBINED_SIZE` | 1 |

## Coverage nach Phase
| Phase | Count |
|---|---:|
| 1 | 35 |
| 2 | 60 |
| 3 | 11 |
| 4 | 18 |

## Coverage nach Status
| Status | Count |
|---|---:|
| imported | 47 |
| unknown | 17 |
| xfail | 69 |

## Coverage nach Scope
| Scope | Count |
|---|---:|
| common | 126 |
| apache | 0 |
| nginx | 7 |
| unknown | 0 |

## Top offene Gaps
- Siehe `docs/testing/generated/connector-gap-summary.generated.md` für detaillierte Einträge.

## Verified Runtime Coverage
- Runtime-verified ist nur das, was als `runtime_verified=true` klassifiziert ist.

## Pending Runtime Verification
- Fälle mit `runtime_verified=false/unknown` sind nicht als Runtime-PASS zu lesen.

## XFAIL / Known Gap Coverage
- XFAIL/Pending/Future/Experimental Fälle sind in der XFAIL-Summary gelistet.

## Connector Gap / Runtime Difference Coverage
- Connector-Gap und Runtime-Difference sind explizit separat ausgewiesen.

## Phase 3/4 Outbound Coverage
- Phase 3/4 Fälle sind in `phase-coverage.generated.md` und der Matrix enthalten.

## RESPONSE_BODY Status
- RESPONSE_BODY bleibt nicht verified/promoted.

## Cloud/Quick/Full Smoke Bedeutung
- Quick/Cloud Checks sind nützlich für frühes Signal, ersetzen aber keine vollständige Runtime-Verifikation.
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
