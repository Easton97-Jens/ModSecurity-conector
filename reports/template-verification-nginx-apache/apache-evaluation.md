# Apache Evaluation

Status: reviewed

Apache-Bewertung: partial mit aktuellem `/src` No-CRS-PASS und With-CRS-FAIL-Scope

Begründung: `connectors/apache` enthält eine adapter-owned Quellstruktur,
Autotools/APXS-Builddateien, Metadaten, Herkunftsdokumentation, Harness und
Dokumentation. Die Bewertung ist aber nur teilweise vollständig, weil der
aktuelle `/src` Common-Runtime-Run und `test-no-crs` nur die ausgefuehrten
Apache-Faelle belegen, nicht die vollstaendige Mindestmatrix. `test-with-crs`
lief, ist aber wegen `action_status_401_phase1_block` FAIL: erwartet 401,
tatsaechlich 403. Apache-spezifische YAML-Faelle wurden nicht gefunden,
Status-Angaben sind nicht konsistent, und RESPONSE_BODY blocking ist laut
Repo-Evidenz nicht verifiziert. Die separate Analyse
`crs-action-status-401-analysis.md` bewertet den With-CRS 401/403-Mismatch als
nicht eindeutig verursacht; eine connector-spezifische Apache-Ursache ist
nicht belegt, weil NGINX denselben Mismatch zeigt.

Scaffold-Regeln fuer neue Connectoren und die Grenze zwischen `partial`,
`runtime-smoke-verified` und `not-verified` sind in
`connector-scaffold-decisions.md` dokumentiert.

## Bewertung

