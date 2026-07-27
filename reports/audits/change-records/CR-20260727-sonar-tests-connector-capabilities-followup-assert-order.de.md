# Change Record: Parent-Connector-Capabilities-Folge-Assertion-Reihenfolge für SonarQube Cloud S3415

**Sprache:** [English](CR-20260727-sonar-tests-connector-capabilities-followup-assert-order.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-tests-connector-capabilities-followup-assert-order |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent-SonarQube-Cloud-`python:S3415`: AZ-KYVU7fYmbqbBXVNGv (210), AZ-KYVU7fYmbqbBXVNGw (211), AZ-KYVU7fYmbqbBXVNGx (212), AZ-KYVU7fYmbqbBXVNGy (240), AZ-KYVU7fYmbqbBXVNGz (241), AZ-KYVU7fYmbqbBXVNG0 (243), AZ-KYVU7fYmbqbBXVNG1 (244), AZ-KYVU7fYmbqbBXVNG2 (247), AZ-KYVU7fYmbqbBXVNG3 (248), AZ-KYVU7fYmbqbBXVNG4 (286), AZ-KYVU7fYmbqbBXVNG5 (306), AZ-KYVU7fYmbqbBXVNG6 (311), AZ-KYVU7fYmbqbBXVNG7 (315), AZ-KYVU7fYmbqbBXVNG8 (319), AZ-KYVU7fYmbqbBXVNG9 (323), AZ-KYVU7fYmbqbBXVNG- (327) und AZ-KYVU7fYmbqbBXVNG_ (332). |
| Grenze | Parent-Testquelltext sowie dieses englisch/deutsche Change-Record-Paar und Indizes. Produktionsverhalten der Connector-Capabilities, Framework, MRTS, Gitlinks, Scanner-Konfiguration, Quality Gates, Suppressions und externer Sonar-Issue-Status bleiben unverändert. |

## Motivation und Entscheidung

Siebzehn ausgewählte Assertions übergaben konstante erwartete
Capability-/Provenance-States vor beobachteten Manifest-, Provenance-, Record-,
Merge- oder Evidence-Feldern. Diese Änderung vertauscht nur diese ersten zwei
Argumente zu `Istwert, Erwartungswert`. Die Methoden behalten ihre temporären
Fixture-Repositories, Gitlink-Provenance-Fälle, Staleness-Prüfungen und
Runtime-Merge-Assertions unverändert.

## Validierung

| Prüfung | Ergebnis |
| --- | --- |
| Vier fokussierte Parent-only-Methoden vor der Änderung | bestanden: 4 Tests in 0,523 s. |
| Dieselben Methoden nach der Änderung | bestanden: 4 Tests in 0,536 s. |
| Strukturelles AST-Inventar | bestanden: genau 17 ausgewählte Zeilen haben einen Dictionary-Subscript-Istwert vor einem konstanten Erwartungswert. |
| Bilinguale Change-Record-Validierung | bestanden: `tests.test_bilingual_docs`, 13 Tests in 0,033 s. |
| `git diff --check` | bestanden, nachdem das vollständige B08-Traceability-Paar und die Indizes hinzugefügt wurden. |

## Motivation und Problemstellung

Die konkrete Sonar-Regel, der Parent-Testumfang und die Begründung für den
Erhalt des Verhaltens stehen im vorhergehenden Abschnitt
`## Motivation und Entscheidung`. Diese strukturelle Korrektur ändert weder
den dokumentierten Quelltext noch das Testverhalten.

## Akzeptanzkriterien

- Die bereits dokumentierte Remediation und fokussierte Validierung bleiben
  unverändert.
- Dieses englisch/deutsche Change-Record-Paar behält gleichwertige technische
  Fakten.
- Blockierte, nicht ausgeführte oder ausstehende gehostete Evidence wird nicht
  als bestanden dargestellt.

## Implementierungsentscheidung und Begründung

Die bestehende Begründung und Validierung bleiben erhalten. Die kanonischen
Change-Record-Überschriften werden ergänzt, statt den Dokumentationschecker zu
schwächen oder eine recordspezifische Ausnahme zu schaffen.

## Geänderte Dateien

Der ursprüngliche versionierte Umfang steht in `## Identität` und der
vorhergehenden Implementierungsbeschreibung. Dieses Follow-up ändert nur die
Struktur dieses Change-Record-Paars.

## Ausgeführte Befehle

Die exakten Befehle und beobachteten Ergebnisse bleiben in `## Validierung`;
diese strukturelle Korrektur klassifiziert kein Ergebnis neu.

## Security-Auswirkung

Der bestehende nachfolgende Abschnitt bleibt für diese konkrete Grenze
maßgeblich. Diese Normalisierung ändert keine Sicherheitskontrolle.

## Security-Auswirkung und Einschränkungen

`not_applicable` für Produktionscode: Es handelt sich ausschließlich um
Testdiagnostik. Die Tests behalten ihre Provenance- und Runtime-Result-
Integrity-Assertions. Der lokale Kandidat ist uncommittet; es gab keine
gehostete Sonar-Analyse, keine GitHub-CI, keinen Commit, Push, Pull Request
oder Master-Merge. Die aufgeführten Keys bleiben OPEN, bis ein ausgelieferter
Head analysiert wird.

## Runtime-Evidence

Diese strukturelle Korrektur beansprucht keine zusätzliche Runtime-Evidence;
die bestehende Parent-Testmethoden-Validierung behält ihren dokumentierten
Umfang.

## Bekannte Einschränkungen

Die fokussierte Validierung ist bewusst enger als das vollständige
Framework-abhängige Aggregat-Testmodul und eine gehostete Analyse.

## Verbleibende Risiken

Die Record-Normalisierung führt kein neues Risiko ein. Ergebnisse eines
späteren Framework-Aggregats oder einer gehosteten Analyse bleiben bis zu
ihrer tatsächlichen Beobachtung ausstehend.

## Nicht ausgeführte Prüfungen mit Begründung

Für diese reine Dokumentationskorrektur werden kein zusätzlicher
Connector-Runtime-Test, kein Framework-Aggregat und kein gehosteter Check
ausgeführt; die ursprünglichen Validierungsgrenzen bleiben unverändert.

## Finaler Diff- und Review-Status

Die frühere Delivery-Formulierung ist eine Momentaufnahme der ursprünglichen
lokalen Validierung. Dieser Record behauptet keine finale PR-Verifikation,
keinen Merge und keinen Sonar-Issue-Abschluss für einen späteren Delivery-Head.
