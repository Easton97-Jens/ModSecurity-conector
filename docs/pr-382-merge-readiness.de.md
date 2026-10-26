# PR #382: Status für Review und Merge-Entscheidung

**Sprache:** [English](pr-382-merge-readiness.md) | Deutsch

## Aktueller Auftrag und Sonar-Zuständigkeit

Der wiederaufgenommene Nutzerauftrag verlangt zuerst die Integration des neuen Masterstands `7a44f18edac729291d6551d068da64fa3fec4e1e` (PR #421). Der reguläre Merge beginnt am PR-#382-Head `209ab41a16cc34c88e3dc23d312eada0a38a8169`; Ergebnisrevision und Providerergebnisse werden nach Veröffentlichung im PR gebunden. Die frühere Pause ist durch diesen Auftrag aufgehoben. Abgeschlossener Merge, bestandenes Gate oder Auslieferungsfreigabe werden hier nicht behauptet.

Master-Sonar-Workflow, Scope-Prüfung, Native-Kontextvorbereitung und `run-sonar-coverage.py` sind maßgeblich. C++17 bleibt verpflichtend, C++20/23 bleiben beratend. Jeder Scanner wartet auf sein tatsächliches Quality Gate. Die integrierte Toolchain behält Python `3.15.1`, Go `1.27.3`, Modul-Sprachversion `1.26.9` und setup-python `7.1.0`; Scanner CLI ist jetzt `8.2.0.6438`.

Master wählt Python-Verhalten, das PR #421 als 80 Methoden dokumentiert, 37 benannte Go-Szenarien und native Common-Helper-/Konstruktor-/Interventions-Coverage. Methoden sind keine expandierten Fallzahlen. Diese Prüfung bleibt außerhalb des Parent-Inventars. Jede Matrixvariante wiederholt Ausführungskosten, erweitert aber keinen eigenständigen Fallkatalog. Geschützte Standard-Discovery bleibt erhalten; ausschließlich die feste `PYTHON_TESTS`-Auswahl mit 13 Einträgen erhält im Kind explizit `ON_DEMAND_TESTS=1`. Es gibt keinen globalen Bypass. Diese Prozess-/Go-/Native-Auswahl gehört nicht zur Python-Offline-Ausnahme und eröffnet keine historischen I12-Kampagnen.

Entfernter PR-eigener Collector, Artefaktübertragung/-prüfung, Quellrollen-Generator/alternative Properties und eigene Null-Befund-/Duplikations-Gates bleiben entfernt. Master-#421-Coverage ist dessen eigene Implementierung, keine Wiederherstellung jener Pipeline. Frühere unveröffentlichte Arbeit bleibt in benanntem Stash/Checkpoint gesichert und wird nicht wiederhergestellt.

## Erhaltene Parent-Arbeit

Das Parent-Inventar bleibt bei **932 expandierten Fällen / 536 Ausführungen**: **89 Kernfälle / 69 Ausführungen** und **843 ausdrücklich autorisierte Python-Offline-Ausnahmen / 467 Ausführungen**. Die Kerngrenze bleibt 100; die Zulassung lehnt Überlauf vor ausgewählten Prozessen ab. Master-Sonar-Selektoren sind getrennt; keine globale 100-Fall-Aussage schließt sie ein. Übrige Inventar-Quellbindungen und das Spezialarchiv müssen zu den zusammengeführten Quellen passen.

Connector-E2E bleiben bei **26 Fällen**. Historische I12-Host-/Matrix-/Oracle-Kampagnen bleiben geschlossen, ohne neues `I12_COMPLETE`. Framework-/MRTS-Checkouts und Gitlinks bleiben unverändert. Das Lesen des exakt gepinnten Framework-Vertrags für freigegebene native Header ist passive Provenienzeingabe, keine Framework-/MRTS-Schreib- oder Qualifikationsfreigabe. Go-/Python-/Actions-Wartung, Inventar-Runner und Offline-Prozess-/Netzwerkguards bleiben erhalten.

## Nachweise und Auslieferungsgrenzen

PR-#421-Source `d5450cd3d88e7ac20c5fdee3e4173c65f5626ca8` hatte drei erfolgreiche terminale Analysen mit Gates `OK`: 83.5% PR-/84.6% Advisory-New-Code-Coverage, 179 `FIXED` plus 24 `FALSE_POSITIVE`-IDs und null OPEN/CONFIRMED-Befunde/Hotspots. Seine 136 nativen Einheiten erreichten Parsing-/Include-Qualität 100/100. Dies sind quellgebundene PR-#421-Beobachtungen, keine Nachweise für PR #382, das Merge-Ergebnis oder den größeren Parent-Scope. Der [PR-#421-Abschluss](sonarqube-pr421-closeout.de.md) erhält exakte Task-/Analysebindungen und Grenzen.

Die Architekturanwendung bleibt durch HTTP 415 extern blockiert; CFamily-AutoConfig-Taint, unabhängige Ziele/Varianten, Python-/FIFO-Analyzergrenzen und TLS-Änderungszeilenwarnung bleiben ausdrücklich bestehen. PR-#421-Runtime-Evidence gehört getrennt zu Source `900dddb49c43ec4479c4b75a91071cadb97893c4` und belegt nur dessen ausgewählten Runtime-Scope. Kein Ergebnis geht auf den Merge-Head über.

Die letzte eigene Pipeline-Analyse bleibt historisch vor dem Merge `3baaffb7b5dd30f05fc9d81ea58da5bd06a2244f`, Analyse `c460fc88-86c3-48eb-87da-e795b94b0990`: 12.9% Gesamt-/31.0583536721% New-Code-Coverage und 17 Befunde. Sie qualifiziert die Master-Pipeline nicht. Neue Berichte, Analyzerimport, Gatestatus und Runtime-Qualifikation benötigen eigene revisionsgebundene Nachweise; diese Merge-Dokumentation ändert keine Schwelle, Regel, Baseline oder Befunde.

[Historische Checkliste](pr-382-checklist.de.md), [Handoff](pr-382-i12-handoff.de.md) und [reduzierter I12-Abschluss](pr-410-i12-closeout-20261024.de.md) behalten ihre ursprünglichen Revisionen. #410 ist integriert. [PR-Beschreibung und Checks](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382) binden später tatsächlichen veröffentlichten Merge-Head und Providerstatus. PR #382 bleibt Draft; kein Ready/`verified_pr`, Merge nach master, Release oder Deployment wird behauptet.

[Merge-Change-Record](../reports/audits/change-records/CR-20261026-pr382-master421-merge.de.md) · [Tests und erhaltenes Archiv](testing-and-evidence.de.md) · [Master-Sonar-Implementierung](sonarqube-analysis.de.md).
