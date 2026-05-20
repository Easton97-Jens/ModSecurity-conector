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

## Offene Bereiche / Gaps
- Runtime verification pending: Cases mit `runtime_verified=false` oder `runtime_verified=unknown` sind nicht als Runtime-PASS zu lesen.
- RESPONSE_BODY non-verified: RESPONSE_BODY bleibt nicht promoted, auch wenn Reporting Cases erfasst.
- GitHub/Codex checks sind absichtlich leichtgewichtig und liefern keine Runtime-Kompatibilitaetsbeweise.
- XFAIL/Pending/Gaps brauchen lokale Runtime-Validierung vor einer Promotion.
- `installed-readiness` ist Komponenten-Erkennung/Readiness, keine Runtime-Ausführung.
- `smoke-cached` hängt von vorhandenen Build-Artefakten ab.
- `make smoke-all` bleibt die autoritative Quelle für echte Runtime-PASS-Zahlen.

## Kommandos
- `make quick-check`
- `make quick-all`
- `make cloud-quick-check`
- `make installed-readiness`
- `make smoke-cached`
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
