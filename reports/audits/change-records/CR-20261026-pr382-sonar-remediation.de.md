# Change Record: CR-20261026-pr382-sonar-remediation

**Sprache:** [English](CR-20261026-pr382-sonar-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261026-pr382-sonar-remediation |
| Datum (UTC) | 2026-10-26 |
| Basis-Revision | `67e363d44d5f6be7119eb6d76ade11ac75e95f42` |

## Motivation und Problemstellung

An der Basis-Revision scheiterte das verbindliche Sonar mit 118 neuen Findings und 0.81499% New-Code-Coverage gegen 80%; Analyse `e407faad-955f-49f0-9c6e-443e0629cd1c`, CE `AaF2y9jpF1KaAz-cccYD`. Der Nutzer verlangte ausdrücklich gezielte Findings-/Coverage-Korrektur bei Erhalt der integrierten Master-Pipeline und unveränderter Gates. Zwanzig andere Workflows und manueller No-CRS-Lauf `40277060029` bestanden nur an diesem historischen Head.

## Akzeptanzkriterien

Master `7a44f18edac729291d6551d068da64fa3fec4e1e`, verbindliches C++17 und beratendes C++20/23, echte Berichtsprovenienz und alle Gates erhalten. Zusätzliche Python-Offline-Units ausdrücklich autorisieren, Kernlimit 100 und 2 MiB erhalten. E2E 26, geschlossene I12-Kampagnen und schreibgeschützte Framework/MRTS/Gitlinks erhalten. Abschluss verlangt weiterhin frische vollständige Erhaltungsmessung, mindestens 80% tatsächliche New-Code-Coverage und verbindliche CI/Sonar am aktuellen veröffentlichten Head; dies ist noch nicht erfüllt.

## Implementierungsentscheidung und Begründung

Gezielte native/Python-Qualitätskorrekturen und Root-/Pfad-/Metadaten-/Rezeptgrenzkontrollen anwenden. Master-Coverage-Produzent um exakte zugelassene Offline-IDs, echtes Kind-Branch-Tracing und unabhängige rohe SHA-/Größenbelege erweitern. `xml --keep-combined` nach reproduzierter Löschung durch implizites Combine trotz `combine --keep` erhalten. Feste `PYTHON_TESTS`-Auswahl mit 13 Einträgen, 37 Go-Selektoren und native Prüfung erhalten; alle CFamily MAIN und 16 tatsächliche CI-Python-Unittest-Module TEST klassifizieren. Timeout 30→60 Minuten erhöhen, weil das gemessene Offline-Erfassungs-/Berichtsintervall allein mindestens 1216.9 Sekunden dauerte. Schema 3 dedupliziert 592 Quelleinträge ohne Verlust vollständiger Zuordnungen/Selektoren/Fälle/Validierung; Schema 1/2 bleiben lesbar. Zulassung: 1346 Fälle / 796 Ausführungen = 97 Kern / 77 + 1249 Offline / 719. Dateigröße 1,329,032 statt 2,096,001 Bytes. Referenzgraphprüfung erfolgt vor Kindern; Publisher-Nachweis/No-op-Verhalten und alle bisherigen IDs/Szenarien bleiben erhalten.

## Geänderte Dateien

- `.github/workflows/sonarqube.yml`, `sonar-project.properties`, `ci/sonar-coverage.ini`, `ci/checks/analysis/check-sonar-scope.py`, `ci/checks/analysis/run-sonar-coverage.py`.
- `ci/lib/active_test_inventory.py`, `ci/lib/active_inventory_updates.py`, `config/testing/active-cases.json`, generierte `reports/testing/test-selection-archive.generated.json`.
- Ausgewählte native Connector-Quellen und Lifecycle-Fixtures/-Helfer; Python-Lifecycle-, Inventar-, Updater-, Coverage- und Scope-Kontrollen unter `ci/`, `connectors/`, `scripts/`, `tests/`. Der finale Koordinator-Diff führt die exakte Quellliste.
- `docs/pr-382-merge-readiness.md` / `.de.md`, `docs/testing-and-evidence.md` / `.de.md`, `docs/sonarqube-analysis.md` / `.de.md` und dieses Paar. Historische Records bleiben erhalten.

## Ausgeführte Befehle

Der Koordinator beobachtete Phase 1 PASS: 105 Ausführungen / 115 Fälle ohne Skips; strikte Apache-/NGINX-/HAProxy-C17- und drei SDK-C++17-Syntaxprüfungen bestanden. Phase-2-Vereinigung PASS: 182 verschiedene Ausführungen / 314 Fälle über zwei Inventar-Digests einschließlich aller 145 neuen Ausführungen / 275 Fälle. Ein anfängliches Fixture-Namespace-Literal scheiterte; zwei reine Testpfade leiten nun den konfigurierten privaten Root ab, mit unveränderten sechs Szenarien/Assertions. Fortsetzung: 74 Ausführungen / 168 Fälle PASS ohne Skips einschließlich vier Wiederholungen. Dies ist kein einzelner Lauf an einer sauberen finalen Revision. Der erste tatsächliche Master-Python-Coverage-Produzent bestand 92 Methoden plus 955 Offline-Fälle, 568 Kind-Branch-Nachweise und eine separate ungetracte Zeitkontrolle; XML enthält 374 Dateien. Zwei gezielte Rohdaten-Erhaltungskontrollen bestanden. Der Dokumentationsworker nutzte RTK-Quell-/Textlesezugriffe, statische Überschriften-/Linkprüfungen mit Standardbibliothek und begrenztes `git diff --check`; keine Projektimporte, Tests, Generatoren oder Provider-Schreibzugriffe. Exakte Koordinator-Befehle stehen in laufgebundener Evidence; hier wird kein rekonstruierter Befehl behauptet.

Ursache des statischen Go-Vertragsfehlers war eine exakte Drei-Zeilen-Body-Erwartung, die legitime geprüfte Cache-Suffixe ablehnte. Der Guard akzeptiert nun nur diesen kanonischen Body oder das exakte Job-Cache-Suffix Envoy `go.mod` + `go.sum` / Traefik `native/go.mod`; vertrauenswürdige Go-Ausgabe, Pins und Resolver bleiben unverändert. Checker-CLI plus fünf ausgewählte Ausführungen / 18 expandierte Fälle bestanden ohne Skips und verwarfen 12 Selektor-/Cache-Abweichungsvarianten. Tatsächliche Repository-Prüfungen für Bilingualität, Dokumentationslinks und Pfadreferenzen bestanden; actionlint-Wrapper bestand, zizmor meldete null Findings und Projekt-Pins, Python `3.15.1` / 50 Jobs sowie Go-Vertragsprüfungen bestanden.

Am veröffentlichten Zwischenstand `bcde66f2cf88130c57c7e49a0d5d2a22150948da` bestanden alle 20 anderen automatischen PR-Workflows. Der verbindliche Sonar-Lauf [40298184503](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40298184503), Job `121489276419`, scheiterte vor dem Scan, weil der isolierten Sonar-Umgebung PyYAML fehlte, als der zugelassene Selektor `offline.maintenance.043` `update-workflow-tools.py` importierte. Der Workflow-Folgefix ruft den bestehenden `ci/tools/install-ci-dependencies.py` in derselben virtuellen Umgebung auf. Er nutzt den bestehenden hashgebundenen offiziellen Quellbau von PyYAML `6.0.3`, der für Python `3.15.1` bereits genehmigt war; Locks und Gates bleiben unverändert. Der Koordinator beobachtete Installations-PASS in einer frischen isolierten `3.15.1`-Umgebung, danach PASS des exakten zugelassenen Selektors: eine Methode, zwei expandierte Fälle, keine Skips. Evidence unter `/var/tmp/codex/ModSecurity-conector/runs/pr382-master421-resume-20261026`: `sonar-bootstrap/ci-dependency-build-kgjzjuxb/receipt.json` und `sonar-bootstrap/targeted/active-tests-_766u92i/summary.json`. Diese gezielte Voraussetzungskontrolle belegt keine vollständige Messung nach dem Fix, Kind-Nachweiserhaltung oder ein Quality Gate am neuen Head.

## Security-Auswirkung

Statische Prüfung fand keinen konkreten quellgestützten Bypass; unabhängige Schema-3-Kandidatenprüfung ebenfalls keinen konkreten Bypass/Regression, jeweils mit statischen Grenzen. Für 19 Kontext-Findings bestehen quellgestützte Beibehaltungsentscheidungen ohne Server-Dispositionen. Offline-Sperren, lexikalische Root-/Pfadautorisierung, vollständige Inventarvalidierung und bestehende Gate-Schwellen bleiben erhalten. Keine breite Ausnahme, Baseline-Verschiebung, Wiederherstellung eigener Collectoren oder Framework-/MRTS-Befugniserweiterung.

## Runtime-Evidence

Keine Hostkampagne wurde für diese Korrektur gestartet. E2E bleibt 26, historische I12-Host-/Matrix-/Oracle-Arbeit bleibt ohne neues `I12_COMPLETE` geschlossen. Historischer No-CRS-Erfolg an der Basis belegt nur diesen Lauf/Head; PR-#421-Evidence bleibt an ursprüngliche Revisionen gebunden.

## Bekannte Einschränkungen

Erste lokale SCM-Changed-Python-Coverage beträgt 24.791%: 10,867/41,669 Zeilen plus 3,112/14,718 Bedingungen abgedeckt. Dies ist keine Sonar-Metrik und kein 80%-PASS. Schmutzige Berichte sind nicht importfähig. Nach Rohdaten-Erhaltungskorrektur muss der vollständige Produzent erneut laufen. PR-#421-Gates und Parsing-/Include-Qualität qualifizieren diese Korrektur nicht. Architektur-HTTP-415 und CFamily-/Python-/FIFO-/TLS-Analyzergrenzen bleiben getrennt dokumentiert.

## Verbleibende Risiken

Tatsächliche terminale Serververarbeitung, Finding-Dispositionen, Coverage-Import und Quality Gate für einen neuen veröffentlichten Korrektur-Head fehlen. Weitere Coverage-Arbeit ist nötig; eine Ready-/verified_pr-Aussage ist nicht gerechtfertigt.

## Nicht ausgeführte Prüfungen mit Begründung

Frische vollständige Messung nach Erhaltungskorrektur und Scanner-Import am sauberen Head liegen noch nicht vor; das verbindliche Sonar an `bcde66f2` scheiterte wie oben dokumentiert vor der Analyse. Keine zusätzliche Host-/Matrix-/Oracle-Kampagne ist für diese begrenzte Korrektur erforderlich oder autorisiert. Repository-Sprach-/Link-/Pfadprüfungen bestanden wie oben dokumentiert; weitere finale Quellvalidierung und fehlende Coverage-/Servernachweise übernimmt der Koordinator nach Source-Freeze.

## Finaler Diff- und Review-Status

Zwischenstand `bcde66f2cf88130c57c7e49a0d5d2a22150948da` wurde normal committet und gepusht; seine Bootstrap-Korrektur wird als Folgefix vorbereitet. Zentraler aktueller Stand: [PR-#382-Status](../../../docs/pr-382-merge-readiness.de.md). PR #382 bleibt Draft; Ready, Merge in master, Release oder Deployment werden nicht behauptet. Die Gesamtkorrektur bleibt teilweise abgeschlossen, bis die oben geforderten Akzeptanznachweise vorliegen.
