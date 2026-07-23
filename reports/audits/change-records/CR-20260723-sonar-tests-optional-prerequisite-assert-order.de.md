# Change Record: Optional-Prerequisite-Assert-Diagnostikreihenfolge für SonarQube Cloud

**Sprache:** [English](CR-20260723-sonar-tests-optional-prerequisite-assert-order.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260723-sonar-tests-optional-prerequisite-assert-order |
| Datum (UTC) | 2026-07-23 |
| Basis-Revision | a308d7b414f0859490fe7253e0683a4bde80b563 |
| Tracking | FND-SONAR-0020; 77 aktuelle python:S3415-Befunde in tests/test_optional_prerequisite_status.py, von AZ-KYVRgfYmbqbBXVND6 bis AZ-KYVRgfYmbqbBXVNFG. |
| Grenze | Parent-Test-Source, dieses englisch/deutsche Change-Record-Paar und seine Indizes. Framework, MRTS, Gitlinks, Runtime-Product-Code, Scanner-Konfiguration, Quality Gates, Suppressions, Exclusions, Issue-Status und Default-Branch bleiben unverändert. |

## Motivation und Problemstellung

Die 77 Gleichheits- und Ungleichheitsassertions im Optional-Prerequisite-Status-
Test stellten einen festen Expected-Operand vor den beobachteten Operand. Die
Prädikate waren korrekt, aber ihre Fehlerdiagnostik folgte nicht der
Actual-before-Expected-Konvention des Repositorys.

Die aktuelle offizielle Abfrage identifiziert 73 assertEqual- und vier
assertNotEqual-Aufrufe in dieser exakten Parent-Datei. Dies ist nur eine
Maintainability-Remediation; sie ändert weder Optional-Prerequisite-
Klassifikation, Statusfile-Verhalten, Apache-Preflight noch Runtime-Ausführung.

## Akzeptanzkriterien

- Alle 77 ausgewählten Assertion-Sites stellen beobachtete Actual-Werte zuerst
  und feste Expected-Werte an zweiter Stelle dar.
- Assertions-Methode, Prädikat, Zeilenzuordnung und jedes optionale dritte
  Diagnoseargument bleiben unverändert.
- Das vollständige betroffene Testmodul behält seine Valid-, Blocked-, Failed-,
  Symlink- und Status-Channel-Controls.
- Keine Rule, kein Quality Gate, keine Exclusion, Suppression, kein NOSONAR
  und kein Issue-Status werden geändert.
- Frische Exact-Head-SonarQube-Cloud- und Hosted-Check-Evidence ist
  erforderlich, bevor die Befunde auf einem ungemergten Draft PR als
  verifiziert gelten.

## Implementierungsentscheidung und Begründung

Nur die ersten zwei Operanden der 77 vorhandenen unittest-Assertions werden
vertauscht. Gleichheits- und Ungleichheitswahrheitswerte bleiben erhalten, weil
die Relationen symmetrisch sind, während ein Fehler nun den beobachteten Wert
in der konventionellen ersten Position meldet.

Kein Helper, Status-Runner-Befehl, Fixture, Subprocess-Aufruf, Status-JSON-Feld
oder Assertion-Message wird refaktoriert oder entfernt. Das AST-Mapping von
Base zu Kandidat erfasst alle 77 Sites: 73 assertEqual und vier assertNotEqual,
ohne nicht ausgewählten Gleichheits- oder Ungleichheitsassertion-Aufruf in der
Datei.

## Geänderte Dateien

- tests/test_optional_prerequisite_status.py
- reports/audits/change-records/README.md und README.de.md
- dieses englisch/deutsche Change-Record-Paar

## Security-Auswirkung

Diese Änderung ist als Runtime-Security-Modifikation nicht anwendbar: Sie
ändert nur die Diagnoseoperand-Reihenfolge von Tests. Sie lässt Runtime-Root-,
Symlink-, Status-Channel-, Optional-Prerequisite- und Blocked-Result-Controls
des Status-Writers unverändert. Kein Security- oder Scanner-Control wird
geschwächt.

## Ausgeführte Befehle

- Fokussiertes tests.test_optional_prerequisite_status: alle 20 Tests
  bestanden vor und nach der Operand-Reihenfolgekorrektur.
- In-Memory-AST-Mapping von Base zu Kandidat: alle 77 ausgewählten Aufrufe
  bestanden die Method-, Operand-Swap-, Assertion-Shape- und Optional-Message-
  Checks.
- git diff --check: für den Source-only-Kandidaten vor dem Hinzufügen dieses
  Record-Paars bestanden.

## Runtime-Evidence

Das fokussierte Modul nutzt seine vorhandenen synthetischen Dependent-Check-
Fixtures für Erfolg, erlaubte und nicht erlaubte Blocked-Zustände,
Statuspersistenz, Symlink-Ablehnung und Same-User-Path-Swap-Schutz. Diese
Controls sind unverändert; keine Live-Apache-, Framework-, MRTS- oder
Connector-Runtime wird beansprucht.

## Validierungsstatus

Das betroffene Modul bestand alle 20 Tests vor und nach der Korrektur. Das
Source-Mapping beweist, dass jeder ausgewählte Sonar-Site nur seine ersten zwei
Operanden vertauscht und ein drittes Diagnoseargument erhalten bleibt.
Gezielte bilinguale Dokumentation, finaler Scoped-Diff und Exact-Head-
Delivery-Evidence bleiben erforderlich, nachdem dieser Record in den Draft-PR-
Kandidaten aufgenommen ist.

## Bekannte Einschränkungen und Follow-up

Dieser Record verifiziert nur die 77 aktuellen Parent-S3415-Befunde in der
benannten Testdatei. Er beansprucht nicht, dass die projektweite 1.474-Item-
Inventur oder andere Test-, CI-, Common-, Scripts- oder Connector-Befunde
behoben sind.

## Verbleibende Risiken

Das Testverhalten bleibt absichtlich unverändert. Das verbleibende Delivery-
Risiko ist extern: Die Source muss noch eine frische SonarQube-Cloud-Analyse
und Hosted-Checks auf dem exakten ungemergten Draft-PR-Head bestehen.

## Nicht ausgeführte Prüfungen mit Begründung

- Kein Framework- oder MRTS-Test und keine -Änderung: Beide liegen außerhalb
  dieses Parent-only-Batches.
- Keine Live-Apache- oder Full-Connector-Runtime: Die reine Assertion-
  Reihenfolgeänderung ist durch das vollständige direkte Testmodul abgedeckt.
- Hosted-Checks und Exact-Head-SonarQube-Cloud-Analyse: erst verfügbar, wenn
  der Branch committed, gepusht und als ungemergter Draft PR geöffnet ist.

## Delivery-Status

Der Kandidat ist auf einem isolierten Parent-Task-Branch basierend auf der
festgehaltenen Master-Revision vorbereitet. Er darf nach finaler lokaler
Validierung nur als ungemergter Draft PR committed, gepusht und geöffnet
werden. Kein Merge, Default-Branch-Update, Rebase, Force-Push oder Framework-/
MRTS-Change ist autorisiert.

## Finaler Diff- und Review-Status

Der Source-only-Diff enthält 77 Operand-Pair-Swaps und keine Verhaltensänderung
der Testlogik. Finale Dokumentationsvalidierung, Staged-Diff-Review und frische
Exact-Head-Delivery-Evidence stehen aus; dieser Record behauptet keinen
vorzeitigen Quality-Gate- oder PR-Status.
