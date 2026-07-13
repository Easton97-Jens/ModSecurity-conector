# Change Records

**Sprache:** [English](README.md) | Deutsch

Dieses Verzeichnis enthält manuell gepflegte, versionierte Change Records für
jedes Feature, jeden Bugfix, jeden Security-Fix und jede sonstige nicht triviale
Repository-Änderung. Ein Record ergänzt Commit und Pull Request um Anforderung,
Entscheidungsweg, tatsächliche Prüfergebnisse, Evidence-Grenze und verbleibende
Einschränkungen. Er ist kein Generated Runtime-Report und macht aus einem Build
oder Testergebnis keinen Runtime-Claim.

Lesen Sie vor dem Erstellen oder Aktualisieren eines Records die verbindliche
[Richtlinie zur Nachvollziehbarkeit](../../../docs/change-traceability.de.md).

## Record erstellen oder aktualisieren

1. Ein Change Record ist für jedes Feature, jeden Bugfix, jeden Security-Fix
   und jede sonstige nicht triviale Repository-Änderung erforderlich. Eine
   eindeutige stabile ID im Format <code>CR-YYYYMMDD-short-slug</code> wählen;
   bei Bedarf <code>-01</code>, <code>-02</code> und so weiter anhängen.
2. <code>TEMPLATE.md</code> und
   [TEMPLATE.de.md](TEMPLATE.de.md) in passende Dateien
   <code>&lt;change-id&gt;.md</code> und
   <code>&lt;change-id&gt;.de.md</code> kopieren; der beschreibende
   <code>short-slug</code> ist Teil der Change-ID und kein sprachspezifischer
   Dateiname.
3. Beide Sprachbegleiter ausfüllen. Ein manuell gepflegter Record unter
   <code>reports/</code> bleibt ein englisch-deutsches Paar mit denselben
   technischen Fakten, Ergebnissen, Evidenz, Einschränkungen und Risiken.
   Befehle, Pfade, Dateinamen, Change-IDs, Commit-Hashes, Run-IDs, Statuswerte
   und Konfigurationsschlüssel in beiden Fassungen unverändert bewahren.
4. Nur tatsächlich ausgeführte Befehle und ihre realen Ergebnisse einschließlich
   Fehlschlägen dokumentieren. Geplante Tests dürfen nicht als bestanden
   dokumentiert werden; übersprungene und nicht ausgeführte Prüfungen mit ihrer
   Begründung sichtbar halten. Das fertige Paar vor Abschluss mit dem final
   beabsichtigten Diff abgleichen.

## Identität

Die Identitätstabelle der Vorlage für Titel, eindeutige Change-ID, Datum (UTC),
Autor oder ausführenden Agent, Basis-Revision und gegebenenfalls zugehöriges
Issue oder Pull Request verwenden. Die finale Revision eintragen, sobald sie
verfügbar ist, und die entsprechenden technischen Werte in beiden
Sprachbegleitern identisch halten.

## Motivation und Problemstellung

Aufgabe, betroffene Nutzer oder Maintainer und Grund für die Änderung
erklären. Der Record soll das angestrebte Ergebnis verständlich machen, ohne
sich nur auf den Commit-Betreff zu stützen.

## Betroffene Komponenten und Sicherheitsgrenzen

Geänderte Komponenten, Schnittstellen, Vertrauens- oder Datengrenzen und
absichtlich lokale unversionierte Konfiguration aufführen, die außerhalb des
versionierten Diffs bleibt. Die relevante Grenze auch dann nennen, wenn die
Änderung sie nicht verändert.

## Akzeptanzkriterien

Beobachtbare Kriterien verwenden und jedem einen Status sowie stützende
Evidenz geben. Implementiertes Verhalten von verschobener Arbeit und
ausdrücklich abgegrenztem Umfang trennen.

## Untersuchte Alternativen

Betrachtete Alternativen und den Grund für ihre Verwerfung oder Nichtauswahl
festhalten, damit der gewählte Ansatz in seinem ursprünglichen Kontext
reviewbar bleibt.

## Implementierungsentscheidung und Begründung

