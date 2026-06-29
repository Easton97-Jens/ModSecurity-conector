# Verifizierter Laufzeitlauf

**Sprache:** [English](verified-runtime-run.md) | Deutsch

Status: teilweiser Laufzeitnachweis, aktuelle `/src` No-CRS- und With-CRS-Ziele
Übergeben für ausgeführten Bereich

Aktualisiert: 30.05.2026 20:55:03 UTC

## Umwelt

Arbeitsverzeichnis:

```text
/root/git/ModSecurity-conector
```

Laufzeitumgebung:

```text
SOURCE_ROOT=/src
BUILD_ROOT=/src/ModSecurity-conector-build
REFRESH=1
```

Framework-Stammverzeichnis:

```text
/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework
```

## Ausgeführte Befehle

| Command | Result | Notes |
| --- | --- | --- |
| `make generate-test-matrix` | PASS | Generator exited 0; generated reporting is not runtime proof. |
| `make check-test-matrix` | FAIL | Exited 2 because generated reports intentionally differ from HEAD in this uncommitted HAProxy matrix update. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs` | PASS | Apache 54 PASS; NGINX 60 PASS; both 0 FAIL and 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs` | PASS | Apache 55 PASS; NGINX 61 PASS; both 0 FAIL and 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common` | PASS | Apache common 54 PASS; NGINX common 54 PASS; both 0 FAIL and 0 BLOCKED. |

Framework-lokale Prüfungen:

| Command | Result | Notes |
| --- | --- | --- |
| `modules/ModSecurity-test-Framework: make lint` | PASS | Command exited 0. |
| `modules/ModSecurity-test-Framework: make quick-check` | not found | No `quick-check` target was found in the framework Makefile. |
| `modules/ModSecurity-test-Framework: make check-test-matrix` | PASS | Command exited 0; it printed a warning that framework-local `config/testing/import-status.json` was not found. |

Frühere `/src`-Connector-Smoke-Runs sind noch in anderen Berichten dokumentiert, aber die
Die oben genannten aktuellen Zielbeweise bilden die Grundlage für diese Datei.

## Nachweisdateien

Gewöhnlicher Smoke:

- `/src/ModSecurity-conector-build/results/apache-summary.json`
- `/src/ModSecurity-conector-build/results/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/connector-summary.json`
- `/src/ModSecurity-conector-build/results/apache.rc`
- `/src/ModSecurity-conector-build/results/nginx.rc`

No-CRS-Ziel:

- `/src/ModSecurity-conector-build/results/no-crs/apache-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/connector-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/apache.rc`
- `/src/ModSecurity-conector-build/results/no-crs/nginx.rc`

With-CRS-Ziel:

- `/src/ModSecurity-conector-build/results/with-crs/apache-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/connector-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/apache.rc`
- `/src/ModSecurity-conector-build/results/with-crs/nginx.rc`

CRS Pfade:

- CRS Quelle: `/src/coreruleset`
- CRS Laufzeitpräambel:
  `/src/ModSecurity-conector-build/crs/modsecurity-crs-preamble.conf`

## Zusammenfassung zählt

| Target | Connector | PASS | FAIL | BLOCKED | Result file |
| --- | --- | ---: | ---: | ---: | --- |
| `smoke-common` | Apache | 54 | 0 | 0 | `/src/ModSecurity-conector-build/results/apache-summary.txt` |
| `smoke-common` | NGINX | 54 | 0 | 0 | `/src/ModSecurity-conector-build/results/nginx-summary.txt` |
| `test-no-crs` | Apache | 54 | 0 | 0 | `/src/ModSecurity-conector-build/results/no-crs/apache-summary.txt` |
| `test-no-crs` | NGINX | 60 | 0 | 0 | `/src/ModSecurity-conector-build/results/no-crs/nginx-summary.txt` |
| `test-with-crs` | Apache | 55 | 0 | 0 | `/src/ModSecurity-conector-build/results/with-crs/apache-summary.txt` |
| `test-with-crs` | NGINX | 61 | 0 | 0 | `/src/ModSecurity-conector-build/results/with-crs/nginx-summary.txt` |

Alle aufgelisteten `.rc`-Dateien für diese Ziele enthalten `0`.

## Laufzeitüberprüfung ohne CRS

Befehl:

```sh
SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs
```

Ergebnis: PASS.

Wichtige Fallbeweise:

- Apache `action_status_401_phase1_block`: PASS, erwartet 401, tatsächlich 401.
- NGINX `action_status_401_phase1_block`: PASS, erwartet 401, tatsächlich 401.
- Apache `phase1_header_block`: PASS, erwartet 403, tatsächlich 403.
- NGINX `phase1_header_block`: PASS, erwartet 403, tatsächlich 403.
- Apache `response_body_pass`: PASS, erwartet 200, tatsächlich 200.
- NGINX `response_body_pass`: PASS, erwartet 200, tatsächlich 200.

`response_body_pass` ist nur ein Durchgangsbeweis und beweist nicht
RESPONSE_BODY Blockierung.

## With-CRS-Laufzeitüberprüfung

Befehl:

```sh
SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs
```

Ergebnis: PASS.

CRS Setup-Nachweis:

- `MODSECURITY_TEST_VARIANT=with-crs`
- CRS Quelle: `/src/coreruleset`
- CRS Laufzeitpräambel:
  `/src/ModSecurity-conector-build/crs/modsecurity-crs-preamble.conf`

Wichtige Fallbeweise:

| Connector | Case | Expected | Actual | Status |
| --- | --- | ---: | ---: | --- |
| Apache | `action_status_401_phase1_block` | 403 | 403 | PASS |
| NGINX | `action_status_401_phase1_block` | 403 | 403 | PASS |
| Apache | `crs_sqli_anomaly_block` | 403 | 403 | PASS |
| NGINX | `crs_sqli_anomaly_block` | 403 | 403 | PASS |

Die With-CRS 403-Erwartung für `action_status_401_phase1_block` ist bereichsbezogen
durch die `expect.variants.with-crs.status` des Framework-Falls. Die Basis
Die No-CRS-Erwartung bleibt bei 401.

## RESPONSE_BODY

RESPONSE_BODY Sperrung verifiziert: Nein.

Grund:

- `response_body_pass` ist nur ein Durchgangsbeweis.
- NGINX-spezifische Phase-4-Zeilen in den aktuellen Zusammenfassungen sind Pass-Through- oder
Nur Protokollbeweise, keine blockierenden Nachweise.
- Keine aktuellen Runtime-Nachweise belegen einen blockierenden Response-Body-Trigger mit a
  Blockierungsergebnis wie HTTP 403 für Apache und NGINX.

## Gesamtentscheidungen

- Apache No-CRS-Bereich: PASS, 54 PASS, 0 FAIL, 0 BLOCKIERT.
- NGINX Kein CRS-Bereich: PASS, 60 PASS, 0 FAIL, 0 BLOCKIERT.
- Apache With-CRS-Bereich: PASS, 55 PASS, 0 FAIL, 0 BLOCKIERT.
- NGINX With-CRS-Bereich: PASS, 61 PASS, 0 FAIL, 0 BLOCKIERT.
- CRS SQLi-Anomaliefall: PASS für Apache und NGINX.
- Ehemalige With-CRS `action_status_401_phase1_block`-Konflikt: behoben durch a
  begrenzte With-CRS-Erwartung.
- Apache-Bewertung: teilweise.
- NGINX Bewertung: teilweise.
- RESPONSE_BODY Blockierung: nicht überprüft.
- Mehr als `partial`: in diesem Lauf nicht zulässig.
- Vollständige Laufzeitüberprüfung: Nein.
