# PR #382: begrenzter Abschlussstand

**Sprache:** [English](pr-382-merge-readiness.md) | Deutsch

## Beauftragter Folgefix: die verbleibenden 25 Sonar-Befunde

Am 2026-10-27 autorisierte der Nutzer gesondert die Korrektur der 25 verbleibenden Wartbarkeitsbefunde an Basis `0867713`. Sechs vorhandene native Analysehilfen und ein Test erhalten verhaltenserhaltende Aufteilungen, Konstanten, Comprehensions, ASCII-gleiche Regex-Kürzel und eine eindeutige Ausnahme-Assertion. Die 29 gezielt ausgewählten bestehenden On-demand-Ausführungen / 38 expandierten Fälle bestanden ohne Skips. Das automatische Inventar bleibt bei 100 Fällen / 80 Ausführungen; kein Fall, Workflow, Gate oder Quellscope wird ergänzt oder abgeschwächt. Der [Folgefix-Change-Record](../reports/audits/change-records/CR-20261027-sonar25-maintainability.de.md) beschreibt Umfang und Nachweise. Neue CI/Sonar am veröffentlichten Head und der finale Review-Status stehen im verlinkten PR; der frühere Abschluss unten bleibt an seine genannten Revisionen gebunden.

Der erste Server-Readback bei `39793006` bestätigt alle 25 ursprünglichen IDs als behoben; ein eingeführter `S7500`-Parserausdrucksbefund erhält eine gezielte Präzisierung. Der finale veröffentlichte Head muss null offene PR-Befunde bestätigen.

## Integration und Befugnis

