# Nachvollziehbarkeitsrichtlinie für Änderungen

**Sprache:** [English](change-traceability.md) | Deutsch

## Schnellorientierung

Diese Policy hält Dokumentation und Delivery-Fakten reviewbar. Für eine normale
nicht triviale Änderung gilt praktisch: Englisch und Deutsch gemeinsam
aktualisieren, technische Literale identisch halten, nur tatsächlich
ausgeführte Prüfungen dokumentieren, Build-/Static-Ergebnisse nicht zu
Runtime-Claims hochstufen und generiertes Material über seinen Generator
ändern. Pull-Request-Beschreibung und ein erforderlicher Change Record müssen
zum finalen Diff und zu den beobachteten Ergebnissen passen.

Diese Richtlinie macht die zweisprachige Pflege zu einem Teil der Definition of
Done für repository-eigene, versionierte und für Menschen bestimmte Inhalte.
Sie gilt für jedes Feature, jeden Bugfix, jeden Security-Fix und jede sonstige
nicht triviale Änderung.

## Geltungsbereich und Sprachmodell

Englisch ist die technische Primärsprache. Deutsch ist eine vollständige
Begleitfassung und keine verkürzte Zusammenfassung. Jedes relevante,
versionierte und für Menschen bestimmte Dokument muss in beiden Sprachen
vorliegen und aktuell gehalten werden, normalerweise als <code>name.md</code>
und <code>name.de.md</code>.

## Verpflichtend zweisprachige Inhalte

| Inhaltstyp | Zweisprachige Anforderung |
| --- | --- |
| Repository- und Connector-Dokumentation | READMEs, Connector-Guides, Installations-, Konfigurations-, Build-, Test-, Architektur-, Design-, Migrations- und Einschränkungsdokumentation als Englisch-/Deutsch-Paare pflegen. |
| Security- und Evidenzmaterial | Sicherheitsdokumentation, Audit- und Finding-Berichte, Change Records, manuell gepflegte Reports, Testergebnisse, Runtime-Evidenz, Restrisiken und zugehörige Warnungen in beiden Sprachen gleichwertig halten. |
| Benutzergerichtetes Material | Beispiele, Release Notes, Changelogs, Issue-Vorlagen und weitere benutzergerichtete GitHub-Texte zweisprachig halten; die Pull-Request-Vorlage enthält vollständige englische und deutsche Abschnitte in einer Datei. |
| Neue Dokumentation | Beide Sprachdateien in derselben Änderung anlegen und wechselseitige Sprachumschalter hinzufügen. |

## Inhaltliche Gleichwertigkeit

Beide Fassungen müssen dieselben Funktionen, Voraussetzungen, Konfigurationen,
Sicherheitswarnungen, Beispiele, Befehle, unterstützten und nicht unterstützten
Szenarien, bekannten Einschränkungen, Testergebnisse, Runtime-Evidenz,
Restrisiken, Links und Referenzen vermitteln. Überschriften- und
Tabellenstruktur bleiben gleich, soweit die Repository-Prüfung dies verlangt.
Keine Sprachfassung darf einen wesentlichen Fakt enthalten, der in der anderen
fehlt.

## Unverändert bleibende technische Inhalte

Nicht übersetzt werden Quellcode; Namen von Variablen, Funktionen, Klassen,
Typen oder API-Feldern; Protokollnamen; Konfigurationsschlüssel; Dateinamen oder
Pfade; Shell-Befehle; Kommandozeilenoptionen; Codeblöcke; technisch exakte
Fehlermeldungen; Commit-Hashes; Run-IDs; URLs; sowie maschinenlesbares JSON,
YAML, TOML oder XML. Quellcode-Kommentare bleiben auf Englisch. Die
benutzergerichtete Erklärung um diese Literale wird übersetzt, das Literal
selbst bleibt unverändert.

## Lokale Codex-Dateien

Die folgende ausschließlich lokale Konfiguration benötigt keine deutsche
Begleitdatei: <code>AGENTS.md</code>, <code>AGENTS.override.md</code>, von
ihnen per <code>@...</code> eingebundene Markdown-Steuerdateien auf
Wurzelebene und <code>.codex/</code>. Für eine aktive lokale Steuerdatei darf
keine deutsche Begleitdatei angelegt werden. Diese lokalen Anweisungen
verpflichten Codex dennoch dazu, alle versionierten, benutzergerichteten
Inhalte nach dieser Richtlinie zu pflegen.

## Arbeitsablauf bei Änderungen

Für jede nicht triviale Änderung:

1. Betroffene englische und deutsche Dokumente vor der Bearbeitung ermitteln.
2. Beide Fassungen gemeinsam bearbeiten; bei neuen Dokumenten beide Dateien
   sofort anlegen.
