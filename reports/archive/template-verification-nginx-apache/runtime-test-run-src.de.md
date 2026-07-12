> Status: Historisch
> Ersetzt durch: [../../current/six-connector-core-completion.de.md](../../current/six-connector-core-completion.de.md)
> Datum: Als historischer Bericht bei der Repository-Reorganisation am 2026-07-12 beibehalten
> Evidenzgrenze: Historische Planung, Bewertung oder Momentaufnahme; keine aktuelle kanonische Evidence.

# Laufzeittestlauf unter `/src`

**Sprache:** [English](runtime-test-run-src.md) | Deutsch

Status: aktueller `/src` führt Smoke-Tests aus PASS für den ohne CRS und mit CRS ausgeführten Bereich

## Aktuelles Umfeld

```text
SOURCE_ROOT=/src
BUILD_ROOT=/src/ModSecurity-conector-build
REFRESH=1
```

Arbeitsverzeichnis:

```text
<repository-root>
```

## Befehle

| Command | Result | Summary |
| --- | --- | --- |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-apache` | PASS | Apache source-build smoke completed before later result directories were refreshed. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-nginx` | PASS | NGINX 60 PASS, 0 FAIL, 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common` | PASS | Apache 54 PASS, 0 FAIL, 0 BLOCKED; NGINX 54 PASS, 0 FAIL, 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs` | PASS | Apache 54 PASS, 0 FAIL, 0 BLOCKED; NGINX 60 PASS, 0 FAIL, 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs` | PASS | Apache 55 PASS, 0 FAIL, 0 BLOCKED; NGINX 61 PASS, 0 FAIL, 0 BLOCKED. |

## Nachweisdateien

Gewöhnlicher Smoke:

- `/src/ModSecurity-conector-build/results/apache-summary.json`
- `/src/ModSecurity-conector-build/results/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/connector-summary.json`

Kein CRS:

- `/src/ModSecurity-conector-build/results/no-crs/apache-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/connector-summary.json`

With-CRS:

- `/src/ModSecurity-conector-build/results/with-crs/apache-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/connector-summary.json`

## Kein CRS

- Apache: 54 PASS, 0 FAIL, 0 BLOCKIERT.
- NGINX: 60 PASS, 0 FAIL, 0 GESPERRT.
- Apache `phase1_header_block`: PASS, erwartet 403, tatsächlich 403.
- NGINX `phase1_header_block`: PASS, erwartet 403, tatsächlich 403.
- Apache `response_body_pass`: PASS, erwartet 200, tatsächlich 200.
- NGINX `response_body_pass`: PASS, erwartet 200, tatsächlich 200.
- `response_body_basic_block`: nicht in den No-CRS-Zusammenfassungen vorhanden.

## With-CRS

- CRS Quelle beobachtet: `/src/coreruleset`.
- CRS Laufzeitpräambel beobachtet:
  `/src/ModSecurity-conector-build/crs/modsecurity-crs-preamble.conf`.
- Apache: 55 PASS, 0 FAIL, 0 BLOCKIERT.
- NGINX: 61 PASS, 0 FAIL, 0 GESPERRT.
- Apache `crs_sqli_anomaly_block`: PASS, erwartet 403, tatsächlich 403.
- NGINX `crs_sqli_anomaly_block`: PASS, erwartet 403, tatsächlich 403.
- Apache `action_status_401_phase1_block`: PASS, erwartet 403, tatsächlich 403.
- NGINX `action_status_401_phase1_block`: PASS, erwartet 403, tatsächlich 403.

Das With-CRS-Ziel ist daher PASS für den aktuell ausgeführten `/src`-Bereich.
Die grundlegende No-CRS-Erwartung bleibt 401; Die With-CRS 403-Erwartung ist
Variantenspezifisch.

## Historischer NGINX Docroot-Blocker

Der vorherige `/src`-Berichtsstatus hatte 11 NGINX BLOCKED Zeilen. Dieser Zustand ist
erhalten in `nginx-blocked-runtime-cases.md`. Die aktuellen Wiederholungen haben das Problem behoben
BLOCKED Zeilen, nachdem das NGINX Harness-Arbeitsverzeichnis unten platziert wurde
`BUILD_ROOT`.

## RESPONSE_BODY

RESPONSE_BODY Sperrung verifiziert: Nein.

`response_body_pass` ist ein Durchgangsfall. NGINX Phase-4 pass-through/log-only
Reihen blockieren keine Nachweise. Die aktuellen No-CRS- und With-CRS-Zusammenfassungen tun dies
`response_body_basic_block` nicht einschließen.

## Entscheidungen

- Apache bleibt `partial`.
- NGINX bleibt `partial`.
- Laufzeitziel ohne CRS: PASS.
- With-CRS-Laufzeitziel: PASS.
- CRS SQLi-Anomaliefall: PASS für beide Konnektoren.
- Vollständige Laufzeitüberprüfung: Nein.