| Bereich | Status | Begründung | Beleg/Pfad |
| --- | --- | --- | --- |
| README vorhanden | OK | README beschreibt Adapter-Quellen, Harness, Metadaten und Grenzen. | `connectors/apache/README.md` |
| docs vorhanden | OK | `architecture.md`, `build.md`, `public-sources.md` und `validation.md` vorhanden. | `connectors/apache/docs/` |
| validation.md vorhanden | OK | Datei wurde ergänzt und verweist auf Runtime-Evidenzgrenzen. | `connectors/apache/docs/validation.md` |
| Lokaler Testordner | OK | `connectors/apache/tests` wurde entfernt. Ausführbare Connector-Tests werden nicht connector-lokal gepflegt. | `connectors/apache/docs/validation.md` |
| Harness/Adapter-Struktur | OK | Harness-Skript, Smoke-Konfig, Autotools/APXS-Dateien, `src/`, `metadata.*`, `ORIGIN.md` vorhanden. | `connectors/apache/` |
| Status-Angaben konsistent | Teilweise | README/build/harness nennen adapter-owned, mehrere docs/TODO-Dateien nennen weiterhin `scaffolded`. | `connectors/apache/README.md`, `connectors/apache/TODO.md`, `connectors/apache/docs/architecture.md` |
| Request-Headers geprüft/verifiziert | OK | In Repo-Evidenz als `REQUEST_HEADERS` in Apache und NGINX `verified_variables` dokumentiert. | `reports/testing/real-world-connector-validation.md` |
| Request-Body geprüft/verifiziert | OK | In Repo-Evidenz als `REQUEST_BODY` in Apache und NGINX `verified_variables` dokumentiert. | `reports/testing/real-world-connector-validation.md` |
| Response-Headers geprüft/verifiziert | OK | In Repo-Evidenz als `RESPONSE_HEADERS` in Apache und NGINX `verified_variables` dokumentiert. | `reports/testing/real-world-connector-validation.md` |
| Response-Body geprüft/verifiziert | Nicht verifiziert | RESPONSE_BODY bleibt nicht verifiziert und nicht promoted; pass-through ist kein Blocking-Nachweis. | `reports/testing/real-world-connector-validation.md`, `reports/testing/generated/apache-runtime-results.generated.md` |
| Automatischer Fetch/Prepare | OK | `make fetch-deps` hat `/src/ModSecurity_V3` geholt; Apache-Prepare hat PCRE2, httpd/APR/APR-util, libmodsecurity und das Apache-Modul vorbereitet. | `reports/template-verification-nginx-apache/component-download-check.md` |
| `/src` Runtime-Prüflauf | Teilweise OK | Der aktuelle `/src` Common-Run hat 54 PASS, 0 FAIL und 0 BLOCKED fuer Apache; das ist kein vollstaendiger Runtime-Nachweis und kein RESPONSE_BODY-Blocking-Nachweis. | `reports/template-verification-nginx-apache/verified-runtime-run.md` |
| Gemeinsamer Include-Pfad | OK fuer Build | Der Apache-Buildlog zeigt `-I/root/git/ModSecurity-conector/common/include`; derselbe Header `msconnector/rule_load_stats.h` wird in `connectors/apache/src/mod_security3.h` eingebunden. | `/src/ModSecurity-conector-build/logs/apache/apache-make.log`, `connectors/apache/build/apxs-wrapper.in`, `connectors/apache/src/mod_security3.h` |
| Smoke-Test aktuell ausführbar | Teilweise OK | `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-apache` bestand; die finalen Apache-Resultate aus `make smoke-common` zeigen 54 PASS, 0 FAIL und 0 BLOCKED. | `reports/template-verification-nginx-apache/verified-runtime-run.md` |
| No-CRS Runtime aktuell | OK | `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs` zeigt Apache 54 PASS, 0 FAIL und 0 BLOCKED. | `/src/ModSecurity-conector-build/results/no-crs/apache-summary.json` |
| With-CRS Runtime aktuell | FAIL | `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs` zeigt Apache 54 PASS, 1 FAIL und 0 BLOCKED; `action_status_401_phase1_block` erwartete 401 und erhielt 403. | `/src/ModSecurity-conector-build/results/with-crs/apache-summary.json` |
| With-CRS 401/403-Analyse | Needs evidence | Exact cause not proven; likely With-CRS expected-status/context mismatch involving CRS/default-action behavior or testcase expectation. Not evidenced as Apache-specific because NGINX shows the same result. | `reports/template-verification-nginx-apache/crs-action-status-401-analysis.md` |
| CRS SQLi Case aktuell | OK | `crs_sqli_anomaly_block` bestand mit erwarteten 403 und tatsächlichen 403. | `/src/ModSecurity-conector-build/results/with-crs/apache-summary.json` |
| Direktes Harness-Skript | OK fuer einen Fall | `connectors/apache/harness/run_apache_smoke.sh` wurde versucht und bestand fuer `phase1_header_block` mit HTTP 403. | `connectors/apache/harness/run_apache_smoke.sh`, `reports/template-verification-nginx-apache/runtime-test-run-src.md` |
| Coverage Matrix | Teilweise | Matrix angelegt; `TEST-COVERAGE-SUMMARY.md` meldet 140 YAML-Fälle, Apache attempted 133, FORCE_ALL Apache Snapshot FAIL mit 87 PASS und 46 FAIL; der aktuelle `/src` Common-Run hat 54 PASS, aber RESPONSE_BODY blocking bleibt nicht verifiziert. | `connectors/apache/docs/coverage-decision-matrix.md`, `TEST-COVERAGE-SUMMARY.md`, `reports/template-verification-nginx-apache/verified-runtime-run.md` |
| Apache-spezifische YAML-Fälle | Fehlt | Im Apache-spezifischen Framework-Case-Ordner wurde nur `README.md` gefunden. | `modules/ModSecurity-test-Framework/tests/cases/connector-specific/apache/README.md` |
| Scaffold-Entscheidungen | OK | Apache-spezifische YAML-Fälle bleiben deferred; externe Testpfade, Status-Vokabular, RESPONSE_BODY-Mindest-Evidenz und `partial`-Grenzen sind dokumentiert. | `reports/template-verification-nginx-apache/connector-scaffold-decisions.md` |
| Offene Fragen dokumentiert | OK | Offene Fragen im Prüfbericht dokumentiert. | `reports/template-verification-nginx-apache/open-questions.md` |