3. Fakten, technische Werte, Links, Überschriften, Tabellen, Tests, Evidenz,
   Einschränkungen und Risiken synchron halten.
4. In deutschen Dokumenten nach Möglichkeit auf deutsche Begleitfassungen
   verweisen, wenn eine Begleitfassung existiert.
5. Befehle und andere technische Literale in beiden Fassungen unverändert
   bewahren.
6. Beide Sprachpfade im Change Record aufführen.
7. Generatoren oder Quelldaten anpassen statt nur erzeugte Ausgaben zu ändern,
   und sicherstellen, dass der Generator beide Sprachfassungen erzeugt.
8. Die Bilingual-Dokumentationsprüfung vor Abschluss der Arbeit ausführen.

## Change Records

Change-Record-Paare unter <code>reports/audits/change-records/</code> ablegen.
Jedes Paar heißt <code>&lt;change-id&gt;-&lt;name&gt;.md</code> und
<code>&lt;change-id&gt;-&lt;name&gt;.de.md</code>. Der englische und der
deutsche Record müssen dieselben Fakten und tatsächlichen Werte enthalten.

| Erforderliche Metadaten | Anforderung |
| --- | --- |
| Change-ID | Dieselbe stabile Kennung in beiden Records verwenden. |
| Datum und Basis-Revision | Dasselbe Datum und dieselbe Basis-Revision in beiden Records festhalten. |
| Motivation und Akzeptanzkriterien | Dieselbe Begründung der Änderung und dieselben messbaren Abschlussbedingungen erläutern. |
| Technische und Security-Entscheidungen | Dieselben technischen Entscheidungen, die Security-Auswirkung und die betroffene Grenze festhalten. |
| Dateien und Verifikation | Dieselben geänderten Dateien, Testbefehle, tatsächlichen Ergebnisse, Runtime-Evidenz und nicht ausgeführten Prüfungen aufführen. |
| Verbleibender Zustand | Dieselben bekannten Einschränkungen, Restrisiken und den finalen Review-Status festhalten. |

Die folgenden Abschnittsnamen sind exakt vorgeschrieben, keine Synonyme.
Ihre einzige maschinenlesbare Quelle ist
<code>ci/checks/documentation/check-bilingual-docs.py</code>.
Der Regressionstest gleicht diese Tabellen mit dieser Quelle ab.

| English | Deutsch |
| --- | --- |
| <code>## Identity</code> | <code>## Identität</code> |
| <code>## Motivation and problem statement</code> | <code>## Motivation und Problemstellung</code> |
| <code>## Acceptance criteria</code> | <code>## Akzeptanzkriterien</code> |
| <code>## Implementation decision and rationale</code> | <code>## Implementierungsentscheidung und Begründung</code> |
| <code>## Changed files</code> | <code>## Geänderte Dateien</code> |
| <code>## Commands executed</code> | <code>## Ausgeführte Befehle</code> |
| <code>## Security impact</code> | <code>## Security-Auswirkung</code> |
| <code>## Runtime evidence</code> | <code>## Runtime-Evidence</code> |
| <code>## Known limitations</code> | <code>## Bekannte Einschränkungen</code> |
| <code>## Remaining risks</code> | <code>## Verbleibende Risiken</code> |
| <code>## Checks not run and rationale</code> | <code>## Nicht ausgeführte Prüfungen mit Begründung</code> |
| <code>## Final diff and review status</code> | <code>## Finaler Diff- und Review-Status</code> |

Diese exakten Bezeichnungen der Identitätstabelle verwenden, mit identischen
Werten in beiden Sprachen:

| English | Deutsch |
| --- | --- |
| <code>Change ID</code> | <code>Change-ID</code> |
| <code>Date (UTC)</code> | <code>Datum (UTC)</code> |
| <code>Base revision</code> | <code>Basis-Revision</code> |

Beide Sprachvorlagen gemeinsam mit
<code>ci/tools/new-change-record.py</code> anlegen statt Überschriften frei
zu formulieren. Das Werkzeug importiert das vorhandene Prüfschema, validiert
das erzeugte Paar und schreibt nur zwei neue Dateien im bestehenden
Change-Record-Archiv. Es benötigt POSIX-Verzeichnisdeskriptoren, lehnt
symbolisch verknüpfte Ausgabeverzeichnisse ab und überschreibt keine vorhandene
Datei. Bei einem normalen Erstellungsfehler entfernt es nur neu angelegte
Dateien mit weiterhin passender Identität; der Zwei-Dateien-Vorgang ist nicht
absturzatomar.

