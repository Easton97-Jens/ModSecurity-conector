# Aktuelle Dokumentation und Konfliktabgleich

**Sprache:** [English](CR-20261028-documentation-reconciliation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20261028-documentation-reconciliation` |
| Datum (UTC) | 2026-10-28 |
| Basis-Revision | `ab01cc60e638f03915fc0cc4f1541d91f9c6a62e` |
| Abgeglichener master | `15cea9e4d778fa1ec6e27e6fe084b347010f1367` |
| Vorherige gemeinsame Basis | `820b6975495bdf0f90aca67eee86e27a3b7d329b` |
| Pull Request | #383 |
| Branch | `docs-refresh-root-readmes` |
| Abgleich-Merge | `34dffc40f31cdb870e64283ebaee32b8cdd44bca` |

## Motivation und Problemstellung

Der Benutzer hat die Fertigstellung der Dokumentation auf dem neuen
Repository-Stand und die Lösung der Merge-Konflikte in PR #383 angefordert.
Der frühere Dokumentations-Head hatte seine beobachteten Workflows erfolgreich
abgeschlossen; master wurde danach mit Source-, Konfigurations-, Test-,
Toolchain- und Evidence-Änderungen weiterentwickelt. Ergebnisse des alten Heads
validieren das neue Merge-Ergebnis nicht.

Frühere Übergangstexte behandelten Connector-Response-Limits als
Kompatibilitäts- oder Kapazitätswerte. Aktueller Source entfernt stattdessen
kumulative Request- und Response-Connector-Einstellungen. Standardtests nutzen
nun das aktive Inventar mit gesondert autorisierter Offline-Ausnahme.
Einstiegsseiten müssen diese Änderungen erklären, ohne altes Verhalten
wiederherzustellen oder den Umfang zu übertreiben.

## Akzeptanzkriterien

Aktuellen master-Source, generierte Verträge und neue technische/Evidence-
Dokumente erhalten. Einrichtung, Profilwahl, Konfigurationsmigration und
Testauswahl in gleichwertigen englischen/deutschen Begleitdateien verständlich
erklären. Die zehn logischen Lösungen mit Kompatibilitäts-/Companion-Grenzen
erhalten. Git-Konflikte ohne Force-Push, Branchlöschung oder PR-Merge nach
master lösen. Checker nicht abschwächen und entfernte Einstellungen nicht
wiedereinführen.

## Implementierungsentscheidung und Begründung

Der Merge-Baum basiert auf dem exakten aktuellen master-Baum und erhält
Produktquellen, Tests, Workflows, Pins, Gitlinks, generierte Referenzen und
neuere Detaildokumente. Kompatible Leserorientierung bleibt dort erhalten, wo
die zugrunde liegende master-Datei unverändert ist. Bei weiterentwickelter
technischer Dokumentation haben aktuelle master-Details Vorrang vor veralteten
Ganzdatei-Ersetzungen des früheren PRs.

Root-READMEs, Dokumentationsindex, Einstieg, Konfigurationsguide und
Beispielindex werden anhand aktueller Verträge neu formuliert. Der neue
Migrationsguide trennt Engine-Inspection-Limits von echter Host- und
Transportkapazität, erklärt abgewiesene entfernte Optionen, nennt den
Phase-4-Source-Standard `off` und dokumentiert aktive Tests sowie explizite
Spezialauswahl, ohne I12 erneut zu eröffnen.

Das abschließende Review korrigiert außerdem den veralteten `safe`-Standard
im Repository-Konzept auf den tatsächlichen gemeinsamen `off`-Standard aus
`common/include/msconnector/options.h`. Das Konzept behält Detailarchitektur
und datierte Beobachtungen, trennt historisches Prüf-/Testplatzierungsmaterial
nun aber ausdrücklich von Live-Status und aktueller aktiver Auswahl. Die
engine-eigene Request-/Response-Policy bleibt unverändert.

Der reine Herkunftszweck von `licenses/` bleibt erhalten: Upstream-Herkunft,
aufgezeichnete Revisions-/Lizenzbasis, aufbewahrte Hinweise und lokale
Unterschiede. Originale Upstream-Dateien LICENSE/AUTHORS/CHANGES werden nicht
umgeschrieben; es wird keine repositoryweite Lizenz erklärt.

Der finale Diff ersetzt die alte pauschale Zahl von 86 Dateien. Der historische
Record `CR-20260921-root-readme-refresh` dokumentiert frühere
Vorbereitungsstufen, nicht die aktuelle abgeglichene Dateizahl,
Übergangseinstellungen oder Validierung.

## Geänderte Dateien

Der abgeglichene PR-Diff gegen den ausgewählten master enthält diese Dokumente:

- `README.md` / `README.de.md`
- `SECURITY.md` / `SECURITY.de.md`
- `docs/README.md` / `docs/README.de.md`
- `docs/architecture.md` / `docs/architecture.de.md`
- `docs/change-traceability.md` / `docs/change-traceability.de.md`
- `docs/configuration.md` / `docs/configuration.de.md`
- `docs/connectors/apache.md` / `docs/connectors/apache.de.md`
- `docs/connectors/envoy.md` / `docs/connectors/envoy.de.md`
- `docs/connectors/traefik.md` / `docs/connectors/traefik.de.md`
- `docs/decisions/ADR-003-shared-p1-p4-lifecycle-semantics.md` / `docs/decisions/ADR-003-shared-p1-p4-lifecycle-semantics.de.md`
- `docs/decisions/README.md` / `docs/decisions/README.de.md`
- `docs/getting-started.md` / `docs/getting-started.de.md`
- `docs/migration.md` / `docs/migration.de.md`
- `docs/operations-and-security.md` / `docs/operations-and-security.de.md`
- `docs/reference/glossary.md` / `docs/reference/glossary.de.md`
- `docs/reference/with-crs-no-mrts-profile-contract.md` / `docs/reference/with-crs-no-mrts-profile-contract.de.md`
- `docs/repository-concept.md` / `docs/repository-concept.de.md`
- `examples/README.md` / `examples/README.de.md`
- `licenses/README.md` / `licenses/README.de.md`
- `licenses/apache/ORIGIN.md` / `licenses/apache/ORIGIN.de.md`
- `licenses/modsecurity/README.md` / `licenses/modsecurity/README.de.md`
- `licenses/nginx/ORIGIN.md` / `licenses/nginx/ORIGIN.de.md`
- `reports/audits/change-records/CR-20260921-root-readme-refresh.md` / `reports/audits/change-records/CR-20260921-root-readme-refresh.de.md`
- `reports/audits/change-records/CR-20261028-documentation-reconciliation.md` / `reports/audits/change-records/CR-20261028-documentation-reconciliation.de.md`

## Ausgeführte Befehle

Repository-Dateien, aktuelle master-/PR-Metadaten, Source-Definitionen und
Workflow-Ergebnisse wurden über den GitHub-Connector gelesen. Git-Baum-/Blob-
Identitäten trennten unveränderte technische Dateien von master-Änderungen.
Aussagen zu entfernten Optionen und Engine-Zuständigkeit wurden anhand von
`docs/phase4-mode-budget.md` geprüft, der gemeinsame Standard anhand von
`common/include/msconnector/options.h`.

Der Branch wurde durch einen nicht erzwungenen, auf den erwarteten Head
geprüften Ref-Update zum Abgleich-Merge mit zwei Eltern aktualisiert. GitHub-
Vergleich bestätigte master als Merge-Basis, keinen fehlenden Commit und einen
reinen Markdown-Diff. GitHub meldete den PR anschließend als mergebar.

Hosted-Lint für Abgleich-Head
`34dffc40f31cdb870e64283ebaee32b8cdd44bca` führte
`python ci/checks/documentation/check-bilingual-docs.py` aus und meldete fehlende
kanonische Change-Record-Abschnitts-/Identitätsbezeichnungen in diesem neuen
Record. Commit `1d161212124ad882064f8acfcefb721c67bc3d1d` korrigiert diese
Bezeichnungen und trennt die Pflichtabschnitte, ohne den Checker zu ändern.
Seine beobachteten Workflows `lint` und `quick-framework-check` wurden vor der
abschließenden Konzept-/Default-Korrektur erfolgreich abgeschlossen. Das sind
Ergebnisse des früheren Heads, kein vorweggenommener Erfolg des Nachfolgers.
Repository-native lokale Testbefehle werden nicht behauptet.

## Security-Auswirkung

Gegenüber abgeglichenem master ändert sich nur Dokumentation. Kein
Runtime-Verhalten, Standard, Berechtigungsumfang, Netzwerkzugriff,
Credential-Flow, keine Dependency-Auswahl, kein Workflow, Testbypass oder
Aufbewahrungsverhalten wird ergänzt. Die master-Synchronisierung übernimmt
vorhandene geprüfte master-Arbeit, statt neue Source-Änderungen in einem
Dokumentations-PR zu erzeugen.

Der Migrationstext dokumentiert bereits vorhandene Source-Entfernungen; er
autorisiert weder beliebige Engine-Standards noch das Entfernen echter
Autorisierungs-Hostgrenzen. Beispiele bleiben anzupassende Referenzen, keine
sicheren Deployment-Manifeste. Es werden keine Credentials oder sensiblen
Traffic-Artefakte hinzugefügt.

## Runtime-Evidence

Durch die Dokumentationsbearbeitung wurde keine neue Host-Laufzeitkampagne,
I12-Aufzeichnung, CRS-Prüfung, Protokollmatrix oder Produktionsqualifikation
ausgeführt. Bestehende Reports bleiben an aufgezeichnetes Profil, Revision,
Regeln, Run-ID und Artefakte gebunden. Alte erfolgreiche Workflows sind keine
Laufzeitnachweise für den finalen Head.

## Bekannte Einschränkungen

In dieser Bearbeitungsumgebung war kein vollständiger lokaler
Repository-Checkout verfügbar. Vollständige Repository-Validierung hängt daher
von Hosted-Checks des veröffentlichten Heads ab. Generierte Compiler- und
Konfigurationsreferenzen bleiben aktuelle master-Ausgaben; lokale Regeneration
wird nicht behauptet.

Technische Referenzen behalten bewusst ihre Tiefe. Die neuen Guides bilden
eine Navigations- und Migrationsschicht und ersetzen weder hostspezifische
Syntax, tatsächliche Voraussetzungen, Source-Verträge noch Deployment-Review.

## Verbleibende Risiken

Künftige Source-, Host-, Testinventar- oder Pin-Änderungen können erneut
Dokumentationsdrift erzeugen. Aktuellen Source und Checks des finalen Heads
prüfen, statt sich auf ein fixes README-Datum, historische Dateizahl oder den
Erfolg eines früheren Commits zu verlassen. Nicht unterstützte Strict-Aktionen
und unvollständige Autorisierungsstichproben müssen als Grenzen sichtbar
bleiben, statt als allgemeine Laufzeitunterstützung dargestellt zu werden.

## Nicht ausgeführte Prüfungen mit Begründung

Lokales vollständiges `make test`, `make quick-check`, `make check-bilingual-docs`,
`make check-doc-links`, `git diff --check`, Regeneration generierter Ausgaben,
All-host-Kampagnen, Sanitizer und Protokollmatrizen wurden nicht ausgeführt,
weil kein vollständiger lokaler Checkout mit Toolchain eingerichtet wurde.
Aus Remote-Source-Inspektion wird kein Validierungsergebnis erfunden.

Hosted-Ergebnisse des finalen Heads müssen nach Abschluss in der PR-
Validierungszusammenfassung festgehalten werden. Ausstehende, übersprungene
oder wegen Voraussetzungen blockierte Arbeit ist kein Erfolg. Dieser Record
autorisiert weder eine I12-Kampagne noch zusätzliche On-demand-Suiten.

## Finaler Diff- und Review-Status

Der Abgleich nutzt einen Merge mit zwei Eltern auf dem vorhandenen
Dokumentations-Branch, erhält die bisherige PR-Historie und enthält die exakt
geprüfte master-Revision. Es gab weder Force-Push noch PR-Merge oder
Branchlöschung. Der Change-Record-Formatfehler wurde in einem normalen
Nachfolger behoben; die finale Konzeptkorrektur erhält das aktuelle
Detailreferenzmaterial.

Vor Freigabe finalen Diff und CI des finalen Heads prüfen. Eine erfolgreiche
Dokumentationsänderung ist keine Produktions- oder Vollprotokollzertifizierung.
