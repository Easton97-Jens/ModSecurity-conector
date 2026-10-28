# Aktuelle Dokumentation und Konfliktabgleich

**Sprache:** [English](CR-20261028-documentation-reconciliation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20261028-documentation-reconciliation` |
| Datum (UTC) | 2026-10-28 |
| Pull Request | #383 |
| Branch | `docs-refresh-root-readmes` |
| Vorheriger Dokumentations-Head | `ab01cc60e638f03915fc0cc4f1541d91f9c6a62e` |
| Abgeglichener master | `15cea9e4d778fa1ec6e27e6fe084b347010f1367` |
| Vorherige gemeinsame Basis | `820b6975495bdf0f90aca67eee86e27a3b7d329b` |

## Motivation und Akzeptanzkriterien

Der Benutzer hat die Fertigstellung der Dokumentation auf dem neuen
Repository-Stand und die Lösung der Merge-Konflikte in PR #383 angefordert.
Der frühere Oktober-Dokumentations-Head hatte seine beobachteten Workflows
erfolgreich abgeschlossen; master wurde danach mit Source-, Konfigurations-,
Test-, Toolchain- und Evidence-Änderungen weiterentwickelt. Diese Ergebnisse
des alten Heads validieren das neue Merge-Ergebnis nicht.

Die finale Dokumentation muss aktuellen master-Source und generierte Verträge
erhalten, heutiges Verhalten für Einsteiger erklären, vollständige englische
und deutsche Begleitdateien pflegen und den Git-Konflikt ohne Force-Push oder
Merge des PRs nach master lösen. Entfernte Connector-Body-Limits dürfen nicht
als Kompatibilitätsoptionen zurückkehren. Aktuelle Testauswahl und Grenzen
abgeschlossener Spezialkampagnen bleiben ausdrücklich sichtbar.

## Umsetzung und Konfliktentscheidungen

Der vorgeschlagene Merge-Baum baut auf dem exakten aktuellen master-Baum auf.
Er erhält sämtliche aktuellen Produktquellen, Tests, Workflows, Versions-Pins,
Gitlinks, generierten Referenzen und neuen technischen/Evidence-Dokumente.
Darauf werden geprüfte leserorientierte Dokumentationsänderungen übernommen.

Wo master technische Dokumentation weiterentwickelt hat, bleibt dieser aktuelle
Inhalt erhalten, statt durch eine ältere ganze Datei ersetzt zu werden.
Stabile frühere Orientierungsergänzungen bleiben dort bestehen, wo sich das
zugrunde liegende master-Dokument nicht geändert hat. Root-READMEs,
Dokumentationsindex, Einstieg, Konfigurationsguide und Beispielindex werden auf
Basis aktueller Verträge neu formuliert. Ein neuer Migrationsguide erklärt
entfernte Einstellungen, unveränderte Host-/Transport-Controls, aktive Tests,
Versions-Pins und die Zuständigkeit für generierte Dateien.

Das ersetzt bewusst die alte pauschale Dateizahl des PRs. Der finale
GitHub-Diff bestimmt den tatsächlichen Umfang und nicht eine historische Zahl.
Die Konfliktlösung erhält neuere Detailguides und generierte Ausgaben auch dann,
wenn dadurch eine veraltete PR-eigene Einführung dieser Datei entfällt.

## Dokumentiertes aktuelles Verhalten

Request- und Response-Inspection-Limits/-Aktionen gehören zu libModSecurity.
Entfernte kumulative Connector-Einstellungen aus Common, nativen Direktiven
und Hostservices führen zu Konfigurationsfehlern; sie sind keine still
akzeptierten Aliase. Request-No-files-Limits, Zugriffs-/MIME-Einstellungen,
native Interventionsergebnisse und unabhängige Host-/Transportkapazität werden
getrennt behandelt. Phase-4-Modi steuern unterstütztes spätes Verhalten und
keine Byte-Budgets. Der gemeinsame Source-Standard ist `off`, definiert in
`common/include/msconnector/options.h`.

Normale funktionale Auswahl verwendet `config/testing/active-cases.json` mit
Kerngrenze und separat autorisierter geschützter Offline-Python-Ausnahme.
`make check-active-inventory` prüft die gesamte Auswahl ohne Ausführung;
`make quick-check` enthält statische Checks und zugelassene funktionale
Teilmengen. Spezialausführung benötigt einen getrennten aktuellen Auftrag und
`ON_DEMAND_TESTS=1`; diese Dokumentationsarbeit eröffnet I12 nicht erneut.

Der reine Herkunfts-/Referenzzweck von `licenses/` bleibt erhalten. Originale
Upstream-Dateien LICENSE/AUTHORS/CHANGES werden nicht umgeschrieben, und es wird
keine repositoryweite Lizenz erklärt.

## Geänderte Dokumentation

Neue oder vollständig überarbeitete Einstiege dieses Abgleichs:

- `README.md` / `README.de.md`
- `docs/README.md` / `docs/README.de.md`
- `docs/getting-started.md` / `docs/getting-started.de.md`
- `docs/configuration.md` / `docs/configuration.de.md`
- `docs/migration.md` / `docs/migration.de.md`
- `examples/README.md` / `examples/README.de.md`
- Dieses englische/deutsche Change-Record-Paar.

Der finale PR erhält außerdem kompatible frühere Änderungen an Security- und
Herkunftserklärungen, Architektur, Betrieb, Nachvollziehbarkeit,
Entscheidungsdokumenten, ausgewählten Connector-Einführungen,
Glossar-/Profilreferenzen und dem historischen Record
`CR-20260921-root-readme-refresh`. Der ältere Record dokumentiert frühere
Vorbereitungsstufen; seine damaligen Aktualitätsbeschreibungen und Dateizahlen
sind keine Aussage über den final abgeglichenen Baum.

## Tatsächlich vorgenommene Validierung

Repository-Dateien, aktuelle master-/PR-Metadaten, ausgewählte
Source-Definitionen und Workflow-Ergebnisse des alten Heads wurden über den
GitHub-Connector gelesen. Baum- und Blob-Identitäten unterscheiden unveränderte
technische Dateien von auf master weiterentwickelten Dateien.
Konfigurationsmigration wurde anhand von `docs/phase4-mode-budget.md` und der
gemeinsamen Optionsdefinition geprüft.

Repository-native lokale Shell-Validierung wird nicht behauptet: In dieser
Umgebung wurde kein vollständiger lokaler Checkout hergestellt. Hosted-
Validierung des finalen Heads bleibt von Erfolgen des alten Heads getrennt und
muss aus den Checks dieses Heads abgelesen werden. Die PR-Beschreibung hält das
beobachtete Ergebnis des finalen Heads nach Veröffentlichung fest; ausstehende,
übersprungene oder wegen Voraussetzungen blockierte Arbeit darf nicht als
Erfolg ausgegeben werden.

## Security- und Kompatibilitätsauswirkung

Gegenüber dem abgeglichenen master fügt die Änderung kein Runtime-Verhalten,
keine Standards, Berechtigungen, Netzwerkexposition, Credentials,
Dependency-Auswahl oder Testumgehung hinzu. Die master-Synchronisierung
übernimmt vorhandene geprüfte master-Änderungen, statt in einem Dokumentations-PR
neue Source-Änderungen zu erfinden.

Der Migrationsguide dokumentiert bereits im Source vorhandene inkompatible
Konfigurationsentfernungen. Er autorisiert weder beliebige Engine-Limitstandards
noch das Entfernen echter Host-Autorisierungsgrenzen. Beispiele bleiben vom
Betreiber anzupassende Referenzen und keine sicheren Deployment-Manifeste.

## Runtime-Nachweise und nicht ausgeführte Prüfungen

Durch die Dokumentationsbearbeitung wurde keine neue Host-Laufzeitkampagne,
I12-Aufzeichnung, CRS-Prüfung, Protokollmatrix, Sanitizer-Ausführung oder
Produktionsqualifikation vorgenommen. Vor Hosted-Checks werden weder lokales
vollständiges `make test`, `make quick-check`, Regeneration generierter Ausgaben
noch repositoryweite Linkvalidierung behauptet. Generierte Dateien bleiben
aktuelle master-Ausgaben; ihre normalen CI-Verträge werden nicht abgeschwächt.

## Abschließendes Review und verbleibende Grenze

Beabsichtigt ist ein Merge-Commit mit zwei Eltern auf dem vorhandenen
Dokumentations-Branch. Er erhält die alte PR-Historie und enthält die geprüfte
master-Revision. Dieser Record autorisiert weder Force-Push noch PR-Merge oder
Branchlöschung.

Finalen Diff und CI des finalen Heads prüfen. Laufzeitaussagen bleiben an ihr
tatsächliches Profil, Revision, Regeln, Run-ID und Artefakte gebunden; eine grüne
Dokumentationsänderung ist keine Produktions- oder Vollprotokollzertifizierung.