## Checkbox-Zusammenfassung

- [x] README vorhanden.
- [x] docs vorhanden.
- [x] `validation.md` vorhanden.
- [x] Lokaler Testordner entfernt.
- [x] Harness/Adapter-Struktur vorhanden.
- [ ] Status: teilweise - Status-Angaben sind nicht konsistent.
- [x] Request-Headers repo-seitig als verifiziert dokumentiert.
- [x] Request-Body repo-seitig als verifiziert dokumentiert.
- [x] Response-Headers repo-seitig als verifiziert dokumentiert.
- [ ] Status: nicht verifiziert - Response-Body blocking. Nicht verifiziert -
      keine ausreichende Repo-Evidenz gefunden.
- [x] Status: erledigt - `make fetch-deps` hat `/src/ModSecurity_V3`
      erfolgreich vorbereitet.
- [x] Status: erledigt - `/src`-basierter Apache-Smoke
      `phase1_header_block` bestand mit HTTP 403.
- [x] Status: erledigt - aktueller `/src` Common-Run dokumentiert Apache mit
      54 PASS, 0 FAIL und 0 BLOCKED.
- [x] Status: erledigt - aktueller `/src` No-CRS-Run dokumentiert Apache mit
      54 PASS, 0 FAIL und 0 BLOCKED.
- [ ] Status: fail - aktueller `/src` With-CRS-Run dokumentiert Apache mit
      54 PASS, 1 FAIL und 0 BLOCKED. FAIL:
      `action_status_401_phase1_block`, erwartet 401, tatsaechlich 403.
- [ ] Status: needs evidence - genaue Ursache fuer den With-CRS 401/403-
      Mismatch nicht eindeutig belegt; siehe
      `crs-action-status-401-analysis.md`.
- [x] Status: erledigt - aktueller `/src` With-CRS-Run dokumentiert
      `crs_sqli_anomaly_block` mit erwarteten 403 und tatsaechlichen 403.
- [x] Status: erledigt - der Apache-Buildlog enthaelt den gemeinsamen
      Include-Pfad `common/include`.
- [x] Status: erledigt - Direktes Apache-Harness bestand fuer
      `phase1_header_block` mit HTTP 403.
- [x] Status: erledigt - Coverage-Decision-Matrix angelegt.
- [ ] Status: fail - Force-all Apache Runtime-Snapshot ist Gesamtstatus FAIL
      mit 87 PASS und 46 FAIL.
- [ ] Status: fehlt - Apache-spezifische YAML-Dateien wurden nicht gefunden.
- [ ] Status: nicht verifiziert - Ausführbare Apache-Connector-Tests werden
      nicht connector-lokal gepflegt.

## Entscheidung

Apache bleibt `partial`. Die Connector-Struktur und dokumentierte
Repo-Evidenz sind vorhanden. Der aktuelle `/src` Common-Run dokumentiert
Apache mit 54 PASS, 0 FAIL und 0 BLOCKED, einschliesslich
`phase1_header_block` mit HTTP 403. Der aktuelle No-CRS-Run ist PASS. Der
aktuelle With-CRS-Run ist FAIL, obwohl `crs_sqli_anomaly_block` fuer Apache
PASS ist. Die Ursache fuer den 401/403-Mismatch ist nicht eindeutig belegt;
der Befund spricht eher fuer einen With-CRS Erwartungs-/Kontexteffekt als fuer
einen Apache-spezifischen Connector-Fehler. Das ist kein vollstaendiger
Runtime-Nachweis. Der Apache-Buildlog enthaelt den gemeinsamen Include-Pfad
`common/include`; Status-Angaben sind teilweise uneinheitlich,
Apache-spezifische YAML-Faelle wurden nicht gefunden, und RESPONSE_BODY
blocking ist nicht verifiziert.
