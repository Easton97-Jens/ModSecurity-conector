# Change Record: CR-20261025-pr382-global-inventory-coverage

**Sprache:** [English](CR-20261025-pr382-global-inventory-coverage.md) | Deutsch

Parent-Inventar-/Coverage-Migration. Auslieferungsevidence am exakten veröffentlichten Head: [PR #382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382).

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261025-pr382-global-inventory-coverage |
| Datum (UTC) | 2026-10-25 |
| Basis-Revision | `d510d21dba7eab3c9f0ccbe579fbc9c105eb3da1` |

## Motivation und Problemstellung

Ältere führende Dokumente verlangten abgeschlossene I12-Arbeit, automatische Defaults wählten Tausende Testdefinitionen aus und Sonar Automatic Analysis importierte keine Coverage. Historische Ergebnisse bleiben erhalten; aktiver Status sowie Auswahl-/Messproduzenten werden korrigiert.

## Akzeptanzkriterien

Ein global expandiertes Inventar lässt höchstens 100 Verhaltensfälle vor dem Start ausgewählter Kinder zu. Alle automatischen Defaults werden daraus abgeleitet. Echte Reports müssen erzeugt/importiert und plausible revisionsgebundene Metriken belegt werden. Bestehende Gates einschließlich 80% New-Code-Coverage bleiben unverändert. Ready erfordert exakte lokale/Remote-/PR-Identität, aktuelle Basis, erfolgreiche Pflicht-CI/Sonar und erledigte erforderliche Rückmeldungen. Framework/MRTS und historische I12-Qualifikation bleiben unverändert.

## Implementierungsentscheidung und Begründung

`config/testing/active-cases.json`, geschlossene Selektoren und Quellhashes verwenden; Überlauf, unbekannte/leere Auswahl, Abweichungen und alternative ausführbare Kataloge ohne Kürzung ablehnen. Python-Discovery leitet sich aus denselben Zielen ab. Spezialprüfungen hinter ausdrücklichem `ON_DEMAND_TESTS=1` erhalten und ein nicht ausführbares Definitionsarchiv generieren. Runtime-Sammler zählen unabhängige Fälle und verwenden ausschließlich eine identische kanonische Readiness-Transaktion wieder.

Tatsächliche Python-Zeilenereignisse und geeignete Kinder desselben Präfixes/derselben UID, native Profile für vier Go-Module sowie echte GCC/gcov-C-/C++-Einheiten messen. Revision, Inventar, Quell-/Reporthashes, Toolchains, SDK und Rollen-/Konfigurationseingaben binden; Import erfordert saubere passende Quellen. Einzeln geprüfte Fixtures als TEST klassifizieren; gemischte Betriebswerkzeuge bleiben MAIN. Keine Produktionsausschlüsse, künstlichen Treffer, Baseline-Verschiebung oder Gate-Abschwächung.

## Geänderte Dateien

Inventar/Coverage: `config/testing/active-cases.json`, `ci/lib/active_test_inventory.py`, `ci/lib/active_coverage.py`, `ci/lib/python_coverage_bootstrap.py`, `ci/tools/run-active-tests.py`, `ci/tools/collect-active-coverage.py`, ihre beiden Kontrollmodule, `tests/__init__.py` und verzögerte Hooks in erhaltenen Testmodulen. Integration: Root-/Komponenten-Makefiles, Workflows und verschachtelte Build-/Runtime-Helfer. Analyse: beide Sonar-Properties, `config/testing/sonar-source-roles.json`, gemeinsamer Klassifizierer/Generator, Scanner-Workflow und unveränderlicher Action-Lock/Updater-Allowlisten. Archiv: `ci/tools/update-test-archive.py` und `reports/testing/test-selection-archive.generated.json`.

EN/DE-Paare: aktuelle Abschluss-/Quellrollendokumente, historische Checklist/Handoff/Matrix/Eventvertrag/#410-Abschluss und Phase-4-/Body-Inspection-Verweise, CI-/Test-/Variablenanleitungen sowie dieser Record. Der Git-Diff ist die vollständige Dateiliste.

## Ausgeführte Befehle

RTK umschließt jeden lokalen Shell-Befehl. Beobachtete Verfahren umfassen `ci/tools/run-active-tests.py --check`, ausgewählte Kontrollen, `ci/tools/collect-active-coverage.py run --strict-skips --output-root <external-run-root>`, `ci/tools/sync-sonar-test-scope.py --check`, gepinntes actionlint/zizmor, Workflow-Versionsverträge und `git diff --check`. Detaillierte Laufevidence liegt extern unter `/var/tmp/codex/ModSecurity-conector/runs/pr382-merge-readiness-20261025`.

Die ersten 21 Kontrollen bestanden einschließlich synthetischer 101-Fall-Ablehnung vor dem Start eines Sentinel-Kindprozesses. Tatsächliche Fehler bei Loader-Benennung, Python-3.15-Zeilenmetadaten und fremden GCC-Notizen wurden korrigiert; dieselben betroffenen Fälle bestanden. Der korrigierte native C++-Allow-Fall und vier Memory-Verhalten bestanden einschließlich ASAN ohne Skip. Eine frische Sammlung erzeugte 35 generische Quellen (11 Python, 24 nativ), 13 Go-Quellen aus vier Modulen und 190 Rohreports aus 59 Fällen; der lokale Dirty-Report ist nicht importfähig. Eine spätere Prüfung erkannte und korrigierte einen unpräzisen negativen Shell-Befund; sein Nachweis des exakten Grunds wird getrennt erneuert. Finale Ergebnisse am veröffentlichten Head gehören zur aktuellen PR-Evidence.

Die spätere Sammlung mit 57 Fällen schloss ebenfalls erfolgreich ab und zeigte eine echte Messlücke: Das HTTP-Dienstkind verwendete `_exit`, wodurch seine Zähler verloren gingen. Die Fixture speichert jetzt ausschließlich bei Coverage-Messung echte GCC-Zähler vor diesem Exit. Beide bestehenden Deadline-/Recovery-Fälle bestanden erneut; die tatsächlichen Dienstbeobachtungen änderten sich von 0 auf 694 abgedeckte von 1165 gemessenen Zeilen. Dies sind lokale Zeilenbeobachtungen und keine Sonar-Projekt-/New-Code-Prozente.

Quellbindungen benennen `path` und `sha256` ausdrücklich; ein Quelldateiname wird nie als Credential-ähnlicher Feldname verwendet. Zwölf Scannerbefunde in vorgemerkten Änderungen wurden unabhängig als öffentlicher Konfigurationstext oder exakte aktuelle Quellhashes verifiziert. Strukturierte Darstellung und genauer benannte Property-Konstante beseitigen diese Fehlalarme ohne Suppressions oder Scanneränderungen.

Hosted-Verifikation an `9736ba07cdf0f60488c0d07b2200eea867c02abb` zeigte fehlende Jobvoraussetzungen: Apache-/APR-Header und PyYAML sowie einen lokal vorausgesetzten Ausgabepfad im Header-Wrapper. Jobs provisionieren jetzt tatsächliche erforderliche Pakete/hashgebundene Python-Abhängigkeit; der Wrapper validiert einen bestehenden externen Temp-Parent und erstellt sein privates Unterverzeichnis. Dieselben beiden Fälle bestanden ohne gesetztes `BUILD_ROOT`. Ausgewählter Stock-Sidecar- und Deskriptor-Expiry-Fall bestanden lokal ebenfalls ohne Skips. Der saubere Report mit 56 Fällen an diesem Commit enthält 77 generische Quellen (11 Python/66 nativ), 13 Go-Quellen und 306 Rohreports; nach der Folgeänderung ist er historisch und darf nicht für eine andere Revision importiert werden.

Dieselbe Hosted-Runde erkannte außerdem eine nicht ausgewählte alte Go-Toolchain im Envoy-Runtimejob, ein fehlendes NGINX-Aufruf-Tempverzeichnis und die neue allgemeine Zehn-Minuten-Grenze des Runners, die kalte Apache-Provisionierung unterbrach. Runtimezeilen wählen nun `.go-version` vor Provisionierung; NGINX erstellt/revalidiert sein privates Tempverzeichnis. Ausschließlich die drei geschlossenen Host-Runtimeskripte erhalten eine Frist von 6000 Sekunden innerhalb der bestehenden 120-Minuten-Jobs; gewöhnliche Kontrollen behalten 600 Sekunden und die Ein-Sekunden-Prozessgruppen-Cleanup-Kontrolle bestand erneut.

## Security-Auswirkung

Den vollständigen Katalog vor Ausführung validieren und eigene Prozessgruppen bei Timeout/Terminierung aufräumen. Unsichere Report-/Quellpfade und veränderte Artefakte ablehnen. Kindprozess-Tracing erhält UID/Präfix/Isolation und zeichnet ausschließlich Quellzeilenzähler auf. CI validiert ihr bestehendes Credential am festen Sonar-Ursprung ohne Secret-Ausgabe. Statische/Security-Prüfabsichten und geschützte Namespace-Grenzen bleiben wirksam. Die neue Scanner-Action ist unveränderlich gepinnt; Signaturprüfung bleibt aktiviert.

## Runtime-Evidence

Lokale Beobachtungen belegen ausschließlich die ausgewählte Unit-/Native-/Kontrollschicht und echte Profiler-Ausgaben. Aktuelle CRS-/No-CRS-/NGINX-Host-Fälle benötigen eigene Hosted-Artefakte. Historische I12-Ergebnisse behalten ihre ursprünglichen Revisionen; kein Build-/Scanner-/Konfigurationsergebnis erzeugt neue Host- oder Lifecycle-Qualifikation. Kein `I12_COMPLETE` wird behauptet.

## Bekannte Einschränkungen

Reine Zeilenmessung liefert keine Branch-Coverage. Isolierte Python-Kinder, solche mit bereinigter Umgebung/anderem Präfix/anderer UID/beendete Kinder und nicht ausgeführte Host-Pfade können ungemessen bleiben. Extrahierte native Snippets und externe SDK-Ausführung werden keinen Parent-Quellen zugeschrieben. Lokale Quoten gemessener Dateien sind keine Sonar-Projekt-/New-Code-Coverage; Erzeugung, Import und terminale Servermetriken sind getrennte Aussagen.

## Verbleibende Risiken

Die reduzierte automatische Auswahl verliert bewusst Spezialabdeckung; Abschluss und generiertes Archiv dokumentieren die Disposition. Profilnachweise übertragen sich nie auf Nachbarprofile. Bestehende 80% New-Code-Coverage und alle anderen Pflichtbedingungen bestimmen weiterhin Ready. Spätere vertrauenswürdige Master-Updater-Läufe und tatsächlich erzeugte Wartungs-PRs benötigen separate Masterintegrationsfreigabe.

## Nicht ausgeführte Prüfungen mit Begründung

Keine historische I12-Kampagne, vollständige MRTS-Suite, archivierten breiten Kataloge, beschränkten Plattform-Scans, Master-Merges, Releases oder Deployments: außerhalb der Aufgabenfreigabe. Erhaltene On-demand-Quellen sind kein neuer PASS. Aus Konfiguration oder Simulation wird keine Default-Branch-Live-Veröffentlichung abgeleitet.

## Finaler Diff- und Review-Status

Unabhängige Prüfung untersuchte Default-Auswahl, Report-/Quellgrenzen und Erhaltung ursprünglicher Tests. Alle 436 vorhandenen Hook-Manifest-Quellen entsprechen der Basis; 435 unterscheiden sich ausschließlich durch ihren Hook, und die eine geschützte Workflow-Kontrolle ergänzt ausdrückliche Opt-in-Assertions. Keine ursprüngliche Assertion wurde entfernt. Aktuelle PR-Evidence muss finalen SHA, terminale Pflichtchecks/Sonar, Blocker und Ready-Zustand nennen. Dieser Record allein erklärt kein `verified_pr`.
