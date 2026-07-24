# Change Record: Parent-Adapter-Helper-expliziter Default-Case für SonarQube Cloud S131

**Sprache:** [English](CR-20260724-sonar-ci-adapter-helpers-default-case.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260724-sonar-ci-adapter-helpers-default-case |
| Datum (UTC) | 2026-07-24 |
| Basis-Revision | 30ee953b57f4aafebaa0e6ed565a80f6500db1de |
| Ursprüngliche Quellbasis | 5b8db00d44ab24f3a9f4216a00f7edee977b6898 |
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

- rtk proxy sh -n ci/checks/common/check-adapter-helpers.sh
- rtk proxy env FRAMEWORK_ROOT="$PWD" BUILD_ROOT="$PWD" sh ci/checks/common/check-adapter-helpers.sh
- rtk proxy rg <exakte leere Default-Arm-Inventur>
- rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_bilingual_docs
- rtk proxy make check-bilingual-docs
- rtk proxy make check-doc-links
- rtk proxy git diff --check origin/master...HEAD

## Tests und tatsächliche Ergebnisse

| Kommando oder Check | Ergebnis |
| --- | --- |
| Normaler Master-Update | bestanden: Der normale Update-Commit `151f409800a685aa41b92e3fc8fdb14e9db09f7b` führt den aktuellen Parent-`master` `30ee953b57f4aafebaa0e6ed565a80f6500db1de` zusammen; nur die gepaarten Change-Record-Indizes konfligierten und wurden manuell zusammengeführt. |
| Shell-Syntax nach dem Master-Update | bestanden. |
| Checkout-enthaltenes Build-Root-Control nach dem Master-Update | bestanden: Das Skript gibt die bestehende Zurückweisung aus und endet mit Exit 77 vor Framework-Metadatenzugriff. |
| Exakte Source-Inventur | bestanden: Genau ein leerer Default-Arm ist im ausgewählten case vorhanden. |
| Fokussierter Path-Control-Security-Review | bestanden: Der einzige Source-Delta ist ein leerer Default-Arm; Kanonisierung, Reject-Pattern/-Meldung, Exit 77 und spätere Kommandos sind unverändert. |
| Finaler Parent-Diff und Gitlink-Check | bestanden: Fünf Parent-Pfade unterscheiden sich vom aktuellen `master`; der Framework-Gitlink hat keinen finalen PR-Delta und wird nur über den normalen Master-Update-Parent geerbt. |
| git diff --check | bestanden: kein Whitespace-Fehler. |
| tests.test_bilingual_docs | bestanden: Das englisch/deutsche Paar und beide Indizes bleiben strukturell gültig. |
| make check-bilingual-docs | blocked_environment: Bestehende fehlende Framework-Gitlink-Linkziele verhindern den repository-weiten lokalen Check; Framework-Quellcode, Gitlink und generierte Artefakte wurden nicht geändert. |
| make check-doc-links | blocked_environment: Bestehende fehlende Framework-Gitlink-Linkziele verhindern den repository-weiten lokalen Check; Framework-Quellcode, Gitlink und generierte Artefakte wurden nicht geändert. |
| Hosted-Delivery-Checks | ausstehend: Das Update erzeugt einen neuen PR-Head; daher müssen Checks, SonarQube Cloud und Reviews erneut für diesen exakten Head beobachtet werden. |

## Runtime-Evidence

Es wird keine vollständige erfolgreiche Adapter-Helper-Skriptausführung
behauptet. Sie benötigt ausgeschlossene Framework-Adapter-Metadaten. Der
geänderte Arm läuft nur nach einem Non-Checkout-Root-Match und ist leer; das
direkte Checkout-enthaltene Negativ-Control deckt den betroffenen Policy-Branch
ab, ohne Framework/MRTS zu initialisieren, mocken oder verändern.

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
  Bot-Ergebnis und Review-Status müssen nach dem normalen Master-Update und
  dem Documentation-Reconciliation-Push aktualisiert werden; keine alte
  Draft-Evidenz wird für Merge-Eignung verwendet.

## Bekannte Einschränkungen

Dieser Batch korrigiert nur einen ausgewählten Parent-SonarQube-Cloud-Befund.
Er behauptet nicht, den breiteren SonarQube-Cloud-Backlog zu beheben.

## Verbleibende Risiken

Eine unbeabsichtigte Änderung des bestehenden Reject-Arms könnte das Build-
Root-Containment abschwächen. Der Einzeilen-No-op-Diff, das exakte Exit-77-
Negativ-Control, die Syntaxprüfung und die noch ausstehende Exact-Head-Hosted-
Validierung reduzieren dieses Risiko. Der Full-Success-Pfad bleibt nur durch
ausgeschlossene nicht verfügbare Framework-Metadaten blockiert.

## Finaler Diff- und Review-Status

Die anfängliche Source-Korrektur liegt im Parent-Commit
41f8ed308bf8acb4d6688dd8639944b5e3482957 von der ursprünglichen Quellbasis
5b8db00d44ab24f3a9f4216a00f7edee977b6898. Der normale Master-Update-Commit
151f409800a685aa41b92e3fc8fdb14e9db09f7b bringt den Branch auf den aktuellen
Parent-master `30ee953b57f4aafebaa0e6ed565a80f6500db1de`; er löst nur den
gepaarten Index-Reihenfolgekonflikt. Die historische Draft-Evidenz für den
alten Head `a0c78a5c87b3fc4a9af8e2759fa0fee9c5bd3034` bleibt als Historie
erhalten, ist aber nach diesem Update keine Merge-Evidenz. Draft PR
[#115](https://github.com/Easton97-Jens/ModSecurity-conector/pull/115) muss
erneut veröffentlicht und frisch verifiziert werden, bevor ein autorisierter
geschützter Merge möglich ist. Es gab kein Default-Branch-Update, keine
Framework-Action, keine MRTS-Action, keine Scanner-Control-Änderung und keine
Suppression.