Alternativen, den gewählten Ansatz und seine technischen oder
sicherheitsrelevanten Abwägungen zusammenfassen. Auf einen ausführlicheren
Entscheidungsrecord verweisen, falls vorhanden.

## Geänderte Dateien

Die tatsächlichen finalen versionierten Dateien aufführen. Absichtliche lokale,
unversionierte Konfiguration getrennt nennen, damit sie nicht mit dem Git-Diff
verwechselt wird.

## Hinzugefügte oder geänderte Tests

Hinzugefügte oder geänderte Tests aufführen oder <code>None</code> schreiben.
Dieses Verzeichnis von den tatsächlich ausgeführten Befehlen und ihren
Ergebnissen unterscheiden.

## Ausgeführte Befehle

Für jeden tatsächlich ausgeführten Prüfungsbefehl die Vorlagentabelle nutzen:
exakter Befehl, Exit-Code oder Ergebnis, kurze sanitisierte Zusammenfassung,
kanonischer Evidence-Ort und vorhandene Run-ID. Fehlgeschlagene Befehle und
ihre realen Ergebnisse sichtbar dokumentieren; geplante, übersprungene oder
nicht ausgeführte Befehle gehören unter „Nicht ausgeführte Prüfungen mit
Begründung“ und nicht zu bestandenen Ergebnissen.

## Security-Auswirkung

Geänderte Sicherheitsgrenzen, Validierung, Defaults, Logging oder Threat
Exposure beschreiben. Ausdrücklich sagen, wenn die Änderung kein
Sicherheitsverhalten verändert.

## Dokumentationsänderungen

Aktualisierte Dokumentation oder Beispiele und ihre Sprachbegleiter aufführen
oder <code>None</code> schreiben. Generierte Dokumentation und Reports von
manuell gepflegten Change Records unterscheiden: Generiertes Material über
seinen Generator oder seine Quelldaten aktualisieren und generierte Evidenz
nicht als manuell gepflegten Record darstellen.

## Runtime-Evidence

Runtime-Claims benötigen einen passenden sanitisierten kanonischen Lauf mit
Run-ID, Profil/Scope und Evidence-Ort. Andernfalls ausdrücklich sagen, dass
keine Runtime-Evidence erhoben oder beansprucht wurde.

## Bekannte Einschränkungen

Bekannte Einschränkungen, nicht unterstützte Pfade und abgegrenzte Annahmen
aufführen.

## Verbleibende Risiken

Ungelöste Risiken und Minderungen festhalten, damit sie nach dem Merge
reviewbar bleiben.

## Nicht ausgeführte Prüfungen mit Begründung

Jede relevante nicht ausgeführte Prüfung und den Grund nennen. Geplante,
übersprungene oder vermutete Befehle dürfen nicht als bestanden dargestellt
werden.

## Finaler Diff- und Review-Status

Vor Abschluss finalen Diff-/Whitespace-Review, Review-Status und die
Bestätigung festhalten, dass der Record mit dem tatsächlichen finalen Diff und
realen Ergebnissen übereinstimmt.

## Daten- und Evidence-Grenze

Hier keine vollständigen Logs, Runtime-Rohdaten, Builds, Caches, Secrets,
vollständigen Umgebungsvariablen, Cookies, Tokens, Bodies, privaten Schlüssel
oder operator-spezifischen absoluten Pfade ablegen. Nur kurze sanitisierte
Zusammenfassungen, portable kanonische Evidence-Orte und vorhandene Run-IDs
speichern. Runtime-Rohdaten und Build-Ausgaben bleiben außerhalb des Checkouts.

## Records

| Change-ID | UTC-Datum | Thema | Record |
| --- | --- | --- | --- |
| CR-20260713-change-traceability-governance | 2026-07-13 | Versionierte Change-Traceability-Governance | English companion / [Deutsch](CR-20260713-change-traceability-governance.de.md) |
| CR-20260713-bilingual-policy-enforcement | 2026-07-13 | Durchsetzung der zweisprachigen Richtlinie | English companion / [Deutsch](CR-20260713-bilingual-policy-enforcement.de.md) |
