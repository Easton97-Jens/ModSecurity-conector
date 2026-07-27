# Change Record: Parent-Apache-Request-Transaction-Cleanup-Assertion-Reihenfolge für SonarQube Cloud S3415

**Sprache:** [English](CR-20260727-sonar-tests-apache-request-transaction-cleanup-assert-order.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-tests-apache-request-transaction-cleanup-assert-order |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent-SonarQube-Cloud-`python:S3415`-Code-Smell AZ-KYVVIfYmbqbBXVNHJ in Zeile 64. |
| Grenze | Parent-Testquelltext sowie dieses englisch/deutsche Change-Record-Paar und Indizes. Apache-Produktions-C-Quelltext, Framework, MRTS, Gitlinks, Scanner-Konfiguration, Quality Gates, Suppressions und externer Sonar-Issue-Status bleiben unverändert. |

## Motivation und Entscheidung

Die ausgewählte Assertion übergab das erwartete Literal `1` vor ihrer
beobachteten In-Memory-`str.count`-Auswertung. Diese Änderung vertauscht nur
diese zwei Argumente zu `Istwert, Erwartungswert`. Derselbe String, dasselbe
Count-Prädikat und derselbe Request-Cleanup-Vertrag bleiben unverändert.

## Validierung

| Prüfung | Ergebnis |
| --- | --- |
| Vollständiges Parent-only-Testmodul vor der Änderung | bestanden: 5 Tests in 0,004 s. |
| Dasselbe Modul nach der Änderung | bestanden: 5 Tests in 0,004 s. |
| Strukturelles AST-Prädikat | bestanden: Zeile 64 hat das `str.count`-Ergebnis zuerst und das Integer-Literal `1` danach. |
| Bilinguale Change-Record-Validierung | bestanden: `tests.test_bilingual_docs`, 13 Tests in 0,033 s. |
| `git diff --check` | bestanden, nachdem das vollständige B05-Traceability-Paar und die Indizes hinzugefügt wurden. |

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

`not_applicable`: Es handelt sich ausschließlich um Testdiagnostik. Der Test
liest weiterhin dieselben Parent-Apache-C-/Header-/Check-Script-Quellen; kein
Produktions-Request- oder Transaktionsverhalten änderte sich. Der lokale
Kandidat ist uncommittet; es gab keine gehostete Sonar-Analyse, keine GitHub-CI,
keinen Commit, Push, Pull Request oder Master-Merge. Der Sonar-Key bleibt OPEN,
bis ein ausgelieferter Head analysiert wird.

## Runtime-Evidence

Diese strukturelle Korrektur beansprucht keine zusätzliche Runtime-Evidence;
die fokussierte Parent-Testmethoden-Validierung behält ihren dokumentierten
Umfang.

## Bekannte Einschränkungen

Die fokussierte Validierung ist bewusst enger als ein nativer Apache-Build
oder eine gehostete Analyse.

## Verbleibende Risiken

Die Record-Normalisierung führt kein neues Risiko ein. Spätere
Connector-Runtime- oder gehostete Ergebnisse werden erst nach ihrer tatsächlichen
Beobachtung als Evidenz behandelt.

## Nicht ausgeführte Prüfungen mit Begründung

Für diese reine Dokumentationskorrektur werden kein zusätzlicher nativer
Apache-Build und kein gehosteter Check ausgeführt; die ursprünglichen
Validierungsgrenzen bleiben unverändert.

## Finaler Diff- und Review-Status

Die frühere Delivery-Formulierung ist eine Momentaufnahme der ursprünglichen
lokalen Validierung. Dieser Record behauptet keine finale PR-Verifikation,
keinen Merge und keinen Sonar-Issue-Abschluss für einen späteren Delivery-Head.
