# Change Record: Parent-Adapter-Helper-expliziter Default-Case für SonarQube Cloud S131

**Sprache:** [English](CR-20260724-sonar-ci-adapter-helpers-default-case.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260724-sonar-ci-adapter-helpers-default-case |
| Datum (UTC) | 2026-07-24 |
| Basis-Revision | 5b8db00d44ab24f3a9f4216a00f7edee977b6898 |
| Tracking | Parent-SonarQube-Cloud-shelldre:S131-Code-Smell AZ422z_PmJyaFL6eWoJF an Zeile 23. |
| Grenze | Parent-CI-Shell-Source sowie dieses englisch/deutsche Traceability-Paar und die Indizes. Build-Root-Policy, Framework, MRTS, Gitlinks, Scanner-Konfiguration, Quality Gates, Suppressions, generierte Artefakte und Runtime-Verhalten bleiben unverändert. |

## Motivation und Problemstellung

Die ausgewählte SonarQube-Cloud-Zeile markiert einen kanonisierten
BUILD_ROOT-case, der Checkout-enthaltene Roots zurückweist, aber keinen
expliziten Default-Arm hat. Ein nicht passender Shell-case läuft bereits zur
späteren Validierung weiter; die Darstellung dieser Absicht mit einem leeren
Default-Arm behebt die Maintainability-Beobachtung, ohne erlaubte oder
zurückgewiesene Roots zu ändern.

## Akzeptanzkriterien

- Nur einen expliziten leeren Default-Arm zum ausgewählten case hinzufügen.
- Kanonisierung, Checkout-Root-Pattern, Reject-Meldung, Exit 77 und jedes
  spätere Kommando bytegenau bewahren.
- Shell-Syntax bestehen und beweisen, dass das Checkout-enthaltene Build-Root-
  Control weiterhin mit erwartetem Exit 77 vor Framework-Metadatenzugriff
  zurückweist.
- Synchronisierte englisch/deutsche Change Records und Indizes pflegen.
- Exact-Head-GitHub- und SonarQube-Cloud-Draft-PR-Evidenz einholen, bevor der
  ausgewählte Key als verifiziert beschrieben wird.

## Implementierungsentscheidung und Begründung

Der ausgewählte case hat jetzt nach dem bestehenden Checkout-Root-Reject-Arm
einen expliziten leeren Default-Arm. Er ist ein Shell-semantischer No-op:
Nicht passende Roots fielen bereits zur späteren bestehenden Validierung
weiter. Es wird kein Pfad neu akzeptiert, keine Zurückweisung entfernt und
kein Kommando, keine Variable, keine Compiler-Invocation oder Framework-
Metadata-Route verändert.

## Security-Auswirkung

Dies ist kein Sicherheitsbefund, aber der geänderte case schützt eine
Build-Root-Pfadgrenze. Die fokussierte Sicherheitsbewertung verlangt daher
No-Regression-Evidenz statt einer breiten Sicherheitsbehauptung. Das direkte
Pre-/Post-Negativ-Control bestätigt, dass ein kanonischer Build-Root im
Parent-Checkout weiter dieselbe Zurückweisung ausgibt und mit Exit 77 vor
jedem Framework-Metadatenzugriff endet. Es wird kein Security-Control
abgeschwächt und kein Sicherheitsbefund als behoben behauptet.

## Geänderte Dateien

- ci/checks/common/check-adapter-helpers.sh
- reports/audits/change-records/README.md und README.de.md
- dieses englisch/deutsche Change-Record-Paar

## Ausgeführte Befehle

- rtk proxy -- sh -n ci/checks/common/check-adapter-helpers.sh
- rtk proxy -- sh -c <Checkout-enthaltenes BUILD_ROOT-Exit-77-Control>
- rtk proxy -- rg <exakte leere Default-Arm-Inventur>
- rtk proxy -- shellcheck ci/checks/common/check-adapter-helpers.sh
- rtk proxy -- git diff --check

## Tests und tatsächliche Ergebnisse

| Kommando oder Check | Ergebnis |
| --- | --- |
| Offizieller aktueller Key und alle Open-PR-Selected-Path-Overlap-Abfragen | bestanden: Der eine Parent-Key ist auf der dokumentierten Basis OPEN und keiner der 20 offenen PRs ändert die ausgewählte Datei. |
| Shell-Syntax vor und nach der Änderung | bestanden. |
| Checkout-enthaltenes Build-Root-Control vor und nach der Änderung | bestanden: Das Skript gibt die bestehende Zurückweisung aus und liefert erwarteten Exit 77 vor Framework-Metadatenzugriff. |
| Exakte Source-Inventur | bestanden: Genau ein leerer Default-Arm ist im ausgewählten case vorhanden. |
| Fokussierter Path-Control-Security-Review | bestanden: Der einzige Source-Delta ist ein leerer Default-Arm; Kanonisierung, Reject-Pattern/-Meldung, Exit 77 und spätere Kommandos sind unverändert. |
| git diff --check | bestanden: kein Whitespace-Fehler. |
| Bytecode-Scan des aktuellen Batch-Worktrees | bestanden: keine Python-Bytecode-Datei. |
| ShellCheck | baseline-äquivalentes Warning-Ergebnis: SC1007 an bestehenden Kanonisierungszeilen 4 und 23 vor und nach der Änderung; der neue Default-Arm erzeugt keine Warnung. Diese bestehenden Warnings liegen außerhalb dieses Ein-Key-Batches und werden nicht unterdrückt. |
| tests.test_bilingual_docs und direkter Change-Record-/Index-Paritätscheck | bestanden: 11 Tests; beide Change Records haben 13 Level-two-Abschnitte sowie passende Change-ID-, Basis-Revision-, Key- und Affected-Path-Literale. |
| make check-bilingual-docs | blocked_environment: Genau 20 vorhandene fehlende Framework-Gitlink-Linkziele; kein neuer Change-Record-Fehler. |
| make check-doc-links | blocked_environment: Genau 16 vorhandene fehlende Framework-Gitlink-Linkziele; es wurde kein Framework-Quellcode, Gitlink oder generiertes Artefakt geändert. |
| Hosted-Delivery-Checks | ausstehend: Es gibt noch keinen Draft PR. |

## Runtime-Evidence

Es wird keine vollständige erfolgreiche Adapter-Helper-Skriptausführung
behauptet. Sie benötigt ausgeschlossene Framework-Adapter-Metadaten. Der
geänderte Arm läuft nur nach einem Non-Checkout-Root-Match und ist leer; die
direkte Pre-/Post-Evidenz deckt den betroffenen Checkout-Root-Policy-Branch ab,
ohne Framework/MRTS zu initialisieren, mocken oder verändern.

## Nicht ausgeführte Prüfungen mit Begründung

- Die vollständige erfolgreiche Skriptausführung ist durch ausgeschlossene
  nicht verfügbare Framework-Metadaten blocked_environment. Kein Framework-/
  MRTS-Workaround ist autorisiert.
- Connector-Builds, Konfigurationsprüfungen, Host-Runtime-Smoke-Tests,
  Protokollmatrizen und MRTS-Checks sind nicht anwendbar, weil keine
  Connector-/Runtime-Implementierung oder Framework-/MRTS-Content geändert
  wurde.
- Ruff und Pyright sind nicht anwendbar, weil diese Shell-only-Änderung keinen
  konfigurierten Parent-Pfad und kein installiertes Executable hat; es wird
  keine Abhängigkeit installiert.
- Exact-Head-GitHub-Checks, SonarQube-Cloud-Quality-Gate, PR-Issue-Abfrage,
  Bot-Ergebnis und Review-Status warten auf einen künftigen offenen Draft PR
  und werden nicht behauptet.

## Bekannte Einschränkungen

Dieser Batch korrigiert nur einen ausgewählten Parent-SonarQube-Cloud-Befund.
Er behauptet nicht, den breiteren SonarQube-Cloud-Backlog mit 1.474 Befunden
zu beheben.

## Verbleibende Risiken

Eine unbeabsichtigte Änderung des bestehenden Reject-Arms könnte das Build-
Root-Containment abschwächen. Der Einzeilen-No-op-Diff, das exakte Exit-77-
Negativ-Control, die Syntaxprüfung und die noch ausstehende Exact-Head-Hosted-
Validierung reduzieren dieses Risiko. Der Full-Success-Pfad bleibt nur durch
ausgeschlossene nicht verfügbare Framework-Metadaten blockiert.

## Finaler Diff- und Review-Status

Die Source-Korrektur und das anfängliche englisch/deutsche Traceability-
Material liegen im atomaren Parent-Commit
41f8ed308bf8acb4d6688dd8639944b5e3482957 auf Task-Branch
codex/sonar-ci-adapter-helpers-default-case-20260724-master-5b8db00 von Basis
5b8db00d44ab24f3a9f4216a00f7edee977b6898. Er ist lokal sauber und besteht
branch-weite Diff-Hygiene. Normaler Push, offene Draft-PR-Erstellung und
finale Exact-Head-GitHub-/Sonar-/Review-Beobachtung stehen aus. Es gab keinen
Merge, kein Default-Branch-Update, keine Framework-Action, keine MRTS-Action,
keine Scanner-Control-Änderung und keine Suppression. Finale Delivery-Fakten
werden erst nach Beobachtung ergänzt.
