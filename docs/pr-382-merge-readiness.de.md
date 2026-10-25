# PR #382: Status für Review und Merge-Entscheidung

**Sprache:** [English](pr-382-merge-readiness.md) | Deutsch

## Aktueller Auftrag und Sonar-Zuständigkeit

Der Nutzer verlangt die Entfernung der PR-eigenen Sonar-Arbeit, die verbindliche Master-Implementierung, einen normalen Push und anschließend eine Pause. Das ersetzt den eigenen Coverage-Abschluss und Sonar-Remediation-Plan. Master `9f44647593bac7947113558c6ad183ab118e80af` (#420) bleibt integriert.

`.github/workflows/sonarqube.yml`, Scope-Prüfung, zugehörige Tests und Scanner-Properties folgen dieser Master-Implementierung. Lediglich der bestehende kanonische Python-Minor (3.15), setup-python-Pin (7.1.0) und die Action-Owner-Schreibweise passen zur Toolchain und zentralen Lockdatei dieses PRs. C++17 bleibt verpflichtend, C++20/23 bleiben beratend. Der Scanner wartet weiterhin auf das tatsächliche Quality Gate. Zusätzlicher PR-Coverage-Producer, Artefaktübertragung/-prüfung, Quellrollen-Generator/alternative Properties und eigene Null-Befund-/Duplikations-Gates sind entfernt.

Der Master-Workflow behält ausdrücklich seine Python-Scope-Tests und vier direkten Go-Tests. Das Parent-Inventar ersetzt sie nicht. Tatsächliche Serververarbeitung, importierte Coverage und finales Quality Gate benötigen Nachweise am aktuellen Head; frühere Messungen belegen diese Änderung nicht.

## Erhaltene Parent-Arbeit

Das einzige Parent-Inventar enthält jetzt **932 expandierte Fälle / 536 Ausführungen**: **89 Kernfälle / 69 Ausführungen** und **843 ausdrücklich autorisierte Python-Offline-Ausnahmen / 467 Ausführungen**. Die Kerngrenze bleibt 100; die Zulassung lehnt Überlauf vor ausgewählten Prozessen ab. Entfernte eigene Sonar-Kontrollen und jetzt vom Master ausgewählte Scope-Tests sind im Inventar ausgemustert; übrige Quellbindungen und das nicht ausführbare Spezialarchiv werden regeneriert. Eine globale 100-Fall-Aussage einschließlich der verbindlichen separaten Master-Sonar-Auswahl wird nicht getroffen.

Connector-E2E bleiben bei **26 Fällen**. Historische I12-Host-/Matrix-/Oracle-Kampagnen bleiben geschlossen, ohne neues `I12_COMPLETE`. Framework-/MRTS-Repositories und Gitlinks bleiben unverändert. Go-, Python- und Actions-Wartungsupdates, Inventar-Runner und seine Offline-Prozess-/Netzwerkguards bleiben erhalten. Der unveröffentlichte Stand vor der Pause bleibt in benanntem Stash und prüfsummenverifiziertem externem Checkpoint gesichert und gehört nicht zu dieser Korrektur.

## Nachweise und Auslieferungsgrenzen

Die letzte abgeschlossene eigene Pipeline-Analyse bleibt historisch `3baaffb7b5dd30f05fc9d81ea58da5bd06a2244f`, Analyse `c460fc88-86c3-48eb-87da-e795b94b0990`: 12,9 % Gesamt-/31,0583536721 % New-Code-Coverage und 17 Befunde. Das ist kein Nachweis für die wiederhergestellte Master-Pipeline. Diese Korrektur verändert kein Coverage-Ziel, Quality Gate, keine Baseline und keinen Serverbefund.

[Historische Checkliste](pr-382-checklist.de.md), [Handoff](pr-382-i12-handoff.de.md) und [reduzierter I12-Abschluss](pr-410-i12-closeout-20261024.de.md) behalten ihre ursprünglichen Revisionen. #410 ist integriert. Repository- und Dependabot-Metadaten für `SONAR_TOKEN` wurden zuvor ohne Lesen der Werte geprüft. Tatsächlich erzeugte Wartungs-PRs bleiben eine separate Betriebsprüfung nach autorisierter Masterintegration.

Nach dem Push der Korrektur pausiert die Arbeit auf Nutzerwunsch. [PR-Beschreibung und Checks](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382) binden tatsächlichen veröffentlichten Head und Providerstatus. Der PR bleibt Draft; kein Ready/`verified_pr`, Merge nach master, Release oder Deployment wird behauptet.

[Change Record zur Wiederherstellung](../reports/audits/change-records/CR-20261025-pr382-master-sonar.de.md) · [Tests und erhaltenes Archiv](testing-and-evidence.de.md) · [Master-Sonar-Implementierung](sonarqube-analysis.de.md).
