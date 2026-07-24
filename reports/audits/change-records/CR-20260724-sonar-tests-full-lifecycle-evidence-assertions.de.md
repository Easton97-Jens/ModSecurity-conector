# Change Record: Parent-Full-Lifecycle-Evidence-Assertion-Reihenfolge für SonarQube Cloud S3415

**Sprache:** [English](CR-20260724-sonar-tests-full-lifecycle-evidence-assertions.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260724-sonar-tests-full-lifecycle-evidence-assertions |
| Datum (UTC) | 2026-07-24 |
| Basis-Revision | 8e36b86ac17bce06003b0505fe26f6bb60c3cec7 |
| Tracking | Fünf aktive Parent-SonarQube-Cloud-`python:S3415`-Code-Smells: AZ-KYVT1fYmbqbBXVNF-, AZ-KYVT1fYmbqbBXVNF_, AZ-KYVT1fYmbqbBXVNGA, AZ-KYVT1fYmbqbBXVNGB und AZ-KYVT1fYmbqbBXVNGC. |
| Grenze | Parent-Testquellcode sowie dieses englisch/deutsche Traceability-Paar und die Indizes. Framework, MRTS, Gitlinks, Scanner-Konfiguration, Quality Gates, Suppressions, Full-Lifecycle-Checker-/Runtime-Verhalten und generierte Artefakte bleiben unverändert. |

## Motivation und Problemstellung

Die ausgewählten SonarQube-Cloud-Zeilen melden, dass fünf bestehende
`unittest.assertEqual`-Aufrufe im Parent-Full-Lifecycle-Evidence-Test ihren
erwarteten Wert vor dem tatsächlichen Ergebnis platzieren. Die Assertions
prüfen bereits die richtigen Werte und Control-Pfade; allein das Umkehren ihrer
Operand-Reihenfolge verbessert die Fehlerdiagnostik, ohne zu verändern, was
der Test akzeptiert oder zurückweist.

## Akzeptanzkriterien

- Nur die fünf ausgewählten Assertions auf tatsächlichen Wert zuerst und
  erwarteten Wert danach korrigieren.
- Jedes Fixture, jeden erwarteten String/Listeneintrag, jeden Checker-Aufruf,
  Testzweig und jede Produktionsquelldatei unverändert bewahren.
- Das direkte Parent-Full-Lifecycle-Evidence-Unit-Modul, eine Source-/AST-
  Inventur der fünf Aufrufe und die Diff-Hygiene-Prüfungen bestehen.
- Ein vollständiges englisch/deutsches Change-Record-Paar und die Indizes
  pflegen.
- Exact-Head-GitHub- und SonarQube-Cloud-Draft-PR-Evidenz einholen, bevor die
  ausgewählten Keys als verifiziert beschrieben werden.

## Implementierungsentscheidung und Begründung

Jeder ausgewählte Aufruf übergibt jetzt den bestehenden Checker-Ausdruck als
erstes `assertEqual`-Argument und die unveränderte erwartete Liste als zweites.
Es wurde kein neuer Helper, keine Abstraktion, kein Fixture, kein erwarteter
Wert, keine Assertion-Nachricht und keine Runtime-Bedingung eingeführt. Dies
ist die kleinste repository-native Korrektur für `python:S3415` und bewahrt die
normalen `unittest`-Semantiken.

## Security-Auswirkung

Die fokussierte Sicherheitsbewertung lautet `not_applicable`: Die Änderung
betrifft nur die diagnostische Argument-Reihenfolge in Parent-Testcode. Sie
ändert weder Parser, Datei-/Pfad-Sinks, Subprozesse, Credentials,
Berechtigungen, Netzwerk-/CI-Controls, Sicherheitsvalidierung noch
Connector-Enforcement. Die bestehenden Full-Lifecycle-Negativtests und das
Log-Sanitizer-Control bleiben unverändert und bestehen im fokussierten
Modullauf. Es wird kein Sicherheitsbefund als behoben behauptet.

## Geänderte Dateien

- tests/test_full_lifecycle_evidence.py
- reports/audits/change-records/README.md und README.de.md
- dieses englisch/deutsche Change-Record-Paar

## Ausgeführte Befehle

Die fokussierten Kommandos nutzten Parent-.venv-Python,
`PYTHONDONTWRITEBYTECODE=1`, `PYTHONNOUSERSITE=1` und ein task-owned externes
`TMPDIR`:

- rtk proxy -- env ... <Parent .venv python> -m unittest -v tests.test_full_lifecycle_evidence
- rtk proxy -- env ... <Parent .venv python> -c <AST inventory of the five selected assertEqual calls>
- rtk proxy -- env ... <Parent .venv python> -m unittest -v tests.test_bilingual_docs
- rtk proxy -- env ... make PYTHON=<Parent .venv python> check-bilingual-docs
- rtk proxy -- env ... make PYTHON=<Parent .venv python> check-doc-links
- rtk proxy -- git diff --check
- rtk proxy -- find <current batch worktree> -name '*.pyc' -type f
- rtk proxy -- gh pr checks 112 --repo Easton97-Jens/ModSecurity-conector --watch --interval 15
- rtk proxy -- curl -fsSL <offizielle SonarQube-Cloud-PR-, Quality-Gate- und PR-Issue-Endpunkte>

## Tests und tatsächliche Ergebnisse

| Kommando oder Check | Ergebnis |
| --- | --- |
| Fokussiertes Full-Lifecycle-Evidence-Unit-Modul vor und nach der Änderung | bestanden: tests.test_full_lifecycle_evidence, jeweils 17 Tests. |
| AST-Inventur der ausgewählten Assertions | bestanden: Genau fünf ausgewählte Zeilenanker haben jetzt Checker-Ausdrücke als tatsächliche Werte und unveränderte erwartete Listen. |
| git diff --check | bestanden: kein Whitespace-Fehler. |
| Bytecode-Scan des aktuellen Batch-Worktrees | bestanden: keine `*.pyc`-Datei. Das gemeinsame temporäre Verzeichnis des Gesamt-Runs enthält sechs vorhandene Bytecode-Dateien aus früheren Batch-Worktrees, die außerhalb dieses Batch-Scopes liegen. |
| tests.test_bilingual_docs | bestanden: 11 Tests. |
| Direkter Change-Record-Paar-Review | bestanden: Beide Dateien haben 13 ausgerichtete Level-two-Abschnitte und alle IDs, Issue-Keys, Pfade, Befehle sowie nicht übersetzte technische Literale stimmen überein. |
| make check-bilingual-docs | blocked_environment: Genau 20 vorhandene fehlende Framework-Gitlink-Linkziele; die Ausgabe nennt keinen neuen Change-Record-Fehler. |
| make check-doc-links | blocked_environment: Genau 16 vorhandene fehlende Framework-Gitlink-Linkziele; es wurde kein Framework-Quellcode, Gitlink oder generiertes Artefakt geändert. |

## Runtime-Evidence

Es wurde kein Connector-Runtime-Verhalten geändert oder behauptet. Der
fokussierte Test validiert Parent-Evidence-/Checker-Verträge mit temporären
lokalen Fixtures; er ist weder Host-Traffic- noch Produktions-Runtime-Evidenz.

## Nicht ausgeführte Prüfungen mit Begründung

- Connector-Builds, Konfigurationsprüfungen, Host-Runtime-Smoke-Tests,
  Protokollmatrizen, Framework- und MRTS-Checks sind nicht anwendbar, weil
  keine Connector-/Runtime-Implementierung geändert wurde und Framework/MRTS
  ausgeschlossen sind.
- Die Initial-Exact-Head-Draft-PR-Verifikation für
  `726f56d7787289b8c9f91b68a7b315e5b35a410e` bestand: 33 GitHub-Checks waren
  erfolgreich, 6 waren scope-gerechte Skips und keiner schlug fehl, blieb
  pending, cancelled oder unknown. Das offizielle SonarQube-Cloud-Quality-Gate
  war `OK` mit null offenen PR-Issues; Reviews, Inline-Review-Kommentare und
  Review-Threads ergeben jeweils null. Dieser Traceability-Commit erzeugt
  einen neueren PR-Head, der nach dem Push unabhängig verifiziert und im PR
  sowie Task-Receipt festgehalten wird, statt hier vorab behauptet zu werden.

## Bekannte Einschränkungen

Dieser Batch korrigiert nur fünf ausgewählte Parent-SonarQube-Cloud-Befunde.
Er behauptet nicht, den breiteren SonarQube-Cloud-Backlog mit 1.474 Befunden
zu beheben.

## Verbleibende Risiken

Eine unbeabsichtigte Änderung eines Assertion-Werts könnte einen Evidence-
Control abschwächen. Der abgegrenzte Diff, die Fünf-Aufruf-AST-Inventur und das
vollständige fokussierte 17-Test-Modul reduzieren dieses Risiko; Exact-Head-
Hosted-Analyse bleibt erforderlich, bevor die Keys verifiziert sind.

## Current-Master-Update und finale lokale Verifikation

Der normale nicht umschreibende Merge `1c8a2b9` übernahm aktuellen
Parent-Master `8e36b86ac17bce06003b0505fe26f6bb60c3cec7` in den isolierten
PR-Branch. Er löste nur die gepaarten Change-Record-Indizes auf. Die geerbte
Master-Historie enthält den bereits vorhandenen Framework-Gitlink-Übergang
unter der engen Nutzerfreigabe; Framework und MRTS wurden weder ausgecheckt
noch geändert, getestet, gemergt oder ausgeliefert, und der finale PR-Diff hat
keinen Gitlink-, Framework- oder MRTS-Pfad.

Auf diesem exakten Tree vor der Record-Korrektur bestanden
`tests.test_full_lifecycle_evidence` mit allen 17 Tests,
`tests.test_bilingual_docs` mit allen 11 Tests, die Fünf-Aufruf-AST-Inventur
bestätigte tatsächliche-Checker-Werte zuerst an den ausgewählten Ankern, und
`git diff --check origin/master...HEAD` bestand. Diese Dokumentationskorrektur
erzeugt einen neuen PR-Head; daher müssen alle gehosteten Exact-Head-Checks,
das SonarQube-Cloud-Quality-Gate sowie Review-/Conversation-Evidence frisch
revalidiert werden, bevor der Draft PR als bereit markiert werden kann.

## Finaler Diff- und Review-Status

Die Source-Implementierung bleibt im Initial-Commit
`726f56d7787289b8c9f91b68a7b315e5b35a410e`; dieser Change Record wird ohne
selbstreferenziellen finalen Head aktualisiert. Draft PR #112 bleibt offen,
Draft und ungemergt, bis sein finaler Exact Head aktuelle Base-, lokale,
gehostete, SonarQube-Cloud- sowie Review-Evidence hat. Kein Merge,
Default-Branch-Update, Framework-Action oder MRTS-Action wird durch diesen
Record autorisiert oder ausgeführt.
