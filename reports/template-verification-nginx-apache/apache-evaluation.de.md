# Apache-Bewertung

**Sprache:** [English](apache-evaluation.md) | Deutsch

Status: überprüft

Apache-Bewertung: teilweise mit aktuellem `/src` No-CRS PASS und With-CRS PASS
für den ausgeführten Umfang.

Vorlagenausrichtung: ausgerichtet für Gerüst, origin/license, Metadaten, Build,
Harness, externe Testreferenzen und ausgeführter No-CRS/With-CRS Laufzeitbereich.
Detaillierte phasenweise Ausrichtung:
`reports/template-verification-nginx-apache/apache-template-alignment.md`.

Grund: `connectors/apache` enthält eine dem Adapter gehörende Quellstruktur.
Autotools/APXS Build-Dateien, Metadaten, Ursprungsdokumentation, Harness und
Dokumentation. Aktuelle `/src`-Laufzeitziele gelten für den ausgeführten Bereich, aber
Apache bleibt `partial`, da keine Apache-spezifischen YAML-Fälle gefunden wurden,
RESPONSE_BODY Blockierung wird nicht überprüft, und die vollständige Mindestmatrix ist es nicht
abgeschlossen.

## Zusammenfassung der Nachweise

| Area | Status | Evidence |
| --- | --- | --- |
| README/docs | OK | `connectors/apache/README.md`, `connectors/apache/docs/` |
| Local test folder | OK | `connectors/apache/tests` is absent. |
| Adapter-owned source | OK | `connectors/apache/src/`, `connectors/apache/metadata.c`, `connectors/apache/ORIGIN.md` |
| Common smoke | PASS | Apache 54 PASS, 0 FAIL, 0 BLOCKED. |
| No-CRS target | PASS | Apache 54 PASS, 0 FAIL, 0 BLOCKED. |
| With-CRS target | PASS | Apache 55 PASS, 0 FAIL, 0 BLOCKED. |
| No-CRS action status case | PASS | `action_status_401_phase1_block` expected 401, actual 401. |
| With-CRS action status case | PASS | `action_status_401_phase1_block` expected 403, actual 403. |
| CRS SQLi case | PASS | `crs_sqli_anomaly_block` expected 403, actual 403. |
| RESPONSE_BODY blocking | Not verified | `response_body_pass` is pass-through evidence only. |
| Apache-specific YAML cases | Missing | Only `README.md` found under framework Apache-specific path. |
| More than `partial` | Not allowed | Full matrix and RESPONSE_BODY blocking evidence remain incomplete. |
| Template phase alignment | Aligned | See `apache-template-alignment.md`. |

## Aktuelle Laufzeitzählungen

| Command | Scope | PASS | FAIL | BLOCKED |
| --- | --- | ---: | ---: | ---: |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common` | common | 54 | 0 | 0 |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs` | all/no-crs | 54 | 0 | 0 |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs` | all/with-crs | 55 | 0 | 0 |

Nachweisdateien:

- `/src/ModSecurity-conector-build/results/apache-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/apache-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/apache-summary.json`
- `/src/ModSecurity-conector-build/results/apache-results.jsonl`
- `/src/ModSecurity-conector-build/results/no-crs/apache-results.jsonl`
- `/src/ModSecurity-conector-build/results/with-crs/apache-results.jsonl`

## CRS Variantennachweis

| Variant | Case | Expected | Actual | Status |
| --- | --- | ---: | ---: | --- |
| No-CRS | `action_status_401_phase1_block` | 401 | 401 | PASS |
| With-CRS | `action_status_401_phase1_block` | 403 | 403 | PASS |
| With-CRS | `crs_sqli_anomaly_block` | 403 | 403 | PASS |

Die With-CRS 403-Erwartung ist im Framework-Testfall gültig und nicht
Ersetzen Sie die grundlegende No-CRS 401-Erwartung.

## Zusammenfassung der Kontrollkästchen

- [x] README vorhanden.
- [x] Dokumente vorhanden.
- [x] Lokaler Testordner entfernt.
- [x] Harness/adapter Struktur vorhanden.
- [x] Aktueller `/src` gemeinsamer Apache-Smoke bestanden.
- [x] Aktuelles `/src` No-CRS-Apache-Ziel übergeben.
- [x] Aktuelles `/src` With-CRS Apache-Ziel übergeben.
- [x] Aktueller `/src` Apache CRS SQLi-Anomaliefall bestanden.
- [x] No-CRS `action_status_401_phase1_block` als 401/401 PASS erhalten.
- [x] With-CRS `action_status_401_phase1_block` dokumentiert als 403/403 PASS.
- [ ] RESPONSE_BODY Blockierung überprüft.
- [ ] Apache-spezifische YAML-Dateien gefunden.
- [ ] Vollständige Mindestlaufzeitmatrix überprüft.
- [ ] Der Connector kann über `partial` hinaus hochgestuft werden.

## Entscheidung

Apache bleibt `partial`. Aktuelle No-CRS-, With-CRS- und allgemeine Laufzeitziele
sind PASS für den ausgeführten `/src`-Bereich. Die frühere With-CRS 401/403-Nichtübereinstimmung ist
wird durch eine bereichsbezogene Framework-Erwartung gelöst. Apache kann immer noch nicht hochgestuft werden
über `partial` hinaus, da RESPONSE_BODY Blockierung und die vollständige Minimalmatrix
werden nicht überprüft und es wurden keine Apache-spezifischen YAML-Fälle gefunden.
