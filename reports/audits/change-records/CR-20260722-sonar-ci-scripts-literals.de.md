# Change Record: Parent-CI- und Scripts-Literal-Deduplizierung für SonarQube Cloud S1192

**Sprache:** [English](CR-20260722-sonar-ci-scripts-literals.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260722-sonar-ci-scripts-literals |
| Datum (UTC) | 2026-07-22 |
| Basis-Revision | 961b4fa37cee257a9d50542b3968005e0e21f556 |
| Tracking | Dreizehn Parent-only python:S1192 Code Smells: sieben in scripts/generate_connector_guides.py und sechs in ci/evidence/reports/generate-system-environment-proof.py. |
| Grenze | Parent-CI-/Report- und Guide-Generator-Source sowie dieses englisch/deutsche Traceability-Paar und die Indizes. Framework, MRTS, Gitlinks, generierter Guide-Inhalt, Scanner-Konfiguration, Quality Gates, Suppressions und Connector-Runtime-Verhalten bleiben unverändert. |

## Motivation und Problemstellung

SonarQube Cloud meldet wiederholte unveränderliche Metadata-Literale in zwei
Parent-Python-Generatoren. Die Vorkommen beschreiben Guide-Table-Metadata,
Fallback-Labels, den POSIX-Shell-Pfad, Report-Table-Markup und den Apache-
Toolnamen. Sie können als Modulkonstanten ausgedrückt werden, ohne generierten
Text, Tool-Resolution, Path-Checks, Report-Layout oder Control Flow zu ändern.

## Akzeptanzkriterien

- Jedes ausgewählte wiederholte Literal über eine unveränderliche
  Modulkonstante leiten, ohne seinen Wert oder das Verhalten am Use-Site zu
  ändern.
- Generierten Connector-Guide-Output und den erfolgreichen
  --skip-check-runs-Pfad des System-Environment-Proof-Generators bewahren.
- Beide Change-Record-Sprachen und beide Indizes gleichwertig halten.
- Frische SonarQube-Cloud- und Hosted-Check-Evidence für den exakten Draft-
  PR-Head einholen, bevor ein ausgewählter Key als behoben gilt.

## Implementierungsentscheidung und Begründung

Der Guide-Generator benennt die gemeinsamen Rule-File-Metadata-, Provisioning-,
Provider- und Build-Directory-Strings jetzt einmal. Der System-Environment-
Proof-Generator benennt ebenso seine stabilen Fallback-, Shell-, Apache- und
Markdown-Table-Literale einmal. Jede Verwendung behält denselben Stringwert;
keine generierte Datei wird per Hand editiert und weder Runtime-Command,
Executable, Candidate-Reihenfolge noch Security-Entscheidung ändern sich.

Dieser Batch bleibt absichtlich auf die 13 geprüften Keys begrenzt. Andere
Sonar-Befunde, einschließlich Vulnerability-Type-Observations und sprachstandard-
inkompatibler Common-C++-Vorschläge, bleiben getrennte Arbeit.

## Security-Auswirkung

Die geänderten Strings sind repository-kontrollierte Metadata und Labels. Die
Änderung verändert weder Untrusted-Input-Handling, Command-Construction, Path-
Normalisierung, Executable-Resolution, Autorisierung, Logging, Evidence-Gates,
Scanner-Konfiguration, Quality Gates, Suppressions noch NOSONAR-Marker. Der
System-Environment-Proof-Generator verwendet weiterhin den gleichen /bin/sh-
Wert und dieselben vorhandenen Executable-Checks. Durch diesen reinen
Maintainability-Batch wird kein Security-Finding als behoben beansprucht.

## Geänderte Dateien

- scripts/generate_connector_guides.py
- ci/evidence/reports/generate-system-environment-proof.py
- reports/audits/change-records/README.md und README.de.md
- dieses englische/deutsche Change-Record-Paar

## Ausgeführte Befehle

- Python-Kompilierung der zwei geänderten Module: bestanden.
- `tests.test_compiler_guides`: bestanden (19 Tests).
- Begrenzte System-Environment-Proof-Generierung mit `--skip-check-runs`:
  bestanden.
- `tests.test_bilingual_docs`: bestanden (11 Tests).
- Fokussierter Shell-Path-/Source-/Candidate-/PATH-Fallback-Invariant-Check:
  bestanden.
- `git diff --check`: bestanden.

## Tests und tatsächliche Ergebnisse

| Befehl oder Check | Ergebnis |
| --- | --- |
| rtk proxy -- env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-owned path> <selected-python> -m py_compile scripts/generate_connector_guides.py ci/evidence/reports/generate-system-environment-proof.py | bestanden. |
| rtk proxy -- env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-owned path> <selected-python> -m unittest -v tests.test_compiler_guides | bestanden: 19 Tests. |
| rtk proxy -- env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-owned path> <selected-python> ci/evidence/reports/generate-system-environment-proof.py --connector-root . --framework-root modules/ModSecurity-test-Framework --output-dir <task-owned path> --skip-check-runs | bestanden: einen temporären System-Environment-Proof-Report erzeugt, ohne die übersprungenen externen Checks auszuführen. |
| Source-Occurrence-Review | bestanden: jedes ausgewählte Literal bleibt einmal als Modulkonstante; unverbundene längere Note-Strings bleiben unverändert. |
| Fokussiertes Security-Extraction-Invariant | bestanden: vorhandener Shell-Pfad, Shell-Check-Source/-Candidate und das Missing-Tool-PATH-Fallback-Verhalten behalten ihre exakten Werte. |

Der Draft-PR [#88](https://github.com/Easton97-Jens/ModSecurity-conector/pull/88)
existiert jetzt für Branch `agent/sonar-s1192-ci-scripts-literals-20260722`.
Zum Erstellungszeitpunkt stimmten sein Head, der lokale Commit und der Remote-
Branch auf `dcf0d63f376c8935387643a15012e8828fd13d90` überein. Frische
Exact-Head-SonarQube-Cloud- und GitHub-Actions-Ergebnisse stehen noch aus und
werden nicht aus diesem Datensatz abgeleitet.

## Runtime-Evidence

Es änderte sich kein Connector-Runtime-Verhalten und es wird keines
beansprucht. Der Generatoraufruf ist ein begrenzter Parent-only-Funktionscheck
und keine Connector-Host-Runtime-Evidence.

## Nicht ausgeführte Prüfungen mit Begründung

- Keine vollständige Connector-Build- oder Host-/Runtime-Matrix: Weder
  Connector-Source noch Runtime-Harness-Verhalten änderten sich.
- Kein Framework- oder MRTS-Test und keine -Änderung: Sie sind aus diesem
  Parent-only-Task ausgeschlossen.
- Vollständige Hosted-Checks und SonarQube-Cloud-PR-Analyse stehen für den
  aktuellen exakten Draft-PR-Head noch aus.

## Bekannte Einschränkungen

Dieser Batch behandelt nur 13 ausgewählte python:S1192 Observations. Er
beansprucht weder, den größeren SonarQube-Cloud-Backlog zu leeren, noch nicht
verfügbare Runtime-Umgebungen zu validieren.

## Verbleibende Risiken

Ein versehentlicher Unterschied zwischen einer Konstante und einem früheren
Literal könnte generierten Text oder Reporting-Metadata beeinflussen. Die
fokussierte Compiler-Guide-Suite und der begrenzte Generatoraufruf reduzieren
dieses Risiko; frische Hosted-Exact-Head-Analyse bleibt vor verifizierter
Delivery erforderlich.

## Finaler Diff- und Review-Status

Lokale Implementierung und fokussierte Validierung sind auf dem Parent-only-
Task-Branch abgeschlossen. Draft-PR #88 ist offen und als Draft markiert;
sein initialer exakter Head wurde gegen lokale und Remote-Git-Metadaten
verifiziert. Hosted-Checks, Sonar-Analyse und Quality Gate stehen noch aus.
Es werden weder Review-Freigabe noch Merge oder Default-Branch-Änderung
beansprucht oder autorisiert.
