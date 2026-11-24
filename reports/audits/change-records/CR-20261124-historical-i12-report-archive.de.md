# Change Record: CR-20261124-historical-i12-report-archive

**Sprache:** [English](CR-20261124-historical-i12-report-archive.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261124-historical-i12-report-archive |
| Datum (UTC) | 2026-11-24 |
| Basis-Revision | `48c4672dc07458411288570515bb8357f1e9e581` |

## Motivation und Problemstellung

Sechs I12-Artefakte vom 2026-10-15 belegen im Berichtsbaum 970,967 Bytes. Sie dokumentieren abgeschlossene Untersuchungen zu Apache und lighttpd.

## Akzeptanzkriterien

Den Umfang der versionierten Berichtsdateien um mindestens 900,000 Bytes reduzieren, die bytegenaue Wiederherstellung aller sechs archivierten Dateien prüfen und die Dokumentations- und Report-Governance-Prüfungen bestehen. Die Meldungen der vollständigen Layout-Prüfung mit der Basis-Revision vergleichen.

## Implementierungsentscheidung und Begründung

Die Originaldateien bleiben in der Basis-Revision und sind einzeln im [Berichtsindex](../../README.de.md#historische-i12-nachweise) verlinkt. Die GitHub-Tree-API und das lokale `git ls-tree -rl` lieferten für alle sechs Dateien dieselben Blob-IDs und Größen. Das aktive Inventar des gepinnten Frameworks benötigt das Apache-Testfallprotokoll, das Apache-Review-Skript und die lighttpd-Stock-Sidecar-Testfälle. Diese drei Eingaben liegen mit ihren Originalbytes vor.

## Geänderte Dateien

Der englische und deutsche Berichtsindex verlinken die archivierte Apache-Prüfung der Regeläquivalenz und fünf lighttpd-Testfall- oder Oracle-Snapshots. Die sechs Dateien entfallen im aktuellen Checkout. Dieser Change Record liegt ebenfalls in beiden Sprachen vor.

## Ausgeführte Befehle

Die Referenzprüfung umfasste 542 versionierte Parent-Dokumente, 407 aktive Parent-Quellcode-, Konfigurations- und Workflow-Dateien sowie die Report-Werkzeuge und das aktive Inventar des gepinnten Frameworks.

| Prüfung | Beobachtetes Ergebnis |
| --- | --- |
| `git ls-tree -rl` und `gh api` | Übereinstimmende Blob-IDs und Größen für alle sechs archivierten Pfade in der Basis-Revision. |
| `make check-bilingual-docs`, `make check-doc-links` | Mit gepinntem Framework und Python 3.15.2 bestanden. |
| `make report-governance` | Mit gepinntem Framework bestanden, nachdem die drei im ersten Lauf identifizierten erforderlichen Inventareingaben wiederhergestellt wurden. |
| `make check-generated-report-layout` | Exit 2 auf Basis- und Aufgabenstand mit 207 identischen Meldungen zu historischen Eingaben und Metadaten. |
| `python -P ci/tools/new-change-record.py check`, `git diff --cached --check` | Bestanden. |

## Security-Auswirkung

Die Änderung betrifft die Ablage und Navigation historischer Artefakte. Bestehende Sicherheits- und Laufzeitprüfungen verwenden weiterhin ihre Originaleingaben.

## Runtime-Evidence

Die bestehende I12-Evidence ist in der Basis-Revision verfügbar. Aus dieser Änderung folgen keine neuen Laufzeitaussagen.

## Bekannte Einschränkungen

Ein flacher Klon benötigt die archivierte Revision, bevor `git show` eine Datei daraus abrufen kann.

## Verbleibende Risiken

Private Werkzeuge mit fest kodierten Pfaden zu den sechs historischen Dateien müssen sie aus der festgelegten Revision abrufen.

## Nicht ausgeführte Prüfungen mit Begründung

Connector-Builds, Runtime-Tests und Report-Neugenerierung liegen außerhalb dieser Archivierung. Die Report-Governance-Prüfung umfasst ihre Testfälle für die Runtime-Pfadrichtlinie.

## Finaler Diff- und Review-Status

Die Änderung wurde in einem eigenen Parent-Worktree vorbereitet. Der Pull Request dokumentiert die Veröffentlichung und den GitHub-Prüfstatus.
