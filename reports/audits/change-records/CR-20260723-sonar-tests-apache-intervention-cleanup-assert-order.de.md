# Change Record: Parent-Apache-Intervention-Cleanup-Assertion-Reihenfolge für SonarQube Cloud S3415

**Sprache:** [English](CR-20260723-sonar-tests-apache-intervention-cleanup-assert-order.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260723-sonar-tests-apache-intervention-cleanup-assert-order |
| Datum (UTC) | 2026-07-23 |
| Basis-Revision | a308d7b414f0859490fe7253e0683a4bde80b563 |
| Tracking | Zwei Parent-only-`python:S3415`-Code-Smells in `tests/test_apache_intervention_cleanup.py`: `AZ-KYVR8fYmbqbBXVNFO` und `AZ-KYVR8fYmbqbBXVNFP`. |
| Grenze | Parent-Test-Source sowie dieses englisch/deutsche Change-Record-Paar und die Indizes. Framework, MRTS, Gitlinks, Apache-Production-Source, Scanner-Konfiguration, Quality Gates, Suppressions und Runtime-Verhalten bleiben unverändert. |

## Motivation und Problemstellung

SonarQube Cloud meldet zwei `unittest.TestCase.assertEqual`-Aufrufe, deren
Expected- und beobachtete Operanden vertauscht sind. Die Assertions kodieren
bereits die Apache-Intervention-Cleanup-Invarianten; das ausschließliche
Vertauschen ihrer ersten beiden Operanden richtet die Fehlerdiagnostik an der
Projektkonvention aus, ohne Vergleich oder Pass-/Fail-Ergebnis zu ändern.

## Entscheidung

Die Diagnose-Argumentreihenfolge der zwei bestehenden
`unittest.TestCase.assertEqual`-Aufrufe in
`tests/test_apache_intervention_cleanup.py` korrigieren. SonarQube Cloud
identifiziert `AZ-KYVR8fYmbqbBXVNFO` und `AZ-KYVR8fYmbqbBXVNFP` als
`python:S3415`: Der beobachtete Wert muss vor dem festen Expected-Wert stehen,
damit ein Fehler eine verwertbare Diagnose meldet.

## Scope und Non-Goals

Der Patch vertauscht nur die ersten zwei Positionsargumente der zwei
markierten Assertions. Er ändert nicht die geprüfte C-Source, Prädikate,
Expected-Werte, Fixtures, Testdaten, Apache-Verhalten, Cleanup-Ownership,
Sicherheitskontrollen, Sonar-Konfiguration, Quality Gates, Framework, MRTS
oder Gitlinks.

Der Change Record und sein deutsches Gegenstück sind die einzigen
Dokumentationsänderungen. Die gemeinsamen Indizes werden zur Traceability
aktualisiert. Kein Merge und kein Default-Branch-Write sind Teil dieses
Changes.

## Sicherheit und Kompatibilität

Dies ist eine reine Testdiagnosekorrektur. Der Test übt weiterhin den
bestehenden Cleanup-Ownership-Vertrag in der Apache-Source aus; er ändert weder
die C-Implementierung noch die Assertionsbedeutung. Dieser Delta löst keinen
Security-Workflow aus.

## Validierung und Delivery-Status

Vor und nach dem Edit bestand `make check-apache-intervention-cleanup` auf dem
isolierten Current-Master-Worktree mit allen fünf Testfällen. Eine
AST-Operandreihenfolge-Prüfung bestätigte außerdem, dass nur die zwei
ausgewählten Aufrufe jetzt Actual- und danach Expected-Werte liefern. Der
gezielte bilinguale Dokumentationstest und der Scoped-Diff-Check bestanden.
Die vollständigen Dokumentationskommandos sind ausschließlich durch
vorbestehende fehlende Framework-Gitlink-Targets blockiert und meldeten keinen
task-eigenen Change-Record-Fehler. Die exakte Draft-PR-Head-Verifikation bleibt
erforderlich, bevor dieser Record ein verifiziertes Delivery-Ergebnis
beanspruchen kann.

Die beabsichtigte Delivery ist ein separater ungemergter Draft PR. Hosted-
Check- und SonarQube-Cloud-Ergebnisse werden in diesem Record erst nach
Beobachtung für seinen exakten gepushten Head beansprucht.

## Akzeptanzkriterien

- Exakt die ersten zwei Operanden der zwei ausgewählten `assertEqual`-Aufrufe
  vertauschen.
- Apache-Cleanup-Prädikate, Expected-Werte, C-Source, Fixtures und jedes
  Testverhalten bewahren.
- Beide Change-Record-Sprachen und beide Indizes gleichwertig halten.
- Exact-Draft-PR-Head-SonarQube-Cloud- und Hosted-Check-Evidence einholen,
  bevor einer der ausgewählten Keys als behoben gilt.

## Implementierungsentscheidung und Begründung

Jede ausgewählte Assertion liefert jetzt ihren beobachteten Ausdruck zuerst
und ihr festes Expected-Literal oder ihre Expected-Liste danach. Kein
Prädikat, Fixture, Source-Text, Security-Control oder optionales
Assertion-Argument wurde geändert.

## Geänderte Dateien

- tests/test_apache_intervention_cleanup.py
- reports/audits/change-records/README.md und README.de.md
- dieses englische/deutsche Change-Record-Paar

## Ausgeführte Befehle

- Fokussierter Test des betroffenen Moduls vor und nach dem Edit: bestanden
  (5 Tests).
- AST-Operandreihenfolge-Validierung: bestanden (2 ausgewählte Aufrufe).
- `tests.test_bilingual_docs`: bestanden (11 Tests).
- `git diff --check`: bestanden.
- Vollständige Dokumentations-/Link-Checks: nur durch bekannte fehlende
  Framework-Gitlink-Targets blockiert; kein task-eigener Change-Record-Fehler
  wurde gemeldet.
- Vollständige Draft-PR-Hosted-/SonarQube-Cloud-Analyse: ausstehend, weil noch
  kein Draft PR existiert.

## Security-Auswirkung

Dies ist eine reine Testdiagnosekorrektur. Das Modul prüft weiterhin
Cleanup-Ownership nach einer nativen Apache-Intervention; weder die
C-Implementierung noch die logische Assertionsbedeutung ändert sich. Es wird
kein Security-Finding als behoben beansprucht.

## Runtime-Evidence

Es änderte sich kein Connector-Runtime-Verhalten und es wird keines
beansprucht. Der betroffene Test liest den kontrollierten Parent-Apache-
Source-Vertrag; er ist weder ein Production-Host-Runtime-Deployment noch ein
Framework-/MRTS-Lauf.

## Bekannte Einschränkungen

Dieser Batch behandelt nur zwei ausgewählte `python:S3415`-Observations. Er
beansprucht weder, den breiteren SonarQube-Cloud-Backlog zu leeren, noch eine
Apache-Host-Build-/Runtime-Umgebung zu validieren.

## Verbleibende Risiken

Ein versehentlicher Operandentausch außerhalb einer ausgewählten Assertion
könnte Fehlerdiagnostik irreführend machen. Der Zwei-Aufruf-AST-Vergleich, der
Scoped Diff und das vollständige betroffene Modul reduzieren dieses Risiko;
frische Hosted-Exact-Head-Analyse bleibt vor verifizierter Delivery
erforderlich.

## Nicht ausgeführte Prüfungen mit Begründung

- Kein vollständiger Apache-Build und keine Connector-/Runtime-Matrix: Der
  Delta ändert nur Testdiagnose-Argumentreihenfolge und das vollständige
  betroffene Modul besteht.
- Kein Framework- oder MRTS-Test und keine -Änderung: beide sind aus diesem
  Parent-only-Task ausgeschlossen.
- Vollständige Hosted-Checks und SonarQube-Cloud-PR-Analyse: es existiert noch
  kein Draft PR.

## Finaler Diff- und Review-Status

Lokale Implementierung und fokussierte Validierung sind auf dem Parent-only-
Task-Branch abgeschlossen. Hosted-Checks, Sonar-Analyse und Quality Gate
bleiben ausstehend, bis der separate ungemergte Draft PR gepusht ist. Es
werden weder Review-Freigabe, Merge noch Default-Branch-Änderung beansprucht
oder autorisiert.
