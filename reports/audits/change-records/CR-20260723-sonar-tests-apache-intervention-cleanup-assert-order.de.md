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

Der aktuelle Parent-only-Integrationsbranch wurde nach seinem normalen,
nicht umschreibenden Update vom aktuellen Parent-master geprüft. Das
fokussierte Modul bestand fünf Tests erfolgreich, und eine AST-Prüfung
bestätigte, dass exakt die zwei ausgewählten `assertEqual`-Aufrufe den
beobachteten Ausdruck vor dem festen Expected-Wert platzieren.

### Aktuelle Parent-master-Aktualisierung — 2026-07-24

Der bestehende Draft PR #105 bleibt das Delivery-Vehikel. Sein vorheriger
Remote-Head `60b8254e45b00ddbac556ff78cd0af3490e26ff2` wurde ohne Rebase durch
das Mergen von Parent-master
`053a9ca5b0f9351319c96d359107c53ba8f9d3a1` normal aktualisiert. Der
resultierende lokale Merge-Commit
`709493f9b219db246701a8023ed853e86a3026e7` löst ausschließlich die
gemeinsamen englischen und deutschen Change-Record-Indizes auf. Er ändert
weder Framework noch MRTS, sondern übernimmt lediglich bestehende
Master-Historie. Der aktuelle PR-Base-Diff bleibt bei diesem Parent-Test,
diesem englisch/deutschen Change-Record-Paar und den Indizes, ohne von diesem
PR-Update verfasste Framework-, MRTS-, Gitlink-, Production-Source-, Scanner-,
Gate-, Suppression- oder Security-Control-Änderung.

Hosted-Check-, SonarQube-Cloud-, Quality-Gate-, Review-, Ready- und
Merge-Ergebnisse werden nur durch beobachtete Exact-Head-PR-Delivery-Metadaten
beansprucht. Dieser Record überträgt weder Ergebnisse eines alten Heads auf den
neuen Head noch erfindet er ein späteres Delivery-Ergebnis.

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

- Aktueller fokussierter Test des betroffenen Moduls im gemergten Baum:
  bestanden (5 Tests).
- Aktuelle AST-Operandreihenfolge-Validierung im gemergten Baum: bestanden
  (2 ausgewählte Aufrufe).
- Aktuelles Parent-master-Update und Konfliktauflösung: bestanden; normaler,
  nicht umschreibender Merge `709493f9b219db246701a8023ed853e86a3026e7` löst
  ausschließlich die gepaarten Change-Record-Indizes auf.
- Gezielter bilingualer Dokumentationstest: bestanden (11 Tests).
- Scoped `git diff --check`: bestanden.

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
- Hosted-Checks und SonarQube-Cloud-PR-Analyse sind externe Delivery-Evidence:
  nur ein beobachteter aktueller Exact-Remote-Head kann diese Anforderung vor
  einem geschützten Merge erfüllen.

## Finaler Diff- und Review-Status

Der bestehende Parent-only-PR #105 ist das Delivery-Vehikel. Sein task-eigener
Branch enthält den normalen Current-Master-Update-Merge
`709493f9b219db246701a8023ed853e86a3026e7` sowie gepaarte
Delivery-Evidence-Dokumentation. Dieser Record beansprucht weder
Review-Freigabe noch Merge oder Default-Branch-Änderung. Vor einem geschützten
Merge muss der PR nicht mehr Draft sein und sein aktueller Exact-Remote-Head
muss bestehende Hosted-Checks und SonarQube-Cloud-Analyse sowie einen
aktualisierten Review-Status aufweisen; diese beobachteten Fakten gehören zu
Delivery-Metadaten und nicht zu einer unbeobachteten Behauptung in diesem
Record.
