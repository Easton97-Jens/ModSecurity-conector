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

# Generierte Phasenabdeckung

**Sprache:** [English](phase-coverage.generated.md) | Deutsch

> Hinweis: Diese deutsche Datei ist eine übersetzte Begleitdatei zur generierten englischen Quelle. Maschinenlesbare Werte, Tabellen, IDs, Pfade und Metriken bleiben absichtlich unverändert. Bei einer Neuerzeugung der englischen Quelle muss diese Datei geprüft und aktualisiert werden.

| phase | case_count | top_variables | status_distribution |
|---|---:|---|---|
| 1 | 38 | REQUEST_URI(7), REQUEST_HEADERS_NAMES(5), ARGS:a(4), REQUEST_COOKIES_NAMES(4), ARGS:param1(2) | active:2, imported:36 |
| 2 | 75 | ARGS:q(18), REQUEST_BODY(10), ARGS_NAMES(6), ARGS:test(6), MULTIPART_FILENAME(4) | active:5, imported:70 |
| 3 | 12 | RESPONSE_HEADERS:Set-Cookie(4), RESPONSE_HEADERS:Location(2), RESPONSE_HEADERS:Last-Modified(1), RESPONSE_HEADERS:Content-Type(1), RESPONSE_HEADERS:X-Missing(1) | active:1, imported:11 |
| 4 | 20 | RESPONSE_BODY(20) | imported:20 |

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
