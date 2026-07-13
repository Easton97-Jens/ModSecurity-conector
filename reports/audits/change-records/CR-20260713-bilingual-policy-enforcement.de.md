# Change Record: Durchsetzung der zweisprachigen Richtlinie

**Sprache:** [English](CR-20260713-bilingual-policy-enforcement.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Titel | Durchsetzung der zweisprachigen Richtlinie |
| Change-ID | CR-20260713-bilingual-policy-enforcement |
| Datum (UTC) | 2026-07-13T19:40:08Z |
| Autor oder ausführender Agent | Codex-Agent <code>/root</code> |
| Basis-Revision | 056f93232c6f5dba132bfb2204d96ce49707507b |
| Zugehöriges Issue oder Pull Request | None |
| Finale Revision | Nicht committed |

## Motivation und Problemstellung

Englisch-deutsche Gleichwertigkeit als dauerhafte, erzwingbare Repository-Regel
statt als Best-Effort-Dokumentationskonvention etablieren. Die Arbeit entfernt
außerdem veraltete versionierte Links auf lokale Codex-Anweisungen, die in einem
sauberen Checkout nicht vorhanden sein können.

## Betroffene Komponenten und Sicherheitsgrenzen

Die Änderung betrifft für Menschen bestimmte Markdown-Dateien, den
Bilingual-Dokumentationschecker, den Repository-Linkchecker, Pull-Request-
Hinweise und lokale Codex-Arbeitsanweisungen. Connector-Runtime-Verhalten wird
nicht geändert. Dokumentation und Change Records schließen weiterhin Secrets,
Tokens, Cookies, Bodies, private Umgebungswerte, Runtime-Rohdaten, Builds und
Caches aus.

Unabhängige, gleichzeitig bearbeitete Change-Record-Governance-Artefakte unter
<code>reports/audits/change-records/</code> wurden bewahrt. Dieser Record deckt
die Durchsetzung und Sprachpaar-Arbeit dieser Änderung ab.

## Akzeptanzkriterien

| Kriterium | Status | Evidenz |
| --- | --- | --- |
| Relevantes repository-eigenes, für Menschen bestimmtes Markdown hat einen englisch-deutschen Begleiter | Erfüllt | <code>make check-bilingual-docs</code> besteht mit erweitertem Geltungsbereich. |
| Lokale Codex-Konfiguration bleibt ungepaart und verlangt zugleich zweisprachige versionierte Inhalte | Erfüllt | Lokale Workflow-Dateien existieren; der Checker weist verbotene lokale deutsche Begleiter zurück. |
| Die Pull-Request-Vorlage enthält alle erforderlichen englischen und deutschen Abschnitte | Erfüllt | Checker-Unit-Test und <code>make check-bilingual-docs</code> bestehen. |
| Erforderliche Link-, Whitespace- und Statuschecks haben tatsächliche dokumentierte Ergebnisse | Erfüllt | Fokussierte finale Befehle in diesem Record bestanden. |

## Untersuchte Alternativen

- Die früheren Checker-Ausnahmen für <code>ORIGIN.md</code> und
  <code>TODO.md</code> der Connectoren beibehalten. Verworfen, weil sie
  versionierte, für Menschen bestimmte Inhalte der zweisprachigen Richtlinie
  sind.
- <code>AGENTS.de.md</code> oder <code>RTK.de.md</code> anlegen, um veraltete
  Links zu reparieren. Verworfen, weil lokale Codex-/RTK-Konfiguration
  ungepaart bleiben muss.
- Die Durchsetzung auf Sprachumschalter beschränken. Verworfen, weil der neue
  Checker zusätzlich Geltungsbereich, Struktur, Change Records und
  Pull-Request-Felder prüfen muss.

## Implementierungsentscheidung und Begründung

Ein versioniertes Richtlinienpaar ergänzen, lokale Workflow-Anweisungen
verstärken, die vorhandenen Connector- und Lizenz-Markdown-Paare vervollständigen
und den Checker diese Paarregeln erzwingen lassen. Fokussierte Unit-Tests für
das neue Checker-Verhalten hinzufügen. Versionierte Links auf das lokale
<code>AGENTS.md</code> durch die versionierte Richtlinie ersetzen, damit ein
sauberer Checkout Links validieren kann.

## Geänderte Dateien

Versionierte Dateien im Umfang:

- <code>docs/change-traceability.md</code> und
  <code>docs/change-traceability.de.md</code>
- <code>README.md</code>, <code>README.de.md</code>,
  <code>docs/reference/variables.md</code> und
  <code>docs/reference/variables.de.md</code>
- <code>.github/pull_request_template.md</code>
- <code>ci/checks/documentation/check-bilingual-docs.py</code>,
  <code>ci/checks/documentation/check-repository-path-references.py</code>
  und <code>tests/test_bilingual_docs.py</code>
- Englisch-deutsche <code>TODO.md</code>-Paare unter
  <code>connectors/_template/</code> und jedem ausgewählten Connector
- Englisch-deutsche <code>ORIGIN.md</code>-Paare für die ausgewählten
  Connectoren
- Englisch-deutsche Lizenz- und Provenienzpaare unter <code>licenses/</code>
- dieses englisch-deutsche Change-Record-Paar

Absichtliche lokale, unversionierte Dateien sind <code>AGENTS.md</code>,
<code>.codex/context/conventions.md</code>,
<code>.codex/context/definition-of-done.md</code>,
<code>.codex/context/task-workflow.md</code> und
<code>.codex/context/security-workflow.md</code>.

## Hinzugefügte oder geänderte Tests

<code>tests/test_bilingual_docs.py</code> hinzugefügt. Der Test prüft
Strukturparität für <code>docs/</code>, den Lizenz-Geltungsbereich, verbotene
lokale Begleiter, erforderliche Pull-Request-Felder und übereinstimmende
technische Change-Record-Identitätswerte.

## Ausgeführte Befehle

| Exakter Befehl | Exit-Code oder Ergebnis | Sanitisierte relevante Zusammenfassung | Kanonischer Evidence-Pfad | Run-ID |
| --- | --- | --- | --- | --- |
| <code>rtk .venv/bin/python -m unittest -v tests.test_bilingual_docs</code> | 0 | Fünf fokussierte Bilingual-Checker-Tests bestanden. | None | None |
| <code>rtk make check-bilingual-docs</code> | 0 | Erweiterte Paar-, Struktur-, Change-Record-, Pull-Request- und lokale-Begleiter-Prüfungen meldeten <code>bilingual docs ok</code>. | None | None |
| <code>rtk make check-doc-links</code> | 0 | Repository-Pfadreferenzen und Framework-Dokumentlinks bestanden. | None | None |
| <code>rtk git diff --check</code> | 0 | Keine Whitespace-Diagnostik für getrackte Änderungen. | None | None |
| <code>rtk git status --short</code> | 0 | Finaler Status listete die versionierten Änderungen im Umfang und keine lokalen deutschen Codex-/RTK-Begleiter. | None | None |

## Security-Auswirkung

Keine Änderung des Connector-Runtime-Sicherheitsverhaltens. Der neue Ablauf
verlangt, dass beide Sprachen Sicherheitsgrenzen, Angriffsvoraussetzungen,
Auswirkung, Ursache, Korrekturen, Regressionsevidenz und Restrisiko ohne
sensible Daten dokumentieren. Der Checker verringert die Gefahr, dass
erforderliche Sicherheitsdokumentation stillschweigend ohne Begleitfassung
bleibt.

## Dokumentationsänderungen

Versioniertes Richtlinienpaar und lokale zweisprachige Workflow-Hinweise
hinzugefügt. Englisch-deutsche Paare für Connector-Planung, Provenienz und
Lizenzmaterial vervollständigt. Benutzergerichtete Pull-Request-Hinweise und
versionierte Richtlinienlinks aktualisiert. Englisch-deutsche Change-Record-
Einträge für diese nicht triviale Änderung hinzugefügt.

## Runtime-Evidence

Keine Runtime-Evidence erhoben oder beansprucht. Diese Dokumentations- und
Governance-Änderung macht keinen Connector-Runtime-Claim.

## Bekannte Einschränkungen

- Semantische Übersetzungsqualität braucht weiterhin Urteil von Autor und
  Review; ein automatischer Checker kann Struktur und ausgewählte technische
  Fakten prüfen, nicht jede Bedeutung.
- Generierte Reports können zusätzlich zum allgemeinen Bilingual-Checker
  generatorspezifische Validierung erfordern.
- Lokale Codex-Anweisungen sind absichtlich unversioniert; die versionierte
  Richtlinie bleibt der dauerhafte Repository-Vertrag.

## Verbleibende Risiken

Ein zukünftiges Dokument kann semantisch veralten, wenn ein Review eine
Übersetzungsabweichung übersieht. Erforderliche Sprachpaare, Strukturchecks,
Change Records, Pull-Request-Felder und explizite Abschlussprüfungen mindern,
beseitigen dieses Risiko aber nicht vollständig.

## Nicht ausgeführte Prüfungen mit Begründung

- <code>make quick-check</code> und <code>make lint</code> wurden nicht
  ausgeführt, weil die angeforderten fokussierten Dokumentations-, Link-, Diff-
  und Statuschecks diese Dokumentations-/Governance-Änderung abdecken.
- Connector-Builds, Konfigurationschecks, Lifecycle-Läufe und Runtime-Tests
  wurden nicht ausgeführt, weil kein Runtime-Verhalten geändert wurde und
  diese Befehle externe Build- oder Evidence-Artefakte erzeugen können.

## Finaler Diff- und Review-Status

Der abgegrenzte finale Diff und beide Sprachfassungen wurden geprüft. Die
fokussierten Unit-, Bilingual-Dokumentations-, Link- und Whitespace-Checks
bestanden. Es wurde kein Commit und kein Pull Request erstellt. Dieser Record
ist mit tatsächlichem finalem Diff und Testergebnissen abgeglichen und wird
nach dem Hinzufügen erneut geprüft.
