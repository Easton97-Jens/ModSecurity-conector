> Generierte Datei – nicht manuell bearbeiten.
>
> Erstellt unter: `2026-06-19T16:57:55Z`
> Verifizierte Lauf-ID: `2026-06-16T19-12-00Z-614c8049`
> Datenquellenrichtlinie: `verified-inputs-only`
> Generator: `framework:ci/generate-case-matrix.py`
> Ziel erstellen: `generate-test-matrix`
> Besitzer: `runtime`
> Schweregrad: `informational`
> Connector SHA: `5c9a0ceb2fb04dbc31347f1adc762512ed7fbf9f`
> Framework-SHA: `dc19582d89bd8ef50463c5a9c5a0271cc37bb958`
> Eingabestatus: `complete`

# Generierte Abdeckungszusammenfassung

**Sprache:** [English](coverage-summary.generated.md) | Deutsch

- Gesamtzahl der Fälle: 141
- RESPONSE_BODY Fälle: 24
- Verifizierte Laufzeitfälle: 0
- Nicht verifizierte Laufzeitfälle: 141

## Nach Umfang
- gemeinsam: 134
- Apache: 0
- Nginx: 7
- unbekannt: 0

## Nach Quelle
- ModSecurity-Apache PR: 4
- owasp-modsecurity/ModSecurity-apache#78: 3
- unbekannt: 134

## Nach Status
- aktiv: 8
- importiert: 133

## Von variable/collection
- `RESPONSE_BODY`: 20
- `ARGS:q`: 18
- `REQUEST_BODY`: 10
- `REQUEST_URI`: 7
- `ARGS_NAMES`: 6
- `ARGS:test`: 6
- `REQUEST_HEADERS_NAMES`: 5
- `ARGS:a`: 4
- `REQUEST_COOKIES_NAMES`: 4
- `ARGS:param1`: 4
- `MULTIPART_FILENAME`: 4
- `ARGS`: 4
- `RESPONSE_HEADERS:Set-Cookie`: 4
- `ARGS:probe`: 4
- `XML`: 3
- `ARGS:chain_a`: 3
- `ARGS:chain_b`: 3
- `FILES_NAMES`: 2
- `REQUEST_HEADERS:Content-Type`: 2
- `XML:/*`: 2
- `TX:SCORE`: 2
- `REQUEST_COOKIES:USER_TOKEN`: 2
- `RESPONSE_HEADERS:Location`: 2
- `ARGS:audit`: 1
- `REQUEST_HEADERS:X-PR70-Phase`: 1
- `ARGS_POST:arg1`: 1
- `RESPONSE_HEADERS:Last-Modified`: 1
- `ARGS:foo`: 1
- `FILES`: 1
- `ARGS:name`: 1
- `FILES_COMBINED_SIZE`: 1
- `FILES:filedata1`: 1
- `REQUEST_HEADERS:X-Missing`: 1
- `REQUEST_HEADERS:X-Phase`: 1
- `ARGS_COMBINED_SIZE`: 1
- `ARGS_GET`: 1
- `ARGS_POST_NAMES`: 1
- `ARGS_POST:test`: 1
- `REQUEST_HEADERS:User-Agent`: 1
- `REQUEST_HEADERS:X-Entity-Probe`: 1
- `RESPONSE_HEADERS:Content-Type`: 1
- `RESPONSE_HEADERS:X-Missing`: 1
- `RESPONSE_HEADERS:content-type`: 1
- `RESPONSE_HEADERS:Server`: 1

## Nach Phase
- Phase 1: 38
- Phase 2: 75
- Phase 3: 12
- Phase 4: 20

## Verifizierungshinweis
- Generierte Zusammenfassungen dienen nur der Berichterstattung und ersetzen nicht den vollständigen Laufzeitnachweis aus `make smoke-all`.
- RESPONSE_BODY bleibt non-verified/non-promoted, bis ein stabiler Full-Smoke-Laufzeitnachweis vorliegt.
- Begrenzter Nachweis für Phase 4/strikter Abbruch bleibt bestehen experimental/non-promoted; Pass-Through-Zeilen beweisen nicht die vollständige RESPONSE_BODY-Unterstützung.

## Datenquellen

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `config/testing/import-status.json` | `5eea82df1ded18c34bbc8cf6fc5992572edaa6723a33b6dd4a0b49ee00ab5a4f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/runtime-validation-snapshot.json` | `c8e7113e2b7d4982ad6817e9f3fd4387370db33224a0f14ec265126ec685f5f9` | `2026-06-16T19-12-00Z-614c8049` | present |

## Datenverfügbarkeit / fehlende Informationen

| Input | Status | Notes |
|---|---|---|
| `config/testing/import-status.json` | present | input file available |
| `reports/testing/runtime-validation-snapshot.json` | present | input file available |
