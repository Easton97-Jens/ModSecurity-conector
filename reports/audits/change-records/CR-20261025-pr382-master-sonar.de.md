# Change Record: CR-20261025-pr382-master-sonar

**Sprache:** [English](CR-20261025-pr382-master-sonar.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261025-pr382-master-sonar |
| Datum (UTC) | 2026-10-25 |
| Basis-Revision | `d3225bab29f000c063e3d7ab798c31930c07ec9a` |

## Motivation und Problemstellung

Der Nutzer verlangt Sonar aus master, Entfernung der zusätzlichen PR-Integration, normalen Push und danach eine Pause.

## Akzeptanzkriterien

Master-Scan #420 und tatsächliches C++17-Quality-Gate bleiben verbindlich. Eigene Producer/Gates entfernen, Inventar und unabhängige Go-/Python-/Actions-Arbeit erhalten, ohne History-Umschreiben pushen und pausieren.

## Implementierungsentscheidung und Begründung

Master-Scope/Workflow/Prüfungen wiederherstellen. Nur bestehendes Python3.15, setup-python7.1 und kanonische Action-Owner-Schreibweise abgleichen; Scope-Fixtures erhalten nur passende gültige/Drift-Versionen. Eigenen Collector, Artefakt-/Quellrollen-Schichten und zusätzliche Null-/Duplikations-Gates ausmustern.

## Geänderte Dateien

Sonar-Workflow/Properties/Scope-Tests, gemeinsamer Runner und native Pfadwrapper, Updater-Verträge, ein Inventar/Archiv und EN/DE-Statusdokumente. Der Git-Diff enthält alle Pfade.

## Ausgeführte Befehle

RTK-Staticchecks: vollständige Inventarzulassung, Python-Vertrag50Jobs, actionlint, zizmor, Quellscope, Sprach-/Linkprüfungen und Diff-/Secretprüfung. Master-Scope-Units bestanden8Methoden (12explizite Eingabeszenarien). Gezielte bestehende Inventar-/Pfadguards werden separat geprüft; terminale Ergebnisse und veröffentlichter Head gehören in den PR.

## Security-Auswirkung

Master-Scanner-Gate, Credentials, Ausschlüsse und Baseline bleiben unverändert. Native Wrapper verwenden die erhaltene private Output-Prüfung; Offline-Prozess-/Netzwerkguards bleiben. Parent-Inventar89Kernfälle/69Ausführungen plus843autorisierte Offline-Fälle/467Ausführungen; kein globaler Cap-Nachweis einschließlich eigener Master-Scope-/Go-Auswahl.

## Runtime-Evidence

Keine neue Host-, Matrix- oder Oracle-Kampagne. Connector-E2E26, Framework-/MRTS-Repositories/Gitlinks und reduzierter I12-Abschluss bleiben unverändert.

## Bekannte Einschränkungen

Neue Hosted-Analyse/Coverage/Gate sind durch lokale Static- oder Unitchecks nicht belegt; vorherige3ba31,058% bleiben historisch.

## Verbleibende Risiken

Automatische CI am aktuellen Head kann nach der gewünschten Pause Fehler melden. PR bleibt Draft; kein Ready- oder verified_pr-Nachweis.

## Nicht ausgeführte Prüfungen mit Begründung

Keine neue vollständige lokale Coverage oder I12-Qualifizierung: Eigene Coverage-Pipeline entfernt, Nutzer verlangt Pause nach Push. Hosted-CI wird unabhängig ausgelöst.

## Finaler Diff- und Review-Status

Explizites Staging eigener Pfade und unabhängiges Read-only-Review; finale Diff-/Secretchecks vor normalem Commit. Tatsächliche Lokal-/Remote-/PR-Identität steht nach Push in der PR-Beschreibung. Zusätzlicher unveröffentlichter WIP bleibt in Stash5c82a862/Checkpoint gesichert.
