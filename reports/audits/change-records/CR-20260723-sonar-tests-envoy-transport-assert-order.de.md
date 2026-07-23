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
- Frische Exact-Head-SonarQube-Cloud- und Hosted-Check-Evidence für einen
  offenen, ungemergten Draft-PR einholen, bevor ein ausgewählter Key als
  behoben gilt.

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
  `tests.test_envoy_transport_hardening_contract` bestand nach der Korrektur:
  8 Tests in 1,141 Sekunden.
- AST-/Source-Inventar bestand: Exakt die 19 ausgewählten `assertEqual`-
  Aufrufe behalten ihre Operanden und verwenden Actual-first-Reihenfolge.
- `git diff --check` bestand.

## Tests und tatsächliche Ergebnisse

| Befehl oder Check | Ergebnis |
| --- | --- |
| `rtk proxy -- env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-owned path> <selected-python> -m unittest -v tests.test_envoy_transport_hardening_contract` | bestanden: 8 Tests in 1,141 Sekunden. |
| AST-/Source-Operand-Inventar der Zeilen 50, 51, 75, 111, 194, 195, 200, 204-209, 212, 227 und 292-295 | bestanden: 19 ausgewählte Aufrufe, alle Actual-first. |
| `git diff --check` | bestanden. |

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
  Datensatz nicht beansprucht; sie benötigen einen gepushten exakten
  Draft-PR-Head und externe Evidence.

## Bekannte Einschränkungen

Dieser Batch behandelt nur 19 ausgewählte `python:S3415`-Observations. Er
beansprucht weder, den größeren SonarQube-Cloud-Backlog zu leeren, noch nicht
verfügbare Connector-Runtime-Umgebungen zu validieren.

## Verbleibende Risiken

Eine versehentliche Änderung über die ausgewählte Top-Level-Operand-Reihenfolge
hinaus könnte Fehlerdiagnostik irreführend machen. Das exakte Source-Inventar,
das fokussierte Modul und der finale Diff-Review verringern dieses Risiko.
Frische Hosted-Exact-Head-Analyse bleibt vor verifizierter Delivery erforderlich.

## Finaler Diff- und Review-Status

Lokale Source-Korrektur und ihr fokussierter Test bestanden auf einem
Parent-only-Task-Branch, der auf
`5b8db00d44ab24f3a9f4216a00f7edee977b6898` basiert. Dieser Datensatz
beansprucht keine nicht beobachteten Hosted-Check-, SonarQube-Cloud-, Review-,
Merge- oder Default-Branch-Ergebnisse. Die vorgesehene Delivery ist
ausschließlich ein offener, ungemergter Draft-PR.