[PR #382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382) ist maßgeblich für final veröffentlichten Head, terminale Checks und Review-Status. Dieser Eintrag dokumentiert die endlichen Abschlusskorrekturen nach Zwischenstand `011cb197a82801c2c3eada073eb6847899c44933`; Ergebnisse früherer Heads werden nicht übertragen.

#410 und Master `8ae707d72f1a8acb25d239e55e28a73cbc7522b1` (#422) sind integriert. Der unabhängig geprüfte #422-Merge war ausdrücklich freigegeben und vor dem letzten Umfangsstopp abgeschlossen; seine sechs Ruleset-Checks und drei Sonar-Jobs bestanden. Der geschützte NGINX-Aufrufer pinnt diesen Broker und Framework `99a7985c1be92a2297b1b59208f64df6768f2cbf`. Parents Framework-Gitlink und MRTS bleiben unverändert. Kein weiterer Master-Merge, neuer PR/neues Projekt, Migration, Release oder Deployment ist autorisiert.

Coverage sollte zunächst verbessert werden und wurde anschließend vom Nutzer ausdrücklich aus Sicherheits- und Merge-Abnahme entfernt. `sonar.coverage.exclusions=**` ändert nur Coverage-Anwendbarkeit. Die fünf verbleibenden Bedingungen des eingebauten Gates, Sicherheitsregeln, Quellanalyse, exakte Revisionsprüfung und Secret-Isolation bleiben erhalten.

## Finale automatische Auswahl

**100 expandierte aktive Fälle / 80 Ausführungen** teilen ein Standardinventar für `make test`, Runner ohne Selektor, normale Python-Discovery und jede automatische CI-Gruppe. Eine gemeinsame Gruppe zieht keine archivierten Fälle hinein. Vollständige Quell-/Selektorzulassung und Abweisung von mehr als 100 Fällen vor Kindprozessstart bleiben erhalten; keine Kürzung oder Assertion-Entfernung erfolgt.

**1893 Spezialfälle / 839 Ausführungen** bleiben in Quellen und Inventar außerhalb sämtlicher Standardpfade erhalten. Sie verlangen ausdrücklich `--on-demand` mit Gruppen-/Fall-/Ausführungsselektor oder die vorhandene ausdrückliche modulweite Freigabe. Die frühere automatische Offline-Ausnahme ist durch die abschließende Nutzeranweisung ersetzt. Sonars feste Python-/Go-/Common-Coverage-Kataloge bleiben On-demand erhalten und laufen nicht mehr automatisch; Quell-/Scanner-/nativer Kontext-/Gate-Pipeline bleiben bestehen. Das [Archiv](../modules/ModSecurity-test-Framework/connector_suite/reports/testing/test-selection-archive.generated.json) wird aus dieser Grenze generiert.

Connector-E2E bleibt bei **26**. Die vorhandenen acht gezählten Offline-I12-Fälle bleiben im gemeinsamen Standardbudget; historische I12-Host-/Matrix-/Oraclekampagnen bleiben ohne `I12_COMPLETE` geschlossen. Drei eng ausgewählte Guardkontrollen ergänzen die bisherige Standardauswahl von 97 Fällen; zwei davon bestanden bereits im aufbewahrten Katalog.

## Prüfung und verbleibendes Veröffentlichungskriterium

Die Abschlussauswahl bestand **11 Guard-Ausführungen / 11 expandierte Fälle ohne Skips**. Reine Zulassung und alle 37 Standardgruppen blieben im selben 100-Fälle-Inventar; echte Python-Discovery zählte genau 44 ausgewählte Methoden ohne Ausführung auf. `make -n test` verweist auf den Inventar-Runner. Zwei ausdrückliche C-Nullprüfungen machen die zuvor über Hilfsfunktionen belegte Abweisung direkt an den gemeldeten Aufrufen sichtbar; beide betroffenen C-Einheiten bestanden strikte C17-Syntaxkompilierung. Kein vollständiger Offlinekatalog wurde erneut ausgeführt.

Am Zwischenstand `011cb197` waren alle **22** automatischen Workflows terminal: **20 erfolgreich**, breites und natives Sonar scheiterten ausschließlich an Server-Gates. Natives SDK und alle zwölf tatsächlichen Ziel-Builds/Capture-Validatoren bestanden; **611 aggregierte Compilation Units vollständig analysiert, keine teilweise**, mit 100 % CFamily-Indexierung je Projekt, CTU und erfolgreicher Taint-Ausführung. Dies sind Analyzer-/Build-Nachweise, keine Host-Runtime-Qualifikation. Ursprüngliche native Job-Ergebnisse waren drei bestandene und neun fehlgeschlagene Gates. Kein fehlgeschlagener Job wurde blind wiederholt.

Die zwölf neuen Python-Sicherheitsmeldungen wurden einzeln über private Build-/Ausgabe-Ownership, feste Aufruferauswahl und tatsächliche Producer-Herkunft verfolgt; jede Main-/Advisory-Instanz erhält eigene Begründung und Readback. Native Meldungen wurden ebenso einzeln geprüft, darunter genaue Empfangspuffergrenzen, endliche Stringguards, tatsächliche Daten-gegenüber-Pfadoperanden und die NGINX-Callback-ABI. Kein pauschaler Ausschluss, Regelsuppression, Accepted-risk-Verzicht oder künstliches PASS wird verwendet. Die zwei breiten Null-Propagationsmeldungen erhalten ausdrückliche Quellguards. Historische Jobfehler bleiben Fehler; finale Lieferung verlangt neue terminale Analyse des veröffentlichten Abschluss-Heads.

Der vorhandene getrennte [Framework-PR #138](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/138) endete bei `03da9353561bf632a1f7bfc71b0a2671ec7aa257`: alle zwölf Workflows, Ruff/Pyright und tatsächliches SDK-/C-/CLI-Sonar-Gate bestanden. Daraus folgen kein neuer Framework-Auftrag und kein Parent-Gitlink-Import.

## Abnahme und Stopp

Normaler gezielter Commit/Push muss `lokaler HEAD = Remote-Branch = PR-Head` erhalten. `verified_pr` und Ready verlangen alle anwendbaren Checks/Sonar am exakten Head terminal und bestanden, bearbeitetes handlungsrelevantes Review-Feedback, passende Dokumentation und gestoppte aufgabeneigene Prozesse. Andernfalls muss der PR den konkreten fehlgeschlagenen Check und die fehlende Voraussetzung ohne Bereitschaftsbehauptung nennen. Aktuelle terminale Veröffentlichungsnachweise stehen im verlinkten PR; ein reiner Dokumentations-Push würde denselben Nachweis wieder ungültig machen.

Frühere 94/342-, 79/298-, C++17/20/23-, Coverage- und No-CRS-Ergebnisse behalten ihre ursprünglichen Revisionen. Sie sind keine Abnahme des neuen Heads. Siehe [Korrekturrecord](../reports/audits/change-records/CR-20261026-pr382-sonar-remediation.de.md), [nativen Sicherheitsleitfaden](sonarqube-native-security.de.md), [Testleitfaden](testing-and-evidence.de.md) und [historische Übergabe](pr-382-i12-handoff.de.md). Nach dieser endlichen Abnahmeentscheidung endet der Auftrag; keine weitere Verbesserungskampagne gehört dazu.