<code>BASE_REVISION</code> auf den tatsächlichen vollständigen Git-Commit-SHA
der Änderungsbasis setzen: 40 Zeichen in Kleinbuchstaben. <code>my-change</code>
durch einen kleingeschriebenen, mit Bindestrichen getrennten Namen mit maximal
80 Zeichen ersetzen. Standarddatum ist das aktuelle UTC-Datum;
<code>--date YYYY-MM-DD</code> erlaubt ein ausdrücklich angegebenes gültiges
Datum. Diese nativen Befehlspayloads über einen gegebenenfalls vom lokalen
Arbeitsvertrag vorgeschriebenen Ausführungswrapper starten:

~~~sh
python3 ci/tools/new-change-record.py create --name my-change --base-revision "$BASE_REVISION"
python3 ci/tools/new-change-record.py check
python3 -m unittest -v tests.test_change_record tests.test_prepare_reviewed_framework_handoff
~~~

Alle offenen Absätze und den Vorlagenhinweis durch tatsächliche Fakten
ersetzen, einschließlich nicht ausgeführter Prüfungen und verbleibender
Risiken. Die erzeugten Überschriften und Identitätsbezeichnungen unverändert
lassen. Das sind bearbeitbare Vorlagen, keine generierte Evidence und kein
Nachweis einer abgeschlossenen Änderung.

Der quick-framework-CI-Workflow führt die reine Archivprüfung und ihre
Regressionen vor dem Framework-Setup aus. Die frühe Prüfung liest nur das
Record-Archiv und startet keinen Git-Befehl. Sie lehnt auch verwaiste
Sprachdateien ab. Sie ersetzt weder <code>make check-bilingual-docs</code>
noch <code>make check-doc-links</code>, die manuelle Prüfung der Sprachinhalte
oder Security-/Runtime-Prüfungen. Ein strukturell gültiger Record kann
weiterhin unvollständigen oder unzutreffenden Fließtext enthalten.

## Features und Bugfixes

Wenn sich Verhalten ändert, mindestens Haupt-README, betroffenes
Connector-README, Konfigurationsdokumentation, Architektur- oder
Lifecycle-Dokumentation, Beispiele, bekannte Einschränkungen und Change Record
in beiden Sprachen auf Aktualisierung prüfen. Ein Build- oder
Konfigurationsergebnis ist keine Runtime-Evidenz, sofern die dokumentierte
Testebene dies nicht aussagt.

## Security-Findings und -Fixes

Bei einem Security-Finding oder -Fix müssen beide Fassungen die betroffene
Sicherheitsgrenze, Angriffsvoraussetzungen, Auswirkung, technische Ursache,
Korrekturstrategie, Regressionstest, Verifikation des ursprünglichen
Angriffspfads, Restrisiko und gegebenenfalls Migrations- oder
Konfigurationshinweise beschreiben. Sensible Payloads, Tokens, Cookies, Bodies
oder private Umgebungswerte dürfen in keiner Fassung erscheinen.

## Generierte Dokumentation

Nicht nur eine erzeugte Datei aktualisieren. Ihren Generator oder die
Quelldaten anpassen, den Generator beide Sprachfassungen erzeugen lassen und
automatisch übersetzte oder manuell gepflegte Begleitdateien gemäß den
Repository-Regeln für generierte Dateien markieren.

## Pull Requests und GitHub-Texte

Die Pull-Request-Vorlage muss vollständige englische und deutsche Abschnitte
beibehalten. Jeder Abschnitt enthält Zusammenfassung, Motivation,
Akzeptanzkriterien, wichtigste Änderungen, Testbefehle und tatsächliche
Ergebnisse, Security-Auswirkung, Dokumentationsänderungen, Runtime-Evidenz,
bekannte Einschränkungen, nicht ausgeführte Prüfungen sowie eine Change-ID oder
einen Change-Record-Link. Issue-Vorlagen und weitere benutzergerichtete
GitHub-Texte als gleichwertige englisch/deutsche Inhalte pflegen.

## Abschlussprüfung

Eine Aufgabe nicht als abgeschlossen melden, wenn eine erforderliche
Sprachfassung fehlt oder veraltet ist. Nach der Änderung diese Befehle
ausführen:

~~~sh
make check-bilingual-docs
make check-doc-links
git diff --check
git status --short
~~~

Zusätzlich manuell bestätigen, dass für keine aktive lokale Steuerdatei eine
deutsche Begleitdatei erstellt wurde, neue versionierte Richtlinien und
Vorlagen vollständig zweisprachig sind, beide Fassungen dieselben technischen
Fakten enthalten und unabhängige Änderungen unberührt blieben.
