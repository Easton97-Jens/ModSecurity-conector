# Change Record: Parent-Runtime-Producer-Readiness-Assertion-Reihenfolge für SonarQube Cloud S3415

**Sprache:** [English](CR-20260723-sonar-tests-runtime-producer-readiness-assert-order.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260723-sonar-tests-runtime-producer-readiness-assert-order |
| Datum (UTC) | 2026-07-23 |
| Basis-Revision | a308d7b414f0859490fe7253e0683a4bde80b563 |
| Tracking | Fünf Parent-only-`python:S3415`-Code-Smells in `tests/test_runtime_producer_readiness_path_policy.py`: `AZ-KYVWWfYmbqbBXVNJa`, `AZ-KYVWWfYmbqbBXVNJb`, `AZ-KYVWWfYmbqbBXVNJc`, `AZ-KYVWWfYmbqbBXVNJd` und `AZ-KYVWWfYmbqbBXVNJe`. |
| Grenze | Parent-Test-Source sowie dieses englisch/deutsche Change-Record-Paar und die Indizes. Framework, MRTS, Gitlinks, Production-Source, Scanner-Konfiguration, Quality Gates, Suppressions und Runtime-Verhalten bleiben unverändert. |

## Motivation und Problemstellung

SonarQube Cloud meldet fünf `unittest.TestCase.assertEqual`-Aufrufe, deren
Expected- und Actual-Operanden vertauscht sind. Die Assertions drücken bereits
die beabsichtigten Path-Policy-Prädikate aus; das ausschließliche Vertauschen
ihrer ersten beiden Operanden richtet die Fehlerdiagnostik an der
Projektkonvention aus, ohne Vergleich oder Pass-/Fail-Ergebnis zu ändern.

## Entscheidung

Die Diagnose-Argumentreihenfolge von fünf bestehenden
`unittest.assertEqual`-Aufrufen in
`tests/test_runtime_producer_readiness_path_policy.py` korrigieren. SonarQube
Cloud identifiziert `AZ-KYVWWfYmbqbBXVNJa`, `AZ-KYVWWfYmbqbBXVNJb`,
`AZ-KYVWWfYmbqbBXVNJc`, `AZ-KYVWWfYmbqbBXVNJd` und
`AZ-KYVWWfYmbqbBXVNJe` als `python:S3415`: Actual Values müssen vor Expected
Values stehen, damit ein Fehler eine verwertbare Diagnose meldet.

## Scope und Non-Goals

Der Patch vertauscht nur die ersten zwei Positionsargumente der fünf
markierten Assertions. Er ändert keine Prädikate, erwarteten Statuswerte,
Path-Policy-Verhalten, Fixtures, gemockten Umgebungsdaten, Produktionscode,
Sicherheitskontrollen, Sonar-Konfiguration, Quality Gates, Framework, MRTS
oder Gitlinks.

Der Change Record und sein englisches Gegenstück sind die einzigen
Dokumentationsänderungen. Die gemeinsamen Indizes werden zur Traceability
aktualisiert. Kein Merge und kein Default-Branch-Write sind Teil dieses
Changes.

## Sicherheit und Kompatibilität

Dies ist eine reine Testdiagnosekorrektur. Der betroffene Test übt weiterhin
die bestehenden Source-Root- und System-Write-Path-Kontrollen aus; ihre
Implementierung oder Assertionsbedeutung wird nicht verändert. Dieser Delta
löst keinen Security-Workflow aus.

## Validierung und Delivery-Status

Vor dem Edit bestand das fokussierte Modul auf dem isolierten
Current-Master-Worktree mit allen vier Tests. Nach dem Change sind fokussierte
Test-, AST-, Syntax-, Diff-, bilinguale Dokumentations- und exakte
Draft-PR-Head-Verifikation erforderlich, bevor der Record ein verifiziertes
Delivery-Ergebnis behaupten kann.

### Aktuelles Parent-Master-Update — 2026-07-24

Der bestehende Draft-PR #104 bleibt das Delivery-Vehikel. Sein alter exakter
Head `a1f38b4cdc67b55214a67ecd53d25e45a1ae54e7` wurde ohne Rebase durch einen
normalen Merge von Parent-Master `90e3d8d9603375f9a33e2a51836ba284221fdd0f`
aktualisiert. Der resultierende lokale Merge-Commit
`6116d97a881a666e701ae6afa7671ff9f9fbfd53` löst nur die gemeinsamen
englischen und deutschen Change-Record-Indizes auf. Sein finaler
Current-Base-Diff bleibt dieser Parent-Test, dieses englisch/deutsche
Change-Record-Paar und diese Indizes; er enthält keine Framework-, MRTS-,
Gitlink-, Production-Source-, Scanner-, Gate-, Suppression- oder
Security-Control-Änderung. Das fokussierte Modul (4 Tests), die strukturelle
Fünf-Call-AST-Operandreihenfolge-Prüfung, die bilingualen Dokumentationstests
(11 Tests) und der Diff-Check bestanden auf diesem lokalen Merge-Head.

Hosted-Check- und SonarQube-Cloud-Ergebnisse werden nur über beobachtete
Exact-Head-PR-Delivery-Metadaten behauptet. Dieser Record erfindet sie nicht;
der Task-Flow aktualisiert diese externe Evidence für den aktuellen Remote-Head
vor jedem geschützten Merge.

## Akzeptanzkriterien

- Exakt die ersten zwei Operanden der fünf ausgewählten `assertEqual`-Aufrufe
  vertauschen.
- Prädikate, Fixtures, gemockte Umgebungsdaten, Expected-Statuswerte und jedes
  Path-Policy-Verhalten bewahren.
- Beide Change-Record-Sprachen und beide Indizes gleichwertig halten.
- Exact-Draft-PR-Head-SonarQube-Cloud- und Hosted-Check-Evidence einholen,
  bevor ein ausgewählter Key als behoben gilt.

## Implementierungsentscheidung und Begründung

Jede ausgewählte Assertion liefert jetzt den beobachteten Statuswert aus dem
Mapping zuerst und ihren festen Expected-Status danach. Kein Prädikat, Fixture,
Testdaten, Produktionscode, Path-Resolver, Security-Check oder optionales
Assertion-Argument wurde verändert.

## Geänderte Dateien

- tests/test_runtime_producer_readiness_path_policy.py
- reports/audits/change-records/README.md und README.de.md
- dieses englische/deutsche Change-Record-Paar

## Ausgeführte Befehle

- Fokussierter Test des betroffenen Moduls vor und nach dem Edit: bestanden
  (4 Tests).
- AST-Operand-Reihenfolge- und In-Memory-Syntax-Validierung: bestanden
  (5 ausgewählte Aufrufe).
- `tests.test_bilingual_docs`: bestanden (11 Tests).
- `git diff --check`: bestanden.
- Aktuelles Parent-Master-Update und Konfliktauflösung: bestanden; normaler
  nicht-rewritender Merge `6116d97a881a666e701ae6afa7671ff9f9fbfd53` löst nur
  die beiden Change-Record-Indizes auf.
- Aktueller gemergter Tree: fokussiertes Modul (4 Tests), strukturelle
  Fünf-Call-AST-Operandreihenfolge-Prüfung, bilinguale Dokumentationstests
  (11 Tests) und Diff-Check: bestanden.
- Vollständige Dokumentations-/Link-Checks: Der reparierte Change Record hat
  keinen gemeldeten record-spezifischen Verstoß; beide Kommandos sind nur durch
  bestehende fehlende Framework-Gitlink-Targets außerhalb dieses Tasks blockiert.

## Security-Auswirkung

Dies ist eine reine Testdiagnosekorrektur. Das betroffene Modul prüft weiterhin
Source-Root- und System-Write-Path-Kontrollen; weder ihre Implementierung noch
ihre Assertionsbedeutung ändern sich. Es wird kein Security-Workflow ausgelöst
und kein Security-Finding als behoben beansprucht.

## Runtime-Evidence

Es änderte sich kein Connector-Runtime-Verhalten und es wird keines
beansprucht. Der betroffene Test verwendet gemockte Umgebungsdaten und
temporäre Testpfade; er ist weder ein Production-Host-Runtime-Deployment noch
ein Framework-/MRTS-Lauf.

## Bekannte Einschränkungen

Dieser Batch behandelt nur fünf ausgewählte `python:S3415`-Observations. Er
beansprucht weder, den größeren SonarQube-Cloud-Backlog zu leeren, noch nicht
verfügbare Runtime-Umgebungen zu validieren.

## Verbleibende Risiken

Ein versehentlicher Operandentausch außerhalb einer ausgewählten Assertion
könnte Fehlerdiagnostik irreführend machen. Der exakte AST-Vergleich der fünf
Aufrufe und der Test des betroffenen Moduls reduzieren dieses Risiko; frische
Hosted-Exact-Head-Analyse bleibt vor verifizierter Delivery erforderlich.

## Nicht ausgeführte Prüfungen mit Begründung

- Keine vollständige Connector-Build- oder Host-/Runtime-Matrix: Der Delta
  ändert nur Testdiagnose-Argumentreihenfolge und das vollständige betroffene
  Modul besteht.
- Kein Framework- oder MRTS-Test und keine -Änderung: beide sind aus diesem
  Parent-only-Task ausgeschlossen.
- Vollständige Hosted-Checks und SonarQube-Cloud-PR-Analyse sind externe
  Delivery-Evidence: Nur ein beobachteter aktueller exakter Remote-Head kann
  diese Anforderung vor dem geschützten Merge erfüllen.

## Finaler Diff- und Review-Status

Der bestehende Parent-only-PR #104 ist das Delivery-Vehikel. Sein task-eigener
Branch enthält den normalen Current-Master-Update-Merge
`6116d97a881a666e701ae6afa7671ff9f9fbfd53` und die paarige Delivery-Evidence-
Dokumentation. Dieser Record beansprucht weder Review-Freigabe noch Merge oder
Default-Branch-Änderung. Vor dem geschützten Merge muss der PR non-draft sein,
sein aktueller exakter Remote-Head bestehende Hosted-Checks und Sonar-Analyse
haben und der Review-Status frisch sein; diese beobachteten Fakten gehören in
Delivery-Metadaten statt in eine unbeobachtete Behauptung dieses Records.
