# Change Record: <Titel>

**Sprache:** [English](TEMPLATE.md) | Deutsch

Diese Datei und ihren englischen Begleiter nach
<code>&lt;change-id&gt;.md</code> und
<code>&lt;change-id&gt;.de.md</code> kopieren. Jeden Platzhalter ersetzen.
Keine vollständigen Logs, Runtime-Rohdaten, Secrets, vollständigen
Umgebungsvariablen, Cookies, Tokens, Bodies, privaten Schlüssel, Caches oder
Build-Artefakte einchecken.

## Identität

| Feld | Wert |
| --- | --- |
| Titel | &lt;kurzer beschreibender Titel&gt; |
| Change-ID | CR-YYYYMMDD-short-slug |
| Datum (UTC) | YYYY-MM-DDTHH:MM:SSZ |
| Autor oder ausführender Agent | &lt;Name oder Agent-Identität&gt; |
| Basis-Revision | &lt;vollständige Commit-ID vor der Änderung&gt; |
| Zugehöriges Issue oder Pull Request | &lt;Link oder None&gt; |
| Finale Revision | &lt;Commit-ID oder nicht committed&gt; |

## Motivation und Problemstellung

<Aufgabe, Auswirkung und Grund für die Änderung beschreiben.>

## Betroffene Komponenten und Sicherheitsgrenzen

<Geänderte Komponenten, Schnittstellen, Vertrauens-/Datengrenzen und lokale
Konfiguration nennen, die absichtlich außerhalb des versionierten Diffs
bleibt.>

## Akzeptanzkriterien

| Kriterium | Status | Evidenz |
| --- | --- | --- |
| &lt;beobachtbares Kriterium&gt; | &lt;erfüllt / nicht erfüllt / verschoben&gt; | &lt;Test, Review oder Record-Abschnitt&gt; |

## Untersuchte Alternativen

<Betrachtete Alternativen und den Grund für ihre Verwerfung oder Nichtauswahl
beschreiben.>

## Implementierungsentscheidung und Begründung

<Gewähltes Design einschließlich sicherheitsrelevanter Abwägungen beschreiben.>

## Geänderte Dateien

<Die tatsächlichen finalen versionierten Dateien aufführen. Absichtlich lokale,
unversionierte Konfiguration getrennt nennen, ohne sie als Teil des Git-Diffs
darzustellen.>

## Hinzugefügte oder geänderte Tests

<Hinzugefügte oder geänderte Tests aufführen oder None schreiben.>

## Ausgeführte Befehle

| Exakter Befehl | Exit-Code oder Ergebnis | Sanitisierte relevante Zusammenfassung | Kanonischer Evidence-Pfad | Run-ID |
| --- | --- | --- | --- | --- |
| &lt;exakter Befehl&gt; | &lt;0 / PASS / anderes Ergebnis&gt; | &lt;kurze faktische Zusammenfassung&gt; | &lt;repository-relativer Pfad, portabler Platzhalter oder None&gt; | &lt;Run-ID oder None&gt; |

Jeden tatsächlich ausgeführten Befehl dokumentieren. Keine vollständige
Ausgabe einfügen. Ein geplanter, übersprungener oder vermuteter Befehl gehört
unter „Nicht ausgeführte Prüfungen mit Begründung“, nicht als bestandenes
Ergebnis.

## Security-Auswirkung

<Sicherheitsauswirkung, geänderte Grenzen/Defaults/Validierung/Logging
beschreiben oder Keine Änderung des Sicherheitsverhaltens schreiben.>

## Dokumentationsänderungen

<Aktualisierte Dokumentation/Beispiele und Sprachbegleiter aufführen oder None
schreiben.>

## Runtime-Evidence

<Run-ID, Profil/Scope, kanonischen sanitisierten Evidence-Ort und abgegrenzte
Beobachtung angeben; oder ausdrücklich schreiben: „Für diese Änderung wurde
keine Runtime-Evidence erhoben oder beansprucht.“ Ein Build, Lint,
Konfigurationscheck, Unit-Test oder Smoke ist für sich kein Runtime-Claim.>

## Bekannte Einschränkungen

<Bekannte Einschränkungen aufführen oder None schreiben.>

## Verbleibende Risiken

<Verbleibende Risiken, Minderungen oder None aufführen.>

## Nicht ausgeführte Prüfungen mit Begründung

<Jede relevante nicht ausgeführte Prüfung und den Grund nennen oder None
schreiben.>

## Finaler Diff- und Review-Status

<Ergebnis der finalen Diff-/Whitespace-Prüfung, Review-Status, Abgleich des
Records mit tatsächlichem finalen Diff und realen Testergebnissen sowie
beabsichtigten Commit- oder Pull-Request-Status angeben.>
