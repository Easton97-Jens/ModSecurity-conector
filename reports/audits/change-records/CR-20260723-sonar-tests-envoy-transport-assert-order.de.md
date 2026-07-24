# Change Record: Parent-Envoy-Transport-Assert-Reihenfolge für SonarQube Cloud S3415

**Sprache:** [English](CR-20260723-sonar-tests-envoy-transport-assert-order.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260723-sonar-tests-envoy-transport-assert-order |
| Datum (UTC) | 2026-07-23 |
| Basis-Revision | 5b8db00d44ab24f3a9f4216a00f7edee977b6898 |
| Tracking | Neunzehn Parent-only `python:S3415` Code Smells in `tests/test_envoy_transport_hardening_contract.py`. |
| Grenze | Parent-Test-Source sowie dieses englisch/deutsche Traceability-Paar und die Indizes. Framework, MRTS, Gitlinks, Envoy-Runtime-/Helper-Source, Scanner-Konfiguration, Quality Gates, Suppressions und Runtime-Verhalten bleiben unverändert. |

## Motivation und Problemstellung

SonarQube Cloud meldet bestehende `unittest.TestCase.assertEqual`-Aufrufe,
deren Expected- und Actual-Operanden vertauscht sind. Die Assertions drücken
bereits die beabsichtigten Prädikate aus; das ausschließliche Vertauschen ihrer
ersten zwei Top-Level-Operanden richtet die Fehlerdiagnostik an der
Projektkonvention aus, ohne Equality-Vergleich oder Pass-/Fail-Ergebnis zu
ändern.

Die ausgewählten aktuellen Keys sind `AZ-KYVTIfYmbqbBXVNFo`,
`AZ-KYVTIfYmbqbBXVNFp`, `AZ-KYVTIfYmbqbBXVNFq`,
`AZ-KYVTIfYmbqbBXVNFr`, `AZ-KYVTIfYmbqbBXVNFs`,
`AZ-KYVTIfYmbqbBXVNFt`, `AZ-KYVTIfYmbqbBXVNFu`,
`AZ-KYVTIfYmbqbBXVNFv`, `AZ-KYVTIfYmbqbBXVNFw`,
`AZ-KYVTIfYmbqbBXVNFx`, `AZ-KYVTIfYmbqbBXVNFy`,
`AZ-KYVTIfYmbqbBXVNFz`, `AZ-KYVTIfYmbqbBXVNF0`,
`AZ-KYVTIfYmbqbBXVNF1`, `AZ-KYVTIfYmbqbBXVNF2`,
`AZ-KYVTIfYmbqbBXVNF3`, `AZ-KYVTIfYmbqbBXVNF4`,
`AZ-KYVTIfYmbqbBXVNF5` und `AZ-KYVTIfYmbqbBXVNF6`.

## Akzeptanzkriterien

- Exakt die ersten zwei Operanden der 19 ausgewählten `assertEqual`-Aufrufe
  vertauschen.
- Alle Assertion-Operand-Ausdrücke, Prädikate, Fixture-Verhalten,
  kontrollierten Loopback-Interaktionen, Testeingaben und Expected-Werte
  bewahren.
- Das vollständige betroffene Testmodul ohne generierte Checkout-Artefakte
  bestehen lassen.
- Beide Change-Record-Sprachen und beide Indizes gleichwertig halten.
- Frische Exact-Head-SonarQube-Cloud- und Hosted-Check-Evidence einholen,
  bevor ein ausgewählter Key als behoben oder die Delivery als verifiziert
  gilt.

## Implementierungsentscheidung und Begründung

Der Contract liefert nun jeden beobachteten HTTP-Status, jedes geparste
Evidence-Feld, jedes Record-Feld, jede Receive-Limit-Liste, jedes
Body-Byte-Ergebnis und jeden Event-Line-Count zuerst und danach seinen festen
Expected-Wert. Die innere Reihenfolge jedes Ausdrucks und das gesamte
Test-Setup bleiben erhalten. Keine Assertion wird hinzugefügt, gelöscht,
abgeschwächt oder unterdrückt, und kein produktives Envoy-Verhalten ändert
sich.

Dieser Batch beschränkt sich bewusst auf diese 19 geprüften Parent-Test-
Befunde. Andere SonarQube-Cloud-Observations bleiben getrennte Arbeit.

## Security-Auswirkung

Das Testmodul deckt kontrollierte Loopback-Transport- und Temporary-File-
Evidence-Contracts ab, aber die Änderung betrifft nur die Reihenfolge der
Diagnostik. Socket-Verhalten, Parser, Untrusted-Input-Pfad,
Temporary-File-Policy, Authorization-Entscheidung, Evidence-Regel,
Runtime-Helper, Konfiguration und Security-Control ändern sich nicht. Dieser
reine Maintainability-Batch beansprucht nicht, ein Security-Finding zu
beheben.

## Geänderte Dateien

- tests/test_envoy_transport_hardening_contract.py
- reports/audits/change-records/README.md und README.de.md
- dieses englische/deutsche Change-Record-Paar

## Ausgeführte Befehle

- Das vollständige betroffene Modul
  `tests.test_envoy_transport_hardening_contract` bestand nach dem normalen
  Current-Master-Update: 8 Tests in 1,144 Sekunden.
- Cross-Tree-AST-/Source-Inventar bestand: Exakt 19 `assertEqual`-Aufrufe
  sind Expected-zu-Actual-Operandentausche; alle anderen Operand-Ausdrücke
  bleiben erhalten.
- Der finale `git diff --check` wird nach diesem Delivery-Evidence-Update
  erneut ausgeführt.

## Tests und tatsächliche Ergebnisse

| Befehl oder Check | Ergebnis |
| --- | --- |
| `rtk proxy env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-owned path> <selected-python> -m unittest -v tests.test_envoy_transport_hardening_contract` | bestanden: 8 Tests in 1,144 Sekunden nach dem Current-Master-Update. |
| Cross-Tree-AST-/Source-Operand-Inventar | bestanden: 19 exakte Expected-zu-Actual-Tausche; alle anderen `self.assertEqual`-Operandpaare sind unverändert. |
| `git diff --check origin/master...HEAD` | wird nach diesem Change-Record-Update erneut ausgeführt. |

## Runtime-Evidence

Es änderte sich kein Connector-Runtime-Verhalten und es wird keines
beansprucht. Das betroffene Modul verwendet begrenzte Loopback-Fixtures und
temporäre Testdateien; es ist weder ein produktives Envoy-Deployment noch ein
Framework-/MRTS-Lauf.

## Nicht ausgeführte Prüfungen mit Begründung

- Keine vollständige Connector-Build- oder Runtime-Matrix: Die Änderung
  vertauscht nur Test-Diagnostik-Operanden und das vollständige betroffene
  Modul bestand.
- Kein Framework- oder MRTS-Test und keine -Änderung: Sie sind aus diesem
  Parent-only-Task ausgeschlossen.
- Hosted-Checks und SonarQube-Cloud-PR-Analyse werden von diesem lokalen
  Datensatz nicht beansprucht; sie benötigen einen gepushten exakten PR-Head
  und externe Evidence.

## Bekannte Einschränkungen

Dieser Batch behandelt nur 19 ausgewählte `python:S3415`-Observations. Er
beansprucht weder, den größeren SonarQube-Cloud-Backlog zu leeren, noch nicht
verfügbare Connector-Runtime-Umgebungen zu validieren.

## Verbleibende Risiken

Eine versehentliche Änderung über die ausgewählte Top-Level-Operand-Reihenfolge
hinaus könnte Fehlerdiagnostik irreführend machen. Das exakte Source-Inventar,
das fokussierte Modul und der finale Diff-Review verringern dieses Risiko.
Frische Hosted-Exact-Head-Analyse bleibt vor verifizierter Delivery erforderlich.

### Current-Parent-Master-Update — 2026-07-24

Der bestehende Draft-PR #107 wurde ohne Rebase regulär aktualisiert, indem
Parent-Master `a60dd0380332a24cf231a36775256d21a812c027` gemergt wurde. Der
daraus entstandene lokale Merge-Commit
`345b699eef301e6088286048cf13ba08f29345a9` führte die gemeinsamen
Change-Record-Indizes zusammen, wobei alle Current-Master-Einträge und der
Eintrag für PR 107 erhalten blieben. Er ändert weder Framework noch MRTS, sondern
übernimmt nur vorhandene Master-Historie. Der aktuelle PR-Base-Diff besteht
weiterhin aus diesem Parent-Test, diesem englisch/deutschen Change-Record-Paar
und den beiden Indizes, ohne eine durch dieses PR-Update verfasste Framework-,
MRTS-, Gitlink-, Envoy-Runtime-/Helper-Source-, Scanner-, Gate-, Suppression-
oder Security-Control-Änderung.

Das vollständige betroffene Modul bestand im aktuellen Merge-Tree mit acht
Tests; das unabhängige Cross-Tree-AST-/Source-Inventar verifizierte exakt 19
Expected-zu-Actual-Operandentausche. Hosted-Check-, SonarQube-Cloud-,
Quality-Gate-, Review-, Readiness- und Merge-Ergebnisse werden nur über
beobachtete Exact-Head-PR-Delivery-Metadaten beansprucht.

## Finaler Diff- und Review-Status

Der Parent-only-PR #107 ist das Delivery-Vehikel und enthält nun den normalen
Current-Master-Update-Merge
`345b699eef301e6088286048cf13ba08f29345a9` sowie dieses gepaarte
Delivery-Evidence-Update. Dieser Datensatz beansprucht weder Review-Approval,
Merge noch eine Default-Branch-Änderung. Vor dem geschützten Merge muss der PR
nicht mehr Draft sein und sein aktueller exakter Remote-Head muss bestehende
Hosted-Checks und SonarQube-Cloud-Analyse sowie einen aktualisierten
Review-Status haben; diese beobachteten Tatsachen gehören zu
Delivery-Metadaten und nicht zu einer unbeobachteten Behauptung dieses
Datensatzes.
