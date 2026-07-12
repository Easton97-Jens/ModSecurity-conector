> Status: Historisch
> Ersetzt durch: [../../current/six-connector-core-completion.de.md](../../current/six-connector-core-completion.de.md)
> Datum: Als historischer Bericht bei der Repository-Reorganisation am 2026-07-12 beibehalten
> Evidenzgrenze: Historische Planung, Bewertung oder Momentaufnahme; keine aktuelle kanonische Evidence.

# NGINX Auswertung

**Sprache:** [English](nginx-evaluation.md) | Deutsch

Status: überprüft

NGINX Bewertung: teilweise mit aktuellem `/src` No-CRS PASS und With-CRS PASS für
ausgeführter Umfang.

Vorlagenausrichtung: ausgerichtet für Gerüst, origin/license, Metadaten, Build,
Harness, externe Testreferenzen und ausgeführter No-CRS/With-CRS Laufzeitbereich.
Detaillierte phasenweise Ausrichtung:
`reports/archive/template-verification-nginx-apache/nginx-template-alignment.md`.

Grund: `connectors/nginx` enthält einen adaptereigenen Quellbaum, Metadaten,
Ursprungsdokumentation, Harness-Dateien und Connector-Dokumente. Aktuelle `/src`
Laufzeitziele gelten für den ausgeführten Bereich, einschließlich des CRS-spezifischen
Erwartung für `action_status_401_phase1_block`. NGINX bleibt `partial`
denn RESPONSE_BODY Blockierung ist nicht verifiziert und die volle Mindestlaufzeit
Matrix ist nicht vollständig.

## Zusammenfassung der Nachweise

| Area | Status | Evidence |
| --- | --- | --- |
| README/docs | OK | `connectors/nginx/README.md`, `connectors/nginx/docs/` |
| Local test folder | OK | `connectors/nginx/tests` is absent. |
| Adapter-owned source | OK | `connectors/nginx/src/`, `connectors/nginx/metadata.c`, `connectors/nginx/ORIGIN.md` |
| NGINX build include contract | OK | `MSCONNECTOR_COMMON_INC=$CONNECTOR_ROOT/common/include` is supported by `connectors/nginx/config`. |
| Common smoke | PASS | NGINX 54 PASS, 0 FAIL, 0 BLOCKED. |
| No-CRS target | PASS | NGINX 60 PASS, 0 FAIL, 0 BLOCKED. |
| With-CRS target | PASS | NGINX 61 PASS, 0 FAIL, 0 BLOCKED. |
| No-CRS action status case | PASS | `action_status_401_phase1_block` expected 401, actual 401. |
| With-CRS action status case | PASS | `action_status_401_phase1_block` expected 403, actual 403. |
| CRS SQLi case | PASS | `crs_sqli_anomaly_block` expected 403, actual 403. |
| Historical 11 BLOCKED rows | Resolved | Documented as environment/docroot permission blocker in earlier reports. |
| RESPONSE_BODY blocking | Not verified | Current response-body rows are pass-through or log-only evidence. |
| More than `partial` | Not allowed | Full matrix and RESPONSE_BODY blocking evidence remain incomplete. |
| Template phase alignment | Aligned | See `nginx-template-alignment.md`. |

## Aktuelle Laufzeitzählungen

| Command | Scope | PASS | FAIL | BLOCKED |
| --- | --- | ---: | ---: | ---: |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common` | common | 54 | 0 | 0 |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs` | all/no-crs | 60 | 0 | 0 |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs` | all/with-crs | 61 | 0 | 0 |

Nachweisdateien:

- `/src/ModSecurity-conector-build/results/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/nginx-results.jsonl`
- `/src/ModSecurity-conector-build/results/no-crs/nginx-results.jsonl`
- `/src/ModSecurity-conector-build/results/with-crs/nginx-results.jsonl`

## CRS Variantennachweis

| Variant | Case | Expected | Actual | Status |
| --- | --- | ---: | ---: | --- |
| No-CRS | `action_status_401_phase1_block` | 401 | 401 | PASS |
| With-CRS | `action_status_401_phase1_block` | 403 | 403 | PASS |
| With-CRS | `crs_sqli_anomaly_block` | 403 | 403 | PASS |

Die With-CRS 403-Erwartung ist im Framework-Testfall gültig und nicht
Ersetzen Sie die grundlegende No-CRS 401-Erwartung.

## Historischer Blocker

Beim früheren gemeinsamen Lauf NGINX waren 43 PASS und 11 GESPERRT. Diese Reihen waren es nicht
wird für den historischen Lauf als PASS behandelt. Sie wurden nach der Docroot-Arbeit erneut ausgeführt
übergeordnetes Element wurde nach `BUILD_ROOT` verschoben; aktueller `/src` führt Datensatz 0 BLOCKIERT aus.
Details finden Sie in `nginx-docroot-permission-analysis.md` und
`nginx-blocked-runtime-cases.md`.

## Checkliste

- [x] README vorhanden.
- [x] Dokumente vorhanden.
- [x] Lokaler Testordner entfernt.
- [x] Harness/adapter Struktur vorhanden.
- [x] NGINX Build kann `common/include/msconnector/rule_load_stats.h` finden.
- [x] Aktuelle `/src` NGINX gemeinsamer Smoke-Test bestanden.
- [x] Aktuelles `/src` NGINX No-CRS-Ziel erreicht.
- [x] Aktuelles `/src` NGINX With-CRS-Ziel bestanden.
- [x] Aktueller `/src` NGINX CRS SQLi-Anomaliefall bestanden.
- [x] No-CRS `action_status_401_phase1_block` als 401/401 PASS erhalten.
- [x] With-CRS `action_status_401_phase1_block` dokumentiert als 403/403 PASS.
- [x] Historische 11 BLOCKED Zeilen dokumentiert und erneut ausgeführt.
- [ ] RESPONSE_BODY Blockierung überprüft.
- [ ] Vollständige Mindestlaufzeitmatrix überprüft.
- [ ] Der Connector kann über `partial` hinaus hochgestuft werden.

## Entscheidung

NGINX bleibt `partial`. Aktuelle No-CRS-, With-CRS- und allgemeine Laufzeitziele
sind PASS für den ausgeführten `/src`-Bereich. Die frühere With-CRS 401/403-Nichtübereinstimmung ist
wird durch eine bereichsbezogene Framework-Erwartung gelöst. NGINX kann immer noch nicht hochgestuft werden
über `partial` hinaus, da RESPONSE_BODY Blockierung und die vollständige Minimalmatrix
sind nicht verifiziert.
